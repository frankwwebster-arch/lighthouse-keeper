#!/usr/bin/env python3
"""Build or verify Frank's selected ligne-claire spirit-level V2."""

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
PACK = ROOT / "art/drafts/activity-story-ligne-claire-repair-spirit-level-user-selected-2026-10-21-v1"
SET = "activity-story-ligne-claire-repair-spirit-level-user-selected-2026-10-21-v1"
PICTURE_ID = "repair-spirit-level"
CURRENT_V1 = ROOT / "art/drafts/codex-bubble-story-families-2026-10-21-v1/assets/repair-spirit-level.png"
CURRENT_V1_SHA256 = "97594e40eeef16d383f5f39ac35e55e8b4a40a2fd2e2e735de9ad99b3f5f9998"
SOURCE = PACK / "source/repair-spirit-level-source.png"
SOURCE_SHA256 = "fed10a02beb244715ffd1ea6ff652fc80607900d2c67288ad2135e4c54ec83f0"
OUTPUT = PACK / "drafts/components/repair-spirit-level.png"
CONTACT = PACK / "evidence/current-vs-user-selected-contact-sheet.png"
PALETTE = [
    INK,
    (13, 78, 117),
    (13, 126, 140),
    (35, 162, 180),
    (73, 76, 82),
    (196, 137, 38),
    (231, 166, 56),
    (167, 201, 87),
    (217, 235, 77),
    (246, 229, 183),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def library_entry() -> dict[str, object]:
    library = json.loads((ROOT / "data/activity-stories/pictures.json").read_text())
    return library["pictures"][PICTURE_ID]


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    if sha256(CURRENT_V1) != CURRENT_V1_SHA256:
        raise RuntimeError("spirit-level V1 drift")
    if sha256(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("user-selected source drift")
    source = Image.open(SOURCE)
    if source.mode != "RGBA" or edge_alpha_pixels(source):
        raise RuntimeError("unsafe user-selected source")
    component, evidence = normalise(source, PALETTE)
    if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
        raise RuntimeError("unsafe production component")
    component.save(OUTPUT, optimize=True)
    spec = {"id": PICTURE_ID, "label": "Spirit level", "current": rel(CURRENT_V1)}
    contact_sheet([(spec, component)]).save(CONTACT, optimize=True)
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-family-pack@1",
        "set": SET,
        "status": "approved-current-v2",
        "created": "2026-10-21",
        "tool": "built-in image generation plus deterministic fixed-palette normalisation",
        "family": "repair",
        "semanticSet": "Frank's selected less-cartoonish repair spirit level",
        "styleChampions": {
            "washing-plate": "living hand-drawn shape and controlled minor imperfection",
            "sandwich-tomato": "flat colour economy and selective readable detail",
            "repair-toolbox": "construction, detail hierarchy and confident object presence",
        },
        "evolvingRecipe": "Observational ligne claire, not cartoon: credible adult-tool proportions, straight technical construction, fine mostly-even contour, flat matte spot colour and only restrained hand-drawn irregularity.",
        "components": {
            PICTURE_ID: {
                "family": "repair",
                "label": "Spirit level",
                "intent": "approved-current-v2",
                "priorCurrentLibraryVersion": 1,
                "currentLibraryVersion": 2,
                "preserves": "one low horizontal teal level with exactly three vial stations: vertical left, horizontal centre and diagonal right",
                "currentReferenceFile": rel(CURRENT_V1),
                "currentReferenceSha256": CURRENT_V1_SHA256,
                "sourceFile": rel(SOURCE),
                "sourceSha256": SOURCE_SHA256,
                "sourcePixels": list(source.size),
                "originalCacheFile": "exec-92f3522c-4484-48ce-bdb8-77c3cea6388a.png",
                "flatPalette": ["#%02x%02x%02x" % colour for colour in PALETTE],
                "derivation": "alpha>8 crop; Lanczos scale to fit 216px; nearest fixed RGB palette; integer-centred in transparent 256x256 RGBA; lossless PNG",
                "file": rel(OUTPUT),
                "sha256": sha256(OUTPUT),
                "cellPixels": [CELL, CELL],
                **evidence,
            }
        },
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
            "priorCurrentHashPinned": True,
            "exactPaletteRecorded": True,
            "contactSheetCoverage": True,
            "libraryVersionAdded": True,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": {
            "date": "2026-10-21",
            "verdict": "approved",
            "words": "this one is good",
            "approvedSource": "exec-92f3522c-4484-48ce-bdb8-77c3cea6388a.png",
        },
        "rollback": "Set repair-spirit-level current back to V1; both immutable versions remain selectable. Discarding this pack alone removes no prior art.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify(require_registered=False)
    print(f"Built Frank's selected spirit-level V2 in {SET}")


def verify(*, require_registered: bool = True) -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "approved-current-v2":
        raise RuntimeError("register identity/status mismatch")
    if register["approval"]["words"] != "this one is good":
        raise RuntimeError("approval provenance mismatch")
    if list(register["components"]) != [PICTURE_ID]:
        raise RuntimeError("register coverage mismatch")
    entry = register["components"][PICTURE_ID]
    if sha256(CURRENT_V1) != CURRENT_V1_SHA256 or sha256(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("pinned input hash drift")
    for path, expected in ((OUTPUT, entry["sha256"]), (CONTACT, register["evidence"]["sha256"])):
        if not path.is_file() or sha256(path) != expected:
            raise RuntimeError(f"missing or changed pack file: {path}")
    output = Image.open(OUTPUT)
    if output.mode != "RGBA" or output.size != (CELL, CELL) or edge_alpha_pixels(output):
        raise RuntimeError("component mode, geometry or edge-alpha mismatch")
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
    picture = library_entry()
    if picture["versions"][0]["sha256"] != CURRENT_V1_SHA256:
        raise RuntimeError("library V1 hash drift")
    registered = (
        picture["current"] == 2
        and len(picture["versions"]) == 2
        and picture["versions"][1]["sha256"] == entry["sha256"]
    )
    if require_registered and not registered:
        raise RuntimeError("approved spirit-level V2 is not current")
    if not require_registered and not registered and (picture["current"] != 1 or len(picture["versions"]) != 1):
        raise RuntimeError("unexpected library state before registration")
    expected_hashes = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hashes:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    state = "current immutable V2" if registered else "built and awaiting registration"
    print(f"Verified {SET}: {state}, V1 retained")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
