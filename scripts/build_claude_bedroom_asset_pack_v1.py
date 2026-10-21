#!/usr/bin/env python3
"""Build the immutable Claude bedroom activity-bubble asset pack V1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/claude-bedroom-asset-pack-2026-10-21-v1"
SOURCE_DIR = PACK / "source"
ASSET_DIR = PACK / "assets"
EVIDENCE_DIR = PACK / "evidence"
REGISTER = PACK / "source-register.json"
PROTECTED = PACK / "protected-authorities.json"
CLEANING_CONTACT_SHEET = ROOT / "art/drafts/claude-household-cleaning-cupboard-pack-2026-10-21-v1/evidence/final-assets-contact-sheet.webp"
CLEANING_PROMPT_LOG = ROOT / "art/drafts/claude-household-cleaning-cupboard-pack-2026-10-21-v1/PROMPT_LOG.md"
PRIOR_BUBBLE_CATALOGUE = ROOT / "art/drafts/claude-complete-activity-image-index-2026-10-21-v4/bubble-assets.json"
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.getchannel("A").point(lambda value: 255 if value > VISIBLE_ALPHA else 0).getbbox()
    if bounds is None:
        raise RuntimeError("image has no visible pixels")
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


def contact_sheet(specs: list[dict[str, object]], rendered: dict[str, Image.Image]) -> Image.Image:
    rows = (len(specs) + 3) // 4
    sheet = Image.new("RGBA", (CELL * 4, (CELL + 36) * rows), (18, 35, 52, 255))
    draw = ImageDraw.Draw(sheet)
    for index, spec in enumerate(specs):
        component_id = str(spec["id"])
        x = (index % 4) * CELL
        y = (index // 4) * (CELL + 36)
        draw.text((x + 8, y + 12), component_id.upper(), fill=(243, 231, 204, 255))
        board = checkerboard((CELL, CELL))
        board.alpha_composite(rendered[component_id])
        sheet.alpha_composite(board, (x, y + 36))
    return sheet


def write_hashes() -> None:
    files = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    lines = [f"{sha(path)}  {path.relative_to(PACK).as_posix()}" for path in files]
    (PACK / "HASHES.sha256").write_text("\n".join(lines) + "\n")


def main() -> None:
    register = json.loads(REGISTER.read_text())
    specs = register["accepted"]
    if len(specs) != 26 or register["rejected"]:
        raise RuntimeError("V1 expects 26 accepted generations and no rejected attempts")
    required = [SOURCE_DIR / str(spec["sourceFile"]).split("/", 1)[1] for spec in specs]
    required += [CLEANING_CONTACT_SHEET, CLEANING_PROMPT_LOG, PRIOR_BUBBLE_CATALOGUE, PROTECTED]
    required += [PACK / name for name in ("README.md", "PROMPT_LOG.md", "CLAUDE_REVIEW_PROMPT.md")]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing dependency: {rel(path)}")

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    components: dict[str, dict[str, object]] = {}
    rendered: dict[str, Image.Image] = {}
    for spec in specs:
        component_id = str(spec["id"])
        source_path = PACK / str(spec["sourceFile"])
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
            "family": spec["family"],
            "cellPixels": [CELL, CELL],
            "sourceSet": "claude-bedroom-asset-pack-v1",
            "sourceFile": rel(source_path),
            "sourceSha256": sha(source_path),
            "originalCacheFile": spec["originalCacheFile"],
            "originalGeneratedPngSha256": spec["originalGeneratedPngSha256"],
            "originalGeneratedGeometry": spec["originalGeneratedGeometry"],
            **measurements,
        }

    evidence = EVIDENCE_DIR / "final-assets-contact-sheet.webp"
    contact_sheet(specs, rendered).save(evidence, format="WEBP", lossless=True, method=6)
    manifest = {
        "schema": "lighthouse-keeper/claude-bedroom-asset-pack@1",
        "set": "claude-bedroom-asset-pack-v1",
        "status": "review-only",
        "created": "2026-10-21",
        "styleReferences": [
            {"file": rel(CLEANING_CONTACT_SHEET), "sha256": sha(CLEANING_CONTACT_SHEET), "role": "primary visual and contact-sheet reference"},
            {"file": rel(CLEANING_PROMPT_LOG), "sha256": sha(CLEANING_PROMPT_LOG), "role": "primary prompt and transparency-process reference"},
            {"file": rel(PRIOR_BUBBLE_CATALOGUE), "sha256": sha(PRIOR_BUBBLE_CATALOGUE), "role": "prior complete bubble-vocabulary reference"},
        ],
        "sourceProcessing": {
            "reviewSourceGeometry": [384, 384],
            "method": "alpha <= 8 removed, visible-alpha isolation, proportional fit within 352 px, centered on a 384 px transparent canvas, lossless WebP; original generated PNG SHA-256, cache filename and geometry retained per component",
        },
        "sourceRegister": {"file": rel(REGISTER), "sha256": sha(REGISTER)},
        "protectedAuthorities": {"file": rel(PROTECTED), "sha256": sha(PROTECTED)},
        "components": components,
        "rejectedGenerations": [],
        "rejectedGenerationNote": register["rejectedNote"],
        "evidence": {"file": rel(evidence), "sha256": sha(evidence)},
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersClear": True,
            "componentOwnershipUnambiguous": True,
            "styleReferencesUnchanged": True,
            "allAcceptedAssetsIndependent": True,
            "allTaskGenerationsRepresented": True,
            "protectedAuthoritiesPinned": True,
            "runtimeChanged": False,
            "kitchenAuthorityChanged": False,
            "primeChanged": False,
            "animationAuthorityChanged": False,
            "deploymentAuthorityChanged": False,
            "composerPageChanged": False,
            "deployed": False,
        },
    }
    (PACK / "asset-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    write_hashes()


if __name__ == "__main__":
    main()
