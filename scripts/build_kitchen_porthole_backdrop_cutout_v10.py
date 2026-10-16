#!/usr/bin/env python3
"""Build the reversible Kitchen V10 true-backdrop porthole review draft.

V9 remains immutable. V10 removes every kitchen-owned illustrated porthole
condition and instead creates a true alpha knockout through the room wall, so
the global lighthouse backdrop can be seen beneath the room at runtime.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import build_kitchen_wall_anchored_v8 as v8


ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = ROOT / "data/kitchen_porthole_backdrop_cutout_v10_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
V7_RAW = ROOT / "art/raw/kitchen-room-flat-cutaway-2026-10-16-v7"
V8_RAW = ROOT / "art/raw/kitchen-wall-anchored-2026-10-16-v8"
V8_DRAFT = ROOT / "art/drafts/kitchen-wall-anchored-2026-10-16-v8"
V9_RAW = ROOT / "art/raw/kitchen-fridge-shelf-2026-10-17-v9"
V9_DRAFT = ROOT / "art/drafts/kitchen-fridge-shelf-2026-10-17-v9"
SOURCE = ROOT / "art/source/kitchen-final-reference-2026-10-17-v10"
RAW = ROOT / "art/raw/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
DRAFT = ROOT / "art/drafts/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
PUBLIC = ROOT / "public/keeper-review/kitchen-porthole-backdrop-cutout-v10"
ASSETS = PUBLIC / "assets"

DENSITY = 4
BAY = 21
DOOR_DATUM = 4
FOOT_LINE = 52
TRANSPARENT = (0, 0, 0, 0)
INK = (7, 27, 50, 255)
BRASS_DARK = (135, 80, 12, 255)
BRASS = (215, 150, 34, 255)
BRASS_LIGHT = (255, 205, 67, 255)


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


def save_asset(name: str, image: Image.Image, logical: tuple[int, int], extra: dict | None = None) -> dict:
    path = RAW / f"{name}.png"
    save_png(image, path)
    meta = {
        "w": logical[0], "h": logical[1], "frames": 1, "fps": 0,
        "density": 4, "anchor": [logical[0] / 2, logical[1]],
        "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False},
    }
    if extra:
        meta.update(extra)
    path.with_suffix(".json").write_text(json.dumps(meta, indent=2) + "\n")
    review_path = ASSETS / f"{name}.png"
    save_png(image, review_path)
    return {
        "png": path.relative_to(ROOT).as_posix(),
        "json": path.with_suffix(".json").relative_to(ROOT).as_posix(),
        "sha256": sha(path), "meta": meta,
        "url": f"/keeper-review/kitchen-porthole-backdrop-cutout-v10/assets/{review_path.name}",
        "bound": alpha_bound(image),
    }


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def load_first(record: dict) -> Image.Image:
    image = Image.open(ROOT / record["png"]).convert("RGBA")
    return image.crop((0, 0, record["meta"]["w"] * 4, record["meta"]["h"] * 4))


def fit_alpha_source(filename: str, cell: tuple[int, int], max_size: tuple[int, int], bottom: int) -> Image.Image:
    """Fit a high-resolution approved cutout into an exact logical cell."""
    source = Image.open(SOURCE / filename).convert("RGBA")
    # Discard the generator's extremely faint full-canvas antialias haze before
    # measuring; otherwise the actual object is incorrectly shrunk in its cell.
    source.putalpha(source.getchannel("A").point(lambda value: 255 if value >= 96 else 0))
    box = source.getchannel("A").getbbox()
    if not box:
        raise ValueError(f"empty alpha source: {filename}")
    source = source.crop(box)
    scale = min(px(max_size[0]) / source.width, px(max_size[1]) / source.height)
    size = (max(1, round(source.width * scale)), max(1, round(source.height * scale)))
    source = source.resize(size, Image.Resampling.LANCZOS)
    out = rgba((px(cell[0]), px(cell[1])))
    out.alpha_composite(source, ((out.width - source.width) // 2, px(bottom) - source.height))
    return out


def smooth_complete_counter(image: Image.Image, stem: str) -> Image.Image:
    """Replace the complete slab, not merely its exposed wings.

    The V8 wing-only repair left the old centre in place, producing the visibly
    chipped/stepped joins Frank rejected. This lays one Option-B slab across the
    full 20-lp width, then restores only the appliance/basin foreground.
    """
    spec = v8.COUNTER_SPEC[stem]
    front = spec["front"]
    y0, y1 = front - 6, front + 8
    out = image.copy()
    out.paste((0, 0, 0, 0), (0, y0, out.width, y1))
    out.alpha_composite(v8.clean_counter_slab(image.size, front))
    # Non-wood colour seeds identify the appliance or basin. Grow by two pixels
    # to recover its navy outline without bringing back the old wooden steps.
    seed = Image.new("L", image.size, 0)
    src = image.load(); mask = seed.load()
    for y in range(y0, y1):
        for x in range(image.width):
            r, g, b, a = src[x, y]
            woodish = a and r > 65 and r > g * 1.18 and g > b * .8
            dark = a and r < 65 and g < 75 and b < 90
            if a and not woodish and not dark:
                mask[x, y] = 255
    grown = seed.filter(ImageFilter.MaxFilter(5))
    restored = rgba(image.size)
    restored.paste(image, (0, 0), grown)
    out.alpha_composite(restored)
    return out


def corrected_state_frames(v8_catalogue: dict, stem: str, state: str) -> list[Image.Image]:
    record = v8_catalogue["assets"][stem]["states"][state]
    frames = v8.load_strip(ROOT / record["png"], record["meta"])
    if stem in v8.COUNTER_SPEC:
        return [smooth_complete_counter(frame, stem) for frame in frames]
    return frames


def make_strip(frames: list[Image.Image]) -> Image.Image:
    out = rgba((frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        out.alpha_composite(frame, (index * frame.width, 0))
    return out


def save_state(name: str, frames: list[Image.Image], logical: tuple[int, int], fps: int) -> dict:
    path = RAW / f"{name}.png"
    save_png(make_strip(frames), path)
    meta = {"w": logical[0], "h": logical[1], "frames": len(frames), "fps": fps,
            "density": 4, "anchor": [logical[0] / 2, logical[1]],
            "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False}}
    path.with_suffix(".json").write_text(json.dumps(meta, indent=2) + "\n")
    urls = []
    for index, frame in enumerate(frames):
        review = ASSETS / f"{name}_frame{index + 1}.png"
        save_png(frame, review)
        urls.append(f"/keeper-review/kitchen-porthole-backdrop-cutout-v10/assets/{review.name}")
    return {"png": path.relative_to(ROOT).as_posix(), "json": path.with_suffix('.json').relative_to(ROOT).as_posix(),
            "sha256": sha(path), "meta": meta, "urls": urls, "bounds": [alpha_bound(f) for f in frames]}


def porthole_frame() -> Image.Image:
    """Brass ring only: the complete 14-lp opening is alpha zero."""
    spec = RECIPE["porthole"]
    out = rgba((px(21), px(56)))
    d = ImageDraw.Draw(out)
    cx, cy = px(spec["centreLpFromCellTop"][0]), px(spec["centreLpFromCellTop"][1])
    outer = px(spec["outerFrameDiameterLp"])
    aperture = px(spec["roomWallKnockoutDiameterLp"])
    ox0, oy0 = cx - outer // 2, cy - outer // 2
    ox1, oy1 = ox0 + outer - 1, oy0 + outer - 1
    ax0, ay0 = cx - aperture // 2, cy - aperture // 2
    ax1, ay1 = ax0 + aperture - 1, ay0 + aperture - 1
    d.ellipse((ox0, oy0, ox1, oy1), fill=INK)
    d.ellipse((ox0 + 2, oy0 + 2, ox1 - 2, oy1 - 2), fill=BRASS_DARK)
    d.ellipse((ox0 + 5, oy0 + 5, ox1 - 5, oy1 - 5), fill=BRASS)
    d.arc((ox0 + 7, oy0 + 7, ox1 - 7, oy1 - 7), 205, 335, fill=BRASS_LIGHT, width=2)
    for index in range(8):
        import math
        angle = math.radians(index * 45 - 90)
        bx, by = round(cx + math.cos(angle) * px(8)), round(cy + math.sin(angle) * px(8))
        d.ellipse((bx - 2, by - 2, bx + 2, by + 2), fill=INK)
        d.point((bx, by), fill=BRASS_LIGHT)
    # The last operation is the authority: no outline, glass, shine or scene
    # pixel may survive inside the 14-lp opening.
    d.ellipse((ax0, ay0, ax1, ay1), fill=TRANSPARENT)
    return out


def aperture_geometry(bay: int) -> tuple[int, int, int, int]:
    spec = RECIPE["porthole"]
    cx = px(DOOR_DATUM + (bay - 1) * BAY + spec["centreLpFromCellTop"][0])
    cy = px(spec["centreLpFromCellTop"][1])
    diameter = px(spec["roomWallKnockoutDiameterLp"])
    x0, y0 = cx - diameter // 2, cy - diameter // 2
    return x0, y0, x0 + diameter - 1, y0 + diameter - 1


def room_shell_with_knockout(bay: int) -> Image.Image:
    out = Image.open(V7_RAW / "room_kitchen_shell_9bay.png").convert("RGBA")
    ImageDraw.Draw(out).ellipse(aperture_geometry(bay), fill=TRANSPARENT)
    return out


def place_one_bay(out: Image.Image, image: Image.Image, bay: int) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY) + (px(BAY) - image.width) // 2
    out.alpha_composite(image, (x, px(FOOT_LINE) - image.height))


def place_two_bays(out: Image.Image, image: Image.Image, bay: int) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY) + (px(2 * BAY) - image.width) // 2
    out.alpha_composite(image, (x, px(FOOT_LINE) - image.height))


def place_wall_child(out: Image.Image, image: Image.Image, bay: int) -> None:
    out.alpha_composite(image, (px(DOOR_DATUM + (bay - 1) * BAY), 0))


def full_room(standards: dict[str, Image.Image], shelf: Image.Image, frame: Image.Image, sink_bay: int = 7) -> Image.Image:
    out = room_shell_with_knockout(sink_bay)
    place_wall_child(out, shelf, 2)
    positions = {"obj_bin": 1, "obj_fridge": 2, "obj_kettle": 3, "obj_toaster": 4, "obj_cooker": 5, "obj_mixer": 6}
    for stem, bay in positions.items():
        place_one_bay(out, standards[stem], bay)
    place_wall_child(out, frame, sink_bay)
    place_one_bay(out, standards["obj_sink"], sink_bay)
    place_two_bays(out, standards["obj_table"], 8)
    place_one_bay(out, standards["obj_petbowl"], 9)
    return out


def movement_proof(sink: Image.Image, frame: Image.Image, bay: int) -> Image.Image:
    out = room_shell_with_knockout(bay)
    place_wall_child(out, frame, bay)
    place_one_bay(out, sink, bay)
    return out


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V10 · true backdrop porthole</title><style>
:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--muted:#a8bdc4;--gold:#efb64d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1520px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:12px;min-width:0}.alpha{overflow:auto;border-radius:9px;padding:10px;background:repeating-conic-gradient(#cf4e92 0 25%,#2cb9c2 0 50%) 0/20px 20px}.alpha img{display:block;height:224px;width:auto}.cell{min-height:260px;display:flex;align-items:center;justify-content:center}.cell img{height:224px;width:84px;object-fit:contain}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0}select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}select:disabled{opacity:.45}.recipe{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}.metric{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:10px}.metric strong{display:block;color:var(--gold);font-size:1.15rem}.stack{display:grid;grid-template-columns:auto 1fr;gap:7px 12px}.stack strong{color:var(--gold)}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:7px;border-bottom:1px solid var(--line);vertical-align:top}code{color:#9ce5ea;word-break:break-all}.small{font-size:.84rem;color:var(--muted)}@media(max-width:720px){header,main{padding:12px}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">True alpha opening</span><span class="tag">No kitchen-owned scenery</span><h1>Kitchen V10 · porthole opens onto the real lighthouse backdrop</h1><p>The kitchen supplies only a circular wall knockout and its brass frame. Sea, sky, weather and time remain entirely in the global backdrop beneath the room.</p><p id="loading" class="notice">Preloading and decoding every unique review image… controls remain locked.</p></header><main>
<section class="panel"><h2>Corrected construction</h2><div class="recipe"><div class="metric"><strong>14 lp</strong>alpha knockout through wall</div><div class="metric"><strong>19 lp</strong>separate brass ring</div><div class="metric"><strong>0 pixels</strong>glazing or painted scenery inside</div><div class="metric"><strong>backdrop-owned</strong>sea, sky, weather and time</div><div class="metric"><strong>same delta</strong>hole + frame + sink</div></div><p class="notice"><strong>Approval boundary:</strong> review draft only. No live room renderer, backdrop, runtime sprites, manifests, Keeper art or Final art have changed.</p></section>
<section class="panel"><h2>Alpha proof · deliberately no illustrated proxy</h2><p>The magenta/cyan checker is only a transparency test surface supplied by this page. It is not kitchen art and is not written to any PNG. Wherever it is visible, the image is genuinely alpha zero.</p><div class="grid"><div class="card"><h3>Brass frame only</h3><div class="alpha cell"><img id="frame"></div><p class="small">The full 14-lp centre is empty—no glass shine or condition imagery.</p></div><div class="card"><h3>Room wall knockout only</h3><div class="alpha"><img id="shell"></div><p class="small">The opening is cut through the room shell, not merely through the frame sprite.</p></div></div></section>
<section class="panel"><h2>Approved-reference family restored</h2><p>V9 is rejected. These are fresh V10 drafts based on the attached approved family: a detailed white refrigerator, a fitted polished shelf, and one uninterrupted Option-B slab across every counter state.</p><div id="family" class="grid"></div></section>
<section class="panel"><h2>Complete V10 kitchen with real backdrop opening</h2><div class="alpha"><img id="room"></div><p>The checker remains visible through the completed room after the frame and sink are composed. At runtime, this exact lower layer position belongs to the global lighthouse backdrop.</p></section>
<section class="panel"><h2>Move the sink · wall opening and frame follow</h2><div class="controls"><label>Sink bay <select id="bay" disabled><option>2</option><option>5</option><option>8</option></select></label></div><div class="alpha"><img id="move"></div><p>Wall-knockout delta = frame delta = sink delta. The room renderer must apply the knockout at the sink-owned position before drawing the frame and sink.</p></section>
<section class="panel"><h2>Required runtime layer stack</h2><div class="stack"><strong>z0</strong><span>Existing global lighthouse backdrop: real sea, sky, weather and time layers.</span><strong>z20</strong><span>Room shell with the 14-lp sink-owned alpha knockout applied.</span><strong>z26</strong><span>Brass porthole ring; centre remains entirely transparent.</span><strong>z40</strong><span>Sink unit.</span></div><p class="notice">The rejected V8/V9 day, sunset, night and rain porthole underlays are absent from V10 outputs and absent from this page.</p></section>
<section class="panel"><h2>Measured hand-back and hashes</h2><table><thead><tr><th>Item</th><th>Measurement</th><th>Role</th><th>SHA-256</th></tr></thead><tbody id="rows"></tbody></table></section>
</main><script>
const DATA=__DATA__,all=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))all.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const urls=[...new Set(all)];
function setup(){document.querySelectorAll('select').forEach(x=>x.disabled=false);frame.src=DATA.frame;shell.src=DATA.shell;room.src=DATA.room;for(const [name,url] of Object.entries(DATA.family)){const c=document.createElement('article');c.className='card';c.innerHTML=`<h3>${name}</h3><div class="alpha cell"><img src="${url}"></div>`;family.append(c)}bay.value='5';const show=()=>move.src=DATA.moves[bay.value];bay.onchange=show;show();for(const row of DATA.rows){const tr=document.createElement('tr');tr.innerHTML=`<td>${row.name}</td><td>${row.measure}</td><td>${row.role}</td><td><code>${row.sha256}</code></td>`;rows.append(tr)}loading.textContent=`All ${urls.length} unique review images loaded and decoded. Controls enabled.`}
document.querySelectorAll('select').forEach(x=>x.disabled=true);Promise.all(urls.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed to load: ${e.message}`);
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()

    v8_catalogue = read_json(V8_DRAFT / "asset-catalogue.json")
    standards = {stem: load_first(v8_catalogue["assets"][stem]["states"]["standard"]) for stem in v8.ORDER}
    state_records = {}
    for stem in v8.COUNTER_SPEC:
        state_records[stem] = {}
        for state in v8_catalogue["assets"][stem]["states"]:
            frames = corrected_state_frames(v8_catalogue, stem, state)
            logical = (v8_catalogue["assets"][stem]["cell"][0], v8_catalogue["assets"][stem]["cell"][1])
            state_records[stem][state] = save_state(f"{stem[4:]}_{state}", frames, logical, 8 if len(frames) > 1 else 0)
            if state == "standard": standards[stem] = frames[0]
    standards["obj_fridge"] = fit_alpha_source("fridge-approved-reference-cutout.png", (21, 21), (19, 19), 21)
    fridge_record = save_asset("obj_fridge_standard_f1", standards["obj_fridge"], (21, 21), {"visualBaseline": "approved-attached-reference"})
    shelf = fit_alpha_source("fridge-shelf-polished-study.png", (21, 56), (19, 16), 25)
    shelf_record = save_asset("obj_fridge_wall_shelf_v10_f1", shelf, (21, 56), {"parent": "obj_fridge", "movesWithParent": True})
    frame = porthole_frame()

    frame_record = save_asset("obj_sink_porthole_frame_f1", frame, (21, 56), {
        "z": 26, "outerDiameterLp": 19, "apertureDiameterLp": 14,
        "aperture": "fully-alpha-clear", "glazingInsideAperture": False,
        "parent": "obj_sink", "movesWithParent": True,
    })
    shell = room_shell_with_knockout(7)
    shell_record = save_asset("room_kitchen_shell_9bay_porthole_cutout_bay_7", shell, (193, 56), {
        "reviewDerivedShell": True, "sinkBay": 7, "knockoutDiameterLp": 14,
        "containsBackdropPixels": False,
    })
    room_record = save_asset("room_kitchen_9bay_true_backdrop_opening", full_room(standards, shelf, frame), (193, 56), {
        "reviewComposite": True, "sinkBay": 7, "apertureAlpha": 0,
        "containsBackdropPixels": False, "conditionUnderlays": [],
    })
    moves = {str(bay): save_asset(f"sink_porthole_cutout_move_bay_{bay}", movement_proof(standards["obj_sink"], frame, bay), (193, 56), {
        "reviewComposite": True, "sinkBay": bay, "frameBay": bay, "wallKnockoutBay": bay,
        "containsBackdropPixels": False,
    }) for bay in RECIPE["movementProofBays"]}

    data = {
        "frame": frame_record["url"], "shell": shell_record["url"], "room": room_record["url"],
        "family": {"white refrigerator": fridge_record["url"], "polished fitted shelf": shelf_record["url"], **{stem.replace('obj_','') + ' · smooth standard': states['standard']['urls'][0] for stem, states in state_records.items()}},
        "moves": {key: value["url"] for key, value in moves.items()},
        "rows": [
            {"name": "brass porthole frame", "measure": "21×56-lp cell; 19-lp outer; 14-lp empty centre", "role": "sink-owned z26 ring; no glazing/scenery", "sha256": frame_record["sha256"]},
            {"name": "room-wall knockout", "measure": "14-lp circular alpha opening", "role": "derived wall mask at sink bay 7", "sha256": shell_record["sha256"]},
            {"name": "complete V10 kitchen", "measure": "193×56 lp; aperture alpha 0", "role": "approved-reference family; V9 not reused", "sha256": room_record["sha256"]},
        ],
    }
    catalogue = {
        "version": 10, "status": "reversible-draft", "recipe": RECIPE["id"],
        "projection": RECIPE["projection"], "porthole": RECIPE["porthole"],
        "frame": frame_record, "shell": shell_record, "room": room_record, "fridge": fridge_record, "shelf": shelf_record,
        "correctedCounterStates": state_records,
        "movementPlacementsLp": {str(bay): {
            "sinkXLp": DOOR_DATUM + (bay - 1) * BAY,
            "frameXLp": DOOR_DATUM + (bay - 1) * BAY,
            "wallKnockoutXLp": DOOR_DATUM + (bay - 1) * BAY,
        } for bay in RECIPE["movementProofBays"]},
        "moves": moves,
    }
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)

    outputs = sorted(path for path in RAW.iterdir() if path.is_file()) + sorted(DRAFT.glob("*.json")) + [PUBLIC / "index.html"]
    register = {
        "version": 10, "status": "reversible-draft", "scope": "approved-reference-family-and-true-backdrop-porthole",
        "visualBaseline": RECIPE["visualBaseline"],
        "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)},
        "runtimeChanged": False, "finalChanged": False, "keeperChanged": False,
        "v8Overwritten": False, "v9Overwritten": False,
        "v9Accepted": False, "v9UsedAsVisualBaseline": False,
        "illustratedConditionUnderlaysProduced": 0,
        "protectedSnapshots": {
            "kitchenV9": tree_sha(V9_RAW), "kitchenRoomV7": tree_sha(V7_RAW),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
        "outputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs],
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"set": RECIPE["id"], "frameDiameterLp": 19, "alphaOpeningLp": 14, "illustratedUnderlays": 0, "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
