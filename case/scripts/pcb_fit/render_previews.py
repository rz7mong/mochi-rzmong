#!/usr/bin/env python3
"""Preview renders: PCB top layout (v2 outline + v7 layout), section views (loose-module layout and PCB variant),
OpenSCAD scenes for transparent 3D renders, and an STL of the component envelopes."""
import json, sys, numpy as np, trimesh
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon as MPoly
from _paths import *; import fit_tatakan_gmt130 as F
OUT = json.load(open(OUTLINE_V2)); poly = np.asarray(OUT['outline'])
V7 = json.load(open(PLACEMENT_V7_VERIFIED)); LOOSE = json.load(open('placement_verified.json'))
COL = {'esp': '#1f77b4', 'usb': '#17becf', 'sd': '#2ca02c', 'max': '#9467bd', 'cap': '#8c564b', 'bat': '#ff7f0e', 'spe': '#e377c2',
       'ttp': '#d62728', 'swi': '#bcbd22', 'tp4': '#7f7f7f', 'lcd': '#000000', 'm2_': '#444444', 'bot': '#bbbbbb'}
col = lambda k: next((v for p, v in COL.items() if p in k), '#333333')
# LCD module boxes (case frame)
zf = F.FLOOR_Z + 0.02 - 10.38
LCD = [((-F.PCB_W/2, F.PCB_FRONT_Y, zf), (F.PCB_W/2, F.PCB_BACK_Y, zf + F.PCB_H)),
       ((-F.GLASS_W/2, F.FRAME_Y_BACK, zf + 5), (F.GLASS_W/2, F.PCB_FRONT_Y, zf + 5 + 29.22)),
       ((-10, F.PCB_BACK_Y, zf + 0.3), (10, F.PCB_BACK_Y + 2.5, zf + 4.8))]
# ---------- 1) PCB top view ----------
fig, ax = plt.subplots(figsize=(8, 7.5))
ax.add_patch(MPoly(poly, closed=True, fc='#e8f5e9', ec='g', lw=2, label='carrier PCB outline v2'))
for x, y in OUT['holes']: ax.add_patch(Circle((x, y), 1.1, fc='w', ec='k')); ax.add_patch(Circle((x, y), 2.5, fill=False, ls=':', ec='k'))
ax.add_patch(Rectangle((-2.5, 22), 5, 11.5, fc='none', ec='k', hatch='///', lw=0.5))
ax.text(0, 21.2, 'no joints (rest-pad slide)', ha='center', fontsize=6)
ax.add_patch(Circle((0, 30.5), 2.0, fc='#999', ec='k', alpha=0.6))
for k, v in V7.items():
    if k.startswith('tp4056'): continue
    lo, hi = v['lo'], v['hi']; onb = abs(lo[2] - (-13.6)) < 0.7
    ax.add_patch(Rectangle((lo[0], lo[1]), hi[0] - lo[0], hi[1] - lo[1], fc=col(k), alpha=0.35 if onb else 0.12,
                           ec=col(k), lw=1.5 if onb else 1, ls='-' if onb else '--'))
    ax.text((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, k.replace('_', ' ') + ('' if onb else '\n(off-board)') + f'\nz {lo[2]:.1f}..{hi[2]:.1f}',
            ha='center', va='center', fontsize=5.5)
t = V7['tp4056_on_floor']; ax.add_patch(Rectangle((t['lo'][0], t['lo'][1]), t['hi'][0] - t['lo'][0], t['hi'][1] - t['lo'][1], fill=False, ec='gray', ls=':', lw=1))
ax.text(t['hi'][0] - 0.3, 22, 'TP4056 under PCB\n(on stand floor)', ha='right', fontsize=5.5, color='gray')
ax.annotate('FRONT edge: faces LCD (7 wires)', (0, -2.5), (0, -7.5), ha='center', fontsize=8, arrowprops=dict(arrowstyle='->'))
ax.annotate('REAR tab: ESP32 USB-C -> rear port', (0, 33.5), (0, 38), ha='center', fontsize=8, arrowprops=dict(arrowstyle='->'))
ax.text(14, 36, 'switch (off-board, glued in pocket,\nhandle through rear wall x 9.5..13.5)', fontsize=6, ha='center')
ax.set_xlim(-26, 26); ax.set_ylim(-10, 40); ax.set_aspect('equal'); ax.grid(alpha=0.3)
ax.set_title('Carrier PCB v2 (case coordinates, mm), top view: -y = face/LCD, +y = rear\nsolid = on the board, dashed = off-board parts above it')
ax.set_xlabel('x'); ax.set_ylabel('y'); plt.tight_layout(); plt.savefig('pcb_layout_v2_top.png', dpi=150); plt.close()
# ---------- 2) sections ----------
case_pcb = trimesh.load(CASE_PCB); stand_pcb = trimesh.load(STAND_PCB); stand_pcb.apply_translation([0, 0, -10.38])
case0 = trimesh.load(CASE_ORIG); stand0 = trimesh.load(STAND_ORIG); stand0.apply_translation([0, 0, -10.38])
def draw_section(ax, meshes, P, axis, val, extra=()):
    n = np.zeros(3); n[axis] = 1; o = np.zeros(3); o[axis] = val
    keep = [i for i in range(3) if i != axis]
    for m, c in meshes:
        s = m.section(plane_origin=o, plane_normal=n)
        if s is None: continue
        for e in s.discrete: ax.plot(e[:, keep[0]], e[:, keep[1]], color=c, lw=1)
    boxes = list(P.items()) + [(f'lcd{i}', dict(lo=a, hi=b)) for i, (a, b) in enumerate(LCD)] + list(extra)
    for k, v in boxes:
        lo, hi = v['lo'], v['hi']
        if lo[axis] <= val <= hi[axis]:
            ax.add_patch(Rectangle((lo[keep[0]], lo[keep[1]]), hi[keep[0]] - lo[keep[0]], hi[keep[1]] - lo[keep[1]],
                                   fc=col(k), alpha=0.35 if not k.startswith('lcd') else 0.15, ec=col(k)))
            if not k.startswith('lcd'):
                ax.text((lo[keep[0]] + hi[keep[0]]) / 2, (lo[keep[1]] + hi[keep[1]]) / 2, k.split('_')[0], fontsize=5, ha='center', va='center')
    ax.set_aspect('equal'); ax.grid(alpha=0.25); ax.set_title(f"{'xyz'[axis]} = {val}", fontsize=8)
    ax.set_xlabel('xyz'[keep[0]]); ax.set_ylabel('xyz'[keep[1]])
pcb_box = ('bot_pcb', dict(lo=[poly[:, 0].min(), poly[:, 1].min(), -15.2], hi=[poly[:, 0].max(), poly[:, 1].max(), -13.6]))
for tag, meshes, P, cuts, extra in [
    ('pcb_v7', [(case_pcb, 'k'), (stand_pcb, 'tab:blue')], V7, [(0, 0.0), (0, -12.0), (0, 12.0), (1, 0.0), (1, 6.0), (1, 13.0), (1, 31.0), (2, -10.0), (2, 0.0), (2, 18.5)], [pcb_box]),
    ('loose', [(case0, 'k'), (stand0, 'tab:blue')], LOOSE, [(0, 0.0), (0, -12.0), (0, 12.0), (1, 0.0), (1, 6.0), (1, 13.0), (1, 31.0), (2, -23.0), (2, -10.0), (2, 2.0)], [])]:
    fig, axs = plt.subplots(2, 5, figsize=(22, 9))
    for ax, (a, v) in zip(axs.ravel(), cuts): draw_section(ax, meshes, P, a, v, extra)
    fig.suptitle(f'{tag}: sections through case (black) + stand (blue) with component envelopes (coloured boxes; LCD faint)')
    plt.tight_layout(); plt.savefig(f'sections_{tag}.png', dpi=110); plt.close()
# ---------- 3) envelope STLs + OpenSCAD scenes ----------
def boxes_mesh(P):
    ms = []
    for k, v in P.items():
        lo, hi = np.array(v['lo']), np.array(v['hi']); b = trimesh.creation.box(extents=hi - lo); b.apply_translation((lo + hi) / 2); ms.append(b)
    return trimesh.util.concatenate(ms)
boxes_mesh(V7).export('component_envelopes_pcb_v7.stl'); boxes_mesh(LOOSE).export('component_envelopes_loose.stl')
def scad(P, casef, standf, fname, with_pcb):
    L_ = ['$fn=24;', f'%import("{casef}");', f'color([0.3,0.5,1,0.35]) translate([0,0,-10.38]) import("{standf}");']
    if with_pcb: L_.append('color([0.1,0.6,0.1]) translate([0,0,-15.2]) linear_extrude(1.6) polygon(' + json.dumps(poly.tolist()) + ');')
    for k, v in P.items():
        lo, hi = np.array(v['lo']), np.array(v['hi']); c = col(k).lstrip('#'); rgb = [int(c[i:i+2], 16) / 255 for i in (0, 2, 4)]
        L_.append(f'color([{rgb[0]:.2f},{rgb[1]:.2f},{rgb[2]:.2f}]) translate({lo.round(3).tolist()}) cube({(hi - lo).round(3).tolist()});  // {k}')
    for a, b in LCD: L_.append(f'color([0,0,0,0.5]) translate({list(a)}) cube({[b[i] - a[i] for i in range(3)]});')
    open(fname, 'w').write('\n'.join(L_) + '\n')
scad(V7, CASE_PCB, STAND_PCB, 'assembly_pcb_v7.scad', True)
scad(LOOSE, CASE_ORIG, STAND_ORIG, 'assembly_loose.scad', False)
print('done')
