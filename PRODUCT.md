# Product constants (single source of truth)

Edit here first, then keep firmware header + docs in sync.

| Key | Value |
| --- | --- |
| **Version** | `0.2.8` |
| **Brand** | `rzmong` |
| **AP SSID** | `rzmong mochi` |
| **AP password** | `rzmong123` |
| **Settings page** | `docs/pengaturan.html` |
| **Theme pack** | Release tag `assets-v1` |
| **Media on device** | GIF + WAV 16-bit only (no MP4, no MP3) |

Firmware defines the same values in `firmware/include/MochiRzmong.h`:

```c
#define MOCHI_VERSION "0.2.8"
#define MOCHI_AP_NAME "rzmong mochi"
#define MOCHI_AP_PASS "rzmong123"
```

To change Wi-Fi credentials: edit `MOCHI_AP_NAME` / `MOCHI_AP_PASS`, rebuild, flash.
