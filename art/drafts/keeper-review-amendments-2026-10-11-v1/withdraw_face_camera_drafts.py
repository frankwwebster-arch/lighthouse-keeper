#!/usr/bin/env python3
"""Withdraw generated face-to-camera candidates without deleting provenance."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WITHDRAWN = {
    "keeper_count_money",
    "keeper_lift_button_front",
    "keeper_mechanic_walk_front",
    "keeper_party_dance",
    "keeper_party_idle",
    "keeper_pyjamas_turn_back",
    "keeper_scuba_swim_down",
    "keeper_souwester_walk_front",
    "keeper_spaceman_walk_front",
    "keeper_swim_costume_down",
    "keeper_tarzan_walk_front",
    "keeper_trampoline_front",
    "keeper_water_plants_front",
}


def main() -> None:
    records = []
    for name in sorted(WITHDRAWN):
        register_path = ROOT / "drafts" / name / "draft-register.json"
        if not register_path.exists():
            continue
        register = json.loads(register_path.read_text())
        register["status"] = "withdrawn-by-user"
        register["selection"] = (
            "Withdrawn on 2026-10-12: revert every newly rendered face-to-camera "
            "candidate. Retained only as rejected provenance; never expose as an active review candidate."
        )
        register_path.write_text(json.dumps(register, indent=2) + "\n")
        records.append({"animation": name, "register": register_path.relative_to(ROOT.parents[2]).as_posix()})

    record = {
        "decision": "withdraw-all-generated-face-camera-candidates",
        "date": "2026-10-12",
        "reason": "Frank judged the face-to-camera amendments completely wrong.",
        "canonicalAssetsChanged": False,
        "activeHistoricalDraftsChanged": False,
        "withdrawn": records,
    }
    (ROOT / "withdrawn-face-camera-drafts.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"Withdrew {len(records)} face-to-camera draft candidates")


if __name__ == "__main__":
    main()
