# 🍡 Mochi rzmong

Palm-sized **ESP32-C3** desk buddy: animated **GIF** faces on ST7789, touch reactions, and short **WAV** SFX through MAX98357.

> Inspired by expressive desk toys (e.g. Dasai-style faces). This is an **independent open-source project**, not affiliated with any commercial brand.

| | |
| --- | --- |
| 🏷️ Brand | **rzmong** |
| 📌 Version | **0.2.6** |
| 📜 License | [MIT](LICENSE) |
| 🌐 Install | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📦 Theme pack | [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) |

## English summary

ESP32-C3 Super Mini + ST7789 240×240 + MAX98357 I2S amp. **GIF only** on device (no MP4 player). **WAV 16-bit** SFX from SD or flash jingle (no MP3 decoder). Default Wi-Fi AP `Mochi-rzmong` / `rzmong24` — **change the password** for anything beyond a private lab. Theme pack lives in GitHub Releases. Flash from the browser (Chrome/Edge) via the install page.

---

## ✨ Fitur

| Fitur | Keterangan |
| --- | --- |
| 🎬 Animasi | **GIF saja** (240×240). Bukan pemutar MP4 di ESP32. |
| 👆 Reaksi sentuh | 10 ekspresi di flash + SFX (mode acak/tetap) |
| 🔊 SFX | **WAV 16-bit** di SD `/sfx/` → else jingle flash |
| 🎨 Tema SD | 9 kategori; pilih di **web** (default) atau **LCD** (manual jika SD ada) |
| 📋 Menu LCD | 16 baris |
| 📶 Wi-Fi AP | Default: `Mochi-rzmong` / `rzmong24` ⚠️ ganti untuk produksi |

## ❌ Tidak didukung di perangkat

- Decoder **MP3** / pemutar musik SD penuh
- Putar **MP4** di ESP32 (Studio web bisa konversi MP4→GIF)

## 🎨 Pilih tema

| Tempat | Cara |
| --- | --- |
| **Web** | Wi-Fi Mochi → [Pengaturan](https://rz7mong.github.io/mochi-rzmong/thietlap.html) → pilih tema → **Simpan** = default |
| **ESP32 + SD** | Ketuk 2× → **Pilih tema** |

Pack: unduh dari [Releases / assets-v1](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1), extract ke root microSD FAT32 (`gif/`, `sfx/`, `themes.json`).

## 👆 Gestur

| Gestur | Ambang | Aksi |
| --- | --- | --- |
| Ketuk 1× | lepas < 900 ms | GIF reaksi + SFX |
| Ketuk 2× | 2 ketuk cepat | Menu PENGATURAN |
| Tahan | ≥ 900 ms | Bisu / bunyi |

## 🔌 Pin (boot-safe)

| Modul | Pin ESP32-C3 |
| --- | --- |
| Touch (TTP223) | OUT → **GPIO1** |
| SD SPI | SCK **4**, MOSI **6**, MISO **3**, CS **5** |
| TFT ST7789 | SCLK **4**, MOSI **6**, CS **7**, DC **10**, RST **0** |
| I2S MAX98357 | BCLK **21**, LRC **20**, DIN **8** |
| Kosong (strap) | **GPIO2**, **GPIO9** |

Detail wiring & power: [docs/hardware.html](https://rz7mong.github.io/mochi-rzmong/hardware.html)

## ⚡ Power

`LiPo → TP4056 → Saklar → VIN ESP32 + VIN MAX98357` · 3V3 → LCD / SD / touch

Speaker **hanya** lewat MAX98357 (jangan GPIO langsung).

## 📶 Wi-Fi (keamanan)

Default AP: SSID `Mochi-rzmong`, password `rzmong24`.
Ini **sandi lab/default** agar mudah di-setup. Untuk dipakai di luar meja kerja pribadi, ganti SSID/password di firmware atau batasi jangkauan. Halaman pengaturan tidak dilindungi login — siapa pun di AP bisa mengubah setting.

## 🛠️ Build

| Item | Nilai |
| --- | --- |
| Python | **3.11+** |
| PlatformIO | **6.x** (`pip install -U platformio`) |
| Platform | `espressif32` |
| Board | `esp32-c3-devkitm-1` |
| Framework | Arduino |
| Libs | TFT_eSPI ^2.5.43, AnimatedGIF ^2.1.1, ChronosESP32 ^1.8.0, ArduinoJson ^7.2.1 |

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```

Flash dari browser: [halaman instalasi](https://rz7mong.github.io/mochi-rzmong/) (Chrome/Edge + Web Serial).

## 🧰 Troubleshooting

| Gejala | Cek |
| --- | --- |
| Layar putih / hitam | RST=**0**, CS=7, DC=10, SCLK=4, MOSI=6, backlight 3V3 |
| SD tidak terbaca | FAT32, MISO=**3**, CS=5; jangan pakai GPIO2 |
| Tidak ada suara | DIN=8 → MAX98357; speaker ke **OUT+/− amp**, bukan GPIO; volume menu |
| Tidak bisa flash | Chrome/Edge, tahan BOOT saat colok USB |
| Wi-Fi tidak muncul | Tunggu boot selesai; reset; cek power 5V/USB stabil |

## 📚 Kredits & lisensi

- Kode proyek: **MIT** — lihat [LICENSE](LICENSE)
- [TFT_eSPI](https://github.com/Bodmer/TFT_eSPI) (Bodmer)
- [AnimatedGIF](https://github.com/bitbank2/AnimatedGIF) (bitbank2)
- [ArduinoJson](https://github.com/bblanchon/ArduinoJson) (bblanchon)
- [ChronosESP32](https://github.com/fbiego/ChronosESP32) (fbiego)

## 📝 Changelog

Lihat [CHANGELOG.md](CHANGELOG.md).

---

Copyright © 2026 rzmong · MIT License
