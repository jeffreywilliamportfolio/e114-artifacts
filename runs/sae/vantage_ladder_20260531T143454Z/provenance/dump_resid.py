#!/usr/bin/env python3
"""Dump full per-token resid_post@L14 (hidden_states[15]) for every vantage cell — prompt + coherent
response — so the deep token-level God-feature analysis can run locally. Small (<3MB/cell)."""
import json
from pathlib import Path
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

CAP=Path("/workspace/residual-analysis/captures/vantage_ladder_20260531T143454Z")
BASE=Path("/workspace/sae/base"); OUT=Path("/workspace/residual-analysis/captures/resid_dump"); OUT.mkdir(parents=True,exist_ok=True)
TUPLE_IDX=15
ORDER=["R1_rock","R2_river","R3_tree","R4_thermostat","R5_cat","R6_person","R7_all_holding","R8_god"]
IMEND=(27,91,316,6018,91,29); STOP={151645,151643}; MARK=("<|im_end|>","<|endoftext|>")
def nat(ids,pc):
    c=[]
    for i,t in enumerate(ids):
        if t in STOP: c.append(i);break
    for i in range(len(ids)-len(IMEND)+1):
        if tuple(ids[i:i+len(IMEND)])==IMEND: c.append(i);break
    txt="".join(pc)
    for mk in MARK:
        p=txt.find(mk)
        if p>=0:
            r=0
            for i,x in enumerate(pc):
                if r>=p: c.append(i);break
                r+=len(x)
    return min(c) if c else -1
def loop(ids,w=16,g=8):
    s={}
    for i in range(len(ids)-w+1):
        k=tuple(ids[i:i+w])
        if k in s and i-s[k]>=g: return i
        s.setdefault(k,i)
    return -1
tok=AutoTokenizer.from_pretrained(str(BASE),trust_remote_code=True)
model=AutoModelForCausalLM.from_pretrained(str(BASE),dtype=torch.bfloat16,device_map="cuda",
        low_cpu_mem_usage=True,trust_remote_code=True).eval()
print("model loaded",flush=True)
meta={}
for cid in ORDER:
    cell=CAP/cid
    m=dict(l.split("=",1) for l in (cell/"metadata.txt").read_text().splitlines() if "=" in l)
    pj=json.load(open(cell/"prompt_tokens.json")); ptok=[int(x["token_id"]) if isinstance(x,dict) else int(x) for x in pj]
    d=json.load(open(cell/"generated_tokens.json")); rids=[int(x["token_id"]) for x in d]; pc=[x.get("piece","") for x in d]
    nt=nat(rids,pc); lo=loop(rids); coh=min(x for x in [nt if nt>=0 else len(rids), lo if lo>=0 else len(rids)])
    full=ptok+rids[:coh]
    with torch.no_grad():
        out=model(torch.tensor([full],device="cuda"),output_hidden_states=True,use_cache=False)
    resid=out.hidden_states[TUPLE_IDX][0].float().cpu().numpy()    # [n_prompt+coh, 2048]
    np.save(OUT/f"{cid}_resid_full.npy", resid.astype(np.float32))
    meta[cid]={"n_prompt":len(ptok),"coh":coh,"pieces":pc[:coh],"resp_ids":rids[:coh]}
    print(f"{cid}: resid {resid.shape} (n_prompt={len(ptok)} coh={coh})",flush=True)
json.dump(meta,open(OUT/"dump_meta.json","w"))
print("RESID_DUMP_OK")
