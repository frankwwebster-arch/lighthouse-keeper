#!/usr/bin/env python3
"""Build or verify the observational hen-and-coop correction gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from build_activity_story_ligne_claire_bbq_family_2026_10_21_v1 import (
    CELL,
    HEADER,
    INK,
    ROW_HEIGHT,
    VISIBLE_ALPHA,
    contact_sheet,
    edge_alpha_pixels,
    normalise,
    sha256,
    visible_bounds,
    write_hashes,
)


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/activity-story-ligne-claire-eggs-hen-coop-correction-2026-10-21-v1"
SET = "activity-story-ligne-claire-eggs-hen-coop-correction-2026-10-21-v1"
PICTURE_ID = "eggs-hen-coop"
CURRENT = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v5/drafts/components/eggs-hen-coop.png"
CURRENT_SHA256 = "4c5c10ba6212cdf35c695b384f30dc52c18e5b1f13737aa4a282b8bff425c50d"
PRIOR_CANDIDATE_SHA256 = "5171bf1b915a41328b1677216e37672262396d0abe8d0bcc8f6e3c5bc2422f5f"
SOURCE = PACK / "source/eggs-hen-coop-source.png"
OUTPUT = PACK / "drafts/components/eggs-hen-coop.png"
REJECTED = PACK / "rejected/eggs-hen-coop-not-quite-right-v1.png"
CONTACT = PACK / "evidence/current-vs-correction-contact-sheet.png"
PALETTE = [
    INK,
    (246, 229, 183),
    (246, 205, 135),
    (231, 166, 56),
    (232, 139, 45),
    (166, 95, 42),
    (116, 65, 40),
    (232, 72, 51),
    (195, 43, 55),
    (24, 112, 166),
    (13, 78, 117),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def library_entry() -> dict[str, object]:
    library = json.loads((ROOT / "data/activity-stories/pictures.json").read_text())
    return library["pictures"][PICTURE_ID]


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    if sha256(CURRENT) != CURRENT_SHA256:
        raise RuntimeError("current eggs-hen-coop V1 drift")
    if sha256(REJECTED) != PRIOR_CANDIDATE_SHA256:
        raise RuntimeError("rejected prior candidate drift")
    source = Image.open(SOURCE)
    if source.mode != "RGBA" or edge_alpha_pixels(source):
        raise RuntimeError("unsafe correction source")
    component, evidence = normalise(source, PALETTE)
    if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
        raise RuntimeError("unsafe correction output")
    component.save(OUTPUT, optimize=True)
    spec = {"id": PICTURE_ID, "label": "Hen and coop", "current": rel(CURRENT)}
    contact_sheet([(spec, component)]).save(CONTACT, optimize=True)
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-family-pack@1",
        "set": SET,
        "status": "review-gate-awaiting-approval",
        "created": "2026-10-21",
        "tool": "built-in image generation plus deterministic fixed-palette normalisation",
        "family": "eggs",
        "semanticSet": "observational adult-hen correction for the baking/eggs/mixing family gate",
        "styleChampions": {
            "washing-plate": "living hand-drawn shape and controlled minor imperfection",
            "sandwich-tomato": "flat colour economy and selective readable detail",
            "repair-toolbox": "construction, detail hierarchy and confident object presence",
        },
        "evolvingRecipe": "Observational ligne claire, not cartoon: animal anatomy must read before graphic charm. Use a small bead eye without visible sclera, natural weight-bearing breast/legs/toes, irregular feather groups and a non-symmetrical tail; keep the coop literal and secondary.",
        "components": {
            PICTURE_ID: {
                "family": "eggs",
                "label": "Hen and coop",
                "intent": "replacement-candidate-for-unregistered-v2",
                "priorCurrentLibraryVersion": 1,
                "proposedLibraryVersion": 2,
                "preserves": "one naturally proportioned adult brown-and-cream hen front-left of one small blue-green pitched-roof coop with dark doorway and spilling straw",
                "currentReferenceFile": rel(CURRENT),
                "currentReferenceSha256": CURRENT_SHA256,
                "sourceFile": rel(SOURCE),
                "sourceSha256": sha256(SOURCE),
                "sourcePixels": list(source.size),
                "originalCacheFile": "exec-dad3b011-75a2-473f-a7b0-1ff8470ac210.png",
                "flatPalette": ["#%02x%02x%02x" % colour for colour in PALETTE],
                "derivation": "alpha>8 crop; Lanczos scale to fit 216px; nearest fixed RGB palette; integer-centred in transparent 256x256 RGBA; lossless PNG",
                "file": rel(OUTPUT),
                "sha256": sha256(OUTPUT),
                "cellPixels": [CELL, CELL],
                **evidence,
            }
        },
        "rejected": [{
            "file": rel(REJECTED),
            "sha256": sha256(REJECTED),
            "reason": "Frank said the chicken was not quite right; its face, smooth breast and evenly fanned tail remained too designed despite the first anatomy correction.",
        }],
        "evidence": {
            "file": rel(CONTACT),
            "sha256": sha256(CONTACT),
            "columns": 5,
            "rows": 1,
            "coveredIds": [PICTURE_ID],
        },
        "checks": {
            "sourceEdgesClear": True,
            "componentGutterAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "currentReferenceHashPinned": True,
            "rejectedCandidateHashPinned": True,
            "exactPaletteRecorded": True,
            "contactSheetCoverage": True,
            "libraryVersionAdded": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": None,
        "nextStep": "Frank reviews this exact hen-and-coop correction. Register nothing before explicit approval.",
        "rollback": "Discard this correction pack alone; the family pack, V1 and all existing bytes remain immutable.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified the hen-and-coop correction in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "review-gate-awaiting-approval":
        raise RuntimeError("register identity/status mismatch")
    if register["approval"] is not None or list(register["components"]) != [PICTURE_ID]:
        raise RuntimeError("register approval/coverage mismatch")
    entry = register["components"][PICTURE_ID]
    picture = library_entry()
    if picture["current"] != 1 or len(picture["versions"]) != 1:
        raise RuntimeError("eggs-hen-coop was registered before approval")
    if picture["versions"][0]["sha256"] != CURRENT_SHA256 or sha256(CURRENT) != CURRENT_SHA256:
        raise RuntimeError("current V1 hash drift")
    if sha256(REJECTED) != PRIOR_CANDIDATE_SHA256:
        raise RuntimeError("rejected prior candidate drift")
    for path, expected in ((SOURCE, entry["sourceSha256"]), (OUTPUT, entry["sha256"]), (CONTACT, register["evidence"]["sha256"])):
        if not path.is_file() or sha256(path) != expected:
            raise RuntimeError(f"missing or changed pack file: {path}")
    source = Image.open(SOURCE)
    output = Image.open(OUTPUT)
    if source.mode != "RGBA" or output.mode != "RGBA" or output.size != (CELL, CELL):
        raise RuntimeError("mode/dimensions mismatch")
    if edge_alpha_pixels(source) or edge_alpha_pixels(output):
        raise RuntimeError("edge alpha found")
    bounds = visible_bounds(output)
    if list(bounds) != entry["bounds"]:
        raise RuntimeError("bounds mismatch")
    gutter = min(bounds[0], bounds[1], CELL - bounds[2], CELL - bounds[3])
    if gutter != entry["transparentGutterPx"] or gutter < 20:
        raise RuntimeError("gutter mismatch")
    allowed = {tuple(int(value[index:index + 2], 16) for index in (1, 3, 5)) for value in entry["flatPalette"]}
    actual = {pixel[:3] for pixel in output.get_flattened_data() if pixel[3] > VISIBLE_ALPHA}
    if not actual.issubset(allowed):
        raise RuntimeError("palette mismatch")
    if entry["ownership"] != {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0}:
        raise RuntimeError("ownership mismatch")
    contact = Image.open(CONTACT)
    if contact.mode != "RGBA" or contact.size != (CELL * 5, HEADER + ROW_HEIGHT):
        raise RuntimeError("contact sheet geometry mismatch")
    expected_hashes = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hashes:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {SET}: correction remains unregistered; V1 and prior rejected candidate retained")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
