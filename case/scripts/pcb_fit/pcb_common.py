#!/usr/bin/env python3
"""Layout for the custom carrier-PCB variant (case_luar_lcd_23_40mm_pcb.stl + tatakan_GMT130_fit_pcb.stl).
Carrier: single-sided 1.6 mm FR4, bottom z=-15.2, top z=-13.6, outline pcb_recommended_outline.json, 2 mm joints below
(1.2 mm over the rear pocket). Modules on short headers (2.5 mm spacer, ASSUMED). Off-board: LiPo, speaker, TTP223,
TP4056 (on the stand floor under the PCB, USB-C in the existing rear-bottom slot)."""
import json, sys, numpy as np, shapely.geometry as sg
from _paths import *  # repo-relative paths
sys.path.insert(0, '.')
import place as PL
D = np.load('cavity_pcb_0.5.npz'); PL.D = D; PL.CAV = D['cav']
import scipy.ndimage as nd
PL.EDT = nd.distance_transform_edt(~D['case']) * PL.R
from components import COMPONENTS as CMP
OUT = json.load(open(OUTLINE_V2)); POLY = sg.Polygon(OUT['outline'])
Z0, T = -15.2, 1.6; ZT = Z0 + T; HDR = 2.5
def vox_box(lo, hi):
    m = np.zeros_like(PL.CAV); a, b = PL.box_idx(lo, hi); m[a[0]:b[0], a[1]:b[1], a[2]:b[2]] = True; return m
# PCB slab + bottom keep-out as occupied (rasterised outline)
X = PL.O[0] + (np.arange(PL.CAV.shape[0]) + .5) * PL.R; Y = PL.O[1] + (np.arange(PL.CAV.shape[1]) + .5) * PL.R
from matplotlib.path import Path
inside = Path(np.asarray(OUT['outline'])).contains_points(np.c_[np.repeat(X, len(Y)), np.tile(Y, len(X))]).reshape(len(X), len(Y))
occ = np.zeros_like(PL.CAV)
k = lambda z: int(np.floor((z - PL.O[2]) / PL.R + 1e-6))
occ[:, :, k(Z0 - 2.0):k(ZT) + 1] |= inside[:, :, None]
FIXED = {   # fixed by openings (lo, hi)
 'esp32c3_supermini_on_headers': ([-9.0, 10.0, ZT], [9.0, 32.5, ZT + HDR + 1.0 + 2.0]),   # header 2.5 + PCB 1.0 + parts <=2.0 (ASSUMED)
 'esp32c3_usbc_receptacle': ([-4.5, 26.6, ZT + HDR + 1.0], [4.5, 34.0, ZT + HDR + 1.0 + 3.2]),  # 8.94x7.35x3.16 receptacle, front at y=34
 'switch_rightangle_offboard': ([7.2, 29.0, -7.9], [15.8, 33.7, -4.2]),   # SK-12D07 class 8.6x4.7 body, 3.7 tall ASSUMED; glued in the pocket above the ESP edge, wired
 'switch_handle': ([10.5, 33.7, -6.8], [12.5, 37.3, -5.3]),             # handle 2x1.5x3.6 ASSUMED, into the rear-wall slot
 'lcd_pad_row_7pin': ([-9.0, -2.5, ZT], [9.0, 0.5, ZT + 2.0]),
 'm2_nut_L': ([-16.8, -1.8, ZT], [-12.2, 2.8, ZT + 1.6]),
 'm2_nut_R': ([12.2, -1.8, ZT], [16.8, 2.8, ZT + 1.6]),                           # 7 pads @2.54 + wire bend
 'tp4056_on_floor': ([-8.5, -3.0, -26.73], [8.8, 25.0, -26.73 + 5.4]),                  # from the loose-module run, USB-C in the bottom slot
}
res = {}
for n, (lo, hi) in FIXED.items():
    occ |= vox_box(np.array(lo) - 0.5, np.array(hi) + 0.5); res[n] = dict(name=n, lo=lo, hi=hi, fixed=True)
BASEOCC = None
def onboard(l, h, conn, th):
    return th == 2 and ZT - 0.05 <= l[2] <= ZT + 0.6 and POLY.buffer(0.01).contains(sg.box(l[0], l[1], h[0], h[1]))
ENV = {
 'sd_wemos_on_headers': (28.0, 25.6, HDR + 3.0),
 'sd_adafruit4682_on_headers': (25.4, 22.8, HDR + 3.5),
 'max98357a_on_headers': (19.4, 17.8, HDR + 3.0),
 'cap_470uF_flat': (11.5 + 2.5, 8.0, 8.0 + 0.5),
}
def run(names, occ0):
    occ = occ0.copy(); out = {}
    for n in names:
        sc = lambda l, h, conn, th: abs(PL.c(l, h)[0]) * 0.05 + (h[1]) * 0.05
        r = PL.place(n, ENV[n], occ, onboard, sc, False)
        if r is None: out[n] = None; print(f'{n:28s} does NOT fit on the board'); continue
        p, o = r; occ |= o; out[n] = p; print(f"{n:28s} ON BOARD lo={p['lo']} hi={p['hi']}")
