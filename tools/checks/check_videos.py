#!/usr/bin/env python3
"""Check the tutorial videos' fields on the question pages (notes/VIDEOS.md).

    python tools/checks/check_videos.py          # every question page

Needs no video and no network. The videos are on YouTube; a page links its video with two
front matter fields, checked here for every page that has a ``video:`` field:

- the id has the YouTube form (11 characters of ``A-Z a-z 0-9 _ -``, quoted when YAML
  would read it as a number or a boolean);
- ``video_parts`` is optional: without it the page gets one link to the video; with it, it
  has one start time (whole seconds) per part (``### סעיף ...``), rising from 0, and each
  part's solution gets a link to its chapter.

The same checks run in tools/checks/lint_pages.py and in the build hook, which import
``video_problems`` from here. Exit status 1 on a problem.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
QUESTIONS = ROOT / "docs" / "questions"

VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
PART_HEADING = re.compile(r"^### סעיף\s+([א-ת])")
FENCE = re.compile(r"^\s*(```|~~~)")


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
        return out                                      # one link to the whole video
    if not isinstance(times, list) or not all(isinstance(t, int) and not isinstance(t, bool) for t in times):
        return out + [f"'video_parts' must be a list of whole seconds, e.g. [0, 95, 210]: {times!r}"]
    if len(times) != parts:
        out.append(f"'video_parts' has {len(times)} times but the page has {parts} part{'s' * (parts > 1)}")
    if times and times[0] != 0:
        out.append(f"'video_parts' must start at 0: {times!r}")
    if any(b <= a for a, b in zip(times, times[1:])):
        out.append(f"'video_parts' must rise: {times!r}")
    return out


def check(root: Path = ROOT) -> list[str]:
    """The problems of every question page with a video under root."""
    problems: list[str] = []
    for page in sorted((root / "docs" / "questions").glob("*/0*.md")):
        meta, body = split_front_matter(page.read_text(encoding="utf-8"))
        problems += [f"{page.relative_to(root).as_posix()}: {p}" for p in video_problems(meta, body)]
    return problems


def main(argv: list[str]) -> int:
    problems = check()
    for p in problems:
        print(p)
    pages = sum(1 for p in QUESTIONS.glob("*/0*.md") if "video" in split_front_matter(p.read_text(encoding="utf-8"))[0])
    print(f"{pages} pages with a video, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
