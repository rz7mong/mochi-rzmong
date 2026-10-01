import sys, json, numpy as np, trimesh
from _paths import *  # repo-relative paths
sys.argv = ['x']
exec(open('check_designer_v3.py').read().split('# ================= checks')[0]); TRIM = TRIM
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon as MP
cm = trimesh.load(CASE_PCB); sm = trimesh.load(STAND_PCB); sm.apply_translation([0, 0, -10.38])
def sec(ax, m, ax_i, val, col, keep):
    n = np.zeros(3); n[ax_i] = 1; o = np.zeros(3); o[ax_i] = val; s = m.section(plane_origin=o, plane_normal=n)
    if s is not None:
        for e in s.discrete: ax.plot(e[:, keep[0]], e[:, keep[1]], color=col, lw=0.9)
def bb(m): b = m.bounding_box(); return np.array(b[:3]), np.array(b[3:])
parts = {'MAX98357 (edge)': (top['max98357_edge'], '#9467bd'), 'SD (edge)': (top['sd_edge'], '#2ca02c'), 'cap 6.3': (top['cap'], '#8c564b'),
         'ESP32-C3': (top['esp'], '#1f77b4'), 'USB-C': (top['esp_usb'], '#17becf'), 'hdr MAX': (hdr_max, '#555'), 'hdr SD': (hdr_sd, '#555'),
         'LiPo (off-board)': (off['battery_LiPo501640'], '#ff7f0e'), 'switch': (off['switch_rightangle_offboard'], '#bcbd22'),
         'speaker': (off['speaker_15x11'], '#e377c2'), 'TTP223': (off['ttp223_red_15x11'], '#d62728'), 'TP4056': (TP, '#7f7f7f'),
         'LCD wires': (LCDW, '#000000'), 'nut L': (nut['L'], '#444'), 'nut R': (nut['R'], '#444')}
fig = plt.figure(figsize=(20, 11)); gs = fig.add_gridspec(2, 3)
ax = fig.add_subplot(gs[:, 0])
sec(ax, cm, 2, -14.0, 'k', (0, 1)); sec(ax, sm, 2, -16.0, 'tab:blue', (0, 1))
ax.add_patch(MP(np.asarray(L['outline']), closed=True, fc='#f6efd9', ec='g', lw=1.5, zorder=1))
for n, p in pads.items():
    ax.add_patch(Circle((p['x'], p['y']), p['d'] / 2, fc='#d4a017' if n not in TRIM else '#ff4040', ec='k', lw=0.3, zorder=3))
for x, y in L['holes']:
    ax.add_patch(Circle((x, y), 1.1, fc='w', ec='k', zorder=4)); ax.add_patch(Circle((x, y), 2.31, fill=False, ec='k', ls='--', zorder=4)); ax.add_patch(Circle((x, y), 2.5, fill=False, ec='b', ls=':', zorder=4))
for k, (m, c) in parts.items():
    lo, hi = bb(m)
    if k in ('speaker', 'TTP223'): continue
    ax.add_patch(Rectangle(lo[:2], *(hi - lo)[:2], fc=c, alpha=0.18, ec=c, lw=1, zorder=2))
for j in L['jumpers']:
    xy = np.asarray(j['path']); ax.plot(xy[:, 0], xy[:, 1], '-' if j['side'] == 'top' else '--', color='k' if j['side'] == 'top' else 'm', lw=1.6 if j['side'] == 'top' else 1.0, zorder=7)
    ax.text(*xy[len(xy) // 2], j['name'] + (' (bottom)' if j['side'] == 'bottom' else ''), fontsize=6, color='m' if j['side'] == 'bottom' else 'k', zorder=8)
ax.add_patch(MP(np.asarray(PL.exterior.coords) if PL.geom_type == 'Polygon' else np.zeros((3, 2)), closed=True, fill=False))
for g in (PL.geoms if PL.geom_type != 'Polygon' else [PL]): ax.add_patch(MP(np.asarray(g.exterior.coords), closed=True, fc='#333', alpha=0.25, zorder=2))
for ln in lcd_lines: xy = np.asarray(ln.coords); ax.plot(xy[:, 0], xy[:, 1], color='#00a', lw=0.8, zorder=6)
ax.plot([0.3], [5.6], 'mx', ms=9, mew=2, zorder=9); ax.text(0.8, 5.9, 'JP3/JP4 cross', color='m', fontsize=6, zorder=9)
ax.add_patch(Rectangle((-2.5, 22), 5, 11.5, fill=False, hatch='///', lw=0.4)); ax.add_patch(Circle((0, 30.5), 2, fc='b', alpha=0.15))

ax.add_patch(Circle((-15.25, 13.2), 3.15, fill=False, ec='#8c564b', lw=1.2, zorder=6))
ax.set_xlim(-24, 24); ax.set_ylim(-8, 38); ax.set_aspect('equal'); ax.grid(alpha=0.3)
ax.set_title('Designer layout v3 in the assembly, top view (case frame)\nblack = case section z -14, blue = stand z -16; red pads = trimmed joints;\nblack = top jumpers, magenta dashed = bottom jumpers, blue = LCD wires (under PCB); grey = ESP header plastic; dashed circle = M2 nut circumcircle, dotted = Ø5 post', fontsize=9)
cuts = [(1, 6.0, 'y = 6 (through MAX/SD)'), (1, 3.5, 'y = 3.5 (LCD row + bottom jumpers)'), (0, -10.0, 'x = -10 (MAX side)'), (0, 12.0, 'x = 12 (SD side)')]
for i, (a, v, t) in enumerate(cuts):
    axx = fig.add_subplot(gs[i // 2, 1 + i % 2]); keep = [j for j in range(3) if j != a]
    sec(axx, cm, a, v, 'k', keep); sec(axx, sm, a, v, 'tab:blue', keep)
    bl, bh = bb(board); 
    for k, (m, c) in list(parts.items()) + [('PCB', (board, 'g')), ('joints', (board, 'r')), ('JP3/JP4 bottom', (jsolid['JP3'] + jsolid['JP4'], 'm'))]:
        lo, hi = bb(m)
        if k == 'joints':
            for jn, j in joints.items():
                jl, jh = bb(j)
                if jl[a] <= v <= jh[a]: axx.add_patch(Rectangle((jl[keep[0]], jl[keep[1]]), jh[keep[0]] - jl[keep[0]], jh[keep[1]] - jl[keep[1]], fc='r', alpha=0.5))
            continue
        if lo[a] <= v <= hi[a]:
            axx.add_patch(Rectangle((lo[keep[0]], lo[keep[1]]), hi[keep[0]] - lo[keep[0]], hi[keep[1]] - lo[keep[1]], fc=c, alpha=0.3, ec=c))
            axx.text((lo[keep[0]] + hi[keep[0]]) / 2, (lo[keep[1]] + hi[keep[1]]) / 2, k, fontsize=6, ha='center')
    axx.set_aspect('equal'); axx.grid(alpha=0.3); axx.set_title(t, fontsize=9); axx.set_xlabel('xyz'[keep[0]]); axx.set_ylabel('xyz'[keep[1]])
plt.tight_layout(); plt.savefig(os.path.join(DOCS_FIT, 'pcb_v3', 'designer_v3_in_assembly.png'), dpi=120); print('ok')
