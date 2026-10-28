# Change the prices and press Run
prices = [5, 8, 3, 9, 2, 6]

print("prices:          ", prices)
print("long only, brute:", max_long_brute(prices))  # (6, 2, 3)
print("long only, fast: ", max_long_fast(prices))  # (6, 2, 3)
print("long/short brute:", max_profit_brute(prices))  # (7, 'short', 3, 4)
print("long/short fast: ", max_profit_fast(prices))  # (7, 'short', 3, 4)
