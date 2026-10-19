#!/usr/bin/env python3
"""Build Kitchen Oven V27 with fixed state registration and shaped flicker masks."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-standalone-v27"
BATCH = "kitchen-oven-standalone-2026-10-19-v27"
SOURCE_DIR = ROOT / "art/source" / BATCH
RAW_DIR = ROOT / "art/raw" / BATCH
DRAFT_DIR = ROOT / "art/drafts" / BATCH
PUBLIC_DIR = ROOT / "public/keeper-review" / SET
TEMPLATE = ROOT / "scripts/templates/kitchen_oven_standalone_v27.html"

SOURCE_STATES = SOURCE_DIR / "oven-three-state-registered-source.png"
SOURCE_PROVENANCE = SOURCE_DIR / "generation-provenance.json"
SOURCE_REFERENCE = ROOT / "art/source/kitchen-oven-standalone-2026-10-19-v26/oven-three-state-broken-lit-generated-source.png"
ROOM_BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"
CABINET_CELL = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"
CABINET_APPROVAL = ROOT / "docs/review/kitchen-cabinet-run-v11-approval-2026-10-19.json"

CELL_SOURCE = (724, 724)
BODY_SIZE = (84, 77)
CELL_SIZE = (92, 85)
GUTTER = (4, 4)
ROOM_SIZE = (772, 224)
OVEN_BODY_ORIGIN = (336, 131)
OVEN_CELL_ORIGIN = (332, 127)
CABINET_CELL_ORIGINS = ((164, 130), (416, 130))
FRAME_COUNT = 40
FPS = 4

# Equal source-space windows pin the chassis to one scale.  Their x offsets
# compensate only for the three generated cells' different transparent padding.
# Unlike V26, no state is independently normalised to its own alpha bounds.
SOURCE_WINDOWS = (
    (116, 48, 710, 667),
    (65, 48, 659, 667),
    (13, 48, 607, 667),
)
ON_REGIONS = ((11, 15, 74, 29), (11, 30, 74, 68))
CAVITY_REGIONS = ((13, 31, 72, 48), (17, 47, 68, 66))
WARNING_SEARCH_REGION = (62, 13, 80, 29)

# Uneven 40-frame fault grammar: isolated flashes, short sputters and terminal
# flutter. It deliberately has no short repeated cadence.
CAVITY_PATTERN = [
    0, 0, 0, 1, 0, 0, 0, 0, 1, 1,
    0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    1, 0, 0, 1, 1, 1, 0, 0, 0, 1,
    0, 0, 1, 0, 1, 1, 0, 1, 0, 1,
]
WARNING_PATTERN = [
    1, 0, 1, 1, 0, 1, 0, 0, 1, 0,
    1, 1, 1, 0, 1, 0, 1, 1, 0, 0,
    1, 0, 1, 0, 0, 1, 1, 0, 1, 1,
    0, 1, 0, 1, 1, 1, 0, 1, 0, 0,
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_alpha(image: Image.Image) -> Image.Image:
    result = image.convert("RGBA")
    pixels = result.load()
    for y in range(result.height):
        for x in range(result.width):
            r, g, b, a = pixels[x, y]
            if a < 8:
                pixels[x, y] = (0, 0, 0, 0)
    return result


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def extract_native_body(sheet: Image.Image, index: int) -> tuple[Image.Image, tuple[int, int, int, int]]:
    left = index * CELL_SOURCE[0]
    cell = clean_alpha(sheet.crop((left, 0, left + CELL_SOURCE[0], CELL_SOURCE[1])))
    visible_bbox = cell.getchannel("A").point(lambda value: 255 if value >= 8 else 0).getbbox()
    if visible_bbox is None:
        raise RuntimeError(f"Source state {index} contains no visible pixels")
    window = SOURCE_WINDOWS[index]
    body = resize_premultiplied(cell.crop(window), BODY_SIZE)
    return body, visible_bbox


def to_cell(body: Image.Image) -> Image.Image:
    cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
    cell.alpha_composite(body, GUTTER)
    return cell


def paste_regions(target: Image.Image, source: Image.Image, regions: tuple[tuple[int, int, int, int], ...]) -> None:
    for region in regions:
        target.paste(source.crop(region), region)


def compose_on(off_body: Image.Image, on_source: Image.Image) -> Image.Image:
    """Keep one exact exterior and replace only the On-state semantic pixels."""
    result = off_body.copy()
    paste_regions(result, on_source, ON_REGIONS)
    result.putalpha(off_body.getchannel("A"))
    return result


def cavity_light_mask(image: Image.Image) -> Image.Image:
    """Select lit cavity pixels by shape and colour, never by a solid rectangle."""
    mask = Image.new("L", BODY_SIZE, 0)
    src = image.load()
    dst = mask.load()
    for x0, y0, x1, y1 in CAVITY_REGIONS:
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, a = src[x, y]
                luminance = (3 * r + 5 * g + 2 * b) // 10
                if a and r > 55 and r >= g + 8 and g >= b - 6 and luminance < 235:
                    dst[x, y] = 255
    return mask.filter(ImageFilter.MaxFilter(3))


def warning_light_mask(image: Image.Image) -> Image.Image:
    """Follow the round red lamp itself; V26's broad fascia box is forbidden."""
    mask = Image.new("L", BODY_SIZE, 0)
    src = image.load()
    dst = mask.load()
    x0, y0, x1, y1 = WARNING_SEARCH_REGION
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = src[x, y]
            # The ivory fascia is warm too, so hue alone is insufficient.
            # Select only the saturated red ring; one-pixel dilation then owns
            # the lamp highlight without ever reaching the surrounding panel.
            if a and r > 105 and g < 105 and b < 90 and r > g * 3 // 2:
                dst[x, y] = 255
    return mask.filter(ImageFilter.MaxFilter(3))


def dim_with_mask(image: Image.Image, mask: Image.Image, *, cavity: bool) -> Image.Image:
    result = image.copy()
    src = image.load()
    dst = result.load()
    selected = mask.load()
    for y in range(BODY_SIZE[1]):
        for x in range(BODY_SIZE[0]):
            amount = selected[x, y]
            if not amount:
                continue
            r, g, b, a = src[x, y]
            if cavity:
                dark = (max(10, r * 28 // 100), max(9, g * 25 // 100), max(12, b * 35 // 100), a)
            else:
                dark = (max(26, r * 22 // 100), max(5, g * 12 // 100), max(8, b * 16 // 100), a)
            blend = amount / 255
            dst[x, y] = tuple(round(old * (1 - blend) + new * blend) for old, new in zip((r, g, b, a), dark))
    return result


def make_strip(frames: list[Image.Image]) -> Image.Image:
    strip = Image.new("RGBA", (CELL_SIZE[0] * len(frames), CELL_SIZE[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * CELL_SIZE[0], 0))
    return strip


def write_image(image: Image.Image, name: str) -> Path:
    path = RAW_DIR / name
    image.save(path)
    return path


def main() -> None:
    for required in (SOURCE_REFERENCE, SOURCE_STATES, SOURCE_PROVENANCE, ROOM_BACKGROUND, CABINET_CELL, CABINET_APPROVAL, TEMPLATE):
        if not required.exists():
            raise FileNotFoundError(required)
    if len(CAVITY_PATTERN) != FRAME_COUNT or len(WARNING_PATTERN) != FRAME_COUNT:
        raise RuntimeError("Flicker patterns must contain exactly 40 frames")

    for directory in (RAW_DIR, DRAFT_DIR, PUBLIC_DIR):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    sheet = Image.open(SOURCE_STATES).convert("RGBA")
    if sheet.size != (CELL_SOURCE[0] * 3, CELL_SOURCE[1]):
        raise RuntimeError(f"Generated state sheet is {sheet.size}, expected 2172x724")

    off_body, off_bbox = extract_native_body(sheet, 0)
    on_source_body, on_bbox = extract_native_body(sheet, 1)
    broken_lit_body, broken_bbox = extract_native_body(sheet, 2)
    on_body = compose_on(off_body, on_source_body)

    cavity_mask = cavity_light_mask(broken_lit_body)
    warning_mask = warning_light_mask(broken_lit_body)
    broken_dark_body = dim_with_mask(broken_lit_body, cavity_mask, cavity=True)
    # The Off state supplies the exact ivory fascia and dormant lamp beneath
    # the round warning mask.  This removes the V26 black rectangle while
    # retaining a clearly readable unlit indicator.
    broken_dark_body.paste(off_body, (0, 0), warning_mask)
    broken_cavity_body = broken_dark_body.copy()
    broken_cavity_body.paste(broken_lit_body, (0, 0), cavity_mask)
    broken_warning_body = broken_dark_body.copy()
    broken_warning_body.paste(broken_lit_body, (0, 0), warning_mask)
    broken_both_body = broken_dark_body.copy()
    broken_both_body.paste(broken_lit_body, (0, 0), cavity_mask)
    broken_both_body.paste(broken_lit_body, (0, 0), warning_mask)

    cells = {
        "oven-off.png": to_cell(off_body),
        "oven-on.png": to_cell(on_body),
        "oven-broken.png": to_cell(broken_dark_body),
        "oven-broken-cavity-lit.png": to_cell(broken_cavity_body),
        "oven-broken-warning-lit.png": to_cell(broken_warning_body),
        "oven-broken-both-lit.png": to_cell(broken_both_body),
    }
    outputs: list[Path] = [write_image(image, name) for name, image in cells.items()]

    state_strip = Image.new("RGBA", (CELL_SIZE[0] * 3, CELL_SIZE[1]), (0, 0, 0, 0))
    for index, name in enumerate(("oven-off.png", "oven-on.png", "oven-broken.png")):
        state_strip.alpha_composite(cells[name], (index * CELL_SIZE[0], 0))
    outputs.append(write_image(state_strip, "oven-state-family-strip.png"))

    cavity_frames = [cells["oven-broken-cavity-lit.png"] if value else cells["oven-broken.png"] for value in CAVITY_PATTERN]
    warning_frames = [cells["oven-broken-warning-lit.png"] if value else cells["oven-broken.png"] for value in WARNING_PATTERN]
    outputs.append(write_image(make_strip(cavity_frames), "oven-broken-cavity-flicker-f40.png"))
    outputs.append(write_image(make_strip(warning_frames), "oven-broken-warning-flicker-f40.png"))

    room_background = Image.open(ROOM_BACKGROUND).convert("RGBA")
    cabinet = Image.open(CABINET_CELL).convert("RGBA")
    if room_background.size != ROOM_SIZE or cabinet.size != (176, 82):
        raise RuntimeError("Room or approved V11 cabinet authority changed dimensions")
    room_cells = {
        "off": cells["oven-off.png"],
        "on": cells["oven-on.png"],
        "broken": cells["oven-broken.png"],
        "broken-cavity-lit": cells["oven-broken-cavity-lit.png"],
        "broken-warning-lit": cells["oven-broken-warning-lit.png"],
        "broken-both-lit": cells["oven-broken-both-lit.png"],
    }
    for state, oven_cell in room_cells.items():
        room = room_background.copy()
        for origin in CABINET_CELL_ORIGINS:
            room.alpha_composite(cabinet, origin)
        room.alpha_composite(oven_cell, OVEN_CELL_ORIGIN)
        outputs.append(write_image(room, f"oven-{state}-native-room.png"))

    asset_hashes = {path.name: sha256(path) for path in outputs}
    catalogue = {
        "schema": "lighthouse-keeper/kitchen-standalone-state-family@1",
        "set": SET,
        "version": 27,
        "status": "reversible-unapproved-unpromoted",
        "authorities": {
            "approvedCabinet": {"file": str(CABINET_CELL.relative_to(ROOT)), "sha256": sha256(CABINET_CELL)},
            "cabinetApproval": {"file": str(CABINET_APPROVAL.relative_to(ROOT)), "sha256": sha256(CABINET_APPROVAL)},
            "roomBackground": {"file": str(ROOM_BACKGROUND.relative_to(ROOT)), "sha256": sha256(ROOM_BACKGROUND)},
        },
        "sources": {
            "v26LitFamilyReference": {"file": str(SOURCE_REFERENCE.relative_to(ROOT)), "sha256": sha256(SOURCE_REFERENCE)},
            "registeredFamily": {"file": str(SOURCE_STATES.relative_to(ROOT)), "sha256": sha256(SOURCE_STATES)},
            "generationProvenance": {"file": str(SOURCE_PROVENANCE.relative_to(ROOT)), "sha256": sha256(SOURCE_PROVENANCE)},
            "generationMode": "built-in-imagegen",
            "sourceCellPixels": list(CELL_SOURCE),
            "fixedSourceWindows": [list(window) for window in SOURCE_WINDOWS],
            "visibleBBoxes": {"off": list(off_bbox), "on": list(on_bbox), "broken": list(broken_bbox)},
        },
        "geometry": {
            "logicalBodyPixels": list(BODY_SIZE),
            "cellPixels": list(CELL_SIZE),
            "transparentGutterPixels": list(GUTTER),
            "ovenBodyBoundsInRoom": [336, 131, 84, 77],
            "ovenCellOriginInRoom": list(OVEN_CELL_ORIGIN),
            "cabinetBodyBounds": [[168, 134, 168, 74], [420, 134, 168, 74]],
            "primeInteractionAnchor": [378, 218],
            "projection": "straight-on-flat-cutaway-parallel",
            "offOnExteriorEnvelopeByteIdentical": True,
            "onSemanticRegionsInBody": [list(region) for region in ON_REGIONS],
            "roomVariantCompositing": "complete-precomposed-room-images-no-canvas-clearRect",
        },
        "states": {
            "off": {"file": "oven-off.png", "hobIntegrated": True, "cavityLight": False, "warningLight": False},
            "on": {"file": "oven-on.png", "hobIntegrated": True, "cavityLight": True, "warningLight": "solid", "roastingDish": "visible"},
            "broken": {
                "file": "oven-broken.png",
                "hobIntegrated": True,
                "door": "attached-bottom-hinge-opening-straight-toward-camera",
                "doorWindowTransparent": True,
                "roastingDish": "burnt-blackened",
                "failedDial": "hanging-from-fascia-on-exactly-two-wires",
                "smokeBakedIntoBase": False,
                "visibleElectricalEffectsBakedIntoBase": False,
            },
        },
        "lighting": {
            "baseFps": FPS,
            "frameCount": FRAME_COUNT,
            "durationSeconds": FRAME_COUNT / FPS,
            "speedRange": [0.1, 4.0],
            "cavityPattern": CAVITY_PATTERN,
            "warningPattern": WARNING_PATTERN,
            "sameBrokenGeometryForEveryLightingVariant": True,
            "maskMethod": "shape-and-colour-derived-no-rectangular-fascia-darkening",
            "maskOpaquePixels": {
                "cavity": sum(cavity_mask.histogram()[1:]),
                "warning": sum(warning_mask.histogram()[1:]),
            },
            "regionsInNativeBody": {"cavitySearch": [list(region) for region in CAVITY_REGIONS], "warningSearch": list(WARNING_SEARCH_REGION)},
            "cavityStrip": "oven-broken-cavity-flicker-f40.png",
            "warningStrip": "oven-broken-warning-flicker-f40.png",
            "completeRoomVariants": [f"oven-{name}-native-room.png" for name in room_cells],
        },
        "sfxPlaceholders": [
            "kitchen_oven_on_fan_low_loop",
            "kitchen_oven_broken_low_electrical_buzz_loop",
            "kitchen_oven_broken_warning_light_angry_blink_loop",
            "kitchen_oven_broken_cavity_failing_bulb_loop",
            "kitchen_oven_broken_smoke_hiss_loop",
        ],
        "publishedAssets": asset_hashes,
        "boundaries": {
            "approvedCabinetChanged": False,
            "roomBackgroundChanged": False,
            "finalChanged": False,
            "runtimeChanged": False,
            "promotionPerformed": False,
            "nextAssetStarted": False,
        },
    }
    catalogue_path = DRAFT_DIR / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n", encoding="utf-8")

    page_path = PUBLIC_DIR / "index.html"
    page_path.write_text(TEMPLATE.read_text(encoding="utf-8").replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))), encoding="utf-8")
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "reversible-unapproved-unpromoted",
        "candidate": {
            "catalogue": {"file": str(catalogue_path.relative_to(ROOT)), "sha256": sha256(catalogue_path)},
            "publicShell": {"file": str(page_path.relative_to(ROOT)), "sha256": sha256(page_path)},
        },
        "sources": [
            {"file": str(path.relative_to(ROOT)), "sha256": sha256(path)}
            for path in (SOURCE_REFERENCE, SOURCE_STATES, SOURCE_PROVENANCE)
        ],
        "publishedAssets": [
            {
                "source": str(path.relative_to(ROOT)),
                "sourceSha256": sha256(path),
                "publicAssemblyPath": str((PUBLIC_DIR / "assets" / path.name).relative_to(ROOT)),
            }
            for path in outputs
        ],
    }
    (DRAFT_DIR / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n", encoding="utf-8")
    print(f"Built {SET}: fixed Off/On envelope, shaped Broken flicker masks, and intact cabinet joins")


if __name__ == "__main__":
    main()
