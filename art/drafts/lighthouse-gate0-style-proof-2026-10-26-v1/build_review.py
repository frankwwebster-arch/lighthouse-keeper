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

    # Minimal left-wall circulation-door edge, not a back-wall door.
    draw.rectangle((16, 104, 29, 239), fill=INK)
    draw.rectangle((18, 106, 27, 239), fill=WOOD_DARK)
    draw.rectangle((21, 110, 27, 236), fill=WOOD)
    draw.rectangle((24, 170, 26, 173), fill=(230, 185, 85, 255))

    draw_pixel_window(draw, 272)
    draw_pixel_window(draw, 560)

    # Skirting and 32 px delivered floor slab.
    draw.rectangle((16, 230, 751, 239), fill=INK)
    draw.rectangle((16, 232, 751, 238), fill=WOOD)
    draw.line((16, 232, 751, 232), fill=WOOD_LIGHT, width=1)
    draw.rectangle((0, 240, 767, 255), fill=INK)
    draw.rectangle((2, 242, 765, 255), fill=FLOOR)
    draw.line((2, 246, 765, 246), fill=WOOD_LIGHT, width=2)
    for x in range(32, 768, 96):
        draw.line((x, 242, x, 255), fill=WOOD_DARK, width=1)

    keeper = prepare_keeper(SOURCES / "keeper-candidate-a-generated.png", 125, pixel=True)
    keeper_x = max(18, 104 - keeper.width // 2)
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

    # Flat left-wall door edge.
    rect((32, 208, 59, 479), fill=INK)
    rect((36, 212, 55, 479), fill=WOOD_DARK)
    rect((42, 220, 55, 472), fill=WOOD)
    rect((49, 340, 54, 347), fill=(230, 185, 85, 255))

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
    for x in range(64, 1536, 192):
        line((x, 484, x, 511), fill=WOOD_DARK, width=2)

    image = image.resize((1536, 512), Image.Resampling.LANCZOS)

    # Reinstate byte-exact key panes after antialiasing the smooth frames.
    target = ImageDraw.Draw(image)
    for x in (544, 1120):
        target.rectangle((x + 16, 146, x + 91, 219), fill=MAGENTA)
        target.rectangle((x + 100, 146, x + 175, 219), fill=MAGENTA)
        target.rectangle((x + 16, 228, x + 91, 303), fill=MAGENTA)
        target.rectangle((x + 100, 228, x + 175, 303), fill=MAGENTA)

    keeper = prepare_keeper(SOURCES / "keeper-candidate-b-generated.png", 248, pixel=False)
    keeper_x = max(36, 208 - keeper.width // 2)
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
    ]

    manifest = {
        "schema": "lighthouse-keeper/gate0-style-proof@1",
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
        },
        "candidates": {
            "A": {
                "label": "High-resolution pixel illustration",
                "room": outputs["candidateARoom"].relative_to(ROOT).as_posix(),
                "tower": outputs["candidateATower"].relative_to(ROOT).as_posix(),
                "authoring": outputs["candidateAAuthoring"].relative_to(ROOT).as_posix(),
                "keeperHeightPx": 250,
                "rendering": "768x256 authoring; exact nearest-neighbour 2x delivery; hard alpha",
            },
            "B": {
                "label": "Smooth flat-colour illustration",
                "room": outputs["candidateBRoom"].relative_to(ROOT).as_posix(),
                "tower": outputs["candidateBTower"].relative_to(ROOT).as_posix(),
                "keeperHeightPx": 248,
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
    }

    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
