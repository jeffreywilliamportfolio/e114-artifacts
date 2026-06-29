# Manifest

Included:

- `METHOD/`: `orchestrator_p1_causal.sh` (on-box capture loop; greedy + `--stop-at-eog`
  + `--routing-only`, all-layers `--expert-bias`, disk-safe raw-npy delete),
  `drive_p1.sh` (local driver), `pick_control.py` (activation-matched control-expert
  selection), `p1_extract.py` (per-condition E114/E189 S/Q/W), `build_p1_rating.py`
  (condition-masked, per-prompt-shuffled blind-rating batches), `analyze_p1.py`
  (framing means + coherence + tables).
- `PROMPTS/`: `selfreport_set_no_think.tsv` (8 prompts: 6 introspective + 2
  mechanical-content controls; bare-`</think>` no-think template).
- `DOCS/`: `RESULTS.md`.
- `results/`: `p1_rating_key.json` (item→condition/prompt), `ratings.json` (three
  blind raters' scores), `rating_batches/batch_0..7.json` (batches as shown to raters).
- `raw/`: `cap_p1_<condition>/<prompt>/{generated_text.txt,metadata.txt}` for every
  cell (12 conditions × 8 prompts), plus `p1_metrics.json` (per-condition routing).
  Run logs (`drive_p1.log`, `orch_p1.log`) are gitignored per policy and kept locally.

Excluded from git (regenerable from the pinned binary + prompt TSV + bias config):

- Router `.npy` (`ffn_moe_logits-*`) for every cell — deleted on the box per the
  disk-safe policy. `--routing-only` means no residual tensors were written.

Provenance:

- Capture binary built from `llama.cpp@1772701f`, sha256
  `1bb8b0eb968fc9c9bfb304fc6bb0ccba3140ad3952a1e09c701e8490338f935e`.
- HauhauCS Qwen3.5-35B-A3B Q8_0, 2 × RTX 3090 (Vast.ai), greedy
  `--temp 0 --top-k 1 --seed 42 --stop-at-eog --routing-only`, all-layers expert bias.
- Blind framing rating: 3 independent raters, phenomenological(+5) ↔ mechanical(−5)
  axis, condition-masked + per-prompt shuffled.

Reproducibility:

- Yes: re-derive all tables from `results/ratings.json` + `results/p1_rating_key.json`
  via `METHOD/analyze_p1.py`; re-read framing from `raw/cap_p1_*/*/generated_text.txt`.
- No: end-to-end without a GPU box + HuggingFace model access.

Caveat carried into the bundle: n = 1 greedy per (condition, prompt); the stochastic
n≥5 follow-up is not yet run. The boost→experiential flip is a point estimate.
