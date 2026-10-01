# MochiDfPlayer

Library suara DFPlayer. Firmware GIF, menu, sentuh, SD, dan Chronos sama dengan build MAX98357. Yang beda hanya suara.

Build MAX98357 tidak memakai library ini.

```bash
cd firmware
pio run -e esp32-c3-dfplayer -t upload
```

Kabel: VCC 5V, GND, RX modul <- GPIO20 lewat ~1k, TX modul -> GPIO21, speaker di SPK+/SPK-. Lepas MAX98357.

SD modul, FAT32:

- `01/001.mp3` .. `01/011.mp3` = reaksi (raspberry, squint, love_hearts_kiss, angry_2, smirk, sleepy, yawn_tired, rainbow, pong, revs, hadouken_hit)
- `02/001.mp3` .. = suara wajah, nomor = indeks bawaan + 1
