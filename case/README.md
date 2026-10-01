# Case Mochi rzmong — model terbaru

Target hardware **2026**: ESP32-C3 Super Mini + LCD ST7789 **1.3" 240×240** modul **GMT130-V1.0** (Easyware EP002065), PCB **27.78 × 39.22 mm**, **7 pin tanpa CS** (bukan 1.54" / 32 mm).

> Dokumen lama menyebut "23×40 mm" dan "8-pin" — itu **salah**. Ukuran di bawah dari datasheet modul GMT130.

## File cetak resmi

| File | Fungsi | Ukuran |
| --- | --- | --- |
| [case_luar_lcd_23_40mm.stl](./case_luar_lcd_23_40mm.stl) | Kulit luar (tidak berubah; nama file lama dipertahankan agar tautan tidak putus) | 35.0 MB |
| [tatakan_GMT130_fit.stl](./tatakan_GMT130_fit.stl) | **Dudukan LCD GMT130** 27.78 × 39.22 mm, pin di bawah — **pakai ini** | 25.9 MB |
| [tatakan_lcd_23_40mm.stl](./tatakan_lcd_23_40mm.stl) | *Legacy* — dudukan lama dari asumsi 23×40 mm yang salah; rongga 32.86 mm vs PCB 27.78 mm, LCD GMT130 goyang ke samping | 28.8 MB |

Unduh mentah:

- https://github.com/rz7mong/mochi-rzmong/raw/main/case/case_luar_lcd_23_40mm.stl
- https://github.com/rz7mong/mochi-rzmong/raw/main/case/tatakan_GMT130_fit.stl
- https://github.com/rz7mong/mochi-rzmong/raw/main/case/tatakan_lcd_23_40mm.stl (legacy)

## Ukuran LCD GMT130 (datasheet)

| Bagian | Ukuran |
| --- | --- |
| PCB | 27.78 × 39.22 mm (tebal **diasumsikan 1.6 mm**, tidak ada di gambar) |
| Kaca | 26.16 × 29.22 mm, tebal ≤ 1.5 mm |
| Area aktif | 23.40 × 23.40 mm |
| Lubang | Ø2 mm, 2.5 mm dari tepi (jarak 22.78 × 34.22 mm) |
| Pin | 7: GND VCC SCL SDA RES DC BLK — **tanpa CS** |

## Tatakan GMT130 (`tatakan_GMT130_fit.stl`)

Dibuat dari tatakan lama dengan skrip [`scripts/fit_tatakan_gmt130.py`](./scripts/fit_tatakan_gmt130.py). Kulit luar tidak diubah; tatakan tetap masuk ke celah dasar case (posisi rakit: offset (0, 0, −10.38) mm dari koordinat case).

| | Tatakan lama | Tatakan GMT130 |
| --- | --- | --- |
| Jendela depan | 32.90 × 22.95 mm | 23.60 × 23.60 mm (area aktif + 0.1 mm/sisi), bevel 1.2 mm ke depan |
| Penahan samping | dinding 32.86 mm, LCD goyang | rel samping, lebar 28.18 mm (PCB + 0.2 mm/sisi), kanal PCB 2.05 mm |
| Lantai LCD | slot tembus di alas | lantai 0.6 mm |
| Belakang pin | dinding tepat di belakang pin (±1 mm) | takik 20 mm untuk kabel solder (±2 mm) |

![Tatakan GMT130 di dalam case, tampak depan](./preview_tatakan_GMT130_assembly_front.png)
![Tatakan GMT130 + modul LCD](./preview_tatakan_GMT130_iso.png)

Biru tua = PCB, hitam = kaca, biru muda = area aktif 23.4 mm.

### Asumsi (belum dicetak uji)

- Tebal PCB 1.6 mm, kaca ≤ 1.5 mm, sambungan solder/kabel di belakang baris pin ≤ 2 mm.
- **Cetak tatakan dulu** dan cek LCD masuk sebelum merakit semuanya. Jika kanal terlalu sempit, amplas sedikit atau ubah `POCKET_CLR` di skrip lalu generate ulang.

### Generate ulang / cek

```bash
pip install numpy trimesh manifold3d shapely
python case/scripts/fit_tatakan_gmt130.py      # tulis case/tatakan_GMT130_fit.stl dari tatakan lama
python case/scripts/check_fit.py               # tabrakan LCD / tatakan / case
python case/scripts/check_view.py              # % area aktif yang tertutup visor
```

## Cetak

- Material: PLA (PETG jika dekat TP4056 yang hangat)
- Layer 0.2 mm, dinding 2, infill 15–20%
- Support: biasanya tidak perlu jika jendela menghadap plate sesuai desain
- Resin: permukaan kubah sudah dihaluskan; cetak miring dengan support. Tatakan punya bibir pengunci yang masuk ke celah di dasar case (celah ±0.2 mm, 3 tonjolan penahan di bibir kiri).
- Tatakan GMT130: dinding jendela/rel tipis — layer 0.2 mm atau lebih halus, cek kanal PCB bersih dari stringing.

## Rakit LCD

1. Solder kabel **langsung** ke pad LCD (tanpa pin header), arahkan ke belakang. Sambungan ≤ 2 mm.
2. BLK → 3V3. Tidak ada CS (GPIO7 dibiarkan kosong).
3. Masukkan LCD ke tatakan **dari atas, pin di bawah** (tepi pin di lantai tatakan), kaca menghadap jendela.
4. Firmware **0.5.4+** memakai rotasi default **2** (180°) untuk posisi ini, jadi gambar langsung tegak. Jika terbalik (mis. tatakan lama / pin di atas): menu LCD → **Rotasi layar** 2×, atau build dengan `-DMOCHI_DEFAULT_ROTATION=0`.

## Isi case yang muat

- ESP32-C3 Super Mini (bukan WROOM-32)
- ST7789 1.3" GMT130 7 pin (27.78 × 39.22 mm)
- TP4056 mini + proteksi
- MAX98357A
- TTP223
- LiPo pipih 400–800 mAh (bukan 18650)
- Speaker tipis 4–8 Ω
- microSD SPI opsional

Tidak muat: PAM8403, ESP32 DevKit besar, LCD 1.54".

Panduan rakit + pin firmware 0.5.4: https://rz7mong.github.io/mochi-rzmong/hardware.html
