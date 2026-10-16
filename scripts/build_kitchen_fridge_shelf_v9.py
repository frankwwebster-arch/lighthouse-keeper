#!/usr/bin/env python3
"""Build the reversible Kitchen V9 fridge-and-shelf review draft.

V8 is immutable.  This builder changes only the fridge drawing, adds a separate
fridge-owned wall shelf, and recomposes review evidence without touching live
game art or manifests.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

import build_kitchen_wall_anchored_v8 as v8
from build_kitchen_basic_assets_v6_option_b import render_effect


ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = ROOT / "data/kitchen_fridge_shelf_v9_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
V5_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
V5_DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v5"
V8_RAW = ROOT / "art/raw/kitchen-wall-anchored-2026-10-16-v8"
V8_DRAFT = ROOT / "art/drafts/kitchen-wall-anchored-2026-10-16-v8"
V7_RAW = ROOT / "art/raw/kitchen-room-flat-cutaway-2026-10-16-v7"
SOURCE = ROOT / "art/source/kitchen-fridge-shelf-2026-10-17-v9"
RAW = ROOT / "art/raw/kitchen-fridge-shelf-2026-10-17-v9"
DRAFT = ROOT / "art/drafts/kitchen-fridge-shelf-2026-10-17-v9"
PUBLIC = ROOT / "public/keeper-review/kitchen-fridge-shelf-v9"
ASSETS = PUBLIC / "assets"

DENSITY = 4
BAY = 21
DOOR_DATUM = 4
ROOM_H = 56
FOOT_LINE = 52
TRANSPARENT = (0, 0, 0, 0)
INK = (7, 27, 50, 255)
WHITE_HIGHLIGHT = (255, 255, 251, 255)
WHITE = (248, 248, 238, 255)
WHITE_MID = (233, 234, 225, 255)
WHITE_SHADOW = (196, 207, 211, 255)
WHITE_DEEP = (146, 166, 175, 255)
BRASS_DARK = (135, 80, 12, 255)
BRASS = (215, 150, 34, 255)
BRASS_LIGHT = (255, 205, 67, 255)
WOOD_DARK = (93, 48, 29, 255)
WOOD = (154, 86, 48, 255)
WOOD_LIGHT = (211, 138, 70, 255)
WOOD_HIGHLIGHT = (238, 174, 88, 255)
TEAL_DARK = (10, 106, 134, 255)
TEAL = (20, 184, 204, 255)
TEAL_LIGHT = (104, 232, 236, 255)
LEAF_DARK = (38, 91, 35, 255)
LEAF = (73, 143, 48, 255)
LEAF_LIGHT = (139, 189, 67, 255)


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


def alpha_bound(image: Image.Image) -> dict | None:
    box = image.getchannel("A").getbbox()
    if not box:
        return None
    x0, y0, x1, y1 = box
    return {"xLp": x0 / 4, "yLp": y0 / 4, "widthLp": (x1 - x0) / 4, "heightLp": (y1 - y0) / 4}


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=False, compress_level=9)


def make_strip(frames: list[Image.Image]) -> Image.Image:
    strip = rgba((frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * frame.width, 0))
    return strip


def save_strip(name: str, frames: list[Image.Image], logical: tuple[int, int], fps: int, extra: dict | None = None) -> dict:
    strip_path = RAW / f"{name}.png"
    save_png(make_strip(frames), strip_path)
    meta = {
        "w": logical[0], "h": logical[1], "frames": len(frames), "fps": fps,
        "density": DENSITY, "anchor": [logical[0] / 2, logical[1]], "z": 40,
        "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False},
    }
    if extra:
        meta.update(extra)
    strip_path.with_suffix(".json").write_text(json.dumps(meta, indent=2) + "\n")
    urls = []
    for index, frame in enumerate(frames):
        path = ASSETS / f"{name}_frame{index + 1}.png"
        save_png(frame, path)
        urls.append(f"/keeper-review/kitchen-fridge-shelf-v9/assets/{path.name}")
    return {
        "png": strip_path.relative_to(ROOT).as_posix(),
        "json": strip_path.with_suffix(".json").relative_to(ROOT).as_posix(),
        "sha256": sha(strip_path), "meta": meta, "urls": urls,
        "bounds": [alpha_bound(frame) for frame in frames],
    }


def save_asset(name: str, image: Image.Image, logical: tuple[int, int], extra: dict | None = None) -> dict:
    return save_strip(name, [image], logical, 0, extra)


def load_strip(path: Path, meta: dict) -> list[Image.Image]:
    image = Image.open(path).convert("RGBA")
    width, height = meta["w"] * DENSITY, meta["h"] * DENSITY
    return [image.crop((i * width, 0, (i + 1) * width, height)) for i in range(meta["frames"])]


def enriched_white_fridge() -> Image.Image:
    """White enamel appliance with V5-like depth and no furniture top."""
    out = rgba((px(21), px(21)))
    d = ImageDraw.Draw(out)
    # Deep casing silhouette and cool side return.
    d.rounded_rectangle((3, 3, 80, 80), radius=7, fill=INK)
    d.rounded_rectangle((6, 5, 77, 78), radius=5, fill=WHITE_SHADOW)
    d.rectangle((9, 12, 73, 74), fill=WHITE)
    d.rectangle((73, 15, 76, 73), fill=WHITE_DEEP)
    d.rectangle((10, 17, 13, 70), fill=WHITE_HIGHLIGHT)

    # A white enamel appliance lid: layered bevel, never a brown countertop.
    d.rounded_rectangle((4, 2, 79, 17), radius=5, fill=INK)
    d.rounded_rectangle((7, 4, 76, 14), radius=3, fill=WHITE_MID)
    d.rectangle((10, 5, 73, 9), fill=WHITE_HIGHLIGHT)
    d.line((8, 13, 75, 13), fill=WHITE_DEEP, width=2)
    d.line((8, 16, 75, 16), fill=INK, width=2)

    # Inset front door and readable enamel volume.
    d.rounded_rectangle((8, 18, 74, 75), radius=4, fill=WHITE_SHADOW)
    d.rounded_rectangle((11, 20, 71, 72), radius=3, fill=WHITE)
    d.line((12, 22, 12, 69), fill=WHITE_HIGHLIGHT, width=3)
    d.line((69, 23, 69, 68), fill=WHITE_MID, width=2)
    d.line((15, 21, 65, 21), fill=WHITE_HIGHLIGHT, width=2)
    d.line((13, 71, 68, 71), fill=WHITE_DEEP, width=1)

    # Brass pull with highlight/shadow, plus two right-side hinges.
    d.rounded_rectangle((16, 25, 53, 31), radius=3, fill=INK)
    d.rounded_rectangle((19, 26, 50, 29), radius=2, fill=BRASS)
    d.ellipse((17, 24, 24, 31), fill=BRASS_DARK, outline=INK)
    d.ellipse((19, 25, 22, 28), fill=BRASS_LIGHT)
    d.ellipse((47, 24, 54, 31), fill=BRASS_DARK, outline=INK)
    d.ellipse((48, 25, 51, 28), fill=BRASS_LIGHT)
    for y in (22, 52):
        d.rounded_rectangle((71, y, 77, y + 13), radius=2, fill=INK)
        d.rectangle((73, y + 2, 75, y + 10), fill=BRASS)
        d.point((74, y + 3), fill=BRASS_LIGHT)

    # Vent and feet add unmistakable appliance detail.
    d.rounded_rectangle((16, 65, 67, 75), radius=3, fill=INK)
    d.rectangle((20, 68, 63, 72), fill=(45, 62, 78, 255))
    for x in range(22, 63, 9):
        d.line((x, 68, x, 72), fill=(9, 21, 36, 255), width=2)
    d.line((20, 69, 63, 69), fill=(92, 108, 116, 255), width=1)
    for x0, x1 in ((7, 21), (63, 77)):
        d.rounded_rectangle((x0, 76, x1, 83), radius=3, fill=INK)
        d.rectangle((x0 + 3, 78, x1 - 3, 81), fill=(67, 82, 94, 255))
        d.point((x0 + 4, 78), fill=(123, 141, 148, 255))
    return out


def fridge_shelf() -> Image.Image:
    """Separate 21×56-lp wall child, wholly above the refrigerator."""
    out = rgba((px(21), px(56)))
    d = ImageDraw.Draw(out)
    # Trailing plant: compact crown and a clear downward vine.
    d.rounded_rectangle((13, 79, 29, 93), radius=3, fill=INK)
    d.rectangle((16, 81, 26, 91), fill=WOOD)
    d.line((20, 82, 20, 58), fill=LEAF_DARK, width=3)
    leaves = [(15, 58), (21, 54), (27, 58), (11, 65), (22, 64), (29, 69), (12, 72), (24, 74), (10, 82), (8, 91), (9, 101)]
    for index, (x, y) in enumerate(leaves):
        d.ellipse((x - 5, y - 3, x + 5, y + 4), fill=INK)
        d.ellipse((x - 3, y - 2, x + 3, y + 2), fill=LEAF_LIGHT if index % 3 == 0 else LEAF)
    d.line((13, 78, 8, 108), fill=LEAF_DARK, width=3)

    # Blue pot plus two cream pantry jars, echoing the supplied room reference.
    d.ellipse((34, 67, 52, 72), fill=INK)
    d.rounded_rectangle((33, 69, 53, 91), radius=4, fill=INK)
    d.rounded_rectangle((36, 70, 50, 88), radius=3, fill=TEAL)
    d.rectangle((38, 72, 41, 84), fill=TEAL_LIGHT)
    d.arc((36, 70, 50, 88), 280, 80, fill=TEAL_DARK, width=2)
    d.rounded_rectangle((56, 75, 65, 91), radius=2, fill=INK)
    d.rectangle((58, 78, 63, 89), fill=WHITE)
    d.rectangle((57, 74, 64, 78), fill=BRASS_DARK)
    d.rounded_rectangle((66, 68, 77, 91), radius=2, fill=INK)
    d.rectangle((68, 72, 75, 89), fill=WHITE_HIGHLIGHT)
    d.rectangle((67, 67, 76, 72), fill=WOOD_LIGHT)

    # Straight shelf and brackets. Bounds stay x=1..20 lp with alpha gutters.
    d.rectangle((4, 92, 79, 105), fill=INK)
    d.rectangle((7, 94, 76, 101), fill=WOOD)
    d.line((8, 95, 74, 95), fill=WOOD_HIGHLIGHT, width=2)
    d.line((7, 102, 76, 102), fill=WOOD_DARK, width=2)
    for x in (14, 66):
        d.rectangle((x, 105, x + 8, 121), fill=INK)
        d.rectangle((x + 2, 105, x + 6, 117), fill=WOOD)
        d.line((x + 2, 106, x + 5, 106), fill=WOOD_LIGHT)
    # Enforce the declared 19×17-lp ownership envelope deterministically.
    clipped = rgba(out.size)
    clipped.alpha_composite(out.crop((4, 54, 80, 122)), (4, 54))
    return clipped


def place_one_bay(out: Image.Image, image: Image.Image, bay: int) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY) + (px(BAY) - image.width) // 2
    out.alpha_composite(image, (x, px(FOOT_LINE) - image.height))


def place_two_bays(out: Image.Image, image: Image.Image, bay: int) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY) + (px(2 * BAY) - image.width) // 2
    out.alpha_composite(image, (x, px(FOOT_LINE) - image.height))


def place_wall_child(out: Image.Image, image: Image.Image, bay: int) -> None:
    out.alpha_composite(image, (px(DOOR_DATUM + (bay - 1) * BAY), 0))


def v8_standard(stem: str, catalogue: dict) -> Image.Image:
    record = catalogue["assets"][stem]["states"]["standard"]
    return load_strip(ROOT / record["png"], record["meta"])[0]


def room_composite(standards: dict[str, Image.Image], shelf: Image.Image, condition: str) -> Image.Image:
    out = Image.open(V7_RAW / "room_kitchen_shell_9bay.png").convert("RGBA")
    place_wall_child(out, shelf, 2)
    positions = {"obj_bin": 1, "obj_fridge": 2, "obj_kettle": 3, "obj_toaster": 4, "obj_cooker": 5, "obj_mixer": 6}
    for stem, bay in positions.items():
        place_one_bay(out, standards[stem], bay)
    v8.place_sink_children(out, 7, condition)
    place_one_bay(out, standards["obj_sink"], 7)
    place_two_bays(out, standards["obj_table"], 8)
    place_one_bay(out, standards["obj_petbowl"], 9)
    return out


def move_proof(fridge: Image.Image, shelf: Image.Image, bay: int) -> Image.Image:
    out = Image.open(V7_RAW / "room_kitchen_shell_9bay.png").convert("RGBA")
    place_wall_child(out, shelf, bay)
    place_one_bay(out, fridge, bay)
    return out


def pair_proof(fridge: Image.Image, shelf: Image.Image) -> Image.Image:
    out = rgba((px(21), px(56)))
    out.alpha_composite(shelf)
    out.alpha_composite(fridge, (0, px(FOOT_LINE) - fridge.height))
    return out


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V9 · dimensional fridge and attached shelf</title><style>
:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--muted:#a8bdc4;--gold:#efb64d;--cyan:#58d4df}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1520px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:12px;min-width:0}.compare3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.well{min-height:250px;display:flex;align-items:end;justify-content:center;overflow:auto;background:repeating-conic-gradient(#172c36 0 25%,#10232d 0 50%) 0/18px 18px;border-radius:8px;padding:8px}.well img{flex:none}.scroll{overflow:auto;background:#071923;border-radius:10px;padding:10px}.scroll img{display:block;height:224px;width:auto}.small{font-size:.84rem;color:var(--muted)}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0}button,select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.recipe{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}.metric{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:10px}.metric strong{display:block;color:var(--gold);font-size:1.15rem}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:7px;border-bottom:1px solid var(--line);vertical-align:top}code{color:#9ce5ea;word-break:break-all}@media(max-width:720px){header,main{padding:12px}.compare3{grid-template-columns:1fr}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">V8 preserved</span><span class="tag">Fridge-owned wall child</span><h1>Kitchen V9 · dimensional white fridge and attached shelf</h1><p>Only the fridge has been redrawn. A separate shelf with a plant and pantry pots now travels with it; every other approved V8 draft element is unchanged.</p><p id="loading" class="notice">Preloading and decoding every unique review image… controls remain locked.</p></header><main>
<section class="panel"><h2>Locked V9 recipe</h2><div class="recipe"><div class="metric"><strong>21 × 21 lp</strong>unchanged fridge cell</div><div class="metric"><strong>no countertop</strong>white enamel lid</div><div class="metric"><strong>21 × 56 lp</strong>separate shelf cell</div><div class="metric"><strong>19-lp max</strong>shelf width</div><div class="metric"><strong>52 lp</strong>unchanged foot line</div><div class="metric"><strong>same delta</strong>shelf follows fridge</div></div><p class="notice"><strong>Approval boundary:</strong> review draft only. No runtime art, live manifests, Keeper assets or Final art have changed.</p></section>
<section class="panel"><h2>Fridge redraw · every state</h2><p>V5 supplies the richer volume cue; V8 shows the overly flat transposition; V9 keeps the bright-white request while restoring lid bevel, door inset, side highlight and casing shadow.</p><div class="controls"><label>State <select id="state" disabled><option>standard</option><option>on</option><option>broken</option></select></label><button id="prev" disabled>Previous</button><button id="play" disabled>Play</button><button id="next" disabled>Next</button></div><div class="compare3"><div class="card"><h3>V5 dimensional reference</h3><div class="well"><img id="v5"></div></div><div class="card"><h3>V8 flat white</h3><div class="well"><img id="v8"></div></div><div class="card"><h3>V9 white enamel</h3><div class="well"><img id="v9"></div></div></div></section>
<section class="panel"><h2>Separate fridge-owned wall detail</h2><div class="grid"><div class="card"><h3>Shelf layer only</h3><div class="well"><img id="shelf"></div><p class="small">21×56-lp transparent cell · max 19×17-lp opaque bound · z26</p></div><div class="card"><h3>Attached pair</h3><div class="well"><img id="pair"></div><p class="small">Shelf stays above the refrigerator and is not baked into either sprite or room shell.</p></div></div></section>
<section class="panel"><h2>Move the fridge · shelf follows exactly</h2><div class="controls"><label>Fridge bay <select id="bay" disabled><option>2</option><option>5</option><option>8</option></select></label></div><div class="scroll"><img id="move"></div><p>Shelf delta = fridge delta. Both remain one-bay assets and neither is rescaled.</p></section>
<section class="panel"><h2>Full 9-bay kitchen · V8 versus V9</h2><div class="grid"><div class="card"><h3>Immutable V8</h3><div class="scroll"><img id="room8"></div></div><div class="card"><h3>V9 fridge + shelf only</h3><div class="scroll"><img id="room9"></div></div></div><p>The bin, counters, cooker, porthole, sink, table/chair, pet bowl, room projection and rear-wall anchoring are byte-identical to V8.</p></section>
<section class="panel"><h2>Measured hand-back and hashes</h2><table><thead><tr><th>Item</th><th>Cell / bound</th><th>Ownership / interaction</th><th>SHA-256</th></tr></thead><tbody id="rows"></tbody></table></section>
</main><script>
const DATA=__DATA__,all=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))all.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const urls=[...new Set(all)];const image=(src,alt='')=>Object.assign(new Image,{src,alt});let n=0,t=null;
function showState(){const key=state.value,s=DATA.fridge[key],k=((n%s.v9.length)+s.v9.length)%s.v9.length;v5.src=s.v5[k%s.v5.length];v8.src=s.v8[k%s.v8.length];v9.src=s.v9[k];}
function setup(){document.querySelectorAll('button,select').forEach(x=>x.disabled=false);state.onchange=()=>{n=0;showState()};prev.onclick=()=>{clearInterval(t);t=null;n--;showState()};next.onclick=()=>{clearInterval(t);t=null;n++;showState()};play.onclick=()=>{if(t){clearInterval(t);t=null;play.textContent='Play'}else{t=setInterval(()=>{n++;showState()},125);play.textContent='Pause'}};showState();shelf.src=DATA.shelf;pair.src=DATA.pair;bay.value='5';const showMove=()=>move.src=DATA.moves[bay.value];bay.onchange=showMove;showMove();room8.src=DATA.roomV8;room9.src=DATA.roomV9;for(const row of DATA.rows){const tr=document.createElement('tr');tr.innerHTML=`<td>${row.name}</td><td>${row.measure}</td><td>${row.role}</td><td><code>${row.sha256}</code></td>`;rows.append(tr)}loading.textContent=`All ${urls.length} unique review images loaded and decoded. Controls enabled.`}
document.querySelectorAll('button,select').forEach(x=>x.disabled=true);Promise.all(urls.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed to load: ${e.message}`);
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()

    v5_catalogue = json.loads((V5_DRAFT / "asset-catalogue.json").read_text())
    v8_catalogue = json.loads((V8_DRAFT / "asset-catalogue.json").read_text())

    base = enriched_white_fridge()
    fridge_records = {}
    fridge_frames = {}
    for state in RECIPE["fridge"]["states"]:
        frames = [base] if state == "standard" else [render_effect(base, "obj_fridge", state, i) for i in range(4)]
        fridge_frames[state] = frames
        fps = 0 if state == "standard" else 8
        fridge_records[state] = save_strip(f"obj_fridge_{state}_f{len(frames)}", frames, (21, 21), fps, {
            "interactionSpotKu": v8_catalogue["assets"]["obj_fridge"]["interactionSpotKu"],
            "backWallFootLineLp": FOOT_LINE, "correction": "new-v9-dimensional-enamel-draft",
        })

    shelf = fridge_shelf()
    shelf_record = save_asset("obj_fridge_wall_shelf_v9_f1", shelf, (21, 56), {
        "anchor": [10.5, 0], "z": 26, "parent": "obj_fridge", "movesWithParent": True,
        "translationRule": "shelfDeltaLp == fridgeDeltaLp", "runtimeWiring": False,
    })
    pair_record = save_asset("obj_fridge_with_wall_shelf_review", pair_proof(base, shelf), (21, 56), {"reviewComposite": True})

    standards = {stem: v8_standard(stem, v8_catalogue) for stem in v8.ORDER}
    standards["obj_fridge"] = base
    rooms = {condition: save_asset(f"room_kitchen_9bay_{condition}", room_composite(standards, shelf, condition), (193, 56), {
        "reviewComposite": True, "condition": condition, "backWallFootLineLp": FOOT_LINE,
    }) for condition in v8.WEATHER}
    moves = {str(bay): save_asset(f"fridge_shelf_move_bay_{bay}", move_proof(base, shelf, bay), (193, 56), {
        "reviewComposite": True, "fridgeBay": bay, "shelfBay": bay,
    }) for bay in RECIPE["movementProofBays"]}

    comparisons = {}
    for state in RECIPE["fridge"]["states"]:
        v5_state = v5_catalogue["assets"]["obj_fridge"]["states"][state]
        v8_state = v8_catalogue["assets"]["obj_fridge"]["states"][state]
        v5_frames = load_strip(ROOT / v5_state["png"], v5_state["meta"])
        v8_frames = load_strip(ROOT / v8_state["png"], v8_state["meta"])
        v5_urls, v8_urls = [], []
        for label, frames, urls in (("v5", v5_frames, v5_urls), ("v8", v8_frames, v8_urls)):
            for index, frame in enumerate(frames):
                path = ASSETS / f"obj_fridge_{state}_{label}_frame{index + 1}.png"
                save_png(frame, path)
                urls.append(f"/keeper-review/kitchen-fridge-shelf-v9/assets/{path.name}")
        comparisons[state] = {"v5": v5_urls, "v8": v8_urls, "v9": fridge_records[state]["urls"]}

    v8_room = Image.open(V8_RAW / "room_kitchen_9bay_day.png").convert("RGBA")
    v8_room_path = ASSETS / "room_kitchen_9bay_v8_day.png"
    save_png(v8_room, v8_room_path)
    data = {
        "fridge": comparisons,
        "shelf": shelf_record["urls"][0], "pair": pair_record["urls"][0],
        "moves": {key: value["urls"][0] for key, value in moves.items()},
        "roomV8": f"/keeper-review/kitchen-fridge-shelf-v9/assets/{v8_room_path.name}",
        "roomV9": rooms["day"]["urls"][0],
        "rows": [
            {"name": "dimensional white fridge", "measure": "21×21-lp cell; one bay", "role": f"interaction {v8_catalogue['assets']['obj_fridge']['interactionSpotKu']} ku; foot line 52 lp", "sha256": fridge_records["standard"]["sha256"]},
            {"name": "plant-and-pots wall shelf", "measure": "21×56-lp cell; max 19×17 lp", "role": "fridge-owned z26 child; same horizontal delta", "sha256": shelf_record["sha256"]},
            {"name": "9-bay V9 kitchen", "measure": "193×56 lp", "role": "V8 room with only fridge and shelf changed", "sha256": rooms["day"]["sha256"]},
        ],
    }

    catalogue = {
        "version": 9, "status": "reversible-draft", "recipe": RECIPE["id"],
        "projection": RECIPE["projection"], "fridge": {"states": fridge_records, "largestBound": alpha_bound(base)},
        "fridgeShelf": {**shelf_record, "largestBound": alpha_bound(shelf)},
        "movementPlacementsLp": {str(bay): {"fridgeXLp": DOOR_DATUM + (bay - 1) * BAY, "shelfXLp": DOOR_DATUM + (bay - 1) * BAY} for bay in RECIPE["movementProofBays"]},
        "rooms": rooms,
    }
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)

    source_files = sorted(path for path in SOURCE.iterdir() if path.is_file())
    outputs = sorted(path for path in RAW.iterdir() if path.is_file()) + sorted(DRAFT.glob("*.json")) + source_files + [PUBLIC / "index.html"]
    register = {
        "version": 9, "status": "reversible-draft", "scope": "dimensional-white-fridge-and-fridge-owned-wall-shelf",
        "visualBaseline": RECIPE["visualBaseline"],
        "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)},
        "runtimeChanged": False, "finalChanged": False, "keeperChanged": False,
        "v8Overwritten": False,
        "protectedSnapshots": {
            "kitchenV8": tree_sha(V8_RAW), "kitchenRoomV7": tree_sha(V7_RAW),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
        "outputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs],
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"set": "kitchen-fridge-shelf-v9", "fridgeStates": len(fridge_records), "shelfBound": alpha_bound(shelf), "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
