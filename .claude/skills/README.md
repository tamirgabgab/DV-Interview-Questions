# Skills of this project

Third-party Claude Code skills, copied into the repository so every session (local or cloud)
loads them. The design skills were added in session 33 (2026-11-07) at the owner's request, for
reviewing and improving the site's visual design, effects and animations; ponytail and
diagram-design in session 34 (2026-11-14), also at the owner's request. Each folder keeps its upstream
license; the files are as upstream published them (only the upstream test fixtures of
ui-ux-pro-max were left out). To update one, copy the folder again from the same source.

| Skill | Source (commit) | License | What it gives |
|-------|-----------------|---------|---------------|
| `ui-ux-pro-max` | github.com/nextlevelbuilder/ui-ux-pro-max-skill, `.claude/skills/ui-ux-pro-max` (b7d5353) | MIT | Searchable local data: styles, palettes, font pairings, UX guidelines, motion presets, charts. Python 3 only, no network. |
| `impeccable` | github.com/pbakaus/impeccable, `.claude/skills/impeccable` (687bc38) | Apache 2.0 | Design commands (audit, critique, animate, polish, quieter, typeset, ...) with a reference file each. |
| `web-design-guidelines` | github.com/vercel-labs/agent-skills, `skills/web-design-guidelines` (1a2c79d) | MIT | Reviews UI code against Vercel's Web Interface Guidelines, fetched fresh from raw.githubusercontent.com. |
| `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help` | github.com/DietrichGebert/ponytail, `skills/` (96608e0), v5.3.3 | MIT | "Lazy senior dev" rules: reuse the codebase's helpers, the stdlib and the platform before new code; a review of a change and an audit of the repo (both report only, change no code); a ledger of `shortcut:` comments. Markdown only. |
| `diagram-design` | github.com/cathrynlavery/diagram-design, `skills/diagram-design` (f6db0de), v2.6.164 | MIT | Editorial diagrams (50 types: architecture, flowchart, sequence, state machine, timeline, swimlane, charts, ...) as self-contained HTML/SVG with its own design system, 239 HTML templates, 69 references, and Python scripts that import draw.io / Mermaid / Excalidraw / PlantUML and export SVG / PNG. |

Anthropic's `frontend-design` skill is installed as a plugin, not here.

## Notes for this repository

- **ui-ux-pro-max:** its SKILL.md runs the search through `${CLAUDE_PLUGIN_ROOT}`, which is
  empty for a project skill. From the repository root run it as
  `python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain>`
  (domains: style, color, typography, ux, chart, icons, gsap, ...; `--design-system` for a
  whole direction).
- **impeccable:** `scripts/impeccable` is a launcher that downloads a platform binary from
  the project's GitHub releases on first use (checked against `engine-checksums.txt`) into
  `scripts/bin/`, which is git-ignored. Running it needs the owner's permission in the
  session; without it, read the files under `reference/` directly (the skill says so too).
  Its optional design-detector hook is off unless `/impeccable hooks on` is run.
- **ponytail:** only the six skill folders were copied, not the plugin. The plugin's hooks are
  therefore not installed: no session-start auto-activation, no band above the prompt, no
  task ledger in `~/.config/ponytail/` and no webhook. The skills run only when invoked
  (`/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail [lite|full|ultra]`).
  Use review and audit as reports; the lazy mode itself is for code changes and must not cut
  what a question page needs (parts, figures, tests, the checks). Its reports are written in
  English by design; in this repository the summary to the owner is still in Hebrew.
- **diagram-design:** its output is a standalone HTML/SVG page with its own palette and
  Google Fonts, so it is never pasted into the site: the site's figures stay in
  `tools/figures/q<id>.py` with the palette variables and the RTL rules. Use it for layout
  ideas for a figure, or for diagrams outside the site (notes, slides). On first use it asks
  to customise `references/style-guide.md` (the working copy inside this folder) and can save
  profiles to `~/.diagram-design/profiles/`; its scripts are local (no network, no
  subprocess), `export_png.py` needs Playwright, which is installed.
- **The site's own rules come first:** RTL and the colon spacing, the palette variables of
  `docs/stylesheets/` (no literal colours), `check_contrast.py`, the reduced-motion rules
  and the checks of `CLAUDE.md`. A skill's suggestion that conflicts with them is reported
  to the owner, not applied.

## Not installed

- **Taste Skill** (github.com/Leonxlnx/taste-skill, MIT): about 40 MB of photos and assets,
  aimed at company landing pages, and it registers a `Stop` hook that runs a Node gate at
  the end of every turn. Left out for now.
- **elite-frontend-design:** only found on third-party skill registries, with no source
  repository to check. Not installed.
