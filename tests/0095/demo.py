# Starting code of the run panel of question 0095: the page's Python code is loaded
# as solution.py; call its functions here.
from solution import *  # noqa: F401,F403

for n in (1, 2, 3):
    army, moves = search(n, NEED[n])
    boards = replay(army, moves)
    print(f"row {n}: {len(army)} soldiers, {len(moves)} jumps, potential {float(potential(army, n))}")

# row 4: search(4, 20) takes a few seconds; its play, replayed:
for n in (4, 5):
    print(f"row {n}: the whole half plane weighs {float(half_plane(n)):.6f}")
print(half_plane(5) == 1)   # True: exactly 1, so no finite army reaches row 5
