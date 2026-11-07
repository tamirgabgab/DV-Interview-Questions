"""Contrast of the site's colour pairs in the light and the dark scheme (WCAG 2).

The colours are the CSS custom properties: Material's own (read from the installed theme's
stylesheets) overridden by the site's own, `docs/stylesheets/NN-*.css` in order (`:root`, then
`[data-md-color-scheme="default"]` or `[data-md-color-scheme="slate"]`). Each pair below is
a text or a mark on a background as the site draws it; a translucent colour is composited
over what lies under it. Text needs 4.5:1, marks and controls (icons, bars, focus rings)
3:1. A pair under its minimum fails, so a new colour that reads badly stops the deploy.

    python tools/checks/check_contrast.py          # every pair, both schemes
    python tools/checks/check_contrast.py --all    # also print the pairs that pass
"""

from __future__ import annotations

import argparse
import colorsys
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# the site's stylesheets in their load order (mkdocs.yml lists the same parts)
STYLES = (sorted((ROOT / "docs" / "stylesheets").glob("[0-9][0-9]-*.css"))
          + sorted((ROOT / "docs" / "stylesheets" / "questions").glob("[0-9][0-9][0-9][0-9]-*.css")))

TEXT, UI = 4.5, 3.0

# (what, foreground, background, minimum); a background is a list, top layer first, for a
# translucent fill over another fill (a layer may differ by scheme: a dict). CARD is the
# explorer box's surface (white on the off-white page in the light scheme, W336).
PAGE = "var(--md-default-bg-color)"
TOAST = {"default": "var(--md-primary-fg-color)", "slate": "color-mix(in srgb, var(--md-primary-fg-color) 70%, #000)"}
# the seven output tints of 0078 (the five series, the amber accent, a blue-green mix)
RN_TINTS = ["var(--viz-s1)", "var(--viz-s2)", "var(--viz-s3)", "var(--viz-s4)", "var(--viz-s5)", "var(--md-accent-fg-color)",
            "color-mix(in srgb, var(--viz-s1) 50%, var(--viz-s3))"]
CARD = {"default": "var(--site-surface)",
        "slate": "color-mix(in srgb, var(--md-default-fg-color) 4%, var(--md-default-bg-color))"}
PAIRS = [
    ("body text", "var(--md-default-fg-color)", [PAGE], TEXT),
    ("secondary text", "var(--md-default-fg-color--light)", [PAGE], TEXT),
    ("links", "var(--md-typeset-a-color)", [PAGE], TEXT),
    ("box header title", "var(--md-typeset-a-color)", ["color-mix(in srgb, var(--md-typeset-a-color) 7%, var(--md-default-bg-color))"], TEXT),
    ("code", "var(--md-code-fg-color)", ["var(--md-code-bg-color)"], TEXT),
    ("code keyword", "var(--md-code-hl-keyword-color)", ["var(--md-code-bg-color)"], TEXT),
    ("keyword, highlighted line", "var(--md-code-hl-keyword-color)", ["var(--md-code-hl-color--light)", "var(--md-code-bg-color)"], TEXT),
    ("comment, highlighted line", "var(--md-code-hl-comment-color)", ["var(--md-code-hl-color--light)", "var(--md-code-bg-color)"], TEXT),
    ("id label", "var(--site-label-color)", [PAGE], TEXT),
    ("chip easy", "var(--diff-easy)", ["var(--diff-easy-bg)", PAGE], TEXT),
    ("chip medium", "var(--diff-medium)", ["var(--diff-medium-bg)", PAGE], TEXT),
    ("chip hard", "var(--diff-hard)", ["var(--diff-hard-bg)", PAGE], TEXT),
    ("site header", "var(--md-primary-bg-color)", ["var(--md-primary-fg-color)"], TEXT),
    ("navy on amber (buttons)", "#1b2a4a", ["var(--md-accent-fg-color)"], TEXT),
    ("message and guide text", "#ffffff", [TOAST], TEXT),
    ("figure text", "var(--viz-text)", [PAGE], TEXT),
    ("follow-up answer label", "var(--adm-followup)", [PAGE], TEXT),
    ("figure ink", "var(--viz-ink)", [PAGE], TEXT),
    ("orange running text", "var(--viz-s2-text)", [PAGE], TEXT),
    *[(f"series {n} text in a box", f"var(--viz-s{n}-text)", [CARD, PAGE], TEXT) for n in (1, 2, 3, 4)],
    ("figure text in a box", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("pressed tool icon", "var(--md-typeset-a-color)", ["var(--site-primary-soft)", PAGE], UI),
    ("amber marks (star, sort)", "var(--site-mark-color)", [PAGE], UI),
    ("amber bar in the message", "var(--md-accent-fg-color)", [TOAST], UI),
    ("focus ring", "var(--site-focus-ring)", [PAGE], UI),
    ("chart blue", "var(--viz-s1)", [PAGE], UI),
    ("chart orange", "var(--viz-s2)", [PAGE], UI),
    ("chart green", "var(--viz-s3)", [PAGE], UI),
    ("map digit on high ground", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 29%, var(--md-default-bg-color))"], TEXT),
    ("map digit on deep water", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 45%, var(--md-default-bg-color))"], TEXT),
    ("table text on water", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 20%, var(--md-default-bg-color))"], TEXT),
    ("ladder cell label, chosen", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s2) 22%, var(--md-default-bg-color))"], TEXT),
    ("dead mouse number", "var(--md-default-bg-color)", ["var(--viz-ink)"], TEXT),
    ("tag on a doubled response", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 22%, var(--md-default-bg-color))"], TEXT),
    ("tag fault badge", "var(--md-default-bg-color)", ["var(--viz-ink)"], TEXT),
    ("coin of the first player", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("a search match, dark text on its amber tint (site search)", "var(--md-default-fg-color)", ["color-mix(in srgb, var(--md-accent-fg-color) 32%, var(--md-default-bg-color))"], TEXT),
    ("the no-result button of the site search", "var(--md-primary-bg-color)", ["var(--md-primary-fg-color)"], TEXT),
    ("the TOC link being read (one scroll-spy)", "var(--md-typeset-a-color)", [PAGE], TEXT),
    ("wizards box, the option taken", "var(--md-default-fg-color)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("chain state text on a win", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("chain state turn on a win", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("a bit 0 or a matching flip (0079 figures and boxes)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("the deciding flip (0079 figure and cmpcoin box)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 22%, var(--md-default-bg-color))"], TEXT),
    ("a bit 0, its border (0079 boxes)", "var(--viz-s3)", [CARD], UI),
    ("a token I can take, its border on the box (0082 box)", "var(--viz-s1)", [CARD], UI),
    ("the winning move's token, its border on the box (0082 box)", "var(--viz-s2)", [CARD], UI),
    ("the XOR's top bit, its frame (0082 box)", "var(--viz-s2)", [CARD], UI),
    ("base-3 digit (0076 box)", "var(--viz-ink)", [CARD], TEXT),
    ("base-3 leading digit (0076 box)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 22%, var(--md-default-bg-color))"], TEXT),
    ("base-3 appended 0, its dashed border (0076 box)", "var(--viz-s3)", [CARD], UI),
    ("base-3 leading digit, its border (0076 box)", "var(--viz-s2)", [CARD], UI),
    ("a moved 0, its border (0077 box)", "var(--viz-s2)", [CARD], UI),
    ("a bit cell of 1 (0077 box)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("the step's queen on a light square (0081 boards)", "var(--viz-s1)", [PAGE], UI),
    ("the step's queen on a dark square (0081 boards)", "var(--viz-s1)", ["color-mix(in srgb, var(--viz-grid) 75%, var(--md-default-bg-color))"], UI),
    ("a queen on a dark square (0081 figures)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-grid) 75%, var(--md-default-bg-color))"], UI),
    ("an attacked queen on a dark square (0081 nqplace)", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-grid) 75%, var(--md-default-bg-color))"], UI),
    ("an attacked queen on a light square (0081 nqplace)", "var(--viz-s2-text)", [PAGE], UI),
    ("a queen of the even half (0081 construction)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], UI),
    ("a queen of the odd half (0081 construction)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 28%, var(--md-default-bg-color))"], UI),
    ("a free bit (0081 masks)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 28%, var(--md-default-bg-color))"], TEXT),
    ("a solution's queen, its outline on a dark square (0081 nqueens)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-grid) 75%, var(--md-default-bg-color))"], UI),
    ("figure text on the felt (0080)", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-grid) 35%, var(--md-default-bg-color))"], TEXT),
    ("a pocket and the ball's outline on the felt (0080)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-grid) 35%, var(--md-default-bg-color))"], UI),
    ("the path, the aim and the pocket entered on the felt (0080)", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-grid) 35%, var(--md-default-bg-color))"], UI),
    ("a cushion hit and a gap on the felt (0080)", "var(--viz-s1)", ["color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-grid) 35%, var(--md-default-bg-color))"], UI),
    ("the gap of the pocket entered (0080 box)", "var(--viz-s3-text)", ["color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-grid) 35%, var(--md-default-bg-color))"], UI),
    *[(f"output on tint {i} (0078)", "var(--viz-ink)", [f"color-mix(in srgb, {c} 24%, var(--md-default-bg-color))"], TEXT)
      for i, c in enumerate(RN_TINTS, 1)],
    *[(f"v above the output on tint {i} (0078)", "var(--viz-text)", [f"color-mix(in srgb, {c} 24%, var(--md-default-bg-color))"], TEXT)
      for i, c in enumerate(RN_TINTS, 1)],
    ("a rejected outcome, its text and dashed border (0078)", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("the cheapest k, on the current row (0078 box)", "var(--viz-s3-text)", ["var(--md-code-bg-color)"], TEXT),
    ("chain state text on the cats", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 18%, var(--md-default-bg-color))"], TEXT),
    ("chain state turn on the cats", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s2) 18%, var(--md-default-bg-color))"], TEXT),
    ("chain frame of my states", "var(--viz-s1)", [PAGE], UI),
    ("figure digit on the found square", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 45%, var(--md-default-bg-color))"], TEXT),
    ("ball number, maybe heavy", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))"], TEXT),
    ("ball number, maybe light", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 30%, var(--md-default-bg-color))"], TEXT),
    ("ball number, either", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s4) 30%, var(--md-default-bg-color))"], TEXT),
    ("ball number, known good", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-grid) 50%, var(--md-default-bg-color))"], TEXT),
    ("load number on the balance", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 14%, var(--md-default-bg-color))"], TEXT),
    *[(f"island number on colour {n}", "var(--viz-ink)", [f"color-mix(in srgb, var(--viz-s{n}) 40%, var(--md-default-bg-color))"], TEXT) for n in (1, 2, 3, 4, 5)],
    ("land not yet flooded", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 16%, var(--md-default-bg-color))"], TEXT),
    ("settled node time", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 30%, var(--md-default-bg-color))"], TEXT),
    ("corner link and relaxed edge", "var(--viz-s2)", [PAGE], UI),
    ("grid wall (0070)", "color-mix(in srgb, var(--viz-ink) 72%, var(--md-default-bg-color))", [CARD, PAGE], UI),
    *[(f"grid value, {what} cell on {ground} (0070)", "var(--viz-ink)", [f"color-mix(in srgb, var(--viz-{s}) 30%, transparent)", f"color-mix(in srgb, var(--viz-{g}) {p}%, var(--md-default-bg-color))"], TEXT)
      for what, s in (("visited", "s1"), ("frontier", "s3")) for ground, g, p in (("mud", "s2", 22), ("mountain", "ink", 29))],
    ("question count on the fold button", "var(--md-default-fg-color)", ["var(--site-primary-soft)", "var(--site-surface)"], TEXT),
    ("column grip line", "var(--site-mark-color)", [PAGE], UI),
    ("home band heading", "var(--hb-ink)", ["var(--hb-bg)"], TEXT),
    ("home band card text", "var(--hb-ink-2)", ["var(--hb-card)", "var(--hb-bg)"], TEXT),
    ("home band card secondary text", "var(--hb-ink-3)", ["var(--hb-card)", "var(--hb-bg)"], TEXT),
    ("home band link", "var(--hb-link)", ["var(--hb-card)", "var(--hb-bg)"], TEXT),
    ("home band id and kicker", "var(--hb-accent)", ["var(--hb-card)", "var(--hb-bg)"], TEXT),
    ("home band easy chip", "var(--hb-easy)", ["var(--hb-easy-bg)", "var(--hb-card)", "var(--hb-bg)"], TEXT),
    ("home band easy bar segment", "var(--hb-easy)", ["var(--hb-card)", "var(--hb-bg)"], UI),
    ("home band medium chip", "var(--hb-medium)", ["var(--hb-medium-bg)", "var(--hb-card)", "var(--hb-bg)"], TEXT),
    ("home band medium bar segment", "var(--hb-medium)", ["var(--hb-card)", "var(--hb-bg)"], UI),
    ("home band hard chip", "var(--hb-hard)", ["var(--hb-hard-bg)", "var(--hb-card)", "var(--hb-bg)"], TEXT),
    ("home band hard bar segment", "var(--hb-hard)", ["var(--hb-card)", "var(--hb-bg)"], UI),
    ("home band level chip", "var(--hb-link)", ["var(--hb-soft)", "var(--hb-card)", "var(--hb-bg)"], TEXT),
    ("home band button", "var(--hb-on-accent)", ["var(--hb-accent)"], TEXT),
    ("home band focus ring", "var(--hb-accent)", ["var(--hb-bg)"], UI),
    ("interview bar text", "#ffffff", [TOAST], TEXT),
    ("interview clock past the target", "var(--md-accent-fg-color)", [TOAST], TEXT),
    ("interview confidence question", "var(--md-default-fg-color)", ["var(--md-accent-fg-color--transparent)", PAGE], TEXT),
    ("interview summary secondary text", "var(--md-default-fg-color--light)", [CARD, PAGE], TEXT),
    ("builder text on the hero", "rgba(255, 255, 255, 0.82)", ["rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("builder card id", "var(--site-logo-v)", ["rgba(255, 255, 255, 0.12)", "rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("builder card minutes", "rgba(255, 255, 255, 0.82)", ["rgba(255, 255, 255, 0.12)", "rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("builder card, easy", "var(--hh-easy)", ["rgba(255, 255, 255, 0.12)", "rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("builder card, medium", "var(--hh-medium)", ["rgba(255, 255, 255, 0.12)", "rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("builder card, hard", "var(--hh-hard)", ["rgba(255, 255, 255, 0.12)", "rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("builder card edge, picked", "var(--site-logo-v)", ["rgba(255, 255, 255, 0.05)", TOAST], UI),
    ("builder title line", "#ffffff", ["rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("builder option, off", "#ffffff", ["rgba(255, 255, 255, 0.1)", "rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("wave viewer cursor A", "var(--md-typeset-a-color)", [CARD, PAGE], UI),
    ("wave viewer cursor B and knob edge", "var(--site-mark-color)", [CARD, PAGE], UI),
    ("wave viewer knob A letter", "var(--md-default-bg-color)", ["var(--md-typeset-a-color)"], TEXT),
    ("wave viewer knob B letter", "#1b2a4a", ["var(--md-accent-fg-color)"], TEXT),
    ("wave viewer dimension label", "var(--md-default-bg-color)", ["var(--md-default-fg-color)"], TEXT),
    ("wave viewer button, on", "var(--md-typeset-a-color)", ["var(--site-primary-soft)", CARD], TEXT),
    ("steps beside a figure, the active step", "var(--md-default-fg-color)", ["var(--md-accent-fg-color--transparent)", CARD, PAGE], TEXT),
    ("steps beside a figure, a lit arc or state", "var(--site-mark-color)", [CARD, PAGE], UI),
    ("steps beside a figure, a lit arc's bit", "var(--site-label-color)", [CARD, PAGE], TEXT),
    ("part bar, the current part", "var(--md-primary-fg-color--dark)", ["var(--md-accent-fg-color)"], TEXT),
    ("quick jump row, chosen", "var(--md-default-fg-color)", ["var(--site-primary-soft)", CARD], TEXT),
    ("quick jump match, chosen", "var(--md-typeset-a-color)", ["var(--site-primary-soft)", CARD], TEXT),
    ("quick jump details, chosen", "var(--md-default-fg-color)", ["var(--site-primary-soft)", CARD], TEXT),
    ("quick jump details", "var(--md-default-fg-color--light)", [CARD], TEXT),
    ("quick jump id, chosen", "var(--site-label-color)", ["var(--site-primary-soft)", CARD], TEXT),
    ("my map, a solved square", "var(--diff-easy)", [CARD, PAGE], UI),
    ("my map, a started square", "var(--site-mark-color)", [CARD, PAGE], UI),
    ("metro line 1 badge text", "var(--mm-on)", ["var(--mm-1)"], TEXT),
    ("metro line 1 on the map", "var(--mm-1)", [CARD, PAGE], UI),
    ("metro line 2 badge text", "var(--mm-on)", ["var(--mm-2)"], TEXT),
    ("metro line 2 on the map", "var(--mm-2)", [CARD, PAGE], UI),
    ("metro line 3 badge text", "var(--mm-on)", ["var(--mm-3)"], TEXT),
    ("metro line 3 on the map", "var(--mm-3)", [CARD, PAGE], UI),
    ("metro line 4 badge text", "var(--mm-on)", ["var(--mm-4)"], TEXT),
    ("metro line 4 on the map", "var(--mm-4)", [CARD, PAGE], UI),
    ("metro line 5 badge text", "var(--mm-on)", ["var(--mm-5)"], TEXT),
    ("metro line 5 on the map", "var(--mm-5)", [CARD, PAGE], UI),
    ("metro line 6 badge text", "var(--mm-on)", ["var(--mm-6)"], TEXT),
    ("metro line 6 on the map", "var(--mm-6)", [CARD, PAGE], UI),
    ("metro line 7 badge text", "var(--mm-on)", ["var(--mm-7)"], TEXT),
    ("metro line 7 on the map", "var(--mm-7)", [CARD, PAGE], UI),
    ("metro line 8 badge text", "var(--mm-on)", ["var(--mm-8)"], TEXT),
    ("metro line 8 on the map", "var(--mm-8)", [CARD, PAGE], UI),
    ("metro line 9 badge text", "var(--mm-on)", ["var(--mm-9)"], TEXT),
    ("metro line 9 on the map", "var(--mm-9)", [CARD, PAGE], UI),
    ("metro line 10 badge text", "var(--mm-on)", ["var(--mm-10)"], TEXT),
    ("metro line 10 on the map", "var(--mm-10)", [CARD, PAGE], UI),
    ("metro line 11 badge text", "var(--mm-on)", ["var(--mm-11)"], TEXT),
    ("metro line 11 on the map", "var(--mm-11)", [CARD, PAGE], UI),
    ("metro line 12 badge text", "var(--mm-on)", ["var(--mm-12)"], TEXT),
    ("metro line 12 on the map", "var(--mm-12)", [CARD, PAGE], UI),
    ("metro line 13 badge text", "var(--mm-on)", ["var(--mm-13)"], TEXT),
    ("metro line 13 on the map", "var(--mm-13)", [CARD, PAGE], UI),
    ("metro interchange ring", "var(--mm-ink)", [CARD, PAGE], UI),
    ("tag graph link", "var(--tg-edge)", [CARD, PAGE], UI),
    ("tag graph circle edge", "var(--tg-stroke)", ["var(--tg-fill)"], UI),
    ("tag graph count", "var(--md-default-fg-color)", ["var(--tg-fill)"], TEXT),
    ("tag graph picked count", "var(--tg-on-accent)", ["var(--md-accent-fg-color)"], TEXT),
    ("level band text fg", "var(--lst-fg)", ["var(--lst-band-bg)"], TEXT),
    ("level band text fg-soft", "var(--lst-fg-soft)", ["var(--lst-band-bg)"], TEXT),
    ("level band text fg-mute", "var(--lst-fg-mute)", ["var(--lst-band-bg)"], TEXT),
    ("level band easy chip", "var(--lst-easy)", ["var(--lst-easy-bg)", "var(--lst-band-bg)"], TEXT),
    ("level band easy bar segment", "var(--lst-easy)", ["var(--lst-band-bg)"], UI),
    ("level band medium chip", "var(--lst-medium)", ["var(--lst-medium-bg)", "var(--lst-band-bg)"], TEXT),
    ("level band medium bar segment", "var(--lst-medium)", ["var(--lst-band-bg)"], UI),
    ("level band hard chip", "var(--lst-hard)", ["var(--lst-hard-bg)", "var(--lst-band-bg)"], TEXT),
    ("level band hard bar segment", "var(--lst-hard)", ["var(--lst-band-bg)"], UI),
    ("level band progress bar", "var(--md-accent-fg-color)", ["var(--lst-track)", "var(--lst-band-bg)"], UI),
    ("level band icon", "var(--md-accent-fg-color)", ["var(--lst-panel)", "var(--lst-band-bg)"], UI),
    ("solved check in a row", "var(--lst-solved-fg)", ["var(--lst-solved-bg)"], UI),
    ("solved disc in a row", "var(--lst-solved-bg)", ["var(--site-primary-soft)", "var(--site-surface)"], UI),
    ("favourite star in a hovered row", "var(--site-mark-color)", ["var(--site-primary-soft)", "var(--site-surface)"], UI),
    ("kind tile in a row", "var(--lst-kind-fg)", ["var(--site-primary-soft)", "var(--site-surface)"], UI),
    ("question link in a hovered row", "var(--md-typeset-a-color)", ["var(--site-primary-soft)", "var(--site-surface)"], TEXT),
    ("row stripe easy", "var(--diff-easy)", ["var(--site-surface)"], UI),
    ("row stripe medium", "var(--diff-medium)", ["var(--site-surface)"], UI),
    ("row stripe hard", "var(--diff-hard)", ["var(--site-surface)"], UI),
    ("code window title", "var(--md-default-fg-color)", ["var(--qw-bar)"], TEXT),
    ("part circle letter", "var(--md-default-fg-color)", [PAGE], TEXT),
    ("part circle passed", "var(--qp-ink)", ["var(--md-accent-fg-color)"], TEXT),
    ("part circle solved", "var(--md-default-bg-color)", ["var(--diff-easy)"], TEXT),
    ("negative digit, current conversion row", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s1) 14%, var(--md-default-bg-color))", CARD, PAGE], TEXT),
    ("explanation step chip, lit", "var(--md-default-fg-color)", ["var(--md-accent-fg-color--transparent)", PAGE], TEXT),
    ("explanation step chip", "var(--viz-text)", [PAGE], TEXT),
    ("ladder cell label, a term", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s1) 18%, var(--md-default-bg-color))"], TEXT),
    *[(f"code {k}", f"var(--md-code-hl-{k}-color)", ["var(--md-code-hl-color--light)", "var(--md-code-bg-color)"], TEXT)
      for k in ("function", "special", "constant", "number", "string", "variable", "generic", "operator")],
    ("orange text, highlighted row", "var(--viz-s2-text)", ["var(--md-code-bg-color)"], TEXT),
    ("body text on a card", "var(--md-default-fg-color)", ["var(--site-surface)"], TEXT),
    ("trap group title", "var(--adm-trap)", ["var(--site-surface)"], TEXT),
    ("trap number", "var(--site-surface)", ["var(--adm-trap)"], TEXT),
    ("footer text", "var(--md-footer-fg-color)", ["var(--md-footer-bg-color)"], TEXT),
    ("footer secondary text", "var(--md-footer-fg-color--light)", ["var(--md-footer-bg-color--dark)"], TEXT),
    # round M (13-motion.css): the logo's check, the hero's live example, the footer's
    # counts, the question header's topic chips and the 404 page's waveform
    ("logo check on the header", "var(--site-logo-v)", ["var(--md-primary-fg-color)"], UI),
    ("hero example bits", "rgba(255, 255, 255, 0.72)", ["rgba(255, 255, 255, 0.08)", "rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("hero example title", "rgba(255, 255, 255, 0.78)", ["rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("amber on the navy card", "var(--md-accent-fg-color)", ["rgba(255, 255, 255, 0.05)", TOAST], TEXT),
    ("footer count", "var(--md-footer-fg-color--light)", ["rgba(255, 255, 255, 0.1)", "var(--md-footer-bg-color--dark)"], TEXT),
    ("topic chip", "var(--md-default-fg-color--light)", [CARD, PAGE], TEXT),
    ("404 unknown state", "var(--site-x-state)", [TOAST], TEXT),
    ("404 signal names", "rgba(255, 255, 255, 0.62)", [TOAST], TEXT),
    ("edit link", "var(--md-default-fg-color--light)", [PAGE], TEXT),
    ("tag count on a tag chip", "var(--md-default-fg-color--light)", ["var(--site-surface)"], TEXT),
    # the tutorial video (20-video.css): the chapter link in a solution, the dialog's navy
    ("video chapter link", "var(--md-typeset-a-color)", ["var(--site-surface)"], TEXT),
    ("video chapter time", "var(--md-default-fg-color--light)", ["var(--site-surface)"], TEXT),
    ("video dialog title", "var(--vd-ink)", ["var(--vd-bg)"], TEXT),
    ("video poster kicker", "var(--vd-accent)", ["var(--vd-bg)"], TEXT),
    ("video poster start line", "var(--vd-ink-2)", ["var(--vd-glow)", "var(--vd-bg)"], TEXT),
    ("video chapter button", "var(--vd-ink-2)", ["var(--vd-bg)"], TEXT),
    ("video chapter button, hovered", "var(--vd-ink)", ["var(--vd-soft)", "var(--vd-bg)"], TEXT),
    ("video chapter button, chosen", "var(--vd-on-accent)", ["var(--vd-accent)"], TEXT),
    ("video note", "var(--vd-ink-3)", ["var(--vd-bg)"], TEXT),
    ("video play disc", "var(--vd-accent)", ["var(--vd-glow)", "var(--vd-bg)"], UI),
    ("video play triangle", "var(--vd-on-accent)", ["var(--vd-accent)"], UI),
    ("video focus ring", "var(--vd-accent)", ["var(--vd-bg)"], UI),
    ("in-place cells (0072 to 0075), tint c1", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 24%, var(--md-default-bg-color))"], TEXT),
    ("in-place cells (0072 to 0075), tint c2", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 24%, var(--md-default-bg-color))"], TEXT),
    ("in-place cells (0072 to 0075), tint c3", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 24%, var(--md-default-bg-color))"], TEXT),
    ("in-place cells (0072 to 0075), tint c4", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s4) 24%, var(--md-default-bg-color))"], TEXT),
    ("in-place cells (0072 to 0075), tint c5", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s5) 24%, var(--md-default-bg-color))"], TEXT),
    ("in-place cells, a cell or an index", "var(--viz-text)", [PAGE], TEXT),
    ("in-place cells, the mark of a step", "var(--site-mark-color)", [PAGE], UI),
    ("bitmatrix box, a bit that is on", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 14%, var(--md-default-bg-color))"], TEXT),
    ("bitmatrix box, a bit that is off", "var(--viz-text)", [CARD], TEXT),
    # the circuit layer (22-circuit.css): the difficulty word beside its LEDs, with no pill now
    *[(f"difficulty word beside its LEDs, {d}", f"var(--diff-{d})", [CARD, PAGE], TEXT) for d in ("easy", "medium", "hard")],
    *[(f"level band difficulty word beside its LEDs, {d}", f"var(--lst-{d})", ["var(--lst-band-bg)"], TEXT) for d in ("easy", "medium", "hard")],
    ("question chip, a lit bit on its body", "var(--md-accent-fg-color)",
     [{"default": "var(--md-primary-fg-color)", "slate": "var(--md-primary-fg-color--light)"}], UI),
    ("question chip label DVQ-<id> in the header", "var(--md-default-fg-color--light)", [CARD], TEXT),
    # polish (fork A): one action colour in the boxes and the run panel (23-polish.css)
    ("action button, filled", "var(--act-ink)", ["var(--act)"], TEXT),
    ("action button, filled, hovered", "var(--act-ink)", ["var(--act-hover)"], TEXT),
    ("action button, outlined, in a box", "var(--act-line)", [CARD, PAGE], TEXT),
    ("action button, outlined, on the page (run panel)", "var(--act-line)", [PAGE], TEXT),
    ("action button, outlined, hovered", "var(--act-line)", ["var(--act-tint)", CARD], TEXT),
    ("action button, the filled one's edge on the box", "var(--act)", [CARD], UI),
    ("speed button pressed", "var(--act-line)", ["var(--act-tint)", "var(--md-default-bg-color)"], TEXT),
    ("an icon button's name under it on a phone", "var(--md-default-fg-color--light)", [CARD], TEXT),
    # living (fork B, 24-living.css): the footer's board line (REV, the date and the count)
    ("footer board line", "var(--md-footer-fg-color--light)", ["var(--md-footer-bg-color--dark)"], TEXT),
    # figures (fork C): the XOR bits of 0002, the passes of 0003, the handshake contract of 0038 (25-figures-c.css)
    ("figures C, a digit on a cell of 1 or of the sorted part", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("figures C, the rule number on its badge", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 22%, var(--md-default-bg-color))"], TEXT),
    ("figures C, the name of the ack state", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))"], TEXT),
    ("figures C, req and ack values in the ack state", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))"], TEXT),
    ("figures C, the frame of a changed cell", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], UI),
    # 0083 jugs (stylesheets/questions/0083-jugs.css): the jugs, the grid of the states and the jugs / jugs3 boxes
    ("0083 jugs, the amount on the water", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 32%, var(--md-default-bg-color))"], TEXT),
    ("0083 jugs, the amount in an empty jug or a name", "var(--viz-ink)", [CARD, PAGE], TEXT),
    ("0083 jugs, a capacity under a jug", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0083 jugs, the frame of the jug a step changed", "var(--viz-s2-text)", [CARD, PAGE], UI),
    ("0083 jugs, the outline of a jug", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 32%, var(--md-default-bg-color))"], UI),
    ("0083 jugs, a reachable state", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0083 jugs, a state with the target", "var(--viz-s3)", [CARD, PAGE], UI),
    ("0083 jugs, a state never reached", "var(--viz-text)", [CARD, PAGE], UI),
    ("0083 jugs, the longer plan on the grid", "var(--viz-s4)", [CARD, PAGE], UI),
    ("0083 jugs, the shortest-plan tag", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))", CARD, PAGE], TEXT),
    # 0084 LIS (stylesheets/questions/0084-lis.css): the figures and the box of the longest increasing subsequence
    ("0084 LIS, a value on the LIS", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("0084 LIS, a value compared or appended", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("0084 LIS, a value not compared (a[j] >= a[i])", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 10%, var(--md-default-bg-color))"], TEXT),
    ("0084 LIS, a value in the search range", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s4) 16%, var(--md-default-bg-color))"], TEXT),
    ("0084 LIS, an index, a row name or tail_at", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0084 LIS, lo, hi and k under tails", "var(--viz-s4-text)", [CARD, PAGE], TEXT),
    ("0084 LIS, the frame of a[i] on a value on the LIS", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], UI),
    ("0084 LIS, the frame of mid in the search range", "var(--viz-s4)", ["color-mix(in srgb, var(--viz-s4) 16%, var(--md-default-bg-color))"], UI),
    ("0084 LIS, a prev or parent arc on the box", "var(--viz-text)", [CARD], UI),
    ("0084 LIS, the LIS's arc on the box", "var(--viz-s1)", [CARD], UI),
    # 0085 self-describing (stylesheets/questions/0085-selfdesc.css): the digit tables of the figures and the box
    ("0085 self-describing, a digit d[i]", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("0085 self-describing, a count that matches", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("0085 self-describing, a count that does not match", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))"], TEXT),
    ("0085 self-describing, the frame of a count that does not match", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))"], UI),
    ("0085 self-describing, a value cut by the search", "var(--viz-s2-text)", [CARD, PAGE], TEXT),
    ("0085 self-describing, the positions and row names", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0085 self-describing, the base shown in the strip", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s4) 18%, var(--md-default-bg-color))"], TEXT),
    ("0085 self-describing, the frame of the base shown", "var(--viz-s4)", ["color-mix(in srgb, var(--viz-s4) 18%, var(--md-default-bg-color))"], UI),
    # 0086 chameleons (stylesheets/questions/0086-chameleons.css): red is --viz-s5, green --viz-s3, blue --viz-s1
    ("0086 chameleons, a count on its disc", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s5) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 18%, var(--md-default-bg-color))"], TEXT),
    ("0086 chameleons, a count and its residue in the box", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s5) 12%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 12%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 12%, var(--md-default-bg-color))"], TEXT),
    ("0086 chameleons, a chameleon's colour as a mark", "var(--viz-s5)", [CARD, PAGE], UI),
    ("0086 chameleons, green as a mark", "var(--viz-s3)", [CARD, PAGE], UI),
    ("0086 chameleons, blue as a mark", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0086 chameleons, a reachable state", "var(--viz-ink)", [CARD, PAGE], UI),
    ("0086 chameleons, a state never reached", "var(--viz-text)", [CARD, PAGE], UI),
    ("0086 chameleons, the start ring", "var(--viz-s2-text)", [CARD, PAGE], UI),
    ("0086 chameleons, the path so far", "var(--viz-s2)", [CARD, PAGE], UI),
    ("0086 chameleons, the shortest-plan tag", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))"], TEXT),
    # 0087 lights out (stylesheets/questions/0087-lights.css): the boards of the figures and of the box
    ("0087 lights out, the rim of a light that is on", "var(--viz-ink)", [CARD, PAGE, "var(--md-accent-fg-color)"], UI),
    ("0087 lights out, the ring of a light that is off", "var(--viz-text)", [CARD, PAGE], UI),
    ("0087 lights out, a press", "var(--viz-s1)", [CARD, PAGE, "color-mix(in srgb, var(--viz-s3) 16%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))"], UI),
    ("0087 lights out, the press of the step", "var(--viz-s2-text)", [CARD, PAGE, "color-mix(in srgb, var(--viz-s3) 16%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))"], UI),
    ("0087 lights out, a quiet pattern", "var(--viz-s4)", [CARD, PAGE], UI),
    ("0087 lights out, a light's number, a caption, the equals sign", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0087 lights out, a count under a cell", "var(--viz-ink)", [CARD, PAGE], TEXT),
    ("0087 lights out, a press of the solution in the system", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    # 0088 ducci (stylesheets/questions/0088-ducci.css): the circle of numbers, the parity rows, the box's chart
    ("0088 ducci, a number on the circle", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 16%, var(--md-default-bg-color))"], TEXT),
    ("0088 ducci, the rim of a number", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0088 ducci, the rim of a number in the cycle", "var(--viz-s4)", [CARD, PAGE], UI),
    ("0088 ducci, a difference on an edge", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 18%, var(--md-default-bg-color))"], TEXT),
    ("0088 ducci, the frame of a difference", "var(--viz-s2-text)", [CARD, PAGE], UI),
    ("0088 ducci, an odd cell of the parity rows", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0088 ducci, the frame of an all-even row", "var(--viz-s3-text)", [CARD, PAGE], UI),
    ("0088 ducci, a panel title, a round number, a chart label", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0088 ducci, a bar of the round where all turned even", "var(--viz-s3)", [CARD, PAGE], UI),
    # 0089 frobenius (stylesheets/questions/0089-frobenius.css): the amount tables of the figures and of the box
    ("0089 frobenius, a payable amount", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("0089 frobenius, an amount that cannot be paid", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))"], TEXT),
    ("0089 frobenius, the frame of the largest amount that cannot be paid", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))"], UI),
    ("0089 frobenius, the frame of a payable amount of the run", "var(--viz-s3-text)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))", CARD, PAGE], UI),
    ("0089 frobenius, the head of a column", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("0089 frobenius, the frame of a head and of the best so far", "var(--viz-s1)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))", CARD, PAGE], UI),
    ("0089 frobenius, the column settled now and the typed amount", "var(--viz-ink)", [CARD, PAGE], UI),
    ("0089 frobenius, an amount not settled yet, the remainders", "var(--viz-text)", [CARD, PAGE], TEXT),
    # 0090 pancakes (stylesheets/questions/0090-pancake.css): the stacks of the figures and of the box
    ("0090 pancakes, a size on a pancake", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))"], TEXT),
    ("0090 pancakes, a size on a pancake in place", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 28%, var(--md-default-bg-color))"], TEXT),
    ("0090 pancakes, the edge of a pancake", "var(--viz-s2-text)", [CARD, PAGE], UI),
    ("0090 pancakes, the burnt side on a pancake", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))"], UI),
    ("0090 pancakes, the frame of a flip", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0090 pancakes, the hint", "var(--viz-s4)", [CARD, PAGE], UI),
    ("0090 pancakes, the plate", "var(--viz-text)", [CARD, PAGE], UI),
    # 0091 chomp (stylesheets/questions/0091-chomp.css): the chocolate bars of the figures and of the box
    ("0091 chomp, the edge of a square of chocolate", "var(--viz-s2-text)", [CARD, PAGE], UI),
    ("0091 chomp, the edge of the poisoned square", "var(--viz-s5)", [CARD, PAGE], UI),
    ("0091 chomp, the cross on the poisoned square", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s5) 30%, var(--md-default-bg-color))"], UI),
    ("0091 chomp, the square chosen on chocolate", "var(--viz-s1)", ["color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))"], UI),
    ("0091 chomp, a winning move on chocolate", "var(--viz-s3-text)", ["color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))"], UI),
    ("0091 chomp, a losing move on chocolate", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))"], UI),
    ("0091 chomp, the squares a move ate", "var(--viz-text)", [CARD, PAGE], UI),
    ("0091 chomp, a column letter or a row number", "var(--viz-text)", [CARD, PAGE], TEXT),
    # 0092 circle (stylesheets/questions/0092-circle.css): the disc cut into regions, in the figures and the box
    ("0092 circle, a region number on any of the six tints", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s4) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s5) 20%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-text) 16%, var(--md-default-bg-color))"], TEXT),
    ("0092 circle, a chord over any region", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s4) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s5) 20%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-text) 16%, var(--md-default-bg-color))"], UI),
    ("0092 circle, the new chord over any region", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s1) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s4) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s5) 20%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-text) 16%, var(--md-default-bg-color))"], UI),
    ("0092 circle, a ring where three chords meet", "var(--viz-s5)", ["color-mix(in srgb, var(--viz-s1) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s4) 24%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s5) 20%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-text) 16%, var(--md-default-bg-color))"], UI),
    ("0092 circle, a point on the circle", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0092 circle, the number of a point", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0092 circle, the dashed bar of the powers of 2", "var(--viz-s2-text)", [CARD, PAGE], UI),
    # 0093 matching (stylesheets/questions/0093-match.css): the figure and the box's preference tables
    ("0093 matching, an entry that holds or a pair now", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("0093 matching, a refused entry", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))"], TEXT),
    ("0093 matching, an entry, a name, a label in the figure", "var(--viz-ink)", [CARD, PAGE], TEXT),
    ("0093 matching, a candidate's label in the figure", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("0093 matching, the role and the ranks over the tables", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0093 matching, the frame of the proposal of the step", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0093 matching, a final pair and a held frame", "var(--viz-s3)", [CARD, PAGE], UI),
    ("0093 matching, a refused proposal in the figure", "var(--viz-s2)", [CARD, PAGE], UI),
    ("0093 matching, the dashed frame of an entry picked for a swap", "var(--viz-ink)", [CARD, PAGE], UI),
    # 0094 credit walk (stylesheets/questions/0094-creditwalk.css): the walk, the two curves and the tags
    ("0094 credit walk, the wall N and the curve of the chance to fill", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0094 credit walk, the wall 0 and the curve of the expected cycles", "var(--viz-s2)", [CARD, PAGE], UI),
    ("0094 credit walk, the walk and the fair curve", "var(--viz-ink)", [CARD, PAGE], UI),
    ("0094 credit walk, the ring of what the runs measured", "var(--viz-s3)", [CARD, PAGE], UI),
    ("0094 credit walk, the tag \"filled\"", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("0094 credit walk, the tag \"emptied\"", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 22%, var(--md-default-bg-color))"], TEXT),
    # 0095 soldiers (stylesheets/questions/0095-soldiers.css): the boards of the figures and of the box
    ("0095 soldiers, a soldier on the ground", "var(--viz-s1)", ["color-mix(in srgb, var(--viz-s2) 12%, var(--md-default-bg-color))"], UI),
    ("0095 soldiers, a soldier above the line", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0095 soldiers, the soldier that just jumped", "var(--viz-s2-text)", ["color-mix(in srgb, var(--viz-s2) 12%, var(--md-default-bg-color))", CARD, PAGE], UI),
    ("0095 soldiers, a cell a jump emptied", "var(--viz-text)", ["color-mix(in srgb, var(--viz-s2) 12%, var(--md-default-bg-color))", CARD, PAGE], UI),
    ("0095 soldiers, the target", "var(--viz-s5)", [CARD, PAGE], UI),
    ("0095 soldiers, the soldier chosen", "var(--viz-s5)", ["color-mix(in srgb, var(--viz-s2) 12%, var(--md-default-bg-color))", CARD, PAGE], UI),
    ("0095 soldiers, where it can jump", "var(--viz-s3-text)", ["color-mix(in srgb, var(--viz-s2) 12%, var(--md-default-bg-color))", CARD, PAGE], UI),
    ("0095 soldiers, the line", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 12%, var(--md-default-bg-color))", CARD, PAGE], UI),
    ("0095 soldiers, a row number or a caption", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0095 soldiers, a distance above the line", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0095 soldiers, a distance on weight 0", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 48%, var(--md-default-bg-color))"], TEXT),
    ("0095 soldiers, a distance on weight 1", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 36%, var(--md-default-bg-color))"], TEXT),
    ("0095 soldiers, a distance on weight 2", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 26%, var(--md-default-bg-color))"], TEXT),
    ("0095 soldiers, a distance on weight 3", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 18%, var(--md-default-bg-color))"], TEXT),
    ("0095 soldiers, a distance on weight 4", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 12%, var(--md-default-bg-color))"], TEXT),
    ("0095 soldiers, a distance on weight 5", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 7%, var(--md-default-bg-color))"], TEXT),
    ("0095 soldiers, a distance on weight 6", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 4%, var(--md-default-bg-color))"], TEXT),
    ("0095 soldiers, the meter's bar", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0095 soldiers, the meter's mark of 1, above and below the bar", "var(--viz-ink)", [CARD, PAGE], UI),
    # 0096 kelly (stylesheets/questions/0096-kelly.css): the curve g(f), the median, the line W0 e^(g t)
    ("0096 kelly, the curve g(f) and the best fraction f*", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0096 kelly, the median of the paths and the current f", "var(--viz-ink)", [CARD, PAGE], UI),
    ("0096 kelly, the line W0 e^(g t) and the zero of the growth", "var(--viz-s2)", [CARD, PAGE], UI),
    ("0096 kelly, half Kelly", "var(--viz-s3)", [CARD, PAGE], UI),
    # 0097 isqrt (stylesheets/questions/0097-isqrt.css): the step as areas, the bit rows, the box's table
    ("0097 isqrt, a number on r² (the old square)", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 26%, var(--md-default-bg-color))"], TEXT),
    ("0097 isqrt, a number on a trial rectangle", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 26%, var(--md-default-bg-color))"], TEXT),
    ("0097 isqrt, a number on the trial's small square", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 46%, var(--md-default-bg-color))"], TEXT),
    ("0097 isqrt, a number on a trial that does not fit", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 32%, var(--md-default-bg-color))"], TEXT),
    ("0097 isqrt, the edge of r²", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0097 isqrt, the edge of the trial", "var(--viz-s3)", [CARD, PAGE], UI),
    ("0097 isqrt, the edge of a trial that does not fit", "var(--viz-s2)", [CARD, PAGE], UI),
    ("0097 isqrt, the dashed square of side root n", "var(--viz-ink)", [CARD, PAGE], UI),
    ("0097 isqrt, a bit of the root", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("0097 isqrt, the bit of b²", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("0097 isqrt, a bit not decided yet", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0097 isqrt, the row of the step just decided", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 8%, var(--md-default-bg-color))", CARD, PAGE], TEXT),
    ("0097 isqrt, the step's yes", "var(--viz-s3-text)", [CARD, PAGE], TEXT),
    ("0097 isqrt, the step's no", "var(--viz-s2-text)", [CARD, PAGE], TEXT),
    # 0098 luhn (stylesheets/questions/0098-luhn.css): the digit strips and the box's maps
    ("0098 luhn, a digit in a doubled place", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("0098 luhn, a digit in a plain place", "var(--viz-ink)", [CARD, PAGE], TEXT),
    ("0098 luhn, a digit in the colliding columns 0 and 9", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))"], TEXT),
    ("0098 luhn, the edge of a doubled place", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0098 luhn, the frame of the chosen place and of the last error's cell", "var(--viz-ink)", [CARD, PAGE, "color-mix(in srgb, var(--viz-s3) 18%, var(--md-default-bg-color))"], UI),
    ("0098 luhn, the × of an error that slips by", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s2) 40%, var(--md-default-bg-color))"], TEXT),
    ("0098 luhn, the digits around a map", "var(--viz-ink)", [CARD, PAGE], TEXT),
    # 0099 iban (stylesheets/questions/0099-iban.css): the digit tables, the boxes and part b's state diagrams
    ("0099 iban, a digit or a remainder", "var(--viz-ink)", [CARD, PAGE], TEXT),
    ("0099 iban, a digit of a letter", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))"], TEXT),
    ("0099 iban, a check digit", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("0099 iban, the first four characters in the box", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s4) 26%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s4) 22%, var(--md-default-bg-color))"], TEXT),
    ("0099 iban, a remainder not read yet", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0099 iban, the frame of the last remainder", "var(--viz-s3-text)", [CARD, PAGE], UI),
    ("0099 iban, the frame of a last remainder that is not 1", "var(--viz-s2-text)", [CARD, PAGE], UI),
    ("0099 iban, the frame of the step and of the chosen place", "var(--viz-ink)", [CARD, PAGE, "color-mix(in srgb, var(--viz-s4) 26%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], UI),
    ("0099 iban, the edges of the letter and check-digit cells", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0099 ibanhw, a state, a label, a block's text, a bit", "var(--viz-ink)", [CARD, PAGE, "color-mix(in srgb, var(--viz-s1) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 22%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 10%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 16%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 18%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 20%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 22%, var(--md-default-bg-color))"], TEXT),
    ("0099 ibanhw, an edge, a wire, a block's second line, a register's name", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0099 ibanhw, a value in the table of signals", "var(--viz-ink)", [CARD, PAGE, "color-mix(in srgb, var(--viz-ink) 6%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-ink) 4%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 18%, var(--md-default-bg-color))"], TEXT),
    ("0099 ibanhw, a clock's number in the table", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0099 ibanhw, the frame of a register and the edge a digit took", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0099 ibanhw, the frame of a stage and of the head's digits", "var(--viz-s2)", [CARD, PAGE], UI),
    ("0099 ibanhw, the frame of the start and of the output", "var(--viz-s3)", [CARD, PAGE], UI),
    ("0099 iban, an error caught", "var(--viz-s3-text)", [CARD, PAGE], TEXT),
    ("0099 iban, an error that slips", "var(--viz-s2-text)", [CARD, PAGE], TEXT),
    # 0022 latpaths (stylesheets/questions/0022-latpaths.css): the counts on their tints, the small boards and the box
    ("0022 latpaths, a count on its tint", "var(--viz-ink)", [CARD, PAGE] + [f"color-mix(in srgb, var(--viz-s1) {p}%, var(--md-default-bg-color))" for p in (8, 18, 30, 44)], TEXT),
    ("0022 latpaths, a cell no path reaches", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0022 latpaths, S and T on their tint", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 8%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 44%, var(--md-default-bg-color))"], TEXT),
    ("0022 latpaths, the path on a small board", "var(--viz-ink)", [CARD, PAGE, "color-mix(in srgb, var(--viz-s1) 30%, var(--md-default-bg-color))"], UI),
    ("0022 latpaths, the path line over the tints", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-s1) 44%, var(--md-default-bg-color))"], UI),
    # 0100 stairs (stylesheets/questions/0100-stairs.css): the staircases and the box
    ("0100 stairs, a count on a stair", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 7%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 30%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 26%, var(--md-default-bg-color))"], TEXT),
    ("0100 stairs, a stair's number in the box", "var(--viz-text)", ["color-mix(in srgb, var(--viz-ink) 7%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 30%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 26%, var(--md-default-bg-color))"], TEXT),
    ("0100 stairs, the cross of a broken stair", "var(--viz-ink)", ["color-mix(in srgb, var(--viz-ink) 22%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-ink) 12%, var(--md-default-bg-color))"], TEXT),
    ("0100 stairs, the edges of the picked stair and of the stairs below it", "var(--viz-s1)", [CARD, PAGE], UI),
    ("0100 stairs, the arrows into the last stair", "var(--viz-s3-text)", [CARD, PAGE], UI),
    ("0100 stairs, a jump size that is on", "var(--act-ink)", ["var(--act)"], TEXT),
    # 0037 editdist (stylesheets/questions/0037-editdist.css): the tables of the prefixes and the box
    ("0037 editdist, a value on the tint of its step", "var(--viz-ink)", [CARD, PAGE, "color-mix(in srgb, var(--viz-ink) 12%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s2) 30%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s3) 30%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s4) 30%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 30%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-s1) 16%, var(--md-default-bg-color))", "color-mix(in srgb, var(--viz-ink) 6%, var(--md-default-bg-color))"], TEXT),
    ("0037 editdist, the indices of the prefixes", "var(--viz-text)", [CARD, PAGE], TEXT),
    ("0037 editdist, the edges of the steps of the path", "var(--viz-s2)", [CARD, PAGE], UI),
    ("0037 editdist, the edges of an extra packet", "var(--viz-s3)", [CARD, PAGE], UI),
    ("0037 editdist, the edges of a changed packet", "var(--viz-s4)", [CARD, PAGE], UI),
    ("0037 editdist, the edges of a swap and of the neighbours that give the minimum", "var(--viz-s1)", [CARD, PAGE], UI),
]

BLOCK = re.compile(r"([^{}]+)\{([^{}]*)\}")
PROP = re.compile(r"(--[\w-]+)\s*:\s*([^;]+)")


def blocks(css: str, selector: str) -> dict[str, str]:
    """The custom properties of every rule whose whole selector list contains selector."""
    out: dict[str, str] = {}
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for sel, body in BLOCK.findall(css):
        if selector in [s.strip().replace('"', "") for s in sel.split(",")]:
            out.update({k: v.strip() for k, v in PROP.findall(body)})
    return out


def material_css() -> str:
    import material
    folder = Path(material.__file__).parent / "templates" / "assets" / "stylesheets"
    return "".join(p.read_text() for p in sorted(folder.glob("*.min.css")))


def schemes() -> dict[str, dict[str, str]]:
    mat, extra = material_css(), "\n".join(p.read_text(encoding="utf-8") for p in STYLES)
    base = {**blocks(mat, ":root"), **blocks(mat, "[data-md-color-scheme=default]")}
    light = {**base, **blocks(extra, ":root"), **blocks(extra, "[data-md-color-scheme=default]")}
    dark = {**base, **blocks(mat, "[data-md-color-scheme=slate]"), **blocks(extra, ":root"),
            **blocks(extra, "[data-md-color-scheme=slate]")}
    return {"default": light, "slate": dark}


# --- colours: (r, g, b, a) with r, g, b in 0..1 -------------------------------------------

def resolve(value: str, props: dict[str, str], depth: int = 0) -> str:
    if depth > 20:
        raise ValueError(f"var() loop in {value}")
    def sub(m: re.Match) -> str:
        name, fallback = m.group(1), m.group(2)
        if name in props:
            return resolve(props[name], props, depth + 1)
        if fallback is not None:
            return fallback.strip()
        raise KeyError(name)
    while "var(" in value:
        value = re.sub(r"var\((--[\w-]+)(?:\s*,\s*([^()]*))?\)", sub, value)
    return value


def split_args(s: str) -> list[str]:
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
            continue
        depth += ch == "("
        depth -= ch == ")"
        cur += ch
    return out + [cur.strip()]


def num(s: str, scale: float = 1.0) -> float:
    s = s.strip()
    if s.endswith("%"):
        return float(s[:-1]) / 100
    if s.endswith("deg"):
        return float(s[:-3])
    return float(s) / scale


def parse(c: str) -> tuple[float, float, float, float]:
    c = c.strip()
    if c == "transparent":
        return (0.0, 0.0, 0.0, 0.0)
    if c.startswith("#"):
        h = c[1:]
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        vals = [int(h[i:i + 2], 16) / 255 for i in range(0, len(h), 2)]
        return (*vals[:3], vals[3] if len(vals) == 4 else 1.0)
    m = re.fullmatch(r"(rgba?|hsla?)\((.*)\)", c, re.S)
    if m:
        args = re.split(r"[\s,/]+", m.group(2).strip())
        a = num(args[3]) if len(args) > 3 else 1.0
        if m.group(1).startswith("rgb"):
            return (num(args[0], 255), num(args[1], 255), num(args[2], 255), a)
        r, g, b = colorsys.hls_to_rgb(num(args[0]) / 360, num(args[2]), num(args[1]))
        return (r, g, b, a)
    m = re.fullmatch(r"color-mix\(in srgb,(.*)\)", c, re.S)
    if m:
        (c1, *p1), (c2, *p2) = [part.rsplit(" ", 1) if part.rstrip().endswith("%") else [part] for part in split_args(m.group(1))]
        w1 = num(p1[0]) if p1 else (1 - num(p2[0]) if p2 else 0.5)
        w2 = num(p2[0]) if p2 else 1 - w1
        a, b = parse(c1), parse(c2)
        alpha = a[3] * w1 + b[3] * w2
        if alpha == 0:
            return (0.0, 0.0, 0.0, 0.0)
        mix = [(a[i] * a[3] * w1 + b[i] * b[3] * w2) / alpha for i in range(3)]   # premultiplied
        return (*mix, alpha)
    raise ValueError(f"cannot read the colour {c!r}")


def over(top, under):
    a = top[3] + under[3] * (1 - top[3])
    if a == 0:
        return (0.0, 0.0, 0.0, 0.0)
    return (*[(top[i] * top[3] + under[i] * under[3] * (1 - top[3])) / a for i in range(3)], a)


def luminance(c) -> float:
    lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c[:3]]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hexof(c) -> str:
    return "#" + "".join(f"{round(v * 255):02x}" for v in c[:3])


def check(show_all: bool = False) -> int:
    failures = 0
    for scheme, props in schemes().items():
        color = lambda v: parse(resolve(v, props))   # noqa: E731
        for what, fg, layers, minimum in PAIRS:
            layers = [layer[scheme] if isinstance(layer, dict) else layer for layer in layers]
            bg = (1.0, 1.0, 1.0, 1.0)
            for layer in reversed(layers):
                bg = over(color(layer), bg)
            r = ratio(over(color(fg), bg), bg)
            bad = r < minimum
            failures += bad
            if bad or show_all:
                print(f"{'FAIL' if bad else 'ok  '}  {scheme:7} {what:26} {r:5.2f}:1 (needs {minimum}) "
                      f"{hexof(over(color(fg), bg))} on {hexof(bg)}")
    print(f"{len(PAIRS)} colour pairs in 2 schemes, {failures} under their minimum")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--all", action="store_true", help="print the pairs that pass too")
    return check(ap.parse_args(argv).all)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
