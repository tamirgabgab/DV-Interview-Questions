# Design skills of this project

Third-party Claude Code skills, copied into the repository so every session (local or cloud)
loads them. Added in session 33 (2026-11-07) at the owner's request, for reviewing and
improving the site's visual design, effects and animations. Each folder keeps its upstream
license; the files are as upstream published them (only the upstream test fixtures of
ui-ux-pro-max were left out). To update one, copy the folder again from the same source.

| Skill | Source (commit) | License | What it gives |
|-------|-----------------|---------|---------------|
| `ui-ux-pro-max` | github.com/nextlevelbuilder/ui-ux-pro-max-skill, `.claude/skills/ui-ux-pro-max` (b7d5353) | MIT | Searchable local data: styles, palettes, font pairings, UX guidelines, motion presets, charts. Python 3 only, no network. |
| `impeccable` | github.com/pbakaus/impeccable, `.claude/skills/impeccable` (687bc38) | Apache 2.0 | Design commands (audit, critique, animate, polish, quieter, typeset, ...) with a reference file each. |
| `web-design-guidelines` | github.com/vercel-labs/agent-skills, `skills/web-design-guidelines` (1a2c79d) | MIT | Reviews UI code against Vercel's Web Interface Guidelines, fetched fresh from raw.githubusercontent.com. |

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
