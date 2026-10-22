#!/usr/bin/env python3
"""Build or verify the immutable Bubble-story tea-and-toast review gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

from build_activity_story_ligne_claire_bbq_family_2026_10_21_v1 import (
    CELL,
    DARK_BACK,
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


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/activity-story-ligne-claire-tea-toast-2026-10-22-v1"
SET = "activity-story-ligne-claire-tea-toast-2026-10-22-v1"
CREAM_BACK = (247, 236, 204, 255)

CREAM = (246, 229, 183)
LIGHT = (237, 233, 222)
PALE_BLUE = (151, 202, 218)
NAVY = (13, 78, 117)
BLUE = (24, 112, 166)
TEAL = (42, 132, 148)
GOLD = (231, 166, 56)
ORANGE = (232, 139, 45)
BROWN = (166, 95, 42)
RED = (195, 43, 55)


SPECS: tuple[dict[str, object], ...] = (
    {
        "id": "tea-kettle",
        "family": "tea",
        "label": "Tea kettle",
        "source": "tea-kettle-source.png",
        "cache": "exec-99020388-bfe0-4580-9d0e-c9e1719881b6.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/tea-kettle.png",
        "currentSha256": "7014b90c1465cbf0b1b9559f57be78a4a36c354ba13033c9639aa048253dd7cf",
        "palette": [INK, CREAM, LIGHT, PALE_BLUE, NAVY, ORANGE],
        "preserves": "one squat cream stovetop kettle in the same right-facing three-quarter view, with navy arched handle and base, two warm-metal handle hinges, lid and knob, short right spout and one steam plume",
    },
    {
        "id": "tea-milk",
        "family": "tea",
        "label": "Tea milk",
        "source": "tea-milk-source.png",
        "cache": "exec-4d6a723a-3f83-4792-afda-9acd20215972.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/tea-milk.png",
        "currentSha256": "01eb45bb370455c770702cc7cb25334fccc3d2a6d3cc0cf376733da2f9dfeadc",
        "palette": [INK, CREAM, PALE_BLUE],
        "preserves": "exactly one tall open glass bottle filled with milk at left and one small cream pouring jug with a single loop handle at right, in the same overlap and viewpoint",
    },
    {
        "id": "tea-mug",
        "family": "tea",
        "label": "Tea mug",
        "source": "tea-mug-source.png",
        "cache": "exec-7134eeba-b66f-4aa4-967c-1f31a510903c.png",
        "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/tea-mug.png",
        "currentSha256": "af8fb40591e8165cfb4ec8f9f30be0df24abd733cc412d086c3920a37242bff3",
        "palette": [INK, CREAM, NAVY, BROWN],
        "preserves": "one squat cream enamel mug with left loop handle, navy rolled rim and handle edging, and one visible warm-brown tea surface in the same front three-quarter view",
    },
    {
        "id": "toast-butter-jam",
        "family": "toast",
        "label": "Toast butter jam",
        "source": "toast-butter-jam-source.png",
        "cache": "exec-880acf66-908e-4c1b-81ff-fc8f6cb9bbd3.png",
        "current": "art/drafts/activity-cloud-composer-2026-10-19-v5/drafts/components/toast-butter-jam.png",
        "currentSha256": "c75e23294215d751b315296776b39e53fc5690e0a8b2216c62e7dc29da77a134",
        "palette": [INK, CREAM, TEAL, GOLD, BLUE, RED, ORANGE],
        "preserves": "front-left teal-rimmed butter dish and cream cover with teal knob, exactly one large butter block and one smaller cut pat, plus one rear-right raspberry-jam jar with blue-and-cream checked cloth and one tied cord bow",
    },
    {
        "id": "toast-slices",
        "family": "toast",
        "label": "Toast slices",
        "source": "toast-slices-source.png",
        "cache": "exec-e03337f5-f03b-4584-826a-8ef96d8ddc6a.png",
        "current": "art/drafts/activity-cloud-composer-2026-10-19-v5/drafts/components/toast-slices.png",
        "currentSha256": "4a1344273465976f1c69b858e1ada925a69432242450c2838c68d9fe63e25a27",
        "palette": [INK, GOLD, ORANGE],
        "preserves": "exactly two overlapping diagonal toast slices, rear upper-left and front lower-right, plus exactly five detached cereal-grain marks below in a group of three and a group of two",
    },
    {
        "id": "toast-toaster",
        "family": "toast",
        "label": "Toast toaster",
        "source": "toast-toaster-source.png",
        "cache": "exec-c86f6db9-4a83-4af9-b307-079d5d036df4.png",
        "current": "art/drafts/activity-cloud-composer-2026-10-19-v5/drafts/components/toast-toaster.png",
        "currentSha256": "92845e8574dbbb507267f89a65bfcc0fe0933f389bb6dd052120a891a828ef98",
        "palette": [INK, CREAM, TEAL, GOLD],
        "preserves": "one compact vintage toaster in the same front-right three-quarter view, with exactly two top slots, teal front, cream top and right side, ochre base and feet, one right lever in its slot and one round browning control below",
    },
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def library_entries() -> dict[str, dict[str, object]]:
    return json.loads((ROOT / "data/activity-stories/pictures.json").read_text())["pictures"]


def contact_sheet(rows: list[tuple[dict[str, object], Image.Image]]) -> Image.Image:
    columns = 5
    sheet = Image.new("RGBA", (CELL * columns, HEADER + ROW_HEIGHT * len(rows)), DARK_BACK)
    draw = ImageDraw.Draw(sheet)
    titles = ("PRIOR V1", "APPROVED V2 / CREAM", "APPROVED V2 / DARK", "PRIOR / 64PX", "APPROVED / 64PX")
    for index, title in enumerate(titles):
        draw.text((index * CELL + 8, 14), title, fill=CREAM_BACK)
    for row_index, (spec, candidate) in enumerate(rows):
        y = HEADER + row_index * ROW_HEIGHT
        current = Image.open(ROOT / str(spec["current"])).convert("RGBA")
        sheet.alpha_composite(backed(current, CREAM_BACK), (0, y))
        sheet.alpha_composite(backed(candidate, CREAM_BACK), (CELL, y))
        sheet.alpha_composite(backed(candidate, DARK_BACK), (CELL * 2, y))
        for column, picture in ((3, current), (4, candidate)):
            small = picture.resize((64, 64), Image.Resampling.LANCZOS)
            cell = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
            cell.alpha_composite(small, (96, 96))
            sheet.alpha_composite(cell, (CELL * column, y))
        label = f"{spec['id']} / V1 retained / approved V2"
        for column in range(columns):
            draw.text((column * CELL + 8, y + CELL + 8), label, fill=CREAM_BACK)
    return sheet


def build() -> None:
    component_dir = PACK / "drafts/components"
    evidence_dir = PACK / "evidence"
    component_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    library = library_entries()
    entries: dict[str, object] = {}
    rows: list[tuple[dict[str, object], Image.Image]] = []

    for spec in SPECS:
        picture_id = str(spec["id"])
        current_path = ROOT / str(spec["current"])
        source_path = PACK / "source" / str(spec["source"])
        if sha256(current_path) != spec["currentSha256"]:
            raise RuntimeError(f"current source drift: {picture_id}")
        picture = library[picture_id]
        if len(picture["versions"]) < 2:
            raise RuntimeError(f"approved pack requires registered V2 library entry: {picture_id}")
        if picture["versions"][0]["sha256"] != spec["currentSha256"]:
            raise RuntimeError(f"library V1 hash drift: {picture_id}")
        source = Image.open(source_path)
        if source.mode != "RGBA" or edge_alpha_pixels(source):
            raise RuntimeError(f"unsafe source: {picture_id}")
        palette = list(spec["palette"])
        component, evidence = normalise(source, palette)
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe candidate: {picture_id}")
        output_path = component_dir / f"{picture_id}.png"
        component.save(output_path, optimize=True)
        entries[picture_id] = {
            "family": spec["family"],
            "label": spec["label"],
            "intent": "frank-approved-library-version-v2",
            "priorCurrentLibraryVersion": 1,
            "proposedLibraryVersion": 2,
            "preserves": spec["preserves"],
            "currentReferenceFile": rel(current_path),
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

    contact_path = evidence_dir / "current-vs-proposed-v2-contact-sheet.png"
    contact_sheet(rows).save(contact_path, optimize=True)
    rejected_path = PACK / "rejected/tea-kettle-gradient-inflated-v1.png"
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-family-pack@1",
        "set": SET,
        "status": "approved-and-registered",
        "created": "2026-10-22",
        "tool": "built-in image editing plus deterministic reduced-palette normalisation",
        "families": ["tea", "toast"],
        "semanticSet": "six legacy tea-and-toast objects; the already-line-clear commissioned tea-bag V1 remains untouched",
        "visualAuthority": [
            "art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/drafts/components/sandwich-tomato.png",
            "art/drafts/activity-story-ligne-claire-washing-2026-10-21-v1/drafts/components/washing-plate.png",
            "art/drafts/activity-story-ligne-claire-general-repair-2026-10-21-v1/drafts/components/repair-toolbox.png",
            "art/drafts/activity-story-ligne-claire-condiments-flat-glass-correction-2026-10-21-v1/drafts/components/condiment-raspberry-jam.png",
        ],
        "bindingTaxonomy": "one even black outline; a line only for a real edge; every closed area one flat colour; no gradient, shine or glow; accurate adult object construction; clear at 64px; black only for outlines and true black/dark openings; marks use the same line",
        "components": entries,
        "rejected": [
            {
                "file": rel(rejected_path),
                "sha256": sha256(rejected_path),
                "originalCacheFile": "exec-11f19f9e-b6b1-4e05-a270-b0f9c8ce13c9.png",
                "reason": "Rejected before the gate: gradient fills, a white specular spout stripe and inflated toy-like kettle proportions violated the binding taxonomy.",
            }
        ],
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
            "flatColourOnly": True,
            "contactSheetCoversEveryCandidate": True,
            "libraryVersionsAdded": True,
            "storiesChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": {
            "by": "Frank",
            "date": "2026-10-22",
            "words": "These are superb, I think the best yet, and they follow the direction very well.",
            "scope": "the exact six-picture tea-and-toast contact sheet",
        },
        "nextStep": "Keep these exact six immutable files as their approved V2s; any later correction must be a new version.",
        "rollback": "Set each picture selector back to its byte-identical retained V1. Never overwrite either version.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(SPECS)} approved V2s in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "approved-and-registered":
        raise RuntimeError("register identity/status mismatch")
    if not register["checks"]["libraryVersionsAdded"]:
        raise RuntimeError("approved review gate does not record registered library versions")
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
            raise RuntimeError(f"source/candidate hash mismatch: {picture_id}")
        if sha256(current_path) != entry["currentReferenceSha256"]:
            raise RuntimeError(f"current reference drift: {picture_id}")
        picture = library[picture_id]
        if len(picture["versions"]) < 2:
            raise RuntimeError(f"approved candidate is not registered as V2: {picture_id}")
        if picture["versions"][0]["sha256"] != entry["currentReferenceSha256"]:
            raise RuntimeError(f"library V1 drift: {picture_id}")
        if picture["versions"][1]["sha256"] != entry["sha256"]:
            raise RuntimeError(f"library V2 drift: {picture_id}")
        output = Image.open(output_path)
        if output.mode != "RGBA" or output.size != (CELL, CELL) or edge_alpha_pixels(output):
            raise RuntimeError(f"candidate geometry/edge mismatch: {picture_id}")
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
    print(f"Verified {SET}: six approved flat-colour V2s, pinned priors and immutable review evidence")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
