# Handoff (internal / AI)

| Key | Value |
| --- | --- |
| Version | **0.5.1** |
| AP | `rzmong mochi` / `rzmong123` |
| Settings (preferred) | `http://192.168.4.1/` on device |
| Settings (Pages) | `docs/pengaturan.html` |
| Binary | `docs/firmware/firmware.bin` |
| Manifest | `docs/firmware/manifest.json` → version **0.5.1** |
| Install | https://rz7mong.github.io/mochi-rzmong/ |
| Theme pack | `assets-v1` |
| Hardware | ESP32-C3 Super Mini + ST7789 1.3" 240×240 (PCB 23×40 mm) |

## Web on device

- `GET /` · `GET /index.html` → captive HTML (`captive_ui.h`)
- `GET /api/status` · `GET /api/themes` · `POST /api/settings` · `POST /api/upload`
- No authentication on AP (lab). Erase install wipes NVS.

## Chronos

- Optional: menu **Chronos** or `chronos` in settings JSON
- Library: ChronosESP32 (fbiego) — see THIRD_PARTY_NOTICES
- ESP32-C3 one 2.4 GHz radio: Wi-Fi AP + BLE together may affect latency; test on hardware

## SPI / SD

- TFT+SD share SCK/MOSI; `sdBusy` + `SUPPORT_TRANSACTIONS` prevent bus clash
- TFT RST = **GPIO0**, SD MISO = **GPIO3**, I2S DIN = **GPIO8**
- Leave **GPIO2** and **GPIO9** unconnected (strapping)

## Partitions

- Single factory app 3 MB — **no OTA dual-slot**
- `otadata` retained for Arduino boot_app0 layout only

## Pins

Touch=1 · SD 4/6/3/5 · TFT 4/6/7/10/0 · I2S 21/20/8 · leave GPIO2/9 unconnected

## Build

```bash
pip install -U platformio pillow esptool
python firmware/tools/embed_assets.py
cd firmware && pio run -e esp32-c3-super-mini
```

Platform pinned: `espressif32@6.9.0`
