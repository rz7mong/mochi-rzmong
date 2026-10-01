import json, numpy as np, shapely.geometry as sg
from _paths import *  # repo-relative paths
from matplotlib.path import Path
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D = np.load('cavity_pcb_0.5.npz'); cav = D['cav']; O = D['origin'].astype(float); R = float(D['R'])
X = O[0] + (np.arange(cav.shape[0]) + .5) * R; Y = O[1] + (np.arange(cav.shape[1]) + .5) * R; Z = O[2] + (np.arange(cav.shape[2]) + .5) * R
OUT = json.load(open(OUTLINE_V2)); poly = np.asarray(OUT['outline'])
ins = Path(poly).contains_points(np.c_[np.repeat(X, len(Y)), np.tile(Y, len(X))]).reshape(len(X), len(Y))
ZT = -13.6; k0 = np.searchsorted(Z, ZT)
H = np.full(ins.shape, np.nan)
for i, j in np.argwhere(ins):
    col = cav[i, j, k0:]
    n = np.argmax(~col) if (~col).any() else len(col)
    H[i, j] = n * R
def zone(x0, x1, y0, y1):
    m = ins & (X[:, None] >= x0) & (X[:, None] <= x1) & (Y[None, :] >= y0) & (Y[None, :] <= y1)
    return np.nanmin(H[m]), np.nanmedian(H[m])
for name, z in [('front strip y-2.5..9.5', (-20, 20, -2.5, 9.5)), ('ESP zone x+-9 y10..26', (-9, 9, 10, 26)),
                ('left wedge x<-9.5 y9.5..21', (-20, -9.5, 9.5, 21)), ('right wedge x>9.5 y9.5..21', (9.5, 20, 9.5, 21)),
                ('rear tab y26.5..33.5', (-11, 10, 26.5, 33.5))]:
    print(f'{name:30s} min {zone(*z)[0]:.1f} median {zone(*z)[1]:.1f} mm above board top')
fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(H.T, origin='lower', extent=[X[0] - R/2, X[-1] + R/2, Y[0] - R/2, Y[-1] + R/2], cmap='viridis', vmin=0, vmax=35)
ax.plot(*np.r_[poly, poly[:1]].T, 'r-'); ax.set_xlim(-24, 24); ax.set_ylim(-6, 37)
for x, y in OUT['holes']: ax.add_patch(plt.Circle((x, y), 1.1, color='w'))
ax.set_title('Free height above carrier top (z -13.6), case+stand PCB variant [mm]\n-y = LCD/face side, +y = rear USB port')
plt.colorbar(im, ax=ax); ax.set_xlabel('x [mm]'); ax.set_ylabel('y [mm]'); plt.tight_layout(); plt.savefig('pcb_headroom_map_v2.png', dpi=130)
