# Change the strings and press Run
tests = ["()", "()[]{}", "{[()]}", "([]{})", "(]", "([)]", "(((", "())", ")("]

for s in tests:
    print(f"{s:10} brute={isValid_brute(s)!s:5}  stack={isValid(s)}")

# The worst case of the simple solution: n/2 times "(" then n/2 times ")"
import time
for n in [1_000, 10_000]:
    s = "(" * (n // 2) + ")" * (n // 2)
    for f in (isValid_brute, isValid):
        t = time.perf_counter()
        f(s)
        print(f"n={n:6} {f.__name__:14} {1000 * (time.perf_counter() - t):8.2f} ms")
