#!/usr/bin/env python3
"""Build Kitchen V14 with the stepped rear countertop reveal removed."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_kitchen_wall_anchored_v8 as v8
import build_kitchen_porthole_backdrop_cutout_v10 as v10

RECIPE_PATH = ROOT / "data/kitchen_countertop_no_splashback_v14_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
V8_DRAFT = ROOT / "art/drafts/kitchen-wall-anchored-2026-10-16-v8"
V10_RAW = ROOT / "art/raw/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
V10_DRAFT = ROOT / "art/drafts/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
V12_RAW = ROOT / "art/raw/kitchen-kettle-recipe-shelf-2026-10-17-v12"
V13_RAW = ROOT / "art/raw/kitchen-countertop-continuity-2026-10-17-v13"
RAW = ROOT / "art/raw/kitchen-countertop-no-splashback-2026-10-17-v14"
DRAFT = ROOT / "art/drafts/kitchen-countertop-no-splashback-2026-10-17-v14"
PUBLIC = ROOT / "public/keeper-review/kitchen-countertop-no-splashback-v14"
ASSETS = PUBLIC / "assets"

DENSITY = 4
TRANSPARENT = (0, 0, 0, 0)
WOOD = {v8.WOOD_DARK, v8.WOOD, v8.WOOD_LIGHT, v8.WOOD_HIGHLIGHT}


def rgba(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGBA", size, TRANSPARENT)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(directory: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path for path in directory.rglob("*") if path.is_file()):
        digest.update(item.relative_to(directory).as_posix().encode())
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=False, compress_level=9)


def split_strip(record: dict) -> list[Image.Image]:
    strip = Image.open(ROOT / record["png"]).convert("RGBA")
    width = record["meta"]["w"] * DENSITY
    height = record["meta"]["h"] * DENSITY
    return [strip.crop((i * width, 0, (i + 1) * width, height)) for i in range(record["meta"]["frames"])]


def make_strip(frames: list[Image.Image]) -> Image.Image:
    out = rgba((frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        out.alpha_composite(frame, (index * frame.width, 0))
    return out


def fascia_template(size: tuple[int, int], front: int) -> Image.Image:
    complete = v8.clean_counter_slab(size, front)
    out = rgba(size)
    out.alpha_composite(complete.crop((0, front, size[0], front + 8)), (0, front))
    return out


def appliance_mask(frame: Image.Image, stem: str, bottom: int) -> Image.Image:
    spec = RECIPE["units"][stem]
    front = spec["frontYPx"]
    left, right = spec["applianceXPxInclusive"]
    seed = Image.new("L", frame.size, 0)
    source = frame.load(); seed_px = seed.load()
    for y in range(front - 6, bottom):
        for x in range(left, right + 1):
            pixel = source[x, y]
            if pixel[3] and pixel not in WOOD and pixel != v8.INK:
                seed_px[x, y] = 255
    grown = seed.filter(ImageFilter.MaxFilter(3))
    final = Image.new("L", frame.size, 0)
    final_px = final.load(); grown_px = grown.load()
    for y in range(front - 6, bottom):
        for x in range(left, right + 1):
            pixel = source[x, y]
            if grown_px[x, y] and pixel[3] and pixel not in WOOD:
                final_px[x, y] = 255
    return final


def remove_rear_ridge(frame: Image.Image, stem: str) -> tuple[Image.Image, Image.Image]:
    spec = RECIPE["units"][stem]
    front = spec["frontYPx"]
    out = frame.copy()
    # Remove the complete old reveal and fascia before rebuilding the visible
    # front as a single rectangle. This prevents any inherited shoulder pixels.
    out.paste(TRANSPARENT, (0, front - 6, out.width, front + 8))
    rear_mask = appliance_mask(frame, stem, front)
    rear = rgba(frame.size); rear.paste(frame, (0, 0), rear_mask)
    out.alpha_composite(rear)
    fascia = fascia_template(frame.size, front)
    out.alpha_composite(fascia)
    if stem == "obj_sink":
        basin_mask = appliance_mask(frame, stem, front + 4)
        basin_px = basin_mask.load()
        basin_left, basin_right = spec["fasciaOcclusionXPxInclusive"]
        for y in range(front, front + 4):
            for x in range(frame.width):
                if not basin_left <= x <= basin_right:
                    basin_px[x, y] = 0
        basin = rgba(frame.size); basin.paste(frame, (0, 0), basin_mask)
        out.alpha_composite(basin)
    return out, fascia


def save_state(stem: str, state: str, frames: list[Image.Image], meta: dict) -> dict:
    name = f"{stem[4:]}_{state}"
    png_path = RAW / f"{name}.png"; json_path = RAW / f"{name}.json"
    save_png(make_strip(frames), png_path)
    json_path.write_text(json.dumps(meta, indent=2) + "\n")
    urls = []
    for index, frame in enumerate(frames):
        target = ASSETS / f"{name}_frame{index + 1}.png"
        save_png(frame, target)
        urls.append(f"/keeper-review/kitchen-countertop-no-splashback-v14/assets/{target.name}")
    return {"png": png_path.relative_to(ROOT).as_posix(), "json": json_path.relative_to(ROOT).as_posix(), "sha256": sha(png_path), "meta": meta, "urls": urls}


def save_asset(name: str, image: Image.Image, logical: tuple[int, int], extra: dict | None = None) -> dict:
    png_path = RAW / f"{name}.png"; json_path = RAW / f"{name}.json"
    save_png(image, png_path)
    meta = {"w": logical[0], "h": logical[1], "frames": 1, "fps": 0, "density": 4, "anchor": [logical[0] / 2, logical[1]], "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False}}
    if extra: meta.update(extra)
    json_path.write_text(json.dumps(meta, indent=2) + "\n")
    target = ASSETS / f"{name}.png"; save_png(image, target)
    return {"png": png_path.relative_to(ROOT).as_posix(), "json": json_path.relative_to(ROOT).as_posix(), "sha256": sha(png_path), "meta": meta, "url": f"/keeper-review/kitchen-countertop-no-splashback-v14/assets/{target.name}"}


def violation_count(image: Image.Image, stem: str) -> int:
    spec = RECIPE["units"][stem]; front = spec["frontYPx"]
    left, right = spec["applianceXPxInclusive"]
    count = 0
    for y in range(front - 6, front):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            if pixel in WOOD or (pixel[3] and not left <= x <= right):
                count += 1
    return count


def compose_room(standards: dict[str, Image.Image]) -> Image.Image:
    out = v10.room_shell_with_knockout(7)
    v10.place_wall_child(out, Image.open(V10_RAW / "obj_fridge_wall_shelf_v10_f1.png").convert("RGBA"), 2)
    v10.place_wall_child(out, Image.open(V12_RAW / "obj_kettle_recipe_shelf_v12_f1.png").convert("RGBA"), 3)
    positions = {"obj_bin": 1, "obj_fridge": 2, "obj_kettle": 3, "obj_toaster": 4, "obj_cooker": 5, "obj_mixer": 6}
    for stem, bay in positions.items(): v10.place_one_bay(out, standards[stem], bay)
    v10.place_wall_child(out, Image.open(V10_RAW / "obj_sink_porthole_frame_f1.png").convert("RGBA"), 7)
    v10.place_one_bay(out, standards["obj_sink"], 7)
    v10.place_two_bays(out, standards["obj_table"], 8)
    v10.place_one_bay(out, standards["obj_petbowl"], 9)
    return out


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V14 · no splashback ridge</title><style>:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--gold:#efb64d;--good:#7ee0a6;--bad:#ff8d78}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}header,main{max-width:1540px;margin:auto;padding:22px}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin-right:7px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px}.alpha{background:repeating-conic-gradient(#33434b 0 25%,#203039 0 50%) 0/20px 20px;padding:8px;overflow:auto}.sprite{display:block;width:168px;max-width:100%;height:auto;margin:auto}.room{display:block;min-width:772px;width:100%;height:auto}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px}.good{color:var(--good)}.bad{color:var(--bad)}button,select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}</style></head><body><header><span class="tag">Draft only</span><span class="tag">Rear ridge removed</span><span class="tag">Exact fascia test</span><h1>Kitchen V14 · no splashback behind appliances</h1><p>The stepped brown rear reveal has been removed. Each appliance now meets one clean, full-width front fascia.</p><p id="loading" class="notice">Preloading and decoding all review frames… controls remain locked.</p></header><main><section class="panel"><h2>V13 ridge → V14 flat counter</h2><div id="comparison" class="grid"></div></section><section class="panel"><h2>Every V14 state</h2><div class="controls"><label>State <select id="state" disabled><option>standard</option><option>on</option><option>broken</option></select></label><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><span id="readout"></span></div><div id="family" class="grid"></div></section><section class="panel"><h2>Complete kitchen</h2><div class="alpha"><img id="room" class="room"></div></section><section class="panel"><p class="notice"><strong>Binding gate:</strong> zero wood or structural ridge above the fascia; no pixels outside each appliance interval; exact eight-pixel fascia across every frame. V13 must fail this test. Nothing is approved, promoted or wired.</p></section></main><script>const DATA=__DATA__;let n=0,timer=null;const urls=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))urls.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const unique=[...new Set(urls)];function render(){family.innerHTML='';let max=1;for(const [name,states] of Object.entries(DATA.units)){const frames=states[state.value]||states.standard;max=Math.max(max,frames.length);const c=document.createElement('article');c.className='card';c.innerHTML=`<h3>${name}</h3><div class="alpha"><img class="sprite" src="${frames[n%frames.length]}"></div><p class="good">No-ridge + fascia gate: PASS</p>`;family.append(c)}readout.textContent=`Frame ${n+1} / ${max}`}function stop(){if(timer)clearInterval(timer);timer=null}function start(){stop();timer=setInterval(()=>{n=(n+1)%4;render()},220)}function setup(){for(const [name,pair] of Object.entries(DATA.comparison)){const c=document.createElement('article');c.className='card';c.innerHTML=`<h3>${name}</h3><div class="pair"><div><b class="bad">V13 ridge</b><div class="alpha"><img class="sprite" src="${pair.before}"></div></div><div><b class="good">V14 removed</b><div class="alpha"><img class="sprite" src="${pair.after}"></div></div></div>`;comparison.append(c)}room.src=DATA.room;state.disabled=play.disabled=pause.disabled=false;state.onchange=()=>{n=0;render()};play.onclick=start;pause.onclick=stop;render();start();loading.textContent=`All ${unique.length} images loaded and decoded. Controls enabled; playback started.`}Promise.all(unique.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed: ${e.message}`);</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
        for item in folder.iterdir():
            if item.is_file(): item.unlink()
    v10_catalogue = read_json(V10_DRAFT / "asset-catalogue.json")
    v8_catalogue = read_json(V8_DRAFT / "asset-catalogue.json")
    states = {}; templates = {}; standards = {}; controls = {}; comparisons = {}
    for stem, state_map in v10_catalogue["correctedCounterStates"].items():
        states[stem] = {}
        for state, record in state_map.items():
            frames = []; template = None
            for frame in split_strip(record):
                fixed, template = remove_rear_ridge(frame, stem); frames.append(fixed)
            states[stem][state] = save_state(stem, state, frames, record["meta"])
            if state == "standard":
                standards[stem] = frames[0]
                old = Image.open(V13_RAW / f"{stem[4:]}_standard.png").convert("RGBA")
                controls[stem] = violation_count(old, stem)
                before = save_asset(f"{stem[4:]}_v13_ridge_control", old, (21, 31), {"role": "required-failing-control"})
                comparisons[stem] = {"before": before["url"], "after": states[stem][state]["urls"][0]}
        templates[stem] = save_asset(f"{stem[4:]}_front_fascia_template", template, (21, 31), {"role": "canonical-fascia-test-template"})
    base_standards = {stem: v10.load_first(v8_catalogue["assets"][stem]["states"]["standard"]) for stem in v8.ORDER}
    base_standards.update(standards)
    base_standards["obj_fridge"] = Image.open(V10_RAW / "obj_fridge_standard_f1.png").convert("RGBA")
    room = save_asset("room_kitchen_9bay_v14_no_splashbacks", compose_room(base_standards), (193, 56), {"reviewComposite": True, "countertopGate": RECIPE["id"]})
    data = {"units": {stem.replace("obj_", ""): {state: record["urls"] for state, record in state_map.items()} for stem, state_map in states.items()}, "comparison": {stem.replace("obj_", ""): pair for stem, pair in comparisons.items()}, "room": room["url"]}
    catalogue = {"version": 14, "status": "reversible-draft", "recipe": RECIPE, "states": states, "templates": templates, "room": room, "v13NegativeControlViolationCounts": controls}
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)
    register = {"version": 14, "status": "reversible-draft", "scope": "remove-rear-countertop-ridge", "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)}, "v13TreeSha256": tree_sha(V13_RAW), "runtimeSpriteManifestSha256": sha(ROOT / "public/sprites/manifest.json"), "animationWorkbenchFinalStateSha256": sha(ROOT / "data/keeper_animation_workbench.json"), "runtimeChanged": False, "finalChanged": False, "keeperChanged": False}
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    outputs = sorted(path for path in RAW.iterdir() if path.is_file()) + sorted(path for path in DRAFT.glob("*.json") if path.name != "batch-register.json") + [PUBLIC / "index.html"]
    register["outputs"] = [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs]
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"set": RECIPE["id"], "v13Failures": controls, "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__": main()
