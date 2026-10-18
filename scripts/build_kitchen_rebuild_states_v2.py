#!/usr/bin/env python3
"""Build Kitchen Rebuild V2 as amendments to the exact V1 foundation."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-states-2026-10-18-v2"
SOURCE_DIR = ROOT / "art/source" / SET / "generated"
ON_SOURCE = SOURCE_DIR / "on-object-amendments-v1.png"
BROKEN_SOURCE = SOURCE_DIR / "broken-object-amendments-v1.png"
ON_FX_SOURCE = SOURCE_DIR / "on-effects-reference-v1.png"
BROKEN_FX_REFERENCE = SOURCE_DIR / "broken-effects-reference-v2.png"
V1 = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1"
BIN_V28 = ROOT / "art/raw/kitchen-bin-states-2026-10-18-v28"
BIN_V31 = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v31"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-states-v2"
ASSETS = PUBLIC / "assets"

HASHES = {
    ON_SOURCE: "f7e459c8c39db0fc77b995cbdcdc31b569eaf9f54c1267991e32e077ff445086",
    BROKEN_SOURCE: "8a3f278218711a4684e9fdc7bdf318d19af29d8d768342ed5c7def4a53a141d8",
    ON_FX_SOURCE: "fb76d72ac18bbbdc1dbd5235c30e4f3824e3ebf2f6f107eed1b29fa5aecc6e5f",
    BROKEN_FX_REFERENCE: "a0b422980d159cffaba8fb8b782a4a8a2f21670b53cbf9c5136cbfe3caf68248",
}

ROOM = (772, 224)
RUN_X = 84
BAY = 84
BAY_NAMES = ("fridge", "kettle", "toaster", "oven", "bowl", "basin")
BIN_ORIGIN = (8, 149)
TABLE_ORIGIN = (680, 148)
FPS = 4
FRAMES = 40
FX_CELL = (120, 144)

FX = {
    "kettle-on-steam": {"origin": (122, 20), "state": "on", "asset": "kettle", "sfx": "kitchen_kettle_boiling_steam_loop"},
    "toaster-on-heat": {"origin": (234, 15), "state": "on", "asset": "toaster", "sfx": "kitchen_toaster_heat_hum_loop"},
    "basin-on-flow": {"origin": (492, 60), "state": "on", "asset": "basin", "sfx": "kitchen_basin_gentle_flow_loop"},
    "fridge-broken-drip": {"origin": (44, 80), "state": "broken", "asset": "fridge", "sfx": "kitchen_fridge_slow_drip_loop"},
    "kettle-broken-steam": {"origin": (132, 0), "state": "broken", "asset": "kettle", "sfx": "kitchen_kettle_broken_pressure_hiss_loop"},
    "toaster-broken-smoke": {"origin": (234, 10), "state": "broken", "asset": "toaster", "sfx": "kitchen_toaster_burnt_smoke_crackle_loop"},
    "oven-broken-smoke": {"origin": (318, 0), "state": "broken", "asset": "oven", "sfx": "kitchen_oven_broken_smoke_hiss_loop"},
    "oven-broken-flicker": {"origin": (318, 74), "state": "broken", "asset": "oven", "sfx": "kitchen_oven_broken_warning_flicker_loop"},
    "basin-broken-spray": {"origin": (492, 20), "state": "broken", "asset": "basin", "sfx": "kitchen_basin_broken_upward_spray_loop"},
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def clean_alpha(image: Image.Image, threshold: int = 16) -> Image.Image:
    result = image.convert("RGBA")
    pixels = result.load()
    for y in range(result.height):
        for x in range(result.width):
            r, g, b, a = pixels[x, y]
            if a < threshold:
                pixels[x, y] = (0, 0, 0, 0)
    return result


def normalize_run(source: Image.Image) -> Image.Image:
    output = Image.new("RGBA", (504, 113))
    segments = (((169, 200, 1714, 289), 29), ((169, 289, 1714, 345), 17), ((169, 345, 1714, 615), 67))
    y = 0
    for crop, height in segments:
        section = clean_alpha(source.crop(crop)).resize((504, height), Image.Resampling.LANCZOS)
        output.alpha_composite(clean_alpha(section), (0, y))
        y += height
    return output


def broken_fridge_extended(source: Image.Image) -> Image.Image:
    # Apply the exact V1 piecewise coordinate mapping to the damage extending
    # left of the bay and below the cabinet baseline. Target room x=44..168,
    # y=105..224; the floor puddle remains flat on the actual floor surface.
    output = Image.new("RGBA", (124, 119))
    segments = (((45, 200, 427, 289), 29), ((45, 289, 427, 345), 17), ((45, 345, 427, 615), 67), ((45, 615, 427, 690), 6))
    y = 0
    for crop, height in segments:
        section = clean_alpha(source.crop(crop)).resize((124, height), Image.Resampling.LANCZOS)
        output.alpha_composite(clean_alpha(section), (0, y))
        y += height
    # The generated puddle is deliberately reinforced as a flat floor plane,
    # then kept behind the amended door/carcass. This prevents the old floating
    # pool failure while preserving every damage pixel above it.
    puddle = Image.new("RGBA", output.size)
    draw = ImageDraw.Draw(puddle)
    draw.ellipse((2, 109, 117, 118), fill=(44, 115, 157, 115), outline=(23, 73, 108, 205), width=1)
    draw.ellipse((18, 111, 104, 116), fill=(126, 208, 232, 128), outline=(194, 240, 250, 180), width=1)
    draw.line((30, 113, 91, 113), fill=(226, 249, 252, 180), width=1)
    puddle.alpha_composite(output)
    return puddle


def cell_from_run(run: Image.Image, index: int) -> Image.Image:
    cell = Image.new("RGBA", (84, 120))
    cell.alpha_composite(run.crop((index * 84, 0, (index + 1) * 84, 113)), (0, 7))
    return cell


def merge_upper(base: Image.Image, amended: Image.Image, split: int = 53) -> Image.Image:
    result = base.copy()
    # Replace, never superimpose: clear the complete amended upper zone first.
    result.paste((0, 0, 0, 0), (0, 0, 84, split))
    result.alpha_composite(amended.crop((0, 0, 84, split)), (0, 0))
    return result


def effect_source(third: int, target: tuple[int, int]) -> Image.Image:
    source = Image.open(ON_FX_SOURCE).convert("RGBA").crop((third * 724, 0, (third + 1) * 724, 724))
    mask = source.getchannel("A").point(lambda value: 255 if value >= 64 else 0)
    box = mask.getbbox()
    if box is None:
        raise RuntimeError("generated effect source is empty")
    crop = clean_alpha(source.crop(box), 64).resize(target, Image.Resampling.LANCZOS)
    return clean_alpha(crop, 12)


def alpha_scaled(image: Image.Image, factor: float) -> Image.Image:
    result = image.copy()
    alpha = result.getchannel("A").point(lambda value: max(0, min(255, round(value * factor))))
    result.putalpha(alpha)
    return result


def warped_source_frame(base: Image.Image, frame: int, bottom: int, amplitude: int = 2) -> Image.Image:
    result = Image.new("RGBA", FX_CELL)
    phase = frame * math.tau / FRAMES
    x0 = (FX_CELL[0] - base.width) // 2
    y0 = bottom - base.height
    for y in range(base.height):
        strength = (base.height - y) / base.height
        offset = round(math.sin(phase + y * 0.075) * amplitude * strength)
        strip = base.crop((0, y, base.width, y + 1))
        result.alpha_composite(strip, (x0 + offset, y0 + y))
    return result


def smoke_frame(frame: int, large: bool) -> Image.Image:
    image = Image.new("RGBA", FX_CELL)
    draw = ImageDraw.Draw(image)
    phase = frame * math.tau / FRAMES
    levels = (132, 118, 102, 84, 66, 49, 34, 22) if large else (132, 118, 103, 87, 72, 58, 46, 36)
    points = []
    for i, y in enumerate(levels):
        rise = i / (len(levels) - 1)
        swing = (4 + rise * (10 if large else 6))
        x = round(60 + math.sin(phase + i * 0.77) * swing + math.sin(phase * .41 + i * 1.12) * rise * 4)
        points.append((x, y))
    dark = (38, 45, 57, 185 if large else 165)
    mid = (76, 82, 91, 205 if large else 188)
    light = (151, 151, 148, 80)
    for i in range(len(points) - 1):
        width = (14 + i * 2) if large else (8 + i)
        draw.line((points[i], points[i + 1]), fill=dark, width=width, joint="curve")
    draw.line(points, fill=mid, width=10 if large else 6, joint="curve")
    # One off-centre highlight keeps the middle filled rather than splitting
    # into the twin hollow ribbons rejected in the first composite check.
    highlight = [(x - 2, y) for x, y in points[2:7]]
    draw.line(highlight, fill=light, width=2, joint="curve")
    # Only the large oven plume receives short attached billows; neither effect
    # creates a second independent smoke stem or round bubble chain.
    if large:
        for index, direction in ((5, -1), (6, 1)):
            start = points[index]
            tip = (start[0] + direction * 13, start[1] - 6)
            draw.line((start, tip), fill=dark, width=8, joint="curve")
            draw.line((start, tip), fill=mid, width=5, joint="curve")
    return image


def fridge_drip_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", FX_CELL)
    draw = ImageDraw.Draw(image)
    phase = frame % 20
    x = 84 + round(math.sin(frame * .63))
    y = 54 + phase * 3
    if y < 114:
        draw.polygon(((x, y - 4), (x - 2, y), (x, y + 3), (x + 2, y)), fill=(74, 180, 228, 220))
        draw.point((x, y - 1), fill=(222, 248, 255, 255))
    ripple_age = (phase - 1) % 20
    if ripple_age < 9:
        width = 5 + ripple_age * 2
        alpha = 185 - ripple_age * 18
        draw.ellipse((84 - width, 120 - ripple_age // 3, 84 + width, 124 + ripple_age // 3), outline=(75, 186, 229, alpha), width=1)
    return image


def water_spray_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", FX_CELL)
    draw = ImageDraw.Draw(image)
    phase = frame * math.tau / FRAMES
    root = (61, 124)
    blue = (41, 157, 225, 225)
    light = (190, 241, 255, 245)
    for branch, lean in enumerate((-23, -12, 0, 14, 25)):
        height = 65 + branch % 3 * 9 + round(4 * math.sin(phase + branch))
        tip = (root[0] + lean + round(3 * math.sin(phase * 1.3 + branch)), root[1] - height)
        mid = (root[0] + lean // 3, root[1] - height // 2)
        draw.line((root, mid, tip), fill=blue, width=4 if branch == 2 else 3, joint="curve")
        draw.line((root, mid, tip), fill=light, width=1, joint="curve")
        drop = (tip[0] + (branch - 2) * 2, tip[1] - 5)
        draw.ellipse((drop[0] - 1, drop[1] - 2, drop[0] + 1, drop[1] + 2), fill=blue)
    return image


def warning_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", FX_CELL)
    draw = ImageDraw.Draw(image)
    red_on = frame in {0, 1, 3, 4, 7, 8, 9, 13, 14, 18, 19, 20, 25, 27, 28, 32, 33, 37, 39}
    cavity_on = frame in {5, 6, 15, 16, 22, 23, 34, 35}
    if red_on:
        draw.ellipse((83, 77, 91, 85), fill=(123, 8, 5, 145))
        draw.ellipse((85, 79, 89, 83), fill=(255, 34, 14, 255))
        for point in ((82, 81), (92, 81), (87, 76), (87, 86)):
            draw.point(point, fill=(255, 74, 25, 230))
    if cavity_on:
        alpha = 178 if frame % 2 else 128
        draw.polygon(((43, 97), (89, 97), (87, 130), (44, 130)), fill=(255, 122, 20, alpha))
        draw.line((47, 101, 85, 101), fill=(255, 220, 112, min(240, alpha + 45)), width=1)
    return image


def make_strip(builder) -> Image.Image:
    strip = Image.new("RGBA", (FX_CELL[0] * FRAMES, FX_CELL[1]))
    for frame in range(FRAMES):
        cell = builder(frame)
        strip.alpha_composite(cell, (frame * FX_CELL[0], 0))
    return strip


def make_effects() -> dict[str, Image.Image]:
    steam = effect_source(0, (38, 72))
    heat = effect_source(1, (34, 74))
    water = effect_source(2, (22, 54))
    return {
        "kettle-on-steam": make_strip(lambda f: warped_source_frame(alpha_scaled(steam, .78 + .12 * math.sin(f * math.tau / FRAMES)), f, 116, 2)),
        "toaster-on-heat": make_strip(lambda f: warped_source_frame(alpha_scaled(heat, .58 + .12 * math.sin(f * math.tau / 10)), f, 119, 1)),
        "basin-on-flow": make_strip(lambda f: warped_source_frame(alpha_scaled(water, .74 + .12 * math.sin(f * math.tau / 8)), f, 118, 1)),
        "fridge-broken-drip": make_strip(fridge_drip_frame),
        "kettle-broken-steam": make_strip(lambda f: warped_source_frame(alpha_scaled(steam.resize((62, 118), Image.Resampling.LANCZOS), .82), f, 138, 4)),
        "toaster-broken-smoke": make_strip(lambda f: smoke_frame(f, False)),
        "oven-broken-smoke": make_strip(lambda f: smoke_frame(f, True)),
        "oven-broken-flicker": make_strip(warning_frame),
        "basin-broken-spray": make_strip(water_spray_frame),
    }


def compose_room(background: Image.Image, table: Image.Image, cells: dict[str, dict[str, Image.Image]], states: dict[str, str], bin_state: str) -> Image.Image:
    room = background.copy()
    bin_file = BIN_V28 / ("bin-broken-overflowing.png" if bin_state == "broken" else "bin-standard.png")
    room.alpha_composite(Image.open(bin_file).convert("RGBA"), BIN_ORIGIN)
    for index, asset in enumerate(BAY_NAMES):
        state = states[asset]
        sprite = cells[asset][state]
        if asset == "fridge" and state == "broken":
            room.alpha_composite(sprite, (44, 105))
        else:
            room.alpha_composite(sprite, (RUN_X + index * BAY, 98))
    room.alpha_composite(table, TABLE_ORIGIN)
    return room


def composite_effect(room: Image.Image, strip: Image.Image, origin: tuple[int, int], frame: int) -> None:
    cell = strip.crop((frame * FX_CELL[0], 0, (frame + 1) * FX_CELL[0], FX_CELL[1]))
    room.alpha_composite(cell, origin)


def build_page(catalogue: dict) -> str:
    options = {
        "fridge": ("standard", "broken"),
        "kettle": ("standard", "on", "broken"),
        "toaster": ("standard", "on", "broken"),
        "oven": ("standard", "on", "broken"),
        "bowl": ("standard", "broken"),
        "basin": ("standard", "on", "broken"),
        "bin": ("standard", "broken"),
    }
    selects = "".join(f'<label>{asset.title()}<select data-asset="{asset}">' + "".join(f'<option value="{state}">{state.title()}</option>' for state in states) + "</select></label>" for asset, states in options.items())
    cards = "".join(
        f'<article><h3>{asset.title()} · {state.title()}</h3><div class="cell"><img data-media src="assets/{asset}-{state}.png" alt="{asset} {state} amendment"></div></article>'
        for asset in BAY_NAMES for state in options[asset]
    )
    media = ["kitchen-standard-v2.png", "kitchen-all-on-static.png", "kitchen-all-broken-static.png", "kitchen-mixed-static.png", "bin-standard.png", "bin-broken.png", "table-chair.png"]
    media += [f"{asset}-{state}.png" for asset in BAY_NAMES for state in options[asset]]
    media += [f"fx-{name}-f40.png" for name in FX]
    media += ["fx-bin-stench-f40.png", "fx-bin-flies-f40.png"]
    metadata = json.dumps({"effects": catalogue["effects"], "states": options, "media": media})
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-rebuild-states-v2/"><title>Kitchen Rebuild V2 · amended state mixer</title><style>
:root{{--ink:#eff8ff;--muted:#abc0d4;--panel:#12253b;--line:#355474;--accent:#79dde0;--hot:#ffb34d}}*{{box-sizing:border-box}}body{{margin:0;background:#08131f;color:var(--ink);font:15px/1.48 system-ui,sans-serif}}main{{max-width:1240px;margin:auto;padding:28px}}h1,h2,h3{{line-height:1.15}}p{{color:var(--muted);max-width:92ch}}.tags,.controls,.selectors{{display:flex;gap:8px;flex-wrap:wrap;align-items:end}}.tag{{border:1px solid var(--line);border-radius:999px;padding:4px 9px;color:var(--accent)}}section,article{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}}section{{margin:18px 0}}.stage{{overflow:auto;background:#050a10;padding:12px;border-radius:8px}}canvas{{display:block;width:772px;height:224px;image-rendering:pixelated}}.zoom canvas{{width:1544px;height:448px}}button,select{{background:#143c55;color:white;border:1px solid #5d829f;border-radius:7px;padding:8px 10px}}button:disabled,select:disabled{{opacity:.45}}label{{display:grid;gap:4px;color:var(--muted);font-size:12px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(220px,1fr));gap:12px}}.cell{{height:260px;display:flex;align-items:end;justify-content:center;background:linear-gradient(#f6e7c6 0 78%,#b94e2d 78%);overflow:hidden;border-radius:8px}}.cell img{{height:240px;width:auto;image-rendering:pixelated}}.warn{{border-left:4px solid var(--hot);padding-left:12px}}code{{color:#b5edf0}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body><main><div class="tags"><span class="tag">Rebuild V2 amendment draft</span><span class="tag">Exact V1 geometry</span><span class="tag">40 frames · 4 fps · 10 seconds</span><span class="tag">No cabinet rerender</span></div><h1>Kitchen state family · On, Broken and mixed</h1><p>The V1 run remains the construction authority. V2 changes only the state-bearing pixels inside each existing bay; environmental motion is drawn from separate reusable strips. The fridge door is now white in every state.</p><p id="loading">Loading and decoding all state cells and effect strips…</p><div class="controls"><button id="play" disabled>Play all loops</button><button id="pause" disabled>Pause</button><button id="zoom" disabled>Toggle 2× inspection</button></div>
<section><h2>All On · complete kitchen at native game size</h2><div class="stage"><canvas id="all-on" width="772" height="224"></canvas></div><p>Kettle steam, toaster heat and basin flow animate. The oven light, roasting dish and solid red indicator remain deliberately steady.</p></section>
<section><h2>All Broken · complete kitchen at native game size</h2><div class="stage"><canvas id="all-broken" width="772" height="224"></canvas></div><p>Includes the accepted broken bin and its approved V31 smell/flies, plus the amended fridge, kettle, toaster, oven, bowl and basin states.</p></section>
<section><h2>Intermingled state mixer</h2><div class="controls"><button data-preset="standard" disabled>All standard</button><button data-preset="on" disabled>All On</button><button data-preset="broken" disabled>All Broken</button><button data-preset="mixed" disabled>Alternating mix</button><button data-preset="random" disabled>Random mix</button></div><div class="selectors" style="margin:12px 0">{selects}</div><div class="stage"><canvas id="mixed" width="772" height="224"></canvas></div><p>Each redraw starts from the empty V1 background and composes exactly one state per asset—there is no intact appliance hidden underneath a replacement.</p></section>
<h2>Isolated state amendments</h2><div class="grid">{cards}</div>
<section><h2>Named SFX placeholders</h2><p><code>kitchen_kettle_boiling_steam_loop</code> · <code>kitchen_toaster_heat_hum_loop</code> · <code>kitchen_oven_on_fan_loop</code> · <code>kitchen_basin_gentle_flow_loop</code> · <code>kitchen_fridge_low_electrical_buzz_loop</code> · <code>kitchen_fridge_slow_drip_loop</code> · <code>kitchen_kettle_broken_pressure_hiss_loop</code> · <code>kitchen_toaster_burnt_smoke_crackle_loop</code> · <code>kitchen_oven_broken_smoke_hiss_loop</code> · <code>kitchen_oven_broken_warning_flicker_loop</code> · <code>kitchen_bowl_ceramic_break_one_shot</code> · <code>kitchen_basin_broken_upward_spray_loop</code> · <code>kitchen_bin_flies_slow_loop</code>.</p></section>
<p class="warn"><strong>Review boundary:</strong> reversible V2 draft only. No Final/runtime promotion. V1 stays immutable and can be restored by discarding the V2 directories alone.</p>
<script>const DATA={metadata};const A='assets/';const images={{}};const state={{playing:true,frame:0,last:0,mix:{{fridge:'broken',kettle:'on',toaster:'broken',oven:'on',bowl:'broken',basin:'on',bin:'broken'}}}};const image=name=>images[name];const load=name=>new Promise((ok,bad)=>{{const i=new Image();i.onload=()=>i.decode().then(()=>{{images[name]=i;ok()}}).catch(bad);i.onerror=bad;i.src=A+name}});const frame=(ctx,img,n,w=120,h=144,x=0,y=0)=>ctx.drawImage(img,n*w,0,w,h,x,y,w,h);const drawBase=(ctx,states)=>{{ctx.clearRect(0,0,772,224);ctx.drawImage(image('kitchen-background.png'),0,0);ctx.drawImage(image(states.bin==='broken'?'bin-broken.png':'bin-standard.png'),8,149);for(const [index,asset] of ['fridge','kettle','toaster','oven','bowl','basin'].entries()){{const value=states[asset];const name=`${{asset}}-${{value}}.png`;if(asset==='fridge'&&value==='broken')ctx.drawImage(image(name),44,105);else ctx.drawImage(image(name),84+index*84,98)}}ctx.drawImage(image('table-chair.png'),680,148)}};const fx=(ctx,states,n)=>{{for(const [name,meta] of Object.entries(DATA.effects))if(states[meta.asset]===meta.state)frame(ctx,image(meta.file),n,120,144,...meta.origin);if(states.bin==='broken'){{frame(ctx,image('fx-bin-stench-f40.png'),n,80,80,4,104);frame(ctx,image('fx-bin-flies-f40.png'),n,80,80,4,104)}}}};const presets={{standard:{{fridge:'standard',kettle:'standard',toaster:'standard',oven:'standard',bowl:'standard',basin:'standard',bin:'standard'}},on:{{fridge:'standard',kettle:'on',toaster:'on',oven:'on',bowl:'standard',basin:'on',bin:'standard'}},broken:{{fridge:'broken',kettle:'broken',toaster:'broken',oven:'broken',bowl:'broken',basin:'broken',bin:'broken'}},mixed:{{fridge:'broken',kettle:'on',toaster:'broken',oven:'on',bowl:'broken',basin:'on',bin:'broken'}}}};const draw=(id,states)=>{{const ctx=document.querySelector(id).getContext('2d');ctx.imageSmoothingEnabled=false;drawBase(ctx,states);fx(ctx,states,state.frame)}};const render=()=>{{draw('#all-on',presets.on);draw('#all-broken',presets.broken);draw('#mixed',state.mix)}};const tick=t=>{{if(state.playing&&t-state.last>=250){{state.frame=(state.frame+1)%40;state.last=t;render()}}requestAnimationFrame(tick)}};Promise.all(DATA.media.map(load).concat(load('kitchen-background.png'))).then(()=>{{document.querySelector('#loading').textContent='All state cells and effect strips loaded and decoded.';document.querySelectorAll('button,select').forEach(x=>x.disabled=false);render();requestAnimationFrame(tick)}}).catch(e=>document.querySelector('#loading').textContent='A review asset failed to load: '+e);document.querySelector('#play').onclick=()=>state.playing=true;document.querySelector('#pause').onclick=()=>state.playing=false;document.querySelector('#zoom').onclick=()=>document.querySelectorAll('.stage').forEach(x=>x.classList.toggle('zoom'));document.querySelectorAll('select[data-asset]').forEach(select=>{{select.value=state.mix[select.dataset.asset];select.onchange=()=>{{state.mix[select.dataset.asset]=select.value;render()}}}});document.querySelectorAll('[data-preset]').forEach(button=>button.onclick=()=>{{const name=button.dataset.preset;if(name==='random')for(const [asset,states] of Object.entries(DATA.states))state.mix[asset]=states[Math.floor(Math.random()*states.length)];else state.mix={{...presets[name]}};document.querySelectorAll('select[data-asset]').forEach(s=>s.value=state.mix[s.dataset.asset]);render()}});</script></main></body></html>'''


def main() -> None:
    for path, expected in HASHES.items():
        assert sha(path) == expected, f"source hash changed: {path}"
    for directory in (RAW, DRAFT, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    base_run = Image.open(V1 / "standard-fitted-run.png").convert("RGBA")
    background = Image.open(V1 / "kitchen-standard-background.png").convert("RGBA")
    table = Image.open(V1 / "standard-table-chair.png").convert("RGBA")
    on_run = normalize_run(Image.open(ON_SOURCE).convert("RGBA"))
    broken_source = Image.open(BROKEN_SOURCE).convert("RGBA")
    broken_run = normalize_run(broken_source)

    base_cells = {name: cell_from_run(base_run, i) for i, name in enumerate(BAY_NAMES)}
    on_cells = {name: cell_from_run(on_run, i) for i, name in enumerate(BAY_NAMES)}
    broken_cells = {name: cell_from_run(broken_run, i) for i, name in enumerate(BAY_NAMES)}

    cells: dict[str, dict[str, Image.Image]] = {name: {} for name in BAY_NAMES}
    # White fridge from the localized On edit becomes the V2 standard authority.
    cells["fridge"]["standard"] = on_cells["fridge"]
    cells["fridge"]["broken"] = broken_fridge_extended(broken_source)
    cells["kettle"]["standard"] = base_cells["kettle"]
    cells["kettle"]["on"] = base_cells["kettle"]  # boiling motion is effect-only
    cells["kettle"]["broken"] = merge_upper(base_cells["kettle"], broken_cells["kettle"])
    cells["toaster"]["standard"] = base_cells["toaster"]
    cells["toaster"]["on"] = merge_upper(base_cells["toaster"], on_cells["toaster"])
    cells["toaster"]["broken"] = merge_upper(base_cells["toaster"], broken_cells["toaster"])
    cells["oven"]["standard"] = base_cells["oven"]
    cells["oven"]["on"] = on_cells["oven"]
    cells["oven"]["broken"] = broken_cells["oven"]
    cells["bowl"]["standard"] = base_cells["bowl"]
    cells["bowl"]["broken"] = merge_upper(base_cells["bowl"], broken_cells["bowl"])
    cells["basin"]["standard"] = base_cells["basin"]
    cells["basin"]["on"] = base_cells["basin"]  # flowing water is effect-only
    cells["basin"]["broken"] = merge_upper(base_cells["basin"], broken_cells["basin"])

    outputs: dict[str, dict[str, object]] = {}
    for asset, states in cells.items():
        for state, image in states.items():
            filename = f"{asset}-{state}.png"
            save(image, RAW / filename)
            copy(RAW / filename, ASSETS / filename)
            outputs[filename] = {"sha256": sha(RAW / filename), "pixels": list(image.size)}

    fixed = {
        "kitchen-background.png": background,
        "table-chair.png": table,
    }
    for filename, image in fixed.items():
        save(image, RAW / filename); copy(RAW / filename, ASSETS / filename)
        outputs[filename] = {"sha256": sha(RAW / filename), "pixels": list(image.size)}
    for source, filename in ((BIN_V28 / "bin-standard.png", "bin-standard.png"), (BIN_V28 / "bin-broken-overflowing.png", "bin-broken.png")):
        copy(source, RAW / filename); copy(source, ASSETS / filename)
        outputs[filename] = {"sha256": sha(source), "pixels": [72, 72]}

    effects = make_effects()
    effect_meta = {}
    for name, strip in effects.items():
        filename = f"fx-{name}-f40.png"
        save(strip, RAW / filename); copy(RAW / filename, ASSETS / filename)
        outputs[filename] = {"sha256": sha(RAW / filename), "pixels": list(strip.size)}
        effect_meta[name] = {**FX[name], "file": filename, "frames": FRAMES, "fps": FPS, "durationSeconds": 10, "cellPixels": list(FX_CELL), "reusable": True, "effectOnly": True}
    for source, filename in ((BIN_V31 / "fx-stench-miasma-f40.png", "fx-bin-stench-f40.png"), (BIN_V31 / "fx-slow-flies-f40.png", "fx-bin-flies-f40.png")):
        copy(source, RAW / filename); copy(source, ASSETS / filename)
        outputs[filename] = {"sha256": sha(source), "pixels": [3200, 80]}

    all_on = {"fridge": "standard", "kettle": "on", "toaster": "on", "oven": "on", "bowl": "standard", "basin": "on"}
    all_broken = {name: "broken" for name in BAY_NAMES}
    mixed = {"fridge": "broken", "kettle": "on", "toaster": "broken", "oven": "on", "bowl": "broken", "basin": "on"}
    rooms = {
        "kitchen-standard-v2.png": compose_room(background, table, cells, {name: "standard" for name in BAY_NAMES}, "standard"),
        "kitchen-all-on-static.png": compose_room(background, table, cells, all_on, "standard"),
        "kitchen-all-broken-static.png": compose_room(background, table, cells, all_broken, "broken"),
        "kitchen-mixed-static.png": compose_room(background, table, cells, mixed, "broken"),
    }
    for filename, image in rooms.items():
        save(image, RAW / filename); copy(RAW / filename, ASSETS / filename)
        outputs[filename] = {"sha256": sha(RAW / filename), "pixels": list(image.size)}

    # Still previews use representative loop frames without baking effects into
    # any state object.
    previews = {}
    for name, states, bin_state, frame_index in (("all-on", all_on, "standard", 8), ("all-broken", all_broken, "broken", 13), ("mixed", mixed, "broken", 24)):
        preview = compose_room(background, table, cells, states, bin_state)
        for effect_name, meta in effect_meta.items():
            if states[meta["asset"]] == meta["state"]:
                composite_effect(preview, effects[effect_name], tuple(meta["origin"]), frame_index)
        if bin_state == "broken":
            for bin_fx in (BIN_V31 / "fx-stench-miasma-f40.png", BIN_V31 / "fx-slow-flies-f40.png"):
                strip = Image.open(bin_fx).convert("RGBA")
                preview.alpha_composite(strip.crop((frame_index * 80, 0, frame_index * 80 + 80, 80)), (4, 104))
        filename = f"kitchen-{name}-preview.png"
        save(preview, RAW / filename); copy(RAW / filename, ASSETS / filename)
        outputs[filename] = {"sha256": sha(RAW / filename), "pixels": list(preview.size)}
        previews[name] = filename

    catalogue = {
        "set": SET,
        "version": 2,
        "status": "amended-state-family-awaiting-review",
        "foundation": {"set": "kitchen-rebuild-foundation-2026-10-18-v1", "immutable": True, "roomPixels": list(ROOM), "bayWidthPixels": BAY, "bayCount": 6},
        "method": {"amendmentsNotRerenders": True, "sharedCabinetAuthority": "V1", "environmentalEffectsSeparate": True, "fridgeDoorColour": "warm-white-ivory-enamel"},
        "states": {asset: list(states.keys()) for asset, states in cells.items()},
        "allOn": {**all_on, "bin": "standard"},
        "allBroken": {**all_broken, "bin": "broken"},
        "mixedPreset": {**mixed, "bin": "broken"},
        "effects": effect_meta,
        "acceptedBinEffects": {"stench": "exact V31", "flies": "exact V31"},
        "sfxPlaceholders": [meta["sfx"] for meta in FX.values()] + ["kitchen_oven_on_fan_loop", "kitchen_fridge_low_electrical_buzz_loop", "kitchen_bowl_ceramic_break_one_shot", "kitchen_bin_flies_slow_loop"],
        "outputs": outputs,
        "previews": previews,
        "promotion": "none",
        "runtimeWiring": "unchanged",
    }
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({"set": SET, "status": "awaiting-complete-state-family-visual-review", "preserves": ["Rebuild V1", "approved V28/V31 bin"], "promotion": "none", "runtimeWiring": "unchanged", "rollback": "Delete only V2 source/raw/draft/review/archive/builder/verifier/docs files; V1 remains exact."}, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: {len(outputs)} outputs, {len(effect_meta)} new effect strips")


if __name__ == "__main__":
    main()
