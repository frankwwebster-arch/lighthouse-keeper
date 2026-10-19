#!/usr/bin/env python3
"""Build Kitchen Sink Water Effects V14 from isolated generated keyframes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-sink-water-effects-2026-10-19-v14"
SOURCE = ROOT / "art/source" / SET
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-sink-water-effects-v14"
ASSETS = PUBLIC / "assets"
ON_SOURCE = SOURCE / "on-water-keyframes-source.png"
BROKEN_SOURCE = SOURCE / "broken-basin-spouts-keyframes-source.png"
SINK = ROOT / "art/raw/kitchen-sink-cabinet-2026-10-19-v13/sink-cabinet-standard.png"
ROOM = ROOT / "art/raw/kitchen-sink-cabinet-2026-10-19-v13/cabinet-run-plus-sink-native-room.png"

CELL = (92, 108)
FRAME_COUNT = 40
FPS = 4
DURATION = 10


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def eight_cells(image: Image.Image) -> list[Image.Image]:
    return [image.crop((round(i * image.width / 8), 0, round((i + 1) * image.width / 8), image.height)) for i in range(8)]


def on_keys() -> list[Image.Image]:
    image = Image.open(ON_SOURCE).convert("RGBA")
    if image.size != (2172, 724):
        raise RuntimeError(f"Unexpected On source size {image.size}")
    result = []
    for source_cell in eight_cells(image):
        effect = Image.new("RGBA", source_cell.size, (0, 0, 0, 0))
        src = source_cell.load(); dst = effect.load()
        for y in range(source_cell.height):
            for x in range(source_cell.width):
                r, g, b, a = src[x, y]
                water_colour = (b > r * 1.18 and g > r * 1.03) or (r > 205 and g > 220 and b > 220)
                if a >= 8 and y >= 224 and water_colour:
                    dst[x, y] = (r, g, b, a)
        bbox = effect.getchannel("A").getbbox()
        if bbox is None:
            raise RuntimeError("On water keyframe has no isolated water")
        water = resize_premultiplied(effect.crop(bbox), (20, 20))
        cell = Image.new("RGBA", CELL, (0, 0, 0, 0))
        cell.alpha_composite(water, (44, 21))
        result.append(cell)
    return result


def broken_keys() -> list[Image.Image]:
    image = Image.open(BROKEN_SOURCE).convert("RGBA")
    if image.size != (2171, 724):
        raise RuntimeError(f"Unexpected Broken source size {image.size}")
    result = []
    for source_cell in eight_cells(image):
        effect = Image.new("RGBA", source_cell.size, (0, 0, 0, 0))
        src = source_cell.load(); dst = effect.load()
        for y in range(source_cell.height):
            for x in range(source_cell.width):
                r, g, b, a = src[x, y]
                water_colour = (b > r * 1.08 and g > r * 0.92) or (r > 190 and g > 205 and b > 220)
                if a >= 8 and water_colour:
                    dst[x, y] = (r, g, b, a)
        bbox = effect.getchannel("A").getbbox()
        if bbox is None:
            raise RuntimeError("Broken water keyframe has no water")
        water = resize_premultiplied(effect.crop(bbox), (48, 36))
        cell = Image.new("RGBA", CELL, (0, 0, 0, 0))
        cell.alpha_composite(water, (22, 4))
        result.append(cell)
    return result


def forty_frames(keys: list[Image.Image]) -> list[Image.Image]:
    frames = []
    for index in range(8):
        current = keys[index]
        following = keys[(index + 1) % 8]
        for subframe in range(5):
            frame = Image.blend(current, following, subframe / 5)
            pixels = frame.load()
            for y in range(frame.height):
                for x in range(frame.width):
                    if pixels[x, y][3] < 8:
                        pixels[x, y] = (0, 0, 0, 0)
            frames.append(frame)
    if len(frames) != FRAME_COUNT:
        raise RuntimeError("Interpolation did not produce 40 frames")
    return frames


def strip(frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (CELL[0] * FRAME_COUNT, CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        output.alpha_composite(frame, (index * CELL[0], 0))
    return output


def composite(base: Image.Image, effect: Image.Image) -> Image.Image:
    output = base.copy().convert("RGBA")
    output.alpha_composite(effect)
    return output


def room_composite(base: Image.Image, effect: Image.Image) -> Image.Image:
    output = base.copy().convert("RGBA")
    output.alpha_composite(effect, (332, 104))
    return output


def page() -> str:
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-sink-water-effects-v14/"><title>Kitchen Sink Water Effects V14 · animated review</title><style>
:root{color-scheme:dark;--bg:#07171e;--panel:#0d2630;--line:#276679;--ink:#eff9f6;--muted:#abc8c5;--sea:#72d9d3;--gold:#e8ad47}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:26px 20px 54px}h1{font-size:clamp(28px,4vw,46px);line-height:1.05;margin:.2rem 0 .5rem}h2{margin:0 0 9px}.lede{max-width:920px;color:var(--muted);font-size:17px}.tags{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 22px}.tag{border:1px solid var(--line);border-radius:999px;padding:6px 10px;background:#0b212a}.notice{border-left:4px solid var(--gold);background:#19262a;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:18px 0;overflow:auto}.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.card{background:#091d25;border:1px solid #214f5d;border-radius:10px;padding:12px}.stage{display:flex;justify-content:center;align-items:center;overflow:auto;background:#091a21;border-radius:8px;padding:14px}.isolated{width:368px;height:432px;image-rendering:auto}.room{width:772px;height:224px;display:block}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:10px 0}input{accent-color:var(--sea)}.status{font-weight:700;color:var(--sea)}@media(max-width:820px){.grid{grid-template-columns:1fr}}</style></head><body><main>
<div class="tags"><span class="tag">V14 reversible effect gate</span><span class="tag">40 frames</span><span class="tag">4 fps source</span><span class="tag">10-second loop</span><span class="tag">Static sink unchanged</span></div><h1>Sink water states</h1><p class="lede">On uses a narrow animated flow registered beneath the tap outlet. Broken leaves the tap and basin intact and adds several water spouts shooting upward from inside the basin.</p><p id="status" class="status">Loading and decoding all animation media…</p>
<p class="notice"><strong>Layer contract:</strong> both strips contain water pixels only. The complete standalone V13 sink cabinet remains byte-identical beneath Standard, On and Broken.</p>
<div class="controls"><button id="toggle" disabled>Pause</button><label>Speed <input id="speed" type="range" min="0.1" max="4" step="0.1" value="1" disabled></label><output id="speedOut">1.0×</output></div>
<section class="panel"><div class="grid"><div class="card"><h2>On · outlet flow</h2><div class="stage"><canvas class="isolated" id="onIso" width="92" height="108"></canvas></div><p>Gentle stream and small basin splash. Cue: <code>kitchen_sink_water_gentle_loop</code>.</p></div><div class="card"><h2>Broken · basin spouts</h2><div class="stage"><canvas class="isolated" id="brokenIso" width="92" height="108"></canvas></div><p>Three upward jets from within the basin. Cue: <code>kitchen_sink_pipe_burst_loop</code>.</p></div></div></section>
<section class="panel"><h2>On beside approved cabinet run · native game size</h2><div class="stage"><canvas class="room" id="onRoom" width="772" height="224"></canvas></div></section>
<section class="panel"><h2>Broken beside approved cabinet run · native game size</h2><div class="stage"><canvas class="room" id="brokenRoom" width="772" height="224"></canvas></div></section>
</main><script>
const urls={sink:'assets/sink-cabinet-static.png',room:'assets/cabinet-run-plus-sink-native-room.png',on:'assets/fx-sink-on-water-f40.png',broken:'assets/fx-sink-broken-basin-spouts-f40.png'};const media={};let playing=true,start=performance.now(),speed=1;const load=Object.entries(urls).map(([key,url])=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>image.decode().then(()=>{media[key]=image;resolve()}).catch(reject);image.onerror=reject;image.src=url}));
function drawEffect(ctx,strip,frame,dx=0,dy=0){ctx.drawImage(strip,frame*92,0,92,108,dx,dy,92,108)}function render(now){if(!media.sink)return;const frame=Math.floor(((now-start)/1000)*4*speed)%40;for(const [id,effect] of [['onIso','on'],['brokenIso','broken']]){const c=document.getElementById(id),x=c.getContext('2d');x.clearRect(0,0,92,108);x.drawImage(media.sink,0,0);drawEffect(x,media[effect],frame)}for(const [id,effect] of [['onRoom','on'],['brokenRoom','broken']]){const c=document.getElementById(id),x=c.getContext('2d');x.clearRect(0,0,772,224);x.drawImage(media.room,0,0);drawEffect(x,media[effect],frame,332,104)}if(playing)requestAnimationFrame(render)}
Promise.all(load).then(()=>{document.getElementById('status').textContent='All animation media loaded and decoded. Playback unlocked.';toggle.disabled=false;speed.disabled=false;requestAnimationFrame(render)}).catch(error=>document.getElementById('status').textContent='Media failed to decode: '+error.message);toggle.onclick=()=>{playing=!playing;toggle.textContent=playing?'Pause':'Play';if(playing){start=performance.now();requestAnimationFrame(render)}};speed.oninput=()=>{speed=Number(speed.value);speedOut.textContent=speed.toFixed(1)+'×';start=performance.now()}
</script></body></html>"""


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    on_frames = forty_frames(on_keys())
    broken_frames = forty_frames(broken_keys())
    on_strip = strip(on_frames)
    broken_strip = strip(broken_frames)
    sink = Image.open(SINK).convert("RGBA")
    room = Image.open(ROOM).convert("RGBA")
    outputs = {
        "sink-cabinet-static.png": sink,
        "cabinet-run-plus-sink-native-room.png": room,
        "fx-sink-on-water-f40.png": on_strip,
        "fx-sink-broken-basin-spouts-f40.png": broken_strip,
        "sink-on-frame-00.png": composite(sink, on_frames[0]),
        "sink-broken-frame-00.png": composite(sink, broken_frames[0]),
        "room-sink-on-frame-00.png": room_composite(room, on_frames[0]),
        "room-sink-broken-frame-00.png": room_composite(room, broken_frames[0]),
    }
    for name, image in outputs.items():
        save(image, RAW / name)
        (ASSETS / name).write_bytes((RAW / name).read_bytes())
    catalogue = {
        "set": SET,
        "status": "sink-water-effects-awaiting-visual-review",
        "staticAuthority": {"file": str(SINK.relative_to(ROOT)), "sha256": sha(SINK), "tapAndBasinChanged": False},
        "effects": {
            "onWater": {"file": "fx-sink-on-water-f40.png", "origin": "tap-outlet", "frames": 40, "fps": 4, "durationSeconds": 10, "cellPixels": list(CELL), "sfxCue": "kitchen_sink_water_gentle_loop"},
            "brokenWater": {"file": "fx-sink-broken-basin-spouts-f40.png", "origin": "inside-basin", "frames": 40, "fps": 4, "durationSeconds": 10, "cellPixels": list(CELL), "sfxCue": "kitchen_sink_pipe_burst_loop"},
        },
        "playback": {"sourceFps": 4, "speedMultiplierRange": [0.1, 4], "sourceDurationSeconds": 10},
        "outputs": {name: sha(RAW / name) for name in outputs},
        "boundaries": {"effectPixelsOnly": True, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    register = {"set": SET, "status": "reversible-unapproved-unpromoted", "files": {str(path.relative_to(ROOT)): sha(path) for path in [ON_SOURCE, BROKEN_SOURCE, SINK, ROOM, catalogue_path, *[RAW / name for name in outputs]]}}
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(page())
    print("Built Kitchen Sink Water Effects V14: outlet flow and upward basin-spout 40-frame loops")


if __name__ == "__main__":
    main()
