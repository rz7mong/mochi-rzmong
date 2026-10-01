#!/usr/bin/env python3
"""Full fit/insertion check of designer layout v3 (pcb/v3/layout_v3_case_frame.json) against
case_luar_lcd_23_40mm_pcb.stl + tatakan_GMT130_fit_pcb.stl. Same models as check_designer_v2.py, plus jumper wires
(top JP1/JP2 Ø1.0 flat, bottom JP3/JP4 Ø0.6 flat), ESP header plastic pieces, individual LCD wires, off-board wire stubs."""
import json, re, sys, math, numpy as np, manifold3d as mf, shapely.geometry as sg, shapely.ops as so
from _paths import *; import fit_tatakan_gmt130 as F
box = F.box
L = json.load(open(LAYOUT_V3))
V7 = json.load(open('placement_pcb_v7_cap6.3.json')); REF = json.load(open(OUTLINE_V2))
ZB, ZT = -15.2, -13.6
R = {}
def cyl(x, y, z0, z1, d, n=32): return mf.Manifold.cylinder(z1 - z0, d / 2, d / 2, n).translate([x, y, z0])
def B(lo, hi): return box(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
def ext(poly, z0, z1):
    polys = [poly] if poly.geom_type == 'Polygon' else list(poly.geoms)
    return mf.Manifold.batch_boolean([mf.Manifold.extrude(mf.CrossSection([list(p.exterior.coords)[:-1]]), z1 - z0).translate([0, 0, z0]) for p in polys], mf.OpType.Add)
def gap(a, b):
    v = (a ^ b).volume(); return (-round(v, 3) if v > 1e-4 else round(a.min_gap(b, 6), 2))
# ---- outline ----
svg = open(LAYOUT_V3_SVG).read()
m = re.search(r'id="outline_v\d" d="([^"]+)"', svg)
Ps = sg.Polygon([(float(a) - 29.5, 44 - float(b)) for a, b in re.findall(r'([-\d.]+),([-\d.]+)', m.group(1))]) if m else None
Pj, Pr = sg.Polygon(L['outline']), sg.Polygon(REF['outline'])
R['outline'] = dict(json_vs_v2dxf_symdiff=round(Pj.symmetric_difference(Pr).area, 4), svg_vs_v2dxf_symdiff=round(Ps.symmetric_difference(Pr).area, 4) if Ps else 'no outline path',
                    holes_equal=L['holes'] == REF['holes'])
print('outline', R['outline'])
# ---- parts ----
pads = {p['name']: p for p in L['pads']}
TRIM = set(L['trim_le_1mm']); TH = {n: (1.0 if n in TRIM else 2.0) for n in pads}
board = ext(Pj, ZB, ZT)
for x, y in L['holes']: board = board - cyl(x, y, ZB - 1, ZT + 1, 2.2)
fil = {n: sg.Point(p['x'], p['y']).buffer((p['d'] + 0.4) / 2, 32) for n, p in pads.items()}
joints = {n: cyl(p['x'], p['y'], ZB - TH[n], ZB, p['d'] + 0.4) for n, p in pads.items()}
JOINTS = mf.Manifold.batch_boolean(list(joints.values()), mf.OpType.Add)
M = L['modules_top']; mx, sd, c = M['max98357_edge'], M['sd_edge'], M['cap']
top = {'max98357_edge': B([mx[0], mx[1], ZT], [mx[2], mx[3], ZT + 0.6 + 19.4 + 2.5]),
       'sd_edge': B([sd[0], sd[1], ZT], [sd[2], sd[3], ZT + 0.6 + 20.0 + 2.5]),
       'cap': cyl(c['c'][0], c['c'][1], ZT, 0.5, c['d']),
       'esp': B([M['esp'][0], M['esp'][1], ZT + 2.5], [M['esp'][2], M['esp'][3], V7['esp32c3_supermini_on_headers']['hi'][2]]),
       'esp_usb': B(V7['esp32c3_usbc_receptacle']['lo'], V7['esp32c3_usbc_receptacle']['hi'])}
# ESP header plastic pieces (2.54 wide per pin, 2.5 tall), cut pins removed incl. plastic
cut = {(round(cp['x'], 2), round(cp['y'], 2)) for cp in L['cut_pins']}
plast = []
for sx in (-7.62, 7.62):
    for k in range(8):
        y = 13.12 + 2.54 * k
        if (sx, round(y, 2)) in cut: continue
        plast.append(sg.box(sx - 1.27, y - 1.27, sx + 1.27, y + 1.27))
PL = so.unary_union(plast); ESPPL = ext(PL.buffer(0), ZT, ZT + 2.5)
def hdr(names):
    xs = [pads[n]['x'] for n in names]; y = pads[names[0]]['y']; return B([min(xs) - 1.27, y - 1.27, ZT], [max(xs) + 1.27, y + 1.27, ZT + 2.5])
hdr_max = hdr([n for n in pads if n.startswith('J3.')]); hdr_sd = hdr([n for n in pads if n.startswith('J2.')])
nut = {s: cyl(x, y, ZT, ZT + 1.6, 4.62, 48) for s, (x, y) in zip('LR', L['holes'])}
stdo = {s: cyl(x, y, ZT, ZT + 3.0, 3.5, 32) for s, (x, y) in zip('LR', L['holes'])}
post2d = {s: sg.Point(x, y).buffer(2.5, 48) for s, (x, y) in zip('LR', L['holes'])}
# jumpers
J = {j['name']: j for j in L['jumpers']}
jl2d = {n: sg.LineString(j['path']) for n, j in J.items()}
jw = {n: (1.0 if J[n]['side'] == 'top' else 0.6) for n in J}
jsolid = {}
for n, j in J.items():
    poly = jl2d[n].buffer(jw[n] / 2, 16)
    jsolid[n] = ext(poly, ZT, ZT + jw[n]) if j['side'] == 'top' else ext(poly, ZB - jw[n], ZB)
# LCD wires: bundle riser behind LCD within x+-9.5, then under PCB (z ZB-1.0..ZB, Ø1.0) fanning to J1 pads only at y>-3.6
j1 = sorted([pads[n] for n in pads if n.startswith('J1.')], key=lambda p: p['x'])
riser = B([-9.5, F.PCB_BACK_Y + 0.1, -22.6], [9.5, F.PCB_BACK_Y + 2.3, ZB - 1.0])
lcd_lines = []
for i, p in enumerate(j1):
    xr = -7.62 + 2.54 * i            # position in the riser (ASSUMED 2.54 spacing, within +-9.5)
    lcd_lines.append(sg.LineString([(xr, F.PCB_BACK_Y + 1.2), (xr, -3.6), (p['x'], p['y'])]))
LCDW2D = so.unary_union([l.buffer(0.5, 16) for l in lcd_lines])
LCDW = riser + ext(LCDW2D, ZB - 1.0, ZB)
# env
C = F.load(CASE_PCB); T = F.load(STAND_PCB).translate([0, 0, -10.38])
zf = F.FLOOR_Z + 0.02 - 10.38
LCD = box(-F.PCB_W/2, F.PCB_W/2, F.PCB_FRONT_Y, F.PCB_BACK_Y, zf, zf + F.PCB_H) + box(-F.GLASS_W/2, F.GLASS_W/2, F.FRAME_Y_BACK + 0.02, F.PCB_FRONT_Y, zf + 5, zf + 5 + 29.22)
LCDP = box(-10, 10, F.PCB_BACK_Y, F.PCB_BACK_Y + 2.5, zf + 0.3, zf + 4.8)
tp = V7['tp4056_on_floor']; TP = B(tp['lo'], tp['hi'])
off = {k: B(V7[k]['lo'], V7[k]['hi']) for k in ('battery_LiPo501640', 'speaker_15x11', 'ttp223_red_15x11', 'switch_rightangle_offboard', 'switch_handle')}
ENV = dict(case=C, stand=T, lcd=LCD, lcd_pins=LCDP, tp4056=TP)
# ================= checks =================
# applied fixes
R['fixes'] = dict(
    header_row_y={n: pads[n]['y'] for n in ('J3.GND', 'J2.SCK')},
    pad_to_hole={'J3.GND': round(math.dist((pads['J3.GND']['x'], pads['J3.GND']['y']), L['holes'][0]), 2), 'J2.SCK': round(math.dist((pads['J2.SCK']['x'], pads['J2.SCK']['y']), L['holes'][1]), 2)},
    nut_to_header_plastic={s: round(nut[s].min_gap(hdr_max if s == 'L' else hdr_sd, 5), 2) for s in 'LR'},
    standoff35_to_header_plastic={s: round(stdo[s].min_gap(hdr_max if s == 'L' else hdr_sd, 5), 2) for s in 'LR'},
    post_to_nearest_fillet={s: round(min(post2d[s].distance(f) for f in fil.values()), 2) for s in 'LR'},
    JP1_to_esp_plastic=round(jl2d['JP1'].buffer(0.5).distance(PL), 2), JP2_to_esp_plastic=round(jl2d['JP2'].buffer(0.5).distance(PL), 2),
    JP1_to_cap_body=round(jl2d['JP1'].buffer(0.5).distance(sg.Point(*c['c']).buffer(c['d'] / 2, 64)), 2),
    JP2_to_cap_body=round(jl2d['JP2'].buffer(0.5).distance(sg.Point(*c['c']).buffer(c['d'] / 2, 64)), 2),
    JP1_JP2_vs_esp_bottom_clear_mm=round(2.5 - 1.0, 2),
    rear_joints_ge_y25={n: TH[n] for n, p in pads.items() if p['y'] + (p['d'] + 0.4) / 2 > 25.0},
    pads_in_rest_strip=[n for n in pads if fil[n].intersects(sg.box(-2.5, 22, 2.5, 33.5))])
print('FIXES', R['fixes'])
# item 1/2: off-board wire stubs (Ø1.0 rising 6 mm; merged hole: 2 wires -> Ø1.4 bundle, ASSUMED)
stubs = {'SW.B': 1.0, 'TTP.GND': 1.4, 'TTP.OUT': 1.0}
R['item1_2'] = {n: {k: gap(cyl(pads[n]['x'], pads[n]['y'], ZT, ZT + 6, d), top[k]) for k in ('max98357_edge', 'cap', 'esp')} for n, d in stubs.items()}
R['item1_2']['pad_to_pad_SW.B_TTP.GND'] = round(fil['SW.B'].distance(fil['TTP.GND']), 2)
print('ITEM1/2', R['item1_2'])
# item 3: bottom jumpers
it3 = {}
for n in ('JP3', 'JP4'):
    ends = {J[n]['a'], J[n]['b']}
    w = jl2d[n].buffer(jw[n] / 2, 16)
    fg = sorted(((round(w.distance(f), 2), k) for k, f in fil.items() if k not in ends))[:3]
    it3[n] = dict(min_fillet_gaps=fg, to_post={s: round(jl2d[n].distance(sg.Point(*h)), 2) for s, h in zip('LR', L['holes'])},
                  to_post_edge={s: round(w.distance(post2d[s]), 2) for s in 'LR'},
                  to_lcd_wires_2d=round(w.difference(sg.Point(pads[J[n]['b']]['x'], pads[J[n]['b']]['y']).buffer(1.6)).distance(LCDW2D), 2),
                  inside_outline=Pj.buffer(-0.0).contains(w), edge_margin=round(Pj.exterior.distance(jl2d[n]) - jw[n] / 2, 2),
                  vs_env={k: gap(jsolid[n], o) for k, o in ENV.items()})
it3['JP3_JP4_gap'] = round(jl2d['JP3'].buffer(0.3).distance(jl2d['JP4'].buffer(0.3)), 2)
it3['tp4056_top_below_jumpers'] = round((ZB - 0.6) - tp['hi'][2], 2)
print('ITEM3', it3); R['item3'] = it3
# item 4
p = pads['J3.DIN']; R['item4'] = dict(d=p['d'], hole=p['hole'], annular_ring=round((p['d'] - p['hole']) / 2, 2),
                                     fillet_gap_neighbours=sorted((round(fil['J3.DIN'].distance(fil[k]), 2), k) for k in fil if k != 'J3.DIN')[:2])
print('ITEM4', R['item4'])
# ---- final position all-vs-all ----
ITEMS = dict(top); ITEMS.update(board=board, joints=JOINTS, esp_plastic=ESPPL, hdr_max=hdr_max, hdr_sd=hdr_sd, nut_L=nut['L'], nut_R=nut['R'], lcd_wires=LCDW)
ITEMS.update({f'jumper_{n}': s for n, s in jsolid.items()}); ITEMS.update(off)
allowed = {frozenset(p) for p in [('esp', 'esp_usb'), ('switch_rightangle_offboard', 'switch_handle'), ('hdr_max', 'max98357_edge'), ('hdr_sd', 'sd_edge'),
           ('esp', 'esp_plastic'), ('lcd_wires', 'joints'), ('lcd_wires', 'lcd_pins'), ('lcd_wires', 'lcd'), ('jumper_JP3', 'joints'), ('jumper_JP4', 'joints'),
           ('jumper_JP1', 'joints'), ('jumper_JP2', 'joints')]}
final = {}; bad = []
for k, mm in ITEMS.items():
    row = {w: gap(mm, o) for w, o in ENV.items()}
    for k2, m2 in ITEMS.items():
        if k2 == k or frozenset((k, k2)) in allowed or 'board' in (k, k2): continue
        g = gap(mm, m2)
        if g < 0.3: row[k2] = g
    final[k] = row
    for w, g in row.items():
        if g < 0 and not (k == 'board' and w in ('case', 'stand')): bad.append((k, w, g))
# joints vs jumpers: only the jumper's own end pads may touch
for n in ('JP1', 'JP2', 'JP3', 'JP4'):
    for k, jt in joints.items():
        if k in (J[n]['a'], J[n]['b']): continue
        if (jsolid[n] ^ jt).volume() > 1e-4: bad.append((f'jumper_{n}', k, -round((jsolid[n] ^ jt).volume(), 3)))
R['final'] = final; R['final_bad'] = bad
for k, v in final.items(): print(f'{k:26s}', v)
print('FINAL collisions:', bad or 'none')
bat = off['battery_LiPo501640']
R['battery'] = dict(foam_gap_max=round(bat.min_gap(top['max98357_edge'], 6), 2), foam_gap_sd=round(bat.min_gap(top['sd_edge'], 6), 2))
# ---- assembly ----
REST_JOINT_SLIDE = None
MOVE = board + JOINTS + nut['L'] + nut['R'] + ESPPL + hdr_max + hdr_sd + jsolid['JP1'] + jsolid['JP2'] + jsolid['JP3'] + jsolid['JP4']
for k in ('max98357_edge', 'sd_edge', 'cap', 'esp', 'esp_usb'): MOVE = MOVE + top[k]
bp = V7['battery_LiPo501640']
OBS = C + off['speaker_15x11'] + off['ttp223_red_15x11'] + off['switch_rightangle_offboard'] + off['switch_handle'] + \
      box(bp['lo'][0], bp['hi'][0], bp['lo'][1] - 6.5, bp['hi'][1] - 6.5, bp['lo'][2], bp['hi'][2])
BOFF = 8.0
lift = max(((MOVE.translate([0, -BOFF, dz]) ^ OBS).volume(), dz) for dz in np.arange(-30, 0.01, 0.5))
slide = max(((MOVE.translate([0, dy, 0]) ^ OBS).volume(), dy) for dy in np.arange(-BOFF, 0.01, 0.25))
slide_gap_min = min((MOVE.translate([0, dy, 0])).min_gap(C, 2) for dy in np.arange(-BOFF, 0.01, 0.5))
bat_push = max((box(bp['lo'][0], bp['hi'][0], bp['lo'][1] + dy, bp['hi'][1] + dy, bp['lo'][2], bp['hi'][2]) ^ (MOVE + C)).volume() for dy in np.arange(-6.5, 0.01, 0.25))
SM = T + LCD + LCDP + box(tp['lo'][0], tp['hi'][0], tp['lo'][1], tp['hi'][1], tp['lo'][2] + 0.05, tp['hi'][2])
STAT = C + MOVE + bat + off['speaker_15x11'] + off['ttp223_red_15x11'] + off['switch_rightangle_offboard']
st = max(((SM.translate([0, 0, dz]) ^ STAT).volume(), dz) for dz in np.arange(-40, 0.01, 0.5))
# stand insertion vs the LCD wires under the PCB (wires are attached to the LCD; check the rising stand body vs the under-PCB wire run)
st_w = max(((T.translate([0, 0, dz]) ^ ext(LCDW2D, ZB - 1.0, ZB)).volume(), dz) for dz in np.arange(-40, 0.01, 0.5))
R['assembly'] = dict(lift=[round(lift[0], 3), float(lift[1])], slide=[round(slide[0], 3), float(slide[1])], slide_min_gap_case=round(slide_gap_min, 2),
                     lipo_push=round(bat_push, 3), stand_insert=[round(st[0], 3), float(st[1])], stand_vs_lcd_wire_run=[round(st_w[0], 3), float(st_w[1])],
                     preexisting_stand_case=round((T ^ C).volume(), 3))
print('ASSEMBLY', R['assembly'])
json.dump(R, open(os.path.join(DOCS_FIT, 'pcb_v3', 'check_designer_v3.json'), 'w'), indent=1, default=float)
import pickle
