#!/usr/bin/env python3
from pathlib import Path
p = Path("firmware/src/main.cpp")
m = p.read_text()
if "if(taps==0) nextPart()" in m:
    print("auto-advance already"); raise SystemExit(0)
old = "  gif.close(); sdBusy=false; brandMark(); return true;\n}"
idx = m.find("bool playCurrent()")
if idx < 0:
    raise SystemExit("no playCurrent")
pos = m.find(old, idx)
if pos < 0:
    raise SystemExit("end not found")
new = "  gif.close(); sdBusy=false; brandMark();\n  if(taps==0) nextPart();\n  return true;\n}"
m = m[:pos] + new + m[pos+len(old):]
p.write_text(m)
print("auto-advance ok", len(m))
