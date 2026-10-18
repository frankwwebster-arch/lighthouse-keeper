#!/usr/bin/env python3
"""Build reversible Kitchen V39 from-scratch fridge states and water FX."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE_V1 = ROOT / "art/source/kitchen-fridge-states-2026-10-18-v39/generated/fridge-two-state-from-scratch-source-v1.png"
SOURCE = ROOT / "art/source/kitchen-fridge-states-2026-10-18-v39/generated/fridge-two-state-compact-hinge-source-v2.png"
BASE_ROOM = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v31/kitchen-bin-standard-in-situ.png"
RAW = ROOT / "art/raw/kitchen-fridge-states-2026-10-18-v39"
DRAFT = ROOT / "art/drafts/kitchen-fridge-states-2026-10-18-v39"
PUBLIC = ROOT / "public/keeper-review/kitchen-fridge-states-v39"
ASSETS = PUBLIC / "assets"

SOURCE_V1_SHA = "c0b3549d879584c17e9a3db57e15c140c3e99664fc114402b019f3eda71ec66d"
SOURCE_SHA = "48a8c8e03e2ea791d69124de2853d8223d8ce62801604461bd40405316fadaba"
BASE_ROOM_SHA = "027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674"

SOURCE_SIZE = (2172, 724)
SOURCE_CROPS = {
    "standard": (324, 145, 810, 584),
    "broken": (1156, 145, 1849, 621),
}
REDUCED_SIZES = {"standard": (84, 78), "broken": (120, 85)}
CELL_SIZE = (136, 104)
CELL_OFFSETS = {"standard": (26, 4), "broken": (2, 4)}
ROOM_SIZE = (772, 224)
ROOM_CELL_TOP_LEFT = (58, 136)
FRIDGE_BAY = (84, 140, 168, 218)
CLEAR_RECT = (84, 151, 168, 218)
CLONE_RECT = (168, 151, 252, 218)
FLOOR_SURFACE_Y = 218
FX_FRAMES = 40
FX_FPS = 4

WATER_DARK = (7, 84, 132, 220)
WATER = (32, 178, 211, 235)
WATER_LIGHT = (178, 244, 240, 245)


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
    reduced = source.crop(SOURCE_CROPS[name]).resize(REDUCED_SIZES[name], Image.Resampling.LANCZOS)
    alpha = reduced.getchannel("A").point(lambda value: 255 if value >= 80 else 0)
    palette = reduced.convert("RGB").quantize(colors=48, method=Image.Quantize.MEDIANCUT).convert("RGB")
    reduced = Image.merge("RGBA", (*palette.split(), alpha))
    cell = Image.new("RGBA", CELL_SIZE)
    cell.alpha_composite(reduced, CELL_OFFSETS[name])
    return cell


def clean_fridge_bay(room: Image.Image) -> Image.Image:
    """Remove every original-fridge pixel before any replacement is drawn."""
    clean = room.copy()
    # Keep the already-continuous y=140:150 worktop.  Clone only the cabinet
    # face and plinth, below every neighbouring worktop prop.
    clean.paste(room.crop(CLONE_RECT), CLEAR_RECT[:2])
    return clean


def room_variant(clean_room: Image.Image, sprite: Image.Image) -> Image.Image:
    result = clean_room.copy()
    result.alpha_composite(sprite, ROOM_CELL_TOP_LEFT)
    return result


def drip_ripple_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    cycle = frame_index % 20
    pass_index = frame_index // 20
    x = 111 + pass_index
    if cycle <= 11:
        progress = cycle / 11
        y = round(67 + (progress ** 1.45) * 15)
        tail = 1 if cycle < 7 else 2
        draw.rectangle((x, y - tail, x + 1, y + 1), fill=WATER_DARK)
        draw.point((x, y - tail), fill=WATER_LIGHT)
        if 5 <= cycle <= 9:
            draw.point((x, y - tail - 2), fill=(32, 178, 211, 155))
    else:
        age = cycle - 12
        width = 5 + age * 2
        alpha = max(35, 210 - age * 24)
        left = x - width // 2
        right = x + width // 2
        draw.arc((left, 83, right, 89), 180, 355, fill=WATER_DARK, width=1)
        draw.line((left + 2, 87, right - 2, 87), fill=(*WATER[:3], alpha), width=1)
        if age <= 3:
            draw.point((x, 85), fill=(*WATER_LIGHT[:3], max(25, alpha - 45)))
    return frame


def make_strip() -> Image.Image:
    strip = Image.new("RGBA", (CELL_SIZE[0] * FX_FRAMES, CELL_SIZE[1]))
    for frame_index in range(FX_FRAMES):
        strip.alpha_composite(drip_ripple_frame(frame_index), (frame_index * CELL_SIZE[0], 0))
    return strip


def save_output(name: str, image: Image.Image) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    image.save(RAW / name, optimize=True)
    copy(RAW / name, ASSETS / name)


def write_page() -> None:
    page = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-fridge-states-v39/"><title>Kitchen V39 · from-scratch fridge correction</title><style>
*{box-sizing:border-box}body{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}main{max-width:1160px;margin:auto;padding:22px}h1,h2,h3{line-height:1.12}.tag{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin:0 6px 5px 0;color:#9af1e9}section{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}.note{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}.warn{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}.grid{display:grid;grid-template-columns:repeat(2,minmax(300px,1fr));gap:16px}.card{text-align:center;background:#091e29;border:1px solid #315768;border-radius:11px;padding:14px}.checker{background-color:#e8f2ed;background-image:linear-gradient(45deg,#c4d7d0 25%,transparent 25%),linear-gradient(-45deg,#c4d7d0 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#c4d7d0 75%),linear-gradient(-45deg,transparent 75%,#c4d7d0 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0;border-radius:9px}.isolated{position:relative;width:544px;height:416px;max-width:100%;margin:auto;overflow:hidden}.isolated img{position:absolute;inset:0;width:544px;height:416px;max-width:none;image-rendering:pixelated}.stage{overflow:auto;background:#02080b;border-radius:9px;padding:16px}.room{position:relative;width:772px;height:224px;overflow:hidden}.room>img:first-child{position:absolute;inset:0;width:772px;height:224px;max-width:none}.room-fx{position:absolute;left:58px;top:136px;width:136px;height:104px;overflow:hidden}.room-fx img{height:104px;max-width:none;image-rendering:pixelated}.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}button{background:#147d78;color:white;border:0;border-radius:6px;padding:9px 12px;cursor:pointer}button:disabled{opacity:.45;cursor:wait}[data-media]{visibility:hidden}body.ready [data-media]{visibility:visible}code{color:#9af1e9}@media(max-width:760px){.grid{grid-template-columns:1fr}.isolated{transform-origin:top left;zoom:.62}}
</style></head><body><main><span class="tag">V39 corrective draft</span><span class="tag">Fridge only</span><span class="tag">From-scratch family</span><span class="tag">Old bay cleared first</span><h1>Fridge · standard and hinge-failed states redrawn together</h1><p class="note">V39 does not reuse V32 fridge pixels. Both states were redrawn from scratch in the approved storm-blue/sea-glass palette. The room compositor first removes every pixel of the previous fridge, then inserts exactly one new state. The measured floor surface is y=218; the fallen door and flattened pool meet that surface.</p><p id="loading">Loading and decoding every unique review image before playback…</p><div class="controls"><button id="play" disabled>Play loop</button><button id="pause" disabled>Pause</button><button id="buzz" disabled>Play low buzz placeholder</button></div>
<section><h2>Isolated state drawings · 4× inspection</h2><div class="grid"><article class="card"><h3>Standard</h3><div class="checker isolated"><img data-media src="assets/fridge-standard.png" width="544" height="416" alt="From-scratch standard fitted fridge"></div></article><article class="card"><h3>Broken · static state</h3><div class="checker isolated"><img data-media src="assets/fridge-broken-hinge-failed.png" width="544" height="416" alt="From-scratch broken fridge with one grille, connected lower hinge, fallen door and floor pool"></div><p>The top hinge has failed. One compact lower-right hinge arm visibly connects the door to the carcass. Generic milk, jar and produce shapes show that it is not empty.</p></article></div></section>
<section><h2>Compositing proof · previous fridge removed</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-fridge-cleared-bay.png" width="772" height="224" alt="Complete kitchen with the original fridge bay fully cleared before replacement"></div></div><p>This intermediate proof exists only to expose the construction: no white door, grille, hinge or plinth pixels from the previous fridge remain in the bay.</p></section>
<section><h2>Standard in the complete kitchen · exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-fridge-standard-in-situ.png" width="772" height="224" alt="From-scratch standard fridge in the complete kitchen at exact game size"></div></div></section>
<section><h2>Broken in the complete kitchen · exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-fridge-broken-in-situ.png" width="772" height="224" alt="From-scratch broken fridge in the complete kitchen at exact game size"><i class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-fridge-drip-ripple-f40.png" width="5440" height="104" alt="Reusable slow fridge drip and pool ripple effect"></i></div></div><p>The object and pool are static. No smoke, sparks or electrical flash; the low electrical buzz remains sound-only.</p></section>
<section><h2>Reusable drip and ripple only · 4× inspection</h2><div class="checker isolated"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-fridge-drip-ripple-f40.png" width="21760" height="416" alt="Effect-only forty-frame slow drip and restrained floor ripple"></div><p>No fridge artwork is present in this strip: 40 isolated frames · 4 fps · 10 seconds.</p></section>
<section><h2>Broken state plus reusable effect · 4× inspection</h2><div class="checker isolated"><img data-media src="assets/fridge-broken-hinge-failed.png" width="544" height="416" alt="Static broken fridge"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-fridge-drip-ripple-f40.png" width="21760" height="416" alt="Separate slow drip and floor ripple over the broken fridge"></div></section>
<p class="warn"><strong>Review boundary:</strong> V32 and V33–V38 are rejected provenance. V39 is the only active fridge correction and remains reversible, unpromoted and unwired. No kettle or later asset has been revised.</p>
</main><script>
const strips=[...document.querySelectorAll('[data-strip]')],controls=[...document.querySelectorAll('button')];let playing=false,start=0,held=0,raf=0;function render(now){if(!playing)return;const elapsed=held+(now-start);for(const image of strips){const frame=Math.floor(elapsed*(+image.dataset.fps)/1000)%(+image.dataset.frames),w=image.parentElement.clientWidth;image.style.transform=`translateX(${-frame*w}px)`}raf=requestAnimationFrame(render)}function play(){if(playing)return;playing=true;start=performance.now();raf=requestAnimationFrame(render)}function pause(){if(!playing)return;held+=performance.now()-start;playing=false;cancelAnimationFrame(raf)}function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}const unique=[...new Set([...document.querySelectorAll('[data-media]')].map(image=>image.src))];Promise.all(unique.map(preload)).then(()=>{document.body.classList.add('ready');controls.forEach(button=>button.disabled=false);loading.textContent=`All ${unique.length} unique state/effect images loaded and decoded. Playback unlocked.`;play()}).catch(error=>loading.textContent='Review locked: '+error.message);play.onclick=play;pause.onclick=pause;buzz.onclick=()=>{const C=window.AudioContext||window.webkitAudioContext,c=new C,o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.setValueAtTime(58,c.currentTime);o.frequency.linearRampToValueAtTime(62,c.currentTime+1.2);g.gain.setValueAtTime(.022,c.currentTime);g.gain.exponentialRampToValueAtTime(.001,c.currentTime+1.35);o.connect(g).connect(c.destination);o.start();o.stop(c.currentTime+1.4)};
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    for path, expected in ((SOURCE_V1, SOURCE_V1_SHA), (SOURCE, SOURCE_SHA), (BASE_ROOM, BASE_ROOM_SHA)):
        if sha(path) != expected:
            raise RuntimeError(f"Pinned input changed: {path.relative_to(ROOT)}")
    with Image.open(SOURCE) as image:
        source = image.convert("RGBA")
    if source.size != SOURCE_SIZE:
        raise RuntimeError(f"Generated source is {source.size}, expected {SOURCE_SIZE}")
    with Image.open(BASE_ROOM) as image:
        room = image.convert("RGBA")
    standard = reduce_state(source, "standard")
    broken = reduce_state(source, "broken")
    clean_room = clean_fridge_bay(room)
    effect = make_strip()
    outputs = {
        "fridge-standard.png": standard,
        "fridge-broken-hinge-failed.png": broken,
        "kitchen-fridge-cleared-bay.png": clean_room,
        "kitchen-fridge-standard-in-situ.png": room_variant(clean_room, standard),
        "kitchen-fridge-broken-in-situ.png": room_variant(clean_room, broken),
        "fx-fridge-drip-ripple-f40.png": effect,
    }
    for name, image in outputs.items():
        save_output(name, image)

    catalogue = {
        "version": 39,
        "status": "from-scratch-fridge-correction-awaiting-review",
        "states": ["standard", "broken_hinge_failed"],
        "densityPxPerLp": 4,
        "cellPixels": list(CELL_SIZE),
        "roomPixels": list(ROOM_SIZE),
        "roomCellTopLeft": list(ROOM_CELL_TOP_LEFT),
        "fridgeBayPixels": list(FRIDGE_BAY),
        "floorSurfaceY": FLOOR_SURFACE_Y,
        "source": {
            "file": str(SOURCE.relative_to(ROOT)),
            "generator": "OpenAI built-in image generation",
            "sha256": SOURCE_SHA,
            "provenance": [{"file": str(SOURCE_V1.relative_to(ROOT)), "sha256": SOURCE_V1_SHA, "role": "initial-from-scratch-family"}],
            "size": list(SOURCE_SIZE),
            "cropsExclusive": {name: list(crop) for name, crop in SOURCE_CROPS.items()},
            "reducedSizes": {name: list(size) for name, size in REDUCED_SIZES.items()},
        },
        "originalAuthority": {"room": str(BASE_ROOM.relative_to(ROOT)), "roomSha256": BASE_ROOM_SHA, "changed": False},
        "outputs": {name: {"sha256": sha(RAW / name), "size": list(image.size)} for name, image in outputs.items()},
        "opaqueBounds": {"standard": list(opaque_bbox(standard)), "broken_hinge_failed": list(opaque_bbox(broken))},
        "construction": {
            "fromScratch": True,
            "coordinatedFamily": True,
            "sameSourceSheet": True,
            "previousFridgeClearedBeforeComposite": True,
            "objectAnimated": False,
            "topHingeFailed": True,
            "lowerRightHingeAttached": True,
            "singleGrillePerState": True,
            "doorLowerLeftRestsOnFloor": True,
            "staticPoolOnFloorSurface": True,
            "visibleElectricalEffects": False,
        },
        "effects": {"slow_drip_pool_ripple": {"file": "fx-fridge-drip-ripple-f40.png", "reusable": True, "frames": FX_FRAMES, "fps": FX_FPS, "durationSeconds": FX_FRAMES / FX_FPS, "cellPixels": list(CELL_SIZE), "roomTopLeft": list(ROOM_CELL_TOP_LEFT), "effectOnly": True, "sfxCue": "kitchen_fridge_water_drip_slow"}},
        "sfxCues": [
            {"cue": "kitchen_fridge_low_electrical_buzz_loop", "state": "broken_hinge_failed", "visibleEffect": False},
            {"cue": "kitchen_fridge_water_drip_slow", "state": "broken_hinge_failed", "visibleEffect": "slow_drip_pool_ripple"},
        ],
        "boundaries": {"approved": False, "promoted": False, "runtimeChanged": False, "finalChanged": False, "v32ThroughV38Rejected": True, "laterAssetsRevised": False},
    }
    DRAFT.mkdir(parents=True, exist_ok=True)
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "version": 39,
        "status": "awaiting-fridge-visual-review",
        "supersedesRejectedDraft": 32,
        "rejectedBatch": list(range(33, 39)),
        "originalHashes": {"v31Room": BASE_ROOM_SHA},
        "draftHashes": {name: sha(RAW / name) for name in outputs},
        "nextAssetBlockedUntilApproval": "kettle",
        "rollback": "Delete only V39 source/raw/draft/review/archive/builder/verifier/docs files; V31 and rejected V32-V38 provenance remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
