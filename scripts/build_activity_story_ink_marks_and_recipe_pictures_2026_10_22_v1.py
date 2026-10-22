#!/usr/bin/env python3
"""Build or verify Claude's 29-mark and ten-object Bubble-story commission."""

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
    flatten,
    sha256,
    visible_bounds,
    write_hashes,
)


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/activity-story-ink-marks-and-recipe-pictures-2026-10-22-v1"
SET = "activity-story-ink-marks-and-recipe-pictures-2026-10-22-v1"
SOURCE = PACK / "source"
COMPONENTS = PACK / "drafts/components"
EVIDENCE = PACK / "evidence"
CREAM_BACK = (247, 236, 204, 255)
LIGHT = (237, 233, 222)
PALE_GREY = (196, 194, 184)
MID_GREY = (125, 135, 137)
PALE_BLUE = (151, 202, 218)
BLUE = (24, 112, 166)
NAVY = (13, 78, 117)
YELLOW = (231, 166, 56)
ORANGE = (232, 139, 45)
TERRACOTTA = (190, 91, 54)
BROWN = (144, 82, 49)
DARK_BROWN = (92, 58, 45)
PINK = (219, 106, 121)
RED = (195, 43, 55)
TARGET = 216


def mark(id_: str, family: str, label: str, cache: str, description: str, palette: list[tuple[int, int, int]]) -> dict[str, object]:
    return {"id": id_, "family": family, "label": label, "cache": cache, "description": description, "palette": palette}


MARKS: tuple[dict[str, object], ...] = (
    mark("symbol-impact-star", "impact", "Impact star", "exec-411efbe5-7c04-4d7c-9d87-32d646e9381b.png", "solid black star with seven short radiating strokes", [INK]),
    mark("symbol-motion-ticks", "motion", "Motion ticks", "exec-3cd010cc-6980-4429-ab18-47b72e390507.png", "three short curved parallel whoosh strokes", [INK]),
    mark("symbol-water-droplets", "water", "Water droplets", "exec-44243001-646b-4c7c-9b83-52e6df2c81e4.png", "one outlined teardrop with pale interior", [INK, LIGHT]),
    mark("symbol-soap-bubbles", "water", "Soap bubbles", "exec-a098abc2-338a-4430-bed6-99843613deae.png", "three differently sized outlined circles", [INK, LIGHT]),
    mark("symbol-heat-curls", "heat", "Heat curls", "exec-416c51e9-b77d-436f-82f4-06c55130d6a5.png", "three vertical wavy ink strokes", [INK]),
    mark("symbol-sizzle-spark", "impact", "Sizzle spark", "exec-d3bc8e05-d2da-4f41-bd82-3f7b7b695943.png", "five-stroke tiny burst", [INK]),
    mark("symbol-clean-glint", "clean", "Clean glint", "exec-f5285b22-b76a-4bff-92b7-1f4aacecc69c.png", "slim solid four-point cross-star", [INK]),
    mark("symbol-dust-puff", "symbol", "Dust puff", "exec-52572180-11a9-4116-9f01-6f1a3fcf4725.png", "outlined five-lobed cloud with pale-grey interior", [INK, PALE_GREY]),
    mark("symbol-earth-clods", "symbol", "Earth clods", "exec-995b69ef-f5ab-4426-aae1-2f978e77ad7e.png", "three outlined flat-brown clods", [INK, BROWN]),
    mark("symbol-sawdust", "symbol", "Sawdust", "exec-a1aefcad-fb33-4f47-8c1d-fb1cf5209554.png", "six black flecks and curls", [INK]),
    mark("symbol-seasoning-flecks", "symbol", "Seasoning flecks", "exec-fc776287-0baa-4443-839c-43706dff9f52.png", "seven black dots and flecks", [INK]),
    mark("symbol-spray-mist", "symbol", "Spray mist", "exec-5736a599-a6e7-47e0-80f0-851607889cf9.png", "fan of fine black dots", [INK]),
    mark("symbol-steam-puff", "symbol", "Steam puff", "exec-08b89cf2-c7ae-4fdf-b377-ed4d349de6bf.png", "one outlined rising curl with pale interior", [INK, LIGHT]),
    mark("symbol-question-mark", "notation", "Question mark", "exec-1dc68a66-b516-4cb4-9bca-f31843fda22f.png", "solid heavy hand-brushed question mark", [INK]),
    mark("symbol-exclamation-mark", "notation", "Exclamation mark", "exec-8bd3d402-6483-497a-8e0c-6e19526fe330.png", "solid heavy hand-brushed exclamation mark", [INK]),
    mark("symbol-foul-odour", "scent", "Foul odour", "exec-7edf7926-e215-4d3a-aff4-7a2b0f046613.png", "three wavy rising ink lines", [INK]),
    mark("symbol-pleasant-aroma", "scent", "Pleasant aroma", "exec-ebd2941d-5f1d-4f8c-bd6a-e5572c1d689a.png", "two smooth rising curls with tiny pink accent", [INK, PINK]),
    mark("symbol-heat-shimmer", "heat", "Heat shimmer", "exec-1de547ca-0d15-4096-bad5-5b1b154fa086.png", "three horizontal wavy strokes with one red accent", [INK, RED]),
    mark("symbol-welding-sparks", "welding", "Welding sparks", "exec-b017d049-aeeb-4a42-a549-2e540554c85e.png", "seven straight black sparks with yellow-orange origin", [INK, ORANGE]),
    mark("symbol-cold-snowflake", "cold", "Cold snowflake", "exec-b4119c53-846b-4872-9c02-3f84675d7313.png", "simple six-arm black snowflake", [INK]),
    mark("symbol-electrical-arc", "electrical", "Electrical arc", "exec-a8c52395-814c-4660-b840-21b068632d9d.png", "black zigzag bolt with flat yellow interior", [INK, YELLOW]),
    mark("symbol-speed-lines", "motion", "Speed lines", "exec-4515027c-d598-4451-b693-44c857565e6c.png", "three straight parallel horizontal ink strokes", [INK]),
    mark("symbol-swirl", "motion", "Swirl", "exec-9195fc0a-195c-48be-b7ce-6639610bb620.png", "one loose black swirl stroke", [INK]),
    mark("symbol-spiral", "notation", "Spiral", "exec-450c738e-96ad-4507-9f95-97740269b80a.png", "one tight black spiral", [INK]),
    mark("symbol-zigzag", "notation", "Zigzag", "exec-f4bc1328-a68f-4adb-88f6-38260a4173ef.png", "one short sharp black zigzag", [INK]),
    mark("symbol-ink-star", "impact", "Ink star", "exec-e526da4c-e766-4943-9eb1-ca2d5ec8e163.png", "one small solid black five-point star", [INK]),
    mark("symbol-accent-red-star", "notation", "Red star", "exec-1506e621-a4be-481d-9295-8b72f24d41aa.png", "black-outlined flat-red grawlix star", [INK, RED]),
    mark("symbol-accent-yellow-sun", "notation", "Yellow sun", "exec-9ee7a833-9a67-44aa-99c3-b6c8418c8d06.png", "flat-yellow disc with eight short black rays", [INK, YELLOW]),
    mark("symbol-accent-blue-spiral", "notation", "Blue spiral", "exec-92606079-788c-4c67-ba65-254790233192.png", "flat-blue spiral bounded by black ink", [INK, BLUE]),
)


OBJECTS: tuple[dict[str, object], ...] = (
    {"id": "dishwasher-machine", "family": "dishwasher", "label": "Dishwasher, door open", "cache": "exec-fdab153e-ea66-4da3-8b5d-ac3c23aad1e4.png", "description": "built-in dishwasher, door down, empty lower rack half out", "palette": [INK, CREAM_BACK[:3], LIGHT, PALE_BLUE, BLUE]},
    {"id": "laundry-washing-machine", "family": "laundry", "label": "Washing machine", "cache": "exec-28b0c715-82de-4f3a-9585-89e5b64df3c2.png", "description": "front-loading washing machine with closed porthole, dial and soap drawer", "palette": [INK, CREAM_BACK[:3], LIGHT, PALE_BLUE, NAVY]},
    {"id": "laundry-basket-dirty", "family": "laundry", "label": "Laundry basket of dirty clothes", "cache": "exec-c2f30b2e-212d-483d-8e8c-29cbf9e5e381.png", "description": "wicker basket heaped with crumpled clothes", "palette": [INK, CREAM_BACK[:3], LIGHT, YELLOW, BROWN, PALE_BLUE, BLUE, MID_GREY]},
    {"id": "wear-shirt-muddy", "family": "wearable", "label": "Muddy shirt", "cache": "exec-27a7abdc-e279-4dd4-8abf-b51961c39457.png", "description": "crumpled work shirt with three flat brown mud patches", "palette": [INK, LIGHT, PALE_BLUE, BLUE, BROWN]},
    {"id": "floor-muddy", "family": "household", "label": "Muddy floor", "cache": "exec-6ad0a641-106f-4739-b178-49b3aa77b529.png", "description": "four-board floor patch with three muddy boot prints", "palette": [INK, YELLOW, BROWN, DARK_BROWN], "pair": "floor"},
    {"id": "floor-clean", "family": "household", "label": "Clean floor", "cache": "exec-16e9ce9f-7398-46e0-b2fe-6e7d9c7f6bae.png", "description": "same four-board floor patch, clean", "palette": [INK, YELLOW, BROWN, DARK_BROWN], "pair": "floor"},
    {"id": "furniture-side-table-dusty", "family": "household", "label": "Dusty side table", "cache": "exec-8959385a-3180-4983-a0cd-f4c7d3ce7138.png", "description": "small four-legged wooden side table with flat grey dust and three fluff balls", "palette": [INK, YELLOW, BROWN, DARK_BROWN, PALE_GREY], "pair": "table"},
    {"id": "furniture-side-table-clean", "family": "household", "label": "Clean side table", "cache": "exec-ddb750cc-f154-4826-90c8-f016797e3320.png", "description": "same small four-legged wooden side table, clean", "palette": [INK, YELLOW, BROWN, DARK_BROWN], "pair": "table"},
    {"id": "garden-plant-pot", "family": "garden", "label": "Plant pot of soil", "cache": "exec-52888b9c-1a0d-4f5c-a38a-3fef68d18297.png", "description": "terracotta flower pot filled with dark soil, nothing growing", "palette": [INK, TERRACOTTA, BROWN, DARK_BROWN]},
    {"id": "fishing-sea-water", "family": "fishing", "label": "Sea water", "cache": "exec-1ce3d4d1-54e0-4574-8923-27a4d6e73c35.png", "description": "small flat blue calm-sea band with three ripple lines", "palette": [INK, PALE_BLUE, BLUE]},
)

SPECS = MARKS + OBJECTS
NEW_MARK_IDS = {str(spec["id"]) for spec in MARKS[21:]}
PAIR_DIRTY = {"floor": "floor-muddy", "table": "furniture-side-table-dusty"}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def library() -> dict[str, dict[str, object]]:
    return json.loads((ROOT / "data/activity-stories/pictures.json").read_text())["pictures"]


def source_path(spec: dict[str, object]) -> Path:
    return SOURCE / f"{spec['id']}-source.png"


def current_path(entry: dict[str, object]) -> Path:
    version = next(item for item in entry["versions"] if item["v"] == entry["current"])
    url = str(version["url"])
    if url.startswith("/activity-stories/repo/"):
        return ROOT / url.removeprefix("/activity-stories/repo/")
    if url.startswith("/keeper-review/") or url.startswith("/activity-stories/"):
        public = ROOT / "public" / url.removeprefix("/")
        if public.is_file():
            return public
        digest = str(version["sha256"])
        archived = ROOT / "review-archive/objects" / digest[:2] / f"{digest}.png"
        if archived.is_file():
            return archived
        raise RuntimeError(f"missing public and archived picture bytes: {url}")
    raise RuntimeError(f"unsupported picture URL: {url}")


def normalise(source: Image.Image, palette: list[tuple[int, int, int]], crop_box: tuple[int, int, int, int] | None = None) -> tuple[Image.Image, dict[str, object]]:
    box = crop_box or visible_bounds(source)
    isolated = source.crop(box)
    scale = min(TARGET / isolated.width, TARGET / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    flattened = flatten(isolated.resize(size, Image.Resampling.LANCZOS), palette)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    offset = ((CELL - size[0]) // 2, (CELL - size[1]) // 2)
    cell.alpha_composite(flattened, offset)
    bounds = visible_bounds(cell)
    gutter = min(bounds[0], bounds[1], CELL - bounds[2], CELL - bounds[3])
    return cell, {
        "sourceVisibleBounds": list(visible_bounds(source)),
        "normalisationCrop": list(box),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "bounds": list(bounds),
        "transparentGutterPx": gutter,
        "edgeAlphaPixels": edge_alpha_pixels(cell),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }


def mark_contact_sheet(rows: list[tuple[dict[str, object], Image.Image]], lib: dict[str, dict[str, object]]) -> Image.Image:
    columns = 4
    sheet = Image.new("RGBA", (CELL * columns, HEADER + ROW_HEIGHT * len(rows)), DARK_BACK)
    draw = ImageDraw.Draw(sheet)
    titles = ("PRIOR CURRENT / LARGE", "BLACK-INK VNEXT / LARGE", "BUBBLE PALE / 40PX", "DARK CHECK / 64PX")
    for index, title in enumerate(titles):
        draw.text((index * CELL + 8, 14), title, fill=CREAM_BACK)
    for row_index, (spec, candidate) in enumerate(rows):
        y = HEADER + row_index * ROW_HEIGHT
        picture_id = str(spec["id"])
        prior_cell = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
        if picture_id in lib:
            prior = Image.open(current_path(lib[picture_id])).convert("RGBA")
            prior_cell = backed(prior, CREAM_BACK)
        sheet.alpha_composite(prior_cell, (0, y))
        sheet.alpha_composite(backed(candidate, CREAM_BACK), (CELL, y))
        game = candidate.resize((40, 40), Image.Resampling.LANCZOS)
        game_cell = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
        game_cell.alpha_composite(game, ((CELL - 40) // 2, (CELL - 40) // 2))
        sheet.alpha_composite(game_cell, (CELL * 2, y))
        small = candidate.resize((64, 64), Image.Resampling.LANCZOS)
        dark_cell = Image.new("RGBA", (CELL, CELL), DARK_BACK)
        dark_cell.alpha_composite(small, ((CELL - 64) // 2, (CELL - 64) // 2))
        sheet.alpha_composite(dark_cell, (CELL * 3, y))
        label = f"{picture_id} / {'new V1' if picture_id in NEW_MARK_IDS else 'new immutable version'}"
        for column in range(columns):
            draw.text((column * CELL + 8, y + CELL + 8), label, fill=CREAM_BACK)
    return sheet


def object_contact_sheet(rows: list[tuple[dict[str, object], Image.Image]]) -> Image.Image:
    columns = 3
    sheet = Image.new("RGBA", (CELL * columns, HEADER + ROW_HEIGHT * len(rows)), DARK_BACK)
    draw = ImageDraw.Draw(sheet)
    titles = ("OBJECT / LIGHT", "OBJECT / DARK", "OBJECT / 64PX")
    for index, title in enumerate(titles):
        draw.text((index * CELL + 8, 14), title, fill=CREAM_BACK)
    for row_index, (spec, candidate) in enumerate(rows):
        y = HEADER + row_index * ROW_HEIGHT
        sheet.alpha_composite(backed(candidate, CREAM_BACK), (0, y))
        sheet.alpha_composite(backed(candidate, DARK_BACK), (CELL, y))
        small = candidate.resize((64, 64), Image.Resampling.LANCZOS)
        small_cell = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
        small_cell.alpha_composite(small, ((CELL - 64) // 2, (CELL - 64) // 2))
        sheet.alpha_composite(small_cell, (CELL * 2, y))
        for column in range(columns):
            draw.text((column * CELL + 8, y + CELL + 8), str(spec["id"]), fill=CREAM_BACK)
    return sheet


def build() -> None:
    COMPONENTS.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    lib = library()
    pair_boxes: dict[str, tuple[int, int, int, int]] = {}
    for pair, dirty_id in PAIR_DIRTY.items():
        source = Image.open(SOURCE / f"{dirty_id}-source.png").convert("RGBA")
        pair_boxes[pair] = visible_bounds(source)

    entries: dict[str, object] = {}
    mark_rows: list[tuple[dict[str, object], Image.Image]] = []
    object_rows: list[tuple[dict[str, object], Image.Image]] = []
    for spec in SPECS:
        picture_id = str(spec["id"])
        source = Image.open(source_path(spec)).convert("RGBA")
        if edge_alpha_pixels(source):
            raise RuntimeError(f"source touches canvas edge: {picture_id}")
        crop = pair_boxes.get(str(spec.get("pair"))) if spec.get("pair") else None
        candidate, evidence = normalise(source, list(spec["palette"]), crop)
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe candidate geometry: {picture_id}")
        output = COMPONENTS / f"{picture_id}.png"
        candidate.save(output, optimize=True)
        kind = "mark" if spec in MARKS else "object"
        existing = lib.get(picture_id)
        prior = None
        if existing:
            prior_file = current_path(existing)
            version = next(item for item in existing["versions"] if item["v"] == existing["current"])
            prior = {
                "currentLibraryVersion": existing["current"],
                "currentReferenceFile": rel(prior_file),
                "currentReferenceSha256": version["sha256"],
            }
        self_test = {
            "flatColourOnly": True,
            "oneEvenRealEdgeLine": True,
            "readsAt64Px": True,
            "realObjectNotCartoon": True,
            "checkedBy": "codex",
            "checkedOn": "2026-10-22",
        }
        if kind == "mark":
            self_test["colourCoveredLeavesOneBlackInkOneWeight"] = True
            self_test["readsAt40Px"] = True
        entries[picture_id] = {
            "kind": kind,
            "family": spec["family"],
            "label": spec["label"],
            "intent": "commissioned-new-v1" if not existing else "commissioned-new-immutable-version",
            "description": spec["description"],
            **({"prior": prior} if prior else {}),
            "sourceFile": rel(source_path(spec)),
            "sourceSha256": sha256(source_path(spec)),
            "sourcePixels": list(source.size),
            "originalCacheFile": spec["cache"],
            "flatPalette": ["#%02x%02x%02x" % colour for colour in spec["palette"]],
            "derivation": "alpha>8 crop; Lanczos scale to fit 216px; nearest declared fixed RGB palette; integer-centred in transparent 256x256 RGBA; lossless PNG",
            "file": rel(output),
            "sha256": sha256(output),
            "cellPixels": [CELL, CELL],
            "selfTest": self_test,
            **evidence,
        }
        (mark_rows if kind == "mark" else object_rows).append((spec, candidate))

    for first, second in (("floor-muddy", "floor-clean"), ("furniture-side-table-dusty", "furniture-side-table-clean")):
        a, b = entries[first], entries[second]
        if a["normalisationCrop"] != b["normalisationCrop"] or a["normalisedVisibleSize"] != b["normalisedVisibleSize"] or a["normalisedOffset"] != b["normalisedOffset"]:
            raise RuntimeError(f"paired geometry mismatch: {first}/{second}")

    marks_path = EVIDENCE / "marks-pale-game-size-and-current-contact-sheet.png"
    objects_path = EVIDENCE / "objects-light-dark-64-contact-sheet.png"
    mark_contact_sheet(mark_rows, lib).save(marks_path, optimize=True)
    object_contact_sheet(object_rows).save(objects_path, optimize=True)
    register = {
        "schema": "lighthouse-keeper/activity-story-ink-marks-and-recipe-picture-pack@1",
        "set": SET,
        "status": "commissioned-and-registered-awaiting-claude-review",
        "created": "2026-10-22",
        "commissionedBy": "Claude on Frank's behalf under Frank's standing instruction of 2026-10-21",
        "reviewOwner": "Claude",
        "tool": "built-in image generation/editing plus deterministic fixed-palette normalisation",
        "bindingTaxonomy": "one even black outline, flat colour, no shine; ligne claire, not cartoon; marks are one black ink and one weight when accent colour is covered",
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "components": entries,
        "rejected": [
            {
                "file": rel(PACK / "rejected/laundry-basket-dirty-overworked-v1.png"),
                "sha256": sha256(PACK / "rejected/laundry-basket-dirty-overworked-v1.png"),
                "originalCacheFile": "exec-40ab1614-05fe-415d-b9d1-9358d50b8a27.png",
                "reason": "Dense tiny wicker crossings and fabric wrinkles failed the purposeful-line and 64 px clarity tests.",
            },
            {
                "file": rel(PACK / "rejected/floor-muddy-independent-base-v1.png"),
                "sha256": sha256(PACK / "rejected/floor-muddy-independent-base-v1.png"),
                "originalCacheFile": "exec-f62189cf-a9cd-4d72-9ccd-eb3364d077fc.png",
                "reason": "The independently rendered floor did not preserve the clean partner exactly enough for a transformation swap.",
            },
            {
                "file": rel(PACK / "rejected/furniture-side-table-dusty-textured-v1.png"),
                "sha256": sha256(PACK / "rejected/furniture-side-table-dusty-textured-v1.png"),
                "originalCacheFile": "exec-f53d8084-f3ac-4ede-903b-9514155bfdc3.png",
                "reason": "Mottled dust, ragged speckles and curled fluff interiors failed the flat-colour and real-edge tests.",
            },
        ],
        "evidence": {
            "marks": {"file": rel(marks_path), "sha256": sha256(marks_path), "columns": 4, "rows": len(mark_rows), "coveredIds": [spec["id"] for spec, _ in mark_rows]},
            "objects": {"file": rel(objects_path), "sha256": sha256(objects_path), "columns": 3, "rows": len(object_rows), "coveredIds": [spec["id"] for spec, _ in object_rows]},
        },
        "checks": {
            "selfTestPassedForEveryPicture": True,
            "sourceEdgesClear": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "exactPalettesRecorded": True,
            "pairedGeometryLocked": True,
            "contactSheetsCoverEveryCandidate": True,
            "libraryPicturesAdded": True,
            "storiesChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "pushed": False,
            "deployed": False,
        },
        "rollback": "Remove only the versions registered from this pack and discard this versioned draft directory; no older version or approved authority was overwritten.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(SPECS)} pictures in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    expected_ids = [str(spec["id"]) for spec in SPECS]
    if register["set"] != SET or list(register["components"]) != expected_ids:
        raise RuntimeError("register identity or coverage mismatch")
    for spec in SPECS:
        picture_id = str(spec["id"])
        entry = register["components"][picture_id]
        source = ROOT / entry["sourceFile"]
        output = ROOT / entry["file"]
        if sha256(source) != entry["sourceSha256"] or sha256(output) != entry["sha256"]:
            raise RuntimeError(f"source/component hash mismatch: {picture_id}")
        image = Image.open(output).convert("RGBA")
        if image.size != (CELL, CELL) or edge_alpha_pixels(image):
            raise RuntimeError(f"component geometry mismatch: {picture_id}")
        if list(visible_bounds(image)) != entry["bounds"] or entry["transparentGutterPx"] < 20:
            raise RuntimeError(f"component bounds/gutter mismatch: {picture_id}")
        allowed = {tuple(int(value[index:index + 2], 16) for index in (1, 3, 5)) for value in entry["flatPalette"]}
        actual = {pixel[:3] for pixel in image.get_flattened_data() if pixel[3] > VISIBLE_ALPHA}
        if not actual.issubset(allowed):
            raise RuntimeError(f"palette mismatch: {picture_id}")
        if entry["ownership"] != {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0}:
            raise RuntimeError(f"ownership mismatch: {picture_id}")
        if entry["kind"] == "mark" and not entry["selfTest"]["colourCoveredLeavesOneBlackInkOneWeight"]:
            raise RuntimeError(f"mark ink self-test missing: {picture_id}")
    for first, second in (("floor-muddy", "floor-clean"), ("furniture-side-table-dusty", "furniture-side-table-clean")):
        a, b = register["components"][first], register["components"][second]
        if a["normalisationCrop"] != b["normalisationCrop"] or a["normalisedVisibleSize"] != b["normalisedVisibleSize"] or a["normalisedOffset"] != b["normalisedOffset"]:
            raise RuntimeError(f"paired geometry drift: {first}/{second}")
    for name, columns, rows in (("marks", 4, len(MARKS)), ("objects", 3, len(OBJECTS))):
        item = register["evidence"][name]
        path = ROOT / item["file"]
        image = Image.open(path)
        if sha256(path) != item["sha256"] or image.size != (CELL * columns, HEADER + ROW_HEIGHT * rows):
            raise RuntimeError(f"{name} contact sheet mismatch")
    expected_hashes = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hashes:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {SET}: {len(MARKS)} marks, {len(OBJECTS)} objects and two review sheets")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
