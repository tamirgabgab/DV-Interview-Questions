# The odd ball on a balance: the interviewer's test harness against the page's solvers
from solution import *  # noqa: F401,F403


def make_scale(n, odd, heavy):
    w = {b: 10 for b in range(1, n + 1)}
    w[odd] = 11 if heavy else 9
    calls = [0]

    def weigh(left, right):
        calls[0] += 1
        assert len(set(left) | set(right)) == len(left) + len(right), "ball used twice"
        l, r = sum(w[b] for b in left), sum(w[b] for b in right)
        return "left" if l > r else "right" if r > l else "equal"
    return weigh, calls


def test(solver, n, max_weighings):
    for odd in range(1, n + 1):
        for heavy in (True, False):
            weigh, calls = make_scale(n, odd, heavy)
            assert solver(weigh) == (odd, "heavy" if heavy else "light")
            assert calls[0] <= max_weighings
    print(f"{n} balls: all {2 * n} cases in at most {max_weighings} weighings")


test(find_odd_ball_12_tree, 12, 3)
test(find_odd_ball_12, 12, 3)
test(lambda w: find_odd_ball(39, w), 39, 4)
test(lambda w: find_odd_ball(13, w), 13, 4)
weigh, _ = make_scale(12, 11, False)
print("ball 11 light ->", find_odd_ball_12(weigh))  # ball 11 light -> (11, 'light')
