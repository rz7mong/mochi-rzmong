# 🍡 Mochi rzmong

[![Build firmware](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml/badge.svg)](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml)
[![Pages](https://github.com/rz7mong/mochi-rzmong/actions/workflows/pages.yml/badge.svg)](https://github.com/rz7mong/mochi-rzmong/actions/workflows/pages.yml)

Teman meja **ESP32-C3**: wajah **GIF** di ST7789, reaksi sentuh, SFX **WAV** lewat MAX98357.

> Proyek open-source **independen**. Tidak berafiliasi dengan merek komersial mana pun. English: [README.en.md](README.en.md).

| | |
| --- | --- |
| 🏷️ Merek | **rzmong** (opsional di pojok LCD, bisa dimatikan di menu) |
| 📌 Versi | Lihat [PRODUCT.md](PRODUCT.md) (saat ini **0.2.9**) |
| 📜 Lisensi kode | [MIT](LICENSE) · [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |
| 🌐 Instalasi | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📦 Pack tema | [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) |
| 📶 Wi-Fi | SSID **`rzmong mochi`** · sandi **`rzmong123`** |

## ✨ Fitur

| Fitur | Keterangan |
| --- | --- |
| 🎬 Animasi | **GIF** 240×240 di perangkat |
| 👆 Reaksi | 10 ekspresi + SFX |
| 🔊 SFX | **WAV 16-bit** di SD, fallback jingle flash |
| 🎨 Tema | Web = default · LCD = manual jika SD ada |
| 📶 AP | `rzmong mochi` / `rzmong123` |

## ⚠️ Keterbatasan

- Tidak ada decoder **MP3** / pemutar musik SD penuh
- Tidak memutar **MP4** di ESP32
- Halaman pengaturan AP **tanpa login**

## 📶 Wi-Fi

| | |
| --- | --- |
| SSID | **`rzmong mochi`** |
| Password | **`rzmong123`** |

Ganti di `firmware/include/MochiRzmong.h` (`MOCHI_AP_NAME` / `MOCHI_AP_PASS`) → rebuild → flash.

## 🎨 Tema

| Tempat | Cara |
| --- | --- |
| Web | [pengaturan.html](https://rz7mong.github.io/mochi-rzmong/pengaturan.html) → Simpan |
| ESP32 + SD | Ketuk 2× → **Pilih tema** |

Pack: [assets-v1](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) · detail [ASSETS.md](ASSETS.md).

URL lama `thietlap.html` dialihkan ke `pengaturan.html`.

## 👆 Gestur

| Gestur | Ambang | Aksi |
| --- | --- | --- |
| Ketuk 1× | &lt; 900 ms | GIF reaksi + SFX |
| Ketuk 2× | 2 ketuk cepat | Menu |
| Tahan | ≥ 900 ms | Bisu / bunyi |

## 🔌 Pin

| Modul | GPIO | Catatan |
| --- | --- | --- |
| Touch | **1** | |
| SD | SCK **4**, MOSI **6**, MISO **3**, CS **5** | SCK/MOSI **berbagi** dengan TFT |
| TFT | SCLK **4**, MOSI **6**, CS **7**, DC **10**, RST **0** | |
| I2S | BCLK **21**, LRC **20**, DIN **8** | GPIO8 = strapping; jangan tarik LOW saat reset |
| Strapping boot | **2**, **9** | **Biarkan tidak terhubung** (atau jangan ditarik LOW saat boot) |

**Bus SPI:** TFT dan SD berbagi clock/data. Firmware mengakses SD secara bergiliran (flag `sdBusy`) agar putar GIF dari SD tidak bersamaan dengan API/SFX yang membuka file SD lain.

Detail: [docs/hardware.html](https://rz7mong.github.io/mochi-rzmong/hardware.html)

## ⚡ Power

```
LiPo → TP4056 (+ DW01/8205A) → Saklar → VIN ESP32 + VIN MAX98357
ESP32 3V3 → LCD / SD / touch
```

- Pakai modul **berproteksi** (bukan TP4056 polos).
- Beban yang tetap menyala saat *charging* dapat membuat terminasi pengisian kurang akurat; idealnya beban diputus saat charge atau gunakan modul dengan jalur beban terpisah.
- Speaker **hanya** lewat MAX98357.

## 🛠️ Build

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware
pio run -e esp32-c3-super-mini
pio run -e esp32-c3-super-mini -t upload
```

Atau flash browser (Chrome/Edge): [instalasi](https://rz7mong.github.io/mochi-rzmong/).

## 🧰 Troubleshooting

| Gejala | Cek |
| --- | --- |
| Layar putih | RST=0, CS=7, DC=10, SCLK=4, MOSI=6 |
| SD gagal | FAT32, MISO=3, CS=5 |
| Tidak ada suara | DIN=8 → amp; speaker ke OUT amp |
| Boot/flash gagal | GPIO8 tidak LOW saat reset; **GPIO2 & GPIO9 tidak di-wiring** (jangan ditarik LOW saat boot); Chrome + BOOT |
| Wi-Fi | SSID `rzmong mochi` / `rzmong123` |

## 📚 Lisensi & aset

- Kode: **MIT**
- Library: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- Media pack: hanya bagikan aset yang Anda punya haknya ([ASSETS.md](ASSETS.md))

[CHANGELOG.md](CHANGELOG.md) · [PRODUCT.md](PRODUCT.md)

Copyright © 2026 rzmong · MIT
