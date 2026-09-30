# Mochi rzmong

Firmware, pustaka, dan halaman instalasi untuk ESP32-C3 Super Mini + LCD TFT ST7789 240×240.

Merek: **rzmong** · Repo: [rz7mong/mochi-rzmong](https://github.com/rz7mong/mochi-rzmong)  
Instal: **[rz7mong.github.io/mochi-rzmong](https://rz7mong.github.io/mochi-rzmong/)**

Versi pustaka: **0.2.1**

## Fitur yang benar-benar ada di firmware

- Instal dari browser (ESP Web Tools)
- 10 GIF reaksi sentuh di **flash ESP32** (PROGMEM), tanpa SD
- Tema SD opsional: wajah, gundam, mobil, neon, anime, makanan, musik, intro
- Menu pengaturan di LCD (16 baris, bergulir, gaya iPod)
- Wi-Fi AP `Mochi-rzmong` / `rzmong24` + halaman pengaturan web
- Jingle I2S (MAX98357), volume 0–21, bisu
- Chronos opsional (peta & notifikasi)
- Merek rzmong di LCD / web / repo

Yang **tidak** ada di firmware ini: pemutar MP3 dari SD, overlay teks `o_o`, ketuk 1× untuk ganti GIF.

## Sentuh (jangan tertukar)

| Gestur | Aksi |
|---|---|
| Jari turun / ketuk 1× | Putar **GIF reaksi** dari flash (~1,6 dtk) + jingle. GIF tema **tidak** berganti. |
| Ketuk 2× | Buka menu PENGATURAN |
| Tahan ≥1 detik | Bisu / bunyi |
| Di menu, ketuk 1× | Geser highlight (otomatis gulir) |
| Di menu, ketuk 2× | Jalankan baris |

Ganti GIF tema hanya lewat menu **GIF berikutnya** atau Pengaturan web.

### 10 reaksi flash

tickle `yelling` · kedip `distracted_2` · cinta `dumb_love` · marah `hadouken_hit` · ketawa `awkward_laugh` · nangis `crying_smile` · ngantuk `keep_it_up` · kaget `big_sneeze` · kedip-satu `blade` · cemberut `pinky`

Mode reaksi: **acak** (default) atau **tetap** (pilih di menu Model reaksi).

## Menu LCD (16)

GIF berikutnya · Pilih tema · Ekspresi flash · Mode putar · Reaksi acak/tetap · Model reaksi · Sumber SD/Flash · Volume + · Volume − · Bisu · Rotasi layar · Chronos · Merek LCD · Info Wi-Fi AP · Tentang rzmong · Tutup

**Musik tes** = jingle di flash, bukan file MP3.

## Pin (satu sumber, jangan diganti semaunya)

| Fungsi | GPIO |
|---|---|
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

## SD (opsional)

```
/gif/<tema>/<nama>.gif
/sfx/<tema>/<nama>.wav
```

FAT32. Tanpa SD, Mochi tetap jalan dari flash.

## Bangun

```bash
python firmware/tools/embed_assets.py
cd firmware
pio run -e esp32-c3-super-mini
```

GIF reaksi sumber: `firmware/assets/react/` atau `firmware/tools/react_b64/`.

## Tautan

- [Instalasi](https://rz7mong.github.io/mochi-rzmong/)
- [Panduan](https://rz7mong.github.io/mochi-rzmong/panduan.html)
- [Hardware](https://rz7mong.github.io/mochi-rzmong/hardware.html)
- [Pengaturan](https://rz7mong.github.io/mochi-rzmong/thietlap.html)
- Pustaka: `library/MochiRzmong.h`

© rzmong
