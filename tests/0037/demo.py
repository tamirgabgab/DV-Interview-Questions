# MTBF of one, two and three flops at 500 MHz and 1 GHz (the page example)
from solution import *  # noqa: F401,F403

YEAR = 365.25 * 86400
for f_clk in (500e6, 1e9):
    for flops in (1, 2, 3):
        m = sync_mtbf(f_clk, 50e6, 100e-12, 50e-12, 0.3e-9, flops)
        unit = f"{m:.3g} s" if m < 86400 else f"{m / 86400:.3g} days" if m < YEAR else f"{m / YEAR:.3g} years"
        print(f"{f_clk / 1e6:.0f} MHz, {flops} flop(s): {unit}")
