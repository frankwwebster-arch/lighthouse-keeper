#!/usr/bin/env python3
"""Build or verify the unregistered ligne-claire condiment-family review pack."""

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
PACK = ROOT / "art/drafts/activity-story-ligne-claire-condiments-2026-10-21-v1"
SET = "activity-story-ligne-claire-condiments-2026-10-21-v1"

CREAM = (246, 229, 183)
LIGHT = (237, 233, 222)
PALE_BLUE = (151, 202, 218)
BLUE = (24, 112, 166)
DARK_BLUE = (13, 78, 117)
GOLD = (231, 166, 56)
ORANGE = (232, 139, 45)
BROWN = (166, 95, 42)
DARK_BROWN = (116, 65, 40)
RED = (232, 72, 51)
DARK_RED = (195, 43, 55)
PINK = (245, 126, 106)
GREEN = (73, 145, 55)
DARK_GREEN = (37, 104, 48)
OLIVE = (147, 150, 38)

SPECS: tuple[dict[str, object], ...] = (
    {
        "id": "condiment-honey-pot",
        "label": "Honey pot",
        "source": "condiment-honey-pot-source.png",
        "cache": "exec-d8ebc6b7-0939-4e73-a71a-974b5fc42919.png",
        "current": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-honey-pot.png",
        "currentSha256": "e8a1d55341f198f0eb7e2018ea4ca8e37d7f9452cc81e6e601c9be3418c4b5b4",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, ORANGE, BROWN, DARK_BROWN],
        "preserves": "one squat round clear-glass honey pot with honey, blank cream front label, wooden lid and one grooved wooden dipper resting left-to-right across the top",
    },
    {
        "id": "condiment-ketchup-bottle",
        "label": "Ketchup",
        "source": "condiment-ketchup-bottle-source.png",
        "cache": "exec-63ae6da2-d839-43f1-8397-a42f90caa235.png",
        "current": "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/assets/condiment-ketchup-bottle.png",
        "currentSha256": "153cdd6ac24624c2ffad96e7c990ece2c1a53972adb3f4e67b0f51b340ffcb49",
        "palette": [INK, RED, DARK_RED, PINK],
        "preserves": "one plain red plastic squeeze bottle in front view with cylindrical body, rounded shoulders, ribbed screw collar and pointed dispensing nozzle",
    },
    {
        "id": "condiment-malt-vinegar",
        "label": "Malt vinegar",
        "source": "condiment-malt-vinegar-source.png",
        "cache": "exec-ad76e433-0505-4b58-bd03-10a162467620.png",
        "current": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-malt-vinegar.png",
        "currentSha256": "99e49748fc316803a5b7743a8c4ac063a879498c25258c8a65ca5572397fd672",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, ORANGE, BROWN, DARK_BROWN],
        "preserves": "one clear-glass malt-vinegar cruet with amber vinegar, rounded stopper, narrow neck, left pouring lip, right loop handle and blank cream label",
    },
    {
        "id": "condiment-mayonnaise-jar",
        "label": "Mayonnaise",
        "source": "condiment-mayonnaise-jar-source.png",
        "cache": "exec-87aef70b-f423-438a-8f8d-38ae1386e351.png",
        "current": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-mayonnaise-jar.png",
        "currentSha256": "7d503285bc4ccf5cb098741c569b01a4887e4806e3c6147f97b480311be95d25",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, BLUE, DARK_BLUE, GOLD],
        "preserves": "one squat clear-glass mayonnaise jar with pale mayonnaise and one surface curl, dark-blue ribbed screw lid and blank cream wrap label",
    },
    {
        "id": "condiment-mustard-bottle",
        "label": "Mustard",
        "source": "condiment-mustard-bottle-source.png",
        "cache": "exec-d2cd2e65-f2bd-462e-a925-bf65c4603d13.png",
        "current": "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/assets/condiment-mustard-bottle.png",
        "currentSha256": "65c2f38eec206e0f07160f8d8e1ae6dd4ce2b415154a73ca845508f2fdbd44ee",
        "palette": [INK, CREAM, GOLD, ORANGE],
        "preserves": "one plain yellow plastic squeeze bottle in front view with cylindrical body, rounded shoulders, ribbed screw collar and pointed dispensing nozzle",
    },
    {
        "id": "condiment-olive-oil",
        "label": "Olive oil",
        "source": "condiment-olive-oil-source.png",
        "cache": "exec-6b55c0e6-edb6-4bae-8068-ef1b741e2036.png",
        "current": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-olive-oil.png",
        "currentSha256": "102d543540a2675c5b82575f5fc332585e6b3749bfdced4c1f162e087c49d124",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, OLIVE, GREEN, BROWN],
        "preserves": "one clear-glass olive-oil bottle with rounded low body, narrow neck, flared lip, natural cork, golden-green oil and blank cream front label",
    },
    {
        "id": "condiment-pickle-jar",
        "label": "Pickle jar",
        "source": "condiment-pickle-jar-source.png",
        "cache": "exec-595849fa-6674-4842-9860-27977eb13d8e.png",
        "current": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-pickle-jar.png",
        "currentSha256": "a48fc115e5ef7cc8a8200f3a26d53667e740e97473ee5c5bb9c8c70e9b81d9e4",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, OLIVE, GREEN, DARK_GREEN, BROWN],
        "preserves": "one tall clear-glass pickle jar with cream screw lid, blank cream front label, green brine and several overlapping whole gherkins",
    },
    {
        "id": "condiment-raspberry-jam",
        "label": "Raspberry jam",
        "source": "condiment-raspberry-jam-source.png",
        "cache": "exec-bde92ed5-385f-4a36-adac-f4112fa03ccf.png",
        "current": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-raspberry-jam.png",
        "currentSha256": "dfc5ce3f9d6ccd334bd8e6eed5ba71d203c80b7542b85e64fcf9c6d90ef2b23b",
        "palette": [INK, CREAM, LIGHT, BLUE, DARK_BLUE, RED, DARK_RED, PINK, GOLD, BROWN],
        "preserves": "one squat clear-glass raspberry-jam jar with blank cream front label, red jam and fruit cues, blue-and-cream checked cloth cap and one ochre cord bow tied at right",
    },
    {
        "id": "condiment-wholegrain-mustard-jar",
        "label": "Wholegrain mustard",
        "source": "condiment-wholegrain-mustard-jar-source.png",
        "cache": "exec-31446f5a-79fc-4f0e-8906-0161f87e83c1.png",
        "current": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-wholegrain-mustard-jar.png",
        "currentSha256": "5f0739bd891dd0475e5f3827a3392fbfac6df9c584ca73937591db7c9cf4b74c",
        "palette": [INK, CREAM, LIGHT, GOLD, ORANGE, BROWN, DARK_BROWN, DARK_BLUE],
        "preserves": "one squat clear-glass wholegrain-mustard jar with wide cream ribbed screw lid, blank cream oval label, ochre mustard and irregular dark seeds",
    },
)

REJECTED = (
    {
        "file": "rejected/condiment-honey-pot-glossy-cartoon-v1.png",
        "cache": "exec-45a93450-7ccf-4411-b7a6-cb079f00e46f.png",
        "reason": "Rejected before the gate for thick contour, perfect vector symmetry, specular shine and glossy cartoon/clip-art modelling.",
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
        current_path = ROOT / str(spec["current"])
        source_path = PACK / "source" / str(spec["source"])
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
            "family": "condiment",
            "label": spec["label"],
            "intent": "candidate-new-version-v2",
            "method": "composition-preserving-observational-ligne-claire-redraw",
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
        "family": "condiment",
        "semanticSet": "nine bottles, jars and table condiments",
        "styleChampions": {
            "washing-plate": "living hand-drawn shape and controlled minor imperfection",
            "sandwich-tomato": "flat-colour economy and selective readable detail",
            "repair-toolbox": "construction, detail hierarchy and confident object presence",
        },
        "preservationRule": "Each current V1 is the semantic and compositional authority: preserve container type, contents, closure, label, viewpoint, object count, relative arrangement and broad silhouette while replacing glossy cartoon rendering with observational ligne claire.",
        "recipeEvolution": "Reject polished cartoon clip-art even when cleanly outlined. Use thinner living contour, far fewer flat colour steps, no specular glass stripes, and sparse material cues. Deterministic palette normalisation removes residual generated tonal modelling.",
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
            "deployed": False,
        },
        "approval": None,
        "nextStep": "Frank reviews the exact nine-picture sheet. Register no V2 before explicit approval.",
        "rollback": "Discard this pack alone; every current V1 and all prior immutable packs remain untouched.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(SPECS)} unregistered condiment candidates in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "review-gate-awaiting-approval":
        raise RuntimeError("register identity/status mismatch")
    if register["approval"] is not None or register["checks"]["libraryVersionsAdded"]:
        raise RuntimeError("unapproved pack records approval/registration")
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
    print(f"Verified {SET}: nine candidates remain unregistered; all V1 priors retained")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
