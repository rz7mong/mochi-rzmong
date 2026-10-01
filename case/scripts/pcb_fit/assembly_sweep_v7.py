#!/usr/bin/env python3
"""Assembly path of the populated carrier (PCB + ESP + SD/amp edge modules + cap + pad row + LiPo taped to the SD/amp
fronts) into the PCB-variant case (stand not yet fitted; switch, speaker, TTP223 already glued in the case):
step 1 lift vertically at y-6.5 from below the case opening to the final z; step 2 slide +6.5 in y."""
import json, sys, numpy as np, manifold3d as mf
from _paths import *  # repo-relative paths
import fit_tatakan_gmt130 as F
box = F.box
P = json.load(open(sys.argv[1])); BOFF = 8.0
C = F.load(CASE_PCB)
OUT = json.load(open(OUTLINE_V2))
PCB = mf.Manifold.extrude(mf.CrossSection([OUT['outline']]), 1.6).translate([0, 0, -15.2])   # board (joint keep-out checked in pcb_outline_check_v2.py)
MOV = ['m2_nut_L', 'm2_nut_R', 'esp32c3_supermini_on_headers', 'esp32c3_usbc_receptacle', 'lcd_pad_row_7pin', 'sd_mini6pin_edge', 'max98357a_edge',
       'cap_470uF_upright', 'cap_470uF_flat']   # LiPo is swung in first and parked 6.5 mm forward (bat_swing.py)
FIX = ['switch_rightangle_offboard', 'switch_handle', 'speaker_15x11', 'ttp223_red_15x11']
A = PCB
for k in MOV:
    if k in P: v = P[k]; A = A + box(v['lo'][0], v['hi'][0], v['lo'][1], v['hi'][1], v['lo'][2], v['hi'][2])
OBS = C - mf.Manifold.cylinder(3, 2.0, 2.0, 24).translate([0, 30.5, -17.3])
for k in FIX:
    if k in P: v = P[k]; OBS = OBS + box(v['lo'][0], v['hi'][0], v['lo'][1], v['hi'][1], v['lo'][2], v['hi'][2])
bp = P['battery_LiPo501640']; OBS = OBS + box(bp['lo'][0], bp['hi'][0], bp['lo'][1] - 6.5, bp['hi'][1] - 6.5, bp['lo'][2], bp['hi'][2])
worst = 0; wpos = None
for dz in np.arange(-25.0, 0.01, 0.25):
    v = (A.translate([0, -BOFF, dz]) ^ OBS).volume()
    if v > worst: worst, wpos = v, ('lift', dz)
for dy in np.arange(-BOFF, 0.01, 0.25):
    v = (A.translate([0, dy, 0]) ^ OBS).volume()
    if v > worst: worst, wpos = v, ('slide', dy)
print('max overlap along path %.3f mm3 at %s' % (worst, wpos))
print('--- per part (with PCB slab), offset', BOFF)

for k in MOV:
    if k not in P: continue
    v = P[k]; Bk = box(v['lo'][0], v['hi'][0], v['lo'][1], v['hi'][1], v['lo'][2], v['hi'][2])
    l = max(((Bk.translate([0, -BOFF, dz]) ^ OBS).volume(), dz) for dz in np.arange(-25.0, 0.01, 0.25))
    s = max(((Bk.translate([0, dy, 0]) ^ OBS).volume(), dy) for dy in np.arange(-BOFF, 0.01, 0.25))
    print(f'{k:30s} lift {l[0]:.3f}@{l[1]}  slide {s[0]:.3f}@{s[1]}')
l = max(((PCB.translate([0, -BOFF, dz]) ^ OBS).volume(), dz) for dz in np.arange(-25.0, 0.01, 0.25)); print('pcb', l)

# final step: LiPo pushed +6.5 mm from its park position with the carrier in place
A_fin = A
bm = lambda dy: box(bp['lo'][0], bp['hi'][0], bp['lo'][1] + dy, bp['hi'][1] + dy, bp['lo'][2], bp['hi'][2])
print('LiPo push from park: max overlap with case %.3f, with carrier+modules %.3f' % (
    max((bm(dy) ^ C).volume() for dy in np.arange(-6.5, 0.01, 0.25)), max((bm(dy) ^ A_fin).volume() for dy in np.arange(-6.5, 0.01, 0.25))))
