#!/usr/bin/env python3
"""
Modify rz7mong/mochi-rzmong case/tatakan_lcd_23_40mm.stl so it fits the real LCD module
used in the repo: GMT130-V1.0 / "1.3inch IPS Module" (ST7789, 240x240).

Module dimensions (source: lcdwiki MSP1308 size drawing 1.3inch_IPS_Size.jpg + TFT1301 spec):
  PCB 27.78 x 39.22 mm, mounting holes D2.0 at 2.5 mm from each edge (pitch 22.78 x 34.22)
  Glass panel 26.16 x 29.22 x 1.5(max) mm, glass starts 5.00 mm from each short PCB edge
  Active area 23.40 x 23.40 mm; AA starts 1.33 mm below glass edge on the PIN side,
  4.49 mm from glass edge on the opposite side, 1.38 mm from glass left/right edges.
  => AA edge is 5.00+1.33 = 6.33 mm from the PIN edge of the PCB, horizontally centred.
ASSUMED: PCB thickness 1.6 mm (typical, not on the drawing).

Coordinates = original tatakan STL coordinates (mm). Front = -Y (the side facing the case window).
Assembled pose in case_luar_lcd_23_40mm.stl coordinates: translate(0, 0, -10.38) (found by
collision search; the tatakan's locking lips sit in the two floor slots of the case).

Module orientation: PINS DOWN (pin header edge on the floor of the pocket, as the original
window position implies). Firmware >= 0.5.4 defaults to rotation 2 (180 deg) for this mounting.

Usage (from the repo root):  python case/scripts/fit_tatakan_gmt130.py [SRC.stl] [OUT.stl]
Requires: pip install numpy trimesh manifold3d   (check_view.py also needs shapely)
"""
import os, sys, numpy as np, trimesh, manifold3d as mf

CASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))   # repo/case

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CASE_DIR, 'tatakan_lcd_23_40mm.stl')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(CASE_DIR, 'tatakan_GMT130_fit.stl')

# ---------------- parameters ----------------
PCB_W, PCB_H, PCB_T = 27.78, 39.22, 1.6          # PCB_T assumed
GLASS_W, GLASS_T = 26.16, 1.5
AA = 23.40
AA_FROM_PIN_EDGE = 6.33
WIN_TOL = 0.10            # visible window = AA + 2*WIN_TOL  (23.6 mm)
WIN_CHAMFER = 1.2         # front side of window opens by this much per side (45-ish deg bevel)
POCKET_CLR = 0.20         # clearance per side PCB edge -> rail (pocket width 28.18)
# measured on the original tatakan (mm):
FRAME_Y_FRONT, FRAME_Y_BACK = -10.92, -9.19   # front frame plate
OLD_WIN = dict(x0=-16.65, x1=16.25, z0=-11.66, z1=11.29)  # old window (32.9 x 22.95)
BASE_TOP, BASE_BOT = -16.35, -17.69
SLOT = dict(x0=-14.01, x1=14.02, y0=-9.21, y1=-4.99)       # old slot through base plate
WALL_IN_X = (-16.63, 16.23)                                # inner faces of pocket side walls
BACKBOX_FRONT = (-5.05, -2.80)                             # y-range of back box front wall (to z=-3.21)
# derived
FLOOR_T = 0.6                                               # floor printed into the old base slot
FLOOR_Z = BASE_BOT + FLOOR_T                                # -17.09: module pin edge rests here
# (chosen by a view-occlusion check: AA fully visible head-on and up to ~10 deg from above;
#  higher floor = more of the top of the screen hidden by the visor when looking down)
AA_Z0 = FLOOR_Z + AA_FROM_PIN_EDGE
AA_Z1 = AA_Z0 + AA
WIN = AA + 2 * WIN_TOL
PCB_FRONT_Y = FRAME_Y_BACK + GLASS_T                        # -7.69
PCB_BACK_Y = PCB_FRONT_Y + PCB_T                            # -6.09

def box(x0, x1, y0, y1, z0, z1):
    return mf.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])

def load(p):
    m = trimesh.load(p)
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                               tri_verts=np.asarray(m.faces, np.uint32)))

def save(man, p):
    m = man.to_mesh()
    t = trimesh.Trimesh(m.vert_properties[:, :3], m.tri_verts, process=True)
    t.export(p)
    return t

def build(src=SRC):
    T = load(src)
    # 1) close the old 32.9 x 22.95 window
    T = T + box(OLD_WIN['x0'] - 0.05, OLD_WIN['x1'] + 0.05, FRAME_Y_FRONT, FRAME_Y_BACK,
                OLD_WIN['z0'] - 0.05, OLD_WIN['z1'] + 0.05)
    # 2) close the old slot in the base plate -> defined floor for the module
    T = T + box(SLOT['x0'] - 0.05, SLOT['x1'] + 0.05, SLOT['y0'] - 0.05, SLOT['y1'] + 0.05, BASE_BOT, FLOOR_Z)
    # 3) side rails with a PCB channel (locate the 27.78 mm PCB; old pocket was 32.86 mm wide)
    xr_in = PCB_W / 2 + POCKET_CLR                 # 14.09 channel bottom
    rail_z1 = 11.2                                 # up to the top ring of the frame
    for s in (1, -1):
        xw = WALL_IN_X[1] if s > 0 else -WALL_IN_X[0]
        xg = GLASS_W / 2 + 0.35                    # keep clear of glass edge (13.43)
        x_block0 = xr_in - 0.9                     # rail lips reach 0.9 mm over the PCB edge
        front = box(xg, xw + 0.3, FRAME_Y_BACK - 0.05, PCB_FRONT_Y - 0.15, FLOOR_Z, rail_z1)
        back = box(x_block0, xw + 0.3, PCB_BACK_Y + 0.30, PCB_BACK_Y + 1.6, FLOOR_Z, rail_z1)
        web = box(xr_in, xw + 0.3, FRAME_Y_BACK - 0.05, PCB_BACK_Y + 1.6, FLOOR_Z, rail_z1)
        r = front + back + web
        if s < 0:
            r = r.mirror([1, 0, 0])
        T = T + r
    # lead-in chamfer at the top of the channel is skipped (keep simple); sand if tight.
    # 4) wire / solder-joint clearance behind the pin row (pins are at the bottom, 2.5 mm above floor)
    T = T - box(-10.0, 10.0, BACKBOX_FRONT[0] - 0.3, BACKBOX_FRONT[1] + 0.05, FLOOR_Z, 0.0)  # leaves FLOOR_T of base under the notch
    # 5) new window = AA + tolerance, bevelled towards the front
    zc = (AA_Z0 + AA_Z1) / 2
    back_face = box(-WIN / 2, WIN / 2, FRAME_Y_BACK - 0.6, FRAME_Y_BACK + 0.3, zc - WIN / 2, zc + WIN / 2)
    w2 = WIN / 2 + WIN_CHAMFER
    front_face = box(-w2, w2, FRAME_Y_FRONT - 0.3, FRAME_Y_FRONT - 0.2, zc - w2, zc + w2)
    T = T - mf.Manifold.batch_hull([back_face, front_face])
    return T

if __name__ == '__main__':
    T = build()
    t = save(T, OUT)
    print('saved', OUT, 'watertight', t.is_watertight, 'extents', np.round(t.extents, 2))
    print(f'window {WIN:.2f} x {WIN:.2f} mm, x {-WIN/2:.2f}..{WIN/2:.2f}, '
          f'z {(AA_Z0+AA_Z1)/2-WIN/2:.2f}..{(AA_Z0+AA_Z1)/2+WIN/2:.2f} (tatakan coords); '
          f'AA z {AA_Z0:.2f}..{AA_Z1:.2f}')
    print(f'pocket width between rails {2*(PCB_W/2+POCKET_CLR):.2f} mm; PCB channel y '
          f'{PCB_FRONT_Y-0.15:.2f}..{PCB_BACK_Y+0.30:.2f} ({PCB_BACK_Y+0.30-PCB_FRONT_Y+0.15:.2f} mm)')
