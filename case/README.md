# Case Mochi rzmong — model terbaru

Target hardware **2026**: ESP32-C3 Super Mini + LCD ST7789 **1.3" 240×240** modul **23×40 mm** (bukan 1.54" / 32 mm).

## File cetak resmi

| File | Fungsi | Ukuran |
| --- | --- | --- |
| [case_luar_lcd_23_40mm.stl](./case_luar_lcd_23_40mm.stl) | Kulit luar | 1.4 MB |
| [tatakan_lcd_23_40mm.stl](./tatakan_lcd_23_40mm.stl) | Dudukan LCD 23×40 mm | 794 KB |

Unduh mentah:

- https://github.com/rz7mong/mochi-rzmong/raw/main/case/case_luar_lcd_23_40mm.stl
- https://github.com/rz7mong/mochi-rzmong/raw/main/case/tatakan_lcd_23_40mm.stl

## Cetak

- Material: PLA (PETG jika dekat TP4056 yang hangat)
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
