#!/usr/bin/env python3
"""Variant 6: LiPo on its 16-mm edge ABOVE the ESP32 (off-board, bridging), SD + amp edge-mounted on right-angle
headers in the front strip, 7-pad LCD row moved to the left half of the front edge, cap, speaker under the dome."""
import json, sys
import pcb_common as PC
from pcb_common import *
# move the LCD pad row: rebuild occupancy without the centred pad strip
occ = np.zeros_like(PL.CAV); occ[:, :, k(Z0 - 2.0):k(ZT) + 1] |= inside[:, :, None]
FX = dict(PC.FIXED); FX['lcd_pad_row_7pin'] = ([-19.5, -2.5, ZT], [-1.0, 0.5, ZT + 2.0])
res = {}
for n, (lo, hi) in FX.items():
    occ |= vox_box(np.array(lo) - 0.5, np.array(hi) + 0.5); res[n] = dict(name=n, lo=lo, hi=hi, fixed=True)
def edge_on(l, h, conn, th):
    return th != 2 and ZT - 0.05 <= l[2] <= ZT + 0.6 and POLY.buffer(0.01).contains(sg.box(l[0], l[1], h[0], h[1]))
def onb(l, h, conn, th):
    return ZT - 0.05 <= l[2] <= ZT + 0.6 and POLY.buffer(0.01).contains(sg.box(l[0], l[1], h[0], h[1]))
CAPD = float(sys.argv[1]) if len(sys.argv) > 1 else 6.3
CAPL = (11.5 if CAPD == 8 else 11.0) + 2.5
EE = {'sd': (28.0, 25.6 + HDR, 6.0), 'amp': (19.4, 17.8 + HDR, 4.0)}
def bat_f(l, h, conn, th): return th == 1 and l[1] >= 9.5        # on edge, above/behind the front strip
plan = [
 ('battery_LiPo501640', CMP['battery_LiPo501640']['env'], bat_f, lambda l, h, c_, t: l[2] + 0.1 * l[1] + 0.1 * abs(PL.c(l, h)[0])),
 ('max98357a_edge', EE['amp'], edge_on, lambda l, h, c_, t: l[1] - 0.01 * l[0]),
 ('sd_wemos_edge', EE['sd'], edge_on, lambda l, h, c_, t: l[1] + 0.01 * abs(PL.c(l, h)[0])),
 ('cap_470uF', (CAPL, CAPD + 0.5, CAPD + 0.5), onb, lambda l, h, c_, t: h[2]),
 ('speaker_20mm', CMP['speaker_20mm']['env'], lambda l, h, c_, t: t == 2, lambda l, h, c_, t: -h[2]),
 ('ttp223_red_15x11', CMP['ttp223_red_15x11']['env'], PL.touch_f, PL.touch_s)]
o = occ.copy(); out = dict(res)
for n, env, f, sc in plan:
    r = PL.place(n, env, o, f, sc, False)
    if r is None: print(f'{n:24s} NO FIT'); continue
    p_, m = r; o |= m; out[n] = p_; print(f"{n:24s} lo={p_['lo']} hi={p_['hi']} thick={p_['thickness_axis']}")
json.dump(out, open(f'placement_pcb_v6_cap{CAPD:g}.json', 'w'), indent=1)
