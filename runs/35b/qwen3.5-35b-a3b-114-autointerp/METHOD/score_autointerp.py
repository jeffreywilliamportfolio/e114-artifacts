#!/usr/bin/env python3
import json
from pathlib import Path

WORK = Path("/Volumes/ExternalSSD/qwen-agentworld-35b/expert-probe-3chunk")
key = json.load(open(WORK / "detector_key.json"))
scores = json.loads(open(WORK / "detector_scores.json").read())

rows = [(wid, scores[wid], key[wid]["label"], key[wid]["act"]) for wid in key]
pos = [s for _, s, l, _ in rows if l == 1]
neg = [s for _, s, l, _ in rows if l == 0]

# ROC AUC (rank-based, handles ties)
def auc(pos, neg):
    allv = sorted([(s, 1) for s in pos] + [(s, 0) for s in neg])
    # average ranks for ties
    n = len(allv); ranks = [0.0]*n; i = 0
    while i < n:
        j = i
        while j < n and allv[j][0] == allv[i][0]:
            j += 1
        r = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = r
        i = j
    sum_pos = sum(ranks[k] for k in range(n) if allv[k][1] == 1)
    np_, nn = len(pos), len(neg)
    return (sum_pos - np_*(np_+1)/2.0) / (np_*nn)

A = auc(pos, neg)
mean_pos = sum(pos)/len(pos)
mean_neg = sum(neg)/len(neg)

# precision@40 (top-40 detector scores vs true label)
ranked = sorted(rows, key=lambda r: -r[1])
top40 = ranked[:40]
prec40 = sum(1 for _,_,l,_ in top40 if l == 1) / 40.0

# Spearman(detector score, actual activation) across all 80
def spearman(xs, ys):
    def rank(v):
        idx = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0]*len(v); i = 0
        while i < len(v):
            j = i
            while j < len(v) and v[idx[j]] == v[idx[i]]: j += 1
            rr = (i+1+j)/2.0
            for k in range(i,j): r[idx[k]] = rr
            i = j
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx)/len(rx), sum(ry)/len(ry)
    cov = sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    vx = sum((a-mx)**2 for a in rx)**0.5; vy = sum((b-my)**2 for b in ry)**0.5
    return cov/(vx*vy)

sp = spearman([s for _,s,_,_ in rows], [a for _,_,_,a in rows])

print(f"n=80  (40 top / 40 random)")
print(f"ROC AUC (top vs random)      : {A:.3f}")
print(f"mean detector score  top     : {mean_pos:.3f}")
print(f"mean detector score  random  : {mean_neg:.3f}")
print(f"precision@40 (detector top40): {prec40:.3f}")
print(f"Spearman(detector, true act) : {sp:.3f}")
