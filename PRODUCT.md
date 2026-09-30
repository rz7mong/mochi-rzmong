# Product constants (single source of truth)

Edit **version and Wi-Fi here and in** `firmware/include/MochiRzmong.h` together. CI reads version from the header for `manifest.json`.

| Key | Value |
| --- | --- |
| **Version** | `0.2.9` |
| **Brand** | `rzmong` |
| **AP SSID** | `rzmong mochi` |
| **AP password** | `rzmong123` |
| **Settings page** | `docs/pengaturan.html` |
| **Legacy settings URL** | `docs/thietlap.html` → redirect to `pengaturan.html` |
| **Theme pack** | Release tag `assets-v1` |
| **Media on device** | GIF + WAV 16-bit only (no MP4, no MP3) |
| **Suggested About text** | `ESP32-C3 desk buddy: GIF faces, touch reactions, WAV SFX. Flash from browser.` |

Firmware:

```c
#define MOCHI_VERSION "0.2.9"
#define MOCHI_AP_NAME "rzmong mochi"
#define MOCHI_AP_PASS "rzmong123"
```
