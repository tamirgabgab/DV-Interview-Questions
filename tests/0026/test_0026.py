"""Question 0026 has no code on the page; these tests replay the plans as motion on the road
(exact fractions), check every number the page states, and check that the figures and the
tables are the generator's output."""

import re
import subprocess
import sys
from fractions import Fraction as Fr

from extract_code import ROOT, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0026  # noqa: E402

# Units: AB = 1, ride speed 1 (t1 = 1), walking speed 1 / alpha.


def meet(bike, walker, alpha):
    """Time until a motorcycle riding back from `bike` meets a walker coming from `walker`."""
    return (bike - walker) / (1 + Fr(1, alpha))


def shuttle(alpha, k, ride):
    """k people need a ride; each rides `ride` forward from the pick-up point, then walks.
    The motorcycle never waits: forward with one person, back to the walking group, again.
    Returns the arrival time of each person and of the motorcycle, and the drop points."""
    a = Fr(alpha)
    t, group = Fr(0), Fr(0)         # time, position of the people still waiting for a ride
    arrivals, drops = [], []
    for i in range(k):
        start = group
        t += ride                   # ride forward
        group += ride / a
        drop = start + ride
        drops.append(drop)
        arrivals.append(t + (1 - drop) * a)
        if i < k - 1:               # ride back to the group
            dt = meet(drop, group, alpha)
            t += dt
            group += dt / a
    return arrivals, t, drops


def best_ride(alpha, k):
    a = Fr(alpha)
    return (a + 1) / (a + 2 * k - 1)


def formula(alpha, k=2):
    a = Fr(alpha)
    return ((2 * k - 1) * a + 1) / (a + 2 * k - 1)


def test_plan_segments():
    for alpha in [Fr(n, 2) for n in range(3, 60)]:
        p = q0026.plan(alpha)
        x, y, z, r = p["x"], p["y"], p["z"], p["r"]
        assert min(x, y, z, r) > 0
        assert 2 * x + y + z + r == 1                       # (4)
        assert alpha * y == y + x + z                       # (1)
        assert z == alpha * x                               # (2)
        assert alpha * r == z + x + r                       # (3)
        assert y == r and y + x == 2 / (alpha + 3)
        assert p["T"] == q0026.t_optimal(alpha) == formula(alpha)
        # through the motorcycle: 2x + 2y + 3z; through the walker: walk y + x, ride the rest
        assert 2 * x + 2 * y + 3 * z == p["T"]
        assert (y + x) * alpha + (1 - y - x) == p["T"]
        # in t0 and t1 only: (3 t0 + t1) / (t0 + 3 t1) * t1
        t1 = Fr(7, 3)
        t0 = alpha * t1
        assert (3 * t0 + t1) / (t0 + 3 * t1) * t1 == p["T"] * t1


def test_plan_as_motion():
    """Replay the three phases and check who is where at each phase end."""
    for alpha in (Fr(3, 2), 2, 4, 13, 100):
        p = q0026.plan(alpha)
        a = Fr(alpha)
        t1 = p["D"]                                  # motorcycle with the passenger to D
        walker = t1 / a
        assert walker == p["Q"]
        dt = meet(p["D"], walker, alpha)             # back to the walker
        assert p["D"] - dt == walker + dt / a == p["C"]
        assert t1 + dt == p["t2"]
        assert p["D"] + dt / a == p["E"]             # the passenger walked meanwhile
        assert p["t2"] + (1 - p["C"]) == p["T"]      # walker on the motorcycle to B
        assert p["t2"] + (1 - p["E"]) * a == p["T"]  # passenger on foot to B
        arrivals, bike, drops = shuttle(alpha, 2, best_ride(alpha, 2))
        assert arrivals == [p["T"], p["T"]] and bike == p["T"] and drops[0] == p["D"]
        assert drops[1] == 1


def test_numbers_on_the_page():
    p = q0026.plan(13)
    assert p["T"] == Fr(5, 2)
    assert (p["x"], p["y"], p["z"]) == (Fr(3, 52), Fr(7, 104), Fr(3, 4))
    assert (p["Q"], p["C"], p["D"], p["E"]) == (Fr(7, 104), Fr(1, 8), Fr(7, 8), Fr(97, 104))
    assert (p["t1"], p["t2"]) == (Fr(7, 8), Fr(13, 8))
    assert p["y"] + p["x"] == Fr(1, 8) and Fr(1, 8) * 13 == Fr(13, 8)    # 1 h 37.5 min on foot
    assert (1 - Fr(1, 8)) * 60 == Fr(105, 2)                             # 52.5 min riding
    assert Fr(3 * 13 + 1, 13 + 3) == Fr(40, 16)
    assert q0026.t_optimal(13) == best_ride(13, 2) * 1 + (1 - best_ride(13, 2)) * 13
    assert best_ride(13, 2) == Fr(7, 8)
    # second example: AB = 360 km, 60 and 15 km/h, alpha = 4, t1 = 6 h
    assert q0026.t_optimal(Fr(60, 15)) * Fr(360, 60) == Fr(78, 7)
    assert q0026.t_optimal(4) == Fr(13, 7)
    # follow-ups: 52 km, so 52 and 4 km/h; each walks 1/8 of the way
    assert Fr(52, 8) == Fr(13, 2)
    assert formula(13, 3) == Fr(11, 3)


def test_other_strategies():
    for alpha in (2, 4, 13, 50):
        a = Fr(alpha)
        # ride to B, ride back to the walker who left at time 0, ride to B
        dt = meet(1, 1 / a, alpha)
        assert 1 + 2 * dt == q0026.t_walk_meanwhile(alpha)
        assert q0026.t_optimal(alpha) < q0026.t_walk_meanwhile(alpha) < q0026.t_wait(alpha)
    assert q0026.t_walk_meanwhile(13) == Fr(19, 7)


def test_drop_point_is_best():
    """Among plans "drop the passenger at d, go back for the walker, ride to B", the latest
    arrival is smallest at the page's drop point."""
    alpha = 13

    def latest(d):
        dt = meet(d, d / alpha, alpha)
        bike = d + dt + (1 - (d - dt))
        passenger = d + (1 - d) * alpha
        return max(bike, passenger)

    grid = [Fr(i, 1000) for i in range(1, 1001)]
    best = min(grid, key=latest)
    assert best == Fr(7, 8) and latest(best) == Fr(5, 2)


def test_more_people_follow_up():
    for alpha in (2, 4, 13):
        for k in range(1, 7):
            arrivals, bike, drops = shuttle(alpha, k, best_ride(alpha, k))
            T = formula(alpha, k)
            assert arrivals == [T] * k and bike == T and drops[-1] == 1


def test_limits():
    assert abs(float(q0026.t_optimal(Fr(1) + Fr(1, 10 ** 9))) - 1) < 1e-8
    assert abs(float(q0026.t_optimal(10 ** 9)) - 3) < 1e-8
    for alpha in (Fr(11, 10), 2, 13, 1000):
        assert q0026.t_optimal(alpha) < alpha


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0026.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(26).read_text(encoding="utf-8")
    pattern = r'<svg class="(?:figure|perf-chart)".*?</svg>|<span class="viz-legend">.*?</span></span>'
    assert re.findall(pattern, text) == re.findall(pattern, out)
    assert len(re.findall(pattern, out)) == 6
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    table_rows = [l.strip() for l in out.splitlines() if l.startswith("|")]
    assert page_rows == table_rows


def test_explorer_matches_python():
    from page_tests import explorer_require, node_json

    alphas = [1.5, 2, 4, 13, 30]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({alphas}.map((a) => m.motorcyclePlan(a))));")
    for alpha, plan in zip(alphas, got):
        ref = q0026.plan(Fr(alpha).limit_denominator(100))
        for key in ("x", "y", "z", "Q", "C", "D", "E", "t1", "t2", "T"):
            assert abs(plan[key] - float(ref[key])) < 1e-12, (alpha, key)
    times = node_json(f"const m = {explorer_require()};"
                      "console.log(JSON.stringify([m.motorcycleTime(13, 1), m.motorcycleTime(24, 6)]));")
    assert abs(times[0] - 2.5) < 1e-12 and abs(times[1] - 78 / 7) < 1e-12
