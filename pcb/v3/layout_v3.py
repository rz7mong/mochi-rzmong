"""Mochi carrier PCB v3 - DRAFT, case coordinate frame (mm). -y = LCD/front, +y = rear (USB-C).
Viewed from COMPONENT side (top, +z). Single-sided: copper on bottom. All THT."""
import json, os
OUTLINE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outline", "pcb_recommended_outline_v2.json")))["outline"]
HOLES = [(-14.5, 0.5), (14.5, 0.5)]; HOLE_D = 2.2
HOLE_TRACE_KEEPOUT = 3.0      # copper keep-away radius around M2 holes (post O5 under board)
HOLE_PART_KEEPOUT = 4.5       # no parts/pads (top) within this radius (per case designer)
NO_PAD_ZONE = (-2.5, 22.0, 2.5, 33.5)   # rest-pad strip: no solder joints on bottom
REST_PAD = (0.0, 30.5)
PAD_D, HOLE_PAD_D = 2.4, 0.9
CLEAR, EDGE_CLEAR = 0.8, 0.5

# ---- ESP32-C3 Super Mini, flat, USB-C to rear (+y), centred x=0, module box (-9,10)-(9,32.5)
# Top view with USB up (+y): left column (x=-7.62) = IO5,IO6,IO7,IO8,IO9,IO10,IO20,IO21 (rear->front)
#                            right column (x=+7.62) = 5V,GND,3V3,IO4,IO3,IO2,IO1,IO0 (rear->front)
# (sigmdel/supermini_esp32c3_sketches pinout_top image; rows 15.24 mm apart; pin1 1.6 mm from USB edge)
XL, XR = -7.62, 7.62
PY = [30.9 - 2.54 * i for i in range(8)]
LEFT = ["IO5", "IO6", "IO7", "IO8", "IO9", "IO10", "IO20", "IO21"]
RIGHT = ["5V", "GND", "3V3", "IO4", "IO3", "IO2", "IO1", "IO0"]
NET = {"5V": "VIN", "GND": "GND", "3V3": "3V3", "IO4": "G4", "IO3": "G3", "IO1": "G1", "IO0": "G0",
       "IO5": "G5", "IO6": "G6", "IO8": "G8", "IO10": "G10", "IO20": "G20", "IO21": "G21"}
OMIT = {"IO2", "IO7", "IO9"}          # header pins removed, no pad (IO2/IO9 must stay NC; frees channels)

pads = []
def P(name, x, y, net, group, label=None, hole=HOLE_PAD_D, d=None):
    pads.append(dict(name=name, x=round(x, 3), y=round(y, 3), net=net, group=group, label=label or name.split(".")[-1], hole=hole, d=d or PAD_D))

for i, p in enumerate(LEFT):
    if p not in OMIT: P("U1." + p, XL, PY[i], NET[p], "U1", p)
for i, p in enumerate(RIGHT):
    if p not in OMIT: P("U1." + p, XR, PY[i], NET[p], "U1", p)
OMIT_POS = [(XL if p in LEFT else XR, PY[(LEFT if p in LEFT else RIGHT).index(p)], p) for p in sorted(OMIT)]

# ---- headers along the front (right-angle, modules stand on edge behind the pin row)
HY = 4.9     # v3: both front header rows +0.3 mm (designer review) for >=0.5 mm to M2 nut/posts
# MAX98357A (Adafruit order LRC,BCLK,DIN,GAIN,SD,GND,Vin) mounted so the row reads Vin..LRC left->right.
# GAIN and SD pins cut (left floating = 9 dB, stereo-average default) -> header in two pieces (2 + 3 pins).
MAXX = {"VIN": -17.94, "GND": -15.40, "SD": -12.86, "GAIN": -10.32, "DIN": -7.78, "BCLK": -5.24, "LRC": -2.70}
P("J3.VIN", MAXX["VIN"], HY, "VIN", "J3", d=2.0); P("J3.GND", MAXX["GND"], HY, "GND", "J3")
P("J3.DIN", MAXX["DIN"], HY, "G8", "J3", d=1.8); P("J3.BCLK", MAXX["BCLK"], HY, "G21", "J3"); P("J3.LRC", MAXX["LRC"], HY, "G20", "J3")
MAX_OMIT = [(MAXX["SD"], HY, "SD"), (MAXX["GAIN"], HY, "GAIN")]
# micro-SD 6-pin (ORDER CHOSEN FOR ROUTING - module must match or be wired): MOSI,CS,GND,VCC,MISO,SCK
S0 = 2.34
SDP = [("MOSI", "G6"), ("CS", "G5"), ("GND", "GND"), ("VCC", "3V3"), ("MISO", "G3"), ("SCK", "G4")]
for k, (lab, net) in enumerate(SDP): P("J2." + lab, S0 + 2.54 * k, HY, net, "J2", lab)

# ---- LCD 7-pad wire row, front edge
LY = -0.7
LCDP = [("RES", "G0"), ("SCL", "G4"), ("DC", "G10"), ("SDA", "G6"), ("GND", "GND"), ("BLK", "3V3"), ("VCC", "3V3")]
for k, (lab, net) in enumerate(LCDP): P("J1." + lab, S0 - 7.62 + 2.54 * k, LY, net, "J1", lab, hole=1.1 if lab in ("RES", "SCL") else HOLE_PAD_D)  # 1.1: LCD wire + jumper share hole

# ---- cap 470uF 10V D6.3x11 upright (leads spread to 3.5 mm), body inside case-designer box (-18.5,10)-(-11.7,16.8)
P("C1.+", -17.0, 13.2, "VIN", "C1", "+"); P("C1.-", -13.5, 13.2, "GND", "C1", "-")
CAP_C, CAP_D = (-15.25, 13.2), 6.3
# ---- off-board wire pads (left hub)
P("SW.B", -17.6, 9.1, "VIN", "SWB", "SW out")          # v3: clear of MAX envelope (ends y 8.3 after shift)
P("TTP.GND", -14.3, 9.1, "GND", "TTPG", "GND x2", hole=1.1)  # v3: TTP223 GND + TP4056 OUT- share this pad
P("TTP.OUT", 11.4, 13.4, "G1", "TTPO", "TTP OUT")
# ---- jumper pads
P("JP1.A", 4.2, 31.8, "VIN", "JP1", "JP1")      # under the ESP: fit wire BEFORE the ESP
P("JP2.A", 4.6, 28.6, "GND", "JP2", "JP2")      # under the ESP: fit wire BEFORE the ESP
P("JP1.B", -16.3, 16.8, "VIN", "JP1", "JP1")
P("JP2.B", -13.0, 16.7, "GND", "JP2", "JP2")
P("JP3.A", 11.3, 9.6, "G0", "JP3", "JP3")
P("JP4.A", 16.5, 11.5, "G4", "JP4", "JP4")
JUMPERS = [  # (name, net, padA, padB)
    ("JP1", "VIN", "JP1.A", "JP1.B"),
    ("JP2", "GND", "JP2.A", "JP2.B"),
    ("JP3", "G0", "JP3.A", "J1.RES"),
    ("JP4", "G4", "JP4.A", "J1.SCL"),
]
# wire paths (case frame). side: "top" = component side, "bottom" = copper side (thin insulated wire, e.g. 30AWG Kynar)
JUMPER_PATH = {
    "JP1": ("top", [(4.2, 31.8), (-5.0, 25.82), (-9.7, 25.82), (-10.4, 22.0), (-11.6, 20.0), (-16.3, 16.8)]),   # through cut IO7 slot
    "JP2": ("top", [(4.6, 28.6), (-5.3, 20.74), (-9.6, 20.74), (-13.0, 16.7)]),                                 # through cut IO9 slot
    "JP3": ("bottom", [(11.3, 9.6), (3.0, 8.3), (-0.7, 4.6), (-0.7, 2.6), (-4.0, 2.6), (-5.28, -0.7)]),         # under board, MAX/SD joint gap
    "JP4": ("bottom", [(16.5, 11.5), (9.4, 11.5), (3.0, 9.4), (0.3, 6.7), (0.3, 2.6), (-2.74, -0.7)]),
}
B = S0 - 7.62
FIXED = [
    ("VIN", 1.5, [(XR, PY[0]), (4.2, 31.8)]),
    ("G5", 1.0, [(XL, PY[0]), (0.28, PY[0]), (0.28, 11.78), (4.88, 7.18), (4.88, HY)]),
    ("G6", 1.0, [(XL, PY[1]), (-1.52, PY[1]), (-1.52, 11.03), (2.34, 7.17), (2.34, LY)]),
    ("G10", 1.0, [(XL, PY[5]), (-3.32, PY[5]), (-3.32, 10.28), (-0.2, 7.16), (-0.2, LY)]),
    ("G20", 1.0, [(XL, PY[6]), (-5.12, PY[6]), (-5.12, 9.53), (MAXX["LRC"], 7.11), (MAXX["LRC"], HY)]),
    ("GND", 1.5, [(XR, PY[1]), (2.33, PY[1]), (2.33, 14.5)]),
    ("GND", 1.0, [(2.33, 14.5), (2.33, 12.28)]),
    ("GND", 1.0, [(2.33, 12.28), (7.42, 7.19), (7.42, 1.95), (4.88, 1.95), (4.88, LY)]),
    ("3V3", 1.5, [(XR, PY[2]), (4.63, PY[2]), (4.63, 14.5)]),
    ("3V3", 1.0, [(4.63, 14.5), (4.63, 12.53)]),
    ("3V3", 1.0, [(4.63, 12.53), (9.96, 7.2), (9.96, LY)]),
    ("3V3", 1.0, [(B + 2.54 * 5, LY), (B + 2.54 * 6, LY)]),          # BLK-VCC bridge
    ("G21", 1.0, [(XL, PY[7]), (XL, 7.1), (MAXX["BCLK"], 7.1), (MAXX["BCLK"], HY)]),
    ("G8", 1.0, [(XL, PY[3]), (-10.12, PY[3]), (-10.12, 6.0), (MAXX["DIN"], HY)]),
    ("G0", 1.0, [(XR, PY[7]), (8.4, 12.34), (10.4, 10.34), (11.3, 9.6)]),
    ("VIN", 1.0, [(-17.6, 9.1), (-17.94, HY)]),   # necked to 1.0 next to J3.GND
    ("G1", 1.0, [(XR, PY[6]), (9.6, PY[6]), (11.4, 13.86), (11.4, 13.4)]),
    ("G4", 1.0, [(XR, PY[3]), (9.7, PY[3]), (10.2, 22.0), (10.2, 20.6), (11.4, 19.4), (15.0, 18.3), (16.5, 16.8),
                 (16.5, 7.0), (S0 + 12.7, 5.54), (S0 + 12.7, HY)]),
]
JOBS = [
    ("G3", 1.0, ["U1.IO3", "J2.MISO"], False),
    ("VIN", 1.5, ["JP1.B", "C1.+", "SW.B"], False),
    ("GND", 1.5, ["JP2.B", "C1.-", "TTP.GND", "J3.GND"], False),
]
REQUIRED = {
    "VIN": {"U1.5V", "JP1.A", "JP1.B", "C1.+", "SW.B", "J3.VIN"},
    "GND": {"U1.GND", "J2.GND", "J1.GND", "JP2.A", "JP2.B", "J3.GND", "C1.-", "TTP.GND"},
    "3V3": {"U1.3V3", "J2.VCC", "J1.VCC", "J1.BLK"},
    "G4": {"U1.IO4", "J2.SCK", "JP4.A", "J1.SCL"},
    "G6": {"U1.IO6", "J2.MOSI", "J1.SDA"},
    "G0": {"U1.IO0", "JP3.A", "J1.RES"},
    "G10": {"U1.IO10", "J1.DC"}, "G3": {"U1.IO3", "J2.MISO"}, "G5": {"U1.IO5", "J2.CS"},
    "G21": {"U1.IO21", "J3.BCLK"}, "G20": {"U1.IO20", "J3.LRC"}, "G8": {"U1.IO8", "J3.DIN"},
    "G1": {"U1.IO1", "TTP.OUT"},
}
