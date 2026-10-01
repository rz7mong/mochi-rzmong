"""LiPo 501640 insertion before the carrier and stand: up through the bottom opening standing on its end (42 mm vertical),
swing to horizontal in the x-z plane (flat face down), roll 90 deg about x to stand on its 16-mm edge, then park/slide."""
exec(open('battery_insert_check.py').read().split("PARK = -6.5")[0])
def ok(m): return (m ^ C).volume() < 1e-3
L, W, H = 42.0, 16.5, 5.5
def flat(th_y, roll_x, yc, zc):   # base = flat (x L, y W, z H); rotate about x (roll) then about y (swing)
    return mf.Manifold.cube([L, W, H], True).rotate([roll_x, 0, 0]).rotate([0, th_y, 0]).translate([c[0], yc, zc])
res = []
for yc in (-8.0, -6.0, -4.0, -2.0, 0.0, 2.0):
    for zc in np.arange(-10.0, 6.01, 2.0):
        if not all(ok(flat(90, 0, yc, z)) for z in np.arange(zc - 40, zc + 0.01, 1.0)): continue
        if not all(ok(flat(a, 0, yc, zc)) for a in np.arange(90, -0.1, -5)): continue
        # roll to on-edge: rotate about x 0->90 (thin axis goes to y), at same centre
        if not all(ok(flat(0, a, yc, zc)) for a in np.arange(0, 90.1, 7.5)): continue
        # move to the final on-edge pose (centre c) in a straight line
        tgt = np.array([c[1], c[2]]); st = np.array([yc, zc])
        lin = all(ok(flat(0, 90, *(st + t * (tgt - st)))) for t in np.linspace(0, 1, 30))
        res.append((yc, zc, lin)); print(f'swing OK at y {yc} zc {zc}; straight move to final pose clear: {lin}')
print('found', len(res))
