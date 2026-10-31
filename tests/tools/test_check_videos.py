"""Tests of tools/check_videos.py: the video fields of a page, the chapters of a script and
the RTL rules of its captions (VIDEOS.md)."""

import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools"))
import check_videos as cv  # noqa: E402

NB = " "
BODY3 = "## השאלה\n\n### סעיף א – x\n\n```python\n### סעיף ז – in code, not a part\n```\n\n### סעיף ב – y\n\n### סעיף ג – z\n"


def test_part_letters():
    assert cv.part_letters(BODY3) == ["א", "ב", "ג"]
    assert cv.part_letters("## השאלה\n\nבלי סעיפים.\n") == []


def test_video_fields():
    ok = {"video": "abc-DEF_123", "video_parts": [0, 95, 210]}
    assert cv.video_problems(ok, BODY3) == []
    assert cv.video_problems({}, BODY3) == []
    assert cv.video_problems({"video": "abcdefghijk"}, "## השאלה\n") == []              # one part: may be left out
    assert cv.video_problems({"video": "abcdefghijk", "video_parts": [0]}, "## השאלה\n") == []
    cases = [
        ({"video_parts": [0]}, "without 'video'"),
        ({"video": "abcdefghij", "video_parts": [0, 95, 210]}, "not a YouTube id"),
        ({"video": "abcdefgh!jk", "video_parts": [0, 95, 210]}, "not a YouTube id"),
        ({"video": 12345678901, "video_parts": [0, 95, 210]}, "quote it"),
        ({"video": "abcdefghijk"}, "'video_parts' is missing"),
        ({"video": "abcdefghijk", "video_parts": [0, 95]}, "2 times but the page has 3 parts"),
        ({"video": "abcdefghijk", "video_parts": [3, 95, 210]}, "must start at 0"),
        ({"video": "abcdefghijk", "video_parts": [0, 210, 95]}, "must rise"),
        ({"video": "abcdefghijk", "video_parts": [0, 95, 95]}, "must rise"),
        ({"video": "abcdefghijk", "video_parts": "0, 95, 210"}, "list of whole seconds"),
        ({"video": "abcdefghijk", "video_parts": [0, 9.5, 210]}, "list of whole seconds"),
    ]
    for meta, says in cases:
        got = cv.video_problems(meta, BODY3)
        assert any(says in p for p in got), (meta, got)


def test_script_chapters_and_captions():
    script = ("# 0002\n\n## Opening\n\n> שתי קופסאות" + NB + ": a ו-b.\n\n## Chapter א — temp\n\n"
              "> ‏temp = a שומר את הערך.\n\n```text\n> not a caption\n## Chapter in code\n```\n\n"
              "## Chapter ב\n\n> בשעה 1:35 ובקוד `a:b` אין רווח.\n\n## Closing\n")
    assert cv.script_chapters(script) == 2
    assert [n for n, _ in cv.captions(script)] == [5, 9, 18]


def test_caption_rules():
    assert cv.caption_problems("שלוש השמות" + NB + ": temp, a ו-b.") == []
    assert cv.caption_problems("‏temp = a שומר את הערך.") == []
    assert cv.caption_problems("ראו https://example.org ובשעה 12:30.") == []
    assert cv.caption_problems("הקוד `x: int` נשאר כמו שהוא.") == []
    assert cv.caption_problems("") == []
    assert any("Hebrew letter" in p for p in cv.caption_problems("temp שומר את הערך."))
    assert any("Hebrew letter" in p for p in cv.caption_problems("3 צעדים."))
    assert any("non-breaking space" in p for p in cv.caption_problems("שלוש השמות : temp."))
    assert any("non-breaking space" in p for p in cv.caption_problems("שלוש השמות: temp."))
    assert any("ordinary space after" in p for p in cv.caption_problems("שלוש השמות" + NB + ":temp."))
    assert cv.caption_problems("א ב ג ד ה ו ז ח ט י כ ל") == []                      # 12 words
    assert any("13 words" in p for p in cv.caption_problems("א ב ג ד ה ו ז ח ט י כ ל מ"))
    assert cv.caption_problems("א ב ג ד ה ו ז ח ט י כ" + NB + ": ל") == []           # the colon is no word


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_check_over_a_tree(tmp_path):
    page = "---\nid: 2\nvideo: abcdefghijk\nvideo_parts: [0, 95, 210]\n---\n" + BODY3
    write(tmp_path, "docs/questions/student/0002-swap.md", page)
    write(tmp_path, "docs/questions/student/0003-plain.md", "---\nid: 3\n---\n## השאלה\n")
    problems, warnings = cv.check(tmp_path)
    assert problems == [] and warnings == ["docs/questions/student/0002-swap.md: videos/0002/script.md does not exist yet"]
    write(tmp_path, "videos/0002/script.md", "## Opening\n\n## Chapter א\n\n> טוב.\n\n## Chapter ב\n\n> bad start\n\n## Closing\n")
    problems, warnings = cv.check(tmp_path)
    assert warnings == []
    assert problems == ["docs/questions/student/0002-swap.md: videos/0002/script.md has 2 '## Chapter' headings, the page has 3 parts",
                        "videos/0002/script.md:9: starts with neither a Hebrew letter nor the RLM mark (U+200F): 'bad start'"]



def test_english_captions(tmp_path):
    script = ("## Opening\n\n> שלב 1" + NB + ": temp = a.\n\n## Chapter א\n\n"
              "> שלב 2" + NB + ": a = b. עכשיו a מחזיק 3,\n> וה-5 המקורי שמור.\n\n## Closing\n")
    assert cv.caption_texts(script) == ["שלב 1" + NB + ": temp = a.",
                                        "שלב 2" + NB + ": a = b. עכשיו a מחזיק 3,\nוה-5 המקורי שמור."]
    one = "he: שלב 1" + NB + ": temp = a.\nen: Step 1: temp = a.\n"
    two = ("he: שלב 2" + NB + ": a = b. עכשיו a מחזיק 3,\nhe: וה-5 המקורי שמור.\n"
           "en: Step 2: a = b. Now a holds 3,\nen: and the original 5 is saved.\n")
    good = "# 0002: the English captions\n\n" + one + "\n" + two
    assert cv.translation_problems(script, good) == []

    def says(translations, text):
        got = cv.translation_problems(script, translations)
        assert any(text in p for p in got), got

    says(one, "no English entry for the caption")                              # a caption left out
    says(good + "\nhe: שלב 3" + NB + ": נמחק.\nen: Step 3: gone.\n", "no longer exists")
    says(two + "\n" + one, "not in the captions' order")
    says(one + "\n" + two.replace("en: and", "en: and the value five, which was, until now, saved in temp, is still"),
         "words in an English line")
    says(one + "\n" + two + "en: a third line.\n", "3 English lines")
    says(one.replace("Step 1", "שלב 1") + "\n" + two, "Hebrew in an English line")
    says(one.split("en:")[0] + "\n" + two, "no 'en:' line")
    says(one + "\nhello\n" + two, "neither 'he:', 'en:'")

    write(tmp_path, "videos/0002/script.md", script)
    write(tmp_path, "videos/0002/captions.en.md", one)
    problems, _ = cv.check(tmp_path)
    assert len(problems) == 1 and problems[0].startswith("videos/0002/captions.en.md: no English entry"), problems
    write(tmp_path, "videos/0002/captions.en.md", good)
    assert cv.check(tmp_path)[0] == []
