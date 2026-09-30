# 🍡 Mochi rzmong

Firmware, pustaka, dan halaman instalasi untuk **ESP32-C3 Super Mini** + LCD TFT **ST7789 240×240**.

| | |
| --- | --- |
| 🏷️ Merek | **rzmong** |
| 📦 Repo | [rz7mong/mochi-rzmong](https://github.com/rz7mong/mochi-rzmong) |
| 🌐 Instal | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| 📌 Versi | **0.2.3** |

## ✨ Fitur

- 🌐 Instal dari browser (ESP Web Tools)
- 🎬 10 GIF reaksi sentuh di flash (PROGMEM)
- 🎨 Tema SD opsional
- 📋 Menu 16 baris di LCD
- 📶 Wi-Fi AP `Mochi-rzmong` / `rzmong24`
- 🔊 Jingle I2S (MAX98357)
- 🗺️ Chronos opsional

## 👆 Sentuh

| Gestur | Aksi |
| --- | --- |
| 👆 Ketuk 1× | GIF reaksi + jingle |
| 👆👆 Ketuk 2× | Menu Pengaturan |
| ✊ Tahan ≥1 d | Bisu / bunyi |

## 🔌 Pin map v0.2.3 (boot-safe)

| Fungsi | GPIO | Catatan |
| --- | --- | --- |
| 👆 TTP223 OUT | **1** | aman |
| 💾 SD MISO | **3** | bukan GPIO2 (strap) |
| 📺 TFT SCLK + SD SCK | **4** | |
| 💾 SD CS | **5** | |
| 📺 TFT MOSI + SD MOSI | **6** | |
| 📺 TFT CS | **7** | |
| 📺 TFT RST | **0** | bukan GPIO8 |
| 🔊 I2S DIN | **8** | satu-satunya strap yang dipakai |
| 📺 TFT DC | **10** | |
| 🔊 I2S LRC | **20** | |
| 🔊 I2S BCLK | **21** | |

**GPIO2 & GPIO9 kosong** (BOOT tetap normal).

## ⚡ Power path

```
🔋 LiPo → TP4056 → 🔌 Saklar → VIN ESP32 + VIN MAX98357
ESP32 3V3 → LCD + SD + TTP223
```

## 💾 SD (opsional)

```text
/gif/<tema>/<nama>.gif
/sfx/<tema>/<nama>.wav
```

## 🛠️ Build

```bash
python firmware/tools/embed_assets.py
cd firmware
pio run -e esp32-c3-super-mini
```

## 🔗 Tautan

- 🍡 [Instalasi](https://rz7mong.github.io/mochi-rzmong/)
- 🔧 [Hardware](https://rz7mong.github.io/mochi-rzmong/hardware.html)
- 📖 [Panduan](https://rz7mong.github.io/mochi-rzmong/panduan.html)

Copyright rzmong
