#!/usr/bin/env python3
"""2D assembly-feasibility map for the carrier: board must (1) rise vertically from below the case at y-offset -b
without hitting case solid (stand not yet fitted), then (2) slide +b in y at its final height (z -17.2/-16.4..-13.6).
Intersected with the previously verified final-position outline. Prints usable area per b."""
import json, numpy as np, shapely.geometry as sg, shapely.ops as so
from matplotlib.path import Path
D = np.load('cavity_pcb_0.5.npz'); cs = D['case']; O = D['origin'].astype(float); R = float(D['R'])
z = O[2] + (np.arange(cs.shape[2]) + .5) * R
X = O[0] + (np.arange(cs.shape[0]) + .5) * R; Y = O[1] + (np.arange(cs.shape[1]) + .5) * R
lift_free = ~cs[:, :, (z > -28.5) & (z < -13.6)].any(2)
slab_hi = ~cs[:, :, (z > -17.2) & (z < -13.6)].any(2)
slab_lo = ~cs[:, :, (z > -16.4) & (z < -13.6)].any(2)
slab = np.where(Y[None, :] > 26.0, slab_lo, slab_hi)
# erode by 0.5 mm clearance
import scipy.ndimage as nd
lift_free = nd.binary_erosion(lift_free, iterations=1); slab = nd.binary_erosion(slab, iterations=1)
OUT = json.load(open('pcb_recommended_outline.json')); P0 = sg.Polygon(OUT['outline'])
inside0 = Path(np.asarray(OUT['outline'])).contains_points(np.c_[np.repeat(X, len(Y)), np.tile(Y, len(X))]).reshape(len(X), len(Y))
best = None; ALL = []
for b in np.arange(0, 16.01, 0.5):
    nb = int(round(b / R))
    ok = inside0.copy()
    # (1) lift: point (x, y) at y-b must be lift-free
    sh = np.zeros_like(ok); sh[:, nb:] = lift_free[:, :len(Y) - nb] if nb else lift_free
    ok &= sh
    # (2) slide: every y' in [y-b, y] must be slab-free -> min filter along y
    if nb:
        run = np.ones_like(ok)
        for d in range(nb + 1):
            s2 = np.zeros_like(ok); s2[:, d:] = slab[:, :len(Y) - d]; run &= s2
        ok &= run
    else: ok &= slab
    # keep the component connected to the ESP area and require the ESP footprint (x+-9, y 10..27) to be fully usable
    lab, n = nd.label(ok); i0 = np.argmin(abs(X)); j0 = np.argmin(abs(Y - 15)); keep = lab == lab[i0, j0] if lab[i0, j0] else np.zeros_like(ok)
    espm = (abs(X)[:, None] <= 9) & (Y[None, :] >= 10) & (Y[None, :] <= 27)
    esp_ok = (keep | ~espm | ~inside0).all() and (keep & espm).sum() > 0
    area = keep.sum() * R * R; ymax = Y[keep.any(0)].max() if keep.any() else None
    print(f'b={b:4.1f} area {area:6.0f} mm2  ESP-strip ok {esp_ok}  max y {ymax}')
    ALL.append((b, area, keep))
    if esp_ok and (best is None or area > best[1]): best = (b, area, keep)
import sys
BSEL = float(sys.argv[1]) if len(sys.argv) > 1 else None
if BSEL is not None: best = [bb for bb in ALL if abs(bb[0] - BSEL) < 1e-6][0]
b, area, keep = best
print('BEST b', b, 'area', area)
np.savez('pcb_assembly_region.npz', keep=keep, X=X, Y=Y, b=b)
# polygonize the kept region
from shapely.geometry import box as sbox
cells = [sbox(X[i] - R/2, Y[j] - R/2, X[i] + R/2, Y[j] + R/2) for i, j in np.argwhere(keep)]
U = so.unary_union(cells).buffer(0)
if U.geom_type != 'Polygon': U = max(U.geoms, key=lambda g: g.area)
U = sg.Polygon(U.exterior).simplify(0.35, preserve_topology=True)
print('region poly area', round(U.area, 1), 'bounds', np.round(U.bounds, 2))
print([tuple(np.round(c, 2)) for c in U.exterior.coords])
json.dump(dict(b=b, poly=[list(map(float, c)) for c in U.exterior.coords]), open('pcb_assembly_region.json', 'w'))
