# 🍡 Mochi rzmong

Palm-sized **ESP32-C3** desk buddy: **GIF** faces on ST7789, touch reactions, **WAV** SFX via MAX98357.

> Independent open-source project inspired by expressive desk toys. **Not affiliated** with any commercial brand.

| | |
| --- | --- |
| 🏷️ Brand | **rzmong** |
| 📌 Version | **0.2.8** — see [PRODUCT.md](PRODUCT.md) |
| 📜 License | [MIT](LICENSE) |
| 🌐 Install | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📦 Theme pack | [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) only |
| 📶 Wi-Fi | SSID **`rzmong mochi`** · password **`rzmong123`** |

## English summary

ESP32-C3 Super Mini + ST7789 240×240 + MAX98357. **GIF + WAV 16-bit only** on device (no MP4 player, no MP3 decoder). Flash with Chrome/Edge. Change AP credentials in `firmware/include/MochiRzmong.h` (`MOCHI_AP_NAME` / `MOCHI_AP_PASS`) then rebuild.

---

## ✨ Fitur

| Fitur | Keterangan |
| --- | --- |
| 🎬 Animasi | **GIF** 240×240 (bukan MP4 di ESP32) |
| 👆 Reaksi | 10 ekspresi + SFX |
| 🔊 SFX | **WAV 16-bit** di SD, fallback jingle flash |
| 🎨 Tema | Web = default · LCD = manual jika SD terpasang |
| 📶 AP | `rzmong mochi` / `rzmong123` |

## ⚠️ Keterbatasan

- Tidak ada decoder **MP3** / pemutar musik SD penuh
- Tidak memutar **MP4** di perangkat
- Halaman pengaturan AP **tanpa login**

## 📶 Wi-Fi

| | |
| --- | --- |
| SSID | **`rzmong mochi`** |
| Password | **`rzmong123`** |

Sumber tunggal: [PRODUCT.md](PRODUCT.md) dan `MOCHI_AP_*` di firmware. Menu LCD **Info Wi-Fi AP** menampilkan nilai yang sama.

## 🎨 Tema & pack

| Tempat | Cara |
| --- | --- |
| Web | [pengaturan.html](https://rz7mong.github.io/mochi-rzmong/pengaturan.html) → Simpan |
| ESP32 + SD | Ketuk 2× → **Pilih tema** |

Unduh pack **hanya** dari [Releases / assets-v1](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) → extract ke root microSD FAT32 (`gif/`, `sfx/`, `themes.json`).

## 👆 Gestur

| Gestur | Ambang | Aksi |
| --- | --- | --- |
| Ketuk 1× | &lt; 900 ms | GIF reaksi + SFX |
| Ketuk 2× | 2 ketuk cepat | Menu |
| Tahan | ≥ 900 ms | Bisu / bunyi |

## 🔌 Pin map

| Modul | GPIO | Catatan |
| --- | --- | --- |
| Touch TTP223 | **1** | |
| SD SPI | SCK **4**, MOSI **6**, MISO **3**, CS **5** | SCK/MOSI **berbagi** dengan TFT |
| TFT ST7789 | SCLK **4**, MOSI **6**, CS **7**, DC **10**, RST **0** | |
| I2S MAX98357 | BCLK **21**, LRC **20**, DIN **8** | Lihat di bawah |
| Hindari tarik di boot | **2**, **9** | Strapping |

**GPIO8** = strapping pin (+ sering LED Super Mini). Jangan tarik **LOW** saat reset. Setelah boot boleh dipakai sebagai DIN.  
**GPIO20/21** = UART0 default; firmware memakai **USB CDC**, jadi pin itu dipakai I2S (bukan Serial UART0).

Detail: [docs/hardware.html](https://rz7mong.github.io/mochi-rzmong/hardware.html)

## ⚡ Power

```
LiPo → TP4056 (+ proteksi DW01/8205A) → Saklar → VIN ESP32 + VIN MAX98357
ESP32 3V3 → LCD / SD / touch
```

Pakai modul charger **berproteksi**. Speaker **hanya** lewat MAX98357.

## 🛠️ Build & upload (PlatformIO)

| Item | Nilai |
| --- | --- |
| Python | 3.11+ |
| PlatformIO | 6.x |
| Env | `esp32-c3-super-mini` |

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware
pio run -e esp32-c3-super-mini
pio run -e esp32-c3-super-mini -t upload   # USB; tahan BOOT jika perlu
```

Atau flash dari browser: [halaman instalasi](https://rz7mong.github.io/mochi-rzmong/) (**Chrome / Edge** + Web Serial).

Ganti Wi-Fi: edit `MOCHI_AP_NAME` / `MOCHI_AP_PASS` di `firmware/include/MochiRzmong.h` → rebuild → flash.

## 🧰 Troubleshooting

| Gejala | Cek |
| --- | --- |
| Layar putih/hitam | RST=0, CS=7, DC=10, SCLK=4, MOSI=6 |
| SD gagal | FAT32, MISO=3, CS=5 |
| Tidak ada suara | DIN=8 → amp; speaker ke OUT+/−; volume menu |
| Gagal boot/flash | Jangan tarik GPIO8 LOW; GPIO2/9 bebas; Chrome + BOOT |
| Wi-Fi salah sandi | SSID `rzmong mochi` / `rzmong123` (bukan kredensial lama) |

## 📚 Lisensi & aset

- Kode: **MIT** — [LICENSE](LICENSE)
- Library: TFT_eSPI, AnimatedGIF, ArduinoJson, ChronosESP32 (masing-masing lisensinya)
- Pastikan GIF/SFX yang Anda distribusikan **berhak** Anda sebarkan (buatan sendiri atau berlisensi)

## 📝 Changelog

[CHANGELOG.md](CHANGELOG.md) · konstanta produk: [PRODUCT.md](PRODUCT.md)

---

Copyright © 2026 rzmong · MIT License
