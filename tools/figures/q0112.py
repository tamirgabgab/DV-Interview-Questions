#!/usr/bin/env python3
"""Figures, logs and the table of question 0112, the factory override that did not take.

    python tools/figures/fill.py 112        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The logs and the table come from a small model of the testbench: which
class the factory gives each driver (fnmatch on its full name, as pyuvm matches an
instance path; an instance override before the type override) and how many items of the
eight each driver sends with a wrong parity bit. tests/0112 runs the page's pyuvm
testbench on Verilator in every scenario and checks the run prints exactly these lines.
"""

from __future__ import annotations

import fnmatch

NB = " "
RLM = "‏"

ITEMS = 8                   # items per channel (the Bytes sequence)
TEST_TOP = "uvm_test_top"   # the name run_test gives the test
DRIVERS = [f"{TEST_TOP}.env.agt{ch}.drv" for ch in (0, 1)]
GOOD_PATH = f"{TEST_TOP}.env.agt1.drv"
BAD_PATH = "env.agt1.drv"   # the colleague's path in part b

# Part b's table: the instance path given to set_inst_override_by_type, where the call is
# made, and the cocotb test of tests/0112 that runs it. "build" is the test's build_phase
# before Env.create, "build_after" the same phase after it, "connect" the test's
# connect_phase, "before_run" the cocotb test before run_test.
ROWS = [
    (GOOD_PATH, "build"),
    (BAD_PATH, "build"),
    (f"{TEST_TOP}.env.agt1", "build"),
    ("*.agt1.*", "build"),
    (f"{TEST_TOP}.env.agt*.drv", "build"),
    (GOOD_PATH, "build_after"),
    (GOOD_PATH, "connect"),
    (GOOD_PATH, "before_run"),
]
WHEN = {
    "build": "‏`build_phase`, לפני `Env.create`",
    "build_after": "‏`build_phase`, אחרי `Env.create`",
    "connect": "‏`connect_phase`",
    "before_run": "לפני `run_test`",
}


def wrong_items(cls: str) -> int:
    """Items an instance of cls sends with a wrong parity bit: ErrDriver flips every
    fourth item (sent % 4 == 3, sent counted before the item)."""
    return sum(1 for sent in range(ITEMS) if sent % 4 == 3) if cls == "ErrDriver" else 0


def built(type_override: bool = False, inst: tuple[str, str] | None = None) -> list[str]:
    """The class the factory builds for each driver path. An instance override counts only
    when it is in the factory when the agent's build_phase creates the driver: set in the
    test's build_phase (before or after Env.create, since the drivers are created two
    levels down), not after the build or before run_test, which clears the overrides."""
    out = []
    for path in DRIVERS:
        cls = "ErrDriver" if type_override else "ParityDriver"
        if inst and inst[1] in ("build", "build_after") and fnmatch.fnmatch(path, inst[0]):
            cls = "ErrDriver"
        out.append(cls)
    return out


def log_lines(classes: list[str]) -> list[str]:
    """The report_phase lines of ErrTest (the message part of the log)."""
    return [f"{p}: {c}, {wrong_items(c)} parity errors" for p, c in zip(DRIVERS, classes)]


def factory_lines(path: str) -> list[str]:
    """uvm_factory().print(0) with one instance override of ParityDriver (pyuvm's format)."""
    return ["--- overrides ---", "", "Overrides:",
            f"{'ParityDriver':25}: {'Type Override: None':25} || Instance Overrides: {path} => ErrDriver"]


def text_block(lines: list[str]) -> str:
    return "```text\n" + "\n".join(lines) + "\n```"


def bug_log():
    """The statement: the type override is set, the agent builds the driver with new."""
    return text_block(log_lines(["ParityDriver", "ParityDriver"]))


def fixed_log():
    """Part a after the fix: the agent asks the factory."""
    return text_block(log_lines(built(type_override=True)))


def colleague_log():
    """Part b: the factory print and the report of the colleague's instance path."""
    return text_block(factory_lines(BAD_PATH) + [""] + log_lines(built(inst=(BAD_PATH, "build"))))


def who(classes: list[str]) -> str:
    """The drivers built as ErrDriver, in words."""
    err = [p.split(".")[-2] for p, c in zip(DRIVERS, classes) if c == "ErrDriver"]
    return {0: "אף אחד", 1: f"רק `{err[0]}`" if err else "", 2: "**שניהם**"}[len(err)]


def path_table():
    """The rows set in the test's build_phase, by path."""
    rows = ["| הנתיב | מי נבנה כ-`ErrDriver` |", "|---|---|"]
    rows += [f"| {RLM}`{path}` | {who(built(inst=(path, when)))} |" for path, when in ROWS if when == "build"]
    return "\n".join(rows)


def time_table():
    """The full path, set at each time."""
    rows = ["| מתי נקבע | מי נבנה כ-`ErrDriver` |", "|---|---|"]
    rows += [f"| {WHEN[when]} | {who(built(inst=(path, when)))} |" for path, when in ROWS if path == GOOD_PATH]
    return "\n".join(rows)


# --- figures ---------------------------------------------------------------------------

ARROW = ('<defs><marker id="fo-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
         'markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>')


def box(x, y, w, h, lines, cls=""):
    cx = x + w / 2
    first = y + h / 2 + 5 - 9 * (len(lines) - 1)
    text = "".join(f'<text x="{cx:g}" y="{first + 18 * i:g}" text-anchor="middle">{t}</text>'
                   for i, t in enumerate(lines))
    return f'<g class="uv-box{" " + cls if cls else ""}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>{text}</g>'


def cont(x, y, w, h, label):
    return (f'<g class="uv-box is-cont"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
            f'<text x="{x + 8}" y="{y + 17}">{label}</text></g>')


def arrow(x1, y1, x2, y2, kind):
    return f'<line class="uv-arrow uv-{kind}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#fo-arrow)"/>'


def create_figure():
    """Part a: a direct constructor call never reaches the factory; create asks it."""
    w, h = 420, 256
    s = (f'<svg class="figure uv-fig" viewBox="0 0 {w} {h}" style="max-width:28rem" role="img" '
         f'aria-label="שתי דרכים לבנות את ה-driver{NB}: קריאה ישירה ל-ParityDriver בונה ParityDriver, '
         'ו-create עובר דרך ה-factory, שמחזיר ErrDriver">' + ARROW)
    s += ('<g class="uv-box is-cont"><text x="105" y="24" text-anchor="middle">ParityDriver("drv", self)</text>'
          '<text x="315" y="24" text-anchor="middle">ParityDriver.create(…)</text></g>')
    s += arrow(105, 36, 105, 196, "pin")
    s += arrow(315, 36, 315, 76, "tlm")
    s += box(230, 80, 170, 72, ["factory", "ParityDriver", "→ ErrDriver"], "uv-scoreboard")
    s += arrow(315, 152, 315, 196, "tlm")
    s += box(35, 200, 140, 44, ["ParityDriver"])
    s += box(245, 200, 140, 44, ["ErrDriver"], "uv-dut")
    return s + "</svg>"


def create_legend():
    return (f'<span class="viz-legend"><span><i class="uv-key-pin"></i>קריאה ישירה לבנאי{NB}: ה-factory לא נשאל</span>'
            f'<span><i class="uv-key-tlm"></i>דרך create{NB}: ה-factory בוחר את ה-class</span></span>')


def tree_figure():
    """Part b: the components and their full names; the override reaches agt1's driver."""
    classes = built(inst=(GOOD_PATH, "build"))
    w, h = 480, 232
    s = (f'<svg class="figure uv-fig" viewBox="0 0 {w} {h}" style="max-width:30rem" role="img" '
         f'aria-label="עץ הרכיבים{NB}: uvm_test_top, בתוכו env, בתוכו agt0 ו-agt1, ובכל אחד seqr ו-drv. '
         'ה-drv של agt1 נבנה כ-ErrDriver">')
    s += cont(6, 6, 468, 220, TEST_TOP) + cont(16, 32, 448, 184, "env")
    for ch, x in ((0, 26), (1, 246)):
        s += cont(x, 58, 208, 148, f"agt{ch}")
        s += box(x + 10, 84, 188, 40, ["seqr"])
        s += box(x + 10, 136, 188, 56, ["drv", classes[ch]], "uv-dut" if classes[ch] == "ErrDriver" else "")
    return s + "</svg>"


def blocks():
    """The generated blocks, in page order."""
    return [bug_log(), create_figure(), create_legend(), fixed_log(), tree_figure(), colleague_log(),
            path_table(), time_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
