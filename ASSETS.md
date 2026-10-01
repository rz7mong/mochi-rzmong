# Theme & media assets

## Official pack location

Only: [GitHub Release `assets-v1`](https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1) — direct download: [mochi-themes.zip](https://github.com/rz7mong/mochi-rzmong/releases/download/assets-v1/mochi-themes.zip)

Pack update 2026-10-02: 8 fps colourful versions of wajah/sleepy, smirk, raspberry, squint, angry_2, musik/pong, rainbow, mobil/revs, headlights; new wajah/default (white smile + blink); new wajah/love_hearts_kiss and wajah/yawn_tired with WAVs. Total 86 GIF + 87 WAV + themes.json.

## Built-in (flash) assets

`firmware/assets/builtin/gif/<tema>/<stem>.gif` + `sfx/<tema>/<stem>.wav` — 30 slots embedded into the app partition by `firmware/tools/embed_assets.py` (order from `firmware/assets/meta.json` → `builtins`). Built-in WAVs are 8 kHz 16-bit mono, trimmed to the GIF length.

Extract to **root of FAT32 microSD**:

```text
/
├── themes.json
├── gif/<tema>/*.gif
└── sfx/<tema>/*.wav
```

## Formats on device

| Type | Format |
| --- | --- |
| Animation | **GIF** 240×240 |
| SFX | **WAV 16-bit PCM** (mono/stereo), not MP3 |

## Licensing

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). You are responsible for rights to any GIF/WAV you upload or redistribute.

## Compatibility

| Firmware | Theme pack |
| --- | --- |
| ≥ 0.2.6 | `assets-v1` (9 themes, WAV SFX) |
| 0.2.8+ | Same + AP `rzmong mochi` / `rzmong123` |
| **0.5.2** | Same pack + captive upload + Chronos nav |
| **0.5.6** | `assets-v1` (updated 2026-10-02, 86 GIF + 87 WAV) + 30 built-in GIF+WAV in flash |
