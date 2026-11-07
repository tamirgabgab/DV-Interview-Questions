"""Question 0099: the page's Python code (it runs as published) against the generator's
reference: to_digits, mod97 and is_valid on the registry examples, made-up IBANs and random
strings; check_digits; the hardware checker of part b (step, finish, stream, check_stream)."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0099  # noqa: E402

ns = load_python(99)


def test_examples():
    for ib in q0099.EXAMPLES + (q0099.SLIP,):
        assert ns["is_valid"](ib) and ns["is_valid"](ib.lower())
        assert ns["to_digits"](ib) == q0099.to_digits(ib)
    assert ns["mod97"]("0108") == 11
    assert ns["check_digits"](q0099.IL) == "62" and ns["check_digits"]("GB00 WEST 1234 5698 7654 32") == "82"
    assert ns["check_digits"]("DE89370400440532013000") == "89"


def test_random_strings():
    rng = random.Random(4)
    alnum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for _ in range(2000):
        s = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(2)) + f"{rng.randrange(100):02d}" \
            + "".join(rng.choice(alnum) for _ in range(rng.randrange(1, 30)))
        assert ns["mod97"](ns["to_digits"](s)) == int(q0099.to_digits(s)) % 97
        assert ns["is_valid"](s) == q0099.valid(s)
        assert int(ns["check_digits"](s)) == int(q0099.check_digits(s))
        fixed = s[:2] + ns["check_digits"](s) + s[4:]
        assert ns["is_valid"](fixed)
    for bad in ("", "IL", "I162000", "IL6A0001", "IL62-0108", "IL62 0108 ש", "ÄL620108"):
        assert not ns["is_valid"](bad), bad


def test_hardware_part_b():
    assert all(ns["step"](r, d) == (10 * r + d) % 97 for r in range(97) for d in range(10))
    assert all(ns["finish"](r, h) == (27 * r + h) % 97 for r in range(97) for h in range(97))
    assert ns["stream"]("IL62 0108") == [1, 8, 2, 1, 6, 2, 0, 1, 0, 8]
    for ib in q0099.EXAMPLES + (q0099.SLIP,):
        assert ns["stream"](ib) == q0099.stream(ib) and ns["check_stream"](ns["stream"](ib))
    rng = random.Random(6)
    alnum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for _ in range(1500):
        s = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(2)) + f"{rng.randrange(100):02d}" \
            + "".join(rng.choice(alnum) for _ in range(rng.randrange(1, 30)))
        assert ns["check_stream"](ns["stream"](s)) == (q0099.mod97(s) == 1) == q0099.run_codes(q0099.stream(s))[0]
    # a stream shorter than the head is never valid
    assert not ns["check_stream"]([1, 8, 2, 1, 6])
