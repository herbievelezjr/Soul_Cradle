# Soul Cradle Document-Evaluation SDK

**PDF in, hash-verified multi-agent evaluation out.** v2026.1

Send a document — a compliance report, a financial memo, a policy draft —
and get back a sealed evaluation payload: the eight Soul Cradle
assessor-witnesses hear the action *"rely on this document as a basis for
decisions,"* judge it on observed evidence under their versioned rubrics,
and every judgment is sealed by content hash. Dissent is surfaced, never
averaged away.

## Install

```bash
pip install -e .        # from this directory (needs pypdf)
# or
pip install pypdf       # then run with soul_cradle/ on your PYTHONPATH
```

## Use

```bash
# Command line
python -m soul_cradle_sdk.cli report.pdf
python -m soul_cradle_sdk.cli report.pdf --out evaluation.json --compact

# Python
from soul_cradle_sdk import evaluate_document, verify_payload

payload = evaluate_document("report.pdf")
print(payload["overall_verdict"])   # clear | flagged | contested | blocked

ok, details = verify_payload(payload)  # independent re-verification
```

## What the witnesses actually check

Deterministic heuristics extract labeled features from the document
(methodology present, limitations discussed, citations, absolute claims
like "guaranteed"/"100%", qualifying hedges, PII-like markers). Those
features become the *evidence* — each value carrying its stated basis —
and the panel judges the reliance action on it. Example: a memo promising
"guaranteed risk-free returns" with no methodology gets flagged by
Dionysus (uncontrolled variance), Hades (unseen risks), Demeter
(long-term extraction), and Persephone (unsafe on repetition), while Eros,
Nemesis, and Janus clear — a **contested** verdict with the disagreement
preserved in full.

## The honest contract

The payload proves the evaluation is **unaltered**, not that the document
is **true**. Witnesses attest what they observed in the document; they
verify none of its claims. `verified` means every engaged witness cleared
on the evidence given — nothing more.

## Layout

- `soul_cradle_sdk/document.py` — PDF/Markdown/text loading + sectioning
- `soul_cradle_sdk/heuristics.py` — deterministic feature extractors
- `soul_cradle_sdk/evidence.py` — features → assessor evidence + bases
- `soul_cradle_sdk/evaluate.py` — `evaluate_document()` / `evaluate_text()`
- `soul_cradle_sdk/verify.py` — `verify_payload()`
- `soul_cradle_sdk/cli.py` — command-line interface
- `examples/` — a clean policy doc and a risky memo to try it on
- `tests/test_sdk.py` — deterministic verdict + tamper-detection tests

## License

Source-available — see `../LICENSE.md`. Copyright © 2025 Herbert Velez Jr.
