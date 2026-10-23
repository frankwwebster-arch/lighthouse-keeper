#!/usr/bin/env python3
"""Build Kitchen Fixed Shell Layout V9 without a standard-cabinet top strip."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

import build_kitchen_fixed_shell_layout_v6 as v6
import build_kitchen_fixed_shell_layout_v8 as v8


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-fixed-shell-2026-10-23-v9"
PUBLIC_SLUG = "kitchen-fixed-shell-layout-v9"
ATLAS_NAME = "kitchen-fixed-shell-atlas-v9.png"
WORKTOP_LOGICAL_HEIGHT = 10
STANDARD_FRONT_SHIFT = 10
END_PLANE_WIDTH = 34


def fitted_insert(image: Image.Image, body: list[int], name: str) -> Image.Image:
    """Put complete cupboard/drawer top outlines directly below the worktop."""
    if name not in {"cupboard", "drawers"}:
        return v8.fitted_insert(image, body, name)

    bx, by, bw, _ = body
    # The approved source's top-front outline begins at master y+60. Move the
    # complete functional front up to y+50, exactly where the shared worktop
    # ends. This deletes the exposed backing/fascia strip rather than covering
    # or recolouring it. The lower 2 px becomes ordinary plinth reveal.
    shifted = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shifted.alpha_composite(image, (0, -STANDARD_FRONT_SHIFT))
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((bx + 4, by + 50, bx + bw - 4, by + 330), fill=255)
    return v6.alpha_masked(shifted, mask)


def build_fixed_layers(cupboard: Image.Image, body: list[int]) -> tuple[Image.Image, Image.Image, Image.Image]:
    backing, carcass, worktop = v8.build_fixed_layers(cupboard, body)
    width, _ = v6.MASTER_RUN
    ink = (3, 22, 37, 255)
    side = (4, 54, 105, 255)
    side_light = (5, 73, 137, 255)
    draw = ImageDraw.Draw(carcass)

    # Overpaint V8's too-subtle end wedges with readable shallow side planes.
    # Their inner edges taper towards the plinth, giving front/side geometry at
    # 1x while remaining wholly inside the exact 504 px run footprint.
    p = END_PLANE_WIDTH
    draw.polygon([(0, 50), (p, 66), (p - 4, 326), (0, 344)], fill=ink)
    draw.polygon([(5, 60), (p - 7, 71), (p - 10, 321), (5, 334)], fill=side)
    draw.line((8, 65, p - 9, 74), fill=side_light, width=3)
    draw.polygon([(width - 1, 50), (width - 1 - p, 66), (width - p + 3, 326), (width - 1, 344)], fill=ink)
    draw.polygon([(width - 6, 60), (width - p + 6, 71), (width - p + 9, 321), (width - 6, 334)], fill=side)
    draw.line((width - 9, 65, width - p + 8, 74), fill=side_light, width=3)
    return backing, carcass, worktop


def patch_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text())
    manifest["schema"] = "lighthouse-keeper/kitchen-fixed-shell-layout@9"
    manifest["status"] = "unapproved-complete-front-and-perspective-review"
    manifest["architecture"].update({
        "continuousShadedCarcassMaterial": True,
        "flatMonotoneCarcass": False,
        "sampledRailPixelsUsed": False,
        "blueDividerFillUsed": False,
        "standardCabinetTopFasciaUsed": False,
        "sinkSourceCountertopPixelsUsed": False,
        "outerEndPerspectivePlanes": True,
    })
    manifest["corrections"] = {
        "standardCabinetTopStripRemoved": True,
        "completeTopDrawerAndDoorOutlineVisible": True,
        "standardFrontSourceShiftMasterPixels": STANDARD_FRONT_SHIFT,
        "sharedWorktopEndsAboveFronts": True,
        "internalJoinTreatment": "single narrow ink seam; no blue divider or top fascia",
        "sinkSourceCountertopPixelsUsed": False,
        "outerEndPerspectivePlaneMasterWidth": END_PLANE_WIDTH,
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
        "Kitchen Fixed Shell Layout V6": "Kitchen Fixed Shell Layout V9",
        "UNAPPROVED FIXED-SHELL V6": "UNAPPROVED FIXED-SHELL V9",
        "/keeper-review/kitchen-fixed-shell-layout-v6": "/keeper-review/kitchen-fixed-shell-layout-v9",
        "lighthouse-kitchen-fixed-shell-v6": "lighthouse-kitchen-fixed-shell-v9",
        "The approved model renders supply the visible fronts and states. One continuous worktop, one continuous plinth and one fixed six-bay carcass now own every join.":
            "No top fascia exists over standard cabinets: each complete top drawer/door outline begins directly beneath the shared worktop. Wider tapered outer end planes make the fitted depth readable at 1×.",
        "Six 84 px apertures and identical shared dividers.": "Six 84 px apertures with complete fronts and one narrow seam per true boundary.",
        "drawRecord(ctx,w,84,134,504,14)": f"drawRecord(ctx,w,84,134,504,{WORKTOP_LOGICAL_HEIGHT})",
    }
    for old, new in replacements.items():
        if old not in page:
            raise AssertionError(f"V9 page patch target missing: {old}")
        page = page.replace(old, new)
    path.write_text(page)


def main() -> None:
    v6.SET = SET
    v6.OUT = ROOT / "art/drafts" / SET
    v6.PUBLIC = ROOT / "public/keeper-review" / PUBLIC_SLUG
    v6.ATLAS_NAME = ATLAS_NAME
    v6.fitted_insert = fitted_insert
    v6.build_fixed_layers = build_fixed_layers
    v6.sink_overlay = v8.sink_overlay
    v6.main()
    manifest = patch_manifest(v6.OUT / "manifest.json")
    patch_manifest(v6.PUBLIC / "manifest.json")
    patch_page(v6.PUBLIC / "index.html")
    print(json.dumps({"set": SET, "atlas": manifest["atlas"], "corrections": manifest["corrections"]}, indent=2))


if __name__ == "__main__":
    main()
