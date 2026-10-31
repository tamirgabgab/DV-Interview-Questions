"""The shared Manim library of the tutorial videos (VIDEOS.md).

A question's `videos/<id>/scene.py` builds its chapters from these parts:

- `C`: the site's palette, read from the stylesheets in docs/stylesheets/ (no colour is
  typed here), with the navy of the home page's hero as the background;
- `T()` (Latin text, Inter), `M()` (code and numbers, a monospace font) and `he()` (a Hebrew
  label: a PNG drawn by the browser through he_label.py, since Manim draws no Hebrew);
- `DVQScene`: the base scene. `say()` / `beat()` play a beat under its caption and record
  the caption's real start and end, `opening()`, `chapter_card()` and `closing()` are the
  frames every video shares, and `tear_down()` writes the record for captions.py;
- `CodePanel`, `VarPanel`, `trace()`, `DVQScene.type_code()` and `DVQScene.run_code()`: the
  code beat. The code is read from the page's Python tab (tools/extract_code.py, the
  parser the tests use) and typed into its panel character by character, a caption after
  each line or group of lines (`type_code`); then it is run on the example with a line
  tracer, and its lines are lit in the order they ran, the variables beside it (`run_code`);
- small parts: `Cell` (a named value), `chip()`, `cost_chips()`.
"""

from __future__ import annotations

import contextlib
import copy
import inspect
import json
import os
import random
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from manim import (DOWN, Animation, Group, LEFT, ORIGIN, RIGHT, UP, Code, Create, FadeIn,
                   FadeOut, ImageMobject, Line, Mobject, Rectangle, RoundedRectangle, Scene,
                   Text, Transform, VGroup, VMobject, config, rate_functions)
from manim.constants import CapStyleType, LineJointType
from manim.mobject.svg.svg_mobject import SVGMobject
from pygments.style import Style
from pygments.token import (Comment, Keyword, Name, Number, Operator, Punctuation, String,
                            Token)

LIB = Path(__file__).resolve().parent
VIDEOS = LIB.parent
ROOT = VIDEOS.parent
STYLES = ROOT / "docs" / "stylesheets"
LOGO = ROOT / "docs" / "assets" / "logo.svg"
SITE_URL = "https://tamirgabgab.github.io/DV-Interview-Questions/"
sys.path.insert(0, str(LIB))
sys.path.insert(0, str(ROOT / "tools"))

import he_label  # noqa: E402

HEBREW = re.compile("[֐-׿]")
PX = 90.0          # frame pixels (720p) per Manim unit: 720 px / 8 units
SAFE_BOTTOM = -2.5 # the player draws the captions below this line: keep the picture above it
MIN_HOLD = 2.0     # every beat ends in a still frame held at least this long

# The typed code beat (DVQScene.type_code)
TYPE_CPS = 16.0        # typing speed, characters a second (the owner: about 12-20)
EOL_PAUSE = 0.3        # the pause at the end of a typed line inside a group
BAND_OPACITY = 0.13    # the soft highlight of the group under its caption
BLINK = 1.0            # the cursor's blink period while the typing pauses, on for 60 %
MONO_ADVANCE = 0.602   # DejaVu Sans Mono's advance width, in em
MIN_CODE_EM = 23.0     # the code's em in frame px at 720p: about 24 px, or the render fails

# --------------------------------------------------------------------------------------
# The palette, read from the site's stylesheets
# --------------------------------------------------------------------------------------


def _css_blocks(path: Path):
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", text):
        yield m.group(1).strip(), m.group(2)


def read_palette(files=("01-base.css", "02-pages.css", "08-explorers.css")) -> dict:
    """The custom properties of the stylesheets, per scheme ("default", "slate"; ":root"
    values are in both), plus the fills of the rules (`rule:<selector>`)."""
    schemes = {"default": {}, "slate": {}}
    rules = {}
    for name in files:
        for selector, body in _css_blocks(STYLES / name):
            found = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body))
            if selector == ":root":
                for s in schemes.values():
                    for k, v in found.items():
                        s.setdefault(k, v.strip())
            elif 'scheme="default"' in selector:
                schemes["default"].update({k: v.strip() for k, v in found.items()})
            elif 'scheme="slate"' in selector:
                schemes["slate"].update({k: v.strip() for k, v in found.items()})
            fill = re.search(r"(?:^|;)\s*fill\s*:\s*(#[0-9a-fA-F]{3,6})\s*;", body)
            if fill:
                rules[selector] = fill.group(1)

    def resolve(s: dict, v: str) -> str:
        while v.startswith("var("):
            v = s[v[4:].split(")")[0].split(",")[0].strip()]
        return v

    for s in schemes.values():
        for k in list(s):
            s[k] = resolve(s, s[k])
    return {"default": schemes["default"], "slate": schemes["slate"], "rules": rules}


def _blend(rgba: str, under: str) -> str:
    """An rgba() colour flattened onto a hex background."""
    r, g, b, a = [float(x) for x in re.findall(r"[\d.]+", rgba)]
    br, bg, bb = (int(under[i:i + 2], 16) for i in (1, 3, 5))
    mix = [round(c * a + d * (1 - a)) for c, d in ((r, br), (g, bg), (b, bb))]
    return "#{:02x}{:02x}{:02x}".format(*mix)


class _Palette:
    """Named colours of the videos, each one a CSS custom property of the site.

    The video has one look for both schemes: the hero's navy with white text. The marks
    on it take the dark scheme's values (made for 4.5:1 on a dark surface), and the amber
    is the logo's."""

    def __init__(self):
        p = read_palette()
        d, s, rules = p["default"], p["slate"], p["rules"]
        self.NAVY = d["--md-primary-fg-color"]                 # the hero, the background
        self.NAVY_DARK = d["--md-primary-fg-color--dark"]      # code panel
        self.NAVY_LIGHT = d["--md-primary-fg-color--light"]    # cells and cards
        self.WHITE = d["--md-primary-bg-color"]
        self.MUTED = _blend(d["--md-primary-bg-color--light"], self.NAVY)
        self.FAINT = _blend(s["--site-card-border"], self.NAVY)
        self.AMBER = d["--site-logo-v"]                        # the marks
        self.GREEN = s["--diff-easy"]
        self.RED = s["--diff-hard"]
        self.BLUE = s["--md-typeset-a-color"]
        self.ORANGE = s["--viz-s2-text"]
        self.PURPLE = s["--viz-s4"]
        self.CRATE = d["--viz-crate"]
        self.CRATE_TOP = d["--viz-crate-top"]
        self.CRATE_SIDE = d["--viz-crate-side"]
        self.CRATE_EDGE = d["--viz-crate-edge"]
        self.BALL_RED = rules[".md-typeset svg .b3-red"]
        self.BALL_BLACK = rules[".md-typeset svg .b3-black"]


C = _Palette()
config.background_color = C.NAVY

SANS = "Inter"
MONO = "DejaVu Sans Mono"


class NavyCode(Style):
    """Pygments colours of the code beat, from the palette."""
    background_color = C.NAVY_DARK
    line_number_color = C.FAINT
    styles = {
        Token: C.WHITE,
        Keyword: C.BLUE,
        Name.Builtin: C.PURPLE,
        Name.Function: C.GREEN,
        String: C.GREEN,
        Number: C.ORANGE,
        Operator: C.WHITE,
        Punctuation: C.WHITE,
        Comment: C.MUTED,
    }


# --------------------------------------------------------------------------------------
# Text: Latin through Pango, Hebrew through the browser
# --------------------------------------------------------------------------------------


def _no_hebrew(s: str) -> None:
    if HEBREW.search(s):
        raise ValueError(f"Hebrew text drawn by Manim: {s!r}; use he() (a he_label PNG)")


def T(s: str, size: float = 32, color: str | None = None, weight: str = "NORMAL", **kw) -> Text:
    """Latin text in Inter. `size` is Manim's font size (about 1.33 frame px per point)."""
    _no_hebrew(s)
    return Text(s, font=SANS, font_size=size, color=color or C.WHITE, weight=weight, **kw)


def M(s: str, size: float = 32, color: str | None = None, weight: str = "NORMAL", **kw) -> Text:
    """Code, numbers and formulas in the monospace font."""
    _no_hebrew(s)
    return Text(s, font=MONO, font_size=size, color=color or C.WHITE, weight=weight, **kw)


def X(s: str, size: float = 32, color: str | None = None, **kw) -> Text:
    """Math (a₀, 2³¹, ⊕) in Inter: its sub- and superscripts sit tight, unlike a
    monospace font's."""
    return T(s, size, color, **kw)


LABEL_PYTHON = os.environ.get("DVQ_LABEL_PYTHON", "python3")
COLLECT = os.environ.get("DVQ_COLLECT_LABELS")   # render.py's first pass: list the labels


def he(text: str, size: int = 36, color: str | None = None, weight: int = 500) -> ImageMobject:
    """A Hebrew label: the PNG he_label.py drew with the browser, at `size` frame px.

    render.py first runs the scenes with Manim's --dry_run and DVQ_COLLECT_LABELS set: each
    label is then only listed (and stood in for by a blank image), and he_label.py draws
    every missing label in one browser session before the real render. A label still
    missing at render time is drawn here, with the Python that has Playwright."""
    color = color or C.WHITE
    path = he_label.label_path(text, size, color, weight)
    if COLLECT:
        with open(COLLECT, "a", encoding="utf-8") as f:
            f.write(json.dumps({"text": text, "size": size, "color": color, "weight": weight},
                               ensure_ascii=False) + "\n")
        if not path.exists():
            w = int(len(text) * size * 0.55 * he_label.SCALE) + 2
            h = int(size * 1.4 * he_label.SCALE)
            img = ImageMobject(np.zeros((h, w, 4), dtype=np.uint8))
            img.height = h / he_label.SCALE / PX
            return img
    if not path.exists():
        subprocess.run([LABEL_PYTHON, str(LIB / "he_label.py"), text, "--size", str(size),
                        "--color", color, "--weight", str(weight)], check=True)
    img = ImageMobject(str(path))
    img.height = img.pixel_array.shape[0] / he_label.SCALE / PX
    return img


def chip(content: Mobject, color: str | None = None, fill: str | None = None,
         buff: float = 0.18, stroke: float = 2.5) -> VGroup:
    """A rounded chip around `content` (text or a label)."""
    color = color or C.AMBER
    box = RoundedRectangle(width=content.width + 2 * buff + 0.15, height=content.height + 2 * buff,
                           corner_radius=min(0.25, (content.height + 2 * buff) / 2),
                           stroke_color=color, stroke_width=stroke,
                           fill_color=fill or C.NAVY_DARK, fill_opacity=1)
    box.move_to(content)
    return VGroup(box, content) if isinstance(content, VMobject) else _Group(box, content)


def _Group(*mobs):
    return Group(*mobs)


def cost_chips(*pairs: tuple, notes: tuple = ()) -> VGroup:
    """The cost as chips, ("time", "O(1)"), ("memory", "0"), ..., each with an optional
    note under it (Latin: where the cost comes from)."""
    items = VGroup()
    for k, (key, value) in enumerate(pairs):
        g = VGroup(T(key, 32, C.MUTED), M(value, 46, C.AMBER)).arrange(RIGHT, buff=0.3)
        c = chip(g, color=C.AMBER, buff=0.25)
        if k < len(notes) and notes[k]:
            c = VGroup(c, T(notes[k], 28, C.MUTED).next_to(c, DOWN, buff=0.35))
        items.add(c)
    return items.arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(ORIGIN)


class Cell(VGroup):
    """A named value: a box with a monospace value and its name above it."""

    def __init__(self, name: str, value, width: float = 2.2, height: float = 1.45,
                 value_size: float = 56, name_size: float = 34, name_color: str | None = None):
        super().__init__()
        self.box = RoundedRectangle(width=width, height=height, corner_radius=0.16,
                                    stroke_color=C.MUTED, stroke_width=2.5,
                                    fill_color=C.NAVY_LIGHT, fill_opacity=1)
        self.name = M(name, name_size, name_color or C.MUTED).next_to(self.box, UP, buff=0.18)
        self.value_size = value_size
        self.value = M(str(value), value_size).move_to(self.box)
        self.add(self.box, self.name, self.value)

    def new_value(self, value, color: str | None = None) -> Text:
        return M(str(value), self.value_size, color or C.WHITE).move_to(self.box)

    def set_value(self, value, color: str | None = None):
        """The animation that turns the value into `value` in place."""
        return Transform(self.value, self.new_value(value, color))


# --------------------------------------------------------------------------------------
# The DV mark of the site, drawn stroke by stroke
# --------------------------------------------------------------------------------------


def dv_mark(height: float = 2.0) -> VGroup:
    """The logo (docs/assets/logo.svg): its two strokes, with the logo's widths and round
    caps, scaled so the D's centre line (y 14..50, 36 of the logo's units) is `height`."""
    svg = SVGMobject(str(LOGO))
    widths = [m.get_stroke_width() for m in svg.submobjects]
    svg.height = height                 # the paths' box: the D's centre line sets it
    unit = height / 36
    for m, w in zip(svg.submobjects, widths):
        m.set_stroke(width=w * unit * 100, opacity=1)
        m.set_fill(opacity=0)
        m.cap_style = CapStyleType.ROUND
        m.joint_type = LineJointType.ROUND
    return svg


# --------------------------------------------------------------------------------------
# The code beat
# --------------------------------------------------------------------------------------

ANNOTATION = re.compile(r"[ \t]*#[ \t]*\(\d+\)!?[ \t]*$")
ANNOTATION_IN_COMMENT = re.compile(r"(#[^\n]*?)[ \t]*\(\d+\)!?[ \t]*$")


def page_python(qid: int | str, marker: str) -> str:
    """The Python block of the page that contains `marker`, without the annotation
    markers (`# (1)!`, ` (1)` at the end of a comment), which only carry page notes."""
    import extract_code  # tools/extract_code.py: the parser the tests use

    code = extract_code.pick(qid, "python", marker)
    lines = []
    for line in code.rstrip("\n").split("\n"):
        line = ANNOTATION.sub("", line)
        line = ANNOTATION_IN_COMMENT.sub(r"\1", line)
        lines.append(line.rstrip())
    return "\n".join(lines) + "\n"


@dataclass
class Step:
    line: int          # 1-based line of the page code that ran
    state: dict        # the function's locals after the line ran
    event: str = "line"


def trace(code: str, func: str, args: tuple, env: dict | None = None) -> tuple[list[Step], object]:
    """Run `func` of the page `code` on `args` and record every line in the order it ran,
    with the locals after it. Returns (steps, result)."""
    ns = dict(env or {})
    exec(compile(code, "<page>", "exec"), ns)
    fn = ns[func]
    events = []

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<page>" or frame.f_code.co_name != func:
            return None
        if event in ("line", "return"):
            events.append((event, frame.f_lineno, copy.deepcopy(dict(frame.f_locals))))
        return tracer

    old = sys.gettrace()
    sys.settrace(tracer)
    try:
        result = fn(*args)
    finally:
        sys.settrace(old)
    steps = []
    for (ev, line, _), (_, _, after) in zip(events, events[1:]):
        if ev == "line":
            steps.append(Step(line, after))
    return steps, result


class CodePanel(VGroup):
    """The page's code in the navy theme, with a cursor that lights one line.

    `drop_comments` leaves full-line comments and blank lines out of the picture only, so a
    long function fits the frame; the code that runs is the page's, whole. The panel may be
    moved and scaled: the cursor is placed from its background."""

    def __init__(self, code: str, font_size: float = 24, drop_comments: bool = False,
                 drop_trailing_comments: bool = False, line_spacing: float = 0.7):
        super().__init__()
        shown, self.index = [], {}
        for n, line in enumerate(code.rstrip("\n").split("\n"), start=1):
            if drop_comments and (not line.strip() or line.strip().startswith("#")):
                continue
            if drop_trailing_comments and "#" in line and not line.strip().startswith("#"):
                line = line[:line.index("#")].rstrip()
            self.index[n] = len(shown)
            shown.append(line)
        self.lines_text = shown
        self.code = Code(code_string="\n".join(shown) + "\n", language="python",
                         formatter_style=NavyCode, add_line_numbers=False,
                         background="rectangle",
                         background_config={"fill_color": C.NAVY_DARK, "stroke_color": C.FAINT,
                                            "stroke_width": 2, "corner_radius": 0.18,
                                            "buff": 0.3},
                         paragraph_config={"font": MONO, "font_size": font_size,
                                           "line_spacing": line_spacing})
        self.add(self.code)
        ys, ns = [], []
        for i, line in enumerate(self.code.code_lines):
            if len(line) and shown[i].strip():
                ys.append(line.get_center()[1])
                ns.append(i)
        slope, y0 = np.polyfit(ns, ys, 1) if len(ns) > 1 else (-0.45, ys[0])
        top = self.code.background.get_top()[1]
        self._pitch = -slope
        self._rel0 = y0 - top            # line 0's centre, below the background's top
        self._h0 = self.code.background.height

    @property
    def background(self):
        return self.code.background

    @property
    def _s(self) -> float:
        return self.background.height / self._h0      # the scale since the panel was built

    def line_y(self, page_line: int) -> float:
        return self.background.get_top()[1] + (self._rel0 - self.index[page_line] * self._pitch) * self._s

    def bar(self, page_line: int) -> VGroup:
        """The cursor on `page_line` (1-based, in the page's code)."""
        bg = self.background
        y = self.line_y(page_line)
        h = self._pitch * 0.96 * self._s
        rect = Rectangle(width=bg.width - 0.12, height=h, stroke_width=0,
                         fill_color=C.AMBER, fill_opacity=0.17)
        rect.move_to([bg.get_center()[0], y, 0])
        tick = Rectangle(width=0.07, height=h, stroke_width=0, fill_color=C.AMBER, fill_opacity=1)
        tick.move_to([bg.get_left()[0] + 0.1, y, 0])
        return VGroup(rect, tick)

    # -- typing (DVQScene.type_code) ---------------------------------------------------------

    def text_of(self, page_line: int) -> str:
        return self.lines_text[self.index[page_line]]

    def shown(self) -> list[int]:
        """The page lines in the picture that hold code (not blank), in order."""
        return [n for n in self.index if self.text_of(n).strip()]

    def glyphs(self, page_line: int) -> dict[int, VMobject]:
        """The glyphs of a line by their column (a space has no glyph)."""
        text = self.text_of(page_line)
        cols = [c for c, ch in enumerate(text) if not ch.isspace()]
        line = self.code.code_lines[self.index[page_line]]
        if len(cols) != len(line):
            raise RuntimeError(f"line {page_line}: {len(cols)} characters, {len(line)} glyphs")
        return dict(zip(cols, line))

    def grid(self) -> tuple[float, float]:
        """(x0, pitch): the left edge of column 0 and the column width, as the panel is
        placed now. The font is monospace, so the centre of column c is x0 + (c + ½) pitch;
        the two are fitted to every glyph's centre (a glyph's ink sits near its cell's
        middle), and the fit is checked."""
        cs, xs = [], []
        for n in self.shown():
            for c, g in self.glyphs(n).items():
                cs.append(c)
                xs.append(g.get_center()[0])
        pitch, a = np.polyfit(cs, xs, 1)
        worst = max(abs(x - (a + pitch * c)) for c, x in zip(cs, xs))
        if worst > 0.4 * pitch:
            raise RuntimeError(f"the code's glyphs are not on a monospace grid (off by {worst / pitch:.2f})")
        return a - pitch / 2, pitch

    def em_px(self) -> float:
        """The code's font size (em) in frame pixels at 720p, as placed now."""
        return self.grid()[1] * PX / MONO_ADVANCE

    def caret(self, pitch: float) -> Rectangle:
        """The typing cursor: an amber bar of about a line's height."""
        h = self._pitch * self._s * 0.82
        return Rectangle(width=max(0.045, 0.16 * pitch), height=h, stroke_width=0,
                         fill_color=C.AMBER, fill_opacity=1)

    def band(self, lines: list[int]) -> Rectangle:
        """A soft highlight over `lines` (page lines), drawn under the text: it sits in the
        code group between the background and the text, invisible until faded in."""
        bg = self.background
        top = self.line_y(lines[0]) + self._pitch * self._s * 0.5
        bottom = self.line_y(lines[-1]) - self._pitch * self._s * 0.5
        rect = Rectangle(width=bg.width - 0.12, height=top - bottom, stroke_width=0,
                         fill_color=C.AMBER, fill_opacity=0)
        rect.move_to([bg.get_center()[0], (top + bottom) / 2, 0])
        self.code.submobjects.insert(self.code.submobjects.index(bg) + 1, rect)
        return rect

    def hide_text(self) -> None:
        for line in self.code.code_lines:
            for g in line:
                g.set_fill(opacity=0)


class _Typing(Animation):
    """One line typed: `events` is [(t, glyph or None, caret point)], the glyph shown and the
    caret moved at time t (seconds from the start). The animation's mobject is the code's
    text, so the renderer redraws it on every frame."""

    def __init__(self, text: Mobject, caret: Mobject, events: list, total: float):
        self.caret, self.events, self.total = caret, events, total
        super().__init__(text, run_time=total, rate_func=rate_functions.linear)

    def interpolate_mobject(self, alpha: float) -> None:
        t = alpha * self.total + 1e-9
        point = self.events[0][2]
        for te, glyph, p in self.events:
            if te <= t:
                point = p
            if glyph is not None:
                glyph.set_fill(opacity=1 if te <= t else 0)
        self.caret.move_to(point)
        self.caret.set_fill(opacity=1)


class _Blink(Animation):
    """The caret blinks while the typing pauses: on for 60 % of every BLINK seconds."""

    def __init__(self, caret: Mobject, total: float):
        self.total = total
        super().__init__(caret, run_time=total, rate_func=rate_functions.linear)

    def interpolate_mobject(self, alpha: float) -> None:
        on = (alpha * self.total) % BLINK < 0.6 * BLINK or alpha >= 1
        self.mobject.set_fill(opacity=1 if on else 0)


def _lines_of(spec) -> list[int]:
    if isinstance(spec, int):
        return [spec]
    return list(spec)


def _captions_of(spec) -> list[tuple[str, list]]:
    """A group's captions: "text", ("text", [anims]) or a list of those."""
    if isinstance(spec, str) or (isinstance(spec, tuple) and isinstance(spec[0], str)
                                 and len(spec) == 2 and isinstance(spec[1], list)):
        spec = [spec]
    return [(c, []) if isinstance(c, str) else (c[0], list(c[1])) for c in spec]


def baseline_text(s: str, size: float = 28, color: str | None = None) -> Text:
    """Monospace text that starts with an invisible "|", which spans the font's full
    height: two such texts aligned by their tops share a baseline, whatever they hold."""
    t = M("|" + s, size, color)
    t[0].set_opacity(0)
    return t


class VarPanel(VGroup):
    """The variables beside the code: one `name = value` row each, monospace. Only the
    value changes when a line runs; a changed value turns amber until `settle()`."""

    def __init__(self, names: list[str], fmt=None, size: float = 28, buff: float = 0.3,
                 cols: int = 1, slot: float = 4.0):
        """`cols` > 1 lays the rows out in a grid, `slot` units apart (room for the values)."""
        super().__init__()
        self.names = names
        self.fmt = fmt or (lambda name, state: repr(state[name]) if name in state else "")
        self.size = size
        keys = VGroup(*[baseline_text(f"{n} =", size, C.MUTED) for n in names])
        kw = max(k.width for k in keys)
        h = keys[0].height + buff
        for idx, k in enumerate(keys):
            c, r = idx % cols, idx // cols
            k.move_to([c * slot + kw - k.width / 2, -r * h, 0])
        self.keys = dict(zip(names, keys))
        self._kh0 = keys[0].height
        self.vals, self.values = {}, {}
        self.add(keys)
        for n in names:
            v = self._val(n, "", C.WHITE)
            self.vals[n] = v
            self.values[n] = ""
            self.add(v)

    def _val(self, n: str, text: str, color: str) -> Text:
        v = baseline_text(text, self.size, color)
        v.scale(self.keys[n].height / self._kh0)      # the panel may have been scaled
        v.next_to(self.keys[n], RIGHT, buff=0.08).align_to(self.keys[n], UP)
        return v

    def set_state(self, state: dict) -> "VarPanel":
        """Show `state` at once, in white (before the panel appears)."""
        for n in self.names:
            text = self.fmt(n, state)
            self.vals[n].become(self._val(n, text, C.WHITE))
            self.values[n] = text
        return self

    def show(self, state: dict, flash: bool = True) -> list:
        """Animations that bring every value to `state`: the changed ones turn amber, the
        ones that turned amber in the previous step go back to white."""
        anims = []
        hot = set()
        for n in self.names:
            text = self.fmt(n, state)
            if self.values[n] == text:
                if n in getattr(self, "hot", set()):
                    anims.append(self.vals[n].animate.set_color(C.WHITE))
                continue
            new = self._val(n, text, C.AMBER if flash else C.WHITE)
            anims.append(Transform(self.vals[n], new))
            self.values[n] = text
            hot.add(n)
        self.hot = hot
        return anims

    def settle(self) -> list:
        """Animations that turn the values back to white."""
        return [v[1:].animate.set_color(C.WHITE) for v in self.vals.values() if len(v) > 1]


# --------------------------------------------------------------------------------------
# The base scene: beats with recorded captions
# --------------------------------------------------------------------------------------


class DVQScene(Scene):
    """A chapter (or the opening / closing) of a question's video.

    Every beat runs under one caption: `say(text, *anims, hold=...)` plays the animations
    and then holds the still picture; `with self.beat(text, hold=...):` does the same for a
    block of several `play()` calls. The caption's start and end are the scene's clock as
    the beat really played (`self.time`), so the captions are in sync by construction.
    `tear_down()` writes them to `videos/<id>/out/parts/<Scene>.json` for captions.py."""

    def setup(self):
        self.camera.background_color = C.NAVY
        self.captions: list[dict] = []
        self.problems: list[str] = []
        self.code_ems: list[float] = []      # the typed code's em in px at 720p, per panel
        self._in_beat = False

    # -- the clock -------------------------------------------------------------------------

    def play(self, *args, run_time: float | None = None, **kw):
        """Every run time is a whole number of frames. Manim writes ceil(t * fps) frames for
        an animation but adds t itself to the clock when it reuses a cached one; on the frame
        grid the two agree, so the recorded captions match the file at any quality."""
        from manim.animation.animation import Wait
        if run_time is None and any(isinstance(a, Wait) for a in args):
            return super().play(*args, **kw)          # Scene.wait() (quantized there)
        n = max(1, round((1.0 if run_time is None else run_time) * config.frame_rate))
        return super().play(*args, run_time=n / config.frame_rate - 1e-7, **kw)

    def wait(self, duration: float = 1.0, *args, **kw):
        """A still of a whole number of frames (Manim writes int(t * fps) of them)."""
        n = max(1, round(duration * config.frame_rate))
        return super().wait(n / config.frame_rate + 1e-7, *args, **kw)

    # -- captions --------------------------------------------------------------------------

    def _record(self, text: str, start: float, end: float, hold: float):
        if hold < MIN_HOLD:
            self.problems.append(f"beat {text[:30]!r}: still frame {hold:.2f} s < {MIN_HOLD} s")
        self.captions.append({"text": text, "start": round(start, 4), "end": round(end, 4),
                              "hold": hold})

    @staticmethod
    def reading_hold(text: str, played: float) -> float:
        """The still after a beat's animations: enough to read the caption at about 14
        characters a second, between MIN_HOLD and 4 s."""
        need = len(text.replace("\n", " ")) / 14 + 0.6
        return float(min(4.0, max(MIN_HOLD, need - played)))

    def say(self, text: str, *anims, run_time: float = 1.5, hold: float | None = None, **kw):
        """One beat: play `anims` (if any), then hold the still picture under `text`."""
        start = self.time
        if anims:
            self.play(*anims, run_time=run_time, **kw)
        if hold is None:
            hold = self.reading_hold(text, self.time - start)
        self.wait(hold)
        self._record(text, start, self.time, hold)

    @contextlib.contextmanager
    def beat(self, text: str, hold: float | None = None):
        """One beat of several play() calls: `with self.beat(text): ...`."""
        start = self.time
        yield
        if hold is None:
            hold = self.reading_hold(text, self.time - start)
        self.wait(hold)
        self._record(text, start, self.time, hold)

    def pause(self, t: float = 0.5):
        """A short silent pause between beats (no caption)."""
        self.wait(t)

    def tear_down(self):
        out = Path(inspect.getfile(type(self))).resolve().parent / "out" / "parts"
        out.mkdir(parents=True, exist_ok=True)
        record = {"scene": type(self).__name__, "duration": round(self.time, 4),
                  "fps": config.frame_rate, "captions": self.captions, "problems": self.problems,
                  "code_em_px": [round(e, 1) for e in self.code_ems]}
        (out / f"{type(self).__name__}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")

    # -- the code beat -----------------------------------------------------------------------

    def place_code(self, panel: "CodePanel", vp: "VarPanel", extra: Mobject | None = None,
                   max_width: float = 13.2, max_height: float = 6.0, vp_width: float | None = None):
        """Side by side when it fits (`vp_width`: the variables' widest, if wider than now),
        else the variables under the code; scaled down to fit the frame, centred."""
        vw = max(vp.width, vp_width or 0)
        side = panel.width + 0.9 + vw <= max_width
        if side:
            body = VGroup(panel, vp).arrange(RIGHT, buff=0.9, aligned_edge=UP)
            vp.align_to(panel, UP).shift(DOWN * 0.3)
        else:
            body = VGroup(panel, vp).arrange(DOWN, buff=0.6)
            vp.align_to(panel, LEFT).shift(RIGHT * 0.3)
        group = VGroup(body) if extra is None else VGroup(body, extra)
        if extra is not None:
            extra.next_to(body, DOWN, buff=0.6)
        need = panel.width + 0.9 + vw if side else max(panel.width, vw)
        k = min(1.0, max_width / need, max_height / group.height)
        if k < 1:
            group.scale(k)
        group.move_to(UP * (3.75 + SAFE_BOTTOM) / 2)      # between the top and the captions
        if side:   # centre the widest the variables get, not the empty panel
            group.shift(LEFT * (vw - vp.width) * k / 2)
        return group

    def type_code(self, panel: "CodePanel", groups: list, intro: str | None = None,
                  intro_anims: tuple = (), cps: float = TYPE_CPS, seed: int = 0):
        """The code beat's first half: the page's code typed into its panel as if someone
        wrote it live, a pause and a caption after each line or group of lines.

        `panel` is the CodePanel of the page's code (`page_python`), already placed for the
        whole code (`place_code`, with the variables' room kept free), so nothing moves
        while it fills; the traced run (`run_code`) reuses it. `groups` is
        [(lines, caption), ...]: `lines` a page line, a range or a list of page lines, the
        groups covering every line in the picture in order; `caption` a text, a pair
        (text, [animations played as it appears]) or a list of those (several beats in
        one pause). `intro` is a caption for the empty panel as it appears.

        Each character appears at about `cps` a second (a seeded jitter of ±30 %), the
        amber caret just after it; the indentation appears at once, a line inside a group
        ends with a short pause, and after a group the typing stops: its lines are lit
        softly under the caption, held for reading (`reading_hold`, 2-4 s) while the caret
        blinks. Fails when the groups do not cover the code, and records a problem when the
        code's text is under MIN_CODE_EM px."""
        shown = panel.shown()
        plan = [(_lines_of(lines), _captions_of(cap)) for lines, cap in groups]
        planned = [n for lines, _ in plan for n in lines]
        if planned != shown:
            raise RuntimeError(f"the groups type lines {planned}, the panel shows {shown}")
        x0, pitch = panel.grid()
        em = pitch * PX / MONO_ADVANCE
        if em < MIN_CODE_EM:
            self.problems.append(f"code text {em:.1f} px high at 720p (at least {MIN_CODE_EM})")
        self.code_ems.append(em)
        rng = random.Random(seed or len(shown) * 7919 + len(panel.lines_text[0]))

        def point(n: int, col: int):
            return np.array([x0 + col * pitch + caret.width / 2, panel.line_y(n), 0.0])

        def indent(n: int) -> int:
            text = panel.text_of(n)
            return len(text) - len(text.lstrip())

        panel.hide_text()
        caret = panel.caret(pitch)
        caret.move_to(point(shown[0], indent(shown[0])))
        start = self.time
        self.play(FadeIn(panel), FadeIn(caret), *intro_anims, run_time=1.0)
        if intro:
            hold = self.reading_hold(intro, self.time - start)
            self.play(_Blink(caret, hold), run_time=hold)
            self._record(intro, start, self.time, hold)
        for lines, captions in plan:
            for li, n in enumerate(lines):
                text, glyphs = panel.text_of(n), panel.glyphs(n)
                t = 0.0
                events = [(0.0, None, point(n, indent(n)))]
                for col in range(indent(n), len(text)):
                    t += rng.uniform(0.7, 1.3) / cps
                    events.append((t, glyphs.get(col), point(n, col + 1)))
                total = t + (EOL_PAUSE if li < len(lines) - 1 else 0.15)
                self.play(_Typing(panel.code.code_lines, caret, events, total),
                          Animation(caret), run_time=total)
            band = panel.band(lines)
            for k, (text, anims) in enumerate(captions):
                start = self.time
                light = [band.animate.set_fill(opacity=BAND_OPACITY)] if k == 0 else []
                if light or anims:
                    self.play(*light, *anims, run_time=1.0 if anims else 0.5)
                hold = self.reading_hold(text, self.time - start)
                self.play(_Blink(caret, hold), run_time=hold)
                self._record(text, start, self.time, hold)
            self.play(band.animate.set_fill(opacity=0), run_time=0.3)
            panel.code.remove(band)
        self.play(FadeOut(caret), run_time=0.4)

    def run_code(self, panel: "CodePanel", vp: "VarPanel", steps: list, groups: list,
                 step_time: float = 2.4):
        """Light the lines in the order they ran: `groups` is [(lines, caption), ...], the
        lines of consecutive trace steps under one caption. The lines must be exactly the
        trace's, in order, so the video follows the page's code as it really runs."""
        planned = [n for lines, _ in groups for n in lines]
        ran = [s.line for s in steps]
        if planned != ran:
            raise RuntimeError(f"the code ran lines {ran}, the script lights {planned}")
        cursor = None
        k = 0
        for lines, caption in groups:
            with self.beat(caption):
                per = min(1.0, step_time / len(lines))
                for _ in lines:
                    step = steps[k]
                    k += 1
                    bar = panel.bar(step.line)
                    move = FadeIn(bar) if cursor is None else Transform(cursor, bar)
                    self.play(move, *vp.show(step.state), run_time=per)
                    cursor = cursor or bar
        return cursor

    # -- shared frames ---------------------------------------------------------------------

    def fade_all(self, run_time: float = 0.8):
        """Fade everything out."""
        mobs = [m for m in self.mobjects]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def opening(self, qid: int, level: str, title: str, parts: list[str], captions: list[str],
                holds=(None, None)):
        """The DV mark drawn as on the site, the id, the title and level, the parts as chips.
        `captions` has two lines: one for the mark and the id, one for the parts."""
        mark = dv_mark(2.0)
        ident = M(f"{qid:04d}", 80, C.AMBER, weight="BOLD")
        head = VGroup(mark, ident).arrange(RIGHT, buff=0.6).move_to(UP * 2.0)
        name = he(title, 52, C.WHITE, 600)
        lvl = chip(he(level, 34, C.AMBER, 500), color=C.AMBER)
        line = _Group(name, lvl).arrange(LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        chips = _Group(*[chip(he(p, 34, C.WHITE, 500), color=C.MUTED, fill=C.NAVY_LIGHT, stroke=1.5)
                         for p in parts]).arrange(LEFT, buff=0.35)
        chips.next_to(line, DOWN, buff=0.7)
        if chips.width > 12.6:
            chips.arrange_in_grid(cols=2, buff=(0.35, 0.3)).next_to(line, DOWN, buff=0.6)
        whole = Group(head, line, chips)
        shift = -whole.get_center()[1] + 0.2
        for m in (head, line, chips):
            m.shift(UP * shift)
        with self.beat(captions[0], hold=holds[0]):
            self.play(Create(mark, lag_ratio=0.6), run_time=1.6, rate_func=rate_functions.smooth)
            self.play(FadeIn(ident, shift=0.2 * LEFT), FadeIn(name), FadeIn(lvl), run_time=1.0)
        self.say(captions[1], *[FadeIn(c, shift=0.2 * UP) for c in chips], lag_ratio=0.25,
                 run_time=1.5, hold=holds[1])
        return VGroup(mark, ident), name, lvl, chips

    def chapter_card(self, letter: str, title: str, caption: str, hold: float | None = None,
                     note: Mobject | None = None, keep: bool = False):
        """The chapter's card: "סעיף א" and its title (Hebrew labels), an amber rule."""
        big = he(letter, 80, C.AMBER, 700)
        sub = he(title, 48, C.WHITE, 500)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, stroke_color=C.AMBER, stroke_width=4)
        group = _Group(big, rule, sub).arrange(DOWN, buff=0.35)
        if note is not None:
            group.add(note)
            note.next_to(sub, DOWN, buff=0.5)
        group.move_to(ORIGIN)
        self.say(caption, FadeIn(big, shift=0.2 * DOWN), Create(rule), FadeIn(sub),
                 run_time=1.2, hold=hold)
        if not keep:
            self.play(FadeOut(group), run_time=0.7)
        return group

    def closing(self, qid: int, rows: list[tuple[str, Mobject]], captions: list[str],
                holds=(None, None)):
        """One line per part (its Hebrew name and the picture or code of its answer), then
        the site's address and the question's id."""
        tags = [chip(he(name, 34, C.AMBER, 600), color=C.AMBER) for name, _ in rows]
        whats = [what for _, what in rows]
        tag_w = max(t.width for t in tags)
        what_w = max(w.width for w in whats)
        gap = 0.6
        x_left = -(tag_w + gap + what_w) / 2
        total = sum(max(t.height, w.height) for t, w in zip(tags, whats)) + 0.5 * (len(rows) - 1)
        y = 1.5 + total / 2
        lines = []
        for tag, what in zip(tags, whats):
            h = max(tag.height, what.height)
            y -= h / 2
            what.move_to([x_left + what.width / 2, y, 0])
            tag.move_to([x_left + what_w + gap + tag_w - tag.width / 2, y, 0])
            y -= h / 2 + 0.5
            lines.append((what, tag))
        with self.beat(captions[0], hold=holds[0]):
            for what, tag in lines:
                self.play(FadeIn(tag), FadeIn(what, shift=0.2 * LEFT), run_time=0.8)
        mark = dv_mark(0.7)
        url = M(SITE_URL, 24, C.WHITE)
        ident = M(f"#{qid:04d}", 34, C.AMBER, weight="BOLD")
        foot = VGroup(mark, VGroup(url, ident).arrange(DOWN, buff=0.15, aligned_edge=LEFT)) \
            .arrange(RIGHT, buff=0.35).move_to(DOWN * 1.9)
        self.say(captions[1], Create(mark), FadeIn(url), FadeIn(ident), run_time=1.4,
                 hold=holds[1])
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.5)
