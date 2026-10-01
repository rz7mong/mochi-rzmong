import json, sys, numpy as np, trimesh
from _paths import *  # repo-relative paths
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
exec(open('render_previews.py').read().split('# ---------- 1) PCB top view')[0])
def dec(m, n=6000):
    try: return m.simplify_quadric_decimation(face_count=n)
    except Exception:
        idx = np.random.default_rng(0).choice(len(m.faces), min(n, len(m.faces)), replace=False); return trimesh.Trimesh(m.vertices, m.faces[idx], process=False)
def cube_faces(lo, hi):
    x0, y0, z0 = lo; x1, y1, z1 = hi
    v = np.array([[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]])
    return [v[[0,1,2,3]], v[[4,5,6,7]], v[[0,1,5,4]], v[[2,3,7,6]], v[[1,2,6,5]], v[[0,3,7,4]]]
for tag, casef, standf, P, pcb in [('pcb_v7', CASE_PCB, STAND_PCB, V7, True),
                                   ('loose', CASE_ORIG, STAND_ORIG, LOOSE, False)]:
    cm = dec(trimesh.load(casef)); sm = trimesh.load(standf); sm.apply_translation([0, 0, -10.38]); sm = dec(sm, 3000)
    fig = plt.figure(figsize=(16, 8))
    for i, (el, az) in enumerate([(25, -60), (20, 120)]):
        ax = fig.add_subplot(1, 2, i + 1, projection='3d')
        ax.add_collection3d(Poly3DCollection(cm.vertices[cm.faces], fc=(0.6, 0.6, 0.6, 0.05), ec=(0.3, 0.3, 0.3, 0.06), lw=0.2))
        ax.add_collection3d(Poly3DCollection(sm.vertices[sm.faces], fc=(0.3, 0.5, 1, 0.08), ec=(0.2, 0.3, 0.8, 0.08), lw=0.2))
        if pcb:
            top = np.c_[poly, np.full(len(poly), -13.6)]; ax.add_collection3d(Poly3DCollection([top], fc=(0.1, 0.6, 0.1, 0.6)))
        for k, v in list(P.items()) + [(f'lcd{j}', dict(lo=a, hi=b)) for j, (a, b) in enumerate(LCD)]:
            ax.add_collection3d(Poly3DCollection(cube_faces(v['lo'], v['hi']), fc=col(k), alpha=0.55 if not k.startswith('lcd') else 0.2, ec='k', lw=0.3))
        ax.set_xlim(-32, 32); ax.set_ylim(-47, 47); ax.set_zlim(-28, 27); ax.set_box_aspect((64, 94, 55)); ax.view_init(el, az)
        ax.set_xlabel('x'); ax.set_ylabel('y (+ = rear)'); ax.set_zlabel('z')
    import matplotlib.patches as mp
    fig.legend(handles=[mp.Patch(color=c, label=p) for p, c in COL.items() if p not in ('bot',)], loc='lower center', ncol=13, fontsize=8)
    fig.suptitle(f'{tag}: transparent case (grey) + stand (blue), component envelopes'); plt.tight_layout(); plt.savefig(f'assembly3d_{tag}.png', dpi=110); plt.close()
print('ok')
