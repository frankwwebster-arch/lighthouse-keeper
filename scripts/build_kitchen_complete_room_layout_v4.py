#!/usr/bin/env python3
"""Build Kitchen Complete Room Layout V4 from immutable V3 pixels.

V4 adds a third, established pair-aware healing comparison and replaces loose
pointer positions with room-grid slot identifiers.  The nineteen V3 drawings
remain pixel-identical.  Five existing compositor healing templates are added
to the single lossless atlas.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
V3_SET = "kitchen-complete-room-layout-2026-10-22-v3"
SET = "kitchen-complete-room-layout-2026-10-22-v4"
V3 = ROOT / "art/drafts" / V3_SET
OUT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-complete-room-layout-v4"
TEMPLATE = ROOT / "scripts/templates/kitchen_complete_room_layout_v4.html"
GRID_CONTRACT = ROOT / "data/kitchen_room_grid_contract_v1.json"
HEALING_ROOT = ROOT / "art/drafts/kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3/candidates/healing"
V3_MANIFEST_SHA256 = "cb80afc71a42b9e3b1ed43dc910d018a0ec746fc6380732f719e78689e3ea9c1"
ATLAS_NAME = "kitchen-complete-room-atlas-v4.png"
GUTTER = 8
HEALING_NAMES = [
    "join-body-backfill-template.png",
    "countertop-join-cap-template.png",
    "countertop-triangle-underlay-template.png",
    "neighbour-seam-cleanup-left.png",
    "neighbour-seam-cleanup-right.png",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    v3_manifest_path = V3 / "manifest.json"
    assert sha256(v3_manifest_path) == V3_MANIFEST_SHA256, "V3 manifest changed"
    v3 = json.loads(v3_manifest_path.read_text())
    grid = json.loads(GRID_CONTRACT.read_text())
    prior_atlas_path = V3 / "assets" / v3["atlas"]["file"]
    assert sha256(prior_atlas_path) == v3["atlas"]["sha256"], "V3 atlas changed"
    prior = Image.open(prior_atlas_path).convert("RGBA")

    healing_images: list[tuple[str, Path, Image.Image]] = []
    for name in HEALING_NAMES:
        source = HEALING_ROOT / name
        healing_images.append((name.removesuffix(".png"), source, Image.open(source).convert("RGBA")))

    width = max([prior.width] + [image.width + GUTTER * 2 for _, _, image in healing_images])
    height = prior.height + sum(image.height for _, _, image in healing_images) + GUTTER * len(healing_images)
    atlas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    atlas.alpha_composite(prior, (0, 0))
    healing_assets = {}
    y = prior.height + GUTTER
    for key, source, image in healing_images:
        atlas.alpha_composite(image, (GUTTER, y))
        healing_assets[key] = {
            "sourceFile": str(source.relative_to(ROOT)),
            "sourceSha256": sha256(source),
            "pixels": list(image.size),
            "atlasRect": [GUTTER, y, image.width, image.height],
        }
        y += image.height + GUTTER

    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "assets").mkdir(parents=True, exist_ok=True)
    draft_atlas = OUT / "assets" / ATLAS_NAME
    public_atlas = PUBLIC / "assets" / ATLAS_NAME
    atlas.save(draft_atlas, optimize=True)
    public_atlas.write_bytes(draft_atlas.read_bytes())

    assets = {name: {**record, "file": ATLAS_NAME} for name, record in v3["assets"].items()}
    loose_assets = {name: {**record, "file": ATLAS_NAME} for name, record in v3["looseAssets"].items()}
    manifest = {
        **v3,
        "schema": "lighthouse-keeper/kitchen-complete-room-layout@4",
        "set": SET,
        "status": "unapproved-grid-snap-and-healing-comparison",
        "deliveryPredecessor": {
            "set": V3_SET,
            "manifestSha256": V3_MANIFEST_SHA256,
            "drawingPixelsChanged": False,
            "fittedGeometryChanged": False,
            "stateBehaviourChanged": False,
            "loosePlacementChangedToExactGridSlots": True,
        },
        "atlas": {
            "file": ATLAS_NAME,
            "sha256": sha256(draft_atlas),
            "pixels": list(atlas.size),
            "drawingCount": 24,
            "uniqueImageRequests": 1,
            "lossless": True,
            "v3AtlasPixelsCopiedAtOrigin": True,
        },
        "assets": assets,
        "looseAssets": loose_assets,
        "healingAssets": healing_assets,
        "roomGrid": grid,
        "healingComparison": {
            "views": ["raw", "narrow-join-diagnostic", "established-pair-aware-v22-v32"],
            "fullMethodDrawOrder": [
                "room background",
                "six-pixel body backfills and oven triangular underlays",
                "unchanged fitted assets",
                "flat countertop caps or oven-neighbour cleanup masks",
                "unchanged loose objects",
            ],
            "sourceAuthority": "Kitchen Split Cabinet Workbench V38 / V22 and V32 compositor contract",
            "approvedForTheseNewAssets": False,
        },
    }
    manifest["looseGeometry"] = {
        **v3["looseGeometry"],
        "defaultPositions": None,
        "positionStorage": "slot identifiers only; pointer coordinates are never persisted",
        "defaultSlotAssignments": grid["defaultAssignments"],
    }
    payload = (json.dumps(manifest, indent=2) + "\n").encode()
    (OUT / "manifest.json").write_bytes(payload)
    (PUBLIC / "manifest.json").write_bytes(payload)
    (PUBLIC / "index.html").write_text(TEMPLATE.read_text())
    print(json.dumps({"set": SET, "atlas": manifest["atlas"], "grid": grid["defaultAssignments"]}, indent=2))


if __name__ == "__main__":
    main()
