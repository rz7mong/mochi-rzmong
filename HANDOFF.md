# HANDOFF — Mochi rzmong v0.5.1

**Repo:** https://github.com/rz7mong/mochi-rzmong  
**Pages:** https://rz7mong.github.io/mochi-rzmong/

## Device

ESP32-C3 Super Mini + ST7789 240×240 + touch + optional microSD + Chronos BLE.

| AP | Value |
|----|--------|
| SSID | `rzmong mochi` |
| Pass | `rzmong123` |
| UI | `http://192.168.4.1/` |

## Build / flash

```bash
cd firmware
pio run -e esp32-c3-super-mini
pio run -e esp32-c3-super-mini -t upload
```

CI (`firmware.yml`): runs `embed_assets.py` (GIF/jingle headers), builds, merges `docs/firmware/firmware.bin`, commits bin + manifest.

**Do not flash an old zip `prebuilt/` 0.4.7** if you need Chronos-nav / serviceNet / captive upload.

## Pins

See `firmware/include/MochiRzmong.h` and `User_Setup_ST7789.h` (`SUPPORT_TRANSACTIONS` for shared SPI).

## SD paths

`/gif/<tema>/<stem>.gif` · `/sfx/<tema>/<stem>.wav` · upload buffer ~600000 bytes

## API

`GET /api/status` · `GET /api/themes` · `POST /api/settings` · `POST /api/upload` · CORS + OPTIONS enabled. **Password not in JSON.**

## Chronos

BLE name `rzmong`. Pair in Chronos app only. Features: notif, call, find, time, navigation (dirty redraw).

Touch: notif 1-tap · call hold 0.6s · nav 2-tap hide · play 1-tap react / 2-tap menu.

## Media flow

1. Studio online → download GIF/WAV  
2. AP + captive **Upload ke SD** (same-origin)

## Runtime notes

- `serviceNet()` during GIF frames (DNS, HTTP, Chronos loop)
- GIF auto-`nextPart()` after a full play with no taps
- One radio: heavy AP + BLE may lag

## License

MIT · rzmong · ChronosESP32 (fbiego)
