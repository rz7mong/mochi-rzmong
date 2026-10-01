#!/usr/bin/env python3
"""Variant 5 search: SD + amp edge-mounted on right-angle headers, cap upright or flat, LiPo/speaker/TTP off-board."""
import json, itertools
from pcb_common import *
def edge_on(l, h, conn, th):
    return th != 2 and ZT - 0.05 <= l[2] <= ZT + 0.6 and POLY.buffer(0.01).contains(sg.box(l[0], l[1], h[0], h[1]))
def up_on(l, h, conn, th):   # upright radial cap: axis z, footprint inside outline
    return abs((h[2]-l[2]) - CAPH) < 0.01 and ZT - 0.05 <= l[2] <= ZT + 0.6 and POLY.buffer(0.01).contains(sg.box(l[0], l[1], h[0], h[1]))
def spk_any(l, h, conn, th): return th == 2
def bat_any(l, h, conn, th): return True
EE = {'sd': (28.0, 25.6 + HDR, 6.0), 'amp': (19.4, 17.8 + HDR, 4.0)}
import sys
CAPD = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
CAPH = (11.5 if CAPD == 8 else 11.0) + 2.0   # body + 2 mm lead standoff
plan = [
 ('sd_wemos_edge', EE['sd'], edge_on, lambda l, h, c_, t: l[0] + 0.2 * l[1]),
 ('max98357a_edge', EE['amp'], edge_on, lambda l, h, c_, t: l[1] * 0.1 - l[0]),
 ('cap_470uF_upright', (CAPD + 0.5, CAPD + 0.5, CAPH), up_on, lambda l, h, c_, t: abs(PL.c(l, h)[0]) * -0.05),
 ('speaker_20mm', CMP['speaker_20mm']['env'], spk_any, lambda l, h, c_, t: -h[2] + 0.05 * abs(PL.c(l, h)[0])),
 ('battery_LiPo501640', CMP['battery_LiPo501640']['env'], bat_any, lambda l, h, c_, t: 0.1 * abs(PL.c(l, h)[0]) + 0.02 * l[2]),
 ('ttp223_red_15x11', CMP['ttp223_red_15x11']['env'], PL.touch_f, PL.touch_s)]
o = occ.copy(); out = dict(res)
for n, env, f, sc in plan:
    r = PL.place(n, env, o, f, sc, False)
    if r is None: print(f'{n:24s} NO FIT'); continue
    p_, m = r; o |= m; out[n] = p_; print(f"{n:24s} lo={p_['lo']} hi={p_['hi']} thick={p_['thickness_axis']}")
json.dump(out, open(f'placement_pcb_v5_cap{CAPD:g}.json', 'w'), indent=1)
