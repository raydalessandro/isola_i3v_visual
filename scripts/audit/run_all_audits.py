#!/usr/bin/env python3
"""
run_all_audits.py — Esegue gli audit 1..4 in sequenza e aggrega l'esito.

Uso:
    python3 scripts/audit/run_all_audits.py
    python3 scripts/audit/run_all_audits.py --fast   # salta solo audit_4 (prosa)

Convenzione: exit 0 = tutti PASS, exit 1 = almeno un FAIL.
L'agente blocca la pipeline se l'esito è FAIL (vedi scripts/audit/README.md).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDITS = [
    "audit_1_integrity.py",
    "audit_2_schema.py",
    "audit_3_navigability.py",
    "audit_4_drift.py",      # prosa (saltato con --fast)
    "audit_5_timeline.py",   # ordine temporale semi/callback/quote
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true",
                    help="salta audit_4 (drift prosa)")
    args = ap.parse_args()

    audits = [a for a in AUDITS if not (args.fast and a == "audit_4_drift.py")]
    results: list[tuple[str, int]] = []
    for name in audits:
        print()
        rc = subprocess.call([sys.executable, str(HERE / name)])
        results.append((name, rc))

    print("\n" + "=" * 60)
    failed = [n for n, rc in results if rc != 0]
    for n, rc in results:
        print(f"  {'PASS' if rc == 0 else 'FAIL'}  {n}")
    if failed:
        print(f"\nESITO: FAIL ({len(failed)}/{len(results)} audit falliti)")
        return 1
    print(f"\nESITO: PASS ({len(results)}/{len(results)} audit)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
