# DV Interview Questions

A curated, searchable collection of **Design Verification (DV)** job interview questions —
plus math and logic questions that often come up in the same interviews. Each question has
a clearly written statement and a full, readable solution, including diagrams, waveforms,
formulas and code where they help.

The content is written in **Hebrew** and published as a public website (MkDocs Material,
right-to-left layout) with filtering by **position level**, **difficulty** and **topic**.

**Live site:** <https://tamirgabgab.github.io/DV-Interview-Questions/>

> **Status:** the site is live and holds 7 questions (see the catalog below).
> [`HANDOFF.md`](HANDOFF.md) has the work log, open tasks and improvement ideas.

---

## Catalog

| Id | Question (Hebrew title on the site) | Level | Difficulty | Main topics |
|----|-------------------------------------|-------|------------|-------------|
| 0001 | Rising edge detector | student | 🟢 easy | digital logic, SystemVerilog, WaveDrom |
| 0002 | Swap two variables (temp / arithmetic / XOR) | student | 🟢 easy | bitwise, math proofs |
| 0003 | What does this code do? (double-loop sort) | student | 🟢 easy | algorithms, sorting |
| 0004 | Three mislabeled boxes | junior | 🟡 medium | logic puzzle, algorithms |
| 0005 | Smallest multiple made of digits 0 and 1 | junior | 🟡 medium | BFS, math, performance chart |
| 0006 | Stock max profit, long or short | junior | 🟡 medium | algorithms, O(n²) vs. O(n) |
| 0007 | Random triangle on the unit circle containing the center | senior | 🟡 medium | SV constraints, probability |

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
| Staff   | `docs/questions/staff/`   | Verification strategy and planning, methodology, scaling, leading a team      |

### 2. Difficulty (within a level)

| Difficulty | Badge | Meaning                                                                  |
|------------|-------|--------------------------------------------------------------------------|
| `easy`     | 🟢    | Direct knowledge question, short answer                                  |
| `medium`   | 🟡    | Requires reasoning or a small design / code snippet                      |
| `hard`     | 🔴    | Multi-step problem, trade-offs, or a non-trivial design / debug scenario |

Difficulty is **relative to the position level** — a "hard" student question may be an
"easy" senior question.

### 3. Topic tags

Each question carries one or more tags. Use the existing ones where possible:

| Area                | Tags                                                                        |
|---------------------|-----------------------------------------------------------------------------|
| Digital design      | `digital-logic`, `fsm`, `fifo`, `clock-domain-crossing`, `timing`           |
| Verification        | `systemverilog`, `uvm`, `sva`, `coverage`, `constraints`, `randomization`, `methodology`, `debug` |
| Hardware / systems  | `protocols`, `computer-architecture`, `memory`, `cache`                     |
| Software            | `scripting`, `python`, `c-cpp`, `algorithms`, `sorting`, `bfs`, `bitwise`   |
| Math and logic      | `math`, `probability`, `combinatorics`, `logic-puzzles`                     |
| Other               | `behavioral`                                                                |

---

## Repository layout

```text
DV-Interview-Questions/
├── README.md
├── HANDOFF.md                  # Task list: done / in progress / future work
├── mkdocs.yml                  # Site configuration
├── requirements.txt            # Pinned Python dependencies for building the site
├── requirements-dev.txt        # Test dependencies (pytest)
├── hooks/
│   └── questions.py            # Validation, navigation, tags, tables, run panels
├── tools/
│   ├── extract_code.py         # Pulls the code blocks out of a question page
│   └── run_tests.py            # Runs all question tests (Python + SystemVerilog)
├── tests/
│   ├── conftest.py
│   └── <id>/                   # One folder per question with code, e.g. tests/0006/
│       ├── test_<id>.py        # pytest tests of the page's Python code
│       ├── tb.sv               # SystemVerilog testbench of the page's SV code
│       └── demo.py             # Starting code of the in-browser "run" panel
├── templates/
│   └── question.md             # Copy this to start a new question
├── docs/                       # Site content
│   ├── index.md                # Home page with the table of all questions
│   ├── tags.md                 # Tag index
│   ├── questions/
│   │   ├── student/
│   │   │   ├── index.md        # Level page (generated question table)
│   │   │   └── 0001-rising-edge-detector.md, 0002-…, 0003-…
│   │   ├── junior/            # 0004-…, 0005-…, 0006-…
│   │   ├── senior/            # 0007-…
│   │   └── staff/
│   ├── assets/images/          # Figures and screenshots referenced by questions
│   ├── javascripts/            # MathJax, WaveDrom, table filter, Python runner (Pyodide)
│   └── stylesheets/extra.css   # RTL fixes and question styling
└── .github/workflows/deploy.yml  # Test + build on every push, deploy main to GitHub Pages
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
  Hints use `??? tip "רמז"`; takeaways and follow-ups use `??? note` / `??? warning`.
- **Multi-part questions** stay in one file, with `### סעיף א`, `### סעיף ב`, ... and a
  separate collapsed solution right after each part.
- **Code answers are given in SystemVerilog and Python**, as linked content tabs
  (`=== "SystemVerilog"` / `=== "Python"`, always in this order). Picking a language in one
  tab switches every tab on the site. Pure RTL design questions (like 0001) may be
  SystemVerilog only.
- **Every code answer is tested automatically** (see [Tests](#tests) below): the tests run
  the code exactly as it appears on the page, and the site is only published when they pass.
- **Questions with code get a "run" panel**: the page's Python code runs in the reader's
  browser (Pyodide), with an editable starting script from `tests/<id>/demo.py`.
- **Math stays symbolic**: no Hebrew inside MathJax (`\text{...}` renders Hebrew reversed);
  Hebrew goes in the surrounding sentence.

```markdown
---
id: 42
title: חישוב עומק של FIFO אסינכרוני
level: junior            # student | junior | senior | staff  (must match the folder)
difficulty: medium       # easy | medium | hard
tags: [fifo, clock-domain-crossing]
source: ""               # optional: company / interview round
added: 2026-10-15
---

## השאלה
...

??? tip "רמז"
    ...

## הפתרון

??? success "פתרון"
    ...

    === "SystemVerilog"
        ```systemverilog
        ...
        ```

    === "Python"
        ```python
        ...
        ```

## נקודות חשובות ושאלות המשך

??? note "נקודות חשובות"
    ...
```

The build hook validates the front matter and **fails the build** on a missing field, an
unknown level or difficulty, a level that does not match the folder, a file name that does
not start with the id, or a duplicate id. It also adds the metadata line at the top of the
page and turns level, difficulty and topics into tags.

### Diagrams, formulas and figures

| Kind of figure                   | How it is written                                                  |
|----------------------------------|--------------------------------------------------------------------|
| Block diagrams, flows, FSMs      | ` ```mermaid ` fenced blocks ([Mermaid](https://mermaid.js.org/))  |
| Timing diagrams / waveforms      | ` ```wavedrom ` fenced blocks ([WaveDrom](https://wavedrom.com/))  |
| Math                             | LaTeX: `\( ... \)` inline, `\[ ... \]` display (MathJax)           |
| Code                             | Fenced blocks inside SystemVerilog / Python content tabs           |
| Charts                           | Inline SVG with class `perf-chart` + an HTML `viz-legend` (0005, 0006, 0007) |
| Geometric figures                | Inline SVG with class `figure` (0004 boxes, 0007 circles)          |
| Arrays / small data states       | `<span class="arr"><span>3</span>…</span>` (see question 0003)     |
| Hand-drawn sketches, screenshots | Image files under `docs/assets/images/`, linked by relative path   |

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

Hover text on a mark is an SVG `<title>` element. Always pair a chart with a table that
holds the same numbers.

---

## Adding a new question

1. Pick the position level and difficulty.
2. Take the next free `id` (one more than the highest existing id under `docs/questions/`).
3. Copy `templates/question.md` to `docs/questions/<level>/<id>-<slug>.md` and fill it in.
4. Put any images in `docs/assets/images/` named `<id>-<description>.<ext>`.
5. If the question has code, add `tests/<id>/` with `test_<id>.py`, `tb.sv` and `demo.py`
   (copy a similar question's folder) and run `python tools/run_tests.py <id>`.
6. Build locally (below) and check the page.
7. Add the question to the catalog table at the top of this README.
8. Commit with a message like `Add question 0042: async FIFO depth`.

The question automatically appears in the navigation, on its level page, on the home page
table and in the tag index — no other file needs to change.

---

## Tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
sudo apt install verilator            # Verilator 5.020 on Ubuntu 24.04
python tools/run_tests.py             # everything (a few seconds once compiled)
python tools/run_tests.py 6 7         # only questions 0006 and 0007
python tools/run_tests.py --python-only
```

- **Python** (`tests/<id>/test_<id>.py`, pytest): `load_python(<id>)` executes every Python
  block of the page and returns the namespace, so the tests call the published functions.
  Typical test: a simple reference solution against the efficient one on random inputs.
- **SystemVerilog** (`tests/<id>/tb.sv`, Verilator): the testbench pulls code from the page
  with directives, and must print a line starting with `PASS`.

  | Directive | Meaning |
  |-----------|---------|
  | `//@page <text>` | Replaced by the page's SV block that contains `<text>` |
  | `//@translation-of <text> <hash>` | The testbench holds a hand translation of that block (for simulator limits); fails when the page block changes, so the translation is never stale |
  | `//@flags <flags>` | Extra Verilator flags, e.g. `--timing` for clocked RTL |

  When the published SV uses something Verilator cannot run, the testbench translates the
  *intent* into supported code, e.g. constraints become check functions plus
  "draw from the declared ranges until all constraints hold", and `dist` becomes a weighted
  queue that is shuffled before taking its first element. Get the hash for a translation
  with `python -c "import sys; sys.path.insert(0, 'tools'); import extract_code as e; print(e.fingerprint(e.pick(<id>, 'systemverilog', '<text>')))"`.
- Compiled testbenches are cached in `.cache/sv/` by content hash, so unchanged ones are not
  recompiled. A first full compile takes about 10 seconds with 4 cores.
- Logic and proof questions have no tests; only questions with code get a `tests/<id>/` folder.

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
