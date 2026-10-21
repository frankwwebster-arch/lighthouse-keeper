#!/usr/bin/env python3
"""Build the immutable Bubble stories symbol redraw pack."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/activity-story-symbol-redraws-2026-10-21-v1"
SOURCE_DIR = PACK / "source"
COMPONENT_DIR = PACK / "drafts/components"
EVIDENCE_DIR = PACK / "evidence"
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216

SPECS = (
    ("symbol-heat-shimmer", "heat", "symbol-heat-shimmer-source.png"),
    ("symbol-pleasant-aroma", "scent", "symbol-pleasant-aroma-source.png"),
    ("symbol-welding-sparks", "welding", "symbol-welding-sparks-source.png"),
    ("symbol-clean-glint", "clean", "symbol-clean-glint-source.png"),
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.getchannel("A").point(
        lambda value: 255 if value > VISIBLE_ALPHA else 0
    ).getbbox()
    if bounds is None:
        raise RuntimeError("source has no visible pixels")
    return bounds


def edge_alpha_pixels(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = set()
    for x in (0, image.width - 1):
        points.update((x, y) for y in range(image.height))
    for y in (0, image.height - 1):
        points.update((x, y) for x in range(image.width))
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in points)


def gutter(image: Image.Image) -> int:
    x0, y0, x1, y1 = visible_bounds(image)
    return min(x0, y0, image.width - x1, image.height - y1)


def normalise(source: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    bounds = visible_bounds(source)
    isolated = source.crop(bounds)
    scale = min(TARGET / isolated.width, TARGET / isolated.height)
    size = (
        max(1, round(isolated.width * scale)),
        max(1, round(isolated.height * scale)),
    )
    rendered = isolated.resize(size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    offset = ((CELL - size[0]) // 2, (CELL - size[1]) // 2)
    cell.alpha_composite(rendered, offset)
    return cell, {
        "sourceVisibleBounds": list(bounds),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "transparentGutterPx": gutter(cell),
        "edgeAlphaPixels": edge_alpha_pixels(cell),
        "ownership": {
            "ownerCount": 1,
            "ambiguousPixels": 0,
            "unownedVisiblePixels": 0,
        },
    }


def main() -> None:
    COMPONENT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    components: dict[str, dict[str, object]] = {}
    rendered: list[Image.Image] = []

    for component_id, family, filename in SPECS:
        source_path = SOURCE_DIR / filename
        if not source_path.exists():
            raise RuntimeError(f"missing source: {rel(source_path)}")
        source = Image.open(source_path).convert("RGBA")
        if edge_alpha_pixels(source):
            raise RuntimeError(f"visible source edge pixels: {component_id}")
        component, evidence = normalise(source)
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe output geometry: {component_id}")
        output_path = COMPONENT_DIR / f"{component_id}.png"
        component.save(output_path, optimize=True)
        components[component_id] = {
            "family": family,
            "owner": component_id,
            "sourceFile": rel(source_path),
            "sourceSha256": sha256(source_path),
            "sourcePixels": list(source.size),
            "file": rel(output_path),
            "sha256": sha256(output_path),
            "cellPixels": [CELL, CELL],
            **evidence,
        }
        rendered.append(component)

    contact = Image.new("RGBA", (CELL * len(rendered), CELL * 2), (0, 0, 0, 0))
    cream = Image.new("RGBA", (CELL, CELL), (243, 231, 204, 255))
    navy = Image.new("RGBA", (CELL, CELL), (20, 36, 58, 255))
    for column, component in enumerate(rendered):
        light = cream.copy()
        dark = navy.copy()
        light.alpha_composite(component)
        dark.alpha_composite(component)
        contact.alpha_composite(light, (column * CELL, 0))
        contact.alpha_composite(dark, (column * CELL, CELL))
    evidence_path = EVIDENCE_DIR / "symbols-light-dark-contact-sheet.png"
    contact.save(evidence_path, optimize=True)

    register = {
        "schema": "lighthouse-keeper/activity-story-symbol-redraw-register@1",
        "set": "activity-story-symbol-redraws-2026-10-21-v1",
        "status": "immutable-reversible-draft",
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "components": components,
        "evidence": {
            "file": rel(evidence_path),
            "sha256": sha256(evidence_path),
            "layout": [len(rendered), 2],
            "backgrounds": ["warm cream", "deep navy"],
        },
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "storiesChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "rollback": "Remove only this draft pack and the picture-library versions that reference it; all earlier picture versions remain intact.",
    }
    register_path = PACK / "batch-register.json"
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"pack": rel(PACK), "components": components}, indent=2))


if __name__ == "__main__":
    main()
