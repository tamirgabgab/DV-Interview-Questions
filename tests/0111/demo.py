# The testbench of the page, fix after fix, with the default seed; change the seed or the flags
from solution import *  # noqa: F401,F403

SEED = 187
steps = [("as found", (0, 0, 0, 0)), ("+ backpressure", (1, 0, 0, 0)), ("+ assertion", (1, 1, 0, 0)),
         ("+ scoreboard", (1, 1, 1, 0)), ("+ DUT fix", (1, 1, 1, 1))]
for name, flags in steps:
    r = run_bench(SEED, *flags)
    verdict = f"FAILED, first error {r['errors'][0]}" if r["errors"] else "PASSED"
    print(f"{name:15} {r['n_in']:2} in, {r['n_out']:2} out, items left {r['left']}: {verdict}")
