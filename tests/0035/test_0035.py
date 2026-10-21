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
