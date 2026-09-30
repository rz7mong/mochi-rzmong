# Handoff (internal / AI)

Bukan panduan pengguna — lihat [README](../README.md) dan [PRODUCT.md](../PRODUCT.md).

| Key | Value |
| --- | --- |
| Version | **0.2.8** |
| AP SSID | `rzmong mochi` |
| AP password | `rzmong123` |
| Settings UI | `docs/pengaturan.html` |
| Theme pack | Release `assets-v1` |

Firmware constants: `firmware/include/MochiRzmong.h` (`MOCHI_VERSION`, `MOCHI_AP_NAME`, `MOCHI_AP_PASS`).

## Theme dual-select

- Web (`pengaturan.html`): save → Preferences default
- LCD: double-tap → Pilih tema (needs SD)
- API: `GET /api/status`, `GET /api/themes`, `POST /api/settings`

## Limits

- GIF only · WAV 16-bit or jingle · MAX98357 only · no MP3/MP4 on device

## Pins

Touch=1, MISO=3, CS=5, SCK=4, MOSI=6, TFT CS=7, RST=0, DC=10, DIN=8 (strapping), LRC=20, BCLK=21. Leave GPIO2/9 free.

## Build

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```
