# Horse races without a stopwatch: the plan of part a on random speeds, race by race
import random

from solution import *  # noqa: F401,F403

LETTERS = "ABCDEFGH"


def show(a, b, c, seed):
    speed = list(range(a))
    random.Random(seed).shuffle(speed)                     # hidden: lower is faster
    ranking, log = horses_plan(a, b, c, lambda g: sorted(g, key=lambda x: speed[x]))
    names = {x: f"{LETTERS[x // b]}{i + 1}" for k in range(0, a, b) for i, x in enumerate(sorted(range(k, min(k + b, a)), key=lambda x: speed[x]))}
    print(f"{a} horses, {b} per race, the {c} fastest: {len(log)} races")
    for r, order in enumerate(log, 1):
        print(f"  race {r}: " + " > ".join(names[x] for x in order))
    print("  ranking:", [names[x] for x in ranking], "- true:", [names[x] for x in sorted(range(a), key=lambda x: speed[x])[:c]])


show(36, 6, 4, 1)
show(30, 6, 3, 2)
show(25, 5, 3, 3)
