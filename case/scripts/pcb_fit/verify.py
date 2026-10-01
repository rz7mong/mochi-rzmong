#!/usr/bin/env python3
"""Exact check of placement.json against the real meshes (manifold3d): overlap volume + min gap of every component
envelope vs case / stand / LCD module and vs each other; USB plug paths; writes placement_verified.json."""
import json, sys, itertools, numpy as np, manifold3d as mf
from _paths import *; sys.path.insert(0, '.')
import fit_tatakan_gmt130 as F
from components import COMPONENTS as CMP
box = F.box
P = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'placement.json'))
C = F.load(CASE_ORIG)
T = F.load(sys.argv[2] if len(sys.argv) > 2 else STAND_ORIG).translate([0, 0, -10.38])
def lcd_module(zf):
    x = F.PCB_W / 2
    m = box(-x, x, F.PCB_FRONT_Y, F.PCB_BACK_Y, zf, zf + F.PCB_H)
    m = m + box(-F.GLASS_W/2, F.GLASS_W/2, F.FRAME_Y_BACK + 0.02, F.PCB_FRONT_Y, zf + 5, zf + 5 + 29.22)
    m = m + box(-10, 10, F.PCB_BACK_Y, F.PCB_BACK_Y + 2.5, zf + 0.3, zf + 4.8)
    return m
L = lcd_module(F.FLOOR_Z + 0.02).translate([0, 0, -10.38])
B = {k: box(v['lo'][0], v['hi'][0], v['lo'][1], v['hi'][1], v['lo'][2], v['hi'][2]) for k, v in P.items() if v}
SL = 6.0
def gap(a, b):
    v = (a ^ b).volume()
    return (-1.0, round(v, 3)) if v > 1e-6 else (round(a.min_gap(b, SL), 2), 0.0)
out = {}
for k, m in B.items():
    r = {w: gap(m, o) for w, o in (('case', C), ('stand', T), ('lcd', L))}
    others = {k2: gap(m, m2)[0] for k2, m2 in B.items() if k2 != k}
    near = min(others.items(), key=lambda kv: kv[1]) if others else (None, None)
    out[k] = dict(P[k], gap_case=r['case'][0], gap_stand=r['stand'][0], gap_lcd=r['lcd'][0],
                  overlap_mm3=sum(x[1] for x in r.values()), nearest_part=near[0], gap_nearest_part=near[1])
    print(f"{k:26s} case {r['case']} stand {r['stand']} lcd {r['lcd']}  nearest {near}")
# USB-C plug overmold paths (ASSUMED 12.35 x 6.5 mm overmold, 20 mm long)
PW, PH = 12.35, 6.5
def plug(cx, cz, y0): return box(cx - PW/2, cx + PW/2, y0 + 0.05, y0 + 20, cz - PH/2, cz + PH/2)
if P.get('esp32c3_supermini'):
    e = P['esp32c3_supermini']; cx = (e['lo'][0] + e['hi'][0]) / 2; cz = e['lo'][2] + 1.0 + 1.0 + 1.6
    pm = plug(cx, cz, e['hi'][1]); v = (pm ^ C).volume()
    out['esp32c3_supermini']['usb_plug_overlap_case_mm3'] = round(v, 3); out['esp32c3_supermini']['usb_plug_gap_case'] = round(pm.min_gap(C, SL), 2) if v < 1e-6 else -1
    print('ESP32 USB-C plug path through rear port: overlap', round(v, 3), 'gap', out['esp32c3_supermini']['usb_plug_gap_case'], 'centre', round(cx, 2), round(cz, 2))
if P.get('tp4056_typec_dw01'):
    t = P['tp4056_typec_dw01']; cx = (t['lo'][0] + t['hi'][0]) / 2; cz = t['lo'][2] + 0.5 + 1.6 + 1.6
    pm = plug(cx, cz, t['hi'][1]); v = (pm ^ C).volume() + (pm ^ T).volume()
    out['tp4056_typec_dw01']['usb_plug_overlap_mm3'] = round(v, 3); out['tp4056_typec_dw01']['usb_plug_gap'] = round(min(pm.min_gap(C, SL), pm.min_gap(T, SL)), 2) if v < 1e-6 else -1
    print('TP4056 USB-C plug path through bottom slot: overlap', round(v, 3), 'gap', out['tp4056_typec_dw01']['usb_plug_gap'], 'centre', round(cx, 2), round(cz, 2))
json.dump(out, open('placement_verified.json', 'w'), indent=1)
