#!/usr/bin/env python3
import io, math, struct, pathlib, base64
from PIL import Image, ImageDraw
root = pathlib.Path(__file__).resolve().parents[1]
inc = root / "include"
inc.mkdir(exist_ok=True)
b64dir = pathlib.Path(__file__).resolve().parent / "react_b64"
rawdir = root / "assets" / "react"

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

def gif_frames(draw_fn, n=3, duration=110):
    frames = []
    for i in range(n):
        im = Image.new("P", (240, 240), 0)
        pal = [0,0,0, 255,107,107, 29,209,161, 255,255,255, 84,160,255, 242,193,78, 80,80,90, 180,80,200]
        pal.extend([0] * (768 - len(pal)))
        im.putpalette(pal)
        d = ImageDraw.Draw(im)
        draw_fn(d, i, n)
        frames.append(im)
    buf = io.BytesIO()
    frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], loop=0, duration=duration, optimize=True)
    return buf.getvalue()

def load_gif(stem, fallback):
    p = rawdir / f"{stem}.gif"
    if p.exists() and p.stat().st_size > 100:
        return p.read_bytes()
    b = b64dir / f"{stem}.gif.b64"
    if b.exists():
        try:
            txt = b.read_text().strip()
            if txt and txt != "PLACEHOLDER" and len(txt) > 32:
                raw = base64.b64decode(txt)
                if len(raw) > 100 and raw[:3] == b"GIF":
                    return raw
        except Exception as e:
            print("b64 skip", stem, e)
    return fallback()

def face(d, i, mouth=20, eye=0):
    d.ellipse((40,30,200,210), fill=5)
    d.ellipse((70,80,110,120), fill=0)
    d.ellipse((130,80,170,120), fill=0)
    d.ellipse((82,92+eye,98,108+eye), fill=3)
    d.ellipse((142,92+eye,158,108+eye), fill=3)
    d.ellipse((90,140,150,140+mouth), fill=1)

def yelling(d,i,n): face(d,i,mouth=20+(i%2)*22, eye=(i%2)*3)
def distracted(d,i,n): face(d,i,mouth=8, eye=0)
def love(d,i,n): face(d,i,mouth=12, eye=0)
def hadouken(d,i,n): d.ellipse((70,70,170,170), fill=4)
def laugh(d,i,n): face(d,i,mouth=16+(i%2)*20, eye=-2)
def cry(d,i,n): face(d,i,mouth=6, eye=2)
def keep(d,i,n):
    r=40+i*10; d.ellipse((120-r,120-r,120+r,120+r), outline=2, width=8)
def sneeze(d,i,n): face(d,i,mouth=8+i*10, eye=-i*2)
def blade(d,i,n): d.polygon([(120,40),(180,200),(60,200)], fill=4)
def pinky(d,i,n): d.ellipse((50,40,190,200), fill=7)

assets = [
    ("GIF_YELLING","wajah","yelling", lambda: gif_frames(yelling)),
    ("GIF_DISTRACTED","wajah","distracted_2", lambda: gif_frames(distracted)),
    ("GIF_LOVE","wajah","dumb_love", lambda: gif_frames(love)),
    ("GIF_HADOUKEN","gundam","hadouken_hit", lambda: gif_frames(hadouken)),
    ("GIF_LAUGH","wajah","awkward_laugh", lambda: gif_frames(laugh)),
    ("GIF_CRY","wajah","crying_smile", lambda: gif_frames(cry)),
    ("GIF_KEEP","intro","keep_it_up", lambda: gif_frames(keep)),
    ("GIF_SNEEZE","wajah","big_sneeze", lambda: gif_frames(sneeze)),
    ("GIF_BLADE","gundam","blade", lambda: gif_frames(blade)),
    ("GIF_PINKY","anime","pinky", lambda: gif_frames(pinky)),
]
g=["#pragma once","#include <Arduino.h>"]
for name,theme,stem,fb in assets:
    raw=load_gif(stem, fb)
    print(name, stem, len(raw))
    g.append(dump(name,raw))
g.append("struct DefaultGif { const char *theme; const char *stem; const uint8_t *data; int len; };")
g.append("static const DefaultGif DEFAULT_GIFS[] = {")
for name,theme,stem,_ in assets:
    g.append(f'  {{"{theme}","{stem}",{name},{name}_LEN}},')
g.append("};")
g.append(f"static const int DEFAULT_GIF_COUNT = {len(assets)};")
(inc/"defaults_gif.h").write_text("\n".join(g)+"\n")
sr=8000
notes=[(523,0.10),(659,0.10),(784,0.14),(1046,0.16)]
samples=[]
for freq,leng in notes:
    nn=int(sr*leng)
    for i in range(nn):
        env=min(1.0,i/70.0)*min(1.0,(nn-i)/100.0)
        samples.append(int(10000*env*math.sin(2*math.pi*freq*i/sr)))
pcm=b"".join(struct.pack("<h",s) for s in samples)
(inc/"jingle.h").write_text("\n".join(["#pragma once","#include <Arduino.h>",f"const int JINGLE_SR={sr};",dump("JINGLE_PCM",pcm)])+"\n")
print("embedded ok")
