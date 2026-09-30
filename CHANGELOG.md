# Changelog

## [0.4.0] — 2026-09-30

### Added
- **Studio Convert + Upload**: halaman `studio.html` convert MP4→GIF 240×240 dan MP3→WAV 16-bit di browser (FFmpeg.wasm), lalu upload ke SD lewat Wi-Fi AP
- **API** `POST /api/upload?tema=&stem=&type=gif|wav` — tulis file ke `/gif/<tema>/` atau `/sfx/<tema>/` (max ~600 KB, hormati `sdBusy`)

### Notes
- Upload hanya jalan jika kartu SD terpasang dan user tersambung ke AP `rzmong mochi`
- API tetap **tanpa autentikasi** (siapa pun di AP bisa upload)

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
