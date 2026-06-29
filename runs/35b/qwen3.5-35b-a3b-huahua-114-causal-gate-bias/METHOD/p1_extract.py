#!/usr/bin/env python3
"""Per-condition x per-prompt L14 routing signature for E114 (and the control expert).
S = mean softmax prob; Q = top-8 selection freq; W = mean routed (top-8 renormalized) weight.
Confirms suppression -> S/W -> 0, boost -> saturation. Reads npy BEFORE the orchestrator deletes them."""
import sys, glob, os, json
import numpy as np

WORK = sys.argv[1]
CTRL = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].lstrip("-").isdigit() else None
GLOB = sys.argv[3] if len(sys.argv) > 3 else "cap_p1_*"
CLUSTER = [114, 87, 170, 68]

def metrics(lg, e):
    if lg.ndim == 1:
        lg = lg[None, :]
    m = lg.max(1, keepdims=True); ex = np.exp(lg - m); p = ex / ex.sum(1, keepdims=True)
    S = float(p[:, e].mean())
    idx = np.argpartition(lg, -8, axis=1)[:, -8:]          # top-8 expert indices per token
    sel = (idx == e).any(1)
    Q = float(sel.mean())
    T = lg.shape[0]; Wsum = 0.0
    for r in np.where(sel)[0]:
        t8 = lg[r, idx[r]]; ee = np.exp(t8 - t8.max()); w = ee / ee.sum()
        Wsum += float(w[np.where(idx[r] == e)[0][0]])
    return {"S": round(S, 5), "Q": round(Q, 5), "W": round(Wsum / T, 6)}

out = {}
for d in sorted(glob.glob(os.path.join(WORK, GLOB))):
    lbl = os.path.basename(d).replace("cap_p1_", "").replace("cap_p1b_", "")
    out[lbl] = {}
    for f in glob.glob(os.path.join(d, "**", "ffn_moe_logits-14.npy"), recursive=True):
        pid = os.path.relpath(f, d).split(os.sep)[0]
        lg = np.load(f)
        rec = {"e114": metrics(lg, 114)}
        if CTRL is not None:
            rec[f"ctrl{CTRL}"] = metrics(lg, CTRL)
        out[lbl][pid] = rec
print(json.dumps(out, indent=1))
