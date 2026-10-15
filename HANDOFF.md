# HANDOFF

Living task list for this repository: what was done, what is in progress, and what comes
next. Update it at the end of every work session so anyone (human or AI) can pick up
where the last session stopped.

_Last updated: 2026-10-15_

---

## Project goal

A public website for a personal collection of Design Verification (DV) interview
questions, plus math and logic questions. Each question is written clearly in Hebrew, with
a full readable solution and diagrams where relevant, and is classified by **position
level** (Student / Junior / Senior / Staff), **difficulty** (Easy / Medium / Hard) and
**topic tags**.

Workflow: the repository owner sends questions + solutions (text and sometimes images)
during the week; each one is rewritten in a clean, consistent format and added to the
requested place in the repository.

---

## Decisions

| Topic               | Decision                                                                   |
|---------------------|----------------------------------------------------------------------------|
| Content language    | Hebrew (code, identifiers and repo docs stay in English)                   |
| Visibility          | Public site on GitHub Pages                                                |
| Topics              | DV topics plus math, probability and logic puzzles                         |
| Site technology     | MkDocs + Material for MkDocs, RTL layout (`language: he`)                  |
| Difficulty scale    | 3 levels: easy / medium / hard                                             |
| Multi-level questions | One file in one level folder                                             |
| Source field        | Optional `source` field, empty by default                                  |
| Code languages      | SystemVerilog + Python only, as linked tabs (SystemVerilog first)          |
| Solutions           | Collapsed by default (practice mode); one collapsed solution per sub-part  |
| Multi-part questions | One file, `### סעיף א/ב/ג` with a solution after each part                |

---

## Done

- [x] `README.md`: purpose, classification scheme, repository layout, question format,
      diagram conventions, how to add a question, local run and publishing.
- [x] `HANDOFF.md` (this file).
- [x] MkDocs Material site skeleton in Hebrew / RTL with light and dark mode.
- [x] `hooks/questions.py`:
  - front-matter validation that fails the build on errors;
  - navigation generated automatically (one tab per level, questions sorted by id);
  - level, difficulty and topics turned into Material tags + a metadata line per question;
  - `<!-- questions-table -->` placeholder replaced by a filterable table
    (level / difficulty / topic / free text) on the home page and on each level page.
- [x] Rendering support: Mermaid diagrams, WaveDrom timing diagrams, MathJax formulas,
      syntax highlighting, collapsible hints (`??? tip`), copy button on code blocks.
- [x] RTL fixes: code, formulas and diagrams stay left-to-right.
- [x] Question template: `templates/question.md`.
- [x] Example question `0001` (student, easy): rising edge detector — shows a Mermaid
      diagram, a formula, SystemVerilog code and a WaveDrom waveform.
- [x] GitHub Actions workflow: `mkdocs build --strict` on every push / PR, deploy of
      `main` to GitHub Pages.
- [x] Practice mode: solutions, hints and takeaways are collapsible blocks (verified that
      Mermaid, WaveDrom and MathJax render correctly inside them).
- [x] Linked SystemVerilog / Python code tabs (`pymdownx.tabbed` + `content.tabs.link`).
- [x] CSS helpers: array visualisation (`.arr`), inline SVG charts (`.perf-chart`,
      `.viz-legend`) with light / dark colours.
- [x] First batch of questions (all code tested in Python, and in SystemVerilog with
      Verilator / Icarus):

| Id | Title | Level | Difficulty |
|----|-------|-------|------------|
| 0002 | Swap two variables (temp / arithmetic / XOR, with proofs and pitfalls) | student | easy |
| 0003 | What does this code do? (the "surprising" double-loop sort) | student | easy |
| 0004 | Three mislabeled boxes (puzzle + simple and two-swap algorithms) | junior | medium |
| 0005 | Smallest multiple made of digits 0/1 (enumeration vs. BFS on remainders, existence proof, chart) | junior | medium |
| 0006 | Stock max profit, long or short (O(n²) vs. O(n), price chart with running min/max, trace table) | junior | medium |
| 0007 | Random triangle on the unit circle containing the center (Python rejection, SV constraints, P = 1/4 and the discrete M-point formula) | senior | medium |

## In progress

- Waiting for the next batch of questions from the owner.

---

## To do

### Owner actions (one-time)

- [ ] Merge the work branch into `main`.
- [ ] Enable GitHub Pages: **Settings → Pages → Source: GitHub Actions**.
- [ ] Decide whether example question `0001` stays or is replaced by real content
      (it is an RTL design question, so its code is SystemVerilog only).

### Phase 1 — Content

- [ ] Add questions as they arrive (rewrite statement + solution, add diagrams, test the code).

### Phase 2 — Practice experience

- [ ] "Random question" button (optionally filtered by level / difficulty / topic).
- [ ] Mark questions as solved / favourite (stored locally in the browser).

### Phase 3 — Quality and convenience

- [ ] Statistics page: number of questions per level / difficulty / topic.
- [ ] Check for broken image links in the build.
- [ ] Custom site logo / favicon.
- [ ] Hebrew-aware search (the built-in search tokenizes Hebrew by whitespace only).

### Future ideas (not committed)

- [ ] Export a filtered set of questions to PDF for offline practice.
- [ ] "Related questions" links between questions that share tags.
- [ ] Bilingual (Hebrew / English) content.

---

## Technical notes for whoever continues this work

- Build: `pip install -r requirements.txt && mkdocs build --strict`. Versions are pinned
  (MkDocs 1.6.1, Material 9.7.7); Material warns about MkDocs 2.0 — do not upgrade MkDocs
  to 2.x, its plugin system (and therefore the hook and the tags plugin) is gone.
- Navigation is **not** written in `mkdocs.yml`; it is generated in `on_config` of
  `hooks/questions.py` from the files in `docs/questions/<level>/`.
- The `level` field must match the folder name; ids are unique across all levels and
  the file name must start with the zero-padded id.
- External scripts (MathJax, WaveDrom) load from `cdn.jsdelivr.net`; Mermaid is loaded by
  Material itself from `unpkg.com`.
- Images go in `docs/assets/images/`, named `<id>-<short-description>.<ext>`.
- Code, comments, commit messages and repo documentation are in **English**; question
  content is in **Hebrew**.
- Verilator 5.020 (Debian) gotchas found while testing: it does not reset an automatic
  function's local queue between calls inside a loop (an LRM-correct function returned
  wrong results), and it rejects `ref` arguments that are queue elements when inlining
  (use `/*verilator no_inline_task*/` in the test harness). Icarus does not support `ref`
  ports or `break`. Verilator 5.020 also cannot run `randomize()` with constraints on arrays
  (question 0007: the class logic was tested without the solver). Cross-check SV answers
  on more than one simulator.
- Figures for 0006 / 0007 are inline SVG generated by small throw-away Python scripts and
  styled by the `.perf-chart` / `.figure` classes in `extra.css`. Do not put Hebrew inside
  MathJax (`\text{...}`): it renders reversed. Keep Hebrew in the surrounding sentence.
- Update the **Done / In progress / To do** sections of this file at the end of every session.
