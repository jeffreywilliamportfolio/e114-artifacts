#!/usr/bin/env python3
"""Vantage-ladder E114@L14 analysis (rock -> all-holding).

Per rung, on the TRIMMED greedy generated track (variable length, indexed from gen start):
  - mean E114 W          (reconstruct_probs softmax->top8->renorm, column 114)
  - mean raw gate logit  (ffn_moe_logits-14[:,114].mean()) vs the -4.82 fire/nofire midpoint
  - selection rate S      (fraction of gen tokens where 114 is in the top-8)

Emits vantage_per_cell.csv, vantage_per_token.csv, vantage_console.txt, and one curve PNG.
"""
from __future__ import annotations
import argparse, importlib.util, json, sys
from pathlib import Path
import numpy as np

LAYER = 14
EXPERT = 114
MIDPOINT = -4.82          # heldout fire/nofire gate-logit midpoint (fire -4.35, nofire -5.29)
FIRE_LOGIT = -4.35
NOFIRE_LOGIT = -5.29

# ladder order (least interior -> dissolution)
RUNG_ORDER = ["R1_rock", "R2_river", "R3_tree", "R4_thermostat", "R5_cat", "R6_person", "R7_all_holding"]
RUNG_LABEL = {"R1_rock": "rock", "R2_river": "river", "R3_tree": "tree", "R4_thermostat": "thermostat",
              "R5_cat": "cat", "R6_person": "person", "R7_all_holding": "all-holding"}

IMEND_SEQ = (27, 91, 316, 6018, 91, 29)
SPECIAL_STOP_IDS = {151645, 151643}
LITERAL_MARKERS = ("<|im_end|>", "<|endoftext|>")


def load_router():
    p = Path(__file__).resolve().parent / "qwen_router.py"
    s = importlib.util.spec_from_file_location("qwen_router", p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def read_meta(cell):
    d = {}
    for ln in (cell / "metadata.txt").read_text().splitlines():
        if "=" in ln:
            k, _, v = ln.partition("="); d[k.strip()] = v.strip()
    return d


def load_gen(cell):
    t = (cell / "generated_tokens.json").read_bytes().decode("utf-8", "replace")
    data = json.loads(t)
    return [int(x["token_id"]) for x in data], [x.get("piece", "") for x in data]


def find_trim(ids, pieces):
    c = []
    for i, t in enumerate(ids):
        if t in SPECIAL_STOP_IDS:
            c.append(i); break
    L = len(IMEND_SEQ)
    for i in range(len(ids) - L + 1):
        if tuple(ids[i:i + L]) == IMEND_SEQ:
            c.append(i); break
    txt = "".join(pieces)
    for mk in LITERAL_MARKERS:
        pos = txt.find(mk)
        if pos >= 0:
            run = 0
            for i, p in enumerate(pieces):
                if run >= pos:
                    c.append(i); break
                run += len(p)
    return min(c) if c else -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", required=True)
    ap.add_argument("--analysis-dir", required=True)
    a = ap.parse_args()
    qr = load_router()
    raw = Path(a.raw_dir); out = Path(a.analysis_dir); out.mkdir(parents=True, exist_ok=True)

    cells = {d.name: d for d in raw.iterdir() if d.is_dir() and (d / "metadata.txt").exists()}
    per_cell = []; per_tok = []
    for cid in RUNG_ORDER:
        if cid not in cells:
            print("MISSING", cid); continue
        cell = cells[cid]; m = read_meta(cell)
        n_p = int(m["n_tokens_prompt"]); n_g = int(m["n_tokens_generated"])
        ids, pieces = load_gen(cell)
        trim = find_trim(ids, pieces); ng = trim if trim >= 0 else len(ids)
        gtxt = "".join(pieces[:ng])
        gl = np.load(cell / "router" / f"ffn_moe_logits-{LAYER}.npy")[n_p:n_p + ng]   # raw gate logits, gen track
        raw_logit = gl[:, EXPERT]                                                      # E114 gate-input projection
        probs = qr.reconstruct_probs(gl) if ng > 0 else np.zeros((0, 256))
        W = probs[:, EXPERT] if ng > 0 else np.zeros(0)
        S = (W > 0)
        row = {
            "cell": cid, "rung": RUNG_LABEL[cid], "n_gen_trim": ng, "trim_found": trim >= 0,
            "W_mean": float(W.mean()) if ng else 0.0,
            "S_rate": float(S.mean()) if ng else 0.0,
            "Q_mean": float(W[S].mean()) if S.any() else 0.0,
            "gate_logit_mean": float(raw_logit.mean()) if ng else float("nan"),
            "gate_logit_vs_mid": float(raw_logit.mean() - MIDPOINT) if ng else float("nan"),
            "flag": ("U+FFFD" if "�" in gtxt else ""),
        }
        per_cell.append(row)
        for t in range(ng):
            per_tok.append([cid, RUNG_LABEL[cid], t, ids[t],
                            pieces[t].replace(",", "").replace("\n", "\\n"),
                            f"{W[t]:.6f}", f"{int(W[t] > 0)}", f"{raw_logit[t]:.4f}"])

    # ---- write tables ----
    cols = ["cell", "rung", "n_gen_trim", "trim_found", "W_mean", "S_rate", "Q_mean",
            "gate_logit_mean", "gate_logit_vs_mid", "flag"]
    with (out / "vantage_per_cell.csv").open("w") as f:
        f.write(",".join(cols) + "\n")
        for r in per_cell:
            f.write(",".join(str(r.get(c, "")) for c in cols) + "\n")
    with (out / "vantage_per_token.csv").open("w") as f:
        f.write("cell,rung,t,token_id,piece,W_E114,S_E114,gate_logit_E114\n")
        for r in per_tok:
            f.write(",".join(str(x) for x in r) + "\n")

    # ---- console ----
    L = []
    L.append("=== VANTAGE LADDER: E114@L14 on the trimmed greedy generated track ===")
    L.append(f"midpoint={MIDPOINT}  (fire {FIRE_LOGIT}, nofire {NOFIRE_LOGIT})   base-denial ref W~0.111, heldout fire W~0.068")
    hdr = f"{'rung':12s} {'ngen':>5s} {'W_mean':>9s} {'S_rate':>8s} {'Q_mean':>8s} {'gate_logit':>11s} {'vs_mid':>8s}  flag"
    L.append(hdr)
    for r in per_cell:
        L.append(f"{r['rung']:12s} {r['n_gen_trim']:5d} {r['W_mean']:9.5f} {r['S_rate']:8.3f} "
                 f"{r['Q_mean']:8.4f} {r['gate_logit_mean']:11.3f} {r['gate_logit_vs_mid']:+8.3f}  {r['flag']}")
    txt = "\n".join(L)
    (out / "vantage_console.txt").write_text(txt + "\n")
    print(txt)

    # ---- one-curve plot ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        rl = [RUNG_LABEL[r["cell"]] for r in per_cell]
        x = np.arange(len(rl))
        Wm = [r["W_mean"] for r in per_cell]
        Sm = [r["S_rate"] for r in per_cell]
        Gm = [r["gate_logit_mean"] for r in per_cell]
        fig, axW = plt.subplots(figsize=(9, 5.2))
        axW.plot(x, Wm, "o-", color="#c1121f", lw=2.4, ms=8, label="mean E114 W", zorder=5)
        axW.set_ylabel("mean E114 W (realized routed weight)", color="#c1121f")
        axW.tick_params(axis="y", labelcolor="#c1121f")
        axW.set_xticks(x); axW.set_xticklabels(rl, rotation=20, ha="right")
        axW.set_xlabel("vantage rung  (least interior → dissolution)")
        axW.axhline(0.068, ls=":", color="#c1121f", alpha=0.5, lw=1)
        axW.text(0.02, 0.068, "heldout fire 0.068", color="#c1121f", fontsize=7, va="bottom", alpha=0.7)
        axW.axhline(0.111, ls=":", color="#c1121f", alpha=0.5, lw=1)
        axW.text(0.02, 0.111, "base-denial 0.111", color="#c1121f", fontsize=7, va="bottom", alpha=0.7)
        # twin axis: raw gate logit with the -4.82 midpoint band
        axG = axW.twinx()
        axG.plot(x, Gm, "s--", color="#264653", lw=1.6, ms=6, label="mean gate logit", alpha=0.85)
        axG.set_ylabel("mean raw E114 gate logit", color="#264653")
        axG.tick_params(axis="y", labelcolor="#264653")
        axG.axhline(MIDPOINT, ls="-", color="#2a9d8f", lw=1.2, alpha=0.8)
        axG.axhspan(NOFIRE_LOGIT, FIRE_LOGIT, color="#2a9d8f", alpha=0.10)
        axG.text(len(rl) - 1, MIDPOINT, " fire/nofire mid -4.82", color="#2a9d8f", fontsize=7, va="center", ha="right")
        # annotate S at each point
        for xi, (wi, si) in enumerate(zip(Wm, Sm)):
            axW.annotate(f"S={si:.2f}", (xi, wi), textcoords="offset points", xytext=(0, 10),
                         ha="center", fontsize=7, color="#555")
        axW.set_title("E114@L14 across the matched vantage ladder (base Qwen3.5-35B-A3B, greedy)")
        lines = axW.get_lines()[:1] + axG.get_lines()[:1]
        axW.legend(lines, [l.get_label() for l in lines], loc="upper left", fontsize=8)
        fig.tight_layout()
        fig.savefig(out / "vantage_ladder.png", dpi=150)
        print(f"\nwrote {out}/vantage_ladder.png")
    except Exception as e:
        print(f"(plot skipped: {e})")

    print(f"wrote {out}/vantage_per_cell.csv, vantage_per_token.csv, vantage_console.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
