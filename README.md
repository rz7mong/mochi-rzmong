# 🍡 Mochi rzmong

Palm-sized **ESP32-C3** desk buddy: animated **GIF** faces on ST7789, touch reactions, and short **WAV** SFX through MAX98357.

> Inspired by expressive desk toys (e.g. Dasai-style faces). This is an **independent open-source project**, not affiliated with any commercial brand.

| | |
| --- | --- |
| 🏷️ Brand | **rzmong** |
| 📌 Version | **0.2.8** |
| 📜 License | [MIT](LICENSE) |
| 🌐 Install | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📦 Theme pack | [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) |

## English summary

ESP32-C3 Super Mini + ST7789 240×240 + MAX98357 I2S amp. **GIF only** on device (no MP4). **WAV 16-bit** SFX from SD or flash jingle (no MP3). Wi-Fi AP: SSID `rzmong mochi`, password `rzmong123`. Theme pack in GitHub Releases. Flash from Chrome/Edge.

---

## ✨ Fitur

| Fitur | Keterangan |
| --- | --- |
| 🎬 Animasi | **GIF saja** (240×240) |
| 👆 Reaksi sentuh | 10 ekspresi + SFX |
| 🔊 SFX | **WAV 16-bit** SD → else jingle flash |
| 🎨 Tema SD | Web = default · LCD = manual jika SD |
| 📶 Wi-Fi AP | SSID **`rzmong mochi`** · sandi **`rzmong123`** |

## ⚠️ Keterbatasan

- Tidak ada decoder **MP3** / pemutar musik SD penuh
- Tidak putar **MP4** di ESP32
- Halaman pengaturan AP **tanpa autentikasi**

## 🎨 Pilih tema

| Tempat | Cara |
| --- | --- |
| **Web** | Wi-Fi → [Pengaturan](https://rz7mong.github.io/mochi-rzmong/pengaturan.html) → Simpan |
| **ESP32 + SD** | Ketuk 2× → **Pilih tema** |

Pack: [assets-v1](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1)

## 👆 Gestur

| Gestur | Ambang | Aksi |
| --- | --- | --- |
| Ketuk 1× | < 900 ms | GIF reaksi + SFX |
| Ketuk 2× | 2 ketuk cepat | Menu |
| Tahan | ≥ 900 ms | Bisu / bunyi |

## 🔌 Pin map

| Modul | Pin | Catatan |
| --- | --- | --- |
| Touch | **GPIO1** | |
| SD | SCK **4**, MOSI **6**, MISO **3**, CS **5** | SPI berbagi dengan TFT |
| TFT | SCLK **4**, MOSI **6**, CS **7**, DC **10**, RST **0** | |
| I2S | BCLK **21**, LRC **20**, DIN **8** | GPIO8 = strapping; jangan tarik LOW saat reset |
| Hindari di boot | **GPIO2**, **GPIO9** | |

## ⚡ Power

`LiPo → TP4056 (+ DW01) → Saklar → VIN ESP32 + MAX98357` · 3V3 → LCD/SD/touch  
Speaker hanya lewat MAX98357.

## 📶 Wi-Fi

| | |
| --- | --- |
| SSID | **`rzmong mochi`** |
| Password | **`rzmong123`** |

Menu LCD **Info Wi-Fi AP** menampilkan keduanya. Ganti di firmware (`MOCHI_AP_NAME` / `MOCHI_AP_PASS`) bila perlu.

## 🛠️ Build

Python 3.11+ · PlatformIO 6.x · `pio run -e esp32-c3-super-mini`  
Flash: [instalasi](https://rz7mong.github.io/mochi-rzmong/) (Chrome/Edge).

## 🧰 Troubleshooting

Layar putih → RST=0 · SD gagal → MISO=3 · Tidak ada suara → DIN=8 + amp · Flash gagal → Chrome + BOOT

## 📚 Lisensi

**MIT** · kredits: TFT_eSPI, AnimatedGIF, ArduinoJson, ChronosESP32

Lihat [CHANGELOG.md](CHANGELOG.md).

Copyright © 2026 rzmong · MIT
