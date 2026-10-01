"""Tiny single-layer grid router (A*, 8-connected) with clearance via distance transform."""
import heapq, math
import numpy as np
from scipy.ndimage import distance_transform_edt
from matplotlib.path import Path

class Grid:
    def __init__(self, outline, res=0.1, pad=1.0):
        xs, ys = zip(*outline)
        self.x0, self.y0 = min(xs) - pad, min(ys) - pad
        self.res = res
        self.nx = int((max(xs) + pad - self.x0) / res) + 1
        self.ny = int((max(ys) + pad - self.y0) / res) + 1
        gx = self.x0 + np.arange(self.nx) * res
        gy = self.y0 + np.arange(self.ny) * res
        self.X, self.Y = np.meshgrid(gx, gy)        # shape (ny, nx)
        inside = Path(outline).contains_points(np.c_[self.X.ravel(), self.Y.ravel()]).reshape(self.X.shape)
        self.inside = inside
        self.dist_out = distance_transform_edt(inside) * res   # distance to outside of board

    def ij(self, x, y):
        return int(round((y - self.y0) / self.res)), int(round((x - self.x0) / self.res))
    def xy(self, i, j):
        return self.x0 + j * self.res, self.y0 + i * self.res

    def disk(self, x, y, r):
        return (self.X - x) ** 2 + (self.Y - y) ** 2 <= r * r
    def seg(self, a, b, r):
        (x1, y1), (x2, y2) = a, b
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy or 1e-12
        t = np.clip(((self.X - x1) * dx + (self.Y - y1) * dy) / L2, 0, 1)
        return (self.X - x1 - t * dx) ** 2 + (self.Y - y1 - t * dy) ** 2 <= r * r

def astar(grid, blocked, start_mask, goal_mask, turn_pen=0.6):
    ny, nx = blocked.shape
    goal_idx = np.argwhere(goal_mask)
    if len(goal_idx) == 0: return None
    gc = goal_idx.mean(0)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    cost = {}
    pq = []
    for (i, j) in np.argwhere(start_mask):
        cost[(i, j, -1)] = 0.0
        heapq.heappush(pq, (0.0, 0.0, i, j, -1))
    prev = {}
    free = ~blocked
    while pq:
        f, g, i, j, d = heapq.heappop(pq)
        if cost.get((i, j, d), 1e18) < g - 1e-9: continue
        if goal_mask[i, j]:
            path = [(i, j)]; key = (i, j, d)
            while key in prev:
                key = prev[key]; path.append((key[0], key[1]))
            return path[::-1]
        for k, (di, dj) in enumerate(dirs):
            a, b = i + di, j + dj
            if a < 0 or b < 0 or a >= ny or b >= nx: continue
            if not (free[a, b] or goal_mask[a, b]): continue
            step = 1.4142 if k >= 4 else 1.0
            ng = g + step + (turn_pen if (d != -1 and d != k) else 0)
            key = (a, b, k)
            if ng < cost.get(key, 1e18):
                cost[key] = ng; prev[key] = (i, j, d)
                h = math.hypot(a - gc[0], b - gc[1]) * 0.999
                heapq.heappush(pq, (ng + h, ng, a, b, k))
    return None

def simplify(pts):
    """drop collinear points"""
    out = [pts[0]]
    for k in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = out[-1], pts[k], pts[k + 1]
        if abs((x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1)) > 1e-9: out.append(pts[k])
    out.append(pts[-1]); return out
