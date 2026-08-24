#!/usr/bin/env python3
"""Step 1 of 2. Reads the AMBER topology and the CHARMM DCD of our own MD run and
writes the Ca coordinates the drawing needs. Deliberately has no MD library
dependency: numpy only, so it runs anywhere. BASE points at the run, which lives
outside this repo because the trajectory is 200 MB. Output feeds tools_md_svg.py."""
import struct, sys, math, json
import numpy as np

BASE="/Users/timmylin/Documents/Claude/Projects/2026 iGEM Project Plant Stress/00_Deliverable_Reports/21_MD_Simulation/results/R1_BoPep4_WT_PEPR1_out"

# ---------- parm7 ----------
def read_parm(path):
    flags={}; cur=None; fmt=None; buf=[]
    for line in open(path):
        if line.startswith('%FLAG'):
            if cur: flags[cur]=(fmt,buf)
            cur=line.split()[1]; buf=[]; fmt=None
        elif line.startswith('%FORMAT'):
            fmt=line.strip()
        elif line.startswith('%'):
            pass
        elif cur is not None:
            buf.append(line.rstrip('\n'))
    if cur: flags[cur]=(fmt,buf)
    return flags

def parse_fixed(fmt, lines, kind):
    # fmt like %FORMAT(20a4) or %FORMAT(10I8)
    import re
    m=re.search(r'\((\d+)([aIEF])([\d.]+)\)', fmt, re.I)
    n=int(m.group(1)); w=int(str(m.group(3)).split('.')[0])
    out=[]
    for ln in lines:
        for i in range(0, len(ln), w):
            s=ln[i:i+w]
            if not s.strip(): continue
            out.append(s.strip() if kind=='s' else int(s))
    return out

p=read_parm(BASE+"/stripped.parm7")
atom_name=parse_fixed(*p['ATOM_NAME'], 's')
res_label=parse_fixed(*p['RESIDUE_LABEL'], 's')
res_ptr  =parse_fixed(*p['RESIDUE_POINTER'], 'i')
natom=len(atom_name); nres=len(res_label)
print("natom",natom,"nres",nres, "last res:", res_label[-25:], file=sys.stderr)

# atom -> residue (0-based)
res_of=np.zeros(natom, dtype=int)
for r in range(nres):
    a0=res_ptr[r]-1
    a1=(res_ptr[r+1]-1) if r+1<nres else natom
    res_of[a0:a1]=r

ca=[i for i in range(natom) if atom_name[i]=='CA']
ca_res=[res_of[i] for i in ca]
print("n CA", len(ca), file=sys.stderr)

pep_res0 = nres-23           # last 23 residues
pep_ca=[i for i,r in zip(ca,ca_res) if r>=pep_res0]
rec_ca=[i for i,r in zip(ca,ca_res) if r< pep_res0]
print("pep CA", len(pep_ca), "rec CA", len(rec_ca), file=sys.stderr)
print("peptide residues:", [res_label[r] for r in range(pep_res0,nres)], file=sys.stderr)

# ---------- dcd ----------
def read_dcd(path, want_idx, max_frames=None, stride=1):
    f=open(path,'rb')
    def rec():
        n=struct.unpack('<i', f.read(4))[0]
        d=f.read(n); struct.unpack('<i', f.read(4))
        return d
    hdr=rec()
    assert hdr[:4]==b'CORD', hdr[:4]
    icntrl=struct.unpack('<20i', hdr[4:84])
    nset=icntrl[0]; namnf=icntrl[8]; withcell=icntrl[10]
    rec()                      # title
    na=struct.unpack('<i', rec())[0]
    if namnf: rec()
    want=np.array(sorted(want_idx))
    out=[]
    fi=0
    while True:
        try:
            if withcell: rec()
            x=np.frombuffer(rec(), dtype='<f4')
            y=np.frombuffer(rec(), dtype='<f4')
            z=np.frombuffer(rec(), dtype='<f4')
        except Exception:
            break
        if fi % stride == 0:
            out.append(np.stack([x[want], y[want], z[want]], axis=1).astype(np.float64))
        fi+=1
        if max_frames and len(out)>=max_frames: break
    f.close()
    return np.array(out), na, nset, fi

sel = pep_ca + rec_ca
order = np.argsort(sel)
inv = np.empty_like(order); inv[order]=np.arange(len(order))
coords, na, nset, nread = read_dcd(BASE+"/stripped.dcd", sel, stride=8)
print("natoms in dcd", na, "nset hdr", nset, "frames read", nread, "kept", coords.shape, file=sys.stderr)
coords = coords[:, inv, :]           # back to sel order: peptide first, then receptor
np.save("md_coords.npy", coords)
json.dump({"n_pep":len(pep_ca),"n_rec":len(rec_ca),"frames":int(coords.shape[0]),
           "total_frames":int(nread)}, open("md_meta.json","w"))
print("saved", coords.shape)
