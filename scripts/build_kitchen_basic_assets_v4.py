#!/usr/bin/env python3
"""Build the reversible Kitchen Basic Assets V4 review batch.

V4 preserves V1/V2/V3 and the live game. It replaces only the rejected
perspective cupboard leaf with a flat rectangular foreground occluder and
demonstrates the complete cupboard activity lifecycle. Nothing under
public/sprites or runtime manifests is written.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-basic-assets-2026-10-16-v4"
GENERATED = SOURCE / "generated"
RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v4"
DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v4"
PUBLIC = ROOT / "public/keeper-review/kitchen-basic-assets-v4"
ASSETS = PUBLIC / "assets"
V2_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v2"
V2_SOURCE = ROOT / "art/source/kitchen-basic-assets-2026-10-16-v2/generated"
V3_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v3"

DENSITY = 4
KU_PER_LP = 8
BAY = 21
DOOR_CLEAR = 4
ROOM_H = 56
ROOM_9_W = 193
ROOM_12_W = 256

INK = "#071b32"
WOOD_DARK = "#5d301d"
WOOD = "#9a5630"
WOOD_LIGHT = "#d38a46"
CREAM = "#f7dda5"
CREAM_LIGHT = "#fff1c9"
CREAM_SHADOW = "#d9b776"
BLUE = "#16a3b9"
BLUE_LIGHT = "#65dce4"
BRASS = "#d79622"
BRASS_LIGHT = "#ffd067"
SMOKE = "#68747c"
WATER = "#34bfea"
FLAME = "#ff8c1a"
FLAME_LIGHT = "#ffe15b"


SPECS = {
    "obj_bin": {"label": "Full-bay pedal bin", "cell": [21, 16], "bound": [20, 14], "bays": 1, "offset": 0, "states": ["standard", "full", "overflowing"]},
    "obj_fridge": {"label": "Freestanding under-counter fridge", "cell": [21, 21], "bound": [20, 19], "bays": 1, "offset": 0, "states": ["standard", "on", "broken"]},
    "obj_kettle": {"label": "Full-bay stove kettle unit", "cell": [21, 31], "bound": [20, 30], "bays": 1, "offset": 0, "states": ["standard", "on", "broken"]},
    "obj_toaster": {"label": "Full-bay toaster unit", "cell": [21, 31], "bound": [20, 30], "bays": 1, "offset": 0, "states": ["standard", "on", "broken"]},
    "obj_cooker": {"label": "Full-bay basic oven", "cell": [21, 28], "bound": [20, 26], "bays": 1, "offset": 0, "states": ["standard", "on", "broken"]},
    "obj_mixer": {"label": "Full-bay mixer unit", "cell": [21, 31], "bound": [20, 30], "bays": 1, "offset": 0, "states": ["standard", "on", "broken"]},
    "obj_sink": {"label": "Full-bay sink unit", "cell": [21, 29], "bound": [20, 27], "bays": 1, "offset": 0, "states": ["standard", "on", "broken"]},
    "obj_table": {"label": "Layered table for one + chair", "cell": [42, 28], "bound": [40, 26], "bays": 2, "offset": 0, "states": ["standard"]},
    "obj_petbowl": {"label": "Pet bowl", "cell": [16, 8], "bound": [12, 3], "bays": 0, "offset": 0, "states": ["standard", "full", "broken"]},
    "obj_cupboard": {"label": "Front-on walk-in cleaning cupboard", "cell": [38, 56], "bound": [36, 52], "bays": 0, "offset": -84, "states": ["standard", "on", "open"]},
}


def rgba(size, colour=(0, 0, 0, 0)):
    return Image.new("RGBA", size, colour)


def hard_alpha(im: Image.Image, threshold: int = 96) -> Image.Image:
    im = im.convert("RGBA")
    im.putalpha(im.getchannel("A").point(lambda a: 255 if a >= threshold else 0))
    return im


def crop_alpha(im: Image.Image) -> Image.Image:
    im = hard_alpha(im)
    box = im.getchannel("A").getbbox()
    if not box:
        raise ValueError("source has no opaque pixels")
    return im.crop(box)


def sheet_slice(name: str, index: int, count: int) -> Image.Image:
    im = Image.open(GENERATED / name).convert("RGBA")
    x0 = round(im.width * index / count)
    x1 = round(im.width * (index + 1) / count)
    return im.crop((x0, 0, x1, im.height))


def source(stem: str) -> Image.Image:
    run = {
        "obj_fridge_standard": 0,
        "obj_kettle_standard": 1,
        "obj_toaster_standard": 2,
        "obj_cooker_standard": 3,
        "obj_mixer_standard": 4,
        "obj_sink_standard": 5,
    }
    if stem in run:
        return sheet_slice("kitchen_run_standard_sheet.png", run[stem], 6)
    if stem == "obj_bin_standard":
        im = Image.open(GENERATED / "bin_bowl_sheet.png").convert("RGBA")
        return im.crop((200, 0, 910, im.height))
    if stem == "obj_petbowl_standard":
        im = Image.open(GENERATED / "bin_bowl_sheet.png").convert("RGBA")
        return im.crop((1000, 0, 1730, im.height))
    if stem == "obj_table_standard":
        return Image.open(GENERATED / "table_layers_sheet.png").convert("RGBA")
    if stem == "obj_cupboard_leaf":
        return Image.open(GENERATED / "flat_cupboard_leaf_source.png").convert("RGBA")
    if stem.startswith("obj_cupboard_"):
        im = Image.open(GENERATED / "cupboard_layers_sheet.png").convert("RGBA")
        box = {
            "obj_cupboard_closed": (30, 0, 540, im.height),
            "obj_cupboard_recess": (560, 0, 1090, im.height),
        }[stem]
        return im.crop(box)
    return Image.open(V2_SOURCE / f"{stem}_source.png").convert("RGBA")


def fit_source(stem: str, cell: tuple[int, int], bound: tuple[int, int]) -> Image.Image:
    src = crop_alpha(source(stem))
    max_w, max_h = bound[0] * DENSITY, bound[1] * DENSITY
    if stem in {"obj_bin_standard", "obj_fridge_standard", "obj_sink_standard", "obj_petbowl_standard"}:
        size = (max_w, max_h)
    else:
        scale = min(max_w / src.width, max_h / src.height)
        size = (max(1, round(src.width * scale)), max(1, round(src.height * scale)))
    src = hard_alpha(src.resize(size, Image.Resampling.LANCZOS), 128)
    out = rgba((cell[0] * DENSITY, cell[1] * DENSITY))
    out.alpha_composite(src, ((out.width - src.width) // 2, out.height - src.height))
    return out


def constrain_to_bound(im: Image.Image, bound: tuple[int, int]) -> Image.Image:
    """Keep state effects inside the same centred, floor-aligned art envelope."""
    bound_w, bound_h = bound[0] * DENSITY, bound[1] * DENSITY
    left = (im.width - bound_w) // 2
    top = im.height - bound_h
    out = rgba(im.size)
    out.alpha_composite(im.crop((left, top, left + bound_w, top + bound_h)), (left, top))
    return out


def table_layers() -> tuple[Image.Image, Image.Image]:
    src = hard_alpha(source("obj_table_standard"))
    left = crop_alpha(src.crop((100, 0, 610, src.height)))
    right = crop_alpha(src.crop((620, 0, 1460, src.height)))
    chair = hard_alpha(left.resize((20 * DENSITY, 26 * DENSITY), Image.Resampling.LANCZOS), 128)
    table = hard_alpha(right.resize((40 * DENSITY, 17 * DENSITY), Image.Resampling.LANCZOS), 128)
    chair_layer = rgba((42 * DENSITY, 28 * DENSITY))
    table_layer = rgba((42 * DENSITY, 28 * DENSITY))
    floor = 28 * DENSITY
    chair_layer.alpha_composite(chair, (11 * DENSITY, floor - chair.height))
    table_layer.alpha_composite(table, (1 * DENSITY, floor - table.height))
    return chair_layer, table_layer


def table_frame() -> Image.Image:
    chair, table = table_layers()
    out = chair.copy()
    out.alpha_composite(table)
    return out


def repeat_frame(shift: int = 0) -> Image.Image:
    src = crop_alpha(source("room_repeat"))
    crop_w = round(src.height * BAY / ROOM_H)
    cx = src.width // 2 + shift
    tile = src.crop((cx - crop_w // 2, 0, cx + crop_w // 2, src.height))
    tile = tile.resize((BAY * DENSITY, ROOM_H * DENSITY), Image.Resampling.LANCZOS)
    return hard_alpha(ImageEnhance.Contrast(tile).enhance(1.03), 128)


def stair_frame(opened: bool) -> Image.Image:
    name = "room_stair_open" if opened else "room_stair_closed"
    src = crop_alpha(source(name))
    return hard_alpha(src.resize((46 * DENSITY, ROOM_H * DENSITY), Image.Resampling.LANCZOS), 128)


def cupboard_closed() -> Image.Image:
    # The closed far-wall leaf is a complete floor-to-lintel occluder.  It
    # must hide the Keeper's boots and either cleaning tool during the swap.
    src = crop_alpha(source("obj_cupboard_closed"))
    src = hard_alpha(src.resize((36 * DENSITY, 52 * DENSITY), Image.Resampling.LANCZOS), 128)
    out = rgba((38 * DENSITY, ROOM_H * DENSITY))
    out.alpha_composite(src, (DENSITY, 4 * DENSITY))
    return out


def cupboard_recess() -> Image.Image:
    src = crop_alpha(source("obj_cupboard_recess"))
    src = hard_alpha(src.resize((36 * DENSITY, 52 * DENSITY), Image.Resampling.LANCZOS), 128)
    out = rgba((38 * DENSITY, ROOM_H * DENSITY))
    out.alpha_composite(src, (DENSITY, 4 * DENSITY))
    return out


def cupboard_leaf(width_lp: int = 34) -> Image.Image:
    src = crop_alpha(source("obj_cupboard_leaf"))
    # Fit the generated surface into an exact orthographic rectangle. The
    # colour comes from the source art; the deterministic alpha slab prevents
    # accidental perspective, taper or a false visible side edge.
    src = src.resize((width_lp * DENSITY, 52 * DENSITY), Image.Resampling.LANCZOS)
    src.putalpha(Image.new("L", src.size, 255))
    out = rgba((38 * DENSITY, ROOM_H * DENSITY))
    out.alpha_composite(src, ((38 - width_lp - 1) * DENSITY, 4 * DENSITY))
    return out


def cupboard_open(width_lp: int = 28) -> Image.Image:
    out = cupboard_recess()
    out.alpha_composite(cupboard_leaf(width_lp))
    return out


def draw_effect(base: Image.Image, stem: str, state: str, frame: int) -> Image.Image:
    im = base.copy()
    d = ImageDraw.Draw(im)
    w, h = im.size
    q = DENSITY
    if state == "on":
        if stem == "obj_fridge":
            x = 5 * q
            door_w = (2 + frame * 3) * q
            d.polygon([(x, 5*q), (x+door_w, 7*q), (x+door_w, h-2*q), (x, h-2*q)], fill=BLUE, outline=INK, width=q)
        elif stem == "obj_kettle":
            for k in range(2):
                y = (5 - frame - k * 3) * q
                d.ellipse((9*q, y, 13*q, y+4*q), fill=CREAM_LIGHT, outline=INK, width=max(1, q//2))
        elif stem == "obj_toaster":
            y = max(q, (7 - [0, 2, 5, 2][frame]) * q)
            d.rounded_rectangle((8*q, y, 13*q, y+4*q), radius=q, fill=CREAM_SHADOW, outline=WOOD_DARK, width=q)
        elif stem == "obj_cooker":
            hob_y = h - 19*q
            for x in (6*q, 15*q):
                flame_h = [1, 3, 2, 4][frame] * q
                d.polygon([(x-2*q, hob_y), (x, hob_y-flame_h), (x+2*q, hob_y)], fill=FLAME, outline=FLAME_LIGHT)
        elif stem == "obj_mixer":
            d.arc((5*q, 3*q, 17*q, 14*q), frame*55, frame*55+160, fill=BLUE_LIGHT, width=q)
        elif stem == "obj_sink":
            d.line((12*q, 4*q, 11*q, (9+frame)*q), fill=WATER, width=q)
    elif state == "broken":
        # Shared wobble/smoke/sparks with a small per-object cue.
        dx = [-1, 1, -1, 1][frame] * q // 2
        shifted = rgba(im.size)
        shifted.alpha_composite(im, (dx, 0))
        im = shifted
        d = ImageDraw.Draw(im)
        for k in range(3):
            x = (8 + ((frame + k * 2) % 6)) * q
            y = (5 - k * 2) * q
            d.ellipse((x-2*q, y-2*q, x+2*q, y+2*q), fill=SMOKE, outline=INK, width=max(1, q//2))
        sx, sy = (4 + frame*3)*q, (5 + frame%2)*q
        d.line((sx-2*q, sy, sx+2*q, sy), fill=FLAME_LIGHT, width=q)
        d.line((sx, sy-2*q, sx, sy+2*q), fill=FLAME, width=q)
        if stem == "obj_sink":
            d.ellipse((7*q, h-2*q, (14+frame)*q, h), fill=WATER)
        elif stem == "obj_toaster":
            d.rounded_rectangle(((12+frame)*q, 2*q, (17+frame)*q, 6*q), radius=q, fill=CREAM_SHADOW, outline=WOOD_DARK, width=q)
        elif stem == "obj_fridge":
            d.line((4*q, h-4*q, (8+frame)*q, h-2*q), fill=BLUE_LIGHT, width=q)
    return im


def make_strip(frames: list[Image.Image]) -> Image.Image:
    out = rgba((frames[0].width * len(frames), frames[0].height))
    for i, frame in enumerate(frames):
        out.alpha_composite(frame, (i * frame.width, 0))
    return out


def alpha_bounds(frame: Image.Image) -> dict[str, float] | None:
    box = frame.getchannel("A").getbbox()
    if not box:
        return None
    x0, y0, x1, y1 = box
    return {"xLp": x0 / DENSITY, "yLp": y0 / DENSITY, "widthLp": (x1-x0) / DENSITY, "heightLp": (y1-y0) / DENSITY}


def save_strip(name: str, frames: list[Image.Image], logical: tuple[int, int], fps: int, meta: dict | None = None) -> dict:
    strip = make_strip(frames)
    png = RAW / f"{name}.png"
    strip.save(png, optimize=True)
    data = {"w": logical[0], "h": logical[1], "frames": len(frames), "fps": fps, "density": DENSITY, "anchor": [logical[0]/2, logical[1]], "z": 40}
    if meta:
        data.update(meta)
    png.with_suffix(".json").write_text(json.dumps(data, indent=2) + "\n")
    urls = []
    for i, frame in enumerate(frames):
        fn = f"{name}_frame{i+1}.png"
        frame.save(ASSETS / fn, optimize=True)
        urls.append(f"/keeper-review/kitchen-basic-assets-v4/assets/{fn}")
    return {"png": png.relative_to(ROOT).as_posix(), "meta": data, "urls": urls, "bounds": [alpha_bounds(f) for f in frames]}


def load_keeper(stem: str) -> list[str]:
    candidates = list((ROOT / "art/raw/keeper-first-batch").glob(f"{stem}_f*.png"))
    if len(candidates) != 1:
        raise ValueError(f"expected one source strip for {stem}, found {len(candidates)}")
    png = candidates[0]
    meta = json.loads(png.with_suffix(".json").read_text())
    strip = Image.open(png).convert("RGBA")
    fw, fh = meta["w"] * meta["density"], meta["h"] * meta["density"]
    urls = []
    for i in range(meta["frames"]):
        frame = strip.crop((i*fw, 0, (i+1)*fw, fh))
        fn = f"{stem}_frame{i+1}.png"
        frame.save(ASSETS / fn, optimize=True)
        urls.append(f"/keeper-review/kitchen-basic-assets-v4/assets/{fn}")
    return urls


def shell(width_lp: int) -> Image.Image:
    out = rgba((width_lp * DENSITY, ROOM_H * DENSITY))
    for k, x in enumerate(range(DOOR_CLEAR, width_lp, BAY)):
        tile = REPEATS[k % len(REPEATS)]
        crop_w = min(BAY, width_lp - x) * DENSITY
        out.alpha_composite(tile.crop((0, 0, crop_w, tile.height)), (x*DENSITY, 0))
    stair = STAIR_CLOSED.crop((42*DENSITY, 0, 46*DENSITY, ROOM_H*DENSITY))
    out.alpha_composite(stair, (0, 0))
    return out


def composite(width_lp: int, outline: bool = False) -> Image.Image:
    out = shell(width_lp)
    d = ImageDraw.Draw(out)
    if outline:
        reservations = [(1,1),(2,2),(4,1),(5,1),(6,2),(8,1),(9,2),(11,1),(12,1)]
        for bay, span in reservations:
            x0 = (DOOR_CLEAR + (bay-1)*BAY + 1) * DENSITY
            x1 = (DOOR_CLEAR + (bay-1+span)*BAY - 1) * DENSITY
            d.rectangle((x0, 15*DENSITY, x1, 54*DENSITY), outline=BLUE, width=DENSITY)
        return out
    order = ["obj_bin", "obj_fridge", "obj_kettle", "obj_toaster", "obj_cooker", "obj_mixer", "obj_sink", "obj_table"]
    bays = [1,2,3,4,5,6,7,8]
    for stem, bay in zip(order, bays):
        frame = STANDARD[stem]
        span = SPECS[stem]["bays"]
        x = (DOOR_CLEAR + (bay-1)*BAY) * DENSITY + (span*BAY*DENSITY-frame.width)//2
        y = ROOM_H*DENSITY - frame.height
        out.alpha_composite(frame, (x, y))
    return out


def write_review(catalogue: dict, keeper: dict[str, list[str]]) -> None:
    data = {
        "assets": catalogue["assets"],
        "keeper": keeper,
        "v2": {},
        "shells": {},
        "room9": "/keeper-review/kitchen-basic-assets-v4/assets/room_kitchen_9bay_composite.png",
        "room12": "/keeper-review/kitchen-basic-assets-v4/assets/room_kitchen_12bay_outline.png",
        "cupboardClosed": catalogue["assets"]["obj_cupboard"]["states"]["standard"]["urls"][0],
        "cupboardOpen": catalogue["assets"]["obj_cupboard"]["states"]["open"]["urls"][0],
        "cupboardRecess": "/keeper-review/kitchen-basic-assets-v4/assets/obj_cupboard_recess_f1_frame1.png",
        "cupboardLeaf": "/keeper-review/kitchen-basic-assets-v4/assets/obj_cupboard_leaf_open_f1_frame1.png",
        "chairLayer": "/keeper-review/kitchen-basic-assets-v4/assets/obj_table_chair_back_f1_frame1.png",
        "tableLayer": "/keeper-review/kitchen-basic-assets-v4/assets/obj_table_foreground_f1_frame1.png",
    }
    for stem in SPECS:
        v2 = V3_RAW / f"{stem}_standard_f1.png"
        if v2.exists():
            fn = f"v2_{v2.name}"
            shutil.copy2(v2, ASSETS / fn)
            data["v2"][stem] = f"/keeper-review/kitchen-basic-assets-v4/assets/{fn}"
    for bays in range(6, 13):
        data["shells"][str(bays)] = f"/keeper-review/kitchen-basic-assets-v4/assets/room_kitchen_shell_{bays}bay_frame1.png"
    for ref in (SOURCE / "reference").glob("*.png"):
        shutil.copy2(ref, ASSETS / ref.name)
    data["references"] = [f"/keeper-review/kitchen-basic-assets-v4/assets/{p.name}" for p in sorted((SOURCE / "reference").glob("*.png"))]

    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Basic Assets V3</title><style>
:root{color-scheme:dark;--bg:#06141e;--panel:#102631;--line:#31505d;--ink:#f3f0df;--muted:#a9bdc4;--gold:#efb64d;--cyan:#57c7d4}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,sans-serif}header,main{max-width:1380px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}h1{margin:0 0 8px}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a}.notice{border-left:4px solid var(--gold);padding:12px 14px;background:#2b261b}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:14px}.card{background:#0a1d27;border:1px solid var(--line);border-radius:12px;padding:12px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:10px}.well{min-height:230px;display:flex;align-items:end;justify-content:center;background:repeating-conic-gradient(#172933 0 25%,#11232d 0 50%) 0/20px 20px;border-radius:8px;padding:12px;overflow:hidden}.well img{max-width:100%;max-height:260px;object-fit:contain}.v2 img{image-rendering:auto}.v3 img{image-rendering:auto}.label{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:9px}button,select{background:#17323e;color:var(--ink);border:1px solid #52717d;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.room-scroll{overflow:auto;background:#071923;border-radius:10px;padding:10px}.room-stage{position:relative;height:224px}.room-stage>img{position:absolute;left:0;top:0;height:224px;width:auto;image-rendering:auto}.cup{position:absolute;right:0!important;left:auto!important;z-index:6}.bowl{position:absolute!important;z-index:10;top:auto!important}.spot{position:absolute!important;z-index:7;top:auto!important}.guide{position:absolute;left:0;right:0;border-top:1px dashed;z-index:9;font-size:11px}.datum-stage{position:relative;width:168px;height:164px;margin:auto;background:#071923}.datum-stage img{position:absolute;image-rendering:auto}.datum-stage .chair-layer,.datum-stage .table-layer{width:168px;height:112px;left:0;top:48px}.datum-stage .chair-layer{z-index:1}.datum-stage .keeper{width:136px;height:160px;left:16px;top:0;z-index:2}.datum-stage .table-layer{z-index:3}.floor{top:160px;border-color:#fff}.seat{top:116px;border-color:#57c7d4}.tabletop{top:92px;border-color:#efb64d}.occlusion-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.cup-stage{position:relative;width:152px;height:224px;margin:auto;background:#071923;overflow:hidden}.cup-stage .recess{position:absolute;width:152px;height:224px;inset:0;z-index:1}.cup-stage .closed{position:absolute;width:152px;height:224px;inset:0;z-index:3}.cup-stage .keeper{position:absolute;width:136px;height:164px;top:60px;z-index:2}.cup-stage .leaf{position:absolute;width:152px;height:224px;inset:0;z-index:3}.finding{color:#ffdc8a}.refs img{width:100%;height:auto}.small{font-size:.9rem;color:var(--muted)}table{width:100%;border-collapse:collapse}th,td{text-align:left;border-bottom:1px solid var(--line);padding:8px}</style></head><body><header><h1>Kitchen Basic Assets V3</h1><span class="tag">Review-only correction · V1 and V2 preserved</span><p>Front-on cupboard layering, full-bay furniture and rear-facing seating. Nothing is approved, promoted or wired.</p></header><main>
<p class="notice"><strong>V3 changes:</strong> every one-bay object now fills 20 of 21 lp; the cupboard is straight ahead in the right end wall with a separate foreground leaf; and the approved rear-facing sit clip is staged between chair and table layers.</p>
<section class="panel"><h2>Reference direction</h2><div class="grid refs"><img id="ref0" alt="Furniture style reference"><img id="ref1" alt="Room shell style reference"></div></section>
<section class="panel"><h2>V2 → V3 fit comparison</h2><p>V2 remains unchanged on the left. V3 occupies the usable width of each bay with only a 0.5-lp safety margin per side.</p><div id="assetGrid" class="grid"></div></section>
<section class="panel"><h2>Modular shell · 6–12 bays</h2><div class="controls"><label>Assembly <select id="shellSelect" disabled></select></label></div><div class="room-scroll"><img id="shellImage" alt="Selected V2 modular shell" style="height:224px;width:auto"></div></section>
<section class="panel"><h2>9-bay starting kitchen · 193 × 56 lp</h2><p>Accepted order and widths are unchanged; the cupboard remains last. The pet bowl is still a foreground child of the table.</p><div class="controls"><select id="spotSelect" disabled></select></div><div class="room-scroll"><div id="room9" class="room-stage" style="width:772px"><img id="room9base" alt="V2 nine-bay kitchen"><img id="room9cup" class="cup" alt="Closed far-wall cupboard"><img id="room9keeper" class="spot" alt="Keeper at selected interaction spot"><img id="room9bowl" class="bowl" alt="Pet bowl foreground"></div></div></section>
<section class="panel"><h2>12-bay upgrade reservation · 256 × 56 lp</h2><div class="room-scroll"><img id="room12" alt="V2 twelve-bay outline" style="height:224px;width:auto"></div></section>
<section class="panel"><h2>Rear-facing seated composition</h2><div class="grid"><div><div class="datum-stage"><img id="chairLayer" class="chair-layer" alt="Chair background layer"><img id="sitBackKeeper" class="keeper" alt="Approved rear-facing sit animation"><img id="tableLayer" class="table-layer" alt="Table foreground layer"><span class="guide floor">floor / boot soles</span><span class="guide seat">seat 11 lp</span><span class="guide tabletop">table 17 lp</span></div></div><div><p><strong>Recommended staging:</strong> the recorded <code>keeper_sit_back</code> clip is 34×40 lp, faces back, and uses seatPoint y=29.33 from a y=40 floor anchor: <strong>10.67 lp above floor</strong>. It is an existing approved clip; no Keeper redraw is proposed.</p><p>The chair is behind him and the 40-lp table is in front. Its apron hides the thighs while his boots remain visible between the outer legs, reading as feet beneath the table rather than a character parked in front of it. Surface remains <strong>17 lp</strong>; underside remains 15 lp.</p></div></div></section>
<section class="panel"><h2>Front-on right-wall cupboard sequence</h2><p>The dollhouse camera looks straight into the end wall. In all three frames the recess is behind the Keeper and the outward-opening door leaf is a separate foreground layer.</p><div class="occlusion-grid"><div class="card"><h3>1 · Walk in behind leaf</h3><div class="cup-stage"><img class="recess" id="recessA"><img class="keeper" id="walkIn"><img class="leaf" id="leafA"></div></div><div class="card"><h3>2 · Fully occluded swap</h3><div class="cup-stage"><img class="closed" id="closedB"><img class="keeper" id="hiddenKeeper"></div></div><div class="card"><h3>3 · Emerge already sweeping</h3><div class="cup-stage"><img class="recess" id="recessC"><img class="keeper" id="walkOut"><img class="leaf" id="leafC"></div></div></div><p class="finding"><strong>V3 answer:</strong> yes—the full-height foreground leaf hides Keeper, boots and tool. He can enter unencumbered and emerge in <code>keeper_sweep_broom</code>; no turn animation while holding the broom is needed.</p></section>
<section class="panel"><h2>19-lp oven door</h2><div class="grid"><div class="card"><h3>Cake retrieval</h3><div class="datum-stage" style="width:168px"><img id="ovenArt" style="position:absolute;width:84px;height:112px;left:42px;top:52px"><img id="cakeKeeper" style="position:absolute;width:136px;height:164px;left:16px;top:0"></div></div><div class="card"><h3>Meal retrieval</h3><div class="datum-stage" style="width:168px"><img id="ovenArtMeal" style="position:absolute;width:84px;height:112px;left:42px;top:52px"><img id="mealKeeper" style="position:absolute;width:136px;height:164px;left:16px;top:0"></div></div><p><strong>V3 answer:</strong> both existing retrieval clips still read against the 19-lp door and 10-lp rack datum. Frank's accepted cake staging is unchanged.</p></div></section>
<section class="panel"><h2>Measured V3 hand-back</h2><table><thead><tr><th>Item</th><th>Largest bound</th><th>Bays</th><th>Interaction</th></tr></thead><tbody id="measureRows"></tbody></table><p class="small">Draft only. V1/V2 remain immutable; rejection is reversible by discarding the V3 directories alone.</p></section>
</main><script>const DATA=__DATA__;const all=[];function urls(v){if(typeof v==='string'&&v.includes('/assets/'))all.push(v);else if(Array.isArray(v))v.forEach(urls);else if(v&&typeof v==='object')Object.values(v).forEach(urls)}urls(DATA);const uniq=[...new Set(all)];function assetState(stem,state){return DATA.assets[stem].states[state]}function img(src,alt){const i=document.createElement('img');i.src=src;i.alt=alt;return i}function setup(){document.querySelectorAll('button,select').forEach(x=>x.disabled=false);document.getElementById('ref0').src=DATA.references[0];document.getElementById('ref1').src=DATA.references[1];const grid=document.getElementById('assetGrid');Object.entries(DATA.assets).forEach(([stem,a])=>{const card=document.createElement('article');card.className='card';const states=Object.keys(a.states);card.innerHTML=`<h3>${a.label}</h3><div class="compare"><div><div class="label">V1</div><div class="well v1"></div></div><div><div class="label">V2 density 4</div><div class="well v2"></div></div></div><div class="controls"><button disabled>Play</button><span class="state"></span></div><p class="small">${a.bays} bay(s) · canvas ${a.cell.join('×')} lp</p>`;const old=DATA.v1[stem];if(old)card.querySelector('.v1 .well').append(img(old,`${a.label} V1`));const target=card.querySelector('.v2 .well'),stateText=card.querySelector('.state'),button=card.querySelector('button');let si=0,fi=0,timer=null;function show(){const s=states[si],u=a.states[s].urls;target.replaceChildren(img(u[fi%u.length],`${a.label} ${s}`));stateText.textContent=`${s} · ${fi%u.length+1}/${u.length}`}function tick(){fi++;if(fi>=a.states[states[si]].urls.length){fi=0;si=(si+1)%states.length}show()}button.onclick=()=>{if(timer){clearInterval(timer);timer=null;button.textContent='Play'}else{timer=setInterval(tick,125);button.textContent='Pause'}};show();grid.append(card)});const shellSel=document.getElementById('shellSelect');Object.keys(DATA.shells).forEach(n=>shellSel.add(new Option(`${n} bays · ${4+21*Number(n)} lp`,n)));shellSel.value='9';function shell(){document.getElementById('shellImage').src=DATA.shells[shellSel.value]}shellSel.onchange=shell;shell();document.getElementById('room9base').src=DATA.room9;document.getElementById('room9cup').src=DATA.cupboardClosed;document.getElementById('room12').src=DATA.room12;const spots=[['Bin',14.5],['Fridge',35.5],['Kettle',56.5],['Toaster',77.5],['Oven',98.5],['Mixer',119.5],['Sink',140.5],['Table chair',161.5],['Pet bowl',172],['Cupboard',182.5]],ss=document.getElementById('spotSelect');spots.forEach((s,i)=>ss.add(new Option(`${s[0]} · ${Math.round(s[1]*8)} ku`,i)));function spot(){const i=Number(ss.value||0),x=spots[i][1]*4,k=document.getElementById('room9keeper'),b=document.getElementById('room9bowl'),c=document.getElementById('room9cup');k.src=DATA.keeper.keeper_walk[0];k.style.width='136px';k.style.height='164px';k.style.left=`${x-68}px`;k.style.top='60px';b.src=assetState('obj_petbowl','standard').urls[0];b.style.width='64px';b.style.height='32px';b.style.left=`${172*4-32}px`;b.style.top='192px';c.src=i===9?DATA.cupboardOpen:DATA.cupboardClosed}ss.onchange=spot;spot();document.getElementById('tableArt').src=assetState('obj_table','standard').urls[0];document.getElementById('eatKeeper').src=DATA.keeper.keeper_eat_seated[0];document.getElementById('walkIn').src=DATA.keeper.keeper_walk[2];document.getElementById('walkIn').style.left='-24px';document.getElementById('hiddenKeeper').src=DATA.keeper.keeper_walk[4];document.getElementById('hiddenKeeper').style.left='28px';document.getElementById('walkOut').src=DATA.keeper.keeper_sweep_broom[0];document.getElementById('walkOut').style.left='-34px';['cupA','cupB','cupC'].forEach(id=>document.getElementById(id).src=DATA.cupboardOpen);document.getElementById('ovenArt').src=assetState('obj_cooker','standard').urls[0];document.getElementById('cakeKeeper').src=DATA.keeper.keeper_cake_from_oven_back[3];const rows=document.getElementById('measureRows');Object.values(DATA.assets).forEach(a=>{const r=document.createElement('tr');r.innerHTML=`<td>${a.label}</td><td>${a.largestBound.widthLp}×${a.largestBound.heightLp} lp</td><td>${a.bays}</td><td>${a.interactionOffsetKu} ku</td>`;rows.append(r)})}Promise.all(uniq.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,e=>bad(new Error(`decode ${src}: ${e}`))):ok();i.onerror=()=>bad(new Error(`load ${src}`));i.src=src}))).then(setup).catch(e=>document.body.insertAdjacentHTML('afterbegin',`<p class="notice">Media failed: ${e}</p>`));</script></body></html>'''
    html = html.replace('<div class="label">V1</div><div class="well v1"></div>', '<div class="label">V2</div><div class="well v2"></div>')
    html = html.replace('<div class="label">V2 density 4</div><div class="well v2"></div>', '<div class="label">V3 full-bay</div><div class="well v3"></div>')
    html = html.replace("const old=DATA.v1[stem]", "const old=DATA.v2[stem]")
    html = html.replace("card.querySelector('.v1 .well')", "card.querySelector('.well.v2')")
    html = html.replace("`${a.label} V1`", "`${a.label} V2`")
    html = html.replace("card.querySelector('.v2 .well')", "card.querySelector('.well.v3')")
    html = html.replace("button=card.querySelector('button');let", "button=card.querySelector('button');button.disabled=false;let")
    html = html.replace("hiddenKeeper').src=DATA.keeper.keeper_walk[4]", "hiddenKeeper').src=DATA.keeper.keeper_sweep_broom[4]")
    html = html.replace("document.getElementById('tableArt').src=assetState('obj_table','standard').urls[0];document.getElementById('eatKeeper').src=DATA.keeper.keeper_eat_seated[0];", "document.getElementById('chairLayer').src=DATA.chairLayer;document.getElementById('tableLayer').src=DATA.tableLayer;document.getElementById('sitBackKeeper').src=DATA.keeper.keeper_sit_back[5];")
    html = html.replace("k.src=DATA.keeper.keeper_walk[0]", "k.src=DATA.keeper.keeper_walk[0]")
    html = html.replace("c.src=i===9?DATA.cupboardOpen:DATA.cupboardClosed", "c.src=DATA.cupboardClosed")
    html = html.replace("document.getElementById('walkIn').src=DATA.keeper.keeper_walk[2]", "document.getElementById('walkIn').src=DATA.keeper.keeper_walk_into_lift[1]")
    html = html.replace("walkIn').style.left='-24px'", "walkIn').style.left='8px'")
    html = html.replace("document.getElementById('hiddenKeeper').style.left='28px'", "document.getElementById('hiddenKeeper').style.left='8px'")
    html = html.replace("document.getElementById('walkOut').style.left='-34px'", "document.getElementById('walkOut').style.left='-2px'")
    html = html.replace("['cupA','cupB','cupC'].forEach(id=>document.getElementById(id).src=DATA.cupboardOpen)", "document.getElementById('recessA').src=DATA.cupboardRecess;document.getElementById('recessC').src=DATA.cupboardRecess;document.getElementById('leafA').src=DATA.cupboardLeaf;document.getElementById('leafC').src=DATA.cupboardLeaf;document.getElementById('closedB').src=DATA.cupboardClosed")
    html = html.replace("document.getElementById('cakeKeeper').src=DATA.keeper.keeper_cake_from_oven_back[3];const rows=", "document.getElementById('cakeKeeper').src=DATA.keeper.keeper_cake_from_oven_back[3];document.getElementById('ovenArtMeal').src=assetState('obj_cooker','standard').urls[0];document.getElementById('mealKeeper').src=DATA.keeper.keeper_meal_from_oven_back[3];const rows=")
    html = html.replace("Kitchen Basic Assets V3", "Kitchen Basic Assets V4")
    html = html.replace("Review-only correction · V1 and V2 preserved", "Review-only correction · V1, V2 and V3 preserved")
    html = html.replace("<strong>V3 changes:</strong> every one-bay object now fills 20 of 21 lp; the cupboard is straight ahead in the right end wall with a separate foreground leaf; and the approved rear-facing sit clip is staged between chair and table layers.", "<strong>V4 correction:</strong> the rejected perspective leaf is replaced by a full, flat rectangular door. It is hinged on the right, extends left, stays open through the cupboard activity and put-away, and closes automatically only after the standard-walk exit is clear.")
    html = html.replace("V2 → V3 fit comparison", "V3 → V4 review comparison")
    html = html.replace("V2 remains unchanged on the left. V3 occupies the usable width of each bay with only a 0.5-lp safety margin per side.", "V3 remains unchanged on the left. V4 retains the accepted full-grid furniture; the only redraft in this pass is the cupboard leaf and its full lifecycle proof.")
    html = html.replace('<div class="label">V2</div><div class="well v2"></div>', '<div class="label">V3</div><div class="well v2"></div>')
    html = html.replace('<div class="label">V3 full-bay</div><div class="well v3"></div>', '<div class="label">V4 flat leaf</div><div class="well v3"></div>')
    html = html.replace("`${a.label} V2`", "`${a.label} V3`")
    old_sequence = '<section class="panel"><h2>Front-on right-wall cupboard sequence</h2><p>The dollhouse camera looks straight into the end wall. In all three frames the recess is behind the Keeper and the outward-opening door leaf is a separate foreground layer.</p><div class="occlusion-grid"><div class="card"><h3>1 · Walk in behind leaf</h3><div class="cup-stage"><img class="recess" id="recessA"><img class="keeper" id="walkIn"><img class="leaf" id="leafA"></div></div><div class="card"><h3>2 · Fully occluded swap</h3><div class="cup-stage"><img class="closed" id="closedB"><img class="keeper" id="hiddenKeeper"></div></div><div class="card"><h3>3 · Emerge already sweeping</h3><div class="cup-stage"><img class="recess" id="recessC"><img class="keeper" id="walkOut"><img class="leaf" id="leafC"></div></div></div><p class="finding"><strong>V3 answer:</strong> yes—the full-height foreground leaf hides Keeper, boots and tool. He can enter unencumbered and emerge in <code>keeper_sweep_broom</code>; no turn animation while holding the broom is needed.</p></section>'
    new_sequence = '<section class="panel"><h2>Flat right-hinged cupboard · complete activity loop</h2><p>The dollhouse camera remains straight-on. The leaf is a full flat rectangle with parallel edges, hinged on the right and extending left in the foreground. Only its handle projects visually. The door remains open throughout the activity and put-away.</p><div class="occlusion-grid"><div class="card"><h3>1 · Enter behind leaf</h3><div class="cup-stage"><img class="recess" id="recessA"><img class="keeper" id="walkIn"><img class="leaf" id="leafA"></div></div><div class="card"><h3>2 · Activity, door stays open</h3><div class="cup-stage"><img class="recess" id="recessB"><img class="keeper front" id="activityKeeper"><img class="leaf" id="leafB"></div></div><div class="card"><h3>3 · Return tool behind leaf</h3><div class="cup-stage"><img class="recess" id="recessC"><img class="keeper" id="hiddenKeeper"><img class="leaf" id="leafC"></div></div><div class="card"><h3>4 · Standard-walk exit</h3><div class="cup-stage"><img class="recess" id="recessD"><img class="keeper front" id="walkOut"><img class="leaf" id="leafD"></div></div><div class="card"><h3>5 · Auto-close after clear</h3><div class="cup-stage"><img class="closed" id="closedB"></div></div></div><p class="finding"><strong>V4 answer:</strong> the Keeper passes behind the open foreground leaf for both prop swaps, so neither broom nor hoover appears beneath it. He returns the item, emerges in the existing standard walk with no turn animation, and the door closes only once he is clear.</p></section>'
    html = html.replace(old_sequence, new_sequence)
    html = html.replace(".occlusion-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}", ".occlusion-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}")
    html = html.replace(".cup-stage{position:relative;width:152px;height:224px", ".cup-stage{position:relative;width:190px;height:224px")
    html = html.replace(".cup-stage .recess{position:absolute;width:152px;height:224px;inset:0;z-index:1}", ".cup-stage .recess{position:absolute;width:152px;height:224px;right:0;top:0;z-index:1}")
    html = html.replace(".cup-stage .closed{position:absolute;width:152px;height:224px;inset:0;z-index:3}", ".cup-stage .closed{position:absolute;width:152px;height:224px;right:0;top:0;z-index:3}")
    html = html.replace(".cup-stage .leaf{position:absolute;width:152px;height:224px;inset:0;z-index:3}", ".cup-stage .leaf{position:absolute;width:152px;height:224px;right:0;top:0;z-index:3}")
    html = html.replace(".cup-stage .keeper{position:absolute;width:136px;height:164px;top:60px;z-index:2}", ".cup-stage .keeper{position:absolute;width:136px;height:164px;top:60px;z-index:2}.cup-stage .keeper.front{z-index:4}")
    html = html.replace("document.getElementById('recessA').src=DATA.cupboardRecess;document.getElementById('recessC').src=DATA.cupboardRecess;document.getElementById('leafA').src=DATA.cupboardLeaf;document.getElementById('leafC').src=DATA.cupboardLeaf;document.getElementById('closedB').src=DATA.cupboardClosed", "['recessA','recessB','recessC','recessD'].forEach(id=>document.getElementById(id).src=DATA.cupboardRecess);['leafA','leafB','leafC','leafD'].forEach(id=>document.getElementById(id).src=DATA.cupboardLeaf);document.getElementById('closedB').src=DATA.cupboardClosed;document.getElementById('activityKeeper').src=DATA.keeper.keeper_sweep_broom[0];document.getElementById('activityKeeper').style.left='0px'")
    html = html.replace("document.getElementById('walkOut').src=DATA.keeper.keeper_sweep_broom[0]", "document.getElementById('walkOut').src=DATA.keeper.keeper_walk[1]")
    html = html.replace("hiddenKeeper').style.left='8px'", "hiddenKeeper').style.left='40px'")
    html = html.replace("walkOut').style.left='-2px'", "walkOut').style.left='0px'")
    html = html.replace("<strong>V3 answer:</strong> both existing retrieval clips", "<strong>V4 answer:</strong> both existing retrieval clips")
    html = html.replace("Measured V3 hand-back", "Measured V4 hand-back")
    html = html.replace("Draft only. V1/V2 remain immutable; rejection is reversible by discarding the V3 directories alone.", "Draft only. V1/V2/V3 remain immutable; rejection is reversible by discarding the V4 directories alone.")
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    for folder in (RAW, DRAFT, ASSETS):
        for p in folder.iterdir():
            if p.is_file():
                p.unlink()

    global REPEATS, STAIR_CLOSED, STANDARD
    REPEATS = [repeat_frame(-140), repeat_frame(0), repeat_frame(140)]
    STAIR_CLOSED = stair_frame(False)
    stair_open = stair_frame(True)

    STANDARD = {
        stem: (table_frame() if stem == "obj_table" else fit_source(f"{stem}_standard", tuple(spec["cell"]), tuple(spec["bound"])))
        for stem, spec in SPECS.items() if stem not in ("obj_cupboard",)
    }
    STANDARD["obj_cupboard"] = cupboard_closed()
    open_cupboard = cupboard_open()
    recess_cupboard = cupboard_recess()
    open_leaf = cupboard_leaf()
    chair_layer, table_layer = table_layers()

    catalogue = {"version": 4, "status": "reversible-draft", "density": DENSITY, "assets": {}, "room": {"doorClearLp": 4, "bayLp": 21, "heightLp": 56, "widthsLp": {"9": 193, "12": 256}}}
    for stem, spec in SPECS.items():
        entry = {"label": spec["label"], "cell": spec["cell"], "bays": spec["bays"], "interactionOffsetKu": spec["offset"], "states": {}}
        for state in spec["states"]:
            if stem == "obj_cupboard":
                if state == "standard": frames = [STANDARD[stem]]
                elif state == "open": frames = [open_cupboard]
                else: frames = [STANDARD[stem], open_cupboard, open_cupboard, open_cupboard]
            elif stem == "obj_bin":
                frames = [STANDARD[stem].copy()]
                d = ImageDraw.Draw(frames[0])
                if state in ("full", "overflowing"):
                    d.polygon([(5*DENSITY,3*DENSITY),(9*DENSITY,DENSITY),(15*DENSITY,4*DENSITY)], fill=CREAM_SHADOW, outline=INK)
                if state == "overflowing":
                    d.ellipse((2*DENSITY,12*DENSITY,7*DENSITY,15*DENSITY), fill=CREAM_LIGHT, outline=INK, width=DENSITY)
            elif stem == "obj_petbowl":
                frames = [STANDARD[stem].copy()] if state != "broken" else [STANDARD[stem].copy() for _ in range(4)]
                for i, fr in enumerate(frames):
                    d = ImageDraw.Draw(fr)
                    if state == "full": d.ellipse((4*DENSITY,5*DENSITY,12*DENSITY,7*DENSITY), fill=WOOD_DARK)
                    if state == "broken":
                        d.line((8*DENSITY,5*DENSITY,7*DENSITY,8*DENSITY), fill="#bd3d34", width=DENSITY)
                        d.ellipse((max(1, 3-i)*DENSITY,7*DENSITY,min(15, 13+i)*DENSITY,8*DENSITY), fill=WATER)
            elif state == "standard":
                frames = [STANDARD[stem]]
            else:
                frames = [draw_effect(STANDARD[stem], stem, state, i) for i in range(4)]
            frames = [constrain_to_bound(frame, tuple(spec["bound"])) for frame in frames]
            fps = 8 if len(frames) > 1 else 0
            saved = save_strip(f"{stem}_{state}_f{len(frames)}", frames, tuple(spec["cell"]), fps, {"interactionOffsetKu": spec["offset"]})
            entry["states"][state] = saved
        bounds = [b for state in entry["states"].values() for b in state["bounds"] if b]
        entry["largestBound"] = {"widthLp": max(round(b["widthLp"],2) for b in bounds), "heightLp": max(round(b["heightLp"],2) for b in bounds)}
        catalogue["assets"][stem] = entry

    # Sink dish overlays retain the V1 three-level contract.
    for level in range(1, 4):
        frames = [rgba((21*DENSITY,29*DENSITY))]
        d = ImageDraw.Draw(frames[0])
        for i in range(level*2):
            y = (12-i*2)*DENSITY
            d.ellipse((5*DENSITY,y,16*DENSITY,y+2*DENSITY), fill=CREAM_LIGHT, outline=INK, width=max(1,DENSITY//2))
        save_strip(f"obj_sink_dishes{level}_f1", frames, (21,29), 0)

    for i, tile in enumerate(REPEATS):
        save_strip(f"room_kitchen_repeat_{'abc'[i]}", [tile], (21,56), 0, {"z": 10})
    save_strip("room_kitchen_stair_cap_outward_closed", [STAIR_CLOSED], (46,56), 0, {"z": 15})
    save_strip("room_kitchen_stair_cap_outward_open", [stair_open], (46,56), 0, {"z": 15})
    save_strip("room_kitchen_far_cap_closed", [STANDARD["obj_cupboard"]], (38,56), 0, {"z": 60})
    save_strip("room_kitchen_far_cap_open", [open_cupboard], (38,56), 0, {"z": 60})
    save_strip("obj_cupboard_recess_f1", [recess_cupboard], (38,56), 0, {"z": 20, "layerRole": "background-recess"})
    save_strip("obj_cupboard_leaf_open_f1", [open_leaf], (38,56), 0, {"z": 80, "layerRole": "foreground-occluder"})
    save_strip("obj_table_chair_back_f1", [chair_layer], (42,28), 0, {"z": 35, "layerRole": "background-chair"})
    save_strip("obj_table_foreground_f1", [table_layer], (42,28), 0, {"z": 60, "layerRole": "foreground-table"})
    for bays in range(6, 13):
        im = shell(DOOR_CLEAR + bays*BAY)
        save_strip(f"room_kitchen_shell_{bays}bay", [im], (DOOR_CLEAR+bays*BAY,56), 0, {"z": 10})
    room9 = composite(ROOM_9_W)
    room12 = composite(ROOM_12_W, True)
    room9.save(RAW / "room_kitchen_9bay_composite.png", optimize=True)
    room12.save(RAW / "room_kitchen_12bay_outline.png", optimize=True)
    room9.save(ASSETS / "room_kitchen_9bay_composite.png", optimize=True)
    room12.save(ASSETS / "room_kitchen_12bay_outline.png", optimize=True)

    keeper = {stem: load_keeper(stem) for stem in ("keeper_walk", "keeper_walk_into_lift", "keeper_sweep_broom", "keeper_hoover_basic", "keeper_sit_back", "keeper_eat_seated", "keeper_cake_from_oven_back", "keeper_meal_from_oven_back")}
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    write_review(catalogue, keeper)

    inputs = sorted((SOURCE / "generated").glob("*.png")) + sorted((SOURCE / "reference").glob("*.png"))
    outputs = sorted(RAW.glob("*")) + sorted(DRAFT.glob("*.json")) + [PUBLIC / "index.html"]
    register = {
        "version": 4,
        "status": "reversible-draft",
        "supersedesForReviewOnly": "kitchen-basic-assets-v3",
        "geometryChanges": {"oneBayArtWidthLp": 20, "chairSeatLp": 11, "confirmedRearSeatContactLp": 10.67, "tableSurfaceLp": 17, "tableUndersideLp": 15, "tableLayering": "chair behind Keeper; table in foreground", "cupboardView": "front-on right end wall", "cupboardLayering": "recess behind Keeper; flat rectangular right-hinged leaf in foreground", "cupboardLeafWidthLp": 34, "cupboardLeafPerspective": False, "doorRemainsOpenDuringActivity": True, "doorClosesAfterStandardWalkExitClear": True, "broomTurnClipRequired": False},
        "inputs": [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p)} for p in inputs],
        "outputs": [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p)} for p in outputs if p.is_file()],
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"assets": len(catalogue["assets"]), "density": DENSITY, "roomWidths": [ROOM_9_W, ROOM_12_W], "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
