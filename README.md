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
├── hooks/
│   └── questions.py            # Validation, navigation, tags and filterable tables
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
│   ├── javascripts/            # MathJax config, WaveDrom rendering, table filter
│   └── stylesheets/extra.css   # RTL fixes and question styling
└── .github/workflows/deploy.yml  # Build on every push, deploy main to GitHub Pages
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
- **Every code answer is executed before it is published**: Python directly, SystemVerilog
  in a simulator (Verilator, Icarus as a cross-check), usually by comparing a simple
  reference solution with the efficient one on many random inputs. When something could
  not be run (e.g. constraints the available simulator does not support), the page says so.
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
5. Build locally (below) and check the page.
6. Add the question to the catalog table at the top of this README.
7. Commit with a message like `Add question 0042: async FIFO depth`.

The question automatically appears in the navigation, on its level page, on the home page
table and in the tag index — no other file needs to change.

---

## Running the site locally

```bash
pip install -r requirements.txt
mkdocs serve          # live preview at http://127.0.0.1:8000
mkdocs build --strict # the same check that CI runs
```

## Publishing

The GitHub Actions workflow builds the site on every push and pull request, and deploys
the `main` branch to GitHub Pages. One-time setup in the repository settings:
**Settings → Pages → Build and deployment → Source: GitHub Actions**.

This is already set up: every push to `main` publishes the site within about a minute at
<https://tamirgabgab.github.io/DV-Interview-Questions/>. A failed deploy can be re-run from
the Actions tab (the workflow also has a manual `workflow_dispatch` trigger).
