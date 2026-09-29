#!/usr/bin/env python3
import json, base64, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
inc = root / "include"
inc.mkdir(exist_ok=True)
meta = json.loads((root / "assets" / "meta.json").read_text())

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

g = ["#pragma once", "#include <Arduino.h>"]
for name, theme, stem in meta["meta"]:
    raw = base64.b64decode((root / "assets" / f"{name}.b64").read_text())
    g.append(dump(name, raw))
g.append("struct DefaultGif { const char *theme; const char *stem; const uint8_t *data; int len; };")
g.append("static const DefaultGif DEFAULT_GIFS[] = {")
for name, theme, stem in meta["meta"]:
    g.append(f'  {{"{theme}", "{stem}", {name}, {name}_LEN}},')
g.append("};")
g.append(f"static const int DEFAULT_GIF_COUNT = {len(meta['meta'])};")
(inc / "defaults_gif.h").write_text("\n".join(g) + "\n")
pcm = base64.b64decode((root / "assets" / "JINGLE_PCM.b64").read_text())
(inc / "jingle.h").write_text("\n".join(["#pragma once", "#include <Arduino.h>", f"const int JINGLE_SR = {meta['sr']};", dump("JINGLE_PCM", pcm)]) + "\n")
print("embedded ok")
try:
    Import("env")
except Exception:
    pass
