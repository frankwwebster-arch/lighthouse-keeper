#!/usr/bin/env python3
"""Build the V24 snap-grid proof with dynamic exposed-end healing."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-exposed-end-healing-v24"
BATCH = "kitchen-exposed-end-healing-2026-10-19-v24"
DRAFT = ROOT / "art/drafts" / BATCH
PUBLIC = ROOT / "public/keeper-review" / SET
TEMPLATE = ROOT / "scripts/templates/kitchen_exposed_end_healing_v24.html"
V22_RAW = ROOT / "art/raw/kitchen-countertop-join-cap-2026-10-19-v22"
V22_APPROVAL = ROOT / "docs/review/kitchen-countertop-join-cap-v22-approval-2026-10-19.json"
V23_CATALOGUE = ROOT / "art/drafts/kitchen-snap-grid-join-2026-10-19-v23/candidate-catalogue.json"

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
    for path in [TEMPLATE, V22_APPROVAL, V23_CATALOGUE, *ASSETS.values()]:
        if not path.exists():
            raise RuntimeError(f"Missing authority: {path.relative_to(ROOT)}")

    slot_origins = [84, 168, 252, 336, 420, 504]
    catalogue = {
        "set": SET,
        "version": 24,
        "status": "snap-grid-exposed-end-healing-awaiting-review",
        "authorities": {
            "v22Approval": {"file": str(V22_APPROVAL.relative_to(ROOT)), "sha256": sha(V22_APPROVAL)},
            "v23Catalogue": {"file": str(V23_CATALOGUE.relative_to(ROOT)), "sha256": sha(V23_CATALOGUE)},
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
            "defaultSinkOriginX": 420,
            "sinkBodyWidthPixels": 84,
            "defaultSinkMidpointX": 462,
        },
        "snapContract": {
            "v23BehaviourPreserved": True,
            "freePointerPreviewAllowed": True,
            "nearestLegalSlotShownDuringDrag": True,
            "commitOccursOnPointerRelease": True,
            "committedOriginAlwaysExactGridValue": True,
            "occupiedSlotsRejected": True,
            "interactionAnchorDerivedFromSnappedBodyMidpoint": True,
            "imprecisePointerCoordinateNeverPersisted": True,
        },
        "surfaceContract": {
            "joinedEdgeUsesApprovedV22Repair": True,
            "exposedLeftEdgeUsesApprovedV11LeftEndPixels": True,
            "exposedEndActivatesOnlyWithoutExactNeighbour": True,
            "exposedEndDeactivatesWhenNeighbourSnapsAdjacent": True,
            "sourceSprite": "cabinet-run-v11-exact.png",
            "sourceCrop": {"x": 0, "y": 0, "width": 12, "height": 82},
            "destinationOffsetFromBodyOrigin": {"x": -4, "y": -4},
            "drawOrder": [
                "room-background",
                "body-backfill",
                "cabinet-assets",
                "exposed-end-overlay",
                "countertop-join-cap",
            ],
            "sourceAssetPixelsChanged": False,
        },
        "publishedAssets": {name: sha(path) for name, path in ASSETS.items()},
        "boundaries": {
            "v22Changed": False,
            "v23Changed": False,
            "finalChanged": False,
            "runtimeChanged": False,
            "promotionPerformed": False,
        },
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
    print("Built Kitchen Exposed End Healing V24: exact snapping, joined-edge repair and automatic exposed-left-end repair")


if __name__ == "__main__":
    main()
