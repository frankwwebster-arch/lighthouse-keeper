#!/usr/bin/env python3
"""Build Kitchen V29: approved V28 bin pixels with quieter 10-second FX."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
V28_RAW = ROOT / "art/raw/kitchen-bin-states-2026-10-18-v28"
RAW_DIR = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v29"
DRAFT_DIR = ROOT / "art/drafts/kitchen-bin-effects-2026-10-18-v29"
PUBLIC_DIR = ROOT / "public/keeper-review/kitchen-bin-effects-v29"
ASSET_DIR = PUBLIC_DIR / "assets"

STATIC_HASHES = {
    "bin-standard.png": "86b05224a7da5fc5c05918f2875018920ed54cf46fc00cb08952ffd29789f9c0",
    "bin-broken-overflowing.png": "77ad87fabfd3e5c10a4a14f294af343a5d93a2a2015e6d77f18a4140b1f5fb4f",
    "kitchen-bin-standard-in-situ.png": "027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674",
    "kitchen-bin-broken-in-situ.png": "bf1c741f9ff7e985ddc44584c9c13c76c60e0df8104d34a2a11848f1be58a1c3",
}

FX_CELL_SIZE = (80, 80)
FX_FRAMES = 40
FX_FPS = 4
FX_ROOM_TOP_LEFT = (4, 104)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def periodic(frame: int, phase: float = 0.0) -> float:
    return math.sin(math.tau * frame / FX_FRAMES + phase)


def paint_wisp(
    frame: Image.Image,
    points: list[tuple[int, int]],
    widths: list[int],
    colour: tuple[int, int, int, int],
    highlight: tuple[int, int, int, int],
    seed: int,
) -> None:
    """Paint a tapered, angular vapour ribbon without rounded cloud stamps."""
    draw = ImageDraw.Draw(frame)
    left = [(x - width, y) for (x, y), width in zip(points, widths)]
    right = [(points[index][0] + widths[index], points[index][1]) for index in range(len(points) - 1, -1, -1)]
    polygon = left + right
    draw.polygon(polygon, fill=colour)

    # A narrow muted inner trace gives depth, while deliberate transparent
    # pinholes make the silhouette read as diffuse vapour rather than a blob.
    inner = points[1:-1]
    if len(inner) >= 2:
        draw.line(inner, fill=highlight, width=1)
    for index, (x, y) in enumerate(points[2:-1], 2):
        if (index + seed) % 3 == 0:
            draw.point((x + (1 if index % 2 else -1), y), fill=(0, 0, 0, 0))


def draw_stench_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    origin_x, origin_y = 40, 69

    # A constant, narrow emission throat pins every frame to the bin opening.
    # Its sway changes by only a pixel at a time over the full ten seconds.
    sway = round(2 * periodic(frame_index, 0.2))
    throat = [
        (origin_x - 1, origin_y),
        (origin_x, 65),
        (origin_x + sway // 2, 61),
        (origin_x + sway, 57),
    ]
    draw.line(throat, fill=(58, 100, 45, 122), width=2)
    draw.point((origin_x + 1, origin_y), fill=(104, 148, 75, 90))

    # Three thin, irregular ribbons share the source but rise at different
    # phases. Their low contrast and broken edges replace V28's round puffs.
    ribbons = (
        (-0.45, -5, (50, 96, 43, 102), (108, 148, 77, 58)),
        (1.65, 1, (58, 106, 48, 88), (118, 158, 86, 50)),
        (3.75, 6, (46, 87, 39, 76), (101, 141, 72, 44)),
    )
    for seed, (phase, lateral, colour, highlight) in enumerate(ribbons):
        slow = math.tau * frame_index / FX_FRAMES + phase
        x0 = origin_x + lateral + round(1.5 * math.sin(slow))
        points = [
            (origin_x + round(lateral * 0.2), 59),
            (x0 - 1, 54),
            (x0 + round(2 * math.sin(slow + 0.7)), 49),
            (x0 + round(3 * math.sin(slow + 1.4)), 44),
            (x0 + round(4 * math.sin(slow + 2.1)), 39),
            (x0 + round(5 * math.sin(slow + 2.8)), 34),
        ]
        widths = [1, 2, 3, 3, 2, 1]
        paint_wisp(frame, points, widths, colour, highlight, seed)

    # Sparse detached traces dissipate above the main ribbons. They remain
    # subdued and change on a five-frame cadence, reinforcing the slow pace.
    drift_step = frame_index // 5
    for index in range(4):
        angle = math.tau * (drift_step + index * 3) / 8
        x = 40 + round(math.cos(angle) * (9 + index * 2))
        y = 29 - index * 3 + round(math.sin(angle) * 2)
        draw.point((x, y), fill=(65, 110, 51, 48 - index * 7))
        if index < 2:
            draw.point((x + 1, y), fill=(105, 146, 72, 34))
    return frame


def draw_flies_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    # Three flies take the entire ten-second loop to circle the refuse. Their
    # paths are shallow and irregular; muted one-pixel wings avoid sparkle.
    flies = (
        (0.00, 10, 5, 0),
        (2.25, 15, 7, 7),
        (4.50, 8, 4, 14),
    )
    for phase, radius_x, radius_y, wing_phase in flies:
        angle = math.tau * frame_index / FX_FRAMES + phase
        wobble = round(math.sin(angle * 2 + phase))
        x = round(40 + math.cos(angle) * radius_x)
        y = round(54 + math.sin(angle) * radius_y) + wobble
        draw.point((x, y), fill=(23, 26, 22, 238))
        draw.point((x + 1, y), fill=(15, 19, 18, 220))
        wing_up = ((frame_index + wing_phase) // 3) % 2 == 0
        wing_y = y - 1 if wing_up else y + 1
        wing = (137, 145, 123, 135)
        draw.point((x - 1, wing_y), fill=wing)
        draw.point((x + 2, wing_y), fill=wing)
    return frame


def make_strip(draw_frame) -> Image.Image:
    strip = Image.new("RGBA", (FX_CELL_SIZE[0] * FX_FRAMES, FX_CELL_SIZE[1]))
    for frame_index in range(FX_FRAMES):
        strip.alpha_composite(draw_frame(frame_index), (frame_index * FX_CELL_SIZE[0], 0))
    return strip


def write_page() -> None:
    prefix = "/keeper-review/kitchen-bin-effects-v29/assets"
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V29 · quieter bin effects</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1120px;margin:auto;padding:22px}}h1,h2{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin:0 6px 6px 0;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.stage{{overflow:auto;background:#02080b;border-radius:9px;padding:16px}}.states{{display:grid;grid-template-columns:repeat(2,minmax(260px,1fr));gap:16px}}.state{{text-align:center;background:#091e29;border:1px solid #315768;border-radius:11px;padding:14px}}.sprite{{width:288px;height:288px;object-fit:contain;image-rendering:pixelated;margin:auto}}.room-wrap{{position:relative;width:772px;height:224px;overflow:hidden}}.room{{position:absolute;inset:0;width:772px;height:224px;max-width:none}}.room-fx{{position:absolute;left:4px;top:104px;width:80px;height:80px;overflow:hidden}}.room-fx img{{height:80px;max-width:none;image-rendering:pixelated}}.fx-preview{{width:320px;height:320px;overflow:hidden;margin:auto;background:#09151a}}.fx-preview img{{height:320px;max-width:none;image-rendering:pixelated}}button{{background:#147d78;color:white;border:0;border-radius:6px;padding:8px 10px;cursor:pointer}}button:disabled{{opacity:.45;cursor:wait}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}@media(max-width:680px){{.states{{grid-template-columns:1fr}}}}
</style></head><body><main><span class="tag">V29 draft</span><span class="tag">V28 bin unchanged</span><span class="tag">10-second reusable FX</span><span class="tag">Native game scale</span><h1>Pedal bin · quieter environmental loop</h1><p class="note">The excellent V28 standard and overflowing bin pixels are preserved exactly. Only the two reusable environmental overlays are revised: the greenish miasma is thinner, more diffuse and irregular, the flies are subdued, and both now take ten seconds to repeat at 4 fps. The bin itself remains static.</p><p id="loading">Loading and decoding every review image and effect strip…</p>
<section><h2>Approved object drawings · 4× inspection</h2><div class="states"><article class="state"><h3>Standard</h3><img data-media class="sprite" src="{prefix}/bin-standard.png" width="72" height="72" alt="Standard turquoise pedal bin"></article><article class="state"><h3>Broken · overflowing</h3><img data-media class="sprite" src="{prefix}/bin-broken-overflowing.png" width="72" height="72" alt="Overflowing turquoise pedal bin with raised lid and fallen rubbish"></article></div></section>
<section><h2>Standard in the complete kitchen · actual game size</h2><div class="stage"><div class="room-wrap"><img data-media class="room" src="{prefix}/kitchen-bin-standard-in-situ.png" width="772" height="224" alt="Standard bin in the complete kitchen at game scale"></div></div></section>
<section><h2>Broken plus quieter environmental fault · actual game size</h2><div class="stage"><div class="room-wrap"><img data-media class="room" src="{prefix}/kitchen-bin-broken-in-situ.png" width="772" height="224" alt="Overflowing bin and floor spill in the complete kitchen at game scale"><div class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="{prefix}/fx-stench-miasma-f40.png" width="3200" height="80" alt="Subtle reusable greenish miasma effect"></div><div class="room-fx"><img data-media data-strip data-frames="40" data-fps="4" src="{prefix}/fx-slow-flies-f40.png" width="3200" height="80" alt="Subdued slowly buzzing flies effect"></div></div></div><p>The static object and floor spill are exactly V28. Both separate environmental layers are anchored at the opening and complete one continuous loop in ten seconds.</p></section>
<section><h2>Reusable environmental layers · 4× inspection</h2><div class="states"><article class="state"><h3>Diffuse greenish miasma</h3><div class="fx-preview"><img data-media data-strip data-frames="40" data-fps="4" src="{prefix}/fx-stench-miasma-f40.png" width="12800" height="320" alt="Reusable subtle greenish miasma loop"></div><p>40 frames · 4 fps · 10 seconds</p></article><article class="state"><h3>Slow, subdued flies</h3><div class="fx-preview"><img data-media data-strip data-frames="40" data-fps="4" src="{prefix}/fx-slow-flies-f40.png" width="12800" height="320" alt="Reusable slow fly loop"></div><p>40 frames · 4 fps · 10 seconds</p><button data-sfx="kitchen_bin_flies_slow_loop">Play placeholder SFX</button></article></div></section>
<p class="warn"><strong>Version boundary:</strong> V28 remains immutable. V29 changes only the reusable effect strips and their timing. No runtime manifest, Final art, approved V23 cabinet run, chair placement or Prime source is changed.</p>
</main><script>const media=[...document.querySelectorAll('[data-media]')],strips=[...document.querySelectorAll('[data-strip]')];Promise.all(media.map(el=>new Promise((ok,bad)=>{{if(el.complete){{el.decode?.().then(ok).catch(ok);return}}el.onload=()=>el.decode?.().then(ok).catch(ok)??ok();el.onerror=()=>bad(new Error('Could not load '+el.src))}}))).then(()=>{{document.body.classList.add('ready');document.querySelector('#loading').textContent='All state images and reusable effect strips loaded and decoded. Playback unlocked.';document.querySelectorAll('button').forEach(button=>button.disabled=false);const start=performance.now();function tick(now){{for(const image of strips){{const frame=Math.floor((now-start)*(+image.dataset.fps)/1000)%(+image.dataset.frames);image.style.transform=`translateX(${{-frame*image.parentElement.clientWidth}}px)`}}requestAnimationFrame(tick)}}requestAnimationFrame(tick)}}).catch(error=>document.querySelector('#loading').textContent='Review locked: '+error.message);document.querySelectorAll('button').forEach(button=>{{button.disabled=true;button.onclick=()=>{{const C=window.AudioContext||window.webkitAudioContext,c=new C,o=c.createOscillator(),g=c.createGain();o.type='sawtooth';o.frequency.setValueAtTime(114,c.currentTime);o.frequency.linearRampToValueAtTime(126,c.currentTime+.65);g.gain.setValueAtTime(.018,c.currentTime);g.gain.exponentialRampToValueAtTime(.001,c.currentTime+.7);o.connect(g).connect(c.destination);o.start();o.stop(c.currentTime+.7)}}}})</script></body></html>'''
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    (PUBLIC_DIR / "index.html").write_text(html)


def main() -> None:
    for name, expected in STATIC_HASHES.items():
        source = V28_RAW / name
        if sha(source) != expected:
            raise RuntimeError(f"Pinned V28 input changed: {source.relative_to(ROOT)}")

    for folder in (RAW_DIR, DRAFT_DIR, ASSET_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    for name in STATIC_HASHES:
        copy(V28_RAW / name, RAW_DIR / name)

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
        "version": 29,
        "status": "approved-v28-bin-with-quieter-ten-second-effects-awaiting-visual-confirmation",
        "states": ["standard", "broken_overflowing"],
        "objectSourceVersion": 28,
        "objectPixelsChanged": False,
        "outputs": {name: {"sha256": sha(RAW_DIR / name), "size": list(image.size)} for name, image in outputs.items()},
        "effects": {
            "stench_miasma": {
                "file": "fx-stench-miasma-f40.png",
                "reusable": True,
                "style": "diffuse-irregular-low-contrast-greenish-vapour",
                "frames": FX_FRAMES,
                "fps": FX_FPS,
                "durationSeconds": FX_FRAMES / FX_FPS,
                "cellPixels": list(FX_CELL_SIZE),
                "roomTopLeft": list(FX_ROOM_TOP_LEFT),
                "objectPixelsChanged": False,
            },
            "slow_flies": {
                "file": "fx-slow-flies-f40.png",
                "reusable": True,
                "style": "subdued-slow-shallow-orbits",
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
            "v28ObjectPixelsPreserved": True,
            "objectAnimated": False,
            "environmentalFxAnimated": True,
            "runtimeChanged": False,
            "canonicalChanged": False,
            "v20ThroughV28Changed": False,
        },
    }
    (DRAFT_DIR / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT_DIR / "batch-register.json").write_text(json.dumps({
        "version": 29,
        "preserves": list(range(20, 29)),
        "v28Disposition": "approved-bin-pixels-retained-byte-for-byte; environmental-effects-superseded-only",
        "rollback": "Delete only V29 raw/draft/review/archive/builder/verifier/docs files; V20-V28 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC_DIR.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
