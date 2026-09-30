# 🍡 Mochi rzmong

[![Build firmware](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml/badge.svg)](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml)

ESP32-C3 desk buddy: wajah GIF, reaksi sentuh, SFX WAV, tema di SD.

| | |
| --- | --- |
| 📌 Versi | **0.4.7** — [PRODUCT.md](PRODUCT.md) |
| 📜 Lisensi | [MIT](LICENSE) · [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |
| 🌐 Instalasi | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📦 Tema | [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) |
| 📶 Wi-Fi | **`rzmong mochi`** / **`rzmong123`** |
| ⚙️ Pengaturan | **`http://192.168.4.1/`** (di perangkat, offline — disarankan) |
| 🎨 Studio | [studio.html](https://rz7mong.github.io/mochi-rzmong/studio.html) convert + upload |

## Fitur

| | |
| --- | --- |
| GIF 240×240 | Bukan MP4 di ESP32 · max **~599 KB** |
| SFX WAV 16-bit | Bukan MP3 · pasangan sama `tema`+`stem` |
| Tema web/LCD | Default di NVS; LCD jika SD |
| Chronos (opsional) | BLE companion; menu **Chronos** |
| Studio Upload | MP4→GIF+WAV di browser, `POST /api/upload` ke SD |

## Wi-Fi dan keamanan

- Default: SSID `rzmong mochi`, sandi `rzmong123` (ganti di `MochiRzmong.h` lalu rebuild).
- API HTTP di AP **tanpa autentikasi** — siapa pun di AP bisa `POST /api/settings` dan `POST /api/upload`.
- **Erase** saat instal menghapus **NVS** (tema, volume, Chronos, dll.).

## Pengaturan

1. **Disarankan:** sambung AP → **http://192.168.4.1/** (offline, tanpa mixed content).
2. Alternatif: [pengaturan.html](https://rz7mong.github.io/mochi-rzmong/pengaturan.html) di Pages — butuh internet; dari `https://` ke `http://192.168.4.1` sering diblokir browser.
3. LCD: ketuk 2×.

## Studio (convert + upload)

1. Flash firmware **≥ 0.4.5** (ideal **0.4.7**).
2. Sambung Wi-Fi **`rzmong mochi`** / **`rzmong123`**.
3. Buka [Studio](https://rz7mong.github.io/mochi-rzmong/studio.html) (butuh internet untuk FFmpeg.wasm).
4. Convert → preview → **Save** atau **Upload** (SD wajib untuk upload).
5. File: `/gif/<tema>/<stem>.gif` dan `/sfx/<tema>/<stem>.wav`.

Tanpa SD, upload gagal (`sd_not_ready`). Max **599 KB** per file.

## Pin (singkat)

Touch=1 · SD SCK/MOSI/MISO/CS=4/6/3/5 · TFT CS/DC/RST=7/10/0 · I2S 21/20/8 · **GPIO2 dan 9 tidak di-wiring** · GPIO8 jangan LOW saat reset.

SPI TFT+SD berbagi; firmware pakai `sdBusy`.

## Power

LiPo → TP4056 (+DW01) → saklar → VIN. Beban saat charge bisa mengganggu terminasi isi.

## Partisi / OTA

Satu slot app (**bukan** OTA dual-slot). Update = flash ulang via USB/Web Serial.

## Build

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```

Platform: `espressif32@6.9.0`.

## Lisensi aset

Kode MIT. Media pack: hanya bagikan yang berhak Anda sebar — [ASSETS.md](ASSETS.md).

[CHANGELOG.md](CHANGELOG.md) · [docs/HANDOFF.md](docs/HANDOFF.md)
