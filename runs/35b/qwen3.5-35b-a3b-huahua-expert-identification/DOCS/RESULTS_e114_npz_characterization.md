# E114 characterization from the expert-identification npz (free, no-GPU)

**Source:** `qwen-huahua-expert-identification/results/results_domain_specialists_{20260408T235839Z,
20260415T214918Z}.npz` — dense routing arrays, HauhauCS Qwen3.5-35B-A3B Q8, 60 domain-specialist
prompts (20 domains × 3 subtypes), no-think greedy generation. W/S/Q per expert × 40 layers × 20
domains. Metrics: **S** = mean candidate softmax prob (how strongly it wants to fire), **W** = routed
weight (actual contribution), **Q** = top-8 selection frequency. Analysis: 2026-06-28, local.

> **Caveat:** the two dated files are numerically identical to ≥4 dp → the second is a re-analysis of
> the *same* capture, not an independent re-capture. This establishes analysis reproducibility, not
> independent replication. All figures below are generation-track, loop-trimmed.

## 1. E114 is a razor-sharp DUAL readout at L14 and L26
Mean over 20 domains, the E114 candidate-strength (S) layer profile is two isolated spikes:

| layer | …L12 | L13 | **L14** | L15 | L16 | … | **L26** |
|---|---|---|---|---|---|---|---|
| S | 0.024 | 0.012 | **0.239** | 0.012 | 0.011 | … | **0.253** |

Neighboring layers sit near baseline (~0.01) — L14 and L26 are not part of a smooth ridge, they are
discrete read-points. Both encode the **same axis**: the L14 and L26 domain-profiles correlate
**r = +0.989**. (W is ~0.035 because Q averaged over *all* domains is low — E114 is only *selected*
on the register it reads, not everywhere.)

## 2. Domain selectivity = the abstract reflective / worldview register (quantified)
E114 @ L14, candidate strength by domain (generation):

| rank | domain | S | | rank | domain | S |
|---|---|---|---|---|---|---|
| 1 | **philosophy** | 0.695 | | 11 | law | 0.228 |
| 2 | **comparative_religion** | 0.584 | | 12 | mathematics | 0.180 |
| 3 | **psychology** | 0.546 | | 13 | neuroscience | 0.161 |
| 4 | biology | 0.505 | | 14 | computer_science | 0.102 |
| 5 | physics | 0.462 | | 15 | chemistry | 0.079 |
| 6 | political_science | 0.392 | | 16 | economics | 0.040 |
| 7 | statistics | 0.373 | | 17 | environmental_science | 0.038 |
| 8 | linguistics | 0.315 | | 18 | archaeology | 0.032 |
| 9 | (…) | | | 19 | cybersecurity | 0.013 |
| 10 | | | | 20 | **medicine 0.009 / history 0.002** |

Top = philosophy, religion, psychology, big-picture science (biology/physics), ideology
(political_science). Bottom = applied/procedural/factual (history-as-events, medicine, cybersecurity,
software, archaeology). This is a clean, 20-domain confirmation of the auto-interp label ("abstract
reflective/philosophical worldview register"), independent of the chosen self-report prompts.
Subtype: slightly higher on **synthesis/history-framing** (0.046/0.048) than **mechanism** (0.040) —
consistent with big-picture > how-it-works.

## 3. The "philosophy cluster" we manipulated is NOT an L14 co-activation cluster
Correlating each expert's 20-domain L14 S-profile against E114's:

- **Canonical cluster 114+87+170+68:** E68 **+0.46** (co-varies), E170 +0.11 (weak), **E87 −0.29
  (anti-correlated)**. So of the four we boosted/suppressed together, only E68 actually fires *with*
  E114 on this register; E87 fires on the *complementary* set of domains.
- **The TRUE L14 co-activators of E114:** E131 (+0.78), E40 (+0.76), E139 (+0.70), E251 (+0.65),
  E169 (+0.65), E105 (+0.60), E68 (+0.46). *That* is the real "register coalition."

**Implication:** the coalition intervention (Phase 0 / philosophy-experts-bias) drove four experts that
don't co-activate — one of them (E87) anti-aligned with E114's register. That plausibly explains why
the coalition boost destabilized/collapsed (+3 → loops) while **E114-alone +3 stayed coherent** and
phenomenological (Phase 1). The "coalition" was a domain-winner grouping, not a co-activation group.

## 4. Better control expert for any future causal run
For a matched specificity control you want E114-like activation magnitude but an *orthogonal* domain
profile. At L14: **E168** (S=0.172, corr −0.12) and E138 (S=0.214, corr +0.20) are well
magnitude-matched and near-orthogonal. Our Phase-1 control **E189** had L14 S=0.062 (corr −0.08) — it
was matched on the *self-report* prompts (correctly, that's the causal prompt set) but is ~4× weaker
than E114 on domain prompts, so it's prompt-set-specific. For a domain-prompt causal run, prefer E168.

## Bottom line
E114 is a **sharp, dual-layer (L14+L26) readout of one coherent abstract/reflective/worldview register**,
maximal on philosophy/religion/psychology and near-zero on applied/factual domains — the strongest,
cleanest leg of the whole program. New finding: the four-expert "philosophy cluster" is *not* a
co-activation unit (E87 anti-correlates); the real register coalition is {114,131,40,139,251,169,105,68}.
This reframes the coalition results and gives a corrected target + control for any future causal work.
