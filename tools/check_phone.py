#!/usr/bin/env python3
"""Check every page of the built site at phone width.

    mkdocs build --strict && python tools/check_phone.py [site] [--shots DIR]

Serves the site locally, opens each page in Chromium at 390 x 844 px with every collapsible
block open (hints and solutions included), and fails when the page scrolls sideways or a
script throws. A full-page screenshot of each page goes to --shots (CI uploads them as an
artifact). Needs Playwright: pip install -r requirements-dev.txt and
python -m playwright install chromium (or --browser PATH to an installed Chromium).

It also warns (without failing) about display math wider than its column: such an
equation scrolls sideways on its own, which is easy to miss on a phone; split it with
`aligned`. It warns, too, about SVG text drawn smaller than 9 px at this width (figures
and explorer boxes that shrink to fit the phone): one line per figure with its smallest
size. --scheme dark runs the same check in dark mode (CI runs it on manual request).

It fails when the enlarge button of a figure covers SVG text: reading-tools.js moves the
button above a drawing whose corner holds text (see `fig-wrap--above` in docs/stylesheets/), and
this check runs the same test on every figure of the open page, the live figures of the
explorer boxes included, one line per covered figure.

In a sandbox without access to the CDNs, --offline ignores errors of external scripts and
--route REGEX=FILE serves a CDN script from a local copy (e.g. MathJax, so math is laid out
as on the live site). --local-cdn does both for the copies tools/dev_setup.sh keeps in
.cache/cdn (MathJax, Mermaid, WaveDrom) and runs axe-core from there unless --axe is given.

Every page's line also gives its weight: the HTML in KB, and what the browser fetched for it
in all (the HTML, the styles, the scripts, the fonts) in KB and requests, so a page that
grows heavy is seen; a page whose HTML is over --weight-warn KB (400) gets a warning, and the
summary names the three heaviest pages.

--axe PATH runs axe-core (its axe.min.js, e.g. from npm) on every page and warns about
serious and critical violations without failing: the count per page is printed with the
rule id and the first element, so the next accessibility regression is visible in the CI
log. --axe-fail turns those warnings into failures, and --small-fail does the same for SVG
text under MIN_TEXT px (CI runs with both).
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import sys
import threading
from pathlib import Path

WIDTH, HEIGHT = 390, 844

# Elements that are allowed to be wider than the screen because they scroll on their own
SCROLLERS = "pre, .highlight, .md-typeset__scrollwrap, .tabbed-labels, mjx-container[display='true'], .stepper"

INSPECT = """(width) => {
  const scrollers = %r;
  const out = [];
  for (const el of document.querySelectorAll(".md-container *")) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || (r.right <= width + 1 && r.left >= -1)) continue;
    if (el.closest(scrollers) || el.closest(".md-sidebar")) continue;   // the menu drawer sits off screen
    const parent = el.parentElement && el.parentElement.getBoundingClientRect();
    if (parent && (parent.right > width + 1 || parent.left < -1) && !el.parentElement.matches(scrollers)) continue;
    out.push(`${el.tagName.toLowerCase()}.${String(el.className).trim().replace(/\\s+/g, ".").slice(0, 40)}`
             + ` [${Math.round(r.left)}..${Math.round(r.right)}] "${(el.textContent || "").trim().slice(0, 40)}"`);
    if (out.length >= 3) break;
  }
  return { scrollWidth: document.documentElement.scrollWidth, wide: out };
}""" % SCROLLERS

# Display math that is wider than its column (it scrolls inside the page); the warning shows
# the start of the equation as text.
WIDE_MATH = """async () => {
  if (window.MathJax && MathJax.startup && MathJax.startup.promise) {
    try { await MathJax.startup.promise; } catch (e) {}
  }
  const out = [];
  for (const el of document.querySelectorAll("mjx-container[display='true']")) {
    const box = el.parentElement;            // div.arithmatex, the width of the column
    const over = el.getBoundingClientRect().width - box.clientWidth;
    if (box.clientWidth === 0 || over <= 1) continue;
    const mml = el.querySelector("mjx-assistive-mml");
    const text = (mml ? mml.textContent : el.textContent).replace(/\\s+/g, " ").trim();
    out.push(`+${Math.round(over)} px: ${text.slice(0, 60)}`);
  }
  return out;
}"""

# SVG text smaller than MIN_TEXT px on screen: the font size times the scale of the figure
# (a viewBox wider than the phone shrinks every label). One entry per figure, its smallest
# text; the figure is named by its aria-label, else by its first text.
MIN_TEXT = 9
SMALL_TEXT = """(min) => {
  const out = [];
  for (const svg of document.querySelectorAll(".md-content svg")) {
    if (svg.closest("mjx-container") || svg.parentElement.closest(".md-content svg")) continue;
    let small = Infinity, sample = "";
    for (const t of svg.querySelectorAll("text")) {
      const r = t.getBoundingClientRect();
      const m = t.getScreenCTM();
      if (!m || r.width === 0 || !t.textContent.trim()) continue;
      const px = parseFloat(getComputedStyle(t).fontSize) * Math.hypot(m.a, m.b);
      if (px < small) { small = px; sample = t.textContent.trim(); }
    }
    if (small >= min) continue;
    const name = svg.getAttribute("aria-label") || (svg.querySelector("text") || {}).textContent || "";
    const box = svg.closest(".explorer");
    out.push(`${small.toFixed(1)} px ("${sample.slice(0, 20)}") in ${box ? "box " + box.dataset.kind + ": " : ""}`
             + name.trim().replace(/\\s+/g, " ").slice(0, 60));
  }
  return out;
}"""

# The enlarge button of a figure over its SVG text (reading-tools.js should have moved the
# button above the drawing): one entry per covered figure, named like SMALL_TEXT names them.
ENLARGE_COVERS = """() => {
  const out = [];
  if (!window.dvqFigCovers) return out;
  for (const wrap of document.querySelectorAll(".md-content .fig-wrap")) {
    if (wrap.closest(".fig-lightbox") || !window.dvqFigCovers(wrap)) continue;
    const svg = wrap.querySelector("svg");
    const name = svg.getAttribute("aria-label") || (svg.querySelector("text") || {}).textContent || "";
    const box = svg.closest(".explorer");
    out.push(`${box ? "box " + box.dataset.kind + ": " : ""}` + name.trim().replace(/\\s+/g, " ").slice(0, 60));
  }
  return out;
}"""

# axe-core on the open page; only the rules whose impact is serious or critical are reported.
# Material's own markup is excluded (the header, drawer, footer and search); the check is
# about the question content and the site's components.
AXE = """async () => {
  const r = await axe.run({ exclude: [[".md-header"], [".md-sidebar"], [".md-footer"], [".md-search"]] }, {
    runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"] },
    resultTypes: ["violations"],
  });
  return r.violations
    .filter((v) => v.impact === "serious" || v.impact === "critical")
    .map((v) => ({ id: v.id, impact: v.impact, count: v.nodes.length,
                   first: v.nodes[0] ? v.nodes[0].target.join(" ").slice(0, 70) : "",
                   help: v.help.slice(0, 70) }));
}"""

# Every collapsible block open, and every explorer box built (they are built lazily, when
# they near the viewport) with its folds open (closed on a phone at first).
OPEN_ALL = """async () => {
  document.querySelectorAll("details").forEach((d) => (d.open = true));
  document.querySelectorAll(".hint-locked").forEach((d) => d.classList.remove("hint-locked"));
  if (window.dvqExplorers) await window.dvqExplorers.ready();
  document.querySelectorAll(".explorer").forEach((box) => box.querySelectorAll(".is-folded > .ex-proof-title .ex-fold-btn, .is-folded > .ex-fold-title .ex-fold-btn").forEach((f) => f.click()));
}"""


# The CDN scripts the pages load and their copies in .cache/cdn (tools/dev_setup.sh), as
# --route specs for --local-cdn.
CDN_DIR = Path(__file__).resolve().parent.parent / ".cache" / "cdn"
LOCAL_CDN = [
    (r"mathjax@3\.2\.2/es5/tex-mml-chtml\.js", "mathjax/es5/tex-mml-chtml.js"),
    (r"unpkg\.com/mermaid@11/dist/mermaid\.min\.js", "mermaid/dist/mermaid.min.js"),
    (r"wavedrom@3\.5\.0/skins/default\.js", "wavedrom/skins/default.js"),
    (r"wavedrom@3\.5\.0/wavedrom\.min\.js", "wavedrom/wavedrom.min.js"),
]


def local_cdn_routes() -> list[str]:
    """The --route specs of the local CDN copies; exits when a copy is missing."""
    specs = []
    for pattern, rel in LOCAL_CDN:
        if not (CDN_DIR / rel).is_file():
            sys.exit(f"--local-cdn: {CDN_DIR / rel} is missing; run tools/dev_setup.sh")
        specs.append(f"{pattern}={CDN_DIR / rel}")
    return specs


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(site: Path) -> tuple[http.server.ThreadingHTTPServer, str]:
    handler = functools.partial(QuietHandler, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--shots", default=".cache/phone", help="screenshot directory")
    ap.add_argument("--browser", help="path to a Chromium executable")
    ap.add_argument("--offline", action="store_true", help="ignore errors of external scripts")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE",
                    help="serve requests matching REGEX from a local file")
    ap.add_argument("--only", help="check only pages whose path matches this regex")
    ap.add_argument("--scheme", choices=["light", "dark"], default="light",
                    help="colour scheme of the browser (the site follows it)")
    ap.add_argument("--axe", metavar="AXE_MIN_JS", help="run axe-core from this file and warn about violations")
    ap.add_argument("--axe-fail", action="store_true", help="count axe violations as failures")
    ap.add_argument("--small-fail", action="store_true", help=f"count SVG text under {MIN_TEXT} px as a failure")
    ap.add_argument("--local-cdn", action="store_true",
                    help="--offline with the CDN copies of .cache/cdn (tools/dev_setup.sh), axe-core included")
    ap.add_argument("--weight-warn", type=int, default=400, metavar="KB", help="warn about a page whose HTML is heavier than this (400)")
    args = ap.parse_args(argv)
    if args.local_cdn:
        args.offline = True
        args.route += local_cdn_routes()
        if not args.axe and (CDN_DIR / "axe-core" / "axe.min.js").is_file():
            args.axe = str(CDN_DIR / "axe-core" / "axe.min.js")

    from playwright.sync_api import sync_playwright

    site = Path(args.site).resolve()
    if not site.is_dir():
        print(f"site directory not found: {site}")
        return 1
    pages = sorted(p.relative_to(site).as_posix() for p in site.rglob("index.html"))
    if args.only:
        pages = [p for p in pages if re.search(args.only, p)]
    shots = Path(args.shots)
    shots.mkdir(parents=True, exist_ok=True)
    server, base = serve(site)

    failures = warned = axe_pages = small_pages = heavy = 0
    weights: list[tuple[float, str]] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1, service_workers="block",
                                  color_scheme=args.scheme)
        for spec in args.route:
            pattern, file = spec.split("=", 1)
            ctx.route(re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file))
        for rel in pages:
            url = base + rel[: -len("index.html")]
            page = ctx.new_page()
            errors: list[str] = []
            fetched: list[int] = []
            page.on("pageerror", lambda e, errors=errors: errors.append(str(e)))
            page.on("response", lambda r, fetched=fetched: fetched.append(int(r.headers.get("content-length") or 0)))
            try:
                page.goto(url, wait_until="networkidle", timeout=60_000)
            except Exception as e:   # a CDN that never answers: check what has loaded
                errors.append(f"load: {e}")
            page.evaluate(OPEN_ALL)
            page.wait_for_timeout(800)
            info = page.evaluate(INSPECT, WIDTH)
            wide_math = page.evaluate(WIDE_MATH)
            small_text = page.evaluate(SMALL_TEXT, MIN_TEXT)
            covered = page.evaluate(ENLARGE_COVERS)
            axe = []
            if args.axe:
                page.add_script_tag(path=args.axe)
                axe = page.evaluate(AXE)
            if args.offline:
                errors = [e for e in errors if not re.search(r"https?://(?!127\.0\.0\.1)", e)]
            name = rel[: -len("/index.html")].replace("/", "__") or "home"
            page.screenshot(path=str(shots / f"{name}.png"), full_page=True)
            page.close()

            bad = info["scrollWidth"] > WIDTH + 1 or errors or covered or (args.axe_fail and axe) or (args.small_fail and small_text)
            failures += bool(bad)
            status = "FAIL" if bad else "ok"
            html_kb = (site / rel).stat().st_size / 1024
            weights.append((html_kb, rel[: -len("/index.html")] or "/"))
            print(f"{status:4}  {rel[: -len('index.html')] or '/'}  width {info['scrollWidth']}  "
                  f"{html_kb:.0f} KB html, {sum(fetched) / 1024:.0f} KB in {len(fetched)} requests")
            if html_kb > args.weight_warn:
                heavy += 1
                print(f"        warn heavy page: {html_kb:.0f} KB of HTML, over {args.weight_warn} KB")
            if info["scrollWidth"] > WIDTH + 1:
                for w in info["wide"] or ["(no single element found; check the screenshot)"]:
                    print(f"        too wide: {w}")
            for e in errors:
                print(f"        script error: {e[:200]}")
            for w in covered:
                print(f"        enlarge button covers text: {w}")
            for w in wide_math:
                print(f"        warn wide math {w}")
            for w in small_text:
                print(f"        {'small text' if args.small_fail else 'warn small text'} {w}")
            for v in axe:
                print(f"        {'axe' if args.axe_fail else 'warn axe'} {v['impact']} {v['id']} x{v['count']}: "
                      f"{v['help']} ({v['first']})")
            warned += bool(wide_math)
            small_pages += bool(small_text)
            axe_pages += bool(axe)
        browser.close()
    server.shutdown()
    heaviest = ", ".join(f"{name} ({kb:.0f} KB)" for kb, name in sorted(weights, reverse=True)[:3])
    print(f"{len(pages)} pages checked at {WIDTH} px ({args.scheme}), {failures} with problems, "
          f"{warned} with wide math warnings, {small_pages} with text under {MIN_TEXT} px, {axe_pages} with axe violations, "
          f"{heavy} over {args.weight_warn} KB of HTML (the heaviest: {heaviest}); screenshots in {shots}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
