# 🍡 Mochi rzmong

Firmware **ESP32-C3 Super Mini** + **ST7789 240×240** + **MAX98357 I2S**.

| | |
| --- | --- |
| 🏷️ Merek | **rzmong** |
| 📌 Versi | **0.2.4** |
| 🌐 Instal | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |

## ✨ Fitur

- 🎬 10 GIF reaksi di flash + opsional dari SD `/gif/`
- 🔊 **SFX reaksi**: file **WAV** di SD `/sfx/` jika ada, kalau tidak → jingle flash
- 📋 Menu LCD 16 baris · 📶 AP `Mochi-rzmong` / `rzmong24`

## ❌ Bukan pemutar musik penuh

- Decoder **MP3 di ESP32-C3 belum diaktifkan** (library umum butuh dual-core)
- Untuk SFX: simpan **WAV 16-bit PCM** (mono/stereo, 8–48 kHz)
- Konversi MP3 → WAV lewat Audacity jika perlu

## 🔊 Speaker — penting

**Jangan** sambungkan speaker HP langsung ke GPIO ESP32.

```
ESP32 I2S (BCLK/LRC/DIN) → MAX98357 → OUT+/OUT− → speaker 4–8Ω
```

GPIO hanya sinyal digital I2S; amp yang menggerakkan speaker.

## 💾 Struktur SD

```text
/gif/<tema>/<nama>.gif
/sfx/<tema>/<stem>.wav     ← diprioritaskan (contoh yelling.wav)
/sfx/<stem>.wav
/sfx/<nama-reaksi>.wav     ← tickle, marah, …
```

Contoh stem reaksi: `yelling`, `dumb_love`, `hadouken_hit`, `awkward_laugh`, …

## 🔌 Pin (boot-safe)

Touch=1 · SD MISO=**3** · SCK=4 · CS=5 · MOSI=6 · TFT CS=7 · RST=**0** · DC=10 · I2S DIN=**8** · LRC=20 · BCLK=21 · GPIO2/9 kosong

## ⚡ Power

`LiPo → TP4056 → Saklar → VIN ESP32 + VIN MAX98357` · 3V3 → LCD/SD/touch

Copyright rzmong
