"""Tests of tools/checks/check_videos.py: the video fields of a page (notes/VIDEOS.md)."""

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
    assert cv.video_problems({"video": "abcdefghijk"}, "## השאלה\n") == []              # chapters are optional
    assert cv.video_problems({"video": "abcdefghijk"}, BODY3) == []
    assert cv.video_problems({"video": "abcdefghijk", "video_parts": [0]}, "## השאלה\n") == []
    cases = [
        ({"video_parts": [0]}, "without 'video'"),
        ({"video": "abcdefghij", "video_parts": [0, 95, 210]}, "not a YouTube id"),
        ({"video": "abcdefgh!jk", "video_parts": [0, 95, 210]}, "not a YouTube id"),
        ({"video": 12345678901, "video_parts": [0, 95, 210]}, "quote it"),
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


def test_check_over_a_tree(tmp_path):
    def write(rel, text):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    write("docs/questions/student/0002-swap.md", "---\nid: 2\nvideo: abcdefghijk\nvideo_parts: [0, 95, 210]\n---\n" + BODY3)
    write("docs/questions/student/0003-plain.md", "---\nid: 3\n---\n## השאלה\n")
    assert cv.check(tmp_path) == []
    write("docs/questions/student/0004-bad.md", "---\nid: 4\nvideo: abc\n---\n## השאלה\n")
    assert cv.check(tmp_path) == ["docs/questions/student/0004-bad.md: 'video' is not a YouTube id "
                                  "(11 characters of A-Z a-z 0-9 _ -): 'abc'"]
