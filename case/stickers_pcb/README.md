# Mochi rzmong: lembar stiker gaya LBWK — varian PCB carrier

Versi lembar [`../stickers/`](../stickers/) untuk **varian PCB carrier**: [`case_luar_lcd_23_40mm_pcb.stl`](../case_luar_lcd_23_40mm_pcb.stl) + [`tatakan_GMT130_fit_pcb.stl`](../tatakan_GMT130_fit_pcb.stl). Kulit PCB punya **grille speaker** (15 lubang Ø1.5 di atap, x −6.75..4.25, y −2.2..3.7) dan **slot saklar + counterbore** di dinding belakang (x 8.5..14.5, z −8.9..−3.8). Di set asli, ventilasi kubah, strip kubah belakang, dan pod belakang sisi +X menutup area itu. Potongan bertanda **-P** di lembar ini sudah dipotong ulang supaya ada jarak bebas ±1 mm.

Untuk case biasa (`case_luar_lcd_23_40mm.stl`, tanpa grille/slot) tetap pakai set asli.

## Yang berubah dibanding set asli

| # | Stiker | Ukuran asli (mm) | Ukuran PCB (mm) | Perubahan | Penempatan |
|---|---|---|---|---|---|
| **13-P** | Penutup ventilasi kubah (vent) | 12.8 × 18.8 | 12.8 × 15.0 | Ujung belakang dipendekkan 3.8 mm; 5 bar abu-abu tetap di atas 5 alur. | Depan di step depan blok ventilasi (sama). Ujung belakang berhenti di y ≈ −3.3, ±1.2 mm sebelum lubang grille. |
| **15a-P** | Strip kembar kubah, segmen belakang | 5.5 × 9.0 | 5.5 × 3.3 | Ujung depan dipotong 5.7 mm. | Mulai y ≈ +4.7 (1 mm di belakang baris lubang terakhir) s/d y 8; 15b/15c tetap. Celah strip di atas grille disengaja. |
| **16R-P** | ALT pinstripe belakang (2×) | 2.0 × 30.8 | 2.0 × 25.1 | Ujung depan dipotong 5.7 mm. | Hanya jika pakai ALT: mulai y ≈ +4.7, bukan dari ujung ventilasi. |
| **16C-P** | ALT strip tengah, potongan belakang | 3.5 × 30.8 | 3.5 × 25.1 | Ujung depan dipotong 5.7 mm. | Hanya jika pakai ALT: mulai y ≈ +4.7. |
| **9L-P** | Tail-light pod sisi +X (kiri mobil) | 16.0 × 7.5 | 16.0 × 7.5 + takik | takik 7.4 × 6.2 mm di sudut atas sisi dalam (arah port USB); sisa kaki 1.3 mm di bawah saklar; lampu bulat dalam dihapus. | Posisi sama seperti 9 (tepi dalam 1.8 mm dari port USB, atas 0.85 mm di bawah ledge). Pod 9 sisi −X tidak berubah. |

Spare ikut diganti (spare ventilasi dan spare strip juga versi -P). Ada satu spare **9L-P** tambahan di blok "VARIAN PCB CARRIER" di bawah lembar. Spare pod biasa (9 spare) tetap untuk sisi −X.

**Tidak berubah:** semua stiker lain (samping, sayap, endplate, strut, plat nomor, shield, splitter, grille depan, segmen kubah 14a/14b/15b/15c, strip ALT depan 16F/16C depan). Ukuran, warna, nomor, dan posisinya sama persis dengan set asli, jadi tetap pakai `placement_guide.png` di [`../stickers/`](../stickers/) untuk potongan-potongan itu.

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
- Bahan, persiapan permukaan, dan urutan tempel sama dengan [`../stickers/README.md`](../stickers/README.md).
- **13-P**: tempel dari step depan blok ventilasi seperti biasa. Ujung belakangnya sekarang berhenti di lereng sebelum lubang grille, jadi lubang paling depan tetap terbuka.
- **15a-P**: tempel mulai ±1 mm di belakang baris lubang grille paling belakang, lalu lanjutkan segmen berikutnya seperti biasa. Strip kubah memang terputus di atas grille. Strip ALT belakang (-P) juga mulai dari titik itu.
- **9L-P**: hanya untuk sisi **+X (kiri mobil, sebelah kiri port USB kalau dilihat dari belakang)**. Takiknya menghadap port USB dan mengelilingi counterbore saklar. Pod sisi −X pakai 9 biasa.
- Tekan tepi stiker di sekitar takik dan di ujung strip dengan kuku supaya tidak terangkat. Jangan tempel extra 21 atau sisa vinyl di atas grille atau slot saklar.

## Verifikasi

Dihitung dari STL `case_luar_lcd_23_40mm_pcb.stl` dengan garis potong lembar ini, berdasarkan posisi tempel di placement guide asli (jarak minimum garis potong ke tepi lubang grille / counterbore, diukur di permukaan; negatif = menutup):

| Potongan | Set asli | Lembar ini | Area |
|---|---|---|---|
| 9L-P tail-light (+X) | -5.46 mm | +1.02 mm | saklar |
| 13-P vent | -1.39 mm | +1.23 mm | grille |
| 15a-P | -1.33 mm | +0.99 mm | grille |
| 16R-P (ALT) | -1.09 mm | +1.00 mm | grille |
| 16R-P (ALT) | -1.25 mm | +1.00 mm | grille |
| 16C-P (ALT) | -1.33 mm | +1.00 mm | grille |

Semua potongan lain berjarak lebih jauh atau tidak berada di dekat grille/slot. PDF berukuran A4 (595.28 × 841.89 pt) skala 1:1.
