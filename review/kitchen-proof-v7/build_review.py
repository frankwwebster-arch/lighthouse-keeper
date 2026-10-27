#!/usr/bin/env python3
"""Build and verify the Kitchen V7 whole-room pre-cut review.

The room is generated freely.  This script supplies only the immutable room
shell, restores exact structural pixels, composites the unchanged Prime Keeper
for scale, and makes review comparisons.  It never cuts an item or door.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCES = HERE / "sources"
OUTPUTS = HERE / "outputs"

ROOM_W, ROOM_H = 2048, 576
AUTHOR_W, AUTHOR_H = ROOM_W * 2, ROOM_H * 2
MAGENTA = (255, 0, 255)
INK = (20, 27, 38)

WINDOWS = ((622, 790), (1294, 1462))
PANES = (
    (632, 116, 701, 185), (711, 116, 780, 185),
    (632, 195, 701, 264), (711, 195, 780, 264),
    (1304, 116, 1373, 185), (1383, 116, 1452, 185),
    (1304, 195, 1373, 264), (1383, 195, 1452, 264),
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Verdana Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Verdana.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def build_shell_2x() -> Path:
    SOURCES.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (AUTHOR_W, AUTHOR_H), (248, 232, 194))
    draw = ImageDraw.Draw(image)

    def s(value: int) -> int:
        return value * 2

    # Structural bands.
    draw.rectangle((0, 0, AUTHOR_W - 1, s(32) - 1), fill=(113, 57, 27), outline=INK, width=7)
    draw.rectangle((0, s(32), AUTHOR_W - 1, s(460) - 1), fill=(248, 232, 194))
    draw.rectangle((0, s(544), AUTHOR_W - 1, AUTHOR_H - 1), fill=(105, 59, 31), outline=INK, width=7)
    draw.rectangle((0, s(208), s(32) - 1, s(544) - 1), fill=(151, 83, 37), outline=INK, width=7)
    draw.rectangle((s(2016), s(208), AUTHOR_W - 1, s(544) - 1), fill=(151, 83, 37), outline=INK, width=7)

    # Flat checkerboard floor: two equal rows, no convergence.
    tile = 42
    for row, y in enumerate(range(460, 544, tile)):
        for col, x in enumerate(range(32, 2016, tile)):
            colour = (244, 239, 220) if (row + col) % 2 == 0 else (31, 37, 43)
            draw.rectangle((s(x), s(y), s(min(x + tile, 2016)), s(min(y + tile, 544))), fill=colour)
    draw.line((s(32), s(460), s(2016), s(460)), fill=INK, width=6)

    # Exact timber windows and hard key-colour panes.
    for x0, x1 in WINDOWS:
        draw.rectangle((s(x0), s(106), s(x1), s(274)), fill=(142, 70, 28), outline=INK, width=8)
    for x0, y0, x1, y1 in PANES:
        draw.rectangle((s(x0), s(y0), s(x1) - 1, s(y1) - 1), fill=MAGENTA, outline=INK, width=5)

    out = SOURCES / "structural-shell-2x.png"
    image.save(out, optimize=True)
    return out


def normalize_generated(raw: Image.Image) -> Image.Image:
    raw = raw.convert("RGB")
    target_ratio = ROOM_W / ROOM_H
    ratio = raw.width / raw.height
    if ratio > target_ratio:
        crop_w = round(raw.height * target_ratio)
        left = (raw.width - crop_w) // 2
        raw = raw.crop((left, 0, left + crop_w, raw.height))
    elif ratio < target_ratio:
        crop_h = round(raw.width / target_ratio)
        top = (raw.height - crop_h) // 2
        raw = raw.crop((0, top, raw.width, top + crop_h))
    if raw.size != (ROOM_W, ROOM_H):
        raw = raw.resize((ROOM_W, ROOM_H), Image.Resampling.LANCZOS)
    return raw


def restore_structure(room: Image.Image, shell_2x: Image.Image) -> None:
    shell = shell_2x.resize((ROOM_W, ROOM_H), Image.Resampling.LANCZOS)
    # Bands and side jambs are immutable shell pixels.
    room.paste(shell.crop((0, 0, ROOM_W, 32)), (0, 0))
    room.paste(shell.crop((0, 544, ROOM_W, 576)), (0, 544))
    room.paste(shell.crop((0, 208, 32, 544)), (0, 208))
    room.paste(shell.crop((2016, 208, 2048, 544)), (2016, 208))
    # The whole window rectangles are structural authority; furniture may not
    # overlap them, so restoring them cannot erase valid item art.
    for x0, x1 in WINDOWS:
        room.paste(shell.crop((x0, 106, x1, 274)), (x0, 106))

    # Make the eight panes exact and remove near-magenta edge colours.
    draw = ImageDraw.Draw(room)
    for x0, y0, x1, y1 in PANES:
        draw.rectangle((x0, y0, x1 - 1, y1 - 1), fill=MAGENTA)
    pixels = room.load()
    for x0, x1 in WINDOWS:
        for y in range(106, 274):
            for x in range(x0, x1):
                r, g, b = pixels[x, y]
                if r >= 200 and b >= 200 and g <= 80 and (r, g, b) != MAGENTA:
                    pixels[x, y] = INK


def composite_keeper(room: Image.Image) -> None:
    keeper_path = ROOT / "review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png"
    keeper = Image.open(keeper_path).convert("RGBA")
    assert keeper.size == (256, 320), keeper.size
    # Prime contract: cell anchor [128,320], opaque sole datum y=316.  Put the
    # sole on kitchen walkY=502 with no scaling.
    # Place him in the deliberately empty walk-in zone so every kitchen item,
    # especially the cooker controls and door window, remains reviewable.
    keeper_x = 250 - 128
    keeper_y = 502 - 316
    room.paste(keeper, (keeper_x, keeper_y), keeper)


def build_comparison(room: Image.Image) -> Path:
    calibration_path = ROOT / "review/kitchen-proof-v3-rebuild/sources/approved-style-calibration.png"
    calibration = Image.open(calibration_path).convert("RGB")
    calibration.thumbnail((ROOM_W, ROOM_H), Image.Resampling.LANCZOS)
    header = 84
    sheet = Image.new("RGB", (ROOM_W * 2, ROOM_H + header), (24, 29, 38))
    left_x = (ROOM_W - calibration.width) // 2
    left_y = header + (ROOM_H - calibration.height) // 2
    sheet.paste(calibration, (left_x, left_y))
    sheet.paste(room, (ROOM_W, header))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 22), "APPROVED LINE-QUALITY CALIBRATION", font=font(30, True), fill=(255, 244, 215))
    draw.text((ROOM_W + 24, 22), "KITCHEN V7 — FREE WHOLE-ROOM PAINT — PRE-CUT", font=font(30, True), fill=(255, 244, 215))
    out = OUTPUTS / "calibration-vs-kitchen-v7-precut.png"
    sheet.save(out, optimize=True)
    return out


def finalize(raw_path: Path) -> tuple[Path, Path]:
    shell_path = build_shell_2x()
    room = normalize_generated(Image.open(raw_path))
    restore_structure(room, Image.open(shell_path).convert("RGB"))
    composite_keeper(room)
    out = OUTPUTS / "kitchen-v7-free-room-with-prime-precut.png"
    room.save(out, optimize=True)
    comparison = build_comparison(room)
    return out, comparison


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize", type=Path)
    args = parser.parse_args()
    print(build_shell_2x())
    if args.finalize:
        for path in finalize(args.finalize):
            print(path)


if __name__ == "__main__":
    main()
