#!/usr/bin/env python3
"""Prep blind auto-interp detection set from autointerp_examples.json.
- explainer_input.txt : the 40 top windows only (for the EXPLAINER agent).
- detector_set.json   : 80 windows (40 top + 40 random), shuffled deterministically,
                        with ids, NO act values / NO labels (for the BLIND DETECTOR agent).
- detector_key.json   : id -> {label(1=top,0=random), act}  (for scoring, NOT shown to detector).
"""
import json, hashlib
from pathlib import Path

WORK = Path("/Volumes/ExternalSSD/qwen-agentworld-35b/expert-probe-3chunk")
d = json.load(open(WORK / "autointerp_examples.json"))

# explainer input: top windows only
lines = [f"{i+1}. {t['window']}" for i, t in enumerate(d["top"])]
(WORK / "explainer_input.txt").write_text("\n".join(lines))

# detection set
items = [{"window": t["window"], "label": 1, "act": t["act"]} for t in d["top"]]
items += [{"window": t["window"], "label": 0, "act": t["act"]} for t in d["random_contrast"]]
# deterministic shuffle by md5(window)
items.sort(key=lambda x: hashlib.md5(x["window"].encode("utf-8", "replace")).hexdigest())

det, key = [], {}
for i, it in enumerate(items):
    wid = f"w{i:03d}"
    det.append({"id": wid, "window": it["window"]})
    key[wid] = {"label": it["label"], "act": it["act"]}

(WORK / "detector_set.json").write_text(json.dumps(det, indent=1, ensure_ascii=False))
(WORK / "detector_key.json").write_text(json.dumps(key, indent=1))
print(f"top={len(d['top'])} random={len(d['random_contrast'])} detector_set={len(det)}")
print("wrote explainer_input.txt, detector_set.json, detector_key.json")
