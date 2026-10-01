# Skrip cek fit — varian PCB carrier

Skrip yang membuat dan mengecek `case/case_luar_lcd_23_40mm_pcb.stl`, `case/tatakan_GMT130_fit_pcb.stl`, outline PCB v2 dan layout PCB v3. Laporan: [docs/fit/REPORT.md](../../../docs/fit/REPORT.md).

Semua path relatif ke repo lewat [`_paths.py`](_paths.py). Jalankan dari folder ini:

```bash
pip install numpy scipy trimesh manifold3d shapely matplotlib
cd case/scripts/pcb_fit
python check_designer_v3.py        # cek fit layout pcb/v3 → docs/fit/pcb_v3/check_designer_v3.json
python render_designer_v3.py       # → docs/fit/pcb_v3/designer_v3_in_assembly.png
```

| Skrip | Fungsi |
| --- | --- |
| `make_pcb_variant.py` | Buat dua STL varian PCB dari STL asli (grille speaker, slot saklar, pad tumpuan belakang; tiang M2 di tatakan) |
| `voxelize.py`, `cavity.py` | Model voxel 0.5 mm rongga case (`*.npz`, tidak di-commit; set `CASE`/`STAND`/`OUT`/`OCC`/`CAVOUT` untuk varian PCB) |
| `pcb_space.py`, `pcb_assembly_region.py`, `pcb_outline_check.py`, `pcb_outline_check_v2.py` | Ruang PCB, area yang bisa dirakit, outline v1/v2 (v2 → `pcb/outline/`) |
| `components.py` | Dimensi komponen + asumsi |
| `place.py`, `verify.py` | Penempatan varian kabel lepas |
| `place_pcb*.py`, `pcb_common.py`, `verify_pcb.py` | Penempatan varian PCB (v7 final) |
| `assembly_sweep_v7.py`, `bat_swing.py`, `battery_insert_check.py`, `stand_insert_check.py` | Cek urutan rakit |
| `check_designer_v3.py`, `render_designer_v3.py` | Cek layout PCB v3 terhadap case/tatakan + semua komponen |
| `render_previews.py`, `render3d.py`, `headroom_v2.py` | Pratinjau PNG (ditulis ke folder ini; salin ke `docs/fit/` bila perlu) |

`placement_*.json`, `pcb_recommended_outline.json` (v1) dan `pcb_assembly_region.json` adalah hasil perantara yang dibaca skrip lain. Hasil final terverifikasi: [docs/fit/placement_pcb_v7_cap6.3_verified.json](../../../docs/fit/placement_pcb_v7_cap6.3_verified.json).

Untuk menjalankan ulang seluruh rantai dari nol, buat dulu `*.npz` dengan `voxelize.py` + `cavity.py` (lihat docstring tiap skrip).
