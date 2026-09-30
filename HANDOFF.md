# 🍡 Mochi rzmong — handoff AI

- Repo: https://github.com/rz7mong/mochi-rzmong
- Situs: https://rz7mong.github.io/mochi-rzmong/
- Versi: **0.2.6**
- Tema pack: https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1
- Jangan hapus merek rzmong. Ketuk 1× = reaksi, bukan ganti tema.

## Tema dual-select

- **Web** (`thietlap.html`): pilih tema → Simpan = default di Preferences
- **LCD**: ketuk 2× → Pilih tema (butuh SD)
- API: GET `/api/status`, GET `/api/themes`, POST `/api/settings`

## Batas fitur

- Animasi: **GIF saja** (bukan MP4)
- SFX: **WAV 16-bit** dari `/sfx/` atau jingle flash (bukan MP3)
- Speaker: hanya **MAX98357**, bukan GPIO

## Gestur

- Ketuk 1× (hold < 900 ms) → GIF reaksi + SFX
- Ketuk 2× → menu
- Tahan **≥ 900 ms** → bisu/bunyi

## Pin boot-safe

Touch=1, MISO=3, CS=5, SCK=4, MOSI=6, TFT CS=7, RST=0, DC=10, DIN=8, LRC=20, BCLK=21. GPIO2/9 kosong.

## Build

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```

Libs: TFT_eSPI^2.5.43, AnimatedGIF^2.1.1, ChronosESP32^1.8.0, ArduinoJson^7.2.1.
