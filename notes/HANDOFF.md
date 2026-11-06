# HANDOFF

Living task list for this repository: what was done, what is in progress, and what comes
next. Update it at the end of every work session so anyone (human or AI) can pick up
where the last session stopped.

_Last updated: 2026-11-06 (session 33)_

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
| Tests                 | Python: full tests of the page code. SystemVerilog: Verilator built from a pinned development commit (after 5.052) with z3, so every class runs as published; a translation by intent (fingerprinted) is allowed only for a proven simulator bug, and none is needed today |
| Failing tests         | Block the deploy; the live site keeps its previous version              |
| Run button            | Per question, Python only (Pyodide in a web worker); SV cannot run in a browser, the panel says it is checked in CI instead |
| Position levels       | Student / Junior / Senior; the Staff level was removed on 2026-10-21 (owner: no staff questions planned) |
| Look and feel         | Own navy + amber palette, logo and footer; level / difficulty as CSS chips; one header card per question (see **Site redesign plan** in `HANDOFF-archive-2.md`) |
| Next rounds (2026-10-27) | Owner: no rounds of new questions for now; only improve the existing questions, the site and its interfaces (series S). The question proposals X360 to X410 stay listed for later |
| Closed (2026-10-27) | Owner: no run panel for questions without Python code, no print style, and 0001 stays as it is; not to be proposed again |

---

## Work log

Sessions 1 to 21 are in [`HANDOFF-archive.md`](HANDOFF-archive.md) and sessions 22 to 30
(items 1 to 111) in [`HANDOFF-archive-2.md`](HANDOFF-archive-2.md), with the site
redesign plan of 2026-10-16 and the proposal series six to eight. The numbered items
below start at item 112 (session 31).

112. **Three touches on the home page, after Hallmark (session 31, 2026-10-31).** The owner
    asked what to take from Hallmark (usehallmark.com, github.com/Nutlope/hallmark): its
    elements, not its colours. A survey of its site and its fifty themes and a page of
    seven live demos in the site's look; the owner chose, for the home page: the motto that
    corrects itself (a new amber line, "פתרון מלא לכל שאלה, כדי להבין", whose last word
    replaces a struck "לשנן" once a browser session), the builder's series as a dealt fan
    of small cards (id, difficulty, minutes; the title of the card under the pointer or
    the focus in a line under it), and the chip with a calm patch under every line of text
    (the text side's wires now run to the edge) and bursts of fast white electrons (no red
    "failed" electrons: the owner did not want a chip that looks broken). Next, as a second
    change: a waveform viewer on the six WaveDrom diagrams (two buttons under each,
    "measure" with cursors A and B in cycles, and in ns where a diagram declares its clock;
    "play" with a time line and a log of changes written from the waves). Last: a figure
    that stays beside the steps of a solution (sticky), tried on one question first.
113. **The waveform viewer (session 31, 2026-10-31).** The owner's choices: on the six
    WaveDrom diagrams only (0001, 0034, 0035, 0038 twice, 0040), two buttons off by default,
    a play that sweeps and lights a log written from the waves, and cycles with ns only
    where a diagram declares its clock (`dvq: { mhz: ... }` in its source; none does yet).
    `docs/javascripts/wave-viewer.js` (added by the hook beside `wavedrom-init.js`, which
    now keeps the sources and hands each rendered diagram to it) reads the period marks
    (`gmark_*`) and the lanes' offset from WaveDrom's SVG; the log's pure part runs under
    Node (`tests/tools/test_wave_viewer.py`). Seen while checking: axe at 1200 px reports,
    on 0038, Material's search dialog without a name, the page tools' "solved" and "star"
    buttons whose names do not contain their visible text, and the current part chip's
    contrast in the light scheme; all from before, fixed in item 114.
114. **Three accessibility fixes (session 31, 2026-10-31).** The owner asked to fix what axe
    found at 1200 px: Material's search dialog (`role="dialog"`, no name) is named "חיפוש
    באתר" by `quick-jump.js`; the names of the "solved" and "star" page tools now start with
    the word shown under their icons as a word of its own ("פתרתי : לסמן כפתורה", "מועדף :
    להוסיף למועדפים", and the pressed states likewise; "שפתרתי" or "כמועדף" do not count,
    a Hebrew prefix glues to the word); the current chip of the part bar is navy on the
    amber (white was 2.5:1 in the light scheme), a new pair in `check_contrast.py`.
115. **A figure beside the steps, on 0055 (session 31, 2026-10-31).** The owner chose 0055
    for the pilot; side by side on a wide screen and not sticky on a phone (a tap lights a
    step there); scroll, click, tap and focus switch the step; the step's parts in amber and
    the rest dimmed. The machine's figure moved from "the idea" into "the steps" in parts a
    and b (the idea now points to it), part a got a fourth step, an example (13 = `1101`:
    r goes 1, 0, 0, 1), whose walk lights arc after arc, as part b's example of 6 does.
    `q0055.py` keys every state and arc (`data-fig`); `div.steps-fig[data-fig-steps]` lists
    per step what it lights (CONTRIBUTING, "the solution blocks"); `question-page.js` does
    the rest. The test checks the keys and that both walks follow the machine.
116. **The figure beside the steps on three more questions (session 31, 2026-10-31).** The
    owner asked which questions with a state diagram could have it: 0040, 0032 and 0052 fit
    (0056 less so; 0018 and 0063 do not; the Mermaid diagrams cannot be lit, Mermaid draws
    in a closed shadow root). The owner's choices: 0040 part a with a sixth step, an example
    (`1011011`, two detections, the second on the first one's last `1`, walked arc by arc);
    0032 with the state graph moved into part b's steps (the BFS steps light the start, the
    goal, the four crossings out of the start, the way back, and a new fifth step walks part
    a's seven crossings); 0052 part a, each equation's step lighting its state and the
    arrows out of it. Their figures are wide and low, so from 60em up such a figure sticks
    above the steps (24rem wide, on the surface) instead of beside them, and the reading
    line is lower there (the owner's choice). Keys in q0040, q0052 and q0032; a test per
    question; `page_tests.fig_steps` and `lit` for them.
117. **0071 explained step by step, without code (session 32, 2026-11-01).** The owner found
    the general formula of the wizards hard to follow and sent a step-by-step solution of
    part a from a chat. The owner's choices: every part (a to d) as numbered stages solved
    backward (the duel, the last wizard, the middle one, me, the weak option, the strong
    option, the rule), each with the general formula in p1, p2, p3 (wizards 1, 2, 3 in turn
    order) and then "with the numbers"; only V(x, y) = x / (x + y - xy) for the duel (no S, no
    F/G, no a/b/c); the code removed (a math question: the Python and SystemVerilog tabs,
    `tests/0071/demo.py` and `tb.sv` deleted), the charts, tables and the explorer kept; at
    the end of each part three tables: my chance per wand with the calculation (a sum over
    the ways the round ends), the rivals' strategies with a check at a wand of 0.59 (0.39 in
    part d) and who wins in the end. The old decision tables are gone. The owner's chat
    solution was checked first: every number in it holds (63.7%, 17.1%, 11.1%, 8%, the
    thresholds 0.6 and 0.355). Part d puts the three positions in each table and adds the
    "fact" (the middle wizard waits iff the last one hits with at least 1/2: both options
    share the denominator). New in q0071: `outcomes`, `wand_table`, `who_wins`,
    `check_table` and their part d forms; a wand "just under" is written \( 0.6^- \) (the
    plain "0.6⁻" showed reversed in RTL, also in the old positions table). The test now
    checks every step's formula and inequality against the generator, not page code.
118. **Four new questions on in-place permutations, 0072 to 0075 (session 32, 2026-11-01).**
    The owner asked for coding and logic questions on principles the bank lacks, liked an
    in-place transpose, and picked three more of its kind. The owner's choices: four
    separate questions, Python and SV everywhere plus an RTL module in 0075, a box of its
    own for each, and all four published together.
    - **0072, rotate an array by k (student):** three reversals (the swap count), the cycles
      (gcd(n, k) of them, every entry moved once), and a full FIFO in a single-port RAM put
      back to entry 0 (2n accesses for the cycles, 4 a swap for the reversals; `Ram` class).
      Box `rotatek`: either method stepped, the cells tinted by part or cycle, tmp beside.
    - **0073, perfect shuffles (junior):** 8 out-shuffles and 52 in-shuffles for 52 cards,
      the order of 2 mod M for any n (M = n - 1, n + 1, or n when odd; the odd deck is the
      even one without its fixed card), and the interleave in place by divide and conquer
      with rotations (the O(n) cycle leader of Jain 2004 told, not coded). Box `faro`.
    - **0074, transpose a matrix in place (junior, hard):** rotate an image by transpose and
      row reversal; m x n by the cycles of k -> k m mod (mn - 1) with a bit per entry; and
      without marks, each cycle from its leader (the walk steps tabled). Box `transpose`.
    - **0075, the 8 x 8 bit transpose (senior):** the loop, three delta swaps (shifts 7, 14,
      28; the masks are the bits with r_i = 0, c_i = 1), N x N in one word and 32 x 32 in 32
      words (80 swaps), and `bit_transpose`, wires only, checked in Verilator at N = 8 and 4.
      Box `bitmatrix`: draw bits or type the word, step the three stages.
    Figures are HTML cell tables from `tools/figures/cells.py` (class `pm-cells`, tints c1 to
    c5, a focusable scroll region), styled in 11-questions.css; new topics permutations,
    number-theory, matrices; nine contrast pairs; the coding path and the question map have
    the four.
119. **Videos 0032 and 0031, the third V7 round (session 32, 2026-11-01).** The owner asked
    for two fairly easy questions with no video and picked 0032 (wolf, goat and cabbage) and
    0031 (the bridge and the torch). 0032 (7:40, `video_parts` [0, 180]): simple drawn icons
    in Manim for the seven crossings, the river box's buttons (two refused tries, then the
    plan), the proof that seven is the least; part ב the 4-bit state, a Manim graph of the
    ten safe states filled layer by layer, `river_safe` and `river_plan` typed (a 15-line
    window) and traced layer by layer beside the box's BFS panel. 0031 (8:23, [0, 213]): the
    19-minute trap first, the 17 plan, the bridge box's plans, then the proof by cases (C
    without D: 18 at least; C with D: 17 at least), a time bar per case; part ב the state
    (mask, torch side), BFS against Dijkstra, `bridge()` typed in a 13-line window and traced
    pop by pop with the variables and a log of pops beside the code (the box is too narrow
    there at 80 % of its page size beside 74-character lines, so it follows for the walk
    back). Environment notes: manimpango needs `libcairo2-dev libpango1.0-dev pkg-config`
    from apt before `pip install -r requirements/video.txt`; the sandbox's proxy blocks
    github.io, so the live site cannot be fetched from here. Waiting on the owner: watch them,
    upload, send the YouTube ids.
120. **Videos 0001 and 0040, a fix on 0040 (session 32, 2026-11-01).** The owner picked two
    more easy questions, both hardware, and chose: SystemVerilog typed in both (the 0011
    exception) and walked beside the box, the timing built cycle by cycle in Manim, and in
    0040's part ב the construction and Mealy against Moore. 0001 (4:55, `video_parts` [0]):
    the circuit drawn, the timing under it, the page's WaveDrom diagram (taken from the built
    site by `videos/0001/wave_shot.py`, since box_shots captures only `.explorer`), the edge
    box, `rise_detect` typed, the two traps. 0040 (7:10, [0, 284]): the Mealy diagram edge by
    edge, 1011011 stepped on it and on the box, `seq_detect_1011` typed in a 14-line window,
    the timing built cycle by cycle; part ב 10101 by the longest suffix that is a prefix, the
    box building it, the Moore diagram and the output table (Mealy in cycles 4 and 7, Moore 5
    and 8). Found while scripting: 0040's trap "back to the start after a mismatch" used the
    stream 10101011, where the naive detector also fires in cycle 8; it is now 101011 (the
    right machine fires in cycle 6, the naive one never), and test_0040 checks both machines,
    tb.sv feeds 101011. Note: the system Playwright (1.56) wants headless_shell-1194, the
    sandbox has 1243; `check_phone.py --browser /opt/pw-browsers/chromium` works.
121. **Videos 0026 and 0012 (session 32, 2026-11-01).** The two easy questions left were
    0036 and 0026; the owner took 0026 and 0012. 0026 (4:04, `video_parts` [0]), no code: the
    road with riders and walkers above a distance-time chart built in step, the plans where
    the second friend waits (3 h) and walks (19/7 h), the best plan stage by stage (2.5 h,
    all arrive together), the formula T = (3t0 + t1)/(t0 + 3t1)·t1 derived in LaTeX and its
    limits, the motorcycle box on other values; every number recomputed with fractions in
    scene.py. 0012 (6:26, [0, 168, 320]): part א `is_special` typed and traced on 352 and 495
    beside the box's column subtraction, the no-padding trap; part ב the difference 99(a − c),
    the ten candidates, d = 5, `find_special` typed (its run drawn as jumps of x, since the
    trace is one line run 1,000 times), the chain, histogram and d-map boxes; part ג briefly,
    the base-7 box (610 to 363, then 363 ↔ 264). No page bug found.
122. **0071 restructured: parts, a Markov chain, the box (session 32, 2026-11-01).** The owner
     asked for new parts, after two rounds of questions. Part א (I am first against 0.6 and 0.8)
     has numbers from the start, only p1 symbolic, and adds, at the best wand (0.6⁻), the
     chances of wizard 2 (6/35), wizard 3 (64/575) and the cats (2/25) beside my 513/805. Part ב
     lets me choose my turn and the rivals' order: a table of the six orders (the best wand is
     0.6⁻ in all of them), the winner, third behind 0.6 then 0.8, developed stage by stage (my
     13101/20125, 36/175, 64/575, cats 4/125), and why (both shoot before me; the weak one
     first, so I am left facing it). Part ג is the general case in p1, p2, p3: the decisions
     of every wizard as inequalities, and the rule, checked on every rival pair a < b in steps
     of 0.025 against all six orders and every wand in steps of 0.005: the best is either
     to hide third behind a then b with a wand just under a, or a sniper playing first
     (1 − a); hide when a is above a threshold between 0.456 (b = 1) and 0.478 (b = a). The
     old parts ב, ג and ד (me second, me third, rivals 0.8 and 0.4) are gone. New: the game
     as a Markov chain, in the question (general, in p1, p2, p3) and in part א with the
     numbers, drawn by `chain_svg` in tools/figures/q0071.py (styles `mk-*` in
     11-questions.css, five contrast pairs). The `wizards` box now takes two rivals, my turn,
     their order and my wand; shows the four chances, the six orders (a click picks a row),
     "הבחירה הטובה ביותר", the chart and the live chain. A wand exactly equal to a rival is
     left out of the grid searches (there the tie rule decides; the point just under stands
     for it). The page has no code, as before. test_0071 takes about two minutes (the rule's
     grid).
123. **Videos 0057 and 0043 (session 32, 2026-11-01).** The owner's picks after the easy
    questions ran out (0036 is the last easy one left). 0057 (8:52, `video_parts` [0, 184,
    340, 479]): parts א to ג in full (bouncing ants above ghosts that pass through, a
    space-time chart, `last_fall`, `collisions` and `fall_times` typed and traced, the pole
    and chart boxes), part ד in about 40 s (the labels turn by R − L a lap, 300 s); a
    brute-force simulation in scene.py confirms the ghost model. 0043 (9:09, [0, 232]): part
    א a Manim grid of 36 horses ruled out race by race to the nine races, the proof and the
    information bound; part ב `horses_plan` typed in an 11-row window (three long lines
    wrapped in the picture only, a caption says so) and traced race by race, the box after
    the trace (too narrow beside 81-character lines). Seen in the horses box: the step line
    puts "ועוד" inside an `ltr()` run ("F1, F2, F3, F4 ועוד 1"), so a wrapped line shows "(1"
    at the start of the next line. Fixed: each Latin run (the horse, the list of faster ones,
    the count, the place) is isolated on its own, the Hebrew words between them.
124. **0071: the chain explained, the box tighter (session 32, 2026-11-01).** The owner's
    four touches and answers: the general chain in p1, p2, p3 left the question statement
    (part א's chain with numbers stays, its intro paragraph now explains the chain); in the
    box the six-orders table (one order column, "0.6 ← 0.8 ← אני"; a row is focusable and
    a click, Enter or Space picks it) and a smaller chart (its own 360-wide frame) sit side by
    side when there is room, the chain under them; the chart follows the pointer (a line, a
    dot, the wand and my chance) and a click or tap sets the wand; the chain's rows are
    closer (viewBox 480 × 340), and a state under the pointer, the focus or a tap lights its
    edges and neighbours and explains its number in a fixed line under the chain (the reach
    as a product or a sum, a duel's V(x, y) with the numbers, a win as the sum of its
    arrows), in the box and on part א's figure (data-p, data-me and data-explain from
    q0071.chain_svg; wizards.js wires it). `q0071.chain_states` is the reference of the box's
    `wzStates`; a test checks both and the explanation's numbers. The labels of the two edges
    into a win sit at different heights so that "0.599" twice does not merge.
125. **0071: side by side, a* transposed, part ג in a and b (session 32, 2026-11-01).** The
    owner's screenshots of the live page: the table and the chart still stacked in their
    window. The box is now a size container: the six orders (right) and the chart (left) are
    a two-column grid, one column only when the box is under 26rem (520 px), the table's
    smaller font under 47rem; no sideways scroll at box widths 332 to 635 px. Part ג's
    threshold table is two rows (b, a*) with all six b and b = a; its row labels are plain
    text (a MathJax label in the sticky first column of a scrolling grid table showed blank
    at 390 px: a site-wide quirk of `table[data-grid][data-scrolls]`, not fixed), and it
    fits 390 px (360 px in a 386 px column). The short answer and
    steps 7 and 8 give the hide plan with V substituted: P_me = a(1 + (1 − a)²(1 − b))/(2 − a)
    + ab(1 − a)/(a + b − ab), P_a = a(1 − a)(2 − b)/(2 − a), P_b = (1 − a)²b²/(a + b − ab),
    cats (1 − a)²(1 − b), the limits as the wand tends to a from below
    (`q0071.hide_closed`, tested equal to `hide_third`, against the induction at a − 10⁻³ and
    a − 10⁻⁶, and 13101/20125 at 0.6 and 0.8), and the rule as that inequality against 1 − a.
126. **0055: the machines in D flip-flops and gates (session 32, 2026-11-01).** The owner
    wants parts א and ב implemented as digital logic, not only as code, on the page (and in
    the coming video, which types no code). Their choices: D flip-flops, binary codes 00, 01,
    10 with 11 a don't care, the minimal equations only, AND/OR/NOT gates, an asynchronous
    active-low reset, no structural SV module. Each part's code block now ends with the
    encoded transition table, the two Karnaugh maps (rows b, columns Q1Q0 in Gray order, a
    tint per group, an unused don't care dashed), the equations in display math and the
    schematic (rails b, b̄, Q1, Q̄1, Q0, Q̄0 joined by name, an AND per term, an OR per D, div
    = Q̄1·Q̄0), and a line on 11: with the minimal equations it stays 11 while b = 0 (part א
    11 → 10 on b = 1, part ב 11 → 01), so the reset to 00 matters. Part א: D1 = Q1·b + Q0·b̄,
    D0 = Q̄1·Q̄0·b + Q1·b̄; part ב is part א with the two flip-flops swapped. q0055.py finds the
    equations by a small Quine-McCluskey (blocks 7 to 14); test_0055 runs the circuit
    against the page's functions on every bit string up to 8 bits.
127. **Video 0071 (session 32, 2026-11-01).** The restructured question as on main
    b9b8d61, no code (8:42, `video_parts` [0, 248, 375]): the duel formula, part א's stages
    and the chart per wand (513/805), the Markov chain built row by row with one state
    focused at a time, the box; part ב's six orders and the winning order stage by stage
    (13101/20125); part ג's two plans, V substituted into the explicit P_me, P_a, P_b and
    the cats, the a* table, the box on 0.4/0.8 and 0.7/0.9. scene.py asserts every number
    against q0071. Shorter than the 10–12 minutes asked; the owner reviews it. To capture a
    state's explanation from the box, box_shots.py would need a hover action (it fires
    clicks; the box explains on pointer and focus).
128. **Video 0055 (session 32, 2026-11-01).** The owner asked for no code: parts א and ב
    are built in D flip-flops in Manim (the three states, the binary code with 11 unused, the
    encoded table, the Karnaugh maps, the equations, the circuit with an asynchronous reset),
    a stream stepped through the circuit cycle by cycle, one beat on 11 staying 11 while
    b = 0; part ג in about a minute with the box (343 in base 10, m = 7, from each end).
    7:04, `video_parts` [0, 210, 355].
129. **Video 0039 (session 32, 2026-11-02).** Eggs and floors (6:55, `video_parts` [0, 193]):
    a 100-floor building in Manim, one egg, two eggs (14), three eggs; the question turned
    around (floors coverable in t drops), the table (92 < 100 ≤ 129), the plan 37, 66, 88,
    100 run against T = 36 (nine drops), the box, 93 < 101 for why 8 are not enough; part ב
    the closed form, a decision tree, `egg_table`, `min_drops` and `egg_run` typed in an
    11-row window and `egg_run(3, 100, 36)` traced drop by drop (the box after: beside the
    code it would be at 0.52 of its page size), the box's chart of every threshold.
130. **Video 0018 (session 32, 2026-11-02).** Two hourglasses (6:42, `video_parts` [0, 120]):
    the glasses drawn in Manim with the sand flowing and each flip on a time line to 15
    (A+B at 0, A at 7, A at 11), the box's four events, which D can be measured from 0; part
    ב events, the state (t, a, b), the options and the pruning, `solve` typed in a 13-row
    window and traced pop by pop with the popped states logged beside the code (the box
    after, too narrow beside 78-character lines), the box's search panel, the trap of a
    search without `seen` (244 pops against 5,403 at D = 60).
131. **The fast lane for text-only changes (session 32, 2026-11-02).** The owner asked
    whether small text changes need the twenty-minute CI. Both parts done: a local habit
    (CLAUDE.md: lint, the question's Python tests, build, links, the phone check of the page
    and a screenshot, then straight to `main`) and a CI fast lane: `tools/checks/text_only.py`
    compares the pushed range (`github.event.before`..sha, a blobless clone in the gate) and
    calls a push text only when every touched file is a question page whose front matter,
    code blocks, generated blocks and script-read HTML are unchanged, or a file outside the
    site (videos, notes). Then `quick` (lint, check_videos, `run_tests.py --python-only` on
    the touched ids) replaces `test`, the build runs the phone check on the touched pages
    only, and the explorers, 404 and keyboard checks are skipped. Tested in
    `tests/tools/test_text_only.py` and on the day's commits (0055's three prose commits are
    text only, d8053ce with its figures is not). Also from the day: 0055's parts renamed by
    where a new bit enters, both transitions derived step by step, part ב's display math
    fixed (it was indented 7 spaces, out of its list item), and video 0055 re-rendered with
    the new chapter names (7:04, [0, 211, 356]).
132. **The self-checks removed (session 32, 2026-11-02).** The owner: the "בדקו את עצמכם"
    fields add length and weight and nothing a reader does not get by opening the solution.
    All 103 on 50 pages deleted with their question text (the answer is in the solution),
    and the mechanism with them: `selfcheck.js`, its styles (10-rounds-w, 13-motion M7),
    the lint rule, `tests/tools/test_selfcheck.py`, the keyboard check's step and three
    contrast pairs. What leaned on them was dropped, not replaced (the owner's choice):
    interview mode no longer counts right answers or asks a follow-up after one (the bar
    keeps the clock, the target, the hints and the confidence question), "started" on my
    map means an interview done, and a part's circle on the timeline gets its check only
    when the whole question is marked solved. The per-question tests keep those values as
    "extra examples" of the code. Old `dvq-check:` keys stay unread in readers' browsers.
    The fast lane's classifier no longer names self-checks (any `data-` line is still
    guarded).
133. **Videos 0030 and 0042 (session 32, 2026-11-02).** Chosen by the owner with guiding
    questions. 0030 (5:02, `[0, 153]`): a translucent box, a colour per face kept through
    the unfoldings, the trap of 42, the five-face route of 40 face by face, the page's 16
    unfoldings in a table; part ב without code, the 16 as thumbnails, the strip of 48 lines
    and the site's strip box. 0042 (7:07, `[0, 200]`): the trap of forgetting the way back,
    the price list (60 + 100 + 300 − 60 = 400), the first segment trip by trip and the rest
    fast, the camel box; part ב without code (the staircase, the area under 1/g, the closed
    form and the bound's proof); the bonus as its own short YouTube chapter (the page has
    two parts, so `video_parts` has two entries).
134. **Videos 0016 and 0013 (session 32, 2026-11-02).** Two rounds of guiding questions each.
    0016 (6:06, `[0, 183, 305]`), no code: a ring of people with a pointer, N = 5 step by
    step, the table of F(N) to 32, the proof by the stop at a power of 2, the 41 of Yodfat
    (told as a different rule, as the page's trap says), the moving top bit, the box; part ב
    the same at a faster pace (zeros at 3^m and 2·3^m, as on the page); part ג short.
    0013 (6:41, `[0, 160, 333]`): one line back to 0012, `is_special_4` typed in Python and
    traced on 3524, the chain to 6174, the traps 7777 → 0 and 95 → 0095; part ב the grid
    of the (p, q) pairs with a difference and ✓/✗ per cell, only (6, 2); the pairs and
    histogram boxes; part ג short with the family B = 5k and the base box.
135. **Videos 0009 and 0048 (session 32, 2026-11-02/03).** 0009 (7:07, `[0, 233]`): the
    boxes as coloured cycles, one cycle of 16 cut by one swap into two of 8, the proof that
    one swap is enough (as the page says), the page's example 11 + 3 + 2, the boxes box;
    part ב types cycle_from, helper and find_my_note with traces, Room walked through.
    0048 (6:15, `[0, 173, 238]`): three routes, the double reflection unfolding into one line
    (√98), the stops 2 : 3 : 2; part ב the same reflection backwards (a = 0, b = H); part ג
    without code, θ = 15° as a rotation about O, then θ swept 0 to 60 with z updating, and
    the farm box in mode c. The page says the reflection holds up to 60°, so the video says so.
136. **Videos 0008 and 0014 (session 32, 2026-11-03).** 0008 (6:02, `[0, 186]`): a live
    scoreboard with each country's room under Israel's 343 against the public points left,
    the announcements one by one until France (512 left, 495 room, 17 spill), the box; no
    trap section (the owner); part ב types israel_cannot_win and earliest_certain_loss in
    Python with traces (returns 4). 0014 (6:45, `[0, 292]`): squares drawn on the 10×8 grid,
    overlaps flashed red and touching allowed, the four zones and the ≤ rule, `square_set`
    typed in SystemVerilog and walked beside the page's draw, the i < j and < traps, the
    box with fixed seeds; part ב only what changes (`rect_set`, `constraint_mode`, the cross
    a corner test misses).
137. **Videos 0027 and 0028 (session 32, 2026-11-03).** The cake pair, no code, the same
    shape: a cake strip cut from what is left and the bars of the shares built person by
    person, the peak through the ratio of neighbours, the tie, the exceptional case in one
    sentence, the cake box. 0027 (4:30, `[0, 165]`): person 4 with 0.2158, T ≈ 0.270, the
    increasing f, the tie at a = d = 1/12 (55/288 each). 0028 (4:35, `[0, 155]`): one line
    back to 0027, person 10 with 0.1697, the traps of the last person (0.0155) and of the
    threshold 1, T = 1 − 1/q, the tie at a = 0.25, q = 2 (0.375 each).
138. **Question 0076, a strictly increasing f with f(f(n)) = 3n (session 32, 2026-11-03).**
    The owner's question, junior / medium, math, no code (the owner's choice), ℕ from 1, in
    the digits path. Part א f(14) = 23 by the chain 1 → 2 → 3 → 6 → 9 → 18 → 27 and the
    counting between f(9) = 18 and f(18) = 27 (a ladder figure), without the general
    formula; part ב the formula (n + 3^k on [3^k, 2·3^k], 3n − 3^(k+1) on [2·3^k, 3^(k+1)])
    with the anchors by induction, uniqueness and existence, the base-3 rule (leading 1 → 2,
    leading 2 → 1 and a 0 appended) with a table, a graph against √3·n, and the new `ffn`
    box (n typed or stepped along the chain, the three numbers in base 3, the interval and
    the two lines that work out each value); part ג f(2027) = 3894, checked by
    f(3894) = 6081 (the owner chose this over the other inverse questions, which became
    follow-ups: f(n) = 2n only at 3^k, 100 is no value, no f for 2n, the version with 0).
    tests/0076 builds every strictly increasing f with f(f(n)) = 3n on 1..60 by search
    (exactly one) and checks the box under Node; four contrast pairs for the box's cells.
139. **Question 0077, the function of five rules that reverses the bits (session 32,
    2026-11-03).** The owner chose it from proposals (IMO 1988, the source not named on the
    page), junior / medium, math, no code, in the digits path; the title and the path note
    do not give the answer away. Part א f(2027) = 1727 by the rules alone: the 13 values
    the rules need, a generated table from the bottom up. Part ב in the two ways the owner
    asked for: guess and substitute (the table to 16 in binary, R(n) = Σ b_i 2^(L−1−i), the
    lemma R(2m + c) = c·2^ℓ(m) + R(m), the five rules checked, uniqueness from part א), and
    a derivation without guessing (d(m) = f(2m+1) − f(m), d(2m) = d(2m+1) = 2d(m),
    d(m) = 2^ℓ(m), f(2m + c) = f(m) + c·2^ℓ(m), unrolled on 13 and in general); a figure of
    the bits of 2027 crossing to 1727. Part ג 92 palindromes up to 1988 (62 up to 1023,
    30 of the 32 of length 11; 2015 and 2047 out), P(k) in closed form. The new `bitrev`
    box (n typed, ±1 or the next palindrome; the bits moving one by one to the top of f(n)
    as in the derivation, and the table of the rules on the way) reuses the bit rows of
    0060 (`gs-bits`); two contrast pairs. tests/0077 checks every number, f = R to 20,000,
    d, the palindrome counts and the box's models under Node.
140. **Question 0078, rand7 from rand5 and randN from any randM (session 32, 2026-11-03).**
    The owner chose the generalized rand7-from-rand5 direction from six proposals, split into
    two questions (0078 and 0079), junior / medium, Python and SystemVerilog, in the
    probability path. Part א: two calls as a base-5 number v = 5(a − 1) + b, reject 22..25,
    (v − 1) mod 7 + 1, 50/21 ≈ 2.38 calls; part ב: k calls a round, L = ⌊M^k/N⌋·N,
    k·M^k/L calls (under 2k), the fewest k not always the cheapest (rand5 from rand2: k = 4,
    64/15, beats k = 3, 24/5); part ג (the owner's pick): an exact algorithm with a bounded
    number of calls exists iff every prime of N divides M (rand8 from rand6 in 3 calls,
    216 = 27·8; none for rand7 from rand5). Generator tools/figures/q0078.py (the coloured
    5 × 5 table, the tables of parts ב and ג), the `randmn` box (M, N and k sliders, four
    values of k against the expectation, the bounded test, the grid of the M^k outcomes up to
    400 cells, ten seeded rounds stepped), tests/0078 (exact fractions, the theorem by brute
    force, statistics of the page code, Verilator, the box under Node), CSS rn-* in
    11-questions.css, 16 contrast pairs. tb.sv declares its loop variables at the top of the
    initial block (an initialiser inside a loop there is static).
141. **Question 0079, biased coins (session 32, 2026-11-03).** The second question of the
    same direction, junior / medium, math, Python and SystemVerilog, in the probability path.
    Part א von Neumann's pairs (HT gives 1, TH gives 0, HH and TT thrown away): fair for any
    unknown p, 1/(p(1−p)) flips per bit, and no exact method with a bounded number of flips
    (P(1) would be a polynomial in p). Part ב a coin of any p from a fair coin: the flips as
    the digits of a uniform U, compared with the digits of p until the first difference,
    P(1) = Σ p_i 2^-i = p, 2 flips on average (2 − 2^(1−k), and at most k, for a p of k
    digits; 1/3 has no bound). Part ג (the owner's pick) a fair die: three fair bits, 6 and 7
    thrown back, 4 fair bits = 4/(p(1−p)) flips. Traps: XOR, overlapping pairs, a fixed 10
    flips (342/1024), v mod 6, flips that are not independent; follow-ups: Peres, 1/H(p), a
    coin from a die (6/5), a die from 11/3 fair bits, 1/3 in hardware. Two new boxes in
    explorer/vncoin.js: `vncoin` (pairs by seed, the last pairs and bits, the counts against
    1/(p(1−p)) and 1/2) and `cmpcoin` (the digits of p against the fair flips, the deciding
    cell marked, 1000 trials against p and 2); CSS bc-* in 08-explorers.css, three contrast
    pairs. tests/0079 runs the page code exactly on every flip sequence up to a length
    with fractions, statistically under seeds, the numbers of the page, and the boxes under
    Node.
142. **Question 0080, which pocket the ball enters (session 32, 2026-11-04).** The owner's
    billiards question from a source write-up, senior / hard, math, Python only (the owner's
    choice), in the geometry-and-motion path. The source was checked first: parts 1 to 3 hold
    (tables, the six cases, the proof, Dirichlet, "K is a convergent denominator"), but its
    part-4 example has m = 4, not 2, and four cushions (top, right, bottom, top), and its
    part-4 method missed pockets near the start (21 of 3651 random starts): it began at
    k = floor(2 x0 / a) + 1 and measured the distance to the whole line. The page uses the
    fix (k from floor((2 x0 - w) / a), the ray only: the pocket must be ahead) and shows the
    two failures as a trap. On the owner's rounded snooker table, 360 x 180 cm (s = tan
    alpha): part a aims at (240, 180), three cushions into (0, 180), 900 cm, traced by hand;
    part b unfolds the table, r = 2 tan alpha = q/p, the parity table, p + q - 2 cushions, 37
    degrees never; part c pockets of w = 9 cm and the two middles, s, eps, K, m, the six
    cases with examples, the impossible corners, Dirichlet (K <= 40 at w = 9), continued
    fractions, 37 degrees into (0, 180) at K = 4; part d any start: from the centre at slope
    7/6 into (0, 0) after four cushions, and a periodic shot that never enters ((180, 45) at
    45 degrees, Kronecker for irrational s). Follow-ups: aiming at (241, 180) (599
    cushions), 37 degrees with 1 cm pockets (K = 211, five convergents), mirroring for other
    directions, a ball radius (the table shrunk), the cushion count, separate widths (the
    proof needs w_c <= 2 w_m; 0.5 degrees with 9 and 1 cm enters (360, 0)). The new
    `billiard` box (explorer/billiard.js): the ball dragged anywhere, the aim arrow's tip
    dragged to any direction (and x0, y0, degrees fields, a slider), the pocket width, a
    separate width for the middles, a real 2.625 cm ball; "מכה" runs the ball along its
    real path into its pocket (the end at once under reduced motion), the unfolded table
    under it with the gap at every line of pockets, the calculation (s, c, eps, K, m and the
    row of the table) in a fold, six preset shots. tests/0080 compares the page code and the
    box (Node) with a physical reflection simulation on thousands of random shots, exact
    fractions for the rational slopes, and every number of the page; five contrast pairs on
    the felt (the path and the entered pocket use the -text tones of orange and green).
143. **Question 0081, N queens (session 32, 2026-11-04).** The owner chose it from six
    coding / logic / math proposals, junior / medium, code, Python and SystemVerilog, in the
    advanced-algorithms path. Column c is bit c, drawn with column 0 on the right, so a
    board row sits over its masks. Part א counts by backtracking row by row with the masks
    cols, left (<< 1) and right (>> 1), free = full & ~(cols | left | right) and the lowest
    bit free & -free: 92, 2,056 placements for 8 (a table of the counts and placements for N
    = 4..12 against N! and N^N); the SystemVerilog is iterative with an explicit stack of
    masks (bit is a keyword, so low). Part ב the 8 symmetries: 12 distinct solutions, 11
    classes of 8 and one of 4 kept by a half turn, Burnside 96 / 8 = 12 with a proof that no
    reflection keeps a solution, and count_half (row 0 in half the columns, doubled; the
    middle column apart for odd N); SystemVerilog canonical packs 4 bits a row and distinct
    counts an associative array. Part ג the explicit construction (evens then odds; the
    fixes for N mod 6 = 2 and 3), the proof of the plain case (3(i − j) = m − 1 only when N
    mod 6 is 2 or 3), why 2 and 3 have none. Traps: one diagonal only (2,113), free without
    & full, rotations counted apart, the search space; follow-ups: the counts to 12, the
    torus (gcd(N, 6) = 1), rooks and bishops, the first solution after 113 placements. Two
    boxes in explorer/nqueens.js: `nqueens` (a step per placed queen, the next row's free
    cells, the masks in binary, a jump to the next solution) and `nqplace` (queens clicked
    or typed with the arrows and Enter, attacks and conflicts, the completions counted and
    one shown faint, the queens in the link through dvqExtra); nine contrast pairs, CSS nq-*
    in 11-questions.css. tests/0081 checks the page code against brute force, the classes,
    Burnside, the construction for every N to 1000, every number of the page and the boxes'
    models under Node.
144. **Question 0082, Nim (session 32, 2026-11-04).** Chosen with 0081, senior / medium,
    math, Python and SystemVerilog, in the advanced-algorithms path. Part א normal Nim on 3,
    4, 5: 3 ⊕ 4 ⊕ 5 = 2, the only winning move 3 → 1 (5 ⊕ 2 = 7 and 4 ⊕ 2 = 6 are out of
    reach), the theorem (lost iff XOR = 0), the move h → h ⊕ x on a heap with the top bit of
    x, the number of winning moves, a table of six positions. Part ב misère: lost iff (a
    heap > 1 and XOR = 0) or (all heaps ≤ 1 and an odd number of ones); the endgame (1, 1,
    4): 4 → 0 loses, 4 → 1 wins. Part ג the subtraction game {1, 3, 4}: mex, Grundy numbers
    0, 1, 0, 1, 2, 3, 2 with period 7, lost iff the XOR of the Grundy numbers is 0: 3, 4, 5
    is now lost (1 ⊕ 2 ⊕ 3 = 0, while the sizes' XOR is 2); Sprague–Grundy stated. Traps:
    sum or parity, the largest heap, normal play to the end in misère, XOR of sizes, max + 1
    for mex; follow-ups: 3, 5, 6, 7 has three winning moves, take 1..k (n mod (k + 1)),
    Staircase Nim, Lasker's Nim. The new `nim` box (explorer/nim.js), three times on the
    page: a game against the computer (heaps, rule, who starts; a token click takes the rest
    of its heap; the winning move on request; the heaps or Grundy numbers in binary with the
    XOR row; undo, a log; my moves in the link); CSS nim-* in 08-explorers.css, three
    contrast pairs. tests/0082 brute-forces every position of three heaps to 9 and four
    heaps to 5 under the three rules against the page code and the theorems, checks every
    number and the box under Node; tb.sv brute-forces all 512 positions of three heaps to 7.
145. **UX fixes from the audit (session 32, 2026-11-05).** The owner chose the "fix the
    faults" package from a UX audit against the VectorLab skills. Search: search.suggest off
    (its ghost overlapped the typed text in RTL, "fifif"); theme.language custom
    (overrides/partials/languages/custom.html: Hebrew with "מסמך אחד תואם" / "# מסמכים
    תואמים", the rest from he.html); a match is dark text on an amber tint (the amber text
    was 2.2:1), tags at least 12 px; no result shows "קפיצה לשאלה" (closes the search, opens
    the quick jump with the typed words) and "לכל השאלות" — a button, not a link, since
    Material's Enter reads every [href] in the results (a link threw getAttribute of null).
    Back to top: Material's inline top beat top: auto, so !important; it sits in the bottom
    corner again (it covered the part bar on phones). Part bar: the solution map hangs under
    the bar as an opaque second row (absolute, the page does not move), the part chips keep
    their row, a row that scrolls fades at the edge with more chips (reading-tools.js
    fades); one reading line (spyLine) for the part bar, the solution maps and the table of
    contents (tocSpy sets .is-spy, the TOC marker follows it; before, the bar said ג while
    the contents said ב: 6 positions of 0052 before, 0 after); h2/h3 stop under the bar when
    reached by a link. Phones: the closed drawer is inert and the closed search's field and
    buttons leave the Tab order (layout.js hiddenChrome; 0061 went from 163 to 57 tab
    stops). The sidebar fold button says "כל המסלולים" in the paths section. Three contrast
    pairs.
146. **The circuit layer (session 32, 2026-11-05).** The owner chose a visual package (navy
    and white kept, nothing drastic). 22-circuit.css and circuit.js: a static board-trace
    mask at 5% (4.5% dark) in a top band (body::before, 8rem, 5.5rem on phones, fading
    before the title) and in the margins outside the max(61rem, 80vw) grid at ≥76.25em
    (body::after, fixed); a chip per question (question_chip in the hook: one pin a side per
    part, 1 to 6, and a 4 × 4 die of the id's 16 bits, MSB top left, lit for a 1; colours
    from qc-* only) in the tables' id cell, path cards, related / recent / new lists and the
    header's corner emblem, with the label DVQ‑<id> (part_number) opening the header's meta
    line; a compact phone header (h1 clamp(1.2rem, 5.4vw, 1.42rem), the label, topics, date
    and source in one ellipsized line); the difficulty chip as three LEDs (CSS only, lit up
    to the level with a glow, the word kept); path cards that rise and run one amber current
    along the top edge on hover; <hr> as a data waveform with one amber packet when it first
    comes into view (.is-on); the part bar's reading line as a clock, passed parts with an
    amber ring; a slow wireframe icosahedron (canvas, 9%) under the home hero's chip and in
    the level bands' corner, leaning to the pointer, on screen only, still under reduced
    motion and webdriver, hidden on phones. Eight contrast pairs; tests: the chip is
    deterministic, pins = parts, lit cells = the id's bits, every header has its chip. /all/
    +41 KB HTML (+1.2 KB gzipped).
147. **Numbers laid out from the right (session 32, 2026-11-05).** The owner caught 0055's
    state codes shown reversed: "0 1" in a right-to-left cell is two digit runs that the
    browser lays out from the right, so r = 1 (01) read "1 0". Fixed with ltr_bits in
    q0055.py; a scan of every built page and every box after a few steps found the same in
    0046's heights rows (fixed) and in ordered tuples, "(3, 1)" read as (1, 3): 0013
    (q0013.py), 0018, 0019, 0047, 0043, 0055's Gray order, 0080's legend (q0080.py) and
    0082's (1, 1, 4) (q0082.py) are now isolated LTR. Lists read in order, years and
    thousands separators stay as they are; 0025's sequence numbers inside a generated
    stepper were left. CLAUDE.md gained the rule (Language and RTL).
148. **The finishing round of the UX audit (session 32, 2026-11-05).** Items 1 to 6 of the
    owner's UX list. Rubik loads as a variable font (overrides/main.html `fonts` block, css2
    API, weights 300 to 800; JetBrains Mono 400 to 700): 500 and 600 were drawn as 400 and
    700. Inline code is at least 13 px (`max(0.85em, 0.65rem)`, boxes excluded; it was
    10.9 px in tables). Figure labels stay at the D194 fit (9 → 9.5 px): raising the fit to
    11 px made tick and value labels overlap (32 → 116 pairs over 143 charts), so 11 px
    needs work per generator (open item). Phones (hover: none or ≤ 30em): the box header's
    icons and the playback bar are 44 px (play 48) with a short name under each
    (`data-name` from core.js, drawn by ::after), the page tools 44 px, the part bar's
    solved toggle 44 px without a name, the figure enlarge button unchanged. One action
    colour in the boxes and the run panel (owner's choice; 23-polish.css `--act`,
    `--act-line`, `--act-ink`): navy filled main action, navy outline for the rest, the play
    button navy, no amber hover; in the dark scheme a light navy-blue `#a9c1f0` with dark
    ink. Surfaces: lighter `--shadow-1/2/3` in light mode over a thin `--site-card-edge`;
    seven literal shadows use the tokens; the window dots above solution code removed.
    Motion: `--dur-0` (150 ms) and `--dur-3` (600 ms) join `--dur-1/2`; `.mp-bar` and
    `.lb-pbar` scale (`--p`, scaleX) instead of resizing; the part bar's reading line is
    clipped (clip-path); the home band's pulses run once when it first comes on screen and
    the level-card pictures once per hover (home-extras.js; owner's choice). Eight
    contrast pairs.
149. **The living layer (session 32, 2026-11-05).** Items 7 to 12 of the owner's UX list, in
    24-living.css and dotgrid.js. A pad field (solder pads as a repeating radial gradient
    under two masks) in the home hero under the chip and in the end corner of the level
    bands (owner's choice), at 12%; with a mouse the pads around the pointer light up
    (dotgrid.js only moves --lv-x/--lv-y, once per frame, and sets .is-lit; still on touch,
    under reduced motion and in an automated browser). The page cross-fade (round M's
    @view-transition, the owner's choice over instant navigation) shortened to 180 ms. A box
    not built yet keeps 30rem (built boxes are 24 to 118rem, median about 52) with grey bars
    for its title and controls around the loading wave; the run panel shows its output area
    as three grey lines while Python downloads. Tabular figures in the boxes, the run panel,
    the question header, lists, the side navigation, search results, the quick jump, the
    interview bar and the footer. Page titles a step larger and semibold (question h1
    1.76rem, level band 1.92rem, hero 2.1rem; phones as before; "subtle", the owner's
    choice). The footer gained crop marks and a board line "DVQ · REV <date of the last
    commit in Israel> · <n> Q" (_revision_date and dvq_cards.rev in the hook). One contrast
    pair; a hook test for the date.
150. **Figures where a page had none (S415, session 32, 2026-11-05).** The owner chose four:
    0001 a schematic of the module (D flip-flop with sig_q and the active-low rst_n bubble,
    inverter, AND; it replaces the mermaid flowchart), 0002 part c's bits of a and b after
    each XOR step (changed bits framed, MSB left), 0003 the array after each pass of i
    (sorted part tinted, changed cells framed, an arc per swap, recorded from the page's own
    mystery), 0038 the contract as a state machine over (req, ack) with the forbidden
    samples marked by rule number. Generators q0001, q0002, q0003 and q0038;
    25-figures-c.css; five contrast pairs. Tests: 0001's netlist simulated against the
    page's assign and flip-flop; 0002's rows against swap_xor and the example table; 0003's
    passes against a replay; 0038's moves against check_handshake. The brute force found
    that the checker (and the SVA `$rose(req) |-> ##[1:3] ack`) misses an ack in the rise
    cycle when a later ack lands in the window (rule 2 says one to three cycles): 9 traces;
    reported to the owner, not changed (open item).
151. **0038's rule 2 closed (session 32, 2026-11-05).** The owner chose to fix the gap found by
    item 150's brute force, without a new trap: rule 2 is `$rose(req) |-> !ack
    ##[1:MAX_WAIT] ack` (an ack in the rise cycle fails at once, in that cycle; before, a
    later quick transaction's ack inside the window satisfied it). The page's Python and SV,
    the short answer, step 2, annotation (2), the follow-ups (`##[0:3]` without `!ack` for a
    combinational ack, `start |-> !ack ##[1:3] ack` back to back), handshake.js (hsCheck,
    hsAttempts, "ack מוקדם") and the contract figure (IDLE → req = ack = 1 marked ✗ 2).
    Tests: a regression test on the covering traces, the figure's brute force agrees with
    the model on every 8-sample trace, tb.sv injects an ack in the rise cycle. Published as a
    small fix (`main` ec6957e).
152. **Question 0083, the water jugs (session 32, 2026-11-05).** Chosen from eight logic and
    coding proposals. Student / medium, Python and SV, logic-puzzles path after 0032. Part
    a: 3 and 5 to 4 in six steps (fill B first; eight filling A first; the only shortest
    plan), 16 of the 24 states reachable. Part b: T is measurable iff T ≤ max(a, b) and
    gcd(a, b) divides T (an invariant one way, keep-pouring and k·a mod b the other); every
    reachable state has a jug empty or full; BFS over (x, y) (`jugs_shortest`). Part c: 8,
    5, 3 without a tap, split into 4 and 4 in seven pours (eight starting 8 into 3; unique),
    `split_shortest`. q0083.py (an independent BFS, stepper, tables, the state grids),
    jugs.js (kinds jugs and jugs3), stylesheets/questions/0083-jugs.css, ten contrast pairs. Tests: the gcd rule and
    the edge property for a ≤ 9 and b ≤ 12, the page code and the box against the reference,
    the follow-ups (the total in both jugs, the shorter keep-pouring plan equals the BFS, the
    DFS trap's eight steps), the SV replayed plans. `dist` is an SV keyword: the SV uses
    `depth`.
153. **Question 0084, the longest increasing subsequence (session 32, 2026-11-05).** Chosen
    with 0083. Junior / medium, Python and SV, advanced-algorithms path after 0046. Part a:
    dp and prev in O(n²) (`[10, 9, 2, 5, 3, 7, 101, 18]`: length 4, `[2, 5, 7, 101]`, 28
    comparisons). Part b: tails with the binary search written out, tail_at and parent, the
    invariant and its proof (`[2, 3, 7, 18]`, 10 comparisons). Part c: count_lis with
    (length, count) pairs (`[1, 3, 5, 4, 7]` → 2, the example → 4). Traps: tails is not the
    LIS (`[3, 4, 5, 1]`), bisect_right, dp[n−1], greedy. Follow-ups: non-decreasing,
    patience piles and Dilworth, envelopes, Fenwick counting, Erdős–Szekeres. Five generated
    blocks (q0084.py); the box `lis` (explorer/lis.js) in dp and tails modes with a text
    field, presets and a random draw; stylesheets/questions/0084-lis.css; ten contrast pairs; the tag binary-search
    named in TOPICS. Tests: brute force over all subsequences in Python and SV, the box's
    models under Node against the reference.
154. **Question 0085, the self-describing number (session 32, 2026-11-06).** The owner chose
    three of eight logic-and-maths proposals (0085 to 0087), asking for the generalizations
    and a proof that no other numbers exist. Junior / medium, Python and SV, digits path.
    Part a: 6210001000; the two sums Σd_i = b and Σi·d_i = b; a search that fills digit by
    digit and cuts when either sum passes b (980 full candidates and 4,845 cuts in base 10,
    out of 10^10; 184,746 with the first sum alone). Part b: uniqueness in base 10 from
    Σ_{i≥2}(i−1)d_i = d_0 (z ≥ 3 gives z = 6; z = 1, 2 force d_1 = 8, 6). Part c: every
    base: (b−4) 2 1 0…0 1 000 for b ≥ 7, 1210 and 2020 in base 4, 21200 in base 5, none in
    bases 2, 3, 6; `predicted` and `differ()` against the search to base 16. q0085.py,
    selfdesc.js (edit, search, bases), stylesheets/questions/0085-selfdesc.css, eight contrast pairs. Tests: brute
    force for b ≤ 6, the classification to 16, the box under Node, the SV against
    `predicted`.
155. **Question 0086, the chameleons (session 32, 2026-11-06).** Junior / medium, Python and
    SV, logic-puzzles path after 0083. Part a: 13, 15, 17 never share a colour (a meeting
    adds 2 to every count mod 3; residues 1, 0, 2). Part b: all can turn to c iff the other
    two counts agree mod 3 (unless everyone already has another single colour);
    `meeting_plan`. Part c: the minimum is max(x, y), by counting meetings by kind (r = p +
    q − 2s ≤ p + q); the cheapest colour, the middle count when all three agree;
    `meetings_to` / `min_meetings`; 13, 16, 17 to blue in 16. Follow-ups: 14, 15, 17 to
    green in 17; the reachable states are those with the same residues of the differences
    (360 of 1,081). q0086.py, chameleons.js (sliders, meetings with undo, the plan, the
    triangle of states), stylesheets/questions/0086-chameleons.css, ten contrast pairs. Tests: formula and
    construction against BFS for counts ≤ 12, the box under Node, the SV against its own
    BFS for counts ≤ 9.
156. **Question 0087, Lights Out (session 32, 2026-11-06).** Senior / hard, Python and SV,
    advanced-algorithms path before 0081. Neighbours up, down, left, right (5, 4 or 3 lights
    flip). Part a: 3×3, rank 9 (the top row lit: presses 3, 4, 5, 7), GF(2) elimination on
    bit vectors (`press_masks`, `gauss`, `solve_lights`; `solve` is an SV keyword). Part b:
    6×6 rank 36; 5×5 rank 23 (a quarter solvable, 4 solutions each, three quiet patterns,
    the parity test); light chasing with n equations for the first row. Part c: with
    diagonals the effect is P·X·P, P singular iff n ≡ 2 mod 3, 2n − 1 free variables, full
    proof. Part d: free variables = deg gcd(p_n(x), p_n(x+1)) (Sutner), checked against the
    rank to n = 40; coprime ⇒ solvable proved, the converse cited; bad sizes to 20: 4, 5, 9,
    11, 14, 16, 17, 19; "all lit" always solvable on any graph. q0087.py (11 blocks),
    lightsout.js (play with the solution or a quiet witness; chase step by step),
    stylesheets/questions/0087-lights.css, eight contrast pairs. Tests: brute force to 3×3, random boards to 8×8,
    the follow-ups (torus, rectangles, m+1 | n+1, 15 presses for 5×5 all lit), Node, SV.
157. **Question 0088, differences in a circle (session 32, 2026-11-06).** The owner chose three
    of eight new proposals (0088 to 0090) after rejecting several rounds of classic puzzles.
    Junior / medium, Python and SV, logic-puzzles path after 0086. Part a: 2, 6, 11, 4 to
    zeros in 6 rounds; the max never rises; mod 2 a round is XOR, after 4 rounds everything
    is even; halve and induct, at most 4(⌊log₂M⌋+1) rounds. Part b: n = 2^k by Pascal's
    triangle mod 2, `parity_step` / `always_zero`. Part c: any other n has a start that
    cycles; cycle lengths for n = 3..10; that every cycle holds only 0 and one c is cited
    (Burmester, Forcade and Jacobs 1978) and checked exhaustively to n = 10. Follow-ups:
    Tribonacci starts (13 and 25 rounds), a real start that never ends, Floyd. q0088.py,
    ducci.js (the circle round by round, presets, a chart of the max), stylesheets/questions/0088-ducci.css, nine
    contrast pairs. The single-1 check runs to n = 18 only (59 numbers has astronomically
    long cycles and ran out of memory).
158. **Question 0089, coins you cannot make up (session 32, 2026-11-06).** Junior / medium,
    Python and SV, digits path after 0085. Part a: 3 and 5 → 7 (columns mod 3 headed by 0,
    10, 5). Part b: g = ab − a − b both ways, Sylvester's (a−1)(b−1)/2 and the symmetry n /
    g − n, gcd > 1 has no largest; `two_coins`, `can_pay_two`. Part c: 6, 9, 20 → 43;
    Dijkstra on the residues mod the smallest coin (heads 0, 49, 20, 9, 40, 29; g = max −
    a) against the plain run (`frobenius_dp`). Traps: the gcd (4, 6), the run 38–42, greedy
    on 24, abc − a − b − c. q0089.py, frobenius.js (line, residues stepped, pay),
    stylesheets/questions/0089-frobenius.css, eight contrast pairs. Tests: g three ways for all pairs ≤ 12 and
    triples ≤ 10, the formula, count and symmetry for a ≤ 15 and b ≤ 24, Node, SV.
159. **Question 0090, pancake sorting (session 32, 2026-11-06).** Senior / hard, Python and
    SV, advanced-algorithms path after 0081. A stack is written top first. Part a: largest
    first, at most 2n − 3 flips with a proof; the example [3, 1, 5, 4, 2] takes 7. Part b:
    one BFS from the sorted stack gives P(n) = 0, 1, 3, 4, 5, 7, 8, 9 for n = 1..8; the
    example in 5; known bounds as context. Part c: burnt pancakes as signed sizes; up, turn,
    down, at most 3n − 2; BFS gives 2n for n = 2..7 (15 at n = 8 cited). q0090.py,
    pancake.js (click to flip, flips against the BFS minimum, hint, plain or burnt),
    stylesheets/questions/0090-pancake.css, seven contrast pairs. Tests: every stack against the reference, Node, SV.
160. **Question 0091, Chomp (session 32, 2026-11-06).** The owner chose three of eight
    proposals (0091 to 0093) and set the order of each: a specific case first, then the
    general one. Senior / medium, Python and SV, advanced-algorithms path after 0082. Squares
    named like a chessboard, the poison a1. Part a: 4×4, b2 leaves an L of equal arms, then
    the mirror (`mirror_move`). Part b: every n×n; positions are staircases; memoized search
    (`eat`, `moves`, `wins`, `winning_moves`; the SV iterative in lexicographic order, 4 bits
    a column, up to 8 columns); 8×8 has 12,869 positions with the poison and b2 is the only
    winning first move. Part c: strategy stealing, the top-right corner loses on 3×3, two
    rows by `two_rows_move`, a table of the winning first moves for 1–7 rows by 1–8 columns
    (each unique). q0091.py, chomp.js (play against perfect play with winning and losing
    squares marked; the mirror on n×n), stylesheets/questions/0091-chomp.css, eight contrast pairs.
161. **Question 0092, points on a circle (session 32, 2026-11-06).** Student / medium,
    Python and SV, geometry-motion path after 0080. Part a: 5 points → 16; each chord adds 1
    + the chords it crosses. Part b: 6 points → 31, not 32; C(n,4) + C(n,2) + 1 proved chord
    by chord and by Euler (V = n + C(n,4), E = n + C(n,2) + 2C(n,4)); the pattern equals
    2^(n−1) only while n ≤ 5. Part c: `count_regions(angles)` from coordinates; the regular
    hexagon gives 30; a point of m chords loses C(m−1, 2); regular polygons 3–12 computed,
    odd n on the formula (Poonen–Rubinstein, cited). q0092.py (faces traced by a half-edge
    walk), circlecut.js (drag or keyboard points, regular mode, chords one at a time; the
    SVG is kept and only its content redrawn so keyboard focus survives the figure
    wrapper), stylesheets/questions/0092-circle.css, seven contrast pairs.
162. **Question 0093, stable matching (session 32, 2026-11-06).** Junior / medium, Python and
    SV, coding path (last). Candidates A–F and jobs 1–6, chosen by search: 5 stable
    matchings, every partner different between the extremes. Part a: a greedy matching with
    3 blocking pairs; proposals take 11 in 5 rounds. Part b: `gale_shapley` with a rank
    table, at most n² − n + 1 proposals (reached), stable, proposer-optimal,
    receiver-pessimal. Part c: all 720 matchings give 5 stable ones; best for one side =
    worst for the other; the lattice. Follow-ups: capacities, roommates with no stable split,
    lying. q0093.py (`rtl_cells` puts an RLM before cells that start in Latin), matching.js
    (two right-to-left tables, proposals step by step, who proposes, editing), stylesheets/questions/0093-match.css,
    nine contrast pairs.
163. **The explorer jobs' time limit (session 32, 2026-11-06).** With 92 questions each of
    the four explorer shards takes 15 to 18 minutes; twice a slow Chromium install (9 to 10
    minutes) on one shard pushed it past the 20-minute limit and the run was cancelled. The
    limit is now 30 minutes (deploy.yml). If it keeps growing, add a fifth shard rather than
    raising the limit again.
164. **The repository's files reorganized (session 33, 2026-11-06).** The owner asked to put
    the many files in order and to update the README, and chose after guiding questions:
    the working notes in `notes/` (`HANDOFF.md`, its archives, `VIDEOS.md`, `CATALOG.md`;
    `paths-ignore` and the fast lane now ignore `notes/**`); the three requirements files in
    `requirements/` (`site.txt`, `dev.txt`, `video.txt`); `tools/` split into `checks/`
    (everything CI runs, `text_only.py` and `run_tests.py` included), `build/`
    (`catalog.py`, `graph.py` and its data, `search_text.py`, `make_icons.py`, the social
    card layout in `build/social/`, `codemirror/`) and `authoring/` (`new_question.py` and the
    page template, formerly `templates/question.md`); the modules every part imports
    (`extract_code.py`, `page_tests.py`, `explorer_node.js`) and `dev_setup.sh` stay in
    `tools/`, and `tests/conftest.py` puts all four folders on the path. The social layout
    did not go to `overrides/`: MkDocs copies the theme folder's files into the site. The
    stylesheets of single questions moved to `docs/stylesheets/questions/<id>-<name>.css`
    (26 to 36 became 0083 to 0093); the hook accepts that form in `extra_css` and
    `check_contrast.py` reads them after the numbered parts. This file kept sessions 31 to 33;
    sessions 22 to 30, the redesign plan and the proposal series 6 to 8 moved to
    `HANDOFF-archive-2.md`. README has a map of the repository, the counts (92 questions, 13
    paths) and the check commands. Every reference was rewritten (CI, CLAUDE.md,
    CONTRIBUTING.md, the hook, the tools' usage lines, the video scripts' comments); checked
    with the Python tests of every question, the tools and hook tests, the lint, the
    contrast check, the strict build, the link check, the phone check on 0083 to 0093 and the
    home page, and the explorer check on 0083 and 0093.


---

## In progress

- **Session 33 (2026-11-06):** the repository's files reorganized (work log item 164):
  the notes in `notes/`, the requirements in `requirements/`, `tools/` split into
  `checks/`, `build/` and `authoring/`, the questions' own stylesheets in
  `docs/stylesheets/questions/`, and this file shortened (`HANDOFF-archive-2.md`).
- **Session 32 (2026-11-01 to 2026-11-06):** questions 0072 to 0093, videos, the UX
  rounds; see the work log items 117 to 163. All on `main`.
- **Waiting on the owner:** ten videos wait for their YouTube ids (`video:` in the front
  matter); the giscus ids (README, Comments) in `extra.comments` of `mkdocs.yml`; checks of
  the live site at 390 px and on a desktop, light and dark (github.io is not reachable
  from the cloud sandbox); a lint rule for numbers laid out from the right was offered
  and not answered (do not add it without a yes).
- **Decision (owner, session 20): the repository stays public.** The options kept for
  later are in `HANDOFF-archive-2.md` ("In progress notes").

## Open items

### Owner decisions

- [x] Staff level removed (session 19, owner's call). Senior has nine questions (0007, 0011, 0019, 0020, 0021, 0023, 0024, 0025, 0037).
- [ ] Fifth series: W1 to W4 done on the branch (W348's drawn check mark not picked); W5 not picked; `main` when the owner asks.
- [ ] Pick rounds from the proposals (now in `HANDOFF-archive-2.md`): the owner's current direction is the eighth series, S1 to S6 (improve what exists, no new questions); the question proposals X360 to X410 wait; the older proposals are in the archive.
- [ ] Colons: many pages and explorer strings put a plain space before a colon in Hebrew text (0065 to 0067 and their boxes have no NBSP at all), and the linter does not check it. The owner chose not to fix it for now (2026-10-30).
- [ ] Comments: enable Discussions, install the giscus app and paste the two ids into `mkdocs.yml` (README, Comments); until then question pages have no discussion section.

### Content

- [ ] Add questions as they arrive (rewrite, translate code, execute, draw figures).
- [x] ~~Explorer state outside the controls is not in the box link or the remembered state~~ (done in session 22 with `box.dvqExtra`, work log item 33)
  (code review, session 22): the hand-made cuts in 0020 and the dragged sandbox shapes in
  0014 come back as the greedy split and the start positions after a reload or from a
  copied link. Give these boxes an `opts.state` codec like the five boxes that have one,
  or mirror the state in a hidden input.
- [x] ~~Re-run the 0007, 0011 and 0014 constraints in a simulator with full constraint support~~ — done in session 5 (Verilator snapshot + z3 in CI).
- [x] ~~Wide data tables still scroll sideways on phones~~: tables of five or more columns that do not fit become cards on phones (C192, session 22).
- [x] ~~0038: the checker missed an ack in the rise cycle~~ (fixed, work log item 151).
- [ ] Figure labels under 11 px on phones (work log item 148): the D194 fit raises them to 9.5 px only; 11 px needs fewer value labels and more room in `charts.py`'s `tick` and `legend` and per generator (0028, 0044 first).
- [ ] When a Verilator release newer than 5.052 is out, bump `VERILATOR_REF` to its tag and check that 0011 and the 0014 subclass still pass.

---

## Question variety

### Coverage (session 27, 69 questions; 92 since session 32)

| Level | Questions | Main topics covered |
|-------|-----------|---------------------|
| Student | 0001, 0002, 0003, 0010, 0012, 0015, 0032, 0036, 0040, 0048, 0064 | digital logic, bitwise, sorting, stack, digit puzzles (with number bases in 0012 part c), conditional probability, BFS over a tiny state space (wolf, goat and cabbage), LFSR periods and primitive polynomials, the shortest path by two reflections (the farmer, the food and the water), weights for every load in base 2, balanced base 3 and balanced base 2c + 1 (0064) |
| Junior | 0004, 0005, 0006, 0008, 0009, 0013, 0014, 0016, 0017, 0018, 0026, 0027, 0028, 0029, 0030, 0031, 0033, 0034, 0035, 0038, 0039, 0041, 0042, 0043, 0044, 0045, 0046, 0047, 0049, 0051, 0053, 0055, 0056, 0058, 0059, 0060, 0061, 0062, 0063, 0065, 0066, 0067, 0068 | FIFO depth from rates, Gray pointers and CDC, a divide-by-3 clock, SVA for a handshake, logic puzzles, BFS (remainders, hourglass states), O(n) scans, permutations, SV constraints, Josephus (proof), cycle detection, motion and speed ratios, sequences and a single-peak proof (cake split), relative speed and counting with inclusion-exclusion (clock hands), geodesics on a box by unfolding (spider and fly), Dijkstra over a bitmask state with the greedy rule (bridge and torch), a price list per load and a range function (the camel and the water), selection from partial orders (horse races without a stopwatch), the Kaprekar step as code with a hash and a closed form for the digits (0044), the odd ball in fewest weighings (0045), the largest square, rectangle and right triangle of ones by dynamic programming and a stack (0046), trapping rain water by two pointers and a heap (0047), the UVM testbench architecture (0049), poisoned bottles as digits in base b + 1 (0051), an ALU covergroup and its closure time (0053), a divisible-by-m state machine from the MSB and the LSB (0055), ants on a pole by ghosts (0056), coins in a row by a parity trick and an interval DP (0058), the next number with as many ones by Gosper's hack, the previous by the complement, and the same for zeros across lengths (0059), the longest run of ones with k flips by a sliding window, and of one value on a bus (0060), the tags a list of transactions needs by an event sweep, one pool and two (0061), the sliding-window maximum by a monotonic deque, the window with max − min <= limit, and the same in hardware (0063), islands in four and eight directions (0065), merged intervals and the total height per piece (0066), BFS and Dijkstra for a broadcast time (0067), the median and the p-quantile of a stream by two heaps (0068) |
| Senior | 0007, 0011, 0019, 0020, 0021, 0023, 0024, 0025, 0037, 0050, 0052, 0054, 0057, 0069, 0071 | a three-wizard duel solved backward (0071), synchronizer MTBF, SV constraints, randomization, probability, combinatorics, Dijkstra on a state graph, PCIe completion rules, recursive enumeration, counting formula with proof, generalized Josephus (recurrences, induction), a PCIe endpoint reference model (classes, block memory, scheduling), a USB4 credit flow-control reference model (modulo counters, loss and resynchronization), a PCIe Ack/Nak reference model (Retry Buffer, Replay, error handling), an out-of-order scoreboard (0050), waiting times of coin patterns and Penney's game (0052), round-robin and weighted arbiters with SVA (0054), a constant-memory checker for missing tags (0057), overtakes in a stream of responses by a Fenwick tree (0069) |

Algorithms and puzzles are well covered; 0020 / 0021 / 0023 / 0024 / 0025 are the protocol questions (PCIe, USB4), with 0023, 0024 and 0025 reference models.
Round R (session 18) opened the DV-core shelf: FIFO depth, Gray pointers / CDC, a clock
divider, an LFSR, synchronizer MTBF and SVA; 0040 (a sequence detector FSM) and 0041
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
  `VERILATOR_REF`; the same recipe is in `README.md`) and `z3` must be on the PATH. The
  5.052 release crashes on 0011 and mis-randomizes the 0014 subclass; the apt package
  (5.020) has no constraint support. `run_tests.py` refuses older versions.
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
    master after 5.052 (the pinned commit in CI). z3 prints `%Warning-UNSATCONSTR` for an
    unsatisfiable `randomize() with`, which the 0007 and 0011 testbenches trigger on purpose.
  - Icarus does not support `ref` ports or `break`.
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
