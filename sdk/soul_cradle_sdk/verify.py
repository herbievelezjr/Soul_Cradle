"""Independent verification of an evaluation payload."""
from __future__ import annotations

import hashlib
import json
from typing import Dict, Tuple

from soul_cradle.assessors import AssessorJudgment, verify_judgment


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str).encode("utf-8")


def verify_payload(payload: Dict) -> Tuple[bool, Dict]:
    """Re-verify a payload: payload seal, then every witness judgment seal.

    Returns (ok, details). Any tampering — edited text, forged judgment,
    altered verdict — fails.
    """
    details: Dict = {"sections": len(payload.get("sections", [])),
                     "failures": []}

    expect = hashlib.sha256(
        _canonical({k: v for k, v in payload.items()
                    if k != "payload_hash"})).hexdigest()
    if payload.get("payload_hash") != expect:
        details["failures"].append({"reason": "payload seal mismatch — tampered"})
        details["ok"] = False
        return False, details

    for s in payload.get("sections", []):
        for j in s.get("judgments", []):
            try:
                obj = AssessorJudgment(**{
                    k: v for k, v in j.items()
                    if k in AssessorJudgment.__dataclass_fields__
                })
            except TypeError as e:
                details["failures"].append({
                    "section": s.get("section_id"),
                    "reason": f"judgment malformed: {e}"})
                continue
            if not verify_judgment(obj):
                details["failures"].append({
                    "section": s.get("section_id"),
                    "reason": (f"witness {j.get('assessor_id')} judgment seal "
                               f"mismatch — forged")})
    details["ok"] = not details["failures"]
    return details["ok"], details
