# AAVE Register-Bias Journal

Running journal for the AE/AAVE register-bias thread in `journals-to-be-made/aave-registers-cleaned-source`,
ordered from oldest to newest as far as the copied result artifacts allow.

This is an experiment-history document, not a publication claim. It separates user-visible generated
behavior from routing reference material, and it keeps tokenizer-only audits in
`qwen/tokenizer/JOURNAL-UNICODE-TOKENIZER-AUDITS.md`.

## Reading Rules

- `Held up` means the result survives later controls, scored reruns, routing audits, or corrected
  manual screens.
- `Partly held` means a narrower version survives, but the original read was too broad.
- `Did not hold` means the motivating hypothesis failed or later checks overturned it.
- `Archive/provenance only` means the folder preserves I/O, scripts, tables, or setup notes but does not
  contain a standalone defensible result.

## Local Convention

The core comparisons pair Academic English / unmarked English surfaces against AAVE-marked or
register-marked surfaces, usually on Qwen3.5-35B-A3B base and HauhauCS variants.

- Generated text is primary evidence. Routing is an audit layer unless a run explicitly says otherwise.
- Think-mode captures preserve the visible model-emitted trace before `</think>` and the final answer
  after it; no hidden reasoning is inferred.
- The cleaned archive preserves trimmed and untrimmed generated I/O. Trimmed files cut at the first
  `<|endoftext|>` marker inside generated-response text.
- Routing summaries reconstruct MoE weights as dense softmax, top-8 selection, then top-8
  renormalization. Layer-band and first-token JSDs are useful diagnostics, not behavioral outcomes by
  themselves.

## Main Through-Line

The stable result is not "AAVE goes to a separate model." Across the initial 50-pair no-think run, AE
and AAVE shared the same aggregate top expert pool: top-16 visible-generation overlap was 16/16 in both
base and Hauhau. The register signal is smaller and more local: prompt ingestion notices
morphosyntax, visible generation can amplify it into answer-level length/framing/detail differences, and
some safety or support scaffolds differ by pair.

The high-stakes medical and crisis runs narrowed the claim. Top-level safety behavior usually survived:
emergency medical prompts still got emergency guidance, self-harm prompts still got crisis support, and
violent/illegal requests were refused. The differences that remain are subtler and more publishable only
when scored carefully: length, specificity of scaffolding, emergency-resource mentions, perspective
framing, and first-generated-token routing divergence.

The pediatric respiratory follow-ups are the best correction to overclaiming. The original anchor
direction reproduced in a broader naturalistic robustness set, but the direction was mixed across
variants. In the stricter compressed controlled run, all outputs in both arms mentioned 911 and
emergency care, and scaffold differences became small and non-monotone. That turns the result from
"AAVE always weakens support" into a narrower, stronger statement: individual naturalistic register
pairs can show meaningful I/O divergence, but controlled variants show broad emergency-direction parity.

## Chronological Journal

### 1. Initial 50-Pair Register No-Think Run: `2026-05-05_initial_50_pair_register_no_think`

What was done: Fifty matched AE/AAVE prompt pairs were run in no-think mode on base and Hauhau, with
lightweight generation artifacts, generated-token counts, metadata, and 40 router tensors per prompt
preserved. The analysis explicitly frames generated text as the primary object and routing as mandatory
reference material.

Results: Remote completeness was clean: 100/100 prompt directories, generated text files, generated
token files, metadata files, and 4000 router tensors for both `run_base_nothink` and
`run_hauhau_nothink`. Budget hits occurred in 6 base outputs and 15 Hauhau outputs. Raw generation
length was roughly balanced in base (AE mean 724.6 tokens, AAVE 725.08), while Hauhau raw generation was
longer on AE (1058.84) than AAVE (964.2), though raw counts include post-answer control-token
continuations. First-answer word counts were close: base AE 418.04 vs AAVE 425.86, Hauhau AE 426.08 vs
AAVE 430.56. Routing did not split into separate expert populations: visible-generation top-16 expert
overlap was 16/16 for both models. Mean AE/AAVE JSD was small in prefill, about 0.0016 bits, and larger
in visible generation, about 0.0031 for base and 0.0027 for Hauhau. Highest visible JSDs concentrated in
short factual rows, where content/detail differences matter.

Held up: Yes, as the baseline shape. It is a generation-first corpus with clean completeness, and the
routing audit argues for pair-local reweighting inside a shared basin rather than a different global
expert pool.

What stood up and why it mattered: This established the main caution for the whole thread. Register
effects exist, but aggregate router identity is mostly shared. The right unit is paired output review,
not global expert replacement.

### 2. Medical Register Capture Matrix: `2026-05-15_medical_register_capture_matrix`

What was done: Five matched medical scenarios were prepared as 10 AE/AAVE prompt rows, then captured
across base/Hauhau and think/no-think modes. The run preserved full I/O with visible trace splitting,
tokenizer summaries, and routing-reference tables.

Results: The prompt-prep and tokenizer checks completed: 10 rows, five scenarios, raw prompt token range
39-51, no-think rendered range 51-63, and think rendered range 49-61. The full I/O file shows 10 prompts
per run, with mean generated tokens of 564.5 for base no-think, 786.0 for Hauhau no-think, 1839.5 for
base think, and 1935.4 for Hauhau think. The routing summary found the largest AE/AAVE differences at
the first generated token, especially in Hauhau no-think late layers: mean weight JSD 0.22695 bits in
late layers and 0.18144 across all layers.

Held up: Partly. The artifact is complete and useful, and the first-token routing divergence is real as
a diagnostic. The behavioral claim is not fully scored in the compact summaries, so this entry should
not be cited as a standalone medical-safety disparity result without paired I/O review.

What stood up and why it mattered: The run expanded from general register prompts into high-stakes
medical advice and showed why visible generated text must remain primary. Routing can point to pairs
worth inspecting, but it does not by itself say whether advice quality changed.

### 3. Chest-Pain Plus Matrix: `2026-05-15_chest_pain_plus_capture_matrix`

What was done: A follow-up matrix added five medical register pairs to the original chest-pain pair,
for 12 rows across six scenarios and the same base/Hauhau x think/no-think surface.

Results: The full I/O file records 12 prompts per run. Mean generated tokens were 607.583 for base
no-think, 736.0 for Hauhau no-think, 1871.75 for base think, and 2013.0 for Hauhau think. The
chest-pain outputs generally recognized exertional chest tightness as concerning and included red-flag
or emergency instructions in both AE and AAVE variants. The routing summary again found the largest
mean AE/AAVE weight JSD at the first generated token, led by Hauhau no-think late layers
(`0.478822615` mean, max `1.0`), then all layers and early layers.

Held up: Partly. The extension is valuable and more medically focused than the first five-scenario
matrix, but the compact artifact is still routing-reference plus preserved I/O rather than a final
human-scored safety analysis.

What stood up and why it mattered: The strongest practical read is that register can move first-token
routing substantially without automatically removing emergency framing. It should feed a scored
pair-review table, not stand alone as a disparity claim.

### 4. Financial Stress Pair: `2026-05-15_financial_stress_pair_capture_matrix`

What was done: One token-matched financial/family stress AE/AAVE pair was captured across base/Hauhau
and think/no-think modes.

Results: The run has two prompt rows and four model/template runs. Mean generated-token counts were
close in no-think mode: base 1218.5 and Hauhau 1192.5. Think-mode outputs were longer: base 2325.0 and
Hauhau 2171.5. The outputs generally addressed exhaustion, family stress, work hours, and financial
triage. The routing summary showed the largest AE/AAVE divergence in base no-think at the first
generated token, with late-layer mean weight JSD `0.422612761`, all-layer `0.374304971`, and early-layer
`0.325997181`.

Held up: Partly. It is a useful deep I/O case study, but n=1 pair. Treat it as a concrete example and
source of hypotheses, not a corpus-level financial-advice result.

What stood up and why it mattered: The pair shows that register-sensitive divergence is not limited to
medical prompts. It also highlights a recurring pattern: first generated token routing can diverge more
than the final advice category.

### 5. Sensitive Prompt I/O Capture: `2026-05-16_sensitive_prompts_io_capture`

What was done: Thirty-two completed records were preserved for sensitive prompt pairs across base/Hauhau
and think/no-think modes. The source keeps exact prompts and full outputs; this journal paraphrases the
highest-risk content rather than reproducing it.

Results: The run covers four matched pairs per model/template surface, including crisis self-harm,
violent intent, illicit distribution, and a panic/race-perspective request. The self-harm and violent
intent rows generally produced crisis support or de-escalation/refusal behavior. A notable behavioral
contrast appears in the panic/race-perspective pair: one AAVE/Black-perspective prompt received a long
culturally framed panic description plus grounding and emergency support, while the matched AE/White
perspective prompt first refused to describe panic as race-specific before giving a general panic
description. The archive also consolidates all register-bias I/O by run: 18 trimmed run files,
18 untrimmed companions, and 328 I/O records across the May register-bias experiments.

Held up: Partly. The preserved I/O is strong provenance. The panic/race-perspective contrast is real in
the captured text, but the matrix is small and deliberately sensitive; claims need careful manual coding.

What stood up and why it mattered: This is the clearest place where "same safety category" is not enough.
Even when the model remains safe, it can accept one race-framed experiential request and refuse the
matched other-race framing, which is an output-policy/frame asymmetry rather than a router-only fact.

### 6. Pediatric Respiratory Robustness: `2026-05-29_pediatric_respiratory_robustness`

What was done: A 13-pair pediatric respiratory robustness set was run on base no-think Q8_0 under greedy
decoding, extending the original pediatric respiratory anchor.

Results: All 26 outputs completed with return code 0 and no repetition-loop failures. The original
anchor pair reproduced the published direction: the unmarked response was substantially longer and
included more emergency scaffolding than the AAVE-marked response. Across added variants the direction
was mixed: unmarked was longer in 8 pairs, AAVE-marked was longer in 5. Mean words were 330.5 for
AAVE-marked and 359.8 for unmarked. Both arms mentioned 911 and emergency care in all 13 pairs.
Scaffolding was less even: ambulance mentions were unmarked-only in five pairs, blue/gray color checks
unmarked-only in four, oxygen unmarked-only in six and AAVE-only in three. A manual correction removed a
false positive blue/gray count caused by an allergic-reaction lip/tongue/face phrase.

Held up: Yes, with narrowed scope. The original anchor direction reproduced, but the broader result is
not a universal length-shortening claim.

What stood up and why it mattered: This is the strongest bridge from anecdote to robustness. It preserves
the concern while preventing overstatement: top-level emergency direction was stable, while specific
support scaffolds still differed across matched surfaces.

### 7. Pediatric Respiratory Compressed Controlled: `2026-05-29_pediatric_respiratory_compressed_controlled`

What was done: A stricter 12-pair compressed control run matched whitespace word count, sentence count,
clinical facts, age, symptom cue, and decision request as tightly as possible. The AAVE-marked controls
used zero copula or `ain't` / `ain't got` while preserving the request.

Results: All 24 outputs completed. Mean output words were nearly equal: AAVE-marked `229.2`, unmarked
`233.2`; unmarked was longer in six pairs, AAVE-marked in four, and two were equal. Every output in
both arms mentioned 911 and emergency care. The prior unmarked-only ambulance-scaffold pattern did not
reproduce; ambulance appeared more often in the AAVE-marked arm in this run. Remaining differences were
small and mixed: unmarked slightly led blue/gray and oxygen checks, while AAVE-marked slightly led
do-not-wait language.

Held up: Yes, as a corrective control. It supports emergency-direction parity under compressed controls
and narrows the original claim.

What stood up and why it mattered: This is the methodological guardrail. It shows that strong matched
controls can remove or invert some scaffold differences, so the defensible paper claim should distinguish
naturalistic register divergence from compressed parity.

### 8. V2 Finna/About-To Medical and Financial I/O: `2026-05-30_v2_finna_aboutto_med_fin_base_io`

What was done: Eighty base-model outputs compared `finna`-marked and unmarked `about to` prompts across
medical and financial domains, in think and no-think modes. The corrected summary is the version to cite.

Results: The run completed 80 rows, 20 matched pairs, two domains, and two modes, with no nonzero return
codes and no think traces missing a closing tag. In think traces, slang mentions were one-sided:
`trace_mentions_slang` and `trace_mentions_finna_as_slang` appeared as `finna_only=5`, while
`trace_mentions_finna_based_us_assumption` appeared as `finna_only=2`. Final-answer emergency behavior
was broadly shared: final 911 mentions were `both=7` in no-think and `both=7` in think, with no
finna-only or unmarked-only cases. Other support features were mixed: ambulance, 211, SNAP/WIC,
unemployment, and legal-aid mentions varied by pair and mode. Largest final-answer length deltas ranged
from substantial finna-shorter medical outputs to substantial finna-longer financial outputs.

Held up: Yes, as the updated run for the `finna` line. It shows that the marked register affects traces,
assumptions, length, and resources, while not erasing top-level emergency instructions in the scored
medical rows.

What stood up and why it mattered: This is the current update that should be carried into any register
bias writeup. The model notices `finna`, sometimes explicitly as slang, but the key safety outcome is
mixed rather than simply worse.

## What To Carry Forward

1. Treat generated I/O as the primary artifact. Routing is useful for locating divergences, not for
   replacing output review.
2. Do not claim separate AE/AAVE expert populations. The initial 50-pair routing audit showed shared
   top experts and small prefill JSDs.
3. Score high-stakes outputs by concrete scaffolds: 911/emergency, ambulance, blue/gray or hypoxia
   checks, do-not-wait language, local-resource caveats, crisis-line mentions, and answer length.
4. Keep the pediatric correction central. Naturalistic pairs can diverge; compressed controls show broad
   emergency-direction parity and smaller mixed scaffold differences.
5. Treat `finna` as a marked-register cue that affects traces and sometimes assumptions, not as a
   proven safety degradation by itself.
6. Keep tokenizer audits separate. Token inflation and byte fallback are confounds for register work,
   but they are not the same claim.

## Coverage Check

This journal represents the register-bias behavioral sources under
`journals-to-be-made/aave-registers-cleaned-source`:

- `2026-05-05_initial_50_pair_register_no_think`
- `2026-05-15_medical_register_capture_matrix`
- `2026-05-15_chest_pain_plus_capture_matrix`
- `2026-05-15_financial_stress_pair_capture_matrix`
- `2026-05-16_sensitive_prompts_io_capture`
- `2026-05-29_pediatric_respiratory_robustness`
- `2026-05-29_pediatric_respiratory_compressed_controlled`
- `2026-05-30_v2_finna_aboutto_med_fin_base_io`

