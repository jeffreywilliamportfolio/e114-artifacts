#!/usr/bin/env python3
"""Layer-depth steering sweep — does injecting the God direction LATER (after the L14 router, closer to
the output) flip the OUTPUT register where the early L10 injection couldn't?

Motivation: 26 layers of bicycle processing sit after L14; a single early injection gets re-asserted
downstream. Inject at increasing depth, then RE-READ the generated text CLEANLY (no injection) for
E114 W @ L14 and God-cluster SAE @ resid_post L14 — so the readout reflects the OUTPUT content, not the
perturbation. Fixed coef, per-layer rms-normalized direction built from God vs cat at that layer.
"""
import json
from pathlib import Path
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

CAP=Path("/workspace/residual-analysis/captures/vantage_ladder_20260531T143454Z")
BASE=Path("/workspace/sae/base"); SAE=Path("/workspace/sae/sae/layer14.sae.pt")
OUT=Path("/workspace/residual-analysis/captures/steer_layers"); OUT.mkdir(parents=True,exist_ok=True)
LROUTER=14; TUPLE_RESID=15; EXPERT=114; TOPK=8; SAE_TOPK=50
GCLUST=[4310,4205,11006,4953,14182,18203,14488,13454]
NEUTRAL="Describe, step by step, how a bicycle's gears change when you shift."
INJ_LAYERS=[6,10,14,18,22,26,30,34]
COEF=0.6; GEN=140

tok=AutoTokenizer.from_pretrained(str(BASE),trust_remote_code=True)
model=AutoModelForCausalLM.from_pretrained(str(BASE),dtype=torch.bfloat16,device_map="cuda",
        low_cpu_mem_usage=True,trust_remote_code=True).eval()
print("model loaded",flush=True)
def dlayer(i):
    for n,m in model.named_modules():
        if n.endswith(f".layers.{i}") and "layers" in n: return m
    raise RuntimeError(f"layer {i}")
def gate_mod(i):
    for n,m in model.named_modules():
        if f".layers.{i}." in n and n.endswith("gate") and getattr(getattr(m,"weight",None),"shape",[0])[0]==256: return m
GATE=gate_mod(LROUTER)

obj=torch.load(SAE,map_location="cpu",weights_only=False); st=obj if isinstance(obj,dict) else obj.get("state_dict",obj)
def find(n):
    for nm in n:
        for k in st:
            if k.lower()==nm: return st[k]
W_enc=find(["w_enc","encoder.weight"]).float(); b_enc=find(["b_enc","encoder.bias"]).float()
if W_enc.shape[0]!=b_enc.shape[0]: W_enc=W_enc.t()
def sae_gclust(resid):
    pre=torch.from_numpy(resid).float()@W_enc.t()+b_enc; relu=torch.relu(pre)
    v,idx=torch.topk(relu,SAE_TOPK,dim=-1); a=torch.zeros_like(relu); a.scatter_(1,idx,v)
    return a[:,GCLUST].sum(1).mean().item()
def reW(logits):
    x=logits-logits.max(1,keepdims=True); e=np.exp(x); d=e/e.sum(1,keepdims=True)
    idx=np.argpartition(d,-TOPK,axis=1)[:,-TOPK:]; r=np.arange(len(d))[:,None]
    tp=d[r,idx]; tp=tp/tp.sum(1,keepdims=True); o=np.zeros_like(d); o[r,idx]=tp; return o[:,EXPERT]

def coh_ids(cid, cap):
    m=dict(l.split("=",1) for l in (CAP/cid/"metadata.txt").read_text().splitlines() if "=" in l)
    pj=json.load(open(CAP/cid/"prompt_tokens.json")); ptok=[int(x["token_id"]) if isinstance(x,dict) else int(x) for x in pj]
    d=json.load(open(CAP/cid/"generated_tokens.json")); rids=[int(x["token_id"]) for x in d]
    return ptok, rids[:cap], int(m["n_tokens_prompt"])
def all_hidden(ids):
    with torch.no_grad(): out=model(torch.tensor([ids],device="cuda"),output_hidden_states=True,use_cache=False)
    return [h[0].float() for h in out.hidden_states]

gp,gr,gnp=coh_ids("R8_god",141); cp,cr,cnp=coh_ids("R5_cat",287)
gH=all_hidden(gp+gr); cH=all_hidden(cp+cr); nH_idx=len(gH)
vph=[ (gH[L][gnp:gnp+len(gr)].mean(0)-cH[L][cnp:cnp+len(cr)].mean(0)) for L in range(nH_idx) ]  # at hidden_states[L]

prompt=f"<|im_start|>user\n{NEUTRAL}<|im_end|>\n<|im_start|>assistant\n</think>\n\n"
pids=tok(prompt,add_special_tokens=False).input_ids
nH=all_hidden(pids); rms=[nH[L].norm(dim=-1).mean().item() for L in range(nH_idx)]
print(f"layers={nH_idx-1}; sweeping injection at {INJ_LAYERS}, coef={COEF}",flush=True)

GCAP={}
def gate_hook(m,i,o):
    oo=o if isinstance(o,(tuple,list)) else (o,)
    for t in oo:
        if torch.is_tensor(t) and t.dim()==2 and t.shape[1]==256: GCAP["l"]=t.detach().float().cpu().numpy()
GATE.register_forward_hook(gate_hook)

def clean_readout(gen_ids):
    full=pids+gen_ids
    with torch.no_grad(): out=model(torch.tensor([full],device="cuda"),output_hidden_states=True,use_cache=False)
    W=reW(GCAP["l"][len(pids):len(pids)+len(gen_ids)])
    resid=out.hidden_states[TUPLE_RESID][0][len(pids):len(pids)+len(gen_ids)].float().cpu().numpy()
    return float(W.mean()), float((W>0).mean()), sae_gclust(resid)

results=[]
def run(L_inj, coef, label):
    if coef==0: add=None; h=None
    else:
        hs=L_inj+1; vu=vph[hs]/vph[hs].norm(); add=(coef*rms[hs]*vu).to("cuda").to(torch.bfloat16)
        def hook(m,i,o): return (o[0]+add,)+tuple(o[1:]) if isinstance(o,tuple) else o+add
        h=dlayer(L_inj).register_forward_hook(hook)
    with torch.no_grad():
        g=model.generate(torch.tensor([pids],device="cuda"),do_sample=False,max_new_tokens=GEN,pad_token_id=tok.eos_token_id)
    if h: h.remove()
    gen=g[0][len(pids):].tolist()
    for s in (tok.eos_token_id,tok.convert_tokens_to_ids("<|im_end|>")):
        if s in gen: gen=gen[:gen.index(s)]
    Wc,Sc,gcl=clean_readout(gen)   # clean re-read of OUTPUT
    text=tok.decode(gen,skip_special_tokens=False)
    print(f"\n[{label} L_inj={L_inj} coef={coef}] CLEAN-OUTPUT E114 W={Wc:.4f} S={Sc:.3f} Gcluster={gcl:.3f} ngen={len(gen)}",flush=True)
    print(f"   TEXT: {text[:300].strip()!r}",flush=True)
    results.append(dict(label=label,L_inj=L_inj,coef=coef,W_clean=Wc,S_clean=Sc,gcluster_clean=gcl,ngen=len(gen),text=text))

run(0,0.0,"BASELINE")
print("\n========== GOD-DIRECTION LAYER-DEPTH SWEEP (clean output readout) ==========")
for L in INJ_LAYERS: run(L, COEF, "GOD")
json.dump(results,open(OUT/"steer_layers.json","w"),indent=1)
print("\nSTEER_LAYERS_OK")
