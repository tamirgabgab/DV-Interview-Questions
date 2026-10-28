#!/usr/bin/env python3
"""Click every button of every explorer box on the built site.

    mkdocs build --strict && python tools/check_explorers.py [site]

Serves the site locally and opens every page that has an explorer box (`div.explorer`) in
Chromium at 390 x 844 px, with every collapsible block open. In each box it clicks every
visible, enabled button once, in document order (the box is queried again before each
click, since the views redraw their controls), lets a running play go on for a moment,
then presses "reset everything". It fails when a script throws or logs a console error
(a resource from another host that fails to load is the network and does not count), and
when the page scrolls sideways after a box was clicked through. The failing button is
named in the report (its aria-label, text or title).

Then, for every box, the link and the remembered state: the box's controls are changed one
by one after a draw with a fixed seed where the box has one (a range or number field to
another value, a select to the next option, a checkbox toggled; the play speed is left
alone), and the box is compared with the same box opened
from its "copy link" URL in a fresh browser, and with the box after a reload of the page
(the remembered state, with its notice). Different control values fail the check; a
different drawing (hidden elements aside) is a warning, since a box may draw from its
history. "Reset everything" must then forget the state.
--no-links skips this part.

Needs Playwright, as tools/check_phone.py. In a sandbox without access to the CDNs,
--offline ignores errors of external scripts and --route REGEX=FILE serves a CDN script
from a local copy; --local-cdn does both with the copies of .cache/cdn (tools/dev_setup.sh);
--only REGEX checks only the matching pages. --shard K/N checks the K-th
of N parts (CI runs the parts on parallel runners): the pages are dealt by their number of
boxes, the largest first, to the part with the fewest boxes so far.
"""

from __future__ import annotations

import argparse
import functools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_phone import HEIGHT, OPEN_ALL, WIDTH, local_cdn_routes, serve  # noqa: E402

BUTTONS = "button, [role=button]"

# The number of boxes on the page, after the lazy ones were built.
BOXES = """async () => {
  if (window.dvqExplorers) await window.dvqExplorers.ready();
  return document.querySelectorAll(".explorer").length;
}"""

COUNT = """([b, sel]) => document.querySelectorAll(".explorer")[b].querySelectorAll(sel).length"""

# Click the i-th button of box b if it is shown and enabled; close a lightbox it opened.
# The box's folds are opened first (a reset closes them again on a phone), and their own
# buttons are not clicked. Returns the button's name, or null when it was skipped.
CLICK = """([b, i, sel]) => {
  const box = document.querySelectorAll(".explorer")[b];
  if (box) box.querySelectorAll(".is-folded > .ex-proof-title .ex-fold-btn, .is-folded > .ex-fold-title .ex-fold-btn").forEach((f) => f.click());
  const el = box && box.querySelectorAll(sel)[i];
  if (!el || el.classList.contains("ex-fold-btn") || el.disabled || el.getAttribute("aria-disabled") === "true" || !el.getClientRects().length) return null;
  const name = (el.getAttribute("aria-label") || el.textContent || el.getAttribute("title") || el.getAttribute("class") || "?").trim().replace(/\\s+/g, " ").slice(0, 50);
  if (typeof el.click === "function") el.click();           // an SVG button has no click()
  else el.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
  const lb = document.querySelector(".fig-lightbox.is-open .fig-lb-close");
  if (lb) lb.click();
  return name;
}"""

# Stop a play that is still running and reset the box.
RESET = """(b) => {
  const box = document.querySelectorAll(".explorer")[b];
  const btn = box.querySelector(".ex-reset-all");
  if (btn) btn.click();
  return box.dataset.kind;
}"""

WIDTH_NOW = "() => document.documentElement.scrollWidth"

# Draw with seed 4242 where the box has a seed field, then change every control of box b in
# document order (re-queried after each change); returns the number changed. An editing aid
# marked data-nolink is no control (see controlsOf in core.js).
CHANGE = """(b) => {
  const box = document.querySelectorAll(".explorer")[b];
  const seed = box.querySelector(".ex-seed");
  if (seed) { seed.value = "4242"; seed.dispatchEvent(new Event("change", { bubbles: true })); }
  const ctl = () => [...box.querySelectorAll("input, select, textarea")].filter((el) => !el.matches(".ex-seed, .ex-scrub, [data-nolink]"));
  let changed = 0;
  for (let i = 0; i < ctl().length; i++) {
    const el = ctl()[i];
    if (el.disabled || !el.getClientRects().length || el.classList.contains("ex-speed")) continue;
    if (el.type === "checkbox") el.checked = !el.checked;
    else if (el.tagName === "SELECT") {
      const opts = [...el.options].filter((o) => !o.disabled);
      if (opts.length < 2) continue;
      el.value = opts[(opts.findIndex((o) => o.value === el.value) + 1) % opts.length].value;
    } else if (el.type === "range" || el.type === "number") {
      const min = el.min === "" ? 0 : Number(el.min), max = el.max === "" ? Number(el.value) + 10 : Number(el.max);
      const step = el.step === "" || el.step === "any" ? 1 : Number(el.step), now = Number(el.value);
      let v = min + Math.round(((max - min) * 0.37) / step) * step;
      if (Math.abs(v - now) < step / 2) v = now + step <= max ? now + step : now - step;
      if (v < min || v > max) continue;
      el.value = String(Number(v.toFixed(6)));
    } else continue;
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
    changed++;
  }
  return changed;
}"""

# Box b as compared across pages: its control values and its drawing without the header,
# the notices, the key hint, what is hidden and the reserved text heights. The seed counts unless the box links with
# its own codec (`#state-`), whose data stands for the draw.
SNAP = """([b, own]) => {
  const box = document.querySelectorAll(".explorer")[b];
  const values = [...box.querySelectorAll("input, select, textarea")].filter((el) => !el.matches(".ex-seed, .ex-scrub, [data-nolink]"))
    .map((el) => el.type === "checkbox" ? el.checked : el.value);
  const seed = box.querySelector(".ex-seed");
  if (seed && !own) values.push(`seed ${seed.value}`);
  const copy = box.cloneNode(true);
  // an answer line that is off keeps its last text only to hold its height (core.js answer)
  copy.querySelectorAll(".ex-bar, .ex-restored, .ex-keys, [hidden], .ex-answer--off").forEach((el) => el.remove());
  // the steady heights (core.js) and the enlarge button moved above a figure (reading-tools.js)
  // depend on the steps the box went through, not on its state
  copy.querySelectorAll("[style]").forEach((el) => { el.style.minHeight = ""; if (!el.getAttribute("style")) el.removeAttribute("style"); });
  copy.querySelectorAll("[data-fig-above]").forEach((el) => el.removeAttribute("data-fig-above"));
  copy.querySelectorAll(".fig-wrap--above").forEach((el) => el.classList.remove("fig-wrap--above"));
  // attributes in one order: a figure refitted on another path sets the same attributes in
  // another order (style before data-fit-base), which is the same drawing
  [copy, ...copy.querySelectorAll("*")].forEach((el) => {
    const attrs = [...el.attributes].map((a) => [a.name, a.value]).sort((x, y) => (x[0] < y[0] ? -1 : 1));
    attrs.forEach(([name]) => el.removeAttribute(name));
    attrs.forEach(([name, value]) => { try { el.setAttribute(name, value); } catch (e) { /* not a valid name: dropped on both sides */ } });
  });
  return { values, html: copy.innerHTML, restored: !!box.querySelector(".ex-restored") };
}"""


def first_difference(a: str, b: str) -> str:
    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
    return f"at {i}: {a[max(0, i - 40):i + 60]!r} / {b[max(0, i - 40):i + 60]!r}"


def open_page(ctx, url: str, errors: list[str]):
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("dialog", lambda d: d.dismiss())
    try:
        page.goto(url, wait_until="networkidle", timeout=60_000)
    except Exception as e:
        errors.append(f"load: {e}")
    page.evaluate(OPEN_ALL)
    page.wait_for_timeout(500)
    return page


def check_links(browser, routes, url: str) -> tuple[list[str], list[str]]:
    """The link and the remembered state of every box on the page at url: problems and
    warnings."""
    problems: list[str] = []
    warnings: list[str] = []
    errors: list[str] = []

    def context():
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1, service_workers="block")
        for pattern, handler in routes:
            ctx.route(pattern, handler)
        return ctx

    ctx = context()
    page = open_page(ctx, url, errors)
    n_boxes = page.evaluate("() => document.querySelectorAll('.explorer').length")
    page.close()
    for b in range(n_boxes):
        page = open_page(ctx, url, errors)
        kind = page.evaluate("(b) => document.querySelectorAll('.explorer')[b].dataset.kind", b)
        if not page.evaluate(CHANGE, b):
            page.close()
            continue
        page.wait_for_timeout(500)                          # the state is saved after 300 ms
        link = page.evaluate("(b) => dvqExplorers.linkOf(document.querySelectorAll('.explorer')[b])", b)
        own = link.startswith("#state-")
        want = page.evaluate(SNAP, [b, own])
        page.close()

        fresh = context()
        other = open_page(fresh, url + link, errors)
        got = other.evaluate(SNAP, [b, own])
        other.close()
        fresh.close()
        if got["values"] != want["values"]:
            problems.append(f"{kind} {b}: the link {link[:80]} gives the controls {got['values']}, not {want['values']}")
        elif got["html"] != want["html"]:
            warnings.append(f"{kind} {b}: the link {link[:80]} draws another box, {first_difference(want['html'], got['html'])}")

        page = open_page(ctx, url, errors)
        got = page.evaluate(SNAP, [b, own])
        if not got["restored"]:
            problems.append(f"{kind} {b}: no remembered state after a reload")
        elif got["values"] != want["values"]:
            problems.append(f"{kind} {b}: the remembered state gives the controls {got['values']}, not {want['values']}")
        elif got["html"] != want["html"]:
            warnings.append(f"{kind} {b}: the remembered state draws another box, {first_difference(want['html'], got['html'])}")
        page.evaluate(RESET, b)
        page.wait_for_timeout(500)
        page.close()
        page = open_page(ctx, url, errors)
        if page.evaluate(SNAP, [b, own])["restored"]:
            problems.append(f"{kind} {b}: \"reset everything\" did not forget the state")
        page.close()
    ctx.close()
    return problems + [f"links: {e[:200]}" for e in errors], warnings


def shard(pages: list[str], counts: dict[str, int], spec: str) -> list[str] | None:
    """The pages of part K of N: largest page first, each to the part with the fewest boxes."""
    m = re.fullmatch(r"(\d+)/(\d+)", spec)
    if not m or not 1 <= int(m.group(1)) <= int(m.group(2)):
        return None
    k, n = int(m.group(1)), int(m.group(2))
    parts: list[list[str]] = [[] for _ in range(n)]
    load = [0] * n
    for p in sorted(pages, key=lambda p: (-counts[p], p)):
        i = load.index(min(load))
        parts[i].append(p)
        load[i] += counts[p]
    return sorted(parts[k - 1])


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--browser", help="path to a Chromium executable")
    ap.add_argument("--offline", action="store_true", help="ignore errors of external scripts")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE",
                    help="serve requests matching REGEX from a local file")
    ap.add_argument("--only", help="check only pages whose path matches this regex")
    ap.add_argument("--no-links", action="store_true", help="skip the link and remembered-state checks")
    ap.add_argument("--local-cdn", action="store_true",
                    help="--offline with the CDN copies of .cache/cdn (tools/dev_setup.sh)")
    ap.add_argument("--shard", metavar="K/N", help="check only the K-th of N parts of the pages (1 <= K <= N)")
    args = ap.parse_args(argv)
    if args.local_cdn:
        args.offline = True
        args.route += local_cdn_routes()

    from playwright.sync_api import sync_playwright

    site = Path(args.site).resolve()
    if not site.is_dir():
        print(f"site directory not found: {site}")
        return 1
    counts = {p.relative_to(site).as_posix(): p.read_text(encoding="utf-8").count('class="explorer"')
              for p in site.rglob("index.html")}
    pages = sorted(p for p, n in counts.items() if n)
    if args.only:
        pages = [p for p in pages if re.search(args.only, p)]
    if args.shard:
        pages = shard(pages, counts, args.shard)
        if pages is None:
            print(f"--shard takes K/N with 1 <= K <= N, not {args.shard}")
            return 1
    server, base = serve(site)

    external = re.compile(r"https?://(?!127\.0\.0\.1)")
    # the GitHub API behind the theme's repository widget answers 403 when CI is rate-limited:
    # that is the network, not a box (a CDN script that fails to load still fails the check)
    remote_fetch = re.compile(r"^Failed to load resource: .*\(https://api\.github\.com/")
    failures = boxes_total = clicks_total = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1, service_workers="block")
        routes = []
        for spec in args.route:
            pattern, file = spec.split("=", 1)
            routes.append((re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file)))
        for pattern, handler in routes:
            ctx.route(pattern, handler)
        for rel in pages:
            url = base + rel[: -len("index.html")]
            page = ctx.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda e, errors=errors: errors.append(str(e)))
            page.on("console", lambda m, errors=errors: errors.append(f"{m.text} ({m.location.get('url', '')})")
                    if m.type == "error" else None)
            page.on("dialog", lambda d: d.dismiss())        # the copy fallback opens a prompt
            try:
                page.goto(url, wait_until="networkidle", timeout=60_000)
            except Exception as e:   # a CDN that never answers: check what has loaded
                errors.append(f"load: {e}")
            page.evaluate(OPEN_ALL)
            page.wait_for_timeout(300)
            n_boxes = page.evaluate(BOXES)

            def take() -> list[str]:
                got = [e for e in errors if not (args.offline and external.search(e)) and not remote_fetch.search(e)]
                errors.clear()
                return got

            problems = [f"on load: {e[:200]}" for e in take()]
            clicks = 0
            for b in range(n_boxes):
                kind = page.evaluate("(b) => document.querySelectorAll('.explorer')[b].dataset.kind", b)
                count = page.evaluate(COUNT, [b, BUTTONS])
                for i in range(count):
                    name = page.evaluate(CLICK, [b, i, BUTTONS])
                    if name is None:
                        continue
                    clicks += 1
                    problems += [f"{kind}, button {i} ({name}): {e[:200]}" for e in take()]
                page.wait_for_timeout(400)                  # a play started above runs on
                problems += [f"{kind}, after the clicks: {e[:200]}" for e in take()]
                width = page.evaluate(WIDTH_NOW)
                if width > WIDTH + 1:
                    problems.append(f"{kind}: the page is {width} px wide after the clicks")
                page.evaluate(RESET, b)
                page.wait_for_timeout(100)
                problems += [f"{kind}, reset everything: {e[:200]}" for e in take()]
            page.close()
            warnings: list[str] = []
            if not args.no_links:
                found, warnings = check_links(browser, routes, url)
                if args.offline:
                    found = [p for p in found if not external.search(p)]
                problems += found

            failures += bool(problems)
            boxes_total += n_boxes
            clicks_total += clicks
            print(f"{'FAIL' if problems else 'ok':4}  {rel[: -len('index.html')]}  {n_boxes} boxes, {clicks} clicks")
            for p in problems:
                print(f"        {p}")
            for w in warnings:
                print(f"        warn {w}")
        browser.close()
    server.shutdown()
    print(f"{len(pages)} pages, {boxes_total} boxes, {clicks_total} clicks, {failures} pages with problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
