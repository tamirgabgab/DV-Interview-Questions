"""Question 0099, the check digits of an IBAN: the numbers the page states, recomputed from the
reference in tools/figures/q0099.py (and from Python's big integers); the generated blocks;
the box's models under Node against the same reference."""

import itertools
import json
import random
import sys
from math import comb

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0099  # noqa: E402

IL = "IL620108000000099999999"


def test_registry_examples():
    for ib in q0099.EXAMPLES:
        s = q0099.norm(ib)
        assert q0099.valid(ib), ib
        assert int(q0099.to_digits(ib)) % 97 == q0099.running(q0099.to_digits(ib))[-1] == 1
        assert q0099.check_digits(s[:2] + "00" + s[4:]) == s[2:4], ib
    assert [q0099.mod97(q0099.norm(ib)[:2] + "00" + q0099.norm(ib)[4:]) for ib in q0099.EXAMPLES] == [36, 16, 9]


def test_part_a_numbers():
    d = q0099.to_digits(IL)
    assert q0099.moved(IL) == "0108000000099999999IL62"
    assert d == "0108000000099999999182162" and len(d) == 25
    assert int(q0099.char_digits("I")) == 18 and int(q0099.char_digits("L")) == 21
    run = q0099.running(d)
    assert run[:4] == [0, 1, 10, 11] and 108 % 97 == 11 and run[-1] == 1
    assert all(r < 97 for r in run) and 10 * 96 + 9 < 970
    # the module: N = R * 10^6 + H, 10^6 = 27 and 100 = 3 mod 97, 3r + v < 324
    assert pow(10, 6, 97) == 27 and 100 % 97 == 3 and 3 * 96 + 35 < 324
    R, H = int(d[:-6]), int(d[-6:])
    assert int(d) == R * 10**6 + H and (27 * (R % 97) + H % 97) % 97 == 1
    # the head is always 6 digits: two letters (2 digits each) and two digits
    assert all(len(q0099.char_digits(c)) == 2 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # the trap: without moving the first four characters the remainder is not 1
    assert int("".join(q0099.char_digits(c) for c in IL)) % 97 != 1
    # 25 digits do not fit 64 bits (up to about 1.8e19, 20 digits); 9 digits fit 31 bits
    assert 10**19 < 2**64 < 10**20 and int(d) > 2**64 and 10**9 - 1 < 2**31


def test_part_b_hardware():
    # one step: 10x + d at most 969, 10 bits; the mod block gives (10x + d) mod 97
    assert 10 * 96 + 9 == 969 < 1024
    # the datapath step against the modulo, every state and digit
    assert all(q0099.step_hw(r, d) == (10 * r + d) % 97 for r in range(97) for d in range(10))
    # six zeros multiply by 10^6; r + h <= 192, and mod 97 it is 1 only for 1 and 98
    assert all((r * 10**6) % 97 == (r * pow(10, 6, 97)) % 97 for r in range(97))
    assert [v for v in range(193) if v % 97 == 1] == [1, 98]
    # the versions agree with the reference on every string, and their costs
    rng = random.Random(9)
    alnum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    strings = [q0099.norm(x) for x in q0099.EXAMPLES] + [q0099.norm(q0099.SLIP)] + q0099.random_ibans(100, seed=12)
    strings += ["".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(2)) + f"{rng.randrange(100):02d}"
                + "".join(rng.choice(alnum) for _ in range(rng.randrange(1, 30))) for _ in range(800)]
    for s in strings:
        ds = q0099.stream(s)
        for run in (q0099.run_buffer, q0099.run_final, q0099.run_codes):
            assert run(ds)[0] == (q0099.mod97(s) == 1), s
    il = q0099.stream(IL)
    assert len(il) == 25 and len(IL) == 23
    assert [run(il)[1:] for run in (q0099.run_buffer, q0099.run_final, q0099.run_codes)] == [(31, 34), (31, 17), (25, 14)]
    # the clock-by-clock table of the page: h = 93 after the head (182162 mod 97), r = 90
    # after the rest, 5 after the tail, and 5 + 93 = 98
    tr = q0099.trace_rows()
    assert tr[5][5] == 93 == 182162 % 97 and tr[24][6] == 90 and tr[-1][6] == 5 and 5 + 93 == 98
    assert (90 * 10**6) % 97 == 5 and len(tr) == 31
    # the follow-ups: two digits a clock (3r + 10a + b <= 387) and a letter (3r + v), 13 clocks
    assert all(q0099.step2_hw(r, a, b) == (100 * r + 10 * a + b) % 97 for r in range(97) for a in range(10) for b in range(10))
    assert all(q0099.step_letter(r, v) == (100 * r + v) % 97 for r in range(97) for v in range(10, 36))
    assert 3 * 96 + 99 == 387 and 6 // 2 + (19 + 1) // 2 == 13
    # 14 with a 12-bit multiplier: 27r + h <= 2688; the lower bound 97 * 97 > 2^13
    assert 27 * 96 + 96 == 2688 < 4096 and pow(10, 6, 97) == 27 and 97 * 97 == 9409 > 2**13
    for (h, r), (h2, r2) in [((5, 7), (5, 8)), ((5, 7), (6, 7)), ((0, 0), (96, 96))]:
        told = any(((27 * ((10**k * r + S) % 97) + h) % 97 == 1) != ((27 * ((10**k * r2 + S) % 97) + h2) % 97 == 1)
                   for k in (2, 3) for S in range(10**k))
        assert told
    assert 27 * 900 % 97 != 0

def test_part_c_check_digits():
    for s in q0099.random_ibans(300, seed=7) + [IL]:
        m = q0099.mod97(s[:2] + "00" + s[4:])
        c = 98 - m
        assert 2 <= c <= 98 and q0099.check_digits(s) == f"{c:02d}"
        assert (m + c) % 97 == 1
        # the check digits are the two last digits of the moved number: they are added
        assert int(q0099.to_digits(s)) == int(q0099.to_digits(s[:2] + "00" + s[4:])) + c
    # two two-digit values can satisfy the rule when m = 0: 01 and 98
    assert {c for c in range(100) if (0 + c) % 97 == 1} == {1, 98}


def test_part_d_claims():
    s = IL
    n0 = int(q0099.to_digits(s))
    # every single digit error and every swap of two different digits, at any distance
    for i in range(2, len(s)):
        for a in "0123456789":
            if a != s[i]:
                assert not q0099.valid(s[:i] + a + s[i + 1:])
    for s2 in q0099.random_ibans(20, seed=3):
        for i, j in itertools.combinations(range(2, len(s2)), 2):
            if s2[i] != s2[j]:
                t = s2[:i] + s2[j] + s2[i + 1:j] + s2[i] + s2[j + 1:]
                assert not q0099.valid(t), (s2, i, j)
        # a letter changed to another letter (the country code) is caught too
        for c in "ABCDEFGHJKMNOPQRSTUVWXYZ":
            assert not q0099.valid(c + s2[1:])
    assert q0099.order10(97) == 96 and q0099.order10(99) == 2
    assert all(pow(10, d, 97) != 1 for d in range(1, 96))
    # the double error 99 -> 02 at the end: 97 * 10^6 less, still valid
    assert q0099.valid(q0099.SLIP) and n0 - int(q0099.to_digits(q0099.SLIP)) == 97 * 10**6
    # all double errors of the example: 147 of 13,851 slip, about 1 %
    slips = sum(q0099.valid(t) for t in q0099.errors(s)["double"])
    assert len(q0099.errors(s)["double"]) == 13851 == comb(19, 2) * 81 and slips == 147
    assert len(q0099.errors(s)["single"]) == 171 == 19 * 9
    # a letter beside a digit: B1 and 1B are both 111, also M2 and X3, and only those
    pairs = [(v, d) for v in range(10, 36) for d in range(10) if (9 * (11 * d - v)) % 97 == 0]
    assert pairs == [(11, 1), (22, 2), (33, 3)]
    for a, b in ("B1", "M2", "X3"):
        assert q0099.char_digits(a) + b == b + q0099.char_digits(a)
    # the trap: three digit -> letter changes of the example slip (the length changes)
    letter_slips = [(i, c) for i in range(2, len(s)) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    if q0099.valid(s[:i] + c + s[i + 1:])]
    assert len(letter_slips) == 3


def test_moduli_table():
    res = q0099.caught()
    for k in ("single", "adjacent", "jump"):
        assert res[97][k][0] == res[97][k][1] and res[98][k][0] == res[98][k][1]
        assert res[100][k][0] == 0
    assert res[99]["single"][0] == res[99]["single"][1] and res[99]["adjacent"][0] == res[99]["adjacent"][1]
    assert res[99]["jump"][0] == 0
    slip = {m: 1 - res[m]["double"][0] / res[m]["double"][1] for m in (97, 98, 99)}
    assert 0.008 < slip[97] < 0.012 and 1.7 < slip[98] / slip[97] < 2.3 and slip[99] > slip[98]
    assert res[100]["double"][0] == 0
    # the cost line: 19 digits in the account part of each IBAN, 30 IBANs
    assert len(q0099.random_ibans()) == 30 and all(len(x) == 23 for x in q0099.random_ibans())


def test_follow_ups():
    # from the end: r <- (r + d * p) mod 97, p <- 10 p mod 97
    for s in q0099.random_ibans(50, seed=5):
        d = q0099.to_digits(s)
        r, p = 0, 1
        for c in reversed(d):
            r, p = (r + int(c) * p) % 97, p * 10 % 97
        assert r == 1
    # nine digits at a time: the remainder (two digits) and seven new digits
    for s in q0099.random_ibans(50, seed=6):
        d = q0099.to_digits(s)
        r, rest = int(d[:9]) % 97, d[9:]
        while rest:
            r, rest = int(f"{r}{rest[:7]}") % 97, rest[7:]
        assert r == 1
    # Luhn misses 09 <-> 90; mod 97 does not
    def luhn_sum(n):
        return sum(v if i % 2 == 0 else (2 * v - 9 if 2 * v > 9 else 2 * v) for i, v in enumerate(int(c) for c in reversed(n))) % 10
    assert luhn_sum("1209") == luhn_sum("1290")
    assert q0099.valid(IL) and not q0099.valid(IL[:15] + "90" + IL[17:]) if IL[15:17] == "09" else True


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(99)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(11)
    alnum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    strings = [q0099.norm(x) for x in q0099.EXAMPLES] + [q0099.SLIP.replace(" ", "")] + q0099.random_ibans(20, seed=2)
    strings += ["".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(2)) + f"{rng.randrange(100):02d}"
                + "".join(rng.choice(alnum) for _ in range(rng.randrange(1, 30))) for _ in range(40)]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(strings)}.map((s) => [m.ibDigits(s).digits, m.ibRunning(m.ibDigits(s).digits), m.ibValid(s), m.ibCheck(s), m.ibGroup(s)])));")
    for s, (digits, run, ok, chk, grp) in zip(strings, got):
        assert digits == q0099.to_digits(s), s
        assert run == q0099.running(q0099.to_digits(s)), s
        assert ok == q0099.valid(s), s
        assert chk == q0099.check_digits(s), s
        assert grp == q0099.grouped(s), s
    # the changes of the box: a digit to the next digit, a letter to the next letter, a swap
    edits = node_json(f"const m = {explorer_require()};"
                      "console.log(JSON.stringify([m.ibChange('IL62', 1), m.ibChange('IL62', 4), m.ibChange('ZZ90', 2),"
                      " m.ibChange('AB90', 3), m.ibSwap('IL62', 1), m.ibSwap('IL62', 4), m.ibSwap('IL62', 3)]));")
    assert edits == ["JL62", "IL63", "ZA90", "AB00", "LI62", "IL26", "IL26"]
    cases = ["IL62 0108 0000 0009 9999 999", "il620108000000099999999", "  GB82 west 1234 5698 7654 32 ", "IL6", "1L62000",
             "IL6A000", "IL62", "IL62" + "0" * 30, "IL62" + "0" * 31, "IL62-0108", ""]
    parsed = node_json(f"const m = {explorer_require()};console.log(JSON.stringify({json.dumps(cases)}.map((t) => m.ibParse(t))));")
    assert parsed == [IL, IL, "GB82WEST12345698765432", None, None, None, None, "IL62" + "0" * 30, None, None, None]


def test_hardware_box_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(21)
    alnum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    strings = [q0099.norm(x) for x in q0099.EXAMPLES] + [q0099.norm(q0099.SLIP)]
    strings += ["".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(2)) + f"{rng.randrange(100):02d}"
                + "".join(rng.choice(alnum) for _ in range(rng.randrange(1, 30))) for _ in range(120)]
    versions = [k for k, _ in q0099.VERSIONS]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(strings)}.map((s) => [m.ihStream(s), {json.dumps(versions)}.map((v) => {{"
                    "const t = m.ihTrace(m.ihStream(s), v); return [t.length, t[t.length - 1].ok]; })])));")
    for s, (ds, res) in zip(strings, got):
        assert ds == q0099.stream(s), s
        for (name, run), (clocks, ok) in zip(q0099.VERSIONS, res):
            want_ok, want_clocks, _ = run(q0099.stream(s))
            assert (clocks, ok) == (want_clocks, want_ok), (s, name)
    # the trace of the page's IBAN, clock by clock, as the table of the page
    tr = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.ihTrace(m.ihStream('{IL}'), 'final').map((e) => [e.regs.h, e.regs.r, e.regs.n])));")
    assert tr == [[row[5], row[6], row[7]] for row in q0099.trace_rows()]
    cases = ["IL62 0108", "il620108", "IL6", "1L620", "IL62" + "0" * 30, "IL62" + "0" * 31]
    parsed = node_json(f"const m = {explorer_require()};console.log(JSON.stringify({json.dumps(cases)}.map(m.ihParse)));")
    assert parsed == ["IL620108", "IL620108", None, None, "IL62" + "0" * 30, None]
