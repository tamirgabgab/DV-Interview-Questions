# Change the numbers and press Run
for x in [352, 7, 45, 111, 0, 495]:
    d = sorted(f"{x:03d}")
    big, small = int("".join(reversed(d))), int("".join(d))
    print(f"{x:03d}: {big:03d} - {small:03d} = {big - small:03d}  special={is_special(x)}")

print("special numbers:", find_special())

# Follow-up: repeat the step until it stops changing
x = 352
path = [x]
while True:
    d = sorted(f"{x:03d}")
    x = int("".join(reversed(d))) - int("".join(d))
    if x == path[-1]:
        break
    path.append(x)
print(" -> ".join(map(str, path)))

# Part c: the same step in base 7, from 610 (301 in decimal)
DIGITS = "0123456789ABCDEF"
text = lambda v, b: "".join(DIGITS[u] for u in (v // (b * b), v // b % b, v % b))  # noqa: E731
print("base 7:", " -> ".join(text(v, 7) for v in kaprekar_chain_b(301, 7)), "| attractor:", [text(v, 7) for v in kaprekar_attractor_b(7)])
print("base 10 attractor:", kaprekar_attractor_b(10), "| base 12:", text(kaprekar_attractor_b(12)[0], 12))
