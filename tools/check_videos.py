#!/usr/bin/env python3
"""Check the tutorial videos' fields on the pages and the captions of their scripts (VIDEOS.md).

    python tools/check_videos.py          # every page and every videos/*/script.md

Needs no video and no network. For every question page with a ``video:`` field:

- the id has the YouTube form (11 characters of ``A-Z a-z 0-9 _ -``, quoted when YAML
  would read it as a number or a boolean);
- ``video_parts`` has one start time (whole seconds) per part (``### סעיף ...``), rising
  from 0; a page with one part may leave it out;
- ``videos/<id>/script.md`` exists (a warning until it does) and has one ``## Chapter ...``
  heading per part (``## Opening`` and ``## Closing`` are not chapters).

For every ``videos/*/script.md``, every caption line (a line that starts with ``> ``, see
VIDEOS.md) follows the RTL rules of CLAUDE.md: it starts with a Hebrew letter or the RLM
mark (U+200F), every colon has a non-breaking space (U+00A0) before it and an ordinary
space or the end of the line after it (times such as 1:35, URLs and `code` are exempt),
and it has at most 12 words.

The same field checks run in tools/lint_pages.py and in the build hook, which import
``video_problems`` from here. Exit status 1 on a problem; a missing script is a warning.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "docs" / "questions"
VIDEOS = ROOT / "videos"

VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
PART_HEADING = re.compile(r"^### סעיף\s+([א-ת])")
CHAPTER_HEADING = re.compile(r"^## Chapter\b")
FENCE = re.compile(r"^\s*(```|~~~)")
CAPTION = re.compile(r"^> (.*)$")
HEBREW_START = re.compile(r"^[א-ת]")
RLM = "‏"
NBSP = " "
MAX_WORDS = 12


def split_front_matter(text: str) -> tuple[dict, str]:
    """The page's front matter as a dict, and the body after it."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return yaml.safe_load(text[3:end]) or {}, text[end + 4:]
    return {}, text


def _outside_fences(text: str):
    """The lines of text that are not inside a fenced code block, with their numbers."""
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield n, line


def part_letters(body: str) -> list[str]:
    """The letters of the page's parts (``### סעיף א ...``), in order; [] for a page
    without parts."""
    return [m.group(1) for _, line in _outside_fences(body) if (m := PART_HEADING.match(line))]


def video_problems(meta: dict, body: str) -> list[str]:
    """What is wrong with the page's ``video`` and ``video_parts`` fields ([] when both are
    absent or right)."""
    if "video" not in meta:
        return ["'video_parts' without 'video'"] if "video_parts" in meta else []
    out = []
    vid = meta["video"]
    if not isinstance(vid, str):
        out.append(f"'video' must be a YouTube id as a string (quote it): {vid!r}")
    elif not VIDEO_ID.match(vid):
        out.append(f"'video' is not a YouTube id (11 characters of A-Z a-z 0-9 _ -): {vid!r}")
    parts = max(1, len(part_letters(body)))
    times = meta.get("video_parts")
    if times is None:
        if parts > 1:
            out.append(f"'video_parts' is missing: the page has {parts} parts, so it needs {parts} start times")
        return out
    if not isinstance(times, list) or not all(isinstance(t, int) and not isinstance(t, bool) for t in times):
        return out + [f"'video_parts' must be a list of whole seconds, e.g. [0, 95, 210]: {times!r}"]
    if len(times) != parts:
        out.append(f"'video_parts' has {len(times)} times but the page has {parts} part{'s' * (parts > 1)}")
    if times and times[0] != 0:
        out.append(f"'video_parts' must start at 0: {times!r}")
    if any(b <= a for a, b in zip(times, times[1:])):
        out.append(f"'video_parts' must rise: {times!r}")
    return out


def script_chapters(text: str) -> int:
    """The number of chapters of a script.md: its ``## Chapter ...`` headings."""
    return sum(1 for _, line in _outside_fences(text) if CHAPTER_HEADING.match(line))


def captions(text: str) -> list[tuple[int, str]]:
    """The caption lines of a script.md (``> ...``), with their line numbers."""
    return [(n, m.group(1).rstrip()) for n, line in _outside_fences(text) if (m := CAPTION.match(line))]


def caption_problems(line: str) -> list[str]:
    """What breaks the RTL rules in one caption line."""
    out = []
    if not line.strip():
        return out
    if not (HEBREW_START.match(line) or line.startswith(RLM)):
        out.append("starts with neither a Hebrew letter nor the RLM mark (U+200F)")
    plain = re.sub(r"`[^`]*`", lambda m: "x" * len(m.group(0)), line)     # code keeps its colons
    for i, ch in enumerate(plain):
        if ch != ":":
            continue
        before, after = plain[i - 1] if i else "", plain[i + 1] if i + 1 < len(plain) else ""
        if before.isdigit() and after.isdigit():
            continue                                    # a time or a ratio: 1:35, 3:2
        if plain.startswith("//", i + 1):
            continue                                    # a URL
        if before != NBSP:
            out.append(f"a colon without a non-breaking space (U+00A0) before it, at column {i + 1}")
        elif after not in ("", " "):
            out.append(f"a colon without an ordinary space after it, at column {i + 1}")
    words = [w for w in line.replace(NBSP, " ").split() if re.search(r"\w", w)]
    if len(words) > MAX_WORDS:
        out.append(f"{len(words)} words, more than {MAX_WORDS} in one line")
    return out


def check(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """(problems, warnings) of every page with a video and every script.md under root."""
    problems: list[str] = []
    warnings: list[str] = []
    for page in sorted((root / "docs" / "questions").glob("*/0*.md")):
        meta, body = split_front_matter(page.read_text(encoding="utf-8"))
        name = page.relative_to(root).as_posix()
        problems += [f"{name}: {p}" for p in video_problems(meta, body)]
        if "video" not in meta:
            continue
        qid = f"{int(meta['id']):04d}"
        parts = max(1, len(part_letters(body)))
        script = root / "videos" / qid / "script.md"
        if not script.exists():
            warnings.append(f"{name}: videos/{qid}/script.md does not exist yet")
            continue
        chapters = script_chapters(script.read_text(encoding="utf-8"))
        if chapters != parts:
            problems.append(f"{name}: videos/{qid}/script.md has {chapters} '## Chapter' headings, the page has {parts} part{'s' * (parts > 1)}")
    for script in sorted((root / "videos").glob("*/script.md")):
        name = script.relative_to(root).as_posix()
        for n, line in captions(script.read_text(encoding="utf-8")):
            problems += [f"{name}:{n}: {p}: {line[:50]!r}" for p in caption_problems(line)]
    return problems, warnings


def main(argv: list[str]) -> int:
    problems, warnings = check()
    for w in warnings:
        print(f"warn {w}")
    for p in problems:
        print(p)
    pages = sum(1 for p in QUESTIONS.glob("*/0*.md") if "video" in split_front_matter(p.read_text(encoding="utf-8"))[0])
    scripts = len(list(VIDEOS.glob("*/script.md")))
    print(f"{pages} pages with a video, {scripts} scripts, {len(problems)} problems"
          + (f", {len(warnings)} warnings" if warnings else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
