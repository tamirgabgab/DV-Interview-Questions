#!/usr/bin/env python3
"""Step every explorer box through its steps and report figures that jump.

    mkdocs build --strict && python tools/check_jumps.py [site]

The text under the controls of a box changes at every step, and core.js (steady) keeps
each paragraph at the tallest height it has shown, so the figures under it stay put while
the box plays. That reservation only knows the steps already shown: a step whose text is
taller than every earlier one still moves the figures once. This check opens every page
with an explorer box at 390 px and at 1200 px, and in every box with a step counter
("k מתוך T") and a next button it goes back to the first step and presses next until the
end (at most --max-steps steps), measuring after each step the top of every figure
relative to the box. A figure that moves by more than --tol px fails the check, with the
step and the paragraphs that grew at that step.

Needs Playwright, as tools/check_phone.py; --local-cdn, --offline, --route, --only and
--shard work as in tools/check_explorers.py.
"""

from __future__ import annotations

import argparse
import functools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_explorers import BOXES, open_page, shard  # noqa: E402
from check_phone import HEIGHT, local_cdn_routes, serve  # noqa: E402

WIDTHS = (390, 1200)

# Step box b through every transport row (a row of .ex-controls with its own .ex-pos counter
# and next button): first step, then next until the counter stops or maxSteps. After each
# step two animation frames pass, so steady() has measured. Returns the jumps found.
STEP = """async ([b, maxSteps, tol]) => {
  const box = document.querySelectorAll(".explorer")[b];
  const frames = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  const name = (el) => (el.getAttribute("aria-label") || el.getAttribute("class") || el.tagName.toLowerCase()).trim().replace(/\\s+/g, " ").slice(0, 60);
  const figs = () => [...box.querySelectorAll("svg")].filter((s) => !s.parentElement.closest("svg") && s.getClientRects().length
    && !s.closest(".ex-controls, .ex-bar, .ex-transport, .fig-lightbox") && s.getBoundingClientRect().height > 40);
  const paras = () => [...box.querySelectorAll("p, .ex-note, [aria-live]")].filter((e) => !e.closest(".ex-controls, .ex-bar"));
  // every element outside the figures, for naming what grew: the deepest element whose height
  // changed by the figure's move is the cause (a paragraph, a table, a figure above)
  const blocks = () => [...box.querySelectorAll("*")].filter((e) => !e.closest("svg") || e.tagName === "svg");
  const snap = () => {
    const top = box.getBoundingClientRect().top;
    return { figs: figs().map((s) => [name(s), s.getBoundingClientRect().top - top]),
             paras: paras().map((e) => [name(e), e.getBoundingClientRect().height]),
             blocks: new Map(blocks().map((e) => [e, e.getBoundingClientRect().height])) };
  };
  const depth = (e) => { let d = 0; for (; e && e !== box; e = e.parentElement) d++; return d; };
  const cause = (prev, now, by) => {
    let best = null;
    for (const [e, h] of now.blocks) {
      const was = prev.blocks.get(e);
      if (was === undefined || Math.abs(h - was - by) > 1.5 || !e.getClientRects().length) continue;
      if (!best || depth(e) > depth(best)) best = e;
    }
    return best ? `${best.tagName.toLowerCase()}.${(best.getAttribute("class") || "").trim().split(/\s+/).join(".")}` : "";
  };
  const jumps = [];
  for (const row of box.querySelectorAll(".ex-controls")) {
    const own = (el) => el && el.closest(".ex-controls") === row;
    const find = (sel) => [...row.querySelectorAll(sel)].find(own);
    const pos = () => [...box.querySelectorAll(".ex-pos")].find(own);
    if (!find("button.ex-next") || !pos()) continue;
    const first = find("button.ex-start, button.ex-first");
    if (first && !first.disabled) first.click();
    await frames();
    let prev = snap();
    for (let i = 0; i < maxSteps; i++) {
      const next = find("button.ex-next");
      if (!next || next.disabled) break;
      const was = pos() ? pos().textContent.trim() : "";
      next.click();
      await frames();
      const now = snap(), at = pos() ? pos().textContent.trim() : "";
      if (now.figs.length === prev.figs.length) {
        const moved = now.figs.map(([n, t], j) => [n, t - prev.figs[j][1]]).filter(([, d]) => Math.abs(d) > tol);
        if (moved.length) {
          const grew = now.paras.length === prev.paras.length
            ? now.paras.map(([n, h], j) => [n, h - prev.paras[j][1]]).filter(([, d]) => Math.abs(d) > 0.5) : [];
          jumps.push({ step: at, figure: moved[0][0], by: moved[0][1], grew, cause: cause(prev, now, moved[0][1]) });
        }
      }
      if (at === was) break;                         // the box stopped advancing
      prev = now;
    }
  }
  return { kind: box.dataset.kind, jumps };
}"""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--browser", help="path to a Chromium executable")
    ap.add_argument("--offline", action="store_true", help="ignore errors of external scripts")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE",
                    help="serve requests matching REGEX from a local file")
    ap.add_argument("--local-cdn", action="store_true",
                    help="--offline with the CDN copies of .cache/cdn (tools/dev_setup.sh)")
    ap.add_argument("--only", help="check only pages whose path matches this regex")
    ap.add_argument("--shard", metavar="K/N", help="check only the K-th of N parts of the pages (1 <= K <= N)")
    ap.add_argument("--max-steps", type=int, default=80, help="steps per box at most (80)")
    ap.add_argument("--tol", type=float, default=2.0, help="a move larger than this many px is a jump (2)")
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

    failures = boxes_total = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        for width in WIDTHS:
            ctx = browser.new_context(viewport={"width": width, "height": HEIGHT}, device_scale_factor=1)
            for spec in args.route:
                pattern, file = spec.split("=", 1)
                ctx.route(re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file))
            for rel in pages:
                errors: list[str] = []
                page = open_page(ctx, base + rel[: -len("index.html")], errors)
                found = []
                for b in range(page.evaluate(BOXES)):
                    r = page.evaluate(STEP, [b, args.max_steps, args.tol])
                    boxes_total += 1
                    for j in r["jumps"]:
                        grew = ", ".join(f"{n} {d:+.0f}px" for n, d in j["grew"]) or "no paragraph grew"
                        found.append(f"{r['kind']} {b}, step {j['step']}: {j['figure'][:50]} moved {j['by']:+.0f}px "
                                     f"({grew}; grew: {j['cause'] or '?'})")
                page.close()
                failures += bool(found)
                print(f"{'FAIL' if found else 'ok':4}  {rel[: -len('index.html')]}  {width} px")
                for f in found:
                    print(f"        jump: {f}")
            ctx.close()
        browser.close()
    server.shutdown()
    print(f"{len(pages)} pages at {', '.join(map(str, WIDTHS))} px, {boxes_total} boxes stepped, "
          f"{failures} page runs with jumps")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
