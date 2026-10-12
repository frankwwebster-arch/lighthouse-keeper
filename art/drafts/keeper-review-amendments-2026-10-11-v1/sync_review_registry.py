#!/usr/bin/env python3
"""Add this batch's active exact-name drafts without disturbing older variants."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
REGISTRY = ROOT / "data/keeper_review_drafts.json"


def main() -> None:
    registry = json.loads(REGISTRY.read_text())
    prior = [
        item for item in registry["drafts"]
        if not item["register"].startswith("art/drafts/keeper-review-amendments-2026-10-11-v1/")
    ]
    additions = []
    for register_path in sorted((BATCH / "drafts").glob("*/draft-register.json")):
        record = json.loads(register_path.read_text())
        if record.get("status") != "active-review-draft":
            continue
        additions.append({
            "name": record["animation"],
            "status": record["status"],
            "label": record["label"],
            "register": register_path.relative_to(ROOT).as_posix(),
        })
    registry["drafts"] = prior + additions
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    print(f"Preserved {len(prior)} earlier variants and registered {len(additions)} active amendment drafts")


if __name__ == "__main__":
    main()
