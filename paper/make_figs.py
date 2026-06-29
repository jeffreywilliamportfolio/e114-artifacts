#!/usr/bin/env python3
"""
Figures for the E114 paper.

PROVENANCE / HONESTY NOTE
-------------------------
The raw per-token / per-prompt captures are NOT in the local tree (Vast.ai
instances destroyed; journal flags artifacts as "forthcoming"). Every value
plotted here is a number *explicitly reported* in the journals:
  - qwen/35b/JOURNAL-RESIDUAL-ANALYSIS.md          (heldout register/control realized W)
  - qwen/e114/JOURNAL-E114-CHARACTERIZATION.md     (vantage ladder; gate-lead tokens; SAE fade)
  - _absorption/NOTES.md                            (cross-check)
No individual data points are synthesized. Where only summary statistics exist
(class mean/sd), the figure shows the summary statistic, not invented points.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
import os

plt.rcParams.update({
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 7.5,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "pdf.fonttype": 42,
})

OUT = os.path.join(os.path.dirname(__file__), "figs")
os.makedirs(OUT, exist_ok=True)

INK = "#1b1b1b"
POS = "#b5341f"       # register-positive class
CTRL = "#3a6ea5"      # lexical-control class
ACC = "#5a5a5a"

# ---------------------------------------------------------------------------
# Figure 1: held-out register/control separability (realized routed weight W).
# Source: JOURNAL-RESIDUAL-ANALYSIS.md, heldout_20260417T202651Z.
#   Register: mean-of-means 0.067450, sd 0.030678 (n=10); F02 0.114997, F09 0.099708, F07 0.012168 (min)
#   Control : mean-of-means 0.003111, sd 0.004036 (n=10); N10 0.010456 (max)
#   no overlap: lowest register 0.012168 > highest control 0.010456 (margin 0.001711)
#   realized-W Cohen's d = 2.94 (this heldout); recovered w114 linear projection d = 3.88, no overlap
# ---------------------------------------------------------------------------
def fig_separability():
    # Two panels. RIGHT panel leads: the linear w114 axis (d=3.88, no overlap)
    # is the primary separability statistic; realized W is the secondary top-k
    # readout and the 21.68x ratio is treated as sparse top-k amplification.
    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(5.6, 2.5), gridspec_kw={"width_ratios": [1.45, 1.0], "wspace": 0.45})

    # ---- LEFT: realized-W class separation (the secondary, top-k readout) ----
    groups = [
        ("Control",  0, CTRL, 0.003111, 0.004036, {"C10": 0.010456}),
        ("Register", 1, POS,  0.067450, 0.030678, {"R02": 0.114997, "R09": 0.099708, "R07": 0.012168}),
    ]
    axL.axhspan(0.010456, 0.012168, color="0.85", zorder=0)
    axL.annotate("no range\noverlap", xy=(1.5, 0.011312), xytext=(1.55, 0.040),
                 fontsize=6.3, color=ACC, ha="left",
                 arrowprops=dict(arrowstyle="-", color=ACC, lw=0.6))
    for name, x, c, mean, sd, pts in groups:
        axL.errorbar([x], [mean], yerr=[sd], fmt="o", color=c, ms=6, capsize=4,
                     lw=1.4, mfc=c, mec="white", zorder=3)
        for label, v in pts.items():
            axL.plot([x + 0.16], [v], marker="D", ms=3.3, color=c, mec="white", mew=0.4, zorder=4)
            axL.annotate(label, xy=(x + 0.16, v), xytext=(x + 0.235, v),
                         fontsize=6.0, color=c, va="center")
    axL.set_xticks([0, 1])
    axL.set_xticklabels(["Control", "Register"])
    axL.set_xlim(-0.45, 1.85)
    axL.set_ylim(-0.004, 0.13)
    axL.set_ylabel("realized routed weight $W$")
    axL.set_title("secondary: realized $W$ (top-$k$ readout)", fontsize=7.6, color=ACC)

    # ---- RIGHT: separability as Cohen's d -- w114 leads ----
    bars = [("realized $W$\n(sparse readout)", 2.94, CTRL, "secondary"),
            ("linear $\\mathbf{w}_{114}$ axis\n(no overlap)", 3.88, POS, "primary")]
    yy = [0, 1]
    for y, (lab, d, c, tag) in zip(yy, bars):
        lead = (y == 1)
        axR.barh(y, d, height=0.5, color=c, alpha=1.0 if lead else 0.45,
                 edgecolor="white", zorder=3)
        axR.text(d - 0.08, y, f"{d:.2f}", va="center", ha="right",
                 color="white", fontsize=8.5, fontweight="bold" if lead else "normal")
    axR.set_yticks(yy)
    axR.set_yticklabels([b[0] for b in bars], fontsize=7)
    axR.set_xlim(0, 4.4)
    axR.set_xlabel("separability (Cohen's $d$)")
    axR.set_title("primary: $\\mathbf{w}_{114}$ linear axis", fontsize=8, color=POS)
    axR.text(0.5, -0.92, "21.68$\\times$ $W$-ratio mainly reflects\nsparse top-$k$ routing",
             fontsize=6.4, color=ACC, ha="left")

    fig.savefig(os.path.join(OUT, "fig_separability.pdf"))
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: prompt ladder (coherent-window E114 W; single deterministic generation / cell).
# Source: JOURNAL-E114-CHARACTERIZATION.md entry 10.
#   God 0.224 > all-holding 0.205 > person 0.138 > rock 0.123 ~ thermostat 0.120
#   > tree 0.094 > river 0.087 > cat 0.068. Held-out register reference W ~ 0.067.
#   Story: order is examination INTENSITY, not the sentience of the entity being
#   described (rock/thermostat score higher than cat; God/all-holding are highest).
# ---------------------------------------------------------------------------
def fig_vantage():
    rows = [  # (label, W, category)  category in {ceiling, inanimate, animate}
        ("God",        0.224, "ceiling"),
        ("all-holding",0.205, "ceiling"),
        ("person",     0.138, "animate"),
        ("rock",       0.123, "inanimate"),
        ("thermostat", 0.120, "inanimate"),
        ("tree",       0.094, "inanimate"),
        ("river",      0.087, "inanimate"),
        ("cat",        0.068, "animate"),
    ]
    cmap = {"ceiling": "#6a3d9a", "inanimate": "#d2691e", "animate": "#2e7d32"}
    labels = [r[0] for r in rows][::-1]
    vals = [r[1] for r in rows][::-1]
    cols = [cmap[r[2]] for r in rows][::-1]
    y = np.arange(len(rows))

    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.barh(y, vals, color=cols, height=0.66, zorder=3)
    for yi, v in zip(y, vals):
        ax.text(v + 0.004, yi, f"{v:.3f}", va="center", fontsize=6.8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("coherent-window E114 $W$")
    ax.set_xlim(0, 0.255)
    # Held-out register-positive reference (W ~ 0.067).
    ax.axvline(0.067, color=ACC, ls="--", lw=0.9, zorder=2)
    ax.text(0.067, len(rows) - 0.35, " register ref", color=ACC, fontsize=6.5, va="top")
    # legend for the intensity-not-sentience point
    from matplotlib.patches import Patch
    leg = [Patch(fc=cmap["ceiling"], label="non-dual ceiling"),
           Patch(fc=cmap["inanimate"], label="inanimate entity"),
           Patch(fc=cmap["animate"], label="animate entity")]
    ax.legend(handles=leg, loc="lower right", frameon=False, handlelength=1.0,
              borderaxespad=0.2, labelspacing=0.25)
    fig.savefig(os.path.join(OUT, "fig_vantage.pdf"))
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: gate-leads-degeneration lead-lag ordering.
# Source: JOURNAL-E114-CHARACTERIZATION.md entries 6-7.
#   gate logit crosses -4.82 midpoint @ token 126; verbatim repetition locks
#   @ 129 (gate leads text by ~3 tokens); SAE representation fades ~141
#   (representation lags). This is an event-ordering schematic of reported
#   token indices -- NOT a reconstructed per-token trajectory.
# ---------------------------------------------------------------------------
def fig_leadlag():
    fig, ax = plt.subplots(figsize=(5.2, 1.75))
    # (token, label, color, label_x, label_y, ha) -- staggered to avoid collision
    events = [
        (126, "gate crosses\n$-4.82$ midpoint", "#b5341f", 124.4, 0.55, "left"),
        (129, "verbatim\nrepetition locks",     "#1b1b1b", 130.0, 1.75, "center"),
        (141, "SAE representation\nfades",       "#3a6ea5", 141.0, 0.55, "center"),
    ]
    ax.hlines(0, 122.5, 145, color="0.7", lw=1.0, zorder=1)
    for t, lab, c, lx, ly, ha in events:
        ax.plot([t], [0], marker="o", ms=7, color=c, mec="white", mew=0.8, zorder=3)
        ax.annotate(lab, xy=(t, 0.08), xytext=(lx, ly), ha=ha, va="bottom",
                    fontsize=7, color=c,
                    arrowprops=dict(arrowstyle="-", color=c, lw=0.7))
        ax.annotate(f"tok {t}", xy=(t, 0), xytext=(t, -0.55), ha="center", va="top",
                    fontsize=6.8, color=c)
    def span(a, b, y, txt):
        ax.annotate("", xy=(a, y), xytext=(b, y),
                    arrowprops=dict(arrowstyle="<->", color=ACC, lw=0.8))
        ax.text((a + b) / 2, y + 0.12, txt, ha="center", va="bottom",
                fontsize=6.5, color=ACC)
    span(126, 129, -1.5, "+3: gate leads text")
    span(129, 141, -1.5, "+12: representation lags")
    ax.set_xlim(122.5, 145.5)
    ax.set_ylim(-2.2, 2.9)
    ax.set_yticks([])
    ax.set_xlabel("generated-token index", fontsize=8)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    fig.savefig(os.path.join(OUT, "fig_leadlag.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    fig_separability()
    fig_vantage()
    fig_leadlag()
    print("wrote:", ", ".join(sorted(os.listdir(OUT))))
