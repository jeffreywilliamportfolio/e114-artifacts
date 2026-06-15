# JOURNAL — All-40-Layer SAE Feature Dictionary & the Dog Empathy Run

Model: `Qwen/Qwen3.5-35B-A3B-Base` (BF16 for the SAE side). SAE family:
`Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50` — per-layer Qwen-Scope SAEs `layer{0..39}.sae.pt`,
width **32768**, TopK-50, read on `resid_post` = HF `hidden_states[L+1]`. All work 2026-06-01 on Vast
H200 `38961723` ($4.393/hr), **destroyed after artifact verification (active instances = 0)**. Greedy /
TopK-50 fixed throughout. This journal is the SAE-dictionary line and its first consumer (the "dog"
empathy axis); it is **distinct from the E114/L14 routing line** (`JOURNAL-E114-CHARACTERIZATION.md`) —
SAE feature indices are per-layer and do not transfer across layers or to the routing-expert story.

Verdict vocabulary: `Held up` · `Partly held` · `Did not hold` · `Archive/provenance/design only`.

---

### 1. Built the all-40-layer SAE feature dictionary (3-stage pipeline): `sae_featmap_all40`

**What was done.** A from-scratch dictionary of **every** Qwen-Scope feature across all 40 layers
(40 × 32768 = **1,310,720 features**). Three stages, scripts `run-staging/scripts/sae_featmap_stage{1,2,3}*.py`,
master `sae-tests/runs/sae_featmap_all40/sae_feature_map_all40.labeled.csv` (schema `feature_id, layer,
label, category, logit_lens_top_tokens, fire_rate, top_examples, observation, source_run, confidence`;
`observation` left blank for hand-fill). Raw CSV out of git; README + summaries in that run dir.

- **Stage 1 — logit-lens** (`stage1_logitlens.py`): per layer `lm_head @ (W_dec[:,f] * norm_w)`
  (norm = `model.language_model.norm.weight`), top-20 promoted tokens/feature. `d_model=2048`,
  `vocab=248320`. ~45 s for all 1.31 M rows. **Validated against the hand-curated L14 log**
  (`SAE_FEATURE_MAP.csv`): 4310 (才不会/刹那间/一念 non-dual), 2961 (whitespace filler), 11006
  (Buddha/Buddhist), 26050 (Kafka/Nietzsche/existential), 13119 (大脑/cognition) all reproduce exactly.
- **Stage 2 — activation profiling** (`stage2_profile.py`, **BF16**, all layers one forward pass):
  corpus = **1,005,548 tokens** (505,434 EN FineWeb `sample-10BT` + 500,114 ZH FineWeb-2 `cmn_Hani` +
  the 16 dog prompts), 1,969 windows @512. Per feature: `fire_rate` (fraction of tokens in the token's
  top-50, val>0) + top-8 max-activating example snippets. **Fire-rate is heavy-tailed and the signal is
  inverted from what's interesting:** ≥1e-3 → 344,322 · ≥5e-3 → 90,437 · ≥1e-2 → 35,873 · ≥5e-2 → 2,140.
  The *highest*-fire features are generic (the top tokens are all whitespace/delimiter `punctuation-format`,
  e.g. feature 2938 at fire 0.75–0.90 across L25–30); the *semantic* features are **rare** — God-feature
  4310@L14 fires at **1.2e-4**, Buddhist 11006@L14 at **1.6e-4**.
- **Stage 3 — gated auto-interp, SELF-LABELED by fanned-out subagents** (`stage3_harness.py` + a
  `sae-stage3-label` workflow, **no external API/key**): gate `fire_rate > 0.03` → **5,410 features** →
  51 layer-grouped chunks (block 150) + 1 supplementary (63 stragglers dropped by their agents, recovered
  in a SUPP pass). **52 subagents** each read their chunk's lens-tokens + examples and wrote a CSV
  fragment; merged into the master. Fixed 13-term category vocab (`lexical-token, morphology,
  script-language, punctuation-format, syntax-function, entity-proper, topic-domain, concept-abstract,
  affect-register, discourse-reference, code-technical, numeric-unit, noise-mixed`); sub-threshold
  **1,305,310** → `low-fire-unlabeled`. Idempotent (rerun skips chunks with an existing fragment).

**Results.** Labeled tier distribution: **noise-mixed 31.1%** · punctuation-format 15.0% ·
syntax-function 12.8% · topic-domain 10.6% · affect-register 6.4% · morphology 5.2% · lexical-token 4.3% ·
discourse-reference 4.1% · concept-abstract 3.6% · entity-proper 3.4% · script-language 1.5% ·
code-technical 1.3% · numeric-unit 0.7%. Confidence **high 1507 / med 1418 / low 2485**. A clean depth
trend (the category × layer heatmap): **`noise-mixed` collapses from ~40% in early layers to ~10% by
L39**, while topic/affect/concept *grow* with depth — features get more interpretable and more semantic
deeper in the stack.

**Verdict: Held up — as infrastructure/method. The labels are interpretive synthesis, not ground truth
(Archive/design + usable reference).**
- **The pipeline works and Stage 1 is validated** (reproduces the curated L14 features bit-for-bit).
- **Hard seam (state it out loud): the fire-rate gate selects the generic backbone, NOT the
  interesting features.** 31% noise-mixed + 46% low-confidence is honest — high-fire base features are
  heavily polysemantic. The rare semantic carriers (E114/God/empathy-type, ~1e-4) sit *below* 0.03 and
  stay `low-fire-unlabeled`; they must be interpreted **in-context** by the run that recruits them, not
  read off this dictionary. The dictionary is a lookup/backbone map, not a discovery tool for rare
  concepts.
- Single corpus, single profiling pass; `fire_rate` is corpus-dependent; subagent labels are short
  synthesis over lens+examples. Expand later by lowering the threshold (idempotent re-chunk + rerun).

---

### 2. Dog empathy/lexical run — the identity-vs-empathic contrast method: `sae_featmap_all40/empathy`

**What was done.** Captured the 9 empathy + 7 lexical "dog" probes (`dog/prompts-{empathy,lexical}-unmatched.json`)
through the **BF16 base** model, all-40-layer SAE encode (TopK-50), via
`run-staging/scripts/sae_featmap_empathy_capture.py`. Prompts are **token-matched & verified**: every
target is a single token (plant/fish/bird/cat/dog/horse/ox/friend/child), the empathy skeleton is
uniformly 20 tokens (raw) / 30 tokens (chat-wrapped), divergence only at the target slot; the distress
word was changed `dehydrated → weak` (user decision) so no cell is aquatically OOD. Anchors (chat-wrapped
positions): empathy `target 7 / love 10 / them 11 / weak 17 / do 22`; lexical `target 4 / they 9 / all 22`.
Outputs `sae-tests/runs/sae_featmap_all40/empathy/{anchor_activations.csv (132,000 rows),
probe_features.csv (511,524 rows), meta.json}`. The intended contrast (from the prompt design): per layer,
join on target — **identity = empathy ∩ lexical** (shared across affect-laden and affect-stripped frames),
**empathic = empathy − lexical** (present only when care is in the prompt).

**Results (observational, single greedy trajectory per cell — point estimate).** The contrast **method
works and surfaces sensible features**. At **dog / L14**: |empathy| = 752, |lexical| = 828,
**identity (∩) = 345, empathic (A−B) = 407**. The top empathy-frame-only features at the dog target are
exactly the predicted bond/distress carriers, read by their logit-lens:
- **f6970** — lens `爱的 | incond | love | Love | dearly | ❤ | loves` → a **love/affection** feature.
- **f6812** — lens `弱的 | …` → the **"weak"/distress** feature.
Both are `low-fire-unlabeled` in the general-corpus dictionary (they're rare) — the **A−B contrast
recovered them where the dictionary's fire-rate gate could not.** This is the central methodological
confirmation: matched empathy/lexical contrast surfaces interpretable empathy features that the
backbone dictionary leaves unlabeled.

**Verdict: Archive / design + method demonstrated. The headline science question is NOT yet answered.**
- **The contrast pipeline and the "interpret-in-context" loop are validated** (Partly held: the *method*
  surfaces love/weak as empathic at L14, as designed).
- **NOT done:** the actual research question — *does feeling-with generalize over the kind-of-mind, or do
  empathic features climb with attributed inner life (plant→child)?* — has **no verdict yet.** We have
  the captured data + an explorer, but: one greedy trajectory per cell (no significance), the
  ladder-climb (Spearman of activation vs attributed-mind rank), the identity-vs-empathic-by-depth
  curve, and an OOD/non-register control are **not yet computed/reported.** Do not read "love/weak
  surface at L14" as an answer to the ladder question.

---

### 3. Interpretation tooling — Datasette + the "SAE Atlas" app: `dog/`

**What was done.** Because **every off-the-shelf SAE viewer is walled off by the model**: SAEDashboard /
sae_vis / Neuronpedia all require TransformerLens' `HookedTransformer`, and **TransformerLens has no
support for Qwen3.5-35B-A3B** (MoE + linear-attention). Our exact SAE set is also not on hosted
Neuronpedia. So all viz was built directly on our own activation/lens data (no TransformerLens):
- **Datasette** over `dog/featmap.db` (5,410 labeled) + `dog/featmap_full.db` (full 1.31 M, FTS on
  lens-tokens) — tabular browse/facet/search.
- **"SAE Atlas" — a Vite + React + shadcn/ui app** (`dog/sae-ui/`, dark, Geist): **Features** (searchable
  list + per-feature dashboard: lens chips, fire-rate, top examples with the firing token highlighted),
  **Graph** (force-directed knowledge graph — 5,410 nodes / 6,482 edges, `react-force-graph-2d`, edges =
  kNN logit-lens-token cosine ≥ 0.42, drag/zoom/filter), **Overview** (category×layer heatmap, category
  bar, fire-rate survival). Static charts in `dog/feature_map_viz/*.png`.

**Verdict: Archive / design only (tooling).**
- The **Graph edges are a logit-lens-token-similarity proxy**, *not* decoder-cosine (the principled SAE
  feature-direction similarity). The decoder-geometry atlas/graph is the upgrade; it needs a fresh box.
- The richer per-feature dashboard data (activation **histogram** + full per-token colour gradient + neg
  logits) was **not produced**: the generator was pathologically slow loading all 40 decoder matrices as
  float upfront and was killed (v2 = defer the decoder loads). Current dashboards highlight the firing
  token only.

---

### Process & failure notes (failure-aware record)

- **TransformerLens does not support Qwen3.5-35B-A3B** → the standard SAE-dashboard ecosystem
  (SAEDashboard/sae_vis/Neuronpedia-export) cannot run on this model without porting the architecture.
  Pivoted to bespoke viz over our own HF activations. *Lesson: for non-TL architectures, generate the
  dashboard data yourself; the tools assume TL.*
- **Streamlit prototypes (built first) were rejected on aesthetics** → rebuilt as the shadcn app.
- **The H200 was flaky on restart** — after parking it twice it came back `exited` with SSH refused;
  destroyed it. The decoder-geometry UMAP/graph was deferred and replaced with the local lens-token
  proxy. *Lesson: parked Vast instances still bill storage ($0.13/hr) and may not restart cleanly;
  destroy when the queued work is local.*

### Provenance & teardown

- Scripts: `run-staging/scripts/sae_featmap_stage{1,2,3}*.py`, `sae_featmap_empathy_capture.py`,
  `build_corpus_mixed.py`; app + data generators under `dog/sae-ui/` (`prep_data.py`, `build_map.py`,
  `build_graph.py`). Workflow `sae-stage3-label`.
- Data (local, out of git): `sae-tests/runs/sae_featmap_all40/` — `sae_feature_map_all40.labeled.csv`
  (1.31 M), `labeled_only.csv` (5,410), `empathy/` (capture), `*.stage{1,2}_summary.json`, `README.md`.
- Curated L14 log `SAE_FEATURE_MAP.csv` was **not clobbered** — the all-40 master is a separate file.
- **Box `38961723` destroyed; active instances = 0.** All outputs verified local before teardown.
