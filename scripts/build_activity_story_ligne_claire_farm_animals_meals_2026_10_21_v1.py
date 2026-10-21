#!/usr/bin/env python3
"""Build or verify the farm-animal full-redraft and plated-meals review gate."""

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
PACK = ROOT / "art/drafts/activity-story-ligne-claire-farm-animals-meals-2026-10-21-v1"
SET = "activity-story-ligne-claire-farm-animals-meals-2026-10-21-v1"
HORSE_REFERENCE = PACK / "references/frank-horse-ligne-claire-reference.png"

CREAM = (246, 229, 183)
LIGHT = (237, 233, 222)
GOLD = (231, 166, 56)
ORANGE = (232, 139, 45)
RED = (232, 72, 51)
DARK_RED = (195, 43, 55)
PINK = (245, 126, 106)
DARK_PINK = (215, 91, 82)
BROWN = (166, 95, 42)
DARK_BROWN = (116, 65, 40)
GREEN = (73, 145, 55)
DARK_GREEN = (37, 104, 48)
BLUE = (24, 112, 166)
DARK_BLUE = (13, 78, 117)
CHARCOAL = (48, 52, 58)

SPECS = (
    {
        "id": "cooking-cow",
        "label": "Adult dairy cow — full redraft",
        "source": "cooking-cow-source.png",
        "cache": "exec-6faf94f0-7779-4cd6-ad3e-c98a74cbaed0.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/cooking-cow.png",
        "currentSha256": "596bc5a5cbb4eec1e48a34ca796b852aa303a027403f3aea5a29ae304af99dac",
        "palette": [INK, CHARCOAL, CREAM, LIGHT, PINK, DARK_PINK, BROWN, DARK_BROWN, GOLD],
        "method": "full-redraft-from-observed-anatomy",
        "preserves": "one adult black-and-cream dairy cow, standing left-to-right with small horns, udder, long tail and one small neck bell; legacy cartoon anatomy was deliberately discarded",
    },
    {
        "id": "cooking-pig",
        "label": "Adult farm pig — full redraft",
        "source": "cooking-pig-source.png",
        "cache": "exec-c2b3e5e0-9a11-4bd9-bbe8-034a77f1e064.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/cooking-pig.png",
        "currentSha256": "45e8deec49338efda30efeeb0f9eb4e26687c147487cfb9ec393132b1228ca9b",
        "palette": [INK, PINK, DARK_PINK, RED, DARK_RED, BROWN, CHARCOAL],
        "method": "full-redraft-from-observed-anatomy",
        "preserves": "one adult warm-pink farm pig, standing left-to-right with folded ears, broad disk snout, cloven hooves and one curled tail; legacy cartoon anatomy was deliberately discarded",
    },
    {
        "id": "cooking-sheep",
        "label": "Adult sheep — full redraft",
        "source": "cooking-sheep-source.png",
        "cache": "exec-7d2b1254-faaf-42eb-941c-35612c749727.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/cooking-sheep.png",
        "currentSha256": "cc66915a7b0cd541332664b6c2233797b884c55c3ad46fe24af66794d659725e",
        "palette": [INK, CHARCOAL, CREAM, LIGHT, GOLD, BROWN],
        "method": "full-redraft-from-observed-anatomy",
        "preserves": "one adult cream-fleeced sheep with charcoal face and legs, standing left-to-right with head at left; legacy cartoon anatomy and cloud-like fleece were deliberately discarded",
    },
    {
        "id": "meal-breakfast",
        "label": "Breakfast",
        "source": "meal-breakfast-source.png",
        "cache": "exec-9a039209-2f7e-4eff-b66a-169f412ff34e.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/meal-breakfast.png",
        "currentSha256": "ec4665ac718fc8892fcfff9701c0f29c17e1667ae77ce68d3eb8446897f5a17c",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, RED, DARK_RED, GREEN, DARK_GREEN, BLUE, DARK_BLUE, BROWN],
        "method": "composition-preserving-style-translation",
        "preserves": "one blue-rimmed plate, two toast slices, three bacon rashers, one fried egg with one yolk and two tomato halves with herb leaves in the current arrangement",
    },
    {
        "id": "meal-dinner",
        "label": "Roast dinner",
        "source": "meal-dinner-source.png",
        "cache": "exec-7a397300-d4f4-4fd0-8615-ee07e77a9f6f.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/meal-dinner.png",
        "currentSha256": "b156ae100f31c4ee20ee1c7ae53df0d0bf16f25ec767ff0ddda898e0ad7f0237",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, BROWN, DARK_BROWN, GREEN, DARK_GREEN, BLUE, DARK_BLUE],
        "method": "composition-preserving-style-translation",
        "preserves": "one blue-rimmed plate with three roast-poultry slices and gravy, three roast potatoes, two broccoli florets, three carrot pieces and the upper-right green sprig",
    },
    {
        "id": "meal-lunch",
        "label": "Vegetable soup lunch",
        "source": "meal-lunch-source.png",
        "cache": "exec-23c9785e-370f-45ea-b919-88b8b546554a.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/meal-lunch.png",
        "currentSha256": "72d65ca5186260c3cb99b802c0be79ed0cfc7d4cb1573a70ed210e5f5d10519c",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, GREEN, DARK_GREEN, BLUE, DARK_BLUE, BROWN],
        "method": "composition-preserving-style-translation",
        "preserves": "one cream footed bowl with two blue bands, orange vegetable soup, four potato cubes, two carrot chunks, green leaves and parsley, plus one bread slice and one front parsley sprig",
    },
    {
        "id": "meal-steak-fries",
        "label": "Steak and fries",
        "source": "meal-steak-fries-source.png",
        "cache": "exec-2dbe2575-79dd-401c-8304-b9ee3b8e4682.png",
        "current": "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/assets/meal-steak-fries.png",
        "currentSha256": "8aebdcafac1a8c2749f9876fc51d2fc1c7bbe78005120b0bb8b5ca5b657c99ae",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, RED, DARK_RED, BROWN, DARK_BROWN, BLUE, DARK_BLUE],
        "method": "composition-preserving-style-translation",
        "preserves": "one blue-rimmed plate with one thick rectangular steak at left/front, its fat edge and five diagonal grill bands, plus the compact overlapping pile of thick fries at right/rear",
    },
)

REJECTED = (
    {
        "file": "rejected/cooking-cow-pre-horse-reference.png",
        "cache": "exec-d60b6cac-ee3e-40f0-8ea0-93718c9b6ce6.png",
        "reason": "Superseded before the gate when Frank supplied a specific ligne-claire horse reference for animal construction.",
    },
    {
        "file": "rejected/cooking-pig-pre-horse-reference.png",
        "cache": "exec-f2ddbeca-ebeb-48c5-8565-f31cafa74bb6.png",
        "reason": "Superseded before the gate when Frank supplied a specific ligne-claire horse reference for animal construction.",
    },
    {
        "file": "rejected/cooking-sheep-pre-horse-reference.png",
        "cache": "exec-f3ff2c06-bbce-45d2-8a65-3df01f444608.png",
        "reason": "Superseded before the gate when Frank supplied a specific ligne-claire horse reference for animal construction.",
    },
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def library_entries() -> dict[str, dict[str, object]]:
    return json.loads((ROOT / "data/activity-stories/pictures.json").read_text())["pictures"]


def build() -> None:
    component_dir = PACK / "drafts/components"
    evidence_dir = PACK / "evidence"
    component_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    entries: dict[str, object] = {}
    rows: list[tuple[dict[str, object], Image.Image]] = []
    for spec in SPECS:
        current_path = ROOT / spec["current"]
        source_path = PACK / "source" / spec["source"]
        if sha256(current_path) != spec["currentSha256"]:
            raise RuntimeError(f"current source drift: {spec['id']}")
        source = Image.open(source_path)
        if source.mode != "RGBA" or edge_alpha_pixels(source):
            raise RuntimeError(f"unsafe source: {spec['id']}")
        component, evidence = normalise(source, list(spec["palette"]))
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe output: {spec['id']}")
        output_path = component_dir / f"{spec['id']}.png"
        component.save(output_path, optimize=True)
        entries[spec["id"]] = {
            "family": "food-provenance" if spec["id"].startswith("cooking-") else "meal",
            "label": spec["label"],
            "intent": "candidate-new-version-v2",
            "method": spec["method"],
            "priorCurrentLibraryVersion": 1,
            "proposedLibraryVersion": 2,
            "preserves": spec["preserves"],
            "currentReferenceFile": spec["current"],
            "currentReferenceSha256": spec["currentSha256"],
            "sourceFile": rel(source_path),
            "sourceSha256": sha256(source_path),
            "sourcePixels": list(source.size),
            "originalCacheFile": spec["cache"],
            "flatPalette": ["#%02x%02x%02x" % colour for colour in spec["palette"]],
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
        "family": "food-provenance-and-meal",
        "semanticSet": "three fully redrafted adult farm animals plus four composition-preserving plated meals",
        "styleChampions": {
            "frank-horse-reference": "primary animal construction authority: weight-bearing anatomy, lively economical contour and sparse interior marks",
            "washing-plate": "living hand-drawn shape and controlled minor imperfection",
            "sandwich-tomato": "flat-colour economy and selective readable detail",
            "repair-toolbox": "construction, detail hierarchy and confident object presence",
        },
        "animalRedraftRule": "Legacy animal drawings constrain only species, count, orientation and indispensable semantic attributes. Anatomy, stance, proportions, face, contour and interior construction are newly drawn from observation; this is not style transfer.",
        "mealPreservationRule": "The current V1 remains sole semantic/compositional authority for each meal: preserve plate or bowl, food counts, state, viewpoint, overlap, relative arrangement and broad silhouette.",
        "horseReference": {"file": rel(HORSE_REFERENCE), "sha256": sha256(HORSE_REFERENCE), "role": "user-supplied animal style/construction reference"},
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
            "animalSourcesExcludeLegacyCartoonArt": True,
            "horseReferencePinned": True,
            "sourceEdgesClear": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "currentReferenceHashesPinned": True,
            "exactPalettesRecorded": True,
            "contactSheetCoversEveryCandidate": True,
            "libraryVersionsAdded": False,
            "storyChanged": False,
            "activityStoriesRuntimeChanged": False,
            "deployed": False,
        },
        "approval": None,
        "nextStep": "Frank reviews this exact seven-picture sheet. Register no candidate before explicit approval.",
        "rollback": "Discard this pack alone; every current V1 and all prior immutable packs remain untouched.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(SPECS)} unregistered farm-animal/meal candidates in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "review-gate-awaiting-approval":
        raise RuntimeError("register identity/status mismatch")
    if register["approval"] is not None or not register["checks"]["animalSourcesExcludeLegacyCartoonArt"]:
        raise RuntimeError("register approval/redraft mismatch")
    expected_ids = [spec["id"] for spec in SPECS]
    if list(register["components"]) != expected_ids:
        raise RuntimeError("register component order/coverage mismatch")
    if sha256(HORSE_REFERENCE) != register["horseReference"]["sha256"]:
        raise RuntimeError("horse reference hash mismatch")
    library = library_entries()
    for spec in SPECS:
        picture_id = spec["id"]
        entry = register["components"][picture_id]
        source_path = ROOT / entry["sourceFile"]
        output_path = ROOT / entry["file"]
        current_path = ROOT / entry["currentReferenceFile"]
        for path in (source_path, output_path, current_path):
            if not path.is_file():
                raise RuntimeError(f"missing manifest path: {path}")
        if sha256(source_path) != entry["sourceSha256"] or sha256(output_path) != entry["sha256"]:
            raise RuntimeError(f"source/component hash mismatch: {picture_id}")
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
        bounds = visible_bounds(output)
        if list(bounds) != entry["bounds"]:
            raise RuntimeError(f"bounds mismatch: {picture_id}")
        gutter = min(bounds[0], bounds[1], CELL - bounds[2], CELL - bounds[3])
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
            raise RuntimeError(f"rejected source mismatch: {item['file']}")
    evidence = register["evidence"]
    contact_path = ROOT / evidence["file"]
    if not contact_path.is_file() or sha256(contact_path) != evidence["sha256"]:
        raise RuntimeError("contact sheet hash mismatch")
    contact = Image.open(contact_path)
    if contact.mode != "RGBA" or contact.size != (CELL * 5, HEADER + ROW_HEIGHT * len(SPECS)):
        raise RuntimeError("contact sheet geometry mismatch")
    if evidence["coveredIds"] != expected_ids or evidence["rows"] != len(SPECS) or evidence["columns"] != 5:
        raise RuntimeError("contact sheet coverage mismatch")
    expected_hashes = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hashes:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {SET}: seven candidates remain unregistered; all V1 priors retained")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
