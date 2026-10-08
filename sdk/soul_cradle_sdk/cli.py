"""Command line: python -m soul_cradle_sdk.cli document.pdf [--out result.json]"""
from __future__ import annotations

import argparse
import json
import sys

from .evaluate import evaluate_document
from .verify import verify_payload


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Evaluate a document with the Soul Cradle witness panel.")
    ap.add_argument("document", help="PDF, Markdown, or text file")
    ap.add_argument("--out", help="write the JSON payload to this file")
    ap.add_argument("--compact", action="store_true",
                    help="one-line verdict output")
    args = ap.parse_args(argv)

    try:
        payload = evaluate_document(args.document)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    ok, _ = verify_payload(payload)
    doc = payload["document"]
    if args.compact:
        print(f"{payload['overall_verdict']}  {doc['filename']}  "
              f"payload_hash={payload['payload_hash'][:16]}...  verified={ok}")
    else:
        print(f"Document : {doc['filename']} "
              f"(sha256 {doc['sha256'][:16]}..., {doc['pages']} page(s), "
              f"{doc['sections']} section(s))")
        print(f"Overall  : {payload['overall_verdict']}")
        for s in payload["sections"]:
            flagged = [j["assessor_id"] for j in s["judgments"]
                       if j["verdict"] == "flagged"]
            print(f"  [{s['section_id']}] {s['panel_verdict']:9s} "
                  f"{s['heading'][:60]}"
                  + (f"  flagged by: {', '.join(flagged)}" if flagged else ""))
        print(f"Seal     : payload_hash={payload['payload_hash'][:16]}... "
              f"verified={ok}")
        print("Contract : " + payload["honest_contract"][:80] + "...")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, default=str)
        print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
