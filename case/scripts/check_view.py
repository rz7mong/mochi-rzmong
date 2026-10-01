# How much of the LCD active area is hidden by the case (visor/chin) in front of it?
import os, numpy as np, trimesh, shapely.affinity as A
from shapely.geometry import box as sbox
from shapely.ops import unary_union
CASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
C = trimesh.load(os.path.join(CASE_DIR, 'case_luar_lcd_23_40mm.stl'))
DZ = -10.38
Y_SCREEN = -9.19            # glass front surface (case coords, y unchanged)
def occl(aa, angle_deg):
    t = np.tan(np.radians(angle_deg))   # +: viewer above (looking down)
    polys = []
    for y in np.arange(-23.5, Y_SCREEN - 0.2, 0.2):
        s = C.section(plane_origin=[0, y, 0], plane_normal=[0, 1, 0])
        if s is None: continue
        T = np.zeros((4, 4)); T[0, 0] = 1; T[1, 2] = 1; T[2, 1] = 1; T[3, 3] = 1
        p, _ = s.to_2D(to_2D=T)
        for g in p.polygons_full:
            # project the occluder onto the screen plane along the view direction
            polys.append(A.translate(g.buffer(0), 0, -(Y_SCREEN - y) * t))
    occ = unary_union(polys)
    return occ.intersection(aa).area / aa.area * 100
for name, zaa in [('NEW  (pins-down, 0.6 mm floor)', (-17.09 + 6.33 + DZ, -17.09 + 6.33 + 23.4 + DZ)),
                  ('ORIG window region (-11.66..11.29)', (-11.66 + DZ, 11.29 + DZ)),
                  ('ORIG design, module through slot to desk', (-17.69 + 6.33 + DZ, -17.69 + 6.33 + 23.4 + DZ))]:
    aa = sbox(-11.7, zaa[0], 11.7, zaa[1])
    print(name, 'AA case z %.2f..%.2f' % zaa, ' hidden %: ' + ', '.join(f'{a:+d}deg={occl(aa, a):.1f}' for a in (0, 10, 20, 30, -10)))
