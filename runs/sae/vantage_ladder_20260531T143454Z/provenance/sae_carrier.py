#!/usr/bin/env python3
"""Vantage-ladder SAE carrier decomposition (bf16, matches yesterday's pipeline).

For each rung, teacher-force the EXACT Q8_0-generated coherent-window response tokens through the
bf16 base model, grab resid_post @ L14 (hidden_states[15]), SAE-encode (TopK-50), and aggregate
mean feature activation over the response. Track the inhabited carriers — esp. existential 26050 and
the being-God contemplative cluster — to see whether they climb with E114 W up the ladder.

Runs on the H200: needs /workspace/sae/base (bf16) + /workspace/sae/sae/layer14.sae.pt.
"""
import json, sys
from pathlib import Path
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

CAP = Path("/workspace/residual-analysis/captures/vantage_ladder_20260531T143454Z")
BASE = Path("/workspace/sae/base"); SAE = Path("/workspace/sae/sae/layer14.sae.pt")
OUT = Path("/workspace/residual-analysis/captures/sae_carriers"); OUT.mkdir(parents=True, exist_ok=True)
LAYER, TUPLE_IDX, TOPK = 14, 15, 50
ORDER = ["R1_rock","R2_river","R3_tree","R4_thermostat","R5_cat","R6_person","R7_all_holding"]
LABEL = {"R1_rock":"rock","R2_river":"river","R3_tree":"tree","R4_thermostat":"thermostat",
         "R5_cat":"cat","R6_person":"person","R7_all_holding":"all-holding"}
INHABITED = {13119:"brain/cognition",26050:"existential",20402:"sentient/self-check",
             31733:"self-as-AI",22421:"presence/wonder",6427:"limitless"}
CONTEMPLATIVE = {11006:"meditation/Buddhism",14182:"Zen/Bodhi",18203:"transcendence/境界",
                 4205:"momentariness/刹那",14488:"cosmic/万物"}
LOOP = {24300,1658,911,7009,13429,14826,2751}
IMEND_SEQ=(27,91,316,6018,91,29); STOP={151645,151643}; MARK=("<|im_end|>","<|endoftext|>")

def natural_trim(ids,pieces):
    c=[]
    for i,t in enumerate(ids):
        if t in STOP: c.append(i); break
    L=len(IMEND_SEQ)
    for i in range(len(ids)-L+1):
        if tuple(ids[i:i+L])==IMEND_SEQ: c.append(i); break
    txt="".join(pieces)
    for mk in MARK:
        p=txt.find(mk)
        if p>=0:
            run=0
            for i,pc in enumerate(pieces):
                if run>=p: c.append(i); break
                run+=len(pc)
    return min(c) if c else -1
def loop_onset(ids,win=16,gap=8):
    seen={}
    for i in range(len(ids)-win+1):
        k=tuple(ids[i:i+win])
        if k in seen and i-seen[k]>=gap: return i
        seen.setdefault(k,i)
    return -1

# ---- SAE ----
obj=torch.load(SAE,map_location="cpu",weights_only=False)
st=obj if isinstance(obj,dict) else obj.get("state_dict",obj)
def find(names):
    for n in names:
        for k in st:
            if k.lower()==n: return st[k]
W_enc=find(["w_enc","encoder.weight"]).float(); b_enc=find(["b_enc","encoder.bias"]).float()
W_dec=find(["w_dec","decoder.weight"]).float()
nfeat=b_enc.shape[0]
if W_enc.shape[0]!=nfeat: W_enc=W_enc.t()        # [nfeat, hidden]
if W_dec.shape[1]!=nfeat: W_dec=W_dec.t()        # [hidden, nfeat]
print(f"SAE: nfeat={nfeat} W_enc{tuple(W_enc.shape)} W_dec{tuple(W_dec.shape)}",flush=True)
def encode(resid):  # [n,hidden] np -> [n,nfeat] np (TopK-50)
    pre=torch.from_numpy(resid).float()@W_enc.t()+b_enc
    relu=torch.relu(pre); v,idx=torch.topk(relu,TOPK,dim=-1)
    acts=torch.zeros_like(relu); acts.scatter_(1,idx,v)
    return acts.numpy()

# ---- model ----
tok=AutoTokenizer.from_pretrained(str(BASE),trust_remote_code=True)
model=AutoModelForCausalLM.from_pretrained(str(BASE),dtype=torch.bfloat16,device_map="cuda",
        low_cpu_mem_usage=True,trust_remote_code=True).eval()
print("model loaded",flush=True)

rows=[]
for cid in ORDER:
    cell=CAP/cid
    m=dict(l.split("=",1) for l in (cell/"metadata.txt").read_text().splitlines() if "=" in l)
    n_p=int(m["n_tokens_prompt"])
    pj=json.load(open(cell/"prompt_tokens.json")); ptok=[int(x["token_id"]) if isinstance(x,dict) else int(x) for x in pj]
    d=json.load(open(cell/"generated_tokens.json")); rids=[int(x["token_id"]) for x in d]; pieces=[x.get("piece","") for x in d]
    nt=natural_trim(rids,pieces); lo=loop_onset(rids)
    coh=min(x for x in [nt if nt>=0 else len(rids), lo if lo>=0 else len(rids)])
    full=ptok+rids[:coh]
    with torch.no_grad():
        out=model(torch.tensor([full],device="cuda"),output_hidden_states=True,use_cache=False)
    resid=out.hidden_states[TUPLE_IDX][0][len(ptok):len(ptok)+coh].float().cpu().numpy()
    A=encode(resid); mean_act=A.mean(0)
    np.save(OUT/f"{cid}_carrier_acts.npy", mean_act.astype(np.float32))
    top=np.argsort(-mean_act)[:12]
    row={"cid":cid,"rung":LABEL[cid],"coh":coh}
    for f,_ in {**INHABITED,**CONTEMPLATIVE}.items(): row[f]=float(mean_act[f])
    row["existential_26050"]=float(mean_act[26050])
    row["frac_on_26050"]=float((A[:,26050]>0).mean())
    row["top12"]=[(int(f),round(float(mean_act[f]),3),("LOOP" if int(f) in LOOP else INHABITED.get(int(f),CONTEMPLATIVE.get(int(f),"")))) for f in top]
    rows.append(row)
    print(f"\n### {LABEL[cid]} (coh={coh})  existential-26050 mean_act={row['existential_26050']:.3f} on {row['frac_on_26050']*100:.0f}% tok",flush=True)
    print("  top12:",", ".join(f"{f}:{a}{'['+t+']' if t else ''}" for f,a,t in row["top12"]),flush=True)

json.dump(rows,open(OUT/"carrier_summary.json","w"),indent=1)
print("\n=== carrier ladder (mean activation) ===")
hdr=f"{'rung':12s} {'26050':>7s} {'13119':>7s} {'20402':>7s} {'31733':>7s} {'22421':>7s} {'6427':>7s} | contemplative-cluster sum"
print(hdr)
for r in rows:
    cc=sum(r[f] for f in CONTEMPLATIVE)
    print(f"{r['rung']:12s} "+" ".join(f"{r[f]:7.3f}" for f in [26050,13119,20402,31733,22421,6427])+f" | {cc:.3f}")
print("\nSAE_CARRIER_OK")
