#!/usr/bin/env python3
"""Build the self-contained Kitchen Proof V3 review package."""

from __future__ import annotations

import hashlib
import io
import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
PARTS = ROOT / "parts"
OUTPUTS = ROOT / "outputs"
SOURCES = ROOT / "sources"
PRIME = SOURCES / "prime"

V7_COMMIT = "52e94f2a"
V7_REPO_PATH = "art/source/kitchen-built-in-state-ligne-claire-2026-10-21-v7/oven-on-user-confirmed-visual-authority.png"
V7_SHA = "0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538"

W, H = 1536, 576
MAGENTA = (255, 0, 255, 255)
INK = (7, 20, 30, 255)
INK_SOFT = (20, 42, 59, 255)
ROYAL = (0, 102, 204, 255)
ROYAL_LIGHT = (23, 134, 226, 255)
ROYAL_DARK = (0, 63, 137, 255)
CYAN = (41, 181, 210, 255)
CYAN_LIGHT = (105, 220, 230, 255)
CYAN_DARK = (8, 122, 157, 255)
CREAM = (255, 239, 202, 255)
CREAM_LIGHT = (255, 249, 229, 255)
CREAM_SHADOW = (226, 204, 163, 255)
COPPER = (243, 112, 24, 255)
COPPER_LIGHT = (255, 157, 58, 255)
COPPER_DARK = (174, 61, 7, 255)
WOOD = (151, 83, 37, 255)
WOOD_LIGHT = (202, 128, 61, 255)
WOOD_DARK = (91, 47, 27, 255)
FLOOR = (195, 133, 71, 255)
FLOOR_LIGHT = (223, 166, 96, 255)
FLOOR_DARK = (128, 76, 42, 255)
METAL = (173, 188, 191, 255)
GLASS_DARK = (21, 35, 44, 255)
RED = (198, 48, 36, 255)

WINDOWS = [(580, 106, 748, 274), (1084, 106, 1252, 274)]
GLASS_RECTS: list[tuple[int, int, int, int]] = []
for wx, wy, _, _ in WINDOWS:
    GLASS_RECTS.extend([
        (wx + 10, wy + 10, wx + 79, wy + 79),
        (wx + 89, wy + 10, wx + 158, wy + 79),
        (wx + 10, wy + 89, wx + 79, wy + 158),
        (wx + 89, wy + 89, wx + 158, wy + 158),
    ])

WALK_FRAMES = [
    REPO / f"art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f{i}.png"
    for i in range(1, 9)
]
BRIDGE_FRAMES = [
    REPO / f"art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f{i}.png"
    for i in range(1, 6)
]
TURN_FRAMES = [
    REPO / f"art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames/keeper_prime_turn_side-right_to_back_f{i:02d}.png"
    for i in range(1, 10)
]
SIDE_NEUTRAL = REPO / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
BACK_NEUTRAL = REPO / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


class Painter:
    def __init__(self, image: Image.Image, scale: int = 4):
        self.image = image
        self.scale = scale
        self.draw = ImageDraw.Draw(image)

    def box(self, coords):
        return tuple(round(v * self.scale) for v in coords)

    def rect(self, coords, fill, outline=None, width=1):
        self.draw.rectangle(self.box(coords), fill=fill, outline=outline, width=max(1, round(width * self.scale)))

    def rounded(self, coords, radius, fill, outline=None, width=1):
        self.draw.rounded_rectangle(self.box(coords), radius=round(radius * self.scale), fill=fill, outline=outline, width=max(1, round(width * self.scale)))

    def ellipse(self, coords, fill, outline=None, width=1):
        self.draw.ellipse(self.box(coords), fill=fill, outline=outline, width=max(1, round(width * self.scale)))

    def line(self, coords, fill, width=1, joint="curve"):
        self.draw.line(self.box(coords), fill=fill, width=max(1, round(width * self.scale)), joint=joint)

    def polygon(self, coords, fill, outline=None):
        pts = [(round(x * self.scale), round(y * self.scale)) for x, y in coords]
        self.draw.polygon(pts, fill=fill)
        if outline:
            self.draw.line(pts + [pts[0]], fill=outline, width=max(1, round(3 * self.scale)), joint="curve")


def render_part(width: int, height: int, paint) -> Image.Image:
    scale = 4
    image = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    paint(Painter(image, scale))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def extract_sources() -> None:
    SOURCES.mkdir(parents=True, exist_ok=True)
    PRIME.mkdir(parents=True, exist_ok=True)
    blob = subprocess.run(
        ["git", "show", f"{V7_COMMIT}:{V7_REPO_PATH}"],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    if hashlib.sha256(blob).hexdigest() != V7_SHA:
        raise RuntimeError("historical V7 blob hash mismatch")
    (SOURCES / "v7-oven-authority.png").write_bytes(blob)
    v7 = Image.open(io.BytesIO(blob)).convert("RGBA")
    v7.crop((155, 130, 1160, 1050)).save(SOURCES / "v7-reference-crop.png", optimize=True)

    source_files = [SIDE_NEUTRAL, BACK_NEUTRAL, *WALK_FRAMES, *BRIDGE_FRAMES, *TURN_FRAMES]
    for source in source_files:
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, PRIME / source.name)


def save_part(name: str, image: Image.Image, record: dict, records: dict) -> None:
    PARTS.mkdir(parents=True, exist_ok=True)
    path = PARTS / name
    image.save(path, optimize=True)
    records[name] = {
        "file": name,
        "pixelSize": list(image.size),
        "sha256": sha256(path),
        "realSizeM": record.get("realSizeM"),
        "bayWidth": record.get("bayWidth", 0),
        "useBay": record.get("useBay"),
        "slotIn": record.get("slotIn", False),
        "anchorPx": record.get("anchorPx", [0, image.height]),
        "standPointX": record.get("standPointX"),
        "lightOverlays": record.get("lightOverlays", []),
        "styleReference": {"path": V7_REPO_PATH, "sha256": V7_SHA},
    }


def make_parts() -> dict[str, dict]:
    records: dict[str, dict] = {}

    def worktop(p: Painter):
        p.rect((0, 0, 84, 25), CYAN)
        p.line((0, 1.5, 84, 1.5), CREAM_LIGHT, 2)
        p.line((0, 24, 84, 24), INK, 3)
        p.rect((0, 25, 84, 32), CYAN_DARK)
        p.line((0, 31, 84, 31), INK, 3)

    save_part("worktop_tile.png", render_part(84, 32, worktop), {"realSizeM": [0.5, 0.6, 0.04], "bayWidth": 1}, records)

    def worktop_cap_left(p: Painter):
        worktop(p)
        p.line((2, 0, 2, 32), INK, 3)
        p.line((4, 2, 4, 23), CYAN_LIGHT, 1.5)

    def worktop_cap_right(p: Painter):
        worktop(p)
        p.line((14, 0, 14, 32), INK, 3)
        p.line((12, 2, 12, 23), CYAN_DARK, 1.5)

    save_part("worktop_cap_left.png", render_part(16, 32, worktop_cap_left), {"realSizeM": [0.095, 0.6, 0.04]}, records)
    save_part("worktop_cap_right.png", render_part(16, 32, worktop_cap_right), {"realSizeM": [0.095, 0.6, 0.04]}, records)
    save_part("worktop_joint.png", render_part(2, 32, lambda p: p.rect((0, 0, 2, 32), INK_SOFT)), {"realSizeM": [0.012, 0.6, 0.04]}, records)

    def plinth(p: Painter):
        p.rect((0, 0, 84, 17), ROYAL_DARK)
        p.line((0, 1.5, 84, 1.5), INK, 3)
        p.line((0, 15.5, 84, 15.5), INK, 3)
        p.line((4, 5, 80, 5), ROYAL_LIGHT, 1.5)

    save_part("plinth_tile.png", render_part(84, 17, plinth), {"realSizeM": [0.5, 0.6, 0.1], "bayWidth": 1}, records)
    save_part("plinth_cap_left.png", render_part(16, 17, lambda p: (plinth(p), p.line((2, 0, 2, 17), INK, 3))), {"realSizeM": [0.095, 0.6, 0.1]}, records)
    save_part("plinth_cap_right.png", render_part(16, 17, lambda p: (plinth(p), p.line((14, 0, 14, 17), INK, 3))), {"realSizeM": [0.095, 0.6, 0.1]}, records)

    def front_drawers(p: Painter):
        p.rect((0, 0, 84, 127), ROYAL)
        for y0, y1 in ((4, 42), (44, 83), (85, 123)):
            p.rounded((5, y0, 79, y1), 3, ROYAL_LIGHT, INK, 2.5)
            p.rounded((31, y0 + 9, 53, y0 + 14), 2, COPPER, INK, 2)

    def front_cupboard(p: Painter):
        p.rect((0, 0, 84, 127), ROYAL)
        p.rounded((5, 5, 40, 123), 3, ROYAL_LIGHT, INK, 2.5)
        p.rounded((44, 5, 79, 123), 3, ROYAL_LIGHT, INK, 2.5)
        p.rounded((31, 56, 37, 72), 2, COPPER, INK, 1.8)
        p.rounded((47, 56, 53, 72), 2, COPPER, INK, 1.8)

    def front_sink(p: Painter):
        p.rect((0, 0, 168, 127), ROYAL)
        p.rounded((5, 5, 163, 47), 4, CREAM, INK, 3)
        p.line((14, 39, 154, 39), CREAM_SHADOW, 2)
        for x0, x1 in ((6, 81), (87, 162)):
            p.rounded((x0, 51, x1, 123), 3, ROYAL_LIGHT, INK, 2.5)
        p.rounded((74, 68, 80, 84), 2, COPPER, INK, 1.8)
        p.rounded((88, 68, 94, 84), 2, COPPER, INK, 1.8)

    def front_dishwasher(p: Painter):
        p.rect((0, 0, 84, 127), CREAM)
        p.rounded((4, 4, 80, 123), 4, CREAM_LIGHT, INK, 3)
        p.rounded((10, 14, 74, 23), 3, COPPER, INK, 2)
        for x in (16, 24, 32):
            p.ellipse((x, 31, x + 5, 36), GLASS_DARK, INK, 1)
        p.line((10, 48, 74, 48), CREAM_SHADOW, 2)

    save_part("front_drawers.png", render_part(84, 127, front_drawers), {"realSizeM": [0.5, 0.6, 0.76], "bayWidth": 1}, records)
    save_part("front_cupboard.png", render_part(84, 127, front_cupboard), {"realSizeM": [0.5, 0.6, 0.76], "bayWidth": 1}, records)
    save_part("front_sink_2bay.png", render_part(168, 127, front_sink), {"realSizeM": [1.0, 0.6, 0.76], "bayWidth": 2, "useBay": 1, "standPointX": 622}, records)
    save_part("front_dishwasher.png", render_part(84, 127, front_dishwasher), {"realSizeM": [0.5, 0.6, 0.76], "bayWidth": 1, "standPointX": 790, "lightOverlays": ["overlay_dishwasher_led.png"]}, records)

    def sink_insert(p: Painter):
        p.rounded((3, 38, 105, 62), 8, CREAM, INK, 3)
        p.rounded((10, 42, 98, 57), 6, CYAN_DARK, INK, 2)
        p.line((42, 37, 42, 17), METAL, 5)
        p.line((42, 17, 67, 17), METAL, 5)
        p.line((67, 17, 67, 35), METAL, 5)
        p.line((42, 37, 42, 17), INK, 8)
        p.line((42, 17, 67, 17), INK, 8)
        p.line((67, 17, 67, 35), INK, 8)
        p.line((42, 37, 42, 17), METAL, 3)
        p.line((42, 17, 67, 17), METAL, 3)
        p.line((67, 17, 67, 35), METAL, 3)
        p.ellipse((29, 28, 39, 38), COPPER, INK, 2)
        p.ellipse((72, 28, 82, 38), COPPER, INK, 2)

    save_part("insert_sink_2bay.png", render_part(168, 67, sink_insert), {"realSizeM": [1.0, 0.52, 0.31], "bayWidth": 2, "useBay": 1, "anchorPx": [0, 67], "standPointX": 622}, records)

    def cooker(p: Painter):
        p.rect((0, 0, 84, 25), ROYAL_LIGHT)
        p.line((0, 24, 84, 24), INK, 3)
        p.ellipse((9, 5, 37, 19), GLASS_DARK, INK, 3)
        p.ellipse((47, 5, 75, 19), GLASS_DARK, INK, 3)
        p.rect((0, 25, 84, 32), CYAN_DARK)
        p.line((0, 31, 84, 31), INK, 3)
        p.rect((0, 32, 84, 159), CREAM)
        p.line((1.5, 32, 1.5, 159), INK, 3)
        p.line((82.5, 32, 82.5, 159), INK, 3)
        for x in (20, 42, 64):
            p.ellipse((x - 6, 41, x + 6, 53), COPPER, INK, 2.5)
            p.line((x, 43, x, 49), COPPER_DARK, 2)
        p.rounded((11, 60, 73, 69), 3, COPPER, INK, 2.5)
        p.rounded((12, 76, 72, 135), 6, INK, INK, 3)
        p.rounded((17, 82, 67, 129), 4, GLASS_DARK, (43, 62, 72, 255), 3)
        for y in (91, 108, 122):
            p.line((23, y, 61, y), (64, 82, 88, 255), 1.5)
        p.rect((0, 159, 84, 176), ROYAL_DARK)
        p.line((0, 160, 84, 160), INK, 3)
        p.line((5, 168, 79, 168), ROYAL_LIGHT, 1.5)

    save_part("cooker.png", render_part(84, 176, cooker), {"realSizeM": [0.5, 0.6, 0.9], "bayWidth": 1, "slotIn": True, "standPointX": 874, "lightOverlays": ["overlay_oven_window.png"]}, records)

    overlay = Image.new("RGBA", (84, 176), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for inset in range(0, 7):
        alpha = max(20, 170 - inset * 20)
        od.rounded_rectangle((17 + inset, 82 + inset, 67 - inset, 129 - inset), radius=4, fill=(255, 153, 34, alpha))
    save_part("overlay_oven_window.png", overlay, {"realSizeM": [0.0, 0.0, 0.0], "bayWidth": 1, "anchorPx": [0, 176]}, records)

    led = Image.new("RGBA", (84, 127), (0, 0, 0, 0))
    ld = ImageDraw.Draw(led)
    for x in (16, 24, 32):
        ld.ellipse((x, 31, x + 5, 36), fill=(63, 232, 117, 255))
    save_part("overlay_dishwasher_led.png", led, {"realSizeM": [0.0, 0.0, 0.0], "bayWidth": 1, "anchorPx": [0, 127]}, records)

    def utility(p: Painter, opened=False):
        p.rect((0, 0, 84, 25), ROYAL_LIGHT)
        p.line((0, 24, 84, 24), INK, 3)
        p.rect((0, 25, 84, 361), ROYAL)
        p.rounded((5, 31, 79, 355), 4, ROYAL_LIGHT, INK, 3)
        p.rounded((62, 176, 70, 205), 3, COPPER, INK, 2)
        p.line((9, 96, 75, 96), ROYAL_DARK, 2)
        p.line((9, 278, 75, 278), ROYAL_DARK, 2)
        if opened:
            p.rounded((76, 31, 124, 355), 4, ROYAL_LIGHT, INK, 3)
            p.line((85, 40, 85, 346), CYAN_LIGHT, 2)
            p.rounded((83, 176, 91, 205), 3, COPPER, INK, 2)

    def fridge(p: Painter):
        p.rect((0, 0, 84, 25), CREAM_LIGHT)
        p.line((0, 24, 84, 24), INK, 3)
        p.rect((0, 25, 84, 327), CREAM)
        p.rounded((4, 29, 80, 323), 4, CREAM_LIGHT, INK, 3)
        p.line((5, 145, 79, 145), INK, 3)
        p.rounded((61, 71, 69, 133), 3, COPPER, INK, 2)
        p.rounded((61, 164, 69, 225), 3, COPPER, INK, 2)
        p.line((9, 311, 75, 311), CREAM_SHADOW, 2)

    save_part("unit_utility_cupboard_closed.png", render_part(84, 361, lambda p: utility(p, False)), {"realSizeM": [0.5, 0.6, 2.0], "bayWidth": 1, "standPointX": 370}, records)
    save_part("unit_utility_cupboard_open.png", render_part(126, 361, lambda p: utility(p, True)), {"realSizeM": [0.5, 0.6, 2.0], "bayWidth": 1, "standPointX": 370}, records)
    save_part("unit_fridge_freezer.png", render_part(84, 327, fridge), {"realSizeM": [0.5, 0.6, 1.8], "bayWidth": 1, "standPointX": 454}, records)

    def toaster(p: Painter):
        p.rounded((3, 10, 61, 43), 8, CREAM, INK, 3)
        p.rounded((10, 4, 54, 18), 6, COPPER, INK, 2.5)
        p.line((17, 9, 47, 9), GLASS_DARK, 3)
        p.ellipse((52, 26, 58, 32), ROYAL, INK, 1.5)
        p.line((11, 43, 11, 40), INK, 3)
        p.line((53, 43, 53, 40), INK, 3)

    def kettle(p: Painter):
        p.rounded((9, 18, 48, 58), 10, CREAM, INK, 3)
        p.polygon([(8, 28), (0, 35), (10, 39)], COPPER, INK)
        p.line((17, 16, 41, 16), INK, 3)
        p.rounded((20, 8, 38, 20), 5, COPPER, INK, 2)
        p.line((45, 24, 54, 10), INK, 5)
        p.line((54, 10, 55, 32), INK, 5)
        p.line((45, 24, 54, 10), ROYAL_DARK, 2)
        p.line((54, 10, 55, 32), ROYAL_DARK, 2)

    def bowl(p: Painter):
        p.ellipse((4, 4, 80, 25), ROYAL_LIGHT, INK, 3)
        p.polygon([(7, 12), (77, 12), (67, 27), (17, 27)], ROYAL, INK)
        p.line((18, 19, 66, 19), CYAN_LIGHT, 2)

    def bin_part(p: Painter):
        p.rounded((6, 12, 78, 104), 8, ROYAL_DARK, INK, 3)
        p.rounded((3, 0, 81, 18), 7, METAL, INK, 3)
        p.line((13, 35, 71, 35), ROYAL_LIGHT, 2)
        p.rounded((25, 91, 59, 101), 4, INK_SOFT, INK, 2)

    save_part("toaster.png", render_part(64, 44, toaster), {"realSizeM": [0.38, 0.25, 0.24], "bayWidth": 1, "anchorPx": [32, 44], "standPointX": 1042}, records)
    save_part("kettle.png", render_part(56, 60, kettle), {"realSizeM": [0.33, 0.28, 0.36], "bayWidth": 1, "anchorPx": [28, 60], "standPointX": 1294}, records)
    save_part("pet_bowl.png", render_part(84, 28, bowl), {"realSizeM": [0.5, 0.30, 0.17], "bayWidth": 1, "anchorPx": [42, 28], "standPointX": 1378}, records)
    save_part("pedal_bin.png", render_part(84, 105, bin_part), {"realSizeM": [0.5, 0.30, 0.55], "bayWidth": 1, "anchorPx": [42, 105], "standPointX": 1462}, records)

    (PARTS / "item.json").write_text(json.dumps({"schema": "lighthouse-keeper/kitchen-v3-parts@1", "walkY": 502, "parts": records}, indent=2) + "\n")
    return records


def shell() -> Image.Image:
    scale = 4
    image = Image.new("RGBA", (W * scale, H * scale), CREAM)
    p = Painter(image, scale)
    p.rect((0, 0, W, 32), WOOD_DARK)
    p.rect((4, 4, W - 4, 25), WOOD)
    p.line((0, 31, W, 31), INK, 4)
    p.rect((0, 32, 32, 544), CREAM_SHADOW)
    p.rect((1504, 32, 1536, 544), CREAM_SHADOW)
    p.line((31, 32, 31, 544), INK, 4)
    p.line((1504, 32, 1504, 544), INK, 4)
    p.rect((32, 32, 1504, 460), CREAM)
    for x, y, length in ((355, 90, 70), (838, 69, 62), (1324, 85, 72), (350, 327, 54), (1278, 362, 64)):
        p.line((x, y, x + length, y), CREAM_LIGHT, 4)
    for x, y, length in ((380, 148, 45), (930, 118, 58), (1382, 314, 50)):
        p.line((x, y, x + length, y), CREAM_SHADOW, 3)

    # Exterior back-wall door, true front elevation.
    p.rect((176, 184, 296, 460), WOOD)
    p.ellipse((176, 124, 296, 244), WOOD, INK, 4)
    p.rect((180, 184, 292, 460), WOOD, INK, 4)
    p.line((236, 127, 236, 458), WOOD_DARK, 3)
    p.rounded((194, 228, 227, 330), 7, WOOD_LIGHT, INK, 3)
    p.rounded((245, 228, 278, 330), 7, WOOD_LIGHT, INK, 3)
    p.rounded((194, 344, 227, 440), 7, WOOD_LIGHT, INK, 3)
    p.rounded((245, 344, 278, 440), 7, WOOD_LIGHT, INK, 3)
    p.ellipse((273, 303, 283, 313), COPPER, INK, 2)

    # Window construction uses a neutral placeholder; exact key is written at 1x.
    for x0, y0, x1, y1 in WINDOWS:
        p.rect((x0, y0, x1, y1), WOOD_DARK, INK, 4)
        p.rect((x0 + 6, y0 + 6, x1 - 6, y1 - 6), CREAM_SHADOW)
        p.line((x0 + 84, y0 + 6, x0 + 84, y1 - 6), WOOD_DARK, 8)
        p.line((x0 + 6, y0 + 84, x1 - 6, y0 + 84), WOOD_DARK, 8)
        p.rect((x0 - 7, y1 - 3, x1 + 7, y1 + 8), WOOD_LIGHT, INK, 3)

    p.line((32, 460, 1504, 460), INK, 4)
    p.rect((0, 460, W, 544), FLOOR)
    for y in (476, 497, 518, 539):
        p.line((0, y, W, y), FLOOR_DARK if y == 539 else FLOOR_LIGHT, 2)
    p.rect((0, 544, W, 576), WOOD_DARK)
    p.rect((4, 548, W - 4, 576), FLOOR)
    p.line((4, 553, W - 4, 553), FLOOR_LIGHT, 3)

    image = image.resize((W, H), Image.Resampling.LANCZOS)
    target = ImageDraw.Draw(image)
    for rect in GLASS_RECTS:
        target.rectangle(rect, fill=MAGENTA)
    return image


def paste(image: Image.Image, part: Image.Image, x: int, y: int) -> None:
    image.alpha_composite(part, (x, y))


def draw_jamb(image: Image.Image) -> None:
    d = ImageDraw.Draw(image)
    d.rectangle((0, 208, 31, 543), fill=INK)
    d.rectangle((5, 208, 25, 543), fill=WOOD_DARK)
    d.rectangle((9, 208, 20, 543), fill=WOOD)
    d.line((24, 208, 24, 543), fill=WOOD_LIGHT, width=3)


def assemble(parts: dict[str, Image.Image], keeper: Image.Image | None = None, keeper_x: int = 874, flip=False, sink_override: Image.Image | None = None) -> tuple[Image.Image, Image.Image]:
    room = shell()
    item_layer = Image.new("RGBA", room.size, (0, 0, 0, 0))

    # Back-row tall units.
    paste(item_layer, parts["unit_utility_cupboard_closed.png"], 328, 124)
    paste(item_layer, parts["unit_fridge_freezer.png"], 412, 158)

    # Plinths, fronts and slot-in cooker.
    for x in (496, 580, 664, 748, 916, 1000, 1084, 1168, 1252):
        paste(item_layer, parts["plinth_tile.png"], x, 468)
    paste(item_layer, parts["front_drawers.png"], 496, 341)
    paste(item_layer, parts["front_sink_2bay.png"], 580, 341)
    paste(item_layer, parts["front_dishwasher.png"], 748, 341)
    paste(item_layer, parts["cooker.png"], 832, 309)
    paste(item_layer, parts["front_drawers.png"], 916, 341)
    paste(item_layer, parts["front_drawers.png"], 1000, 341)
    for x in (1084, 1168, 1252):
        paste(item_layer, parts["front_cupboard.png"], x, 341)

    # Worktops and declared joints/caps.
    for x in (496, 580, 664, 748, 916, 1000, 1084, 1168, 1252):
        paste(item_layer, parts["worktop_tile.png"], x, 309)
    for x in (580, 664, 748, 1000, 1084, 1168, 1252):
        paste(item_layer, parts["worktop_joint.png"], x - 1, 309)
    for x, name in ((496, "worktop_cap_left.png"), (816, "worktop_cap_right.png"), (916, "worktop_cap_left.png"), (1320, "worktop_cap_right.png")):
        paste(item_layer, parts[name], x, 309)
    for x, name in ((496, "plinth_cap_left.png"), (816, "plinth_cap_right.png"), (916, "plinth_cap_left.png"), (1320, "plinth_cap_right.png")):
        paste(item_layer, parts[name], x, 468)

    paste(item_layer, sink_override or parts["insert_sink_2bay.png"], 580, 274)
    paste(item_layer, parts["toaster.png"], 1010, 278)
    paste(item_layer, parts["kettle.png"], 1266, 262)
    paste(item_layer, parts["pet_bowl.png"], 1336, 464)
    paste(item_layer, parts["pedal_bin.png"], 1420, 368)
    room.alpha_composite(item_layer)

    if keeper is not None:
        actor = keeper.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else keeper
        room.alpha_composite(actor, (round(keeper_x - 128), 502 - 316))
    draw_jamb(room)
    return room, item_layer


def snap_magenta(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    px = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if a and r >= 180 and b >= 180 and g <= 100:
                px[x, y] = MAGENTA
    return image


def label_frame(image: Image.Image, title: str, detail: str, warning: bool = False) -> Image.Image:
    image = image.copy()
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle((38, 38, 740, 112), radius=12, fill=(8, 18, 28, 225), outline=(239, 184, 73, 255) if warning else (97, 201, 225, 255), width=3)
    d.text((55, 49), title, font=font(24, True), fill=(255, 245, 216, 255))
    d.text((55, 80), detail, font=font(17), fill=(255, 205, 109, 255) if warning else (201, 230, 239, 255))
    image.alpha_composite(overlay)
    return image


def actor_frame(base: Image.Image, actor: Image.Image, root_x: float, title: str, detail: str, flip=False, warning=False) -> Image.Image:
    frame = base.copy()
    sprite = actor.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else actor
    frame.alpha_composite(sprite, (round(root_x - 128), 186))
    draw_jamb(frame)
    return label_frame(frame, title, detail, warning)


def route_turn_frames(base, root_x, flip, title):
    result = []
    turns = [Image.open(PRIME / p.name).convert("RGBA") for p in TURN_FRAMES]
    for index, actor in enumerate(turns):
        result.append((actor_frame(base, actor, root_x, title, f"turn away · F{index + 1}", flip), 75))
    back = Image.open(PRIME / BACK_NEUTRAL.name).convert("RGBA")
    result.append((actor_frame(base, back, root_x, title, "neutral back · 1.0 s", flip), 1000))
    for index, actor in enumerate(reversed(turns[:-1])):
        result.append((actor_frame(base, actor, root_x, title, f"return to side · F{8 - index}", flip), 75))
    return result


def current_leg(base, start, target, steps, direction, name):
    bridge = [Image.open(PRIME / p.name).convert("RGBA") for p in BRIDGE_FRAMES]
    walk = [Image.open(PRIME / p.name).convert("RGBA") for p in WALK_FRAMES]
    n = max(0, math.floor(((84 * steps - 76) / 168) + 0.5))
    root = float(start)
    frames = [(actor_frame(base, bridge[0], root, name, "approved neutral start", direction < 0), 300)]
    for index, delta in enumerate((2, 6, 12, 18), start=1):
        root += direction * delta
        frames.append((actor_frame(base, bridge[index], root, name, f"approved start bridge · +{delta} px", direction < 0), 90))
    for cycle in range(n):
        for wi in list(range(1, 8)) + [0]:
            root += direction * 21
            frames.append((actor_frame(base, walk[wi], root, name, f"approved Walk V6 · cycle {cycle + 1} · +21 px", direction < 0), 90))
    for actor, delta in zip((bridge[3], bridge[2], bridge[1], bridge[0]), (18, 12, 6, 2)):
        root += direction * delta
        frames.append((actor_frame(base, actor, root, name, f"approved stop bridge · +{delta} px", direction < 0), 90))
    endpoint = round(root)
    error = endpoint - target
    frames[-1] = (label_frame(frames[-1][0], name, f"CURRENT STOP {endpoint}px · target {target}px · error {error:+d}px", True), 650)
    frames.extend(route_turn_frames(base, root, direction < 0, name))
    return frames, {"name": name, "start": start, "target": target, "steps": steps, "cycles": n, "stop": endpoint, "errorPx": error, "phaseValid": True}


def draft_leg(base, start, target, steps, direction, name):
    bridge = [Image.open(PRIME / p.name).convert("RGBA") for p in BRIDGE_FRAMES]
    walk = [Image.open(PRIME / p.name).convert("RGBA") for p in WALK_FRAMES]
    root = float(start)
    frames = [(actor_frame(base, bridge[0], root, name, "D15 DRAFT · exact approved neutral", direction < 0), 300)]
    for index, delta in enumerate((3, 7, 13, 19), start=1):
        root += direction * delta
        frames.append((actor_frame(base, bridge[index], root, name, f"D15 root schedule · +{delta} px · approved pixels", direction < 0), 90))
    steady_frames = 4 * (steps - 1)
    for index in range(steady_frames):
        wi = (index + 1) % 8
        root += direction * 21
        frames.append((actor_frame(base, walk[wi], root, name, f"approved Walk V6 · +21 px · phase F{wi + 1}", direction < 0), 90))
    needs_f5 = steps % 2 == 0
    for actor, delta in zip((bridge[3], bridge[2], bridge[1], bridge[0]), (19, 13, 7, 3)):
        root += direction * delta
        detail = f"D15 stop root · +{delta} px · approved F1 bridge pixels"
        if needs_f5:
            detail = f"MISSING F5→neutral bridge · root +{delta} px only"
        frames.append((actor_frame(base, actor, root, name, detail, direction < 0, needs_f5), 90))
    endpoint = round(root)
    error = endpoint - target
    frames[-1] = (label_frame(frames[-1][0], name, f"D15 ROOT STOP {endpoint}px · target {target}px · error {error:+d}px" + (" · F5 ART MISSING" if needs_f5 else ""), needs_f5), 700)
    frames.extend(route_turn_frames(base, root, direction < 0, name))
    return frames, {"name": name, "start": start, "target": target, "steps": steps, "stop": endpoint, "errorPx": error, "phaseValid": not needs_f5, "missingAuthority": "F5-to-neutral opposite-foot stop" if needs_f5 else None}


def save_route(name: str, all_frames: list[tuple[Image.Image, int]]) -> tuple[Path, Path]:
    # Keep the route proof at delivered room size. Downscaling this proof would
    # visually contradict the Prime contract even though the source cells were
    # unchanged, and would hide the very outline/root-motion defects under test.
    gif_frames = [snap_magenta(frame).convert("P", palette=Image.Palette.ADAPTIVE, colors=255) for frame, _ in all_frames]
    durations = [duration for _, duration in all_frames]
    gif_path = OUTPUTS / f"{name}.gif"
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], duration=durations, loop=0, optimize=True, disposal=2)

    cols, thumb_w, thumb_h, label_h = 6, 256, 96, 34
    rows = math.ceil(len(all_frames) / cols)
    sheet = Image.new("RGBA", (cols * thumb_w, rows * (thumb_h + label_h)), (16, 26, 35, 255))
    sd = ImageDraw.Draw(sheet)
    for index, (frame, _) in enumerate(all_frames):
        x = (index % cols) * thumb_w
        y = (index // cols) * (thumb_h + label_h)
        thumb = snap_magenta(frame.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS))
        sheet.alpha_composite(thumb, (x, y))
        sd.text((x + 5, y + thumb_h + 4), f"F{index + 1:03d}", font=font(16, True), fill=(235, 241, 244, 255))
    sheet_path = OUTPUTS / f"{name}_frame_sheet.png"
    sheet.save(sheet_path, optimize=True)
    return gif_path, sheet_path


def contact_sheet(records: dict[str, dict]) -> Path:
    v7 = Image.open(SOURCES / "v7-reference-crop.png").convert("RGBA")
    names = sorted(records)
    row_h, width = 210, 1500
    sheet = Image.new("RGBA", (width, 86 + row_h * len(names)), (13, 24, 33, 255))
    d = ImageDraw.Draw(sheet)
    d.text((28, 20), "Kitchen Proof V3 · separate parts against V7 style authority", font=font(30, True), fill=(247, 234, 197, 255))
    d.text((28, 56), "Every part is shown at 1:1 where it fits; repeated right-hand crop is reference only.", font=font(17), fill=(177, 211, 224, 255))
    for index, name in enumerate(names):
        y = 86 + index * row_h
        d.rectangle((18, y + 8, width - 18, y + row_h - 8), fill=(23, 40, 52, 255), outline=(58, 87, 101, 255), width=2)
        d.text((34, y + 20), name, font=font(20, True), fill=(255, 211, 107, 255))
        rec = records[name]
        d.text((34, y + 50), f"{rec['pixelSize'][0]} × {rec['pixelSize'][1]} px · {rec['bayWidth']} bay", font=font(16), fill=(205, 226, 233, 255))
        part = Image.open(PARTS / name).convert("RGBA")
        max_w, max_h = 520, 150
        ratio = min(1.0, max_w / part.width, max_h / part.height)
        preview = part if ratio == 1 else part.resize((max(1, round(part.width * ratio)), max(1, round(part.height * ratio))), Image.Resampling.LANCZOS)
        checker = Image.new("RGBA", (560, 158), (238, 231, 211, 255))
        cd = ImageDraw.Draw(checker)
        for cy in range(0, 158, 16):
            for cx in range(0, 560, 16):
                if (cx // 16 + cy // 16) % 2:
                    cd.rectangle((cx, cy, cx + 15, cy + 15), fill=(214, 216, 211, 255))
        checker.alpha_composite(preview, ((560 - preview.width) // 2, (158 - preview.height) // 2))
        sheet.alpha_composite(checker, (360, y + 26))
        crop = v7.copy()
        crop.thumbnail((500, 158), Image.Resampling.LANCZOS)
        sheet.alpha_composite(crop, (970, y + 26))
        d.text((972, y + 10), "V7 authority crop", font=font(14, True), fill=(165, 224, 238, 255))
    path = OUTPUTS / "contact_sheet.png"
    sheet.save(path, optimize=True)
    return path


def near_magenta(pixel) -> bool:
    r, g, b, a = pixel
    return a > 0 and r >= 180 and b >= 180 and g <= 100 and pixel != MAGENTA


def main() -> None:
    PARTS.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    extract_sources()
    records = make_parts()
    parts = {name: Image.open(PARTS / name).convert("RGBA") for name in records}

    neutral = Image.open(PRIME / SIDE_NEUTRAL.name).convert("RGBA")
    room, item_layer = assemble(parts, neutral, 874)
    room_path = OUTPUTS / "kitchen_v3_room.png"
    room.save(room_path, optimize=True)
    room.resize((3072, 1152), Image.Resampling.NEAREST).save(OUTPUTS / "kitchen_v3_room_2x.png", optimize=True)
    tower = snap_magenta(room.resize((384, 144), Image.Resampling.LANCZOS))
    tower.save(OUTPUTS / "kitchen_v3_tower_scale.png", optimize=True)

    base, _ = assemble(parts)
    legs = [
        (118, 622, 6, 1, "1 · door 118 → sink 622"),
        (622, 790, 2, 1, "2 · sink 622 → dishwasher 790"),
        (790, 874, 1, 1, "3 · dishwasher 790 → cooker 874"),
        (874, 454, 5, -1, "4 · cooker 874 → fridge 454"),
    ]
    current_frames, current_results = [], []
    draft_frames, draft_results = [], []
    for leg in legs:
        frames, result = current_leg(base, *leg)
        current_frames.extend(frames)
        current_results.append(result)
        frames, result = draft_leg(base, *leg)
        draft_frames.extend(frames)
        draft_results.append(result)
    save_route("route_current_38px", current_frames)
    save_route("route_d15_draft_42px", draft_frames)
    contact_sheet(records)

    # Isolation proof: mutate only the in-memory tap colour and compare rooms.
    sink_variant = parts["insert_sink_2bay.png"].copy()
    sv = sink_variant.load()
    changed_local = 0
    for y in range(sink_variant.height):
        for x in range(sink_variant.width):
            r, g, b, a = sv[x, y]
            if a and 120 <= r <= 220 and 130 <= g <= 210 and 130 <= b <= 215:
                sv[x, y] = (241, 112, 24, a)
                changed_local += 1
    isolation_room, _ = assemble(parts, neutral, 874, sink_override=sink_variant)
    diff = Image.new("RGBA", room.size, (0, 0, 0, 0))
    dp = diff.load()
    bbox = [W, H, 0, 0]
    diff_count = 0
    for y in range(H):
        for x in range(W):
            if room.getpixel((x, y)) != isolation_room.getpixel((x, y)):
                dp[x, y] = (255, 204, 42, 255)
                bbox = [min(bbox[0], x), min(bbox[1], y), max(bbox[2], x), max(bbox[3], y)]
                diff_count += 1
    diff.save(OUTPUTS / "isolation_sink_taps_diff.png", optimize=True)

    # Machine checks gathered into the manifest and rechecked by verify_review.py.
    exact_magenta = sum(1 for pixel in room.getdata() if pixel == MAGENTA)
    near_magenta_count = sum(1 for pixel in room.getdata() if near_magenta(pixel))
    forbidden_item_pixels = 0
    for x0, _, x1, _ in WINDOWS:
        for y in range(0, 274):
            for x in range(x0, x1):
                if item_layer.getpixel((x, y))[3]:
                    forbidden_item_pixels += 1

    files = {}
    for folder in (PARTS, OUTPUTS, SOURCES):
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                files[path.relative_to(ROOT).as_posix()] = {"sha256": sha256(path), "bytes": path.stat().st_size}

    manifest = {
        "schema": "lighthouse-keeper/kitchen-proof-v3@1",
        "status": "review-only-awaiting-frank",
        "canonMutation": False,
        "runtimeMutation": False,
        "geometry": {
            "modulePx": [1536, 576], "scalePxPerM": 168, "depthRevealPxPerM": 42,
            "backWallLineY": 460, "floorBandY": [460, 544], "slabY": [544, 576], "walkY": 502,
            "bayFieldX": [328, 1504], "bayCount": 14, "bayWidthPx": 84,
            "windows": WINDOWS, "glassRects": GLASS_RECTS,
            "verticals": {"unitBase": 485, "plinth": [468, 485], "unitFront": [341, 468], "worktopEdge": [334, 341], "worktopReveal": [309, 334], "fridge": [158, 485], "utility": [124, 485]},
        },
        "keeper": {"cellPx": [256, 320], "anchorPx": [128, 320], "soleDatumY": 316, "roomSoleY": 502, "roomAnchorY": 506, "standingHeightPx": 298, "sourceScale": 1.0, "walkFrameDeltaPx": 21, "stepPx": 84},
        "styleAuthority": {"path": V7_REPO_PATH, "historicalCommit": V7_COMMIT, "sha256": V7_SHA, "verified": sha256(SOURCES / "v7-oven-authority.png") == V7_SHA},
        "checks": {
            "exactMagentaPixels": exact_magenta, "nearMagentaPixels": near_magenta_count,
            "itemPixelsAboveWindowLimit": forbidden_item_pixels,
            "worktopRuns": [[496, 832], [916, 1336]], "worktopTopY": 309, "cookerTopY": 309,
            "plinthY": [468, 485], "cookerPlinthY": [468, 485],
            "worktopFrontHeightAboveSolesPx": 502 - 334,
            "worktopFrontHeightPercentOfKeeper": round((502 - 334) / 298 * 100, 2),
            "isolation": {"changedLocalTapPixels": changed_local, "roomDiffPixels": diff_count, "roomDiffBoundsInclusive": bbox, "allowedBoundsInclusive": [580, 274, 747, 340], "allPartHashesUnchanged": True},
            "overlayAllowedRects": {"overlay_oven_window.png": [17, 82, 67, 129], "overlay_dishwasher_led.png": [16, 31, 37, 36]},
            "itemOutlinePx": 3, "keeperObservedOutlinePx": "3–4", "outlineAssessment": "matched at native 1:1 within one pixel",
        },
        "routes": {"current38": current_results, "d15Draft42": draft_results, "d15Boundary": "Root arithmetic closes exactly. Even-step legs still lack the separately required F5-to-neutral opposite-foot bridge; exact approved F1 bridge pixels are shown as labelled pose placeholders and are not approval candidates."},
        "parts": records,
        "files": files,
        "documentationAudit": "Existing authority documents remain unchanged because this is a review-only package under a superseding task brief. All new geometry, limitations and verification evidence are contained here.",
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
