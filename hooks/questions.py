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
- Keep only the questions in the search index, each with its statement and its parts'
  statements (math in plain symbols, tools/search_text.py), and add the prefix-stripped
  Hebrew words, and the id, level, difficulty and kind to the result of a question page
  (on_post_build).
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
from search_text import STATEMENT, statement_sections  # noqa: E402

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

NEW_DAYS = 7    # a question added within this many days of the build gets a "new" chip,
NEW_MAX = 5     # and at most this many (the newest), so the chip stays rare (UI322)

# The topics (front matter `tags:`) as the site shows them (UI322): Hebrew, or the term as
# DV engineers say it. The tag itself stays in the files, the URLs and the anchors; a tag
# without a name here shows as written, and `tools/lint_pages.py` warns about it.
TOPICS = {
    "algorithms": "אלגוריתמים",
    "assertions": "Assertions",
    "bfs": "BFS",
    "bitwise": "פעולות על ביטים",
    "cdc": "CDC",
    "clocks": "שעונים",
    "combinatorics": "קומבינטוריקה",
    "constraints": "אילוצים",
    "coverage": "כיסוי",
    "digital-design": "תכן דיגיטלי",
    "digital-logic": "לוגיקה ספרתית",
    "digits": "ספרות",
    "dijkstra": "Dijkstra",
    "dynamic-programming": "תכנות דינמי",
    "fifo": "FIFO",
    "fsm": "מכונת מצבים",
    "geometry": "גאומטריה",
    "gray-code": "קוד Gray",
    "greedy": "אלגוריתם חמדן",
    "heap": "ערימה",
    "lfsr": "LFSR",
    "logic": "לוגיקה",
    "logic-puzzles": "חידות היגיון",
    "math": "מתמטיקה",
    "methodology": "מתודולוגיה",
    "metastability": "מטא־יציבות",
    "number-bases": "בסיסי ספירה",
    "optimization": "אופטימיזציה",
    "pcie": "PCIe",
    "probability": "הסתברות",
    "proof": "הוכחה",
    "protocols": "פרוטוקולים",
    "python": "Python",
    "randomization": "רנדומיזציה",
    "recursion": "רקורסיה",
    "sequences": "סדרות",
    "sliding-window": "חלון נע",
    "sorting": "מיון",
    "stack": "מחסנית",
    "sva": "SVA",
    "systemverilog": "SystemVerilog",
    "two-pointers": "שני מצביעים",
    "usb4": "USB4",
    "uvm": "UVM",
}


def topic_name(tag: str) -> str:
    return TOPICS.get(tag, tag)


# Tags that almost every question carries; they do not make two questions "related".
GENERIC_TAGS = {"python", "systemverilog"}
RELATED_MAX = 3

REQUIRED_FIELDS = ("id", "title", "level", "difficulty", "kind", "tags")
PLACEHOLDER = re.compile(r"<!--\s*questions-table(?:\s+level=(\w+))?\s*-->")
CARDS = re.compile(r"<!--\s*level-cards\s*-->")
HERO = re.compile(r"<!--\s*hero\s*-->(.*?)<!--\s*/hero\s*-->", re.S)
PATH_STEPS = re.compile(r"<!--\s*path-steps\s*-->")
PATH_CARDS = re.compile(r"<!--\s*path-cards(\s+featured)?\s*-->")
HOW_IT_WORKS = re.compile(r"<!--\s*how-it-works\s*-->")
CATALOG_LINK = re.compile(r"<!--\s*catalog-link\s*-->")
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
# Page weight (S423): WaveDrom loads only on the pages that draw a ```wavedrom block, and
# the stylesheet parts of extra_css reach the browser as one file, written at the end of the
# build; the 404 page (a template, not a page) gets the same link in on_post_build.
WAVEDROM_CDN = ["https://cdn.jsdelivr.net/npm/wavedrom@3.5.0/skins/default.js",
                "https://cdn.jsdelivr.net/npm/wavedrom@3.5.0/wavedrom.min.js"]
WAVEDROM_INIT = "javascripts/wavedrom-init.js"
WAVEDROM_BLOCK = '<pre class="wavedrom">'
JOINED_CSS = "stylesheets/site.css"
CSS_LINK = re.compile(r'<link rel="stylesheet" href="([^"]*?)stylesheets/\d\d-[\w-]+\.css">\n?')
_css_parts: list[str] = []      # the parts of extra_css, in order; filled in on_config
# The cost chips of a solution (A183): one comment line under its answer block,
# "<!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->", each chip a label word and a value.
COST_LINE = re.compile(r"^([ \t]*)<!--\s*cost:\s*(.+?)\s*-->[ \t]*$", re.M)

# Question metadata keyed by src_uri, and the study paths in order; filled in on_config.
_questions: dict[str, dict] = {}
_paths: list[dict] = []
_comments: dict = {}
_kind_files: dict[str, str] = {}   # explorer kind -> its file name in EXPLORER_DIR
_statements: dict[str, list] = {}  # question page url -> its statement and parts (search)


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
                              "interactive": interactive, "boxes": body.count('class="explorer"')}

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
                      "order": meta.get("order", 99), "featured": bool(meta.get("featured")),
                      "steps": steps})
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
    global _questions, _paths, _comments, _kind_files, _css_parts
    _questions = _load_questions(Path(config["docs_dir"]))
    _css_parts = [str(c) for c in (config.get("extra_css") or [])]
    if any(not CSS_LINK.match(f'<link rel="stylesheet" href="{c}">') for c in _css_parts):
        raise PluginError(f"extra_css must be the parts stylesheets/NN-name.css, got {_css_parts}")
    _paths = _load_paths(Path(config["docs_dir"]))
    _comments = dict(config["extra"].get("comments") or {})
    _kind_files = _load_kind_files(Path(config["docs_dir"]))

    nav: list = [{"ראשי": "index.md"}, {"כל השאלות": "all.md"}]
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
    # the social cards (layouts/dvq.yml) read the kind names and the counts from here
    config["extra"]["dvq_cards"] = {
        "kinds": KINDS,
        "levels": LEVELS,
        "counts": {lv: sum(q["level"] == lv for q in _questions.values()) for lv in LEVELS},
        "total": len(_questions),
        "boxes": sum(q.get("boxes", 0) for q in _questions.values()),
    }
    # the 404 page (overrides/404.html) offers the question whose id or slug is in the
    # missing address: [id, title, path from the site root]
    config["extra"]["dvq_404"] = [[q["id"], str(q["title"]), q["src_uri"][: -len(".md")] + "/"]
                                  for q in sorted(_questions.values(), key=lambda q: q["id"])]
    return config


def _added_date(q: dict) -> dt.date | None:
    """The date in the front matter's `added`: YAML gives a date, or a string when the
    date is quoted ("2026-10-28"), which counts the same."""
    added = q.get("added")
    if isinstance(added, dt.datetime):
        return added.date()
    if isinstance(added, dt.date):
        return added
    return dt.date.fromisoformat(added.strip()) if isinstance(added, str) and added.strip() else None


def _new_ids() -> set[str]:
    """The questions that get the "new" chip: added within NEW_DAYS of the build, the
    newest NEW_MAX of them (the later id first on the same day)."""
    today = dt.date.today()
    recent = [q for q in _questions.values() if _added_date(q) and (today - _added_date(q)).days <= NEW_DAYS]
    recent.sort(key=lambda q: (_added_date(q), q["id"]), reverse=True)
    return {q["id"] for q in recent[:NEW_MAX]}


def _is_new(q: dict) -> bool:
    return q["id"] in _new_ids()


def new_chip(q: dict) -> str:
    return '<span class="chip chip-new">חדש</span>' if _is_new(q) else ""


# A chip in a list of questions (a path, related questions, what's new) is left out of the
# site search (quiet=True): the search shows a section's text with the tags stripped, and
# the chips glued to the title ("…ומחסריםסטודנטבינוני") only made the result harder to read.
QUIET = " data-search-exclude"


def level_chip(level: str, quiet: bool = False) -> str:
    return f'<span class="chip chip-level"{QUIET if quiet else ""}>{LEVELS[level]}</span>'


def difficulty_chip(difficulty: str, quiet: bool = False) -> str:
    return f'<span class="chip chip-diff chip-diff-{difficulty}"{QUIET if quiet else ""}>{DIFFICULTIES[difficulty]}</span>'


def kind_icon(kind: str) -> str:
    return f'<i class="kind-ico kind-ico-{kind}" aria-hidden="true"></i>'


def kind_chip(kind: str, quiet: bool = False) -> str:
    return f'<span class="chip chip-kind chip-kind-{kind}"{QUIET if quiet else ""}>{kind_icon(kind)}{KINDS[kind]}</span>'


def _base(page_url: str) -> str:
    """Directory of a page URL, for relative links (page URLs end with '/')."""
    return page_url if page_url.endswith("/") or not page_url else posixpath.dirname(page_url) + "/"


def _href(src_uri: str, page_url: str) -> str:
    """Relative link from the page at page_url to the page built from src_uri."""
    target = src_uri[: -len(".md")] + "/"
    if target.endswith("/index/"):
        target = target[: -len("index/")]
    return posixpath.relpath(target or ".", _base(page_url) or ".") + "/"


def _tag_link(tag: str, base: str, cls: str = "") -> str:
    href = posixpath.relpath("tags/", base or ".") + "/#tag:" + tag
    attr = f' class="{cls}"' if cls else ""
    return f'<a{attr} href="{html.escape(href)}">{html.escape(topic_name(tag))}</a>'


def ui_icon(name: str) -> str:
    return f'<i class="ui-ico ui-ico-{name}" aria-hidden="true"></i>'


def _badge(icon: str, text: str, title: str, cls: str = "") -> str:
    return f'<span class="qh-badge{cls}" title="{html.escape(title)}">{ui_icon(icon)}{text}</span>'


def _header(q: dict, markdown: str, page_url: str, tools: str = "") -> str:
    """Header card (UI324): the title first with the page tools beside it, then one row of
    chips (id, level, difficulty, kind) and small badges (interactive, tested code, new),
    and one quiet line of topics, date and source. On a phone the tools go under the
    chips, so the title opens the page."""
    base = _base(page_url)
    langs = [name for name, fence in (("SV", "systemverilog"), ("Python", "python"))
             if extract_code.blocks_from_text(markdown, fence)]
    badges = []
    if q.get("interactive"):
        badges.append(_badge("interactive", "אינטראקטיבי", "יש בדף ממשק אינטראקטיבי : סליידרים, אנימציה או איור צעד-צעד", " qh-badge-play"))
    if langs:
        full = " ו-".join("SystemVerilog" if n == "SV" else n for n in langs)
        if _has_tests(q):    # one badge for the code and its tests
            badges.append(_badge("tested", "קוד נבדק", f"פתרון בקוד {full}, שרץ ונבדק אוטומטית בכל עדכון של האתר", " qh-badge-ok"))
        else:
            badges.append(_badge("code", f'<bdi dir="ltr">{" + ".join(langs)}</bdi>', f"פתרון בקוד {full}"))
    if _is_new(q):
        badges.append(_badge("new", "חדש", "מהשאלות החדשות ביותר באתר : נוספה בשבוע האחרון", " qh-badge-new"))
    topics = "".join(_tag_link(t, base, "qh-tag") for t in q["tags"])     # M5: the topics as chips
    bottom = [f'<span class="qh-topics"><span class="qh-topics-name">נושאים :</span>{topics}</span>']
    added = _added_date(q)
    if added:
        bottom.append(f'<span class="qh-sep"></span><span>נוספה ב-{_date_he(added)}</span>')
    if q.get("source"):
        bottom.append(f'<span class="qh-sep"></span><span>מקור : {html.escape(str(q["source"]))}</span>')
    return (
        '<div class="question-header">\n'
        f'<h1>{html.escape(str(q["title"]))}</h1>\n'
        f'<div class="qh-top"><span class="qh-id">שאלה {q["id"]}</span>'
        f'{level_chip(q["level"])}{difficulty_chip(q["difficulty"])}{kind_chip(q["kind"])}{"".join(badges)}</div>\n'
        f'{tools}\n'
        f'<div class="qh-bottom">{"".join(bottom)}</div>\n'
        '</div>\n\n'
    )


def _tool(cls: str, icon: str, tip: str, extra: str = "", name: str = "") -> str:
    """An icon button; its short name shows under the icon on a touch screen (S420), where
    there is no hover tooltip."""
    label = f'<span class="qt-name" aria-hidden="true">{name}</span>' if name else ""
    return (f'<button type="button" class="qt-btn {cls}" aria-label="{tip}" data-tip="{tip}"{extra}>'
            f'{ui_icon(icon)}{label}</button>')


def _tools(q: dict, page_url: str) -> str:
    """The page tools as icon buttons (UI324): open or close every block (one toggle),
    practice mode with a stopwatch, solved / favourite marks (kept in the browser) and a
    random question of the same level. They sit beside the header's chip row; the toolbar
    carries the level's ids and links for the message shown when a question is marked
    solved."""
    others = [o for o in _questions.values() if o["id"] != q["id"]]
    same = [o for o in others if o["level"] == q["level"]] or others
    random_btn = ""
    if same:
        hrefs = json.dumps([_href(o["src_uri"], page_url) for o in sorted(same, key=lambda o: o["id"])])
        random_btn = _tool("qt-random", "random", "שאלה אקראית מאותה רמה", f' data-hrefs="{html.escape(hrefs)}"', "אקראית")
    # the level's questions in order, for the "solved n of m" message (UI326)
    level = sorted((o for o in _questions.values() if o["level"] == q["level"]), key=lambda o: o["id"])
    level_data = (f' data-level-name="{html.escape(LEVELS[q["level"]])}" data-level-ids="{" ".join(o["id"] for o in level)}"'
                  f' data-level-hrefs="{html.escape(json.dumps([_href(o["src_uri"], page_url) for o in level]))}"'
                  f' data-level-page="{_href("questions/" + q["level"] + "/index.md", page_url)}"')
    # the study paths of the question, for the message when one of them is completed (W348)
    paths = []
    for i, p in enumerate(_paths):
        ids = [s["q"]["id"] for s in p["steps"]]
        if q["id"] in ids:
            nxt = _paths[(i + 1) % len(_paths)] if len(_paths) > 1 else None
            paths.append({"title": p["title"], "ids": ids, "href": _href(p["src_uri"], page_url),
                          "next": {"title": nxt["title"], "href": _href(nxt["src_uri"], page_url)} if nxt else None})
    if paths:
        level_data += f' data-paths="{html.escape(json.dumps(paths, ensure_ascii=False))}"'
    return (f'<div class="question-tools" role="toolbar" aria-label="כלי השאלה" data-search-exclude data-qid="{q["id"]}"{level_data}>'
            + _tool("qt-fold", "unfold-more", "פתח הכל", "", "פתח הכל")
            + _tool("qt-practice", "timer", "מצב תרגול", ' aria-pressed="false"', "תרגול")
            + '<span class="qt-clock" hidden></span>'
            + _tool("qt-mark qt-solved", "solved", "סמן כפתורה", ' data-mark="solved" aria-pressed="false"', "פתרתי")
            + _tool("qt-mark qt-star", "star", "הוסף למועדפים", ' data-mark="star" aria-pressed="false"', "מועדף")
            + random_btn
            + '</div>')


def _progress(ids) -> str:
    """Placeholder for the "solved n of m" bar; marks.js fills it from the browser's marks."""
    return (f'<div class="mark-progress" data-ids="{" ".join(ids)}" hidden>'
            '<span class="mp-bar"><i></i></span><span class="mp-text"></span></div>')


def _path_nav(q: dict, page_url: str) -> str:
    """One block per study path that contains the question: the path and step n of m, then
    the previous and the next step with their ids and titles (S419; a long title is cut
    with an ellipsis, the full one in the tooltip)."""
    lines = []
    for p in _paths:
        ids = [s["q"]["id"] for s in p["steps"]]
        if q["id"] not in ids:
            continue
        i = ids.index(q["id"])
        parts = [f'<span class="pn-path">מסלול <a href="{_href(p["src_uri"], page_url)}">{html.escape(p["title"])}</a></span>'
                 f'<span class="pn-step">שלב {i + 1} מתוך {len(ids)}</span>']
        links = []
        for label, cls, k in (("הקודם", "pn-prev", i - 1), ("הבא", "pn-next", i + 1)):
            if 0 <= k < len(ids):
                other = p["steps"][k]["q"]
                title = html.escape(str(other["title"]))
                links.append(f'<a class="{cls}" href="{_href(other["src_uri"], page_url)}" title="{title}">'
                             f'<span class="pn-label">{label}\u00a0:</span> <span class="pn-id">{other["id"]}</span> '
                             f'<span class="pn-title">{title}</span></a>')
        if links:
            parts.append(f'<span class="pn-links">{"".join(links)}</span>')
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
            f'<li class="path-step" data-id="{q["id"]}"><span class="ps-num" data-search-exclude>{n}</span>'
            f'<div class="ps-body"><div class="ps-head"><span class="ps-id">{q["id"]}</span> '
            f'<a class="ps-title" href="{_href(q["src_uri"], page.url)}">{html.escape(str(q["title"]))}</a>'
            f'{level_chip(q["level"], True)}{difficulty_chip(q["difficulty"], True)}<span class="ps-mark"></span></div>'
            f'<p class="ps-note">{_inline_code(s["note"])}</p></div></li>')
    ids = [s["q"]["id"] for s in p["steps"]]
    return _progress(ids) + '<ol class="path-steps">' + "".join(items) + "</ol>"


def _diff_chips(qs) -> str:
    """The difficulty mix of some questions as chips ("2 קל", "3 בינוני")."""
    counts = {d: sum(q["difficulty"] == d for q in qs) for d in DIFFICULTIES}
    return "".join(f'<span class="chip chip-diff chip-diff-{d}">{n} {DIFFICULTIES[d]}</span>'
                   for d, n in counts.items() if n)


def _path_cards(page_url: str, featured: bool = False) -> str:
    """A card per study path (only the paths marked `featured` on the home page, W342): the
    title on its own line, the description, then the count and the difficulty mix; the "solved" bar shows once a
    question of the path is solved (marks.js, `.is-empty` hides it before)."""
    cards = []
    for p in _paths:
        if featured and not p["featured"]:
            continue
        ids = [s["q"]["id"] for s in p["steps"]]
        kinds = [s["q"]["kind"] for s in p["steps"]]
        kind = max(KINDS, key=kinds.count)            # the kind most of its questions have
        cards.append(
            f'<a class="level-card path-card" href="{_href(p["src_uri"], page_url)}">'
            f'<div class="lc-head"><span class="lc-name">{kind_icon(kind)}{html.escape(p["title"])}</span></div>'
            f'<p class="lc-desc">{html.escape(p["description"])}</p>'
            f'<div class="lc-diff"><span class="lc-count">{len(ids)} שאלות</span>'
            f'{_diff_chips([s["q"] for s in p["steps"]])}</div>'
            f'{_progress(ids)}</a>')
    return '<div class="level-cards path-cards">' + "".join(cards) + "</div>"


HOW_STEPS = [("search", "בוחרים שאלה", "לפי רמת משרה, נושא או מסלול לימוד, או שאלה אקראית."),
             ("timer", "פותרים לבד", "עם רמזים שנפתחים בהדרגה, ובמצב תרגול עם שעון עצר."),
             ("play", "בודקים ומריצים", "פתרון מלא עם הוכחה, קוד שנבדק אוטומטית והרצה בדפדפן.")]


def _how_it_works() -> str:
    """The home page's three steps (W340), in place of the old tip box."""
    items = "".join(f'<li class="hw-step"><span class="hw-ico">{ui_icon(icon)}</span>'
                    f'<span class="hw-num">{n}</span><b class="hw-title">{title}</b>'
                    f'<span class="hw-text">{text}</span></li>'
                    for n, (icon, title, text) in enumerate(HOW_STEPS, 1))
    return f'<ol class="how-it-works">{items}</ol>'


def _catalog_link(page_url: str) -> str:
    """The home page's way into the catalog page (W341)."""
    return (f'<p class="catalog-link"><a class="md-button md-button--primary" href="{_href("all.md", page_url)}">'
            f'לכל {len(_questions)} השאלות</a>'
            '<span>עם סינון לפי רמה, קושי, סוג ונושא, חיפוש ומיון.</span></p>')


def _has_tests(q: dict) -> bool:
    return (extract_code.ROOT / "tests" / q["id"]).exists()


def _level_cards(page_url: str) -> str:
    base = _base(page_url)
    cards = []
    for level, label in LEVELS.items():
        qs = [q for q in _questions.values() if q["level"] == level]
        href = posixpath.relpath(f"{QUESTIONS_DIR}/{level}/", base or ".") + "/"
        diff = _diff_chips(qs)
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


HERO_SEARCHES = ["FIFO", "PCIe", "SVA", "הסתברות", "חידות", "Gray"]

# The hero's background: a clock, a data bit and a bus, drawn as a quiet line pattern
# (pathLength 1, so the CSS can draw each line once from its start, W339). The pattern is
# there twice, side by side, so the stylesheet can roll it along one width without a seam,
# and an amber cursor sweeps across it, like a logic analyzer (M1, 13-motion.css).
HERO_WAVE_PATHS = (
    '<path class="hh-w1" pathLength="1" d="M0 30h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20v-20h20v20h20"/>'
    '<path class="hh-w2" pathLength="1" d="M0 75h50v-20h90v20h40v-20h130v20h60v-20h40v20h110v-20h120"/>'
    '<path class="hh-w3" pathLength="1" d="M0 120h30l10-15h90l10 15-10 15h-90l-10-15M140 120l10-15h110l10 15-10 15h-110l-10-15M270 120l10-15h70l10 15-10 15h-70l-10-15M360 120l10-15h130l10 15-10 15h-130l-10-15M510 120l10-15h110l10 15"/>')
HERO_WAVES = (
    '<svg class="hh-waves" viewBox="0 0 640 150" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">'
    f'<g class="hh-roll"><g>{HERO_WAVE_PATHS}</g><g transform="translate(640 0)">{HERO_WAVE_PATHS}</g></g>'
    '<line class="hh-cursor" x1="0" y1="2" x2="0" y2="148"/>'
    '</svg>')

# The live example beside the hero's text on a wide screen (M2): the machine of 0055 part a
# (the bits arrive MSB first, r -> (2r + b) mod 3) on three states in a row, and home.js
# feeds it numbers bit by bit. The page shows the last frame of the first number as it
# is (27 = 11011, back in the state 0), so nothing is missing without the script.
HERO_FSM_NUMBER = 27
HERO_FSM_NODES = [(62, 0), (150, 1), (238, 2)]
# (from, bit, to, path, label x, label y)
HERO_FSM_EDGES = [
    (0, 1, 1, "M78 53Q106 26 134 53", 106, 31), (1, 1, 0, "M134 75Q106 102 78 75", 106, 109),
    (1, 0, 2, "M166 53Q194 26 222 53", 194, 31), (2, 0, 1, "M222 75Q194 102 166 75", 194, 109),
    (0, 0, 0, "M45 55C12 34 12 94 45 73", 9, 68), (2, 1, 2, "M255 55C288 34 288 94 255 73", 291, 68),
]


def _hero_fsm(href: str) -> str:
    bits = bin(HERO_FSM_NUMBER)[2:]
    edges = "".join(
        f'<path class="hf-edge{" is-taken" if (a, b) == (1, 1) else ""}" data-e="{a}{b}" d="{d}" marker-end="url(#hf-arrow)"/>'
        f'<text class="hf-label" x="{x}" y="{y}" text-anchor="middle">{b}</text>'
        for a, b, _, d, x, y in HERO_FSM_EDGES)
    nodes = "".join(
        f'<g class="hf-node{" is-now" if r == 0 else ""}" data-r="{r}"><circle cx="{x}" cy="64" r="19"/>'
        + (f'<circle cx="{x}" cy="64" r="14"/>' if r == 0 else "")
        + f'<text x="{x}" y="69" text-anchor="middle">{r}</text></g>'
        for x, r in HERO_FSM_NODES)
    svg = ('<svg class="hf-svg" viewBox="0 0 300 120" aria-hidden="true" focusable="false">'
           '<defs><marker id="hf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10 Z" class="hf-head"/></marker></defs>' + edges + nodes + '</svg>')
    bit_spans = "".join(f'<span class="hf-bit is-read">{b}</span>' for b in bits)
    return (
        f'<div class="hh-fsm" data-search-exclude data-number="{HERO_FSM_NUMBER}">'
        '<p class="hf-title">דוגמה חיה\u00a0: חלוקה ב-3, ביט אחרי ביט</p>'
        f'{svg}'
        f'<p class="hf-stream"><span class="hf-bits" dir="ltr">{bit_spans}</span></p>'
        f'<p class="hf-read" aria-live="off">המספר <bdi dir="ltr">{HERO_FSM_NUMBER}</bdi> מתחלק ב-3 ✓</p>'
        f'<a class="hf-go" href="{href}">לשאלה 0055 ←</a>'
        '</div>')


def _hero(inner: str, page_url: str) -> str:
    """The home page's hero (UI319): the title and the lead from the page, on a navy card
    with a waveform pattern; "start practising" (marks.js points it at the first question
    not marked solved, student to senior), a random question, a large search field that
    opens the site search, a few ready searches, and one slim line of numbers."""
    order = sorted(_questions.values(), key=lambda q: (list(LEVELS).index(q["level"]), q["id"]))
    hrefs = [_href(q["src_uri"], page_url) for q in order]
    ids = [q["id"] for q in order]
    qs = list(_questions.values())
    tested = sum(q["has_code"] and _has_tests(q) for q in qs)
    boxes = sum(q.get("boxes", 0) for q in qs)
    stats = [("help", len(qs), "שאלות עם פתרון מלא"), ("tested", tested, "עם קוד שנבדק אוטומטית"),
             ("interactive", boxes, "תיבות אינטראקטיביות")]
    fsm = next((q for q in qs if q["id"] == "0055"), order[0])
    fsm_href = _href(fsm["src_uri"], page_url)
    searches = "".join(f'<button type="button" class="hh-chip" data-q="{html.escape(t)}">{html.escape(t)}</button>' for t in HERO_SEARCHES)
    return (
        '<div class="home-hero" markdown>\n'
        f'<div class="hh-bg" aria-hidden="true">{HERO_WAVES}</div>\n'
        f'{_hero_fsm(fsm_href)}\n\n{inner.strip()}\n\n'
        '<div class="hh-tools" data-search-exclude>'
        '<div class="hh-actions">'
        f'<a class="md-button md-button--primary hh-start" href="{hrefs[0]}" data-hrefs="{html.escape(json.dumps(hrefs))}" data-ids="{" ".join(ids)}">להתחיל לתרגל</a>'
        f'<a class="md-button hh-random" href="{hrefs[0]}" data-hrefs="{html.escape(json.dumps(hrefs))}">{ui_icon("random")}שאלה אקראית</a></div>'
        f'<button type="button" class="hh-search">{ui_icon("search")}<span>חיפוש לפי מספר שאלה, שם או נושא</span><kbd>/</kbd></button>'
        f'<div class="hh-suggest"><span>למשל\u00a0:</span>{searches}</div>'
        '<div class="hh-stats">' + "".join(f'<span>{ui_icon(i)}<b>{n}</b> {label}</span>' for i, n, label in stats) + '</div>'
        '</div>\n'
        '</div>\n'
    )


def _related(q: dict, page_url: str) -> str:
    """Up to RELATED_MAX other questions that share the most (non-generic) tags."""
    mine = set(q["tags"]) - GENERIC_TAGS
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
        href = _href(other["src_uri"], page_url)
        items.append(
            f'<li><span class="rq-id">{other["id"]}</span> '
            f'<a class="rq-title" href="{href}">{html.escape(str(other["title"]))}</a>'
            f'{level_chip(other["level"], True)}{difficulty_chip(other["difficulty"], True)}</li>'
        )
    return "\n\n## שאלות קשורות\n\n<ul class=\"related-questions\">\n" + "\n".join(items) + "\n</ul>\n"


def _by_added() -> list[dict]:
    """The questions with an added date, the newest first (a later id first on one day)."""
    return sorted((q for q in _questions.values() if _added_date(q)), key=lambda q: (_added_date(q), q["id"]), reverse=True)


def _date_he(d: dt.date) -> str:
    return f"{d.day} ב{MONTHS[d.month - 1]} {d.year}"


def _question_item(q: dict, page_url: str) -> str:
    return (f'<li><span class="rq-id">{q["id"]}</span> '
            f'<a class="rq-title" href="{_href(q["src_uri"], page_url)}">{html.escape(str(q["title"]))}</a>'
            f'{level_chip(q["level"], True)}{difficulty_chip(q["difficulty"], True)}{kind_chip(q["kind"], True)}</li>')


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
        if _added_date(q) != day:
            if day is not None:
                out.append("</ul>")
            day = _added_date(q)
            n = sum(_added_date(o) == day for o in _questions.values())
            out.append(f'<h2 class="new-day" id="d{day.isoformat()}">\u200f{_date_he(day)} '
                       f'<span class="new-count">{n} {"שאלה" if n == 1 else "שאלות"}</span></h2>\n<ul class="related-questions">')
        out.append(_question_item(q, page_url))
    if out:
        out.append("</ul>")
    return "\n".join(out)


TOPICS_INLINE = 6   # topics shown in the filter before "more topics"
ROW_TOPICS = 2      # topics shown in a row before "+n"


def _table(level: str | None, page_url: str) -> str:
    """A filterable question table (UI322, UI323). Above it: a search field (title,
    topics in both names, id), a "filter (n)" button that opens the filters on phones,
    and the filters as segmented groups (level on the all-questions table, difficulty,
    kind, the reader's marks) with the topics behind "more topics"; under them the
    active filters as chips with the count. Each row has the id, the title on one line
    with the kind and the first topics under it (a topic filters the table; "+n" shows
    the rest), the level on the all-questions table, and the difficulty.
    question-filter.js keeps the filters in the address and says what to do when no
    row is left."""
    rows = sorted(
        (q for q in _questions.values() if level is None or q["level"] == level),
        key=lambda q: q["id"],
    )
    if not rows:
        return '<p class="questions-empty">עדיין אין שאלות בקטגוריה הזו.</p>'

    count = {}
    for q in rows:
        for t in q["tags"]:
            count[t] = count.get(t, 0) + 1
    tags = sorted(count, key=lambda t: (-count[t], topic_name(t)))   # the most common first

    def chip(name: str, value: str, label: str, extra: str = "") -> str:
        icon = kind_icon(value) if name == "kind" and value else ""
        pressed = "true" if not value else "false"
        return (f'<button type="button" class="filter-chip{" is-active" if not value else ""}" data-value="{html.escape(value)}" '
                f'aria-pressed="{pressed}"{extra}>{icon}{html.escape(label)}</button>')

    def group(name: str, label: str, values) -> str:
        chips = chip(name, "", "הכל") + "".join(chip(name, v, l) for v, l in values)
        return (f'<div class="filter-group filter-seg" data-filter="{name}" data-value="" role="group" aria-label="{label}">'
                f'<span class="filter-label">{label}</span><span class="seg">{chips}</span></div>')

    inline, more = tags[:TOPICS_INLINE], tags[TOPICS_INLINE:]
    topic_chips = chip("tag", "", "הכל") + "".join(chip("tag", t, topic_name(t), f' data-count="{count[t]}"') for t in inline)
    more_html = ""
    if more:
        more_html = (f'<button type="button" class="topics-toggle" aria-expanded="false">עוד נושאים ({len(more)})</button>'
                     '<div class="topics-more" hidden>'
                     '<input type="search" class="topics-search" placeholder="חיפוש נושא" aria-label="חיפוש נושא">'
                     + "".join(chip("tag", t, topic_name(t), f' data-count="{count[t]}" data-en="{html.escape(t)}"') for t in more)
                     + '<p class="topics-none" hidden>אין נושא כזה.</p></div>')
    topics = (f'<div class="filter-group filter-topics" data-filter="tag" data-value="" role="group" aria-label="נושא">'
              f'<span class="filter-label">נושא</span><span class="topics-inline">{topic_chips}</span>{more_html}</div>')

    sorts = [("id", "מספר"), ("title", "שם")] + ([("level", "משרה")] if level is None else []) + [("difficulty", "קושי")]
    panel_id = f"qf-{level or 'all'}"
    # The filter and the table stay out of the site search, under one <section>: the search
    # plugin of Material ends an exclusion at the first closing tag of the same name inside
    # it (a nested </div>), so the excluded element must be a tag that is not nested in it.
    out = ['<section class="q-noindex" markdown="0" data-search-exclude>',
           '<div class="question-filter" markdown="0">']
    out.append('<div class="filter-bar">'
               '<label class="filter-search"><span class="filter-search-label">חיפוש</span>'
               '<input type="search" data-filter="text" placeholder="שם, נושא או מספר"></label>'
               f'<button type="button" class="filter-toggle" aria-expanded="false" aria-controls="{panel_id}">'
               '<span class="ui-ico ui-ico-filter" aria-hidden="true"></span>סינון<span class="filter-n"></span></button>'
               '<label class="filter-sort">מיון <select>'
               + "".join(f'<option value="{k}">{l}</option>' for k, l in sorts)
               + '</select></label>'
               '<button type="button" class="filter-random">שאלה אקראית</button></div>')
    out.append(f'<div class="filter-panel" id="{panel_id}">')
    if level is None:
        out.append(group("level", "משרה", LEVELS.items()))
    out.append(group("difficulty", "קושי", DIFFICULTIES.items()))
    out.append(group("kind", "סוג", [(k, v) for k, v in KINDS.items() if any(q["kind"] == k for q in rows)]))
    out.append(group("mark", "סימון", [("star", "מועדפים"), ("solved", "פתורות"), ("unsolved", "לא פתורות")]))
    out.append(topics)
    out.append("</div>")
    out.append('<div class="filter-active" aria-live="polite"><span class="filter-count"></span></div>')
    out.append("</div>")

    def th(key: str, label: str) -> str:
        return f'<th data-sort="{key}"><button type="button" class="th-sort">{label}</button></th>'

    level_col = th("level", "משרה") if level is None else ""
    new = _new_ids()
    # The table itself has no class, so Material styles it and wraps it for scrolling
    out.append('<div class="questions-wrap"><table><thead><tr>'
               f'{th("id", "#")}{th("title", "שאלה")}{level_col}{th("difficulty", "קושי")}'
               "</tr></thead><tbody>")
    for q in rows:
        href = _href(q["src_uri"], page_url)
        title = html.escape(str(q["title"]))
        level_td = f'<td class="q-level">{level_chip(q["level"])}</td>' if level is None else ""
        topic_btn = lambda t: f'<button type="button" class="q-topic" data-tag="{html.escape(t)}" title="סינון לפי הנושא">{html.escape(topic_name(t))}</button>'  # noqa: E731
        shown, rest = q["tags"][:ROW_TOPICS], q["tags"][ROW_TOPICS:]
        topics_html = "".join(topic_btn(t) for t in shown)
        if rest:
            topics_html += (f'<button type="button" class="q-more" aria-expanded="false" aria-label="עוד {len(rest)} נושאים">+{len(rest)}</button>'
                            f'<span class="q-rest" hidden>{"".join(topic_btn(t) for t in rest)}</span>')
        search = " ".join([q["id"], str(int(q["id"])), str(q["title"]), *q["tags"], *(topic_name(t) for t in q["tags"])])
        out.append(
            f'<tr data-id="{q["id"]}" data-level="{q["level"]}" data-difficulty="{q["difficulty"]}" data-kind="{q["kind"]}" '
            f'data-level-rank="{LEVEL_RANK[q["level"]]}" data-diff-rank="{DIFF_RANK[q["difficulty"]]}" '
            f'data-tags="{html.escape(" ".join(q["tags"]))}" data-search="{html.escape(search.lower())}">'
            f'<td class="q-id">{q["id"]}</td>'
            f'<td class="q-title"><div class="q-line"><a href="{href}" title="{title}">{title}</a>'
            f'{new_chip(q) if q["id"] in new else ""}<span class="q-marks"></span></div>'
            f'<div class="q-meta">{kind_chip(q["kind"])}<span class="q-topics">{topics_html}</span></div></td>'
            f"{level_td}"
            f'<td class="q-diff">{difficulty_chip(q["difficulty"])}</td>'
            "</tr>"
        )
    out.append("</tbody></table></div>")
    out.append('<div class="questions-none" hidden></div>')
    out.append('</section>')
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
<p class="py-runner-note">הפונקציות מהפתרון כבר טעונות. אפשר לשנות את הקוד שבתיבה ולהריץ שוב
(Ctrl+Enter). ליד כל <code>print</code> שבהערה שלו כתוב הערך הצפוי מופיע סימן אחרי ההרצה.</p>
<script type="application/json" class="py-page-code">{json.dumps(page_code).replace("</", "<\\/")}</script>
<div class="py-editor-wrap"><textarea class="py-editor" aria-label="הקוד להרצה (Python)" spellcheck="false" dir="ltr" rows="{min(max(demo_code.count(chr(10)) + 1, 6), 22)}">{html.escape(demo_code)}</textarea></div>
<div class="py-buttons">
<button type="button" class="md-button md-button--primary py-run">▶ הרץ</button>
<button type="button" class="md-button py-stop" disabled>עצור</button>
<button type="button" class="md-button py-reset">איפוס</button>
<span class="py-status" role="status" aria-live="polite"></span>
</div>
<ol class="py-stages" hidden aria-hidden="true"><li data-stage="download">מוריד את Python (פעם אחת)</li><li data-stage="run">טוען את הפתרון ומריץ</li></ol>
<div class="py-output-wrap" hidden><button type="button" class="py-copy" title="העתקת הפלט" aria-label="העתקת הפלט"></button><pre class="py-output" dir="ltr"></pre></div>
<div class="py-checks" hidden></div>
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
        markdown = (_header(q, markdown, page.url, _tools(q, page.url)) + _path_nav(q, page.url) + markdown
                    + _run_panel(q, markdown) + _related(q, page.url) + _comments_block())

    markdown = COST_LINE.sub(_cost_chips, markdown)
    markdown = CARDS.sub(lambda m: _level_cards(page.url), markdown)
    markdown = HERO.sub(lambda m: _hero(m.group(1), page.url), markdown)
    markdown = PATH_STEPS.sub(lambda m: _path_steps(page), markdown)
    markdown = PATH_CARDS.sub(lambda m: _path_cards(page.url, bool(m.group(1))), markdown)
    markdown = HOW_IT_WORKS.sub(lambda m: _how_it_works(), markdown)
    markdown = CATALOG_LINK.sub(lambda m: _catalog_link(page.url), markdown)
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


def wavedrom_scripts(output: str, page_url: str) -> str:
    """The WaveDrom scripts and the init script for a built page with a ```wavedrom block,
    or "" for every other page."""
    if WAVEDROM_BLOCK not in output:
        return ""
    base = _base(page_url) or "."
    return "".join(f'<script src="{src}"></script>' for src in [*WAVEDROM_CDN, posixpath.relpath(WAVEDROM_INIT, base)])


def one_stylesheet(output: str) -> str:
    """The links of the stylesheet parts replaced by one link to the joined file, in the
    place of the first and with its base."""
    m = CSS_LINK.search(output)
    if not m:
        return output
    output = CSS_LINK.sub("", output)
    return output[:m.start()] + f'<link rel="stylesheet" href="{m.group(1)}{JOINED_CSS}">\n' + output[m.start():]


TAG_CHIP = re.compile(r'(<span class="md-tag">)([^<]+)(</span>)')
TAG_TOC = re.compile(r'(href="#tag:([^"]+)" class="md-nav__link">\s*<span class="md-ellipsis">\s*)([^<]+?)(\s*</span>)')


def _tag_names(output: str) -> str:
    """The tags page with the topics' Hebrew names, in its headings and its contents list
    (the anchors keep the tags as written), and a grid of all tags with their counts above
    the lists (Y398)."""
    output = TAG_CHIP.sub(lambda m: m.group(1) + html.escape(topic_name(html.unescape(m.group(2).strip()))) + m.group(3), output)
    output = TAG_TOC.sub(lambda m: m.group(1) + html.escape(topic_name(m.group(2))) + m.group(4), output)
    return _tag_grid(output)


TAG_SECTION = re.compile(r'(<h2 id="tag:([^"]+)">.*?<span class="md-tag">([^<]+)</span>.*?</h2>\s*)<ul>(.*?)</ul>', re.S)


def _tag_grid(output: str) -> str:
    """Every tag as a chip with its number of questions, linking to its list, and each list
    folded under its tag's name (a link to "#tag:..." opens it, reading-tools.js), in
    columns when open (ul.tag-list)."""
    chips = []

    def section(m: re.Match) -> str:
        count = m.group(4).count("<li>")
        count_html = f'<span class="tag-count" aria-label="{count} שאלות">{count}</span>'
        chips.append(f'<a class="tag-chip" href="#tag:{m.group(2)}">{m.group(3)}{count_html}</a>')
        return (f'<details class="tag-section" id="tag:{m.group(2)}"><summary>'
                f'<span class="md-tag">{m.group(3)}</span>{count_html}</summary>\n'
                f'<ul class="tag-list">{m.group(4)}</ul></details>\n')

    output = TAG_SECTION.sub(section, output)
    at = output.find('<details class="tag-section"')
    if at < 0 or not chips:
        return output
    return output[:at] + f'<nav class="tag-grid" aria-label="כל התגיות">{"".join(chips)}</nav>\n' + output[at:]


TRAP_RUN = re.compile(r'(?:<details class="trap">.*?</details>\s*)+', re.S)
TRAP_PREFIX = "<summary>מלכודת\u00a0: "


def _trap_group(m: re.Match) -> str:
    """A run of trap blocks as one group (W337): a title with the count, then the traps,
    each still folding on its own, without the "מלכודת :" prefix the title now carries."""
    run = m.group(0)
    count = run.count('<details class="trap">')
    title = "מלכודת נפוצה" if count == 1 else f"מלכודות נפוצות ({count})"
    return (f'<div class="trap-group" role="group" aria-label="{title}">'
            f'<p class="trap-group-title">{title}</p>\n'
            f'{run.replace(TRAP_PREFIX, "<summary>").rstrip()}</div>\n')


def on_post_page(output, page, config, **kwargs):
    if page.file.src_uri == "tags.md":
        output = _tag_names(output)
    if page.file.src_uri in _questions:
        output = TRAP_RUN.sub(_trap_group, output)
        _statements[page.url] = statement_sections(output)
    output = one_stylesheet(output)
    scripts = wavedrom_scripts(output, page.url) + explorer_scripts(output, page.url)
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
    show them as chips under the title, with the topics by their Hebrew names), and the id
    as written and without its zeros ("0021 21") in its own field."""
    doc["title"] = f'{q["id"]} · {q["title"]}'
    doc["tags"] = [LEVELS[q["level"]], DIFFICULTIES[q["difficulty"]], KINDS[q["kind"]],
                   *[topic_name(t) for t in doc.get("tags", []) if t not in (LEVELS[q["level"]], DIFFICULTIES[q["difficulty"]])]]
    doc[ID_FIELD] = f'{q["id"]} {int(q["id"])}'


def _question_docs(docs: list[dict], pages: dict) -> list[dict]:
    """The search finds the questions themselves (Y396): one document per question page,
    its text the statement, and one per part ("סעיף א ...") with the part's own statement.
    Hints, solutions, code, traps and follow-ups, and every page that is not a question
    (home, paths, catalog, tags, what's new), are left out; the math reads in plain symbols
    (search_text.py)."""
    out = []
    for doc in docs:
        if "#" in doc["location"] or doc["location"] not in pages:
            continue
        sections = _statements.get(doc["location"], [])
        doc["text"] = next((text for _, title, text in sections if title == STATEMENT), "")
        out.append(doc)
        out += [{"location": f'{doc["location"]}#{anchor}', "title": title, "text": text}
                for anchor, title, text in sections if title != STATEMENT]
    return out


def on_post_build(config, **kwargs):
    site, docs = Path(config["site_dir"]), Path(config["docs_dir"])
    joined = ("/* The site's styles: the parts of docs/stylesheets/ joined in this order at build time\n"
              "   (hooks/questions.py); edit the parts, never this file. */\n")
    for part in _css_parts:
        joined += f"\n/* ---- {part} ---- */\n" + (docs / part).read_text(encoding="utf-8")
    (site / JOINED_CSS).write_text(joined, encoding="utf-8")
    not_found = site / "404.html"
    if not_found.exists():
        not_found.write_text(one_stylesheet(not_found.read_text(encoding="utf-8")), encoding="utf-8")
    path = site / "search" / "search_index.json"
    if not path.exists():
        return
    index = json.loads(path.read_text(encoding="utf-8"))
    pages = {q["src_uri"][: -len(".md")] + "/": q for q in _questions.values()}
    index["docs"] = _question_docs(index["docs"], pages)
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
    for doc in index["docs"]:
        if doc["location"] in pages:
            _search_question(doc, pages[doc["location"]])
    index["config"]["fields"][SEARCH_FIELD] = {"boost": 1.0}
    index["config"]["fields"][ID_FIELD] = {"boost": 1e7}
    path.write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
