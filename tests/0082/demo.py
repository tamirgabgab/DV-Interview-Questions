# Nim: the winning move of each rule, for a few positions
from solution import *  # noqa: F401,F403

for heaps in ([3, 4, 5], [1, 2, 3], [1, 1, 4], [5, 6, 7]):
    print(heaps, "normal:", nim_move(heaps), " misere:", misere_move(heaps),
          " 1/3/4:", subtraction_move(heaps))
print("Grundy numbers of 1, 3, 4:", grundy(20))
