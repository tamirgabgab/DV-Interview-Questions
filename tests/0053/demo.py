# The coverage after a few transactions, and the expected closure time for three stimuli
import random
from solution import *  # noqa: F401,F403

cov = AluCoverage()
rng = random.Random(1)
for n in range(1, 2001):
    cov.sample(rng.choice(OPS), rng.randrange(256), rng.randrange(256), rng.randrange(2))
    if n in (1, 10, 100, 2000):
        print(f"{n} uniform transactions: coverage {cov.coverage():.1f}%")
for name, p in (("uniform", {"zero": 1 / 256, "max": 1 / 256, "msb": 1 / 256, "mid": 253 / 256}),
                ("dist 1/5", {"zero": 0.2, "max": 0.2, "msb": 0.2, "mid": 0.4})):
    print(f"{name}: about {expected_closure(cell_probs(p)):,.0f} transactions to close the cross")
