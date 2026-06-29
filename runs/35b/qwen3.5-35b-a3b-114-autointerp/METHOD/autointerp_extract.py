#!/usr/bin/env python3
"""Extract E114@L14 top-activating text contexts for auto-interp. Runs ON the box.
Per-token activation = softmax(ffn_moe_logits-14)[114] (continuous, pre-top8 "router wanted E114").
Emits autointerp_examples.json = the only thing we pull (small): top-K windows + random contrast
windows + activation stats. The activating token is wrapped in <<...>>.
Usage: autointerp_extract.py [WORK] [CAPDIR=cap_autointerp]
"""
import json, sys
from pathlib import Path
import numpy as np

WORK = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/workspace/probe3chunk")
CAP = WORK / (sys.argv[2] if len(sys.argv) > 2 else "cap_autointerp")
HE, LAYER = 114, 14
WIN = 12            # context tokens each side
TOPK = 40          # top-activating examples for the explainer
MAX_PER_DOC = 2    # diversity: cap examples from any single doc
NRAND = 40         # random/low contrast examples (for scoring)


def softmax(x):
    x = x - x.max(axis=1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=1, keepdims=True)


def fixb(s):
    # BPE pieces can split a multibyte UTF-8 char across tokens, so a single piece
    # may hold invalid-UTF-8 bytes. We read the JSON with surrogateescape (every byte
    # preserved as a surrogate), then re-serialize a joined span back to bytes and
    # decode as UTF-8 so split multibyte chars recombine; truly broken bytes -> U+FFFD.
    return s.encode("utf-8", "surrogateescape").decode("utf-8", "replace")


pieces_by_cell, acts = {}, []   # acts: list of (activation, cell, idx)
for cell in sorted(CAP.iterdir()):
    if not cell.is_dir():
        continue
    fp = cell / "router" / f"ffn_moe_logits-{LAYER}.npy"
    ptj = cell / "prompt_tokens.json"
    if not fp.exists() or not ptj.exists():
        continue
    logits = np.load(fp)
    if logits.ndim != 2 or logits.shape[1] <= HE:
        continue
    with open(ptj, encoding="utf-8", errors="surrogateescape") as fh:
        pieces = [t["piece"] for t in json.load(fh)]
    n = min(len(pieces), logits.shape[0])
    a = softmax(logits[:n].astype(np.float64))[:, HE]
    pieces_by_cell[cell.name] = pieces
    for i in range(1, n):                       # skip BOS (idx 0)
        acts.append((float(a[i]), cell.name, i))

if not acts:
    sys.exit("no activations found — check capture")

allv = np.array([a for a, _, _ in acts])
print(f"tokens: {len(acts)} | activation mean {allv.mean():.4f} "
      f"p50 {np.percentile(allv,50):.4f} p99 {np.percentile(allv,99):.4f} max {allv.max():.4f}")


def window(cell, i):
    p = pieces_by_cell[cell]
    lo, hi = max(0, i - WIN), min(len(p), i + WIN + 1)
    return fixb("".join(p[lo:i]) + " <<" + p[i].strip() + ">> " + "".join(p[i + 1:hi])).strip()


acts.sort(key=lambda r: -r[0])
top, per_doc = [], {}
for a, cell, i in acts:
    if per_doc.get(cell, 0) >= MAX_PER_DOC:
        continue
    per_doc[cell] = per_doc.get(cell, 0) + 1
    top.append({"act": round(a, 4), "doc": cell, "window": window(cell, i)})
    if len(top) >= TOPK:
        break

rng = np.random.default_rng(0)
mid = [r for r in acts if r[0] < np.percentile(allv, 80)]
ridx = rng.choice(len(mid), size=min(NRAND, len(mid)), replace=False)
rand = [{"act": round(mid[j][0], 4), "doc": mid[j][1], "window": window(mid[j][1], mid[j][2])}
        for j in ridx]

out = {
    "feature": "E114 @ L14", "metric": "softmax(router_logits)[114] per token",
    "n_tokens": len(acts), "n_docs": len(pieces_by_cell),
    "act_stats": {"mean": float(allv.mean()), "p50": float(np.percentile(allv, 50)),
                  "p99": float(np.percentile(allv, 99)), "max": float(allv.max())},
    "top": top, "random_contrast": rand,
}
dest = WORK / "autointerp_examples.json"
dest.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print("wrote", dest, "| top", len(top), "random", len(rand))
