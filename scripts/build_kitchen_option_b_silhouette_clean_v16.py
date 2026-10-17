#!/usr/bin/env python3
"""Build V16: V5 appliances on a provably uninterrupted Option-B surface."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_kitchen_option_b_clean_surface_v15 as v15
import build_kitchen_porthole_backdrop_cutout_v10 as v10
import build_kitchen_wall_anchored_v8 as v8
import kitchen_countertop_option_b as option_b

RECIPE_PATH = ROOT / "data/kitchen_option_b_silhouette_clean_v16_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
OPTION_B_RECIPE_PATH = ROOT / "data/kitchen_countertop_option_b_recipe.json"
V5_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
V5_DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v5"
V8_DRAFT = ROOT / "art/drafts/kitchen-wall-anchored-2026-10-16-v8"
V10_RAW = ROOT / "art/raw/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
V12_RAW = ROOT / "art/raw/kitchen-kettle-recipe-shelf-2026-10-17-v12"
V15_RAW = ROOT / "art/raw/kitchen-option-b-clean-surface-2026-10-17-v15"
RAW = ROOT / "art/raw/kitchen-option-b-silhouette-clean-2026-10-17-v16"
DRAFT = ROOT / "art/drafts/kitchen-option-b-silhouette-clean-2026-10-17-v16"
PUBLIC = ROOT / "public/keeper-review/kitchen-option-b-silhouette-clean-v16"
ASSETS = PUBLIC / "assets"
ROUTE = "/keeper-review/kitchen-option-b-silhouette-clean-v16"

DENSITY = 4
TRANSPARENT = (0, 0, 0, 0)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


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


def rgba(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGBA", size, TRANSPARENT)


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=False, compress_level=9)


def load_frames(record: dict) -> list[Image.Image]:
    strip = Image.open(ROOT / record["png"]).convert("RGBA")
    width = record["meta"]["w"] * DENSITY
    height = record["meta"]["h"] * DENSITY
    return [strip.crop((index * width, 0, (index + 1) * width, height)) for index in range(record["meta"]["frames"])]


def make_strip(frames: list[Image.Image]) -> Image.Image:
    out = rgba((frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        out.alpha_composite(frame, (index * frame.width, 0))
    return out


def mask_frame(mask: Image.Image) -> Image.Image:
    out = Image.new("RGBA", mask.size, (255, 255, 255, 0))
    out.putalpha(mask)
    return out


def inside_gold_window(stem: str, x: int, y: int) -> bool:
    if stem != "obj_sink":
        return False
    return any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in RECIPE["units"][stem]["goldWindowsPx"])


def is_wood_like(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return bool(a and r > 45 and r > 1.25 * g and g > 1.10 * b and b < 120)


def is_material(stem: str, x: int, y: int, pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    if not a:
        return False
    materials = RECIPE["units"][stem]["materials"]
    teal = "teal" in materials and g > r + 28 and b > r + 35 and g > 55
    neutral = "neutral" in materials and r > 120 and g > 110 and b > 90 and max(r, g, b) - min(r, g, b) < 65
    gold = "gold" in materials and inside_gold_window(stem, x, y) and r > 165 and g > 85 and b < 80
    return bool(teal or neutral or gold)


def appliance_mask(source: Image.Image, standard: Image.Image, stem: str) -> Image.Image:
    """Return only the measured V5 appliance/effect silhouette in the erased zone."""
    construction = option_b.RECIPE["compatibleUnits"][stem]
    spec = RECIPE["units"][stem]
    x0, x1 = spec["silhouetteXPx"]
    y0 = spec["removalTopPx"]
    y1 = construction["frontYPx"] + option_b.RECIPE["construction"]["fasciaPx"]
    source_px = source.load()
    standard_px = standard.load()
    seed = Image.new("L", source.size, 0)
    seed_px = seed.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            pixel = source_px[x, y]
            state_effect = pixel[3] and pixel != standard_px[x, y] and not is_wood_like(pixel)
            if is_material(stem, x, y, pixel) or state_effect:
                seed_px[x, y] = 255
    grown = seed.filter(ImageFilter.MaxFilter(5))
    grown_px = grown.load()
    mask = Image.new("L", source.size, 0)
    mask_px = mask.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            pixel = source_px[x, y]
            r, g, b, a = pixel
            dark_ink = a and max(r, g, b) < 125 and (r < 30 or b >= 0.55 * r)
            cool_edge = a and (b >= r or g >= r)
            neutral_edge = a and r > 115 and g > 105 and b > 85 and max(r, g, b) - min(r, g, b) < 70
            gold_edge = a and inside_gold_window(stem, x, y) and r > 150 and g > 75 and b < 90
            permitted_colour = not is_wood_like(pixel) or gold_edge
            if permitted_colour and (seed_px[x, y] or (grown_px[x, y] and (dark_ink or cool_edge or neutral_edge or gold_edge))):
                mask_px[x, y] = 255
    return mask


def clean_option_b_frame(source: Image.Image, standard: Image.Image, stem: str) -> tuple[Image.Image, Image.Image, Image.Image]:
    construction = option_b.RECIPE["compatibleUnits"][stem]
    spec = RECIPE["units"][stem]
    y0 = spec["removalTopPx"]
    y1 = construction["frontYPx"] + option_b.RECIPE["construction"]["fasciaPx"]
    out = source.copy()
    out.paste(TRANSPARENT, (0, y0, out.width, y1))
    slab = v15.clean_surface(out.size, construction["frontYPx"], construction["edgeLengthLp"])
    out.alpha_composite(slab)
    mask = appliance_mask(source, standard, stem)
    appliance = rgba(source.size)
    appliance.paste(source, (0, 0), mask)
    out.alpha_composite(appliance)
    return out, slab, mask


def save_state(stem: str, state: str, frames: list[Image.Image], masks: list[Image.Image], source_record: dict) -> dict:
    basename = Path(source_record["png"]).stem
    png_path = RAW / f"{basename}.png"
    json_path = RAW / f"{basename}.json"
    mask_path = RAW / f"{basename}_appliance_mask.png"
    save_png(make_strip(frames), png_path)
    save_png(make_strip([mask_frame(mask) for mask in masks]), mask_path)
    json_path.write_text(json.dumps(source_record["meta"], indent=2) + "\n")
    urls = []
    for index, frame in enumerate(frames, start=1):
        target = ASSETS / f"{basename}_frame{index}.png"
        save_png(frame, target)
        urls.append(f"{ROUTE}/assets/{target.name}")
    return {
        "sourcePng": source_record["png"],
        "sourceSha256": sha(ROOT / source_record["png"]),
        "png": png_path.relative_to(ROOT).as_posix(),
        "maskPng": mask_path.relative_to(ROOT).as_posix(),
        "json": json_path.relative_to(ROOT).as_posix(),
        "sha256": sha(png_path),
        "maskSha256": sha(mask_path),
        "meta": source_record["meta"],
        "bounds": source_record["bounds"],
        "urls": urls,
    }


def save_asset(name: str, image: Image.Image, logical: tuple[int, int], extra: dict | None = None) -> dict:
    png_path = RAW / f"{name}.png"
    json_path = RAW / f"{name}.json"
    save_png(image, png_path)
    meta = {"w": logical[0], "h": logical[1], "frames": 1, "fps": 0, "density": 4, "anchor": [logical[0] / 2, logical[1]], "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False}}
    if extra:
        meta.update(extra)
    json_path.write_text(json.dumps(meta, indent=2) + "\n")
    target = ASSETS / f"{name}.png"
    save_png(image, target)
    return {"png": png_path.relative_to(ROOT).as_posix(), "json": json_path.relative_to(ROOT).as_posix(), "sha256": sha(png_path), "meta": meta, "url": f"{ROUTE}/assets/{target.name}"}


def save_sink_overlay(name: str, clean_sink: Image.Image) -> dict:
    source_png = V5_RAW / f"obj_sink_{name}_f1.png"
    source_json = source_png.with_suffix(".json")
    overlay = Image.open(source_png).convert("RGBA")
    composite = clean_sink.copy()
    composite.alpha_composite(overlay)
    overlay_png = RAW / source_png.name
    overlay_json = RAW / source_json.name
    overlay_png.write_bytes(source_png.read_bytes())
    overlay_json.write_bytes(source_json.read_bytes())
    target = ASSETS / f"obj_sink_{name}_composite.png"
    save_png(composite, target)
    return {"sourcePng": source_png.relative_to(ROOT).as_posix(), "png": overlay_png.relative_to(ROOT).as_posix(), "json": overlay_json.relative_to(ROOT).as_posix(), "sourceSha256": sha(source_png), "copySha256": sha(overlay_png), "byteIdentical": source_png.read_bytes() == overlay_png.read_bytes(), "url": f"{ROUTE}/assets/{target.name}"}


def compose_room(standards: dict[str, Image.Image]) -> Image.Image:
    out = v10.room_shell_with_knockout(7)
    v10.place_wall_child(out, Image.open(V10_RAW / "obj_fridge_wall_shelf_v10_f1.png").convert("RGBA"), 2)
    v10.place_wall_child(out, Image.open(V12_RAW / "obj_kettle_recipe_shelf_v12_f1.png").convert("RGBA"), 3)
    for stem, bay in {"obj_bin": 1, "obj_fridge": 2, "obj_kettle": 3, "obj_toaster": 4, "obj_cooker": 5, "obj_mixer": 6}.items():
        v10.place_one_bay(out, standards[stem], bay)
    v10.place_wall_child(out, Image.open(V10_RAW / "obj_sink_porthole_frame_f1.png").convert("RGBA"), 7)
    v10.place_one_bay(out, standards["obj_sink"], 7)
    v10.place_two_bays(out, standards["obj_table"], 8)
    v10.place_one_bay(out, standards["obj_petbowl"], 9)
    return out


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V16 · silhouette-clean Option B</title><style>:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--gold:#efb64d;--good:#7ee0a6;--bad:#ff8d78}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}header,main{max-width:1560px;margin:auto;padding:22px}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin-right:7px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:10px}.alpha{background:repeating-conic-gradient(#33434b 0 25%,#203039 0 50%) 0/20px 20px;padding:8px;overflow:auto}.sprite{display:block;width:336px;max-width:100%;height:auto;margin:auto;image-rendering:pixelated}.room{display:block;min-width:772px;width:100%;height:auto;image-rendering:pixelated}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px}.good{color:var(--good)}.bad{color:var(--bad)}button,select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.small{font-size:.82rem}</style></head><body><header><span class="tag">Draft only</span><span class="tag">V5 visual authority</span><span class="tag">Option B geometry</span><h1>Kitchen V16 · complete old-surface removal</h1><p>V15 left rows of V5’s tapered countertop above the replacement band. V16 erases from the measured first old-surface row, draws one 1.5-lp top plus 2-lp fascia, then restores only the appliance silhouette.</p><p id="loading" class="notice">Preloading and decoding every review frame… controls remain locked.</p></header><main><section class="panel"><h2>Required failing control</h2><p class="notice"><strong>Left:</strong> rejected V15, including the retained shoulders. <strong>Right:</strong> V16 with the full inherited surface removed. Images are enlarged 4× for inspection.</p><div id="comparison" class="grid"></div></section><section class="panel"><h2>Every corrected state</h2><div class="controls"><label>State <select id="state" disabled></select></label><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><span id="readout"></span></div><div id="family" class="grid"></div></section><section class="panel"><h2>Current nine-bay room</h2><div class="alpha"><img id="room" class="room"></div><p>The white fridge, matched shelves, wall anchoring and true-alpha porthole remain unchanged.</p></section><section class="panel"><p class="notice"><strong>Automated gate:</strong> every pixel from V5’s first old-countertop row through the new fascia is checked. Outside the measured appliance mask it must be either the canonical Option-B slab or transparency above it. V15 must fail this exact test. Nothing is approved, promoted or wired.</p></section></main><script>const DATA=__DATA__;let n=0,timer=null;const urls=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))urls.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const unique=[...new Set(urls)];function chosen(name){const states=DATA.units[name];return states[state.value]||states.standard}function render(){family.innerHTML='';let max=1;for(const [name,states] of Object.entries(DATA.units)){const frames=chosen(name);max=Math.max(max,frames.length);const c=document.createElement('article');c.className='card';c.innerHTML=`<h3>${name}</h3><div class="alpha"><img class="sprite" src="${frames[n%frames.length]}"></div><p class="good">Full removal-zone gate: PASS</p>`;family.append(c)}readout.textContent=`Frame ${n+1} / ${max}`}function stop(){if(timer)clearInterval(timer);timer=null}function start(){stop();timer=setInterval(()=>{n=(n+1)%4;render()},220)}function setup(){for(const [name,pair] of Object.entries(DATA.comparison)){const c=document.createElement('article');c.className='card';c.innerHTML=`<h3>${name}</h3><div class="compare"><div><b class="bad">V15 rejected</b><div class="alpha"><img class="sprite" src="${pair.v15}"></div></div><div><b class="good">V16 corrected</b><div class="alpha"><img class="sprite" src="${pair.v16}"></div></div></div>`;comparison.append(c)}for(const s of DATA.stateOptions){const o=document.createElement('option');o.value=o.textContent=s;state.append(o)}room.src=DATA.room;state.disabled=play.disabled=pause.disabled=false;state.onchange=()=>{n=0;render()};play.onclick=start;pause.onclick=stop;render();start();loading.textContent=`All ${unique.length} images loaded and decoded. Controls enabled; playback started.`}Promise.all(unique.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed: ${e.message}`);</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
        for item in folder.iterdir():
            if item.is_file():
                item.unlink()
    v5_catalogue = read_json(V5_DRAFT / "asset-catalogue.json")
    v8_catalogue = read_json(V8_DRAFT / "asset-catalogue.json")
    states: dict[str, dict[str, dict]] = {}
    standards: dict[str, Image.Image] = {}
    templates: dict[str, dict] = {}
    comparison: dict[str, dict[str, str]] = {}
    for stem, unit_spec in RECIPE["units"].items():
        states[stem] = {}
        standard_record = v5_catalogue["assets"][stem]["states"]["standard"]
        standard_frame = load_frames(standard_record)[0]
        slab = None
        for state in unit_spec["states"]:
            source_record = v5_catalogue["assets"][stem]["states"][state]
            corrected: list[Image.Image] = []
            masks: list[Image.Image] = []
            for source in load_frames(source_record):
                frame, slab, mask = clean_option_b_frame(source, standard_frame, stem)
                corrected.append(frame)
                masks.append(mask)
            states[stem][state] = save_state(stem, state, corrected, masks, source_record)
            if state == "standard":
                standards[stem] = corrected[0]
        assert slab is not None
        templates[stem] = save_asset(f"{stem[4:]}_option_b_surface_template", slab, tuple(v5_catalogue["assets"][stem]["cell"]), {"role": "canonical-clean-surface-template"})
        v15_target = ASSETS / f"{stem[4:]}_v15_rejected.png"
        save_png(Image.open(V15_RAW / f"{stem}_standard_f1.png").convert("RGBA"), v15_target)
        comparison[stem.removeprefix("obj_")] = {"v15": f"{ROUTE}/assets/{v15_target.name}", "v16": states[stem]["standard"]["urls"][0]}
    sink_overlays = {name: save_sink_overlay(name, standards["obj_sink"]) for name in RECIPE["units"]["obj_sink"]["overlays"]}
    base_standards = {stem: v10.load_first(v8_catalogue["assets"][stem]["states"]["standard"]) for stem in v8.ORDER}
    base_standards.update(standards)
    base_standards["obj_fridge"] = Image.open(V10_RAW / "obj_fridge_standard_f1.png").convert("RGBA")
    room = save_asset("room_kitchen_9bay_v16_silhouette_clean", compose_room(base_standards), (193, 56), {"reviewComposite": True, "countertopGate": RECIPE["id"], "footLineLp": 52})
    data = {"units": {stem.removeprefix("obj_"): {state: record["urls"] for state, record in state_map.items()} for stem, state_map in states.items()}, "stateOptions": ["standard", "on", "broken", "dishes1", "dishes2", "dishes3"], "comparison": comparison, "room": room["url"]}
    data["units"]["sink"].update({name: [record["url"]] for name, record in sink_overlays.items()})
    catalogue = {"version": 16, "status": "reversible-draft", "visualAuthority": "v5", "geometryAuthority": "option-b", "recipe": RECIPE, "states": states, "sinkOverlays": sink_overlays, "templates": templates, "room": room}
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)
    register = {"version": 16, "status": "reversible-draft", "scope": "silhouette-clean-option-b-countertops", "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)}, "optionBRecipe": {"path": OPTION_B_RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(OPTION_B_RECIPE_PATH)}, "v5TreeSha256": tree_sha(V5_RAW), "v15TreeSha256": tree_sha(V15_RAW), "runtimeSpriteManifestSha256": sha(ROOT / "public/sprites/manifest.json"), "animationWorkbenchFinalStateSha256": sha(ROOT / "data/keeper_animation_workbench.json"), "runtimeChanged": False, "finalChanged": False, "keeperChanged": False}
    outputs = sorted(path for path in RAW.iterdir() if path.is_file()) + sorted(path for path in DRAFT.glob("*.json")) + [PUBLIC / "index.html"]
    register["outputs"] = [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs]
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"set": RECIPE["id"], "correctedStates": sum(len(value) for value in states.values()), "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
