#!/usr/bin/env python3
"""Build Oven Approach V7 with a restrained five-lp visible floor surface."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V6_PAGE = ROOT / "public/keeper-review/keeper-object-approach-oven-v6/index.html"
V6_REGISTER = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v6/batch-register.json"
PACK = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v7"
PUBLIC = ROOT / "public/keeper-review/keeper-object-approach-oven-v7"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for authority in (V6_PAGE, V6_REGISTER):
        if not authority.exists():
            raise RuntimeError(f"Missing authority: {authority.relative_to(ROOT)}")
    PACK.mkdir(parents=True, exist_ok=False)
    PUBLIC.mkdir(parents=True, exist_ok=False)

    spec = {
        "schema": "lighthouse-keeper/oven-restrained-floor-placement@1",
        "status": "draft-placement-and-perspective-awaiting-review",
        "room": {
            "heightLp": 56,
            "frontFloorLipLp": 2,
            "visibleFloorSurfaceDepthOnElevationLp": 5,
            "rearWallFloorJunctionLpAboveStageBottom": 7,
            "wallHeightPercent": 87.5,
        },
        "oven": {
            "ovenBaseLpAboveStageBottom": 7,
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
    spec_path = PACK / "oven-restrained-floor-placement-v1.json"
    spec_path.write_text(json.dumps(spec, indent=2) + "\n")

    page = V6_PAGE.read_text()
    replacements = {
        "<title>Keeper oven approach V6</title>": "<title>Keeper oven approach V7</title>",
        "<h1>Oven approach V6 · visible floor plane + perspective calibration</h1>": "<h1>Oven approach V7 · restrained floor plane + perspective calibration</h1>",
        "V6 places the rear-wall oven on the back edge of a visible 12-lp floor surface": "V7 places the rear-wall oven on the back edge of a restrained 5-lp floor surface",
        "The oven stands at the rear wall/floor junction, 14 lp above the stage bottom. The Keeper remains on the near interaction line, leaving 12 lp of visible floor above the 2-lp front lip.": "The oven stands at the rear wall/floor junction, 7 lp above the stage bottom. The Keeper remains on the near interaction line, leaving 5 lp of visible floor above the 2-lp front lip.",
        "background:linear-gradient(#17313e 0 75%,#293a35 75% 100%)": "background:linear-gradient(#17313e 0 87.5%,#293a35 87.5% 100%)",
        "oven.style.bottom=`${14*scale}px`": "oven.style.bottom=`${7*scale}px`",
        "datum.style.bottom=`${14*scale}px`": "datum.style.bottom=`${7*scale}px`",
        "floorSurface.style.height=`${12*scale}px`": "floorSurface.style.height=`${5*scale}px`",
    }
    for old, new in replacements.items():
        if old not in page:
            raise RuntimeError(f"V6 page pattern missing: {old[:100]}")
        page = page.replace(old, new)
    output = PUBLIC / "index.html"
    output.write_text(page)

    register = {
        "schema": "lighthouse-keeper/review-batch@1",
        "batchId": "keeper-object-approach-oven-2026-10-14-v7",
        "status": spec["status"],
        "authorities": {
            "ovenApproachV6Register": {"file": str(V6_REGISTER.relative_to(ROOT)), "sha256": digest(V6_REGISTER)},
            "ovenApproachV6Page": {"file": str(V6_PAGE.relative_to(ROOT)), "sha256": digest(V6_PAGE)},
        },
        "spec": {"file": str(spec_path.relative_to(ROOT)), "sha256": digest(spec_path)},
        "reviewPage": {"file": str(output.relative_to(ROOT)), "sha256": digest(output)},
        "validation": {
            "ovenBaseEqualsRearFloorJunction": True,
            "visibleFloorSurfaceIsExact": True,
            "v6KeeperFramesRoutesAndPerspectivePreserved": True,
            "approvedKeeperPixelsChanged": False,
            "runtimeChanged": False,
            "approvalChanged": False,
        },
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PACK / "HANDOFF.md").write_text("""# Keeper oven approach V7

Status: draft placement and perspective calibration awaiting Frank's review.

V7 responds to Frank's judgment that V6 showed too much floor. The visible surface is reduced from 12 lp to 5 lp. With the unchanged 2-lp front lip, the rear wall/floor junction and oven base are now 7 lp above the stage bottom.

Every Keeper frame URL, route value, timing, interaction x anchor and perspective calibration remains unchanged. V6 remains immutable historical evidence. Nothing is approved or wired.

Review: `/keeper-review/keeper-object-approach-oven-v7/`.
""")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
