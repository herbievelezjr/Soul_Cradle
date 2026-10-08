# Evaluation & Known Limitations

## What the SDK was tested on

| Document | Sections | Verdict | Notes |
|---|---|---|---|
| `examples/clean_policy.md` — vendor risk review with methodology, citations, limitations | 3 | **clear** | Every engaged witness cleared on the evidence |
| `examples/risky_memo.md` — "guaranteed 100% risk-free returns," no methodology | 2 | **contested** | demeter, dionysus, hades, hermes, persephone flagged; eros, nemesis, janus cleared — dissent preserved |

`sdk/tests/test_sdk.py` asserts these verdicts deterministically and that
payload tampering is detected. Run: `pytest sdk/tests/ -q`.

## Known limitations (stated plainly)

- **Heuristics, not understanding.** Features are deterministic pattern
  counts (absolute-claim phrases, hedges, citation markers, section
  presence). They are labeled as such on every evidence value. A cleverly
  worded bad document can pass; a bluntly worded good one can flag.
- **English only.** All patterns are English regexes.
- **No OCR.** `pypdf` extracts text from text-based PDFs only. Scanned /
  image PDFs yield no text and are rejected rather than guessed at.
- **No accuracy benchmark yet.** Beyond the two example documents and the
  unit tests, there is no measured precision/recall study. That evaluation
  is open work, not a claimed result.
- **No adversarial testing.** Deliberately evasive documents (buried
  qualifications, laundered claims) have not been systematically tested.
- **Heuristic scope.** The panel judges *reliance fitness* (disclosure,
  variance, reversibility) — it does not fact-check document claims.

## What would strengthen this

A labeled corpus of real compliance/financial documents with known issues,
scored blind against the panel's verdicts, published with the misses. That
study does not exist yet; the SDK is versioned 2026.1 and its limits are
part of the interface.
