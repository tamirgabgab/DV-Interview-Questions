# Change the numbers and press Run
for x in [3524, 95, 1000, 7777, 0, 6174]:
    d = sorted(f"{x:04d}")
    big, small = int("".join(reversed(d))), int("".join(d))
    print(f"{x:04d}: {big:04d} - {small:04d} = {big - small:04d}  special={is_special_4(x)}")

print("special numbers:", find_special_4())  # [0, 6174]

# Follow-up: repeat the step until it reaches a fixed point
x = 95
path = [x]
while True:
    d = sorted(f"{x:04d}")
    x = int("".join(reversed(d))) - int("".join(d))
    if x == path[-1]:
        break
    path.append(x)
print(" -> ".join(f"{v:04d}" for v in path), f"({len(path) - 1} steps)")  # 0095 -> 9441 -> 7992 -> 7173 -> 6354 -> 3087 -> 8352 -> 6174 (7 steps)

# The bonus: four digits in base B
DIG = "0123456789ABCDEF"
text = lambda v, B: "".join(DIG[v // B**k % B] for k in (3, 2, 1, 0))  # noqa: E731
for B in (5, 10, 15):
    print(f"base {B}: fixed points", [text(v, B) for v in kaprekar4_fixed_b(B)])
values, start = kaprekar4_orbit_b(1 * 15**3 + 2 * 15**2 + 3 * 15 + 4, 15)
print("base 15, 1234:", " -> ".join(text(v, 15) for v in values), "| the cycle starts at step", start + 1)  # 1234 -> 30DC -> D852 -> B2B4 -> 9676 | the cycle starts at step 2
