#!/usr/bin/env python3
"""Pick the matched specificity-control expert: the non-cluster L14 expert whose mean baseline
activation (softmax prob) is closest to E114's. Prints the expert index."""
import sys, glob, os
import numpy as np
CLUSTER = {114, 87, 170, 68}
base = sys.argv[1]
files = glob.glob(os.path.join(base, "**", "ffn_moe_logits-14.npy"), recursive=True)
if not files:
    sys.exit(0)
acc = np.zeros(256, dtype=np.float64); n = 0
for f in files:
    lg = np.load(f)
    if lg.ndim == 1:
        lg = lg[None, :]
    m = lg.max(axis=1, keepdims=True)
    e = np.exp(lg - m); p = e / e.sum(axis=1, keepdims=True)
    acc += p.mean(axis=0); n += 1
mean = acc / max(n, 1)
e114 = mean[114]
cand = sorted((i for i in range(256) if i not in CLUSTER), key=lambda i: abs(mean[i] - e114))
print(cand[0])
