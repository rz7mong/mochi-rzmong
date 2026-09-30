# Mochi rzmong

ESP32-C3 Super Mini desk buddy — GIF faces, touch reactions, WAV SFX, optional Chronos BLE.

**Version: 0.5.1**

## Quick start

1. Flash firmware (PlatformIO `firmware/` or `docs/firmware/firmware.bin` after CI build).
2. Join Wi-Fi **`rzmong mochi` / `rzmong123`**.
3. Open **`http://192.168.4.1/`** (offline settings + SD upload).
4. Optional: Chronos app → pair BLE name **`rzmong`**.

## Docs

| Link | Purpose |
|------|---------|
| [HANDOFF.md](./HANDOFF.md) | Full handoff (pins, API, Chronos, limits) |
| [Pages — instalasi](https://rz7mong.github.io/mochi-rzmong/) | Web installer |
| [Studio](https://rz7mong.github.io/mochi-rzmong/studio.html) | Convert video→GIF/WAV (needs internet) |
| [Pengaturan](https://rz7mong.github.io/mochi-rzmong/pengaturan.html) | Remote API (mixed-content risk) |

## Recommended media flow

1. Convert on Studio **while online** → download GIF/WAV.
2. Connect to Mochi AP → upload via captive form (same-origin).
   Pages→device HTTP is often blocked (mixed content + captive DNS).

## Build

```bash
cd firmware
pio run -e esp32-c3-super-mini
# headers GIF/jingle: python tools/embed_assets.py  (also run in CI)
```

## Hardware notes

- TFT + SD share SPI → `SUPPORT_TRANSACTIONS` enabled.
- GPIO8 = I2S after boot; respect C3 strapping pins.
- ESP32-C3: one 2.4 GHz radio — Wi-Fi AP + Chronos BLE may lag together.

## License

MIT · rzmong · ChronosESP32 by fbiego
