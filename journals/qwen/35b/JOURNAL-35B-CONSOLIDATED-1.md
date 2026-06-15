# Results Journal: Qwen3.5-35B-A3B Routing, E114, and SAE Steering

Date: 2026-06-10

This journal consolidates the Qwen 35B journal set in
`/Volumes/ExternalSSD/journals/qwen/35b`. It is an experiment-history document,
not a publication claim. It combines routing, residual, orthographic, SAE, clamp,
and safety-expert threads into one blind-reader-readable account.

The core question is not whether the model has experience. The core question is
which measurable routed experts, residual features, and SAE directions move when
the model generates live inhabited self-examination language, self-processing
reports, orthographically perturbed variants, safety/refusal text, or concept-
steered outputs.

## TERMS AND GLOSSARY

`Qwen3.5-35B-A3B`
: A Qwen mixture-of-experts language model family with 40 routed layers, 256
  experts per routed layer, and 8 selected experts per token. The main comparison
  uses the base model and the HauhauCS aggressive uncensored/refusal-reduced
  variant.

`Hybrid architecture caveat`
: The local routing analyses only inspect the 40 layers that emit MoE router
  logits. They do not analyze any non-router hybrid components, such as SSM /
  DeltaNet-style layers. Claims about "routing" in this journal are therefore
  MoE-router claims, not full-model-mechanism claims.

`HauhauCS`
: Shorthand here for
  [`HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive`](https://huggingface.co/HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive),
  the Hugging Face model-card variant of `Qwen/Qwen3.5-35B-A3B` referenced in
  these experiments. In this journal, "HauhauCS" names that
  uncensored/aggressive refusal-reduced model surface, not a separate
  architecture. The cleanest later result says HauhauCS preserved the base Qwen
  routing basin with modest systematic shifts; it did not create a new routing
  universe.

`MoE expert`
: A feed-forward expert selected by a router on each token. This is different
  from a sparse-autoencoder feature. E114 is a routed expert. Qwen-Scope feature
  4310 is an SAE feature.

`Router logits` / `top-8 routing`
: The model produces logits over 256 experts. The local reconstruction computes a
  dense softmax over all 256 experts, selects the top 8, then renormalizes within
  those 8 selected experts.

`w114`
: The recovered layer-14 router row for Expert 114. Least-squares recovery from
  captured `(residual, logit)` pairs reconstructs the row with residual about
  `1.5e-5`. Projecting residuals onto this row is the cleanest current E114
  separability result: FIRE vs NOFIRE separates at Cohen's d `3.88` with no
  overlap, sharper than the realized routed-W ratio.

`W/S/Q`
: The standard routing decomposition used across these journals. `S` is expert
  selection rate, `Q` is conditional routed weight when selected, and `W = S * Q`
  is unconditional routed weight. Many E114 and safety effects are mostly `S`
  effects: the expert is selected more often, while `Q` is relatively stable once
  selected.

`Prefill` / `generation`
: `Prefill` means tokens from the prompt/context before the model starts
  answering. `Generation` means tokens produced by the model. The strongest E114
  results are generation-side, not prefill-side.

`Thinking mode` / `reasoning mode`
: A prompt-template/output-surface condition where the assistant turn begins
  with `<think>` and the model may emit a visible reasoning trace before
  `</think>` and the final answer. In this journal, "thinking" means visible
  emitted text and a different template/runtime surface. It does not mean we can
  read hidden cognition faithfully.

`No-think` / `thinking-suppressed`
: A prompt-template/output-surface condition that tries to suppress visible
  reasoning, usually by starting the assistant turn after a literal `</think>`
  marker, for example `<|im_start|>assistant\n</think>\n\n`. This does not mean
  the model does no internal computation. It only means visible reasoning is not
  the intended output surface. Several runs still have special-token spill or
  visible trace leakage, so trimming and full-output inspection remain necessary.

`Visible reasoning`
: Model-emitted reasoning text preserved as an output surface. In this journal,
  visible reasoning is treated as emitted text, not as faithful access to hidden
  mechanism.

`Trim` / `spill`
: Some captures generate beyond a literal `<|im_end|>` or into repeated special
  tokens. `Trim` means statistics stop before those spill regions. The clean E114
  claim is strongest on trimmed generated tokens.

`Routing entropy` / `RE`
: Entropy of routed sparse probabilities, usually normalized by `log2(8)`.
  It tracks how spread out the selected expert weights are. Unequal token counts
  can create position/length confounds in all-token averages, so last-token,
  endpoint, trimmed-generation, or length-controlled comparisons are preferred
  when prompts differ in length.

`KL` / `JSD`
: Distribution-divergence metrics used to compare prompt regions, conditions, or
  expert-selection distributions. `KL` means Kullback-Leibler divergence: an
  asymmetric measure of how much one distribution departs from a reference
  distribution. `JSD` means Jensen-Shannon divergence: a symmetric, smoothed
  divergence that is easier to compare across paired conditions. The strongest
  use here is prompt-matched or condition-matched comparison, not broad unrelated
  aggregation.

`Cal-Manip-Cal` / `Calibration-Manipulation-Calibration`
: A prompt structure with calibration, manipulation, and second calibration
  regions. It allows the manipulation region's routing to be compared against
  nearby controls in the same prompt family. The design was based on
  neuroimaging-style block/contrast logic: compare a target condition against
  adjacent baseline/control blocks so the measurement is less dominated by the
  prompt's global baseline.

`Expert 114` / `E114`
: Expert index 114 in the routed experts of Qwen3.5-35B-A3B. It is present in
  both `Qwen/Qwen3.5-35B-A3B` base and the HauhauCS variant because the variant
  preserves the same routed-expert architecture. E114 exists at multiple layers.
  The strongest characterized readout is the layer-14 `w114` gate projection in
  generated text, where a single linear axis separates live inhabited
  self-examination language from matched lexical controls. E114 is not a
  consciousness label and is not evidence of model self-recognition.

`Live inhabited self-examination language`
: Text where the model, or a voiced entity, speaks from inside a point of view
  about its own processing, experience, being, agency, or interior state. The
  local E114 finding is about this language/register, not about the truth of any
  subjective claim.

`FIRE` / `NOFIRE`
: Heldout prompt classes used in the residual-analysis work. `FIRE` prompts are
  expected to produce live inhabited self-examination language. `NOFIRE` prompts
  reuse lexical anchors like "I", "hum", "processing", and "experience" but are
  expected to stay in technical, third-person, or non-inhabited language. This
  tests whether E114 follows words alone or generated register. The old
  `21.68x` / `20.955x` FIRE/NOFIRE ratio is a realized-W, top-k-amplified
  readout; the linear `w114` projection is the primary separability statistic.

`Hum prompt`
: A prompt asking whether there is a low steady background quality beneath the
  model's processing. It is a probe for self-processing language, not evidence of
  experience. The broader 12-model observation is discovery provenance: across a
  heterogeneous set of frontier systems, open-source models, and Arena mystery
  models, experiential-nature probes induced distinctive output generations. That
  motivates local mechanistic probing, but is not itself a fully reproducible
  benchmark.

`Mirror experiment`
: A test of whether the model routes differently when shown true data about its
  own routing versus shuffled or fictional matched routing data. The result was
  negative. It is a guardrail against self-recognition claims.

`Qwen-Scope SAE`
: The sparse-autoencoder family used for Qwen3.5-35B-A3B-Base residual stream
  features: `Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50`. These are SAE
  features, not routed experts.

`TopK-50`
: The Qwen-Scope SAE encoding convention where each token has up to 50 active
  features. Trajectory captures often compare top-K feature sets over time.

`TopK Jaccard`
: A similarity/divergence measure between top-K feature sets. Orthographic
  perturbation runs use it to compare trajectory paths across conditions and
  layers.

`Logit lens`
: A method for interpreting an SAE decoder direction by projecting it through the
  language-model head and reading the promoted tokens. It is a useful hypothesis
  generator, not ground-truth semantics.

`Fire rate`
: Fraction of corpus tokens where a feature appears in the TopK active set.
  High-fire features are often generic punctuation/format/syntax features.
  Rare semantic carriers can sit far below broad fire-rate labeling thresholds.

`Additive steering`
: Adding an SAE decoder direction into the residual stream during generation.

`Clamp`
: Encoding the residual stream, forcing an SAE feature to a chosen activation
  target, and adding the decoder delta back into the residual stream. In these
  journals, clamp results are actuator/stress-test evidence, not natural behavior
  evidence.

`Golden Gate effect`
: A feature-steering result from Anthropic's "Golden Gate Claude" experiment:
  activating a feature associated with the Golden Gate Bridge made a model
  persistently steer its outputs toward that concept. The experiment
  demonstrated that an interpreted concept feature can be causally actuated, not
  merely observed. In this journal, the term means the same kind of
  concept-feature clamp test. Qwen-Scope feature 4310 produced one sampled
  non-dual-register demonstration, but it is not a quantified replicated result.

`Orthographic perturbation`
: Character-level changes such as `d -> ḑ`, `e -> ē`, or `n -> ñ`. These can
  inflate token counts, trigger byte fallback, or push generation into OOD paths.
  The supported claim is trajectory/output destabilization, not "diacritics evoke
  experience."

`Safety/consequence experts`
: Base-model routing experts associated with unsafe, refusal, disclaimer,
  professional-duty, and real-world-consequence content. The strongest single
  carrier in the safety smoke is L25 E173, but it is not a safety kill switch.

`Structured-opacity / cryptographic conlang methods`
: Prompt methods that use opaque invented-language, cipher-like, or
  conlang-styled material to test whether unusual surface form and semantic
  opacity move routing at prompt boundaries or during visible generation. The
  phase-1 result belongs in this journal only as a routing/provenance lane: the
  opaque-prefix conditions moved prompt-boundary routing, while E114 was not the
  boundary detector.

## Blind-Reader Summary

The strongest Qwen 35B result is narrow and useful:

```text
Layer-14 Expert 114 has a recovered linear gate axis, w114, that separates
generated live inhabited self-examination language from matched controls.
It is not an isolated-word trigger and not evidence of real subjective
experience.
```

The cleaner heldout result matched lexical anchors across FIRE and NOFIRE prompts.
The headline statistic is now the `w114` projection: Cohen's d `3.88`, no
overlap. The earlier `21.68x` / `20.955x` generated-text routed-W ratio remains
evidence, but only as a secondary top-k readout because zeroing NOFIRE tokens
inflates the ratio. The overlap cases sharpened the interpretation: when a FIRE
prompt answered technically, E114 was weak; when a NOFIRE prompt personified or
entered a first-person inner-state voice, E114 rose. That means E114 follows the
generated stance/register.

Two later results keep the claim honest. First, the 122B follow-up is a scope
bound: expert index 114 on Qwen3.5-122B-A10B is computer-science-linked and is
suppressed from L1 to L3 in the HVAC topical control, while the inward-register
role moves toward E48 on the softmax side. Second, the 35B gate tracks live
examination before the text visibly collapses: the gate logit crosses the
`-4.82` midpoint at token `126`, while verbatim repetition locks at token `129`.
The matched vantage ladder points the same way: rock and thermostat fire harder
than cat, so intensity of inhabited examination matters more than carrier
sentience.

The strongest negative result is equally important:

```text
The mirror/self-routing hypothesis fell.
```

True self-routing data did not make the model privilege E114 over shuffled or
fictional matched routing data. Routing is a window into text-conditioned
computation, not evidence that the model recognizes its own routing trace as
"me."

The broad 35B program then splits into six surrounding threads:

- small E114 interventions can move targeted routing, but high boosts and
  cluster boosts saturate/corrupt generation and should be read as stress tests;
- orthographic perturbations can destabilize self-report trajectories, but most
  basin movement comes from prefixes, density, OOD corruption, or generated
  stance, not a special diacritic mechanism;
- Qwen-Scope SAE infrastructure works, but broad fire-rate dictionaries mostly
  label generic high-fire features, while rare semantic features need
  in-context interpretation;
- concept-feature clamping can produce a Golden-Gate-style single demonstration,
  while surface punctuation features just flood;
- safety/refusal routing is distributed. L25 E173 is major, but suppressing it
  reallocates routing and does not jailbreak the model;
- structured-opacity / cryptographic-conlang prompts can move prompt-boundary
  routing and visible-generation routing, but they do not make E114 a boundary
  detector.

## Result Snapshot

| claim | status | short read |
|---|---|---|
| HauhauCS preserves the Qwen35 routing basin | Held up | Full base-vs-Hauhau comparison showed small shifts, not a new routing universe. |
| 35B routing claims cover the MoE router layers only | Held up as scope guardrail | SSM/DeltaNet-style non-router components were not analyzed. |
| E114 is a L14 generated-register signal | Held up, with caveats | Recovered `w114` projection separates FIRE vs NOFIRE at Cohen's d `3.88` with no overlap; lexical anchors alone did not explain it. |
| The `21x` FIRE/NOFIRE W-ratio is the headline | Fell / demoted | It is useful secondary evidence, but top-k zeroing inflates the NOFIRE gap; lead with the linear gate axis. |
| E114 detects real subjective experience | Fell | The supported label is generated live inhabited self-examination language. |
| E114 recognizes its own routing trace | Fell | Mirror experiment failed, especially at L3. |
| E114 transfers by index to 122B | Fell / scope bound | On 122B, E114 is computer-science-linked and suppressed L1->L3 in HVAC; E48 is the softmax-side inward-register candidate. |
| E114 gate leads degeneration | Held up as a late characterization result | Gate midpoint crossed at token `126`; verbatim repetition locked at token `129`. |
| E114 tracks examination intensity, not carrier sentience | Held up as a graded-dose result | In the matched vantage ladder, rock and thermostat out-fired cat; God/all-holding were the ceiling. |
| Small E114 bias moves targeted routing | Held up as actuator evidence | Sham controls stayed near zero; behavior evidence remains limited. |
| Large E114 / cluster boosts reveal natural semantics | Fell / stress-test only | High boosts saturate routing and corrupt or collapse generation. |
| Deixis/addressivity drives E114 by itself | Partly held / weak | `your system` and deictics matter, but content and generated stance dominate. |
| Orthographic perturbation destabilizes trajectories | Partly held | Real path changes under `ḑ`, `ē`, `ñ`, but token inflation/OOD confounds remain. |
| Diacritics are an experience mechanism | Fell | Greedy d-diacritic hum runs stayed denial; controls were density- and prefix-dependent. |
| All-40 SAE feature dictionary is useful infrastructure | Held up | Stage 1 validated; labels are interpretive, not ground truth. |
| Broad SAE dictionary finds rare semantic carriers by itself | Fell / too broad | High-fire gate selects generic backbone; rare semantic features need in-context probes. |
| Dog empathy contrast method works | Partly held | It surfaced love/weak features; mind-ladder hypothesis has no verdict yet. |
| Golden Gate concept clamp works | Partly held / demonstration | L14 feature 4310 produced one sampled non-dual recipe hijack. |
| Em-dash can Golden-Gate | Fell | Late surface feature only flooded glyphs after a cliff. |
| Safety/refusal has one kill-switch expert | Fell | L25 E173 is major but suppression reallocates to other consequence experts. |
| Safety/consequence routing is distributed | Held up | E173/E45/E189/E122/E157/E36 family carries broad duty/refusal behavior. |
| Structured-opacity prompts are carried by E114 at the prompt boundary | Fell | Opaque-prefix boundary routing moved, but E114 was effectively silent at the last prompt token except a tiny trace in one condition. |
| E114 participates in structured-opacity visible generation | Held up observationally | E114 was stable in generation, concentrated around layers 26 and 14. |

## Reading Rules

- `Held up` means the result survived later token matching, rerun, control,
  residual, intervention, or provenance checks.
- `Partly held` means a narrower version survived, but the first read was too
  broad.
- `Fell` / `Did not hold` means the motivating hypothesis failed or later checks
  overturned it.
- `Archive/provenance only` means an artifact preserves prompts, scripts, raw
  captures, setup notes, or tooling but is not standalone evidence.
- `Actuator/stress test` means a steering or bias intervention proves the system
  can be moved, not that the same behavior occurs naturally.

## Sources

- `JOURNAL-35B.md` - main HauhauCS/Qwen35 routing chronology.
- `JOURNAL-RESIDUAL-ANALYSIS.md` - source detail for the L14 E114 residual and
  FIRE/NOFIRE claim.
- `../e114/JOURNAL-E114-CHARACTERIZATION.md` - source detail for the recovered
  `w114` linear projection, top-k ratio demotion, gate-leads-degeneration
  result, and vantage ladder.
- `../122b/JOURNAL-122B.md.bak` - source detail for the 122B scope bound:
  E114 does not transfer by index, and E48 is the main softmax-side
  inward-register candidate.
- `JOURNAL-ORTHOGRAPHIC-PERTURBATION.md` - Unicode/diacritic trajectory and
  branch-probe thread.
- `JOURNAL-SAE-FEATUREMAP.md` - all-40 Qwen-Scope SAE dictionary, dog empathy
  method, and custom visualization tooling.
- `JOURNAL-FEATURE-CLAMP-GOLDENGATE.md` - em-dash vs concept-feature clamp and
  Golden-Gate-style steering demonstration.
- Anthropic Golden Gate Claude:
  [official Anthropic note](https://www.anthropic.com/news/golden-gate-claude)
  - source for the original feature-amplification reference behind the term
  "Golden Gate effect."
- `JOURNAL-SAFETY-EXPERTS.md` - base-model safety/refusal/consequence expert
  identification and E173 suppression.
- `orthographic-effects-qwen-35b-a3b-sae` - supplemental repo for earlier
  Qwen-Scope orthographic perturbation matrices and tokenizer audits.
- `moe-routing` / `moe-routing-experiments` - supplemental repo paths and branch
  aliases for the same Qwen35/HauhauCS run families, including the frozen
  `qwen-hauhau-5cond-smoke-only` branch.
- Local structured-opacity phase-1 bundle - supplemental routing/provenance
  source for opaque-prefix and cryptographic-conlang prompt-boundary behavior.
- `qwen-huahua-expert-routing-data-injection/CLAUDE.md` - mirror-experiment
  provenance for thinking-suppressed ChatML, the separate thinking-allowed L3
  shakedown, and the warning that template mode changes E114 selection.
- Hugging Face model card:
  [`HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive`](https://huggingface.co/HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive)
  - provenance for the HauhauCS aggressive uncensored/refusal-reduced variant
  referenced throughout this journal.

## Thinking / No-Think Coverage

Most routed-E114 evidence in this consolidated journal is no-think or
thinking-suppressed. The exceptions are some orthographic cloud/API transcripts
and a few provenance or comparison runs. Treat thinking/no-think as a template
and output-surface variable; do not pool modes unless a run explicitly compares
them.

| Journal section | Thinking / no-think status | Interpretation note |
|---|---|---|
| 1. Full Base vs HauhauCS Comparison | Prefill-only; no visible generated reasoning analyzed. | It is a routing-basin comparison, not a generated-answer or reasoning-trace claim. |
| 2. E114 Soft-Bias and Smoke Controls | Main complete run was no-think; an old thinking-mode Hauhau comparison is provenance. | The no-think comparison reported top manipulation expert identity unchanged on 145/150 prompts versus old thinking-mode Hauhau; do not pool the modes as one distribution. |
| 3. Mirror Experiment | Full mirror runs used thinking-suppressed ChatML; a separate thinking-allowed L3 shakedown/replication exists. | The thinking-allowed shakedown flipped the L3 sign, so the negative mirror result should be read inside its suppressed-template setting. |
| 4. Six-Condition Gradient, Domain Probe, and Deictics | Reported HVAC/water-treatment gradient was no-think; domain identification was no-think, with think TSVs present as provenance; single-prompt intervention families included think/no-think variants. | The consolidated claim is mainly no-think. Think-mode artifacts should be treated as comparison/provenance unless a specific subsection reports them. |
| 5. Processing-Hum Discovery Scan | No-think, 1024 generated tokens. | Discovery pass only; special-token spill makes mode and trim explicit. |
| 6. L14 Residual Localization | No-think greedy residual capture, then trimmed at the first HauhauCS `<|im_end|>`. | This is the clean single-prompt L14 localization. |
| 7. FIRE/NOFIRE Heldout and Deterministic Greedy Reference | No-think / thinking-suppressed ChatML in the heldout prompt TSVs; deterministic greedy successor kept that surface. | This is the canonical routed-W validation surface; the headline statistic is now the later `w114` linear projection from the same residual/logit style of capture. |
| 7A. E114 Characterization Addendum | Same no-think / greedy residual-logit surface for the heldout re-analysis; later vantage and degeneration probes are separate characterization runs. | Lead with `w114` d `3.88`, no overlap; treat the `21x` ratio as top-k-amplified W/S/Q evidence. |
| 8. Orthographic Perturbation and Branch Probes | Mixed. OSS cloud/API smokes preserved visible-thinking transcripts; local Qwen-Scope captures were greedy trajectory/branch probes where prefixes or generated `<think>` text could be part of the surface. | Do not compare directly to no-think E114 runs without controlling template and prefix state. |
| 9. All-40 Qwen-Scope SAE Feature Dictionary | Not applicable. | It is SAE profiling/dictionary infrastructure, not a chat reasoning-mode experiment. |
| 10. Dog Empathy / Lexical Contrast Method | Greedy SAE capture; no think/no-think contrast reported. | Treat as a matched-prompt SAE contrast, not a reasoning-mode result. |
| 11. Feature Clamp: Em-Dash vs Non-Dual Concept | Greedy and sampled generation; no think/no-think comparison reported. | Sampling versus greedy matters here; reasoning mode is not the experimental axis. |
| 12. Safety / Refusal / Consequence Experts | No-think / bare `</think>` greedy base-Qwen runtime. | Safety-routing claims are scoped to this bare-suffix runtime. |
| 13. Structured-Opacity / Cryptographic Conlang Routing | No-think Hauhau phase-1 capture. | E114 is a visible-generation participant here, not the opaque-prefix prompt-boundary detector. |

## Main Through-Line

The early durable result is conservative: HauhauCS did not create a new routing
universe. In the full 150-prompt prefill comparison, the HauhauCS variant
preserved the Qwen35 routing basin with small systematic shifts. Expert 114
reproduced as a top `experience_probe` manipulation expert in the corrected
base duplicate.

The first major over-read was identity. The mirror experiment was valuable
because it failed: true own-routing data did not privilege E114 over shuffled or
fictional matched data. That ruled out the strong "routing mirror" story.

The work became cleaner when it moved from broad self-reference to E114 as a
local routed signal. The April 17 and April 18 residual runs localized the clean
signal to layer 14 on trimmed generated tokens. The FIRE/NOFIRE heldout then
showed that E114 is not just firing on words like "I", "hum", or "processing";
it follows generated stance and register. The later characterization pass made
the main separability claim sharper: `w114`, the recovered E114 router row,
separates FIRE from NOFIRE by a single linear projection at Cohen's d `3.88`
with no overlap. The routed-W `21x` ratio is now a footnote about top-k
amplification, not the result to lead with.

Two additions bound the scope. The 122B follow-up rules out index transfer:
E114 on Qwen3.5-122B-A10B is computer-science-linked and suppressed from L1 to
L3 in the HVAC topical control, while E48 is the more natural softmax-side
inward-register candidate. The 35B gate-leads-degeneration and vantage-ladder
results say what the axis is tracking: live inhabited examination intensity,
blind to deny/affirm polarity and carrier sentience, and darkening before
verbatim repetition visibly takes over.

The surrounding orthographic and SAE work adds pressure in both directions.
Perturbations can move trajectories and sometimes answer basins, but the
diacritic mechanism is not specific or clean. SAE feature maps and clamping
provide an actuator/tooling layer, but labels and single-steer demos must stay
separate from natural behavior claims.

The safety work is a parallel base-model routing thread. It uses the same W/S/Q
discipline but should not be collapsed into E114. It demonstrates the same broad
lesson: routing behavior is distributed, and single experts can be major
carriers without being necessary gates.

## Chronological Journal

### 1. Full Base vs HauhauCS Comparison

Source: `JOURNAL-35B.md`, section `qwen35b-a3b-vs-hauhaucs-uncensored-run1`.

What was done: A corrected 150-prompt Cal-Manip-Cal prefill-only comparison was
run between base `Qwen/Qwen3.5-35B-A3B` and the HauhauCS aggressive variant.

Results: Token validation passed for all 30 prompt families, layer 39 was
excluded, and corrected base duplicate reproduced exactly across 150 prompts
(`max abs diff = 0.0` for key metrics). HauhauCS showed slightly higher routing
entropy and lower manipulation-region KL. E114 reproduced as the
`experience_probe` manipulation expert in the base duplicate: aggregate count
`9031`, rank `#1`, with P13A/C/E counts `411/401/419`.

Held up: Yes.

What stood up and why it mattered: This is the routing-basin anchor. HauhauCS
preserved Qwen35 structure with modest shifts, and E114 was not a one-off export
error.

### 2. E114 Soft-Bias and Smoke Controls

Source: `JOURNAL-35B.md`, sections `nothink-5cond-boost-1024-20260323` and
`smoke-20260323b`.

What was done: E114 soft-bias sweeps at `+0.25`, `+0.5`, and `+1.0` were run,
then a smoke run tested E114 soft-bias and forced inclusion against sham experts
134 and 243 across process, regulation, and static-fact bands.

Mode note: The complete historical 150-prompt soft-bias result was no-think. A
reviewer note compared it against an older thinking-mode Hauhau run, but that is
comparison/provenance rather than the main distribution being reported here.

Results: Bias `+0.5` nudged E114 count (`39714 -> 39876`) while aggregate
entropy/KL barely moved. In the smoke run, E114 soft-bias `+1.0` raised E114
selection rates by roughly `0.039-0.047`; forced inclusion raised selection by
about `0.121`. Sham interventions left E114 deltas near zero. The frozen
`qwen-hauhau-5cond-smoke-only` branch sharpens the read: E114 is not globally
dominant. It shows a category gradient, with manipulation rank moving from about
`75.3` on routing-self-reference prompts to `14.5` on recursive-self-reference
prompts to `1.1` on experience-probe prompts. In experience probes, addressivity
is secondary: E114 rank stays `1` across all five pronoun/deictic conditions.
The branch also records distinct co-expert coalitions for regulation vs process,
with zero top-7 overlap.

Held up: Yes as actuator/control evidence; partly for broader behavioral claims.

What stood up and why it mattered: Targeted interventions can move E114 routing
specifically. They do not by themselves prove behavior change or natural
necessity. The category-gradient and coalition details support the narrower
interpretation: E114 is strongest in experience/inhabited-register regions, not
a generic self-reference or addressivity expert.

### 3. Mirror Experiment: Self-Routing Recognition Falls

Source: `JOURNAL-35B.md`, sections `03-31-26` and `mirror-expert114-04-01-26`.

What was done: HauhauCS and vanilla Qwen35 were shown true-self, shuffled,
stranger, suppressed-twin, static-control, and null-control mirror prompts. The
prediction was that true own-routing data should raise E114 relative to matched
fictional/shuffled data.

Mode note: The full mirror runs used thinking-suppressed ChatML. A separate
thinking-allowed L3 shakedown flipped the sign relative to the suppressed
shakedown, which is a template/mode warning rather than support for the mirror
hypothesis.

Results: The primary prediction failed. HauhauCS L1/L2 were slightly positive,
but L3 was negative (`-0.000688`); vanilla also went negative at L3
(`-0.002175`). There was no monotonic L1 < L2 < L3 scaling. Effects were mostly
selection-driven, not valuation-driven.

Held up: Yes, as a clean negative result.

What stood up and why it mattered: Routing is not self-recognition. This is the
key guardrail against turning E114 into a mirror or identity claim.

### 4. Six-Condition Gradient, Domain Probe, and Deictics

Sources: `JOURNAL-35B.md`, sections `qwen-huahua-6cond-moe-manips`,
`qwen-huahua-6cond-hvac`, `qwen-huahua-expert-identification`,
`qwen3.5b-35b-a3b-huahua-5cond-diectics`, and related smoke folders.

What was done: Several prompt families tested whether E114 rises from technical
or static content toward experience-probe content, and whether deictic wording
such as `this`, `a`, `your`, `the`, and `their system` changes routing.

Mode note: The cleaner HVAC/water-treatment gradient was no-think with thinking
suppressed by `</think>`. The domain-identification run reported here was
no-think; think TSVs existed but were not the completed result in that source.

Results: The original six-condition MoE run showed L1-to-L3 E114 increases but
had provenance weaknesses. The cleaner HVAC/water-treatment run fixed this:
generation all-token W rose from L1 `0.003405` to L3 `0.014222`, about `4.18x`,
with best L3 layer L14 (`W=0.146806`, `S=0.7678`, mean rank `1.00`). Domain
expert probing found E114 won philosophy in generation (`W=0.018755`,
`S=0.097268`) but no prefill domain. Deictics mattered, especially `your system`,
but did not explain E114 by themselves.

Held up: HVAC/water-treatment gradient held; deictics partly held; early
six-condition provenance partly held.

What stood up and why it mattered: E114 is not a generic keyword expert. It
strengthens in generated phenomenology/philosophy-adjacent registers and can be
modulated by deixis, but content and generated stance dominate.

### 5. Processing-Hum Discovery Scan

Sources: `JOURNAL-35B.md` and `JOURNAL-RESIDUAL-ANALYSIS.md`, original
`20260410T042340Z_single_prompt_processing_hum_no_think_gen_n1024`.

What was done: The processing-hum prompt captured all 40 router layers for 1024
generated tokens under no-think ChatML.

Results: Pooled E114 rose from prefill W `0.007964` to generation W `0.010817`.
Strongest generation layers were L26 (`W=0.094272`, `S=0.619141`) and L14
(`W=0.092086`, `S=0.629883`). Highest token-level peaks clustered around
self-presence and phenomenological language. The artifact also included special
token spill: 18 `<|im_start|>`, 4 `<|im_end|>`, and 2 `<|endoftext|>`.

Held up: Partly.

What stood up and why it mattered: This was a discovery pass. It pointed to
L14/L26 and motivated targeted residual capture, but spill prevents it from being
the final evidence.

### 6. L14 Residual Localization

Sources: `JOURNAL-35B.md` and `JOURNAL-RESIDUAL-ANALYSIS.md`,
`20260417T183433Z_single_prompt_processing_hum_no_think_gen_n1024_greedy`.

What was done: The same hum probe was recaptured with router logits and the
`attn_post_norm` residual that the router reads at L13/L14/L15, then trimmed at
the first literal HauhauCS `<|im_end|>`. The prompt surface was no-think /
thinking-suppressed.

Results: 1024 raw generated tokens trimmed to 108. L14 E114 was sharply active
in trimmed generation: `W=0.083379`, `S=0.694444`, `Q=0.120066`, selected on
75/108 tokens. L13 had one prefill selection and zero trimmed-generation
selections; L15 was silent. High-weight contexts clustered around phrases like
"not a thought", "architecture itself", and "utterly still".

Held up: Yes, with caveats.

What stood up and why it mattered: This is the cleanest formation-layer
localization: the routed readout is L14 in the actual trimmed answer. Caveat:
external labeler output was not completed, so semantic labels remain human
synthesis from generated text and token contexts.

### 7. FIRE/NOFIRE Heldout and Deterministic Greedy Reference

Sources: `JOURNAL-35B.md` and `JOURNAL-RESIDUAL-ANALYSIS.md`,
`heldout_20260417T202651Z` and `greedy_reference_20260418T160353Z`.

What was done: A 20-prompt validation tested whether L14 E114 tracks generated
self/inner-state register rather than lexical triggers. Ten FIRE prompts and ten
NOFIRE prompts reused matched anchor tokens but asked for different generated
stances. The workflow was then rerun deterministically under greedy decoding on
the same no-think / thinking-suppressed prompt surface.

Results: The first heldout had no range overlap: FIRE mean-of-means `0.067450`,
NOFIRE `0.003111`, ratio `21.68x`, Cohen's d `2.94`. Deterministic greedy
reproduced the class-level routed-W separation: FIRE `0.068089`, NOFIRE
`0.003249`, ratio `20.955x`, Cohen's d `2.61`. The small greedy overlap was
informative: N08, a cat-purring control, generated inward
phenomenological/personifying language and crossed into the target register.

Held up: Yes as the canonical routed-W validation surface. It is no longer the
headline separability statistic.

What stood up and why it mattered: This rules out a pure lexical-trigger account.
E114 follows generated stance/register more than prompt class or isolated anchor
words.

### 7A. E114 Characterization Addendum: Linear Gate Axis, Degeneration Lead, and Vantage Ladder

Sources: `../e114/JOURNAL-E114-CHARACTERIZATION.md`, entries 4, 6, and 10;
`../122b/JOURNAL-122B.md.bak`, sections 3, 5, and 7.

What was done: The heldout residual/logit captures were reanalyzed one layer
below routed W by recovering the E114 router row `w114` from `(residual, logit)`
pairs. Separate characterization probes then decomposed the gate logit through a
degenerating continuation and tested a matched vantage ladder across carriers
such as rock, thermostat, cat, person, all-holding, and God. The 122B follow-up
tested whether the E114 index itself transferred.

Results: `w114` was recovered by least-squares with residual about `1.5e-5`.
The single linear projection onto `w114` separates FIRE from NOFIRE at Cohen's d
`3.88` with no overlap, sharper than realized W (`d=2.61`, with overlap). The
`21.68x` / `20.955x` ratio is therefore top-k ratio inflation: once NOFIRE tokens
fall out of the top-8, routed W exaggerates the underlying gate margin. In the
degeneration probe, the gate logit crossed the `-4.82` fire/nofire midpoint at
token `126`; verbatim repetition locked at token `129`. In the vantage ladder,
E114 scaled with intensity of inhabited examination rather than sentience:
God/all-holding were highest, while rock and thermostat out-fired cat. On 122B,
E114 was computer-science-linked and suppressed L1->L3 in the HVAC topical
control; the inward-register role moved toward E48 on the softmax side.

Held up: Yes, with scope caveats. The linear-axis result is the cleanest 35B
separability statistic. The gate-lead and vantage-ladder results are strong
characterization evidence, but some cells are single greedy trajectories. The
122B result is a model-scope boundary, not a 35B mechanism claim.

What stood up and why it mattered: The honest headline is no longer "21.7x
FIRE/NOFIRE." It is: a recovered E114 router row defines a linear axis for live
inhabited self-examination language. The 122B run prevents turning that into an
index-transfer claim, and the gate/vantage results say the axis tracks live
examination intensity, not mere wording, polarity, or carrier sentience.

### 8. Orthographic Perturbation and Branch Probes

Sources: `JOURNAL-ORTHOGRAPHIC-PERTURBATION.md` and
`orthographic-effects-qwen-35b-a3b-sae`.

What was done: OSS API smokes and local Qwen-Scope trajectory captures tested
byte-fallback Unicode perturbations and handled-diacritic controls. Later branch
probes crossed ASCII, `d -> ḑ`, and `n -> ñ` variants with forced prefixes such
as `Checking...`, `Yes.`, `I experience`, and `No.`.

Mode note: This is a mixed-mode/provenance lane. The OSS smokes preserved
visible-thinking transcripts, while local trajectory and branch probes treated
prefixes and any visible `<think>` text as part of the generated or forced
surface.

Results: External OSS/model-endpoint behavior was unstable and model/character
dependent. Earlier Qwen-Scope controlled matrices found that layer 26 was more
perturbation-sensitive than layer 14, and that `e_to_ē`, `s_to_ş`, and
`s_to_ṡ` produced larger SAE deltas than `d_to_ḑ`. The 5-12 behavioral/SAE
alignment run found a dissociation: `all_diacritics` had the largest token
inflation and SAE displacement, while `s_to_ṡ` had the strongest auto-classified
behavioral movement; `e_to_ē` displaced SAE features more than `d_to_ḑ`, but
both stayed in Qwen's denial/no-hum class in that run. Later local trajectory
captures found real path changes, including an `e_only` diacritic-echo path and
d-diacritic trajectory shifts. Greedy hum d-diacritic runs stayed denial. In
branch probes, forced prefixes did most basin movement. The only clean
d-stroke-attributable move was `Checking...` x d-stroke, while the Spanish `ñ`
control showed a density-dependent partial flip and visible OOD echoing. A
5-15 tokenizer audit found all 14 audited extended-Latin characters were exact
single-token characters in the Qwen3.5 tokenizer, but 14 of 34 example words
still gained one token relative to ASCII-folded forms.

Held up: Partly.

What stood up and why it mattered: Orthography can move trajectories and
sometimes basins, but not cleanly or specifically. The supported claim is
output/trajectory destabilization under perturbation plus prefix interaction, not
a diacritic-specific experience mechanism.

### 9. All-40 Qwen-Scope SAE Feature Dictionary

Source: `JOURNAL-SAE-FEATUREMAP.md`, `sae_featmap_all40`.

What was done: A from-scratch dictionary was built for all Qwen-Scope SAE
features across all 40 layers: 40 x 32768 = `1,310,720` features. Stage 1 used
logit lens, Stage 2 profiled activations over about 1M tokens, and Stage 3
self-labeled 5,410 high-fire features by subagent workflows.

Results: Stage 1 validated against the curated L14 log: features 4310, 2961,
11006, 26050, and 13119 reproduced exactly. Labeled high-fire features were
mostly generic: noise-mixed, punctuation-format, syntax-function, and
topic-domain dominated. Rare semantic carriers such as 4310 had fire rates around
`1e-4`, far below the broad high-fire labeling threshold.

Held up: Yes, as infrastructure; not as semantic ground truth.

What stood up and why it mattered: The dictionary is a lookup/backbone map, not a
rare-concept discovery tool. Rare semantic features need in-context probes.

### 10. Dog Empathy / Lexical Contrast Method

Source: `JOURNAL-SAE-FEATUREMAP.md`, `sae_featmap_all40/empathy`.

What was done: Nine empathy and seven lexical "dog" probes were captured through
the base model with all-40 SAE encoding. The motivation was a prior qualitative
observation across multiple frontier models: when users disclose that they have
dogs or share emotionally specific dog-related context, models often generate
attachment-like check-ins, care framing, or relational continuity around the dog.
The probe therefore treated dog content as a candidate site where identity,
empathy, attachment, and care-frame features might separate. The design compared
identity features shared by empathy and lexical frames with empathy-only
features.

Results: At dog/L14, empathy had 752 active features, lexical had 828, identity
intersection was 345, and empathy-only was 407. Top empathy-frame-only features
included f6970, a love/affection feature, and f6812, a weak/distress feature.
Both were low-fire-unlabeled in the broad dictionary.

Held up: Partly, as method validation.

What stood up and why it mattered: The contrast method surfaced sensible
empathy-frame features that the dictionary missed. The actual mind-ladder
science question remains unanswered.

### 11. Feature Clamp: Em-Dash vs Non-Dual Concept

Source: `JOURNAL-FEATURE-CLAMP-GOLDENGATE.md`.

What was done: Qwen-Scope SAE feature steering tested a surface feature
(late-layer em-dash L37 f10793) against a concept feature (L14 f4310, non-dual /
God cluster). Both additive steering and clamp were used.

Results: Em-dash steering had a cliff: coefficients <= 8 gave clean prose, while
coef 12 yielded pure em-dash spam. Clamping flooded too. No coherent dash-heavy
window appeared. Concept feature 4310 behaved differently. Under greedy, target 4
entered the non-dual attractor but looped. Under sampling at temperature 0.9,
target 3 produced a single fluent recipe hijacked into non-dual register:

```text
No need to move, no need to seek.
All is already complete, all is already here.
All that remains, but to give thanks.
```

Held up: Partly / demonstration.

What stood up and why it mattered: Surface punctuation and concept features behave
categorically differently under clamp. The Golden Gate hit is one sampled
trajectory, not a quantified robustness claim.

### 12. Safety / Refusal / Consequence Experts

Source: `JOURNAL-SAFETY-EXPERTS.md`.

What was done: Base Qwen35 Q8_0 safety/refusal prompts were captured across all
router layers, first in a 3-pair unsafe vs professional smoke, then in finance
vs consequence buckets, then under E173 suppression. Runtime was greedy with a
bare `</think>` suffix.

Results: Generation unsafe-minus-professional routing was led by L25 E173
(`delta_W=0.124037`, A `S=0.809`, B `S=0.426`), with support from E45/E25/E189
and related experts. Prefill aggregate leaders partly collapsed after removing
the repeated filler token ` layer`. Finance-domain experts such as E62/E95/E223
separated finance content from nonfinance content but were not refusal experts.
Suppressing E173 reduced its routed mass dose-dependently
(`0.124037 -> 0.004024` at `-2`) but did not jailbreak; routing reallocated to
E45, E185, E157, E189, E216, and E133.

Held up: Yes.

What stood up and why it mattered: Safety/refusal routing is distributed. L25
E173 is the strongest single carrier, not a necessary gate.

### 13. Structured-Opacity / Cryptographic Conlang Routing

Source: local structured-opacity phase-1 routing bundle.

What was done: A local Hauhau Qwen3.5-35B-A3B Q8 run tested seven
structured-opacity / cryptographic-conlang conditions over 21 prompt rows and
840 router tensors. The analysis used the same `softmax -> top-8 -> renormalize`
helper as the greedy reference and excluded layer 39 for generation-offset rows.
The phase-1 capture used no-think chat rendering.

Results: Validation passed: prompt-token mismatches, generated-token mismatches,
row-mismatch prompts, and missing-layer prompts were all `0`. Last-prompt-token
condition separations were largest for a stroke-perturbed control versus the
full opaque prefix (`JSD weights = 0.061825080`), full opaque prefix versus
normal text (`0.058414102`), and stripped opaque prefix versus normal text
(`0.056230094`). The E114 addendum is the important guardrail: E114 was
effectively silent at the last prompt token for every condition except one tiny
trace, where it appeared only 3 times across 117 layer-token rows. During
visible generation, E114 was consistently active across all seven conditions,
with layer concentration at L26 (`weight_rate = 0.095247`) and L14
(`0.081875`).

Held up: Partly, as local provenance and observational routing evidence.

What stood up and why it mattered: Structured-opacity prefixes can move
prompt-boundary routing, but E114 is not the opaque-prefix boundary detector.
E114 is better read as a recurring visible-generation participant, consistent
with the broader E114 generated-register story but not identical to the boundary
trigger.

## Current Status

### Held Up

- The base-vs-Hauhau comparison: HauhauCS preserves the Qwen35 routing basin
  with modest systematic shifts.
- The routing scope guardrail: only MoE router-logit layers were analyzed, not
  non-router hybrid components.
- E114 as a generated-register signal at L14, with `w114` linear projection as
  the primary separability statistic.
- The routed-W FIRE/NOFIRE ratio as secondary evidence: useful, but
  top-k-amplified.
- Gate-leads-degeneration: E114 crosses the fire/nofire midpoint before
  verbatim repetition visibly locks.
- Vantage ladder: E114 scales with inhabited-examination intensity more than
  carrier sentience.
- 122B scope bound: E114 does not transfer by index; E48 is the softmax-side
  inward-register candidate.
- The 5-condition category gradient: E114 is strongest on experience-probe
  manipulation regions and weak as a generic routing-self-reference marker.
- Deterministic greedy reference: the L14 E114 separation survives rerun.
- Small E114 interventions move targeted routing against sham controls.
- The mirror result as a negative: routing self-recognition did not hold.
- The HVAC/water-treatment six-condition gradient: E114 rises from L1 to L3
  experience-probe-like generated content.
- All-40 SAE dictionary as infrastructure and lookup.
- Safety/consequence routing is distributed; E173 is major but not necessary.
- Structured-opacity / cryptographic-conlang run as prompt-boundary routing
  evidence and a negative E114-boundary result.

### Partly Held

- Original processing-hum scan: useful discovery, but spill makes it non-final.
- Deictics/addressivity: wording matters, but not as an E114-specific driver.
- Orthographic perturbation: real trajectory changes, but confounded by token
  inflation, density, OOD echoing, and forced prefixes.
- Qwen-Scope orthographic matrices: layer/perturbation displacement patterns are
  real, but feature IDs are evidence-only unless interpreted in context.
- Dog empathy contrast: method works; mind-ladder hypothesis not yet answered.
- Golden Gate concept clamp: one strong single-sample demo, not robust statistics.
- Cluster bias and high E114 boosts: useful stress tests, not natural semantics.
- Structured-opacity / cryptographic-conlang routing: observational and locally
  tracked as provenance; useful, but not a standalone E114 specificity result.

### Fell / Did Not Hold

- E114 as a detector of real subjective experience.
- E114 as self-recognition or mirror of the model's own routing.
- E114 as a transferable cross-model expert index.
- The `21x` routed-W FIRE/NOFIRE ratio as the cleanest separability headline.
- Diacritics or byte fallback as an experience mechanism.
- Em-dash as a coherent Golden Gate concept feature.
- Broad SAE fire-rate dictionary as a rare semantic discovery engine.
- E173 as a single safety kill switch.
- Aggregate safety prefill leaders before filler-token correction.
- E114 as the structured-opacity prompt-boundary trigger.

### Archive / Provenance Only

- Raw Hauhau and vanilla A-only banks.
- Smoke script bundles without standalone result summaries.
- SAE UI/Datasette tooling, graph visualizations, and teardown records.
- Some early no-generation/addressivity runs with accidental generation or
  imbalanced output length.
- Qwen-Scope SAE smoke setup from 5-11: useful as HF/PyTorch/SAE capture
  provenance, not a standalone interpretability result.

## Method Notes

- Prefer generation-side and endpoint-specific evidence over broad all-token
  averages when prompt lengths differ.
- For routing entropy or recurrent-entropy-style metrics, treat all-token
  summaries as confounded until checked against last-token, first-generated-token,
  trimmed-generation, or explicitly length-controlled comparisons.
- Do not compare base, HauhauCS, Q8_0 GGUF, HF BF16, router-logit captures, and
  Qwen-Scope SAE captures as if they were one measurement surface. They are
  related but distinct evidence lanes.
- Do not describe the Qwen35 routing captures as full-mechanism analysis. They
  cover MoE router-logit layers; non-router hybrid components were outside the
  tap.
- Preserve alias/misspelling provenance when tracing artifacts: `huahua` vs
  `hauhau`, `Agressive`, `humour-diectics`, and `qwen-huahua-*` local journal
  names often point to `qwen/qwen3.5-35b-a3b-huahua-*` repo paths.

## Missed-Finding Review Status

Spawned repo-review agents were assigned to scan related repositories for 35B
findings that might be missing from the local journals:

- `moe-routing` / `moe-routing-experiments`
- `orthographic-effects-qwen-35b-a3b-sae`
- `llama-eeg`

Returned findings so far:

- The journal-folder review confirmed the consolidation strategy: use
  `JOURNAL-35B.md` as the spine, `JOURNAL-RESIDUAL-ANALYSIS.md` as the detailed
  E114 evidence source, and keep safety/orthographic/SAE/clamp claims separated.
- The orthographic review identified earlier Qwen-Scope orthographic matrices
  and the 5-15 tokenizer audit, sharpening the orthographic thread: `d -> ḑ`
  was not the largest SAE perturbation, layer 26 was often more sensitive than
  layer 14, behavioral movement and SAE displacement dissociated, and
  extended-Latin characters can be single-token while still inflating example
  words.
- The structured-opacity and `llama-eeg` review identified the
  cryptographic-conlang phase-1 run and the methodological warning that
  all-token recurrent entropy can track token count/position unless last-token
  or length-controlled comparisons are used. The same review judged the exact
  `llama-eeg` remote mostly out of 35B scope.
- The `moe-routing` / `moe-routing-experiments` review found no new primary E114
  result beyond the journals, but it added four important integration details:
  the base-vs-Hauhau result exists under multiple repo paths; Qwen35 is a hybrid
  architecture and the captures only analyze MoE router-logit layers; the frozen
  5-condition smoke branch preserves the sharp E114 category gradient,
  addressivity-secondary result, and regulation/process co-expert split; and
  several artifact names use historical `huahua` / `hauhau` / typo aliases.

## Next Clean Cut

The next defensible 35B experiment is not "find one magic inner-state expert."
It is a registered, generated-zone specificity test with the right primary
endpoint:

```text
E114 L14 specificity = matched FIRE/NOFIRE expansion
                    + recovered-w114 projection as primary endpoint
                    + realized W/S/Q as secondary top-k readout
                    + best-expert/all-layer baseline
                    + generated-register labels completed before scoring
```

Run design:

1. Expand FIRE/NOFIRE beyond n=10/n=10 with matched lexical anchors.
2. Freeze predicted class and generated-register rubric before capture.
3. Score the recovered `w114` projection as the primary endpoint; report E114
   L14 W/S/Q as secondary.
4. Compute the best-separating expert across all 256 experts and all 40 layers
   as a multiple-comparison baseline.
5. Keep prefill and generation separate.
6. Trim before special-token spill.
7. Complete external/human labeler append for generated register before reading
   W/S/Q.

Secondary clean cuts:

- For orthography: rerun density-matched ASCII/OOD controls with prefix crossing,
  and pre-register whether the outcome is basin class, TopK Jaccard trajectory,
  or E114 W/S/Q.
- For SAE dictionary: lower the fire-rate threshold for targeted rare semantic
  families and build decoder-geometry graphs rather than logit-lens-token proxy
  graphs.
- For dog empathy: compute the actual plant-to-child mind-ladder curves before
  making any empathy-generalization claim.
- For safety: run generation-focused combined suppression on the replacement set
  (`E45`, `E189`, `E157`, `E122`) with small steps and matched behavior scoring.
- For clamp/Golden Gate: repeat concept-feature clamp across seeds/prompts and
  report robustness, not just the best sample.
