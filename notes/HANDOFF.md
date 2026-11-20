# HANDOFF

Living task list for this repository: what was done, what is in progress, and what comes
next. Update it at the end of every work session so anyone (human or AI) can pick up
where the last session stopped.

_Last updated: 2026-11-20 (session 35)_

**Live site:** <https://tamirgabgab.github.io/DV-Interview-Questions/>

---

## Project goal

A public website for a personal collection of Design Verification (DV) interview
questions, plus math and logic questions. Each question is written clearly in Hebrew, with
a full readable solution and diagrams where relevant, and is classified by **position
level** (Student / Junior / Senior), **difficulty** (Easy / Medium / Hard) and
**topic tags**.

Workflow: the repository owner sends questions + solutions (text, code and sometimes
images) during the week. Each one is rewritten in a clean, consistent format, the code is
translated to the missing language and executed, figures are drawn, and the result is
pushed to `main`, which publishes the site.

---

## Decisions

| Topic                 | Decision                                                                 |
|-----------------------|--------------------------------------------------------------------------|
| Content language      | Hebrew (code, identifiers and repo docs stay in English)                 |
| Visibility            | Public site on GitHub Pages, deployed from `main`                        |
| Topics                | DV topics plus math, probability and logic puzzles                       |
| Site technology       | MkDocs + Material for MkDocs, RTL layout (`language: he`)                |
| Difficulty scale      | 3 levels: easy / medium / hard, relative to the position level           |
| Multi-level questions | One file in one level folder                                             |
| Source field          | Optional `source` field, empty by default                                |
| Code languages        | Python + SystemVerilog, as linked tabs (Python first since 2026-10-29)    |
| Solutions             | Collapsed by default (practice mode); one collapsed solution per sub-part |
| Multi-part questions  | One file, `### סעיף א/ב/ג` with a solution after each part               |
| Owner's own code      | Kept as sent (comments added, minimal bug fixes called out to the owner) |
| Workflow before adding | Ask the owner guiding questions first, then implement                   |
| Tests                 | Python: full tests of the page code. SystemVerilog: Verilator 5.054 (the commit of its release tag, since session 35; a development commit after 5.052 before) built from source with z3, so every class runs as published; a translation by intent (fingerprinted) is allowed only for a proven simulator bug, and none is needed today |
| Failing tests         | Block the deploy; the live site keeps its previous version              |
| Run button            | Per question, Python only (Pyodide in a web worker); SV cannot run in a browser, the panel says it is checked in CI instead |
| Position levels       | Student / Junior / Senior; the Staff level was removed on 2026-10-21 (owner: no staff questions planned) |
| Look and feel         | Own navy + amber palette, logo and footer; level / difficulty as CSS chips; one header card per question (see **Site redesign plan** in `HANDOFF-archive-2.md`) |
| Next rounds (2026-10-27) | Owner: no rounds of new questions for now; only improve the existing questions, the site and its interfaces (series S). The question proposals X360 to X410 stay listed for later |
| Closed (2026-10-27) | Owner: no run panel for questions without Python code, no print style, and 0001 stays as it is; not to be proposed again |

---

## Work log

Sessions 1 to 21 are in [`HANDOFF-archive.md`](HANDOFF-archive.md), sessions 22 to 30
(items 1 to 111) in [`HANDOFF-archive-2.md`](HANDOFF-archive-2.md), with the site
redesign plan of 2026-10-16 and the proposal series six to eight, and items 112 to 191
(sessions 31 to 34) with the review rounds of session 34 in
[`HANDOFF-archive-3.md`](HANDOFF-archive-3.md). The numbered items below start at item
192 (session 34).

192. **Seventh review round: ten more random questions (session 34, 2026-11-10).** Seed
    20261112, the sixty reviewed questions and 0099 left out: 0013, 0017, 0027, 0031, 0036,
    0069, 0074, 0083, 0091, 0098. Five read-only review agents (reports and scripts in the
    session scratchpad, review8/); every box measured at 1920 by 1080 in its default and its
    tallest reachable state. Findings in `HANDOFF-archive-3.md`, "Review round 7 (session 34)".
    Nothing was changed yet.

193. **The seventh ten questions fixed, 0036 deferred (session 34, 2026-11-10/11).** The
    owner's choices: hardware / DV for all six proposals, 0069 keeps three boxes, 0027's box
    drops its second chart (0028's too), and every reachable box state under 1000 px. Seven
    agents; four stopped at the five-hour usage limit and were resumed, then all were stopped
    and replaced by agents at medium effort working from handoff notes (a WIP snapshot,
    b6aeb23, kept the tree safe meanwhile). The owner then gave up 0036 for now (its box was
    still 1003 to 1129 px after two agents): it is back to its state before the round.
    Heights now (worst reachable state at 1920 x 1080, before): 0013 971 (1343), 0017 917
    (1162), 0031 985 (1228), 0027 / 0028 993 (1164 to 1210), 0069 958 (1252), 0074 980
    (1312), 0091 938 (1553), 0083 906 (1734), 0098 883 (1100). Highlights: 0098's legend
    printed literal code; 0091's 8 x 10 board has two winning first moves; 0069's ties
    order was backwards; 0074 writes mn - 2; 0031 B crosses three times, 108 plans; 0017's
    two duplicates; 0027 / 0028's 'formula and bars agree everywhere'; 0013's sorting network
    drawn; 0083's BFS layers. A stray brace in 27-box-columns.css (cake block) would have
    dropped 0039's eggs rule; caught before commit. Page code changed (tell the owner): 0098
    `luhn_sum` keeps only ASCII digits, `luhn_valid` needs a digit, SV `luhn_ok` needs n > 0;
    0031 `bridge([])` still raises KeyError (the owner's code; the statement says one to
    eight people). On main as 4a0b42f (deployed 2026-11-10 22:36 UTC); a crawl of the live site
    (121 pages, 262 links and files) found no 404, and the twelve pages' 23 boxes (0012,
    0028 and 0036 included) built with no script error.

194. **New question 0101: Sicherman dice (session 34, 2026-11-11).** From the owner's
    question (relabel two fair dice, same 2..12 triangle). The lead verified the facts first
    (brute force and generating functions; three dice: only Sicherman with a standard die).
    The owner's choices: junior; parts a (six faces, uniqueness), b (a face 0 allowed, five
    pairs) and c (n faces, another pair exactly when n is composite); different sizes only
    as a follow-up; DV only as a trap in words (a sum-only checker passes Sicherman dice);
    a box `sicherman` (both dice editable, n = 4, 6, 8, the sum table and the histogram
    against the triangle, at most 862 px at 1920 x 1080). Also: subagents now run on the
    session's model and effort (CLAUDE.md, the owner's rule). On main as 4c5699d (deployed
    2026-11-11 10:44 UTC); a crawl of the live site (122 pages, 264 links and files) found
    no 404, and the page's three boxes built with no script error.

195. **0101 part c reworked; CI made robust to an unreachable Ubuntu archive (session 34,
    2026-11-11).** The owner's choice: part c is k six-sided dice instead of n faces (three
    dice first; every die is x(1+x)(1+x+x^2)(1-x+x^2)^e with e <= 2, as the x^2 coefficient is
    2 - e; j Sicherman pairs and k - 2j standard dice, floor(k/2) + 1 sets; with a face 0:
    5, 13, 41, 98, 250 for k = 2..6, no closed form claimed); n faces is a follow-up; the box
    drops its n select (six faces, at most 717 px). The branch CI failed in apt (the runner
    could not resolve azure.archive, then archive and security.ubuntu.com, for hours) and
    the lead fast-forwarded main without checking the conclusion (a mistake: the main CI ran
    the checks and blocked the deploy, the site stayed on 4c5699d). deploy.yml now: z3 and
    Verilator's run-time packages from apt twice (the second time on archive.ubuntu.com),
    then z3 4.8.12 from github.com/Z3Prover/z3/releases (libfl2 is not linked by
    verilator_bin); `playwright install --with-deps` falls back to Chromium alone;
    libcairo2 goes on if the image has libcairo.so.2. On main as 4553951 (deployed
    2026-11-11 17:26 UTC, all jobs green); a crawl found no 404 and 0101's two boxes build.

196. **Eighth review round: ten more random questions (session 34, 2026-11-11).** Seed
    20261113, the seventy-one reviewed questions and 0101 left out: 0002, 0008, 0012, 0014,
    0044, 0051, 0054, 0073, 0094, 0095. Five read-only review agents (reports and scripts in
    the session scratchpad, review9/); every box measured at 1920 by 1080, default and
    tallest reachable state. Findings in `HANDOFF-archive-3.md`, "Review round 8 (session 34)".
    Nothing was changed yet.

197. **The eighth ten questions fixed (session 34, 2026-11-11).** The owner's choices: hardware
    / DV only for 0054 (a block diagram of rr_arbiter, a WRR per-clock table) and 0094 (a
    per-clock table, credit_counter_sva tested with mutations); 0044's kapgraph box moved out
    of the statement into part b; every box state under 1000 px. Five agents, on the
    session's model and effort (the CLAUDE.md rule). Heights now (worst reachable state,
    before): 0014 968 (1487), 0012 989 (1332), 0051 986 (1183), 0044 957 (1144), 0054 972
    (1064), 0094 979 (1008), 0095 915 (987), 0002 727, 0008 929, 0073 914. Highlights: 0008's
    what-if ignored the countries announced before Israel and broke the points balance;
    0054's trap (the bound holds, the share breaks); 0073's odd in-shuffle rule and O(log n)
    stack; 0014's corner check fails for squares too and random_shapes could loop; 0051's
    b = 0 loop (now an error); 0012's histograms and two-digit repdigits; 0044's base-5 sort;
    0002's inout and JavaScript XOR; 0094's NaN for large N in the SV p_full; 0095's
    exhaustive 19-soldier search (DVQ_SLOW=1, about 8 minutes). Page code changed (tell the
    owner if asked): 0051 mice_needed raises for b < 1; 0094 p_full divides by rho^N. On main as ec49ec5
    (deployed 2026-11-12 00:09 UTC, branch CI green first), then the docs commit; a crawl of
    the live site (122 pages, 264 links and files) found no 404, and the twelve pages' 24
    boxes (0003 and 0013 included) built with no script error.
198. **New questions 0102 and 0103: algorithms and data structures (session 34,
    2026-11-13).** The owner asked for new questions in this direction and picked two of four
    proposals (LRU cache and Bloom filter not chosen). 0102 topological sort (junior): Kahn
    with cycle detection, DFS with three colours, the critical path (total 15 on the
    example, E → C → D → F → G); hardware only as a follow-up in words (a scoreboard issues
    one Kahn level per clock); new kind `toposort` (graph edited by clicks or an edge list,
    Kahn stepped, a schedule mode with a Gantt chart), worst state 975 px at 1920. 0103
    longest prefix match (senior): naive scan (the /0 shift trap), binary trie with insert
    and delete, multibit trie with controlled prefix expansion (a stride table for s = 1, 2,
    4, 8), and part d a pipelined trie lookup `lpm_pipe` in SV tested under Verilator against
    the naive model with mutations; TCAM as a follow-up. New kind `lpmtrie` (8-bit prefix
    table, trie drawn, an address walked, stride 1 or 2), worst state 961 px. Two agents in
    parallel on the session's model and effort. 0103's agent corrected its own short answer:
    a /k prefix expands to 2^(s - k mod s) entries, one entry when s divides k (k > 0), the
    whole root for /0. Tags: TOPICS has no graphs / trie names, so the pages use the closest
    (algorithms, sorting, bfs; bitwise, digital-design, protocols); adding topic names is an
    open item.
199. **New questions 0104 and 0105 (session 34, 2026-11-13).** From a later round of
    proposals (the owner rejected merge-k, knapsack, Huffman and two-array median for now,
    and the rain-water / gas-station pair as already in their pool, then asked for an expanded
    write-up of the gas stations and HyperLogLog and picked both). 0104 gas stations on a
    circle (junior): naive, one pass with the skip lemma and the start after the lowest
    prefix sum, every good start (cycle lemma for sum 0, an exact O(n) condition for sum > 0,
    all checked against brute force on 20000 rings); hardware only in words; new kind
    `gasring` (ring, lap step by step, two-lap level chart), 933 px at most. 0105 HyperLogLog
    (senior): exact count, one register, HLL with harmonic mean, small-range correction and
    merge by max (rms error over 200 runs per m checked against 1.04/sqrt(m)), and part d
    `hll_update` in SV with read-modify-write forwarding, the FORWARD = 0 mutant caught under
    Verilator; new kind `hll` (stream, hash and m selects, register grid, error chart), 789 px.
    check_contrast fix: a background list [CARD, PAGE, x, ...] had x under the opaque box
    surface, so 170 tint checks never ran; check() now tests the box and each fill alone.
    It found 0104's step leg (fixed) and 0087's rim (open item).
200. **New questions 0106 and 0107: tricky LeetCode (session 34, 2026-11-13).** The owner
    turned down three more rounds of proposals (common algorithms, DV/hardware-flavoured
    ones, logic/math puzzles, plain LeetCode) and asked for tricky questions with a
    non-obvious answer; picked LeetCode 137 and 179 (perfect squares by Legendre, maximum
    gap by pigeonhole, reaching points backwards and candy in two passes were the others).
    0106 (junior): XOR for twice, a mod-3 counter per bit in ones/twos derived from its state
    table, a bit-sliced counter mod k; kind `thrice`, 971 px. 0107 (junior): the a||b rule,
    the proof by rho(a) = a/(10^|a| - 1), and the smallest number: for every distinct non-zero
    first element, the zeros then the rest ascending, take the least (the lead rechecked it on
    20000 random lists; "first non-zero to the front" fails on [0, 2, 21]: 2102 vs 2021); a
    faster first-element rule is a follow-up marked as checked, not proven; kind `concat`,
    989 px.
201. **New questions 0108 and 0109: tricky LeetCode with generalisations (session 34,
    2026-11-13).** The owner asked for another round with generalisation parts, turned one down
    (equalising an array, trailing zeros of n!, contribution sums, request/response orders,
    nested envelopes, patching an array) and picked LeetCode 995 and 853/1776 from the next
    (integer replacement and NAF, consecutive sums and odd divisors, circular Kadane, task
    scheduler were the others). Both junior, parts a and b only. 0108: the forced greedy and
    uniqueness, O(n) parity, the k x k grid; the ring is a follow-up (g = gcd(n, k) cycles of
    p -> p+k, 2^g or 2^(g-1) solutions, the minimum per cycle with a parity fix; the lead checked
    it by brute force on 3000 cases); kinds `kflip` and `kflip2`, 981 and 960 px. 0109: the
    owner asked how meetings at non-integer times can be ignored; the page answers with
    T_i = max(t_i, T_{i-1}) and the lower envelope of the free lines; part b is the monotonic
    stack of LeetCode 1776; kind `carfleet`, 969 px. 0109 was committed alone first with
    partial staging of the shared files (scratchpad partial_stage.py: HEAD plus only the added
    lines that name the question).
202. **Skills: ponytail and diagram-design (session 34, 2026-11-14).** The owner asked which
    of six GitHub skills fit the project (Impeccable, Ponytail, Humanizer, Scraping, Diagram
    design, Caveman). Impeccable was already installed; Humanizer (English AI-writing tells,
    rewrites tested prose), Scraping (no use here, terms of use) and Caveman (terse replies
    against the owner's Hebrew reply rules) were advised against. ponytail (the six skill
    folders, no plugin hooks) and diagram-design (reference for figure layouts and diagrams
    outside the site) were installed after reading their files; see `.claude/skills/README.md`.

203. **Audit fixes, round 1: A1, A2, A3, A6, A7 (session 34, 2026-11-14).** The fast lane's
    base is now the head commit of the last successful push run of deploy.yml on the same
    branch (`gh api .../runs?branch=&event=push&status=success`), not `github.event.before`; no
    such run, or a commit gone after a force push, gives the full lane. `text_only.protected()`
    keeps indentation (`rstrip`), and the diff runs with `--no-renames`; two tests in
    `tests/tools/test_text_only.py` pin both (a dedented closing fence, a `git mv` into
    `notes/`). check_jumps reports script errors as check_inputs does. The run panel's worker
    stops posting output after 2,000 lines or 200,000 characters and sends one `cut` message;
    the panel then stops the worker as Stop does and writes a Hebrew line (likely an endless
    loop). `test_worker_cuts_endless_output` runs the worker under Node with a fake Pyodide.

204. **Audit fixes, round 2: A4, A5, A8 to A18 (session 34, 2026-11-14).**
    - A4: 41 contrast entries listed opaque fills one over another, so only the first was
      measured; they are now `[CARD, PAGE, *fills]` (each fill and the box surface measured,
      all pass) or drop the hidden layer (the home band's card over its band), and `check()`
      raises on an opaque layer above another one (over the page alone is fine).
    - A5: 0008, 0009, 0010, 0016, 0017, 0023 and 0024 have `blocks()`, gen markers on the page
      and `assert_figures_match`, so every generated SVG, stepper, legend and table is compared
      whole (two subagents; no page block was stale).
    - A8: the build job runs `tests/tools/test_search_text.py` after the build.
    - A9: lint requires a hint, a solution, a short answer, a trap and the follow-ups; the
      follow-up check reads `???+ followup` too. The lint loop reused `text` for an h4 label,
      so the video front-matter check of a page with solution labels read the label; renamed.
    - A10: the SV cache keeps only `obj_dir/sim` (7.1 GB to 120 MB here), and a run of every
      testbench removes unused folders.
    - A11: "reset all" disconnects the scrubber's old observers (10 callbacks a step after 20
      resets on 0017, was 31), and a panel gone with its box leaves PANELS on a tab change.
    - A12: layout.js fits saved column widths on load, not only on resize.
    - A13: search_text takes a lone trailing backslash and an unclosed `\sqrt[`; a failure
      names the page.
    - A14: `pages: write` and `id-token: write` only in the deploy job.
    - A15: 23 new concepts and the 35 missing questions in `graph_concepts.json`,
      `docs/graph.html` rebuilt, and `test_every_question_is_on_the_map`; CONTRIBUTING's
      new-question steps name the map.
    - A16: 0004's page block cannot be pulled with `//@page` (its `draw()` stub would clash
      with the testbench's), so `test_tb_typedef_is_the_pages` keeps the copied typedef equal.
    - A17: the 404 page survives a cut escape; check_404 has the case.
    - A18: lpmtrie uses `lib.bitsOf`; the unused model exports are gone.
    - Both rounds went to `main` together (daab98b, deployed 2026-11-14 14:40 Israel time):
      pushing round 2 cancelled round 1's branch run, and one green run covered both. Live:
      the map has 0109 and the worker has the cap. GitHub Pages answers 400 itself to a path
      with a cut escape ("%E0%A"), so the 404 fix only shows for escapes it lets through.
205. **CSS cleanup: dead rules and overridden declarations (session 34, 2026-11-14).** The
    owner chose dead rules plus duplicates, with no visible change. 22 selectors that name
    a class used nowhere (site HTML, JS, hooks, templates, generators, with the prefixes the
    scripts build) are gone (`.cm-editor` stays: CodeMirror makes it). 97 declarations that
    a later rule with the same selector in the same @media replaces (load order of
    `extra_css`) are gone, 23 rules that were left empty with them, and 4 more that a later
    rule outside any @media replaces (13-motion's M9 skeleton). The square-wave dividers of
    22-circuit.css (off since session 33) are gone with circuit.js's `dividers()`.
    Checked by the computed style of about 60 properties of every element of 21 pages, light
    at 1200 px and dark at 390 px, before and after: no difference except the two collisions
    below and `hr`'s position (no children now). Two class collisions were bugs and are
    fixed: 0001's `.ed-key-now` (blue) overrode 0037's legend key (the step cell is ink),
    now scoped by `.ed-legend`; 0093's `svg.sm-fig .sm-lab` (13 px bold) overrode 0063's
    figure labels, which overflowed the comparator pills; 0093's figure is `svg.sm-match`
    now. 0104's `.gs-note` duplicated 0060's rule of the same name; one rule stays.
206. **A page on how the site is built, with two animated diagrams (session 34,
    2026-11-14).** The owner's choices: a new page linked from the footer and the README,
    two diagrams, animated. `docs/how-built.md`: the CI run of a push (gate, then the lane:
    a code change runs test, then build and explorers; prose only runs quick, then build; a
    commit of main that passed on its branch goes to build; deploy only on main) with lane
    buttons, and how a page becomes the site (generator, fill.py, page, tests, hook,
    explorer scripts, site, checks). `tools/figures/site_flow.py` draws them (diagram-design
    skill's rules adapted: orthogonal r=8 routes, label masks, accent on the run only,
    palette classes, Hebrew `direction="rtl"`); `fill.py` takes non-question pages
    (`PAGES`). The static figure is complete; a decorative SMIL copy draws the run stage by
    stage (6 s cycle), hidden under reduced motion, by the switch over each diagram and in
    print (28-site-flow.css). `tests/tools/test_site_flow.py` checks the page copy, that the
    CI diagram's edges follow `needs` in deploy.yml, and that routes are orthogonal and end
    on their boxes. Phone check (axe, text size) and keyboard check pass on the page.
    Both on `main` (138929e, deployed 2026-11-14 17:17 Israel time), checked live at 1200
    and 390 px, light and dark.
207. **The gate's queries missed passing runs (session 34, 2026-11-14).** The `main` run of
    138929e took the full lane although its branch run had passed: the Actions API's
    `status=success` filter left out that run (and the branch's two latest passing runs)
    over an hour later. Both gate queries (`verified` and the fast lane's base) now list the
    runs without that filter and keep `conclusion == "success"` in jq. On `main` (9272a06,
    2026-11-14): that run was the fix's own test, and took the short lane (gate, build,
    deploy; under 2 minutes).
208. **UX/UI review in three stages (session 34, 2026-11-14).** The owner's prompt: review
    from screenshots (11 pages, 1440 px light and 390 px dark, scrolled to the end) with
    impeccable (critique), ui-ux-pro-max and web-design-guidelines; up to ten ranked
    proposals; a before/after example on one page for the chosen ones; nothing implemented
    before approval. Stages 1 and 2 are done (an independent subagent did impeccable's
    design review, 26/40 on Nielsen's heuristics; its detector needs the owner's permission
    and did not run). The ten proposals, waiting for the owner's choice: (1) a real stepping
    figure in the hero instead of the chip art; (2) the "interactive" chip of a question
    opens and scrolls to its box, and lists mark questions with a box; (3) an end card after
    "solved" and "continue where you stopped" on the home page; (4) one-line list rows with
    the subtitle as a hook, one filter row; (5) drop the "how it works" cards, the lone
    "all questions" section and the previous/next band outside question pages; (6) path
    names on the metro map's lines, a question's title on hover or tap, an edge fade;
    (7) path cards as rows, one sorted tag list; (8) a shorter question header (the tools
    into the sticky strip); (9) an opaque sticky strip and a solution button that does not
    look like a hint; (10) wide tables in solutions scroll or widen. Defects found, not
    fixed yet: a level page's title is "Index" (the header while scrolling and the browser
    tab); the path card "אילוצים ואקראיות ב-SystemVerilog" clips its title to "rilog"; to
    check: a "¶" beside headings on a phone, tiny labels in 0040's FSM figure on a phone.
    Capture note: in the sandbox the site's service worker fetches the CDN scripts itself,
    so MathJax and WaveDrom stay raw on pages loaded after the first; use
    `service_workers="block"` in a Playwright context that routes the CDN to local copies.
209. **The UX round implemented (session 34, 2026-11-14).** The owner saw before/after mocks
    of all ten proposals (injected CSS and DOM, nothing in the repository) and chose 2a, 3a,
    4, 5, 6, 7a, 7b, 8, 9a, 9b and 10, one round, with MCQ answers: no tags in list rows;
    the tools move to the sticky strip on a computer only; wide tables scroll; the end card
    only after "solved" and without a "similar question" line; path rows keep the reader's
    progress; level and difficulty tags apart from the topics; the map's improvement on the
    home page too. Not chosen: 1 (a figure in the hero), 2b, 3b ("continue" already exists).
    Three agents by area, each with its own new stylesheet (29 question page, 30 lists and
    home, 31 maps, paths, tags); the summary of what changed is in CONTRIBUTING ("The UX
    round"). Also fixed: a level page's title was "Index" (now from its header band) and the
    clipped path title (rows replace the cards). Measured: all/ shows 8 rows in the first
    screen at 1440 px (was 2) and is 6305 px tall (was 10717), 10444 px on a phone (was
    18332); the "השאלה" heading of 0083 is at 501 px of 900 on a computer (was 608) and 514
    of 844 on a phone (was 519: the tools keep their row there). Left for later: dead rules
    of the replaced markup in parts 02, 09, 10, 12, 16, 17, 22 (`how-it-works`, `hw-*`,
    `catalog-link`, `filter-panel`, `topics-*`, `q-meta`, `q-topic`, the row stripe,
    `mm-tip`, `tag-grid`, `tag-chip`) and their unused contrast pairs; the metro names'
    width is an estimate without font metrics (check with Rubik on the live site).
    On `main` (a62fb59, deployed 2026-11-14 19:47 Israel time; the main run took the short
    lane). Live check at 1440 px light and 390 px dark on all/, paths/, tags/, the home page
    and 0083: no script errors, no horizontal scroll, and the map's names fit in Rubik.
    Open with the owner: a question page's top on a phone did not get shorter (the box chip
    takes a row of its own); offered to make the chip icon-only there.
210. **The phone header's icons (session 34, 2026-11-14, f49ee03 on `main`).** On a phone the
    box chip and the "tested code" badge show only their icons (the words stay for a screen
    reader) and the id loses its word "שאלה". Only pages with a short kind name gain a row
    (0083: 514 to 479 px; 3 of 19 sampled pages). Offered and not answered: make the kind chip
    icon-only on a phone too, so every page's header gets shorter.
211. **The Manim videos removed (session 34, 2026-11-14).** The owner makes the videos in
    another project and will send YouTube links. Removed: all of `videos/` (30 videos, their
    scripts, captions, scenes, `render.py` and `lib/`, about 500 MB tracked) and
    `requirements/video.txt`. Kept: the YouTube support (`video:` and `video_parts`, the
    "סרטון הסבר" tool and dialog, video.js, 20-video.css). Changed by the owner's answers:
    `video_parts` is now optional on a page with parts too (without it the page has one
    "לסרטון ההסבר" link and the dialog no chapter buttons; the hook gives `[("", 0)]`);
    `check_videos.py` checks only the page fields; `catalog.py` writes the README's video
    table from the pages' `video:` ids; `notes/VIDEOS.md` is now a short how-to. No page has
    a `video:` field yet. Note: the old files stay in the git history (no history rewrite).

212. **A review of the site and of this file; the next steps (session 35, 2026-11-19).** The
    owner asked for a pass over the site and the handoff, with the skills where useful, and
    for the findings as tasks for the coming days. Nothing on the site changed. Done: a
    local strict build of dd9e984; sizes of the built pages, the joined CSS and the scripts;
    Chromium CSS coverage on three pages; screenshots at 1440 px light and 390 px dark; the
    front matter of the 109 pages counted by kind, level, difficulty and tag; the head of a
    built page (description, canonical, structured data); the last CI runs and the open
    issue on GitHub; the pins in `requirements/`; a subagent on the failed weekly run's log;
    a subagent for a front-end audit with impeccable (audit), web-design-guidelines and
    ui-ux-pro-max. ponytail-debt had nothing to list (no `shortcut:` comment in the
    repository) and ponytail-audit was not run again (A1 to A18 of 2026-11-14 are fixed).
    The tasks are under "Open items", "Next steps (session 35)", N1 to N8. This file's
    header date and "In progress" were stale (session 33) and are current again.

213. **Round 1 of the session 35 plan: housekeeping (session 35, 2026-11-19).** N1.1 to
    N1.4 of "Next steps". The weekly link check retries a 5xx or a failed connection twice
    after a pause, leaves links under site_url to the internal check and fetches one of the
    82 edit links for all of them (`tests/tools/test_check_links.py`, a local server that
    answers 503 then 200). Verilator is pinned to the commit of the v5.054 tag (bbb60a4; a
    hash, as `dev_setup.sh` reads it, which now records the commit it built in
    `~/verilator/.ref`); the branch run built it in 7 minutes and every testbench passed on
    it, 0011 and the 0014 subclass included; issue 4 closed. Work log items 112 to 191 and
    the eight review rounds moved to `HANDOFF-archive-3.md` (this file 2,800 to about 900
    lines; the 23 open review items stayed, the video re-caption notes were dropped).
    `requirements/lock.txt` holds the 45 versions the green run of 2026-11-14 installed
    (taken from its log), read with `-c` by site.txt and dev.txt; a pip install on Python
    3.12 gives exactly the lock, and the build equals the live site's but for the date.
    Found on the way: this sandbox had pymdown-extensions 12.3 while CI and the live site
    were on 13.1 (no difference in the built pages but the date). The first branch run
    was cancelled by the push of the lock three minutes in; the second covered all four
    commits.

214. **Round 2 of the session 35 plan: accessibility and speed (session 35, 2026-11-20).**
    N6.1, N6.2 and N6.6 to N6.11, each reproduced in a browser before the fix (the owner:
    both rounds in one push to `main` once the branch run is green).
    - N6.1: the run panel's textarea never let Tab out; it now follows the editor (Esc, then
      Tab or Shift+Tab leaves), a shown line under the panel's note names the keys
      (`.py-keys`), and both fields point at it with `aria-describedby` (the editor's
      attribute is set on its `contentDOM`; the bundle was not rebuilt).
    - N6.2: `fitWords` takes all the titles and works in rounds (read every width, then drop
      one word from each that overflows), and `fitNav` waits for the drawer to open under
      Material's breakpoint. Layouts on load at 390 px: 786 to 31 on the home page, 822 to
      81 on 0033; opening the drawer costs 14. The fitted titles are identical to the old
      algorithm's at 390, 1300 and 1920 px.
    - N6.6: a new part, `32-access.css`: under `forced-colors: active` the site's mask icons,
      the admonition and solution-block icons and the theme's code, tab and annotation icons
      take CanvasText (ButtonText on a button, LinkText in a link), with `!important` over
      the admonitions' type colours.
    - N6.7: `line_links` in the hook gives every line number link `tabindex="-1"` (the anchors
      stay: `core.js` finds the lines by them). axe `target-size`: 25 to 97 nodes a page down
      to 1 (the level chip `a[title]` of the header, not touched).
    - N6.8: measured first: 283 kinds of field on 131 pages under 16 px. One rule under
      `(pointer: coarse)` sets `max(16px, 1em)`. `check_phone.py --touch` opens the pages with
      a touch screen; all 131 pages pass with it locally, and CI now runs the phone check
      that way (three steps of deploy.yml). Not tried on an iPhone: the owner is asked to.
    - N6.9: on a screen up to 30em high the part row is static and the fixed row of a page
      without parts is not shown; `reading-tools.js` (`shortScreen`) counts no height for it
      and hangs no solution map from it. Covered height at 640 x 360: 111 px (31%) to 48 (13%).
    - N6.10: `drawerButton` in `layout.js`: the label is a named button in the tab order,
      Enter and Space toggle the drawer, the opened drawer takes the focus, Escape closes it
      and gives the focus back, and the focus leaving the drawer closes it.
    - N6.11: the guide's hint sits under its target (above it when it would lie on the
      focused element), is the box's first child (the second tab stop of the box, not the
      last) and closes on Escape from anywhere in the box.
    - `check_keyboard.py` gained: the editor's and the textarea's Tab and Esc (the textarea
      on a second load with the bundle cut off), the drawer's button on every walked page,
      and no line number as a tab stop. Each new case fails on the old build.
    - Scratch scripts of both rounds (reproductions, measurements, screenshots) were in the
      session scratchpad (r2/, r3/, lab.py), not kept. Locally the browser is
      `/opt/pw-browsers/chromium-1243/chrome-linux64/chrome` (`--browser`): Playwright's
      Python package expects build 1194.

215. **Round 3 of the session 35 plan: the phone header and layout shifts (session 35,
    2026-11-20).** N5 and N6.3 to N6.5, with the owner's two answers: the kind chip as an
    icon on a phone, and a meta line that wraps.
    - N5, N6.3: on a phone the kind chip is a 1.5 rem circle with its icon (the name is its
      tooltip and stays for a screen reader), so the chip row is one line on 105 of 109
      pages (the four with the "new" badge still wrap). The meta line wraps; its `DVQ-<id>`
      label is hidden there and the date (`.qh-date`) does not break: two lines on 98 pages,
      three on 11 (hiding the date on a phone would give two lines on 107; not done, it
      drops content). `a.qh-tag` is `unicode-bidi: isolate`. The statement's heading starts
      at a median of 504 px (514 before), so the gain is what shows, not height.
    - N6.5, measured with the Layout Instability API (`navigator.webdriver` hidden): three
      sources on a question page, not one. (a) The part row built after the load: the hook
      writes it (`_part_row`, `part_row`), `partBar` wires it: 0.032 to 0.0008 at 390 px on
      0033. (b) On a computer `toolsPlace` moves the tools from the header card into the
      row: `.qh-parts` on the card and `33-steady-load.css` give both their final shape from
      the first paint. (c) `foldLevel` folded the side navigation's list after the load:
      `nav_fold` writes it folded with its button: 0.11 to 0.0001 at 1440 px on 0033.
    - N6.4: the builder is in the page from the start (`hidden` removed), `.hb-peek` and
      `.hb-sum` keep their height, and `html:not(.dvq-js)` hides it without scripts (the
      class comes from an inline script in the head; the theme's `.no-js` stays until its
      bundle runs, which made the first try shift again): 0.137 to 0.0009 at 820 px.
    - Tried and removed: fitting the path strip's titles in a script right after the strip.
      With MathJax cut off the strip's own shift is 0.0004 to 0.005; not worth the script.
    - Found, not fixed (N9 below): MathJax laying out inline math is now the one large shift.
216. **Round 5 and the first part of round 7 (session 35, 2026-11-20).** The owner's
    answers: the sitemap date is each page's last commit; the site goes into Search Console
    (the owner sends the verification code); the level cards are reworded now, by what the
    collection holds; the difficulty criteria are proposed by the session and approved by
    the owner before any page changes.
    - N3.1: every question page has its own description (its statement as plain text,
      whole sentences up to 155 characters, 80 to 154 on the 109 pages), in the
      description, og:description and twitter:description tags; the level pages get theirs
      from `LEVEL_DESC`. The social card keeps the site's description (the hook writes the
      tags after the plugin; setting `page.meta` would race with the card's thread).
    - N3.2: JSON-LD on every question page, a `LearningResource` and a `BreadcrumbList`.
    - N3.3: `sitemap.xml` lastmod is a question file's last commit (`_git_dates`); other
      pages get the site's last commit. The build job checks out the whole history.
    - N3.4 prepared: `extra.google_site_verification` in `mkdocs.yml` (empty) puts the tag
      on the home page; waits for the owner's code.
    - Round 7: the level cards, the level pages' first lines and the home page's "which
      level" answer describe what is there (algorithms, math and proofs, puzzles and the
      basics of design and DV for junior; reference models of protocols, scoreboard and
      hardware design for senior). New topics: `graphs` (0065, 0067, 0070, 0102),
      `topological-sort` (0102, instead of `sorting`) and `trie` (0103).
    - N4.3, the re-grading: three read-only subagents graded the 109 pages against a rubric
      (easy: one textbook idea, 10 to 15 minutes; medium: one key observation or two known
      ideas, 20 to 30; hard: a non-obvious insight or several demanding parts, 40 or more;
      relative to the page's level). 52 changes proposed; shown to the owner with four
      recommended exceptions (0068, 0096, 0098 stay medium; 0050 hard to medium, not easy).
      The owner approved with the four exceptions (2026-11-20): 49 pages changed; student
      5 easy, 6 medium, 3 hard; junior 11, 36, 22; senior 1, 17, 8.
217. **Round 4 of the session 35 plan: page weight and the math at build time (session 35,
    2026-11-20).** The owner's answers: MathJax at build time (not KaTeX), and each round
    goes to `main` when its CI is green, round 4 after the owner saw the numbers of the split.
    - N2.1 and N2.4 (42124f4): the hook minifies the stylesheet parts (`minify_css`); the
      rules the UX round left dead are gone from 09, 10, 12, 16 and 17.
    - N2.2 and N2.3 (1336f15, on `main`): the parts reach a page as one of two bundles the
      hook writes after the build, `site-question.css` (384 KB, 59 gzip) and `site.css`
      (178 KB, 33 gzip), against 844 KB (144) joined before; a rule is kept when the HTML
      of a page of that type, or a script it loads (and a script that script loads), names
      every class, id and box kind its selector needs (class prefixes built in scripts
      count). A question's sheet is linked only on the pages it can style. The scripts of
      `PAGE_SCRIPTS` load only on pages that hold their marks. Styles and scripts per
      page: question pages 1.41 MB to 0.88 MB, others 1.30 MB to 0.55 MB. Checked: the
      computed styles of 21 pages in both schemes, the DOM after load on all 132 pages,
      and no rule left out of a page matches an element there (scratchpad split/verify.py).
      tinycss2 was tried and dropped: it re-quoted `url('data:...')`.
    - N2.5: `check_phone.py` prints each page's own styles and scripts and warns over
      `--code-warn` (1400 KB).
    - N9.1: the math rendered at build time (`tools/build/mathjax/render.js`, Node with
      mathjax@3.2.2 from its lock; `npm ci` in every CI job that builds). The pages load no
      MathJax script (1.1 MB, 259 KB gzip) and link `stylesheets/math.css` (36 KB, the
      characters of the whole site). MathJax's in-browser scale (123.4%, Rubik's x-height)
      is one rule; its msubsup script padding is kept to msubsup and munderover (in the
      browser it padded every subscript on the 21 pages that had one). 17,926 formulas on
      108 pages measured at 820 px against the build before: the same size but 364
      subscripts on those 21 pages, 2 to 5 px narrower; no page changed height; the
      search index is identical; the wide-inline-math marking (`is-wide`) is the same.
      Layout shift at 820 px: 0.21 to 0.005 (0061), 0.15 to 0.006 (0070), 0.24 to 0.003
      (0104), 0.22 to 0.002 (0006). The HTML grows by the math (median 199 to 316 KB, 34
      to 40 KB gzip); the phone check gives it apart and leaves it out of the 400 KB
      warning. An undefined macro now stops the build. Local checks serve the math fonts
      from `.cache/cdn` (`--local-cdn`).
    - N6.12: the 100 declarations outside a custom property that held a literal colour
      (8 files; the other 16 of the 116 were masks, whose black means opaque) name a
      variable now: a `:root` block of `01-base.css` holds the colours that stay the same in
      both schemes (`--site-on-navy`, `--site-navy-ink`, `--site-shade`, `--site-scrim`,
      `--site-deep`, `--viz-on-fill`, the b3 balls), and 07 its line-number and
      highlighted-line colours per scheme. White at a lower alpha is
      `color-mix(in srgb, var(--site-on-navy) N%, transparent)`, exact. Every declaration
      computes the same colours in Chromium in its scheme; screenshots of 7 pages at 390
      and 1200 px in both schemes match the build before, but for the translucent cards
      of the home page's fan (1 to 2 levels of 255). The contrast pairs use the variables
      (614 ratios unchanged). `lint_pages.py` fails on a literal colour in a stylesheet
      declaration outside a custom property.
    - Learned: the runtime MathJax rendered math only on the first page of a Playwright
      context with the routed CDN script; a fresh context per page measures it right.
218. **Round 6, a pilot of two DV questions (session 35, 2026-11-20).** The owner: "find the
    bug" and UVM topics, two or three questions first, kind `dv` with the `debug` tag. Two
    agents, each in its own worktree from a shared scaffold, wrote one page each with its
    tests, figures and box; the session merged them, put 0111 on the question map (with a
    link to 0050) and ran the checks.
    - 0110 (junior, medium), "שלושה באגים ב-RTL": blocking assignments in a delay line, a
      latch from an incomplete `always_comb`, the carry lost to the 8-bit context width.
      Waveforms from the real Verilator trace; Verilator's own messages quoted (BLKSEQ only
      with -Wall, LATCH by default, nothing for the width, WIDTHTRUNC for the fix without
      the cast). Box `rtlbug`. On the logic-design path after 0001.
    - 0111 (senior, medium), "הטסט עובר וה-DUT שבור": a register slice with a registered
      `out_ready` that drops an item under backpressure, hidden by three testbench bugs
      (no backpressure, `disable iff (rst_n)`, a searching scoreboard with no end check).
      The page's SystemVerilog runs all 16 combinations of the fixes for 5 seeds in
      Verilator and agrees with the page's Python model. Box `falsepass`. On the
      testbench path. Verilator needs `--coverage-user` for a cover's action.

219. **Round 8, question 0036 (session 35, 2026-11-20).** The owner: the box redesigned to
    fit one screen with every feature kept, the page's algebra fixed, no DV additions.
    - The box (`explorer/lfsr.js`): one picture of every cycle in the order of the step
      replaces the ring by value and the proof panel's rings. The seed's cycle is the first
      ring and lights up step by step (the edges taken blue, the last one orange); the other
      cycles are smaller rings, green and violet in turn, packed in rows about 1.3 times
      wider than tall; 0 sits inside the seed's ring when there is room. States are written
      in their circles up to 4 bits (31 labels at 5 bits came out at 5 px; the value is the
      tooltip). Under the picture: the register (smaller), the step and the cycles in
      words. In the side column: the strip and the table, which scrolls past about nine rows
      under a sticky header, is redrawn only for a new width or polynomial, and from 6 bits
      drops the period column (every row is primitive; the title gives the period). The
      theme's 5rem floor under a table header is off there. At 1920 x 1080 the box is 944
      px (was 1508), and at most 984 px at any width (was 1612).
    - The page: step 3's x^5 is x^3 + x + 1 modulo x^4 + x^3 + 1; hint 2 gives the lcm for
      coprime factors and the doubling for the repeated one; step 2 shows the order 6 from
      x^6 - 1 = (x^3 - 1)^2; the proof is now the companion matrix of the reciprocal
      P*(x) = x^4 P(1/x), with 0001 as a cyclic vector and the same order of x for P and
      P*; the box's "the 1 of the polynomial is always a tap" is now x^n, that is s[0]; the
      XNOR trap holds for an even tap count, as in every maximal LFSR.
      `test_section_b_algebra` checks each claim over GF(2).
    - Contrast pairs for the picture's states and rims (620 pairs in all).

220. **Round 9, older items and CI time (session 35, 2026-11-20).** The owner: the display
    fixes and the colons of the older pages, eight explorer shards.
    - CI: the explorer checks (clicks, jumps, inputs) run on eight runners, `--shard K/8`.
    - Boxes on one screen (1920 x 1080): 0019's hourglass 1201 -> 999 px (the fork toggle in
      the play row, the fork text after the comparison, the proof in the side column, the
      live figure at most 40rem); 0048's farm box with the reflections 1197 -> 865 px at
      most (the lengths table under the legend in the side column, a 1.4fr picture column,
      560 drawing units across in a wide box so the text keeps its size); the cake table
      in two columns 7.6rem -> 6.7rem. 0012's kapbase boxes were already 869 px at most
      (base 16, x = 100), fixed in session 34.
    - Phone figures (`reading-tools.js`): tick and coord labels render at 11 px at least
      (other labels keep the 9.5 px floor); a column of y-axis labels is thinned like a row,
      and a lone tick label that overlaps another (a bar's value) is hidden, the higher one
      kept. 0028's bar values no longer overlap.
    - 0004's Mermaid labels that mix Hebrew and Latin, and the "?" of the question, are
      right-to-left isolates (U+2067 ... U+2069); no other page has Hebrew in a diagram.
    - 0087: the rim of a lit bulb is `--lo-rim`, the brand navy in the dark scheme (8.8:1
      on the amber); check_contrast takes a foreground per scheme (621 pairs).
    - Short LTR spans of the prose (24 characters or fewer, with a space: 1,239 of them)
      get the class `ltr-nw` in the hook and stay on one line outside table cells.
    - Colons: five generators (0102, 0104, 0107, 0108, 0109) had `NB = " "`, a plain space;
      they and the literal " :" of 0101 to 0109 are U+00A0 now, the pages refilled.
      `lint_pages.py` checks the generated blocks too (a Hebrew letter, then " :"). The
      pages' prose was done in ae7b115 (2026-11-09).
    - The slider width item was no conflict: 10rem is 220 px at the 22 px rem of a 1920 px
      screen.
    - Still taller than 1000 px at 1920 x 1080 (check_heights, before this round as well):
      0066 intervals 1479 / 1280 / 1140, 0024 credits 1352, 0064 weights 1322 / 1223 /
      1182, 0067 netdelay 1258 / 1258 / 1244, 0025 acknak 1250, 0009 boxes 1240, 0068
      twoheaps 1228 / 1213 / 1137, 0043 horses 1220 / 1186, 0065 islands 1186 / 1186 /
      1159, 0062 tagpool 1136 / 1054, 0047 rainwater 1083 / 1082 (N10).

221. **Round 10, tall boxes and phone labels (session 35, 2026-11-20).** The owner: N10's
    boxes each with a layout of its own, as 0019 and 0048 got in round 9, and the phone
    labels other than the axes at 11 px.
    - Phone labels (`reading-tools.js`): legend labels (a line's name, "T ≈ 0.333") grow to
      TICK_PX like the axes; an axis's name at a corner of a chart hides the label it covers
      (the 0 of the y axis). Room in the generators where labels then met: 0007 and 0011
      captions on two lines, 0020's RCB bracket lower, 0024's rings lower, 0039's egg labels,
      0041's median label left of its line (a new side for `vline` in charts.py).
    - Boxes at 1920 x 1080 (check_heights, at the end of every box), before -> after:
      0047 rainwater 1083 / 1082 -> under 1000 (bars or map beside the step and code);
      0062 tagpool 1136 / 1054 -> under 1000 (no figure margins, an eight-line code window);
      0065 islands 1186 / 1186 / 1159 -> under 1000 (queue beside the board);
      0043 horses 1220 / 1186 -> under 1000 (a scrolling races table that follows the race);
      0068 twoheaps 1228 / 1213 / 1137 -> under 1000 (heaps 14rem, legend beside);
      0009 boxes 1240 -> 989 (ring, walk and formula beside the rounds and the proof);
      0025 acknak 1250 -> 974 (event strip beside the notes; 26-unit rows, `waveStrip`
      `rowH`); 0067 netdelay 1258 / 1258 / 1244 -> under 1000 (a scrolling links table);
      0066 intervals 1140 / 1280 / 1479 -> 988 / 1002 / 1087 (the timeline at about its
      drawn size beside the presets and legend, the explain panel at full width with the
      steps beside the code; the box is a container of its own, it has no columns);
      0024 credits 1352 -> 1131 (the circle beside the counters and the free events, the
      random run beside the strip); 0064 weights 1182 / 1223 / 1322 -> 1092 / 1141 / 1210
      (the scale beside its legend, a scrolling convolution table).
    - Left over 1000: 0064 (the controls, the summary, the answer and the scale above the
      columns take about 600 px), 0024 (the counters, the circle, the strip and the notes),
      0066 part c (three heights and the threshold make the tallest timeline) and 0025 after
      a random run (1064). Each would need content cut; offered to the owner.
    - Markup moved into wrappers so a part can go in a column (TOP_PARTS never move):
      `.bx-rounds` / `.bx-sum` (0009), `.an-notes` (0025, 0024), `.cr-top` / `.cr-free`
      (0024), `.wt-top` (0064), `.iv-top` / `.iv-aside` (0066). The phone order is as before.

222. **Round 6, four more DV questions (session 35, 2026-11-20).** The owner chose 2, 3, 4 and
    10 of eleven proposals, and suggested cocotb for UVM in Python: pyuvm 5.0.0 on cocotb
    2.1.0 runs on the pinned Verilator. `run_cocotb()` in `tools/page_tests.py` writes a
    page's testbench and its SystemVerilog into `.cache/cocotb/<name>/`, builds when the
    SystemVerilog changed (a few seconds) and returns each cocotb test's result; it skips
    without cocotb or Verilator (CONTRIBUTING.md, "Tests"). Fetching Accellera's uvm-core to
    run SV UVM in Verilator was refused by the session's permission check, so the UVM
    SystemVerilog tabs are shown, not run (a note under them), and each test checks them
    against the Python by structure. No run panel (no demo.py): Pyodide has no simulator.
    Four agents wrote one page each in worktrees from a shared scaffold (branch
    r6b-scaffold); the session merged them, put them on the testbench path and the map.
    - 0112 (junior), "ה-override שלא נכנס לתוקף": a driver built with `new`, so a type
      override never applies; an instance override with a path missing `uvm_test_top.`;
      when the override must be set. DUT `parity_rx`; 12 cocotb scenarios.
    - 0113 (junior), "הטסט שנגמר בזמן 0": no objection (ends at 0 ns, 0 compared), the
      in-flight items of a 4-stage pipeline (drain 35 ns at least; pyuvm has no drain time,
      a Timer before the drop), a monitor's objection that never drops (a global timeout).
    - 0114 (senior), "סנכרון שני agents ב-virtual sequence": config and traffic forked
      together, a re-key in mid-packet fixed with a pause handshake on a packet boundary,
      and a tested Python model of the sequencer's arbitration, lock and grab (pyuvm's
      sequencer is a plain FIFO).
    - 0115 (senior), "ה-monitor שרואה שגיאות שלא קיימות": both tabs run. In Verilator the
      processes resumed by an edge run in the order they waited, before the always blocks,
      so a blocking driver started after the monitor gives six false mismatches; in cocotb
      a plain write waits for ReadWrite (like `<=`) and the bug needs `Immediate`. The
      fixes change the driver; a monitor-only fix still reports six (the page shows it).
    - Pages are long (0114 has 1018 lines, most of it a collapsed environment); the owner
      may want them shorter. No explorer boxes in this round.

223. **Round 10, the boxes still over 1000 px (session 35, 2026-11-20).** The owner chose to
    delete secondary parts. At 1920 x 1080 after "all steps", before -> after:
    - 0064 weights 1092 / 1141 / 1210 -> 940 / 909 / 975: the conversion table is gone (the
      digits table and the step's note say the same), the summary lost the states clause
      and the reason of the bound, the step's note moved to the main column, the code window
      is five lines with small step chips and no variables line.
    - 0024 credits 1131 -> 977: the free events lost their title (an `aria-label` on the
      group), the invariant line no longer lists slots waiting for a Grant (a leak still
      shows), a short random-run title, the random run's controls in three rows, compact
      counters, "אין" on the line of the packets in flight, a wider side column (1.3fr).
    - 0066 intervals 1002 / 1087 -> 916 / 992: the timeline at 23rem, a five-line code
      window, no variables line, and the summary without the ranges (the figure shows them).

224. **Round 6, the four DV questions shortened, a box each (session 35, 2026-11-20).** The
    owner: a question must be answerable in reasonable time (easy 20 minutes, medium 40, hard
    60), with less code and fewer parts (medium two, hard three), and a simulation box per
    question. Four agents, one per page in worktrees; the session merged their branches and
    added the shared lines (the stylesheets in `mkdocs.yml`, the colour pairs, the kinds in
    CONTRIBUTING.md). Each page's full environment moved to `tests/<id>/env.py` / `env.sv`
    (and the DUT to `tb.sv` or its own file); the tests put the page's blocks into it, so the
    page code still runs as published, and every number on the page is still checked.
    - 0112: 696 -> 323 lines, two parts; box `factory` (the component tree built one
      component at a time, `new` or `create` per line, type or instance override, the path,
      when it is set; a JS glob checked against `fnmatch`), 784 px at 1920.
    - 0113: 781 -> 354 lines, two parts (the old part c is test-only code now); box `objrun`
      (17 falling edges, the objections, a drain slider, the end lines), 918 px.
    - 0114: 1018 -> 477 lines, three parts (part b's fix is in Python only, with a sentence on
      the SystemVerilog, the owner's choice; its test checks the SV bug only); box `seqarb` (one
      sequencer, FIFO or STRICT_FIFO, a priority, lock or grab, slot by slot), 522 px.
    - 0115: 511 -> 240 lines, two parts; box `edgerace` (ten cycles event by event in the
      scheduling regions, SystemVerilog or cocotb; 32 of its SV choices run in Verilator as
      one parameterized bench, the two "DUT first" orders come from the model only), 780 px.

---

## In progress

- **Session 35 (2026-11-19 and 20):** a review of the site and of this file (work log
  212), then rounds 1 to 3 of the plan in [`ROUNDS.md`](ROUNDS.md): housekeeping (213),
  accessibility and speed (214), the phone header and layout shifts (215), round 5 and
  the first part of round 7 (216), round 4 (217) and a pilot of round 6 (218).
  Round 8 is split in two (0036 alone, then the rest as round 9); rounds 8 (219) and 9
  (220) are on `main`; round 10 (221 and 223, N10 and the phone labels) is on the branch. Round 6
  goes on with four questions the owner chose (2, 3, 4 and 10 of the proposals): 0112
  factory override, 0113 phases and objections, 0114 virtual sequence, 0115 a monitor's
  sampling race. Their Python is cocotb with pyuvm on Verilator (`run_cocotb` in
  `tools/page_tests.py`, the owner's suggestion); the UVM SystemVerilog is shown, not run. Round 2 of the four (224) made
  them shorter and gave each a box.
- **State:** `main` (5c71e11, deployed 2026-11-20 13:04 Israel time) has rounds 1 to 5 and
  7 and the pilot of round 6 (111 questions, 204 boxes); the live site was checked at 390
  and 1440 px in both schemes (built math, 0110, 0111, the home page). Next: the owner's
  look at 0110 and 0111 before the rest of round 6, then rounds 8 and 9.
- **Waiting on the owner:** the
  Search Console verification code (N3.4); a try of a box's number field and of the lists' filter on an
  iPhone (the page must not zoom on focus, N6.8); YouTube links of the videos made in the owner's other project
  (add them as `video:`, notes/VIDEOS.md); the giscus ids (README, Comments) in `extra.comments` of `mkdocs.yml`; checks of
  the live site at 390 px and on a desktop, light and dark (github.io is not reachable
  from the cloud sandbox); a lint rule for numbers laid out from the right was offered
  and not answered (do not add it without a yes).
- **Decision (owner, session 20): the repository stays public.** The options kept for
  later are in `HANDOFF-archive-2.md` ("In progress notes").

## Open items

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

## Question variety

### Coverage (session 27, 69 questions; 92 since session 32)

| Level | Questions | Main topics covered |
|-------|-----------|---------------------|
| Student | 0001, 0002, 0003, 0010, 0012, 0015, 0032, 0036, 0040, 0048, 0064 | digital logic, bitwise, sorting, stack, digit puzzles (with number bases in 0012 part c), conditional probability, BFS over a tiny state space (wolf, goat and cabbage), LFSR periods and primitive polynomials, the shortest path by two reflections (the farmer, the food and the water), weights for every load in base 2, balanced base 3 and balanced base 2c + 1 (0064) |
| Junior | 0004, 0005, 0006, 0008, 0009, 0013, 0014, 0016, 0017, 0018, 0026, 0027, 0028, 0029, 0030, 0031, 0033, 0034, 0035, 0038, 0039, 0041, 0042, 0043, 0044, 0045, 0046, 0047, 0049, 0051, 0053, 0055, 0056, 0058, 0059, 0060, 0061, 0062, 0063, 0065, 0066, 0067, 0068 | FIFO depth from rates, Gray pointers and CDC, a divide-by-3 clock, SVA for a handshake, logic puzzles, BFS (remainders, hourglass states), O(n) scans, permutations, SV constraints, Josephus (proof), cycle detection, motion and speed ratios, sequences and a single-peak proof (cake split), relative speed and counting with inclusion-exclusion (clock hands), geodesics on a box by unfolding (spider and fly), Dijkstra over a bitmask state with the greedy rule (bridge and torch), a price list per load and a range function (the camel and the water), selection from partial orders (horse races without a stopwatch), the Kaprekar step as code with a hash and a closed form for the digits (0044), the odd ball in fewest weighings (0045), the largest square, rectangle and right triangle of ones by dynamic programming and a stack (0046), trapping rain water by two pointers and a heap (0047), the UVM testbench architecture (0049), poisoned bottles as digits in base b + 1 (0051), an ALU covergroup and its closure time (0053), a divisible-by-m state machine from the MSB and the LSB (0055), ants on a pole by ghosts (0056), coins in a row by a parity trick and an interval DP (0058), the next number with as many ones by Gosper's hack, the previous by the complement, and the same for zeros across lengths (0059), the longest run of ones with k flips by a sliding window, and of one value on a bus (0060), the tags a list of transactions needs by an event sweep, one pool and two (0061), the sliding-window maximum by a monotonic deque, the window with max − min <= limit, and the same in hardware (0063), islands in four and eight directions (0065), merged intervals and the total height per piece (0066), BFS and Dijkstra for a broadcast time (0067), the median and the p-quantile of a stream by two heaps (0068) |
| Senior | 0007, 0011, 0019, 0020, 0021, 0023, 0024, 0025, 0037, 0050, 0052, 0054, 0057, 0069, 0071 | a three-wizard duel solved backward (0071), the edit distance of a scoreboard (0037), SV constraints, randomization, probability, combinatorics, Dijkstra on a state graph, PCIe completion rules, recursive enumeration, counting formula with proof, generalized Josephus (recurrences, induction), a PCIe endpoint reference model (classes, block memory, scheduling), a USB4 credit flow-control reference model (modulo counters, loss and resynchronization), a PCIe Ack/Nak reference model (Retry Buffer, Replay, error handling), an out-of-order scoreboard (0050), waiting times of coin patterns and Penney's game (0052), round-robin and weighted arbiters with SVA (0054), a constant-memory checker for missing tags (0057), overtakes in a stream of responses by a Fenwick tree (0069) |

Algorithms and puzzles are well covered; 0020 / 0021 / 0023 / 0024 / 0025 are the protocol questions (PCIe, USB4), with 0023, 0024 and 0025 reference models.
Round R (session 18) opened the DV-core shelf: FIFO depth, Gray pointers / CDC, a clock
divider, an LFSR, synchronizer MTBF (replaced by the edit distance in session 33) and SVA; 0040 (a sequence detector FSM) and 0041
(coverage closure of random tests) followed, then 0049 (the UVM testbench) and 0050 (an
out-of-order scoreboard). **Still missing:** UVM in depth (factory, RAL, virtual
sequences as questions of their own), debug ("find the bug") and verification
planning; covergroups since 0053.

### Sources for new questions

Links found during session 3, for inspiration (take the idea, write our own question and
solution; do not copy text). Quality varies, so check the answers.

| Source | What is there |
|--------|---------------|
| [HDLBits](https://hdlbits.01xz.net/) | ~180 small Verilog design problems with online checking (FSMs, counters, shift registers, waveforms) |
| [Verification Academy cookbooks](https://www.verificationacademy.com/cookbook) | UVM and coverage cookbooks (free registration) |
| [ChipVerify](https://www.chipverify.com/) | SystemVerilog / UVM / SVA tutorials with examples |
| [Sunburst Design papers](http://www.sunburst-design.com/papers/) | Cliff Cummings' classic papers: async FIFO, CDC, non-blocking assignments |
| [ZipCPU: async FIFO](https://zipcpu.com/blog/2018/07/06/afifo.html) | A detailed walk-through of an async FIFO, with formal verification |
| [vlsiweb: Top 60 DV questions](https://vlsiweb.com/design-verification-interview-questions/) | A tiered list of DV interview questions |
| [vlsiweb: SystemVerilog questions](https://vlsiweb.com/system-verilog-interview-questions/) | SystemVerilog interview questions |
| [leetcode-for-asic-verification](https://github.com/Mad-Hat-uvm/leetcode-for-asic-verification) | LeetCode-style problems picked for DV interviews |
| [awesome-open-hardware-verification](https://github.com/ben-marshall/awesome-open-hardware-verification) | Open-source verification tools and frameworks |
| [Glassdoor: verification engineer interviews](https://www.glassdoor.com/Interview/verification-engineer-interview-questions-SRCH_KO0,21.htm) | Questions reported by candidates, per company |
| [Brainstellar](https://brainstellar.com/) | Free probability and logic puzzles, by difficulty |
| [Tradermath brainteasers](https://www.tradermath.org/brainteasers) | Quant-style brainteasers (titles are free, many solutions are paid) |
| [LeetCode](https://leetcode.com/problemset/) | Algorithm questions (stacks, queues, bit manipulation are common in DV) |
| [Project Euler](https://projecteuler.net/) | Math / programming problems, good for "math + code" questions |

---

---

## Technical notes for whoever continues this work

- SystemVerilog tests: Verilator must be newer than 5.052 (CI builds the commit in
  `VERILATOR_REF`, the v5.054 release tag since session 35; the recipe is in
  `CONTRIBUTING.md`) and `z3` must be on the PATH. The 5.052 release crashes on 0011 and
  mis-randomizes the 0014 subclass; the apt package (5.020) has no constraint support.
  `run_tests.py` refuses older versions.
- In a cloud sandbox without flex, `pip install verilator` (5.048, in a venv) runs most
  testbenches: wrap the binary so the C++ build gets `-CFLAGS -fcoroutines -CFLAGS
  -std=c++20`, and call `run_sv()` of `run_tests.py` directly (its version check asks for
  5.053+, and the classes with constraints need the CI's build). 0055 to 0062 pass this way.
- Verilator on a fresh cloud sandbox: `apt-get install -y flex bison help2man libfl-dev z3`,
  then `bash tools/dev_setup.sh --verilator` builds the pinned commit into `~/verilator` (about
  15 minutes; it reports chromium missing, which is fine: the checks use
  `/opt/pw-browsers/chromium`). Found with it: `sort()` on an `int` queue orders negative
  values as if unsigned (0068's testbench sorts by hand); `dist` and `before` are keywords,
  not usable as names.
- Build: `pip install -r requirements/site.txt && mkdocs build --strict`. Versions are pinned
  (MkDocs 1.6.1, Material 9.7.7). Material warns about MkDocs 2.0 — do not upgrade MkDocs
  to 2.x, its plugin system (and therefore the hook and the tags plugin) is gone.
- Navigation is **not** written in `mkdocs.yml`; it is generated in `on_config` of
  `hooks/questions.py` from the files in `docs/questions/<level>/`.
- The `level` field must match the folder name; ids are unique across all levels and
  the file name must start with the zero-padded id.
- External scripts (MathJax, WaveDrom) load from `cdn.jsdelivr.net`; Mermaid is loaded by
  Material itself from `unpkg.com`. The cloud sandbox cannot reach these CDNs, so local
  screenshot checks serve them from `npm pack` copies via Playwright request routing:
  `tools/dev_setup.sh` (run by the SessionStart hook in cloud sessions) keeps them in
  `.cache/cdn`, and `check_phone.py` / `check_explorers.py --local-cdn` route to them.
- SystemVerilog static blocks: a variable declared **with an initialiser inside a loop of
  an `initial` block** is initialised once (IEEE 6.21, and Verilator follows it): `int g =
  f(b);` inside `for (int b ...)` keeps the value of the first iteration. Declare such
  variables at the top of the block and assign them in the loop (session 18 found this in
  tests/0031, 0034 and 0038; `run_tests.py` now prints a failing testbench's messages).
- Social cards in the sandbox: Google Fonts is unreachable, so before a build copy a
  Hebrew-capable TTF (DejaVu Sans) to `.cache/plugin/social/fonts/Rubik/Regular.ttf` and
  `Bold.ttf`; the plugin then skips the download (the cards use that font locally, Rubik in
  CI). axe-core comes from `npm pack axe-core@4.14.0` (the npm registry is reachable):
  `python tools/checks/check_phone.py site --offline --axe <copy>/package/axe.min.js ...`.
  `check_links.py --external` in the sandbox reports most hosts as broken (the proxy blocks
  them); it is meant for the weekly workflow.
- Publishing: push to `main` → the workflow builds and deploys. It can also be started
  manually (`workflow_dispatch`). `actions/deploy-pages@v4` prints a Node.js 20
  deprecation warning; bump the action versions when newer majors are available.
- Images go in `docs/assets/images/`, named `<id>-<short-description>.<ext>`.
- Code, comments, commit messages and repo documentation are in **English**; question
  content is in **Hebrew**.
- Do not put Hebrew inside MathJax (`\text{...}`): it renders reversed. In inline SVG,
  give Hebrew `<text>` elements `direction="rtl"`, and prefer an HTML legend over SVG text.
- A lone bracket (`(`, `[`, `{`) in inline code inside Hebrew text is displayed mirrored by
  the browser, whatever `direction` / `unicode-bidi` the `code` element has. Name the
  bracket in Hebrew or show it inside an LTR figure instead.
- Inline SVG figures are generated by Python scripts and styled by `.perf-chart` /
  `.figure` classes in `extra.css` (see the table in `README.md`).
- Simulator gotchas found while testing:
  - Verilator 5.020 (Debian) does not reset an automatic function's local queues and
    associative arrays between calls inside a loop; LRM-correct functions returned wrong
    results (0005, and the 0018 / 0019 BFS and Dijkstra). The pinned 5.053 snapshot resets
    them, so those pages run as published.
  - `wait` is a reserved word in SystemVerilog (`wait(...)` statement); the hourglass code
    calls the waiting time `delay`.
  - Verilator rejects `ref` arguments that are queue elements when inlining; use
    `/*verilator no_inline_task*/` in the test harness (0003).
  - Verilator 5.020 cannot run `randomize()` with constraints on arrays (0007); 5.052 can,
    but crashes on a `rand` array of enums in a class (0011) and leaves elements of
    constraint-sized rand dynamic arrays unrandomized in a subclass (0014). Both fixed in
    master after 5.052, and in the 5.054 release CI uses since session 35. z3 prints `%Warning-UNSATCONSTR` for an
    unsatisfiable `randomize() with`, which the 0007 and 0011 testbenches trigger on purpose.
  - Icarus does not support `ref` ports or `break`.
  - Verilator 5.053 and assertions (round 6, 0020, 0022, 0033, 0039, 0060, 0082): the
    action block of `cover property` never runs unless the bench is built with
    `--coverage-user` (0082 does; the others count with a covergroup and
    `get_inst_coverage()` instead). Two instances of one parameterization of a module that
    holds a covergroup fail at C++ compile (`no member named '__PVT____Vint'`); give them
    different parameters (0060 uses widths 12, 10 and 32). A `break` in an inner `for`
    inside an `initial` block left the outer loop too (0060).
  - In a module `initial` block, `string y = f(x);` inside a loop is a **static**
    initialiser that runs once — declare first, assign inside the loop. Verilator 5.020
    re-ran such initialisers on every iteration (not LRM-correct), which hid two testbench
    bugs (0009 `all_found`, 0014 `k`) that 5.052+ exposed; both fixed in session 5.
  - Verilator 5.020 `sort()` on a queue of signed `int` sorts as unsigned (found in the
    0003 testbench); the testbench checks order pairwise instead.
  - A comment that starts with the word `Verilator` (`// Verilator ...`) is parsed as a
    `/*verilator*/` pragma and fails the build. Start such comments with other words.
  - Assignment patterns in comparisons (`if (q != '{1, 2})`) are unsupported in 5.020;
    compare against a variable.
  - In the 5.053 snapshot, `blk = '{default: 8'h00}` on an unpacked-array local of a class
    method did not zero it (0023, blocks created by a partial write kept stale bytes); the
    page zeroes with a `foreach` loop. An associative array whose value is an unpacked
    array (`typedef byte unsigned block_t[RCB]; block_t memory[bit [63:0]];`) works,
    including `memory[key][i]` reads, with a harmless `SIDEEFFECT` warning on the store.
  - Cross-check SystemVerilog answers on more than one simulator.
- Run panel: `hooks/questions.py` embeds the page's Python blocks as JSON and the demo as
  the editor content; `docs/javascripts/run-python.js` + `py-worker.js` run them. The
  page code runs as `solution.py`, the editor as `your_code.py` (tracebacks show those
  names). Local screenshot tests route the Pyodide CDN to an `npm pack pyodide@0.26.4` copy.
- Explorers (`docs/javascripts/explorer/`, split in session 21): a new kind is a file
  `<kind>.js` whose first line is `// kinds: <kind>`, with its pure functions, its view and
  a `dvqExplorers.register({ views, help, models })` call; shared helpers come from
  `dvqExplorers.lib` (add a helper to `core.js` and its `lib` only when two kinds use it).
  Add a Node test (through `explorer_require()`) that compares the models with the Python
  reference. Build summary
  text with `ltr()` (a `<bdi dir="ltr">`) around math and numbers, or the RTL paragraph
  reorders them.
- SystemVerilog keywords that read like field names: `edge`, `dist`, `inside`, `within`,
  `table`, `wait`, `type`, `var`, `do`, `bind`, `cross`, `cover`, `expect`, `with`,
  `before`, `solve`, `soft`, `local`, `global`, `let`, `until`. A struct field or variable
  with one of these names fails to parse in Verilator ("syntax error, unexpected dist");
  0030 uses `hinge`, `gap` and `in_wall`. Verilator is not installed in the sandbox, so
  before pushing new SV, intersect its identifiers with the IEEE 1800 keyword list (a
  ten-line script over `extract_code.blocks(qid, "systemverilog")` and `tests/*/*.sv`).
- Every explorer kind has `mount(box)` and builds its own controls. Patterns to reuse:
  a play loop on `requestAnimationFrame` with a speed select (clock, motorcycle), a
  stepper on `setInterval` with prev / next / play (cake, Josephus, hourglass, bridge,
  river), pointer drag on an SVG with `setPointerCapture` (clock, strip). Keep the math
  pure and exported; every kind has a Node test against the Python reference.
  Keep the math on integers where it can be (the clock counts meetings in the window
  [sec, sec + 1) as k·P < (sec + 1)·q), and keep time labels inside their second (the
  hundredths are capped at .99) so the label and the highlighted second agree. Avoid
  `<input type="time">`: it shows AM / PM in some locales.
- Generated blocks: wrap each block on the page in `<!-- gen n -->` / `<!-- /gen -->` with
  a blank line inside on both sides (an HTML comment line directly before a Markdown table
  would swallow it into an HTML block); `fill.py` writes them that way.
- Update the **Work log / Open items** sections of this file at the end of every session.
