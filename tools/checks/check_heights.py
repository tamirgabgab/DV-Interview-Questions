#!/usr/bin/env python3
"""Does every explorer box fit one computer screen? A warning, never a failure.

    mkdocs build --strict && python tools/checks/check_heights.py [site]

Serves the site locally and opens every page that has an explorer box (`div.explorer`) in
Chromium at 1920 x 1080 px (the owner's computer screen, session 34), with every
collapsible block open. Every box is built, stepped to its end (its "end" button, when it
has one, where a box is usually at its tallest), and measured. A box taller than the
screen's room under the sticky header and the part bar (BUDGET px) is listed with its
height, tallest first; the box should then lay its blocks out in two columns (a kind's
`cols` in its register call, core.js columns(), stylesheets/27-box-columns.css).

The check only reports (the owner's choice): it exits 0 whatever it finds, unless the site
is missing. --only REGEX checks only the matching pages; --budget PX changes the room;
--local-cdn, --route and --browser as in tools/checks/check_phone.py.
"""

from __future__ import annotations

import argparse
import functools
import re
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from check_phone import OPEN_ALL, local_cdn_routes, serve  # noqa: E402

SCREEN_W, SCREEN_H = 1920, 1080
# the sticky header and the part bar take about 112 px of the 1080; 0099's hardware box,
# the first laid out for one screen, is about 990 px tall at its end
BUDGET = 1000

# Build every box, press its end button, and measure it.
MEASURE = """async () => {
  if (window.dvqExplorers) await window.dvqExplorers.ready();
  const boxes = [...document.querySelectorAll(".explorer")];
  boxes.forEach((b) => { const e = b.querySelector("button.ex-end, button.ex-last"); if (e && !e.disabled) e.click(); });
  await new Promise((r) => setTimeout(r, 300));
  return boxes.map((b) => ({ kind: b.dataset.kind, h: Math.round(b.getBoundingClientRect().height),
    w: Math.round(b.getBoundingClientRect().width), cols: Boolean(b.querySelector(":scope > .ex-cols")) }));
}"""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--browser", help="path to a Chromium executable")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE",
                    help="serve URLs matching REGEX from a local FILE (a CDN copy)")
    ap.add_argument("--only", help="check only pages whose path matches this regex")
    ap.add_argument("--budget", type=int, default=BUDGET, help=f"the room in px (default {BUDGET})")
    ap.add_argument("--local-cdn", action="store_true", help="serve the CDN scripts from .cache/cdn")
    args = ap.parse_args(argv)
    if args.local_cdn:
        args.route += local_cdn_routes()

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
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": SCREEN_W, "height": SCREEN_H}, device_scale_factor=1,
                                  service_workers="block")
        for spec in args.route:
            pattern, file = spec.split("=", 1)
            ctx.route(re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file))
        # other hosts are not needed to lay a box out
        ctx.route(re.compile(r"^https?://(?!127\.0\.0\.1)"), lambda route: route.abort())
        page = ctx.new_page()
        for rel in pages:
            try:
                page.goto(base + rel[: -len("index.html")], wait_until="load", timeout=60_000)
            except Exception as e:  # noqa: BLE001 — a slow page: measure what has loaded
                print(f"warn  {rel}: load: {str(e)[:120]}")
            page.evaluate(OPEN_ALL)
            page.wait_for_timeout(200)
            for i, box in enumerate(page.evaluate(MEASURE)):
                rows.append((box["h"], rel.split("/")[-2], i + 1, box["kind"], box["cols"]))
        browser.close()
    server.shutdown()

    over = sorted((r for r in rows if r[0] > args.budget), reverse=True)
    for h, page_name, n, kind, cols in over:
        print(f"warn  {h:5d} px  {kind:12s} box {n} of {page_name[:48]}{'  (two columns)' if cols else ''}")
    kinds = {r[3] for r in rows}
    print(f"{len(rows)} boxes of {len(kinds)} kinds on {len(pages)} pages at {SCREEN_W} x {SCREEN_H}: "
          f"{len(over)} taller than {args.budget} px ({len({r[3] for r in over})} kinds); "
          f"{sum(r[4] for r in rows)} boxes in two columns")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
