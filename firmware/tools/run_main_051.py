#!/usr/bin/env python3
import base64
from pathlib import Path
root = Path("firmware/tools/main_051")
b64 = "".join((root/f"p{i}.b64").read_text() for i in range(5))
Path("firmware/src/main.cpp").write_text(base64.b64decode(b64).decode())
print("wrote", Path("firmware/src/main.cpp").stat().st_size)
