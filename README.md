# 🍡 Mochi rzmong

Firmware **ESP32-C3 Super Mini** + **ST7789 240×240** + **MAX98357 I2S**.

| | |
| --- | --- |
| 🏷️ Merek | **rzmong** |
| 📌 Versi | **0.2.4** |
| 🌐 Instal | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |

## ✨ Fitur (yang benar-benar ada)

| Fitur | Keterangan |
| --- | --- |
| 🎬 Animasi | **GIF saja** (240×240). Bukan pemutar MP4 di ESP32. |
| 👆 Reaksi sentuh | 10 GIF di flash + SFX |
| 🔊 SFX | **WAV 16-bit** di SD `/sfx/` jika ada → else jingle flash |
| 🎨 Tema SD | Opsional: `/gif/<tema>/*.gif` |
| 📋 Menu LCD | 16 baris |
| 📶 Wi-Fi AP | `Mochi-rzmong` / `rzmong24` |

## ❌ Tidak ada / jangan diasumsikan

- Pemutar **MP3** / musik SD penuh (ESP32-C3 tidak decode MP3 di firmware ini)
- Putar **MP4** di perangkat (MP4 hanya di Studio web → konversi ke GIF)
- Ketuk 1× ganti GIF tema (hanya lewat menu **GIF berikutnya**)

## 👆 Gestur (kode aktual)

| Gestur | Ambang | Aksi |
| --- | --- | --- |
| Ketuk 1× | lepas < 900 ms | GIF reaksi + SFX |
| Ketuk 2× | 2 ketuk < ~320 ms antar | Menu PENGATURAN |
| Tahan | **≥ 900 ms** | Bisu / bunyi |

## 🎲 Reaksi acak/tetap vs 🎭 Model reaksi

| Menu | Fungsi |
| --- | --- |
| **Reaksi acak/tetap** | Mode: `acak` = tiap ketuk pilih random dari 10; `tetap` = selalu model yang dipilih |
| **Model reaksi** | Pilih salah satu dari 10 (tickle, cinta, …) dan **otomatis set mode tetap** |

## 💾 Struktur SD

```text
/gif/<tema>/<nama>.gif          ← animasi tema (bukan MP4)
/sfx/<tema>/<stem>.wav          ← SFX reaksi (WAV saja di perangkat)
/sfx/<stem>.wav
/sfx/<nama-reaksi>.wav
```

File `.mp3` di SD **tidak diputar** — konversi ke WAV 16-bit PCM.

## 🔊 Speaker

**Jangan** ke GPIO. Wajib: `ESP32 I2S → MAX98357 → OUT+/− → speaker 4–8Ω`.

## 🔌 Pin (boot-safe)

Touch=1 · SD MISO=**3** · SCK=4 · CS=5 · MOSI=6 · TFT CS=7 · RST=**0** · DC=10 · I2S DIN=**8** · LRC=20 · BCLK=21 · GPIO2/9 kosong

## ⚡ Power

`LiPo → TP4056 → Saklar → VIN ESP32 + VIN MAX98357` · 3V3 → LCD/SD/touch

## 🛠️ Build (dependency)

| Item | Nilai |
| --- | --- |
| Platform | `espressif32` (PlatformIO) |
| Board | `esp32-c3-devkitm-1` |
| Framework | Arduino |
| Python | 3.11+ (embed_assets + esptool) |
| Libs | TFT_eSPI ^2.5.43, AnimatedGIF ^2.1.1, ChronosESP32 ^1.8.0, ArduinoJson ^7.2.1 |

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```

Lihat `firmware/platformio.ini`.

Copyright rzmong
