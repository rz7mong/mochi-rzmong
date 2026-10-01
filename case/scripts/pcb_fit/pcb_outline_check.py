#!/usr/bin/env python3
"""Recommended carrier-PCB outline: containment in the usable mask, exact mesh check (PCB slab + keep-outs vs case/stand),
and the assembly path (PCB lowered into the upside-down case 6.5 mm forward of its final position, then slid +y into the rear pocket)."""
import json, sys, numpy as np, shapely.geometry as sg, manifold3d as mf, os
os.environ['CAV'] = 'cavity_pcb_0.5.npz'
from _paths import *; sys.path.insert(0, '.')
import fit_tatakan_gmt130 as F
import pcb_space as PS
OUTLINE = [(-20.5, -2.5), (20.0, -2.5), (20.0, 10.0), (17.0, 19.0), (11.5, 21.0), (9.5, 26.5), (16.0, 27.5),
           (16.0, 33.5), (-16.5, 33.5), (-16.5, 27.5), (-10.0, 26.5), (-12.0, 21.0), (-17.5, 19.0), (-20.5, 10.0)]
HOLES = [(-14.5, 1.0), (14.5, 1.0), (-14.0, 31.0), (13.0, 31.0)]   # M2 holes
Z0, T, HB, HB_REAR, HT = -15.2, 1.6, 2.0, 1.2, 6.0
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
for name, solid in (('board', board), ('bottom_keepout', keep_bot - holes), ('top_keepout_6mm', keep_top)):
    for wn, w in (('case', C), ('stand', S)):
        v = (solid ^ w).volume(); g = solid.min_gap(w, 5) if v < 1e-6 else -1
        res[f'{name}_vs_{wn}'] = dict(overlap_mm3=round(v, 3), gap=round(g, 2))
        print(f'{name:16s} vs {wn:5s}: overlap {v:.3f} mm3, min gap {g:.2f}')
# assembly path with the ORIGINAL-shape case (no stand yet): vertical drop at dy=-6.5, then slide +y
env = board + keep_bot + keep_top
worst = 0
for dz in np.arange(-30, 0.01, 1.0):
    worst = max(worst, (env.translate([0, -6.5, dz]) ^ C).volume())
slide = max((env.translate([0, -dy, 0]) ^ C).volume() for dy in np.arange(0, 6.51, 0.5))
print('assembly path: max overlap during vertical insertion %.3f mm3, during +y slide %.3f mm3' % (worst, slide))
res['assembly_vertical_overlap_mm3'] = round(worst, 3); res['assembly_slide_overlap_mm3'] = round(slide, 3)
res['outline'] = OUTLINE; res['holes'] = HOLES; res['area_mm2'] = round(P.area, 1); res['bbox'] = P.bounds
json.dump(res, open('pcb_recommended_outline.json', 'w'), indent=1)
PS.write_svg({'recommended_pcb': P, 'usable_free_area': mask_poly if mask_poly.geom_type == 'Polygon' else max(mask_poly.geoms, key=lambda g: g.area)}, 'pcb_recommended_outline.svg')
PS.write_dxf({'PCB_OUTLINE': P, 'USABLE_AREA': mask_poly if mask_poly.geom_type == 'Polygon' else max(mask_poly.geoms, key=lambda g: g.area)}
             | {f'HOLE_{i}': sg.Point(x, y).buffer(1.1, 8) for i, (x, y) in enumerate(HOLES)}, 'pcb_recommended_outline.dxf')
