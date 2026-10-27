"""The home-screen icons of the web app manifest (docs/manifest.webmanifest): the site logo
(docs/assets/logo.svg, the letters DV, the V an amber check) on the navy of the
header. The plain icons fill a navy square with the logo at 70 %; the maskable one keeps
the logo inside the central 60 % that every launcher mask leaves visible.

    python tools/make_icons.py      # rewrites docs/assets/icons/*.png
"""

import re
from pathlib import Path

import cairosvg

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "docs" / "assets" / "logo.svg"
OUT = ROOT / "docs" / "assets" / "icons"
NAVY = "#1b2a4a"

# file name, size in px, share of the side taken by the logo
ICONS = [("icon-180.png", 180, 0.7), ("icon-192.png", 192, 0.7), ("icon-512.png", 512, 0.7),
         ("icon-maskable-512.png", 512, 0.6)]


def icon(size: int, share: float) -> bytes:
    inner = re.search(r"<svg[^>]*>(.*)</svg>", LOGO.read_text(), re.S).group(1)
    inner = re.sub(r"<!--.*?-->", "", inner, flags=re.S)
    side = 64 / share                      # the logo's 64-unit box at that share of the side
    pad = (side - 64) / 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
           f'viewBox="{-pad:.3f} {-pad:.3f} {side:.3f} {side:.3f}">'
           f'<rect x="{-pad:.3f}" y="{-pad:.3f}" width="{side:.3f}" height="{side:.3f}" fill="{NAVY}"/>{inner}</svg>')
    return cairosvg.svg2png(bytestring=svg.encode())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, size, share in ICONS:
        (OUT / name).write_bytes(icon(size, share))
        print(f"wrote {OUT.relative_to(ROOT) / name}")


if __name__ == "__main__":
    main()
