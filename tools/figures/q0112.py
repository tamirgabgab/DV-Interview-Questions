#!/usr/bin/env python3
"""Figures, logs and the table of question 0112, the factory override that did not take.

    python tools/figures/fill.py 112        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The logs and the table come from a small model of the testbench's build
(factory_build): which class the factory gives each component (only create asks it; an
instance path matched by fnmatch against the full name, as pyuvm does, before the type
override) and how many items of the eight each driver sends with a wrong parity bit.
tests/0112 runs the page's pyuvm testbench on Verilator in every scenario and checks the
run prints exactly these lines; the page's box (docs/javascripts/explorer/factory.js) holds
the same model, checked against this one by tests/0112/test_0112_box.py.
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

# The instance overrides tests/0112 runs: the path given to set_inst_override_by_type and
# where the call is made. "build" is the test's build_phase before Env.create (part b's
# table), "build_after" the same phase after it, "connect" the test's connect_phase,
# "before_run" the cocotb test before run_test (a follow-up).
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
TIMES = ("build", "build_after", "connect", "before_run")

# The components in the order pyuvm's build phase creates them (top-down: the test's
# build_phase creates env, env's creates the agents, then each agent's creates its two
# children): the full name, the class asked for, and the line that builds it. The two
# agents run the same build_phase, so the lines "seqr" and "drv" build both of each.
TREE = [
    (f"{TEST_TOP}.env", "Env", "env"),
    (f"{TEST_TOP}.env.agt0", "Agent", "agt0"),
    (f"{TEST_TOP}.env.agt1", "Agent", "agt1"),
    (f"{TEST_TOP}.env.agt0.seqr", "uvm_sequencer", "seqr"),
    (f"{TEST_TOP}.env.agt0.drv", "ParityDriver", "drv"),
    (f"{TEST_TOP}.env.agt1.seqr", "uvm_sequencer", "seqr"),
    (f"{TEST_TOP}.env.agt1.drv", "ParityDriver", "drv"),
]
LINES = ("env", "agt0", "agt1", "seqr", "drv")
NAMES = [TEST_TOP] + [full for full, _, _ in TREE]
REQUESTED = {TEST_TOP: "ErrTest", **{full: req for full, req, _ in TREE}}


def wrong_items(cls: str) -> int:
    """Items an instance of cls sends with a wrong parity bit: ErrDriver flips every
    fourth item (sent % 4 == 3, sent counted before the item)."""
    return sum(1 for sent in range(ITEMS) if sent % 4 == 3) if cls == "ErrDriver" else 0


def why(full: str, pattern: str) -> tuple[str, str]:
    """How an instance path compares with a component's full name, as pyuvm matches it
    (fnmatch against the whole name; case-sensitive on Linux): ("match", full); ("suffix",
    the missing start) when the pattern matches the name without its first parts;
    ("ancestor", name) when it matches a component above this one; ("other", name) when it
    matches another component (one asked for as the same class first); ("none", "")."""
    if fnmatch.fnmatchcase(full, pattern):
        return "match", full
    parts = full.split(".")
    for k in range(1, len(parts)):
        if fnmatch.fnmatchcase(".".join(parts[k:]), pattern):
            return "suffix", ".".join(parts[:k])
    for k in range(len(parts) - 1, 0, -1):
        if fnmatch.fnmatchcase(".".join(parts[:k]), pattern):
            return "ancestor", ".".join(parts[:k])
    others = sorted((n for n in NAMES if n != full), key=lambda n: REQUESTED[n] != REQUESTED[full])
    for n in others:
        if fnmatch.fnmatchcase(n, pattern):
            return "other", n
    return "none", ""


def factory_build(how: dict, mode: str, path: str = "", when: str = "build") -> list[dict]:
    """The build, one component at a time: how each line builds ("create" or "new"), the
    override of ParityDriver by ErrDriver ("type", "inst" with an instance path, or "none")
    and when the test sets it (one of TIMES). The override is in the factory for a creation
    only if set in the test's build_phase: before Env.create for every one, after it for
    all but env; never if set in connect_phase (the tree is built by then) or before
    run_test (which clears it). Only create asks the factory, and only a request for
    ParityDriver can match: its instance path, else the type override."""
    out = []
    for i, (full, req, line) in enumerate(TREE):
        on = mode != "none" and (when == "build" or (when == "build_after" and i >= 1))
        cls, via, checks = req, None, []
        if how[line] == "create" and on and req == "ParityDriver":
            if mode == "inst":
                checks.append(list(why(full, path)))
                if checks[0][0] == "match":
                    cls, via = "ErrDriver", "inst"
            elif mode == "type":
                cls, via = "ErrDriver", "type"
        out.append({"full": full, "req": req, "line": line, "how": how[line], "on": on,
                    "cls": cls, "via": via, "checks": checks})
    return out


def built(type_override: bool = False, inst: tuple[str, str] | None = None, drv: str = "create") -> list[str]:
    """The class each driver is built as: with a type override set in the test's
    build_phase, or an instance override (path, when); the agent's driver line by create
    or by new."""
    how = dict.fromkeys(LINES, "create") | {"drv": drv}
    if type_override:
        steps = factory_build(how, "type")
    elif inst:
        steps = factory_build(how, "inst", *inst)
    else:
        steps = factory_build(how, "none")
    return [s["cls"] for s in steps if s["full"] in DRIVERS]


def log_lines(classes: list[str]) -> list[str]:
    """The report_phase lines of the test (the message part of the log)."""
    return [f"{p}: {c}, {wrong_items(c)} parity errors" for p, c in zip(DRIVERS, classes)]


def factory_lines(path: str) -> list[str]:
    """uvm_factory().print(0) with one instance override of ParityDriver (pyuvm's format)."""
    return ["--- overrides ---", "", "Overrides:",
            f"{'ParityDriver':25}: {'Type Override: None':25} || Instance Overrides: {path} => ErrDriver"]


def text_block(lines: list[str]) -> str:
    return "```text\n" + "\n".join(lines) + "\n```"


def bug_log():
    """The statement: the type override is set, the agent builds the driver with new."""
    return text_block(log_lines(built(type_override=True, drv="new")))


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
    """Part b's table: the instance paths set in the test's build_phase."""
    rows = ["| הנתיב | מי נבנה כ-`ErrDriver` |", "|---|---|"]
    rows += [f"| {RLM}`{path}` | {who(built(inst=(path, when)))} |" for path, when in ROWS if when == "build"]
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


def blocks():
    """The generated blocks, in page order."""
    return [bug_log(), create_figure() + "\n\n" + create_legend(), fixed_log(), colleague_log(), path_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
