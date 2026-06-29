#!/usr/bin/env python3
"""Reproduce the E114 npz characterization (DOCS/RESULTS_e114_npz_characterization.md).

Reads the dense domain-specialist routing arrays and regenerates, for Expert 114:
  (1) the dual L14/L26 candidate-strength (S) layer profile and the L14<->L26
      domain-profile correlation;
  (2) the 20-domain selectivity ranking at L14;
  (3) the L14 co-activation structure (which experts' 20-domain L14 profile
      correlates with E114's), including the "philosophy cluster" check.

Metric S = mean candidate softmax probability (how strongly the expert wants to
fire). Track = generation, loop-trimmed. The .npz raw arrays are kept out of git by
policy; obtain them from the Zenodo tensor dataset (see ../../../../ZENODO-TENSORS.md)
or the local capture, then pass the path as argv[1].

Usage: python analyze_e114_npz.py results_domain_specialists_<stamp>.npz
"""
import sys
import numpy as np

E = 114
NPZ = sys.argv[1] if len(sys.argv) > 1 else "results_domain_specialists_20260408T235839Z.npz"

d = np.load(NPZ, allow_pickle=True)
S = d["generation_trimmed_domain_layer_S"]          # (20 domains, 40 layers, 256 experts)
domains = [str(x) for x in d["domains"]]            # len 20
n_dom, n_layer, n_exp = S.shape


def pearson(a, b):
    a = a - a.mean(); b = b - b.mean()
    denom = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / denom) if denom else float("nan")


# (1) E114 layer profile (mean over domains) + dual-readout check ----------------
layer_profile = S[:, :, E].mean(axis=0)            # (40,)
print("== E114 candidate-strength (S) by layer, mean over 20 domains ==")
for L in [12, 13, 14, 15, 16, 25, 26, 27]:
    print(f"  L{L:>2}: {layer_profile[L]:.3f}")
top2 = np.argsort(layer_profile)[::-1][:2]
print(f"  top-2 layers: {sorted(top2.tolist())}  (expected 14 and 26)")
r_1426 = pearson(S[:, 14, E], S[:, 26, E])
print(f"  L14<->L26 domain-profile Pearson r = {r_1426:+.3f}  (expected ~+0.99)\n")

# (2) Domain selectivity at L14 --------------------------------------------------
l14 = S[:, 14, E]                                   # (20,)
order = np.argsort(l14)[::-1]
print("== E114 @ L14 domain selectivity (S), generation ==")
for rank, i in enumerate(order, 1):
    print(f"  {rank:>2}. {domains[i]:<22} {l14[i]:.3f}")
print()

# (3) L14 co-activation structure ----------------------------------------------
corr = np.array([pearson(S[:, 14, e], l14) for e in range(n_exp)])
corr[E] = -np.inf                                   # exclude self from "top"
canonical = {68: "E68", 170: "E170", 87: "E87"}     # the prior "philosophy cluster" members
print("== prior 'philosophy cluster' 114+87+170+68 — L14 co-activation check ==")
for e, name in canonical.items():
    print(f"  {name}: r = {corr[e]:+.2f}")
print("  (expected E68 ~+0.46 co-varies; E170 ~+0.11 weak; E87 ~-0.29 ANTI)\n")
print("== true E114 L14 co-activators (top 8 by domain-profile correlation) ==")
for e in np.argsort(corr)[::-1][:8]:
    print(f"  E{e:<3} r = {corr[e]:+.2f}")
