# Review of designer layout v3 ([pcb/v3/layout_v3_case_frame.json](../../../pcb/v3/layout_v3_case_frame.json))

How it was checked: [`case/scripts/pcb_fit/check_designer_v3.py`](../../../case/scripts/pcb_fit/check_designer_v3.py) → `check_designer_v3.json`. Preview: `designer_v3_in_assembly.png`.
- Exact manifold3d checks against `case_luar_lcd_23_40mm_pcb.stl` and `tatakan_GMT130_fit_pcb.stl`.
- Also against the LCD, TP4056, LiPo, speaker, TTP223 and switch.
- Same assumptions as v2, plus these new models:
  - ESP header plastic as 2.54 mm pieces with the IO2/IO7/IO9 plastic removed.
  - Top jumpers JP1/JP2: Ø1.0, flat.
  - Bottom jumpers JP3/JP4: Ø0.6, flat under the board.
  - Each of the 7 LCD wires as Ø1.0 under the PCB, with the riser inside x ±9.5.
  - Off-board wire stubs: Ø1.0, or Ø1.4 for the 2-wire hole.

## Outline
Identical to the v2 DXF: symmetric difference 0.000 mm² for both the JSON and the SVG. Holes are equal.

## Claimed fixes: all verified
| Claim | Result |
|---|---|
| Header rows at y 4.9 | J3.GND 4.49 mm and J2.SCK 4.43 mm from hole centres |
| Clearance at the M2 holes | Nut (4.62 circumcircle) to header plastic: 0.82 mm. Ø3.5 standoff: 1.38 mm. Ø5 post to nearest fillet: 0.59 (L) / 0.53 (R) mm |
| JP1 through the IO7 slot | 0.53 mm to the ESP header plastic |
| JP2 through the IO9 slot | 0.77 mm to the plastic |
| JP1/JP2 under the ESP | 1.5 mm left under the ESP body |
| JP1 next to C1 | 0.10 mm from the cap body. JP1 must go in before C1 |
| Rear-tab trim ≤1.0 mm | All 7 joints, including U1.3V3, are at 1.0 mm. Joint-to-case min 0.37 mm (was -0.73 mm³ in v2) |
| Rest-pad strip | Empty |
| LCD wires | Riser inside x ±9.5. 0 overlap with the stand, LCD and TP4056 |

## Deviations
**1. SW.B / TTP.GND at y 9.1: ACCEPT.**
Wire stub to the MAX module: SW.B 0.30 mm, TTP.GND 0.10 mm (2-wire bundle). TTP.GND to the cap: 0.37 mm. Fillet gap between the two pads: 0.5 mm, copper gap ≈0.9 mm.

**2. TP.OUT- merged into TTP.GND: ACCEPT.**
No cap conflict any more. TP4056 OUT- carries the whole battery return current (≈1 A peaks with the amp). Use ≥26 AWG for that wire and for SW out. Two stripped 26 AWG conductors fit a 1.1 mm hole.

**3. JP3/JP4 under the board: ACCEPT, with one note.**
- Separation:
  - LCD wires: ≥1.07 mm in plan.
  - M2 posts: JP3 is 6.5 mm from the post edge, JP4 8.2 mm.
  - Board edge: 1.5 mm.
  - Stand, case, LCD: >6 mm.
  - TP4056 top: 5.53 mm below the wires.
- Nearest fillets of other nets: JP3 to J2.MOSI 0.24 and J3.LRC 0.32 mm; JP4 to J1.DC 0.17, JP3.A 0.20 and TTP.OUT 0.20 mm. There is no overlap. Solder those joints first, then lay the Kynar so it doesn't melt.
- **JP3 and JP4 cross each other at (0.3, 5.6)**, inside the LRC/MOSI gap.
  - It is insulated, and the stack is 1.2 mm against a 2.0 mm budget, so it is OK.
  - A crossing is unavoidable with RES left of SCL and JP3.A below JP4.A.
  - Fix it at the crossing with a dab of glue or Kapton.
- In the slide-in path: 0 overlap.

**4. MAX DIN pad 1.8 mm: ACCEPT.**
Annular ring 0.45 mm, which is fine for hand etching. Copper gap to BCLK goes from 0.14 to ≈0.44 mm, so less bridging risk. No fit impact.

## Final position and assembly
- Final position, all parts vs everything: no collisions.
- LiPo foam gap: 2.0 mm to both modules.
- Assembly: 0 overlap at every step.
  - Lift 8 mm forward, then +8 mm slide.
  - LiPo push.
  - Stand insertion, and the stand body vs the LCD wire run under the PCB.
- The only remaining contact is the 0.29 mm³ stand/case interference, which already exists in the original stand and case files.

## Verdict
**FINAL GO.** Fit-wise no moves are required.

Assembly notes:
- JP1 before C1.
- Solder neighbouring joints before laying JP3/JP4, and fix their crossing.
- Use ≥26 AWG for TP OUT- and SW out.

Still unverified (real parts): the 18.5 x 20 SD module, its pin order (MOSI, CS, GND, VCC, MISO, SCK), and the ESP header pin positions.
