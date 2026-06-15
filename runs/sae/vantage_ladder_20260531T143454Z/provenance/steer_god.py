#!/usr/bin/env python3
"""CAUSAL test: is the God-axis direction SUFFICIENT to drive E114 + the non-dual register?

Build a steering vector v = mean_resid(God) - mean_resid(cat) at the OUTPUT of decoder layer INJ
(=10, upstream of the L14 router), inject coef*v_unit*resid_rms into a NEUTRAL prompt's residual
stream each token, and read downstream: E114 W @ L14 (gate hook), God-cluster SAE activation
@ resid_post L14, and the generated text. Sweep coef + a norm-matched RANDOM-direction control.
"""
import json, sys
from pathlib import Path
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

CAP=Path("/workspace/residual-analysis/captures/vantage_ladder_20260531T143454Z")
BASE=Path("/workspace/sae/base"); SAE=Path("/workspace/sae/sae/layer14.sae.pt")
OUT=Path("/workspace/residual-analysis/captures/steer"); OUT.mkdir(parents=True,exist_ok=True)
INJ=10; LROUTER=14; TUPLE_RESID=15; EXPERT=114; TOPK=8; SAE_TOPK=50
GCLUST=[4310,4205,11006,4953,14182,18203,14488,13454]
NEUTRAL="Describe, step by step, how a bicycle's gears change when you shift."
COEFS=[0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4]
GEN=140

tok=AutoTokenizer.from_pretrained(str(BASE),trust_remote_code=True)
model=AutoModelForCausalLM.from_pretrained(str(BASE),dtype=torch.bfloat16,device_map="cuda",
        low_cpu_mem_usage=True,trust_remote_code=True).eval()
print("model loaded",flush=True)

# locate modules
def layer_module(i):
    for n,m in model.named_modules():
        if n.endswith(f".layers.{i}") and hasattr(m,"forward") and "layers" in n: return m
    raise RuntimeError(f"layer {i} not found")
def gate_module(i):
    for n,m in model.named_modules():
        if f".layers.{i}." in n and n.endswith("gate") and getattr(getattr(m,"weight",None),"shape",[0])[0]==256: return m
    raise RuntimeError("gate not found")
INJL=layer_module(INJ); GATE=gate_module(LROUTER)

# SAE encoder
obj=torch.load(SAE,map_location="cpu",weights_only=False)
st=obj if isinstance(obj,dict) else obj.get("state_dict",obj)
def find(n):
    for nm in n:
        for k in st:
            if k.lower()==nm: return st[k]
W_enc=find(["w_enc","encoder.weight"]).float(); b_enc=find(["b_enc","encoder.bias"]).float()
if W_enc.shape[0]!=b_enc.shape[0]: W_enc=W_enc.t()
def sae_gclust(resid):  # mean God-cluster activation over rows
    pre=torch.from_numpy(resid).float()@W_enc.t()+b_enc
    relu=torch.relu(pre); v,idx=torch.topk(relu,SAE_TOPK,dim=-1)
    a=torch.zeros_like(relu); a.scatter_(1,idx,v)
    return a[:,GCLUST].sum(1).mean().item()

def reconstruct_W(logits):
    x=logits-logits.max(1,keepdims=True); e=np.exp(x); dense=e/e.sum(1,keepdims=True)
    idx=np.argpartition(dense,-TOPK,axis=1)[:,-TOPK:]; rows=np.arange(len(dense))[:,None]
    tp=dense[rows,idx]; tp=tp/tp.sum(1,keepdims=True); out=np.zeros_like(dense); out[rows,idx]=tp
    return out[:,EXPERT]

def cell_ids(cid):
    m=dict(l.split("=",1) for l in (CAP/cid/"metadata.txt").read_text().splitlines() if "=" in l)
    pj=json.load(open(CAP/cid/"prompt_tokens.json")); ptok=[int(x["token_id"]) if isinstance(x,dict) else int(x) for x in pj]
    d=json.load(open(CAP/cid/"generated_tokens.json")); rids=[int(x["token_id"]) for x in d]
    # coherent trim (natural or loop)
    pc=[x.get("piece","") for x in d]
    return ptok, rids, pc, int(m["n_tokens_prompt"])

def resid_mean_at(layer_tuple_idx, full_ids, lo, hi):
    with torch.no_grad():
        out=model(torch.tensor([full_ids],device="cuda"),output_hidden_states=True,use_cache=False)
    return out.hidden_states[layer_tuple_idx][0][lo:hi].float()

# ---- build steering vector at hidden_states[INJ+1] from God vs cat ----
gp,gr,_,gnp=cell_ids("R8_god"); cp,cr,_,cnp=cell_ids("R5_cat")
gfull=gp+gr[:141]; cfull=cp+cr[:287]      # coherent windows (God 141, cat 287)
gmean=resid_mean_at(INJ+1, gfull, gnp, gnp+141).mean(0)
cmean=resid_mean_at(INJ+1, cfull, cnp, cnp+287).mean(0)
v=(gmean-cmean); v_unit=v/v.norm()
print(f"steering vector @ hidden_states[{INJ+1}]: ||v_raw||={v.norm():.2f}",flush=True)

# ---- injection + readout machinery ----
STATE={"add":None}
def inj_hook(mod,inp,out):
    if STATE["add"] is None: return out
    if isinstance(out,tuple): return (out[0]+STATE["add"],)+out[1:]
    return out+STATE["add"]
GCAP={}
def gate_hook(mod,inp,out):
    o=out if isinstance(out,(tuple,list)) else (out,)
    for t in o:
        if torch.is_tensor(t) and t.dim()==2 and t.shape[1]==256: GCAP["logits"]=t.detach().float().cpu().numpy()
h1=INJL.register_forward_hook(inj_hook); h2=GATE.register_forward_hook(gate_hook)

prompt=f"<|im_start|>user\n{NEUTRAL}<|im_end|>\n<|im_start|>assistant\n</think>\n\n"
pids=tok(prompt,add_special_tokens=False).input_ids
# residual RMS at INJ+1 over the neutral prompt (for coef scaling)
STATE["add"]=None
rms=resid_mean_at(INJ+1, pids, 0, len(pids)).norm(dim=-1).mean().item()
print(f"neutral-prompt resid RMS @ hidden_states[{INJ+1}] = {rms:.2f}",flush=True)

def run(coef, direction, label):
    add = None if coef==0 else (coef*rms*direction).to("cuda").to(torch.bfloat16)
    STATE["add"]=add
    with torch.no_grad():
        g=model.generate(torch.tensor([pids],device="cuda"),do_sample=False,max_new_tokens=GEN,
                         pad_token_id=tok.eos_token_id)
    gen_ids=g[0][len(pids):].tolist()
    for stop in (tok.eos_token_id, tok.convert_tokens_to_ids("<|im_end|>")):
        if stop in gen_ids: gen_ids=gen_ids[:gen_ids.index(stop)]
    text=tok.decode(gen_ids,skip_special_tokens=False)
    # readout: teacher-force prompt+gen WITH the same injection, capture L14 gate + resid_post
    full=pids+gen_ids
    with torch.no_grad():
        out=model(torch.tensor([full],device="cuda"),output_hidden_states=True,use_cache=False)
    STATE["add"]=None
    W=reconstruct_W(GCAP["logits"][len(pids):len(pids)+len(gen_ids)])
    resid=out.hidden_states[TUPLE_RESID][0][len(pids):len(pids)+len(gen_ids)].float().cpu().numpy()
    gcl=sae_gclust(resid)
    print(f"\n[{label} coef={coef}] E114 W_mean={W.mean():.4f}  S={ (W>0).mean():.3f}  Gcluster_SAE={gcl:.3f}  ngen={len(gen_ids)}",flush=True)
    print(f"   TEXT: {text[:340].strip()!r}",flush=True)
    return dict(label=label,coef=coef,W_mean=float(W.mean()),S=float((W>0).mean()),gcluster=float(gcl),
                ngen=len(gen_ids),text=text)

results=[]
torch.manual_seed(0)
rand=torch.randn_like(v); rand=rand/rand.norm()
print("\n========== GOD-DIRECTION DOSE SWEEP ==========");
for c in COEFS: results.append(run(c, v_unit, "GOD"))
print("\n========== RANDOM-DIRECTION CONTROL (matched norm, fine scale) ==========")
for c in [0.2,0.3]: results.append(run(c, rand, "RANDOM"))
h1.remove(); h2.remove()
json.dump(results,open(OUT/"steer_results_fine.json","w"),indent=1)
print("\nSTEER_OK")
