"""Soul Cradle document-evaluation SDK.

Send a document (PDF, Markdown, or text); get back a hash-verified,
multi-agent evaluation payload: the eight assessor-witnesses hear the
action "rely on this document," judge it on observed evidence, and seal
every judgment. Verify the payload any time with
``soul_cradle_sdk.verify_payload``.

The honest contract: the payload proves the evaluation is UNALTERED, not
that the document is TRUE. Witnesses attest what they observed in the
document — they never claim to verify its claims.
"""

from .evaluate import evaluate_document, evaluate_text
from .verify import verify_payload

__version__ = "2026.1"
__all__ = ["evaluate_document", "evaluate_text", "verify_payload"]
