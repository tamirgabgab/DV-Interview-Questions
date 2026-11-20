#!/usr/bin/env python3
"""Write tests/0111/tb.sv: the page's DUT and testbench in all 16 combinations of the fixes.

    python tests/0111/matrix.py        # after a change to the page's code or seeds

One compile cannot hold two modules named reg_slice, so the testbench is assembled from
the page's SystemVerilog blocks as published: the statement's reg_slice and slice_tb
(combination 0000, kept under their own names), part a's coverage section with
BACKPRESSURE = 1, part b's and part c's sections in place of the statement's sections
with the same title (the line "// ---- <title>: ..."), and part d's reg_slice, renamed
reg_slice_fixed. Every combination runs with each of SEEDS, and a final block compares its
error count, first error, counts, items left in the scoreboard and cover counters with
the page's Python model (run_bench). test_0111_tb.py fails when tb.sv is not what this
script writes from the current page.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools" / "figures")]
from extract_code import load_python, pick  # noqa: E402
import q0111  # noqa: E402

SEEDS = (187, 17, 44, 481, 51489)   # the page's; no stall at all; stalls but no loss; seven lost items; another
HEADER = re.compile(r"^// ---- ([^:]+):", re.M)


def sv(marker: str) -> str:
    return pick(111, "systemverilog", marker)


def indent(block: str) -> str:
    return "".join("  " + line if line.strip() else line for line in block.splitlines(keepends=True))


def sections(bench: str) -> tuple[str, list[tuple[str, str]], str]:
    """The bench split at its "  // ---- <title>:" lines: the head, [(title, text)], the tail."""
    lines = bench.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.startswith("  // ---- ")]
    end = max(i for i, line in enumerate(lines) if line.startswith("endmodule"))
    head = "".join(lines[:starts[0]])
    parts = []
    for a, b in zip(starts, starts[1:] + [end]):
        title = HEADER.match(lines[a].strip()).group(1)
        parts.append((title, "".join(lines[a:b]).rstrip("\n") + "\n"))
    return head, parts, "".join(lines[end:])


def title_of(fix: str) -> str:
    return HEADER.match(fix).group(1)


def code_of(bp: int, sva: int, sb: int, fx: int) -> str:
    return f"{bp}{sva}{sb}{fx}"


def bench_variant(bench: str, fixes: dict, bp: int, sva: int, sb: int, fx: int) -> str:
    head, parts, tail = sections(bench)
    code = code_of(bp, sva, sb, fx)
    if code != "0000":
        head = head.replace("module slice_tb #(", f"module slice_tb_{code} #(", 1)
    if bp:
        old = "parameter bit          BACKPRESSURE = 0,"
        assert head.count(old) == 1, "the statement's BACKPRESSURE default moved"
        head = head.replace(old, old.replace("= 0", "= 1"))
        at = [t for t, _ in parts].index("stimulus") + 1
        parts.insert(at, (title_of(fixes["coverage"]), indent(fixes["coverage"])))
    out = []
    for title, text in parts:
        if title == "handshake rule" and sva:
            text = indent(fixes["handshake rule"])
        if title == "scoreboard" and sb:
            text = indent(fixes["scoreboard"])
        out.append(text)
    if fx:
        assert head.count("  reg_slice dut (.*);") == 1
        head = head.replace("  reg_slice dut (.*);", "  reg_slice_fixed dut (.*);")
    return head + "\n".join(out) + tail


def expected_checks(ns, name: str, seed: int, bp: int, sva: int, sb: int, fx: int) -> str:
    r = ns["run_bench"](seed, bp, sva, sb, fx)
    msg = q0111.messages(ns["MAX_WAIT"])
    first = "" if not r["errors"] else "cycle {}: {}".format(r["errors"][0][0], msg[r["errors"][0][1]](r["errors"][0][2]))
    item = f"{name}.expected[i].data" if sb else f"{name}.expected[i]"
    want = " ".join(str(d) for d in r["left"])
    conds = [f"{name}.errors != {len(r['errors'])}", f'{name}.first != "{first}"',
             f"{name}.n_in != {r['n_in']}", f"{name}.n_out != {r['n_out']}", f'left != "{want}"']
    if bp:
        conds.append(f"{name}.stalls != {r['stalls']}")
    if sva:
        conds.append(f"{name}.holds != {r['holds']}")
    return (f"    left = \"\"; foreach ({name}.expected[i]) left = {{left, left == \"\" ? \"\" : \" \", $sformatf(\"%0d\", {item})}};\n"
            f"    if ({' || '.join(conds)}) begin\n"
            f"      bad++;\n"
            f"      $display(\"MISMATCH {name}: %0d errors, first [%s], %0d in, %0d out, left [%s]\", "
            f"{name}.errors, {name}.first, {name}.n_in, {name}.n_out, left);\n"
            f"    end\n")


def source() -> str:
    ns = load_python(111)
    dut, bench = sv("!full_q || out_ready_q;"), sv("module slice_tb")
    fixed_dut = sv("!full_q || out_ready;").replace("module reg_slice #(", "module reg_slice_fixed #(", 1)
    fixes = {title_of(b): b for b in (sv("c_stall: cover property"), sv("c_hold: cover property"), sv("localparam int MAX_WAIT"))}
    assert sorted(fixes) == ["coverage", "handshake rule", "scoreboard"], sorted(fixes)
    combos = [(bp, sva, sb, fx) for bp in (0, 1) for sva in (0, 1) for sb in (0, 1) for fx in (0, 1)]
    out = ["// Generated by tests/0111/matrix.py from the page's code: do not edit (test_0111_tb.py checks it).",
           "//@flags --assert --timing --coverage-user", "",
           "// ---- the statement's DUT", dut,
           "// ---- part d's DUT, renamed", fixed_dut]
    for c in combos:
        out += [f"// ---- testbench {code_of(*c)}: backpressure {c[0]}, assertion fixed {c[1]}, "
                f"scoreboard fixed {c[2]}, DUT fixed {c[3]}", bench_variant(bench, fixes, *c)]
    out.append("module tb;")
    names = []
    for c in combos:
        mod = "slice_tb" if code_of(*c) == "0000" else f"slice_tb_{code_of(*c)}"
        for seed in SEEDS:
            name = f"u_{code_of(*c)}_{seed}"
            names.append((name, seed, c))
            out.append(f"  {mod} #(.SEED({seed})) {name} ();")
    out += ["", "  int    bad = 0;", "  string left;", "  final begin"]
    out += [expected_checks(ns, name, seed, *c).rstrip("\n") for name, seed, c in names]
    out += [f'    if (bad == 0) $display("PASS: {len(names)} runs ({len(combos)} combinations x {len(SEEDS)} seeds) '
            f'agree with the page\'s Python model");',
            '    else $display("FAIL: %0d runs differ from the Python model", bad);',
            "  end", "endmodule", ""]
    return "\n".join(out)


if __name__ == "__main__":
    (HERE / "tb.sv").write_text(source(), encoding="utf-8")
    print(f"wrote {HERE / 'tb.sv'}")
