# HANDOFF — Mochi rzmong v0.5.4

**Repo:** https://github.com/rz7mong/mochi-rzmong  
**Pages:** https://rz7mong.github.io/mochi-rzmong/  
**Salinan web:** https://rz7mong.github.io/mochi-rzmong/handoff.html

## Device

ESP32-C3 Super Mini + ST7789 1.3" 240×240 GMT130 (PCB 27.78×39.22 mm, 7 pin tanpa CS, dipasang pin di bawah → rotasi default 2) + touch + microSD opsional + Chronos BLE.

| AP | Value |
|----|--------|
| SSID | `rzmong mochi` |
| Pass | `rzmong123` (lab; ganti `MOCHI_AP_PASS` lalu flash) |
| UI | `http://192.168.4.1/` |

## Build / flash

```bash
cd firmware
python tools/embed_assets.py
pio run -e esp32-c3-super-mini
pio run -e esp32-c3-super-mini -t upload
```

Installer: https://rz7mong.github.io/mochi-rzmong/  
Tema: https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1

Jangan flash zip prebuilt 0.4.7 jika butuh Chronos-nav / serviceNet / captive upload.

## Pins (bukan boot-safe)

Touch=1 · SD 4/6/3/5 · TFT 4/6/7/10/0 · I2S 21/20/8 · GPIO2/9 kosong.

GPIO8 = strapping + I2S DIN. GPIO20/21 = UART0 — log boot bisa “plok” di speaker.

Lihat `firmware/include/MochiRzmong.h` + `User_Setup_ST7789.h` (`SUPPORT_TRANSACTIONS`).

Rotasi: `MOCHI_DEFAULT_ROTATION` (default 2). NVS `rot` dari firmware ≤ 0.5.4 digeser +2 sekali (penanda `rotv`); setelan lain tetap.

## SD / API

`/gif/<tema>/<stem>.gif` + `/sfx/<tema>/<stem>.wav` · upload ~600000 bytes  
`GET /api/status` · `GET /api/themes` · `POST /api/settings` · `POST /api/upload`  
Password **tidak** di JSON.

## Chronos

BLE name `rzmong`. Satu radio 2.4 GHz: AP + BLE bisa lag.

## License

**MIT © rzmong** · ChronosESP32 (fbiego)


Jam HP: dipilih dari HP di http://192.168.4.1/ (centang Chronos BLE dan Jam HP). LCD tidak sentuh. GPIO1 hanya jika ada kawat sentuh.
