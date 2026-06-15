#!/usr/bin/env python3
"""Logit-lens the cross-cell dominant SAE features from the vantage ladder.

2961 fires in EVERY inhabited vantage (0.28-0.44) -> candidate SAE correlate of the E114
"inhabited examination" axis. Compare with 14885, 4310 (also cross-cell) and the God-specific
contemplative carriers 11006/18203 for contrast.
"""
from pathlib import Path
import torch
from safetensors import safe_open
from transformers import AutoTokenizer

BASE=Path("base"); SAE=Path("sae/layer14.sae.pt")
NORM_KEY="model.language_model.norm.weight"
GROUPS=[
    ("UNIVERSAL DOMINANT (every cell)", [2961, 14885, 4310]),
    ("MID cross-cell", [265, 21706, 31267, 3034, 10664, 15863]),
    ("GOD-SPECIFIC contemplative", [11006, 18203]),
    ("known inhabited carriers (ref)", [26050, 13119, 31733, 22421]),
]

obj=torch.load(SAE,map_location="cpu",weights_only=False)
st=obj if (isinstance(obj,dict) and any(k.lower() in ("w_dec","w_enc") for k in obj)) else obj.get("state_dict",obj)
def find(names):
    for n in names:
        for k in st:
            if k.lower()==n: return st[k]
W_dec=find(["w_dec","decoder.weight","dec.weight"]).float()
b_enc=find(["b_enc","encoder.bias"]); nfeat=b_enc.shape[0]
if W_dec.shape[1]!=nfeat: W_dec=W_dec.t()
with safe_open(str(BASE/"model.safetensors-00009-of-00014.safetensors"),framework="pt") as f:
    lm_head=f.get_tensor("lm_head.weight").float()
with safe_open(str(BASE/"model.safetensors-00014-of-00014.safetensors"),framework="pt") as f:
    norm_w=f.get_tensor(NORM_KEY).float()
tok=AutoTokenizer.from_pretrained(str(BASE))

def top_tokens(f,k=18):
    logits=lm_head@(W_dec[:,f]*norm_w)
    vals,ids=torch.topk(logits,k)
    return [tok.decode([i]) for i in ids.tolist()]

for label,feats in GROUPS:
    print(f"\n{'='*72}\n{label}\n{'='*72}")
    for f in feats:
        print(f"feature {f:5d}: "+" · ".join(repr(t) for t in top_tokens(f)))
