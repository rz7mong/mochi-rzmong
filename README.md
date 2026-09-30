# Mochi rzmong

Firmware, pustaka, dan halaman instalasi untuk **ESP32-C3 Super Mini** + LCD TFT **ST7789 240×240**.

| | |
| --- | --- |
| Merek | **rzmong** |
| Repo | [rz7mong/mochi-rzmong](https://github.com/rz7mong/mochi-rzmong) |
| Instal | [rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/) |
| Versi | **0.2.1** |

## Fitur di firmware ini

- Instal dari browser (ESP Web Tools)
- 10 GIF reaksi sentuh di flash ESP32 (PROGMEM), tanpa kartu SD
- Tema SD opsional: wajah, gundam, mobil, neon, anime, makanan, musik, intro
- Menu pengaturan di LCD (16 baris, bergulir)
- Wi-Fi AP `Mochi-rzmong` / sandi `rzmong24` + halaman pengaturan web
- Jingle I2S (MAX98357), volume 0–21, bisu
- Chronos opsional (peta dan notifikasi)
- Merek rzmong di LCD, web, dan repo

Tidak ada di firmware ini:

- pemutar MP3 dari kartu SD
- overlay teks `o_o`
- ketuk 1× untuk ganti GIF tema

## Sentuh

| Gestur | Aksi |
| --- | --- |
| Ketuk 1× | Putar GIF reaksi dari flash (sekitar 1,6 detik) plus jingle. GIF tema tidak berganti. |
| Ketuk 2× | Buka menu Pengaturan |
| Tahan 1 detik atau lebih | Bisu atau bunyi |
| Di menu, ketuk 1× | Geser sorotan (daftar bergulir sendiri) |
| Di menu, ketuk 2× | Jalankan baris yang tersorot |

Ganti GIF tema hanya lewat menu **GIF berikutnya** atau halaman Pengaturan web.

### Sepuluh reaksi di flash

| Nama | File di memori |
| --- | --- |
| tickle | `yelling` |
| kedip | `distracted_2` |
| cinta | `dumb_love` |
| marah | `hadouken_hit` |
| ketawa | `awkward_laugh` |
| nangis | `crying_smile` |
| ngantuk | `keep_it_up` |
| kaget | `big_sneeze` |
| kedip-satu | `blade` |
| cemberut | `pinky` |

Mode reaksi: **acak** (bawaan) atau **tetap** (pilih di menu Model reaksi).

## Menu LCD (16 baris)

1. GIF berikutnya
2. Pilih tema
3. Ekspresi flash
4. Mode putar
5. Reaksi acak/tetap
6. Model reaksi
7. Sumber SD/Flash
8. Volume +
9. Volume −
10. Bisu
11. Rotasi layar
12. Chronos
13. Merek LCD
14. Info Wi-Fi AP
15. Tentang rzmong
16. Tutup

Tes bunyi di menu memutar jingle di flash, bukan berkas MP3.

## Pin

| Fungsi | GPIO |
| --- | --- |
| TTP223 OUT | 1 |
| SD MISO | 2 |
| TFT SCLK + SD SCK | 4 |
| SD CS | 5 |
| TFT MOSI + SD MOSI | 6 |
| TFT CS | 7 |
| TFT RST | 8 |
| I2S DIN | 9 |
| TFT DC | 10 |
| I2S LRC | 20 |
| I2S BCLK | 21 |

## Kartu SD (opsional)

```text
/gif/<tema>/<nama>.gif
/sfx/<tema>/<nama>.wav
```

Format FAT32. Tanpa SD, Mochi tetap berjalan dari flash.

## Bangun firmware

```bash
python firmware/tools/embed_assets.py
cd firmware
pio run -e esp32-c3-super-mini
```

Sumber GIF reaksi: `firmware/assets/react/` atau `firmware/tools/react_b64/`.

## Tautan

- [Instalasi](https://rz7mong.github.io/mochi-rzmong/)
- [Panduan](https://rz7mong.github.io/mochi-rzmong/panduan.html)
- [Hardware](https://rz7mong.github.io/mochi-rzmong/hardware.html)
- [Pengaturan](https://rz7mong.github.io/mochi-rzmong/thietlap.html)
- Pustaka: `library/MochiRzmong.h`

Copyright rzmong
