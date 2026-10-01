#!/usr/bin/env python3
"""Recommended carrier-PCB outline: containment in the usable mask, exact mesh check (PCB slab + keep-outs vs case/stand),
and the assembly path (PCB lowered into the upside-down case 6.5 mm forward of its final position, then slid +y into the rear pocket)."""
import json, sys, numpy as np, shapely.geometry as sg, manifold3d as mf, os
os.environ['CAV'] = 'cavity_pcb_0.5.npz'
from _paths import *; sys.path.insert(0, '.')
import fit_tatakan_gmt130 as F
import pcb_space as PS
# v2: assembly-feasible outline (pcb_assembly_region.py, b = 8): rises from below 8 mm forward, then slides +8 mm in y
OUTLINE = [(-19.5, -2.5), (19.0, -2.5), (19.0, 10.5), (17.5, 18.5), (16.5, 19.5), (12.0, 20.5), (10.5, 24.5), (9.5, 25.5),
           (9.5, 33.0), (8.0, 33.5), (-8.5, 33.5), (-10.0, 33.0), (-10.5, 32.5), (-10.5, 26.5), (-11.5, 21.5), (-12.5, 20.5),
           (-17.0, 19.5), (-18.5, 17.0), (-19.5, 11.5)]
HOLES = [(-14.5, 0.5), (14.5, 0.5)]   # M2 clearance 2.2 mm; screws from under the stand into nuts/standoffs on the PCB top
BOFF = 8.0
Z0, T, HB, HB_REAR, HT = -15.2, 1.6, 2.0, 1.2, 5.5
P = sg.Polygon(OUTLINE)
m, _ = PS.usable(Z0, hb=HB, ht=HT, hb_rear=HB_REAR)
for hx, hy in HOLES:        # supports are intended contact points
    pass
mask_poly = PS.poly(m).buffer(3.2)  .buffer(-3.2)     # close the support-post rings
print('outline area %.0f mm2, bbox %s, inside usable mask: %s (outside area %.2f mm2)' % (
    P.area, np.round(P.bounds, 1).tolist(), P.within(mask_poly.buffer(0.01)), P.difference(mask_poly).area))
# exact mesh check
def ext(poly, z0, z1):
    cs = mf.CrossSection([list(poly.exterior.coords)[:-1]])
    return mf.Manifold.extrude(cs, z1 - z0).translate([0, 0, z0])
C = F.load(CASE_PCB); C0 = F.load(CASE_ORIG)
S = F.load(STAND_PCB).translate([0, 0, -10.38])
holes = mf.Manifold.batch_boolean([mf.Manifold.cylinder(40, 2.8, 2.8, 24).translate([x, y, -30]) for x, y in HOLES], mf.OpType.Add)
board = ext(P, Z0, Z0 + T)
front = P.intersection(sg.box(-30, -10, 30, 26.0)); rear = P.intersection(sg.box(-30, 26.0, 30, 40))
keep_bot = ext(front, Z0 - HB, Z0) + ext(rear, Z0 - HB_REAR, Z0)
keep_top = ext(P, Z0 + T, Z0 + T + HT)
res = {}
strip = mf.Manifold.cube([5.0, 11.5, 3.0]).translate([-2.5, 22.0, -17.5])
for name, solid in (('board', board), ('bottom_keepout', keep_bot - holes - strip), ('top_keepout_5.5mm', keep_top)):
    for wn, w in (('case', C), ('stand', S)):
        v = (solid ^ w).volume(); g = solid.min_gap(w, 5) if v < 1e-6 else -1
        res[f'{name}_vs_{wn}'] = dict(overlap_mm3=round(v, 3), gap=round(g, 2))
        print(f'{name:16s} vs {wn:5s}: overlap {v:.3f} mm3, min gap {g:.2f}')
# assembly path with the ORIGINAL-shape case (no stand yet): vertical drop at dy=-6.5, then slide +y
env = board + keep_bot + keep_top
env = board + keep_bot          # top keep-out is checked with the real modules in assembly_sweep_v7.py
rest = mf.Manifold.cylinder(3, 2.0, 2.0, 24).translate([0, 30.5, -17.3])
C_norest = C - rest             # the rest pad sits in a joint-free strip x+-2.5, y 22..33.5 (no solder joints there)
worst = 0
for dz in np.arange(-30, 0.01, 0.5):
    worst = max(worst, (env.translate([0, -BOFF, dz]) ^ C_norest).volume())
slide = max((env.translate([0, -dy, 0]) ^ C_norest).volume() for dy in np.arange(0, BOFF + 0.01, 0.25))
print('assembly path: max overlap during vertical insertion %.3f mm3, during +y slide %.3f mm3' % (worst, slide))
res['assembly_vertical_overlap_mm3'] = round(worst, 3); res['assembly_slide_overlap_mm3'] = round(slide, 3)
res['outline'] = OUTLINE; res['holes'] = HOLES; res['area_mm2'] = round(P.area, 1); res['bbox'] = P.bounds
json.dump(res, open(OUTLINE_V2, 'w'), indent=1)
PS.write_svg({'recommended_pcb': P, 'usable_free_area': mask_poly if mask_poly.geom_type == 'Polygon' else max(mask_poly.geoms, key=lambda g: g.area)}, 'pcb_recommended_outline_v2.svg')
PS.write_dxf({'PCB_OUTLINE': P, 'USABLE_AREA': mask_poly if mask_poly.geom_type == 'Polygon' else max(mask_poly.geoms, key=lambda g: g.area)}
             | {f'HOLE_{i}': sg.Point(x, y).buffer(1.1, 8) for i, (x, y) in enumerate(HOLES)}, 'pcb_recommended_outline_v2.dxf')
