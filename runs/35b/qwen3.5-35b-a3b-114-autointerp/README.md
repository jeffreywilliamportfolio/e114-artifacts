# Qwen3.5-35B-A3B — Expert 114 bottom-up auto-interpretation

Unsupervised, prompt-independent characterization of what Expert 114 at layer 14
reads, with a blind two-stage evaluation. This is the bottom-up complement to the
hand-prompted held-out separability result (`../heldout-clean/`): instead of asking
whether E114 fires on chosen self-reference prompts, it asks what E114 fires on in
ordinary natural text, and validates the answer blind.

## Scope

Capture E114@L14 routing over a generic corpus, rank the top-activating contexts,
and run a two-stage blind eval where one agent writes an explanation from the top
windows only and a second, fresh agent uses that explanation to score a shuffled
mix of top and random windows. The headline is the detector's separation of true
activators from contrast.

Run: `NeelNanda/pile-10k`, 392 docs (≤1200 chars), raw text, no ChatML | prefill-only
(`-n 0`), `--routing-only`, `ffn_moe_logits-14` | 93,286 tokens (BOS skipped) | base
`Qwen3.5-35B-A3B` Q8_0, with the identical capture re-run on
`HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive` Q8_0 | 2 × RTX 3090
(Vast.ai), `llama.cpp@1772701f` (build 8493), CUDA 12.8.93.

**Headline result.** A blind detector, given only the auto-generated explanation,
separates the 40 top-activating windows from 40 random-contrast windows at **ROC AUC
0.937**, **precision@40 0.90** (36/40), mean detector score 0.463 (top) vs 0.056
(random), Spearman(detector score, true activation) 0.734.

**What E114 reads.** An abstract reflective / philosophical / existential
"worldview" register — humanities discourse about meaning, belief, and values
(philosophy and theory; religion, spirituality and mythology; moral / political /
ideological and existential argument). First-person introspection is one subset of
this register, not the whole axis. This refines the earlier "introspective register"
label into a broader, prompt-independent one.

**Cross-model.** The uncensored fine-tune leaves what E114 reads intact: activation
distribution near-identical (base mean/p50/p99/max 0.0036/0.0031/0.0110/0.0940;
HauhauCS 0.0036/0.0032/0.0109/0.0966), top-40 document overlap Jaccard 0.920, and a
blind explainer on the HauhauCS top windows returns the same label.

## Folder Contents

- [`METHOD/`](METHOD/): `autointerp_corpus.py` (build the pile-10k window corpus),
  `autointerp_capture.sh` (prefill + routing-only capture; disk-safe raw-npy delete
  gated on a good extract), `autointerp_extract.py` (per-token `softmax(logits)[114]`;
  surrogateescape JSON read because BPE pieces split multibyte UTF-8),
  `prep_autointerp_score.py` (assemble the shuffled 80-window detector set),
  `score_autointerp.py` (AUC / precision@40 / Spearman against ground truth).
- [`DOCS/`](DOCS/): [`RESULTS.md`](DOCS/RESULTS.md) — method, explanation, scoring,
  representative activators, cross-model section, provenance.
- [`results/`](results/): `detector_set.json` (the 80 shuffled windows shown to the
  blind detector, no labels/activations), `detector_key.json` (ground-truth labels),
  `detector_scores.json` (detector output), `autointerp_examples_hauhau.json`
  (HauhauCS top/contrast windows), `explainer_input.txt` (the top-40 windows shown to
  the blind explainer).

## Reproducibility

- Yes: re-score from the included `detector_set.json` + `detector_key.json` via
  `METHOD/score_autointerp.py`.
- No: end-to-end rerun without a GPU box and HuggingFace access to the base and
  HauhauCS models. Raw router `.npy` were deleted on the box (disk-safe); the routing
  is regenerable from the pinned binary + corpus.

## Relationship to other experiments

- Validates, bottom-up, the register that the matched-token held-out test
  (`../heldout-clean/`) found top-down at Cohen's d = 3.88.
- The 20-domain dense-routing confirmation of this same selectivity is in
  `../qwen3.5-35b-a3b-huahua-expert-identification/DOCS/RESULTS_e114_npz_characterization.md`.
- A literal activation→language decode (Patchscopes / Qwen-Scope L14 SAE) needs the
  bf16 residual stream and is not done here; see `DOCS/RESULTS.md` §Not done.
