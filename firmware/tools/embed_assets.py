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

def face(d, i, mouth=20, eye=0):
    d.ellipse((40,30,200,210), fill=5)
    d.ellipse((70,80,110,120), fill=0)
    d.ellipse((130,80,170,120), fill=0)
    d.ellipse((82,92+eye,98,108+eye), fill=3)
    d.ellipse((142,92+eye,158,108+eye), fill=3)
    d.ellipse((90,140,150,140+mouth), fill=1)

def yelling(d,i,n): face(d,i,mouth=20+(i%2)*22, eye=(i%2)*3)
def distracted(d,i,n):
    face(d,i,mouth=8, eye=0)
    d.ellipse((88+i*6,92,104+i*6,108), fill=3)
def love(d,i,n):
    face(d,i,mouth=12, eye=0)
    d.ellipse((100,40-i*2,140,80-i*2), fill=1)
def hadouken(d,i,n):
    d.rectangle((20,40,220,200), fill=6)
    d.ellipse((70,70,170,170), fill=4)
    d.ellipse((90,90,150,150), fill=3)
    d.ellipse((160+i*8,100,200+i*8,140), fill=2)
def laugh(d,i,n): face(d,i,mouth=16+(i%2)*20, eye=-2)
def cry(d,i,n):
    face(d,i,mouth=6, eye=2)
    d.rectangle((80,120,90,120+i*10), fill=4)
    d.rectangle((150,120,160,120+i*10), fill=4)
def keep(d,i,n):
    r=40+i*10
    d.ellipse((120-r,120-r,120+r,120+r), outline=2, width=8)
def sneeze(d,i,n): face(d,i,mouth=8+i*10, eye=-i*2)
def blade(d,i,n):
    d.rectangle((30,30,210,210), fill=6)
    d.polygon([(120,40),(180,200-i*8),(60,200-i*8)], fill=4)
def pinky(d,i,n):
    d.ellipse((50,40,190,200), fill=7)
    d.ellipse((80,90,110,120), fill=3)
    d.ellipse((130,90,160,120), fill=3)
    d.arc((90,130,150,170), start=0, end=180, fill=1)

assets = [
    ("GIF_YELLING","wajah","yelling",gif_frames(yelling)),
    ("GIF_DISTRACTED","wajah","distracted_2",gif_frames(distracted)),
    ("GIF_LOVE","wajah","dumb_love",gif_frames(love)),
    ("GIF_HADOUKEN","gundam","hadouken_hit",gif_frames(hadouken)),
    ("GIF_LAUGH","wajah","awkward_laugh",gif_frames(laugh)),
    ("GIF_CRY","wajah","crying_smile",gif_frames(cry)),
    ("GIF_KEEP","intro","keep_it_up",gif_frames(keep)),
    ("GIF_SNEEZE","wajah","big_sneeze",gif_frames(sneeze)),
    ("GIF_BLADE","gundam","blade",gif_frames(blade)),
    ("GIF_PINKY","anime","pinky",gif_frames(pinky)),
]
g=["#pragma once","#include <Arduino.h>"]
for name,theme,stem,raw in assets:
    print(name,len(raw)); g.append(dump(name,raw))
g.append("struct DefaultGif { const char *theme; const char *stem; const uint8_t *data; int len; };")
g.append("static const DefaultGif DEFAULT_GIFS[] = {")
for name,theme,stem,raw in assets:
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
