# The site's styles

The CSS of the site, in parts that load in the order of their numbers (`extra_css` in
`mkdocs.yml`). Until session 27 it was one file, `extra.css`, written round after round;
it was split in that order (S426), so the cascade is the same: a rule in a later part may
refine one in an earlier part, and moving a rule between parts can change what wins.

| Part | Holds |
|---|---|
| `01-base.css` | the palette of both schemes, the design tokens, left-to-right code and math |
| `02-pages.css` | chips, the question header card, related questions, the filter bar and question tables, arrays, chart colours and legends |
| `03-runner-figures.css` | the first Python runner and the figures of 0008 to 0014 |
| `04-solutions.css` | admonition types, solution blocks and map, cost chips, content tables, the shared box layout, step timelines |
| `05-tools-home.css` | the toolbar, the hint ladder, the first home page, step-through figures, marks and study paths |
| `06-figures.css` | the figures of 0018 to 0048 (hourglass, PCIe, credits, cake, clock, box nets, farm) |
| `07-reading-aids.css` | reading aids (enlarge, lightbox, part bar), focus rings, code in dark mode, comments |
| `08-explorers.css` | the explorer boxes of 0004 to 0047 |
| `09-redesign.css` | the redesign: typography, icons, the header and toolbar, the hero, box cards, the 404 page, print, question tables |
| `10-rounds-w.css` | rounds W1 to W4: surfaces, traps, the home page, the run panel, motion |
| `11-questions.css` | the figures and boxes of 0036 and of 0049 to 0062 |
| `12-rounds-y-s.css` | rounds Y and S: the tags page, box text size, touch tools, side navigation, button runs, S2 figures |
| `13-motion.css` | round M: the drawn logo, the header and table of contents, the hero's live waves and example, cards, the question header card, hint feedback, the box skeleton, page transitions, the footer, the 404 page |
| `14-layout.css` | the desktop layout: the wider grid, the folded level list in the side navigation, the grips that resize the three columns (`layout.js`) |
| `15-home.css` | round V: the home page's navy band, the live level cards, the question of the day (`home-extras.js`) |
| `16-maps.css` | round V: the study-path metro map and the tag graph (tokens `--mm-*`, `--tg-*`; `maps.js`) |
| `17-lists.css` | round V: the level pages' header band with progress, the question table rows (stripe, kind tile, marks, whole-row link, cards on phones; `level-page.js`) |
| `18-question.css` | round V: the question header card's pattern and kind icon, the part timeline, the code window (`question-page.js`) |
| `19-details.css` | round V: the success pulse, the content icons (kinds, levels, paths), the box loading wave (`details.js`) |
| `20-video.css` | the tutorial video (V3): the page tool's play icon, the chapter links at the top of the solutions, the dialog with its navy poster (tokens `--vd-*`, one version for both schemes; `video.js`) |
| `21-interview.css` | interview mode (session 30): the bar at the foot of the screen, the confidence question, the interviewer's follow-up and the summary (`question-tools.js`); the quick jump window (`quick-jump.js`); the home page's interview builder (`home.js`) and my map (`home-extras.js`) |
| `22-circuit.css` | the circuit layer (session 32): the quiet board-trace pattern at the top of every page and in the wide margins (`body::before`, `body::after`), each question's chip (`qchip`, `question_chip` in the hook) in the lists and the question header, the compact phone header, the difficulty as three LEDs (`.chip-diff`), path cards that light on hover, the part bar's reading line as a clock, and the slow icosahedron of the home hero and the level bands (`circuit.js`) |
| `23-polish.css` | the finishing round of the UX audit (session 32): one action colour in the boxes and the run panel (`--act`, `--act-line`: navy filled, navy outline, never amber), icon buttons at 44 px with their short name under them on a phone (`data-name`, set by `core.js`), inline code at least 13 px, the part bar's reading line clipped rather than resized |
| `24-living.css` | the living layer (session 32): the pad field of the home hero and the level bands (`.lv-dots`, `dotgrid.js`), the page transition's timing, the skeletons of a box not built yet and of the run panel's output while Python downloads, tabular figures, the page titles a step larger, and the footer's crop marks and board line (`.df-board`, the date of the last commit from the hook) |
| `25-figures-c.css` | the figures of S415 (session 32): the XOR steps of 0002, the passes of 0003, the handshake contract of 0038 |
| `26-ui-round.css` | the UI round of session 33: one yellow button on the home hero and the board's stop button, a question's title over its subtitle and the source at the page's end, the header's chips in three tiers, exit tokens (`--ease-exit`, `--dur-exit-0..2`) for what closes, a content-only fade between pages, tabular figures |
| `27-box-columns.css` | a box on one computer screen (session 34): the figure beside its tables, notes and code from a 600 px box (`columns()` in `core.js`) |
| `28-site-flow.css` | the two diagrams of the page on how the site is built (session 34, `tools/figures/site_flow.py`): the lane buttons and the animation switch, the static figure and its run, hidden under reduced motion |
| `29-question-ux.css` | the UX round's question page (session 34): the box chip and teaser, the end card after "solved", the shorter header and the tools in the sticky strip on a computer, the opaque strip, the outlined solution button, wide tables that scroll |
| `30-lists-ux.css` | the UX round's lists (session 34): the dropdown filter row, one-line question rows and two-line phone cards, the home page's steps line |
| `31-maps-ux.css` | the UX round's maps (session 34): path names, the station card and the scroll hint of the metro map, the paths as rows, the tags page's level row and sorted topic list |

After the numbered parts come the stylesheets of single questions, in `questions/`, named
`<id>-<name>.css` after the question (`questions/0083-jugs.css` for 0083's water jugs). A new
question whose figures or box need rules of their own gets such a file, with its own class
prefix (the class table of `CONTRIBUTING.md` lists them), and a line at the end of `extra_css`.

| File | Prefix | Holds |
|---|---|---|
| `questions/0083-jugs.css` | `wj-` | the water jugs: the jugs, the grid of the states, the `jugs` / `jugs3` boxes |
| `questions/0084-lis.css` | `lis-` | the longest increasing subsequence: its figures and box |
| `questions/0085-selfdesc.css` | `sd-` | the self-describing number: the digit tables and the box |
| `questions/0086-chameleons.css` | `ch-` | the chameleons: their figures and box |
| `questions/0087-lights.css` | `lo-` | Lights Out: the boards of the figures and the box |
| `questions/0088-ducci.css` | `du-` | differences in a circle: the circle, the parity rows, the box's chart |
| `questions/0089-frobenius.css` | `fb-` | coins you cannot make up: the amount tables and the box |
| `questions/0090-pancake.css` | `pk-` | pancake sorting: the stacks and the box |
| `questions/0091-chomp.css` | `cp-` | Chomp: the chocolate bars and the box |
| `questions/0092-circle.css` | `mc-` | points on a circle: the regions and the box |
| `questions/0093-match.css` | `sm-` | stable matching: the figure and the preference tables of the box |
| `questions/0094-creditwalk.css` | `cw-` | the credit counter as a random walk: the charts of the figures, the walk and the two curves of the box |
| `questions/0095-soldiers.css` | `cy-` | Conway's soldiers: the boards of the figures and the box, the weights of part c, the potential meter |
| `questions/0096-kelly.css` | `ky-` | the Kelly criterion: the curve g(f), the wealth paths on a log scale, the box with its paths and curve |
| `questions/0097-isqrt.css` | `isq-` | the integer square root in hardware: the step as areas, the bit rows, the box's table of the eight steps |
| `questions/0098-luhn.css` | `lu-` | check digits: the digit strips of the figures, the box's strip and its two maps of the errors |
| `questions/0099-iban.css` | `ib-` | the IBAN's check digits: the digits of the moved IBAN with the remainder mod 97 under each, the box's lines and its error at a chosen place; part b's state diagrams, block diagram and the hardware box (`ih-`) |
| `questions/0022-latpaths.css` | `lp-` | the paths in a grid: the tints of the counts on the boards (the shared `gx-` figures and the `gp-` grid of the box), the small boards with one path each |
| `questions/0100-stairs.css` | `sw-` | the ways to climb the stairs: the staircases of the figures with the arrows into a stair, the box's flights of stair buttons |
| `questions/0037-editdist.css` | `ed-` | the edit distance between two streams: the tables of the prefixes with the path shaded by step, the band, the box's table filled a cell at a time and its report |

The browser gets the parts as one file: `hooks/questions.py` joins them in this order into
`stylesheets/site.css` at the end of the build and links that file from every page and from
the 404 page (S423). The parts are the source; the joined file is never edited.

Colours are CSS variables, defined for both schemes in `01-base.css` (the palette) and used
everywhere else; figures and boxes never hard-code a colour. A new rule goes into the part
of its component, at its end, or into the last part when it overrides rules of several
parts. `tools/checks/check_contrast.py` reads every part in this order, the numbered parts first.
