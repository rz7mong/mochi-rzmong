# Mochi rzmong

[![Build firmware](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml/badge.svg)](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Desk buddy **ESP32-C3 Super Mini** + LCD **ST7789 1.3" 240×240** (PCB 23×40 mm): wajah **GIF**, reaksi sentuh, **SFX WAV**. Proyek open-source independen — **terinspirasi** Dasai Mochi, **bukan** produk resmi / clone berlisensi.

**Firmware: 0.5.3** · **MIT © rzmong** · English: [README.en.md](README.en.md)

Satu sumber situs/installer: **https://rz7mong.github.io/mochi-rzmong/**  
(`rz7mong.github.io` tanpa path adalah arsip — jangan flash dari sana.)

Di perangkat: **GIF + WAV 16-bit saja** (tidak ada pemutar MP4, tidak ada decoder MP3).

## Mulai cepat

1. Chrome / Edge → [Instalasi firmware 0.5.3](https://rz7mong.github.io/mochi-rzmong/) (tahan BOOT, colok USB-C).
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


## Wiring firmware 0.5.3

Sumber pin: `firmware/include/MochiRzmong.h` + `User_Setup_ST7789.h`.

Diagram resmi: [docs/wiring-0.5.1.jpg](docs/wiring-0.5.1.jpg) · halaman [hardware](https://rz7mong.github.io/mochi-rzmong/hardware.html).

```
ESP32-C3 Super Mini
  Touch OUT → GPIO1
  SD  SCK=4  MOSI=6  MISO=3  CS=5     (SPI berbagi SCK/MOSI dengan TFT)
  TFT SCLK=4 MOSI=6  CS=7    DC=10  RST=0   BLK→3V3 (bukan 5V)
  I2S BCLK=21  LRC=20  DIN=8          (MAX98357; speaker ke OUT+/OUT− amp)
  GPIO2 dan GPIO9 — jangan disolder (strapping C3)
```

| Net | Apa yang disambung |
| --- | --- |
| GABUNG 3V3 | TFT VCC + BLK, SD VCC, TTP223 VCC |
| GABUNG GND | semua modul |
| GABUNG SCK GPIO4 | TFT SCL + SD SCK |
| GABUNG MOSI GPIO6 | TFT SDA + SD MOSI |
| GABUNG VIN | ESP VIN + MAX98357 VIN **setelah saklar** |

CS tidak berbagi: TFT **GPIO7** ≠ SD **GPIO5** ≠ sentuh **GPIO1** ≠ DIN **GPIO8**.

**Bukan “boot-safe”.** GPIO8 (DIN) adalah pin strapping C3. GPIO20/21 adalah UART0 — log boot bisa bocor ke I2S (“plok” di speaker). Pakai **USB CDC**, jangan andalkan UART0.

**Daya:** LiPo → TP4056 **berproteksi** (DW01/8205A) → saklar → GABUNG VIN. LCD/SD/sentuh makan **3V3 ESP**, bukan 5V.

**Amp:** pasang kapasitor **≈470 µF** (elektrolit, ≥10 V) antara **VIN MAX98357 dan GND**, sedekat mungkin ke modul. Tanpa ini amp mudah “ceklek” / brown-out saat bass.

**SD:** modul harus **native 3.3V** (bukan reader 5V / level-shifter 5V). Kartu FAT32. MISO = GPIO3, bukan GPIO2.

Blueprint + STL: [hardware.html](https://rz7mong.github.io/mochi-rzmong/hardware.html).

## Troubleshooting singkat

| Gejala | Cek |
| --- | --- |
| Port tidak muncul di Chrome | Pakai **Chrome/Edge** (bukan Safari / in-app). Tahan **BOOT**, colok USB-C, lepas BOOT. Coba kabel data lain. |
| Wi-Fi tidak ketemu | Flash **0.5.3**. SSID **`rzmong mochi`**, bukan `Mochi-rzmong`. |
| Sandi ditolak | Default **`rzmong123`**, bukan `rzmong24`. |
| Layar putih/hitam | RST=**0**, CS=7, DC=10, SCLK=4, MOSI=6, BLK=3V3 |
| SD gagal | FAT32, modul **3.3V native**, MISO=**3**, CS=5 — bukan GPIO2 |
| Amp berisik / mati saat bass | Kapasitor ≈470 µF di VIN amp |
| Bunyi plok saat boot | UART0 di 20/21 + strapping GPIO8. Jangan tarik DIN ke GND. |
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
