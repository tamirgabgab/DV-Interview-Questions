# Random final boards. Change `lines` to WRAP_LINES for part b and press Run.
lines = LINES

for _ in range(4):
    result, board = randomize(lines)
    print(f"result: {result}")
    print(show(board), "\n")

print({result: len(boards) for result, boards in final_boards(lines).items()})  # {'X': 626, 'O': 316, 'draw': 16}
