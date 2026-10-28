"""Question 0057: the page's last_fall, collisions and fall_times against the generator's
half-second simulation (tools/figures/q0057.py, ants that turn at every meeting) on random
poles; the page's numbers (90 s and 5 collisions for the six ants, 100 s and 2500 at most
for 100 ants); the explorer's JavaScript at every half second; and the page copies of the
generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0057  # noqa: E402

ns = load_python(57)
last_fall, collisions, fall_times, ring_after = (ns[k] for k in ("last_fall", "collisions", "fall_times", "ring_after"))


def random_pole(rng, n_max=14, length=100):
    n = rng.randint(1, min(n_max, length + 1))
    pos = sorted(rng.sample(range(length + 1), n))
    return pos, [rng.choice((1, -1)) for _ in pos]


def test_page_example():
    pos, dirs = q0057.POS, q0057.DIRS
    assert last_fall(pos, dirs) == 90 and collisions(pos, dirs) == 5
    assert fall_times(pos, dirs) == [25, 60, 75, 90, 60, 10]
    fall, hits, _ = q0057.simulate(pos, dirs)
    assert hits == 5 and [t for t, _ in fall] == [25, 60, 75, 90, 60, 10]
    assert [s for _, s in fall] == ["L", "L", "L", "R", "R", "R"]


def test_against_the_simulation():
    rng = random.Random(56)
    for _ in range(400):
        length = rng.choice([10, 37, 100])
        pos, dirs = random_pole(rng, 14, length)
        fall, hits, _ = q0057.simulate(pos, dirs, length)
        assert fall_times(pos, dirs, length) == [t for t, _ in fall], (pos, dirs)
        assert last_fall(pos, dirs, length) == max(t for t, _ in fall)
        assert collisions(pos, dirs) == hits
        # the ants that fall to the left are the leftmost ones, as many as go left
        ell = sum(1 for d in dirs if d < 0)
        assert [s for _, s in fall] == ["L"] * ell + ["R"] * (len(pos) - ell)


def test_bounds():
    # 100 s at most, reached only with an ant at an end facing in
    assert last_fall([0], [1]) == 100 == last_fall([3, 100], [1, -1]) and last_fall([1, 99], [1, -1]) == 99
    rng = random.Random(57)
    for _ in range(300):
        pos, dirs = random_pole(rng, 30)
        assert last_fall(pos, dirs) <= 100
        assert collisions(pos, dirs) <= len(pos) ** 2 // 4
    half = list(range(1, 101))
    assert collisions(half, [1] * 50 + [-1] * 50) == 2500
    # random directions: n(n - 1)/8 collisions on average (the follow-up), exactly by symmetry
    n = 6
    total = sum(collisions(list(range(n)), [1 if m >> i & 1 else -1 for i in range(n)]) for m in range(1 << n))
    assert total * 8 == n * (n - 1) * (1 << n)


def test_ring():
    """Part d: after each lap of 100 s ant i stands where ant (i + s) % n started, with its
    direction; every ant is home first after n / gcd(n, s) laps (simulated lap by lap)."""
    assert ring_after(q0057.RING_DIRS) == (2, 300) and ring_after(q0057.DIRS) == (0, 100)
    rng = random.Random(59)
    for _ in range(150):
        pos, dirs = random_pole(rng, 8, 99)
        n = len(pos)
        s, home = ring_after(dirs)
        start = list(zip(pos, dirs))
        lap = q0057.ring(pos, dirs, 100, 100)
        assert lap == [(float(pos[(i + s) % n]), dirs[(i + s) % n]) for i in range(n)], (pos, dirs)
        laps = next(k for k in range(1, n + 1) if q0057.ring(pos, dirs, 100, 100 * k) == [(float(p), d) for p, d in start])
        assert home == 100 * laps, (pos, dirs)


def test_explorer_matches_the_simulation():
    from page_tests import explorer_require, node_json

    rng = random.Random(58)
    cases = [(q0057.POS, q0057.DIRS)] + [random_pole(rng, 12) for _ in range(40)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([p, d]) => {{
        const T = 2 * m.antsEnd(p, d, 100);
        return {{ fall: m.antsFall(p, d, 100), hits: m.antsHits(p, d, T), frames: [...Array(T + 1).keys()].map((t) => m.antsAt(p, d, 100, t)) }};
      }})));""")
    for (pos, dirs), res in zip(cases, got):
        fall, hits, paths = q0057.simulate(pos, dirs)
        assert res["fall"] == [[t, s] for t, s in fall] and res["hits"] == hits
        # every ant at every half second: on the turning path of the simulation
        for t2, frame in enumerate(res["frames"]):
            for k, ant in enumerate(frame):
                want = position(paths[k], t2 / 2)
                if want is None:
                    assert ant["gone"] in ("L", "R"), (pos, dirs, t2, k)
                else:
                    assert ant["gone"] is None and abs(ant["x"] - want) < 1e-9, (pos, dirs, t2, k, ant, want)


def position(path, t):
    """Where an ant is at time t on its path of (t, x) corners, None once it fell (the last
    corner is the fall)."""
    if t >= path[-1][0]:
        return None
    for (t0, x0), (t1, x1) in zip(path, path[1:]):
        if t0 <= t <= t1:
            return x0 + (x1 - x0) * (t - t0) / (t1 - t0)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(57)
