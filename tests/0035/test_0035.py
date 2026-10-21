"""Question 0035: the page's half-cycle model (div3_50, as published): after the counter
settles the output has a period of six half-cycles, three of them high, starting at a
rising edge; and the first pulse comes after one full count."""

from extract_code import load_python

ns = load_python(35)
div3_50 = ns["div3_50"]


def test_steady_state_period_and_duty():
    out = div3_50(6 * 40)
    steady = out[4:]                        # from the first rise: the third rising edge
    n = len(steady) // 6 * 6                # whole periods only
    for i in range(0, n, 6):
        assert steady[i:i + 6] == [1, 1, 1, 0, 0, 0], i
    assert sum(steady[:n]) * 2 == n         # 50% duty


def test_transitions_only_on_edges_and_startup():
    out = div3_50(30)
    assert out[:6] == [0, 0, 0, 0, 1, 1]    # a rises at the third rising edge (edge index 4)
    changes = [i for i in range(1, len(out)) if out[i] != out[i - 1]]
    rises = [i for i in changes if out[i] == 1]
    falls = [i for i in changes if out[i] == 0]
    assert all(i % 2 == 0 for i in rises)   # rises on rising edges of clk
    assert all(i % 2 == 1 for i in falls)   # falls on falling edges of clk
    assert all(b - a == 6 for a, b in zip(rises, rises[1:]))


def test_explorer_matches_page_model():
    """The divide-by-three explorer: its trace is the page's half-cycle model; from state 3
    the page's statements with no counter width never return to 2 (the "wide" variant),
    the module's 2-bit counter wraps to 0, and the guarded counter returns to 0."""
    import json

    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({{ out: m.div3Trace(240).map((r) => r.out), duty: m.div3Duty(m.div3Trace(240)),
        wide: m.div3Trace(24, 3, "wide"), wrap: m.div3Trace(24, 3, "wrap"), guard: m.div3Trace(24, 3, "guard") }}));""")
    assert got["out"] == div3_50(240)
    assert got["duty"]["period"] == 6 and got["duty"]["high"] == 3 and got["duty"]["ok"]

    def replay(cnt, wrap, guard, n):
        # the page's two statements per edge, with the start state and the counter variant
        a = b = 0
        rows = []
        for edge in range(n):
            if edge % 2 == 0:
                a = 1 if cnt == 2 else 0
                if guard:
                    cnt = 0 if cnt >= 2 else cnt + 1
                else:
                    cnt = 0 if cnt == 2 else (cnt + 1) & (3 if wrap else -1)
            else:
                b = a
            rows.append((cnt, a, b, a | b))
        return rows

    for key, wrap, guard in (("wide", False, False), ("wrap", True, False), ("guard", False, True)):
        assert [(r["cnt"], r["a"], r["b"], r["out"]) for r in got[key]] == replay(3, wrap, guard, 24), key
    assert all(r["out"] == 0 for r in got["wide"])             # the Python model from 3: stuck low
    assert [r["out"] for r in got["wrap"]] == [r["out"] for r in got["guard"]]
    assert [r["out"] for r in got["wrap"]][2:] == div3_50(22)  # one cycle late, then the same
