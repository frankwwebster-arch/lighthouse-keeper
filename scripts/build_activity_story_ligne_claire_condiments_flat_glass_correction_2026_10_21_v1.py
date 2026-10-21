#!/usr/bin/env python3
"""Build or verify the approved flatter-glass condiment correction pack."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from build_activity_story_ligne_claire_bbq_family_2026_10_21_v1 import (
    CELL,
    HEADER,
    INK,
    ROW_HEIGHT,
    VISIBLE_ALPHA,
    backed,
    edge_alpha_pixels,
    normalise,
    sha256,
    visible_bounds,
    write_hashes,
)
from build_activity_story_ligne_claire_condiments_2026_10_21_v1 import SPECS as PRIOR_SPECS


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/activity-story-ligne-claire-condiments-flat-glass-correction-2026-10-21-v1"
SET = "activity-story-ligne-claire-condiments-flat-glass-correction-2026-10-21-v1"
PRIOR_PACK = ROOT / "art/drafts/activity-story-ligne-claire-condiments-2026-10-21-v1"

CREAM_BACK = (247, 236, 204, 255)
DARK_BACK = (5, 28, 40, 255)
CREAM = (246, 229, 183)
LIGHT = (237, 233, 222)
PALE_BLUE = (151, 202, 218)
BLUE = (24, 112, 166)
DARK_BLUE = (13, 78, 117)
GOLD = (231, 166, 56)
ORANGE = (232, 139, 45)
BROWN = (166, 95, 42)
RED = (232, 72, 51)
DARK_RED = (195, 43, 55)
GREEN = (73, 145, 55)
DARK_GREEN = (37, 104, 48)
OLIVE = (147, 150, 38)

CORRECTIONS: dict[str, dict[str, object]] = {
    "condiment-honey-pot": {
        "source": "condiment-honey-pot-source.png",
        "cache": "exec-92265b00-2e3f-4103-b804-12aafed88873.png",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, ORANGE, BROWN],
    },
    "condiment-malt-vinegar": {
        "source": "condiment-malt-vinegar-source.png",
        "cache": "exec-0179633e-f796-4f49-ad38-acb3fca05222.png",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, BROWN],
    },
    "condiment-mayonnaise-jar": {
        "source": "condiment-mayonnaise-jar-source.png",
        "cache": "exec-06ebdda0-e310-4a9a-9cf7-0d2f2a395fd1.png",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, BLUE, DARK_BLUE],
    },
    "condiment-olive-oil": {
        "source": "condiment-olive-oil-source.png",
        "cache": "exec-5eafd122-c7e4-44cd-82c2-13a6221f259b.png",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, OLIVE, BROWN],
    },
    "condiment-pickle-jar": {
        "source": "condiment-pickle-jar-source.png",
        "cache": "exec-5f5214f5-0398-4efd-81a6-5971a9b57b53.png",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, GREEN, DARK_GREEN, BROWN],
    },
    "condiment-raspberry-jam": {
        "source": "condiment-raspberry-jam-source.png",
        "cache": "exec-674d9031-df27-4254-bd84-5cac09e07a28.png",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, BLUE, DARK_BLUE, RED, DARK_RED, GOLD],
    },
    "condiment-wholegrain-mustard-jar": {
        "source": "condiment-wholegrain-mustard-jar-source.png",
        "cache": "exec-9e7edabf-34fc-4885-a094-2abba5bc706b.png",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, GOLD, ORANGE, BROWN, DARK_BLUE],
    },
}

CARRY_FORWARD = {"condiment-ketchup-bottle", "condiment-mustard-bottle"}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def library_entries() -> dict[str, dict[str, object]]:
    return json.loads((ROOT / "data/activity-stories/pictures.json").read_text())["pictures"]


def prior_register() -> dict[str, object]:
    return json.loads((PRIOR_PACK / "batch-register.json").read_text())


def correction_contact_sheet(rows: list[tuple[dict[str, object], Image.Image, Image.Image]]) -> Image.Image:
    columns = 6
    sheet = Image.new("RGBA", (CELL * columns, HEADER + ROW_HEIGHT * len(rows)), DARK_BACK)
    draw = ImageDraw.Draw(sheet)
    titles = (
        "CURRENT V1",
        "SUPERSEDED CANDIDATE",
        "FLAT-GLASS CORRECTION / CREAM",
        "FLAT-GLASS CORRECTION / DARK",
        "SUPERSEDED / 64PX",
        "CORRECTION / 64PX",
    )
    for index, title in enumerate(titles):
        draw.text((index * CELL + 8, 14), title, fill=CREAM_BACK)
    for row_index, (spec, previous, candidate) in enumerate(rows):
        y = HEADER + row_index * ROW_HEIGHT
        current = Image.open(ROOT / str(spec["current"])).convert("RGBA")
        sheet.alpha_composite(backed(current, CREAM_BACK), (0, y))
        sheet.alpha_composite(backed(previous, CREAM_BACK), (CELL, y))
        sheet.alpha_composite(backed(candidate, CREAM_BACK), (CELL * 2, y))
        sheet.alpha_composite(backed(candidate, DARK_BACK), (CELL * 3, y))
        for column, picture in ((4, previous), (5, candidate)):
            small = picture.resize((64, 64), Image.Resampling.LANCZOS)
            cell = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
            cell.alpha_composite(small, (96, 96))
            sheet.alpha_composite(cell, (CELL * column, y))
        label = f"{spec['id']} / V1 retained / proposed V2 correction"
        for column in range(columns):
            draw.text((column * CELL + 8, y + CELL + 8), label, fill=CREAM_BACK)
    return sheet


def build() -> None:
    component_dir = PACK / "drafts/components"
    evidence_dir = PACK / "evidence"
    component_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    prior = prior_register()
    entries: dict[str, object] = {}
    rows: list[tuple[dict[str, object], Image.Image, Image.Image]] = []

    for spec in PRIOR_SPECS:
        picture_id = str(spec["id"])
        current_path = ROOT / str(spec["current"])
        previous_path = PRIOR_PACK / "drafts/components" / f"{picture_id}.png"
        output_path = component_dir / f"{picture_id}.png"
        if sha256(current_path) != spec["currentSha256"]:
            raise RuntimeError(f"current source drift: {picture_id}")
        if sha256(previous_path) != prior["components"][picture_id]["sha256"]:
            raise RuntimeError(f"previous candidate drift: {picture_id}")

        if picture_id in CARRY_FORWARD:
            shutil.copyfile(previous_path, output_path)
            component = Image.open(output_path).convert("RGBA")
            bounds = visible_bounds(component)
            gutter = min(bounds[0], bounds[1], CELL - bounds[2], CELL - bounds[3])
            evidence = {
                "sourceVisibleBounds": list(bounds),
                "normalisedVisibleSize": [bounds[2] - bounds[0], bounds[3] - bounds[1]],
                "normalisedOffset": [bounds[0], bounds[1]],
                "bounds": list(bounds),
                "transparentGutterPx": gutter,
                "edgeAlphaPixels": edge_alpha_pixels(component),
                "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
            }
            source_path = previous_path
            palette_hex = prior["components"][picture_id]["flatPalette"]
            cache = prior["components"][picture_id]["originalCacheFile"]
            method = "exact-byte-carry-forward-from-first-condiment-gate"
            derivation = "byte-identical carry-forward; squeeze bottle was not part of Frank's glass-flatness correction"
        else:
            correction = CORRECTIONS[picture_id]
            source_path = PACK / "source" / str(correction["source"])
            source = Image.open(source_path)
            if source.mode != "RGBA" or edge_alpha_pixels(source):
                raise RuntimeError(f"unsafe correction source: {picture_id}")
            palette = list(correction["palette"])
            component, evidence = normalise(source, palette)
            component.save(output_path, optimize=True)
            palette_hex = ["#%02x%02x%02x" % colour for colour in palette]
            cache = correction["cache"]
            method = "user-directed-flat-glass-correction"
            derivation = "alpha>8 crop; Lanczos scale to fit 216px; nearest reduced fixed RGB palette; integer-centred in transparent 256x256 RGBA; lossless PNG"

        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe output: {picture_id}")
        entries[picture_id] = {
            "family": "condiment",
            "label": spec["label"],
            "intent": "approved-current-version-v2",
            "method": method,
            "priorCurrentLibraryVersion": 1,
            "proposedLibraryVersion": 2,
            "preserves": spec["preserves"],
            "currentReferenceFile": spec["current"],
            "currentReferenceSha256": spec["currentSha256"],
            "supersededCandidateFile": rel(previous_path),
            "supersededCandidateSha256": sha256(previous_path),
            "sourceFile": rel(source_path),
            "sourceSha256": sha256(source_path),
            "sourcePixels": list(Image.open(source_path).size),
            "originalCacheFile": cache,
            "flatPalette": palette_hex,
            "derivation": derivation,
            "file": rel(output_path),
            "sha256": sha256(output_path),
            "cellPixels": [CELL, CELL],
            **evidence,
        }
        rows.append((spec, Image.open(previous_path).convert("RGBA"), Image.open(output_path).convert("RGBA")))

    contact_path = evidence_dir / "superseded-vs-flat-glass-contact-sheet.png"
    correction_contact_sheet(rows).save(contact_path, optimize=True)
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-family-pack@1",
        "set": SET,
        "status": "approved-and-registered",
        "created": "2026-10-21",
        "tool": "built-in image editing plus deterministic reduced-palette normalisation",
        "family": "condiment",
        "semanticSet": "seven flatter glass-container corrections plus two exact squeeze-bottle carry-forwards",
        "supersedesReviewPack": rel(PRIOR_PACK),
        "userCorrection": "The glass jars are too shiny, not flat enough.",
        "flatGlassRule": "Glass is visually quiet: outer contour plus at most two or three short pale-blue construction ticks. Contents carry the flat colour. No white reflection bands, vertical shine stripes, reflected colour wedges, bevels, gradients or luminous rims.",
        "components": entries,
        "evidence": {
            "file": rel(contact_path),
            "sha256": sha256(contact_path),
            "columns": 6,
            "rows": len(rows),
            "coveredIds": [spec["id"] for spec in PRIOR_SPECS],
        },
        "checks": {
            "priorReviewPackImmutable": True,
            "sevenGlassContainersCorrected": True,
            "twoSqueezeBottlesByteIdentical": True,
            "sourceEdgesClear": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "currentReferenceHashesPinned": True,
            "supersededCandidateHashesPinned": True,
            "exactPalettesRecorded": True,
            "contactSheetCoversEveryCandidate": True,
            "libraryVersionsAdded": True,
            "storyChanged": False,
            "activityStoriesRuntimeChanged": False,
            "deployed": False,
        },
        "approval": {
            "by": "Frank",
            "date": "2026-10-21",
            "words": "yes much better. Taxonomy must be: one even black outline, flat colour, no shine.",
            "scope": "the exact nine-picture flat-glass condiment correction sheet",
        },
        "nextStep": "Continue the next family in a fresh immutable review pack using the binding one-even-black-outline / flat-colour / no-shine taxonomy.",
        "rollback": "Every V1 remains immutable and selectable; each approved V2 is an immutable added library version and both earlier condiment gates remain preserved.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(PRIOR_SPECS)} approved flat-glass condiment V2s in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "approved-and-registered":
        raise RuntimeError("register identity/status mismatch")
    if register["approval"]["words"] != "yes much better. Taxonomy must be: one even black outline, flat colour, no shine.":
        raise RuntimeError("approval wording mismatch")
    if not register["checks"]["libraryVersionsAdded"]:
        raise RuntimeError("approved correction does not record registered versions")
    expected_ids = [str(spec["id"]) for spec in PRIOR_SPECS]
    if list(register["components"]) != expected_ids:
        raise RuntimeError("register component order/coverage mismatch")
    library = library_entries()
    for spec in PRIOR_SPECS:
        picture_id = str(spec["id"])
        entry = register["components"][picture_id]
        source_path = ROOT / entry["sourceFile"]
        output_path = ROOT / entry["file"]
        current_path = ROOT / entry["currentReferenceFile"]
        previous_path = ROOT / entry["supersededCandidateFile"]
        for path in (source_path, output_path, current_path, previous_path):
            if not path.is_file():
                raise RuntimeError(f"missing manifest path: {path}")
        if sha256(source_path) != entry["sourceSha256"] or sha256(output_path) != entry["sha256"]:
            raise RuntimeError(f"source/component hash mismatch: {picture_id}")
        if sha256(current_path) != entry["currentReferenceSha256"] or sha256(previous_path) != entry["supersededCandidateSha256"]:
            raise RuntimeError(f"prior hash drift: {picture_id}")
        picture = library[picture_id]
        if picture["current"] != 2 or len(picture["versions"]) != 2:
            raise RuntimeError(f"approved V2 is not current: {picture_id}")
        if picture["versions"][0]["sha256"] != entry["currentReferenceSha256"]:
            raise RuntimeError(f"library V1 hash drift: {picture_id}")
        if picture["versions"][1]["sha256"] != entry["sha256"]:
            raise RuntimeError(f"library V2 hash mismatch: {picture_id}")
        output = Image.open(output_path)
        if output.mode != "RGBA" or output.size != (CELL, CELL) or edge_alpha_pixels(output):
            raise RuntimeError(f"output geometry/edge mismatch: {picture_id}")
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
        if picture_id in CARRY_FORWARD and sha256(output_path) != sha256(previous_path):
            raise RuntimeError(f"carry-forward changed bytes: {picture_id}")
    evidence = register["evidence"]
    contact_path = ROOT / evidence["file"]
    if not contact_path.is_file() or sha256(contact_path) != evidence["sha256"]:
        raise RuntimeError("contact sheet hash mismatch")
    contact = Image.open(contact_path)
    if contact.mode != "RGBA" or contact.size != (CELL * 6, HEADER + ROW_HEIGHT * len(PRIOR_SPECS)):
        raise RuntimeError("contact sheet geometry mismatch")
    if evidence["coveredIds"] != expected_ids or evidence["rows"] != len(PRIOR_SPECS) or evidence["columns"] != 6:
        raise RuntimeError("contact sheet coverage mismatch")
    expected_hashes = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hashes:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {SET}: seven flatter glass corrections and two exact carry-forwards are current V2s")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
