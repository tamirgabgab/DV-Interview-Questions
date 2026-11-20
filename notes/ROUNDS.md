# Fix rounds: the plan to go over with the owner

Written in session 35 (2026-11-19) from the review of the site. The tasks themselves, with
their measurements and file references, are in [`HANDOFF.md`](HANDOFF.md) under "Open
items", "Next steps (session 35)", N1 to N8; this file only groups them into rounds, in
the proposed order of work, so the owner and the session can go through them one at a
time. Rounds 1 to 3 are done (session 35); rounds 4 to 9 are not started.
Round 8 was split in two on 2026-11-20: 0036 alone is round 8, the rest round 9.

How to use it: before a round, read its row and its section, answer the open questions,
then tick the round's tasks in `HANDOFF.md` as they are done and write the outcome in the
"Status" line here. Rounds 1 to 3 are done.

The model columns are a judgment by the kind of work and its risk, not a measurement of
cost or quality. The cheaper model is expected to do the work when it gets one task at a
time (N6.1 alone, not a whole round) and the matching checks run after each task.
Each cell gives the model and the reasoning effort to set for the session (low, medium,
high, xhigh, max); a cheaper model usually gets a higher effort to make up for it.

## The rounds

| Round | What it holds | Tasks | Size | Recommended model, effort | Cheaper model, effort | Why |
|-------|---------------|-------|------|-------------------|---------------|-----|
| 1. Housekeeping | a retry in `check_links.py`, Verilator v5.054, this folder's archive, a lock of the dependencies | N1.1 to N1.4 | small | Sonnet 5.5, medium | Haiku 5.5, high | well-defined work, and the checks catch mistakes |
| 2. Accessibility and speed | the run panel's Tab trap, `fitNav`, forced colours, line numbers as tab stops, small fields, the sticky rows on a short screen, the drawer button, the first-visit guide | N6.1, N6.2, N6.6 to N6.11 | medium | Opus 5.5, high | Sonnet 5.5, high | small fixes, but in code every page shares, and each finding is reproduced first |
| 3. The question header and layout shifts | the chip row and the meta line on a phone, the home page's shift on a tablet, the part row's jump | N5, N6.3 to N6.5 | medium | Opus 5.5, high | Sonnet 5.5, high | needs visual judgment in RTL at several widths |
| 4. Page weight | minify `site.css`, load by page type, remove dead rules, literal colours, a weight budget | N2.1 to N2.5, N6.12 | large | Fable 5.2, high | Opus 5.5, xhigh | a change in the hook that builds the whole site; a mistake breaks pages nobody looked at |
| 5. Search and sharing | a description per page, JSON-LD, sitemap dates, Search Console (owner) | N3.1 to N3.4 | small to medium | Sonnet 5.5, medium | Haiku 5.5, high | separate additions to the hook, easy to check in the built HTML |
| 6. DV-core questions | about ten new questions: "find the bug", UVM, SVA, coverage, CDC | N4.1, N4.4 | very large | Fable 5.2, xhigh | Opus 5.5, xhigh | correct SystemVerilog, proofs and boxes; a mistake costs the most here |
| 7. Grading and wording | re-grade the difficulty, reword the level cards, missing topic names | N4.2, N4.3, part of N7 | small | Sonnet 5.5, medium | Haiku 5.5, medium | front matter and text, once the owner sets the criteria |
| 8. Question 0036 | the LFSR box taller than a screen and the page's deferred review items | the 0036 line of N7 | medium | Opus 5.5, xhigh | Opus 5.5, high | it already failed twice with agents, so not a cheaper model |
| 9. Older items and CI time | boxes taller than a screen, small figure labels, a shorter CI, the rest of N7 | N7 (without 0036), N8 | medium | Opus 5.5, high | Sonnet 5.5, high | simpler, separate fixes; the checks catch most mistakes |

Where not to save: rounds 6 and 4. In round 6 the content is the product; in round 4 one
change reaches all 109 pages. Where saving is safe: rounds 1, 5 and 7, since
`lint_pages.py`, `mkdocs build --strict` and `check_links.py` catch almost every mistake.
Round 8 (0036) stays on the recommended model; round 9 is safe on the cheaper one.

## Round by round

### Round 1. Housekeeping

- Open questions: none; it can start at once.
- Status: done in session 35 (2026-11-19), work log item 213 of `HANDOFF.md`. Verilator
  v5.054 passed every testbench, so the pin is the release commit.

### Round 2. Accessibility and speed

- The measurements are a subagent's; reproduce each before fixing it.
- Open questions: turn `anchor_linenums` off, or keep the links and take them out of the
  tab order (N6.7)? Answered by the work: the links stay, with `tabindex="-1"`.
- Status: done in session 35 (2026-11-20), work log item 214 of `HANDOFF.md`. Left for the
  owner: a try of N6.8 on an iPhone.

### Round 3. The question header and layout shifts

- Open questions: the kind chip as an icon only on a phone (offered in work log item 210,
  not answered), or the "tested" check moved into the meta line? May the meta line wrap to
  two lines on a phone? The owner (2026-11-19): the kind chip as an icon, and the line wraps.
- Status: done in session 35 (2026-11-20), work log item 215 of `HANDOFF.md`. The largest
  layout shift left is MathJax's (N9.1), which fits round 4.

### Round 4. Page weight

- No visible change is intended; compare computed styles before and after, as in work log
  item 205.
- Open questions: none before starting; the split by page type (N2.3) is shown to the
  owner as numbers before it goes to `main`. New from round 3: math rendered at build time
  (N9.1) removes the MathJax download and the largest layout shift; which renderer?
- Status: not started.

### Round 5. Search and sharing

- Open questions: does the owner want the site in Google Search Console (N3.4)? Yes; the
  owner sends the verification code.
- Status: done in session 35 (2026-11-20), work log item 216 of `HANDOFF.md`, except the
  verification code.

### Round 6. DV-core questions

- 23 of 109 questions are DV or hardware; there is no debug question.
- Open questions: which topics and how many; is "find the bug" a new kind of page; which
  levels (student has 14 questions, junior 69, senior 26).
- Status: not started.

### Round 7. Grading and wording

- 84 of 109 questions are "medium".
- Open questions: the criteria for easy, medium and hard per level; reword the level
  cards now, or after round 6 adds the questions they promise? The owner: now, and the
  session proposes the criteria.
- Status: the level cards and the topic names done (work log 216); the re-grading is
  proposed and waits for the owner.

### Round 8. Question 0036

- Open questions: is 0036 worth a third attempt, or does its box get a simpler design?
- Status: not started.

### Round 9. Older items and CI time

- Open questions: is a 34-minute full lane a problem for the owner at all?
- Status: not started.
