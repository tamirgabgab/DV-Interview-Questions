# Change the numbers and press Run
for x in [3524, 95, 1000, 7777, 0, 6174]:
    d = sorted(f"{x:04d}")
    big, small = int("".join(reversed(d))), int("".join(d))
    print(f"{x:04d}: {big:04d} - {small:04d} = {big - small:04d}  special={is_special_4(x)}")

print("special numbers:", find_special_4())

# Follow-up: repeat the step until it reaches a fixed point
x = 95
path = [x]
while True:
    d = sorted(f"{x:04d}")
    x = int("".join(reversed(d))) - int("".join(d))
    if x == path[-1]:
        break
    path.append(x)
print(" -> ".join(f"{v:04d}" for v in path), f"({len(path) - 1} steps)")
