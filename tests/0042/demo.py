# The camel and the water: the route of part a, the passes one by one, and the water balance
from solution import *  # noqa: F401,F403

for a, c, w, T in ((0.5, 150, 450, 30), (0.5, 150, 250, 30), (1, 100, 1000, 0)):
    segments = camel_segments(a, c, w, T)
    print(f"a={a} c={c} w={w} T={T}: {camel_distance(a, c, w, T):.1f} km, stops at "
          + (", ".join(f"{x1:.1f}" for _, x1, _ in segments[:-1]) or "none") + f", {len(camel_passes(a, c, w, T))} passes")

for s, back, start, end, depots in camel_passes(0.5, 150, 450, 30):
    print(f"segment {s + 1} {'back' if back else 'out '}: {start:5.0f} -> {end:5.0f} litres, depots {[round(v) for v in depots]}")

print("burned, delivered:", camel_check(0.5, 150, 450, 30))
