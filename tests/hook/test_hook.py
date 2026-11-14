"""Tests of the site hook (hooks/questions.py): Hebrew search variants, study paths and the
explorer scripts of a page."""

import importlib.util
import re

from extract_code import ROOT

spec = importlib.util.spec_from_file_location("site_hook", ROOT / "hooks" / "questions.py")
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

DOCS = ROOT / "docs"
HEBREW = re.compile(r"^[א-ת]")


def variants(text, known=()):
    words = hook.WORD.findall(text)
    return hook._search_variants(set(text.split()), words, set(known) | set(words))


def test_prefix_letters_are_stripped():
    v = variants("בטבלה")
    assert "טבלה" in v
    # two or three letters only when the rest is a known word
    assert "תנאי" in variants("והתנאי", known={"תנאי"})
    assert "תנאי" not in variants("והתנאי")
    # at least three letters remain, and non-prefix letters stop the stripping
    assert variants("בית") == set()
    assert not any(w.startswith("ר") for w in variants("קופסה"))


def test_punctuation_and_latin_words():
    v = variants("(לולאה randomize()")
    assert {"לולאה", "randomize"} <= v
    assert variants("plain words") == set()


def test_study_paths():
    hook._questions = hook._load_questions(DOCS)
    paths = hook._load_paths(DOCS)
    assert len(paths) >= 1
    for p in paths:
        assert HEBREW.match(p["title"]) and HEBREW.match(p["description"]), p["src_uri"]
        assert len(p["steps"]) >= 2
        ids = [s["q"]["id"] for s in p["steps"]]
        assert len(ids) == len(set(ids)), p["src_uri"]
        for s in p["steps"]:
            assert HEBREW.match(s["note"]), (p["src_uri"], s["note"])   # RTL: notes start in Hebrew
        assert "<!-- path-steps -->" in (DOCS / p["src_uri"]).read_text(encoding="utf-8")


def test_explorer_kinds_have_files():
    kinds = hook._load_kind_files(DOCS)
    assert kinds["cake-arith"] == kinds["cake-geo"] == "cake.js"
    used = set()
    for page in (DOCS / "questions").rglob("*.md"):
        used |= set(re.findall(r'class="explorer" data-kind="([\w-]+)"', page.read_text(encoding="utf-8")))
    assert used and used <= set(kinds)
    assert set(kinds.values()) == {p.name for p in (DOCS / hook.EXPLORER_DIR).glob("*.js")} - {"core.js"}


def test_explorer_scripts_per_page():
    hook._kind_files = hook._load_kind_files(DOCS)
    page = ('<div class="explorer" data-kind="kaprekar" data-digits="3"></div>'
            '<div class="explorer" data-kind="kapbase"></div><div class="explorer" data-kind="kaprekar"></div>')
    tags = re.findall(r'src="([^"]+)"', hook.explorer_scripts(page, "questions/student/0012-x/"))
    assert tags == ["../../../javascripts/explorer/core.js", "../../../javascripts/explorer/kaprekar.js",
                    "../../../javascripts/explorer/kapbase.js"]
    assert hook.explorer_scripts("<p>no box</p>", "") == ""
    try:
        hook.explorer_scripts('<div class="explorer" data-kind="nope"></div>', "x/")
    except hook.PluginError as e:
        assert "nope" in str(e)
    else:
        raise AssertionError("an unknown kind must fail the build")


def test_wavedrom_only_where_drawn():
    page = '<p>x</p><pre class="wavedrom">{signal: []}</pre>'
    tags = re.findall(r'src="([^"]+)"', hook.wavedrom_scripts(page, "questions/junior/0034-x/"))
    assert tags == [*hook.WAVEDROM_CDN, "../../../javascripts/wave-viewer.js", "../../../javascripts/wavedrom-init.js"]
    assert hook.wavedrom_scripts("<p>no diagram</p>", "questions/junior/0034-x/") == ""


def test_one_stylesheet_link():
    head = ('<link rel="stylesheet" href="../../assets/stylesheets/main.css">\n'
            '<link rel="stylesheet" href="../../stylesheets/01-base.css">\n'
            '<link rel="stylesheet" href="../../stylesheets/02-pages.css">\n'
            '<link rel="stylesheet" href="../../stylesheets/12-rounds-y-s.css">\n<script></script>')
    out = hook.one_stylesheet(head)
    assert out == ('<link rel="stylesheet" href="../../assets/stylesheets/main.css">\n'
                   '<link rel="stylesheet" href="../../stylesheets/site.css">\n<script></script>')
    assert hook.one_stylesheet("<p>no links</p>") == "<p>no links</p>"


def test_cost_chips():
    md = "??? success \"x\"\n    !!! answer \"y\"\n        z\n\n    <!-- cost: זמן \\( O(n) \\) | פלופים 2 -->\n"
    out = hook.COST_LINE.sub(hook._cost_chips, md)
    assert ('    <div class="cost-chips" role="note" aria-label="סיבוכיות" data-search-exclude>'
            '<span class="cost-chip"><b>זמן</b> \\( O(n) \\)</span>'
            '<span class="cost-chip"><b>פלופים</b> 2</span></div>\n') in out
    assert "<!--" not in out


def test_search_keeps_only_the_questions():
    hook._statements["q/a/"] = [("_1", "השאלה", "<p>ניסוח</p>"), ("_2", "סעיף א", "<p>חלק</p>")]
    docs = [{"location": "", "title": "ראשי", "text": "x"},
            {"location": "all/", "title": "כל השאלות", "text": "x"},
            {"location": "q/a/", "title": "A", "text": "chips"},
            {"location": "q/a/#_5", "title": "הרעיון", "text": "פתרון"}]
    out = hook._question_docs(docs, {"q/a/": {}})
    assert out == [{"location": "q/a/", "title": "A", "text": "<p>ניסוח</p>"},
                   {"location": "q/a/#_2", "title": "סעיף א", "text": "<p>חלק</p>"}]


def test_tag_grid_counts_each_tag():
    """The tags page: the level and difficulty tags in their own row, the topics in one
    list with the most questions first (ties by name), every fold keeping its anchor."""
    page = ('<p>intro</p><h2 id="tag:bfs"><span class="md-tag">BFS</span></h2>\n<ul><li>a</li><li>b</li></ul>'
            '<h2 id="tag:cdc"><span class="md-tag">CDC</span></h2>\n<ul><li>c</li></ul>'
            '<h2 id="tag:algorithms"><span class="md-tag">אלגוריתמים</span></h2>\n<ul><li>d</li><li>e</li></ul>'
            '<h2 id="tag:קל"><span class="md-tag">קל</span></h2>\n<ul><li>f</li></ul>'
            '<h2 id="tag:גוניור"><span class="md-tag">ג&#39;וניור</span></h2>\n<ul><li>h</li></ul>'
            '<h2 id="tag:סטודנט"><span class="md-tag">סטודנט</span></h2>\n<ul><li>g</li></ul>')
    out = hook._tag_grid(page)
    assert out.count('<ul class="tag-list">') == 6 and "<h2 id=\"tag:" not in out and "\0" not in out
    order = re.findall(r'<details class="tag-section ([\w-]+)" id="tag:([^"]+)">', out)
    assert order == [("tag-level", "סטודנט"), ("tag-level", "גוניור"), ("tag-level", "קל"), ("tag-row", "bfs"), ("tag-row", "algorithms"), ("tag-row", "cdc")]
    assert out.index('<div class="tag-levels">') < out.index('<div class="tag-rows">')
    assert ('<span class="tr-name">BFS</span><span class="tr-bar" aria-hidden="true"><i style="--p:1.000"></i></span>'
            '<span class="tag-count" aria-label="2 שאלות">2</span>') in out
    assert '<i style="--p:0.500"></i></span><span class="tag-count" aria-label="1 שאלות">1</span>' in out
    assert '<span class="tr-name chip chip-diff chip-diff-easy">קל</span><span class="tag-count" aria-label="1 שאלות">1</span>' in out
    assert hook._tag_grid("<p>no tags</p>") == "<p>no tags</p>"


def _metro_geometry(compact):
    hook._questions = hook._load_questions(DOCS)
    paths = [p for p in hook._load_paths(DOCS) if not compact or p["featured"]]
    g, pad, r = (46, 26, 12) if compact else (54, 30, 13)
    px = hook.maps_metro_px(hook.maps_metro_layout(paths), g, pad)
    return paths, px, r, hook.maps_metro_names(px, {k: p["title"] for k, p in enumerate(paths)}, r)


def test_metro_names_touch_nothing():
    """Every line of both maps has its name, and a name's box (from the generator's width
    estimate) overlaps no station circle, no line or stub, no square and no other name.
    The geometry is checked here on its own: points every half pixel along the lines."""
    for compact in (False, True):
        paths, px, r, names = _metro_geometry(compact)
        assert sorted(names) == list(range(len(paths)))
        for n, nm in names.items():
            x0, y0, x1, y1 = nm["box"]
            assert "".join(t for t, _ in nm["rows"]).replace(" ", "") == paths[n]["title"].replace(" ", "")
            assert len(nm["rows"]) <= 2 and x1 - x0 >= max(hook.maps_text_width(t) for t, _ in nm["rows"]) - 1e-6
            assert (nm["x"] == x1) if nm["anchor"] == "start" else (nm["x"] == x0)
            for m, other in names.items():
                bx0, by0, bx1, by1 = other["box"]
                assert m == n or x1 <= bx0 or bx1 <= x0 or y1 <= by0 or by1 <= y0, (compact, n, m)
            for ln in px["lines"]:
                bx, by = ln["badge"]
                assert x1 <= bx - 12 or bx + 12 <= x0 or y1 <= by - 12 or by + 12 <= y0, (compact, n, "square", ln["n"])
                for cx, cy in ln["pts"]:       # r + 4: an interchange (r + 2) with its ring
                    near = (max(x0 - cx, 0, cx - x1) ** 2 + max(y0 - cy, 0, cy - y1) ** 2) ** 0.5
                    assert near >= r + 4, (compact, n, "station of", ln["n"])
                for (ax, ay), (qx, qy) in zip([ln["badge"]] + ln["pts"], ln["pts"]):
                    steps = int(max(abs(qx - ax), abs(qy - ay)) * 2) + 1
                    for i in range(steps + 1):
                        x, y = ax + (qx - ax) * i / steps, ay + (qy - ay) * i / steps
                        assert not (x0 - 3.5 < x < x1 + 3.5 and y0 - 3.5 < y < y1 + 3.5), (compact, n, "line", ln["n"])


def test_metro_long_name_breaks_in_two():
    """A name with no room on one line breaks at the space nearest its middle, by rule."""
    px = {"width": 200, "height": 200, "lines": [
        {"n": 0, "pts": [(100, 100), (46, 100)], "badge": (154, 100)},
        {"n": 1, "pts": [(46, 46), (46, 100), (46, 154)], "badge": (46, -8)}]}
    names = hook.maps_metro_names(px, {0: "אילוצים ואקראיות ב-SystemVerilog", 1: "קצר"}, 13)
    assert [t for t, _ in names[0]["rows"]] == ["אילוצים ואקראיות", "ב-SystemVerilog"]
    assert names[0]["anchor"] == "start" and names[1]["rows"][0][0] == "קצר"


def test_metro_map_html():
    """The map's SVG: a name per line with direction="rtl", inside the line's link; every
    station carries what its card shows; the scroll hint and the card are there, hidden."""
    hook._questions = hook._load_questions(DOCS)
    hook._paths = hook._load_paths(DOCS)
    out = hook.maps_metro("paths/")
    assert out.count('<a class="mm-badge"') == len(hook._paths)
    assert len(re.findall(r'<text class="mm-lname mm-c\d+(?: is-end)?" x="[-\d.]+" y="[-\d.]+" direction="rtl">', out)) >= len(hook._paths)
    for st in re.findall(r'<a class="mm-st[^>]*>', out):
        assert all(f' data-{k}="' in st for k in ("id", "lines", "kind", "level", "diff", "title")), st
    assert '<button type="button" class="mm-more" hidden>' in out
    assert '<div class="mm-card" id="mm-card" role="tooltip" hidden></div>' in out
    assert 'id="mm-card-compact"' in hook.maps_metro("", compact=True)


def test_path_rows():
    """The paths page: a row per path with its number, a name that is never cut, the
    description whole in the title, the counts, and the link to its first question."""
    hook._questions = hook._load_questions(DOCS)
    hook._paths = hook._load_paths(DOCS)
    out = hook._path_rows("paths/")
    assert out.count('<li class="path-row">') == len(hook._paths)
    p = hook._paths[0]
    first = hook._href(p["steps"][0]["q"]["src_uri"], "paths/")
    assert f'<a class="pr-go" href="{first}"' in out
    assert f'data-ids="{" ".join(s["q"]["id"] for s in p["steps"])}"' in out
    for m in re.finditer(r'data-ids="([^"]*)" data-hrefs="([^"]*)"', out):
        assert len(m.group(1).split()) == len(m.group(2).split())


def test_added_date_quoted_or_not():
    day = hook.dt.date(2026, 10, 28)
    for added in (day, hook.dt.datetime(2026, 10, 28, 9, 30), "2026-10-28", " 2026-10-28 "):
        assert hook._added_date({"added": added}) == day, added
    for added in (None, "", 20261028):
        assert hook._added_date({"added": added}) is None, added


def test_renumbered_lists_agree():
    """The renumbered questions of mkdocs.yml (the 404 page's redirects) and of marks.js
    (the marks moved in the browser) are the same list."""
    yml = re.search(r"^  dvq_renumbered:\n((?:    \"\d{4}\": \"\d{4}\"\n)+)", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"), re.M)
    js = re.search(r"RENUMBERED = \[\[\"[\d-]+\", (\{[^}]*\})\]\]", (DOCS / "javascripts" / "marks.js").read_text(encoding="utf-8"))
    assert yml and js
    assert dict(re.findall(r'"(\d{4})": "(\d{4})"', yml.group(1))) == dict(re.findall(r'"(\d{4})": "(\d{4})"', js.group(1)))
    moved = dict(re.findall(r'"(\d{4})": "(\d{4})"', yml.group(1)))
    ids = {p.name[:4] for p in (DOCS / "questions").rglob("*.md") if p.name[:4].isdigit()}
    assert set(moved.values()) <= ids


VIDEO_PAGE = """---
id: 999
title: שאלת ניסיון
level: student
difficulty: easy
kind: code
tags: [math]
added: 2026-10-30
video: abcdefghijk
video_parts: [0, 95, 3725]
---

## השאלה

ניסוח.

### סעיף א – ראשון

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        א.

### סעיף ב – שני

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ב.

??? success "פתרון שני לסעיף ב"
    !!! answer "תשובה בקצרה"
        ב2.

### סעיף ג – שלישי

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ג.
"""


def video_docs(tmp_path, page=VIDEO_PAGE):
    (tmp_path / "questions" / "student").mkdir(parents=True)
    (tmp_path / "questions" / "student" / "0999-try.md").write_text(page, encoding="utf-8")
    return tmp_path


def test_video_tool_and_chapter_links(tmp_path):
    """A page with a (fake) video gets the "סרטון הסבר" tool and one "לפרק בסרטון" link at
    the top of each part's first solution, with the chapter's start (V3)."""
    hook._questions = hook._load_questions(video_docs(tmp_path))
    hook._paths = []
    q = hook._questions["questions/student/0999-try.md"]
    assert q["video_chapters"] == [("א", 0), ("ב", 95), ("ג", 3725)]
    tools = hook._tools(q, "questions/student/0999-try/")
    btn = re.search(r'<button type="button" class="qt-btn qt-video"[^>]*>', tools).group(0)
    assert 'aria-label="סרטון הסבר"' in btn and 'data-video="abcdefghijk"' in btn and 'aria-haspopup="dialog"' in btn
    assert html_unescape(re.search(r'data-video-chapters="([^"]*)"', btn).group(1)) == '[["א", 0], ["ב", 95], ["ג", 3725]]'
    assert tools.index("qt-video") < tools.index("qt-fold")         # the first tool
    built = "".join(f'<h3 id="_{i}">סעיף {k} – x</h3>\n<details class="success">\n<summary>פתרון סעיף {k}</summary>\n<p>תשובה</p>\n</details>\n'
                    for i, k in enumerate("אבג"))
    built = built.replace("</details>\n<h3 id=\"_2\"", '</details>\n<details class="success">\n<summary>פתרון שני</summary>\n</details>\n<h3 id="_2"')
    out = hook.video_links(built, q)
    links = re.findall(r'<div class="video-chapter".*?</div>', out)
    assert len(links) == 3
    assert [re.search(r'data-video-start="(\d+)"', a).group(1) for a in links] == ["0", "95", "3725"]
    assert [re.search(r'<span class="vc-time" dir="ltr">([^<]+)</span>', a).group(1) for a in links] == ["0:00", "1:35", "1:02:05"]
    assert 'href="https://www.youtube.com/watch?v=abcdefghijk&amp;t=95s"' in links[1]
    assert all(HEBREW.match(re.sub(r"<[^>]+>", "", a)) for a in links)            # RTL: the words first
    assert out.count('<summary>פתרון סעיף ב</summary>\n<div class="video-chapter"') == 1
    assert '<summary>פתרון שני</summary>\n<div class="video-chapter"' not in out    # one link per part
    assert hook.video_links(built, {"src_uri": "x"}) == built                    # no video, no change
    try:
        hook.video_links(built.replace("סעיף ג", "סעיף"), q)
    except hook.PluginError as e:
        assert "video chapters" in str(e)
    else:
        raise AssertionError("a part count that differs from video_parts must fail the build")


def test_video_on_a_page_without_parts(tmp_path):
    page = VIDEO_PAGE.split("### סעיף א")[0].replace("video_parts: [0, 95, 3725]\n", "") + (
        '??? success "פתרון"\n    !!! answer "תשובה בקצרה"\n        כן.\n')
    hook._questions = hook._load_questions(video_docs(tmp_path, page))
    q = hook._questions["questions/student/0999-try.md"]
    assert q["video_chapters"] == [("", 0)]
    out = hook.video_links('<h2 id="_1">השאלה</h2>\n<details class="success">\n<summary>פתרון</summary>\n</details>\n', q)
    assert '<summary>פתרון</summary>\n<div class="video-chapter"' in out and "לסרטון ההסבר" in out and "vc-time" not in out


def test_video_fields_fail_the_build(tmp_path):
    for bad, says in (("video: abc", "not a YouTube id"), ("video_parts: [0, 95]", "2 times but the page has 3 parts"),
                      ("video_parts: [5, 95, 210]", "must start at 0"), ("video_parts: [0, 95, 95]", "must rise")):
        field = "video: abcdefghijk" if bad.startswith("video:") else "video_parts: [0, 95, 3725]"
        page = VIDEO_PAGE.replace(field, bad)
        root = tmp_path / str(len(says))
        try:
            hook._load_questions(video_docs(root, page))
        except hook.PluginError as e:
            assert says in str(e), (bad, str(e))
        else:
            raise AssertionError(f"{bad} must fail the build")


def test_no_real_page_has_a_fake_video():
    for page in (DOCS / "questions").rglob("*.md"):
        assert "abcdefghijk" not in page.read_text(encoding="utf-8"), page.name


def html_unescape(s):
    import html
    return html.unescape(s)


def test_question_chip():
    """A question's chip (22-circuit.css): the same id and parts give the same chip; one pin a
    side per part (1 to 6), and the die's lit cells read the id in binary, MSB first."""
    pins = re.compile(r'class="qc-pins" d="([^"]*)"')
    cells = lambda svg, cls: re.findall(r"M[\d.]+ [\d.]+h3v3h-3z", (re.search(rf'class="{cls}" d="([^"]*)"', svg) or ["", ""])[1])  # noqa: E731
    assert hook.question_chip("0080", 4) == hook.question_chip("0080", 4)
    assert hook.question_chip("0080", 4) != hook.question_chip("0081", 4)
    for parts, n in ((0, 1), (1, 1), (3, 3), (4, 4), (9, 6)):
        svg = hook.question_chip("0080", parts)
        assert pins.search(svg).group(1).count("h5v2.4h-5z") == 2 * n
    for qid in ("0001", "0080", "0255", "9999"):
        svg = hook.question_chip(qid, 2)
        assert len(cells(svg, "qc-on")) == bin(int(qid)).count("1") and 'class="qc-die"' in svg
        assert 'aria-hidden="true"' in svg and "fill=" not in svg and "style=" not in svg   # colours from the stylesheet
    # the bits read in order: 0080 = 0000 0000 0101 0000 lights the cells 9 and 11 of 16
    order = [f"M{hook._n(11.6 + c * 4.4)} {hook._n(8 + r * 4.4)}h3v3h-3z" for r in range(4) for c in range(4)]
    lit = cells(hook.question_chip("0080", 1), "qc-on")
    assert [order.index(x) for x in lit] == [9, 11]
    assert hook.part_number("0080") == "DVQ‑0080"


def test_every_question_page_has_its_chip():
    hook._questions = hook._load_questions(DOCS)
    for q in hook._questions.values():
        assert q["parts"] >= 0
        header = hook._header(q, "", "questions/x/y/")
        assert hook.question_chip(q["id"], q["parts"]) in header and hook.part_number(q["id"]) in header


def test_revision_date(tmp_path):
    """The footer's board line (24-living.css): the date of the last commit, the build day
    outside a git checkout."""
    import datetime as dt
    rev = hook._revision_date(DOCS)
    assert isinstance(rev, dt.date) and rev <= dt.date.today() + dt.timedelta(days=1)   # Israel is ahead of UTC
    assert hook._revision_date(tmp_path) == dt.date.today()


# ---- the lists of the UX round (session 34): one-line rows, one row of filters, the home page

def _fresh():
    hook._questions = hook._load_questions(DOCS)
    return hook._questions


def test_split_title():
    assert hook.split_title("רווח מקסימלי ממניה – לונג או שורט") == ("רווח מקסימלי ממניה", "לונג או שורט")
    assert hook.split_title("סוגריים תקינים") == ("סוגריים תקינים", "")
    assert hook.split_title("א – ב – ג") == ("א", "ב – ג")          # only the first dash splits
    assert hook.split_title("טווח 1-5") == ("טווח 1-5", "")           # a hyphen is not the dash


def test_table_rows_are_one_line():
    qs = _fresh()
    out = hook._table(None, "all/")
    rows = re.findall(r"<tr data-id=.*?</tr>", out, re.S)
    assert len(rows) == len(qs)
    by_id = {q["id"]: q for q in qs.values()}
    with_sub = 0
    for row in rows:
        q = by_id[re.search(r'data-id="(\d{4})"', row).group(1)]
        main, sub = hook.split_title(q["title"])
        link = re.search(r'<a href="[^"]+" title="([^"]*)">([^<]*)</a>', row)
        assert hook.html.unescape(link.group(1)) == str(q["title"]) and hook.html.unescape(link.group(2)) == main
        m = re.search(r'<span class="q-sub">([^<]*)</span>', row)
        assert (hook.html.unescape(m.group(1)) if m else "") == sub
        with_sub += bool(sub)
        # the search still finds a row by its whole title and by its topics, in both names
        data = hook.html.unescape(re.search(r'data-search="([^"]*)"', row).group(1))
        assert str(q["title"]).lower() in data and all(t in data for t in q["tags"])
        assert 'class="q-marks"' in row and "chip-level" in row and "chip-diff" in row
    assert with_sub and with_sub < len(rows)
    # no question chip, no kind chip and no topics in a row (the owner's choice)
    body = out[out.index("<tbody>"):]
    assert not re.search(r"qchip|q-meta|q-topic|chip-kind", body)
    assert "chip-level" not in hook._table("junior", "questions/junior/").split("<tbody>")[1]


def test_filters_are_one_row_of_dropdowns():
    _fresh()
    for level, names in ((None, ["level", "difficulty", "kind", "mark", "tag"]), ("senior", ["difficulty", "kind", "mark", "tag"])):
        out = hook._table(level, "x/")
        head = out[:out.index("<table>")]
        groups = re.findall(r'<div class="filter-group filter-dd[^"]*" data-filter="(\w+)" data-value="">(.*?)</div></div>', head, re.S)
        assert [g[0] for g in groups] == names
        ids = set()
        for name, inner in groups:
            btn = re.search(r'<button type="button" class="dd-btn" aria-expanded="false" aria-controls="([\w-]+)">', inner)
            pop = re.search(r'<div class="dd-pop" id="([\w-]+)" role="group" aria-label="([^"]+)" hidden>', inner)
            assert btn and pop and btn.group(1) == pop.group(1), name
            assert HEBREW.match(pop.group(2))
            ids.add(pop.group(1))
            chips = re.findall(r'<button type="button" class="filter-chip[^"]*" data-value="([^"]*)" aria-pressed="(true|false)"', inner)
            assert chips[0] == ("", "true") and all(p == "false" for _, p in chips[1:])   # "all" is the choice at first
            assert len(chips) >= 3
        assert len(ids) == len(names)
        # every topic of the table is a choice, not only the common ones
        tags = {t for q in hook._questions.values() if level in (None, q["level"]) for t in q["tags"]}
        topic = dict(groups)["tag"]
        assert set(re.findall(r'data-value="([^"]+)"', topic)) == tags
        assert "filter-toggle" not in head and "filter-panel" not in head and "topics-toggle" not in head
        assert head.count('class="filter-random"') == 1 and head.count("<select>") == 1
        assert head.index("filter-search") < head.index("filter-dds") < head.index("filter-random") < head.index("filter-active")


def test_home_steps_line_and_catalog_button():
    qs = _fresh()
    how = hook._how_it_works()
    assert how.startswith('<ol class="how-line"') and how.count("<li>") == 3 and "<h2" not in how
    for icon, text in hook.HOW_STEPS:
        assert HEBREW.match(text) and f"ui-ico-{icon}" in how and text in how
    recent = hook._recent("")
    more = recent[recent.index('<p class="recent-more">'):]
    assert f"לכל {len(qs)} השאלות</a>" in more and 'href="all/"' in more and 'href="new/"' in more
    home = (DOCS / "index.md").read_text(encoding="utf-8")
    assert "catalog-link" not in home and "## איך זה עובד" not in home and "## כל השאלות" not in home
    assert home.index("<!-- /hero -->") < home.index("<!-- how-it-works -->") < home.index("<!-- home-continue -->")
    assert not hasattr(hook, "_catalog_link")


def test_list_pages_take_their_title_from_the_band():
    """A level page was titled "Index": the band wraps its "# title", so MkDocs found no
    heading at the top of the page and fell back to the file name."""
    _fresh()

    class Page:
        def __init__(self, meta):
            self.meta = meta

    for level, name in hook.LEVELS.items():
        page = Page({})
        text = (DOCS / "questions" / level / "index.md").read_text(encoding="utf-8")
        out = hook._lists_top(text, page)
        assert page.meta["title"] == name and 'class="list-band lb-level"' in out
    page = Page({"title": "שם אחר"})
    hook._lists_top("# כל השאלות\n\nשורה.\n\n<!-- questions-table -->\n", page)
    assert page.meta["title"] == "שם אחר"            # a title the page gives stays
    page = Page({})
    hook._lists_top("# דף רגיל\n\nבלי טבלה.\n", page)
    assert "title" not in page.meta
    # a page that opens with front matter only, then the heading, as the real pages do
    for path in [DOCS / "all.md", *(DOCS / "paths").glob("*.md"), DOCS / "tags.md", DOCS / "new.md"]:
        body = re.sub(r"\A---\n.*?\n---\n+", "", path.read_text(encoding="utf-8"), flags=re.S)
        assert body.startswith("# ") or re.search(r"^title:", path.read_text(encoding="utf-8"), re.M), path.name



# --- the question page of the UX round (session 34) ------------------------------------------

def test_box_chip_and_teaser():
    """A page with an explorer box gets a button chip in its header, and, when its first box
    sits inside a closed block, a teaser button right under the statement."""
    _fresh()
    q = next(iter(hook._questions.values()))
    with_box = '## השאלה\n\nניסוח.\n\n<div class="explorer" data-kind="kaprekar"></div>\n'
    head = hook._header(q, with_box, "questions/x/0001-y/")
    assert '<button type="button" class="qh-badge qh-badge-play qh-box-go" data-box-go' in head
    assert "תיבה אינטראקטיבית" in head
    assert "qh-box-go" not in hook._header(q, "## השאלה\n\nניסוח.\n", "questions/x/0001-y/")
    box = '<div class="explorer" data-kind="kaprekar"></div>'
    closed = ('<article><h2 id="a">השאלה</h2><p>ניסוח</p>\n<details class="interviewer"><summary>מה המראיין בודק</summary></details>\n'
              f'<details class="success"><summary>פתרון</summary>{box}</details></article>')
    out = hook.box_teaser(closed)
    assert out.count('class="box-teaser"') == 1
    assert out.index('class="box-teaser"') < out.index('<details class="interviewer"')    # under the statement
    assert HEBREW.match(re.search(r'class="bt-go">([^<]+)', out).group(1))
    # a page without the interviewer block: before its first part
    parts = f'<article><p>ניסוח</p>\n<h3 id="p">סעיף א</h3><details class="success"><summary>פתרון</summary>{box}</details></article>'
    assert hook.box_teaser(parts).index('class="box-teaser"') < hook.box_teaser(parts).index('<h3 id="p">')
    # a box in the open (visible on load), or no box: no teaser
    assert hook.box_teaser(f'<article><p>ניסוח</p>{box}<details class="interviewer"></details></article>').count("box-teaser") == 0
    assert hook.box_teaser(f'<article><details class="tip"><summary>רמז</summary></details>{box}</article>').count("box-teaser") == 0
    assert hook.box_teaser("<article><p>ניסוח</p></article>") == "<article><p>ניסוח</p></article>"


def test_closed_solution_reads_show():
    """The summary of a solution keeps its text and gets the words of the closed state in
    spans ("הצג פתרון · סעיף א"); other blocks and other titles are left alone."""
    page = ('<details class="success">\n<summary>פתרון סעיף א</summary>\n</details>'
            '<details class="success"><summary>פתרון</summary></details>'
            '<details class="success"><summary>פתרון 2 – טבלה</summary></details>'
            '<details class="success"><summary>הוכחה</summary></details>'
            '<details class="tip"><summary>פתרון חלקי</summary></details>')
    out = hook.solution_summaries(page)
    show, dot = '<span class="sol-closed">הצג </span>', '<span class="sol-closed"> ·</span>'
    assert f"<summary>{show}פתרון{dot} סעיף א</summary>" in out
    assert f"<summary>{show}פתרון</summary>" in out
    assert f"<summary>{show}פתרון 2 – טבלה</summary>" in out
    assert "<summary>הוכחה</summary>" in out and "<summary>פתרון חלקי</summary>" in out
    assert re.sub(r'<span class="sol-closed">[^<]*</span>', "", out) == page      # the open text is the old one


def test_end_card():
    """The end card: the step in the first path of the question and its next question, a
    closing line on the path's last question, and the page's next question without a path."""
    _fresh()
    hook._paths = hook._load_paths(DOCS)
    path = hook._paths[0]
    first, last = path["steps"][0]["q"], path["steps"][-1]["q"]
    # the questions whose first path is this one (the card and the path strip agree on it)
    own = lambda q: next(p for p in hook._paths if q["id"] in [s["q"]["id"] for s in p["steps"]]) is path
    assert own(first)
    card = hook._end_card(first, "questions/x/0001-y/")
    assert card.startswith("\n\n<div class=\"q-end-slot\" aria-live=\"polite\"") and '<section class="q-end"' in card and " hidden>" in card
    assert f"שלב 1 מתוך {len(path['steps'])} במסלול" in card and hook.html.escape(path["title"]) in card
    nxt = path["steps"][1]["q"]
    assert "השאלה הבאה במסלול" in card and f'<span class="qe-nid">{nxt["id"]}</span>' in card
    assert "שאלה דומה" not in card
    if own(last):
        done = hook._end_card(last, "questions/x/0001-y/")
        assert "qe-next" not in done and "paths/" in done and "האחרונה במסלול" in done

    class File:
        def __init__(self, src_uri):
            self.src_uri = src_uri

    class Page:
        def __init__(self, src_uri):
            self.file = File(src_uri)

    saved, hook._paths = hook._paths, []
    try:
        other = hook._end_card(first, "questions/x/0001-y/", Page(nxt["src_uri"]))
        assert "במסלול" not in other and f'<span class="qe-nid">{nxt["id"]}</span>' in other and "השאלה הבאה" in other
        end = hook._end_card(first, "questions/x/0001-y/", Page("new.md"))      # the level's last page
        assert "qe-next" not in end and "האחרונה ברמה" in end
    finally:
        hook._paths = saved
    # the path strip: the step also in its short form for a phone
    strip = hook._path_nav(first, "questions/x/0001-y/")
    assert f'<span class="pn-step-short" dir="ltr" aria-hidden="true">1/{len(path["steps"])}</span>' in strip
