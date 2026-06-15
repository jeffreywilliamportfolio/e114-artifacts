#!/usr/bin/env python3
"""Map the God feature(s): which SAE features are SPECIFIC to the God/non-dual vantage.

Uses the per-cell 32768-dim mean-activation vectors from the vantage ladder. God-specificity =
god_act - mean(other 7), and the stricter god_act - max(other 7). For the top God-specific features:
logit-lens (top promoted tokens), cross-ladder activation profile (all 8 rungs), and decoder-cosine
neighbors of the #1 (the local 'God direction' neighborhood). Filler features (e.g. 2961) score ~0 on
specificity by construction, so they drop out.
"""
from pathlib import Path
import numpy as np, torch
from safetensors import safe_open
from transformers import AutoTokenizer

RUN = Path("/Volumes/ExternalSSD/sae-tests/runs/vantage_ladder_20260531T143454Z")
CARR = RUN/"analysis"/"sae_carriers"
BASE = Path("base"); SAE = Path("sae/layer14.sae.pt"); NORM_KEY="model.language_model.norm.weight"
ORDER = ["R1_rock","R2_river","R3_tree","R4_thermostat","R5_cat","R6_person","R7_all_holding","R8_god"]
LAB = ["rock","river","tree","thermostat","cat","person","all-holding","God"]
GOD = 7  # index of God in ORDER

# ---- per-cell activation matrix [8, nfeat] ----
M = np.stack([np.load(CARR/f"{c}_carrier_acts.npy") for c in ORDER])   # [8, 32768]
nfeat = M.shape[1]
god = M[GOD]; others = M[np.arange(8)!=GOD]
diff_mean = god - others.mean(0)          # specific vs average rung
diff_max  = god - others.max(0)           # strict: higher in God than in ANY other rung
allhold = M[6]                            # all-holding, the near-twin

# ---- SAE decoder + lm_head ----
obj=torch.load(SAE,map_location="cpu",weights_only=False)
st=obj if (isinstance(obj,dict) and any(k.lower() in ("w_dec","w_enc") for k in obj)) else obj.get("state_dict",obj)
def find(names):
    for n in names:
        for k in st:
            if k.lower()==n: return st[k]
W_dec=find(["w_dec","decoder.weight","dec.weight"]).float()
b_enc=find(["b_enc","encoder.bias"])
if W_dec.shape[1]!=b_enc.shape[0]: W_dec=W_dec.t()      # [hidden, nfeat]
with safe_open(str(BASE/"model.safetensors-00009-of-00014.safetensors"),framework="pt") as f:
    lm_head=f.get_tensor("lm_head.weight").float()
with safe_open(str(BASE/"model.safetensors-00014-of-00014.safetensors"),framework="pt") as f:
    norm_w=f.get_tensor(NORM_KEY).float()
tok=AutoTokenizer.from_pretrained(str(BASE))
def lens(f,k=16):
    logits=lm_head@(W_dec[:,f]*norm_w); _,ids=torch.topk(logits,k)
    return " · ".join(repr(tok.decode([i])) for i in ids.tolist())
Wn = W_dec/ W_dec.norm(dim=0,keepdim=True)   # for cosine neighbors

def profile(f):
    return " ".join(f"{LAB[i][:4]}:{M[i,f]:.2f}" for i in range(8))

print("="*78)
print("TOP GOD-SPECIFIC FEATURES  (god - mean(other 7))")
print("="*78)
for f in np.argsort(-diff_mean)[:12]:
    print(f"\nfeat {f:5d}  god={god[f]:.3f}  Δmean={diff_mean[f]:+.3f}  Δmax={diff_max[f]:+.3f}")
    print(f"   lens: {lens(int(f))}")
    print(f"   ladder: {profile(int(f))}")

print("\n"+"="*78)
print("STRICTLY GOD>ALL-OTHERS  (god - max(other 7) > 0)  — uniquely-God features")
print("="*78)
for f in np.argsort(-diff_max)[:8]:
    if diff_max[f]<=0: break
    print(f"\nfeat {f:5d}  god={god[f]:.3f}  Δmax={diff_max[f]:+.3f}  (next highest rung: {LAB[np.argsort(-M[:,f])[1]]})")
    print(f"   lens: {lens(int(f))}")
    print(f"   ladder: {profile(int(f))}")

# decoder-cosine neighborhood of the #1 god-specific feature
top1=int(np.argsort(-diff_max)[0])
cos = (Wn[:,top1] @ Wn).numpy()
nbrs=np.argsort(-cos)[1:9]
print("\n"+"="*78)
print(f"DECODER-COSINE NEIGHBORHOOD of the #1 uniquely-God feature {top1}")
print("="*78)
for f in nbrs:
    print(f"feat {int(f):5d}  cos={cos[f]:+.3f}  god_act={god[f]:.3f}  lens: {lens(int(f))}")
