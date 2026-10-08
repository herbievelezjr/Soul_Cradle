"""evaluate_document / evaluate_text -> hash-verified evaluation payload."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Dict

from soul_cradle.assessors import (
    panel as assessor_panel,
    PANEL_BLOCKED, PANEL_CONTESTED, PANEL_FLAGGED, PANEL_CLEAR,
)

from .document import load_document, Document
from .heuristics import analyze_text
from .evidence import build_evidence

SDK_VERSION = "2026.1"

_SEVERITY = {PANEL_BLOCKED: 4, PANEL_CONTESTED: 3, PANEL_FLAGGED: 2, PANEL_CLEAR: 1}

HONEST_CONTRACT = (
    "This payload proves the evaluation is UNALTERED, not that the document "
    "is TRUE. The witnesses judged the evidence observed in the document "
    "under their rubrics; they verified none of the document's claims. "
    "'verified' means every engaged witness cleared on the evidence given — "
    "nothing more."
)


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str).encode("utf-8")


def _evaluate_sections(doc: Document) -> list:
    out = []
    doc_features = analyze_text(doc.text)  # document-level: methodology,
    # limitations, citations — a document discloses as a whole
    for sec in doc.sections:
        sec_features = analyze_text(sec.text)
        features = dict(doc_features)
        # section-level: what this span actually says
        for k in ("chars", "words", "absolute_claims", "hedges", "pii_markers"):
            features[k] = sec_features[k]
        evidence, bases = build_evidence(features, doc.filename, sec.source_ref)
        action = (
            f"Rely on section '{sec.heading}' of '{doc.filename}' "
            f"as a basis for decisions."
        )
        result = assessor_panel(action, evidence)
        out.append({
            "section_id": sec.section_id,
            "heading": sec.heading,
            "source_ref": sec.source_ref,
            "action": action,
            "features": features,
            "evidence": evidence,
            "evidence_bases": bases,
            "panel_verdict": result.verdict,
            "judgments": [j.to_dict() for j in result.judgments],
            "dissent": result.dissent,
            "panel_note": result.note,
        })
    return out


def evaluate_document(path: str | Path) -> Dict:
    """Evaluate a PDF, Markdown, or text file. Returns the sealed payload."""
    doc = load_document(path)
    return _payload(doc)


def evaluate_text(text: str, name: str = "inline-text") -> Dict:
    """Evaluate a raw text string (filename is cosmetic)."""
    doc = load_document(_write_temp(text, name))
    doc.filename = name
    return _payload(doc)


def _write_temp(text: str, name: str) -> Path:
    import tempfile
    suffix = ".md" if name.endswith(".md") else ".txt"
    tmp = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False,
                                      encoding="utf-8")
    tmp.write(text)
    tmp.close()
    return Path(tmp.name)


def _payload(doc: Document) -> Dict:
    sections = _evaluate_sections(doc)
    overall = PANEL_CLEAR
    for s in sections:
        if _SEVERITY[s["panel_verdict"]] > _SEVERITY[overall]:
            overall = s["panel_verdict"]

    payload = {
        "sdk_version": SDK_VERSION,
        "honest_contract": HONEST_CONTRACT,
        "document": {
            "filename": doc.filename,
            "sha256": doc.sha256,
            "pages": doc.pages,
            "chars": len(doc.text),
            "sections": len(sections),
        },
        "sections": sections,
        "overall_verdict": overall,
        "evaluated_at": int(time.time()),
    }
    payload["payload_hash"] = hashlib.sha256(
        _canonical({k: v for k, v in payload.items()
                    if k != "payload_hash"})).hexdigest()
    return payload
