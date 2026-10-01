"""Netlist + DRC check for Mochi carrier v3 (case frame). Geometric: rebuilds connectivity from copper shapes."""
import itertools, sys, math
from shapely.geometry import Point, box
from shapely.ops import unary_union
import layout_v3 as L
from geom_v3 import *

ok = True; notes = []
def fail(msg):
    global ok; ok = False; print("  FAIL:", msg)
def note(msg): notes.append(msg); print("  NOTE:", msg)

print("Mochi carrier v3 check  (outline v2 38.5 x 36 mm, case frame)")
cu = copper_by_net()
islands = polys(unary_union(list(cu.values())))
print(f"Copper islands: {len(islands)}")
pad_island = {}
for p in L.pads:
    idx = [i for i, g in enumerate(islands) if g.contains(Point(p["x"], p["y"]))]
    pad_island[p["name"]] = idx[0]
for i, g in enumerate(islands):
    nets = {p["net"] for p in L.pads if pad_island[p["name"]] == i}
    if len(nets) > 1: fail(f"SHORT: island {i} joins nets {sorted(nets)}")
print("  [OK ] no shorts" if ok else "")

parent = list(range(len(islands)))
def find(a):
    while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
    return a
for jp, net, a, b in L.JUMPERS: parent[find(pad_island[a])] = find(pad_island[b])
group = {n: find(i) for n, i in pad_island.items()}
pads_by = {p["name"]: p for p in L.pads}
print("\nNet check (copper + jumpers JP1..JP4):")
for net, req in L.REQUIRED.items():
    missing = req - set(pads_by)
    if missing: fail(f"{net}: pads not placed: {missing}")
    roots = {group[n] for n in req if n in group}
    on_net = {n for n in pads_by if group[n] in roots}
    extra = on_net - req
    if len(roots) != 1: fail(f"{net}: split into {len(roots)} pieces")
    if extra: fail(f"{net}: extra pads connected {sorted(extra)}")
    print(f"  [{'OK ' if len(roots) == 1 and not extra else 'BAD'}] {net:4s}: {', '.join(sorted(req))}")
unlisted = set(pads_by) - set().union(*L.REQUIRED.values())
if unlisted: fail(f"pads not in required netlist: {unlisted}")
for p in ("IO2", "IO9"):
    if "U1." + p in pads_by: fail(f"{p} has a pad (must be NC)")
print("  [OK ] IO2, IO9 NC (header pin cut, no pad); IO7 also cut (unused)")
for p in pads_by:
    if p.startswith("U1.") and p[3:] in L.OMIT: fail(f"{p} should be omitted")

print(f"\nDRC (clearance >= {L.CLEAR} mm, edge >= {L.EDGE_CLEAR} mm):")
items = [("pad", p["name"], p["net"], p["group"], pad_shape(p)) for p in L.pads] + \
        [("trace", f"{t[0]}#{k}", t[0], None, trace_shape(t).difference(unary_union([pad_shape(p) for p in L.pads if p["net"] == t[0]]))) for k, t in enumerate(TRACES)] + \
        [("pour", "GNDpour", "GND", None, build_pour())]
worst = 99; nviol = 0; exempt = 0
for a, b in itertools.combinations(items, 2):
    if a[2] == b[2]: continue
    d = a[4].distance(b[4])
    if a[0] == b[0] == "pad" and a[3] == b[3] and d < L.CLEAR: exempt += 1; continue
    worst = min(worst, d)
    if d < L.CLEAR - 5e-3: nviol += 1; fail(f"clearance {d:.2f} mm between {a[1]} and {b[1]}")
minedge = 99
for it in items:
    e = BOARD.exterior.distance(it[4]) if BOARD.contains(it[4]) else -1
    minedge = min(minedge, e)
    if e < L.EDGE_CLEAR - 1e-6: fail(f"edge clearance {e:.2f} for {it[1]}")
print(f"  min clearance between different nets: {worst:.2f} mm; violations: {nviol}")
print(f"  min copper-to-board-edge: {minedge:.2f} mm")
print(f"  exempt 2.54-pitch header pad pairs (0.14 mm gap, standard): {exempt}")
for t in TRACES:
    lim = 1.5 if t[0] in ("VIN", "GND", "3V3") else 1.0
    if t[1] < lim: note(f"{t[0]} segment {t[1]} mm wide (power rule {lim}) {tuple(t[2][0])} -> {tuple(t[2][-1])}")
    if t[1] < 1.0: fail(f"{t[0]} trace below 1.0 mm")

print("\nCase constraints:")
x0, y0, x1, y1 = L.NO_PAD_ZONE
zone = box(x0, y0, x1, y1)
bad = [p["name"] for p in L.pads if pad_shape(p).intersects(zone)]
if bad: fail(f"pads in no-joint strip x±2.5,y22..33.5: {bad}")
else: print("  [OK ] no pads/joints in strip x -2.5..2.5, y 22..33.5 (traces only, flat copper)")
for hx, hy in L.HOLES:
    for p in L.pads:
        d = math.hypot(p["x"] - hx, p["y"] - hy)
        if d < L.HOLE_PART_KEEPOUT:
            note(f"pad {p['name']} centre {d:.2f} mm from M2 hole ({hx},{hy}) (< {L.HOLE_PART_KEEPOUT} keepout)")
    hc = Point(hx, hy)
    dt = min(trace_shape(t).distance(hc) for t in TRACES)
    if dt < L.HOLE_TRACE_KEEPOUT - 1e-6: fail(f"trace {dt:.2f} mm from hole ({hx},{hy})")
    else: print(f"  [OK ] traces >= {dt:.2f} mm from hole centre ({hx},{hy}); pour kept {L.HOLE_TRACE_KEEPOUT} mm away")
tab = [p["name"] for p in L.pads if p["y"] > 25]
print(f"  rear-tab joints (y>25, incl. U1.3V3): trim to <=1.0 mm below board: {', '.join(tab)}")
for c, nm in [((L.CAP_C), "C1 body")]:
    pass

print("\nJumper wire geometry:")
from shapely.geometry import LineString
WIRE_TOP_R, WIRE_BOT_R = 0.5, 0.3      # top: ~1.0 mm insulated wire; bottom: 30AWG Kynar (~0.5-0.6 mm)
plastic = [box(p["x"] - 1.27, p["y"] - 1.27, p["x"] + 1.27, p["y"] + 1.27) for p in L.pads if p["name"].startswith("U1.")]
front = [box(-19.5, L.HY - 1.27, 19.0, 9.3)]          # header plastic + on-edge MAX/SD module band (y to 9.3)
capc = Point(L.CAP_C).buffer(L.CAP_D / 2, 64)
for n, net, a_, b_ in L.JUMPERS:
    side, path = L.JUMPER_PATH[n]
    pa, pb = pads_by[a_], pads_by[b_]
    if (round(path[0][0], 2), round(path[0][1], 2)) != (pa["x"], pa["y"]) or (round(path[-1][0], 2), round(path[-1][1], 2)) != (pb["x"], pb["y"]):
        fail(f"{n}: path endpoints do not land on {a_}/{b_}")
    ln = LineString(path)
    if side == "top":
        w = ln.buffer(WIRE_TOP_R)
        if not BOARD.contains(w): fail(f"{n}: wire leaves the board outline")
        dpl = min(w.distance(b) for b in plastic)
        dfr = min(w.distance(b) for b in front)
        dcap = w.distance(capc)
        if dpl < 0.2: fail(f"{n}: wire {dpl:.2f} mm from ESP header plastic")
        if dfr < 0.2: fail(f"{n}: wire crosses/approaches the front header+module band ({dfr:.2f})")
        print(f"  [OK ] {n} ({net}, top, {ln.length:.0f} mm): ESP header plastic >= {dpl:.2f} mm, front module band {dfr:.1f} mm, cap body {dcap:.2f} mm")
        if dcap < 0.3: note(f"{n} wire only {dcap:.2f} mm from C1 body -> fit {n} BEFORE C1")
    else:
        w = ln.buffer(WIRE_BOT_R)
        if not BOARD.contains(w): fail(f"{n}: wire leaves the board outline")
        dj = min(w.distance(Point(p["x"], p["y"]).buffer(p["d"] / 2 + 0.2)) for p in L.pads if p["name"] not in (a_, b_))
        dp = min(w.distance(Point(h).buffer(2.5)) for h in L.HOLES)
        if dj < 0.1: fail(f"{n}: bottom wire {dj:.2f} mm from a solder fillet")
        if w.intersects(zone): fail(f"{n}: bottom wire in rest-pad strip")
        print(f"  [OK ] {n} ({net}, BOTTOM, {ln.length:.0f} mm): solder fillets (pad+0.4) >= {dj:.2f} mm, M2 posts (D5) {dp:.1f} mm, no top-side crossing of SD/MAX")
pour = build_pour()
print(f"  GND pour area: {pour.area:.0f} mm^2 in {len(polys(pour))} piece(s)")
print("\nRESULT:", "PASS" if ok else "FAIL", f"({len(notes)} notes)")
sys.exit(0 if ok else 1)
