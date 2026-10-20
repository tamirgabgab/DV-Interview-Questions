#!/usr/bin/env python3
"""Figures and tables of question 0032.

    python tools/figures/fill.py 32        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. Shared chart helpers are in charts.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402,F401


def blocks():
    """The generated blocks, in page order."""
    return [
        "<!-- figure 0: replace with a drawing -->",
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
