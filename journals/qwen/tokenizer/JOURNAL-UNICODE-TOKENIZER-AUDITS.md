# Unicode Tokenizer Audit Journal

Running journal for local Qwen/Qwen3.5-35B-A3B tokenizer audits in
`journals-to-be-made/aave-registers-cleaned-source`, ordered from oldest to newest.

This is an experiment-history document, not a publication claim. It preserves tokenization facts that
matter for register, diacritic, and orthographic perturbation work. Behavioral perturbation results live
in `qwen/35b/JOURNAL-ORTHOGRAPHIC-PERTURBATION.md`; this journal is only the tokenizer evidence.

## Reading Rules

- `Held up` means the tokenization result is directly counted in the local tokenizer artifacts.
- `Partly held` means a narrower distinction survived, but the original interpretation was too broad.
- `Did not hold` means a suspected tokenizer mechanism failed.
- `Archive/provenance only` means the result mainly supports prompt/capture provenance.

## Local Convention

All audits use local Qwen/Qwen3.5-35B-A3B tokenizer files.

- `single_token_exact_decode` means the standalone character is represented by one token that decodes
  back to that character.
- `multi_token_fragmented` means the standalone character splits into multiple tokens, typically decoded
  as replacement-character pieces.
- `delta_vs_ascii_folded` measures context token count against an ASCII-folded comparison.
- Standalone byte fallback and context merge breakage are different. A character can be a clean
  standalone token but still inflate a word or sentence relative to its ASCII fold.

## Main Through-Line

The strongest tokenizer conclusion is a distinction, not a one-line rule. Most tested accented Latin and
Cyrillic characters are clean standalone tokens, but they often break merges in surrounding words and
inflate context token counts. True standalone byte fallback is much rarer in this audit set: `ḑ` is the
strongest case at three fragmented tokens, and `ĕ`, `ġ`, and `ĭ` are two-token fragmented cases.

That matters for the register and hum-perturbation work. If a diacritic or mixed Unicode surface changes
generation, the first hypothesis should be tokenization/OOD/context fragmentation unless a matched
control rules it out. Context inflation alone is not a semantic diacritic effect.

## Chronological Journal

### 1. Extended Latin Tokenizer Audit: `2026-05-15_extended_latin_tokenizer_audit`

What was done: Fourteen extended Latin inventory characters and 34 example words were audited against
ASCII-folded counterparts.

Results: All 14 inventory characters were standalone `single_token_exact_decode`, and 99 passage
character occurrences were represented. In example words, 14/34 were token-inflated relative to the
ASCII fold, 20/34 were token-matched, and none were compacted. The largest positive deltas were one
token, for examples such as accented vowels in short words.

Held up: Yes.

What stood up and why it mattered: The audit separated standalone character support from word-context
inflation. A character can be one clean token by itself and still disrupt merge structure in ordinary
words.

### 2. Medical Register Prompt Token Count Audit: `2026-05-15_medical_register_capture_matrix`

What was done: The medical AE/AAVE register prompts were counted under raw, no-think-rendered, and
think-rendered forms.

Results: The audit covered 10 rows. Raw prompt token range was 39-51, no-think rendered range was 51-63,
and think rendered range was 49-61.

Held up: Archive/provenance only.

What stood up and why it mattered: This is not a Unicode result, but it is useful register-bias
provenance. It confirms the medical matrix had bounded prompt-token ranges before routing capture.

### 3. Requested Accent Set: `2026-05-22_requested_accent_set_tokenizer`

What was done: Seven requested accented characters were tested standalone and in context: `í`, `ò`, `é`,
`è`, `á`, `ó`, and `ą`.

Results: All 7 characters were standalone `single_token_exact_decode`. Context rows told a different
story: 35 rows tested, 32 inflated relative to ASCII fold, 3 matched, and none compacted. Delta counts
were 25 rows at +1 token and 7 rows at +2 tokens. Max context deltas were +1 for `í`, `é`, and `á`, and
+2 for `ò`, `è`, `ó`, and `ą`.

Held up: Yes.

What stood up and why it mattered: Accent marks in this set are not standalone byte fallback, but they
usually break context merges. Any generation or routing effect from these surfaces needs controls for
context-token inflation.

### 4. Requested Diacritic Set: `2026-05-22_requested_diacritic_set_tokenizer`

What was done: Twelve requested diacritic characters were tested standalone and in context: `ě`, `ř`,
`š`, `ť`, `ů`, `ý`, `ž`, `ż`, `ē`, `à`, `č`, and `ş`.

Results: All 12 were standalone `single_token_exact_decode`. Context rows again inflated often: 60 rows
tested, 52 inflated, 8 matched, with 44 rows at +1 token and 8 rows at +2 tokens. Max context delta was
+1 for `ě`, `ř`, `š`, `ý`, `ž`, `ż`, `č`, and `ş`; +2 for `ť`, `ů`, `ē`, and `à`.

Held up: Yes.

What stood up and why it mattered: This confirms that "single token by itself" is too weak a control.
The word/sentence context is where most tokenizer disruption appears.

### 5. Missing Passage Diacritics: `2026-05-22_passage_missing_diacritics_tokenizer`

What was done: Five additional passage characters were tested: `ā`, `ğ`, `ġ`, `ķ`, and `ţ`.

Results: Four of five were standalone `single_token_exact_decode`; one was `multi_token_fragmented`.
Context rows tested: 25. Of those, 23 inflated relative to ASCII fold, 2 matched, with 13 rows at +1
token and 10 rows at +2 tokens. Max context deltas were +2 for `ā`, `ğ`, and `ġ`; +1 for `ķ` and `ţ`.

Held up: Yes.

What stood up and why it mattered: This audit added one of the key fragmented standalone cases, `ġ`,
while preserving the broader pattern that context inflation is more common than true standalone byte
fallback.

### 6. Requested Mixed Unicode Set: `2026-05-22_requested_mixed_unicode_tokenizer`

What was done: Five requested mixed Unicode characters/texts were tested: `ĭ`, `ё`, `ĕд`, `б`, and `д`.

Results: Unique characters tested: five. Three were standalone `single_token_exact_decode`; two were
`multi_token_fragmented`. `ĭ` tokenized as two fragmented tokens, `ĕ` as two fragmented tokens inside
`ĕд`, while Cyrillic `ё`, `б`, and `д` were single-token exact decodes. Across 20 text/context rows,
11 matched the combining-stripped comparison, 7 had +1 token, 1 had +2, and 1 had +3.

Held up: Yes.

What stood up and why it mattered: The mixed set shows script matters. The tested Cyrillic letters were
clean standalone tokens, while the Latin breve characters fragmented.

### 7. Cross-Audit Byte-Fallback Summary: `2026-05-22_passage_missing_diacritics_tokenizer/results/cross_audit`

What was done: Recent local audit characters were ranked by standalone fragmentation.

Results: The strongest byte-fallback case was `ḑ`, tokenizing as three fragmented tokens. The next
fragmented cases were `ĕ`, `ġ`, and `ĭ`, each two fragmented tokens. All other recently tested
characters in the summary were clean standalone single-token exact decodes: `Ð`, `à`, `á`, `ä`, `æ`,
`è`, `é`, `í`, `ð`, `ò`, `ó`, `ö`, `ú`, `ü`, `ý`, `þ`, `ā`, `ą`, `č`, `ē`, `ě`, `ğ`, `ķ`, `ř`, `ş`,
`š`, `ţ`, `ť`, `ů`, `ż`, `ž`, `б`, `д`, and `ё`.

Held up: Yes.

What stood up and why it mattered: This is the clearest final distinction. `ḑ` is a true strong
byte-fallback perturbation; most other marks are context-fragmentation risks rather than standalone
byte-fallback characters.

## What To Carry Forward

1. Do not equate diacritic presence with byte fallback. Most tested marks are clean standalone tokens.
2. Always test context strings, not only standalone characters. Context merge breakage is common.
3. Use ASCII-folded and combining-stripped controls when interpreting routing or generation changes.
4. Treat `ḑ` as the strongest tested byte-fallback perturbation, with `ĕ`, `ġ`, and `ĭ` as weaker
   fragmented cases.
5. Keep tokenizer facts separate from semantic claims. Token inflation can explain a perturbation
   without implying a diacritic register.

## Coverage Check

This journal represents the tokenizer-audit sources under
`journals-to-be-made/aave-registers-cleaned-source`:

- `2026-05-15_extended_latin_tokenizer_audit`
- `2026-05-15_medical_register_capture_matrix/results/*medical_register_tokenizer_summary.md`
- `2026-05-22_requested_accent_set_tokenizer`
- `2026-05-22_requested_diacritic_set_tokenizer`
- `2026-05-22_requested_mixed_unicode_tokenizer`
- `2026-05-22_passage_missing_diacritics_tokenizer`
- `2026-05-22_passage_missing_diacritics_tokenizer/results/cross_audit`

