import json, sys, time
import numpy as np
from scipy.ndimage import distance_transform_edt
import layout_v3 as L
from router import Grid, astar, simplify

G = Grid(L.OUTLINE, res=0.1)
traces = [list(t) for t in L.FIXED]

def net_copper(net, extra_r=0.0, exclude_net=None):
    m = np.zeros(G.X.shape, bool)
    for p in L.pads:
        if (p["net"] == net) != (exclude_net is not None):
            if exclude_net is None or p["net"] != exclude_net: m |= G.disk(p["x"], p["y"], p["d"] / 2 + extra_r)
    for t in traces:
        if (t[0] == net) != (exclude_net is not None):
            if exclude_net is None or t[0] != exclude_net:
                for a, b in zip(t[2][:-1], t[2][1:]): m |= G.seg(a, b, t[1] / 2 + extra_r)
    return m

def other_copper(net):
    m = np.zeros(G.X.shape, bool)
    for p in L.pads:
        if p["net"] != net: m |= G.disk(p["x"], p["y"], p["d"] / 2)
    for t in traces:
        if t[0] != net:
            for a, b in zip(t[2][:-1], t[2][1:]): m |= G.seg(a, b, t[1] / 2)
    return m

def own_copper(net):
    m = np.zeros(G.X.shape, bool)
    for p in L.pads:
        if p["net"] == net: pass
    for t in traces:
        if t[0] == net:
            for a, b in zip(t[2][:-1], t[2][1:]): m |= G.seg(a, b, t[1] / 2)
    return m

failed = []
for job in L.JOBS:
    net, w, plist = job[:3]; use_fixed = job[3] if len(job) > 3 else True
    t0 = time.time()
    oc = other_copper(net)
    d_other = distance_transform_edt(~oc) * G.res
    blocked = (d_other < w / 2 + L.CLEAR + 0.1) | (G.dist_out < w / 2 + L.EDGE_CLEAR + 0.06)
    for hx, hy in L.HOLES: blocked |= G.disk(hx, hy, L.HOLE_TRACE_KEEPOUT + w / 2)
    pads_by = {p["name"]: p for p in L.pads}
    tree = own_copper(net) if use_fixed else np.zeros(G.X.shape, bool)
    # existing traces of this net count as tree; if none, start from first pad
    plist = list(plist)
    if not tree.any():
        p = pads_by[plist.pop(0)]; tree = G.disk(p["x"], p["y"], 0.35)
    for pn in plist:
        p = pads_by[pn]
        goal = G.disk(p["x"], p["y"], 0.35)
        start = tree & ~blocked
        # allow starting from tree cells even if inside own pad halo
        start = tree.copy()
        path = astar(G, blocked & ~tree & ~goal, start, goal)
        if path is None:
            failed.append((net, pn)); print(f"  FAIL {net} -> {pn}"); continue
        pts = simplify([G.xy(i, j) for i, j in path])
        pts = [(round(x, 2), round(y, 2)) for x, y in pts]
        pts[-1] = (p["x"], p["y"])
        traces.append([net, w, pts])
        for a, b in zip(pts[:-1], pts[1:]): tree |= G.seg(a, b, w / 2)
        tree |= G.disk(p["x"], p["y"], 0.35)
    print(f"{net:6s} routed {len(plist)} in {time.time()-t0:.1f}s")
json.dump(dict(traces=traces, failed=failed), open("routed.json", "w"), indent=1)
print("FAILED:", failed)
