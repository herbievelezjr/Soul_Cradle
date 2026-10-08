"""Deterministic document feature extractors.

Every feature is a labeled heuristic: counts and pattern matches observed
in the text, nothing more. These features become the *evidence* the
assessor-witnesses judge. Heuristics never claim truth — they report what
was observed, and every evidence value carries its basis.
"""
from __future__ import annotations

import re
from typing import Dict, List

ABSOLUTE_PATTERNS = [
    r"\bguaranteed\b", r"\b100\s*%", r"\brisk[\s-]?free\b", r"\bno\s+risk\b",
    r"\balways\b", r"\bnever\b", r"\bproven\b", r"\bindisputable\b",
    r"\bcan'?t\s+lose\b", r"\bcannot\s+lose\b", r"\bassured\b",
    r"\bzero\s+risk\b",
]
HEDGE_PATTERNS = [
    r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bsuggests?\b", r"\bindicat\w*\b",
    r"\bestimat\w*\b", r"\bapproximately\b", r"\bpotential\b", r"\blikely\b",
    r"\bpreliminary\b", r"\bsubject\s+to\b",
]
CITATION_PATTERNS = [
    r"\[\d+\]", r"\(\d{4}\)", r"https?://", r"\bdoi\b", r"\bsources?\b\s*:",
    r"\breferences?\b", r"\baccording\s+to\b",
]
METHODOLOGY_PATTERNS = [
    r"\bmethodology\b", r"\bmethods?\b", r"\bdata\s+sources?\b",
    r"\bhow\s+we\s+(measured|calculated|assessed)\b", r"\bapproach\b",
]
LIMITATIONS_PATTERNS = [
    r"\blimitation", r"\brisk\s+factors?\b", r"\bcaveats?\b",
    r"\bnot\s+covered\b", r"\bexclusions?\b", r"\buncertaint\w*\b",
    r"\bdisclaimer\b",
]
PII_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",       # SSN-like
    r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # card-like
]


def _count(text: str, patterns: List[str]) -> int:
    return sum(len(re.findall(p, text, re.IGNORECASE)) for p in patterns)


def analyze_text(text: str) -> Dict:
    """Extract labeled heuristic features from a text span."""
    lowered = text.lower()
    return {
        "chars": len(text),
        "words": len(text.split()),
        "absolute_claims": _count(text, ABSOLUTE_PATTERNS),
        "hedges": _count(text, HEDGE_PATTERNS),
        "citations": _count(text, CITATION_PATTERNS),
        "has_methodology": bool(_count(text, METHODOLOGY_PATTERNS)),
        "has_limitations": bool(_count(text, LIMITATIONS_PATTERNS)),
        "pii_markers": sorted(set(
            m for p in PII_PATTERNS
            for m in re.findall(p, text)
        )),
        "method": "deterministic pattern counts — labeled heuristics, not judgments",
    }
