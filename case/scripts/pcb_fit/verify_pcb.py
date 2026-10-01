#!/usr/bin/env python3
"""Exact manifold3d check of a PCB-variant placement against case_luar_lcd_23_40mm_pcb.stl, tatakan_GMT130_fit_pcb.stl,
the LCD module, the carrier PCB slab (outline x z -15.2..-13.6) + 2 mm solder keep-out below, and each other.
Parts sitting ON the board are allowed to touch the PCB top (gap 0)."""
import json, sys, numpy as np, manifold3d as mf
from _paths import *; sys.path.insert(0, '.')
import fit_tatakan_gmt130 as F
box = F.box
P = json.load(open(sys.argv[1]))
C = F.load(CASE_PCB)
T = F.load(STAND_PCB).translate([0, 0, -10.38])
def lcd_module(zf):
    x = F.PCB_W / 2
    m = box(-x, x, F.PCB_FRONT_Y, F.PCB_BACK_Y, zf, zf + F.PCB_H)
    m = m + box(-F.GLASS_W/2, F.GLASS_W/2, F.FRAME_Y_BACK + 0.02, F.PCB_FRONT_Y, zf + 5, zf + 5 + 29.22)
    m = m + box(-10, 10, F.PCB_BACK_Y, F.PCB_BACK_Y + 2.5, zf + 0.3, zf + 4.8)
    return m
L = lcd_module(F.FLOOR_Z + 0.02).translate([0, 0, -10.38])
OUT = json.load(open(OUTLINE_V2))
cs = mf.CrossSection([OUT['outline']])
PCB = mf.Manifold.extrude(cs, 1.6).translate([0, 0, -15.2])
KEEP = mf.Manifold.extrude(cs, 2.0).translate([0, 0, -17.2])
holes = [mf.Manifold.cylinder(1.6 + 2.0 + 0.2, 1.1, 1.1, 24).translate([x, y, -17.3]) for x, y in OUT.get('holes', [])]
for h in holes: PCB = PCB - h
SL = 6.0
def gap(a, b):
    v = (a ^ b).volume()
    return (-1.0, round(v, 3)) if v > 1e-6 else (round(a.min_gap(b, SL), 2), 0.0)
B = {k: box(v['lo'][0], v['hi'][0], v['lo'][1], v['hi'][1], v['lo'][2], v['hi'][2]) for k, v in P.items() if v}
out = {}; bad = []
for k, m in B.items():
    r = {w: gap(m, o) for w, o in (('case', C), ('stand', T), ('lcd', L), ('pcb', PCB), ('pcb_bottom_keepout', KEEP))}
    same = lambda a, b: {a, b} == {'esp32c3_supermini_on_headers', 'esp32c3_usbc_receptacle'} or {a, b} == {'switch_rightangle_offboard', 'switch_handle'}
    others = {k2: gap(m, m2) for k2, m2 in B.items() if k2 != k and not same(k, k2)}
    ov_parts = sum(v[1] for v in others.values())
    near = min(others.items(), key=lambda kv: kv[1][0]) if others else (None, (None, 0))
    ov = sum(x[1] for x in r.values()) + ov_parts
    if ov > 1e-3: bad.append(k)
    out[k] = dict(P[k], **{f'gap_{w}': r[w][0] for w in r}, overlap_mm3=round(ov, 3), nearest_part=near[0], gap_nearest_part=near[1][0])
    print(f"{k:26s} " + ' '.join(f"{w} {r[w][0]}" for w in r) + f"  nearest {near[0]} {near[1][0]}  overlap {ov:.3f}")
# ESP USB-C plug path through the rear port
PW, PH = 12.35, 6.5
e = P.get('esp32c3_usbc_receptacle')
if e:
    cx = (e['lo'][0] + e['hi'][0]) / 2; cz = -8.5
    pm = box(cx - PW/2, cx + PW/2, e['hi'][1] + 0.05, e['hi'][1] + 20, cz - PH/2, cz + PH/2)
    v = (pm ^ C).volume(); print('ESP USB-C plug path: overlap', round(v, 3), 'gap', round(pm.min_gap(C, SL), 2) if v < 1e-6 else -1)
t = P.get('tp4056_on_floor')
if t:
    cx = (t['lo'][0] + t['hi'][0]) / 2; cz = t['lo'][2] + 0.5 + 1.6 + 1.6
    pm = box(cx - PW/2, cx + PW/2, t['hi'][1] + 0.05, t['hi'][1] + 20, cz - PH/2, cz + PH/2)
    v = (pm ^ C).volume() + (pm ^ T).volume(); print('TP4056 USB-C plug path: overlap', round(v, 3), 'gap', round(min(pm.min_gap(C, SL), pm.min_gap(T, SL)), 2) if v < 1e-6 else -1)
print('PARTS WITH OVERLAP:', bad or 'none')
json.dump(out, open(sys.argv[1].replace('.json', '_verified.json'), 'w'), indent=1)
