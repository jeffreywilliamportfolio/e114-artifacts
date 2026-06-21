# E114 — Artifact Bundle

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20709736.svg)](https://doi.org/10.5281/zenodo.20709736)

Durable artifacts for the paper *"Expert 114: A Linear Router Axis for Inhabited
Self-Examination in a Mixture-of-Experts Language Model — and Why It Does Not
Transfer."*

**DOI:** [10.5281/zenodo.20709736](https://doi.org/10.5281/zenodo.20709736) (concept DOI — resolves to the latest version, currently v1.0.1)

This is the **paper-scoped** bundle: only the Qwen3.5-35B-A3B (and 122B transfer)
runs behind the paper's claims. Legacy DeepSeek / Ling / GPT-OSS material is *not*
included.

## Policy
Per the project's standing rule, **raw activation tensors (`.npy`) are kept out of
git.** The durable artifacts here are per-run results (JSON/CSV/TSV), analysis
scripts, prompt/class manifests, plots, checksums, and the journals. The raw tensors
(~18 GB) are archived separately as a Zenodo dataset — see `ZENODO-TENSORS.md`.

## Layout
```
paper/      the manuscript (LaTeX source, figures, compiled PDF)
journals/   primary-source experiment journals + the master synthesis (NOTES.md)
runs/35b/   curated Qwen3.5-35B-A3B run results (tensor-free)
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

## Citation
DOIs (paper record / tensor dataset record) to be filled in after Zenodo deposit.

## License
MIT (see `LICENSE`).
