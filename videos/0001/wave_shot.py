"""The page's WaveDrom diagram of 0001 as a picture, for the end of the video's timing beat.

The diagram is not an explorer box, so box_shots.py does not take it; this takes it the same
way (the built site in videos/.cache/site, the dark scheme, the CDN scripts from the local
copies, the sticky bars hidden) and saves out/wavedrom.png. scene.py runs it, with the
Python that has Playwright (dvq.LABEL_PYTHON), when the picture is missing:

    python3 videos/0001/wave_shot.py
"""

from __future__ import annotations

import functools
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "videos" / "lib"))
sys.path.insert(0, str(ROOT / "tools"))

import box_shots as bs  # noqa: E402
from check_phone import local_cdn_routes  # noqa: E402

OUT = HERE / "out" / "wavedrom.png"
SCALE = 4          # the diagram is 480 CSS px wide: four device pixels per CSS pixel
BORDER = 4         # a CSS pixel of the page's background on the top and left edges


def main() -> int:
    from playwright.sync_api import sync_playwright

    site = ROOT / "videos" / ".cache" / "site"
    if not site.is_dir():
        sys.exit(f"{site} is missing: render.py builds it when it captures the boxes")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    server, base = bs._serve(site.resolve())
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=bs.CHROMIUM)
            ctx = browser.new_context(viewport={"width": bs.WIDTH, "height": 1400},
                                      device_scale_factor=SCALE, color_scheme="dark",
                                      service_workers="block", reduced_motion="reduce")
            for spec in local_cdn_routes():
                pattern, file = spec.split("=", 1)
                ctx.route(re.compile(pattern), functools.partial(lambda f, route: route.fulfill(path=f), file))
            page = ctx.new_page()
            page.goto(base + bs.page_url("0001"), wait_until="networkidle", timeout=60_000)
            page.evaluate("() => document.querySelectorAll('details').forEach((d) => (d.open = true))")
            page.wait_for_selector("#WaveDrom_Display_0 svg", timeout=30_000)
            page.evaluate(bs.HIDE)
            el = page.locator("#WaveDrom_Display_0 svg").first
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(600)
            el.screenshot(path=str(OUT))
            browser.close()
        from PIL import Image
        img = Image.open(OUT)
        w, h = img.size
        img.crop((BORDER, BORDER, w, h)).save(OUT)     # the page's background on two sides
    finally:
        server.shutdown()
    print(f"wavedrom: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
