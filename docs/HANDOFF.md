# Handoff (internal / AI)

Bukan panduan pengguna — lihat [README](../README.md) dan [PRODUCT.md](../PRODUCT.md).

| Key | Value |
| --- | --- |
| Version | **0.2.9** |
| Brand | `rzmong` |
| AP SSID | `rzmong mochi` |
| AP password | `rzmong123` |
| Settings UI | `docs/pengaturan.html` |
| Legacy URL | `docs/thietlap.html` → redirect |
| Theme pack | Release `assets-v1` |
| Binary | `docs/firmware/firmware.bin` + `manifest.json` |
| Install | https://rz7mong.github.io/mochi-rzmong/ |

Firmware constants: `firmware/include/MochiRzmong.h` (`MOCHI_VERSION`, `MOCHI_AP_NAME`, `MOCHI_AP_PASS`).

## Theme dual-select

- Web (`pengaturan.html`): save → Preferences default
- LCD: double-tap → **Pilih tema** (needs SD)
- API: `GET /api/status`, `GET /api/themes`, `POST /api/settings`
- `/api/themes` returns **503** `sd_busy` while SD GIF/WAV is active

## Limits

- GIF only · WAV 16-bit or jingle · MAX98357 only · no MP3/MP4 on device
- Optional LCD brand mark (menu **Merek LCD**)

## Pins

| Function | GPIO |
| --- | --- |
| Touch | 1 |
| SD SCK / MOSI / MISO / CS | 4 / 6 / 3 / 5 |
| TFT SCLK / MOSI / CS / DC / RST | 4 / 6 / 7 / 10 / 0 |
| I2S BCLK / LRC / DIN | 21 / 20 / 8 |

- Leave **GPIO2** and **GPIO9** unconnected (do not pull LOW at boot).
- **GPIO8** is strapping + often onboard LED — do not pull LOW at reset; OK as I2S DIN after boot.
- TFT+SD share SPI; firmware uses **`sdBusy`** to avoid concurrent SD access.

## Gestures

- 1× tap (&lt; 900 ms) → react GIF + SFX
- 2× tap → menu
- Hold ≥ 900 ms → mute toggle

## Build

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
# upload: pio run -e esp32-c3-super-mini -t upload
```

Or flash from browser (Chrome/Edge) via the install page.

## Docs map

| File | Role |
| --- | --- |
| PRODUCT.md | Version + Wi-Fi source of truth |
| THIRD_PARTY_NOTICES.md | Library licenses |
| ASSETS.md | Theme pack + media rights |
| README.md | Indonesian primary |
| README.en.md | English summary |
