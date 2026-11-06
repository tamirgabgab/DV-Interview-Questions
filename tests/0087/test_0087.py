"""Question 0087: Lights Out.

The page's press_masks, gauss and solve_lights against a brute force over every press set
of the small boards and against the rank on random boards; light chasing (chase,
solve_by_chasing) against the elimination; the quiet patterns, the parity test and the
chasing table of 5 x 5; the diagonals (king_quiet, the period of P's determinant, 2n - 1);
the polynomial criterion (plus_nullity) against the rank up to 40 and the bad sizes; the
all-lit board; the traps and the follow-ups (the torus, rectangles, sizes that imply
sizes, the fewest presses); the page's numbers, the generated blocks, and the box's models
under Node against the Python reference."""

import itertools
import json
import random
import sys
from fractions import Fraction

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))

import q0087 as q  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "senior" / "0087-lights-out.md").read_text(encoding="utf-8")
ns = load_python(87)
press_masks, gauss, solve_lights = ns["press_masks"], ns["gauss"], ns["solve_lights"]
chase, solve_by_chasing = ns["chase"], ns["solve_by_chasing"]
path_kernel, king_quiet = ns["path_kernel"], ns["king_quiet"]
path_poly, poly_mod, plus_nullity = ns["path_poly"], ns["poly_mod"], ns["plus_nullity"]


def weight(v: int) -> int:
    return bin(v).count("1")


def test_masks_and_brute_force():
    for n in range(1, 9):
        for diag in (False, True):
            assert press_masks(n, diag) == q.masks(n, diag)
    m = press_masks(3)
    assert [weight(m[k]) for k in (4, 1, 0)] == [5, 4, 3]          # interior, edge, corner
    for n, diag in [(1, False), (2, False), (3, False), (2, True), (3, True)]:
        N = n * n
        sols = {}
        for x in range(1 << N):
            sols.setdefault(q.apply(n, 0, x, diag), []).append(x)
        for lit in range(1 << N):
            x, free = solve_lights(n, lit, diag)
            want = sols.get(lit, [])
            assert (x is None) == (not want)
            if want:
                assert x in want and 2 ** free == len(want)


def test_random_boards_and_chasing():
    rng = random.Random(870)
    for n in range(1, 9):
        for diag in (False, True):
            f = q.free(n, diag)
            for _ in range(40):
                lit = rng.getrandbits(n * n)
                x, free = solve_lights(n, lit, diag)
                assert free == f
                if x is not None:
                    assert q.apply(n, lit, x, diag) == 0
                else:
                    assert q.solve(n, lit, diag) is None
                if not diag:
                    y = solve_by_chasing(n, lit)
                    assert (y is None) == (x is None)
                    if y is not None:
                        assert q.apply(n, lit, y) == 0
    # gauss on a tiny system: x0 ^ x1 = 1, x1 = 1 → x0 = 0; x0 = 0 and x0 = 1 → none
    assert gauss([0b111, 0b110], 2) == (0b10, 0)
    assert gauss([0b001 | 0, 0b101], 2)[0] is None


def test_part_a():
    x, free = solve_lights(3, 0b111)
    assert free == 0 and [k for k in range(9) if x >> k & 1] == [3, 4, 5, 7]
    assert "הלחיצות 3, 4, 5 ו-7" in PAGE and "דולקת רק השורה העליונה" in PAGE
    assert q.rank(3) == 9


def test_part_b():
    assert q.free(6) == 0 and q.free(5) == 2 and q.rank(5) == 23 and q.rank(6) == 36
    ks = q.kernel(5)
    show = sorted(q.bits(k, 25) for k in ks)
    assert show == sorted(["0111010101110111010101110", "1010110101000001010110101", "1101100000110110000011011"])
    assert ks[0] ^ ks[1] == ks[2] or ks[0] ^ ks[2] == ks[1]
    # the parity test: a board can be solved iff it has an even number of lit lights in each
    rng = random.Random(5)
    for _ in range(300):
        lit = rng.getrandbits(25)
        ok = all(weight(lit & k) % 2 == 0 for k in ks)
        assert ok == (solve_lights(5, lit)[0] is not None)
    # the chasing table of 5 x 5 (column 0 on the left), as the page's code finds it
    tab = q.chase_table(5)
    assert len(tab) == 8 and all(len(v) == 4 for v in tab.values())
    want = {"00000": "00000", "00111": "00010", "01010": "01001", "01101": "10000",
            "10001": "00011", "10110": "00001", "11011": "00100", "11100": "01000"}
    assert {q.bits(r, 5): q.bits(v[0], 5) for r, v in tab.items()} == want
    zero = 0
    for rest, firsts in tab.items():
        for f in firsts:
            assert chase(5, zero, f)[1] == rest
    # the table of sizes
    assert [q.free(n) for n in range(3, 8)] == [0, 4, 2, 0, 0]
    assert "רק 8 מתוך 32 השורות התחתונות" in PAGE


def test_part_c():
    # the determinant of P over GF(2): period 3, zero when n % 3 == 2
    def det_p(n):
        d = [1, 1]
        for _ in range(n - 1):
            d.append(d[-1] ^ d[-2])
        return d[n]
    for n in range(1, 30):
        P = [sum(1 << j for j in range(n) if abs(i - j) <= 1) for i in range(n)]
        rows, piv = q.rref(P, n)
        assert (len(piv) == n) == (det_p(n) == 1) == (n % 3 != 2)
        u = path_kernel(n)
        if u is not None:
            assert len(piv) == n - 1 and all(weight(P[i] & u) % 2 == 0 for i in range(n))
            assert q.bits(u, 5 if n == 5 else n)[:5] == "11011"[: min(5, n)]
    for n in range(1, 15):
        pats = king_quiet(n)
        f = q.free(n, True)
        assert f == (2 * n - 1 if n % 3 == 2 else 0) == len(pats)
        assert len(q.rref(pats, n * n)[1]) == len(pats)          # independent
        assert all(q.apply(n, 0, v, True) == 0 for v in pats)     # quiet
    assert q.free(5, True) == 9
    assert q.solve(5, 1, True) is None                             # the corner of the box


def test_part_d():
    assert [path_poly(k) for k in range(5)] == [1, 0b10, 0b101, 0b1000, 0b10101]
    assert poly_mod(0b10101, 0b111) == 0                           # x^4 + x^2 + 1 = (x^2 + x + 1)^2
    for n in range(1, 41):
        assert plus_nullity(n) == q.free(n) == q.gcd_degree(n)
    bad = [n for n in range(1, 21) if q.free(n)]
    assert bad == [4, 5, 9, 11, 14, 16, 17, 19]
    assert "4, 5, 9, 11, 14, 16, 17 ו-19" in PAGE
    # the all-lit board can always be solved, with or without the diagonals
    for n in range(1, 21):
        for diag in (False, True):
            assert solve_lights(n, (1 << n * n) - 1, diag)[0] is not None
    assert weight(q.solve(5, (1 << 25) - 1)) == 15 and "ב-15 לחיצות לפחות" in PAGE


def rank_q(rows_bits, N):
    M = [[Fraction(r >> i & 1) for i in range(N)] for r in rows_bits]
    r = 0
    for c in range(N):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def test_traps():
    lit = 0b111
    for k in (0, 1, 2):
        lit ^= press_masks(3)[k]
    assert weight(lit) == 5
    assert rank_q(q.masks(4), 16) == 14 and q.rank(4) == 12


def torus_free(n):
    masks = []
    for r in range(n):
        for c in range(n):
            v = 0
            for dr, dc in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                v |= 1 << (((r + dr) % n) * n + (c + dc) % n)
            masks.append(v)
    return n * n - len(q.rref(masks, n * n)[1])


def rect_free(m, n):
    masks = []
    for r in range(m):
        for c in range(n):
            v = 0
            for dr, dc in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= r + dr < m and 0 <= c + dc < n:
                    v |= 1 << ((r + dr) * n + c + dc)
            masks.append(v)
    return m * n - len(q.rref(masks, m * n)[1])


def test_follow_ups():
    assert [torus_free(n) for n in range(3, 9)] == [4, 0, 8, 8, 0, 0]
    for m in range(1, 11):
        for n in range(1, 11):
            g = q.pgcd(q.path_poly(m), q.shift1(q.path_poly(n)))
            assert rect_free(m, n) == g.bit_length() - 1
    assert rect_free(2, 3) == 2 and rect_free(3, 4) == 0
    # sizes that imply sizes: p_m divides p_n when m + 1 divides n + 1
    for m in range(1, 40):
        for n in range(m, 120):
            if (n + 1) % (m + 1) == 0:
                assert q.pgcd(q.path_poly(n), q.path_poly(m)) == q.path_poly(m)
                if q.free(m):
                    assert q.gcd_degree(n) > 0
    assert all(q.free(n) for n in (9, 14, 19, 24, 11, 17, 23))
    assert len([x for x in q.kernel(5)]) + 1 == 4


def test_page_boxes():
    for s in ['data-kind="lightsout" data-mode="play" data-n="3" data-diag="0" data-lit="7"',
              'data-kind="lightsout" data-mode="chase" data-n="5" data-lit="1ffffff"',
              'data-kind="lightsout" data-mode="play" data-n="5" data-diag="1" data-lit="1"']:
        assert s in PAGE, s


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(87)


def to_list(v, N):
    return [v >> k & 1 for k in range(N)]


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(871)
    cases = []
    for n in range(3, 8):
        for diag in (False, True):
            for lit in [0, (1 << n * n) - 1, 1, 0b111] + [rng.getrandbits(n * n) for _ in range(6)]:
                cases.append((n, diag, lit))
    js = [[n, diag, to_list(lit, n * n)] for n, diag, lit in cases]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(js)}.map(([n, d, lit]) => [m.loSolve(n, d, lit), d ? null : m.loChaseSteps(n, lit), m.loHex(lit), m.loUnhex(m.loHex(lit), n * n)])));")
    for (n, diag, lit), (sol, steps, hx, back) in zip(cases, got):
        N = n * n
        assert back == to_list(lit, N) and int(hx, 16) == lit
        ref = q.solve(n, lit, diag)
        assert sol["free"] == q.free(n, diag)
        if ref is None:
            assert sol["press"] is None and sol["quiet"] is not None
            quiet = sum(b << k for k, b in enumerate(sol["quiet"]))
            assert q.apply(n, 0, quiet, diag) == 0 and weight(quiet & lit) % 2 == 1
        else:
            press = sum(b << k for k, b in enumerate(sol["press"]))
            assert q.apply(n, lit, press, diag) == 0 and weight(press) == weight(ref)
            assert sol["count"] == 2 ** q.free(n, diag)
        if steps is not None:
            last = steps[-1] if steps else None
            if ref is None:
                assert last and last["phase"] == "rest" and last["first"] is None
            elif lit:
                assert last["phase"] == "done" and not any(last["lit"])
                press = sum(b << k for k, b in enumerate(last["press"]))
                assert q.apply(n, lit, press) == 0
                rest = [s for s in steps if s["phase"] in ("rest", "done")][0]
                r = sum(b << c for c, b in enumerate(rest["rest"]))
                if r:
                    f = sum(b << c for c, b in enumerate(rest["first"]))
                    assert f == q.chase_table(n)[r][0]
                # every press of a chase clears the light above it
                for s in steps:
                    if s["phase"] in ("chase1", "chase2"):
                        assert s["lit"][s["row"] * n + s["k"] % n] == 0
    assert node_json(f"const m = {explorer_require()};console.log(JSON.stringify(['1ffffff', 'zz', '2000000', ''].map((t) => m.loUnhex(t, 25))));")[1:] == [None, None, None]
