#!/usr/bin/env bash
# Builds docs/javascripts/vendor/codemirror.min.js from tools/codemirror/entry.js with the
# pinned CodeMirror packages below (MIT licence). Run it after a version bump or an edit of
# entry.js, and commit the bundle; the site never loads CodeMirror from a CDN.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/../.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cp "$here/entry.js" "$work/"
cd "$work"
npm init -y >/dev/null
npm install --no-audit --no-fund --silent \
  esbuild@0.24.0 @codemirror/state@6.4.1 @codemirror/view@6.35.0 @codemirror/commands@6.7.1 \
  @codemirror/language@6.10.6 @codemirror/lang-python@6.1.6 @lezer/highlight@1.2.1
mkdir -p "$root/docs/javascripts/vendor"
npx esbuild entry.js --bundle --minify --format=iife --target=es2020 \
  --legal-comments=none \
  --banner:js="/* CodeMirror 6 (MIT, https://codemirror.net), bundled by tools/codemirror/build.sh */" \
  --outfile="$root/docs/javascripts/vendor/codemirror.min.js"
ls -l "$root/docs/javascripts/vendor/codemirror.min.js"
