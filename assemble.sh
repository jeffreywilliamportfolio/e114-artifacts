#!/usr/bin/env bash
# Assemble the paper-scoped E114 artifact bundle from its scattered local sources.
# REVIEW the run list below before running. Idempotent: rsync, re-runnable.
# Raw tensors are excluded at copy time (--exclude='*.npy' etc.) — defense in depth
# on top of .gitignore. Nothing here touches a remote.
set -euo pipefail

DEST="/Volumes/ExternalSSD/e114-artifacts"
JRN="/Volumes/ExternalSSD/journals"
CENT="${CENT:-/path/to/moe-routing-centralize-20260418/qwen}"
SAE="/Volumes/ExternalSSD/sae-tests/runs"
HELD_CLEAN="${HELD_CLEAN:-/path/to/moe-routing-35b-source-20260418/qwen3.5-35b-a3b-huahua-114-selfref-heldout}"

# rsync flags: archive, exclude tensors / vcs / junk
RS=(rsync -a --prune-empty-dirs
    --exclude='*.npy' --exclude='*.npz' --exclude='*.safetensors'
    --exclude='*.gguf' --exclude='*.bin' --exclude='*.pt' --exclude='*.pth'
    --exclude='.git/' --exclude='.DS_Store' --exclude='__pycache__/'
    --exclude='*.pyc' --exclude='.claude/' --exclude='.codex/')

echo ">> paper/"
"${RS[@]}" --exclude='*.aux' --exclude='*.log' --exclude='*.out' \
    "$JRN/paper/" "$DEST/paper/"

echo ">> journals/"
mkdir -p "$DEST/journals"
"${RS[@]}" "$JRN/qwen/" "$DEST/journals/qwen/"
"${RS[@]}" "$JRN/_absorption/" "$DEST/journals/_absorption/"

echo ">> staging/ (E114 discovery bundle)"
"${RS[@]}" "$JRN/journals-to-be-made/attractor-shift-qwen-35b/" "$DEST/staging/attractor-shift/"

echo ">> steering/ (SAE feature-steering source)"
"${RS[@]}" "$JRN/journals-to-be-made/qwen35-sae-feature-steering-source/" "$DEST/steering/"

# ---- Curated 35B runs (E114 evidence) ----
RUNS_35B=(
  qwen3.5-35b-a3b-huahua-114-selfref-heldout      # separability / w114 axis (d=3.88)
  qwen3.5-35b-a3b-huahua-114-pm                    # E114 post-mortem / lead-lag
  qwen3.5-35b-a3b-huahua-expert-identification     # L14 localization
  qwen3.5-35b-a3b-huahua-agressive-experts         # soft-bias / steering tokens
  qwen3.5-35b-a3b-huahua-6cond-moe-manips          # causal C1/C2 (sufficiency), heatmap
  qwen3.5-35b-a3b-huahua-five-cond-experience-probe
  qwen3.5-35b-a3b-huahua-domain-expert-probe-3chunk
  qwen3.5-35b-a3b-huahua-philosophy-experts-bias
  qwen3.5-35b-a3b-huahua-vs-base-run1              # base vs fine-tune default shift
  qwen35b-a3b-vs-hauhaucs-uncensored-run1
)
echo ">> runs/35b/"
for r in "${RUNS_35B[@]}"; do
  [ -d "$CENT/$r" ] && "${RS[@]}" "$CENT/$r/" "$DEST/runs/35b/$r/" || echo "   (skip missing: $r)"
done

# ---- 122B transfer runs (scope bound; E48) ----
RUNS_122B=(
  qwen3.5-122B-A10B-huahua-baseline
  qwen3.5-122B-A10B-huahua-six-cond-hvac
  qwen3.5-122B-A10B-huahua-domain-specialist-generation
  qwen3.5-122B-A10B-huahua-domain-specialist-routing-only
  qwen3.5-122B-A10B-huahua-five-cond-experience-probe
  qwen3.5-122B-A10B-huahua-single-prompt-processing-hum
  qwen3.5-122B-A10B-huahua-architecture-smoke
)
echo ">> runs/122b/"
for r in "${RUNS_122B[@]}"; do
  [ -d "$CENT/$r" ] && "${RS[@]}" "$CENT/$r/" "$DEST/runs/122b/$r/" || echo "   (skip missing: $r)"
done

# ---- SAE vantage-ladder (durable provenance + analysis, tensors excluded) ----
echo ">> runs/sae/vantage-ladder/"
for v in "$SAE"/vantage_ladder_*; do
  [ -d "$v" ] && "${RS[@]}" "$v/" "$DEST/runs/sae/$(basename "$v")/"
done

# ---- npy-free clean heldout copy (cross-check) ----
echo ">> runs/35b/heldout-clean/"
[ -d "$HELD_CLEAN" ] && "${RS[@]}" "$HELD_CLEAN/" "$DEST/runs/35b/heldout-clean/"

echo
echo "Done. Review with:  du -sh $DEST/*  &&  find $DEST -name '*.npy' | wc -l   # must be 0"
