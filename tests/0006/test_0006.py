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
