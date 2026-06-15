#!/usr/bin/env bash
# Stage ONLY the figure-backing raw captures (~1.2 GB) for the Zenodo dataset record.
# Excludes the ~18 GB of non-figure material (venvs, SAE featmap dump, UI app,
# safety-smoke run, library test fixtures). Writes checksums + manifest + tarball.
# Nothing here touches a remote.
set -euo pipefail

STAGE="/Volumes/ExternalSSD/e114-tensors-zenodo"
SAE="/Volumes/ExternalSSD/sae-tests/runs"
ATT="/Volumes/ExternalSSD/attractor-shift-qwen-35b/run-staging/results"
TARBALL="/Volumes/ExternalSSD/e114-figure-tensors.tar.gz"

# rsync: copy captures, drop envs / caches / fixtures / vcs
RS=(rsync -a --prune-empty-dirs
    --exclude='.venv*/' --exclude='venv/' --exclude='site-packages/'
    --exclude='__pycache__/' --exclude='*.pyc' --exclude='.git/'
    --exclude='.DS_Store' --exclude='dog/' --exclude='lib/python*/')

rm -rf "$STAGE"; mkdir -p "$STAGE"

echo ">> fig_vantage  : vantage ladder"
"${RS[@]}" "$SAE/vantage_ladder_20260531T143454Z/" "$STAGE/fig_vantage__vantage_ladder/"

echo ">> fig_leadlag  : greedy reference (per-token gate trajectory)"
"${RS[@]}" "$SAE/greedy_reference_20260418T160353Z/" "$STAGE/fig_leadlag__greedy_reference/"

echo ">> fig_separability + fig_leadlag : reproduction run (W114_L14 gate projections)"
"${RS[@]}" "$SAE/run-staging-repro-20260531T191119Z/" "$STAGE/fig_separability_leadlag__repro/"

echo ">> fig_separability : w114 recovery inputs (L14 router logits + residuals)"
for s in base_prefill diac_sae n08_entropy; do
  "${RS[@]}" "$ATT/$s/" "$STAGE/fig_separability__w114_inputs/$s/"
done

# ---- checksums + manifest ----
echo ">> checksums"
( cd "$STAGE" && find . -name '*.npy' -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS.txt )
NPY=$(grep -c '' "$STAGE/SHA256SUMS.txt")

cat > "$STAGE/MANIFEST.md" <<EOF
# E114 figure-backing raw captures

Deposited alongside the paper "Expert 114: A Linear Router Axis for Inhabited
Self-Examination in a Mixture-of-Experts Language Model — and Why It Does Not
Transfer." These are the raw tensors behind the paper's three figures; see
SHA256SUMS.txt for file-level checksums. License: MIT.

Layout:
  fig_vantage__vantage_ladder/          -> Fig. vantage ladder (coherent-window E114 W)
  fig_leadlag__greedy_reference/        -> Fig. gate-leads-degeneration (per-token gate)
  fig_separability_leadlag__repro/      -> Fig. separability + lead-lag (W114_L14 gate)
  fig_separability__w114_inputs/        -> L14 router logits + residuals (w114 recovers
                                           by least squares: d=3.88, no overlap)

Provenance caveat: the original heldout capture 20260417T202651Z is not retained
(Vast.ai instances destroyed); figures were plotted from journal summary statistics.
The captures here are the surviving raw tensors that substantiate the same numbers.

Total .npy files: ${NPY}
EOF

echo ">> tarball"
tar -czf "$TARBALL" -C "$STAGE" .

echo
echo "Staged: $STAGE"
du -sh "$STAGE"
echo "Tarball: $TARBALL"
du -sh "$TARBALL"
echo "npy files: $NPY  (verify with: shasum -a 256 -c $STAGE/SHA256SUMS.txt)"
