# Contributing to Soul Cradle

## Ground rules

1. **Honest claims only.** Never assert what the code cannot prove. The
   contracts in each module's docstring (tamper-evidence ≠ truth, witnesses
   observe never claim, fail closed) are load-bearing — do not weaken them
   to make a demo look better.
2. **Deterministic core stays dependency-free.** `soul_cradle/` runs with
   zero model calls and only the standard library. Keep it that way.
3. **Tests for behavior changes.** Run the suite before pushing:
   `pytest tests/test_assessors.py tests/test_emotional_chain.py tests/test_soul_cradle_math.py tests/test_standing.py sdk/tests/ -q`
4. **Version your rubrics.** Changing an assessor rubric means bumping its
   `version` (`YYYY.N`) and `effective_date` — old judgments must stay
   auditable.

## Layout

- `soul_cradle/` — the framework (stdlib only)
- `sdk/` — the document-evaluation SDK (`pip install pypdf`)
- `tests/` — framework tests; `sdk/tests/` — SDK tests
- `docs/` — architecture breakdown

## Pull requests

CI runs the self-contained suites on Python 3.10–3.12. Keep PRs small,
describe what the witnesses now see that they didn't before, and note any
rubric version bumps.
