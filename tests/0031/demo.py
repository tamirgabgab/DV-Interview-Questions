# The four people of the question: 1, 2, 5 and 10 minutes
NAMES = "ABCDEFGH"
for times in ([1, 2, 5, 10], [1, 2, 5, 10, 20], [1, 2, 3, 4], [3, 3, 3, 3, 3]):
    total, moves = bridge(times)
    plan = " ".join("".join(NAMES[i] for i in g) + (">" if k % 2 == 0 else "<") for k, g in enumerate(moves))
    print(f"{times}: {total} minutes, {plan}")
