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


def test_cost_chips():
    md = "??? success \"x\"\n    !!! answer \"y\"\n        z\n\n    <!-- cost: זמן \\( O(n) \\) | פלופים 2 -->\n"
    out = hook.COST_LINE.sub(hook._cost_chips, md)
    assert ('    <div class="cost-chips" role="note" aria-label="סיבוכיות" data-search-exclude>'
            '<span class="cost-chip"><b>זמן</b> \\( O(n) \\)</span>'
            '<span class="cost-chip"><b>פלופים</b> 2</span></div>\n') in out
    assert "<!--" not in out
