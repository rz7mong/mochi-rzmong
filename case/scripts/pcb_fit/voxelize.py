# Voxelize case + stand (assembled) via manifold slicing -> occupancy grid (npz)
import numpy as np, trimesh, manifold3d as mf, sys
from matplotlib.path import Path
from _paths import *  # repo-relative paths
import fit_tatakan_gmt130 as F
R = float(sys.argv[1]) if len(sys.argv)>1 else 0.5
import os
C = F.load(os.environ.get('CASE',CASE_ORIG))
T = F.load(os.environ.get('STAND',STAND_ORIG)).translate([0,0,-10.38])
x0,y0,z0 = -34.0,-49.0,-30.0
nx,ny,nz = int(68/R),int(98/R),int(60/R)
xs = x0+(np.arange(nx)+0.5)*R; ys = y0+(np.arange(ny)+0.5)*R; zs = z0+(np.arange(nz)+0.5)*R
XX,YY = np.meshgrid(xs,ys,indexing='ij'); pts = np.c_[XX.ravel(),YY.ravel()]
def rast(man):
    g = np.zeros((nx,ny,nz),bool)
    for k,z in enumerate(zs):
        cs = man.slice(z)
        polys = cs.to_polygons()
        if not polys: continue
        acc = np.zeros(len(pts),np.int32)
        for p in polys:
            acc ^= Path(np.asarray(p)).contains_points(pts).astype(np.int32)  # even-odd
        g[:,:,k] = acc.reshape(nx,ny).astype(bool)
    return g
gc = rast(C); gt = rast(T)
# LCD module (GMT130) in its rails, same geometry as ../check_fit.py module(): PCB+glass+2 mm wire/solder zone
from _paths import *  # repo-relative paths
def lcd_module(z_floor):   # copy of ../check_fit.py module() (do not import: that script runs on import)
    x = F.PCB_W / 2; box = F.box
    m = box(-x, x, F.PCB_FRONT_Y, F.PCB_BACK_Y, z_floor, z_floor + F.PCB_H)
    g0 = z_floor + 5.0
    m = m + box(-F.GLASS_W/2, F.GLASS_W/2, F.FRAME_Y_BACK + 0.02, F.PCB_FRONT_Y, g0, g0 + 29.22)
    # ASSUMED: header pin stubs + direct-soldered wires behind pin row: 20 x 4.5 mm, 2.5 mm deep
    m = m + box(-10, 10, F.PCB_BACK_Y, F.PCB_BACK_Y + 2.5, z_floor + 0.3, z_floor + 4.8)
    return m
LZ0 = F.FLOOR_Z + 0.02
gl = rast(lcd_module(LZ0).translate([0,0,-10.38]))
np.savez_compressed(os.environ.get('OUT',f'occ_{R}.npz'), case=gc, stand=gt, lcd=gl, origin=[x0,y0,z0], R=R)
print('done', gc.sum()*R**3, gt.sum()*R**3)
