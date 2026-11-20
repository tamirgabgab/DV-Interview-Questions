"""Question 0111: tb.sv (the Verilator run of the page's DUT and testbench in all 16
combinations of the fixes) is what tests/0111/matrix.py writes from the current page, so
the simulation checks the code and the Python model as published."""

import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tests" / "0111"))
import matrix  # noqa: E402


def test_tb_is_generated_from_the_page():
    current = (ROOT / "tests" / "0111" / "tb.sv").read_text(encoding="utf-8")
    assert current == matrix.source(), "tests/0111/tb.sv is out of date: run python tests/0111/matrix.py"


def test_the_matrix_keeps_the_statement_as_published():
    src = matrix.source()
    # combination 0000 is the statement's code verbatim, under its own names
    assert matrix.sv("module slice_tb") in src and matrix.sv("!full_q || out_ready_q;") in src
    assert src.count("module slice_tb #(") == 1 and src.count("module slice_tb_") == 15
    assert src.count("module reg_slice #(") == 1 and src.count("module reg_slice_fixed #(") == 1
    # every fix block went in where it belongs, 8 times each
    for marker in ("c_stall: cover property", "c_hold: cover property", "localparam int MAX_WAIT", "reg_slice_fixed dut (.*);"):
        assert src.count(marker) == 8, marker
    assert src.count("disable iff (rst_n)") == 8 and src.count("BACKPRESSURE = 1,") == 8
    assert len(matrix.SEEDS) * 16 == src.count(" #(.SEED(")
