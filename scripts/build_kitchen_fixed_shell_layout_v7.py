#!/usr/bin/env python3
"""Build the corrected Kitchen Fixed Shell Layout V7 review.

V7 preserves every approved functional insert and the exact room grid from V6,
but replaces sampled cabinet-edge pixels with a deterministic fitted skeleton.
The Belfast sink is an opaque cut-in above the continuous worktop.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

import build_kitchen_fixed_shell_layout_v6 as v6


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-fixed-shell-2026-10-23-v7"
PUBLIC_SLUG = "kitchen-fixed-shell-layout-v7"
WORKTOP_MASTER_HEIGHT = 50
WORKTOP_LOGICAL_HEIGHT = 10


def fitted_insert(image: Image.Image, body: list[int], name: str) -> Image.Image:
    """Retain fronts and effects, excluding every source shell/top remnant."""
    bx, by, bw, _ = body
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    # Standard cabinetry contained a curved highlight immediately below its
    # source worktop. Appliances begin slightly higher to preserve their flat
    # fascia tops; the corrected fixed worktop ends above both apertures.
    top = by + (76 if name in {"cupboard", "drawers"} else 54)
    draw.rectangle((bx + 30, top, bx + bw - 30, by + 340), fill=255)
    if name.startswith("sink"):
        draw.rectangle((bx + 92, 0, bx + 328, by + 112), fill=255)
    if name.endswith("broken"):
        draw.rectangle((0, by + 250, image.width, image.height), fill=255)
    return v6.alpha_masked(image, mask)


def build_fixed_layers(_cupboard: Image.Image, _body: list[int]) -> tuple[Image.Image, Image.Image, Image.Image]:
    """Draw one clean worktop and one flat fitted carcass without sampled rails."""
    width, height = v6.MASTER_RUN
    ink = (3, 22, 37, 255)
    blue = (7, 87, 161, 255)
    blue_dark = (5, 70, 135, 255)
    cyan = (18, 185, 194, 255)
    cyan_dark = (7, 143, 171, 255)
    cyan_light = (104, 226, 222, 255)

    backing = Image.new("RGBA", (width, height), blue)
    carcass = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(carcass)

    # Flat end posts and shared dividers. There are no bevel/highlight samples,
    # so adjacent bays cannot produce pale blue seams or curved shadows.
    post_width = 20
    for edge in range(0, width + 1, v6.MASTER_BODY[0]):
        left = max(0, min(width - post_width, edge - post_width // 2))
        draw.rectangle((left, 50, left + post_width - 1, 338), fill=ink)
        draw.rectangle((left + 4, 54, left + post_width - 5, 337), fill=blue_dark)

    # One continuous plinth, using the same flat blue as the skeleton.
    draw.rectangle((0, 337, width - 1, height - 1), fill=ink)
    draw.rectangle((4, 342, width - 5, height - 5), fill=blue)
    draw.rectangle((4, 346, width - 5, 351), fill=blue_dark)

    # A single shallow counter. It has only outer end geometry and ends before
    # appliance fascias begin, removing the old blue masking strip.
    worktop = Image.new("RGBA", (width, WORKTOP_MASTER_HEIGHT), (0, 0, 0, 0))
    top = ImageDraw.Draw(worktop)
    top.polygon(
        [(8, 0), (width - 9, 0), (width - 1, 8), (width - 1, 43),
         (width - 8, 49), (7, 49), (0, 42), (0, 8)],
        fill=ink,
    )
    top.polygon(
        [(10, 4), (width - 11, 4), (width - 5, 10), (width - 5, 36),
         (width - 10, 41), (9, 41), (5, 36), (5, 10)],
        fill=cyan,
    )
    top.rectangle((6, 29, width - 7, 40), fill=cyan_dark)
    top.line((13, 8, width - 14, 8), fill=cyan_light, width=4)
    top.line((7, 42, width - 8, 42), fill=ink, width=4)
    return backing, carcass, worktop


def sink_overlay(sink: Image.Image, body: list[int]) -> Image.Image:
    """Make the Belfast sink an opaque cut-in through the worktop front."""
    bx, by, bw, _ = body
    rgb = sink.convert("RGB")
    seed = Image.new("L", sink.size, 0)
    out, pix = seed.load(), rgb.load()
    x0, x1 = bx + 58, bx + bw - 58
    for y in range(max(0, by - 180), min(sink.height, by + 112)):
        for x in range(max(0, x0), min(sink.width, x1)):
            r, g, b = pix[x, y]
            cream = r > 145 and g > 115 and b > 72 and not (g > r * 1.18 and b > r * 1.18)
            orange = r > 135 and r > g * 1.16 and b < 115
            water = b > 135 and b > r * 1.18 and b > g * 1.03
            outline = max(r, g, b) < 82
            if cream or orange or water or outline:
                out[x, y] = 255
    expanded = seed.filter(ImageFilter.MaxFilter(5))
    # Binary alpha is intentional: the sink must cover, not blend with, the
    # fixed worktop where the Belfast cutout exists.
    mask = expanded.point(lambda value: 255 if value >= 1 else 0)
    result = sink.copy()
    result.putalpha(ImageChops.multiply(mask, sink.getchannel("A").point(lambda value: 255 if value else 0)))
    return result


def patch_page(path: Path) -> None:
    page = path.read_text()
    replacements = {
        "Kitchen Fixed Shell Layout V6": "Kitchen Fixed Shell Layout V7",
        "UNAPPROVED FIXED-SHELL V6": "UNAPPROVED FIXED-SHELL V7",
        "/keeper-review/kitchen-fixed-shell-layout-v6": "/keeper-review/kitchen-fixed-shell-layout-v7",
        "lighthouse-kitchen-fixed-shell-v6": "lighthouse-kitchen-fixed-shell-v7",
        "The approved model renders supply the visible fronts and states. One continuous worktop, one continuous plinth and one fixed six-bay carcass now own every join.":
            "The approved fronts and states sit inside a flat fitted skeleton. A shallow continuous worktop no longer masks their tops, and the Belfast sink overpaints its real cutout.",
        "Six 84 px apertures and identical shared dividers.": "Six 84 px apertures with flat, monotone shared dividers.",
        "drawRecord(ctx,w,84,134,504,14)": f"drawRecord(ctx,w,84,134,504,{WORKTOP_LOGICAL_HEIGHT})",
    }
    for old, new in replacements.items():
        if old not in page:
            raise AssertionError(f"V7 page patch target missing: {old}")
        page = page.replace(old, new)
    path.write_text(page)


def patch_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text())
    manifest["schema"] = "lighthouse-keeper/kitchen-fixed-shell-layout@7"
    manifest["status"] = "unapproved-fixed-shell-correction-review"
    manifest["architecture"].update({
        "flatMonotoneCarcass": True,
        "sampledRailPixelsUsed": False,
        "opaqueBelfastSink": True,
        "sourceWorktopUndersideUsed": False,
    })
    manifest["corrections"] = {
        "worktopMasterHeightPixels": WORKTOP_MASTER_HEIGHT,
        "worktopLogicalHeight": WORKTOP_LOGICAL_HEIGHT,
        "applianceTopMaskingStripRemoved": True,
        "opaqueBelfastSink": True,
        "flatMonotoneSkeleton": True,
        "sampledRailPixelsUsed": False,
        "outerRunArtifactsRemoved": True,
        "gridOrStateBehaviourChanged": False,
    }
    manifest["fixedLayers"]["worktop-run"]["logicalSize"] = [504, WORKTOP_LOGICAL_HEIGHT]
    for state in ("sink", "sink-on", "sink-broken"):
        manifest["overlays"][state]["role"] = "opaque Belfast sink cut-in above fixed worktop"
    payload = json.dumps(manifest, indent=2) + "\n"
    path.write_text(payload)
    return manifest


def main() -> None:
    v6.SET = SET
    v6.OUT = ROOT / "art/drafts" / SET
    v6.PUBLIC = ROOT / "public/keeper-review" / PUBLIC_SLUG
    v6.ATLAS_NAME = "kitchen-fixed-shell-atlas-v7.png"
    v6.fitted_insert = fitted_insert
    v6.build_fixed_layers = build_fixed_layers
    v6.sink_overlay = sink_overlay
    v6.main()

    draft_manifest = patch_manifest(v6.OUT / "manifest.json")
    patch_manifest(v6.PUBLIC / "manifest.json")
    patch_page(v6.PUBLIC / "index.html")
    print(json.dumps({"set": SET, "atlas": draft_manifest["atlas"], "corrections": draft_manifest["corrections"]}, indent=2))


if __name__ == "__main__":
    main()
