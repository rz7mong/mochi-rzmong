import json, os
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union
import layout_v3 as L

R = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "routed.json")))
TRACES = [tuple(t) for t in R["traces"]]
BOARD = Polygon(L.OUTLINE).buffer(0)

def pad_shape(p):  return Point(p["x"], p["y"]).buffer(p["d"] / 2, 64)
def trace_shape(t): return LineString(t[2]).buffer(t[1] / 2, 32)
def polys(g):
    if g.is_empty: return []
    return list(g.geoms) if hasattr(g, "geoms") else [g]

_pour = None
def build_pour(min_width=1.0):
    global _pour
    if _pour is not None: return _pour
    other = [pad_shape(p) for p in L.pads if p["net"] != "GND"] + \
            [trace_shape(t) for t in TRACES if t[0] != "GND"]
    keepout = unary_union(other).buffer(L.CLEAR + 0.2, 32)        # pour gets 1.0 mm clearance (hand etch)
    holes = unary_union([Point(h).buffer(L.HOLE_TRACE_KEEPOUT, 64) for h in L.HOLES])
    area = BOARD.buffer(-(L.EDGE_CLEAR + 0.3), join_style=2).difference(keepout).difference(holes)
    area = area.buffer(-min_width / 2, 16).buffer(min_width / 2, 16)
    gnd_cu = unary_union([pad_shape(p) for p in L.pads if p["net"] == "GND"] +
                         [trace_shape(t) for t in TRACES if t[0] == "GND"])
    keep = [g for g in polys(area) if g.buffer(0.01).intersects(gnd_cu) and g.area > 4]
    _pour = unary_union(keep)
    return _pour

def copper_by_net(with_pour=True):
    nets = {}
    for p in L.pads:   nets.setdefault(p["net"], []).append(pad_shape(p))
    for t in TRACES:   nets.setdefault(t[0], []).append(trace_shape(t))
    if with_pour: nets["GND"].append(build_pour())
    return {n: unary_union(v) for n, v in nets.items()}
