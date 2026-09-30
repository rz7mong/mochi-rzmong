# Handoff (internal / AI)

Catatan ringkas untuk kontributor dan asisten AI. Bukan panduan pengguna akhir — lihat [README](../README.md) dan [situs](https://rz7mong.github.io/mochi-rzmong/).

- Repo: https://github.com/rz7mong/mochi-rzmong
- Version: **0.2.6**
- Theme pack release: `assets-v1`
- Do not remove brand **rzmong**. Single tap = reaction, not theme change.

## Theme dual-select

- Web (`thietlap.html`): save theme → Preferences default
- LCD: double-tap → Pilih tema (needs SD)
- API: `GET /api/status`, `GET /api/themes`, `POST /api/settings`

## Limits

- Device animation: **GIF only**
- SFX: **WAV 16-bit** or flash jingle (no MP3)
- Speaker: **MAX98357 only**

## Gestures

- 1× tap (< 900 ms) → react GIF + SFX
- 2× tap → menu
- Hold ≥ 900 ms → mute toggle

## Pins

Touch=1, MISO=3, CS=5, SCK=4, MOSI=6, TFT CS=7, RST=0, DC=10, DIN=8, LRC=20, BCLK=21. Leave GPIO2/9 free.

## Build

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```
