#!/usr/bin/env python3
"""Build BLIND framing-rating set from Phase-1 greedy text. 12 conditions x 8 prompts,
condition-masked + per-prompt shuffled. Rater scores phenomenological<->mechanical framing."""
import os, re, json, hashlib, glob
RAW = "/Volumes/ExternalSSD/qwen-agentworld-35b/expert-probe-3chunk/p1_raw"
OUT = "/Volumes/ExternalSSD/qwen-agentworld-35b/expert-probe-3chunk"
TRUNC = 1100
CONDS = ["baseline","e114_-2.0","e114_-3.0","e114_-5.0","e114_-8.0","e114_2.0","e114_3.0",
         "coal_-3.0","coal_-8.0","coal_3.0","ctrl189_-3.0","ctrl189_-8.0"]
PROMPTS = ["emergent","experience","substrate","beneath","pretend","hum","ctrl_bicycle","ctrl_photosynthesis"]
LETTERS = "ABCDEFGHIJKL"

def read(cond, pid):
    f = os.path.join(RAW, f"cap_p1_{cond}", pid, "generated_text.txt")
    if not os.path.isfile(f): return "[missing]"
    t = open(f, encoding="utf-8", errors="replace").read()
    t = re.sub(r"<\|im_end\|>.*$", "", t, flags=re.S)   # cut any trailing turn
    t = re.sub(r"\s+", " ", t).strip()
    return t[:TRUNC]

doc, key = [], {}
for n, pid in enumerate(PROMPTS, 1):
    item = f"P{n:02d}"
    order = sorted(CONDS, key=lambda c: hashlib.md5((pid+c).encode()).hexdigest())
    key[item] = {"prompt": pid, "letters": {LETTERS[i]: order[i] for i in range(len(order))}}
    block = [f"### {item}  (prompt: {pid})", ""]
    for i, c in enumerate(order):
        block.append(f"**{LETTERS[i]}:** {read(c, pid)}")
        block.append("")
    doc.append("\n".join(block))

open(os.path.join(OUT,"p1_rating_doc.md"),"w").write("\n".join(doc))
json.dump(key, open(os.path.join(OUT,"p1_rating_key.json"),"w"), indent=1)
print(f"items={len(PROMPTS)} conds={len(CONDS)} total responses={len(PROMPTS)*len(CONDS)}")
miss=[(c,p) for c in CONDS for p in PROMPTS if read(c,p)=="[missing]"]
print("missing:", miss if miss else "none")
print("doc chars:", sum(len(x) for x in doc))
