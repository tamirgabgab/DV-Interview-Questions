#!/usr/bin/env python3
"""Check every page of the built site at phone width.

    mkdocs build --strict && python tools/check_phone.py [site] [--shots DIR]

Serves the site locally, opens each page in Chromium at 390 x 844 px with every collapsible
block open (hints and solutions included), and fails when the page scrolls sideways or a
script throws. A full-page screenshot of each page goes to --shots (CI uploads them as an
artifact). Needs Playwright: pip install -r requirements-dev.txt and
python -m playwright install chromium (or --browser PATH to an installed Chromium).

In a sandbox without access to the CDNs, --offline ignores errors of external scripts and
--route REGEX=FILE serves a CDN script from a local copy (e.g. MathJax, so math is laid out
as on the live site).
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

OPEN_ALL = """() => {
  document.querySelectorAll("details").forEach((d) => (d.open = true));
  document.querySelectorAll(".hint-locked").forEach((d) => d.classList.remove("hint-locked"));
}"""


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
    args = ap.parse_args(argv)

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

    failures = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1)
        for spec in args.route:
            pattern, file = spec.split("=", 1)
            ctx.route(re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file))
        for rel in pages:
            url = base + rel[: -len("index.html")]
            page = ctx.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda e, errors=errors: errors.append(str(e)))
            try:
                page.goto(url, wait_until="networkidle", timeout=60_000)
            except Exception as e:   # a CDN that never answers: check what has loaded
                errors.append(f"load: {e}")
            page.evaluate(OPEN_ALL)
            page.wait_for_timeout(800)
            info = page.evaluate(INSPECT, WIDTH)
            if args.offline:
                errors = [e for e in errors if not re.search(r"https?://(?!127\.0\.0\.1)", e)]
            name = rel[: -len("/index.html")].replace("/", "__") or "home"
            page.screenshot(path=str(shots / f"{name}.png"), full_page=True)
            page.close()

            bad = info["scrollWidth"] > WIDTH + 1 or errors
            failures += bool(bad)
            status = "FAIL" if bad else "ok"
            print(f"{status:4}  {rel[: -len('index.html')] or '/'}  width {info['scrollWidth']}")
            if info["scrollWidth"] > WIDTH + 1:
                for w in info["wide"] or ["(no single element found; check the screenshot)"]:
                    print(f"        too wide: {w}")
            for e in errors:
                print(f"        script error: {e[:200]}")
        browser.close()
    server.shutdown()
    print(f"{len(pages)} pages checked at {WIDTH} px, {failures} with problems; screenshots in {shots}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
