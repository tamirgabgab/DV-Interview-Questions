"""Contrast of the site's colour pairs in the light and the dark scheme (WCAG 2).

The colours are the CSS custom properties: Material's own (read from the installed theme's
stylesheets) overridden by the site's own, `docs/stylesheets/NN-*.css` in order (`:root`, then
`[data-md-color-scheme="default"]` or `[data-md-color-scheme="slate"]`). Each pair below is
a text or a mark on a background as the site draws it; a translucent colour is composited
over what lies under it. Text needs 4.5:1, marks and controls (icons, bars, focus rings)
3:1. A pair under its minimum fails, so a new colour that reads badly stops the deploy.

    python tools/check_contrast.py          # every pair, both schemes
    python tools/check_contrast.py --all    # also print the pairs that pass
"""

from __future__ import annotations

import argparse
import colorsys
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# the site's stylesheets in their load order (mkdocs.yml lists the same parts)
STYLES = sorted((ROOT / "docs" / "stylesheets").glob("[0-9][0-9]-*.css"))

TEXT, UI = 4.5, 3.0

# (what, foreground, background, minimum); a background is a list, top layer first, for a
# translucent fill over another fill (a layer may differ by scheme: a dict). CARD is the
# explorer box's surface (white on the off-white page in the light scheme, W336).
PAGE = "var(--md-default-bg-color)"
TOAST = {"default": "var(--md-primary-fg-color)", "slate": "color-mix(in srgb, var(--md-primary-fg-color) 70%, #000)"}
CARD = {"default": "var(--site-surface)",
        "slate": "color-mix(in srgb, var(--md-default-fg-color) 4%, var(--md-default-bg-color))"}
PAIRS = [
    ("body text", "var(--md-default-fg-color)", [PAGE], TEXT),
    ("secondary text", "var(--md-default-fg-color--light)", [PAGE], TEXT),
    ("links", "var(--md-typeset-a-color)", [PAGE], TEXT),
    ("box header title", "var(--md-typeset-a-color)", ["color-mix(in srgb, var(--md-typeset-a-color) 7%, var(--md-default-bg-color))"], TEXT),
    ("code", "var(--md-code-fg-color)", ["var(--md-code-bg-color)"], TEXT),
    ("code keyword", "var(--md-code-hl-keyword-color)", ["var(--md-code-bg-color)"], TEXT),
    ("keyword, highlighted line", "var(--md-code-hl-keyword-color)", ["var(--md-code-hl-color--light)", "var(--md-code-bg-color)"], TEXT),
    ("comment, highlighted line", "var(--md-code-hl-comment-color)", ["var(--md-code-hl-color--light)", "var(--md-code-bg-color)"], TEXT),
    ("id label", "var(--site-label-color)", [PAGE], TEXT),
    ("chip easy", "var(--diff-easy)", ["var(--diff-easy-bg)", PAGE], TEXT),
    ("chip medium", "var(--diff-medium)", ["var(--diff-medium-bg)", PAGE], TEXT),
    ("chip hard", "var(--diff-hard)", ["var(--diff-hard-bg)", PAGE], TEXT),
    ("site header", "var(--md-primary-bg-color)", ["var(--md-primary-fg-color)"], TEXT),
    ("navy on amber (buttons)", "#1b2a4a", ["var(--md-accent-fg-color)"], TEXT),
    ("message and guide text", "#ffffff", [TOAST], TEXT),
    ("figure text", "var(--viz-text)", [PAGE], TEXT),
    ("follow-up answer label", "var(--adm-followup)", [PAGE], TEXT),
    ("self-check right", "var(--diff-easy)", ["var(--md-code-bg-color)", PAGE], TEXT),
    ("self-check wrong", "var(--diff-hard)", ["var(--md-code-bg-color)", PAGE], TEXT),
    ("self-check label", "var(--viz-text)", ["var(--md-code-bg-color)", PAGE], TEXT),
    ("figure ink", "var(--viz-ink)", [PAGE], TEXT),
    ("orange running text", "var(--viz-s2-text)", [PAGE], TEXT),
    *[(f"series {n} text in a box", f"var(--viz-s{n}-text)", [CARD, PAGE], TEXT) for n in (1, 2, 3, 4)],
    ("figure text in a box", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("pressed tool icon", "var(--md-typeset-a-color)", ["var(--site-primary-soft)", PAGE], UI),
    ("amber marks (star, sort)", "var(--site-mark-color)", [PAGE], UI),
    ("amber bar in the message", "var(--md-accent-fg-color)", [TOAST], UI),
    ("focus ring", "var(--site-focus-ring)", [PAGE], UI),
    ("chart blue", "var(--viz-s1)", [PAGE], UI),
    ("chart orange", "var(--viz-s2)", [PAGE], UI),
    ("chart green", "var(--viz-s3)", [PAGE], UI),
    ("map digit on high ground", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 29%, var(--md-default-bg-color))"], TEXT),
    ("map digit on deep water", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 45%, var(--md-default-bg-color))"], TEXT),
    ("table text on water", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 20%, var(--md-default-bg-color))"], TEXT),
    ("ladder cell label, chosen", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s2) 22%, var(--md-default-bg-color))"], TEXT),
    ("dead mouse number", "var(--md-default-bg-color)", ["var(--viz-ink)"], TEXT),
    ("tag on a doubled response", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 22%, var(--md-default-bg-color))"], TEXT),
    ("tag fault badge", "var(--md-default-bg-color)", ["var(--viz-ink)"], TEXT),
    ("coin of the first player", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("figure digit on the found square", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 45%, var(--md-default-bg-color))"], TEXT),
    ("ball number, maybe heavy", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))"], TEXT),
    ("ball number, maybe light", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 30%, var(--md-default-bg-color))"], TEXT),
    ("ball number, either", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s4) 30%, var(--md-default-bg-color))"], TEXT),
    ("ball number, known good", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-grid) 50%, var(--md-default-bg-color))"], TEXT),
    ("load number on the balance", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 14%, var(--md-default-bg-color))"], TEXT),
    *[(f"island number on colour {n}", "var(--viz-ink)", [f"color-mix(in srgb, var(--viz-s{n}) 40%, var(--md-default-bg-color))"], TEXT) for n in (1, 2, 3, 4, 5)],
    ("land not yet flooded", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 16%, var(--md-default-bg-color))"], TEXT),
    ("settled node time", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 30%, var(--md-default-bg-color))"], TEXT),
    ("corner link and relaxed edge", "var(--viz-s2)", [PAGE], UI),
    ("question count on the fold button", "var(--md-default-fg-color)", ["var(--site-primary-soft)", "var(--site-surface)"], TEXT),
    ("column grip line", "var(--site-mark-color)", [PAGE], UI),
    ("negative digit, current conversion row", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s1) 14%, var(--md-default-bg-color))", CARD, PAGE], TEXT),
    ("explanation step chip, lit", "var(--md-default-fg-color)", ["var(--md-accent-fg-color--transparent)", PAGE], TEXT),
    ("explanation step chip", "var(--viz-text)", [PAGE], TEXT),
    ("ladder cell label, a term", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s1) 18%, var(--md-default-bg-color))"], TEXT),
    *[(f"code {k}", f"var(--md-code-hl-{k}-color)", ["var(--md-code-hl-color--light)", "var(--md-code-bg-color)"], TEXT)
      for k in ("function", "special", "constant", "number", "string", "variable", "generic", "operator")],
    ("orange text, highlighted row", "var(--viz-s2-text)", ["var(--md-code-bg-color)"], TEXT),
    ("body text on a card", "var(--md-default-fg-color)", ["var(--site-surface)"], TEXT),
    ("trap group title", "var(--adm-trap)", ["var(--site-surface)"], TEXT),
    ("trap number", "var(--site-surface)", ["var(--adm-trap)"], TEXT),
    ("footer text", "var(--md-footer-fg-color)", ["var(--md-footer-bg-color)"], TEXT),
    ("footer secondary text", "var(--md-footer-fg-color--light)", ["var(--md-footer-bg-color--dark)"], TEXT),
    # round M (13-motion.css): the logo's check, the hero's live example, the footer's
    # counts, the question header's topic chips and the 404 page's waveform
    ("logo check on the header", "var(--site-logo-v)", ["var(--md-primary-fg-color)"], UI),
    ("hero example bits", "rgba(255, 255, 255, 0.72)", ["rgba(255, 255, 255, 0.08)", "rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("hero example title", "rgba(255, 255, 255, 0.78)", ["rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("amber on the navy card", "var(--md-accent-fg-color)", ["rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("footer count", "var(--md-footer-fg-color--light)", ["rgba(255, 255, 255, 0.1)", "var(--md-footer-bg-color--dark)"], TEXT),
    ("topic chip", "var(--md-default-fg-color--light)", [CARD, PAGE], TEXT),
    ("404 unknown state", "var(--site-x-state)", [TOAST], TEXT),
    ("404 signal names", "rgba(255, 255, 255, 0.62)", [TOAST], TEXT),
    ("edit link", "var(--md-default-fg-color--light)", [PAGE], TEXT),
    ("tag count on a tag chip", "var(--md-default-fg-color--light)", ["var(--site-surface)"], TEXT),
]

BLOCK = re.compile(r"([^{}]+)\{([^{}]*)\}")
PROP = re.compile(r"(--[\w-]+)\s*:\s*([^;]+)")


def blocks(css: str, selector: str) -> dict[str, str]:
    """The custom properties of every rule whose whole selector list contains selector."""
    out: dict[str, str] = {}
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for sel, body in BLOCK.findall(css):
        if selector in [s.strip().replace('"', "") for s in sel.split(",")]:
            out.update({k: v.strip() for k, v in PROP.findall(body)})
    return out


def material_css() -> str:
    import material
    folder = Path(material.__file__).parent / "templates" / "assets" / "stylesheets"
    return "".join(p.read_text() for p in sorted(folder.glob("*.min.css")))


def schemes() -> dict[str, dict[str, str]]:
    mat, extra = material_css(), "\n".join(p.read_text(encoding="utf-8") for p in STYLES)
    base = {**blocks(mat, ":root"), **blocks(mat, "[data-md-color-scheme=default]")}
    light = {**base, **blocks(extra, ":root"), **blocks(extra, "[data-md-color-scheme=default]")}
    dark = {**base, **blocks(mat, "[data-md-color-scheme=slate]"), **blocks(extra, ":root"),
            **blocks(extra, "[data-md-color-scheme=slate]")}
    return {"default": light, "slate": dark}


# --- colours: (r, g, b, a) with r, g, b in 0..1 -------------------------------------------

def resolve(value: str, props: dict[str, str], depth: int = 0) -> str:
    if depth > 20:
        raise ValueError(f"var() loop in {value}")
    def sub(m: re.Match) -> str:
        name, fallback = m.group(1), m.group(2)
        if name in props:
            return resolve(props[name], props, depth + 1)
        if fallback is not None:
            return fallback.strip()
        raise KeyError(name)
    while "var(" in value:
        value = re.sub(r"var\((--[\w-]+)(?:\s*,\s*([^()]*))?\)", sub, value)
    return value


def split_args(s: str) -> list[str]:
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
            continue
        depth += ch == "("
        depth -= ch == ")"
        cur += ch
    return out + [cur.strip()]


def num(s: str, scale: float = 1.0) -> float:
    s = s.strip()
    if s.endswith("%"):
        return float(s[:-1]) / 100
    if s.endswith("deg"):
        return float(s[:-3])
    return float(s) / scale


def parse(c: str) -> tuple[float, float, float, float]:
    c = c.strip()
    if c == "transparent":
        return (0.0, 0.0, 0.0, 0.0)
    if c.startswith("#"):
        h = c[1:]
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        vals = [int(h[i:i + 2], 16) / 255 for i in range(0, len(h), 2)]
        return (*vals[:3], vals[3] if len(vals) == 4 else 1.0)
    m = re.fullmatch(r"(rgba?|hsla?)\((.*)\)", c, re.S)
    if m:
        args = re.split(r"[\s,/]+", m.group(2).strip())
        a = num(args[3]) if len(args) > 3 else 1.0
        if m.group(1).startswith("rgb"):
            return (num(args[0], 255), num(args[1], 255), num(args[2], 255), a)
        r, g, b = colorsys.hls_to_rgb(num(args[0]) / 360, num(args[2]), num(args[1]))
        return (r, g, b, a)
    m = re.fullmatch(r"color-mix\(in srgb,(.*)\)", c, re.S)
    if m:
        (c1, *p1), (c2, *p2) = [part.rsplit(" ", 1) if part.rstrip().endswith("%") else [part] for part in split_args(m.group(1))]
        w1 = num(p1[0]) if p1 else (1 - num(p2[0]) if p2 else 0.5)
        w2 = num(p2[0]) if p2 else 1 - w1
        a, b = parse(c1), parse(c2)
        alpha = a[3] * w1 + b[3] * w2
        if alpha == 0:
            return (0.0, 0.0, 0.0, 0.0)
        mix = [(a[i] * a[3] * w1 + b[i] * b[3] * w2) / alpha for i in range(3)]   # premultiplied
        return (*mix, alpha)
    raise ValueError(f"cannot read the colour {c!r}")


def over(top, under):
    a = top[3] + under[3] * (1 - top[3])
    if a == 0:
        return (0.0, 0.0, 0.0, 0.0)
    return (*[(top[i] * top[3] + under[i] * under[3] * (1 - top[3])) / a for i in range(3)], a)


def luminance(c) -> float:
    lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c[:3]]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hexof(c) -> str:
    return "#" + "".join(f"{round(v * 255):02x}" for v in c[:3])


def check(show_all: bool = False) -> int:
    failures = 0
    for scheme, props in schemes().items():
        color = lambda v: parse(resolve(v, props))   # noqa: E731
        for what, fg, layers, minimum in PAIRS:
            layers = [layer[scheme] if isinstance(layer, dict) else layer for layer in layers]
            bg = (1.0, 1.0, 1.0, 1.0)
            for layer in reversed(layers):
                bg = over(color(layer), bg)
            r = ratio(over(color(fg), bg), bg)
            bad = r < minimum
            failures += bad
            if bad or show_all:
                print(f"{'FAIL' if bad else 'ok  '}  {scheme:7} {what:26} {r:5.2f}:1 (needs {minimum}) "
                      f"{hexof(over(color(fg), bg))} on {hexof(bg)}")
    print(f"{len(PAIRS)} colour pairs in 2 schemes, {failures} under their minimum")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--all", action="store_true", help="print the pairs that pass too")
    return check(ap.parse_args(argv).all)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
