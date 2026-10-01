"""Component envelopes (mm). Every number has a source; ASSUMED = not found in a datasheet/listing.
Envelope = body + keep-out for wires/solder/leads, as axis-aligned box (L, W, H) in the component's own frame:
  L along local x, W along local y, H along local z (H = thickness, PCB bottom at local z=0).
'connector' = which local face the connector/card slot is on (for access checks).
Repo sources (rz7mong/mochi-rzmong @11328ef): see REPORT.md table."""
COMPONENTS = {
 'battery_LiPo501640': dict(
    body=(40.0, 16.0, 5.0),                      # DNK501640 datasheet: 5.0 x 16 x 40 cell, L1 42 incl. PCM
    env=(42.0, 16.0 + 0.5, 5.0 + 0.5),           # L1 42 (cell+PCM), leads folded flat along PCM/side (ASSUMED); +0.5 swelling / width tolerance
    src='DNK501640 280 mAh spec (dnkpower.com): L1xWxT 42x16x5.0 incl. PCM', connector=None),
 'esp32c3_supermini': dict(
    body=(22.52, 18.0, 4.3),
    env=(22.52 + 1.5, 18.0 + 2*1.5, 4.3 + 1.0),  # USB-C overhang ~1.5-2 (sigmdel: 24 incl. USB); wire bends 1.5/side (ASSUMED); 1.0 underside joints (ASSUMED)
    src='22.52x18 (espboards/sigmdel; 24 mm incl. USB-C). Height ASSUMED: PCB ~1.0 + USB-C top-mount receptacle 3.2 = 4.3',
    connector='+x'),
 'tp4056_typec_dw01': dict(
    body=(28.0, 17.3, 4.9),
    env=(28.0, 17.3, 4.9 + 0.5),                 # wires leave the B+/B-/OUT pads upward (no end keep-out); +0.5 underside joints (ASSUMED)
    src='open-electronics TP4056A+DW01A+FS8205A Type-C: 28 x 17.3 x 4.9 mm (mikroelectron: 29 x 17.3 x 4.3)',
    connector='+x'),
 'max98357a': dict(
    body=(19.4, 17.8, 3.0),
    env=(19.4 + 2.0, 17.8, 3.0 + 0.5),           # wires direct-soldered at header edge (+2, ASSUMED); NO screw terminal
    src='Adafruit 3006: 19.4 x 17.8 x 3.0 mm (without 3.5 mm terminal block / header)', connector=None),
 'cap_470uF_10V': dict(
    body=(11.5, 8.0, 8.0),
    env=(11.5 + 2.0, 8.0, 8.0),                  # lying on its side, leads bent 2 mm (ASSUMED)
    src='Panasonic EEU-FC1A471 / Samyoung NXB10V470M8x11.5: D8 x 11.5 mm (6.3x11 option: Rubycon 10YXJ470M6.3X11)',
    connector=None),
 'speaker_20mm': dict(
    body=(20.0, 20.0, 4.3),
    env=(20.0 + 1.5, 20.0, 4.3),                 # solder tabs/wires on rim +1.5 (ASSUMED)
    src='Taoglas SPKM.20.8.A 20 mm 8 ohm (3.6 mm datasheet / 4.3 mm listing); SparkFun 20 mm 1 W: 4 mm. Repo: "speaker tipis 4-8 ohm" (size not given -> ASSUMED 20 mm)',
    connector=None),
 'ttp223_red_15x11': dict(
    body=(15.0, 11.0, 3.0),
    env=(15.0 + 1.5, 11.0, 3.0),                 # height ASSUMED (PCB 1.6 + SOT-23/LED), header removed, wires +1.5
    src='Red TTP223 module PCB 15 x 11 mm (temperosystems; handsontec 14 x 10). Height ASSUMED 3.0 without header',
    connector=None),
 'switch_SS12D00G3': dict(
    body=(8.8, 3.9, 7.2),
    env=(8.8, 3.9, 7.2 + 2.0),                   # 7.2 incl. 3 mm handle; pins trimmed + wires 2 mm (ASSUMED)
    src='SOFNG SS-12D00-G3: 8.8 x 3.9 x 7.2 mm incl. 3.0 mm handle. Repo names only "saklar On/Off" -> model ASSUMED',
    connector=None),
 'sd_wemos_microsd_shield': dict(
    body=(28.0, 25.6, 5.0),
    env=(28.0, 25.6 + 1.5, 5.0),                 # width 25.6 (D1-mini shield width); 28 x 25 x 5 per listings; wire side +1.5 (ASSUMED)
    src='Wemos/LOLIN D1 mini Micro SD shield: 28 x 25 x 5 mm (alphatronic / ifuturetech listings; no official drawing)',
    connector='-x'),   # card slot edge; ASSUMED card sticks out ~3 mm when inserted
}
# optional alternatives checked separately
ALTERNATIVES = {
 'ttp223b_red_24x24': dict(env=(24.0, 24.0, 7.2), src='TTP223B 24 x 24 x 7.2 mm (fillxpert / circuits-diy listing)'),
 'max98357a_with_terminal': dict(env=(21.4, 17.8, 3.0 + 8.5), src='+3.5 mm-pitch terminal block ~8.5 mm tall (ASSUMED typical)'),
 'cap_470uF_6.3x11': dict(env=(13.0, 6.3, 6.3), src='Rubycon 10YXJ470M6.3X11'),
}
