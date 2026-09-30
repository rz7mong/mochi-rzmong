# 🍡 Mochi rzmong

[![Build firmware](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml/badge.svg)](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml)

Teman meja **ESP32-C3**: wajah **GIF**, reaksi sentuh, SFX **WAV** (MAX98357).

> Open-source **independen**. Tidak berafiliasi dengan merek komersial. English: [README.en.md](README.en.md).

| | |
| --- | --- |
| 📌 Versi | **0.3.0** — [PRODUCT.md](PRODUCT.md) |
| 📜 Lisensi | [MIT](LICENSE) · [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |
| 🌐 Instalasi | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📦 Tema | [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) |
| 📶 Wi-Fi | **`rzmong mochi`** / **`rzmong123`** |
| ⚙️ Pengaturan | **`http://192.168.4.1/`** (di perangkat, offline) |

## Fitur

| | |
| --- | --- |
| GIF 240×240 | Bukan MP4 di ESP32 |
| SFX WAV 16-bit | Bukan MP3 |
| Tema web/LCD | Default di NVS; LCD jika SD |
| Chronos (opsional) | BLE companion ([ChronosESP32](https://github.com/fbiego/ChronosESP32)); menu **Chronos**. Satu radio 2,4 GHz — uji lag bila AP+BLE aktif bersamaan |

## Wi-Fi & keamanan

- Default: SSID `rzmong mochi`, sandi `rzmong123` (ganti di `MochiRzmong.h` lalu rebuild).
- API HTTP di AP **tanpa autentikasi** — siapa pun di jaringan AP bisa `POST /api/settings`.
- **Erase** saat instal menghapus **NVS** (tema, volume, Chronos, dll.).

## Pengaturan

1. Sambung ke AP → buka **http://192.168.4.1/** (disarankan di HP).
2. Atau Pages [pengaturan.html](https://rz7mong.github.io/mochi-rzmong/pengaturan.html) (butuh internet).
3. LCD: ketuk 2×.

## Pin (singkat)

Touch=1 · SD SCK/MOSI/MISO/CS=4/6/3/5 · TFT CS/DC/RST=7/10/0 · I2S 21/20/8 · **GPIO2 & 9 tidak di-wiring** · GPIO8 jangan LOW saat reset.

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
