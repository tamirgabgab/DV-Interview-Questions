---
name: dv-question
description: Turn a conversation or write-up the owner pastes (an interview question and its solution, in any form - chat log, notes, a document, code) into a finished question page of this site, through the whole process - check the source's math and code, choose level, difficulty and kind, scaffold, write the Hebrew page (interviewer block, hints, short answer, idea, steps, Python and SystemVerilog code, proof, cost, traps, follow-ups), figures, an interactive box when it helps, tests, study path and map, the checks, commit and CI. Use when the owner sends a question with a solution and asks for a question, a page, "תעלה את זה כשאלה", "תהפוך את ההתכתבות לשאלה", or invokes /dv-question.
---

# dv-question: from a conversation to a question page

The owner pastes material about one interview question: a chat, a solution write-up, code,
tables, a photo of a whiteboard. This skill turns it into a page that a candidate can study
in the time the level allows, and that the site's tests and checks accept.

The repository's own documents are the authority: `CLAUDE.md`, `CONTRIBUTING.md`
("Question format", "Adding a new question", "Tests", the figures and boxes sections) and
`tools/authoring/question.md`. Where this file and those differ, they win, and this file is
updated. Read `notes/HANDOFF.md` (open items, recent work) before starting, as every session
does.

The owner is spoken to in Hebrew, RTL-safe (see `CLAUDE.md`). The page is Hebrew; code,
comments, commit messages and notes are English.

## Phase 1 - Understand the material

1. Extract from the paste: the question as asked, every part (סעיף), the expected answer of
   each, the code (which language, whose: the owner's own code is kept as sent, comments may
   be added, bugs are reported to the owner and not silently fixed), every number, table,
   formula and example, and anything the interviewer was after.
2. Look for a near-duplicate: search `notes/CATALOG.md` and `docs/questions/` for the topic
   (`grep -ril "<keyword>" docs/questions`). If one exists, tell the owner and ask whether
   this is a new question, a new part of the old one, or a variant to mention in a follow-up.
3. Note what is missing: an unstated assumption, a part without a solution, a claim without
   a proof. These become questions for the owner (phase 3) or work for phase 2.

## Phase 2 - Check the source before writing (mandatory)

Never write a page on top of an unchecked answer. In a scratch script (later the question's
test, `tests/<id>/test_<id>.py`):

- Recompute every table, example and closed form with exact arithmetic (`fractions.Fraction`,
  integers, `math.comb`), and compare each closed form with a brute force over small inputs.
- Try the edge cases of every general formula: 0, 1, the smallest and the largest legal
  input, equal values, an empty input, the case where a bound is reached exactly (0026 to
  0028 found a capped last person and one rounding this way).
- Run the given code: Python with pytest, SystemVerilog on Verilator (`tools/checks/run_tests.py`
  shows how), on the examples and on random inputs against a reference.
- For a proof, check each step; find the invariant, the induction or the exchange argument,
  and say which one the page will use.

Report to the owner, in Hebrew, what holds and what does not, with the counterexample, before
writing the page. A wrong answer is corrected on the page only with the owner's agreement.

## Phase 3 - Classify and plan, then one round of questions

Propose, from `CONTRIBUTING.md` "How questions are organized":

- **Level** (student, junior, senior) and **difficulty** relative to the level (easy,
  medium, hard).
- **Kind** (puzzle, code, design, math, dv) and **tags**, reusing existing tags.
- **Time budget** (the owner's rule, 2026-11-20): easy 20 minutes, medium 40, hard 60. That
  sets the size: easy has one part, medium up to two, hard up to three; less code, and a
  secondary part is cut or moved to a follow-up rather than kept.
- **Element budget** (the owner's rule, 2026-11-20): the built page stays under 8,000
  elements once loaded; `check_phone.py` warns over 8,000 and fails over 12,000. Plan for it
  from the start, since the heavy part is the math: a formula is about fifteen elements, a
  fraction or a subscript twenty to thirty. Keep the parameters small (a table of 10 to 16
  rows, not 40; a chart to 40 or 60, not 200; examples by hand of 5 to 20 people, cells or
  bits), give a proof's check two or three examples, and see phase 5 for the writing.
- **Slug** (lower-case English words joined by hyphens) and the **Hebrew title** (a title
  with " – " shows the rest as a subtitle).
- **Code:** Python and SystemVerilog as linked tabs, Python first; pure RTL design may be
  SystemVerilog only; a UVM or cocotb question runs on the cocotb/pyuvm bench
  (`tools/page_tests.py run_cocotb`).
- **Proof:** a `sol-proof` block whenever the answer is a claim (optimality, a bound, a
  probability, correctness of an algorithm); a `sol-cost` block with cost chips for an
  algorithm.
- **Figures and a box:** which figure explains the idea (a state machine, a timeline, a
  waveform, a grid, a tree), and whether an interactive box helps: a simulation for dv and
  design questions (the owner asked for one per question in round 6), a step-through for an
  algorithm, a slider for a formula. Name the box's kind and what it shows.
- **Study path** (a file in `docs/paths/`) and where in it.

Ask the owner once, with `AskUserQuestion`, only what the material does not settle: the
findings of phase 2 that change the answer, the level and difficulty if unclear, whether a
box is wanted, and whether to stop at the branch or go on to `main` after the CI. Put the
recommended option first. When the owner said to just do it, take the recommendations and
say so in the summary.

## Phase 4 - Scaffold

```bash
python tools/authoring/new_question.py --level <level> --difficulty <d> --kind <kind> \
  --slug <slug> --title "<Hebrew title>" --tags a,b [--figures] [--code]
```

It takes the next free id, writes `docs/questions/<level>/<id>-<slug>.md` from the template,
`tests/<id>/`, a generator stub `tools/figures/q<id>.py` (`--figures`), `tb.sv` and `demo.py`
(`--code`), and the catalog row.

## Phase 5 - Write the page

Follow the skeleton exactly (the linter enforces it): the question, one
`??? interviewer "מה המראיין בודק"` block that does not reveal the answer, then per part a
hint ladder (`??? tip "רמז 1"`, `"רמז 2"`, from a nudge to almost the idea) and
`??? success "פתרון סעיף א"` that opens with `!!! answer "תשובה בקצרה"` (one or two
sentences), then only the blocks that apply, in this order: `#### הרעיון { .sol-idea }`,
`#### השלבים { .sol-steps }`, `#### הקוד { .sol-code }`, `#### למה זה נכון { .sol-proof }`,
`#### סיבוכיות { .sol-cost }`. At the end, `## נקודות חשובות ושאלות המשך` with
`??? trap "מלכודת: ..."` items and a `??? followup` list, each follow-up with its collapsed
`??? fu-answer "תשובה"` (8 spaces, the answer at 12).

What makes the page good to study, not only valid:

- **The question** is a scene an interviewer would set: concrete numbers, a small example
  the reader can work by hand, the constraints stated once.
- **The idea** comes before any code: the one observation that cracks the problem, with the
  intuition (why someone would think of it), in a few sentences.
- **The steps** are a short ordered timeline (`<div class="steps" markdown>`); when a figure
  shows the walk, put them beside it with `steps-fig` and `data-fig-steps` (0055, 0040).
- **The code** is short and readable: `title=`, `linenums="1"` on long blocks, `hl_lines=`
  on the key lines, annotation markers (`# (1)!`, `// (1)!`) with a numbered Hebrew list
  after the block. Markers are the only decoration on code lines. A `print()` line's comment
  is its expected value (the run panel checks it).
- **The proof** is rigorous and short: name the method (invariant, induction, exchange,
  counting both ways, a bijection), state the claim, prove it, and close the edge cases.
  Display math is split with `aligned` so it fits a phone.
- **The cost** line: `<!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->` under the answer.
- **Traps** are the wrong answers candidates really give, each with why it fails (a
  counterexample is best). **Follow-ups** are what the interviewer asks next, with short
  answers.

Writing to the element budget (`CONTRIBUTING.md`, the weight paragraph of the phone check):

- A single letter or a plain number that reads well as text stays text: "1, 2, 4, 8", a
  digit string in a table cell, a list of zero points. Math is for expressions.
- A table column of computed values holds the numbers, and the formula appears once, in
  the column's header or in the sentence before the table, not as `\( \tfrac{3}{2} \cdot 4 = 6 \)`
  in every row.
- A display formula that only repeats the previous line, or a chain `a = b = \cdots = c`
  whose middle the reader does not need, is shortened to its two ends.
- A stepper's later frames are templates and cost nothing; a chart draws one line per
  straight run, not one per step.

RTL and typography rules that the checks enforce (all of them are in `CLAUDE.md`):

- Every paragraph, heading, list item and table cell starts with a Hebrew word; a line that
  must start with Latin text, code, a number with a period or math gets RLM (U+200F) first.
- A Hebrew colon has a no-break space (U+00A0) before it and a space after.
- No Hebrew inside MathJax; no math in headings (write it in words, keep the anchor with
  `{ #id }`).
- Ordered numbers in Hebrew text (bits, rows, tuples) go in `<span dir="ltr">`, or are
  written without spaces, or in math or code.

## Phase 6 - Figures

The generator `tools/figures/q<id>.py` defines `blocks()`, uses `tools/figures/charts.py`, and
takes colours only from the CSS variables of `docs/stylesheets/` (the palette in
`01-base.css`). Its blocks sit between `<!-- gen n -->` markers; write them with
`python tools/figures/fill.py <id>`. Hebrew SVG `<text>` gets `direction="rtl"`; prefer an HTML
legend. Labels stay at 9 px or more at 390 px.

## Phase 7 - The box (when planned)

Follow the most recent box of a similar question (0112 `factory`, 0113 `objrun`, 0114
`seqarb`, 0115 `edgerace`; for algorithms 0064 `weights`, 0066 `intervals`) and the explorer
sections of `CONTRIBUTING.md`:

- `docs/javascripts/explorer/<kind>.js`, registered with `dvqExplorers.register({views, help,
  cols, models})`, the shared code in `core.js`; `cols` lays the box in columns on a wide
  screen.
- Its stylesheet `docs/stylesheets/questions/<id>-<kind>.css`, listed in `extra_css` of
  `mkdocs.yml` after the previous question's; colours from variables only.
- A Node test of the model against the Python reference (`tests/<id>/test_<id>_box.py`).
- New colour pairs (a text or a mark on a fill) in `PAIRS` of `tools/checks/check_contrast.py`.
- The kind added to the list of kinds in `CONTRIBUTING.md`.
- The box is at most about 1000 px tall at 1920 x 1080 (`check_heights.py`), its figures do
  not move while it steps (`check_jumps.py`, `data-steady`), and nothing moves while the page
  loads.

## Phase 8 - Tests

`tests/<id>/test_<id>.py` runs the page's code as published (`tools/extract_code.py`,
`tools/page_tests.py`): every number, table and example on the page is checked against an
exact computation, the code against a reference on random inputs, the SystemVerilog on
Verilator through `tb.sv`, the figures with `assert_figures_match(<id>)`, and the step keys
with `fig_steps` / `lit`. `tests/<id>/demo.py` is the run panel's starting script, every
printed result with its expected value in the comment. A long environment moves to
`tests/<id>/env.py` / `env.sv` and the tests insert the page's blocks into it.

## Phase 9 - Wire it into the site

- The question into a study path: a `{id, note}` step in `docs/paths/<path>.md` (the note one
  quoted Hebrew sentence).
- Its concepts into `tools/build/graph_concepts.json`, then `python tools/build/graph.py`.
- `python tools/build/catalog.py` after a title or level change.

## Phase 10 - Checks

Run, on the new page (`--only <id>` where the tool takes it), the checks of `CLAUDE.md`:
`lint_pages.py <id>`, `run_tests.py <id>`, `mkdocs build --strict`, `check_links.py`,
`check_phone.py --touch --local-cdn --only <id>` (and `--scheme dark`), `check_explorers.py`,
`check_jumps.py`, `check_inputs.py`, `check_keyboard.py`, `check_heights.py`, and
`check_contrast.py` when colours were added. In the cloud sandbox pass
`--browser <the pinned Chromium>` and `--local-cdn`.

Read the element count on the page's line of the phone check: over 8,000, cut before the
commit (phase 5's list); over 12,000 the CI fails.

Then look at the page yourself (the `webapp-testing` skill's notes in
`.claude/skills/README.md`): screenshots at 390 px and 1920 x 1080, light and dark, of the
question, an opened solution, the figures and the box. Check the RTL of every line with
numbers, the display math, and the indentation inside lists and admonitions.

## Phase 11 - Commit, CI, publish

- Commit on the session's work branch: `Add question <id>: <English title>` with a short
  body (what was checked, what the box shows).
- Push, wait for the branch CI (use a scheduled check, not a polling loop), fix what fails.
- A new question is not a small fix: `main` is fast-forwarded to the branch only after the
  branch CI is green and the owner said so.
- Add a work-log entry to `notes/HANDOFF.md` (and `notes/ROUNDS.md` if the question belongs
  to a round).

## Phase 12 - Report to the owner

In Hebrew, short, by sections: what phase 2 found (and what was changed with the owner's
agreement), the level, difficulty and time budget chosen, what the page has (parts, code,
proof, figures, box), the checks and the CI, and what is left (main, the video, a follow-up
question).
