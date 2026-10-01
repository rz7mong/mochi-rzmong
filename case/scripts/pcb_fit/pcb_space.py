#!/usr/bin/env python3
"""Usable outline for a custom carrier PCB inside case + stand (LCD fixed), from the voxel cavity (0.5 mm).
For a PCB lying flat (normal = z) with bottom at z0, thickness t, bottom-side keep-out hb and top-side stack ht,
a cell (x,y) is usable if the whole column z0-hb .. z0+t+ht is free cavity. Outline = largest connected region,
eroded by 0.5 mm edge clearance. Exports SVG + DXF (R12 LWPOLYLINE-free POLYLINE) + heightmap PNG."""
import json, numpy as np, scipy.ndimage as nd, shapely.geometry as sg, shapely.ops as so
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import os
D = np.load(os.environ.get('CAV','cavity_0.5.npz')); CAV = D['cav']; O = D['origin'].astype(float); R = float(D['R']); ST = D['stand']; CA = D['case']
nx, ny, nz = CAV.shape
zc = O[2] + (np.arange(nz) + 0.5) * R
def kz(z): return int(np.floor((z - O[2]) / R + 1e-6))
SUPPORTS = [(-14.5, 1.0), (14.5, 1.0), (-14.0, 31.0)]
def usable(z0, t=1.6, hb=0.0, ht=4.0, hb_rear=None):
    k0, k1 = kz(z0 - hb), int(np.ceil((z0 + t + ht - O[2]) / R - 1e-6))
    m = CAV[:, :, k0:k1].all(axis=2)
    if hb_rear is not None:      # thinner bottom keep-out over the rear pocket floor (y >= 26.0)
        m2 = CAV[:, :, kz(z0 - hb_rear):k1].all(axis=2)
        yy = (O[1] + (np.arange(ny) + 0.5) * R)[None, :]
        m = np.where(yy >= 26.0, m2, m)
    if os.environ.get('CAV'):    # re-admit the PCB support posts / pads (they end at the PCB bottom)
        xx, yy = np.meshgrid(O[0] + (np.arange(nx) + .5) * R, O[1] + (np.arange(ny) + .5) * R, indexing='ij')
        for sx, sy in SUPPORTS:
            m |= ((xx - sx) ** 2 + (yy - sy) ** 2 <= 2.6 ** 2) & CAV[:, :, kz(z0 + 0.1):k1].all(axis=2)
    m &= (O[1] + (np.arange(ny) + 0.5) * R)[None, :] >= -3.5     # behind the LCD (+wire zone) only
    m = nd.binary_erosion(m, iterations=1)                       # 0.5 mm edge clearance
    lab, n = nd.label(m)
    if n == 0: return m, None
    big = lab == (np.argmax(nd.sum(m, lab, range(1, n + 1))) + 1)
    return big, k1
def headroom(z_top):
    """free height (mm) above z_top for each column (continuous free run starting at z_top)."""
    k = kz(z_top); col = CAV[:, :, k:]
    run = np.cumprod(col, axis=2).sum(axis=2) * R
    return run
def poly(mask):
    boxes = [sg.box(O[0] + i * R, O[1] + j * R, O[0] + (i + 1) * R, O[1] + (j + 1) * R) for i, j in np.argwhere(mask)]
    p = so.unary_union(boxes).simplify(0.3, preserve_topology=True)
    if p.geom_type == 'MultiPolygon': p = max(p.geoms, key=lambda g: g.area)
    return p
def max_rect(mask):
    """largest axis-aligned rectangle of True cells (histogram method)."""
    h = np.zeros(mask.shape[1], int); best = (0, None)
    for i in range(mask.shape[0]):
        h = np.where(mask[i], h + 1, 0)
        st = []
        for j in range(len(h) + 1):
            cur = h[j] if j < len(h) else 0
            s = j
            while st and st[-1][1] >= cur:
                s, hh = st.pop(); a = hh * (j - s)
                if a > best[0]: best = (a, (i - hh + 1, s, i + 1, j))
            st.append((s, cur))
    a, (i0, j0, i1, j1) = best
    return dict(x0=O[0] + i0 * R, y0=O[1] + j0 * R, x1=O[0] + i1 * R, y1=O[1] + j1 * R, W=(i1 - i0) * R, D=(j1 - j0) * R)
def write_svg(polys, fn):
    allx = [x for p in polys.values() for x, _ in p.exterior.coords]; ally = [y for p in polys.values() for _, y in p.exterior.coords]
    x0, x1, y0, y1 = min(allx) - 2, max(allx) + 2, min(ally) - 2, max(ally) + 2
    cols = ['#d33', '#36c', '#393', '#c90']
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{x1-x0}mm" height="{y1-y0}mm" viewBox="{x0} {-y1} {x1-x0} {y1-y0}">',
         '<!-- case coordinates, mm; SVG y = -case y (top of drawing = rear of head, +y) -->']
    for (name, p), c in zip(polys.items(), cols):
        pts = ' '.join(f'{x:.2f},{-y:.2f}' for x, y in p.exterior.coords)
        s.append(f'<polygon id="{name}" points="{pts}" fill="none" stroke="{c}" stroke-width="0.2"/>')
    s.append('</svg>'); open(fn, 'w').write('\n'.join(s))
def write_dxf(polys, fn):
    L = ['0', 'SECTION', '2', 'ENTITIES']
    for name, p in polys.items():
        L += ['0', 'POLYLINE', '8', name, '66', '1', '70', '1']
        for x, y in list(p.exterior.coords)[:-1]:
            L += ['0', 'VERTEX', '8', name, '10', f'{x:.3f}', '20', f'{y:.3f}', '30', '0.0']
        L += ['0', 'SEQEND']
    L += ['0', 'ENDSEC', '0', 'EOF']; open(fn, 'w').write('\n'.join(L) + '\n')
CASES = {
 'P_pcb_variant_ht6': dict(z0=-15.2, hb=2.0, ht=6.0, hb_rear=1.2),
 'P_pcb_variant_ht9': dict(z0=-15.2, hb=2.0, ht=9.0, hb_rear=1.2),
 # C: designer constraints: single-sided 1.6 mm THT carrier, modules on short headers (5-6 mm), cap 8-9 mm, 2 mm joints below.
 #    PCB bottom z=-15.2 / top -13.6 so the ESP32 (2.5 mm header spacer + 1.0 PCB + 1.6 half receptacle) has its USB-C
 #    centre at z=-8.5 = centre of the rear 13x8 port.
 'C_carrier_ht6': dict(z0=-15.2, hb=2.0, ht=6.0),
 'C_carrier_ht9': dict(z0=-15.2, hb=2.0, ht=9.0),
 'C_carrier_ht6_hb1': dict(z0=-15.2, hb=1.0, ht=6.0),
 # A: PCB lying on the stand floor (z=-26.73), parts on top up to 4 mm (TP4056 itself must also sit here -> USB to bottom slot)
 'A_floor_ht4': dict(z0=-26.5, hb=0.0, ht=4.0),   # true floor -26.73 (0.23 mm voxel margin)
 # B: PCB above the stand rails, ESP32 soldered flat on top so its USB-C lines up with the rear 13x8 port
 #    (ESP PCB bottom = carrier top = -11.1 -> carrier z -12.7..-11.1), 2 mm bottom-side keep-out, 4.5 mm top-side
 'B_mid_esp_on_top': dict(z0=-12.7, hb=2.0, ht=4.5),
 'B_mid_tall_top8': dict(z0=-12.7, hb=2.0, ht=8.0),
}
res, polys = {}, {}
for name, cfg in CASES.items():
    m, k1 = usable(**cfg)
    p = poly(m); polys[name] = p; mr = max_rect(m)
    b = p.bounds
    res[name] = dict(cfg, pcb_z=(cfg['z0'], cfg['z0'] + 1.6), area_mm2=round(p.area, 1), bbox=[round(v, 1) for v in b],
                     bbox_W=round(b[2] - b[0], 1), bbox_D=round(b[3] - b[1], 1), max_rect=mr,
                     outline=[(round(x, 2), round(y, 2)) for x, y in p.exterior.coords])
    print(name, 'area', round(p.area), 'bbox', [round(v, 1) for v in b], 'max rect', {k: round(v, 1) for k, v in mr.items()})
SFX = '_pcbvariant' if os.environ.get('CAV') else ''
json.dump(res, open(f'pcb_outlines{SFX}.json', 'w'), indent=1)
write_svg(polys, f'pcb_free_outline{SFX}.svg'); write_dxf(polys, f'pcb_free_outline{SFX}.dxf')
# heightmaps: free height above PCB top for each candidate
fig, ax = plt.subplots(1, 2, figsize=(16, 9))
for a, name in zip(ax, (['P_pcb_variant_ht6', 'P_pcb_variant_ht9'] if os.environ.get('CAV') else ['C_carrier_ht6', 'C_carrier_ht9'])):
    z_top = CASES[name]['z0'] + 1.6; hr = headroom(z_top)
    hr = np.where(CAV[:, :, kz(z_top)], hr, np.nan)
    im = a.imshow(hr.T, origin='lower', extent=[O[0], O[0] + nx * R, O[1], O[1] + ny * R], cmap='viridis', vmin=0, vmax=40)
    cs = a.contour(O[0] + (np.arange(nx) + .5) * R, O[1] + (np.arange(ny) + .5) * R, np.nan_to_num(hr).T, levels=[3, 5, 8, 12, 20], colors='w', linewidths=.6)
    a.clabel(cs, fmt='%d mm', fontsize=7)
    x, y = polys[name].exterior.xy; a.plot(x, y, 'r-', lw=1.5)
    mr = res[name]['max_rect']; a.add_patch(plt.Rectangle((mr['x0'], mr['y0']), mr['W'], mr['D'], fill=False, ec='orange', lw=1.5, ls='--'))
    a.set_xlim(-26, 26); a.set_ylim(-14, 40); a.set_aspect('equal'); a.grid(alpha=.3)
    a.set_title(f"{name}: free height above PCB top (z={z_top:.1f})\nred = usable outline (stack {CASES[name]['ht']} mm), orange = max rectangle {mr['W']:.1f} x {mr['D']:.1f}")
    a.set_xlabel('x (mm)'); a.set_ylabel('y (mm)  (+y = rear / USB port, -y = LCD)')
plt.colorbar(im, ax=ax, shrink=.7, label='free height above PCB top (mm)')
plt.savefig(f'pcb_headroom_map{SFX}.png', dpi=110, bbox_inches='tight')
# stand features usable as PCB supports: top z of stand material per column (under B plane)
k_b = kz(-12.7)
top = np.full((nx, ny), np.nan)
for i, j in np.argwhere(ST[:, :, :k_b].any(axis=2)):
    top[i, j] = O[2] + (np.max(np.where(ST[i, j, :k_b])[0]) + 1) * R
for name, (x, y) in {'rail_L_front': (-14.5, 0), 'rail_L_back': (-14.5, 10), 'rail_R_front': (14.5, 0), 'rail_R_back': (14.5, 10)}.items():
    i, j = int((x - O[0]) / R), int((y - O[1]) / R); print(name, (x, y), 'stand top z', top[i, j])
