#!/usr/bin/env python3
"""Build reversible Kitchen V33-V38 coordinated state families."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
BASE_ROOM = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v31/kitchen-bin-standard-in-situ.png"
BASE_ROOM_SHA = "027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674"
ROOM_SIZE = (772, 224)
FRAMES = 40
FPS = 4

NAVY = (4, 20, 48, 255)
PALE = (224, 242, 231, 230)
WATER = (35, 178, 218, 230)
WATER_LIGHT = (184, 246, 242, 245)
SMOKE = (48, 54, 63, 205)
SMOKE_LIGHT = (116, 121, 124, 145)
FLAME = (245, 96, 37, 245)
FLAME_LIGHT = (255, 211, 72, 255)
HEAT = (245, 172, 79, 145)


SPECS = {
    "kettle": {
        "version": 33,
        "source_dir": "kitchen-kettle-states-2026-10-18-v33",
        "source_file": "kettle-three-state-source-v1.png",
        "source_sha": "f935e112d0d5fc43536762fb528fbff0fd3121733434aea2936d5b4e428b4b54",
        "columns": 3,
        "states": ["standard", "on", "broken"],
        "max_size": (32, 32), "cell": (84, 68), "room_at": (168, 76),
        "current": "kettle.png", "current_sha": "a3b7d1ea445b66a5c72d6c52d290fd9d2e1859342867cbf0f5392db460daad37",
        "effects": ["small_steam"],
        "effect_states": {"on": ["small_steam"]},
        "sfx": ["kitchen_kettle_heating_hiss_loop", "kitchen_kettle_broken_handle_rattle"],
        "requirements": {"smallSteamFromSpout": True, "steamSeparate": True, "brokenHandleMountFailed": True, "brokenHandleAttached": True, "visibleElectricalEffects": False},
        "summary": "The on state keeps the lid seated and uses a small spout-owned steam curl. The broken handle leans from one failed mounting while remaining attached; the sprung lid, dent and chip stay static.",
    },
    "toaster": {
        "version": 34,
        "source_dir": "kitchen-toaster-states-2026-10-18-v34",
        "source_file": "toaster-three-state-source-v1.png",
        "source_sha": "72c4336829f4bb6da2ff71283e2c0a4c4b9f026692b3e6e2df5bec6af307402b",
        "columns": 3,
        "states": ["standard", "on", "broken"],
        "max_size": (48, 38), "cell": (84, 68), "room_at": (252, 76),
        "current": "toaster.png", "current_sha": "2bf3b2b2c14c9a87ef2165b45c6cedd3dd109d7ecdeb9b1af79b1a8acf5f97fe",
        "effects": ["restrained_heat"],
        "effect_states": {"on": ["restrained_heat"]},
        "sfx": ["kitchen_toaster_heating_hum_loop", "kitchen_toaster_jammed_click"],
        "requirements": {"onBreadTopsVisible": True, "heatSeparate": True, "brokenBreadJammed": True, "visibleFlames": False, "visibleElectricalEffects": False},
        "summary": "The on state has its lever down and bread tops visible; restrained heat rises separately. The broken state has jammed crooked bread, a bent lever and a loosened scorched seam without flames or electrical flashes.",
    },
    "oven": {
        "version": 35,
        "source_dir": "kitchen-oven-states-2026-10-18-v35",
        "source_file": "oven-three-state-source-v1.png",
        "source_sha": "6468b44c8a3e3aa5e8a87c2c97020bc2cded221de40bf9bb00bf65a75ee2bfaf",
        "columns": 3,
        "states": ["standard", "on", "broken"],
        "max_size": (84, 84), "cell": (92, 96), "room_at": (332, 112),
        "current": "basic-oven.png", "current_sha": "45658c2649d10efc896d646821b16e12d3a19fc401d04168e00ace3a6f016ba8",
        "effects": ["billowing_smoke", "hob_flames"],
        "effect_states": {"broken": ["billowing_smoke", "hob_flames"]},
        "sfx": ["kitchen_oven_on_fan_loop", "kitchen_oven_broken_smoke_hiss_loop", "kitchen_oven_hob_flame_loop"],
        "requirements": {"standardInteriorLight": False, "onInteriorLight": True, "onDialsTurned": True, "onRedIndicator": True, "onRoastingTin": True, "brokenDoorAskew": True, "smokeSeparate": True, "hobFlamesSeparate": True},
        "summary": "Standard is fully dark and off. On has turned dials, a red indicator, warm interior light and a roasting tin. Broken has a static askew attached door; smoke and hob flames are separate reusable layers.",
    },
    "mixing-bowl": {
        "version": 36,
        "source_dir": "kitchen-mixing-bowl-states-2026-10-18-v36",
        "source_file": "mixing-bowl-two-state-source-v1.png",
        "source_sha": "700f66771ef1ce63c5ef293066e9512d32db338f5932a2a0966be1129514e6e6",
        "columns": 2,
        "states": ["standard", "broken"],
        "max_size": (44, 30), "cell": (84, 68), "room_at": (420, 76),
        "current": "mixer.png", "current_sha": "de45048124ad67398f84ac86c7cf3d359c21334c39422d2fbe1b4bac5238f47f",
        "effects": [], "effect_states": {},
        "sfx": ["kitchen_mixing_bowl_ceramic_break"],
        "requirements": {"animationRequired": False, "brokenLargeCeramicPieces": True, "intactTableauBeneathBroken": False},
        "summary": "The intact cream bowl and its large broken ceramic sections share one painted construction. The broken drawing contains no intact bowl beneath it and needs no animation.",
    },
    "basin": {
        "version": 37,
        "source_dir": "kitchen-basin-states-2026-10-18-v37",
        "source_file": "basin-three-state-source-v1.png",
        "source_sha": "9518bc62fcd36704d59b3993d5d1719c984d07f43a8e64b019638adff0cedacc",
        "columns": 3,
        "states": ["standard", "on", "broken"],
        "max_size": (84, 96), "cell": (92, 112), "room_at": (500, 96),
        "current": "sink.png", "current_sha": "9bad73df84998eb6187e5ee78a0a9784535c5fc529786060704547f7985f5bb9",
        "effects": ["gentle_flow", "upward_spray"],
        "effect_states": {"on": ["gentle_flow"], "broken": ["upward_spray"]},
        "sfx": ["kitchen_basin_gentle_flow_loop", "kitchen_basin_broken_spray_loop"],
        "requirements": {"standardWaterRunning": False, "onGentleFlow": True, "onFlowSeparate": True, "brokenTapCracked": True, "brokenUpwardSpraySeparate": True},
        "summary": "Standard is dry. On turns one handle and adds a separate gentle spout flow. Broken keeps the cracked tilted tap static and adds a separate upward spray.",
    },
    "table": {
        "version": 38,
        "source_dir": "kitchen-table-states-2026-10-18-v38",
        "source_file": "table-two-state-source-v1.png",
        "source_sha": "d5d34dd002c9f14f6d0585026ff9f2c61baecb639a6c9325cf8b543e7ec8872f",
        "columns": 2,
        "states": ["standard", "broken"],
        "max_size": (96, 78), "cell": (104, 96), "room_at": (666, 120),
        "current": "table.png", "current_sha": "582fbf39719bbda940d2dadf3821852f3415b984c93787f3d7ce6d1a118b74ad",
        "effects": [], "effect_states": {},
        "sfx": ["kitchen_table_broken_creak"],
        "requirements": {"animationRequired": False, "brokenLegPartlyAttached": True, "brokenFootFloorContact": True, "intactTableBeneathBroken": False},
        "summary": "The broken table is a dedicated tilted drawing, not an overlay on the intact table. Its fractured front-left leg remains visibly partly attached and the damaged foot still meets the floor.",
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hard_alpha(image: Image.Image, threshold: int = 80) -> Image.Image:
    image.putalpha(image.getchannel("A").point(lambda value: 255 if value >= threshold else 0))
    return image


def quantize(image: Image.Image, colours: int = 40) -> Image.Image:
    pal = image.convert("RGB").quantize(colors=colours, method=Image.Quantize.MEDIANCUT).convert("RGB")
    return Image.merge("RGBA", (*pal.split(), image.getchannel("A")))


def clean_generated_effects(name: str, state: str, crop: Image.Image) -> Image.Image:
    """Remove concept-sheet motion marks; production effects are separate strips."""
    out = crop.copy()
    alpha = out.getchannel("A")
    draw = ImageDraw.Draw(alpha)
    w, h = out.size
    if name == "kettle" and state == "on":
        draw.rectangle((0, 0, round(w * .20), round(h * .48)), fill=0)
    elif name == "toaster" and state == "on":
        draw.rectangle((0, 0, w, round(h * .20)), fill=0)
    elif name == "oven" and state == "broken":
        draw.rectangle((0, 0, w, round(h * .17)), fill=0)
    elif name == "basin" and state == "on":
        pixels = out.load(); mask = alpha.load()
        for y in range(round(h * .18), round(h * .52)):
            for x in range(round(w * .32), round(w * .68)):
                r, g, b, _ = pixels[x, y]
                if b > r * 1.35 and g > r * 1.25:
                    mask[x, y] = 0
    out.putalpha(alpha)
    return out


def make_state(source: Image.Image, spec: dict, index: int, state: str) -> Image.Image:
    x0 = round(index * source.width / spec["columns"])
    x1 = round((index + 1) * source.width / spec["columns"])
    crop = clean_generated_effects(spec["slug"], state, source.crop((x0, 0, x1, source.height)))
    crop = hard_alpha(crop)
    bbox = crop.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError(f"{spec['slug']} {state} is empty")
    crop = crop.crop(bbox)
    max_w, max_h = spec["max_size"]
    scale = min(max_w / crop.width, max_h / crop.height)
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    reduced = quantize(hard_alpha(crop.resize(size, Image.Resampling.LANCZOS)))
    cell = Image.new("RGBA", spec["cell"])
    x = (spec["cell"][0] - size[0]) // 2
    y = spec["cell"][1] - size[1] - 3
    cell.alpha_composite(reduced, (x, y))
    return cell


def frame_canvas(cell: tuple[int, int]) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", cell)
    return image, ImageDraw.Draw(image)


def effect_frame(kind: str, index: int, cell: tuple[int, int]) -> Image.Image:
    image, draw = frame_canvas(cell)
    phase = index / FRAMES * math.tau
    cx = cell[0] // 2
    if kind == "small_steam":
        for strand in range(2):
            base_x = cx - 19 + strand * 4
            for step in range(7):
                y = 31 - step * 2
                x = base_x + round(math.sin(phase + step * .8 + strand) * 2)
                draw.point((x, y), fill=PALE if step < 5 else (224, 242, 231, 120))
    elif kind == "restrained_heat":
        for strand in range(3):
            for step in range(6):
                y = 31 - step * 2
                x = cx - 7 + strand * 7 + round(math.sin(phase + step + strand) * 1.5)
                draw.point((x, y), fill=HEAT)
    elif kind == "billowing_smoke":
        for puff in range(7):
            age = (index + puff * 6) % FRAMES
            y = 72 - round(age * 1.25)
            x = cx + round(math.sin(phase + puff * 1.3) * (5 + age * .08))
            radius = 2 + age // 12
            colour = SMOKE if puff % 2 else SMOKE_LIGHT
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=colour)
    elif kind == "hob_flames":
        for branch, burner in enumerate((-18, 18)):
            height = 7 + ((index * (3 + branch) + branch * 2) % 5)
            lean = round(math.sin(phase + branch * 1.7) * 2)
            x = cx + burner
            draw.polygon([(x-4, 39), (x-2, 34), (x+lean, 39-height), (x+2, 34), (x+4, 39)], fill=FLAME)
            draw.polygon([(x-1, 38), (x+lean, 33-height//2), (x+2, 38)], fill=FLAME_LIGHT)
    elif kind == "gentle_flow":
        x = cx + 1
        for y in range(31, 57):
            wobble = round(math.sin(phase + y * .45)) if y > 42 else 0
            draw.point((x+wobble, y), fill=WATER)
            if y % 3 == index % 3:
                draw.point((x+wobble+1, y), fill=WATER_LIGHT)
        draw.arc((cx-7, 52, cx+9, 59), 0, 180, fill=WATER)
    elif kind == "upward_spray":
        origin = (cx + 4, 38)
        for branch, angle in enumerate((-2.25, -1.9, -1.55, -1.25, -.9)):
            length = 20 + ((index + branch * 5) % 9)
            end = (round(origin[0] + math.cos(angle) * length), round(origin[1] + math.sin(angle) * length))
            draw.line((origin, end), fill=WATER, width=2)
            draw.point(end, fill=WATER_LIGHT)
        for drop in range(5):
            x = cx - 17 + ((index * 3 + drop * 11) % 35)
            y = 10 + ((index * 2 + drop * 7) % 24)
            draw.point((x, y), fill=WATER_LIGHT)
    else:
        raise RuntimeError(kind)
    return image


def make_strip(kind: str, cell: tuple[int, int]) -> Image.Image:
    strip = Image.new("RGBA", (cell[0] * FRAMES, cell[1]))
    for index in range(FRAMES):
        strip.alpha_composite(effect_frame(kind, index, cell), (index * cell[0], 0))
    return strip


def fill_wall(room: Image.Image, box: tuple[int, int, int, int]) -> None:
    pixels = room.load(); x0, y0, x1, y1 = box
    for y in range(y0, y1):
        samples = [pixels[x, y] for x in list(range(4, 76)) + list(range(624, 670))]
        samples = [p for p in samples if p[3] and p[0] > 120 and p[1] > 105 and p[2] > 80]
        colour = tuple(sum(p[channel] for p in samples) // len(samples) for channel in range(4))
        for x in range(x0, x1): pixels[x, y] = colour


def chair_foreground(room: Image.Image) -> Image.Image:
    layer = Image.new("RGBA", room.size); pix = room.load(); out = layer.load()
    for y in range(114, 190):
        for x in range(694, 750):
            r, g, b, a = pix[x, y]
            blue = b > 55 and b > r * 1.12 and b > g * .72
            navy = r < 48 and g < 76 and b < 138
            orange = r > 95 and r > g * 1.25 and g > b * 1.05
            cream = 704 <= x <= 739 and 166 <= y <= 189 and r > 135 and g > 125 and b > 105
            geometry = x <= 713 or x >= 728 or 121 <= y <= 174
            if a and ((geometry and (blue or navy or orange)) or cream): out[x, y] = pix[x, y]
    return layer


def clean_room(base: Image.Image, name: str) -> tuple[Image.Image, Image.Image | None]:
    room = base.copy(); chair = None
    if name == "kettle": fill_wall(room, (181, 106, 241, 141))
    elif name == "toaster": fill_wall(room, (262, 116, 326, 141))
    elif name == "mixing-bowl": fill_wall(room, (436, 116, 491, 141))
    elif name == "oven":
        room.paste(base.crop((252, 124, 336, 208)), (336, 124)); fill_wall(room, (336, 112, 420, 141))
    elif name == "basin":
        room.paste(base.crop((420, 112, 504, 208)), (504, 112)); fill_wall(room, (504, 96, 588, 141))
    elif name == "table":
        chair = chair_foreground(base); pix = room.load()
        for y in range(112, 224):
            sample_x = 651 if y < 194 else 642
            colour = pix[sample_x, y]
            for x in range(666, 772): pix[x, y] = colour
    return room, chair


def compose_room(base: Image.Image, name: str, spec: dict, state_image: Image.Image) -> Image.Image:
    room, chair = clean_room(base, name)
    room.alpha_composite(state_image, spec["room_at"])
    if chair is not None: room.alpha_composite(chair)
    return room


def save_png(image: Image.Image, raw: Path, public_assets: Path, name: str) -> None:
    raw.mkdir(parents=True, exist_ok=True); public_assets.mkdir(parents=True, exist_ok=True)
    image.save(raw / name, optimize=True); shutil.copyfile(raw / name, public_assets / name)


def write_page(name: str, spec: dict, outputs: dict[str, dict]) -> None:
    route = f"kitchen-{name}-states-v{spec['version']}"
    public = ROOT / "public/keeper-review" / route
    state_cards = "".join(f'<article><h3>{state.replace("-", " ").title()}</h3><div class="iso"><img data-media src="assets/{name}-{state}.png"></div></article>' for state in spec["states"])
    room_cards = ""
    for state in spec["states"]:
        overlays = "".join(f'<i class="roomfx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-{name}-{kind}-f40.png"></i>' for kind in spec["effect_states"].get(state, []))
        room_cards += f'<article><h3>{state.replace("-", " ").title()}</h3><div class="room"><img data-media src="assets/kitchen-{name}-{state}-in-situ.png">{overlays}</div></article>'
    fx_cards = "".join(f'<article><h3>{kind.replace("_", " ").title()} · 40f / 4fps / 10s</h3><div class="fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-{name}-{kind}-f40.png"></div></article>' for kind in spec["effects"])
    comparison = f'<section><h2>Canonical reference beside the new standard</h2><div class="grid"><article><h3>Current V21/V23 authority</h3><div class="iso contain"><img data-media src="assets/{name}-v21-current.png"></div></article><article><h3>V{spec["version"]} coordinated standard</h3><div class="iso"><img data-media src="assets/{name}-standard.png"></div></article></div></section>'
    page = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/{route}/"><title>Kitchen V{spec['version']} · {name} family</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:15px/1.4 system-ui}}main{{max-width:1160px;margin:auto;padding:20px}}section,article{{background:#102b37;border:1px solid #315768;border-radius:12px;padding:12px;margin:12px 0}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}}.iso{{position:relative;height:{spec['cell'][1]*4}px;overflow:hidden;background:#dceae4}}.iso img{{width:{spec['cell'][0]*4}px;height:{spec['cell'][1]*4}px;image-rendering:pixelated}}.contain img{{object-fit:contain}}.room{{position:relative;width:772px;height:224px;overflow:hidden}}.room>img:first-child{{width:772px;height:224px}}.roomfx{{position:absolute;left:{spec['room_at'][0]}px;top:{spec['room_at'][1]}px;width:{spec['cell'][0]}px;height:{spec['cell'][1]}px;overflow:hidden}}.roomfx img{{height:{spec['cell'][1]}px;max-width:none;image-rendering:pixelated}}.fx{{width:{spec['cell'][0]*4}px;height:{spec['cell'][1]*4}px;overflow:hidden;background:#dceae4}}.fx img{{height:{spec['cell'][1]*4}px;max-width:none;image-rendering:pixelated}}[data-media]{{visibility:hidden}}.ready [data-media]{{visibility:visible}}button{{padding:8px 12px;background:#147d78;color:white;border:0;border-radius:6px}}.warn{{border-left:4px solid #e8b852;padding:10px}}.scroll{{overflow:auto}}</style></head><body><main><h1>Kitchen V{spec['version']} · coordinated {name} family</h1><p>{spec['summary']}</p><p id="loading">Loading and decoding every unique review image before playback…</p><button id="play" disabled>Play effects</button> <button id="pause" disabled>Pause</button><section><h2>Isolated states · 4× inspection</h2><div class="grid">{state_cards}</div></section>{comparison}<section><h2>Complete kitchen · exact 772 × 224 game pixels</h2><div class="grid scroll">{room_cards}</div></section>{f'<section><h2>Reusable environmental layers</h2><div class="grid">{fx_cards}</div></section>' if fx_cards else ''}<p>Named SFX placeholders: {', '.join(spec['sfx'])}</p><p class="warn">Reversible review draft only. V5 and V20–V{spec['version']-1}, Final art and runtime remain unchanged.</p></main><script>const strips=[...document.querySelectorAll('[data-strip]')],buttons=[...document.querySelectorAll('button')];let go=0,start=0,held=0,raf;function tick(now){{if(!go)return;for(const image of strips){{const frame=Math.floor((held+now-start)*4/1000)%40,w=image.parentElement.clientWidth;image.style.transform=`translateX(${{-frame*w}}px)`}}raf=requestAnimationFrame(tick)}}function run(){{if(go)return;go=1;start=performance.now();raf=requestAnimationFrame(tick)}}function stop(){{if(!go)return;held+=performance.now()-start;go=0;cancelAnimationFrame(raf)}}function preload(src){{return new Promise((ok,bad)=>{{const image=new Image;image.onload=()=>image.decode?image.decode().then(ok,ok):ok();image.onerror=bad;image.src=src}})}}const unique=[...new Set([...document.querySelectorAll('[data-media]')].map(x=>x.src))];Promise.all(unique.map(preload)).then(()=>{{document.body.classList.add('ready');buttons.forEach(x=>x.disabled=false);loading.textContent='All review images decoded. Playback unlocked.';run()}});play.onclick=run;pause.onclick=stop</script></body></html>'''
    public.mkdir(parents=True, exist_ok=True); (public / "index.html").write_text(page)


def build_family(name: str, raw_spec: dict, base: Image.Image) -> None:
    spec = dict(raw_spec); spec["slug"] = name
    source_path = ROOT / "art/source" / spec["source_dir"] / "generated" / spec["source_file"]
    current_path = ROOT / "art/raw/kitchen-final-assets-2026-10-17-v21" / spec["current"]
    if sha(source_path) != spec["source_sha"] or sha(current_path) != spec["current_sha"]:
        raise RuntimeError(f"Pinned input changed for {name}")
    source = Image.open(source_path).convert("RGBA")
    states = {state: make_state(source, spec, index, state) for index, state in enumerate(spec["states"])}
    effects = {kind: make_strip(kind, spec["cell"]) for kind in spec["effects"]}
    route = f"kitchen-{name}-states-v{spec['version']}"
    raw = ROOT / "art/raw" / f"kitchen-{name}-states-2026-10-18-v{spec['version']}"
    draft = ROOT / "art/drafts" / f"kitchen-{name}-states-2026-10-18-v{spec['version']}"
    assets = ROOT / "public/keeper-review" / route / "assets"
    outputs: dict[str, dict] = {}
    for state, image in states.items():
        filename = f"{name}-{state}.png"; save_png(image, raw, assets, filename)
    for kind, strip in effects.items():
        filename = f"fx-{name}-{kind}-f40.png"; save_png(strip, raw, assets, filename)
    current = Image.open(current_path).convert("RGBA")
    save_png(current, raw, assets, f"{name}-v21-current.png")
    for state, image in states.items():
        room = compose_room(base, name, spec, image)
        save_png(room, raw, assets, f"kitchen-{name}-{state}-in-situ.png")
    for file in sorted(raw.glob("*.png")):
        with Image.open(file) as image:
            outputs[file.name] = {"sha256": sha(file), "pixels": list(image.size)}
    catalogue = {
        "version": spec["version"], "asset": name, "status": "awaiting-visual-review",
        "construction": {"coordinatedFamily": True, "sameSourceSheet": True, "objectAnimation": False},
        "requirements": spec["requirements"],
        "states": spec["states"], "cellPixels": list(spec["cell"]), "roomPixels": list(ROOM_SIZE),
        "roomCellTopLeft": list(spec["room_at"]),
        "source": {"path": str(source_path.relative_to(ROOT)), "sha256": spec["source_sha"]},
        "canonicalReference": {"path": str(current_path.relative_to(ROOT)), "sha256": spec["current_sha"]},
        "effects": {kind: {"file": f"fx-{name}-{kind}-f40.png", "frames": FRAMES, "fps": FPS, "durationSeconds": 10, "reusable": True, "cellPixels": list(spec["cell"]), "objectPixelsChanged": False} for kind in spec["effects"]},
        "sfxCues": spec["sfx"], "outputs": outputs,
        "boundaries": {"approved": False, "promoted": False, "runtimeChanged": False, "finalChanged": False, "v5AndV20OnwardChanged": False},
    }
    draft.mkdir(parents=True, exist_ok=True)
    (draft / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (draft / "batch-register.json").write_text(json.dumps({"version": spec["version"], "asset": name, "status": "awaiting-visual-review", "previousApprovedReview": 32 if spec["version"] == 33 else spec["version"] - 1, "rollback": f"Delete only the V{spec['version']} source/raw/draft/review/archive/builder outputs."}, indent=2) + "\n")
    write_page(name, spec, outputs)


def main() -> None:
    if sha(BASE_ROOM) != BASE_ROOM_SHA: raise RuntimeError("Pinned V31 room changed")
    base = Image.open(BASE_ROOM).convert("RGBA")
    if base.size != ROOM_SIZE: raise RuntimeError("V31 room geometry changed")
    for name, spec in SPECS.items(): build_family(name, spec, base)
    print(json.dumps({"built": [f"V{spec['version']} {name}" for name, spec in SPECS.items()], "framesPerEffect": FRAMES, "fps": FPS}, indent=2))


if __name__ == "__main__": main()
