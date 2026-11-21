#!/usr/bin/env python3
"""Fail on figure text that a line of the figure crosses (round 21.5).

    mkdocs build --strict && python tools/checks/check_collisions.py [site]

Serves the built site and opens every question page in Chromium at 1200 x 900 px, with every
collapsible block open and every frame of every stepper shown (the later frames are
<template>s until a step, so they are put in the page). In each inline SVG figure of
the page (math, the explorer boxes and the diagrams of the libraries aside) it walks every
stroked line, polyline and unfilled path in steps of about 2 px and fails when a point falls
inside the box of a text element, shrunk by 1.5 px on each side. Not counted: a line and a
text inside the same <g> (a node and its name, a bar and its value), a text drawn with a
halo (`halo`: it is meant to sit on its line, and paints a background under itself), a
line inside a marker, and a line whose class says it is a grid or a strike-through (`grid`, `tick`, `*-grid`, `*-tick`,
`*-strike`: a line drawn over a number on purpose).

The geometry of a figure is in its own units, so one width is enough: a figure's text and
lines scale together. The collisions found when the check was written are listed in
collisions_known.txt and only warn; a new one fails. --only REGEX checks only the matching pages; --local-cdn and --browser
as in check_phone.py.
"""

from __future__ import annotations

import argparse
import functools
import re
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from check_phone import OPEN_ALL, local_cdn_routes, serve  # noqa: E402

WIDTH, HEIGHT = 1200, 900
KNOWN = Path(__file__).resolve().parent / "collisions_known.txt"
KNOWN_HEAD = ("# Figure text crossed by a line, found when check_collisions.py was written (round 21.5).\n"
              "# A collision listed here is a warning; a new one fails. Fix a figure, then delete its lines\n"
              "# (the check names the fixed ones). Written by check_collisions.py --write-known.\n")

# Every frame of a stepper shown, so each one is measured (the stepper shows one at a time).
SHOW_FRAMES = """() => {
  document.querySelectorAll(".stepper template.stepper-later").forEach((t) => t.replaceWith(t.content.cloneNode(true)));
  document.querySelectorAll(".stepper [hidden]").forEach((f) => { f.hidden = false; });
  document.querySelectorAll(".stepper .stepper-frame").forEach((f) => { f.style.display = "block"; });
}"""

FIND = r"""() => {
  const out = [];
  const grid = /(^|\s)(grid|tick|[\w-]+-(grid|tick|strike))(\s|$)/;
  const figures = [...document.querySelectorAll(".md-content svg")].filter((s) =>
    !s.closest("mjx-container, .explorer, .mermaid, [id^='svgcontent_'], .wavedrom") && !s.parentElement.closest(".md-content svg"));
  for (const svg of figures) {
    const texts = [...svg.querySelectorAll("text")].filter((t) => {
      if (!t.textContent.trim() || t.closest("defs, marker") || t.matches(".halo, .halo *")) return false;
      const r = t.getBoundingClientRect();
      return r.width > 0 && r.height > 0 && getComputedStyle(t).visibility !== "hidden" && +getComputedStyle(t).opacity !== 0;
    }).map((t) => ({ t, r: t.getBoundingClientRect() }));
    if (!texts.length) continue;
    const lines = [...svg.querySelectorAll("line, polyline, path")].filter((l) => {
      if (l.closest("defs, marker, clipPath, mask, pattern")) return false;
      const cs = getComputedStyle(l);
      if (cs.stroke === "none" || parseFloat(cs.strokeWidth) === 0 || +cs.opacity === 0 || +cs.strokeOpacity === 0 || cs.visibility === "hidden") return false;
      if (l.tagName !== "line" && cs.fill !== "none" && +cs.fillOpacity !== 0) return false;
      if (grid.test(l.getAttribute("class") || "")) return false;
      const r = l.getBoundingClientRect();
      return r.width > 0 || r.height > 0;
    });
    const name = (svg.getAttribute("aria-label") || "").replace(/\s+/g, " ").slice(0, 50);
    const group = (el) => (el.parentElement && el.parentElement.tagName === "g" ? el.parentElement : null);
    for (const l of lines) {
      const m = l.getScreenCTM();
      if (!m) continue;
      let pts = [];
      if (l.tagName === "line") {
        const a = l.x1.baseVal.value, b = l.y1.baseVal.value, c = l.x2.baseVal.value, d = l.y2.baseVal.value;
        const n = Math.max(1, Math.ceil(Math.hypot(c - a, d - b) / 2));
        for (let i = 0; i <= n; i++) pts.push(new DOMPoint(a + (c - a) * i / n, b + (d - b) * i / n));
      } else {
        let len = 0;
        try { len = l.getTotalLength(); } catch (e) { continue; }
        const n = Math.max(1, Math.ceil(len / 2));
        for (let i = 0; i <= n; i++) { const p = l.getPointAtLength(len * i / n); pts.push(new DOMPoint(p.x, p.y)); }
      }
      pts = pts.map((p) => p.matrixTransform(m));
      const lg = group(l);
      for (const { t, r } of texts) {
        if (lg && group(t) === lg) continue;
        const x0 = r.left + 1.5, x1 = r.right - 1.5, y0 = r.top + 1.5, y1 = r.bottom - 1.5;
        if (pts.some((p) => p.x > x0 && p.x < x1 && p.y > y0 && p.y < y1)) {
          out.push(`"${t.textContent.trim().slice(0, 24)}" crossed by <${l.tagName} class="${l.getAttribute("class") || ""}"> in ${name}`);
        }
      }
    }
  }
  return [...new Set(out)];
}"""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--browser", help="path to a Chromium executable")
    ap.add_argument("--only", help="check only pages whose path matches this regex")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE", help="serve a URL from a local file")
    ap.add_argument("--local-cdn", action="store_true", help="serve the CDN scripts from .cache/cdn")
    ap.add_argument("--known", default=str(KNOWN), help="the list of collisions known before the check (a warning)")
    ap.add_argument("--write-known", action="store_true", help="write every collision found to the --known list")
    args = ap.parse_args(argv)
    known_file = Path(args.known)
    known = {ln for ln in known_file.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")} \
        if known_file.is_file() and not args.write_known else set()
    found: list[str] = []
    if args.local_cdn:
        args.route += local_cdn_routes()

    from playwright.sync_api import sync_playwright

    site = Path(args.site).resolve()
    pages = sorted(p.relative_to(site).as_posix() for p in (site / "questions").rglob("index.html"))
    if args.only:
        pages = [p for p in pages if re.search(args.only, p)]
    server, base = serve(site)
    failures = old = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1, service_workers="block")
        for spec in args.route:
            pattern, file = spec.split("=", 1)
            ctx.route(re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file))
        for rel in pages:
            page = ctx.new_page()
            try:
                page.goto(base + rel[: -len("index.html")], wait_until="load", timeout=60_000)
            except Exception as e:
                print(f"FAIL  {rel}: load: {e}")
                failures += 1
                page.close()
                continue
            page.evaluate(OPEN_ALL)
            page.evaluate(SHOW_FRAMES)
            page.wait_for_timeout(300)
            path = rel[: -len("index.html")]
            hits = [f"{path} | {h}" for h in page.evaluate(FIND)]
            found += hits
            new = [h for h in hits if h not in known]
            old += len(hits) - len(new)
            if new:
                failures += 1
                print(f"FAIL  {path}")
                for h in new:
                    print(f"        {h.split(' | ', 1)[1]}")
            page.close()
        browser.close()
    server.shutdown()
    if args.write_known:
        known_file.write_text(KNOWN_HEAD + "".join(h + "\n" for h in sorted(found)), encoding="utf-8")
        print(f"wrote {len(found)} collisions to {known_file}")
        return 0
    gone = sorted(h for h in known if h not in found and (not args.only or re.search(args.only, h.split(" | ")[0])))
    for h in gone:
        print(f"fixed (remove it from {known_file.name}): {h}")
    print(f"{len(pages)} pages checked, {failures} with figure text crossed by a new line collision; "
          f"{old} known collisions left ({known_file.name}), {len(gone)} of them fixed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
