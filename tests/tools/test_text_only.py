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


def test_moving_a_closing_fence_is_not_prose():
    tabbed = BASE.replace("```python\ndef f():\n    return 1\n```", "=== \"Python\"\n\n    ```python\n    def f():\n        return 1\n    ```")
    assert run(tabbed, old=tabbed)[0]
    assert not run(tabbed.replace("\n    ```\n\n<div", "\n```\n\n<div"), old=tabbed)[0]


def test_a_file_moved_out_of_the_site_is_not_fast(tmp_path, monkeypatch):
    import subprocess
    g = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True).stdout
    g("init", "-q"); g("config", "user.email", "t@t"); g("config", "user.name", "t")
    (tmp_path / "docs/javascripts").mkdir(parents=True)
    (tmp_path / "docs/javascripts/py_run.py").write_text("x = 1\n")
    g("add", "-A"); g("commit", "-qm", "a"); base = g("rev-parse", "HEAD").strip()
    (tmp_path / "notes").mkdir()
    g("mv", "docs/javascripts/py_run.py", "notes/py_run.py"); g("commit", "-qm", "b"); head = g("rev-parse", "HEAD").strip()
    monkeypatch.chdir(tmp_path)
    out = subprocess.run([sys.executable, str(Path(text_only.__file__)), base, head], capture_output=True, text=True).stdout
    assert "text only: False" in out, out
