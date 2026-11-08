import random

from extract_code import load_python

ns = load_python(6)


def check_trade(prices, result):
    profit, kind, first, second = result
    if kind is None:
        assert profit == 0 and first is None and second is None
        return
    assert first < second
    gain = prices[second] - prices[first]
    assert profit == (gain if kind == "long" else -gain) and profit > 0


def test_page_example():
    prices = [5, 8, 3, 9, 2, 6]
    assert ns["max_profit_fast"](prices) == (7, "short", 3, 4)
    assert ns["max_profit_brute"](prices) == (7, "short", 3, 4)
    assert ns["max_long_fast"](prices) == (6, 2, 3)


def test_fast_matches_brute():
    rng = random.Random(6)
    for _ in range(3000):
        prices = [rng.randint(1, 20) for _ in range(rng.randint(0, 10))]
        brute, fast = ns["max_profit_brute"](prices), ns["max_profit_fast"](prices)
        assert brute[0] == fast[0], prices
        check_trade(prices, brute)
        check_trade(prices, fast)
        assert ns["max_long_brute"](prices)[0] == ns["max_long_fast"](prices)[0], prices


def test_chart_trades_match_page_code():
    import sys

    from extract_code import ROOT

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0006

    (lp, lb, ls), (sp, ss, sb) = q0006.best_trades()
    assert (lp, lb, ls) == tuple(ns["max_long_fast"](q0006.PRICES))
    assert (sp, "short", ss, sb) == tuple(ns["max_profit_fast"](q0006.PRICES))


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(6)


def test_explorer_matches_page_code():
    """The stock explorer: its scan against the page's max_long_fast and max_profit_fast
    on the page example, short arrays and random prices."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(6)
    cases = [[5, 8, 3, 9, 2, 6], [], [7], [9, 1], [1, 9], [4, 4, 4], [3, 4, 6, 7, 9, 11, 12, 14, 16, 18], [18, 16, 15, 13, 12, 10, 8, 7, 5, 3]]
    cases += [[rng.randint(1, 20) for _ in range(rng.randint(0, 12))] for _ in range(300)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map((p) => m.stockScan(p))));""")
    for prices, sc in zip(cases, got):
        best, buy, sell = ns["max_long_fast"](prices)
        assert (sc["long"]["best"], sc["long"]["open"], sc["long"]["close"]) == (best, buy, sell), prices
        profit, kind, first, second = ns["max_profit_fast"](prices)
        side = sc["short"] if kind == "short" else sc["long"] if kind == "long" else None
        assert sc["kind"] == kind, prices
        if side:
            assert (side["best"], side["open"], side["close"]) == (profit, first, second), prices
        else:
            assert profit == 0
        # the frames replay the loop: the running minimum and maximum before each day
        for i, fr in enumerate(sc["frames"]):
            assert fr["minP"] == min(prices[:i + 1]) if i == 0 else fr["minP"] == min(prices[:i])
            assert fr["maxP"] == max(prices[:i + 1]) if i == 0 else fr["maxP"] == max(prices[:i])
            assert fr["longToday"] == prices[i] - fr["minP"] and fr["shortToday"] == fr["maxP"] - prices[i]


def test_explorer_state_link():
    """The copy link of the box carries the prices, the day reached and the mode as
    `#state-stock.<payload>`: the codec round-trips the page example and random boxes,
    clamps the day to the number of prices, and rejects prices outside 1..20, a single
    price, more than 30 or a malformed payload."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(60)
    states = [{"prices": [5, 8, 3, 9, 2, 6], "k": 3, "both": True}]
    states += [{"prices": [rng.randint(1, 20) for _ in range(rng.randint(2, 30))], "k": rng.randint(0, 30), "both": rng.random() < 0.5} for _ in range(40)]
    bad = ["5.8.0-1-both", "5.8.21-1-both", "5-1-both", "5.8-1-short", "5.8-x-both", "", "5.8.3.9.2.6-3", "5..8-1-both", ".".join(["5"] * 31) + "-1-both"]
    got = node_json(f"""
      const m = {explorer_require()};
      const C = m.STATE_CODECS.stock;
      console.log(JSON.stringify({{ trip: {json.dumps(states)}.map((s) => [C.enc(s), C.dec(C.enc(s))]), bad: {json.dumps(bad)}.map((t) => C.dec(t)) }}));""")
    for s, (payload, back) in zip(states, got["trip"]):
        assert payload == ".".join(map(str, s["prices"])) + f"-{s['k']}-" + ("both" if s["both"] else "long")
        assert back == {"prices": s["prices"], "k": min(s["k"], len(s["prices"])), "both": s["both"]}, s
    assert got["bad"] == [None] * len(bad)


def test_explorer_typed_prices():
    """The box's price field: whole numbers split by spaces or commas, 2 to 30 of them,
    each 1..20; anything else is refused with a Hebrew reason (a string)."""
    import json

    from page_tests import explorer_require, node_json

    ok = {"7 1 5 3 6 4": [7, 1, 5, 3, 6, 4], " 5,8, 3 ,9  2,6 ": [5, 8, 3, 9, 2, 6], "1 20": [1, 20],
          " ".join(["3"] * 30): [3] * 30}
    bad = ["", "7", "7 x 5", "7 1.5", "7 -1", "0 5", "5 21", " ".join(["3"] * 31), "7;1"]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(list(ok) + bad)}.map((t) => m.stockParse(t))));""")
    assert got[:len(ok)] == list(ok.values())
    assert all(isinstance(r, str) and r for r in got[len(ok):]), got[len(ok):]


def _long_update_first(prices):
    """Part a's loop with the two lines swapped: the minimum updated before the check."""
    best, buy, sell = 0, None, None
    if not prices:
        return best, buy, sell
    min_p, min_i = prices[0], 0
    for i, p in enumerate(prices):
        if p < min_p:
            min_p, min_i = p, i
        if p - min_p > best:
            best, buy, sell = p - min_p, min_i, i
    return best, buy, sell


def _must_trade(prices, update_first=False):
    """The follow-up "a trade is a must": the best starts at day 1 minus day 0."""
    min_p, min_i = prices[0], 0
    best, buy, sell = prices[1] - prices[0], 0, 1
    for i in range(1, len(prices)):
        p = prices[i]
        if update_first and p < min_p:
            min_p, min_i = p, i
        if p - min_p > best:
            best, buy, sell = p - min_p, min_i, i
        if not update_first and p < min_p:
            min_p, min_i = p, i
    return best, buy, sell


def test_loop_order_claims():
    """Part a's proof: with the strict > and a best that starts at 0 the order of the check
    and the update changes neither the profit nor the days. The must-trade follow-up: there
    the order decides ({9, 7, 4, 1} gives -2 on days 0 and 1, the swapped order 0 on day 1)."""
    rng = random.Random(61)
    for _ in range(5000):
        prices = [rng.randint(1, 20) for _ in range(rng.randint(0, 10))]
        assert _long_update_first(prices) == ns["max_long_fast"](prices), prices
        if len(prices) >= 2:
            best = max(prices[j] - prices[i] for i in range(len(prices)) for j in range(i + 1, len(prices)))
            got = _must_trade(prices)
            assert got[0] == best and got[1] < got[2] and prices[got[2]] - prices[got[1]] == best, prices
    assert _must_trade([9, 7, 4, 1]) == (-2, 0, 1)
    assert _must_trade([9, 7, 4, 1], update_first=True) == (0, 1, 1)


def test_part_a_trace_and_traps():
    """Part a's trace on {3, 9, 1, 2}: the long is 6 (days 0 and 1), while max - min = 8 is
    the short of part b; the tie {1, 5, 1} answers the long. The box's trap buttons load the
    same prices."""
    import json

    from page_tests import explorer_require, node_json

    assert ns["max_long_fast"]([3, 9, 1, 2]) == (6, 0, 1)
    assert ns["max_profit_fast"]([3, 9, 1, 2]) == (8, "short", 1, 2)
    assert ns["max_profit_fast"]([1, 5, 1]) == (4, "long", 0, 1)
    assert ns["max_profit_brute"]([1, 5, 1]) == (4, "long", 0, 1)
    assert ns["max_profit_fast"]([2, 5, 1]) == (4, "short", 1, 2)   # the box task: day 0 -> 2
    assert ns["max_long_fast"]([3, 9, 1, 12]) == (11, 2, 3)          # the box task: day 3 -> 12
    # the trace table: the minimum of the previous days and the profit of each day
    prices, mins = [3, 9, 1, 2], [3, 3, 3, 1]
    assert [min(prices[:max(i, 1)]) for i in range(4)] == mins
    assert [p - m for p, m in zip(prices, mins)] == [0, 6, -2, 1]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify(m.stockTraps));""")
    assert got["peak"]["prices"] == [3, 9, 1, 2] and got["tie"]["prices"] == [1, 5, 1]


def test_followup_numbers():
    """The follow-ups on the page example: many trades 13; k = 1, 2, 3 trades 6, 10, 13;
    a fee of 2: one trade 7 - 2 = 5 (the short), many long trades 7 = 1 + 4 + 2."""
    ex = [5, 8, 3, 9, 2, 6]
    assert sum(max(0, b - a) for a, b in zip(ex, ex[1:])) == 13

    def k_trades(prices, k):
        hold, free = [float("-inf")] * (k + 1), [0] * (k + 1)
        for p in prices:
            for t in range(1, k + 1):
                hold[t] = max(hold[t], free[t - 1] - p)
                free[t] = max(free[t], hold[t] + p)
        return free[k]

    assert [k_trades(ex, k) for k in (1, 2, 3)] == [6, 10, 13]

    def many_with_fee(prices, fee):
        cash, hold = 0, float("-inf")
        for p in prices:
            cash, hold = max(cash, hold + p - fee), max(hold, cash - p)
        return cash

    assert ns["max_profit_fast"](ex)[0] - 2 == 5
    assert many_with_fee(ex, 2) == 7 == (8 - 5 - 2) + (9 - 3 - 2) + (6 - 2 - 2)
