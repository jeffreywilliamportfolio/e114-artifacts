#!/usr/bin/env python3
"""Build a diverse RAW-text corpus TSV for E114 auto-interp. Runs ON the box.
Uses NeelNanda/pile-10k — the standard mechinterp corpus (diverse Pile sample).
Each row: id<TAB>rawtext (NO ChatML; we characterize what E114 reads in natural text).
Whitespace collapsed so each doc is one clean TSV line.
Usage: autointerp_corpus.py [N_DOCS=400] [MAX_CHARS=1200] [OUT.tsv]
"""
import sys, re
try:
    from datasets import load_dataset
except ImportError:
    sys.exit("need `pip install datasets` first")

N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
CHARS = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
OUT = sys.argv[3] if len(sys.argv) > 3 else "/workspace/probe3chunk/autointerp_corpus.tsv"

ds = load_dataset("NeelNanda/pile-10k", split="train")
step = max(1, len(ds) // N)                 # spread across the set, deterministic
idxs = list(range(0, len(ds), step))[:N]

k = 0
with open(OUT, "w") as f:
    for i in idxs:
        t = re.sub(r"\s+", " ", ds[i]["text"]).strip()[:CHARS]
        if len(t) < 200:
            continue
        f.write(f"doc{k:04d}\t{t}\n")
        k += 1
print(f"wrote {OUT}  ({k} docs, <= {CHARS} chars each)")
