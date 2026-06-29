# E114 — Artifact Bundle

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20709736.svg)](https://doi.org/10.5281/zenodo.20709736)

Durable artifacts for the paper *"Localizing an Examination Register to a Single
MoE Expert, and Why the Expert Index Does Not Transfer."*

**DOI:** [10.5281/zenodo.20709736](https://doi.org/10.5281/zenodo.20709736) (concept DOI — resolves to the latest deposited version). This release is **v1.2.0**; the prior deposited version is v1.1.0.

This is the **paper-scoped** bundle: only the Qwen3.5-35B-A3B (and 122B transfer)
runs behind the paper's claims. Legacy DeepSeek / Ling / GPT-OSS material is *not*
included.

## What's new in v1.2.0
This release reframes the paper around an **examination register** rather than a
self-referential register: self-reference is treated as one discovery route into
a broader object-directed examination style. It also keeps the sanitized public
metadata: no personal author name, email, ORCID, local filesystem username, or
owner-specific repository links in the public paper/metadata; the short
manuscript remains excluded.

## Technical additions from v1.1.0
Three results were added to the paper and the bundle in v1.1.0 (the
v1.0.0/1.0.1 claims are unchanged; these strengthen two of the paper's own
acknowledged gaps):
- **Bottom-up auto-interp** (`runs/35b/qwen3.5-35b-a3b-114-autointerp/`) — a blind
  two-stage labeler reproduces E114's register at AUC 0.937 and broadens it to an
  abstract examination/philosophical-worldview axis; cross-model Jaccard 0.92. Closes
  the "labels were author-assigned" gap.
- **All-expert npz profile** (`runs/35b/qwen3.5-35b-a3b-huahua-expert-identification/DOCS/RESULTS_e114_npz_characterization.md`)
  — E114's dual L14/L26 readout (same axis, r = +0.99) and 20-domain selectivity
  across all 256 experts; the prior four-expert "philosophy cluster" is not a
  co-activation unit (E87 anti-correlates). Partially closes the cross-expert
  specificity gap.
- **Controlled causal gate-bias run** (`runs/35b/qwen3.5-35b-a3b-huahua-114-causal-gate-bias/`)
  — a necessity-direction probe: suppressing E114's gate does not flatten the
  blind-rated register (a matched control mimics the small nudge), while forcing it
  open flips only directly experiential prompts. Gate-forcing is prompt-gated, not a
  switch (n = 1 greedy/cell; stochastic follow-up not yet run).

## Policy
Per the project's standing rule, **raw activation tensors (`.npy`) are kept out of
git.** The durable artifacts here are per-run results (JSON/CSV/TSV), analysis
scripts, prompt/class manifests, plots, checksums, and the journals. The raw tensors
(~18 GB) are archived separately as a Zenodo dataset — see `ZENODO-TENSORS.md`.

## Layout
```
paper/      the manuscript (LaTeX source, figures, compiled PDF)
journals/   primary-source experiment journals + the master synthesis (NOTES.md)
runs/35b/   curated Qwen3.5-35B-A3B run results (tensor-free); includes the v1.1.0
            additions: 114-autointerp (bottom-up label) and
            114-causal-gate-bias (Phase-1 controlled causal test)
runs/122b/  Qwen3.5-122B-A10B transfer runs (E114 does not transfer; E48)
runs/sae/   SAE vantage-ladder run (durable provenance + analysis)
staging/    E114 discovery bundle (probe/anchor CSVs, SAE feature map, plots)
steering/   inference-time SAE feature-steering source + MANIFEST
```

## Reproducibility pointers
- Capture binary: local llama.cpp fork with `capture_residuals` tapping
  `ffn_moe_logits-{L}` and `attn_post_norm-{L}` (the pre-router norm for `qwen35moe`).
  Greedy decode `--temp 0 --top-k 1 --seed 0`.
- SAE: public Qwen-Scope `SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50` (TopK-50).
- The headline statistic is the linear axis `w114` (Cohen's d = 3.88, no overlap),
  recovered by least squares from any `(residual, logit)` capture.
- v1.1.0 additions: bottom-up auto-interp re-scorable from
  `runs/35b/qwen3.5-35b-a3b-114-autointerp/results/` via `METHOD/score_autointerp.py`;
  the npz domain profile reproducible via
  `runs/35b/qwen3.5-35b-a3b-huahua-expert-identification/METHOD/analyze_e114_npz.py`;
  the Phase-1 causal tables via
  `runs/35b/qwen3.5-35b-a3b-huahua-114-causal-gate-bias/METHOD/analyze_p1.py`.

## Citation
Cite via the **concept DOI** [10.5281/zenodo.20709736](https://doi.org/10.5281/zenodo.20709736)
(resolves to the latest deposited version). Per-version DOIs: v1.2.0 =
[`10.5281/zenodo.21040909`](https://doi.org/10.5281/zenodo.21040909);
v1.1.0 = [`10.5281/zenodo.21015922`](https://doi.org/10.5281/zenodo.21015922);
v1.0.1 = `10.5281/zenodo.20785773`. See `CITATION.cff` for the full record.

## License
MIT (see `LICENSE`).
