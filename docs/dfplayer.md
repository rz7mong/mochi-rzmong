# Varian DFPlayer (MP3)

Build terpisah dari MAX98357. Jangan pasang keduanya: GPIO20 dan GPIO21 hanya satu fungsi.

```bash
cd firmware
pio run -e esp32-c3-dfplayer -t upload
```

Environment lama `esp32-c3-super-mini` tetap WAV + MAX98357.

## Kabel

| DFPlayer | ESP32-C3 |
|---|---|
| VCC | 5 V (bukan 3V3) |
| GND | GND |
| RX | GPIO20 lewat resistor ~1 kOhm |
| TX | GPIO21 langsung |
| SPK+ / SPK- | speaker 8 ohm |

Lepas MAX98357. GPIO8 tidak dipakai di varian ini. TFT, SD GIF, dan sentuh tidak berubah.

## Kartu SD modul

FAT32. Folder `01` dan `02`, berkas `001.mp3` dan seterusnya.

Folder `01` (reaksi, urutan `MOCHI_REACT`):

1. raspberry
2. squint
3. love_hearts_kiss
4. angry_2
5. smirk
6. sleepy
7. yawn_tired
8. rainbow
9. pong
10. revs
11. hadouken_hit

Folder `02` suara wajah bawaan, `001.mp3` = indeks 0. ESP tidak membaca MP3 ini.
