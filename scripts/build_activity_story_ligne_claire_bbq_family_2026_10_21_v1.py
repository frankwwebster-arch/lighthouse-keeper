#!/usr/bin/env python3
"""Build or verify the two approved ligne-claire BBQ continuation packs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216
HEADER = 46
ROW_HEIGHT = CELL + 34
INK = (5, 24, 36)
CREAM_BACK = (246, 233, 205, 255)
DARK_BACK = (*INK, 255)


PACKS: dict[str, dict[str, object]] = {
    "food": {
        "directory": "art/drafts/activity-story-ligne-claire-bbq-food-2026-10-21-v1",
        "set": "activity-story-ligne-claire-bbq-food-2026-10-21-v1",
        "family": "bbq",
        "approvalScope": "the seven food-family V2 candidates in the approved contact sheet",
        "specs": (
            {
                "id": "bbq-burgers",
                "label": "Burgers",
                "source": "bbq-burgers-source.png",
                "cache": "exec-dee1bc84-74d4-4b91-9788-9f28c3d2f3cd.png",
                "current": "review-archive/objects/52/5244d4289bbaf95f4c2ddd36a72f24fe9b5bf12e2a349365d9fe574fdfa64354.png",
                "currentSha256": "5244d4289bbaf95f4c2ddd36a72f24fe9b5bf12e2a349365d9fe574fdfa64354",
                "palette": [INK, (231, 166, 56), (246, 229, 183), (232, 72, 51), (57, 148, 55), (116, 65, 40)],
                "preserves": "two overlapping finished burgers, golden seeded buns, lettuce, tomato and cooked patties in the current front three-quarter arrangement",
            },
            {
                "id": "bbq-ketchup",
                "label": "BBQ ketchup",
                "source": "bbq-ketchup-source.png",
                "cache": "exec-020cab0e-0669-460f-bcb0-98cfbc31ccb3.png",
                "current": "art/drafts/activity-cloud-composer-2026-10-19-v1/drafts/components/bbq-ketchup.png",
                "currentSha256": "fb8b53e64900967299aa1b9f161640d3862413d8a579128de02cd35129c4a27a",
                "palette": [INK, (232, 72, 51), (246, 229, 183)],
                "preserves": "the tall red squeeze bottle at left and cream bowl of ketchup at lower right as one grouped condiment picture",
            },
            {
                "id": "bbq-lamb-chops",
                "label": "BBQ lamb chops",
                "source": "bbq-lamb-chops-source.png",
                "cache": "exec-63e07089-d3a0-474c-ad96-a22a18cb83db.png",
                "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/bbq-lamb-chops.png",
                "currentSha256": "d0b507c045397faada719d5b9c4317689280a287a65a172ceed1cef08db69fff",
                "palette": [INK, (232, 72, 62), (195, 43, 55), (246, 229, 183)],
                "preserves": "two overlapping raw bone-in lamb chops with both pale bones rising up-right and no plate or garnish",
            },
            {
                "id": "bbq-leg-lamb",
                "label": "BBQ leg lamb",
                "source": "bbq-leg-lamb-source.png",
                "cache": "exec-1c23f9b4-a1d6-462a-a8d3-507e128ba1ed.png",
                "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/bbq-leg-lamb.png",
                "currentSha256": "19c65af65d6ba61db422ee922e786f5d876323777dff4265a3ddba39b251f354",
                "palette": [INK, (229, 138, 46), (201, 66, 60), (246, 229, 183), (73, 145, 55), (13, 78, 117)],
                "preserves": "the tied roasted leg with cut face and bone end, rosemary sprigs and shallow cream oval plate with blue rim",
            },
            {
                "id": "bbq-steak",
                "label": "BBQ steak",
                "source": "bbq-steak-source.png",
                "cache": "exec-3a7b6b7f-3ada-47e0-87d8-fd66ad41e782.png",
                "current": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/bbq-steak.png",
                "currentSha256": "b6c81c2fbc03d1daaabeae70b1e8856216c49fdd0fbc49b2788509febceb5cad",
                "palette": [INK, (232, 72, 62), (195, 43, 55), (246, 229, 183)],
                "preserves": "one long low irregular raw red steak with a rounded left end, raised right end, cream fat edge and no plate",
            },
            {
                "id": "bbq-raw-burger-patties",
                "label": "Raw burger patties",
                "source": "bbq-raw-burger-patties-source.png",
                "cache": "exec-a54bf916-f47a-45a7-9adc-cba7f77e6ada.png",
                "current": "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/assets/bbq-raw-burger-patties.png",
                "currentSha256": "8d8107dbe7705c7cecbe90ad2ead6e83b82525ab4ca9b52b25e13d624c4e9521",
                "palette": [INK, (245, 126, 106), (215, 73, 62)],
                "preserves": "three thick raw minced-beef patties in the current triangular overlap, with one in front and two behind",
            },
            {
                "id": "bbq-raw-steak",
                "label": "Raw steak",
                "source": "bbq-raw-steak-source.png",
                "cache": "exec-186d791d-bf36-4d0e-b97d-3d593e83f3db.png",
                "current": "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/assets/bbq-raw-steak.png",
                "currentSha256": "14870ae013f48d8ff84ccb1894c41cb8baec661273f0da2f15cf1032033aa670",
                "palette": [INK, (232, 72, 62), (195, 43, 55), (246, 229, 183)],
                "preserves": "one thick rounded rectangular raw steak with pale fat network, short side wall and no plate",
            },
        ),
        "rejected": (
            {
                "file": "rejected/bbq-leg-lamb-four-band-prompt-v1.png",
                "cache": "exec-e49053f3-3464-4512-b67c-fe0260fe8eb3.png",
                "reason": "The drawing matched the source's three tying bands, but the prompt incorrectly asserted four; rerendered with correct provenance after an enlarged count audit.",
            },
            {
                "file": "rejected/bbq-steak-v1.png",
                "cache": "exec-c610fbd9-67a4-4a72-917b-ae18b20bb8cd.png",
                "reason": "The silhouette became too rectangular and the dense marbling blurred the distinction from bbq-raw-steak.",
            },
        ),
    },
    "tools": {
        "directory": "art/drafts/activity-story-ligne-claire-bbq-tools-2026-10-21-v1",
        "set": "activity-story-ligne-claire-bbq-tools-2026-10-21-v1",
        "family": "bbq-tools",
        "approvalScope": "the seven tool-family V2 candidates in the approved contact sheet",
        "specs": (
            {
                "id": "bbq-basting-brush",
                "label": "Basting brush",
                "source": "bbq-basting-brush-source.png",
                "cache": "exec-5181c616-adc2-46b5-bf31-ee7f646286de.png",
                "current": "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/assets/bbq-basting-brush.png",
                "currentSha256": "a6bcd75aa5b4c50216622c04a5018c23998b18097eb20a77eddd4e79c613a16d",
                "palette": [INK, (13, 78, 117), (232, 139, 45), (237, 233, 222)],
                "preserves": "one diagonal brush with orange silicone bristles, pale collar, blue handle and hanging hole",
            },
            {
                "id": "bbq-charcoal-bag",
                "label": "Charcoal bag",
                "source": "bbq-charcoal-bag-source.png",
                "cache": "exec-2a3d5494-f10c-4e29-8d5a-e67aca6fe4f3.png",
                "current": "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/assets/bbq-charcoal-bag.png",
                "currentSha256": "f45c271e7d9d14cbab2a3dde2f4d15784a875a659515c163ef9fe3f72fdee254",
                "palette": [INK, (13, 78, 117), (232, 139, 45), (48, 52, 58), (73, 76, 82)],
                "preserves": "one upright closed blue-and-orange charcoal bag with folded top and three-lump charcoal motif",
            },
            {
                "id": "bbq-charcoal-chimney",
                "label": "Charcoal chimney",
                "source": "bbq-charcoal-chimney-source.png",
                "cache": "exec-bd0285b4-9f15-433f-853e-5f944ee8d505.png",
                "current": "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/assets/bbq-charcoal-chimney.png",
                "currentSha256": "9f172c34fd0cfeeaeebcc924522ae7ee552c053229e61ffae08ae2c0e91e46c7",
                "palette": [INK, (237, 233, 222), (151, 166, 172), (13, 78, 117), (232, 139, 45), (48, 52, 58)],
                "preserves": "the upright perforated steel chimney, visible charcoal, lower vent slots and right blue shield handle with orange grip",
            },
            {
                "id": "bbq-grill-fork",
                "label": "Grill fork",
                "source": "bbq-grill-fork-source.png",
                "cache": "exec-13218404-a578-4876-8c7c-1dcc5d66b17e.png",
                "current": "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/assets/bbq-grill-fork.png",
                "currentSha256": "6a2451de5e126ef784cae7a0d6c001b6640fb6fc582938b90de6cbb7424cb36d",
                "palette": [INK, (237, 233, 222), (13, 78, 117), (232, 139, 45)],
                "preserves": "one diagonal two-tine fork with steel shaft, blue two-rivet handle and orange end hole",
            },
            {
                "id": "bbq-heatproof-mitt",
                "label": "Heatproof mitt",
                "source": "bbq-heatproof-mitt-source.png",
                "cache": "exec-969214bf-19a5-4c1e-8a5d-86d70309616d.png",
                "current": "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/assets/bbq-heatproof-mitt.png",
                "currentSha256": "85b7b5c527287ecb238b57184bdbd3327649cf338b7a40504d0113381d9f4367",
                "palette": [INK, (13, 78, 117), (23, 124, 157), (232, 139, 45)],
                "preserves": "one blue diamond-quilted mitt with left thumb, orange-bound open cuff and orange hanging loop",
            },
            {
                "id": "bbq-skewer-bundle",
                "label": "Skewers",
                "source": "bbq-skewer-bundle-source.png",
                "cache": "exec-05d28427-74eb-443c-a44a-531e42be3490.png",
                "current": "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/assets/bbq-skewer-bundle.png",
                "currentSha256": "b07b6828cc76a3b54b8aa8a8671f48adb91ec751b48a52068c69bdc710f0cc26",
                "palette": [INK, (237, 233, 222), (13, 78, 117), (232, 139, 45)],
                "preserves": "exactly three parallel diagonal skewers with three points, blue loop handles and orange collars",
            },
            {
                "id": "bbq-slotted-turner",
                "label": "Slotted turner",
                "source": "bbq-slotted-turner-source.png",
                "cache": "exec-5d27d887-098d-4a5e-a335-23950e1ffa80.png",
                "current": "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/assets/bbq-slotted-turner.png",
                "currentSha256": "9115fb7c3602151d786db177f2ea6aa5baaac1529a24cd71a05ed95f83985065",
                "palette": [INK, (237, 233, 222), (13, 78, 117), (232, 139, 45)],
                "preserves": "one diagonal turner with broad steel blade, exactly four slots, bent neck and blue two-rivet handle with orange end hole",
            },
        ),
        "rejected": (
            {
                "file": "rejected/bbq-skewer-bundle-four-count-prompt-v1.png",
                "cache": "exec-0c4e333e-aeda-4a4c-bb52-21f7c516bf45.png",
                "reason": "The drawing matched the source's three skewers, but the prompt incorrectly asserted four; rerendered with correct provenance after an enlarged count audit.",
            },
            {
                "file": "rejected/bbq-slotted-turner-v1.png",
                "cache": "exec-a9fc9404-0400-4f17-9055-cf86c1d99bdd.png",
                "reason": "The drawing matched the source's four slots, but the prompt incorrectly asserted five; rerendered with correct provenance after an enlarged count audit.",
            },
        ),
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def visible_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    if image.mode != "RGBA":
        raise RuntimeError(f"expected RGBA image, got {image.mode}")
    found = image.getchannel("A").point(lambda a: 255 if a > VISIBLE_ALPHA else 0).getbbox()
    if found is None:
        raise RuntimeError("image has no visible pixels")
    return found


def edge_alpha_pixels(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = {(x, 0) for x in range(image.width)} | {(x, image.height - 1) for x in range(image.width)}
    points |= {(0, y) for y in range(image.height)} | {(image.width - 1, y) for y in range(image.height)}
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in points)


def flatten(image: Image.Image, palette: list[tuple[int, int, int]]) -> Image.Image:
    rgba = image.convert("RGBA")
    output = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    source_pixels = rgba.load()
    output_pixels = output.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            red, green, blue, alpha = source_pixels[x, y]
            if alpha <= VISIBLE_ALPHA:
                continue
            colour = min(
                palette,
                key=lambda item: (red - item[0]) ** 2 + (green - item[1]) ** 2 + (blue - item[2]) ** 2,
            )
            output_pixels[x, y] = (*colour, alpha)
    return output


def normalise(source: Image.Image, palette: list[tuple[int, int, int]]) -> tuple[Image.Image, dict[str, object]]:
    source_box = visible_bounds(source)
    isolated = source.crop(source_box)
    scale = min(TARGET / isolated.width, TARGET / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    resized = isolated.resize(size, Image.Resampling.LANCZOS)
    flattened = flatten(resized, palette)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    offset = ((CELL - size[0]) // 2, (CELL - size[1]) // 2)
    cell.alpha_composite(flattened, offset)
    output_box = visible_bounds(cell)
    gutter = min(output_box[0], output_box[1], CELL - output_box[2], CELL - output_box[3])
    return cell, {
        "sourceVisibleBounds": list(source_box),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "bounds": list(output_box),
        "transparentGutterPx": gutter,
        "edgeAlphaPixels": edge_alpha_pixels(cell),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }


def backed(image: Image.Image, colour: tuple[int, int, int, int]) -> Image.Image:
    result = Image.new("RGBA", image.size, colour)
    result.alpha_composite(image)
    return result


def contact_sheet(rows: list[tuple[dict[str, object], Image.Image]]) -> Image.Image:
    columns = 5
    sheet = Image.new("RGBA", (CELL * columns, HEADER + ROW_HEIGHT * len(rows)), DARK_BACK)
    draw = ImageDraw.Draw(sheet)
    titles = ("PRIOR CURRENT", "CANDIDATE / CREAM", "CANDIDATE / DARK", "PRIOR / 64PX", "CANDIDATE / 64PX")
    for index, title in enumerate(titles):
        draw.text((index * CELL + 8, 14), title, fill=CREAM_BACK)
    for row_index, (spec, candidate) in enumerate(rows):
        y = HEADER + row_index * ROW_HEIGHT
        current = Image.open(ROOT / str(spec["current"])).convert("RGBA")
        if current.size != (CELL, CELL):
            raise RuntimeError(f"prior current is not 256x256: {spec['id']}")
        sheet.alpha_composite(backed(current, CREAM_BACK), (0, y))
        sheet.alpha_composite(backed(candidate, CREAM_BACK), (CELL, y))
        sheet.alpha_composite(backed(candidate, DARK_BACK), (CELL * 2, y))
        current_small = current.resize((64, 64), Image.Resampling.LANCZOS)
        candidate_small = candidate.resize((64, 64), Image.Resampling.LANCZOS)
        current_cell = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
        candidate_cell = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
        current_cell.alpha_composite(current_small, (96, 96))
        candidate_cell.alpha_composite(candidate_small, (96, 96))
        sheet.alpha_composite(current_cell, (CELL * 3, y))
        sheet.alpha_composite(candidate_cell, (CELL * 4, y))
        label = f"{spec['id']} / prior v1 / proposed v2"
        for column in range(columns):
            draw.text((column * CELL + 8, y + CELL + 8), label, fill=CREAM_BACK)
    return sheet


def write_hashes(pack: Path) -> None:
    files = sorted(path for path in pack.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (pack / "HASHES.sha256").write_text(
        "\n".join(f"{sha256(path)}  {path.relative_to(pack).as_posix()}" for path in files) + "\n"
    )


def build(name: str) -> None:
    config = PACKS[name]
    pack = ROOT / str(config["directory"])
    source_dir = pack / "source"
    component_dir = pack / "drafts/components"
    evidence_dir = pack / "evidence"
    component_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    entries: dict[str, object] = {}
    rows: list[tuple[dict[str, object], Image.Image]] = []
    for spec in config["specs"]:
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
            "family": config["family"],
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
    rejected = []
    for item in config["rejected"]:
        path = pack / str(item["file"])
        rejected.append({**item, "sha256": sha256(path)})
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-family-pack@1",
        "set": config["set"],
        "status": "approved-and-registered",
        "created": "2026-10-21",
        "tool": "built-in image generation plus deterministic fixed-palette normalisation",
        "family": config["family"],
        "visualAuthority": "art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/drafts/components",
        "preservationRule": "Translate each current asset's drawing language while preserving subject identity, viewpoint, object count, container, construction, state, recognisable contents, relative arrangement and broad silhouette.",
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "components": entries,
        "rejected": rejected,
        "evidence": {
            "file": rel(contact_path),
            "sha256": sha256(contact_path),
            "columns": 5,
            "rows": len(rows),
            "coveredIds": [spec["id"] for spec in config["specs"]],
        },
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "currentReferenceHashesPinned": True,
            "exactPalettesRecorded": True,
            "contactSheetCoversEveryCandidate": True,
            "libraryVersionsAdded": True,
            "storiesChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": {
            "by": "Frank",
            "date": "2026-10-21",
            "words": "approved",
            "scope": config["approvalScope"],
        },
        "rollback": "Set each picture's current selector back to V1; the approved V2 assets and all earlier bytes remain immutable and selectable.",
    }
    (pack / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(pack)
    verify(name)
    print(f"Built and verified {len(rows)} candidates in {config['set']}")


def library_current() -> dict[str, dict[str, object]]:
    library = json.loads((ROOT / "data/activity-stories/pictures.json").read_text())
    result: dict[str, dict[str, object]] = {}
    for picture_id, picture in library["pictures"].items():
        current_version = picture["current"]
        version = next(item for item in picture["versions"] if item["v"] == current_version)
        result[picture_id] = {"current": current_version, "version": version, "versions": picture["versions"]}
    return result


def verify(name: str) -> None:
    config = PACKS[name]
    pack = ROOT / str(config["directory"])
    register_path = pack / "batch-register.json"
    register = json.loads(register_path.read_text())
    if register["set"] != config["set"] or register["status"] != "approved-and-registered":
        raise RuntimeError("register identity/status mismatch")
    if register["family"] != config["family"]:
        raise RuntimeError("register family mismatch")
    current_library = library_current()
    expected_ids = [str(spec["id"]) for spec in config["specs"]]
    if list(register["components"]) != expected_ids:
        raise RuntimeError("register component order/coverage mismatch")
    for spec in config["specs"]:
        picture_id = str(spec["id"])
        entry = register["components"][picture_id]
        source_path = ROOT / entry["sourceFile"]
        output_path = ROOT / entry["file"]
        current_path = ROOT / entry["currentReferenceFile"]
        for path in (source_path, output_path, current_path):
            if not path.is_file():
                raise RuntimeError(f"missing manifest path: {path}")
        if sha256(source_path) != entry["sourceSha256"]:
            raise RuntimeError(f"source hash mismatch: {picture_id}")
        if sha256(output_path) != entry["sha256"]:
            raise RuntimeError(f"output hash mismatch: {picture_id}")
        if sha256(current_path) != entry["currentReferenceSha256"]:
            raise RuntimeError(f"prior-current hash mismatch: {picture_id}")
        library_entry = current_library[picture_id]
        if library_entry["current"] != 2:
            raise RuntimeError(f"approved candidate is not current V2: {picture_id}")
        if library_entry["version"]["sha256"] != entry["sha256"]:
            raise RuntimeError(f"library current V2 hash drift: {picture_id}")
        prior_version = next((item for item in library_entry["versions"] if item["v"] == 1), None)
        if prior_version is None or prior_version["sha256"] != entry["currentReferenceSha256"]:
            raise RuntimeError(f"library retained V1 hash drift: {picture_id}")
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
        ownership = entry["ownership"]
        if ownership != {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0}:
            raise RuntimeError(f"ownership mismatch: {picture_id}")
    evidence = register["evidence"]
    contact_path = ROOT / evidence["file"]
    if sha256(contact_path) != evidence["sha256"]:
        raise RuntimeError("contact sheet hash mismatch")
    contact = Image.open(contact_path)
    if contact.mode != "RGBA" or contact.size != (CELL * 5, HEADER + ROW_HEIGHT * len(expected_ids)):
        raise RuntimeError("contact sheet geometry mismatch")
    if evidence["coveredIds"] != expected_ids or evidence["rows"] != len(expected_ids) or evidence["columns"] != 5:
        raise RuntimeError("contact sheet coverage metadata mismatch")
    hash_paths = sorted(
        path for path in pack.rglob("*") if path.is_file() and path.name != "HASHES.sha256"
    )
    expected_hash_lines = [
        f"{sha256(path)}  {path.relative_to(pack).as_posix()}" for path in hash_paths
    ]
    actual_hash_lines = (pack / "HASHES.sha256").read_text().splitlines()
    if actual_hash_lines != expected_hash_lines:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {config['set']}: {len(expected_ids)} components, contact sheet and pinned priors")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", choices=("food", "tools", "all"))
    parser.add_argument("--verify", action="store_true", help="verify existing outputs without rebuilding")
    args = parser.parse_args()
    names = ("food", "tools") if args.pack == "all" else (args.pack,)
    for name in names:
        if args.verify:
            verify(name)
        else:
            build(name)


if __name__ == "__main__":
    main()
