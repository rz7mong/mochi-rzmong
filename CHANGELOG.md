# Changelog

All notable changes to **Mochi rzmong** are documented here.

## [0.2.6] — 2026-09-30

### Added
- Dual theme selection: **web settings** set the default theme; **LCD menu** can change theme when SD is present
- `GET /api/themes` — list categories and GIF counts on SD
- Safer `embed_assets.py` (skips invalid/PLACEHOLDER base64)

### Changed
- Version bump across docs, manifest, and CI commit message
- README/docs clarity: GIF/WAV only, pin tables, troubleshooting

### Fixed
- CI embed step no longer fails on placeholder `.b64` files

## [0.2.5] — 2026-09-29

### Added
- Theme catalog alignment with SD pack (9 categories)
- Web settings page (`thietlap.html`) theme chips

### Changed
- Documentation consistency: WAV only, GIF only, 900 ms hold

## [0.2.4] — 2026-09-28

### Added
- WAV 16-bit SFX playback from SD via MAX98357 I2S
- Boot-safe pin map (MISO=3, RST=0, DIN=8)
- Touch reactions (10 stems) + jingle fallback

### Notes
- MP3/MP4 not supported on device
