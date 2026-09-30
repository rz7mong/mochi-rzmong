# Product constants (single source of truth)

| Key | Value |
| --- | --- |
| **Version** | `0.4.7` |
| **Brand** | `rzmong` |
| **AP SSID** | `rzmong mochi` |
| **AP password** | `rzmong123` |
| **On-device settings** | `http://192.168.4.1/` (captive UI, offline — **recommended**) |
| **Studio + Upload** | `docs/studio.html` → convert + `POST /api/upload` to SD |
| **GIF size limit** | max **599 KB** (ESP32 RAM / upload buffer) |
| **GitHub Pages settings** | `docs/pengaturan.html` (needs internet; mixed-content risk) |
| **Theme pack** | Release `assets-v1` |
| **Media** | GIF 240×240 + WAV 16-bit mono ~22 kHz only |
| **Suggested About** | `ESP32-C3 desk buddy: GIF faces, touch reactions, WAV SFX. Flash from browser.` |

```c
#define MOCHI_VERSION "0.4.7"
#define MOCHI_AP_NAME "rzmong mochi"
#define MOCHI_AP_PASS "rzmong123"
```

**Erase on install:** `new_install_prompt_erase: true` wipes **NVS** (saved theme, volume, Chronos flag, etc.). SD card content is separate.

**GIF + SFX pair:** same `tema` + `stem` → firmware plays WAV then GIF when opening that GIF from SD.
