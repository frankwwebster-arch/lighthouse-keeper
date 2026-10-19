#!/usr/bin/env python3
"""Build the V23 snap-to-grid and seamless-join interaction proof."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-snap-grid-join-v23"
BATCH = "kitchen-snap-grid-join-2026-10-19-v23"
DRAFT = ROOT / "art/drafts" / BATCH
PUBLIC = ROOT / "public/keeper-review" / SET
TEMPLATE = ROOT / "scripts/templates/kitchen_snap_grid_join_v23.html"
V22_RAW = ROOT / "art/raw/kitchen-countertop-join-cap-2026-10-19-v22"
V22_APPROVAL = ROOT / "docs/review/kitchen-countertop-join-cap-v22-approval-2026-10-19.json"

ASSETS = {
    "room-background-exact.png": V22_RAW / "room-background-exact.png",
    "cabinet-run-v11-exact.png": V22_RAW / "cabinet-run-v11-exact.png",
    "sink-cabinet-v19-exact.png": V22_RAW / "sink-cabinet-v19-exact.png",
    "join-body-backfill-template.png": V22_RAW / "join-body-backfill-template.png",
    "countertop-join-cap-template.png": V22_RAW / "countertop-join-cap-template.png",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for directory in (DRAFT, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)
    for path in [TEMPLATE, V22_APPROVAL, *ASSETS.values()]:
        if not path.exists():
            raise RuntimeError(f"Missing authority: {path.relative_to(ROOT)}")

    slot_origins = [84, 168, 252, 336, 420, 504]
    catalogue = {
        "set": SET,
        "version": 23,
        "status": "snap-grid-and-seamless-join-proof-awaiting-review",
        "authorities": {
            "v22Approval": {"file": str(V22_APPROVAL.relative_to(ROOT)), "sha256": sha(V22_APPROVAL)},
            "assets": {
                name: {"source": str(path.relative_to(ROOT)), "sha256": sha(path), "byteIdentical": True}
                for name, path in ASSETS.items()
            },
        },
        "grid": {
            "originX": 84,
            "bayWidthPixels": 84,
            "slotOriginsX": slot_origins,
            "slotCentresX": [x + 42 for x in slot_origins],
            "primeStopTurnY": 218,
            "occupiedByTwoBayRun": [168, 252],
            "legalSinkOriginsX": [84, 336, 420, 504],
            "defaultSinkOriginX": 336,
            "sinkBodyWidthPixels": 84,
            "defaultSinkMidpointX": 378,
        },
        "snapContract": {
            "freePointerPreviewAllowed": True,
            "nearestLegalSlotShownDuringDrag": True,
            "commitOccursOnPointerRelease": True,
            "committedOriginAlwaysExactGridValue": True,
            "occupiedSlotsRejected": True,
            "interactionAnchorDerivedFromSnappedBodyMidpoint": True,
            "imprecisePointerCoordinateNeverPersisted": True,
            "multiBayUpgradeRequiresContiguousLegalSlots": True,
            "multiBayInteractionAnchorUsesFullBodyMidpoint": True,
        },
        "joinContract": {
            "approvedMethodVersion": 22,
            "joinActivatesOnlyForExactCommittedAdjacency": True,
            "requiredLogicalGapPixels": 0,
            "drawOrder": ["room-background", "body-backfill", "cabinet-assets", "countertop-join-cap"],
            "bodyUnderlapPixelsPerSide": 3,
            "capUnderlapPixelsPerSide": 8,
            "countertopRowsInclusive": [134, 145],
            "sourceAssetPixelsChanged": False,
        },
        "publishedAssets": {name: sha(path) for name, path in ASSETS.items()},
        "boundaries": {"v22Changed": False, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    page_path = PUBLIC / "index.html"
    page_path.write_text(TEMPLATE.read_text().replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))))
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "reversible-unapproved-unpromoted",
        "candidate": {
            "catalogue": {"file": str(catalogue_path.relative_to(ROOT)), "sha256": sha(catalogue_path)},
            "publicShell": {"file": str(page_path.relative_to(ROOT)), "sha256": sha(page_path)},
        },
        "publishedAssets": [
            {
                "source": str(path.relative_to(ROOT)),
                "sourceSha256": sha(path),
                "publicAssemblyPath": str((PUBLIC / "assets" / name).relative_to(ROOT)),
            }
            for name, path in ASSETS.items()
        ],
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print("Built Kitchen Snap Grid Join V23: imprecise drag preview, exact bay commit, midpoint anchor and approved seamless join")


if __name__ == "__main__":
    main()
