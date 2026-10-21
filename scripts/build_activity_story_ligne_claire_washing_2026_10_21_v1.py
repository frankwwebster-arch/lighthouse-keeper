#!/usr/bin/env python3
"""Build or verify the approved ligne-claire washing-family pack."""

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
PACK = ROOT / "art/drafts/activity-story-ligne-claire-washing-2026-10-21-v1"
SET = "activity-story-ligne-claire-washing-2026-10-21-v1"
STORY = ROOT / "data/activity-stories/stories/washing-up.json"
STORY_SHA256 = "34bcc4e28a96fed0233c870613a08cb61f2eae98a6f63d19f3c2f5de87d4f1b7"

SPECS: tuple[dict[str, object], ...] = (
    {
        "id": "washing-plate",
        "label": "Plate",
        "source": "washing-plate-source.png",
        "cache": "exec-280b4e8e-d312-4e57-80e0-a18813386a63.png",
        "current": "review-archive/objects/01/01b82c03b73ae82461d420b87bfb44384fffb179cbfe544a2f9810f4358a427f.png",
        "currentSha256": "01b82c03b73ae82461d420b87bfb44384fffb179cbfe544a2f9810f4358a427f",
        "palette": [INK, (246, 229, 183), (13, 78, 117), (24, 112, 166), (153, 231, 226)],
        "preserves": "exactly one broad oval cream plate in the current low front three-quarter view, including its blue double rim and surrounding aqua bubble arrangement",
    },
    {
        "id": "washing-liquid",
        "label": "Washing-up liquid",
        "source": "washing-liquid-source.png",
        "cache": "exec-8809dc8f-f501-4a90-9e5a-3bdde560c654.png",
        "current": "review-archive/objects/f3/f311431e2c6e480033982790d416bbd6df16f414338c6a030ff28d2780efd2c1.png",
        "currentSha256": "f311431e2c6e480033982790d416bbd6df16f414338c6a030ff28d2780efd2c1",
        "palette": [INK, (16, 110, 62), (31, 190, 112), (246, 229, 183), (153, 231, 226)],
        "preserves": "exactly one upright green hourglass squeeze bottle with its cream neck ring, ridged green collar, push-pull cap and existing bubble arrangement",
    },
    {
        "id": "washing-sponge",
        "label": "Sponge",
        "source": "washing-sponge-source.png",
        "cache": "exec-3880c735-c718-4753-85cf-4cdd7a20a262.png",
        "current": "review-archive/objects/ae/aed0b35f1bf279fe02a211b566d694a9d90fde94e7b263aec072b8449d8b2533.png",
        "currentSha256": "aed0b35f1bf279fe02a211b566d694a9d90fde94e7b263aec072b8449d8b2533",
        "palette": [INK, (255, 205, 48), (232, 139, 45), (207, 92, 24), (246, 229, 183), (153, 231, 226)],
        "preserves": "exactly one thick yellow rectangular sponge in the current diagonal three-quarter view, with its orange side faces, modest front-left foam bank and five detached bubbles",
    },
    {
        "id": "washing-droplets",
        "label": "Rinse water",
        "source": "washing-droplets-source.png",
        "cache": "exec-dd0ce19d-a366-4f7b-a260-fe5b3468bac6.png",
        "current": "review-archive/objects/14/14fa3c4503f2362d509623d50e9537dddffce047cbd81092ec0383ddd94052da.png",
        "currentSha256": "14fa3c4503f2362d509623d50e9537dddffce047cbd81092ec0383ddd94052da",
        "palette": [INK, (153, 231, 226), (35, 162, 180)],
        "preserves": "exactly four water droplets in the current centre-large, left-medium, right-small and lower-left-tiny arrangement",
    },
    {
        "id": "washing-cutlery",
        "label": "Clean cutlery",
        "source": "washing-cutlery-source.png",
        "cache": "exec-c3ee3b28-61de-469d-a5e2-20ab8b97edd2.png",
        "current": "review-archive/objects/76/76d1a71e4d9e2cb24272136ef3df210ad2f1303e91fcf5846c0937825471b6ca.png",
        "currentSha256": "76d1a71e4d9e2cb24272136ef3df210ad2f1303e91fcf5846c0937825471b6ca",
        "palette": [INK, (246, 229, 183), (171, 157, 137), (153, 231, 226), (231, 166, 56)],
        "preserves": "exactly one three-pronged fork and one oval-bowled spoon in the current crossed X arrangement, with the spoon in front, paired gold handle insets and existing bubble clusters",
    },
)

REJECTED: tuple[dict[str, str], ...] = (
    {
        "file": "rejected/washing-plate-tonal-v1.png",
        "cache": "exec-99b8f58b-6582-46b2-a6ed-a8e2728c902d.png",
        "reason": "The plate preserved its construction but retained blue and cream tonal modelling instead of the tomato-calibrated flat spot-colour treatment.",
    },
    {
        "file": "rejected/washing-sponge-excess-foam-v1.png",
        "cache": "exec-a11f0589-011f-4ea3-9430-e8d6a41ffb38.png",
        "reason": "The sponge gained an oversized foam blanket, excess detached bubbles and excessive pore detail instead of preserving the current restrained arrangement.",
    },
    {
        "file": "rejected/washing-cutlery-prompt-conflict-v1.png",
        "cache": "exec-c1c27cee-0e01-4515-9190-a81f1b9d69b0.png",
        "reason": "The image kept the current three-pronged fork, but the generating prompt incorrectly described four tines; it was rerun so provenance and drawing agree.",
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
        if source.mode != "RGBA":
            raise RuntimeError(f"source is not RGBA: {spec['id']}")
        if edge_alpha_pixels(source):
            raise RuntimeError(f"source touches an outer edge: {spec['id']}")
        palette = list(spec["palette"])
        component, evidence = normalise(source, palette)
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe output: {spec['id']}")
        output_path = component_dir / f"{spec['id']}.png"
        component.save(output_path, optimize=True)
        entries[str(spec["id"])] = {
            "family": "washing",
            "label": spec["label"],
            "intent": "approved-new-version-v2",
            "priorLibraryVersion": 1,
            "currentLibraryVersion": 2,
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
    rejected = [{**item, "sha256": sha256(PACK / item["file"])} for item in REJECTED]
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-family-pack@1",
        "set": SET,
        "status": "approved-and-registered",
        "created": "2026-10-21",
        "tool": "built-in image generation plus deterministic fixed-palette normalisation",
        "family": "washing",
        "semanticSet": "the five pictures used by Claude's Washing up Bubble story",
        "primaryVisualCalibration": "art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/drafts/components/sandwich-tomato.png",
        "additionalVisualAuthority": "art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/drafts/components/bbq-tongs.png",
        "preservationRule": "Translate each current asset's drawing language while preserving subject identity, viewpoint, object count, construction, state, recognisable contents, relative arrangement and broad silhouette.",
        "storyFile": rel(STORY),
        "storySha256": STORY_SHA256,
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "components": entries,
        "rejected": rejected,
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
            "libraryVersionsAdded": True,
            "storyChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": {
            "by": "Frank",
            "date": "2026-10-21",
            "words": "approved continue - update your recipe as you go",
            "scope": "the exact five-picture washing family contact sheet",
        },
        "nextStep": "Continue with a new tightly related Bubble-story family using the evolving recipe and a new immutable review gate.",
        "rollback": "Set each picture's current selector back to V1; the approved V2 assets and all earlier bytes remain immutable and selectable.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(rows)} approved components in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "approved-and-registered":
        raise RuntimeError("register identity/status mismatch")
    if register["family"] != "washing" or register["approval"]["by"] != "Frank":
        raise RuntimeError("register family/approval mismatch")
    if sha256(STORY) != STORY_SHA256 or register["storySha256"] != STORY_SHA256:
        raise RuntimeError("Claude's washing-up story changed")
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
        if picture["current"] != 2 or len(picture["versions"]) != 2:
            raise RuntimeError(f"approved candidate is not current V2: {picture_id}")
        prior = next((version for version in picture["versions"] if version["v"] == 1), None)
        current = next((version for version in picture["versions"] if version["v"] == 2), None)
        if prior is None or prior["sha256"] != entry["currentReferenceSha256"]:
            raise RuntimeError(f"library V1 hash drift: {picture_id}")
        if current is None or current["sha256"] != entry["sha256"]:
            raise RuntimeError(f"library V2 hash drift: {picture_id}")
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
    if not register["checks"]["libraryVersionsAdded"]:
        raise RuntimeError("approved pack does not record registered versions")
    expected_hash_lines = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hash_lines:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {SET}: {len(expected_ids)} approved V2 components, contact sheet and retained V1 priors")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="verify existing outputs without rebuilding")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
