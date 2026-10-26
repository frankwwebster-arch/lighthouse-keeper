#!/usr/bin/env python3
"""Build the reversible Lighthouse Keeper pixel-style comparison V3.

Concepts A and B retain their generated island/lamp-room source pixels, then
enforce the shared tower module, chroma key, Keeper scale and palette in code.
Concept C is deliberately a code-only conversion of the rejected legacy Day 1
reference; its structural mismatches are recorded rather than silently fixed.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "public" / "art" / "concepts" / "pixel"
REVIEW_ASSETS = (
    ROOT
    / "public"
    / "keeper-review"
    / "lighthouse-pixel-style-v3"
    / "assets"
)
SOURCE_DIR = ROOT / "art" / "drafts" / "lighthouse-pixel-style-test-2026-10-26-v2" / "sources"

SOURCE_A = SOURCE_DIR / "concept-a-16bit-generated-source-v2.png"
SOURCE_B = SOURCE_DIR / "concept-b-8bit-generated-source-v2.png"
SOURCE_C = ROOT / "public" / "art" / "reference" / "day1.png"
KEEPER_SOURCE = (
    ROOT
    / "review-archive"
    / "objects"
    / "a1"
    / "a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3.png"
)

# The user-facing package remains under public/art/concepts/pixel, but large
# review PNGs first land in keeper-review so the standard archive maintenance
# can content-address them and remove them from the deployment payload.
NATIVE_A = REVIEW_ASSETS / "concept-a-16bit-native-v3.png"
VIEW_A = REVIEW_ASSETS / "concept-a-16bit-view-x3-v3.png"
NATIVE_B = REVIEW_ASSETS / "concept-b-8bit-native-v3.png"
VIEW_B = REVIEW_ASSETS / "concept-b-8bit-view-x6-v3.png"
NATIVE_C = REVIEW_ASSETS / "concept-c-code-only-legacy-control-native-v3.png"
VIEW_C = REVIEW_ASSETS / "concept-c-code-only-legacy-control-view-x3-v3.png"
COMPARISON = REVIEW_ASSETS / "comparison-a-b-c-v3.png"
MANIFEST = PACKAGE / "manifest-v3.json"

MAGENTA = (255, 0, 255)
NAVY = (24, 31, 45)
CREAM = (246, 226, 174)
SAGE = (132, 160, 115)
SAGE_DARK = (91, 126, 83)
LILAC = (178, 150, 195)
WOOD = (155, 91, 39)
WOOD_LIGHT = (197, 129, 58)
WOOD_DARK = (87, 50, 30)
RED = (184, 36, 39)
RED_LIGHT = (224, 58, 43)
STONE_LIGHT = (226, 218, 181)
STONE_MID = (160, 155, 132)
GRASS = (105, 157, 73)
GRASS_DARK = (56, 103, 58)
SOIL = (91, 55, 39)
ROCK = (75, 81, 103)
ROCK_LIGHT = (132, 132, 128)

# Generated A/B share the same 2103 x 748 composition. These measured seams
# isolate left outdoors, the tower module and right outdoors, while the y seams
# isolate lamp room, three equal room floors and cliff.
SOURCE_X = (0, 794, 1120, 2103)
SOURCE_Y = (0, 196, 312, 425, 541, 748)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_magenta(image: Image.Image) -> Image.Image:
    """Convert the generated/reference chroma family to one exact key colour."""

    if "A" in image.getbands():
        rgba = image.convert("RGBA")
        backdrop = Image.new("RGBA", rgba.size, (*MAGENTA, 255))
        backdrop.alpha_composite(rgba)
        image = backdrop.convert("RGB")
    else:
        image = image.convert("RGB")

    array = np.asarray(image).copy()
    red = array[:, :, 0].astype(np.int16)
    green = array[:, :, 1].astype(np.int16)
    blue = array[:, :, 2].astype(np.int16)
    key = (
        (red >= 215)
        & (blue >= 215)
        & (green <= 100)
        & ((red - green) >= 120)
        & ((blue - green) >= 120)
    )
    array[key] = MAGENTA
    return Image.fromarray(array, "RGB")


def warp_generated(source_path: Path, scale: int) -> Image.Image:
    """Piecewise-nearest warp into the exact shared A/B module geometry."""

    source = normalize_magenta(Image.open(source_path))
    if source.size != (2103, 748):
        raise ValueError(f"Unexpected generated source size for {source_path}: {source.size}")

    width = 1152 * scale
    height = 540 * scale
    target_x = tuple(value * scale for value in (0, 480, 672, 1152))
    target_y = tuple(value * scale for value in (18, 136, 200, 264, 324, 496))

    horizontal = Image.new("RGB", (width, source.height), MAGENTA)
    for index in range(len(SOURCE_X) - 1):
        source_left = SOURCE_X[index]
        source_right = SOURCE_X[index + 1]
        target_left = target_x[index]
        target_right = target_x[index + 1]
        strip = source.crop((source_left, 0, source_right, source.height))
        strip = strip.resize((target_right - target_left, source.height), Image.Resampling.NEAREST)
        horizontal.paste(strip, (target_left, 0))

    result = Image.new("RGB", (width, height), MAGENTA)
    for index in range(len(SOURCE_Y) - 1):
        source_top = SOURCE_Y[index]
        source_bottom = SOURCE_Y[index + 1]
        target_top = target_y[index]
        target_bottom = target_y[index + 1]
        strip = horizontal.crop((0, source_top, width, source_bottom))
        strip = strip.resize((width, target_bottom - target_top), Image.Resampling.NEAREST)
        result.paste(strip, (0, target_top))

    # The user-selected direction has a broader, more convincing gallery and
    # lantern crown. Enlarge only the lamp segment; room geometry stays fixed.
    lamp = source.crop((780, 0, 1128, 196)).resize(
        (280 * scale, 118 * scale), Image.Resampling.NEAREST
    )
    lamp_left = 436 * scale
    lamp_top = 18 * scale
    clear = Image.new("RGB", (320 * scale, 118 * scale), MAGENTA)
    result.paste(clear, (416 * scale, lamp_top))
    result.paste(lamp, (lamp_left, lamp_top))

    return normalize_magenta(result)


def draw_flat_island(image: Image.Image, scale: int) -> dict[str, Any]:
    """Replace generated ground with one strict orthographic side elevation."""

    draw = ImageDraw.Draw(image)
    width, height = image.size
    ground_y = 324 * scale
    waterline_y = 430 * scale

    # Remove every inherited lawn, paving, cliff, jetty and boat pixel first.
    # This prevents a generated top face or diagonal terrace from surviving.
    draw.rectangle((0, 288 * scale, width - 1, height - 1), fill=MAGENTA)

    def points(values: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return [(x * scale, y * scale) for x, y in values]

    # The complete rock mass is a front-facing panel. Its upper boundary stays
    # level until the far-right side-on stair descent; no ground plane is seen.
    cliff_profile = points(
        [
            (16, 324),
            (1008, 324),
            (1020, 332),
            (1032, 348),
            (1044, 364),
            (1056, 380),
            (1068, 396),
            (1080, 412),
            (1092, 430),
            (1092, 464),
            (1032, 496),
            (64, 496),
            (46, 476),
            (32, 448),
            (20, 402),
            (16, 360),
        ]
    )
    draw.polygon(cliff_profile, fill=ROCK, outline=NAVY)

    # Large flat rock cells. B uses exactly one lighter rock step; A adds only
    # sparse single-pixel highlights, never gradients or a receding top plane.
    cell_height = 34
    cell_width = 52
    for row_index, y in enumerate(range(332, 478, cell_height)):
        offset = -26 if row_index % 2 else 0
        for x in range(offset + 16, 1012, cell_width):
            left = max(17, x + 2)
            right = min(1007, x + cell_width - 3)
            top = y + 2
            bottom = min(493, y + cell_height - 3)
            if right <= left:
                continue
            polygon = points(
                [
                    (left + 5, top),
                    (right - 7, top + 1),
                    (right, top + 10),
                    (right - 4, bottom - 3),
                    (left + 8, bottom),
                    (left, bottom - 8),
                ]
            )
            fill = ROCK_LIGHT if (row_index + (x // cell_width)) % 3 == 0 else ROCK
            draw.polygon(polygon, fill=fill, outline=NAVY)
            if scale == 2:
                draw.line(
                    points([(left + 8, top + 5), (right - 10, top + 5)]),
                    fill=STONE_MID,
                    width=1,
                )

    # Exactly measured outdoor plots. Each is a flat edge band whose top is
    # the same ground line as the kitchen floor; there are no visible top faces.
    bed_bounds = (48 * scale, ground_y - 16 * scale, 240 * scale, ground_y)
    lawn_bounds = (240 * scale, ground_y, 432 * scale, ground_y + 8 * scale)
    terrace_bounds = (720 * scale, ground_y, 912 * scale, ground_y + 8 * scale)

    # Raised bed: one module wide, seen edge-on. Soil is only a narrow line;
    # the stone rectangle below it is its front face rather than a top plane.
    draw.rectangle(
        (48 * scale, ground_y - 16 * scale, 240 * scale - 1, ground_y - 1),
        fill=STONE_MID,
        outline=NAVY,
    )
    draw.rectangle(
        (51 * scale, ground_y - 15 * scale, 237 * scale - 1, ground_y - 12 * scale),
        fill=SOIL,
    )
    for x in range(60, 240, 24):
        draw.line(
            (x * scale, ground_y - 11 * scale, x * scale, ground_y - scale),
            fill=STONE_LIGHT,
            width=1,
        )

    # Lawn and rough grass are shallow front-edge bands on the same line.
    draw.rectangle(
        (240 * scale, ground_y, 432 * scale - 1, ground_y + 7 * scale),
        fill=GRASS_DARK,
    )
    draw.line(
        (240 * scale, ground_y, 432 * scale - 1, ground_y),
        fill=GRASS,
        width=scale,
    )
    draw.rectangle(
        (16 * scale, ground_y, 48 * scale - 1, ground_y + 7 * scale),
        fill=GRASS_DARK,
    )
    draw.line(
        (16 * scale, ground_y, 48 * scale - 1, ground_y),
        fill=GRASS,
        width=scale,
    )
    draw.rectangle(
        (912 * scale, ground_y, 1008 * scale - 1, ground_y + 7 * scale),
        fill=GRASS_DARK,
    )
    draw.line(
        (912 * scale, ground_y, 1008 * scale - 1, ground_y),
        fill=GRASS,
        width=scale,
    )
    for x in list(range(20, 48, 7)) + list(range(918, 1008, 7)):
        height_px = 4 + (x % 3)
        draw.line(
            (x * scale, ground_y, (x + 1) * scale, (324 - height_px) * scale),
            fill=GRASS_DARK,
            width=scale,
        )

    # Terrace: one module wide. Only its vertical front edge is visible; the
    # joints are vertical ticks, never a perspective grid.
    draw.rectangle(
        (720 * scale, ground_y, 912 * scale - 1, ground_y + 7 * scale),
        fill=STONE_MID,
    )
    draw.line(
        (720 * scale, ground_y, 912 * scale - 1, ground_y),
        fill=STONE_LIGHT,
        width=scale,
    )
    for x in range(744, 912, 24):
        draw.line(
            (x * scale, ground_y + scale, x * scale, ground_y + 7 * scale),
            fill=NAVY,
            width=1,
        )

    # A side-profile stone stair follows the cliff silhouette to the water.
    for index in range(7):
        x = 1008 + index * 12
        y = 324 + index * 16
        draw.line(
            points([(x, y), (x + 18, y)]),
            fill=STONE_LIGHT,
            width=scale,
        )
        draw.line(
            points([(x + 18, y), (x + 18, y + 16)]),
            fill=NAVY,
            width=scale,
        )

    # Side-on jetty and the one permitted outdoor object: the Keeper's boat.
    jetty_y = 422 * scale
    draw.rectangle(
        (1068 * scale, jetty_y, 1122 * scale - 1, jetty_y + 5 * scale),
        fill=WOOD,
        outline=NAVY,
    )
    for post_x in (1074, 1098, 1118):
        draw.rectangle(
            (post_x * scale, jetty_y, (post_x + 3) * scale - 1, 454 * scale),
            fill=WOOD_DARK,
        )
    boat = points([(1092, 435), (1136, 435), (1130, 447), (1116, 450), (1098, 445)])
    draw.polygon(boat, fill=STONE_LIGHT, outline=NAVY)
    draw.line(points([(1100, 441), (1129, 441)]), fill=RED, width=scale)
    draw.rectangle(
        (1088 * scale, 431 * scale, 1094 * scale - 1, 441 * scale),
        fill=WOOD_DARK,
        outline=NAVY,
    )

    return {
        "canvasSize": [width, height],
        "groundLineY": ground_y,
        "waterlineY": waterline_y,
        "visibleTopFaces": False,
        "presentation": "single orthographic side-profile panel",
        "bedBounds": list(bed_bounds),
        "lawnBounds": list(lawn_bounds),
        "terraceBounds": list(terrace_bounds),
        "roughLeftSpan": [16 * scale, 48 * scale],
        "roughRightSpan": [912 * scale, 1008 * scale],
        "boatHorizontalSpan": [1088 * scale, 1136 * scale],
        "plotWidth": 192 * scale,
        "stairPresentation": "side profile on far-right cliff only",
    }


def draw_window(
    draw: ImageDraw.ImageDraw,
    left: int,
    top: int,
    size: int,
    scale: int,
) -> tuple[int, int, int, int]:
    """Draw an exact 24/48 px framed window and return its glass rectangle."""

    frame = scale
    sill = 3 * scale
    draw.rectangle((left, top, left + size - 1, top + size - 1), fill=NAVY)
    glass = (
        left + frame,
        top + frame,
        left + size - frame - 1,
        top + size - sill - 1,
    )
    draw.rectangle(glass, fill=MAGENTA)
    draw.rectangle(
        (left - scale, top + size - sill, left + size + scale - 1, top + size - 1),
        fill=STONE_LIGHT,
    )
    draw.line(
        (left - scale, top + size - sill, left + size + scale - 1, top + size - sill),
        fill=NAVY,
        width=1,
    )
    return glass


def draw_front_door(
    draw: ImageDraw.ImageDraw,
    left: int,
    floor_surface: int,
    scale: int,
) -> None:
    width = 24 * scale
    height = 40 * scale
    top = floor_surface - height
    draw.rectangle((left, top, left + width - 1, floor_surface - 1), fill=NAVY)
    inset = scale
    draw.rectangle(
        (left + inset, top + inset, left + width - inset - 1, floor_surface - 1),
        fill=WOOD,
    )
    panel_inset = 4 * scale
    draw.rectangle(
        (
            left + panel_inset,
            top + 5 * scale,
            left + width - panel_inset - 1,
            floor_surface - 6 * scale,
        ),
        outline=WOOD_LIGHT,
        width=scale,
    )
    draw.rectangle(
        (
            left + width - 5 * scale,
            top + 21 * scale,
            left + width - 4 * scale,
            top + 22 * scale,
        ),
        fill=STONE_LIGHT,
    )


def draw_room_modules(image: Image.Image, scale: int) -> dict[str, Any]:
    """Replace the generated room stack with exact flat orthographic modules."""

    draw = ImageDraw.Draw(image)
    tower_x = 480 * scale
    module_width = 192 * scale
    module_height = 64 * scale
    wall = 4 * scale
    band = 4 * scale
    walk_zone = 28 * scale
    bay = 12 * scale
    window_size = 24 * scale
    floor_tops = [136 * scale, 200 * scale, 264 * scale]
    colours = [LILAC, SAGE, CREAM]
    glass_rects: list[list[tuple[int, int, int, int]]] = []

    # Classic lighthouse shell: fixed rectangular rooms sit inside a subtly
    # tapering striped exterior. The solid margin is the concealed circulation
    # pocket; no stair/landing/shaft pixels are exposed to the player.
    body_top = floor_tops[0]
    body_bottom = floor_tops[-1] + module_height
    outer_top_left = 456 * scale
    outer_top_right = 696 * scale
    outer_bottom_left = 432 * scale
    outer_bottom_right = 720 * scale
    stripe_height = 16 * scale

    def edge_at(top_value: int, bottom_value: int, y: int) -> int:
        progress = (y - body_top) / (body_bottom - body_top)
        return round(top_value + (bottom_value - top_value) * progress)

    stripe_index = 0
    for stripe_top in range(body_top, body_bottom, stripe_height):
        stripe_bottom = min(body_bottom, stripe_top + stripe_height)
        left_top = edge_at(outer_top_left, outer_bottom_left, stripe_top)
        left_bottom = edge_at(outer_top_left, outer_bottom_left, stripe_bottom)
        right_top = edge_at(outer_top_right, outer_bottom_right, stripe_top)
        right_bottom = edge_at(outer_top_right, outer_bottom_right, stripe_bottom)
        stripe_colour = RED if stripe_index % 2 == 0 else STONE_LIGHT
        draw.polygon(
            [
                (left_top, stripe_top),
                (right_top, stripe_top),
                (right_bottom, stripe_bottom - 1),
                (left_bottom, stripe_bottom - 1),
            ],
            fill=stripe_colour,
        )
        if scale == 2 and stripe_colour == RED:
            highlight_y = min(stripe_bottom - 2, stripe_top + 2)
            draw.line(
                (left_top + 2, highlight_y, right_top - 2, highlight_y),
                fill=RED_LIGHT,
                width=1,
            )
        stripe_index += 1

    draw.line(
        (outer_top_left, body_top, outer_bottom_left, body_bottom),
        fill=NAVY,
        width=1,
    )
    draw.line(
        (outer_top_right - 1, body_top, outer_bottom_right - 1, body_bottom),
        fill=NAVY,
        width=1,
    )

    # A weathered stone plinth grounds the tapered tower into the cliff.
    foundation_bottom = 360 * scale
    draw.polygon(
        [
            (outer_bottom_left, body_bottom),
            (outer_bottom_right, body_bottom),
            (728 * scale, foundation_bottom),
            (424 * scale, foundation_bottom),
        ],
        fill=ROCK,
        outline=NAVY,
    )
    block_height = 8 * scale
    for course_index, y in enumerate(
        range(body_bottom, foundation_bottom, block_height)
    ):
        course_bottom = min(foundation_bottom, y + block_height)
        progress_top = (y - body_bottom) / (foundation_bottom - body_bottom)
        progress_bottom = (course_bottom - body_bottom) / (
            foundation_bottom - body_bottom
        )
        left_top = round(outer_bottom_left + (424 * scale - outer_bottom_left) * progress_top)
        right_top = round(outer_bottom_right + (728 * scale - outer_bottom_right) * progress_top)
        left_bottom = round(outer_bottom_left + (424 * scale - outer_bottom_left) * progress_bottom)
        right_bottom = round(outer_bottom_right + (728 * scale - outer_bottom_right) * progress_bottom)
        draw.line((left_top, y, right_top, y), fill=STONE_LIGHT, width=1)
        joint_offset = 12 * scale if course_index % 2 else 0
        for x in range(440 * scale + joint_offset, 720 * scale, 24 * scale):
            if left_bottom < x < right_bottom:
                draw.line((x, y + 1, x, course_bottom - 1), fill=NAVY, width=1)

    for floor_index, (top, wall_colour) in enumerate(zip(floor_tops, colours)):
        bottom = top + module_height
        floor_surface = bottom - band

        # One flat outer rectangle, exact straight wall/floor bands, no depth.
        draw.rectangle(
            (tower_x, top, tower_x + module_width - 1, bottom - 1), fill=NAVY
        )
        draw.rectangle(
            (
                tower_x + wall,
                top + band,
                tower_x + module_width - wall - 1,
                floor_surface - 1,
            ),
            fill=wall_colour,
        )
        draw.rectangle(
            (tower_x + 1, top + 1, tower_x + wall - 1, bottom - 2),
            fill=STONE_LIGHT,
        )
        draw.rectangle(
            (
                tower_x + module_width - wall,
                top + 1,
                tower_x + module_width - 2,
                bottom - 2,
            ),
            fill=STONE_LIGHT,
        )
        draw.rectangle(
            (tower_x + wall, top, tower_x + module_width - wall - 1, top + band - 1),
            fill=RED,
        )
        draw.line(
            (tower_x + wall, top, tower_x + module_width - wall - 1, top),
            fill=NAVY,
            width=1,
        )
        draw.rectangle(
            (
                tower_x + wall,
                floor_surface,
                tower_x + module_width - wall - 1,
                bottom - 1,
            ),
            fill=WOOD,
        )
        draw.line(
            (
                tower_x + wall,
                floor_surface,
                tower_x + module_width - wall - 1,
                floor_surface,
            ),
            fill=WOOD_LIGHT,
            width=scale,
        )
        draw.line(
            (tower_x + wall, bottom - 1, tower_x + module_width - wall - 1, bottom - 1),
            fill=RED,
            width=1,
        )

        # Stone quoin blocks remain flat, but carry discrete material steps.
        block = 8 * scale
        for block_top in range(top + scale, bottom - scale, block):
            colour = STONE_LIGHT if ((block_top - top) // block) % 2 == 0 else STONE_MID
            draw.rectangle(
                (tower_x + scale, block_top, tower_x + wall - 1, min(block_top + block - scale - 1, bottom - 2)),
                fill=colour,
            )
            draw.rectangle(
                (
                    tower_x + module_width - wall,
                    block_top,
                    tower_x + module_width - scale - 1,
                    min(block_top + block - scale - 1, bottom - 2),
                ),
                fill=colour,
            )

        if floor_index == 1:
            panelling_top = floor_surface - 16 * scale
            draw.rectangle(
                (
                    tower_x + wall,
                    panelling_top,
                    tower_x + module_width - wall - 1,
                    floor_surface - 1,
                ),
                fill=SAGE_DARK,
            )
            draw.line(
                (tower_x + wall, panelling_top, tower_x + module_width - wall - 1, panelling_top),
                fill=NAVY,
                width=1,
            )
            for offset in range(tower_x + wall + 6 * scale, tower_x + module_width - wall, 6 * scale):
                draw.line((offset, panelling_top + scale, offset, floor_surface - 1), fill=SAGE, width=1)

        bay_start = tower_x + wall + walk_zone
        first_window = bay_start + 3 * bay
        second_window = bay_start + 9 * bay
        sill_y = floor_surface - 20 * scale
        window_top = sill_y - window_size
        floor_glass = [
            draw_window(draw, first_window, window_top, window_size, scale),
            draw_window(draw, second_window, window_top, window_size, scale),
        ]
        glass_rects.append(floor_glass)

        # Concealed circulation: closed panel is edge-on, so only the jamb is visible.
        jamb_x = tower_x + wall + scale
        draw.rectangle(
            (jamb_x, top + 20 * scale, jamb_x + 2 * scale - 1, floor_surface - 1),
            fill=WOOD_DARK,
        )
        draw.line(
            (jamb_x + scale, top + 20 * scale, jamb_x + scale, floor_surface - 1),
            fill=WOOD_LIGHT,
            width=1,
        )

        # Ground floor additionally has the exterior front door.
        if floor_index == 2:
            draw_front_door(draw, tower_x + 108 * scale, floor_surface, scale)

        # Bedroom alone has a right-hand en-suite partition and edge-on jamb.
        if floor_index == 0:
            partition_x = tower_x + 168 * scale
            draw.rectangle(
                (
                    partition_x,
                    top + band,
                    partition_x + wall - 1,
                    top + 28 * scale - 1,
                ),
                fill=STONE_LIGHT,
            )
            draw.line(
                (partition_x, top + band, partition_x, top + 28 * scale - 1),
                fill=NAVY,
                width=1,
            )
            draw.rectangle(
                (
                    partition_x,
                    top + 28 * scale,
                    partition_x + 2 * scale - 1,
                    floor_surface - 1,
                ),
                fill=WOOD_DARK,
            )

        # 16-bit only: tiny discrete masonry highlights, never gradients.
        if scale == 2:
            for px, py in (
                (tower_x + 47, top + 25),
                (tower_x + 188, top + 52),
                (tower_x + 307, top + 18),
            ):
                if px < tower_x + module_width - wall and py < floor_surface:
                    draw.point((px, py), fill=STONE_LIGHT)

    return {
        "towerBounds": [tower_x, floor_tops[0], tower_x + module_width, floor_tops[-1] + module_height],
        "module": [module_width, module_height],
        "wallBand": wall,
        "floorCeilingBand": band,
        "walkInZone": [tower_x + wall, tower_x + wall + walk_zone],
        "bayWidth": bay,
        "windowOuterSize": [window_size, window_size],
        "windowGlassRects": [[list(rect) for rect in floor] for floor in glass_rects],
        "floorTops": floor_tops,
        "groundLineY": floor_tops[-1] + module_height - band,
        "outerShell": {
            "topBounds": [outer_top_left, outer_top_right],
            "baseBounds": [outer_bottom_left, outer_bottom_right],
            "bodyY": [body_top, body_bottom],
            "stripeHeight": stripe_height,
            "taperPerSide": outer_top_left - outer_bottom_left,
        },
        "hiddenCirculationPocket": {
            "visible": False,
            "leftShellToRoomGapAtTop": tower_x - outer_top_left,
            "leftShellToRoomGapAtBase": tower_x - outer_bottom_left,
            "entrancePresentation": "slim edge-on jamb only",
        },
    }


def prepare_keeper(height: int) -> Image.Image:
    source = Image.open(KEEPER_SOURCE).convert("RGBA")
    alpha = source.getchannel("A")
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError("Approved Keeper source has no visible pixels")
    source = source.crop(bounds)
    hard_alpha = source.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
    source.putalpha(hard_alpha)
    width = max(1, round(source.width * height / source.height))
    keeper = source.resize((width, height), Image.Resampling.NEAREST)
    keeper.putalpha(keeper.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
    if keeper.getchannel("A").getbbox() is None:
        raise ValueError("Keeper disappeared during conversion")
    return keeper


def place_keeper(
    image: Image.Image,
    height: int,
    zone: tuple[int, int],
    floor_y: int,
) -> tuple[Image.Image, dict[str, Any]]:
    keeper = prepare_keeper(height)
    left = zone[0] + (zone[1] - zone[0] - keeper.width) // 2
    top = floor_y - keeper.height
    result = image.convert("RGBA")
    result.alpha_composite(keeper, (left, top))
    return result.convert("RGB"), {
        "bbox": [left, top, left + keeper.width, top + keeper.height],
        "visibleHeight": keeper.height,
        "source": str(KEEPER_SOURCE.relative_to(ROOT)),
        "sourceSha256": sha256(KEEPER_SOURCE),
        "hardAlphaBeforeComposite": True,
    }


def quantize_with_reserved_magenta(image: Image.Image, colour_limit: int) -> Image.Image:
    """Quantize non-key pixels only, reserving exact magenta as one colour."""

    array = np.asarray(normalize_magenta(image)).copy()
    key = np.all(array == np.asarray(MAGENTA, dtype=np.uint8), axis=2)
    non_key = array[~key]
    if len(non_key) == 0:
        raise ValueError("Concept contains no non-magenta pixels")

    row_width = 1024
    row_count = math.ceil(len(non_key) / row_width)
    padded = np.empty((row_count * row_width, 3), dtype=np.uint8)
    padded[: len(non_key)] = non_key
    padded[len(non_key) :] = non_key[0]
    palette_source = Image.fromarray(padded.reshape((row_count, row_width, 3)), "RGB")
    quantized = palette_source.quantize(
        colors=colour_limit - 1,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    ).convert("RGB")
    mapped = np.asarray(quantized).reshape((-1, 3))[: len(non_key)]
    array[~key] = mapped
    array[key] = MAGENTA
    return Image.fromarray(array, "RGB")


def save_png(image: Image.Image, path: Path) -> None:
    image.save(path, format="PNG", optimize=True, compress_level=9)


def palette_count(image: Image.Image) -> int:
    pixels = np.asarray(image.convert("RGB")).reshape((-1, 3))
    return int(np.unique(pixels, axis=0).shape[0])


def magenta_count(image: Image.Image) -> int:
    array = np.asarray(image.convert("RGB"))
    return int(np.all(array == np.asarray(MAGENTA, dtype=np.uint8), axis=2).sum())


def concept_record(
    *,
    concept_id: str,
    source_path: Path,
    native_path: Path,
    view_path: Path,
    native: Image.Image,
    upscale: int,
    colour_limit: int,
    geometry: dict[str, Any] | None,
    keeper: dict[str, Any],
    rule_breaks: list[str],
) -> dict[str, Any]:
    return {
        "id": concept_id,
        "source": str(source_path.relative_to(ROOT)),
        "sourceSha256": sha256(source_path),
        "native": {
            "path": str(native_path.relative_to(ROOT)),
            "sha256": sha256(native_path),
            "size": list(native.size),
            "paletteCount": palette_count(native),
            "paletteLimit": colour_limit,
            "magentaPixels": magenta_count(native),
            "alphaValues": [255],
        },
        "view": {
            "path": str(view_path.relative_to(ROOT)),
            "sha256": sha256(view_path),
            "size": [native.width * upscale, native.height * upscale],
            "integerUpscale": upscale,
            "resampling": "nearest-neighbour",
        },
        "geometry": geometry,
        "keeper": keeper,
        "ruleBreaks": rule_breaks,
    }


def build_generated_concept(
    source_path: Path,
    native_path: Path,
    view_path: Path,
    *,
    scale: int,
    keeper_height: int,
    colour_limit: int,
    upscale: int,
) -> tuple[Image.Image, dict[str, Any], dict[str, Any]]:
    image = warp_generated(source_path, scale)
    outdoors = draw_flat_island(image, scale)
    geometry = draw_room_modules(image, scale)
    geometry["outdoors"] = outdoors
    image, keeper = place_keeper(
        image,
        keeper_height,
        tuple(geometry["walkInZone"]),
        int(geometry["groundLineY"]),
    )
    native = quantize_with_reserved_magenta(image, colour_limit)
    view = native.resize(
        (native.width * upscale, native.height * upscale), Image.Resampling.NEAREST
    )
    save_png(native, native_path)
    save_png(view, view_path)
    return native, geometry, keeper


def build_control() -> tuple[Image.Image, dict[str, Any]]:
    source = normalize_magenta(Image.open(SOURCE_C).convert("RGB"))
    converted = source.resize((1920, 1080), Image.Resampling.NEAREST)
    native = Image.new("RGB", (2304, 1080), MAGENTA)
    native.paste(converted, (192, 0))
    ground_y = round(571 * 1080 / 941)
    native, keeper = place_keeper(native, 62, (982, 1038), ground_y - 1)
    native = quantize_with_reserved_magenta(native, 32)
    view = native.resize((6912, 3240), Image.Resampling.NEAREST)
    save_png(native, NATIVE_C)
    save_png(view, VIEW_C)
    keeper["placementNote"] = "Placed in the legacy ground-floor walk-in area without altering its architecture."
    return native, keeper


def binary_label(text: str, panel_width: int, bar_height: int) -> Image.Image:
    logical_width = panel_width // 4
    logical_height = bar_height // 4
    mask = Image.new("1", (logical_width, logical_height), 0)
    draw = ImageDraw.Draw(mask)
    font = ImageFont.load_default()
    bounds = draw.textbbox((0, 0), text, font=font)
    text_width = bounds[2] - bounds[0]
    text_height = bounds[3] - bounds[1]
    draw.text(
        ((logical_width - text_width) // 2, (logical_height - text_height) // 2),
        text,
        fill=1,
        font=font,
    )
    mask = mask.resize((panel_width, bar_height), Image.Resampling.NEAREST)
    label = Image.new("RGB", (panel_width, bar_height), NAVY)
    ink = Image.new("RGB", (panel_width, bar_height), STONE_LIGHT)
    label.paste(ink, mask=mask)
    return label


def build_comparison(a: Image.Image, b: Image.Image, c: Image.Image) -> Image.Image:
    panel_width = 2304
    panel_height = 1080
    bar_height = 96
    b_display = b.resize((panel_width, panel_height), Image.Resampling.NEAREST)
    panels = [a, b_display, c]
    labels = [
        "A  GENERATED 16-BIT  32 COLOURS",
        "B  GENERATED 8-BIT  16 COLOURS",
        "C  CODE-ONLY LEGACY CONTROL  32 COLOURS",
    ]
    sheet = Image.new("RGB", (panel_width * 3, panel_height + bar_height), NAVY)
    for index, (panel, label) in enumerate(zip(panels, labels)):
        x = index * panel_width
        sheet.paste(binary_label(label, panel_width, bar_height), (x, 0))
        sheet.paste(panel, (x, bar_height))
    save_png(sheet, COMPARISON)
    return sheet


def main() -> None:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    REVIEW_ASSETS.mkdir(parents=True, exist_ok=True)
    for required in (SOURCE_A, SOURCE_B, SOURCE_C, KEEPER_SOURCE):
        if not required.exists():
            raise FileNotFoundError(required)

    native_a, geometry_a, keeper_a = build_generated_concept(
        SOURCE_A,
        NATIVE_A,
        VIEW_A,
        scale=2,
        keeper_height=62,
        colour_limit=32,
        upscale=3,
    )
    native_b, geometry_b, keeper_b = build_generated_concept(
        SOURCE_B,
        NATIVE_B,
        VIEW_B,
        scale=1,
        keeper_height=31,
        colour_limit=16,
        upscale=6,
    )
    native_c, keeper_c = build_control()
    comparison = build_comparison(native_a, native_b, native_c)

    records = [
        concept_record(
            concept_id="A-generated-16-bit",
            source_path=SOURCE_A,
            native_path=NATIVE_A,
            view_path=VIEW_A,
            native=native_a,
            upscale=3,
            colour_limit=32,
            geometry=geometry_a,
            keeper=keeper_a,
            rule_breaks=[],
        ),
        concept_record(
            concept_id="B-generated-8-bit",
            source_path=SOURCE_B,
            native_path=NATIVE_B,
            view_path=VIEW_B,
            native=native_b,
            upscale=6,
            colour_limit=16,
            geometry=geometry_b,
            keeper=keeper_b,
            rule_breaks=[],
        ),
        concept_record(
            concept_id="C-code-only-legacy-control",
            source_path=SOURCE_C,
            native_path=NATIVE_C,
            view_path=VIEW_C,
            native=native_c,
            upscale=3,
            colour_limit=32,
            geometry=None,
            keeper=keeper_c,
            rule_breaks=[
                "The supplied legacy source has two room floors rather than the requested three; the missing living-room floor was not invented in a code-only control.",
                "The supplied legacy source visibly contains stair flights and stair recesses rather than the new concealed circulation slot.",
                "Whole-frame conversion cannot produce the requested exact 384 x 128 room module geometry without redrawing the source.",
            ],
        ),
    ]

    payload = {
        "schemaVersion": 1,
        "status": "review-only; no runtime or canon promotion",
        "builtBy": "scripts/build_lighthouse_pixel_concepts_v3.py",
        "magenta": "#FF00FF",
        "packaging": {
            "entrypoint": "public/art/concepts/pixel/",
            "reviewSet": "lighthouse-pixel-style-v3",
            "reviewAssets": "public/keeper-review/lighthouse-pixel-style-v3/assets/",
            "archivePolicy": "Run npm run maintain:keeper-review after building; PNGs move to content-addressed review-archive objects while their review URLs remain stable.",
            "supersedesReviewSet": "lighthouse-pixel-style-v2",
        },
        "architectureRevision": {
            "reason": "User feedback: restore classic lighthouse identity, then preserve full outdoor widths around the tapered shell.",
            "features": [
                "alternating red and warm-white masonry shell",
                "slight exterior taper around fixed rectangular rooms",
                "wider gallery and lantern crown",
                "concealed stair-sized pocket behind the left room jamb",
                "six-module canvas with full one-module lawn, bed and terrace outside the shell",
                "rough ground and sea breathing room at both image edges",
            ],
        },
        "supersededGeneratedSources": [
            "art/drafts/lighthouse-pixel-style-test-2026-10-26-v2/sources/concept-a-16bit-generated-source-v1.png",
            "art/drafts/lighthouse-pixel-style-test-2026-10-26-v2/sources/concept-b-8bit-generated-source-v1.png",
        ],
        "keeperSourceSubstitution": {
            "requestedPath": "public/art/keeper/canon/ (missing)",
            "usedPath": str(KEEPER_SOURCE.relative_to(ROOT)),
            "reason": "Exact approved 256 x 320 smooth side-right idle authority.",
        },
        "concepts": records,
        "comparison": {
            "path": str(COMPARISON.relative_to(ROOT)),
            "sha256": sha256(COMPARISON),
            "size": list(comparison.size),
            "panelSize": [2304, 1080],
            "labelBarHeight": 96,
            "note": "B is shown at exact x2 beside native A/C so all scenes have the same display size and 8-bit pixels remain visibly twice as large.",
        },
    }
    MANIFEST.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    for record in records:
        native = record["native"]
        print(
            f"{record['id']}: {native['size'][0]}x{native['size'][1]}, "
            f"{native['paletteCount']}/{native['paletteLimit']} colours, "
            f"{native['magentaPixels']} magenta pixels"
        )
    print(f"comparison: {comparison.width}x{comparison.height}")


if __name__ == "__main__":
    main()
