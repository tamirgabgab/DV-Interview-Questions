import random
import re
import subprocess
import sys
from collections import Counter

from extract_code import ROOT, load_python, question_path

ns = load_python(17)
SOLUTIONS = [ns[f"find_duplicate_{s}"] for s in ("sort", "seen", "binary", "floyd")]
EXAMPLE = [3, 9, 5, 6, 7, 8, 1, 1, 2, 4]


def random_case(rng, n):
    """n + 1 values in 1..n: a random mix, sometimes one value repeated many times."""
    if rng.random() < 0.5:
        return [rng.randint(1, n) for _ in range(n + 1)]
    nums = list(range(1, n + 1))
    v = rng.randint(1, n)
    for i in rng.sample(range(n), rng.randint(0, n - 1)):
        nums[i] = v                      # v replaces some other values
    nums.append(v)
    rng.shuffle(nums)
    return nums


def test_example():
    for f in SOLUTIONS:
        assert f(list(EXAMPLE)) == 1, f.__name__


def test_random_inputs_and_input_unchanged():
    rng = random.Random(17)
    for _ in range(3000):
        nums = random_case(rng, rng.randint(1, 60))
        before = list(nums)
        dups = {v for v, c in Counter(nums).items() if c > 1}
        for f in SOLUTIONS:
            assert f(nums) in dups, (f.__name__, nums)
            assert nums == before, f.__name__


def test_every_input_up_to_n4():
    # all arrays of length n + 1 with values 1..n, n <= 4
    import itertools
    for n in range(1, 5):
        for nums in itertools.product(range(1, n + 1), repeat=n + 1):
            nums = list(nums)
            dups = {v for v, c in Counter(nums).items() if c > 1}
            for f in SOLUTIONS:
                assert f(nums) in dups, (f.__name__, nums)


def test_floyd_is_linear():
    # count the steps: phase 1 at most mu + lambda, phase 2 mu, so at most 2(n + 1)
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 300)
        nums = random_case(rng, n)
        seen, x = {}, 0
        while x not in seen:
            seen[x] = len(seen)
            x = nums[x]
        mu, lam = seen[x], len(seen) - seen[x]
        assert mu >= 1 and mu + lam <= n + 1


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0017.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(17).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<svg class="figure".*?</svg>',
                    r'<div class="box-grid.*?</div>',
                    r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    for row in (l.strip() for l in out.splitlines() if l.startswith("|")):
        assert row in page_rows, row
