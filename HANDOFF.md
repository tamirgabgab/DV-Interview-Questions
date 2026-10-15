# HANDOFF

Living task list for this repository: what was done, what is in progress, and what comes
next. Update it at the end of every work session so anyone (human or AI) can pick up
where the last session stopped.

_Last updated: 2026-10-15_

---

## Project goal

A web interface for a personal collection of Design Verification (DV) interview
questions. Each question is written clearly, with a full readable solution and diagrams
where relevant, and is classified by **position level** (Student / Junior / Senior /
Staff), **difficulty** (Easy / Medium / Hard) and **topic tags**.

Workflow: the repository owner sends questions + solutions (text and sometimes images)
during the week; each one is rewritten in a clean, consistent format and added to the
requested place in the repository.

---

## Done

- [x] Initial `README.md`: purpose, classification scheme (level / difficulty / tags),
      planned repository layout, question file format, diagram conventions.
- [x] `HANDOFF.md` (this file).

## In progress

- Nothing yet.

---

## To do

### Phase 1 — Content foundation

- [ ] Confirm the classification scheme with the owner (open decisions below).
- [ ] Create the folder structure: `questions/{student,junior,senior,staff}/`,
      `assets/images/`.
- [ ] Add a question template file (`templates/question.md`) matching the README format.
- [ ] Add the first real questions as they arrive.
- [ ] Keep a question index (table of all questions with level, difficulty, tags) —
      generated automatically once the site exists.

### Phase 2 — Web interface (MVP)

- [ ] Choose the site technology (see open decisions). Current recommendation:
      **MkDocs + Material for MkDocs** — renders Markdown directly, built-in search,
      tags, Mermaid support, dark mode, Hebrew/RTL support, minimal maintenance.
- [ ] Site configuration (`mkdocs.yml`), navigation by position level.
- [ ] Filtering by level, difficulty and tag (Material tags plugin + a filter page).
- [ ] Render diagrams: Mermaid (built in) and WaveDrom (plugin) for timing diagrams.
- [ ] Syntax highlighting for SystemVerilog, Verilog, Python, C/C++, TCL.
- [ ] "Practice mode": solutions collapsed by default, revealed on click.
- [ ] GitHub Actions workflow that builds the site on every push to `main` and deploys
      it to GitHub Pages.

### Phase 3 — Quality and convenience

- [ ] Validation script / CI check: required front-matter fields present, valid
      `level` / `difficulty` values, unique ids, image links not broken.
- [ ] Auto-generated statistics page (questions per level / difficulty / tag).
- [ ] "Random question" button for practice.
- [ ] Mark questions as solved / favourite (stored locally in the browser).

### Future ideas (not committed)

- [ ] Hebrew UI or a bilingual (Hebrew / English) interface.
- [ ] Export a filtered set of questions to PDF for offline practice.
- [ ] Related-questions links between questions that share tags.

---

## Open decisions (need the owner's input)

1. **Language of the questions:** English, Hebrew, or both?
2. **Difficulty scale:** 3 levels (Easy / Medium / Hard) or a 1–5 scale?
3. **A question that fits several levels:** keep it in one folder with a
   `levels: [junior, senior]` list, or duplicate it per level?
4. **Site technology:** MkDocs Material (recommended, simplest) vs. a custom web app
   (e.g. React/Vite — more flexible UI, more maintenance).
5. **Visibility:** public site on GitHub Pages, or private?
6. **Source field:** keep the company / interview round each question came from, or omit it?

---

## Conventions for whoever continues this work

- Code, comments, commit messages and documentation are in **English**.
- One question per file, named `<id>-<slug>.md`, ids are unique and never reused.
- Images go in `assets/images/`, named `<id>-<short-description>.<ext>`.
- Prefer text-based diagrams (Mermaid / WaveDrom) over images, so they stay editable.
- Update the **Done / In progress / To do** sections of this file at the end of every session.
