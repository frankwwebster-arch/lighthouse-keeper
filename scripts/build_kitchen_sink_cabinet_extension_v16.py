#!/usr/bin/env python3
"""Build Kitchen Sink Cabinet Extension V16 from exact approved V11 geometry."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-sink-cabinet-extension-2026-10-19-v16"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-sink-cabinet-extension-v16"
ASSETS = PUBLIC / "assets"
V11 = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"
V15_SINK = ROOT / "art/raw/kitchen-sink-perspective-correction-2026-10-19-v15/sink-cabinet-standard.png"
V15_ON = ROOT / "art/raw/kitchen-sink-perspective-correction-2026-10-19-v15/fx-sink-on-water-f40.png"
V15_BROKEN = ROOT / "art/raw/kitchen-sink-perspective-correction-2026-10-19-v15/fx-sink-broken-basin-spouts-f40.png"
BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"

V11_SHA = "112dfb2ed337a15fe76b3fbe41cacf5c752eea93eed79b394eccc378370f6e81"
CELL = (92, 108)
BODY = (84, 74)
BODY_ORIGIN = (4, 30)
FRAME_COUNT = 40
FPS = 4
DURATION = 10
RUN_ORIGIN = (164, 130)
SINK_ORIGIN = (332, 104)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def exact_v11_bay() -> Image.Image:
    if sha(V11) != V11_SHA:
        raise RuntimeError("Approved V11 cabinet changed")
    run = Image.open(V11).convert("RGBA")
    if run.size != (176, 82):
        raise RuntimeError("Approved V11 cell geometry changed")
    # Use the complete right-hand 84 x 74 bay. Its left edge is the internal
    # joining seam and its right edge is the run end-cap, so an adjacent copy
    # reads as a literal extension while remaining a separate sprite.
    return run.crop((88, 4, 172, 78))


def fixture_only() -> Image.Image:
    source = Image.open(V15_SINK).convert("RGBA")
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    src = source.load()
    dst = output.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            r, g, b, a = src[x, y]
            if not a:
                continue
            keep = y < 30
            if 30 <= y <= 39 and 24 <= x <= 68:
                ivory = r >= 105 and g >= 95 and b >= 75
                copper = r >= 70 and r > g * 1.25 and g > b * 1.15
                drain = 40 <= x <= 52 and 33 <= y <= 38 and b > r * 1.1
                keep = ivory or copper or drain
            if keep:
                dst[x, y] = (r, g, b, a)
    return output


def standalone_sink(bay: Image.Image, fixture: Image.Image) -> Image.Image:
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    output.alpha_composite(bay, BODY_ORIGIN)
    output.alpha_composite(fixture)
    return output


def room_proof(sink: Image.Image) -> Image.Image:
    room = Image.open(BACKGROUND).convert("RGBA")
    run = Image.open(V11).convert("RGBA")
    room.alpha_composite(run, RUN_ORIGIN)
    room.alpha_composite(sink, SINK_ORIGIN)
    return room


def composite(base: Image.Image, effect: Image.Image) -> Image.Image:
    output = base.copy()
    output.alpha_composite(effect)
    return output


def room_composite(base: Image.Image, effect: Image.Image) -> Image.Image:
    output = base.copy()
    output.alpha_composite(effect, SINK_ORIGIN)
    return output


def page() -> str:
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-sink-cabinet-extension-v16/"><title>Kitchen Sink V16 · exact cabinet extension</title><style>
:root{color-scheme:dark;--bg:#07171e;--panel:#0d2630;--line:#276679;--ink:#eff9f6;--muted:#abc8c5;--sea:#72d9d3;--gold:#e8ad47}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:26px 20px 54px}h1{font-size:clamp(28px,4vw,46px);line-height:1.05;margin:.2rem 0 .5rem}h2{margin:0 0 9px}.lede{max-width:940px;color:var(--muted);font-size:17px}.tags,.controls{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin:16px 0 22px}.tag{border:1px solid var(--line);border-radius:999px;padding:6px 10px;background:#0b212a}.notice{border-left:4px solid var(--gold);background:#19262a;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:18px 0;overflow:auto}.grid{display:grid;grid-template-columns:repeat(3,minmax(240px,1fr));gap:14px}.card{background:#091d25;border:1px solid #214f5d;border-radius:10px;padding:12px}.stage{display:flex;justify-content:center;align-items:center;width:max-content;min-width:100%;overflow:auto;background:#091a21;border-radius:8px;padding:14px}.checker{background-color:#091a21;background-image:linear-gradient(45deg,#112d37 25%,transparent 25%),linear-gradient(-45deg,#112d37 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#112d37 75%),linear-gradient(-45deg,transparent 75%,#112d37 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}.bay{width:336px;height:296px;image-rendering:auto}.isolated{width:368px;height:432px;image-rendering:auto}.room{width:772px;height:224px;display:block}.status{font-weight:700;color:var(--sea)}input{accent-color:var(--sea)}@media(max-width:900px){.grid{grid-template-columns:1fr}}</style></head><body><main>
<div class="tags"><span class="tag">V16 reversible draft</span><span class="tag">Literal V11 bay geometry</span><span class="tag">Separate 92 × 108 px sprite</span><span class="tag">40 frames · 4 fps · 10 seconds</span></div><h1>Sink as an exact cabinet extension</h1><p class="lede">The sink remains a completely separate asset, but its entire cabinet shell is now one literal approved V11 bay. Only the inset basin and intact tap amend those structural pixels. The adjoining worktop, fascia, doors, rails and plinth therefore share exact geometry.</p><p id="status" class="status">Loading and decoding all review media…</p>
<p class="notice"><strong>Review boundary:</strong> V15 remains immutable rejection evidence. V16 changes no approved V11 source, Final art or runtime asset.</p>
<section class="panel"><h2>Deterministic construction · 4× inspection</h2><div class="grid"><div class="card"><h2>Exact V11 structural bay</h2><div class="stage checker"><img class="bay" src="assets/structural-bay-exact-v11.png" alt="Exact approved V11 right cabinet bay"></div></div><div class="card"><h2>Sink fixture only</h2><div class="stage checker"><img class="isolated" src="assets/sink-fixture-only.png" alt="Isolated basin and intact tap fixture"></div></div><div class="card"><h2>Separate finished asset</h2><div class="stage checker"><canvas class="isolated" id="standard" width="92" height="108"></canvas></div></div></div></section>
<section class="panel"><h2>Approved two-bay run + separate sink extension · exact game size</h2><div class="stage"><img class="room" src="assets/cabinet-run-plus-sink-native-room.png" alt="Approved V11 run with separate exact-geometry sink bay"></div></section>
<div class="controls"><button id="toggle" disabled>Pause</button><label>Speed <input id="speed" type="range" min="0.1" max="4" step="0.1" value="1" disabled></label><output id="speedOut">1.0×</output></div>
<section class="panel"><div class="grid"><div class="card"><h2>On · outlet flow</h2><div class="stage checker"><canvas class="isolated" id="onIso" width="92" height="108"></canvas></div><p>Cue: <code>kitchen_sink_water_gentle_loop</code>.</p></div><div class="card"><h2>Broken · approved jets</h2><div class="stage checker"><canvas class="isolated" id="brokenIso" width="92" height="108"></canvas></div><p>Cue: <code>kitchen_sink_pipe_burst_loop</code>.</p></div></div></section>
<section class="panel"><h2>On · native game size</h2><div class="stage"><canvas class="room" id="onRoom" width="772" height="224"></canvas></div></section><section class="panel"><h2>Broken · native game size</h2><div class="stage"><canvas class="room" id="brokenRoom" width="772" height="224"></canvas></div></section>
</main><script>
const urls={sink:'assets/sink-cabinet-standard.png',room:'assets/cabinet-run-plus-sink-native-room.png',on:'assets/fx-sink-on-water-f40.png',broken:'assets/fx-sink-broken-basin-spouts-f40.png'};const media={};let playing=true,start=performance.now(),speed=1;const load=Object.entries(urls).map(([key,url])=>new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>img.decode().then(()=>{media[key]=img;resolve()}).catch(reject);img.onerror=reject;img.src=url}));function effect(ctx,strip,frame,dx=0,dy=0){ctx.drawImage(strip,frame*92,0,92,108,dx,dy,92,108)}function render(now){if(!media.sink)return;const frame=Math.floor(((now-start)/1000)*4*speed)%40;const s=document.getElementById('standard').getContext('2d');s.clearRect(0,0,92,108);s.drawImage(media.sink,0,0);for(const [id,key] of [['onIso','on'],['brokenIso','broken']]){const c=document.getElementById(id),x=c.getContext('2d');x.clearRect(0,0,92,108);x.drawImage(media.sink,0,0);effect(x,media[key],frame)}for(const [id,key] of [['onRoom','on'],['brokenRoom','broken']]){const c=document.getElementById(id),x=c.getContext('2d');x.clearRect(0,0,772,224);x.drawImage(media.room,0,0);effect(x,media[key],frame,332,104)}if(playing)requestAnimationFrame(render)}Promise.all(load).then(()=>{document.getElementById('status').textContent='All animation media loaded and decoded. Playback unlocked.';toggle.disabled=false;speed.disabled=false;requestAnimationFrame(render)}).catch(error=>document.getElementById('status').textContent='Review media failed to decode: '+error.message);toggle.onclick=()=>{playing=!playing;toggle.textContent=playing?'Pause':'Play';if(playing){start=performance.now();requestAnimationFrame(render)}};speed.oninput=()=>{speed=Number(speed.value);speedOut.textContent=speed.toFixed(1)+'×';start=performance.now()}
</script></body></html>"""


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    bay = exact_v11_bay()
    fixture = fixture_only()
    sink = standalone_sink(bay, fixture)
    room = room_proof(sink)
    on = Image.open(V15_ON).convert("RGBA")
    broken = Image.open(V15_BROKEN).convert("RGBA")
    on0 = on.crop((0, 0, *CELL))
    broken0 = broken.crop((0, 0, *CELL))
    outputs = {
        "structural-bay-exact-v11.png": bay,
        "sink-fixture-only.png": fixture,
        "sink-cabinet-standard.png": sink,
        "sink-cabinet-on-base.png": sink,
        "sink-cabinet-broken-base.png": sink,
        "cabinet-run-plus-sink-native-room.png": room,
        "sink-on-frame-00.png": composite(sink, on0),
        "sink-broken-frame-00.png": composite(sink, broken0),
        "room-sink-on-frame-00.png": room_composite(room, on0),
        "room-sink-broken-frame-00.png": room_composite(room, broken0),
    }
    for name, image in outputs.items():
        save(image, RAW / name)
    shutil.copyfile(V15_ON, RAW / "fx-sink-on-water-f40.png")
    shutil.copyfile(V15_BROKEN, RAW / "fx-sink-broken-basin-spouts-f40.png")
    all_names = [*outputs, "fx-sink-on-water-f40.png", "fx-sink-broken-basin-spouts-f40.png"]
    for name in all_names:
        shutil.copyfile(RAW / name, ASSETS / name)

    catalogue = {
        "set": SET,
        "status": "exact-cabinet-extension-awaiting-visual-review",
        "construction": {
            "standaloneAsset": True,
            "overlaysAnotherCabinetAtRuntime": False,
            "structuralSource": str(V11.relative_to(ROOT)),
            "structuralSourceSha256": sha(V11),
            "structuralCropExclusive": [88, 4, 172, 78],
            "structuralPixelsExactV11": True,
            "fixtureIsOnlyAmendment": True,
            "bodyPixels": list(BODY),
            "cellPixels": list(CELL),
            "bodyOriginInCell": list(BODY_ORIGIN),
        },
        "states": {"staticBasesByteIdentical": True, "tapAndBasinChangedWhenBroken": False},
        "effects": {
            "onWater": {"source": str(V15_ON.relative_to(ROOT)), "byteIdenticalToV15": True, "frames": FRAME_COUNT, "fps": FPS, "durationSeconds": DURATION, "sfxCue": "kitchen_sink_water_gentle_loop"},
            "brokenWater": {"source": str(V15_BROKEN.relative_to(ROOT)), "byteIdenticalToV15": True, "frames": FRAME_COUNT, "fps": FPS, "durationSeconds": DURATION, "sfxCue": "kitchen_sink_pipe_burst_loop"},
        },
        "outputs": {name: sha(RAW / name) for name in all_names},
        "boundaries": {"v11Changed": False, "v15Changed": False, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    registered = [V11, V15_SINK, V15_ON, V15_BROKEN, BACKGROUND, catalogue_path, *[RAW / name for name in all_names]]
    register = {"set": SET, "status": "reversible-unapproved-unpromoted", "files": {str(path.relative_to(ROOT)): sha(path) for path in registered}}
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(page())
    print("Built Kitchen Sink V16: exact V11 structural bay plus isolated sink fixture")


if __name__ == "__main__":
    main()
