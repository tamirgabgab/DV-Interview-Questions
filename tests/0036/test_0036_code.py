"""Question 0036: the page's Python code (lfsr_next and lfsr_period, as published) against
the generator on every 4-bit mask and seed, the zero fixed point, and a maximal 8-bit
polynomial."""

import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0036  # noqa: E402

ns = load_python(36)
lfsr_next, lfsr_period = ns["lfsr_next"], ns["lfsr_period"]


def test_against_generator():
    for mask in range(1, 16):
        for seed in range(1, 16):
            taps = tuple(4 - i for i in range(4) if (mask >> i) & 1)
            assert lfsr_period(mask, 4, seed) == q0036.period(taps, seed)
            assert lfsr_next(seed, mask, 4) == q0036.step(seed, taps)


def test_page_numbers():
    assert lfsr_period(0b0011, 4) == 15 and lfsr_period(0b0101, 4) == 6 and lfsr_period(0b1001, 4) == 15
    assert lfsr_next(0, 0b0011, 4) == 0
    s, states = 1, []
    for _ in range(15):
        states.append(s)
        s = lfsr_next(s, 0b0011, 4)
    assert s == 1 and sorted(states) == list(range(1, 16))
    assert lfsr_period(0b00011101, 8) == 255          # x^8 + x^6 + x^5 + x^4 + 1
    assert lfsr_period(0b1011, 4, 5) == 2             # a short cycle of a reducible polynomial, seed 0101


def test_explorer_matches_page_code():
    """The LFSR explorer: its step and period against the page's functions on every 4-bit
    mask and seed (the zero fixed point included), its table against the generator, the
    walk of the page's first polynomial, and a maximal 8-bit polynomial."""
    import json

    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const next = [], period = [];
      for (let mask = 1; mask < 16; mask += 2) for (let seed = 0; seed < 16; seed++) {{
        next.push(m.lfsrNext(seed, mask, 4)); period.push(m.lfsrPeriod(mask, 4, seed));
      }}
      console.log(JSON.stringify({{ next, period, table: m.lfsrTable(4), walk: m.lfsrWalk(3, 4, 1), p8b: m.lfsrPeriod(29, 8) }}));""")
    k = 0
    for mask in range(1, 16, 2):
        for seed in range(16):
            assert got["next"][k] == lfsr_next(seed, mask, 4)
            assert got["period"][k] == lfsr_period(mask, 4, seed)
            k += 1
    table = {q0036.mask_of(taps): p for taps, p in q0036.all_polys()}
    assert {r["mask"]: r["period"] for r in got["table"]} == table
    assert [r["poly"] for r in got["table"]][:3] == ["x^4 + 1", "x^4 + x^3 + 1", "x^4 + x^2 + 1"]
    assert got["walk"]["states"] == q0036.sequence((4, 3)) and got["walk"]["period"] == 15 and got["walk"]["back"] == 0
    assert got["p8b"] == lfsr_period(29, 8) == 255          # x^8 + x^6 + x^5 + x^4 + 1
