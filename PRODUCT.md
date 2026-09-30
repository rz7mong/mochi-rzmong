# Product constants (single source of truth)

| Key | Value |
| --- | --- |
| **Version** | `0.3.0` |
| **Brand** | `rzmong` |
| **AP SSID** | `rzmong mochi` |
| **AP password** | `rzmong123` |
| **On-device settings** | `http://192.168.4.1/` (captive UI, offline) |
| **GitHub Pages settings** | `docs/pengaturan.html` (needs internet; prefer on-device UI) |
| **Theme pack** | Release `assets-v1` |
| **Media** | GIF + WAV 16-bit only |
| **Suggested About** | `ESP32-C3 desk buddy: GIF faces, touch reactions, WAV SFX. Flash from browser.` |

```c
#define MOCHI_VERSION "0.3.0"
#define MOCHI_AP_NAME "rzmong mochi"
#define MOCHI_AP_PASS "rzmong123"
```

**Erase on install:** `new_install_prompt_erase: true` wipes **NVS** (saved theme, volume, Chronos flag, etc.). Documented in install guide.
