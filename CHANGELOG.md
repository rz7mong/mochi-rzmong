# Changelog

## [0.5.1] — 2026-09-30

### Changed
- **Docs sync**: Pages, PRODUCT, README, HANDOFF, hardware/blueprint, tutorial → **0.5.1**
- **Blueprint**: pinout mengikuti `MochiRzmong.h` + `User_Setup_ST7789.h` (bukan skema lama RST=8 / MISO=2 / DIN=9)
- **Model hardware**: ESP32-C3 Super Mini + ST7789 1.3" 240×240 PCB 23×40 mm

### Notes
- Jangan flash zip prebuilt 0.4.7 jika butuh Chronos-nav / serviceNet / captive upload
- Prefer **http://192.168.4.1/** di AP perangkat

## [0.4.7] — 2026-09-30

### Changed
- **Docs sync**: all Pages + PRODUCT + README + firmware version string → **0.4.7**
- **Studio**: GIF target **599 KB**; tries longer duration first (up to ~8s), then lowers quality
- **pengaturan.html**: clear offline-first guidance; mixed-content warning for Pages→HTTP AP

### Notes
- Prefer **http://192.168.4.1/** on device AP for settings (no mixed content, works without internet)
- Studio on GitHub Pages needs internet (FFmpeg.wasm); upload still needs join AP

## [0.4.5] — 2026-09-30

### Added
- GIF+SFX path pairing on SD (`playSfxForGifPath`)
- Studio auto-extract WAV from video track

## [0.4.0] — 2026-09-30

### Added
- Studio Convert + Upload (FFmpeg.wasm + `POST /api/upload`)
- Upload max ~600 KB, SD required

## [0.3.0] — 2026-09-30

### Added
- Captive settings UI at `http://192.168.4.1/`
- Chronos optional BLE documented

## [0.2.9] — 2026-09-30

sdBusy SPI guard; THIRD_PARTY_NOTICES; pin wording.

## [0.2.8] — 2026-09-30

Wi-Fi `rzmong mochi` / `rzmong123`.

## [0.2.6] — 2026-09-30

Dual theme selection.
