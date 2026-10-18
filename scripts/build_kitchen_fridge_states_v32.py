#!/usr/bin/env python3
"""Build reversible Kitchen V32 coordinated fridge states and water FX."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE_V1 = ROOT / "art/source/kitchen-fridge-states-2026-10-18-v32/generated/fridge-two-state-source-v1.png"
SOURCE_V2 = ROOT / "art/source/kitchen-fridge-states-2026-10-18-v32/generated/fridge-two-state-contents-source-v2.png"
SOURCE = ROOT / "art/source/kitchen-fridge-states-2026-10-18-v32/generated/fridge-two-state-floor-contact-source-v3.png"
BASE_ROOM = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v31/kitchen-bin-standard-in-situ.png"
CURRENT_FRIDGE = ROOT / "art/raw/kitchen-final-assets-2026-10-17-v21/fridge.png"
RAW = ROOT / "art/raw/kitchen-fridge-states-2026-10-18-v32"
DRAFT = ROOT / "art/drafts/kitchen-fridge-states-2026-10-18-v32"
PUBLIC = ROOT / "public/keeper-review/kitchen-fridge-states-v32"
ASSETS = PUBLIC / "assets"

SOURCE_V1_SHA = "fadbe42e57d9b8611e23d3be10c513e6481c5b847e774c4a26e1d9eb78bc0980"
SOURCE_V2_SHA = "07dd6abc154ac667ae004f8d133f3c8e681080b642496b8fb11c86b0d78dded3"
SOURCE_SHA = "0a69aa583eb9964ad17886b88f486e1c7d7d938938725df856cf5118b50e549d"
BASE_ROOM_SHA = "027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674"
CURRENT_FRIDGE_SHA = "e59142a1ed4d7181daa2b4968061642416e3d3352c1cbd3fd7e053676c25da6c"

SOURCE_SIZE = (2169, 725)
SOURCE_CROPS = {
    "standard": (310, 140, 1030, 680),
    "broken": (1050, 140, 1770, 680),
}
REDUCED_SIZE = (116, 80)
CELL_SIZE = (120, 96)
CELL_OFFSET = (2, 11)
ROOM_SIZE = (772, 224)
ROOM_CELL_TOP_LEFT = (66, 127)
FRIDGE_BAY_X = (84, 168)
FRIDGE_FOOT_Y = 208
FX_FRAMES = 40
FX_FPS = 4

NAVY = (4, 20, 48, 255)
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


def hard_alpha(image: Image.Image, threshold: int = 80) -> Image.Image:
    alpha = image.getchannel("A").point(lambda value: 255 if value >= threshold else 0)
    image.putalpha(alpha)
    return image


def reduce_state(source: Image.Image, crop: tuple[int, int, int, int]) -> Image.Image:
    reduced = source.crop(crop).resize(REDUCED_SIZE, Image.Resampling.LANCZOS)
    reduced = hard_alpha(reduced)
    palette = reduced.convert("RGB").quantize(colors=40, method=Image.Quantize.MEDIANCUT)
    rgb = palette.convert("RGB")
    reduced = Image.merge("RGBA", (*rgb.split(), reduced.getchannel("A")))
    cell = Image.new("RGBA", CELL_SIZE)
    cell.alpha_composite(reduced, CELL_OFFSET)
    return cell


def drip_ripple_frame(frame_index: int) -> Image.Image:
    """Draw two slow drips per ten seconds and a restrained impact ripple."""
    frame = Image.new("RGBA", CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    cycle = frame_index % 20
    pass_index = frame_index // 20
    x = 88 + pass_index * 2

    if cycle <= 11:
        progress = cycle / 11
        y = round(68 + (progress ** 1.45) * 15)
        tail = 1 if cycle < 7 else 2
        draw.rectangle((x, y - tail, x + 1, y + 1), fill=WATER_DARK)
        draw.point((x, y - tail), fill=WATER_LIGHT)
        if 5 <= cycle <= 9:
            draw.point((x, y - tail - 2), fill=(32, 178, 211, 155))
    else:
        ripple_age = cycle - 12
        width = 5 + ripple_age * 2
        alpha = max(35, 210 - ripple_age * 24)
        ripple = (WATER[0], WATER[1], WATER[2], alpha)
        light = (WATER_LIGHT[0], WATER_LIGHT[1], WATER_LIGHT[2], max(25, alpha - 45))
        left = x - width // 2
        right = x + width // 2
        draw.arc((left, 84, right, 89), 180, 355, fill=WATER_DARK, width=1)
        draw.line((left + 2, 87, right - 2, 87), fill=ripple, width=1)
        if ripple_age <= 3:
            draw.point((x, 85), fill=light)
    return frame


def make_strip() -> Image.Image:
    strip = Image.new("RGBA", (CELL_SIZE[0] * FX_FRAMES, CELL_SIZE[1]))
    for frame_index in range(FX_FRAMES):
        strip.alpha_composite(drip_ripple_frame(frame_index), (frame_index * CELL_SIZE[0], 0))
    return strip


def room_variant(room: Image.Image, sprite: Image.Image) -> Image.Image:
    result = room.copy()
    result.alpha_composite(sprite, ROOM_CELL_TOP_LEFT)
    return result


def save_output(name: str, image: Image.Image) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    image.save(RAW / name, optimize=True)
    copy(RAW / name, ASSETS / name)


def write_page() -> None:
    page = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-fridge-states-v32/"><title>Kitchen V32 · coordinated fridge states</title><style>
*{box-sizing:border-box}body{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}main{max-width:1160px;margin:auto;padding:22px}h1,h2,h3{line-height:1.12}.tag{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin:0 6px 5px 0;color:#9af1e9}section{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}.note{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}.warn{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}.grid{display:grid;grid-template-columns:repeat(2,minmax(300px,1fr));gap:16px}.card{text-align:center;background:#091e29;border:1px solid #315768;border-radius:11px;padding:14px}.checker{background-color:#e8f2ed;background-image:linear-gradient(45deg,#c4d7d0 25%,transparent 25%),linear-gradient(-45deg,#c4d7d0 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#c4d7d0 75%),linear-gradient(-45deg,transparent 75%,#c4d7d0 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0;border-radius:9px}.isolated{position:relative;width:480px;height:384px;max-width:100%;margin:auto;overflow:hidden}.isolated img{position:absolute;inset:0;width:480px;height:384px;max-width:none;image-rendering:pixelated}.stage{overflow:auto;background:#02080b;border-radius:9px;padding:16px}.room{position:relative;width:772px;height:224px;overflow:hidden}.room>img:first-child{position:absolute;inset:0;width:772px;height:224px;max-width:none}.room-fx{position:absolute;left:66px;top:127px;width:120px;height:96px;overflow:hidden}.room-fx img{height:96px;max-width:none;image-rendering:pixelated}.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}button{background:#147d78;color:white;border:0;border-radius:6px;padding:9px 12px;cursor:pointer}button:disabled{opacity:.45;cursor:wait}[data-media]{visibility:hidden}body.ready [data-media]{visibility:visible}code{color:#9af1e9}@media(max-width:760px){.grid{grid-template-columns:1fr}.isolated{transform-origin:top left;zoom:.72}}
</style></head><body><main><span class="tag">V32 draft</span><span class="tag">Fridge only</span><span class="tag">Static object</span><span class="tag">10-second reusable FX</span><h1>Fridge · coordinated standard and broken family</h1><p class="note">Both states were drawn together from one construction. The failed door remains on its lower-right hinge and rests on the floor. The door and leaked pool are static; only the separate falling-drip and restrained-ripple layer moves.</p><p id="loading">Loading and decoding every unique review image before playback…</p><div class="controls"><button id="play" disabled>Play loop</button><button id="pause" disabled>Pause</button><button id="buzz" disabled>Play low buzz placeholder</button></div>
<section><h2>Isolated state drawings · 4× inspection</h2><div class="grid"><article class="card"><h3>Standard</h3><div class="checker isolated"><img data-media src="assets/fridge-standard.png" width="480" height="384" alt="Standard fitted undercounter fridge"></div></article><article class="card"><h3>Broken · static state</h3><div class="checker isolated"><img data-media src="assets/fridge-broken-hinge-failed.png" width="480" height="384" alt="Broken fridge with top hinge failed, lower hinge attached, fallen door and static pool"></div><p>Sparse unlabelled milk, jar and produce shapes make the cavity read as used, not empty.</p></article></div></section>
<section><h2>Approved current fridge versus V32 standard</h2><div class="grid"><article class="card"><h3>Current V21/V23 authority</h3><div class="checker isolated"><img data-media src="assets/fridge-v21-current.png" style="object-fit:contain" width="480" height="384" alt="Current V21 fridge used by the approved V23 room"></div></article><article class="card"><h3>V32 new coordinated construction</h3><div class="checker isolated"><img data-media src="assets/fridge-standard.png" width="480" height="384" alt="V32 standard fridge"></div></article></div><p>The earlier pixels remain immutable; V32 is a separate draft and can be rejected by discarding only its versioned files.</p></section>
<section><h2>Standard in the complete kitchen · exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-fridge-standard-in-situ.png" width="772" height="224" alt="Standard V32 fridge in the complete approved kitchen at exact game size"></div></div></section>
<section><h2>Broken in the complete kitchen · exact 772 × 224 game pixels</h2><div class="stage"><div class="room"><img data-media src="assets/kitchen-fridge-broken-in-situ.png" width="772" height="224" alt="Broken V32 fridge in the complete approved kitchen at exact game size"><i class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-fridge-drip-ripple-f40.png" width="4800" height="96" alt="Reusable slow fridge drip and pool ripple effect"></i></div></div><p>No smoke, sparks or electrical flash. The named low electrical buzz is sound-only.</p></section>
<section><h2>Reusable drip and ripple · 4× inspection</h2><div class="checker isolated"><img data-media src="assets/fridge-broken-hinge-failed.png" width="480" height="384" alt="Static broken fridge"><img data-media data-strip data-frames="40" data-fps="4" src="assets/fx-fridge-drip-ripple-f40.png" width="19200" height="384" alt="Forty-frame slow drip and restrained pool ripple"></div><p>40 frames · 4 fps · 10 seconds · transparent safety gutters · separate from the object pixels</p></section>
<p class="warn"><strong>Version boundary:</strong> V20–V31, Final art and runtime remain unchanged. V32 is a reversible visual-review draft for the fridge only. Do not begin the kettle until this fridge has been reviewed.</p>
</main><script>
const strips=[...document.querySelectorAll('[data-strip]')],controls=[...document.querySelectorAll('button')];let playing=false,start=0,held=0,raf=0;function render(now){if(!playing)return;const elapsed=held+(now-start);for(const image of strips){const frame=Math.floor(elapsed*(+image.dataset.fps)/1000)%(+image.dataset.frames),w=image.parentElement.clientWidth;image.style.transform=`translateX(${-frame*w}px)`}raf=requestAnimationFrame(render)}function play(){if(playing)return;playing=true;start=performance.now();raf=requestAnimationFrame(render)}function pause(){if(!playing)return;held+=performance.now()-start;playing=false;cancelAnimationFrame(raf)}function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}const unique=[...new Set([...document.querySelectorAll('[data-media]')].map(image=>image.src))];Promise.all(unique.map(preload)).then(()=>{document.body.classList.add('ready');controls.forEach(button=>button.disabled=false);loading.textContent=`All ${unique.length} unique state/effect images loaded and decoded. Playback unlocked.`;play()}).catch(error=>loading.textContent='Review locked: '+error.message);play.onclick=play;pause.onclick=pause;buzz.onclick=()=>{const C=window.AudioContext||window.webkitAudioContext,c=new C,o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.setValueAtTime(58,c.currentTime);o.frequency.linearRampToValueAtTime(62,c.currentTime+1.2);g.gain.setValueAtTime(.022,c.currentTime);g.gain.exponentialRampToValueAtTime(.001,c.currentTime+1.35);o.connect(g).connect(c.destination);o.start();o.stop(c.currentTime+1.4)};
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    pinned = ((SOURCE_V1, SOURCE_V1_SHA), (SOURCE_V2, SOURCE_V2_SHA), (SOURCE, SOURCE_SHA), (BASE_ROOM, BASE_ROOM_SHA), (CURRENT_FRIDGE, CURRENT_FRIDGE_SHA))
    for path, expected in pinned:
        if sha(path) != expected:
            raise RuntimeError(f"Pinned input changed: {path.relative_to(ROOT)}")

    with Image.open(SOURCE) as image:
        source = image.convert("RGBA")
    if source.size != SOURCE_SIZE:
        raise RuntimeError(f"Generated source is {source.size}, expected {SOURCE_SIZE}")
    standard = reduce_state(source, SOURCE_CROPS["standard"])
    broken = reduce_state(source, SOURCE_CROPS["broken"])
    with Image.open(BASE_ROOM) as image:
        room = image.convert("RGBA")
    if room.size != ROOM_SIZE:
        raise RuntimeError(f"Base room is {room.size}, expected {ROOM_SIZE}")
    with Image.open(CURRENT_FRIDGE) as image:
        current_fridge = image.convert("RGBA")
    effect = make_strip()

    outputs = {
        "fridge-v21-current.png": current_fridge,
        "fridge-standard.png": standard,
        "fridge-broken-hinge-failed.png": broken,
        "kitchen-fridge-standard-in-situ.png": room_variant(room, standard),
        "kitchen-fridge-broken-in-situ.png": room_variant(room, broken),
        "fx-fridge-drip-ripple-f40.png": effect,
    }
    for name, image in outputs.items():
        save_output(name, image)

    catalogue = {
        "version": 32,
        "status": "fridge-state-family-awaiting-visual-confirmation",
        "states": ["standard", "broken_hinge_failed"],
        "densityPxPerLp": 4,
        "cellPixels": list(CELL_SIZE),
        "roomPixels": list(ROOM_SIZE),
        "roomCellTopLeft": list(ROOM_CELL_TOP_LEFT),
        "fridgeBayPixels": list(FRIDGE_BAY_X),
        "fridgeFootY": FRIDGE_FOOT_Y,
        "source": {
            "file": str(SOURCE.relative_to(ROOT)),
            "generator": "OpenAI built-in image generation",
            "sha256": SOURCE_SHA,
            "provenance": [
                {"file": str(SOURCE_V1.relative_to(ROOT)), "sha256": SOURCE_V1_SHA, "role": "initial-coordinated-source"},
                {"file": str(SOURCE_V2.relative_to(ROOT)), "sha256": SOURCE_V2_SHA, "role": "contents-revision"},
            ],
            "size": list(SOURCE_SIZE),
            "sharedReducedSize": list(REDUCED_SIZE),
            "cropsExclusive": {name: list(crop) for name, crop in SOURCE_CROPS.items()},
        },
        "originalAuthority": {
            "fridge": str(CURRENT_FRIDGE.relative_to(ROOT)),
            "fridgeSha256": CURRENT_FRIDGE_SHA,
            "room": str(BASE_ROOM.relative_to(ROOT)),
            "roomSha256": BASE_ROOM_SHA,
            "changed": False,
        },
        "outputs": {name: {"sha256": sha(RAW / name), "size": list(image.size)} for name, image in outputs.items()},
        "opaqueBounds": {"standard": list(opaque_bbox(standard)), "broken_hinge_failed": list(opaque_bbox(broken))},
        "construction": {
            "coordinatedFamily": True,
            "sameSourceSheet": True,
            "objectAnimated": False,
            "topHingeFailed": True,
            "lowerRightHingeAttached": True,
            "doorLowerLeftRestsOnFloor": True,
            "staticPoolIncluded": True,
            "visibleElectricalEffects": False,
        },
        "effects": {
            "slow_drip_pool_ripple": {
                "file": "fx-fridge-drip-ripple-f40.png",
                "reusable": True,
                "frames": FX_FRAMES,
                "fps": FX_FPS,
                "durationSeconds": FX_FRAMES / FX_FPS,
                "cellPixels": list(CELL_SIZE),
                "roomTopLeft": list(ROOM_CELL_TOP_LEFT),
                "objectPixelsChanged": False,
                "sfxCue": "kitchen_fridge_water_drip_slow",
            }
        },
        "sfxCues": [
            {"cue": "kitchen_fridge_low_electrical_buzz_loop", "state": "broken_hinge_failed", "visibleEffect": False},
            {"cue": "kitchen_fridge_water_drip_slow", "state": "broken_hinge_failed", "visibleEffect": "slow_drip_pool_ripple"},
        ],
        "boundaries": {
            "approved": False,
            "promoted": False,
            "runtimeChanged": False,
            "finalChanged": False,
            "v20ThroughV31Changed": False,
            "laterKitchenAssetsStarted": False,
        },
    }
    DRAFT.mkdir(parents=True, exist_ok=True)
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "version": 32,
        "status": "awaiting-fridge-visual-review",
        "preserves": list(range(20, 32)),
        "originalHashes": {"v21Fridge": CURRENT_FRIDGE_SHA, "v31Room": BASE_ROOM_SHA},
        "draftHashes": {name: sha(RAW / name) for name in outputs},
        "nextAssetBlockedUntilApproval": "kettle",
        "rollback": "Delete only V32 source/raw/draft/review/archive/builder/verifier/docs files; V20-V31 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
