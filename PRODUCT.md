# Product constants (single source of truth)

| Key | Value |
| --- | --- |
| **Version** | `0.5.1` |
| **Brand** | `rzmong` |
| **AP SSID** | `rzmong mochi` |
| **AP password** | `rzmong123` (change in firmware; not exposed in API JSON) |
| **On-device settings** | `http://192.168.4.1/` (captive UI — recommended) |
| **Studio** | Convert online, then upload via captive form on AP |
| **GIF size limit** | max **~600000** bytes upload buffer |
| **Chronos BLE name** | `rzmong` |
| **Theme pack** | Release `assets-v1` |
| **Media** | GIF 240×240 + WAV 16-bit mono ~22 kHz |

```c
#define MOCHI_VERSION "0.5.1"
#define MOCHI_AP_NAME "rzmong mochi"
#define MOCHI_AP_PASS "rzmong123"
```

**Erase on install:** wipes NVS (theme, volume, Chronos). SD is separate.

**GIF+SFX pair:** `/gif/<tema>/<stem>.gif` + `/sfx/<tema>/<stem>.wav`

**Touch (device):** notif 1-tap · call hold 0.6s · nav 2-tap hide · play 1-tap react / 2-tap menu
