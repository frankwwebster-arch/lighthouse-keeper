#!/usr/bin/env python3
"""Build Kitchen Sink Perspective Correction V15 as a reversible review draft."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-sink-perspective-correction-2026-10-19-v15"
SOURCE = ROOT / "art/source" / SET / "sink-cabinet-perspective-redraw.png"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-sink-perspective-correction-v15"
ASSETS = PUBLIC / "assets"
CABINET = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"
BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"
V14_ON = ROOT / "art/raw/kitchen-sink-water-effects-2026-10-19-v14/fx-sink-on-water-f40.png"
V14_BROKEN = ROOT / "art/raw/kitchen-sink-water-effects-2026-10-19-v14/fx-sink-broken-basin-spouts-f40.png"

SOURCE_SHA = "0a442dd7efdd3aeaf3706faab49db877e9185c950bc6da8b269d97671a75ea93"
APPROVED_CABINET_SHA = "112dfb2ed337a15fe76b3fbe41cacf5c752eea93eed79b394eccc378370f6e81"
CELL = (92, 108)
BODY_SIZE = (84, 74)
BODY_ORIGIN = (4, 30)
FRAME_COUNT = 40
FPS = 4
DURATION = 10
ON_SHIFT_Y = -2
ROOM_SIZE = (772, 224)
RUN_CELL_ORIGIN = (164, 130)
SINK_CELL_ORIGIN = (332, 104)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def clean_alpha(image: Image.Image) -> Image.Image:
    output = image.copy().convert("RGBA")
    pixels = output.load()
    for y in range(output.height):
        for x in range(output.width):
            if pixels[x, y][3] < 8:
                pixels[x, y] = (0, 0, 0, 0)
    return output


def native_sink() -> Image.Image:
    if sha(SOURCE) != SOURCE_SHA:
        raise RuntimeError("V15 generated source changed")
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != (1346, 1168):
        raise RuntimeError(f"Unexpected generated source size {source.size}")

    # The complete unit is redrawn. These two source regions merely preserve
    # the required independent native heights: 26 px tap/headroom above an
    # exact 84 x 74 px standalone cabinet body.
    upper = resize_premultiplied(source.crop((151, 41, 1193, 336)), (84, 26))
    body = resize_premultiplied(source.crop((151, 336, 1193, 1124)), BODY_SIZE)
    cell = Image.new("RGBA", CELL, (0, 0, 0, 0))
    cell.alpha_composite(upper, (4, 4))
    cell.alpha_composite(body, BODY_ORIGIN)
    return clean_alpha(cell)


def translated_on_strip() -> Image.Image:
    source = Image.open(V14_ON).convert("RGBA")
    if source.size != (CELL[0] * FRAME_COUNT, CELL[1]):
        raise RuntimeError("V14 On strip geometry changed")
    output = Image.new("RGBA", source.size, (0, 0, 0, 0))
    for frame in range(FRAME_COUNT):
        key = source.crop((frame * CELL[0], 0, (frame + 1) * CELL[0], CELL[1]))
        output.alpha_composite(key, (frame * CELL[0], ON_SHIFT_Y))
    return output


def room_proof(sink: Image.Image) -> Image.Image:
    room = Image.open(BACKGROUND).convert("RGBA")
    cabinet = Image.open(CABINET).convert("RGBA")
    if room.size != ROOM_SIZE or cabinet.size != (176, 82):
        raise RuntimeError("Room or approved cabinet authority geometry changed")
    if sha(CABINET) != APPROVED_CABINET_SHA:
        raise RuntimeError("Approved V11 cabinet authority changed")
    room.alpha_composite(cabinet, RUN_CELL_ORIGIN)
    room.alpha_composite(sink, SINK_CELL_ORIGIN)
    return room


def composite(base: Image.Image, effect: Image.Image) -> Image.Image:
    output = base.copy()
    output.alpha_composite(effect)
    return output


def room_composite(base: Image.Image, effect: Image.Image) -> Image.Image:
    output = base.copy()
    output.alpha_composite(effect, SINK_CELL_ORIGIN)
    return output


def page() -> str:
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-sink-perspective-correction-v15/"><title>Kitchen Sink V15 · perspective and outlet correction</title><style>
:root{color-scheme:dark;--bg:#07171e;--panel:#0d2630;--line:#276679;--ink:#eff9f6;--muted:#abc8c5;--sea:#72d9d3;--gold:#e8ad47}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:26px 20px 54px}h1{font-size:clamp(28px,4vw,46px);line-height:1.05;margin:.2rem 0 .5rem}h2{margin:0 0 9px}.lede{max-width:930px;color:var(--muted);font-size:17px}.tags,.controls{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin:16px 0 22px}.tag{border:1px solid var(--line);border-radius:999px;padding:6px 10px;background:#0b212a}.notice{border-left:4px solid var(--gold);background:#19262a;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:18px 0;overflow:auto}.grid{display:grid;grid-template-columns:repeat(2,minmax(300px,1fr));gap:14px}.card{background:#091d25;border:1px solid #214f5d;border-radius:10px;padding:12px}.stage{display:flex;justify-content:center;align-items:center;width:max-content;min-width:100%;overflow:auto;background:#091a21;border-radius:8px;padding:14px}.checker{background-color:#091a21;background-image:linear-gradient(45deg,#112d37 25%,transparent 25%),linear-gradient(-45deg,#112d37 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#112d37 75%),linear-gradient(-45deg,transparent 75%,#112d37 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}.master{width:min(100%,700px);height:auto}.isolated{width:368px;height:432px;image-rendering:auto}.room{width:772px;height:224px;display:block}.status{font-weight:700;color:var(--sea)}input{accent-color:var(--sea)}@media(max-width:820px){.grid{grid-template-columns:1fr}}</style></head><body><main>
<div class="tags"><span class="tag">V15 reversible draft</span><span class="tag">84 × 74 px body</span><span class="tag">V11 parallel projection</span><span class="tag">40 frames · 4 fps · 10 seconds</span></div><h1>Sink perspective and tap-outlet correction</h1><p class="lede">The complete standalone sink cabinet has been redrawn to the approved V11 cabinet projection: a shallow constant-height worktop, parallel cabinet sides and matching front-plane proportions. The On flow now begins at the tap outlet. The approved Broken water animation is retained byte-for-byte.</p><p id="status" class="status">Loading and decoding all review media…</p>
<p class="notice"><strong>Review boundary:</strong> V13 and V14 remain immutable. This is a new unpromoted draft; no Final or runtime art changed.</p>
<section class="panel"><h2>Fresh high-resolution construction</h2><div class="stage checker"><img class="master" src="assets/sink-cabinet-perspective-redraw.png" alt="Fresh high-resolution standalone sink cabinet redraw"></div></section>
<section class="panel"><h2>Standard · exact native asset at 4×</h2><div class="stage checker"><canvas class="isolated" id="standard" width="92" height="108"></canvas></div><p class="lede">The installed cabinet body remains exactly 84 × 74 px inside a 92 × 108 px transparent cell.</p></section>
<section class="panel"><h2>Exact approved V11 run + corrected standalone sink · native game size</h2><div class="stage"><img class="room" src="assets/cabinet-run-plus-sink-native-room.png" alt="Approved cabinet run beside corrected standalone sink at native scale"></div></section>
<div class="controls"><button id="toggle" disabled>Pause</button><label>Speed <input id="speed" type="range" min="0.1" max="4" step="0.1" value="1" disabled></label><output id="speedOut">1.0×</output></div>
<section class="panel"><div class="grid"><div class="card"><h2>On · water touches outlet</h2><div class="stage"><canvas class="isolated" id="onIso" width="92" height="108"></canvas></div><p>Gentle flow; cue <code>kitchen_sink_water_gentle_loop</code>.</p></div><div class="card"><h2>Broken · approved animation retained</h2><div class="stage"><canvas class="isolated" id="brokenIso" width="92" height="108"></canvas></div><p>Upward basin jets; cue <code>kitchen_sink_pipe_burst_loop</code>.</p></div></div></section>
<section class="panel"><h2>On beside approved cabinets · native game size</h2><div class="stage"><canvas class="room" id="onRoom" width="772" height="224"></canvas></div></section>
<section class="panel"><h2>Broken beside approved cabinets · native game size</h2><div class="stage"><canvas class="room" id="brokenRoom" width="772" height="224"></canvas></div></section>
</main><script>
const urls={sink:'assets/sink-cabinet-standard.png',room:'assets/cabinet-run-plus-sink-native-room.png',on:'assets/fx-sink-on-water-f40.png',broken:'assets/fx-sink-broken-basin-spouts-f40.png'};const media={};let playing=true,start=performance.now(),speed=1;const load=Object.entries(urls).map(([key,url])=>new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>img.decode().then(()=>{media[key]=img;resolve()}).catch(reject);img.onerror=reject;img.src=url}));
function effect(ctx,strip,frame,dx=0,dy=0){ctx.drawImage(strip,frame*92,0,92,108,dx,dy,92,108)}function render(now){if(!media.sink)return;const frame=Math.floor(((now-start)/1000)*4*speed)%40;const s=document.getElementById('standard').getContext('2d');s.clearRect(0,0,92,108);s.drawImage(media.sink,0,0);for(const [id,key] of [['onIso','on'],['brokenIso','broken']]){const c=document.getElementById(id),x=c.getContext('2d');x.clearRect(0,0,92,108);x.drawImage(media.sink,0,0);effect(x,media[key],frame)}for(const [id,key] of [['onRoom','on'],['brokenRoom','broken']]){const c=document.getElementById(id),x=c.getContext('2d');x.clearRect(0,0,772,224);x.drawImage(media.room,0,0);effect(x,media[key],frame,332,104)}if(playing)requestAnimationFrame(render)}
Promise.all(load).then(()=>{status.textContent='All review media loaded and decoded. Playback unlocked.';toggle.disabled=false;speed.disabled=false;requestAnimationFrame(render)}).catch(error=>status.textContent='Review media failed to decode: '+error.message);toggle.onclick=()=>{playing=!playing;toggle.textContent=playing?'Pause':'Play';if(playing){start=performance.now();requestAnimationFrame(render)}};speed.oninput=()=>{speed=Number(speed.value);speedOut.textContent=speed.toFixed(1)+'×';start=performance.now()}
</script></body></html>"""


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    sink = native_sink()
    room = room_proof(sink)
    on_strip = translated_on_strip()

    outputs: dict[str, Image.Image] = {
        "sink-cabinet-standard.png": sink,
        "sink-cabinet-on-base.png": sink,
        "sink-cabinet-broken-base.png": sink,
        "cabinet-run-plus-sink-native-room.png": room,
        "fx-sink-on-water-f40.png": on_strip,
        "sink-on-frame-00.png": composite(sink, on_strip.crop((0, 0, *CELL))),
        "sink-broken-frame-00.png": composite(sink, Image.open(V14_BROKEN).convert("RGBA").crop((0, 0, *CELL))),
        "room-sink-on-frame-00.png": room_composite(room, on_strip.crop((0, 0, *CELL))),
        "room-sink-broken-frame-00.png": room_composite(room, Image.open(V14_BROKEN).convert("RGBA").crop((0, 0, *CELL))),
    }
    for name, image in outputs.items():
        save(image, RAW / name)
    shutil.copyfile(V14_BROKEN, RAW / "fx-sink-broken-basin-spouts-f40.png")
    shutil.copyfile(SOURCE, RAW / SOURCE.name)

    all_names = [*outputs, "fx-sink-broken-basin-spouts-f40.png", SOURCE.name]
    for name in all_names:
        shutil.copyfile(RAW / name, ASSETS / name)

    catalogue = {
        "set": SET,
        "status": "sink-perspective-and-outlet-correction-awaiting-visual-review",
        "construction": {
            "completeStandaloneOneBayUnit": True,
            "overlaysApprovedCabinet": False,
            "projection": "straight-on-flat-cutaway-parallel",
            "bodyPixels": list(BODY_SIZE),
            "cellPixels": list(CELL),
            "bodyOriginInCell": list(BODY_ORIGIN),
            "approvedCabinetAuthoritySha256": sha(CABINET),
            "sourceSha256": sha(SOURCE),
        },
        "states": {"staticBasesByteIdentical": True, "tapAndBasinChangedWhenBroken": False},
        "effects": {
            "onWater": {"frames": FRAME_COUNT, "fps": FPS, "durationSeconds": DURATION, "source": str(V14_ON.relative_to(ROOT)), "translationPixels": [0, ON_SHIFT_Y], "origin": "tap-outlet", "sfxCue": "kitchen_sink_water_gentle_loop"},
            "brokenWater": {"frames": FRAME_COUNT, "fps": FPS, "durationSeconds": DURATION, "source": str(V14_BROKEN.relative_to(ROOT)), "byteIdenticalToV14": True, "origin": "inside-basin", "sfxCue": "kitchen_sink_pipe_burst_loop"},
        },
        "playback": {"speedMultiplierRange": [0.1, 4], "sourceDurationSeconds": DURATION},
        "outputs": {name: sha(RAW / name) for name in all_names},
        "boundaries": {"v13Changed": False, "v14Changed": False, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    registered = [SOURCE, CABINET, BACKGROUND, V14_ON, V14_BROKEN, catalogue_path, *[RAW / name for name in all_names]]
    register = {"set": SET, "status": "reversible-unapproved-unpromoted", "files": {str(path.relative_to(ROOT)): sha(path) for path in registered}}
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(page())
    print("Built Kitchen Sink V15: V11 projection, outlet-connected On flow, byte-identical V14 Broken loop")


if __name__ == "__main__":
    main()
