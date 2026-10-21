#!/usr/bin/env python3
"""Build or verify the review-gated ligne-claire General repair story pack."""

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
PACK = ROOT / "art/drafts/activity-story-ligne-claire-general-repair-2026-10-21-v1"
SET = "activity-story-ligne-claire-general-repair-2026-10-21-v1"
STORY = ROOT / "data/activity-stories/stories/general-repair.json"
STORY_SHA256 = "e174e6c3578c92ec417119917e0708300e596f2f26f28eedcddec0a5a58f9543"

SPECS: tuple[dict[str, object], ...] = (
    {
        "id": "repair-toolbox",
        "label": "Toolbox",
        "source": "repair-toolbox-source.png",
        "cache": "exec-939406d7-8741-42bd-90a1-7c3eebc9ccdb.png",
        "current": "review-archive/objects/bd/bddc65528cb63fed1403fcbd0de210af4b357585dac5660102512b706f459c10.png",
        "currentSha256": "bddc65528cb63fed1403fcbd0de210af4b357585dac5660102512b706f459c10",
        "palette": [INK, (13, 78, 117), (24, 112, 166), (231, 166, 56), (232, 139, 45), (232, 72, 51), (237, 233, 222), (151, 166, 172)],
        "preserves": "exactly one open blue metal toolbox with its raised lid, brass hardware and handle, plus the current visible spanner, pliers, screwdriver and smaller tool contents",
    },
    {
        "id": "repair-boat-hull-patch",
        "label": "Hull patch",
        "source": "repair-boat-hull-patch-source.png",
        "cache": "exec-6c1acbe0-cda2-40a9-aab1-545a3f0a867a.png",
        "current": "review-archive/objects/ce/cef61bcec5542ac32a74bcae933b972deab398bec5edfabd8ded71441b23c28e.png",
        "currentSha256": "cef61bcec5542ac32a74bcae933b972deab398bec5edfabd8ded71441b23c28e",
        "palette": [INK, (24, 112, 166), (166, 95, 42), (232, 139, 45), (246, 229, 183), (231, 166, 56), (73, 76, 82)],
        "preserves": "exactly four weathered blue hull planks, two horizontal battens, two short vertical straps, six visible brass fasteners and one wooden mallet in the current arrangement",
    },
    {
        "id": "repair-hammer-nails",
        "label": "Hammer and nails",
        "source": "repair-hammer-nails-source.png",
        "cache": "exec-f5767384-ff41-46fe-b6b7-61a28f7e3438.png",
        "current": "review-archive/objects/0c/0c71ed9d475b334ad85c2f6c7a190ae61a90bcf44c18974559f8a8e7e06632e9.png",
        "currentSha256": "0c71ed9d475b334ad85c2f6c7a190ae61a90bcf44c18974559f8a8e7e06632e9",
        "palette": [INK, (73, 76, 82), (171, 166, 156), (232, 139, 45), (24, 112, 166), (231, 166, 56)],
        "preserves": "exactly one diagonal claw hammer with its steel head, timber upper handle and blue lower grip, plus exactly three brass nails in the current fan",
    },
    {
        "id": "repair-wrench-cog",
        "label": "Wrench and cog",
        "source": "repair-wrench-cog-source.png",
        "cache": "exec-c83e004e-3a68-4d0c-94fa-ce707e4ed543.png",
        "current": "review-archive/objects/58/588a382fd46f0fbb2186db0e40613a6e02c8476d4b99bd53dd6d3b2f27861ea4.png",
        "currentSha256": "588a382fd46f0fbb2186db0e40613a6e02c8476d4b99bd53dd6d3b2f27861ea4",
        "palette": [INK, (246, 229, 183), (171, 157, 137), (231, 166, 56), (73, 76, 82), (166, 95, 42)],
        "preserves": "exactly one gold cog with dark inset hub behind one crossing combination spanner, including its open jaw, ring end and brown two-pin grip panel",
    },
    {
        "id": "repair-rope-knot",
        "label": "Rope knot",
        "source": "repair-rope-knot-source.png",
        "cache": "exec-e35cf3fc-68ee-4858-bdd0-183711d5a312.png",
        "current": "review-archive/objects/03/03f0806f550a4953ac72c0dc6e17745e00ef71d4d231177343de29e75e4436d5.png",
        "currentSha256": "03f0806f550a4953ac72c0dc6e17745e00ef71d4d231177343de29e75e4436d5",
        "palette": [INK, (246, 229, 183), (246, 205, 135), (231, 166, 56), (207, 92, 24)],
        "preserves": "one compact thick-rope knot following the current over-under path and horizontal silhouette, with exactly two bound ends and two frayed tassels",
    },
)

REJECTED: tuple[dict[str, str], ...] = (
    {
        "file": "rejected/repair-boat-hull-patch-three-count-prompt-v1.png",
        "cache": "exec-40bb0f89-7e94-4b0e-8433-982a696198f8.png",
        "reason": "The image retained the current four hull planks and six fasteners, but the prompt incorrectly asserted three planks and four total fasteners; rerun after an enlarged count audit.",
    },
    {
        "file": "rejected/repair-rope-knot-overcomplicated-v1.png",
        "cache": "exec-b51ebc2e-1154-45b8-a5db-3339774dc9d8.png",
        "reason": "The rope became an elaborate multi-loop braided knot instead of preserving the current compact over-under topology and silhouette.",
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
        "semanticSet": "the five object pictures used by Claude's General repair Bubble story",
        "primaryShapeCalibration": "art/drafts/activity-story-ligne-claire-washing-2026-10-21-v1/drafts/components/washing-plate.png",
        "primaryColourCalibration": "art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/drafts/components/sandwich-tomato.png",
        "evolvingRecipe": "Preserve exact semantic construction while favouring lively mostly-even near-black contour, flat opaque spot colour, minimal decisive detail and controlled hand-drawn asymmetry instead of sterile geometry.",
        "preservationRule": "Translate each current asset's drawing language while preserving subject identity, viewpoint, object count, construction, state, recognisable contents, relative arrangement and broad silhouette. Audit ambiguous counts enlarged before prompting.",
        "storyFile": rel(STORY),
        "storySha256": STORY_SHA256,
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
            "storyHashPinned": True,
            "exactPalettesRecorded": True,
            "contactSheetCoversEveryCandidate": True,
            "libraryVersionsAdded": False,
            "storyChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": None,
        "nextStep": "Frank reviews the exact five-picture contact sheet. On approval, add each candidate as immutable V2 with the official add-picture command; do not overwrite V1.",
        "rollback": "Before approval, discard this pack alone. After approval, set each picture's current selector back to V1; all earlier bytes remain immutable and selectable.",
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
    if sha256(STORY) != STORY_SHA256 or register["storySha256"] != STORY_SHA256:
        raise RuntimeError("Claude's general-repair story changed")
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
