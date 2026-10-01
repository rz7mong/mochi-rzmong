"""Last step: stand (PCB variant) + LCD in its rails + TP4056 on its floor rise vertically into the case that already holds
the carrier, LiPo, switch, speaker, TTP223."""
import json, sys, numpy as np, manifold3d as mf
from _paths import *  # repo-relative paths
sys.argv = ['x', 'placement_pcb_v7_cap6.3.json']
exec(open('verify_pcb.py').read().split("SL = 6.0")[0])
tp = P['tp4056_on_floor']
MOVE = T + L + box(tp['lo'][0], tp['hi'][0], tp['lo'][1], tp['hi'][1], tp['lo'][2] + 0.05, tp['hi'][2])
STAT = C + PCB
for k, v in P.items():
    if k in ('tp4056_on_floor',): continue
    STAT = STAT + box(v['lo'][0], v['hi'][0], v['lo'][1], v['hi'][1], v['lo'][2], v['hi'][2])
w = [((MOVE.translate([0, 0, dz]) ^ STAT).volume(), dz) for dz in np.arange(-40, 0.01, 0.5)]
print('max overlap during stand insertion %.3f mm3 at dz %.1f' % max(w))
print('final: stand+LCD+TP vs everything %.3f mm3' % (MOVE ^ STAT).volume())
print('stand^case', round((T ^ C).volume(), 3), 'stand^pcb', round((T ^ PCB).volume(), 3), 'lcd^case', round((L ^ C).volume(), 3))
T0 = F.load(STAND_ORIG).translate([0, 0, -10.38]); C0 = F.load(CASE_ORIG)
print('ORIGINAL stand^original case', round((T0 ^ C0).volume(), 3))
I = T ^ C; print('bbox', np.round(I.bounding_box(), 2) if I.volume() > 0 else '')
