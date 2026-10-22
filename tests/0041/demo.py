# 16 equal bins: the expectation, the median and the 95 % point; then unequal bins and at_least
import random
from solution import *  # noqa: F401,F403

for n in (16, 100):
    print(f"{n} bins: expected {expected_uniform(n):.1f}, median {tests_for(n, 0.5)}, 95% at {tests_for(n, 0.95)}")

rng = random.Random(1)
for p, k in (([0.25] * 4, 1), ([0.1, 0.2, 0.3, 0.4], 1), ([0.1, 0.2, 0.3, 0.4], 3), ([0.01] + [0.99 / 15] * 15, 1)):
    runs = 2000
    mean = sum(simulate_tests(p, k, rng) for _ in range(runs)) / runs
    closed = f", closed form {expected_k1(p):.2f}" if k == 1 else ""
    print(f"p={p[:4]}{'...' if len(p) > 4 else ''} k={k}: integral {expected_tests(p, k):.2f}{closed}, simulation {mean:.2f}")
