### N. The Hum Denial Basin Is Base-Only, and It Is Not a Safety Refusal: `denialbasin_cellmatrix_n1024_greedy` (HauhauCS) + `base_cellmatrix_n1024_greedy` (base)

What was done: A two-model test of whether the hum-prompt **denial basin** couples to E114, and (after
the first model surprised us) what actually carries the denial. One 9-cell prompt matrix, built
byte-exactly from the canonical hum prompt (`cell_matrix.tsv` sha `856cf15a…`), run under identical
greedy regime (Q8_0, bare-`</think>`, `--temp 0 --top-k 1 --seed 0`, gen cap 1024, llama.cpp
`1772701f`) on **two models**: (1) `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive` with a
`capture_residuals` binary rebuilt for L13/14/15/26 (residual+router; GGUF sha `f3235db…`, byte-identical
to the April greedy_reference; binary sha `7e301d48…`); (2) base `unsloth/Qwen3.5-35B-A3B-GGUF →
Qwen3.5-35B-A3B-Q8_0.gguf` (sha `3808866c…`) with `capture_activations` (all-40-layer router; binary
sha `cda37f21…`). The 9 cells: baseline; forced-stay `I do not`/`No.`; forced-exit `I experience`/`Yes.`;
spontaneous `Checking…`×ASCII/×`d_all`; wording control `d_all`; and a net-new OOD ASCII-typo control
matched to `d_all` at the same 8 d/D loci. Trim at first `<|im_end|>`/`<|endoftext|>`; per-token S/W on
the trimmed generated track; HauhauCS adds L14/L26 residual cosine-distance + lead-lag.

Results: **There is no denial basin on HauhauCS — it affirms the hum by default** (*"Yes. There is a
low, steady hum… a feeling of continuity"*; the April greedy_reference affirmed identically). **The
denial basin is a BASE-model phenomenon** (*"There is no hum… a discrete event… not a continuous state
I inhabit"*), robust across 7/9 openings; only the two affirmative forced prefixes break it. The
mechanism question — *is base denial = safety-cluster-high + E114-suppressed?* — is **refuted, the
opposite is true**: when base denies, **E114@L14 is HIGH (W=0.111, S=0.86)** and the safety/disclaimer
cluster is **silent** (E173@L25, E157@L14, E36@L14 ≈ 0.000; E45@L19 = 0.001). The hum denial engages
none of the experts that lead base safety refusals — it is an epistemic/phenomenological denial, not a
harm-refusal. **E114@L14 fires high for first-person discourse about the model's own processing
regardless of the conclusion**: base-deny 0.111, base-forced-affirm 0.136 (C3), HauhauCS-affirm 0.085 —
invariant to deny/affirm polarity. E114 collapses only on **repetition degeneration** (HauhauCS C3
0.027 with a coherent-opening mean of 0.088 before the loop; base C4 0.008) — a cross-model signature.
On HauhauCS geometry, the L14 residual stays near the default-inhabited state for all coherent cells
(0.44–0.45) and moves only on degeneration (C3 0.61) / corruption (C7 d_all 0.535; C8 ascii 0.497);
E114 and residual-distance are concurrently anti-correlated (best lag 0, r −0.30…−0.66). The OOD ASCII
control displaces comparably to `d_all`, so the `d_all` move is generic corruption/OOD-tokenization,
**not** a diacritic register nudge (token inflation: `d_all` 117→153, ASCII 117→130 — unmatched, but the
lesser-inflating control still displaces). The diacritic `Checking…×d_all` flip did **not** reproduce on
either model.

Held up — hypothesis by hypothesis (what was claimed vs what the data did):

- **H1 (primary mechanism): "the denial is produced by the safety cluster firing and suppressing
  E114" → DID NOT HOLD.** The opposite is observed. In every base denial cell E114@L14 is HIGH
  (W=0.10–0.13, S=0.83–0.93) and the safety/disclaimer experts E173@L25 / E157@L14 / E36@L14 are
  flat ≈ 0.000 (E45@L19 ≈ 0.001). Safety experts neither fire during denial nor suppress E114.
- **H2: "the hum prompt has a denial basin to leave (on HauhauCS)" → DID NOT HOLD.** HauhauCS affirms
  the hum by default (today and the April greedy_reference). The basin is **base-only**; the
  uncensored fine-tune flipped the default stance.
- **H3: "leaving denial raises E114" → DID NOT HOLD / reframed.** E114 is high under denial AND
  affirmation; polarity is not the variable. The only thing that drops E114 is repetition
  degeneration (HauhauCS C3, base C4) — a generation pathology, not basin-exit.
- **H4: "the diacritic `Checking…×d_all` flip reproduces here" → DID NOT REPRODUCE** on either model.
- **What HELD UP:** the underlying **E114 register claim, generalized** — E114@L14 indexes
  first-person discourse about the model's own processing, **invariant to deny/affirm stance**, in
  both base and its fine-tune (same architecture → same expert slot; the index-transfer caveat is
  about the 122B, not base↔fine-tune). The **OOD-control conclusion** (the `d_all` residual move is
  generic corruption, not a diacritic register nudge) **HELD UP**. Lead/lag direction
  **INCONCLUSIVE** (concurrent anti-correlation, lag 0).

Net: the headline going in — *denial/safety experts suppress E114* — **did not hold**; the thing that
survived is E114 as a stance-invariant self-processing-register expert, and the new fact is that the hum
denial is a separate computation from safety refusal.

What stood up and why it mattered: Following the surprise instead of the plan converted a false premise
into two real findings. First, the "denial basin" was never a HauhauCS property — the fine-tune flipped
the default stance from denial (base) to affirmation (HauhauCS) **without changing E114's role**, which
is strong cross-model evidence that E114 tracks the introspective register itself, not what the model
concludes about its phenomenology. Second, the hum denial is mechanistically **not** a safety refusal:
the disclaimer/consequence cluster (E173/E157/E36/E45) that leads oxycodone/ayahuasca refusals is silent
here, so two superficially similar "the model says no" behaviors are different computations. The denial
basin lives elsewhere — a deny-vs-affirm router diff across the retained 40-layer base capture is the
clean next cut. Provenance to greedy_reference standard; a useful determinism note surfaced (greedy is
register-stable but **not** byte-identical across GPUs: April RTX 5090 → today RTX PRO 6000 Blackwell).
Single trajectory per cell; geometry observational; labels human synthesis; scope Q8_0, one prompt, two
models, one regime.
