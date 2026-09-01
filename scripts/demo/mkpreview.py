#!/usr/bin/env python3
"""Wrap a cast in a self-contained HTML page with the asciinema player inlined.

The player JS/CSS are fetched once into assets/ (gitignored) and embedded, so the
resulting page works offline and can be opened straight from the filesystem.

Usage: mkpreview.py <cast> <html> [--font-size 14] [--font-family "..."]
"""
import json, pathlib, subprocess, sys

PLAYER = "https://cdn.jsdelivr.net/npm/asciinema-player@3.10.0/dist/bundle"
ASSETS = pathlib.Path(__file__).parent / "assets"


def asset(name):
    """Return the asset's text, downloading it on first use."""
    path = ASSETS / name
    if not path.exists():
        ASSETS.mkdir(exist_ok=True)
        subprocess.run(["curl", "-fsSL", "-o", str(path), f"{PLAYER}/{name}"], check=True)
    return path.read_text()


TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<title>auto-task demo</title>
<style>%s</style>
<style>
 body{background:#14151c;margin:0;min-height:100vh;display:flex;flex-direction:column;
      align-items:center;justify-content:center;font-family:system-ui,sans-serif;gap:14px}
 /* window chrome: rounded frame + title bar, so the clip reads as a terminal */
 .win{border-radius:12px;overflow:hidden;background:#0d1117;max-width:96vw;
      box-shadow:0 18px 50px rgba(0,0,0,.55)}
 .bar{height:34px;background:#20242c;display:flex;align-items:center;padding:0 13px;
      gap:8px;position:relative}
 .dot{width:11px;height:11px;border-radius:50%%}   /* %% : escaped for the format string */
 .bar span.t{position:absolute;left:0;right:0;text-align:center;color:#8a90a6;
             font-size:12px;letter-spacing:.02em}
 #player{max-width:96vw}
 /* asciinema-player hardcodes "Consolas, Menlo, ..." in its own stylesheet, so
    terminalFontFamily alone is ignored. Override it here, at higher specificity. */
 .ap-terminal, .ap-terminal .ap-line, .ap-terminal .ap-line span{font-family:%s !important}
 p{color:#8a90a6;font-size:13px;margin:0}
 code{color:#c0c6dc}
</style></head><body>
<div class="win">
  <div class="bar">
    <i class="dot" style="background:#ff5f57"></i>
    <i class="dot" style="background:#febc2e"></i>
    <i class="dot" style="background:#28c840"></i>
    <span class="t">Terminal &mdash; %d&times;%d</span>
  </div>
  <div id="player"></div>
</div>
<p><code>space</code> play/pause · <code>←/→</code> seek · <code>&lt; &gt;</code> speed</p>
<script>%s</script>
<script>
AsciinemaPlayer.create({data:%s},document.getElementById('player'),
 {cols:%d,rows:%d,autoPlay:true,loop:true,fit:false,controls:true,
  terminalFontSize:'%spx',terminalFontFamily:%s,terminalLineHeight:%s});
</script></body></html>"""


FONT_STACK = ('"JetBrains Mono","SF Mono",Menlo,Consolas,'
              '"Liberation Mono",monospace')


def main():
    args = sys.argv[1:]
    def opt(name, default):
        return args[args.index(name) + 1] if name in args else default
    font_size = opt("--font-size", "18")
    line_height = opt("--line-height", "1.45")
    font_family = opt("--font-family", FONT_STACK)
    cast_path, html_path = args[0], args[1]
    lines = pathlib.Path(cast_path).read_text().strip().split("\n")
    hdr, events = json.loads(lines[0]), [json.loads(l) for l in lines[1:]]

    # asciicast v3 stores relative intervals; v2 stores absolute timestamps.
    relative = hdr.get("version", 2) >= 3
    term = hdr.get("term", {})
    cols = term.get("cols", hdr.get("width", 92))
    rows = term.get("rows", hdr.get("height", 26))

    out, t = [], 0.0
    for e in events:
        t = t + e[0] if relative else e[0]
        if e[1] in ("o", "i"):
            out.append([round(t, 3), e[1], e[2]])

    v2 = {"version": 2, "width": cols, "height": rows,
          "title": hdr.get("title", "auto-task"),
          "env": {"TERM": "xterm-256color", "SHELL": "/bin/zsh"}}
    if hdr.get("theme"):
        v2["theme"] = hdr["theme"]
    elif term.get("theme"):
        v2["theme"] = term["theme"]

    cast = json.dumps(v2) + "\n" + "\n".join(
        json.dumps(e, ensure_ascii=False) for e in out) + "\n"

    html = TEMPLATE % (asset("asciinema-player.css"), font_family, cols, rows,
                       asset("asciinema-player.min.js").replace("</script", "<\\/script"),
                       json.dumps(cast).replace("</script", "<\\/script"), cols, rows,
                       font_size, json.dumps(font_family), line_height)
    pathlib.Path(html_path).write_text(html)
    print(f"{html_path}: {len(html) // 1024} KB — {cols}x{rows} @ {font_size}px, "
          f"{out[-1][0]:.1f}s, lh {line_height}")


if __name__ == "__main__":
    main()
