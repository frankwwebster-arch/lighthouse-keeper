#!/usr/bin/env python3
"""Build Kitchen Fixed Shell Layout V8 with continuous shaded carcass material.

V8 keeps the approved functional art and locked V7 geometry. It removes the
remaining periodic divider surfaces and defines the Belfast overlay by object
geometry, so no sink-source countertop pixel can enter the composite.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

import build_kitchen_fixed_shell_layout_v6 as v6
import build_kitchen_fixed_shell_layout_v7 as v7


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-fixed-shell-2026-10-23-v8"
PUBLIC_SLUG = "kitchen-fixed-shell-layout-v8"
ATLAS_NAME = "kitchen-fixed-shell-atlas-v8.png"
WORKTOP_MASTER_HEIGHT = 50
WORKTOP_LOGICAL_HEIGHT = 10


def fitted_insert(image: Image.Image, body: list[int], name: str) -> Image.Image:
    """Keep functional faces close to the shared seam, excluding shell tops."""
    bx, by, bw, _ = body
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    top = by + (76 if name in {"cupboard", "drawers"} else 54)
    # V7 left 12 logical pixels of synthetic material around every boundary.
    # V8 carries the approved face shading to within less than one logical
    # pixel of each boundary; only the shared ink seam remains visible.
    draw.rectangle((bx + 4, top, bx + bw - 4, by + 340), fill=255)
    if name.startswith("sink"):
        draw.rectangle((bx + 92, 0, bx + 328, by + 112), fill=255)
    if name.endswith("broken"):
        draw.rectangle((0, by + 250, image.width, image.height), fill=255)
    return v6.alpha_masked(image, mask)


def _vertical_material(width: int, height: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    """One continuous cabinet-material field, never repeated per bay."""
    image = Image.new("RGBA", (width, height))
    pixels = image.load()
    for y in range(height):
        t = y / max(1, height - 1)
        colour = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)) + (255,)
        for x in range(width):
            pixels[x, y] = colour
    return image


def build_fixed_layers(_cupboard: Image.Image, _body: list[int]) -> tuple[Image.Image, Image.Image, Image.Image]:
    """Build continuous shaded material, hairline joins and two end planes."""
    width, height = v6.MASTER_RUN
    ink = (3, 22, 37, 255)
    blue_top = (9, 103, 181)
    blue_bottom = (5, 70, 137)
    blue_dark = (4, 58, 112, 255)
    cyan = (18, 185, 194, 255)
    cyan_dark = (7, 143, 171, 255)
    cyan_light = (104, 226, 222, 255)

    backing = _vertical_material(width, height, blue_top, blue_bottom)
    carcass = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(carcass)

    # Internal structure is a single ink seam. There is no blue divider fill,
    # highlight, repeated strip or sampled rail surface.
    seam_width = 4
    for edge in range(v6.MASTER_BODY[0], width, v6.MASTER_BODY[0]):
        draw.rectangle((edge - seam_width // 2, 52, edge + seam_width // 2 - 1, 338), fill=ink)

    # Only exposed run ends receive shallow perspective. These fixed tapered
    # planes remain at the room edges while functional inserts swap within.
    draw.polygon([(0, 50), (18, 60), (18, 334), (0, 342)], fill=ink)
    draw.polygon([(4, 58), (14, 64), (14, 330), (4, 335)], fill=blue_dark)
    draw.polygon([(width - 1, 50), (width - 19, 60), (width - 19, 334), (width - 1, 342)], fill=ink)
    draw.polygon([(width - 5, 58), (width - 15, 64), (width - 15, 330), (width - 5, 335)], fill=blue_dark)

    # One continuous plinth shares the same vertical material rather than a
    # brighter inserted band.
    plinth = _vertical_material(width - 8, 24, (7, 89, 164), (5, 69, 135))
    draw.rectangle((0, 337, width - 1, height - 1), fill=ink)
    carcass.alpha_composite(plinth, (4, 342))
    draw.line((4, 342, width - 5, 342), fill=blue_dark, width=3)

    # Same single fixed worktop as V7. The sink is forbidden from contributing
    # any countertop colour or rear boundary pixels.
    worktop = Image.new("RGBA", (width, WORKTOP_MASTER_HEIGHT), (0, 0, 0, 0))
    top = ImageDraw.Draw(worktop)
    top.polygon(
        [(8, 0), (width - 9, 0), (width - 1, 8), (width - 1, 43),
         (width - 8, 49), (7, 49), (0, 42), (0, 8)], fill=ink,
    )
    top.polygon(
        [(10, 4), (width - 11, 4), (width - 5, 10), (width - 5, 36),
         (width - 10, 41), (9, 41), (5, 36), (5, 10)], fill=cyan,
    )
    top.rectangle((6, 29, width - 7, 40), fill=cyan_dark)
    top.line((13, 8, width - 14, 8), fill=cyan_light, width=4)
    top.line((7, 42, width - 8, 42), fill=ink, width=4)
    return backing, carcass, worktop


def sink_overlay(sink: Image.Image, body: list[int]) -> Image.Image:
    """Extract porcelain, hardware and central water—never source worktop."""
    bx, by, bw, _ = body
    rgb = sink.convert("RGB")
    component = Image.new("L", sink.size, 0)
    comp, pix = component.load(), rgb.load()
    x0, x1 = bx + 48, bx + bw - 48
    centre = bx + bw // 2
    y0, y1 = max(0, by - 190), min(sink.height, by + 116)

    for y in range(y0, y1):
        for x in range(max(0, x0), min(sink.width, x1)):
            r, g, b = pix[x, y]
            cream = r > 145 and g > 115 and b > 72 and not (g > r * 1.18 and b > r * 1.18)
            orange = r > 135 and r > g * 1.16 and b < 115
            # Water above the basin can only be the narrow central stream.
            # Turquoise source-counter pixels cannot satisfy this geometry.
            water = abs(x - centre) <= 30 and b > 145 and b > r * 1.20 and b > g * 1.02
            if cream or orange or water:
                comp[x, y] = 255

    near = component.filter(ImageFilter.MaxFilter(11))
    near_pixels = near.load()
    selected = Image.new("L", sink.size, 0)
    out = selected.load()
    for y in range(y0, y1):
        for x in range(max(0, x0), min(sink.width, x1)):
            r, g, b = pix[x, y]
            dark_outline = max(r, g, b) < 82 and near_pixels[x, y]
            if comp[x, y] or dark_outline:
                out[x, y] = 255

    mask = selected.point(lambda value: 255 if value else 0)
    result = sink.copy()
    result.putalpha(ImageChops.multiply(mask, sink.getchannel("A").point(lambda value: 255 if value else 0)))
    return result


def patch_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text())
    manifest["schema"] = "lighthouse-keeper/kitchen-fixed-shell-layout@8"
    manifest["status"] = "unapproved-material-and-sink-mask-review"
    manifest["architecture"].update({
        "continuousShadedCarcassMaterial": True,
        "flatMonotoneCarcass": False,
        "sampledRailPixelsUsed": False,
        "blueDividerFillUsed": False,
        "sinkSourceCountertopPixelsUsed": False,
        "outerEndPerspectivePlanes": True,
    })
    manifest["corrections"] = {
        "approvedFaceShadingExtendedTowardSeams": True,
        "internalJoinTreatment": "single narrow ink seam; no blue divider surface",
        "sinkMask": "porcelain, hardware and state water only",
        "sinkSourceCountertopPixelsUsed": False,
        "sharedWorktopBehindSink": True,
        "outerEndPerspectivePlanes": True,
        "verticalGridChanged": False,
        "stateBehaviourChanged": False,
    }
    manifest["fixedLayers"]["worktop-run"]["logicalSize"] = [504, WORKTOP_LOGICAL_HEIGHT]
    for state in ("sink", "sink-on", "sink-broken"):
        manifest["overlays"][state]["role"] = "geometry-masked Belfast porcelain/hardware/state-water; zero source countertop pixels"
    payload = json.dumps(manifest, indent=2) + "\n"
    path.write_text(payload)
    return manifest


def patch_page(path: Path) -> None:
    page = path.read_text()
    replacements = {
        "Kitchen Fixed Shell Layout V6": "Kitchen Fixed Shell Layout V8",
        "UNAPPROVED FIXED-SHELL V6": "UNAPPROVED FIXED-SHELL V8",
        "/keeper-review/kitchen-fixed-shell-layout-v6": "/keeper-review/kitchen-fixed-shell-layout-v8",
        "lighthouse-kitchen-fixed-shell-v6": "lighthouse-kitchen-fixed-shell-v8",
        "The approved model renders supply the visible fronts and states. One continuous worktop, one continuous plinth and one fixed six-bay carcass now own every join.":
            "Approved face shading reaches each narrow structural seam. The Belfast layer contains only porcelain, hardware and state water, so one shared worktop supplies its exact colour and alignment.",
        "Six 84 px apertures and identical shared dividers.": "Six 84 px apertures with narrow ink seams and no inserted blue strips.",
        "drawRecord(ctx,w,84,134,504,14)": f"drawRecord(ctx,w,84,134,504,{WORKTOP_LOGICAL_HEIGHT})",
    }
    for old, new in replacements.items():
        if old not in page:
            raise AssertionError(f"V8 page patch target missing: {old}")
        page = page.replace(old, new)
    path.write_text(page)


def main() -> None:
    v6.SET = SET
    v6.OUT = ROOT / "art/drafts" / SET
    v6.PUBLIC = ROOT / "public/keeper-review" / PUBLIC_SLUG
    v6.ATLAS_NAME = ATLAS_NAME
    v6.fitted_insert = fitted_insert
    v6.build_fixed_layers = build_fixed_layers
    v6.sink_overlay = sink_overlay
    v6.main()
    manifest = patch_manifest(v6.OUT / "manifest.json")
    patch_manifest(v6.PUBLIC / "manifest.json")
    patch_page(v6.PUBLIC / "index.html")
    print(json.dumps({"set": SET, "atlas": manifest["atlas"], "corrections": manifest["corrections"]}, indent=2))


if __name__ == "__main__":
    main()
