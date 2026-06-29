# Manifest

Included:

- `METHOD/`: `autointerp_corpus.py`, `autointerp_capture.sh`, `autointerp_extract.py`,
  `prep_autointerp_score.py`, `score_autointerp.py`.
- `DOCS/`: `RESULTS.md`.
- `results/`: `detector_set.json` (80 shuffled windows; no labels/activations),
  `detector_key.json` (ground truth), `detector_scores.json` (blind detector output),
  `autointerp_examples_hauhau.json` (HauhauCS top/contrast windows),
  `explainer_input.txt` (top-40 windows shown to the blind explainer).

Excluded from git (regenerable from the pinned binary + corpus):

- Raw router `.npy` (`ffn_moe_logits-14` over 392 docs) — deleted on the capture box
  per the disk-safe policy.
- `autointerp_examples.json` for the base model was overwritten on pull; the base
  data is preserved in `detector_set.json` + `detector_key.json` and in
  `DOCS/RESULTS.md`.

Provenance:

- Capture binary `llama-capture-activations` built from `llama.cpp@1772701f` (build
  8493), `-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=86`, CUDA 12.8.93, g++ 13.3,
  2 × RTX 3090.
- Corpus `NeelNanda/pile-10k`, 392 docs ≤1200 chars, raw text (no ChatML),
  prefill-only, routing-only, `ffn_moe_logits-14`, 93,286 tokens (BOS skipped).
- Models: `Qwen/Qwen3.5-35B-A3B-Base` (primary) and
  `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive` (cross-model), both Q8_0.

Reproducibility:

- Yes: re-score from `detector_set.json` + `detector_key.json` via
  `METHOD/score_autointerp.py`.
- No: end-to-end without a GPU box + HuggingFace model access.
