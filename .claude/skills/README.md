# Skills of this project

Third-party Claude Code skills, copied into the repository so every session (local or cloud)
loads them. The design skills were added in session 33 (2026-11-07) at the owner's request, for
reviewing and improving the site's visual design, effects and animations; ponytail and
diagram-design in session 34 (2026-11-14), and webapp-testing and the six web-quality skills
on 2026-11-20, also at the owner's request (`dv-question` is this repository's own skill). Each folder keeps its upstream
license; the files are as upstream published them (only the upstream test fixtures of
ui-ux-pro-max were left out). To update one, copy the folder again from the same source.

| Skill | Source (commit) | License | What it gives |
|-------|-----------------|---------|---------------|
| `ui-ux-pro-max` | github.com/nextlevelbuilder/ui-ux-pro-max-skill, `.claude/skills/ui-ux-pro-max` (b7d5353) | MIT | Searchable local data: styles, palettes, font pairings, UX guidelines, motion presets, charts. Python 3 only, no network. |
| `impeccable` | github.com/pbakaus/impeccable, `.claude/skills/impeccable` (687bc38) | Apache 2.0 | Design commands (audit, critique, animate, polish, quieter, typeset, ...) with a reference file each. |
| `web-design-guidelines` | github.com/vercel-labs/agent-skills, `skills/web-design-guidelines` (1a2c79d) | MIT | Reviews UI code against Vercel's Web Interface Guidelines, fetched fresh from raw.githubusercontent.com. |
| `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help` | github.com/DietrichGebert/ponytail, `skills/` (96608e0), v5.3.3 | MIT | "Lazy senior dev" rules: reuse the codebase's helpers, the stdlib and the platform before new code; a review of a change and an audit of the repo (both report only, change no code); a ledger of `shortcut:` comments. Markdown only. |
| `diagram-design` | github.com/cathrynlavery/diagram-design, `skills/diagram-design` (f6db0de), v2.6.164 | MIT | Editorial diagrams (50 types: architecture, flowchart, sequence, state machine, timeline, swimlane, charts, ...) as self-contained HTML/SVG with its own design system, 239 HTML templates, 69 references, and Python scripts that import draw.io / Mermaid / Excalidraw / PlantUML and export SVG / PNG. |
| `webapp-testing` | github.com/anthropics/skills, `skills/webapp-testing` (e4bb5d9) | Apache 2.0 | Playwright recipes for testing a local web app: `scripts/with_server.py` starts servers, waits for their ports and runs a script; examples of element discovery, console capture and screenshots. |
| `web-quality-audit`, `performance`, `core-web-vitals`, `accessibility`, `seo`, `best-practices` | github.com/addyosmani/web-quality-skills, `skills/` (afa8da9), v2.0 | MIT | Evidence-led web quality audits in the Lighthouse categories: a measurement workflow (lab trace, Lighthouse, field data kept apart), page budgets, LCP / INP / CLS references, WCAG 2.2, SEO and security headers; `web-quality-audit/scripts/analyze.sh` is a read-only HTML smoke test (needs `jq`). Markdown only otherwise. |
| `dv-question` | this repository | (the site's) | Turns a conversation the owner pastes (a question and its solution) into a full question page: checks the math, picks the level, scaffolds, writes the parts, tests, figures and box, runs the checks and commits. |
