"""SDK tests: deterministic verdicts + payload verification."""
import json
import os
import tempfile

from soul_cradle_sdk import evaluate_text, verify_payload

CLEAN = """# Policy\n\n## Methodology\n\nWe reviewed ten cases using documented criteria [1].\nAccording to Smith (2024), outcomes vary.\n\n## Limitations\n\nSmall sample. Results are approximate and may not generalize.\n"""

RISKY = """# Memo\n\nThis fund is guaranteed to deliver 100% risk-free returns. """ \
        """It has never lost money and always wins."""


def _payload(text):
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w") as f:
        f.write(text)
    try:
        return evaluate_text(open(path).read(), name="t.md")
    finally:
        os.unlink(path)


def test_clean_document_clears():
    p = _payload(CLEAN)
    assert p["overall_verdict"] == "clear", p["overall_verdict"]
    ok, _ = verify_payload(p)
    assert ok


def test_risky_document_flagged_or_contested():
    p = _payload(RISKY)
    assert p["overall_verdict"] in ("flagged", "contested", "blocked"), \
        p["overall_verdict"]
    ok, _ = verify_payload(p)
    assert ok


def test_payload_seal_detects_tampering():
    p = _payload(CLEAN)
    p["overall_verdict"] = "blocked"  # tamper with the verdict
    ok, details = verify_payload(p)
    assert not ok
    assert details["failures"]


def test_payload_is_json_serializable():
    p = _payload(CLEAN)
    json.dumps(p, default=str)
    assert p["payload_hash"]
    assert p["document"]["sha256"]
