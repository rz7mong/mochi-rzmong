# 🍡 Mochi rzmong

Firmware **ESP32-C3 Super Mini** + **ST7789 240×240** + **MAX98357 I2S**.

| | |
| --- | --- |
| 🏷️ Merek | **rzmong** |
| 📌 Versi | **0.2.6** |
| 🌐 Instal | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📦 Tema | [Release assets-v1](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) |

## ✨ Fitur

| Fitur | Keterangan |
| --- | --- |
| 🎬 Animasi | **GIF saja** (240×240). Bukan MP4 di ESP32. |
| 👆 Reaksi sentuh | 10 GIF di flash + SFX (acak/tetap seperti Dasai) |
| 🔊 SFX | **WAV 16-bit** di SD `/sfx/` → else jingle flash |
| 🎨 Tema SD | 9 kategori dari pack; pilih di **web** (default) atau **LCD** (manual) |
| 📋 Menu LCD | 16 baris termasuk Pilih tema |
| 📶 Wi-Fi AP | `Mochi-rzmong` / `rzmong24` → halaman Pengaturan |

## 🎨 Pilih tema (web + ESP32)

| Tempat | Cara |
| --- | --- |
| **Web** | Sambung Wi-Fi Mochi → [thietlap.html](https://rz7mong.github.io/mochi-rzmong/thietlap.html) → pilih tema → **Simpan** = **default** di flash |
| **ESP32** | Ketuk 2× → **Pilih tema** → ganti manual (butuh SD terpasang) |

Pack tema: [mochi-themes.zip](https://github.com/user-attachments/files/32840215/mochi-themes.zip) → extract ke root SD FAT32.

## ❌ Tidak ada

- Decoder **MP3** di ESP32-C3
- Putar **MP4** di perangkat (Studio web → konversi GIF)

## 👆 Gestur

| Gestur | Ambang | Aksi |
| --- | --- | --- |
| Ketuk 1× | lepas < 900 ms | GIF reaksi + SFX |
| Ketuk 2× | 2 ketuk cepat | Menu PENGATURAN |
| Tahan | **≥ 900 ms** | Bisu / bunyi |

## 🔊 Speaker

**Jangan** ke GPIO. Wajib: `ESP32 I2S → MAX98357 → speaker 4–8Ω`.

## 🔌 Pin (boot-safe)

Touch=1 · SD MISO=**3** · SCK=4 · CS=5 · MOSI=6 · TFT CS=7 · RST=**0** · DC=10 · I2S DIN=**8** · LRC=20 · BCLK=21

## ⚡ Power

`LiPo → TP4056 → Saklar → VIN ESP32 + VIN MAX98357` · 3V3 → LCD/SD/touch

## 🛠️ Build

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```

Copyright rzmong
