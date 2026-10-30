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
    assert tags == [*hook.WAVEDROM_CDN, "../../../javascripts/wavedrom-init.js"]
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
    page = ('<p>intro</p><h2 id="tag:bfs"><span class="md-tag">BFS</span></h2>\n<ul><li>a</li><li>b</li></ul>'
            '<h2 id="tag:cdc"><span class="md-tag">CDC</span></h2>\n<ul><li>c</li></ul>')
    out = hook._tag_grid(page)
    assert out.index('<nav class="tag-grid"') < out.index('<details class="tag-section" id="tag:bfs">')
    assert '<a class="tag-chip" href="#tag:bfs">BFS<span class="tag-count" aria-label="2 שאלות">2</span></a>' in out
    assert out.count('<ul class="tag-list">') == 2 and "<h2" not in out


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
