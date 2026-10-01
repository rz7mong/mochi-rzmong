"""Render deliverables for Mochi carrier v3 (case frame, mm)."""
import json, math, os, cairosvg
from shapely.geometry import Polygon, Point
import layout_v3 as L
from geom_v3 import TRACES, build_pour, polys, pad_shape

OUT = os.path.dirname(os.path.abspath(__file__)) + os.sep
pour = build_pour()
pads_by = {p["name"]: p for p in L.pads}
NETCOL = {"VIN": "#d62728", "GND": "#2ca02c", "3V3": "#ff7f0e", "G4": "#1f77b4", "G6": "#9467bd", "G0": "#8c564b",
          "G10": "#e377c2", "G3": "#17becf", "G5": "#bcbd22", "G21": "#7f7f7f", "G20": "#393b79", "G8": "#637939", "G1": "#843c39"}

# module footprints (top side) in case frame
MAXC = L.MAXX["GAIN"]; SDC = L.S0 + 2.54 * 2.5
MODS = [
    ("U1 ESP32-C3 Super Mini, flat on 2.5 mm header", (-9, 10, 9, 32.5), "#4a90d9"),
    ("USB-C (front y 34)", (-4.5, 26.6, 4.5, 34.0), "#4a90d9"),
    ("J3 MAX98357A on edge", (MAXC - 8.9, 4.3, MAXC + 8.9, 8.3), "#c0392b"),
    ("J2 micro-SD 6p on edge", (SDC - 9.25, 4.3, SDC + 9.25, 9.3), "#8e44ad"),
    ("M2 nut", (-16.8, -1.8, -12.2, 2.8), "#555"), ("M2 nut", (12.2, -1.8, 16.8, 2.8), "#555"),
]
SWITCH_BOX = (7.2, 29, 15.8, 33.7)

def ring_path(coords, T):
    pts = [T(x, y) for x, y in coords]
    return "M" + " L".join(f"{a:.3f},{b:.3f}" for a, b in pts) + " Z"
def geom_path(g, T):
    d = ""
    for pg in polys(g):
        d += ring_path(list(pg.exterior.coords), T)
        for i in pg.interiors: d += ring_path(list(i.coords), T)
    return d
def poly_line(pts, T): return " ".join(f"{a:.3f},{b:.3f}" for a, b in (T(x, y) for x, y in pts))
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

XMIN, XMAX, YMIN, YMAX = -19.5, 19.0, -2.5, 34.0

# ---------------------------------------------------------------- copper mirrored 1:1
def copper_svg():
    M = 6.0  # margin mm
    W = (XMAX - XMIN) + 2 * M; H = (YMAX - YMIN) + 2 * M + 10
    T = lambda x, y: ((XMAX - x) + M, (YMAX - y) + M)     # mirrored in x (seen from copper side), +y (rear) at top
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" height="{H:.2f}mm" viewBox="0 0 {W:.2f} {H:.2f}">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<path d="{ring_path(L.OUTLINE, T)}" fill="none" stroke="black" stroke-width="0.15" stroke-dasharray="0.8,0.4"/>',
         f'<path d="{geom_path(pour, T)}" fill="black" fill-rule="evenodd"/>']
    for t in TRACES:
        s.append(f'<polyline points="{poly_line(t[2], T)}" fill="none" stroke="black" stroke-width="{t[1]}" stroke-linecap="round" stroke-linejoin="round"/>')
    for p in L.pads:
        x, y = T(p["x"], p["y"]); s.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{p["d"]/2}" fill="black"/>')
    for p in L.pads:
        x, y = T(p["x"], p["y"]); s.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{p["hole"]/2 - 0.1}" fill="white"/>')
    for hx, hy in L.HOLES:
        x, y = T(hx, hy); s.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{L.HOLE_D/2}" fill="white" stroke="black" stroke-width="0.15"/>')
        s.append(f'<line x1="{x-0.6}" y1="{y}" x2="{x+0.6}" y2="{y}" stroke="black" stroke-width="0.1"/><line x1="{x}" y1="{y-0.6}" x2="{x}" y2="{y+0.6}" stroke="black" stroke-width="0.1"/>')
    # scale bar
    bx, by = M, H - 7
    s.append(f'<rect x="{bx}" y="{by}" width="10" height="1.2" fill="black"/>')
    for k in range(11): s.append(f'<line x1="{bx+k}" y1="{by-0.6 if k % 5 == 0 else by-0.3}" x2="{bx+k}" y2="{by}" stroke="black" stroke-width="0.1"/>')
    s.append(f'<text x="{bx+11}" y="{by+1.1}" font-family="sans-serif" font-size="1.6">10 mm - verify 1:1 before transfer</text>')
    s.append(f'<text x="{M}" y="3.2" font-family="sans-serif" font-size="1.5">Mochi carrier v3 - COPPER SIDE (mirrored), 1:1, black=copper</text>')
    s.append(f'<text x="{M}" y="{H-3.6}" font-family="sans-serif" font-size="1.1">rear/USB at top. Drill 0.9; J1 RES/SCL + GND x2: 1.1; M2 holes 2.2.</text>')
    s.append(f'<text x="{M}" y="{H-2.0}" font-family="sans-serif" font-size="1.1">Dashed = cut line (38.5 x 36). JP3/JP4 bottom wires not shown.</text>')
    s.append("</svg>")
    open(OUT + "copper_mirrored_1to1.svg", "w").write("\n".join(s))
    cairosvg.svg2pdf(url=OUT + "copper_mirrored_1to1.svg", write_to=OUT + "copper_mirrored_1to1.pdf")

# ---------------------------------------------------------------- component-side preview / case frame
def preview_svg(case_frame=False):
    S = 1.0 if case_frame else 16.0     # case frame file: 1 user unit = 1 mm
    M = 8 if not case_frame else 10
    W = (XMAX - XMIN) + 2 * M; H = (YMAX - YMIN) + 2 * M + (8.5 if not case_frame else 4)
    T = lambda x, y: ((x - XMIN) + M, (YMAX - y) + M)   # top view: x right, +y (rear) up
    fs = 1.1 if case_frame else 1.0
    out = []
    A = out.append
    if case_frame:
        # explicit case transform: group in case coords (x, y) with y flipped
        A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.1f}mm" height="{H:.1f}mm" viewBox="0 0 {W:.2f} {H:.2f}">')
    else:
        A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*S:.0f}" height="{H*S:.0f}" viewBox="0 0 {W:.2f} {H:.2f}">')
    A(f'<rect width="{W}" height="{H}" fill="white"/>')
    # grid
    for gx in range(-20, 21, 2):
        x, _ = T(gx, 0); A(f'<line x1="{x}" y1="{M-1}" x2="{x}" y2="{T(0, YMIN)[1]+1}" stroke="#eee" stroke-width="0.05"/>')
        A(f'<text x="{x}" y="{M-1.5}" font-size="0.9" text-anchor="middle" fill="#999" font-family="sans-serif">{gx}</text>')
    for gy in range(-2, 35, 2):
        _, y = T(0, gy); A(f'<line x1="{M-1}" y1="{y}" x2="{W-M+1}" y2="{y}" stroke="#eee" stroke-width="0.05"/>')
        A(f'<text x="{M-1.5}" y="{y+0.3}" font-size="0.9" text-anchor="end" fill="#999" font-family="sans-serif">{gy}</text>')
    A(f'<path id="outline_v2" d="{ring_path(L.OUTLINE, T)}" fill="#f6efd9" stroke="#2a7a2a" stroke-width="0.2"/>')
    # zones
    x0, y0, x1, y1 = L.NO_PAD_ZONE; a = T(x0, y1); b = T(x1, y0)
    A(f'<rect id="no_joint_strip" x="{a[0]}" y="{a[1]}" width="{b[0]-a[0]}" height="{b[1]-a[1]}" fill="#ff0000" fill-opacity="0.06" stroke="#c00" stroke-width="0.08" stroke-dasharray="0.5,0.3"/>')
    A(f'<text x="{a[0]+0.2}" y="{a[1]+1.2}" font-size="0.7" fill="#c00" font-family="sans-serif">no bottom joints</text>')
    a = T(7.2, 33.7); b = T(9.5, 29)
    A(f'<rect id="h52_zone" x="{a[0]}" y="{a[1]}" width="{b[0]-a[0]}" height="{b[1]-a[1]}" fill="#ffa500" fill-opacity="0.2" stroke="#e67e00" stroke-width="0.08"/>')
    a = T(SWITCH_BOX[0], SWITCH_BOX[3]); b = T(SWITCH_BOX[2], SWITCH_BOX[1])
    A(f'<rect id="switch_offboard" x="{a[0]}" y="{a[1]}" width="{b[0]-a[0]}" height="{b[1]-a[1]}" fill="none" stroke="#e67e00" stroke-width="0.08" stroke-dasharray="0.4,0.3"/>')
    A(f'<text x="{a[0]+0.3}" y="{a[1]+1.3}" font-size="0.7" fill="#e67e00" font-family="sans-serif">switch (off-board, z -7.9..-4.2)</text>')
    A(f'<text x="{a[0]+0.3}" y="{a[1]+2.2}" font-size="0.7" fill="#e67e00" font-family="sans-serif">5.2 mm max x7.2..9.5</text>')
    # copper (semi transparent, seen through board)
    A(f'<path id="gnd_pour" d="{geom_path(pour, T)}" fill="{NETCOL["GND"]}" fill-opacity="0.18" fill-rule="evenodd"/>')
    for t in TRACES:
        A(f'<polyline class="trace net-{t[0]}" points="{poly_line(t[2], T)}" fill="none" stroke="{NETCOL[t[0]]}" stroke-opacity="0.55" stroke-width="{t[1]}" stroke-linecap="round" stroke-linejoin="round"/>')
    # holes + keepouts
    for hx, hy in L.HOLES:
        x, y = T(hx, hy)
        A(f'<circle cx="{x}" cy="{y}" r="{L.HOLE_PART_KEEPOUT}" fill="none" stroke="#c00" stroke-width="0.08" stroke-dasharray="0.4,0.3"/>')
        A(f'<circle cx="{x}" cy="{y}" r="{L.HOLE_D/2}" fill="white" stroke="black" stroke-width="0.12"/>')
        A(f'<text x="{x}" y="{y+3.6}" font-size="0.75" text-anchor="middle" font-family="sans-serif">M2 ({hx},{hy}) 4.5 keepout</text>')
    x, y = T(*L.REST_PAD); A(f'<circle id="rest_pad" cx="{x}" cy="{y}" r="2" fill="#0000ff" fill-opacity="0.06" stroke="#00f" stroke-width="0.08" stroke-dasharray="0.3,0.2"/>')
    A(f'<text x="{x}" y="{y+0.25}" font-size="0.7" text-anchor="middle" fill="#00f" font-family="sans-serif">rest pad</text>')
    # module outlines
    for name, (a0, b0, a1, b1), col in MODS:
        p = T(a0, b1); q = T(a1, b0)
        A(f'<rect class="module" x="{p[0]:.3f}" y="{p[1]:.3f}" width="{q[0]-p[0]:.3f}" height="{q[1]-p[1]:.3f}" fill="{col}" fill-opacity="0.07" stroke="{col}" stroke-width="0.15"/>')
        if "nut" not in name:
            ty = q[1] - 0.5 if "ESP" in name else (p[1] + 0.9)
            if "USB" in name: ty = p[1] - 0.3
            A(f'<text x="{(p[0]+q[0])/2:.3f}" y="{ty:.3f}" font-size="{0.8 if "USB" in name else 0.85}" text-anchor="middle" fill="{col}" font-family="sans-serif">{esc(name)}</text>')
    cx, cy = T(*L.CAP_C)
    A(f'<circle id="C1" cx="{cx}" cy="{cy}" r="{L.CAP_D/2}" fill="#333" fill-opacity="0.08" stroke="#333" stroke-width="0.15"/>')
    A(f'<text x="{cx}" y="{cy+0.25}" font-size="0.7" text-anchor="middle" font-family="sans-serif" font-weight="bold">C1</text>')
    A(f'<text x="{cx-3.4}" y="{cy+0.25}" font-size="0.6" text-anchor="end" font-family="sans-serif">470uF</text>')
    # omitted pins
    for x0_, y0_, n in L.OMIT_POS + L.MAX_OMIT:
        x, y = T(x0_, y0_)
        A(f'<circle cx="{x}" cy="{y}" r="1.0" fill="none" stroke="#999" stroke-width="0.1" stroke-dasharray="0.3,0.2"/>')
        A(f'<text x="{x}" y="{y+0.3}" font-size="0.65" text-anchor="middle" fill="#888" font-family="sans-serif">{n} cut</text>')
    # pads
    for p in L.pads:
        x, y = T(p["x"], p["y"])
        A(f'<circle class="pad" id="{p["name"]}" cx="{x:.3f}" cy="{y:.3f}" r="{p["d"]/2}" fill="#d4a017" stroke="{NETCOL[p["net"]]}" stroke-width="0.25"/>')
        A(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{p["hole"]/2}" fill="white"/>')
        lab = p["label"] if p["name"].startswith(("U1", "J")) and not p["name"].startswith("JP") else p["label"]
        dy = -1.55
        if p["name"].startswith("J1."): dy = 2.1
        if p["name"].startswith(("J2.", "J3.")): dy = 2.0
        A(f'<text x="{x:.3f}" y="{y+dy:.3f}" font-size="0.75" text-anchor="middle" font-family="sans-serif" font-weight="bold">{esc(lab)}</text>')
        if p["name"].startswith("U1."):
            A(f'<text x="{x:.3f}" y="{y+0.27:.3f}" font-size="0.55" text-anchor="middle" fill="{NETCOL[p["net"]]}" font-family="sans-serif">{p["net"]}</text>')
    # jumpers
    for n, net, a_, b_ in L.JUMPERS:
        side, path = L.JUMPER_PATH[n]
        col = "black" if side == "top" else "#0057d9"
        A(f'<polyline class="jumper {side}" id="{n}" points="{poly_line(path, T)}" fill="none" stroke="{col}" stroke-width="{0.2 if side == "top" else 0.15}" stroke-dasharray="{"0.8,0.4" if side == "top" else "0.4,0.25"}" stroke-linejoin="round"/>')
        k = {"JP1": 2, "JP2": 1, "JP3": 1, "JP4": 2}[n]
        mx, my = T(*path[k])
        dx = {"JP1": -0.6, "JP2": 0.4, "JP3": 0.6, "JP4": 0.4}[n]; dy = {"JP1": -0.4, "JP2": 1.0, "JP3": 1.1, "JP4": -0.4}[n]
        A(f'<text x="{mx+dx}" y="{my+dy}" font-size="0.75" font-family="sans-serif" fill="{col}" font-weight="bold" text-anchor="{"end" if n == "JP1" else "start"}">{n} {net}{"" if side == "top" else " (bottom)"}</text>')
    # group labels
    for txt, x0_, y0_ in [("J1 LCD wire row (to ST7789 GMT130)", L.S0 + 1.0, -2.0), ("front / LCD side (-y)", 0, -3.6), ("rear / USB-C (+y)", 0, 35.0)]:
        x, y = T(x0_, y0_); A(f'<text x="{x}" y="{y}" font-size="0.9" text-anchor="middle" font-family="sans-serif" font-style="italic">{txt}</text>')
    x, y = T(-17.6, 10.6); A(f'<text x="{x}" y="{y}" font-size="0.6" font-family="sans-serif" fill="#555">off-board wires</text>')
    # dims
    a = T(XMIN, -2.5); b = T(XMAX, -2.5)
    A(f'<line x1="{a[0]}" y1="{a[1]+4.5}" x2="{b[0]}" y2="{b[1]+4.5}" stroke="black" stroke-width="0.08"/>')
    A(f'<text x="{(a[0]+b[0])/2}" y="{a[1]+5.6}" font-size="0.9" text-anchor="middle" font-family="sans-serif">38.5 mm (x -19.5..19)</text>')
    a = T(19.0, -2.5); b = T(19.0, 33.5)
    A(f'<line x1="{a[0]+3}" y1="{a[1]}" x2="{b[0]+3}" y2="{b[1]}" stroke="black" stroke-width="0.08"/>')
    A(f'<text x="{a[0]+3.6}" y="{(a[1]+b[1])/2}" font-size="0.9" font-family="sans-serif" transform="rotate(90 {a[0]+3.6} {(a[1]+b[1])/2})" text-anchor="middle">36 mm (y -2.5..33.5)</text>')
    if not case_frame:
        legend = ["COMPONENT SIDE (top) view, case frame mm. Copper is on the BOTTOM, shown see-through.",
                  "Black dashed = top jumpers JP1/JP2 (under the ESP via cut IO7/IO9 slots; fit before ESP, JP1 before C1).",
                  "Blue dashed = JP3/JP4 thin insulated wire on the COPPER side (under board, through MAX/SD joint gap).",
                  "Grey dashed = header pins cut off (IO2, IO7, IO9, MAX SD, MAX GAIN). Red dashed = M2 4.5 mm keepout.",
                  "Off-board pads: SW out(VIN), GND x2 (TTP GND + TP4056 OUT-), TTP OUT(G1). TTP 3V3 from J1 BLK/VCC. Speaker -> MAX terminals.",
                  "C1 470uF 10V D6.3x11 upright, leads 3.5 mm. 1.1 mm holes: J1 RES/SCL, GND x2. Trim rear-tab + U1.3V3 joints to <=1.0 mm."]
        for k, l in enumerate(legend):
            A(f'<text x="{M-6}" y="{H-7.4+k*1.2}" font-size="0.8" font-family="sans-serif">{esc(l)}</text>')
    else:
        A(f'<text x="{M}" y="{H-2}" font-size="1" font-family="sans-serif">Case STL frame, 1 unit = 1 mm, top view; svg_x = x + {M - XMIN}, svg_y = {YMAX + M} - y. Pad ids = netlist names.</text>')
    A("</svg>")
    return "\n".join(out)

copper_svg()
svg = preview_svg(False)
open(OUT + "preview_component_side.svg", "w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to=OUT + "preview_component_side.png", output_width=1400)
open(OUT + "layout_case_frame.svg", "w").write(preview_svg(True))
cairosvg.svg2png(url=OUT + "copper_mirrored_1to1.svg", write_to=OUT + "copper_check.png", output_width=900)
print("ok")
