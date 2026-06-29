# E114 auto-interp (Path A, expert-level) — base Qwen3.5-35B-A3B

**Question:** bottom-up, what does Expert 114 @ L14 fire on in *natural text* — independent of
the hand-picked prompts that gave the d=3.88 "introspective register" readout result?

**Verdict:** E114@L14 is a detector of an **abstract reflective / philosophical / existential
"worldview" register** — humanities discourse about meaning, belief, and values. First-person
introspection is one *subset*, not the whole axis. A blind detector given only the auto-generated
explanation separates activators from contrast at **AUC 0.937 / precision@40 0.90**, so the
characterization is trustworthy. This is independent, unsupervised confirmation that E114 reads a
coherent register axis (not an artifact of our chosen prompts).

## Method
- **Model:** base `unsloth/Qwen3.5-35B-A3B-GGUF` → `Qwen3.5-35B-A3B-Q8_0.gguf` (36.9 GB; Q8 to
  match all prior E114 captures).
- **Corpus:** `NeelNanda/pile-10k` (the standard mechinterp corpus), 392 diverse docs, ≤1200 chars,
  **raw text, no ChatML** (characterize what E114 reads, not generation).
- **Capture:** prefill-only (`-n 0`), `--routing-only`, 2×RTX 3090, Q8, `ffn_moe_logits-14` only
  used. Per-token activation = `softmax(ffn_moe_logits-14)[114]`. 93,286 tokens (BOS skipped).
- **Activation stats:** mean 0.0036, p50 0.0031, p99 0.0110, **max 0.0940**.
- **Examples:** top-40 activating windows (≤2/doc for diversity) + 40 random-contrast windows
  (<p80 activation). Activating token wrapped `<<…>>`, ±12 tokens.
- **Two-stage blind eval** (no hypothesis leaked):
  1. *Explainer* agent sees the 40 top windows only → writes an explanation.
  2. *Detector* agent (fresh, blind) sees the explanation + a deterministically-shuffled mix of all
     80 windows (no activation values, no labels) → scores each 0–1 for match.
  3. Score the detector against ground truth.

## Auto-generated explanation (blind, top windows only)
> "Reflective, essayistic prose that grapples with big abstract ideas about human existence, belief,
> and values — humanities/worldview discourse rather than concrete narrative or technical
> instruction. Sub-themes: (1) philosophy & theory; (2) religion, spirituality & mythology;
> (3) moral/political/ideological argumentation and existential questions. The marked token is often
> a function/abstract noun inside a sentence framing a sweeping conceptual claim — the trigger is the
> surrounding register of abstract intellectual reflection, not a single word. Extends to generalized
> definitional/conceptual framing of abstract entities."

## Detection scoring (n=80; 40 top / 40 random)
| metric | value |
|---|---|
| ROC AUC (top vs random) | **0.937** |
| precision@40 (detector top-40) | **0.90** (36/40 true) |
| mean detector score, top | 0.463 |
| mean detector score, random | 0.056 |
| Spearman(detector score, true activation) | 0.734 |

## Representative top activators (act)
- 0.094 "more about philosophy … as **an** instrument to teach it"
- 0.065 "Philosophy of Art and the **Beautiful**"
- 0.039 "philosophers **interpret** the world … the point is to change it" (Marx)
- 0.032 "relationship with **Christ**"
- 0.032 "whole **world** view, a level plane"
- 0.031 "greatest mystery in **human** evolution"
- 0.029 "the **philosopher** Ralph Cudworth"
- 0.024 "regards homosexuality a **sin**"
- 0.020 "drive vol**ition**"; "NON **IO** (arte in mancanza di soggetto)" = *"NOT I (art without subject)"*
- 0.017 "supposed to **feel**"

Random contrast (act 0.001–0.005): legal opinions, clinical trials, patents, code, sports stats,
proper names — mundane technical/factual text. ~10–30× lower.

## Interpretation vs the d=3.88 readout finding
The hand-picked-prompt result labeled the L14 axis "first-person experiential/introspective
register." The bottom-up corpus result **refines** this: the axis is the broader register of
**abstract humanistic reflection on meaning / existence / belief / values** (philosophy, religion,
existential & moral-political argument). Introspection ("supposed to feel", "how all things in life
affect you") is one facet of that register. So E114 is confirmed as a *readout/detector* of a real,
coherent L14 register direction — and we now have a sharper, prompt-independent name for it.

## Provenance
- Binary: `llama-capture-activations` built from llama.cpp pinned commit `1772701f` (build 8493),
  `-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=86`, CUDA 12.8.93, g++ 13.3, on Vast box 42769252
  (2×RTX 3090, Florida). The prebuilt May-17 binary was abandoned (ABI mismatch vs image libs:
  undefined `llama_memory_breakdown_print`); built from source instead.
- Scripts: `autointerp_corpus.py`, `autointerp_capture.sh` (prefill+routing-only, disk-safe delete
  now gated on extract success), `autointerp_extract.py` (surrogateescape JSON read — BPE pieces
  split multibyte UTF-8), `prep_autointerp_score.py`, `score_autointerp.py`.
- Artifacts: `autointerp_examples.json` (pulled), `explainer_input.txt`, `detector_set.json`,
  `detector_key.json`, `detector_scores.json`. Raw npy deleted on box (disk-safe).

## Cross-model: base vs HauhauCS-Aggressive (same corpus, same capture)
Ran the identical 392-doc routing capture on `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive`
(Q8). **The uncensored fine-tune does not move E114's register.**
- Activation distribution ~identical: base mean/p50/p99/max = 0.0036/0.0031/0.0110/0.0940;
  hauhau = 0.0036/0.0032/0.0109/0.0966.
- Top-40 doc overlap: **Jaccard 0.920** (23/24 shared docs; base-only doc0100, hauhau-only doc0297).
  Top windows are essentially the same texts/tokens (philosophy, Marx, Christ, "world view",
  evolution mystery, Cudworth) at near-identical activations.
- Blind explainer on hauhau's top windows independently returns the **same label**: "discursive
  essay-style prose about abstract big-picture humanities/worldview topics — (1) philosophy &
  political ideology, (2) religion & theology, (3) contested moral/biological questions."

This matches the prior 3-model routing finding (E114 hotspot = L14 in all models; register not
E114-controllable): the fine-tune leaves *what E114 reads* intact. Note: base's `autointerp_examples.json`
was overwritten on pull; base data preserved in `detector_set.json`+`detector_key.json` and above.
Hauhau windows in `autointerp_examples_hauhau.json`.

## Not done — needs money (no credit): literal activation→language vector decode
The routing path characterizes E114 *correlationally* (what input fires it). Decoding the L14
*residual vector itself* into words needs the **bf16 residual stream** (A100-80GB/H200), which the
GGUF routing-only box cannot provide:
- **Patchscopes / SelfIE** — inject the real L14 vector into "The concept here is ___" and let the
  model verbalize its own activation (the most literal "reconstruct activation into language").
- **Qwen-Scope L14 SAE** — decompose the residual into named features → name the direction.
Parked until credit is available; see NEXT_SESSION.md.
