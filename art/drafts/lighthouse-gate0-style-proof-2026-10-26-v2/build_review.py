#!/usr/bin/env python3
"""Build the reversible Gate 0 A/B style proof without touching canon."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
ASSETS = ROOT / "assets"

MAGENTA = (255, 0, 255, 255)
INK = (20, 36, 58, 255)
CREAM = (243, 231, 204, 255)
CREAM_LIGHT = (255, 246, 229, 255)
CREAM_SHADOW = (218, 202, 169, 255)
WOOD = (182, 109, 50, 255)
WOOD_LIGHT = (212, 151, 81, 255)
WOOD_DARK = (120, 69, 33, 255)
FLOOR = (200, 137, 70, 255)
FLOOR_SHADOW = (154, 91, 42, 255)
BLUE = (68, 111, 164, 255)
BLUE_LIGHT = (102, 145, 193, 255)
BLUE_DARK = (37, 72, 116, 255)
ENAMEL = (238, 232, 213, 255)
METAL = (142, 159, 169, 255)

KEEPER_PALETTE = [
    (4, 21, 53),
    (20, 36, 58),
    (38, 62, 107),
    (61, 84, 128),
    (5, 96, 196),
    (10, 87, 181),
    (31, 121, 220),
    (252, 241, 222),
    (229, 216, 194),
    (248, 241, 223),
    (236, 209, 181),
    (217, 147, 96),
    (231, 161, 126),
    (230, 185, 85),
    (180, 124, 31),
    (255, 255, 255),
    (0, 0, 0),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError("transparent Keeper source")
    return bbox


def nearest_palette(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    return min(
        KEEPER_PALETTE,
        key=lambda p: (p[0] - rgb[0]) ** 2 + (p[1] - rgb[1]) ** 2 + (p[2] - rgb[2]) ** 2,
    )


def flatten_keeper(image: Image.Image, hard_alpha: bool) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a == 0 or (hard_alpha and a < 128):
                pixels[x, y] = (0, 0, 0, 0)
                continue
            nr, ng, nb = nearest_palette((r, g, b))
            pixels[x, y] = (nr, ng, nb, 255 if hard_alpha else a)
    return image


def prepare_keeper(path: Path, target_height: int, pixel: bool) -> Image.Image:
    source = Image.open(path).convert("RGBA")
    source = source.crop(alpha_bbox(source))
    target_width = round(source.width * target_height / source.height)
    resized = source.resize(
        (target_width, target_height),
        Image.Resampling.LANCZOS,
    )
    return flatten_keeper(resized, hard_alpha=pixel)


def draw_pixel_window(draw: ImageDraw.ImageDraw, x: int) -> None:
    y = 64
    draw.rectangle((x + 2, y + 2, x + 97, y + 97), fill=CREAM_SHADOW)
    draw.rectangle((x, y, x + 95, y + 95), fill=INK)
    draw.rectangle((x + 2, y + 2, x + 93, y + 93), fill=WOOD_DARK)
    draw.rectangle((x + 6, y + 6, x + 89, y + 89), fill=WOOD_LIGHT)
    draw.rectangle((x + 8, y + 8, x + 87, y + 87), fill=MAGENTA)
    draw.rectangle((x + 46, y + 6, x + 49, y + 89), fill=WOOD_DARK)
    draw.rectangle((x + 6, y + 46, x + 89, y + 49), fill=WOOD_DARK)
    draw.line((x + 8, y + 8, x + 87, y + 8), fill=CREAM_LIGHT, width=1)
    draw.rectangle((x - 4, y + 94, x + 99, y + 99), fill=INK)
    draw.rectangle((x - 2, y + 94, x + 97, y + 97), fill=WOOD_LIGHT)


def draw_pixel_kitchen(draw: ImageDraw.ImageDraw) -> None:
    """Draw the back-wall kitchen on whole 48 px authoring bays."""

    # Fridge: bays 1-2 (delivered x=256-447), full-height back-wall unit.
    draw.rectangle((128, 103, 223, 239), fill=INK)
    draw.rectangle((130, 105, 221, 239), fill=BLUE_LIGHT)
    draw.rectangle((130, 176, 221, 239), fill=BLUE)
    draw.line((176, 105, 176, 239), fill=BLUE_DARK, width=2)
    draw.line((132, 176, 219, 176), fill=CREAM_LIGHT, width=1)
    draw.rectangle((168, 139, 171, 168), fill=METAL)
    draw.rectangle((180, 139, 183, 168), fill=METAL)
    draw.rectangle((130, 236, 221, 239), fill=BLUE_DARK)

    # Cooker: bay 3.
    draw.rectangle((224, 183, 271, 239), fill=INK)
    draw.rectangle((226, 185, 269, 239), fill=ENAMEL)
    draw.rectangle((226, 185, 269, 191), fill=WOOD_DARK)
    for cx in (232, 242, 252, 262):
        draw.rectangle((cx, 195, cx + 3, 198), fill=BLUE_DARK)
    draw.rectangle((231, 203, 264, 231), fill=BLUE_DARK)
    draw.rectangle((235, 207, 260, 226), fill=(33, 43, 53, 255))
    draw.rectangle((237, 209, 258, 211), fill=WOOD_LIGHT)
    draw.rectangle((226, 235, 269, 239), fill=CREAM_SHADOW)

    # Worktop: bays 4-5.
    draw.rectangle((272, 183, 367, 239), fill=INK)
    draw.rectangle((274, 187, 365, 239), fill=BLUE)
    draw.rectangle((270, 181, 369, 188), fill=INK)
    draw.rectangle((272, 182, 367, 185), fill=WOOD_LIGHT)
    draw.line((320, 188, 320, 238), fill=BLUE_DARK, width=2)
    for cx in (294, 342):
        draw.rectangle((cx, 202, cx + 5, 204), fill=ENAMEL)
    draw.rectangle((274, 235, 365, 239), fill=BLUE_DARK)

    # Belfast sink and cabinet: bays 6-7.
    draw.rectangle((368, 183, 463, 239), fill=INK)
    draw.rectangle((370, 187, 461, 239), fill=BLUE)
    draw.rectangle((366, 181, 465, 188), fill=INK)
    draw.rectangle((371, 181, 460, 190), fill=ENAMEL)
    draw.rectangle((379, 184, 452, 196), fill=CREAM_SHADOW)
    draw.line((416, 188, 416, 238), fill=BLUE_DARK, width=2)
    draw.rectangle((395, 168, 399, 181), fill=METAL)
    draw.rectangle((397, 167, 420, 170), fill=METAL)
    draw.rectangle((417, 169, 420, 181), fill=METAL)
    draw.rectangle((370, 235, 461, 239), fill=BLUE_DARK)

    # Dresser: bays 8-9, taller than the fitted counter run.
    draw.rectangle((464, 165, 559, 239), fill=INK)
    draw.rectangle((466, 168, 557, 239), fill=BLUE_LIGHT)
    draw.rectangle((466, 188, 557, 239), fill=BLUE)
    draw.rectangle((470, 171, 553, 184), fill=CREAM)
    for cx in (479, 506, 533):
        draw.rectangle((cx, 174, cx + 9, 181), fill=ENAMEL)
    draw.line((512, 188, 512, 238), fill=BLUE_DARK, width=2)
    draw.rectangle((486, 201, 491, 203), fill=ENAMEL)
    draw.rectangle((534, 201, 539, 203), fill=ENAMEL)
    draw.rectangle((466, 235, 557, 239), fill=BLUE_DARK)

    # Bin: bay 10. The three rightmost bays stay open.
    draw.rectangle((560, 203, 607, 239), fill=INK)
    draw.rectangle((564, 207, 603, 239), fill=BLUE_DARK)
    draw.rectangle((562, 201, 605, 207), fill=INK)
    draw.rectangle((566, 202, 601, 204), fill=METAL)
    draw.rectangle((568, 232, 599, 239), fill=(29, 55, 86, 255))


def draw_pixel_room() -> Image.Image:
    image = Image.new("RGBA", (768, 256), CREAM)
    draw = ImageDraw.Draw(image)

    # Bare, completely flat room shell: all visible surfaces are bands.
    draw.rectangle((0, 0, 767, 15), fill=WOOD_DARK)
    draw.rectangle((2, 2, 765, 11), fill=WOOD)
    draw.line((0, 15, 767, 15), fill=INK, width=2)
    draw.rectangle((0, 0, 15, 255), fill=CREAM_SHADOW)
    draw.rectangle((752, 0, 767, 255), fill=CREAM_SHADOW)
    draw.line((15, 0, 15, 255), fill=INK, width=2)
    draw.line((752, 0, 752, 255), fill=INK, width=2)

    # Controlled plaster clusters; no one-pixel noise.
    for x, y in [(172, 42), (432, 33), (662, 48), (372, 196), (686, 211)]:
        draw.rectangle((x, y, x + 7, y + 2), fill=CREAM_LIGHT)
    for x, y in [(212, 207), (486, 50), (714, 184)]:
        draw.rectangle((x, y, x + 9, y + 2), fill=CREAM_SHADOW)

    # Door jamb only: a narrow cut edge at the front-left. There is no door
    # leaf, knob, back-wall opening or stair depiction.
    draw.rectangle((16, 16, 24, 239), fill=INK)
    draw.rectangle((18, 17, 22, 239), fill=WOOD_DARK)
    draw.rectangle((20, 17, 22, 239), fill=WOOD)

    draw_pixel_window(draw, 272)
    draw_pixel_window(draw, 560)

    # Skirting and flat front walking strip. No receding seams or angled edge.
    draw.rectangle((16, 230, 751, 239), fill=INK)
    draw.rectangle((16, 232, 751, 238), fill=WOOD)
    draw.line((16, 232, 751, 232), fill=WOOD_LIGHT, width=1)
    draw.rectangle((0, 240, 767, 255), fill=INK)
    draw.rectangle((2, 242, 765, 255), fill=FLOOR)
    draw.line((2, 246, 765, 246), fill=WOOD_LIGHT, width=2)
    draw.rectangle((2, 253, 765, 255), fill=FLOOR_SHADOW)

    # Furniture sits on the back layer; the Keeper is composited afterwards
    # on the separate front locomotion strip.
    draw_pixel_kitchen(draw)

    keeper = prepare_keeper(SOURCES / "keeper-candidate-a-generated.png", 125, pixel=True)
    keeper_x = 505 - keeper.width // 2
    keeper_y = 240 - keeper.height
    image.alpha_composite(keeper, (keeper_x, keeper_y))
    return image


def scaled_draw(draw: ImageDraw.ImageDraw, scale: int, kind: str, coords, **kwargs) -> None:
    c = tuple(round(v * scale) for v in coords)
    if "width" in kwargs:
        kwargs["width"] = max(1, round(kwargs["width"] * scale))
    getattr(draw, kind)(c, **kwargs)


def draw_smooth_room() -> Image.Image:
    scale = 3
    image = Image.new("RGBA", (1536 * scale, 512 * scale), CREAM)
    draw = ImageDraw.Draw(image)

    def rect(coords, **kwargs):
        scaled_draw(draw, scale, "rectangle", coords, **kwargs)

    def line(coords, **kwargs):
        scaled_draw(draw, scale, "line", coords, **kwargs)

    def ellipse(coords, **kwargs):
        scaled_draw(draw, scale, "ellipse", coords, **kwargs)

    def rounded(coords, radius, **kwargs):
        c = tuple(round(v * scale) for v in coords)
        if "width" in kwargs:
            kwargs["width"] = max(1, round(kwargs["width"] * scale))
        draw.rounded_rectangle(c, radius=round(radius * scale), **kwargs)

    rect((0, 0, 1535, 31), fill=WOOD_DARK)
    rect((4, 4, 1531, 23), fill=WOOD)
    line((0, 31, 1535, 31), fill=INK, width=4)
    rect((0, 0, 31, 511), fill=CREAM_SHADOW)
    rect((1504, 0, 1535, 511), fill=CREAM_SHADOW)
    line((31, 0, 31, 511), fill=INK, width=4)
    line((1504, 0, 1504, 511), fill=INK, width=4)

    # Broad, restrained plaster marks: flat fills only.
    for x, y, w in [(344, 84, 84), (866, 67, 64), (1290, 98, 82), (746, 399, 76)]:
        rect((x, y, x + w, y + 5), fill=CREAM_LIGHT)
    for x, y, w in [(422, 414, 92), (970, 102, 72), (1390, 370, 58)]:
        rect((x, y, x + w, y + 5), fill=CREAM_SHADOW)

    # Door jamb only at the front-left cut edge; no back-wall door panel.
    rect((32, 32, 48, 479), fill=INK)
    rect((36, 34, 44, 479), fill=WOOD_DARK)
    rect((40, 34, 44, 479), fill=WOOD)

    for x in (544, 1120):
        y = 128
        rect((x + 8, y + 8, x + 199, y + 199), fill=CREAM_SHADOW)
        rect((x, y, x + 191, y + 191), fill=INK)
        rect((x + 4, y + 4, x + 187, y + 187), fill=WOOD_DARK)
        rect((x + 12, y + 12, x + 179, y + 179), fill=WOOD_LIGHT)
        # Neutral construction fill here prevents antialiasing from creating
        # near-magenta edge pixels. Exact key panes are written after resize.
        rect((x + 16, y + 16, x + 175, y + 175), fill=CREAM_SHADOW)
        rect((x + 92, y + 12, x + 99, y + 179), fill=WOOD_DARK)
        rect((x + 12, y + 92, x + 179, y + 99), fill=WOOD_DARK)
        line((x + 16, y + 16, x + 175, y + 16), fill=CREAM_LIGHT, width=2)
        rect((x - 8, y + 188, x + 199, y + 201), fill=INK)
        rect((x - 4, y + 188, x + 195, y + 195), fill=WOOD_LIGHT)

    rect((32, 460, 1503, 479), fill=INK)
    rect((32, 464, 1503, 476), fill=WOOD)
    line((32, 464, 1503, 464), fill=WOOD_LIGHT, width=2)
    rect((0, 480, 1535, 511), fill=INK)
    rect((4, 484, 1531, 511), fill=FLOOR)
    line((4, 492, 1531, 492), fill=WOOD_LIGHT, width=4)
    rect((4, 506, 1531, 511), fill=FLOOR_SHADOW)

    # Back-wall furniture. Each footprint is one or two whole bays. The
    # Keeper is composited after this group, on the front walking layer.
    # Fridge, bays 1-2.
    rounded((256, 206, 447, 479), 8, fill=INK)
    rounded((262, 212, 441, 479), 5, fill=BLUE_LIGHT)
    rect((262, 352, 441, 479), fill=BLUE)
    line((352, 214, 352, 478), fill=BLUE_DARK, width=4)
    line((266, 352, 437, 352), fill=CREAM_LIGHT, width=2)
    rounded((336, 276, 344, 336), 3, fill=METAL)
    rounded((360, 276, 368, 336), 3, fill=METAL)
    rect((262, 470, 441, 479), fill=BLUE_DARK)

    # Cooker, bay 3.
    rounded((448, 366, 543, 479), 6, fill=INK)
    rect((454, 374, 537, 479), fill=ENAMEL)
    rect((448, 362, 543, 378), fill=INK)
    rect((454, 365, 537, 371), fill=WOOD_DARK)
    for cx in (466, 485, 504, 523):
        ellipse((cx, 389, cx + 8, 397), fill=BLUE_DARK)
    rounded((465, 406, 526, 463), 4, fill=BLUE_DARK)
    rounded((472, 413, 519, 453), 3, fill=(33, 43, 53, 255))
    rect((475, 416, 516, 421), fill=WOOD_LIGHT)
    rect((454, 470, 537, 479), fill=CREAM_SHADOW)

    # Worktop, bays 4-5.
    rect((544, 368, 735, 479), fill=INK)
    rect((550, 378, 729, 479), fill=BLUE)
    rounded((540, 362, 739, 378), 5, fill=INK)
    rounded((546, 365, 733, 373), 3, fill=WOOD_LIGHT)
    line((640, 379, 640, 478), fill=BLUE_DARK, width=4)
    for cx in (590, 686):
        rounded((cx, 405, cx + 14, 411), 3, fill=ENAMEL)
    rect((550, 470, 729, 479), fill=BLUE_DARK)

    # Belfast sink, bays 6-7.
    rect((736, 368, 927, 479), fill=INK)
    rect((742, 382, 921, 479), fill=BLUE)
    rounded((732, 362, 931, 381), 5, fill=INK)
    rounded((742, 362, 921, 390), 5, fill=ENAMEL)
    rounded((758, 369, 905, 400), 4, fill=CREAM_SHADOW)
    line((832, 401, 832, 478), fill=BLUE_DARK, width=4)
    rounded((790, 336, 800, 362), 4, fill=METAL)
    rounded((796, 332, 842, 341), 4, fill=METAL)
    rounded((835, 336, 844, 362), 4, fill=METAL)
    rect((742, 470, 921, 479), fill=BLUE_DARK)

    # Dresser, bays 8-9.
    rounded((928, 330, 1119, 479), 7, fill=INK)
    rect((934, 338, 1113, 479), fill=BLUE_LIGHT)
    rect((934, 378, 1113, 479), fill=BLUE)
    rounded((942, 344, 1105, 370), 4, fill=CREAM)
    for cx in (960, 1013, 1066):
        rounded((cx, 349, cx + 26, 365), 5, fill=ENAMEL)
    line((1024, 379, 1024, 478), fill=BLUE_DARK, width=4)
    rounded((972, 405, 986, 411), 3, fill=ENAMEL)
    rounded((1062, 405, 1076, 411), 3, fill=ENAMEL)
    rect((934, 470, 1113, 479), fill=BLUE_DARK)

    # Bin, bay 10; bays 11-13 remain open.
    rounded((1120, 404, 1215, 479), 6, fill=INK)
    rounded((1128, 414, 1207, 479), 5, fill=BLUE_DARK)
    rounded((1124, 400, 1211, 414), 6, fill=INK)
    rounded((1132, 403, 1203, 409), 3, fill=METAL)
    rect((1136, 464, 1199, 479), fill=(29, 55, 86, 255))

    image = image.resize((1536, 512), Image.Resampling.LANCZOS)

    # Reinstate byte-exact key panes after antialiasing the smooth frames.
    target = ImageDraw.Draw(image)
    for x in (544, 1120):
        target.rectangle((x + 16, 146, x + 91, 219), fill=MAGENTA)
        target.rectangle((x + 100, 146, x + 175, 219), fill=MAGENTA)
        target.rectangle((x + 16, 228, x + 91, 303), fill=MAGENTA)
        target.rectangle((x + 100, 228, x + 175, 303), fill=MAGENTA)

    keeper = prepare_keeper(SOURCES / "keeper-candidate-b-generated.png", 248, pixel=False)
    keeper_x = 1010 - keeper.width // 2
    keeper_y = 480 - keeper.height
    image.alpha_composite(keeper, (keeper_x, keeper_y))
    return image


def magenta_count(image: Image.Image) -> int:
    return sum(1 for pixel in image.convert("RGBA").get_flattened_data() if pixel == MAGENTA)


def hard_alpha_ok(image: Image.Image) -> bool:
    return all(a in (0, 255) for *_, a in image.convert("RGBA").get_flattened_data())


def save(image: Image.Image, name: str) -> Path:
    path = ASSETS / name
    image.save(path, optimize=True)
    return path


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    a_authoring = draw_pixel_room()
    a_room = a_authoring.resize((1536, 512), Image.Resampling.NEAREST)
    b_room = draw_smooth_room()
    a_tower = a_authoring.resize((384, 128), Image.Resampling.NEAREST)
    b_tower = b_room.resize((384, 128), Image.Resampling.LANCZOS)

    outputs = {
        "candidateAAuthoring": save(a_authoring, "candidate-a-authoring-768x256.png"),
        "candidateARoom": save(a_room, "candidate-a-room-1536x512.png"),
        "candidateATower": save(a_tower, "candidate-a-tower-384x128.png"),
        "candidateBRoom": save(b_room, "candidate-b-room-1536x512.png"),
        "candidateBTower": save(b_tower, "candidate-b-tower-384x128.png"),
    }

    source_names = [
        "LIGHTHOUSE_SPEC_v2_DRAFT.md",
        "keeper-approved-side.png",
        "keeper-approved-front.png",
        "keeper-approved-back.png",
        "keeper-candidate-a-generated.png",
        "keeper-candidate-b-generated.png",
        "room-source-a-rejected.png",
        "room-source-b-rejected.png",
        "room_depth_rule.png",
    ]

    manifest = {
        "schema": "lighthouse-keeper/gate0-style-proof@2",
        "status": "candidate-awaiting-frank",
        "date": "2026-10-26",
        "canonMutation": False,
        "geometry": {
            "deliveredModulePx": [1536, 512],
            "authoringModuleAu": [768, 256],
            "floorSurfaceY": 480,
            "walkInZoneX": [32, 256],
            "bayFieldX": [256, 1504],
            "bayCount": 13,
            "bayWidthPx": 96,
            "windows": [
                {"x": 544, "y": 128, "width": 192, "height": 192, "bays": [4, 5]},
                {"x": 1120, "y": 128, "width": 192, "height": 192, "bays": [10, 11]},
            ],
            "depthRule": {
                "logicalPlan": {"backFurniturePercent": 70, "frontWalkingPercent": 30},
                "frontProjection": "strict orthographic front elevation",
                "floorStripY": [480, 511],
                "doorJambX": [32, 48],
                "doorPanel": False,
                "visibleStairs": False,
                "angledSideWalls": False,
                "floorSeenFromAbove": False,
                "layerOrder": [
                    "back-wall shell",
                    "back-wall furniture",
                    "Keeper/front walking strip",
                ],
            },
            "furniture": [
                {"id": "fridge", "bays": [1, 2], "x": [256, 448]},
                {"id": "cooker", "bays": [3], "x": [448, 544]},
                {"id": "worktop", "bays": [4, 5], "x": [544, 736]},
                {"id": "sink", "bays": [6, 7], "x": [736, 928]},
                {"id": "dresser", "bays": [8, 9], "x": [928, 1120]},
                {"id": "bin", "bays": [10], "x": [1120, 1216]},
            ],
        },
        "candidates": {
            "A": {
                "label": "High-resolution pixel illustration",
                "room": outputs["candidateARoom"].relative_to(ROOT).as_posix(),
                "tower": outputs["candidateATower"].relative_to(ROOT).as_posix(),
                "authoring": outputs["candidateAAuthoring"].relative_to(ROOT).as_posix(),
                "keeperHeightPx": 250,
                "keeperCentreX": 1010,
                "keeperFootY": 480,
                "rendering": "768x256 authoring; exact nearest-neighbour 2x delivery; hard alpha",
            },
            "B": {
                "label": "Smooth flat-colour illustration",
                "room": outputs["candidateBRoom"].relative_to(ROOT).as_posix(),
                "tower": outputs["candidateBTower"].relative_to(ROOT).as_posix(),
                "keeperHeightPx": 248,
                "keeperCentreX": 1010,
                "keeperFootY": 480,
                "rendering": "1536x512 smooth antialiased delivery; flat palette; exact key panes restored after rasterisation",
            },
        },
        "sources": {
            name: {"path": f"sources/{name}", "sha256": sha256(SOURCES / name)}
            for name in source_names
        },
        "outputs": {
            key: {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "size": list(Image.open(path).size),
                "magentaPixels": magenta_count(Image.open(path)),
                "hardAlpha": hard_alpha_ok(Image.open(path)),
            }
            for key, path in outputs.items()
        },
        "knownBoundary": "The approved Prime identity references contain one broad torso stripe while the proposed reboot text describes two separate chest stripes. These non-canon style candidates preserve the approved source identity rather than deciding Gate 3 stripe geometry.",
        "revision": "V2 supersedes V1 for review only by applying Frank's room-depth rule: fitted furniture on the back layer, Keeper on the front walking strip, left-front jamb only, and no perspective floor, angled wall, stair or back-wall door.",
    }

    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
