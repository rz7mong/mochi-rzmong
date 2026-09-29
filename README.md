# 🍡 Mochi rzmong

Firmware + perpustakaan + halaman instalasi untuk **Dasai Mochi clone** di ESP32-C3 Super Mini + LCD TFT **ST7789 240×240**.

> Watermark: **rzmong** · GitHub: [rz7mong/mochi-rzmong](https://github.com/rz7mong/mochi-rzmong)  
> Flash dari browser (Chrome / Edge): **[rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/)**

![badge](https://img.shields.io/badge/rzmong-Mochi-ff6b6b?style=flat-square)
![badge](https://img.shields.io/badge/ESP32--C3-ST7789_240x240-1dd1a1?style=flat-square)
![badge](https://img.shields.io/badge/tema-wajah_gundam_mobil-54a0ff?style=flat-square)

## ✨ Fitur

|  | |
|---|---|
| 🔌 | Nạp firmware dari web (ESP Web Tools), seperti Huykhong |
| 🎭 | Tema per kategori: wajah · gundam · mobil · neon · anime · makanan · musik · intro |
| 🎲 | Mode acak atau tetap di satu tema |
| 👇 | Kontrol sentuh: ketuk, ketuk 2×, tahan |
| 🔇 | Bisukan / bersuara |
| 🛠️ | Studio web: unggah GIF atau MP4 jadi bagian tema + ganti SFX (MP3/WAV) |
| 🎵 | Putar MP3 dari kartu SD `/music/` |
| 🗺️ | ChronosESP32 — peta & notifikasi HP |
| 💧 | Watermark **rzmong** di boot LCD, web, dan repo |

## 📦 Isi kartu SD

```
/themes.json
/gif/<tema>/<nama>.gif
/sfx/<tema>/<nama>.wav     ← atau .mp3
/music/*.mp3               ← pemutar musik
```

Tema Gundam **bukan** satu GIF campur. Pilih mode Gundam → hanya kokpit, helm, isyarat, tembak, pilot.

## 👇 Sentuh

| Gestur | Aksi |
|---|---|
| Ketuk 1× | Bagian berikutnya dalam tema |
| Ketuk 2× | Buka menu di LCD |
| Tahan 1 detik | Bisukan / bunyi |
| Di menu | Ketuk pilih baris |

Menu LCD: Tema · Acak · Musik · Suara · Chronos · Tentang rzmong

## 🛠️ Bangun firmware

```bash
cd firmware
pio run -e esp32-c3-super-mini
pio run -t upload
```

Bin hasil taruh di `docs/firmware/firmware.bin` agar tombol flash web hidup.

Aktifkan GitHub Pages: Settings → Pages → Deploy from branch `main` → folder `/docs`.

## 📚 Pustaka

Header `library/MochiRzmong.h` + `library/themes.json`.
Kredit ekspresi: Dasai / Huykhong / Emote Buddy.
Kode instalasi & port ST7789: **rzmong**.

© rzmong · 🍡
