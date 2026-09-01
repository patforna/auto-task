#!/usr/bin/env bash
# Rebuild the demo: screenplay -> asciicast -> GIF + scrubbing HTML preview.
#
#   ./render.sh [screenplay]     (default: demo.txt)
#
# Requires: python3, agg (brew install agg), uv (for Pillow, used to draw the
# window chrome). curl on first run, to fetch the asciinema player preview.
set -euo pipefail
cd "$(dirname "$0")"

script="${1:-demo.txt}"
cols=$(python3 -c 'import cast; print(cast.COLS)')
# The GIF renders at 2x, so the chrome has to scale with it.
scale=$(python3 -c "print(${FONT_SIZE:-30} / 15)")
rows=$(python3 -c 'import cast; print(cast.ROWS)')

python3 cast.py "$script" -o demo.cast
# 2x font size: the GIF is a fixed raster, so render at double resolution and let
# it display at half width. Sharp on retina, ~2x the bytes.
# Pin the font: agg's default chain starts at JetBrains Mono but falls through to
# whatever the machine has, so an unpinned render is not reproducible. --font-family
# bypasses fallbacks entirely, so the emoji font has to be named too or 🚢/🎉 vanish.
# Menlo sits between them on purpose: JetBrains Mono has none of the spinner
# dingbats (✳ ✻ ✽ ✢), and without a text fallback they resolve to Apple Color
# Emoji and render in colour.
FONT="${FONT:-JetBrains Mono,Menlo,Apple Color Emoji}"
agg --cols "$cols" --rows "$rows" --font-size "${FONT_SIZE:-30}" \
    --font-family "$FONT" demo.cast demo-raw.gif >/dev/null 2>&1

# Frame it in window chrome (agg can't). Falls back to the bare GIF if Pillow
# isn't reachable, so a missing uv never blocks a render.
if uv run --with pillow python chrome.py demo-raw.gif demo.gif "Terminal" --scale "$scale" >/dev/null 2>&1; then
  :
else
  echo "warning: chrome.py failed, using the unframed GIF" >&2
  cp demo-raw.gif demo.gif
fi
python3 mkpreview.py demo.cast demo.html

printf 'gif: %s  (%s)\n' "$(du -h demo.gif | cut -f1)" "$PWD/demo.gif"
printf 'open %s to scrub through it\n' "$PWD/demo.html"
