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


def test_explorer_divide_by_n():
    """The box's follow-up: a divide by N for N = 2..10 against a plain Python model of
    the same statements (a counter modulo N in ceil(log2 N) bits, a high for the last
    floor(N / 2) counts, b half a cycle later, the output a | b for an odd N and
    a for an even N): 50% duty and a period of N cycles from the first rise; the
    unreachable wake-up state is the counter's highest, when it exists."""
    import json
    import math

    from page_tests import explorer_require, node_json

    def model(N, half_cycles, cnt0=0, counter="wrap"):
        bits = max(1, math.ceil(math.log2(N)))
        high = N // 2
        cnt = cnt0
        a = b = 0
        out = []
        for edge in range(half_cycles):
            if edge % 2 == 0:
                a = 1 if N - high <= cnt <= N - 1 else 0
                if counter == "guard":
                    cnt = 0 if cnt >= N - 1 else cnt + 1
                elif counter == "wide":
                    cnt = 0 if cnt == N - 1 else cnt + 1
                else:
                    cnt = 0 if cnt == N - 1 else (cnt + 1) & ((1 << bits) - 1)
            else:
                b = a
            out.append((cnt, a, b, (a | b) if N % 2 else a))
        return out, bits

    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (let N = 2; N <= 10; N++) {{
        const p = m.div3Params(N);
        out[N] = {{ p, rows: m.div3Trace(120, 0, "wrap", N).map((r) => [r.cnt, r.a, r.b, r.out]), duty: m.div3Duty(m.div3Trace(120, 0, "wrap", N)),
          woke: p.wake === null ? null : {{ wrap: m.div3Trace(40, p.wake, "wrap", N).map((r) => r.out), wide: m.div3Trace(40, p.wake, "wide", N).map((r) => r.out), guard: m.div3Trace(40, p.wake, "guard", N).map((r) => r.out) }} }};
      }}
      console.log(JSON.stringify(out));""")
    for N in range(2, 11):
        g = got[str(N)]
        rows, bits = model(N, 120)
        assert [tuple(r) for r in g["rows"]] == rows, N
        assert g["p"]["bits"] == bits and g["p"]["high"] == N // 2
        assert g["p"]["wake"] == ((1 << bits) - 1 if (1 << bits) - 1 >= N else None), N
        assert g["duty"]["period"] == 2 * N and g["duty"]["high"] == N and g["duty"]["ok"], N
        if g["woke"] is not None:
            w = g["p"]["wake"]
            for key in ("wrap", "wide", "guard"):
                assert g["woke"][key] == [r[3] for r in model(N, 40, w, key)[0]], (N, key)
            assert all(v == 0 for v in g["woke"]["wide"]), N           # stuck above N - 1
            assert g["woke"]["wrap"][2 * bits:] == g["woke"]["guard"][2 * bits:] or N == 3, N
    assert [tuple(r) for r in got["3"]["rows"]] == [tuple(r) for r in model(3, 120)[0]]


def test_part_b_odd_n():
    """Part b's div_odd_50: for N = 3 it is part a's div3_50, and for every odd N up to 21,
    after the first rise, every period is 2N half-cycles with N of them high, rises on
    rising edges and falls on falling edges."""
    div_odd_50 = ns["div_odd_50"]
    assert div_odd_50(3, 240) == div3_50(240)
    for N in range(3, 22, 2):
        out = div_odd_50(N, 2 * N * 30)
        first = out.index(1)
        steady = out[first:]
        whole = len(steady) // (2 * N) * (2 * N)
        for i in range(0, whole, 2 * N):
            assert steady[i:i + 2 * N] == [1] * N + [0] * N, (N, i)
        changes = [i for i in range(1, len(out)) if out[i] != out[i - 1]]
        assert all(i % 2 == (0 if out[i] else 1) for i in changes), N


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(35)
