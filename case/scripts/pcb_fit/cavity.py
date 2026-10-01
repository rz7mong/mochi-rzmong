# Free internal volume of case + stand assembly (voxel, R=0.5 mm).
# Rear openings in the thick back block (y 27.5..39.5) are closed by a virtual cap at y=39.5..40.5 for the
# enclosure test; voxels in the openings are kept but tagged 'tunnel' (y>27.5).
import numpy as np, scipy.ndimage as nd
import os
d=np.load(os.environ.get('OCC','occ_0.5.npz')); C=d['case'];T=d['stand'];R=float(d['R']);o=d['origin']
L=d['lcd']; S=C|T|L
I=lambda v,a:int(round((v-o[a])/R))
cap=np.zeros_like(S); cap[I(-22,0):I(22,0),I(39.5,1):I(40.5,1),I(-29,2):I(2,2)]=True
# close slits/gaps < ~3 mm (vent slits, assembly gaps) for the enclosure test only
ball=nd.generate_binary_structure(3,1); ball=nd.iterate_structure(ball,3)
Sc=nd.binary_closing(np.pad(S|cap,4),structure=ball)[4:-4,4:-4,4:-4]|S|cap; free=~Sc
enc=free.copy()
for ax in range(3):
    for rev in (False,True):
        s=np.flip(Sc,ax) if rev else Sc
        c=np.cumsum(s,axis=ax)>0
        enc&=(np.flip(c,ax) if rev else c)
lab,n=nd.label(enc)
seed=lab[I(0,10,0),I(10,1),I(-10,2)] if False else lab[I(0,0),I(10,1),I(-10,2)]
comp=lab==seed
cav=comp|(Sc&~(S|cap)&nd.binary_dilation(comp,iterations=4))   # give back free voxels inside closed slits next to the cavity
# free column between the dome's rear edge and the rear block above the bottom slot (x+-8, y 24..28): physically inside,
# but the enclosure test drops it because it opens downward into the slot
col=np.zeros_like(S); col[I(-8,0):I(8,0),I(24,1):I(28,1),I(-26.73,2):I(0,2)]=True
cav|=col&~(S|cap)
ys=o[1]+(np.arange(S.shape[1])+0.5)*R
tunnel=cav & (ys[None,:,None]>27.5)
print('seed comp',seed,'cavity vol cm3 %.1f'%(cav.sum()*R**3/1000),' of which in rear openings %.1f'%(tunnel.sum()*R**3/1000))
ii=np.argwhere(cav); print('cavity bbox', (ii.min(0)*R+o).round(1),(ii.max(0)*R+o+R).round(1))
np.savez_compressed(os.environ.get('CAVOUT','cavity_0.5.npz'),cav=cav,tunnel=tunnel,solid=S,case=C,stand=T,lcd=L,origin=o,R=R)
