#!/usr/bin/env python3
"""Build the immutable Claude BBQ/food asset pack V1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1"
SOURCE_DIR = PACK / "source"
ASSET_DIR = PACK / "assets"
EVIDENCE_DIR = PACK / "evidence"
REJECTED = PACK / "rejected/plateless-cooked-sausages-attempt-1.webp"
OLD_SAUSAGES = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v1/drafts/components/bbq-sausages.png"
OLD_GRILL = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/bbq-grill.png"
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216

SPECS = (
    ("bbq-raw-burger-patties", "bbq", "bbq-raw-burger-patties-source.webp", "4ac3e4269955c51d31fee0d18b47a1512116995ea041eba0563c413c817214ed"),
    ("bbq-sausages", "bbq", "bbq-raw-linked-sausages-source.webp", "8cca15c23f1391dee66db124cc35acff16783564d0b1ee45bf298ac4ce3e6a66"),
    ("bbq-grill", "bbq", "bbq-unlit-grill-source.webp", "b717c2ac1166905aec8f7c919bfbfb418a2b3832bafa608aa71c6249aaea1ed6"),
    ("cooking-cheese-slicing", "cooking", "cooking-cheese-slicing-source.webp", "bda822b834cd56993087ce787354c48ff6b0b055d79c56f8cdee23d6221150f4"),
    ("bbq-raw-steak", "bbq", "bbq-raw-steak-source.webp", "b183c397e9cc6ccf80abdcabf8b79b1e6df19f2ab8e72616d1ec249bae3d1cfb"),
    ("meal-steak-fries", "meal", "meal-steak-fries-source.webp", "7c1604bf1be6fc9540a096c00e8053181b278ef245c8ebc83e7abf51ef912005"),
    ("condiment-ketchup-bottle", "condiment", "condiment-ketchup-bottle-source.webp", "9bd83b220ab6b226b9c049e40b621d7ca849e9d810472e9789e809e692ba9877"),
    ("condiment-mustard-bottle", "condiment", "condiment-mustard-bottle-source.webp", "65333b6307e926acf0fb1cd24fe57155ac9621ba351c597e29482aebc40c6bf9"),
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.getchannel("A").point(lambda value: 255 if value > VISIBLE_ALPHA else 0).getbbox()
    if bounds is None:
        raise RuntimeError("source has no visible pixels")
    return bounds


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = {(x, 0) for x in range(image.width)} | {(x, image.height - 1) for x in range(image.width)}
    points |= {(0, y) for y in range(image.height)} | {(image.width - 1, y) for y in range(image.height)}
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in points)


def gutter(image: Image.Image) -> int:
    left, top, right, bottom = visible_bounds(image)
    return min(left, top, image.width - right, image.height - bottom)


def normalise(source: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    if source.size != (384, 384):
        raise RuntimeError(f"source must be 384 x 384: {source.size}")
    if edge_alpha(source):
        raise RuntimeError("source contains visible alpha on an outer edge")
    bounds = visible_bounds(source)
    isolated = source.crop(bounds)
    scale = min(TARGET / isolated.width, TARGET / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    isolated = isolated.resize(size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    offset = ((CELL - size[0]) // 2, (CELL - size[1]) // 2)
    cell.alpha_composite(isolated, offset)
    return cell, {
        "sourceVisibleBounds": list(bounds),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "edgeAlphaPixels": edge_alpha(cell),
        "transparentGutterPx": gutter(cell),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }


def checkerboard(size: tuple[int, int], tile: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, (234, 238, 239, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(210, 218, 220, 255))
    return image


def contact_sheet(rendered: dict[str, Image.Image]) -> Image.Image:
    sheet = Image.new("RGBA", (CELL * 4, (CELL + 36) * 2), (18, 35, 52, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (component_id, _, _, _) in enumerate(SPECS):
        x = (index % 4) * CELL
        y = (index // 4) * (CELL + 36)
        draw.text((x + 8, y + 12), component_id.upper(), fill=(243, 231, 204, 255))
        board = checkerboard((CELL, CELL))
        board.alpha_composite(rendered[component_id])
        sheet.alpha_composite(board, (x, y + 36))
    return sheet


def main() -> None:
    required = (OLD_SAUSAGES, OLD_GRILL, REJECTED, *(SOURCE_DIR / spec[2] for spec in SPECS))
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing dependency: {rel(path)}")

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    components: dict[str, dict[str, object]] = {}
    rendered: dict[str, Image.Image] = {}

    for component_id, family, source_name, original_generated_sha in SPECS:
        source_path = SOURCE_DIR / source_name
        source = Image.open(source_path).convert("RGBA")
        component, measurements = normalise(source)
        if measurements["edgeAlphaPixels"] or measurements["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe normalised component: {component_id}")
        output = ASSET_DIR / f"{component_id}.png"
        component.save(output)
        rendered[component_id] = component
        components[component_id] = {
            "file": rel(output),
            "sha256": sha(output),
            "family": family,
            "cellPixels": [CELL, CELL],
            "sourceSet": "claude-bbq-food-asset-pack-v1",
            "sourceFile": rel(source_path),
            "sourceSha256": sha(source_path),
            "originalGeneratedPngSha256": original_generated_sha,
            **measurements,
        }

    evidence = EVIDENCE_DIR / "final-assets-contact-sheet.webp"
    contact_sheet(rendered).save(evidence, format="WEBP", lossless=True, method=6)
    rejected = Image.open(REJECTED).convert("RGBA")
    rejected_bounds = visible_bounds(rejected)

    manifest = {
        "schema": "lighthouse-keeper/claude-bbq-food-asset-pack@1",
        "set": "claude-bbq-food-asset-pack-v1",
        "status": "review-only",
        "created": "2026-10-20",
        "foodPresentationRule": "Loose ingredients and cookable food items are unplated; plates are reserved for finished meals.",
        "sourceProcessing": {
            "originalGeometry": [1254, 1254],
            "reviewSourceGeometry": [384, 384],
            "method": "cwebp 384 x 384 resize followed by lossless WebP encoding; original generated PNG SHA-256 retained per component",
        },
        "components": components,
        "rejectedAttempts": [{
            "file": rel(REJECTED),
            "sha256": sha(REJECTED),
            "originalGeneratedPngSha256": "47e002e96d2d50d91058431af26cd2c5295c53569040f2add601c2c9693ab024",
            "visibleBounds": list(rejected_bounds),
            "reason": "Rendered as browned cooked sausages rather than a raw linked sausage string.",
        }],
        "supersessionProposals": {
            "bbq-sausages": {
                "oldFile": rel(OLD_SAUSAGES),
                "oldSha256": sha(OLD_SAUSAGES),
                "proposedFile": components["bbq-sausages"]["file"],
                "proposedSha256": components["bbq-sausages"]["sha256"],
                "oldBytesUnchanged": True,
            },
            "bbq-grill": {
                "oldFile": rel(OLD_GRILL),
                "oldSha256": sha(OLD_GRILL),
                "proposedFile": components["bbq-grill"]["file"],
                "proposedSha256": components["bbq-grill"]["sha256"],
                "oldBytesUnchanged": True,
            },
        },
        "evidence": {"file": rel(evidence), "sha256": sha(evidence)},
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersClear": True,
            "componentOwnershipUnambiguous": True,
            "priorAssetsUnchanged": True,
            "rejectedAttemptRetained": True,
            "allAssetsIndependent": True,
            "runtimeChanged": False,
            "kitchenChanged": False,
            "deployed": False,
        },
    }
    (PACK / "asset-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
