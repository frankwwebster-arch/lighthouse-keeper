#!/usr/bin/env python3
"""Build Oven V29 by lowering only V28's Broken fixed-shelf contents."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-standalone-v29"
BATCH = "kitchen-oven-standalone-2026-10-20-v29"
SOURCE_DIR = ROOT / "art/source" / BATCH
RAW_DIR = ROOT / "art/raw" / BATCH
DRAFT_DIR = ROOT / "art/drafts" / BATCH
PUBLIC_DIR = ROOT / "public/keeper-review" / SET
TEMPLATE = ROOT / "scripts/templates/kitchen_oven_standalone_v29.html"

V28_BATCH = "kitchen-oven-standalone-2026-10-20-v28"
V28_RAW = ROOT / "art/raw" / V28_BATCH
V28_CATALOGUE = ROOT / "art/drafts" / V28_BATCH / "candidate-catalogue.json"
V27_APPROVAL = ROOT / "docs/review/kitchen-oven-standalone-v27-state-family-approval-2026-10-20.json"
SOURCE_FIXED_SHELF = SOURCE_DIR / "oven-broken-lowered-fixed-shelf-generated-source.png"
SOURCE_PROVENANCE = SOURCE_DIR / "generation-provenance.json"
ROOM_BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"
CABINET_CELL = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"
CABINET_APPROVAL = ROOT / "docs/review/kitchen-cabinet-run-v11-approval-2026-10-19.json"

BODY_SIZE = (84, 77)
CELL_SIZE = (92, 85)
GUTTER = (4, 4)
ROOM_SIZE = (772, 224)
OVEN_BODY_ORIGIN = (336, 131)
OVEN_CELL_ORIGIN = (332, 127)
CABINET_CELL_ORIGINS = ((164, 130), (416, 130))
FIXED_SHELF_SOURCE_WINDOW = (1451, 35, 2058, 698)
FIXED_SHELF_BODY_PATCH = (14, 35, 70, 51)
SHELF_FOCUS_BOX = (10, 27, 82, 72)
FRAME_COUNT = 40
FPS = 4

STATE_NAMES = (
    "oven-off.png",
    "oven-on.png",
    "oven-broken.png",
    "oven-broken-cavity-lit.png",
    "oven-broken-warning-lit.png",
    "oven-broken-both-lit.png",
)


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


def to_cell(body: Image.Image) -> Image.Image:
    cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
    cell.alpha_composite(body, GUTTER)
    return cell


def body_from_cell(cell: Image.Image) -> Image.Image:
    return cell.convert("RGBA").crop((GUTTER[0], GUTTER[1], GUTTER[0] + BODY_SIZE[0], GUTTER[1] + BODY_SIZE[1]))


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
    required = [
        SOURCE_FIXED_SHELF,
        SOURCE_PROVENANCE,
        V28_CATALOGUE,
        V27_APPROVAL,
        ROOM_BACKGROUND,
        CABINET_CELL,
        CABINET_APPROVAL,
        TEMPLATE,
        *[V28_RAW / name for name in STATE_NAMES],
    ]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(path)

    for directory in (RAW_DIR, DRAFT_DIR, PUBLIC_DIR):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    shelf_source = Image.open(SOURCE_FIXED_SHELF).convert("RGBA")
    if shelf_source.size != (2172, 724):
        raise RuntimeError(f"Fixed-shelf source is {shelf_source.size}, expected 2172x724")
    fixed_shelf_lit = clean_alpha(
        resize_premultiplied(shelf_source.crop(FIXED_SHELF_SOURCE_WINDOW), BODY_SIZE)
    )
    cells: dict[str, Image.Image] = {}
    v28_hashes: dict[str, str] = {}
    for name in STATE_NAMES:
        authority_path = V28_RAW / name
        authority = Image.open(authority_path).convert("RGBA")
        if authority.size != CELL_SIZE:
            raise RuntimeError(f"V28 authority {name} changed dimensions")
        body = body_from_cell(authority)
        if name.startswith("oven-broken"):
            x0, y0, x1, y1 = FIXED_SHELF_BODY_PATCH
            patch = fixed_shelf_lit.crop(FIXED_SHELF_BODY_PATCH)
            if "cavity-lit" not in name and "both-lit" not in name:
                patch_pixels = patch.load()
                for py in range(patch.height):
                    for px in range(patch.width):
                        r, g, b, a = patch_pixels[px, py]
                        patch_pixels[px, py] = (
                            round(r * 0.33),
                            round(g * 0.39),
                            round(b * 0.60),
                            a,
                        )
            body.paste(patch, (x0, y0))
        cells[name] = to_cell(body)
        v28_hashes[name] = sha256(authority_path)

    outputs: list[Path] = [write_image(image, name) for name, image in cells.items()]

    state_strip = Image.new("RGBA", (CELL_SIZE[0] * 3, CELL_SIZE[1]), (0, 0, 0, 0))
    for index, name in enumerate(("oven-off.png", "oven-on.png", "oven-broken.png")):
        state_strip.alpha_composite(cells[name], (index * CELL_SIZE[0], 0))
    outputs.append(write_image(state_strip, "oven-state-family-strip.png"))

    v28_data = json.loads(V28_CATALOGUE.read_text(encoding="utf-8"))
    cavity_pattern = v28_data["lighting"]["cavityPattern"]
    warning_pattern = v28_data["lighting"]["warningPattern"]
    if len(cavity_pattern) != FRAME_COUNT or len(warning_pattern) != FRAME_COUNT:
        raise RuntimeError("V28 lighting authority no longer has exactly 40 frames")
    cavity_frames = [cells["oven-broken-cavity-lit.png"] if value else cells["oven-broken.png"] for value in cavity_pattern]
    warning_frames = [cells["oven-broken-warning-lit.png"] if value else cells["oven-broken.png"] for value in warning_pattern]
    outputs.append(write_image(make_strip(cavity_frames), "oven-broken-cavity-flicker-f40.png"))
    outputs.append(write_image(make_strip(warning_frames), "oven-broken-warning-flicker-f40.png"))

    room_background = Image.open(ROOM_BACKGROUND).convert("RGBA")
    cabinet = Image.open(CABINET_CELL).convert("RGBA")
    if room_background.size != ROOM_SIZE or cabinet.size != (176, 82):
        raise RuntimeError("Room or Cabinet V11 authority changed dimensions")
    room_cells = {
        "off": cells["oven-off.png"],
        "on": cells["oven-on.png"],
        "broken": cells["oven-broken.png"],
        "broken-cavity-lit": cells["oven-broken-cavity-lit.png"],
        "broken-warning-lit": cells["oven-broken-warning-lit.png"],
        "broken-both-lit": cells["oven-broken-both-lit.png"],
    }
    rooms: dict[str, Image.Image] = {}
    for state, oven_cell in room_cells.items():
        room = room_background.copy()
        for origin in CABINET_CELL_ORIGINS:
            room.alpha_composite(cabinet, origin)
        room.alpha_composite(oven_cell, OVEN_CELL_ORIGIN)
        rooms[state] = room
        outputs.append(write_image(room, f"oven-{state}-native-room.png"))

    outputs.append(write_image(Image.open(V28_RAW / "oven-broken.png").convert("RGBA").crop(SHELF_FOCUS_BOX), "oven-v28-shelf-focus.png"))
    outputs.append(write_image(cells["oven-broken.png"].crop(SHELF_FOCUS_BOX), "oven-v29-shelf-focus.png"))

    asset_hashes = {path.name: sha256(path) for path in outputs}
    catalogue = {
        "schema": "lighthouse-keeper/kitchen-standalone-state-family@1",
        "set": SET,
        "version": 29,
        "status": "reversible-unapproved-unpromoted",
        "authorities": {
            "approvedV27StateFamily": {"file": str(V27_APPROVAL.relative_to(ROOT)), "sha256": sha256(V27_APPROVAL)},
            "v28Catalogue": {"file": str(V28_CATALOGUE.relative_to(ROOT)), "sha256": sha256(V28_CATALOGUE)},
            "approvedCabinet": {"file": str(CABINET_CELL.relative_to(ROOT)), "sha256": sha256(CABINET_CELL)},
            "cabinetApproval": {"file": str(CABINET_APPROVAL.relative_to(ROOT)), "sha256": sha256(CABINET_APPROVAL)},
            "roomBackground": {"file": str(ROOM_BACKGROUND.relative_to(ROOT)), "sha256": sha256(ROOM_BACKGROUND)},
        },
        "sources": {
            "loweredFixedShelfGeneratedEdit": {"file": str(SOURCE_FIXED_SHELF.relative_to(ROOT)), "sha256": sha256(SOURCE_FIXED_SHELF)},
            "generationProvenance": {"file": str(SOURCE_PROVENANCE.relative_to(ROOT)), "sha256": sha256(SOURCE_PROVENANCE)},
            "generationMode": "built-in-imagegen",
            "finalSourcePixels": list(shelf_source.size),
            "fixedShelfSourceWindow": list(FIXED_SHELF_SOURCE_WINDOW),
            "v28StateHashes": v28_hashes,
        },
        "geometry": {
            "logicalBodyPixels": list(BODY_SIZE),
            "cellPixels": list(CELL_SIZE),
            "transparentGutterPixels": list(GUTTER),
            "ovenBodyBoundsInRoom": [336, 131, 84, 77],
            "ovenCellOriginInRoom": list(OVEN_CELL_ORIGIN),
            "cabinetBodyBounds": [[168, 134, 168, 74], [420, 134, 168, 74]],
            "primeInteractionAnchor": [378, 218],
            "projection": "cabinet-v11-shallow-straight-on-flat-cutaway",
            "brokenFixedShelfPatchInBody": list(FIXED_SHELF_BODY_PATCH),
            "brokenShelfAlignment": "roast-top-matches-on-state-with-lower-tray-occluded-by-door",
            "brokenDarkPatchRgbScale": [0.33, 0.39, 0.60],
            "offOnExteriorEnvelopeByteIdentical": True,
            "roomVariantCompositing": "complete-precomposed-room-images-no-canvas-clearRect",
            "shelfFocusBox": list(SHELF_FOCUS_BOX),
        },
        "states": v28_data["states"],
        "lighting": {
            **v28_data["lighting"],
            "completeRoomVariants": [f"oven-{name}-native-room.png" for name in room_cells],
        },
        "sfxPlaceholders": v28_data["sfxPlaceholders"],
        "publishedAssets": asset_hashes,
        "boundaries": {
            "v28StateFamilyChangedOutsideDeclaredPatch": False,
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
            for path in (SOURCE_FIXED_SHELF, SOURCE_PROVENANCE, V28_CATALOGUE, V27_APPROVAL)
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
    print(f"Built {SET}: V28 retained with Broken fixed-shelf contents lowered to the On-state level")


if __name__ == "__main__":
    main()
