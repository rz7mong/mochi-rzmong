# 🍡 Mochi rzmong

Palm-sized **ESP32-C3** desk buddy: animated **GIF** faces on ST7789, touch reactions, and short **WAV** SFX through MAX98357.

> Inspired by expressive desk toys (e.g. Dasai-style faces). This is an **independent open-source project**, not affiliated with any commercial brand.

| | |
| --- | --- |
| 🏷️ Brand | **rzmong** |
| 📌 Version | **0.2.7** |
| 📜 License | [MIT](LICENSE) |
| 🌐 Install | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📦 Theme pack | [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) |

## English summary

ESP32-C3 Super Mini + ST7789 240×240 + MAX98357 I2S amp. **GIF only** on device (no MP4 player). **WAV 16-bit** SFX from SD or flash jingle (no MP3 decoder). Wi-Fi AP password is derived from the device MAC (`rz` + last 4 hex). Theme pack in GitHub Releases. Flash from Chrome/Edge via the install page.

---

## ✨ Fitur

| Fitur | Keterangan |
| --- | --- |
| 🎬 Animasi | **GIF saja** (240×240). Bukan pemutar MP4 di ESP32. |
| 👆 Reaksi sentuh | 10 ekspresi di flash + SFX (mode acak/tetap) |
| 🔊 SFX | **WAV 16-bit** di SD `/sfx/` → else jingle flash |
| 🎨 Tema SD | 9 kategori; pilih di **web** (default) atau **LCD** (manual jika SD ada) |
| 📋 Menu LCD | 16 baris |
| 📶 Wi-Fi AP | SSID `Mochi-rzmong` · sandi `rz`+MAC (lihat Info Wi-Fi) |

## ⚠️ Keterbatasan

- Decoder **MP3** / pemutar musik SD penuh — tidak ada
- Putar **MP4** di ESP32 — tidak ada (Studio web: konversi MP4→GIF)
- Halaman pengaturan AP **tanpa autentikasi**

## 🎨 Pilih tema

| Tempat | Cara |
| --- | --- |
| **Web** | Wi-Fi Mochi → [Pengaturan](https://rz7mong.github.io/mochi-rzmong/pengaturan.html) → pilih tema → **Simpan** |
| **ESP32 + SD** | Ketuk 2× → **Pilih tema** |

Pack: [Releases / assets-v1](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) → extract ke root microSD FAT32.

## 👆 Gestur

| Gestur | Ambang | Aksi |
| --- | --- | --- |
| Ketuk 1× | lepas < 900 ms | GIF reaksi + SFX |
| Ketuk 2× | 2 ketuk cepat | Menu PENGATURAN |
| Tahan | ≥ 900 ms | Bisu / bunyi |

## 🔌 Pin map

| Modul | Pin ESP32-C3 | Catatan |
| --- | --- | --- |
| Touch (TTP223) | OUT → **GPIO1** | Aman |
| SD SPI | SCK **4**, MOSI **6**, MISO **3**, CS **5** | SPI **berbagi** SCK/MOSI dengan TFT |
| TFT ST7789 | SCLK **4**, MOSI **6**, CS **7**, DC **10**, RST **0** | SCK/MOSI sama dengan SD |
| I2S MAX98357 | BCLK **21**, LRC **20**, DIN **8** | Lihat catatan di bawah |
| Hindari tarik di boot | **GPIO2**, **GPIO9** | Strapping boot mode |

**Catatan pin (ESP32-C3):**
- **GPIO8** (I2S DIN) adalah *strapping pin* dan sering ke LED onboard Super Mini. Setelah boot boleh dipakai; **jangan** tarik LOW saat reset. Amp MAX98357 DIN biasanya high-Z saat idle — uji board Anda.
- **GPIO20 / GPIO21** = UART0 RX/TX default. Firmware memakai **USB CDC** untuk log/flash lewat USB, sehingga 20/21 dipakai I2S. Jangan andalkan Serial UART0 di pin itu bersamaan dengan I2S.
- Klaim “boot-safe penuh” **tidak absolut** untuk GPIO8.

Detail: [docs/hardware.html](https://rz7mong.github.io/mochi-rzmong/hardware.html)

## ⚡ Power

`LiPo → TP4056 **(+ proteksi DW01/8205A)** → Saklar → VIN ESP32 + VIN MAX98357` · 3V3 → LCD / SD / touch

Pakai modul charger **berproteksi** (bukan TP4056 polos tanpa DW01) agar LiPo tidak over-discharge.

Speaker **hanya** lewat MAX98357 (jangan GPIO langsung).

## 📶 Wi-Fi (keamanan)

- SSID: `Mochi-rzmong`
- Password: **`rz` + 4 hex terakhir MAC** (contoh `rz3a7f`). Menu LCD **Info Wi-Fi AP** atau `GET /api/status` → `ap_pass`.
- Pengaturan **tanpa login** — jangan pakai di lingkungan tidak terpercaya tanpa mengubah firmware.

## 🛠️ Build

| Item | Nilai |
| --- | --- |
| Python | **3.11+** |
| PlatformIO | **6.x** |
| Platform | `espressif32` · board `esp32-c3-devkitm-1` |
| Libs | TFT_eSPI ^2.5.43, AnimatedGIF ^2.1.1, ChronosESP32 ^1.8.0, ArduinoJson ^7.2.1 |

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```

Flash browser: [instalasi](https://rz7mong.github.io/mochi-rzmong/) — **Chrome atau Edge** + Web Serial.

## 🧰 Troubleshooting

| Gejala | Cek |
| --- | --- |
| Layar putih / hitam | RST=**0**, CS=7, DC=10, SCLK=4, MOSI=6 |
| SD tidak terbaca | FAT32, MISO=**3**, CS=5; jangan GPIO2 |
| Tidak ada suara | DIN=8 → MAX98357; speaker ke OUT amp; volume |
| Gagal boot / flash | Jangan tarik GPIO8 LOW; GPIO2/9 bebas |
| Tidak bisa flash | Chrome/Edge, tahan BOOT |

## 📚 Kredits & lisensi

- Kode: **MIT** — [LICENSE](LICENSE)
- [TFT_eSPI](https://github.com/Bodmer/TFT_eSPI) · [AnimatedGIF](https://github.com/bitbank2/AnimatedGIF) · [ArduinoJson](https://github.com/bblanchon/ArduinoJson) · [ChronosESP32](https://github.com/fbiego/ChronosESP32)

## 📝 Changelog

Lihat [CHANGELOG.md](CHANGELOG.md).

---

Copyright © 2026 rzmong · MIT License
