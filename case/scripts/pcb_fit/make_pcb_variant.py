#!/usr/bin/env python3
"""Variant for a custom carrier PCB (single-sided 1.6 mm THT). Writes NEW files only:
  tatakan_GMT130_fit_pcb.stl   = tatakan_GMT130_fit.stl with the old back-box walls behind the LCD rails (y > -4.0,
                                 above case z -17.4) removed -> room under the PCB, + 2 front PCB support posts
  case_luar_lcd_23_40mm_pcb.stl = case with: speaker grille (top), slide-switch slot (rear wall, right of USB port),
                                 2 rear PCB screw pads in the rear pocket (M2 / 2 mm self-tapping, pilot 1.7 mm)
Case coordinates (mm); stand STL is in its own frame = case frame + (0,0,+10.38)."""
import sys, numpy as np, manifold3d as mf
from _paths import *  # repo-relative paths
import fit_tatakan_gmt130 as F
box, load, save = F.box, F.load, F.save
DZ = -10.38
PCB_Z0, PCB_T = -15.2, 1.6            # PCB bottom / thickness (case z)
FLOOR = -26.73
PILOT = 1.7                           # M2 self-tapping into PLA (use 1.6-1.8); M2 machine screw + nut: 2.2 clearance
def cyl(x, y, z0, z1, d, n=40):
    return mf.Manifold.cylinder(z1 - z0, d / 2, d / 2, n).translate([x, y, z0])
POSTS = [(-14.5, 0.5), (14.5, 0.5)]   # front PCB supports on the stand floor (clear of TP4056 x+-8.65, LCD wires y<-3.6)
REAR_PADS = []                     # (v1 had screw pads in the pocket wings; wings are unreachable during assembly -> removed)
REST_PAD = (0.0, 30.5, 4.0)        # rear rest pad under the PCB tab, on the pocket floor plate, top = PCB bottom (no screw)
SCREW_THRU, HEAD_D, HEAD_H = 2.4, 4.4, 1.8   # M2 screw from UNDER the stand base, up through the post into an M2 nut/standoff on the PCB top
GRILLE_C, GRILLE_AX, HOLE_D, PITCH = (-1.25, 0.75), (6.0, 4.0), 1.5, 2.2   # over the 15x11 speaker face (PUI AS01508MS-SP11-WP-R) at (-9..6.5, -5..6.5)
SW_SLOT = dict(x=(9.5, 13.5), z=(-8.0, -4.7))    # handle slot through the rear wall right of the 13x8 USB port (3 mm web)
SW_CBORE = dict(x=(8.5, 14.5), z=(-8.9, -3.8), y=(37.0, 41.0))  # outside counterbore -> handle only ~0.3 mm recessed

def stand():
    T = load(STAND_ORIG)
    cut = box(-25, 25, -4.0, 40, -17.4 - DZ, 30)          # everything behind the rail back lips (y>-4.0) above case z -17.4
    T = T - cut
    for x, y in POSTS:
        T = T + cyl(x, y, FLOOR - DZ - 0.5, PCB_Z0 - DZ, 5.0)
        T = T - cyl(x, y, -30, PCB_Z0 - DZ + 0.1, SCREW_THRU) - cyl(x, y, -30, -17.7 + HEAD_H, HEAD_D)
    return T

def case():
    C = load(CASE_ORIG)
    holes = []
    for i in np.arange(-4, 5):
        for j in np.arange(-4, 5):
            x = GRILLE_C[0] + i * PITCH; y = GRILLE_C[1] + j * PITCH
            if ((x - GRILLE_C[0]) / GRILLE_AX[0]) ** 2 + ((y - GRILLE_C[1]) / GRILLE_AX[1]) ** 2 <= 1.0:
                holes.append(cyl(x, y, 15.0, 30.0, HOLE_D, 16))
    C = C - mf.Manifold.batch_boolean(holes, mf.OpType.Add)
    C = C - box(SW_SLOT['x'][0], SW_SLOT['x'][1], 33.0, 41.0, SW_SLOT['z'][0], SW_SLOT['z'][1])
    C = C - box(SW_CBORE['x'][0], SW_CBORE['x'][1], SW_CBORE['y'][0], SW_CBORE['y'][1], SW_CBORE['z'][0], SW_CBORE['z'][1])
    for x, y in REAR_PADS:
        pad = cyl(x, y, -16.6, PCB_Z0, 4.5) - cyl(x, y, -22.0, PCB_Z0 + 0.1, PILOT)
        C = (C - cyl(x, y, -22.0, -16.4, PILOT)) + pad
    x, y, d = REST_PAD
    C = C + cyl(x, y, -17.4, PCB_Z0, d)
    return C, len(holes)

if __name__ == '__main__':
    T = stand(); t = save(T, STAND_PCB)
    print('stand', t.is_watertight, np.round(t.bounds, 2).tolist())
    C, nh = case(); c = save(C, CASE_PCB)
    print('case', c.is_watertight, np.round(c.bounds, 2).tolist(), 'grille holes', nh)
