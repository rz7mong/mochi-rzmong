# Mochi rzmong — paket untuk AI lain

Lanjutkan firmware ESP32-C3 Super Mini + ST7789 240×240 milik rzmong.
Jangan hapus merek rzmong.
Jangan mengembalikan ketuk 1× menjadi ganti GIF tema.

- Repo: https://github.com/rz7mong/mochi-rzmong
- Situs: https://rz7mong.github.io/mochi-rzmong/
- Versi: 0.2.1

## Gestur

- Ketuk 1× = GIF reaksi dari PROGMEM `DEFAULT_GIFS`
- Ketuk 2× = menu 16 item bergulir
- Tahan 900 ms = bisu
- Ganti GIF tema hanya lewat menu **GIF berikutnya**

## Pin

Touch = 1, SD MISO = 2, SD CS = 5, SPI clock = 4, MOSI = 6, TFT CS = 7, DC = 10, RST = 8, I2S BCLK = 21, LRC = 20, DIN = 9.

## Reaksi flash

yelling, distracted_2, dumb_love, hadouken_hit, awkward_laugh, crying_smile, keep_it_up, big_sneeze, blade, pinky.

## Build

```bash
python firmware/tools/embed_assets.py
cd firmware
pio run -e esp32-c3-super-mini
```
