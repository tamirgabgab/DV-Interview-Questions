#!/usr/bin/env python3
"""Write CATALOG.md: every question's id, its Hebrew title as a link to its page on the
live site, and its level, read from the pages' front matter. Also write the README's table
of tutorial videos (between `<!-- videos -->` and `<!-- /videos -->`): one row per
`videos/<id>/script.md`, with the page, the number of chapters, the length and download
links to the files of `videos/<id>/release/` (render.py --release writes them and their
info.json), and the YouTube link once the page has a `video:` id.

    python tools/catalog.py           # rewrite CATALOG.md and the README's video table
    python tools/catalog.py --check   # exit 1 when either is out of date

tools/new_question.py rewrites it when it adds a page; a test checks it is up to date.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://tamirgabgab.github.io/DV-Interview-Questions/"
RAW = "https://github.com/tamirgabgab/DV-Interview-Questions/raw/main/"
RELEASE = [("{id}.mp4", "video"), ("{id}-music.mp3", "music"),
           ("{id}.he.vtt", "Hebrew captions"), ("{id}.en.vtt", "English captions"),
           ("{id}-chapters.txt", "chapters")]
LEVELS = {"student": "student (סטודנט)", "junior": "junior (ג'וניור)", "senior": "senior (סניור)"}
FIELD = re.compile(r"^(id|title|level|video):\s*(.+?)\s*$", re.M)
VIDEOS = re.compile(r"(<!-- videos -->\n).*?(<!-- /videos -->)", re.S)


def fronts(root: Path) -> list[tuple[dict, str]]:
    """The front matter fields and the path on the site of every question page."""
    out = []
    for p in sorted((root / "docs" / "questions").glob("*/[0-9][0-9][0-9][0-9]-*.md")):
        text = p.read_text(encoding="utf-8")
        out.append((dict(FIELD.findall(text[:text.index("\n---", 3)])),
                    p.relative_to(root / "docs").with_suffix("").as_posix() + "/"))
    return out


def pages(root: Path) -> list[tuple[int, str, str, str]]:
    """(id, title, level, path on the site) of every question page, by id."""
    return sorted((int(f["id"]), f["title"], f["level"], path) for f, path in fronts(root))


def render(root: Path) -> str:
    rows = [f"| {qid:04d} | [{title}]({SITE}{path}) | {LEVELS.get(level, level)} |"
            for qid, title, level, path in pages(root)]
    return ("# Catalog\n\n"
            f"All {len(rows)} questions, with links to their pages on the [live site]({SITE}). Written by\n"
            "`python tools/catalog.py` from the pages' front matter; do not edit by hand.\n\n"
            "| Id | Question | Level |\n|----|----------|-------|\n" + "\n".join(rows) + "\n")


def video_rows(root: Path) -> str:
    """The README's video table: a row per question with a video script, its files to
    download from videos/<id>/release/ (render.py --release) and its YouTube link."""
    import json

    by_id = {int(f["id"]): (f, path) for f, path in fronts(root)}
    rows = []
    for script in sorted((root / "videos").glob("[0-9][0-9][0-9][0-9]/script.md")):
        qid = int(script.parent.name)
        front, path = by_id[qid]
        chapters = len(re.findall(r"^## Chapter", script.read_text(encoding="utf-8"), re.M))
        info_path = script.parent / "release" / "info.json"
        if info_path.exists():
            info = json.loads(info_path.read_text(encoding="utf-8"))
            length = f"{int(info['seconds'] // 60)}:{int(info['seconds'] % 60):02d}"
            base = f"{RAW}videos/{qid:04d}/release/"
            links = [f"[{label}]({base}{name.format(id=f'{qid:04d}')})" for name, label in RELEASE
                     if name.format(id=f"{qid:04d}") in info["files"]]
            files = " · ".join(links)
        else:
            length, files = "–", "not rendered yet"
        vid = front.get("video", "").strip("'\"")
        if vid:
            files += f" · [YouTube](https://youtu.be/{vid})"
        rows.append(f"| {qid:04d} | [{front['title']}]({SITE}{path}) | {chapters} | {length} | {files} |")
    if not rows:
        return "No videos yet.\n"
    return ("| Id | Question | Chapters | Length | Download |\n|----|----------|----------|--------|----------|\n"
            + "\n".join(rows) + "\n")


def render_readme(root: Path) -> str:
    text = (root / "README.md").read_text(encoding="utf-8")
    return VIDEOS.sub(lambda m: m.group(1) + video_rows(root) + m.group(2), text, count=1)


def write(root: Path = ROOT) -> Path:
    path = root / "CATALOG.md"
    path.write_text(render(root), encoding="utf-8")
    if (root / "README.md").exists():   # a scratch tree in the tests has none
        (root / "README.md").write_text(render_readme(root), encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="only check that CATALOG.md is up to date")
    if ap.parse_args(argv).check:
        path = ROOT / "CATALOG.md"
        if not path.exists() or path.read_text(encoding="utf-8") != render(ROOT):
            print("CATALOG.md is out of date: run python tools/catalog.py")
            return 1
        if (ROOT / "README.md").read_text(encoding="utf-8") != render_readme(ROOT):
            print("the README's video table is out of date: run python tools/catalog.py")
            return 1
        print("CATALOG.md and the README's video table are up to date")
        return 0
    print(f"wrote {write().relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
