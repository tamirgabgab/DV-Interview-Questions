# The expected waits of a few patterns, and a race, against a quick simulation
import random
from solution import *  # noqa: F401,F403

rng = random.Random(1)
for p in ("HT", "HH", "HHH", "HTH"):
    runs, total = 5000, 0
    for _ in range(runs):
        seen = ""
        while not seen.endswith(p):
            seen += rng.choice("HT")
        total += len(seen)
    print(f"{p}: formula {expected_tosses(p)}, simulation {total / runs:.2f}")
print("THH before HHH:", p_first("THH", "HHH"))
