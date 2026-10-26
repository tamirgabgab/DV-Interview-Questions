# HANDOFF

Living task list for this repository: what was done, what is in progress, and what comes
next. Update it at the end of every work session so anyone (human or AI) can pick up
where the last session stopped.

_Last updated: 2026-10-25 (session 26)_

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


## In progress

- **State (2026-10-26, session 26):** `main` is 682f406 (fix rounds 1 to 6a, question 0048, review rounds V1, V5, V7), deployed.
  47 questions (0022 was
  merged into 0016), every one with an explorer box. CI runs the lint, the contrast check,
  the tests (pytest and Verilator), the strict build, the link check, the phone check
  (axe findings and figure text under 9 px fail) and the explorer click-check.
- **Done in session 26:** 0044 became a coding question (work log item 48); fix rounds 1
  and 2, axe and small text (item 49); fix round 4, the documents (item 50); fix round 3, the CI actions (item 51); fix round 5,
  the cloud sandbox (item 52); question 0048, the farmer, the food and the water (item 54).
- **Review of session 26:** findings and rounds V1 to V7 under **Fourth series**; V1, V5 and V7 are
  done (work log item 55), V2, V3, V4 and V6 wait for the owner.
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
- **Next, the owner picks:** the rest of the second series A to E, the new questions of
  M to R and Z, the deferred G222, H223, H224 and E35, the three coding proposals of
  session 24 (meeting rooms, topological sort, single number II), the topic gaps under
  **Question variety**, or questions the owner sends.
- **Decision (owner, session 20): the repository stays public.** Options kept for later:
  a private "interview bank" beside the public site; two builds from one repository (the
  public one without the interviewer, trap and follow-up blocks, the full one behind a
  password on Cloudflare Pages or Netlify); or private with no Pages site (GitHub Pro is
  needed to publish Pages from a private repository, and the site would still be public).
  Visibility is changed under Settings, General, Danger Zone.

## Open items

### Owner decisions

- [ ] Keep example question `0001` or replace it with real content.
- [x] Staff level removed (session 19, owner's call). Senior has nine questions (0007, 0011, 0019, 0020, 0021, 0023, 0024, 0025, 0037).
- [ ] Pick the next topic gaps to fill from **Question variety** below.
- [ ] Pick the next rounds from **Proposals and rounds**: the open rows of the first series (E, F, I, L, N, O, the rest of Q, S), the rest of the second series A to E, the deferred G222, H223, H224, and the new questions of M to R and Z. Done: U to X (in the archive), I to L, the third series UI1 to UI5.
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
- [ ] Question ideas the owner has not picked yet (logic, math, digital design, EE): poisoned wine with 10 testers, 12 coins in 3 weighings, two eggs and 100 floors, Boyer-Moore majority, 100 doors, Gray code, XOR from NAND / universal MUX, two's complement overflow, divide-by-3 clock with 50% duty, maximal LFSR, Hamming (7,4), resistor cube, infinite resistor ladder.
- [ ] When a Verilator release newer than 5.052 is out, bump `VERILATOR_REF` to its tag and check that 0011 and the 0014 subclass still pass.

---

## Question variety

### Coverage today (47 questions)

| Level | Questions | Main topics covered |
|-------|-----------|---------------------|
| Student | 0001, 0002, 0003, 0010, 0012, 0015, 0032, 0036, 0040, 0048 | digital logic, bitwise, sorting, stack, digit puzzles (with number bases in 0012 part c), conditional probability, BFS over a tiny state space (wolf, goat and cabbage), LFSR periods and primitive polynomials, the shortest path by two reflections (the farmer, the food and the water) |
| Junior | 0004, 0005, 0006, 0008, 0009, 0013, 0014, 0016, 0017, 0018, 0026, 0027, 0028, 0029, 0030, 0031, 0033, 0034, 0035, 0038, 0039, 0041, 0042, 0043, 0044, 0045, 0046, 0047 | FIFO depth from rates, Gray pointers and CDC, a divide-by-3 clock, SVA for a handshake, logic puzzles, BFS (remainders, hourglass states), O(n) scans, permutations, SV constraints, Josephus (proof), cycle detection, motion and speed ratios, sequences and a single-peak proof (cake split), relative speed and counting with inclusion-exclusion (clock hands), geodesics on a box by unfolding (spider and fly), Dijkstra over a bitmask state with the greedy rule (bridge and torch), a price list per load and a range function (the camel and the water), selection from partial orders (horse races without a stopwatch), the Kaprekar step as code with a hash and a closed form for the digits (0044), the odd ball in fewest weighings (0045), the largest square, rectangle and right triangle of ones by dynamic programming and a stack (0046), trapping rain water by two pointers and a heap (0047) |
| Senior | 0007, 0011, 0019, 0020, 0021, 0023, 0024, 0025, 0037 | synchronizer MTBF, SV constraints, randomization, probability, combinatorics, Dijkstra on a state graph, PCIe completion rules, recursive enumeration, counting formula with proof, generalized Josephus (recurrences, induction), a PCIe endpoint reference model (classes, block memory, scheduling), a USB4 credit flow-control reference model (modulo counters, loss and resynchronization), a PCIe Ack/Nak reference model (Retry Buffer, Replay, error handling) |

Algorithms and puzzles are well covered; 0020 / 0021 / 0023 / 0024 / 0025 are the protocol questions (PCIe, USB4), with 0023, 0024 and 0025 reference models.
Round R (session 18) opened the DV-core shelf: FIFO depth, Gray pointers / CDC, a clock
divider, an LFSR, synchronizer MTBF and SVA; 0040 (a sequence detector FSM) and 0041
(coverage closure of random tests) followed. **Still missing:** UVM, covergroups,
debug ("find the bug") and verification planning.

### Topic gaps worth filling

| Topic | Example questions | Level |
|-------|-------------------|-------|
| FSM design | Sequence detector (Mealy vs. Moore) with a WaveDrom trace; a vending machine | student / junior |
| FIFO | Synchronous FIFO with full / empty, then "how deep must the FIFO be" for a given burst | junior |
| Clock domain crossing | Two-flop synchronizer and metastability; Gray-code pointers in an async FIFO | junior / senior |
| SVA | Write the assertion: req → ack within 1–3 cycles, one-hot, no grant without request | junior / senior |
| Functional coverage | Write a covergroup with crosses and illegal / ignore bins for an ALU or a packet | junior / senior |
| Constraints | Unique values without `unique`, a sorted array, a weighted `dist`, a constraint that fails on purpose | junior / senior |
| UVM | Phases, factory override, sequence / sequencer / driver handshake, a scoreboard for out-of-order responses | senior |
| Protocols | Valid / ready handshake (AXI-stream) checker, APB transfer, arbiter fairness | senior |
| Debug | "Find the bug" in a short RTL or testbench, or from a waveform | any |
| Computer architecture | Cache hit / miss trace, LRU replacement, pipeline hazards | junior / senior |
| Verification planning | Write a test plan for a FIFO / arbiter; what to measure for sign-off; regression strategy | staff |
| Behavioral | A bug that escaped to silicon: what happened and what you changed | staff |

### New question formats

| Format | Why | How on the site |
|--------|-----|-----------------|
| **Find the bug** | Very common in DV interviews and quick to practise | Code with a hidden bug, the fix in the solution; the test proves the fix |
| **Read the waveform** | Tests timing intuition | WaveDrom figure plus "what is the value of X at cycle 5?" |
| **Write the assertion / covergroup** | Core DV skills with no coverage yet | SV only; check with Verilator `--assert` where it is supported |
| **Mini-project** | Design + verify in one question (e.g. FIFO + scoreboard) | Several parts, each with its own collapsed solution |
| **Quick quiz** | Short knowledge questions (blocking vs. non-blocking, `logic` vs. `wire`) | A short multiple-choice block, many per page |

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
| Logo / favicon | A drawn SVG: digital waveform ending in an amber check mark (white on the navy header; navy rounded square for the favicon) |
| Question id | A small label above a clean title; the id stays in the side navigation and the tables |
| Footer | Site name + link to the repository, no personal name; the Material generator line is off |
| Table filters | Chip buttons, single choice per group (level, difficulty, topic), plus the text search |

### Proposals and rounds

Effort: **S** under an hour, **M** a few hours, **L** a day or more.

**Round A — identity and mobile** (done in session 4):

| # | Proposal | Effort |
|---|----------|--------|
| A1 | Logo and favicon | S |
| A2 | Own colour palette (navy + amber) in light and dark mode | S |
| A3 | Styled level / difficulty chips (CSS) instead of emoji, used in tables, question header and legends | S |
| A4 | Own footer | S |
| A6 | One question header card: id label, clean title, level and difficulty chips, topics, added date, "code in SV + Python / tested in CI" badges; hide the duplicate Material tag chips | S–M |
| A13 | Previous / next question links (`navigation.footer`) and "related questions" by shared tags | S |
| A15 | Question tables become cards on narrow screens | S–M |
| A16 | Chip filters instead of selects, with a result counter | S–M |

**Round B — clearer explanations** (done in session 4 except B14; see the work log):

| # | Proposal | Effort |
|---|----------|--------|
| B5 | Home page redesign: one-line intro, four level cards with counts, a statistics strip (questions, by difficulty, "all code is tested"), a "how to practise" box, then the full table | M |
| B7 | "Answer in short" line at the top of every solution | S per question |
| B8 | Fixed structure inside solutions: idea → steps → code → why it is correct → complexity; numbered steps with a vertical timeline line | M, applied gradually |
| B9 | Custom admonitions with own icons: "what the interviewer checks" (moved to the top of the solution area), "trap", "follow-up" | S–M |
| B10 | More readable code: a title per block, line numbers on long blocks, highlighted key lines, Material **code annotations** (numbered circles that open a Hebrew explanation next to the line) | S infra, M per question |
| B11 | Hint ladder: hint 1 light, hint 2 stronger, opened one after another | S |
| B12 | "Open all / close all solutions" buttons and a practice mode (solutions hidden, optional timer) | S / M |
| B14 | Step-through figures (next / previous) for the stack in 0010 and the cycles in 0009 | M |

**Round C — navigation, discovery, sharing** (later):

| # | Proposal | Effort |
|---|----------|--------|
| C17 | ~~Phone check in CI: screenshot every page at 390 px and fail on horizontal scroll~~ — done in session 6 | M |
| C18 | ~~Sortable table columns~~ — done in session 6 | S |
| C19 | ~~Topic pages / study paths (e.g. constraints: 0007 → 0014 → 0011) with a short intro each~~ — done in session 6 | M |
| C20 | ~~Random question button honouring the filters~~ — done in session 6 | S |
| C21 | ~~Better Hebrew search (prefix letters ו/ה/ב/ל/מ/ש as separators)~~ — done in session 6 | M |
| C22 | ~~Solved / favourite marks in the browser with a progress bar per level~~ — done in session 6 | M |
| C23 | ~~Social preview cards per question~~ | S–M — **done** in session 16 (G45) |
| C24 | ~~Comments per question via GitHub Discussions~~ | M — **done** in session 16 (G45), waits for the owner's ids |

**Rounds D to G — proposed 2026-10-18, after 0020 / 0021** (not started; the owner picks):

The two PCIe pages are the longest on the site (three parts, a proof, ten figures and
tables) and showed where the interface strains: long pages have no in-page navigation,
figures with 16 rows are unreadable at 390 px, and display math wider than the phone was
found by hand. The proposals are grouped so a round can be done in one session.

**Round D** — dropped by the owner in session 20 (2026-10-22). D25 and D26 had been done
as H51 and H50; D27 and D28 live on as L69 and L71; D29 (a share button beside the
existing heading anchors) and D30 (reading time, a `prerequisites:` line) were dropped.

**Round E — discovery and navigation**

| # | Proposal | Effort |
|---|----------|--------|
| ~~E31~~ | ~~**Question kind filter**: `kind:` front matter (puzzle / code / design / proof / knowledge) → a chip group in the tables and a badge in the header card (idea 7b)~~ done (session 22: puzzle / code / design / math / dv) | S–M |
| E32 | **Explicit `related:` links** in front matter that take precedence over tag overlap, a "PCIe" study path 0020 → 0021 with a topic intro, and topic pages for the largest tags (idea 22) | S–M |
| ~~E33~~ | ~~**Search results with context**: level / difficulty chips and a snippet per hit, and search by id ("0021")~~ done (session 22) | S–M |
| ~~E34~~ | ~~**Home page memory**: a "continue where you left off" card (last visited question from localStorage) and a "recently added" strip~~ done (session 22) | S |
| E35 | **Keyboard shortcuts** on desktop: n / p previous-next question, s open / close solutions, r random, ? help overlay | S |
| ~~E36~~ | ~~**"מה חדש" changelog page** generated from the `added` dates (and the git log), linked from the footer~~ done from the `added` dates only (session 22) | S |

**Round F — interactivity**

| # | Proposal | Effort |
|---|----------|--------|
| F37 | ~~**Parameter explorer for 0020 / 0021**~~ (done as M73, session 17): sliders for address, length, MPS and RCB; the page draws the splits map and shows the count live (a JS port of the recursion, with a test that compares it to the Python output on a grid of cases) | M |
| F38 | **Run panel presets**: a dropdown of example inputs per question, an "expected output" comparison, and a shareable link that carries the editor code | M |
| F39 | **Quick quiz blocks**: multiple-choice self-checks (`??? quiz`) with instant feedback, counted in the marks (the "quick quiz" format of Question variety) | M |
| F40 | **Side-by-side SystemVerilog / Python** on wide screens (a toggle next to the tabs) with matching line highlights | M |
| F41 | **"Open in EDA Playground"**: copy the SV code and open the site in one click (idea 7c) | S |

**Round G — infrastructure and quality**

| # | Proposal | Effort |
|---|----------|--------|
| G42 | ~~**`tools/new_question.py`**: scaffold the page, `tests/<id>/`, a figure-generator stub and the README catalog row from the template (idea 12b)~~ | S–M — **done** as J60 |
| G43 | ~~**Generators for the old figures** 0004–0007 in `tools/figures/` (idea 12a)~~ | S–M — **done** in session 16 |
| G44 | ~~**Accessibility pass**: focus rings, aria labels on the toolbar and steppers, contrast of the amber chips in dark mode, `prefers-reduced-motion`; an axe / Lighthouse check in CI~~ | M — **done** in session 16 (axe warns in CI) |
| G45 | ~~**Social preview cards** (C23) and **giscus comments** (C24)~~ | S–M / M — **done** in session 16 (comments wait for the owner's ids) |
| G46 | ~~**Scheduled workflow**: a weekly external-link check and a reminder when a Verilator release newer than the pinned commit is out~~ | S — **done** in session 16 |
| G47 | ~~**Display-math width in CI**: extend `check_phone.py` to report `mjx-container[display]` elements wider than the content box (the ten equations of 0021 were found with an ad-hoc script)~~ | S — **done** as K65 |

Suggested order by value for effort: D26 and D25 (done as H50 and H51; round D since dropped),
G47 (so the next proof page is caught by CI), F37 (the PCIe explorer), E31 and E32.

**Rounds H to K — proposed 2026-10-19, after 0026 to 0028** (K, H and J done in session 13 except H49; I open):

Session 12 added the first questions without code that lean on figures (0026 motion,
0027 / 0028 cake split) and the first interactive component (`cake-explorer.js`). What it
showed: charts with 11 to 13 bars and rows are small at 390 px, wide display math is still
found by eye, the page linter skips indented lines and everything inside the steps
timeline, and each new figure page repeats the same bar / stem / threshold code. Rounds D
to G above are still open; H to K add to them.

**Round H — interface, building on the explorer**

| # | Proposal | Effort |
|---|----------|--------|
| H48 | **One explorer component**: turn `cake-explorer.js` into a small declarative widget (sliders from `data-*`, charts from a shared JS module) and reuse it: α for 0026 (the position-time chart moves), N for 0016 / 0022, address / MPS / RCB for 0020 / 0021 (this is F37) | M — **done** |
| H49 | **Guess before you look**: in practice mode an input "your answer" above the solution (a number or a person), checked against an `answer:` front-matter field before the solution opens; counted in the marks | M — **deferred by the owner** |
| H50 | **Figure lightbox** (D26), now more pressing: the cake rows, the 13-bar charts and the 0015 grid need pinch-zoom on a phone | M — **done** |
| H51 | **Part navigation bar** (D25): every new page has two parts with long solutions | S–M — **done** |
| H52 | **Theme check**: run the phone check in dark mode too (all screenshots today are light), and flag SVG text whose colour is not a CSS variable | S — **done (warn only; dark mode on a manual run)** |
| H53 | **Chart hover values on touch**: tap a bar or dot to show its `<title>` as a small tooltip (phones have no hover) | S — **done** |

**Round I — new questions, by theme** (each line is one or two pages)

| # | Theme | Questions |
|---|-------|-----------|
| I54 | Motion and rates, after 0026 | bridge and torch (4 people, 17 minutes), the jeep / desert crossing, two trains and a fly, river boat up and down stream |
| I55 | Quant brainteasers, after 0027 / 0028 | optimal stopping (secretary problem, 1/e), gambler's ruin, coupon collector, broken stick into a triangle; each with an explorer |
| I56 | Owner's open list (Open items) | poisoned wine with 10 testers, 12 coins in 3 weighings, two eggs and 100 floors, 100 doors, Boyer–Moore majority |
| I57 | Digital design for DV | Gray code and async FIFO pointers, divide-by-3 clock with 50% duty, maximal LFSR, Hamming (7,4), XOR from NAND only; WaveDrom and Verilator tests |
| I58 | Core DV gaps | SVA req → ack in 1–3 cycles, a covergroup with crosses and illegal bins, FIFO depth for a burst, find-the-bug in a scoreboard, UVM sequence / driver handshake |
| ~~I59~~ | Dropped, the Staff level was removed (session 19). Was: staff level | a verification plan for an arbiter, sign-off metrics, regression strategy; a written "what would you check" format |

**Round J — adding questions faster**

| # | Proposal | Effort |
|---|----------|--------|
| J60 | **`tools/new_question.py`** (G42): page, tests folder with the figures-up-to-date test, generator stub, README row | S–M — **done** |
| J61 | **Shared chart helpers** `tools/figures/charts.py`: bars with a highlighted bar, stems against a threshold, ratio against y = 1, curve against a line; 0026–0028 and the older charts move onto it | M — **done for 0026–0028** |
| J62 | **Fill script in the repo**: the page template with `{{B0}}` placeholders and the generator blocks (used by hand in session 12) as `tools/figures/fill.py`, so a page and its figures are regenerated in one command | S — **done (gen markers + fill.py)** |
| J63 | **One test helper** for "figures and tables match the generator" (copied into every no-code test today) | S — **done** |

**Round K — safety net**

| # | Proposal | Effort |
|---|----------|--------|
| K64 | **Linter gaps**: check RTL on indented lines and inside `<div class="steps">` (paragraph starts only), and fail on a `\tag` inside a list item without `aligned` | S — **done** |
| K65 | **Display-math width in CI** (G47): every equation split by hand in sessions 8–12 would have been caught | S — **done (warn only)** |
| K66 | **Node in CI explicitly** (`actions/setup-node`), so the explorer tests can never be skipped silently | S — **done** |
| K67 | **Owner-file check list**: when a source file arrives, recompute its tables and formulas in a test first (done by hand for 0026–0028; it found the capped-last-person gap and one rounding) | S per question — **done (CLAUDE.md, README)** |

Suggested order: K64 + K65 + K66 (small, protect every next page), H51 + H50 (phone
reading), J60 + J62 (faster batches), then H48 and a content round from I.

**Rounds L to O — proposed 2026-10-19, after session 13** (not started; the owner picks):

Session 13 gave every page a lightbox, tooltips and a part bar, one explorer component and
authoring tools. The next gaps: practising (the site shows solutions but does not help to
remember them), explorers on the rest of the "numbers" pages, the older figures still
outside `fill.py`, and no visual or accessibility check in CI.

**Round L — practising and remembering**

| # | Proposal | Effort |
|---|----------|--------|
| L68 | **Review queue**: the "solved" mark keeps the date; the home page shows "to review" for questions solved more than 7 / 30 days ago (spaced repetition, localStorage only) | M |
| L69 | **Progressive reveal** in practice mode (D27): idea → steps → proof one block at a time, with "show more" | M |
| L70 | **Key-ideas page per study path**: the "answer in short" and "idea" blocks of each question on one page, for revision before an interview | S–M |
| L71 | **Print / PDF of a path** (D28, idea 19): all blocks open, figures kept, one question per page | M |
| L72 | **Guess before you look** (H49), kept for later: a typed answer checked against an `answer:` field | M |

**Round M — more explorers and figures**

| # | Proposal | Effort |
|---|----------|--------|
| M73 | ~~**PCIe split explorer** for 0020 / 0021 (F37): address, length, MPS, RCB → the splits map and the count~~ | M–L — **done** in session 17 |
| M74 | **Hourglass explorer** for 0018 / 0019: pick the two glasses and the target, the BFS / Dijkstra path shown step by step | M |
| M75 | **Probability explorer** for 0015: p, q and the number of children move the outcome grid and the answer | S–M |
| M76 | ~~**Stepper upgrades**: autoplay with a speed control, a deep link to a step (`#step-5`), swipe on phones~~ | S–M — **done** in session 17 (deep link and swipe; autoplay lives in the explorers) |
| M77 | ~~**"Interactive" badge** in the header card and a filter chip for pages with an explorer or a stepper~~ | S — **done** in session 17 |

**Round N — finding questions**

| # | Proposal | Effort |
|---|----------|--------|
| ~~N78~~ | done as E33: **Search by id and with context** (E33): "0027" finds the page; hits show level / difficulty chips | S–M |
| ~~N79~~ | done as E34: **Home page memory** (E34): "continue where you left off" and a "recently added" strip | S |
| ~~N80~~ | done as E36: **"מה חדש" page** (E36) generated from the `added` dates, linked from the footer | S |
| N81 | **Keyboard shortcuts** (E35): n / p, s, r, ? help | S |

**Round O — tooling and quality**

| # | Proposal | Effort |
|---|----------|--------|
| O82 | **All generators on `blocks()` + `fill.py`** (0008–0025), dropping the per-test regex comparisons; generators for 0004–0007 (G43) end the literal-colour warning | M |
| O83 | **Visual regression**: compare the CI phone screenshots with the last `main` run and list pages whose pixels changed | M |
| O84 | **Accessibility check** (G44): axe in the phone check, focus rings, labels on the toolbar, lightbox and sliders | M |
| O85 | **Browser tests of the reading tools** in `tests/tools/` (lightbox, part bar, tooltip, explorer sliders) with Playwright | S–M |
| O86 | **Weekly scheduled workflow** (G46): external links and a newer Verilator release | S |

Suggested order: O85 (protects what session 13 added), N78 + N79 (cheap and visible),
M75 or M74 (one more explorer), L68 + L70 (practising), then O82 before the next large
batch of figure pages.

**Rounds P to S — proposed 2026-10-20, after 0029 and 0030**

Session 14 added the first explorer with its own controls (the clock of 0029) and the
first embedded standalone tool (the owner's spider-and-fly page of 0030). What it showed:
a play button and a draggable figure explain motion better than a slider and a chart; a
tool sent as a file can be embedded as is, but it does not follow the site's theme or
language; the recent questions are all puzzles, and the senior / staff and DV-core shelves
have not grown since 0025. Rounds D to G, I and L to O above stay open; P to S add to
them, and P and R answer the owner's request for clearer graphics on specific questions
and for new questions.

**Round P — graphical explorers for specific questions**

| # | Proposal | Effort |
|---|----------|--------|
| P87 | ~~**Strip explorer for 0030, in the site's style**: drag S on the wall x = 0 and F on x = a (two small wall panels), the periodic strip redraws with the eight images, the 48 lines faint, the valid ones solid and the shortest in orange; the exit point and the distance in the summary. Hebrew, follows light / dark. The owner's tool stays as the full 3D view~~ **Done** in session 15 | M |
| P88 | ~~**Motorcycle animation for 0026**: a play button moves the three travellers along the road figure while the position-time chart draws itself; a scrubber for the time, the phase boundaries marked (the clock explorer's play loop reused)~~ **Done** in session 15 | M |
| P89 | ~~**Cake cutting animation for 0027 / 0028**: the rows appear one person at a time with the slice highlighted, the bar chart grows with them; a toggle "arithmetic / geometric" on one page to compare the two laws with the same a~~ **Done** in session 15 | S–M |
| P90 | ~~**Josephus circle animation for 0016 / 0022**: people leave the circle one by one at a chosen speed, the survivor highlighted, the binary of N shown rotating for L = 2; the survivor chart stays~~ **Done** in session 15 (without the rotating binary) | M |
| P91 | ~~**Clock explorer additions for 0029**: a timeline strip under the day slider with a tick at every meeting (dense bands show where the pairs cluster), a pair filter, and a "next triple" jump~~ **Done** in session 15 | S–M |
| P92 | ~~**Hourglass explorer for 0018 / 0019** (M74) and **probability explorer for 0015** (M75), both still open; the PCIe split explorer (M73) after them~~ **Done** in session 15 (hourglass and probability; M73 still open) | M each |

**Round Q — new questions, puzzles in the style of 0026–0030**

| # | Proposal | Effort |
|---|----------|--------|
| Q93 | **Ant on a can** (geodesics again): the shortest path on a cylinder from a point outside to a drop inside the rim, by unrolling the side and reflecting in the rim; junior / medium, no code, an unrolled-strip figure like 0030 | M |
| Q94 | ~~**Bridge and torch**: four people, 1 / 2 / 5 / 10 minutes, two at a time, one torch; 17 minutes and why 19 is the trap; part b a BFS over states in SV + Python with a stepper of the crossings; junior / medium~~ **Done** in session 15 as 0031 (Dijkstra, not BFS: the crossings are weighted) | M |
| Q95 | **Two trains and the fly**: the fly's total distance by the easy way and by the geometric series; student / easy, an animation of the fly bouncing (play button) | S–M |
| Q96 | ~~**Wolf, goat and cabbage**: BFS over the eight bank states with the forbidden ones struck out; student / easy; a stepper and code~~ **Done** in session 15 as 0032 | S–M |
| Q97 | **Clock angles** (0029 follow-ups made a question): when are the minute and hour hands opposite, at right angles, mirror images; student / easy; the clock explorer reused with a target angle | S |
| Q98 | **Heron's shortest path** (reflection in a wall): the path from A to B that touches a line; student / easy, prepares 0030 and Q93 | S |
| Q99 | **Rope around the Earth**: add one metre to the rope, how high does it lift; student / easy, mental arithmetic and a figure not to scale | S |

**Round R — new questions, DV core (the shelves that did not grow)**

| # | Proposal | Effort |
|---|----------|--------|
| R100 | ~~**Synchroniser MTBF**: two flops, τ, T0, the clock and data rates; compute the MTBF and how a third flop changes it; senior / medium; a small calculator explorer (sliders for the rates) and the formula in SV + Python~~ | M — **done** in session 18 as 0037 |
| R101 | ~~**FIFO depth from rates and bursts**: write and read rates, a burst length, back-pressure; the depth formula and a simulation of the fill level; junior / medium; an explorer that plots the fill level over time for the chosen rates~~ | M — **done** in session 18 as 0033 |
| R102 | ~~**Gray code pointers for an async FIFO**: why one bit changes, the conversion both ways, the full / empty test with the two top bits; junior / medium; SV + Python and a WaveDrom of the pointer crossing~~ | M — **done** in session 18 as 0034 |
| R103 | ~~**Divide-by-3 clock with 50% duty**: the design with a negative-edge flop, a WaveDrom timing diagram, and the testbench that checks the duty; junior / medium~~ | S–M — **done** in session 18 as 0035 |
| R104 | ~~**Maximal LFSR**: period of a 4-bit LFSR for two tap sets, why one is 15 and the other shorter; the sequence table from code; student / easy~~ | S — **done** in session 18 as 0036 |
| ~~R105~~ | Dropped with the Staff level (session 19). Was: **staff level, first question**: reviewing a verification plan (a given feature list with holes: missing negative tests, no coverage goals, no reset / power scenarios); a rubric-style answer with no code; staff / medium | M |
| R106 | ~~**SVA for a handshake**: req must hold until ack, ack within N cycles, no ack without req; the assertions, a WaveDrom with a passing and a failing trace; junior / medium; Verilator checks the assertions~~ | M — **done** in session 18 as 0038 |

**Round S — clearer question pages**

| # | Proposal | Effort |
|---|----------|--------|
| S107 | **Answer-at-a-glance card**: the first screen of every solution shows the final result, the one-line idea and a thumbnail of the key figure (the 40 net, the clock, the strategies bars), before the steps | S–M |
| S108 | **Steps linked to figures**: a step in the timeline highlights its element in the figure on hover or tap (the triangle legs in step 3 of 0030, a phase in 0026, a band in 0029), with `data-step` attributes written by the generators | M |
| S109 | **"Naive vs best" compare card**: the two routes, strategies or indices side by side with their numbers (0026 strategies, 0030 42 vs 40, 0027 person 3 vs 4), two columns on desktop and stacked on a phone | S |
| S110 | **Embedded tools follow the site**: the iframe of 0030 gets `?theme=` and `?lang=` from the page; needs a few lines in the owner's file (the owner decides), otherwise a note on the page that the tool is English and dark by default | S |
| S111 | **Numbered figure captions** ("איור 3") with the caption as the lightbox title, and cross-references from the text; the generators emit the caption | S–M |
| S112 | **Full-screen explorer on phones**: an explorer box opens in the lightbox overlay with its charts at full width (the strip and the clock are cramped at 390 px) | M |

Suggested order: P87 + S109 (0030 gets its own figure explorer and the 42-vs-40 card),
R101 + R102 (two DV-core questions that share the FIFO theme and a path), Q94 (the bridge,
with code), then P88 and S108, and R105 to open the staff shelf.

**Round T — explorers for the existing questions, proposed 2026-10-21** (the owner picks)

A survey of the pages that have no interactive component yet (the clock, strip, cake,
motorcycle, Josephus, hourglass, probability, bridge and river explorers exist). Each
proposal names the one thing the reader should be able to *do* that the static figures
cannot show; the pattern (play loop, stepper, drag, "generate") is the one already in
`explorer.js`. Effort as above.

| # | Page | Explorer | Effort |
|---|------|----------|--------|
| ~~T113~~ | Done in session 19. Was: 0009 boxes and cycles | **Permutation lab**: N boxes (sliders 4..16), "shuffle" draws the permutation as arrows and colours its cycles; a stepper follows one prisoner box by box; "1,000 rounds" runs the strategy against random choice and shows the success rates side by side (≈ 31% against 1 / 2^N) | M |
| ~~T114~~ | Done in session 19. Was: 0010 valid parentheses | **Stack animation**: type a string, the stack pushes and pops character by character, the depth chart draws itself, the first mismatch is circled; presets for the page examples and the traps (`([)]`, lone `)`) | S–M |
| ~~T115~~ | Done in session 19. Was: 0017 duplicate number | **Tortoise and hare**: the array as nodes i → a[i] (type or shuffle an array), the two runners move at their speeds, the meeting and the second phase to the entry of the cycle (the duplicate); a second tab plays the binary-search-on-values method with the count per step | M |
| ~~T116~~ | Done in session 19. Was: 0014 random shapes | **Generate**: a button draws N random squares or rectangles on the grid with the constraints of the page (a JS port of the rejection sampling), rejected attempts flashed in red; a heat map of where shapes land after 500 draws shows the bias the question asks about | M |
| ~~T117~~ | Done in session 19. Was: 0011 tic-tac-toe | **Board builder**: tap cells to place X / O, the page's rules decide live whether the board is a legal final board and say why not (counts, two winners, play after a win); "random legal board" and the wrap-around variant of part b as a toggle | M |
| ~~T118~~ | Done in session 19 (see the log). Was: 0007 triangle and centre | **Throw three points**: a button (or drag the points) on the unit circle, the arcs coloured, inside / outside decided; "1,000 throws" fills a running counter that converges to 1/4; an M slider for the discrete version with the formula beside it | S–M |
| ~~T119~~ | Done in session 19. Was: 0005 smallest 0/1 multiple | **BFS on remainders**: x up to ~30, the x remainders as a ring, the queue and the visited set grow step by step, the path back to 0 spelled out as the answer; a step counter next to the enumeration count for the same x | M |
| ~~T120~~ | Done in session 19. Was: 0012, 0013 Kaprekar | **Iterate**: type a number, sort-subtract step by step until 495 / 6174, the chain drawn; a histogram of the number of steps over all numbers (the page's part b) with the typed number highlighted | S–M |
| ~~T121~~ | Done in session 19. Was: 0008 Eurovision | **Announcement slider**: the cups chart with a slider "countries announced so far"; the room left for Israel against the points left, the moment of certain loss marked; a "what if" box to change Israel's jury score and watch the moment move | S–M |
| ~~T122~~ | Done in session 19. Was: 0004 three boxes | **Sample a ball**: tap a box to draw one ball (the hidden contents are random each time), the deduction appears line by line; "try the wrong box first" shows why one draw from "red" or "black" is not enough | S |
| ~~T123~~ | Done in session 20. Was: 0001 edge detector | **Waveform lab**: click the input per cycle, the output and the flop values appear on a live WaveDrom-like strip with the two-flop diagram beside it; a toggle for the one-cycle-late variant of the follow-ups | S–M |
| ~~T124~~ | Done in session 20. Was: 0002, 0003 swaps and loops | **Code tracer**: a step button runs the page's loop with a variable table and the current line highlighted (the swap variants, the double loop); one component reused by every short-code question | M |
| ~~T125~~ | Done in session 20. Was: 0024 USB4 credits | **Credit flow**: sliders for the buffer size and the packet rate, the two modulo-256 counters and the credits in flight animated, a "lose a packet" button and the resynchronisation that follows, as in the page's step figures | M–L |
| ~~T126~~ | Done in session 20. Was: 0025 PCIe Ack/Nak | **Sequence timeline**: send TLPs, press Ack / Nak at the receiver, watch the Retry Buffer fill and empty, a Replay after a Nak or a timeout; the page's error cases as presets | M–L |
| ~~T127~~ | Done in session 20. Was: 0023 PCIe endpoint | **Request builder** on top of M73: address, length, MPS, RCB → the completions the model returns and the memory reads it performs, reusing the split explorer | L (after M73) |
| ~~T128~~ | Done in session 20: 0036 LFSR | **Tap lab**: tick the taps, step or play on a ring of the 15 states, the output bits, the table of the eight polynomials | S–M |
| ~~T129~~ | Done in session 20: 0035 divide by 3 | **Half-cycle stepper**: cnt, a, b and clk_out edge by edge, the overlap shaded, the duty measured; a wake-up in state 3 in three counter variants | S–M |
| ~~T130~~ | Done in session 20: 0034 Gray pointers | **Sampled step and flags**: every changing bit arrived or not (binary against Gray); a 16-entry FIFO with 5-bit pointers and the full / empty rules | M |
| ~~T131~~ | Done in session 20. Was: 0006 stock | **Scan lab**: an editable price chart (drag or random), the scan animated with the running minimum and the best trade so far, a long / short toggle for part b | M |
| ~~T132~~ | Done in session 20. Was: 0038 handshake | **Rule checker**: draw req and ack on a timing strip (the `waveStrip` helper), the four rules evaluated every cycle, a violation marked with its rule, the three violations of the page as presets | M |

Suggested order: T114, T118, T122 (small, each page gets its "try it" box in an hour),
then T113 and T115 (the two algorithm animations that readers ask about most), T121 and
T120, and the protocol trio T125 to T127 after M73. Session 19 did T118, T113, T115, T119
and T114, then T117, T116, T120, T121 and T122. Session 20 did T123, T128 to T132, T125 to T127 and T124. Round T is closed.

The finished rounds U to X and the explorer survey of session 20 are in
[`HANDOFF-archive.md`](HANDOFF-archive.md).

### Second series, rounds A to E — presenting the answers (proposed 2026-10-22, owner picks)

The owner asked for new proposals on how answers are shown: clear, good-looking pages
with visual explanations. The rounds restart at A; item numbers continue the global
count (181 on), so they do not collide with the first series' A1 to D30.

What the pages look like today (screenshots of 0020 at 1280 and 390 px, light): a long
single column; each solution is a stack of blocks (short answer, idea, steps, code,
proof, cost) that the reader scrolls through; figures are generated SVG with a separate
legend under them, and on a phone the address-axis figures shrink until their labels are
about 6 px high while the legend wraps to four or five lines; the table of contents lists
only the top sections; the 34 explorer boxes each have their own control layout.

What the short research found (sources in the chat summary of 2026-10-22):

- Interactive diagrams should add to the text, never replace it: the reader learns without
  touching anything, and a box is not dropped on the reader as a sandbox without guidance
  (Red Blob Games). Diagrams work best interlinked with the text and annotations (UW
  CSE442). Animation must reveal something, interactions must be discoverable, and a
  reduced-motion path must exist.
- Discrete states read better in an explicit stepper than in scroll-driven animation
  (known length, direct access, replay, comparison); scrollytelling needs a stacked or
  stepped fallback on phones (Kosara, "The scrollytelling scourge"; The Pudding's
  responsive scrollytelling guide).
- Program visualisation that steps forwards and backwards through real execution, with
  the state beside the code, is the best-studied form for code answers (Python Tutor,
  Guo, SIGCSE 2013). Diagrams should focus on the part of the code that matters for the
  task (MIT thesis on code-comprehension diagrams).
- Interview-prep products stage the answer: hints, then complexity, then patterns, then
  code, each behind a toggle, and give every approach its complexity (AlgoExpert,
  StreamPrep, AlgoMaster's animated visualisations).
- Material for MkDocs is in maintenance mode (no new features since 9.7, end of life
  announced for November 2026; the team moved to Zensical, which reads `mkdocs.yml`).
  New interface work should therefore live in our own CSS / JS, not wait for theme
  features; a move to Zensical is a separate decision for the owner.

**Round A — the answer at a glance**

| Id | Idea | Size |
|---|---|---|
| ~~A181~~ | ~~**Solution map**: a strip at the top of every solution with its blocks (idea → steps → code → proof → cost), one line each, clickable; the block in view is marked while scrolling~~ done (session 22, round 1 of the owner's interface plan) | S–M |
| A182 | **Answer hero card**: the short answer with its key result set large (a number, a formula, a verdict), a thumbnail of the main figure beside it, and the hint ladder folded into a progress line above it | M |
| ~~A183~~ | ~~**Cost as chips and a comparison**: time / space (and flops, gates, latency on design pages) as chips in the solution header; on pages with several approaches a small table or bar chart comparing them~~ done as chips only (session 22; the comparison part dropped with the owner's no-naive-comparison rule) | S–M |
| A184 | **Approaches side by side**: where a page has a naive and a good solution, a two-column compare view (or tabs with a "what changed" note) instead of two blocks far apart | M |

**Round B — code and figure linked**

| Id | Idea | Size |
|---|---|---|
| B185 | **Linked highlighting**: tapping a code line, or one of its annotation markers, highlights the figure element it builds, and the other way round (ids emitted by the figure generators, a shared `data-link`) | M |
| B186 | **Step-through of the page code beside its state** (the Python Tutor pattern) for the algorithm pages that have a trace-like box: the current line lit, the variables and data structures beside it, forward and back; generalises the 0002 / 0003 trace view to 0005, 0010, 0017 | M–L |
| B187 | **Proofs as steppers**: each step of a proof block highlights the part of the figure it talks about, with the step text under it (the figure steppers of M76 applied to proofs) | M |
| B188 | **Code and waveform side by side** on the DV pages: on a wide screen the SystemVerilog tab and its WaveDrom diagram in two columns, the waveform sticky while the code scrolls | S–M |

**Round C — the reading surface**

| Id | Idea | Size |
|---|---|---|
| C189 | **Sticky figure column on wide screens**: in long solutions the current figure stays beside the text while it scrolls (a stepper, not scroll-driven animation); one column with the figures inline on phones | M |
| C190 | **Typography pass for Hebrew**: a Hebrew face with good digits (e.g. Assistant or Heebo), tabular numbers in tables, a line-length cap, more line height, styled LTR runs | S–M |
| ~~C191~~ | ~~**One visual identity per block**: idea / steps / code / proof / cost / trap each with an icon, an accent colour and a side rail, the same in light and dark~~ done (session 22) | S |
| ~~C192~~ | ~~**Tables that read**: sticky header, numbers aligned, the row the text refers to highlighted, and on phones long tables as cards~~ done without the row highlight (session 22) | S–M |
| C193 | **Direct labels instead of separate legends** in the generated figures where there is room, and a colour-blind-safe palette checked by a script over every `--viz-*` pair | M |

**Round D — figures made for the phone**

| Id | Idea | Size |
|---|---|---|
| ~~D194~~ | ~~**Compact figure variants**: generators emit a narrow layout for phones (fewer ticks, larger text, stacked rows) shown under 480 px; today's address-axis figures fall to ~6 px labels~~ done as a phone layer in `reading-tools.js` (session 22, the owner's pick over a second SVG per figure) | M–L |
| ~~D195~~ | ~~**Minimum text size check**: `check_phone.py` measures rendered SVG text at 390 px and warns below 9 px~~ done (session 22; 160 figures on 36 pages warned, the input of D194) | S |
| D196 | **Controls in a bottom sheet** on phones for the explorer boxes: the figure stays in view while the controls sit at the bottom of the screen | M |
| ~~D197~~ | ~~**Legend as chips** under a figure on phones (one row that scrolls) instead of a list of five lines~~ done as wrapping chips (session 22, the owner's pick) | S |

**Round E — motion and consistency in the boxes**

| Id | Idea | Size |
|---|---|---|
| E198 | **Purposeful transitions**: values and cells move between states (tweened bus values, sliding queue chips, growing arcs), off under `prefers-reduced-motion` | M |
| ~~E199~~ | ~~**The answer lights up**: when a box reaches its result, the element that is the answer (the duplicate, the survivor, the maximal polynomial) is outlined and named in one line~~ done in 11 kinds (session 22) | S–M |
| ~~E200~~ | ~~**One layout for all 34 boxes**: control groups in a fixed order (input, playback, output), a status line at the bottom, the same spacing and button sizes, documented once~~ done as a shared layer in `core.js` (session 22) | M |
| ~~E201~~ | ~~**A first-visit guide** on one box per page: three dismissible hints pointing at the main control, the figure and the summary, remembered per browser~~ done (session 23, part 6: once per browser, on the page's first box) | S–M |

Suggested order: A181 and C191 (small, visible on every page), D195 then D194 (the phone
figures are the weakest point today), B185 (the largest gain in understanding), then A182
and A183.

### Second series, rounds F to H — the explorer boxes (proposed 2026-10-23, owner picks)

The owner asked for proposals to improve the explorer boxes. A read of `explorer.js`
(41 views, 8,114 lines) on 2026-10-23 found:

- `explorer.js` is 631 KB unminified and is listed in `extra_javascript`, so every page
  loads and parses it, the home page and the catalogs included; every box on a page is
  built at `DOMContentLoaded`, also the ones far below the fold.
- No test clicks the boxes: the Node tests compare each model's math with the Python
  reference, and `check_phone.py` loads every page (axe, `pageerror`, width) without
  pressing a control. The 8,000 lines of view code have no interaction test.
- The copy link carries the box state (`seedControls` with `opts.state`) in 5 boxes
  (boxes, floyd, stock, acknak, credits); the other seeded boxes (eggs, seqdet, coverage,
  horses, kapbase, kap4base, triangle, polygon, trace, endpoint and more) carry only the
  seed, and the boxes driven by typed fields (cake, motorcycle, josephus, clock,
  hourglass, bridge, pcie, fifo, mtbf, bfs01, abmap, camel, brackets, lfsr, div3) have no
  link at all.
- No box remembers its state when the reader comes back (no `localStorage`); nothing
  downloads a figure or a table (U133 covers the WaveDrom strips only).
- A speed select exists on every play except the 0014 shapes flash (350 ms), so no
  speed item is needed.

Item numbers continue the global count; rounds F to H here are the second series and do
not collide with the first series' F to H (items 37 to 53).

**Round F — safety net and load time**

| Id | Idea | Size |
|---|---|---|
| ~~F218~~ | ~~**Click-through test of every box**: a Playwright run over the built site that, in every box, presses each button, plays to the end, uses "reset everything", copies a link and reopens it; it fails on a JS error, a console error or a page wider than 390 px. Runs in CI next to `check_phone.py` (offline routes as there)~~ done (session 21) | M |
| ~~F219~~ | ~~**Split and lazy-load `explorer.js`**: a small shared core (seed, strip, controls, header, keyboard) and one file per kind, loaded only on a page that has that kind; each box is built when it nears the viewport (IntersectionObserver); minified at build time. The Node tests keep requiring the same model exports~~ done (session 21) | M–L |

**Round G — the same behaviour in every box**

| Id | Idea | Size |
|---|---|---|
| ~~G220~~ | ~~**State in the copy link for every box**: a generic serializer of the box's inputs, selects and toggles (plus the step index where a box steps), written to `#state-<kind>.<payload>`; the 5 hand-written states stay, every other box gets a link without its own code~~ done (session 21) | M |
| ~~G221~~ | ~~**The box remembers where the reader stopped**: the same payload saved per page and box in `localStorage` (wrapped in try / catch), restored on load, cleared by "reset everything"; a URL state wins over the saved one~~ done (session 21) | S |
| ~~G222~~ | ~~**Download the figure and the table**: a button per box that saves the current SVG (and a PNG) and the box's table as CSV, next to the WaveDrom row of U133~~ deferred by the owner (session 21) | S |

Pairs with E200 (one layout for all boxes): both touch every view, so they are best done
in the same pass.

**Round H — practice inside the boxes**

| Id | Idea | Size |
|---|---|---|
| ~~H223~~ | ~~**"Guess before the step"**: an optional practice mode in the stepping boxes that asks for the next state or the result before showing it (who survives in Josephus, how many drops for the eggs, the next state of seqdet, the next chain value in kaprekar) and counts the hits. Not H49 / L72 (a typed answer checked before the solution opens, deferred by the owner): this one lives inside the box and checks a step~~ deferred by the owner (session 21) | M |
| ~~H224~~ | ~~**"Open in the box" from the text**: a small button on a table row or a worked example that sets the box to those values and scrolls to it (a row of the k / n table of 0039, the base-7 example of 0012, the scripts of 0025); the page text and the box linked, as the second-series research recommends~~ deferred by the owner (session 21) | S–M |

Pairs with E199 (the answer lights up) and E201 (a first-visit guide).

Suggested order: F218 first (a safety net before changes that touch every box), then F219
with G220 (both reshape the shared code), G221 and G222 with E200, then round H with E199.
D196 (controls in a bottom sheet on phones) and B186 (the page code stepped beside its
state) stay open in their rounds.

### Second series, rounds I to L — boxes that show the solution (proposed 2026-10-23, revised, owner picks)

A review of every page (session 21, three read-only passes over the pages and the kind
files) asked of each box whether it shows the solution the page gives (its idea, the steps
of the algorithm, the invariant or the proof) and which parts have no visual at all. Every
page has a box, but 13 pages have a part (beyond the statement) with no visual, more have
parts with static figures only, and most boxes show the answer rather than why it holds.

The owner's direction (session 21): illustrate the solutions on the pages; no comparisons
with a naive solution and no "trap failing on screen" views. This version replaces the
first one (I225 to L262): the trap round and the naive comparisons were dropped, the trap
toggles were removed from the items that stayed, and round K now shows the mechanism of the
solution inside the existing boxes. Parameter knobs stay out (the owner turned them down
in round W). Item numbers continue the global count, so these rounds do not collide with
the first series' rounds of the same letters.

**Round I — a visual in the parts that have none (puzzles and algorithms)**

| Id | Page | Idea | Size |
|---|---|---|---|
| ~~I284~~ | 0002 parts a, b | Done in session 22. **Each part with its own swap**: the existing `trace` box placed in part a (the temporary variable) and in part b (the sum and the XOR), each preset to its part's version, the values and the a0 / b0 expressions line by line | S |
| ~~I285~~ | 0004 part b | Done in session 22. **The labels fix**: a `boxes3` mode with the labels array, k, same and other marked, and the two swaps drawn as a 3-cycle | M |
| ~~I286~~ | 0006 part a | Done in session 22. **The scan in part a**: the `stock` box placed in part a in long-only mode, so the minimum so far and the best long sit beside the part that explains them | S |
| ~~I287~~ | 0005 bonus | Done in session 22. **Pigeonhole on the repunits**: R1 … R(x+1) dropped into x remainder slots, the first collision lit, and R_i − R_j = 1…10…0 shown as the multiple | M |
| ~~I288~~ | 0007 part c | Done in session 22. **Three half-circles**: for a drawn triangle, the half-circle that starts at each point; at most one holds the other two; seeded draws count A1, A2, A3 apart (about 1/4 each, never two at once) | M |
| ~~I289~~ | 0011 part b | Done in session 22. **Any five cells hold a line**: pick cells on the wrap-around board; the 2-2-1 split per direction and the pair count are shown, and the fifth cell always completes a line | M |
| ~~I290~~ | 0012 part b | Done in session 22. **The map of the proof**: `kapbase` with base 10 placed in part b: the map k → max(10 − k, k − 1) and the fixed point at 5 | S |
| ~~I291~~ | 0013 part b | Done in session 22. **The 55 pairs, clickable**: a cell of the (p, q) grid shows its digits, the case of the analysis that applies and the arrow to the next pair; only 6174 points to itself | S–M |
| ~~I292~~ | 0017 solution 3 | Done in session 22. **Binary search on values**: the histogram of 1..n with the count of values ≤ mid against y = mid, lo and hi narrowing with the invariant in colour, on the same array as the Floyd box | M |

**Round J — a visual in the parts that have none (DV, math and probability)**

| Id | Page | Idea | Size |
|---|---|---|---|
| ~~J293~~ | 0033 part a | Done in session 22. **Written and read staircases**: the two cumulative step curves; the gap between them is the fill, and it peaks at the last write of the burst | S–M |
| ~~J294~~ | 0034 part b | Done in session 22. **The conversions stepped**: binary, the shifted row, XOR gives Gray; back by a prefix XOR from the MSB one bit per step; a counter walk marks the one changing bit, the 15 → 0 wrap included | S |
| ~~J295~~ | 0037 part a | Done in session 22. **Metastability by Monte Carlo**: data edges on a clock timeline, those in the T0 window settle after an exponential time; the histogram with the t_res cut, and a second flop moving the cut by Tclk, so the two factors of the formula are seen | M |
| ~~J296~~ | 0038 part a | Done in session 22. **Attempt lanes**: one lane per property of the page, where the antecedent matched, the window as a bracket, and pass / fail / vacuous | M |
| ~~J297~~ | 0041 part a | Done in session 22. **The stage ribbon**: equal bins played test by test, a bar per stage i → i + 1 with the measured wait against n / (n − i), the sum that makes n·H_n | S–M |
| ~~J298~~ | 0029 part b | Done in session 22. **The gap line**: the unwrapped angle difference of a chosen pair against time with the integers as lines, each crossing a meeting; the interval ends switched between closed, open and half-open with the page's three counts | S |
| ~~J299~~ | 0021 part b | Done in session 22. **The recurrence ladder**: C(0..N) as a row; a click on C(n) lights the m terms it sums and the block strip shows "the first completion takes i blocks" for each term | M |
| ~~J300~~ | 0015 part b | Done in session 22. **The Tuesday grid**: the 14 × 14 grid of (child, weekday) pairs, the cross of the 27 families with a boy born on Tuesday lit, the shared cell counted once, and the 13 with two boys | S–M |

**Round K — the mechanism of the solution, inside the existing boxes**

| Id | Page | Idea | Size |
|---|---|---|---|
| ~~K301~~ | 0039 | Done in session 22. **The recurrence on the building**: at every drop the band below is marked f(k − 1, t − 1), the drop floor 1 and the band above f(k, t − 1), with the matching cell of the table lit | M |
| ~~K302~~ | 0040 | Done in session 22. **How the automaton is built**: the pattern slides under itself to show each state's fall-back (the longest suffix that is a prefix) and the edge it gives, state by state | M |
| ~~K303~~ | 0042 | Done in session 22. **The price list on the road**: every stretch of road shows how many times the camel crosses it (5 / 3 / 1) as the passes play, so the litres per km of the solution appear on the road | S |
| ~~K304~~ | 0020 | Done in session 22. **Splits are sets of boundaries**: click the RCB boundaries inside the request to cut or not; the split forms live, a gap above MPS is marked, and the count is the number of allowed subsets | S |
| ~~K305~~ | 0014 | Done in session 22. **The projections**: two rectangles to drag, their projections on both axes and the page's four conditions turning true or false; in the main box a rejected candidate shades the shape and the projection that rejected it | M |
| ~~K306~~ | 0031 | Done in session 22. **The greedy rule, round by round**: the two costs of moving the current slowest pair (escort by the fastest, or the two fastest shuttle) side by side, the cheaper one taken and the pair removed, ending at the plan's total | M |
| ~~K307~~ | 0019 part a | Done in session 22. **The run that branches**: at t = 11 the timeline forks into "flip A" and "do not flip", the end times of each branch coloured, so the reader sees why 14 and 15 never share a run, with the 7k and 11k ticks | S |
| ~~K308~~ | 0013 part b | Done in session 22. **Subtraction by columns**: the sorted digits of the typed number subtracted column by column with the borrows lit, as in the page's table | M |

**Round L — the proof step, visible**

| Id | Page | Idea | Size |
|---|---|---|---|
| ~~L309~~ | 0016 | Done in session 22. **Renumbering**: after each step every remaining person shows the old and the new label (new = old − L mod N), the survivor the same person under both, so F(N − 1) visibly becomes F(N); a "full round" button shrinks the circle by L | M |
| ~~L310~~ | 0009 | Done in session 22. **Choose your cut**: tap any box of the long cycle to swap with c0; the two pieces h and L − h are shown, and only the middle range keeps both at 8 or less | M |
| ~~L311~~ | 0026 | Done in session 22. **The drop point**: drag D; the passenger's and the walker's arrival times and the curve of T = max of both against D, its minimum where the two are equal (7/8) | S |
| ~~L312~~ | 0027, 0028 | Done in session 22. **The live proof panel**: the f(p) = p²/(1 − p) curve (0027) or the q(1 − p) line (0028) with the people's p_k as dots and the threshold that moves with the slider; the single crossing is the peak | S |
| ~~L313~~ | 0036 | Done in session 22. **All cycles**: every state's arrow, so the ring shows its cycles (6 + 6 + 3 and the 0 loop for x⁴ + x² + 1, one cycle of 15 for a primitive polynomial) | S–M |
| ~~L314~~ | 0018, 0019 | Done in session 22. **The search itself**: one panel for both pages that steps through the queue (BFS in 0018, Dijkstra ordered by t in 0019), each state's four children marked new, seen or past D, until the goal is popped | M |
| ~~L315~~ | 0008 | Done in session 22. **Pouring the points**: the points left fill the cups to the brim with nobody above Israel; after France 17 points spill over, which is the page's moment of certain loss | M |
| ~~L316~~ | 0032 | Done in session 22. **BFS layers**: the state graph filled layer by layer (visited, frontier, parent arrows) until 1111 at depth 7 by the two mirror paths | S |
| ~~L317~~ | 0043 | Done in session 22. **The chain behind a verdict**: clicking a horse lights the race results that prove its known-faster set | S |
| ~~L318~~ | 0004, 0011 | Done in session 22. **Help lines that match the buttons**: `boxes3` names "סידור אחר", `ttt` names "הגרלה" and "הבורר", buttons that no longer exist | S |

Suggested order (session 21): L first (the proofs are where a box teaches most, and L312,
L311, L313 and L316 are small), then K (inside boxes that already exist, so the pages do
not grow), then I and J. Within a round, the small items first in one batch. Shared work:
L314 is one panel for two pages, L312 one panel for two pages.

### Second series, rounds M to R — new questions (proposed 2026-10-23, owner picks)

Ideas not already listed (Z202 to Z217, Q93 to Q99, I54 to I58, the open items and the
topic gaps are not repeated); 0015, 0009 and 0041 are the nearest existing pages, and each
idea here asks something they do not. Each is rewritten in our words with an original solution, a
generalisation and an explorer; the `source` field names a classic when there is one.

**Round M — logic with an invariant**

| Id | Question | Level | Generalisation | Explorer | Size |
|---|---|---|---|---|---|
| M263 | **Hats in a line**: 100 prisoners in a row, black or white hats, each sees the ones in front and says one colour from the back; how many are certainly saved | junior / medium | k colours: the sum mod k; why 99 is the most | the line, the parity the last one announces, each guess explained from what he sees and hears | M |
| M264 | **The mutilated chessboard**: an 8 × 8 board without two opposite corners, 31 dominoes | student / easy | which two removed squares leave a tileable board (Gomory: any two of opposite colours) | place dominoes by tap, the colour count shown; Gomory's cycle for two squares of opposite colours | S–M |
| M265 | **Lights out**: a 5 × 5 grid, a tap toggles a cell and its neighbours; turn everything off | junior / medium | a linear system over GF(2): which boards are solvable, the solution by Gaussian elimination (XOR rows, as in hardware) | the board to tap, "solve" lights the cells to press, the matrix row operations stepped | M |
| M266 | **Tower of Hanoi and Gray code**: the moves for n discs, and which disc moves at step k | student / easy | 2^n − 1 moves; the disc of step k is the lowest set bit of k, the reflected Gray code walks the same states | the pegs animated beside the Gray-code counter, the changing bit lit with the disc it moves | S–M |

**Round N — logic about knowledge and choice**

| Id | Question | Level | Generalisation | Explorer | Size |
|---|---|---|---|---|---|
| N267 | **Monty Hall with n doors**: the host opens k empty doors; stay or switch | student / easy | P(win by switching) = (n − 1) / (n (n − k − 1)); the "host who does not know" trap | a game to play and 1,000 seeded games, the two strategies' bars against the formula | S |
| N268 | **Knights and knaves**: three islanders' statements, who lies | student / easy | any set of statements as a truth table, solved by trying all 2^n assignments (the same brute force as a formal tool) | statements built from blocks, the truth table with the consistent rows lit | S–M |
| N269 | **The blue-eyed islanders**: n blue-eyed islanders and one public announcement | senior / hard | induction on n: everyone leaves on day n; what the announcement adds (common knowledge) | a day stepper with each islander's possible worlds shrinking | M–L |

**Round O — probability for random stimulus**

| Id | Question | Level | Generalisation | Explorer | Size |
|---|---|---|---|---|---|
| O270 | **Birthday paradox and transaction IDs**: n random 8-bit tags, the chance that two outstanding transactions share one | junior / easy | 1 − Π(1 − i/N) ≈ 1 − e^(−n²/2N); the n for 50 % and 1 %; why tags are allocated, not drawn | sliders n and N, the exact curve and the approximation, seeded draws with the first collision marked | S–M |
| O271 | **The longest run**: in n random bits, how long is the longest run of ones | junior / medium | about log2 n; the exact probability by a run-length recursion; why random stimulus rarely makes a 20-cycle burst | n slider, the stream with its longest run framed, the distribution of the longest run over runs | M |
| O272 | **The inspection paradox**: buses every 10 minutes on average, how long do you wait | junior / medium | E[wait] = E[T²] / 2E[T]: fixed, uniform and exponential gaps; the same bias in "average packet size seen by a monitor" | a timeline of arrivals with random riders, the gap each rider lands in coloured | M |
| O273 | **Derangements**: n letters in n envelopes at random, the chance that none is right | junior / medium | D(n) = n! Σ(−1)^k/k!, the limit 1/e, the expected number of fixed points is 1 | shuffle and look, the cycle picture of the permutation (as 0009), the exact and simulated fractions | S–M |

**Round P — geometry and counting**

| Id | Question | Level | Generalisation | Explorer | Size |
|---|---|---|---|---|---|
| P274 | **Buffon's needle**: needles of length l on lines d apart, the chance to cross a line | junior / medium | 2l / (π d) for l ≤ d, the long-needle case, estimating π and its error | needles dropped one by one or a thousand at once, the running estimate of π | S–M |
| P275 | **Paths that do not cross the diagonal**: monotone paths on an n × n grid that stay below the diagonal | junior / medium | the Catalan number by the reflection trick; the same count as 0010's valid bracket strings | a path to draw or draw at random, the first crossing reflected into a path to the mirrored corner | M |

**Round Q — digital design and checking**

| Id | Question | Level | Generalisation | Explorer | Size |
|---|---|---|---|---|---|
| Q276 | **Divisible by 3, one bit at a time**: an FSM that reads a binary number MSB first and says whether it divides by 3 | student / easy | any modulus m: state = remainder, next = (2r + b) mod m; LSB first needs the powers of 2 mod m | bits fed by hand, the remainder automaton with the taken edge lit (the seqdet view) | S |
| Q277 | **A serial CRC**: CRC-8 computed bit by bit in an LFSR, then checked against a table-driven reference | junior / medium | any polynomial and width, reflected or not, the residue a receiver checks (the LCRC of 0025) | the register stepping bit by bit with the XOR taps lit, the byte-wise table result beside it | M |
| Q278 | **A button debouncer**: a noisy input, a clean one-cycle pulse per press | student / easy | an N-cycle stability counter; the SVA that no pulse comes within N cycles of another | a bouncing waveform to draw, the counter and the output on a strip | S–M |

**Round R — flow, performance and verification method**

| Id | Question | Level | Generalisation | Explorer | Size |
|---|---|---|---|---|---|
| R279 | **Outstanding requests to fill a link** (Little's law): latency L cycles, one request per cycle, how many tags | junior / medium | N = throughput × latency; with a reply size, a credit limit and a variable latency | a pipeline of requests with their tags, throughput against the number of tags | S–M |
| R280 | **A skid buffer**: a valid / ready pipeline stage that registers ready without losing data | senior / medium | why one extra entry is enough; the SVA for "no data lost, no data duplicated" | a strip with valid / ready / data both sides, stalls drawn by tap, the buffer entry shown | M |
| R281 | **Find the bug: a synchronous FIFO** whose full flag is one entry late | junior / medium | the count against the pointer compare, the test that finds it (fill to the brim), the assertion that would have caught it | the FIFO filled and drained on a strip, the buggy and fixed flags side by side | S–M |
| R282 | **Why a constraint skews the distribution**: `x < y` on 8-bit values, how often is x = 0 | junior / medium | the solver is uniform over solutions, not per variable; `solve x before y` and `dist`; the histogram of both | the two histograms over seeded draws against the exact counts | M |
| R283 | **Regression minimisation**: tests that each hit some coverage bins, the fewest tests that hit all | senior / medium | set cover is NP-hard; the greedy choice and its ln n bound; an exact search for small sets | a test × bin matrix, the greedy pick stepped, the exact optimum beside it | M |

Suggested order: M and Q first (short pages with a strong picture: the hats, Hanoi and Gray
code, the divisibility FSM, the serial CRC), then O (probability the DV pages lean on),
then R, N and P. Round Z's open rows (Z202, Z204 to Z209, Z211 to Z216) stay open beside
these.

### Round Z — new questions from outside sources (proposed 2026-10-22, owner picks)

Half logic and math, half electrical engineering for beginners. Each idea is rewritten in
our words with an original solution and generalisation; the `source` field names where the
idea came from. Not to repeat: the open Q93, Q95, Q97 to Q99 (ant on a can, trains and
fly, clock angles, Heron, rope around the Earth).

| # | Question | Level | Source | Generalisation | Explorer | Size |
|---|---|---|---|---|---|---|
| Z202 | **Two burning ropes, 45 minutes** | student / easy | Wu, Leino | which times n ropes can measure (sums of 60/2^k), a search over lighting states | ropes burning from one or both ends, a timeline | S–M |
| ~~Z203~~ | Done as 0039. **Two eggs, 100 floors** | junior / medium | Leino, LeetCode 887 | k eggs and n floors: the DP and the binomial sum; 14 drops | sliders k and n, the drop tree and the table | M |
| ~~Z204~~ | Done as 0045. **Twelve coins, one fake, three weighings** | senior / hard | Wu | (3^n − 3)/2 coins in n weighings, fake heavier or lighter | a balance: pick coins per pan, the tree of outcomes | M–L |
| Z205 | **100 prisoners and a light bulb** | senior / hard | Wu | the counter protocol for n prisoners, the expected number of days | a simulation with a day counter and a histogram | M |
| Z206 | **Pirates dividing gold** | junior / medium | Wu, Winkler | backward induction for n pirates; the twist past 200 | a stepper adding one pirate at a time | M |
| Z207 | **Ants on a stick** | student / easy | Wu | n ants, any directions: collisions as passing through | an animation with the "swap labels" view | S–M |
| Z208 | **HH or HT – expected flips** | junior / medium | Zhou | any pattern: the Markov chain and Conway's correlation formula | a pattern field, simulation and the chain | M |
| Z209 | **Gambler's ruin** | junior / medium | Zhou | reach N before 0 with probability p, the closed form and the expected time | sliders p, N and the start, simulated paths | M |
| ~~Z210~~ | Done as 0040. **Sequence detector 1011, overlapping** | student / easy | HDLBits, Harris & Harris | any pattern: the KMP automaton, Mealy against Moore | type a bit stream, the state graph lights up | M |
| Z211 | **Setup and hold: the highest clock frequency** | junior / medium | Harris & Harris | clock skew both ways, hold violations, a path with several stages | sliders for t_cq, logic, t_su, skew, and a timing diagram | M |
| Z212 | **Reset synchronizer: async assert, sync deassert** | junior / easy | Cummings | why two flops, what goes wrong without them | a waveform with the release edge near the clock | S–M |
| Z213 | **A one-cycle pulse to a slower clock domain** | junior / medium | Cummings | the toggle synchronizer and the minimum spacing for any clock ratio | two clocks with a ratio slider, lost and kept pulses | M |
| Z214 | **Glitch-free clock mux** | senior / medium | Cummings, ChipVerify | the two-flop handshake per clock, any two frequencies | a waveform where select switches at a random moment | M |
| Z215 | **Round-robin arbiter** | junior / medium | ChipVerify, Verification Guide | N requesters, fairness as SVA, a weighted variant | request toggles, a grant pointer stepping round | M |
| Z216 | **Priority encoder and leading zeros in log depth** | student / medium | HDLBits | a tree for N bits, depth log2 N against a chain | a bit field, the tree with the winning path marked | S–M |
| ~~Z217~~ | Done as 0041. **How many random tests close coverage** | junior / medium | coupon collector, Zhou | n bins: n·H_n, the variance, unequal bin weights | a covergroup filling up, a histogram over runs | M |

### Third series, rounds UI1 to UI5 — look and feel (proposed 2026-10-24, owner picks)

The owner asked for UX / UI proposals that make the site prettier and friendlier. From
screenshots of the home page, the junior catalog and the 0046 page at 1280 and 390 px
(light) on 2026-10-24:

- The home page opens with a plain title, a paragraph and four grey stat tiles; there
  is no call to action, and "3/3 levels with questions" says little. On a phone the
  tiles take most of the first screen.
- Bug: in the study-path cards a long title squeezes the count, so "3 שאלות" breaks
  letter by letter ("שאלו / ת") in the SystemVerilog and PCIe cards.
- Every catalog row carries the "חדש" chip (all questions were added within 30 days),
  so it says nothing; the title column wraps to three lines, and the topics column is
  English monospace tags. The topic filter is four rows of chips.
- The question header is busy: six chips, monospace topics, the source, two badges,
  then two rows of tool buttons and the part bar before the statement.
- Explorer controls are equal-weight outlined buttons that wrap to three or four rows.
- Text uses the theme's Latin-first font; Hebrew has no face of its own (C190 open).

Item numbers continue the global count (319 on).

**Round UI1 — first impression**

| Id | Idea | Size |
|---|---|---|
| ~~UI319~~ | ~~**A real hero**: a headline, one sentence, two buttons ("להתחיל לתרגל" to the next unsolved or a random question, "לכל השאלות"), a large search field; the stats as one slim row with icons~~ done (session 22, part 3) | S–M |
| ~~UI320~~ | ~~**Path cards fixed and polished**: the count never wraps (the letter-by-letter bug), equal heights, a progress ring instead of a bar, an icon per path~~ done (session 22, part 1) | S |
| ~~UI321~~ | ~~**Hebrew typography** (C190 promoted): a Hebrew face (Heebo or Assistant) for text and headings, tabular digits, a line-length cap near 70 characters, more line height~~ done (session 22, part 1 (Rubik kept)) | S–M |

**Round UI2 — the catalog**

| Id | Idea | Size |
|---|---|---|
| ~~UI322~~ | ~~**Compact rows or cards**: the title on one line, level / difficulty / kind as one row of chips, two topics and "+3"; "חדש" only for the newest five or the last 14 days~~ done (session 23, part 5: the newest five of 7 days) | S–M |
| ~~UI323~~ | ~~**Folded filters**: level, difficulty and kind as segmented controls, topics behind "עוד נושאים" with a search field, the active filters as removable chips with the result count~~ done (session 23, part 5, with filters in the address, Hebrew topic names and an empty state) | M |

**Round UI3 — the question page**

| Id | Idea | Size |
|---|---|---|
| ~~UI324~~ | ~~**A calmer header**: id · level · difficulty · kind in one line, topics as quiet links, "interactive", "tested" and "new" as small icons with tooltips; the page tools (open / close all, practice, solved, favourite, random) in one icon toolbar, an overflow menu on phones~~ done (session 22, part 2 (icon-only tools)) | M |
| ~~UI325~~ | ~~**A sticky mini-header** while scrolling: the title, the current part and the solved toggle, with a thin reading-progress line~~ done (session 22, part 2 (no title: the site header shows it)) | S–M |
| ~~UI326~~ | ~~**Friendly feedback**: marking a question solved shows a short celebration (off under reduced motion) and the progress of its level ("5 of 27 in junior")~~ done (session 23, part 6) | S |

**Round UI4 — the explorer boxes**

| Id | Idea | Size |
|---|---|---|
| ~~UI327~~ | ~~**Playback as an icon bar**: start, back, play / pause, step, end as icons with tooltips and a scrub slider, the speed as a three-way segmented control; the edit controls on one row~~ done (session 22, part 4) | M |
| ~~UI328~~ | ~~**Boxes as cards**: a soft background, rounded corners, a header with the kind's icon and name, one spacing scale~~ done (session 22, part 4) | S |
| ~~UI329~~ | ~~**Purposeful micro-motion** (a first cut of E198): changed cells and values fade or slide, the answer appears with a short reveal; off under `prefers-reduced-motion`~~ done (session 23, part 6: a shared flash, tweens in six kinds) | M |

**Round UI5 — identity and polish**

| Id | Idea | Size |
|---|---|---|
| ~~UI330~~ | ~~**An icon per kind** (puzzle, code, design, math, dv) used in the chips, cards, headers and boxes; a friendly 404 page~~ done (session 22, part 1 (kinds); the 404 page in session 23, part 7) | S–M |
| ~~UI331~~ | ~~**Dark mode tuning**: a contrast pass, a softer navy, the figure palette checked for colour-blind pairs (C193's script)~~ done (session 23, part 7: the contrast check in CI and softer dark; the colour-blind pass not picked) | S–M |
| ~~UI332~~ | ~~**Social cards** for shared links (idea 17): the title, the chips and the logo as an image per question~~ done (G45 in session 16; session 23, part 7 added the kind and the counts) | S–M |

Suggested order: UI320 (a bug) and UI321 first, then UI319 and UI324 (the two most
visible screens), then UI322 / UI323, then the boxes (UI327, UI328).

The older idea list below is kept for reference; items covered by the rounds above are
marked.

### Fourth series, review rounds V1 to V7 (session 26, 2026-10-26, owner picks)

A review of the whole project: the site-wide pages and tools (done by hand) and every
question page with its box at 1200 and 390 px (two review passes, findings below as they
came in). Effort: S under an hour, M a few hours, L a day or more.

**Site-wide findings**

- **Study paths cover 21 of 47 questions.** Not in any path: 0001, 0003, 0016, 0024, 0025,
  0026, 0029 to 0048. There is no path for the DV core (FSM, FIFO, CDC, LFSR, SVA,
  coverage: 0001, 0033 to 0036, 0038, 0040, 0041), for the protocol reference models
  (0023 to 0025), or for geometry and motion (0026, 0029, 0030, 0048).
- **No glossary** of DV terms (Hebrew and English: CDC, metastability, credit, TLP...);
  a reader meets a term on one page and its explanation on another.
- **Progress lives only in one browser** (localStorage): solved and favourite marks and
  the remembered boxes are lost on another device, with no export or import.
- **No review loop**: a solved question is never offered again; no "come back to this
  one" list, no self-rating after solving.
- **No interview simulation across questions**: practice mode times one page; there is
  no "three random questions in 45 minutes" session with a summary at the end.
- **No offline use**: a manifest exists but no service worker, so the site does not open
  without a network (for example on a train before an interview).
- **No check-yourself steps**: no page asks the reader for a number or a choice and
  checks it (the "quick quiz" format of **New question formats** is still open).
- **CI jobs have no `timeout-minutes`**: a hung browser check would run for six hours.
- **The header tabs fade in** on the home page; for a moment the last tabs are hard to
  read (cosmetic).
- **The heaviest pages** are 0016 (370 KB of HTML), 0025 (300 KB), 0023 and 0024 (240 KB),
  mostly inline SVG; fine on a phone today, worth watching.

**Question findings, 0001 to 0024** (every box clicked at 1200 and 390 px; drags,
fields and dark mode not covered in this pass)

| Question | Finding | Proposal | Type | Effort |
|---|---|---|---|---|
| 0023 | **Bug, confirmed:** "שלח בקשה" then "מחזור" throws `Cannot read properties of undefined (reading 'cpls')` in `epNext` (`endpoint.js`); play at ×4 too | Drop the page example's scripted draws on a manual send (or range-check the pick); a Node test of send-then-step | bug | S |
| 0002 | The part c box opens on the arithmetic version, not XOR | Open on XOR there without locking the select | box UX | S |
| 0020, 0021 | The map of splits: tick labels collide at 390 px, long row labels run into the bars; 1,563 px tall in 0021 | Show the splits of one completion count, picked from the count table; collapsed by default | box UX | M |
| 0004 | "גילוי התוכן" only changes small captions; the status line stays | Draw the contents in the boxes, update the status; a check-yourself step (assign the three labels, then reveal) | box UX, new aid | S–M |
| 0003 | The page's trap (j = i + 1 sorts descending) cannot be tried; line 5 of the code cut at 390 px; the array wraps at 1200 px | A select "j from 0 / from i + 1" with both results; wrap the code panel | new aid, box UX | M |
| 0010 | Part a's pass-by-pass pair deletion has no visual | A pair-deletion mode in `brackets` with the operation count against the stack's | new aid | M |
| 0015 | Follow-ups ask for a simulation, the page has no code | A Monte Carlo tab (SV and Python) for 1/3 and 13/27 | content | M |
| 0016 | A classic coding question with no code (`kind: math`) | SV and Python tabs: the O(N) recurrence and the closed form | content | M |
| 0001 | SV only; no Python model, no SVA | A Python cycle model and `pulse \|=> !pulse` | consistency | S |
| 0024 | 2,087 px tall on a phone (six stacked buttons); the four hand labels overlap at the start | Buttons in two columns; offset the labels | box UX | S–M |
| 0018, 0019 | Event figures tiny at 390 px; labels in English ("flip A + B") | Stack before / after on phones; Hebrew labels | box UX | S–M |
| 0013 | Path arrows of `kappairs` run over the numbers | Curved arrows, or under the cells | box UX | S |
| 0015 | The 196-cell grid opens empty | Open on step 1 | box UX | S |
| 0011, 0017 | Box content wider than the box at 390 px | Wrap or narrow | box UX | S |
| 0009, 0013, 0016, 0024 | Boxes 1,600 to 2,100 px tall on phones, mostly the proof panels | Collapse the proof panel by default on narrow screens | box UX | M |
| all | Follow-ups answered inline in 0001, bare in 0015 and 0016 | One pattern: a collapsible short answer per follow-up | consistency | M |
| 0021 | The ladder works well | A "guess C(n) before revealing" step | new aid | S |

**Question findings, 0025 to 0048** (38 boxes stepped, played and preset at 1200 and
390 px, drags in 0030 and 0048; no JS errors, no sideways scroll; dark mode not covered)

| Question | Finding | Proposal | Type | Effort |
|---|---|---|---|---|
| 12 pages (0029, 0030, 0031, 0033, 0036, 0037, 0044, 0046, 0048...) | Short LTR spans of box text (formulas, coordinates) break across lines at 390 px and read in the wrong order | `white-space: nowrap` in `ltr()` of `core.js` for short spans; long formulas on their own line | box UX | S |
| 0045 | At 390 px the end balls sit past the ends of the tilted beam | Scale the balls to the beam on narrow widths | bug | S |
| 0039 | At 390 px the "21" next-drop label is clipped at the right edge | Move the label inside the figure | bug | S |
| 0042 | The camel covers the "60" tick; segment labels collide on a phone; "0/3" unexplained | Camel above the axis, short labels on phones, a word for the ratio | bug | S |
| 0040 | "הביט הבא" far from its 0 / 1 buttons; arrowheads cover the state labels | Group the label with the buttons; labels under the nodes | box UX | S |
| 0038 | Rule table 27 px wider than its scroll box on a phone | Shorter headers | box UX | S |
| 0048 | Dragging is mentioned only in the help | A visible "גררו את..." caption, as in 0030 | box UX | S |
| 0046, 0047 | About ten controls above the grid; on a phone it starts 950 px down | Fold the editing controls into a closed group | box UX | M |
| 0047 | Heap entries "(2, 1, 3)" have no field names | Caption "(גובה, שורה, עמודה)" | content | S |
| 0027, 0028, 0042, 0043 | The steady reservation leaves large blank areas (230 px in 0027) | A fixed-height scroll area for the growing table | box UX | M |
| 0029 | The first two rows of the 24-hour strips are solid bars | A one-hour window that can move, or the count only | box UX | S |
| 0034, 0037 | Powers written with a caret ("2^4", "10^-8") | Superscripts, as in 0036 and 0048 | consistency | S |
| 0031 | "A+B> A<" hard to read in RTL; the bridge strip sits under a long table on a phone | Arrows → ←; the bridge above the table | box UX | S |
| 0037 | The three-column table wraps every value on a phone; the ±25 ps window invisible on the 1,000-edge strip | Stack the table on phones; a zoomed inset of the window | box UX | S |
| 0026 | "ב-0.000" beside "2.50"; at t = 0 the dots cover the "A" label | One number format; offset the label | box UX | S |
| 0025 | Box 1,837 px tall on a phone; a status line breaks after a comma | Collapse the random-run controls | box UX | S |
| 0041 | Weight sliders of different lengths on a phone; a row starts with English | Equal widths; a Hebrew label first | box UX | S |
| 0031 | The box replays three fixed plans only | A "your plan" mode (pick who crosses, the running total against 17), like the river box | new aid | M |
| 0039 | The threshold is shown and the box plays the optimal plan | A guess mode: a hidden threshold, the reader picks floors, the worst case against f(k, n) | new aid | M |
| 0036 | No picture of the register with its taps and XOR | A register row that shifts with the steps; the chord over the 0000 node | new aid | M |
| 0035 | No schematic of the circuit; odd N never generalised; 3 cycles visible on a phone | A generated schematic, a third hint, a follow-up for odd N, a duty readout | content | M |
| 0033 to 0038 | Parts listed at the top with hints after them; one hint in several parts; two traps per page (0035: no parts, no figure) | The layout of 0027 to 0032 and 0039 to 0048: a heading per part with two or three hints, four or five traps | consistency | M |

**Rounds** (pick any; the earlier ones are smaller and fix what is broken)

| Round | Content | Effort |
|-------|---------|--------|
| V1 (done, item 55) | **Bugs and quick fixes**: the 0023 box error, the 0002 default, `ltr()` without line breaks, the 0045 balls, the 0039 label, the 0042 camel, the 0048 drag caption, the 0047 caption, superscripts in 0034 and 0037, the 0026 number format | S–M |
| V2 | **Study paths for everything**: paths for the DV core, the protocol reference models, geometry and motion; 0044 to 0047 into the algorithms path; a lint check that names a question in no path | S–M |
| V3 | **Boxes on a phone**: collapse the proof panels (0009, 0013, 0016, 0024) and the editing and random-run controls (0025, 0046, 0047); 0024 buttons in two columns; 0018 and 0019 stacked with Hebrew labels; the 0020 / 0021 split map by completion count; 0031, 0037, 0038, 0040, 0041; scroll areas instead of blank reservations (0027, 0028, 0042, 0043) | M–L |
| V4 | **Try it yourself**: 0031 your own plan, 0039 a hidden threshold, 0004 assign the labels, 0003 the j = i + 1 trap, 0010 pair deletion, 0021 guess C(n), 0036 the register row, a check-yourself step (a number or a choice checked on the page) on chosen pages | M–L |
| V5 (done, item 55) | **Content and consistency**: 0033 to 0038 in the common layout with more hints and traps; 0035 schematic and odd N; one follow-up pattern (a collapsible short answer); code tabs for 0016 (the owner did not pick the 0015 simulation or the 0001 Python model) | M–L |
| V6 | **Practice loop and glossary**: a "my progress" page, a self-rating after a solution, export / import of the progress; a glossary page with a tooltip on a term's first use | M |
| V7 (done, item 55) | **Robustness**: `timeout-minutes` on the CI jobs, a service worker for offline reading, the header tabs without the fade | S–M |

## Improvement ideas

Ordered roughly by value for effort. **S** = small (under an hour), **M** = a few hours,
**L** = a day or more.

### Practice experience

| # | Idea | Effort | Notes |
|---|------|--------|-------|
| 1 | ~~Previous / next question links~~ | S | **Done** in session 4 (round A) |
| 2 | ~~"Open all / close all solutions" button~~ | S | **Done** in session 4 (round B) |
| 3 | ~~Random question button, honouring the current filters~~ | S–M | **Done** in session 6 (C20) |
| 4 | ~~Solved / favourite marks stored in the browser, with progress per level~~ | M | **Done** in session 6 (C22) |
| 5 | ~~Interview mode~~ | M | **Done** in session 4 as "practice mode" (solutions hidden, stopwatch counting up) |
| 6 | ~~**Sortable table columns** (id, level, difficulty); coloured chips~~ | S–M | Done: chips in session 4, sorting in session 6 (C18) |
| 7 | ~~Related questions by shared tags~~ | S–M | **Done** in session 4 (round A) |
| 7a | ~~Hint ladder~~ | S | **Done** in session 4 (round B) |
| 7b | ~~**Question type filter** (puzzle / code / design / knowledge) next to level and difficulty~~ | S–M | **Done** as the `kind` field and its filter chips (E31, session 22) |
| 7c | **"Open in EDA Playground"** link for SV code, so readers can run it on a commercial simulator | S–M | EDA Playground has no prefill API; a "copy code + open site" button is the simple version |
| 7d | ~~Step-through figures with next / previous buttons~~ | M | **Done** in session 5 (B14) |

### Content quality and safety net

| # | Idea | Effort | Notes |
|---|------|--------|-------|
| 8 | ~~Keep the test harnesses in the repo and run them in CI~~ | M | **Done** in session 2 |
| 9 | ~~Extract code from the pages for testing~~ | M | **Done** in session 2 (`tools/extract_code.py`) |
| 9a | Show a "tested ✓" badge per question on the tables, from the last CI run | S–M | The header card shows "נבדק אוטומטית" since session 4 |
| 9b | ~~Adopt a newer Verilator in CI to run constraints natively and drop translations~~ | M | **Done** in session 5 (pinned commit + z3) |
| 10 | ~~Keep the figure generators in the repo~~ (`tools/figures/`) | S | **Done** for 0008–0011 in session 3; older figures (0005–0007) still have no generator |
| 11 | ~~Broken link / image check in CI~~ | S | **Done** in session 5 (`tools/check_links.py`) |
| 12 | ~~Repository `CLAUDE.md`~~ | S | **Done** in session 5 |
| 12a | ~~Generators for the older figures (0004–0007) in `tools/figures/`~~ | S–M | **Done** in session 16 (G43) |
| 12b | ~~A **"new question" script** that creates the page, `tests/<id>/` and the catalog row from the template~~ | S–M | **Done**: `tools/new_question.py` (G42, J60) |

### Site polish

| # | Idea | Effort | Notes |
|---|------|--------|-------|
| 13 | ~~Site logo and favicon~~ | S | **Done** in session 4 (round A) |
| 14 | ~~Statistics on the home page~~ | S–M | **Done** in session 4 (round B) |
| 15 | ~~Show the `added` date, `source` and a "new" badge~~ | S | **Done** (date in session 4, source and the 30-day "new" chip in session 5) |
| 16 | ~~**Better Hebrew search**~~ (done, C21) | M | The built-in search splits Hebrew on whitespace only; evaluate the search `separator` setting or an alternative index |
| 17 | ~~**Social preview cards** when sharing a question link~~ | S–M | **Done** in session 16 (G45) |
| 18 | ~~**Comments / discussion** per question via GitHub Discussions (giscus)~~ | M | **Done** in session 16 (G45); waits for the owner's giscus ids |
| 19 | **PDF export** of a filtered question set for offline practice | M–L | e.g. a print-site plugin |
| 20 | Bilingual content (Hebrew / English) | L | Only if the audience grows beyond Hebrew readers |
| 21 | ~~**Mobile check** of every page in CI~~ (done, C17) (screenshots at phone width) | M | Wide tables and figures were the main issue so far (see the 0009 box grid) |
| 22 | **Topic pages**: a short intro per topic (FSM, SVA, coverage...) linking to its questions | M | Study paths done in C19; topic intros proposed again as E32 |
| 23 | ~~Step-through figures (B14)~~ | M | **Done** in session 5 (0010 stack, 0009 walks) |

---

## Technical notes for whoever continues this work

- SystemVerilog tests: Verilator must be newer than 5.052 (CI builds the commit in
  `VERILATOR_REF`; the same recipe is in `README.md`) and `z3` must be on the PATH. The
  5.052 release crashes on 0011 and mis-randomizes the 0014 subclass; the apt package
  (5.020) has no constraint support. `run_tests.py` refuses older versions.
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
