#!/bin/bash
# Prepare a sandbox (a Claude Code cloud session, or any fresh machine) to run the checks
# the way CI runs them. Safe to run again: every step skips what is already in place.
#
#   tools/dev_setup.sh               Python packages (site, tests, cairosvg for the social
#                                    cards) and local copies of the CDN scripts the pages
#                                    load, in .cache/cdn, for check_phone.py and
#                                    check_explorers.py with --local-cdn
#   tools/dev_setup.sh --verilator   also build Verilator at the commit CI pins
#                                    (VERILATOR_REF in .github/workflows/deploy.yml) into
#                                    ~/verilator, 10 to 15 minutes; put ~/verilator/bin first
#                                    on PATH to use it
#
# A step that fails (no network, a package that will not install) is reported and the
# others still run; the exit status is 1 when anything is missing.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CDN="$ROOT/.cache/cdn"
missing=()

step() { printf '[dev_setup] %s\n' "$*"; }

# --- Python -------------------------------------------------------------------------------
if python3 -c "import mkdocs, material, pytest, playwright, cairosvg" 2>/dev/null; then
  step "python packages: present"
else
  step "python packages: installing"
  pip install -q --root-user-action=ignore -r "$ROOT/requirements.txt" -r "$ROOT/requirements-dev.txt" cairosvg \
    || missing+=("python packages")
fi

# --- CDN scripts (the versions mkdocs.yml and Material load) -------------------------------
# name  npm package@version  file inside the package the checks route to
fetch() {
  local name=$1 spec=$2 file=$3
  if [ -f "$CDN/$name/$file" ]; then step "$name: present"; return; fi
  step "$name: fetching $spec"
  local tmp; tmp="$(mktemp -d)"
  if (cd "$tmp" && npm pack -q "$spec" >/dev/null 2>&1) && mkdir -p "$CDN/$name" \
     && tar -xzf "$tmp"/*.tgz -C "$CDN/$name" --strip-components=1 && [ -f "$CDN/$name/$file" ]; then
    :
  else
    missing+=("$name"); rm -rf "${CDN:?}/$name"
  fi
  rm -rf "$tmp"
}
fetch mathjax   mathjax@3.2.2    es5/tex-mml-chtml.js
fetch mermaid   mermaid@11       dist/mermaid.min.js
fetch wavedrom  wavedrom@3.5.0   wavedrom.min.js
fetch axe-core  axe-core@4.14.0  axe.min.js

# --- Chromium for Playwright -------------------------------------------------------------
if python3 - <<'PY' 2>/dev/null
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()
PY
then step "chromium: present"
else
  step "chromium: installing"
  python3 -m playwright install chromium >/dev/null 2>&1 || missing+=("chromium")
fi

# --- Verilator at the pinned commit (only with --verilator) --------------------------------
if [ "${1:-}" = "--verilator" ]; then
  ref="$(sed -n 's/^ *VERILATOR_REF: *"\([0-9a-f]*\)".*/\1/p' "$ROOT/.github/workflows/deploy.yml")"
  # a build of the pinned commit reports its short hash in --version ("rev ...-7a5509c")
  if "$HOME/verilator/bin/verilator" --version 2>/dev/null | grep -q -- "-${ref:0:7}"; then
    step "verilator $ref: present"
  else
    step "verilator: building $ref (10 to 15 minutes)"
    src="$(mktemp -d)"
    if (cd "$src" && git init -q && git fetch -q --depth 1 https://github.com/verilator/verilator.git "$ref" \
        && git checkout -q FETCH_HEAD && autoconf && ./configure -q --prefix="$HOME/verilator" >/dev/null \
        && make -s -j"$(nproc)" >/dev/null && make -s install >/dev/null); then
      :
    else
      missing+=("verilator")
    fi
    rm -rf "$src"
  fi
fi

if [ ${#missing[@]} -eq 0 ]; then
  step "ready"
else
  step "missing: ${missing[*]}"
  exit 1
fi
