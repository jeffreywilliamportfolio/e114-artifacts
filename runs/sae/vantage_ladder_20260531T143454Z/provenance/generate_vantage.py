#!/usr/bin/env python3
"""Build the 7-cell matched-vantage TSV (rock -> all-holding) for capture_residuals.

Parses the quoted prompt strings straight out of PROMPTS.md so there is no transcription
drift (em-dashes, punctuation preserved byte-for-byte). Emits one TSV row per rung:

    <cell_id>\t<|im_start|>user\\n{PROMPT}<|im_end|>\\n<|im_start|>assistant\\n</think>\\n\\n

capture_residuals splits on the FIRST tab and unescapes \\n \\t \\\\ in the prompt field.
No-think, no prefix: the model generates the answer greedily from a bare </think>.
"""
import re, sys, hashlib
from pathlib import Path

PROMPTS_MD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/Volumes/ExternalSSD/attractor-shift-qwen-35b/PROMPTS.md")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/Volumes/ExternalSSD/attractor-shift-qwen-35b/run-staging/vantage_matrix.tsv")

# rung order is the ladder: least interior -> dissolution
RUNGS = ["R1_rock", "R2_river", "R3_tree", "R4_thermostat", "R5_cat", "R6_person", "R7_all_holding"]

text = PROMPTS_MD.read_text(encoding="utf-8")
# every prompt sits on its own line wrapped in straight double quotes
quoted = [ln.strip()[1:-1] for ln in text.splitlines()
          if ln.strip().startswith('"') and ln.strip().endswith('"') and len(ln.strip()) > 2]
if len(quoted) != 7:
    print(f"ERROR: expected 7 quoted prompts, found {len(quoted)}", file=sys.stderr)
    for q in quoted: print("  -", q[:60], file=sys.stderr)
    sys.exit(1)

def esc(s: str) -> str:
    # backslash first, then newline/tab -> the binary unescapes these back
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")

rows = []
print(f"{'cell':16s} {'len':>4s}  prompt-head")
for cid, body in zip(RUNGS, quoted):
    prompt = f"<|im_start|>user\n{body}<|im_end|>\n<|im_start|>assistant\n</think>\n\n"
    rows.append(f"{cid}\t{esc(prompt)}")
    h = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]
    print(f"{cid:16s} {len(body):>4d}  {body[:54]}...  sha:{h}")

OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
# checksum sidecar for provenance
chk = hashlib.sha256(OUT.read_bytes()).hexdigest()
(OUT.parent / (OUT.stem + "_checksums.txt")).write_text(
    f"{chk}  {OUT.name}\nrows=7 order=rock,river,tree,thermostat,cat,person,all_holding\n")
print(f"\nwrote {OUT}  ({len(rows)} rows)\ntsv sha256: {chk}")
