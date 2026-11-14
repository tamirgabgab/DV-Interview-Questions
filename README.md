# DV Interview Questions

Design Verification (DV) job interview questions, with the math, probability and logic
puzzles that come up in the same interviews: 92 questions at three levels, each with a full
solution in Hebrew, tested code and an interactive box.

## The site

**<https://tamirgabgab.github.io/DV-Interview-Questions/>**

**[Question map](https://tamirgabgab.github.io/DV-Interview-Questions/graph.html)**: an
interactive knowledge graph of every question and the techniques its solution uses (made
with [graphify](https://pypi.org/project/graphifyy/)); click a question for a link to its page

- [Home page](https://tamirgabgab.github.io/DV-Interview-Questions/): how it works, the
  newest questions, the levels, featured study paths and the FAQ
- [All questions](https://tamirgabgab.github.io/DV-Interview-Questions/all/): a table you
  can filter by level, difficulty, kind and topic, and a random question
- By level: [student](https://tamirgabgab.github.io/DV-Interview-Questions/questions/student/) (14),
  [junior](https://tamirgabgab.github.io/DV-Interview-Questions/questions/junior/) (62),
  [senior](https://tamirgabgab.github.io/DV-Interview-Questions/questions/senior/) (24)
- [Study paths](https://tamirgabgab.github.io/DV-Interview-Questions/paths/): 13 paths of a
  few questions on one topic, in the order to solve them
- [Topics](https://tamirgabgab.github.io/DV-Interview-Questions/tags/) and
  [what's new](https://tamirgabgab.github.io/DV-Interview-Questions/new/)
- [`notes/CATALOG.md`](notes/CATALOG.md): every question with a direct link
- [Tutorial videos](#tutorial-videos): the questions' videos on YouTube
- [How the site is built](https://tamirgabgab.github.io/DV-Interview-Questions/how-built/):
  two animated diagrams, the CI run of a push (its three lanes) and how a question page
  becomes the site

## What is on the site

- Questions at three levels (student, junior, senior), each with a "what the interviewer
  checks" note, hints that open one at a time, a short answer and a full solution: the
  idea, the steps, the code, the proof and the cost.
- Code in Python and SystemVerilog (linked tabs, Python first), tested automatically: the
  tests run the code exactly as the page shows it, the SystemVerilog under Verilator. A run
  panel executes the Python in the browser.
- An interactive box in every question: edit the input, then play the solution step by
  step or jump to the result. Figures are inline SVG, generated and checked against the page.
- Interview mode (a clock against a target time, hints counted, a confidence question
  before a solution, the interviewer's follow-up questions and a summary), an interview
  builder on the home page, a quick jump to any question (Ctrl K or /), "solved" and
  "favourite" marks kept in the browser, search, light and dark themes, and a layout that
  works on a phone.

## Tutorial videos

A video walks through a question's solution. The videos are made outside this repository
and published on YouTube; a question page links its video with its YouTube id, and then
gets a "סרטון הסבר" button that opens the video in a dialog (and, when the chapter starts
are given, a link to each part's chapter). How to add one: [`notes/VIDEOS.md`](notes/VIDEOS.md).
This table is written by `python tools/build/catalog.py`.

<!-- videos -->
No videos yet.
<!-- /videos -->

## The repository

```text
docs/            the site: question pages (docs/questions/<level>/<id>-<slug>.md), study paths,
                 javascripts/ (explorer/ has one file per box), stylesheets/ (numbered shared
                 parts, then questions/<id>-<name>.css), assets/
hooks/           questions.py, the MkDocs hook: validation, navigation, tables, the search index
overrides/       the theme's templates: main.html, 404.html, partials/
tests/           pytest and Verilator tests: one folder per question (tests/<id>/), hook/, tools/
tools/
  checks/        everything CI runs: lint_pages, run_tests, check_links, check_phone, check_404,
                 check_keyboard, check_explorers, check_jumps, check_inputs, check_contrast,
                 check_videos, text_only (the fast lane)
  build/         what the site is built from: catalog, graph (+ graph_concepts.json),
                 search_text, make_icons, social/ (the share card layout), codemirror/
  authoring/     new_question.py and the page template question.md
  figures/       q<id>.py, the generator of each question's figures, with charts.py and fill.py;
                 site_flow.py draws the diagrams of docs/how-built.md
  extract_code.py, page_tests.py, explorer_node.js, dev_setup.sh   shared by all of the above
notes/           working notes, not part of the site: HANDOFF.md (task list and work log, with
                 two archives), VIDEOS.md (adding a YouTube video), CATALOG.md (written by catalog.py)
requirements/    site.txt (building the site), dev.txt (tests and checks)
mkdocs.yml       the site's configuration
CONTRIBUTING.md  how a question is written, the tools and the checks in full
CLAUDE.md        the working rules for AI sessions
```

## Running it locally

```bash
pip install -r requirements/site.txt
mkdocs serve          # http://127.0.0.1:8000
```

The tests and checks need `requirements/dev.txt` as well (or `tools/dev_setup.sh`):

```bash
python tools/checks/lint_pages.py     # the page skeleton and the RTL rules
python tools/checks/run_tests.py      # every question's tests (Python, and SystemVerilog with Verilator)
mkdocs build --strict                 # the build CI runs
```

Writing questions, every check and the tools: [`CONTRIBUTING.md`](CONTRIBUTING.md). Work
log and open tasks: [`notes/HANDOFF.md`](notes/HANDOFF.md).
