#!/usr/bin/env python3
"""Build the reversible Kitchen V28 two-state bin review."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "art/source/kitchen-bin-states-2026-10-18-v28/generated"
RAW_DIR = ROOT / "art/raw/kitchen-bin-states-2026-10-18-v28"
DRAFT_DIR = ROOT / "art/drafts/kitchen-bin-states-2026-10-18-v28"
PUBLIC_DIR = ROOT / "public/keeper-review/kitchen-bin-states-v28"
ASSET_DIR = PUBLIC_DIR / "assets"

SOURCE_V1 = SOURCE_DIR / "bin-two-state-source-v1.png"
SOURCE_V2 = SOURCE_DIR / "bin-two-state-spill-source-v2.png"
ROOM = ROOT / "art/raw/kitchen-game-scale-prime-2026-10-17-v26/kitchen-game-scale-room.png"

SOURCE_V1_SHA = "d917330d83d2e9527e02dc7d8dbdaae0a9e27aa024879775839645a89f99d5ba"
SOURCE_V2_SHA = "f07c82b186dab52aff66fbde0ccabe23ef0f3428f64656dbe4f9716b6c74d1ec"
ROOM_SHA = "69df58a0db864cdb02064d4b236dcb7f31e56269dde61162d5f4cb388453558b"

STANDARD_CROP = (293, 182, 682, 831)
BROKEN_CROP = (1014, 53, 1691, 831)
CELL_SIZE = (72, 72)
STANDARD_SIZE = (32, 53)
BROKEN_SIZE = (56, 64)
BASELINE_Y = 68
ROOM_CELL_TOP_LEFT = (8, 149)
ROOM_ERASE_BOX = (18, 156, 70, 220)
FX_CELL_SIZE = (80, 80)
FX_FRAMES = 24
FX_FPS = 4
FX_ROOM_TOP_LEFT = (4, 104)


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


def reduce_state(source: Image.Image, crop: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    reduced = source.crop(crop).resize(size, Image.Resampling.LANCZOS)
    reduced = hard_alpha(reduced)
    palette = reduced.convert("RGB").quantize(colors=28, method=Image.Quantize.MEDIANCUT)
    rgb = palette.convert("RGB")
    return Image.merge("RGBA", (*rgb.split(), reduced.getchannel("A")))


def place_on_cell(sprite: Image.Image) -> Image.Image:
    cell = Image.new("RGBA", CELL_SIZE)
    x = (CELL_SIZE[0] - sprite.width) // 2
    y = BASELINE_Y - sprite.height
    cell.alpha_composite(sprite, (x, y))
    return cell


def draw_room_background(room: Image.Image) -> Image.Image:
    """Erase the V25 bin by interpolating the uninterrupted wall/floor rows."""
    clean = room.copy()
    x0, y0, x1, y1 = ROOM_ERASE_BOX
    pixels = clean.load()
    for y in range(y0, y1):
        left = pixels[x0 - 1, y]
        right = pixels[x1, y]
        width = x1 - x0
        for offset, x in enumerate(range(x0, x1), 1):
            t = offset / (width + 1)
            pixels[x, y] = tuple(round(left[channel] * (1 - t) + right[channel] * t) for channel in range(4))
    return clean


def room_variant(clean_room: Image.Image, sprite: Image.Image) -> Image.Image:
    result = clean_room.copy()
    result.alpha_composite(sprite, ROOM_CELL_TOP_LEFT)
    return result


def cloud_stamp(frame: Image.Image, x: int, y: int, scale: int, fade_step: int) -> None:
    """Paint one soft-edged but grid-crisp miasma puff."""
    shape = (
        "...###...",
        ".#######.",
        "#########",
        "#########",
        ".#######.",
        "..#####..",
        "...###...",
    )
    outline = (47, 74, 30, max(72, 190 - fade_step * 13))
    fill = (102, 139, 49, max(62, 166 - fade_step * 11))
    light = (157, 181, 76, max(42, 112 - fade_step * 8))
    mask = Image.new("L", FX_CELL_SIZE)
    draw = ImageDraw.Draw(mask)
    for row, cells in enumerate(shape):
        for column, value in enumerate(cells):
            if value == "#":
                draw.rectangle(
                    (x + column * scale, y + row * scale, x + (column + 1) * scale - 1, y + (row + 1) * scale - 1),
                    fill=255,
                )
    dilated = mask.filter(ImageFilter.MaxFilter(3))
    frame.alpha_composite(Image.composite(Image.new("RGBA", FX_CELL_SIZE, outline), Image.new("RGBA", FX_CELL_SIZE), dilated))
    frame.alpha_composite(Image.composite(Image.new("RGBA", FX_CELL_SIZE, fill), Image.new("RGBA", FX_CELL_SIZE), mask))
    highlight = Image.new("RGBA", FX_CELL_SIZE)
    ImageDraw.Draw(highlight).rectangle(
        (x + 3 * scale, y + scale, x + 5 * scale - 1, y + 2 * scale - 1),
        fill=light,
    )
    frame.alpha_composite(highlight)


def draw_stench_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    origin_x, origin_y = 40, 69
    # The stem always touches the bin opening, so the cloud never reads as a
    # detached overlay. Its staircase changes only every other frame.
    sway = round(2 * math.sin(frame_index * math.tau / FX_FRAMES))
    stem = [(origin_x, origin_y), (origin_x - 1, 65), (origin_x + sway, 61), (origin_x - 1 + sway, 57)]
    draw.line(stem, fill=(74, 108, 38, 182), width=2)
    draw.point((origin_x + 1, origin_y), fill=(157, 181, 76, 130))

    # Four overlapping puffs move one pixel only every 2–3 frames. Staggered
    # phases keep the six-second loop continuous without a simultaneous reset.
    for offset, direction in ((0, -1), (6, 1), (12, -1), (18, 1)):
        age = (frame_index - offset) % FX_FRAMES
        if age > 17:
            continue
        rise = age // 2
        drift = direction * round(3 * math.sin(age * math.pi / 18))
        scale = 1 if age < 7 else 2
        cloud_stamp(frame, origin_x - (9 * scale) // 2 + drift, 55 - rise * 3 - (scale - 1) * 3, scale, max(0, age - 9))
    return frame


def draw_flies_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    # Independent shallow orbits stay near the refuse and advance at no more
    # than roughly one pixel per frame. Wing shapes alternate every two frames.
    flies = ((0, 10, 5, 0.0), (8, 14, 7, 2.2), (16, 9, 4, 4.1))
    for phase, radius_x, radius_y, angle_offset in flies:
        angle = ((frame_index + phase) % FX_FRAMES) * math.tau / FX_FRAMES + angle_offset
        x = round(40 + math.cos(angle) * radius_x)
        y = round(55 + math.sin(angle) * radius_y)
        wing_up = ((frame_index + phase) // 2) % 2 == 0
        draw.point((x, y), fill=(19, 25, 28, 255))
        draw.point((x + 1, y), fill=(19, 25, 28, 255))
        wing_y = y - 1 if wing_up else y + 1
        draw.point((x - 1, wing_y), fill=(191, 205, 173, 220))
        draw.point((x + 2, wing_y), fill=(191, 205, 173, 220))
    return frame


def make_strip(draw_frame) -> Image.Image:
    strip = Image.new("RGBA", (FX_CELL_SIZE[0] * FX_FRAMES, FX_CELL_SIZE[1]))
    for frame_index in range(FX_FRAMES):
        strip.alpha_composite(draw_frame(frame_index), (frame_index * FX_CELL_SIZE[0], 0))
    return strip


def write_page() -> None:
    prefix = "/keeper-review/kitchen-bin-states-v28/assets"
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V28 · bin state family</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1120px;margin:auto;padding:22px}}h1,h2{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.stage{{overflow:auto;background:#02080b;border-radius:9px;padding:16px}}.states{{display:grid;grid-template-columns:repeat(2,minmax(260px,1fr));gap:16px}}.state{{text-align:center;background:#091e29;border:1px solid #315768;border-radius:11px;padding:14px}}.sprite{{width:288px;height:288px;object-fit:contain;image-rendering:pixelated;margin:auto}}.room-wrap{{position:relative;width:772px;height:224px;overflow:hidden}}.room{{position:absolute;inset:0;width:772px;height:224px;max-width:none}}.room-fx{{position:absolute;left:4px;top:104px;width:80px;height:80px;overflow:hidden}}.room-fx img{{height:80px;max-width:none;image-rendering:pixelated}}.fx-preview{{width:320px;height:320px;overflow:hidden;margin:auto}}.fx-preview img{{height:320px;max-width:none;image-rendering:pixelated}}button{{background:#147d78;color:white;border:0;border-radius:6px;padding:8px 10px;cursor:pointer}}button:disabled{{opacity:.45;cursor:wait}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}@media(max-width:680px){{.states{{grid-template-columns:1fr}}}}
</style></head><body><main><span class="tag">V28 draft</span><span class="tag">Static object</span><span class="tag">6-second reusable FX</span><span class="tag">Native game scale</span><h1>Pedal bin · coordinated two-state family</h1><p class="note">The standard and broken drawings were authored together from scratch. The bin itself is static in both states. The overflowing fault drives two separate reusable environmental overlays: a slow green miasma and slowly orbiting flies. Both run for six seconds at 4 fps and are anchored to the bin opening without moving the object.</p><p id="loading">Loading and decoding every review image and effect strip…</p>
<section><h2>Isolated state drawings · 4× inspection</h2><div class="states"><article class="state"><h3>Standard</h3><img data-media class="sprite" src="{prefix}/bin-standard.png" width="72" height="72" alt="Standard turquoise pedal bin"></article><article class="state"><h3>Broken · overflowing</h3><img data-media class="sprite" src="{prefix}/bin-broken-overflowing.png" width="72" height="72" alt="Overflowing turquoise pedal bin with raised lid and fallen rubbish"></article></div></section>
<section><h2>Standard in the complete kitchen · actual game size</h2><div class="stage"><div class="room-wrap"><img data-media class="room" src="{prefix}/kitchen-bin-standard-in-situ.png" width="772" height="224" alt="Standard bin in the complete Kitchen V26 room at game scale"></div></div></section>
<section><h2>Broken plus environmental fault · actual game size</h2><div class="stage"><div class="room-wrap"><img data-media class="room" src="{prefix}/kitchen-bin-broken-in-situ.png" width="772" height="224" alt="Overflowing bin and floor spill in the complete Kitchen V26 room at game scale"><div class="room-fx"><img data-media data-strip data-frames="24" data-fps="4" src="{prefix}/fx-stench-miasma-f24.png" width="1920" height="80" alt="Slow reusable green miasma effect"></div><div class="room-fx"><img data-media data-strip data-frames="24" data-fps="4" src="{prefix}/fx-slow-flies-f24.png" width="1920" height="80" alt="Slow reusable flies effect"></div></div></div><p>The floor spill may extend into the room; it remains inside the bin's isolated interaction cell and stops short of the fridge. The two animated layers are separate from the static object.</p></section>
<section><h2>Reusable environmental layers · 4× inspection</h2><div class="states"><article class="state"><h3>Green stench miasma</h3><div class="fx-preview"><img data-media data-strip data-frames="24" data-fps="4" src="{prefix}/fx-stench-miasma-f24.png" width="7680" height="320" alt="Reusable slow green miasma loop"></div><p>24 frames · 4 fps · 6 seconds</p></article><article class="state"><h3>Slow flies</h3><div class="fx-preview"><img data-media data-strip data-frames="24" data-fps="4" src="{prefix}/fx-slow-flies-f24.png" width="7680" height="320" alt="Reusable slow fly loop"></div><p>24 frames · 4 fps · 6 seconds</p><button data-sfx="kitchen_bin_flies_slow_loop">Play placeholder SFX</button></article></div></section>
<p class="warn"><strong>Version boundary:</strong> V27 is retained as rejected provenance. V28 is a new reversible state-family draft. Only reusable environmental overlays animate; the bin object remains static. No runtime manifest, Final art, approved V23 cabinet run, chair placement or Prime source is changed.</p>
</main><script>const media=[...document.querySelectorAll('[data-media]')],strips=[...document.querySelectorAll('[data-strip]')];Promise.all(media.map(el=>new Promise((ok,bad)=>{{if(el.complete){{el.decode?.().then(ok).catch(ok);return}}el.onload=()=>el.decode?.().then(ok).catch(ok)??ok();el.onerror=()=>bad(new Error('Could not load '+el.src))}}))).then(()=>{{document.body.classList.add('ready');document.querySelector('#loading').textContent='All state images and reusable effect strips loaded and decoded. Playback unlocked.';document.querySelectorAll('button').forEach(button=>button.disabled=false);const start=performance.now();function tick(now){{for(const image of strips){{const frame=Math.floor((now-start)*(+image.dataset.fps)/1000)%(+image.dataset.frames);image.style.transform=`translateX(${{-frame*image.parentElement.clientWidth}}px)`}}requestAnimationFrame(tick)}}requestAnimationFrame(tick)}}).catch(error=>document.querySelector('#loading').textContent='Review locked: '+error.message);document.querySelectorAll('button').forEach(button=>{{button.disabled=true;button.onclick=()=>{{const C=window.AudioContext||window.webkitAudioContext,c=new C,o=c.createOscillator(),g=c.createGain();o.type='sawtooth';o.frequency.setValueAtTime(118,c.currentTime);o.frequency.linearRampToValueAtTime(132,c.currentTime+.45);g.gain.setValueAtTime(.028,c.currentTime);g.gain.exponentialRampToValueAtTime(.001,c.currentTime+.5);o.connect(g).connect(c.destination);o.start();o.stop(c.currentTime+.5)}}}})</script></body></html>'''
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    (PUBLIC_DIR / "index.html").write_text(html)


def main() -> None:
    for path, expected in ((SOURCE_V1, SOURCE_V1_SHA), (SOURCE_V2, SOURCE_V2_SHA), (ROOM, ROOM_SHA)):
        if sha(path) != expected:
            raise RuntimeError(f"Pinned input changed: {path.relative_to(ROOT)}")

    source = Image.open(SOURCE_V2).convert("RGBA")
    if source.size != (1774, 887):
        raise RuntimeError(f"V28 source is {source.size}, expected 1774 x 887")
    standard = place_on_cell(reduce_state(source, STANDARD_CROP, STANDARD_SIZE))
    broken = place_on_cell(reduce_state(source, BROKEN_CROP, BROKEN_SIZE))

    room = Image.open(ROOM).convert("RGBA")
    if room.size != (772, 224):
        raise RuntimeError(f"V26 room is {room.size}, expected 772 x 224")
    clean_room = draw_room_background(room)
    stench_strip = make_strip(draw_stench_frame)
    flies_strip = make_strip(draw_flies_frame)
    outputs = {
        "bin-standard.png": standard,
        "bin-broken-overflowing.png": broken,
        "kitchen-bin-standard-in-situ.png": room_variant(clean_room, standard),
        "kitchen-bin-broken-in-situ.png": room_variant(clean_room, broken),
        "fx-stench-miasma-f24.png": stench_strip,
        "fx-slow-flies-f24.png": flies_strip,
    }

    for folder in (RAW_DIR, DRAFT_DIR, ASSET_DIR):
        folder.mkdir(parents=True, exist_ok=True)
    for name, image in outputs.items():
        image.save(RAW_DIR / name, optimize=True)
        copy(RAW_DIR / name, ASSET_DIR / name)

    catalogue = {
        "version": 28,
        "status": "static-bin-state-family-awaiting-visual-confirmation",
        "states": ["standard", "broken_overflowing"],
        "cellPixels": list(CELL_SIZE),
        "baselineYExclusive": BASELINE_Y,
        "roomPixels": list(room.size),
        "roomCellTopLeft": list(ROOM_CELL_TOP_LEFT),
        "source": {
            "initialSha256": SOURCE_V1_SHA,
            "spillRevisionSha256": SOURCE_V2_SHA,
            "standardCropExclusive": list(STANDARD_CROP),
            "brokenCropExclusive": list(BROKEN_CROP),
        },
        "outputs": {name: {"sha256": sha(RAW_DIR / name), "size": list(image.size)} for name, image in outputs.items()},
        "opaqueBounds": {
            "standard": list(opaque_bbox(standard)),
            "broken_overflowing": list(opaque_bbox(broken)),
        },
        "effects": {
            "stench_miasma": {
                "file": "fx-stench-miasma-f24.png",
                "reusable": True,
                "frames": FX_FRAMES,
                "fps": FX_FPS,
                "durationSeconds": FX_FRAMES / FX_FPS,
                "cellPixels": list(FX_CELL_SIZE),
                "roomTopLeft": list(FX_ROOM_TOP_LEFT),
                "objectPixelsChanged": False,
            },
            "slow_flies": {
                "file": "fx-slow-flies-f24.png",
                "reusable": True,
                "frames": FX_FRAMES,
                "fps": FX_FPS,
                "durationSeconds": FX_FRAMES / FX_FPS,
                "cellPixels": list(FX_CELL_SIZE),
                "roomTopLeft": list(FX_ROOM_TOP_LEFT),
                "objectPixelsChanged": False,
                "sfxCue": "kitchen_bin_flies_slow_loop",
            },
        },
        "boundaries": {
            "approved": False,
            "promoted": False,
            "objectAnimated": False,
            "environmentalFxAnimated": True,
            "runtimeChanged": False,
            "canonicalChanged": False,
            "v20ThroughV27Changed": False,
        },
    }
    (DRAFT_DIR / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT_DIR / "batch-register.json").write_text(json.dumps({
        "version": 28,
        "preserves": list(range(20, 28)),
        "v27Disposition": "rejected-provenance-retained",
        "rollback": "Delete only V28 source/raw/draft/review/archive/builder/verifier/docs files; V20-V27 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC_DIR.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
