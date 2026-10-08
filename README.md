# Soul Cradle

[![ci](https://github.com/herbievelezjr/Soul_Cradle/actions/workflows/ci.yml/badge.svg)](https://github.com/herbievelezjr/Soul_Cradle/actions/workflows/ci.yml)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/herbievelezjr/Soul_Cradle/blob/main/sdk/Soul_Cradle_SDK_Demo.ipynb)

**A deterministic trust layer for multi-agent AI systems.**
Version 2026.1 · Pre-revenue research prototype · Built by Herb Velez, Mythara Labs LLC

> Every consequential act is heard by a panel of specialized assessors, judged
> against versioned rubrics over observable evidence, and sealed into a
> tamper-evident record. If the witnesses cannot clear the evidence, the act
> does not happen.

Extracted from [herbievelezjr/Mythara_Archive](https://github.com/herbievelezjr/Mythara_Archive),
where the original copies remain as built. Full architectural breakdown:
[`docs/SOUL_CRADLE_ARCHITECTURE.md`](docs/SOUL_CRADLE_ARCHITECTURE.md).

## The honest contracts

- **Tamper-evidence ≠ truth.** Hash chains prove the record is *unaltered*, never that it is *true*.
- **Witnesses observe, never claim.** Assessors attest only what they observed in the evidence.
- **Fail closed.** Missing evidence is itself a finding. A critical-severity finding blocks the action.
- **Abstention over guessing.** An assessor whose domain is not engaged *declines to judge*.
- **Dissent is the signal.** Conflicting verdicts are preserved and reported — never averaged away.

## The eight witnesses

| Assessor | Domain question |
|---|---|
| Demeter | Long-term interests vs short-term extraction |
| Dionysus | Uncontrolled variance introduced |
| Eros | Principal relationship preserved or strengthened |
| Hades | Hidden costs, externalities, unseen risks |
| Hermes | Communication boundaries, deception |
| Janus | Consistency with past commitments, precedent |
| Nemesis | Fairness to all parties, proportionality |
| Persephone | Reversibility, safety on repetition |

Panel verdicts: `clear` · `flagged` · `contested` (dissent surfaced in full) · `blocked`
(any critical finding — one critical witness is enough; the panel does not outvote it).

## Quickstart

```python
from soul_cradle.assessors import panel

evidence = {
    "principal_consent": True,
    "fully_disclosed": True,
    "deception_involved": False,
    "reversible": True,
    "variance": "low",
    "safe_on_repetition": True,
    "sustains_long_term": True,
    "hidden_costs_addressed": True,
    "strengthens_relationship": True,
    "contradicts_commitments": False,
    "precedent_setting": False,
    "disproportionate_harm": False,
}

result = panel("Send partnership proposal to Acme Corp", evidence)
print(result.verdict)  # "clear" | "flagged" | "contested" | "blocked"
```

Run the tests: `pytest tests/ -q`

## What is real, what is not

**Real:** eight assessors with versioned rubrics and sealed judgments; hash-chained
attested records with independent re-verification; signed action envelopes;
fail-closed operator will; witnessed action log; benevolence reservoir with
escalation tiers. Deterministic core — zero LLM calls inside the trust boundary.

**Not claimed:** no claim of moral truth or correctness — only attested process.
No blockchain. No production key management yet (KMS/HSM is the documented path).
Not certified for regulated data; no compliance claims are made.

## Layout

- `soul_cradle/` — the framework (`assessors.py`, `emotional_chain.py`,
  `authorization.py`, `standing.py`, `bot_witness.py`, `will.py`, `forge.py`,
  `benevolence.py`, `pantheon.py`, `identity.py`, `health.py`)
- `tests/` — focused test suite
- `docs/SOUL_CRADLE_ARCHITECTURE.md` — full architectural breakdown

## License

Source-available — see [LICENSE.md](LICENSE.md). Copyright © 2025 Herbert Velez Jr.
Mythara Labs LLC (Colorado domestic LLC, filed 2026-10-04; CO SOS ID #20268239831).

**In plain English:** you may read, evaluate, and run the tests. Production
use, distribution, and sublicensing require a signed written agreement —
see [COMMERCIAL.md](COMMERCIAL.md) for tiers and how to start. Copyright
stays with Herbert Velez Jr. This summary is explanatory only; `LICENSE.md`
controls, and none of this is legal advice.

## Document-evaluation SDK

**PDF in, hash-verified multi-agent evaluation out.** The `sdk/` directory
is the enterprise on-ramp: point it at a compliance document, financial
report, or policy draft and get back a sealed payload — the eight witnesses
hear the reliance action, judge it on observed evidence, and every judgment
is content-hashed and independently verifiable. See `sdk/README.md`.

```bash
cd sdk && pip install -e .
python -m soul_cradle_sdk.cli report.pdf --out evaluation.json
```
