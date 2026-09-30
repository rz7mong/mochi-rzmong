# Changelog

## [0.3.0] — 2026-09-30

### Added
- **Captive settings UI** at `http://192.168.4.1/` (and `/index.html`) — works offline on the device AP
- Document Chronos (optional BLE companion, menu toggle); single radio — test if AP+BLE both on

### Changed
- `platformio.ini`: pin `espressif32@6.9.0` for reproducible builds
- Partitions: documented **no dual-slot OTA** (single factory app)
- Install guide: Erase wipes NVS warning; prefer on-device UI over github.io from phone AP

### Security note
- HTTP API on the AP has **no auth** (lab default). Anyone on the AP can POST `/api/settings`.

## [0.2.9] — 2026-09-30

sdBusy SPI guard; THIRD_PARTY_NOTICES; pin wording.

## [0.2.8] — 2026-09-30

Wi-Fi `rzmong mochi` / `rzmong123`.

## [0.2.6] — 2026-09-30

Dual theme selection.
