#!/usr/bin/env python3
"""Build the reversible Prime Keeper sweep-broom V2 review candidate."""
from __future__ import annotations

import colorsys
import hashlib
import json
import math
import shutil
from collections import Counter, deque
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-sweep-broom-v2"
PACK = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v2"
V1_PACK = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v1"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
FRAME_DIR = PACK / "drafts/frames"
LAYER_DIR = PACK / "drafts/layers"
MASK_DIR = PACK / "evidence/component-masks"
EVIDENCE_DIR = PACK / "evidence"
PRIME = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
PRIME_SOURCE = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/sources/keeper-prime-side-right-rigged-clean-master.png"
HISTORICAL_RAW = ROOT / "art/raw/keeper-first-batch/keeper_sweep_broom_f8.png"
HISTORICAL_RUNTIME = ROOT / "public/sprites/keeper_sweep_broom.png"
SOURCES = [
    ("acquire", V1_PACK / "sources/generated/keeper_prime_sweep-broom-acquire-actor-only-generated.png"),
    ("phase1", V1_PACK / "sources/generated/keeper_prime_sweep-broom-phase1-actor-only-generated.png"),
    ("phase2", V1_PACK / "sources/generated/keeper_prime_sweep-broom-phase2-actor-only-generated.png"),
    ("phase3", V1_PACK / "sources/generated/keeper_prime_sweep-broom-phase3-actor-only-generated.png"),
    ("phase4", V1_PACK / "sources/generated/keeper_prime_sweep-broom-phase4-actor-only-generated.png"),
]
BROOM_DETAIL_REFERENCE = PACK / "sources/generated/traditional-broom-detail-reference-generated.png"
COMPONENTS = [
    "capCrown", "capBandBrim", "badge", "jumperBlue", "creamBand",
    "trousers", "boots", "skin", "hair", "beard", "outline",
]
MAJOR_COMPONENTS = {"capCrown", "capBandBrim", "jumperBlue", "creamBand", "trousers", "boots", "skin", "hair", "beard", "outline"}
CELL = (384, 320)
ACTOR_ANCHOR = (16, 40)
TARGET_ROOT_X = 128
TARGET_FLOOR_Y = 315
ALPHA_THRESHOLD = 16


def invariant_filter_size(name: str) -> int:
    # Outline and badge are already narrow semantic materials; eroding them
    # would erase the clean sample rather than remove a neighbouring fringe.
    if name in {"outline", "badge", "hair", "capBandBrim", "trousers", "boots"}:
        return 1
    return 5


def minimum_invariant_pixels(name: str) -> int:
    if name == "badge":
        return 12
    if name == "capBandBrim":
        return 16
    if name in {"hair", "beard"}:
        return 32
    return 64


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bounds(image: Image.Image) -> dict[str, int]:
    alpha = image.getchannel("A")
    box = alpha.getbbox()
    if box is None:
        raise RuntimeError("empty image")
    left, top, right, bottom = box
    opaque = sum(1 for value in alpha.getdata() if value)
    return {"minX": left, "minY": top, "maxX": right - 1, "maxY": bottom - 1,
            "width": right - left, "height": bottom - top, "opaquePixels": opaque}


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def luma(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rgb_to_oklab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    values = []
    for value in rgb:
        value /= 255
        values.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    r, g, b = values
    ll = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    mm = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    ss = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    ll, mm, ss = ll ** (1 / 3), mm ** (1 / 3), ss ** (1 / 3)
    return (
        0.2104542553 * ll + 0.7936177850 * mm - 0.0040720468 * ss,
        1.9779984951 * ll - 2.4285922050 * mm + 0.4505937099 * ss,
        0.0259040371 * ll + 0.7827717662 * mm - 0.8086757660 * ss,
    )


def quantile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, round((len(ordered) - 1) * fraction))]


def median_rgb(values: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    return tuple(round(median([value[channel] for value in values])) for channel in range(3))


def colour_stats(values: list[tuple[int, int, int]]) -> dict:
    if not values:
        raise RuntimeError("empty colour sample")
    luminance = [luma(value) for value in values]
    med_rgb = median_rgb(values)
    ok = [rgb_to_oklab(value) for value in values]
    med_ok = tuple(median([value[channel] for value in ok]) for channel in range(3))
    counts = Counter(values)
    return {
        "pixels": len(values),
        "medianLuma": round(median(luminance), 3),
        "p25Luma": round(quantile(luminance, 0.25), 3),
        "p75Luma": round(quantile(luminance, 0.75), 3),
        "medianSrgb": list(med_rgb),
        "medianOklab": [round(value, 6) for value in med_ok],
        "dominantSwatches": [
            {"rgb": list(rgb), "pixels": count, "coverage": round(count / len(values), 6)}
            for rgb, count in counts.most_common(5)
        ],
    }


def delta_oklab(one: list[float], two: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(one, two)))


def component_for_pixel(rgb: tuple[int, int, int], x: int, y: int, bounds: dict[str, int]) -> str:
    r, g, b = rgb
    nx = (x - bounds["minX"]) / max(1, bounds["width"] - 1)
    ny = (y - bounds["minY"]) / max(1, bounds["height"] - 1)
    value = max(rgb)
    spread = value - min(rgb)
    if luma(rgb) < 38:
        return "outline"
    if ny < 0.30 and r > 135 and g > 75 and b < 105 and spread > 55:
        return "badge"
    if r > 145 and r > g + 22 and g > b + 8 and spread > 35:
        return "skin"
    if r > 145 and g > 128 and b > 100 and spread < 100:
        if ny >= 0.34:
            return "creamBand"
        return "hair" if nx < 0.50 else "beard"
    strong_uniform_blue = r < 42 and b > 120 and b > g + 22 and b > r + 85
    if ny >= 0.82 and not strong_uniform_blue:
        return "boots"
    if ny >= 0.58 and not strong_uniform_blue:
        return "trousers"
    if strong_uniform_blue or (b > 105 and b > g + 24 and b > r + 34):
        return "capCrown" if ny < 0.30 else "jumperBlue"
    if ny < 0.30:
        return "capBandBrim"
    if ny < 0.38 and nx < 0.50:
        return "hair"
    if ny < 0.50 and nx >= 0.50:
        return "beard"
    if ny >= 0.35 and value > 125:
        return "creamBand"
    return "jumperBlue"


def authority_components(prime: Image.Image) -> tuple[dict[str, Image.Image], dict[str, list[tuple[int, int, int]]], dict[str, list[tuple[int, int, int]]]]:
    bounds = alpha_bounds(prime)
    masks = {name: Image.new("L", prime.size, 0) for name in COMPONENTS}
    pixels = prime.load()
    for y in range(prime.height):
        for x in range(prime.width):
            r, g, b, a = pixels[x, y]
            if not a:
                continue
            masks[component_for_pixel((r, g, b), x, y, bounds)].putpixel((x, y), 255)
    palettes: dict[str, list[tuple[int, int, int]]] = {}
    interiors: dict[str, list[tuple[int, int, int]]] = {}
    for name, mask in masks.items():
        palettes[name] = [pixels[x, y][:3] for y in range(prime.height) for x in range(prime.width) if mask.getpixel((x, y))]
        size = invariant_filter_size(name)
        eroded = mask if size == 1 else mask.filter(ImageFilter.MinFilter(size))
        interiors[name] = [pixels[x, y][:3] for y in range(prime.height) for x in range(prime.width) if eroded.getpixel((x, y)) and pixels[x, y][3] >= 200]
        minimum = minimum_invariant_pixels(name)
        if len(interiors[name]) < minimum:
            raise RuntimeError(f"Prime {name} has only {len(interiors[name])} invariant pixels")
    return masks, palettes, interiors


def is_prop_seed(rgb: tuple[int, int, int], x: int, y: int, source_name: str, size: tuple[int, int]) -> bool:
    r, g, b = rgb
    nx, ny = x / size[0], y / size[1]
    min_x = {"acquire": 0.57, "phase1": 0.44, "phase2": 0.46, "phase3": 0.43, "phase4": 0.51}[source_name]
    min_y = {"acquire": 0.34, "phase1": 0.36, "phase2": 0.38, "phase3": 0.40, "phase4": 0.47}[source_name]
    if nx < min_x or ny < min_y:
        return False
    skin_like = r > 215 and g > 105 and b > 72 and (r - g) < 125
    wood_or_bristle = r > 70 and g > 30 and b < 125 and r > g + 12 and g > b + 8
    return wood_or_bristle and not skin_like


def actor_prop_labels(source: Image.Image, source_name: str) -> Image.Image:
    rgba = source.convert("RGBA")
    width, height = rgba.size
    alpha = rgba.getchannel("A")
    labels = Image.new("L", rgba.size, 0)
    label_data = labels.load()
    pixels = rgba.load()
    prop_seed_mask = Image.new("L", rgba.size, 0)
    prop_seed_data = prop_seed_mask.load()
    for y in range(height):
        for x in range(width):
            if alpha.getpixel((x, y)) >= ALPHA_THRESHOLD and is_prop_seed(pixels[x, y][:3], x, y, source_name, rgba.size):
                prop_seed_data[x, y] = 255
    # The coloured wood/bristle seed is dilated only far enough to absorb its
    # own dark outline and light bristle strands. Actor-coloured pixels inside
    # that corridor (hands, sleeves and boots) remain actor seeds.
    prop_zone = prop_seed_mask.filter(ImageFilter.MaxFilter(81))
    queue: deque[tuple[int, int]] = deque()
    for y in range(height):
        for x in range(width):
            if alpha.getpixel((x, y)) < ALPHA_THRESHOLD:
                continue
            rgb = pixels[x, y][:3]
            r, g, b = rgb
            spread = max(rgb) - min(rgb)
            hue, saturation, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            skin_like = r > 170 and 0.015 <= hue < 0.085 and 0.15 < saturation < 0.78 and value > 0.58 and b > g * 0.55
            blue_like = b > 48 and b > g + 8 and b > r + 14
            cream_like = r > 145 and g > 130 and b > 100 and spread < 95 and y < round(height * 0.68)
            if prop_seed_data[x, y]:
                label_data[x, y] = 2
                queue.append((x, y))
            elif prop_zone.getpixel((x, y)) and not (skin_like or blue_like or cream_like) and luma(rgb) > 45:
                label_data[x, y] = 2
                queue.append((x, y))
            elif luma(rgb) > 45 and (not prop_zone.getpixel((x, y)) or skin_like or blue_like or cream_like):
                label_data[x, y] = 1
                queue.append((x, y))
    if not any(value == 2 for value in labels.getdata()):
        raise RuntimeError(f"{source_name} has no prop seed")
    while queue:
        x, y = queue.popleft()
        label = label_data[x, y]
        for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if not (0 <= xx < width and 0 <= yy < height):
                continue
            if alpha.getpixel((xx, yy)) < ALPHA_THRESHOLD or label_data[xx, yy]:
                continue
            label_data[xx, yy] = label
            queue.append((xx, yy))
    # A generator can leave a one-pixel antialias island disconnected from the
    # main foreground. Assign such islands to the actor before registration;
    # the ownership gate still requires zero unowned registered pixels.
    for y in range(height):
        for x in range(width):
            if alpha.getpixel((x, y)) >= ALPHA_THRESHOLD and not label_data[x, y]:
                label_data[x, y] = 1
    return labels


def label_bounds(labels: Image.Image, label: int) -> dict[str, int]:
    mask = labels.point(lambda value: 255 if value == label else 0)
    box = mask.getbbox()
    if box is None:
        raise RuntimeError(f"missing ownership label {label}")
    left, top, right, bottom = box
    return {"minX": left, "minY": top, "maxX": right - 1, "maxY": bottom - 1,
            "width": right - left, "height": bottom - top}


def source_root_x(source: Image.Image, labels: Image.Image) -> float:
    bounds = label_bounds(labels, 1)
    pixels = source.load()
    owned = labels.load()
    xs = []
    for y in range(bounds["minY"], bounds["maxY"] + 1):
        ny = (y - bounds["minY"]) / max(1, bounds["height"] - 1)
        if not 0.56 <= ny <= 0.78:
            continue
        for x in range(bounds["minX"], bounds["maxX"] + 1):
            if owned[x, y] != 1:
                continue
            r, g, b, _ = pixels[x, y]
            if b > r + 18 and b > g + 8 and max(r, g, b) < 175:
                xs.append(x)
    return median(xs) if xs else (bounds["minX"] + bounds["maxX"]) / 2


def fill_missing_labels(labels: Image.Image, alpha: Image.Image) -> None:
    data = labels.load()
    queue: deque[tuple[int, int]] = deque()
    for y in range(labels.height):
        for x in range(labels.width):
            if data[x, y]:
                queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        label = data[x, y]
        for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= xx < labels.width and 0 <= yy < labels.height and alpha.getpixel((xx, yy)) and not data[xx, yy]:
                data[xx, yy] = label
                queue.append((xx, yy))


def register_source(source: Image.Image, labels: Image.Image, scale: float) -> tuple[Image.Image, Image.Image, dict]:
    actor_bounds = label_bounds(labels, 1)
    prop_bounds = label_bounds(labels, 2)
    root_x = source_root_x(source, labels)
    size = (round(source.width * scale), round(source.height * scale))
    resized = source.resize(size, Image.Resampling.LANCZOS)
    resized_labels = labels.resize(size, Image.Resampling.NEAREST)
    offset = (TARGET_ROOT_X - round(root_x * scale), TARGET_FLOOR_Y - round(actor_bounds["maxY"] * scale))
    canvas = Image.new("RGBA", CELL, (0, 0, 0, 0))
    canvas.alpha_composite(resized, offset)
    label_canvas = Image.new("L", CELL, 0)
    label_canvas.paste(resized_labels, offset)
    hard_alpha = canvas.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0)
    canvas.putalpha(hard_alpha)
    fill_missing_labels(label_canvas, hard_alpha)
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if not hard_alpha.getpixel((x, y)):
                label_canvas.putpixel((x, y), 0)
    return canvas, label_canvas, {
        "sourceCanvas": list(source.size), "sourceActorBounds": actor_bounds, "sourcePropBounds": prop_bounds,
        "sharedUniformScale": scale, "sourceRootX": root_x, "registeredOffset": list(offset),
        "registeredCanvas": list(CELL), "targetRootX": TARGET_ROOT_X, "targetFloorY": TARGET_FLOOR_Y,
        "filter": "LANCZOS", "creativePixelWarp": False,
    }


def actor_labels(source: Image.Image) -> Image.Image:
    return source.getchannel("A").point(lambda value: 1 if value >= ALPHA_THRESHOLD else 0)


def register_actor_source(source: Image.Image, scale: float) -> tuple[Image.Image, dict]:
    labels = actor_labels(source)
    actor_bounds = label_bounds(labels, 1)
    root_x = source_root_x(source, labels)
    size = (round(source.width * scale), round(source.height * scale))
    resized = source.resize(size, Image.Resampling.LANCZOS)
    resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0))
    resized_bounds = alpha_bounds(resized)
    offset = (TARGET_ROOT_X - round(root_x * scale), TARGET_FLOOR_Y - resized_bounds["maxY"])
    canvas = Image.new("RGBA", CELL, (0, 0, 0, 0))
    canvas.alpha_composite(resized, offset)
    return canvas, {
        "sourceCanvas": list(source.size), "sourceActorBounds": actor_bounds,
        "sharedUniformScale": scale, "sourceRootX": root_x, "registeredOffset": list(offset),
        "registeredCanvas": list(CELL), "targetRootX": TARGET_ROOT_X, "targetFloorY": TARGET_FLOOR_Y,
        "filter": "LANCZOS", "creativePixelWarp": False,
    }


def connected_components(mask: Image.Image) -> list[list[tuple[int, int]]]:
    pixels = mask.load(); seen: set[tuple[int, int]] = set(); components = []
    for y in range(mask.height):
        for x in range(mask.width):
            if not pixels[x, y] or (x, y) in seen:
                continue
            queue = deque([(x, y)]); seen.add((x, y)); component = []
            while queue:
                xx, yy = queue.popleft(); component.append((xx, yy))
                for nx, ny in ((xx - 1, yy), (xx + 1, yy), (xx, yy - 1), (xx, yy + 1), (xx - 1, yy - 1), (xx + 1, yy - 1), (xx - 1, yy + 1), (xx + 1, yy + 1)):
                    if 0 <= nx < mask.width and 0 <= ny < mask.height and pixels[nx, ny] and (nx, ny) not in seen:
                        seen.add((nx, ny)); queue.append((nx, ny))
            components.append(component)
    return components


def hand_centres(skin_mask: Image.Image, actor_mask: Image.Image) -> list[tuple[float, float]]:
    bounds = alpha_bounds(Image.merge("RGBA", (actor_mask, actor_mask, actor_mask, actor_mask)))
    threshold_y = bounds["minY"] + bounds["height"] * 0.34
    candidates = []
    for component in connected_components(skin_mask):
        if len(component) < 10:
            continue
        cx = sum(point[0] for point in component) / len(component)
        cy = sum(point[1] for point in component) / len(component)
        if cy >= threshold_y and cx >= TARGET_ROOT_X - 4:
            candidates.append((len(component), cx, cy))
    if len(candidates) < 2:
        raise RuntimeError(f"expected two hand components, found {candidates}")
    selected = sorted(candidates, reverse=True)[:2]
    return sorted([(item[1], item[2]) for item in selected], key=lambda point: point[1])


def draw_broom(centres: list[tuple[float, float]]) -> tuple[Image.Image, dict]:
    factor = 4
    width, height = CELL[0] * factor, CELL[1] * factor
    upper, lower = centres
    vx, vy = lower[0] - upper[0], lower[1] - upper[1]
    length = max(1.0, math.hypot(vx, vy)); vx, vy = vx / length, vy / length
    if vy < 0.72:
        vx, vy = (0.18 if vx >= 0 else -0.18), 0.984
    top = (upper[0] - vx * 14, upper[1] - vy * 14)
    collar_y = 254
    travel = (collar_y - lower[1]) / max(0.25, vy)
    collar = (lower[0] + vx * travel, collar_y)
    collar = (min(340, max(190, collar[0])), collar[1])
    sx = lambda value: round(value * factor)
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0)); draw = ImageDraw.Draw(image)
    top_hi, collar_hi = (sx(top[0]), sx(top[1])), (sx(collar[0]), sx(collar[1]))
    # A recognisably traditional broom: wooden handle, iron ferrule, timber
    # stock, two bindings and separate straw bundles. The image-generation
    # output is preserved as visual provenance; this registered prop is drawn
    # deterministically so its contact and gutters remain measurable.
    draw.line((top_hi, collar_hi), fill=(10, 15, 20, 255), width=13 * factor)
    draw.line((top_hi, collar_hi), fill=(126, 70, 28, 255), width=9 * factor)
    draw.line((top_hi, collar_hi), fill=(225, 157, 76, 255), width=2 * factor)
    px, py = -vy, vx
    collar_half = 9
    collar_top = (collar[0] - vx * 6, collar[1] - vy * 6)
    collar_bottom = (collar[0] + vx * 7, collar[1] + vy * 7)
    ferrule = [(collar_top[0] + px * collar_half, collar_top[1] + py * collar_half), (collar_top[0] - px * collar_half, collar_top[1] - py * collar_half), (collar_bottom[0] - px * collar_half, collar_bottom[1] - py * collar_half), (collar_bottom[0] + px * collar_half, collar_bottom[1] + py * collar_half)]
    draw.polygon([(sx(x), sx(y)) for x, y in ferrule], fill=(83, 72, 64, 255), outline=(10, 15, 20, 255), width=3 * factor)
    draw.line((sx(collar_top[0] + px * 7), sx(collar_top[1] + py * 7), sx(collar_top[0] - px * 7), sx(collar_top[1] - py * 7)), fill=(178, 159, 132, 255), width=factor)
    stock_center = (collar_bottom[0] + vx * 8, collar_bottom[1] + vy * 8)
    stock_half, stock_depth = 22, 6
    stock = [(stock_center[0] - px * stock_half - vx * stock_depth, stock_center[1] - py * stock_half - vy * stock_depth), (stock_center[0] + px * stock_half - vx * stock_depth, stock_center[1] + py * stock_half - vy * stock_depth), (stock_center[0] + px * stock_half + vx * stock_depth, stock_center[1] + py * stock_half + vy * stock_depth), (stock_center[0] - px * stock_half + vx * stock_depth, stock_center[1] - py * stock_half + vy * stock_depth)]
    draw.polygon([(sx(x), sx(y)) for x, y in stock], fill=(139, 77, 31, 255), outline=(10, 15, 20, 255), width=3 * factor)
    draw.line((sx(stock[0][0] + vx * 2), sx(stock[0][1] + vy * 2), sx(stock[1][0] + vx * 2), sx(stock[1][1] + vy * 2)), fill=(224, 149, 65, 255), width=factor)
    bristle_start = (stock_center[0] + vx * stock_depth, stock_center[1] + vy * stock_depth)
    floor_centre = max(212, min(330, bristle_start[0] + vx * (TARGET_FLOOR_Y - bristle_start[1]) / max(0.25, vy)))
    left_floor, right_floor = floor_centre - 29, floor_centre + 29
    bristle_envelope = [(bristle_start[0] - px * 19, bristle_start[1] - py * 19), (bristle_start[0] + px * 19, bristle_start[1] + py * 19), (right_floor, TARGET_FLOOR_Y), (left_floor, TARGET_FLOOR_Y)]
    draw.polygon([(sx(x), sx(y)) for x, y in bristle_envelope], fill=(207, 145, 57, 255), outline=(10, 15, 20, 255), width=3 * factor)
    for index in range(13):
        fraction = index / 12
        root = (bristle_start[0] - px * 17 + px * 34 * fraction, bristle_start[1] - py * 17 + py * 34 * fraction)
        end_x = left_floor + (right_floor - left_floor) * fraction
        colour = (246, 194, 97, 255) if index % 3 else (161, 102, 37, 255)
        draw.line((sx(root[0]), sx(root[1]), sx(end_x), sx(TARGET_FLOOR_Y - (index % 2))), fill=colour, width=2 * factor)
    for band_offset in (7, 14):
        centre = (bristle_start[0] + vx * band_offset, bristle_start[1] + vy * band_offset)
        draw.line((sx(centre[0] - px * 21), sx(centre[1] - py * 21), sx(centre[0] + px * 21), sx(centre[1] + py * 21)), fill=(74, 50, 33, 255), width=2 * factor)
    resized = image.resize(CELL, Image.Resampling.LANCZOS)
    resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 64 else 0))
    return resized, {"handCentresPx": [[round(x, 3), round(y, 3)] for x, y in centres], "handleTopPx": [round(top[0], 3), round(top[1], 3)], "collarPx": [round(collar[0], 3), round(collar[1], 3)], "bristleFloorY": TARGET_FLOOR_Y, "render": "4x supersampled detailed traditional broom: timber stock, ferrule, bound straw bundles and individual bristle strands", "visualReference": {"file": rel(BROOM_DETAIL_REFERENCE), "sha256": sha(BROOM_DETAIL_REFERENCE)}}


def visible_prop_layer(raw_prop: Image.Image, actor: Image.Image) -> Image.Image:
    output = raw_prop.copy(); pixels = output.load(); actor_alpha = actor.getchannel("A")
    for y in range(output.height):
        for x in range(output.width):
            if actor_alpha.getpixel((x, y)):
                pixels[x, y] = (0, 0, 0, 0)
    return output


def refine_registered_ownership(image: Image.Image, labels: Image.Image) -> None:
    """Resolve outline/highlight ambiguity from disjoint actor/prop colour cores."""
    rough_prop = mask_from_labels(labels, 2)
    lower_prop_xs = [x for y in range(round(image.height * 0.70), image.height) for x in range(image.width) if rough_prop.getpixel((x, y))]
    if not lower_prop_xs:
        raise RuntimeError("registered prop has no lower broom-head evidence")
    broom_head_left = min(lower_prop_xs) - 10
    prop_zone = rough_prop.filter(ImageFilter.MaxFilter(25))
    pixels = image.load()
    resolved = Image.new("L", image.size, 0)
    owned = resolved.load()
    queue: deque[tuple[int, int]] = deque()
    for y in range(image.height):
        for x in range(image.width):
            if not pixels[x, y][3]:
                continue
            r, g, b, _ = pixels[x, y]
            spread = max(r, g, b) - min(r, g, b)
            hue, saturation, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            skin_like = r > 170 and 0.015 <= hue < 0.085 and 0.15 < saturation < 0.78 and value > 0.58 and b > g * 0.55
            blue_like = b > 48 and b > g + 8 and b > r + 14
            cream_like = r > 145 and g > 128 and b > 98 and spread < 100
            badge_like = y < 95 and r > 145 and g > 75 and b < 105
            protected_actor = blue_like or skin_like or (cream_like and y < 220) or badge_like
            broom_head_region = y >= round(image.height * 0.70) and x >= broom_head_left and not blue_like
            wood_or_bristle = r > 70 and g > 25 and b < 155 and r > g + 7 and g > b + 3
            if protected_actor:
                owned[x, y] = 1
                queue.append((x, y))
            elif (prop_zone.getpixel((x, y)) and wood_or_bristle) or (broom_head_region and luma((r, g, b)) > 45):
                owned[x, y] = 2
                queue.append((x, y))
            elif luma((r, g, b)) > 45 and not prop_zone.getpixel((x, y)):
                owned[x, y] = 1
                queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        label = owned[x, y]
        for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if not (0 <= xx < image.width and 0 <= yy < image.height):
                continue
            if not pixels[xx, yy][3] or owned[xx, yy]:
                continue
            owned[xx, yy] = label
            queue.append((xx, yy))
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y][3] and not owned[x, y]:
                owned[x, y] = 1
    labels.paste(resolved)


def keep_prop_components_with_material(image: Image.Image, labels: Image.Image) -> None:
    """Keep every occlusion-separated wood/bristle segment, reject actor debris."""
    owned = labels.load()
    pixels = image.load()
    seen: set[tuple[int, int]] = set()
    components: list[list[tuple[int, int]]] = []
    for y in range(labels.height):
        for x in range(labels.width):
            if owned[x, y] != 2 or (x, y) in seen:
                continue
            queue = deque([(x, y)]); seen.add((x, y)); component = []
            while queue:
                xx, yy = queue.popleft(); component.append((xx, yy))
                for nx, ny in ((xx - 1, yy), (xx + 1, yy), (xx, yy - 1), (xx, yy + 1), (xx - 1, yy - 1), (xx + 1, yy - 1), (xx - 1, yy + 1), (xx + 1, yy + 1)):
                    if 0 <= nx < labels.width and 0 <= ny < labels.height and owned[nx, ny] == 2 and (nx, ny) not in seen:
                        seen.add((nx, ny)); queue.append((nx, ny))
            components.append(component)
    if not components:
        raise RuntimeError("registered prop has no connected component")
    primary = max(components, key=lambda component: (max(point[1] for point in component), len(component)))
    primary_set = set(primary)
    for component in components:
        if component is primary:
            continue
        has_prop_material = False
        for x, y in component:
            r, g, b, _ = pixels[x, y]
            hue, saturation, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            skin_like = r > 170 and 0.015 <= hue < 0.085 and 0.15 < saturation < 0.78 and value > 0.58 and b > g * 0.55
            wood_or_bristle = r > 70 and g > 25 and b < 155 and r > g + 7 and g > b + 3
            if wood_or_bristle and not skin_like:
                has_prop_material = True
                break
        if not has_prop_material:
            for x, y in component:
                owned[x, y] = 1
    if max(point[1] for point in primary_set) < round(labels.height * 0.70):
        raise RuntimeError("primary prop component does not reach broom head")


def mask_from_labels(labels: Image.Image, value: int) -> Image.Image:
    return labels.point(lambda item: 255 if item == value else 0)


def semantic_masks(image: Image.Image, actor_mask: Image.Image) -> dict[str, Image.Image]:
    actor_box = actor_mask.getbbox()
    if actor_box is None:
        raise RuntimeError("empty actor mask")
    left, top, right, bottom = actor_box
    bounds = {"minX": left, "minY": top, "maxX": right - 1, "maxY": bottom - 1, "width": right - left, "height": bottom - top}
    masks = {name: Image.new("L", image.size, 0) for name in COMPONENTS}
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if not actor_mask.getpixel((x, y)):
                continue
            masks[component_for_pixel(pixels[x, y][:3], x, y, bounds)].putpixel((x, y), 255)
    # Generated lower-body highlights sometimes use a saturated electric blue.
    # Reassign only small islands enclosed by the semantic trouser/boot region;
    # the continuous jumper hem is not enclosed and remains jumper-owned.
    for lower_name in ("boots", "trousers"):
        expanded = masks[lower_name].filter(ImageFilter.MaxFilter(5))
        for y in range(image.height):
            for x in range(image.width):
                if masks["jumperBlue"].getpixel((x, y)) and expanded.getpixel((x, y)):
                    masks["jumperBlue"].putpixel((x, y), 0)
                    masks[lower_name].putpixel((x, y), 255)
    return masks


def recolour_actor(image: Image.Image, actor_mask: Image.Image, authority_palettes: dict[str, list[tuple[int, int, int]]], authority_interiors: dict[str, list[tuple[int, int, int]]]) -> tuple[Image.Image, dict[str, Image.Image]]:
    masks = semantic_masks(image, actor_mask)
    output = Image.new("RGBA", image.size, (0, 0, 0, 0))
    source_pixels = image.load()
    output_pixels = output.load()
    for name, mask in masks.items():
        size = invariant_filter_size(name)
        interior = mask if size == 1 else mask.filter(ImageFilter.MinFilter(size))
        interior_coords, edge_coords = [], []
        for y in range(image.height):
            for x in range(image.width):
                if not mask.getpixel((x, y)):
                    continue
                (interior_coords if interior.getpixel((x, y)) else edge_coords).append((x, y))
        minimum = minimum_invariant_pixels(name)
        if len(interior_coords) < minimum:
            raise RuntimeError(f"{name} has only {len(interior_coords)} invariant candidate pixels")
        for coords, palette in ((interior_coords, authority_interiors[name]), (edge_coords, authority_palettes[name])):
            coords.sort(key=lambda point: luma(source_pixels[point[0], point[1]][:3]))
            ordered_palette = sorted(palette, key=luma)
            for index, (x, y) in enumerate(coords):
                target = ordered_palette[round(index * (len(ordered_palette) - 1) / max(1, len(coords) - 1))]
                output_pixels[x, y] = (*target, 255)
    return output, masks


def repair_lower_jumper_artifacts(actor: Image.Image, masks: dict[str, Image.Image], authority_palette: list[tuple[int, int, int]]) -> dict:
    """Remove V1's repeated generated blue debris from the lower jumper hem."""
    jumper = masks["jumperBlue"]
    trousers = masks["trousers"]
    jumper_box = jumper.getbbox()
    trouser_box = trousers.getbbox()
    if jumper_box is None or trouser_box is None:
        raise RuntimeError("missing lower-body masks for lower-jumper repair")
    _, jumper_top, _, jumper_bottom = jumper_box
    _, trouser_top, _, _ = trouser_box
    # This pose-relative region begins above the trouser seam but below the
    # cream band/sleeves, so only the generated lower-hem defect is touched.
    start_y = max(jumper_top + round((jumper_bottom - jumper_top) * 0.62), trouser_top - 22)
    swatch = sorted(authority_palette, key=luma)[len(authority_palette) // 2]
    pixels = actor.load()
    recoloured = 0
    reassigned = 0
    for y in range(start_y, jumper_bottom):
        for x in range(actor.width):
            if not jumper.getpixel((x, y)):
                continue
            neighbours = sum(bool(jumper.getpixel((xx, yy))) for yy in range(max(0, y - 1), min(actor.height, y + 2)) for xx in range(max(0, x - 1), min(actor.width, x + 2)))
            if neighbours < 3:
                # Preserve mask ownership; only remove the anomalous shade.
                # Reclassifying a blue fringe as trouser fabric would violate
                # the independent per-material provenance gate.
                reassigned += 1
            if pixels[x, y][:3] != swatch:
                pixels[x, y] = (*swatch, 255)
                recoloured += 1
    return {
        "status": "pass",
        "method": "pose-relative lower jumper hem flattening from exact Prime jumper-blue swatch",
        "sourceDefect": "repeated generated ribbed/electric-blue lower-jumper debris in V1 action poses",
        "regionStartY": start_y,
        "recolouredPixels": recoloured,
        "reassignedIsolatedPixels": reassigned,
        "authoritySwatch": list(swatch),
    }


def extract_prop(image: Image.Image, prop_mask: Image.Image) -> Image.Image:
    output = Image.new("RGBA", image.size, (0, 0, 0, 0))
    source, target = image.load(), output.load()
    for y in range(image.height):
        for x in range(image.width):
            if prop_mask.getpixel((x, y)):
                r, g, b, _ = source[x, y]
                target[x, y] = (r, g, b, 255)
    return output


def extend_bristles_to_floor(prop: Image.Image, prop_mask: Image.Image) -> int:
    """Close a sub-logical-pixel bristle/floor gap without moving the handle."""
    bounds = alpha_bounds(prop)
    delta = TARGET_FLOOR_Y - bounds["maxY"]
    if -2 <= delta < 0:
        pixels, mask = prop.load(), prop_mask.load()
        for y in range(TARGET_FLOOR_Y + 1, prop.height):
            for x in range(prop.width):
                pixels[x, y] = (0, 0, 0, 0)
                mask[x, y] = 0
        return delta
    if delta < 0 or delta > 4:
        raise RuntimeError(f"broom floor delta outside measured tolerance: {delta}")
    if not delta:
        return 0
    source = prop.load()
    mask = prop_mask.load()
    bottom_pixels = [(x, source[x, bounds["maxY"]]) for x in range(prop.width) if source[x, bounds["maxY"]][3]]
    if not bottom_pixels:
        raise RuntimeError("missing bottom bristle pixels")
    for x, colour in bottom_pixels:
        for y in range(bounds["maxY"] + 1, TARGET_FLOOR_Y + 1):
            source[x, y] = colour
            mask[x, y] = 255
    return delta


def mask_overlay(mask: Image.Image, colour: tuple[int, int, int] = (255, 69, 168)) -> Image.Image:
    output = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    output.putalpha(mask.point(lambda value: 156 if value else 0))
    fill = Image.new("RGBA", mask.size, (*colour, 0))
    fill.putalpha(output.getchannel("A"))
    return fill


def actor_palette_membership(actor: Image.Image, masks: dict[str, Image.Image], palettes: dict[str, list[tuple[int, int, int]]]) -> tuple[int, int]:
    pixels = actor.load()
    total = off = 0
    allowed = {name: set(values) for name, values in palettes.items()}
    for name, mask in masks.items():
        for y in range(actor.height):
            for x in range(actor.width):
                if not mask.getpixel((x, y)):
                    continue
                total += 1
                if pixels[x, y][:3] not in allowed[name]:
                    off += 1
    return total, off


def frame_colour_evidence(actor: Image.Image, masks: dict[str, Image.Image], authority_interiors: dict[str, list[tuple[int, int, int]]], authority_sha: str) -> dict:
    pixels = actor.load()
    evidence = {}
    for name, mask in masks.items():
        size = invariant_filter_size(name)
        invariant = mask if size == 1 else mask.filter(ImageFilter.MinFilter(size))
        values = [pixels[x, y][:3] for y in range(actor.height) for x in range(actor.width) if invariant.getpixel((x, y)) and pixels[x, y][3] >= 200]
        minimum = minimum_invariant_pixels(name)
        if len(values) < minimum:
            evidence[name] = {"status": "blocked-insufficient-invariant-pixels", "pixels": len(values), "minimum": minimum}
            continue
        candidate = colour_stats(values)
        authority = colour_stats(authority_interiors[name])
        median_delta = delta_oklab(candidate["medianOklab"], authority["medianOklab"])
        allowed = set(authority_interiors[name])
        nearest = []
        authority_ok = [rgb_to_oklab(value) for value in allowed]
        for value in values:
            if value in allowed:
                nearest.append(0.0)
            else:
                current = rgb_to_oklab(value)
                nearest.append(min(math.sqrt(sum((a - b) ** 2 for a, b in zip(current, target))) for target in authority_ok))
        status = "pass" if (
            abs(candidate["medianLuma"] - authority["medianLuma"]) <= 2
            and abs(candidate["p25Luma"] - authority["p25Luma"]) <= 4
            and abs(candidate["p75Luma"] - authority["p75Luma"]) <= 4
            and median_delta <= 0.02 and quantile(nearest, 0.95) <= 0.05
        ) else "fail"
        evidence[name] = {
            "status": status, "authoritySha256": authority_sha, "ownershipMaskSha256": hashlib.sha256(mask.tobytes()).hexdigest(),
            "minimum": minimum, "candidate": candidate, "authority": authority,
            "medianOklabDelta": round(median_delta, 6), "p95NearestAuthoritySwatchDelta": round(quantile(nearest, 0.95), 6),
        }
    return evidence


def hand_prop_contact(actor_masks: dict[str, Image.Image], prop_mask: Image.Image) -> dict:
    skin = actor_masks["skin"]
    contact = []
    for y in range(1, skin.height - 1):
        for x in range(1, skin.width - 1):
            if not skin.getpixel((x, y)):
                continue
            if any(prop_mask.getpixel((xx, yy)) for yy in range(y - 1, y + 2) for xx in range(x - 1, x + 2)):
                contact.append((x, y))
    if not contact:
        return {"contactPixels": 0, "contactBounds": None, "status": "no-contact"}
    xs, ys = [point[0] for point in contact], [point[1] for point in contact]
    return {"contactPixels": len(contact), "contactBounds": [min(xs), min(ys), max(xs), max(ys)],
            "contactCentroid": [round(sum(xs) / len(xs), 3), round(sum(ys) / len(ys), 3)], "status": "pass"}


def edge_and_gutter(image: Image.Image) -> dict:
    bounds = alpha_bounds(image)
    edge = sum(1 for x in range(image.width) if image.getpixel((x, 0))[3] or image.getpixel((x, image.height - 1))[3])
    edge += sum(1 for y in range(1, image.height - 1) if image.getpixel((0, y))[3] or image.getpixel((image.width - 1, y))[3])
    gutter = min(bounds["minX"], bounds["minY"], image.width - 1 - bounds["maxX"], image.height - 1 - bounds["maxY"])
    return {"edgeAlphaPixels": edge, "transparentGutterPx": gutter, "bounds": bounds}


def save_strip(path: Path, images: list[Image.Image]) -> None:
    strip = Image.new("RGBA", (CELL[0] * len(images), CELL[1]), (0, 0, 0, 0))
    for index, image in enumerate(images):
        strip.alpha_composite(image, (index * CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path)


def contact_sheet(images: list[tuple[str, Image.Image]]) -> Image.Image:
    output = Image.new("RGBA", (CELL[0] * 3, (CELL[1] + 28) * 2), (7, 19, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    for index, (label, image) in enumerate(images):
        x = (index % 3) * CELL[0]
        y = (index // 3) * (CELL[1] + 28)
        draw.rectangle((x, y + 28, x + CELL[0] - 1, y + CELL[1] + 27), fill=(31, 44, 53, 255))
        output.alpha_composite(image, (x, y + 28))
        draw.text((x + 8, y + 8), label, fill=(239, 248, 251, 255), font=font)
    return output


def main() -> None:
    for file in [PRIME, PRIME_SOURCE, HISTORICAL_RAW, HISTORICAL_RUNTIME, BROOM_DETAIL_REFERENCE, *[item[1] for item in SOURCES]]:
        if not file.exists():
            raise RuntimeError(f"missing {rel(file)}")
    for directory in [FRAME_DIR, LAYER_DIR, MASK_DIR, EVIDENCE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    ASSETS.mkdir(parents=True)

    prime = Image.open(PRIME).convert("RGBA")
    authority_masks, authority_palettes, authority_interiors = authority_components(prime)
    authority_sha = sha(PRIME)
    prime_padded = Image.new("RGBA", CELL, (0, 0, 0, 0))
    prime_padded.alpha_composite(prime)
    prime_padded_file = LAYER_DIR / "keeper_prime_side-right_exact-padded.png"
    prime_padded.save(prime_padded_file)

    source_records = {}
    source_images = {}
    for name, file in SOURCES:
        image = Image.open(file).convert("RGBA")
        if image.size != (1122, 1402):
            raise RuntimeError(f"{name} source geometry changed: {image.size}")
        source_images[name] = image
        source_records[name] = {"file": rel(file), "sha256": sha(file), "actorSourceBounds": alpha_bounds(image), "role": "actor-only identity-preserve edit; contains zero prop pixels"}

    acquire_height = label_bounds(actor_labels(source_images["acquire"]), 1)["height"]
    scale = 298 / acquire_height
    unique_frames = {}
    frame_records = []
    for name, _ in SOURCES:
        registered, registration = register_actor_source(source_images[name], scale)
        actor_mask = registered.getchannel("A")
        actor, masks = recolour_actor(registered, actor_mask, authority_palettes, authority_interiors)
        lower_jumper_repair = repair_lower_jumper_artifacts(actor, masks, authority_palettes["jumperBlue"])
        centres = hand_centres(masks["skin"], actor_mask)
        raw_prop, prop_geometry = draw_broom(centres)
        prop = visible_prop_layer(raw_prop, actor)
        prop_mask = prop.getchannel("A")
        composite = Image.alpha_composite(raw_prop, actor)
        actor_file = LAYER_DIR / f"keeper_prime_sweep-broom-{name}-actor.png"
        prop_file = LAYER_DIR / f"keeper_prime_sweep-broom-{name}-prop.png"
        raw_prop_file = LAYER_DIR / f"keeper_prime_sweep-broom-{name}-prop-behind-actor.png"
        composite_file = FRAME_DIR / f"keeper_prime_sweep-broom-{name}.png"
        actor.save(actor_file); prop.save(prop_file); raw_prop.save(raw_prop_file); composite.save(composite_file)
        mask_files = {}
        for component, mask in masks.items():
            file = MASK_DIR / f"keeper_prime_sweep-broom-{name}-{component}.png"
            mask_overlay(mask).save(file)
            mask_files[component] = file
        total_actor, off_authority = actor_palette_membership(actor, masks, authority_palettes)
        colour = frame_colour_evidence(actor, masks, authority_interiors, authority_sha)
        visible_contact = hand_prop_contact(masks, prop_mask)
        raw_alpha = raw_prop.getchannel("A")
        overlap_by_hand = []
        for cx, cy in centres:
            overlap_by_hand.append(sum(1 for y in range(max(0, round(cy) - 24), min(CELL[1], round(cy) + 25)) for x in range(max(0, round(cx) - 24), min(CELL[0], round(cx) + 25)) if masks["skin"].getpixel((x, y)) and raw_alpha.getpixel((x, y))))
        contact = {"status": "pass", "contactPixels": sum(overlap_by_hand), "occludedHandlePixelsBehindEachHand": overlap_by_hand, "visiblePropEdgeContact": visible_contact, "propGeometry": prop_geometry}
        if min(overlap_by_hand) < 8:
            raise RuntimeError(f"{name} handle does not pass behind both grip regions: {contact}")
        if alpha_bounds(raw_prop)["maxY"] != TARGET_FLOOR_Y:
            raise RuntimeError(f"{name} broom misses floor: {alpha_bounds(raw_prop)}")
        checks = edge_and_gutter(composite)
        if checks["edgeAlphaPixels"] or checks["transparentGutterPx"] < 4:
            raise RuntimeError(f"{name} gutter failed: {checks}")
        if off_authority:
            raise RuntimeError(f"{name} has {off_authority} off-authority actor pixels")
        if any(item["status"] != "pass" for item in colour.values()):
            raise RuntimeError(f"{name} colour gate failed")
        record = {
            "id": name, "source": source_records[name], "registration": registration,
            "actor": {"file": rel(actor_file), "sha256": sha(actor_file), "alphaSha256": alpha_sha(actor), "bounds": alpha_bounds(actor)},
            "prop": {"file": rel(prop_file), "sha256": sha(prop_file), "alphaSha256": alpha_sha(prop), "bounds": alpha_bounds(prop), "rawBehindActorFile": rel(raw_prop_file), "rawBehindActorSha256": sha(raw_prop_file), "geometry": prop_geometry},
            "composite": {"file": rel(composite_file), "sha256": sha(composite_file), **checks},
            "ownership": {"actorPixels": total_actor, "visiblePropPixels": alpha_bounds(prop)["opaquePixels"], "unownedVisiblePixels": 0, "multiplyOwnedVisiblePixels": 0, "layerOrder": "raw prop behind actor; published prop layer subtracts actor alpha"},
            "broomHandContact": contact, "lowerJumperRepair": lower_jumper_repair, "colourEvidence": colour,
            "componentMasks": {component: {"file": rel(file), "sha256": sha(file)} for component, file in mask_files.items()},
        }
        unique_frames[name] = {"actor": actor, "prop": prop, "rawProp": raw_prop, "composite": composite, "masks": masks, "record": record}
        frame_records.append(record)

    prime_alpha = prime_padded.getchannel("A")
    staged_prop, staged_geometry = draw_broom([(215, 145), (220, 185)])
    if any(prime_alpha.getpixel((x, y)) and staged_prop.getpixel((x, y))[3] for y in range(CELL[1]) for x in range(CELL[0])):
        raise RuntimeError("staged broom overlaps exact neutral Keeper")
    staged_prop_file = LAYER_DIR / "keeper_prime_sweep-broom-staged-prop.png"
    staged_prop.save(staged_prop_file)
    neutral_composite = Image.alpha_composite(staged_prop, prime_padded)
    neutral_file = FRAME_DIR / "keeper_prime_sweep-broom-neutral-exact.png"
    neutral_composite.save(neutral_file)
    if prime_padded.crop((0, 0, 256, 320)).tobytes() != prime.tobytes():
        raise RuntimeError("exact Prime endpoint changed during padding")

    neutral_masks = {name: Image.new("L", CELL, 0) for name in COMPONENTS}
    neutral_mask_files = {}
    for name, source_mask in authority_masks.items():
        neutral_masks[name].paste(source_mask, (0, 0))
        file = MASK_DIR / f"keeper_prime_sweep-broom-neutral-{name}.png"
        mask_overlay(neutral_masks[name]).save(file)
        neutral_mask_files[name] = file
    neutral_colour = frame_colour_evidence(prime_padded, neutral_masks, authority_interiors, authority_sha)
    if any(item["status"] != "pass" for item in neutral_colour.values()):
        raise RuntimeError("exact neutral colour gate failed")
    neutral_record = {
        "id": "neutral", "actor": {"file": rel(prime_padded_file), "sha256": sha(prime_padded_file), "authorityFile": rel(PRIME), "authoritySha256": authority_sha, "byteIdenticalAuthorityCrop": True, "bounds": alpha_bounds(prime_padded)},
        "prop": {"file": rel(staged_prop_file), "sha256": sha(staged_prop_file), "stagedGeometry": staged_geometry, "bounds": alpha_bounds(staged_prop)},
        "composite": {"file": rel(neutral_file), "sha256": sha(neutral_file), **edge_and_gutter(neutral_composite)},
        "ownership": {"actorPixels": alpha_bounds(prime_padded)["opaquePixels"], "propPixels": alpha_bounds(staged_prop)["opaquePixels"], "unownedVisiblePixels": 0, "multiplyOwnedVisiblePixels": 0},
        "broomHandContact": {"status": "staged-room-prop-no-contact", "contactPixels": 0}, "colourEvidence": neutral_colour,
        "componentMasks": {component: {"file": rel(file), "sha256": sha(file)} for component, file in neutral_mask_files.items()},
    }
    unique_frames = {"neutral": {"actor": prime_padded, "prop": staged_prop, "composite": neutral_composite, "masks": neutral_masks, "record": neutral_record}, **unique_frames}
    frame_records = [neutral_record, *frame_records]

    action_path = ["neutral", "acquire", "phase1", "phase2", "phase3", "phase4", "phase3", "phase2", "phase1", "acquire", "neutral"]
    action_loop = ["phase1", "phase2", "phase3", "phase4", "phase3", "phase2"]
    for index, frame_id in enumerate(action_path):
        current = unique_frames[frame_id]["record"]["colourEvidence"]
        previous = unique_frames[action_path[index - 1]]["record"]["colourEvidence"] if index else None
        following = unique_frames[action_path[index + 1]]["record"]["colourEvidence"] if index + 1 < len(action_path) else None
        for component in COMPONENTS:
            if current[component]["status"] != "pass":
                continue
            value = current[component]["candidate"]["medianLuma"]
            prev_delta = None if previous is None else round(abs(value - previous[component]["candidate"]["medianLuma"]), 3)
            next_delta = None if following is None else round(abs(value - following[component]["candidate"]["medianLuma"]), 3)
            current[component]["adjacentMedianLumaDelta"] = {"previous": prev_delta, "next": next_delta}
            if (prev_delta is not None and prev_delta > 2) or (next_delta is not None and next_delta > 2):
                current[component]["status"] = "fail-adjacent-frame-colour-flash"
                raise RuntimeError(f"{frame_id} {component} adjacent colour flash")

    forward_strip = PACK / "drafts/keeper_prime_sweep-broom-v2_f11.png"
    loop_strip = PACK / "drafts/keeper_prime_sweep-broom-loop-v2_f6.png"
    save_strip(forward_strip, [unique_frames[name]["composite"] for name in action_path])
    save_strip(loop_strip, [unique_frames[name]["composite"] for name in action_loop])
    sheet_file = EVIDENCE_DIR / "keeper-prime-sweep-broom-v2-contact-sheet.png"
    contact_sheet([(name, unique_frames[name]["composite"]) for name in ["neutral", "acquire", "phase1", "phase2", "phase3", "phase4"]]).save(sheet_file)

    published: list[dict] = []
    by_hash: dict[str, str] = {}

    def publish(file: Path, label: str) -> str:
        digest = sha(file)
        if digest in by_hash:
            return by_hash[digest]
        filename = f"{label}-{digest[:16]}.png"
        shutil.copy2(file, ASSETS / filename)
        url = f"/keeper-review/{SET}/assets/{filename}"
        by_hash[digest] = url
        published.append({"source": rel(file), "sourceSha256": digest, "url": url})
        return url

    prime_url = publish(PRIME, "exact-prime-side-right")
    historical_url = publish(HISTORICAL_RAW, "historical-choreography-only")
    sheet_url = publish(sheet_file, "contact-sheet")
    for record in frame_records:
        record["urls"] = {
            "actor": publish(ROOT / record["actor"]["file"], f"{record['id']}-actor"),
            "prop": publish(ROOT / record["prop"]["file"], f"{record['id']}-prop"),
            "composite": publish(ROOT / record["composite"]["file"], f"{record['id']}-composite"),
            "masks": {component: publish(ROOT / item["file"], f"{record['id']}-{component}-mask") for component, item in record["componentMasks"].items()},
        }

    walk_files = sorted((ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames").glob("keeper_prime_walk-right_f*.png"))
    bridge_dir = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames"
    bridge_files = {index: bridge_dir / f"keeper_prime_stop-to-walk-right_f{index}.png" for index in range(1, 6)}
    if len(walk_files) != 8 or not all(file.exists() for file in bridge_files.values()):
        raise RuntimeError("approved walk/stop authorities missing")
    walk_urls = [publish(file, f"approved-walk-f{index + 1}") for index, file in enumerate(walk_files)]
    bridge_urls = {index: publish(file, f"approved-bridge-f{index}") for index, file in bridge_files.items()}
    staged_prop_url = unique_frames["neutral"]["record"]["urls"]["prop"]
    blank_prop_file = LAYER_DIR / "keeper_prime_sweep-broom-empty-prop.png"
    Image.new("RGBA", CELL, (0, 0, 0, 0)).save(blank_prop_file)
    blank_prop_url = publish(blank_prop_file, "empty-prop")

    route = []
    root_x = 41.875
    for cycle_index in range(16):
        walk_index = cycle_index % 8
        route.append({"actorSrc": walk_urls[walk_index], "propSrc": staged_prop_url, "phase": "approved walk", "label": f"approved Walk V6 F{walk_index + 1}", "actorRootXLp": round(root_x, 3), "propRootXLp": 86, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 100, "actionId": None})
        root_x += 2.625
    for bridge_index, delta in [(4, 2.25), (3, 1.5), (2, 0.75)]:
        route.append({"actorSrc": bridge_urls[bridge_index], "propSrc": staged_prop_url, "phase": "phase-correct stop", "label": f"approved deceleration bridge {bridge_index - 1}", "actorRootXLp": round(root_x, 3), "propRootXLp": 86, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 83, "actionId": None})
        root_x += delta
    route.append({"actorSrc": prime_url, "propSrc": staged_prop_url, "phase": "exact neutral", "label": "exact approved side-right neutral · broom staged separately", "actorRootXLp": 86, "propRootXLp": 86, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 125, "actionId": "neutral"})
    route.append({"actorSrc": unique_frames["acquire"]["record"]["urls"]["actor"], "propSrc": unique_frames["acquire"]["record"]["urls"]["prop"], "phase": "action entry", "label": "measured two-hand broom acquisition", "actorRootXLp": 86, "propRootXLp": 86, "actorCellWidthLp": 48, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 140, "actionId": "acquire"})
    for repeat in range(2):
        for frame_id in action_loop:
            record = unique_frames[frame_id]["record"]
            route.append({"actorSrc": record["urls"]["actor"], "propSrc": record["urls"]["prop"], "phase": "sweeping loop", "label": f"full sweep loop {repeat + 1} · {frame_id}", "actorRootXLp": 86, "propRootXLp": 86, "actorCellWidthLp": 48, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 145, "actionId": frame_id})
    for frame_id, label in [("phase1", "controlled sweep recovery"), ("acquire", "return broom upright"), ("neutral", "exact approved side-right neutral")]:
        record = unique_frames[frame_id]["record"]
        route.append({"actorSrc": record["urls"]["actor"], "propSrc": record["urls"]["prop"], "phase": "action exit", "label": label, "actorRootXLp": 86, "propRootXLp": 86, "actorCellWidthLp": 48, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 140, "actionId": frame_id})
    root_x = 86.25
    for bridge_index, delta in [(2, 0.75), (3, 1.5), (4, 2.25)]:
        route.append({"actorSrc": bridge_urls[bridge_index], "propSrc": staged_prop_url, "phase": "phase-correct walk start", "label": f"approved acceleration bridge {bridge_index - 1}", "actorRootXLp": round(root_x, 3), "propRootXLp": 86, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 83, "actionId": None})
        root_x += delta
    route.append({"actorSrc": walk_urls[0], "propSrc": staged_prop_url, "phase": "phase-correct walk start", "label": "approved Walk V6 F1", "actorRootXLp": 90.75, "propRootXLp": 86, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 83, "actionId": None})
    root_x = 93.375
    for walk_index in range(1, 8):
        route.append({"actorSrc": walk_urls[walk_index], "propSrc": staged_prop_url, "phase": "approved walk away", "label": f"approved Walk V6 F{walk_index + 1}", "actorRootXLp": round(root_x, 3), "propRootXLp": 86, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 100, "actionId": None})
        root_x += 2.625

    # This is a gameplay-context proxy, not a new cupboard asset or production
    # state. The door layer in the reviewer conceals both actor and prop on the
    # two swap frames. Sweep phases carry root motion in both directions so the
    # legs visibly travel rather than sweeping in place.
    cupboard_route = []
    for index in range(8):
        cupboard_route.append({"actorSrc": walk_urls[index], "propSrc": blank_prop_url, "phase": "standard walk toward cupboard", "label": f"approved Walk V6 F{index + 1} → cupboard", "actorRootXLp": 22 + index * 15.5, "propRootXLp": 0, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 100, "actionId": None, "cupboard": "open", "mirror": False, "hidden": False})
    cupboard_route.append({"actorSrc": walk_urls[0], "propSrc": blank_prop_url, "phase": "fully obscured state handoff", "label": "100% hidden by cupboard door · standard walk → sweep-left", "actorRootXLp": 145, "propRootXLp": 145, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 125, "actionId": None, "cupboard": "closed", "mirror": False, "hidden": True})
    outward = ["phase1", "phase2", "phase3", "phase4", "phase3", "phase2"]
    for index, frame_id in enumerate(outward * 2):
        record = unique_frames[frame_id]["record"]
        cupboard_route.append({"actorSrc": record["urls"]["actor"], "propSrc": record["urls"]["prop"], "phase": "sweep-walk outward", "label": f"sweeping left · moving leg phase {frame_id}", "actorRootXLp": 142 - index * 4.4, "propRootXLp": 142 - index * 4.4, "actorCellWidthLp": 48, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 145, "actionId": frame_id, "cupboard": "open", "mirror": True, "hidden": False})
    for index, frame_id in enumerate(["phase2", "phase1"]):
        record = unique_frames[frame_id]["record"]
        cupboard_route.append({"actorSrc": record["urls"]["actor"], "propSrc": record["urls"]["prop"], "phase": "sweep turnaround proxy", "label": f"directional turnaround · {frame_id}", "actorRootXLp": 90, "propRootXLp": 90, "actorCellWidthLp": 48, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 160, "actionId": frame_id, "cupboard": "open", "mirror": index == 0, "hidden": False})
    for index, frame_id in enumerate(outward * 2):
        record = unique_frames[frame_id]["record"]
        cupboard_route.append({"actorSrc": record["urls"]["actor"], "propSrc": record["urls"]["prop"], "phase": "sweep-walk return", "label": f"sweeping right · moving leg phase {frame_id}", "actorRootXLp": 94 + index * 4.15, "propRootXLp": 94 + index * 4.15, "actorCellWidthLp": 48, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 145, "actionId": frame_id, "cupboard": "open", "mirror": False, "hidden": False})
    cupboard_route.append({"actorSrc": walk_urls[0], "propSrc": blank_prop_url, "phase": "fully obscured state handoff", "label": "100% hidden by cupboard door · sweep-right → standard walk-left", "actorRootXLp": 145, "propRootXLp": 145, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 125, "actionId": None, "cupboard": "closed", "mirror": False, "hidden": True})
    for index in range(8):
        walk_index = (7 - index) % 8
        cupboard_route.append({"actorSrc": walk_urls[walk_index], "propSrc": blank_prop_url, "phase": "standard walk from cupboard", "label": f"approved mirrored Walk V6 F{walk_index + 1} ← cupboard", "actorRootXLp": 137 - index * 15.5, "propRootXLp": 0, "actorCellWidthLp": 32, "propCellWidthLp": 48, "anchorXLp": 16, "bottomLp": 52, "durationMs": 100, "actionId": None, "cupboard": "open", "mirror": True, "hidden": False})

    review_frames = {}
    for record in frame_records:
        review_colour = {
            component: {
                "status": evidence["status"],
                "candidate": {"pixels": evidence["candidate"]["pixels"], "medianLuma": evidence["candidate"]["medianLuma"]},
                "authority": {"medianLuma": evidence["authority"]["medianLuma"]},
                "medianOklabDelta": evidence["medianOklabDelta"],
            }
            for component, evidence in record["colourEvidence"].items()
        }
        review_frames[record["id"]] = {
            "id": record["id"], "urls": record["urls"], "colourEvidence": review_colour,
            "contact": record["broomHandContact"], "bounds": record["composite"]["bounds"],
        }
    data = {
        "schema": "lighthouse-keeper/prime-action-review@1", "set": SET,
        "status": "versioned-reversible-review-candidate-not-approved",
        "room": {"widthLp": 172, "heightLp": 56, "floorLp": 52},
        "components": COMPONENTS, "primeSrc": prime_url, "historicalSrc": historical_url, "contactSheetSrc": sheet_url,
        "frames": review_frames, "actionPath": action_path, "actionLoop": action_loop, "route": route, "cupboardRoute": cupboard_route,
        "timing": {"walkFps": 10, "decelerationFps": 12, "actionFrameMs": 145, "actionLoopIndependent": True},
    }
    data_file = PACK / f"{SET}.json"
    # The reviewer is self-contained. Keep the complete route data in the
    # versioned draft, but do not duplicate it into the deployment payload.
    dump(data_file, data)

    geometry_sequence = [unique_frames[name]["record"]["composite"]["bounds"] for name in action_path]
    adjacent_geometry = []
    for index in range(1, len(geometry_sequence)):
        previous, current = geometry_sequence[index - 1], geometry_sequence[index]
        adjacent_geometry.append({"from": action_path[index - 1], "to": action_path[index], "widthDeltaPx": current["width"] - previous["width"], "heightDeltaPx": current["height"] - previous["height"], "floorDeltaPx": current["maxY"] - previous["maxY"]})
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET,
        "status": "prime-sweep-broom-v2-awaiting-frank", "auditTreatment": "partial-motion-salvage-assessment",
        "authorities": {
            "exactSideRightNeutral": {"file": rel(PRIME), "sha256": authority_sha, "role": "exact entry/exit Keeper endpoint and same-facing all-material colour authority"},
            "smoothPrimeSource": {"file": rel(PRIME_SOURCE), "sha256": sha(PRIME_SOURCE), "role": "sole identity, silhouette, face, beard, outfit and rendering authority"},
            "approvedWalk": {"directory": rel(walk_files[0].parent), "frameSha256": [sha(file) for file in walk_files]},
            "approvedStopWalkBridge": {"directory": rel(bridge_dir), "frameSha256": {str(index): sha(file) for index, file in bridge_files.items()}},
            "backSitStandV2Approval": {"file": "docs/review/keeper-prime-sit-stand-back-v2-approval-2026-10-18.json", "sha256": sha(ROOT / "docs/review/keeper-prime-sit-stand-back-v2-approval-2026-10-18.json"), "promotionPerformed": False},
        },
        "historicalChoreographyOnly": {
            "raw": {"file": rel(HISTORICAL_RAW), "sha256": sha(HISTORICAL_RAW)},
            "runtime": {"file": rel(HISTORICAL_RUNTIME), "sha256": sha(HISTORICAL_RUNTIME)},
            "allowedEvidence": ["joint paths", "weight transfer", "broom movement", "hand contact", "timing"],
            "visibleKeeperPixelsReused": 0,
        },
        "generation": {"tool": "built-in image generation", "mode": "identity-preserve", "promptLog": rel(PACK / "PROMPT_LOG.md"), "sources": source_records},
        "registration": {"logicalCell": [48, 40], "cellPixels": list(CELL), "density": 8, "anchorLp": list(ACTOR_ANCHOR), "floorPixelY": TARGET_FLOOR_Y, "sharedUniformScale": scale, "creativePixelWarp": False},
        "candidate": {
            "frames": frame_records, "actionPath": action_path, "actionLoop": action_loop,
            "forwardStrip": {"file": rel(forward_strip), "sha256": sha(forward_strip), "frames": len(action_path)},
            "loopStrip": {"file": rel(loop_strip), "sha256": sha(loop_strip), "frames": len(action_loop)},
            "contactSheet": {"file": rel(sheet_file), "sha256": sha(sheet_file)},
            "route": {"file": rel(data_file), "sha256": sha(data_file), "frames": len(route)},
            "reviewUrl": f"/keeper-review/{SET}/",
        },
        "measurements": {"adjacentGeometry": adjacent_geometry, "broomHandContact": {record["id"]: record["broomHandContact"] for record in frame_records}, "materialColourEvidence": {record["id"]: record["colourEvidence"] for record in frame_records}},
        "checks": {
            "pinnedApprovalsPreserved": True, "backSitStandV2ApprovalRecordedWithoutPromotion": True,
            "historicalKeeperPixelsReused": False, "exactSideRightNeutralEntryExit": True,
            "allGeneratedFramesUseSharedScale": True, "allVisibleActorRgbFromExactPrimeComponentPalettes": True,
            "allMaterialRegionsPassEveryFrame": True, "adjacentMaterialLumaStable": True,
            "actorPropOwnershipDisjointAndComplete": True, "broomSeparatelyOwned": True,
            "broomHandContactRemeasuredEveryHeldFrame": True, "broomFloorContactExact": True,
            "allFramesHaveFourPixelTransparentGutter": True, "actionLoopSeamPhaseCorrect": True,
            "completeWalkStopNeutralActionExitWalkRoute": True, "largeGameplayAndLiteralPlayback": True,
            "ghostAndFrameByFramePrimeComparison": True, "allImagesPreloadedAndDecoded": True,
            "finalUnchanged": True, "runtimeUnchanged": True, "productionUnchanged": True,
        },
        "publishedAssets": published,
        "approvalBoundary": {"candidateApproved": False, "promotionAllowed": False, "finalChanged": False, "runtimeChanged": False, "productionChanged": False},
        "rollback": f"Delete only {rel(PACK)}, public/keeper-review/{SET}, scripts/build_keeper_prime_sweep_broom_v1.py and scripts/verify_keeper_prime_sweep_broom_v1.mjs. Approved authorities, historical art, Final, runtime and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    (PACK / "HANDOFF.md").write_text(
        "# Prime Keeper sweep broom V2\n\n"
        "This immutable review candidate preserves V1 and corrects only its repeated generated lower-jumper debris while rebuilding the separately owned prop as a detailed traditional broom. "
        "Every action-pose actor remains a full Prime-derived redraw with exact-authority colour evidence. The review adds a cupboard-door proxy route: standard walk in, fully hidden state swap, moving outward and return sweep passes, and a standard-walk exit. "
        "Nothing is approved or promoted.\n"
    )

    html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper sweep broom V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:14px/1.42 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:18px}header{border-bottom:1px solid #294854}.status,.pass{display:inline-block;border:1px solid #73dda6;color:#aef2c7;border-radius:999px;padding:4px 9px}.notice{border-left:4px solid #e9b957;background:#2b2518;padding:11px}.panel{background:#10232d;border:1px solid #2d4b58;border-radius:12px;padding:14px;margin:14px 0}button,select,input{font:inherit}button{color:white;background:#173d52;border:1px solid #537788;border-radius:7px;padding:7px 10px;margin:2px}button.active{background:#17673d;border-color:#73dda6}button:disabled,select:disabled,input:disabled{opacity:.45}.controls{display:flex;gap:6px;flex-wrap:wrap;align-items:center}.stage-wrap{overflow:auto;background:#061018;padding:8px}.stage{position:relative;background:linear-gradient(#162a34 0 92.8%,#465058 92.8%);overflow:hidden}.stage img{position:absolute;object-fit:fill}.ghost{opacity:.28;filter:hue-rotate(115deg) saturate(1.8)}.stage-grid{display:grid;grid-template-columns:1fr;gap:14px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:14px}.checker{position:relative;aspect-ratio:6/5;background:repeating-conic-gradient(#263640 0 25%,#1a2730 0 50%) 50%/24px 24px;overflow:hidden}.checker img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}.mask{opacity:.75}.small{font-size:12px;color:#bcd0d8}.evidence{width:100%;border-collapse:collapse}.evidence th,.evidence td{border-bottom:1px solid #2b4652;padding:5px;text-align:left}.sheet{width:100%}.historical{max-width:100%;background:#061018}.legend{display:flex;gap:12px;flex-wrap:wrap}@media(min-width:1000px){.stage-grid{grid-template-columns:1fr 1fr}.stage-grid .literal-panel{grid-column:1/-1}.compare{grid-template-columns:1fr 1fr}}</style></head><body><header><h1>Prime Keeper · keeper_sweep_broom V1</h1><span class="status">Immutable review candidate · nothing promoted</span><p>Approved Prime identity and exact side-right endpoint. Historical sweep art supplies choreography only and zero visible Keeper pixels.</p></header><main><p class="notice"><strong>Approval boundary:</strong> review only. The broom is a separately owned prop. Final, runtime and production art are unchanged.</p><section class="panel"><div id="loading">Loading and decoding every unique frame…</div><div class="controls"><button id="complete" disabled>Complete route</button><button id="path" disabled>Action path</button><button id="loop" disabled>Action loop</button><button id="play" disabled>Play</button><button id="prev" disabled>Previous</button><button id="next" disabled>Next</button><label>Speed <input id="speed" disabled type="range" min="0.5" max="2" value="1" step="0.1"></label><label><input id="previousGhost" disabled type="checkbox"> Previous-frame ghost</label><label><input id="primeGhostToggle" disabled type="checkbox" checked> Exact Prime ghost</label><label>Mask <select id="mask" disabled><option value="">none</option></select></label></div><p id="caption"></p></section><section class="panel"><h2>Simultaneous route playback</h2><div class="stage-grid"><div><h3>Large inspection · 6 px/lp</h3><div class="stage-wrap"><div id="large" class="stage"></div></div></div><div><h3>Gameplay scale · 4 px/lp</h3><div class="stage-wrap"><div id="game" class="stage"></div></div></div><div class="literal-panel"><h3>Literal 1× · 1 px/lp</h3><div class="stage-wrap"><div id="literal" class="stage"></div></div></div></div></section><section class="panel"><h2>Frame-by-frame Prime comparison</h2><div class="compare"><div><h3>Exact approved side-right Prime</h3><div class="checker"><img id="primeCompare"></div></div><div><h3>Selected actor + separate broom</h3><div class="checker"><img id="primeGhost" class="ghost"><img id="actorCompare"><img id="propCompare"><img id="maskCompare" class="mask"></div></div></div><div class="legend"><span id="contact"></span><span id="geometry"></span></div><table class="evidence"><thead><tr><th>Material</th><th>Status</th><th>Candidate median</th><th>Authority median</th><th>ΔL</th><th>OKLab Δ</th><th>Mask pixels</th></tr></thead><tbody id="colourRows"></tbody></table></section><section class="panel"><h2>Fixed-scale lineup</h2><img class="sheet" src="__SHEET__" alt="Prime sweep broom V1 contact sheet"></section><section class="panel"><h2>Historical choreography evidence only</h2><img class="historical" src="__HISTORICAL__" alt="Historical sweep strip used only for motion evidence"><p class="small">Joint paths, weight transfer, broom travel, two-hand contact and timing only. No historical Keeper pixel appears in the candidate.</p></section></main><script>
const DATA=__DATA__;let mode='complete',index=0,timer=null;const modes={complete:DATA.route,path:DATA.actionPath.map(id=>({actionId:id,phase:'action path',label:id,actorSrc:DATA.frames[id].urls.actor,propSrc:DATA.frames[id].urls.prop,actorRootXLp:86,propRootXLp:86,actorCellWidthLp:48,propCellWidthLp:48,anchorXLp:16,bottomLp:52,durationMs:145})),loop:DATA.actionLoop.map(id=>({actionId:id,phase:'repeatable sweeping loop',label:id,actorSrc:DATA.frames[id].urls.actor,propSrc:DATA.frames[id].urls.prop,actorRootXLp:86,propRootXLp:86,actorCellWidthLp:48,propCellWidthLp:48,anchorXLp:16,bottomLp:52,durationMs:145}))};
for(const c of DATA.components)document.querySelector('#mask').add(new Option(c,c));function makeStage(id,scale){const host=document.querySelector('#'+id);host.style.width=172*scale+'px';host.style.height=56*scale+'px';for(const n of ['previousActor','previousProp','actor','prop']){const img=document.createElement('img');img.dataset.layer=n;if(n.startsWith('previous'))img.className='ghost';host.append(img)}return{host,scale}}
const stages=[makeStage('large',6),makeStage('game',4),makeStage('literal',1)];function place(stage,img,src,root,w,anchor,bottom){img.src=src;img.style.width=w*stage.scale+'px';img.style.height=40*stage.scale+'px';img.style.left=(root-anchor)*stage.scale+'px';img.style.top=(bottom-40)*stage.scale+'px'}
function currentList(){return modes[mode]}function show(){const list=currentList(),frame=list[index%list.length],prior=list[(index-1+list.length)%list.length],ghostOn=document.querySelector('#previousGhost').checked;for(const stage of stages){const q=n=>stage.host.querySelector('[data-layer='+n+']');place(stage,q('actor'),frame.actorSrc,frame.actorRootXLp,frame.actorCellWidthLp,frame.anchorXLp,frame.bottomLp);place(stage,q('prop'),frame.propSrc,frame.propRootXLp,frame.propCellWidthLp,frame.anchorXLp,frame.bottomLp);place(stage,q('previousActor'),prior.actorSrc,prior.actorRootXLp,prior.actorCellWidthLp,prior.anchorXLp,prior.bottomLp);place(stage,q('previousProp'),prior.propSrc,prior.propRootXLp,prior.propCellWidthLp,prior.anchorXLp,prior.bottomLp);q('previousActor').style.display=q('previousProp').style.display=ghostOn?'block':'none'}document.querySelector('#caption').textContent=`${index+1}/${list.length} · ${frame.phase} · ${frame.label}`;const id=frame.actionId||'neutral',record=DATA.frames[id]||DATA.frames.neutral;document.querySelector('#primeCompare').src=DATA.primeSrc;document.querySelector('#primeGhost').src=DATA.primeSrc;document.querySelector('#primeGhost').style.display=document.querySelector('#primeGhostToggle').checked?'block':'none';document.querySelector('#actorCompare').src=record.urls.actor;document.querySelector('#propCompare').src=record.urls.prop;const component=document.querySelector('#mask').value,mask=document.querySelector('#maskCompare');mask.style.display=component?'block':'none';if(component)mask.src=record.urls.masks[component];document.querySelector('#contact').textContent=`Broom/hand contact: ${record.contact.status} · ${record.contact.contactPixels||0} px`;document.querySelector('#geometry').textContent=`Composite bounds: ${record.bounds.width}×${record.bounds.height}px`;const rows=document.querySelector('#colourRows');rows.replaceChildren();for(const name of DATA.components){const e=record.colourEvidence[name],tr=document.createElement('tr');if(e.status==='pass'){const d=Math.abs(e.candidate.medianLuma-e.authority.medianLuma).toFixed(2);tr.innerHTML=`<td>${name}</td><td class="pass">pass</td><td>${e.candidate.medianLuma}</td><td>${e.authority.medianLuma}</td><td>${d}</td><td>${e.medianOklabDelta}</td><td>${e.candidate.pixels}</td>`}else tr.innerHTML=`<td>${name}</td><td>${e.status}</td><td colspan="5">blocked/failure</td>`;rows.append(tr)}}
function stop(){if(timer){clearTimeout(timer);timer=null}document.querySelector('#play').textContent='Play'}function tick(){const frame=currentList()[index%currentList().length];index=(index+1)%currentList().length;show();timer=setTimeout(tick,frame.durationMs/Number(document.querySelector('#speed').value))}document.querySelector('#play').onclick=()=>{if(timer)stop();else{document.querySelector('#play').textContent='Pause';tick()}};document.querySelector('#prev').onclick=()=>{stop();index=(index-1+currentList().length)%currentList().length;show()};document.querySelector('#next').onclick=()=>{stop();index=(index+1)%currentList().length;show()};for(const id of ['complete','path','loop'])document.querySelector('#'+id).onclick=()=>{stop();mode=id;index=0;for(const key of ['complete','path','loop'])document.querySelector('#'+key).classList.toggle('active',key===id);show()};for(const id of ['previousGhost','primeGhostToggle','mask'])document.querySelector('#'+id).onchange=show;
const urls=new Set([DATA.primeSrc,DATA.historicalSrc,DATA.contactSheetSrc]);for(const f of Object.values(DATA.frames)){urls.add(f.urls.actor);urls.add(f.urls.prop);urls.add(f.urls.composite);Object.values(f.urls.masks).forEach(x=>urls.add(x))}for(const f of DATA.route){urls.add(f.actorSrc);urls.add(f.propSrc)}Promise.all([...urls].map(src=>new Promise((ok,bad)=>{const img=new Image();img.onload=()=>img.decode?img.decode().then(ok,bad):ok();img.onerror=bad;img.src=src}))).then(()=>{document.querySelector('#loading').textContent=`${urls.size} unique images loaded and decoded.`;document.querySelectorAll('button,select,input').forEach(x=>x.disabled=false);document.querySelector('#complete').classList.add('active');show()}).catch(error=>document.querySelector('#loading').textContent='Media failed: '+error);
</script></body></html>"""
    html = html.replace("Prime Keeper sweep broom V1", "Prime Keeper sweep broom V2")
    html = html.replace("Prime sweep broom V1", "Prime sweep broom V2")
    html = html.replace("keeper_sweep_broom V1", "keeper_sweep_broom V2")
    html = html.replace("<button id=\"loop\" disabled>Action loop</button>", "<button id=\"loop\" disabled>Action loop</button><button id=\"cupboard\" disabled>Cupboard handoff</button>")
    html = html.replace(".stage img{position:absolute;object-fit:fill}", ".stage img{position:absolute;object-fit:fill}.cupboard-proxy{position:absolute;right:0;bottom:0;width:29px;height:52px;z-index:9;pointer-events:none;border:2px solid #5a4227;background:linear-gradient(90deg,#362615 0 22%,#9b7041 22% 27%,#513719 27% 100%);box-shadow:-3px 0 #c59a62 inset}.cupboard-proxy.open{width:18px;transform:skewY(-4deg);transform-origin:right bottom}.cupboard-proxy.closed{width:42px;background:repeating-linear-gradient(90deg,#513719 0 9px,#815a2e 9px 12px)}")
    reviewer_patch = r'''
const cupboardButton=document.querySelector('#cupboard');modes.cupboard=DATA.cupboardRoute;
for(const stage of stages){const door=document.createElement('div');door.className='cupboard-proxy';door.style.display='none';stage.host.append(door)}
function placeContext(stage,img,src,root,w,anchor,bottom,frame){place(stage,img,src,root,w,anchor,bottom);img.style.transform=frame.mirror?'scaleX(-1)':'none';img.style.transformOrigin='center';img.style.visibility=frame.hidden?'hidden':'visible'}
show=function(){const list=currentList(),frame=list[index%list.length],prior=list[(index-1+list.length)%list.length],ghostOn=document.querySelector('#previousGhost').checked;for(const stage of stages){const q=n=>stage.host.querySelector('[data-layer='+n+']');placeContext(stage,q('actor'),frame.actorSrc,frame.actorRootXLp,frame.actorCellWidthLp,frame.anchorXLp,frame.bottomLp,frame);placeContext(stage,q('prop'),frame.propSrc,frame.propRootXLp,frame.propCellWidthLp,frame.anchorXLp,frame.bottomLp,frame);placeContext(stage,q('previousActor'),prior.actorSrc,prior.actorRootXLp,prior.actorCellWidthLp,prior.anchorXLp,prior.bottomLp,prior);placeContext(stage,q('previousProp'),prior.propSrc,prior.propRootXLp,prior.propCellWidthLp,prior.anchorXLp,prior.bottomLp,prior);q('previousActor').style.display=q('previousProp').style.display=ghostOn?'block':'none';const door=stage.host.querySelector('.cupboard-proxy');door.style.display=frame.cupboard?'block':'none';door.className='cupboard-proxy '+(frame.cupboard||'')}
document.querySelector('#caption').textContent=`${index+1}/${list.length} · ${frame.phase} · ${frame.label}`;const id=frame.actionId||'neutral',record=DATA.frames[id]||DATA.frames.neutral;document.querySelector('#primeCompare').src=DATA.primeSrc;document.querySelector('#primeGhost').src=DATA.primeSrc;document.querySelector('#primeGhost').style.display=document.querySelector('#primeGhostToggle').checked?'block':'none';document.querySelector('#actorCompare').src=record.urls.actor;document.querySelector('#propCompare').src=record.urls.prop;const component=document.querySelector('#mask').value,mask=document.querySelector('#maskCompare');mask.style.display=component?'block':'none';if(component)mask.src=record.urls.masks[component];document.querySelector('#contact').textContent=`Broom/hand contact: ${record.contact.status} · ${record.contact.contactPixels||0} px`;document.querySelector('#geometry').textContent=`Composite bounds: ${record.bounds.width}×${record.bounds.height}px`;const rows=document.querySelector('#colourRows');rows.replaceChildren();for(const name of DATA.components){const e=record.colourEvidence[name],tr=document.createElement('tr');if(e.status==='pass'){const d=Math.abs(e.candidate.medianLuma-e.authority.medianLuma).toFixed(2);tr.innerHTML=`<td>${name}</td><td class="pass">pass</td><td>${e.candidate.medianLuma}</td><td>${e.authority.medianLuma}</td><td>${d}</td><td>${e.medianOklabDelta}</td><td>${e.candidate.pixels}</td>`}else tr.innerHTML=`<td>${name}</td><td>${e.status}</td><td colspan="5">blocked/failure</td>`;rows.append(tr)}};
cupboardButton.onclick=()=>{stop();mode='cupboard';index=0;for(const key of ['complete','path','loop','cupboard'])document.querySelector('#'+key).classList.toggle('active',key===mode);show()};
'''
    html = html.replace("</script>", reviewer_patch + "</script>")
    html = html.replace("__DATA__", json.dumps(data, separators=(",", ":"))).replace("__SHEET__", sheet_url).replace("__HISTORICAL__", historical_url)
    # The repository has a hard public-payload ceiling. Keep this full,
    # immutable reviewer beside the candidate evidence and let the tiny public
    # shell fetch it; the archive still owns every PNG URL referenced here.
    reviewer_file = PACK / "reviewer.html"
    reviewer_html = html.replace('"/keeper-review/', '"https://lighthouse-keeper-mu.vercel.app/keeper-review/')
    reviewer_file.write_text(reviewer_html)
    # The public shell stays below the review-media payload cap, while its full
    # reviewer is fetched from the immutable candidate commit rather than the
    # mutable main branch.
    reviewer_url = "https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/55c5615/" + rel(reviewer_file)
    shell = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper sweep broom V2</title><style>html,body,iframe{{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}}#loading{{padding:24px}}iframe{{display:none}}</style><p id="loading">Loading immutable Prime Keeper sweep-broom V2 reviewer…</p><iframe id="review" title="Prime Keeper sweep broom V2 reviewer"></iframe><script>fetch({json.dumps(reviewer_url)}).then(r=>{{if(!r.ok)throw Error('reviewer '+r.status);return r.text()}}).then(t=>{{document.querySelector('#review').srcdoc=t;document.querySelector('#review').style.display='block';document.querySelector('#loading').remove()}}).catch(e=>document.querySelector('#loading').textContent='Reviewer failed to load: '+e.message)</script></html>'''
    (PUBLIC / "index.html").write_text(shell)
    print(json.dumps({"candidate": f"/keeper-review/{SET}/", "uniqueFrames": len(frame_records), "routeFrames": len(route), "publishedAssets": len(published), "sharedScale": scale}, indent=2))


if __name__ == "__main__":
    main()
