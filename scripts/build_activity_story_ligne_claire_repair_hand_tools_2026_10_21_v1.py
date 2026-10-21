#!/usr/bin/env python3
"""Build or verify the review-gated ligne-claire repair hand-tools pack."""

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
PACK = ROOT / "art/drafts/activity-story-ligne-claire-repair-hand-tools-2026-10-21-v1"
SET = "activity-story-ligne-claire-repair-hand-tools-2026-10-21-v1"
CURRENT_ROOT = "art/drafts/codex-bubble-story-families-2026-10-21-v1/assets"

SPECS: tuple[dict[str, object], ...] = (
    {
        "id": "repair-adjustable-spanner",
        "label": "Adjustable spanner",
        "source": "repair-adjustable-spanner-source.png",
        "cache": "exec-87ec3d20-3b66-4c6a-b033-809610c077ea.png",
        "current": f"{CURRENT_ROOT}/repair-adjustable-spanner.png",
        "currentSha256": "8443775c2d4d9de5af59d9339b976fda94ddd4226962d381c821f353f4560d5b",
        "palette": [INK, (246, 229, 183), (171, 166, 156), (73, 76, 82), (35, 162, 180), (13, 78, 117), (231, 166, 56)],
        "preserves": "one adult adjustable spanner with fixed and moving jaws, brass worm screw, teal two-pin grip and brass-edged hanging hole",
    },
    {
        "id": "repair-c-clamp",
        "label": "C-clamp",
        "source": "repair-c-clamp-source.png",
        "cache": "exec-3697443b-85b2-4504-9ae2-65ba25e9808d.png",
        "current": f"{CURRENT_ROOT}/repair-c-clamp.png",
        "currentSha256": "7baa85ec13949352f1460534e80d815b5237c87f7ccc489c2fd3d5da6f1ea54a",
        "palette": [INK, (13, 78, 117), (24, 112, 166), (231, 166, 56), (35, 162, 180), (246, 229, 183)],
        "preserves": "one side-on C-clamp with blue frame, brass threaded screw, pressure pad and vertical teal-ended T handle",
    },
    {
        "id": "repair-combination-pliers",
        "label": "Combination pliers",
        "source": "repair-combination-pliers-source.png",
        "cache": "exec-607f8393-8912-4d50-a2bd-648314d667e5.png",
        "current": f"{CURRENT_ROOT}/repair-combination-pliers.png",
        "currentSha256": "dadda73bf3e3aa44eebe2a5edd0694261e812857e86b317797f1f85e38bbdea2",
        "palette": [INK, (246, 229, 183), (171, 166, 156), (73, 76, 82), (231, 166, 56), (35, 162, 180), (13, 78, 117)],
        "preserves": "one pair of combination pliers with serrated steel jaws, cutting notch, round pivot and two separated teal grips",
    },
    {
        "id": "repair-flat-head-screwdriver",
        "label": "Flat-head screwdriver",
        "source": "repair-flat-head-screwdriver-source.png",
        "cache": "exec-3825c9f1-b9a1-4474-b09f-0c1cb7f29f41.png",
        "current": f"{CURRENT_ROOT}/repair-flat-head-screwdriver.png",
        "currentSha256": "8c70b4549514713f55dada9b8d58a91ee9f4251fde417fc2feadea0b5e40f471",
        "palette": [INK, (246, 229, 183), (171, 166, 156), (73, 76, 82), (231, 166, 56), (35, 162, 180), (13, 78, 117)],
        "preserves": "one flat-head screwdriver with slotted steel tip, long shaft, brass ferrule and dark-teal fluted handle",
    },
    {
        "id": "repair-phillips-screwdriver",
        "label": "Phillips screwdriver",
        "source": "repair-phillips-screwdriver-source.png",
        "cache": "exec-9f199efa-ed15-4c82-9216-3bddae929974.png",
        "current": f"{CURRENT_ROOT}/repair-phillips-screwdriver.png",
        "currentSha256": "733b49927d6ae1054898b56fa11eb464216e8ed6996073e6f22b68ebad13a073",
        "palette": [INK, (246, 229, 183), (171, 166, 156), (73, 76, 82), (231, 166, 56), (232, 72, 51), (207, 92, 24)],
        "preserves": "one Phillips screwdriver with cross-head steel tip, long shaft, plain brass ferrule and coral fluted handle",
    },
    {
        "id": "repair-hand-saw",
        "label": "Hand saw",
        "source": "repair-hand-saw-source.png",
        "cache": "exec-05467f27-b1ad-4507-8f6e-af4e43d1682d.png",
        "current": f"{CURRENT_ROOT}/repair-hand-saw.png",
        "currentSha256": "a7d6b4af87a3468838fe6515c42112ba39789ebd7dc1bd0a35835dc61d22dfdd",
        "palette": [INK, (246, 229, 183), (171, 166, 156), (73, 76, 82), (13, 78, 117), (24, 112, 166), (231, 166, 56)],
        "preserves": "one adult hand saw with tapering steel blade, one fine tooth row, tip hole and blue closed handle with two brass fasteners",
    },
    {
        "id": "repair-spirit-level",
        "label": "Spirit level",
        "source": "repair-spirit-level-source.png",
        "cache": "exec-3f9fa9f9-bd1b-47d7-a7ec-cdb76e92db03.png",
        "current": f"{CURRENT_ROOT}/repair-spirit-level.png",
        "currentSha256": "97594e40eeef16d383f5f39ac35e55e8b4a40a2fd2e2e735de9ad99b3f5f9998",
        "palette": [INK, (13, 98, 109), (35, 162, 180), (231, 166, 56), (166, 95, 42), (167, 201, 87), (246, 229, 183)],
        "preserves": "one horizontal spirit level with brass end caps and exactly three vial stations: vertical left, horizontal centre and diagonal right",
    },
    {
        "id": "repair-tape-measure",
        "label": "Tape measure",
        "source": "repair-tape-measure-source.png",
        "cache": "exec-6c8d3d00-5732-4dab-85a4-6d20c14496eb.png",
        "current": f"{CURRENT_ROOT}/repair-tape-measure.png",
        "currentSha256": "d5d3b3ff9d0df7db1ed6967e7a15f99fba35e06e785eb47249ad967105f4166e",
        "palette": [INK, (13, 78, 117), (24, 112, 166), (35, 162, 180), (231, 166, 56), (246, 229, 183), (73, 76, 82)],
        "preserves": "one tape measure with blue case, brass side plate and belt clip, teal controls and one cream tape extending to a hooked end",
    },
)

REJECTED: tuple[dict[str, str], ...] = (
    {
        "file": "rejected/repair-phillips-screwdriver-extra-ferrule-button-v1.png",
        "cache": "exec-abf7bb6c-8b2f-4a11-bbdc-12a26883ead8.png",
        "reason": "Invented a round side button on the brass ferrule and made the Phillips tip read as an oversized diamond spear rather than the current cross-head construction.",
    },
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def library_entries() -> dict[str, dict[str, object]]:
    return json.loads((ROOT / "data/activity-stories/pictures.json").read_text())["pictures"]


def build() -> None:
    source_dir = PACK / "source"
    component_dir = PACK / "drafts/components"
    evidence_dir = PACK / "evidence"
    component_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    entries: dict[str, object] = {}
    rows: list[tuple[dict[str, object], Image.Image]] = []
    for spec in SPECS:
        current_path = ROOT / str(spec["current"])
        source_path = source_dir / str(spec["source"])
        if sha256(current_path) != spec["currentSha256"]:
            raise RuntimeError(f"current source drift: {spec['id']}")
        source = Image.open(source_path)
        if source.mode != "RGBA" or edge_alpha_pixels(source):
            raise RuntimeError(f"unsafe source: {spec['id']}")
        palette = list(spec["palette"])
        component, evidence = normalise(source, palette)
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe output: {spec['id']}")
        output_path = component_dir / f"{spec['id']}.png"
        component.save(output_path, optimize=True)
        entries[str(spec["id"])] = {
            "family": "repair",
            "label": spec["label"],
            "intent": "candidate-new-version-v2",
            "priorCurrentLibraryVersion": 1,
            "proposedLibraryVersion": 2,
            "preserves": spec["preserves"],
            "currentReferenceFile": spec["current"],
            "currentReferenceSha256": spec["currentSha256"],
            "sourceFile": rel(source_path),
            "sourceSha256": sha256(source_path),
            "sourcePixels": list(source.size),
            "originalCacheFile": spec["cache"],
            "flatPalette": ["#%02x%02x%02x" % colour for colour in palette],
            "derivation": "alpha>8 crop; Lanczos scale to fit 216px; nearest fixed RGB palette; integer-centred in transparent 256x256 RGBA; lossless PNG",
            "file": rel(output_path),
            "sha256": sha256(output_path),
            "cellPixels": [CELL, CELL],
            **evidence,
        }
        rows.append((spec, component))

    contact_path = evidence_dir / "current-vs-ligne-claire-contact-sheet.png"
    contact_sheet(rows).save(contact_path, optimize=True)
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-family-pack@1",
        "set": SET,
        "status": "review-gate-awaiting-approval",
        "created": "2026-10-21",
        "tool": "built-in image generation plus deterministic fixed-palette normalisation",
        "family": "repair",
        "semanticSet": "eight adult hand tools from the repair picture family",
        "styleChampions": {
            "washing-plate": "living hand-drawn shape and controlled minor imperfection",
            "sandwich-tomato": "flat colour economy and selective readable detail",
            "repair-toolbox": "construction, detail hierarchy and confident object presence",
        },
        "evolvingRecipe": "Observational ligne claire, not cartoon: credible adult-object proportions and mechanisms, lively mostly-even near-black contour, flat opaque spot colour, minimal decisive construction lines and controlled minor asymmetry.",
        "preservationRule": "Preserve each current asset's identity, working construction, viewpoint, part count, relative proportions, orientation and broad silhouette. Reject cute, toy-like, inflated, sticker or caricature treatment.",
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "components": entries,
        "rejected": [{**item, "sha256": sha256(PACK / item["file"])} for item in REJECTED],
        "evidence": {
            "file": rel(contact_path),
            "sha256": sha256(contact_path),
            "columns": 5,
            "rows": len(rows),
            "coveredIds": [spec["id"] for spec in SPECS],
        },
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "currentReferenceHashesPinned": True,
            "exactPalettesRecorded": True,
            "contactSheetCoversEveryCandidate": True,
            "libraryVersionsAdded": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": None,
        "nextStep": "Frank reviews the exact eight-picture contact sheet. On approval, add each candidate as immutable V2 with the official add-picture command; never overwrite V1.",
        "rollback": "Before approval, discard this pack alone. After approval, set any picture's current selector back to V1; all version bytes remain immutable.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(rows)} review candidates in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "review-gate-awaiting-approval":
        raise RuntimeError("register identity/status mismatch")
    if register["family"] != "repair" or register["approval"] is not None:
        raise RuntimeError("register family/approval mismatch")
    expected_ids = [str(spec["id"]) for spec in SPECS]
    if list(register["components"]) != expected_ids:
        raise RuntimeError("register component order/coverage mismatch")
    library = library_entries()
    for spec in SPECS:
        picture_id = str(spec["id"])
        entry = register["components"][picture_id]
        source_path = ROOT / entry["sourceFile"]
        output_path = ROOT / entry["file"]
        current_path = ROOT / entry["currentReferenceFile"]
        for path in (source_path, output_path, current_path):
            if not path.is_file():
                raise RuntimeError(f"missing manifest path: {path}")
        if sha256(source_path) != entry["sourceSha256"] or sha256(output_path) != entry["sha256"]:
            raise RuntimeError(f"candidate hash mismatch: {picture_id}")
        if sha256(current_path) != entry["currentReferenceSha256"]:
            raise RuntimeError(f"prior-current hash mismatch: {picture_id}")
        picture = library[picture_id]
        if picture["current"] != 1 or len(picture["versions"]) != 1:
            raise RuntimeError(f"review gate unexpectedly registered a candidate: {picture_id}")
        if picture["versions"][0]["sha256"] != entry["currentReferenceSha256"]:
            raise RuntimeError(f"library V1 hash drift: {picture_id}")
        source = Image.open(source_path)
        output = Image.open(output_path)
        if source.mode != "RGBA" or output.mode != "RGBA" or output.size != (CELL, CELL):
            raise RuntimeError(f"mode/dimensions mismatch: {picture_id}")
        if edge_alpha_pixels(source) or edge_alpha_pixels(output):
            raise RuntimeError(f"edge alpha found: {picture_id}")
        output_box = visible_bounds(output)
        if list(output_box) != entry["bounds"]:
            raise RuntimeError(f"bounds mismatch: {picture_id}")
        gutter = min(output_box[0], output_box[1], CELL - output_box[2], CELL - output_box[3])
        if gutter != entry["transparentGutterPx"] or gutter < 20:
            raise RuntimeError(f"gutter mismatch: {picture_id}")
        allowed = {tuple(int(value[index:index + 2], 16) for index in (1, 3, 5)) for value in entry["flatPalette"]}
        actual = {pixel[:3] for pixel in output.get_flattened_data() if pixel[3] > VISIBLE_ALPHA}
        if not actual.issubset(allowed):
            raise RuntimeError(f"palette mismatch: {picture_id}")
        if entry["ownership"] != {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0}:
            raise RuntimeError(f"ownership mismatch: {picture_id}")
    for item in register["rejected"]:
        path = PACK / item["file"]
        if not path.is_file() or sha256(path) != item["sha256"]:
            raise RuntimeError(f"rejected-source hash mismatch: {item['file']}")
    evidence = register["evidence"]
    contact_path = ROOT / evidence["file"]
    if sha256(contact_path) != evidence["sha256"]:
        raise RuntimeError("contact sheet hash mismatch")
    contact = Image.open(contact_path)
    if contact.mode != "RGBA" or contact.size != (CELL * 5, HEADER + ROW_HEIGHT * len(expected_ids)):
        raise RuntimeError("contact sheet geometry mismatch")
    if evidence["coveredIds"] != expected_ids or evidence["rows"] != len(expected_ids) or evidence["columns"] != 5:
        raise RuntimeError("contact sheet coverage metadata mismatch")
    if register["checks"]["libraryVersionsAdded"]:
        raise RuntimeError("review pack incorrectly records registered versions")
    expected_hash_lines = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hash_lines:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {SET}: {len(expected_ids)} review candidates, contact sheet and retained V1 priors")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="verify existing outputs without rebuilding")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
