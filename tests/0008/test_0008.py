import itertools
import random

from extract_code import load_python

ns = load_python(8)
cannot_win = ns["israel_cannot_win"]
earliest = ns["earliest_certain_loss"]

ABOVE_2026 = [("Poland", 133, 17), ("Italy", 134, 147), ("Finland", 141, 138),
              ("France", 144, 14), ("Australia", 165, 122), ("Denmark", 165, 78),
              ("Bulgaria", 204, 312)]


def test_page_example():
    assert not cannot_win(343, [133, 134, 141, 144, 165, 165, 204], 828)
    assert not cannot_win(343, [165, 165, 204], 495)       # exactly fills every cup
    assert cannot_win(343, [165, 165, 204], 512)
    assert cannot_win(343, [344], 0)                       # already ahead
    assert not cannot_win(343, [], 0)
    assert earliest(343, ABOVE_2026, 828) == 4             # France
    # The order between Australia and Denmark does not matter
    swapped = ABOVE_2026[:4] + [ABOVE_2026[5], ABOVE_2026[4], ABOVE_2026[6]]
    assert earliest(343, swapped, 828) == 4


def can_still_win_brute(israel_total, jury, left):
    """Try every way to split `left` points among the countries (small inputs only)."""
    for split in itertools.product(range(left + 1), repeat=len(jury)):
        if sum(split) == left and all(j + p <= israel_total for j, p in zip(jury, split)):
            return True
    return not jury and left == 0


def test_check_matches_brute_force():
    rng = random.Random(8)
    for _ in range(400):
        israel_total = rng.randint(0, 8)
        jury = [rng.randint(0, 10) for _ in range(rng.randint(0, 3))]
        left = rng.randint(0, 9)
        assert cannot_win(israel_total, jury, left) == (not can_still_win_brute(israel_total, jury, left))


def earliest_reference(israel_total, above, points_left):
    """Call the check again after every announcement: O(k^2), obviously right."""
    for k in range(len(above) + 1):
        left = points_left - sum(p for _, _, p in above[:k])
        passed = any(j + p > israel_total for _, j, p in above[:k])
        if passed or cannot_win(israel_total, [j for _, j, _ in above[k:]], left):
            return k
    return None


def test_scan_matches_reference():
    rng = random.Random(80)
    for _ in range(3000):
        israel_total = rng.randint(50, 400)
        above = [(f"c{i}", rng.randint(0, israel_total + 20), rng.randint(0, 300))
                 for i in range(rng.randint(0, 8))]
        points_left = sum(p for _, _, p in above)
        assert earliest(israel_total, above, points_left) == earliest_reference(israel_total, above, points_left)
