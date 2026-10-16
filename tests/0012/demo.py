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
