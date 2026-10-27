# 1000 bottles in one, two and three rounds; bottle 613 found from the deaths
from solution import *  # noqa: F401,F403

for rounds in (1, 2, 3):
    m = mice_needed(1000, rounds)
    death = experiment(613, 1000, rounds)
    print(f"{rounds} round(s): {m} mice, deaths by round {death}, bottle {find_bottle(death, rounds)}")
