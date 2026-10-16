#!/usr/bin/env python3
"""Build the reversible full-family Kitchen V6 Option B review draft.

Kitchen V5 is the sole pixel and geometry baseline. The selected Option B
recipe changes only compatible top masks; effects are drawn onto one stable
standard base and are clipped to declared masks. Nothing is promoted or wired.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from kitchen_countertop_option_b import RECIPE, RECIPE_PATH, apply_option_b, compatible_stems


ROOT = Path(__file__).resolve().parents[1]
V5_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
V5_DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v5"
CALIBRATION_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v6-calibration"
SOURCE = ROOT / "art/source/kitchen-basic-assets-2026-10-16-v6-option-b"
RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v6-option-b"
DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v6-option-b"
PUBLIC = ROOT / "public/keeper-review/kitchen-basic-assets-v6-option-b"
ASSETS = PUBLIC / "assets"

DENSITY = 4
BAY = 21
DOOR_DATUM = 4
ROOM_H = 56
ROOM_9_W = 193
ROOM_12_W = 256
TRANSPARENT = (0, 0, 0, 0)
INK = (7, 27, 50, 255)
CREAM_LIGHT = (255, 241, 201, 255)
CREAM_SHADOW = (217, 183, 118, 255)
TEAL_LIGHT = (101, 220, 228, 255)
SMOKE = (104, 116, 124, 255)
WATER = (52, 191, 234, 255)
FLAME = (255, 140, 26, 255)
FLAME_LIGHT = (255, 225, 91, 255)

ORDER = ["obj_bin", "obj_fridge", "obj_kettle", "obj_toaster", "obj_cooker", "obj_mixer", "obj_sink", "obj_table", "obj_petbowl", "obj_cupboard"]
COUNTER_ORDER = ["obj_fridge", "obj_kettle", "obj_toaster", "obj_cooker", "obj_mixer", "obj_sink"]
ANIMATED = ["obj_fridge", "obj_kettle", "obj_toaster", "obj_cooker", "obj_mixer", "obj_sink"]

EFFECT_MASKS = {
    "obj_fridge": {
        "on": [[8, 24, 80, 80]],
        "broken": [[16, 0, 68, 24], [12, 64, 72, 84]],
    },
    "obj_kettle": {"on": [[20, 0, 64, 40]], "broken": [[16, 0, 68, 40]]},
    "obj_toaster": {"on": [[20, 0, 64, 28]], "broken": [[16, 0, 72, 28]]},
    "obj_cooker": {"on": [[8, 16, 76, 36]], "broken": [[12, 0, 72, 36]]},
    "obj_mixer": {"on": [[12, 0, 72, 44]], "broken": [[12, 0, 72, 44]]},
    "obj_sink": {"on": [[28, 0, 60, 56]], "broken": [[16, 0, 68, 40], [12, 88, 72, 116]]},
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(file.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(file.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def rgba(size: tuple[int, int], colour=TRANSPARENT) -> Image.Image:
    return Image.new("RGBA", size, colour)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


V5_CATALOGUE = read_json(V5_DRAFT / "asset-catalogue.json")


def load_strip(path: Path, meta: dict) -> list[Image.Image]:
    strip = Image.open(path).convert("RGBA")
    fw, fh = meta["w"] * meta["density"], meta["h"] * meta["density"]
    return [strip.crop((i * fw, 0, (i + 1) * fw, fh)) for i in range(meta["frames"])]


def load_v5_state(stem: str, state: str) -> list[Image.Image]:
    record = V5_CATALOGUE["assets"][stem]["states"][state]
    return load_strip(ROOT / record["png"], record["meta"])


def load_v5_raw(name: str) -> Image.Image:
    return Image.open(V5_RAW / name).convert("RGBA")


def alpha_bounds(frame: Image.Image) -> dict | None:
    box = frame.getchannel("A").getbbox()
    if not box:
        return None
    x0, y0, x1, y1 = box
    return {"xLp": x0 / DENSITY, "yLp": y0 / DENSITY, "widthLp": (x1 - x0) / DENSITY, "heightLp": (y1 - y0) / DENSITY}


def make_strip(frames: list[Image.Image]) -> Image.Image:
    out = rgba((frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        out.alpha_composite(frame, (index * frame.width, 0))
    return out


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def save_strip(name: str, frames: list[Image.Image], logical: tuple[int, int], fps: int, meta: dict | None = None) -> dict:
    strip = make_strip(frames)
    png = RAW / f"{name}.png"
    save_png(strip, png)
    sidecar = {
        "w": logical[0], "h": logical[1], "frames": len(frames), "fps": fps,
        "density": DENSITY, "anchor": [logical[0] / 2, logical[1]], "z": 40,
        "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False},
    }
    if meta:
        sidecar.update(meta)
    png.with_suffix(".json").write_text(json.dumps(sidecar, indent=2) + "\n")
    urls = []
    for index, frame in enumerate(frames):
        name_frame = f"{name}_frame{index + 1}.png"
        save_png(frame, ASSETS / name_frame)
        urls.append(f"/keeper-review/kitchen-basic-assets-v6-option-b/assets/{name_frame}")
    return {"png": png.relative_to(ROOT).as_posix(), "meta": sidecar, "urls": urls, "bounds": [alpha_bounds(frame) for frame in frames]}


def review_frames(prefix: str, frames: list[Image.Image]) -> list[str]:
    urls = []
    for index, frame in enumerate(frames):
        name = f"{prefix}_frame{index + 1}.png"
        save_png(frame, ASSETS / name)
        urls.append(f"/keeper-review/kitchen-basic-assets-v6-option-b/assets/{name}")
    return urls


def ghost_overlay(base: Image.Image, frame: Image.Image) -> Image.Image:
    out = Image.new("RGBA", base.size, (8, 18, 28, 255))
    old = base.copy()
    old.putalpha(old.getchannel("A").point(lambda alpha: round(alpha * 0.4)))
    tint = Image.new("RGBA", base.size, (255, 75, 108, 0))
    tint.putalpha(old.getchannel("A"))
    out.alpha_composite(tint)
    new = frame.copy()
    new.putalpha(new.getchannel("A").point(lambda alpha: round(alpha * 0.74)))
    out.alpha_composite(new)
    return out


def clipped_composite(base: Image.Image, overlay: Image.Image, masks: list[list[int]]) -> Image.Image:
    out = base.copy()
    for x0, y0, x1, y1 in masks:
        out.alpha_composite(overlay.crop((x0, y0, x1, y1)), (x0, y0))
    return out


def render_effect(base: Image.Image, stem: str, state: str, frame: int) -> Image.Image:
    overlay = rgba(base.size)
    draw = ImageDraw.Draw(overlay)
    q = DENSITY
    if state == "on":
        if stem == "obj_fridge":
            width = (5 + frame * 3) * q
            draw.rounded_rectangle((3 * q, 7 * q, 3 * q + width, 19 * q), radius=q, fill=CREAM_LIGHT, outline=INK, width=q)
            draw.line((3 * q + width, 8 * q, 3 * q + width, 18 * q), fill=TEAL_LIGHT, width=q)
        elif stem == "obj_kettle":
            for k in range(2):
                y = max(q, (7 - frame - k * 3) * q)
                draw.ellipse((9 * q, y, 13 * q, y + 4 * q), fill=CREAM_LIGHT, outline=INK, width=1)
        elif stem == "obj_toaster":
            y = max(q, (6 - (0, 2, 5, 2)[frame]) * q)
            draw.rounded_rectangle((8 * q, y, 13 * q, y + 4 * q), radius=q, fill=CREAM_SHADOW, outline=INK, width=q)
        elif stem == "obj_cooker":
            hob_y = 35
            for x in (6 * q, 15 * q):
                flame_h = (1, 3, 2, 4)[frame] * q
                draw.polygon([(x - 2 * q, hob_y), (x, hob_y - flame_h), (x + 2 * q, hob_y)], fill=FLAME, outline=FLAME_LIGHT)
        elif stem == "obj_mixer":
            draw.arc((5 * q, 3 * q, 17 * q, 11 * q), frame * 55, frame * 55 + 170, fill=TEAL_LIGHT, width=q)
        elif stem == "obj_sink":
            draw.line((12 * q, 4 * q, 11 * q, (9 + frame) * q), fill=WATER, width=q)
    else:
        # Restrained V5-colour smoke/spark loops replace V5's whole-object
        # shake. The stable base therefore remains byte-identical off-mask.
        for k in range(3):
            x = (8 + ((frame + k * 2) % 6)) * q
            y = max(q, (6 - k * 2) * q)
            draw.ellipse((x - 2 * q, y - 2 * q, x + 2 * q, y + 2 * q), fill=SMOKE, outline=INK, width=1)
        sx, sy = (5 + frame * 3) * q, (5 + frame % 2) * q
        draw.line((sx - 2 * q, sy, sx + 2 * q, sy), fill=FLAME_LIGHT, width=q)
        draw.line((sx, sy - 2 * q, sx, sy + 2 * q), fill=FLAME, width=q)
        if stem == "obj_sink":
            draw.ellipse((7 * q, base.height - 2 * q, (14 + frame) * q, base.height - 1), fill=WATER)
        elif stem == "obj_toaster":
            draw.rounded_rectangle(((11 + frame) * q, 2 * q, (16 + frame) * q, 6 * q), radius=q, fill=CREAM_SHADOW, outline=INK, width=q)
        elif stem == "obj_fridge":
            draw.line((4 * q, base.height - 4 * q, (8 + frame) * q, base.height - q), fill=TEAL_LIGHT, width=q)
    return clipped_composite(base, overlay, EFFECT_MASKS[stem][state])


def narrow_bin(base: Image.Image) -> Image.Image:
    """Keep the V5 bin character but restore furniture-scale breathing room."""
    box = base.getchannel("A").getbbox()
    if not box:
        raise ValueError("V5 bin has no opaque pixels")
    source = base.crop(box).resize((15 * DENSITY, 14 * DENSITY), Image.Resampling.LANCZOS)
    source.putalpha(source.getchannel("A").point(lambda alpha: 255 if alpha >= 112 else 0))
    out = rgba(base.size)
    out.alpha_composite(source, ((base.width - source.width) // 2, base.height - source.height))
    return out


def render_bin_state(base: Image.Image, state: str) -> Image.Image:
    out = base.copy()
    draw = ImageDraw.Draw(out)
    q = DENSITY
    if state in {"full", "overflowing"}:
        draw.polygon([(5 * q, 3 * q), (9 * q, q), (15 * q, 4 * q)], fill=CREAM_SHADOW, outline=INK)
    if state == "overflowing":
        draw.ellipse((3 * q, 12 * q, 8 * q, 15 * q), fill=CREAM_LIGHT, outline=INK, width=q)
    return out


def base_candidates() -> tuple[dict[str, Image.Image], Image.Image, Image.Image]:
    kettle_v5 = load_v5_state("obj_kettle", "standard")[0]
    standards: dict[str, Image.Image] = {}
    for stem in ORDER:
        if stem == "obj_table":
            continue
        original = load_v5_state(stem, "standard")[0]
        if stem == "obj_bin":
            standards[stem] = narrow_bin(original)
        else:
            standards[stem] = apply_option_b(original, stem, kettle_v5) if stem in compatible_stems() else original.copy()
    chair = load_v5_raw("obj_table_chair_back_f1.png")
    table_v5 = load_v5_raw("obj_table_foreground_f1.png")
    table = apply_option_b(table_v5, "obj_table", table_v5)
    combined = chair.copy()
    combined.alpha_composite(table)
    standards["obj_table"] = combined
    return standards, chair, table


def room_shell(width_lp: int) -> Image.Image:
    return load_v5_raw(f"room_kitchen_shell_{(width_lp - DOOR_DATUM) // BAY}bay.png")


def room_composite(standards: dict[str, Image.Image], width_lp: int, outline: bool = False) -> Image.Image:
    if outline:
        return load_v5_raw("room_kitchen_12bay_outline.png")
    out = room_shell(width_lp).copy()
    bays = {"obj_bin": 1, "obj_fridge": 2, "obj_kettle": 3, "obj_toaster": 4, "obj_cooker": 5, "obj_mixer": 6, "obj_sink": 7, "obj_table": 8}
    for stem, bay in bays.items():
        frame = standards[stem]
        span = V5_CATALOGUE["assets"][stem]["bays"]
        x = (DOOR_DATUM + (bay - 1) * BAY) * DENSITY + (span * BAY * DENSITY - frame.width) // 2
        out.alpha_composite(frame, (x, ROOM_H * DENSITY - frame.height))
    bowl = standards["obj_petbowl"]
    out.alpha_composite(bowl, (172 * DENSITY, ROOM_H * DENSITY - bowl.height))
    return out


def horizontal_run(standards: dict[str, Image.Image], stems: list[str], height_lp: int = 31) -> Image.Image:
    out = rgba((len(stems) * BAY * DENSITY, height_lp * DENSITY))
    for index, stem in enumerate(stems):
        frame = standards[stem]
        out.alpha_composite(frame, (index * BAY * DENSITY, out.height - frame.height))
    return out


def load_keeper(stem: str) -> list[str]:
    matches = list((ROOT / "art/raw/keeper-first-batch").glob(f"{stem}_f*.png"))
    if len(matches) != 1:
        raise ValueError(f"expected one Keeper source for {stem}, found {len(matches)}")
    meta = read_json(matches[0].with_suffix(".json"))
    return review_frames(stem, load_strip(matches[0], meta))


def copy_room_evidence() -> dict:
    records = {}
    names = ["room_kitchen_repeat_a", "room_kitchen_repeat_b", "room_kitchen_repeat_c", "room_kitchen_stair_cap", "room_kitchen_far_cap_closed", "room_kitchen_far_cap_open"]
    names += [f"room_kitchen_shell_{n}bay" for n in range(6, 13)]
    for name in names:
        source_png = V5_RAW / f"{name}.png"
        source_json = source_png.with_suffix(".json")
        shutil.copy2(source_png, RAW / source_png.name)
        shutil.copy2(source_json, RAW / source_json.name)
        meta = read_json(source_json)
        records[name] = review_frames(f"v6_{name}", load_strip(source_png, meta))[0]
    return records


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Basic Assets V6 · Option B full-family review</title><style>
:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--muted:#a8bdc4;--gold:#efb64d;--cyan:#58d4df;--red:#ff786d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1520px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:12px;min-width:0}.compare{display:grid;grid-template-columns:repeat(3,minmax(90px,1fr));gap:8px}.well{min-height:190px;display:flex;align-items:end;justify-content:center;overflow:auto;background:repeating-conic-gradient(#172c36 0 25%,#10232d 0 50%) 0/18px 18px;border-radius:8px;padding:8px}.well img{flex:none}.small{font-size:.84rem;color:var(--muted)}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0}button,select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.scroll{overflow:auto;background:#071923;border-radius:10px;padding:10px}.run{position:relative;display:inline-block}.run img{display:block}.guides{position:absolute;inset:0;pointer-events:none}.guides i{position:absolute;left:0;right:0;border-top:1px dashed}.guides .front{bottom:76px;border-color:var(--gold)}.guides .rear{bottom:82px;border-color:var(--cyan)}.guides .cells{inset:0;background:repeating-linear-gradient(90deg,transparent 0 83px,rgba(255,120,109,.55) 83px 84px)}.seam{position:relative;display:inline-block}.seam:after{content:"21-lp bay seam";position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed var(--red);font-size:10px;padding-left:4px}.logical img{width:126px;height:31px;image-rendering:auto}.scale{display:flex;align-items:end;justify-content:center;gap:10px;min-height:180px}.scale .keeper{width:128px;height:160px;object-fit:contain}.layers{position:relative;width:168px;height:112px;margin:auto}.layers img{position:absolute;inset:0}.layers .keeper{width:128px;height:160px;left:20px;top:-48px;object-fit:contain}.layers .chair{z-index:10}.layers .keeper{z-index:20}.layers .table{z-index:30}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:7px;border-bottom:1px solid var(--line);vertical-align:top}code{color:#9ce5ea;word-break:break-all}@media(max-width:720px){header,main{padding:12px}.compare{grid-template-columns:1fr}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">Option B selected construction</span><span class="tag">V5 sole baseline</span><h1>Kitchen Basic Assets V6 · full family</h1><p>Review-only redraw using Frank's selected 1.5-lp countertop construction. Nothing is approved, promoted or wired.</p><p id="loading" class="notice">Preloading and decoding every unique frame… controls remain locked.</p></header><main>
<section class="panel"><h2>Locked recipe</h2><p>Every compatible unit uses the same 1.5-lp visible top, 2-lp fascia, equal 20-lp horizontal rear/front edges, zero shear and vertical constant-width bodies. The table uses the same construction over its 40-lp front. Exact 21-lp cells and transparent gutters take priority over forced contact; the remaining ownership seam is straight, never V-shaped. The pedal bin is deliberately narrower at 15 lp, centred with 3 lp clear on each side of its unchanged bay.</p><p class="notice"><strong>Approval boundary:</strong> this page requests review of the full draft family only. Runtime sprites, Final, manifests, Keeper art and animations are unchanged.</p></section>
<section class="panel"><h2>Every asset and state · exact V5 beside V6</h2><p>Animated states use one fixed V6 standard base. Ghost view overlays each state on that base; stationary pixels outside the declared mask are byte-identical.</p><div id="assetGrid" class="grid"></div></section>
<section class="panel"><h2>Complete compatible run · parallel edge guides</h2><div class="grid"><div class="card"><h3>Exact V5</h3><div class="scroll"><img id="runV5"></div></div><div class="card"><h3>V6 Option B</h3><div class="scroll"><div class="run"><img id="runV6"><div class="guides"><i class="rear"></i><i class="front"></i><i class="cells"></i></div></div></div></div></div><h3>Two adjacent ordinary units</h3><div class="scroll"><span class="seam"><img id="seam"></span></div><h3>Exact logical game scale</h3><div class="scroll logical"><img id="logical"></div></section>
<section class="panel"><h2>Modular room shell · 6–12 bays</h2><div class="controls"><label>Assembly <select id="shellSelect" disabled></select></label></div><div class="scroll"><img id="shell" style="height:224px;width:auto"></div><p>The shell is byte-identical to V5: 56-lp height, 5-lp floor band, fixed stair datum and fixed right-side-wall cupboard cap.</p></section>
<section class="panel"><h2>9-bay starting kitchen · 193 × 56 lp</h2><div class="scroll"><img id="room9" style="height:224px;width:auto"></div><p>Every reservation remains a whole bay. The right-side-wall cupboard is fixed in the far cap and always last.</p></section>
<section class="panel"><h2>12-bay outline · 256 × 56 lp</h2><div class="scroll"><img id="room12" style="height:224px;width:auto"></div></section>
<section class="panel"><h2>Keeper scale beside every major asset</h2><p>The same unchanged Keeper walk frame is reused without resizing between cards.</p><div id="scaleGrid" class="grid"></div></section>
<section class="panel"><h2>Table/chair draw stack</h2><div class="grid"><div class="card"><div class="layers"><img class="chair" id="chair"><img class="keeper" id="sit"><img class="table" id="table"></div></div><div><p>Chair behind the rear-facing seated Keeper; table and apron in front. Seat remains 11 lp and tabletop contact remains 19 lp. The table now uses the selected B construction while the sitting geometry and floor contact remain unchanged.</p></div></div></section>
<section class="panel"><h2>Right-side-wall cupboard lifecycle</h2><p>The cupboard is exact V5: closed edge-on, fixed right hinge, rectangular opaque leaf extending left, open through activity and put-away, then closing only after the standard-walk exit is clear. It remains a foreground occluder and takes no furniture bay.</p><div class="scroll"><img id="cupboard" style="height:224px;width:auto"></div></section>
<section class="panel"><h2>19-lp cooker check</h2><div class="grid"><div class="card"><h3>Cake retrieval</h3><div class="scale"><img id="cookerCake"><img class="keeper" id="cake"></div></div><div class="card"><h3>Meal retrieval</h3><div class="scale"><img id="cookerMeal"><img class="keeper" id="meal"></div></div></div><p>The existing Keeper clips remain unchanged and continue to read against the 19-lp cooker front.</p></section>
<section class="panel"><h2>Sink dish overlays</h2><div id="dishes" class="grid"></div></section>
<section class="panel"><h2>Measured hand-back and hashes</h2><table><thead><tr><th>Item</th><th>Cell</th><th>Largest bound</th><th>Bays</th><th>Interaction</th><th>V5 standard SHA-256</th><th>V6 standard SHA-256</th></tr></thead><tbody id="rows"></tbody></table></section>
</main><script>
const DATA=__DATA__,all=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))all.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const urls=[...new Set(all)];const img=(src,alt='')=>Object.assign(new Image,{src,alt});
function setupAssets(){const grid=document.getElementById('assetGrid');for(const [stem,a] of Object.entries(DATA.assets)){const card=document.createElement('article');card.className='card';card.innerHTML=`<h3>${a.label}</h3><div class="controls"><select></select><button>Previous</button><button>Play</button><button>Next</button></div><div class="compare"><div><div class="well v5"></div><p class="small">Exact V5</p></div><div><div class="well v6"></div><p class="small">V6 Option B</p></div><div><div class="well ghost"></div><p class="small">base/state ghost</p></div></div><p class="small">cell ${a.cell.join('×')} lp · ${a.bays} bay(s) · interaction ${a.interactionSpotKu} ku</p>`;const sel=card.querySelector('select'),buttons=card.querySelectorAll('button'),states=Object.keys(a.states);states.forEach(s=>sel.add(new Option(s,s)));let n=0,t=null;const show=()=>{const s=a.states[sel.value],k=n%s.v6Urls.length;card.querySelector('.v5').replaceChildren(img(s.v5Urls[k%s.v5Urls.length],`${a.label} V5 ${sel.value}`));card.querySelector('.v6').replaceChildren(img(s.v6Urls[k],`${a.label} V6 ${sel.value}`));card.querySelector('.ghost').replaceChildren(img(s.ghostUrls[k],`${a.label} ghost ${sel.value}`))};sel.onchange=()=>{n=0;show()};buttons[0].onclick=()=>{clearInterval(t);t=null;n--;show()};buttons[2].onclick=()=>{clearInterval(t);t=null;n++;show()};buttons[1].onclick=()=>{if(t){clearInterval(t);t=null;buttons[1].textContent='Play'}else{t=setInterval(()=>{n++;show()},125);buttons[1].textContent='Pause'}};show();grid.append(card)}}
function setupShell(){const sel=document.getElementById('shellSelect');for(let n=6;n<=12;n++)sel.add(new Option(`${n} bays · ${4+21*n} lp`,n));sel.value='9';const show=()=>document.getElementById('shell').src=DATA.shells[sel.value];sel.onchange=show;show()}
function setupScale(){const grid=document.getElementById('scaleGrid');for(const stem of DATA.major){const a=DATA.assets[stem],card=document.createElement('div');card.className='card';card.innerHTML=`<h3>${a.label}</h3><div class="scale"></div>`;card.querySelector('.scale').append(img(a.states.standard.v6Urls[0],a.label),Object.assign(img(DATA.keeper.keeper_walk[0],'Unchanged Keeper'),{className:'keeper'}));grid.append(card)}}
function setupRows(){const body=document.getElementById('rows');for(const a of Object.values(DATA.assets)){const tr=document.createElement('tr');tr.innerHTML=`<td>${a.label}</td><td>${a.cell.join('×')} lp</td><td>${a.largestBound.widthLp}×${a.largestBound.heightLp} lp</td><td>${a.bays}</td><td>${a.interactionSpotKu} ku</td><td><code>${a.v5StandardSha256}</code></td><td><code>${a.v6StandardSha256}</code></td>`;body.append(tr)}}
function setup(){document.querySelectorAll('button,select').forEach(x=>x.disabled=false);setupAssets();setupShell();setupScale();setupRows();document.getElementById('runV5').src=DATA.runV5;document.getElementById('runV6').src=DATA.runV6;document.getElementById('seam').src=DATA.seam;document.getElementById('logical').src=DATA.runV6;document.getElementById('room9').src=DATA.room9;document.getElementById('room12').src=DATA.room12;document.getElementById('chair').src=DATA.chair;document.getElementById('table').src=DATA.table;document.getElementById('sit').src=DATA.keeper.keeper_sit_back.at(-1);document.getElementById('cupboard').src=DATA.assets.obj_cupboard.states.open.v6Urls[0];const cooker=DATA.assets.obj_cooker.states.standard.v6Urls[0];document.getElementById('cookerCake').src=cooker;document.getElementById('cookerMeal').src=cooker;document.getElementById('cake').src=DATA.keeper.keeper_cake_from_oven_back[3];document.getElementById('meal').src=DATA.keeper.keeper_meal_from_oven_back[3];for(const u of DATA.dishes){const c=document.createElement('div');c.className='card';c.append(img(u,'Sink dish overlay'));document.getElementById('dishes').append(c)}document.getElementById('loading').textContent=`All ${urls.length} unique review images loaded and decoded. Controls enabled.`}
document.querySelectorAll('button,select').forEach(x=>x.disabled=true);Promise.all(urls.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>document.getElementById('loading').textContent=`Media failed to load: ${e.message}`);
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

    standards, chair, table = base_candidates()
    # Pin the three calibration authorities byte-for-byte.
    for stem in ("obj_kettle", "obj_cooker", "obj_sink"):
        selected = load_v5_raw(f"{stem}_standard_f1.png")
        standards[stem] = apply_option_b(selected, stem, load_v5_state("obj_kettle", "standard")[0])

    catalogue = {
        "version": 6, "variant": "option-b", "status": "reversible-draft",
        "density": DENSITY, "recipe": RECIPE["id"],
        "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False, "camera": "straight-on", "vanishingPoint": False},
        "room": V5_CATALOGUE["room"], "assets": {},
    }

    for stem in ORDER:
        v5_asset = V5_CATALOGUE["assets"][stem]
        entry = {key: v5_asset[key] for key in ("label", "cell", "bays", "interactionSpotKu", "frontRectLp", "projection")}
        if stem == "obj_bin":
            entry["label"] = "Pedal bin"
        entry["topRevealLp"] = 1.5 if stem in compatible_stems() else v5_asset["topRevealLp"]
        entry["recipeApplies"] = stem in compatible_stems()
        entry["states"] = {}
        base = standards[stem]
        for state, v5_state in v5_asset["states"].items():
            v5_frames = load_v5_state(stem, state)
            if stem in ANIMATED and state in {"on", "broken"}:
                frames = [render_effect(base, stem, state, index) for index in range(4)]
                masks = EFFECT_MASKS[stem][state]
            elif stem == "obj_bin":
                frames = [render_bin_state(base, state)]
                masks = [] if state == "standard" else [[12, 0, 72, 64]]
            elif state == "standard":
                frames = [base]
                masks = [RECIPE["compatibleUnits"][stem]["maskPx"]] if stem in compatible_stems() else []
            else:
                frames = [frame.copy() for frame in v5_frames]
                masks = []
            saved = save_strip(f"{stem}_{state}_f{len(frames)}", frames, tuple(entry["cell"]), v5_state["meta"]["fps"], {
                "interactionSpotKu": entry["interactionSpotKu"],
                "contactDatumsLp": v5_state["meta"].get("contactDatumsLp"),
                "declaredChangeMasksPx": masks,
                "stableBaseOutsideMasks": stem in ANIMATED and state in {"on", "broken"},
            })
            v5_urls = review_frames(f"v5_{stem}_{state}", v5_frames)
            ghost_base = load_v5_state(stem, "standard")[0] if state == "standard" else base
            ghost_urls = review_frames(f"ghost_{stem}_{state}", [ghost_overlay(ghost_base, frame) for frame in frames])
            saved.update({"v5Urls": v5_urls, "v6Urls": saved.pop("urls"), "ghostUrls": ghost_urls, "v5StripSha256": sha(ROOT / v5_state["png"]), "v6StripSha256": sha(ROOT / saved["png"])})
            entry["states"][state] = saved
        bounds = [bound for state in entry["states"].values() for bound in state["bounds"] if bound]
        entry["largestBound"] = {"widthLp": max(round(bound["widthLp"], 2) for bound in bounds), "heightLp": max(round(bound["heightLp"], 2) for bound in bounds)}
        entry["v5StandardSha256"] = sha(ROOT / v5_asset["states"]["standard"]["png"])
        entry["v6StandardSha256"] = sha(ROOT / entry["states"]["standard"]["png"])
        catalogue["assets"][stem] = entry

    # Preserve V5 overlays and architecture byte-for-byte where the recipe is irrelevant.
    dishes = []
    for level in range(1, 4):
        name = f"obj_sink_dishes{level}_f1"
        source_png = V5_RAW / f"{name}.png"
        shutil.copy2(source_png, RAW / source_png.name)
        shutil.copy2(source_png.with_suffix(".json"), RAW / f"{name}.json")
        dishes.extend(review_frames(f"v6_{name}", [load_v5_raw(f"{name}.png")]))
    room_records = copy_room_evidence()
    chair_saved = save_strip("obj_table_chair_back_f1", [chair], (42, 28), 0, {"z": 35, "layerRole": "background-chair", "seatContactLp": 11})
    table_saved = save_strip("obj_table_foreground_f1", [table], (42, 28), 0, {"z": 60, "layerRole": "foreground-table-apron", "tableContactLp": 19})

    room9 = room_composite(standards, ROOM_9_W)
    room12 = room_composite(standards, ROOM_12_W, True)
    run_v5 = horizontal_run({stem: load_v5_state(stem, "standard")[0] for stem in COUNTER_ORDER}, COUNTER_ORDER)
    run_v6 = horizontal_run(standards, COUNTER_ORDER)
    seam = horizontal_run({"obj_kettle": standards["obj_kettle"]}, ["obj_kettle", "obj_kettle"])
    for name, image in (("room_kitchen_9bay_composite", room9), ("room_kitchen_12bay_outline", room12), ("complete_counter_run_v5", run_v5), ("complete_counter_run_v6_option_b", run_v6), ("ordinary_counter_seam_option_b", seam)):
        save_png(image, RAW / f"{name}.png")
        save_png(image, ASSETS / f"{name}.png")

    keeper = {stem: load_keeper(stem) for stem in ("keeper_walk", "keeper_sit_back", "keeper_cake_from_oven_back", "keeper_meal_from_oven_back")}
    data = {
        "assets": catalogue["assets"], "major": ORDER[:-1], "keeper": keeper,
        "runV5": "/keeper-review/kitchen-basic-assets-v6-option-b/assets/complete_counter_run_v5.png",
        "runV6": "/keeper-review/kitchen-basic-assets-v6-option-b/assets/complete_counter_run_v6_option_b.png",
        "seam": "/keeper-review/kitchen-basic-assets-v6-option-b/assets/ordinary_counter_seam_option_b.png",
        "room9": "/keeper-review/kitchen-basic-assets-v6-option-b/assets/room_kitchen_9bay_composite.png",
        "room12": "/keeper-review/kitchen-basic-assets-v6-option-b/assets/room_kitchen_12bay_outline.png",
        "shells": {str(n): room_records[f"room_kitchen_shell_{n}bay"] for n in range(6, 13)},
        "chair": chair_saved["urls"][0],
        "table": table_saved["urls"][0],
        "dishes": dishes,
    }
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)

    outputs = sorted(RAW.glob("*")) + sorted(DRAFT.glob("*.json")) + [PUBLIC / "index.html"]
    register = {
        "version": 6, "variant": "option-b", "status": "reversible-draft",
        "soleVisualBaseline": "Kitchen Basic Assets V5", "readsFormerV6": False,
        "selectedCalibration": {"option": "B", "topRevealLp": 1.5, "calibrationSet": "kitchen-countertop-calibration-v6"},
        "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)},
        "runtimeChanged": False, "finalChanged": False, "keeperChanged": False,
        "protectedSnapshots": {
            "kitchenV5": tree_sha(V5_RAW),
            "calibration": tree_sha(CALIBRATION_RAW),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
        "outputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs if path.is_file()],
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"assets": len(catalogue["assets"]), "variant": "option-b", "roomWidthsLp": [193, 256], "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
