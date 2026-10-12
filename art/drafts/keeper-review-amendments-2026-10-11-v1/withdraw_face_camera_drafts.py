#!/usr/bin/env python3
"""Keep rejected face-to-camera candidates out of the active review registry."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WITHDRAWN = {
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

DELETED = [{
    "animation": "keeper_count_money",
    "deletedAtUserRequest": "2026-10-12",
    "reason": "Frank judged every pose terrible and explicitly requested deletion and reversion to the previous version.",
    "sourceSha256": "3567b77564ed483776d90ba504606f4ec4c96c4abbabd668484b37ea560232ee",
    "draftStripSha256": "499eadb2658812bfb58c90618bf50ebc1d2bbc060e7e026ed590c96043a4c64f",
    "canonicalStripSha256": "451c620ce890021930b04aa0bdecddc756d6bd830c552ad0ce6ea61d1d34c7a2",
    "canonicalRuntimeSha256": "47002b4c2d69148e4a172ca8fff5be4ea251c34b501a26e6ce63022f4b867a64",
    "recovery": "Rejected files remain recoverable from Git history before their explicit deletion; canonical raw and runtime assets were never changed.",
}]

REJECTION_DETAILS = {
    "keeper_pyjamas_turn_back": {
        "sourceSha256": "a1e34e26df0a6feb22b1f08883c0c512875baf90c44b7053ecdd83c003570730",
        "rejectionReason": "The front pose loses the defined moustache and mouth and collapses them into the cheesy pixie grin Frank explicitly rejected.",
    },
}


def main() -> None:
    records = []
    for name in sorted(WITHDRAWN):
        register_path = ROOT / "drafts" / name / "draft-register.json"
        if not register_path.exists():
            continue
        register = json.loads(register_path.read_text())
        details = REJECTION_DETAILS.get(name, {})
        detail_sentence = f" {details['rejectionReason']}" if details else ""
        register["status"] = "withdrawn-by-user"
        register["selection"] = (
            "Withdrawn on 2026-10-12: revert every newly rendered face-to-camera "
            f"candidate.{detail_sentence} Retained only as rejected provenance; never expose as an active review candidate."
        )
        if name == "keeper_pyjamas_turn_back":
            register["qualification"] = (
                "Rejected: the front pose loses canonical moustache and mouth definition and substitutes a cutesy curved grin. "
                "This source is provenance only and is not an acceptable face reference."
            )
        register_path.write_text(json.dumps(register, indent=2) + "\n")
        records.append({
            "animation": name,
            "register": register_path.relative_to(ROOT.parents[2]).as_posix(),
            **details,
        })

    record = {
        "decision": "withdraw-all-generated-face-camera-candidates",
        "date": "2026-10-12",
        "reason": "Frank judged the face-to-camera amendments completely wrong.",
        "canonicalAssetsChanged": False,
        "activeHistoricalDraftsChanged": False,
        "withdrawn": records,
        "deleted": DELETED,
    }
    (ROOT / "withdrawn-face-camera-drafts.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"Recorded {len(records)} retained withdrawals and {len(DELETED)} explicit deletion")


if __name__ == "__main__":
    main()
