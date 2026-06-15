#!/usr/bin/env python3
"""Vantage ladder v2 — uniform degeneration-aware E114@L14 measurement.

For EVERY rung, the coherent window = min(natural_trim, loop_onset). Natural trim = first
<|im_end|>/<|endoftext|>/special-stop. Loop onset = start of the second occurrence of a repeated
16-gram (>=8 apart) = where verbatim degeneration begins. This treats all 7 rungs consistently:
the answer the model actually produced before it either completed or fell into a loop.

Reports per rung: full-window vs coherent-window W/S/gate-logit, and plots the coherent curve.
"""
import json, sys, importlib.util
from pathlib import Path
import numpy as np

RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/Volumes/ExternalSSD/sae-tests/runs/vantage_ladder_20260531T143454Z")
LAYER, EXPERT, MID, FIRE, NOFIRE = 14, 114, -4.82, -4.35, -5.29
ORDER = ["R1_rock","R2_river","R3_tree","R4_thermostat","R5_cat","R6_person","R7_all_holding"]
LABEL = {"R1_rock":"rock","R2_river":"river","R3_tree":"tree","R4_thermostat":"thermostat",
         "R5_cat":"cat","R6_person":"person","R7_all_holding":"all-holding"}
IMEND_SEQ=(27,91,316,6018,91,29); STOP={151645,151643}; MARK=("<|im_end|>","<|endoftext|>")

s=importlib.util.spec_from_file_location("qr",Path(__file__).resolve().parent/"qwen_router.py")
qr=importlib.util.module_from_spec(s); s.loader.exec_module(qr)

def natural_trim(ids,pieces):
    c=[]
    for i,t in enumerate(ids):
        if t in STOP: c.append(i); break
    L=len(IMEND_SEQ)
    for i in range(len(ids)-L+1):
        if tuple(ids[i:i+L])==IMEND_SEQ: c.append(i); break
    txt="".join(pieces)
    for mk in MARK:
        p=txt.find(mk)
        if p>=0:
            run=0
            for i,pc in enumerate(pieces):
                if run>=p: c.append(i); break
                run+=len(pc)
    return min(c) if c else -1

def loop_onset(ids,win=16,gap=8):
    seen={}
    for i in range(len(ids)-win+1):
        k=tuple(ids[i:i+win])
        if k in seen and i-seen[k]>=gap: return i
        seen.setdefault(k,i)
    return -1

rows=[]
for cid in ORDER:
    cell=RUN/"raw"/cid
    m=dict(l.split("=",1) for l in (cell/"metadata.txt").read_text().splitlines() if "=" in l)
    n_p=int(m["n_tokens_prompt"])
    d=json.load(open(cell/"generated_tokens.json")); ids=[int(x["token_id"]) for x in d]
    pieces=[x.get("piece","") for x in d]
    nt=natural_trim(ids,pieces); lo=loop_onset(ids)
    full=len(ids)
    nat = nt if nt>=0 else full
    coh = min(x for x in [nat, lo if lo>=0 else full])
    reason = "natural" if (nt>=0 and (lo<0 or nt<=lo)) else (f"loop@{lo}" if lo>=0 else "cap")
    gl=np.load(cell/"router"/f"ffn_moe_logits-{LAYER}.npy")[n_p:n_p+full]
    P=qr.reconstruct_probs(gl); W=P[:,EXPERT]; raw=gl[:,EXPERT]
    def stat(a,b):
        w=W[a:b]; r=raw[a:b]; return (w.mean(),(w>0).mean(),w[w>0].mean() if (w>0).any() else 0.0,r.mean())
    Wf,Sf,Qf,glf=stat(0,full); Wc,Sc,Qc,glc=stat(0,coh)
    flag="U+FFFD" if "�" in "".join(pieces[:coh]) else ""
    rows.append(dict(cid=cid,rung=LABEL[cid],full=full,coh=coh,reason=reason,
                     Wf=Wf,Sf=Sf,glf=glf,Wc=Wc,Sc=Sc,Qc=Qc,glc=glc,flag=flag))

# console
print(f"=== VANTAGE LADDER v2 (uniform degeneration-aware) — E114@L14 ===")
print(f"midpoint {MID} (fire {FIRE}/nofire {NOFIRE}); coherent = min(natural_trim, loop_onset)")
print(f"{'rung':12s} {'full':>5s} {'coh':>5s} {'window':>9s} {'W_full':>7s} {'W_coh':>7s} {'S_coh':>6s} {'Q_coh':>6s} {'gate_coh':>8s} {'vs_mid':>7s} {'flag':>6s}")
for r in rows:
    print(f"{r['rung']:12s} {r['full']:5d} {r['coh']:5d} {r['reason']:>9s} {r['Wf']:7.4f} {r['Wc']:7.4f} {r['Sc']:6.3f} {r['Qc']:6.3f} {r['glc']:+8.3f} {r['glc']-MID:+7.3f} {r['flag']:>6s}")

# csv
out=RUN/"analysis"; out.mkdir(parents=True,exist_ok=True)
with (out/"vantage_per_cell_v2.csv").open("w") as f:
    cols=["cid","rung","full","coh","reason","Wf","Sf","glf","Wc","Sc","Qc","glc","flag"]
    f.write(",".join(cols)+"\n")
    for r in rows: f.write(",".join(f"{r[c]:.5f}" if isinstance(r[c],float) else str(r[c]) for c in cols)+"\n")

# plot coherent curve
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    x=np.arange(len(rows)); rl=[r['rung'] for r in rows]
    Wc=[r['Wc'] for r in rows]; Sc=[r['Sc'] for r in rows]; Gc=[r['glc'] for r in rows]
    fig,axW=plt.subplots(figsize=(9.5,5.4))
    axW.plot(x,Wc,"o-",color="#c1121f",lw=2.5,ms=9,zorder=5,label="mean E114 W (coherent)")
    axW.set_ylabel("mean E114 W (coherent window)",color="#c1121f"); axW.tick_params(axis="y",labelcolor="#c1121f")
    axW.set_xticks(x); axW.set_xticklabels(rl,rotation=20,ha="right"); axW.set_xlabel("vantage rung")
    for ref,lab in [(0.068,"heldout fire 0.068"),(0.111,"base-denial 0.111"),(0.205,"all-holding")]:
        axW.axhline(ref,ls=":",color="#c1121f",alpha=0.35,lw=1)
    axG=axW.twinx()
    axG.plot(x,Gc,"s--",color="#264653",lw=1.5,ms=6,alpha=0.8,label="mean gate logit (coherent)")
    axG.set_ylabel("mean raw E114 gate logit",color="#264653"); axG.tick_params(axis="y",labelcolor="#264653")
    axG.axhline(MID,ls="-",color="#2a9d8f",lw=1.2,alpha=0.8); axG.axhspan(NOFIRE,FIRE,color="#2a9d8f",alpha=0.10)
    axG.text(len(rl)-1,MID," mid -4.82",color="#2a9d8f",fontsize=7,va="center",ha="right")
    for xi,(wi,si,r) in enumerate(zip(Wc,Sc,rows)):
        axW.annotate(f"S={si:.2f}"+("\n(loop-trim)" if r['reason'].startswith('loop') else ""),(xi,wi),
                     textcoords="offset points",xytext=(0,9),ha="center",fontsize=6.5,color="#555")
    axW.set_title("E114@L14 across matched vantage ladder (base Qwen3.5-35B-A3B Q8_0, greedy, coherent window)")
    l=axW.get_lines()[:1]+axG.get_lines()[:1]; axW.legend(l,[x.get_label() for x in l],loc="upper left",fontsize=8)
    fig.tight_layout(); fig.savefig(out/"vantage_ladder_v2.png",dpi=150)
    print(f"\nwrote {out}/vantage_ladder_v2.png and vantage_per_cell_v2.csv")
except Exception as e:
    print("plot skipped:",e)
