# Three eggs and 100 floors: the worst case, the first egg's floors, and the run against threshold 36
from solution import *  # noqa: F401,F403

for k, n in ((3, 100), (2, 100), (4, 1000)):
    t = min_drops(k, n)
    first = [fl for fl, broke in egg_run(k, n, n)]
    print(f"{k} eggs, {n} floors: {t} drops in the worst case; the first egg: {first}")

print("threshold 36:", egg_run(3, 100, 36))
used = [len(egg_run(3, 100, T)) for T in range(101)]
print("worst over every threshold:", max(used), "- thresholds at the worst case:", used.count(max(used)))
