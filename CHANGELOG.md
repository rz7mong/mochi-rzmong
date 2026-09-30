# Changelog

## [0.2.7] — 2026-09-30

### Added
- SoftAP password from device MAC: `rz` + last 4 hex (menu **Info Wi-Fi AP**, `/api/status` → `ap_pass`)

### Changed
- Docs: honest pin notes (GPIO8 strapping, UART0 on 20/21, shared SPI)
- `thietlap.html` → `pengaturan.html` (redirect kept)
- Heading “Keterbatasan”; TP4056 + DW01 note
- Softened “boot-safe” claims for GPIO8

## [0.2.6] — 2026-09-30

### Added
- Dual theme selection (web default + LCD if SD)
- `GET /api/themes`

### Changed
- README MIT, EN summary, troubleshooting

## [0.2.5] — 2026-09-29

Theme catalog + web settings chips.

## [0.2.4] — 2026-09-28

WAV SFX, boot pin map, touch reactions.
