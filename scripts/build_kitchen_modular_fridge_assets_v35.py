#!/usr/bin/env python3
"""Build the coordinated V35 fridge states at exact modular-kitchen scale."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-modular-fridge-workbench-2026-10-20-v35/fridge-family-open-base-source.png"
DOOR_SOURCE = ROOT / "art/source/kitchen-modular-fridge-workbench-2026-10-20-v35/fridge-family-door-source.png"
RAW = ROOT / "art/raw/kitchen-modular-fridge-workbench-2026-10-20-v35"
DRAFT = ROOT / "art/drafts/kitchen-modular-fridge-workbench-2026-10-20-v35"

CELL = (144, 90)
BODY = (84, 74)
BODY_AT = (30, 4)

# The coordinated source was generated at one shared scale. These are the two
# carcass top-left registrations in that source; the standard carcass measures
# exactly 551 x 485 source pixels and defines the downsample scale.
STANDARD_ORIGIN = (200, 188)
BROKEN_ORIGIN = (999, 188)
SOURCE_BODY = (566, 493)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def premultiplied_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    image = image.convert("RGBA")
    r, g, b, a = image.split()
    # Resize premultiplied colour so transparent fringe pixels cannot darken the
    # polished native sprite edge.
    channels = []
    for channel in (r, g, b):
        multiplied = Image.new("L", image.size)
        multiplied.putdata([(c * alpha + 127) // 255 for c, alpha in zip(channel.getdata(), a.getdata())])
        channels.append(multiplied.resize(size, Image.Resampling.LANCZOS))
    alpha = a.resize(size, Image.Resampling.LANCZOS)
    out_channels = []
    for channel in channels:
        values = []
        for c, av in zip(channel.getdata(), alpha.getdata()):
            values.append(0 if av == 0 else min(255, (c * 255 + av // 2) // av))
        restored = Image.new("L", size)
        restored.putdata(values)
        out_channels.append(restored)
    return Image.merge("RGBA", (*out_channels, alpha))


def clean_source() -> Image.Image:
    image = Image.open(SOURCE).convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y][3] <= 8:
                pixels[x, y] = (0, 0, 0, 0)
    # Reattach the fallen door at its real lower-right pivot. Image generation
    # supplied the open cavity and the matching door, but could not guarantee a
    # pixel-exact hinge connection. The deterministic composite keeps the door
    # inside the one-bay elevation and puts its bottom-right corner under the
    # copper hinge knuckle. This is still one coordinated source construction.
    door_source = Image.open(DOOR_SOURCE).convert("RGBA")
    polygon = [(1028, 421), (1244, 329), (1372, 585), (1123, 691), (1024, 451)]
    mask = Image.new("L", image.size)
    from PIL import ImageDraw

    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    isolated = Image.new("RGBA", image.size)
    isolated.alpha_composite(door_source)
    isolated.putalpha(Image.composite(isolated.getchannel("A"), Image.new("L", image.size), mask))
    shifted = Image.new("RGBA", image.size)
    shifted.alpha_composite(isolated, (120, 0))
    image.alpha_composite(shifted)

    # Put the lower hinge knuckle in front of the door corner so the attachment
    # reads at native scale. The loose upper hinge remains detached.
    hinge = Image.open(SOURCE).convert("RGBA").crop((1460, 540, 1530, 635))
    image.alpha_composite(hinge, (1460, 540))
    return image


def state_cell(source: Image.Image, origin: tuple[int, int], standard: bool) -> Image.Image:
    sx = SOURCE_BODY[0] / BODY[0]
    sy = SOURCE_BODY[1] / BODY[1]
    left = round(origin[0] - BODY_AT[0] * sx)
    top = round(origin[1] - BODY_AT[1] * sy)
    right = round(left + CELL[0] * sx)
    bottom = round(top + CELL[1] * sy)
    crop = Image.new("RGBA", (right - left, bottom - top))
    source_box = (max(0, left), max(0, top), min(source.width, right), min(source.height, bottom))
    crop.alpha_composite(source.crop(source_box), (source_box[0] - left, source_box[1] - top))
    cell = premultiplied_resize(crop, CELL)

    # The broken door/puddle reaches left into the transparent space separating
    # the two source constructions. Keep the Standard cell wholly isolated.
    if standard:
        for y in range(CELL[1]):
            for x in range(BODY_AT[0] + BODY[0], CELL[0]):
                cell.putpixel((x, y), (0, 0, 0, 0))

    # Deterministic transparent safety gutter on every edge.
    for x in range(CELL[0]):
        cell.putpixel((x, 0), (0, 0, 0, 0))
        cell.putpixel((x, CELL[1] - 1), (0, 0, 0, 0))
    for y in range(CELL[1]):
        cell.putpixel((0, y), (0, 0, 0, 0))
        cell.putpixel((CELL[0] - 1, y), (0, 0, 0, 0))
    return cell


def effect_strip() -> Image.Image:
    old = Image.open(ROOT / "art/raw/kitchen-fridge-states-2026-10-18-v39/fx-fridge-drip-ripple-f40.png").convert("RGBA")
    out = Image.new("RGBA", (CELL[0] * 40, CELL[1]))
    # Retain only the approved effect pixels. Re-register each old 136 x 104
    # frame onto the new y=134 appliance datum; no fridge pixels are present.
    for frame in range(40):
        src = old.crop((frame * 136, 0, (frame + 1) * 136, 104))
        # The V39 effect was eight pixels lower in-room. Shift it upward while
        # preserving its native pixel dimensions and transparent isolation.
        out.alpha_composite(src, (frame * CELL[0] + 4, -8))
        x0 = frame * CELL[0]
        for x in range(x0, x0 + CELL[0]):
            out.putpixel((x, 0), (0, 0, 0, 0))
            out.putpixel((x, CELL[1] - 1), (0, 0, 0, 0))
        for y in range(CELL[1]):
            out.putpixel((x0, y), (0, 0, 0, 0))
            out.putpixel((x0 + CELL[0] - 1, y), (0, 0, 0, 0))
    return out


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    source = clean_source()
    standard = state_cell(source, STANDARD_ORIGIN, True)
    broken = state_cell(source, BROKEN_ORIGIN, False)

    # The worktop belongs to the coordinated family and must be byte-identical
    # between states. Copy only that shared construction band from Standard.
    shared_top = standard.crop((BODY_AT[0], BODY_AT[1], BODY_AT[0] + BODY[0], BODY_AT[1] + 14))
    broken.alpha_composite(shared_top, BODY_AT)

    outputs = {
        "fridge-standard.png": standard,
        "fridge-broken-hinge-failed.png": broken,
        "fx-fridge-drip-ripple-f40.png": effect_strip(),
    }
    for name, image in outputs.items():
        image.save(RAW / name, optimize=True)

    provenance = {
        "schema": "lighthouse-keeper/generated-raster-provenance@1",
        "set": "kitchen-modular-fridge-workbench-v35",
        "source": {
            "file": str(SOURCE.relative_to(ROOT)),
            "sha256": sha256(SOURCE),
            "doorSourceFile": str(DOOR_SOURCE.relative_to(ROOT)),
            "doorSourceSha256": sha256(DOOR_SOURCE),
            "mode": "imagegen coordinated family plus deterministic lower-hinge registration",
            "references": [
                "art/source/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-generated-source.png",
                "art/raw/kitchen-fridge-states-2026-10-18-v39/fridge-broken-hinge-failed.png",
                "art/raw/kitchen-rebuild-states-2026-10-18-v2/fridge-standard.png",
            ],
        },
        "nativeRegistration": {
            "cellPixels": list(CELL),
            "bodyPixels": list(BODY),
            "bodyAt": list(BODY_AT),
            "roomBodyBounds": [0, 134, 84, 208],
        },
        "outputs": {name: sha256(RAW / name) for name in outputs},
    }
    (DRAFT / "generation-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print("Built coordinated V35 fridge states: 84 x 74 body, y=134..208, isolated 144 x 90 cells")


if __name__ == "__main__":
    main()
