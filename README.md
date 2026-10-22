# DV Interview Questions

A curated, searchable collection of **Design Verification (DV)** job interview questions —
plus math and logic questions that often come up in the same interviews. Each question has
a clearly written statement and a full, readable solution, including diagrams, waveforms,
formulas and code where they help.

The content is written in **Hebrew** and published as a public website (MkDocs Material,
right-to-left layout, own navy + amber palette and logo) with filtering by **position
level**, **difficulty** and **topic**.

**Live site:** <https://tamirgabgab.github.io/DV-Interview-Questions/>

> **Status:** the site is live and holds 38 questions (see the catalog below).
> [`HANDOFF.md`](HANDOFF.md) has the work log, open tasks and the proposed rounds of
> improvements (interface, explorers per question, new puzzle and DV-core questions, tooling).

---

## Catalog

| Id | Question (Hebrew title on the site) | Level | Difficulty | Main topics |
|----|-------------------------------------|-------|------------|-------------|
| 0001 | Rising edge detector; a timing-strip explorer (draw sig, pick the edge, the reset trap) | student | 🟢 easy | digital logic, SystemVerilog, WaveDrom |
| 0002 | Swap two variables (temp / arithmetic / XOR) | student | 🟢 easy | bitwise, math proofs; a line-by-line tracer with the symbolic values, and the three-variable XOR rotation of the follow-up |
| 0003 | What does this code do? (double-loop sort) | student | 🟢 easy | algorithms, sorting; a comparison-by-comparison tracer with the invariant |
| 0004 | Three mislabeled boxes | junior | 🟡 medium | logic puzzle, algorithms |
| 0005 | Smallest multiple made of digits 0 and 1 | junior | 🟡 medium | BFS, math, performance chart |
| 0006 | Stock max profit, long or short; a scan explorer with draggable prices | junior | 🟡 medium | algorithms, O(n²) vs. O(n) |
| 0007 | Random triangle on the unit circle containing the center; then a polygon with n vertices (an array of n angles); the continuous and the discrete probabilities | senior | 🟡 medium | SV constraints, probability |
| 0008 | Eurovision 2026: when was it certain Israel would not win? | junior | 🟡 medium | pigeonhole, O(k) scan, "cups" chart |
| 0009 | 16 people, 16 boxes and a helper (100 prisoners variant) | junior | 🟡 medium | permutation cycles, API with limits, cycle diagrams |
| 0010 | Valid parentheses (LeetCode 20) | student | 🟢 easy | stack, O(n²) vs. O(n), log-scale chart |
| 0011 | Random final board of tic-tac-toe, plus wrap-around diagonals | senior | 🟡 medium | SV constraints, solve-before, Steiner system S(2,3,9) |
| 0012 | Sort the digits and subtract (3-digit Kaprekar routine) | student | 🟢 easy | digits, 3-element sorting network, proof (0 and 495) |
| 0013 | Sort the digits and subtract, four digits (Kaprekar's constant) | junior | 🟡 medium | 4-element sorting network, column subtraction, case analysis (0 and 6174) |
| 0014 | Random non-overlapping squares, then rectangles, on a grid of points | junior | 🟡 medium | SV constraints on dynamic arrays, pairwise no-overlap, constraint override, the cross trap |
| 0015 | Two children, at least one boy (boy or girl paradox, the Tuesday boy) | student | 🟢 easy | conditional probability, inclusion-exclusion, Bayes, general formula, outcome grids (no code) |
| 0016 | The Josephus problem, every second person leaves (N = 20, then a formula) | junior | 🟡 medium | round-by-round simulation, recurrence by relabelling, zero points at powers of 2, F = 2r by induction, binary view, step-through circle (no code) |
| 0017 | Find the duplicate number without changing the array and in O(1) memory | junior | 🟡 medium | sort / seen table / binary search on values / Floyd's cycle detection, rho graph, tortoise-and-hare stepper |
| 0018 | Two hourglasses: measure D minutes from time 0 | junior | 🟡 medium | BFS over (time, sand, sand) states, decide only at events, hourglass stepper and branching figure |
| 0019 | Two hourglasses: measure D minutes between two moments | senior | 🔴 hard | Dijkstra over (sand, sand, measured) with a zero-cost "start" edge, Bézout, hourglass stepper |
| 0020 | PCIe: every legal completion split of one read request (MRRS, MPS, RCB) | senior | 🟡 medium | protocol rules → "every cut on an RCB boundary", recursive enumeration largest-first, 2^c count, splits map, MPS pruning |
| 0021 | PCIe: how many completion splits (two 256-byte and two 512-byte requests), and the general formula with proof | senior | 🟡 medium | blocks and interior boundaries, 2^(N-1) when MPS does not bind, compositions with parts ≤ m, generating function, closed form S(N) − S(N−1) + δ, T(N, k), no code |
| 0022 | Generalized Josephus: one stays, two leave (N = 30, a formula, bonus for any L) | senior | 🔴 hard | recurrence in steps of 2, parity chains, zero points 3^m and 2·3^m, F = 3(N − M)/2, general L with residue chains, charts of the chains (no code) |
| 0023 | PCIe endpoint reference model: writes, reads and completions (aligned, then any address) | senior | 🟡 medium | memory as RCB-sized blocks, completions built at request time, per-read queue with a random ready cycle, interleaving between reads, read-modify-write of partial blocks, random subset of the interior RCB boundaries, Byte Count; SV classes with virtual methods and a Python subclass; an explorer with a request builder and the interleaved completions |
| 0024 | USB4 Path credits reference model: Credit Grant, the transmit rule across the wrap, and Path Credit Sync after a lost packet | senior | 🟡 medium | four cumulative 8-bit counters (PCC, PCL at the Egress; PCR, PCA at the Ingress), forward distance on the modulo-256 circle (1..127), grant overwrites PCL, credits leak on packet loss, Sync corrects PCA with the old PCR; one class per side, subclasses add the Sync; stepper of both runs, circle figures; an explorer with the counters on a modulo-256 circle |
| 0025 | PCIe Data Link Ack/Nak reference model: Sequence Numbers, Retry Buffer, cumulative Ack (a random 1..4 TLPs per Ack), rollover, then bad LCRC, Nak and Replay, lost Acks, duplicates and illegal DLLPs | senior | 🟡 medium | transmitter (NEXT_TRANSMIT_SEQ, ACKD_SEQ, Retry Buffer purged by position) and receiver (NEXT_RCV_SEQ, NAK_SCHEDULED, random Ack coalescing) classes, part b subclasses add Nak / Replay / duplicate window / DLLP checks; error injection on the link, replay timeout from the environment; steppers of both runs, Mermaid decision flows; an explorer with the two sides, the link queues and the page's examples as scripts |
| 0026 | Three people and one motorcycle: the fastest way for all three to arrive (walk 13 h, ride 1 h, then a formula) | junior | 🟢 easy | speed ratio α instead of the unknown distance, three phases with one equation each, symmetry y = r, T = (3α + 1)/(α + 3)·t1, three strategies compared, position-time chart, road figure (no code) |
| 0027 | Cake split by fractions of what is left, growing as an arithmetic sequence: who gets the most (a = 0.01, d = 0.1, then any a and d ≤ 1/2) | junior | 🟡 medium | ratio of neighbours, quadratic threshold T = (√(d² + 4d) − d)/2, single peak because p²/(1 − p) grows, the capped last person, ties, a = d; cake rows, shares bars, fractions against T, ratio chart, slider explorer (no code) |
| 0028 | Cake split by fractions of what is left, growing as a geometric sequence: who gets the most (a = 0.01, q = 1.5, then any a and 1 < q ≤ 2) | junior | 🟡 medium | ratio q(1 − p), threshold 1 − 1/q, k = ⌈log_q((q − 1)/a)⌉, ties, the capped last person, q ≤ 1 and q > 2; cake rows, shares bars, fractions against T, ratio chart, slider explorer (no code) |
| 0029 | Second, minute and hour hands: how many times at least two meet in a day (00:00 to 23:59:59), then the general formula and proof | junior | 🟡 medium | laps of the faster hand, n_i − n_j meetings per pair (1416, 1438, 22), 00:00 and 12:00 counted three times, 2872; T_ij = t_i t_j / (t_j − t_i), closed / open / half-open counts, 11a = 708b so triple meetings only every 12 h; clock face, angle charts, a draggable clock explorer with live counters (no code) |
| 0030 | Spider and fly on a box: the shortest surface path (30 × 12 × 12 room, spider one unit below the ceiling, fly one unit above the floor), then code for any two points on the opposite end walls | junior | 🟡 medium | unfolding the faces into a plane, the 42 over the ceiling vs 40 through five faces (legs 32 and 24), all 16 nets in a table, validity of a straight line in a net; part b: the four lateral faces as a periodic strip, 4 × 4 × 3 images, two interval checks, the exit point from the spider's wall; SV + Python, tests against an independent face-sequence unfolder; the owner's 3D / net / unfolding-animation tool embedded as is |
| 0031 | Bridge and torch: four people (1, 2, 5, 10 minutes), two on the bridge, one torch, the least total time; then code for any crossing times | junior | 🟡 medium | the slowest pair crosses together (17, not the 19 of "the fastest escorts everyone"), a lower-bound proof, a crossing-by-crossing step figure; part b: Dijkstra over (who is across, torch side) with parent pointers, the greedy rule min(t1 + 2t2 + tn, 2t1 + t(n−1) + tn) checked against the search; SV + Python, a bridge explorer that plays the plan (or a classic one, on a bridge of two or three) |
| 0032 | Wolf, goat and cabbage: ferry all three across with a boat for the farmer and one more; then code that finds the plan | student | 🟢 easy | the goat goes first and comes back once (seven crossings, two mirror solutions), a lower-bound argument, a crossing-by-crossing step figure; part b: four-bit states, the ten safe ones, BFS with parent pointers, the state graph with the forbidden states struck out; SV + Python, a river explorer to cross by hand or watch the plan |
| 0033 | FIFO depth from write and read rates: a burst of 120 words at 100 MHz read at 80 MHz, then a reader that skips one slot in four | junior | 🟡 medium | depth = ceil(B (1 - f_r / f_w)), the phase can add one word, cycle simulation against the formula, a fill-level explorer |
| 0034 | Gray code pointers for an asynchronous FIFO: why binary pointers break across a synchronizer, the conversions, full / empty with the wrap bit | junior | 🟡 medium | one bit per step (also on the wrap), bin2gray / gray2bin, full = top two bits inverted and the rest equal, exhaustive check against the occupancy; explorers for the sampled step and for the flags |
| 0035 | Divide a clock by 3 with a 50% duty cycle | junior | 🟡 medium | mod-3 counter, a pulse re-sampled on the falling edge, OR of two flops; glitch argument; half-cycle Python model; the testbench measures period and duty with $realtime; an edge-by-edge explorer with a wake-up in state 3 |
| 0036 | Maximal LFSR: why x^4 + x^3 + 1 cycles through 15 states and x^4 + x^2 + 1 through 6 | student | 🟢 easy | Fibonacci LFSR step and period, zero is a fixed point, primitive polynomials and the order of x, table of every x^4 + ... + 1; an explorer with the taps, the ring of states and the table |
| 0037 | Synchronizer MTBF: one, two and three flops at 500 MHz and 1 GHz | senior | 🟡 medium | MTBF = exp(t_res / tau) / (T0 f_clk f_data), each flop adds a clock period to t_res, sensitivity to frequency and tau, an MTBF explorer |
| 0038 | SVA for a req / ack handshake: req holds, ack within 1..3 cycles, no orphan ack, req drops after ack | junior | 🟡 medium | four concurrent assertions with |->, |=>, ##[1:3], $rose and disable iff, action blocks that count, a Python reference model on sampled traces, injected violations in the testbench; a rule-checker explorer on a drawn trace |

Update this table whenever a question is added.

---

## How questions are organized

Every question is classified along two independent axes, plus free-form topic tags.

### 1. Position level

| Level   | Folder                    | Typical expectations                                                          |
|---------|---------------------------|-------------------------------------------------------------------------------|
| Student | `docs/questions/student/` | Digital logic fundamentals, basic HDL, basic programming, math, logic puzzles |
| Junior  | `docs/questions/junior/`  | SystemVerilog, basic UVM, writing tests and checkers, simple protocols        |
| Senior  | `docs/questions/senior/`  | Testbench architecture, advanced UVM, SVA, coverage closure, debugging        |

### 2. Difficulty (within a level)

| Difficulty | Chip colour | Meaning                                                                  |
|------------|-------------|--------------------------------------------------------------------------|
| `easy`     | green       | Direct knowledge question, short answer                                  |
| `medium`   | amber       | Requires reasoning or a small design / code snippet                      |
| `hard`     | red         | Multi-step problem, trade-offs, or a non-trivial design / debug scenario |

On the site, level and difficulty appear as coloured chips (CSS classes `chip-level` and
`chip-diff-<difficulty>`), generated by the build hook.

Difficulty is **relative to the position level** — a "hard" student question may be an
"easy" senior question.

### 3. Topic tags

Each question carries one or more tags. Use the existing ones where possible:

| Area                | Tags                                                                        |
|---------------------|-----------------------------------------------------------------------------|
| Digital design      | `digital-logic`, `fsm`, `fifo`, `clock-domain-crossing`, `timing`           |
| Verification        | `systemverilog`, `uvm`, `sva`, `coverage`, `constraints`, `randomization`, `methodology`, `debug` |
| Hardware / systems  | `protocols`, `computer-architecture`, `memory`, `cache`                     |
| Software            | `scripting`, `python`, `c-cpp`, `algorithms`, `sorting`, `bfs`, `stack`, `bitwise` |
| Math and logic      | `math`, `digits`, `geometry`, `probability`, `combinatorics`, `sequences`, `logic-puzzles` |
| Other               | `behavioral`                                                                |

---

## Where new questions come from

The owner sends questions and solutions during the week. Gaps in the coverage, new
question formats, and a list of external sources for inspiration (HDLBits, Verification
Academy, ChipVerify, Sunburst Design papers, puzzle sites and more) are kept in
[`HANDOFF.md` → Question variety](HANDOFF.md#question-variety). Take ideas from them, but
write our own statement and solution.

---

## Repository layout

```text
DV-Interview-Questions/
├── README.md
├── CLAUDE.md                   # Working rules for AI sessions (language, skeleton, tests, workflow)
├── HANDOFF.md                  # Task list: done / in progress / future work
├── mkdocs.yml                  # Site configuration
├── requirements.txt            # Pinned Python dependencies for building the site
├── requirements-dev.txt        # Test dependencies (pytest)
├── hooks/
│   └── questions.py            # Validation, navigation, tags, tables, run panels
├── tools/
│   ├── extract_code.py         # Pulls the code blocks out of a question page
│   ├── lint_pages.py           # Checks the page skeleton and the RTL rules
│   ├── check_links.py          # Internal link / anchor check of the built site (--external fetches the rest)
│   ├── check_phone.py          # Every built page at 390 px (sideways scroll, JS errors, axe-core)
│   ├── run_tests.py            # Runs all question tests (Python + SystemVerilog)
│   ├── new_question.py         # Scaffold: page, tests folder, generator stub, README row
│   ├── page_tests.py           # Test helpers: Node runner, "page blocks match the generator"
│   └── figures/                # Generators of the inline SVG figures (q<id>.py with blocks()),
│                               # charts.py (shared chart helpers), fill.py (puts blocks on pages),
│                               # stepper.py, cake.py
├── tests/
│   ├── conftest.py
│   ├── hook/                   # Tests of the site hook (search variants, study paths)
│   ├── tools/                  # Tests of new_question.py, fill.py and charts.py
│   └── <id>/                   # One folder per question with code, e.g. tests/0006/
│       ├── test_<id>.py        # pytest tests of the page's Python code
│       ├── tb.sv               # SystemVerilog testbench of the page's SV code
│       └── demo.py             # Starting code of the in-browser "run" panel
├── templates/
│   └── question.md             # Copy this to start a new question
├── layouts/
│   └── dvq.yml                 # Social preview card layout (RTL) for Material's social plugin
├── docs/                       # Site content
│   ├── index.md                # Home page with the table of all questions
│   ├── tags.md                 # Tag index
│   ├── paths/                  # Study paths: index.md + one page per path
│   ├── questions/
│   │   ├── student/
│   │   │   ├── index.md        # Level page (generated question table)
│   │   │   └── 0001-rising-edge-detector.md, 0002-…, 0003-…, 0010-…, 0012-…, 0015-…, 0032-…, 0036-…
│   │   ├── junior/            # 0004-… to 0006-…, 0008-…, 0009-…, 0013-…, 0014-…, 0016-…, 0017-…, 0018-…, 0026-… to 0031-…, 0033-… to 0035-…, 0038-…
│   │   └── senior/            # 0007-…, 0011-…, 0019-…, 0020-…, 0021-…, 0022-…, 0023-…, 0024-…, 0025-…, 0037-…
│   ├── assets/
│   │   ├── logo.svg, favicon.svg  # Site mark: waveform + amber check
│   │   ├── images/             # Figures and screenshots referenced by questions
│   │   └── spider-fly.html     # The owner's standalone spider-and-fly tool, embedded by 0030 (kept as sent)
│   ├── javascripts/            # MathJax, WaveDrom, marks, table tools, page tools, Python runner,
│   │                           # explorer.js (explorers), reading-tools.js (lightbox, tooltips, part bar)
│   └── stylesheets/extra.css   # Palette, chips, question header, tables / cards, figures
└── .github/workflows/
    ├── deploy.yml              # Test + build on every push, deploy main to GitHub Pages
    └── weekly.yml              # Mondays: external links of the site, newer Verilator release
```

Files are named `<id>-<short-slug>.md`, where `<id>` is a zero-padded running number that
is unique across the whole repository (e.g. `0042-async-fifo-depth.md`).

---

## Question format

Each question is a single Markdown file: a front-matter header followed by the question,
optional collapsible hints, the solution and the key takeaways. The headings and text are
in Hebrew. See [`templates/question.md`](templates/question.md).

Conventions:

- **Solutions are collapsed** (`??? success "פתרון"`) so the page can be used for practice.
- **Multi-part questions** stay in one file, with `### סעיף א`, `### סעיף ב`, ... and a
  separate collapsed solution right after each part.
- **Fixed page skeleton** (checked by `tools/lint_pages.py`, which runs in CI):
  - one `??? interviewer "מה המראיין בודק"` block right after the question text, written
    so that it does not reveal the answer;
  - hints as a ladder: `??? tip "רמז 1"`, `??? tip "רמז 2"` (hint 2 is shown only after
    hint 1 was opened);
  - every solution starts with `!!! answer "תשובה בקצרה"` (one or two sentences), followed
    by the blocks `#### הרעיון { .sol-idea }`, `#### השלבים { .sol-steps }`,
    `#### הקוד { .sol-code }`, `#### למה זה נכון { .sol-proof }`, `#### סיבוכיות { .sol-cost }`
    in this order, keeping only the ones that apply; no other `####` headings;
  - steps are an ordered list inside `<div class="steps" markdown>`, drawn as a timeline;
  - traps and follow-ups at the end use `??? trap "מלכודת: ..."` and `??? followup`.
- **Code answers are given in SystemVerilog and Python**, as linked content tabs
  (`=== "SystemVerilog"` / `=== "Python"`, always in this order). Picking a language in one
  tab switches every tab on the site. Pure RTL design questions (like 0001) may be
  SystemVerilog only.
- **Readable code blocks:** every block has a `title=`, long blocks `linenums="1"`, the
  key lines `hl_lines=`, and non-trivial lines carry Material **code annotations**: a
  `// (1)!` / `# (1)!` marker (or ` (1)` appended to an existing comment) and a numbered
  Hebrew list right after the block. Annotation markers are ignored by the testbench
  fingerprints, so they can be added without touching the translations.
- **Every code answer is tested automatically** (see [Tests](#tests) below): the tests run
  the code exactly as it appears on the page, and the site is only published when they pass.
- **Questions with code get a "run" panel**: the page's Python code runs in the reader's
  browser (Pyodide), with an editable starting script from `tests/<id>/demo.py`.
- **Math stays symbolic**: no Hebrew inside MathJax (`\text{...}` renders Hebrew reversed);
  Hebrew goes in the surrounding sentence.
- **RTL-safe text:** every line, list item and table cell starts with a Hebrew word, or
  with the RLM mark (U+200F) when it has to start with Latin text, code or math.

The full skeleton with comments is in [`templates/question.md`](templates/question.md):

```markdown
---
id: 42
title: חישוב עומק של FIFO אסינכרוני
level: junior            # student | junior | senior  (must match the folder)
difficulty: medium       # easy | medium | hard
tags: [fifo, clock-domain-crossing]
source: ""               # optional: company / interview round
added: 2026-10-15
---

## השאלה
...

??? interviewer "מה המראיין בודק"
    - **...:** ...

### סעיף א – ...

??? tip "רמז 1"
    ...

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ...

    #### הרעיון { .sol-idea }
    ...

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function f" hl_lines="2"
        ...   // (1)!
        ```

        1. ...

    === "Python"
        ```python title="f"
        ...
        ```

    #### למה זה נכון { .sol-proof }
    ...

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: ..."
    ...

??? followup "שאלות המשך"
    ...
```

The build hook validates the front matter and **fails the build** on a missing field, an
unknown level or difficulty, a level that does not match the folder, a file name that does
not start with the id, or a duplicate id. It also generates, per question page:

- the **header card** (id label, title, level and difficulty chips, a "new" chip for 30
  days after `added`, topic links, `added` date, `source` when filled, and "code:
  SystemVerilog + Python" / "tested automatically" badges when the page has code and a
  `tests/<id>/` folder); the page's own title comes from `title`, so the
  Markdown must not start with a `#` heading;
- the Material tags (level, difficulty, topics) for the tag index, with the tag chips above
  the title hidden because the header card shows them;
- a **toolbar** (open all / close all, practice mode that hides the solutions and starts a
  stopwatch; "solved" and "favourite" marks; a random question of the same level). Practice
  mode and the marks are kept in the browser's localStorage (`docs/javascripts/marks.js`),
  so they are per browser and are not sent anywhere;
- a **study path bar** under the toolbar for every path that contains the question (step n
  of m, previous and next in the path);
- a **related questions** list at the end (up to three questions sharing the most topic
  tags, `python` and `systemverilog` not counted), and the previous / next links come from
  Material's `navigation.footer`.

`docs/javascripts/reading-tools.js` adds three reading aids to every question page: an
**enlarge button** on each inline SVG figure and chart (a full-screen view with pinch / wheel
zoom, drag, double tap and Esc), **tap tooltips** on touch screens (a tap on a mark shows its
SVG `<title>`), and on pages with two or more parts a sticky **part bar** of chips under the
toolbar that marks the part being read.

The question tables on the home and level pages have **chip filters** (one choice per group:
level, difficulty, topic, and the reader's own marks: favourites, solved, not solved) plus a
title search, **sortable columns** (header buttons; a "sort" select on phones), a **random
question** button that picks among the rows left after filtering, and turn into **cards** on
narrow screens (`docs/javascripts/question-filter.js`, `.questions-wrap` in `extra.css`).
The level cards and path cards show a "solved n of m" bar from the same marks. Pages with
an explorer, a step figure or an embedded tool carry an "אינטראקטיבי" chip in the header
card, a ▶ mark in the tables and a "ממשק" filter group.

### Study paths

A study path is a short ordered list of questions on one topic, one file per path in
`docs/paths/` (front matter `title`, `description`, `order`, and `steps`: a list of
`{id, note}`; the note is one Hebrew sentence, with code in backticks). The page body is a
short intro and the `<!-- path-steps -->` placeholder; `docs/paths/index.md` and the home
page show the `<!-- path-cards -->`. The hook validates the ids, adds a "מסלולים" tab to the
navigation and puts the path bar on each question of the path.

### Search

Material's search splits on whitespace only and has no Hebrew stemmer, so a word with a
prefix letter (ו ה ב כ ל מ ש) or glued punctuation would not be found. After the build, the
hook adds a hidden `alt` field to every search document with the clean words and their forms
without the prefix letters (one letter always, two or three letters when the rest is a word
used on the site). The toolbar, filters and path bar carry `data-search-exclude`.

### Diagrams, formulas and figures

| Kind of figure                   | How it is written                                                  |
|----------------------------------|--------------------------------------------------------------------|
| Block diagrams, flows, FSMs      | ` ```mermaid ` fenced blocks ([Mermaid](https://mermaid.js.org/); 0024 has a sequence diagram)  |
| Timing diagrams / waveforms      | ` ```wavedrom ` fenced blocks ([WaveDrom](https://wavedrom.com/))  |
| Math                             | LaTeX: `\( ... \)` inline, `\[ ... \]` display (MathJax)           |
| Code                             | Fenced blocks inside SystemVerilog / Python content tabs           |
| Charts                           | Inline SVG with class `perf-chart` + an HTML `viz-legend` (0005, 0006, 0007; 0016 and 0022 survivor chains; 0026 strategy bars and a position-time chart) |
| Geometric figures                | Inline SVG with class `figure` (0004 boxes, 0007 circles, 0016 and 0022 box rows: relabelling, one round, bits; 0020, 0021 and 0023 address axes; 0024 modulo-256 circles) |
| Probability grids                | Inline SVG `figure` with `pg-*` cell classes (outcome ruled out / condition / target) + `viz-legend` (0015) |
| Step-through figures             | `div.stepper` from `tools/figures/stepper.py`: SVG frames with captions, shown one at a time with previous / next buttons, the arrow keys, a swipe on phones, and a link button that copies a deep link to the step (`#stepper-2-step-5` opens that step; steppers are numbered in page order) (0009 walks, 0010 stack, 0016 and 0022 circles, 0017 tortoise and hare, 0018 and 0019 hourglass events, 0023 completion queues cycle by cycle, 0024 credit counters step by step, 0025 Retry Buffer and receiver state per packet) |
| Interactive explorers            | `<div class="explorer" data-kind="..." data-...>`: `docs/javascripts/explorer.js` builds the controls, a summary line and live figures. Every kind now has its own `mount(box)` (controls, a play loop where motion matters, a stepper where steps matter). Kinds: `cake-arith` / `cake-geo` (`data-a`, `data-step`; 0027, 0028: a law select to compare the two laws with the same a, sliders with an exact number field each (a down to 0.0001, a negative d, q below 1; a queue that never finishes stops at 10,000 people), and a person-by-person stepper of a round cake with the growing, scrolling table; the charts and the table show a window of 200 people around the peak), `motorcycle` (`data-t0`, `data-t1`; 0026: sliders, a strategy select, play at four speeds moving the travellers on a road while the chart draws, a scrubber; one to five riders with the symmetric shuttle and its formula, an optional distance in km, and a second plan dashed on the same chart), `josephus` (`data-n`, `data-l`, optional `data-lmax`, `data-nmax`; 0016, 0022: the circle played step by step or at a speed, the survivor highlighted from the start, the order of leaving, the survivor chart; Josephus's own rule (two stay, one leaves) with the recurrence on 0016, a seat field that lists the circles in which a seat survives and rings them on the chart, and N up to a million by a linked list, the circle up to 128), `clock` (`data-t`; 0029: a draggable face, play, a day slider, a typed time, next / previous / next-triple jumps, a pair filter, live counters, and a timeline with a tick per meeting), `strip` (`data-a`, `data-b`, `data-h`, `data-y0`, `data-z0`, `data-y1`, `data-z1`; 0030: drag S and F on two wall panels, the periodic strip with the images, the 48 lines and the shortest one, the path face by face), `hourglass` (`data-mode` zero / interval, `data-a`, `data-b`, `data-d`; 0018, 0019: the plan on a time axis and the events one at a time; an optional third hourglass and a fewest-flips objective beside the page's, with a comparison line), `probability` (`data-p`, `data-c`; 0015: the answer, the two-children square, the curve against q), `bridge` (`data-times`; 0031: typed crossing times, a bridge of two or three, the Dijkstra plan or one of the two classic plans played crossing by crossing, and a table of the three plans), `river` (0032: cross by hand or watch the BFS plan, the state graph follows), `fifo` (`data-burst`, `data-fw`, `data-fr`, `data-idle`; 0033: the fill level over the burst from the cycle simulation, the formula beside it; a timing strip on a real time axis, both clocks at their own period, wr_en and rd_en with the skipped read slots shaded and the count as a bus, over a 40-write-cycle window that a slider moves and the chart marks), `mtbf` (`data-fclk`, `data-fdata`, `data-tau`, `data-t0`, `data-overhead`; 0037: the MTBF of one to three flops in readable units and against the clock frequency), `pcie` (`data-addr`, `data-len`, `data-mps`, `data-rcb`; 0020, 0021: the request cut into its blocks, the count by the dynamic program and by the closed form, the count per number of completions, and the map of the splits when there are at most forty; presets of the page examples), `triangle` (`data-angles`; 0007: three points on the unit circle to drag, type in whole degrees or nudge with the arrow keys once focused (one degree, ten with Shift), green / amber / red for inside / on an edge / outside, the arcs with the longest marked, a random throw, and play, a frame slider and steps over all C(360, 3) triangles of different angles with running counts against 89/359; a histogram of the largest arc over 1,000 seeded draws, inside and outside stacked, with the expected count per bin), `polygon` (`data-n`, `data-nmax`; 0007 part b: the same box for n vertices (arrow keys on a focused vertex too), an n slider, a random draw, 1,000 draws against 1 − n / 2^(n−1) and against the exact discrete fraction over C(360, n)), `boxes` (`data-nmax`; 0009: N boxes on a ring with their cycles coloured, person 0's cut as dashed arrows, a person's walk opening by opening, and 1,000-round counts of the strategy without person 0 against random picks; the copy link carries the arrangement, the person and the opening), `floyd` (`data-nmax`; 0017: a typed or random array as the graph i → nums[i] laid out as a rho, the tortoise and the hare through both phases; the copy link carries the array and the step), `bfs01` (`data-x`, `data-xmax`; 0005: the remainders modulo x on a ring, the BFS tree one dequeue at a time, the queue, the answer read back along the path; a digit set of up to three digits with "no multiple" when the queue empties, and a length-only mode with the BFS layers and the memory line of the hardware follow-up), `brackets` (`data-s`; 0010: a typed bracket string read character by character, the stack, the depth chart, the first failure with its reason), `ttt` (`data-board`; 0011: tap cells on a 3 × 3 board, the page's conditions decide live with the reason a board is not final, a random legal board, the wrap-around diagonals of part b), `shapes` (`data-n`, `data-m`, `data-max`; 0014: squares or rectangles drawn one at a time with the overlapping candidates flashed in red, a whole draw, a heat map over 500 draws), `kaprekar` (`data-digits` 3 or 4; 0012, 0013: a number, its sort-and-subtract chain to 495 or 6174, the histogram of chain lengths), `eurovision` (0008: the announcements one by one with the cups under Israel's total against the points left, and a what-if box for Israel's own scores), `boxes3` (0004: three mislabelled boxes with hidden contents, a tap draws a ball and the deduction appears line by line), `edge` (0001: tap the cells of sig on a timing strip, sig_q and pulse follow for a rising edge, a falling edge or both; the reset trap as a toggle; the page's diagram as a preset), `lfsr` (0036: a width of 3 to 8 bits; tick the taps, step or play from 0…01 on a ring of the non-zero states (up to 6 bits), a timing strip of clk, the state, s[0] and the feedback bit for every step so far (scrolled to the current one), the table of the polynomials with their periods, every one up to 5 bits and the primitive ones from 6 with the count φ(2^n − 1) / n), `div3` (0035: the half-cycle model one clock edge at a time or played, cnt, a, b and clk_out on a strip with the overlap shaded, the duty measured; a wake-up in the unreachable state with the counter as in the module, without a wrap or guarded; a divide by N from 2 to 10 and a strip length of 18, 30 or 60 cycles), `gray` (`data-mode` sync / flags; 0034: a pointer of 3 to 6 bits stepping through a synchroniser with every changing bit tapped as arrived or not, binary against Gray; a FIFO of 8 to 64 entries with pointers one bit wider than the address, write and read, empty and full by the page's rules, and a timing strip with a column per accepted write or read: wr, rd, both pointers in binary and Gray, full and empty). `stock` (0006: prices to drag (or arrow keys on a focused point), random or the page's example, the scan played day by day with the cheapest day so far and the best long, and with the part b select the dearest day so far and the best short; the copy link carries the prices, the day and the select), `handshake` (0038: req and ack drawn cell by cell on a timing strip, the four rules of the reference model checked every cycle with a failure marked on its assertion's row at the cycle the SVA reports it; the page's four traces as presets). `acknak` (0025: the RC and the EP with the two link queues between them; a new TLP, the head of each queue delivered, corrupted or lost, the Ack and Replay timers; the page's two examples as scripts stepped with the same engine, undo, the two invariants checked; a random run of 20, 50 or 200 events at a chosen fault rate, drawn from the seed the way the page's test drives the link, with the invariants checked after every event and the script stopping at a first violation; an event axis under the two sides, a column per event with its label, the counters and a ✗ row for the invariants), `credits` (0024: the four counters as hands on one modulo-256 circle with the credits and the free-slot arcs, the dedicated buffer, packets in flight; grant, transmit, receive or lose, dequeue, sync; the page's examples as scripts; a start at 250 for the wrap; the summary balances credits plus packets in flight against the free slots and names the leak after a loss; a random run of legal events at a chosen loss rate with the invariants checked after every event; the same event axis with the four counters, the credits and the occupancy), `endpoint` (0023: a request builder on the block map, writes painted by write, reads cut at random RCB boundaries and parked, a cycle button running tick-then-completion with the reads interleaved, the completions table with the falling Byte Count and the rules checked; a timeline under the open reads with every read's random wait dashed, its ready time solid, a mark per completion and the current cycle, and under it a cycle axis with the completion of every cycle and a ready row per read; the page's two examples with their exact draws). `trace` (`data-mode` swap / loop; 0002, 0003: the page's Python with the current line lit; the three swaps and the three-variable XOR rotation one line at a time with the values and their expressions in a0, b0 and c0, a same-variable toggle and an 8-bit toggle; the double loop one comparison at a time on a typed or random array, with a jump to the end of the outer iteration and its invariant). The timing strips are one helper (`waveStrip`: clock, bit, bus and flag rows over cycles or half-cycles, scrollable on phones). The row names of every strip stay in view while it scrolls (`stickyNames`). Every strip carries its WaveDrom source (`waveDromOf`, the format of the ```wavedrom blocks) in `data-wavedrom`, and a row under it copies the source or opens it in the WaveDrom editor; the 0033 strip exports on an integer grid of the two clock periods (`fifoGrid`), since WaveDrom takes integer lane periods only. Shared controls of every box: a header with a "?" button that opens one line of help (what the box shows and what its buttons do, one sentence per kind in `HELP`) and an "איפוס הכול" button that rebuilds the box from its data attributes (every control back to its default, a seed or state link dropped from the URL); an enlarge button on every figure (kept through redraws); keyboard stepping when the box has focus (→ next, ← previous, space play / stop, Home and End), with a one-line key hint, and arrow keys on a focused point in the stock, triangle and polygon boxes; a slow / medium / fast select on every play; a seed field and a "copy link" button beside every random draw (the random button draws a new seed, a typed seed replays, and `#seed-<kind>-<n>` in a link replays on load; in stock, floyd, boxes and after a random run of acknak and credits the link is `#state-<kind>.<payload>` and reopens the box in the same state); a reset that returns to the page's values. The math of each kind is exported under Node (with the `mulberry32` seed generator), and the question tests compare it with the Python reference |
| Arrays / small data states       | `<span class="arr"><span>3</span>…</span>` (see question 0003)     |
| Hand-drawn sketches, screenshots | Image files under `docs/assets/images/`, linked by relative path   |
| Standalone HTML tools            | A self-contained page under `docs/assets/`, kept exactly as the owner sent it, embedded with `<iframe class="tool-frame" src="../../../assets/<name>.html">` plus a Markdown link `(../../assets/<name>.html)` to open it in a new tab (0030: `spider-fly.html`). Such a page is not a question page: the linter, the phone check and the figure tests leave it alone, only the link checker sees it |

Prefer text-based diagrams (Mermaid / WaveDrom) over images so they stay editable.

Inline SVG colours come from CSS variables in `docs/stylesheets/extra.css`, so figures
follow the light / dark switch automatically:

| Class | Use |
|-------|-----|
| `s1-line`, `s2-line`, `ink-line` | Series lines (blue, orange, neutral ink) |
| `s1-dot`, `s2-dot`, `ink-dot` | Markers with a background-coloured ring |
| `by-multiples`, `by-enum`, `by-bfs` | Bar fills (series 1–3) |
| `grid`, `axis`, `tick`, `legend` | Chart scaffolding and text |
| `tri-ok`, `tri-bad`, `half-fill`, `axis-c`, `center-dot` | Geometry figures |
| `cup-room`, `left-bar`, `overflow`, `israel-line`, `lost-zone` | "Cups" chart of 0008 (room below a ceiling vs. what is left) |
| `box-node`, `box-hl`, `box-num`, `*-fill` (arrowheads), `s3-line` | Graph of boxes / cycles (0009) |
| `.box-grid` (HTML) | Compact row of numbered cells with a value in each (0009; `bg-10` for ten cells, 0017) |
| `fl-slow`, `fl-fast` | Tortoise and hare rings on a graph (0017) |
| `sand-a`, `sand-b`, `stream-*`, `glass`, `frame`, `measure`, `pruned` | Hourglasses: sand, the falling stream, the glass and frame, the measurement window, a pruned option (0018, 0019; drawn by `tools/figures/hourglass.py`) |
| `cs-rcb`, `cs-req`, `cs-first`, `cs-mid`, `cs-last`, `cs-one`, `cs-bad`, `cs-can`, `cs-size` | PCIe completion splits over the address axis: RCB grid, request limits, completions by role, one above MPS (0020, 0021, 0023; drawn by `tools/figures/q0020.py`, `q0021.py` and `q0023.py`) |
| `cs-blk`, `cs-new`, `cs-keep` | Memory blocks of the endpoint model: a block, the bytes a request touches, the bytes kept by a read-modify-write (0023) |
| `fc-ring`, `fc-tick`, `fc-window`, `fc-ahead`, `fc-pkt`, `fc-grant`, `fc-sync`, `fc-drop`, `fc-slot`, `fc-full` | USB4 credit counters on the modulo-256 circle (the 127-step window, the forward distance) and the stepper of the two adapters: packet / grant / sync arrows, a dropped packet, buffer slots (0024; drawn by `tools/figures/q0024.py`; 0025 adds `fc-nak`, `fc-replay`) |
| `clock-face`, `clock-tick`, `clock-tick5` | The clock dial and its minute and five-minute marks (0029, in the figures and in the clock explorer; hands use `ink-line`, `s1-line`, `s3-line`, and `.hand.is-meet` turns a meeting hand orange) |
| `cake-slice`, `cake-slice2`, `cake-peak`, `cake-rest`, `cake-gone`, `cake-edge` | Cake split rows: a person's slice (two alternating colours), the largest slice, what is left for the next people, what is already taken, the outline of the whole cake (0027, 0028; drawn by `tools/figures/cake.py`) |
| `ttt-grid`, `ttt-ghost`, `mark`, `mark-new`, `cell-s1`…`cell-s3` | Tic-tac-toe boards with highlighted cells (0011) |
| `gp-line`, `gp-dot`, `shp-1`…`shp-3`, `shp-bad`, `shp-num`, `sep-zone`, `dash`, `coord`, `zone-label`, `halo` | Shapes on a grid of points, overlap areas, zones, text with a background halo (0014) |

Site-wide (HTML) classes in the same file: `chip`, `chip-level`, `chip-diff-*`, `chip-new`
(level, difficulty and "new" chips), `question-header` (header card), `question-tools`
(toolbar, with `qt-mark` / `qt-random`), `path-nav`, `path-steps`, `path-card`, `mark-progress`,
`related-questions`, `question-filter` / `filter-group` / `filter-chip` (table
filters), `questions-wrap` (table that becomes cards on phones), the admonition types
`answer` / `interviewer` / `trap` / `followup`, the solution labels `sol-*`, `steps` and
`stepper` (with the `st-*` SVG cell classes). The palette lives in the `[data-md-color-scheme]` blocks at the top:
Material's `primary` / `accent` are set to `custom`, so every colour is defined there.

Figures generated by a script keep the script in `tools/figures/q<id>.py`, so they can be
regenerated when numbers change (`python tools/figures/q0008.py` prints the SVG to paste).
Newer generators (0026 onward) define `blocks()`, and the page marks each block with
`<!-- gen n -->` and `<!-- /gen -->` at its indentation; `python tools/figures/fill.py <id>`
rewrites them in place and `--check` reports a stale page (the question test calls it).
New charts use `tools/figures/charts.py` (`Chart`: slot or value axis, log y, grid,
threshold line, bars, stems, dots, paths), so every chart takes its colours from the CSS.

Hover text on a mark is an SVG `<title>` element. Always pair a chart with a table that
holds the same numbers.

---

## Adding a new question

1. Pick the position level and difficulty. When the owner sends a source file with tables
   and formulas, recompute them first in the question's test and report what does not hold.
2. Run `python tools/new_question.py --level <level> --difficulty <d> --slug <slug> --title
   "<Hebrew title>" --tags a,b [--figures] [--code]`. It takes the next free id, writes
   `docs/questions/<level>/<id>-<slug>.md` from the template, `tests/<id>/`, a generator stub
   with `--figures` and `tb.sv` / `demo.py` with `--code`, and adds a catalog row to this
   README (complete its English title and topics).
3. Write the page. Put any images in `docs/assets/images/` named `<id>-<description>.<ext>`;
   put generated figures in `blocks()` and run `python tools/figures/fill.py <id>`.
4. Run `python tools/run_tests.py <id>` and `python tools/lint_pages.py <id>`, build locally
   (below) and check the page at desktop and phone width, light and dark.
5. Commit with a message like `Add question 0042: async FIFO depth`.

The question automatically appears in the navigation, on its level page, on the home page
table and in the tag index — no other file needs to change.

---

## Tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
python tools/lint_pages.py            # page structure and RTL rules (also in CI)
python tools/run_tests.py             # everything (under a minute once compiled)
python tools/run_tests.py 6 7         # only questions 0006 and 0007
python tools/run_tests.py --python-only
python tools/check_links.py           # internal links and anchors of the built site
python tools/check_links.py site --external   # also fetch every external link (the weekly workflow)
python tools/check_phone.py           # every built page at 390 px: no sideways scroll, no JS errors
python tools/check_phone.py --scheme dark   # the same in dark mode (CI: manual run with phone_dark)
python tools/check_phone.py --axe node_modules/axe-core/axe.min.js   # plus axe-core (npm install axe-core)
python tools/figures/fill.py --check 26     # generated blocks of a page are up to date
```

The linter checks RTL at the start of every paragraph, list item, heading and table cell,
at any indent (admonitions, list items, the steps timeline), and **warns** about literal
SVG colours. The phone check also **warns** about display math wider than its column (it
would scroll on its own; split it with `aligned`) and, with `--axe`, about serious and
critical [axe-core](https://github.com/dequelabs/axe-core) findings (contrast, names,
keyboard access; CI runs it on every page, `--axe-fail` makes them failures). Warnings never
fail CI. The explorer tests run the JavaScript under Node (CI installs it; locally the tests
skip without it).

`check_phone.py` needs Playwright (`requirements-dev.txt`) and its Chromium
(`python -m playwright install chromium`). It writes a screenshot of each page to
`.cache/phone/` (CI uploads them as the `phone-screenshots` artifact). Without access to the
CDNs, add `--offline` and serve MathJax and Mermaid from local copies with `--route`, as in
`HANDOFF.md`. `tests/hook/` tests the hook itself (search variants, study paths), and
`tests/tools/` the authoring tools.

The SystemVerilog tests need **Verilator newer than 5.052, with the z3 solver**, so that
`randomize()` with constraints runs the classes exactly as published (the 5.052 release
crashes on the 0011 class and leaves shapes of the 0014 subclass unrandomized; the apt
package, 5.020, has no constraint support at all). Until the next release, CI builds a
pinned development commit (`VERILATOR_REF` in `.github/workflows/deploy.yml`, currently
`7a5509c`). Build the same commit once locally (about 10 minutes) and put it on the `PATH`:

```bash
sudo apt install git help2man perl python3 make autoconf g++ flex bison libfl2 libfl-dev zlib1g zlib1g-dev z3
git init /tmp/verilator && cd /tmp/verilator
git fetch --depth 1 https://github.com/verilator/verilator.git 7a5509c89b1dd55cf78809907729a55f7fef55b7 && git checkout FETCH_HEAD
autoconf && ./configure --prefix="$HOME/verilator" && make -j"$(nproc)" && make install
export PATH="$HOME/verilator/bin:$PATH"
```

CI caches the install tree per commit, so only the first run after a bump is slow.
`run_tests.py` refuses an older Verilator with a message; `--python-only` still works
without it.

- **Python** (`tests/<id>/test_<id>.py`, pytest): `load_python(<id>)` executes every Python
  block of the page and returns the namespace, so the tests call the published functions.
  Typical test: a simple reference solution against the efficient one on random inputs.
- **SystemVerilog** (`tests/<id>/tb.sv`, Verilator): the testbench pulls code from the page
  with directives, and must print a line starting with `PASS`.

  | Directive | Meaning |
  |-----------|---------|
  | `//@page <text>` | Replaced by the page's SV block that contains `<text>` |
  | `//@translation-of <text> <hash>` | The testbench holds a hand translation of that block, only for a proven simulator bug (none today); fails when the page block changes, so the translation is never stale |
  | `//@flags <flags>` | Extra Verilator flags, e.g. `--timing` for clocked RTL |

  When the simulator provably cannot run the published SV (a crash or wrong results, not a
  missing feature), the testbench translates the *intent* into supported code, e.g.
  constraints become check functions plus an exhaustive or rejection solver. No page
  needs one today; the mechanism stays for the next simulator bug. Get the hash for a
  translation with `python -c "import sys; sys.path.insert(0, 'tools'); import extract_code as e; print(e.fingerprint(e.pick(<id>, 'systemverilog', '<text>')))"`.
- Compiled testbenches are cached in `.cache/sv/` by content hash, so unchanged ones are not
  recompiled. A first full compile takes about a minute with 4 cores; the z3 solver needs
  about 0.1 s per `randomize()` on 0014, so that testbench runs for ~30 s.
- Pure logic questions have no tests. A page without code can still have a `tests/<id>/`
  folder when it states numbers worth checking (0015 probabilities, 0021 counts and the
  formula): the tests then compute them independently and check the figures against the
  generator. The "tested automatically" badge needs both code and a tests folder.

## Running the site locally

```bash
pip install -r requirements.txt
mkdocs serve          # live preview at http://127.0.0.1:8000
mkdocs build --strict # the same check that CI runs
```

## Publishing

The GitHub Actions workflow runs the tests and builds the site on every push and pull
request, and deploys the `main` branch to GitHub Pages. A failing test blocks the deploy,
so the live site keeps its previous version. One-time setup in the repository settings:
**Settings → Pages → Build and deployment → Source: GitHub Actions**.

This is already set up: every push to `main` publishes the site within about a minute at
<https://tamirgabgab.github.io/DV-Interview-Questions/>. A failed deploy can be re-run from
the Actions tab (the workflow also has a manual `workflow_dispatch` trigger).

### Social preview cards

Material's `social` plugin renders a 1200 × 630 card per page (`og:image`, shown when a
link is shared in WhatsApp, LinkedIn, Slack...) from the RTL layout in `layouts/dvq.yml`:
navy background, the logo, the title aligned to the right, level · difficulty · id on
question pages, the description and an amber bar. It needs `pillow` and `cairosvg`
(`requirements.txt`; `libcairo2` on the machine) and downloads the Rubik font from Google
Fonts into `.cache/plugin/social/` on the first build (CI caches that directory). Without
network access, put any Hebrew-capable TTF there as `fonts/Rubik/Regular.ttf` and
`Bold.ttf`. The cards are written to `site/assets/images/social/`.

### Comments

Question pages can end with a **discussion** section backed by GitHub Discussions through
[giscus](https://giscus.app) (readers sign in with GitHub; the thread lives in the
repository's Discussions, one per page path). The code is in place and switched off until
the ids are filled in. One-time setup by the repository owner:

1. **Settings → General → Features**: tick **Discussions**. In the Discussions tab create
   (or keep) a category of the **Announcements** type, so only the site creates threads.
2. Install the [giscus GitHub App](https://github.com/apps/giscus) on this repository.
3. Open <https://giscus.app>, enter `tamirgabgab/DV-Interview-Questions`, choose the
   category, and copy the `data-repo-id` and `data-category-id` values it shows.
4. Paste them into `mkdocs.yml` under `extra.comments` (`repo_id`, `category_id`; change
   `category` if a different one was chosen) and push to `main`.

The hook (`_comments_block` in `hooks/questions.py`) then adds "## דיון" with the giscus
script to every question page, in Hebrew, following the site's light / dark toggle.

### Weekly checks

`.github/workflows/weekly.yml` runs every Monday (and on request): it builds the site and
fetches every external link (`check_links.py --external`; 403 / 429 answers count as
"refused the robot", not broken), and compares the latest Verilator release with
`VERILATOR_RELEASE` (the release the pinned commit of `deploy.yml` follows). A broken link
fails the run; a newer release opens one issue with the steps to bump the pin.
