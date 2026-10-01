#!/usr/bin/env python3
"""Variant 7 (final PCB layout candidate):
 - LiPo 501640 off-board, on its 16-mm edge along x, hovering over the front PCB edge (above the LCD pad row)
 - small native-3.3V 6-pin microSD module (18.5 x 20, ASSUMED) and MAX98357A edge-mounted on right-angle headers
   side by side behind the LiPo, thin axis = y
 - 470 uF cap upright (6.3 or 8 mm) in a side wedge, or flat if it fits
 - PUI AS01508MS-SP11-WP-R 15x11x3.5 speaker face-up under the top grille (centre 0,2)
 - TTP223 against the left cheek wall; TP4056 on the stand floor under the PCB (fixed)."""
import json, sys
from pcb_common import *
def edge_y(l, h, conn, th):
    return th == 1 and ZT - 0.05 <= l[2] <= ZT + 0.6 and POLY.buffer(0.01).contains(sg.box(l[0], l[1], h[0], h[1]))
def onb(l, h, conn, th):
    return ZT - 0.05 <= l[2] <= ZT + 0.6 and POLY.buffer(0.01).contains(sg.box(l[0], l[1], h[0], h[1]))
CAPD = float(sys.argv[1]) if len(sys.argv) > 1 else 8
CAPH = (11.5 if CAPD == 8 else 11.0) + 2.5
SDS = (18.5, 20.0 + HDR, 4.0 + 1.0)  # mini 6-pin microSD 18.5x20 (ASSUMED ~4 mm incl. socket) + 1 mm header body
AMP = (17.8, 19.4 + HDR, 4.0)   # 7-pin header runs along the 17.8 mm edge -> 17.8 horizontal, 19.4 + header vertical
SPK = (15.5, 11.5, 4.0)             # PUI AS01508MS-SP11-WP-R 15x11x3.5 (+0.5 tolerance ASSUMED)
def bat_f(l, h, conn, th): return th == 1 and l[1] <= -2.0 and l[2] >= ZT + 2.5
def grille_f(l, h, conn, th):
    cc = PL.c(l, h); return th == 2 and abs(cc[0]) <= 1.5 and abs(cc[1] - 2) <= 1.5
def ttp_f(l, h, conn, th):  # pad face parallel to a case wall: mean gap <=1.2 mm, max <=2.5 mm (curved wall; fill with foam/glue)
    return any(PL.face_gap(l, h, th, sg)[0] <= 2.0 and PL.face_gap(l, h, th, sg)[1] <= 4.0 for sg in (1, -1))
plan = [
 ('battery_LiPo501640', CMP['battery_LiPo501640']['env'], bat_f, lambda l, h, c_, t: l[1] + 0.1 * abs(PL.c(l, h)[0]) + 0.01 * l[2]),
 ('sd_mini6pin_edge', SDS, lambda l, h, c_, t: edge_y(l, h, c_, t) and abs(h[0] - l[0] - SDS[0]) < .01, lambda l, h, c_, t: l[0] + 0.5 * l[1]),
 ('max98357a_edge', AMP, lambda l, h, c_, t: edge_y(l, h, c_, t) and abs(h[0] - l[0] - AMP[0]) < .01, lambda l, h, c_, t: -h[0] + 0.5 * l[1]),
 ('cap_470uF_flat', (CAPH, CAPD + 0.5, CAPD + 0.5), lambda l, h, c_, t: onb(l, h, c_, t) and t == 2 and False or (onb(l, h, c_, t) and (h[2] - l[2]) < CAPD + 0.6), lambda l, h, c_, t: h[2]),
 ('cap_470uF_upright', (CAPD + 0.5, CAPD + 0.5, CAPH), lambda l, h, c_, t: onb(l, h, c_, t) and abs(h[2] - l[2] - CAPH) < .01, lambda l, h, c_, t: abs(PL.c(l, h)[0]) * -0.05),
 ('speaker_15x11', SPK, grille_f, lambda l, h, c_, t: -h[2]),
 ('ttp223_red_15x11', CMP['ttp223_red_15x11']['env'], ttp_f, PL.touch_s)]
o = occ.copy(); out = dict(res)
for n, env, f, sc in plan:
    if n == 'cap_470uF_upright' and 'cap_470uF_flat' in out: continue
    r = PL.place(n, env, o, f, sc, False)
    if r is None: print(f'{n:24s} NO FIT'); continue
    p_, m = r; o |= m; out[n] = p_; print(f"{n:24s} lo={p_['lo']} hi={p_['hi']} thick={p_['thickness_axis']}")
json.dump(out, open(f'placement_pcb_v7_cap{CAPD:g}.json', 'w'), indent=1)
