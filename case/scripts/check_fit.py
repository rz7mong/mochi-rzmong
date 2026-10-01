import os, sys, numpy as np, trimesh, manifold3d as mf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fit_tatakan_gmt130 as F
box, load = F.box, F.load
DZ = -10.38   # tatakan -> case assembled offset
def module(z_floor, sweep=0.0, back_parts=True):
    x = F.PCB_W / 2
    pcb = box(-x, x, F.PCB_FRONT_Y, F.PCB_BACK_Y, z_floor, z_floor + F.PCB_H + sweep)
    g0 = z_floor + 5.0
    glass = box(-F.GLASS_W/2, F.GLASS_W/2, F.FRAME_Y_BACK + 0.02, F.PCB_FRONT_Y, g0, g0 + 29.22 + sweep)
    m = pcb + glass
    if back_parts:  # ASSUMED: solder joints / wires behind pin row: 17x4 mm, 2 mm deep
        m = m + box(-8.5, 8.5, F.PCB_BACK_Y, F.PCB_BACK_Y + 2.0, z_floor + 0.5, z_floor + 4.5 + sweep)
    return m
z0 = F.FLOOR_Z + 0.02
T = load(os.path.join(F.CASE_DIR, 'tatakan_GMT130_fit.stl'))
T0 = load(F.SRC)
C = load(os.path.join(F.CASE_DIR, 'case_luar_lcd_23_40mm.stl'))
M = module(z0)
print('module vs NEW tatakan overlap mm3:', round((M ^ T).volume(), 3))
print('module insertion sweep (from top) vs NEW tatakan:', round((module(z0, 40) ^ T).volume(), 3))
print('module vs case (assembled):', round((M.translate([0, 0, DZ]) ^ C).volume(), 3))
print('NEW tatakan vs case (assembled):', round((T.translate([0, 0, DZ]) ^ C).volume(), 3),
      ' ORIGINAL tatakan vs case:', round((T0.translate([0, 0, DZ]) ^ C).volume(), 3))
# lateral play of module in NEW tatakan
for dx in [0.1, 0.2, 0.3, 0.5]:
    print(f'  module shifted x+{dx}: overlap', round((M.translate([dx, 0, 0]) ^ T).volume(), 3))
for dx in [1.0, 2.0, 2.5]:
    print(f'  module shifted x+{dx} in ORIGINAL tatakan (pins-down, on base top): overlap',
          round((module(z0, back_parts=False).translate([dx, 0, 0]) ^ T0).volume(), 3))
