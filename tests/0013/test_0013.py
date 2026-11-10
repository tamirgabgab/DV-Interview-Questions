from extract_code import load_python

ns = load_python(13)
is_special, find_special = ns["is_special_4"], ns["find_special_4"]


def digits_sorted(x):
    """The four digits of x (with leading zeros), largest first."""
    return sorted([x // 1000, x // 100 % 10, x // 10 % 10, x % 10], reverse=True)


def step(x):
    a, b, c, d = digits_sorted(x)
    return (1000 * a + 100 * b + 10 * c + d) - (1000 * d + 100 * c + 10 * b + a)


def test_page_examples():
    assert step(3524) == 3087 and step(95) == 9441 and step(1000) == 999 and step(7777) == 0
    for x in (3524, 95, 1000, 7777, 9441, 495):
        assert is_special(x) == 0, x
    assert is_special(0) == 1
    assert is_special(6174) == 1


def test_matches_definition():
    for x in range(10000):
        assert is_special(x) == int(step(x) == x), x


def test_final_array():
    assert find_special() == [0, 6174]


def test_proof_steps():
    # Step 1: the difference is 999p + 90q with 0 <= q <= p <= 9 (55 values)
    for x in range(10000):
        a, b, c, d = digits_sorted(x)
        assert step(x) == 999 * (a - d) + 90 * (b - c)
    # Step 3: the digits of the difference from the column subtraction
    for p in range(1, 10):
        for q in range(p + 1):
            expected = [p, q - 1, 9 - q, 10 - p] if q >= 1 else [p - 1, 9, 9, 10 - p]
            assert [int(ch) for ch in f"{999 * p + 90 * q:04d}"] == expected, (p, q)
    # Steps 4-7: among the 55 candidates only 0 (p = 0) and 6174 (p = 6, q = 2) are fixed
    fixed = [(p, q) for p in range(10) for q in range(p + 1)
             if step(999 * p + 90 * q) == 999 * p + 90 * q]
    assert fixed == [(0, 0), (6, 2)]


def test_follow_up_steps():
    # Every number without four equal digits reaches 6174 in at most 7 steps
    counts = [0] * 8
    for x in range(10000):
        if len(set(f"{x:04d}")) == 1:
            continue
        n = 0
        while x != 6174:
            x, n = step(x), n + 1
        counts[n] += 1
    assert counts == [1, 383, 576, 2400, 1272, 1518, 1656, 2184]


def test_sorting_network():
    """Part a's figure and the follow-up on verifying it: the network of the generator is the
    one of the page's SystemVerilog (five comparators, three layers), it sorts every input of
    four digits, by the 0-1 principle its 16 inputs of zeros and ones are enough, and without
    any one comparator some 0/1 input comes out unsorted. The figure's example is 3524."""
    import re
    import sys
    from itertools import product

    from extract_code import ROOT, question_path

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0013

    flat = [c for layer in q0013.NETWORK for c in layer]
    sv = re.findall(r"if \((\w) < (\w)\) \{\1, \2\} = \{\2, \1\};", question_path(13).read_text(encoding="utf-8").split("function automatic bit is_special_4")[1].split("endfunction")[0])
    assert [("abcd".index(u), "abcd".index(v)) for u, v in sv] == flat and len(flat) == 5 and len(q0013.NETWORK) == 3
    for layer in q0013.NETWORK:                              # a layer's comparators share no wire
        assert len({w for c in layer for w in c}) == 2 * len(layer)

    def run(values, net):
        v = list(values)
        for i, j in net:
            if v[i] < v[j]:
                v[i], v[j] = v[j], v[i]
        return v

    bits = list(product((0, 1), repeat=4))
    assert len(bits) == 16 and all(run(v, flat) == sorted(v, reverse=True) for v in bits)
    assert all(run(v, flat) == sorted(v, reverse=True) for v in product(range(10), repeat=4))
    for k in range(5):
        assert any(run(v, flat[:k] + flat[k + 1:]) != sorted(v, reverse=True) for v in bits), k
    states, swapped = q0013.run_network([3, 5, 2, 4])
    assert states == [[3, 5, 2, 4], [5, 3, 4, 2], [5, 3, 4, 2], [5, 4, 3, 2]] and swapped == [True, True, False, False, True]
    import math
    assert math.factorial(4) == 24 > 2 ** 4                  # four comparisons cannot tell 24 orders apart


def test_hardware_follow_up():
    """The BCD digits of the difference straight from p and q, for every number: (p, q - 1,
    9 - q, 10 - p), (p - 1, 9, 9, 10 - p) when q = 0, and 0000 when p = 0."""
    for x in range(10000):
        a, b, c, d = digits_sorted(x)
        p, q = a - d, b - c
        want = [0, 0, 0, 0] if p == 0 else [p, q - 1, 9 - q, 10 - p] if q else [p - 1, 9, 9, 10 - p]
        assert [int(ch) for ch in f"{step(x):04d}"] == want, x


def test_box_tasks():
    """The numbers of the "try it" lists under the boxes of part b."""
    assert step(3524) == step(6543) == step(9876) == 3087
    assert [digits_sorted(x)[0] - digits_sorted(x)[3] for x in (3524, 6543, 9876)] == [3, 3, 3]
    assert [digits_sorted(x)[1] - digits_sorted(x)[2] for x in (3524, 6543, 9876)] == [1, 1, 1]
    chain = [9441]                                           # the pair (9, 5): six steps to 6174
    while chain[-1] != 6174:
        chain.append(step(chain[-1]))
    assert chain == [9441, 7992, 7173, 6354, 3087, 8352, 6174]
    lengths = {}
    for p in range(1, 10):
        for q in range(p + 1):
            x, n = 999 * p + 90 * q, 0
            while x != 6174:
                x, n = step(x), n + 1
            lengths[p, q] = n
    assert max(lengths.values()) == 6 == lengths[9, 5]
    assert sorted(999 * p + 90 * q for (p, q), n in lengths.items() if n == 1) == [4176, 8352, 8532]
    assert f"{step(1000):04d}" == "0999"


def test_explorer_matches_page_code():
    """The Kaprekar explorer with four digits: its step against is_special_4 and the
    test's own step() on every number, every chain ending at 6174 (or 0) within 7 steps."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const chains = Array.from({{length: 10000}}, (_, x) => m.kapChain(x, 4));
      console.log(JSON.stringify({{
        special: chains.map((c) => c.steps[0].special), ends: chains.map((c) => [c.end, c.length, c.fixed]),
        diff: chains.map((c) => c.steps[0].diff), hist: m.kapHistogram(4),
      }}));""")
    for x in range(10000):
        assert got["special"][x] == bool(is_special(x)) and got["diff"][x] == step(x)
        end, length, fixed = got["ends"][x]
        assert fixed and length <= 7
        assert end == (0 if len(set(f"{x:04d}")) == 1 else 6174), x
    assert got["hist"]["ends"] == {"0": 10, "6174": 9990}
    assert sum(got["hist"]["hist"]["6174"]) == 9990 and len(got["hist"]["hist"]["6174"]) == 8
    # the box's bars are the numbers that reach 6174: the follow-up's table, not 392 and 2
    assert got["hist"]["hist"]["6174"] == [1, 383, 576, 2400, 1272, 1518, 1656, 2184]
    assert [v or 0 for v in got["hist"]["hist"]["0"]] == [1, 9]


# --- the bonus: four digits in base B ---------------------------------------------------------

import sys  # noqa: E402

from extract_code import ROOT  # noqa: E402

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0013  # noqa: E402

step_b, fixed_b, orbit_b = ns["kaprekar4_step_b"], ns["kaprekar4_fixed_b"], ns["kaprekar4_orbit_b"]


def test_base_b_page_numbers():
    assert step_b(6174, 10) == 6174 and fixed_b(10) == [6174]
    assert fixed_b(2) == [7, 9] and fixed_b(4) == [201] and fixed_b(5) == [392] and fixed_b(15) == [30996]
    assert [fixed_b(B) for B in (3, 6, 7, 8, 9, 11, 12, 13, 14, 16)] == [[]] * 10
    assert [q0013.text_b(x, 2) for x in fixed_b(2)] == ["0111", "1001"] and q0013.text_b(201, 4) == "3021"
    assert [q0013.text_b(fixed_b(B)[-1], B) for B in (5, 10, 15, 20, 25, 30, 35)] == ["3032", "6174", "92B6", "C3F8", "F4JA", "I5NC", "L6RE"]
    assert [fixed_b(B)[-1] for B in (40, 45, 50)] == [1548456, 2478168, 3774470]
    for k in range(1, 20):
        B = 5 * k
        x = fixed_b(B)[-1]
        assert q0013.digits_b(x, B) == [3 * k, k - 1, 4 * k - 1, 2 * k]
        assert x == k * (5 * k - 1) * (75 * k * k + 20 * k + 3) == 375 * k ** 4 + 25 * k ** 3 - 5 * k * k - 3 * k
        assert x == q0013.value_b(3 * k, k, B)
    values, start = orbit_b(q0013.EXAMPLE_X, 15)
    assert [q0013.text_b(v, 15) for v in values] == ["1234", "30DC", "D852", "B2B4", "9676"] and start == 1
    assert q0013.pair_b(values[-1], 15) == (3, 1) == q0013.pair_b(q0013.EXAMPLE_X, 15)      # 9676 has the pair of 1234
    att15 = q0013.attractors_b(15)
    assert [(len(c), n) for c, n in att15] == [(4, 10052), (4, 9640), (4, 9538), (4, 9490), (2, 5170), (2, 4560), (1, 2160), (1, 15)]
    assert round(100 * 2160 / (15 ** 4 - 15), 1) == 4.3                       # the trap's "about 4 %"
    # numbers with four equal digits go to 0, a cycle of length 1, also in a base without a fixed point
    assert orbit_b(40, 3) == ([40, 0], 1) and orbit_b(0, 3) == ([0], 0) and orbit_b(7777, 10) == ([7777, 0], 1)
    # the "try it" list of the base box
    assert [q0013.text_b(v, 15) for v in orbit_b(int("62B9", 15), 15)[0]] == ["62B9", "92B6"]
    assert [q0013.text_b(v, 10) for v in orbit_b(1234, 10)[0]] == ["1234", "3087", "8352", "6174"]
    assert step_b(201, 4) == 201 and [(len(c), n) for c, n in q0013.attractors_b(4)] == [(2, 168), (1, 84), (1, 4)]
    assert len(orbit_b(3 * 6 + 3, 6)[0]) == 10 == max(len(orbit_b(x, 6)[0]) for x in range(6 ** 4))


def test_base_b_longest_orbit():
    """The cost paragraph: in the bases 2 to 16 the longest orbit has 13 values (0036 in base
    12), far under the bound B(B + 1) / 2; without a fixed point every number with two
    different digits ends in a cycle longer than 1."""
    longest = {B: max(len(orbit_b(x, B)[0]) for x in range(B ** 4)) for B in range(2, 17)}
    assert max(longest.values()) == 13 == longest[12] == len(orbit_b(3 * 12 + 6, 12)[0])
    assert all(longest[B] <= B * (B + 1) // 2 for B in longest)
    for B in (3, 6, 7, 8, 9, 11):
        for x in range(B ** 4):
            values, start = orbit_b(x, B)
            assert (len(values) - start == 1) == (len(set(q0013.digits_b(x, B))) == 1), (B, x)


def test_base_b_digit_forms():
    """The difference is p(B^3 - 1) + q(B^2 - B), with the digits of the proof, in every base."""
    for B in range(2, 17):
        for x in range(B ** 4):
            p, q = q0013.pair_b(x, B)
            y = step_b(x, B)
            assert y == q0013.step_b(x, B) == q0013.value_b(p, q, B)
            if p:
                want = [p - 1, B - 1, B - 1, B - p] if q == 0 else [p, q - 1, B - q - 1, B - p]
                assert q0013.digits_b(y, B) == want, (B, x)


def test_base_b_theorem_exhaustively():
    """Every fixed point with two different digits is the value of a pair (p, q), so a search
    over the pairs finds them all: bases 2 to 60. Bases 2 to 12 also run every number."""
    for B in range(2, 61):
        found = sorted(v for p in range(1, B) for q in range(p + 1) if step_b(v := q0013.value_b(p, q, B), B) == v)
        assert found == fixed_b(B) == q0013.fixed_b(B), B
    for B in range(2, 13):
        assert [x for x in range(B ** 4) if step_b(x, B) == x and len(set(q0013.digits_b(x, B))) > 1] == fixed_b(B)
    # existence is not convergence: bases 5 and 10 converge, 15 mostly does not
    for B in (5, 10):
        assert all(orbit_b(x, B)[0][orbit_b(x, B)[1]] in fixed_b(B) + [0] for x in range(B ** 4))


def test_base_b_tables_and_figures():
    th = q0013.theorem_table().splitlines()[2:]
    assert len(th) == 4 and "0111 ו-1001" in th[0] and "3021" in th[1]
    fam = q0013.family_table().splitlines()[2:]
    assert len(fam) == 10 and "**6174**" in fam[1] and "**92B6**" in fam[2] and fam[9].endswith("| ‏3,774,470 |")
    ex = q0013.example_table().splitlines()[2:]
    assert len(ex) == 5 and "**30DC**" in ex[0] and "‏<span dir='ltr'>(3, 1)</span>" in ex[4]
    att = q0013.attractor_table().splitlines()[2:]
    assert len(att) == 15 and "‏6174" in att[8] and att[8].endswith("| ‏9,990 מתוך 9,990 |") and "‏2,160 מתוך 50,610" in att[13]
    from page_tests import assert_figures_match

    assert_figures_match(13)


def test_base_b_explorer_matches_page_code():
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (let B = 2; B <= 16; B++) {{
        const steps = [];
        for (let x = 0; x < B ** 4; x += (B > 10 ? 7 : 1)) {{ const s = m.k4Step(x, B), o = m.k4Orbit(x, B); steps.push([x, s.diff, s.p, s.q, s.digitsF, s.pNext, s.qNext, o.values, o.start]); }}
        out[B] = {{ fixed: m.k4Fixed(B), att: m.k4Attractors(B).map((a) => [a.cycle, a.count]), steps,
                    parse: [m.k4Parse("1234", B), m.k4Parse("12345", B), m.k4Parse("00G0", B)] }};
      }}
      console.log(JSON.stringify(out));""")
    for B in range(2, 17):
        r = got[str(B)]
        assert r["fixed"] == fixed_b(B)
        assert r["parse"] == [((1 * B + 2) * B + 3) * B + 4 if B >= 5 else None, None, None]
        assert sorted((tuple(c), n) for c, n in r["att"]) == sorted((tuple(c), n) for c, n in q0013.attractors_b(B)), B
        for x, diff, p, q, digits_f, p_next, q_next, values, start in r["steps"]:
            assert diff == step_b(x, B) and (p, q) == q0013.pair_b(x, B)
            assert digits_f == (q0013.digits_b(diff, B) if p else [0, 0, 0, 0])
            assert (p_next, q_next) == q0013.pair_b(diff, B)
            assert (values, start) == orbit_b(x, B)


def test_explorer_column_subtraction():
    """The box's column subtraction: for every four-digit number, the columns of largest
    minus smallest give the difference digit by digit with the borrows of the page's
    table (units and tens always, hundreds only when q = 0, thousands never)."""
    from page_tests import explorer_require, node_json

    xs = list(range(0, 10000, 7)) + [95, 3524, 1000, 6174]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({xs}.map((x) => {{ const s = m.kapStep(x, 4); return [s.diff, m.kapColumns(s.largest, s.smallest, 4)]; }})));")
    for x, (diff, cols) in zip(xs, got):
        ds = sorted(f"{x:04d}", reverse=True)
        a, b, c, d = map(int, ds)
        p, q = a - d, b - c
        assert int("".join(str(col["digit"]) for col in cols)) == diff
        if p == 0:
            assert not any(col["borrowOut"] for col in cols)
            continue
        assert [col["borrowOut"] for col in cols] == [0, int(q == 0), 1, 1], x
        want = [p, q - 1, 9 - q, 10 - p] if q >= 1 else [p - 1, 9, 9, 10 - p]
        assert [col["digit"] for col in cols] == want, x


def test_explorer_pairs_box():
    """The pairs box of part b: for each of the 54 pairs, the difference, its digits by
    step 3, the next pair (the pair of the difference), conditions a and b (both only at
    (6, 2)), the cases of step 6 that hold, and the path that ends at 6174."""
    from page_tests import explorer_require, node_json

    pairs = [(p, q) for p in range(1, 10) for q in range(p + 1)]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({[list(t) for t in pairs]}.map(([p, q]) => [m.kapPair(p, q), m.kapPairPath(p, q)])));")
    cases = {("P", "Q1"): 1, ("P", "N"): 2, ("P", "T"): 3, ("N", "Q1"): 4, ("N", "T"): 5, ("T", "Q1"): 6, ("T", "N"): 7}
    for (p, q), (r, path) in zip(pairs, got):
        v = 999 * p + 90 * q
        assert r["value"] == v
        assert r["digits"] == [int(ch) for ch in f"{v:04d}"]
        a, b, c, d = digits_sorted(v)
        assert r["next"] == [a - d, b - c]
        assert step(v) == 999 * (a - d) + 90 * (b - c)
        assert (r["condA"] and r["condB"]) == ((p, q) == (6, 2))
        if q == 0:
            assert r["cases"] == []
        else:
            ex = {"P": p, "Q1": q - 1, "N": 9 - q, "T": 10 - p}
            want = sorted({n for (t, s), n in cases.items() if ex[t] == a and ex[s] == d})
            assert r["cases"] == want, (p, q)
        assert path[0] == [p, q] and path[-1] == [6, 2] and len(path) <= 8
        x = v
        for np_, nq in path[1:]:
            x = step(x)
            assert x == 999 * np_ + 90 * nq
