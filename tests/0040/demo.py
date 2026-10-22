# The detector on the question's stream, and the general machine on a few patterns
from solution import *  # noqa: F401,F403

bits = [int(c) for c in "1011011"]
states, out = detect_1011(bits)
print("1011011:", list(zip(bits, states, out)))

for text in ("1011", "0110", "1111", "10101"):
    pattern = [int(c) for c in text]
    print(text, "table:", fsm_table(pattern))
    stream = [int(c) for c in "10110110101011"]
    print("  mealy:", run_fsm(pattern, stream)[1], " moore:", run_fsm(pattern, stream, moore=True)[1])
