# Change the prices and press Run
prices = [5, 8, 3, 9, 2, 6]

print("prices:          ", prices)
print("long only, brute:", max_long_brute(prices))
print("long only, fast: ", max_long_fast(prices))
print("long/short brute:", max_profit_brute(prices))
print("long/short fast: ", max_profit_fast(prices))
