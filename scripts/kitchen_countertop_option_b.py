#!/usr/bin/env python3
"""Reusable Option B countertop constructor for future kitchen draft assets.

This module is intentionally pure: callers supply a V5-derived RGBA base and
receive a new image. It never writes files or touches runtime assets.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = ROOT / "data/kitchen_countertop_option_b_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
TRANSPARENT = (0, 0, 0, 0)


def _colour(name: str) -> tuple[int, int, int, int]:
    return tuple(RECIPE["paletteRgba"][name])


def _extend_rows_to_rectangle(region: Image.Image, x0: int, x1: int) -> Image.Image:
    out = region.copy()
    px = out.load()
    for y in range(out.height):
        opaque = [x for x in range(x0, x1 + 1) if px[x, y][3] >= 96]
        if not opaque:
            continue
        left, right = min(opaque), max(opaque)
        for x in range(x0, left):
            px[x, y] = px[left, y]
        for x in range(right + 1, x1 + 1):
            px[x, y] = px[right, y]
    return out


def _wood_counter(authority: Image.Image, target_size: tuple[int, int], front_y: int, edge_length_lp: int) -> Image.Image:
    depth = RECIPE["construction"]["topRevealPx"]
    fascia = RECIPE["construction"]["fasciaPx"]
    rear_y = front_y - depth
    width = edge_length_lp * RECIPE["density"]
    x0 = (target_size[0] - width) // 2
    x1 = x0 + width - 1

    # The selected calibration's polished V5-derived worktop is the colour and
    # texture authority. Resize only this shallow slab when a wider table is
    # requested; never resize the receiving asset or its structural front.
    source = Image.new("RGBA", authority.size, TRANSPARENT)
    source.alpha_composite(authority.crop((0, 42, 84, 48)), (0, 42))
    source.alpha_composite(authority.crop((0, 48, 84, 56)), (0, 48))
    slab = source.crop((2, 42, 82, 56)).resize((width, depth + fascia), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", target_size, TRANSPARENT)
    out.alpha_composite(slab, (x0, rear_y))
    out = _extend_rows_to_rectangle(out, x0, x1)
    draw = ImageDraw.Draw(out)
    ink = _colour("ink")
    draw.line((x0, rear_y, x1, rear_y), fill=ink, width=2)
    draw.line((x0, rear_y, x0, front_y + fascia - 1), fill=ink, width=2)
    # Pillow expands a 2-px vertical stroke towards +x. Place the right stroke
    # one pixel inward so the inclusive envelope remains exactly x0..x1.
    draw.line((x1 - 1, rear_y, x1 - 1, front_y + fascia - 1), fill=ink, width=2)
    draw.line((x0, front_y - 1, x1, front_y - 1), fill=ink, width=2)
    draw.line((x0, front_y + fascia - 1, x1, front_y + fascia - 1), fill=ink, width=1)
    return out


def _draw_hob(image: Image.Image, original: Image.Image, front_y: int, edge_length_lp: int) -> None:
    depth = RECIPE["construction"]["topRevealPx"]
    fascia = RECIPE["construction"]["fasciaPx"]
    rear_y = front_y - depth
    width = edge_length_lp * RECIPE["density"]
    x0 = (image.width - width) // 2
    x1 = x0 + width - 1
    draw = ImageDraw.Draw(image)
    draw.rectangle((x0, rear_y, x1, front_y - 1), fill=_colour("hob"))
    draw.line((x0 + 2, rear_y + 1, x1 - 2, rear_y + 1), fill=_colour("hobLight"), width=1)
    cy = rear_y + depth // 2
    for cx in (x0 + 20, x1 - 20):
        draw.ellipse((cx - 8, cy - 2, cx + 8, cy + 2), fill=(29, 31, 42, 255), outline=_colour("ink"), width=1)
        draw.ellipse((cx - 3, cy - 1, cx + 3, cy + 1), fill=(221, 171, 92, 255))
        draw.line((cx - 9, cy - 2, cx + 9, cy + 2), fill=_colour("ink"), width=1)
        draw.line((cx - 9, cy + 2, cx + 9, cy - 2), fill=_colour("ink"), width=1)
    if rear_y > 20:
        draw.rectangle((10, 20, 73, rear_y - 1), fill=(247, 221, 165, 255))
        draw.line((10, 20, 10, rear_y - 1), fill=_colour("ink"), width=2)
        draw.line((73, 20, 73, rear_y - 1), fill=_colour("ink"), width=2)
    image.alpha_composite(original.crop((0, front_y, original.width, front_y + fascia)), (0, front_y))
    draw = ImageDraw.Draw(image)
    draw.line((x0, rear_y, x1, rear_y), fill=_colour("ink"), width=2)
    draw.line((x0, front_y - 1, x1, front_y - 1), fill=_colour("ink"), width=2)
    draw.line((x0, rear_y, x0, front_y + fascia - 1), fill=_colour("ink"), width=2)
    draw.line((x1 - 1, rear_y, x1 - 1, front_y + fascia - 1), fill=_colour("ink"), width=2)
    draw.line((x0, front_y + fascia - 1, x1, front_y + fascia - 1), fill=_colour("ink"), width=1)


def apply_option_b(base: Image.Image, stem: str, wood_authority: Image.Image) -> Image.Image:
    """Return one Option B standard base while preserving pixels off the top mask."""
    spec = RECIPE["compatibleUnits"][stem]
    out = base.convert("RGBA").copy()
    out.paste(TRANSPARENT, tuple(spec["maskPx"]))
    if spec["material"] == "hob":
        _draw_hob(out, base, spec["frontYPx"], spec["edgeLengthLp"])
    else:
        out.alpha_composite(_wood_counter(wood_authority, out.size, spec["frontYPx"], spec["edgeLengthLp"]))
    if spec["preservePx"]:
        box = tuple(spec["preservePx"])
        out.alpha_composite(base.crop(box), (box[0], box[1]))
    return out


def compatible_stems() -> tuple[str, ...]:
    return tuple(RECIPE["compatibleUnits"])
