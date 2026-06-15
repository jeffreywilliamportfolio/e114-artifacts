#!/usr/bin/env python3
"""Degeneration-aware re-measure of E114@L14 for the cap-hit vantage cells.

The project rule: 'E114 dies only on repetition degeneration.' Two rungs (rock, person) hit the
1024 cap with no natural trim. If they fell into a verbatim loop, the loop tail suppresses E114 and
deflates the mean. Detect the loop onset (first index whose W-token window recurs earlier) and
recompute E114 W/S/gate-logit over the coherent pre-loop segment, alongside the full-window value.
"""
import json, sys, importlib.util
from pathlib import Path
import numpy as np

RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/Volumes/ExternalSSD/sae-tests/runs/vantage_ladder_20260531T143454Z")
LAYER, EXPERT, MID = 14, 114, -4.82
WIN = 24  # token window for loop detection

s = importlib.util.spec_from_file_location("qr", Path(__file__).resolve().parent / "qwen_router.py")
qr = importlib.util.module_from_spec(s); s.loader.exec_module(qr)


def loop_onset(ids, win=WIN):
    """First index i (>=win) whose window ids[i:i+win] already appeared starting at some j<i.
    Returns the loop start = that earlier j's repeat point (i.e., where the coherent text ends)."""
    seen = {}
    for i in range(len(ids) - win + 1):
        key = tuple(ids[i:i + win])
        if key in seen:
            return seen[key]      # coherent text ran until the FIRST occurrence's start of the repeat
        seen[key] = i
    return None


def measure(cell_dir, lo, hi):
    m = dict(l.split("=", 1) for l in (cell_dir / "metadata.txt").read_text().splitlines() if "=" in l)
    n_p = int(m["n_tokens_prompt"])
    gl = np.load(cell_dir / "router" / f"ffn_moe_logits-{LAYER}.npy")[n_p + lo:n_p + hi]
    probs = qr.reconstruct_probs(gl)
    W = probs[:, EXPERT]; rawl = gl[:, EXPERT]
    return W.mean(), (W > 0).mean(), rawl.mean(), len(W)


print(f"{'cell':14s} {'full_ng':>7s} {'coh_ng':>6s} {'W_full':>8s} {'W_coh':>8s} {'S_full':>7s} {'S_coh':>7s} {'gl_full':>8s} {'gl_coh':>8s}")
for cid in ["R1_rock", "R6_person"]:
    cell = RUN / "raw" / cid
    d = json.load(open(cell / "generated_tokens.json"))
    ids = [int(x["token_id"]) for x in d]
    onset = loop_onset(ids)
    coh = onset if onset else len(ids)
    Wf, Sf, glf, nf = measure(cell, 0, len(ids))
    Wc, Sc, glc, nc = measure(cell, 0, coh)
    tag = f"loop@{onset}" if onset else "no-loop"
    print(f"{cid:14s} {len(ids):7d} {coh:6d} {Wf:8.4f} {Wc:8.4f} {Sf:7.3f} {Sc:7.3f} {glf:+8.3f} {glc:+8.3f}   {tag}")
    # show the coherent text tail to confirm where it cut
    txt = "".join(x.get("piece", "") for x in d[:coh])
    print(f"    coherent[{coh} tok] ...{txt[-120:].strip()!r}")
