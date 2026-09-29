# 🍡 Mochi rzmong

Firmware, pustaka, dan halaman instalasi untuk ESP32-C3 Super Mini + LCD TFT ST7789 240×240.

Merek: **rzmong** · Repo: [rz7mong/mochi-rzmong](https://github.com/rz7mong/mochi-rzmong)  
Instal dari browser (Chrome / Edge): **[rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/)**

![badge](https://img.shields.io/badge/rzmong-Mochi-ff6b6b?style=flat-square)
![badge](https://img.shields.io/badge/ESP32--C3-ST7789_240x240-1dd1a1?style=flat-square)
![badge](https://img.shields.io/badge/tema-wajah_gundam_mobil-54a0ff?style=flat-square)

## ✨ Fitur

|  | |
|---|---|
| 🔌 | Instal firmware dari web (ESP Web Tools) |
| 🎭 | Tema: wajah · gundam · mobil · neon · anime · makanan · musik · intro |
| 🎲 | Mode acak atau tetap di satu tema |
| 👇 | Kontrol sentuh: ketuk, ketuk 2×, tahan |
| 🔇 | Bisu / bersuara |
| 🛠️ | Studio web: unggah GIF atau MP4 + SFX |
| 🎵 | Putar MP3 dari kartu SD `/music/` |
| 🗺️ | ChronosESP32 — peta & notifikasi HP |
| 💧 | Merek **rzmong** di boot LCD, web, dan repo |

## 📦 Isi kartu SD

```
/themes.json
/gif/<tema>/<nama>.gif
/sfx/<tema>/<nama>.wav
/music/*.mp3
```

Tema Gundam berisi bagian terpisah: kokpit, helm, isyarat, tembak, pilot.

## 👇 Sentuh

| Gestur | Aksi |
|---|---|
| Ketuk 1× | Bagian berikutnya dalam tema |
| Ketuk 2× | Buka menu di LCD |
| Tahan 1 detik | Bisu / bunyi |

Menu LCD: Tema · Acak · Musik · Suara · Chronos · Tentang rzmong

## 🛠️ Bangun firmware

```bash
cd firmware
pio run -e esp32-c3-super-mini
pio run -t upload
```

Bin hasil: `docs/firmware/firmware.bin`.

## 📚 Pustaka

Header `library/MochiRzmong.h` + `library/themes.json`.

© rzmong · 🍡
