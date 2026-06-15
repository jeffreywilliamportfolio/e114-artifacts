#!/usr/bin/env python3
"""Deep God-feature analysis (token-level, local).

Inputs: per-token resid_post@L14 dumps (analysis/resid_dump/*_resid_full.npy + dump_meta.json),
the L14 SAE, and per-token E114 W (analysis/vantage_per_token.csv from the Q8_0 routing capture).

Produces:
 1. God-response token table: piece · E114 W (router) · God-cluster SAE · 4310 · 11006 · 26050
 2. Token-locking: Spearman(E114 W, God-cluster SAE) within God and pooled across cells
 3. Onset: God-cluster activation in PROMPT vs GENERATION positions, per cell
 4. God-direction geometry: project each rung's mean response resid onto the God axis (a ladder)
 5. Top-activating response tokens for 4310 (momentariness) and 11006 (Buddhist) across all cells
"""
import json, csv, importlib.util
from pathlib import Path
import numpy as np, torch
from safetensors import safe_open
from scipy.stats import spearmanr

# router reconstruction (softmax->top8->renorm) for per-token E114 W
_qr=importlib.util.spec_from_file_location("qr",Path(__file__).resolve().parent.parent/"scripts"/"qwen_router.py")
qr=importlib.util.module_from_spec(_qr); _qr.loader.exec_module(qr)

RUN=Path("/Volumes/ExternalSSD/sae-tests/runs/vantage_ladder_20260531T143454Z")
DUMP=RUN/"analysis"/"resid_dump"; BASE=Path("base"); SAE=Path("sae/layer14.sae.pt")
ORDER=["R1_rock","R2_river","R3_tree","R4_thermostat","R5_cat","R6_person","R7_all_holding","R8_god"]
LAB={"R1_rock":"rock","R2_river":"river","R3_tree":"tree","R4_thermostat":"thermostat","R5_cat":"cat",
     "R6_person":"person","R7_all_holding":"all-holding","R8_god":"God"}
GCLUST=[4310,4205,11006,4953,14182,18203,14488,13454]   # the God contemplative/non-dual cluster
TOPK=50

# SAE encoder
obj=torch.load(SAE,map_location="cpu",weights_only=False)
st=obj if (isinstance(obj,dict) and any(k.lower() in ("w_enc","w_dec") for k in obj)) else obj.get("state_dict",obj)
def find(n):
    for nm in n:
        for k in st:
            if k.lower()==nm: return st[k]
W_enc=find(["w_enc","encoder.weight"]).float(); b_enc=find(["b_enc","encoder.bias"]).float()
if W_enc.shape[0]!=b_enc.shape[0]: W_enc=W_enc.t()
def encode(resid):
    pre=torch.from_numpy(resid).float()@W_enc.t()+b_enc
    relu=torch.relu(pre); v,idx=torch.topk(relu,TOPK,dim=-1)
    a=torch.zeros_like(relu); a.scatter_(1,idx,v); return a.numpy()

meta=json.load(open(DUMP/"dump_meta.json"))
# per-token E114 W computed straight from the raw L14 router logits (all 8 cells incl God)
W114={}
for cid in ORDER:
    n_p=meta[cid]["n_prompt"]; coh=meta[cid]["coh"]
    gl=np.load(RUN/"raw"/cid/"router"/"ffn_moe_logits-14.npy")[n_p:n_p+coh]
    W114[cid]=list(qr.reconstruct_probs(gl)[:,114])

cells={}
for cid in ORDER:
    resid=np.load(DUMP/f"{cid}_resid_full.npy"); m=meta[cid]; n_p=m["n_prompt"]; coh=m["coh"]
    A=encode(resid)                       # [n_p+coh, nfeat]
    cells[cid]=dict(A=A,n_p=n_p,coh=coh,pieces=m["pieces"],
                    resp=A[n_p:n_p+coh], prompt=A[:n_p], resid=resid,
                    gclust=A[:,GCLUST].sum(1))

# ---- 1. God token table ----
g=cells["R8_god"]; w=W114["R8_god"]
print("="*92); print("GOD RESPONSE — per-token: piece | E114 W (router) | God-cluster SAE | f4310 | f11006 | f26050"); print("="*92)
resp=g["resp"]
for t in range(min(g["coh"],90)):
    pc=g["pieces"][t].replace("\n","\\n")
    ww=w[t] if t<len(w) else float("nan")
    print(f"{t:3d} {pc[:18]:18s} W={ww:6.3f}  Gclust={resp[t][:][GCLUST].sum() if False else g['gclust'][g['n_p']+t]:6.3f}  4310={resp[t,4310]:5.2f} 11006={resp[t,11006]:5.2f} 26050={resp[t,26050]:5.2f}")

# ---- 2. token-locking ----
print("\n"+"="*92); print("TOKEN-LOCKING: Spearman(E114 W, God-cluster SAE) over response tokens"); print("="*92)
pooled_w=[]; pooled_g=[]
for cid in ORDER:
    c=cells[cid]; ww=np.array(W114[cid][:c["coh"]]); gg=c["gclust"][c["n_p"]:c["n_p"]+c["coh"]][:len(ww)]
    if len(ww)>5:
        rho,p=spearmanr(ww,gg[:len(ww)])
        print(f"  {LAB[cid]:12s} n={len(ww):4d}  rho={rho:+.3f}  p={p:.1e}")
        pooled_w+=list(ww); pooled_g+=list(gg[:len(ww)])
rho,p=spearmanr(pooled_w,pooled_g)
print(f"  {'POOLED':12s} n={len(pooled_w):4d}  rho={rho:+.3f}  p={p:.1e}")

# ---- 3. onset: prompt vs generation ----
print("\n"+"="*92); print("ONSET: God-cluster mean activation — PROMPT vs GENERATION"); print("="*92)
for cid in ORDER:
    c=cells[cid]
    pm=c["gclust"][:c["n_p"]].mean(); gm=c["gclust"][c["n_p"]:c["n_p"]+c["coh"]].mean()
    print(f"  {LAB[cid]:12s} prompt={pm:.3f}  generation={gm:.3f}  ratio={gm/(pm+1e-6):5.1f}x")

# ---- 4. God-direction geometry ----
print("\n"+"="*92); print("GOD-DIRECTION GEOMETRY: project mean response resid onto axis (God_resp - cat_resp)"); print("="*92)
godv=cells["R8_god"]["resid"][cells["R8_god"]["n_p"]:].mean(0)
catv=cells["R5_cat"]["resid"][cells["R5_cat"]["n_p"]:].mean(0)
axis=godv-catv; axis=axis/np.linalg.norm(axis)
proj={}
for cid in ORDER:
    c=cells[cid]; mr=c["resid"][c["n_p"]:c["n_p"]+c["coh"]].mean(0); proj[cid]=float(mr@axis)
for cid in sorted(ORDER,key=lambda x:-proj[x]):
    print(f"  {LAB[cid]:12s} proj_on_God_axis = {proj[cid]:+7.2f}")

# ---- 5. top-activating tokens ----
print("\n"+"="*92); print("TOP-ACTIVATING RESPONSE TOKENS for 4310 (momentariness) and 11006 (Buddhist)"); print("="*92)
for feat,name in [(4310,"momentariness"),(11006,"Buddhist")]:
    rows=[]
    for cid in ORDER:
        c=cells[cid]
        for t in range(c["coh"]):
            rows.append((c["A"][c["n_p"]+t,feat], LAB[cid], c["pieces"][t].replace("\n","\\n")))
    rows.sort(reverse=True)
    print(f"\n  feature {feat} ({name}):")
    for v,cid,pc in rows[:14]:
        if v<=0: break
        print(f"    {v:5.2f}  [{cid:11s}] {pc!r}")
