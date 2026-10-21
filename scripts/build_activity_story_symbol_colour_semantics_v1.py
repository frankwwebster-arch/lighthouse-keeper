#!/usr/bin/env python3
"""Build the immutable colour-semantic Bubble stories symbol pack."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/activity-story-symbol-colour-semantics-2026-10-21-v1"
SOURCE_DIR = PACK / "source"
COMPONENT_DIR = PACK / "drafts/components"
EVIDENCE_DIR = PACK / "evidence"
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216

SPECS = (
    {
        "id": "symbol-heat-shimmer",
        "family": "heat",
        "label": "Heat shimmer",
        "source": "symbol-heat-shimmer-source.png",
        "cache": "exec-3bab53d9-c80d-4dfb-99c6-f02028e637c5.png",
        "intent": "new-version-v3",
        "libraryVersion": 3,
        "primaryRequest": "three horizontal air-distortion ripples in coral-red, vermilion, deep orange and warm cream; unmistakably hot without flames or aroma curls",
    },
    {
        "id": "symbol-pleasant-aroma",
        "family": "scent",
        "label": "Pleasant aroma",
        "source": "symbol-pleasant-aroma-source.png",
        "cache": "exec-14de7057-58b0-465d-8968-dd6ac949a750.png",
        "intent": "new-version-v3",
        "libraryVersion": 3,
        "primaryRequest": "three warm-cream and blush-pink aroma curls carrying two small five-petal flowers and one sparkle: classic comic shorthand for a lovely smell",
    },
    {
        "id": "symbol-welding-sparks",
        "family": "welding",
        "label": "Welding sparks",
        "source": "symbol-welding-sparks-source.png",
        "cache": "exec-d1eb181a-0c61-4560-ba1a-7340f680e578.png",
        "intent": "new-version-v3",
        "libraryVersion": 3,
        "primaryRequest": "an electric blue-white welding contact core, a jagged blue arc and one-sided cyan/cobalt needle-spark spray with two or three molten coral droplets",
    },
    {
        "id": "symbol-cold-snowflake",
        "family": "cold",
        "label": "Cold snowflake",
        "source": "symbol-cold-snowflake-source.png",
        "cache": "exec-35ab0501-24be-4adc-adc0-43b64f6ae1ca.png",
        "intent": "new-picture-v1",
        "libraryVersion": 1,
        "primaryRequest": "one hand-painted six-armed frost crystal in pale ice blue, bright cyan and crisp white with storm-blue facets",
    },
)

REJECTED = ({
    "id": "symbol-pleasant-aroma",
    "file": "art/drafts/activity-story-symbol-colour-semantics-2026-10-21-v1/rejected/symbol-pleasant-aroma-teal-coral-source.png",
    "sha256": "d333027c1662456a949f5e9ed8563799f10b3ac3c9b6c6fd3da5ae3eb6e8c222",
    "originalCacheFile": "exec-7689f2b1-ff57-4fb6-8dbe-ac87e1b2da3b.png",
    "reason": "Rejected after Frank's review: two differently coloured ribbons remained abstract and did not communicate a pleasant smell through comic visual grammar.",
},)


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
    points = {(x, 0) for x in range(image.width)} | {
        (x, image.height - 1) for x in range(image.width)
    }
    points |= {(0, y) for y in range(image.height)} | {
        (image.width - 1, y) for y in range(image.height)
    }
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in points)


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
    final_bounds = visible_bounds(cell)
    gutter = min(
        final_bounds[0],
        final_bounds[1],
        CELL - final_bounds[2],
        CELL - final_bounds[3],
    )
    return cell, {
        "sourceVisibleBounds": list(bounds),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "transparentGutterPx": gutter,
        "edgeAlphaPixels": edge_alpha_pixels(cell),
        "ownership": {
            "ownerCount": 1,
            "ambiguousPixels": 0,
            "unownedVisiblePixels": 0,
        },
    }


def contact_sheet(rendered: list[tuple[str, Image.Image]]) -> Image.Image:
    contact = Image.new("RGBA", (CELL * len(rendered), CELL * 2 + 32), (20, 36, 58, 255))
    cream = Image.new("RGBA", (CELL, CELL), (243, 231, 204, 255))
    navy = Image.new("RGBA", (CELL, CELL), (20, 36, 58, 255))
    draw = ImageDraw.Draw(contact)
    for column, (component_id, component) in enumerate(rendered):
        draw.text((column * CELL + 8, 10), component_id.upper(), fill=(243, 231, 204, 255))
        light = cream.copy()
        dark = navy.copy()
        light.alpha_composite(component)
        dark.alpha_composite(component)
        contact.alpha_composite(light, (column * CELL, 32))
        contact.alpha_composite(dark, (column * CELL, CELL + 32))
    return contact


def write_hashes() -> None:
    files = sorted(
        path for path in PACK.rglob("*")
        if path.is_file() and path.name != "HASHES.sha256"
    )
    (PACK / "HASHES.sha256").write_text(
        "\n".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}" for path in files) + "\n"
    )


def main() -> None:
    COMPONENT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    components: dict[str, dict[str, object]] = {}
    rendered: list[tuple[str, Image.Image]] = []

    for spec in SPECS:
        source_path = SOURCE_DIR / spec["source"]
        if not source_path.exists():
            raise RuntimeError(f"missing source: {rel(source_path)}")
        source = Image.open(source_path).convert("RGBA")
        source_edges = edge_alpha_pixels(source)
        if source_edges:
            raise RuntimeError(f"visible source edge pixels: {spec['id']}")
        component, evidence = normalise(source)
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe output geometry: {spec['id']}")
        output_path = COMPONENT_DIR / f"{spec['id']}.png"
        component.save(output_path, optimize=True)
        components[spec["id"]] = {
            "family": spec["family"],
            "label": spec["label"],
            "owner": spec["id"],
            "intent": spec["intent"],
            "libraryVersion": spec["libraryVersion"],
            "sourceFile": rel(source_path),
            "sourceSha256": sha256(source_path),
            "sourcePixels": list(source.size),
            "originalCacheFile": spec["cache"],
            "primaryRequest": spec["primaryRequest"],
            "file": rel(output_path),
            "sha256": sha256(output_path),
            "cellPixels": [CELL, CELL],
            **evidence,
        }
        rendered.append((spec["id"], component))

    evidence_path = EVIDENCE_DIR / "symbols-light-dark-contact-sheet.png"
    contact_sheet(rendered).save(evidence_path, optimize=True)
    register = {
        "schema": "lighthouse-keeper/activity-story-symbol-colour-register@1",
        "set": "activity-story-symbol-colour-semantics-2026-10-21-v1",
        "status": "registered-current-versions",
        "created": "2026-10-21",
        "tool": "built-in image generation",
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "components": components,
        "rejected": list(REJECTED),
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
            "priorPictureVersionsChanged": False,
            "priorDraftPackChanged": False,
            "storiesChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "libraryVersionsAdded": True,
            "deployed": False,
        },
        "rollback": "Switch each existing mark back to V2 and remove the new cold picture; the prior V1/V2 assets remain byte-identical and independently addressable. The rejected aroma candidate is evidence only and is never registered.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes()
    print("Built 4 colour-semantic Bubble-story marks")


if __name__ == "__main__":
    main()
