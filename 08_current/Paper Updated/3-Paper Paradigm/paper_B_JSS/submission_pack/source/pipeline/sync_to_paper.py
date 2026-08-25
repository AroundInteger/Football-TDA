#!/usr/bin/env python3
"""Validate Paper B LaTeX numbers against pipeline/outputs/numbers.json."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
PAPER_DIR = PIPELINE_DIR.parent
SECTIONS = PAPER_DIR / "sections"
NUMBERS_PATH = PIPELINE_DIR / "outputs" / "numbers.json"


def check(name: str, expected, tex: str, pattern: str, group: int = 1) -> bool:
    if expected is None:
        print(f"  SKIP {name}")
        return True
    m = re.search(pattern, tex)
    if not m:
        print(f"  FAIL {name}: pattern not found")
        return False
    if group == 0:
        print(f"  OK {name}")
        return True
    found = m.group(group).replace(",", "").replace("{,}", "")
    try:
        ok = abs(float(expected) - float(found)) <= max(0.02, 0.01 * abs(float(expected)))
    except ValueError:
        ok = str(expected) == found
    print(f"  {'OK' if ok else 'MISMATCH'} {name}: pipeline={expected} tex={found}")
    return ok


def main() -> None:
    if not NUMBERS_PATH.exists():
        print(f"ERROR: run pipeline first ({NUMBERS_PATH})")
        sys.exit(1)
    with open(NUMBERS_PATH) as f:
        data = json.load(f)
    h = data.get("headline", {})
    tex = "\n".join(p.read_text() for p in SECTIONS.glob("*.tex"))

    print("=== sync_to_paper: Paper B ===")
    ok = True
    ok &= check("event_pairs", h.get("event_topology_pairs"), tex, r"104\{,}722", group=0)
    ok &= check("auc_baseline", h.get("auc_baseline"), tex, r"0\.693", group=0)
    ok &= check("auc_topology", h.get("auc_with_topology"), tex, r"0\.687", group=0)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
