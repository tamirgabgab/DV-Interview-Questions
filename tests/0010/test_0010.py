import subprocess
import sys
import re
import itertools
import math
import random

from extract_code import load_python

ns = load_python(10)
brute, fast = ns["isValid_brute"], ns["isValid"]

EXAMPLES = {"": True, "()": True, "()[]{}": True, "{[()]}": True, "([]{})": True,
            "(((())))": True, "(]": False, "([)]": False, "(((": False, "())": False,
            ")(": False, "]": False, "((": False}


def test_page_examples():
    for s, expected in EXAMPLES.items():
        assert brute(s) == expected, s
        assert fast(s) == expected, s


def test_all_short_strings():
    # Both solutions agree on every string up to length 8, and the number of valid strings
    # of length 2k is 3^k * Catalan(k): 1, 3, 18, 135, 1134
    for n in range(9):
        valid = 0
        for chars in itertools.product("()[]{}", repeat=n):
            s = "".join(chars)
            assert brute(s) == fast(s), s
            valid += fast(s)
        k = n // 2
        assert valid == (3 ** k * math.comb(2 * k, k) // (k + 1) if n % 2 == 0 else 0), n


def test_random_long_strings():
    rng = random.Random(10)
    for _ in range(2000):
        # Build a valid string, then maybe break one character
        s, stack = [], []
        for _ in range(rng.randint(0, 60)):
            if stack and rng.random() < 0.5:
                s.append(")]}"["([{".index(stack.pop())])
            else:
                stack.append(rng.choice("([{"))
                s.append(stack[-1])
        s += [")]}"["([{".index(c)] for c in reversed(stack)]
        if s and rng.random() < 0.5:
            s[rng.randrange(len(s))] = rng.choice("()[]{}")
        s = "".join(s)
        assert brute(s) == fast(s), s


def test_steppers_up_to_date():
    # The step-through figures on the page are the output of tools/figures/q0010.py
    from extract_code import ROOT, question_path
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0010.py")],
                         capture_output=True, text=True, check=True).stdout
    generated = re.findall(r'<div class="stepper".*?</div></div>', out)
    page = re.findall(r'<div class="stepper".*?</div></div>', question_path(10).read_text(encoding="utf-8"))
    assert page == generated and len(page) == 2
