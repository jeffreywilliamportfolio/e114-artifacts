# Zenodo tensor dataset — figure-backing raw captures only

The raw `.npy` activation/router tensors are kept **out of git** and archived as a
separate Zenodo *dataset* record (own DOI), cross-linked from the paper record and
this repo's README.

Following Zenodo's data-availability practice, we deposit **only the captures that
back the paper's figures** (~1.2 GB), **not** the full ~18 GB working set. The
excluded bulk is non-figure material: Python virtualenvs, the SAE feature-map dump,
a UI app, a safety-smoke run, and library test fixtures.

## Provenance caveat (carry verbatim)
The *original* held-out separability capture (`20260417T202651Z_heldout`) raw
residual/logit tensors are **not** in the local tree — those Vast.ai instances were
destroyed, and `make_figs.py` plots **journal-reported summary statistics**, not raw
points. What is deposited are the **surviving raw captures that substantiate the same
statistics**: the BF16 greedy-reference trajectory, the reproduction run's per-cell
`W114_L14` gate projections, the vantage-ladder captures, the AI-hidden-state
follow-up rung capture, and the L14 router-logit + residual prefill captures from
which `w114` recovers by least squares.

## What gets deposited (figure -> capture)
| Figure | Capture | Source | Size |
|---|---|---|---|
| `fig_vantage` | vantage ladder | `sae-tests/runs/vantage_ladder_20260531T143454Z` | 311 MB |
| `fig_vantage` | AI-hidden-state follow-up rung | `e114-artifacts/tmp/vast_ai_vantage/results/ai_vantage_20260629T212734Z` | 7.4 MB |
| `fig_leadlag` | greedy reference (per-token gate trajectory) | `sae-tests/runs/greedy_reference_20260418T160353Z` | 191 MB |
| `fig_separability`, `fig_leadlag` | reproduction run (`W114_L14` gate projections) | `sae-tests/runs/run-staging-repro-20260531T191119Z` | 686 MB |
| `fig_separability` | w114 recovery inputs (L14 router logits + residuals) | `attractor-shift-qwen-35b/run-staging/results/{base_prefill,diac_sae,n08_entropy}` | ~44 MB |

Total ~1.2 GB — comfortably within Zenodo's 50 GB/record limit.

## Package it
Run `./package-tensors.sh`. It stages only the above, drops venvs / caches / test
fixtures, writes `SHA256SUMS.txt` and `MANIFEST.md`, and produces the versioned
data archives `release_data-e114-figure-tensors-v1.2.5.tar.gz` and
`release_data-e114-figure-tensors-v1.2.5.zip`.

## Cross-linking
1. Reserve the dataset DOI on Zenodo (can reserve before upload completes).
2. Put that DOI in this repo's `README.md` and the paper's *Data and Artifact
   Availability* section.
3. On the paper *publication* record, add the dataset DOI as a related identifier
   ("is supplemented by"); on the dataset record, link back ("is supplement to").
