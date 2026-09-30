# Mochi rzmong

[![Build firmware](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml/badge.svg)](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Desk buddy **ESP32-C3 Super Mini** + LCD **ST7789 1.3" 240×240** (PCB 23×40 mm): wajah **GIF**, reaksi sentuh, **SFX WAV**. Proyek open-source independen — **terinspirasi** Dasai Mochi, **bukan** produk resmi / clone berlisensi.

**Firmware: 0.5.1** · **MIT © rzmong** · English: [README.en.md](README.en.md)

Di perangkat: **GIF + WAV 16-bit saja** (tidak ada pemutar MP4, tidak ada decoder MP3).

## Mulai cepat

1. Chrome / Edge → [Instalasi firmware 0.5.1](https://rz7mong.github.io/mochi-rzmong/) (tahan BOOT, colok USB-C).
2. Wi-Fi AP default: **`rzmong mochi` / `rzmong123`** — sandi lab; **ganti** `MOCHI_AP_PASS` di firmware lalu flash ulang sebelum dipakai di tempat umum.
3. Pengaturan (disarankan): **`http://192.168.4.1/`** di AP perangkat.
4. Pack tema: [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) → ekstrak ke root SD FAT32 (`gif/` + `sfx/`).

## Tautan

| | |
| --- | --- |
| Instalasi | https://rz7mong.github.io/mochi-rzmong/ |
| Merakit + pin | [docs/hardware.html](https://rz7mong.github.io/mochi-rzmong/hardware.html) |
| Panduan pakai | [docs/panduan.html](https://rz7mong.github.io/mochi-rzmong/panduan.html) |
| Studio (convert) | [docs/studio.html](https://rz7mong.github.io/mochi-rzmong/studio.html) |
| Pengaturan online | [docs/pengaturan.html](https://rz7mong.github.io/mochi-rzmong/pengaturan.html) |
| Handoff | [HANDOFF.md](HANDOFF.md) · [halaman](https://rz7mong.github.io/mochi-rzmong/handoff.html) |
| Case STL | [case/](case/) |
| Konstanta | [PRODUCT.md](PRODUCT.md) |

`thietlap.html` hanya redirect ke `pengaturan.html`.

## Wiring firmware 0.5.1

```
ESP32-C3 Super Mini
  Touch OUT → GPIO1
  SD  SCK=4  MOSI=6  MISO=3  CS=5     (SPI berbagi dengan TFT)
  TFT SCLK=4 MOSI=6  CS=7    DC=10  RST=0   BLK→3V3
  I2S BCLK=21  LRC=20  DIN=8          (MAX98357; speaker ke OUT amp)
  GPIO2 dan GPIO9 — jangan disolder (strapping)
```

**Bukan “boot-safe”.** GPIO8 (DIN) adalah pin strapping C3. GPIO20/21 adalah UART0 — log boot bisa bocor ke I2S dan terdengar “plok” di speaker. Uji di hardware; pakai USB CDC, jangan andalkan UART0.

Blueprint lengkap: [hardware.html](https://rz7mong.github.io/mochi-rzmong/hardware.html).

## Troubleshooting singkat

| Gejala | Cek |
| --- | --- |
| Port tidak muncul di Chrome | Pakai **Chrome/Edge** (bukan Safari / in-app). Tahan **BOOT**, colok USB-C, lepas BOOT. Coba kabel data lain. |
| Wi-Fi tidak ketemu | Flash **0.5.1**. SSID **`rzmong mochi`**, bukan `Mochi-rzmong`. |
| Sandi ditolak | Default **`rzmong123`**, bukan `rzmong24`. |
| Layar putih/hitam | RST=**0**, CS=7, DC=10, SCLK=4, MOSI=6, BLK=3V3 |
| SD gagal | FAT32, MISO=**3**, CS=5 — bukan GPIO2 |
| Bunyi plok saat boot | Normal-ish: UART0 di 20/21 + strapping GPIO8. Jangan tarik DIN ke GND. |
| Upload dari Pages gagal | Mixed content. Upload lewat `http://192.168.4.1/` |

## Media

Studio butuh internet (FFmpeg.wasm). Setelah file jadi, sambung AP Mochi lalu unggah di captive (same-origin).

Pasangan: `/gif/<tema>/<stem>.gif` + `/sfx/<tema>/<stem>.wav`

## Build

```bash
cd firmware
python tools/embed_assets.py
pio run -e esp32-c3-super-mini
```

## Lisensi

**MIT © rzmong** — lihat [LICENSE](LICENSE) dan [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) (ChronosESP32 / fbiego).
