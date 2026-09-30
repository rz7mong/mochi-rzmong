# Mochi rzmong

[![Build firmware](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml/badge.svg)](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Palm-sized **ESP32-C3 Super Mini** desk buddy + **ST7789 1.3" 240×240** (23×40 mm PCB): **GIF** faces, touch reactions, **WAV** SFX.

Independent open-source project **inspired by** Dasai Mochi — **not affiliated**, not a licensed clone.

**Firmware 0.5.1** · **MIT © rzmong** · Bahasa Indonesia: [README.md](README.md)

On device: **GIF + 16-bit WAV only** (no MP4 player, no MP3 decoder).

## Quick start

1. Chrome / Edge → [installer 0.5.1](https://rz7mong.github.io/mochi-rzmong/) (hold BOOT, plug USB-C).
2. Default AP: **`rzmong mochi` / `rzmong123`**. Lab password — change `MOCHI_AP_PASS` and reflash before public use.
3. Settings: **`http://192.168.4.1/`** on the device AP.
4. Themes: [Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) → FAT32 SD root (`gif/` + `sfx/`).

Do not use expired `user-attachments` zip links. Use the Release.

Settings page is **pengaturan.html** (`thietlap.html` only redirects).

Pins are **not** “boot-safe”: GPIO8 is a C3 strapping pin (I2S DIN); GPIO20/21 are UART0 (boot log may click the speaker).

Full pins / case STL / troubleshooting: see [README.md](README.md).

## License

**MIT © rzmong** · [LICENSE](LICENSE) · ChronosESP32 by fbiego — [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
