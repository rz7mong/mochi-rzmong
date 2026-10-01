# 🍡 Mochi rzmong

[![Build firmware](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml/badge.svg)](https://github.com/rz7mong/mochi-rzmong/actions/workflows/firmware.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Palm-sized **ESP32-C3 Super Mini** desk buddy + **ST7789 1.3" 240×240** (GMT130 module, 27.78×39.22 mm PCB, 7-pin, no CS): **GIF** faces, touch reactions, **WAV** SFX.

Independent open-source project **inspired by** Dasai Mochi — **not affiliated**, not a licensed clone.

**Firmware 0.5.6** · **MIT © rzmong** · Bahasa Indonesia: [README.md](README.md)

On device: **GIF + 16-bit WAV only** (no MP4 player, no MP3 decoder).

## 🕐 Phone clock

The LCD is not a touchscreen. Enable **Jam HP** from the phone: join `rzmong mochi` / `rzmong123`, open `http://192.168.4.1/`, check Chronos BLE and Jam HP, save, then connect `rzmong` in the Chronos app. Uncheck Jam HP to return to GIFs. Touch menu only works with a wire on GPIO1.

## 🚀 Quick start

1. Chrome / Edge → [installer 0.5.6](https://rz7mong.github.io/mochi-rzmong/) (hold BOOT, plug USB-C).
2. Default AP: **`rzmong mochi` / `rzmong123`**. Lab password — change `MOCHI_AP_PASS` and reflash before public use.
3. Settings: **`http://192.168.4.1/`** on the device AP.
4. Themes: [mochi-themes.zip](https://github.com/rz7mong/mochi-rzmong/releases/download/assets-v1/mochi-themes.zip) (Release [`assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1)) → FAT32 SD root (`gif/` + `sfx/`).

**Built-ins (0.5.6):** without an SD card the firmware plays **30 GIF+WAV slots from flash** (~1.04 MB): the new white smile+blink `wajah/default` (also the phone-clock face), colourful wajah/musik clips used as the 11 tap reactions, 14 mobil clips and 6 gundam clips. Matching SD files still take precedence.

Do not use expired `user-attachments` zip links. Use the Release.

Settings page is **pengaturan.html** (`thietlap.html` only redirects).

Pins are **not** “boot-safe”: GPIO8 is a C3 strapping pin (I2S DIN); GPIO20/21 are UART0 (boot log may click the speaker).

The LCD stand [`case/tatakan_GMT130_fit.stl`](case/README.md) holds the screen **pins-down** with wires soldered directly to the pads (no pin header). Since firmware 0.5.4 the default rotation is **2** (180°) so the image is upright; on the old stand / pins-up, use LCD menu → **Rotasi layar** twice, or build with `-DMOCHI_DEFAULT_ROTATION=0`.

Optional **carrier PCB** variant: a single-sided, hand-etched 1.6 mm FR4 THT board (38.5 × 36 mm) that holds the ESP32-C3 Super Mini, a small 3.3 V micro SD module (~18.5 × 20 mm), the MAX98357A and a 470 µF 10 V Ø6.3 × 11 cap, used with `case/case_luar_lcd_23_40mm_pcb.stl` + `case/tatakan_GMT130_fit_pcb.stl`. It needs a 15 × 11 × 3.5 mm speaker and a 501640 LiPo. Etch artwork, assembly order and notes: [pcb/README.md](pcb/README.md), fit report: [docs/fit/REPORT.md](docs/fit/REPORT.md). The loose-wiring build is still supported.

Full pins / case STL / troubleshooting: see [README.md](README.md). Wiring diagram 0.5.6: [docs/wiring-0.5.1.jpg](docs/wiring-0.5.1.jpg).

## 📄 License

**MIT © rzmong** · [LICENSE](LICENSE) · ChronosESP32 by fbiego — [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
