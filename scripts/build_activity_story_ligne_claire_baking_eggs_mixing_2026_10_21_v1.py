#!/usr/bin/env python3
"""Build or verify the review-gated ligne-claire baking/eggs/mixing pack."""

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
PACK = ROOT / "art/drafts/activity-story-ligne-claire-baking-eggs-mixing-2026-10-21-v1"
SET = "activity-story-ligne-claire-baking-eggs-mixing-2026-10-21-v1"

CREAM = (246, 229, 183)
LIGHT = (246, 205, 135)
GOLD = (231, 166, 56)
ORANGE = (232, 139, 45)
BROWN = (166, 95, 42)
DARK_BROWN = (116, 65, 40)
RED = (232, 72, 51)
DARK_RED = (195, 43, 55)
BLUE = (24, 112, 166)
DARK_BLUE = (13, 78, 117)

SPECS: tuple[dict[str, object], ...] = (
    {
        "id": "baking-flour",
        "label": "Baking flour",
        "source": "baking-flour-source.png",
        "cache": "exec-059de055-5dc7-4c14-816e-6c43e28b0dab.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/baking-flour.png",
        "currentSha256": "80a4ec6ed2e1a4e9fb898c937f1c9d80ddd2239d27261358e4bc18e6433ce830",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, BROWN, DARK_BROWN],
        "preserves": "one open folded flour sack, one filled adult wooden scoop at front-right, and the current loose flour pile and scattered grains",
    },
    {
        "id": "eggs-basket",
        "label": "Eggs basket",
        "source": "eggs-basket-source.png",
        "cache": "exec-4ec996fb-5b02-4d8d-91ce-1c4b8aee79a6.png",
        "current": "art/drafts/activity-cloud-composer-2026-10-19-v5/drafts/components/eggs-basket.png",
        "currentSha256": "7dddec98a124dc65bf908a7e45068c7fc0bd86c4c3645071d6b848f4f4776b76",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, BROWN, DARK_BROWN, BLUE, DARK_BLUE],
        "preserves": "one low woven basket with one arched braided handle, exactly four visible eggs, one two-blue-stripe cream cloth and the side fastening",
    },
    {
        "id": "eggs-hen-coop",
        "label": "Eggs hen coop",
        "source": "eggs-hen-coop-source.png",
        "cache": "exec-90f3960e-2239-4c71-8b86-d626805a09f1.png",
        "current": "art/drafts/activity-cloud-composer-2026-10-19-v5/drafts/components/eggs-hen-coop.png",
        "currentSha256": "4c5c10ba6212cdf35c695b384f30dc52c18e5b1f13737aa4a282b8bff425c50d",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, BROWN, DARK_BROWN, RED, DARK_RED, BLUE, DARK_BLUE],
        "preserves": "one adult brown-and-cream hen in front-left of one small blue-green pitched-roof coop with dark doorway and spilling straw",
    },
    {
        "id": "eggs-nest",
        "label": "Eggs nest",
        "source": "eggs-nest-source.png",
        "cache": "exec-768ca883-a831-4a05-9bc8-3f40cc4d75c5.png",
        "current": "art/drafts/activity-cloud-composer-2026-10-19-v5/drafts/components/eggs-nest.png",
        "currentSha256": "e863dbed7c72829c10a33ae89acbe588b47f4d385f8a1bfbaca474e0864bf349",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, BROWN, DARK_BROWN],
        "preserves": "one compact shallow straw nest with exactly four visible eggs, two warm brown and two cream, in the current overlap",
    },
    {
        "id": "ingredient-butter-block",
        "label": "Butter",
        "source": "ingredient-butter-block-source.png",
        "cache": "exec-8ff9b684-0b93-400e-b0f6-8447d7c50fab.png",
        "current": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/ingredient-butter-block.png",
        "currentSha256": "0dcf64e538831b23f10de0de4f2a773b84271470417c1908642b11fc0c847e59",
        "palette": [INK, CREAM, LIGHT, (242, 201, 76), GOLD, BLUE, DARK_BLUE],
        "preserves": "one large golden butter block and exactly one thick front-right slice on one opened cream wrapper with dark-blue underside",
    },
    {
        "id": "mixing-bowl",
        "label": "Mixing bowl",
        "source": "mixing-bowl-source.png",
        "cache": "exec-9f989e6e-dcbb-4cfb-b270-2f59f5982207.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/drafts/callouts/mixing-bowl.png",
        "currentSha256": "2cae4495779bdd4da3c9a1d0875b870a47cda30419f43555544616bc3052ef9a",
        "palette": [INK, CREAM, LIGHT, ORANGE, GOLD, BROWN, BLUE, DARK_BLUE],
        "preserves": "one low cream bowl with two blue bands, orange spiral batter, two detached left splash shapes and one small right-side batter dot",
    },
    {
        "id": "mixing-egg",
        "label": "Mixing egg",
        "source": "mixing-egg-source.png",
        "cache": "exec-846c57a3-8d00-4491-ad3c-b331120c16da.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/drafts/callouts/mixing-egg.png",
        "currentSha256": "97d7b75641c4c580e672a7621f4d3114ef3c300d71de5439084f52522810b1df",
        "palette": [INK, CREAM, LIGHT, (242, 201, 76), GOLD, ORANGE, BROWN],
        "preserves": "one freshly cracked egg with exactly two shell halves, one intact yolk, pooled white and the current two detached drops",
    },
    {
        "id": "mixing-flour",
        "label": "Mixing flour",
        "source": "mixing-flour-source.png",
        "cache": "exec-a4738f53-83d7-4e0d-bb98-e883f701b382.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/drafts/callouts/mixing-flour.png",
        "currentSha256": "5734cdf3a8b777e10bb9a1ecb85d97029a28f2f4aff8d40e1385fcfbb6ee6d09",
        "palette": [INK, CREAM, LIGHT, DARK_BLUE],
        "preserves": "one compact overlapping-lobe flour puff, the current detached-dot field and exactly two dark-blue upper-right emphasis rays",
    },
    {
        "id": "mixing-whisk",
        "label": "Mixing whisk",
        "source": "mixing-whisk-source.png",
        "cache": "exec-af487215-b1f7-4ca5-baf0-f3868f6ebe91.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/drafts/callouts/mixing-whisk.png",
        "currentSha256": "8246369441e5bfe99eea3c60f746e6204b9282ddca0a106aa5cfe22a38eb2c8c",
        "palette": [INK, CREAM, GOLD, ORANGE, BROWN, DARK_BROWN, BLUE, DARK_BLUE],
        "preserves": "one diagonal adult balloon whisk with tapered wooden handle, golden ferrule, dark-blue wire cage, batter coating and separate drops",
    },
)

REJECTED = ({
    "file": "rejected/eggs-hen-coop-cartoon-eye-v1.png",
    "cache": "exec-35f38e9d-43fd-4d09-a12e-05be1bca5f16.png",
    "reason": "The construction was sound, but the enlarged eye and dense feather treatment drifted toward mascot/cartoon language; corrected with a restrained adult eye and simpler interior detail.",
},)


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
            "family": str(spec["id"]).split("-")[0],
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
        "family": "baking-eggs-mixing",
        "semanticSet": "nine related flour, egg, butter and mixing pictures from the Food and meals menu group",
        "styleChampions": {
            "washing-plate": "living hand-drawn shape and controlled minor imperfection",
            "sandwich-tomato": "flat colour economy and selective readable detail",
            "repair-toolbox": "construction, detail hierarchy and confident object presence",
        },
        "evolvingRecipe": "Observational ligne claire, not cartoon: preserve literal counts, construction, overlap, viewpoint and state; use lively mostly-even near-black contour, flat opaque spot colour, minimal decisive interior lines and controlled human irregularity. For animals, keep adult anatomy and a restrained natural eye; simplify feather or fibre detail before it becomes mascot or texture rendering.",
        "preservationRule": "Treat every current V1 as sole semantic and compositional authority. Preserve literal objects and counts, ingredient state, construction, relative arrangement, broad silhouette and detached action marks; style references never override content.",
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
    print(f"Built and verified {len(rows)} baking/eggs/mixing review candidates in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "review-gate-awaiting-approval":
        raise RuntimeError("register identity/status mismatch")
    if register["family"] != "baking-eggs-mixing" or register["approval"] is not None:
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
