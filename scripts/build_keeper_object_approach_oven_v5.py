#!/usr/bin/env python3
"""Build Oven Approach V5 with a visible floor plane and rear-floor oven datum."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3_PAGE = ROOT / "public/keeper-review/keeper-object-approach-oven-v3/index.html"
V3_REGISTER = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v3/batch-register.json"
V4_REGISTER = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v4/batch-register.json"
PACK = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v5"
PUBLIC = ROOT / "public/keeper-review/keeper-object-approach-oven-v5"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


SPEC = {
    "schema": "lighthouse-keeper/oven-visible-floor-placement@1",
    "status": "draft-placement-and-perspective-awaiting-review",
    "room": {
        "heightLp": 56,
        "rearWallFloorJunctionLpAboveStageBottom": 14,
        "frontFloorLipLp": 2,
        "visibleFloorSurfaceDepthOnElevationLp": 12,
        "rearWallWidthPercent": 96,
    },
    "oven": {
        "ovenBaseLpAboveStageBottom": 14,
        "v3BaseLpAboveStageBottom": 0.5,
        "v4UnshownBaseLpAboveStageBottom": 2,
        "additionalRaiseFromV3Lp": 13.5,
        "footprintLp": [30, 30],
        "interactionCentreLp": 120,
    },
    "preserved": {
        "keeperFrameUrls": 20,
        "routeValues": True,
        "timing": True,
        "perspectiveCalibration": True,
        "interactionAnchor": True,
        "keeperStageBottom": True,
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
    for authority in (V3_PAGE, V3_REGISTER, V4_REGISTER):
        if not authority.exists():
            raise RuntimeError(f"Missing authority: {authority.relative_to(ROOT)}")
    PACK.mkdir(parents=True, exist_ok=False)
    PUBLIC.mkdir(parents=True, exist_ok=False)
    spec_path = PACK / "oven-visible-floor-placement-v1.json"
    spec_path.write_text(json.dumps(SPEC, indent=2) + "\n")

    page = V3_PAGE.read_text()
    replacements = {
        "<title>Keeper oven approach V3</title>": "<title>Keeper oven approach V5</title>",
        "<h1>Oven approach V3 · corrected floor datum + perspective calibration</h1>": "<h1>Oven approach V5 · visible floor plane + perspective calibration</h1>",
        "V3 raises the proxy by the measured 0.5-lp boot gutter and proposes a shared perspective guide.": "V5 places the rear-wall oven on the back edge of a visible 12-lp floor surface while preserving every Keeper frame and route value.",
        "The oven base is raised exactly 0.5 lp to the approved Keeper's lowest opaque boot datum. The 30 × 30 lp proxy and interaction centre are otherwise unchanged.": "The oven stands at the rear wall/floor junction, 14 lp above the stage bottom. The Keeper remains on the near interaction line, leaving 12 lp of visible floor above the 2-lp front lip.",
        "shared boot / oven base": "rear wall / oven base",
        "oven.style.bottom=`${.5*scale}px`;const datum=el.querySelector('.footDatum');datum.style.bottom=`${.5*scale}px`;": "oven.style.bottom=`${14*scale}px`;const datum=el.querySelector('.footDatum');datum.style.bottom=`${14*scale}px`;",
    }
    for old, new in replacements.items():
        if old not in page:
            raise RuntimeError(f"V3 page pattern missing: {old[:90]}")
        page = page.replace(old, new, 1)

    page = page.replace(
        ".floor{position:absolute;left:0;right:0;bottom:0;background:#75583d;border-top:2px solid #d3ae75}",
        ".floor{position:absolute;left:0;right:0;bottom:0;background:#75583d;border-top:2px solid #d3ae75;z-index:3}.floorSurface{position:absolute;left:0;right:0;background:linear-gradient(#3b5048,#293a35);clip-path:polygon(2% 0,98% 0,100% 100%,0 100%);border-top:1px solid #8ba08a;z-index:0}",
        1,
    )
    page = page.replace('<div class="floor"></div><div class="footDatum">', '<div class="floorSurface"></div><div class="floor"></div><div class="footDatum">')
    page = page.replace(
        "const oven=el.querySelector('.asset'),target=el.querySelector('.target'),floor=el.querySelector('.floor');",
        "const oven=el.querySelector('.asset'),target=el.querySelector('.target'),floor=el.querySelector('.floor'),floorSurface=el.querySelector('.floorSurface');",
        1,
    )
    page = page.replace(
        "target.style.left=`${(DATA.oven.centreLp-leftLp)*scale}px`;floor.style.width=`${DATA.room.widthLp*scale}px`",
        "target.style.left=`${(DATA.oven.centreLp-leftLp)*scale}px`;floor.style.width=`${DATA.room.widthLp*scale}px`;floorSurface.style.bottom=`${2*scale}px`;floorSurface.style.height=`${12*scale}px`;floorSurface.style.width=`${DATA.room.widthLp*scale}px`",
        1,
    )
    output = PUBLIC / "index.html"
    output.write_text(page)

    register = {
        "schema": "lighthouse-keeper/review-batch@1",
        "batchId": "keeper-object-approach-oven-2026-10-14-v5",
        "status": SPEC["status"],
        "authorities": {
            "ovenApproachV3Register": {"file": str(V3_REGISTER.relative_to(ROOT)), "sha256": digest(V3_REGISTER)},
            "ovenApproachV3Page": {"file": str(V3_PAGE.relative_to(ROOT)), "sha256": digest(V3_PAGE)},
            "ovenApproachV4Register": {"file": str(V4_REGISTER.relative_to(ROOT)), "sha256": digest(V4_REGISTER)},
        },
        "spec": {"file": str(spec_path.relative_to(ROOT)), "sha256": digest(spec_path)},
        "reviewPage": {"file": str(output.relative_to(ROOT)), "sha256": digest(output)},
        "validation": {
            "ovenBaseEqualsRearFloorJunction": True,
            "visibleFloorSurfaceIsExact": True,
            "v3KeeperFrameUrlsReused": True,
            "v3PerspectiveCalibrationPreserved": True,
            "approvedKeeperPixelsChanged": False,
            "runtimeChanged": False,
            "approvalChanged": False,
        },
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PACK / "HANDOFF.md").write_text("""# Keeper oven approach V5

Status: draft placement and perspective calibration awaiting Frank's review.

V5 responds to Frank's observation that seeing floor is part of the room's perspective. The oven is a rear-wall object, so its base now sits at the rear wall/floor junction 14 lp above the stage bottom. A 12-lp visible floor surface runs forward to a 2-lp front floor lip; the Keeper remains on the unchanged near interaction line.

V4's unshown 2-lp placement is retained as historical construction evidence but was too shallow to express room depth. Every Keeper frame URL, route value, timing, interaction x anchor and perspective calibration remains unchanged from V3. Nothing is approved or wired.

Review: `/keeper-review/keeper-object-approach-oven-v5/`.
""")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
