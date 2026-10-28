# HANDOFF

Living task list for this repository: what was done, what is in progress, and what comes
next. Update it at the end of every work session so anyone (human or AI) can pick up
where the last session stopped.

_Last updated: 2026-10-27 (session 27)_

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
| Code languages        | SystemVerilog + Python, as linked tabs (SystemVerilog first)             |
| Solutions             | Collapsed by default (practice mode); one collapsed solution per sub-part |
| Multi-part questions  | One file, `### סעיף א/ב/ג` with a solution after each part               |
| Owner's own code      | Kept as sent (comments added, minimal bug fixes called out to the owner) |
| Workflow before adding | Ask the owner guiding questions first, then implement                   |
| Tests                 | Python: full tests of the page code. SystemVerilog: Verilator built from a pinned development commit (after 5.052) with z3, so every class runs as published; a translation by intent (fingerprinted) is allowed only for a proven simulator bug, and none is needed today |
| Failing tests         | Block the deploy; the live site keeps its previous version              |
| Run button            | Per question, Python only (Pyodide in a web worker); SV cannot run in a browser, the panel says it is checked in CI instead |
| Position levels       | Student / Junior / Senior; the Staff level was removed on 2026-10-21 (owner: no staff questions planned) |
| Look and feel         | Own navy + amber palette, logo and footer; level / difficulty as CSS chips; one header card per question (see **Site redesign plan**) |
| Next rounds (2026-10-27) | Owner: no rounds of new questions for now; only improve the existing questions, the site and its interfaces (series S). The question proposals X360 to X410 stay listed for later |
| Closed (2026-10-27) | Owner: no run panel for questions without Python code, no print style, and 0001 stays as it is; not to be proposed again |

---

## Work log

The work log of sessions 1 to 21 is in [`HANDOFF-archive.md`](HANDOFF-archive.md). The
section below starts at session 22, whose numbered items run on through the later sessions.

### Session 22 — 2026-10-23: round L, first batch (L311, L312, L313, L316, L317, L318)

1. **The owner's picks:** round L, then round K, with clarifying questions before each
   round. Answers for L: the proof view is a panel inside the existing box (under its
   drawing, driven by the same controls; no new boxes), L in two batches (the small
   items, then L309, L310, L314 and L315) with `main` only when the owner asks, the
   search of L314 as both a queue list and a small tree, and the renumbering of L309 as
   two labels on the circle.
2. **The proof panel** is `<section class="ex-proof">` with a title "שלב ההוכחה : …"
   (CSS in `extra.css`, hidden with `[hidden]` when it does not apply). Each page's "נסו
   בעצמכם" paragraph names it; the README table rows mention it.
3. **L311, 0026:** a drop-point slider D (step 0.005, so 7/8 is on it) and "ה-D של
   התוכנית"; the chart of both arrival times against D (the passenger's falling, the
   walker's rising), their maximum as a wide band, the minimum marked, and a sentence
   for the current D. The height follows the dragged point. Shown for two riders only.
   Model `motorcycleDrop(alpha, d)`, tested against the exact replay of the page test.
4. **L312, 0027 and 0028:** the condition curve (f(p) = p² / (1 − p) against y = d, or
   q (1 − p) against y = 1), the threshold T, and the people seen so far as dots on it
   (before the peak, the peak, after), so stepping person by person shows the dots move
   one way and cross once. Model `cakeCondition`, tested against the exact shares on the
   grids of both pages (the person before the last excluded, as the proof's step 5).
5. **L313, 0036:** every cycle of the polynomial as its own small ring (the fixed point
   0 first, the seed's cycle with the thick frame, the current state lit), cropped to the
   rings so a phone shows them large, and the lengths in words (6 + 6 + 3 = 15 for
   x^4 + x^2 + 1). Up to 6 bits drawn, beyond that the lengths only. Model `lfsrCycles`,
   tested for every polynomial of 3 to 8 bits.
6. **L316, 0032:** "השכבה הבאה" fills the state graph layer by layer: the depth on every
   state, the newest layer lit, an arrow from every parent one layer up, and at layer 7
   both shortest plans; the sentence names each new state and where it came from. Model
   `riverLayers`, tested against a plain BFS and the generator's two solutions.
7. **L317, 0043:** a tap (or Enter) on a horse frames the horses known faster than it,
   draws an arrow per direct result on the chains, marks the races used in the table,
   and the panel lists the chains with their races and the verdict (out, settled,
   candidate). Model `horsesChain`, tested after every race of three seeds: the chains
   are direct results, reach exactly the known-faster set, and are as short as a BFS.
   One Hebrew colon in the step line got its NBSP.
8. **L318:** the help lines of `boxes3` and `ttt` name the buttons that exist.
9. **Checks of the first batch:** Python tests (340), lint, strict build, links, the phone check with axe
   (55 pages, none with problems) and `check_explorers.py` (every button of every box, the links and the remembered state).

10. **Second batch, L309:** "עד סוף הסיבוב" and a checkbox in the 0016 box: after any
    step every person left gets a green new label (the position in counting order from
    the next one who stays) outside the circle; the text reads F(N) off F of the smaller
    circle, the recurrence F(N) = (F(N − L + 1) + L) mod N after one step, and, when the
    old labels are a·new + b (after a full round), F(N) = a·F(N') + b: F(2k) = 2F(k) and
    F(2k + 1) = 2F(k) + 2 for L = 2. Model `josephusRenumber`, tested for N up to 40 and L
    2 to 6 against a plain simulation.
11. **L310, 0009:** the long cycle as a row of its boxes, a tap picks c_h (the ring above
    applies that cut while person 0 is on), and a chart of the larger piece for every h
    against N / 2: the safe range L − N/2 ≤ h ≤ N/2 always holds the middle. Model
    `permCutAt`, tested on the page's Room and cycle_from.
12. **L314, 0018 and 0019:** the page's own search, pop by pop ("השליפה הבאה", "עד
    המטרה"): the popped state, its children with what happens to each (new, seen, past D,
    nothing runs; in the Dijkstra also "start", better and stale), the queue as chips, and
    the search tree with the path to the goal (the owner's choice: both the list and the
    tree). Shown for two hourglasses and the page's objective. Models
    `hourglassSolveTrace` and `hourglassIntervalTrace`, tested on the grids of both pages
    (FIFO order, depths, t order, the goal path is the page's plan; 16 pops in 0019's
    example, as its cost section says).
13. **L315, 0008:** "מזיגה" pours the points left into the cups still to come, each to
    Israel's total, with the spill beside them (17 after France), animated. Model
    `euroPour`, tested against israel_cannot_win after every announcement.
14. **Found by `check_explorers.py`:** a cut away from the middle leaves a cycle longer than
    N / 2, and its chip in the 0009 cycle line did not wrap (427 px at phone width); a long
    cycle's chip now wraps.
15. **Round L is done.** The owner's answers for round K: the mechanism on the existing
    drawing with a toggle (no new panel), the small items first (K303, K304, K307, then
    K301, K302, K306, K305, K308), K305 both as a small sandbox of two rectangles and as
    the rejected candidate marked in the main box, and `main` fast-forwarded once round L
    passes every check.

16. **`main` fast-forwarded** to 4847d65 (round L) after the full checks: 734 clicks, no
    problems.
17. **Round K, first batch (K303, K304, K307), each a toggle on the existing drawing:**
    0042 "המחירון על הדרך" draws a band under every stretch with its crossings so far out
    of 2j − 1 and the litres per km, and a line with the prices (`camelCrossings`, tested:
    every stretch crossed 2j − 1 times, the burnt water adds up to w − T); 0020 "לבחור
    חיתוכים בעצמי" turns the inner boundaries into buttons, the completions they form drawn
    under the blocks (one above MPS in red), and the line counts the valid subsets of the
    2^|B| (`pcieSplitOf`, tested on every subset of five requests against the page's
    rules and splits); 0019 "ההסתעפות" draws the run-outs of each glass flipped every
    time (multiples of 7 and of 11) and the fork at t = 11 into 14 and 15
    (`hourglassFork`, tested for every pair of sizes up to 12).
18. **Round K, second batch, again as toggles on the existing drawings:** 0039 "הנוסחה על
    הבניין" puts two bands beside the building at the next drop, f(k − 1, t − 1) floors
    below it in green and those above in blue, with the sum in a line (`eggsSplitAt`,
    tested against sums of binomials at every drop of many thresholds); 0040 "איך נבנה
    המעבר" shows both edges out of the current state as the input with the pattern slid
    under it to the longest match (`seqFallback`, tested for every pattern up to 6 bits
    against the KMP table); 0031 "הכלל החמדני" tables the rounds, both ways to move the
    two slowest and the cheaper one, ending at the search's time (`bridgeGreedy`, tested
    on 150 random sets); 0014 "ההטלות על הצירים" draws a rejected candidate's projections
    and those of the shape it overlaps, and a sandbox of two shapes to drag (or move with
    the arrow keys) lights the page's four cases (`shapesWhy`, tested against the page's
    overlap); 0013 "החיסור במאונך" lays the first step out by columns with the borrows and
    the digits p and q predict (`kapColumns`, tested on every seventh number against the
    page's table). The same toggle shows on 0012 with three digits.
19. **Round K is done.** Checks: Python tests (353), lint, strict build, links, the phone check
    with axe (55 pages, none with problems) and `check_explorers.py` (749 clicks, none).
20. **CI had been red since cb34d66 (session 21), so the site was not deployed:** the click
    check failed every page on a console error from the theme's repository widget, whose
    request to the GitHub API gets 403 when the runner is rate-limited (the sandbox runs
    with `--offline`, which hid it). A failed load from another host no longer counts; a
    failed local resource still does. The fix went to `main` alone (84bc64f, on top of
    round L) and was merged into the branch; round K followed to `main` on the owner's
    request. Lesson: after a push, wait for the deploy run and read it, not just the local
    checks.
21. **Code review of round K (nine findings); the owner picked seven to fix:** 0020's
    hand-made cuts now follow the greedy split of the current parameters until a boundary
    is clicked, and a clicked split stays while its cuts are boundaries (an empty greedy
    list and an MPS change used to keep the old split and report it as invalid); 0039's
    recurrence line says "fewer than f(e − 1, t − 1)" when the drop stops at the last
    unknown floor, instead of "exactly"; the 0019 fork labels get room inside the frame
    (A = 7, B = 11, D = 4 clipped "flip A: 15"); the 0014 sandbox is redrawn only when it
    changes, so the animation no longer takes a dragged shape's keyboard focus; the 0031
    greedy toggle is disabled with a note on a bridge of three, and the 0019 fork toggle
    with a third glass; `check_explorers.py` ignores failed loads from api.github.com only
    (a CDN script that fails still fails the check). Not fixed: old `#ctl-` links that
    predate the new toggles (none exist: the deploy was red from G220 until round K) and
    the state outside the controls, now an open item.
22. **Round I, first batch (I284, I286, I290).** The owner's answers: each new box locked on
    its part, and `main` only at the end of round I. 0002 parts a and b get their own
    `trace` box (`data-version="temp"` or `"arith"` hides the version select; part a also
    hides the 8-bit toggle, overflow being part b's); 0006 part a gets a `stock` box with
    `data-mode="long"` (no mode select, a link cannot turn the short on); 0012 part b gets
    `kapbase` on base 10 with `data-fixed` (no base slider), after a new paragraph that
    reads k' = max(10 − k, k − 1) off the candidates table, with 352's path 3 → 7 → 6 → 5.
    Two fixes on the way: a codec link (`#state-<kind>.…`) always opened the first box of
    its kind, and now names the n-th as `#state-<kind>-<n>.…` (0006 has two stock boxes);
    and `.explorer label { display: flex }` overrode the `hidden` attribute, so hidden
    labels showed (the 0002 "c" field showed in every version, not only the rotation).
    Links and remembered state made before this batch for the later boxes of 0002, 0006
    and 0012 now point one box earlier (a day's worth; the page-attribute check drops a
    remembered state that does not fit).
23. **Round I, second batch (I291, I287, I292), three new kinds.** The owner's answers: the
    0013 box goes under the static chart, which stays (it prints and needs no script); x
    on a slider up to 40, stopping at the first collision; the 0017 box has its own
    array, starting from the page's example. `kappairs` (0013 part b): the 54 pairs as
    the chart's grid, a click (or the select, which carries the link) shows the
    difference, the digits of step 3 with the largest and smallest marked, the case of
    step 6 (several on a tie) or step 5 for q = 0, conditions a and b, and the arrow to
    the next pair with the rest of the path to 6174 fainter (`kapPair`, `kapPairPath`,
    tested on every pair against the proof's expressions and the page's step). `repunit`
    (0005 bonus): R1, R11, … dropped into the x remainder slots, each remainder from the
    one before, the shared slot lit, and R_i − R_j written as x times the quotient
    (`repunitDrops`, `repunitDiff`, tested for x up to 40; the page's x = 7 example is
    R7 − R1 = 1111110 = 7 · 158730). `dupbin` (0017 solution 3): the page's loop step by
    step, the counted cells lit, c(v) against y = v with lo..hi shaded, and the invariant
    per step (`dupBinarySearch`, `dupCounts`, tested against find_duplicate_binary and the
    page's table). The 0017 text first said the duplicate is the first value over the
    line; with several repeated values (the statement allows them) that is only true of
    one repeated value, and the page now says what the invariant gives.
24. **Round I, third batch (I285, I288, I289); round I is done.** The owner's answers: new
    boxes in the parts, not modes of the boxes above them; draws plus dragging for the
    half-circles; up to five cells. `labelfix` (0004 part b, solution 2, in `boxes3.js`):
    fix_labels step by step on three crates, k and the ball, same and other, swap 1 and
    swap 2 on the labels array, and the three arcs of the 3-cycle (same → k, k → other,
    other → same) lit as each label arrives, the true contents at the end (`labelSwaps`,
    tested on the twelve cases against fix_labels and the page's example table).
    `halfcirc` (0007 part c): P1, P2, P3 to drag or type, each half-circle as an arc in
    its point's colour with its half-disc when A_i holds, and 100 or 1,000 continuous
    random triangles counted per event against 1/4 (`halfEvents`, `halfCount`, tested on
    3,000 integer triangles against contains_center and on 40,000 draws). `tttfive`
    (0011 part b, default the page's 2 x 2 square): up to five cells, the four directions
    with their split and pairs on a line, the full line, and the stars on the empty cells
    that would complete one (`tttFive`, tested on every set of up to five cells: the
    directions are the page's 12 lines, every pair on exactly one, five cells always
    hold a line).
25. **CI broke again, outside the code:** the deploy run of fcca5a9 (the review fixes) failed
    in "Install Playwright": `ubuntu-latest` moved to Ubuntu 26.04, where Playwright 1.56
    cannot install Chromium. The three jobs of `deploy.yml` now run on `ubuntu-24.04` (the
    Verilator cache was built there too). The review fixes reach the site with round I.
26. **Round J, first batch (J294, J298, J300).** The owner's answers (four questions for
    the whole round): the Gray conversions as a mode of the existing box; sliders in the
    medium boxes; a new SVA box in part a with presets and editing; τ, T0 and the flop
    count in the Monte Carlo box. `gray` `data-mode="convert"` (0034 part b): forward
    the binary row, the shifted row with a 0 entering at the top and the XOR; back the
    binary bits one per step from the top, each the bit before XOR its Gray bit; the
    counter walk as a strip of the Gray bits over a full cycle with the one changing bit
    lit, b + 1 and play (`grayConvertSteps`, `grayWalk`, tested on every value of 3 to 6
    bits against bin2gray / gray2bin and the trailing-zeros rule). `gapline` (0029 part
    b, at the end of the proof): the angle difference in turns against time with the
    integers as lines and a dot per meeting, L in quarters of T, the interval closed,
    open or half-open with its ends filled or hollow and the three counts of formula 3
    (`gapLine`, `gapIn`, exact fractions, tested against counting k T in each interval,
    the page's table for 12 hours and the day's 1,416, 1,438 and 22). `tuesday` (0015
    part b, after "why 13 and not 14"): the 196 families counted in four steps (row,
    column, the shared cell once, two boys), a tap names a family, any weekday, and
    "at least one boy" (1/3) and "the elder is a boy" (1/2) on the same grid with the
    three answers in a table (`tuesdayCount`, tested against enumerating the families
    for every information and day).
27. **Round J, second batch (J293, J297, J299).** Three new kinds, each in the file of
    the box already on its page. `fifostairs` (0033 part a, in `fifo.js`): the words
    written and read as two staircases from the cycle simulation, the gap shaded, a time
    cursor with the counts, and the peak against the formula (`fifoStairs`, `fifoGapAt`;
    tested against the page's fifo_fill: the peak is its maximum, reached last at the
    last write whenever the reader is slower, checked on 22,464 cases while writing it;
    the page's 1,190 ns with 120 − 95 = 25). `stages` (0041 part a, in `coverage.js`,
    default seed 37, a run of 56 tests close to 54.1): the ribbon of tests cut into
    stages, a bar per stage against n / (n − i), the mean over 500 runs (`stageRun`,
    `stageExpect`, `stageAverage`; tested against expected_uniform and the page's
    waits table). `ladder` (0021 part b, in `pcie.js`): C(0..N), the terms of C(n) and
    a block strip per term (`ladderC`, `ladderTerms`; tested against counting
    compositions for m up to 6 and the page's table).
28. **Round J, third batch (J295, J296); round J is done.** `metamc` (0037 part a, in
    `mtbf.js`, seed 3): data edges folded onto one clock period with the T0 window,
    the settling times of the edges inside it against e^(−t/τ), the t_res cut moved by
    T_clk per flop, and a table of the two factors measured against the formula
    (`metaDraw`, `metaFactors`; tested against sync_mtbf, 19 seconds for one flop, and
    on 200,000 edges for the window share, the mean and the tail). With the page's
    numbers no edge fails, which is the point: the cut sits far in the tail. `attempts`
    (0038 part a, in `handshake.js`, default the late-ack trace): an attempt lane per
    property under the strip, a dot where the antecedent matched, the window as a
    bracket ending in ✓, ✗ or …, vacuous cycles grey, a cursor cycle explained and a
    count per property (`hsAttempts`; tested on the page's traces and 300 random ones:
    vacuous exactly where the antecedent fails, fails at the cycles of check_handshake).
    The owner asked for `main` after the round; `main` was fast-forwarded to the round's
    last commit. Final checks: all Python tests, lint 42/42, 0 broken links, 69 boxes
    and 1,010 clicks with no problem, 55 pages at 390 px with no problem.
29. **New question 0044, Kaprekar after n steps (the owner's write-up).** The owner sent a
    full solution: the closed form for the digits (a_n, b_n, c_n) after n steps of the
    three-digit routine, the answer after 1000 steps in base 10 (495) and base 5 (143₅ or
    242₅ by the parity of t = |d₀ − 3|), and any base B. Every table, example and
    closed form was checked first by brute force (every number of every base from 2 to
    16, n up to 59 and n = 1000): all hold, nothing to report. The owner's answers: a new
    page (0012 part c already has the fixed point and the cycle; 0044 is about when and
    how), junior / hard, no code, a new box. The page follows the write-up step by step
    (parts a, b and the bonus, the facts with their proofs, the 211, 401₅ and 300₅
    examples, the consistency table); math with Hebrew was rewritten (no `\text` in
    Hebrew, parity as ≡ mod 2 or in a table), and the wide equations split for phones.
    Figures (`q0044.py`): D_k for every starting gap in bases 10 and 5. The `kapn` box
    (one kind, three boxes: base 10 and base 5 fixed, the bonus free): the gap chart with
    the line part shaded and a table of the steps, the closed form beside the direct
    digits (`kapnStep`, `kapnRun`, `kapnGap`, `kapnFormula`, tested against the
    simulation for every base and starting gap). 0012's follow-up now links to 0044.
    Round Z's Z203, Z210 and Z217 are marked done (0039, 0040, 0041).
30. **0044: a state diagram at the top of the page (the owner's ask).** The owner's
    answers: one new box after the statement (the three `kapn` boxes stay in the parts),
    a snake layout closed by a loop or a back arrow, everything shown at once, and on
    every card the number in the base and in decimal, the gap d as the card's shade and
    the stage of the proof. `kapgraph` (in `kapn.js`): base 2 to 20 (digits up to J),
    three digits typed or drawn; cards right to left then back (one column under 520 px,
    redrawn by a ResizeObserver), elbow arrows between rows, a 2-cycle kept on one row;
    the table of a_n, b_n, c_n, d_n with the closed form checked on every row and the
    repeated value last; a tap on a card or a row explains that step (`kapgChain`,
    `kapgStage`; tested on every number of bases 2 to 12 and samples up to 20).
31. **The owner's interface plan, round 1 (D195, C191, A181, A183).** The owner picked
    four rounds from the open interface proposals, asked in this order: round 1 (D195,
    C191, A181, A183), round 2 (D194, D197, C192), round 3 (E200, E199 and the state of
    the 0020 cuts and 0014 shapes; G222 stays deferred) and round 6 (E31, E33, E34, E36;
    no E35), with multiple-choice questions per round. Round 1 answers: a colour and a
    side rail per block kind, a sticky map inside the solution, cost chips written by
    hand for every solution, a warning (not a failure) under 9 px.
    - D195: `check_phone.py` measures every SVG text at 390 px (font size times the
      figure's screen scale) and prints one "warn small text" line per figure or box with
      its smallest text; the first run listed 160 figures on 36 pages (most charts at
      about 6 px, the hourglass and bridge boxes under 5 px), which is round 2's list.
    - C191: `reading-tools.js` wraps each `#### ... { .sol-* }` label and its content in
      `div.sol-block.sol-block--<kind>`; colours `--sol-c-idea / steps / code / proof /
      cost` (amber, blue, purple, green, orange as text colours, 4.5:1 in both schemes)
      on the label, its icon and a side rail. The variables are set on `.md-typeset`, not
      `:root`, since the scheme attribute sits on `<body>`.
    - A181: a sticky `nav.sol-map` of chips (one per block, a coloured dot) above the
      first block of every solution with two or more blocks, under the part bar
      (`--part-nav-h`); the block being read is marked, and on a phone the row scrolls
      sideways to keep it in view.
    - A183: `<!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->` under the answer block,
      rendered by the hook (`COST_LINE`, `_cost_chips`) as `div.cost-chips`; written for
      all 70 solutions that have a complexity block (labels such as זמן, זיכרון,
      פלופים, השהיה, הטלות, values copied from each block). The linter requires the line
      when a solution has `.sol-cost` and a Hebrew label on every chip; the template has
      it. Tests: the hook's chips and the lint rule.
32. **The owner's interface plan, round 2 (D194, D197, C192).** Answers: a phone layer
    rather than a second SVG per figure, the explorer boxes included, legends as chips
    that wrap, cards only for wide tables.
    - D194 (`reading-tools.js`, "figure text on narrow screens"): a ResizeObserver on every
      inline SVG of the content (so a figure is fitted when first laid out, when the
      solution or tab holding it opens, and on resize) and a MutationObserver on every
      explorer box (refit once per frame after a redraw). Text that renders under 9 px
      gets a font size that renders at 9.5 px, at most 1.8 times its own; a label wider
      than the viewBox shrinks to fit, one past an edge moves inward (`translate`, not on
      labels with their own transform); rows of `text.tick` / `text.coord` with
      `text-anchor="middle"` at the same y are thinned when they overlap. `unfit()`
      restores the page sizes (the lightbox copy uses it). The phone check's small-text
      warnings fell from 160 figures to the few capped by the 1.8 limit (the bridge
      letters and the hourglass and pcie boxes at 7.5 to 8.4 px).
    - D197: under 30em every `viz-legend` entry is a small bordered chip; the chips wrap.
    - C192: tabular numbers in every content table; a table of eight or more rows that
      fits its column gets a sticky header (`data-long`, the scroll wrapper set to visible
      by `.table-fits`); a table of five or more columns and three or more rows that does
      not fit becomes cards under 30em (`data-cards`, measured on load, resize, toggle and
      tab change): the first cell as the card's title, the other cells as "column value"
      pairs in two columns. Nineteen pages have such tables at 390 px (0016's 20-row table
      among them); the row-per-value tables (0013, 0044) stay tables.
33. **The owner's interface plan, round 3 (E200, E199, the 0020 / 0014 state; G222 stays
    deferred).** Answers: a shared layer without rewriting the boxes, the answer lit in
    the boxes with one clear result, the state in both the link and the memory.
    - E200: `layout(box)` in `core.js` runs after every mount and tags each child of an
      `.ex-controls` row `ex-c-input` / `ex-c-action` / `ex-c-play` / `ex-c-other`; CSS
      `order` shows inputs, then actions, then playback, with one gap and one button
      size, and the keyboard hint is a status line with a dashed rule at the bottom. The
      DOM order is untouched, so every old `#ctl-` link and remembered state still
      applies.
    - E199: `lib.answer(box, text, marks)`: a `p.ex-answer` ("התשובה" tag and one line)
      after the box's summary, and `ex-answer-mark` on the answer's elements (an SVG
      stroke in the green series colour, `:not(#_)` to outrank the views' state colours;
      a tinted table row; an outline otherwise). Called at the end of the draw of
      josephus (the survivor), floyd and dupbin (the duplicate), kaprekar, kapbase and
      kapgraph (where the chain ends), eggs (the threshold), bfs01 (the path), river (the
      goal state), lfsr (the polynomial's row, primitive or not) and horses (the top c).
    - The state: `box.dvqExtra = { get, set }` in core; its text rides at the end of the
      `#ctl-` payload as `~!<text>` and is applied after the controls. `pcie` stores the
      clicked cuts as hex addresses ("-" for none), `shapes` the two sandbox rectangles
      once moved. Checked by clicking: the link and a reload bring both back.
34. **The owner's interface plan, round 6 (E31, E33, E34, E36; not E35).** Answers: one
    kind per question, the id and chips in the search results, the "continue" card and
    a "recently added" list, a "what's new" page from the `added` dates.
    - E31: `kind:` is a required front-matter field (`KINDS` in the hook: puzzle חידה 13,
      code קוד ואלגוריתם 6, design תכן חומרה 7, math מתמטיקה והוכחה 9, dv אימות
      ופרוטוקולים 8); a chip in the header card and beside the difficulty in the tables,
      a "סוג" filter group (`data-kind` on the rows). `new_question.py` takes `--kind`;
      the template has the field. The kinds were assigned by hand and are open to the
      owner's review: 0007 (math, though it has constraints), 0020 (dv) against 0021
      (math, the proof), 0039 (puzzle).
    - E33: the question page's search document: "0021 · title", its tags led by the
      level, difficulty and kind (the results show them as chips), no text, and a `qid`
      field ("0021 21") boosted 1e7, so "21" and "0021" both put the question first.
    - E34: `<!-- home-continue -->` (marks.js saves the last question page opened,
      `dvq-last`, and fills the card with its marks and "how long ago") and
      `<!-- recent -->` (the five newest by `added`) on the home page.
    - E36: `docs/new.md` with `<!-- whats-new -->`, every question by the day it was
      added (Hebrew dates, the newest first); a "מה חדש" tab and a footer link on every
      page (the hook appends it to `copyright` with the site's path).
35. **New question 0045, the odd ball on a balance (the owner's write-up).** Checked first
    by exact computation: the tree of part a on all 24 cases (at most 3 weighings), the
    codes of part b (distinct, no code with its negation, 4 against 4, the unused pair
    ±(1, −1, 1), the weighings listed), the general code of part c on every N from 3 to
    364 (always the fewest weighings), k = ⌈log₃(2N + 3)⌉ against the table up to N =
    1999, the 13-ball argument (9 non-zero codes per column) and the N = 13 trap. All
    hold. One wording point: step 4 of part c said "first digit 0 (off the scale)" while
    the digits there are {0, 1, 2} (0 = right); the page says "0 in weighing 1" in the
    {+1, −1, 0} notation. The owner's photos use another valid partition for 12 balls
    (1, 2, 6, 8 against 3, 4, 5, 7, …); the owner chose part b's table for the box.
    Answers: junior / hard / puzzle, SystemVerilog and Python, the box with N from 3 to
    39, the table sorted by the outcomes as in the photos. The page keeps the owner's
    Python as sent (the statement's Hebrew docstrings included) and adds SystemVerilog:
    a `virtual class scale` with `weigh(left[$], right[$])` returning +1 / −1 / 0 and an
    `odd_t` struct; the tree, the fixed codes and `odd_ball(n, s)` (the orbits, the
    trimmed last orbit, the genuine balls). Tests: pytest (all three solvers, every N
    from 3 to 364 with equal pans asserted, the page numbers, the explorer against the
    page's pans for every scenario of N from 3 to 39), Verilator (a hidden-ball scale
    class; N from 3 to 130 and 363), the run panel's demo (the owner's harness).
    The `oddball` box (two boxes: part b fixed at 12, part c free): a row of balances per
    weighing, the decision table, a scenario from a row or from the ball and kind fields.
    Verilator was built locally from the CI's pinned commit for this (with z3).
36. **New question 0046, the largest square and rectangle of ones (the owner's write-up).**
    Checked first: both Python solvers against a brute force on 10,000 random grids up to
    7 × 7, the dp table of the square example, (9, (0, 2), (2, 4)) and the second 3 × 3
    square, the heights per row of the rectangle example (best 4, 8, 6), the stack trace
    of row 1 (areas 2, 4, 6, 8, 5) and the 2 × 2 square of that grid. All hold. The
    owner's "common mistake" note had no example; the trap uses [[0, 1], [1, 1]] (width 2
    and height 2 at (1, 1), best rectangle 2). Answers: a box in each part (square, then
    rectangle, with a mode select), a grid up to 16 × 16 edited by tap, drag (then set to
    1 or 0) and a random fill at a probability of 1, the heights and the stack with the
    rectangle being checked, SystemVerilog and Python with the owner's tester. The page
    keeps the owner's Python as sent and adds SystemVerilog (`shape_t`, corners -1 for no
    shape, `bit grid[][]`). The tester sits in the interviewer block fenced as `py`, not
    `python`: the run panel and `load_python` run the python blocks in page order, and the
    tester calls the solvers before the solutions define them; the test runs it after
    them. Kind `code`, junior / medium. Tests: pytest (every grid up to 3 × 3 and 2 × 5,
    3,000 random grids, the edge cases, the owner's tester, the page numbers, the explorer
    against the page for 155 grids up to 16 × 16: dp, heights, every stack event, the
    answers and the tie counts), Verilator (the examples, the edge cases, 3,000 random
    grids against a brute force). The `maxones` box: the grid and the dp (or heights)
    matrix side by side, a step per cell (square) or per row update, push and pop
    (rectangle), "next row" and "to the end", the best so far in orange, the checked
    rectangle dashed, the answer green with the count of ties; the link carries the grid
    and the step.
37. **The owner's look-and-feel plan, parts 1 to 4 (UI319, UI320, UI321, UI324, UI325,
    UI327, UI328, UI330).** Split into seven parts; the owner picked 1 to 4, with
    multiple-choice questions before each. Part 1: Rubik kept with line height 1.7, firmer
    headings, tabular digits and a 75-character cap on paragraphs and plain lists; a line
    icon per kind (Material Design Icons as CSS masks, `kind-ico`); the path cards' count
    no longer wraps and each path carries its dominant kind's icon. Part 2: the header as
    one chip row with small badges (icon and word) and the tools beside it as icon buttons
    with tooltips (open / close all as one toggle), a quiet line of topics, Hebrew date and
    source; the part bar became the page's sticky bar (part chips, the solved toggle once
    the header is gone, a reading-progress line; pages without parts get the line and a
    floating button fixed under the site header). Material's own header already shows the
    title on scroll, so the bar has none. Part 3: the home hero (`<!-- hero -->` …
    `<!-- /hero -->`): a navy card with a waveform pattern, "start practising" to the
    first unsolved question, a random question, a search field and ready searches that
    open the site search, one line of numbers (the stat tiles removed). Part 4: every box
    a card with a header (title, help / reset / link as icon buttons), playback as one
    left-to-right icon bar (`transport()` moves the views' own buttons; the word stays as
    the name and tooltip; "עצירה" shows pause), the speed select hidden behind ×1 ×2 ×4,
    and a scrubber that presses the box's own start / next buttons (not a control of the
    link). A new badge failed contrast (white on the accent) and now uses navy text.
38. **Part 6 of the look-and-feel plan (UI326, UI329, E201).** The owner picked the
    message with confetti only at the end of a level, the level's progress with a link to
    the next unsolved question, the shared flash plus tweens in a few kinds, and the
    first-visit guide (not the export of the marks). UI326: the toolbar carries the
    level's ids, links and page (`data-level-*`); `question-tools.js` shows a navy message
    at the bottom ("פתרת n מתוך m שאלות ברמת …", a bar, "לשאלה הבאה שלא פתרת (id)", or
    the level page when all are solved), pops the check mark, drops 40 confetti pieces
    when the level is complete, and offers an undo when the mark is taken off. UI329:
    `motion()` in `core.js` arms on the first trusted pointer or key event in a box (so
    restores, links and the page checks never animate), snapshots the box's short values
    by their path of child indices after every redraw, and flashes up to eight that
    changed (a reshuffle of texts already shown, an emptied value and a new picture do
    not); in `TWEEN` kinds integers count to their new value and SVG bars grow or slide
    (Web Animations, transform-box fill-box); the flash lasts 80 % of the time since the
    last redraw (160 to 600 ms), so ×4 play keeps up; the answer marks pulse once. A first
    pass flashed whole reshuffled lists in josephus, lfsr and credits, hence the eight-value
    cap and the reshuffle rule. E201: `guide()` on the page's first box with a playback
    bar, once per browser (`dvq-guide` in localStorage, set when shown), when 60 % of the
    box or half the screen shows; hints for the playback bar, the largest figure (inside
    it) and the summary line, "הבא" / "דילוג" / Escape; none under `navigator.webdriver`
    unless the address has `?guide`. Also fixed: on phones the first three toolbar
    tooltips overflowed the right edge; they now open leftwards. axe on the message and
    the guide (light and dark, 390 px): no violations.
39. **Part 7 of the look-and-feel plan (UI331, UI332, the 404 page, print, home screen).**
    The owner picked the contrast check in CI and softer dark tones (not the colour-blind
    pass or the old axe findings), the kind and the main pages on the social cards, the
    Hebrew 404 with a guess by id, printing and the home-screen icon.
    `tools/check_contrast.py` reads Material's tokens from the installed theme and ours
    from `extra.css`, composites translucent layers, and checks 30 pairs per scheme (text
    4.5:1, marks 3:1); it runs in the CI test job and has tests in `tests/tools/`. It found
    two light-mode marks under 3:1: the chart green (`--viz-s3` #1baf7a → #17a06e) and the
    amber of the star and the sort arrows (new `--site-mark-color` #b07d00; the amber stays
    for hovers and decoration). Dark: navy #243760 → #2a3d66, page #141a26 → #171f2d,
    the box card a shade lighter with a visible shadow. The lighter page pushed the dark
    series text (`--viz-s1-text`, `--viz-s3-text`, which were the mark colours) and the
    keywords on highlighted code lines under 4.5:1 in the axe run (11 pages instead of 6):
    the series text is now #5a9cf0 / #24b583, the code background stayed #1b2231, and
    both are pairs in the check now; the dark phone run is back to its 6 old findings.
    Social cards: the meta line in Hebrew first (an English level made the line LTR and
    put it in the wrong order), the kind added, counts on the home and level pages from
    `config.extra.dvq_cards` (the card cache hashes the rendered text, so counts refresh);
    "interactive" was left out since every question has a box. 404: `overrides/404.html`
    (custom_dir) with search, random, home and levels, and a guess from the address
    (`config.extra.dvq_404`). Print: Material keeps every admonition whole
    (`page-break-inside: avoid`), which left near-blank pages; print now lets them break,
    opens the blocks on `beforeprint` (ignoring a second one), prints dark as light and
    restores both after. Manifest and icons (`tools/make_icons.py`).
40. **Part 5 of the look-and-feel plan (UI322, UI323).** The owner picked two-line rows,
    "new" for at most the newest five of the last 7 days, segmented filters with a phone
    drawer, and three additions: filters in the address (replaceState, so "back" leaves
    the page), Hebrew topic names everywhere they show, and a friendly empty state; the
    row shows the first two topics as written; the search covers title, topics and id.
    The table lost its topics column (they sit under the title as filter buttons, "+n"
    for the rest) and its "interactive" mark and filter (every question has a box). The
    topics filter shows the six most common, the rest behind "עוד נושאים (n)" with its own
    search. `TOPICS` in the hook names the 39 topics (approved by the owner); the
    tags page is rewritten in `on_post_page`, the search chips in `_search_question`, and
    the linter warns about a topic without a name (it reads the table with `ast`). Found
    on the way: the address parameter `q` opens Material's search, which then swallowed
    every key typed into the table's search field, so the search text rides as `find`.
    The theme's table wrapper shrank to the content, so the title column could not take
    the width (`.md-typeset__table` is a block now); "+3" read "3+" in RTL (isolated LTR).
    axe on the open drawer, the topics panel, the empty state and the rows (390 and 1280
    px, light and dark): no violations. On `main` after a green CI run, with the topic
    names approved.
41. **0046 part c, the largest right triangle of ones (the owner's request, session 24).**
    The owner picked equal legs along the axes, the right angle in any of the four
    directions, the area (the number of cells, k(k + 1)/2) with the three vertices as the
    answer (`(area, corner, leg_col, leg_row)`, SV `tri_t` with -1 for no shape), and the
    triangle as a third option of every box's select plus a third box in part c. The
    solution is the square's dp without the diagonal: dp = 1 + min(the neighbour along
    each leg), a pass per direction that starts from the side the legs point to, one row
    of memory and a `prev`; O(m·n) time, O(n) memory. The example (5 × 7) has a leg-4
    triangle (area 10) where the largest square is 4 and the largest rectangle 6, a
    leg-3 triangle the other way and the owner's "010 / 111" shape (leg 2 only). Traps:
    three neighbours (the owner's left triangle gives leg 2, not 3) and the scan order;
    a follow-up on the pyramid (P = min(P above + 1, the run left, the run right), tested
    against a brute force). The box draws a triangle as a staircase polygon in an SVG over
    its bounding square, shows the dp of the pass being played, and has "the next
    direction"; the tie count is the cells holding the best leg (any 1 for a leg of 1).
    Tests: pytest (every grid up to 3 × 3, random grids, the page's tester, the numbers,
    the explorer's four dp matrices, order and ties), Verilator (the examples, the edge
    cases, 3,000 random grids against a brute force; a mutated min was caught). Found on
    the way: `\text{top\_left}` showed its backslash (MathJax's `\text` is literal
    without textmacros); 0046 and 0038 now write `\text{top_left}`. The page title says
    "the square, the rectangle and the triangle"; the file name stays, so links hold.
42. **New question 0047, trapping rain water in a row and on a map (session 24).** The
    owner asked for coding questions of the kind Google, Meta, NVIDIA and Microsoft ask
    (less architecture), picked this one from four proposals (trapping rain water,
    meeting rooms, topological sort, single number II), and asked for the 2D map as the
    hard part. Choices: two parts (a: the row, with two arrays as the step before two
    pointers; b: the map), junior / hard, the functions return the amount only, a box in
    each part. Part a: the column formula, the two-pointer proof (left_max never exceeds
    the right wall). Part b: the row formula fails on a winding leak (13 instead of 8 on
    the page's 5 × 5 map), the flood from the border with a min-heap pushed at the water
    surface, the proof by the escape height (Dijkstra). SystemVerilog has a heap class
    (`min_heap`, `cell_t`). Traps: moving the higher pointer (14 instead of 6), the row
    formula on the map, pushing the ground (1 instead of 8), edge cases. Tests: pytest
    (every row up to length 7 with heights 0 to 3, every map up to 3 × 3 with heights 0
    to 2 and 3 × 4 with 0 to 1, random rows and maps against the column formula and the
    escape height by relaxation, the tables and the trace, the traps, the explorer's
    steps, water and heap order against the page), Verilator (the examples, 3,000 rows
    and 2,000 maps against direct computations; two mutants caught). The `rainwater`
    kind: the columns as stacks with the pointers and the maxL / maxR / water table, the
    map with the heap outlined, the popped cell framed, the filled neighbours dashed,
    the water by depth and the heap list. New topics `two-pointers` (שני מצביעים) and
    `heap` (ערימה) in `TOPICS`; three new pairs in `tools/check_contrast.py`.
43. **0047 renamed "מילוי מים בבאר", and editing in the grid boxes (0046, 0047).** The owner
    renamed the question (file `0047-filling-a-well.md`, not yet published) and asked for
    a straight-to-the-result option and easier editing, with multiple-choice answers:
    a view select (`viewSel` in core: every step, or the final result, which every edit,
    random fill and resize keeps; the run's row, the scrubber, the step words and their
    legend keys hide), a drag that selects a range of columns or a rectangle of cells
    with a value field, "apply to the selection" and ±1, digits typed on a cell (two
    within 0.9 s make one number) or on the selection, an in-place editor on a double
    tap or Enter, and a text field that takes the values or a pasted Python list
    (`parseGrid` / `gridText` in core). Heights 0 to 20 with a "highest" field for the
    random fill; the row's cells shrink with the tallest column. 0046's boxes got the
    same view select, the text field and 0 / 1 typed on a cell or the selection. Editing
    aids are marked `data-nolink`: core's `controlsOf` and `tools/check_explorers.py`
    skip them, so links and saved states hold the grid in `dvqExtra` only (0046's view
    select sits after its mode select, so an older saved state still maps). Found on the
    way: a tap re-rendered the map under the pointer, which lost the double tap (the
    selection is painted in place now, and the double tap finds the cell under the
    pointer, since the pointer capture retargets it), and 0046's "the next direction"
    showed in every mode (the layout's display beat `[hidden]` on buttons).
44. **A short README (session 24).** The owner found the README too long (the catalog's
    long cells, the explorers row) and wanted it to be about reaching the site. Picked:
    the technical sections move as they were to `CONTRIBUTING.md` (question format,
    tests, tools, explorers, publishing); the catalog moves to `CATALOG.md`, written by
    the new `tools/catalog.py` from the front matter (id, the Hebrew title linked to the
    live page, the level), rewritten by `new_question.py` and checked by a test (the old
    hand-kept table had drifted: "38 questions"); the README keeps the site's links, a
    paragraph on what the site has and how to run it locally. CLAUDE.md, the template,
    `run_tests.py` and `mkdocs.yml` point to `CONTRIBUTING.md` now.
45. **A shorter CI (session 24).** A README-only commit took 25 minutes on the branch and
    25 more on `main`. The owner picked three changes: `paths-ignore` for README,
    CONTRIBUTING, CATALOG, HANDOFF and CLAUDE.md (such a push runs nothing); a `gate` job
    that finds a successful branch run of the same commit (the GitHub API, `actions:
    read`), so `main` then only builds and deploys; the explorer check as its own job on
    four runners (`check_explorers.py --shard K/N`, pages dealt by box count, 20 boxes
    each; the shards build without social cards, `DVQ_SOCIAL_CARDS=false` in
    `mkdocs.yml`). The tests and the build were left in sequence (not picked).
46. **Code review of 0025 and a highlight lint (session 25, 2026-10-25).** A code
    review of the 0025 commit found eight problems; the owner asked for all of them,
    with option a for the Ack policy (no Ack of any kind while NAK_SCHEDULED is set).
    The fixes were first made on the old session-11 branch, which `main` had left about
    200 commits behind (tag `review-fixes-old-base` keeps those two commits locally); the
    owner chose to re-apply them on the current `main`, which is this item. (a) Page
    code, both languages: the duplicate branch of `receive_tlp` sends its Ack only when
    `nak_scheduled` is off, like `flush_ack`; the steps, annotation (6), the part-b
    overview and the "number of Naks" proof say so; the explorer engine
    `docs/javascripts/explorer/acknak.js` mirrors it (its log says why no Ack went out),
    since `test_explorer_matches_page_classes` compares the two. (b) `hl_lines`: the four
    0025 blocks pointed at blank lines, comments and `end`; renumbered to the annotated
    lines. `tools/lint_pages.py` now checks that every `hl_lines` number lands on a code
    line of the dedented block; it found the same drift in 0007, 0012, 0020, 0023, 0024,
    0035, 0038, 0040 and 0041 (14 blocks in 10 pages), all renumbered to their annotated
    lines; documented in `CONTRIBUTING.md`. (c) `tools/figures/q0025.py`: frames record
    whether the delivered TLPs are replays and draw them with the dashed `fc-replay`
    arrow whatever the receiver does with them (part-b step 11, the three duplicates,
    now matches the legend); the dead `if False else` caption expression and the unused
    `faded` parameter of `seq_boxes` are gone; stepper b regenerated (only that arrow
    class changed). (d) `tests/0025/demo.py`: the EP's first Ack threshold is pinned to 3,
    so the scripted story (Nak, replay, damaged Ack, timer, duplicates) holds for every
    seed the reader tries (with a first threshold of 1 an Ack was queued ahead of the Nak
    and the comments described a run that did not happen). (e) "ולא רק את הרשומה
    אחת" → "ולא רק רשומה אחת" in the interviewer block. Checks: lint (46/46), the
    Python tests (403, including the Node explorer tests), the strict build (with
    `DVQ_SOCIAL_CARDS=false` in the sandbox, which has no cairosvg), links, the phone
    check and the explorer click-check of 0025. Verilator in the sandbox is 5.020, which
    rejects the `ref` helpers of `tests/0025/tb.sv`; the page's SV classes alone compiled
    and ran there with a duplicate-under-NAK_SCHEDULED check, and the old-base CI run
    (same SV change) passed the full testbench. Also seen: GitHub's `ubuntu-latest` is
    Ubuntu 26.04 now, where Playwright 1.56 cannot install Chromium; `main` already pins
    `ubuntu-24.04`.
---
47. **Steady text heights and a smaller enlarge button (session 25, 2026-10-25).** The
    owner saw two things on the live site. (a) In the explorer boxes the text under the
    controls changes at every step (the summary of 0026, the frame caption of 0018), a line
    more or less moved the figure under it, and while playing the figure jumped up and down.
    Options offered: a fixed floor plus "grow only", a measured line count per box, or a
    measurement of every possible text at mount; the owner chose the first, for every text
    paragraph of every box. `core.js` `steady(box)`: a MutationObserver on the box queues
    one measurement per frame; every `p`, `.ex-note` and `[aria-live]` element outside the
    controls keeps the tallest height it has shown as an inline `min-height` (border-box
    aware); the heights are released on a `change` of a control outside the play row and
    the scrubber, on "back to the question's values", and 150 ms after a resize. The CSS
    gives `.ex-summary`, `.hg-caption` and `.bridge-caption` two lines from the start
    (`2lh`, with a `3.2em` fallback). Measured at 1200 and 390 px: the hourglass frame and
    the motorcycle chart keep the same top through every event and scrub position (one
    8 px move at the first event comes from above the box, not from it). (b) The enlarge
    button (1.6rem, opacity 0.75) hid the "5" of a flipped hourglass. Now 1.2rem, opacity
    0.45 (0.6 on touch screens), full on hover or focus; and `reading-tools.js` decides per
    figure, once the wrap is laid out (ResizeObserver), after the phone text fit and on
    resize, whether the button's rectangle meets any SVG `<text>`: then the wrap gets
    `fig-wrap--above` (a 1.4rem strip above the drawing) and the decision is kept on the
    figure's container, so a live figure that a box redraws every frame does not flip
    between the layouts. (c) `check_phone.py` fails when a button still covers text
    (`ENLARGE_COVERS`, via `window.dvqFigCovers`); it caught the first version, where the
    decision was taken before the phone fit enlarged the stepper text of 0025.
    `check_explorers.py` strips the inline `min-height`, `data-fig-above` and
    `fig-wrap--above` from the compared drawings, since they depend on the steps a box went
    through, not on its state. The jitter check the owner was offered (step every box and
    report a paragraph that outgrew its reservation) was not chosen.
48. **0044 becomes a coding question: the Kaprekar step, a hash, then the closed form
    (session 26, 2026-10-25).** From the owner's write-up (f(x, b, n) in Python and
    SystemVerilog, a hash of the results over x = 0..999, the single-step table
    6d(10 − d) with its inclusion-exclusion). Checked first: the example, the table, the
    formula and the double loop's result hold; the owner's Python loop had inconsistent
    indentation (an IndentationError), fixed and called out. The owner's choices: f is a new
    part a, the old parts move to b, c, d; part b shows the double loop as code (1000 steps
    on each x) and asks what the hash holds without running it ({0: 10, 495: 990}, step 8 of
    its solution, from the existing proof); the single-step table is left out; `int`
    instead of `longint`; the SV hash is `int hash[int]` (the Python keeps the owner's
    `num`); title "צעד קפרקר, hash והספרות אחרי n פעולות", kind `code`, tags `sorting`,
    `python`, `systemverilog` added. Anchors: part a `#kaprekar-step`, the base-10 and
    base-5 parts keep their old ids `#10` and `#5`, the bonus `#base-b`. A trap on locals
    that are not reset. Tests: pytest compares f with a digit count in every base 2..16 with
    1..4 digits and checks the hash; `tests/0044/tb.sv` puts the page's f at `$unit` scope,
    instantiates the page's `kaprekar_hash` module and checks in a `final` block (the
    module calls `$finish` at time 0). Found on the way: in Verilator 5.020 a fixed-size
    local array (`int cnt[16]`) of an automatic `$unit` function kept its values between
    calls (the testbench's reference hung); explicit zeroing fixed it, and the page now
    says the owner's explicit init is the portable choice (a queue and a scalar with a
    declaration initializer were reset correctly in the small tests). `demo.py` added: the
    run panel runs part b's million calls on load (2.2 s in CPython, a few seconds more in
    Pyodide). At the owner's request the function is named `kaprekar_step` on the page,
    in the tests and in the run panel (the write-up called it f).
49. **Accessibility and small text on phones (session 26, 2026-10-25, fix rounds 1 and 2).**
    The CI log of the phone check listed axe findings on seven pages and SVG text under
    9 px on six; the owner chose to fix them, to grow the fonts (not to widen the figures)
    and to make both checks fail in CI. axe: the ladder cells of 0021 lost contrast to
    Material's `small { opacity: .75 }` (now `opacity: 1`; their tinted fills added to
    `PAIRS`) and lost their `aria-label` (the name is the visible text); the 0013 pair cells
    and the 0044 state-diagram cards start their names with the visible text (the card's
    text elements end with a space, since axe joins SVG text without one); the points of
    the 0007 triangle and half-circle boxes have an `aria-label`; the 0043 race grid is a
    `group`, not an `img`; the scrolling table wrappers of 0038 and 0044 take focus with a
    region name. Small text: `reading-tools.js` grows a label at most 2x (was 1.8x), which
    lifts the 10 px labels of 0018, 0019 and 0031 over 9 px at the boxes' 0.47 scale; a
    label marked `data-fit-drop` (the 9 px sizes inside narrow bars of the PCIe box) hides
    when it still renders under 9 px; the long legend lines of the PCIe box and of the 0023
    request figure split into two lines (the generator and the page copy updated); the
    hourglass tree says "מצב אחד". `check_phone.py --small-fail` is new; CI runs the phone
    check with `--axe-fail --small-fail` (light and the manual dark run). Checks: the full
    phone check light and dark with both flags, the explorer click-check of the ten touched
    pages, the Python tests (405), contrast, links, lint. The wide-math warning came and
    went between local runs on untouched pages (0012, 0041): font timing in the sandbox.
50. **Fix round 4, the documents (session 26, 2026-10-25).** `HANDOFF.md` had grown to
    3,450 lines. The work log of sessions 1 to 21, the "In progress" notes of sessions 20
    to 26 and the finished rounds U to X with the explorer survey moved to
    `HANDOFF-archive.md` (word for word); `HANDOFF.md` keeps the goal, the decisions, the
    log from session 22 on, a rewritten "In progress" (the state, the open fix rounds, the
    owner's checks and choices), the open items, the question variety, the open proposals,
    the improvement ideas and the technical notes (about 1,690 lines). The coverage table
    counts 46 questions with 0044 to 0047; "still missing" names UVM, covergroups, debug and
    planning (0040 and 0041 covered an FSM and coverage closure); improvement ideas 7b, 12a,
    12b, 17 and 18 are marked done; the senior list of the owner decisions is corrected.
    `CLAUDE.md`: Israel is on winter time (UTC+2) until 26 March 2027, and it points at the
    archive. The archive joins the files whose push runs no CI (`paths-ignore`, CONTRIBUTING).
51. **Fix round 3, the CI actions on Node 24 (session 26, 2026-10-25).** GitHub warned on
    every run that the actions ran on the deprecated Node 20. All moved to their latest
    major (the owner's pick, version tags rather than SHAs): `checkout@v7`,
    `setup-python@v7`, `setup-node@v7`, `cache@v6`, `upload-artifact@v7`,
    `upload-pages-artifact@v5`, `deploy-pages@v5`, in `deploy.yml` and `weekly.yml`. Their
    breaking changes (fork checkouts under `pull_request_target`, npm `always-auth`,
    `package.json` caching, Docker container actions) do not touch these workflows. The
    branch run was green with the Verilator cache found (no rebuild) and no Node 20
    warning. Verilator: the newest release tag is still v5.052, and the pinned commit is
    newer, so `VERILATOR_REF` stays.
52. **Fix round 5, a prepared cloud sandbox (session 26, 2026-10-25).** The owner's picks:
    a hook in the repository, Verilator only on request, a `--local-cdn` flag.
    `tools/dev_setup.sh` (idempotent, reports what is missing) installs the Python
    packages and `cairosvg`, fetches MathJax 3.2.2, Mermaid 11, WaveDrom 3.5.0 and axe-core
    4.14.0 into `.cache/cdn` with `npm pack`, and checks Chromium; `--verilator` builds the
    pinned commit into `~/verilator` or finds it there (by the short hash in
    `--version`). `.claude/hooks/session-start.sh`, registered in `.claude/settings.json`,
    runs it in cloud sessions only (synchronous; about 10 s on a fresh container, 1 s when
    everything is in place), sets `DVQ_SOCIAL_CARDS=false` when fonts.google.com is blocked
    (the social plugin's font; the build fails otherwise) and puts `~/verilator/bin` first
    on `PATH` when it exists. `check_phone.py` and `check_explorers.py` take `--local-cdn`
    (implies `--offline`, routes the four scripts; the phone check also runs axe-core from
    there). Found on the way: this container already had the pinned Verilator in
    `~/verilator` (built 2026-10-19), and every SV testbench passes with it; WaveDrom was
    not routed in earlier local checks, so its diagrams were missing there. Checks: the
    hook run as a cloud session would, the strict build, `--local-cdn` phone and explorer
    checks on 0005, 0034 and 0044, `run_tests.py --sv-only` (all PASS).
53. **Fix round 6 part a, figures that stay still while a box steps (session 26,
    2026-10-26).** The owner picked part a only, as a CI failure once the boxes are fixed,
    at 390 and 1200 px, a 2 px tolerance, and chose the fixes per kind after the findings.
    `tools/check_jumps.py` steps every box with a step counter and a next button from the
    first step to the last and fails on a figure that moves more than 2 px, naming the
    element that grew. The first run found 113 jumps in 11 pages of four kinds: (a) a text
    longer than every earlier one (0016, 0041, 0042, 0043); (b) the answer line appearing
    at the end (0012, 0013, 0039, 0043); (c) a block above the figures that grows with the
    steps (the step tables of 0012 and 0013, the cake table of 0027 and 0028, the zoom of
    0039, the ribbon of 0041, the circle of 0016); (d) the two sides of the 0025 box. Fixes:
    `steady()` in `core.js` primes the heights at mount and after every release, running
    each timeline (a counter with previous and next buttons; a next without a previous
    draws something new and is left alone) to its end and back synchronously, through the
    previous button (a start button can clear a history), at most 150 steps and 250 ms,
    with the save of the remembered state paused meanwhile; blocks marked `data-steady`
    are held like paragraphs (the cake table, the 0039 zoom and its wrap, the Josephus
    circle, the three parts of the 0025 box); `answer()` keeps a cleared answer line in
    place (`ex-answer--off`, invisible); the step tables of 0012 (last in the box) and
    0013 (under the map) and the ribbon of 0041 (under the chart) moved, and the page
    texts of 0012 and 0013 describe the new order; `reading-tools.js` honours
    `data-fig-strip` on a container (the 0039 zoom), whose figures always have the enlarge
    button's strip, since its labels reach the button only at some steps. CI runs the check
    in the four explorer shards. Checks: the jump check (0 jumps in 160 boxes), the explorer
    click-check of every page (no problems; the Josephus link warnings are as on `main`),
    the phone check with `--axe-fail --small-fail`, the Python tests (405).
54. **0048, the farmer, the food and the water (session 26, 2026-10-26).** A student
    question (medium, math) from the owner's write-up: two parallel lines H apart (food on
    top, water below), the farmer A at height a and the cow B at height b, L apart; the
    path goes to the food line, then the water line, then the cow. Part a (a = H/3,
    b = 2H/3) by two reflections: B' through the water line, B'' through the food line at
    2H + b, so z = sqrt(L^2 + (2H + b - a)^2) with the stops in the ratio (H - a) : H : b
    (2L/7, 3L/7, 2L/7). Part b is the inverse: stops at a third and two thirds give
    a = 0, b = H. Checking the write-up found two things, told to the owner and fixed with
    their picks: the answer of part b lies on the lines while the statement said "between
    the lines" (now "between the lines or on them"), and the conditions of part b missed
    b <= H, that is w <= y (the full condition: y is the longest of x, y, w; a trap now
    says so). The page has no code (owner's pick). Figures (`tools/figures/q0048.py`):
    the problem with a path that is not the shortest (x, y, w, z1, z2, z3), and the
    unfolding of each part with the strips reflected below and above, B', B'', the
    straight line and the three similar triangles. The box `farm` (`farm.js`, one box in
    part a's solution with a part select; see CONTRIBUTING): drag the farmer and the cow
    (part a) or the two stops (part b, the drag stopping at x = y or w = y with a line
    that says why), the four corners for L and H, typed values checked, a seeded random
    example, a Pythagoras table, and the reflection toggle (off by default). Tests: exact
    arithmetic of both parts, the reflection against a search over the two stops, the
    inverse on 200 random pairs, the follow-ups, the box's math against the generator.
55. **Review rounds V1, V5 and V7 (session 26, 2026-10-26).** The owner picked V1, then
    V5, then V7, with a publish to `main` at the end. V1: the 0023 box error (a manual
    request after the page's example used the example's scripted draws; the example now
    stops there, the pick stays in range, a Node test), `ltr()` keeps a short LTR span on
    one line (table cells may still wrap), 0002 part c opens on XOR (`data-start`), the
    0045 beam, the 0039 label, the 0042 camel and phone price labels, 0026 numbers and the
    A / B labels, the 0048 drag caption, the 0047 heap caption, superscripts in 0034 and
    0037. V5: 0033, 0034 and 0036 to 0038 in the common layout (each part's heading before
    its hints), a second hint where one was missing, four traps per page; 0035 in two parts
    (part b divides by any odd N, `div_odd_50` in SV and Python, measured for N = 3, 5, 7),
    a generated schematic (`tools/figures/q0035.py`), a third hint and two traps; 0016 part
    c gets code (`josephus_chain`, `josephus_closed`, tested in pytest and Verilator; the
    closed form tests `m <= n / L`, so it does not overflow a 32-bit int); every follow-up
    on every page (199) has a short collapsed answer (`??? fu-answer`), written by five
    agents in parallel with the numbers recomputed, and `lint_pages.py` now fails on a
    follow-up without one and on a non-breaking space inside code. The answers corrected
    three page claims: 0041 (90% of 16 bins needs about 38 tests, not 30), 0042 (two camels
    are not explained by the price list alone), 0040 (the reversed pattern 1101 has its own
    machine); answers to check against the specs: 0023 a write in the middle of a read,
    0024 shared credits and Sync, 0025 the replay limits. V7: `timeout-minutes` on every CI
    job, `docs/sw.js` for offline reading of visited pages (network first, a kill switch,
    blocked in the page checks), the header tabs without the slide-in.
56. **Review round V2, study paths for every question (session 26, 2026-10-26).** The
    owner's picks: two DV paths (logic design 0001, 0040, 0035, 0036; clock crossing and
    verification 0033, 0034, 0037, 0038, 0041), the PCIe path extended into "protocols"
    (0020, 0021, 0023, 0025, 0024), the puzzles split (logic puzzles get 0032, 0045, 0043;
    a new "optimization puzzles" path 0031, 0039, 0042), a "geometry and motion" path (0026,
    0029, 0030, 0048), an "advanced algorithms" path (0016, 0046, 0047), 0003 first in the
    coding path and 0044 last in the digits path. Twelve paths cover all 47 questions; the
    DV paths come first. `lint_pages.py` fails on a question in no path (a test checks it);
    the path front matter is quoted.
57. **Review round V3, the boxes on a phone (session 26, 2026-10-26).** The owner's picks:
    folds closed on a phone only, the split map only collapsed with short phone labels (not
    split by completion count), an eight-row scroll for the growing table, V2 and V3 to
    `main` together. `folds()` in `core.js`: a proof panel (`.ex-proof`) or a group
    (`.ex-fold` with an `.ex-fold-title`) gets a title button, closed under 720 px;
    `data-fold="closed"` everywhere (the 0020 / 0021 map). Folded: every proof panel (the nine
    kinds with an `.ex-proof`: boxes, cake, eurovision, horses, hourglass, josephus, lfsr,
    motorcycle, river), the editing rows of 0046 and
    0047 (the shape and view selects moved after the fold, so the link payload keeps its
    order), the random-run rows of 0024 and 0025, the 0013 base table. Layout: 0024 / 0025
    free events in two columns on a phone and the 0024 hand labels beside their hands;
    0018 / 0019 event frames stacked on a narrow box, all their figure words in Hebrew (the
    fork labels too); 0031 and 0032 bank names in Hebrew, 0031 plans as "A+B → · ← A", the
    bridge before the tables on a phone (CSS order); 0040 "הביט הבא" with its buttons and
    the state meanings along the bottom of the graph; 0038 short headers; 0041 equal
    sliders and Hebrew-first labels; 0037 the factor table as blocks on a phone and a zoom
    of ±3 windows under the edge strip; 0027 / 0028 the table scrolls at eight rows; 0042
    and 0043 the step text under the figure. Phone heights: 0009 1,873 → 1,393 px, 0016
    1,564 → 1,350, 0024 2,087 → 1,877, 0025 1,837 → 1,751, 0027 2,093 → 1,655, 0046 1,500
    → 1,145, 0047 1,619 → 1,235, 0020 1,413 → 1,021, 0021 map 1,813 → 1,092 (2,526 → 880
    on a desktop). The page checks open every fold; `check_explorers.py` does not click the
    fold buttons.
58. **Round V3b, the small box fixes and a ρ for 0044 (session 26, 2026-10-26).** The
    owner's picks: the 0044 state diagram as a ρ at every width, a movable hour in 0029,
    long formulas split with `aligned`. 0044 `kapgraph`: the tail on a ring of cards from
    the top, right to left, the fixed point in the middle with its loop under it, or the
    two values of an odd base side by side with an arrow each way; smaller cards and short
    tags under 520 px (base 10 from 211: about 1,000 px tall on a phone before, 347 now).
    0013: the `kappairs` path bowed and drawn under the numbers (which keep a halo); the
    `kaprekar` histogram with four to eight grid lines (it had 25 labels on top of each
    other). 0015 opens on step 1. 0011 and 0017: a long number field wraps inside the box.
    0029: under the day strip, the hour of the current time as the same three rows with a
    tick per meeting (the hour shaded on the day strip; a click jumps to a meeting), and
    the counts with the colon rule. 0012, 0013, 0039, 0041: four display formulas split
    with `aligned` (the phone check warned about them). 0026 needed nothing: V1 had moved
    the A and B labels beside the road.
59. **Rounds V4a and V4b, try it yourself (session 26, 2026-10-26).** The owner's picks: a
    wrong answer shows a hint, then a button with the answer; self-checks on about 15
    pages with a numeric answer; a right answer is remembered but does not mark the
    question solved; V4a and V4b go to `main` together. **Self-checks**
    (`docs/javascripts/selfcheck.js`, CONTRIBUTING): 15 on 13 pages (0015 a and b, 0016,
    0021 a and b, 0026, 0027, 0028, 0029, 0030, 0031, 0032, 0036, 0039, 0042), linted, and
    every answer recomputed in `tests/tools/test_selfcheck.py`. **Boxes:** 0021 guesses
    C(n) before it shows; 0004 names the three contents before the deduction (a right
    answer the draws did not decide is called a guess; the reveal draws the balls); 0003
    the trap j = i + 1 as a select (descending, n(n − 1)/2 comparisons, tested against
    Python); 0031 "התוכנית שלי", crossings picked by hand, the best plan hidden until all
    are across; 0039 a hidden-threshold game, random or an adversary (tested: the page's
    plan needs exactly f against it, random play never fewer); 0010 part a's pair
    deletion pass by pass with the characters read (tested against the page's Python);
    0036 the register drawn with its taps, XOR and fb. 0043 got no self-check while a
    minimality claim on its page is unchecked (review finding).
60. **New questions 0049 to 0052 (session 27, 2026-10-27).** The owner asked for four
    extended questions, two on DV, for juniors and seniors; picked the UVM architecture,
    the out-of-order scoreboard and HH against HT as proposed, and changed the bottles
    question to one round, then two, then n bottles and b rounds (the owner's "three
    rounds, base 3" was base 4: b rounds give b + 1 outcomes per mouse; said so before
    writing); no code on the UVM page; all four published together. **0049** (junior, dv,
    no code): the testbench figure from `tools/figures/q0049.py` (LAYOUT, ARROWS, PATH),
    the components with what they do and do not do, the sequence / driver handshake, the
    phases, passive agents and reuse; box `uvmarch` draws the same layout (tested to
    agree), a click explains a component, the transaction is stepped along its arrows,
    and a quiz asks "who does this?". **0050** (senior, dv): one queue per ID, the head
    only, timeout, end check and reset, as a SystemVerilog class (an associative array of
    queues, Verilator runs it) and Python; the scenario table against a single FIFO and
    "search the ID's queue" (a false alarm on legal interleaving, a miss on a swap within
    an ID); tested against the generator's checkers and random legal and mutated
    streams; box `scoreboard` steps the scenarios or a seeded random stream with one
    injected bug and shows the three verdicts. **0051** (junior, puzzle): 10, 7 and 5
    mice for 1000 bottles in 1, 2 and 3 rounds, ⌈log_{b+1} n⌉ in general, digit d = the
    round a mouse drinks and dies; every bottle of small cellars decoded in pytest and
    Verilator; box `mice` steps the rounds with the bottles still possible, and a decoder
    mode hides a bottle. **0052** (senior, math): 4 and 6 tosses, Conway's correlation and
    the fair-casino proof, the race (HT against HH is 1/2; Penney's table of length 3),
    the exact distributions; tested against exact Markov chains for every pattern up to
    8 letters and every race up to 4; box `coins` tosses by hand or plays, with 1000
    seeded games against the exact distribution. Self-checks on 0051 (a, b, c) and 0052
    (a, b, c). New study path `testbench` (0049, 0050); 0051 in logic puzzles, 0052 in
    probability. Topic names for `uvm` and `methodology`.

61. **0052 generalized (session 27, 2026-10-27).** The owner's picks: a biased coin; races
    of three patterns and more; the generating function; in the box a choice of q or a
    die, and the state graph. Part b takes a probability per letter (each overlap adds 1
    over the probability of its prefix; a table for q = 1/2, 2/3, 3/4, 9/10, where HH
    overtakes HT); part c solves Conway's m + 1 equations (each pattern's chance and the
    race's length; HHH, HTH and THH win 1/8, 5/12 and 11/24 in 16/3 tosses) in Python
    with fractions and in SystemVerilog with reals (`$abs` is not in Verilator: squares
    compared for the pivot); new part d, G(z) = P(A) z^L / (P(A) z^L + (1 − z) C(z)) with
    its proof, the distribution by one recurrence and the variance (HH 22, a self-check).
    The generator solves the chains (first and second moments, races of any number of
    patterns, any alphabet) and the tests compare them for every pattern up to 8 letters,
    biased coins, the die and every race of three and four patterns of length 3.

62. **New questions 0053 and 0054 (session 27, 2026-10-27).** The owner picked 1 and 2 of
    four proposals (covergroup, arbiter; not reservoir sampling or the skid-buffer bug)
    and asked for boxes that show the solution well. **0053** (junior, dv): an ALU
    covergroup, 15 coverpoint bins and a cross of 72 (80 less 8 ignored SHL cells), the
    LRM's group coverage (24.28 % after one sample), and the closure time of the cross:
    1,393,801 transactions with uniform stimulus against 534 with `dist` and 389 (80 H_72)
    with equal classes, exact by inclusion-exclusion over three cell groups in the
    generator and by a numeric integral on the page. Verilator 5.053 runs the covergroup
    (cross, `ignore_bins` with `binsof ... ||`, `iff`, `sample` with arguments) and its
    `get_inst_coverage()` follows the LRM; `get_coverage()` is the type's, merged over
    instances. The testbench checks it against a reference model of the bins on random
    runs. Box `covergroup`: stimulus and seed, +100 to "until closed", a hand sample, the
    coverpoint bins, the cross as five maps (3 + 2 on a phone), the coverage curve on a
    log axis with the expected closure, and the ignored cells counted on demand. **0054**
    (senior, design): fixed priority and starvation, round robin by
    `dbl & ~(dbl - pri)`, the checker (one-hot, no grant without a request, the hold rule
    of the environment, fairness within N - 1) and weighted round robin (shares w_i over
    the sum, longest wait the sum of the others). The testbench runs four lanes (the
    arbiter and three buggy copies) and the checker's counters equal a procedural count;
    samples are taken just after the falling-edge drive (at the rising edge the pointer
    may have moved already). Box `arbiter`: a request grid drawn by click, the three
    arbiters with wait/bound per requester, the trick at the chosen cycle, a bug select
    and the failing assertions with their cycles. Its classes are `arb-*` (`ab-*` belongs
    to the abmap box). Self-checks on both; 0053 in the testbench path, 0054 in logic
    design.

63. **New questions 0055 and 0056 (session 27, 2026-10-27).** The owner turned down a
    first set (solve-before, skid buffer, reservoir sampling, the light bulb) and a second
    (the SV scheduler, hats, the sum of uniforms past 1), asked for interview questions in
    the style of Nvidia and Apple, and picked the divisible-by-3 machine and the ants on a
    pole (PLRU was picked first, then swapped for the ants). **0055** (junior, design): from
    the MSB the state is the remainder, r' = 2r + b; from the LSB the naive machine keeps
    the remainder and the position (6 states for 3, 20 for 5), but x = r * 2^-k is enough,
    x' = (x + b) * 2^-1, so m states both ways for odd m (and for 3 it is the MSB machine with
    1 and 2 swapped, since 2 = -1 mod 3). Part c: any base B coprime to m (k bits a cycle are
    base 2^k, the multipliers B and B^-1 mod m; 1 means a digit sum), one parametrized
    module. The generator builds the naive machines from the definition and minimizes them
    by partition refinement: the table of fewest states for m = 2 to 16 (even m = 2^a m':
    m' + a from the MSB, m' + a + 1 from the LSB, a follow-up). Box `divfsm`: one number fed
    to both machines side by side (MSB from the left, LSB from the right), m, the base,
    digits typed, added by buttons or drawn; each ring shows the current state, the edges
    out of it (bent inward) and the edge just taken (bent outward). **0056** (junior,
    puzzle): ghosts that walk through each other give the last fall (100 s at most), the
    collisions (pairs going toward each other, 2500 at most for 100 ants) and the fall of
    each ant (the order along the pole is kept: the leftmost ants, as many as go left,
    fall left in the order of the left ghosts' times); part d, added at the owner's pick, puts
    the ants on a ring: after a lap of 100 s ant i stands where ant (i + R - L) mod n started,
    and all are home after n / gcd(n, R - L) laps. The generator simulates in half seconds
    on doubled coordinates (the pole and the ring). Box `ants`: ants placed and turned by a click on the
    pole (its container has `data-fig-strip`, an ant reaches the corner of the enlarge
    button only at some steps), drawn from a seed, played by half seconds on the pole and
    on a space-time chart, a toggle between ants and ghosts, the fall of every ant as
    chips; the ants ride in the link through `dvqExtra`. Self-checks on both; 0055 in the
    logic-design path, 0056 in logic puzzles.

64. **New questions 0057 and 0058 (session 27, 2026-10-27).** From four proposals (the missing
    tag, a pulse synchronizer, coins in a row, a die from `% 6`) the owner picked the first
    and the third, asked for a box each and for n coins with n even rather than 2n. **0057**
    (senior, dv): a checker in constant memory on a tagged interface. One missing by XOR of
    every tag sent and returned, with a count of the tags out (0 is also tag 0); two missing
    by x = a ^ b and part[j], the XOR of the tags with bit j set, kept for every bit since
    the bit is known only at the end (W + W^2 bits; sum and sum of squares need fewer); one
    missing and one doubled fool XOR (it reads as two missing) and are found by s = a - d
    and q = a^2 - d^2; k missing by power sums and Newton's identities, the roots among the
    tags. Three page modules (`tag_xor`, `tag_xor2`, `tag_sums`) and `missing_k` run in
    Verilator on random runs with a request and a response often in the same cycle. Box
    `tagcheck`. **0058** (junior, code): the parity trick (the first player takes a whole
    colour, at least half), greedy losing on 1, 2, 5, 3 (the first such row of four distinct
    coins up to 5), the interval DP d[i][j] = max(c_i - d[i+1][j], c_j - d[i][j-1]), the
    trick leaving 8 of 22 on 1, 1, 9, 1, 1, 9, and an odd row (1, 5, 1). Box `coinrow`. Self-
    checks on both; 0057 in the testbench path, 0058 in advanced algorithms.
65. **Session 27, 2026-10-27: a visual review and the fifth series W1 to W5.** The owner
    asked for UI / UX proposals that make the site look more professional (effects,
    typography, colour, spacing) and sent a list of ideas from a generic interview-prep
    site. Screenshots of the home page, a level catalog, 0046 (statement, an open
    solution, the box, the run panel with a mocked output, since Pyodide's CDN is blocked
    in the sandbox) at 1280 and 390 px, light and dark. The owner's list was checked
    against what exists and against the audience (working students preparing for a DV /
    electrical engineering interview); what fits became rounds W1 to W5 under **Fifth
    series**, with the items that do not fit and why. Found on the way: the line-length cap
    of UI321 (`max-width: 75ch` on `p`) also caps `p.admonition-title`, so the title bar of
    every non-folding admonition ends half way on a wide screen (the home tip box; 48
    built pages have such a title). Nothing in the site was changed in this session.

66. **Round W1, foundations (session 27, 2026-10-27).** The owner's picks: the traps in
    one group, the edit link at the page end, a cool off-white, cards with a soft shadow
    and no outline. W333: `.admonition-title` out of the 75ch cap. W334: the home page
    without its TOC column. W335: tokens in `extra.css` (`--sp-1` to `--sp-6`,
    `--radius-s/m/l`, `--shadow-1` to `--shadow-3` per scheme, `--dur-1/2`, `--ease`),
    used by the cards, boxes, admonitions and the new rules. W336: the light page
    `#f7f8fb`, code `#eef1f6`, white surfaces (`--site-surface`) for cards, boxes,
    admonitions, tables and filter chips, `--site-card-edge` transparent in light and the
    old outline in dark, the footer in the brand navy in both schemes. W337: `--adm-trap`
    `#b45309` / `#fdba74` (amber-orange); `on_post_page` wraps each run of trap blocks in
    `.trap-group` titled "מלכודות נפוצות (n)" with numbered rows (a solid circle, white
    digit) and drops the "מלכודת :" prefix; every question page has one group (165 traps).
    W338: `overrides/partials/content.html` drops the header action icon and adds "עריכת
    העמוד ב-GitHub" at the end of every page. `check_contrast.py`: CARD is the surface,
    six new pairs (card text, trap title and number, footer text, edit link). axe then
    found code tokens under 4.5:1 on the new code background (13 pages): the light
    function, special, constant, variable and generic colours were darkened, the dark
    constant and number lifted (they failed on a highlighted line before), and eight
    code token pairs joined `check_contrast.py`.
67. **Round W2, the home page (session 27, 2026-10-27).** The owner's picks: the audience
    line "לסטודנטים ולמהנדסים בתחילת הדרך שמתכוננים לראיון DV", no rotating word, six
    featured paths mixing DV and algorithms, the catalog as a tab after "ראשי". W339: the
    audience line in amber under the title (`{ .hh-audience }`), the hero's waveform drawn
    once (`pathLength="1"`, `stroke-dashoffset`, 2.4 s, staggered), the three numbers
    counting up on first view (`docs/javascripts/home.js`); both off under reduced motion.
    W340: "איך זה עובד", three step cards (`<!-- how-it-works -->`, `HOW_STEPS`) right
    after the hero, in place of the tip box. W341: `docs/all.md` holds the table and the
    difficulty legend, a "כל השאלות" tab, and the home page a "לכל 47 השאלות" button
    (`<!-- catalog-link -->`); the home page is 2,757 px tall at 1280 px (was 7,456).
    W342: `featured: true` on logic design, CDC and verification, protocols, interview
    algorithms, logic puzzles and probability (`<!-- path-cards featured -->`; the paths
    page shows all twelve); the card title on its own line, the count beside the
    difficulty chips (no more ids), equal heights on wide screens, the "solved" bar hidden
    until something is solved (level cards too); the PCIe path renamed "פרוטוקולים ומודלי
    ייחוס". W343: six FAQ items at the end of the home page (DV, a DV interview, which
    level, how to practise, where progress is kept, offline), styled in the site's navy.
68. **Round W4, the run panel (session 27, 2026-10-27).** The owner's picks: the output in
    the site's code colours (not a dark terminal), Python fetched when the panel opens, a
    mismatch shown with the expected value, a run button on the SystemVerilog tabs too.
    **Bug found and fixed:** 16 starting scripts (0016, 0033 to 0047) begin with `from
    solution import *`, but the worker never made a module `solution`, so their panels
    failed at once with `ModuleNotFoundError` on the live site (reproduced in Pyodide 0.26.4
    under Node). `docs/javascripts/py_run.py` now runs a panel: the page code as the module
    `solution` and in scope, the reader's code as your_code.py, and the output check;
    `py-worker.js` loads it, `tests/tools/test_run_panel.py` runs every demo (39) against
    its page in CPython and fails on an error or a commented `print()` whose output differs;
    all 39 also ran clean through `py_run.py` in Pyodide under Node (15 checks, 0 bad).
    W349: CodeMirror 6 (Python, line numbers, the site's code colours, Ctrl+Enter runs)
    bundled into `docs/javascripts/vendor/codemirror.min.js` (361 KB, 122 KB gzipped) by
    `tools/codemirror/build.sh` from `tools/codemirror/entry.js`, loaded on the first open,
    the textarea kept when it fails. W350: a reader's own opening of the panel (a trusted
    click, or a run button; not "open all" or the page checks) starts the worker; stages
    "מוריד את Python (פעם אחת)" → "טוען את הפתרון ומריץ" with a spinner, the status as a
    chip (busy, done ✓ with the time, error). W351: the output with a copy button, stderr
    and errors in the trap colour, `File "your_code.py", line N` a link that selects the
    line. W352: ✓ / ✗ in the editor's gutter beside each commented `print()` that ran once,
    and a line "בדיקת פלט : 5 מתוך 6 ..." with the mismatches (got, expected); only 0016,
    0044, 0046 and 0047 have such comments today (15 prints). W353: "▶ להרצה בדפדפן" under
    every Python tab of a solution, "▶ להרצה (גרסת ה-Python)" under every SystemVerilog tab
    (it opens the panel and flashes its Verilator note). Local check: the worker bypasses
    Playwright routing, so a test page builds it from its source with Pyodide and
    `py_run.py` pointed at local copies (scratch script, not in the repository).
69. **Round W3, motion and one sticky row (session 27, 2026-10-27).** The owner's picks:
    one translucent row, "back to top" as a round button in the bottom corner, W344, W345
    and W346 (not the drawn check mark of W348), and for a completed path a message with
    confetti. W344: `home.js` gives the home page's headings, lists, cards and FAQ items
    `.w-reveal` and an `IntersectionObserver` lifts each once (400 ms, a 40 ms stagger in a
    row of cards); nothing hides without the script, under reduced motion or when
    `navigator.webdriver` is set (the page checks). W345: level, path and step cards rise
    2 px under a real pointer (`hover: hover`), buttons and chips press to 0.97, the arrow of
    "להתחיל לתרגל" nudges. W346: `::details-content` with `interpolate-size: allow-keywords`
    animates the opening of every details outside the boxes (300 ms; other browsers open at
    once). W347: the solution map stays in its solution (no longer sticky); the part bar
    holds `.pn-sol`, a copy of the map of the open solution whose own row has scrolled
    above the bar, with the current block marked (`reading-tools.js`, `syncSlot`); the bar
    is translucent with `backdrop-filter: blur(10px)` (solid where unsupported), and the
    fixed bar of a page without parts becomes a full row while it holds a map; `.md-top` is
    a 2.6 rem circle at the bottom left. W348 (part): the toolbar carries `data-paths` (the
    question's paths, their ids and the next path); marking the last unsolved question of a
    path shows "סיימת את המסלול ..." with a link to the next path, and confetti. Found by
    the page checks on the way (W1 and W2 follow-ups): the path cards overflowed a phone
    (a one-line title in a `1fr` grid column; now `minmax(0, 1fr)`, and the title wraps
    under 45em), and the orange running text was under 4.5:1 on a highlighted table row of
    0027, 0028 and 0031 (the row is the code background, now darker): `--viz-s2-text`
    `#bf4a16` → `#ab4213`, with a new contrast pair.
70. **Proposals replaced (session 27, 2026-10-27).** The owner asked for fresh proposals
    instead of the accumulated ones: every proposal section (the topic gaps and question
    formats, the first series A1 to T132, the second series A to R and Z, UI1 to UI5, V1 to
    V7, W1 to W5 and the old idea list) moved as written to the end of
    `HANDOFF-archive.md`; the open items and the "Next" line point to the new **Proposals**
    section, the sixth series X1 to X6 (X360 to X392): visual aids of a new kind, tools
    that check the reader's own answer, a shared cycle simulator, and 20 new questions in
    digital design and DV, EE basics, and algorithms and puzzles, none of them proposed
    before.

### Session 27 — 2026-10-27: four new questions (0049 to 0052)


71. **New question 0059, the next number with as many ones (session 27, 2026-10-27).** The
    owner did not take four proposals (reservoir sampling, rand5 to rand7, Boyer-Moore, the
    prisoners and the bulb), then picked Gosper's hack from the second four. A first version
    had the place in the sorted list (sums of binomials) as part c; the owner replaced it:
    three parts, the next, the previous, and the same for zeros. Junior, code. Part a:
    c = x & -x, r = x + c, r | (((x ^ r) >> 2) / c), with a proof by the highest differing
    bit and the edges (x = 0, the block at the top). Part b: prev(x) = ~next(~x) in w bits,
    the complement reversing the order. Part c: zeros counted below the top one (leading
    zeros do not count, no fixed width): within a length they are the ones of parts a and
    b; when the length runs out, the next is 2^L + 2^(L-z) - 1 and the previous
    (2^(L-1-z) - 1) * 2^z (none when L - 1 - z < 1). SV functions (`next_same`,
    `prev_same`, `next_zeros`, `prev_zeros`) run in Verilator against a search on every
    10-bit number and random 32-bit numbers; the Python against a search. Box `popnext`
    (a bit select, the rows of the formula step by step for the next or the previous, the
    jump to another length for zeros, previous / next). Self-checks 99, 80 and 143; 0059 in
    the coding path.
72. **A second visual review, five fixes (session 27, 2026-10-27).** The owner asked for
    only the changes that are really needed after the W rounds. Screenshots of the home
    page, the paths, the catalog and two questions (desktop and 390 px, light and dark)
    found five; the owner took all of them and logo option c. The logo is now the letters
    DV with the V an amber check (`logo.svg`, `favicon.svg`, the app icons from
    `make_icons.py`): the old two-pulse waveform read as Hebrew letters at header size and
    as a smudge in a browser tab. The question header puts the title first with the page
    tools beside it, then the chips and badges; on a phone the tools move to their own row
    under the chips, so the title opens the screen (it started about 210 px down, the
    statement about 540 px). "SV + Python" and "tested" are one badge, "קוד נבדק" (the
    languages in its tooltip; untested code keeps the language badge). Every page h1 takes
    the text colour (Material greys it, so the paths, catalog, level and tag pages had a
    faint title), h1 and h2 wrap with `text-wrap: balance` (0050 left "ID" alone on a
    line), and the catalog page hides the navigation sidebar, which held one link.
73. **Round Y, the reading experience (session 27, 2026-10-27).** The owner took Y393, Y394,
    Y396, Y397 and Y398 (not Y395, the calmer solution colours), and asked during the round
    that the search find only the questions themselves, with real symbols instead of TeX
    source, and noticed run-together words ("השאלותעם"). Y396 became: the search index keeps
    one document per question (its statement) and one per part (the part's statement);
    hints, solutions, code, boxes, traps, follow-ups and every other page are gone (1117
    documents to 194). `tools/search_text.py` reads the statement out of the built page and
    writes the math in plain symbols (all 6989 formulas of the site, no backslash left),
    each in a left-to-right isolate, since the results drop `<bdi>` and "O(n)" showed as
    "(n)O". Y393: hints, solutions, traps and follow-ups at the page size (16 px instead
    of 12.8 px), titles 14 px, explorer boxes inside unchanged. Y394: a table of short
    values is a grid (24 tables): narrow columns (the theme's 5rem per header had pushed
    0047's trace out of its step, hiding its last column on a desktop too), tighter on a
    phone, a sticky first column when it scrolls; 0047's named-row table no longer becomes
    cards. Y397: "what's new" and tags without the one-link sidebar. Y398: the tags page
    opens with a grid of every tag and its count, the lists in two columns. The bigger box
    text first made twelve pages wider than a phone (MathJax and the solution map scaled
    with it, and a grid kept the theme's negative scroll-box margin): math inside a box is
    0.8em (its old pixel size), the map and cost chips 0.64rem, a grid's scroll box stays in
    its column.
74. **Loose ends (session 27, 2026-10-27).** The owner's picks: Y395 as one grey rail with
    the colour in each label, folded tag lists, and the local 0050 failure fixed. Y395: the
    solution blocks share one quiet rail (`--sol-rail`), the kind's colour stays in its
    label, icon and map chip, and an open solution's frame is neutral. Tags: each tag's
    list folds under its name and count (the phone page from about 24,000 px to 3,300);
    a link to `#tag:...` opens its fold (reading-tools.js `openTarget`). 0050: the cause was
    not the scoreboard strip but a proof table 357 px wide in a 356 px scroll box, called
    "fits" although the theme's padding pushed it out; a table now fits when its scroll box
    does not overflow, measured again when the fonts load. The local phone check is clean.
75. **Round S4, the question page and navigation (session 27, 2026-10-27).** The owner's
    picks: the id and the title in the path bar, the tool names always under the icons on a
    touch screen, one line per question in the side navigation; no print style (S422 not
    taken). S419: the path bar's previous and next steps sit side by side with id and
    title. S420: `qt-name` under each icon under `hover: none` (the fold name follows its
    state), the hover tooltip off there. S421: one line per question in the side
    navigation, the current one in full, the full title as the tooltip. A CSS ellipsis cut
    English words inside Hebrew titles ("PCIe" read "Cle", "Sequence" "ence"), so
    reading-tools.js `fitWords` drops whole words from the end instead, for the side
    navigation and the path bar. Before the round, `main` had moved again (the other
    session's search list cleanup, no search highlight, and the CLAUDE.md rule for small
    fixes); merged without conflicts.
76. **Round S1, the questions' practice tools (session 27, 2026-10-27).** The owner's picks:
    expected values on every deterministic print, a self-check on every part with a short
    answer, no run panel for the nine questions without Python (S412 not taken), 0001 kept
    as it is (S414: the owner decision is closed). S411: 59 prints of 26 demos gained their
    value (29 of the 49 demos check their output now, 74 prints; before 14 and 15). The
    annotation ran each demo twice in separate processes and took only a print that runs
    once, gives the same short line both times and calls something (an echo of the input
    gets none). `py_run.matches` takes the value after a label ending in ":" or "=", so a
    comment holds the value alone. The other 20 demos print in loops only. S413: 14 new
    self-checks (0003, 0004 a, 0007 c and d, 0012 b, 0013 b, 0016 part b 1, 0023 b, 0033 b,
    0040 a, 0041 a, 0043 a and b, 0044 b), each recomputed in `tests/tools/test_selfcheck.py`
    (59 fields on 33 pages now, from 45 on 22). The other parts answer with code, an explanation or a general formula, or
    already have one (0058 d's value is its part c check); 0033 a was left out, since the
    page gives 24 by the formula and 25 by the simulation.
77. **Round S3, the boxes (session 27, 2026-10-27).** The owner's picks: presets in one
    scrolling row, no names under the playback icons. S416: the Josephus box (0016) kept the
    step counter of its last small circle when N grew past 128 (no circle, the play row
    hidden), so the scrubber read "0 of 23" and, after a reload, "0 of 63"; the counter is
    emptied there, which hides the scrubber. The Floyd warning was no bug: an answer line
    that is off keeps its last text only to hold its height. S417: `check_explorers.py`
    leaves off answer lines out of its comparison and puts every element's attributes in
    one order (a refitted figure set `style` and `data-fit-base` in either order), so it
    warns only about real differences. S418: three or more action buttons in a row go into
    one run (`ex-btnrun`, core.js `layout`) that scrolls sideways on a phone, fading at its
    end, and lays out as before elsewhere (`display: contents`); a row a view lays out as a
    grid keeps it (0024's events). Nine runs on eight pages, each one line instead of two to
    six at 390 px. The attribute order of S417 found a real bug on the first CI run: the
    ants box (0056) put a `<bdi dir="ltr">` inside its pole's `aria-label`, so the quotes
    broke the attribute and a screen reader read it garbled; the label is plain text now,
    and the check drops an attribute whose name is not valid on both sides.
78. **Round S2, figures where a page had none (session 27, 2026-10-27).** The owner's pick:
    only where a figure adds. Of the six pages first named, 0034 and 0038 have WaveDrom
    waveforms and 0057 generated tables, so the pages without a figure were 0045, 0046 and
    0047. New generators `tools/figures/q0045.py` (what the first weighing leaves for each
    result: the twelve balls as maybe heavy, maybe light, either or good, eight cases each),
    `q0046.py` (the grid of part a beside its dp table, the first 3 x 3 square marked in
    both; replaces the text drawing of step 4) and `q0047.py` (the columns of [3, 0, 2, 0, 4]
    with the 7 units of water; replaces the text drawing of the statement), each
    independent of the page code, with a legend, five new contrast pairs (64 in all) and a
    test per question that compares the generator with the page code and the page copy.
79. **Round S6, the styles in parts (session 27, 2026-10-27).** The owner's pick: a file per
    part. `extra.css` (4,020 lines) became twelve parts, `docs/stylesheets/01-base.css` to
    `12-rounds-y-s.css`, cut at top-level sections in the original order and loaded in that
    order, so the cascade is unchanged; `docs/stylesheets/README.md` lists them (excluded
    from the site). `check_contrast.py` reads every part in order. A regrouping by component
    was not done: later rounds refine earlier rules across components, so moving a rule
    between parts can change what wins. Checked: every built page is the same before and
    after apart from its stylesheet links, and the parts joined in order are the old file,
    so the cascade is the same. A computed-style fingerprint of every element was too noisy
    to prove it (the custom properties come back in a changing order, the repository widget
    loads its facts from the network, the hero animates).
80. **The question map, a knowledge graph (session 28, 2026-10-28).** The owner asked to
    try three Claude Code add-ons (Caveman, Claude-mem, Graphify) and then to run Graphify.
    Its code-only pass (tree-sitter, no LLM) mapped the infrastructure but not the
    questions (only the page headings), so the semantic pass was run on the 58 pages alone:
    six readers wrote, per question, its core concepts, secondary ones and related
    questions (every page read to its last line), merged into `tools/graph_concepts.json`
    (115 concepts in seven groups; `systemverilog` dropped as a secondary concept, it was a
    hub on 23 questions). `tools/graph.py` builds `docs/graph.html` with graphify (vis-network
    from unpkg): titles and levels from the front matter, the canvas and the side panel
    right to left, a Hebrew header with a link back to the site, the panel under the graph
    below 700 px, and a link to the question's page in the panel. `README.md` links it
    under the site link. Not in the navigation, not part of CI (graphify is not a site
    dependency); add a new question's entry to the JSON and rerun the script. What the map
    shows: math (36 questions with a core concept there) and algorithms (32) dominate;
    probability (5), puzzles as such (6) and digital design (10) are thin; no question is
    about debugging or a sliding window, and UVM, covergroups, async FIFO, clock dividers
    and credit flow control have one question each.

### Session 28 — 2026-10-28: code review fixes

81. **Code review of the S rounds, eight fixes (session 28, 2026-10-28).** A review of
    `docs/javascripts`, `hooks/questions.py` and `tools/check_explorers.py`; the owner took
    eight of its ten findings (not the cached "new" set or the computed-style read in
    `layout`):
    - The button run (`ex-btnrun`) no longer carries `ex-c-action`: as `display: contents`
      on a desktop its buttons were not children of the row any more, lost the actions'
      `order: 2` and showed before the inputs (0004, 0007, 0011, 0014, 0034, 0039, 0047,
      0053, 0059); and on a phone the button padding of `ex-c-action` (stronger selector)
      cut the run's end padding to 0.75rem, so the last button stayed under the fade. The
      run and its buttons now get `order: 2` in `12-rounds-y-s.css`.
    - `py_run.matches` takes one label only (`is_label`): "5 != 7", "5 <= 7" and
      "a = 5, b = 7" no longer match the comment "7"; "N = 5: 0110" still does.
    - `check_explorers.py` reports an attribute name that is not valid (a broken quote, the
      0056 bug) instead of dropping it.
    - The hook has one `_added_date`, which also reads a quoted date ("2026-10-28"), used by
      the header, the "new" chip, the recent strip and the what's-new page (`_added` gone).
    - `_header`, `_level_cards` and `_related` use `_base` and `_href` instead of building
      relative links inline.
    - `josephus.js`: the counter of a big circle is the else branch of the small one.
82. **Questions 0060 and 0061, from the owner's chat (session 28, 2026-10-28).** The owner
    picked two LeetCode-shaped questions asked at Meta and Google and asked for a part b
    that generalizes each; the generalizations were picked from multiple-choice questions.
    - **0060, the longest run of ones with up to k flips** (Max Consecutive Ones III):
      part a the sliding window on bits, part b the same window on any value of a bus with
      a counter per value (Longest Repeating Character Replacement, the \(O(n |\Sigma|)\)
      form with the proper shrink; the stale-maximum \(O(n)\) trick is a follow-up). The
      `onesk` box plays the window one cell per step in both modes.
    - **0061, how many tags** (Meeting Rooms II as outstanding transactions): part a the
      event sweep with the response-before-send rule at equal times, part b a pool for
      reads and one for writes against a shared pool, \(\max(R, W) \le S \le R + W\), in one
      sweep with two counters. The `tagpool` box steps the events over a timeline with the
      count as a step line.
    - Both junior, medium, kind code, in the coding study path, with figure generators
      (`q0060.py`, `q0061.py`), tests against every window / every moment, testbenches,
      demos with expected values and two self-checks each. Verilator could not be built in
      the sandbox (`flex` is not installable), so the SystemVerilog ran in CI only.

83. **The explanation panel of a box (session 28, 2026-10-28).** The owner asked for an
    interface that explains and illustrates the solution of every part; picked from
    multiple-choice questions: the solution's steps lit and the code synced to the steps,
    inside the existing box, for 0060 and 0061 first. `explain()` in `core.js` appends a
    fold "הסבר" with the steps as chips (the step of the moment lit), a line of the
    variables (before → after) and the page's own code (read from the page's tabbed block
    that names the function, in the language of the open tab, the annotation markers
    stripped) with the lines the step ran lit as `.hll`. The `onesk` and `tagpool` views
    call it after every draw, with the function of their mode (`longest_ones` /
    `longest_same`, `tags_needed` / `pools`). Two contrast pairs for the chips. Not yet
    on the older boxes: the owner wants to see it on the two pages first.

84. **Round S5, speed and access (session 28, 2026-10-28).** The owner's picks: loading by
    need and a weight report, a fixed check of the 404 page, and a scripted keyboard pass
    that stays as a check.
    - **S423 :** WaveDrom and its init script load only on the five pages with a
      ```` ```wavedrom ```` block (the hook adds the tags, as it adds the explorer scripts);
      the twelve stylesheet parts reach the browser as one `stylesheets/site.css` that the
      hook joins at the end of the build and links from every page and the 404 page (12
      requests become 1; the parts stay the source). The phone check prints every page's
      weight (HTML KB, bytes fetched, requests), warns over 400 KB of HTML and names the three
      heaviest pages. The heaviest stay as they were: 0016 (378 KB, 230 KB of them its SVG
      figures), 0025, 0023, 0024 (the reference-model code and tables); the owner chose not
      to trim them.
    - **S424 :** `tools/check_404.py` serves the site under `/DV-Interview-Questions/` and
      answers a missing address with 404.html as Pages does; six views (three addresses at
      390 and 1200 px) check the page, its assets, the guess, the level links, the random
      question, the search button and axe. All clean on the first run.
    - **S425 :** `tools/check_keyboard.py` walks five pages with Tab (visible stops, names,
      focus rings, the skip link first, no trap) and presses the keys of the components on
      0060. Findings: the trap and lightbox reports of the first run were the check's own
      mistakes (same-looking elements counted as repeats; the lightbox stays in the DOM when
      closed); the one real finding was MathJax's contextual menu, which made every formula
      a tab stop (hundreds on a math-heavy page), now off in `mathjax.js` (the assistive
      MathML stays). Both checks run in the CI build job. CLAUDE.md lists ten checks now.

85. **The phone's enlarged text (session 28, 2026-10-28).** The owner saw every page
    zoomed out on Android Chrome, cut at the sides with the navigation drawer beside it.
    The phone's text scaling was on: at 1.3 times the text, some rows grew wider than the
    screen and Chrome zoomed the page out to fit them (44 pages). Fixed: the part bar's
    chips scroll, the box's playback bar and the tools under the title wrap, an inline
    formula wider than its line scrolls on its own (`reading-tools.js` marks it `.is-wide`
    by its line's content box, both sides), the fields of a box shrink to it, and the
    tables of the 0031 and 0037 boxes scroll. `check_phone.py` loads every page a second
    time with the text enlarged 1.3 times (`--font-scale`) and fails when it is wider than
    the screen. Published (`main` 2c04376); the owner checks the phone.
86. **A slider and its value on one row (session 28, 2026-10-28).** The owner saw the
    value of the base slider of 0044 on a row under the slider on the phone. A slider's
    label wrapped freely and the slider kept its 11rem, so the value dropped to the next
    row: 30 pages had it, some at the normal text size too (0013, 0014, 0017, 0035, 0043,
    0044). Fixed for every box, at every width (`12-rounds-y-s.css`): a label of a
    `<span>`, a slider and an `<output>` does not wrap, the slider shrinks first (down to
    3rem), the label keeps up to 40% of the row and wraps its words beyond that, and on a
    phone the value takes only its own width. The number field of the 0016 box moved to
    its own `<label>`. `check_phone.py` fails, at both text sizes, when a slider's value
    sits on another row or a slider's label is cut off at the box's edge.
87. **Questions 0056 to 0061 renumbered to 0057 to 0062 (session 28, 2026-10-28).** The
    owner wanted the windowed version of 0055 next to it, as 0056. The pages, tests,
    figure generators, study paths, the question map and every reference moved together
    (the work log above keeps the old numbers). An old address goes on to the new page:
    `dvq_renumbered` in `mkdocs.yml` maps the old ids, and the 404 page replaces the location
    with the same level and slug under the new id, the anchor kept (`check_404.py` opens one).
    `marks.js` moves what a browser saved, once (`dvq-renumbered-<date>`): the marks by id,
    the last question opened, and the self-checks and the boxes' saved states by the page's
    path. Its `RENUMBERED` list and the one in `mkdocs.yml` must agree (a hook test checks).
88. **One machine at a time in the 0055 box (session 28, 2026-10-28).** The owner did not
    want two state diagrams. The `divfsm` box has a list, "שרשור ל-LSB" (read from the MSB,
    part a) or "שרשור ל-MSB" (read from the LSB, part b), and draws one ring; the buttons
    concatenate a digit at the chosen end. The ring is now a shared `ring()` in
    `divfsm.js`.
89. **Question 0056, divisible by 3 in a window of L bits (session 28, 2026-10-28).** The
    owner's question: 0055 with the number a window of the last L bits, zeros after reset;
    part a a bit entering as the LSB (the highest leaves), part b as the MSB (the lowest
    leaves), part c any m, base, L and start window (`INIT`). The answer: a shift register
    and the remainder updated by the bit in and the bit out, r' = (2r + b − 2^L·out) mod 3 and
    r' = (2(r − out) + 2^(L−1)·b) mod 3 (the MSB way divides by B, so it needs gcd(B, m) = 1).
    The minimal machines were counted by refinement: 2, 4, 7, 14, 27, 54, 107, 214 states
    for L = 1 to 8, the same both ways, above 2^(L−1) from L = 3, so L flip-flops at least;
    the page proves 2^(L−2). The `winfsm` box: m, base, L, the direction, the start window
    and the digits; the data path every step, and the ring of the direct machine up to 16
    windows. Tests: every bit string and start window up to L = 6, random digits in six
    bases, the proof's distinguishing bits, the explorer against the page, and a testbench
    of nine parameter sets (run here with the pip Verilator, below).
90. **How the formula is built, in the boxes of 0055 and 0056 (session 28, 2026-10-28).**
    The owner wanted the box itself to show how each part reaches the formula that draws
    the diagram, with the numbers put in, so the moves between states are easy to follow.
    Under the summary, the way to the formula in four steps for the chosen direction, with
    the box's m, base and L put in (0056: the window's arrow and the remainder's update).
    Under the ring, a table of the moves out of the current state: a row per digit with the
    formula and its numbers (0056: the next window and the next remainder), the row of the
    next digit marked "הבאה". A click, or Enter / space, on a state of the ring shows its
    moves in the table and its edges dashed; a second click or any step goes back.

91. **Round M, motion and finish (session 28, 2026-10-28).** The owner asked for a UI/UX
    review with more motion and a more professional look (logo, home, question pages,
    404). Fourteen proposals in four groups; the owner took twelve (not the animated
    light / dark switch nor the 404 as a typed log) and asked for one push of all of them.
    A new part, `13-motion.css`, and a new script, `motion.js`; every movement is off under
    reduced motion, and the scripts skip it in an automated browser.
    - M3, logo: the mark is inline (`overrides/partials/logo.html`, the paths of
      `logo.svg`), drawn on the first page of a visit (sessionStorage) and under the
      pointer. Its amber is `--site-logo-v`.
    - M4, header: a shadow once it scrolls (Material's `md-header--shadow`), and an amber
      bar sliding along the table of contents to the active link. The reading progress
      line was already in the part bar, so no second one was added.
    - M1 and M2, hero: the waves roll by one width (drawn twice side by side) with a
      sweeping amber cursor; on 76.25em and up a live example beside the text runs the
      machine of 0055 part a over 27, 10, 21, 14, 6 and 13 (`_hero_fsm` in the hook draws
      the last frame of 27, `home.js` runs it, both pause off screen).
    - M12, cards: the top edge fills with amber under the pointer, the icon tilts, the
      progress bar fills in.
    - M5, question header: a card; the topics as chips (`qh-tag`); the tools along the
      card's foot with their names on a pointer screen (touch keeps S420's layout).
    - M7 and M8: a self-check's right answer draws its check mark, a wrong one shakes the
      field and colours its border; a row of dots above a run of two hints or more.
    - M9: `.explorer:empty` is a skeleton with a sheen until the box is built.
    - M6: `@view-transition` cross-fade; the followed question link and the page's `h1`
      share the name `dvq-title`, so the title moves into place.
    - M13: buttons get a raised shadow, the header buttons press, and the focus ring
      settles in (only its offset moves).
    - M10: the footer (`overrides/partials/footer.html`): the mark, the name and the
      numbers, the levels with their counts, the site's pages, then the copyright line
      (the hook no longer appends "מה חדש" to the copyright; the footer lists it).
    - M11, 404: 404 on a seven-segment display and a waveform whose bus reads question ids
      until the cursor at 404 ns, where it turns to the unknown state X
      (`--site-x-state`); drawn once, the display flickers on, the X pulses.
    Eight colour pairs were added to `check_contrast.py`.

92. **A review of ten random questions, round R (session 28, 2026-10-28).** The owner asked
    for a pass over ten random questions with proposals for the explanations and the
    boxes: 0009, 0012, 0020, 0023, 0026, 0027, 0037, 0039, 0059 and 0061, one reviewer
    agent per pair. Seven statements were wrong and were fixed first, straight to `main`
    (f397198): 0037 three flops at 1 GHz with τ = 50 ps give 1.1·10^17 seconds, not years;
    0039 the n-versus-n + 1 trap flips at n = 2^t, eight drops tell 93 thresholds apart,
    five eggs already reach seven drops; 0009 the swaps are summed over the cycles; 0020
    the greedy proof's monotone quantity; 0023 a later posted write may pass the read;
    0059 `parity_move` costs O(n) per move as written. The owner then took the
    explanations and traps and the boxes that show the key idea (not presets, not new
    modes), and for 0037 kept the model with a note and a follow-up on the per-stage form.
    One agent per pair made the changes on disjoint files, each under its own heading in
    `11-questions.css`; every claim was checked by exact computation, and new tests cover
    the new numbers. Per question: 0009 a bar with person 0, his swap count and the walk
    without him, follow-ups on the 231 cycle types and the unchecked box range; 0012 one
    difference per d in the step line, d throughout part b, the boxes swapped, the e = ±1/2
    case, a follow-up on 5 to 7 digits; 0020 its own notation in the pcie box
    (`data-notation="c"`), RCB facts, a uniformly random split; 0023 the split count of a
    sent read, a follow-up for MPS below MRRS; 0026 a bound proving 2.5 h optimal for any
    plan, the points defined first, the drop point argued in the text, fractions and the
    wait in the box; 0027 the ratio column, the peak named only once reached, the rounding
    trap's example, d ≤ 0; 0037 why settling is exponential, the model's assumption, the
    per-stage follow-up (15 years instead of 297), the f_data trap, the tail on a log scale
    in metamc; 0039 the first floor is not unique (8 to 37), the padded lower bound, all 46
    worst-case dots; 0059 the parity colours, sums and fallback in the box, the proof's
    (S + d) / 2 and a worked cell; 0061 the left end frame by frame with a move counter,
    the invalid-window fact, the real `best`-before-`while` trap, the edge cases. Left as
    they were: the figures of 0027 that looked duplicated (they show different values or
    the two forms of the condition), the mermaid colour of 0020 (no theming hook; 0005,
    0018 and 0019 share it). 0062 still has ordinary spaces before its colons (seen while
    fixing 0061).

## In progress

- **Session 28 (2026-10-28):** the question map, `docs/graph.html` (work log item 80),
  linked from `README.md`; when a question is added, add it to `tools/graph_concepts.json`
  and run `python tools/graph.py` (needs `pip install graphifyy`).
- **State (2026-10-27, session 27):** `main` is 84ae476 (fix rounds 1 to 6a, question 0048, review rounds V1, V2, V3, V3b, V4a, V4b, V5, V7, questions 0049 to 0058 with 0052 generalized and 0056 part d), deployed; then question 0059 (work log item 71) and the design rounds W1 to W4 (items 65 to 70), merged on the design branch and published to `main` (4186f5a); the second visual review (item 72) published; round Y (item 73) and the loose ends (item 74) published (`main` 7f3770b, with the other session's search cleanup merged); S4, S1, S3, S2 and S6 (items 75 to 79) published together after one green CI run (`main` 59ceca4, 2026-10-28); the code review fixes (item 81), questions 0060 and 0061 (item 82) and the explanation panel (item 83) published (`main` 82b60f4); round S5 (item 84) and the fix for the phone's enlarged text (item 85) published (`main` 2c04376); the S series is done; a slider and its value on one row (item 86) published (`main` a4e0b47); the renumbering (item 87), the 0055 list (item 88) and question 0056 (item 89) published (`main` 905863d); the formula steps and the moves table in both boxes (item 90) published (`main` 8d8bd24); round M, motion and finish (item 91) published (`main` 3c31a22 and this log); the review of ten questions (item 92): the fixes published (`main` f397198), the improvements on the branch.
  61 questions (0022 was
  merged into 0016), every one with an explorer box. CI runs the lint, the contrast check,
  the tests (pytest and Verilator), the strict build, the link check, the phone check
  (axe findings and figure text under 9 px fail) and the explorer click-check.
- **Done in session 26:** 0044 became a coding question (work log item 48); fix rounds 1
  and 2, axe and small text (item 49); fix round 4, the documents (item 50); fix round 3, the CI actions (item 51); fix round 5,
  the cloud sandbox (item 52); question 0048, the farmer, the food and the water (item 54).
- **Review of session 26:** findings and rounds V1 to V7 (now in `HANDOFF-archive.md`); V1 to V5 (V3b, V4a and V4b
  included) and V7 are done (work log items 55 to 59), V6 waits for the owner; the V3 split map by
  completion count was not picked (only collapsed).
- **Fix rounds of session 26:** rounds 1 to 5 are done (items 49 to 52), and round 6 part
  a, the jump check (item 53); part b, a visual diff of the phone screenshots, was not
  picked.
- **Owner's checks on the live site (github.io is not reachable from the sandbox):** the
  WaveDrom diagrams of 0034, 0035 and 0038; dragging in the boxes on a real phone; the
  timing strips of 0001 and 0035 scrolled sideways; 0025 part b step 11 and its code
  highlights; the boxes of 0018 and 0026 while playing and the enlarge button on the
  hourglass frames; the code of 0044 parts a and b and its run panel; the PCIe box legend
  and the 0023 request figure on a phone.
- **Waiting on the owner:** the giscus ids (README, Comments) in `extra.comments` of
  `mkdocs.yml`; a look at the social card of a shared link; keep or replace 0001.
- **Session 27:** a visual review and the fifth series W1 to W5 (look, motion, the run
  panel, practice tools); the owner picked W1 to W4 (catalog on its own page, amber traps,
  off-white, CodeMirror). W1 to W4 are done (work log items 65 to 70, merged with
  `main`'s questions 0049 to 0059). Content idea: add
  expected-value comments to the `print()` lines of more demos (only 4 of 39 have them).
- **Next, the owner picks:** a round of the sixth series under **Proposals** (new
  questions, interactive tools, visual aids), or questions the owner sends. Every earlier
  proposal that was not picked moved to `HANDOFF-archive.md` in session 27, at the owner's
  request (the owner wanted fresh proposals).
- **Decision (owner, session 20): the repository stays public.** Options kept for later:
  a private "interview bank" beside the public site; two builds from one repository (the
  public one without the interviewer, trap and follow-up blocks, the full one behind a
  password on Cloudflare Pages or Netlify); or private with no Pages site (GitHub Pro is
  needed to publish Pages from a private repository, and the site would still be public).
  Visibility is changed under Settings, General, Danger Zone.

## Open items

### Owner decisions

- [x] Staff level removed (session 19, owner's call). Senior has nine questions (0007, 0011, 0019, 0020, 0021, 0023, 0024, 0025, 0037).
- [ ] Fifth series: W1 to W4 done on the branch (W348's drawn check mark not picked); W5 not picked; `main` when the owner asks.
- [ ] Pick rounds from **Proposals**: the owner's current direction is the eighth series, S1 to S6 (improve what exists, no new questions); the question proposals X360 to X410 wait; the older proposals are in the archive.
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
- [ ] When a Verilator release newer than 5.052 is out, bump `VERILATOR_REF` to its tag and check that 0011 and the 0014 subclass still pass.

---

## Question variety

### Coverage today (61 questions)

| Level | Questions | Main topics covered |
|-------|-----------|---------------------|
| Student | 0001, 0002, 0003, 0010, 0012, 0015, 0032, 0036, 0040, 0048 | digital logic, bitwise, sorting, stack, digit puzzles (with number bases in 0012 part c), conditional probability, BFS over a tiny state space (wolf, goat and cabbage), LFSR periods and primitive polynomials, the shortest path by two reflections (the farmer, the food and the water) |
| Junior | 0004, 0005, 0006, 0008, 0009, 0013, 0014, 0016, 0017, 0018, 0026, 0027, 0028, 0029, 0030, 0031, 0033, 0034, 0035, 0038, 0039, 0041, 0042, 0043, 0044, 0045, 0046, 0047, 0049, 0051, 0053, 0055, 0056, 0058, 0059, 0060, 0061 | FIFO depth from rates, Gray pointers and CDC, a divide-by-3 clock, SVA for a handshake, logic puzzles, BFS (remainders, hourglass states), O(n) scans, permutations, SV constraints, Josephus (proof), cycle detection, motion and speed ratios, sequences and a single-peak proof (cake split), relative speed and counting with inclusion-exclusion (clock hands), geodesics on a box by unfolding (spider and fly), Dijkstra over a bitmask state with the greedy rule (bridge and torch), a price list per load and a range function (the camel and the water), selection from partial orders (horse races without a stopwatch), the Kaprekar step as code with a hash and a closed form for the digits (0044), the odd ball in fewest weighings (0045), the largest square, rectangle and right triangle of ones by dynamic programming and a stack (0046), trapping rain water by two pointers and a heap (0047), the UVM testbench architecture (0049), poisoned bottles as digits in base b + 1 (0051), an ALU covergroup and its closure time (0053), a divisible-by-m state machine from the MSB and the LSB (0055), ants on a pole by ghosts (0056), coins in a row by a parity trick and an interval DP (0058), the next number with as many ones by Gosper's hack, the previous by the complement, and the same for zeros across lengths (0059), the longest run of ones with k flips by a sliding window, and of one value on a bus (0060), the tags a list of transactions needs by an event sweep, one pool and two (0061) |
| Senior | 0007, 0011, 0019, 0020, 0021, 0023, 0024, 0025, 0037, 0050, 0052, 0054, 0057 | synchronizer MTBF, SV constraints, randomization, probability, combinatorics, Dijkstra on a state graph, PCIe completion rules, recursive enumeration, counting formula with proof, generalized Josephus (recurrences, induction), a PCIe endpoint reference model (classes, block memory, scheduling), a USB4 credit flow-control reference model (modulo counters, loss and resynchronization), a PCIe Ack/Nak reference model (Retry Buffer, Replay, error handling), an out-of-order scoreboard (0050), waiting times of coin patterns and Penney's game (0052), round-robin and weighted arbiters with SVA (0054), a constant-memory checker for missing tags (0057) |

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

## Site redesign plan (decided 2026-10-16)

The owner reviewed the site (desktop and phone screenshots of the home page, a level page,
question pages open and closed, and the tag index) and asked for a more professional, less
generic look, with clearer and better explained answers. Findings that drove the plan:

- The home page was a heading, a paragraph and a table; the colours and the icon were
  Material's defaults; the footer said "Made with Material for MkDocs".
- Question pages opened with the same metadata twice (Material tag chips above the title,
  then the metadata box), and the title started with the id ("0002 · ...").
- On a phone the five-column question tables broke: titles wrapped word by word and the
  topics column was pushed off screen.
- Open solutions were one long run of identical green blocks, with no one-line answer at
  the top, and "what the interviewer checks" buried at the end.
- Difficulty was shown with emoji, which render differently on every OS.
- No previous / next links, no related questions, no "open all" button.

### Decisions

| Topic | Decision |
|-------|----------|
| Colour palette | **Navy + amber** (variant 1 of three mock-ups: navy + amber, forest + gold, charcoal + teal). Light: primary `#1b2a4a`, accent `#d99a00`, links `#1f4e9c`. Dark: primary `#2a3d66` (was `#243760`), accent `#ffc233`, links `#8db3ff`, page background `#171f2d` (was `#141a26`), code background `#1b2231`; every pair is checked by `tools/check_contrast.py` |
| Logo / favicon | A drawn SVG: the letters DV, the V an amber check mark (white D on the navy header; navy rounded square for the favicon); until session 27 a waveform ending in a check |
| Question id | A small label above a clean title; the id stays in the side navigation and the tables |
| Footer | Site name + link to the repository, no personal name; the Material generator line is off |
| Table filters | Chip buttons, single choice per group (level, difficulty, topic), plus the text search |

---

## Proposals — sixth series, rounds X1 to X6 (session 27, 2026-10-27, owner picks)

Fresh proposals, at the owner's request: none of them repeats an idea of the earlier series
(those are in `HANDOFF-archive.md`, "Proposals archived in session 27"). Three kinds: visual
aids that the pages do not have yet (X1), interactive tools of a new type rather than one
more stepping box (X2, X3), and new questions with an aid of their own (X4 to X6). Item
numbers continue the global count (360 on). Size: S under an hour, M a few hours, L a day
or more.

What the site has today, so the new ideas differ from it: generated SVG figures with
legends, step-through boxes with play / scrub / presets per question, drags in a few boxes,
proof panels inside boxes, a run panel for Python, study paths, marks and practice mode.

**Round X1 — visual aids of a new kind**

| Id | Idea | Where first | Size |
|---|---|---|---|
| X360 | **Live schematic under a waveform**: a generated gate / flop schematic whose wires take the colour of their value (0, 1, X) at a time cursor; dragging the cursor along the WaveDrom diagram (or the box's timing strip) moves the schematic with it, so the reader sees which flop holds what at each edge | 0001, 0035, 0040 | M–L |
| X361 | **Growth chart in the cost section**: a small log-log plot of the operation count against n for the page's approach and the obvious one (n, n log n, n², 2^n), the page's own n marked with the number of steps it means ("n = 10⁵: 10¹⁰ steps, about 10 s") | 0003, 0017, 0046, 0047 | S–M |
| X362 | **Orders-of-magnitude ruler**: one horizontal log scale from picoseconds to the age of the universe with the page's quantities placed on it (a clock period, a resolution time, an MTBF), so "10⁻⁸" and "300 years" become distances | 0037, 0033, 0024 | S |
| X363 | **Scenario illustration in the header**: a small drawn SVG of each puzzle's setting (two hourglasses, the camel and the depots, the bridge with the torch) in the site's line style, also on the social card; the first thing the eye meets on the page | the puzzle pages | M |
| X364 | **Wrong-versus-right diff for a trap**: a trap whose mistake is in code shows the buggy lines and the fixed ones side by side, the changed tokens marked, and the input that tells them apart with both outputs | 0003, 0010, 0046 | S–M |
| X365 | **Map of techniques**: an interactive graph of all questions joined by the technique they share (BFS, DP, two pointers, Gray code, invariants, reflection), on the paths page; a tap on a technique lights its questions, a tap on a question opens it | paths page | M |

**Round X2 — interactive tools that check the reader's own answer**

| Id | Idea | Where first | Size |
|---|---|---|---|
| X366 | **Waveform input editor**: the reader clicks the cells of the input signals (a WaveDrom-like grid) and the page's circuit model draws the outputs at once; presets for the tricky inputs (a one-cycle glitch, back-to-back pulses) | 0001, 0038, 0040 | M |
| X367 | **"Draw your FSM" and get a counterexample**: the reader builds a state machine (states, edges labelled 0 / 1, outputs); the page compares it with the reference by a product-machine BFS and shows the shortest input on which they differ, or "equivalent" | 0040, a new FSM question | M–L |
| X368 | **Karnaugh map you can group**: click cells to set 1 / 0 / don't care, drag rectangles to group, the expression and its gate count update; a static hazard (two groups that only touch) is flagged with the consensus term that removes it | the static hazard question (X377) | M |
| X369 | **Distribution playground for constraints**: a small subset of SystemVerilog constraints (ranges, `!=`, `<`, `dist`, `solve before`) typed in a field, solved by enumeration in the browser for small domains, with the histogram of each variable over 10,000 draws next to the uniform one | 0007, 0011, 0014 | M–L |
| X370 | **Register bit playground**: an 8 / 16-bit register of toggles shown at once as binary, hex, unsigned, two's complement, Gray and BCD, with shift, rotate, sign-extend and the tricks `x & (x − 1)`, `x & −x` as buttons that animate the bits | the bit-tricks question (X385), 0002, 0034 | S–M |
| X371 | **Whiteboard beside the question**: a drawing layer (pen, eraser, undo, a grid) that the reader opens in practice mode to sketch as in an onsite interview; saved per question in the browser, cleared on demand | every page | M |

**Round X3 — one shared engine for X366 to X368**

| Id | Idea | Size |
|---|---|---|
| X372 | **A tiny cycle simulator in JavaScript** for the page's design described as data (signals, flops, gates, a next-state table), with a Node test that checks it against the page's Python model on random inputs; X360, X366 and X367 draw from it instead of a model per question | M |

**Round X4 — new questions: digital design and DV**

| Id | Question | Level / difficulty | The point | Aid | Size |
|---|---|---|---|---|---|
| X373 | **Count the ones in a 16-bit word in hardware**: the fewest full adders and the shortest depth | junior / medium | a carry-save adder tree, depth log₃/₂ n, against a chain of adders | the tree drawn level by level, a slider for the width | M |
| X374 | **Ripple-carry against a prefix adder**: when is the 64th sum bit ready | junior / medium | delay n against log₂ n, the generate / propagate operator, Kogge-Stone's wiring | the prefix graph lit stage by stage for chosen inputs | M |
| X375 | **Booth multiplication**: multiply −7 by 5 in 4-bit two's complement | junior / medium | recoding runs of ones, why Booth handles signs for free | a step-through of the partial products and shifts | M |
| X376 | **Gate a clock without glitches**: why `clk & en` glitches, and the latch-based clock gate that does not | junior / easy | the enable changing while the clock is high; latch transparency | X366 editor with the enable moved across the clock | S–M |
| X377 | **A static hazard**: f = AB' + BC glitches when B falls; find and remove it | student / medium | the consensus term AC, two-level timing | X368 Karnaugh map, a waveform of the glitch | S–M |
| X378 | **Johnson counter**: count to 8 with the fewest flops and glitch-free decoding | student / easy | n flops give 2n states, one bit changes per step, two-input decoders | the ring of states with the changing bit lit | S |
| X379 | **March test for a memory**: which faults March C− finds (stuck-at, transition, coupling) and why the read-after-write order matters | senior / hard | element order, detection proof per fault model | a memory grid with an injected fault and the march elements stepping | M–L |
| X380 | **Byte enables on an unaligned write**: a 32-bit bus writes 3 bytes at address 0x...6; which lanes, which strobes, what the memory holds after | junior / medium | lane = address mod 4, splitting across a word boundary, the reference model | the four lanes as boxes, the bytes sliding into place | S–M |
| X381 | **Dynamic power**: P = αCV²f; what halving V, f or the activity buys, and why clock gating and Gray counters save power | junior / easy | the V² term, activity of a binary against a Gray counter | sliders with the four terms and the bar of P | S |

**Round X5 — new questions: electrical engineering basics (asked in EE interviews for DV roles)**

| Id | Question | Level / difficulty | The point | Aid | Size |
|---|---|---|---|---|---|
| X382 | **Two capacitors**: a charged capacitor is connected to an equal empty one; where did half the energy go | student / medium | charge is conserved, energy is not; the resistor takes half whatever its value | the energy bars before and after, R as a slider that changes only the time | S–M |
| X383 | **RC step response**: the time to reach 90%, and the rise time 10% to 90% (2.2 RC) | student / easy | e^(−t/RC), the log of the ratio | the curve with the two thresholds draggable | S |
| X384 | **Op-amp gain from a schematic**: inverting, non-inverting and a summing amplifier; what the ideal op-amp rules give | student / easy | virtual short, no input current | the schematic with node voltages written on it as the inputs change | S–M |

**Round X6 — new questions: algorithms and puzzles not proposed before**

| Id | Question | Level / difficulty | The point | Aid | Size |
|---|---|---|---|---|---|
| X385 | **Bit tricks**: is x a power of two, the lowest set bit, count ones in as many steps as there are ones | student / easy | `x & (x − 1)` clears the lowest one | X370 register playground | S |
| X386 | **Shuffle a list uniformly**: why "swap each item with a random position" is biased, and Fisher-Yates | junior / medium | n^n outcomes do not divide evenly by n! | the histogram of the 6 orders of 3 items for both methods after many draws | S–M |
| X387 | **Sample k lines from a log you can read once** (reservoir sampling) | junior / medium | the probability invariant k / i, proof by induction | the reservoir as slots, each new line's chance shown | S–M |
| X388 | **Sliding-window maximum** in O(n) with a deque | junior / medium | indices kept in decreasing value order | the deque as chips, the window moving | S–M |
| X389 | **A queue from two stacks**, amortised O(1) | student / easy | each item moves at most twice | the two stacks animated with a cost counter | S |
| X390 | **Nim**: three heaps, who wins and how to move | junior / medium | the XOR of the heap sizes, why a zero XOR is a losing position | a game against the page, the XOR of the heaps shown in binary | S–M |
| X391 | **Weights for every load**: the fewest weights that measure every whole load from 1 to 40 on a two-pan balance | student / medium | powers of 3, balanced ternary digits −1 / 0 / 1 | a balance with the load and the weights placed for the chosen number | S–M |
| X392 | **Three switches, one bulb in another room**, one visit | student / easy | use a third state (heat) | none needed: a short page with the reasoning as a table | S |

Suggested order: X364 and X361 (small, on pages that exist), X385 with X370, then X377 with
X368 and X376 with X366 (a question and its tool together), then X372 before X367.

## Proposals — seventh series, round Y, the reading experience (session 27, 2026-10-27)

A third visual review, after work log item 72: the inside of a question (hints, an open
solution, traps, follow-ups, the run panel), the level, tags and "what's new" pages and the
search, desktop and 390 px, light and dark. Item numbers continue at 393. Size as above.

| # | Finding | Proposal | Size |
|---|---|---|---|
| Y393 (done, item 73) | Hints, solutions, traps and follow-ups are set at 12.8 px (Material's admonition size), the statement at 16 px: the core text of the site is the smallest, and on a phone it is small | body text of those blocks at the page size (0.8rem); titles, chips and code stay | S |
| Y394 (done, item 73) | On a phone a table of 5+ columns that does not fit becomes cards. A table whose rows are named in its first column (0047: i, height, maxL, maxR, water) turns into unreadable cards of number pairs, and a 4-row trace takes about 750 px | tighter cell padding on a phone, so short tables fit and stay tables; a table with row names in its first column scrolls sideways with that column sticky, never cards; cards only for wide tables of long text | M |
| Y395 (done, item 74) | An open solution shows a green frame, an amber short answer and five coloured side rails (idea, steps, code, proof, cost), next to teal hints, a teal follow-up box, a purple run panel and an amber trap group | one quiet rail colour for the solution blocks, the colour kept in each block's icon, title and map chip; the open solution's frame neutral | M |
| Y396 (done, item 73) | The search lists the catalog page as one run-together blob ("#שאלהמשרהקושי 0001גלאי..."), every tag of the tags page and every date of "what's new" ("27 באוקטובר 202611 שאלות"), above or between the questions | leave the catalog, tags and "what's new" pages out of the search index (front matter `search: exclude`), so a search finds questions and their sections | S |
| Y397 (done, item 73) | "What's new" and the tags page have a navigation sidebar with one link (the catalog's was hidden in item 72) | hide the navigation on those two pages too | S |
| Y398 (done, item 73) | The tags page is one long column of lists, about 17,800 px on a desktop and 24,000 px on a phone, with 40 tags in the contents sidebar | a compact grid of tag chips with counts at the top, each tag's list in two columns on a desktop | M |

Not changed: the home page, the cards, the path box and the footer read well; the 404 page
could not be judged locally (its assets point at the site path).

## Proposals — questions given in chat (session 27, 2026-10-27, owner picks)

The owner asked for puzzles and LeetCode-style coding with less hardware; these were
explained in the chat (problem, a short solution, the trap) and are recorded here so they
are not lost. Item numbers continue at 399. None is on the site; check each example in a
test before writing a page.

| # | Question | Level | Idea | Size |
|---|---|---|---|---|
| X399 | Longest substring without a repeated character | junior / medium | sliding window, last index of each character | M |
| X400 | Number of subarrays with sum k (negatives allowed) | junior / medium | prefix sums and a counter; why a window fails with negatives | M |
| X401 | Number of islands as land is added one cell at a time | senior / hard | union-find with path compression, the count after each step | L |
| X402 | Cheryl's birthday | student / medium | elimination from what each person knows, as a table | M |
| X403 | The sack of fake coins (ten sacks, one weighing) | student / easy | take i coins from sack i, the missing weight names the sack | S |
| X404 | How many squares and rectangles on a chessboard | student / easy to medium | Σk² and C(9, 2)² | S |
| X405 | Smallest window that contains every character of t | senior / hard | variable window with a "missing" counter, repeats in t | M |
| X406 | Longest substring with at most k distinct characters | junior / medium | window with a counter map, delete keys at zero | M |
| X407 | Longest run of one letter with k replacements | junior / medium | window length − max count ≤ k; why max count never needs to shrink | M |
| X408 | All anagrams of p in s | junior / medium | fixed window, 26 counts and a "matched" counter | M |
| X409 | Shortest subarray with sum at least target (positive numbers) | junior / medium | shrinking window; follow-up with negatives (prefix sums and a monotonic deque) | M |
| X410 | Longest run of ones with k flips | student / medium | window with a zero counter | S |

X399 and X405 to X410 can form a "sliding window" study path in the order X410, X399,
X406, X409, X408, X407, X405, with one shared box (the string as a row of cells, the window
as a moving frame, the counter map beside it, left and right stepping).

## Proposals — eighth series, rounds S1 to S6, improve what exists (session 27, 2026-10-27)

At the owner's request: no new questions, only the existing 58 questions, the site and its
interfaces. Numbers from the built site and the repository on 2026-10-27. Item numbers
continue at 411.

**Round S1 — the questions' practice tools (content, no new questions)**

| # | Finding | Proposal | Size |
|---|---|---|---|
| S411 (done, item 76) | 35 of the 49 starting scripts (`tests/<id>/demo.py`) have no expected value in their `print()` comments, so the run panel shows no ✓ / ✗ for them | add the expected value to every `print()` of those demos (the test already checks each one) | M |
| S413 (done, item 76) | 36 questions have no "try it yourself" answer field (`selfcheck`, 22 have one) | a self-check field on every part whose answer is a number, a formula value or a short word | M |

**Round S2 — figures where a page has none**

| # | Finding | Proposal | Size |
|---|---|---|---|
| S415 (done for 0045 to 0047, item 78) | 11 pages have no static figure (0001, 0002, 0003, 0034, 0036, 0038, 0045, 0046, 0047, 0057, 0059); their only picture is the box | one generated figure each where it explains the idea at a glance (0046 the DP grid, 0047 the water profile, 0045 the weighing tree, 0038 the handshake waveform...), via `tools/figures/` | L |

**Round S3 — the boxes: bugs and consistency**

| # | Finding | Proposal | Size |
|---|---|---|---|
| S416 (done, item 77) | `check_explorers.py` warns that a box link or the remembered state draws another box: 0016 (Josephus, 8 steps instead of 21) and the Floyd box (4 instead of 1) are real differences | fix the state codec of those boxes so a link and a reload restore the same box | M |
| S417 (done, item 77) | the same check warns on 0036, 0020 and the cake box only because attributes come back in another order (`style` and `data-fit-base`) | compare the boxes with attributes in a fixed order, so only real differences warn | S |
| S418 (done, item 77) | box controls on a phone: icon buttons without names, presets that wrap into several rows on some boxes | one review pass of every box at 390 px: names under the playback icons on touch, presets in one scrolling row | M |

**Round S4 — the question page and navigation**

| # | Finding | Proposal | Size |
|---|---|---|---|
| S419 (done, item 75) | the path box shows the previous and next steps as ids only ("הקודם : 0002") | the title beside the id, cut with an ellipsis on a phone | S |
| S420 (done, item 75) | the page tools are five icons without names; a touch screen has no hover tooltip | a one-time row of names under the icons on a phone (dismissed and remembered), and the names in the toolbar's accessible labels as today | S |
| S421 (done, item 75) | the side navigation wraps long titles into two or three lines (0023: "Endpoint – כתיבה, קריאה ושידור Completions") | one line per question with an ellipsis and the full title as a tooltip, the current one highlighted | S |

**Round S5 — speed and access**

| # | Finding | Proposal | Size |
|---|---|---|---|
| S423 (done as loading by need and a weight report, item 84) | the heaviest pages are 0016 (396 KB of HTML), 0025 (312 KB), 0023, 0024 (248 KB each) | find what makes them heavy (inline SVG repeated in tabs, long tables) and trim it; a page-weight line in the phone check | M |
| S424 (done, item 84) | the 404 page cannot be checked locally (its assets point at the site path) and was never looked at | a check of the live 404 at both widths, and a local check that serves the site under its path | S |
| S425 (done as a check, item 84) | keyboard and screen-reader paths were checked by axe only | one manual pass: tab order on a question, the folds, the boxes, the run panel and the search | M |

**Round S6 — the code behind the site**

| # | Finding | Proposal | Size |
|---|---|---|---|
| S426 (done as parts, item 79) | `extra.css` is 3,970 lines written over many rounds; components are styled in several places (the question header at line 150 and again at 3090) | regroup it by component, drop rules that match nothing in the built site (a small script finds them), with the phone, jump and contrast checks proving nothing moved | L |

Suggested order: S1 (the most use for a reader preparing), S4, S3, S2, S5, S6. Every round
ends with the full check set and the owner's look at the live site.

## Technical notes for whoever continues this work

- SystemVerilog tests: Verilator must be newer than 5.052 (CI builds the commit in
  `VERILATOR_REF`; the same recipe is in `README.md`) and `z3` must be on the PATH. The
  5.052 release crashes on 0011 and mis-randomizes the 0014 subclass; the apt package
  (5.020) has no constraint support. `run_tests.py` refuses older versions.
- In a cloud sandbox without flex, `pip install verilator` (5.048, in a venv) runs most
  testbenches: wrap the binary so the C++ build gets `-CFLAGS -fcoroutines -CFLAGS
  -std=c++20`, and call `run_sv()` of `run_tests.py` directly (its version check asks for
  5.053+, and the classes with constraints need the CI's build). 0055 to 0062 pass this way.
- Build: `pip install -r requirements.txt && mkdocs build --strict`. Versions are pinned
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
  `python tools/check_phone.py site --offline --axe <copy>/package/axe.min.js ...`.
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
