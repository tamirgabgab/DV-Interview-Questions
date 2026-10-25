#!/bin/bash
# SessionStart hook: prepare a Claude Code cloud session to run the checks as CI does
# (tools/dev_setup.sh); local sessions are left alone. Never blocks the session: a step
# that fails is reported in the output.
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

"$CLAUDE_PROJECT_DIR/tools/dev_setup.sh" || true

# the social cards fetch their font from fonts.google.com; where the network policy blocks
# it, the build runs without them (as CI's DVQ_SOCIAL_CARDS switch allows)
if [ -n "${CLAUDE_ENV_FILE:-}" ] && ! curl -sfI -m 10 "https://fonts.google.com/download/list?family=Rubik" >/dev/null 2>&1; then
  echo "export DVQ_SOCIAL_CARDS=false" >> "$CLAUDE_ENV_FILE"
  echo "[session-start] fonts.google.com is not reachable: DVQ_SOCIAL_CARDS=false (no social cards in local builds)"
fi

# a Verilator built earlier with tools/dev_setup.sh --verilator comes first on PATH
if [ -x "$HOME/verilator/bin/verilator" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$HOME/verilator/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi
exit 0
