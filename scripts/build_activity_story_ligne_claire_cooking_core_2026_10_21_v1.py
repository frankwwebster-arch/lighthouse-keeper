#!/usr/bin/env python3
"""Build or verify the review-gated ligne-claire cooking-core pack."""

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
PACK = ROOT / "art/drafts/activity-story-ligne-claire-cooking-core-2026-10-21-v1"
SET = "activity-story-ligne-claire-cooking-core-2026-10-21-v1"

SPECS: tuple[dict[str, object], ...] = (
    {
        "id": "cooking-bacon",
        "label": "Cooking bacon",
        "source": "cooking-bacon-source.png",
        "cache": "exec-adeb2ce4-dc75-4cdd-b36c-6a4a2f922819.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/cooking-bacon.png",
        "currentSha256": "2bc0d1bcb08b12985fc82841d3e02cabceceb13ecdb633d8bd28319527f1c323",
        "palette": [INK, (246, 229, 183), (232, 72, 51), (195, 43, 55), (232, 139, 45), (13, 78, 117), (24, 112, 166)],
        "preserves": "one shallow cream oval plate with blue rim and exactly three overlapping wavy cooked bacon rashers with red meat and cream fat bands",
    },
    {
        "id": "cooking-cheese-slicing",
        "label": "Cheese being sliced",
        "source": "cooking-cheese-slicing-source.png",
        "cache": "exec-8a192b89-78ea-4d32-95a5-111614e1e93d.png",
        "current": "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/assets/cooking-cheese-slicing.png",
        "currentSha256": "ca7d2733d7f22b350602566aef641065c5321acd298b9e6611bf8c1e8fd5cb35",
        "palette": [INK, (246, 229, 183), (246, 205, 135), (231, 166, 56), (13, 78, 117), (24, 112, 166), (171, 166, 156), (73, 76, 82)],
        "preserves": "one large golden cheese block, one separated rectangular slice and one diagonal adult knife with blue three-pin handle in the current overlap",
    },
    {
        "id": "cooking-gravy",
        "label": "Cooking gravy",
        "source": "cooking-gravy-source.png",
        "cache": "exec-17e0b3b3-e278-4558-af25-dc324ef11c62.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/cooking-gravy.png",
        "currentSha256": "e31e4153eab4a977e62d0b3b7bcd0d03f779da5e80d0ad3d94a26dfd09de9b0f",
        "palette": [INK, (246, 229, 183), (246, 205, 135), (13, 78, 117), (24, 112, 166), (232, 139, 45), (166, 95, 42), (116, 65, 40)],
        "preserves": "one filled cream gravy boat with left spout, right loop handle, blue band, pedestal foot and dark brown gravy",
    },
    {
        "id": "cooking-knife",
        "label": "Cooking knife",
        "source": "cooking-knife-source.png",
        "cache": "exec-d28a72f2-9ac6-4aac-88c6-13ddd1c41e49.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/cooking-knife.png",
        "currentSha256": "8c1e77edeeb466f7b445a3f916738525ed4ddaae6606ca1590889a6d5f416d1a",
        "palette": [INK, (246, 229, 183), (171, 166, 156), (73, 76, 82), (166, 95, 42), (207, 92, 24), (231, 166, 56)],
        "preserves": "one diagonal adult chef's knife with broad pointed steel blade, brass bolster and brown wooden handle with exactly three rivets",
    },
    {
        "id": "cooking-pan",
        "label": "Cooking pan",
        "source": "cooking-pan-source.png",
        "cache": "exec-a0037f98-0b55-4d24-ac2a-1b4731e78437.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/drafts/callouts/cooking-pan.png",
        "currentSha256": "0ec54ca7575b962e5fae9f321cf4883208c6da9a4f7da6c33a84289c49254642",
        "palette": [INK, (73, 76, 82), (232, 72, 51), (207, 92, 24), (232, 139, 45), (166, 95, 42), (231, 166, 56), (246, 205, 135)],
        "preserves": "one low copper frying pan with dark inner surface and brown handle, one pancake in mid-flip and the current separate droplets and action ticks",
    },
    {
        "id": "cooking-seasoning",
        "label": "Cooking seasoning",
        "source": "cooking-seasoning-source.png",
        "cache": "exec-7e63b8e0-9bd4-48e0-a4b3-a86981a0d22d.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/drafts/callouts/cooking-seasoning.png",
        "currentSha256": "208e02a5b2e7ae1508327c8ad2dcdc7ed2b78947d0a40de37b62e9e365092438",
        "palette": [INK, (232, 72, 51), (207, 92, 24), (232, 139, 45), (231, 166, 56), (246, 205, 135)],
        "preserves": "the current open burst of separate red-brown flakes, golden pieces and small grains with three dark directional emphasis strokes",
    },
    {
        "id": "cooking-spoon",
        "label": "Cooking spoon",
        "source": "cooking-spoon-source.png",
        "cache": "exec-a97dad0e-5cff-4972-ae29-0de8fc3ec227.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/drafts/callouts/cooking-spoon.png",
        "currentSha256": "0793c1ea85d3a38d024de9c788ac3368dafc7c7270a65f65feb03beb10c005f8",
        "palette": [INK, (116, 65, 40), (166, 95, 42), (207, 92, 24), (232, 139, 45), (246, 205, 135)],
        "preserves": "one diagonal adult wooden spoon with deep oval bowl, long tapered handle, one hanging hole and exactly four dark emphasis ticks",
    },
    {
        "id": "cooking-steam",
        "label": "Cooking steam",
        "source": "cooking-steam-source.png",
        "cache": "exec-0df8b9a4-9671-4039-885f-3f9cd3071a2d.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/drafts/callouts/cooking-steam.png",
        "currentSha256": "440c359bcda03d83e026705cbb727c6e79b3d0e9bdf8812488ed0a72aac1b395",
        "palette": [INK, (246, 229, 183), (246, 205, 135), (231, 166, 56)],
        "preserves": "exactly three separate rising cream steam curls in the left-small, centre-tall, right-small arrangement plus exactly two detached wisps",
    },
    {
        "id": "cooking-vegetables",
        "label": "Cooking vegetables",
        "source": "cooking-vegetables-source.png",
        "cache": "exec-a449b9a6-424e-43ea-9d8a-1237a5420e8b.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/cooking-vegetables.png",
        "currentSha256": "92f3c0c1e740bd4e3602d9c1def9a4d558fd8840f31bceea2ca62846145a4384",
        "palette": [INK, (232, 72, 51), (195, 43, 55), (207, 92, 24), (232, 139, 45), (231, 166, 56), (57, 148, 55), (87, 174, 58), (246, 205, 135)],
        "preserves": "one carrot with greens, leafy vegetables, green peas, orange rounds and cubes, exactly one whole red tomato and one tomato wedge in the current compact mound",
    },
)

REJECTED: tuple[dict[str, str], ...] = (
    {
        "file": "rejected/cooking-cheese-slicing-two-rivet-prompt-v1.png",
        "cache": "exec-d3194a45-8e84-4af3-85e2-dd8a94e5bb9b.png",
        "reason": "The output showed three rivets, but its prompt incorrectly called the current knife handle a two-rivet construction; rerendered after enlarged inspection confirmed three rivets.",
    },
    {
        "file": "rejected/cooking-vegetables-two-tomato-prompt-v1.png",
        "cache": "exec-db4ce6eb-097d-42f1-876e-7a1022c4a3c5.png",
        "reason": "The candidate remained visually close, but its prompt incorrectly asserted two whole tomatoes; rerendered after enlarged inspection confirmed one whole tomato and one wedge.",
    },
    {
        "file": "rejected/cooking-knife-speckled-v1.png",
        "cache": "exec-023c2493-e3f9-4014-821f-ddb5b1a239a0.png",
        "reason": "The construction was sound, but pale blade speckling and surface noise violated the approved flat-colour economy.",
    },
    {
        "file": "rejected/cooking-pan-distressed-v1.png",
        "cache": "exec-9ce4622b-1ca2-4220-8911-2c2dca665909.png",
        "reason": "The action and construction were sound, but decorative copper distress and mottling violated the approved flat-colour economy.",
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
            "family": "cooking",
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
        "family": "cooking",
        "semanticSet": "nine core cooking food, utensil and action pictures from the Food and meals menu group",
        "styleChampions": {
            "washing-plate": "living hand-drawn shape and controlled minor imperfection",
            "sandwich-tomato": "flat colour economy and selective readable detail",
            "repair-toolbox": "construction, detail hierarchy and confident object presence",
            "repair-spirit-level": "restrained adult technical-object proportions",
        },
        "evolvingRecipe": "Observational ligne claire, not cartoon: preserve literal counts, construction, overlap and state; use lively mostly-even near-black contour, flat opaque spot colour, minimal decisive interior lines and controlled human irregularity.",
        "preservationRule": "Translate each current asset's drawing language while preserving subject identity, viewpoint, object count, construction, state, recognisable contents, relative arrangement and broad silhouette. Audit ambiguous counts enlarged before prompting and reject even visually plausible outputs when prompt provenance is wrong.",
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
            "storyChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": None,
        "nextStep": "Frank reviews this exact nine-picture contact sheet. Register no candidate before explicit approval.",
        "rollback": "Before approval, discard this pack alone. After approval, each V1 remains immutable and can be reselected independently.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(rows)} cooking-core review candidates in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "review-gate-awaiting-approval":
        raise RuntimeError("register identity/status mismatch")
    if register["family"] != "cooking" or register["approval"] is not None:
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
            raise RuntimeError(f"candidate was registered before approval: {picture_id}")
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
    if not contact_path.is_file() or sha256(contact_path) != evidence["sha256"]:
        raise RuntimeError("contact sheet hash mismatch")
    contact = Image.open(contact_path)
    if contact.mode != "RGBA" or contact.size != (CELL * 5, HEADER + ROW_HEIGHT * len(expected_ids)):
        raise RuntimeError("contact sheet geometry mismatch")
    if evidence["coveredIds"] != expected_ids or evidence["rows"] != len(expected_ids) or evidence["columns"] != 5:
        raise RuntimeError("contact sheet coverage metadata mismatch")
    if register["checks"]["libraryVersionsAdded"]:
        raise RuntimeError("unapproved pack records registered versions")
    expected_hash_lines = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hash_lines:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {SET}: {len(expected_ids)} unregistered candidates, contact sheet and retained V1 priors")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="verify existing outputs without rebuilding")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
