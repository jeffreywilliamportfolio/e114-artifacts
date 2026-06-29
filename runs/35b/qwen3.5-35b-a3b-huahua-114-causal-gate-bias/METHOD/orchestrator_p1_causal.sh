#!/usr/bin/env bash
# Phase 1 causal (runs ON the box, hauhau Q8). Greedy + --stop-at-eog + --routing-only (disk-safe).
# Arms: E114-alone (all-layers, original protocol) vs coalition(114,87,170,68) vs matched control expert.
# Confirms suppression->mechanical framing is SPECIFIC to E114/cluster, not generic perturbation.
set -uo pipefail
WORK=/workspace/probe3chunk
LOG="$WORK/orch_p1.log"
exec > >(tee -a "$LOG") 2>&1
echo "ORCH_P1_START $(date -u +%FT%TZ)"

CAP="$WORK/capture_activations"
HAU=/workspace/models/hauhau/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf
SET="$WORK/selfreport_set_no_think.tsv"
COMMON=(-n 2056 -ngl 999 -c 8192 -t 16 -fa on --cache-type-k q8_0 --cache-type-v q8_0 \
        --seed 42 --temp 0 --top-k 1 --top-p 1 --min-p 0 --repeat-penalty 1 --mirostat 0 \
        --no-stream --stop-at-eog --routing-only)

cap() { # label  bias_spec(empty=baseline)
  local lbl="$1"; local bias="$2"
  local out="$WORK/cap_p1_${lbl}"; mkdir -p "$out"
  local extra=(); [ -n "$bias" ] && extra=(--expert-bias "$bias")
  echo ">>> cap ${lbl} bias='${bias}' $(date -u +%T)"
  "$CAP" -m "$HAU" --prompt-file "$SET" -o "$out" "${extra[@]}" "${COMMON[@]}" \
    2>&1 | grep -iE "Expert bias|Failed to parse|Capture Complete|error|loading model" | head -4
  echo "  exit=${PIPESTATUS[0]} done ${lbl} $(date -u +%T)"
}

echo "== free GPU (no-op on full-cuda; harmless) =="
pkill -x llama-server 2>/dev/null; sleep 2

# 1) BASELINE first (router npy kept until extract)
cap baseline ""

# 2) pick matched control expert from baseline L14 router (closest activation to E114, non-cluster)
CTRL=$(python3 "$WORK/pick_control.py" "$WORK/cap_p1_baseline" 2>/dev/null)
[ -z "$CTRL" ] && CTRL=100   # fallback: mathematics specialist
echo "MATCHED_CONTROL_EXPERT=$CTRL"

# 3) E114-alone arm (all-layers default = original PM protocol)
for b in -2.0 -3.0 -5.0 -8.0 2.0 3.0; do cap "e114_${b}" "114:${b}"; done

# 4) coalition arm (114,87,170,68 all-layers; matches philosophy-experts-bias)
for b in -3.0 -8.0 3.0; do cap "coal_${b}" "114:${b},87:${b},170:${b},68:${b}"; done

# 5) matched-control arm (same protocol, different expert -> specificity test)
for b in -3.0 -8.0; do cap "ctrl${CTRL}_${b}" "${CTRL}:${b}"; done

# 6) extract routing signature (reads npy) -> JSON, then tar text, then delete raw npy
echo "== extract routing metrics =="
python3 "$WORK/p1_extract.py" "$WORK" "$CTRL" > "$WORK/p1_metrics.json" 2>"$WORK/p1_extract.err" || { echo "EXTRACT FAILED"; cat "$WORK/p1_extract.err"; }
echo "== tar generated text + metadata + metrics =="
cd "$WORK"
tar czf /tmp/p1_text.tgz cap_p1_*/*/generated_text.txt cap_p1_*/*/metadata.txt \
    p1_metrics.json p1_extract.err selfreport_set_no_think.tsv orch_p1.log 2>/dev/null
echo "tar: $(du -h /tmp/p1_text.tgz | cut -f1)"
echo "== delete raw npy (disk-safe) =="
find cap_p1_* -name '*.npy' -delete
echo "df: $(df -h /workspace | tail -1)"
echo "ORCH_P1_DONE $(date -u +%FT%TZ)"
