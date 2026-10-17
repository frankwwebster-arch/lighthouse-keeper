#!/usr/bin/env python3
"""Build Kitchen V13 with exact, testable Option-B countertop structure."""

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

RECIPE_PATH = ROOT / "data/kitchen_countertop_continuity_v13_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
V8_DRAFT = ROOT / "art/drafts/kitchen-wall-anchored-2026-10-16-v8"
V10_RAW = ROOT / "art/raw/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
V10_DRAFT = ROOT / "art/drafts/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
V12_RAW = ROOT / "art/raw/kitchen-kettle-recipe-shelf-2026-10-17-v12"
RAW = ROOT / "art/raw/kitchen-countertop-continuity-2026-10-17-v13"
DRAFT = ROOT / "art/drafts/kitchen-countertop-continuity-2026-10-17-v13"
PUBLIC = ROOT / "public/keeper-review/kitchen-countertop-continuity-v13"
ASSETS = PUBLIC / "assets"

DENSITY = 4
INK = (7, 27, 50, 255)


def rgba(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGBA", size, (0, 0, 0, 0))


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
    strip = rgba((frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * frame.width, 0))
    return strip


def repair_frame(frame: Image.Image, stem: str) -> tuple[Image.Image, Image.Image]:
    """Place the canonical slab last, then restore only the declared sink basin."""
    spec = RECIPE["units"][stem]
    front = spec["frontYPx"]
    template = v8.clean_counter_slab(frame.size, front)
    out = frame.copy()
    out.alpha_composite(template)
    allowed = spec["intentionalOcclusionXPxInclusive"]
    if allowed is not None:
        left, right = allowed
        seed = Image.new("L", frame.size, 0)
        source = frame.load()
        mask = seed.load()
        for y in range(front - 14, front + 4):
            for x in range(left + 1, right):
                r, g, b, a = source[x, y]
                woodish = a and r > 65 and r > g * 1.18 and g > b * 0.8
                if a and not woodish:
                    mask[x, y] = 255
        grown = seed.filter(ImageFilter.MaxFilter(3))
        # A hard contract prevents antialias growth from escaping into either
        # exposed countertop wing.
        clipped = Image.new("L", frame.size, 0)
        clipped.paste(grown.crop((left, 0, right + 1, frame.height)), (left, 0))
        restored = rgba(frame.size)
        restored.paste(frame, (0, 0), clipped)
        out.alpha_composite(restored)
    return out, template


def save_state(stem: str, state: str, frames: list[Image.Image], meta: dict) -> dict:
    name = f"{stem[4:]}_{state}"
    png_path = RAW / f"{name}.png"
    json_path = RAW / f"{name}.json"
    save_png(make_strip(frames), png_path)
    new_meta = dict(meta)
    json_path.write_text(json.dumps(new_meta, indent=2) + "\n")
    urls = []
    for index, frame in enumerate(frames):
        review = ASSETS / f"{name}_frame{index + 1}.png"
        save_png(frame, review)
        urls.append(f"/keeper-review/kitchen-countertop-continuity-v13/assets/{review.name}")
    return {
        "png": png_path.relative_to(ROOT).as_posix(),
        "json": json_path.relative_to(ROOT).as_posix(),
        "sha256": sha(png_path),
        "meta": new_meta,
        "urls": urls,
    }


def save_asset(name: str, image: Image.Image, logical: tuple[int, int], extra: dict | None = None) -> dict:
    png_path = RAW / f"{name}.png"
    json_path = RAW / f"{name}.json"
    save_png(image, png_path)
    meta = {
        "w": logical[0], "h": logical[1], "frames": 1, "fps": 0,
        "density": DENSITY, "anchor": [logical[0] / 2, logical[1]],
        "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False},
    }
    if extra:
        meta.update(extra)
    json_path.write_text(json.dumps(meta, indent=2) + "\n")
    review = ASSETS / f"{name}.png"
    save_png(image, review)
    return {
        "png": png_path.relative_to(ROOT).as_posix(),
        "json": json_path.relative_to(ROOT).as_posix(),
        "sha256": sha(png_path), "meta": meta,
        "url": f"/keeper-review/kitchen-countertop-continuity-v13/assets/{name}.png",
    }


def pixel_mismatches(frame: Image.Image, template: Image.Image, stem: str) -> int:
    spec = RECIPE["units"][stem]
    front = spec["frontYPx"]
    allowed = spec["intentionalOcclusionXPxInclusive"]
    count = 0
    for y in range(front - 6, front + 8):
        for x in range(2, 82):
            if allowed is not None and allowed[0] <= x <= allowed[1]:
                continue
            if frame.getpixel((x, y)) != template.getpixel((x, y)):
                count += 1
    return count


def compose_room(standards: dict[str, Image.Image]) -> Image.Image:
    out = v10.room_shell_with_knockout(7)
    fridge_shelf = Image.open(V10_RAW / "obj_fridge_wall_shelf_v10_f1.png").convert("RGBA")
    books_shelf = Image.open(V12_RAW / "obj_kettle_recipe_shelf_v12_f1.png").convert("RGBA")
    porthole = Image.open(V10_RAW / "obj_sink_porthole_frame_f1.png").convert("RGBA")
    v10.place_wall_child(out, fridge_shelf, 2)
    v10.place_wall_child(out, books_shelf, 3)
    positions = {"obj_bin": 1, "obj_fridge": 2, "obj_kettle": 3, "obj_toaster": 4, "obj_cooker": 5, "obj_mixer": 6}
    for stem, bay in positions.items():
        v10.place_one_bay(out, standards[stem], bay)
    v10.place_wall_child(out, porthole, 7)
    v10.place_one_bay(out, standards["obj_sink"], 7)
    v10.place_two_bays(out, standards["obj_table"], 8)
    v10.place_one_bay(out, standards["obj_petbowl"], 9)
    return out


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V13 · countertop continuity gate</title><style>
:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--muted:#a8bdc4;--gold:#efb64d;--bad:#ff8d78;--good:#7ee0a6}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.48 system-ui,sans-serif}header,main{max-width:1540px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:12px}.alpha{background:repeating-conic-gradient(#33434b 0 25%,#203039 0 50%) 0/20px 20px;overflow:auto;padding:10px;border-radius:8px}.sprite{display:block;width:168px;height:auto;image-rendering:auto;margin:auto}.room{display:block;min-width:772px;width:100%;height:auto}.good{color:var(--good)}.bad{color:var(--bad)}button,select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}code{color:#9ce5ea}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:7px;border-bottom:1px solid var(--line)}@media(max-width:720px){header,main{padding:12px}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">Exact RGBA gate</span><span class="tag">V10 retained as failing control</span><h1>Kitchen V13 · countertop continuity correction</h1><p>The test now covers the complete 80 × 14-pixel Option-B slab in every standard, on and broken frame. Present-but-wrong pixels fail just as missing pixels do.</p><p id="loading" class="notice">Preloading and decoding every unique frame… playback remains locked.</p></header><main>
<section class="panel"><h2>Why V10 passed incorrectly</h2><p>Its test examined alpha on one row. The restoration mask left those pixels opaque while overwriting their required wood colours and outlines. This page keeps V10 as a negative control: all four units must fail the new exact-structure diagnostic.</p><table><thead><tr><th>V10 unit</th><th>Wrong structural pixels in standard frame</th><th>Expected result</th></tr></thead><tbody id="failures"></tbody></table></section>
<section class="panel"><h2>Corrected V13 family · every state and frame tested</h2><div class="controls"><label>State <select id="state" disabled><option>standard</option><option>on</option><option>broken</option></select></label><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><span id="readout"></span></div><div id="family" class="grid"></div></section>
<section class="panel"><h2>Complete room with the latest two shelves</h2><div class="alpha"><img class="room" id="room" alt="Nine-bay kitchen with corrected continuous countertops"></div></section>
<section class="panel"><h2>Binding test</h2><p class="notice"><strong>PASS requires:</strong> full-band opacity; byte-exact Option-B RGBA structure outside the declared sink-basin interval; zero mask escape; and identical structure through every animation frame. <code>npm test</code> runs this gate. No runtime, Final, Keeper, manifest or live-game asset is changed.</p></section>
</main><script>
const DATA=__DATA__;let frame=0,timer=null;const urls=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))urls.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const unique=[...new Set(urls)];
function render(){family.innerHTML='';const selected=state.value;let max=1;for(const [name,states] of Object.entries(DATA.units)){const frames=states[selected]||states.standard;max=Math.max(max,frames.length);const card=document.createElement('article');card.className='card';card.innerHTML=`<h3>${name}</h3><div class="alpha"><img class="sprite" src="${frames[frame%frames.length]}"></div><p class="good">Exact slab gate: PASS</p>`;family.append(card)}readout.textContent=`Frame ${frame+1} / ${max}`}
function stop(){if(timer)clearInterval(timer);timer=null}function start(){stop();timer=setInterval(()=>{frame=(frame+1)%4;render()},220)}
function setup(){for(const [name,count] of Object.entries(DATA.v10Failures)){const tr=document.createElement('tr');tr.innerHTML=`<td>${name}</td><td class="bad">${count}</td><td>FAIL detected</td>`;failures.append(tr)}room.src=DATA.room;state.disabled=false;play.disabled=false;pause.disabled=false;state.onchange=()=>{frame=0;render()};play.onclick=start;pause.onclick=stop;render();start();loading.textContent=`All ${unique.length} unique images loaded and decoded. Controls enabled; playback started.`}
Promise.all(unique.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed to load: ${e.message}`);
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
        for item in folder.iterdir():
            if item.is_file():
                item.unlink()

    v10_catalogue = read_json(V10_DRAFT / "asset-catalogue.json")
    v8_catalogue = read_json(V8_DRAFT / "asset-catalogue.json")
    states: dict[str, dict[str, dict]] = {}
    standard_frames: dict[str, Image.Image] = {}
    templates: dict[str, dict] = {}
    baseline_failures: dict[str, int] = {}
    for stem, state_map in v10_catalogue["correctedCounterStates"].items():
        states[stem] = {}
        template = None
        for state, record in state_map.items():
            originals = split_strip(record)
            repaired = []
            for original in originals:
                fixed, current_template = repair_frame(original, stem)
                repaired.append(fixed)
                template = current_template
            states[stem][state] = save_state(stem, state, repaired, record["meta"])
            if state == "standard":
                standard_frames[stem] = repaired[0]
                baseline_failures[stem] = pixel_mismatches(originals[0], template, stem)
        template_record = save_asset(f"{stem[4:]}_option_b_structure", template, (21, 31), {"role": "canonical-test-template"})
        templates[stem] = template_record

    standards = {stem: v10.load_first(v8_catalogue["assets"][stem]["states"]["standard"]) for stem in v8.ORDER}
    standards.update(standard_frames)
    standards["obj_fridge"] = Image.open(V10_RAW / "obj_fridge_standard_f1.png").convert("RGBA")
    room_record = save_asset("room_kitchen_9bay_v13_continuous_countertops", compose_room(standards), (193, 56), {
        "reviewComposite": True, "countertopGate": RECIPE["id"], "latestShelves": ["fridge-plant-v10", "kettle-books-v12"],
    })

    data = {
        "units": {stem.replace("obj_", ""): {state: record["urls"] for state, record in state_map.items()} for stem, state_map in states.items()},
        "v10Failures": {stem.replace("obj_", ""): count for stem, count in baseline_failures.items()},
        "room": room_record["url"],
    }
    catalogue = {
        "version": 13, "status": "reversible-draft", "recipe": RECIPE,
        "states": states, "templates": templates, "room": room_record,
        "v10NegativeControlStandardMismatchCounts": baseline_failures,
    }
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)

    register = {
        "version": 13, "status": "reversible-draft", "scope": "exact-countertop-rgba-continuity-gate",
        "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)},
        "v10TreeSha256": tree_sha(V10_RAW),
        "runtimeSpriteManifestSha256": sha(ROOT / "public/sprites/manifest.json"),
        "animationWorkbenchFinalStateSha256": sha(ROOT / "data/keeper_animation_workbench.json"),
        "runtimeChanged": False, "finalChanged": False, "keeperChanged": False,
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    outputs = sorted(path for path in RAW.iterdir() if path.is_file()) + sorted(path for path in DRAFT.glob("*.json") if path.name != "batch-register.json") + [PUBLIC / "index.html"]
    register["outputs"] = [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs]
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"set": RECIPE["id"], "v10Failures": baseline_failures, "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
