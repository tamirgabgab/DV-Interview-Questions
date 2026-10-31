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
| On the page | One video per question, a chapter per part: 1–3 minutes, 2–4 for a complex part (2026-10-30) |
| Pace | Calm, in the style of 3Blue1Brown: animations of 1–2 s, every picture held 2–4 s for its caption |
| Code beat | Python only |
| Opening and closing | The drawn DV mark, the question's id and parts; the closing has the site's address and the question's id |
| Review | The pilots are scripted and rendered in one go; the owner reviews the videos |
| Pilots | 0002 (swap two variables) and 0004 (three mislabeled boxes) |

## Why the Hebrew stays out of the frame

Manim draws text through Pango and splits it into glyphs. Right-to-left lines and lines
that mix Hebrew with code are fragile there: the order of words can flip, and so can
punctuation. The video therefore carries only what reads the same in any direction:

- code, numbers, formulas, bits and arrows;
- boxes, balls and the other objects of the question;
- nothing in Hebrew drawn by Manim: even the part's letter on the chapter card is a
  label PNG (below).

Everything said in words goes into the captions. The browser and YouTube lay out
Hebrew captions correctly, a screen reader reads them, and a wording fix needs no
re-render.

A label that must be in Hebrew inside the frame (rare: a name on a box, "אדום") is drawn
once by the browser. Playwright renders the label to a transparent PNG, and the scene
loads it as an `ImageMobject`. That is the same route the site's own figures take, so
the text is shaped right. The pilot of 0004 tests this route, because its labels are
Hebrew words. `videos/lib/he_label.py` draws each label in Rubik (the site's text font,
fetched once from Google Fonts into `videos/.cache/fonts`, with DejaVu Sans as the
fallback) at twice the frame's pixels, and caches it by text, size, colour and weight in
`videos/.cache/labels`. The pilots use it for the opening's title, level and part chips,
the chapter cards, the closing's part letters, and 0004's box labels and stamp.

## The structure of a video

A video is one file per question, with chapters. Each part of the question is one
chapter of 1–3 minutes (2–4 for a complex part), and a short opening and closing frame the chapters. The same
skeleton serves every question; the beats inside a chapter follow the page's solution
blocks (idea → steps → code → proof → cost), so the video and the page tell the same story
in the same order.

```
0:00  Opening (15–25 s) — the DV mark drawn as on the site, the question's id, the level and the parts as chips
      Chapter א (1–3 min, 2–4 for a complex part)
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
      Closing (10–15 s) — the parts side by side in one line each, the site's address and the
                          question's id ("try it in the box")
```

YouTube ignores a chapter shorter than 10 s, so the opening and the closing, which are
chapters of their own in `chapters.txt`, last at least 10 s (render.py checks it).

Rules for every video:

- **The page's example.** A chapter uses the example the page works by hand. A reader
  who pauses the video can find the same numbers on the page and in the box.
- **One idea per beat.** A beat ends on a still frame that holds for at least two
  seconds, so a pause lands on a readable picture.
- **The code is the page's code.** The code beat loads the code from the page's Python
  tab (`tools/extract_code.py`, without the annotation markers), so it never drifts from
  the tested code. Python only: the SystemVerilog stays on the page. The library runs the
  page's function on the example under a line tracer, so the lines are lit in the order
  they really ran, with the locals after each line beside the code; the scene only groups
  the traced lines under its captions, and the render fails if the groups differ from the
  trace. A long function may leave its comment and blank lines out of the picture (0004's
  first solution), never its code.
- **A caption per beat**, 1–2 lines: 12 words per line at most, 1.5–7 s on screen. The
  still after a beat's animations is held long enough to read its caption at about 14
  characters a second, between 2 and 4 s.
- **Colours** come from the site's palette, read from `docs/stylesheets/01-base.css` by
  the shared library (and the figure colours of `02-pages.css` and `08-explorers.css`:
  the crates and the balls of 0004), so the video matches the site. The marks on the navy
  take the dark scheme's values, made for a dark surface.
- **Fonts.** Inter for Latin text and math (its sub- and superscripts sit tight:
  `a₀`, `2³¹`), DejaVu Sans Mono for code and numbers, Rubik for the Hebrew labels.
- **The frame** is 1280×720 at 30 fps. Text is at least 28 px high, so it can be read
  on a phone. The bottom 1.5 units (about 135 px) are the captions' zone: the player
  draws the captions there, so the picture stays above it (`dvq.SAFE_BOTTOM`).
- **Math in the captions.** `captions.vtt` wraps every code or math expression of a
  caption in Unicode isolates (LRI … PDI, added by `captions.isolate()` when the file is
  written; `script.md` stays as typed). Without them a right-to-left line reorders
  expressions around their parentheses and numbers: Chromium showed `[3, 5]` as `[5 ,3]`
  and `(k + 1) % 3` with its parenthesis moved. Both the browser and libass (the burned
  preview) honour the isolates.

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
│   └── out/            # rendered, not committed: video.mp4, captions.vtt, chapters.txt,
│                       # parts/ (each scene's recorded captions), media/ (Manim's files)
└── 0004/ …
```

- **The script** (`script.md`, Hebrew captions and English notes) is written first and
  reviewed by the owner before any animation is built. A video is cheap to rework at
  the script stage and expensive after the render. Its format is fixed, because
  `tools/check_videos.py` reads it (see "The script's format" below).
- **The captions are recorded while the scene plays.** Each beat calls
  `self.say("…", hold=…)`. The library writes the caption with its exact start and end
  times, as the animation really ran. Captions are therefore in sync by construction,
  with no times typed by hand. `captions.py` turns the record into `captions.vtt`, and
  into `chapters.txt`: the chapter start times, in the format YouTube reads from a
  video's description.
- **The scenes** are chained into one video with ffmpeg's concat (no re-encode), so a
  fix to chapter ב re-renders chapter ב only.

### The script's format

```markdown
# 0002 — swap two variables

## Opening

> שתי קופסאות : a = 5 ו-b = 3.

## Chapter א — with a temp variable

Beat 1, the problem: two boxes and a third one, t (English notes are plain lines).

> משתנה עזר שומר את הערך שהיה ב-a.
> ‏temp = a, ואז a = b, ואז b = temp.

## Chapter ב — no temp, arithmetic
...

## Closing
```

- **Chapters.** One `## Chapter …` heading per part of the question, in the page's order.
  `## Opening` and `## Closing` are not chapters. Any other heading level is free for
  notes (`### Beat 1`). The number of `## Chapter` headings must equal the page's parts.
- **Captions.** A caption line starts with `> ` (a Markdown quote), one line of the
  caption per `> ` line, so a two-line caption is two consecutive `> ` lines. Every other
  line is a note in English, and a note is never a quote. Lines inside a fenced code block
  are neither captions nor chapters.
- **Caption rules** (CLAUDE.md's RTL rules, checked line by line):
  - the text after `> ` starts with a Hebrew letter, or with the RLM mark (U+200F) when it
    must start with code, a number or Latin text;
  - every colon has a non-breaking space (U+00A0) before it and an ordinary space (or the
    end of the line) after it; a time or a ratio (1:35, 3:2), a URL and `code` in
    backticks are exempt;
  - at most 12 words per line (a word is a run of characters with a letter or a digit
    in it, so a lone colon or dash does not count).

## Rendering

- **Tools.**
  - `manim` (Community Edition, pinned in `requirements-video.txt`, apart from the site's
    requirements so CI does not install it).
  - `ffmpeg`.
  - The Code mobject (Pygments) for the code beats.
  - No LaTeX. The pilots showed that `Text` with Unicode math (`a₀`, `2³¹`, `−`, `≡`) is
    enough, so nothing installs it. The Manim parts that call LaTeX are avoided:
    `MathTex`, `Tex`, the numbers of a `NumberLine`, `DecimalNumber`, `MathTable`,
    `BraceLabel`.
- **The command.** `~/.venvs/manim/bin/python videos/render.py 0002` (any Python with
  `requirements-video.txt`) renders the chapters at 720p30, chains them, and writes
  `video.mp4`, `captions.vtt` and `chapters.txt` to `videos/0002/out/`. The flag
  `--draft` renders at 480p15 for a quick look, and `--preview` also writes
  `preview.mp4` with the captions burned in (libass, Rubik, `Encoding=-1` so the base
  direction is right to left) for a review in a plain player. The steps:
  1. **Read** `scene.py`'s `SCENES` (the scene classes in order, each with its chapter
     title for `chapters.txt`) and `script.md`'s captions, and fail early when a literal
     caption of `scene.py` is not in the script or breaks a caption rule.
  2. **Labels.** A Manim `--dry_run` lists the Hebrew labels, and `he_label.py` draws the
     missing ones in one browser session, with a Python that has Playwright
     (`--label-python`, default `python3`).
  3. **Render** every scene, then chain them with ffmpeg's concat demuxer: a stream copy
     when the scenes' parameters match (they do), a re-encode otherwise.
  4. **Captions.** Each scene's recorded captions are shifted by the real duration of the
     scene files before it.
  5. **Fail** on a caption under 1.5 s or over 7 s, a line that breaks the RTL or colon
     rules, a beat whose still is under 2 s, a chapter under 10 s, captions that differ
     from `script.md` (text, line breaks or order), or a scene whose recorded length
     differs from its file. It prints the length, the size, the chapters and the
     `video_parts` for the front matter (the first part at 0, as the checks want: the
     link to part א plays the opening too).
  A pilot renders in about 2–3 minutes as a draft and 4–6 minutes at 720p30.
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

   The id is quoted when YAML would read it as a number or a boolean. A page with one
   part may leave `video_parts` out. The build, `lint_pages.py` and `check_videos.py`
   all reject a bad id, a missing time, a count that differs from the page's
   `### סעיף` headings, a first time other than 0, or times that do not rise.
   Then `python tools/catalog.py` turns the README's "Tutorial videos" row of that
   question into a YouTube link. The table has a row per `videos/<id>/script.md`, and a
   test checks that it is up to date.
4. **The hook** (`hooks/questions.py`) does the rest:
   - **The page tool.** A "סרטון הסבר" icon button (a screen with a play triangle) first
     among the page tools of the header card. Practice mode hides it with the solutions.
   - **The chapter links.** A "לפרק בסרטון 1:35" pill at the top of the first solution
     block of each part, right under its summary, so it shows only to a reader who
     opened the solution. On a page without parts the one link reads "לסרטון ההסבר".
     Its `href` is the video on youtube.com at that time, for a reader without the script
     or one who opens it in a new tab.
5. **The dialog** (`docs/javascripts/video.js`, `docs/stylesheets/20-video.css`):
   - **A native `<dialog>`, modal.** It is titled "סרטון הסבר : <the question's title>"
     and the focus moves to the play button. Tab and Shift+Tab cycle inside it. Esc,
     the × button and a click on the backdrop close it, and the focus returns to the
     button or link that opened it.
   - **The poster.** The site's navy with a faint grid, two amber traces and the
     question's id and title, an amber play disc and the start ("הפעלה מסעיף ב · 1:35").
     It is CSS only, the same in both schemes. Nothing comes from YouTube until the
     reader presses play: no request, no thumbnail, no cookie, and the page keeps its
     weight.
   - **Chapter buttons.** Above the stage, one per part ("סעיף ב 1:35"), the chosen one
     amber. Before play they move the poster's start; while playing they restart the
     player at that part.
   - **The player.** Play puts an iframe in the poster's place:
     `https://www.youtube-nocookie.com/embed/<id>?start=<s>&cc_load_policy=1&cc_lang_pref=he&hl=he&rel=0&modestbranding=1&autoplay=1`,
     titled like the dialog, with `allow="autoplay; encrypted-media; picture-in-picture; fullscreen"`
     and `allowfullscreen`. Closing removes the iframe, which stops the video.
   - **The size.** The stage is 16:9, as wide as the screen allows up to 60rem and short
     enough for a landscape phone. Under 30em the dialog runs edge to edge.
   - The page checks run offline, so they never load YouTube; `check_keyboard.py` cuts
     the player's request off when it presses play.

## Checks

- **`tools/check_videos.py`** runs in CI's test job, after the lint, and needs no video.
  For every question with a `video:` field:
  - the id has the YouTube form;
  - `video_parts` has one time per part, rising from 0;
  - `videos/<id>/script.md` has one `## Chapter` heading per part of the page. A page
    whose script does not exist yet gets a warning, not a failure.

  For every `videos/*/script.md`, every caption line (`> …`) follows the caption rules
  above. Its tests are in `tests/tools/test_check_videos.py`, and the hook's in
  `tests/hook/test_hook.py` (a page with a fake id, never a real page).
- **The page checks** must stay green: `check_phone`, `check_keyboard` and axe. The dialog
  is checked as a component by `check_keyboard.py`, on the first question page with a
  video: Enter opens it with the focus inside, Tab and Shift+Tab stay in it, its buttons
  are named, Esc closes it and gives the focus back, and play makes a titled iframe that
  the close button removes.
- **`render.py`** stops on a caption shorter than 1.5 s or longer than 7 s, on a beat
  with no still frame of 2 s at its end, on a chapter under 10 s, and on captions that
  differ from `script.md` (see "Rendering").

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

- **Opening.** Two registers `a = 5` and `b = 3` (the page's example), shown as boxes with
  their bits.
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

- **Review.** The pilots skip the separate script review: script and video are made in
  one go and the owner reviews the video. Whether later rounds keep this is decided after
  V5.

- **Voice.** Each caption is a full sentence, so a recorded voice (the owner's, or a
  generated one) can be added later. The captions become its script, and the timing
  moves to the voice track.
- **An English version.** Only the captions file changes: a second `captions.en.vtt`.
- **Long questions.** The protocol questions, 0020 to 0025, may need 4–5 minutes per
  part. Splitting a part into two chapters is allowed there.
