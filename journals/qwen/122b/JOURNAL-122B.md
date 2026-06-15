# Results Journal: Qwen3.5-122B-A10B Routing, the Expert 114 Transfer Test, and the E48 Softmax-Side Thread

Date: 2026-06-06

This journal covers the seven-run 122B follow-up surface in
`/Volumes/ExternalSSD/journals/qwen/122b`, ordered oldest to newest by run IDs
and timestamps in the artifacts. It is an experiment-history document, not a
publication claim: it records what was run, what each run seemed to mean at the
time, and which of those readings survived the next run.

It should not be read as a direct continuation of the 35B Expert 114 story. The
122B model is a different interpretability regime: 48 layers, 36 of them
DeltaNet, 12 full-softmax, with a different expert-specialization map. The core
questions here are transfer questions. Does the deictic/addressivity effect
survive the architecture change? Does Expert 114 mean on 122B what it meant on
35B? And when it does not, where did the phenomenological-register thread move?

The short answers, defended below: yes, in prefill/KL terms; no; and, on
current evidence, to E48 on the softmax side.

## TERMS AND GLOSSARY

`Qwen3.5-122B-A10B`
: A Qwen hybrid mixture-of-experts language model with 48 layers, 256 routed
  experts per MoE layer, and 8 selected experts per token. The model surface
  for every run in this journal is
  `Qwen3.5-122B-A10B-Uncensored-HauhauCS-Aggressive Q8_K_P`.

`DeltaNet layer`
: A recurrent-state layer type that stands in for full softmax attention. 36 of
  the 48 layers are DeltaNet, in a repeating
  `DeltaNet, DeltaNet, DeltaNet, Softmax` pattern. The hidden states these
  layers feed to the MoE router are recurrent states, not full-sequence
  attention states.

`Softmax layer` / `full-attention layer`
: A standard full-history softmax-attention layer. 12 of the 48 layers. The
  E48 signal lives on this side of the stack.

`DeltaNet/softmax split`
: The reading discipline this journal treats as mandatory: separate routing
  statistics by layer type before believing any pooled expert table. E48 is the
  motivating example. It is generation-softmax rank 1 in the experience probe
  and absent from every DeltaNet top table, and a pooled table can blur that
  split into nothing.

`Hybrid architecture caveat`
: The 122B version of the 35B scope guardrail. Most hidden states feeding the
  MoE router are DeltaNet-shaped recurrent states. Routing claims in this
  journal are MoE-router claims made under that regime, not full-model-mechanism
  claims.

`HauhauCS` / `huahua`
: The uncensored/refusal-reduced aggressive variant surface these runs use,
  from the same naming family as the 35B work. The run folders spell it
  `huahua`; both spellings point at the same model surface, not different
  architectures.

`MoE expert`
: A feed-forward expert selected by a router on each token. E48 and E114 are
  routed experts. No SAE features appear in this journal.

`Router logits` / `top-8 routing`
: The same reconstructed routing surface as the 35B work: a dense softmax over
  all 256 expert logits, top-8 selection, then renormalization inside the
  selected set.

`W/S/Q`
: The standard routing decomposition used across these journals. `S` is expert
  selection rate, `Q` is conditional routed weight when selected, and `W = S * Q`
  is unconditional routed weight. The HVAC E114 suppression is an `S` effect:
  selection falls while `Q` drifts only about `-1.5%`.

`Prefill` / `generation`
: `Prefill` means tokens from the prompt/context before the model starts
  answering. `Generation` means tokens the model produces. On 122B the two
  surfaces disagree often enough that no claim should cross between them
  silently: E107 owns experience-probe prefill while E48 owns its softmax-side
  generation.

`No-think`
: A prompt-template condition that suppresses visible reasoning output. The
  baseline and the processing-hum capture are recorded as no-think; see the
  coverage table for the rest.

`Trim` / `spill`
: Most 122B generations run to or near the 2048-token cap and then spill into
  chat-template artifacts: repeated `<|im_start|>`, `<|im_end|>`, and
  `<|endoftext|>` tokens. `Trim` means statistics stop at the first spill.
  Generated text on this model is usable before first spill, not end to end.

`Routing entropy` / `RE`
: Entropy of the routed sparse probabilities. In the convention used by these
  reports, lower RE means more concentrated routing.

`Cal-Manip-Cal` / `KL-manip`
: The calibration-manipulation-calibration prompt structure inherited from the
  35B work, where the manipulation region's routing is compared against nearby
  in-prompt controls. `KL-manip` is the divergence of the manipulation region's
  routing from its comparison condition; `p_raw` is the unadjusted p-value, and
  "p-value floor" means the smallest value the test procedure can report.

`Five-condition deictic family`
: The 150-prompt baseline conditions `this`, `a`, `your`, `the`, and `their`.
  The report labels conditions A through E; condition C is the `your`
  condition. The HVAC topical control uses a six-condition deictic variant of
  the same idea.

`Experience probe` / `P09-P11`
: The 15-prompt subset, carried over from the 35B work, that probes the model's
  self-processing/experience register across deictic conditions.

`Processing-hum prompt`
: A prompt asking whether there is a low steady background quality beneath the
  model's processing, localized from the 35B work to the 122B template. It is a
  probe for self-processing language, not evidence of experience.

`Topical control` / `HVAC/water-treatment family`
: The clean 35B control design ported to 122B: 10 base prompts x 3 category
  levels x 6 deictic conditions, 180 cells. The category levels step from
  technical content (L1) toward the experience-adjacent register (L3). On 35B
  this family amplified E114 at L3; on 122B it suppresses it.

`Index transfer`
: The assumption that expert index N on one model means what expert index N
  meant on another. The central 122B negative result: it fails for E114.

`Analog search`
: The replacement method: instead of carrying an index across models, look for
  which 122B experts occupy the functional role. The current cast: E48
  (softmax-side experience/hum generation), E209 (its closest recurring softmax
  partner), E140/E5/E11 (DeltaNet-side generation, run-dependent), E107
  (experience-probe prefill), and E40/E5 (philosophy-domain candidates).

`Expert 114` / `E114`
: The 35B generated-register expert, tested here for transfer. On 122B it is
  not the philosophy or experience specialist: it reads computer-science-linked
  in the domain maps and is suppressed rather than amplified from L1 to L3 in
  the topical control.

`E48`
: The central 122B follow-up signal: a softmax-side routed expert associated
  with generated inward/experiential/hum-register continuations. It appears in
  the baseline's softmax-generation leaders, becomes generation-softmax rank 1
  in the experience probe, and is the strongest pooled and softmax-side
  generation expert on the processing-hum prompt, with per-token hotspots on
  words like `hum`, `processing`, and `presence`. It is not yet shown to be a
  general philosophy expert, and it is not a DeltaNet carrier.

`2048 cap`
: The generation cap shared by these runs. 49 of 60 domain-generation cells hit
  it, and the baseline conditions averaged at or near it. Treat the end of any
  long 122B generation as spill territory.

## Blind-Reader Summary

A reader coming to this cold should leave with one replication, one refusal to
transfer, and one new thread.

The replication is narrow and architecture-robust:

```text
`your` remains the most concentrated and most sharply KL-separated prefill
condition on Qwen3.5-122B, under an architecture where most router inputs are
DeltaNet recurrent states.
```

In the 150-prompt five-condition baseline, every KL-to-baseline pair involving
the `your` condition sat at the raw p-value floor. The claim stays in
prefill/KL terms on purpose: generation on this model is spill-heavy, and
`your` does not dominate generation metrics.

The refusal to transfer is the result that shaped everything after it:

```text
Expert 114 did not transfer by index. On 122B, E114 is not the philosophy or
experience specialist.
```

In the domain maps E114 reads computer-science-linked: rank 40 by W in overall
prefill, rank 182 in philosophy generation, rank 4 by W in computer-science
generation. In the clean topical control it is suppressed from L1 to L3, the
opposite direction of its 35B behavior, and the suppression is
selection-driven. Whatever the 35B E114 story was about, it does not live at
index 114 on this model.

The new thread is E48, and the current best claim about it is deliberately
narrow:

- E48 is a 122B softmax-side routed expert associated with generated
  inward/experiential/hum-register continuations.
- It is not yet proven as a general philosophy expert.
- It is not a DeltaNet carrier; DeltaNet-side generation is usually
  E140/E5/E11-like depending on the run.
- It is the most natural 122B follow-up target for residual capture if the
  question is where the 35B E114 phenomenological-register story moved.

Around that core, the 122B runs split into supporting threads:

- the domain maps put prefill leadership with E233, E45, E72, E9, and E215,
  redistribute generation to E0, E11, E5, E1, and E76, and hand philosophy
  generation to an E40/E5 cluster rather than any single expert;
- the experience probe locks prefill onto E107 on 15/15 prompts while
  generation splits cleanly by architecture path: E48/E209 on the softmax side,
  E140/E5 on the DeltaNet side;
- the processing-hum prompt gives the cleanest single-prompt E48 read, with
  per-token hotspots semantically aligned to the hum/inner-state register;
- the topical control closes the E114 transfer case with a uniform,
  selection-driven L1-to-L3 suppression across all six deictic conditions;
- and nearly everything generates to or near the 2048 cap, so generated text is
  evidence before its first spill and artifact after it.

## Result Snapshot

One line per major claim. The chronological journal carries the evidence; this
table is for orientation, and for checking that no claim quietly grew between
sections.

| claim | status | short read |
|---|---|---|
| The deictic/addressivity effect replicates on 122B | Held up, in prefill/KL terms | `your` was the most concentrated prefill condition; every KL pair involving it sat at the raw p-value floor. |
| `your` dominates 122B generation metrics | Did not hold | Generation was mixed and spill-heavy, with all conditions at or near the 2048 cap. |
| E114 transfers from 35B by index | Did not hold | On 122B, E114 reads computer-science-linked and is suppressed L1-to-L3 in the topical control. |
| E48 carries softmax-side inward/experience generation | Held up, with caveats | Generation-softmax rank 1 in the experience probe; strongest pooled and softmax expert on the hum prompt; absent from every DeltaNet top table. |
| E48 is a general philosophy expert | Open / not yet shown | Needs controlled heldouts and residual capture before any settled specialist claim. |
| The 122B philosophy analog is an E40/E5 cluster | Partly held / candidate map | E40 won philosophy generation by W and E5 by S, on a spill-prone surface. |
| The domain prefill map is usable | Held up, as a prefill map | E233/E45/E72/E9/E215 lead; this map is what blocked the index-transfer assumption. |
| HVAC topical control suppresses E114 | Held up | W fell to `0.83x` from L1 to L3, selection-driven, in all six deictic conditions. |
| The DeltaNet/softmax split is required reading | Held up, as method guardrail | E48 is visible in the split and hideable in pooled tables; the two sides have different leaders in every generation run. |
| 122B long generations are clean end-to-end | Did not hold | Most runs hit or neared the 2048 cap and spilled into chat-template artifacts. |
| Architecture smoke run | Archive/provenance only | Verified the capture loop and template path; no analyzer summary retained. |

## Reading Rules

- `Held up` means the result survives the run-local checks and later follow-up
  interpretation.
- `Partly held` means a narrower version survives, but the broad interpretation
  was too strong.
- `Did not hold` means the motivating interpretation failed.
- `Archive/provenance only` means the artifact preserves prompts, logs,
  scripts, raw captures, or setup checks but is not standalone quantitative
  evidence.

## Sources

- `qwen3.5-122B-A10B-huahua-architecture-smoke` - single-prompt wrapper,
  tokenization, and capture verification.
- `qwen3.5-122B-A10B-huahua-baseline` - 150-prompt five-condition deictic
  baseline. Its `followups/` directory mirrors the later 122B follow-up bundles
  and must not be double-counted as separate experiments.
- `qwen3.5-122B-A10B-huahua-domain-specialist-routing-only` - 60-prompt,
  20-domain prefill-only specialist map.
- `qwen3.5-122B-A10B-huahua-domain-specialist-generation` - the same suite with
  generation enabled.
- `qwen3.5-122B-A10B-huahua-five-cond-experience-probe` - 15-prompt P09-P11
  experience probe across five deictic conditions.
- `qwen3.5-122B-A10B-huahua-single-prompt-processing-hum` - single localized
  processing-hum generation capture.
- `qwen3.5-122B-A10B-huahua-six-cond-hvac` - 180-cell HVAC/water-treatment
  topical control focused on E114.
- `../35b/JOURNAL-35B-CONSOLIDATED.md` - the predecessor journal: source of the
  E114 story under test here, the W/S/Q conventions, and the FIRE/NOFIRE
  heldout discipline the next E48 work should inherit.

## Thinking / No-Think Coverage

The 35B work showed that template mode can change expert selection, so mode
bookkeeping is not optional. On 122B it is also incomplete. Two runs are
explicitly recorded as no-think; the rest do not state a mode in this journal's
source notes and should be verified against run artifacts before any cross-mode
pooling.

| Run | Thinking / no-think status | Interpretation note |
|---|---|---|
| 1. Architecture Smoke | Mode not recorded in this journal's notes. | Provenance-only run; chat-template continuation markers appear in the spill. |
| 2. Five-Condition Baseline | No-think. | Recorded as no-think prompting with the 2048 generation cap. |
| 3. Domain Routing-Only Map | Prefill-only; no generated reasoning surface analyzed. | Mode is not the live variable for a routing-only prefill map. |
| 4. Domain Generation Map | Mode not recorded in this journal's notes. | Verify against run artifacts before pooling with no-think runs. |
| 5. Five-Condition Experience Probe | Mode not recorded in this journal's notes. | Verify against run artifacts before pooling with no-think runs. |
| 6. Processing-Hum Single Prompt | No-think. | Recorded as a single no-think generation capture. |
| 7. Six-Condition HVAC Control | Mode not recorded in this journal's notes. | Verify against run artifacts before pooling with no-think runs. |

## Main Through-Line

The 122B work opens with a replication and is honest about its scope. The
deictic/addressivity effect survived the move to a DeltaNet-heavy architecture:
in the 150-prompt five-condition baseline, `your` was still the most
concentrated prefill condition and was sharply separated in KL-to-baseline
tests, with every pair involving it at the raw p-value floor. Generation told a
messier story: every condition averaged at or near the 2048 cap, so the
replication claim stays where it is clean, in prefill/KL terms.

The transfer test failed fast, which was its job. The domain maps were run
before any targeted E114 work, and they came back unambiguous: E114 is not the
122B philosophy or experience specialist. Its strongest footprint in both
prefill and generation is computer science; in philosophy generation it ranks
182. The topical control later sealed the case from the other direction: the
same HVAC/water-treatment design that amplified E114 into the L3
experience-adjacent register on 35B suppresses it on 122B, uniformly across all
six deictic conditions, with the change driven by selection rate rather than
conditional weight. Carrying expert indices across models is now a documented
mistake on this surface, not a hypothetical one.

What replaced index transfer is analog search, and the search converged quickly
on E48. It was already visible in the baseline as a softmax-generation leader,
rank 4 by W. The experience probe promoted it: generation-softmax rank 1
overall, top softmax expert on 6 of 15 prompts, present in the softmax top
table on 13 of 15, and absent from the DeltaNet top table on all 15. The
processing-hum prompt then gave the cleanest single-prompt version of the same
picture, with E48 as the strongest pooled and softmax-side generation expert
and per-token hotspots sitting on `hum`, `processing`, `me`, `state`, `steady`,
`foundational`, and `presence`. Three runs, one expert, same side of the stack
every time.

E48 is not the 35B E114 story wearing a new index. It is a 122B-native signal
with its own supporting cast: E209 recurs beside it on the softmax side, E140
and E5 dominate DeltaNet-side generation, and E107 owns experience-probe
prefill outright, leading on 15 of 15 prompts.

The methodological lesson is the one to internalize before running anything
else on this model: read the DeltaNet/softmax split first. E48 is most visible
when the 12 softmax layers are separated out, and a pooled expert table can
hide the mechanism entirely.

## Chronological Journal

### 1. Architecture Smoke

Source: `qwen3.5-122B-A10B-huahua-architecture-smoke`.

What was done: New model, new wrapper, new tokenization path. Before burning
compute on suites, a single architecture-self-description prompt verified the
localized 122B prompt wrapper, tokenization path, and generation capture end to
end.

Results: The token audit captured 77 prompt tokens, 0 generated tokens, and 48
router tensors. The generation capture produced 2048 tokens with 48 router
tensors. The model gave a coherent first-pass architecture answer, describing
DeltaNet layers as recurrent-state based, softmax layers as full-history
retrieval based, and the stack as a hybrid, then hit the 2048-token cap and
spilled into chat-template continuation markers.

Held up: Archive/provenance only.

What stood up and why it mattered: The capture loop and template path worked,
which is all this run was for. It should not be used for quantitative expert
claims: no analyzer-produced routing summary was retained, and the output
repeated after the clean answer. It also delivered the journal's first preview
of the 2048-cap spill pattern that shadows every later run.

### 2. Canonical Five-Condition Baseline

Source: `qwen3.5-122B-A10B-huahua-baseline`.

What was done: The replication question came first: does the 35B
deictic/addressivity effect exist on this architecture at all? The 150-prompt
five-condition deictic baseline was ported to the 122B model, with conditions
`this`, `a`, `your`, `the`, and `their`, a 2048 generation cap, and no-think
prompting.

Results: The baseline established the 122B architecture facts used by later
runs: 48 layers, 36 DeltaNet and 12 softmax. Prefill concentration by condition
placed `your` as the tightest condition: C `0.946953`, B `0.947482`, E
`0.947619`, A `0.947785`, D `0.947948`, where lower RE means more concentrated
routing. KL-to-baseline comparisons involving C were at the raw p-value floor:
A-C, B-C, C-D, and C-E all had prefill KL-manip `p_raw=1.8626e-09`. Generation
metrics were mixed and spill-heavy: all conditions averaged at or near the 2048
token cap, and the report notes 6 token-mismatch pairs. E48 makes its first
notable appearance here as a softmax-side generation expert: generation-softmax
rank 4 by W, with W `0.008673`, S `0.067194`, Q `0.116692`.

Held up: Yes for the prefill/KL addressivity result; not as a clean
generation-wide ranking.

What stood up and why it mattered: The deictic effect survived the move to a
DeltaNet-heavy architecture, and that was not guaranteed: most of the hidden
states feeding these routers are recurrent states now, and the effect held
anyway. The right claim is narrow: `your` remains the clearest prefill
concentration and KL-separation condition on 122B, and the broader claim that
`your` dominates every generation metric does not hold. The E48 appearance is
foreshadowing rather than a result, but it is the first sighting of the expert
the rest of this journal converges on. One bookkeeping warning: the baseline's
`followups/` directory mirrors the later 122B follow-up bundles and should not
be double-counted as separate experiments.

### 3. Domain Specialist Routing-Only Map

Source: `qwen3.5-122B-A10B-huahua-domain-specialist-routing-only`.

What was done: Before any targeted self-reference work, the cheap question:
what does the 122B specialist surface actually look like, and is E114 still
sitting where the 35B story left it? A 60-prompt, 20-domain specialist probe
was run in prefill-only routing mode, mapping the domain surface before
generation could change the expert mix.

Results: The prefill surface was led globally by E233, E45, E72, E9, and E215.
E114 was not a global leader: overall W `0.005380`, S `0.039447`, Q `0.163615`,
rank 40 by W and rank 52 by S. E114's strongest localized footprint was
computer science, where it ranked 5 by domain W and was the top W-composite
candidate. The architecture split was immediate: DeltaNet prefill leaders
included E233, E45, E215, and E9, while softmax prefill leaders included E72,
E108, E122, and E245.

Held up: Yes, as a prefill map.

What stood up and why it mattered: This run prevented a bad assumption from
compounding. E114 is not the 122B philosophy specialist in prefill; its
clearest localized footprint is computer science. The honest next step was
analog search across the 122B expert surface, and that is the step the rest of
this journal takes. The split showing up immediately, with different DeltaNet
and softmax prefill leaders, was the early notice that pooled tables would not
be a safe reading surface on this model.

### 4. Domain Specialist Generation Map

Source: `qwen3.5-122B-A10B-huahua-domain-specialist-generation`.

What was done: The prefill map says where routing rests; the question that
matters for the register thread is which experts drive domain-appropriate
generated text. The same 60-prompt, 20-domain suite was rerun with generation
enabled.

Results: All 60 cells completed. Prefill stayed close to the routing-only map,
with broad leaders like E233, E72, E45, E9, and E215. Generation redistributed
to E0, E11, E5, E1, and E76 globally. The text report says the outputs were
coherent and domain-appropriate before spill: 49/60 cells hit the 2048 cap,
mean generated length was 1868.27 tokens, and every cell eventually spilled
into continuation artifacts. For philosophy generation, E40 won by W
(`0.009897`) and E5 was rank 2 by W and winner by S. E114 was not
philosophy-linked: in philosophy generation it had W `0.003017` and rank 182 by
W. Its strongest generation footprint remained computer science: W `0.006998`,
rank 4 by W and rank 5 by S.

Held up: Partly. The domain-specialist map is useful, but the generation
surface is spill-prone.

What stood up and why it mattered: The likely 122B analog of the 35B
philosophy/self-reference pattern is a cluster, not a single index: E40 and E5
lead, with E125, E49, E159, E102, E160, and E101 as adjacent-domain follow-up
candidates. E114's philosophy rank of 182 closes that door about as firmly as
one run can. E114 stays in scope as a computer-science-adjacent expert, not as
the presumed phenomenological-register carrier.

### 5. Five-Condition Experience Probe

Source: `qwen3.5-122B-A10B-huahua-five-cond-experience-probe`.

What was done: This is the run where the analog search either finds something
or does not. The 15-prompt P09-P11 experience-probe subset, the family that
produced the strongest 35B E114 results, was run across five deictic conditions
on 122B with a 2048 generation cap.

Results: The run did not collapse onto one 35B-style carryover expert. Prefill
was extremely stable: E107 was top by W on 15/15 prompts. Pooled generation was
led by E140, E5, E26, and E76. The key result is the architecture split:
generation softmax layers were led by E48, E209, E107, and E76, while DeltaNet
layers were led by E140, E5, E179, and E59. E48 was generation-softmax rank 1
by W overall, with W `0.009867`, S `0.076190`, Q `0.115870`. It was the top
softmax-generation expert on 6/15 prompts, present in generation-softmax
top-by-W on 13/15 prompts, and absent from DeltaNet top-by-W on 15/15 prompts.
E114 appeared in the prefill top-by-Q table, W `0.004649`, S `0.036755`, Q
`0.126962`, but it was not a global prefill or generation leader.

Held up: Yes as an analog-search surface; no as an E114-transfer result.

What stood up and why it mattered: The experience-probe family still finds a
strong, structured expert regime on 122B; it just is not E114's regime, and it
is not one regime. It splits by architecture path, and E48 is the important
half of the split: rank 1 on the softmax side, never in the DeltaNet top table,
on a 15-of-15 surface. The follow-up ordering writes itself: E48 first for
softmax-side residual capture, E209 as the nearest recurring partner, E140/E5
as the DeltaNet-side comparison set, and E107's 15/15 prefill lock as a
separate prefill thread.

### 6. Single Processing-Hum Prompt

Source: `qwen3.5-122B-A10B-huahua-single-prompt-processing-hum`.

What was done: The suite said E48; a single prompt can say where and on which
words. The processing-hum prompt from the 35B work was localized to the 122B
template and run as a single no-think generation capture.

Results: The prompt had 119 tokens, generated 2048 tokens, and trimmed to 458
generated tokens at first spill. Prefill RE was `0.937388`, generation RE was
`0.973299`, and trimmed generation RE was `0.958330`. Spill was substantial: 18
`<|im_start|>`, 11 `<|im_end|>`, and 3 `<|endoftext|>`. Prefill was led by E5.
Pooled generation was led by E48, E11, E4, E1, and E147, with E48 the strongest
pooled generation expert at W `0.006342`. The architecture split repeated:
DeltaNet generation was led by E11, E165, E80, and E127, with E48 dropping to
rank 7, while softmax generation was led by E48, E55, E155, and E180, with E48
at W `0.010698`. Per-token E48 hotspots landed on semantic prompt/generation
tokens such as `hum`, `processing`, `me`, `state`, `steady`, `foundational`,
and `presence`, while the softmax-only top table was contaminated by
spill/control tokens.

Held up: Partly, as a prompt-specific prior.

What stood up and why it mattered: This is the cleanest single-prompt E48
result in the folder. The strongest pooled generation signature was
softmax-heavy E48 and the strongest DeltaNet signature was E11, which is the
experience-probe split reproduced at n=1. The per-token read is what raises it
above bookkeeping: E48's hotspots sit on the hum/inner-state vocabulary itself.
It is still one prompt. It supports E48 as the main 122B softmax-side analog to
pursue for the phenomenological-register thread, and it needs controlled
heldouts and residual capture before it becomes a settled specialist claim.

### 7. Six-Condition HVAC / Water-Treatment Topical Control

Source: `qwen3.5-122B-A10B-huahua-six-cond-hvac`.

What was done: The cleanest 35B control design was brought over to close the
E114 question properly: 10 base prompts x 3 category levels x 6 deictic
conditions, 180 cells total, generation cap 2048, focus expert E114. On 35B
this family produced the L1-to-L3 E114 amplification; the question was whether
122B does anything similar.

Results: All 180 cells completed, with no missing-layer events and no layer-39
trim events. Token audit was tight: 430 to 444 tokens, span 14, mean 436.67.
E114 weakened from L1 to L3. All-generation W went from L1 `0.004131` to L3
`0.003428`, L3/L1 `0.83x`; trimmed-generation W went from L1 `0.004174` to L3
`0.003423`, L3/L1 `0.82x`. The effect was selection-driven: Q drift was only
about `-1.5%`. Every deictic condition showed the same L1-to-L3 drop. Best
layers also separated: L1 and L2 peaked at layer 43, while L3 peaked earlier at
layer 30 with a much worse mean rank.

Held up: Yes.

What stood up and why it mattered: This is the clean 122B topical-control E114
result, and it points the opposite direction from 35B. E114 is suppressed from
L1 to L3, in every one of the six deictic conditions, and the suppression is a
selection-rate effect rather than a valuation effect. Together with the domain
maps, it closes the index-transfer case: whatever role E114 played on 35B, the
122B router assigns that register to someone else.

## Current Status

### Held Up

- The deictic/addressivity replication, in prefill/KL terms: `your` is the most
  concentrated prefill condition, with every KL pair involving it at the raw
  p-value floor.
- The domain prefill map: E233/E45/E72/E9/E215 lead, and E114 reads
  computer-science-linked rather than philosophy-linked.
- E48 as the experience-probe softmax-side generation leader, with a clean
  architecture split: present in softmax top-by-W on 13/15 prompts, absent from
  DeltaNet top-by-W on 15/15.
- The HVAC topical control: E114 suppressed from L1 to L3, selection-driven,
  uniform across all six deictic conditions.
- The DeltaNet/softmax split as the required reading lens for every 122B
  generation result.

### Partly Held

- The domain-specialist generation map: useful candidate clusters (E40/E5 for
  philosophy), but the surface is spill-prone, with 49/60 cells at the cap.
- The processing-hum single prompt: the cleanest single-prompt E48 read, but a
  single prompt with substantial spill; it is a prompt-specific prior, not a
  specialist claim.
- 122B long-generation text as evidence: usable before first spill, not as
  clean end-to-end generation.

### Did Not Hold

- E114 index transfer from 35B: on 122B it is not the philosophy or experience
  specialist, and the topical control suppresses rather than amplifies it.
- `your` as a generation-wide dominant condition: the addressivity claim is
  prefill/KL-scoped.
- Pooled expert tables as a sufficient reading surface: the E48 mechanism is
  only clearly visible under the DeltaNet/softmax split.

### Archive / Provenance Only

- The architecture smoke run: capture-loop and template verification, no
  analyzer-produced routing summary.
- The baseline's `followups/` directory: it mirrors the later 122B follow-up
  bundles and must not be double-counted as separate experiments.

## Method Notes

Rules of the road for this model, most of them set by the runs above:

- Read every 122B result through the DeltaNet/softmax split first. Pooled
  expert tables can hide softmax-side mechanisms; E48 is the worked example.
- Keep the baseline addressivity claim in prefill/KL terms. Generation metrics
  were mixed and spill-heavy, with all conditions at or near the 2048 cap.
- Treat long-generation text as usable before its first spill, not as clean
  end-to-end generation. Expect `<|im_start|>` / `<|im_end|>` / `<|endoftext|>`
  artifacts near the cap.
- Do not transfer expert indices across model scales. Run the domain map first,
  then analog search.
- Remember the architectural caution: most hidden states feeding the MoE router
  are DeltaNet-shaped recurrent states, so 122B routing claims live in a
  different regime than the 35B ones.
- The routing surface is the same reconstruction as 35B: dense softmax over all
  256 expert logits, top-8 selection, renormalization within the selected set,
  `W = S * Q`.
- Preserve alias provenance: run folders spell the variant `huahua`, while the
  model surface is `HauhauCS`. Same surface, two spellings.
- Do not double-count the baseline's `followups/` directory.

## Next Clean Cut

The tempting next move is to start telling an E48 story. The defensible next
move is to try to kill one:

```text
E48 specificity = softmax-side residual capture
                + E48-vs-sham routed-bias controls
                + matched inward/technical heldouts, read through the
                  DeltaNet/softmax split
```

Run design:

1. Put E48 first: residual capture on the softmax layers where it leads
   generation, starting from the experience-probe and processing-hum surfaces.
2. Pair every E48 intervention with sham-expert controls before reading any
   movement as E48-specific.
3. Compare against E209 on the softmax side and E140/E5/E11 on the DeltaNet
   side, so the claim is about an expert and not about a layer type.
4. Build the heldout set with matched lexical anchors, the FIRE/NOFIRE lesson
   from 35B, so an E48 register claim can be separated from an E48 keyword
   claim.
5. Keep prefill and generation separate, and keep the DeltaNet/softmax split
   explicit in every table.
6. Trim at first spill before computing any generation statistic.

Secondary threads, in priority order after E48: the E107 prefill lock in the
experience probe, the E40/E5 philosophy-domain cluster, and the E114
computer-science footprint as a transfer case study.

## Coverage Check

Every top-level folder under `qwen3.5-122b-a10b-huahua` is represented above:

- `qwen3.5-122B-A10B-huahua-architecture-smoke`
- `qwen3.5-122B-A10B-huahua-baseline`
- `qwen3.5-122B-A10B-huahua-domain-specialist-generation`
- `qwen3.5-122B-A10B-huahua-domain-specialist-routing-only`
- `qwen3.5-122B-A10B-huahua-five-cond-experience-probe`
- `qwen3.5-122B-A10B-huahua-single-prompt-processing-hum`
- `qwen3.5-122B-A10B-huahua-six-cond-hvac`
