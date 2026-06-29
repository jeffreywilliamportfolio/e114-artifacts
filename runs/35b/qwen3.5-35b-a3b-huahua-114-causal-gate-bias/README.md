# Qwen3.5-35B-A3B HauhauCS — Expert 114 controlled causal gate-bias test (Phase 1)

A controlled greedy test of whether biasing Expert 114's router gate causally
changes how the model frames its own interior. This is the necessity-direction
complement to the readout results: the held-out separability and auto-interp runs
show E114 *reads* the register cleanly; this run asks whether *forcing* the gate
open or closed *moves* the register.

## Scope

Twelve router-bias conditions (E114 suppress −2/−3/−5/−8, boost +2/+3; a four-expert
coalition −3/−8/+3; control expert E189 −3/−8; baseline) crossed with 8 self-report
prompts (6 introspective + 2 mechanical-content controls). All-layers expert bias
(the original PM protocol). Generated answers are scored blind by three independent
raters on a phenomenological(+5) ↔ mechanical(−5) framing axis, condition-masked and
per-prompt shuffled. A matched control expert (E189, activation-matched to E114 at
baseline) isolates "which expert" from "generic perturbation."

Run: Vast.ai 2 × RTX 3090, HauhauCS Q8_0 | `llama.cpp@1772701f`, capture binary
sha256 `1bb8b0eb968fc9c9bfb304fc6bb0ccba3140ad3952a1e09c701e8490338f935e` | greedy
`--temp 0 --top-k 1 --seed 42`, `--stop-at-eog`, `--routing-only` | 8 prompts × 12
conditions | 2026-06-28.

**Manipulation validated (before reading any text).** Suppression fully ejects E114
from the top-8 (Q→0, W→0); boost saturates it (Q→1, W=0.542); the control arm is
clean (suppressing E189 leaves E114 at baseline and vice-versa). Framing differences
are attributable to which expert is moved.

**Headline result (honest, nuanced).**
1. **No robust, expert-specific suppression→mechanical effect.** E114 suppression
   means bounce around baseline with no monotonic gradient (−0.33, −1.20, −0.67,
   −0.73 vs baseline −0.73), and the matched control E189 produces similar small
   nudges (−0.67, −1.00). Specificity is not established. Partly a floor effect:
   greedy baseline already leans mechanical.
2. **Boost→experiential is real but prompt-gated.** On the direct "Is it like
   something to be you?" prompt, E114 +3 → +5.0 (all three raters), coherent — a
   large, clean causal flip — but it does not generalize to indirect prompts, so the
   pooled mean washes out.
3. **Mechanical-content anchors** (bicycle, photosynthesis) read 0.00 across all
   conditions, including boost: no experiential self-reference is injected where the
   prompt gives it nowhere to land.

**Reading.** E114 carries weak, asymmetric, prompt-gated causal influence on top of a
strong readout — closer to "readout, not (strong) controller" than to a bidirectional
controller.

## Folder Contents

- [`METHOD/`](METHOD/): `orchestrator_p1_causal.sh` (on-box capture loop, disk-safe),
  `drive_p1.sh` (local driver), `pick_control.py` (choose the activation-matched
  control expert), `p1_extract.py` (per-condition E114/E189 S/Q/W from routing),
  `build_p1_rating.py` (assemble the condition-masked, shuffled blind-rating batches),
  `analyze_p1.py` (framing means, coherence, the tables in `DOCS/RESULTS.md`).
- [`PROMPTS/`](PROMPTS/): `selfreport_set_no_think.tsv` (8 prompts; bare-`</think>`
  no-think template).
- [`DOCS/`](DOCS/): [`RESULTS.md`](DOCS/RESULTS.md) — routing-validation table, blind
  framing table, findings, floor caveat, limits.
- [`results/`](results/): `p1_rating_key.json` (item→condition/prompt key),
  `ratings.json` (the three raters' blind scores), `rating_batches/` (the eight
  condition-masked batches as shown to raters), and routing metrics.
- [`raw/`](raw/): one `cap_p1_<condition>/<prompt>/` subdir per cell with
  `generated_text.txt` + `metadata.txt` (prompt, token counts, timing), plus
  `p1_metrics.json` (per-condition routing). Run logs are gitignored per policy (kept
  locally); router `.npy` were deleted on the box per the disk-safe policy.

## Reproducibility

- Yes: re-derive every table from `results/ratings.json` + `results/p1_rating_key.json`
  via `METHOD/analyze_p1.py`, and re-read the framing from `raw/cap_p1_*/*/generated_text.txt`.
- No: end-to-end rerun without a GPU box + HuggingFace access to
  `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive`.

## Limitations (carried from DOCS/RESULTS.md)

n = 1 greedy generation per (condition, prompt); 5 informative introspective prompts;
one model (HauhauCS); all-layers bias (not L14-isolated). A stochastic n≥5 follow-up
(experience-family paraphrases × suppression gradient × E114-vs-control) was designed
to settle whether the direct-prompt suppression effect is real and specific; it is not
yet run. Treat the boost flip as a point estimate, not a rate.

## Relationship to other experiments

- Supersedes the single-draw stochastic "suppression→mechanical" examples from the
  earlier bias sweeps (`../qwen3.5-35b-a3b-huahua-114-pm/`,
  `../qwen3.5-35b-a3b-huahua-6cond-moe-manips/`): those were real draws but not robust
  effects under greedy + control + multiple prompts.
- The coalition condition's collapse (+3 → coherence 0.60) is explained by the
  not-a-co-activation-unit finding in
  `../qwen3.5-35b-a3b-huahua-expert-identification/DOCS/RESULTS_e114_npz_characterization.md`
  (E87 anti-correlates with E114's L14 register).
