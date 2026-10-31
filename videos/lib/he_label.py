"""Render a Hebrew label to a transparent PNG with the browser.

Manim draws text through Pango glyph by glyph, and right-to-left lines can come out with
their words or punctuation flipped. A Hebrew label is therefore drawn once by Chromium
(Playwright), the same engine that shapes the site's own figures, and the scene loads the
PNG as an ImageMobject.

Two sides use this module:

- `render.py` (or the scene, when a PNG is missing) runs it as a script with a Python that
  has Playwright: ``python3 videos/lib/he_label.py --json specs.json``. The script renders
  every spec whose PNG is not cached yet.
- The scene imports it only for `label_path()`, which needs no Playwright.

A label is cached under ``videos/.cache/labels/<hash>.png``; the hash covers the text, the
size, the colour, the weight and the renderer version, so a changed label renders again.
Sizes are in pixels of the 720p frame; the PNG is drawn at twice that (`SCALE`), so it stays
sharp when the scene scales it.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

VIDEOS = Path(__file__).resolve().parent.parent
CACHE = VIDEOS / ".cache"
LABELS = CACHE / "labels"
FONTS = CACHE / "fonts"
SCALE = 2                 # device pixels per frame pixel
VERSION = "1"             # bump to re-render every cached label
FONT_FAMILY = "Rubik"     # the site's text font (mkdocs.yml), downloaded once
FALLBACK = "'Heebo', 'DejaVu Sans', 'Liberation Sans', sans-serif"
CHROMIUM = "/opt/pw-browsers/chromium"
GOOGLE_CSS = "https://fonts.googleapis.com/css2?family=Rubik:wght@{w}"


def label_key(text: str, size: int = 36, color: str = "#ffffff", weight: int = 500) -> str:
    raw = json.dumps([VERSION, FONT_FAMILY, text, size, color.lower(), weight], ensure_ascii=False)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def label_path(text: str, size: int = 36, color: str = "#ffffff", weight: int = 500) -> Path:
    return LABELS / f"{label_key(text, size, color, weight)}.png"


def _font_file(weight: int) -> Path | None:
    """The cached Rubik TTF of `weight`, downloaded from Google Fonts on first use.
    None when it cannot be fetched: the label then falls back to a system font."""
    path = FONTS / f"rubik-{weight}.ttf"
    if path.exists():
        return path
    try:
        css = urllib.request.urlopen(GOOGLE_CSS.format(w=weight), timeout=20).read().decode()
        url = css.split("url(", 1)[1].split(")", 1)[0]
        data = urllib.request.urlopen(url, timeout=30).read()
    except Exception as exc:  # offline: fall back
        print(f"he_label: Rubik {weight} not available ({exc}); using {FALLBACK}", file=sys.stderr)
        return None
    FONTS.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _html(spec: dict) -> str:
    weight = int(spec.get("weight", 500))
    font = _font_file(weight)
    face = ""
    if font is not None:
        b64 = base64.b64encode(font.read_bytes()).decode()
        face = (f"@font-face {{ font-family: '{FONT_FAMILY}'; font-weight: {weight}; "
                f"src: url(data:font/ttf;base64,{b64}) format('truetype'); }}")
    text = (spec["text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>
{face}
html, body {{ margin: 0; background: transparent; }}
#l {{ display: inline-block; padding: 0.12em 0.08em; white-space: nowrap; direction: rtl;
      font-family: '{FONT_FAMILY}', {FALLBACK}; font-size: {int(spec.get('size', 36))}px;
      font-weight: {weight}; color: {spec.get('color', '#ffffff')}; line-height: 1.15; }}
</style></head><body><span id="l">{text}</span></body></html>"""


def render(specs: list[dict], force: bool = False) -> list[Path]:
    """Render every spec ({text, size, color, weight}) that is not cached yet."""
    todo = []
    for spec in specs:
        out = label_path(spec["text"], int(spec.get("size", 36)), spec.get("color", "#ffffff"),
                         int(spec.get("weight", 500)))
        if force or not out.exists():
            todo.append((spec, out))
    if not todo:
        return []
    from playwright.sync_api import sync_playwright   # only the rendering side needs it

    LABELS.mkdir(parents=True, exist_ok=True)
    done = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROMIUM)
        page = browser.new_page(device_scale_factor=SCALE, viewport={"width": 1600, "height": 400})
        for spec, out in todo:
            page.set_content(_html(spec))
            page.evaluate("document.fonts.ready")
            page.locator("#l").screenshot(path=str(out), omit_background=True)
            done.append(out)
        browser.close()
    return done


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("text", nargs="?", help="one label to render")
    ap.add_argument("--size", type=int, default=36)
    ap.add_argument("--color", default="#ffffff")
    ap.add_argument("--weight", type=int, default=500)
    ap.add_argument("--json", type=Path, help="a JSON list of specs {text, size, color, weight}")
    ap.add_argument("--force", action="store_true", help="render again even when cached")
    args = ap.parse_args()
    specs = json.loads(args.json.read_text(encoding="utf-8")) if args.json else []
    if args.text:
        specs.append({"text": args.text, "size": args.size, "color": args.color,
                      "weight": args.weight})
    done = render(specs, force=args.force)
    for path in done:
        print(path)
    print(f"he_label: {len(done)} rendered, {len(specs) - len(done)} cached", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
