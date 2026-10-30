# VIDEOS.md — the plan for the tutorial videos

Every question gets a tutorial video. The video walks through the solution step by step,
one chapter per part. This file is the plan: the owner's choices, the structure every
video follows, how a video is written, rendered, captioned, published and linked from its
page, the checks, and the order of work. The first two videos are pilots, 0002 and 0004.
Once their structure is approved, the rest follow it question by question.

## The owner's choices (2026-10-30)

| Topic | Choice |
|---|---|
| Technology | Manim (Community Edition), rendered to MP4 |
| Narration | Captions only for now. The script is written so a voice can be added later |
| Hebrew text | Kept out of the picture as far as possible. The Hebrew captions are a separate WebVTT file shown by the player |
| Hosting | YouTube, on the owner's channel. The site embeds the video |
| Look | The site's navy (the hero's) with amber marks, one version for both schemes |
| On the page | One video per question, a chapter per part, 1–3 minutes each |
| Pilots | 0002 (swap two variables) and 0004 (three mislabeled boxes) |

## Why the Hebrew stays out of the frame

Manim draws text through Pango and splits it into glyphs. Right-to-left lines and lines
that mix Hebrew with code are fragile there: the order of words can flip, and so can
punctuation. The video therefore carries only what reads the same in any direction:

- code, numbers, formulas, bits and arrows;
- boxes, balls and the other objects of the question;
- the part's letter (א, ב, ג) as a single glyph in the chapter card.

Everything said in words goes into the captions. The browser and YouTube lay out
Hebrew captions correctly, a screen reader reads them, and a wording fix needs no
re-render.

A label that must be in Hebrew inside the frame (rare: a name on a box, "אדום") is drawn
once by the browser. Playwright renders the label to a transparent PNG, and the scene
loads it as an `ImageMobject`. That is the same route the site's own figures take, so
the text is shaped right. The pilot of 0004 tests this route, because its labels are
Hebrew words.

## The structure of a video

A video is one file per question, with chapters. Each part of the question is one
chapter of 1–3 minutes, and a short opening and closing frame the chapters. The same
skeleton serves every question; the beats inside a chapter follow the page's solution
blocks (idea → steps → code → proof → cost), so the video and the page tell the same story
in the same order.

```
0:00  Opening (5–10 s)  — the site mark, the question's id, the level and the parts as chips
      Chapter א (1–3 min)
        1. The problem   — the part's setting drawn (the objects, the input, what is asked)
        2. The idea      — one picture of the key insight (the "aha"), held still for a moment
        3. The steps     — the page's worked example, animated step by step
        4. The code      — the Python answer, lines lit in the order they run on the example,
                           the variables beside it
        5. Why it works  — the proof as a picture (an invariant, a table, a case split)
        6. The cost      — time and memory as two chips, and where they come from
        7. One trap      — the most common mistake, shown failing on a small input
      Chapter ב …        — the same beats; it opens with what changed from the previous part
                           (the new constraint), so the ladder of the question is visible
      Closing (5–10 s)  — the parts side by side in one line each, and "try it in the box"
```

Rules for every video:

- **The page's example.** A chapter uses the example the page works by hand. A reader
  who pauses the video can find the same numbers on the page and in the box.
- **One idea per beat.** A beat ends on a still frame that holds for at least two
  seconds, so a pause lands on a readable picture.
- **The code is the page's code.** The code beat loads the code from the page's Python
  tab, so it never drifts from the tested code. Python only: the SystemVerilog stays on
  the page.
- **A caption per beat**, about 1–2 lines: 12 words per line at most, 2–6 s on screen.
- **Colours** come from the site's palette, read from `docs/stylesheets/01-base.css` by
  the shared library, so the video matches the site.
- **The frame** is 1280×720 at 30 fps. Text is at least 28 px high, so it can be read
  on a phone.

## The files

Everything for one question lives in its own folder. Shared code sits in `videos/lib`.

```
videos/
├── lib/
│   ├── dvq.py          # the shared Manim library: palette, fonts, opening/closing, chapter card,
│   │                   # code beat (from the page), chips, still-frame helper, caption recorder
│   ├── captions.py     # writes captions.vtt and chapters.txt from the recorded captions
│   └── he_label.py     # renders a Hebrew label to a transparent PNG with Playwright
├── 0002/
│   ├── script.md       # the storyboard: per chapter, per beat, the picture and the caption (Hebrew)
│   ├── scene.py        # the Manim scenes, one class per chapter + Opening + Closing
│   └── out/            # rendered, not committed: video.mp4, captions.vtt, chapters.txt
└── 0004/ …
```

- **The script** (`script.md`, Hebrew captions and English notes) is written first and
  reviewed by the owner before any animation is built. A video is cheap to rework at
  the script stage and expensive after the render.
- **The captions are recorded while the scene plays.** Each beat calls
  `self.say("…", hold=…)`. The library writes the caption with its exact start and end
  times, as the animation really ran. Captions are therefore in sync by construction,
  with no times typed by hand. `captions.py` turns the record into `captions.vtt`, and
  into `chapters.txt`: the chapter start times, in the format YouTube reads from a
  video's description.
- **The scenes** are chained into one video with ffmpeg's concat (no re-encode), so a
  fix to chapter ב re-renders chapter ב only.

## Rendering

- **Tools.**
  - `manim` (Community Edition, pinned in `requirements-video.txt`, apart from the site's
    requirements so CI does not install it).
  - `ffmpeg`.
  - The Code mobject (Pygments) for the code beats.
  - Math as `MathTex` needs LaTeX (`texlive-latex-base` and a few packages). The pilots
    check whether plain `Text` with Unicode math is enough for the easy questions.
- **The command.** `python videos/render.py 0002` renders the chapters at 720p30, chains
  them, and writes `video.mp4`, `captions.vtt` and `chapters.txt` to `videos/0002/out/`.
  The flag `--draft` renders at 480p15 for a quick look.
- **Rendering stays local.** It does not run in CI: Manim and LaTeX are heavy, and the
  MP4 is not served from the site.

## Publishing and linking

1. **Upload.** The owner uploads `video.mp4` to the YouTube channel. Unlisted or public
   is the owner's call per video.
2. **Captions and chapters.** The owner adds `captions.vtt` as the Hebrew captions,
   pastes `chapters.txt` into the description (YouTube makes chapters from it), and
   turns captions on by default.
3. **The page.** The video id and the chapter times go into the page's front matter:

   ```yaml
   video: dQw4w9WgXcQ          # the YouTube id
   video_parts: [0, 95, 210]   # the start of each part's chapter, in seconds
   ```

4. **The hook** (`hooks/questions.py`) does the rest:
   - It adds a "סרטון הסבר" button to the question's header card, and a "לפרק בסרטון"
     link at the top of each part's solution, which starts the video at that part's
     chapter.
   - The video opens in a dialog above the page.
   - It is a light facade, with no YouTube code until the click: a still image and a
     play button. The click loads the player from `youtube-nocookie.com` with
     `cc_load_policy=1` (captions on) and `start=<part>`.
   - The page keeps its weight and no cookies are set before the reader chooses to
     watch.
   - The page checks run offline, so they never load YouTube.

## Checks

- **`tools/check_videos.py`** (new, runs in CI with the tests, needs no video). For every
  question with a `video:` field:
  - the id has the YouTube form;
  - `video_parts` has one time per part, rising from 0;
  - the folder `videos/<id>/` exists, with a `script.md` whose chapter count equals the
    page's parts.

  For every `script.md`, every caption follows the RTL rules of CLAUDE.md:

  - it starts with a Hebrew word or an RLM;
  - a colon has a non-breaking space before it;
  - lines are at most 12 words.
- **The page checks** must stay green: `check_phone`, `check_keyboard` and axe. The dialog
  is checked as a component: focus trapped, Esc closes, the button named, and the
  iframe titled.
- **`render.py`** stops on a caption shorter than 1.5 s or longer than 7 s, and on a
  beat with no still frame at its end.

## Order of work

| Step | What | Done when |
|---|---|---|
| V0 | This plan | the owner approves it |
| V1 | `videos/lib` (palette, opening/closing, chapter card, code beat, caption recorder, VTT and chapters), `render.py`, `requirements-video.txt` | a 20 s test scene renders with captions in sync |
| V2 | Pilot 0002: script → owner review → scenes → render | the owner approves the video and its captions |
| V3 | The site side: front matter fields, the hook's button, links and dialog, `check_videos.py`, CONTRIBUTING | 0002's page plays its video from YouTube at each part |
| V4 | Pilot 0004: script → review → scenes (Hebrew box labels by `he_label.py`) → render | approved, and the Hebrew-label route is proven |
| V5 | Freeze the structure: lessons from the pilots folded into this file | the owner approves |
| V6… | The rest, a few questions per round, short questions first (student, then junior) | each video approved before upload |

## The pilots' storyboards (outline; the full scripts are step V2 and V4)

**0002 — swap two variables (three parts, ~5 min in all)**

- **Opening.** Two registers `a = 6` and `b = 9`, shown as boxes with their bits.
- **Chapter א — with a temp variable.**
  - A third box `t`; the three moves animated; the values travel as cards.
  - Code: three lines, lit in turn.
  - Why it works: each value always sits in at least one box.
  - Cost: O(1) time and one word of memory.
  - Trap: the order of the moves, shown failing when the first move is lost.
- **Chapter ב — no temp, arithmetic.**
  - The new constraint is struck out on the chapter card: the `t` box fades away.
  - `a = a + b`: the sum appears; then the two subtractions recover each value.
  - A number line shows why no information is lost.
  - Overflow: the 32-bit wheel (mod 2^32) turns past the top and still comes back right.
  - Trap: `swap(x, x)`, the same variable twice, giving 0.
- **Chapter ג — bitwise only.**
  - The same three steps with `^`, on 4-bit columns: a bit flips where the column has a 1.
  - The XOR rules as a 2×2 table.
  - The proof: each bit column separately.
  - Trap: the same address again, and why `&` or `|` lose information (a column that can
    no longer be undone).
- **Closing.** Three lines side by side: temp / sum / XOR.

**0004 — three mislabeled boxes (two parts, ~4 min in all)**

- **Opening.** The three boxes with their Hebrew labels (`he_label.py`) and the rule "all
  labels are wrong" as a red stamp.
- **Chapter א — the minimum number of draws.**
  - The six ways to fill the boxes shrink to the two in which every label is wrong (a
    permutation table with the fixed points struck out).
  - Drawing from a red or a black box can leave two cases open; drawing from "mixed"
    cannot.
  - One draw, so the answer is 1, and zero draws is not enough.
  - Both cases are played out: a red ball, then a black ball.
- **Chapter ב — the code.**
  - `draw(i)` as a hand taking one ball.
  - The first solution: find the box labelled MIXED, draw once, and fill a new label
    array in three passes by part א's rule. Its lines are lit for a red result, then for
    a black one.
  - The page's second solution: the fix is a rotation of the three labels, shown as the
    labels sliding one box over. Two swaps in place do it, with no new array.
  - The index arithmetic: `(k + 1) % 3` and `(k + 2) % 3`, and why `(k - 1) % 3` differs
    between Python and SystemVerilog for k = 0.
  - Cost: O(1).
- **Closing.** One draw from the "mixed" box fixes all three labels.

## Open points for later

- **Voice.** Each caption is a full sentence, so a recorded voice (the owner's, or a
  generated one) can be added later. The captions become its script, and the timing
  moves to the voice track.
- **An English version.** Only the captions file changes: a second `captions.en.vtt`.
- **Long questions.** The protocol questions, 0020 to 0025, may need 4–5 minutes per
  part. Splitting a part into two chapters is allowed there.
