"""Question 0111: tests of the page's Python code (it runs as published); the same model
runs under Verilator in tb.sv (16 combinations of the fixes) and under Node in the box."""

from extract_code import load_python, pick

NS = load_python(111)


def test_lfsr_is_the_bench_shift_and_has_full_period():
    step = NS["lfsr_step"]
    s, seen = 1, set()
    while s not in seen:
        seen.add(s)
        s = step(s)
    assert len(seen) == 65535 and 0 not in seen          # x^16 + x^14 + x^13 + x^11 + 1 is maximal
    # the bench's {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]}
    for x in (0xACE1, 187, 0x8000, 0x2C00):
        bit = (x >> 15 ^ x >> 13 ^ x >> 12 ^ x >> 10) & 1
        assert step(x) == ((x & 0x7FFF) << 1) | bit
    assert "lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]" in pick(111, "systemverilog", "module slice_tb")


def test_fixed_bench_and_dut_pass_and_every_item_comes_out():
    for seed in range(1, 3000):
        r = NS["run_bench"](seed, 1, 1, 1, 1)
        if r["stalls"]:
            assert r["errors"] == [] and r["n_in"] == r["n_out"] and r["left"] == [], seed
        else:   # no stall at all in this seed: the coverage goals fail, as they should
            assert [w for _, w, _ in r["errors"]] == ["c_stall", "c_hold"], seed


def test_broken_dut_loses_exactly_the_items_left():
    for seed in range(1, 3000):
        r = NS["run_bench"](seed, 1, 1, 1, 0)
        lost = [w["out_data"] for w in r["rows"]
                if w["out_valid"] and not w["out_ready"] and w["in_valid"] and w["in_ready"]]
        assert r["left"] == lost and r["n_in"] - r["n_out"] == len(lost), seed
        # a_hold reports each overwritten item, at the edge after it was overwritten
        assert [d for _, who, d in r["errors"] if who == "a_hold"] == lost, seed


def test_testbench_bugs_hide_the_dut_bug():
    for seed in range(1, 3000):
        asis = NS["run_bench"](seed, 0, 0, 0, 0)
        assert asis["errors"] == [] and asis["n_in"] == asis["n_out"]          # no backpressure: nothing to see
        bp = NS["run_bench"](seed, 1, 0, 0, 0)                                   # the checkers stay silent;
        assert bp["errors"] == ([] if bp["stalls"] else [(40, "c_stall", 0)]), seed   # only the new goal speaks
