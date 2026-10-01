#!/usr/bin/env python3
"""LiPo 501640 (42 x 5.5 x 16.5 envelope, on edge) insertion BEFORE the carrier, stand/LCD not fitted:
1) enters the bottom opening yawed in plan, 2) straightened once inside, parked where the LCD will go (y-6.5),
3) after the carrier is slid home, pushed +6.5 mm in y to its final place in front of the SD/amp modules."""
import json, sys, numpy as np, manifold3d as mf
from _paths import *  # repo-relative paths
import fit_tatakan_gmt130 as F
box = F.box
C = F.load(CASE_PCB)
P = json.load(open('placement_pcb_v7_cap6.3.json'))
b = P['battery_LiPo501640']; lo, hi = np.array(b['lo']), np.array(b['hi']); c = (lo + hi) / 2; d = hi - lo
for k in ('speaker_15x11', 'ttp223_red_15x11', 'switch_rightangle_offboard'):
    v = P[k]; C = C + box(v['lo'][0], v['hi'][0], v['lo'][1], v['hi'][1], v['lo'][2], v['hi'][2])
def bat(yaw, cx, cy, zc):
    return mf.Manifold.cube(list(d), True).rotate([0, 0, yaw]).translate([cx, cy, zc])
PARK = -6.5
# straight battery: parked at y-6.5 at the final z, and the +6.5 slide
park = bat(0, c[0], c[1] + PARK, c[2]); print('park overlap %.3f gap %.2f' % ((park ^ C).volume(), park.min_gap(C, 5)))
print('slide max overlap %.3f' % max((bat(0, c[0], c[1] + dy, c[2]) ^ C).volume() for dy in np.arange(PARK, 0.01, 0.25)))
# vertical lift of the straight battery at y-6.5: lowest z it can be straight
zs = np.arange(c[2] - 25, c[2] + 0.01, 0.25)
ov = [(bat(0, c[0], c[1] + PARK, z) ^ C).volume() for z in zs]
bad = [z for z, o in zip(zs, ov) if o > 1e-3]
print('straight lift blocked at zc <=', max(bad) if bad else None, '(final zc %.2f, bottom of battery = zc-8.25)' % c[2])
# yawed entry below that height
for yaw in (20, 25, 30, 35, 40):
    worst = 0
    for z in np.arange(c[2] - 25, (max(bad) if bad else c[2]) + 0.6, 0.25):
        worst = max(worst, (bat(yaw, c[0], c[1] + PARK, z) ^ C).volume())
    # can it be straightened at the first straight-ok height? check intermediate yaws
    zst = (max(bad) + 0.5) if bad else c[2]
    rot = max((bat(a, c[0], c[1] + PARK, zst) ^ C).volume() for a in np.arange(0, yaw + 0.1, 2.5))
    print(f'yaw {yaw}: entry overlap {worst:.3f}; straighten at zc {zst:.2f}: {rot:.3f}')
print('--- yaw entry at various y, straighten, then move straight to the park position')
import itertools
def ok(m): return (m ^ C).volume() < 1e-3
found = []
for ye, yaw in itertools.product((0.0, 4.0, 8.0, 12.0), (25, 30, 35)):
    yc = ye
    for zs in np.arange(-20.0, -1.9, 2.0):
        if not all(ok(bat(yaw, c[0], yc, z)) for z in np.arange(zs - 25, zs + 0.01, 1.0)): continue
        if not all(ok(bat(a, c[0], yc, zs)) for a in np.arange(0, yaw + 0.1, 2.5)): continue
        # straight move to park (y = c1-6.5, z = c2): along a line
        tgt = np.array([c[1] + PARK, c[2]]); st = np.array([yc, zs])
        if all(ok(bat(0, c[0], *(st + t * (tgt - st)))) for t in np.linspace(0, 1, 25)):
            found.append((ye, yaw, zs)); print(f'OK: enter at y {ye} yawed {yaw} deg, straighten at zc {zs}, move to park'); break
    if found and found[-1][:2] == (ye, yaw): continue
print('paths found:', len(found))
