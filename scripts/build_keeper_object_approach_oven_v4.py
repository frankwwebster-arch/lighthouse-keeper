#!/usr/bin/env python3
"""Build Oven Approach V4 with the oven on the floor's top surface."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3_PAGE = ROOT / "public/keeper-review/keeper-object-approach-oven-v3/index.html"
V3_REGISTER = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v3/batch-register.json"
PACK = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v4"
PUBLIC = ROOT / "public/keeper-review/keeper-object-approach-oven-v4"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


SPEC = {
    "schema": "lighthouse-keeper/oven-floor-surface-placement@1",
    "status": "draft-placement-and-perspective-awaiting-review",
    "oven": {
        "floorBandThicknessLp": 2,
        "floorTopSurfaceLpAboveStageBottom": 2,
        "ovenBaseLpAboveStageBottom": 2,
        "v3BaseLpAboveStageBottom": 0.5,
        "additionalRaiseFromV3Lp": 1.5,
        "footprintLp": [30, 30],
        "interactionCentreLp": 120,
    },
    "preserved": {
        "keeperFrameUrls": 20,
        "routeValues": True,
        "timing": True,
        "perspectiveCalibration": True,
        "interactionAnchor": True,
    },
    "boundaries": {
        "approvedKeeperPixelsChanged": False,
        "approvedTimingChanged": False,
        "runtimeGridChanged": False,
        "productionChanged": False,
        "approvalChanged": False,
    },
}


def main() -> None:
    if not V3_PAGE.exists() or not V3_REGISTER.exists():
        raise RuntimeError("Oven Approach V3 authority is missing")
    PACK.mkdir(parents=True, exist_ok=False)
    PUBLIC.mkdir(parents=True, exist_ok=False)
    spec_path = PACK / "oven-floor-surface-placement-v1.json"
    spec_path.write_text(json.dumps(SPEC, indent=2) + "\n")

    page = V3_PAGE.read_text()
    replacements = {
        "<title>Keeper oven approach V3</title>": "<title>Keeper oven approach V4</title>",
        "<h1>Oven approach V3 · corrected floor datum + perspective calibration</h1>": "<h1>Oven approach V4 · oven on the floor surface + perspective calibration</h1>",
        "V3 raises the proxy by the measured 0.5-lp boot gutter and proposes a shared perspective guide.": "V4 places the proxy on top of the 2-lp floor surface, 1.5 lp above V3, while preserving the perspective guide.",
        "The oven base is raised exactly 0.5 lp to the approved Keeper's lowest opaque boot datum. The 30 × 30 lp proxy and interaction centre are otherwise unchanged.": "The oven base now sits exactly on the top of the 2-lp structural floor band. This is 1.5 lp higher than V3; the 30 × 30 lp proxy and interaction centre are otherwise unchanged.",
        "shared boot / oven base": "floor top / oven base",
        "oven.style.bottom=`${.5*scale}px`;const datum=el.querySelector('.footDatum');datum.style.bottom=`${.5*scale}px`;": "oven.style.bottom=`${2*scale}px`;const datum=el.querySelector('.footDatum');datum.style.bottom=`${2*scale}px`;",
    }
    for old, new in replacements.items():
        if old not in page:
            raise RuntimeError(f"V3 page pattern missing: {old[:90]}")
        page = page.replace(old, new, 1)
    output = PUBLIC / "index.html"
    output.write_text(page)

    register = {
        "schema": "lighthouse-keeper/review-batch@1",
        "batchId": "keeper-object-approach-oven-2026-10-14-v4",
        "status": SPEC["status"],
        "authorities": {
            "ovenApproachV3Register": {"file": str(V3_REGISTER.relative_to(ROOT)), "sha256": digest(V3_REGISTER)},
            "ovenApproachV3Page": {"file": str(V3_PAGE.relative_to(ROOT)), "sha256": digest(V3_PAGE)},
        },
        "spec": {"file": str(spec_path.relative_to(ROOT)), "sha256": digest(spec_path)},
        "reviewPage": {"file": str(output.relative_to(ROOT)), "sha256": digest(output)},
        "validation": {
            "ovenBaseEqualsFloorTop": True,
            "additionalRaiseFromV3IsExact": True,
            "v3KeeperFrameUrlsReused": True,
            "v3PerspectiveCalibrationPreserved": True,
            "approvedKeeperPixelsChanged": False,
            "runtimeChanged": False,
            "approvalChanged": False,
        },
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PACK / "HANDOFF.md").write_text("""# Keeper oven approach V4\n\nStatus: draft placement and perspective calibration awaiting Frank's review.\n\nV4 corrects Frank's V3 review note: furniture must stand on the top surface of the floor, not share the Keeper's foot/contact level inside the floor band. The floor band is 2 lp thick, so the oven base is now exactly 2 lp above the stage bottom—1.5 lp above V3.\n\nEvery Keeper frame URL, route value, timing, interaction x anchor and perspective calibration remains byte-for-byte or value-for-value unchanged from V3. Nothing is approved or wired.\n\nReview: `/keeper-review/keeper-object-approach-oven-v4/`.\n""")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
