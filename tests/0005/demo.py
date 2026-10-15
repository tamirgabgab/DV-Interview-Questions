import time

# Change the values of x and press Run
for x in [7, 9, 12, 99, 999]:
    start = time.perf_counter()
    y = smallest_01_multiple(x)
    ms = (time.perf_counter() - start) * 1000
    print(f"x = {x:<4} y = {y}  ({len(y)} digits, {ms:.2f} ms)")

# The simple enumeration is fine for small answers only
print("by_enumeration(9) =", by_enumeration(9))
