"""Render a question's tutorial video: the chapters, chained, with captions and chapters.

    python videos/render.py 0002            # 720p30 (1280x720), the version to upload
    python videos/render.py 0002 --draft    # 480p15, a quick look
    python videos/render.py 0002 --captions-only   # only out/captions.en.vtt, no render

Run it with the Python that has Manim (requirements-video.txt). The Hebrew labels are drawn
first by videos/lib/he_label.py with a Python that has Playwright (`--label-python`, or
DVQ_LABEL_PYTHON; default `python3`).

Steps:

1. Read `videos/<id>/scene.py`'s `SCENES` (the scene classes in video order, each with its
   chapter title) and `script.md`'s captions, and check the scene's literal captions.
2. List the Hebrew labels with a Manim dry run, and draw the ones not cached yet
   (videos/.cache/labels) in one browser session.
3. Render every scene with Manim (media under videos/<id>/out/media).
4. Chain the scene files with ffmpeg's concat demuxer; streams with the same parameters are
   copied with no re-encode.
5. Shift each scene's recorded captions by its offset (the real duration of the scene files
   before it) and write captions.vtt and chapters.txt (lib/captions.py), and
   captions.en.vtt: the same cues with the English of `videos/<id>/captions.en.md`.
6. Fail on a caption shorter than 1.5 s or longer than 7 s, a caption that breaks the RTL or
   colon rules, a beat with no still frame at its end, captions that differ from
   script.md, or a translation file that misses a caption or has an entry for one that no
   longer exists (checked in step 1 too, before the long render). A video with no
   captions.en.md yet gets a warning and no English track.

Output: videos/<id>/out/video.mp4, captions.vtt, captions.en.vtt, chapters.txt; with
--preview also preview.mp4, the captions burned in, for review in a plain player.

`--captions-only` renders nothing: it writes out/captions.en.vtt from the existing
out/captions.vtt (its cues and times) and captions.en.md, so a wording fix of the English
needs no render. It fails when captions.vtt no longer matches script.md (render again) or
when the translation file does not match the captions.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VIDEOS = Path(__file__).resolve().parent
sys.path.insert(0, str(VIDEOS / "lib"))

import captions as caps  # noqa: E402

QUALITY = {False: ("-qm", "720p30"), True: ("-ql", "480p15")}


def module_literals(path: Path) -> dict:
    """The literal module-level assignments of scene.py (SCENES, ...)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
    return out


def literal_says(path: Path) -> list[str]:
    """The literal captions of the scene's say()/beat() calls, in source order."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in ("say", "beat") and node.args \
                and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            found.append(node.args[0].value)
    return found


def script_captions(path: Path) -> list[str]:
    """The captions of script.md: a run of lines that start with "> " is one caption, a
    line each (the caption's lines in the video)."""
    out, cur = [], []
    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        if line.startswith("> "):
            cur.append(line[2:])
        elif cur:
            out.append("\n".join(cur))
            cur = []
    return out


def norm(s: str) -> str:
    """A caption as its lines in the video, for comparing scene.py with script.md."""
    return "\n".join(caps.wrap(s))


def read_english(folder: Path, captions: list[str], required: bool) -> tuple[list[str] | None, list[str]]:
    """The English of the Hebrew captions from videos/<id>/captions.en.md, in order, and the
    problems. With no translation file: (None, []) and a warning, or a problem if required."""
    path = folder / caps.TRANSLATIONS
    rel = path.relative_to(VIDEOS.parent).as_posix()
    if not path.exists():
        msg = f"{rel} does not exist, so there is no English track (see VIDEOS.md)"
        if required:
            return None, [msg]
        print(f"warn {msg}", file=sys.stderr)
        return None, []
    entries, problems = caps.read_translations(path.read_text(encoding="utf-8"))
    english, more = caps.translate(captions, entries)
    problems = [f"{rel}: {p}" for p in problems + more]
    return (None if problems else english), problems


def captions_only(folder: Path) -> int:
    """Write out/captions.en.vtt from out/captions.vtt and captions.en.md, rendering nothing."""
    out = folder / "out"
    src = out / "captions.vtt"
    if not src.exists():
        print(f"{src.relative_to(VIDEOS.parent)} does not exist: render the video first", file=sys.stderr)
        return 1
    cues = caps.parse_vtt(src.read_text(encoding="utf-8"))
    texts = ["\n".join(caps.strip_isolates(line) for line in c["lines"]) for c in cues]
    problems = []
    if [caps.key(t) for t in texts] != [norm(c) for c in script_captions(folder / "script.md")]:
        problems.append("out/captions.vtt differs from script.md: render the video again "
                        "(the English track copies the cues of captions.vtt)")
    english, more = read_english(folder, texts, required=True)
    problems += more
    if problems:
        print("\n".join(f"  - {p}" for p in problems), file=sys.stderr)
        return 1
    dst = out / "captions.en.vtt"
    dst.write_text(caps.english_vtt(cues, english), encoding="utf-8")
    print(f"{dst.relative_to(VIDEOS.parent)}: {len(cues)} cues, the times of captions.vtt")
    return 0


def ffprobe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=codec_name,width,height,pix_fmt,r_frame_rate,time_base,profile:format=duration",
         "-of", "json", str(path)], check=True, capture_output=True, text=True).stdout
    data = json.loads(out)
    s = data["streams"][0]
    return {"params": (s["codec_name"], s["width"], s["height"], s["pix_fmt"], s["r_frame_rate"],
                       s["time_base"], s.get("profile")),
            "duration": float(data["format"]["duration"])}


def main() -> int:
    ap = argparse.ArgumentParser(description="Render a question's tutorial video.")
    ap.add_argument("qid", help="the question id, e.g. 0002")
    ap.add_argument("--draft", action="store_true", help="480p15 instead of 720p30")
    ap.add_argument("--label-python", default=os.environ.get("DVQ_LABEL_PYTHON", "python3"),
                    help="a Python with Playwright, for the Hebrew labels")
    ap.add_argument("--preview", action="store_true",
                    help="also write out/preview.mp4 with the captions burned in (for review)")
    ap.add_argument("--keep-going", action="store_true",
                    help="write the outputs even when a caption check fails (exit 1 still)")
    ap.add_argument("--captions-only", action="store_true",
                    help="render nothing: write out/captions.en.vtt from out/captions.vtt "
                         "and captions.en.md")
    args = ap.parse_args()

    qid = f"{int(args.qid):04d}"
    folder = VIDEOS / qid
    if args.captions_only:
        return captions_only(folder)
    scene_py = folder / "scene.py"
    out = folder / "out"
    lits = module_literals(scene_py)
    scenes = lits["SCENES"]                     # [(class, chapter title), ...]
    problems: list[str] = []

    # 1. the captions in scene.py against script.md (before the long render)
    script_raw = script_captions(folder / "script.md")
    script = [norm(c) for c in script_raw]
    english, problems = read_english(folder, script_raw, required=False)
    for text in literal_says(scene_py):
        if norm(text) not in script:
            problems.append(f"scene.py caption not in script.md: {text!r}")
        for p in caps.check_text(text):
            problems.append(f"scene.py caption {text[:40]!r}…: {p}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1

    flag, qdir = QUALITY[args.draft]
    media = out / "media"
    parts_dir = out / "parts"
    names = [s[0] for s in scenes]
    manim = [sys.executable, "-m", "manim", "render", flag, "--media_dir", str(media),
             "--progress_bar", "none", "-v", "WARNING", str(scene_py), *names]
    env = dict(os.environ, DVQ_LABEL_PYTHON=args.label_python)

    # 2. the Hebrew labels: a dry run lists them, he_label.py draws the missing ones
    with tempfile.TemporaryDirectory() as tmp:
        listed = Path(tmp) / "labels.jsonl"
        dry = subprocess.run([*manim, "--dry_run"], cwd=folder, capture_output=True, text=True,
                             env=dict(env, DVQ_COLLECT_LABELS=str(listed)))
        if dry.returncode:
            print(dry.stdout[-6000:], dry.stderr[-6000:], file=sys.stderr)
            return 1
        specs = {}
        if listed.exists():
            for line in listed.read_text(encoding="utf-8").splitlines():
                spec = json.loads(line)
                specs[json.dumps(spec, sort_keys=True, ensure_ascii=False)] = spec
        if specs:
            spec_file = Path(tmp) / "labels.json"
            spec_file.write_text(json.dumps(list(specs.values()), ensure_ascii=False), encoding="utf-8")
            subprocess.run([args.label_python, str(VIDEOS / "lib" / "he_label.py"), "--json",
                            str(spec_file)], check=True)

    # 3. the scenes
    if parts_dir.exists():
        shutil.rmtree(parts_dir)
    print("+", " ".join(manim))
    subprocess.run(manim, check=True, cwd=folder, env=env)
    files = [media / "videos" / "scene" / qdir / f"{n}.mp4" for n in names]

    # 4. chain them
    probes = [ffprobe(f) for f in files]
    same = len({p["params"] for p in probes}) == 1
    listing = out / "concat.txt"
    listing.write_text("".join(f"file '{f.resolve()}'\n" for f in files), encoding="utf-8")
    video = out / "video.mp4"
    codec = ["-c", "copy"] if same else ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18"]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
                    *codec, "-movflags", "+faststart", str(video)], check=True)
    print(f"concat: {'stream copy' if same else 're-encoded (scene parameters differ)'}")

    # 5. captions and chapters
    parts, offset = [], 0.0
    for (name, title), probe in zip(scenes, probes):
        rec = json.loads((parts_dir / f"{name}.json").read_text(encoding="utf-8"))
        if abs(rec["duration"] - probe["duration"]) > 1.5 / rec["fps"]:
            problems.append(f"{name}: recorded {rec['duration']:.3f} s, file {probe['duration']:.3f} s")
        parts.append({"scene": name, "title": title, "offset": offset,
                      "duration": probe["duration"], "captions": rec["captions"],
                      "problems": rec["problems"]})
        offset += probe["duration"]
    vtt, chapters, cues, more = caps.build(parts)
    problems += more
    total = ffprobe(video)["duration"]
    if cues and cues[-1]["end"] > total + 1e-3:
        problems.append(f"last caption ends at {cues[-1]['end']:.2f} s, after the video ({total:.2f} s)")

    # 6. the captions as played against script.md
    played = [norm(c["text"]) for c in cues]
    if played != script:
        missing = [c for c in script if c not in played]
        extra = [c for c in played if c not in script]
        problems.append(f"captions differ from script.md: {len(missing)} only in the script, "
                        f"{len(extra)} only in the video"
                        + "".join(f"\n    script only: {c}" for c in missing)
                        + "".join(f"\n    video only:  {c}" for c in extra)
                        + ("" if missing or extra else "\n    (same captions, different order)"))

    vtt_en = None
    if english is not None:
        english, more = read_english(folder, [c["text"] for c in cues], required=True)
        problems += more
        vtt_en = english and caps.english_vtt(cues, english)
    if not problems or args.keep_going:
        (out / "captions.vtt").write_text(vtt, encoding="utf-8")
        (out / "chapters.txt").write_text(chapters, encoding="utf-8")
        if vtt_en:
            (out / "captions.en.vtt").write_text(vtt_en, encoding="utf-8")
    if args.preview and (not problems or args.keep_going):
        burn_preview(out)
    size = video.stat().st_size / 1e6
    print(f"\n{video.relative_to(VIDEOS.parent)}: {total:.1f} s "
          f"({int(total // 60)}:{int(total % 60):02d}), {size:.1f} MB, {len(cues)} captions")
    print(chapters, end="")
    starts = [int(p["offset"]) for p in parts if p["scene"].startswith("Chapter")]
    if starts:
        starts[0] = 0          # the link to the first part plays the opening too
    print(f"front matter: video_parts: {starts}")
    if problems:
        print(f"\n{len(problems)} problem(s):", file=sys.stderr)
        print("\n".join(f"  - {p}" for p in problems), file=sys.stderr)
        return 1
    return 0


PREVIEW_STYLE = ("FontName=Rubik,FontSize=20,Encoding=-1,PrimaryColour=&H00FFFFFF,"
                 "BackColour=&H99000000,BorderStyle=4,Outline=0,Shadow=0,MarginV=16")


def burn_preview(out: Path) -> None:
    """out/preview.mp4: the video with its captions burned in by libass, for watching in a
    plain player. Encoding=-1 makes libass pick the base direction from the text (right to
    left here); the default left-to-right base puts a caption's colon and full stop at the
    wrong end. Rubik comes from he_label.py's font cache (videos/.cache/fonts)."""
    fonts = VIDEOS / ".cache" / "fonts"
    vf = (f"subtitles={out / 'captions.vtt'}:fontsdir={fonts}:force_style='{PREVIEW_STYLE}'")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out / "video.mp4"), "-vf", vf,
                    "-c:v", "libx264", "-crf", "21", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    str(out / "preview.mp4")], check=True)
    print(f"preview: {out / 'preview.mp4'}")


if __name__ == "__main__":
    sys.exit(main())
