# Mochi rzmong — paket lanjut ke AI lain

Salin file ini + folder firmware. Instruksi: lanjutkan firmware ESP32-C3 Super Mini + ST7789 240x240 milik rzmong. Jangan hapus merek rzmong.

Repo: https://github.com/rz7mong/mochi-rzmong
Situs: https://rz7mong.github.io/mochi-rzmong/

## Hardware
ESP32-C3 Super Mini; ST7789 SCLK=4 MOSI=6 CS=7 DC=10 RST=8; SD SCK=4 MOSI=6 MISO=2 CS=5; TTP223 GPIO1 HIGH; MAX98357 BCLK=21 LRC=20 DIN=9.

## Gestur
Sentuh turun saat GIF = overlay o_o + jingle 180ms.
1 ketuk = reaksi saja (tidak ganti GIF).
2 ketuk = menu iPod.
Tahan 900ms = bisu.
Menu: 1 ketuk geser, 2 ketuk pilih. Ganti GIF lewat baris GIF berikutnya.

## Build
python firmware/tools/embed_assets.py && cd firmware && pio run -e esp32-c3-super-mini
