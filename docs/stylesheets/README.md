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
| `10-rounds-w.css` | rounds W1 to W4: surfaces, traps, the home page, the run panel, motion, self-checks |
| `11-questions.css` | the figures and boxes of 0036 and of 0049 to 0061 |
| `12-rounds-y-s.css` | rounds Y and S: the tags page, box text size, touch tools, side navigation, button runs, S2 figures |

The browser gets the parts as one file: `hooks/questions.py` joins them in this order into
`stylesheets/site.css` at the end of the build and links that file from every page and from
the 404 page (S423). The parts are the source; the joined file is never edited.

Colours are CSS variables, defined for both schemes in `01-base.css` (the palette) and used
everywhere else; figures and boxes never hard-code a colour. A new rule goes into the part
of its component, at its end, or into the last part when it overrides rules of several
parts. `tools/check_contrast.py` reads every part in this order.
