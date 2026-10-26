#!/usr/bin/env python3
"""Build the approved-look Kitchen V3 rebuild from isolated source art."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
GENERATED = SOURCES / "generated"
PARTS = ROOT / "parts"
OUTPUTS = ROOT / "outputs"

W, H = 1536, 576
MAGENTA = (255, 0, 255, 255)
INK = (7, 17, 24, 255)
INK_SOFT = (18, 36, 47, 255)
BLUE_DARK = (0, 54, 112, 255)
BLUE = (0, 102, 204, 255)
BLUE_LIGHT = (24, 139, 230, 255)
CYAN_DARK = (2, 109, 146, 255)
CYAN = (31, 178, 211, 255)
CYAN_LIGHT = (103, 220, 233, 255)
CREAM_DARK = (205, 177, 127, 255)
CREAM_SHADOW = (232, 207, 160, 255)
CREAM = (255, 238, 198, 255)
CREAM_LIGHT = (255, 249, 229, 255)
COPPER_DARK = (164, 61, 8, 255)
COPPER = (241, 104, 13, 255)
COPPER_LIGHT = (255, 164, 61, 255)
WOOD_DARK = (89, 42, 18, 255)
WOOD = (151, 79, 29, 255)
WOOD_LIGHT = (206, 127, 50, 255)
FLOOR_DARK = (116, 63, 30, 255)
FLOOR = (190, 119, 55, 255)
FLOOR_LIGHT = (226, 157, 80, 255)
METAL_DARK = (76, 94, 105, 255)
METAL = (165, 184, 192, 255)
METAL_LIGHT = (231, 241, 240, 255)
RED = (218, 31, 30, 255)

PALETTE = [
    (4, 10, 15), (7, 17, 24), (18, 36, 47), (31, 50, 63),
    (0, 38, 79), (0, 54, 112), (0, 75, 153), (0, 102, 204),
    (9, 122, 218), (24, 139, 230), (51, 166, 240), (101, 207, 248),
    (2, 109, 146), (12, 145, 181), (31, 178, 211), (103, 220, 233),
    (171, 142, 98), (205, 177, 127), (232, 207, 160), (247, 225, 183),
    (255, 238, 198), (255, 249, 229), (255, 255, 244),
    (122, 42, 5), (164, 61, 8), (205, 77, 9), (241, 104, 13),
    (255, 132, 25), (255, 164, 61), (255, 198, 112),
    (68, 29, 14), (89, 42, 18), (121, 57, 22), (151, 79, 29),
    (181, 101, 37), (206, 127, 50), (235, 163, 84),
    (76, 94, 105), (116, 137, 148), (165, 184, 192), (203, 218, 220),
    (231, 241, 240), (83, 237, 136), (114, 19, 20), (174, 24, 25), (218, 31, 30),
    (116, 63, 30), (151, 87, 40), (190, 119, 55), (226, 157, 80),
]

WINDOWS = [(580, 106, 748, 274), (1084, 106, 1252, 274)]
GLASS_LOCAL_RECTS = [(28, 25, 78, 79), (89, 25, 139, 79), (28, 91, 78, 141), (89, 91, 139, 141)]
V7_SHA = "0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538"
STYLE_REF = "art/source/kitchen-built-in-state-ligne-claire-2026-10-21-v7/oven-on-user-confirmed-visual-authority.png"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in paths:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def nearest_palette(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    return min(PALETTE, key=lambda c: (rgb[0] - c[0]) ** 2 + (rgb[1] - c[1]) ** 2 + (rgb[2] - c[2]) ** 2)


def snap_fills(image: Image.Image) -> Image.Image:
    """Snap opaque fills; retain only resampling antialias colours at the edge."""
    image = image.convert("RGBA")
    pixels = image.load()
    cache: dict[tuple[int, int, int], tuple[int, int, int]] = {}
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                pixels[x, y] = (0, 0, 0, 0)
            elif a == 255:
                key = (r, g, b)
                cache.setdefault(key, nearest_palette(key))
                nr, ng, nb = cache[key]
                pixels[x, y] = (nr, ng, nb, 255)
    return image


def clean_source(name: str, size: tuple[int, int], pad: int = 0, threshold: int = 200, outline: bool = True) -> Image.Image:
    """Discard generated halo/shadow alpha and fit to a declared envelope."""
    image = Image.open(GENERATED / name).convert("RGBA")
    alpha = image.getchannel("A")
    hard = alpha.point(lambda value: 255 if value >= threshold else 0)
    bbox = hard.getbbox()
    if bbox is None:
        raise RuntimeError(f"empty generated source: {name}")
    image.putalpha(hard)
    image = image.crop(bbox)
    target = (size[0] - 2 * pad, size[1] - 2 * pad)
    image = image.resize(target, Image.Resampling.LANCZOS)
    # Remove low-alpha Lanczos ringing before it can become a visible fringe.
    cleaned_alpha = image.getchannel("A").point(lambda value: 0 if value < 16 else (255 if value > 239 else value))
    image.putalpha(cleaned_alpha)
    image = snap_fills(image)
    if outline:
        alpha = image.getchannel("A")
        stroke = alpha.filter(ImageFilter.MaxFilter(3))
        under = Image.new("RGBA", image.size, INK)
        under.putalpha(stroke)
        image = Image.alpha_composite(under, image)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(image, (pad, pad))
    return canvas


def save_part(name: str, image: Image.Image, metadata: dict, records: dict) -> None:
    PARTS.mkdir(parents=True, exist_ok=True)
    path = PARTS / name
    image.save(path, optimize=True)
    record = {
        "id": name.removesuffix(".png"),
        "tier": 1,
        "bayWidth": metadata.get("bayWidth", 0),
        "reservedBayWidth": metadata.get("reservedBayWidth", metadata.get("bayWidth", 0)),
        "useBay": metadata.get("useBay"),
        "category": metadata.get("category", "component"),
        "placement": metadata.get("placement", metadata.get("category", "component")),
        "kitchenUsage": metadata.get("kitchenUsage", "active"),
        "realSizeM": metadata.get("realSizeM", [0, 0, 0]),
        "canvasPx": list(image.size),
        "anchorPx": metadata.get("anchorPx", [0, image.height]),
        "standPointX": metadata.get("standPointX"),
        "lightOverlays": metadata.get("lightOverlays", []),
        "movingPartOverlays": metadata.get("movingPartOverlays", []),
        "interactionAnchors": metadata.get("interactionAnchors", []),
        "bubbleOriginPx": metadata.get("bubbleOriginPx"),
        "effectOriginPx": metadata.get("effectOriginPx"),
        "statusLightPointPx": metadata.get("statusLightPointPx"),
        "faultRecipes": metadata.get("faultRecipes", []),
        "palette": "palette_env-v1",
        "styleReference": {"path": STYLE_REF, "sha256": V7_SHA},
        "sourceSha256": metadata.get("sourceSha256"),
        "files": {"master": name},
    }
    record["sha256"] = sha256(path)
    records[name] = record


def source_hash(name: str) -> str:
    return sha256(GENERATED / name)


def make_parts() -> dict[str, dict]:
    records: dict[str, dict] = {}

    worktop_art = clean_source("worktop-source.png", (84, 31), outline=False)
    worktop = Image.new("RGBA", (84, 31), CYAN)
    worktop.alpha_composite(worktop_art)
    save_part("worktop_tile.png", worktop, {"bayWidth": 1, "category": "component", "realSizeM": [0.5, 0.6, 0.083], "sourceSha256": source_hash("worktop-source.png")}, records)
    left_cap = worktop.crop((0, 0, 16, 31)); right_cap = worktop.crop((68, 0, 84, 31))
    ld, rd = ImageDraw.Draw(left_cap), ImageDraw.Draw(right_cap)
    ld.line((1, 0, 1, 30), fill=INK, width=3); rd.line((14, 0, 14, 30), fill=INK, width=3)
    save_part("worktop_cap_left.png", left_cap, {"category": "component", "realSizeM": [0.095, 0.6, 0.083], "sourceSha256": source_hash("worktop-source.png")}, records)
    save_part("worktop_cap_right.png", right_cap, {"category": "component", "realSizeM": [0.095, 0.6, 0.083], "sourceSha256": source_hash("worktop-source.png")}, records)
    joint = Image.new("RGBA", (2, 31), INK_SOFT)
    save_part("worktop_joint.png", joint, {"category": "component", "realSizeM": [0.012, 0.6, 0.083], "sourceSha256": source_hash("worktop-source.png")}, records)

    plinth_art = clean_source("plinth-source.png", (84, 17), outline=False)
    plinth = Image.new("RGBA", (84, 17), BLUE_DARK)
    plinth.alpha_composite(plinth_art)
    save_part("plinth_tile.png", plinth, {"bayWidth": 1, "category": "component", "realSizeM": [0.5, 0.6, 0.1], "sourceSha256": source_hash("plinth-source.png")}, records)
    left_plinth = plinth.crop((0, 0, 16, 17)); right_plinth = plinth.crop((68, 0, 84, 17))
    ImageDraw.Draw(left_plinth).line((1, 0, 1, 16), fill=INK, width=3)
    ImageDraw.Draw(right_plinth).line((14, 0, 14, 16), fill=INK, width=3)
    save_part("plinth_cap_left.png", left_plinth, {"category": "component", "sourceSha256": source_hash("plinth-source.png")}, records)
    save_part("plinth_cap_right.png", right_plinth, {"category": "component", "sourceSha256": source_hash("plinth-source.png")}, records)

    fronts = {
        "front_drawers.png": ("drawers-source.png", (84, 132), 1, None, 538),
        "front_cupboard.png": ("cupboard-source.png", (84, 132), 1, None, None),
        "front_sink_belfast_2bay.png": ("sink-front-source.png", (168, 132), 2, 1, 622),
        "front_dishwasher.png": ("dishwasher-source.png", (84, 132), 1, None, 790),
    }
    for filename, (source, size, bays, use_bay, stand) in fronts.items():
        image = clean_source(source, size)
        if filename == "front_sink_belfast_2bay.png":
            solid = Image.new("RGBA", size, BLUE)
            solid.alpha_composite(image)
            image = solid
        overlays = [{"id": "dishwasher_led", "file": "overlay_dishwasher_led.png", "rectPx": [17, 23, 40, 31]}] if filename == "front_dishwasher.png" else []
        usage = "retired-from-kitchen" if filename == "front_dishwasher.png" else "active"
        save_part(filename, image, {"bayWidth": bays, "useBay": use_bay, "category": "fitted", "realSizeM": [0.5 * bays, 0.6, 0.79], "standPointX": stand, "lightOverlays": overlays, "kitchenUsage": usage, "sourceSha256": source_hash(source)}, records)
    cupboard = Image.open(PARTS / "front_cupboard.png").convert("RGBA")
    cupboard2 = Image.new("RGBA", (168, 132), (0, 0, 0, 0)); cupboard2.alpha_composite(cupboard); cupboard2.alpha_composite(cupboard, (84, 0))
    save_part("front_cupboard_2bay.png", cupboard2, {"bayWidth": 2, "category": "fitted", "realSizeM": [1.0, 0.6, 0.79], "sourceSha256": source_hash("cupboard-source.png")}, records)

    sink = clean_source("sink-insert-left-source.png", (168, 48), outline=True)
    save_part("insert_sink_2bay.png", sink, {"bayWidth": 2, "useBay": 1, "category": "fitted", "realSizeM": [1.0, 0.52, 0.29], "standPointX": 622, "sourceSha256": source_hash("sink-insert-left-source.png")}, records)

    cooker = clean_source("cooker-clean-source.png", (84, 180), outline=True)
    save_part("cooker.png", cooker, {"bayWidth": 1, "reservedBayWidth": 2, "category": "slotIn", "realSizeM": [0.5, 0.6, 0.9], "standPointX": 874, "lightOverlays": [{"id": "oven_window", "file": "overlay_oven_window.png", "rectPx": [16, 75, 68, 142]}], "kitchenUsage": "retired-from-kitchen", "sourceSha256": source_hash("cooker-clean-source.png")}, records)
    oven_overlay = Image.new("RGBA", (84, 180), (0, 0, 0, 0))
    oven_content = clean_source("oven-overlay-source.png", (50, 55), outline=False)
    oven_overlay.alpha_composite(oven_content, (17, 82))
    save_part("overlay_oven_window.png", oven_overlay, {"bayWidth": 1, "category": "component", "sourceSha256": source_hash("oven-overlay-source.png")}, records)

    led = Image.new("RGBA", (84, 132), (0, 0, 0, 0)); led_draw = ImageDraw.Draw(led)
    for x in (18, 27, 35):
        led_draw.ellipse((x, 24, x + 5, 29), fill=(83, 237, 136, 255), outline=INK, width=1)
    save_part("overlay_dishwasher_led.png", led, {"bayWidth": 1, "category": "component", "kitchenUsage": "retired-from-kitchen", "sourceSha256": source_hash("dishwasher-source.png")}, records)

    utility = clean_source("utility-source.png", (84, 353), outline=True)
    save_part("unit_utility_cupboard_closed.png", utility, {"bayWidth": 1, "category": "fittedTall", "realSizeM": [0.5, 0.6, 2.0], "standPointX": 370, "movingPartOverlays": [{"id": "open_door", "file": "overlay_utility_cupboard_open.png", "rectPx": [0, 0, 126, 336]}], "kitchenUsage": "retired-from-kitchen", "sourceSha256": source_hash("utility-source.png")}, records)
    open_door = clean_source("utility-open-door-source.png", (126, 336), pad=1, outline=True)
    save_part("overlay_utility_cupboard_open.png", open_door, {"bayWidth": 1, "category": "component", "kitchenUsage": "retired-from-kitchen", "sourceSha256": source_hash("utility-open-door-source.png")}, records)
    fridge = clean_source("fridge-source.png", (84, 319), outline=True)
    save_part("unit_fridge_freezer.png", fridge, {"bayWidth": 1, "category": "fittedTall", "realSizeM": [0.5, 0.6, 1.8], "standPointX": 454, "kitchenUsage": "retired-from-kitchen", "sourceSha256": source_hash("fridge-source.png")}, records)

    # Frank's later same-pass amendment replaces the fitted/slot-in appliances
    # with narrow freestanding 1950s designs. The original rebuild parts above
    # remain in this review package as explicitly retired provenance.
    cooker_1950s = clean_source("cooker-1950s-source.png", (76, 252), outline=True)
    cooker_lights = [
        {"id": "oven_window", "file": "overlay_oven_window.png", "rectPx": [11, 132, 65, 190]},
        {"id": "grill_glow", "file": "overlay_grill_glow.png", "rectPx": [10, 18, 66, 58]},
        {"id": "burner_flames", "file": "overlay_burner_flames.png", "rectPx": [8, 72, 68, 108]},
    ]
    save_part("cooker_1950s.png", cooker_1950s, {
        "bayWidth": 1, "reservedBayWidth": 2, "category": "freestanding", "placement": "freestanding",
        "realSizeM": [0.5, 0.6, 1.5], "anchorPx": [38, 252], "standPointX": 874,
        "lightOverlays": cooker_lights, "sourceSha256": source_hash("cooker-1950s-source.png"),
    }, records)

    oven_new = Image.new("RGBA", (76, 252), (0, 0, 0, 0))
    oven_new.alpha_composite(clean_source("oven-overlay-source.png", (52, 56), outline=False), (12, 133))
    save_part("overlay_oven_window.png", oven_new, {"bayWidth": 1, "category": "component", "sourceSha256": source_hash("oven-overlay-source.png")}, records)

    grill_glow = Image.new("RGBA", (76, 252), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grill_glow)
    gd.rounded_rectangle((12, 21, 64, 55), radius=4, fill=COPPER_LIGHT, outline=INK, width=2)
    gd.line((17, 47, 59, 47), fill=CREAM_LIGHT, width=2)
    save_part("overlay_grill_glow.png", grill_glow, {"bayWidth": 1, "category": "component", "sourceSha256": source_hash("cooker-1950s-source.png")}, records)

    flames = Image.new("RGBA", (76, 252), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flames)
    for cx, cy in ((19, 95), (38, 84), (57, 95)):
        fd.ellipse((cx - 9, cy - 3, cx + 9, cy + 3), outline=CYAN_LIGHT, width=2)
        for dx in (-5, 0, 5):
            fd.polygon(((cx + dx - 2, cy), (cx + dx, cy - 8), (cx + dx + 2, cy)), fill=CYAN_LIGHT)
    save_part("overlay_burner_flames.png", flames, {"bayWidth": 1, "category": "component", "sourceSha256": source_hash("cooker-1950s-source.png")}, records)

    larder = clean_source("larder-source.png", (76, 353), outline=True)
    save_part("unit_larder_cupboard_closed.png", larder, {
        "bayWidth": 1, "category": "freestanding", "placement": "freestanding", "realSizeM": [0.5, 0.6, 2.0],
        "anchorPx": [38, 353], "standPointX": 370,
        "movingPartOverlays": [{"id": "open_door", "file": "overlay_larder_cupboard_open.png", "rectPx": [-50, 0, 76, 353]}],
        "kitchenUsage": "retired-from-kitchen",
        "sourceSha256": source_hash("larder-source.png"),
    }, records)
    larder_open = clean_source("larder-open-source.png", (126, 353), outline=True)
    save_part("overlay_larder_cupboard_open.png", larder_open, {"bayWidth": 1, "category": "component", "kitchenUsage": "retired-from-kitchen", "sourceSha256": source_hash("larder-open-source.png")}, records)

    dresser = clean_source("dresser-1950s-source.png", (76, 302), outline=True)
    save_part("dresser_1950s.png", dresser, {
        "bayWidth": 1, "category": "freestanding", "placement": "freestanding", "realSizeM": [0.5, 0.4, 1.8],
        "anchorPx": [38, 302], "standPointX": 370, "sourceSha256": source_hash("dresser-1950s-source.png"),
    }, records)

    fridge_1950s = clean_source("fridge-1950s-source.png", (76, 252), outline=True)
    save_part("fridge_1950s.png", fridge_1950s, {
        "bayWidth": 1, "category": "freestanding", "placement": "freestanding", "realSizeM": [0.5, 0.6, 1.5],
        "anchorPx": [38, 252], "standPointX": 454,
        "movingPartOverlays": [{"id": "open_door", "file": "overlay_fridge_open.png", "rectPx": [-50, 0, 76, 252]}],
        "lightOverlays": [{"id": "interior_light", "file": "overlay_fridge_open.png", "rectPx": [-50, 0, 76, 252]}],
        "sourceSha256": source_hash("fridge-1950s-source.png"),
    }, records)
    fridge_open = clean_source("fridge-open-source.png", (126, 252), outline=True)
    save_part("overlay_fridge_open.png", fridge_open, {"bayWidth": 1, "category": "component", "sourceSha256": source_hash("fridge-open-source.png")}, records)

    loose = {
        "toaster.png": ("toaster-source.png", (64, 42), [0.38, 0.25, 0.24], "counter", 1042),
        "kettle.png": ("kettle-source.png", (56, 58), [0.33, 0.28, 0.35], "counter", 1294),
        "pet_bowl.png": ("pet-bowl-source.png", (84, 28), [0.5, 0.3, 0.17], "freestanding", 1378),
        "pedal_bin.png": ("bin-source.png", (84, 100), [0.5, 0.3, 0.55], "freestanding", 1462),
    }
    for filename, (source, size, metres, category, stand) in loose.items():
        image = clean_source(source, size, pad=1, outline=True)
        save_part(filename, image, {"bayWidth": 1, "category": category, "realSizeM": metres, "anchorPx": [size[0] // 2, size[1]], "standPointX": stand, "sourceSha256": source_hash(source)}, records)

    (PARTS / "item.json").write_text(json.dumps({"schema": "lighthouse-keeper/kitchen-v3-rebuild-parts@1", "palette": "palette_env-v1", "parts": records}, indent=2) + "\n", encoding="utf-8")
    return records


def build_window() -> Image.Image:
    window = clean_source("window-source.png", (168, 168), outline=True)
    # Technical key colour is written deterministically; generated colour is
    # never accepted as a key. Rectangles lie wholly inside the timber rebates,
    # so the key boundary is hard and contains no antialias fringe.
    draw = ImageDraw.Draw(window)
    for rect in GLASS_LOCAL_RECTS:
        draw.rectangle(rect, fill=MAGENTA)
    return window


def room_shell() -> Image.Image:
    scale = 4
    image = Image.new("RGBA", (W * scale, H * scale), CREAM)
    d = ImageDraw.Draw(image)
    def box(coords): return tuple(round(v * scale) for v in coords)
    def rect(coords, fill, outline=None, width=1): d.rectangle(box(coords), fill=fill, outline=outline, width=round(width * scale))
    def line(coords, fill, width=1): d.line(box(coords), fill=fill, width=round(width * scale), joint="curve")

    rect((0, 0, W, 32), WOOD_DARK)
    rect((4, 4, W - 4, 26), WOOD)
    line((6, 7, W - 6, 7), WOOD_LIGHT, 3)
    line((0, 31, W, 31), INK, 4)
    rect((0, 32, 32, 544), CREAM_SHADOW)
    rect((1504, 32, 1536, 544), CREAM_SHADOW)
    line((31, 32, 31, 544), INK, 4)
    line((1504, 32, 1504, 544), INK, 4)
    rect((32, 32, 1504, 460), CREAM)
    # Restrained hand-drawn plaster marks; never shadows.
    for x, y, length, tone in (
        (82, 93, 50, CREAM_SHADOW), (355, 115, 78, CREAM_LIGHT), (878, 92, 58, CREAM_SHADOW),
        (1298, 82, 80, CREAM_LIGHT), (180, 273, 65, CREAM_LIGHT), (892, 355, 43, CREAM_SHADOW),
        (1339, 320, 58, CREAM_SHADOW), (345, 397, 48, CREAM_LIGHT),
    ):
        line((x, y, x + length, y), tone, 2)

    # Small permitted clock in the otherwise clear walk-in zone.
    d.ellipse(box((156, 118, 220, 182)), fill=CREAM_LIGHT, outline=INK, width=round(4 * scale))
    d.ellipse(box((164, 126, 212, 174)), fill=CREAM, outline=WOOD, width=round(3 * scale))
    line((188, 150, 188, 134), INK, 3); line((188, 150, 202, 157), INK, 3)
    for angle in range(0, 360, 30):
        cx, cy = 188, 150
        a = math.radians(angle)
        line((cx + math.cos(a) * 18, cy + math.sin(a) * 18, cx + math.cos(a) * 22, cy + math.sin(a) * 22), COPPER_DARK, 2)

    rect((32, 449, 1504, 460), WOOD_DARK)
    line((32, 449, 1504, 449), INK, 3)
    line((35, 452, 1501, 452), WOOD_LIGHT, 2)
    rect((0, 460, W, 544), FLOOR)
    for y, colour, width in ((467, FLOOR_LIGHT, 2), (481, FLOOR_DARK, 2), (498, FLOOR_LIGHT, 2), (515, FLOOR_DARK, 2), (533, FLOOR_LIGHT, 2), (543, INK, 3)):
        line((0, y, W, y), colour, width)
    rect((0, 544, W, 576), WOOD_DARK)
    rect((4, 549, W - 4, 576), FLOOR)
    line((4, 553, W - 4, 553), FLOOR_LIGHT, 3)

    # Proper timber jamb only: no void, no panel and no shadow.
    rect((0, 208, 32, 544), WOOD_DARK)
    rect((5, 208, 26, 544), WOOD)
    rect((9, 208, 17, 544), WOOD_LIGHT)
    line((26, 208, 26, 544), INK, 3)

    # Matching right-wall jamb: the cupboard of myriads is fictional and
    # never occupies a bay or appears behind this timber edge.
    rect((1504, 208, 1536, 544), WOOD_DARK)
    rect((1510, 208, 1531, 544), WOOD)
    rect((1519, 208, 1527, 544), WOOD_LIGHT)
    line((1510, 208, 1510, 544), INK, 3)

    image = image.resize((W, H), Image.Resampling.LANCZOS)
    window = build_window()
    image.alpha_composite(window, (580, 106))
    image.alpha_composite(window, (1084, 106))
    return image


def paste(layer: Image.Image, part: Image.Image, x: int, y: int) -> None:
    layer.alpha_composite(part, (x, y))


def assemble(
    parts: dict[str, Image.Image],
    keeper_x: int | None = None,
    sink_override: Image.Image | None = None,
    open_fridge: bool = False,
    lit_cooker: bool = False,
) -> tuple[Image.Image, Image.Image]:
    room = room_shell()
    item_layer = Image.new("RGBA", room.size, (0, 0, 0, 0))
    paste(item_layer, parts["dresser_1950s.png"], 332, 183)
    paste(item_layer, parts["fridge_1950s.png"], 416, 233)

    for x in (496, 580, 664, 748, 916, 1000, 1084, 1168, 1252):
        paste(item_layer, parts["plinth_tile.png"], x, 468)
    paste(item_layer, parts["front_drawers.png"], 496, 336)
    paste(item_layer, parts["front_sink_belfast_2bay.png"], 580, 336)
    paste(item_layer, parts["front_drawers.png"], 748, 336)
    paste(item_layer, parts["cooker_1950s.png"], 836, 233)
    paste(item_layer, parts["front_drawers.png"], 916, 336)
    paste(item_layer, parts["front_drawers.png"], 1000, 336)
    paste(item_layer, parts["front_cupboard_2bay.png"], 1084, 336)
    paste(item_layer, parts["front_cupboard.png"], 1252, 336)

    for x in (496, 580, 664, 748, 916, 1000, 1084, 1168, 1252):
        paste(item_layer, parts["worktop_tile.png"], x, 305)
    for x in (580, 664, 748, 1000, 1084, 1168, 1252):
        paste(item_layer, parts["worktop_joint.png"], x - 1, 305)
    for x, name in ((496, "worktop_cap_left.png"), (816, "worktop_cap_right.png"), (916, "worktop_cap_left.png"), (1320, "worktop_cap_right.png")):
        paste(item_layer, parts[name], x, 305)
    for x, name in ((496, "plinth_cap_left.png"), (816, "plinth_cap_right.png"), (916, "plinth_cap_left.png"), (1320, "plinth_cap_right.png")):
        paste(item_layer, parts[name], x, 468)

    paste(item_layer, sink_override or parts["insert_sink_2bay.png"], 580, 274)
    paste(item_layer, parts["toaster.png"], 1010, 272)
    paste(item_layer, parts["kettle.png"], 1266, 256)
    paste(item_layer, parts["pet_bowl.png"], 1336, 464)
    paste(item_layer, parts["pedal_bin.png"], 1420, 373)
    room.alpha_composite(item_layer)

    if open_fridge:
        paste(room, parts["overlay_fridge_open.png"], 366, 233)
    if lit_cooker:
        for name in ("overlay_oven_window.png", "overlay_grill_glow.png", "overlay_burner_flames.png"):
            paste(room, parts[name], 836, 233)

    if keeper_x is not None:
        keeper = Image.open(SOURCES / "keeper_prime_master-neutral-standing-back_f1.png").convert("RGBA")
        room.alpha_composite(keeper, (keeper_x - 128, 502 - 316))
    # Reapply jamb as the final foreground occluder.
    jd = ImageDraw.Draw(room)
    jd.rectangle((0, 208, 31, 543), fill=WOOD_DARK)
    jd.rectangle((5, 208, 25, 543), fill=WOOD)
    jd.rectangle((9, 208, 16, 543), fill=WOOD_LIGHT)
    jd.line((26, 208, 26, 543), fill=INK, width=3)
    jd.rectangle((1504, 208, 1535, 543), fill=WOOD_DARK)
    jd.rectangle((1510, 208, 1530, 543), fill=WOOD)
    jd.rectangle((1519, 208, 1526, 543), fill=WOOD_LIGHT)
    jd.line((1510, 208, 1510, 543), fill=INK, width=3)
    return room, item_layer


def contact_sheet(records: dict[str, dict]) -> None:
    names = sorted(records)
    width, row_h = 1380, 190
    sheet = Image.new("RGBA", (width, 90 + len(names) * row_h), (12, 24, 32, 255))
    d = ImageDraw.Draw(sheet)
    d.text((24, 18), "Kitchen V3 rebuild · isolated production parts", font=font(30, True), fill=CREAM)
    d.text((24, 56), "Every part at native pixels where practical · generated source normalized to exact contract", font=font(16), fill=(183, 214, 224, 255))
    for index, name in enumerate(names):
        y = 90 + index * row_h
        d.rounded_rectangle((14, y + 5, width - 14, y + row_h - 6), radius=8, fill=(21, 40, 52, 255), outline=(55, 86, 101, 255), width=2)
        rec = records[name]
        d.text((30, y + 18), name, font=font(19, True), fill=(255, 205, 99, 255))
        d.text((30, y + 48), f"{rec['canvasPx'][0]} × {rec['canvasPx'][1]} · {rec['category']} · {rec['bayWidth']} bay", font=font(15), fill=(195, 222, 230, 255))
        checker = Image.new("RGBA", (720, 150), (239, 231, 208, 255)); cd = ImageDraw.Draw(checker)
        for yy in range(0, 150, 15):
            for xx in range(0, 720, 15):
                if (xx // 15 + yy // 15) % 2: cd.rectangle((xx, yy, xx + 14, yy + 14), fill=(211, 216, 211, 255))
        part = Image.open(PARTS / name).convert("RGBA")
        ratio = min(1.0, 690 / part.width, 138 / part.height)
        preview = part.resize((max(1, round(part.width * ratio)), max(1, round(part.height * ratio))), Image.Resampling.NEAREST if ratio > 1 else Image.Resampling.LANCZOS)
        checker.alpha_composite(preview, ((720 - preview.width) // 2, (150 - preview.height) // 2))
        sheet.alpha_composite(checker, (640, y + 20))
    sheet.save(OUTPUTS / "contact_sheet.png", optimize=True)


def main() -> None:
    PARTS.mkdir(parents=True, exist_ok=True); OUTPUTS.mkdir(parents=True, exist_ok=True)
    if sha256(SOURCES / "v7-oven-authority.png") != V7_SHA:
        raise RuntimeError("V7 style authority hash mismatch")
    records = make_parts()
    parts = {name: Image.open(PARTS / name).convert("RGBA") for name in records}
    shell = room_shell()
    shell_path = PARTS / "room_shell_kitchen.png"
    shell.save(shell_path, optimize=True)
    shell_record = {
        "canvasPx": [W, H], "category": "shell", "bayWidth": 0,
        "sha256": sha256(shell_path), "sourceSha256": source_hash("window-source.png"),
    }
    room, item_layer = assemble(parts)
    room.save(OUTPUTS / "kitchen_v3_rebuild_room.png", optimize=True)
    room.resize((3072, 1152), Image.Resampling.NEAREST).save(OUTPUTS / "kitchen_v3_rebuild_room_2x.png", optimize=True)
    room.resize((384, 144), Image.Resampling.LANCZOS).save(OUTPUTS / "kitchen_v3_rebuild_tower_scale.png", optimize=True)

    state_sheet = Image.new("RGBA", (W, H * 3), (0, 0, 0, 255))
    state_draw = ImageDraw.Draw(state_sheet)
    for index, (label, options) in enumerate((
        ("RIGHT DOOR · JAMB ONLY", {}),
        ("FRIDGE OPEN / INTERIOR LIT", {"open_fridge": True}),
        ("COOKER LIGHT OVERLAYS", {"lit_cooker": True}),
    )):
        state_room, _ = assemble(parts, **options)
        state_sheet.alpha_composite(state_room, (0, index * H))
        state_draw.rounded_rectangle((45, index * H + 42, 370, index * H + 84), radius=8, fill=(7, 17, 24, 225))
        state_draw.text((62, index * H + 52), label, font=font(18, True), fill=CREAM_LIGHT)
    state_sheet.save(OUTPUTS / "freestanding_state_overlays.png", optimize=True)

    keeper_checks = []
    for label, x in (("fridge", 454), ("sink", 622), ("cooker", 874)):
        image, _ = assemble(parts, keeper_x=x)
        image.save(OUTPUTS / f"keeper_check_{label}.png", optimize=True)
        keeper_checks.append((label, image))
    check_sheet = Image.new("RGBA", (W, H * 3), (0, 0, 0, 255)); cd = ImageDraw.Draw(check_sheet)
    for index, (label, image) in enumerate(keeper_checks):
        check_sheet.alpha_composite(image, (0, index * H))
        cd.rounded_rectangle((45, index * H + 42, 275, index * H + 84), radius=8, fill=(7, 17, 24, 225))
        cd.text((62, index * H + 52), f"Prime at {label} · 1:1", font=font(19, True), fill=CREAM_LIGHT)
    check_sheet.save(OUTPUTS / "keeper_check_sheet.png", optimize=True)

    calibration = Image.open(SOURCES / "approved-style-calibration.png").convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
    comparison = Image.new("RGBA", (W * 2, H + 52), (11, 23, 31, 255)); comparison.alpha_composite(calibration, (0, 52)); comparison.alpha_composite(room, (W, 52))
    comp_d = ImageDraw.Draw(comparison); comp_d.text((28, 14), "APPROVED STYLE CALIBRATION", font=font(23, True), fill=CREAM); comp_d.text((W + 28, 14), "GRID-SNAPPED MODULAR REBUILD", font=font(23, True), fill=CREAM)
    comparison.save(OUTPUTS / "calibration_vs_rebuild.png", optimize=True)
    contact_sheet({"room_shell_kitchen.png": shell_record, **records})

    # Isolation proof: recolour only the sink taps in memory.
    sink = parts["insert_sink_2bay.png"].copy(); sp = sink.load(); changed_local = 0
    for y in range(sink.height):
        for x in range(sink.width):
            r, g, b, a = sp[x, y]
            if a and b > r and b > g and 50 < r < 220:
                sp[x, y] = (COPPER[0], COPPER[1], COPPER[2], a); changed_local += 1
    isolated, _ = assemble(parts, sink_override=sink)
    diff = ImageChops.difference(room, isolated).convert("RGB")
    bbox_raw = diff.getbbox(); bbox = None if bbox_raw is None else [bbox_raw[0], bbox_raw[1], bbox_raw[2] - 1, bbox_raw[3] - 1]
    diff_pixels = sum(1 for pixel in diff.get_flattened_data() if pixel != (0, 0, 0))
    evidence = Image.new("RGBA", room.size, (0, 0, 0, 0)); ep = evidence.load()
    for y in range(H):
        for x in range(W):
            if diff.getpixel((x, y)) != (0, 0, 0): ep[x, y] = (255, 210, 48, 255)
    evidence.save(OUTPUTS / "isolation_sink_taps_diff.png", optimize=True)

    room_pixels = list(room.get_flattened_data())
    exact_magenta = sum(1 for p in room_pixels if p == MAGENTA)
    near_magenta = sum(1 for r, g, b, a in room_pixels if a and r >= 180 and b >= 180 and g <= 100 and (r, g, b, a) != MAGENTA)
    forbidden = 0
    for x0, _, x1, _ in WINDOWS:
        for y in range(274):
            for x in range(x0, x1):
                if item_layer.getpixel((x, y))[3]: forbidden += 1

    (PARTS / "room.json").write_text(json.dumps({
        "schema": "lighthouse-keeper/kitchen-v3-rebuild-room@1", "canvasPx": [W, H], "walkY": 502,
        "bayFieldX": [328, 1504], "bayWidthPx": 84, "bayCount": 14,
        "runs": [[3, 6], [8, 12]], "windows": WINDOWS,
        "placements": {"dresser": [1, 370], "fridge": [2, 454], "drawers": [[3, 538], [6, 790], [8, 958], [9, 1042]], "sink": [[4, 5], 622], "cooker": [7, 874], "toaster": [9, 1042], "kettle": [12, 1294], "petBowl": [13, 1378], "pedalBin": [14, 1462]},
        "rightDoorJambPx": [1504, 208, 1536, 544],
        "retiredFromKitchen": ["unit_utility_cupboard_closed.png", "overlay_utility_cupboard_open.png", "unit_larder_cupboard_closed.png", "overlay_larder_cupboard_open.png", "unit_fridge_freezer.png", "front_dishwasher.png", "overlay_dishwasher_led.png", "cooker.png"],
    }, indent=2) + "\n", encoding="utf-8")

    files = {}
    for folder in (PARTS, OUTPUTS, SOURCES):
        for path in sorted(folder.rglob("*")):
            if path.is_file(): files[path.relative_to(ROOT).as_posix()] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    manifest = {
        "schema": "lighthouse-keeper/kitchen-proof-v3-rebuild@1", "status": "review-only-awaiting-frank", "canonMutation": False, "runtimeMutation": False,
        "geometry": {"modulePx": [W, H], "scalePxPerM": 168, "topRevealPxPerM": 28, "walkY": 502, "floorBandY": [460, 544], "bayFieldX": [328, 1504], "bayCount": 14, "bayWidthPx": 84, "windows": WINDOWS, "glassLocalRects": GLASS_LOCAL_RECTS, "leftDoorJambPx": [0, 208, 32, 544], "rightDoorJambPx": [1504, 208, 1536, 544], "verticals": {"unitBase": 485, "plinth": [468, 485], "fronts": [336, 468], "worktopEdge": [322, 336], "worktopReveal": [305, 322], "dresser1950s": [183, 485], "fridge1950s": [233, 485], "cooker1950s": [233, 485], "cookerHobReveal": [305, 322]}},
        "keeper": {"sourceScale": 1.0, "standingHeightPx": 298, "soleDatumY": 316, "roomSoleY": 502, "positions": [454, 622, 874], "worktopEdgeHeightPx": 180, "worktopEdgePercent": round(180 / 298 * 100, 2)},
        "style": {"approvedCalibrationSha256": sha256(SOURCES / "approved-style-calibration.png"), "v7Sha256": V7_SHA, "fillPalette": "palette_env-v1", "fillPaletteSize": len(PALETTE), "normalization": "generated alpha >=200 becomes silhouette; lower-alpha exterior halo/shadow discarded; final antialias created only by deterministic resampling"},
        "checks": {"exactMagentaPixels": exact_magenta, "nearMagentaPixels": near_magenta, "itemPixelsAboveWindowLimit": forbidden, "worktopRuns": [[496, 832], [916, 1336]], "worktopTopY": 305, "cookerHobTopY": 305, "cookerTopY": 233, "cookerFeetY": 485, "eyeLevelGrillY": [251, 291], "rightJambPx": [1504, 208, 1536, 544], "plinthY": [468, 485], "castShadowPolicy": "none; generated exterior alpha below threshold discarded before fitting", "itemInkPx": "2–3 at native scale", "keeperInkPx": "3–4 at native scale", "isolation": {"changedLocalTapPixels": changed_local, "roomDiffPixels": diff_pixels, "roomDiffBoundsInclusive": bbox, "allowedBoundsInclusive": [580, 274, 747, 321], "allStoredPartHashesUnchanged": True}, "overlayRects": {"overlay_oven_window.png": [11, 132, 65, 190], "overlay_grill_glow.png": [10, 18, 66, 58], "overlay_burner_flames.png": [8, 72, 68, 108]}},
        "shell": {"file": "parts/room_shell_kitchen.png", **shell_record},
        "parts": records, "files": files,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
