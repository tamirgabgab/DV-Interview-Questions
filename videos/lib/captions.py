"""Captions and chapters of a video, from the captions its scenes recorded.

Each scene (dvq.DVQScene) writes `out/parts/<Scene>.json`: its captions with the start and
end it really played at, in the scene's own clock. `build()` shifts them by the scene's
offset in the chained video and writes

- `captions.vtt`: WebVTT, a cue per caption, wrapped to at most two lines, every code or
  math expression wrapped in Unicode isolates (`isolate()`);
- `chapters.txt`: YouTube's chapter list for the description ("0:00 פתיחה", one line per
  scene, the first at 0:00);
- `captions.en.vtt`: the English track, the same cues and times with the English text of
  `videos/<id>/captions.en.md` (`read_translations()`, `translate()`, `english_vtt()`).

`check_caption()` holds the rules of CLAUDE.md and VIDEOS.md for a caption: every line
starts with a Hebrew letter or an RLM, a colon has a no-break space before it, at most 12
words a line and 2 lines, and 1.5–7 s on screen.
"""

from __future__ import annotations

import re
from collections import Counter

RLM = "‏"
NBSP = " "
HEBREW = re.compile("[֐-׿]")
MAX_WORDS = 12
MAX_LINES = 2
MAX_CHARS = 44          # a line of a caption, so it fits a phone's player at a readable size
MIN_SECONDS = 1.5
MAX_SECONDS = 7.0
MIN_CHAPTER = 10.0      # YouTube ignores chapters shorter than 10 s


def words(line: str) -> list[str]:
    # split on ordinary spaces only: a no-break space keeps "שלב 1 :" in one piece
    return [w for w in line.split(" ") if w]


def count_words(line: str) -> int:
    """Words as tools/check_videos.py counts them: tokens with a letter or a digit."""
    return sum(1 for w in line.replace(NBSP, " ").split() if re.search(r"\w", w))


def wrap(text: str) -> list[str]:
    """The caption's lines: its own line breaks ("\\n", as script.md writes them), or else
    a balanced split into at most two lines, the second one starting right-to-left."""
    if "\n" in text:
        return [" ".join(words(line)) for line in text.split("\n")]
    text = " ".join(words(text))
    ws = words(text)
    if count_words(text) <= MAX_WORDS and len(text) <= MAX_CHARS:
        return [text]
    best = None
    for i in range(1, len(ws)):
        a, b = " ".join(ws[:i]), " ".join(ws[i:])
        if count_words(a) > MAX_WORDS or count_words(b) > MAX_WORDS:
            continue
        score = max(len(a), len(b)) + (0 if HEBREW.match(b) else 6)
        if best is None or score < best[0]:
            best = (score, a, b)
    if best is None:
        return [text]          # too long: check_caption reports it
    a, b = best[1], best[2]
    if not HEBREW.match(b) and not b.startswith(RLM):
        b = RLM + b
    return [a, b]


def check_text(text: str) -> list[str]:
    """The RTL and colon rules for one caption's text (any duration)."""
    problems = []
    lines = wrap(text)
    if len(lines) > MAX_LINES:
        problems.append(f"more than {MAX_LINES} lines")
    for line in lines:
        if not (HEBREW.match(line) or line.startswith(RLM)):
            problems.append(f"line does not start with a Hebrew word or an RLM: {line!r}")
        n = count_words(line)
        if n > MAX_WORDS:
            problems.append(f"{n} words in a line (at most {MAX_WORDS}): {line!r}")
        if len(line) > MAX_CHARS + 8:
            problems.append(f"line of {len(line)} characters: {line!r}")
    for m in re.finditer(":", text):
        i = m.start()
        before, after = text[i - 1:i], text[i + 1:i + 2]
        if before.isdigit() and after.isdigit():
            continue              # a time or a ratio (12:00)
        if before != NBSP:
            problems.append(f"colon without a no-break space before it at {text[max(0, i - 12):i + 2]!r}")
        if after not in ("", " ", "\n"):
            problems.append(f"colon not followed by a space at {text[max(0, i - 12):i + 2]!r}")
    return problems


def check_caption(cap: dict) -> list[str]:
    problems = check_text(cap["text"])
    dur = cap["end"] - cap["start"]
    if dur < MIN_SECONDS - 1e-6:
        problems.append(f"on screen {dur:.2f} s (at least {MIN_SECONDS} s)")
    if dur > MAX_SECONDS + 1e-6:
        problems.append(f"on screen {dur:.2f} s (at most {MAX_SECONDS} s)")
    return problems


LRI, PDI = "\u2066", "\u2069"
LTR_RUN = re.compile(r"[A-Za-z0-9(\[−][A-Za-z0-9_()\[\]{}%^&|=+\-−*/<>≡'²³¹⁰₀ ,.]*")


def _pieces(run: str):
    """Split a left-to-right run at ", " and ". " outside brackets (a list, a sentence)."""
    depth, start = 0, 0
    for i, ch in enumerate(run):
        depth += ch in "([" and 1 or 0
        depth -= ch in ")]" and 1 or 0
        if depth == 0 and ch in ",." and run[i + 1:i + 2] == " ":
            yield run[start:i]
            yield run[i:i + 2]
            start = i + 2
    yield run[start:]


def isolate(line: str) -> str:
    """Wrap every code or math expression of a caption line in Unicode isolates (LRI ...
    PDI), so the player lays it out left to right as one unit inside the right-to-left
    line. Without them "(k + 1) % 3" or "8 − 3 = 5" can come out reordered around their
    parentheses, operators and numbers. Plain words (RED, temp) are left alone."""
    def wrap(m):
        run = m.group(0)
        tail = len(run) - len(run.rstrip(" ,.?"))
        core, rest = run[:len(run) - tail], run[len(run) - tail:]
        out = []
        for piece in _pieces(core):
            if piece in (", ", ". ") or not piece or re.fullmatch(r"[A-Za-z_]+", piece):
                out.append(piece)
            else:
                out.append(LRI + piece + PDI)
        return "".join(out) + rest
    return LTR_RUN.sub(wrap, line)


def vtt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def chapter_time(t: float) -> str:
    s = int(t)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def build(parts: list[dict]) -> tuple[str, str, list[dict], list[str]]:
    """`parts`: [{scene, title, offset, duration, captions: [{text, start, end}]}] in video
    order. Returns (vtt, chapters, captions on the video's clock, problems)."""
    problems = []
    cues = []
    for part in parts:
        for cap in part["captions"]:
            c = {"text": cap["text"], "start": part["offset"] + cap["start"],
                 "end": part["offset"] + cap["end"], "scene": part["scene"]}
            for p in check_caption(c):
                problems.append(f"{part['scene']} @ {chapter_time(c['start'])}: {p}  [{cap['text']}]")
            cues.append(c)
        problems += [f"{part['scene']}: {p}" for p in part.get("problems", [])]
    for a, b in zip(cues, cues[1:]):
        if b["start"] < a["end"] - 1e-3:
            problems.append(f"captions overlap at {vtt_time(b['start'])}")
    out = ["WEBVTT", ""]
    for i, c in enumerate(cues, start=1):
        out += [str(i), f"{vtt_time(c['start'])} --> {vtt_time(c['end'])}",
                *[isolate(line) for line in wrap(c["text"])], ""]
    vtt = "\n".join(out)

    chapters = []
    for k, part in enumerate(parts):
        start = 0.0 if k == 0 else part["offset"]
        chapters.append(f"{chapter_time(start)} {part['title']}")
        if part["duration"] < MIN_CHAPTER:
            problems.append(f"chapter {part['title']!r} lasts {part['duration']:.1f} s "
                            f"(YouTube needs {MIN_CHAPTER:.0f} s)")
    if len(parts) < 3:
        problems.append("YouTube needs at least three chapters")
    return vtt, "\n".join(chapters) + "\n", cues, problems


def parse_vtt(text: str) -> list[dict]:
    """A small WebVTT reader for the checks: the cues with their times and lines (and the
    timing line as written, so a second track can copy it exactly)."""
    if not text.startswith("WEBVTT"):
        raise ValueError("no WEBVTT header")
    cues = []
    for block in text.strip().split("\n\n")[1:]:
        lines = block.split("\n")
        if "-->" not in lines[1]:
            raise ValueError(f"bad cue: {block!r}")
        a, b = [x.strip() for x in lines[1].split("-->")]

        def sec(s):
            h, m, rest = s.split(":")
            return int(h) * 3600 + int(m) * 60 + float(rest)
        cues.append({"id": lines[0], "start": sec(a), "end": sec(b), "lines": lines[2:],
                     "timing": lines[1]})
    return cues


# --- The English track ----------------------------------------------------------------------
#
# videos/<id>/captions.en.md pairs every Hebrew caption of script.md, in order, with its
# English translation:
#
#     # comment lines start with "#"
#
#     he: שלב 1 : temp = a. הערך 5 נשמר ב-temp.
#     en: Step 1: temp = a. The value 5 is saved in temp.
#
#     he: שלב 2 : a = b. עכשיו a מחזיק 3,
#     he: וה-5 המקורי עדיין שמור ב-temp.
#     en: Step 2: a = b. Now a holds 3,
#     en: and the original 5 is still saved in temp.
#
# An entry is its "he:" lines (the caption's lines, exactly as script.md has them) and then
# its "en:" lines (the English cue's lines, one or two); a blank line ends it.

TRANSLATIONS = "captions.en.md"
EN_MAX_WORDS = 12
EN_MAX_LINES = 2
EN_MAX_CHARS = 60
BIDI_MARKS = re.compile("[\u200e\u200f\u2066-\u2069\u202a-\u202e]")


def strip_isolates(line: str) -> str:
    """A caption line of captions.vtt without the isolates isolate() added."""
    return line.replace(LRI, "").replace(PDI, "")


def key(text: str) -> str:
    """A caption as its lines in the video, for matching script.md, scene.py, captions.vtt
    and the translation file."""
    return "\n".join(wrap(text))


def read_translations(text: str) -> tuple[list[dict], list[str]]:
    """The entries of a captions.en.md, [{he, en, line}] in file order, and the problems of
    its format ("line N: ...")."""
    entries, problems = [], []
    he, en, start = [], [], 0
    for n, raw in enumerate(text.splitlines() + [""], 1):
        line = raw.rstrip()
        if line.startswith("#"):
            continue
        if not line:
            if he and en:
                entries.append({"he": "\n".join(he), "en": "\n".join(en), "line": start})
            elif he:
                problems.append(f"line {start}: no 'en:' line for the caption {he[0]!r}")
            elif en:
                problems.append(f"line {n - len(en)}: 'en:' lines with no 'he:' line before them")
            he, en = [], []
            continue
        tag, _, rest = line.partition(":")
        rest = rest[1:] if rest.startswith(" ") else rest
        if tag == "he" and not en:
            start = start if he else n
            he.append(rest)
        elif tag == "he":
            problems.append(f"line {n}: a 'he:' line after the 'en:' lines (a blank line ends an entry)")
        elif tag == "en":
            en.append(rest)
        else:
            problems.append(f"line {n}: neither 'he:', 'en:', a '#' comment nor a blank line: {line[:40]!r}")
    return entries, problems


def check_english(en: str) -> list[str]:
    """The rules of an English cue: one or two lines of at most 12 words and 60 characters,
    no Hebrew and no direction marks (a left-to-right track needs none)."""
    problems = []
    lines = en.split("\n")
    if len(lines) > EN_MAX_LINES:
        problems.append(f"{len(lines)} English lines (at most {EN_MAX_LINES})")
    for line in lines:
        if not line.strip():
            problems.append("an empty English line")
            continue
        n = count_words(line)
        if n > EN_MAX_WORDS:
            problems.append(f"{n} words in an English line (at most {EN_MAX_WORDS}): {line!r}")
        if len(line) > EN_MAX_CHARS:
            problems.append(f"English line of {len(line)} characters (at most {EN_MAX_CHARS}): {line!r}")
        if HEBREW.search(line):
            problems.append(f"Hebrew in an English line: {line!r}")
        if BIDI_MARKS.search(line) or NBSP in line:
            problems.append(f"a direction mark or a no-break space in an English line: {line!r}")
    return problems


def translate(captions: list[str], entries: list[dict]) -> tuple[list[str], list[str]]:
    """The English of every Hebrew caption, in order, and the problems: a caption with no
    entry, an entry for a caption that no longer exists, entries out of order, and English
    that breaks check_english(). `captions` are the Hebrew captions in video order."""
    want = [key(c) for c in captions]
    have = [key(e["he"]) for e in entries]
    problems = []
    for e in entries:
        problems += [f"line {e['line']}: {p}" for p in check_english(e["en"])]
    if have != want:
        counts, seen, order = Counter(have), Counter(), len(problems)
        for c in dict.fromkeys(want):
            if counts[c] < want.count(c):
                problems.append(f"no English entry for the caption {c!r}")
        for e, h in zip(entries, have):
            seen[h] += 1
            if seen[h] > want.count(h):
                problems.append(f"line {e['line']}: " + (
                    "a second entry for the caption" if h in want
                    else "an entry for a caption that no longer exists") + f" {e['he']!r}")
        if len(problems) == order:
            first = next(i for i, (a, b) in enumerate(zip(want, have)) if a != b)
            problems.append(f"line {entries[first]['line']}: the entries are not in the captions' order "
                            f"(caption {first + 1} is {want[first]!r})")
    return [e["en"] for e in entries], problems


def english_vtt(cues: list[dict], english: list[str]) -> str:
    """The English WebVTT: the cues of captions.vtt (same numbers and times), English text."""
    out = ["WEBVTT", ""]
    for i, (c, en) in enumerate(zip(cues, english, strict=True), start=1):
        timing = c.get("timing") or f"{vtt_time(c['start'])} --> {vtt_time(c['end'])}"
        out += [str(i), timing, *en.split("\n"), ""]
    return "\n".join(out)
