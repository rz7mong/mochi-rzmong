> **Lokasi file di repo ini** (laporan asli menyebut nama file tanpa folder):
> STL baru → [`case/`](../../case/README.md#varian-pcb-carrier) · outline v2 → [`pcb/outline/`](../../pcb/outline/) · layout PCB v3 → [`pcb/v3/`](../../pcb/README.md) ·
> skrip + JSON perantara → [`case/scripts/pcb_fit/`](../../case/scripts/pcb_fit/) · pratinjau + `placement_pcb_v7_cap6.3_verified.json` → folder ini ·
> review layout v3 → [`pcb_v3/REVIEW.md`](pcb_v3/REVIEW.md). File `*.npz`, `component_envelopes_*.stl`, `assembly_*.scad` dan pratinjau varian kabel lepas tidak disertakan (bisa dibuat ulang dengan skrip).

# Component fit check: case_luar_lcd_23_40mm.stl + tatakan_GMT130_fit.stl (stand offset z -10.38)

All coordinates are in the case STL frame (mm): -y = face/LCD side, +y = rear (USB port), z up.
The stand floor top is z -26.73. The original STLs are not modified. All new files are in this folder.
Every fit was checked exactly with manifold3d, using real meshes and component envelope boxes
(overlap volume and min gap). Placement was searched on a 0.5 mm voxel grid with ≥0.5 mm clearance.

## Component list from the repo (rz7mong/mochi-rzmong @ 11328ef)

| Part | Repo source |
|---|---|
| ESP32-C3 Super Mini | README.md L56-80 (wiring 0.5.3), case/README.md "Isi case yang muat", firmware/include/MochiRzmong.h L12-19 |
| ST7789 1.3" 8-pin (GMT130), BLK tied to 3V3, so 7 wires | README.md L56-80 |
| microSD over SPI, "must be native 3.3 V" | README.md L56-80. docs/wiring-0.5.1.jpg shows a Wemos Micro SD shield |
| MAX98357A I2S plus a ~470 µF ≥10 V cap at VIN | README.md L56-80 |
| TTP223 touch on GPIO1 | README.md, docs/hardware.html |
| TP4056 + DW01/8205A, then switch, then VIN | README.md power section, docs/wiring-0.5.1.jpg |
| Flat LiPo (400-800 / 400-1000 mAh). Parent specified 501640 | case/README.md, docs/hardware.html |
| Thin 4-8 Ω speaker | case/README.md |

Datasheet and listing dimensions, plus every assumption, are in `components.py`. The ones that matter most:
- LiPo 501640 envelope: 42 x 16.5 x 5.5 (cell 40 x 16 x 5 plus PCM).
- ESP32-C3 Super Mini: 22.52 x 18, 24 including the USB-C overhang.
- MAX98357A (Adafruit 3006): 19.4 x 17.8. Its 7-pin header runs along the 17.8 mm edge.
- PUI AS01508MS-SP11-WP-R speaker: 15 x 11 x 3.5 (datasheet).
- Mini 6-pin microSD module: 18.5 x 20 x ~4. **ASSUMED** from listings (18x18, 18x20, 18.5x17.5).
- 470 µF 10 V: Ø6.3 x 11 (Rubycon 10YXJ470M6.3X11), or Ø8 x 11.5.
- SK-12D07-class right-angle slide switch body: 8.6 x 4.7 (LCSC C5289941). 3.7 mm height and the handle are **ASSUMED**.

## A) Loose modules, original STLs (`placement.json`, `placement_verified.json`)
Everything fits with zero overlap:
- TP4056: on the floor, USB-C into the existing rear-bottom slot.
- ESP32: USB-C into the existing 13x8 rear port.
- LiPo 42 mm: on its 16 mm edge along x. Case gap is 0.32 mm (critical); a 45 mm cell does not fit.
- Wemos SD shield: upright behind the LCD.
- 20 mm speaker: face up under the top. Needs a grille.
- TTP223: against the left cheek.
- MAX98357A and the cap: upright.
- SS-12D00 switch: in the rear pocket. Needs a hole in the wall.

Previews: `sections_loose.png`, `assembly3d_loose.png`, `component_envelopes_loose.stl`.

## B) Custom carrier PCB (hand-etched single-sided 1.6 mm FR4, all THT). Final layout = v7

### Outline (use v2; v1 is superseded)
Files: `pcb_recommended_outline_v2.dxf` (outline plus 2 holes), `.svg`, `.json`. Checked by `pcb_outline_check_v2.py`.

- Polygon (case x, y):
  (-19.5,-2.5) (19,-2.5) (19,10.5) (17.5,18.5) (16.5,19.5) (12,20.5) (10.5,24.5) (9.5,25.5) (9.5,33) (8,33.5)
  (-8.5,33.5) (-10,33) (-10.5,32.5) (-10.5,26.5) (-11.5,21.5) (-12.5,20.5) (-17,19.5) (-18.5,17) (-19.5,11.5)
- **Max outline: 38.5 W x 36 D, area 1131 mm².**
  - Front block: 38.5 x 13 (y -2.5..10.5).
  - Rear tab: 20 wide (x -10.5..9.5) out to y 33.5.
- **28 x 40 is impossible.** Depth is limited to ~36 mm, between the LCD wires (y ≈ -3) and the rear wall (y 34). Largest full-depth rectangle is 20 x 36.
- Why v1 was dropped: v1 (40.5 x 36, with wide pocket wings to x ±16.5) fit in its final position but **cannot be assembled**:
  - The pocket wings sit behind a throat that is only x ±11.5 wide.
  - Below the wings the case is solid.
- v2 assembly (verified with 0 overlap, case only, stand not fitted yet): the board rises vertically 8 mm forward of its final position, then slides +8 mm in y.
- PCB plane: bottom at z -15.2, top at z -13.6. This puts the ESP on a 2.5 mm header with its USB-C centre at z -8.5, which matches the rear port centre.

### Heights
- **Above the board top:**
  - 5.5 mm is clear everywhere (min gap 0.32 mm).
  - Free height from the case: front strip ≥29 mm, side wedges ≥24.5, ESP zone ≥13.5. Rear tab is 11 mm, limited by the pocket ceiling at z -2.5.
  - The switch above the right rear corner leaves only 5.2 mm over x 7.2..9.5, y 29..33.7.
  - Your 5-6 mm modules and 8-9 mm cap are all fine.
- **Below the board:**
  - 2.0 mm solder-joint keep-out everywhere (5 mm gap to the case and stand).
  - Rear tab (y > 26): only 1.2 mm, because the pocket floor plate is 1.8 mm below the board.
  - **No joints at all in the strip x ±2.5, y 22..33.5.** The rear rest pad slides through there.
  - The TP4056 sits under the centre (x ±8.8, y -3..25), with its top 6 mm below the PCB.

### Edges
- **Front edge (y -2.5)** faces the LCD. The 7-pad row (2.54 mm pitch) is at x ±9, y ≈ -1.
- **Rear tab edge (y 33.5)** has the ESP32 USB-C. Receptacle front is at y 34, centre x 0, z -8.5, into the existing rear port.
- **SD:** there is no reachable slot edge. The SD module stands on edge inside, so use Wi-Fi upload to the SD or open the case to swap the card.
- **Switch:** cannot be on the PCB. Each pocket wing is 8.25 mm and a THT right-angle switch body is 8.6 mm, and the rear tab must stay narrow for assembly. Mount it **off-board on wires**, glued in the right rear pocket above the ESP edge: (7.2,29,-7.9)-(15.8,33.7,-4.2). The handle goes through a new rear-wall slot right of the USB port.

### Mounting
- 2 x M2 holes, Ø2.2 in the PCB, at **(-14.5, 0.5) and (14.5, 0.5)**, on Ø5 posts on the stand.
- Screws go **M2 x 16 from under the stand base**, up through the post (Ø2.4 through-hole, Ø4.4 x 1.8 counterbore underneath), into an **M2 nut or brass standoff glued or soldered on the PCB top**.
- Screws from above are impossible because the top is inside the closed case. 2 mm self-tapping screws would not grip FR4.
- At the rear the board rests on a Ø4 rest pad at (0, 30.5) on the pocket floor, and is held by the USB-C receptacle in the port. There is no rear screw.

### Final layout v7 (`placement_pcb_v7_cap6.3_verified.json`, all 0 overlap)

| Part | Box lo-hi (case frame) | Min gap | Notes |
|---|---|---|---|
| ESP32-C3 on 2.5 mm header | (-9,10,-13.6)-(9,32.5,-8.1) + USB-C (-4.5,26.6,-10.1)-(4.5,34,-6.9) | case 1.6 | Plug path through the port: gap 0.11 |
| Mini SD module, edge-mounted, right-angle header | (-19.5,4,-13)-(-1,9,9.5) | 1.0 to ESP | |
| MAX98357A, edge-mounted, right-angle header | (1,4,-13)-(18.8,8,8.9) | | Wire the speaker directly; no screw terminal |
| 470 µF Ø6.3 x 11, upright | (-18.5,10,-13)-(-11.7,16.8,0.5) | | Ø8 does NOT fit, neither flat nor upright |
| LCD pad row | (-9,-2.5)-(9,0.5) | | |
| M2 nuts on top | at holes, 1.6 tall | | |
| LiPo 501640 (off-board), on edge, taped with 2 mm foam to the front of the SD/amp | (-21,-3.5,-10.5)-(21,2,6) | case 0.46 | Hovers over the pad row |
| PUI 15x11 speaker (off-board), face up | (-9,-5,16.5)-(6.5,6.5,20.5) | case 0.5 | |
| TTP223 (off-board), face up under the top front | (-8,-17,15)-(8.5,-6,18) | case 0.68 | Needs a 2-3 mm foam/glue spacer to the ceiling |
| Switch (off-board) | see Edges | ESP 0.2 | |
| TP4056 on the stand floor | (-8.5,-3,-26.73)-(8.8,25,-21.3) | | USB-C into the existing bottom slot, gap 0.45 |

### Assembly order (each step verified)
`assembly_sweep_v7.py`, `bat_swing.py`, `battery_insert_check.py`, `stand_insert_check.py`

1. Turn the case upside down. Glue the speaker, TTP223 and switch.
2. Put the LiPo in through the bottom opening, standing on its end. Swing it horizontal, roll it onto its edge, and park it at y -10..-4.5 (where the LCD will go). It cannot go in straight: the bottom opening is only 40-41.5 mm wide.
3. Insert the populated carrier: rise 8 mm forward of final, then slide +8 mm.
4. Push the LiPo +6.5 mm onto its foam.
5. Insert the stand with the LCD and TP4056 vertically. The LCD wires are already soldered.
6. Fit the 2 x M2 screws from below.

There is a 0.29 mm³ stand/case interference at x -28.5, y -1..9, z -26.7..-25.3. It already exists in the ORIGINAL stand + case and was not introduced here.

### Case openings
| Opening | Status |
|---|---|
| ESP USB-C | Existing 13x8 rear port. No change |
| TP4056 USB-C | Existing rear-bottom slot (16 x ~8.7, open to the desk). No change |
| Slide switch | New 4 x 3.3 slot at x 9.5..13.5, z -8..-4.7 through the 5.5 mm rear wall, plus an outside counterbore x 8.5..14.5, z -8.9..-3.8, 2.5 mm deep |
| Speaker grille | New: 15 holes Ø1.5 at 2.2 pitch in a 12 x 8 ellipse centred (-1.25, 0.75), through the top shell |
| SD slot | None (not practical) |

### New STLs (originals untouched, both watertight)
- `case_luar_lcd_23_40mm_pcb.stl`: grille, switch slot + counterbore, rear rest pad.
- `tatakan_GMT130_fit_pcb.stl`: back-box walls behind the LCD rails removed (y > -4, z > -17.4), plus 2 posts Ø5 with Ø2.4 through-holes and bottom counterbores.

### Previews
`pcb_layout_v2_top.png`, `sections_pcb_v7.png`, `assembly3d_pcb_v7.png`, `pcb_headroom_map_v2.png`, `component_envelopes_pcb_v7.stl`, `assembly_pcb_v7.scad` (open in the OpenSCAD GUI).

## Open questions
- **SD module:** the Wemos shield (28 x 25.6) and Adafruit 4682 (25.4 x 22.8) do not fit on the carrier. You need a small 18x18 to 18x20 6-pin module that runs directly on 3.3 V. Many "mini micro SD" listings have an LDO and level shifter wanting a 4.5-5 V supply, so confirm before buying.
- **Speaker:** the 20 mm round no longer fits in the PCB variant. Use a 15x11x3.5 rectangular.
- **Cap:** Ø6.3 upright instead of Ø8 lying flat.
- **TTP223 sensitivity:** it sits under ~2 mm of top shell plus a 2-4 mm gap, partly under the 4-6 mm decorative raised vent. A copper-foil pad may be needed.
- **LiPo:** 42 mm is marginal (0.46 mm gap) and needs the swing-in. A ≤38 mm cell would be much easier.
- **BOOT button:** the ESP BOOT/RESET buttons near the USB end lie under the switch, 0.2 mm away. Not needed for native-USB flashing.
