# The trick and the best play on the page's rows
from solution import *  # noqa: F401,F403

for coins in ([1, 2, 5, 3], [1, 1, 9, 1, 1, 9], [1, 5, 1]):
    print(coins, "best:", best_total(coins), "of", sum(coins))
print("first move of the trick on 1, 2, 5, 3:", parity_move([1, 2, 5, 3], 0, 3))  # L
