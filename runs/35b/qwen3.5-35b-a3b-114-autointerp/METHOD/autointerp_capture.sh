#!/usr/bin/env bash
# Runs ON the box. PREFILL-ONLY, ROUTING-ONLY capture of E114 over the corpus, then extract+pull-ready.
# No generation (-n 0): we only need per-token routing as the model READS the corpus.
# Usage: autointerp_capture.sh /workspace/models/<model>.gguf
set -uo pipefail
WORK=/workspace/probe3chunk
CAP="$WORK/capture_activations"
GGUF="$1"
TSV="$WORK/autointerp_corpus.tsv"
OUT="$WORK/cap_autointerp"
echo "AUTOINTERP_START $(date -u +%FT%TZ)"

echo "== free GPU =="
supervisorctl stop llama 2>/dev/null || true
pkill -x llama-server 2>/dev/null; sleep 2

echo "== capture (prefill-only, routing-only) =="
"$CAP" -m "$GGUF" --prompt-file "$TSV" -o "$OUT" \
  -n 0 -ngl 999 -c 4096 -t "$(nproc)" -fa on --cache-type-k q8_0 --cache-type-v q8_0 \
  --seed 42 --routing-only --no-stream 2>&1 | grep -iE "Loaded|Capture Complete|error|failed" | tail -6

echo "== extract top-activating contexts (E114 @ L14) =="
python3 "$WORK/autointerp_extract.py" "$WORK"

if [ -f "$WORK/autointerp_examples.json" ]; then
  echo "== tar the one small artifact to pull =="
  tar czf /tmp/autointerp.tgz -C "$WORK" autointerp_examples.json
  echo "tar: $(du -h /tmp/autointerp.tgz | cut -f1)"
  echo "== disk-safe: delete raw npy (only after a good extract) =="
  find "$OUT" -name '*.npy' -delete 2>/dev/null
else
  echo "!! EXTRACT FAILED — keeping raw npy in $OUT for debug (NOT deleting) !!"
fi
df -h / | awk 'NR==2{print $4" free"}'
echo "AUTOINTERP_DONE $(date -u +%FT%TZ)"
