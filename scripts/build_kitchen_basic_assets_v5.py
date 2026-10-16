#!/usr/bin/env python3
"""Build the reversible Kitchen Basic Assets V5 flat-cutaway review.

V5 is review evidence only. It writes a new immutable source/raw/draft/review
set and never touches runtime sprites, registers, manifests, or game wiring.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-basic-assets-2026-10-16-v5"
GENERATED = SOURCE / "generated"
RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v5"
PUBLIC = ROOT / "public/keeper-review/kitchen-basic-assets-v5"
ASSETS = PUBLIC / "assets"

DENSITY = 4
KU_PER_LP = 8
BAY = 21
DOOR_DATUM = 4
ROOM_H = 56
FLOOR_BAND = 5
FOOT_Y = 56
ROOM_9_W = 193
ROOM_12_W = 256
PROJECTION = "flat-cutaway-v1"

INK = "#071b32"
WOOD_DARK = "#5d301d"
WOOD = "#9a5630"
WOOD_LIGHT = "#d38a46"
CREAM = "#f7dda5"
CREAM_LIGHT = "#fff1c9"
CREAM_SHADOW = "#d9b776"
TEAL = "#16a3b9"
TEAL_LIGHT = "#65dce4"
BRASS = "#d79622"
SMOKE = "#68747c"
WATER = "#34bfea"
FLAME = "#ff8c1a"
FLAME_LIGHT = "#ffe15b"


SPECS = {
    "obj_bin": {"label": "Full-bay pedal bin", "cell": [21, 16], "bound": [20, 14], "bays": 1, "states": ["standard", "full", "overflowing"], "top": 0},
    "obj_fridge": {"label": "Freestanding under-counter fridge", "cell": [21, 21], "bound": [20, 19], "bays": 1, "states": ["standard", "on", "broken"], "top": 1},
    "obj_kettle": {"label": "Stove-kettle counter unit", "cell": [21, 31], "bound": [20, 30], "bays": 1, "states": ["standard", "on", "broken"], "top": 1},
    "obj_toaster": {"label": "Toaster counter unit", "cell": [21, 31], "bound": [20, 30], "bays": 1, "states": ["standard", "on", "broken"], "top": 1},
    "obj_cooker": {"label": "Basic oven · 19-lp body", "cell": [21, 28], "bound": [20, 26], "bays": 1, "states": ["standard", "on", "broken"], "top": 1},
    "obj_mixer": {"label": "Stand-mixer counter unit", "cell": [21, 31], "bound": [20, 30], "bays": 1, "states": ["standard", "on", "broken"], "top": 1},
    "obj_sink": {"label": "Sink counter unit", "cell": [21, 29], "bound": [20, 27], "bays": 1, "states": ["standard", "on", "broken"], "top": 1},
    "obj_table": {"label": "Table for one + player-side chair", "cell": [42, 28], "bound": [40, 26], "bays": 2, "states": ["standard"], "top": 2},
    "obj_petbowl": {"label": "Pet bowl", "cell": [16, 8], "bound": [12, 3], "bays": 0, "states": ["standard", "full", "broken"], "top": 0},
    "obj_cupboard": {"label": "Right-side-wall cleaning cupboard leaf", "cell": [38, 56], "bound": [34, 52], "bays": 0, "states": ["standard", "on", "open"], "top": 0},
}

RUN_COMPONENTS = {
    "obj_fridge": (31, 9, 355, 708),
    "obj_kettle": (380, 9, 701, 708),
    "obj_toaster": (722, 9, 1046, 708),
    "obj_cooker": (1067, 9, 1410, 708),
    "obj_sink": (1771, 9, 2144, 708),
}
SMALL_COMPONENTS = {
    "table": (71, 29, 759, 686),
    "chair": (825, 29, 1179, 686),
    "obj_bin": (1283, 29, 1596, 686),
    "obj_petbowl": (1724, 29, 2098, 686),
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


def source_image(name: str) -> Image.Image:
    return Image.open(GENERATED / name).convert("RGBA")


def component(stem: str) -> Image.Image:
    if stem in RUN_COMPONENTS:
        return crop_alpha(source_image("flat_kitchen_run_sheet.png").crop(RUN_COMPONENTS[stem]))
    if stem == "obj_mixer":
        return crop_alpha(source_image("flat_mixer_unit_source.png"))
    if stem in {"obj_bin", "obj_petbowl"}:
        return crop_alpha(source_image("flat_table_chair_bin_bowl_sheet.png").crop(SMALL_COMPONENTS[stem]))
    raise KeyError(stem)


def fit_component(stem: str) -> Image.Image:
    spec = SPECS[stem]
    cell_w, cell_h = (v * DENSITY for v in spec["cell"])
    bound_w, bound_h = (v * DENSITY for v in spec["bound"])
    src = component(stem)
    # Fill the usable 20-lp width for all one-bay objects. The height is the
    # authoritative contact envelope; this deliberately removes V4's gaps.
    size = (bound_w, bound_h)
    src = hard_alpha(src.resize(size, Image.Resampling.LANCZOS), 112)
    out = rgba((cell_w, cell_h))
    out.alpha_composite(src, ((cell_w - bound_w) // 2, cell_h - bound_h))
    return out


def constrain(im: Image.Image, bound: tuple[int, int]) -> Image.Image:
    bw, bh = bound[0] * DENSITY, bound[1] * DENSITY
    left = (im.width - bw) // 2
    top = im.height - bh
    out = rgba(im.size)
    out.alpha_composite(im.crop((left, top, left + bw, top + bh)), (left, top))
    return out


def table_layers() -> tuple[Image.Image, Image.Image, Image.Image]:
    sheet = source_image("flat_table_chair_bin_bowl_sheet.png")
    table_src = crop_alpha(sheet.crop(SMALL_COMPONENTS["table"]))
    chair_src = crop_alpha(sheet.crop(SMALL_COMPONENTS["chair"]))
    chair = hard_alpha(chair_src.resize((20 * DENSITY, 26 * DENSITY), Image.Resampling.LANCZOS), 112)
    table = hard_alpha(table_src.resize((40 * DENSITY, 19 * DENSITY), Image.Resampling.LANCZOS), 112)
    chair_layer = rgba((42 * DENSITY, 28 * DENSITY))
    table_layer = rgba((42 * DENSITY, 28 * DENSITY))
    floor = 28 * DENSITY
    # The chair is on the player/camera side spatially, centred behind the
    # seated Keeper in draw order. The table/apron is the foreground occluder.
    chair_layer.alpha_composite(chair, (11 * DENSITY, floor - chair.height))
    table_layer.alpha_composite(table, (1 * DENSITY, floor - table.height))
    combined = chair_layer.copy()
    combined.alpha_composite(table_layer)
    return chair_layer, table_layer, combined


def flat_floor(width_px: int) -> Image.Image:
    out = Image.new("RGBA", (width_px, FLOOR_BAND * DENSITY), WOOD)
    d = ImageDraw.Draw(out)
    d.line((0, 0, width_px, 0), fill=INK, width=DENSITY)
    d.line((0, 7, width_px, 7), fill=WOOD_LIGHT, width=2)
    d.line((0, 15, width_px, 15), fill=WOOD_DARK, width=2)
    return out


def flatten_floor(im: Image.Image) -> Image.Image:
    out = im.convert("RGBA")
    out.alpha_composite(flat_floor(out.width), (0, (ROOM_H - FLOOR_BAND) * DENSITY))
    return out


def repeat_frame(variant: int) -> Image.Image:
    src = source_image("flat_room_shell_source.png")
    centres = (900, 1120, 1340)
    cx = centres[variant]
    # Stop at the back-wall/floor junction. Stretch only this wall portion to
    # 51 lp, then append the exact 5-lp floor band; the source's deeper angled
    # floor is intentionally excluded.
    wall = src.crop((cx - 180, 54, cx + 180, 530)).resize((BAY * DENSITY, (ROOM_H-FLOOR_BAND)*DENSITY), Image.Resampling.LANCZOS)
    wall = hard_alpha(ImageEnhance.Contrast(wall).enhance(1.02), 96)
    out = rgba((BAY*DENSITY, ROOM_H*DENSITY)); out.alpha_composite(wall); out.alpha_composite(flat_floor(out.width),(0,wall.height))
    return out


def stair_cap() -> Image.Image:
    src = source_image("flat_room_shell_source.png").crop((100, 54, 650, 530))
    wall = hard_alpha(src.resize((46*DENSITY,(ROOM_H-FLOOR_BAND)*DENSITY),Image.Resampling.LANCZOS),96)
    cap=rgba((46*DENSITY,ROOM_H*DENSITY)); cap.alpha_composite(wall); cap.alpha_composite(flat_floor(cap.width),(0,wall.height))
    return cap


def far_cap(opening: bool = False) -> Image.Image:
    src = source_image("flat_room_shell_source.png").crop((1650, 54, 2074, 530))
    wall = hard_alpha(src.resize((38*DENSITY,(ROOM_H-FLOOR_BAND)*DENSITY),Image.Resampling.LANCZOS),96)
    cap=rgba((38*DENSITY,ROOM_H*DENSITY)); cap.alpha_composite(wall); cap.alpha_composite(flat_floor(cap.width),(0,wall.height))
    d = ImageDraw.Draw(cap)
    # The frame lies on the right side wall. Closed, only the edge/hinge datum
    # is visible. Open, a narrow dark side-wall opening appears behind the leaf.
    x = cap.width - 4 * DENSITY
    if opening:
        d.rectangle((x, 4 * DENSITY, cap.width - DENSITY, 51 * DENSITY), fill=INK)
        d.line((x, 4 * DENSITY, x, 51 * DENSITY), fill=WOOD_LIGHT, width=DENSITY)
    else:
        d.line((cap.width - 2 * DENSITY, 4 * DENSITY, cap.width - 2 * DENSITY, 56 * DENSITY), fill=WOOD_DARK, width=DENSITY)
    return cap


def door_surface() -> Image.Image:
    src = crop_alpha(source_image("flat_cupboard_leaf_source.png"))
    src = src.resize((34 * DENSITY, 52 * DENSITY), Image.Resampling.LANCZOS)
    # A deterministic rectangular alpha slab removes glow, false thickness and
    # any trapezoidal source silhouette. Surface detail and handle remain.
    src.putalpha(Image.new("L", src.size, 255))
    return src


def door_leaf(projected_width_lp: int) -> Image.Image:
    out = rgba((38 * DENSITY, ROOM_H * DENSITY))
    width = max(1, projected_width_lp) * DENSITY
    if projected_width_lp <= 1:
        edge = Image.new("RGBA", (width, 52 * DENSITY), WOOD_DARK)
        ImageDraw.Draw(edge).line((0, 0, 0, edge.height), fill=BRASS, width=1)
        leaf = edge
    else:
        leaf = hard_alpha(door_surface().resize((width, 52 * DENSITY), Image.Resampling.LANCZOS), 64)
        leaf.putalpha(Image.new("L", leaf.size, 255))
    # Hinge is fixed at x=37 lp; projected width grows leftwards.
    out.alpha_composite(leaf, ((37 - projected_width_lp) * DENSITY, 4 * DENSITY))
    return out


def shell(width_lp: int, with_far_cap: bool = True) -> Image.Image:
    out = rgba((width_lp * DENSITY, ROOM_H * DENSITY))
    # The left cap contributes only the 4-lp datum to this revised kitchen.
    # Its full 46-lp source is kept separately for architectural review.
    out.alpha_composite(STAIR.crop((42 * DENSITY, 0, 46 * DENSITY, ROOM_H * DENSITY)), (0, 0))
    for k, x_lp in enumerate(range(DOOR_DATUM, width_lp, BAY)):
        tile = REPEATS[k % 3]
        width = min(BAY, width_lp - x_lp) * DENSITY
        out.alpha_composite(tile.crop((0, 0, width, tile.height)), (x_lp * DENSITY, 0))
    if with_far_cap:
        out.alpha_composite(FAR_CLOSED, (out.width - FAR_CLOSED.width, 0))
    return out


def draw_effect(base: Image.Image, stem: str, state: str, frame: int) -> Image.Image:
    im = base.copy()
    d = ImageDraw.Draw(im)
    q, w, h = DENSITY, im.width, im.height
    if state == "on":
        if stem == "obj_fridge":
            x = 3 * q
            door_w = (3 + frame * 3) * q
            d.rectangle((x, 4*q, x + door_w, h - q), fill=CREAM_LIGHT, outline=INK, width=q)
            d.line((x + door_w, 5*q, x + door_w, h - 2*q), fill=TEAL_LIGHT, width=q)
        elif stem == "obj_kettle":
            for k in range(2):
                y = max(q, (7 - frame - k*3) * q)
                d.ellipse((9*q, y, 13*q, y+4*q), fill=CREAM_LIGHT, outline=INK, width=1)
        elif stem == "obj_toaster":
            y = max(q, (7 - (0,2,5,2)[frame]) * q)
            d.rounded_rectangle((8*q, y, 13*q, y+4*q), radius=q, fill=CREAM_SHADOW, outline=INK, width=q)
        elif stem == "obj_cooker":
            hob_y = h - 19*q
            for x in (6*q, 15*q):
                flame_h = (1,3,2,4)[frame] * q
                d.polygon([(x-2*q,hob_y),(x,hob_y-flame_h),(x+2*q,hob_y)], fill=FLAME, outline=FLAME_LIGHT)
        elif stem == "obj_mixer":
            d.arc((5*q, 3*q, 17*q, 14*q), frame*55, frame*55+170, fill=TEAL_LIGHT, width=q)
        elif stem == "obj_sink":
            d.line((12*q, 4*q, 11*q, (9+frame)*q), fill=WATER, width=q)
    elif state == "broken":
        shifted = rgba(im.size)
        shifted.alpha_composite(im, (((-1,1,-1,1)[frame] * q)//2, 0))
        im, d = shifted, ImageDraw.Draw(shifted)
        for k in range(3):
            x = (8 + ((frame+k*2)%6))*q
            y = max(q, (5-k*2)*q)
            d.ellipse((x-2*q,y-2*q,x+2*q,y+2*q), fill=SMOKE, outline=INK, width=1)
        sx, sy = (4+frame*3)*q, (5+frame%2)*q
        d.line((sx-2*q,sy,sx+2*q,sy), fill=FLAME_LIGHT, width=q)
        d.line((sx,sy-2*q,sx,sy+2*q), fill=FLAME, width=q)
        if stem == "obj_sink": d.ellipse((7*q,h-2*q,(14+frame)*q,h), fill=WATER)
        if stem == "obj_toaster": d.rounded_rectangle(((12+frame)*q,2*q,(17+frame)*q,6*q), radius=q, fill=CREAM_SHADOW, outline=INK, width=q)
        if stem == "obj_fridge": d.line((4*q,h-4*q,(8+frame)*q,h-q), fill=TEAL_LIGHT, width=q)
    return im


def make_strip(frames: list[Image.Image]) -> Image.Image:
    out = rgba((frames[0].width * len(frames), frames[0].height))
    for i, frame in enumerate(frames):
        out.alpha_composite(frame, (i * frame.width, 0))
    return out


def alpha_bounds(frame: Image.Image) -> dict[str, float] | None:
    box = frame.getchannel("A").getbbox()
    if not box: return None
    x0,y0,x1,y1 = box
    return {"xLp": x0/DENSITY, "yLp": y0/DENSITY, "widthLp": (x1-x0)/DENSITY, "heightLp": (y1-y0)/DENSITY}


def save_strip(name: str, frames: list[Image.Image], logical: tuple[int,int], fps: int, meta: dict | None = None) -> dict:
    strip = make_strip(frames)
    png = RAW / f"{name}.png"
    strip.save(png, optimize=True)
    data = {"w":logical[0],"h":logical[1],"frames":len(frames),"fps":fps,"density":DENSITY,"anchor":[logical[0]/2,logical[1]],"z":40,"projection":{"id":PROJECTION,"runtimeDepthScaling":False}}
    if meta: data.update(meta)
    png.with_suffix(".json").write_text(json.dumps(data, indent=2)+"\n")
    urls=[]
    for i,frame in enumerate(frames):
        fn=f"{name}_frame{i+1}.png"; frame.save(ASSETS/fn,optimize=True)
        urls.append(f"/keeper-review/kitchen-basic-assets-v5/assets/{fn}")
    return {"png":png.relative_to(ROOT).as_posix(),"meta":data,"urls":urls,"bounds":[alpha_bounds(f) for f in frames]}


def load_keeper(stem: str) -> list[str]:
    candidates=list((ROOT/"art/raw/keeper-first-batch").glob(f"{stem}_f*.png"))
    if len(candidates)!=1: raise ValueError(f"expected one Keeper source for {stem}, found {len(candidates)}")
    png=candidates[0]; meta=json.loads(png.with_suffix(".json").read_text()); strip=Image.open(png).convert("RGBA")
    fw,fh=meta["w"]*meta["density"],meta["h"]*meta["density"]
    urls=[]
    for i in range(meta["frames"]):
        frame=strip.crop((i*fw,0,(i+1)*fw,fh)); fn=f"{stem}_frame{i+1}.png"; frame.save(ASSETS/fn,optimize=True)
        urls.append(f"/keeper-review/kitchen-basic-assets-v5/assets/{fn}")
    return urls


def room_composite(width_lp: int, outline: bool = False) -> Image.Image:
    out=shell(width_lp)
    if outline:
        d=ImageDraw.Draw(out)
        reservations=[(1,1,"BIN"),(2,2,"FRIDGE T3"),(4,1,"KETTLE"),(5,1,"TOASTER"),(6,2,"RANGE T3"),(8,1,"MIXER"),(9,2,"SINK + DW"),(11,1,"SNACK"),(12,1,"DUMB WAITER")]
        for bay,span,_ in reservations:
            x0=(DOOR_DATUM+(bay-1)*BAY+1)*DENSITY; x1=(DOOR_DATUM+(bay-1+span)*BAY-1)*DENSITY
            d.rectangle((x0,15*DENSITY,x1,55*DENSITY),outline=TEAL,width=DENSITY)
        return out
    for stem,bay in zip(("obj_bin","obj_fridge","obj_kettle","obj_toaster","obj_cooker","obj_mixer","obj_sink","obj_table"),(1,2,3,4,5,6,7,8)):
        frame=STANDARD[stem]; span=SPECS[stem]["bays"]
        x=(DOOR_DATUM+(bay-1)*BAY)*DENSITY+(span*BAY*DENSITY-frame.width)//2
        out.alpha_composite(frame,(x,ROOM_H*DENSITY-frame.height))
    bowl=STANDARD["obj_petbowl"]
    # Foreground child of the table: cell x=172..188 lp, interaction at 180 lp.
    out.alpha_composite(bowl,(172*DENSITY,ROOM_H*DENSITY-bowl.height))
    return out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_review(catalogue: dict, keeper: dict[str,list[str]]) -> None:
    data={
        "assets":catalogue["assets"], "keeper":keeper,
        "shells":{str(n):f"/keeper-review/kitchen-basic-assets-v5/assets/room_kitchen_shell_{n}bay_frame1.png" for n in range(6,13)},
        "room9":"/keeper-review/kitchen-basic-assets-v5/assets/room_kitchen_9bay_composite.png",
        "room12":"/keeper-review/kitchen-basic-assets-v5/assets/room_kitchen_12bay_outline.png",
        "repeat":"/keeper-review/kitchen-basic-assets-v5/assets/room_kitchen_repeat_a_frame1.png",
        "stairCap":"/keeper-review/kitchen-basic-assets-v5/assets/room_kitchen_stair_cap_frame1.png",
        "farClosed":"/keeper-review/kitchen-basic-assets-v5/assets/room_kitchen_far_cap_closed_frame1.png",
        "farOpen":"/keeper-review/kitchen-basic-assets-v5/assets/room_kitchen_far_cap_open_frame1.png",
        "chair":"/keeper-review/kitchen-basic-assets-v5/assets/obj_table_chair_back_f1_frame1.png",
        "table":"/keeper-review/kitchen-basic-assets-v5/assets/obj_table_foreground_f1_frame1.png",
        "leafClosed":"/keeper-review/kitchen-basic-assets-v5/assets/obj_cupboard_standard_f1_frame1.png",
        "leafOpening":catalogue["assets"]["obj_cupboard"]["states"]["on"]["urls"],
        "leafOpen":"/keeper-review/kitchen-basic-assets-v5/assets/obj_cupboard_open_f1_frame1.png",
        "references":[
            "/keeper-review/kitchen-basic-assets-v5/assets/approved_flat_room_mockup.png",
        ],
    }
    for ref in (SOURCE/"reference").glob("*"):
        if ref.suffix.lower() in {".png",".jpg",".jpeg",".webp"}:
            shutil.copy2(ref,ASSETS/ref.name)

    html=r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Basic Assets V5 · flat cutaway review</title><style>
:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#0a1c25;--line:#365663;--ink:#f7f1dd;--muted:#a8bdc4;--gold:#efb64d;--cyan:#58d4df;--red:#ff786d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1480px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}h1{margin:.1em 0}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin-right:7px}.notice,.finding{border-left:4px solid var(--gold);background:#2a2518;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;min-width:0}.well{min-height:220px;display:flex;align-items:end;justify-content:center;overflow:auto;background:repeating-conic-gradient(#162b35 0 25%,#10232d 0 50%) 0/20px 20px;border-radius:8px;padding:12px}.well img{image-rendering:auto;flex:none}.controls{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:9px 0}button,select{background:#17323e;color:var(--ink);border:1px solid #5f7a84;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.small{font-size:.85rem;color:var(--muted)}code{color:#9ce5ea}.scroll{overflow:auto;background:#071923;border-radius:10px;padding:10px}.room{position:relative;height:224px;flex:none}.room>img.base{position:absolute;inset:0;height:224px;width:auto}.keeper{position:absolute;z-index:50;image-rendering:auto}.pin{position:absolute;z-index:95;width:7px;height:7px;background:var(--red);border:1px solid white;border-radius:50%;bottom:0;transform:translateX(-50%)}.guides{position:absolute;inset:0;pointer-events:none;z-index:90}.guides i{position:absolute;left:0;right:0;border-top:1px dashed}.guides .floor{bottom:0;border-color:#fff}.guides .work{bottom:76px;border-color:var(--gold)}.guides .seat{bottom:44px;border-color:var(--cyan)}.front-grid{position:absolute;inset:0;z-index:91;pointer-events:none;background:repeating-linear-gradient(90deg,transparent 0 83px,rgba(88,212,223,.45) 83px 84px)}.proof{height:224px;position:relative;background:#071923;overflow:hidden}.proof img{position:absolute}.proof .shell{inset:0;height:224px;width:auto}.proof .same{bottom:0;width:84px;height:auto;z-index:40}.asset-scale{display:flex;align-items:end;gap:8px;min-height:180px;overflow:auto}.asset-scale img{flex:none}.asset-scale .k{width:128px;height:160px;object-fit:contain}.layer-stage{width:168px;height:224px;position:relative;background:repeating-conic-gradient(#172933 0 25%,#10232d 0 50%) 0/20px 20px;margin:auto;overflow:hidden}.layer-stage img{position:absolute;left:0;bottom:0;width:168px;height:112px;object-fit:contain}.layer-stage .sit{z-index:50;width:136px;height:160px;left:16px;bottom:0;object-fit:contain}.layer-stage .chair{z-index:35}.layer-stage .table{z-index:60}.layer-stage .bowl{z-index:70;width:64px;height:32px;left:98px}.datum{position:absolute;left:0;right:0;border-top:1px dashed;z-index:95;font-size:10px}.datum span{background:#071923;padding:1px 3px}.datum.work{bottom:76px;border-color:var(--gold)}.datum.seat{bottom:44px;border-color:var(--cyan)}.door-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(205px,1fr));gap:10px}.door-stage{position:relative;width:230px;height:224px;margin:auto;background:#071923;overflow:hidden}.door-stage .cap{position:absolute;right:0;top:0;width:152px;height:224px;z-index:20}.door-stage .person{position:absolute;width:136px;height:164px;bottom:0;z-index:50;object-fit:contain}.door-stage .leaf{position:absolute;right:0;top:0;width:152px;height:224px;z-index:80}.door-stage .outside{z-index:90}.oven-stage{position:relative;width:210px;height:224px;margin:auto;background:#071923}.oven-stage .oven{position:absolute;width:84px;height:112px;left:63px;bottom:0;object-fit:contain}.oven-stage .actor{position:absolute;width:136px;height:164px;left:37px;bottom:0;object-fit:contain}.parallel{position:relative}.parallel:after{content:"true front elevation · parallel edges";position:absolute;top:8px;left:12px;color:#08202a;background:var(--cyan);padding:3px 7px;font-size:.75rem}.parallel .plines{position:absolute;inset:10px;z-index:99;pointer-events:none;border-left:2px solid var(--cyan);border-right:2px solid var(--cyan)}.parallel .plines:before,.parallel .plines:after{content:"";position:absolute;left:0;right:0;border-top:2px solid var(--cyan)}.parallel .plines:before{top:20%}.parallel .plines:after{bottom:9%}table{border-collapse:collapse;width:100%}th,td{text-align:left;border-bottom:1px solid var(--line);padding:7px;vertical-align:top}@media(max-width:700px){header,main{padding:12px}.door-stage{width:190px}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">flat-cutaway-v1</span><h1>Kitchen basic assets V5</h1><p>Review-only redraft. V1–V4 and the live game remain untouched.</p><p id="loading" class="notice">Preloading and decoding every unique review image… controls remain locked.</p></header><main>
<section class="panel"><h2>What changed</h2><p>Functional fronts are now orthographic rectangles. Cabinet sides do not taper, top cues are limited to 0–2 lp (table 2 lp), the visible floor is exactly 5 lp, and the same raster stays the same size in every bay. The fridge is visibly freestanding. The cupboard frame lives on the right side wall: its closed leaf is edge-on; its open leaf is a full opaque rectangle hinged on the right and extending left.</p><p class="finding"><strong>Animation record:</strong> <code>keeper_sit_back</code> confirms a 10.67-lp seat contact for the 11-lp chair. <code>keeper_lean_table_back</code> is a standing rear-facing reach, not a seated loop. V5 changes no Keeper animation; a future generic seated arm overlay remains the only table-animation gap.</p></section>
<section class="panel"><h2>Authoring reference</h2><div class="grid"><div class="card"><h3>Accepted flat room direction</h3><div class="scroll"><img id="ref0" alt="Frank-approved flat room direction" style="height:224px;width:auto"></div></div><div class="card"><h3>V5 shell projection proof</h3><div class="scroll parallel"><div class="plines"></div><img id="projectionRoom" alt="V5 room with parallel guide" style="height:224px;width:auto"></div></div></div></section>
<section class="panel"><h2>Every asset and state · 4× authoring scale</h2><p>These are the native density-4 frames. Use Previous/Next or Play after preload completes.</p><div id="assetGrid" class="grid"></div></section>
<section class="panel"><h2>Modular room shell · 6–12 bays</h2><div class="controls"><label>Assembly <select id="shellSelect" disabled></select></label></div><div class="scroll"><img id="shellImage" alt="Selected modular shell" style="height:224px;width:auto"></div><div class="grid"><div class="card"><h3>Stair-side cap</h3><div class="scroll"><img id="stairCap" style="height:224px;width:auto" alt="Stair-side cap"></div><p class="small">46×56-lp source; 4-lp contribution in the revised kitchen assembly.</p></div><div class="card"><h3>Repeat section</h3><div class="scroll"><img id="repeat" style="height:224px;width:auto" alt="21 by 56 repeat"></div></div><div class="card"><h3>Far-wall / side-wall cap</h3><div class="scroll"><img id="farCap" style="height:224px;width:auto" alt="Far cap with edge-on closed door"></div><p class="small">Door frame is on the right side wall; no frontal cupboard is baked into the back wall.</p></div></div></section>
<section class="panel"><h2>9-bay starting kitchen · 193 × 56 lp</h2><p>Furniture fills 20 of each 21-lp bay, giving a transparent half-lp safety gutter per side without angled gaps. The cupboard is fixed to the far cap and always last.</p><div class="controls"><button id="spotPrev" disabled>Previous spot</button><select id="spotSelect" disabled></select><button id="spotNext" disabled>Next spot</button><label><input id="datumToggle" type="checkbox" disabled> show 19/11-lp datums</label></div><div class="scroll"><div id="room9" class="room" style="width:772px"><img class="base" id="room9base" alt="Nine bay starting kitchen"><img class="keeper" id="room9keeper" alt="Keeper at selected interaction"><i class="pin"></i><div class="guides" hidden><i class="floor"></i><i class="work"></i><i class="seat"></i></div></div></div></section>
<section class="panel"><h2>Same raster in three bays · no depth scaling</h2><p>All three kettle units use the same URL and the same 84-pixel cell width.</p><div class="scroll"><div id="sameProof" class="proof" style="width:772px"><img class="shell" id="sameShell" alt="Room shell"><img class="same" data-bay="2"><img class="same" data-bay="5"><img class="same" data-bay="8"></div></div></section>
<section class="panel"><h2>Front face versus shallow cue</h2><div class="controls"><label><input id="cueToggle" type="checkbox" checked disabled> show 1-lp shallow top cue</label></div><div class="grid" id="cueGrid"></div><p class="small">The toggle hides only the highlighted guide overlay; the source art is unchanged. Blue = functional front rectangle. Gold = allowed shallow top cue. No side face appears between neighbouring units.</p></section>
<section class="panel"><h2>Keeper scale beside every major asset</h2><p>The same unscaled <code>keeper_walk</code> frame is reused beside each object.</p><div id="scaleGrid" class="grid"></div></section>
<section class="panel"><h2>Table for one · chair on the player side</h2><div class="grid"><div class="card"><h3>Required draw stack</h3><div class="layer-stage"><img class="chair" id="chairLayer" alt="Chair background layer"><img class="sit" id="sitKeeper" alt="Approved rear sit final pose"><img class="table" id="tableLayer" alt="Table foreground layer"><img class="bowl" id="tableBowl" alt="Pet bowl foreground"><div class="datum work"><span>table 19 lp</span></div><div class="datum seat"><span>seat 11 lp</span></div></div></div><div><p>The chair is nearest the player/camera in floor placement. The Keeper sits facing away from camera, with the table in front of him. In draw order the chair is behind him, the Keeper is central, and the table apron is foreground, so his legs and boots read as underneath the table rather than pasted in front.</p><p><strong>Measured contacts:</strong> seat 11 lp; table top 19 lp; underside 17 lp; 2-lp top; 15-lp minimum knee clearance retained.</p><p class="finding"><strong>Review finding:</strong> the rear sit pose fits naturally and keeps his boots on the floor. No existing approved clip supplies a seated rear-facing generic arm loop, so V5 does not pretend that <code>lean_table_back</code> is seated.</p></div></div></section>
<section class="panel"><h2>Right-side-wall cupboard · full lifecycle</h2><p>The right hinge never moves. The leaf projects from 1→8→22→34 lp as it physically rotates, with constant 52-lp height. It is never a trapezoid. At full opening it extends left in front of the Keeper and remains open through the activity and return.</p><div id="doorGrid" class="door-grid"></div><p class="finding"><strong>V5 answer:</strong> yes—the 34×52-lp fully open rectangle hides the 19-lp rear Keeper core, boots, broom and basic-hoover swap route. The activity itself occurs left of the leaf; he returns behind it to put the tool away, exits in the standard walk, and the leaf closes only after he is clear.</p></section>
<section class="panel"><h2>19-lp oven door · existing clips unchanged</h2><div class="grid"><div class="card"><h3>Cake retrieval</h3><div class="oven-stage"><img class="oven" id="ovenCake"><img class="actor" id="cakeKeeper"></div></div><div class="card"><h3>Meal retrieval</h3><div class="oven-stage"><img class="oven" id="ovenMeal"><img class="actor" id="mealKeeper"></div></div><p class="finding"><strong>V5 answer:</strong> both existing rear retrieval clips still read with the cooker constrained to a 19-lp body and 19-lp oven-door width. The accepted cake action remains especially clear; no wider oven workaround is needed.</p></div></section>
<section class="panel"><h2>12-bay outline · 256 × 56 lp</h2><p>Every reservation is a whole 21-lp bay. The repeat module is not stretched; the side-wall cupboard remains fixed at the far right and takes no bay.</p><div class="scroll"><img id="room12" alt="Twelve bay reservation outline" style="height:224px;width:auto"></div></section>
<section class="panel"><h2>Measured V5 hand-back</h2><table><thead><tr><th>Item</th><th>Largest measured alpha bound</th><th>Bays</th><th>Interaction spot</th><th>Projection</th></tr></thead><tbody id="measureRows"></tbody></table><p class="small">Draft only. V1–V4 and runtime assets remain immutable; rejection is reversible by discarding V5 directories alone.</p></section>
</main><script>
const DATA=__DATA__;const urls=[];const collect=v=>{if(typeof v==='string'&&(v.includes('/assets/')||v.includes('/objects/')))urls.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const uniq=[...new Set(urls)];
const image=(src,alt,cls='')=>{const i=new Image;i.src=src;i.alt=alt;i.className=cls;return i};
const stateUrls=(stem,state)=>DATA.assets[stem].states[state].urls;
function setupAssets(){const grid=document.getElementById('assetGrid');Object.entries(DATA.assets).forEach(([stem,a])=>{const states=Object.keys(a.states),flat=[];states.forEach(s=>a.states[s].urls.forEach((u,n)=>flat.push({u,s,n,count:a.states[s].urls.length})));const card=document.createElement('article');card.className='card';card.innerHTML=`<h3>${a.label}</h3><div class="well"></div><div class="controls"><button>Previous</button><button>Play</button><button>Next</button><span class="small"></span></div><p class="small">cell ${a.cell.join('×')} lp · ${a.bays} bay(s) · top cue ${a.topRevealLp} lp</p>`;let n=0,t=null;const well=card.querySelector('.well'),buttons=card.querySelectorAll('button'),read=card.querySelector('span');const show=()=>{const f=flat[n];well.replaceChildren(image(f.u,`${a.label} ${f.s} frame ${f.n+1}`));read.textContent=`${f.s} · ${f.n+1}/${f.count}`};buttons[0].onclick=()=>{clearInterval(t);t=null;n=(n-1+flat.length)%flat.length;show()};buttons[2].onclick=()=>{clearInterval(t);t=null;n=(n+1)%flat.length;show()};buttons[1].onclick=()=>{if(t){clearInterval(t);t=null;buttons[1].textContent='Play'}else{t=setInterval(()=>{n=(n+1)%flat.length;show()},125);buttons[1].textContent='Pause'}};show();grid.append(card)})}
function setupShell(){const sel=document.getElementById('shellSelect');Object.keys(DATA.shells).forEach(n=>sel.add(new Option(`${n} bays · ${4+21*Number(n)} lp`,n)));sel.value='9';const show=()=>document.getElementById('shellImage').src=DATA.shells[sel.value];sel.onchange=show;show();document.getElementById('stairCap').src=DATA.stairCap;document.getElementById('repeat').src=DATA.repeat;document.getElementById('farCap').src=DATA.farClosed;document.getElementById('projectionRoom').src=DATA.shells['9']}
const spots=[['Bin',14.5],['Fridge',35.5],['Kettle',56.5],['Toaster',77.5],['Oven',98.5],['Mixer',119.5],['Sink',140.5],['Table/chair',161.5],['Pet bowl',180],['Cupboard handle',189]];
function setupRoom(){document.getElementById('room9base').src=DATA.room9;const sel=document.getElementById('spotSelect'),keeper=document.getElementById('room9keeper'),pin=document.querySelector('#room9 .pin');spots.forEach((s,i)=>sel.add(new Option(`${s[0]} · ${Math.round(s[1]*8)} ku`,i)));const show=()=>{const [name,x]=spots[Number(sel.value||0)];keeper.src=DATA.keeper.keeper_walk[0];keeper.style.width='128px';keeper.style.height='160px';keeper.style.left=`${x*4-64}px`;keeper.style.bottom='0';pin.style.left=`${x*4}px`;keeper.alt=`Keeper at ${name}`};sel.onchange=show;document.getElementById('spotPrev').onclick=()=>{sel.value=(Number(sel.value)-1+spots.length)%spots.length;show()};document.getElementById('spotNext').onclick=()=>{sel.value=(Number(sel.value)+1)%spots.length;show()};document.getElementById('datumToggle').onchange=e=>document.querySelector('#room9 .guides').hidden=!e.target.checked;show()}
function setupSame(){document.getElementById('sameShell').src=DATA.shells['9'];document.querySelectorAll('#sameProof .same').forEach(i=>{i.src=stateUrls('obj_kettle','standard')[0];i.style.left=`${(4+(Number(i.dataset.bay)-1)*21)*4}px`})}
function setupCue(){const grid=document.getElementById('cueGrid');for(const stem of ['obj_fridge','obj_kettle','obj_toaster','obj_cooker','obj_mixer','obj_sink']){const a=DATA.assets[stem],card=document.createElement('div');card.className='card';card.innerHTML=`<h3>${a.label}</h3><div class="well" style="position:relative"><img src="${stateUrls(stem,'standard')[0]}" alt="${a.label}"><i class="frontbox" style="position:absolute;border:2px solid var(--cyan);width:${a.frontRectLp.width*4}px;height:${a.frontRectLp.height*4}px;bottom:12px;left:50%;transform:translateX(-50%)"></i><i class="topcue" style="position:absolute;background:rgba(239,182,77,.45);width:${a.frontRectLp.width*4}px;height:${a.topRevealLp*4}px;bottom:${12+a.frontRectLp.height*4}px;left:50%;transform:translateX(-50%)"></i></div>`;grid.append(card)}document.getElementById('cueToggle').onchange=e=>document.querySelectorAll('.topcue').forEach(x=>x.hidden=!e.target.checked)}
function setupScale(){const grid=document.getElementById('scaleGrid');for(const stem of ['obj_bin','obj_fridge','obj_kettle','obj_toaster','obj_cooker','obj_mixer','obj_sink','obj_table','obj_petbowl']){const a=DATA.assets[stem],card=document.createElement('div');card.className='card';card.innerHTML=`<h3>${a.label}</h3><div class="asset-scale"><img src="${stateUrls(stem,'standard')[0]}" alt="${a.label}"><img class="k" src="${DATA.keeper.keeper_walk[0]}" alt="Same unscaled Keeper"></div>`;grid.append(card)}}
function setupTable(){document.getElementById('chairLayer').src=DATA.chair;document.getElementById('tableLayer').src=DATA.table;document.getElementById('sitKeeper').src=DATA.keeper.keeper_sit_back.at(-1);document.getElementById('tableBowl').src=stateUrls('obj_petbowl','standard')[0]}
function setupDoor(){const defs=[['1 · Closed: edge-on',DATA.farClosed,DATA.leafClosed,'keeper_walk',0,8,false],['2 · Opens from fixed right hinge',DATA.farOpen,DATA.leafOpening[2],'keeper_walk',1,58,false],['3 · Walk behind full leaf',DATA.farOpen,DATA.leafOpen,'keeper_walk_into_lift',1,78,false],['4 · Emerge sweeping; stays open',DATA.farOpen,DATA.leafOpen,'keeper_sweep_broom',0,0,true],['5 · Return tool behind leaf',DATA.farOpen,DATA.leafOpen,'keeper_sweep_broom',4,76,false],['6 · Standard-walk exit',DATA.farOpen,DATA.leafOpen,'keeper_walk',1,0,true],['7 · Auto-close once clear',DATA.farClosed,DATA.leafClosed,'keeper_walk',1,-95,true]],grid=document.getElementById('doorGrid');for(const [label,cap,leaf,clip,frame,left,outside] of defs){const card=document.createElement('div');card.className='card';card.innerHTML=`<h3>${label}</h3><div class="door-stage"><img class="cap"><img class="person ${outside?'outside':''}"><img class="leaf"></div>`;card.querySelector('.cap').src=cap;const p=card.querySelector('.person');p.src=DATA.keeper[clip][frame];p.style.left=`${left}px`;card.querySelector('.leaf').src=leaf;grid.append(card)}}
function setupOven(){const oven=stateUrls('obj_cooker','standard')[0];document.getElementById('ovenCake').src=oven;document.getElementById('ovenMeal').src=oven;document.getElementById('cakeKeeper').src=DATA.keeper.keeper_cake_from_oven_back[3];document.getElementById('mealKeeper').src=DATA.keeper.keeper_meal_from_oven_back[3];document.getElementById('room12').src=DATA.room12}
function setupTableRows(){const body=document.getElementById('measureRows');Object.values(DATA.assets).forEach(a=>{const r=document.createElement('tr');r.innerHTML=`<td>${a.label}</td><td>${a.largestBound.widthLp} × ${a.largestBound.heightLp} lp</td><td>${a.bays}</td><td>${a.interactionSpotKu} ku</td><td>${a.projection.id}; runtime scaling ${a.projection.runtimeDepthScaling}</td>`;body.append(r)})}
function setup(){document.querySelectorAll('button,select,input').forEach(x=>x.disabled=false);document.getElementById('ref0').src=DATA.references[0];setupAssets();setupShell();setupRoom();setupSame();setupCue();setupScale();setupTable();setupDoor();setupOven();setupTableRows();document.getElementById('loading').textContent=`All ${uniq.length} unique review images loaded and decoded. Controls enabled.`}
Promise.all(uniq.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,()=>bad(new Error(`decode ${src}`))):ok();i.onerror=()=>bad(new Error(`load ${src}`));i.src=src}))).then(setup).catch(e=>{document.getElementById('loading').textContent=`Media failed to load: ${e.message}`});
</script></body></html>'''
    html=html.replace("grid-template-columns:repeat(auto-fit,minmax(205px,1fr));gap:10px}.door-stage{position:relative;width:230px", "grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:10px}.door-stage{position:relative;width:300px")
    html=html.replace("@media(max-width:700px){header,main{padding:12px}.door-stage{width:190px}", "@media(max-width:700px){header,main{padding:12px}.door-grid{grid-template-columns:1fr}.door-stage{width:300px}")
    html=html.replace("'keeper_walk',0,8,false],['2 · Opens from fixed right hinge',DATA.farOpen,DATA.leafOpening[2],'keeper_walk',1,58,false],['3 · Walk behind full leaf',DATA.farOpen,DATA.leafOpen,'keeper_walk_into_lift',1,78,false],['4 · Emerge sweeping; stays open',DATA.farOpen,DATA.leafOpen,'keeper_sweep_broom',0,0,true],['5 · Return tool behind leaf',DATA.farOpen,DATA.leafOpen,'keeper_sweep_broom',4,76,false],['6 · Standard-walk exit',DATA.farOpen,DATA.leafOpen,'keeper_walk',1,0,true],['7 · Auto-close once clear',DATA.farClosed,DATA.leafClosed,'keeper_walk',1,-95,true]", "'keeper_walk',0,76,false],['2 · Opens from fixed right hinge',DATA.farOpen,DATA.leafOpening[2],'keeper_walk',1,128,false],['3 · Walk behind full leaf',DATA.farOpen,DATA.leafOpen,'keeper_walk_into_lift',1,174,false],['4 · Emerge sweeping; stays open',DATA.farOpen,DATA.leafOpen,'keeper_sweep_broom',0,10,true],['5 · Return tool behind leaf',DATA.farOpen,DATA.leafOpen,'keeper_sweep_broom',4,172,false],['6 · Standard-walk exit',DATA.farOpen,DATA.leafOpen,'keeper_walk',1,10,true],['7 · Auto-close once clear',DATA.farClosed,DATA.leafClosed,'keeper_walk',1,-105,true]")
    (PUBLIC/"index.html").write_text(html.replace("__DATA__",json.dumps(data,separators=(",",":"))))
    (DRAFT/"review-data.json").write_text(json.dumps(data,indent=2)+"\n")


def main() -> None:
    for folder in (RAW,DRAFT,ASSETS):
        folder.mkdir(parents=True,exist_ok=True)
        for p in folder.iterdir():
            if p.is_file(): p.unlink()

    global REPEATS, STAIR, FAR_CLOSED, FAR_OPEN, STANDARD
    REPEATS=[repeat_frame(i) for i in range(3)]
    STAIR=stair_cap(); FAR_CLOSED=far_cap(False); FAR_OPEN=far_cap(True)
    chair_layer,table_layer,table_combined=table_layers()
    STANDARD={stem:fit_component(stem) for stem in ("obj_bin","obj_fridge","obj_kettle","obj_toaster","obj_cooker","obj_mixer","obj_sink","obj_petbowl")}
    STANDARD["obj_table"]=table_combined
    leaf_closed=door_leaf(1); leaf_open=door_leaf(34)

    catalogue={"version":5,"status":"reversible-draft","density":DENSITY,"projection":{"id":PROJECTION,"runtimeDepthScaling":False,"camera":"straight-on","vanishingPoint":False},"room":{"doorDatumLp":DOOR_DATUM,"bayLp":BAY,"heightLp":ROOM_H,"floorBandLp":FLOOR_BAND,"footLineLp":FOOT_Y,"widthsLp":{"9":ROOM_9_W,"12":ROOM_12_W}},"assets":{}}
    spots={"obj_bin":116,"obj_fridge":284,"obj_kettle":452,"obj_toaster":620,"obj_cooker":788,"obj_mixer":956,"obj_sink":1124,"obj_table":1292,"obj_petbowl":1440,"obj_cupboard":1512}
    for stem,spec in SPECS.items():
        front_w=40 if stem=="obj_table" else (34 if stem=="obj_cupboard" else (12 if stem=="obj_petbowl" else 20))
        front_h=19 if stem in {"obj_fridge","obj_kettle","obj_toaster","obj_cooker","obj_mixer","obj_sink","obj_table"} else spec["bound"][1]
        entry={"label":spec["label"],"cell":spec["cell"],"bays":spec["bays"],"interactionSpotKu":spots[stem],"topRevealLp":spec["top"],"frontRectLp":{"width":front_w,"height":front_h},"projection":{"id":PROJECTION,"frontFace":"true-rectangle","rearEdgeScale":1,"runtimeDepthScaling":False},"states":{}}
        for state in spec["states"]:
            if stem=="obj_cupboard":
                if state=="standard": frames=[leaf_closed]; widths=[1]
                elif state=="on": widths=[1,8,22,34]; frames=[door_leaf(w) for w in widths]
                else: widths=[34]; frames=[leaf_open]
                extra={"projectedWidthLp":widths,"realLeafSizeLp":[34,52],"hingeXLp":37,"hingeSide":"right","opens":"left","layerRole":"foreground-occluder"}
            elif stem=="obj_bin":
                frames=[STANDARD[stem].copy()]; d=ImageDraw.Draw(frames[0])
                if state in {"full","overflowing"}: d.polygon([(5*DENSITY,3*DENSITY),(9*DENSITY,DENSITY),(15*DENSITY,4*DENSITY)],fill=CREAM_SHADOW,outline=INK)
                if state=="overflowing": d.ellipse((2*DENSITY,12*DENSITY,7*DENSITY,15*DENSITY),fill=CREAM_LIGHT,outline=INK,width=DENSITY)
                extra={}
            elif stem=="obj_petbowl":
                frames=[STANDARD[stem].copy()] if state!="broken" else [STANDARD[stem].copy() for _ in range(4)]
                for i,fr in enumerate(frames):
                    d=ImageDraw.Draw(fr)
                    if state=="full": d.ellipse((4*DENSITY,5*DENSITY,12*DENSITY,7*DENSITY),fill=WOOD_DARK)
                    if state=="broken":
                        d.line((8*DENSITY,5*DENSITY,7*DENSITY,8*DENSITY),fill="#bd3d34",width=DENSITY)
                        d.ellipse((max(1,3-i)*DENSITY,7*DENSITY,min(15,13+i)*DENSITY,8*DENSITY),fill=WATER)
                extra={}
            elif state=="standard": frames=[STANDARD[stem]]; extra={}
            else: frames=[draw_effect(STANDARD[stem],stem,state,i) for i in range(4)]; extra={}
            if stem!="obj_cupboard": frames=[constrain(f,tuple(spec["bound"])) for f in frames]
            saved=save_strip(f"{stem}_{state}_f{len(frames)}",frames,tuple(spec["cell"]),8 if len(frames)>1 else 0,{"interactionSpotKu":spots[stem],"contactDatumsLp":{"foot":0,"worktopOrTable":19 if stem in {"obj_fridge","obj_kettle","obj_toaster","obj_cooker","obj_mixer","obj_sink","obj_table"} else None,"seat":11 if stem=="obj_table" else None},**extra})
            entry["states"][state]=saved
        bounds=[b for state in entry["states"].values() for b in state["bounds"] if b]
        entry["largestBound"]={"widthLp":max(round(b["widthLp"],2) for b in bounds),"heightLp":max(round(b["heightLp"],2) for b in bounds)}
        catalogue["assets"][stem]=entry

    for level in range(1,4):
        fr=rgba((21*DENSITY,29*DENSITY)); d=ImageDraw.Draw(fr)
        for i in range(level*2):
            y=(12-i*2)*DENSITY; d.ellipse((5*DENSITY,y,16*DENSITY,y+2*DENSITY),fill=CREAM_LIGHT,outline=INK,width=2)
        save_strip(f"obj_sink_dishes{level}_f1",[fr],(21,29),0,{"layerRole":"dirty-dishes-overlay"})

    for i,tile in enumerate(REPEATS): save_strip(f"room_kitchen_repeat_{'abc'[i]}",[tile],(21,56),0,{"z":10,"moduleContributionLp":21,"floorBandLp":5})
    save_strip("room_kitchen_stair_cap",[STAIR],(46,56),0,{"z":15,"moduleContributionLp":4,"floorBandLp":5})
    save_strip("room_kitchen_far_cap_closed",[FAR_CLOSED],(38,56),0,{"z":20,"moduleContributionLp":0,"doorView":"edge-on-right-side-wall"})
    save_strip("room_kitchen_far_cap_open",[FAR_OPEN],(38,56),0,{"z":20,"moduleContributionLp":0,"doorView":"open-right-side-wall"})
    save_strip("obj_table_chair_back_f1",[chair_layer],(42,28),0,{"z":35,"layerRole":"background-chair","seatContactLp":11})
    save_strip("obj_table_foreground_f1",[table_layer],(42,28),0,{"z":60,"layerRole":"foreground-table-apron","tableContactLp":19})
    for n in range(6,13): save_strip(f"room_kitchen_shell_{n}bay",[shell(DOOR_DATUM+n*BAY)],(DOOR_DATUM+n*BAY,56),0,{"z":10,"floorBandLp":5,"repeatCount":n})
    room9=room_composite(ROOM_9_W); room12=room_composite(ROOM_12_W,True)
    for name,im in (("room_kitchen_9bay_composite",room9),("room_kitchen_12bay_outline",room12)):
        im.save(RAW/f"{name}.png",optimize=True); im.save(ASSETS/f"{name}.png",optimize=True)

    keeper={stem:load_keeper(stem) for stem in ("keeper_walk","keeper_walk_into_lift","keeper_sweep_broom","keeper_hoover_basic","keeper_sit_back","keeper_lean_table_back","keeper_cake_from_oven_back","keeper_meal_from_oven_back")}
    (DRAFT/"asset-catalogue.json").write_text(json.dumps(catalogue,indent=2)+"\n")
    write_review(catalogue,keeper)
    inputs=sorted(GENERATED.glob("*.png"))+sorted((SOURCE/"reference").glob("*"))
    outputs=sorted(RAW.glob("*"))+sorted(DRAFT.glob("*.json"))+[PUBLIC/"index.html"]
    register={"version":5,"status":"reversible-draft","supersedesForReviewOnly":"kitchen-basic-assets-v4","projection":{"id":PROJECTION,"runtimeDepthScaling":False,"frontFace":"true-rectangle","floorBandLp":5,"rearEdgeScale":1},"geometryChanges":{"oneBayArtWidthLp":20,"safetyGutterLpEachSide":0.5,"worktopHobTableLp":19,"chairSeatLp":11,"confirmedRearSeatContactLp":10.67,"tableLayering":"player-side chair behind Keeper; table/apron foreground","cupboardView":"right-side wall; closed leaf edge-on","cupboardLeafRealSizeLp":[34,52],"cupboardProjectedWidthsLp":[1,8,22,34],"cupboardHinge":"fixed right; opens left","doorRemainsOpenDuringActivity":True,"doorClosesAfterStandardWalkExitClear":True,"broomTurnClipRequired":False,"genericSeatedBackArmClipAvailable":False},"inputs":[{"path":p.relative_to(ROOT).as_posix(),"sha256":sha(p)} for p in inputs if p.is_file()],"outputs":[{"path":p.relative_to(ROOT).as_posix(),"sha256":sha(p)} for p in outputs if p.is_file()]}
    (DRAFT/"batch-register.json").write_text(json.dumps(register,indent=2)+"\n")
    print(json.dumps({"assets":len(catalogue["assets"]),"projection":PROJECTION,"roomWidths":[193,256],"floorBandLp":5,"review":PUBLIC.relative_to(ROOT).as_posix()},indent=2))


if __name__=="__main__":
    main()
