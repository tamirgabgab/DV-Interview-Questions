"""Render a question's tutorial video: the chapters, chained, with captions and chapters.

    python videos/render.py 0002            # 720p30 (1280x720), the version to upload
    python videos/render.py 0002 --draft    # 480p15, a quick look
    python videos/render.py 0002 --captions-only   # only out/captions.en.vtt, no render
    python videos/render.py 0002 --music-only      # only the music: out/music.wav and music.mp3

Run it with the Python that has Manim (requirements-video.txt). The Hebrew labels are drawn
first by videos/lib/he_label.py with a Python that has Playwright (`--label-python`, or
DVQ_LABEL_PYTHON; default `python3`).

Steps:

1. Read `videos/<id>/scene.py`'s `SCENES` (the scene classes in video order, each with its
   chapter title) and `script.md`'s captions, and check the scene's literal captions.
2. Capture the page's boxes that scene.py's `BOXES` names (lib/box_shots.py, on the site
   built into videos/.cache/site, rebuilt when docs/ or hooks/ is newer), then list the
   Hebrew labels with a Manim dry run, and draw the ones not cached yet
   (videos/.cache/labels) in one browser session.
3. Render every scene with Manim (media under videos/<id>/out/media).
4. Chain the scene files with ffmpeg's concat demuxer; streams with the same parameters are
   copied with no re-encode.
5. Shift each scene's recorded captions by its offset (the real duration of the scene files
   before it) and write captions.vtt and chapters.txt (lib/captions.py), and
   captions.en.vtt: the same cues with the English of `videos/<id>/captions.en.md`.
6. Generate the music (lib/music.py, seeded by the question's id or scene.py's
   MUSIC_SEED) for the video's exact length and write it beside the video, as
   out/music.wav and out/music.mp3. The video stays silent: the owner edits the two
   together in an editor (2026-10-31). `--mux-music` puts the music into video.mp4 instead
   (the video stream copied, the music as AAC at 160 kbps).
7. Fail on a caption shorter than 1.5 s or longer than 7 s, a caption that breaks the RTL or
   colon rules, a beat with no still frame at its end, captions that differ from
   script.md, or a translation file that misses a caption or has an entry for one that no
   longer exists (checked in step 1 too, before the long render). A video with no
   captions.en.md yet gets a warning and no English track.

`--release` also copies the finished files into `videos/<id>/release/`, the folder kept in
the repository and linked from the README (the owner downloads them there and uploads them
to YouTube; 2026-10-31): `<id>.mp4` (silent), `<id>-music.mp3` (the music alone; no
video with the music in it, the owner puts the two together in an editor), `<id>.he.vtt`, `<id>.en.vtt`, `<id>-chapters.txt` and `info.json` (the
length, the chapters and the `video_parts`, which tools/catalog.py reads for the README).
Only a 720p render with no problem makes a release.

Output: videos/<id>/out/video.mp4 (silent), music.wav, music.mp3, captions.vtt,
captions.en.vtt, chapters.txt; with --preview also preview.mp4, the captions burned in and
the same soundtrack as video.mp4, for review in a plain player. `--no-music` makes no
music at all.

`--music-only` renders no scene: it regenerates out/music.wav and music.mp3 for the length
of the existing out/video.mp4, leaving the video silent (or, with `--mux-music`, remuxing the
music into video.mp4 and preview.mp4, their video streams copied).

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
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VIDEOS = Path(__file__).resolve().parent
sys.path.insert(0, str(VIDEOS / "lib"))

import captions as caps  # noqa: E402

MUSIC_BITRATE = "160k"

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


def video_seconds(path: Path) -> float:
    """The length of a file's video stream (the soundtrack, once muxed, does not count)."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=duration", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def mux_music(movie: Path, wav: Path) -> None:
    """Replace `movie`'s soundtrack with `wav`: the video stream copied, the music as AAC."""
    tmp = movie.with_suffix(".tmp.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(movie), "-i", str(wav),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", MUSIC_BITRATE, "-ar", "48000",
                    "-movflags", "+faststart", str(tmp)], check=True)
    os.replace(tmp, movie)


def strip_audio(movie: Path) -> None:
    """Drop any soundtrack from `movie`, the video stream copied."""
    tmp = movie.with_suffix(".tmp.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(movie), "-map", "0:v:0",
                    "-c:v", "copy", "-an", "-movflags", "+faststart", str(tmp)], check=True)
    os.replace(tmp, movie)


def add_music(out: Path, seed: int, movies: list[Path], mux: bool = False) -> None:
    """Generate out/music.wav and out/music.mp3 for the length of out/video.mp4. With
    `mux`, put the music into `movies`; without, leave them silent (any old soundtrack is
    dropped), the music a file of its own beside them."""
    import music  # numpy, only needed here

    seconds = video_seconds(out / "video.mp4")
    wav = out / "music.wav"
    info = music.make(seed, seconds, wav)
    print(f"music: {info['piece']}")
    print(f"music: {info['seconds']:.2f} s, {info['lufs']:.1f} LUFS, true peak "
          f"{info['true_peak']:.1f} dBTP, largest step {info['max_step_over_rms']:.2f} x RMS, "
          f"{info['spikes']} click(s)")
    mp3 = out / "music.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-c:a", "libmp3lame",
                    "-b:a", "192k", str(mp3)], check=True)
    print(f"music: {wav.relative_to(VIDEOS.parent)} and {mp3.name}")
    for movie in movies:
        if mux:
            mux_music(movie, wav)
            print(f"music: muxed into {movie.relative_to(VIDEOS.parent)}")
        else:
            strip_audio(movie)


def music_only(folder: Path, seed: int, mux: bool = False) -> int:
    out = folder / "out"
    video = out / "video.mp4"
    if not video.exists():
        print(f"{video.relative_to(VIDEOS.parent)} does not exist: render the video first",
              file=sys.stderr)
        return 1
    add_music(out, seed, [m for m in (video, out / "preview.mp4") if m.exists()], mux)
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
    ap.add_argument("--music-only", action="store_true",
                    help="render no scene: regenerate out/music.wav and music.mp3 for the "
                         "existing out/video.mp4 (with --mux-music, remux it in)")
    ap.add_argument("--no-music", action="store_true", help="make no music at all")
    ap.add_argument("--mux-music", action="store_true",
                    help="put the music into video.mp4 instead of a file beside it")
    ap.add_argument("--release", action="store_true",
                    help="copy the finished files into videos/<id>/release/ (720p, no problem)")
    args = ap.parse_args()

    qid = f"{int(args.qid):04d}"
    folder = VIDEOS / qid
    if args.captions_only:
        return captions_only(folder)
    scene_py = folder / "scene.py"
    out = folder / "out"
    lits = module_literals(scene_py)
    seed = int(lits.get("MUSIC_SEED", int(qid)))   # scene.py may pick another piece
    if args.music_only:
        return music_only(folder, seed, args.mux_music)
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

    # the math is set by LaTeX (dvq.TX): say what to install rather than fail mid-render
    if re.search(r"\bTX\(|\$[^\"']+\$", scene_py.read_text(encoding="utf-8")):
        sys.path.insert(0, str(VIDEOS / "lib"))
        from dvq import LATEX_PACKAGES, latex_missing
        if latex_missing():
            print(f"LaTeX is missing ({', '.join(latex_missing())}): apt-get install -y "
                  f"--no-install-recommends {LATEX_PACKAGES}", file=sys.stderr)
            return 1

    flag, qdir = QUALITY[args.draft]
    media = out / "media"
    parts_dir = out / "parts"
    names = [s[0] for s in scenes]
    manim = [sys.executable, "-m", "manim", "render", flag, "--media_dir", str(media),
             "--progress_bar", "none", "-v", "WARNING", str(scene_py), *names]
    env = dict(os.environ, DVQ_LABEL_PYTHON=args.label_python)

    # 2. the page's boxes, then the Hebrew labels: a dry run lists them, he_label.py draws
    #    the missing ones
    if "\nBOXES" in scene_py.read_text(encoding="utf-8") and "BOXES" not in lits:
        print("scene.py's BOXES must be a literal (no names in it)", file=sys.stderr)
        return 1
    if lits.get("BOXES"):
        capture_boxes(qid, lits["BOXES"], args.label_python)
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
    if not args.no_music:
        add_music(out, seed, [video], args.mux_music)
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
        if args.release:
            print("no release: fix the problems first", file=sys.stderr)
        return 1
    if args.release:
        if args.draft or args.no_music:
            print("no release from a draft or without music", file=sys.stderr)
            return 1
        release(folder, qid, total, chapters, starts)
    return 0


def release(folder: Path, qid: str, seconds: float, chapters: str, parts: list[int]) -> None:
    """videos/<id>/release/: the files the owner downloads from the README."""
    out, rel = folder / "out", folder / "release"
    rel.mkdir(exist_ok=True)
    shutil.copyfile(out / "video.mp4", rel / f"{qid}.mp4")
    shutil.copyfile(out / "music.mp3", rel / f"{qid}-music.mp3")
    shutil.copyfile(out / "captions.vtt", rel / f"{qid}.he.vtt")
    if (out / "captions.en.vtt").exists():
        shutil.copyfile(out / "captions.en.vtt", rel / f"{qid}.en.vtt")
    (rel / f"{qid}-chapters.txt").write_text(chapters, encoding="utf-8")
    info = {"id": qid, "seconds": round(seconds, 2), "video_parts": parts,
            "chapters": [line.split(" ", 1) for line in chapters.strip().splitlines()],
            "files": sorted(p.name for p in rel.iterdir() if p.name != "info.json")}
    (rel / "info.json").write_text(json.dumps(info, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8")
    size = sum((rel / f).stat().st_size for f in info["files"]) / 1e6
    print(f"release: {rel.relative_to(VIDEOS.parent)} ({len(info['files'])} files, {size:.1f} MB)")


SITE = VIDEOS / ".cache" / "site"


def newest(*folders: Path) -> float:
    return max(p.stat().st_mtime for f in folders for p in f.rglob("*") if p.is_file())


def capture_boxes(qid: str, boxes: dict, python: str) -> None:
    """The pictures of the page's boxes (lib/box_shots.py) on the built site: built into
    videos/.cache/site when it is missing or older than docs/ and hooks/."""
    root = VIDEOS.parent
    stamp = SITE / ".built"
    if not stamp.exists() or stamp.stat().st_mtime < newest(root / "docs", root / "hooks"):
        print("+ mkdocs build (for the boxes)")
        subprocess.run([python, "-m", "mkdocs", "build", "-q", "-d", str(SITE)], check=True,
                       cwd=root, env=dict(os.environ, DVQ_SOCIAL_CARDS="false"))
        stamp.touch()
    sys.path.insert(0, str(root / "tools"))
    from check_phone import local_cdn_routes   # the CDN scripts from .cache/cdn

    routes = [a for spec in local_cdn_routes() for a in ("--route", spec)]
    with tempfile.TemporaryDirectory() as tmp:
        spec = Path(tmp) / "boxes.json"
        spec.write_text(json.dumps(boxes, ensure_ascii=False), encoding="utf-8")
        subprocess.run([python, str(VIDEOS / "lib" / "box_shots.py"), qid, "--spec", str(spec),
                        "--site", str(SITE), *routes], check=True)


PREVIEW_STYLE = ("FontName=Rubik,FontSize=20,Encoding=-1,PrimaryColour=&H00FFFFFF,"
                 "BackColour=&H99000000,BorderStyle=4,Outline=0,Shadow=0,MarginV=16")


def burn_preview(out: Path) -> None:
    """out/preview.mp4: the video with its captions burned in by libass, for watching in a
    plain player. Encoding=-1 makes libass pick the base direction from the text (right to
    left here); the default left-to-right base puts a caption's colon and full stop at the
    wrong end. Rubik comes from he_label.py's font cache (videos/.cache/fonts). The
    soundtrack of video.mp4, the music, is copied as it is."""
    fonts = VIDEOS / ".cache" / "fonts"
    vf = (f"subtitles={out / 'captions.vtt'}:fontsdir={fonts}:force_style='{PREVIEW_STYLE}'")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out / "video.mp4"), "-vf", vf,
                    "-c:v", "libx264", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart",
                    str(out / "preview.mp4")], check=True)
    print(f"preview: {out / 'preview.mp4'}")


if __name__ == "__main__":
    sys.exit(main())
