#!/usr/bin/env python3
"""Build Kitchen V41: exact V21-size oven family with separate environmental FX."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-oven-states-2026-10-18-v41/generated/oven-three-state-fitted-exact-size-source-v1.png"
APPROVED_OVEN = ROOT / "art/raw/kitchen-final-assets-2026-10-17-v21/basic-oven.png"
BASE_ROOM = ROOT / "art/raw/kitchen-fridge-states-2026-10-18-v39/kitchen-fridge-standard-in-situ.png"
RAW = ROOT / "art/raw/kitchen-oven-states-2026-10-18-v41"
DRAFT = ROOT / "art/drafts/kitchen-oven-states-2026-10-18-v41"
PUBLIC = ROOT / "public/keeper-review/kitchen-oven-states-v41"
ASSETS = PUBLIC / "assets"

SOURCE_SHA = "6ee0a16d77af2e0d76d8594b611cfc9e48abb963d5746073ab2785039f9828f9"
APPROVED_OVEN_SHA = "45658c2649d10efc896d646821b16e12d3a19fc401d04168e00ace3a6f016ba8"
BASE_ROOM_SHA = "2778c5712deb7a11ddf4fbefdb6ae23cb825772af0db6d2db192a57ee59c7e85"
SOURCE_SIZE = (2172, 724)
SOURCE_CROPS = {
    "off": (88, 192, 723, 594),
    "on": (770, 192, 1403, 594),
    "broken": (1449, 192, 2084, 645),
}

# Binding V21 measurements. The complete hob + fascia artwork occupies exactly
# x=12..95 and y=31..107 inside the original 108 x 120 review cell.
CELL_SIZE = (108, 120)
APPROVED_BOUNDS = (12, 31, 96, 108)
ART_SIZE = (84, 77)
HOB_SPLIT_Y = 48
PANEL_SIZE = (84, APPROVED_BOUNDS[3] - HOB_SPLIT_Y)
ROOM_SIZE = (772, 224)
ROOM_CELL_TOP_LEFT = (324, 100)
OVEN_BOUNDS_ROOM = (336, 131, 420, 208)
FLOOR_SURFACE_Y = 218

FX_CELL_SIZE = (120, 144)
FX_ROOM_TOP_LEFT = (318, 74)
FX_FRAMES = 40
FX_FPS = 4

SMOKE_DARK = (43, 48, 54, 168)
SMOKE_MID = (83, 88, 93, 132)
SMOKE_LIGHT = (150, 151, 147, 102)
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
        raise RuntimeError("sprite has no visible pixels")
    return bbox


def approved_palette(reference: Image.Image) -> list[tuple[int, int, int]]:
    # Quantize only visibly approved V21 pixels. The source's LANCZOS alpha
    # means many canonical copper/amber colours sit at alpha 254 rather than
    # 255; excluding those would incorrectly turn the controls grey.
    pixels = [(r, g, b) for r, g, b, a in reference.getdata() if a >= 128]
    strip = Image.new("RGB", (len(pixels), 1))
    strip.putdata(pixels)
    reduced = strip.quantize(colors=48, method=Image.Quantize.MEDIANCUT).convert("RGB")
    return sorted(set(reduced.getdata()))


def nearest_palette(pixel: tuple[int, int, int], palette: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    r, g, b = pixel
    return min(palette, key=lambda colour: (colour[0] - r) ** 2 + (colour[1] - g) ** 2 + (colour[2] - b) ** 2)


def normalize_panel(source: Image.Image, state: str, palette: list[tuple[int, int, int]]) -> Image.Image:
    crop = source.crop(SOURCE_CROPS[state]).resize(PANEL_SIZE, Image.Resampling.LANCZOS)
    alpha = crop.getchannel("A").point(lambda value: 255 if value >= 96 else 0)
    pixels = crop.convert("RGB").load()
    mask = alpha.load()
    mapped = Image.new("RGBA", PANEL_SIZE)
    output = mapped.load()
    cache: dict[tuple[int, int, int], tuple[int, int, int]] = {}
    for y in range(PANEL_SIZE[1]):
        for x in range(PANEL_SIZE[0]):
            if not mask[x, y]:
                continue
            colour = pixels[x, y]
            # Off and Broken indicators stay dark in the static object. Broken's
            # angry red activity belongs only to the separate warning strip.
            indicator_zone = y < 17 and ((state == "off" and 31 <= x <= 47) or (state == "broken" and 20 <= x <= 43))
            if state != "on" and indicator_zone and colour[0] > 90 and colour[0] > colour[1] * 1.35:
                colour = (7, 27, 56)
            if colour not in cache:
                cache[colour] = nearest_palette(colour, palette)
            output[x, y] = (*cache[colour], 255)
    return mapped


def make_state(source: Image.Image, reference: Image.Image, state: str, palette: list[tuple[int, int, int]]) -> Image.Image:
    cell = Image.new("RGBA", CELL_SIZE)
    # Preserve the approved hob and continuous sea-glass surround byte-for-byte.
    hob = reference.crop((APPROVED_BOUNDS[0], APPROVED_BOUNDS[1], APPROVED_BOUNDS[2], HOB_SPLIT_Y))
    cell.alpha_composite(hob, (APPROVED_BOUNDS[0], APPROVED_BOUNDS[1]))
    cell.alpha_composite(normalize_panel(source, state, palette), (APPROVED_BOUNDS[0], HOB_SPLIT_Y))
    if opaque_bbox(cell) != APPROVED_BOUNDS:
        raise RuntimeError(f"{state} bounds {opaque_bbox(cell)} do not match approved {APPROVED_BOUNDS}")
    return cell


def clean_oven_bay(room: Image.Image) -> Image.Image:
    """Remove the complete prior oven/hob footprint before replacement."""
    clean = room.copy()
    # A plain neighbouring fitted bay is the neutral underlay. V41 subsequently
    # replaces the full measured 84 x 77 oven/hob footprint, so no old state can
    # survive beneath the new one.
    clean.paste(room.crop((84, 123, 168, 151)), (336, 123))
    clean.paste(room.crop((168, 151, 252, 218)), (336, 151))
    return clean


def room_variant(clean_room: Image.Image, sprite: Image.Image) -> Image.Image:
    result = clean_room.copy()
    result.alpha_composite(sprite, ROOM_CELL_TOP_LEFT)
    return result


def smoke_frame(frame_index: int) -> Image.Image:
    """One connected, curling smoke stream—never discrete circular bubbles."""
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    phase = frame_index * math.tau / FX_FRAMES
    levels = (117, 105, 92, 78, 64, 50, 37, 26, 18)
    points = []
    for index, y in enumerate(levels):
        rise = index / (len(levels) - 1)
        x = round(61 + math.sin(phase + index * 0.72) * (2 + rise * 7) + math.sin(phase * 0.41 + index * 1.09) * rise * 4)
        points.append((x, y))

    # Overlapping variable-width segments form one uninterrupted stream which
    # broadens and rolls as it rises from the oven cavity.
    for index in range(len(points) - 1):
        width = 10 + index * 2
        draw.line((points[index], points[index + 1]), fill=SMOKE_DARK, width=width, joint="curve")
    top = points[-1]
    curl = (top[0] + round(13 + 3 * math.sin(phase * 0.7)), top[1] + round(3 * math.cos(phase)))
    draw.line((points[-2], top, curl), fill=SMOKE_DARK, width=22, joint="curve")

    # A narrow internal current and an attached upper wisp create rolling flow
    # without introducing detached round puffs.
    draw.line(points, fill=SMOKE_MID, width=8, joint="curve")
    branch_from = points[5]
    branch_tip = (branch_from[0] - round(13 + 3 * math.sin(phase)), branch_from[1] - 9)
    draw.line((branch_from, branch_tip), fill=SMOKE_DARK, width=8, joint="curve")
    draw.line((branch_from, branch_tip), fill=SMOKE_MID, width=3, joint="curve")
    draw.line(points[2:8], fill=SMOKE_LIGHT, width=3, joint="curve")
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
    flame_cluster(draw, 40, 68, 13 + round(3 * math.sin(phase)), round(2 * math.sin(phase * 1.7)))
    flame_cluster(draw, 76, 68, 13 + round(3 * math.sin(phase + 2.2)), round(2 * math.sin(phase * 1.4 + 1.1)))
    draw.line((34, 68, 46, 68), fill=FLAME_ORANGE, width=1)
    draw.line((70, 68, 82, 68), fill=FLAME_ORANGE, width=1)
    return frame


def warning_light_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    red_on = frame_index in {0, 1, 3, 4, 5, 8, 9, 12, 13, 14, 15, 19, 20, 24, 26, 27, 28, 32, 33, 37, 38}
    hot = frame_index in {1, 4, 9, 13, 15, 20, 27, 32, 38}
    if red_on:
        draw.ellipse((48, 77, 56, 85), fill=(120, 8, 6, 150))
        draw.ellipse((49, 78, 55, 84), fill=WARNING_RED)
        draw.ellipse((51, 79, 54, 82), fill=WARNING_HOT)
        draw.point((52, 79), fill=WARNING_WHITE)
        if hot:
            for point in ((47, 81), (57, 81), (52, 76), (52, 86)):
                draw.point(point, fill=WARNING_RED)
    if frame_index in {6, 7, 22, 34, 35}:
        strength = 190 if frame_index in {7, 35} else 125
        amber = (*FLICKER_AMBER[:3], strength)
        draw.polygon(((35, 97), (87, 97), (85, 109), (51, 105), (35, 111)), fill=amber)
        draw.line((41, 100, 82, 100), fill=(255, 206, 84, min(235, strength + 35)), width=1)
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
    page = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-oven-states-v41/"><title>Kitchen V41 · exact measured oven family</title><style>
*{box-sizing:border-box}body{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:22px}h1,h2,h3{line-height:1.12}.tag{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin:0 6px 5px 0;color:#9af1e9}section{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}.note{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}.warn{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}.grid{display:grid;grid-template-columns:repeat(3,minmax(260px,1fr));gap:14px}.grid.two{grid-template-columns:repeat(2,minmax(300px,1fr))}.card{text-align:center;background:#091e29;border:1px solid #315768;border-radius:11px;padding:12px}.checker{background-color:#e8f2ed;background-image:linear-gradient(45deg,#c4d7d0 25%,transparent 25%),linear-gradient(-45deg,#c4d7d0 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#c4d7d0 75%),linear-gradient(-45deg,transparent 75%,#c4d7d0 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0;border-radius:9px}.isolated{position:relative;width:432px;height:480px;max-width:100%;margin:auto;overflow:hidden}.isolated img{position:absolute;inset:0;width:432px;height:480px;max-width:none;image-rendering:pixelated}.effect{position:relative;width:480px;height:576px;max-width:100%;margin:auto;overflow:hidden}.effect>img{position:absolute;inset:0;height:576px;max-width:none;image-rendering:pixelated}.stage{overflow:auto;background:#02080b;border-radius:9px;padding:16px}.room{position:relative;width:772px;height:224px;overflow:hidden}.room>img:first-child{position:absolute;inset:0;width:772px;height:224px;max-width:none}.room-fx{position:absolute;left:318px;top:74px;width:120px;height:144px;overflow:hidden}.room-fx img{height:144px;max-width:none;image-rendering:pixelated}.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}button{background:#147d78;color:white;border:0;border-radius:6px;padding:9px 12px;cursor:pointer}button:disabled{opacity:.45;cursor:wait}code{color:#9af1e9}[data-media]{visibility:hidden}body.ready [data-media]{visibility:visible}@media(max-width:900px){.grid,.grid.two{grid-template-columns:1fr}.isolated,.effect{zoom:.68;transform-origin:top left}}
</style></head><body><main><span class="tag">V41 corrective draft</span><span class="tag">Oven only</span><span class="tag">Exact V21 measurement</span><span class="tag">Approved hob retained</span><h1>Oven · Off, On and Broken</h1><p class="note"><strong>Binding geometry:</strong> every state is the original 108 × 120 px review cell with the original exact 84 × 77 px opaque footprint. The approved hob and sea-glass surround are preserved byte-for-byte; the redrawn fascia uses only colours sampled from the approved V21 oven.</p><p id="loading">Loading and decoding every review image…</p><div class="controls"><button id="play" disabled>Play effects</button><button id="pause" disabled>Pause</button><button id="fan" disabled>Fan SFX</button><button id="hiss" disabled>Smoke SFX</button><button id="flame" disabled>Flame SFX</button><button id="blink" disabled>Warning SFX</button></div>
<section><h2>Measured authority and three states · 4× inspection</h2><div class="grid"><article class="card"><h3>Approved V21 measurement</h3><div class="checker isolated"><img data-media src="assets/oven-v21-approved-reference.png" width="432" height="480" alt="Approved V21 oven measurement authority"></div><p><code>cell 108×120 · bounds 84×77</code></p></article><article class="card"><h3>Off</h3><div class="checker isolated"><img data-media src="assets/oven-off.png" width="432" height="480" alt="Oven off"></div><p>Dark cavity, upright dials and dark indicator.</p></article><article class="card"><h3>On</h3><div class="checker isolated"><img data-media src="assets/oven-on.png" width="432" height="480" alt="Oven on"></div><p>Turned dials, red indicator, amber interior and roasting tin.</p></article><article class="card"><h3>Broken · static object</h3><div class="checker isolated"><img data-media src="assets/oven-broken.png" width="432" height="480" alt="Broken oven with askew door and dial hanging by two wires"></div><p>Door askew; one rotary dial hangs from the fascia by two wires.</p></article></div></section>
<section><h2>Compositing proof · old oven and hob removed first</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-oven-cleared-bay.png" width="772" height="224" alt="Complete kitchen with previous oven and hob removed"></div></div><p>The neutral bay proves no former oven or hob remains beneath V41.</p></section>
<section><h2>Off · complete kitchen at exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-oven-off-in-situ.png" width="772" height="224" alt="Off oven in complete kitchen"></div></div></section>
<section><h2>On · complete kitchen at exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-oven-on-in-situ.png" width="772" height="224" alt="On oven in complete kitchen"></div></div></section>
<section><h2>Broken · complete kitchen at exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-oven-broken-in-situ.png" width="772" height="224" alt="Broken oven in complete kitchen"><i class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-flowing-smoke-f40.png" width="4800" height="144" alt="Continuous flowing smoke"></i><i class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-hob-flames-f40.png" width="4800" height="144" alt="Hob flames"></i><i class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-warning-light-flicker-f40.png" width="4800" height="144" alt="Angry red warning blink and cavity flicker"></i></div></div><p>The smoke rises as one connected curling plume, not discrete bubbles. Flames align with the retained approved hob.</p></section>
<section><h2>Reusable environmental effects · 4× inspection</h2><div class="grid"><article class="card"><h3>Connected flowing smoke</h3><div class="checker effect"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-flowing-smoke-f40.png" width="19200" height="576" alt="Continuous smoke only"></div></article><article class="card"><h3>Hob flames</h3><div class="checker effect"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-hob-flames-f40.png" width="19200" height="576" alt="Flames only"></div></article><article class="card"><h3>Angry warning + cavity flicker</h3><div class="checker effect"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-oven-warning-light-flicker-f40.png" width="19200" height="576" alt="Warning light only"></div></article></div><p>Each strip has 40 isolated frames at 4 fps for a ten-second loop.</p></section>
<p class="warn"><strong>Review boundary:</strong> V39 fridge remains approved. V40 is rejected immutable provenance. V41 is reversible, unpromoted and unwired; no later kitchen asset changed.</p>
</main><script>
const strips=[...document.querySelectorAll('[data-strip]')],controls=[...document.querySelectorAll('button')];let playing=false,start=0,held=0,raf=0;function render(now){if(!playing)return;const elapsed=held+(now-start);for(const image of strips){const frame=Math.floor(elapsed*(+image.dataset.fps)/1000)%(+image.dataset.frames),w=image.parentElement.clientWidth;image.style.transform=`translateX(${-frame*w}px)`}raf=requestAnimationFrame(render)}function play(){if(playing)return;playing=true;start=performance.now();raf=requestAnimationFrame(render)}function pause(){if(!playing)return;held+=performance.now()-start;playing=false;cancelAnimationFrame(raf)}function preload(src){return new Promise((resolve,reject)=>{const image=new Image;image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}function tone(kind){const C=window.AudioContext||window.webkitAudioContext,c=new C,o=c.createOscillator(),g=c.createGain(),n=c.currentTime;o.type=kind==='fan'?'sine':'sawtooth';o.frequency.setValueAtTime(kind==='fan'?72:kind==='hiss'?132:92,n);o.frequency.linearRampToValueAtTime(kind==='fan'?76:kind==='hiss'?168:104,n+1.1);g.gain.setValueAtTime(kind==='fan'?.018:.012,n);g.gain.exponentialRampToValueAtTime(.001,n+1.3);o.connect(g).connect(c.destination);o.start();o.stop(n+1.35)}const unique=[...new Set([...document.querySelectorAll('[data-media]')].map(image=>image.src))];Promise.all(unique.map(preload)).then(()=>{document.body.classList.add('ready');controls.forEach(button=>button.disabled=false);loading.textContent=`All ${unique.length} images decoded. Playback unlocked.`;play()}).catch(error=>loading.textContent='Review locked: '+error.message);play.onclick=play;pause.onclick=pause;fan.onclick=()=>tone('fan');hiss.onclick=()=>tone('hiss');flame.onclick=()=>tone('flame');blink.onclick=()=>tone('blink');
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    for path, expected in ((SOURCE, SOURCE_SHA), (APPROVED_OVEN, APPROVED_OVEN_SHA), (BASE_ROOM, BASE_ROOM_SHA)):
        if sha(path) != expected:
            raise RuntimeError(f"pinned input changed: {path.relative_to(ROOT)}")
    source = Image.open(SOURCE).convert("RGBA")
    reference = Image.open(APPROVED_OVEN).convert("RGBA")
    room = Image.open(BASE_ROOM).convert("RGBA")
    if source.size != SOURCE_SIZE or reference.size != CELL_SIZE or room.size != ROOM_SIZE:
        raise RuntimeError("pinned input geometry changed")
    if opaque_bbox(reference) != APPROVED_BOUNDS:
        raise RuntimeError("approved V21 oven bounds changed")

    palette = approved_palette(reference)
    states = {state: make_state(source, reference, state, palette) for state in ("off", "on", "broken")}
    clean_room = clean_oven_bay(room)
    smoke = make_strip(smoke_frame)
    flames = make_strip(flame_frame)
    warning = make_strip(warning_light_frame)
    outputs = {
        "oven-v21-approved-reference.png": reference,
        "oven-off.png": states["off"],
        "oven-on.png": states["on"],
        "oven-broken.png": states["broken"],
        "kitchen-oven-cleared-bay.png": clean_room,
        "kitchen-oven-off-in-situ.png": room_variant(clean_room, states["off"]),
        "kitchen-oven-on-in-situ.png": room_variant(clean_room, states["on"]),
        "kitchen-oven-broken-in-situ.png": room_variant(clean_room, states["broken"]),
        "fx-oven-flowing-smoke-f40.png": smoke,
        "fx-oven-hob-flames-f40.png": flames,
        "fx-oven-warning-light-flicker-f40.png": warning,
    }
    for name, image in outputs.items():
        save_output(name, image)

    catalogue = {
        "version": 41,
        "asset": "oven",
        "status": "exact-approved-size-colour-matched-family-awaiting-review",
        "states": ["off", "on", "broken"],
        "densityPxPerLp": 4,
        "cellPixels": list(CELL_SIZE),
        "approvedOpaqueBoundsExclusive": list(APPROVED_BOUNDS),
        "opaqueFootprintPixels": list(ART_SIZE),
        "roomPixels": list(ROOM_SIZE),
        "roomCellTopLeft": list(ROOM_CELL_TOP_LEFT),
        "ovenBoundsInRoomExclusive": list(OVEN_BOUNDS_ROOM),
        "floorSurfaceY": FLOOR_SURFACE_Y,
        "source": {"file": str(SOURCE.relative_to(ROOT)), "generator": "OpenAI built-in image generation", "sha256": SOURCE_SHA, "size": list(SOURCE_SIZE), "cropsExclusive": {name: list(crop) for name, crop in SOURCE_CROPS.items()}},
        "measurementAuthority": {"file": str(APPROVED_OVEN.relative_to(ROOT)), "sha256": APPROVED_OVEN_SHA, "cellPixels": list(CELL_SIZE), "opaqueBoundsExclusive": list(APPROVED_BOUNDS), "opaqueFootprintPixels": list(ART_SIZE), "hobRowsExclusive": [APPROVED_BOUNDS[1], HOB_SPLIT_Y], "hobPreservation": "byte-identical"},
        "colourAuthority": {"file": str(APPROVED_OVEN.relative_to(ROOT)), "approvedPaletteRGB": [list(colour) for colour in palette], "opaquePaletteColours": len(palette), "generatedPanelColoursRestrictedToApprovedOpaquePalette": True},
        "approvedContext": {"v39Room": str(BASE_ROOM.relative_to(ROOT)), "v39RoomSha256": BASE_ROOM_SHA, "fridgeApproval": "docs/review/kitchen-fridge-states-v39-approval-2026-10-18.json", "changed": False},
        "outputs": {name: {"sha256": sha(RAW / name), "size": list(image.size)} for name, image in outputs.items()},
        "opaqueBounds": {name: list(opaque_bbox(image)) for name, image in states.items()},
        "construction": {"fromScratchFascia": True, "coordinatedFamily": True, "sameSourceSheet": True, "approvedHobRetained": True, "approvedHobByteIdentical": True, "exactApprovedCellSize": True, "exactApprovedOpaqueFootprint": True, "previousOvenAndHobClearedBeforeComposite": True, "objectAnimated": False, "offInteriorDark": True, "offIndicatorDark": True, "onInteriorLight": True, "onDialsTurned": True, "onRedIndicator": True, "onRoastingTin": True, "brokenDoorAttachedAskew": True, "brokenDialHangingByTwoWires": True, "smokeBakedIntoObject": False, "flamesBakedIntoObject": False, "warningLightBakedIntoObject": False},
        "effects": {
            "flowing_smoke": {"file": "fx-oven-flowing-smoke-f40.png", "reusable": True, "frames": FX_FRAMES, "fps": FX_FPS, "durationSeconds": 10, "cellPixels": list(FX_CELL_SIZE), "roomTopLeft": list(FX_ROOM_TOP_LEFT), "effectOnly": True, "connectedPlume": True, "discreteBubblePuffs": False, "anchor": "broken_oven_cavity", "sfxCue": "kitchen_oven_broken_smoke_hiss_loop"},
            "hob_flames": {"file": "fx-oven-hob-flames-f40.png", "reusable": True, "frames": FX_FRAMES, "fps": FX_FPS, "durationSeconds": 10, "cellPixels": list(FX_CELL_SIZE), "roomTopLeft": list(FX_ROOM_TOP_LEFT), "effectOnly": True, "anchors": [[358, 142], [394, 142]], "sfxCue": "kitchen_oven_hob_flame_loop"},
            "warning_light_flicker": {"file": "fx-oven-warning-light-flicker-f40.png", "reusable": True, "frames": FX_FRAMES, "fps": FX_FPS, "durationSeconds": 10, "cellPixels": list(FX_CELL_SIZE), "roomTopLeft": list(FX_ROOM_TOP_LEFT), "effectOnly": True, "redIndicatorAnchor": [370, 155], "cavityFlicker": True, "redBurstFrames": 21, "cavityFlickerFrames": 5, "sfxCue": "kitchen_oven_broken_warning_light_angry_blink_loop"},
        },
        "sfxCues": ["kitchen_oven_on_fan_loop", "kitchen_oven_broken_smoke_hiss_loop", "kitchen_oven_hob_flame_loop", "kitchen_oven_broken_warning_light_angry_blink_loop"],
        "boundaries": {"approved": False, "promoted": False, "runtimeChanged": False, "finalChanged": False, "v40Changed": False, "otherKitchenAssetsRevised": False},
    }
    DRAFT.mkdir(parents=True, exist_ok=True)
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "version": 41,
        "status": "awaiting-oven-visual-review",
        "supersedesRejectedDraft": 40,
        "preservesApprovedFridge": 39,
        "measurementAuthoritySha256": APPROVED_OVEN_SHA,
        "originalHashes": {"v39Room": BASE_ROOM_SHA, "v21Oven": APPROVED_OVEN_SHA},
        "draftHashes": {name: sha(RAW / name) for name in outputs},
        "nextAssetBlockedUntilApproval": "kettle-or-user-selected-next-asset",
        "rollback": "Delete only V41 source/raw/draft/review/archive/builder/verifier/docs files; approved V39 and rejected V40 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "outputs": len(outputs), "paletteColours": len(palette)}, indent=2))


if __name__ == "__main__":
    main()
