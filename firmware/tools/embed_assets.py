#!/usr/bin/env python3
import io, math, struct, pathlib
from PIL import Image, ImageDraw

root = pathlib.Path(__file__).resolve().parents[1]
inc = root / "include"
inc.mkdir(exist_ok=True)

def dump(name, raw):
    lines = [f"const uint8_t {name}[] PROGMEM = {{"]
    chunk = []
    for b in raw:
        chunk.append(f"0x{b:02x}")
        if len(chunk) == 16:
            lines.append("  " + ", ".join(chunk) + ",")
            chunk = []
    if chunk:
        lines.append("  " + ", ".join(chunk) + ",")
    lines.append("};")
    lines.append(f"const int {name}_LEN = {len(raw)};")
    return "\n".join(lines)

def gif_frames(draw_fn, n=4, duration=120):
    frames = []
    for i in range(n):
        im = Image.new("P", (240, 240), 0)
        pal = []
        pal.extend([0, 0, 0])
        pal.extend([255, 107, 107])
        pal.extend([29, 209, 161])
        pal.extend([255, 255, 255])
        pal.extend([84, 160, 255])
        pal.extend([242, 193, 78])
        pal.extend([80, 80, 90])
        pal.extend([0] * (768 - len(pal)))
        im.putpalette(pal)
        d = ImageDraw.Draw(im)
        draw_fn(d, i, n)
        frames.append(im)
    buf = io.BytesIO()
    frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], loop=0, duration=duration, optimize=True)
    return buf.getvalue()

def wajah(d, i, n):
    d.ellipse((40, 30, 200, 210), fill=5)
    d.ellipse((70, 80, 110, 120), fill=0)
    d.ellipse((130, 80, 170, 120), fill=0)
    d.ellipse((82, 92 + (i % 2) * 4, 98, 108 + (i % 2) * 4), fill=3)
    d.ellipse((142, 92 + (i % 2) * 4, 158, 108 + (i % 2) * 4), fill=3)
    openm = 20 + (i % 2) * 18
    d.ellipse((90, 140, 150, 140 + openm), fill=1)

def mobil(d, i, n):
    x = 20 + i * 18
    d.rectangle((0, 180, 240, 240), fill=6)
    d.rounded_rectangle((x, 110, x + 140, 170), radius=12, fill=4)
    d.ellipse((x + 15, 155, x + 45, 185), fill=0)
    d.ellipse((x + 95, 155, x + 125, 185), fill=0)
    d.rectangle((x + 90, 118, x + 130, 145), fill=2)

def intro(d, i, n):
    r = 30 + i * 8
    d.ellipse((120 - r, 120 - r, 120 + r, 120 + r), outline=1, width=6)
    d.text((70, 200), "rzmong", fill=3)

assets = [
    ("GIF_WAJAH", "wajah", "yelling", gif_frames(wajah)),
    ("GIF_MOBIL", "mobil", "car", gif_frames(mobil)),
    ("GIF_INTRO", "intro", "intro_3", gif_frames(intro)),
]

g = ["#pragma once", "#include <Arduino.h>"]
for name, theme, stem, raw in assets:
    print(name, len(raw))
    g.append(dump(name, raw))
g.append("struct DefaultGif { const char *theme; const char *stem; const uint8_t *data; int len; };")
g.append("static const DefaultGif DEFAULT_GIFS[] = {")
for name, theme, stem, raw in assets:
    g.append(f'  {{"{theme}", "{stem}", {name}, {name}_LEN}},')
g.append("};")
g.append(f"static const int DEFAULT_GIF_COUNT = {len(assets)};")
(inc / "defaults_gif.h").write_text("\n".join(g) + "\n")

sr = 8000
notes = [(523, 0.12), (659, 0.12), (784, 0.16), (1046, 0.18)]
samples = []
for freq, leng in notes:
    nn = int(sr * leng)
    for i in range(nn):
        env = min(1.0, i / 80.0) * min(1.0, (nn - i) / 120.0)
        samples.append(int(10000 * env * math.sin(2 * math.pi * freq * i / sr)))
pcm = b"".join(struct.pack("<h", s) for s in samples)
(inc / "jingle.h").write_text("\n".join([
    "#pragma once", "#include <Arduino.h>", f"const int JINGLE_SR = {sr};", dump("JINGLE_PCM", pcm)
]) + "\n")
print("embedded ok", "pcm", len(pcm))
try:
    Import("env")
except Exception:
    pass
