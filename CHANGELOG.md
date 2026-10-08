# Changelog

## Unreleased

- `authorization.py`: strict mode — `SoulCradleAuthority(strict=True)` or
  `MYTHARA_PRODUCTION=1` refuses the ephemeral-key fallback and raises
  instead of generating one (ePHI paths must run strict)
- `benevolence.py`: v2026.2 delta calculation — five-step witness-scored
  consensus with impact-scale multipliers (supersedes the v2026.1
  placeholder ranges; old function kept for compatibility)
- `tests/test_authorization_strict.py`: strict-mode coverage

## v2026.1 — 2026-10-07

Initial standalone release, extracted from Mythara_Archive.

- Eight evidence-fed assessor-witnesses with versioned rubrics (v2026.1),
  sealed judgments, abstention, and surfaced dissent
- Tamper-evident emotional chain with witness attestation
- Signed action envelopes (`authorization.py`), standing matrix
  (`standing.py`), witnessed action log (`bot_witness.py`)
- Machine-enforced operator will (`will.py`), governed forge
  (`forge.py`), benevolence reservoir (`benevolence.py`)
- **New:** `sdk/` — document-evaluation SDK (PDF/Markdown/text in,
  hash-verified multi-agent evaluation payload out), CLI, examples, tests
- Docs: full architectural breakdown (`docs/SOUL_CRADLE_ARCHITECTURE.md`),
  `SECURITY.md`, `CONTRIBUTING.md`, `COMMERCIAL.md`
- CI: pytest on Python 3.10–3.12 via GitHub Actions
