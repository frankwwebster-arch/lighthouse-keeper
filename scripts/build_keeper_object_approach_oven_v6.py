#!/usr/bin/env python3
"""Build the label-corrected immutable Oven Approach V6 review page."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V5_PAGE = ROOT / "public/keeper-review/keeper-object-approach-oven-v5/index.html"
V5_REGISTER = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v5/batch-register.json"
PACK = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v6"
PUBLIC = ROOT / "public/keeper-review/keeper-object-approach-oven-v6"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for authority in (V5_PAGE, V5_REGISTER):
        if not authority.exists():
            raise RuntimeError(f"Missing authority: {authority.relative_to(ROOT)}")
    PACK.mkdir(parents=True, exist_ok=False)
    PUBLIC.mkdir(parents=True, exist_ok=False)

    page = V5_PAGE.read_text()
    replacements = {
        "<title>Keeper oven approach V5</title>": "<title>Keeper oven approach V6</title>",
        "<h1>Oven approach V5 · visible floor plane + perspective calibration</h1>": "<h1>Oven approach V6 · visible floor plane + perspective calibration</h1>",
        "V5 places the rear-wall oven": "V6 places the rear-wall oven",
        "shared boot / oven base": "rear wall / oven base",
    }
    for old, new in replacements.items():
        if old not in page:
            raise RuntimeError(f"V5 page pattern missing: {old}")
        page = page.replace(old, new)
    output = PUBLIC / "index.html"
    output.write_text(page)

    spec = {
        "schema": "lighthouse-keeper/oven-visible-floor-delivery@1",
        "status": "draft-placement-and-perspective-awaiting-review",
        "geometryInheritedExactlyFromV5": True,
        "labelCorrection": "Both rulers identify the 14-lp rear wall / oven base datum.",
        "boundaries": {
            "approvedKeeperPixelsChanged": False,
            "routeOrTimingChanged": False,
            "floorOrOvenGeometryChangedFromV5": False,
            "runtimeChanged": False,
            "approvalChanged": False,
        },
    }
    spec_path = PACK / "delivery-correction-v1.json"
    spec_path.write_text(json.dumps(spec, indent=2) + "\n")
    register = {
        "schema": "lighthouse-keeper/review-batch@1",
        "batchId": "keeper-object-approach-oven-2026-10-14-v6",
        "status": spec["status"],
        "authorities": {
            "ovenApproachV5Register": {"file": str(V5_REGISTER.relative_to(ROOT)), "sha256": digest(V5_REGISTER)},
            "ovenApproachV5Page": {"file": str(V5_PAGE.relative_to(ROOT)), "sha256": digest(V5_PAGE)},
        },
        "spec": {"file": str(spec_path.relative_to(ROOT)), "sha256": digest(spec_path)},
        "reviewPage": {"file": str(output.relative_to(ROOT)), "sha256": digest(output)},
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PACK / "HANDOFF.md").write_text("""# Keeper oven approach V6

Status: draft placement and perspective calibration awaiting Frank's review.

V6 is the immutable delivery correction for V5. Geometry, animation, timing, floor depth and oven placement are exact; it only corrects the large ruler's stale V3 datum label so both panes say `rear wall / oven base`.

Review: `/keeper-review/keeper-object-approach-oven-v6/`.
""")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
