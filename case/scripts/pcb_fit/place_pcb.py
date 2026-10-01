#!/usr/bin/env python3
"""Layout for the custom carrier-PCB variant (case_luar_lcd_23_40mm_pcb.stl + tatakan_GMT130_fit_pcb.stl).
Carrier: single-sided 1.6 mm FR4, bottom z=-15.2, top z=-13.6, outline pcb_recommended_outline.json, 2 mm joints below
(1.2 mm over the rear pocket). Modules on short headers (2.5 mm spacer, ASSUMED). Off-board: LiPo, speaker, TTP223,
TP4056 (on the stand floor under the PCB, USB-C in the existing rear-bottom slot)."""
import json, sys, numpy as np, shapely.geometry as sg
sys.path.insert(0, '.')
import place as PL
D = np.load('cavity_pcb_0.5.npz'); PL.D = D; PL.CAV = D['cav']
import scipy.ndimage as nd
PL.EDT = nd.distance_transform_edt(~D['case']) * PL.R
from components import COMPONENTS as CMP
OUT = json.load(open('pcb_recommended_outline.json')); POLY = sg.Polygon(OUT['outline'])
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
 'esp32c3_supermini_on_headers': ([-9.0, 10.0, ZT], [9.0, 34.0, ZT + HDR + 4.3]),       # USB-C front at y=34 (pocket back face)
 'switch_rightangle_rear': ([7.5, 30.0, ZT], [16.3, 34.0, ZT + 4.0]),                    # ASSUMED right-angle slide switch body 8.8x4x4, handle +y into slot
 'lcd_pad_row_7pin': ([-9.0, -2.5, ZT], [9.0, 0.5, ZT + 2.0]),                           # 7 pads @2.54 + wire bend
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
    return out, occ
BASEOCC = occ.copy()
print('--- variant 1: Wemos SD shield + amp + cap on the board')
v1, _ = run(['sd_wemos_on_headers', 'max98357a_on_headers', 'cap_470uF_flat'], occ)
print('--- variant 2: amp + cap + Adafruit 4682 SD')
v2, _ = run(['max98357a_on_headers', 'cap_470uF_flat', 'sd_adafruit4682_on_headers'], occ)
print('--- variant 3: amp + cap on board; SD off-board')
v3, occ3 = run(['max98357a_on_headers', 'cap_470uF_flat'], occ)
# off-board parts for variant 3
def grille_f(l, h, conn, th):   # speaker face up under the grille (centre 0,2, R8)
    cc = PL.c(l, h); return th == 2 and abs(cc[0]) <= 2 and abs(cc[1] - 2) <= 2.5
grille_s = lambda l, h, conn, th: -h[2]
off = [('speaker_20mm', CMP['speaker_20mm']['env'], grille_f, grille_s),
       ('battery_LiPo501640', CMP['battery_LiPo501640']['env'], PL.ANY, lambda l, h, c_, t: 0.1 * abs(PL.c(l, h)[0]) + 0.02 * l[2]),
       ('sd_wemos_offboard', CMP['sd_wemos_microsd_shield']['env'], PL.ANY, lambda l, h, c_, t: -0.0 * h[2] + 0.1 * abs(PL.c(l, h)[0])),
       ('ttp223_red_15x11', CMP['ttp223_red_15x11']['env'], PL.touch_f, PL.touch_s)]
occ = occ3.copy(); offres = {}
for n, env, f, s in off:
    r = PL.place(n, env, occ, f, s, False)
    if r is None: offres[n] = None; print(f'{n:28s} NO FIT'); continue
    p, o = r; occ |= o; offres[n] = p; print(f"{n:28s} OFF BOARD lo={p['lo']} hi={p['hi']}")
final = dict(res); final.update({k: v for k, v in v3.items()}); final.update(offres)
json.dump(dict(fixed=res, variant1=v1, variant2=v2, variant3=v3, offboard_v3=offres), open('placement_pcb.json', 'w'), indent=1)
json.dump({k: v for k, v in final.items() if v}, open('placement_pcb_flat.json', 'w'), indent=1)

# ---- variant 4: amp + SD stood on edge on RIGHT-ANGLE headers in the front strip, cap flat; then off-board parts
print('--- variant 4: SD + amp edge-mounted (right-angle headers) in the front strip, cap flat; LiPo/speaker/TTP off-board')
def edge_on(l, h, conn, th):  # module plane vertical, sitting on the board, footprint inside outline
    return th != 2 and ZT - 0.05 <= l[2] <= ZT + 0.6 and POLY.buffer(0.01).contains(sg.box(l[0], l[1], h[0], h[1]))
ENV_E = {'sd_wemos_edge': (28.0, 25.6 + HDR, 5.0 + 1.0),      # 2.5 mm right-angle header below the module edge, 1 mm header body behind
         'max98357a_edge': (19.4, 17.8 + HDR, 3.0 + 1.0)}
import copy
occ4 = BASEOCC.copy(); v4 = {}
for n, env, f, sc in [
    ('sd_wemos_edge', ENV_E['sd_wemos_edge'], edge_on, lambda l, h, c_, t: l[0] + 0.2 * l[1]),
    ('max98357a_edge', ENV_E['max98357a_edge'], edge_on, lambda l, h, c_, t: -h[0] * 0 + l[1] * 0.1 - l[0]),
    ('cap_470uF_flat', ENV['cap_470uF_flat'], onboard, lambda l, h, c_, t: abs(PL.c(l, h)[0]) * -0.05),
    ('battery_LiPo501640', CMP['battery_LiPo501640']['env'], PL.ANY, lambda l, h, c_, t: 0.1 * abs(PL.c(l, h)[0]) + 0.02 * l[2]),
    ('speaker_20mm', CMP['speaker_20mm']['env'], grille_f, grille_s),
    ('ttp223_red_15x11', CMP['ttp223_red_15x11']['env'], PL.touch_f, PL.touch_s)]:
    r = PL.place(n, env, occ4, f, sc, False)
    if r is None: v4[n] = None; print(f'{n:28s} NO FIT'); continue
    p_, o = r; occ4 |= o; v4[n] = p_; print(f"{n:28s} lo={p_['lo']} hi={p_['hi']} thick={p_['thickness_axis']}")
allv4 = dict(res); allv4.update({k: v for k, v in v4.items() if v})
json.dump(allv4, open('placement_pcb_v4.json', 'w'), indent=1)
