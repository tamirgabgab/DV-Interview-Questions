# HANDOFF archive, part 4

The backlog that the owner cancelled on 2026-11-21 (session 35), moved here whole from
"Open items" of `HANDOFF.md` as it stood that day: the weight audit's proposals that were
not done (N11.2, N11.4, N11.6 and the 14 pages over 8,000 elements), the unticked tasks of
"Next steps (session 35)" (the rest of round 6, N4.4, N9.2 to N9.5, the hardware and DV
additions the owner had deferred in round 8), the three boxes still over 1000 px, the
ponytail-audit findings, the flaky checks, the content notes and the items left from the
review rounds of session 34. Nothing here is a task any more: a new review and plan
replaced it ([`PLAN.md`](PLAN.md)). It is kept as a record, and as a place to look before
proposing something again. The items that wait on the owner alone were kept in
`HANDOFF.md`.

---

### N11, the weight audit's proposals (work log 225; 1, 3 and 5 done in 226)

1. **Big DOM from the math (done, 226):** every page is under 12,000 elements; 0016 is
   11,889. Left: 14 pages between 8,000 and 10,450 (0094, 0044, 0087, 0021, 0070, 0069,
   0071, 0101, 0068, 0013, 0048, 0052, 0096, 0095) warn; cut them when they are next
   edited, with the rules of the weight paragraph in `CONTRIBUTING.md`.
2. **The question stylesheet:** `site-question.css` is 60 KB gzip and about 87% of it is
   unused on a given page; a split by feature (code, figures, run panel, boxes) would save
   about 50 KB on a first visit (it is cached after that).
3. **Unminified own scripts (done, 226):** `explorer/core.js`, `reading-tools.js`, `question-tools.js`
   and the others, about 20 KB gzip to save with a minify step in the build.
4. **Scripts at the end of the body delay the first paint** (Lighthouse counts about 1.8 s
   on a simulated phone). `defer` would let parts move while loading, against the
   "nothing moves" rule; only per script, with `check_jumps.py` and the load-shift check.
5. **graph.html (done, 226)** (the map, written by graphify): text at 2.28:1 contrast in its side
   panel, no `main` landmark, no meta description; a post-processing step in
   `tools/build/graph.py` can fix all three.
6. **Code blocks with line numbers** are tables without a caption (axe
   `table-fake-caption`, Material's markup) and a target-size note on desktop: minor.

### Next steps (session 35, 2026-11-19)

The owner asked for a review of the site and of this file and for the next steps as tasks
for the coming days. Every number below was measured in session 35 on a local build of
dd9e984 (work log item 212). N1, N5 and N6.1 to N6.11 are done (work log 213 to 215);
the order is the proposed order of work. Sizes: S up to an hour, M half a day, L a day or more.
[`ROUNDS.md`](ROUNDS.md) groups these tasks into eight rounds with the questions to settle
with the owner before each; go through it with the owner round by round.

**N1. Housekeeping first (S each, one short session):**
- [x] N1.1 (done, work log 213) The weekly workflow is red since 2026-11-16 (run 43904002880, external-links):
  "269 checked, 1 broken, 82 refused the robot". The one broken link is the site's own
  canonical URL of 0006, which answered 503 once; the 82 refusals are all the per-page edit
  links on github.com (429). `check_links.py` `fetch()` returns a 5xx at once (only 403,
  404, 405, 429, 500 and 501 on HEAD go on to GET, and nothing is retried). Fix: retry a
  5xx or a network error twice with a pause; do not fetch URLs under `site_url` (the
  internal check covers them) and fetch one `/edit/main/` link, not one per page.
- [x] N1.2 (done, work log 213) Issue 4 (opened by the weekly workflow, 2026-11-16): Verilator v5.054 is out.
  Bump `VERILATOR_REF` in deploy.yml to the tag and `VERILATOR_RELEASE` in weekly.yml, run
  every testbench (0011 and the 0014 subclass are the two that needed the development
  commit), then close the issue. This also closes the older open item under "Content".
- [x] N1.3 (done, work log 213) This file is 2,600 lines. Move the work log items 112 to 190 and the eight
  "Review round" sections (all done except the lines listed under N7) to
  `HANDOFF-archive-3.md`; keep the decisions, the last twenty work log items, the open
  items and the technical notes.
- [x] N1.4 (done, work log 213) Lock the build. `requirements/site.txt` and `dev.txt` pin six top-level packages;
  everything below them (Jinja2, Markdown, pymdown-extensions, ...) floats. Material for
  MkDocs 9.7 is the last feature line and its promised fixes ran to 2026-11-05 (the team
  moved to Zensical; MkDocs 2.0 drops plugins and hooks). The site is static, so nothing
  breaks today, but a floating dependency can break the build later with no upstream fix.
  Add a full lock (`pip freeze` of a passing CI run, as a constraints file used by every
  `pip install` in both workflows). Not now, only a note: moving off MkDocs means porting
  `hooks/questions.py` (2,200 lines of hook events); try a Zensical build on a copy before
  deciding anything.

**N2. Page weight (M, one to two sessions; no visible change):**
- Measured: every page loads `stylesheets/site.css`, 816 KB (144 KB gzip), not minified
  (120 KB of it is comments), and Chromium's CSS coverage shows 7% of it used on the home
  page, 10% on 0033 with every fold open and 5% on all/. It joins the 31 parts (590 KB) and
  all 54 per-question sheets (242 KB). Every page also loads all 20 site scripts (324 KB
  unminified): home.js, hero-board.js, home-extras.js, maps.js, level-page.js and
  question-filter.js on question pages, question-page.js, run-python.js and video.js on the
  home page. The explorer scripts are already loaded per page by the hook.
- [x] N2.1 (done, work log 217) Minify `site.css` when the hook joins it (comments and white space; a regex pass
  or `rcssmin`, no new build step), and compare the computed styles of the 21 pages of work
  log item 205 before and after.
- [x] N2.2 (done, work log 217) Per-question sheets only on the pages that use them, keyed by box kind, not by
  page id (0044-kapn.css serves 0012 and 0044; 0019 uses 0018's sheet). The hook already
  knows a page's kinds.
- [x] N2.3 (done, work log 217) Split the joined file by page type (core; question page; home, lists and maps)
  and the scripts likewise, added by the hook as the explorer scripts are.
- [x] N2.4 (done, work log 217) Remove the rules the UX round left dead (work log item 209): `how-it-works`,
  `hw-*`, `catalog-link`, `filter-panel`, `topics-*`, `q-meta`, `q-topic`, `mm-tip`,
  `tag-grid`, `tag-chip` (45 uses in the parts; `how-it-works`, `hw-` and `topics-` still
  appear in the hook, the scripts or the pages, so check each name before removing) and
  their pairs in `check_contrast.py`.
- [x] N2.5 (done, work log 217) A budget in `check_phone.py` beside the HTML weight: CSS and script bytes
  fetched per page, a warning over the number N2.1 to N2.3 reach.

**N3. Found by a search engine and shared (S to M):**
- [x] N3.1 (done, work log 216) All 109 question pages carry the same `<meta name="description">` (the site's).
  Write it per page from the statement's first sentence (the search text the hook already
  builds, TeX removed), about 150 characters.
- [x] N3.2 (done, work log 216) No structured data. Add JSON-LD per question (`LearningResource` with the level,
  the topics and `inLanguage: he`, and a `BreadcrumbList`), written by the hook.
- [x] N3.3 (done, work log 216) `sitemap.xml` gives every page the build date as `lastmod`; use the page's
  `added` date or its last commit date.
- [ ] N3.4 (prepared, work log 216: `extra.google_site_verification`) Owner: register the site in Google Search Console (a verification meta tag in
  `overrides/main.html`) and submit the sitemap; a project site cannot serve its own
  `robots.txt`. Then check on the live site that the social cards (`og:image`) are there:
  local builds switch them off.

**N4. What the collection holds (the owner decides, then L):**
- Measured from the front matter: by kind, code 41, math 28, puzzle 17, dv 12, design 11,
  so 23 of 109 questions are DV or hardware on a site named for DV interviews. Tags: uvm 2,
  sva 2, coverage 3, assertions 1, cdc 1, fifo 2. The home page's level cards promise
  "UVM מתקדם, SVA, סגירת כיסוי, דיבאג" for senior and "יסודות UVM, כתיבת טסטים ו-checkers"
  for junior; there is no debug question at all. "Question variety" below has said so
  since session 27 (UVM in depth, debug, verification planning).
- [ ] N4.1 (a pilot of two done, work log 218: 0110, 0111) Proposal: a DV-core round of about ten questions. Candidates: "find the bug"
  pages (a short buggy RTL block or testbench with its waveform; the WaveDrom viewer of
  item 113 fits), UVM factory overrides, sequences and virtual sequences, phases and
  objections, RAL; SVA beyond the handshake (overlapped against non-overlapped
  implication, `$past`, `disable iff`, a liveness bound); coverage (crosses, `ignore_bins`,
  transition bins); CDC (two-flop, pulse and handshake synchronizers); a verification plan
  for a small block (FIFO, arbiter). Ask the owner which, as always.
- [x] N4.2 (done, work log 216) Or, and at least: reword the level cards so they describe what is there.
- [x] N4.3 (done, work log 216) Difficulty tells little: 84 of 109 are "medium" (junior: 1 easy, 64 medium,
  4 hard), so the difficulty filter, the interview builder and the lists' dots barely
  separate questions. Proposal: a re-grading pass with the owner's criteria (front matter
  only; the lists and the catalog follow).
- [ ] N4.4 Levels: student 14, junior 69, senior 26. New questions for the student shelf
  would balance it; X377, X378, X385, X389, X392, X403 and X404 in
  `HANDOFF-archive-2.md` are student-level proposals not yet used.

**N5. The question header on a phone (S):**
- [x] (done, work log 215) At 390 px the chip row of the header wraps on 92 of 109 pages, and on 64 of them the
  second row holds only one or two icons (the box button, the "tested" check); the "השאלה"
  heading starts at a median of 514 px of an 844 px screen (min 412, max 555; measured with
  the sandbox's fallback font, so check with Rubik on the live site). This is the offer of
  work log item 210 that was not answered: the kind chip as an icon only on a phone, or
  the "tested" check moved into the meta line.

**N6. Front-end audit (impeccable audit, web-design-guidelines, ui-ux-pro-max):**
A read-only subagent followed impeccable's `audit` (14 of 20: accessibility 3, performance
2, theming 3, responsive 3, implementation 3; the detector binary was not run), the Web
Interface Guidelines (fetched) and ui-ux-pro-max's UX rules, at 1440 px light, 390 px dark,
820 px, 200% zoom and forced colours, where the CI checks do not look. The lead checked
the file references; the measurements are the subagent's and are to be reproduced before a
fix. Its scripts and screenshots were in the session scratchpad (audit-fe/), not kept.
Note for every browser check: the site's scripts go still when `navigator.webdriver` is
true, so CI never runs the motion paths or a box's first-visit guide.
- [x] N6.1 (done, work log 214; P1, S) The run panel's editor traps the Tab key (WCAG 2.1.2): inside
  `.cm-content` Tab and Shift+Tab never leave; only Esc then Tab does, and the panel names
  only Ctrl+Enter. The fallback textarea (`run-python.js:227`) swallows Tab with no way
  out. 98 pages. Fix: a visible hint with `aria-describedby`, and Esc blurs the textarea.
  `check_keyboard.py` walks the page before the panel opens; add the case.
- [x] N6.2 (done, work log 214; P1, S to M) `fitNav` / `fitWords` (`reading-tools.js:615`, `719`) write and then
  read `scrollWidth` for each of about 135 navigation titles on every load, also when the
  drawer is closed: 815 layouts on the home page and 826 on 0033 at 390 px (64 and 71
  without the first call), about 0.7 s of blocked time at a 4x slower CPU. Fix: skip while
  the sidebar is not shown, and read all widths before writing.
- [x] N6.3 (done, work log 215; P2, S) The phone header's meta line (`.qh-bottom`, `29-question-ux.css:76`) is
  one `nowrap` line with an ellipsis that opens only on `:focus-visible`, so a touch reader
  cannot open it: cut on 109 of 109 pages at 390 px, a tag hidden or cut on 98, and on 90
  pages neighbouring Latin tags show in swapped order (the "·" of "Python" away from its
  word). Fix: `unicode-bidi: isolate` on `.qh-tag`, and let the line wrap on a phone.
  Do it with N5.
- [x] N6.4 (done, work log 215; P2, S to M) The home page shifts on a tablet (CLS 0.14 at 820 x 1180): the
  builder `.hh-builder` ships `hidden` (`hooks/questions.py:1061`) and home.js shows it
  after load; the hero grows from 720 to 1274 px. Fix: render it shown, or keep its height.
- [x] N6.5 (done, work log 215; P2, M) Every question page jumps about 67 px at about 0.7 s when
  reading-tools.js builds the part row `nav.part-nav` (CLS 0.03 to 0.075 at three widths
  on 0033, 0023, 0040). Fix: the hook writes the row, or the page keeps its height.
- [x] N6.6 (done, work log 214; P2, S) Forced colours (Windows high contrast): the `.ui-ico` icons are a mask
  over `background-color` (`09-redesign.css:30`), so the five question tools, the play
  buttons and the hero's pause show as empty circles; the joined CSS has no
  `forced-colors` rule. Fix: one `@media (forced-colors: active)` block.
- [x] N6.7 (done, work log 214; P2, S) `anchor_linenums` (`mkdocs.yml:100`) makes every code line number a link
  and a tab stop: 48 more stops on 0033, 101 on 0023, each 16 by 18 px (axe `target-size`
  at 1440 px, 25 to 97 nodes a page). Fix: `tabindex="-1"` on them, or the option off.
- [x] N6.8 (done, work log 214; P2, S) Fields under 16 px on a phone, so iOS zooms the page on focus (from the
  computed sizes; not tried on a device): the filter of all/ (14.4 px, its selects 14),
  the boxes' `.ex-num`, `.ex-seed` (14), `.ex-addr`, `.ex-len` (15) and selects (12.8), the
  run panel's editor (14.4). Fix: `max(16px, ...)` under `(pointer: coarse)`.
- [x] N6.9 (done, work log 214; P2, S) The sticky header and part row take 111 px whatever the screen's
  height: 31% of 640 x 360 (200% zoom of 1280 x 720) and 28% of a phone on its side.
  Fix: the part row does not stick on a short screen (`max-height` query).
- [x] N6.10 (done, work log 214; P3, S) At 1220 px and under (and at 200% zoom) the drawer's button
  `label[for=__drawer]` is not reachable by keyboard; the footer links and Ctrl+K are the
  way around today.
- [x] N6.11 (done, work log 214; P3, S) A box's first-visit guide (`core.js:1057` on): the tip covers the
  figure's axis labels and the focused enlarge button, is last in the box's tab order and
  closes on Esc only with the focus inside it.
- [x] N6.12 (done, work log 217; P3, M) 115 declarations with literal colours outside `01-base.css`, in 13
  files (`09-redesign.css` 44, `21-interview.css` 31); the linter warns only about SVG.
  Move them to variables and widen the lint rule.
- Checked and fine: contrast by axe at three widths in both schemes on ten pages; no
  sideways scroll on any question page at 390, 820 and 1440 px; reduced motion stops every
  animation; no `transition: all`, every `outline: none` has a focus style; the quick jump
  on a phone; boxes at 820 px; MathJax typesetting moves nothing.
- Not checked: the video dialog (no page has a video), the service worker, web fonts
  (blocked in the sandbox), real devices and screen readers, drag gestures by touch.

**N9. Found in rounds 2 and 3 (session 35), not fixed:**
- [x] N9.1 (done, work log 217; P1, L) MathJax lays the math out after the load: the raw TeX shows first, then
  the lines re-wrap, and a word that moves to another line counts as a large shift. Layout
  shift at 820 px: 0.20 on 0061, 0.26 on 0070, 0.25 on 0104 and 0006 (0.001 to 0.004 with
  MathJax cut off), 0.04 to 0.11 at 390 px; 29 of 131 pages were over 0.1 at 820 px. The fix
  is math rendered at build time (MathJax in Node writing CHTML into the page, or KaTeX),
  which also drops the MathJax download from the pages; it belongs with round 4 (page
  weight). Ask the owner before choosing the renderer: the pages' TeX must render the same.
- [ ] N9.2 (P3, S) The quick jump's "#" button is added to the site header by a script and
  moves the title 48 px (0.0008).
- [ ] N9.3 (P3, S) At 820 px something of about 33 px is added above the first hint after
  the load (0.008 on 0033 and 0040; `details.tip` moves down, `details.success` up).
- [ ] N9.4 (P3, S) The four newest questions (the "new" badge with its word) still wrap the
  phone header's chip row; 11 pages have a meta line of three lines.
- [ ] N9.5 (P3, S) axe `target-size`: one node a question page, the level chip of the
  header (`a[title]`), at 1440 px.
- [ ] N9.6 (owner) N6.8 on a real iPhone: focus a box's number field and the lists' filter;
  the page must not zoom.

**N7. Carried over from earlier sessions (still open, see the sections below):**
- [x] (done, work log 219) 0036: the LFSR box is 1508 px at 1920 x 1080 and the page's review
  items (part b step 3 reduces modulo the wrong polynomial, hint 2, the proof's bit order).
  The RTL module, SVA and state coverpoint were left out by the owner's choice (round 8).
- [x] (done, work log 220) Boxes taller than one screen: 0019 (1201 px), 0048 with the reflection on (1120,
  1221 in free-stops mode), 0012's kapbase boxes (1091, 1093); the cake boxes have 7 px of
  margin. The 24 other boxes over 1000 px are N10.
- [x] (done, work log 220: the axes) Figure labels under 11 px on a phone (0028, 0044 first).
  Other labels (legends, a line's name) keep the 9.5 px floor.
- [x] (done, work log 220) The NBSP before a colon on the older pages (round 5, R0), and a lint rule for it.
- [x] (done, work log 220) 0087: the rim of a lit bulb in the dark scheme (1.3:1).
- [x] (done, work log 216: graphs, topological-sort, trie; LPM is the question itself) Topic names for graphs, topological sort, trie and LPM in TOPICS (0102, 0103).
- [x] (done, work log 220) 0004's Mermaid flowchart shows "?" first in two labels.
- [ ] Hardware and DV additions not done by the owner's choice in round 8: 0014 a
  covergroup, 0012 an exhaustive BCD check, 0044 and 0002 per-clock tables and SVA.
- [ ] Flaky: check_inputs on 0101 (once, 2026-11-14).
- [ ] Owner: the giscus ids, the YouTube links of the videos.

**N8. CI time (optional, M):**
- [x] (done, work log 220: eight shards) The full lane takes 34 minutes (run 43644406759): tests 11, the phone check 12, and
  four explorer shards of about 22 each (clicks 10 to 12, jumps 4, inputs 5), which set the
  total. Options: eight shards, or on a branch run only the boxes of the kinds a push
  touched (the full set stays on `main`).

**N10. Boxes still taller than one screen (found in round 9, a proposal for a later round):**
- [x] (done, work log 221; 0064, 0024 and 0066 part c stay over 1000 px) 24 boxes of 11 kinds are over 1000 px at 1920 x 1080 in check_heights' states (they
  were before round 9 as well): 0066 intervals 1479 / 1280 / 1140, 0024 credits 1352, 0064
  weights 1322 / 1223 / 1182, 0067 netdelay 1258 / 1258 / 1244, 0025 acknak 1250, 0009
  boxes 1240, 0068 twoheaps 1228 / 1213 / 1137, 0043 horses 1220 / 1186, 0065 islands
  1186 / 1186 / 1159, 0062 tagpool 1136 / 1054, 0047 rainwater 1083 / 1082. Each needs
  its own layout (`cols` and its side blocks), as 0019 and 0048 got in round 9.
- [x] (done, work log 221) Phone labels other than the axes (a line's name, "T ≈ 0.333", "D = 5") keep the
  9.5 px floor; 11 px for them needs room per generator.

### Owner decisions

- [x] Staff level removed (session 19, owner's call). Senior has nine questions (0007, 0011, 0019, 0020, 0021, 0023, 0024, 0025, 0037).
- [ ] Fifth series: W1 to W4 done on the branch (W348's drawn check mark not picked); W5 not picked; `main` when the owner asks.
- [ ] Pick rounds from the proposals (now in `HANDOFF-archive-2.md`): the owner's current direction is the eighth series, S1 to S6 (improve what exists, no new questions); the question proposals X360 to X410 wait; the older proposals are in the archive.
- [x] (done: the pages in ae7b115, the generated figures in work log 220) Colons: many pages and explorer strings put a plain space before a colon in Hebrew text (0065 to 0067 and their boxes have no NBSP at all), and the linter does not check it. The owner chose not to fix it for now (2026-10-30). The explorers were fixed and linted in round 4 (session 34); the pages remain (round 5, R0).
- [ ] Comments: enable Discussions, install the giscus app and paste the two ids into `mkdocs.yml` (README, Comments); until then question pages have no discussion section.

### Audit findings (ponytail-audit, session 34, 2026-11-14)

All fixed: A1-A3, A6, A7 in work log 203, the rest in 204.

A read-only audit of the whole repository (three auditors: CI and build, browser code, checks
and tests; each finding was reproduced, the lead re-read the code of the main ones). The owner
asked to fix 1, 2, 3, 6, 7 first, then the rest. Scratch evidence was in the session's
scratchpad (audit-ci, audit-web, audit-checks), not kept.

Must fix:
- [x] A1. The fast lane compares with the previous push (`github.event.before`,
  `deploy.yml:75`), not with the last commit that passed: push A breaks code and its run fails
  or is cancelled, push B fixes prose, B takes the fast lane and A's code deploys untested. The
  same hole lets main's "verified" shortcut (`deploy.yml:56-58`) skip the checks for a branch
  commit that passed only through the fast lane. Fix: base = head_sha of the last successful
  push run of deploy.yml on the same branch; none means the full lane.
  Done (work log 203): every passing run now covers the diff since the previous passing run
  on its branch, so the "verified" shortcut only reuses a fully checked chain.
- [x] A2. `text_only.protected()` strips indentation (`text_only.py:74`): moving a closing fence
  of an indented SV tab to column 0 counts as prose (127 such one-line edits; on 0005 the fast
  lane passed and `--sv-only` failed). Fix: `rstrip()`. Done (work log 203).
- [x] A3. An endless printing loop in the run panel floods the main thread
  (`py-worker.js:18-19`, `run-python.js:85`): at 20,000 lines/s Stop was not handled in 120 s.
  Fix: cap the output per run in the worker (about 200,000 characters, then one "output cut"
  line, then stop posting). Done (work log 203): 2,000 lines or 200,000 characters.
- [x] A4. check_contrast tests only the first fill of 31 entries whose list has no
  `CARD, PAGE` prefix (64 tints per scheme never measured; none fails today): 0080 felt
  (:105-109), 0086 (:333-334), 0092 (:392-395), 0101 (:525), 0102 (:533). Fix: write them as
  `[CARD, PAGE, *tints]` and raise in `check()` when an opaque layer sits above another one.
- [x] A5. Older figure tests compare part of the generated copy: 0008 (3 perf-chart SVGs never
  compared), 0009 (27 of 30 lines), 0010 (its table), 0024 (the table twice, one copy free),
  row checks in 0016, 0017, 0023 (extra or reordered rows pass). Fix: gen markers + blocks() +
  assert_figures_match.

Should fix:
- [x] A6. `text_only.py:113` diffs with rename detection: `git mv docs/javascripts/py_run.py
  notes/` reads as "only files outside the site". Fix: `--no-renames`. Done (work log 203).
- [x] A7. check_jumps collects page errors and never reports them (`check_jumps.py:142`): a box
  that throws at its 4th step printed ok. Fix: the line of `check_inputs.py:270`. Done (work log 203).
- [x] A8. `tests/tools/test_search_text.py:60` (statement without TeX) always skips in CI (the
  test job has no built site). Fix: run it in the build job after `mkdocs build`.
- [x] A9. lint_pages does not require the skeleton (a page with no hints, solution, traps or
  follow-ups lints clean) and `lint_followups` misses `???+ followup`; dead `if ...: pass` at
  `lint_pages.py:321-322`.
- [x] A10. The SV cache keeps whole obj_dirs (two 88 MB PCH each) and never prunes: 7.1 GB
  locally, only `obj_dir/sim` (176 MB in all) is reused (`run_tests.py:103-116`,
  `deploy.yml:148`). Fix: keep only `sim` after a compile; prune unused folders on a full run.
- [x] A11. "Reset all" in a box adds one more MutationObserver per reset (`core.js:874`) and
  explain panels stay in PANELS (`core.js:418`): 0017 went from 11 to 61 callbacks per step
  after 50 resets. Fix: disconnect the old observer; drop a render whose panel is gone.
- [x] A12. Saved side-column widths are not clamped on load (`layout.js:72`): at 1300 px the
  page column was 344 px instead of 600 until a resize. Fix: run the resize fit once on load.

Nice to have:
- [x] A13. `search_text._convert` crashes the build on a trailing `\ ` or an unclosed
  `\sqrt[` in a statement, without naming the page.
- [x] A14. `pages: write` and `id-token: write` are workflow-wide (`deploy.yml:18-22`); move
  them to the deploy job.
- [x] A15. `docs/graph.html` lacks 0101-0109 and `graph_concepts.json` covers 74 of 109
  questions; nothing checks it.
- [x] A16. Nine SV blocks on pages are never compiled; 0004's `typedef string labels_t[3]` is
  copied by hand into `tests/0004/tb.sv:2`. Fix: `//@page`.
- [x] A17. `overrides/404.html:28` `decodeURIComponent` throws on a cut escape, which stops the
  404 script.
- [x] A18. Dead code: `bitsOf` redefined in `lpmtrie.js:148` (core.js has `lib.bitsOf`);
  unused exports `bilFold`, `chompEat`, `nimLegal`, `ihStep`.

### Flaky checks

- [ ] check_inputs on 0101 (sicherman box 0, the first face field): "a click does not focus the
  field" failed once in CI (run 43575254032, 2026-11-14), passed on the rerun and five times
  locally. Watch it; if it repeats, look at the click target of `sc-face` in CI's viewport.

### Content

- [ ] Add questions as they arrive (rewrite, translate code, execute, draw figures).
- [ ] Algorithms proposals not chosen (2026-11-13): LRU cache in O(1) (hash + doubly linked
  list; true LRU needs ceil(log2 N!) bits: 5 for 4 ways, 16 for 8; matrix vs tree PLRU) and
  Bloom filter (m/n = 8, 10, 16 give k = 6, 7, 11 and false positives 2.2%, 0.82%, 0.05%).
- [x] (done, work log 220) 0087 lights out: the dark rim (--viz-ink) of a light that is on is 1.3:1 against the
  amber bulb in the dark scheme (found when check_contrast began testing the fills after
  CARD, PAGE). The bulb still shows by its amber fill on the dark card; a darker rim in the
  slate scheme would fix it. Not changed without the owner.
- [ ] TOPICS (hooks) has no names for graphs, topological sort, trie or LPM; 0102 and 0103 use
  the closest tags. Add topic names if the owner wants them.
- [ ] Candidate the owner liked (2026-11-07), not yet chosen to implement: check digits, ISBN-10
  against Luhn. ISBN-10 (weights 10..1, mod 11) catches every single-digit error and every
  swap of two digits, since (i − j)(b − a) is never 0 mod the prime 11; Luhn (mod 10, the
  Israeli ID number uses it) catches every single error and every adjacent swap except
  09 ↔ 90. Generalization: no weighted sum mod 10 catches both kinds (the weights must be
  units, 1 3 7 9, and the difference of two of them is even, so not a unit); Verhoeff /
  Damm do. The same-style list offered with it: EAN-13 (weights 1, 3, misses adjacent swaps
  of digits 5 apart), IBAN mod 97, Damm / Verhoeff, the Internet checksum against Fletcher,
  RAID 5 / RAID 6 recovery, Hamming (7,4) and SECDED, CRC as polynomial division.
- [x] ~~Explorer state outside the controls is not in the box link or the remembered state~~ (done in session 22 with `box.dvqExtra`, work log item 33)
  (code review, session 22): the hand-made cuts in 0020 and the dragged sandbox shapes in
  0014 come back as the greedy split and the start positions after a reload or from a
  copied link. Give these boxes an `opts.state` codec like the five boxes that have one,
  or mirror the state in a hidden input.
- [x] ~~Re-run the 0007, 0011 and 0014 constraints in a simulator with full constraint support~~ — done in session 5 (Verilator snapshot + z3 in CI).
- [x] ~~Wide data tables still scroll sideways on phones~~: tables of five or more columns that do not fit become cards on phones (C192, session 22).
- [x] ~~0038: the checker missed an ack in the rise cycle~~ (fixed, work log item 151).
- [x] (the axes at 11 px, work log 220; the other labels keep 9.5 px) Figure labels under 11 px on phones (work log item 148): the D194 fit raises them to 9.5 px only; 11 px needs fewer value labels and more room in `charts.py`'s `tick` and `legend` and per generator (0028, 0044 first).
- [x] ~~When a Verilator release newer than 5.052 is out, bump `VERILATOR_REF`~~ (v5.054, session 35, work log 213).

### Still open from the review rounds (session 34)

The eight review rounds are in `HANDOFF-archive-3.md`; these are their items that were
still open when they moved (session 35), each marked with its round.

- [x] (done, work log 220) (round 4) 0019's hourglass box is 1201 px at 1920 x 1080 (it shares 0018's stylesheet now).
- [x] (done, work log 220) (round 4) 0048's farm box with "הצגת השיקוף" on is 1120 px (1221 in free-stops mode); check_heights
  measures the default state only.
- [x] (done, work log 220) (round 4) 0004's mermaid flowchart: "איזה צבע יצא?" renders with "?" first, and "צבע הכדור עובר
  ל-k" breaks around "-k" (Mermaid's RTL layout).
- [x] (no conflict: 10rem is 220 px at the 22 px rem of 1920 px) (round 4) stylesheets/27-box-columns.css sets `max-width: 10rem` on `.ex-controls input[type=range]`,
  but the motorcycle box's sliders measure 220 px: check which rule wins.
- [ ] (round 5) Not done by the owner's choice (R3): 0038 bind / cover / req at reset release, 0058's
  per-clock table and end-of-test check, 0059's parity assertion, 0070's Lee router, 0087's
  per-clock table and SVA, 0090's network-diameter sentence.
- [ ] (round 5) 0038's violations WaveDrom was checked only as source (the CDN script is blocked
  locally): look at it on the live site.
- [ ] (round 6) 0057 part d (the ring) has no box (the owner: not now).
- [ ] (round 6) 0020: a 4 KB request at MPS 128 with the splits map opened measures 1012 px (a state,
  not the default); 0046's box with a 16 x 16 grid is 1234 px, as large grids always were.
- [ ] (round 6) Not done: 0046's histogram bars in rectangle mode (optional, would add height); 0076's
  marker for where f(n) lands (optional); 0020's "draw" button.
- [x] (done, work log 219) (round 7) 0036 `lfsr`: 1508 / 1612 (5 bits); every state over. Proposal: one ring in cycle
  order, the proof panel folded, the strip in the side column, the table capped at 8 rows.
- [x] (done, work log 219) (round 7) 0036: part b step 3's "x^5 = x^2 + x" is modulo x^4+x+1, not the step's x^4+x^3+1
  (x^3+x+1); hint 2's "at most the lcm of the factors' periods" fails on its own
  (x^2+x+1)^2 (lcm 3, period 6); the proof's "a step is multiplication by x up to bit
  order" is false for 3 or more taps (the periods still equal the order of x); the box's
  "the 1 of the polynomial is always a tap" contradicts the page; the XNOR trap holds only
  for an even tap count.
- [ ] (round 7) 0036: no RTL module, no SVA (the trap describes one in words), no state coverpoint.
  Not done by the owner's choice (round 8, 2026-11-20).
- [x] (done, work log 219) (round 7) 0036: every item above (R1 step 3, hint 2, the proof's bit order, the box's "the 1 of
  the polynomial", the XNOR trap; the box 1508 / 1612 px; the RTL module, SVA and coverage).
  Two agents reached 1003 to 1129 px with one ring in cycle order and the table scrolling;
  their work is in b6aeb23 and the handoff notes of the session scratchpad (lost with it).
- [x] (already fixed in session 34: 869 px at most) (round 7) 0012's kapbase boxes are 1091 and 1093 px (not part of this round).
- [ ] (round 7) check_heights.py should click `.wj-best` before "סוף" (0083) and cannot reach the
  extreme states (a long game, help open, a law select used); the agents measured those with
  their own scripts.
- [x] (done, work log 220: `ltr-nw`) (round 7) Site-wide: an LTR tuple "(a, b)" in prose can break after the comma (0013 got U+00A0);
  a shared nowrap rule for short LTR spans would fix it everywhere.
- [x] (done, work log 220) (round 7) The cake boxes' worst state is 993 px (7 px margin): `.cake-scroll` max-height 7.6rem
  -> 6.7rem would save about 20 px.
- [ ] (round 8) 0014: a covergroup on n, the side and the pair relation (apart, edge, corner).
- [ ] (round 8) 0012: an exhaustive 1,000-input BCD check, two assertions, coverage on d and d -> d'.
- [ ] (round 8) 0044: a per-clock table for 211, SVA and coverage, the closed form as the scoreboard's
  reference.
- [ ] (round 8) 0002: a per-clock table and an SVA in the non-blocking swap follow-up.
- [ ] (round 8) 0051: a two-line "how to verify" (the exhaustive round trip the tb runs). 0008, 0073,
  0095: none needed.
- [ ] (round 8) Review scripts: register Playwright's abort-all route before the CDN routes (the last
  registered route wins; MathJax was blocked in some reviewers' measurements).
