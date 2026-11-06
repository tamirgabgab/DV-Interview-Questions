# The page's functions: part a's 3 x 3 board with the top row lit, part b's 6 x 6, 5 x 5 and
# light chasing, part c's diagonals, part d's free variables by the polynomials
from solution import *  # noqa: F401,F403

x, free = solve_lights(3, 0b000000111)
print([k for k in range(9) if x >> k & 1], free)      # [3, 4, 5, 7] 0
print(solve_lights(6, (1 << 36) - 1)[1])              # 0
print(solve_lights(5, 1)[0], solve_lights(5, 1)[1])   # None 2
print(bin(solve_by_chasing(5, (1 << 25) - 1)).count("1") >= 15)   # True
print(len(king_quiet(5)), solve_lights(5, 0, True)[1])   # 9 9
print([plus_nullity(n) for n in range(1, 11)])        # [0, 0, 0, 4, 2, 0, 0, 0, 8, 0]
