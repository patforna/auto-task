#!/usr/bin/env python3
"""Frame a terminal GIF in window chrome: rounded corners + a title bar.

agg renders bare terminal frames; this composites each one onto a window,
preserving per-frame durations. The corners are backed by OUTER rather than made
transparent: GIF transparency forces a per-frame palette and full frames, which
cost ~20x the file size for a detail nobody sees on a dark page.

Usage: chrome.py <in.gif> <out.gif> [title] [--win #rrggbb] [--bar #rrggbb] [--outer #rrggbb]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SCALE = 1.0        # set from --scale; the GIF is rendered at 2x so chrome must match
PAD = 0            # px of window border either side of the terminal
OUTER = (24, 26, 31)   # behind the rounded corners; a shade under the window
BAR = 34           # title bar height, at scale 1
RADIUS = 12
BAR_BG = (54, 59, 69)
WIN_BG = (40, 44, 52)   # #282c34, a shade above the terminal ground; PAD=0,
                        # so only the corner arcs ever show it
TITLE = (150, 156, 166)
TITLE_SIZE = 10    # at scale 1; the body mono a size down, 20 px at the 2x render
LIGHTS = [(255, 95, 87), (254, 188, 46), (40, 200, 64)]


def px(v):
    return int(round(v * SCALE))


def font(size=TITLE_SIZE):
    size = px(size)
    # The terminal's own face first — Pillow resolves a bare filename against the
    # system font dirs — with the macOS sans behind it, so a machine without it
    # still gets a title rather than a crash.
    for path in ("JetBrainsMono-Regular.ttf",
                 "/System/Library/Fonts/SFNS.ttf",
                 "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def window(size, title):
    """The chrome, as RGBA with transparent outside-the-corners."""
    w, h = size
    img = Image.new("RGBA", (w, h), OUTER + (255,))
    d = ImageDraw.Draw(img)
    bar, radius = px(BAR), px(RADIUS)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius, fill=WIN_BG + (255,))
    d.rounded_rectangle([0, 0, w - 1, bar + radius], radius, fill=BAR_BG + (255,))
    d.rectangle([0, bar, w - 1, bar + radius], fill=WIN_BG + (255,))
    d.rectangle([0, bar - 1, w - 1, bar - 1], fill=(0, 0, 0, 60))
    r = px(5)
    for i, colour in enumerate(LIGHTS):
        x = px(18) + i * px(20)
        d.ellipse([x, bar // 2 - r, x + 2 * r, bar // 2 + r], fill=colour + (255,))
    f = font()
    tw = d.textlength(title, font=f)
    _, top, _, bottom = f.getbbox(title)   # centre on the ink, not a tuned offset
    y = bar // 2 - (top + bottom) // 2
    d.text(((w - tw) / 2, y), title, font=f, fill=TITLE + (255,))
    return img


def hexcol(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main():
    global WIN_BG, BAR_BG, OUTER, SCALE
    argv = sys.argv[1:]

    def opt(name):
        if name in argv:
            i = argv.index(name)
            value = argv[i + 1]
            del argv[i:i + 2]
            return value
        return None

    scale = opt("--scale")
    if scale:
        SCALE = float(scale)
    for flag, target in (("--win", "WIN_BG"), ("--bar", "BAR_BG"), ("--outer", "OUTER")):
        value = opt(flag)
        if value:
            globals()[target] = hexcol(value)
    src, dst = argv[0], argv[1]
    gif = Image.open(src)
    title = argv[2] if len(argv) > 2 else f"Terminal — {gif.width}×{gif.height}"

    size = (gif.width + px(PAD) * 2, gif.height + px(BAR) + px(PAD))
    chrome = window(size, title)

    def compose(i):
        """The finished frame i: terminal pasted into the window, corners rounded."""
        gif.seek(i)
        canvas = chrome.copy()
        canvas.paste(gif.convert("RGB"), (px(PAD), px(BAR)))
        mask = Image.new("L", size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1],
                                               px(RADIUS), fill=255)
        return Image.composite(canvas, Image.new("RGBA", size, OUTER + (255,)),
                               mask).convert("RGB")

    # Build the shared palette from a spread of COMPOSED frames. Sampling frame 1 —
    # or the bare terminal without its chrome — starves the palette of the shades
    # text antialiasing needs, and the glyphs come out chunky.
    idx = list(range(0, gif.n_frames, max(1, gif.n_frames // 12)))
    strip = Image.new("RGB", (size[0], size[1] * len(idx)))
    for n, i in enumerate(idx):
        strip.paste(compose(i), (0, n * size[1]))
    base = strip.quantize(colors=256, method=Image.MEDIANCUT)

    frames, durations = [], []
    for i in range(gif.n_frames):
        frames.append(compose(i).quantize(palette=base, dither=Image.Dither.NONE))
        durations.append(gif.info.get("duration", 40))

    frames[0].save(dst, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True)
    print(f"{dst}: {size[0]}x{size[1]} px, {len(frames)} frames")


if __name__ == "__main__":
    main()
