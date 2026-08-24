#!/usr/bin/env python3
"""Step 2 of 2. Superposes every frame on the receptor Ca, projects to the plane
that best shows the pocket and the peptide, picks the window whose last frame is
closest to its first so the loop closes, and emits the SVG that is inlined in
index.html. Run tools_md_extract.py first."""
import numpy as np, json, math
C=np.load("md_coords.npy"); meta=json.load(open("md_meta.json"))
NP=meta["n_pep"]; NR=meta["n_rec"]
pep=C[:,:NP,:]; rec=C[:,NP:,:]

def kabsch(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0)
    V,S,Wt=np.linalg.svd(Pc.T@Qc)
    D=np.diag([1,1,np.sign(np.linalg.det(V@Wt))])
    return V@D@Wt, P.mean(0), Q.mean(0)

ref=rec[0]; P=np.empty_like(pep); R_=np.empty_like(rec)
for i in range(C.shape[0]):
    Rm,mc,mr=kabsch(rec[i],ref)
    P[i]=(pep[i]-mc)@Rm+mr
    R_[i]=(rec[i]-mc)@Rm+mr

d=np.linalg.norm(R_[0][:,None,:]-P[0][None,:,:],axis=2).min(1)
pocket=R_[0][d<11.0]
ARG487 = R_[0][487-29]                      # receptor numbering starts at 29

allpts=np.vstack([pocket, P.reshape(-1,3)])
mu=allpts.mean(0); _,_,Vt=np.linalg.svd(allpts-mu, full_matrices=False)
ax1,ax2=Vt[0],Vt[1]
th=math.radians(17.0); ca_,sa=math.cos(th),math.sin(th)
def proj(X):
    Y=X-mu; u=Y@ax1; v=Y@ax2
    return np.stack([u*ca_-v*sa, u*sa+v*ca_], axis=-1)

pp=proj(P); pk=proj(pocket); ar=proj(ARG487)

L=46; best=(1e9,0)
for s in range(0, C.shape[0]-L):
    r=np.sqrt(((pp[s]-pp[s+L])**2).sum(1).mean())
    if r<best[0]: best=(r,s)
s=best[1]; W=pp[s:s+L]
print("loop start",s,"closure %.2f A"%best[0])

allxy=np.vstack([pk, W.reshape(-1,2), ar[None,:]])
lo=allxy.min(0); hi=allxy.max(0); ext=hi-lo
Wbox,Hbox,pad=200,150,9
sc=min((Wbox-2*pad)/ext[0], (Hbox-2*pad)/ext[1])
off=(np.array([Wbox,Hbox])-ext*sc)/2
def box(xy):
    q=(xy-lo)*sc+off; q=q.copy(); q[...,1]=Hbox-q[...,1]; return q
Wb=box(W); pkb=box(pk); arb=box(ar)

# The envelope: the mean backbone across the window, stroked as wide as the
# backbone actually wanders. It is the picture of the acceptance criterion.
mean=Wb.mean(0)
dev=np.linalg.norm(Wb-mean[None,:,:],axis=2).mean()
band_w=max(9.0, 2.6*dev)
band_d="M"+"L".join("%.1f %.1f"%(x,y) for x,y in mean)

def path(pts): return "M"+"L".join("%.0f %.0f"%(x,y) for x,y in pts)
vals=";".join(path(f) for f in Wb)
tipx=";".join("%.0f"%f[-1][0] for f in Wb)
tipy=";".join("%.0f"%f[-1][1] for f in Wb)
dots=" ".join('<circle cx="%.0f" cy="%.0f" r="2.2"/>'%(x,y) for x,y in pkb)

svg=f'''<svg class="mdanim" viewBox="0 0 200 150" role="img"
     aria-label="Thirty nanoseconds of molecular dynamics we ran: the BoPep4 backbone moving in the PEPR1 groove, Asn23 in green and Arg487 in amber. Still until it is pointed at."
     data-frames="{vals}"
     data-tipx="{tipx}"
     data-tipy="{tipy}">
  <path class="md-band" fill="none" stroke-width="{band_w:.1f}" d="{band_d}"/>
  <g class="md-pocket">{dots}</g>
  <circle class="md-anchor" cx="{arb[0]:.0f}" cy="{arb[1]:.0f}" r="3.4"/>
  <path class="md-chain" fill="none" d="{path(Wb[0])}"/>
  <circle class="md-tip" cx="{Wb[0][-1][0]:.0f}" cy="{Wb[0][-1][1]:.0f}" r="4.4"/>
</svg>'''
open("mdanim.svg","w").write(svg); print("bytes",len(svg),"frames",len(Wb),"pocket",len(pkb))
