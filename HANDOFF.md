# 🍡 Mochi rzmong — paket untuk AI lain

Lanjutkan firmware ESP32-C3 Super Mini + ST7789 240×240 milik rzmong.
Jangan hapus merek rzmong.
Jangan mengembalikan ketuk 1× menjadi ganti GIF tema.

- Repo: https://github.com/rz7mong/mochi-rzmong
- Situs: https://rz7mong.github.io/mochi-rzmong/
- Versi: **0.2.3**

## 👆 Gestur

- Ketuk 1× = GIF reaksi PROGMEM
- Ketuk 2× = menu 16 item
- Tahan 900 ms = bisu

## 🔌 Pin map v0.2.3 (boot-safe)

Touch=1, SD MISO=**3**, SD CS=5, SCK=4, MOSI=6, TFT CS=7, TFT RST=**0**, TFT DC=10, I2S DIN=**8**, LRC=20, BCLK=21.

**Jangan pakai GPIO2 / GPIO9** untuk peripheral (strapping / BOOT).

## ⚡ Power

```
LiPo → TP4056 → Saklar → VIN ESP32 + VIN MAX98357
ESP32 3V3 → LCD + SD + TTP223
```

## 🛠️ Build

```bash
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```
