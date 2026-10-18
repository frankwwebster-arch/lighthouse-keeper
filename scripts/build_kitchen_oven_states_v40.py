#!/usr/bin/env python3
"""Build reversible Kitchen V40 from-scratch oven states and separate FX."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-oven-states-2026-10-18-v40/generated/oven-three-state-hanging-dial-source-v2.png"
BASE_ROOM = ROOT / "art/raw/kitchen-fridge-states-2026-10-18-v39/kitchen-fridge-standard-in-situ.png"
RAW = ROOT / "art/raw/kitchen-oven-states-2026-10-18-v40"
DRAFT = ROOT / "art/drafts/kitchen-oven-states-2026-10-18-v40"
PUBLIC = ROOT / "public/keeper-review/kitchen-oven-states-v40"
ASSETS = PUBLIC / "assets"

SOURCE_SHA = "d21f2ba12fb4fd2b2c5e1483b0792717cd316e964f59c63d75f40dec9ffcca78"
BASE_ROOM_SHA = "2778c5712deb7a11ddf4fbefdb6ae23cb825772af0db6d2db192a57ee59c7e85"
SOURCE_SIZE = (2172, 724)
SOURCE_CROPS = {
    "off": (137, 124, 677, 627),
    "on": (815, 124, 1356, 627),
    "broken": (1495, 124, 2035, 633),
}
REDUCED_SIZE = (84, 95)
CELL_SIZE = (104, 112)
CELL_OFFSET = (10, 4)
ROOM_SIZE = (772, 224)
ROOM_CELL_TOP_LEFT = (326, 119)
OVEN_BAY = (336, 123, 420, 218)
FLOOR_SURFACE_Y = 218
FX_CELL_SIZE = (120, 144)
FX_ROOM_TOP_LEFT = (318, 74)
FX_FRAMES = 40
FX_FPS = 4

SMOKE_DARK = (48, 53, 58, 210)
SMOKE_MID = (91, 96, 99, 185)
SMOKE_LIGHT = (143, 145, 143, 140)
FLAME_DARK = (128, 30, 10, 255)
FLAME_ORANGE = (245, 76, 8, 255)
FLAME_GOLD = (255, 184, 22, 255)
FLAME_LIGHT = (255, 238, 126, 255)
WARNING_RED = (238, 36, 20, 255)
WARNING_HOT = (255, 116, 38, 255)
WARNING_WHITE = (255, 232, 168, 255)
FLICKER_AMBER = (255, 134, 24, 150)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def opaque_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("Sprite contains no opaque pixels")
    return bbox


def reduce_state(source: Image.Image, name: str) -> Image.Image:
    reduced = source.crop(SOURCE_CROPS[name]).resize(REDUCED_SIZE, Image.Resampling.LANCZOS)
    alpha = reduced.getchannel("A").point(lambda value: 255 if value >= 80 else 0)
    palette = reduced.convert("RGB").quantize(colors=48, method=Image.Quantize.MEDIANCUT).convert("RGB")
    reduced = Image.merge("RGBA", (*palette.split(), alpha))
    cell = Image.new("RGBA", CELL_SIZE)
    cell.alpha_composite(reduced, CELL_OFFSET)
    return cell


def clean_oven_bay(room: Image.Image) -> Image.Image:
    """Remove the complete old oven and hob before any V40 state is drawn."""
    clean = room.copy()
    # Prop-free wall and approved V39 sea-glass cap from the fridge bay.
    clean.paste(room.crop((84, 123, 168, 140)), (336, 123))
    clean.paste(room.crop((84, 140, 168, 151)), (336, 140))
    # An intact cabinet face from the kettle bay replaces the old oven body.
    clean.paste(room.crop((168, 151, 252, 218)), (336, 151))
    return clean


def room_variant(clean_room: Image.Image, sprite: Image.Image) -> Image.Image:
    result = clean_room.copy()
    result.alpha_composite(sprite, ROOM_CELL_TOP_LEFT)
    return result


def smoke_frame(frame_index: int) -> Image.Image:
    """Continuous, clearly billowing comic smoke with a stable door origin."""
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    phase = frame_index / FX_FRAMES
    for lane, lane_x in enumerate((54, 67)):
        for puff in range(6):
            t = (phase + puff / 6 + lane * 0.08) % 1.0
            y = 94 - round(t * 76)
            x = lane_x + round(math.sin((t * 2.0 + lane * 0.55) * math.tau) * (5 + 3 * t))
            radius_x = 4 + round(math.sin(math.pi * t) * 5)
            radius_y = 5 + round(math.sin(math.pi * t) * 6)
            fade = max(0.18, math.sin(math.pi * t))
            dark = (*SMOKE_DARK[:3], round(SMOKE_DARK[3] * fade))
            mid = (*SMOKE_MID[:3], round(SMOKE_MID[3] * fade))
            light = (*SMOKE_LIGHT[:3], round(SMOKE_LIGHT[3] * fade))
            draw.ellipse((x - radius_x, y - radius_y, x + radius_x, y + radius_y), fill=dark)
            draw.ellipse((x - radius_x + 2, y - radius_y + 1, x + radius_x - 1, y + radius_y - 2), fill=mid)
            if radius_x >= 7:
                draw.ellipse((x - 2, y - radius_y + 2, x + radius_x - 2, y), fill=light)
    # Permanent throat: smoke unmistakably emerges from the askew door gap.
    throat_x = 61 + round(math.sin(phase * math.tau) * 2)
    draw.ellipse((throat_x - 6, 88, throat_x + 7, 101), fill=SMOKE_DARK)
    draw.ellipse((throat_x - 3, 87, throat_x + 5, 96), fill=SMOKE_MID)
    return frame


def flame_cluster(draw: ImageDraw.ImageDraw, x: int, base_y: int, height: int, lean: int) -> None:
    draw.polygon(((x - 6, base_y), (x - 5, base_y - 5), (x - 2, base_y - height + 4), (x + lean, base_y - height), (x + 3, base_y - 7), (x + 6, base_y - 3), (x + 5, base_y)), fill=FLAME_DARK)
    draw.polygon(((x - 4, base_y - 1), (x - 3, base_y - 6), (x + lean, base_y - height + 3), (x + 3, base_y - 5), (x + 4, base_y - 1)), fill=FLAME_ORANGE)
    draw.polygon(((x - 2, base_y - 1), (x - 1, base_y - 5), (x + lean, base_y - height + 6), (x + 2, base_y - 2)), fill=FLAME_GOLD)
    draw.point((x, base_y - 2), fill=FLAME_LIGHT)


def flame_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    phase = frame_index * math.tau / FX_FRAMES
    flame_cluster(draw, 47, 60, 12 + round(3 * math.sin(phase)), round(2 * math.sin(phase * 1.7)))
    flame_cluster(draw, 75, 60, 12 + round(3 * math.sin(phase + 2.2)), round(2 * math.sin(phase * 1.4 + 1.1)))
    # Restrained burner-base glow anchors both flames to the hob surface.
    draw.line((41, 60, 53, 60), fill=FLAME_ORANGE, width=1)
    draw.line((69, 60, 81, 60), fill=FLAME_ORANGE, width=1)
    return frame


def warning_light_frame(frame_index: int) -> Image.Image:
    """Irregular angry red bursts plus rare internal-cavity light flickers."""
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    red_on = frame_index in {0, 1, 3, 4, 5, 8, 9, 12, 13, 14, 15, 19, 20, 24, 26, 27, 28, 32, 33, 37, 38}
    hot = frame_index in {1, 4, 9, 13, 15, 20, 27, 32, 38}
    if red_on:
        draw.ellipse((56, 73, 64, 81), fill=(120, 8, 6, 150))
        draw.ellipse((57, 74, 63, 80), fill=WARNING_RED)
        draw.ellipse((59, 75, 62, 78), fill=WARNING_HOT)
        draw.point((60, 75), fill=WARNING_WHITE)
        if hot:
            draw.point((55, 77), fill=WARNING_RED)
            draw.point((65, 77), fill=WARNING_RED)
            draw.point((60, 72), fill=WARNING_RED)
            draw.point((60, 82), fill=WARNING_RED)
    if frame_index in {6, 7, 22, 34, 35}:
        strength = 190 if frame_index in {7, 35} else 125
        amber = (*FLICKER_AMBER[:3], strength)
        # Upper cavity wedge only: the static askew door remains unobscured.
        draw.polygon(((42, 94), (88, 94), (87, 101), (54, 98), (42, 103)), fill=amber)
        draw.line((47, 96, 83, 96), fill=(255, 206, 84, min(235, strength + 35)), width=1)
    return frame


def make_strip(frame_builder) -> Image.Image:
    strip = Image.new("RGBA", (FX_CELL_SIZE[0] * FX_FRAMES, FX_CELL_SIZE[1]))
    for frame_index in range(FX_FRAMES):
        strip.alpha_composite(frame_builder(frame_index), (frame_index * FX_CELL_SIZE[0], 0))
    return strip


def save_output(name: str, image: Image.Image) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    image.save(RAW / name, optimize=True)
    copy(RAW / name, ASSETS / name)


def write_page() -> None:
    page = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-oven-states-v40/"><title>Kitchen V40 · from-scratch oven states</title><style>
*{box-sizing:border-box}body{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:22px}h1,h2,h3{line-height:1.12}.tag{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin:0 6px 5px 0;color:#9af1e9}section{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}.note{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}.warn{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}.grid{display:grid;grid-template-columns:repeat(3,minmax(260px,1fr));gap:14px}.grid.two{grid-template-columns:repeat(2,minmax(300px,1fr))}.card{text-align:center;background:#091e29;border:1px solid #315768;border-radius:11px;padding:12px}.checker{background-color:#e8f2ed;background-image:linear-gradient(45deg,#c4d7d0 25%,transparent 25%),linear-gradient(-45deg,#c4d7d0 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#c4d7d0 75%),linear-gradient(-45deg,transparent 75%,#c4d7d0 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0;border-radius:9px}.isolated{position:relative;width:416px;height:448px;max-width:100%;margin:auto;overflow:hidden}.isolated img{position:absolute;inset:0;width:416px;height:448px;max-width:none;image-rendering:pixelated}.effect{position:relative;width:480px;height:576px;max-width:100%;margin:auto;overflow:hidden}.effect>img{position:absolute;inset:0;height:576px;max-width:none;image-rendering:pixelated}.combo{position:relative;width:480px;height:576px;max-width:100%;margin:auto;overflow:hidden}.combo .object{position:absolute;left:32px;top:180px;width:416px;height:448px;image-rendering:pixelated}.combo .fx{position:absolute;inset:0;height:576px;max-width:none;image-rendering:pixelated}.stage{overflow:auto;background:#02080b;border-radius:9px;padding:16px}.room{position:relative;width:772px;height:224px;overflow:hidden}.room>img:first-child{position:absolute;inset:0;width:772px;height:224px;max-width:none}.room-fx{position:absolute;left:318px;top:74px;width:120px;height:144px;overflow:hidden}.room-fx img{height:144px;max-width:none;image-rendering:pixelated}.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}button{background:#147d78;color:white;border:0;border-radius:6px;padding:9px 12px;cursor:pointer}button:disabled{opacity:.45;cursor:wait}[data-media]{visibility:hidden}body.ready [data-media]{visibility:visible}@media(max-width:900px){.grid{grid-template-columns:1fr}.grid.two{grid-template-columns:1fr}.isolated,.effect,.combo{zoom:.68;transform-origin:top left}}
</style></head><body><main><span class="tag">V40 corrective draft</span><span class="tag">Oven only</span><span class="tag">From-scratch family</span><span class="tag">Old oven and hob cleared first</span><h1>Oven · Off, On and Broken</h1><p class="note">One new family replaces the cleared old oven/hob. Smoke, flames and fault-light motion are separate effect-only strips.</p><p id="loading">Loading and decoding review images…</p><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="fan" disabled>Fan SFX</button><button id="hiss" disabled>Smoke SFX</button><button id="flame" disabled>Flame SFX</button><button id="blink" disabled>Warning SFX</button></div>
<section><h2>Three coordinated states · 4× inspection</h2><div class="grid"><article class="card"><h3>Off</h3><div class="checker isolated"><img data-media src="assets/oven-off.png" width="416" height="448" alt="Oven off with dark interior, unlit indicator and upright dials"></div><p>Interior and indicator dark; all controls upright.</p></article><article class="card"><h3>On</h3><div class="checker isolated"><img data-media src="assets/oven-on.png" width="416" height="448" alt="Oven on with rotated dials, red indicator, warm interior and roasting tin"></div><p>Rotated dials, red indicator, amber interior and roasting tin.</p></article><article class="card"><h3>Broken · static object</h3><div class="checker isolated"><img data-media src="assets/oven-broken.png" width="416" height="448" alt="Broken oven with attached askew door and one rotary dial hanging by two wires"></div><p>Door remains attached and askew; the failed right dial hangs from two exposed wires. No smoke or flame pixels are baked into the object.</p></article></div></section>
<section><h2>Compositing proof · previous oven and hob removed</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-oven-cleared-bay.png" width="772" height="224" alt="Complete kitchen with the previous oven and hob fully removed before replacement"></div></div><p>The diagnostic intermediate shows a plain fitted cabinet bay: no previous oven door, glowing cavity, controls or hob survive underneath V40.</p></section>
<section><h2>Off in the complete kitchen · exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-oven-off-in-situ.png" width="772" height="224" alt="Oven Off in the complete approved kitchen at exact game size"></div></div></section>
<section><h2>On in the complete kitchen · exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-oven-on-in-situ.png" width="772" height="224" alt="Oven On in the complete approved kitchen at exact game size"></div></div></section>
<section><h2>Broken in the complete kitchen · exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-oven-broken-in-situ.png" width="772" height="224" alt="Broken oven at game size"><i class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-billowing-smoke-f40.png" width="4800" height="144" alt="Smoke"></i><i class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-hob-flames-f40.png" width="4800" height="144" alt="Flames"></i><i class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-warning-light-flicker-f40.png" width="4800" height="144" alt="Angry red warning blink and cavity flicker"></i></div></div><p>Billowing smoke, burner-anchored flames, irregular rapid red bursts and rare internal-light flickers.</p></section>
<section><h2>Reusable effects only · 4× inspection</h2><div class="grid"><article class="card"><h3>Billowing smoke</h3><div class="checker effect"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-billowing-smoke-f40.png" width="19200" height="576" alt="Smoke only"></div></article><article class="card"><h3>Hob flames</h3><div class="checker effect"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-hob-flames-f40.png" width="19200" height="576" alt="Flames only"></div></article><article class="card"><h3>Angry warning light</h3><div class="checker effect"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-warning-light-flicker-f40.png" width="19200" height="576" alt="Warning light only"></div></article></div><p>Each effect-only strip has 40 isolated frames at 4 fps for a ten-second loop.</p></section>
<section><h2>Broken object plus all reusable effects · 4× inspection</h2><div class="checker combo"><img data-media class="object" src="assets/oven-broken.png" width="416" height="448" alt="Static broken oven"><img data-media class="fx" data-strip data-frames="40" data-fps="4" src="assets/fx-oven-billowing-smoke-f40.png" width="19200" height="576" alt="Smoke"><img data-media class="fx" data-strip data-frames="40" data-fps="4" src="assets/fx-oven-hob-flames-f40.png" width="19200" height="576" alt="Flames"><img data-media class="fx" data-strip data-frames="40" data-fps="4" src="assets/fx-oven-warning-light-flicker-f40.png" width="19200" height="576" alt="Warning light"></div></section>
<p class="warn"><strong>Review boundary:</strong> V39 fridge is approved review authority. V35 remains rejected provenance. V40 is the only active oven gate and remains reversible, unpromoted and unwired. No other kitchen asset was revised.</p>
</main><script>
const strips=[...document.querySelectorAll('[data-strip]')],controls=[...document.querySelectorAll('button')];let playing=false,start=0,held=0,raf=0;function render(now){if(!playing)return;const elapsed=held+(now-start);for(const image of strips){const frame=Math.floor(elapsed*(+image.dataset.fps)/1000)%(+image.dataset.frames),w=image.parentElement.clientWidth;image.style.transform=`translateX(${-frame*w}px)`}raf=requestAnimationFrame(render)}function play(){if(playing)return;playing=true;start=performance.now();raf=requestAnimationFrame(render)}function pause(){if(!playing)return;held+=performance.now()-start;playing=false;cancelAnimationFrame(raf)}function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}function tone(kind){const C=window.AudioContext||window.webkitAudioContext,c=new C,o=c.createOscillator(),g=c.createGain(),n=c.currentTime;o.type=kind==='fan'?'sine':'sawtooth';o.frequency.setValueAtTime(kind==='fan'?72:kind==='hiss'?132:92,n);o.frequency.linearRampToValueAtTime(kind==='fan'?76:kind==='hiss'?168:104,n+1.1);g.gain.setValueAtTime(kind==='fan'?.018:.012,n);g.gain.exponentialRampToValueAtTime(.001,n+1.3);o.connect(g).connect(c.destination);o.start();o.stop(n+1.35)}const unique=[...new Set([...document.querySelectorAll('[data-media]')].map(image=>image.src))];Promise.all(unique.map(preload)).then(()=>{document.body.classList.add('ready');controls.forEach(button=>button.disabled=false);loading.textContent=`All ${unique.length} images decoded. Playback unlocked.`;play()}).catch(error=>loading.textContent='Review locked: '+error.message);play.onclick=play;pause.onclick=pause;fan.onclick=()=>tone('fan');hiss.onclick=()=>tone('hiss');flame.onclick=()=>tone('flame');blink.onclick=()=>tone('blink');
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    for path, expected in ((SOURCE, SOURCE_SHA), (BASE_ROOM, BASE_ROOM_SHA)):
        if sha(path) != expected:
            raise RuntimeError(f"Pinned input changed: {path.relative_to(ROOT)}")
    with Image.open(SOURCE) as image:
        source = image.convert("RGBA")
    if source.size != SOURCE_SIZE:
        raise RuntimeError(f"Generated source is {source.size}, expected {SOURCE_SIZE}")
    with Image.open(BASE_ROOM) as image:
        room = image.convert("RGBA")
    states = {name: reduce_state(source, name) for name in SOURCE_CROPS}
    clean_room = clean_oven_bay(room)
    smoke = make_strip(smoke_frame)
    flames = make_strip(flame_frame)
    warning = make_strip(warning_light_frame)
    outputs = {
        "oven-off.png": states["off"],
        "oven-on.png": states["on"],
        "oven-broken.png": states["broken"],
        "kitchen-oven-cleared-bay.png": clean_room,
        "kitchen-oven-off-in-situ.png": room_variant(clean_room, states["off"]),
        "kitchen-oven-on-in-situ.png": room_variant(clean_room, states["on"]),
        "kitchen-oven-broken-in-situ.png": room_variant(clean_room, states["broken"]),
        "fx-oven-billowing-smoke-f40.png": smoke,
        "fx-oven-hob-flames-f40.png": flames,
        "fx-oven-warning-light-flicker-f40.png": warning,
    }
    for name, image in outputs.items():
        save_output(name, image)

    catalogue = {
        "version": 40,
        "asset": "oven",
        "status": "from-scratch-oven-family-awaiting-review",
        "states": ["off", "on", "broken"],
        "densityPxPerLp": 4,
        "cellPixels": list(CELL_SIZE),
        "roomPixels": list(ROOM_SIZE),
        "roomCellTopLeft": list(ROOM_CELL_TOP_LEFT),
        "ovenBayPixels": list(OVEN_BAY),
        "floorSurfaceY": FLOOR_SURFACE_Y,
        "source": {"file": str(SOURCE.relative_to(ROOT)), "generator": "OpenAI built-in image generation", "sha256": SOURCE_SHA, "size": list(SOURCE_SIZE), "cropsExclusive": {name: list(crop) for name, crop in SOURCE_CROPS.items()}, "reducedSize": list(REDUCED_SIZE)},
        "approvedContext": {"v39Room": str(BASE_ROOM.relative_to(ROOT)), "v39RoomSha256": BASE_ROOM_SHA, "fridgeApproval": "docs/review/kitchen-fridge-states-v39-approval-2026-10-18.json", "changed": False},
        "outputs": {name: {"sha256": sha(RAW / name), "size": list(image.size)} for name, image in outputs.items()},
        "opaqueBounds": {name: list(opaque_bbox(image)) for name, image in states.items()},
        "construction": {"fromScratch": True, "coordinatedFamily": True, "sameSourceSheet": True, "previousOvenAndHobClearedBeforeComposite": True, "objectAnimated": False, "offInteriorDark": True, "offIndicatorDark": True, "onInteriorLight": True, "onDialsTurned": True, "onRedIndicator": True, "onRoastingTin": True, "brokenDoorAttachedAskew": True, "brokenDialHangingByWires": True, "smokeBakedIntoObject": False, "flamesBakedIntoObject": False, "warningLightBakedIntoObject": False},
        "effects": {
            "billowing_smoke": {"file": "fx-oven-billowing-smoke-f40.png", "reusable": True, "frames": FX_FRAMES, "fps": FX_FPS, "durationSeconds": FX_FRAMES / FX_FPS, "cellPixels": list(FX_CELL_SIZE), "roomTopLeft": list(FX_ROOM_TOP_LEFT), "effectOnly": True, "anchor": "open_oven_cavity", "sfxCue": "kitchen_oven_broken_smoke_hiss_loop"},
            "hob_flames": {"file": "fx-oven-hob-flames-f40.png", "reusable": True, "frames": FX_FRAMES, "fps": FX_FPS, "durationSeconds": FX_FRAMES / FX_FPS, "cellPixels": list(FX_CELL_SIZE), "roomTopLeft": list(FX_ROOM_TOP_LEFT), "effectOnly": True, "anchors": [[365, 134], [393, 134]], "sfxCue": "kitchen_oven_hob_flame_loop"},
            "warning_light_flicker": {"file": "fx-oven-warning-light-flicker-f40.png", "reusable": True, "frames": FX_FRAMES, "fps": FX_FPS, "durationSeconds": FX_FRAMES / FX_FPS, "cellPixels": list(FX_CELL_SIZE), "roomTopLeft": list(FX_ROOM_TOP_LEFT), "effectOnly": True, "redIndicatorAnchor": [378, 151], "cavityFlicker": True, "redBurstFrames": 21, "cavityFlickerFrames": 5, "sfxCue": "kitchen_oven_broken_warning_light_angry_blink_loop"},
        },
        "sfxCues": ["kitchen_oven_on_fan_loop", "kitchen_oven_broken_smoke_hiss_loop", "kitchen_oven_hob_flame_loop", "kitchen_oven_broken_warning_light_angry_blink_loop"],
        "boundaries": {"approved": False, "promoted": False, "runtimeChanged": False, "finalChanged": False, "v35Changed": False, "otherKitchenAssetsRevised": False},
    }
    DRAFT.mkdir(parents=True, exist_ok=True)
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "version": 40,
        "status": "awaiting-oven-visual-review",
        "supersedesRejectedDraft": 35,
        "preservesApprovedFridge": 39,
        "originalHashes": {"v39Room": BASE_ROOM_SHA},
        "draftHashes": {name: sha(RAW / name) for name in outputs},
        "nextAssetBlockedUntilApproval": "kettle-or-user-selected-next-asset",
        "rollback": "Delete only V40 source/raw/draft/review/archive/builder/verifier/docs files; approved V39 and rejected V35 provenance remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
