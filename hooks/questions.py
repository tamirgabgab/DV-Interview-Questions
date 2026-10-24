"""MkDocs hook for the DV interview questions site.

Responsibilities:
- Validate the front matter of every question file (fails the build on errors).
- Build the navigation: one section per position level, questions sorted by id.
- Turn level / difficulty / topic fields into Material tags and a header card.
- Replace the ``<!-- questions-table -->`` placeholder with a filterable table (cards on phones).
- Append "related questions" (by shared tags) and an in-browser "run" panel to questions
  that have ``tests/<id>/demo.py``.
- Study paths (``docs/paths/*.md``): validate the steps, add them to the navigation, render
  the step list and the path cards, and put a previous / next bar on every question of a path.
- Add the explorer scripts to the pages that have explorer boxes: the shared core and the
  file of each kind on the page (on_post_page).
- The home page's "continue" card and "recently added" strip, and the "what's new" page
  (``<!-- home-continue -->``, ``<!-- recent -->``, ``<!-- whats-new -->``).
- Add the prefix-stripped Hebrew words to the search index, and the id, level,
  difficulty and kind to the result of a question page (on_post_build).
"""

from __future__ import annotations

import datetime as dt
import html
import json
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from mkdocs.exceptions import PluginError
from mkdocs.utils.meta import get_data

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import extract_code  # noqa: E402

LEVELS = {
    "student": "סטודנט",
    "junior": "ג'וניור",
    "senior": "סניור",
}

LEVEL_DESC = {
    "student": "יסודות לוגיקה ספרתית, HDL בסיסי, מתמטיקה, הסתברות וחידות היגיון",
    "junior": "SystemVerilog, יסודות UVM, כתיבת טסטים ו-checkers, פרוטוקולים פשוטים",
    "senior": "ארכיטקטורת סביבת אימות, UVM מתקדם, SVA, סגירת כיסוי, דיבאג",
}

DIFFICULTIES = {
    "easy": "קל",
    "medium": "בינוני",
    "hard": "קשה",
}

# The kind of a question (front matter `kind:`), one per question: a filter group in the
# tables and a chip in the header card.
KINDS = {
    "puzzle": "חידה",
    "code": "קוד ואלגוריתם",
    "design": "תכן חומרה",
    "math": "מתמטיקה והוכחה",
    "dv": "אימות ופרוטוקולים",
}

NEW_DAYS = 30   # a question added within this many days of the build gets a "new" chip

# Tags that almost every question carries; they do not make two questions "related".
GENERIC_TAGS = {"python", "systemverilog"}
RELATED_MAX = 3

REQUIRED_FIELDS = ("id", "title", "level", "difficulty", "kind", "tags")
PLACEHOLDER = re.compile(r"<!--\s*questions-table(?:\s+level=(\w+))?\s*-->")
CARDS = re.compile(r"<!--\s*level-cards\s*-->")
STATS = re.compile(r"<!--\s*stats\s*-->")
PATH_STEPS = re.compile(r"<!--\s*path-steps\s*-->")
PATH_CARDS = re.compile(r"<!--\s*path-cards\s*-->")
CONTINUE = re.compile(r"<!--\s*home-continue\s*-->")
RECENT = re.compile(r"<!--\s*recent\s*-->")
WHATS_NEW = re.compile(r"<!--\s*whats-new\s*-->")
RECENT_MAX = 5
MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
QUESTIONS_DIR = "questions"
PATHS_DIR = "paths"
LEVEL_RANK = {level: i for i, level in enumerate(LEVELS)}
DIFF_RANK = {d: i for i, d in enumerate(DIFFICULTIES)}

# Hebrew search. The lunr index splits on whitespace only and has no Hebrew stemmer (the
# bundled lunr.he only rewrites final letters), so "טבלה" does not find "בטבלה" and
# "(לולאה" hides "לולאה". on_post_build adds a hidden field to every search document with
# the clean words and their forms without the prefix letters ו ה ב כ ל מ ש.
SEARCH_FIELD = "alt"
ID_FIELD = "qid"      # a question page's id, "0021 21", ranked above every other field
PREFIX_LETTERS = set("והבכלמש")
WORD = re.compile(r"[\u05d0-\u05ea]+|[A-Za-z0-9_]+")

# Explorer boxes: docs/javascripts/explorer/core.js and one file per kind, whose first line
# names the kinds it registers ("// kinds: cake-arith cake-geo").
EXPLORER_DIR = "javascripts/explorer"
EXPLORER_BOX = re.compile(r"<div\b[^>]*\bclass=\"explorer\"[^>]*>")
EXPLORER_KIND = re.compile(r"\bdata-kind=\"([\w-]+)\"")
KINDS_LINE = re.compile(r"^// kinds: ([\w -]+)$")
# The cost chips of a solution (A183): one comment line under its answer block,
# "<!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->", each chip a label word and a value.
COST_LINE = re.compile(r"^([ \t]*)<!--\s*cost:\s*(.+?)\s*-->[ \t]*$", re.M)

# Question metadata keyed by src_uri, and the study paths in order; filled in on_config.
_questions: dict[str, dict] = {}
_paths: list[dict] = []
_comments: dict = {}
_kind_files: dict[str, str] = {}   # explorer kind -> its file name in EXPLORER_DIR


def _load_questions(docs_dir: Path) -> dict[str, dict]:
    questions: dict[str, dict] = {}
    errors: list[str] = []
    seen_ids: dict[str, str] = {}

    for path in sorted((docs_dir / QUESTIONS_DIR).glob("*/*.md")):
        if path.name == "index.md":
            continue
        src_uri = path.relative_to(docs_dir).as_posix()
        body, meta = get_data(path.read_text(encoding="utf-8"))

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
        if meta["kind"] not in KINDS:
            errors.append(f"{src_uri}: unknown kind '{meta['kind']}' (one of {', '.join(KINDS)})")
        if not isinstance(meta["tags"], list):
            errors.append(f"{src_uri}: 'tags' must be a list")
        if not path.name.startswith(qid + "-"):
            errors.append(f"{src_uri}: file name must start with '{qid}-'")
        if qid in seen_ids:
            errors.append(f"{src_uri}: duplicate id {qid} (also in {seen_ids[qid]})")
        seen_ids[qid] = src_uri

        has_code = any(extract_code.blocks_from_text(body, f) for f in ("systemverilog", "python"))
        interactive = 'class="explorer"' in body or 'class="stepper"' in body or "<iframe" in body
        questions[src_uri] = {**meta, "id": qid, "src_uri": src_uri, "has_code": has_code,
                              "interactive": interactive}

    if errors:
        raise PluginError("Invalid question files:\n  " + "\n  ".join(errors))
    return questions


def _load_paths(docs_dir: Path) -> list[dict]:
    by_id = {q["id"]: q for q in _questions.values()}
    paths, errors = [], []
    for path in sorted((docs_dir / PATHS_DIR).glob("*.md")):
        if path.name == "index.md":
            continue
        src_uri = path.relative_to(docs_dir).as_posix()
        _, meta = get_data(path.read_text(encoding="utf-8"))
        steps = []
        for step in meta.get("steps") or []:
            qid = f"{int(step['id']):04d}"
            if qid not in by_id:
                errors.append(f"{src_uri}: step {qid} is not a question")
                continue
            steps.append({"q": by_id[qid], "note": str(step.get("note", ""))})
        if not meta.get("title") or len(steps) < 2:
            errors.append(f"{src_uri}: a path needs a title and at least two steps")
        paths.append({"src_uri": src_uri, "title": str(meta.get("title", "")),
                      "description": str(meta.get("description", "")),
                      "order": meta.get("order", 99), "steps": steps})
    if errors:
        raise PluginError("Invalid study paths:\n  " + "\n  ".join(errors))
    return sorted(paths, key=lambda p: (p["order"], p["src_uri"]))


def _load_kind_files(docs_dir: Path) -> dict[str, str]:
    """Map every explorer kind to the file that registers it (its "// kinds:" first line)."""
    kinds: dict[str, str] = {}
    for path in sorted((docs_dir / EXPLORER_DIR).glob("*.js")):
        if path.name == "core.js":
            continue
        first = path.read_text(encoding="utf-8").split("\n", 1)[0]
        m = KINDS_LINE.match(first)
        if not m:
            raise PluginError(f"{EXPLORER_DIR}/{path.name}: the first line must be '// kinds: <kind> ...'")
        for kind in m.group(1).split():
            if kind in kinds:
                raise PluginError(f"explorer kind {kind!r} is registered by {kinds[kind]} and {path.name}")
            kinds[kind] = path.name
    return kinds


def on_config(config, **kwargs):
    global _questions, _paths, _comments, _kind_files
    _questions = _load_questions(Path(config["docs_dir"]))
    _paths = _load_paths(Path(config["docs_dir"]))
    _comments = dict(config["extra"].get("comments") or {})
    _kind_files = _load_kind_files(Path(config["docs_dir"]))

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
    if _paths:
        nav.append({"מסלולים": [f"{PATHS_DIR}/index.md"]
                    + [{p["title"]: p["src_uri"]} for p in _paths]})
    nav.append({"תגיות": "tags.md"})
    nav.append({"מה חדש": "new.md"})
    config["nav"] = nav
    # the "what's new" page linked from the footer of every page (an absolute path, since
    # the footer is the same on pages at every depth)
    root = urlparse(config.get("site_url") or "/").path or "/"
    config["copyright"] = (config.get("copyright") or "") + f' &middot; <a href="{root.rstrip("/")}/new/">מה חדש</a>'
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


def kind_icon(kind: str) -> str:
    return f'<i class="kind-ico kind-ico-{kind}" aria-hidden="true"></i>'


def kind_chip(kind: str) -> str:
    return f'<span class="chip chip-kind chip-kind-{kind}">{kind_icon(kind)}{KINDS[kind]}</span>'


def interactive_chip(q: dict) -> str:
    """A chip on pages with an explorer, a step figure or an embedded tool."""
    return ('<span class="chip chip-interactive" title="יש בדף ממשק אינטראקטיבי : סליידרים, אנימציה או איור צעד-צעד">אינטראקטיבי</span>'
            if q.get("interactive") else "")


def _base(page_url: str) -> str:
    """Directory of a page URL, for relative links (page URLs end with '/')."""
    return page_url if page_url.endswith("/") or not page_url else posixpath.dirname(page_url) + "/"


def _href(src_uri: str, page_url: str) -> str:
    """Relative link from the page at page_url to the page built from src_uri."""
    target = src_uri[: -len(".md")] + "/"
    if target.endswith("/index/"):
        target = target[: -len("index/")]
    return posixpath.relpath(target or ".", _base(page_url) or ".") + "/"


def _tag_link(tag: str, base: str) -> str:
    href = posixpath.relpath("tags/", base or ".") + "/#tag:" + tag
    return f'<a href="{html.escape(href)}"><code>{html.escape(tag)}</code></a>'


def _header(q: dict, markdown: str, page_url: str) -> str:
    """Header card: id label, clean title, chips, topics, date and code badges."""
    base = posixpath.dirname(page_url) + "/" if page_url else ""
    langs = [name for name, fence in (("SystemVerilog", "systemverilog"), ("Python", "python"))
             if extract_code.blocks_from_text(markdown, fence)]
    topics = " ".join(_tag_link(t, base) for t in q["tags"])
    bottom = [f"<span>נושאים : {topics}</span>"]
    if q.get("added"):
        bottom.append(f'<span class="qh-sep"></span><span>נוסף {html.escape(str(q["added"]))}</span>')
    if q.get("source"):
        bottom.append(f'<span class="qh-sep"></span><span>מקור : {html.escape(str(q["source"]))}</span>')
    if langs:
        bottom.append(f'<span class="qh-sep"></span><span class="qh-badge">קוד : {" + ".join(langs)}</span>')
        if _has_tests(q):
            bottom.append('<span class="qh-badge qh-badge-ok">✓ נבדק אוטומטית</span>')
    return (
        '<div class="question-header">\n'
        f'<div class="qh-top"><span class="qh-id">שאלה {q["id"]}</span>'
        f'{level_chip(q["level"])}{difficulty_chip(q["difficulty"])}{kind_chip(q["kind"])}{interactive_chip(q)}{new_chip(q)}</div>\n'
        f'<h1>{html.escape(str(q["title"]))}</h1>\n'
        f'<div class="qh-bottom">{"".join(bottom)}</div>\n'
        '</div>\n\n'
    )


def _tools(q: dict, page_url: str) -> str:
    """Toolbar under the header: open / close every block, practice mode with a stopwatch,
    solved / favourite marks (kept in the browser) and a random question of the same level."""
    others = [o for o in _questions.values() if o["id"] != q["id"]]
    same = [o for o in others if o["level"] == q["level"]] or others
    random_btn = ""
    if same:
        hrefs = json.dumps([_href(o["src_uri"], page_url) for o in sorted(same, key=lambda o: o["id"])])
        random_btn = (f'<button type="button" class="qt-btn qt-random" data-hrefs="{html.escape(hrefs)}" '
                      'title="שאלה אקראית מאותה רמה">שאלה אקראית</button>')
    return (f'<div class="question-tools" role="toolbar" aria-label="כלי השאלה" data-search-exclude data-qid="{q["id"]}">'
            '<button type="button" class="qt-btn qt-open">פתח הכל</button>'
            '<button type="button" class="qt-btn qt-close">סגור הכל</button>'
            '<button type="button" class="qt-btn qt-practice">מצב תרגול</button>'
            '<span class="qt-clock" hidden></span>'
            '<span class="qt-spacer"></span>'
            '<button type="button" class="qt-btn qt-mark qt-solved" data-mark="solved" aria-pressed="false">✓ פתרתי</button>'
            '<button type="button" class="qt-btn qt-mark qt-star" data-mark="star" aria-pressed="false">☆ מועדף</button>'
            f'{random_btn}'
            '</div>\n\n')


def _progress(ids) -> str:
    """Placeholder for the "solved n of m" bar; marks.js fills it from the browser's marks."""
    return (f'<div class="mark-progress" data-ids="{" ".join(ids)}" hidden>'
            '<span class="mp-bar"><i></i></span><span class="mp-text"></span></div>')


def _path_nav(q: dict, page_url: str) -> str:
    """One line per study path that contains the question: step n of m, previous and next."""
    lines = []
    for p in _paths:
        ids = [s["q"]["id"] for s in p["steps"]]
        if q["id"] not in ids:
            continue
        i = ids.index(q["id"])
        parts = [f'<span class="pn-path">מסלול <a href="{_href(p["src_uri"], page_url)}">{html.escape(p["title"])}</a></span>'
                 f'<span class="pn-step">שלב {i + 1} מתוך {len(ids)}</span>']
        for label, cls, k in (("הקודם", "pn-prev", i - 1), ("הבא", "pn-next", i + 1)):
            if 0 <= k < len(ids):
                other = p["steps"][k]["q"]
                parts.append(f'<a class="{cls}" href="{_href(other["src_uri"], page_url)}" '
                             f'title="{html.escape(str(other["title"]))}">{label} : <span class="pn-id">{other["id"]}</span></a>')
        lines.append('<div class="path-nav-line">' + "".join(parts) + "</div>")
    if not lines:
        return ""
    return '<div class="path-nav" data-search-exclude>' + "".join(lines) + "</div>\n\n"


def _inline_code(text: str) -> str:
    """Escape a note and turn `x` into <code>x</code> (keeps "f()" from being mirrored)."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text))


def _path_steps(page) -> str:
    p = next((p for p in _paths if p["src_uri"] == page.file.src_uri), None)
    if p is None:
        return ""
    items = []
    for n, s in enumerate(p["steps"], 1):
        q = s["q"]
        items.append(
            f'<li class="path-step" data-id="{q["id"]}"><span class="ps-num">{n}</span>'
            f'<div class="ps-body"><div class="ps-head"><span class="ps-id">{q["id"]}</span>'
            f'<a class="ps-title" href="{_href(q["src_uri"], page.url)}">{html.escape(str(q["title"]))}</a>'
            f'{level_chip(q["level"])}{difficulty_chip(q["difficulty"])}<span class="ps-mark"></span></div>'
            f'<p class="ps-note">{_inline_code(s["note"])}</p></div></li>')
    ids = [s["q"]["id"] for s in p["steps"]]
    return _progress(ids) + '<ol class="path-steps">' + "".join(items) + "</ol>"


def _path_cards(page_url: str) -> str:
    cards = []
    for p in _paths:
        ids = [s["q"]["id"] for s in p["steps"]]
        kinds = [s["q"]["kind"] for s in p["steps"]]
        kind = max(KINDS, key=kinds.count)            # the kind most of its questions have
        cards.append(
            f'<a class="level-card path-card" href="{_href(p["src_uri"], page_url)}">'
            f'<div class="lc-head"><span class="lc-name">{kind_icon(kind)}{html.escape(p["title"])}</span>'
            f'<span class="lc-count">{len(ids)} שאלות</span></div>'
            f'<p class="lc-desc">{html.escape(p["description"])}</p>'
            f'<div class="lc-diff"><span class="pc-ids">{" · ".join(ids)}</span></div>'
            f'{_progress(ids)}</a>')
    return '<div class="level-cards">' + "".join(cards) + "</div>"


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
            f'<div class="lc-diff">{diff}</div>'
            f'{_progress(sorted(q["id"] for q in qs)) if qs else ""}</a>'
        )
    return '<div class="level-cards">' + "".join(cards) + "</div>"


def _stats() -> str:
    qs = list(_questions.values())
    with_code = sum(q["has_code"] and _has_tests(q) for q in qs)   # a page may have tests but no code
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


def _added(q: dict) -> dt.date | None:
    added = q.get("added")
    if isinstance(added, dt.datetime):
        added = added.date()
    return added if isinstance(added, dt.date) else None


def _by_added() -> list[dict]:
    """The questions with an added date, the newest first (a later id first on one day)."""
    return sorted((q for q in _questions.values() if _added(q)), key=lambda q: (_added(q), q["id"]), reverse=True)


def _date_he(d: dt.date) -> str:
    return f"{d.day} ב{MONTHS[d.month - 1]} {d.year}"


def _question_item(q: dict, page_url: str) -> str:
    return (f'<li><span class="rq-id">{q["id"]}</span>'
            f'<a class="rq-title" href="{_href(q["src_uri"], page_url)}">{html.escape(str(q["title"]))}</a>'
            f'{level_chip(q["level"])}{difficulty_chip(q["difficulty"])}{kind_chip(q["kind"])}</li>')


def _continue_card() -> str:
    """Filled by marks.js from the last question this browser opened; hidden until then."""
    return '<div class="continue-card" hidden data-search-exclude></div>'


def _recent(page_url: str) -> str:
    qs = _by_added()[:RECENT_MAX]
    if not qs:
        return ""
    href = posixpath.relpath("new/", _base(page_url) or ".") + "/"
    return ('<ul class="related-questions recent-questions">\n' + "\n".join(_question_item(q, page_url) for q in qs)
            + f'\n</ul>\n<p class="recent-more"><a href="{href}">כל השאלות לפי תאריך ההוספה</a></p>')


def _whats_new(page_url: str) -> str:
    """Every question by the day it was added, the newest day first."""
    out, day = [], None
    for q in _by_added():
        if _added(q) != day:
            if day is not None:
                out.append("</ul>")
            day = _added(q)
            n = sum(_added(o) == day for o in _questions.values())
            out.append(f'<h2 class="new-day" id="d{day.isoformat()}">\u200f{_date_he(day)}'
                       f'<span class="new-count">{n} {"שאלה" if n == 1 else "שאלות"}</span></h2>\n<ul class="related-questions">')
        out.append(_question_item(q, page_url))
    if out:
        out.append("</ul>")
    return "\n".join(out)


def _table(level: str | None, page_url: str) -> str:
    rows = sorted(
        (q for q in _questions.values() if level is None or q["level"] == level),
        key=lambda q: q["id"],
    )
    if not rows:
        return '<p class="questions-empty">עדיין אין שאלות בקטגוריה הזו.</p>'

    tags = sorted({t for q in rows for t in q["tags"]})

    def group(name: str, label: str, values) -> str:
        chips = '<button type="button" class="filter-chip is-active" data-value="">הכל</button>'
        chips += "".join(
            f'<button type="button" class="filter-chip" data-value="{html.escape(v)}">'
            f'{kind_icon(v) if name == "kind" else ""}{html.escape(l)}</button>'
            for v, l in values
        )
        return (f'<div class="filter-group" data-filter="{name}" data-value="">'
                f'<span class="filter-label">{label}</span>{chips}</div>')

    out = ['<div class="question-filter" markdown="0" data-search-exclude>']
    if level is None:
        out.append(group("level", "משרה", LEVELS.items()))
    out.append(group("difficulty", "קושי", DIFFICULTIES.items()))
    out.append(group("kind", "סוג", [(k, v) for k, v in KINDS.items() if any(q["kind"] == k for q in rows)]))
    out.append(group("tag", "נושא", ((t, t) for t in tags)))
    out.append(group("mark", "סימון", [("star", "מועדפים"), ("solved", "פתורות"), ("unsolved", "לא פתורות")]))
    out.append(group("interactive", "ממשק", [("1", "אינטראקטיביות")]))
    sorts = [("id", "מספר"), ("title", "שם")] + ([("level", "משרה")] if level is None else []) + [("difficulty", "קושי")]
    out.append('<div class="filter-tools">'
               '<label class="filter-search">חיפוש '
               '<input type="search" data-filter="text" placeholder="חיפוש בכותרת"></label>'
               '<label class="filter-sort">מיון <select>'
               + "".join(f'<option value="{k}">{l}</option>' for k, l in sorts)
               + '</select></label>'
               '<button type="button" class="filter-random">שאלה אקראית</button></div>')
    out.append("</div>")

    def th(key: str | None, label: str) -> str:
        if key is None:
            return f"<th>{label}</th>"
        return f'<th data-sort="{key}"><button type="button" class="th-sort">{label}</button></th>'

    level_col = th("level", "משרה") if level is None else ""
    # The table itself has no class, so Material styles it and wraps it for scrolling
    out.append('<div class="questions-wrap"><table><thead><tr>'
               f'{th("id", "#")}{th("title", "שאלה")}{level_col}{th("difficulty", "קושי")}{th(None, "נושאים")}'
               "</tr></thead><tbody>")
    for q in rows:
        href = _href(q["src_uri"], page_url)
        level_td = f'<td class="q-level">{level_chip(q["level"])}</td>' if level is None else ""
        interactive_mark = '<span class="q-interactive" title="עם ממשק אינטראקטיבי">▶</span>' if q.get("interactive") else ""
        out.append(
            f'<tr data-id="{q["id"]}" data-level="{q["level"]}" data-difficulty="{q["difficulty"]}" data-kind="{q["kind"]}" '
            f'data-level-rank="{LEVEL_RANK[q["level"]]}" data-diff-rank="{DIFF_RANK[q["difficulty"]]}" '
            f'data-tags="{html.escape(" ".join(q["tags"]))}" data-interactive="{int(bool(q.get("interactive")))}">'
            f'<td class="q-id">{q["id"]}</td>'
            f'<td class="q-title"><a href="{href}">{html.escape(str(q["title"]))}</a> {new_chip(q)}{interactive_mark}'
            '<span class="q-marks"></span></td>'
            f"{level_td}"
            f'<td class="q-diff">{difficulty_chip(q["difficulty"])}{kind_chip(q["kind"])}</td>'
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
<textarea class="py-editor" aria-label="הקוד להרצה (Python)" spellcheck="false" dir="ltr" rows="{min(max(demo_code.count(chr(10)) + 1, 6), 22)}">{html.escape(demo_code)}</textarea>
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


def _comments_block() -> str:
    """The giscus comments section (GitHub Discussions), or "" until the repository and
    category ids are set in mkdocs.yml (extra.comments)."""
    c = _comments
    if not (c.get("repo") and c.get("repo_id") and c.get("category_id")):
        return ""
    attrs = {"data-repo": c["repo"], "data-repo-id": c["repo_id"], "data-category": c.get("category", ""),
             "data-category-id": c["category_id"], "data-mapping": "pathname", "data-strict": "1",
             "data-reactions-enabled": "1", "data-emit-metadata": "0", "data-input-position": "top",
             "data-theme": "preferred_color_scheme", "data-lang": "he", "data-loading": "lazy"}
    attr_text = " ".join(f'{k}="{html.escape(v)}"' for k, v in attrs.items())
    return ("\n\n## דיון\n\n"
            '<p class="comments-note">שאלות, תיקונים ופתרונות אחרים : הדיון נשמר ב-GitHub Discussions של המאגר, '
            "וכדי לכתוב צריך להתחבר עם חשבון GitHub.</p>\n"
            f'<div class="comments"><script src="https://giscus.app/client.js" {attr_text} crossorigin="anonymous" async></script></div>\n')


def _cost_chip(text: str) -> str:
    """One chip: the label in bold, then the value (arithmatex wraps its \\( \\) math)."""
    label, _, value = text.strip().partition(" ")
    return f'<span class="cost-chip"><b>{html.escape(label)}</b> {html.escape(value.strip())}</span>'


def _cost_chips(m: re.Match) -> str:
    """A cost comment line as a row of chips, at the indentation of the comment."""
    chips = "".join(_cost_chip(c) for c in m.group(2).split(" | "))
    return f'{m.group(1)}<div class="cost-chips" role="note" aria-label="סיבוכיות" data-search-exclude>{chips}</div>'


def on_page_markdown(markdown, page, config, files, **kwargs):
    q = _questions.get(page.file.src_uri)
    if q:
        page.meta["tags"] = [LEVELS[q["level"]], DIFFICULTIES[q["difficulty"]], *q["tags"]]
        page.meta.setdefault("hide", []).append("tags")   # the header card shows them
        markdown = (_header(q, markdown, page.url) + _tools(q, page.url) + _path_nav(q, page.url) + markdown
                    + _run_panel(q, markdown) + _related(q, page.url) + _comments_block())

    markdown = COST_LINE.sub(_cost_chips, markdown)
    markdown = CARDS.sub(lambda m: _level_cards(page.url), markdown)
    markdown = STATS.sub(lambda m: _stats(), markdown)
    markdown = PATH_STEPS.sub(lambda m: _path_steps(page), markdown)
    markdown = PATH_CARDS.sub(lambda m: _path_cards(page.url), markdown)
    markdown = CONTINUE.sub(lambda m: _continue_card(), markdown)
    markdown = RECENT.sub(lambda m: _recent(page.url), markdown)
    markdown = WHATS_NEW.sub(lambda m: _whats_new(page.url), markdown)
    return PLACEHOLDER.sub(lambda m: _table(m.group(1), page.url), markdown)


def explorer_scripts(output: str, page_url: str) -> str:
    """The script tags for the explorer boxes in a built page: the core, then the file of
    every kind on the page (each once), or "" when the page has no box."""
    files: list[str] = []
    for tag in EXPLORER_BOX.findall(output):
        m = EXPLORER_KIND.search(tag)
        if not m:
            raise PluginError(f"{page_url}: an explorer box without data-kind: {tag[:80]}")
        kind = m.group(1)
        if kind not in _kind_files:
            raise PluginError(f"{page_url}: no file in docs/{EXPLORER_DIR}/ registers the explorer kind {kind!r}")
        if _kind_files[kind] not in files:
            files.append(_kind_files[kind])
    if not files:
        return ""
    base = _base(page_url) or "."
    return "".join(f'<script src="{posixpath.relpath(f"{EXPLORER_DIR}/{name}", base)}"></script>'
                   for name in ["core.js", *files])


def on_post_page(output, page, config, **kwargs):
    scripts = explorer_scripts(output, page.url)
    if not scripts:
        return output
    at = output.rfind("</body>")
    return output[:at] + scripts + output[at:] if at >= 0 else output + scripts


def _search_variants(raw_tokens: set[str], words: list[str], known: set[str]) -> set[str]:
    """Clean words that differ from the raw index tokens, and Hebrew words without their
    prefix letters: one letter always (when 3+ letters remain), two or three letters only
    when the rest is a word that appears somewhere on the site."""
    out = set()
    for w in words:
        out.add(w.lower())
        if not ("\u05d0" <= w[0] <= "\u05ea"):
            continue
        for k in (1, 2, 3):
            if len(w) - k < 3 or w[k - 1] not in PREFIX_LETTERS:
                break
            rest = w[k:]
            if k == 1 or rest in known:
                out.add(rest)
    return out - raw_tokens


def _search_question(doc: dict, q: dict) -> None:
    """A question page in the search results (E33): the id before the title (so "0021"
    ranks it first), the kind beside the level and difficulty in its tags (the results
    show them as chips under the title, with the topics), no text instead of the header
    card's run-together chips, and the id as written and without its zeros ("0021 21") in
    its own field."""
    doc["title"] = f'{q["id"]} · {q["title"]}'
    doc["tags"] = [LEVELS[q["level"]], DIFFICULTIES[q["difficulty"]], KINDS[q["kind"]],
                   *[t for t in doc.get("tags", []) if t not in (LEVELS[q["level"]], DIFFICULTIES[q["difficulty"]])]]
    doc["text"] = ""   # the tags, shown as chips under the title, are the topics already
    doc[ID_FIELD] = f'{q["id"]} {int(q["id"])}'


def on_post_build(config, **kwargs):
    path = Path(config["site_dir"]) / "search" / "search_index.json"
    if not path.exists():
        return
    index = json.loads(path.read_text(encoding="utf-8"))
    sep = re.compile(index["config"].get("separator") or r"[\s\-]+")
    texts = []
    for doc in index["docs"]:
        plain = re.sub(r"<[^>]+>", " ", doc.get("title", "") + " " + doc.get("text", ""))
        texts.append((set(t.lower() for t in sep.split(plain) if t), WORD.findall(plain)))
    known = {w for _, words in texts for w in words}
    for doc, (raw, words) in zip(index["docs"], texts):
        extra = _search_variants(raw, words, known)
        if extra:
            doc[SEARCH_FIELD] = " ".join(sorted(extra))
    pages = {q["src_uri"][: -len(".md")] + "/": q for q in _questions.values()}
    for doc in index["docs"]:
        if doc["location"] in pages:
            _search_question(doc, pages[doc["location"]])
    index["config"]["fields"][SEARCH_FIELD] = {"boost": 1.0}
    index["config"]["fields"][ID_FIELD] = {"boost": 1e7}
    path.write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
