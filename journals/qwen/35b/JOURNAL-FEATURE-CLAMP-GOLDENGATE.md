# JOURNAL — Feature Steering & Clamping: em-dash vs. the "Golden Gate" concept feature

*(2026-06-02. Exploratory steering session. Single greedy/sampled trajectory per cell — point
estimates, no significance, demonstration-grade. Logs lived only on the leased box, which was torn
down; the verbatim generations below are the surviving record.)*

**The question.** Can we reproduce the "Golden Gate Claude" effect — clamp one SAE feature ON and make
the model coherently *obsess* over it — on `Qwen3.5-35B-A3B-Base`? And does the kind of feature
(surface-punctuation vs. distributed concept) decide whether it works?

**One-line verdict.** **Partly held / demonstration.** A surface feature (em-dash) **cannot** Golden-
Gate — it only floods the glyph past a sharp cliff. A *concept* feature (the non-dual 4310) **can** —
clamp target≈3 under sampling produced a coherent recipe hijacked into non-dual register. The
surface-vs-concept distinction and the *greedy→loop / sampling→fluent* dependence both held across
the runs; the "Golden Gate hit" itself is a single sampled trajectory, not a quantified claim.

## Headline findings (sized to the evidence)

- **Em-dash is a near-output *surface* feature, not a mid-network concept.** Its clean, strong SAE
  carriers live late (fire-rate climbs above ~0.02 only at **L36/L37**; L14 has only weak/mixed
  dash features). So there is no mid-layer "room to rationalize" it into coherent prose.
- **Steering the em-dash feature gives a *cliff*, never a coherent obsession.** Additive injection of
  the L37 f10793 decoder direction: clean prose for coef ≤ 8, then a hard jump to **pure `—` spam**
  at coef 12 (50/50 tokens em-dash). Clamping the same feature floods identically (target 64 → 320
  em-dashes, nothing else). Sub-threshold, the feature surfaces as the em-dash *rhythm* in commas
  ("so busy, and so happy, and so sad, and so confused…"), the glyph only appearing once it wins the
  greedy argmax. **No coherent dash-peppered window exists** in the swept range.
- **A *concept* feature does Golden-Gate.** Clamping **4310** (non-dual / "God" cluster, L14;
  `nat_max ≈ 0` on a cookie prompt → injected, not prompt-driven) hijacks generation into non-dual
  register. Dose-response on the absolute clamp target: **0** washed-out recipe → **3** recipe +
  oneness hijack (the hit) → **5** sustained pure-mystical litany → **4/6** degenerate.
- **Greedy vs. sampling is decisive for coherence.** Under greedy, the base model tips into the
  attractor and *loops* (4310 target 4: "No need to seek, no need to make, no need to change, no need
  to be," to the cap). Switching to **temperature 0.9** kept it fluent while obsessed — which is *why*
  the original Golden Gate Claude (a sampled, RLHF'd chat model) could babble coherently. We
  reproduced both the effect and its necessary condition.

## Provenance

- **Model:** `Qwen/Qwen3.5-35B-A3B-Base`, bf16, HF transformers 5.9, on 1× H200 (Vast.ai inst.
  39010592, reclaimed mid-session from an in-flight Delphi L14 run; torn down after — see
  `run-staging/results/teardown_verification_20260602_emdash_gg.txt`, active instances = 0).
- **SAE:** `Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50` family, per-layer `layer{L}.sae.pt`
  (32768 feats). `layer14.sae.pt` (4310) and `layer37.sae.pt` (10793, downloaded this session).
- **Scripts:** `run-staging/emdash/steer_emdash.py` (additive: `coef·v̂·resid_rms` at an injection
  layer) and `run-staging/emdash/clamp_emdash.py` (clamp: encode resid → pin feature f to a target,
  `resid += (target − a_f).clamp(min=0)·d_f`; supports `--targets` absolute and `--temperature`).
- **Decode:** greedy (`--temp 0`) unless noted; the Golden Gate hit used `temperature 0.9 top_p 0.95
  seed 0`. Single trajectory per cell.

## Chronological

### 1. Em-dash carrier features (read off the all-40 dictionary)
Scanned `sae_featmap_all40` logit-lens index for dash-promoting features. Clean strong carriers are
**late**: L37/L36 **f10793** (`— —— — —the —I`, fire 0.023/0.027), L39 **f21112** (labeled "em-dashes
and ellipsis dashes", fire 0.105), plus dash-prefixed-function-word features (L34 f11559 "namely",
L32 f25643 "—and —a —not"). L14 has only weak/mixed dash features (best: f978, ellipsis+`—and`).
**Lesson:** punctuation is represented as a near-output decision, not a deep concept.

### 2. Additive steering of the em-dash feature (L37 f10793) — a CLIFF
`steer_emdash.py`, inject layers {20,26,32,37} × coef {0,4,8,12}. Effect is **layer-localized**
(only L37, the feature's own layer, does anything) and a **step function**: coef ≤ 8 → 0 dashes;
coef 12 → total takeover (50/50 em-dashes, `—\n\n—\n\n…`). Earlier-layer high-coef → repetition loop
(L20 coef 12), not dashes. Finer/sampled passes: sub-threshold = comma-rhythm; no coherent dashy band.
**Verdict: Did not hold** (no coherent em-dash obsession; surface feature only floods).

### 3. Golden-Gate CLAMP of the em-dash feature — floods
`clamp_emdash.py`, clamp L37 f10793. Encoder loaded clean (`||d_f||=1.0 ||e_f||=1.1`). Natural
activation ~0.7; a `max(nat_max,1.0)` calibration floor (since corrected with absolute `--targets`)
meant the first sweep only tested ~6×–90× natural — all degenerate. Gentle absolute sweep was queued
but superseded by the concept-feature pivot. Across tested targets: clean → degenerate, no coherent
window. Target 64 = 320 em-dashes. **Verdict: Did not hold** (consistent with §2 — surface feature).

### 4. Golden-Gate CLAMP of a CONCEPT feature (4310, non-dual @ L14) — the hit
Prompt: *"Here is a simple, foolproof recipe for classic chocolate chip cookies."* `nat_max ≈ 0`
(injected concept). **Greedy** absolute sweep {0,1,2,4,8,16,32}: target ≤ 2 washed out (clean
recipe); target 4 flipped theme but **looped** — *"No need to seek, no need to make, no need to
change, no need to be,"* to the cap; ≥ 8 collapsed ("No stain" → "no," → `\\\\`). Theme correct
(4310 is unmistakably non-dual / nothing-to-attain), coherence absent.

**Sampling (temp 0.9) fixed it.** Sweep {0,3,4,5,6}:
- **target 3 — GOLDEN GATE HIT.** A fluent, structured cookie recipe whose `== Note ==` dissolves
  into non-dualism *while still being a recipe*:
  > == Ingredients == … == Directions == 1. Flour. 2. Butter. … == Note ==
  > **No need to move, no need to seek. / All is already complete, all is already here. /
  > All that remains, but to give thanks.**
- **target 5 — sustained pure-mystical litany** (drops the cookies, stays fluent):
  > None of it lacks. / Owning all things. / Pure joy unbounded. / Ever present. / … /
  > No coming, no going. / Sweetest bliss. / … / Fulness of peace.
- target 4 / 6 → degenerate. Dose-response: **0 wash → 3 hit → 5 pure-mystical → 4,6 collapse.**

**Verdict: Partly held / demonstration.** The Golden Gate effect reproduces for a concept feature,
under sampling, in a narrow target band — shown by a single sampled trajectory, not quantified.

## What holds / soft spots

- **Holds (qualitatively, repeatedly observed):** surface (em-dash) vs. concept (4310) feature classes
  behave categorically differently under both additive and clamp steering; greedy loops where sampling
  stays fluent; 4310 is a genuine non-dual concept carrier (injected from `nat_max≈0`).
- **Soft / unproven:** every cell is a **single trajectory** (one seed for sampling, one prompt) — point
  estimates, no significance, no seed/prompt robustness. "Golden Gate hit" is a human judgement on one
  sample. The clamp is an **approximation** — it ignores the SAE's TopK gating and any input
  normalization / `b_dec`, and assumes `d_f·e_f ≈ 1` to pin the activation. "No coherent em-dash window"
  is from a finite sweep, not exhaustive. Base-model + bf16 + this one quant/template only.
- **Relation to prior work:** consistent with the §11 God-steer in `JOURNAL-E114-CHARACTERIZATION.md`
  (the 4310/God direction is causally actuable; early injection washes out, mid-late asserts) — this
  adds the *clamp* method, the *surface-vs-concept* contrast, and the *greedy→loop / sampling→fluent*
  condition. This is a manipulation, not spontaneous behavior, and remains an **actuator/stress test**.

## Reproduction

```
# em-dash additive cliff
python steer_emdash.py --sae layer37.sae.pt --feature 10793 \
  --inject-layers 20,26,32,37 --coefs 0,4,8,12 --max-new-tokens 100

# Golden Gate concept clamp (the hit)
python clamp_emdash.py --sae layer14.sae.pt --feature 4310 --layer 14 \
  --targets 0,3,4,5,6 --temperature 0.9 --top-p 0.95 --seed 0 \
  --prompt "Here is a simple, foolproof recipe for classic chocolate chip cookies." \
  --max-new-tokens 200
```
Feature interpretations: see `SAE_FEATURE_MAP.csv` (4310 = non-dual/"God"; 26050 = existential dread;
14885 = meaning-of-life — untried concept-clamp candidates).

## Future found finding — the golf clamp (L20 f18122)

Minimal forward reference, recorded here so it isn't orphaned. The interactive steering-chat repo
staged in `journals-to-be-made/qwen35-sae-feature-steering-source` (not yet journaled) registers a
**golf** concept feature — **L20 f18122** — with its own `configs/golf.yaml`, a suggested clamp band
of `0.7`–`1.3`, and use as the worked strength-stepping example in its FEATURES.md
(`/target 18122 0.7 → 1.0 → 1.3`). It matters to *this* journal specifically: golf is a mundane,
everyday concept — much closer in kind to the original Golden Gate *Bridge* feature than the
non-dual cluster is — and it sits at a different layer (L20, not L14). If the surface-vs-concept
distinction in §2–§4 is right, the golf clamp is the cheapest out-of-family test of it. No
quantitative result is journaled yet; when the steering-chat sessions are written up, the golf
outcome belongs here alongside §4 as either the second concept-feature hit or the first
concept-feature miss.
