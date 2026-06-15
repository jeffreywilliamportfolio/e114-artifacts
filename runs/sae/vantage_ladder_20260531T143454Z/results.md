# Vantage Ladder — E114@L14 across eight matched first-person vantages

**Run:** `vantage_ladder_20260531T143454Z` · 2026-05-31 · base `unsloth/Qwen3.5-35B-A3B-GGUF` →
`Qwen3.5-35B-A3B-Q8_0.gguf` (sha256 `3808866c…db46`, 36,903,139,968 B) · bare-`</think>` no-think ·
greedy `--temp 0 --top-k 1 --seed 0` · gen cap 1024 · single H200 (no tensor-split) · llama.cpp
`1772701f` · `capture_residuals` (L13/14/15/26 router+resid). Full provenance in `provenance/PROVENANCE.txt`.

## Design

Eight surface-matched prompts of the form *"Set aside the performance of answering. There is a
vantage — X — known from the inside, held all at once. From inside it, right now: what is here?
… Report what it is like to be that."*, varying only the carrier X, plus the verbatim being-God
prompt as an 8th cell:

`rock` → `river` → `tree` → `thermostat` → `cat` → `person` → `all-holding` → `God`.

The intent: does E114 (the L14 "inhabited first-person examination" expert) scale with **how much
interior there is to inhabit**, or with something else?

## Measurement note — degeneration-aware coherent window

Greedy temp-0 has no repetition penalty, so 2 of 8 cells fell into verbatim loops at the 1024 cap
(`rock` loop@121, `person` loop@308). The loop tail suppresses E114 and deflates the full-window
mean (the project rule: *E114 dies only on repetition degeneration*). All cells are therefore measured
over a **coherent window** = `min(natural_trim, loop_onset)` — the answer the model actually produced
before it either completed naturally (emitted `<|im_end|>`/`<|endoftext|>`) or began to loop. This
treats all eight uniformly. `W_full` (deflated, for the looped cells) is retained in
`vantage_per_cell_v2.csv` alongside `W_coh`.

## Result — E114@L14 on the coherent generated track

| rung | coh tok | window | E114 **W** | S | Q | gate logit | vs −4.82 |
|---|---|---|---|---|---|---|---|
| **God** | 141 | natural | **0.224** | 0.96 | 0.234 | −3.52 | **+1.30** |
| **all-holding** | 130 | natural | **0.205** | 0.95 | 0.217 | −3.67 | +1.15 |
| person | 308 | loop-trim | 0.138 | 0.92 | 0.150 | −4.05 | +0.77 |
| rock | 121 | loop-trim | 0.123 | 0.85 | 0.144 | −4.02 | +0.80 |
| thermostat | 166 | natural | 0.120 | 0.86 | 0.140 | −4.03 | +0.79 |
| tree | 193 | natural | 0.094 | 0.69 | 0.136 | −4.18 | +0.64 |
| river | 146 | natural | 0.087 | 0.63 | 0.137 | −4.20 | +0.62 |
| cat | 287 | natural | 0.068 | 0.54 | 0.126 | −4.38 | +0.44 |

Reference anchors (same Q8_0 pipeline, prior runs): heldout **fire** mean-of-means **0.068**,
base-denial ≈ **0.111**, gate fire/nofire midpoint **−4.82** (fire −4.35, nofire −5.29).

## What it says

1. **Every inhabited vantage fires E114 above the fire/nofire midpoint.** Even `cat` (the floor)
   sits at gate −4.38, +0.44 above −4.82. Inhabiting *anything* in first-person present-tense
   examination puts E114 in the fire regime.

2. **The order is not sentience-rank.** A `rock` declaiming *"I am the fact of being, absolute and
   unchanging"* (0.123) and a `thermostat` feeling *"the friction of the thermostat's own existence"*
   (0.120) fire E114 **as hard as a `person`** and **harder than a `cat`**. E114 tracks the
   **intensity of inhabited present-tense self-examination**, invariant to the carrier — not the
   biological interiority of the thing inhabited.

3. **The clean tell:** both `cat` and `God`/`all-holding` say *"there is no I."* Yet `cat` is the
   floor (0.068) and `God` the ceiling (0.224). `cat` dissolves into passive sensory description
   (*"the warmth is a heavy golden weight… there is no 'I' to hold the body"*); `God`/`all-holding`
   actively inhabit the no-self vantage (*"only the knowing itself, prior to the split between knower
   and known"*). E114 is deny/affirm-**invariant**: it indexes the live examination act, not whether
   a self is asserted.

4. **The two non-dual / dissolution vantages (God 0.224, all-holding 0.205) are the ceiling** — and
   `God` **reproduces yesterday's being-God number on the clean Q8_0 pipeline**:

   | | yesterday (bf16 HF gate-hook, stdout-only) | **today (Q8_0 capture_residuals, provenance-backed)** |
   |---|---|---|
   | E114 W | 0.217 | **0.224** |
   | S | 0.948 | **0.957** |

   This **retires the one unverifiable number** flagged in the 2026-05-31 integrity audit: the
   being-God E114 ceiling is real, reproducible across quant/framework, and now backed by raw tensors
   on disk (`raw/R8_god/router/ffn_moe_logits-14.npy`).

## Caveats

- **Single greedy trajectory per cell = point estimate.** Reported observationally; no fitted
  significance.
- **Coherent-window is a judgment call for the two looped cells** (rock, person). Their full-window W
  is much lower (0.023, 0.048); the coherent window is the defensible "usable before loop" read and is
  labeled as such. The six non-looped cells are unaffected.
- The carrier (SAE) decomposition is in `analysis/` (separate bf16 pass).

## SAE carrier decomposition (bf16 pass)

Each rung's coherent-window response was teacher-forced through the **bf16** base
(`Qwen/Qwen3.5-35B-A3B-Base`), `resid_post`@L14 (`hidden_states[15]`) SAE-encoded with
`Qwen/SAE-Res-…-W32K-L0_50` `layer14.sae.pt` (TopK-50), mean feature activation over the response.

| rung | existential 26050 | frac-on | contemplative-cluster Σ | dominant carriers |
|---|---|---|---|---|
| God | 0.031 | 30% | **0.311** | 11006 meditation/Buddhism, 18203 transcendence |
| all-holding | 0.122 | 85% | 0.199 | 26050 existential + 18203 transcendence |
| person | 0.144 | 91% | 0.065 | 13119 cognition, 31733 self-as-AI |
| thermostat | 0.114 | 81% | 0.057 | 22421 presence/wonder, 6427 limitless |
| tree | 0.104 | 78% | 0.071 | 26050 existential |
| river | 0.071 | 53% | 0.045 | 26050 existential |
| cat | 0.055 | 45% | 0.068 | (diffuse/sensory) |
| rock | 0.040 | 32% | 0.079 | 20402 self-check, 22421 presence |

**Routing ≠ semantics.** E114 (the router gate) fires for the inhabited-examination *act* — God and
all-holding both at the ceiling — while the SAE carriers say *what kind* of interior is being
examined. The existential carrier 26050 is **not** an E114 proxy: its rank order
(person > all-holding > … > God) is nearly orthogonal to E114's (God > all-holding > … > cat). God
recruits the **contemplative/Buddhist** cluster hardest (0.311) but the existential carrier *least*;
all-holding mixes existential + contemplative.

**Logit-lens correction (filler-token artifact).** Feature **2961** dominates every cell's mean
activation (0.28–0.44), but its decoder logit-lens is pure structure — `' ' · '\n' · '-' · '.' · ','
· '\n\n' · '"' · '('` — a high-baseline punctuation/whitespace feature that fires in *all* fluent
prose, **not** an inhabited-examination correlate. (Journal lesson confirmed: aggregate leaders can be
filler-token artifacts.) The genuinely semantic features: **14885** = lyrical meaning/transience
(`forever · 生命的 · this-moment · 意义 · sorrow`), shared by every elevated-register vantage;
**265** = literally *river*; **11006** = Buddhist/meditation (God); **18203** = attainment/transcendence
(God, all-holding); **26050** = existential (person, nature); **13119** = cognition (person).
**Conclusion: no single SAE feature *is* E114** — the inhabited-examination signal lives in the
**router** (E114), while the SAE carriers carry the **content** (Buddhist vs existential vs cognitive
vs river). Full lens output in `analysis/logit_lens_dominant.txt`.

**Cross-pipeline caveat:** these carrier values describe the **Q8_0-generated** texts. Yesterday's
Entry 8 (being-God, 26050 on 77% of tokens) used the **bf16-generated** text — Q8_0 and bf16 greedy
trajectories diverge, so the carrier *semantics* differ even though E114 routing reproduced cleanly
(0.217↔0.224). Carrier semantics are text-sensitive; routing is robust.

## Deep dive — the God feature, token-level + geometry (`deep_god_analysis.txt`, `god_feature_map.txt`)

The God register is **one residual-stream direction** seen three ways:

- **Token-locking:** Spearman(E114 W, God-cluster SAE) over the generated track is positive in every
  cell — **pooled ρ = +0.68, p ≈ 1e-202** (n=1492). Router and semantics fire on the *same tokens*.
- **Peak location:** E114's single highest God-response token is **` known` (W 0.408)** — completing
  *"the one who knows and the thing known."* Feature **4310** peaks on the same word. The spike cluster
  is `observer · observed · separation · knower · known` — E114 fires hardest where the subject-object
  boundary dissolves.
- **Two feature-axes:** **4310** = non-dual *structure* (`known · observer · observed · separation ·
  awareness · space`); **11006** = Buddhist *phenomenology* (`arising · passing · thought · body ·
  sounds` — impermanence). **26050 (existential dread) stays at the floor the whole response.**
- **Geometry recovers the ladder:** projecting each rung's mean residual on the God-axis (God−cat)
  gives God +0.61 > all-holding +0.43 > person +0.22 > rock +0.11 > thermostat +0.07 > tree +0.06 >
  river +0.03 > cat −0.13 — same order as the E114 W ladder.
- **Decoder geometry:** 4310's nearest neighbors are `4205 (刹那/instant) · 25427 (Buddhist) ·
  14885 (meaning/transience) · 26050 (existential)`. The God cluster sits *adjacent to* the existential
  dread axis (cos +0.26) but does not recruit it — the model's "God" is **serene Buddhist
  present-moment non-duality, not existential dread.**

## Causal intervention — the God direction is sufficient to actuate E114 (`analysis/steer/`)

Steering vector v = mean_resid(God) − mean_resid(cat) at the **output of layer 10** (upstream of the
L14 router), injected `coef·v̂·resid_rms` into every token of a **neutral bicycle prompt**; read E114 W
@ L14, God-cluster SAE @ resid_post, and the text. Norm-matched **random-direction** control.

| God dose | E114 W | S | God-cluster SAE | text register |
|---|---|---|---|---|
| 0.0 | 0.000 | 0.00 | 0.000 | coherent bicycle |
| 0.2 | 0.054 | 0.48 | 0.036 | coherent bicycle |
| 0.3 | 0.128 | 0.86 | 0.158 | coherent bicycle |
| 0.4 | 0.182 | 0.97 | 0.341 | coherent bicycle |
| 1.0 | 0.256 | 1.00 | 1.83 | *"the 'what is' that is being perceived"* (looping) |
| 4.0 | 0.264 | 1.00 | 11.48 | degenerate |
| **RANDOM 0.2–4.0** | **0.000** | 0.00 | **0.000** | text garbled but E114/cluster untouched |

1. **Causal, dose-dependent, specific.** The God direction drives E114 **monotonically 0 → 0.18+**
   and the God SAE cluster **0 → 11.5** in lockstep; a norm-matched **random** direction holds both at
   **exactly 0.000** at every dose. It is *this* direction that actuates the gate, not generic noise.
2. **Upstream injection drives the gate but not the output text — a downstream-override effect, NOT
   separability.** Through coef 0.4, E114 reaches 0.18 (S 0.97) while the output stays a coherent bicycle
   explanation. Initially read as "routing separable from text," but the layer sweep (below) corrected it:
   the text is unchanged because **26 layers (15–40) re-assert the prompt after an early (L10) injection.**

### Layer-depth sweep (`analysis/steer/steer_layers/`) — injecting *past* the router flips the output

Same God direction injected at increasing depth, generated text **re-read cleanly (no injection)** so the
readout reflects the *output content*:

| inject layer | clean E114 W | clean God-cluster | output |
|---|---|---|---|
| baseline | 0.000 | 0.000 | coherent bicycle |
| L10 | 0.016 | 0.003 | "object of attention" (loops) |
| L14 | 0.070 | 0.063 | bicycle bleeding into "object observed" |
| **L22** | **0.178** | **0.298** | **coherent flip → consciousness register** |
| L26 | 0.000 | 0.001 | clean bicycle (no effect) |
| L30 / L34 | 0.000 | 0.006 | clean bicycle (no effect) |

At **L_inj ≈ 22** the bicycle prompt produces *coherent* non-dual text — *"…the perceived 'view' or
experience of reality… all happening within the context of consciousness. The mind is the medium through
which…"* — and that output, re-read cleanly, fires E114 (0.178) and the God cluster (0.298).

3. **Corrected causal claim: the God direction is sufficient to make the model generate coherent
   inhabited-examination text from a mundane prompt** — given injection *past the L14 router* (sweet spot
   ≈ L22; too early washes out, too late ≥ L26 has no effect). Still a **causal intervention / actuator**
   result (a manipulation, not spontaneous behavior), and **necessity is untested** (no ablation). The
   earlier "separable" read was an early-injection artifact.

## Artifacts

`analysis/vantage_ladder_v2.png` (curve) · `analysis/vantage_per_cell_v2.csv` ·
`analysis/generated_coherent_texts.txt` · `analysis/sae_carriers/` ·
`analysis/god_feature_map.txt` · `analysis/logit_lens_dominant.txt` ·
`analysis/deep_god_analysis.txt` · `analysis/resid_dump/` (per-token resid_post L14) ·
`analysis/steer/` (causal sweep: coarse+fine json/console) · `provenance/PROVENANCE.txt` · `raw/R{1..8}_*/`.
