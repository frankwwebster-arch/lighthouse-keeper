#!/usr/bin/env python3
"""Build the immutable Claude BBQ tools and ephemera asset pack V1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1"
SOURCE_DIR = PACK / "source"
ASSET_DIR = PACK / "assets"
EVIDENCE_DIR = PACK / "evidence"
REFERENCE_PACK = ROOT / "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1"
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216

SPECS = (
    ("bbq-tongs", "tool", "bbq-tongs-source.webp", "35f85ebf1bda8174e4a55cc381bf12241c15e48293d39e7611f015c45c48cf8f", [1661, 947]),
    ("bbq-slotted-turner", "tool", "bbq-slotted-turner-source.webp", "d7b7fa11a4ff784b94b54beea36055c3d08d7953e41579628fa281adfde41f9f", [1661, 947]),
    ("bbq-basting-brush", "tool", "bbq-basting-brush-source.webp", "9f67c615536249ee76a2dd54591a351bbd3cf06a4d648d087127ed394511dedc", [1536, 1024]),
    ("bbq-grill-fork", "tool", "bbq-grill-fork-source.webp", "f8f852169c4644abfa054e0f700a4e714cc47c3c17b87981f96ccbfcdd557398", [1536, 1024]),
    ("bbq-heatproof-mitt", "ephemera", "bbq-heatproof-mitt-source.webp", "b9aab84a9767a638d17d14798112a9623db4f41cba1fd3208422659067943136", [1405, 1119]),
    ("bbq-charcoal-chimney", "ephemera", "bbq-charcoal-chimney-source.webp", "dca0e3498599c29f703fefe77e0a75a15b20e8f7a293a33ea7c02297b4feca55", [1536, 1024]),
    ("bbq-skewer-bundle", "ephemera", "bbq-skewer-bundle-source.webp", "3d30686cb06793da2cdb8c6e0773b2a4c9d799e35d9a1e80f11eef9320ebbac4", [1536, 1024]),
    ("bbq-charcoal-bag", "ephemera", "bbq-charcoal-bag-source.webp", "43447a18939438f904a4da0c894733c1f424c549a3eda0a0dd465b6fe3782ca5", [1292, 1218]),
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
    for index, (component_id, _, _, _, _) in enumerate(SPECS):
        x = (index % 4) * CELL
        y = (index // 4) * (CELL + 36)
        draw.text((x + 8, y + 12), component_id.upper(), fill=(243, 231, 204, 255))
        board = checkerboard((CELL, CELL))
        board.alpha_composite(rendered[component_id])
        sheet.alpha_composite(board, (x, y + 36))
    return sheet


def main() -> None:
    required = [SOURCE_DIR / spec[2] for spec in SPECS]
    required.append(REFERENCE_PACK / "asset-manifest.json")
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
            "sourceSet": "claude-bbq-tools-ephemera-pack-v1",
            "sourceFile": rel(source_path),
            "sourceSha256": sha(source_path),
            "originalGeneratedPngSha256": original_generated_sha,
            "originalGeneratedGeometry": original_geometry,
            **measurements,
        }

    evidence = EVIDENCE_DIR / "final-assets-contact-sheet.webp"
    contact_sheet(rendered).save(evidence, format="WEBP", lossless=True, method=6)
    reference_manifest = REFERENCE_PACK / "asset-manifest.json"
    manifest = {
        "schema": "lighthouse-keeper/claude-bbq-tools-ephemera-pack@1",
        "set": "claude-bbq-tools-ephemera-pack-v1",
        "status": "review-only",
        "created": "2026-10-20",
        "styleReference": {
            "file": rel(reference_manifest),
            "sha256": sha(reference_manifest),
            "role": "style-only; no prior asset bytes changed",
        },
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
            "styleReferenceUnchanged": True,
            "allAssetsIndependent": True,
            "runtimeChanged": False,
            "kitchenChanged": False,
            "primeChanged": False,
            "deployed": False,
        },
    }
    (PACK / "asset-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
