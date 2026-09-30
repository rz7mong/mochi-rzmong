# 🍡 Mochi rzmong — handoff AI

- Repo: https://github.com/rz7mong/mochi-rzmong
- Situs: https://rz7mong.github.io/mochi-rzmong/
- Versi: **0.2.4**
- Jangan hapus merek rzmong. Ketuk 1× = reaksi, bukan ganti tema.

## Batas fitur (jangan overclaim)

- Animasi perangkat: **GIF saja** (bukan MP4)
- SFX perangkat: **WAV 16-bit** dari `/sfx/` atau jingle flash (bukan MP3 player)
- Speaker: hanya lewat **MAX98357**, bukan GPIO langsung

## Gestur (main.cpp)

- Ketuk 1× (hold < 900 ms) → GIF reaksi + SFX
- Ketuk 2× → menu
- Tahan **≥ 900 ms** → bisu/bunyi

## Menu reaksi

- **Reaksi acak/tetap**: mode `acak` vs `tetap`
- **Model reaksi**: pilih 1 dari 10 + set mode `tetap`

## Pin boot-safe

Touch=1, MISO=3, CS=5, SCK=4, MOSI=6, TFT CS=7, RST=0, DC=10, DIN=8, LRC=20, BCLK=21. GPIO2/9 kosong.

## Build

Python 3.11+, PlatformIO, `espressif32`, board `esp32-c3-devkitm-1`.
Libs: TFT_eSPI^2.5.43, AnimatedGIF^2.1.1, ChronosESP32^1.8.0, ArduinoJson^7.2.1.

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```
