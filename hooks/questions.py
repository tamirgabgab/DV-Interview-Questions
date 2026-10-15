"""MkDocs hook for the DV interview questions site.

Responsibilities:
- Validate the front matter of every question file (fails the build on errors).
- Build the navigation: one section per position level, questions sorted by id.
- Turn level / difficulty / topic fields into Material tags and a badge line.
- Replace the ``<!-- questions-table -->`` placeholder with a filterable table.
- Append an in-browser "run" panel to questions that have ``tests/<id>/demo.py``.
"""

from __future__ import annotations

import html
import json
import posixpath
import re
import sys
from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.utils.meta import get_data

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import extract_code  # noqa: E402

LEVELS = {
    "student": "סטודנט",
    "junior": "ג'וניור",
    "senior": "סניור",
    "staff": "סטאף",
}

DIFFICULTIES = {
    "easy": ("קל", "🟢"),
    "medium": ("בינוני", "🟡"),
    "hard": ("קשה", "🔴"),
}

REQUIRED_FIELDS = ("id", "title", "level", "difficulty", "tags")
PLACEHOLDER = re.compile(r"<!--\s*questions-table(?:\s+level=(\w+))?\s*-->")
QUESTIONS_DIR = "questions"

# Question metadata keyed by src_uri, filled in on_config.
_questions: dict[str, dict] = {}


def _load_questions(docs_dir: Path) -> dict[str, dict]:
    questions: dict[str, dict] = {}
    errors: list[str] = []
    seen_ids: dict[str, str] = {}

    for path in sorted((docs_dir / QUESTIONS_DIR).glob("*/*.md")):
        if path.name == "index.md":
            continue
        src_uri = path.relative_to(docs_dir).as_posix()
        _, meta = get_data(path.read_text(encoding="utf-8"))

        missing = [f for f in REQUIRED_FIELDS if f not in meta]
        if missing:
            errors.append(f"{src_uri}: missing front-matter fields {missing}")
            continue

        qid = f"{int(meta['id']):04d}"
        level = meta["level"]
        folder = path.parent.name
        if level not in LEVELS:
            errors.append(f"{src_uri}: unknown level '{level}'")
        elif level != folder:
            errors.append(f"{src_uri}: level '{level}' does not match folder '{folder}'")
        if meta["difficulty"] not in DIFFICULTIES:
            errors.append(f"{src_uri}: unknown difficulty '{meta['difficulty']}'")
        if not isinstance(meta["tags"], list):
            errors.append(f"{src_uri}: 'tags' must be a list")
        if not path.name.startswith(qid + "-"):
            errors.append(f"{src_uri}: file name must start with '{qid}-'")
        if qid in seen_ids:
            errors.append(f"{src_uri}: duplicate id {qid} (also in {seen_ids[qid]})")
        seen_ids[qid] = src_uri

        questions[src_uri] = {**meta, "id": qid, "src_uri": src_uri}

    if errors:
        raise PluginError("Invalid question files:\n  " + "\n  ".join(errors))
    return questions


def on_config(config, **kwargs):
    global _questions
    _questions = _load_questions(Path(config["docs_dir"]))

    nav: list = [{"ראשי": "index.md"}]
    for level, label in LEVELS.items():
        pages = sorted(
            (q for q in _questions.values() if q["level"] == level),
            key=lambda q: q["id"],
        )
        nav.append(
            {label: [f"{QUESTIONS_DIR}/{level}/index.md"]
             + [{f"{q['id']} · {q['title']}": q["src_uri"]} for q in pages]}
        )
    nav.append({"תגיות": "tags.md"})
    config["nav"] = nav
    return config


def _badges(q: dict) -> str:
    diff_label, diff_icon = DIFFICULTIES[q["difficulty"]]
    topics = " ".join(f"`{t}`" for t in q["tags"])
    return (
        f'<div class="question-meta" markdown>\n'
        f"**מס' שאלה:** {q['id']} &nbsp;|&nbsp; "
        f"**משרה:** {LEVELS[q['level']]} &nbsp;|&nbsp; "
        f"**קושי:** {diff_icon} {diff_label} &nbsp;|&nbsp; "
        f"**נושאים:** {topics}\n"
        f"</div>\n\n"
    )


def _table(level: str | None, page_url: str) -> str:
    rows = sorted(
        (q for q in _questions.values() if level is None or q["level"] == level),
        key=lambda q: q["id"],
    )
    if not rows:
        return '<p class="questions-empty">עדיין אין שאלות בקטגוריה הזו.</p>'

    base = page_url if page_url.endswith("/") or not page_url else posixpath.dirname(page_url) + "/"
    tags = sorted({t for q in rows for t in q["tags"]})

    def options(values):
        return "".join(f'<option value="{html.escape(v)}">{html.escape(l)}</option>' for v, l in values)

    out = ['<div class="question-filter" markdown="0">']
    if level is None:
        out.append(
            '<label>משרה <select data-filter="level"><option value="">הכל</option>'
            + options(LEVELS.items()) + "</select></label>"
        )
    out.append(
        '<label>קושי <select data-filter="difficulty"><option value="">הכל</option>'
        + options((k, f"{v[1]} {v[0]}") for k, v in DIFFICULTIES.items()) + "</select></label>"
    )
    out.append(
        '<label>נושא <select data-filter="tag"><option value="">הכל</option>'
        + options((t, t) for t in tags) + "</select></label>"
    )
    out.append('<label>חיפוש <input type="search" data-filter="text" placeholder="חיפוש בכותרת"></label>')
    out.append("</div>")

    out.append('<table><thead><tr>'
               "<th>#</th><th>שאלה</th><th>משרה</th><th>קושי</th><th>נושאים</th>"
               "</tr></thead><tbody>")
    for q in rows:
        target = q["src_uri"][: -len(".md")] + "/"
        href = posixpath.relpath(target, base or ".") + "/"
        diff_label, diff_icon = DIFFICULTIES[q["difficulty"]]
        out.append(
            f'<tr data-level="{q["level"]}" data-difficulty="{q["difficulty"]}" '
            f'data-tags="{html.escape(" ".join(q["tags"]))}">'
            f"<td>{q['id']}</td>"
            f'<td><a href="{href}">{html.escape(str(q["title"]))}</a></td>'
            f"<td>{LEVELS[q['level']]}</td>"
            f"<td>{diff_icon} {diff_label}</td>"
            f"<td>{' '.join(f'<code>{html.escape(t)}</code>' for t in q['tags'])}</td>"
            "</tr>"
        )
    out.append("</tbody></table>")
    out.append('<p class="questions-count"></p>')
    return "\n".join(out)


def _run_panel(q: dict, markdown: str) -> str:
    """HTML for the in-browser Python runner, or "" when the question has no demo."""
    tests = extract_code.ROOT / "tests" / q["id"]
    demo = tests / "demo.py"
    if not demo.exists():
        return ""
    page_code = "\n".join(extract_code.blocks_from_text(markdown, "python"))
    demo_code = demo.read_text(encoding="utf-8")

    sv_note = ""
    tb = tests / "tb.sv"
    if tb.exists():
        translated = "//@translation-of" in tb.read_text(encoding="utf-8")
        sv_note = ("<p class=\"py-runner-note\">קוד ה-SystemVerilog בשאלה נבדק אוטומטית ב-Verilator "
                   "בכל עדכון של האתר"
                   + (" (בגרסת בדיקה שמותאמת למגבלות הסימולטור)" if translated else "")
                   + ".</p>")

    return f"""

## הרצה בדפדפן

<details class="example py-runner">
<summary>▶ הרצת קוד ה-Python של השאלה</summary>
<p class="py-runner-note">הפונקציות מהפתרון כבר טעונות. אפשר לשנות את הקוד שבתיבה ולהריץ שוב.
ההרצה הראשונה טוענת את Python לדפדפן ולוקחת כמה שניות.</p>
<script type="application/json" class="py-page-code">{json.dumps(page_code).replace("</", "<\\/")}</script>
<textarea class="py-editor" spellcheck="false" dir="ltr" rows="{min(max(demo_code.count(chr(10)) + 1, 6), 22)}">{html.escape(demo_code)}</textarea>
<div class="py-buttons">
<button type="button" class="md-button md-button--primary py-run">▶ הרץ</button>
<button type="button" class="md-button py-stop" disabled>עצור</button>
<button type="button" class="md-button py-reset">איפוס</button>
<span class="py-status"></span>
</div>
<pre class="py-output" dir="ltr"></pre>
{sv_note}
</details>
"""


def on_page_markdown(markdown, page, config, files, **kwargs):
    q = _questions.get(page.file.src_uri)
    if q:
        diff_label, _ = DIFFICULTIES[q["difficulty"]]
        page.meta["tags"] = [LEVELS[q["level"]], diff_label, *q["tags"]]
        markdown = _badges(q) + markdown + _run_panel(q, markdown)

    return PLACEHOLDER.sub(lambda m: _table(m.group(1), page.url), markdown)
