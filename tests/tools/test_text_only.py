"""tools/checks/text_only.py: which changes take the CI's fast lane."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import text_only  # noqa: E402

PAGE = "docs/questions/junior/0055-divisible-by-m-fsm.md"
BASE = """---
id: 55
title: x
---
## השאלה

פסקה ראשונה.

<!-- gen 0 -->
<svg class="figure">a</svg>
<!-- /gen -->

```python
def f():
    return 1
```

<div class="explorer" data-kind="divfsm" data-m="3"></div>
"""


def run(new, path=PAGE, old=BASE):
    return text_only.verdict({path: (old, new)})


def test_prose_only_is_fast():
    fast, ids, _ = run(BASE.replace("פסקה ראשונה.", "פסקה אחרת, ארוכה יותר.\n\n\\[ x = 1 \\]"))
    assert fast and ids == ["0055"]


def test_code_figure_front_matter_and_boxes_are_not():
    for old, new in [("return 1", "return 2"), ("<svg class=\"figure\">a", "<svg class=\"figure\">b"),
                     ("title: x", "title: y"), ('data-m="3"', 'data-m="5"')]:
        assert not run(BASE.replace(old, new))[0], old


def test_other_files_and_new_pages_are_not():
    assert not text_only.verdict({"tools/x.py": ("a", "b")})[0]
    assert not text_only.verdict({"docs/javascripts/explorer/x.js": ("a", "b")})[0]
    assert not run(BASE, old=None)[0]


def test_ignored_files_alone_are_fast_with_no_pages():
    fast, ids, _ = text_only.verdict({"videos/0055/release/0055.mp4": (None, None), "notes/HANDOFF.md": (None, None)})
    assert fast and ids == []
