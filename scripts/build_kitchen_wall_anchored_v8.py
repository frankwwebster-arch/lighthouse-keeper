#!/usr/bin/env python3
"""Build the reversible Kitchen V8 wall-anchored correction draft.

Kitchen V6 Option B and Kitchen Room V7 remain immutable.  This builder reads
them as baselines, writes a fresh review set, and never touches runtime art.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from build_kitchen_basic_assets_v6_option_b import render_effect


ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = ROOT / "data/kitchen_wall_anchored_v8_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
V6_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v6-option-b"
V6_DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v6-option-b"
V7_RAW = ROOT / "art/raw/kitchen-room-flat-cutaway-2026-10-16-v7"
V7_DRAFT = ROOT / "art/drafts/kitchen-room-flat-cutaway-2026-10-16-v7"
SOURCE = ROOT / "art/source/kitchen-wall-anchored-2026-10-16-v8"
RAW = ROOT / "art/raw/kitchen-wall-anchored-2026-10-16-v8"
DRAFT = ROOT / "art/drafts/kitchen-wall-anchored-2026-10-16-v8"
PUBLIC = ROOT / "public/keeper-review/kitchen-wall-anchored-v8"
ASSETS = PUBLIC / "assets"

DENSITY = 4
BAY = 21
DOOR_DATUM = 4
ROOM_H = 56
FOOT_LINE = 52
TRANSPARENT = (0, 0, 0, 0)
INK = (7, 27, 50, 255)
WOOD_DARK = (93, 48, 29, 255)
WOOD = (154, 86, 48, 255)
WOOD_LIGHT = (211, 138, 70, 255)
WOOD_HIGHLIGHT = (238, 174, 88, 255)
BRASS_DARK = (135, 80, 12, 255)
BRASS = (215, 150, 34, 255)
BRASS_LIGHT = (255, 205, 67, 255)
WHITE = (250, 250, 239, 255)
WHITE_HIGHLIGHT = (255, 255, 250, 255)
WHITE_SHADOW = (213, 221, 222, 255)
TEAL_DARK = (10, 106, 134, 255)
TEAL = (20, 184, 204, 255)
TEAL_LIGHT = (104, 232, 236, 255)

ORDER = ["obj_bin", "obj_fridge", "obj_kettle", "obj_toaster", "obj_cooker", "obj_mixer", "obj_sink", "obj_table", "obj_petbowl", "obj_cupboard"]
CHANGED = ["obj_bin", "obj_fridge", "obj_kettle", "obj_toaster", "obj_mixer", "obj_sink"]
ANIMATED = ["obj_fridge", "obj_kettle", "obj_toaster", "obj_cooker", "obj_mixer", "obj_sink"]
COUNTER_SPEC = {
    "obj_kettle": {"front": 48, "central": (14, 68)},
    "obj_toaster": {"front": 36, "central": (12, 72)},
    "obj_mixer": {"front": 52, "central": (12, 72)},
    "obj_sink": {"front": 48, "central": (14, 70)},
}


def rgba(size: tuple[int, int], fill=TRANSPARENT) -> Image.Image:
    return Image.new("RGBA", size, fill)


def px(lp: float) -> int:
    return round(lp * DENSITY)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        digest.update(path.relative_to(directory).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


V6_CATALOGUE = read_json(V6_DRAFT / "asset-catalogue.json")
V6_REVIEW = read_json(V6_DRAFT / "review-data.json")


def alpha_bound(image: Image.Image) -> dict | None:
    box = image.getchannel("A").getbbox()
    if not box:
        return None
    x0, y0, x1, y1 = box
    return {
        "xLp": x0 / DENSITY,
        "yLp": y0 / DENSITY,
        "widthLp": (x1 - x0) / DENSITY,
        "heightLp": (y1 - y0) / DENSITY,
    }


def load_strip(path: Path, meta: dict) -> list[Image.Image]:
    strip = Image.open(path).convert("RGBA")
    width, height = meta["w"] * DENSITY, meta["h"] * DENSITY
    return [strip.crop((index * width, 0, (index + 1) * width, height)) for index in range(meta["frames"])]


def load_v6_state(stem: str, state: str) -> list[Image.Image]:
    record = V6_CATALOGUE["assets"][stem]["states"][state]
    return load_strip(ROOT / record["png"], record["meta"])


def make_strip(frames: list[Image.Image]) -> Image.Image:
    out = rgba((frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        out.alpha_composite(frame, (index * frame.width, 0))
    return out


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=False, compress_level=9)


def save_strip(name: str, frames: list[Image.Image], logical: tuple[int, int], fps: int, extra: dict | None = None) -> dict:
    strip = make_strip(frames)
    png_path = RAW / f"{name}.png"
    save_png(strip, png_path)
    metadata = {
        "w": logical[0], "h": logical[1], "frames": len(frames), "fps": fps,
        "density": DENSITY, "anchor": [logical[0] / 2, logical[1]], "z": 40,
        "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False},
    }
    if extra:
        metadata.update(extra)
    png_path.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n")
    urls = []
    for index, frame in enumerate(frames):
        review_name = f"{name}_frame{index + 1}.png"
        save_png(frame, ASSETS / review_name)
        urls.append(f"/keeper-review/kitchen-wall-anchored-v8/assets/{review_name}")
    return {
        "png": png_path.relative_to(ROOT).as_posix(),
        "json": png_path.with_suffix(".json").relative_to(ROOT).as_posix(),
        "sha256": sha(png_path),
        "meta": metadata,
        "urls": urls,
        "bounds": [alpha_bound(frame) for frame in frames],
    }


def save_asset(name: str, image: Image.Image, logical: tuple[int, int], extra: dict | None = None) -> dict:
    return save_strip(name, [image], logical, 0, extra)


def white_fridge() -> Image.Image:
    """A simple bright freestanding fridge with no furniture countertop."""
    out = rgba((px(21), px(21)))
    draw = ImageDraw.Draw(out)
    # Casing and flat enamel appliance top.
    draw.rounded_rectangle((4, 4, 79, 80), radius=6, fill=WHITE_SHADOW, outline=INK, width=3)
    draw.rectangle((7, 9, 76, 75), fill=WHITE)
    draw.rectangle((10, 6, 73, 10), fill=WHITE_HIGHLIGHT)
    draw.line((7, 13, 76, 13), fill=INK, width=3)
    draw.line((10, 16, 73, 16), fill=WHITE_HIGHLIGHT, width=2)
    # One unmistakeable fridge door.
    draw.rounded_rectangle((8, 16, 74, 73), radius=3, fill=WHITE, outline=WHITE_SHADOW, width=2)
    draw.line((9, 18, 9, 70), fill=WHITE_HIGHLIGHT, width=2)
    # Brass pull and right-side hinges.
    draw.rounded_rectangle((17, 23, 52, 29), radius=3, fill=INK)
    draw.rounded_rectangle((20, 24, 49, 27), radius=2, fill=BRASS)
    draw.ellipse((18, 23, 23, 28), fill=BRASS_LIGHT)
    draw.ellipse((47, 23, 52, 28), fill=BRASS_DARK)
    for y in (22, 55):
        draw.rounded_rectangle((71, y, 76, y + 12), radius=2, fill=INK)
        draw.rectangle((72, y + 2, 74, y + 10), fill=BRASS)
    # Lower grille and feet are child-recognition cues.
    draw.rounded_rectangle((17, 66, 66, 75), radius=3, fill=INK)
    for y in (69, 72):
        draw.line((22, y, 61, y), fill=(68, 83, 94, 255), width=1)
    draw.rounded_rectangle((7, 76, 20, 83), radius=3, fill=INK)
    draw.rounded_rectangle((64, 76, 77, 83), radius=3, fill=INK)
    draw.rectangle((10, 78, 18, 81), fill=(64, 77, 87, 255))
    draw.rectangle((66, 78, 74, 81), fill=(64, 77, 87, 255))
    return out


def brighten_fridge_neutrals(image: Image.Image) -> Image.Image:
    out = image.copy()
    pixels = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = pixels[x, y]
            if a and r > 205 and g > 175 and b > 155 and max(r, g, b) - min(r, g, b) < 65:
                luminance = (r + g + b) // 3
                pixels[x, y] = WHITE_HIGHLIGHT if luminance > 235 else WHITE
    return out


def shrink_to_bounds(image: Image.Image, width_lp: int, height_lp: int) -> Image.Image:
    box = image.getchannel("A").getbbox()
    if not box:
        raise ValueError("cannot shrink an empty image")
    cropped = image.crop(box).resize((px(width_lp), px(height_lp)), Image.Resampling.LANCZOS)
    cropped.putalpha(cropped.getchannel("A").point(lambda value: 255 if value >= 112 else 0))
    out = rgba(image.size)
    out.alpha_composite(cropped, ((out.width - cropped.width) // 2, out.height - cropped.height))
    return out


def clean_counter_slab(size: tuple[int, int], front_y: int) -> Image.Image:
    """Draw the selected B slab as one unbroken true rectangle."""
    out = rgba(size)
    draw = ImageDraw.Draw(out)
    x0, x1 = 2, 81
    rear_y, fascia_bottom = front_y - 6, front_y + 7
    draw.rectangle((x0, rear_y, x1, front_y - 1), fill=WOOD)
    draw.line((x0, rear_y, x1, rear_y), fill=INK, width=2)
    draw.line((x0 + 2, rear_y + 2, x1 - 2, rear_y + 2), fill=WOOD_HIGHLIGHT, width=1)
    draw.line((x0, front_y - 2, x1, front_y - 2), fill=WOOD_DARK, width=1)
    draw.line((x0, front_y - 1, x1, front_y - 1), fill=INK, width=1)
    draw.rectangle((x0, front_y, x1, fascia_bottom), fill=WOOD_DARK)
    draw.rectangle((x0 + 2, front_y + 1, x1 - 2, front_y + 3), fill=WOOD)
    draw.line((x0, fascia_bottom, x1, fascia_bottom), fill=INK, width=1)
    draw.line((x0, rear_y, x0, fascia_bottom), fill=INK, width=2)
    draw.line((x1 - 1, rear_y, x1 - 1, fascia_bottom), fill=INK, width=2)
    return out


def smooth_counter_wings(image: Image.Image, stem: str) -> Image.Image:
    spec = COUNTER_SPEC[stem]
    front_y = spec["front"]
    centre_left, centre_right = spec["central"]
    slab = clean_counter_slab(image.size, front_y)
    out = image.copy()
    y0, y1 = front_y - 6, front_y + 8
    for x0, x1 in ((2, centre_left - 1), (centre_right + 1, 81)):
        box = (x0, y0, x1 + 1, y1)
        out.paste(slab.crop(box), box)
    return out


def corrected_frames(stem: str, state: str) -> list[Image.Image]:
    old = load_v6_state(stem, state)
    if stem == "obj_fridge":
        base = white_fridge()
        if state in {"on", "broken"}:
            return [brighten_fridge_neutrals(render_effect(base, stem, state, index)) for index in range(4)]
        return [base]
    if stem == "obj_bin":
        return [shrink_to_bounds(frame, 10, 12) for frame in old]
    if stem in COUNTER_SPEC:
        return [smooth_counter_wings(frame, stem) for frame in old]
    return [frame.copy() for frame in old]


def porthole_frame() -> Image.Image:
    spec = RECIPE["sinkPorthole"]
    out = rgba((px(21), px(56)))
    draw = ImageDraw.Draw(out)
    cx, cy = px(spec["centreLpFromCellTop"][0]), px(spec["centreLpFromCellTop"][1])
    outer = px(spec["outerDiameterLp"])
    aperture = px(spec["apertureDiameterLp"])
    ox0, oy0 = cx - outer // 2, cy - outer // 2
    ox1, oy1 = ox0 + outer - 1, oy0 + outer - 1
    gx0, gy0 = cx - aperture // 2, cy - aperture // 2
    gx1, gy1 = gx0 + aperture - 1, gy0 + aperture - 1
    draw.ellipse((ox0, oy0, ox1, oy1), fill=INK)
    draw.ellipse((ox0 + 2, oy0 + 2, ox1 - 2, oy1 - 2), fill=BRASS_DARK)
    draw.ellipse((ox0 + 5, oy0 + 5, ox1 - 5, oy1 - 5), fill=BRASS)
    draw.arc((ox0 + 7, oy0 + 7, ox1 - 7, oy1 - 7), 205, 335, fill=BRASS_LIGHT, width=2)
    # The aperture itself is deliberately alpha zero. Only a faint glazing
    # highlight remains, so a separately rendered condition is visible below.
    draw.ellipse((gx0, gy0, gx1, gy1), fill=TRANSPARENT, outline=INK, width=2)
    draw.arc((gx0 + 3, gy0 + 3, gx1 - 3, gy1 - 3), 205, 300, fill=(255, 255, 250, 82), width=2)
    radius = px(8)
    for index in range(8):
        angle = math.radians(index * 45 - 90)
        bx, by = round(cx + math.cos(angle) * radius), round(cy + math.sin(angle) * radius)
        draw.ellipse((bx - 2, by - 2, bx + 2, by + 2), fill=INK)
        draw.point((bx, by), fill=BRASS_LIGHT)
    return out


def weather_underlay(condition: str) -> Image.Image:
    spec = RECIPE["sinkPorthole"]
    out = rgba((px(21), px(56)))
    cx, cy = px(spec["centreLpFromCellTop"][0]), px(spec["centreLpFromCellTop"][1])
    diameter = px(spec["apertureDiameterLp"])
    x0, y0 = cx - diameter // 2, cy - diameter // 2
    x1, y1 = x0 + diameter - 1, y0 + diameter - 1
    view = rgba(out.size)
    draw = ImageDraw.Draw(view)
    if condition == "day":
        sky, horizon, sea = (153, 231, 247, 255), (62, 194, 229, 255), (20, 126, 181, 255)
    elif condition == "sunset":
        sky, horizon, sea = (255, 183, 111, 255), (229, 111, 83, 255), (80, 77, 126, 255)
    elif condition == "night":
        sky, horizon, sea = (26, 45, 82, 255), (40, 70, 112, 255), (12, 44, 74, 255)
    else:
        sky, horizon, sea = (119, 144, 153, 255), (82, 119, 138, 255), (34, 84, 112, 255)
    draw.rectangle((x0, y0, x1, cy), fill=sky)
    draw.rectangle((x0, cy, x1, y1), fill=horizon)
    draw.rectangle((x0, cy + px(3), x1, y1), fill=sea)
    if condition == "night":
        draw.ellipse((x0 + 9, y0 + 7, x0 + 17, y0 + 15), fill=(255, 244, 177, 255))
        for sx, sy in ((28, 14), (50, 22), (37, 34)):
            draw.point((x0 + sx, y0 + sy), fill=WHITE_HIGHLIGHT)
    elif condition == "rain":
        for offset in range(5, diameter - 5, 10):
            draw.line((x0 + offset, y0 + 5, x0 + offset - 5, y0 + 17), fill=(194, 231, 239, 230), width=2)
            draw.line((x0 + offset + 3, cy, x0 + offset - 2, cy + 12), fill=(194, 231, 239, 230), width=2)
    else:
        draw.ellipse((x0 + 8, y0 + 9, x0 + 26, y0 + 17), fill=(255, 250, 221, 230))
    draw.polygon([(cx - px(3), cy + px(3)), (cx, cy + px(.5)), (cx + px(3), cy + px(3))], fill=WOOD_DARK)
    draw.rectangle((cx - 1, cy - px(2), cx + 1, cy + px(1)), fill=WHITE_HIGHLIGHT)
    mask = Image.new("L", out.size, 0)
    ImageDraw.Draw(mask).ellipse((x0, y0, x1, y1), fill=255)
    view.putalpha(mask)
    out.alpha_composite(view)
    return out


PORTHOLE_FRAME = porthole_frame()
WEATHER = {condition: weather_underlay(condition) for condition in RECIPE["sinkPorthole"]["weatherAndTimeLayers"]}


def room_shell(bays: int) -> Image.Image:
    return Image.open(V7_RAW / f"room_kitchen_shell_{bays}bay.png").convert("RGBA")


def place_one_bay(out: Image.Image, image: Image.Image, bay: int) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY) + (px(BAY) - image.width) // 2
    out.alpha_composite(image, (x, px(FOOT_LINE) - image.height))


def place_two_bays(out: Image.Image, image: Image.Image, bay: int) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY) + (px(2 * BAY) - image.width) // 2
    out.alpha_composite(image, (x, px(FOOT_LINE) - image.height))


def place_sink_children(out: Image.Image, bay: int, condition: str) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY)
    out.alpha_composite(WEATHER[condition], (x, 0))
    out.alpha_composite(PORTHOLE_FRAME, (x, 0))


def room_composite(standards: dict[str, Image.Image], condition: str = "day") -> Image.Image:
    out = room_shell(9)
    positions = {"obj_bin": 1, "obj_fridge": 2, "obj_kettle": 3, "obj_toaster": 4, "obj_cooker": 5, "obj_mixer": 6}
    for stem, bay in positions.items():
        place_one_bay(out, standards[stem], bay)
    place_sink_children(out, 7, condition)
    place_one_bay(out, standards["obj_sink"], 7)
    place_two_bays(out, standards["obj_table"], 8)
    place_one_bay(out, standards["obj_petbowl"], 9)
    return out


def sink_move_proof(standards: dict[str, Image.Image], bay: int, condition: str = "rain") -> Image.Image:
    out = room_shell(9)
    place_sink_children(out, bay, condition)
    place_one_bay(out, standards["obj_sink"], bay)
    return out


def porthole_layers(condition: str) -> Image.Image:
    out = rgba((px(21), px(56)))
    out.alpha_composite(WEATHER[condition])
    out.alpha_composite(PORTHOLE_FRAME)
    return out


def outline_12() -> Image.Image:
    out = room_shell(12)
    place_sink_children(out, 9, "day")
    draw = ImageDraw.Draw(out)
    for index in range(13):
        x = px(DOOR_DATUM + index * BAY)
        for y in range(px(6), px(51), 8):
            draw.line((x, y, x, min(y + 3, px(51) - 1)), fill=(88, 212, 223, 190), width=1)
    reservations = [(1, 1, 12), (2, 1, 21), (3, 1, 31), (4, 1, 31), (5, 1, 31), (6, 1, 31), (8, 2, 28), (10, 1, 12)]
    for bay, span, height in reservations:
        x0 = px(DOOR_DATUM + (bay - 1) * BAY + .5)
        x1 = px(DOOR_DATUM + (bay - 1 + span) * BAY - .5) - 1
        y0, y1 = px(FOOT_LINE - height), px(FOOT_LINE) - 1
        for x in range(x0, x1 + 1, 8):
            draw.line((x, y0, min(x + 3, x1), y0), fill=(239, 182, 77, 220), width=1)
        draw.line((x0, y0, x0, y1), fill=(239, 182, 77, 220), width=1)
        draw.line((x1, y0, x1, y1), fill=(239, 182, 77, 220), width=1)
    return out


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V8 · wall-anchored corrections</title><style>
:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--muted:#a8bdc4;--gold:#efb64d;--cyan:#58d4df;--red:#ff786d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1520px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:12px;min-width:0}.compare{display:grid;grid-template-columns:1fr 1fr;gap:8px}.well{min-height:190px;display:flex;align-items:end;justify-content:center;overflow:auto;background:repeating-conic-gradient(#172c36 0 25%,#10232d 0 50%) 0/18px 18px;border-radius:8px;padding:8px}.well img{flex:none}.scroll{overflow:auto;background:#071923;border-radius:10px;padding:10px}.scroll img{display:block;height:224px;width:auto}.small{font-size:.84rem;color:var(--muted)}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0}button,select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.anchor{position:relative;display:inline-block}.anchor:after{content:"asset foot line 52 lp · 4-lp clear floor";position:absolute;left:0;right:0;top:208px;border-top:2px solid var(--cyan);color:#06131c;background:var(--cyan);font-size:11px;line-height:18px;padding-left:6px;pointer-events:none}.recipe{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}.metric{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:10px}.metric strong{display:block;color:var(--gold);font-size:1.15rem}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:7px;border-bottom:1px solid var(--line);vertical-align:top}code{color:#9ce5ea;word-break:break-all}@media(max-width:720px){header,main{padding:12px}.compare{grid-template-columns:1fr}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">Wall-anchored</span><span class="tag">Transparent dynamic porthole</span><h1>Kitchen V8 · corrected units and room placement</h1><p>Frank-approved wall-anchored composition, smooth worktops, a plain white freestanding fridge, smaller pedal bin and a larger condition-responsive sink porthole.</p><p id="loading" class="notice">Preloading and decoding every unique review image… controls remain locked.</p></header><main>
<section class="panel"><h2>Locked correction recipe</h2><div class="recipe"><div class="metric"><strong>52 lp</strong>back-wall asset foot line</div><div class="metric"><strong>4 lp</strong>foreground floor remains clear</div><div class="metric"><strong>10 × 12 lp</strong>maximum bin bounds</div><div class="metric"><strong>no wood top</strong>bright-white fridge</div><div class="metric"><strong>19 lp</strong>porthole outer diameter</div><div class="metric"><strong>alpha-clear</strong>separate weather aperture</div></div><p class="notice"><strong>Approval boundary:</strong> V8 remains review-only. Kitchen V6, Room V7, Keeper art, runtime sprites, Final and manifests remain unchanged.</p></section>
<section class="panel"><h2>Corrected assets and every state</h2><p>V6 is shown on the left; V8 is shown on the right. The exposed countertop wings are solid rectangles with no chipped pixels.</p><div id="assetGrid" class="grid"></div></section>
<section class="panel"><h2>Units anchored to the rear wall</h2><div class="compare"><div class="card"><h3>Previous placement · foot line 56</h3><div class="scroll"><img id="beforeRoom"></div></div><div class="card"><h3>V8 placement · foot line 52</h3><div class="scroll"><span class="anchor"><img id="afterRoom"></span></div></div></div><p>The unit transform is tied to the rear wall/floor junction. It is not an arbitrary upward offset: the feet bed 1 lp into the floor band and leave 4 lp of uninterrupted foreground floor.</p></section>
<section class="panel"><h2>Larger sink-owned porthole · transparent weather/time layers</h2><div class="controls"><label>Condition <select id="conditionSelect" disabled><option>day</option><option>sunset</option><option>night</option><option>rain</option></select></label></div><div class="grid"><div class="card"><h3>Frame/glazing only</h3><div class="well"><img id="frameOnly"></div><p class="small">19-lp brass frame; aperture pixels remain transparent.</p></div><div class="card"><h3>Separate condition underlay</h3><div class="well"><img id="conditionOnly"></div><p class="small">Swappable child layer; no weather pixels are baked into the frame.</p></div><div class="card"><h3>Composed behind sink</h3><div class="well"><img id="portholeComposite"></div><p class="small">underlay z24 · frame z26 · sink z40</p></div></div></section>
<section class="panel"><h2>Move the sink · frame and condition move with it</h2><div class="controls"><label>Sink bay <select id="moveSelect" disabled><option value="2">2</option><option value="5">5</option><option value="8">8</option></select></label></div><div class="scroll"><img id="moveProof"></div><p>Frame delta = weather-underlay delta = sink delta. Scale and bytes do not change.</p></section>
<section class="panel"><h2>9-bay condition proofs</h2><div id="weatherRooms" class="grid"></div></section>
<section class="panel"><h2>12-bay wall-anchored reservation</h2><div class="scroll"><img id="room12"></div><p>Every reservation terminates at the 52-lp foot line; the far-wall cupboard remains last.</p></section>
<section class="panel"><h2>Measured hand-back and hashes</h2><table><thead><tr><th>Item</th><th>Cell / bound</th><th>Recipe role</th><th>SHA-256</th></tr></thead><tbody id="rows"></tbody></table></section>
</main><script>
const DATA=__DATA__,all=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))all.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const urls=[...new Set(all)];const img=(src,alt='')=>Object.assign(new Image,{src,alt});
function setupAssets(){const grid=document.getElementById('assetGrid');for(const stem of DATA.changed){const a=DATA.assets[stem],card=document.createElement('article');card.className='card';card.innerHTML=`<h3>${a.label}</h3><div class="controls"><select></select><button>Previous</button><button>Play</button><button>Next</button></div><div class="compare"><div><div class="well old"></div><p class="small">V6</p></div><div><div class="well fresh"></div><p class="small">V8</p></div></div><p class="small">cell ${a.cell.join('×')} lp · V8 max ${a.largestBound.widthLp}×${a.largestBound.heightLp} lp</p>`;const sel=card.querySelector('select'),buttons=card.querySelectorAll('button'),states=Object.keys(a.states);states.forEach(s=>sel.add(new Option(s,s)));let n=0,t=null;const show=()=>{const s=a.states[sel.value],k=((n%s.v8Urls.length)+s.v8Urls.length)%s.v8Urls.length;card.querySelector('.old').replaceChildren(img(s.v6Urls[k%s.v6Urls.length],`${a.label} V6`));card.querySelector('.fresh').replaceChildren(img(s.v8Urls[k],`${a.label} V8`))};sel.onchange=()=>{n=0;show()};buttons[0].onclick=()=>{clearInterval(t);t=null;n--;show()};buttons[2].onclick=()=>{clearInterval(t);t=null;n++;show()};buttons[1].onclick=()=>{if(t){clearInterval(t);t=null;buttons[1].textContent='Play'}else{t=setInterval(()=>{n++;show()},125);buttons[1].textContent='Pause'}};show();grid.append(card)}}
function showCondition(){const key=conditionSelect.value;conditionOnly.src=DATA.porthole.conditions[key];portholeComposite.src=DATA.porthole.composites[key]}
function setup(){document.querySelectorAll('button,select').forEach(x=>x.disabled=false);setupAssets();beforeRoom.src=DATA.beforeRoom;afterRoom.src=DATA.rooms.day;frameOnly.src=DATA.porthole.frame;conditionSelect.value='day';conditionSelect.onchange=showCondition;showCondition();moveSelect.value='5';const showMove=()=>moveProof.src=DATA.moves[moveSelect.value];moveSelect.onchange=showMove;showMove();for(const [key,url] of Object.entries(DATA.rooms)){const c=document.createElement('div');c.className='card';c.innerHTML=`<h3>${key}</h3><div class="scroll"></div>`;c.querySelector('.scroll').append(img(url,`${key} kitchen condition`));weatherRooms.append(c)}room12.src=DATA.room12;for(const row of DATA.rows){const tr=document.createElement('tr');tr.innerHTML=`<td>${row.name}</td><td>${row.measure}</td><td>${row.role}</td><td><code>${row.sha256}</code></td>`;rows.append(tr)}loading.textContent=`All ${urls.length} unique review images loaded and decoded. Controls enabled.`}
document.querySelectorAll('button,select').forEach(x=>x.disabled=true);Promise.all(urls.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed to load: ${e.message}`);
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


def main() -> None:
    for folder in (SOURCE, RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    for folder in (RAW, DRAFT, ASSETS):
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()

    catalogue = {
        "version": 8,
        "status": "reversible-draft",
        "recipe": RECIPE["id"],
        "projection": RECIPE["projection"],
        "wallAnchoring": RECIPE["wallAnchoring"],
        "sinkPorthole": RECIPE["sinkPorthole"],
        "movementPlacementsLp": {
            str(bay): {
                "sinkXLp": DOOR_DATUM + (bay - 1) * BAY,
                "frameXLp": DOOR_DATUM + (bay - 1) * BAY,
                "weatherUnderlayXLp": DOOR_DATUM + (bay - 1) * BAY,
            }
            for bay in (2, 5, 8)
        },
        "assets": {},
    }
    standards: dict[str, Image.Image] = {}
    for stem in ORDER:
        old_asset = V6_CATALOGUE["assets"][stem]
        entry = {
            "label": old_asset["label"], "cell": old_asset["cell"], "bays": old_asset["bays"],
            "interactionSpotKu": old_asset["interactionSpotKu"], "states": {},
        }
        if stem == "obj_fridge":
            entry["label"] = "Bright-white freestanding fridge"
        elif stem == "obj_bin":
            entry["label"] = "Smaller pedal bin"
        for state, old_state in old_asset["states"].items():
            frames = corrected_frames(stem, state)
            saved = save_strip(f"{stem}_{state}_f{len(frames)}", frames, tuple(entry["cell"]), old_state["meta"]["fps"], {
                "interactionSpotKu": entry["interactionSpotKu"],
                "backWallFootLineLp": FOOT_LINE,
                "correction": "new-v8-draft" if stem in CHANGED else "exact-v6-copy",
            })
            saved.update({
                "v6Urls": old_state["v6Urls"],
                "v8Urls": saved.pop("urls"),
                "v6StripSha256": old_state["v6StripSha256"],
                "v8StripSha256": saved["sha256"],
            })
            entry["states"][state] = saved
            if state == "standard":
                standards[stem] = frames[0]
        bounds = [bound for state in entry["states"].values() for bound in state["bounds"] if bound]
        entry["largestBound"] = {
            "widthLp": max(round(bound["widthLp"], 2) for bound in bounds),
            "heightLp": max(round(bound["heightLp"], 2) for bound in bounds),
        }
        catalogue["assets"][stem] = entry

    frame_rec = save_asset("obj_sink_porthole_frame_f1", PORTHOLE_FRAME, (21, 56), {
        "z": 26, "outerDiameterLp": 19, "apertureDiameterLp": 14, "aperture": "transparent-alpha",
    })
    condition_records = {condition: save_asset(f"obj_sink_porthole_condition_{condition}_f1", image, (21, 56), {
        "z": 24, "condition": condition, "parent": "obj_sink", "separateFromFrame": True,
    }) for condition, image in WEATHER.items()}
    composite_records = {condition: save_asset(f"obj_sink_porthole_composite_{condition}", porthole_layers(condition), (21, 56), {
        "reviewComposite": True, "condition": condition,
    }) for condition in WEATHER}

    rooms = {condition: save_asset(f"room_kitchen_9bay_{condition}", room_composite(standards, condition), (193, 56), {
        "reviewComposite": True, "backWallFootLineLp": FOOT_LINE, "condition": condition,
    }) for condition in WEATHER}
    moves = {str(bay): save_asset(f"sink_porthole_move_bay_{bay}", sink_move_proof(standards, bay), (193, 56), {
        "reviewComposite": True, "sinkBay": bay, "frameBay": bay, "conditionBay": bay,
    }) for bay in (2, 5, 8)}
    room12 = save_asset("room_kitchen_12bay_wall_anchored_outline", outline_12(), (256, 56), {
        "reviewComposite": True, "backWallFootLineLp": FOOT_LINE,
    })

    before_room_path = V7_RAW / "room_kitchen_9bay_composite.png"
    before_review = ASSETS / "room_kitchen_9bay_v7_before.png"
    save_png(Image.open(before_room_path).convert("RGBA"), before_review)
    before_url = "/keeper-review/kitchen-wall-anchored-v8/assets/room_kitchen_9bay_v7_before.png"

    data = {
        "assets": catalogue["assets"],
        "changed": CHANGED,
        "beforeRoom": before_url,
        "rooms": {key: value["urls"][0] for key, value in rooms.items()},
        "moves": {key: value["urls"][0] for key, value in moves.items()},
        "room12": room12["urls"][0],
        "porthole": {
            "frame": frame_rec["urls"][0],
            "conditions": {key: value["urls"][0] for key, value in condition_records.items()},
            "composites": {key: value["urls"][0] for key, value in composite_records.items()},
        },
        "rows": [
            {"name": "smaller pedal bin", "measure": "10 × 12 lp max", "role": "centred one-bay floor child", "sha256": catalogue["assets"]["obj_bin"]["states"]["standard"]["sha256"]},
            {"name": "bright-white fridge", "measure": "21 × 21-lp cell", "role": "freestanding; no counter", "sha256": catalogue["assets"]["obj_fridge"]["states"]["standard"]["sha256"]},
            {"name": "smooth counter family", "measure": "20-lp slab; 1.5-lp reveal", "role": "continuous exposed wings", "sha256": catalogue["assets"]["obj_sink"]["states"]["standard"]["sha256"]},
            {"name": "porthole frame", "measure": "19-lp outer; 14-lp aperture", "role": "transparent sink-owned frame", "sha256": frame_rec["sha256"]},
            {"name": "day condition", "measure": "21 × 56-lp child", "role": "separate z24 underlay", "sha256": condition_records["day"]["sha256"]},
            {"name": "9-bay anchored kitchen", "measure": "193 × 56 lp", "role": "foot line 52; 4-lp floor clear", "sha256": rooms["day"]["sha256"]},
        ],
    }
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)

    source_files = sorted(path for path in SOURCE.iterdir() if path.is_file())
    outputs = sorted(path for path in RAW.iterdir() if path.is_file()) + sorted(DRAFT.glob("*.json")) + source_files + [PUBLIC / "index.html"]
    register = {
        "version": 8,
        "status": "reversible-draft",
        "scope": "kitchen-surface-fridge-bin-wall-anchor-and-porthole-corrections",
        "visualBaseline": RECIPE["visualBaseline"],
        "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)},
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
        "v6Overwritten": False,
        "v7Overwritten": False,
        "protectedSnapshots": {
            "kitchenV6": tree_sha(V6_RAW),
            "kitchenRoomV7": tree_sha(V7_RAW),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
        "outputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs],
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({
        "set": "kitchen-wall-anchored-v8", "assets": len(catalogue["assets"]),
        "footLineLp": FOOT_LINE, "clearFloorLp": 4, "portholeDiameterLp": 19,
        "review": PUBLIC.relative_to(ROOT).as_posix(),
    }, indent=2))


if __name__ == "__main__":
    main()
