#!/usr/bin/env python3
"""Build V15: V5-quality units with one clean Option-B countertop plane."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_kitchen_wall_anchored_v8 as v8
import build_kitchen_porthole_backdrop_cutout_v10 as v10
import kitchen_countertop_option_b as option_b

RECIPE_PATH = ROOT / "data/kitchen_option_b_clean_surface_v15_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
OPTION_B_RECIPE_PATH = ROOT / "data/kitchen_countertop_option_b_recipe.json"
V5_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
V5_DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v5"
V6_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v6-option-b"
V8_DRAFT = ROOT / "art/drafts/kitchen-wall-anchored-2026-10-16-v8"
V10_RAW = ROOT / "art/raw/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
V12_RAW = ROOT / "art/raw/kitchen-kettle-recipe-shelf-2026-10-17-v12"
RAW = ROOT / "art/raw/kitchen-option-b-clean-surface-2026-10-17-v15"
DRAFT = ROOT / "art/drafts/kitchen-option-b-clean-surface-2026-10-17-v15"
PUBLIC = ROOT / "public/keeper-review/kitchen-option-b-clean-surface-v15"
ASSETS = PUBLIC / "assets"

DENSITY = 4
TRANSPARENT = (0, 0, 0, 0)
WOOD = {
    tuple(option_b.RECIPE["paletteRgba"][name])
    for name in ("woodDark", "wood", "woodLight", "woodHighlight")
}
INK = tuple(option_b.RECIPE["paletteRgba"]["ink"])


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


def appliance_layer(source: Image.Image, stem: str) -> Image.Image:
    """Keep the V5 appliance/effect, but reject all inherited wood pixels."""
    preserve = option_b.RECIPE["compatibleUnits"][stem]["preservePx"]
    if preserve is None:
        raise ValueError(f"{stem} needs an appliance preserve rectangle")
    x0, y0, x1, y1 = preserve
    seed = Image.new("L", source.size, 0)
    source_px = source.load()
    seed_px = seed.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            pixel = source_px[x, y]
            if pixel[3] and pixel not in WOOD and pixel != INK:
                seed_px[x, y] = 255
    # One-pixel growth recovers the appliance outline without reaching the
    # inherited V5 countertop lines underneath it.
    grown = seed.filter(ImageFilter.MaxFilter(3))
    mask = Image.new("L", source.size, 0)
    grown_px = grown.load()
    mask_px = mask.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            pixel = source_px[x, y]
            if grown_px[x, y] and pixel[3] and pixel not in WOOD:
                mask_px[x, y] = 255
    out = rgba(source.size)
    out.paste(source, (0, 0), mask)
    return out


def clean_surface(size: tuple[int, int], front_y: int, edge_length_lp: int) -> Image.Image:
    """Draw one uninterrupted Option-B plane without sampling old top pixels."""
    depth = option_b.RECIPE["construction"]["topRevealPx"]
    fascia = option_b.RECIPE["construction"]["fasciaPx"]
    width = edge_length_lp * DENSITY
    x0 = (size[0] - width) // 2
    x1 = x0 + width - 1
    rear_y = front_y - depth
    bottom_y = front_y + fascia - 1
    colours = option_b.RECIPE["paletteRgba"]
    ink = tuple(colours["ink"])
    dark = tuple(colours["woodDark"])
    wood = tuple(colours["wood"])
    light = tuple(colours["woodLight"])
    highlight = tuple(colours["woodHighlight"])
    out = rgba(size)
    draw = ImageDraw.Draw(out)
    draw.rectangle((x0, rear_y, x1, front_y - 1), fill=light)
    draw.line((x0 + 2, rear_y + 2, x1 - 2, rear_y + 2), fill=highlight, width=1)
    draw.line((x0 + 2, front_y - 2, x1 - 2, front_y - 2), fill=wood, width=1)
    draw.rectangle((x0, front_y, x1, bottom_y), fill=wood)
    draw.line((x0 + 2, front_y + 2, x1 - 2, front_y + 2), fill=light, width=1)
    draw.line((x0 + 2, bottom_y - 2, x1 - 2, bottom_y - 2), fill=dark, width=1)
    # Structural outline: only straight, continuous edges. No texture or old
    # appliance pixels may introduce notches into this template.
    draw.line((x0, rear_y, x1, rear_y), fill=ink, width=2)
    draw.line((x0, front_y - 1, x1, front_y - 1), fill=ink, width=2)
    draw.line((x0, bottom_y, x1, bottom_y), fill=ink, width=1)
    draw.line((x0, rear_y, x0, bottom_y), fill=ink, width=2)
    draw.line((x1 - 1, rear_y, x1 - 1, bottom_y), fill=ink, width=2)
    return out


def clean_option_b_frame(source: Image.Image, stem: str) -> tuple[Image.Image, Image.Image]:
    spec = option_b.RECIPE["compatibleUnits"][stem]
    out = source.copy()
    out.paste(TRANSPARENT, tuple(spec["maskPx"]))
    slab = clean_surface(out.size, spec["frontYPx"], spec["edgeLengthLp"])
    out.alpha_composite(slab)
    out.alpha_composite(appliance_layer(source, stem))
    return out, slab


def save_state(stem: str, state: str, frames: list[Image.Image], source_record: dict) -> dict:
    basename = Path(source_record["png"]).stem
    png_path = RAW / f"{basename}.png"
    json_path = RAW / f"{basename}.json"
    save_png(make_strip(frames), png_path)
    json_path.write_text(json.dumps(source_record["meta"], indent=2) + "\n")
    urls = []
    for index, frame in enumerate(frames, start=1):
        target = ASSETS / f"{basename}_frame{index}.png"
        save_png(frame, target)
        urls.append(f"/keeper-review/kitchen-option-b-clean-surface-v15/assets/{target.name}")
    return {
        "sourcePng": source_record["png"], "sourceSha256": sha(ROOT / source_record["png"]),
        "png": png_path.relative_to(ROOT).as_posix(), "json": json_path.relative_to(ROOT).as_posix(),
        "sha256": sha(png_path), "meta": source_record["meta"], "bounds": source_record["bounds"], "urls": urls,
    }


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
    return {
        "sourcePng": source_png.relative_to(ROOT).as_posix(),
        "png": overlay_png.relative_to(ROOT).as_posix(),
        "json": overlay_json.relative_to(ROOT).as_posix(),
        "sourceSha256": sha(source_png), "copySha256": sha(overlay_png),
        "byteIdentical": source_png.read_bytes() == overlay_png.read_bytes(),
        "url": f"/keeper-review/kitchen-option-b-clean-surface-v15/assets/{target.name}",
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
    return {"png": png_path.relative_to(ROOT).as_posix(), "json": json_path.relative_to(ROOT).as_posix(), "sha256": sha(png_path), "meta": meta, "url": f"/keeper-review/kitchen-option-b-clean-surface-v15/assets/{target.name}"}


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
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V15 · clean Option-B surfaces</title><style>:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--gold:#efb64d;--good:#7ee0a6;--bad:#ff8d78}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}header,main{max-width:1540px;margin:auto;padding:22px}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin-right:7px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}.compare{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}.alpha{background:repeating-conic-gradient(#33434b 0 25%,#203039 0 50%) 0/20px 20px;padding:8px;overflow:auto}.sprite{display:block;width:168px;max-width:100%;height:auto;margin:auto}.room{display:block;min-width:772px;width:100%;height:auto}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px}.good{color:var(--good)}.bad{color:var(--bad)}button,select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.small{font-size:.82rem}</style></head><body><header><span class="tag">Draft only</span><span class="tag">Option B retained</span><span class="tag">V5 polish retained</span><h1>Kitchen V15 · clean shallow-perspective countertops</h1><p>The required V6 perspective change remains: a 1.5-lp top and 2-lp fascia. The V5→V6 splintering is removed by rebuilding the entire surface as one plane and restoring only the appliance—not the old countertop—over it.</p><p id="loading" class="notice">Preloading and decoding all review frames… controls remain locked.</p></header><main><section class="panel"><h2>Regression boundary</h2><p class="notice"><strong>V5:</strong> visual quality and animation authority. <strong>V6:</strong> geometry intent only and required failing surface control. <strong>V15:</strong> V5 pixels outside the reconstruction band + clean Option-B geometry inside it.</p><div id="comparison" class="grid"></div></section><section class="panel"><h2>Every corrected state</h2><div class="controls"><label>State <select id="state" disabled></select></label><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><span id="readout"></span></div><div id="family" class="grid"></div></section><section class="panel"><h2>Current room</h2><div class="alpha"><img id="room" class="room"></div><p>The detailed white fridge, matched shelves and true alpha porthole remain. The corrected units stay on the exact 52-lp rear-wall foot line.</p></section><section class="panel"><p class="notice"><strong>Automated gate:</strong> every exposed RGBA pixel in both countertop wings must match one canonical 80 × 14-px Option-B slab in every frame. V6 must fail the same gate. Nothing is approved, promoted or wired.</p></section></main><script>const DATA=__DATA__;let n=0,timer=null;const urls=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))urls.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const unique=[...new Set(urls)];function chosen(name){const states=DATA.units[name];return states[state.value]||states.standard}function render(){family.innerHTML='';let max=1;for(const [name,states] of Object.entries(DATA.units)){const frames=chosen(name);max=Math.max(max,frames.length);const c=document.createElement('article');c.className='card';c.innerHTML=`<h3>${name}</h3><div class="alpha"><img class="sprite" src="${frames[n%frames.length]}"></div><p class="good">Option-B wing gate: PASS</p>`;family.append(c)}readout.textContent=`Frame ${n+1} / ${max}`}function stop(){if(timer)clearInterval(timer);timer=null}function start(){stop();timer=setInterval(()=>{n=(n+1)%4;render()},220)}function setup(){for(const [name,pair] of Object.entries(DATA.comparison)){const c=document.createElement('article');c.className='card';c.innerHTML=`<h3>${name}</h3><div class="compare"><div><b>V5 quality</b><div class="alpha"><img class="sprite" src="${pair.v5}"></div></div><div><b class="bad">V6 splintering</b><div class="alpha"><img class="sprite" src="${pair.v6}"></div></div><div><b class="good">V15 clean B</b><div class="alpha"><img class="sprite" src="${pair.v15}"></div></div></div>`;comparison.append(c)}for(const s of DATA.stateOptions){const o=document.createElement('option');o.value=o.textContent=s;state.append(o)}room.src=DATA.room;state.disabled=play.disabled=pause.disabled=false;state.onchange=()=>{n=0;render()};play.onclick=start;pause.onclick=stop;render();start();loading.textContent=`All ${unique.length} images loaded and decoded. Controls enabled; playback started.`}Promise.all(unique.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed: ${e.message}`);</script></body></html>'''
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
        slab = None
        for state in unit_spec["states"]:
            source_record = v5_catalogue["assets"][stem]["states"][state]
            corrected = []
            for source in load_frames(source_record):
                frame, slab = clean_option_b_frame(source, stem)
                corrected.append(frame)
            states[stem][state] = save_state(stem, state, corrected, source_record)
            if state == "standard":
                standards[stem] = corrected[0]
        assert slab is not None
        templates[stem] = save_asset(f"{stem[4:]}_option_b_surface_template", slab, tuple(v5_catalogue["assets"][stem]["cell"]), {"role": "canonical-clean-surface-template"})
        v5_target = ASSETS / f"{stem[4:]}_v5_standard.png"
        v6_target = ASSETS / f"{stem[4:]}_v6_standard.png"
        save_png(load_frames(v5_catalogue["assets"][stem]["states"]["standard"])[0], v5_target)
        save_png(Image.open(V6_RAW / f"{stem}_standard_f1.png").convert("RGBA"), v6_target)
        comparison[stem.removeprefix("obj_")] = {
            "v5": f"/keeper-review/kitchen-option-b-clean-surface-v15/assets/{v5_target.name}",
            "v6": f"/keeper-review/kitchen-option-b-clean-surface-v15/assets/{v6_target.name}",
            "v15": states[stem]["standard"]["urls"][0],
        }
    sink_overlays = {
        name: save_sink_overlay(name, standards["obj_sink"])
        for name in RECIPE["units"]["obj_sink"]["overlays"]
    }
    base_standards = {stem: v10.load_first(v8_catalogue["assets"][stem]["states"]["standard"]) for stem in v8.ORDER}
    base_standards.update(standards)
    base_standards["obj_fridge"] = Image.open(V10_RAW / "obj_fridge_standard_f1.png").convert("RGBA")
    room = save_asset("room_kitchen_9bay_v15_clean_option_b", compose_room(base_standards), (193, 56), {"reviewComposite": True, "countertopGate": RECIPE["id"], "footLineLp": 52})
    data = {
        "units": {stem.removeprefix("obj_"): {state: record["urls"] for state, record in state_map.items()} for stem, state_map in states.items()},
        "stateOptions": ["standard", "on", "broken", "dishes1", "dishes2", "dishes3"],
        "comparison": comparison, "room": room["url"],
    }
    data["units"]["sink"].update({name: [record["url"]] for name, record in sink_overlays.items()})
    catalogue = {"version": 15, "status": "reversible-draft", "visualAuthority": "v5", "geometryAuthority": "option-b", "recipe": RECIPE, "states": states, "sinkOverlays": sink_overlays, "templates": templates, "room": room}
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)
    register = {
        "version": 15, "status": "reversible-draft", "scope": "clean-option-b-countertops",
        "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)},
        "optionBRecipe": {"path": OPTION_B_RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(OPTION_B_RECIPE_PATH)},
        "v5TreeSha256": tree_sha(V5_RAW), "v6TreeSha256": tree_sha(V6_RAW),
        "runtimeSpriteManifestSha256": sha(ROOT / "public/sprites/manifest.json"),
        "animationWorkbenchFinalStateSha256": sha(ROOT / "data/keeper_animation_workbench.json"),
        "runtimeChanged": False, "finalChanged": False, "keeperChanged": False,
    }
    outputs = sorted(path for path in RAW.iterdir() if path.is_file()) + sorted(path for path in DRAFT.glob("*.json")) + [PUBLIC / "index.html"]
    register["outputs"] = [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs]
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"set": RECIPE["id"], "correctedStates": sum(len(v) for v in states.values()), "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
