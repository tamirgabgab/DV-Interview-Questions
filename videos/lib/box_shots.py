"""Capture a question's interactive box, step by step, from the built site.

The videos show the page's own box (the owner, 2026-10-31): not a copy drawn in Manim, but
the box as a reader sees it, driven by the same clicks. A scene names its boxes in the
module literal `BOXES` of `videos/<id>/scene.py`:

    BOXES = {
        "long": {                      # the name the scene loads with dvq.BoxView(QID, "long")
            "box": 0,                  # the page's n-th explorer box (div.explorer)
            "region": [".ex-play-row", ".st-chart", ".wv-step"],   # the part of the box shown
            "steps": [                 # one picture after each step
                [],                                        # the box as the page opens it
                [["click", ".ex-start"]],
                {"do": [["click", ".ex-next"]], "repeat": 5},   # five pictures, a click each
            ],
        },
    }

- **region**: the selectors (inside the box) whose union, over every step, is cropped, so
  the picture keeps one size and nothing in it moves but what the box changes. A box is
  about 600 px wide and up to 850 high, too tall for half the frame at a readable size, so
  a video shows the part that carries the example (the figure, the player, the line that
  explains the step); the controls it clicks are best inside it.
- **hide** (optional): selectors inside the box hidden while it is captured (a hint line
  between the player and the figure), so the region is only what the video needs.
- **width** (optional): the box's width in CSS px while it is captured (the page's is
  about 600), for a box that shares the frame with wide code: its text wraps into more
  lines, and the picture is narrower and taller.
- **steps**: a list of actions, or {"do": [...], "repeat": n}. An action is
  ["click", sel] (a button, a cell of a figure; several clicks may make one step),
  ["fill", sel, value] (typed, then Enter, as a reader applies a field), ["check", sel,
  true|false], or ["wait", ms]. A selector is a Playwright selector inside the box,
  `button:has-text("דוגמת העמוד")` included.

The page is the built site (`mkdocs build`, served locally) in Chromium at 1280 px, the
dark scheme (the video is navy), twice the pixels, with the site's sticky bars hidden so
none covers the box. Each picture is the box's screenshot cropped to the region. The record
`out/boxes/<name>/shots.json` has, per picture, its file and the rectangles of the controls
the step clicked, in the picture's pixels, so the scene can mark the click.

Run by render.py before the Manim pass, with the Python that has Playwright:

    python3 videos/lib/box_shots.py 0006 --spec specs.json --site videos/.cache/site
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import http.server
import json
import re
import sys
import threading
from pathlib import Path

VIDEOS = Path(__file__).resolve().parent.parent
ROOT = VIDEOS.parent
CHROMIUM = "/opt/pw-browsers/chromium"
SCALE = 2           # device pixels per CSS pixel
WIDTH = 1280        # the viewport: the desktop page, its box about 600 px wide
PAD = 10            # CSS px around the region
VERSION = "1"       # bump to capture every box again

# Every bar of the site that stays on screen (the header, the part navigation) hidden, so a
# screenshot of a box never has one over it; the enlarge buttons of the figures too.
HIDE = """() => {
  for (const el of document.querySelectorAll("body *")) {
    if (el.closest(".explorer")) continue;
    const pos = getComputedStyle(el).position;
    if (pos === "fixed" || pos === "sticky") el.style.visibility = "hidden";
  }
  const st = document.createElement("style");
  st.textContent = ".explorer .fig-enlarge { visibility: hidden !important; } *:focus { outline: none !important; }";
  document.head.append(st);
}"""

# The union of the region's selectors inside box b, in CSS px relative to the box.
REGION = """([b, sels]) => {
  const box = document.querySelectorAll(".explorer")[b];
  const o = box.getBoundingClientRect();
  let r = null;
  for (const sel of sels) for (const el of box.querySelectorAll(sel)) {
    const e = el.getBoundingClientRect();
    if (!e.width || !e.height) continue;
    r = r ? { l: Math.min(r.l, e.left), t: Math.min(r.t, e.top), r: Math.max(r.r, e.right), b: Math.max(r.b, e.bottom) }
          : { l: e.left, t: e.top, r: e.right, b: e.bottom };
  }
  return r && { l: r.l - o.left, t: r.t - o.top, r: r.r - o.left, b: r.b - o.top, w: o.width, h: o.height };
}"""

RECT = """([b, el]) => {
  const o = document.querySelectorAll(".explorer")[b].getBoundingClientRect();
  const e = el.getBoundingClientRect();
  return { l: e.left - o.left, t: e.top - o.top, r: e.right - o.left, b: e.bottom - o.top };
}"""


def steps_of(spec: dict) -> list[list]:
    """The spec's steps as a flat list of action lists, one per picture."""
    out = []
    for step in spec["steps"]:
        if isinstance(step, dict):
            out += [list(step["do"])] * int(step.get("repeat", 1))
        else:
            out.append(list(step))
    return out


def spec_hash(qid: str, name: str, spec: dict) -> str:
    """What a capture depends on: the spec, the page and the site's scripts and styles."""
    h = hashlib.sha256(json.dumps([VERSION, qid, name, spec], sort_keys=True,
                                  ensure_ascii=False).encode())
    page = next((ROOT / "docs" / "questions").glob(f"*/{qid}-*.md"))
    for p in [page, *sorted((ROOT / "docs" / "javascripts").rglob("*.js")),
              *sorted((ROOT / "docs" / "stylesheets").glob("*.css"))]:
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def page_url(qid: str) -> str:
    page = next((ROOT / "docs" / "questions").glob(f"*/{qid}-*.md"))
    return page.relative_to(ROOT / "docs").with_suffix("").as_posix() + "/"


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def _serve(site: Path):
    handler = functools.partial(_Quiet, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/"


def _act(page, b: int, action: list) -> list[dict]:
    """Do one action in box b; returns the rectangles (CSS px, box-relative) it clicked."""
    kind = action[0]
    box = page.locator(".explorer").nth(b)
    if kind == "wait":
        page.wait_for_timeout(int(action[1]))
        return []
    el = box.locator(action[1]).first
    handle = el.element_handle()
    rect = page.evaluate(RECT, [b, handle])
    if kind == "click":
        # a JS click, as a tap: no focus ring, and an SVG cell is clicked through its group
        page.evaluate("(el) => el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}))",
                      handle)
        return [rect]
    if kind == "fill":
        el.fill(str(action[2]))
        el.press("Enter")
        page.evaluate("(el) => el.blur()", handle)
        return [rect]
    if kind == "check":
        el.set_checked(bool(action[2]))
        return [rect]
    raise ValueError(f"unknown action {action!r}")


def capture(qid: str, name: str, spec: dict, site: Path, routes: list[str]) -> Path:
    """Capture the box `name` of question `qid` into out/boxes/<name>/; returns shots.json."""
    from PIL import Image
    from playwright.sync_api import sync_playwright

    out = VIDEOS / qid / "out" / "boxes" / name
    record = out / "shots.json"
    digest = spec_hash(qid, name, spec)
    if record.exists() and json.loads(record.read_text(encoding="utf-8")).get("hash") == digest:
        return record
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.png"):
        old.unlink()
    b = int(spec.get("box", 0))
    server, base = _serve(site)
    raw, rects, regions = [], [], []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=CHROMIUM)
            ctx = browser.new_context(viewport={"width": WIDTH, "height": 1400},
                                      device_scale_factor=SCALE, color_scheme="dark",
                                      service_workers="block", reduced_motion="reduce")
            for spec_route in routes:
                pattern, file = spec_route.split("=", 1)
                ctx.route(re.compile(pattern),
                          functools.partial(lambda f, route: route.fulfill(path=f), file))
            page = ctx.new_page()
            page.goto(base + page_url(qid), wait_until="networkidle", timeout=60_000)
            page.evaluate("""async () => {
              document.querySelectorAll("details").forEach((d) => (d.open = true));
              if (window.dvqExplorers) await window.dvqExplorers.ready();
            }""")
            page.evaluate(HIDE)
            if spec.get("hide"):
                page.evaluate("""([b, sels]) => { const box = document.querySelectorAll(".explorer")[b];
                  for (const sel of sels) box.querySelectorAll(sel).forEach((e) => (e.style.display = "none")); }""",
                              [b, spec["hide"]])
            if spec.get("width"):     # a narrower box: its text wraps, the picture is taller
                page.evaluate("""([b, w]) => { const box = document.querySelectorAll(".explorer")[b];
                  box.style.width = w + "px"; box.style.maxWidth = w + "px"; }""", [b, int(spec["width"])])
            box = page.locator(".explorer").nth(b)
            box.scroll_into_view_if_needed()
            page.wait_for_timeout(600)
            for k, actions in enumerate(steps_of(spec)):
                clicked = []
                for action in actions:
                    clicked += _act(page, b, action)
                    page.wait_for_timeout(120)
                page.wait_for_timeout(450)          # the box redraws
                png = out / f"raw-{k:02d}.png"
                box.screenshot(path=str(png))
                raw.append(png)
                rects.append(clicked)
                region = page.evaluate(REGION, [b, spec["region"]])
                if region is None:
                    raise RuntimeError(f"{qid} {name}: no element of {spec['region']} is shown")
                regions.append(region)
            browser.close()
    finally:
        server.shutdown()
    left = max(0, min(r["l"] for r in regions) - PAD)
    top = max(0, min(r["t"] for r in regions) - PAD)
    right = min(regions[0]["w"], max(r["r"] for r in regions) + PAD)
    bottom = min(max(r["h"] for r in regions), max(r["b"] for r in regions) + PAD)
    crop = [round(v * SCALE) for v in (left, top, right, bottom)]
    shots = []
    for k, (png, clicked) in enumerate(zip(raw, rects)):
        img = Image.open(png)
        w, h = img.size
        box_crop = (crop[0], crop[1], min(crop[2], w), min(crop[3], h))
        canvas = Image.new("RGBA", (crop[2] - crop[0], crop[3] - crop[1]), img.getpixel((4, h - 4)))
        canvas.paste(img.crop(box_crop), (0, 0))
        name_k = f"{k:02d}.png"
        canvas.save(out / name_k)
        png.unlink()
        marks = []
        for r in clicked:
            x0, y0 = r["l"] * SCALE - crop[0], r["t"] * SCALE - crop[1]
            x1, y1 = r["r"] * SCALE - crop[0], r["b"] * SCALE - crop[1]
            if x1 > 0 and y1 > 0 and x0 < canvas.width and y0 < canvas.height:
                marks.append([round(x0), round(y0), round(x1), round(y1)])
        shots.append({"file": name_k, "clicks": marks})
    record.write_text(json.dumps({"hash": digest, "qid": qid, "name": name, "scale": SCALE,
                                  "size": [crop[2] - crop[0], crop[3] - crop[1]],
                                  "shots": shots}, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("qid")
    ap.add_argument("--spec", type=Path, required=True, help="a JSON file: scene.py's BOXES")
    ap.add_argument("--site", type=Path, required=True, help="the built site")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE",
                    help="serve a CDN script from a local copy (as tools/check_phone.py)")
    args = ap.parse_args()
    qid = f"{int(args.qid):04d}"
    boxes = json.loads(args.spec.read_text(encoding="utf-8"))
    for name, spec in boxes.items():
        record = capture(qid, name, spec, args.site.resolve(), args.route)
        n = len(json.loads(record.read_text(encoding="utf-8"))["shots"])
        print(f"box {name}: {n} picture(s) in {record.parent.relative_to(VIDEOS.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
