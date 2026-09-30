# Pustaka Mochi rzmong

10 GIF reaksi **tersimpan di flash ESP32** (PROGMEM), bukan hanya SD.

Urutan putar saat sentuh:
1. Array flash `DEFAULT_GIFS[]`
2. Baru SD `/gif/<tema>/<stem>.gif` jika flash gagal

File sumber: `firmware/assets/react/` + `firmware/tools/react_b64/`.
Compile: `python firmware/tools/embed_assets.py` lalu PlatformIO.
