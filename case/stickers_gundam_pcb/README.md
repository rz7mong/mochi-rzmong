# MOCHI rzmong RZ-78: lembar stiker gaya Gunpla/mecha — varian PCB carrier

Versi lembar [`../stickers_gundam/`](../stickers_gundam/) untuk **varian PCB carrier**: [`case_luar_lcd_23_40mm_pcb.stl`](../case_luar_lcd_23_40mm_pcb.stl) + [`tatakan_GMT130_fit_pcb.stl`](../tatakan_GMT130_fit_pcb.stl). Kulit PCB punya **grille speaker** (15 lubang Ø1.5 di atap, x −6.75..4.25, y −2.2..3.7) dan **slot saklar + counterbore** di dinding belakang (x 8.5..14.5, z −8.9..−3.8). Di set asli, ventilasi kubah, strip kubah belakang, dan pod belakang sisi +X menutup area itu. Potongan bertanda **-P** di lembar ini sudah dipotong ulang supaya ada jarak bebas ±1 mm.

Untuk case biasa (`case_luar_lcd_23_40mm.stl`, tanpa grille/slot) tetap pakai set asli.

## Yang berubah dibanding set asli

| # | Stiker | Ukuran asli (mm) | Ukuran PCB (mm) | Perubahan | Penempatan |
|---|---|---|---|---|---|
| **14-P** | Penutup ventilasi kuning | 12.8 × 18.8 | 12.8 × 15.0 | Bagian belakang digeser maju 3.8 mm; bar hitam tetap di atas 5 alur, segitiga merah tetap ada. | Depan di step depan blok ventilasi. Ujung belakang berhenti di y ≈ −3.3, ±1.2 mm sebelum lubang grille. |
| **16b-P** | Tri-stripe kubah, segmen belakang | 5.5 × 9.0 | 5.5 × 3.3 | Ujung depan dipotong 5.7 mm. | Mulai y ≈ +4.7 s/d y 8; 16c/16d tetap. Celah di atas grille disengaja. |
| **17B-P** | ALT strip biru belakang (2×) | 1.75 × 30.8 | 1.75 × 25.1 | Ujung depan dipotong 5.7 mm. | Hanya jika pakai ALT: mulai y ≈ +4.7. |
| **17C-P** | ALT strip merah tengah, belakang | 1.0 × 30.8 | 1.0 × 25.1 | Ujung depan dipotong 5.7 mm. | Hanya jika pakai ALT: mulai y ≈ +4.7. |
| **10L-P** | Thruster pod sisi +X (kiri mobil) | 16.0 × 7.5 | 16.0 × 7.5 + takik | takik 7.4 × 6.2 mm di sudut atas sisi dalam (arah port USB); sisa kaki 1.3 mm di bawah saklar; nozzle kanan dihapus, bingkai abu-abu mengikuti takik. | Posisi sama seperti 10 (tepi dalam 1.8 mm dari port USB). Pod 10 sisi −X tidak berubah. |

Spare ikut diganti (spare ventilasi dan spare strip juga versi -P). Ada satu spare **10L-P** tambahan di blok "VARIAN PCB CARRIER" di bawah lembar. Spare pod biasa (10 spare) tetap untuk sisi −X.

**Tidak berubah:** semua stiker lain (samping, sayap, endplate, strut, plat nomor, shield, splitter, grille depan, V-fin 15, segmen kubah 16a/16c/16d, strip ALT depan 17B/17C 9.6 mm, extra 21). Ukuran, warna, nomor, dan posisinya sama persis dengan set asli, jadi tetap pakai `placement_guide.png` di [`../stickers_gundam/`](../stickers_gundam/) untuk potongan-potongan itu.

## File

| File | Isinya |
|---|---|
| `sticker_sheet_A4_white_vinyl.pdf` / `.svg` | **File cetak utama.** A4, skala 1:1, gambar + garis potong magenta `#FF00FF` 0.1 mm (layer tersendiri di SVG) |
| `sticker_sheet_A4_white_vinyl_PRINT_ONLY_no_cutlines.pdf` | Halaman yang sama tanpa garis potong, untuk mesin print-and-cut |
| `sticker_sheet_A4_CUT_ONLY.svg` / `.pdf` | Hanya jalur potong, posisinya pas dengan halaman A4 yang sama |
| `sticker_sheet_A4_clear_vinyl.pdf` / `.svg` | Versi vinyl bening (bagian putih dihilangkan), hanya untuk case putih |
| `sticker_sheet_A4_white_vinyl_preview.png` | Pratinjau lembar utama 200 dpi |
| `placement_guide.png` | Posisi potongan -P terhadap grille dan slot saklar, plus tabel perubahan |
| `mockup_stickers_applied.png` | Render case PCB (dari STL) dengan stiker terpasang; lubang grille dan slot saklar terlihat terbuka |

Gaya, warna, bleed 0.5–0.6 mm, margin putih 0.3 mm, dan konvensi garis potong sama dengan set asli. Semua teks tetap di-outline.

## Cetak dan pasang

- Cetak di **100 % / "Actual size"**, jangan "Fit to page". Cek batang 50 mm dan kotak 10 × 10 mm.
- Bahan, persiapan permukaan, dan urutan tempel sama dengan [`../stickers_gundam/README.md`](../stickers_gundam/README.md).
- **14-P**: tempel dari step depan blok ventilasi seperti biasa. Ujung belakangnya sekarang berhenti di lereng sebelum lubang grille, jadi lubang paling depan tetap terbuka.
- **16b-P**: tempel mulai ±1 mm di belakang baris lubang grille paling belakang, lalu lanjutkan segmen berikutnya seperti biasa. Strip kubah memang terputus di atas grille. Strip ALT belakang (-P) juga mulai dari titik itu.
- **10L-P**: hanya untuk sisi **+X (kiri mobil, sebelah kiri port USB kalau dilihat dari belakang)**. Takiknya menghadap port USB dan mengelilingi counterbore saklar. Pod sisi −X pakai 10 biasa.
- Tekan tepi stiker di sekitar takik dan di ujung strip dengan kuku supaya tidak terangkat. Jangan tempel extra 21 atau sisa vinyl di atas grille atau slot saklar.

## Verifikasi

Dihitung dari STL `case_luar_lcd_23_40mm_pcb.stl` dengan garis potong lembar ini, berdasarkan posisi tempel di placement guide asli (jarak minimum garis potong ke tepi lubang grille / counterbore, diukur di permukaan; negatif = menutup):

| Potongan | Set asli | Lembar ini | Area |
|---|---|---|---|
| 10L-P pod (+X) | -5.46 mm | +1.02 mm | saklar |
| 14-P vent | -1.39 mm | +1.23 mm | grille |
| 16b-P | -1.33 mm | +0.99 mm | grille |
| 17B-P (ALT) | -0.90 mm | +1.00 mm | grille |
| 17B-P (ALT) | -1.12 mm | +1.00 mm | grille |
| 17C-P (ALT) | -0.50 mm | +1.06 mm | grille |

Semua potongan lain berjarak lebih jauh atau tidak berada di dekat grille/slot. PDF berukuran A4 (595.28 × 841.89 pt) skala 1:1.
