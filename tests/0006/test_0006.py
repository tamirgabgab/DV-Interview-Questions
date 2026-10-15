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
