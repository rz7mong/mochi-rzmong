# Case Mochi rzmong — model terbaru

Target hardware **2026**: ESP32-C3 Super Mini + LCD ST7789 **1.3" 240×240** modul **23×40 mm** (bukan 1.54" / 32 mm).

File cetak 3D yang diharapkan (unggah ke folder ini jika sudah siap):

- `case_luar_lcd_23_40mm.stl` — kulit luar
- `tatakan_lcd_23_40mm.stl` — dudukan LCD 23×40 mm

**Catatan:** STL belum ada di repo ini. Jendela depan harus 23×40 mm agar modul 1.3" 8-pin muat rapat. Modul 1.54" **tidak** muat tanpa redesign.

## Cetak

- Material: PLA (atau PETG jika case di dekat TP4056 yang hangat)
- Layer 0.2 mm, dinding 2, infill 15–20%
- Support: biasanya tidak perlu jika jendela menghadap plate sesuai desain

## Isi case yang muat

- ESP32-C3 Super Mini (bukan WROOM-32)
- ST7789 1.3" 8-pin
- TP4056 mini + proteksi
- MAX98357A
- TTP223
- LiPo pipih 400–800 mAh (bukan 18650)
- Speaker tipis 4–8 Ω
- microSD SPI opsional

Tidak muat: PAM8403, ESP32 DevKit besar, LCD 1.54".

Panduan rakit + pin firmware 0.5.1: https://rz7mong.github.io/mochi-rzmong/hardware.html
