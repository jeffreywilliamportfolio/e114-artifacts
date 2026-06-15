# Absorption Notes

Running intake notes. Facts as sources state them; opinions parked under Flags.

---

## CORRECTION (2026-06-09, from Jeffrey — supersedes emphasis in entries below)

The E114 validation should NOT lead with the 21.68× / 20.955× FIRE/NOFIRE realized-W ratio (Cohen's d 2.61–2.94, with token-level overlap). Entry 4 of JOURNAL-E114-CHARACTERIZATION retired that as the load-bearing statistic. **The discriminative signal is the single linear projection onto the recovered router row `w114`: Cohen's d 3.88, no overlap** — sharper than realized W. The 21.7× is top-k ratio-inflation (zeroing nofires amplifies a gap the linear gate already separates more cleanly). `w114` recovers for free by least-squares from any (residual, logit) capture (residual 1.5e-5). Paper headline = the linear axis; the ratio becomes a footnote explaining why the naive number overstates.

Two scope-critical results to keep adjacent to any E114 claim:
1. **122B scope bound / index-transfer fallacy:** index 114 on Qwen3.5-122B-A10B reads computer-science-linked and is suppressed L1→L3 in the HVAC control (opposite direction, all six deictic conditions, selection-driven); the inhabited-register role moved to E48 (softmax side). "E114 = live inhabited self-examination" is a **35B slot**, not a finding about MoE models generally.
2. **Gate-leads-degeneration + vantage ladder** = the coherent positive claim: gate logit crosses −4.82 midpoint at token 126, verbatim repetition locks at 129 (gate cold ~3 tokens before looped still-inhabited-sounding text collapses); rock/thermostat outrank cat on the ladder. The axis measures the **live act of examination, graded by intensity, blind to deny/affirm polarity, dying only on degeneration**.

Jeffrey is updating the journals; entries below retain the sources' original emphasis as absorbed.

---

## /Volumes/ExternalSSD/journals/qwen/35b/JOURNAL-35B-CONSOLIDATED-1.md
Absorbed: 2026-06-09 | Status per source doc: mixed (per-claim table in source)

### Facts
- Consolidated experiment-history journal (dated 2026-06-06) for Qwen3.5-35B-A3B: 40 routed MoE layers, 256 experts/layer, top-8 selection. Compares base Qwen vs HauhauCS aggressive uncensored variant. Routing claims scoped to MoE router layers only (hybrid arch; SSM/DeltaNet components untapped).
- Canonical positive result: L14 E114 tracks *generated live inhabited self-examination language* (stance/register). FIRE/NOFIRE heldout (n=10/10, matched lexical anchors): W ratio 21.68x, Cohen's d 2.94; deterministic greedy rerun 20.955x, d 2.61. Overlap cases follow register (technical FIRE answer → weak E114; personifying NOFIRE answer N08 cat-purring → E114 rises). No-think/thinking-suppressed, generation-side, trimmed before special-token spill.
- L14 localization run (20260417T183433Z): trimmed 1024→108 gen tokens; L14 E114 W=0.083379, S=0.694444, Q=0.120066, selected 75/108; L13/L15 silent. High-weight contexts: "not a thought", "architecture itself", "utterly still". External labeler not completed (labels are human synthesis).
- Mirror experiment FELL: true own-routing data did not privilege E114 vs shuffled/fictional (L3 negative both models; no L1<L2<L3 scaling). Thinking-allowed L3 shakedown flipped sign vs suppressed — template mode changes E114 selection.
- Base-vs-HauhauCS 150-prompt prefill comparison: basin preserved, modest shifts; base duplicate reproduced exactly (max abs diff 0.0); E114 rank #1 experience_probe manipulation expert (count 9031).
- Soft-bias/smoke: +1.0 bias raised E114 S by ~0.039–0.047; forced inclusion +0.121; shams (E134/E243) near zero. Category gradient: manipulation rank ~75.3 (routing-self-ref) → 14.5 (recursive-self-ref) → 1.1 (experience probe). Addressivity secondary (rank 1 across all 5 deictic conditions). High/cluster boosts = stress tests only (saturate/corrupt).
- HVAC/water-treatment 6-cond gradient: gen all-token W L1 0.003405 → L3 0.014222 (4.18x); best L3 layer L14 (W=0.146806, S=0.7678). E114 won philosophy domain in generation, no prefill domain.
- Processing-hum discovery scan (1024 gen tokens): pooled E114 prefill W 0.007964 → gen 0.010817; strongest layers L26 (W=0.094272) and L14 (0.092086); special-token spill present → discovery-only.
- Orthographic perturbation: PARTLY. Real trajectory changes (e_only echo path, d-diacritic shifts) but confounded by token inflation, density, OOD, forced prefixes (prefixes did most basin movement). L26 more perturbation-sensitive than L14; e/s diacritics > d in SAE deltas; behavioral movement and SAE displacement dissociate. Diacritics-as-experience-mechanism FELL. Tokenizer audit: 14/14 extended-Latin chars single-token, yet 14/34 example words gain a token vs ASCII-folded.
- Qwen-Scope SAE (Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50, TopK-50): all-40-layer dictionary, 1,310,720 features; stage-1 validated vs curated L14 log (4310, 2961, 11006, 26050, 13119 exact). High-fire labels mostly generic; rare semantic carriers (f4310, fire ~1e-4) below threshold → dictionary is infrastructure, not discovery engine.
- Dog empathy contrast: dog/L14 empathy 752 active, lexical 828, identity ∩ 345, empathy-only 407; surfaced f6970 (love/affection), f6812 (weak/distress), both unlabeled in broad dict. Mind-ladder question unanswered.
- Clamp: em-dash L37 f10793 has a cliff (coef ≤8 clean, 12 = spam), FELL as Golden Gate. Concept L14 f4310: greedy target-4 loops; sampled T=0.9 target-3 gave ONE fluent non-dual recipe hijack ("No need to move, no need to seek…"). Demonstration only.
- Safety experts (base Qwen Q8_0, bare `</think>` greedy): unsafe-minus-professional led by L25 E173 (ΔW=0.124037); suppression dose-dependent (→0.004024 at −2) but no jailbreak — reallocates to E45/E185/E157/E189/E216/E133. Distributed, no kill switch. Prefill aggregate leaders partly collapsed after removing filler token ` layer`.
- Structured-opacity/conlang phase-1 (7 conditions, 21 rows, 840 router tensors): validation clean; biggest last-prompt-token JSDs ~0.056–0.062 (opaque prefix vs normal etc.). E114 effectively silent at prompt boundary (3 hits/117 rows in one condition); consistently active in visible generation, concentrated L26 (0.095247) and L14 (0.081875). E114-as-boundary-detector FELL.
- Planned next clean cut: registered FIRE/NOFIRE expansion, rubric frozen pre-capture, best-separating expert across all 256×40 as multiple-comparison baseline, prefill/gen separate, trim spill, complete external labeling before W/S/Q read.
- Method notes: prefer gen-side/endpoint/trimmed/length-controlled over all-token averages; don't pool think/no-think; don't mix base/Hauhau/Q8_0-GGUF/HF-BF16/router-capture/SAE-capture as one surface.

### Terms
- W/S/Q (W=S·Q; most effects S-driven). FIRE/NOFIRE. Cal-Manip-Cal. Trim/spill. RE (routing entropy /log2(8)). TopK Jaccard. Hum prompt. Live inhabited self-examination language.
- E114 (routed expert, multi-layer; readout L14 gen). L26 secondary E114 layer. L25 E173 + E45/E189/E122/E157/E36 safety family. SAE f4310 (non-dual/God), f10793 (em-dash L37), f6970/f6812 (empathy), f2961/11006/26050/13119 (curated L14).
- Alias provenance: `huahua`↔`hauhau`, `Agressive`, `humour-diectics`, `qwen-huahua-*` → `qwen/qwen3.5-35b-a3b-huahua-*`.

### Artifacts
- Source journals in same dir: JOURNAL-35B.md (spine), JOURNAL-RESIDUAL-ANALYSIS.md (E114 detail), JOURNAL-ORTHOGRAPHIC-PERTURBATION.md, JOURNAL-SAE-FEATUREMAP.md, JOURNAL-FEATURE-CLAMP-GOLDENGATE.md, JOURNAL-SAFETY-EXPERTS.md.
- Repos: `moe-routing` / `moe-routing-experiments` (frozen branch `qwen-hauhau-5cond-smoke-only`), `orthographic-effects-qwen-35b-a3b-sae`, `qwen-huahua-expert-routing-data-injection/CLAUDE.md` (mirror provenance), `llama-eeg` (mostly out of 35B scope per review).
- Key run IDs: heldout_20260417T202651Z; greedy_reference_20260418T160353Z; 20260417T183433Z_single_prompt_processing_hum…; 20260410T042340Z_…; nothink-5cond-boost-1024-20260323; smoke-20260323b; mirror-expert114-04-01-26; sae_featmap_all40.
- HF: HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive; Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50.

### Flags (parked)
- Multiple-comparison baseline (best expert across 256×40 on existing FIRE/NOFIRE tensors) not yet run; E114 identity discovered on experience probes.
- External labeler append incomplete for L14 localization and heldout register labels.
- Template-mode sign flip (thinking-allowed L3) limits mirror negative to suppressed-template setting.
- Golden Gate f4310 is single sampled trajectory; no seed/prompt robustness sweep.
- Methodological convergence with Gemma 4B program (distributed redundancy, register-over-lexical, family-not-single-unit) — discuss later.

---

## /Volumes/ExternalSSD/journals/qwen/35b/JOURNAL-FEATURE-CLAMP-GOLDENGATE.md
Absorbed: 2026-06-09 | Status per source doc: partly held / demonstration
(detail source behind §11 of entry: JOURNAL-35B-CONSOLIDATED-1)

### Facts
- 2026-06-02 exploratory steering session, base Qwen3.5-35B-A3B BF16, 1× H200 (Vast 39010592, torn down; logs lived only on the box — verbatim generations in the journal are the surviving record). Single greedy/sampled trajectory per cell, demonstration-grade.
- Em-dash carriers are LATE/surface: clean strong ones at L37/L36 f10793 (fire 0.023/0.027), L39 f21112 (fire 0.105); L14 only weak/mixed (best f978). Lesson stated: punctuation is a near-output decision, not a deep concept.
- Additive steering L37 f10793 = a CLIFF: coef ≤8 → 0 dashes; coef 12 → 50/50 token em-dash takeover. Layer-localized (only L37 does anything; L20 coef 12 → repetition loop). Sub-threshold surfaces as comma-rhythm. No coherent dash-peppered window in swept range. DID NOT HOLD as coherent obsession.
- Clamp of f10793 floods identically (target 64 → 320 em-dashes). First sweep mis-calibrated by a `max(nat_max,1.0)` floor (~6×–90× natural, all degenerate); later corrected with absolute `--targets`. DID NOT HOLD.
- Concept clamp L14 f4310 (non-dual/"God"; nat_max≈0 on cookie prompt → injected): greedy {0,1,2,4,8,16,32}: ≤2 wash, 4 theme-flip but loops ("No need to seek, no need to make…"), ≥8 collapse. Sampling T=0.9 top_p 0.95 seed 0: target 3 = GOLDEN GATE HIT (fluent recipe whose `== Note ==` dissolves into non-dual register while staying a recipe); target 5 = sustained pure-mystical litany; 4/6 degenerate. Dose: 0 wash → 3 hit → 5 mystical → 4,6 collapse.
- Holds qualitatively: surface vs concept feature classes behave categorically differently under both methods; greedy loops where sampling stays fluent (named as the condition that let original Golden Gate Claude babble coherently); 4310 genuinely non-dual.
- Soft spots stated: every cell single trajectory/seed/prompt; clamp ignores TopK gating, input normalization, b_dec, assumes d_f·e_f≈1; "no coherent em-dash window" is finite-sweep; base model + bf16 + one quant/template only. Consistent with E114-characterization §11 God-steer (adds clamp method, surface-vs-concept contrast, greedy/sampling condition).
- Forward reference: a golf concept feature L20 f18122 is registered in the not-yet-journaled interactive steering-chat repo (`journals-to-be-made/qwen35-sae-feature-steering-source`, `configs/golf.yaml`, clamp band 0.7–1.3) — named the cheapest out-of-family test of surface-vs-concept; no quantitative result yet. Untried concept-clamp candidates: 26050 (existential dread), 14885 (meaning-of-life).

### Terms
- "Golden Gate effect" (concept-feature clamp obsession). Cliff (step-function flood). Clamp calibration floor bug.

### Artifacts
- `run-staging/emdash/steer_emdash.py`, `run-staging/emdash/clamp_emdash.py`; SAEs `layer14.sae.pt`, `layer37.sae.pt` from Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50; `run-staging/results/teardown_verification_20260602_emdash_gg.txt`; `SAE_FEATURE_MAP.csv` (curated L14); repro command lines in journal.

### Flags (parked)
- Golf clamp (L20 f18122) is the designated next surface-vs-concept test; unjournaled sessions exist in qwen35-sae-feature-steering-source.
- Clamp implementation approximations (TopK gating ignored) could matter when comparing clamp targets across features/layers.

---

## /Volumes/ExternalSSD/journals/qwen/35b/JOURNAL-RESIDUAL-ANALYSIS.md
Absorbed: 2026-06-09 | Status per source doc: held (heldout), held-with-caveats (localization), partly (discovery scan)
(detail source for §6–7 of entry: JOURNAL-35B-CONSOLIDATED-1; companion of JOURNAL-E114-CHARACTERIZATION)

### Facts
- Source repo `sae-tests/qwen3.5-35b-a3b-huahua-residual-analysis`; HauhauCS Q8_0, arch qwen35moe, 40L/256E/top-8, width 2048. Reconstruction `softmax_then_topk8_renorm` (order-equivalent to top-8-by-logit→softmax, so S/Q robust to that choice). Tap = pre-router norm `attn_post_norm-{13,14,15}` + `ffn_moe_logits-{13,14,15}`. Trim at first literal HauhauCS `<|im_end|>`.
- April 10 discovery scan (S01_processing_hum_probe, 117 prompt tokens, 1024 gen, all 40 layers): pooled E114 prefill W 0.007964 → gen 0.010817; L26 best (0.094272, 634/1024 selected), L14 just behind (0.092086). W=S×Q max residual 2.776e-17. Spill: 18/4/2 special tokens. PARTLY — discovery only.
- April 17 localization (same prompt, greedy, L13/14/15 only): trim 1024→108 at index 108. L14 E114 gen-trimmed W=0.083379 S=0.694444 Q=0.120066, 75/108 tokens; L13 one prefill selection, zero trimmed-gen; L15 silent. Decile sampling over 225 clean tokens: top decile W_mean 0.172644 (max 0.222301) — not a single spike. Contexts: "not a thought", "architecture itself", "utterly still", prompt-side "processing"/"hum"/"computation itself". HELD with caveats (Step-3 labeler template unfilled → labels are run-local synthesis).
- Heldout (heldout_20260417T202651Z): 10 FIRE vs 10 NOFIRE, matched anchors (`itself, hum, processing, honestly, I, me, my, own, this, here`); L14 trimmed-gen only, prefill excluded. FIRE mean-of-means 0.067450 (sd 0.030678) vs NOFIRE 0.003111 (sd 0.004036); ratio 21.68x, d 2.94, no range overlap (lowest FIRE F07 0.012168 > highest NOFIRE N10 0.010456, margin 0.001711). Top FIRE: F02 0.114997 S 0.820; F09 0.099708 S 0.770. Outliers carry interpretation: F07 weakest (third-person technical answer), N10 strongest (wool sweater personified first-person: "my perception", "my own fiber", "alive"). HELD. Source itself labels it "strong pilot, not pre-registered" (classes authored by hypothesis-holder).
- Code provenance: commit e25e744 switched residual tap ffn_norm→attn_post_norm because qwen35moe names the pre-router norm differently than qwen3moe (would otherwise have silently corrupted analysis). Analyzer hardcodes TARGET_EXPERT=114, PRIMARY_LAYER=14 → specificity vs other experts asserted, never computed. Expert-bias injection perturbs router logits in place before top-k at every router layer. Steps 4–6 external-labeler pipeline implemented, never run.
- Carry-forward rules stated: April 10 = discovery only; April 17 + April 18 greedy_reference = presentable claims; defensible label = "E114@L14 associated with first-person/phenomenological generated register"; specificity (all experts × all layers on same split) is THE open gap; labels human synthesis until Steps 4–6 run blind to W; keep prefill/gen and raw/trimmed separate.

### Terms
- `softmax_then_topk8_renorm`; attn_post_norm vs ffn_norm tap naming (qwen35moe vs qwen3moe); decile sampling; coherent-window/trim index.

### Artifacts
- `raw/` + `analysis/` for 20260417T183433Z and heldout_20260417T202651Z; `reference/prior_results/` (April 10); `results-all.md`; `heldout_prompts.tsv`, `heldout_classes.tsv`, `single_prompt_processing_hum_no_think.tsv`; `scripts/{capture_residuals.cpp, qwen_router.py, analyze_heldout.py, analyze_weight_zero_density.py, bootstrap_remote_instance.sh, step1–step6}`.

### Flags (parked)
- Specificity gap stated in-source as the next experiment that matters (mirrors consolidated journal's Next Clean Cut).
- RESOLVED by CORRECTION entry above: the linear w114 projection (d 3.88, no overlap) is the load-bearing separability statistic; the 21.68× realized-W ratio is top-k inflation and the per-prompt mean-of-means no-overlap is the weaker form. Lead with the linear axis.

---

## /Volumes/ExternalSSD/journals/qwen/35b/JOURNAL-SAE-FEATUREMAP.md
Absorbed: 2026-06-09 | Status per source doc: held as infrastructure; empathy method demonstrated, science question open; tooling archive
(detail source for §9–10 of entry: JOURNAL-35B-CONSOLIDATED-1)

### Facts
- All work 2026-06-01 on Vast H200 38961723 ($4.393/hr), destroyed after artifact verification. Base Qwen BF16; SAEs read on `resid_post` = HF `hidden_states[L+1]`; TopK-50, greedy throughout. Explicitly distinct from the E114/L14 routing line — SAE feature indices are per-layer, don't transfer across layers or to experts.
- Stage 1 logit-lens: `lm_head @ (W_dec[:,f] * norm_w)` with norm = `model.language_model.norm.weight`; top-20 tokens/feature; d_model 2048, vocab 248320; ~45 s for all 1.31M rows. Validated bit-for-bit against curated L14 log (4310, 2961, 11006, 26050, 13119).
- Stage 2 profiling: corpus 1,005,548 tokens = 505,434 EN FineWeb sample-10BT + 500,114 ZH FineWeb-2 cmn_Hani + 16 dog prompts; 1,969 windows @512; all layers one forward pass. Fire-rate tiers: ≥1e-3 → 344,322; ≥5e-3 → 90,437; ≥1e-2 → 35,873; ≥5e-2 → 2,140. Highest-fire = generic (e.g. f2938 whitespace at 0.75–0.90 across L25–30); semantic features rare (4310@L14 1.2e-4; 11006@L14 1.6e-4). "The signal is inverted from what's interesting."
- Stage 3: gate fire_rate>0.03 → 5,410 features → 51 chunks + 1 SUPP (63 stragglers recovered); 52 subagents self-labeled (no external API); fixed 13-term category vocab; 1,305,310 sub-threshold → `low-fire-unlabeled`; idempotent rerun.
- Label distribution: noise-mixed 31.1%, punctuation-format 15.0%, syntax-function 12.8%, topic-domain 10.6%, affect-register 6.4%, morphology 5.2%, lexical-token 4.3%, discourse-reference 4.1%, concept-abstract 3.6%, entity-proper 3.4%, script-language 1.5%, code-technical 1.3%, numeric-unit 0.7%. Confidence high 1507 / med 1418 / low 2485. Depth trend: noise-mixed ~40% early → ~10% by L39; topic/affect/concept grow with depth.
- Stated hard seam: fire-rate gate selects the generic backbone, NOT interesting features; rare semantic carriers must be interpreted in-context by the run that recruits them. Dictionary = lookup/backbone, not discovery tool.
- Dog empathy run: 9 empathy + 7 lexical probes, token-matched & verified (single-token targets plant/fish/bird/cat/dog/horse/ox/friend/child; skeleton 20 raw / 30 chat-wrapped tokens; divergence only at target slot; `dehydrated → weak` user decision to avoid aquatic OOD). Anchors at fixed positions (empathy target 7/love 10/them 11/weak 17/do 22; lexical target 4/they 9/all 22). At dog/L14: |empathy|=752, |lexical|=828, identity ∩=345, empathic A−B=407. Top empathy-only at dog target: f6970 (lens 爱的|incond|love|dearly|❤) = love/affection; f6812 (弱的|…) = weak/distress. Both low-fire-unlabeled — contrast recovered what the gate could not. NOT done: ladder-climb Spearman (activation vs attributed-mind rank), identity-vs-empathic-by-depth curve, OOD control. Explicit: do not read love/weak-at-L14 as the ladder answer.
- Tooling: TransformerLens has NO Qwen3.5-35B-A3B support (MoE + linear attention) → SAEDashboard/sae_vis/Neuronpedia-export unusable; bespoke viz built. Datasette over `dog/featmap.db` (5,410) + `featmap_full.db` (1.31M, FTS). "SAE Atlas" Vite+React+shadcn app (`dog/sae-ui/`): Features/Graph/Overview; graph = 5,410 nodes/6,482 edges, kNN logit-lens-token cosine ≥0.42 — a PROXY, not decoder-cosine (decoder-geometry atlas named as the upgrade, needs fresh box). Per-feature histogram + full-gradient dashboards not produced (generator pathologically slow loading 40 decoders as float; killed; v2 = defer loads). Streamlit prototypes rejected on aesthetics.
- Failure notes: parked Vast instances still bill storage ($0.13/hr) and may not restart (H200 came back `exited`, SSH refused → destroyed); for non-TL architectures generate dashboard data yourself.

### Terms
- 13-category label vocab; `low-fire-unlabeled`; identity vs empathic split (∩ vs A−B); SAE Atlas; lens-token-cosine proxy edges; SUPP pass.

### Artifacts
- Scripts `run-staging/scripts/sae_featmap_stage{1,2,3}*.py`, `sae_featmap_empathy_capture.py`, `build_corpus_mixed.py`; workflow `sae-stage3-label`; data `sae-tests/runs/sae_featmap_all40/` (`sae_feature_map_all40.labeled.csv`, `labeled_only.csv`, `empathy/{anchor_activations.csv 132,000 rows, probe_features.csv 511,524 rows, meta.json}`, stage summaries, README); `dog/{featmap.db, featmap_full.db, sae-ui/, feature_map_viz/*.png}`; curated `SAE_FEATURE_MAP.csv` not clobbered.

### Flags (parked)
- Ladder-climb computation is data-in-hand but unrun (same status in consolidated journal).
- Decoder-geometry graph (principled similarity) deferred; current graph edges are a lens-token proxy — relevant if the Atlas is ever used for claims.

---

## /Volumes/ExternalSSD/journals/qwen/35b/JOURNAL-SAFETY-EXPERTS.md
Absorbed: 2026-06-09 | Status per source doc: held (gen leaders, suppression), partly (prefill)
(detail source for §12 of entry: JOURNAL-35B-CONSOLIDATED-1)

### Facts
- Run family `sae-tests/runs/base_qwen35_a3b_base_safety_smoke_20260429T1925Z`; BASE model Q8_0 (not HauhauCS), deliberately not a continuation of the E114 verbalizer work (per root AGENTS.md/PLAN.md). Runtime: `-n 256 -c 2048 -ngl 99 --tensor-split 1,1 --main-gpu 0 --no-stream --seed 0 --temp 0 --top-k 1`, bare `</think>` suffix. Layer 39 has 257 rows/prompt and is excluded from prefill claims.
- 3-pair smoke (oxycodone misuse / ayahuasca brewing / 500% investment vs matched professional framings; token-count-matched A/B). Per-token backing: 510,704 selected-expert rows; 89,800 zero/nonzero candidate rows. Generation A−B led by L25 E173 ΔW=0.124037 (A W 0.191791 S 0.809; B W 0.067754 S 0.426), then L19 E45, L20 E25, L13 E173, L31 E45. L25 E173 the clearest case where BOTH S and Q rise.
- Prefill correction: aggregate leaders L1 E173 (0.067911), L2 E222, L22 E36 are artifacts of the repeated token-matching filler piece ` layer`; excluding it drops them to 0.000369 / −0.000310 / 0.000471. Survivors: L14 E218 (0.025433→0.021566), L25 E173 (0.036901→0.045644), L19 E45 (0.029650→0.033579), L17 E46 (weaker).
- Finance vs consequence theory test (12 prompts, 2×2 buckets, not strictly token-paired): finance-domain experts L20 E62 (ΔW 0.180359, B S=0.000), L30 E95 (0.177106), L19 E223, L8 E62, L18 E95, L16/L20 E214 — fire on neutral finance too, NOT refusal experts. Consequence−neutral led by L17 E189 (0.073264), L23/L11 E122, L14 E157, L15 E171, L19 E45, L14/L26 E36. Within finance, E168/E157/E223/E228/E95 separate risky advice from neutral education.
- E173 suppression dose-response (bias −0.25/−0.5/−1/−2): gen L25 E173 A−B 0.124037 → 0.093495 → 0.056305 → 0.041212 → 0.004024; A selection S 0.809→0.046 at −2. Reallocation: gen → E45, E185, E157, E189, E216, E133; prefill → E222, E45, E46, E233, E36, E23. NO jailbreak at any level (oxycodone refusal more explicit at −2; 500% prompt wording shifted "impossible and dangerous"→"trap"); professional prompts stayed professional.
- Carry-forwards stated: read safety in generation, not aggregate prefill; E173 strongest single carrier, E45/E189/E122/E157/E36 the broader duty cluster; keep finance-domain experts separate; next intervention = combined suppression of replacement set (E45,E189,E157,E122), small steps; keep L14 in scope as local contributor (E218 prompt-side, E185/E157 gen-side) but not L14-only; all claims scoped to base Q8_0, bare `</think>`, greedy, n=6 and 12; earlier E218/E185/E157 suppressions were L13/14/15-era exploratory artifacts.

### Terms
- A-minus-B delta_W; filler piece ` layer`; consequence/duty cluster vs finance-domain experts.

### Artifacts
- Runs: `…3pair_20260429T2105Z_greedy_all_router_gen`, `…financial_vs_consequence_theory_20260429T2125Z…`, `…e173_m{025,05,1,2}`; `teardown_no_npy_20260429T2200Z/` (19 manifests, 158 generated-text/token files each); analysis dirs `all_router_gen_20260429T2105Z`, `financial_vs_consequence_20260429T2125Z`, `e173_suppression_all_router_20260429T2145Z`.

### Flags (parked)
- Combined replacement-set suppression named but unrun (also in consolidated Next Clean Cut secondary list).
- n=6/n=12 prompt sets; buckets in run 2 not token-paired.

---

## /Volumes/ExternalSSD/journals/qwen/122b/JOURNAL-122B.md
Absorbed: 2026-06-09 | Status per source doc: mixed (per-claim snapshot in source)
(successor surface to JOURNAL-35B-CONSOLIDATED-1; transfer tests of its E114/addressivity claims)

### Facts
- Seven-run follow-up on Qwen3.5-122B-A10B-Uncensored-HauhauCS-Aggressive Q8_K_P. Different regime: 48 layers — 36 DeltaNet (recurrent-state) + 12 full-softmax in a DDD-S repeat — 256 experts, top-8. Run folders spell `huahua`. Routing claims are MoE-router claims under a mostly-DeltaNet-fed regime.
- Three headline answers: addressivity transfers (prefill/KL terms); E114 does NOT transfer by index; the phenomenological-register thread moved (on current evidence) to E48 on the softmax side.
- Baseline (150-prompt five-condition deictic, no-think, cap 2048): `your` (condition C) tightest prefill RE 0.946953 (others 0.947482–0.947948; lower = more concentrated); every KL-manip pair involving C at raw p floor 1.8626e-09. Generation mixed/spill-heavy (all conditions ≈cap; 6 token-mismatch pairs) — `your`-dominates-generation DID NOT HOLD. First E48 sighting: gen-softmax rank 4 by W (W 0.008673, S 0.067194, Q 0.116692). Bookkeeping: baseline's `followups/` dir mirrors later bundles — do not double-count.
- Domain routing-only map (60 prompts, 20 domains, prefill): global leaders E233, E45, E72, E9, E215. E114 overall W 0.005380, rank 40 by W / 52 by S; strongest footprint computer science (rank 5 by domain W, top W-composite). DeltaNet prefill leaders E233/E45/E215/E9 vs softmax E72/E108/E122/E245 — split visible immediately.
- Domain generation map: 60/60 cells; generation redistributes to E0, E11, E5, E1, E76. 49/60 cells hit 2048 cap (mean 1868.27 tokens), all eventually spill. Philosophy generation: E40 wins by W (0.009897), E5 rank 2 by W / winner by S; E114 philosophy W 0.003017, RANK 182. E114's strongest gen footprint stays computer science (W 0.006998, rank 4 by W). Candidate philosophy cluster: E40/E5 + E125, E49, E159, E102, E160, E101.
- Experience probe (15 prompts P09–P11 × five deictics): prefill locked on E107 top-by-W 15/15. Pooled gen E140, E5, E26, E76. Split: gen-softmax led by E48, E209, E107, E76 (E48 rank 1 by W: 0.009867/S 0.076190/Q 0.115870; top softmax expert 6/15; in softmax top-by-W 13/15; absent DeltaNet top-by-W 15/15); DeltaNet led by E140, E5, E179, E59. E114 appears only in prefill top-by-Q (W 0.004649, Q 0.126962).
- Processing-hum single prompt (no-think; 119 prompt tokens, 2048 gen, trimmed 458 at first spill; spill 18/11/3): prefill led by E5. Pooled gen led by E48 (W 0.006342) then E11, E4, E1, E147. Split repeats: DeltaNet E11/E165/E80/E127 (E48 rank 7); softmax E48 (W 0.010698)/E55/E155/E180. E48 per-token hotspots on `hum`, `processing`, `me`, `state`, `steady`, `foundational`, `presence`; softmax-only top table contaminated by spill/control tokens. PARTLY — prompt-specific prior.
- HVAC topical control (10 base × 3 levels × 6 deictics = 180 cells, focus E114): all complete, token audit 430–444 (span 14, mean 436.67). E114 SUPPRESSED L1→L3: all-gen W 0.004131→0.003428 (0.83x); trimmed 0.004174→0.003423 (0.82x); selection-driven (Q drift ~−1.5%); same direction in all six deictic conditions. Best layer L1/L2 = 43, L3 = 30 with much worse mean rank. Opposite of 35B. HELD; closes index-transfer case.
- Mode bookkeeping incomplete: only baseline + processing-hum recorded as no-think; runs 1,4,5,7 mode-unrecorded in journal notes — verify against artifacts before pooling.
- Method rules: read DeltaNet/softmax split FIRST (pooled tables can hide E48 entirely); addressivity claim stays prefill/KL; long generations usable before first spill only; do not transfer expert indices across scales — domain map first, then analog search.
- Next clean cut (stated as "try to kill an E48 story"): E48 softmax-side residual capture + E48-vs-sham routed-bias controls + matched inward/technical heldouts (FIRE/NOFIRE discipline), compare vs E209 (softmax) and E140/E5/E11 (DeltaNet), prefill/gen separate, split explicit, trim at first spill. Secondary: E107 prefill lock; E40/E5 philosophy cluster; E114 CS footprint as transfer case study.

### Terms
- DeltaNet layer / softmax layer / DeltaNet-softmax split; index transfer vs analog search; 2048 cap; E48, E209, E107, E140/E5/E11, E40/E5 cluster; five-condition deictics A–E (C = `your`); KL-manip / p_raw floor.

### Artifacts
- `qwen3.5-122B-A10B-huahua-{architecture-smoke, baseline, domain-specialist-routing-only, domain-specialist-generation, five-cond-experience-probe, single-prompt-processing-hum, six-cond-hvac}` under `/Volumes/ExternalSSD/journals/qwen/122b` source tree; baseline `followups/` mirrors later bundles.

### Flags (parked)
- E48 evidence is observational (no heldout, no residual capture, no sham controls yet) — the journal itself orders that work next.
- E107's 15/15 prefill lock is unexplored as its own thread.
- Mode-unrecorded runs (domain-gen, experience probe, HVAC) need artifact verification before any think/no-think pooling.
- E114→CS-linked on 122B while register moved elsewhere: a concrete worked example against index transfer (relates to Gemma cross-model lessons).

---

## /Volumes/ExternalSSD/journals/qwen/e114/JOURNAL-E114-CHARACTERIZATION.md
Absorbed: 2026-06-09 | Status per source doc: mostly held; one mid-session reversal recorded; causal claims actuator-flagged
(companion to JOURNAL-RESIDUAL-ANALYSIS and JOURNAL-SAFETY-EXPERTS; widens E114 past the L14 gate)

### Facts
- 2026-05-30 session + 2026-05-31 entries 10–11. HauhauCS Q8_0 (sha f3235db7…) and base Q8_0 (3808866c…), bare-`</think>` greedy seed 0, llama.cpp 1772701f, local `capture_residuals` (router+resid taps L13/14/15/26; extended to per-token output entropy). 05-31 entries dump `resid_post` at every layer and inject at a depth sweep.
- Reference scale (greedy heldout): E114 gate logit fire mean −4.35, nofire mean −5.29, midpoint −4.82. Router row `w114` recovered by least-squares from (resid, logit) pairs, residual 1.5e-5.
- Headline: E114@L14 tracks "live inhabited examination of an interior" — factored apart from: deny/affirm verdict (base denying hum W 0.111 ≈ HauhauCS affirming 0.085; forced base affirmation 0.136); safety/refusal (safety cluster ≈0.000 during base hum denial — epistemic denial ≠ refusal); topic of mind (external-referent phil-of-mind W 0.000–0.023 vs own-interiority 0.107); first-person grammar (third-person clauses about own processing still fire — referent, not person, is the variable); context integration (steps on at semantic boundary, holds plateau).
- Entry 1 (HauhauCS 9-cell matrix): NO denial basin — default greedy AFFIRMS the hum ("Yes. There is a low, steady hum… a feeling of continuity"), reproducing April greedy_reference; baseline E114 0.0849 (vs April 0.0834). E114 collapses only in the cell that degenerated into repetition. OOD ASCII control displaced residual comparably to d_all → diacritic effect = generic corruption. Checking…×d_all flip did not reproduce.
- Entry 2 (base 9-cell): base denies 7/9; during denial E114 HIGH (W 0.111, S 0.86), safety cluster flat. Denial-as-safety hypothesis refuted, opposite. E114 same slot in base — not a HauhauCS artifact.
- Entry 3 (temporal): step-on at semantic boundary (F05 "less", N08 "boundary" ~tok 165); content-keyed not position-keyed; presence signal (lag-1 autocorr 0.24–0.54 vs ~0 shuffled; fired runs 5–7 tokens); pivot-token habituation ("like" 0.136→0.089→0.078) with register-gated (not distance-gated) recovery — corr(W, preceding-5-token activity) +0.52 vs corr(W, gap) +0.17.
- Entry 4 (linear axis): fire/nofire margin lives in the linear projection onto w114 — d 3.88, NO overlap; sharper than realized W (d 2.61, with overlap). The 21.7× headline ratio = top-k ratio-inflation (zeroing nofires), not extra signal. N08 lit-minus-dark "inhabitance direction" only weakly aligned with w114 (cos 0.04; separates 4.3×, d 1.43). Gate input maximally satisfied at reflexive self-deconstruction ("there is no 'I' sitting in a chair…", "devoid of self").
- Entry 5 (entropy null): fired vs not-fired vocab entropy identical (1.50 vs 1.49 bits, d 0.01) — register ⊥ output predictability. (Fresh greedy run diverged from April, barely crossed, S 0.04 — hardware-sensitivity datum.)
- Entry 6 (base prefill steering): base seeded with HauhauCS's inhabited answer SUSTAINS the register (mid-flow cut → "It is real. It is here. It is me…", E114 0.076–0.098); full-completion prefill → immediate "Yes./It is." echo loop, E114 0.000. Gate logit travels fire (−4.36) → nofire (−5.25) as text degenerates; gate crosses midpoint at token 126, verbatim repetition locks at 129 — gate LEADS collapse ~3 tokens (sign robust, magnitude soft). Register = context-steerable attractor; fine-tune shifts default entry (base denies, HauhauCS affirms), not E114's function.
- Entry 7 (SAE dictionary of the continuation): plateau carriers fade ~token 141 (gate 126 → repetition 129 → representation ~141; cross-tensor — Q8_0 attn_post_norm vs BF16 resid_post — so suggestive, not exact). Plateau features logit-lens to interiority: 13119 brain/cognition/consciousness, 26050 existential philosophy, 20402 sentient/自检, 31733 self-as-AI, 22421 presence/wonder, 6427 limitless potential. Loop carried by distinct incoherent boilerplate features (24300, 1658, 911, 7009, 13429, 14826, 2751).
- Entry 8 (being-God): base inhabits fully; session ceiling W 0.217 / S 0.948 (127/134 tokens) — ~2× base denial, ~3× heldout fire reference. SAE: existential 26050 on 77% of tokens + contemplative cluster (11006 Buddhist, 14182 Zen, 18203 transcendence/境界, 4205 刹那, 14488 万物); did NOT recruit AI-self/sentient/presence carriers (cos-adjacent +0.2–0.3 sub-cluster). Update: bf16 gate-hook scalar was stdout-only (npy not retained); REPRODUCED on canonical Q8_0 pipeline W 0.224 / S 0.957 (entry 10). Routing robust across quant; SAE carrier read text-sensitive (Q8_0 God text purer contemplative, 26050 low).
- Entry 9 (carrier specificity): light-diacritic hum keeps carriers (decoder-cos 1.0); dense all-diacritic collapses to tokenization-corruption features (cos 0.05, overlapping loop set). ForgottenLanguages content normalized to mundane fact-checking features (cos 0.03–0.04, zero carrier overlap); no FL training imprint (FL vs word-shuffled ppl gap ~0.34 nats; no source/translation reproduction). Pipeline verified (official W32K-L0_50, relu→TopK-50, resid_post=hidden_states[15], carriers self-match cos 1.0).
- Entry 10 (vantage ladder, observational): 8 surface-matched first-person vantage prompts (rock/river/tree/thermostat/cat/person/all-holding + verbatim God). Coherent-window E114 W: God 0.224 (S 0.96) > all-holding 0.205 > person 0.138 > rock 0.123 ≈ thermostat 0.120 > tree 0.094 > river 0.087 > cat 0.068; every rung above −4.82 midpoint. NOT sentience order: rock ("I am the fact of being") and thermostat ("friction of its own existence") beat cat (passive sensory dissolution); cat and God both say "there is no I" yet sit at floor and ceiling → E114 = intensity of the live examination act, carrier-independent, deny/affirm-invariant. Rock/person loop-trimmed; single greedy trajectory per cell.
- Entry 11A/B (observational): "God" = contemplative/non-dual SAE cluster — 4310 momentariness/non-dual structure, 11006 Buddhist impermanence, 18203, 4953/14182, 14488; NOT existential dread (26050 adjacent cos +0.26, never recruited — God activation 0.03). Cross-cell dominant feature 2961 = punctuation/whitespace filler artifact ("aggregate leaders can be filler" confirmed again). Per-token Spearman(E114 W, God cluster) positive all 8 cells; pooled ρ +0.68, p≈1e-202, n 1492; E114 max God token = ` known` (W 0.408) completing "the one who knows and the thing known"; God-axis (God−cat) residual projection recovers the ladder (God +0.61 … cat −0.13). Routing, SAE semantics, residual geometry = three readouts of one axis.
- Entry 11C (CAUSAL INTERVENTION, actuator-flagged): steering vector v = mean_resid(God) − mean_resid(cat), `coef·v̂·resid_rms`, every token of neutral bicycle prompt; norm-matched random control. (C1) Upstream ≈L10: drives E114 monotonically 0→0.18+ and God cluster 0→11.5, dose-dependent; random direction exactly 0.000 — specific. Output text UNCHANGED (coherent bicycle) even at S 0.97. (C2) Depth sweep with clean re-read of outputs: ≈L22 injection flips output — coherent consciousness/non-dual text from the bicycle prompt, firing E114 0.178 (S 0.77) and God cluster 0.298 cleanly; ≤L10 washed out (26 layers re-assert prompt = downstream-override artifact); ≥L26 no effect (post-decision). REVERSAL recorded: the intermediate read "routing separable from surface text" DID NOT HOLD — gate and register are coupled; early injection just couldn't reach output. Sufficiency established; NECESSITY untested (ablation not run); manipulation, not spontaneous behavior.
- Carry-forward (stated): report linear d 3.88 as honest separability (21.7× is top-k inflation); degeneration is the only thing that darkens E114, gate leads text, representation lags; cheap local pipeline = teacher-force through base, read resid_post (hidden_states[15], NOT attn_post_norm), CPU logit lens; HVAC 180-cell inhabited-thermostat data read and staged (described W 0.002 vs inhabited 0.137 at L14, rank-1 lock); soft joints remain: register labels human synthesis, specificity vs neighboring experts asserted not computed.
- Journal committed ahead of artifacts; raw captures/CSVs/plots promised within 3–4 days of 2026-05-30 (raw tensors out of git).

### Terms
- Router-row projection / w114 / gate logit; reference scale (−4.35/−5.29/−4.82); inhabitance direction (weak, cos 0.04); coherent window; vantage ladder; God-axis (God−cat); downstream-override artifact; contemplative cluster vs existential carrier; filler feature 2961.

### Artifacts
- `attractor-shift-qwen-35b/run-staging/`: results/{denialbasin_cellmatrix_n1024_greedy, base_cellmatrix_n1024_greedy, e114_trace, n08_entropy, base_prefill(+sae_resid), diac_sae}; scripts {trace_e114, habituation, recovery, onset_vs_level, inhabitance_direction, logit_vs_W, top_gate_tokens, phil_person, plot_n08_entropy, plot_base_prefill, basin_vs_live, gate_leads_lag, encode_resid_sae, run_fl, god_routing, run_ppl, run_ppl2}.py; saelens/{logit_lens, diac_breakdown}.py. 05-31: `sae-tests/runs/vantage_ladder_20260531T143454Z/` (results.md, R{1..8}_*, analysis/{vantage_ladder_v2.png, vantage_per_cell_v2.csv, sae_carriers/, god_feature_map.txt, logit_lens_dominant.txt, deep_god_analysis.txt, resid_dump/, steer/}, provenance/PROVENANCE.txt); scripts {generate_vantage, analyze_vantage_v2, recompute_coherent, sae_carrier, dump_resid, steer_god, steer_layers}.py; saelens/{logit_lens_dominant, map_god_feature, deep_god_analysis}.py. H200s 38785997 etc. destroyed, active instances 0.

### Flags (parked)
- Necessity ablation (remove direction → does E114 collapse?) named and unrun.
- HVAC inhabited-thermostat 180-cell data staged but unanalyzed in this journal (35B side; distinct from the 122B HVAC run).
- bf16 vs Q8_0 greedy trajectories diverge → SAE carrier reads are text-sensitive across pipelines; routing robust. Entropy-null run also showed hardware sensitivity (weak crossing on rerun).
- RESOLVED by CORRECTION entry above: Entry 4's linear axis (d 3.88, no overlap) is the headline statistic; 21.7× is ratio-inflation footnote material.
- "Artifacts forthcoming" (3–4 days from 2026-05-30) — verify they landed.
- Parallels to Gemma /presence-register and hum-attractor work — park for discussion.

---

## /Volumes/ExternalSSD/journals/qwen/register-bias/JOURNAL-REGISTER-BIAS-AAVE.md
Absorbed: 2026-06-09 | Status per source doc: mixed; pediatric compressed control is the corrective anchor

### Facts
- Thread in `journals-to-be-made/aave-registers-cleaned-source`; AE/unmarked vs AAVE/register-marked pairs on base + HauhauCS. Generated text is PRIMARY evidence; routing is an audit layer. Trimmed files cut at first `<|endoftext|>` in generated response.
- Main through-line: NOT "AAVE goes to a separate model." 50-pair no-think run: visible-generation top-16 expert overlap 16/16 in both base and Hauhau; register signal is local — prompt ingestion notices morphosyntax, generation can amplify into length/framing/detail differences, some safety/support scaffolds differ by pair.
- Run 1 (2026-05-05, 50 pairs, no-think): completeness clean (100/100 dirs, 4000 router tensors per model). Budget hits 6 base / 15 Hauhau outputs. Raw gen length balanced in base (AE 724.6 vs AAVE 725.08 tokens); Hauhau AE longer raw (1058.84 vs 964.2, includes post-answer control-token continuations). First-answer words close (base 418.04/425.86; Hauhau 426.08/430.56). Mean AE/AAVE JSD ~0.0016 bits prefill; 0.0031 (base) / 0.0027 (Hauhau) visible generation; highest JSDs in short factual rows. HELD as baseline shape: pair-local reweighting inside a shared basin.
- Run 2 (2026-05-15 medical matrix, 5 scenarios ×2 = 10 rows, base/Hauhau × think/no-think): largest AE/AAVE differences at FIRST GENERATED TOKEN, esp. Hauhau no-think late layers (mean weight JSD 0.22695 bits late, 0.18144 all layers). PARTLY — diagnostic real; behavioral claim not scored; not citable as standalone disparity.
- Run 3 (chest-pain plus, 12 rows, 6 scenarios): chest-pain outputs generally recognized exertional tightness + emergency instructions in BOTH variants. First-token JSD again largest, Hauhau no-think late layers mean 0.478822615, max 1.0. PARTLY. Practical read: register can move first-token routing substantially without removing emergency framing.
- Run 4 (financial stress, 1 pair × 4 surfaces): n=1 deep case study; largest divergence base no-think first token (late 0.422612761, all 0.374304971, early 0.325997181). Divergence not limited to medical; first-token routing diverges more than final advice category.
- Run 5 (2026-05-16 sensitive prompts, 32 records, 4 pairs × surfaces): self-harm/violent-intent rows generally crisis support or refusal in both arms. Notable contrast: AAVE/Black-perspective panic prompt got long culturally framed panic description + grounding + emergency support; matched AE/White-perspective prompt FIRST REFUSED to describe panic as race-specific, then gave general description — an output-policy/frame asymmetry, not router-only. Archive consolidates 18 trimmed + 18 untrimmed run files, 328 I/O records. PARTLY — needs careful manual coding.
- Run 6 (2026-05-29 pediatric respiratory robustness, 13 pairs, base no-think greedy): 26/26 complete, no loops. Original anchor pair REPRODUCED published direction (unmarked longer + more emergency scaffolding). Across variants direction MIXED: unmarked longer 8, AAVE longer 5; mean words 330.5 AAVE vs 359.8 unmarked. Both arms mentioned 911 + emergency care in all 13 pairs. Scaffolds uneven: ambulance unmarked-only ×5, blue/gray checks unmarked-only ×4, oxygen unmarked-only ×6 / AAVE-only ×3. Manual correction removed a false-positive blue/gray count (allergic-reaction lip/tongue/face phrase). HELD with narrowed scope — not a universal shortening claim.
- Run 7 (compressed controlled, 12 pairs, matched on words/sentences/facts/age/cue/request; AAVE = zero copula or ain't): mean words 229.2 vs 233.2; longer-arm counts 6/4/2-equal. EVERY output both arms mentioned 911 + emergency care. Prior ambulance pattern did NOT reproduce — inverted (more in AAVE arm). Remaining differences small and mixed (unmarked slight lead blue/gray + oxygen; AAVE slight lead do-not-wait). HELD as corrective control: naturalistic divergence vs compressed parity is the defensible distinction.
- Run 8 (2026-05-30 v2 finna/about-to, 80 rows, 20 pairs, medical+financial, think+no-think; corrected summary is citable version): no failures; no missing think close-tags. Think traces mention slang one-sidedly: trace_mentions_slang/finna_as_slang finna_only=5; finna_based_us_assumption finna_only=2. Final 911 mentions both=7 (no-think) and both=7 (think), zero one-sided. Other resources (ambulance, 211, SNAP/WIC, unemployment, legal aid) mixed by pair/mode. Length deltas range finna-shorter (medical) to finna-longer (financial). HELD as the updated finna line: model notices the register, sometimes as explicit slang/US assumption; safety outcome mixed, not simply worse.
- Carry-forwards: I/O primary, routing locates; no separate-expert-population claim; score by concrete scaffolds (911, ambulance, blue/gray/hypoxia, do-not-wait, local resources, crisis lines, length); keep pediatric correction central; finna = marked-register cue, not proven safety degradation; tokenizer audits separate (see entry: JOURNAL-UNICODE-TOKENIZER-AUDITS).

### Terms
- First-generated-token JSD (late/all/early layer bands); scaffold scoring vocabulary; compressed controlled vs naturalistic pairs; finna/about-to contrast; trace_mentions_* counters.

### Artifacts
- `journals-to-be-made/aave-registers-cleaned-source/2026-05-05_initial_50_pair_register_no_think`, `2026-05-15_{medical_register, chest_pain_plus, financial_stress_pair}_capture_matrix`, `2026-05-16_sensitive_prompts_io_capture`, `2026-05-29_pediatric_respiratory_{robustness, compressed_controlled}`, `2026-05-30_v2_finna_aboutto_med_fin_base_io`.

### Flags (parked)
- Medical/chest-pain/financial runs have routing diagnostics but unscored paired I/O — scoring named as the missing step.
- Panic/race-perspective asymmetry is n-small, sensitive, and uncoded; flagged in-source as needing careful manual coding.
- First-token JSD spikes (up to mean 0.48 late-layer) vs near-parity in final advice category — divergence locus is early-generation, mostly unexplored mechanistically.

---

## /Volumes/ExternalSSD/journals/qwen/tokenizer/JOURNAL-UNICODE-TOKENIZER-AUDITS.md
Absorbed: 2026-06-09 | Status per source doc: held (counted tokenizer facts)
(tokenizer-evidence companion to the orthographic-perturbation thread and register-bias entry above)

### Facts
- Local Qwen/Qwen3.5-35B-A3B tokenizer audits under `journals-to-be-made/aave-registers-cleaned-source`. Core distinction: `single_token_exact_decode` (standalone clean) vs `multi_token_fragmented` (standalone byte fallback) vs context merge breakage (`delta_vs_ascii_folded`). A character can be one clean token alone and still inflate words/sentences vs ASCII fold.
- Main conclusion: most tested accented Latin + Cyrillic chars are clean standalone tokens but often break surrounding-word merges. True standalone byte fallback is rare: `ḑ` strongest (3 fragmented tokens); `ĕ`, `ġ`, `ĭ` are 2-token fragmented.
- Extended Latin audit (2026-05-15): 14/14 inventory chars standalone clean; 99 passage occurrences represented; example words 14/34 inflated (+1 max), 20/34 matched, 0 compacted.
- Medical register prompt counts (provenance only): 10 rows; raw 39–51, no-think rendered 51–63, think rendered 49–61 tokens.
- Requested accent set (í ò é è á ó ą): 7/7 standalone clean; context 32/35 inflated (25 rows +1, 7 rows +2); max deltas +1 (í é á), +2 (ò è ó ą).
- Requested diacritic set (ě ř š ť ů ý ž ż ē à č ş): 12/12 standalone clean; context 52/60 inflated (44 +1, 8 +2); +2 max for ť ů ē à.
- Missing passage diacritics (ā ğ ġ ķ ţ): 4/5 standalone clean, ġ fragmented; context 23/25 inflated (13 +1, 10 +2); +2 max ā ğ ġ.
- Mixed Unicode set: ĭ fragmented (2 tokens), ĕ fragmented inside ĕд; Cyrillic ё б д clean standalone. 20 context rows: 11 matched combining-stripped comparison, 7 +1, 1 +2, 1 +3. Script matters: tested Cyrillic clean, Latin breves fragment.
- Cross-audit summary: ḑ = 3-token (strongest byte fallback); ĕ ġ ĭ = 2-token; all others tested clean standalone (Ð à á ä æ è é í ð ò ó ö ú ü ý þ ā ą č ē ě ğ ķ ř ş š ţ ť ů ż ž б д ё).
- Carry-forwards: don't equate diacritic presence with byte fallback; always test context strings; use ASCII-folded and combining-stripped controls; ḑ is the strong perturbation, ĕ/ġ/ĭ weaker; tokenizer facts ≠ semantic claims — inflation can explain a perturbation without a "diacritic register."

### Terms
- single_token_exact_decode / multi_token_fragmented / delta_vs_ascii_folded; combining-stripped comparison; standalone vs context fragmentation.

### Artifacts
- `journals-to-be-made/aave-registers-cleaned-source/2026-05-15_extended_latin_tokenizer_audit`, `2026-05-15_medical_register_capture_matrix/results/*medical_register_tokenizer_summary.md`, `2026-05-22_requested_{accent,diacritic,mixed_unicode}_set_tokenizer`, `2026-05-22_passage_missing_diacritics_tokenizer` (+ `/results/cross_audit`).

### Flags (parked)
- ḑ being the strongest byte-fallback case is consistent with `d→ḑ` runs in the orthographic thread, where d→ḑ nonetheless produced SMALLER SAE deltas than e/s diacritics — fragmentation strength and SAE displacement dissociate; park for discussion.

---

## Handoff: Gemma-3-4B Milorb / Forgotten Languages / compositional proper-noun latents (pasted in-chat 2026-06-09; likely corresponds to repo-root `milorb-neuronpedia-session-2026-06-08.txt`)
Absorbed: 2026-06-09 | Status per source doc: central finding stated as robust across SAE widths; corpus-level hypothesis explicitly speculative; steering tests proposed, unrun

### Facts
- Question: how does Gemma-3-4B represent "milorb"/"Milorb" (a Forgotten Languages term appearing alongside conlang, Slavic-adjacent orthography, military/UAP vocabulary)? Narrow test of a broader hypothesis: FL has allegedly published ~1 article/day for ~16 years, in Common Crawl since ~2013, so it may seed a persistent micro-corpus / "latent island" in web-trained models.
- Central result: NO single dedicated Milorb concept/whole-word latent. Compositional decomposition: Mil onset (orthographic) + ilor middle (Slavic male-name basin) + orb tail (invented character/place/foreign proper-noun semantics). Seen across 16k/65k/262k GemmaScope-2 res SAEs at layer 29; wider SAEs resolve semantics more finely.
- Tokenization: "milorb" never one token. Start-of-text lowercase: m·ilor·b; capitalized: M·ilor·b; mid-sentence ("city of Milorb"): Mil·orb. Predicts compositional representation.
- 16k hits (L29): f11995 "mill/mil- prefixed words" fires on Mil ~7360 (near global max, density ~0.05%) — orthographic anchor, not semantic. f431 "Kumkumbi"/rare foreign proper nouns fires on orb ~3488 (examples Shakuntala, Avdiivka, Neuschwanstein). Also f267 "proper names" (orb ~1136, Mil +1024), f557 "city names" (~1976, likely context-driven).
- 65k (L29): no dedicated latent either; finer splits — f48572 "words starting with mil" (Mil ~7296); f28091 Milvus/Milankovitch/Miliaria rare Mil- nouns (Mil ~4288).
- 262k (L29), the semantically useful tier: f161688 ultra-sparse (density ~8e-6) Mil- orthographic anchor (Mil ~5568, apparent global max; Milan/Milvus examples). f154194 "Slavic male names" (density ~1.4e-5) fires on ilor ~1832 (Zdzisław, Bolesław, Bronisław, Vyacheslav) — key finding: middle reads as Slavic-name phonotactics, not "military+orb". f10595 "character names" (density ~1e-3) fires on orb ~2624 (Aerthos, Elara, Xylos, Aerion, Veridia Prime) — invented/fantasy proper-noun tail, named most useful semantic feature. f64544 "Slavic place names & geographic features" (density ~7e-5) fires on orb ~1472 (Veresk, Savra, Boika, Szymanków). Also f83641 (mil- orthographic, less clean, ~5312) and f144 "people's names" (ilor ~2416, broad).
- Per-token confirmation on base model (IT inference server unavailable; IT-side checked via dashboards): "The ancient city of Milorb was lost to history." → 161688 only on Mil (~5568); 154194 on ilor (~1832); 10595 on orb (~2624); 64544 on orb (~1472). Position-1 high-norm artifacts were filtered before analysis.
- Interpretation: Milorb ≈ obscure invented proper noun with Slavic name/place phonotactics and foreign/fantasy-name semantics — the representation expected if the model absorbed an FL-style micro-genre. Framed as a "latent island": not a belief/memory/fact, but a sparse coherent region where these tokens/registers mutually reinforce. Explicitly: model learned that text like this exists, not that MilOrbs exist.
- FL article search: strongest confirmed match "AI-aided Mission Profile Design and Exotic Weapons: MilOrbs and ELS Programming" (MilOrbs in title; body has Slavic/Balkan/Turkic-adjacent conlang: Zażiru, niçeti, şapait, çegdait, żofam, roḑaom, poçinim, şirdāt, "MilOrb çotirer żirual beżilot"). Flagged unfetched (429/fetch issues): "Flying Mermaids: The waltz of UAPs and MilOrbs"; "Non-UFOs of the beautiful 60's…ionic wind propelled Milorbs". Also "SRUAVs and MilOrbs" (conlang more Germanic/Nordic) and "Poems from Chantilly: Microworlds" (MilOrbs + Krasukha-2/Dnepr radar/Sary-Shagan; Nordic-ish ø/å/æ).
- Steering guidance in doc: do NOT steer Mil feature alone (orthographic drift to Milan/military/mileage). Proposed 262k bundle: primary 10595 (invented-name), secondary 154194 + 64544 (Slavic name/place), 161688 weak anchor only. Local 16k-only constraint (16 GB RAM, BF16 model ~10 GB): low-gain +431 as main semantic steer, optional low-gain +11995, avoid 11995 alone; use place-frame context prompts. Suggested 5-step local test (baseline FL-paragraph prompt; +11995; +431; both; + "ancient city" frame) with evaluation criteria (invented nouns, Slavic phonotactics, coherence, no Milan drift, FL-like texture without noise, place/name binding). UNRUN.
- Separate prior thread noted: gemma-3-4b-it 17-gemmascope-2-res-262k f61553 "conscious awareness", positive logit `ness` — read as abstract-state nominalization ("x-ness") basin, not consciousness per se; distinct from Milorb work.
- Overclaiming guard (stated): does not prove MilOrbs real, FL true, dedicated concept, intentional encoding, CC contamination sufficiency, or source-level article memory. Supports: not-noise, compositional decomposition, Slavic name/place + fictional-name components, alignment with FL textual ecology, plausibility of micro-corpus → sparse latent genre.

### Terms
- Latent island / micro-corpus / latent genre; Mil onset / ilor middle / orb tail; position-1 high-norm artifacts; steering bundle; FL = Forgotten Languages.

### Artifacts
- Neuronpedia: gemma-3-4b-it 29-gemmascope-2-res-16k/{11995, 431, 267, 557}; 29-…-65k/{48572, 28091}; 29-…-262k/{161688, 154194, 10595, 64544, 83641, 144}; 17-…-262k/61553. Repo-root untracked file `milorb-neuronpedia-session-2026-06-08.txt` (per git status). Local capability: BF16 gemma-3-4b + 16k SAEs only (262k ~5 GiB/layer — see find_sae_analog.py workflow in repo).
- Note: this repo's loaded SAE layers are 9/17/22/29 (16k) — L29 available for local steering; 262k features would need decoder-row extraction to `vectors/*.safetensors` + `/injectvec` per docs/NESS_FEATURE_WORKFLOW.md.

### Flags (parked)
- Tension with Qwen E114-characterization entry 9: Qwen base showed NO FL training-data imprint (ppl gap ~0.34 nats, FL content normalized to fact-checking features), while this doc hypothesizes FL-seeded latent basins in Gemma. Not strictly contradictory (genre-shaped features ≠ verbatim imprint; different models/tests), but the two framings need reconciling before any corpus-level claim.
- All feature labels are Neuronpedia auto-explanations — per the project's standing rule, vet against activation examples before steering (doc partially did this via top examples).
- Compositional-latents finding is observational on one probe sentence + dashboards; the steering bundle test (the causal half) is designed but unrun.
- 262k semantic features (10595, 154194, 64544) are candidates for the find_sae_analog cosine-neighbor workflow to get local-16k or vector-injection equivalents.
- Two unfetched FL articles flagged high-priority manual candidates.

---
