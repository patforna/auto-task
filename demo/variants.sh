#!/usr/bin/env bash
# Render the demo in every theme, side by side, for comparison.
#   ./variants.sh            all themes
#   ./variants.sh kiro       just one
set -euo pipefail
cd "$(dirname "$0")"
cols=$(python3 -c 'import cast; print(cast.COLS)')
rows=$(python3 -c 'import cast; print(cast.ROWS)')
FONT="${FONT:-JetBrains Mono,Menlo,Apple Color Emoji}"
title=$(python3 -c 'import cast; print(cast.title())')   # one name for the window

themes=("$@")
[ ${#themes[@]} -eq 0 ] && themes=(ghostty kiro catppuccin)

for theme in "${themes[@]}"; do
  read -r win bar outer <<<"$(python3 -c "
import cast; t = cast.THEMES['$theme']; print(t['win'], t['bar'], t['outer'])")"
  python3 cast.py demo.txt --theme "$theme" -o "/tmp/$theme.cast" >/dev/null
  agg --cols "$cols" --rows "$rows" --font-size 30 --font-family "$FONT" \
      "/tmp/$theme.cast" "/tmp/$theme-raw.gif" >/dev/null 2>&1
  uv run --with pillow python chrome.py "/tmp/$theme-raw.gif" "demo-$theme.gif" \
      "$title" --scale 2 --win "$win" --bar "$bar" --outer "$outer" >/dev/null
  python3 mkpreview.py "/tmp/$theme.cast" "demo-$theme.html" >/dev/null
  printf '%-12s gif %s · preview demo-%s.html\n' \
    "$theme" "$(du -h "demo-$theme.gif" | cut -f1)" "$theme"
done
