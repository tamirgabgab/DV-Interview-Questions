"""Tests of the site hook (hooks/questions.py): Hebrew search variants and study paths."""

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
