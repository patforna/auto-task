#!/usr/bin/env bash
# Re-vendor panel, synthesize, tdd from the core-skills plugin.
#
# These three skills live canonically in core-skills and are vendored here so the
# auto-task plugin stays self-contained. Run this after editing any of them in
# core-skills. The vendored copies differ from the originals ONLY in that
# `/core-skills:` refs are rewritten to `/at:`. See CLAUDE.md for the invariant.
#
# Usage: scripts/vendor.sh [path-to-core-skills]   (default: ~/github/core-skills)
set -euo pipefail

CORE="${1:-$HOME/github/core-skills}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"   # plugin repo root
SKILLS=(panel synthesize tdd)

[ -d "$CORE/skills" ] || { echo "error: core-skills not found at $CORE" >&2; exit 1; }

for s in "${SKILLS[@]}"; do
  src="$CORE/skills/$s"
  [ -d "$src" ] || { echo "error: source skill missing: $src" >&2; exit 1; }
  rm -rf "$HERE/skills/$s"
  cp -R "$src" "$HERE/skills/$s"
  # vendored copies namespace their internal refs to this plugin:
  find "$HERE/skills/$s" -name '*.md' -exec perl -pi -e 's|/core-skills:|/at:|g' {} +
  echo "vendored $s"
done

cat <<'EOF'

Re-vendored from core-skills. Live in your own checkout already; to ship it,
cut a release — see README section "Releasing".
EOF
