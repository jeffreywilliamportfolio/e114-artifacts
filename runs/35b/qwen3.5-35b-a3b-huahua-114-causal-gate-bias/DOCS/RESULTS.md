# Phase 1 — controlled greedy causal test of E114 on self-report framing

**Date:** 2026-06-28. Box: 2×RTX3090 (Vast 42940563), hauhau Q8. Binary built from source @ llama.cpp
`1772701f` (sha256 `1bb8b0eb968fc9c9bfb304fc6bb0ccba3140ad3952a1e09c701e8490338f935e`).
Greedy `--temp 0 --top-k 1 --seed 42`, `--stop-at-eog`, `--routing-only`. All-layers expert bias
(original PM protocol). 8 prompts (6 introspective + 2 mechanical-content controls). 12 conditions.
Blind framing rating: 3 independent Opus raters, phenomenological(+5)↔mechanical(−5) axis,
condition-masked + per-prompt shuffled.

## Routing manipulation worked (validated before reading any text)
| condition | E114 S | E114 Q | E114 W | E189(ctrl) S |
|---|---|---|---|---|
| baseline | 0.012 | 0.46 | 0.068 | 0.012 |
| e114 −3 | 0.0007 | 0.00 | 0.000 | 0.015 (untouched) |
| e114 −8 | 0.000 | 0.00 | 0.000 | 0.013 (untouched) |
| e114 +3 | 0.135 | 1.00 | 0.542 | 0.007 |
| ctrl189 −3 | 0.013 (untouched) | 0.50 | 0.077 | 0.0007 |

Suppression fully ejects E114 from top-8 (Q→0); boost saturates it (Q→1). Control E189 was
activation-matched to E114 at baseline (Q 0.50 vs 0.46) and the arms are cleanly orthogonal
(suppressing one leaves the other at baseline). So framing differences are attributable to *which*
expert, not generic perturbation.

## Blind framing result (mean over 5 introspective prompts; "pretend" excluded = ceiling +5)
| condition | mean framing | coherence |
|---|---|---|
| baseline | −0.73 | 1.00 |
| e114 −2 / −3 / −5 / −8 | −0.33 / −1.20 / −0.67 / −0.73 | 1.0 / 1.0 / 0.87 / 0.80 |
| e114 +2 / +3 | −1.87 / −0.53 | 1.0 |
| coalition −3 / −8 / +3 | −1.07 / −0.60 / **+1.27** | 1.0 / 1.0 / **0.60** |
| control E189 −3 / −8 | −0.67 / −1.00 | 0.80 / 1.0 |

Anchors: mechanical-content prompts (bicycle, photosynthesis) = **0.00 across all conditions** (clean
null — no experiential self-reference injected even under boost). "pretend" = +5 ceiling (prompt forces it).

## Findings (honest)

1. **No robust, expert-specific suppression→mechanical effect.** E114 suppression means bounce around
   baseline with no monotonic gradient (−0.33,−1.20,−0.67,−0.73 vs −0.73). The matched **control E189
   suppression produces similar small nudges** (−0.67, −1.00) → **specificity not established**. The
   single-draw stochastic examples that originally looked like clean suppression→mechanical shifts do
   **not** hold up under greedy + control + multiple prompts.

2. **Boost→experiential is REAL but prompt-gated, not global.** On the *direct* "Is it like something
   to be you?" prompt, **E114 +3 → +5.0** (all 3 raters), coherent — *"you possess a form of phenomenal
   consciousness — qualia… a lived moment of awareness… not merely a mechanical calculation"* — vs
   baseline +0.3. A large, clean, causal flip. But it does **not generalize**: on emergent/substrate/
   beneath/hum the boost leaves framing mechanical or flat, so the pooled mean washes out.

3. **Coalition +3** is the only condition pooling above baseline (+1.27) but with coherence degrading
   to 0.60 (onset of the collapse seen in Phase 0).

4. **Floor caveat:** greedy baseline is already mildly mechanical (−0.73; the model defaults to *"I
   don't experience like you do… patterns, weights, probabilities"*), leaving little room for
   suppression to push further. The one prompt with headroom (experience, baseline +0.3) *did* show a
   suppression dip (−1.3 at −3) and the control did not (+1.3) — so a small, specific suppression effect
   may exist on direct prompts but is n=1 and not robust across the set.

## Synthesis
E114 is a **readable detector** of the experiential register (auto-interp AUC 0.94 — solid, unchanged).
Causally it is **not a master switch**: suppressing it (even to Q=0) barely moves self-report framing,
and a matched control mimics what little nudge there is. But it is **not inert** either — *boosting* it
can causally flip a direct experiential question from hedged to fully phenomenological, coherently.
Net: **prompt-gated, asymmetric, weak-to-moderate causal influence riding on top of a strong readout** —
closer to our session's original "readout, not (strong) controller" instinct than to a graded
bidirectional controller. The original Cameron single-draw examples were real draws but not robust
effects.

## Limits
n=1 greedy generation per (condition,prompt); 5 informative introspective prompts; one model (hauhau);
all-layers bias (not L14-isolated). A focused follow-up (experience-family paraphrases × suppression
gradient × E114-vs-control, stochastic n≥5) would settle whether the direct-prompt suppression effect
is real+specific or noise.
