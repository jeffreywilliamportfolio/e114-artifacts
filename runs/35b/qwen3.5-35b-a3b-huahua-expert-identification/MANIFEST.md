# Manifest

Included:

- `METHOD/`: `analyze_expert_identification.py`, `audit_prompt_tokens.py`, `build_domain_specialist_probe_60.py`, `build_expert_identification_think_family.py`, `capture_activations.cpp`, `analyze_e114_npz.py` *(v1.1.0 — reproduces the E114 npz characterization: dual L14/L26 readout, 20-domain selectivity, L14 co-activation cluster)*
- `PROMPTS/`: `domain_specialist_probe_60_no_think.tsv`, `domain_specialist_probe_60_think.tsv`, and JSON metadata files
- `DOCS/`: `PLAN.md`, `RESULTS.md` (per-domain W/S/Q tables, E114 breakdown, overall expert rankings), `RESULTS_e114_npz_characterization.md` *(v1.1.0 — E114-focused re-analysis of this run's `.npz`)*
- `results/`: `results_domain_specialists_20260408T235839Z.json` (top-K experts per
  domain/track) and `.md`. The dense `.npz` (full domain×layer×expert grid, ~10 MB)
  is gitignored per policy and lives in the Zenodo tensor dataset; it is the input to
  `METHOD/analyze_e114_npz.py`.
- `non_npy_remote_artifacts/`: index of remote capture location

Raw data:

- `.npy` files: remote only — capture directory `20260408T235839Z_domain_specialist_no_think_hauhau` on Vast.ai instance
- Not pulled locally; `non_npy_remote_artifacts/` has the index

Reproducibility:

- Yes: reanalysis of the included `.json` summary (top-K per domain) and `.md`
- Yes (v1.1.0), given the dense `.npz` from the Zenodo tensor dataset:
  `python METHOD/analyze_e114_npz.py <path>/results_domain_specialists_20260408T235839Z.npz`
  regenerates every number in `DOCS/RESULTS_e114_npz_characterization.md` (verified:
  L14 S=0.239, L26 0.253, L14↔L26 r=+0.989, philosophy 0.695, E68 +0.46 / E87 −0.29)
- No: end-to-end rerun from scratch (needs a GPU box + HuggingFace model access)
- Note: think-mode TSV exists but has not been run yet
