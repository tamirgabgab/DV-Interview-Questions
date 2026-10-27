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


def test_explorer_matches_page_code():
    """The brackets explorer: its verdict against the page's isValid and isValid_brute on
    the examples, every short string and random long ones, and its frames against a
    replay of the page's stack loop."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(10)
    alphabet = "()[]{}"
    cases = list(EXAMPLES) + ["".join(p) for n in range(1, 5) for p in itertools.product(alphabet, repeat=n)]
    cases += ["".join(rng.choice(alphabet) for _ in range(rng.randint(5, 40))) for _ in range(400)]
    cases += ["(" * 20 + ")" * 20, "([{" * 6 + "}])" * 6, "a(b)[c]{ }x"]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map((s) => m.bracketsTrace(m.bracketsClean(s)))));""")
    pairs = {")": "(", "]": "[", "}": "{"}
    for raw, tr in zip(cases, got):
        s = "".join(c for c in raw if c in alphabet)
        assert tr["valid"] == ns["isValid"](s) == ns["isValid_brute"](s), s
        assert tr["odd"] == (len(s) % 2 == 1)
        frames, stack, fail = [], [], None
        for i, ch in enumerate(s):
            if ch in pairs:
                if not stack:
                    fail = {"i": i, "kind": "unopened"}
                    frames.append({"i": i, "ch": ch, "action": "unopened", "stack": ""})
                    break
                if stack[-1] != pairs[ch]:
                    fail = {"i": i, "kind": "mismatch", "top": stack[-1]}
                    frames.append({"i": i, "ch": ch, "action": "mismatch", "stack": "".join(stack), "top": stack[-1]})
                    break
                stack.pop()
                frames.append({"i": i, "ch": ch, "action": "pop", "stack": "".join(stack)})
            else:
                stack.append(ch)
                frames.append({"i": i, "ch": ch, "action": "push", "stack": "".join(stack)})
        if fail is None and stack:
            fail = {"i": len(s), "kind": "unclosed", "left": "".join(stack)}
        assert tr["frames"] == frames and tr["fail"] == fail, s


def test_explorer_pair_passes():
    """The box's part a (V4): the passes of the pair deletion and the characters they read,
    against the page's Python loop with every replace counted."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(10)
    cases = ["", "()", "(((())))", "([)]", "{[()]}", "()[]{}"] + ["".join(rng.choice("()[]{}") for _ in range(rng.randint(1, 20))) for _ in range(150)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map((s) => {{ const r = m.bracketsPasses(s); return [r.passes.map((p) => p.after), r.reads, r.valid]; }})));""")
    for s, (afters, reads, valid) in zip(cases, got):
        want, total = [], 0
        while "()" in s or "[]" in s or "{}" in s:
            for pair in ("()", "[]", "{}"):
                total += len(s)
                s = s.replace(pair, "")
            want.append(s)
        assert afters == want and reads == total and valid == (s == "")
