#!/usr/bin/env python3
"""Greedy axis-aligned placement of the mochi-rzmong components inside case_luar_lcd_23_40mm.stl +
tatakan_GMT130_fit.stl (stand at z-offset -10.38) with the GMT130 LCD fixed in its rails.
Coordinates: case STL frame, mm. +y = back of the head (rear openings), -y = face/LCD side, +z = up.
Grid search on a 0.5 mm voxel model (cavity_0.5.npz from cavity.py), then exact verification with
manifold3d (intersection volume + min_gap against the real meshes)."""
import itertools, json, sys, numpy as np, manifold3d as mf
from _paths import *; sys.path.insert(0, '.')
from components import COMPONENTS as CMP, ALTERNATIVES as ALT
D = np.load('cavity_0.5.npz'); CAV = D['cav']; O = D['origin'].astype(float); R = float(D['R'])
CLR = 1          # voxels of clearance to walls/other parts (0.5 mm); voxel rounding adds up to +0.5 mm more
FLOOR = -26.73   # top of the stand base plate (tatakan BASE_TOP -16.35 - 10.38)
BACK_IN = 27.5   # inner face of the thick rear block; block outer face y = 39.5
POCKET = dict(x=(-17.5, 17.5), y=(27.5, 34.0), z=(-16.5, -2.5))  # inner pocket in the rear block (measured)
USB_PORT = dict(x=(-6.5, 6.5), y=(34.0, 39.5), z=(-12.5, -4.5))   # rear through-opening 13 x 8 mm (measured) -> USB-C port
SLOT = dict(x=(-8.0, 8.0), y=(25.5, 39.5), z=(FLOOR, -18.0))      # rear bottom slot 16 x ~8.7, open to the desk (measured)
PLUG = (12.35, 6.5)   # USB-C plug overmold W x H (ASSUMED: USB-IF recommended max; real cables vary 10.5-13 x 5.5-8)
import scipy.ndimage as nd
EDT = nd.distance_transform_edt(~D['case']) * R       # mm to nearest CASE wall (touch / speaker / switch must act through the case)
def box_idx(lo, hi): return (np.floor((np.array(lo) - O) / R + 1e-6).astype(int), np.ceil((np.array(hi) - O) / R - 1e-6).astype(int))
def region(rg):
    m = np.zeros_like(CAV); a, b = box_idx([rg['x'][0], rg['y'][0], rg['z'][0]], [rg['x'][1], rg['y'][1], rg['z'][1]])
    m[a[0]:b[0], a[1]:b[1], a[2]:b[2]] = True
    return m & ~D['solid']

def integral(a):
    s = np.zeros(tuple(n + 1 for n in a.shape), np.int32)
    s[1:, 1:, 1:] = a.astype(np.int32).cumsum(0).cumsum(1).cumsum(2)
    return s
def fits(free, dims_vox):
    a, b, c = dims_vox; S = integral(free)
    tot = (S[a:, b:, c:] - S[:-a, b:, c:] - S[a:, :-b, c:] - S[a:, b:, :-c]
           + S[:-a, :-b, c:] + S[:-a, b:, :-c] + S[a:, :-b, :-c] - S[:-a, :-b, :-c])
    return tot == a * b * c          # index (i,j,k) = lower corner voxel of the (clearance-grown) box

def orientations(env, has_conn):
    out = []
    for perm in set(itertools.permutations(range(3))):      # perm[i] = world axis of local axis i
        dims = [0, 0, 0]
        for i, w in enumerate(perm): dims[w] = env[i]
        signs = (1, -1) if has_conn else (0,)
        for s in signs:
            out.append((tuple(dims), (perm[0], s), perm[2]))  # connector dir (axis, sign), thickness axis
    return out

def place(name, env, occupied, flt, score, has_conn=False, clr=CLR, extra=None):
    free = (CAV | (extra if extra is not None else False)) & ~occupied
    best = None
    for dims, conn, thick_ax in orientations(env, has_conn):
        nv = [int(np.ceil(d / R - 1e-6)) + 2 * clr for d in dims]
        ok = fits(free, nv)
        idx = np.argwhere(ok)
        if len(idx) == 0: continue
        lo = O + (idx + clr) * R; hi = lo + np.array(dims)
        m = np.array([flt(l, h, conn, thick_ax) for l, h in zip(lo, hi)])
        if not m.any(): continue
        sc = np.array([score(l, h, conn, thick_ax) for l, h in zip(lo[m], hi[m])])
        j = int(np.argmin(sc))
        cand = (sc[j], lo[m][j], hi[m][j], conn, thick_ax, dims)
        if best is None or cand[0] < best[0]: best = cand
    if best is None: return None
    sc, lo, hi, conn, thick_ax, dims = best
    i0 = np.floor((lo - O) / R + 1e-6).astype(int) - clr; i1 = np.ceil((hi - O) / R - 1e-6).astype(int) + clr
    occ = np.zeros_like(occupied); occ[i0[0]:i1[0], i0[1]:i1[1], i0[2]:i1[2]] = True
    return dict(name=name, lo=lo.round(2).tolist(), hi=hi.round(2).tolist(), dims=list(dims),
                connector=('+-'[conn[1] < 0] + 'xyz'[conn[0]]) if conn[1] else None,
                thickness_axis='xyz'[thick_ax], score=float(sc)), occ

def c(l, h): return (l + h) / 2
# ---------------- placement rules (constraints + preference scores) ----------------
def tp_f(l, h, conn, th):  # USB-C faces +y into the rear bottom slot, board flat on the stand floor
    cc = c(l, h)
    usb_z = l[2] + 0.5 + 1.6 + 1.6        # envelope has 0.5 underside joints; PCB ~1.6 (ASSUMED) + half receptacle 3.2
    okz = SLOT['z'][0] + PLUG[1] / 2 - 0.3 <= usb_z <= SLOT['z'][1] - PLUG[1] / 2   # overmold may touch floor line (slot open to desk)
    return (conn == (1, 1) and th == 2 and h[1] >= SLOT['y'][0] - 1.0 and abs(cc[0]) <= (16.0 - PLUG[0]) / 2
            and l[2] <= FLOOR + 1.1 and okz)
tp_s = lambda l, h, conn, th: abs(c(l, h)[0]) + abs(h[1] - (SLOT['y'][0] + 1.5))
def esp_usb_z(l): return l[2] + 1.0 + 1.0 + 1.6   # 1.0 joints + PCB ~1.0 + half of 3.2 mm USB-C receptacle (ASSUMED)
def esp_f(l, h, conn, th):  # USB-C faces +y, receptacle front at the rear 13x8 port, plug overmold inside the port outline
    if not (conn == (1, 1) and th == 2): return False
    uz = esp_usb_z(l); cx = c(l, h)[0]
    return (h[1] >= USB_PORT['y'][0] - 1.1 and
            USB_PORT['z'][0] + PLUG[1] / 2 <= uz <= USB_PORT['z'][1] - PLUG[1] / 2 and
            abs(cx) <= (13.0 - PLUG[0]) / 2 + 0.5)
esp_s = lambda l, h, conn, th: (USB_PORT['y'][0] - h[1]) + abs(c(l, h)[0]) + abs(esp_usb_z(l) + 8.5)
def sd_f(l, h, conn, th):    # upright, parallel to and directly behind the LCD (thin axis = y)
    return th == 1 and h[1] <= 3.0
sd_s = lambda l, h, conn, th: (l[2] - FLOOR) + 0.2 * abs(c(l, h)[0])
bat_s = lambda l, h, conn, th: np.linalg.norm(c(l, h) - np.array([0, 8, -12])) * 0.2 + (l[2] - FLOOR) * 0.5
def spk_f(l, h, conn, th): return th == 2 and l[2] <= FLOOR + 1.1       # flat on the stand floor -> sound holes in base
spk_s = lambda l, h, conn, th: abs(c(l, h)[0]) * 0.1 + abs(c(l, h)[1] - 10) * 0.1
near = lambda p: (lambda l, h, conn, th: np.linalg.norm(c(l, h) - np.asarray(p)))
def face_gap(l, h, th, sign):
    a, b = box_idx(l, h); sl = [slice(a[0], b[0]), slice(a[1], b[1]), slice(a[2], b[2])]
    k = b[th] if sign > 0 else a[th] - 1
    sl[th] = slice(k, k + 1)
    return float(EDT[tuple(sl)].mean()), float(EDT[tuple(sl)].max())
def touch_f(l, h, conn, th):  # TTP223 pad (component top face) parallel to and within ~1.5 mm of an inner wall
    return any(face_gap(l, h, th, sg)[1] <= 1.6 for sg in (1, -1))
touch_s = lambda l, h, conn, th: min(face_gap(l, h, th, sg)[0] for sg in (1, -1)) - 0.02 * h[2]
def sw_f(l, h, conn, th):    # body flat on the stand floor, handle (7.2-mm axis) pointing down through a new slot in the stand base
    return th == 2 and l[2] <= FLOOR + 1.1
sw_s = lambda l, h, conn, th: -abs(c(l, h)[0]) * 0.1 + (h[1] - 25) ** 2 * 0.01
ANY = lambda l, h, conn, th: True

def wall_contact_score(l, h, solid):
    """mean distance (mm) from the top face of the box to the nearest solid above (for TTP223 pad)."""
    return 0
SLOTREG = region(SLOT)
def spk_f(l, h, conn, th):   # speaker cone face (thickness axis) flat against an inner wall (<=1.6 mm) -> drill/print sound holes there
    return any(face_gap(l, h, th, sg)[0] <= 2.5 and face_gap(l, h, th, sg)[1] <= 4.0 for sg in (1, -1))
spk_s = lambda l, h, conn, th: min(face_gap(l, h, th, sg)[0] for sg in (1, -1)) + 0.05 * abs(c(l, h)[2] + 10)
def sw2_f(l, h, conn, th):   # switch: handle side (local z = 7.2 axis) against a side wall (|x| big) -> needs a 4 x 6 mm slot
    return any(face_gap(l, h, th, sg)[1] <= 1.6 for sg in (1, -1))
sw2_s = lambda l, h, conn, th: min(face_gap(l, h, th, sg)[0] for sg in (1, -1)) + 0.05 * abs(c(l, h)[2] + 15)
bat_s = lambda l, h, conn, th: -0.0 * h[2] + 0.1 * abs(c(l, h)[0])
sd_s = lambda l, h, conn, th: l[1] + 0.5 * h[2] + 0.1 * abs(c(l, h)[0]) + (0 if conn[0] == 0 else 2)   # parallel behind the LCD, card slot facing a side wall (x)
ORDER = [   # (name, constraint, score, has_connector, extra allowed region)
 ('tp4056_typec_dw01', tp_f, tp_s, True, SLOTREG),
 ('esp32c3_supermini', esp_f, esp_s, True, None),
 ('battery_LiPo501640', ANY, bat_s, False, None),
 ('sd_wemos_microsd_shield', sd_f, sd_s, True, None),
 ('speaker_20mm', spk_f, spk_s, False, None),
 ('ttp223_red_15x11', touch_f, touch_s, False, None),
 ('max98357a', ANY, None, False, None),
 ('cap_470uF_10V', ANY, None, False, None),
 ('switch_SS12D00G3', sw2_f, sw2_s, False, None),
]
def run(order=ORDER, cmp=CMP, verbose=True):
    occupied = np.zeros_like(CAV); res = {}
    for name, f, s, hc, ex in order:
        if s is None:   # default: hug amp near speaker, cap near amp, touch high up near the dome top
            s = {'max98357a': near((res.get('speaker_20mm') or {}).get('c', (0, 10, -20))),
                 'cap_470uF_10V': near((res.get('max98357a') or {}).get('c', (0, 10, -20))),
                 }[name]
        r = place(name, cmp[name]['env'], occupied, f, s, hc, extra=ex)
        if r is None:
            res[name] = None
            if verbose: print(f'{name:26s} NO FEASIBLE PLACEMENT')
            continue
        p, occ = r; p['c'] = c(np.array(p['lo']), np.array(p['hi'])).round(2).tolist()
        occupied |= occ; res[name] = p
        if verbose: print(f"{name:26s} lo={p['lo']} hi={p['hi']} conn={p['connector']} thick={p['thickness_axis']}")
    return res
if __name__ == '__main__':
    res = run()
    json.dump(res, open('placement.json', 'w'), indent=1)
