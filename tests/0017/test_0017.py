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


def test_explorer_matches_page_code():
    """The Floyd explorer: its frames against a Python replay of the page's
    find_duplicate_floyd, its answer against the page function, and the rho (tail, cycle,
    entry) against a plain walk."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(17)
    cases = [EXAMPLE] + [random_case(rng, rng.randint(3, 12)) for _ in range(80)]
    cases += [[1, 1], [2, 1, 2], [1, 2, 3, 1], [3, 3, 3, 3]]
    got = node_json(f"""
      const m = {explorer_require()};
      const cases = {json.dumps(cases)};
      console.log(JSON.stringify({{
        rho: cases.map((c) => m.floydRho(c)),
        trace: cases.map((c) => m.floydTrace(c)),
        parse: [m.floydParse("3, 9, 5, 6, 7, 8, 1, 1, 2, 4"), m.floydParse("1 2 3"), m.floydParse("0 1"), m.floydParse("x")],
      }}));""")
    assert got["parse"] == [EXAMPLE, None, None, None]
    for nums, rho, tr in zip(cases, got["rho"], got["trace"]):
        # the rho by a plain walk from 0
        walk, x = [], 0
        while x not in walk:
            walk.append(x)
            x = nums[x]
        mu = walk.index(x)
        assert rho["tail"] == walk[:mu] and rho["cycle"] == walk[mu:] and rho["entry"] == x
        assert rho["mu"] == mu and rho["lambda"] == len(walk) - mu
        assert rho["others"] == [i for i in range(len(nums)) if i not in walk]
        assert nums.count(x) >= 2
        # the frames: a replay of the page's two loops
        frames, slow, fast, step = [{"phase": 1, "step": 0, "slow": 0, "fast": 0}], 0, 0, 0
        while True:
            slow, fast, step = nums[slow], nums[nums[fast]], step + 1
            frames.append({"phase": 1, "step": step, "slow": slow, "fast": fast})
            if slow == fast:
                break
        meet, slow, step = slow, 0, 0
        frames.append({"phase": 2, "step": 0, "slow": 0, "fast": fast})
        while slow != fast:
            slow, fast, step = nums[slow], nums[fast], step + 1
            frames.append({"phase": 2, "step": step, "slow": slow, "fast": fast})
        assert tr["frames"] == frames and tr["meet"] == meet
        assert tr["answer"] == slow == x == ns["find_duplicate_floyd"](list(nums))
