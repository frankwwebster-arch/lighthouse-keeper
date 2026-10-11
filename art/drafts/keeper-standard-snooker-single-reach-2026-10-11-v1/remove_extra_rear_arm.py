#!/usr/bin/env python3
"""Remove only the small erroneous rear hand/arm protrusion from the V1 reach pose."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "inputs/first-attempt-reach-with-extra-arm.png"
OUTPUT = HERE / "generated/single-reach-pose-v4-complete-rear-arm-removed.png"
REPORT = HERE / "validation-v4.json"

# The extra rear limb is the narrow sleeve and small orange hand behind the
# character's left side. The polygon follows the complete limb from its rear
# shoulder attachment to the hand. The correct broad lowered foreground arm
# begins to the right of this polygon and the reaching arm is far outside it.
REMOVAL_POLYGON = [
    (128, 265),
    (145, 268),
    (150, 281),
    (146, 304),
    (143, 332),
    (144, 361),
    (149, 386),
    (155, 408),
    (153, 427),
    (140, 443),
    (111, 443),
    (91, 430),
    (85, 409),
    (89, 381),
    (97, 352),
    (106, 321),
    (117, 291),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def opaque_bounds(image: Image.Image) -> list[int]:
    return list(image.getchannel("A").getbbox() or (0, 0, 0, 0))


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    corrected = source.copy()
    mask = Image.new("L", source.size, 0)
    ImageDraw.Draw(mask).polygon(REMOVAL_POLYGON, fill=255)

    source_pixels = source.load()
    corrected_pixels = corrected.load()
    mask_pixels = mask.load()
    changed = 0
    removed_opaque = 0
    for y in range(source.height):
        for x in range(source.width):
            if not mask_pixels[x, y]:
                continue
            if source_pixels[x, y][3]:
                removed_opaque += 1
            if corrected_pixels[x, y] != (0, 0, 0, 0):
                changed += 1
            corrected_pixels[x, y] = (0, 0, 0, 0)

    corrected.save(OUTPUT, "PNG", optimize=False, compress_level=9)
    rerun = source.copy()
    rerun_pixels = rerun.load()
    for y in range(source.height):
        for x in range(source.width):
            if mask_pixels[x, y]:
                rerun_pixels[x, y] = (0, 0, 0, 0)
    deterministic = corrected.tobytes() == rerun.tobytes()

    report = {
        "status": "draft-only-awaiting-frank-review",
        "operation": "clear the complete erroneous rear arm from shoulder/sleeve through hand",
        "source": {"path": str(SOURCE.relative_to(HERE)), "sha256": sha256(SOURCE)},
        "removalPolygon": REMOVAL_POLYGON,
        "changedPixelsInsideMask": changed,
        "removedOpaquePixels": removed_opaque,
        "unchangedOutsideMask": True,
        "sourceOpaqueBounds": opaque_bounds(source),
        "outputOpaqueBounds": opaque_bounds(corrected),
        "deterministicRerun": deterministic,
        "output": {"path": str(OUTPUT.relative_to(HERE)), "sha256": sha256(OUTPUT)},
        "scopeGate": {
            "headChanged": False,
            "beardChanged": False,
            "reachingArmChanged": False,
            "loweredForegroundArmChanged": False,
            "normalized": False,
            "registered": False,
            "promoted": False,
        },
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
