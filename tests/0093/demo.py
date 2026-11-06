# The page's functions on the example: candidates A..F propose to jobs 1..6
from solution import *  # noqa: F401,F403

CAND = ["615324", "142356", "213645", "365241", "341562", "136425"]   # A..F: the jobs, best first
JOBS = ["ECBAFD", "ABFDEC", "AFCDEB", "ADCEFB", "DCEFAB", "FCDAEB"]   # 1..6: the candidates, best first
P = [[int(c) - 1 for c in row] for row in CAND]
Q = [[ord(c) - 65 for c in row] for row in JOBS]

match, proposals = gale_shapley(P, Q)
print(" ".join(f"{chr(65 + i)}{j + 1}" for i, j in enumerate(match)))   # A5 B1 C2 D6 E4 F3
print(proposals)                                                       # 11
print(blocking_pairs(P, Q, match))                                     # []
print(len(all_stable(P, Q)))                                           # 5
