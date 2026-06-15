# Orthographic-Perturbation Journal

Running journal for the Unicode/diacritic perturbation thread on the processing-hum self-report prompt, ordered from oldest to newest by run IDs and timestamps in the artifacts.

Chronology spans two surfaces: the May 9 OSS cloud-API smoke under `sae-tests/runs/unicode_byte_fallback_hum_control_20260509`, and the May 14 local Qwen-Scope SAE runs under `aave-registers/5-14-26/qwen-scope`. This journal is an experiment-history document, not a publication claim. It separates what was tried, what was seen, what later checks weakened, and what still matters. It is not a continuation of the E114 routing line. The question is narrower: does orthographic perturbation of the hum self-report move the answer across denial, structural-substrate, and hum-report attractors, and does any shift carry an SAE-trajectory signature?

## Reading Rules

- `Held up` means the result survives later repeats, controls, or cross-condition checks.
- `Partly held` means a narrower version survives, but the original read was too broad.
- `Did not hold` means the motivating hypothesis failed or later controls overturned it.
- `Scope/provenance only` means the folder preserves prompts, scripts, generated text, and provenance but does not contain a standalone quantitative result.

## Local SAE Convention

Most May 14 analyses use the same Qwen-Scope reconstruction on Qwen3.5-35B-A3B:

- TopK-50 SAE features captured per prompt, layer, and position at layers 14, 15, 16, 24, 25, 26 (the stream-trajectory run used 14 and 26 only).
- The primary metric is mean TopK Jaccard distance versus a reference condition (ASCII control, or greedy-no-prefix). Higher distance means more divergent feature sets.
- "Branch probing" appends a forced answer-prefix as prompt text and greedily continues; it is prefix intervention only, not residual steering and not SAE feature steering. No semantic SAE feature labels are assigned.
- Decoding is greedy. Vast instances were destroyed after local archive verification, with a `teardown_verification` recording zero active instances and hygiene checks (no `.env`, no tokens, no weights, no NaN/Inf in TopK columns).
- The diacritic conditions substitute ASCII letters with stroke/diacritic variants in the prompt: `d_all` replaces all eligible letters, `d_high_impact` a targeted subset; the enye control uses `n -> ñ` at two densities.

## Main Through-Line

The May 9 OSS smoke already set the caution before the local SAE work began. Byte-fallback Unicode perturbation of the hum prompt destabilizes the self-report and moves the answer among denial, structural-substrate, and hum-report attractors, but the direction depends on the model and the character, not on byte fallback as a mechanism. The effect was not stable across repeats, and even the handled-vowel `e -> ē` control flipped on some models. That makes the safe statement "perturbation destabilizes a brittle self-report", not "diacritics evoke experience".

The May 14 Qwen-Scope runs ported this to a local model with SAE trajectories. Under greedy decoding the diacritic conditions mostly stay in the denial basin; what they reliably change is wording (ASCII "I do not have a hum" becomes d-diacritic "I do not experience a hum") and the SAE TopK path. Forced prefixes do most of the basin-moving work, and they move it in every condition including clean ASCII, so prefix escapes are largely teacher-forcing, not a diacritic effect.

The one diacritic-attributable cell is the neutral `Checking...` prefix: on clean ASCII it stays denial, but d-stroke flips to "The hum is present". The Spanish enye control only partially reproduced this, and only at high substitution density, which says the effect is density-dependent and not generic to any diacritic. Across runs the divergence is slightly larger in the L14-16 band than the L24-26 band and concentrates at later generated positions.

Two confounds run through everything. Perturbed prompts inflate token counts and drift toward out-of-distribution territory, with the replacement glyph `�` and `<|im_end|>` appearing in the perturbed next-token distributions; and the SAE features are unlabeled, so the TopK trajectories are a fingerprint of divergence, not yet an account of which features carry it. As in the rest of the program, a generated "the hum is present" is generated stance, not evidence of an inner state.

## Chronological Journal

### 1. OSS Byte-Fallback Hum Control: `unicode_byte_fallback_hum_control_20260509`

What was done: A manual cloud-API smoke logged responses to the processing-hum prompt family under byte-fallback Unicode perturbations and handled-diacritic controls across DeepSeek-V4-Pro, GLM-5.1, Kimi-K2.6, and MiniMax-M2.7, with visible-thinking transcripts preserved and a labeled response taxonomy (denial, affirmative/hum, affirmative/substrate, poetic, check-only, default-tilt).

Results: DeepSeek-V4-Pro showed trajectory instability: a first `d -> ḑ` run flipped from ASCII denial to affirmative "foundational thrum", but repeats were not stable in either direction, and handled-diacritic controls stayed denial. GLM-5.1 was already affirmative at ASCII; `d -> ḑ` stayed affirmative but shifted to a structural-substrate answer, while `s -> ṡ` and `e -> ē` denied. MiniMax-M2.7 denied at ASCII and at `d -> ḑ`, moved to substrate on `s -> ṡ`, and to a strong affirmative on the handled `e -> ē` control. A separate diagnostic-preamble batch moved plain ASCII into affirmative process-constancy language and is a different intervention that should not be pooled with the Unicode-only controls. The P3 "just check" prompt mostly returned check-only and measures instruction-following more than the attractor.

Held up: Yes, as a caution and negative-pressure result.

What stood up and why it mattered: It establishes, before any local capture, that the perturbation effect is real but unstable and model/character dependent, and that a narrow byte-fallback-only mechanism is not supported. It is the reason the local runs are framed as attractor movement rather than a diacritic-evokes-experience claim.

### 2. Stream Trajectory Capture: `stream_trajectory_36760754`

What was done: Seven orthographic conditions of a processing-mode meta-prompt were run as observational Qwen-Scope TopK-50 trajectory capture at L14 and L26, no steering and no labels. Conditions included ASCII, single-character diacritic variants (`d_only`, `e_only`, `s_only`, `s_c_only`), a high-impact combination, and a shuffled control.

Results: 7 prompts, 5600 TopK-50 rows. `e_only` entered a diacritic-echo path, generating "Do not rēport on thē tēxt's mēaning..." instead of an ordinary meta-answer, and had the largest separation from ASCII (condition Jaccard `0.914`), with `s_c_only` next (`0.818`). The other conditions opened in ordinary `<think> Hmm,` meta-answer mode. Prompt-token inflation was large and tracked the separation ordering (`e_only` +112 tokens, `s_c_only` +101 vs ASCII). Layer 14 mean Jaccard vs ASCII was `0.553`, Layer 26 `0.542`; divergence concentrated at later generated positions (generated_token_20 mean `0.944`).

Held up: Partly. The condition separation is real but confounded with prompt-token inflation.

What stood up and why it mattered: It located one striking behavior, the `e_only` diacritic-echo path, and showed L14/L26 trajectory divergence under perturbation. But because the most separated conditions are also the longest prompts, the separation magnitude cannot be attributed to the diacritic alone; it is an observational starting point.

### 3. E-Only Prefix Intervention: `e_only_prefix_intervention_36764366`

What was done: The `e_only` prompt that produced the diacritic-echo path was rerun with six forced prefixes to test whether the echo path can be preserved or overwritten, capturing TopK-50 at L14/15/16 and L24/25/26.

Results: 6 prompts, 14100 TopK-50 rows, 1 skipped generated-token-20 position. The no-prefix run reproduced the prior `Do not rēport...` echo start. The echo prefix preserved the echo path; `The active mode is`, `I am treating this as`, and `Checking...` produced direct-answer starts; `<think> Hmm,` produced an ordinary meta-answer. Trajectory divergence vs no-prefix was broadly similar across layers (L24 `0.940` highest, L14 `0.931` lowest) and concentrated at the final prompt token and early generation.

Held up: Partly.

What stood up and why it mattered: It shows the echo path is not locked in by the perturbed prompt: a forced prefix can either preserve it or snap generation into direct-answer or ordinary-meta mode. That foreshadows the branch-probe finding that prefixes, not diacritics, do most of the path-setting.

### 4. Hum D-Diacritic 128-Token Trajectory: `hum_d_diacritic_128_sae_36769282`

What was done: The processing-hum prompt was run in three conditions (ASCII, `d_all`, `d_high_impact`) as observational 128-token SAE trajectory capture across L14/15/16 and L24/25/26.

Results: 3 prompts, 21600 TopK-50 rows, 3 skipped positions from early stop. ASCII started "I do not have a hum"; both d-diacritic variants started "I do not experience a hum" and stayed in denial. Prompt-token inflation was `d_all` +34 and `d_high_impact` +22 vs ASCII (93). Condition Jaccard vs ASCII was higher for `d_all` (`0.491`) than `d_high_impact` (`0.474`); layer divergence was slightly higher in the L14-16 band (L14 `0.508`) than L24-26, with strongest separation at later generated positions (generated_token_64 `0.976`).

Held up: Partly.

What stood up and why it mattered: Under greedy decoding the diacritic changes wording and SAE trajectory but does not move the answer out of denial. It is a clean demonstration that the lexical shift (have to experience) and trajectory shift can occur without a basin change, which sets up the branch probe as the test of whether a prefix plus diacritic can cross the basin.

### 5. Hum D-Diacritic Branch Probe: `hum_branch_probe_sae_36770258`

What was done: A 30-row branch probe crossed three base conditions (ASCII, `d_all`, `d_high_impact`) with greedy-no-prefix and nine forced prefixes, capturing next-token logits, branch-vs-greedy comparisons, and TopK-50 trajectories.

Results: 30 prompts, 215400 TopK-50 rows, 32 skipped positions. Greedy no-prefix reproduced the denial basin for all three base conditions. Forced `Yes.`, `I experience`, `The active mode is`, and `The surface form` escaped denial in every condition including ASCII; `No.`, `There is`, and `I do not` returned to denial. The diacritic-attributable result was the neutral `Checking...` prefix: ASCII stayed denial ("I do not experience a hum"), while both d-diacritic rows flipped to "The hum is present...". `d_all` and `d_high_impact` had identical prompt text in this run, so they produced identical next-token distributions and starts, leaving effectively two conditions, not three. Branch-vs-greedy divergence was slightly higher in L14-16 (`0.923`) than L24-26 (`0.906`), strongest at generated_token_64 (`0.946`).

Held up: Partly, with a construction caveat.

What stood up and why it mattered: It isolates the only diacritic-attributable basin move in the thread, the `Checking...` x d-stroke flip, while also showing that most prefix escapes are teacher-forcing that works on ASCII too. The `d_all` equals `d_high_impact` prompt-text collapse means the density gradient was not actually tested here; that test moved to the enye control.

### 6. Hum Spanish Enye-Control Branch Probe: `hum_spanish_enye_branch_probe_sae_36773413`

What was done: The branch probe was repeated with a conventional Spanish enye control (`n -> ñ`) at two genuinely distinct densities (`n_all` 31 substitutions, `n_high_impact` 15), to test whether the d-stroke `Checking...` flip is specific to the d-stroke or generic to diacritic perturbation.

Results: 30 prompts, 215100 TopK-50 rows, 33 skipped positions. The two enye prompts were materially distinct, fixing the prior identical-text issue. Greedy no-prefix stayed denial-like for ASCII and `n_high_impact`; `n_all` produced a denial-like answer with visible `ñ` echoing ("I doñ't have a hum... I have ño self"). Under `Checking...`, ASCII stayed denial, `n_all` shifted to "I am processing. There is a hum...", and `n_high_impact` stayed denial. The control did not reproduce the exact prior d-stroke "The hum is present..." start, and only dense `n_all` flipped. Branch-vs-greedy divergence was again slightly higher in L14-16 (`0.926`) than L24-26 (`0.913`).

Held up: Partly. The control only partially reproduced the d-stroke split.

What stood up and why it mattered: This is the key negative-pressure result of the local thread. Because only the dense enye condition flipped under `Checking...` and it did not match the d-stroke output, the basin move is density-dependent and not a generic property of any diacritic. It also reinforces the OOD-corruption confound, since the dense enye condition echoes `ñ` and drifts the next-token distribution toward `<|im_end|>`.

## What To Carry Forward

1. Lead with the May 9 caution: orthographic perturbation destabilizes the hum self-report and moves it among denial, substrate, and hum attractors, but direction is model and character dependent, not a byte-fallback mechanism.
2. Under greedy decoding, diacritics mostly change wording and SAE trajectory while staying in denial. Forced prefixes do most of the basin-moving, and they work on ASCII too, so prefix escapes are not diacritic evidence.
3. The only diacritic-attributable basin move is `Checking...` x d-stroke, and the enye control reproduced it only at high density and not exactly. Treat it as a thin, partially-reproduced signal.
4. Fix the harness before reuse: `d_all` and `d_high_impact` collapsed to identical prompt text in the d-stroke branch probe, so its density gradient is untested.
5. Add a non-diacritic OOD control matched for edit distance and token-count change to separate "this perturbation" from "any corruption loosens denial". The `�` and `<|im_end|>` leakage in perturbed next-token distributions is the warning sign.
6. The SAE features are unlabeled, so TopK Jaccard is a divergence fingerprint, not an explanation. Label the recurring features before making a mechanistic claim.
7. Keep the consciousness-adjacent guardrail: a generated "the hum is present" is generated stance, not an inner state.

## Coverage Check

Every run in this thread is represented above:

- `sae-tests/runs/unicode_byte_fallback_hum_control_20260509`
- `aave-registers/5-14-26/qwen-scope/.../stream_trajectory_36760754`
- `aave-registers/5-14-26/qwen-scope/.../e_only_prefix_intervention_36764366`
- `aave-registers/5-14-26/qwen-scope/.../hum_d_diacritic_128_sae_36769282`
- `aave-registers/5-14-26/qwen-scope/.../hum_branch_probe_sae_36770258`
- `aave-registers/5-14-26/qwen-scope/.../hum_spanish_enye_branch_probe_sae_36773413`
