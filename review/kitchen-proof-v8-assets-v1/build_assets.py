#!/usr/bin/env python3
"""Build guides and deterministic review outputs for Kitchen v8 Day-1 assets.

This is a candidate/review build.  It does not promote art to runtime, create
future upgrade tiers, assemble a room, or mutate Keeper canon.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GUIDES = HERE / "sources" / "guides"
SELECTED = HERE / "sources" / "selected"
LAYER_SOURCES = HERE / "sources" / "layers"
OUTPUTS = HERE / "outputs"
STATES = OUTPUTS / "states"
ITEMS = HERE / "items"

APPROVED = {
    "belfast_sink_cabinet": ROOT / "review/kitchen-proof-v8-style-test-v2/outputs/belfast_sink_cabinet-1x.png",
    "painted_dresser": ROOT / "review/kitchen-proof-v8-style-test-v2/outputs/painted_dresser-1x.png",
    "old_school_cooker": ROOT / "review/kitchen-proof-v8-style-test-v2/outputs/small_cream_cooker-1x.png",
}

# Delivered canvases.  A standard freestanding kitchen unit is 126 px wide.
# The future range is deliberately absent; Frank deferred it and fixed it at
# exactly two standard-unit widths when that upgrade is authored.
SPECS = {
    "cream_larder_fridge": (126, 180),
    "painted_base_cupboard": (126, 180),
    "scrubbed_pine_table": (252, 147),
    "wooden_chair_side": (84, 151),
    "enamel_pedal_bin": (42, 92),
    "enamel_electric_kettle": (52, 62),
    "cream_toaster": (55, 45),
    "stand_mixer": (68, 82),
    "painted_wall_cupboard": (126, 105),
}

STATUS_BEZELS = {
    "cream_larder_fridge": {"centrePx": [111, 59], "radiusPx": 3},
    "old_school_cooker": {"centrePx": [111, 156], "radiusPx": 3},
    "enamel_electric_kettle": {"centrePx": [46, 50], "radiusPx": 2},
    "cream_toaster": {"centrePx": [37, 35], "radiusPx": 2},
    "stand_mixer": {"centrePx": [56, 60], "radiusPx": 2},
}

LABELS = {
    "cream_larder_fridge": "CREAM LARDER FRIDGE",
    "belfast_sink_cabinet": "BELFAST SINK",
    "painted_base_cupboard": "PAINTED CUPBOARD",
    "old_school_cooker": "OLD-SCHOOL COOKER",
    "scrubbed_pine_table": "PINE TABLE",
    "wooden_chair_side": "WOODEN CHAIR",
    "painted_dresser": "PAINTED DRESSER",
    "enamel_pedal_bin": "PEDAL BIN",
    "enamel_electric_kettle": "KETTLE",
    "cream_toaster": "TOASTER",
    "stand_mixer": "MIXER",
    "painted_wall_cupboard": "WALL CUPBOARD",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Verdana Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Verdana.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def guide_rect(size: tuple[int, int]) -> tuple[int, int, int, int]:
    width, height = size
    available_w, available_h = 824, 1184
    ratio = min(available_w / width, available_h / height)
    rect_w = round(width * ratio)
    rect_h = round(height * ratio)
    x0 = (1024 - rect_w) // 2
    y1 = 1360
    return x0, y1 - rect_h, x0 + rect_w, y1


def build_guides() -> None:
    GUIDES.mkdir(parents=True, exist_ok=True)
    SELECTED.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    STATES.mkdir(parents=True, exist_ok=True)
    ITEMS.mkdir(parents=True, exist_ok=True)
    for name, size in SPECS.items():
        image = Image.new("RGBA", (1024, 1536), (247, 242, 228, 255))
        draw = ImageDraw.Draw(image)
        x0, y0, x1, y1 = guide_rect(size)
        draw.line((92, y1, 932, y1), fill=(76, 83, 83, 255), width=3)
        dash = 14
        for x in range(x0, x1, dash * 2):
            draw.line((x, y0, min(x + dash, x1), y0), fill=(154, 156, 149, 255), width=2)
            draw.line((x, y1, min(x + dash, x1), y1), fill=(154, 156, 149, 255), width=2)
        for y in range(y0, y1, dash * 2):
            draw.line((x0, y, x0, min(y + dash, y1)), fill=(154, 156, 149, 255), width=2)
            draw.line((x1, y, x1, min(y + dash, y1)), fill=(154, 156, 149, 255), width=2)
        draw.text((32, 28), f"{LABELS[name]} · {size[0]} × {size[1]} px", font=font(24, True), fill=(43, 55, 59, 255))
        image.save(GUIDES / f"{name}-guide.png", optimize=True)


def alpha_crop(image: Image.Image) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("generated source has no visible pixels")
    return image.crop(bbox)


def prepare_asset(path: Path, canvas_size: tuple[int, int], gutter: int = 2) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A").point(lambda value: value if value >= 32 else 0)
    image.putalpha(alpha)
    image = alpha_crop(image)
    inner = (canvas_size[0] - gutter * 2, canvas_size[1] - gutter * 2)
    ratio = min(inner[0] / image.width, inner[1] / image.height)
    fitted = image.resize(
        (max(1, round(image.width * ratio)), max(1, round(image.height * ratio))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(fitted, ((canvas.width - fitted.width) // 2, canvas.height - fitted.height - gutter))
    return canvas


def fit_to_box(path: Path, canvas_size: tuple[int, int], box: tuple[int, int, int, int]) -> Image.Image:
    """Fit a generated isolated source to an exact registered game-space box."""
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A").point(lambda value: value if value >= 32 else 0)
    image.putalpha(alpha)
    image = alpha_crop(image)
    x0, y0, x1, y1 = box
    fitted = image.resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(fitted, (x0, y0))
    return canvas


def status_overlay(size: tuple[int, int], centre: list[int], radius: int) -> Image.Image:
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x, y = centre
    draw.ellipse((x - radius - 1, y - radius - 1, x + radius + 1, y + radius + 1), fill=(27, 37, 45, 230))
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(68, 220, 110, 255))
    if radius >= 2:
        draw.point((x - 1, y - 1), fill=(206, 255, 207, 255))
    return overlay


def oven_light_overlay() -> Image.Image:
    overlay = Image.new("RGBA", (126, 252), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle((17, 178, 109, 231), radius=8, fill=(255, 155, 39, 52))
    draw.ellipse((84, 180, 103, 199), fill=(255, 202, 92, 118))
    draw.ellipse((89, 184, 99, 194), fill=(255, 241, 184, 210))
    return overlay


def translucent_cooker_door(door: Image.Image) -> Image.Image:
    """Make the glass panel genuinely translucent while retaining painted reflections."""
    result = door.copy()
    pixels = result.load()
    for y in range(179, 228):
        for x in range(17, 109):
            r, g, b, a = pixels[x, y]
            if a and max(r, g, b) < 190:
                pixels[x, y] = (r, g, b, min(a, 142))
    return result


def build_registered_layers(assets: dict[str, Image.Image]) -> dict[str, Image.Image]:
    required = [
        "fridge_body_open.png", "fridge_door.png", "cooker_body_open.png",
        "cooker_door.png", "cottage_pie_cooking.png", "cottage_pie_burnt.png",
    ]
    for name in required:
        if not (LAYER_SOURCES / name).is_file():
            raise FileNotFoundError(LAYER_SOURCES / name)

    layers: dict[str, Image.Image] = {}
    layers["fridge_body_open"] = fit_to_box(
        LAYER_SOURCES / "fridge_body_open.png", (126, 180), (2, 38, 124, 178)
    )
    layers["fridge_door"] = fit_to_box(
        LAYER_SOURCES / "fridge_door.png", (126, 180), (6, 51, 120, 165)
    )
    layers["cooker_body_open"] = fit_to_box(
        LAYER_SOURCES / "cooker_body_open.png", (126, 252), (2, 48, 124, 250)
    )
    cooker_door = fit_to_box(
        LAYER_SOURCES / "cooker_door.png", (126, 252), (9, 163, 117, 234)
    )
    layers["cooker_door"] = translucent_cooker_door(cooker_door)
    layers["cooker_contents_cooking"] = prepare_asset(
        LAYER_SOURCES / "cottage_pie_cooking.png", (80, 34), gutter=2
    )
    layers["cooker_contents_burnt"] = prepare_asset(
        LAYER_SOURCES / "cottage_pie_burnt.png", (80, 34), gutter=2
    )
    layers["cooker_oven_light_on"] = oven_light_overlay()

    for name, image in layers.items():
        image.save(STATES / f"{name}-1x.png", optimize=True)

    # Closed masters remain the visible authority. These registered composites
    # demonstrate that the new body/door/content layers occupy the same fixed
    # canvas without changing runtime geometry.
    fridge_registered = layers["fridge_body_open"].copy()
    fridge_registered.alpha_composite(layers["fridge_door"])
    fridge_registered.save(STATES / "fridge_closed_registered-1x.png", optimize=True)

    cooker_registered = layers["cooker_body_open"].copy()
    cooker_registered.alpha_composite(layers["cooker_door"])
    cooker_registered.save(STATES / "cooker_closed_registered-1x.png", optimize=True)

    for state in ("cooking", "burnt"):
        open_state = layers["cooker_body_open"].copy()
        open_state.alpha_composite(layers["cooker_oven_light_on"])
        open_state.alpha_composite(layers[f"cooker_contents_{state}"], (23, 193))
        open_state.save(STATES / f"cooker_open_lit_{state}-1x.png", optimize=True)

    for name, bezel in STATUS_BEZELS.items():
        overlay = status_overlay(assets[name].size, bezel["centrePx"], bezel["radiusPx"])
        overlay.save(STATES / f"{name}_status_on-1x.png", optimize=True)

    return layers


def scale(image: Image.Image, factor: float, resample: Image.Resampling) -> Image.Image:
    return image.resize(
        (max(1, round(image.width * factor)), max(1, round(image.height * factor))),
        resample,
    )


def load_assets() -> dict[str, Image.Image]:
    assets: dict[str, Image.Image] = {}
    for name, path in APPROVED.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        destination = OUTPUTS / f"{name}-1x.png"
        shutil.copyfile(path, destination)
        assets[name] = Image.open(destination).convert("RGBA")
    for name, size in SPECS.items():
        source = SELECTED / f"{name}.png"
        if not source.is_file():
            raise FileNotFoundError(f"missing selected source: {source}")
        asset = prepare_asset(source, size)
        asset.save(OUTPUTS / f"{name}-1x.png", optimize=True)
        assets[name] = asset
    chair_mirror = assets["wooden_chair_side"].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    chair_mirror.save(OUTPUTS / "wooden_chair_side_mirrored-1x.png", optimize=True)
    assets["wooden_chair_side_mirrored"] = chair_mirror
    return assets


def paste_centred(sheet: Image.Image, image: Image.Image, centre: int, baseline: int) -> None:
    sheet.alpha_composite(image, (centre - image.width // 2, baseline - image.height))


def build_lineup(assets: dict[str, Image.Image]) -> Path:
    keeper_path = ROOT / "review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png"
    keeper = Image.open(keeper_path).convert("RGBA")
    sheet = Image.new("RGBA", (2300, 1050), (18, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((40, 28), "KITCHEN v8 UK COTTAGE · COMPLETE DAY-1 ASSET LINEUP", font=font(31, True), fill=(250, 238, 207, 255))
    draw.text((40, 72), "Exact 1:1 game canvases · approved family · future range deliberately not drawn", font=font(17), fill=(190, 213, 219, 255))

    baseline = 542
    draw.line((40, baseline, 2260, baseline), fill=(99, 121, 127, 255), width=2)
    first = [
        (155, "cream_larder_fridge"),
        (365, "belfast_sink_cabinet"),
        (565, "painted_base_cupboard"),
        (760, "old_school_cooker"),
        (1020, "scrubbed_pine_table"),
        (1225, "wooden_chair_side"),
        (1425, "painted_dresser"),
        (1605, "painted_wall_cupboard"),
        (1740, "enamel_pedal_bin"),
    ]
    for centre, name in first:
        paste_centred(sheet, assets[name], centre, baseline)
        box = draw.textbbox((0, 0), LABELS[name], font=font(12, True))
        draw.text((centre - (box[2] - box[0]) // 2, baseline + 13), LABELS[name], font=font(12, True), fill=(238, 204, 111, 255))
    sheet.alpha_composite(keeper, (1970, baseline - 316))
    draw.text((1970, baseline + 13), "PRIME KEEPER · EXACT 1:1", font=font(12, True), fill=(238, 204, 111, 255))

    draw.text((40, 620), "COUNTERTOP ELECTRICALS", font=font(22, True), fill=(250, 215, 116, 255))
    draw.text((40, 653), "2× close-up above exact 1:1 · each has one unlit engine-driven status bezel", font=font(15), fill=(190, 213, 219, 255))
    small_names = ["enamel_electric_kettle", "cream_toaster", "stand_mixer"]
    centres = [410, 885, 1360]
    for centre, name in zip(centres, small_names):
        close = scale(assets[name], 2.0, Image.Resampling.LANCZOS)
        paste_centred(sheet, close, centre, 880)
        paste_centred(sheet, assets[name], centre + 145, 880)
        draw.text((centre - 85, 905), f"{LABELS[name]} · 2× + 1:1", font=font(15, True), fill=(238, 204, 111, 255))

    draw.text((40, 1005), "REVIEW ONLY · no room, runtime promotion, upgrade range or Keeper mutation", font=font(14, True), fill=(190, 213, 219, 255))
    path = OUTPUTS / "kitchen-v8-complete-day1-assets-1x.png"
    sheet.convert("RGB").save(path, optimize=True)
    return path


def build_three_scale(assets: dict[str, Image.Image]) -> Path:
    keeper_path = ROOT / "review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png"
    keeper = Image.open(keeper_path).convert("RGBA")
    names = [
        "cream_larder_fridge", "belfast_sink_cabinet", "painted_base_cupboard",
        "old_school_cooker", "scrubbed_pine_table", "wooden_chair_side",
        "painted_dresser", "enamel_pedal_bin", "enamel_electric_kettle",
        "cream_toaster", "stand_mixer", "painted_wall_cupboard",
    ]
    sheet = Image.new("RGBA", (2900, 2360), (18, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((40, 28), "KITCHEN v8 · COMPLETE ASSET THREE-SCALE GATE", font=font(31, True), fill=(250, 238, 207, 255))
    draw.text((40, 72), "2× detail · exact 1:1 room art · exact 12.5% tower reduction", font=font(17), fill=(190, 213, 219, 255))

    groups = [names[:6], names[6:]]
    baselines = [750, 1600]
    title_ys = [190, 840]
    for group_index, (group, baseline) in enumerate(zip(groups, baselines)):
        draw.text((40, title_ys[group_index]), f"2× CLOSE-UP · GROUP {group_index + 1}", font=font(22, True), fill=(250, 215, 116, 255))
        draw.line((40, baseline, 2860, baseline), fill=(99, 121, 127, 255), width=2)
        x = 110
        for name in group:
            image = scale(assets[name], 2.0, Image.Resampling.LANCZOS)
            centre = x + image.width // 2
            paste_centred(sheet, image, centre, baseline)
            draw.text((x, baseline + 12), LABELS[name], font=font(11, True), fill=(238, 204, 111, 255))
            x += image.width + 70
        keeper_2x = scale(keeper, 2.0, Image.Resampling.NEAREST)
        sheet.alpha_composite(keeper_2x, (2340, baseline - 632))

    draw.text((40, 1742), "1:1 ROOM STRIP", font=font(22, True), fill=(250, 215, 116, 255))
    baseline_1x = 2160
    draw.line((40, baseline_1x, 2860, baseline_1x), fill=(99, 121, 127, 255), width=2)
    x = 55
    for name in names:
        image = assets[name]
        paste_centred(sheet, image, x + image.width // 2, baseline_1x)
        x += image.width + 28
    sheet.alpha_composite(keeper, (2460, baseline_1x - 316))

    draw.text((40, 2201), "TOWER ≈1/8", font=font(18, True), fill=(250, 215, 116, 255))
    x = 260
    for name in names:
        image = scale(assets[name], 0.125, Image.Resampling.LANCZOS)
        sheet.alpha_composite(image, (x, 2310 - image.height))
        x += image.width + 34
    keeper_small = scale(keeper, 0.125, Image.Resampling.LANCZOS)
    sheet.alpha_composite(keeper_small, (2350, 2310 - 40))

    path = OUTPUTS / "kitchen-v8-complete-assets-three-scale.png"
    sheet.convert("RGB").save(path, optimize=True)
    return path


def labelled_asset(
    sheet: Image.Image,
    draw: ImageDraw.ImageDraw,
    image: Image.Image,
    x: int,
    baseline: int,
    label: str,
    factor: float,
) -> int:
    enlarged = scale(image, factor, Image.Resampling.NEAREST)
    sheet.alpha_composite(enlarged, (x, baseline - enlarged.height))
    draw.text((x, baseline + 10), label, font=font(13, True), fill=(238, 204, 111, 255))
    return x + enlarged.width


def build_layer_review(assets: dict[str, Image.Image], layers: dict[str, Image.Image]) -> Path:
    sheet = Image.new("RGBA", (2400, 1300), (18, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((40, 28), "KITCHEN v8 · REGISTERED DOORS, INTERIORS AND ENGINE LIGHTS", font=font(31, True), fill=(250, 238, 207, 255))
    draw.text((40, 72), "Candidate technical layers · exact fixed canvases · closed approved masters retained", font=font(17), fill=(190, 213, 219, 255))

    draw.text((40, 138), "FRIDGE · 126 × 180 px", font=font(22, True), fill=(250, 215, 116, 255))
    fridge_registered = Image.open(STATES / "fridge_closed_registered-1x.png").convert("RGBA")
    x = 70
    x = labelled_asset(sheet, draw, assets["cream_larder_fridge"], x, 690, "APPROVED CLOSED MASTER · 3×", 3)
    x += 90
    x = labelled_asset(sheet, draw, layers["fridge_body_open"], x, 690, "COMPLETE FIXED INTERIOR · 3×", 3)
    x += 90
    x = labelled_asset(sheet, draw, layers["fridge_door"], x, 690, "SEPARATE RIGHT-HINGED DOOR · 3×", 3)
    x += 90
    labelled_asset(sheet, draw, fridge_registered, x, 690, "REGISTERED CLOSED CHECK · 3×", 3)

    draw.text((40, 760), "COOKER · 126 × 252 px · FUTURE 252 px RANGE NOT DRAWN", font=font(22, True), fill=(250, 215, 116, 255))
    cooker_registered = Image.open(STATES / "cooker_closed_registered-1x.png").convert("RGBA")
    cooking = Image.open(STATES / "cooker_open_lit_cooking-1x.png").convert("RGBA")
    burnt = Image.open(STATES / "cooker_open_lit_burnt-1x.png").convert("RGBA")
    entries = [
        (assets["old_school_cooker"], "APPROVED CLOSED MASTER"),
        (layers["cooker_body_open"], "COMPLETE FIXED INTERIOR"),
        (layers["cooker_door"], "SEPARATE TRANSLUCENT DOOR"),
        (cooker_registered, "REGISTERED CLOSED CHECK"),
        (cooking, "OPEN + LIGHT + COOKING"),
        (burnt, "OPEN + LIGHT + BURNT"),
    ]
    x = 45
    for image, label in entries:
        labelled_asset(sheet, draw, image, x, 1240, label, 1.75)
        x += 390

    path = OUTPUTS / "kitchen-v8-registered-layers-review.png"
    sheet.convert("RGB").save(path, optimize=True)
    return path


def build_status_review(assets: dict[str, Image.Image]) -> Path:
    sheet = Image.new("RGBA", (1900, 700), (18, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((40, 28), "KITCHEN v8 · ENGINE-DRIVEN STATUS LAMPS", font=font(31, True), fill=(250, 238, 207, 255))
    draw.text((40, 72), "The painted master contains one dark bezel; the green lamp is a separate overlay", font=font(17), fill=(190, 213, 219, 255))
    names = list(STATUS_BEZELS)
    x = 50
    baseline = 590
    for name in names:
        base = assets[name]
        on = base.copy()
        overlay = Image.open(STATES / f"{name}_status_on-1x.png").convert("RGBA")
        on.alpha_composite(overlay)
        factor = min(2.0, 260 / base.height, 270 / base.width)
        off_scaled = scale(base, factor, Image.Resampling.NEAREST)
        on_scaled = scale(on, factor, Image.Resampling.NEAREST)
        sheet.alpha_composite(off_scaled, (x, baseline - off_scaled.height))
        sheet.alpha_composite(on_scaled, (x + off_scaled.width + 18, baseline - on_scaled.height))
        draw.text((x, baseline + 10), f"{LABELS[name]} · OFF / ON", font=font(12, True), fill=(238, 204, 111, 255))
        x += off_scaled.width + on_scaled.width + 85
    path = OUTPUTS / "kitchen-v8-status-lamps-review.png"
    sheet.convert("RGB").save(path, optimize=True)
    return path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_metadata() -> Path:
    item_data = {
        "cream_larder_fridge": {
            "canvasPx": [126, 180], "standardUnitWidths": 1, "quantity": 1,
            "states": {"body": "../../outputs/states/fridge_body_open-1x.png", "door": "../../outputs/states/fridge_door-1x.png"},
            "door": {"hinge": "right", "pivotPx": [120, 108]}, "statusLightPointPx": STATUS_BEZELS["cream_larder_fridge"]["centrePx"],
            "engineDrawsStatusLight": True,
        },
        "belfast_sink_cabinet": {"canvasPx": [168, 211], "quantity": 1, "states": {"master": "../../outputs/belfast_sink_cabinet-1x.png"}},
        "painted_base_cupboard": {"canvasPx": [126, 180], "standardUnitWidths": 1, "quantity": 2, "reuseSameBytes": True, "states": {"master": "../../outputs/painted_base_cupboard-1x.png"}},
        "old_school_cooker": {
            "canvasPx": [126, 252], "standardUnitWidths": 1, "quantity": 1,
            "states": {
                "body": "../../outputs/states/cooker_body_open-1x.png", "door": "../../outputs/states/cooker_door-1x.png",
                "cookingContents": "../../outputs/states/cooker_contents_cooking-1x.png", "burntContents": "../../outputs/states/cooker_contents_burnt-1x.png",
            },
            "door": {"hinge": "bottom", "pivotPx": [63, 234]}, "contentsOffsetPx": [23, 193],
            "lightRectPx": [17, 178, 109, 231], "statusLightPointPx": STATUS_BEZELS["old_school_cooker"]["centrePx"], "controlKnobs": 4,
            "engineDrawsOvenLight": True, "engineDrawsStatusLight": True,
        },
        "scrubbed_pine_table": {"canvasPx": [252, 147], "standardUnitWidths": 2, "quantity": 1, "states": {"master": "../../outputs/scrubbed_pine_table-1x.png"}},
        "wooden_chair_side": {"canvasPx": [84, 151], "quantity": 2, "states": {"right": "../../outputs/wooden_chair_side-1x.png", "left": "../../outputs/wooden_chair_side_mirrored-1x.png"}},
        "painted_dresser": {"canvasPx": [150, 355], "quantity": 1, "states": {"master": "../../outputs/painted_dresser-1x.png"}},
        "enamel_pedal_bin": {"canvasPx": [42, 92], "quantity": 1, "states": {"master": "../../outputs/enamel_pedal_bin-1x.png"}},
        "enamel_electric_kettle": {"canvasPx": [52, 62], "quantity": 1, "states": {"master": "../../outputs/enamel_electric_kettle-1x.png"}, "statusLightPointPx": STATUS_BEZELS["enamel_electric_kettle"]["centrePx"], "engineDrawsStatusLight": True},
        "cream_toaster": {"canvasPx": [55, 45], "quantity": 1, "states": {"master": "../../outputs/cream_toaster-1x.png"}, "statusLightPointPx": STATUS_BEZELS["cream_toaster"]["centrePx"], "engineDrawsStatusLight": True},
        "stand_mixer": {"canvasPx": [68, 82], "quantity": 1, "states": {"master": "../../outputs/stand_mixer-1x.png"}, "statusLightPointPx": STATUS_BEZELS["stand_mixer"]["centrePx"], "engineDrawsStatusLight": True},
        "painted_wall_cupboard": {"canvasPx": [126, 105], "standardUnitWidths": 1, "quantity": 1, "states": {"master": "../../outputs/painted_wall_cupboard-1x.png"}},
    }
    for item_id, data in item_data.items():
        item_dir = ITEMS / item_id
        item_dir.mkdir(parents=True, exist_ok=True)
        payload = {"schema": "lighthouse-keeper/kitchen-item@1", "id": item_id, "status": "review-candidate", "anchor": "bottom-left", **data}
        (item_dir / "item.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    files = {}
    for path in sorted(OUTPUTS.rglob("*.png")):
        relative = path.relative_to(HERE).as_posix()
        files[relative] = {"canvasPx": list(Image.open(path).size), "bytes": path.stat().st_size, "sha256": sha256(path)}
    source_files = {}
    for path in sorted((SELECTED).glob("*.png")) + sorted((LAYER_SOURCES).glob("*.png")):
        relative = path.relative_to(HERE).as_posix()
        source_files[relative] = {"canvasPx": list(Image.open(path).size), "bytes": path.stat().st_size, "sha256": sha256(path)}
    predecessor = ROOT / "review/kitchen-proof-v8-style-test-v2/manifest.json"
    manifest = {
        "schema": "lighthouse-keeper/kitchen-v8-day1-assets@1",
        "status": "review-candidate",
        "runtimeMutation": False,
        "canonMutation": False,
        "roomBuilt": False,
        "standardUnitWidthPx": 126,
        "futureRangeWidthPx": 252,
        "futureRangeDrawn": False,
        "approvedClosedMasterAuthority": "review/kitchen-proof-v8-style-test-v2",
        "predecessorManifestSha256": sha256(predecessor),
        "items": sorted(item_data),
        "sourceFiles": source_files,
        "files": files,
    }
    path = HERE / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalise", action="store_true")
    args = parser.parse_args()
    build_guides()
    print(GUIDES)
    if args.finalise:
        assets = load_assets()
        layers = build_registered_layers(assets)
        print(build_lineup(assets))
        print(build_three_scale(assets))
        print(build_layer_review(assets, layers))
        print(build_status_review(assets))
        print(write_metadata())


if __name__ == "__main__":
    main()
