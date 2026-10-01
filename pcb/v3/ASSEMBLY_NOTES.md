# Mochi carrier v3 - assembly notes (hand-etched, single-sided, THT)

Frame: case STL mm, -y = LCD/front, +y = rear/USB. Copper on the bottom.

## Before etching
- Print copper_mirrored_1to1.pdf at 100 %. Check the 10 mm bar.
- Drill: 0.9 mm everywhere except J1.RES, J1.SCL and the "GND x2" pad (1.1 mm, two wires each). M2 holes 2.2 mm.

## Order of assembly
1. **Cut the ESP header strips.**
   - Remove pins IO2, IO7 and IO9 **including their plastic**. JP1 passes through the IO7 slot and JP2 through the IO9 slot.
   - Left strip pieces: [IO5 IO6] [IO8] [IO10 IO20 IO21].
   - Right strip pieces: [5V GND 3V3 IO4 IO3] [IO1 IO0].
2. **MAX98357A header:** cut the SD and GAIN pins. The row is then [VIN GND] + [DIN BCLK LRC], reading VIN..LRC left to right.
3. **JP1 (VIN) and JP2 (GND), top side, about 1 mm insulated wire, laid flat.**
   - JP1: JP1.A (4.2,31.8) → (-5,25.8) → IO7 slot → (-9.7,25.8) → (-10.4,22) → (-11.6,20) → JP1.B (-16.3,16.8).
   - JP2: JP2.A (4.6,28.6) → (-5.3,20.7) → IO9 slot → (-9.6,20.7) → JP2.B (-13,16.7).
   - Both run under the ESP, so they **must go in before the ESP**.
   - **JP1.B must be fitted before C1.** The JP1 wire passes only 0.1 mm from the cap body.
4. **C1** 470 µF 10 V, Ø6.3 x 11, upright. Bend the leads out to 3.5 mm. + goes to the left pad.
5. **ESP32-C3 Super Mini** on 2.5 mm headers, USB-C to the rear.
6. **SD and MAX right-angle headers** (row y 4.9), modules standing on edge.
   - SD pin order on the board, left to right: MOSI, CS, GND, VCC, MISO, SCK. The module must match, or be wired to match.
7. **JP3 (G0) and JP4 (G4), COPPER side.** Use thin insulated wire (30AWG Kynar / wire-wrap, OD ≤ 0.6 mm), laid flat on the bottom.
   - JP3: JP3.A (11.3,9.6) → (3,8.3) → (-0.7,4.6) → (-0.7,2.6) → (-4,2.6) → J1.RES.
   - JP4: JP4.A (16.5,11.5) → (9.4,11.5) → (3,9.4) → (0.3,6.7) → (0.3,2.6) → J1.SCL.
   - Both pass through the joint gap between MAX.LRC and SD.MOSI. They never cross the SD or MAX header or the modules on top, so the header height does not matter.
   - Keep them flat (within the 2 mm bottom zone) and away from the M2 posts.
8. **Off-board wires:**
   - SW out (VIN, from the slide switch).
   - GND x2: TTP223 GND **and** TP4056 OUT- in one 1.1 mm hole.
   - TTP OUT (G1).
   - TTP223 3V3 goes to the J1 BLK/VCC pad.
   - The speaker is wired directly to the MAX module terminals.
   - TP4056 OUT+ goes to the switch input off-board.
9. **LCD (ST7789, GMT130) 7-wire bundle.** J1 order RES, SCL, DC, SDA, GND, BLK, VCC at y -0.7, x -5.28..9.96.
   - Solder to the bottom pads, entering from below.
   - The riser behind the LCD must stay within **x ±9.5**. Fan out toward VCC (x 9.96) **only once past y -3.6**, under the PCB.
   - RES and SCL share their joints with JP3 and JP4.

## Trimming (bottom)
- Trim **U1.3V3 and ALL rear-tab joints** (U1.IO5, U1.IO6, U1.5V, U1.GND, U1.3V3, JP1.A, JP2.A) to **≤ 1.0 mm** below the board, with low fillets.
- No solder at all in the strip x ±2.5, y 22..33.5 (rest pad). The board has no pads there.
- All other joints: ≤ 2.0 mm.

## Final notes from case fit check (v3 approved)
- Use 26 AWG or thicker for the merged GND x2 wire (TTP.GND + TP4056 OUT-) and SW.B: they carry full battery current (~1 A peaks).
- Fit JP1 before C1 (0.10 mm to the cap body).
- Solder J1.DC, JP3.A, TTP.OUT, J2.MOSI and J3.LRC BEFORE laying the JP3/JP4 Kynar wires under the board.
- JP3 and JP4 cross at (0.3, 5.6): fix with a dab of glue or Kapton tape.
- Still verify against real parts: SD module size (~18.5x20) and pin order, ESP32-C3 Super Mini header positions.
