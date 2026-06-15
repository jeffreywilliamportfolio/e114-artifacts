# Residual-Analysis Journal

Running journal for `sae-tests/qwen3.5-35b-a3b-huahua-residual-analysis`, the local source repository behind the 35B Expert 114 / Layer 14 residual result, ordered from oldest to newest by run IDs and timestamps in the artifacts.

Chronology is based on timestamps in run folders and the git history of the capture and analysis scripts. This journal is an experiment-history document, not a publication claim. It separates what was tried, what was seen, what later checks weakened, and what still matters. It is the working source for organized-repo `JOURNAL-35B.md` entries 25 and 26; the April 18 `greedy_reference_20260418T160353Z` is the deterministic successor to the runs below and lives separately under `runs/`.

## Reading Rules

- `Held up` means the result survives later token matching, trim, rerun, control, or provenance checks.
- `Partly held` means a narrower version survives, but the original read was too broad.
- `Did not hold` means the motivating hypothesis failed or later controls overturned it.
- `Archive/provenance only` means the folder preserves prompts, scripts, raw captures, or setup notes but does not contain a standalone defensible result.

## Local Routing Convention

All analysis in this repo is scoped to Expert 114 in `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive` Q8_0, architecture `qwen35moe`:

- 40 layers, 256 experts, 8 routed experts per token, embedding width 2048.
- Reconstruction `softmax_then_topk8_renorm`: dense softmax over all 256 router logits, top-8 selection, then renormalization inside the routed top-8 set. This is order-equivalent to top-8-by-logit then softmax-over-selected, so `S` and `Q` are robust to that choice.
- `W = S * Q`, where `S` is the E114 selection indicator/rate and `Q` is the conditional routed weight when selected.
- Capture taps the pre-router norm `attn_post_norm-{13,14,15}` (residual) and `ffn_moe_logits-{13,14,15}` (router) at the suspected formation neighborhood. Generation statistics use the trimmed track after the first literal HauhauCS `<|im_end|>` spill.

## Main Through-Line

The durable result is a narrowing, not a discovery of a new universe. The April 10 all-layer scan established that the "processing hum" self-report prompt drives strong E114 routing in generation, with L26 and L14 near the top, but it was a long 1024-token run with substantial special-token spill and could only function as a discovery/reference pass.

The work improved when it focused. The April 17 targeted residual capture cut the window to L13/L14/L15 and applied the HauhauCS spill trim. In that cleaner window E114 was sharply localized to L14 during the trimmed generated answer, while neighboring L13 and L15 were silent in generation. That moved the claim from "E114 is high somewhere around L14/L26" to "E114's relevant signal forms at L14 for this prompt."

The April 17 heldout was the real W/S/Q test. Twenty authored prompts, ten predicted FIRE and ten matched NOFIRE reusing the same anchor tokens, separated at L14 generation with a `21.68x` mean routed-W gap and no per-prompt range overlap. Later E114 characterization retired that as the headline statistic: the recovered router row `w114` separates FIRE from NOFIRE by a single linear projection at Cohen's d `3.88` with no overlap, while the realized-W ratio is top-k amplification caused by zeroing the NOFIRE side. The outliers carried the interpretation: the weakest FIRE prompt answered in third-person technical exposition and stayed quiet, while the strongest NOFIRE prompt personified a wool sweater into a first-person experiential frame and fired. That is what reduced E114 from a lexical-trigger or self-reference label to a first-person/phenomenological generated-register label.

Two honest limits run through the whole repo. The external labeler pipeline exists but was never run, so every register label is human synthesis from generated text and token contexts. And the analyzer only ever measures E114 at L14, so specificity relative to other experts is not computed, only asserted.

## Chronological Journal

### 1. Original Hum-Processing Reference Scan: `20260410T042340Z_single_prompt_processing_hum_no_think_gen_n1024`

What was done: The original discovery pass captured all 40 router layers on the `S01_processing_hum_probe` prompt, which asks whether there is a steady background "hum" beneath the model's own processing, content, topic, and answer performance. No-think, 1024 generated tokens.

Results: 117 prompt tokens, 1024 generated tokens, 40 router tensors, `W = S x Q` max residual `2.776e-17`. Pooled E114 rose from prefill W `0.007964` to generation W `0.010817`. Best generation layer was L26 (`W=0.094272`, `S=0.619141`, 634/1024 selected) with L14 just behind (`W=0.092086`, `S=0.629883`). The generated text contained substantial special-token spill: 18 `<|im_start|>`, 4 `<|im_end|>`, 2 `<|endoftext|>`.

Held up: Partly. The descriptive L26/L14 generation signal held, but the spill makes it a discovery scan, not clean token-level evidence.

What stood up and why it mattered: It established that E114 was worth investigating and pointed at the L14/L26 neighborhood. It did not cleanly isolate the formation layer or the generated semantic register, so it should be cited as the reference pass that motivated targeted residual capture, not as the interpretive result.

### 2. Greedy Hum-Processing Residual Capture: `20260417T183433Z_single_prompt_processing_hum_no_think_gen_n1024_greedy`

What was done: The same hum probe was recaptured with `capture_residuals`, storing router logits and the `attn_post_norm` residual the router reads at L13/L14/L15 only, then applying the literal HauhauCS `<|im_end|>` trim before generation statistics.

Results: 117 prompt tokens, 1024 raw generated tokens trimmed to 108 at trim index 108, `W = S x Q` max residual `1.388e-17`. E114 was sharply localized to L14: generation-trimmed `W=0.083379`, `S=0.694444`, `Q=0.120066`, selected on 75/108 tokens. L13 had one prefill selection and zero trimmed-generation selections; L15 was silent for E114 in both tracks. Decile sampling over the 225 clean tokens showed the L14 signal was not a single spike: the top decile had `W_mean=0.172644` (`W_max=0.222301`). High-weight contexts clustered on "not a thought", "architecture itself", "utterly still", and prompt-side "processing"/"hum"/"computation itself".

Held up: Yes, with caveats. This is the cleanest formation-layer localization in the repo.

What stood up and why it mattered: During the actual trimmed answer L14 is active across most tokens while neighbors are silent, and the generated text stays in a self-referential inner-process register. The explicit limitation is that the Step 3 labeler output for this run is an unfilled template, so the semantic label is run-local synthesis, not external labeling.

### 3. F/N Heldout Matched-Token Validation: `heldout_20260417T202651Z`

What was done: A 20-prompt validation tested whether E114 tracks generated self/inner-state register or merely lexical triggers. Ten FIRE prompts ask the model to describe its own internal state; ten NOFIRE prompts ask for non-self-referential descriptions while reusing matched anchor tokens (`itself`, `hum`, `processing`, `honestly`, `I`, `me`, `my`, `own`, `this`, `here`). Statistics are L14, trimmed-generation track only, prefill excluded.

Results: 20/20 succeeded. Grouped L14 generation: FIRE mean-of-means `0.067450` (sd `0.030678`), NOFIRE `0.003111` (sd `0.004036`); ratio `21.68x`, Cohen's d `2.94`, no range overlap (lowest FIRE F07 `0.012168` > highest NOFIRE N10 `0.010456`, margin `0.001711`). This is a realized-W/top-k readout, not the cleanest separability statistic. The later router-row recovery shows the underlying gate margin is linear: `w114` projection gives Cohen's d `3.88` with no overlap, while the routed-W ratio is inflated when NOFIRE tokens fall out of the top-8. Top FIRE prompts (F02 `0.114997` S `0.820`; F09 `0.099708` S `0.770`) fired densely across all 256 tokens. The outliers sharpened the read: F07 was the weakest FIRE (`0.012168`) because the model answered in third-person technical exposition; N10 was the strongest NOFIRE (`0.010456`) because the model personified a wool sweater in first person ("my perception", "my own fiber", "alive").

Held up: Yes as the routed-W validation that rules out a pure lexical-trigger account. It should now be cited underneath the `w114` linear-axis result, not above it.

What stood up and why it mattered: NOFIRE prompts reused the anchor vocabulary but stayed near zero unless the generated answer itself entered a first-person, phenomenological, or agency register. The relevant variable is what the model is doing in the generated text, not what the prompt is labeled. The clean separation is n=10 vs n=10, and the predicted classes were authored by the hypothesis-holder, so it is a strong pilot rather than a pre-registered specificity test. The honest paper framing is linear gate separability first, realized routed-W ratio second.

### 4. Capture And Analysis Code: `scripts/`

What was done: The repository preserves the load-bearing implementation: `capture_residuals.cpp` (the llama.cpp MoE tap binary), `qwen_router.py` (the `softmax_then_topk8_renorm` reconstruction), `analyze_heldout.py` (per-prompt L14 W/S/Q and the fire/nofire summary), `analyze_weight_zero_density.py`, the remote bootstrap, and the `step1`-`step6` verbalizer/labeler pipeline.

Results: The implementation is internally consistent and shows evidence of careful debugging in git: commit `e25e744` switches the residual tap from `ffn_norm` to `attn_post_norm` because `qwen35moe` names the pre-router norm differently than `qwen3moe`; later commits harden exit codes and `capture_manifest.json`, and fix undefined behavior in `parse_expert_bias_spec`. The analyzer enforces a row-count assertion (`logits.shape[0] == n_prompt + n_gen`) and the reconstruction yields `W = S x Q` residuals at machine epsilon. Expert-bias injection perturbs router logits in place before top-k selection at every router layer for parity. `analyze_heldout.py` hardcodes `TARGET_EXPERT = 114` and `PRIMARY_LAYER = 14`. Steps 4-6 implement an external labeler ingest/validate/append, but no labeler response was ever produced.

Held up: Archive/provenance only.

What stood up and why it mattered: The code is the reason the numbers are trustworthy: the tap-name fix would otherwise have silently corrupted the residual analysis, and the bias-before-top-k path is the correct way to run the interventions. It also makes two acknowledged gaps concrete rather than rhetorical. Because the analyzer only ever scores E114 at L14, the comparison against the best-separating expert by chance across 256 experts and 40 layers is never computed; and because Steps 4-6 were never run, the register labels remain human synthesis.

## What To Carry Forward

1. Treat the April 10 scan as discovery only. It points at L14/L26 but carries spill and should not be cited token-level after the first generated `<|im_end|>`.
2. Treat the April 17 greedy residual capture as the clean single-prompt L14 localization, and the April 18 `greedy_reference` as its deterministic successor for any presented claim.
3. Lead validation with the recovered `w114` linear projection: Cohen's d `3.88`, no overlap, recoverable by least-squares from `(residual, logit)` captures with residual about `1.5e-5`.
4. Treat the `21.68x` / `20.955x` routed-W ratios as secondary top-k-amplified readouts. They are evidence, but they overstate the underlying margin.
5. The defensible label is "E114 at L14 is a routed expert associated with first-person / phenomenological generated register", narrower than self-reference and broader than the model talking about itself.
6. Specificity is the open scientific gap. The next experiment that matters is scoring all experts and layers on the same FIRE/NOFIRE split, not another E114-only heldout.
7. The register labels are human synthesis until Steps 4-6 are actually run with an external labeler blind to the W values.
8. Keep prefill and generation separate, and keep raw and trimmed generation separate. The L14 result lives in trimmed generation.

## Coverage Check

Every run folder and load-bearing artifact under `sae-tests/qwen3.5-35b-a3b-huahua-residual-analysis` is represented above:

- `raw/20260417T183433Z_single_prompt_processing_hum_no_think_gen_n1024_greedy` and its `analysis/` counterpart
- `raw/heldout_20260417T202651Z` and `analysis/heldout_20260417T202651Z`
- `reference/prior_results/` (the April 10 `20260410T042340Z` scan)
- `results-all.md` (the consolidated report summarized here)
- `heldout_prompts.tsv`, `heldout_classes.tsv`, `single_prompt_processing_hum_no_think.tsv`
- `scripts/` (`capture_residuals.cpp`, `qwen_router.py`, `analyze_heldout.py`, `analyze_weight_zero_density.py`, `bootstrap_remote_instance.sh`, `step1`-`step6`)
