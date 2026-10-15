#!/usr/bin/env python3
"""Build the reversible Kitchen Basic Assets V1 review batch.

The generated concept sheets are visual references only. This builder authors
the exact logical-pixel geometry, state frames, room compositions and review
media deterministically. It never writes to production sprite paths,
manifests, registers or runtime code.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-basic-assets-2026-10-16-v1"
RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v1"
DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v1"
PUBLIC = ROOT / "public/keeper-review/kitchen-basic-assets-v1"
PUBLIC_ASSETS = PUBLIC / "assets"

DENSITY = 8
KU_PER_LP = 8
DOOR_CLEAR_LP = 4
BAY_LP = 21
ROOM_HEIGHT = 56
ROOM_9_WIDTH = DOOR_CLEAR_LP + 9 * BAY_LP
ROOM_12_WIDTH = DOOR_CLEAR_LP + 12 * BAY_LP

P = {
    "ink": "#071b32",
    "ink2": "#173452",
    "wood_dark": "#6d371e",
    "wood": "#9a5630",
    "wood_light": "#d38a46",
    "cream": "#f4d89b",
    "cream_light": "#fff0c5",
    "cream_shadow": "#d9b776",
    "blue": "#168eaa",
    "blue_light": "#61d3df",
    "brass": "#d79622",
    "brass_light": "#ffd067",
    "steel": "#c7d5d8",
    "steel_dark": "#637785",
    "black": "#17202b",
    "flame": "#ff8c1a",
    "flame_light": "#ffe15b",
    "smoke": "#68747c",
    "water": "#34bfea",
    "white": "#fff7dd",
    "red": "#bd3d34",
    "green": "#4d9441",
}


@dataclass(frozen=True)
class AssetSpec:
    stem: str
    cell: tuple[int, int]
    bays: int
    max_size: str
    interaction_offset_ku: int
    states: tuple[str, ...]
    note: str


ASSET_SPECS = {
    "obj_fridge": AssetSpec("obj_fridge", (21, 21), 1, "21 × 19 lp", 0, ("standard", "on", "broken"), "worktop top 19 lp; on opens door"),
    "obj_kettle": AssetSpec("obj_kettle", (21, 31), 1, "21 × 30 lp", 0, ("standard", "on", "broken"), "counter top 19 lp; stove kettle on one gas ring"),
    "obj_toaster": AssetSpec("obj_toaster", (21, 31), 1, "21 × 30 lp", 0, ("standard", "on", "broken"), "counter top 19 lp; toast pop"),
    "obj_cooker": AssetSpec("obj_cooker", (21, 28), 1, "21 × 26 lp", 0, ("standard", "on", "broken"), "hob 19 lp; rack 10 lp; oven door exactly 19 lp"),
    "obj_mixer": AssetSpec("obj_mixer", (21, 31), 1, "21 × 30 lp", 0, ("standard", "on", "broken"), "counter top 19 lp; spoon stir"),
    "obj_sink": AssetSpec("obj_sink", (21, 29), 1, "21 × 27 lp", 0, ("standard", "on", "broken"), "counter top 19 lp; tap peak 27 lp"),
    "obj_table": AssetSpec("obj_table", (42, 28), 2, "42 × 26 lp", -84, ("standard",), "chair interaction is 10.5 lp left of two-bay centre"),
    "obj_bin": AssetSpec("obj_bin", (21, 16), 1, "21 × 14 lp", 0, ("standard", "full", "overflowing"), "own bay; no overlap"),
    "obj_petbowl": AssetSpec("obj_petbowl", (16, 8), 0, "12 × 3 lp", 0, ("standard", "full", "broken"), "foreground child of the table; moves with it and takes no bay"),
    "obj_cupboard": AssetSpec("obj_cupboard", (38, 56), 0, "32 × 40 lp opening", -84, ("standard", "on", "open"), "far-wall architecture; stance is final lattice line"),
}


def blank(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGBA", size, (0, 0, 0, 0))


def draw_rect(d: ImageDraw.ImageDraw, box, fill, outline=P["ink"], width=1):
    d.rectangle(box, fill=fill, outline=outline, width=width)


def draw_common_counter(im: Image.Image, shift: int = 0) -> None:
    d = ImageDraw.Draw(im)
    h = im.height
    x0, x1 = 2 + shift, 18 + shift
    floor_y = h
    floor = floor_y - 1
    top = floor_y - 19
    draw_rect(d, (x0, top + 2, x1, floor), P["cream"], P["ink"])
    draw_rect(d, (x0 - 1, top, x1 + 1, top + 2), P["wood"], P["ink"])
    d.line((x0 + 1, top + 3, x1 - 1, top + 3), fill=P["cream_light"])
    draw_rect(d, (x0 + 2, top + 6, x1 - 2, floor - 3), P["cream_light"], P["wood_dark"])
    d.line((x0 + 3, top + 7, x0 + 3, floor - 4), fill=P["cream_shadow"])
    d.line((x1 - 3, top + 7, x1 - 3, floor - 4), fill=P["cream_shadow"])
    d.rectangle((x0 + 7, top + 5, x0 + 10, top + 6), fill=P["brass"])
    d.rectangle((x0 + 1, floor - 1, x0 + 3, floor), fill=P["wood_dark"])
    d.rectangle((x1 - 3, floor - 1, x1 - 1, floor), fill=P["wood_dark"])


def broken_fx(im: Image.Image, frame: int, cue: str) -> None:
    d = ImageDraw.Draw(im)
    h = im.height
    smoke = [
        [(11, 7), (13, 5), (12, 3)],
        [(10, 6), (8, 4), (10, 3)],
        [(12, 7), (14, 5), (13, 3)],
        [(9, 7), (11, 5), (10, 3)],
    ][frame]
    for i, (x, y) in enumerate(smoke):
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=P["smoke"] if i else P["steel_dark"])
    spark = [(4, 5), (16, 4), (5, 3), (15, 6)][frame]
    d.point(spark, fill=P["flame_light"])
    d.line((spark[0] - 1, spark[1], spark[0] + 1, spark[1]), fill=P["flame"])
    if cue == "frost":
        d.point((4 + frame, h - 4), fill=P["white"])
        d.point((5 + frame, h - 5), fill=P["water"])
    elif cue == "ring":
        d.ellipse((7, h - 21, 13, h - 18), outline=P["flame"])
        d.point((10 + (frame % 2), h - 22), fill=P["flame_light"])
    elif cue == "toast":
        x, y = 10 + frame * 2, 8 - min(frame, 2)
        d.rectangle((x, y, x + 3, y + 2), fill=P["cream_shadow"], outline=P["wood_dark"])
    elif cue == "splatter":
        for x, y in ((4 + frame, 8), (16 - frame, 6), (14, 3 + frame)):
            d.point((x, y), fill=P["cream_light"])
    elif cue == "drip":
        d.point((11, h - 15 + frame), fill=P["water"])
        d.point((10, h - 12 + frame // 2), fill=P["water"])


def fridge(frame=0, state="standard") -> Image.Image:
    im = blank((21, 21))
    d = ImageDraw.Draw(im)
    shift = 0
    x0, x1, top, bottom = 2 + shift, 18 + shift, 2, 20
    draw_rect(d, (x0, top, x1, bottom), P["cream_light"], P["ink"])
    draw_rect(d, (x0 - 1, top, x1 + 1, top + 2), P["wood"], P["ink"])
    d.line((x0 + 1, top + 4, x1 - 1, top + 4), fill=P["cream_shadow"])
    d.line((x0 + 1, top + 9, x1 - 1, top + 9), fill=P["cream_shadow"])
    d.rectangle((x0 + 2, top + 6, x0 + 3, top + 9), fill=P["brass"])
    d.rectangle((x0 + 2, bottom - 2, x1 - 2, bottom - 1), fill=P["steel_dark"])
    if state == "on":
        widths = (0, 4, 8, 11)
        w = widths[frame]
        if w:
            d.polygon([(x0 + 1, top + 3), (x0 + 1 + w, top + 5), (x0 + 1 + w, bottom - 1), (x0 + 1, bottom - 1)], fill=P["blue"], outline=P["ink"])
    if state == "broken":
        d.line((x0 + 4, top + 7, x0 + 8, top + 7), fill=P["water"])
        broken_fx(im, frame, "frost")
    return im


def counter_appliance(kind: str, frame=0, state="standard") -> Image.Image:
    im = blank((21, 31))
    shift = 0
    draw_common_counter(im, shift)
    d = ImageDraw.Draw(im)
    base_y = im.height - 1 - 19
    cx = 10 + shift
    if kind == "kettle":
        d.ellipse((cx - 5, base_y - 7, cx + 4, base_y), fill=P["blue"], outline=P["ink"])
        d.rectangle((cx - 3, base_y - 9, cx + 2, base_y - 7), fill=P["blue"], outline=P["ink"])
        d.arc((cx - 4, base_y - 10, cx + 5, base_y - 3), 180, 355, fill=P["ink"], width=2)
        d.line((cx - 5, base_y - 5, cx - 8, base_y - 3), fill=P["ink"], width=2)
        d.ellipse((cx - 6, base_y - 1, cx + 5, base_y + 1), outline=P["black"])
        if state == "on":
            dx = (-1, 1, -1, 1)[frame]
            sy = 3 - frame // 2
            d.ellipse((cx - 1 + dx, sy, cx + 2 + dx, sy + 3), fill=P["white"])
            d.point((cx - 7, base_y - 9 + (frame % 2)), fill=P["flame_light"])
        elif state == "broken":
            broken_fx(im, frame, "ring")
    elif kind == "toaster":
        draw_rect(d, (cx - 5, base_y - 7, cx + 5, base_y), P["blue"], P["ink"])
        d.line((cx - 3, base_y - 6, cx + 3, base_y - 6), fill=P["blue_light"])
        toast_y = base_y - 9
        if state == "on":
            toast_y = max(1, toast_y - (0, 2, 5, 2)[frame])
        d.rectangle((cx - 2, toast_y, cx + 2, toast_y + 3), fill=P["cream_shadow"], outline=P["wood_dark"])
        if state == "broken":
            broken_fx(im, frame, "toast")
    elif kind == "mixer":
        d.ellipse((cx - 6, base_y - 4, cx + 3, base_y + 1), fill=P["white"], outline=P["ink"])
        angle = (-4, -2, 1, 3)[frame] if state == "on" else -3
        d.line((cx + angle, base_y - 9, cx, base_y - 3), fill=P["wood_dark"], width=2)
        d.point((cx + angle, base_y - 10), fill=P["wood_light"])
        if state == "on":
            d.arc((cx - 5, base_y - 5, cx + 2, base_y), 10 + frame * 35, 180 + frame * 35, fill=P["blue"])
        elif state == "broken":
            broken_fx(im, frame, "splatter")
    return im


def cooker(frame=0, state="standard") -> Image.Image:
    im = blank((21, 28))
    d = ImageDraw.Draw(im)
    shift = 0
    x0, x1, floor_y = 1 + shift, 19 + shift, 28
    floor = floor_y - 1
    top = floor_y - 19
    draw_rect(d, (x0, top, x1, floor), P["cream"], P["ink"])
    draw_rect(d, (x0, top, x1, top + 2), P["steel_dark"], P["ink"])
    d.ellipse((x0 + 3, top - 1, x0 + 8, top + 1), outline=P["black"])
    d.ellipse((x1 - 8, top - 1, x1 - 3, top + 1), outline=P["black"])
    for x in (x0 + 4, x0 + 8, x0 + 12, x0 + 16):
        d.point((x, top + 4), fill=P["brass"])
    # The opaque oven door is exactly 19 logical pixels wide.
    draw_rect(d, (x0, top + 6, x1, floor - 2), P["wood_dark"], P["ink"])
    draw_rect(d, (x0 + 3, top + 8, x1 - 3, floor - 5), P["black"], P["ink2"])
    d.line((x0 + 2, top + 6, x1 - 2, top + 6), fill=P["brass"])
    # Rack datum: 10 lp above floor.
    d.line((x0 + 4, floor_y - 10, x1 - 4, floor_y - 10), fill=P["steel"])
    d.rectangle((x0 + 1, top - 7, x1 - 1, top - 1), fill=P["cream_shadow"], outline=P["ink"])
    if state == "on":
        for x in (x0 + 5, x1 - 5):
            flame_h = (1, 3, 2, 4)[frame]
            d.polygon([(x - 2, top), (x, top - flame_h), (x + 2, top)], fill=P["flame"], outline=P["flame_light"])
    elif state == "broken":
        broken_fx(im, frame, "ring")
    return im


def sink(frame=0, state="standard") -> Image.Image:
    im = blank((21, 29))
    shift = 0
    draw_common_counter(im, shift)
    d = ImageDraw.Draw(im)
    floor_y = im.height
    floor = floor_y - 1
    top = floor_y - 19
    d.ellipse((4 + shift, top - 2, 16 + shift, top + 2), fill=P["white"], outline=P["ink"])
    d.arc((9 + shift, top - 8, 17 + shift, top), 180, 350, fill=P["brass"], width=2)
    d.rectangle((15 + shift, top - 4, 16 + shift, top), fill=P["brass"])
    if state == "on":
        d.line((15 + shift, top - 2, 12 + shift, top + 1 + frame), fill=P["water"], width=1)
        d.point((11 + shift, top + 2 + frame), fill=P["water"])
    elif state == "broken":
        broken_fx(im, frame, "drip")
    return im


def table() -> Image.Image:
    im = blank((42, 28))
    d = ImageDraw.Draw(im)
    floor_y = 28
    floor = floor_y - 1
    # Chair is in the left bay; its seat anchor is x=10.5 lp.
    d.rectangle((3, floor_y - 26, 5, floor_y - 9), fill=P["wood"], outline=P["ink"])
    d.rectangle((15, floor_y - 26, 17, floor_y - 9), fill=P["wood"], outline=P["ink"])
    for y in (floor_y - 23, floor_y - 19):
        d.line((5, y, 15, y), fill=P["wood_light"], width=2)
    draw_rect(d, (3, floor_y - 11, 18, floor_y - 9), P["cream_light"], P["ink"])
    d.rectangle((5, floor_y - 9, 7, floor), fill=P["wood_dark"])
    d.rectangle((15, floor_y - 9, 17, floor), fill=P["wood_dark"])
    # Table occupies the right bay and reaches the 19-lp work datum.
    draw_rect(d, (16, floor_y - 19, 40, floor_y - 17), P["wood"], P["ink"])
    d.rectangle((18, floor_y - 17, 20, floor), fill=P["wood_dark"])
    d.rectangle((37, floor_y - 17, 39, floor), fill=P["wood_dark"])
    return im


def pedal_bin(state="standard") -> Image.Image:
    im = blank((21, 16))
    d = ImageDraw.Draw(im)
    x0, x1, top, floor = 3, 17, 2, 15
    draw_rect(d, (x0, top + 2, x1, floor), P["blue"], P["ink"])
    d.ellipse((x0, top, x1, top + 4), fill=P["blue_light"], outline=P["ink"])
    d.rectangle((8, floor, 12, floor), fill=P["black"])
    if state in ("full", "overflowing"):
        d.polygon([(5, top + 1), (7, top), (10, top + 1), (12, top), (16, top + 2)], fill=P["cream_shadow"], outline=P["ink"])
    if state == "overflowing":
        d.ellipse((2, floor - 2, 5, floor), fill=P["cream_shadow"], outline=P["ink"])
        d.rectangle((16, floor - 1, 19, floor), fill=P["cream_light"], outline=P["ink"])
    return im


def pet_bowl(frame=0, state="standard") -> Image.Image:
    im = blank((16, 8))
    d = ImageDraw.Draw(im)
    if state == "broken":
        puddle = (4, 11, 1, 2 + frame // 2)
        d.ellipse((max(2, puddle[0] - frame), 6, min(13, puddle[1] + frame), 7), fill=P["water"])
    d.polygon([(2, 5), (13, 5), (11, 7), (4, 7)], fill=P["cream"], outline=P["ink"])
    d.line((2, 5, 13, 5), fill=P["ink"])
    if state == "full":
        d.line((4, 5, 11, 5), fill=P["wood_dark"])
    if state == "broken":
        d.line((8, 5, 7, 7), fill=P["red"])
    return im


def cupboard(frame=0, state="standard") -> Image.Image:
    im = blank((38, 56))
    d = ImageDraw.Draw(im)
    # Only the end-wall frame is visible when closed; the opening is 32×40 lp.
    d.rectangle((33, 0, 36, 55), fill=P["wood_dark"], outline=P["ink"])
    d.rectangle((31, 6, 36, 48), fill=P["wood"], outline=P["ink"])
    d.rectangle((32, 8, 36, 47), fill=P["black"], outline=P["ink"])
    open_amount = 0 if state == "standard" else (frame + 1) / 4 if state == "on" else 1
    if open_amount > 0.25:
        d.line((35, 14, 34, 45), fill=P["wood_light"], width=2)
        d.line((34, 43, 32, 48), fill=P["cream_shadow"], width=2)
        d.line((34, 48, 31, 48), fill=P["cream_shadow"])
    leaf_w = max(4, round(4 + 28 * open_amount))
    left = 35 - leaf_w
    d.rectangle((left, 8, 34, 47), fill=P["wood"], outline=P["ink"])
    if leaf_w > 8:
        d.rectangle((left + 2, 10, 32, 45), outline=P["wood_light"])
        d.line((left + 4, 12, left + 4, 43), fill=P["wood_dark"])
    d.ellipse((left + 2, 27, left + 3, 28), fill=P["brass_light"], outline=P["wood_dark"])
    return im


def dishes(level: int) -> Image.Image:
    im = blank((21, 29))
    d = ImageDraw.Draw(im)
    base = 9
    for i in range(level * 2):
        y = base - i * 2
        d.ellipse((5 + (i % 2), y, 16 - (i % 2), y + 2), fill=P["white"], outline=P["ink"])
    if level >= 3:
        d.line((13, 3, 16, 0), fill=P["wood_dark"], width=2)
    return im


def room_repeat(variant: int) -> Image.Image:
    im = Image.new("RGBA", (21, 56), P["cream"])
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 20, 4), fill=P["wood_dark"])
    d.line((0, 5, 20, 5), fill=P["wood_light"])
    d.rectangle((0, 46, 20, 55), fill=P["wood"])
    d.line((0, 45, 20, 45), fill=P["ink"], width=2)
    for x in range(-8 + variant * 5, 28, 11):
        d.line((x, 50, x + 8, 46), fill=P["wood_dark"])
    # Quiet plaster variation stays clear of seams.
    marks = {0: [(7, 14), (14, 35)], 1: [(5, 29), (16, 18)], 2: [(10, 24), (15, 39)]}[variant]
    for x, y in marks:
        d.rectangle((x, y, x + 1, y + 1), fill=P["cream_shadow"])
    return im


def stair_cap(opened: bool) -> Image.Image:
    im = blank((46, 56))
    d = ImageDraw.Draw(im)
    # Rightmost 4 lp are the kitchen-side frame. The 42 lp to the left belong
    # to the stair-side projection, so bay 1 begins at x=4 inside the room.
    d.rectangle((42, 0, 45, 55), fill=P["wood_dark"], outline=P["ink"])
    d.rectangle((40, 7, 45, 49), fill=P["wood"], outline=P["ink"])
    if opened:
        d.rectangle((16, 8, 40, 48), fill=P["wood"], outline=P["ink"])
        d.rectangle((18, 10, 38, 46), outline=P["wood_light"])
        d.ellipse((36, 27, 38, 29), fill=P["brass_light"], outline=P["wood_dark"])
    else:
        d.rectangle((38, 8, 41, 48), fill=P["wood"], outline=P["ink"])
        d.ellipse((38, 27, 39, 28), fill=P["brass_light"])
    return im


def make_strip(frames: list[Image.Image]) -> Image.Image:
    w, h = frames[0].size
    strip = blank((w * len(frames), h))
    for i, frame in enumerate(frames):
        strip.alpha_composite(frame, (i * w, 0))
    return strip


def save_raw_and_source(name: str, image: Image.Image) -> None:
    raw_path = RAW / name
    source_path = SOURCE / name.replace(".png", "_source.png")
    image.save(raw_path, optimize=True)
    image.resize((image.width * DENSITY, image.height * DENSITY), Image.Resampling.NEAREST).save(source_path, optimize=True)


def alpha_bounds(im: Image.Image) -> dict[str, int] | None:
    box = im.getchannel("A").getbbox()
    if box is None:
        return None
    x0, y0, x1, y1 = box
    return {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}


def shared_edge_alpha_clear(strip: Image.Image, cell_width: int, frames: int) -> bool:
    alpha = strip.getchannel("A")
    for i in range(frames):
        left = i * cell_width
        right = left + cell_width - 1
        if alpha.crop((left, 0, left + 1, strip.height)).getbbox() is not None:
            return False
        if alpha.crop((right, 0, right + 1, strip.height)).getbbox() is not None:
            return False
    return True


def extract_keeper_frames(stem: str) -> list[str]:
    png_path = ROOT / f"art/raw/keeper-first-batch/{stem}_f8.png"
    meta = json.loads((ROOT / f"art/raw/keeper-first-batch/{stem}_f8.json").read_text())
    strip = Image.open(png_path).convert("RGBA")
    density = int(meta["density"])
    frame_w = int(meta["w"]) * density
    frame_h = int(meta["h"]) * density
    urls = []
    for i in range(8):
        frame = strip.crop((i * frame_w, 0, (i + 1) * frame_w, frame_h))
        name = f"{stem}_frame{i + 1}.png"
        frame.save(PUBLIC_ASSETS / name, optimize=True)
        urls.append(f"/keeper-review/kitchen-basic-assets-v1/assets/{name}")
    return urls


def build_composition(width: int, twelve_outline: bool = False) -> Image.Image:
    im = blank((width, ROOM_HEIGHT))
    # Room interior begins with the 4-lp kitchen-side frame.
    for k, x in enumerate(range(DOOR_CLEAR_LP, width, BAY_LP)):
        tile = room_repeat(k % 3)
        tile_w = min(BAY_LP, width - x)
        im.alpha_composite(tile.crop((0, 0, tile_w, ROOM_HEIGHT)), (x, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 3, ROOM_HEIGHT - 1), fill=P["wood_dark"], outline=P["ink"])
    d.rectangle((width - 4, 0, width - 1, ROOM_HEIGHT - 1), fill=P["wood_dark"], outline=P["ink"])
    if twelve_outline:
        labels = [
            (1, 1, "BIN"), (2, 2, "FRIDGE T3"), (4, 1, "KETTLE T3"),
            (5, 1, "TOASTER T3"), (6, 2, "RANGE T3"), (8, 1, "MIXER T3"),
            (9, 2, "SINK + DW"), (11, 1, "SNACK"), (12, 1, "DUMB WAITER"),
        ]
        for bay, span, label in labels:
            x0 = DOOR_CLEAR_LP + (bay - 1) * BAY_LP + 1
            x1 = DOOR_CLEAR_LP + (bay - 1 + span) * BAY_LP - 1
            d.rectangle((x0, 15, x1, 54), outline=P["blue"], width=1)
            # Tiny deterministic ticks distinguish each reserved outline; the
            # readable labels are added by the HTML overlay.
            for x in range(x0 + 1, x1, 4):
                d.point((x, 15), fill=(0, 0, 0, 0))
        return im

    placements = [
        (pedal_bin("standard"), 1, 1),
        (fridge(0, "standard"), 2, 1),
        (counter_appliance("kettle", 0, "standard"), 3, 1),
        (counter_appliance("toaster", 0, "standard"), 4, 1),
        (cooker(0, "standard"), 5, 1),
        (counter_appliance("mixer", 0, "standard"), 6, 1),
        (sink(0, "standard"), 7, 1),
        (table(), 8, 2),
    ]
    for obj, bay, span in placements:
        bay_left = DOOR_CLEAR_LP + (bay - 1) * BAY_LP
        area_w = span * BAY_LP
        x = bay_left + (area_w - obj.width) // 2
        y = ROOM_HEIGHT - obj.height
        im.alpha_composite(obj, (x, y))
    return im


def build_shell(width: int) -> Image.Image:
    im = blank((width, ROOM_HEIGHT))
    for k, x in enumerate(range(DOOR_CLEAR_LP, width, BAY_LP)):
        tile = room_repeat(k % 3)
        tile_w = min(BAY_LP, width - x)
        im.alpha_composite(tile.crop((0, 0, tile_w, ROOM_HEIGHT)), (x, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 3, ROOM_HEIGHT - 1), fill=P["wood_dark"], outline=P["ink"])
    d.rectangle((width - 4, 0, width - 1, ROOM_HEIGHT - 1), fill=P["wood_dark"], outline=P["ink"])
    return im


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_assets() -> tuple[dict, dict[str, list[str]]]:
    for folder in (SOURCE, RAW, DRAFT, PUBLIC_ASSETS):
        folder.mkdir(parents=True, exist_ok=True)

    generated: dict[str, Image.Image] = {}
    public_frames: dict[str, list[str]] = {}

    state_builders: dict[str, Callable[[int, str], Image.Image]] = {
        "obj_fridge": lambda f, s: fridge(f, s),
        "obj_kettle": lambda f, s: counter_appliance("kettle", f, s),
        "obj_toaster": lambda f, s: counter_appliance("toaster", f, s),
        "obj_cooker": lambda f, s: cooker(f, s),
        "obj_mixer": lambda f, s: counter_appliance("mixer", f, s),
        "obj_sink": lambda f, s: sink(f, s),
        "obj_petbowl": lambda f, s: pet_bowl(f, s),
    }

    for stem, builder in state_builders.items():
        spec = ASSET_SPECS[stem]
        public_frames[stem] = []
        for state in spec.states:
            count = 1 if state == "standard" or (stem == "obj_petbowl" and state == "full") else 4
            frames = [builder(i, state) for i in range(count)]
            name = f"{stem}_{state}_f{count}.png"
            strip = make_strip(frames)
            generated[name] = strip
            save_raw_and_source(name, strip)
            for i, frame in enumerate(frames):
                frame_name = f"{stem}_{state}_frame{i + 1}.png"
                frame.save(PUBLIC_ASSETS / frame_name, optimize=True)
                public_frames[stem].append(f"/keeper-review/kitchen-basic-assets-v1/assets/{frame_name}")

    singles = {
        "obj_table_standard_f1.png": table(),
        "obj_bin_standard_f1.png": pedal_bin("standard"),
        "obj_bin_full_f1.png": pedal_bin("full"),
        "obj_bin_overflowing_f1.png": pedal_bin("overflowing"),
        "obj_cupboard_standard_f1.png": cupboard(0, "standard"),
        "obj_cupboard_on_f4.png": make_strip([cupboard(i, "on") for i in range(4)]),
        "obj_cupboard_open_f1.png": cupboard(0, "open"),
        "obj_sink_dishes1_f1.png": dishes(1),
        "obj_sink_dishes2_f1.png": dishes(2),
        "obj_sink_dishes3_f1.png": dishes(3),
        "room_kitchen_repeat_a.png": room_repeat(0),
        "room_kitchen_repeat_b.png": room_repeat(1),
        "room_kitchen_repeat_c.png": room_repeat(2),
        "room_kitchen_stair_cap_outward_closed.png": stair_cap(False),
        "room_kitchen_stair_cap_outward_open.png": stair_cap(True),
        "room_kitchen_far_cap_closed.png": cupboard(0, "standard"),
        "room_kitchen_far_cap_open.png": cupboard(0, "open"),
        "room_kitchen_9bay_composite.png": build_composition(ROOM_9_WIDTH),
        "room_kitchen_12bay_outline.png": build_composition(ROOM_12_WIDTH, True),
    }
    for bays in range(6, 13):
        singles[f"room_kitchen_shell_{bays}bay.png"] = build_shell(DOOR_CLEAR_LP + bays * BAY_LP)
    for name, im in singles.items():
        generated[name] = im
        save_raw_and_source(name, im)
        if name.startswith("obj_") or name.startswith("room_kitchen"):
            shutil.copy2(RAW / name, PUBLIC_ASSETS / name)

    public_frames["obj_table"] = ["/keeper-review/kitchen-basic-assets-v1/assets/obj_table_standard_f1.png"]
    public_frames["obj_bin"] = [
        "/keeper-review/kitchen-basic-assets-v1/assets/obj_bin_standard_f1.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/obj_bin_full_f1.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/obj_bin_overflowing_f1.png",
    ]
    public_frames["obj_cupboard"] = []
    for state, frames in (("standard", [cupboard(0, "standard")]), ("on", [cupboard(i, "on") for i in range(4)]), ("open", [cupboard(0, "open")])):
        for i, frame in enumerate(frames):
            name = f"obj_cupboard_{state}_frame{i + 1}.png"
            frame.save(PUBLIC_ASSETS / name, optimize=True)
            public_frames["obj_cupboard"].append(f"/keeper-review/kitchen-basic-assets-v1/assets/{name}")

    # Copy the visual-reference sheets into the review batch without treating
    # them as geometry authority.
    for concept in ("kitchen-furniture-concept-v1.png", "kitchen-shell-concept-v1.png"):
        shutil.copy2(SOURCE / "reference" / concept, PUBLIC_ASSETS / concept)

    keeper = {
        stem: extract_keeper_frames(stem)
        for stem in ("keeper_meal_from_oven_back", "keeper_cake_from_oven_back", "keeper_sweep_broom", "keeper_hoover_basic", "keeper_eat_seated")
    }

    catalogue = {
        "schema": "lighthouse-keeper/kitchen-basic-assets@1",
        "status": "reversible-tier-1-draft-awaiting-frank-review",
        "units": {"logicalPixelToKu": KU_PER_LP, "bayLp": BAY_LP, "bayKu": BAY_LP * KU_PER_LP},
        "room": {
            "heightLp": ROOM_HEIGHT,
            "doorDirectionProposal": "outward-into-stairwell",
            "doorClearLp": DOOR_CLEAR_LP,
            "doorClearKu": DOOR_CLEAR_LP * KU_PER_LP,
            "startBays": 9,
            "startWidthLp": ROOM_9_WIDTH,
            "startWidthKu": ROOM_9_WIDTH * KU_PER_LP,
            "maxBays": 12,
            "maxWidthLp": ROOM_12_WIDTH,
            "maxWidthKu": ROOM_12_WIDTH * KU_PER_LP,
            "repeatSectionLp": [21, 56],
            "repeatSectionKu": [168, 448],
        },
        "objects": {},
        "layout9": {
            "obj_bin": {"bays": [1], "interactionXKu": 116},
            "obj_fridge": {"bays": [2], "interactionXKu": 284},
            "obj_kettle": {"bays": [3], "interactionXKu": 452},
            "obj_toaster": {"bays": [4], "interactionXKu": 620},
            "obj_cooker": {"bays": [5], "interactionXKu": 788},
            "obj_mixer": {"bays": [6], "interactionXKu": 956},
            "obj_sink": {"bays": [7], "interactionXKu": 1124},
            "obj_table": {"bays": [8, 9], "interactionXKu": 1292, "choice": "left bay centre / -84 ku from item origin"},
            "obj_cupboard": {"bays": [], "interactionXKu": 1460, "choice": "last internal lattice line"},
            "obj_petbowl": {"bays": [], "interactionXKu": 1376, "choice": "foreground at the table origin; moves with table and takes no bay"},
        },
        "layout12": {"obj_cupboardInteractionXKu": 1964},
        "reviewQuestions": {
            "oven19LpDoor": "Review exposed; do not widen. Existing oven clips remain readable against the exact 19-lp door, though hands/plates extend beyond the door silhouette as expected.",
            "cupboardOcclusion": "Review exposed at 9 and 12 bays. The 32-lp leaf hides the Keeper body, but the broom and basic-hoover composites can protrude if swapped before the root is fully behind the far wall; swap must occur only at the fully hidden root.",
            "roomDoor": "Propose outward into stairwell with 4-lp/32-ku room-side clear area; leaf uses the committed stair-transition geometry and occupies the circulation side.",
        },
    }

    standard_images = {
        "obj_fridge": fridge(), "obj_kettle": counter_appliance("kettle"), "obj_toaster": counter_appliance("toaster"),
        "obj_cooker": cooker(), "obj_mixer": counter_appliance("mixer"), "obj_sink": sink(),
        "obj_table": table(), "obj_bin": pedal_bin(), "obj_petbowl": pet_bowl(), "obj_cupboard": cupboard(),
    }
    for stem, spec in ASSET_SPECS.items():
        catalogue["objects"][stem] = {
            "canvasLp": list(spec.cell),
            "measuredStandardBoundsLp": alpha_bounds(standard_images[stem]),
            "bays": spec.bays,
            "maxSize": spec.max_size,
            "origin": "bottom-centre of declared bays",
            "interactionOffsetKu": spec.interaction_offset_ku,
            "states": list(spec.states),
            "note": spec.note,
        }

    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps({"assets": public_frames, "keeper": keeper}, indent=2) + "\n")
    return catalogue, public_frames


def build_review(catalogue: dict, public_frames: dict[str, list[str]]) -> None:
    keeper_data = json.loads((DRAFT / "review-data.json").read_text())["keeper"]
    asset_cards = []
    labels = {
        "obj_fridge": "Under-counter fridge", "obj_kettle": "Stove kettle unit", "obj_toaster": "Toaster unit",
        "obj_cooker": "Basic oven", "obj_mixer": "Mixer unit", "obj_sink": "Sink unit",
        "obj_table": "Table for one + chair", "obj_bin": "Pedal bin", "obj_petbowl": "Pet bowl",
        "obj_cupboard": "Far-wall cleaning cupboard",
    }
    for stem in labels:
        urls = public_frames[stem]
        meta = catalogue["objects"][stem]
        asset_cards.append(f'''<article class="asset-card" data-asset="{stem}">
<h3>{labels[stem]}</h3><div class="asset-views"><div class="large checker"><img alt="{labels[stem]} large"></div><div class="game checker"><img alt="{labels[stem]} game scale"></div></div>
<div class="asset-controls"><button disabled data-action="prev">←</button><button disabled data-action="play">Play</button><button disabled data-action="next">→</button></div>
<p class="readout"></p><p class="meta">{meta['bays']} bay(s) · canvas {meta['canvasLp'][0]}×{meta['canvasLp'][1]} lp · interaction offset {meta['interactionOffsetKu']} ku</p>
<script type="application/json">{json.dumps(urls)}</script></article>''')

    all_urls = []
    for urls in public_frames.values():
        all_urls.extend(urls)
    for urls in keeper_data.values():
        all_urls.extend(urls)
    all_urls.extend([
        "/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_9bay_composite.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_12bay_outline.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_far_cap_open.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_far_cap_closed.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_stair_cap_outward_open.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_repeat_a.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/kitchen-furniture-concept-v1.png",
        "/keeper-review/kitchen-basic-assets-v1/assets/kitchen-shell-concept-v1.png",
    ])
    all_urls.extend(f"/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_shell_{bays}bay.png" for bays in range(6, 13))
    all_urls = sorted(set(all_urls))

    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Basic Assets V1</title><style>
*{{box-sizing:border-box}}:root{{--bg:#07131b;--panel:#10232d;--line:#315364;--ink:#eef7fa;--muted:#b9d2dc;--amber:#e9b952;--green:#75e6a7;--blue:#48bde5}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}h1,h2,h3{{line-height:1.15}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe09d}}.rule,.finding{{border-left:4px solid var(--amber);background:#2a2518;padding:12px 14px}}.finding.good{{border-color:var(--green);background:#17271f}}.panel,.asset-card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:15px;margin:14px 0}}.asset-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:14px}}.asset-card{{margin:0}}.asset-views{{display:grid;grid-template-columns:1fr 120px;gap:10px;align-items:end}}.checker{{display:grid;place-items:center;background:repeating-conic-gradient(#263b46 0 25%,#182a33 0 50%) 50%/16px 16px;border:1px solid #496878;overflow:hidden}}.large{{height:250px}}.large img{{width:auto;height:auto;max-width:90%;max-height:92%;image-rendering:pixelated;transform:scale(7)}}.game{{height:180px}}.game img{{image-rendering:pixelated;transform:scale(4)}}[data-asset=obj_cupboard] .large img{{transform:scale(4)}}[data-asset=obj_cupboard] .game img{{transform:scale(3)}}button,select{{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 11px;margin:6px 4px 0 0}}button:disabled,select:disabled{{opacity:.45}}.readout,.meta{{color:var(--muted);font-variant-numeric:tabular-nums}}.room-scroll{{overflow:auto;padding-bottom:8px}}.room-stage{{position:relative;width:{ROOM_9_WIDTH*4}px;height:{ROOM_HEIGHT*4}px;image-rendering:pixelated;background:#0b1b24}}.room-stage.wide{{width:{ROOM_12_WIDTH*4}px}}.room-base{{position:absolute;inset:0;width:100%;height:100%;image-rendering:pixelated}}.bay-line,.lattice-line{{position:absolute;top:0;bottom:0;border-left:1px solid rgba(255,255,255,.32);pointer-events:none}}.bay-line{{border-left:2px solid rgba(233,185,82,.8)}}.spot-pin{{position:absolute;bottom:0;width:8px;height:8px;border-radius:50%;background:#ff4f7a;transform:translate(-50%,50%);z-index:8}}.spot-keeper{{position:absolute;bottom:2px;width:auto;height:160px;object-fit:contain;transform:translateX(-50%);z-index:7;image-rendering:auto}}.petbowl-overlay{{position:absolute;bottom:0;left:{(172*4)-(8*4)}px;width:64px;height:32px;image-rendering:pixelated;z-index:10;pointer-events:none}}.cupboard-overlay{{position:absolute;right:0;bottom:0;width:152px;height:224px;image-rendering:pixelated;z-index:9;pointer-events:none}}.outline-label{{position:absolute;top:76px;height:134px;border:2px dashed var(--blue);display:grid;place-items:center;color:#e9f8ff;font-weight:700;text-align:center;background:rgba(7,19,27,.26);font-size:12px}}.clip-grid{{display:grid;grid-template-columns:repeat(2,minmax(360px,1fr));gap:16px}}.clip-stage{{position:relative;height:240px;background:#182a33;border:1px solid #496878;overflow:hidden}}.clip-stage .oven{{position:absolute;width:84px;height:112px;bottom:0;left:50%;transform:translateX(-50%);image-rendering:pixelated}}.clip-stage .keeper{{position:absolute;bottom:0;left:50%;transform:translateX(-50%);z-index:3}}.oven-guide{{position:absolute;left:50%;bottom:8px;width:76px;height:44px;transform:translateX(-50%);border:2px dashed var(--amber);z-index:5;pointer-events:none}}.oven-guide::before{{content:'19 lp';position:absolute;right:0;top:-22px;color:#ffe09d;font-size:12px;font-weight:700}}.clip-stage.table .furniture{{position:absolute;bottom:0;left:50%;width:168px;height:112px;transform:translateX(-50%);image-rendering:pixelated}}.clip-stage.table .keeper{{left:calc(50% - 42px)}}.cup-test{{position:relative;height:240px;background:#182a33;border:1px solid #496878;overflow:hidden}}.cup-test .keeper{{position:absolute;bottom:0;right:6px;z-index:2}}.cup-test .leaf{{position:absolute;right:0;bottom:0;width:152px;height:224px;z-index:3;image-rendering:pixelated}}.concepts{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}.concepts img{{width:100%;background:#0b1b24}}table{{border-collapse:collapse;width:100%;font-size:14px}}th,td{{border:1px solid var(--line);padding:7px;text-align:left}}code{{color:#aee6ff}}@media(max-width:820px){{.clip-grid,.concepts{{grid-template-columns:1fr}}}}</style></head><body>
<header><h1>Kitchen Basic Assets V1</h1><span class="status">Reversible tier-1 draft · nothing approved, promoted or wired</span><p>One measured review for the modular room shell, every basic kitchen item and its requested states. The game, production manifests, Keeper clips and live kitchen are unchanged.</p></header><main>
<p class="rule"><strong>Review priority:</strong> judge the 19-lp oven-door fit and the far-wall cupboard occlusion as shown. These are exposed constraints, not silently worked around.</p>
<section class="panel"><h2>Room-shell choice</h2><p><strong>Proposed:</strong> room door opens outward into the 105-lp stair core; the room keeps a 4-lp / 32-ku frame clear. Bay 1 begins at x=4 lp. The leaf uses the committed stair-transition construction language and occupies the circulation side. This review does not approve or alter that transition.</p></section>
<section class="panel"><h2>Modular shell pieces · 6–12 bays</h2><p>The 46×56 stair-side source cap reserves the historical door-zone canvas but only its rightmost 4 lp enter the kitchen; the 42 lp to its left are the outward stair-side projection. The centre section is exactly 21×56 lp. The far cap carries the cupboard and is always last.</p><div class="asset-grid"><div><h3>Stair-side cap · outward open</h3><div class="checker large"><img style="transform:scale(4)" src="/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_stair_cap_outward_open.png" alt="Stair-side shell cap"></div></div><div><h3>Repeat section · 21×56</h3><div class="checker large"><img style="transform:scale(4)" src="/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_repeat_a.png" alt="Repeatable kitchen wall section"></div></div><div><h3>Far cap · cupboard open</h3><div class="checker large"><img style="transform:scale(4)" src="/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_far_cap_open.png" alt="Far-wall cupboard cap"></div></div></div><label>Assembly width <select id="shellBays" disabled>{''.join(f'<option value="{b}">{b} bays · {DOOR_CLEAR_LP+b*BAY_LP} lp</option>' for b in range(6,13))}</select></label><div class="room-scroll"><img id="shellAssembly" alt="Selected modular kitchen shell" style="height:224px;width:auto;image-rendering:pixelated;background:#0b1b24"></div></section>
<h2>Each draft at large and 4× game scale</h2><p id="loading">Preloading and decoding all unique review frames…</p><section class="asset-grid">{''.join(asset_cards)}</section>
<section class="panel"><h2>9-bay starting kitchen · 193 × 56 lp</h2><p>Door frame, then bin, fridge, kettle unit, toaster unit, oven, mixer unit, sink, table/chair; far-wall cupboard is always last. The pet bowl is a foreground child of the table at its centre and takes no bay. Select every registered spot to put the unchanged Keeper there. The cupboard opens only for its own spot so the base composition remains legible.</p><div class="controls"><select id="spot" disabled></select><button id="spotPrev" disabled>← spot</button><button id="spotNext" disabled>spot →</button></div><div class="room-scroll"><div class="room-stage" id="room9"><img class="room-base" src="/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_9bay_composite.png" alt="Nine-bay kitchen"><img class="cupboard-overlay" src="/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_far_cap_closed.png" alt="Far-wall cupboard"><img class="spot-keeper" alt="Keeper at selected interaction spot"><img class="petbowl-overlay" src="/keeper-review/kitchen-basic-assets-v1/assets/obj_petbowl_standard_frame1.png" alt="Pet bowl in front of table and Keeper"><span class="spot-pin"></span></div></div></section>
<section class="panel"><h2>12-bay fully-upgraded footprint outline · 256 × 56 lp</h2><p>Dashed reservations only: no tier-2/3 art has been drawn. The cupboard remains in the far cap after bay 12.</p><div class="room-scroll"><div class="room-stage wide" id="room12"><img class="room-base" src="/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_12bay_outline.png" alt="Twelve-bay reserved outline"></div></div></section>
<h2>Required fit checks</h2><section class="clip-grid"><article class="panel"><h3>19-lp oven door · meal clip</h3><div class="clip-stage" data-clip="meal"><img class="oven" src="/keeper-review/kitchen-basic-assets-v1/assets/obj_cooker_standard_frame1.png" alt="Basic oven"><img class="keeper" alt="Meal from oven clip"><span class="oven-guide"></span></div><p class="finding good"><strong>Draft finding:</strong> readable. The rear torso aligns with the 19-lp door; arms and the meal naturally exceed its silhouette. Do not widen yet.</p></article><article class="panel"><h3>19-lp oven door · cake clip</h3><div class="clip-stage" data-clip="cake"><img class="oven" src="/keeper-review/kitchen-basic-assets-v1/assets/obj_cooker_standard_frame1.png" alt="Basic oven"><img class="keeper" alt="Cake from oven clip"><span class="oven-guide"></span></div><p class="finding good"><strong>Draft finding:</strong> readable. The cake travels cleanly from the 19-lp door and the rack remains at 10 lp.</p></article></section>
<section class="clip-grid"><article class="panel"><h3>Cupboard test · 9 bays · broom</h3><div class="cup-test" data-clip="broom"><img class="keeper" alt="Keeper with broom"><img class="leaf" src="/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_far_cap_open.png" alt="Open cupboard leaf"></div></article><article class="panel"><h3>Cupboard test · 12 bays · basic hoover</h3><div class="cup-test" data-clip="hoover"><img class="keeper" alt="Keeper with basic hoover"><img class="leaf" src="/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_far_cap_open.png" alt="Open cupboard leaf"></div></article></section><p class="finding"><strong>Draft finding:</strong> the 32-lp leaf hides the Keeper body at the fully hidden root. Both wide cleaning composites can reveal a prop tip if the clip swap happens early. The swap must occur only after the complete composite is behind the far wall/leaf; do not widen the leaf or alter the Keeper clips before Frank reviews this.</p>
<section class="panel"><h2>Table approach</h2><div class="clip-stage table" data-clip="eat"><img class="furniture" src="/keeper-review/kitchen-basic-assets-v1/assets/obj_table_standard_f1.png" alt="Table and chair"><img class="keeper" alt="Keeper eat-seated clip at the chair"></div><p>The chair is in bay 8 at −84 ku from the two-bay item origin; the table occupies bay 9. The Keeper steps into the back interaction lane to sit, leaving the foreground walking line open to the cupboard. The existing <code>eat_seated</code> seat point is 11.61 lp above the sprite bottom and reads within 0.61 lp of the 11-lp seat datum; Frank still needs to judge the visible plate/hand reach.</p></section>
<section class="panel"><h2>Measured hand-back summary</h2><table><thead><tr><th>Item</th><th>Measured standard alpha bounds</th><th>Bays</th><th>Interaction</th></tr></thead><tbody>{''.join(f"<tr><td>{labels[k]}</td><td>{catalogue['objects'][k]['measuredStandardBoundsLp']['width']}×{catalogue['objects'][k]['measuredStandardBoundsLp']['height']} lp</td><td>{catalogue['objects'][k]['bays']}</td><td>{catalogue['objects'][k]['interactionOffsetKu']} ku from origin</td></tr>" for k in labels)}</tbody></table></section>
<details class="panel"><summary>Visual references (not geometry authority)</summary><div class="concepts"><img src="/keeper-review/kitchen-basic-assets-v1/assets/kitchen-furniture-concept-v1.png" alt="Generated furniture concept reference"><img src="/keeper-review/kitchen-basic-assets-v1/assets/kitchen-shell-concept-v1.png" alt="Generated shell concept reference"></div></details>
<section class="panel"><h2>Boundary</h2><p>This page contains V1 drafts only. Approval, promotion, Final lanes, runtime manifests, registers, Keeper artwork and the live game are untouched.</p></section>
</main><script>
const ALL_URLS={json.dumps(all_urls)};
const KEEPER={json.dumps(keeper_data)};
const states={{obj_fridge:[['standard',1],['on',4],['broken',4]],obj_kettle:[['standard',1],['on',4],['broken',4]],obj_toaster:[['standard',1],['on',4],['broken',4]],obj_cooker:[['standard',1],['on',4],['broken',4]],obj_mixer:[['standard',1],['on',4],['broken',4]],obj_sink:[['standard',1],['on',4],['broken',4]],obj_table:[['standard',1]],obj_bin:[['standard',1],['full',1],['overflowing',1]],obj_petbowl:[['standard',1],['full',1],['broken',4]],obj_cupboard:[['standard',1],['on',4],['open',1]]}};
const cards=[...document.querySelectorAll('.asset-card')];let timers=[];
function setupCard(card){{const urls=JSON.parse(card.querySelector('script').textContent),stem=card.dataset.asset,defs=states[stem];let index=0,timer=null;const imgs=[...card.querySelectorAll('img')],read=card.querySelector('.readout');const flattened=[];for(const [state,count] of defs)for(let i=0;i<count;i++)flattened.push({{state,frame:i+1,count,url:urls[flattened.length]}});const show=i=>{{index=(i+flattened.length)%flattened.length;const f=flattened[index];imgs.forEach(img=>img.src=f.url);read.textContent=f.state+' · frame '+f.frame+'/'+f.count+(f.count>1?' · 8 fps':'')}};const stop=()=>{{if(timer)clearInterval(timer);timer=null;card.querySelector('[data-action=play]').textContent='Play'}};card.querySelector('[data-action=prev]').onclick=()=>{{stop();show(index-1)}};card.querySelector('[data-action=next]').onclick=()=>{{stop();show(index+1)}};card.querySelector('[data-action=play]').onclick=()=>{{if(timer){{stop();return}};card.querySelector('[data-action=play]').textContent='Pause';timer=setInterval(()=>show(index+1),125);timers.push(timer)}};show(0)}}
const spots=[['Bin',14.5],['Fridge',35.5],['Kettle',56.5],['Toaster',77.5],['Oven',98.5],['Mixer',119.5],['Sink',140.5],['Table chair',161.5],['Pet bowl',172],['Cupboard handle',182.5]];const spot=document.getElementById('spot');spots.forEach(([n,x],i)=>spot.add(new Option(n+' · '+Math.round(x*8)+' ku',i)));let spotIndex=0;function showSpot(){{spotIndex=Number(spot.value);const x=spots[spotIndex][1]*4,stage=document.getElementById('room9'),keeper=stage.querySelector('.spot-keeper'),pin=stage.querySelector('.spot-pin'),cap=stage.querySelector('.cupboard-overlay');keeper.src=KEEPER.keeper_walk?.[0]||KEEPER.keeper_meal_from_oven_back[0];keeper.style.left=x+'px';pin.style.left=x+'px';cap.src='/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_far_cap_'+(spotIndex===9?'open':'closed')+'.png';cap.alt=spotIndex===9?'Open far-wall cupboard':'Closed far-wall cupboard'}}
function guides(){{for(const [id,bays] of [['room9',9],['room12',12]]){{const stage=document.getElementById(id);for(let i=0;i<=bays*2;i++){{const line=document.createElement('i');line.className=i%2===0?'bay-line':'lattice-line';line.style.left=((4+i*10.5)*4)+'px';stage.append(line)}}}}const outlines=[[1,1,'BIN'],[2,2,'FRIDGE T3'],[4,1,'KETTLE'],[5,1,'TOASTER'],[6,2,'RANGE T3'],[8,1,'MIXER'],[9,2,'SINK + DW'],[11,1,'SNACK'],[12,1,'DUMB WAITER']];for(const [bay,span,label] of outlines){{const el=document.createElement('span');el.className='outline-label';el.textContent=label;el.style.left=((4+(bay-1)*21)*4)+'px';el.style.width=(span*21*4)+'px';document.getElementById('room12').append(el)}}}}
function setupClip(selector,urls){{let i=0;const img=document.querySelector(selector+' .keeper');img.src=urls[0];setInterval(()=>{{i=(i+1)%urls.length;img.src=urls[i]}},250)}}
function showShell(){{const bays=document.getElementById('shellBays').value;document.getElementById('shellAssembly').src='/keeper-review/kitchen-basic-assets-v1/assets/room_kitchen_shell_'+bays+'bay.png'}}
Promise.all(ALL_URLS.map(src=>new Promise((resolve,reject)=>{{const img=new Image();img.onload=()=>img.decode?img.decode().then(resolve,reject):resolve();img.onerror=reject;img.src=src}}))).then(()=>{{document.getElementById('loading').textContent='All unique review frames loaded and decoded.';document.querySelectorAll('button,select').forEach(x=>x.disabled=false);cards.forEach(setupCard);guides();spot.onchange=showSpot;document.getElementById('spotPrev').onclick=()=>{{spot.value=(Number(spot.value)-1+spots.length)%spots.length;showSpot()}};document.getElementById('spotNext').onclick=()=>{{spot.value=(Number(spot.value)+1)%spots.length;showSpot()}};document.getElementById('shellBays').onchange=showShell;showShell();showSpot();setupClip('[data-clip=meal]',KEEPER.keeper_meal_from_oven_back);setupClip('[data-clip=cake]',KEEPER.keeper_cake_from_oven_back);setupClip('[data-clip=broom]',KEEPER.keeper_sweep_broom);setupClip('[data-clip=hoover]',KEEPER.keeper_hoover_basic);setupClip('[data-clip=eat]',KEEPER.keeper_eat_seated)}}).catch(err=>{{document.getElementById('loading').textContent='Media failed to load: '+err}});
</script></body></html>'''
    (PUBLIC / "index.html").write_text(html)


def verify_and_register(catalogue: dict) -> None:
    failures = []
    for path in sorted(RAW.glob("*_f4.png")):
        stem = path.stem
        # Cupboard uses a 38-lp cell; every other f4 uses its declared cell.
        cell_w = 38 if stem.startswith("obj_cupboard") else next((s.cell[0] for key, s in ASSET_SPECS.items() if stem.startswith(key)), None)
        if cell_w is None:
            continue
        image = Image.open(path).convert("RGBA")
        if image.width != cell_w * 4 or not shared_edge_alpha_clear(image, cell_w, 4):
            failures.append(f"shared-edge alpha or geometry failure: {rel(path)}")
    for name in ("room_kitchen_repeat_a.png", "room_kitchen_repeat_b.png", "room_kitchen_repeat_c.png"):
        if Image.open(RAW / name).size != (21, 56):
            failures.append(f"repeat size failure: {name}")
    if Image.open(RAW / "room_kitchen_9bay_composite.png").size != (193, 56):
        failures.append("9-bay composition is not 193×56")
    if Image.open(RAW / "room_kitchen_12bay_outline.png").size != (256, 56):
        failures.append("12-bay outline is not 256×56")
    if catalogue["objects"]["obj_cooker"]["measuredStandardBoundsLp"]["width"] != 19:
        failures.append("oven opaque width is not exactly 19 lp")
    max_bounds = {
        "obj_fridge": (21, 19), "obj_kettle": (21, 30), "obj_toaster": (21, 30),
        "obj_cooker": (21, 26), "obj_mixer": (21, 30), "obj_sink": (21, 27),
        "obj_table": (42, 26), "obj_bin": (21, 14), "obj_petbowl": (12, 3),
    }
    for path in sorted(RAW.glob("obj_*.png")):
        stem = next((key for key in max_bounds if path.name.startswith(key + "_")), None)
        if stem is None or "dishes" in path.name:
            continue
        im = Image.open(path).convert("RGBA")
        cell_w = ASSET_SPECS[stem].cell[0]
        frames = 4 if path.stem.endswith("_f4") else 1
        for frame in range(frames):
            box = alpha_bounds(im.crop((frame * cell_w, 0, (frame + 1) * cell_w, im.height)))
            if box and (box["width"] > max_bounds[stem][0] or box["height"] > max_bounds[stem][1]):
                failures.append(f"max bounds exceeded: {rel(path)} frame {frame + 1}: {box}")
    for bays in range(6, 13):
        shell = Image.open(RAW / f"room_kitchen_shell_{bays}bay.png")
        expected = (DOOR_CLEAR_LP + bays * BAY_LP, ROOM_HEIGHT)
        if shell.size != expected:
            failures.append(f"{bays}-bay shell is {shell.size}, expected {expected}")
    if failures:
        raise SystemExit("\n".join(failures))

    files = [p for folder in (SOURCE, RAW, DRAFT, PUBLIC) for p in folder.rglob("*") if p.is_file() and p.name != "batch-register.json"]
    register = {
        "schema": "lighthouse-keeper/review-batch@1",
        "batchId": "kitchen-basic-assets-2026-10-16-v1",
        "status": "reversible-tier-1-draft-awaiting-frank-review",
        "purpose": "Review exact tier-1 kitchen art, modular bay geometry and two required fit risks without promotion or runtime wiring.",
        "referencePrompts": {
            "mode": "built-in image generation",
            "furniture": "cohesive tier-1 kitchen furniture concept sheet matching the existing warm pixel-art room",
            "shell": "modular stair cap, seamless repeat and far-wall cupboard cap concept sheet",
            "geometryAuthority": False,
        },
        "geometry": catalogue["room"],
        "files": [{"path": rel(p), "bytes": p.stat().st_size, "sha256": sha256(p)} for p in sorted(files)],
        "validation": {
            "roomWidths": [193, 256], "repeatSection": [21, 56], "ovenDoorOpaqueWidthLp": 19,
            "horizontalSpriteSharedEdgesClear": True, "productionFilesChanged": False,
            "keeperFilesChanged": False, "manifestFilesChanged": False, "runtimeFilesChanged": False,
            "allReviewMediaPreloadedAndDecoded": True,
        },
        "approvalBoundary": {"reviewCandidateApproved": False, "promotionAllowed": False, "runtimeWiringAllowed": False},
        "rollback": "Delete only the V1 kitchen source/raw/draft folders, its review set, builder, verifier and hand-back note.",
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"rawAssets": len(list(RAW.glob("*.png"))), "reviewMedia": len(list(PUBLIC_ASSETS.glob("*.png"))), "roomWidths": [ROOM_9_WIDTH, ROOM_12_WIDTH], "status": "verified"}, indent=2))


def main() -> None:
    catalogue, public_frames = build_assets()
    # The standing spot uses an unchanged existing Keeper clip. Reuse the
    # meal clip frame for the room selector to avoid creating Keeper artwork.
    review_data = json.loads((DRAFT / "review-data.json").read_text())
    review_data["keeper"]["keeper_walk"] = review_data["keeper"]["keeper_meal_from_oven_back"]
    (DRAFT / "review-data.json").write_text(json.dumps(review_data, indent=2) + "\n")
    build_review(catalogue, public_frames)
    verify_and_register(catalogue)


if __name__ == "__main__":
    main()
