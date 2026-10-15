# DV Interview Questions

A curated, searchable collection of **Design Verification (DV)** job interview questions —
plus math and logic questions that often come up in the same interviews. Each question has
a clearly written statement and a full, readable solution, including diagrams, waveforms,
formulas and code where they help.

The content is written in **Hebrew** and published as a public website (MkDocs Material,
right-to-left layout) with filtering by **position level**, **difficulty** and **topic**.

> **Status:** the site skeleton is built and contains one example question.
> See [`HANDOFF.md`](HANDOFF.md) for the task list, progress and next steps.

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
| Verification        | `systemverilog`, `uvm`, `sva`, `coverage`, `methodology`, `debug`           |
| Hardware / systems  | `protocols`, `computer-architecture`, `memory`, `cache`                     |
| Software            | `scripting`, `python`, `c-cpp`, `algorithms`                                |
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
│   │   │   └── 0001-rising-edge-detector.md
│   │   ├── junior/
│   │   ├── senior/
│   │   └── staff/
│   ├── assets/images/          # Figures and screenshots referenced by questions
│   ├── javascripts/            # MathJax config, WaveDrom rendering, table filter
│   └── stylesheets/extra.css   # RTL fixes and question styling
└── .github/workflows/deploy.yml  # Build on every push, deploy main to GitHub Pages
```

Files are named `<id>-<short-slug>.md`, where `<id>` is a zero-padded running number that
is unique across the whole repository (e.g. `0007-async-fifo-depth.md`).

---

## Question format

Each question is a single Markdown file: a front-matter header followed by the question,
an optional collapsible hint, the solution and the key takeaways. The headings and text are
in Hebrew. See [`templates/question.md`](templates/question.md).

```markdown
---
id: 7
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
...

## נקודות חשובות ושאלות המשך
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
| Code                             | Fenced blocks with a language (`systemverilog`, `python`, `c`, …)  |
| Hand-drawn sketches, screenshots | Image files under `docs/assets/images/`, linked by relative path   |

Prefer text-based diagrams (Mermaid / WaveDrom) over images so they stay editable.

---

## Adding a new question

1. Pick the position level and difficulty.
2. Take the next free `id` (one more than the highest existing id under `docs/questions/`).
3. Copy `templates/question.md` to `docs/questions/<level>/<id>-<slug>.md` and fill it in.
4. Put any images in `docs/assets/images/` named `<id>-<description>.<ext>`.
5. Build locally (below) and check the page.
6. Commit with a message like `Add question 0007: async FIFO depth`.

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

The site is then available at `https://tamirgabgab.github.io/DV-Interview-Questions/`.
