# PLAN: the next rounds (a fresh review, 2026-11-21)

The owner cancelled the old backlog on 2026-11-21 (it is kept, as it stood, in
[`HANDOFF-archive-4.md`](HANDOFF-archive-4.md)) and asked for a wide, fresh review of the
whole site and for proposals of a different kind: new styles of questions, the visual look,
effects, better explanations, new elements and a better interactive interface. This file is
the result: what the review found, and its proposals grouped into rounds 11 to 23 for the
owner to pick from. The first plan, rounds 1 to 10, is closed in [`ROUNDS.md`](ROUNDS.md).

How to use it: pick a round, answer its open questions, and the session implements it by the
usual flow (work branch, the checks, branch CI, `main` when the owner says). Tick the round's
status line here and write the outcome in the work log of [`HANDOFF.md`](HANDOFF.md). A round
can be taken whole or one proposal at a time; the ids (11.1, 11.2 and so on) are stable.

## How the review was done

Four reviewers worked in parallel on the built site and the sources, read-only, each with one
lens and the third-party skills that fit it, and the lead looked at the main pages itself and
spot-checked the findings:

| Lens | What was looked at | Skills applied |
|------|--------------------|----------------|
| Pedagogy and question formats | 14 question pages from source (7 in full), 4 rendered at 390 px with folds open, the template, the paths, interview mode | the repository's `dv-question` |
| Visual design, figures, motion | home, lists, paths, tags, new, how-built, a level page, the map, the 404 page and 11 question pages, at 1440 and 390 px, light and dark; a returning learner's state; a print render | `impeccable` (critique, animate), `diagram-design`, `ui-ux-pro-max` |
| The interactive layer | all 208 boxes swept at 1440 and 390 px with touch, 14 pages driven by hand, the steppers, the hints, interview mode, the run panel's interface | `ui-ux-pro-max`, `webapp-testing`, `vectorlab-ux-skills:ux-audit` (on 0114) |
| The site as a product | four journeys in the browser (a first visit, a returning learner with 20 solved, an arrival from a search engine, "a 40-minute session"), the stored state, the service worker, search | `web-quality-audit`, `seo`, `accessibility`, `best-practices`, `ui-ux-pro-max` |

Limits of the review: Pyodide and vis-network could not load in the sandbox (their CDN is
blocked), so the run panel's execution and the map's canvas were judged from the code; the
social cards are not built locally and were judged from their layout file; the live site is
not reachable from the sandbox.

## The headline

The quality inside a page is not where the gap is. Ideas come before formalism, hand-worked
tables come before proofs, traps name the wrong number a candidate would get, and 555 of the
712 hints are phrased as questions. Every page has a box, and every claim on a page is
executed by a test. The gaps are **around** the page:

1. **Nothing comes back.** A solved mark has no date, and nothing on the site resurfaces a
   solved question, although the pages hold 493 follow-ups with short answers and 447 traps,
   all card-sized and hidden at page ends.
2. **The mock interview ends in nothing.** A series of three questions ends on the last
   question's own numbers and one line of congratulation; there is no outcome, no report, and
   the solved marks do not change. The rubric is already written on every page ("מה המראיין
   בודק") and is not used.
3. **Nothing is short.** The median page is about 1,700 Hebrew words and 14 to 29 phone
   screens with the folds open. The two-minute concept question, the most common DV interview
   format, does not exist; no page mentions mailbox, semaphore, shallow or deep copy, `randc`
   or `modport`.
4. **The boxes show; they rarely ask.** All 208 boxes are titled "נסו בעצמכם", and their
   summaries state the answer at step 0. Only 32 of the 208 fit one phone screen, so the
   button pressed and the figure it changes are often not in view together; on a laptop only
   4 of the 125 boxes that declare two columns get them.
5. **The best data on the site is invisible.** `tools/build/graph_concepts.json` holds 158
   hand-written concepts, 78 of them shared by three or more questions, and related links
   with a reason each. Its only output is `graph.html`, which no page links to and whose
   panel is in English.
6. **Two figure languages.** The 379 generated figures share one palette and are tested;
   the 16 WaveDrom and 11 Mermaid diagrams keep their libraries' default look, and a
   WaveDrom diagram is a white slab in dark mode.

## What already exists (verified; do not propose again)

- **A question page:** the interviewer block, the hint ladder with a lock and dots, the short
  answer with cost chips, the solution blocks with a sticky map, traps and follow-ups with
  collapsed answers, steps beside a figure (`steps-fig`, four pages), a part timeline, code as
  an editor window with linked Python and SystemVerilog tabs, an end card, related questions
  by shared tags, print of one question.
- **Interview mode:** a clock against a target (10, 15 or 25 minutes), hints counted, "how
  sure are you?" before a solution, a summary beside the previous attempt, a link to the next
  question of a series.
- **The home page:** the hero with a live board, the interview builder (level, 20 / 40 / 60
  minutes, kinds, unsolved first), the question of the day, a continue card, "my map", level
  cards, a compact metro map.
- **Lists and paths:** `all/` with filters, search, sort and state in the address; level pages
  with a progress band; `new/`; `tags/` with a tag graph; 13 paths with a metro map, solved
  stations, a strip on every question and a toast and confetti at a finished path or level.
- **Boxes:** a shared shell in `core.js` (header with help, reset and copy link; state links;
  remembered state; a playback bar with a scrubber and keys; steady heights; change flashes;
  lazy building; a first-visit guide), an answer line (112 boxes), seeded draws (81), a
  steps-and-code panel (0061 to 0070), timing strips with WaveDrom export (13 kinds), a wave
  viewer with cursors under WaveDrom diagrams.
- **The run panel:** Python in the browser on 100 pages, with run, stop, reset and a check of
  `print()` lines against their expected-value comments.
- **Site:** Material search with Hebrew prefix variants, a quick jump, descriptions, JSON-LD,
  sitemap dates, social cards, a manifest and a network-first service worker that keeps
  visited pages, a 404 page that offers the question from the address, view transitions
  between pages, a considered dark scheme. No analytics and no cookies.
- **Removed by the owner on 2026-11-02, not to come back:** typed self-check fields on the
  page ("length and weight, and nothing a reader does not get by opening the solution").

## What must not be lost

- **Every claim is executed.** Tables, logs, waveforms and counts come from runs; a new
  format keeps an executable ground truth or it does not go in.
- **The recipe of a page:** a concrete scene with numbers, Socratic hints, the idea before
  the code, a hand trace, a proof that names its method, traps with the wrong value, short
  follow-ups, and the "נסו בעצמכם" paragraphs that script a box as an experiment with a
  predicted outcome.
- **The domain-native identity:** the clock-signal reading line, the question chip with pins,
  the difficulty LEDs, the trace pattern, the "lost signal" 404 page.
- **The generated-figure discipline** (one palette through variables, tested against the
  generators) and the **shared box shell**; new work extends them, never a parallel system.
- **Restraint:** one set of durations, everything off under reduced motion, nothing moving
  while a page loads, the figure still while a box steps.
- **Personal state that is honest and quiet:** everything in the browser, no accounts, no
  streak pressure, personal parts hidden until there is something to show.
- **The paths as the spine** and **the hook as the single writer** of every derived surface:
  a new feature is "the hook writes one more small JSON, a pure function consumes it, a Node
  test covers it".

## The rounds

| Round | What the reader gets | Proposals | Size | Model, effort | Why this model |
|-------|----------------------|-----------|------|---------------|----------------|
| 11. Quick wins | dark-mode waveforms that fit the site, search in both languages, true texts, bigger touch targets | 11.1 to 11.6 | small | Sonnet 5.5, high | separate, well-defined fixes; the checks catch mistakes |
| 12. The interview as a session | a rubric to grade yourself by, a report at the end, a series to send a friend, clarifying questions | 12.1 to 12.6 | medium | Opus 5.5, high | one shared script and a new page block; judgment in the wording |
| 13. What you solved comes back | a five-minute daily review from the pages' own follow-ups | 13.1 to 13.3 | medium | Opus 5.5, high | a new page, a hook export and a scheduler, all testable |
| 14. My area | a personal page, a home page that knows a returning reader, progress on another device, a plan to the interview date | 14.1 to 14.4 | large | Fable 5.2, high | touches the home page's first paint and the stored state of every reader |
| 15. Techniques | "where else does this trick appear", a page per technique, the map inside the site | 15.1 to 15.4 | medium to large | Opus 5.5, high | 158 Hebrew labels and primers: content judgment, then mechanical |
| 16. Boxes that ask | a mission per box, "show it in the box" links, one stepping convention, code lit by the step | 16.1 to 16.4 | medium | Opus 5.5, high | extends `core.js`, which 208 boxes share |
| 17. A box on one screen | a focus mode, a playback bar that stays with the figure, predict-then-reveal, pin and compare | 17.1 to 17.4 | large | Fable 5.2, high | layout of every box at every width; the jump and height checks |
| 18. Practice by writing | your own solution checked, tests that kill mutants, a drawn waveform, the simulator's real transcript | 18.1 to 18.4 | large | Fable 5.2, xhigh | new exercise types on top of the run panel; correctness is the product |
| 19. New kinds of questions | two-minute concept cards with tested "what prints", spec to verification plan, debug with staged evidence, four new areas | 19.1 to 19.4 | very large | Fable 5.2, xhigh | new content and a new page family; a mistake costs the most here |
| 20. Explanations | the first solution before the idea, "enough for the interview", a block that does not leak, pictures on the DV pages, steps that light the figure and the code | 20.1 to 20.5 | large | Opus 5.5, xhigh | a pass over many pages; each change re-runs the page's tests |
| 21. Figure craft | captions and numbers, one arrow and label grammar, waveforms drawn by the site, steps that move | 21.1 to 21.6 | large | Opus 5.5, high | generators and regenerated pages; the figure tests catch drift |
| 22. Paths with a finish line | a path that looks like its metro line, a finish card, a home map without the empty panel | 22.1 to 22.3 | small to medium | Sonnet 5.5, high | the hook and CSS, on 14 pages and the home page |
| 23. Take it with you | an offline pack, a designed print sheet, an interviewer's sheet for a friend, share, a feed, English one-liners, an about page and a licence | 23.1 to 23.8 | medium to large | Opus 5.5, high | many small separate surfaces; the service worker needs care |

The model column is a judgment by the kind of work and its risk, as in `ROUNDS.md`; a cheaper
model gets one proposal at a time and a higher effort.

**A suggested order.** Round 11 first: it is small and fixes the one visible defect the
review found (waveforms in dark mode). Then the three rounds that most change how the site
feels to someone who comes back: 12 (the interview), 13 (the daily review) and 16 (boxes
that ask). Round 19 is the largest and the one that adds the most new content; round 14 is
best after 12 and 13, which give it something to show. Dependencies: 13.1 (dated marks) is
needed by 13.2, 14.1, 14.4 and 12.5's review preset; 15.1 (Hebrew concept labels) is
needed by 15.2 to 15.4; 17.1 (focus mode) gives 17.3 and 16.4 their room; 21.3 (waveforms
drawn by the site) is the second phase of 11.1; 20.3 is the authoring half of 12.2.

## Round by round

Each proposal: what the reader gets, the evidence, a sketch, its size (S, M, L), and what it
touches. "Checks" names the checks that need a new case, beyond the usual run.

### Round 11. Quick wins

- **11.1 Waveforms and flowcharts in the site's look (phase A).** WaveDrom ships its own
  skin: Helvetica, blue names, green bus values and an inline white background, so in dark
  mode each of the 16 diagrams (9 pages; six on 0110) is a white slab. The 11 Mermaid
  diagrams (7 pages) keep their default colours; on 0025 the first flow has unreadably small
  labels. Sketch: a site copy of WaveDrom's `skins/default.js` served from
  `docs/javascripts/` with `currentColor` strokes and palette variables and no background
  rectangle (`WAVEDROM_CDN` in the hook points to it); Material's `--md-mermaid-*` variables
  set in `01-base.css`. A CSS-only reskin was tried and is not enough. S. Checks:
  `check_contrast.py` pairs for the wave ink on both grounds; the 9 px rule of the phone check.
- **11.2 Search that answers in both languages.** The quick jump finds nothing for coverage,
  fsm, debug, probability, constraint, handshake, factory, josephus (the word is in the
  page's own address), פיפו or metastability, and "גריי" matches only "סוגריים". Sketch:
  `questions.json` gains a field of search words per question (tag slugs, the words of the
  address); whole words score first; a small `SYNONYMS` table in the hook for
  transliterations, also written into the search index's alternative text; rows for paths
  and topics in the quick jump. S to M. Checks: the failing words as cases in
  `tests/tools/test_interview.py`.
- **11.3 Texts that are true.** The home FAQ (`docs/index.md`) says interview mode "סופר
  רמזים ותשובות נכונות" and that the interviewer asks a follow-up after each right answer;
  both went with the self-checks. `README.md` says 92 questions (115) and `CONTRIBUTING.md`
  "Twelve paths" (13). Sketch: fix the texts; `tools/build/catalog.py` rewrites the README's
  counts between markers. S.
- **11.4 Touch and feedback.** Preset chips ("מקרי מלכודת"), "copy WaveDrom" and the
  scrubber are 22 px high on a phone where every other button is 44; "reset everything" in a
  box has no undo while the solved mark has one; a failed download of the run panel prints a
  raw browser error with no retry. S. Checks: target sizes in the phone check.
- **11.5 The map is reachable.** `graph.html` is linked from no page and is not in the
  sitemap. Sketch: links from `tags/` and `paths/`; its six English panel strings translated
  in `tools/build/graph.py`. (Its full place in the site is round 15.) S.
- **11.6 Path rows use their width.** A path row clips its description at about 45
  characters with half the row empty. S.
- Open questions: none; it can start at once.
- Status: done on 2026-11-21 (branch `claude/vibrant-ritchie-8ju107`). 11.1: WaveDrom's skin
  is restyled in `wavedrom-init.js` (prefixed shape classes, palette rules, no white
  rectangle; the text keeps Helvetica's widths at 11pt), Mermaid takes `--md-mermaid-*`, and
  the wide flows of 0023 and 0025 run top to bottom. 11.2: `search_words()` and `SYNONYMS`
  in the hook, whole words first, path and topic rows. 11.3: FAQ, README counts between
  markers (`catalog.py`), CONTRIBUTING. 11.4: box controls 36 px on touch, `--touch` fails a
  control under 24 px, an undo after "reset everything", a retry in the run panel. 11.5:
  links from paths and tags, the sitemap, a Hebrew panel. 11.6: two-line descriptions.

### Round 12. The interview as a session

- **12.1 Grade yourself against "מה המראיין בודק".** The summary of an interview shows time,
  hints and the confidence given, never an outcome. 112 of the 115 pages have an interviewer
  block of 3 to 6 bullets with a bold name each. Sketch: at "סיום הראיון" the bullets become
  tick boxes ("נגעתי בזה"), read from the page's own DOM; the record keeps n of m and the
  last five attempts; one calibration line ("אמרתם 'בטוחים', סימנתם 2 מתוך 5"). No free text,
  no typed answer. S to M. Checks: `check_keyboard.py`, a contrast pair.
- **12.2 The block does not give the answer away.** The block is documented as safe to open
  before solving, and on 10 of the 14 pages read it states the method or the answer (0087
  names Gaussian elimination over GF(2), which is hint 3; 0061 gives part ב's formula; 0064
  names the two bases). In interview mode it opens freely and is not counted. Sketch: in
  interview mode the block is locked until a solution opens (or counts as a hint); an
  authoring pass moves the revealing bullets behind a marker that shows them only after the
  solution. S for the mechanism, M for the pass over 115 pages.
- **12.3 A report for the whole series.** A three-question series ends with "סיימתם את כל
  הסדרה. כל הכבוד!" and the solved marks unchanged. Sketch: `dvq-plan` keeps each question's
  result; the last summary shows a table (time against target, hints, confidence against
  the rubric, the weakest point) with "לסמן כפתורות" for those that went well; the bar shows
  the series clock ("שאלה 2 מתוך 3 · 23:10 מתוך 40"). M. Checks: Node cases for the totals, a
  print rule for the report.
- **12.4 Send the same interview to a friend.** Sketch: the plan as a link
  (`?plan=0005.0102.0033`) read by the home page; the result as text through the share
  sheet with a clipboard fallback. S.
- **12.5 Builder presets.** `buildPlan` shuffles one level's questions, so the shape of a
  real DV interview (design, verification, short code, a puzzle) comes out only by chance.
  Sketch: "ראיון טיפוסי" (one per kind, in that order, within the minutes), "מהמועדפים",
  "ממסלול", and "חזרה מעורבת" over solved questions (needs 13.1). S.
- **12.6 "שאלות הבהרה": the first two minutes.** No page has clarifying questions, and the
  statements are fully specified: 0033 states the assumption that its own interviewer block
  says the interviewer is checking. Sketch: one optional `??? ask "מה כדאי לשאול לפני
  שמתחילים"` block between the interviewer block and the first hint, items with a collapsed
  "מה המראיין עונה" (the follow-ups' shape, already linted); interview mode shows it first.
  S for the mechanism, M for the 29 design and dv pages, three items each.
- Open questions: lock the interviewer block in interview mode, or count opening it as a
  hint? Should an interview that ends with most of the rubric ticked mark the question
  solved by itself, or only offer the button?
- Status: not started.

### Round 13. What you solved comes back

- **13.1 A solved mark with a date.** `dvq-marks` stores `1`. Sketch: `marks.js` stores the
  time instead (an old `1` reads as "unknown date"; every reader of the marks tests
  truthiness, so nothing else changes). S. It unlocks 13.2, 14.1, 14.4 and 12.5.
- **13.2 "חזרה של היום": a review deck.** The 493 follow-ups are card-sized (a median
  question of 81 characters and answer of 206; 11 answers hold code). Sketch: the hook
  writes the follow-ups of each question as a small JSON at build time (the built HTML,
  math already rendered); a `review/` page shows the cards that are due, one in the DOM at
  a time: the page's title and the question, reveal, "ידעתי / לא ידעתי", coming back after
  1, 3, 7, 14 and 30 days (Leitner boxes, pure functions tested under Node); starred and
  "לא ידעתי" first; a cap of about 15 a day and never a debt or a streak. M. Checks: a hook
  test that every question yields its cards, the scheduler under Node, the page in the
  phone and keyboard checks.
- **13.3 The entry point.** One line in the home page's continue card ("3 לחזרה היום") and
  a link in the footer; nothing moves at load. S.
- Open questions: cards from follow-ups only, or also from the 447 traps (as "מה משתבש
  אם…") and from each part's "תשובה בקצרה"? About 40 follow-ups lean on the page's context
  ("לפי ההוכחה"): skip them with a flag, or reword them?
- Status: not started.

### Round 14. My area

- **14.1 "האזור שלי".** Progress is scattered over the level bands, the path rows, my map
  and a filter; nothing is by kind or by weakness, and a series left in the middle is shown
  nowhere. Sketch: `me/` with bars per kind and per path (HTML with a text value beside each
  bar), "לחזור אליהן" (over target, many hints, low confidence, from the records of 12.1),
  the starred questions, the series in progress, today's review count, my map in full. M.
- **14.2 A home page that knows a returning reader.** With 20 solved, the continue card
  starts at y = 907 of a 900 px screen and at 1841 px on a phone, behind a 1581 px hero; the
  hero's button sends everyone to the first unsolved id in student order (a junior reader
  got a student question). Sketch: an inline script in `<head>` marks a reader with state
  before the first paint, and CSS swaps the pitch for a personal strip the hook already
  wrote (continue, series k of n, review count, next in my path), so nothing moves; the
  button picks the next unsolved of the reader's own path or level. M. Checks: a new
  `check_state.py` (seed the state, load the home page, the lists, `me/` and a question at
  390 and 1440 px, assert the strip, the counts and no layout shift): no browser check
  loads a page with personal state today.
- **14.3 Progress on another device.** The FAQ states the limit ("במכשיר אחר או בדפדפן אחר
  הם לא יופיעו"), and a phone browser can evict the storage after a week without a visit.
  Sketch: export and import of one small JSON; a transfer link that holds the solved and
  starred marks as a bitmap in the address (115 questions in about 40 characters), with a
  confirmation before it writes. S to M.
- **14.4 A plan to the interview date.** The first-visit journey stalls on "what do I do in
  two weeks": the home page offers a start, a random question, an interview, 13 paths and
  115 rows. Sketch: "ראיון ב-10 בדצמבר, 5 שעות בשבוע, ג'וניור" becomes weeks of questions
  built from the paths (core paths first, about twice the target minutes per question); it
  is recomputed from the marks, so it is never "behind", only re-flowed; "הוסיפו ליומן"
  downloads an `.ics` file. No notifications: push needs a server. M. Checks: the scheduler
  under Node (the date passed, zero hours, everything solved), the fields in
  `check_inputs.py`.
- Open questions: is the returning home a different first screen, or the same hero with the
  strip above it? Which paths are "core" for a junior interview (the plan's order is that
  judgment)? Is the transfer link enough, or is a QR code worth a vendored script?
- Status: not started.

### Round 15. Techniques

- **15.1 Hebrew labels and a one-line definition per concept.** `graph_concepts.json` has
  158 concepts in 7 groups, in English. Sketch: a label and an optional two-sentence primer
  each, lint-warned when missing; this is also the glossary earlier rounds asked for. M
  (content).
- **15.2 Related questions that are related.** The related list is by shared tags and comes
  out as id neighbours: 0061 (a sliding window) shows 0060, 0062 and 0059 and not its
  sibling 0063, although the concept file says of 0063 "the same variable window with a
  left end that only moves forward". Sketch: `_related()` ranks by shared core concepts,
  explicit relations first, and prints the reason in Hebrew. S after 15.1.
- **15.3 A page per technique.** "כל השאלות שנפתרות עם אינווריאנטה" (27), "XOR" (10),
  "Scoreboard" (13): a `techniques/` index by the 7 groups and a page per concept with its
  primer and its questions from easy to hard; a "טכניקות" line in the end card of a
  question. Never above the solution: a technique's name is a hint. M.
- **15.4 The map inside the site.** `graph.html` has its own purple-black palette, no site
  header and an English panel. Sketch: `tools/build/graph.py` swaps the palette for the
  site's variables, adds the header bar and follows the light and dark toggle. M.
- Open questions: may a question show its techniques before a solution is opened, or only
  after (recommended: after)? Technique names as a filter in the tables too? The map as its
  own page, or as a second view of the tags page?
- Status: not started.

### Round 16. Boxes that ask

- **16.1 Missions.** Every box is titled "נסו בעצמכם" and its help is a paragraph (a median
  of 339 characters). 0112's box opens on the page's bug and never asks the reader to fix
  it; 0113's opens with the answer stated. Sketch: a kind registers `missions: [{ text,
  start, goal(state), solution }]`; the shell shows the mission in the title's place with
  previous and next, evaluates the goal after each change and ticks it with the answer
  line's pulse ("גרמו שרק agt1 יקבל ErrDriver", "העבירו את הטסט עם ה-drain הקטן ביותר"). M.
  Pilot: `factory` (0112), `objrun` (0113), `seqarb` (0114), then `credits` (0024) and
  `fifo` (0033). Checks: per mission under Node, `goal(start)` is false and
  `goal(solution)` true; `check_explorers.py` applies each solution and expects the tick.
- **16.2 "הראו את זה בתיבה".** No page links into a box state, and traps describe box
  settings in prose (0115: "swap the fork order and Verilator sees 0 errors"). Sketch: a
  link in the text sets the box to exactly that case in place (opens the folds, scrolls,
  focuses); authors copy the payload from the box's own "copy link". S. Pilot: 0115's three
  traps, 0112, 0016. Checks: `check_explorers.py` clicks every such link and compares the
  box's own link with it, so a stale payload fails.
- **16.3 One stepping convention.** On 0016 the step figure has ← as next, counts from "1 of
  21" and advances on space; the box two screens below has → as next, counts from "0 of 19"
  and plays on space. 14 boxes with a playback bar have no play button, the three newest
  among them. Sketch: the stepper adopts the playback bar's markup and keys, and keeps its
  swipe. S. Checks: the stepper's direction in `check_keyboard.py`.
- **16.4 The step lights its line of code, on the DV boxes.** The steps-and-code panel
  supports both languages and reads the page's own code, and only 0061 to 0070 use it.
  0115's regions card names "the DUT's `always_ff`" in words while the code sits elsewhere.
  Sketch: `edgerace`, `objrun`, `factory` and `rtlbug` call it with the lines of each step.
  S per kind. Checks: the box test asserts the lit lines hold an expected token, since line
  numbers drift.
- Open questions: should a completed mission count anywhere (the part's circle, my map),
  or stay private to the box? Which direction is "next" on a right-to-left page: the media
  bar's (→) or the reading order (←)?
- Status: not started.

### Round 17. A box on one screen

- **17.1 Focus mode, and a playback bar that stays.** On a phone only 32 of the 208 boxes
  fit one 844 px screen (the median is 1188 px): on 0016 and 0115 three presses of "next"
  change only the step counter in view. On a laptop a box inside a solution is about 555 px
  wide inside and the two-column rule needs 600, so at 1280 to 1536 px only 4 of the 125
  boxes that declare columns get them; `check_heights.py` looks only at 1920 x 1080.
  Sketch: on a phone the playback row is sticky at the bottom of its box; a "focus" button
  in the header opens the box over the page (a placeholder keeps its room; Esc and Back
  close it), where the container rule gives two columns on every laptop with no work per
  kind. M. Checks: a 1366 x 768 focus pass in `check_jumps.py` and `check_heights.py`, Esc
  and the focus return in `check_keyboard.py`. This is a different matter from the three
  tall boxes of the cancelled list.
- **17.2 Predict, then reveal.** Summaries state the answer at step 0 (0016: "the survivor
  is 8"; 0115: "6 errors in cycles 2, 3, 5, 7, 8, 10"), and three kinds (`pcie`, `mice`,
  `tagcheck`) each built a guess mode of their own. Sketch: an optional toggle in the
  header covers the values the next step will change, and the verdict, with "?" until a
  tap; the shell already finds the values a redraw changed, so no code per kind. Off by
  default and zero height when off, which is the lesson of the removed self-checks. M.
  Pilot: `seqarb`, `edgerace`, `josephus`, and the `pcie` ladder moved onto it.
- **17.3 Pin and compare.** 149 boxes have a select whose point is a comparison (blocking
  against nonblocking, FIFO against STRICT_FIFO), and a change replaces the picture.
  Sketch: a header button freezes the current figure as "לפני" beside the live one in
  focus mode, or under it on a phone; one snapshot at most (it doubles the figure's
  elements). M.
- **17.4 A chart that fits.** 31 boxes have a part that scrolls sideways at 1440 px; in
  0066 the chart is 45 px too wide and hides the page's last interval. S to M, per kind.
- Open questions: a focus mode, or only a lower two-column threshold (cheaper, tighter
  columns)? Should interview mode switch the page's boxes to predict mode?
- Status: not started.

### Round 18. Practice by writing

- **18.1 "הפתרון שלי" in the run panel.** The panel sits after the solutions with their
  functions already loaded, and a typed edit is lost on reload. Sketch: a second mode
  passes the reader's text as the solution and the page's unchanged `demo.py` as the code;
  the existing check of `print()` comments then gives a mark per example with no new
  checker; the hook derives a stub per part (signature, docstring, `pass`); drafts are kept
  per question with a "start over" line. M. Pilot: 0066, 0016, 0062. Checks: the stub
  parses, and the reference as the "solution" passes every check.
- **18.2 "להרוג את המוטנטים": the reader writes the tests.** The verification skill itself,
  and no preparation site has it: the page ships four or five subtly wrong versions of its
  function, the reader types test inputs and sees which mutants the tests killed and which
  survived. Sketch: `tests/<id>/mutants.py` with a one-line Hebrew description each (shown
  for a survivor on request); a third mode of the panel. M to L. Pilot: 0066 (`<=` against
  `<` on touching intervals, a missing sort), 0016, 0050. Checks: every mutant differs from
  the reference on some input and is killed by the page's own tests.
- **18.3 Draw the output waveform.** A timing strip already supports clickable cells, and
  only inputs are editable; on 0110 the expected lane is drawn for the reader from the
  start. Sketch: the output lane starts empty, the reader toggles its cells, "check" marks
  each cycle against the model. M. Pilot: `rtlbug` (0110), `edge` (0001), `seqdet` (0040).
  The cells need 44 px on touch, so the mode needs a wider slot.
- **18.4 The simulator's real transcript.** The SystemVerilog tab's button reads "להרצה
  (גרסת ה-Python)", and the 15 UVM pages have no run panel. SystemVerilog in the browser is
  not feasible for these pages (Verilator needs a C++ compiler; the WebAssembly builds of
  other tools do not run class-based testbenches, and would show results the CI never
  verified). Sketch: a recorded `tb.log` per question that the tests fail on when the real
  run differs, shown folded under the tab with the simulator's version; then a log viewer
  for debug questions (filters by severity, component and time; the reader clicks the line
  that is the cause). M. Pilot: 0115, 0113, 0111.
- Open questions: the practice editor near the statement too, or only at the page's end?
  Mutants as a tab of the panel, or as a new kind of part on the DV pages? Is a recorded
  transcript worth showing, or is "tested in Verilator" enough?
- Status: not started.

### Round 19. New kinds of questions

- **19.1 "שאלות בזק": concept decks with a tested "what prints?".** The two-minute
  SystemVerilog or UVM concept question as tap-to-reveal cards: a snippet of at most 12
  lines, a spoken answer of three lines, and "what the interviewer asks next". Sketch: a
  new page family `docs/decks/<topic>.md`, 10 to 15 cards each; a linter rule for a card;
  `tests/decks/` runs every snippet on Verilator or Python and compares the output with its
  `prints:` comment; a deck row in the lists and paths. M for the mechanism, M per deck.
  First decks: processes and `fork`, classes and copying, randomization, interfaces and
  `modport`, mailboxes and semaphores. Limit: Verilator is two-state, so cards about X and
  Z cannot be executed and are left out.
- **19.2 From a spec to a verification plan, scored by the bugs it lets through.** The
  senior question "here is a block, how would you verify it?" with an objective answer.
  "Testplan" and "תוכנית אימות" appear on no page. Sketch: half a page of spec; part א what
  to check and how (feature, stimulus, checker), part ב coverage and when to stop, part ג
  eight DUTs with a bug each: which rows of the plan catch which. The matrix comes from
  running the page's testbench on `ifdef` mutants (the precedent is 0111's
  `tests/0111/matrix.py`), and a box lets the reader switch plan rows off and see which
  mutants escape. `kind: dv`, the standard skeleton. L for the first, M after.
- **19.3 Debug with staged evidence: "מה בודקים קודם?".** Every debug page puts all the
  evidence in the statement and asks for the bug; choosing what to look at next is never
  practised. Sketch: an `evidence` fold counted in interview mode like a hint ("הלוג של שש
  השגיאות", "אותה ריצה כשה-driver ראשון ב-fork : 0 שגיאות"), each holding a block
  generated from a real run. S to M for the mechanism, L per new question. Pilot: 0115
  re-staged (its evidence exists).
- **19.4 Four areas the site does not touch.** Timing arithmetic (setup, hold, fmax, skew:
  the `timing` tag is defined and used by no page), with a slack box; regression triage in
  Python (bucket failures by signature, find the first failing seed: the `scripting` tag is
  unused, and it fits the run panel); bisecting a flaky failure (1 in 5 runs, 64 commits,
  95% confidence), next to 0039 and 0041; cache index and tag arithmetic or pipeline
  forwarding (the tags exist and are unused). Each is a question by the `dv-question`
  skill. L each.
- Open questions: decks as a separate family (recommended), or a sixth kind inside
  `docs/questions`? The first block of 19.2: a FIFO (continues 0033 and 0034) or a small
  register block with RO and W1C fields? Is a Python-only page acceptable for the triage
  question?
- Status: not started.

### Round 20. Explanations

- **20.1 "פתרון ראשון": the brute force before the idea.** Interview mode's own summary
  advises "תנו קודם תשובה חלקית שעובדת, ואחר כך שפרו אותה", and of the 41 code pages the
  naive approach is in the idea block of 4 and nowhere on 27; 0061 files the natural first
  attempt under traps. Sketch: an optional `#### פתרון ראשון { .sol-first }` before the
  idea: three to six lines, its cost, and the waste the idea removes; a chip in the
  solution map. S for the mechanism, M for about 15 pages.
- **20.2 "מספיק לראיון".** The authoring budget is 20, 40 or 60 minutes of study and the
  interview target 10, 15 or 25. In 0033 (easy) steps 1 to 4 are the interview answer and
  the two-sided bound and part ב's formula are beyond it, and nothing says so. Sketch: a
  rail labelled "מעבר לראיון" on the marked paragraphs (a label, not a fold: depth is the
  site's identity). S for the mechanism, M to L for the pass (the 17 easy pages first).
- **20.3 The interviewer block, rewritten where it leaks.** The authoring half of 12.2, if
  round 12 was not taken.
- **20.4 A picture on the DV pages that have none.** 0115 (the sampling race) has no static
  figure: the scheduler's regions exist only as a table inside the box. 0111 has no
  testbench diagram, though its three bugs are places in a testbench. 0025 has only
  Mermaid. Sketch: for 0115 "region lanes", one clock edge unrolled into its regions with
  the driver, the DUT and the monitor placed where each reads or writes and the racing pair
  joined by a bracket, before and after the fix; for 0111 the testbench diagram of 0049
  with three numbered pins; for 0025 a lifeline chart with the Retry Buffer as a queue. M.
- **20.5 Steps that light the figure and the code.** `steps-fig` is on four pages, and on
  0055 the lit step turns every arc amber, so the legend under it (bit 0 blue, bit 1
  orange) no longer matches. Sketch: block diagrams, cell rows and bars get step keys from
  the generators; a step may also light code lines (`L12-14`) in the editor window; the lit
  part keeps its hue with a heavier stroke and the rest dims. No new elements and no motion
  at load. M. First: 0049, 0112, 0114, 0040 part ב, 0055 part ג.
- Open questions: "beyond the interview" as a label or as a fold? In 0115, do the lanes
  replace the table inside the box or come before it?
- Status: not started.

### Round 21. Figure craft

- **21.1 A figure style guide, enforced by the generators.** None of the 379 static figures
  has a caption or a number (only stepper frames do). Arrowheads are dark grey on blue or
  orange arcs; on 0040 state sub-labels are run over by arcs; the same testbench diagram is
  drawn at two label scales (0049 and 0114); legends sit above charts and below diagrams.
  Sketch: a "Figure style" section in `CONTRIBUTING.md` and defaults in `charts.py` (one
  label size per figure type, arrowheads in their line's colour, the legend under the
  figure). M.
- **21.2 Captions and numbers.** An optional caption per figure, numbered by a CSS counter
  ("איור 3"), so the numbers cost no elements and a caption one. S after 21.1.
- **21.3 Waveforms drawn by the site (phase B of 11.1).** `tools/figures/wave.py` renders a
  `wavedrom` fence at build time into the timing strip's drawing, and the 11 Mermaid
  diagrams are redrawn with the generators. It removes both libraries from those pages and
  about 1,000 elements per page (on 0110, 2,106 of its 4,986 elements are WaveDrom's). M to
  L. The wave viewer reads WaveDrom's geometry and needs its tests.
- **21.4 Stepper frames that move.** The 164 stepper frames swap whole figures. Sketch: the
  person who leaves the circle, the packet that enters the buffer, the credit that moves is
  seen moving: marks keep a key across frames and the stepper plays the difference
  (transforms only, 300 ms, on a user's step only, instant under reduced motion). S to M.
- **21.5 A lint for collisions.** No figure text may cross a path of another group. S.
- **21.6 One frame fewer inside an open solution** (the reviewer's lowest, and subjective):
  at 1440 px an open solution shows three vertical rules before a figure adds a fourth.
- Open questions: captions on every figure, or only where the prose refers to one? Do the
  rails of an open solution read as structure (keep) or as clutter?
- The owner's answers (2026-11-21): captions only where the prose refers to a figure; 21.3
  is skipped when 11.1 is enough; 21.4 as a pilot on three questions; 21.6 dropped.
- Status: not started.

### Round 22. Paths with a finish line

- **22.1 A path looks like its line.** The 13 line colours live only on the map: a path
  page is a plain title and a grey bar, and thirteen path icons are drawn and appear on no
  built page. Sketch: a band on the path page with its icon and colour, used for the step
  numbers and for the edge of the path strip on its questions. M. Checks: 13 colours in 2
  schemes on the new grounds in `check_contrast.py`.
- **22.2 A finish card.** After all 10 questions of "סביבת אימות" the path page shows a
  green bar, and the end card of the last question is one sentence. Sketch: a card in the
  built page, hidden until every id is solved: the path's icon, "סיימת את המסלול · 10/10",
  its difficulty mix and the next path; a filled terminus on the metro map. S.
- **22.3 The home page's compact map.** About 650 px tall at 1440 px, more than half of it
  empty ground with one vertical line, and two screens on a phone. Sketch: the six featured
  lines as horizontal rows, about 320 px. S.
- Open questions: who picks the "next path": a `next:` key in each path file, or the map's
  order?
- The owner's answer (2026-11-21): a `next:` key, in one ring: logic design, clock
  crossing, protocols, testbench, constraints, coding, advanced algorithms, digits,
  probability, logic puzzles, optimization puzzles, geometry and motion, the cake, and back
  to logic design; a finished next path is skipped to the next unfinished one.
- Status: not started.

### Round 23. Take it with you

- **23.1 An offline pack.** The service worker keeps only pages already opened and shows
  nothing about which; it is network-first with no timeout, so on a weak connection a saved
  page waits for the network to fail; the font hosts are not cached. The FAQ recommends it
  "בדרך לראיון". Sketch: "לשמור את המסלול לקריאה בלי רשת" on a path page (about 2.6 MB for
  a path of nine; everything is about 40 MB), a mark on saved rows, a three-second race
  before the saved copy, an offline line in the header. M. Checks: one opt-in browser test
  that allows the worker, saves a path, goes offline and opens its pages.
- **23.2 A designed print sheet.** Print today is the screen on paper: 0040 is 21 A4 pages,
  with the grey ground, the interface chips and an orphaned tab label, and no page numbers.
  Sketch: A4 margins and a footer (the site, the id, the page number), a white ground at
  full width, both code tabs printed with their labels, figures kept whole; two entries,
  "הדפסת השאלה" (the statement only, for a mock interview on paper) and "הדפסה עם פתרון".
  S to M. Checks: a page-count smoke test.
- **23.3 An interviewer's sheet, for practice in pairs.** Mock interviews with a friend are
  how candidates really practise. Sketch: a view of a question for the friend who plays the
  interviewer (the statement, what to check, the hints in the order to give them, the
  follow-ups with their answers, the traps; solutions folded), and a pack of a series or a
  path as one printable document. M.
- **23.4 Share.** There is no share control anywhere. Sketch: a share tool on the question
  and on the end card (the share sheet, with a clipboard fallback and the existing toast).
  S.
- **23.5 A feed.** `new/` is a page only. Sketch: the hook writes `feed.xml` from the
  questions by date added. S.
- **23.6 English one-liners.** Titles and descriptions are Hebrew only and the English name
  lives only in the address, while engineers search these topics in English. Sketch: a
  `title_en` per question, drafted from the addresses for the owner to review, in the
  structured data, in the search words of 11.2 and as a small line under the title. A full
  English edition is not recommended: it would double every future change. S to M.
- **23.7 Social cards that show the question.** The card is the same navy layout for every
  page. Sketch: the question's own chip and a difficulty-coloured edge. S.
- **23.8 Trust and feedback.** The only feedback path is "edit on GitHub" (the raw Markdown
  editor); `.github/` has no issue templates; the public repository has no licence file, so
  an outside writer cannot know the terms; there is no about or privacy page. Sketch:
  "מצאתם טעות?" and "להציע שאלה" on every question, opening an issue already filled with
  the question's id and address; an "על האתר" page (who writes it, how the code is tested,
  what is stored in the browser); a licence; a 40-line "your first question" section at the
  top of `CONTRIBUTING.md`. S.
- Open questions: "save everything" offline, or a path at a time? Is the question-only
  print sheet wanted? The English line visible on the page, or metadata only? Which licence
  for the Hebrew content (for example CC BY-NC-SA for the text and MIT for the code)?
- Status: not started.

## Considered and not recommended

- **SystemVerilog running in the browser.** Not feasible for the pages' class-based
  testbenches, and it would show results the CI never verified (18.4 is the alternative).
- **Notifications and reminders.** Web push needs a server; the calendar file of 14.4 asks
  no permission and works on every phone.
- **Streaks, "you missed a day", points.** Against the site's quiet tone; the review queue
  of round 13 has a cap and no debt.
- **Typed self-check fields on the page.** Removed by the owner on 2026-11-02; every
  proposal here is tap-to-reveal, a tick box, or inside a box or the run panel.
- **A full English edition.** 115 long pages, Hebrew figure legends and the strings of 208
  boxes; 23.6 gets most of the search value for about a day of work.
- **Charts that draw themselves in on scroll, more celebration on "solved", more
  page-to-page effects.** Decoration that fights the steady-figure rules; the pulse, the
  confetti and the view transition are enough. The motion that teaches is 21.4 and 20.5.
- **Low power, formal, emulation and gate-level flows as question areas.** Tool-bound,
  untestable in this CI, and rare for the student and junior audience. Behavioural
  questions were put to the owner before with no recorded answer and stay a question.
