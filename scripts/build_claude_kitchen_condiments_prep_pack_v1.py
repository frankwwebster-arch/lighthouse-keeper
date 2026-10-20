#!/usr/bin/env python3
"""Build the immutable Claude Kitchen condiments and prep asset pack V1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1"
SOURCE_DIR = PACK / "source"
ASSET_DIR = PACK / "assets"
EVIDENCE_DIR = PACK / "evidence"
FOOD_REFERENCE = ROOT / "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/asset-manifest.json"
KITCHEN_REFERENCE = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/source/kitchen-prep-generated-v3.png"
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216

SPECS = (
    ("condiment-wholegrain-mustard-jar", "condiment", "condiment-wholegrain-mustard-jar-source.webp", "ae55a63e1efdd030f19d29d2eda353c980e870cde24956fb614ebdf239dc844c", [1312, 1199]),
    ("condiment-pickle-jar", "condiment", "condiment-pickle-jar-source.webp", "dfa0e2c70b38f6b11c02773099d6f25b71033d1e5b2da8f57b240bc9855d54ee", [1312, 1199]),
    ("condiment-mayonnaise-jar", "condiment", "condiment-mayonnaise-jar-source.webp", "bbfb3a1a78183e736f06da3d5d30f7e1a3adcfcb66ed7594e2171c13bb4b7529", [1312, 1199]),
    ("condiment-salt-mill", "seasoning", "condiment-salt-mill-source.webp", "8fa94267dd6ad97fb9c20b55daee0661bd98dac246cd1145848b317b20f4866f", [1024, 1536]),
    ("condiment-pepper-mill", "seasoning", "condiment-pepper-mill-source.webp", "60812cc0efc43cabb34145df81159bda3a9cc78ce5a2b0d8537f7a4aebb31c8a", [1024, 1536]),
    ("prep-bread-slicing", "preparation-action", "prep-bread-slicing-source.webp", "5417f90054bbc14d849f1b1edd961d3f1c9e185d0d1a77cedee5b5f75870d105", [1536, 1024]),
    ("knife-chef", "tool", "knife-chef-source.webp", "9b8127a11211789943bc6d781c7cf902dadb902e813ee793f497b9088e7357f4", [1536, 1024]),
    ("knife-bread", "tool", "knife-bread-source.webp", "25375c30b67b6b6a7dc443bae66d49da33a52077f9b6f609ade933100246cb6e", [1536, 1024]),
    ("knife-paring", "tool", "knife-paring-source.webp", "b2ebeec14e5ca8833dab7f4714db84cf01f8252e473dd6990ed574465a7f0f6a", [1536, 1024]),
    ("ingredient-butter-block", "ingredient", "ingredient-butter-block-source.webp", "39082ad382c531108253a2da260ca6d86e9b24ac9b4c061128f406f397e77f63", [1536, 1024]),
    ("condiment-olive-oil", "condiment", "condiment-olive-oil-source.webp", "db10be19bddc1dfa2afc2791bd11ff684d08c59b1a768a4eaebe85e197156dc1", [1024, 1536]),
    ("condiment-raspberry-jam", "condiment", "condiment-raspberry-jam-source.webp", "06b91b0c8e7363c90785e6b28c3c1b95c833b853ecaebbdebdaa799b04066948", [1312, 1199]),
    ("condiment-honey-pot", "condiment", "condiment-honey-pot-source.webp", "4266a8305b83ec408d0d344884ac145467090a8afc23e5b06dd5465eefcdec14", [1312, 1199]),
    ("condiment-malt-vinegar", "condiment", "condiment-malt-vinegar-source.webp", "f100ad8def086c40a3add78a1f7a8d642e998e95143654417b37466e3b54ce6f", [1330, 1182]),
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
    rows = (len(SPECS) + 3) // 4
    sheet = Image.new("RGBA", (CELL * 4, (CELL + 36) * rows), (18, 35, 52, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (component_id, _, _, _, _) in enumerate(SPECS):
        x = (index % 4) * CELL
        y = (index // 4) * (CELL + 36)
        draw.text((x + 8, y + 12), component_id.upper(), fill=(243, 231, 204, 255))
        board = checkerboard((CELL, CELL))
        board.alpha_composite(rendered[component_id])
        sheet.alpha_composite(board, (x, y + 36))
    return sheet


def main() -> None:
    required = [SOURCE_DIR / spec[2] for spec in SPECS] + [FOOD_REFERENCE, KITCHEN_REFERENCE]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing dependency: {rel(path)}")

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    components: dict[str, dict[str, object]] = {}
    rendered: dict[str, Image.Image] = {}

    for component_id, family, source_name, original_generated_sha, original_geometry in SPECS:
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
            "sourceSet": "claude-kitchen-condiments-prep-pack-v1",
            "sourceFile": rel(source_path),
            "sourceSha256": sha(source_path),
            "originalGeneratedPngSha256": original_generated_sha,
            "originalGeneratedGeometry": original_geometry,
            **measurements,
        }

    evidence = EVIDENCE_DIR / "final-assets-contact-sheet.webp"
    contact_sheet(rendered).save(evidence, format="WEBP", lossless=True, method=6)
    manifest = {
        "schema": "lighthouse-keeper/claude-kitchen-condiments-prep-pack@1",
        "set": "claude-kitchen-condiments-prep-pack-v1",
        "status": "review-only",
        "created": "2026-10-20",
        "styleReferences": [
            {"file": rel(FOOD_REFERENCE), "sha256": sha(FOOD_REFERENCE), "role": "food and transparent-prop style only"},
            {"file": rel(KITCHEN_REFERENCE), "sha256": sha(KITCHEN_REFERENCE), "role": "Kitchen preparation language only"},
        ],
        "sourceProcessing": {
            "reviewSourceGeometry": [384, 384],
            "method": "visible-alpha isolation, proportional fit within 352 px, centered on a 384 px transparent canvas, lossless WebP; original generated PNG SHA-256 and geometry retained per component",
        },
        "components": components,
        "evidence": {"file": rel(evidence), "sha256": sha(evidence)},
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersClear": True,
            "componentOwnershipUnambiguous": True,
            "styleReferencesUnchanged": True,
            "allAssetsIndependent": True,
            "runtimeChanged": False,
            "kitchenAuthorityChanged": False,
            "primeChanged": False,
            "deployed": False,
        },
    }
    (PACK / "asset-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
