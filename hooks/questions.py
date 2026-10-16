"""MkDocs hook for the DV interview questions site.

Responsibilities:
- Validate the front matter of every question file (fails the build on errors).
- Build the navigation: one section per position level, questions sorted by id.
- Turn level / difficulty / topic fields into Material tags and a header card.
- Replace the ``<!-- questions-table -->`` placeholder with a filterable table (cards on phones).
- Append "related questions" (by shared tags) and an in-browser "run" panel to questions
  that have ``tests/<id>/demo.py``.
"""

from __future__ import annotations

import datetime as dt
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

LEVEL_DESC = {
    "student": "יסודות לוגיקה ספרתית, HDL בסיסי, מתמטיקה, הסתברות וחידות היגיון",
    "junior": "SystemVerilog, יסודות UVM, כתיבת טסטים ו-checkers, פרוטוקולים פשוטים",
    "senior": "ארכיטקטורת סביבת אימות, UVM מתקדם, SVA, סגירת כיסוי, דיבאג",
    "staff": "אסטרטגיית אימות, תכנון, מתודולוגיה והובלת צוות",
}

DIFFICULTIES = {
    "easy": "קל",
    "medium": "בינוני",
    "hard": "קשה",
}

NEW_DAYS = 30   # a question added within this many days of the build gets a "new" chip

# Tags that almost every question carries; they do not make two questions "related".
GENERIC_TAGS = {"python", "systemverilog"}
RELATED_MAX = 3

REQUIRED_FIELDS = ("id", "title", "level", "difficulty", "tags")
PLACEHOLDER = re.compile(r"<!--\s*questions-table(?:\s+level=(\w+))?\s*-->")
CARDS = re.compile(r"<!--\s*level-cards\s*-->")
STATS = re.compile(r"<!--\s*stats\s*-->")
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


def _is_new(q: dict) -> bool:
    added = q.get("added")
    if isinstance(added, dt.datetime):
        added = added.date()
    if not isinstance(added, dt.date):
        return False
    return (dt.date.today() - added).days <= NEW_DAYS


def new_chip(q: dict) -> str:
    return '<span class="chip chip-new">חדש</span>' if _is_new(q) else ""


def level_chip(level: str) -> str:
    return f'<span class="chip chip-level">{LEVELS[level]}</span>'


def difficulty_chip(difficulty: str) -> str:
    return f'<span class="chip chip-diff chip-diff-{difficulty}">{DIFFICULTIES[difficulty]}</span>'


def _tag_link(tag: str, base: str) -> str:
    href = posixpath.relpath("tags/", base or ".") + "/#tag:" + tag
    return f'<a href="{html.escape(href)}"><code>{html.escape(tag)}</code></a>'


def _header(q: dict, markdown: str, page_url: str) -> str:
    """Header card: id label, clean title, chips, topics, date and code badges."""
    base = posixpath.dirname(page_url) + "/" if page_url else ""
    langs = [name for name, fence in (("SystemVerilog", "systemverilog"), ("Python", "python"))
             if extract_code.blocks_from_text(markdown, fence)]
    topics = " ".join(_tag_link(t, base) for t in q["tags"])
    bottom = [f"<span>נושאים: {topics}</span>"]
    if q.get("added"):
        bottom.append(f'<span class="qh-sep"></span><span>נוסף {html.escape(str(q["added"]))}</span>')
    if q.get("source"):
        bottom.append(f'<span class="qh-sep"></span><span>מקור: {html.escape(str(q["source"]))}</span>')
    if langs:
        bottom.append(f'<span class="qh-sep"></span><span class="qh-badge">קוד: {" + ".join(langs)}</span>')
        if _has_tests(q):
            bottom.append('<span class="qh-badge qh-badge-ok">✓ נבדק אוטומטית</span>')
    return (
        '<div class="question-header">\n'
        f'<div class="qh-top"><span class="qh-id">שאלה {q["id"]}</span>'
        f'{level_chip(q["level"])}{difficulty_chip(q["difficulty"])}{new_chip(q)}</div>\n'
        f'<h1>{html.escape(str(q["title"]))}</h1>\n'
        f'<div class="qh-bottom">{"".join(bottom)}</div>\n'
        '</div>\n\n'
    )


def _tools() -> str:
    """Toolbar under the header: open / close every block, practice mode with a stopwatch."""
    return ('<div class="question-tools">'
            '<button type="button" class="qt-btn qt-open">פתח הכל</button>'
            '<button type="button" class="qt-btn qt-close">סגור הכל</button>'
            '<button type="button" class="qt-btn qt-practice">מצב תרגול</button>'
            '<span class="qt-clock" hidden></span>'
            '</div>\n\n')


def _has_tests(q: dict) -> bool:
    return (extract_code.ROOT / "tests" / q["id"]).exists()


def _level_cards(page_url: str) -> str:
    base = posixpath.dirname(page_url) + "/" if page_url else ""
    cards = []
    for level, label in LEVELS.items():
        qs = [q for q in _questions.values() if q["level"] == level]
        href = posixpath.relpath(f"{QUESTIONS_DIR}/{level}/", base or ".") + "/"
        counts = {d: sum(q["difficulty"] == d for q in qs) for d in DIFFICULTIES}
        diff = "".join(f'<span class="chip chip-diff chip-diff-{d}">{n} {DIFFICULTIES[d]}</span>'
                       for d, n in counts.items() if n)
        if not diff:
            diff = '<span class="lc-empty">עדיין אין שאלות ברמה הזו</span>'
        cards.append(
            f'<a class="level-card" href="{href}">'
            f'<div class="lc-head"><span class="lc-name">{label}</span>'
            f'<span class="lc-count">{len(qs)} שאלות</span></div>'
            f'<p class="lc-desc">{LEVEL_DESC[level]}</p>'
            f'<div class="lc-diff">{diff}</div></a>'
        )
    return '<div class="level-cards">' + "".join(cards) + "</div>"


def _stats() -> str:
    qs = list(_questions.values())
    with_code = sum(_has_tests(q) for q in qs)
    topics = {t for q in qs for t in q["tags"]}
    levels = sum(any(q["level"] == level for q in qs) for level in LEVELS)
    items = [(len(qs), "שאלות עם פתרון מלא"),
             (with_code, "שאלות עם קוד ב-SystemVerilog וב-Python, שנבדק אוטומטית"),
             (len(topics), "נושאים"),
             (f"{levels}/{len(LEVELS)}", "רמות משרה עם שאלות")]
    return ('<div class="stats-strip">'
            + "".join(f'<div class="stat"><b>{n}</b><span>{label}</span></div>' for n, label in items)
            + "</div>")


def _related(q: dict, page_url: str) -> str:
    """Up to RELATED_MAX other questions that share the most (non-generic) tags."""
    mine = set(q["tags"]) - GENERIC_TAGS
    base = posixpath.dirname(page_url) + "/" if page_url else ""
    scored = []
    for other in _questions.values():
        if other["id"] == q["id"]:
            continue
        shared = mine & set(other["tags"])
        if shared:
            same_level = other["level"] == q["level"]
            scored.append((-len(shared), not same_level, abs(int(other["id"]) - int(q["id"])), other))
    scored.sort(key=lambda t: t[:3])
    if not scored:
        return ""
    items = []
    for *_, other in scored[:RELATED_MAX]:
        href = posixpath.relpath(other["src_uri"][: -len(".md")] + "/", base or ".") + "/"
        items.append(
            f'<li><span class="rq-id">{other["id"]}</span>'
            f'<a class="rq-title" href="{href}">{html.escape(str(other["title"]))}</a>'
            f'{level_chip(other["level"])}{difficulty_chip(other["difficulty"])}</li>'
        )
    return "\n\n## שאלות קשורות\n\n<ul class=\"related-questions\">\n" + "\n".join(items) + "\n</ul>\n"


def _table(level: str | None, page_url: str) -> str:
    rows = sorted(
        (q for q in _questions.values() if level is None or q["level"] == level),
        key=lambda q: q["id"],
    )
    if not rows:
        return '<p class="questions-empty">עדיין אין שאלות בקטגוריה הזו.</p>'

    base = page_url if page_url.endswith("/") or not page_url else posixpath.dirname(page_url) + "/"
    tags = sorted({t for q in rows for t in q["tags"]})

    def group(name: str, label: str, values) -> str:
        chips = '<button type="button" class="filter-chip is-active" data-value="">הכל</button>'
        chips += "".join(
            f'<button type="button" class="filter-chip" data-value="{html.escape(v)}">{html.escape(l)}</button>'
            for v, l in values
        )
        return (f'<div class="filter-group" data-filter="{name}" data-value="">'
                f'<span class="filter-label">{label}</span>{chips}</div>')

    out = ['<div class="question-filter" markdown="0">']
    if level is None:
        out.append(group("level", "משרה", LEVELS.items()))
    out.append(group("difficulty", "קושי", DIFFICULTIES.items()))
    out.append(group("tag", "נושא", ((t, t) for t in tags)))
    out.append('<label class="filter-search">חיפוש '
               '<input type="search" data-filter="text" placeholder="חיפוש בכותרת"></label>')
    out.append("</div>")

    level_col = "<th>משרה</th>" if level is None else ""
    # The table itself has no class, so Material styles it and wraps it for scrolling
    out.append('<div class="questions-wrap"><table><thead><tr>'
               f"<th>#</th><th>שאלה</th>{level_col}<th>קושי</th><th>נושאים</th>"
               "</tr></thead><tbody>")
    for q in rows:
        target = q["src_uri"][: -len(".md")] + "/"
        href = posixpath.relpath(target, base or ".") + "/"
        level_td = f'<td class="q-level">{level_chip(q["level"])}</td>' if level is None else ""
        out.append(
            f'<tr data-level="{q["level"]}" data-difficulty="{q["difficulty"]}" '
            f'data-tags="{html.escape(" ".join(q["tags"]))}">'
            f'<td class="q-id">{q["id"]}</td>'
            f'<td class="q-title"><a href="{href}">{html.escape(str(q["title"]))}</a> {new_chip(q)}</td>'
            f"{level_td}"
            f'<td class="q-diff">{difficulty_chip(q["difficulty"])}</td>'
            f'<td class="q-tags">{" ".join(f"<code>{html.escape(t)}</code>" for t in q["tags"])}</td>'
            "</tr>"
        )
    out.append("</tbody></table></div>")
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
        page.meta["tags"] = [LEVELS[q["level"]], DIFFICULTIES[q["difficulty"]], *q["tags"]]
        page.meta.setdefault("hide", []).append("tags")   # the header card shows them
        markdown = (_header(q, markdown, page.url) + _tools() + markdown
                    + _run_panel(q, markdown) + _related(q, page.url))

    markdown = CARDS.sub(lambda m: _level_cards(page.url), markdown)
    markdown = STATS.sub(lambda m: _stats(), markdown)
    return PLACEHOLDER.sub(lambda m: _table(m.group(1), page.url), markdown)
