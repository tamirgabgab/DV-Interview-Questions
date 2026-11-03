# The page's numbers, then 70000 draws of rand7, then randN from randM with the calls counted
import random
from collections import Counter

from solution import *  # noqa: F401,F403

print(expected_calls(5, 7))                               # 50/21
print(expected_calls(2, 5, 3), expected_calls(2, 5, 4))   # 24/5 64/15
print(exact_calls(5, 7), exact_calls(6, 8))               # 0 3

random.seed(1)
counts = Counter(rand7() for _ in range(70000))
print("rand7:", dict(sorted(counts.items())))

for m, n, k in ((5, 7, 0), (2, 5, 3), (2, 5, 4), (6, 8, 0)):
    used = [0]

    def src(m=m):
        used[0] += 1
        return random.randint(1, m)
    out = Counter(rand_n(src, m, n, k) for _ in range(20000))
    print(f"rand{n} from rand{m}, k = {k or calls_needed(m, n)}: calls per output {used[0] / 20000:.3f}, "
          f"exact {float(expected_calls(m, n, k)):.3f}")
