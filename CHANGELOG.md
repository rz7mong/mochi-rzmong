# Changelog

## [0.5.6] — 2026-10-02

### Changed
- **GIF bawaan di flash diganti** dengan set warna baru: 30 slot GIF+WAV (`firmware/assets/builtin/`, urutan di `firmware/assets/meta.json`), total 1.041.648 B (GIF 782.448 + PCM 259.200). App ≈2,25 MB dari 3 MB.
  - `wajah/default`: wajah putih senyum + kedip dari video (loop 7,2 dtk, 120 ms/frame) — wajah Jam HP dan diselang di antara klip lain saat idle.
  - Wajah/musik warna: raspberry, squint, love_hearts_kiss, angry_2, smirk, sleepy, yawn_tired, rainbow, pong.
  - Mobil (14): revs, headlights baru + accel, gtr_rain, road_rage, rotation, speed_2, speed_3, tsurikawa, turbo, car, lb, lb_intro, lb_star.
  - Gundam (6): hadouken_miss, hadouken_hit, blade, mecha_doc, titan, equip (gundam besar tetap dari SD).
- **Reaksi sentuh** (11): tickle, kedip, cinta, marah, ketawa, ngantuk, nguap, pelangi, pong, ngebut, hadouken. `MOCHI_REACT_COUNT` dihitung otomatis.
- **Suara bawaan**: tiap slot punya WAV (8 kHz 16-bit mono) yang diputar langsung dari flash (tanpa salin ke heap). Urutan reaksi: WAV SD → WAV bawaan → jingle. Putar idle dari flash juga bersuara; `default.wav` hanya sekali setelah boot.
- **Jam HP** mengikuti delay frame GIF (sebelumnya dijepit 10–80 ms).
- Pack `assets-v1` diperbarui: versi warna 8 fps (wajah/sleepy, smirk, raspberry, squint, angry_2, musik/pong, rainbow, mobil/revs, headlights), wajah/default baru, wajah/love_hearts_kiss + yawn_tired (+ WAV). 86 GIF + 87 WAV. `themes.json` disamakan (library/, sd-pack/, pack).

### Fixed
- `embed_assets.py` tidak lagi diam-diam membuat gambar pengganti 3 frame; GIF yang hilang menggagalkan build. Bug jam-hp/default (GIF default bawaan ternyata pengganti) selesai.

### Removed
- `firmware/tools/react_b64/`, `firmware/tools/sfx_b64/` (placeholder).

## [0.5.5] — 2026-10-01

### Fixed
- **Jam HP**: wajah diam memakai GIF tertanam `wajah/default` (sebelumnya hanya mencari stem yang tidak ada). SD `/gif/wajah/default.gif` tetap didahulukan.
- **SPI**: bus bersama TFT+SD di-init sebelum `tft.init()`; CS SD ditahan HIGH; rotasi diterapkan ulang setelah `SD.begin`.
- **Upload**: permintaan upload menutup pemutar GIF yang sedang memegang SD, bukan ditolak `sd_busy` selama animasi.
- **Menu sumber**: SD kosong tidak dipaksa kembali ke flash; hanya SD yang tidak terpasang yang mengunci ke flash.
- **Portal captive**: label versi mengikuti `MOCHI_VERSION` (sebelumnya tertinggal di 0.5.1).
- **HANDOFF**: migrasi rotasi NVS hanya untuk firmware ≤ 0.5.3, bukan ≤ 0.5.4.

### Notes
- GPIO8 (I2S DIN, pin strapping) dan GPIO20/21 (UART0 + I2S) tidak diubah — itu kabel yang sudah disolder. Bunyi plok saat boot tetap mungkin.


## [0.5.4] — 2026-10-01

### Changed
- **Rotasi layar default 2** (180°): LCD GMT130 kini dipasang **pin di bawah** di tatakan baru. `MOCHI_DEFAULT_ROTATION` di `MochiRzmong.h` (override: `-DMOCHI_DEFAULT_ROTATION=0` untuk tatakan lama / pin di atas).
- **NVS**: nilai `rot` yang tersimpan oleh firmware ≤ 0.5.3 digeser +2 sekali saat boot pertama (penanda `rotv`). Setelan lain (tema, volume, Chronos, dll.) tidak disentuh. Menu **Rotasi layar** tetap memutar 90° per langkah.
- `/api/status` menampilkan `rot`.

### Added
- **Case**: `case/tatakan_GMT130_fit.stl` — tatakan untuk LCD GMT130 27.78×39.22 mm (jendela 23.6×23.6 mm + bevel 1.2 mm, rel samping 28.18 mm + kanal PCB 2.05 mm, lantai 0.6 mm, takik 20 mm untuk kabel solder). Skrip parametrik + cek di `case/scripts/`, pratinjau PNG di `case/`. Belum dicetak uji.
- **PCB carrier (opsional)**: `pcb/` — PCB etsa tangan satu sisi 38.5×36 mm (FR4 1.6 mm, THT) untuk ESP32-C3, modul micro SD 3.3 V ±18.5×20 mm, MAX98357A, elko 470 µF Ø6.3×11; artwork etsa 1:1, sumber layout v3, catatan rakit. Case/tatakan varian `case/*_pcb.stl` (grille speaker, slot saklar, tiang M2), laporan fit `docs/fit/`, skrip `case/scripts/pcb_fit/`. Varian kabel lepas tetap. Belum dibuat/dicetak uji.

### Fixed
- **Docs**: ukuran LCD "23×40 mm" dan "8-pin" salah → **GMT130 27.78×39.22 mm, 7 pin tanpa CS** (area aktif 23.40 mm, lubang Ø2 mm 2.5 mm dari tepi). Catatan pemasangan pin di bawah + kabel solder langsung.

### Notes
- `case/tatakan_lcd_23_40mm.stl` tetap ada sebagai *legacy*. Kulit luar tidak berubah.

## [0.5.3] — 2026-10-01

### Added
- **Jam HP**: tanggal, hari, jam dari HP, waktu HP di atas GIF wajah diam (wajah/default.gif). Angka bawah = baterai HP. Notifikasi tetap mengalahkan layar jam.

## [0.5.2] — 2026-10-01
# Changelog

## [0.5.3] — 2026-10-01

### Fixed
- **GIF**: palet RGB565 big-endian, piksel transparan dilewati, posisi dari ukuran kanvas.
- **Ketukan**: jeda 320 ms tidak memutar ulang GIF/SFX yang sama. Ketuk 1x reaksi, ketuk 2x menu.
- **Mode acak**: tema acak tidak ditulis ke NVS. Tema kosong tidak mematikan SD.
- **Menu**: redraw hanya saat berubah. Footer menampilkan snd/bisu.
- **Chronos**: notifikasi, panggilan, dan navigasi memotong GIF. `playFrame` tidak menahan `watch.loop()`. Panggilan berikutnya tetap tergambar. Nav tidak memicu reaksi palsu.
- **SFX**: WAV dimuat ke buffer RAM yang dipakai ulang (maks. 48 KB), GIF dan suara berjalan bersama.
- **Upload**: CORS di handler POST, tolak saat SD sibuk, scan ulang, tema divalidasi.
- **CI**: Pages di-deploy ulang setelah `Build firmware.bin` sukses (commit GITHUB_TOKEN tidak memicu push).

### Unchanged
- Nama AP `rzmong mochi` dan sandi `rzmong123`. Aset GIF/SFX tidak diubah.


## [0.5.1] — 2026-09-30

### Changed
- **Wiring diagram**: `docs/wiring-0.5.1.jpg` resmi (pin 0.5.1) dipasang di hardware.html. Workflow impor catbox tidak lagi menimpa file ini.
- **Docs sync**: Pages, PRODUCT, README, HANDOFF, hardware/blueprint, tutorial → **0.5.1**
- **Blueprint**: pinout mengikuti `MochiRzmong.h` + `User_Setup_ST7789.h` (bukan skema lama RST=8 / MISO=2 / DIN=9)
- **Model hardware**: ESP32-C3 Super Mini + ST7789 1.3" 240×240 PCB 23×40 mm

### Notes
- Jangan flash zip prebuilt 0.4.7 jika butuh Chronos-nav / serviceNet / captive upload
- Prefer **http://192.168.4.1/** di AP perangkat

## [0.4.7] — 2026-09-30

### Changed
- **Docs sync**: all Pages + PRODUCT + README + firmware version string → **0.4.7**
- **Studio**: GIF target **599 KB**; tries longer duration first (up to ~8s), then lowers quality
- **pengaturan.html**: clear offline-first guidance; mixed-content warning for Pages→HTTP AP

### Notes
- Prefer **http://192.168.4.1/** on device AP for settings (no mixed content, works without internet)
- Studio on GitHub Pages needs internet (FFmpeg.wasm); upload still needs join AP

## [0.4.5] — 2026-09-30

### Added
- GIF+SFX path pairing on SD (`playSfxForGifPath`)
- Studio auto-extract WAV from video track

## [0.4.0] — 2026-09-30

### Added
- Studio Convert + Upload (FFmpeg.wasm + `POST /api/upload`)
- Upload max ~600 KB, SD required

## [0.3.0] — 2026-09-30

### Added
- Captive settings UI at `http://192.168.4.1/`
- Chronos optional BLE documented

## [0.2.9] — 2026-09-30

sdBusy SPI guard; THIRD_PARTY_NOTICES; pin wording.

## [0.2.8] — 2026-09-30

Wi-Fi `rzmong mochi` / `rzmong123`.

## [0.2.6] — 2026-09-30

Dual theme selection.
