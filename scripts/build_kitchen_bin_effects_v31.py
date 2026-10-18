#!/usr/bin/env python3
"""Build Kitchen V31: child-readable comic stink trails, haze and flies."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ModuleNotFoundError:
    Image = ImageDraw = None


ROOT = Path(__file__).resolve().parents[1]
V30_RAW = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v30"
RAW_DIR = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v31"
DRAFT_DIR = ROOT / "art/drafts/kitchen-bin-effects-2026-10-18-v31"
PUBLIC_DIR = ROOT / "public/keeper-review/kitchen-bin-effects-v31"
ASSET_DIR = PUBLIC_DIR / "assets"

STATIC_HASHES = {
    "bin-standard.png": "86b05224a7da5fc5c05918f2875018920ed54cf46fc00cb08952ffd29789f9c0",
    "bin-broken-overflowing.png": "77ad87fabfd3e5c10a4a14f294af343a5d93a2a2015e6d77f18a4140b1f5fb4f",
    "kitchen-bin-standard-in-situ.png": "027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674",
    "kitchen-bin-broken-in-situ.png": "bf1c741f9ff7e985ddc44584c9c13c76c60e0df8104d34a2a11848f1be58a1c3",
}
V30_MIASMA_SHA = "99ba9d9c316d20a628ffafa8cc12693d5b63df77efb468854d29827a3edd2181"
V29_FLIES_SHA = "28f3b35fdfe91d655ebe47914d17c948203f2def6bfa6b8fd5e2bf0a2b86cc5c"

FX_CELL_SIZE = (80, 80)
FX_FRAMES = 40
FX_FPS = 4
FX_ROOM_TOP_LEFT = (4, 104)

TRAIL_DARK = (50, 96, 43, 150)
TRAIL_MAIN = (58, 100, 45, 175)
TRAIL_MID = (58, 106, 48, 140)
TRAIL_LIGHT = (108, 148, 77, 80)
HAZE_DARK = (46, 87, 39, 76)
HAZE_MID = (65, 110, 51, 48)
HAZE_LIGHT = (118, 158, 86, 50)
TRACE = (105, 146, 72, 34)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def phase(frame: int, offset: float = 0.0) -> float:
    return math.tau * frame / FX_FRAMES + offset


def paint_haze(frame: Image.Image, frame_index: int) -> None:
    """Paint loose, discontinuous haze behind the readable smell trails."""
    draw = ImageDraw.Draw(frame)
    step = frame_index // 5
    patches = (
        (31, 42, 15, 8, HAZE_DARK, 0.1),
        (48, 35, 18, 9, HAZE_MID, 2.2),
        (35, 24, 20, 8, HAZE_MID, 4.0),
        (49, 15, 14, 6, HAZE_LIGHT, 5.3),
    )
    for index, (cx, cy, width, height, colour, offset) in enumerate(patches):
        drift = round(3 * math.sin(phase(frame_index, offset)))
        notch = (step + index) % 3
        left, right = cx + drift - width // 2, cx + drift + width // 2
        top, bottom = cy - height // 2, cy + height // 2
        shape = [
            (left + 2 + notch, top),
            (right - 3, top - 1),
            (right + 1, cy),
            (right - 2, bottom),
            (left + 4, bottom + 1),
            (left - 1, cy + 1),
        ]
        draw.polygon(shape, fill=colour)
        draw.rectangle((cx + drift - 3, cy - 1, cx + drift + 1, cy + 1), fill=(0, 0, 0, 0))
        draw.point((left + 2, bottom - 1), fill=TRACE)
        draw.point((right - 1, top + 1), fill=TRAIL_LIGHT)


def paint_smell_trail(
    frame: Image.Image,
    frame_index: int,
    base_x: int,
    base_y: int,
    top_y: int,
    amplitude: float,
    offset: float,
    colour: tuple[int, int, int, int],
    width: int,
) -> None:
    """Draw one slow curling comic stink line with a hooked open end."""
    draw = ImageDraw.Draw(frame)
    time = phase(frame_index, offset)
    points: list[tuple[int, int]] = []
    span = base_y - top_y
    for y in range(base_y, top_y - 1, -3):
        progress = (base_y - y) / span
        wave = math.sin(progress * math.tau * 1.35 + time)
        drift = math.sin(time * 0.5 + offset) * progress * 2
        x = round(base_x + wave * amplitude + drift)
        points.append((x, y))
    draw.line(points, fill=colour, width=width)

    end_x, end_y = points[-1]
    hook_sign = -1 if math.sin(time) < 0 else 1
    hook = [
        (end_x, end_y),
        (end_x + hook_sign * 2, end_y - 2),
        (end_x + hook_sign * 5, end_y - 2),
        (end_x + hook_sign * 6, end_y),
    ]
    draw.line(hook, fill=colour, width=width)


def draw_stench_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    paint_haze(frame, frame_index)
    paint_smell_trail(frame, frame_index, 34, 61, 19, 3.2, 0.2, TRAIL_DARK, 2)
    paint_smell_trail(frame, frame_index, 40, 69, 8, 4.0, 2.0, TRAIL_MAIN, 3)
    paint_smell_trail(frame, frame_index, 47, 60, 16, 3.4, 4.2, TRAIL_MID, 2)

    draw = ImageDraw.Draw(frame)
    draw.line([(39, 69), (40, 66), (40, 63)], fill=TRAIL_MAIN, width=2)
    draw.point((41, 69), fill=TRAIL_LIGHT)
    return frame


def draw_flies_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    flies = (
        (0.0, 12, 6, 0),
        (2.1, 16, 8, 6),
        (4.4, 9, 5, 13),
    )
    for offset, radius_x, radius_y, wing_offset in flies:
        angle = phase(frame_index, offset)
        wobble = round(math.sin(angle * 2.3 + offset) * 2)
        x = round(40 + math.cos(angle) * radius_x)
        y = round(53 + math.sin(angle) * radius_y) + wobble
        body = (19, 25, 28, 255)
        wing = (191, 205, 173, 220)
        draw.rectangle((x, y, x + 1, y + 1), fill=body)
        wing_up = ((frame_index + wing_offset) // 3) % 2 == 0
        wing_y = y - 1 if wing_up else y + 2
        draw.line((x - 2, wing_y, x - 1, wing_y), fill=wing, width=1)
        draw.line((x + 2, wing_y, x + 3, wing_y), fill=wing, width=1)
        if (frame_index + wing_offset) % 5 < 2:
            draw.point((x - 3, y + (1 if wing_up else 0)), fill=(72, 79, 68, 130))
    return frame


def make_strip(draw_frame) -> Image.Image:
    strip = Image.new("RGBA", (FX_CELL_SIZE[0] * FX_FRAMES, FX_CELL_SIZE[1]))
    for frame_index in range(FX_FRAMES):
        strip.alpha_composite(draw_frame(frame_index), (frame_index * FX_CELL_SIZE[0], 0))
    return strip


def write_page() -> None:
    page = """<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><base href=/keeper-review/kitchen-bin-effects-v31/><title>Kitchen V31 · comic-readable bin stench</title><style>
body{margin:auto;max-width:1060px;padding:16px;background:#071722;color:#edf8f5;font:15px/1.4 system-ui}section{background:#102b37;padding:12px;margin:12px 0}.grid{display:flex;gap:12px}.card{flex:1;text-align:center}.sprite{width:288px;height:288px;object-fit:contain;image-rendering:pixelated}.stage{overflow:auto}.room{position:relative;width:772px;height:224px}.room>img:first-child{width:772px;height:224px}.fx{position:absolute;left:4px;top:104px;width:80px;height:80px;overflow:hidden}.fx img{height:80px;max-width:none;image-rendering:pixelated}.zoom{width:320px;height:320px;overflow:hidden;margin:auto}.zoom img{height:320px;max-width:none;image-rendering:pixelated}[data-media]{visibility:hidden}.ready [data-media]{visibility:visible}
</style><main><p>V31 draft · V28 bin unchanged · native game scale</p><h1>Pedal bin · comic-readable stink effect</h1><p>V31 uses three curling green smell trails, loose translucent haze, and three clearly legible slow flies.</p><p id=loading>Loading every review image…</p>
<section><h2>Two states · 4×</h2><div class=grid><div class=card><h3>Standard</h3><img data-media class=sprite src=assets/bin-standard.png alt="Standard bin"></div><div class=card><h3>Broken · overflowing</h3><img data-media class=sprite src=assets/bin-broken-overflowing.png alt="Overflowing bin"></div></div></section>
<section><h2>Broken kitchen · game size</h2><div class=stage><div class=room><img data-media src=assets/kitchen-bin-broken-in-situ.png width=772 height=224 alt="Kitchen"><i class=fx><img data-media data-strip data-frames="40" data-fps="4" src=assets/fx-stench-miasma-f40.png></i><i class=fx><img data-media data-strip data-frames="40" data-fps="4" src=assets/fx-slow-flies-f40.png></i></div></div></section>
<section><h2>Reusable FX · 4×</h2><div class=grid><div class=card><h3>Stink trails and haze</h3><div class=zoom><img data-media data-strip data-frames="40" data-fps="4" src=assets/fx-stench-miasma-f40.png></div><p>40 frames · 4 fps · 10 seconds</p></div><div class=card><h3>Slow flies</h3><div class=zoom><img data-media data-strip data-frames="40" data-fps="4" src=assets/fx-slow-flies-f40.png></div><p>40 frames · 4 fps · 10 seconds</p><button disabled>Play placeholder SFX</button></div></div></section>
<p>V28–V30 remain immutable. V31 changes only the environmental overlays; the bin itself is static.</p></main><script>
const media=[...document.querySelectorAll('[data-media]')],strips=[...document.querySelectorAll('[data-strip]')];Promise.all(media.map(x=>new Promise((ok,no)=>{x.onload=ok;x.onerror=no;if(x.complete)x.decode?.().then(ok,ok)}))).then(()=>{document.body.classList.add('ready');loading.textContent='All state images and reusable effect strips loaded and decoded. Playback unlocked.';document.querySelector('button').disabled=false;let s=performance.now();requestAnimationFrame(function go(t){strips.forEach(x=>x.style.transform=`translateX(${-Math.floor((t-s)*+x.dataset.fps/1000)%+x.dataset.frames*x.parentElement.clientWidth}px)`);requestAnimationFrame(go)})}).catch(()=>loading.textContent='Review locked: media failed to load');document.querySelector('button').onclick=()=>{let C=AudioContext,c=new C,o=c.createOscillator(),g=c.createGain();o.frequency.value=120;g.gain.value=.015;o.connect(g).connect(c.destination);o.start();g.gain.exponentialRampToValueAtTime(.001,c.currentTime+.7);o.stop(c.currentTime+.7)}
</script>"""
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    (PUBLIC_DIR / "index.html").write_text(page)


def main() -> None:
    for name, expected in STATIC_HASHES.items():
        source = V30_RAW / name
        if sha(source) != expected:
            raise RuntimeError(f"Pinned static input changed: {source.relative_to(ROOT)}")
    if sha(V30_RAW / "fx-stench-miasma-f40.png") != V30_MIASMA_SHA:
        raise RuntimeError("Pinned V30 miasma changed")
    if sha(V30_RAW / "fx-slow-flies-f40.png") != V29_FLIES_SHA:
        raise RuntimeError("Pinned V29/V30 fly strip changed")

    for folder in (RAW_DIR, DRAFT_DIR, ASSET_DIR):
        folder.mkdir(parents=True, exist_ok=True)
    for name in STATIC_HASHES:
        copy(V30_RAW / name, RAW_DIR / name)

    outputs = {
        **{name: Image.open(RAW_DIR / name).convert("RGBA") for name in STATIC_HASHES},
        "fx-stench-miasma-f40.png": make_strip(draw_stench_frame),
        "fx-slow-flies-f40.png": make_strip(draw_flies_frame),
    }
    for name, image in outputs.items():
        if name not in STATIC_HASHES:
            image.save(RAW_DIR / name, optimize=True)
        copy(RAW_DIR / name, ASSET_DIR / name)

    catalogue = {
        "version": 31,
        "status": "comic-readable-stench-awaiting-visual-confirmation",
        "states": ["standard", "broken_overflowing"],
        "objectSourceVersion": 28,
        "effectSourceVersions": [29, 30],
        "objectPixelsChanged": False,
        "outputs": {name: {"sha256": sha(RAW_DIR / name), "size": list(image.size)} for name, image in outputs.items()},
        "effects": {
            "stench_miasma": {
                "file": "fx-stench-miasma-f40.png",
                "reusable": True,
                "style": "three-curling-comic-smell-trails-with-loose-translucent-haze",
                "frames": FX_FRAMES,
                "fps": FX_FPS,
                "durationSeconds": FX_FRAMES / FX_FPS,
                "cellPixels": list(FX_CELL_SIZE),
                "roomTopLeft": list(FX_ROOM_TOP_LEFT),
                "objectPixelsChanged": False,
                "previousSha256": V30_MIASMA_SHA,
            },
            "slow_flies": {
                "file": "fx-slow-flies-f40.png",
                "reusable": True,
                "style": "three-legible-slow-uneven-orbits",
                "frames": FX_FRAMES,
                "fps": FX_FPS,
                "durationSeconds": FX_FRAMES / FX_FPS,
                "cellPixels": list(FX_CELL_SIZE),
                "roomTopLeft": list(FX_ROOM_TOP_LEFT),
                "objectPixelsChanged": False,
                "previousSha256": V29_FLIES_SHA,
                "sfxCue": "kitchen_bin_flies_slow_loop",
            },
        },
        "boundaries": {
            "approved": False,
            "promoted": False,
            "v28ObjectPixelsPreserved": True,
            "objectAnimated": False,
            "environmentalFxAnimated": True,
            "runtimeChanged": False,
            "canonicalChanged": False,
            "v20ThroughV30Changed": False,
        },
    }
    (DRAFT_DIR / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT_DIR / "batch-register.json").write_text(json.dumps({
        "version": 31,
        "preserves": list(range(20, 31)),
        "v30Disposition": "retained as immutable high-cloud provenance; replaced by clearer wordless comic stink grammar",
        "rollback": "Delete only V31 raw/draft/review/archive/builder/verifier/docs files; V20-V30 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC_DIR.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    if "--page-only" in sys.argv:
        write_page()
    else:
        if Image is None:
            raise RuntimeError("Pillow is required for the full V31 asset build")
        main()
