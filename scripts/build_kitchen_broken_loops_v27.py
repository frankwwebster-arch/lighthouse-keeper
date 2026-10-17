#!/usr/bin/env python3
"""Build reversible Kitchen V27 broken-state animation drafts and review page."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-broken-loops-2026-10-18-v27"
GENERATED = SOURCE / "generated"
RAW = ROOT / "art/raw/kitchen-broken-loops-2026-10-18-v27"
DRAFT = ROOT / "art/drafts/kitchen-broken-loops-2026-10-18-v27"
PUBLIC = ROOT / "public/keeper-review/kitchen-broken-loops-v27"
ASSETS = PUBLIC / "assets"
ROOM_SOURCE = ROOT / "art/raw/kitchen-narrower-bin-2026-10-17-v25/full-kitchen-narrower-bin.png"
PRIME_BACK = ROOT / "art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-back_f01.png"
TV_SMOKE = ROOT / "art/raw/floor-asset-catalogue/fx_broken_smoke_f8.png"
TV_SPARKS = ROOT / "art/raw/floor-asset-catalogue/fx_broken_sparks_f6.png"

ROOM_SHA = "175d77c063297c435eab468f297c369f79e5491b89bbdd2b03400d31cd334f4a"
PRIME_BACK_SHA = "28a879bcee43c6d06330d05fb3cd74b4098b2ccce38ce41d15117f5fb0be5167"
ROOM_CROP = (0, 45, 2064, 643)
ROOM_SIZE = (772, 224)
FRAMES = 8
FPS = 8

NAVY = (4, 20, 48, 255)
CHARCOAL = (25, 30, 39, 235)
SMOKE = (54, 57, 63, 225)
PALE = (239, 247, 232, 235)
STEAM = (198, 232, 228, 215)
ORANGE = (255, 111, 9, 255)
YELLOW = (255, 220, 50, 255)
RED = (212, 43, 19, 255)
CYAN = (55, 210, 229, 255)
BLUE = (17, 119, 187, 245)
OLIVE = (122, 139, 52, 235)


SPECS = {
    "bin": {"cell": (80, 120), "fit": (44, 78), "source": "bin-broken-source.png", "logical": (20, 30)},
    "fridge": {"cell": (128, 160), "fit": (84, 120), "source": "fridge-broken-source.png", "logical": (32, 40)},
    "kettle": {"cell": (112, 160), "fit": (84, 120), "source": "kettle-broken-source.png", "logical": (28, 40)},
    "toaster": {"cell": (112, 160), "fit": (84, 120), "source": "toaster-broken-source.png", "logical": (28, 40)},
    "oven": {"cell": (144, 160), "fit": (108, 120), "source": "oven-broken-source.png", "logical": (36, 40)},
    "bowl": {"cell": (112, 160), "fit": (84, 120), "source": "bowl-broken-source.png", "logical": (28, 40)},
    "sink": {"cell": (112, 160), "fit": (84, 120), "source": "sink-broken-source.png", "logical": (28, 40)},
    "table": {"cell": (128, 112), "fit": (80, 58), "source": "table-broken-source.png", "logical": (32, 28)},
}

SFX = {
    "bin": [{"frame": 0, "cue": "kitchen_bin_flies_loop"}],
    "fridge": [{"frame": 0, "cue": "kitchen_fridge_electrical_buzz_loop"}, {"frame": 2, "cue": "kitchen_fridge_crackle"}, {"frame": 6, "cue": "kitchen_fridge_drip"}],
    "kettle": [{"frame": 0, "cue": "kitchen_kettle_whistle_loop"}, {"frame": 2, "cue": "kitchen_kettle_rattle"}, {"frame": 6, "cue": "kitchen_kettle_rattle"}],
    "toaster": [{"frame": 0, "cue": "kitchen_toaster_fire_loop"}, {"frame": 4, "cue": "kitchen_toaster_crackle"}],
    "oven": [{"frame": 0, "cue": "kitchen_oven_smoulder_loop"}, {"frame": 3, "cue": "kitchen_oven_hob_flare"}, {"frame": 7, "cue": "kitchen_oven_hob_flare"}],
    "bowl": [{"frame": 4, "cue": "kitchen_bowl_ceramic_tinkle"}],
    "sink": [{"frame": 0, "cue": "kitchen_sink_water_jet_loop"}, {"frame": 4, "cue": "kitchen_sink_pipe_rattle"}],
    "table": [{"frame": 0, "cue": "kitchen_table_creak"}, {"frame": 4, "cue": "kitchen_table_creak"}],
}

LABELS = {"bin": "Bin", "fridge": "Fridge", "kettle": "Kettle", "toaster": "Toaster", "oven": "Oven", "bowl": "Mixing bowl", "sink": "Basin", "table": "Table"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, name: str) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    image.save(RAW / name, optimize=True)
    shutil.copyfile(RAW / name, ASSETS / name)


def fit_generated(path: Path, cell: tuple[int, int], target: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        rgba = source.convert("RGBA")
    bbox = rgba.getbbox()
    if not bbox:
        raise RuntimeError(f"Empty generated source: {path}")
    cropped = rgba.crop(bbox)
    scale = min(target[0] / cropped.width, target[1] / cropped.height)
    size = (max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale)))
    reduced = cropped.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", cell)
    canvas.alpha_composite(reduced, ((cell[0] - size[0]) // 2, cell[1] - 8 - size[1]))
    return canvas


def strip(frames: list[Image.Image]) -> Image.Image:
    out = Image.new("RGBA", (frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        out.alpha_composite(frame, (index * frame.width, 0))
    return out


def cloud_frame(index: int, *, dark: bool) -> Image.Image:
    """Reuse the approved TV smoke silhouette; only palette changes for steam."""
    with Image.open(TV_SMOKE) as source:
        frame = source.convert("RGBA").crop((index * 48, 0, index * 48 + 48, 64))
    if dark:
        return frame
    pixels = frame.load()
    for y in range(frame.height):
        for x in range(frame.width):
            r, g, b, a = pixels[x, y]
            if a:
                light = (r + g + b) // 3
                mix = min(255, 145 + light // 2)
                pixels[x, y] = (min(255, mix + 22), min(255, mix + 35), min(255, mix + 32), a)
    return frame


def flame_frame(index: int, size: tuple[int, int] = (48, 64)) -> Image.Image:
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    lean = (-2, -1, 1, 2, 1, 0, -1, -2)[index]
    top = (12, 8, 11, 5, 9, 6, 10, 7)[index]
    draw.polygon([(10, 58), (8, 42), (15, 31), (17 + lean, top), (27, 26), (34 + lean, 14), (38, 42), (35, 58)], fill=NAVY)
    draw.polygon([(14, 55), (13, 42), (20 + lean, 20), (25, 36), (32 + lean, 23), (34, 45), (31, 55)], fill=RED)
    draw.polygon([(18, 54), (18, 43), (24 + lean, 30), (29, 44), (28, 54)], fill=ORANGE)
    draw.rectangle((22, 46, 27, 53), fill=YELLOW)
    return image


def smell_frame(index: int) -> Image.Image:
    image = Image.new("RGBA", (64, 80))
    draw = ImageDraw.Draw(image)
    shift = (-2, 0, 2, 1, -1, -2, 0, 2)[index]
    for x, phase in ((19, 0), (34, 2), (47, 4)):
        points = []
        for step in range(6):
            points.append((x + shift + (3 if (step + index + phase) % 2 else -2), 68 - step * 10))
        draw.line(points, fill=NAVY, width=5)
        draw.line(points, fill=OLIVE, width=2)
    flies = [((11, 18), (2, -1)), ((52, 27), (-2, 1)), ((41, 9), (1, 2))]
    for (x, y), (dx, dy) in flies:
        x += dx * ((index % 3) - 1); y += dy * (((index + 1) % 3) - 1)
        draw.rectangle((x - 2, y - 2, x + 2, y + 2), fill=NAVY)
        draw.point((x - 4, y - 3), fill=PALE); draw.point((x + 4, y - 3), fill=PALE)
    return image


def water_frame(index: int) -> Image.Image:
    image = Image.new("RGBA", (48, 96))
    draw = ImageDraw.Draw(image)
    sway = (-2, -1, 0, 2, 1, 0, -1, -2)[index]
    points = [(24, 88), (19 + sway, 72), (26 + sway, 57), (20 - sway, 39), (24 + sway, 18), (22, 7)]
    draw.line(points, fill=NAVY, width=9)
    draw.line(points, fill=CYAN, width=5)
    draw.line([(p[0] - 1, p[1]) for p in points], fill=(190, 249, 244, 255), width=2)
    for x, y in ((8 + index % 4, 34), (39 - index % 5, 50), (12 + index % 3, 72)):
        draw.rectangle((x, y, x + 3, y + 5), fill=CYAN)
    return image


def spark_frame(index: int) -> Image.Image:
    source_index = (0, 1, 2, 3, 4, 5, 4, 2)[index]
    with Image.open(TV_SPARKS) as source:
        return source.convert("RGBA").crop((source_index * 48, 0, source_index * 48 + 48, 48))


def add_puddle(frame: Image.Image, index: int, at: tuple[int, int]) -> None:
    draw = ImageDraw.Draw(frame)
    x, y = at
    width = (18, 20, 22, 24, 23, 21, 19, 18)[index]
    draw.rectangle((x - width // 2, y, x + width // 2, y + 4), fill=NAVY)
    draw.rectangle((x - width // 2 + 3, y + 1, x + width // 2 - 2, y + 2), fill=BLUE)
    if index in (2, 6):
        draw.rectangle((x - 2, y - 9, x + 2, y - 4), fill=CYAN)


def compose_objects(bases: dict[str, Image.Image], effects: dict[str, list[Image.Image]]) -> dict[str, list[Image.Image]]:
    clips: dict[str, list[Image.Image]] = {}
    for name, base in bases.items():
        frames = []
        for i in range(FRAMES):
            frame = Image.new("RGBA", base.size)
            dx = 0
            dy = 0
            if name == "kettle":
                dx = (-1, 1, 0, -1, 1, 0, -1, 1)[i]
                dy = (0, -1, 0, 0, -1, 0, 0, -1)[i]
            elif name == "table":
                dx = (0, 0, 1, 1, 0, -1, -1, 0)[i]
                dy = (0, 1, 1, 0, 0, 1, 1, 0)[i]
            frame.alpha_composite(base, (dx, dy))
            if name == "bin":
                frame.alpha_composite(effects["smell"][i], (8, 0))
            elif name == "fridge":
                frame.alpha_composite(effects["smoke_light"][i], (5, 0))
                frame.alpha_composite(effects["sparks"][i], (63, 35))
                add_puddle(frame, i, (33, 148))
            elif name == "kettle":
                frame.alpha_composite(effects["steam"][i], (14, 0))
                frame.alpha_composite(effects["steam"][(i + 3) % FRAMES], (49, 5))
            elif name == "toaster":
                flame = effects["flame"][i].resize((32, 43), Image.Resampling.NEAREST)
                frame.alpha_composite(flame, (40, 10))
            elif name == "oven":
                frame.alpha_composite(effects["smoke_black"][i], (38, 0))
                frame.alpha_composite(effects["smoke_black"][(i + 3) % FRAMES], (72, 5))
                small = effects["flame"][i].resize((30, 40), Image.Resampling.NEAREST)
                frame.alpha_composite(small, (48, 9))
                frame.alpha_composite(effects["flame"][(i + 3) % FRAMES].resize((30, 40), Image.Resampling.NEAREST), (76, 9))
            elif name == "bowl":
                draw = ImageDraw.Draw(frame)
                if i in (2, 6):
                    draw.line([(79, 75), (84, 70)], fill=PALE, width=2)
                    draw.line([(82, 67), (87, 62)], fill=YELLOW, width=2)
            elif name == "sink":
                frame.alpha_composite(effects["water"][i], (32, 0))
                add_puddle(frame, i, (63, 148))
            frames.append(frame)
        clips[name] = frames
    return clips


def chair_foreground(room: Image.Image) -> Image.Image:
    layer = Image.new("RGBA", room.size)
    pix = room.load(); out = layer.load()
    for y in range(114, 186):
        for x in range(700, 740):
            r, g, b, a = pix[x, y]
            in_shape = (x <= 711 or x >= 729 or 121 <= y <= 136 or 141 <= y <= 153 or 158 <= y <= 170)
            blue = b > 55 and b > r * 1.12 and b > g * 0.72
            navy = r < 48 and g < 76 and b < 138
            orange = r > 95 and r > g * 1.25 and g > b * 1.05
            cream_seat = 708 <= x <= 733 and 170 <= y <= 185 and r > 145 and g > 135 and b > 115
            if a and ((in_shape and (blue or navy or orange)) or cream_seat):
                out[x, y] = pix[x, y]
    return layer


def build_room_and_chair(clips: dict[str, list[Image.Image]]) -> tuple[list[Image.Image], Image.Image, Image.Image]:
    with Image.open(ROOM_SOURCE) as source:
        room = source.convert("RGBA").crop(ROOM_CROP).resize(ROOM_SIZE, Image.Resampling.LANCZOS)
    with Image.open(PRIME_BACK) as source:
        prime = source.convert("RGBA").resize((128, 160), Image.Resampling.LANCZOS)
    corrected = room.copy()
    corrected.alpha_composite(prime, (655, 64))
    corrected.alpha_composite(chair_foreground(room))

    centres = {"bin": 43, "fridge": 126, "kettle": 210, "toaster": 294, "oven": 378, "bowl": 462, "sink": 546, "table": 718}
    room_frames = []
    for i in range(FRAMES):
        frame = room.copy()
        for name, centre in centres.items():
            sprite = clips[name][i]
            x = centre - sprite.width // 2
            y = 218 - (sprite.height - 8)
            frame.alpha_composite(sprite, (x, y))
        room_frames.append(frame)
    return room_frames, room, corrected


def write_page(catalogue: dict) -> None:
    prefix = "/keeper-review/kitchen-broken-loops-v27/assets"
    cards = []
    for name, spec in SPECS.items():
        cards.append(f'''<article><h3>{LABELS[name]}</h3><div class="sprite" style="--w:{spec['cell'][0]}px;--h:{spec['cell'][1]}px"><img data-media data-strip data-frames="8" data-fps="8" src="{prefix}/{name}-broken-cycle-f8.png" width="{spec['cell'][0] * 8}" height="{spec['cell'][1]}" alt="Animated broken {LABELS[name].lower()}"></div><p>{', '.join(c['cue'] for c in SFX[name])}</p><button data-sfx="{SFX[name][0]['cue']}">Play placeholder SFX</button></article>''')
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V27 · broken loops</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1500px;margin:auto;padding:22px}}h1,h2,h3{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.stage{{overflow:auto;background:#02080b;border-radius:9px;padding:16px}}.room{{position:relative;width:772px;height:224px;overflow:hidden}}.room img{{height:224px;max-width:none}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}}article{{background:#091e29;border:1px solid #315768;border-radius:11px;padding:12px}}.sprite{{width:var(--w);height:var(--h);overflow:hidden;margin:0 auto 10px;background:#02080b}}.sprite img{{height:var(--h);max-width:none;image-rendering:pixelated}}button{{background:#147d78;color:white;border:0;border-radius:6px;padding:8px 10px;cursor:pointer}}button:disabled{{opacity:.45;cursor:wait}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}code{{color:#9af1e9}}
</style></head><body><main><span class="tag">V27 draft</span><span class="tag">8 fps loops</span><span class="tag">Reusable FX</span><h1>Kitchen broken-state animation set</h1><p class="note">Eight isolated repair states, shown at native density-4 game scale. Structural damage and effects are separate in the catalogue; every loop has named SFX cues which currently play a deterministic review placeholder.</p><p id="loading">Loading and decoding every animation strip…</p>
<section><h2>All broken items in situ</h2><div class="stage"><div class="room"><img data-media data-strip data-frames="8" data-fps="8" src="{prefix}/kitchen-broken-full-room-cycle-f8.png" width="6176" height="224" alt="Complete kitchen with all eight broken assets animated in situ"></div></div><p>The oven includes animated flames on both hob burners in addition to black smoke. The bin remains the approved narrower V25 width.</p></section>
<section><h2>Individual repair loops</h2><div class="grid">{''.join(cards)}</div></section>
<section><h2>Corrected chair / Keeper registration</h2><div class="stage"><img data-media src="{prefix}/kitchen-prime-seated-chair-corrected.png" width="772" height="224" alt="Prime Keeper seated with the chair back visibly behind and supporting his back"></div><p>The chair-back posts, rails and seat foreground are restored over the Keeper’s lower back. The table stays behind both.</p></section>
<section><h2>Reusable effect library</h2><div class="grid">{''.join(f'<article><h3>{name.replace("_", " ").title()}</h3><div class="sprite" style="--w:{frames[0].width}px;--h:{frames[0].height}px"><img data-media data-strip data-frames="8" data-fps="8" src="{prefix}/fx-{name.replace("_", "-")}-cycle-f8.png" width="{frames[0].width*8}" height="{frames[0].height}" alt="Reusable {name} effect"></div></article>' for name, frames in catalogue['_effectFrames'].items())}</div></section>
<p class="warn"><strong>Version boundary:</strong> V20–V26 remain unchanged. V27 is a reversible draft asset set; the original generated sources, rejected snapped-leg source, hashes, effect placements and loop metadata are retained.</p>
</main><script>
const strips=[...document.querySelectorAll('[data-strip]')];const media=[...document.querySelectorAll('[data-media]')];Promise.all(media.map(el=>new Promise((ok,bad)=>{{if(el.complete){{el.decode?.().then(ok).catch(ok);return}}el.onload=()=>el.decode?.().then(ok).catch(ok)??ok();el.onerror=()=>bad(new Error('Could not load '+el.src))}}))).then(()=>{{document.body.classList.add('ready');document.querySelector('#loading').textContent='All animation strips loaded and decoded. Playback unlocked.';document.querySelectorAll('button').forEach(b=>b.disabled=false);let start=performance.now();function tick(now){{strips.forEach(el=>{{const frames=+el.dataset.frames,fps=+el.dataset.fps,w=el.parentElement.clientWidth,frame=Math.floor((now-start)*fps/1000)%frames;el.style.transform=`translateX(${{-frame*w}}px)`}});requestAnimationFrame(tick)}}requestAnimationFrame(tick)}}).catch(error=>document.querySelector('#loading').textContent='Review locked: '+error.message);
document.querySelectorAll('button').forEach(button=>{{button.disabled=true;button.onclick=()=>{{const C=window.AudioContext||window.webkitAudioContext,c=new C,o=c.createOscillator(),g=c.createGain(),seed=[...button.dataset.sfx].reduce((a,v)=>a+v.charCodeAt(0),0);o.type=seed%2?'square':'sawtooth';o.frequency.setValueAtTime(140+seed%320,c.currentTime);o.frequency.exponentialRampToValueAtTime(70+seed%90,c.currentTime+.18);g.gain.setValueAtTime(.045,c.currentTime);g.gain.exponentialRampToValueAtTime(.001,c.currentTime+.2);o.connect(g).connect(c.destination);o.start();o.stop(c.currentTime+.21)}}}});
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    if sha(ROOM_SOURCE) != ROOM_SHA or sha(PRIME_BACK) != PRIME_BACK_SHA:
        raise RuntimeError("Pinned V25 room or Prime seated-back source changed")
    for spec in SPECS.values():
        if not (GENERATED / spec["source"]).exists():
            raise RuntimeError(f"Missing generated source {spec['source']}")

    bases = {name: fit_generated(GENERATED / spec["source"], spec["cell"], spec["fit"]) for name, spec in SPECS.items()}
    effects = {
        "smell": [smell_frame(i) for i in range(FRAMES)],
        "smoke_black": [cloud_frame(i, dark=True) for i in range(FRAMES)],
        "smoke_light": [cloud_frame(i, dark=True) for i in range(FRAMES)],
        "steam": [cloud_frame(i, dark=False) for i in range(FRAMES)],
        "flame": [flame_frame(i) for i in range(FRAMES)],
        "water": [water_frame(i) for i in range(FRAMES)],
        "sparks": [spark_frame(i) for i in range(FRAMES)],
    }
    clips = compose_objects(bases, effects)
    room_frames, room, corrected = build_room_and_chair(clips)

    outputs: dict[str, dict] = {}
    for name, frames in clips.items():
        filename = f"{name}-broken-cycle-f8.png"
        save(strip(frames), filename)
        spec = SPECS[name]
        outputs[name] = {"file": filename, "sha256": sha(RAW / filename), "w": spec["cell"][0] // 4, "h": spec["cell"][1] // 4, "frames": FRAMES, "fps": FPS, "density": 4, "anchor": [spec["cell"][0] // 8, spec["cell"][1] // 4 - 2], "loop": True, "sfxCues": SFX[name]}
    effect_outputs = {}
    for name, frames in effects.items():
        filename = f"fx-{name.replace('_', '-')}-cycle-f8.png"
        save(strip(frames), filename)
        effect_outputs[name] = {"file": filename, "sha256": sha(RAW / filename), "w": frames[0].width // 4, "h": frames[0].height // 4, "frames": FRAMES, "fps": FPS, "density": 4, "anchor": [frames[0].width // 8, frames[0].height // 4 - 1], "loop": True, "reusable": True}
    save(strip(room_frames), "kitchen-broken-full-room-cycle-f8.png")
    save(corrected, "kitchen-prime-seated-chair-corrected.png")
    save(room, "kitchen-game-scale-room-v25.png")

    DRAFT.mkdir(parents=True, exist_ok=True)
    source_hashes = {p.name: sha(p) for p in sorted(GENERATED.glob("*.png"))}
    catalogue = {
        "version": 27,
        "status": "broken-state-loop-draft-awaiting-visual-confirmation",
        "densityPxPerLp": 4,
        "frames": FRAMES,
        "fps": FPS,
        "base": {"version": 25, "roomSha256": ROOM_SHA, "changed": False},
        "chairCorrection": {"primeSourceSha256": PRIME_BACK_SHA, "chairBackForegroundRestored": True, "tableRemainsBehind": True},
        "sources": source_hashes,
        "reusedEffectSources": {"smoke": {"file": str(TV_SMOKE.relative_to(ROOT)), "sha256": sha(TV_SMOKE)}, "sparks": {"file": str(TV_SPARKS.relative_to(ROOT)), "sha256": sha(TV_SPARKS)}},
        "clips": outputs,
        "effects": effect_outputs,
        "effectPlacements": {
            "bin": ["smell"], "fridge": ["smoke_light", "sparks", "water_leak"], "kettle": ["steam", "vibration"], "toaster": ["flame"], "oven": ["smoke_black", "flame:left_hob", "flame:right_hob"], "bowl": ["ceramic_glint"], "sink": ["water", "water_leak"], "table": ["wobble"]
        },
        "roomLoop": {"file": "kitchen-broken-full-room-cycle-f8.png", "sha256": sha(RAW / "kitchen-broken-full-room-cycle-f8.png"), "w": 193, "h": 56, "frames": 8, "fps": 8, "density": 4, "loop": True},
        "boundaries": {"approved": False, "promoted": False, "runtimeChanged": False, "canonicalChanged": False, "v20ThroughV26Changed": False},
    }
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({"version": 27, "preserves": [20, 21, 22, 23, 24, 25, 26], "rejectedSourceRetained": "table-broken-snapped-rejected-source.png", "rollback": "Delete only the V27 source/raw/draft/review files, archive set, builder, verifier and V27 documentation."}, indent=2) + "\n")
    public_catalogue = {k: v for k, v in catalogue.items() if k != "sources"}
    (PUBLIC / "catalogue.json").write_text(json.dumps(public_catalogue, indent=2) + "\n")
    page_data = dict(catalogue)
    page_data["_effectFrames"] = effects
    write_page(page_data)
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "clips": len(clips), "effects": len(effects), "outputs": len(list(RAW.glob('*.png')))}, indent=2))


if __name__ == "__main__":
    main()
