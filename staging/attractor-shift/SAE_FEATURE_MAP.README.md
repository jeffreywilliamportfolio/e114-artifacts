# SAE_FEATURE_MAP.csv — running SAE-feature observation log (Qwen3.5-35B-A3B, L14)

A curated, human-readable index of every Qwen-Scope **L14** SAE feature we have *interpreted*
across the E114 / inward-register runs. Companion to the raw per-token / per-cell dumps; this
records what each feature **means** and how it relates to the **E114 inhabited-examination axis**.

Regenerate / append: `python3 run-staging/scripts/build_sae_feature_map.py`
(add rows to `ROWS` in that script and re-run; do not hand-edit the CSV — it is generated).

## SAE provenance
- **SAE family:** `Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50` — per-layer Qwen-Scope SAEs
  `layer{L}.sae.pt` for `L = 0..39`, width **32768**, TopK-50.
- **Read on:** `resid_post` of `Qwen/Qwen3.5-35B-A3B-Base` decoder block `L` = `hidden_states[L+1]`
  (NOT `attn_post_norm`; skip `hidden_states[0]` = embedding). The base SAE is native to this stream.
- **Logit-lens evidence:** `lm_head @ (W_dec[:,f] * norm_w)` → top promoted tokens.
- **Canonical God contemplative/non-dual cluster** (`deep_god_analysis.py`, all L14):
  `GCLUST = [4310, 4205, 11006, 4953, 14182, 18203, 14488, 13454]`.

**Primary key is `(feature_id, layer)`.** Every interpreted feature so far is **L14** (the E114
anchor), but per the 2026-06-01 full-stack-SAE methodology (CLAUDE.md) upcoming probes hook all 40
layers, so the same feature index at a different layer is a **different feature** — always pair the
index with its layer.

## Columns
| col | meaning |
|-----|---------|
| `feature_id` | SAE feature index (0–32767) |
| `layer` | always 14 (single-layer SAE so far) |
| `label` | short human name |
| `category` | `god-cluster` · `carrier-ref` · `filler` · `god-specific` · `duality` · `topical` · `referent` · `geom-neighbor` · `noise` · `todo` |
| `e114_relation` | `drives` · `co-fires` · `carrier` · `adjacent-unrecruited` · `dominant-filler` · `duality-low` · `topical` · `none` · `unknown` |
| `logit_lens_top_tokens` | top promoted tokens (pipe-separated evidence) |
| `observation` | what we concluded + key numbers |
| `source_run` | run the interpretation came from |
| `confidence` | `high` · `med` · `low` · `todo` |

## Reading guidance (carry the seams from CLAUDE.md)
- **`e114_relation` is the research variable.** `drives` = the linear/causal carrier (only 4310 so
  far). `co-fires` = token-locked but not shown causal. `adjacent-unrecruited` = decoder-cosine-near
  but the model does **not** light it (e.g. 26050 existential dread, 25427 Buddhist-neighbor) — these
  are the controls that keep "non-dual ≠ dread" honest.
- **`filler` / `dominant-filler` are cautions, not findings.** 2961 (punctuation) is the canonical
  "aggregate leaders can be filler" trap — high cross-cell mass, ~0 register-specificity.
- **`geom-neighbor` warns that decoder-cosine adjacency ≠ semantic relatedness** (32412 = Chinese ink
  painting sits cos +0.276 from the God feature yet is never recruited).
- **Model/regime scope:** these indices are **HauhauCS/Base 35B, L14** only. Do **not** transfer to
  122B (E48 regime) or assume any index means the same thing at another layer.
- **`todo` rows** = features that recur as high-selrate leaders in `carrier_summary.json` /
  base-prefill plateau but have not been logit-lensed yet. Map them next.

## Primary sources
- `/Volumes/ExternalSSD/sae-tests/runs/vantage_ladder_20260531T143454Z/analysis/`
  `{god_feature_map,logit_lens_dominant,deep_god_analysis}.txt`, `sae_carriers/carrier_summary.json`
- `run-staging/results/base_prefill/sae_resid/plateau_features.json`
- Narrative: `JOURNAL-E114-CHARACTERIZATION.md` (entries 10–11).
