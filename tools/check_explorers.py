#!/usr/bin/env python3
"""Click every button of every explorer box on the built site.

    mkdocs build --strict && python tools/check_explorers.py [site]

Serves the site locally and opens every page that has an explorer box (`div.explorer`) in
Chromium at 390 x 844 px, with every collapsible block open. In each box it clicks every
visible, enabled button once, in document order (the box is queried again before each
click, since the views redraw their controls), lets a running play go on for a moment,
then presses "reset everything". It fails when a script throws or logs a console error,
and when the page scrolls sideways after a box was clicked through. The failing button is
named in the report (its aria-label, text or title).

Needs Playwright, as tools/check_phone.py. In a sandbox without access to the CDNs,
--offline ignores errors of external scripts and --route REGEX=FILE serves a CDN script
from a local copy; --only REGEX checks only the matching pages.
"""

from __future__ import annotations

import argparse
import functools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_phone import HEIGHT, OPEN_ALL, WIDTH, serve  # noqa: E402

BUTTONS = "button, [role=button]"

# The number of boxes on the page, after the lazy ones were built.
BOXES = """async () => {
  if (window.dvqExplorers) await window.dvqExplorers.ready();
  return document.querySelectorAll(".explorer").length;
}"""

COUNT = """([b, sel]) => document.querySelectorAll(".explorer")[b].querySelectorAll(sel).length"""

# Click the i-th button of box b if it is shown and enabled; close a lightbox it opened.
# Returns the button's name, or null when it was skipped.
CLICK = """([b, i, sel]) => {
  const box = document.querySelectorAll(".explorer")[b];
  const el = box && box.querySelectorAll(sel)[i];
  if (!el || el.disabled || el.getAttribute("aria-disabled") === "true" || !el.getClientRects().length) return null;
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


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="?", default="site")
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
    pages = sorted(p.relative_to(site).as_posix() for p in site.rglob("index.html")
                   if 'class="explorer"' in p.read_text(encoding="utf-8"))
    if args.only:
        pages = [p for p in pages if re.search(args.only, p)]
    server, base = serve(site)

    external = re.compile(r"https?://(?!127\.0\.0\.1)")
    failures = boxes_total = clicks_total = 0
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
                got = [e for e in errors if not (args.offline and external.search(e))]
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

            failures += bool(problems)
            boxes_total += n_boxes
            clicks_total += clicks
            print(f"{'FAIL' if problems else 'ok':4}  {rel[: -len('index.html')]}  {n_boxes} boxes, {clicks} clicks")
            for p in problems:
                print(f"        {p}")
        browser.close()
    server.shutdown()
    print(f"{len(pages)} pages, {boxes_total} boxes, {clicks_total} clicks, {failures} pages with problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
