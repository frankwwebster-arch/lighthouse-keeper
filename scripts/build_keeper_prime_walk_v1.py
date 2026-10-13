#!/usr/bin/env python3
"""Build the reversible finished-art Keeper Prime right-facing walk V1 review pack."""
from __future__ import annotations

import hashlib
import json
import shutil
import statistics
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-13-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-v1"
RAW = PACK / "sources/keeper-prime-walk-8pose-generated.png"
REJECTED_INITIAL = PACK / "sources/rejected-initial-scale-drift.png"
REJECTED_BACKGROUND = PACK / "sources/rejected-unneeded-background-extraction.png"
SIDE = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
SIDE_MASTER = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/sources/keeper-prime-side-right-rigged-clean-master.png"
SIDE_APPROVAL = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v2/batch-register.json"
MOTION = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v3/motion/keeper-prime-rig-motion-v3.json"
MOTION_APPROVAL = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v4/batch-register.json"
ORIGINAL_RAW = ROOT / "art/raw/keeper-first-batch/keeper_walk_f8.png"
ORIGINAL_SIDECAR = ROOT / "art/raw/keeper-first-batch/keeper_walk_f8.json"
ORIGINAL_RUNTIME = ROOT / "public/sprites/keeper_walk.png"

SOURCE_CELL = (384, 512)
CELL = (256, 320)
SOURCE_AXIS_X = 192
TARGET_AXIS_X = 128
TARGET_FLOOR = 316
TARGET_REFERENCE_HEIGHT = 298
ALPHA_THRESHOLD = 8
FPS = 8
POSES = ("contact", "down", "passing", "up", "opposite contact", "opposite down", "opposite passing", "opposite up")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    box = image.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0).getbbox()
    if box is None:
        raise RuntimeError("empty frame")
    return box


def edge_alpha_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = [(x, 0) for x in range(image.width)] + [(x, image.height - 1) for x in range(image.width)]
    points += [(0, y) for y in range(1, image.height - 1)] + [(image.width - 1, y) for y in range(1, image.height - 1)]
    return sum(1 for point in points if alpha.getpixel(point) != 0)


def opaque_area(image: Image.Image) -> int:
    return sum(1 for value in image.getchannel("A").tobytes() if value >= ALPHA_THRESHOLD)


def centroid(image: Image.Image) -> list[float]:
    alpha = image.getchannel("A")
    points = [(x, y) for y in range(image.height) for x in range(image.width) if alpha.getpixel((x, y)) >= ALPHA_THRESHOLD]
    return [round(sum(x for x, _ in points) / len(points), 3), round(sum(y for _, y in points) / len(points), 3)]


def clean_source() -> tuple[Image.Image, Path]:
    raw = Image.open(RAW).convert("RGBA")
    if raw.size != (1536, 1024):
        raise RuntimeError(f"unexpected source geometry {raw.size}")
    clean = raw.copy()
    clean.putalpha(clean.getchannel("A").point(lambda value: 0 if value < ALPHA_THRESHOLD else value))
    path = PACK / "sources/keeper-prime-walk-8pose-clean.png"
    clean.save(path, optimize=False, compress_level=9)
    return clean, path


def source_cells(clean: Image.Image) -> tuple[list[Image.Image], list[dict]]:
    cells, records = [], []
    for index in range(8):
        col, row = index % 4, index // 4
        cell = clean.crop((col * SOURCE_CELL[0], row * SOURCE_CELL[1], (col + 1) * SOURCE_CELL[0], (row + 1) * SOURCE_CELL[1]))
        box = alpha_bounds(cell)
        record = {
            "frame": index + 1,
            "sourceCell": [col, row],
            "significantAlphaBoundsExclusive": list(box),
            "opaqueWidth": box[2] - box[0],
            "opaqueHeight": box[3] - box[1],
            "edgeAlphaPixels": edge_alpha_count(cell),
        }
        if record["edgeAlphaPixels"]:
            raise RuntimeError(f"source frame {index + 1} touches its cell edge")
        cells.append(cell)
        records.append(record)
    return cells, records


def normalize(cells: list[Image.Image], source_records: list[dict]) -> tuple[list[Image.Image], list[dict]]:
    scale = TARGET_REFERENCE_HEIGHT / source_records[0]["opaqueHeight"]
    frames, records = [], []
    frame_dir = PACK / "drafts/frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    for index, (cell, source_record) in enumerate(zip(cells, source_records)):
        box = tuple(source_record["significantAlphaBoundsExclusive"])
        crop = cell.crop(box)
        size = (round(crop.width * scale), round(crop.height * scale))
        resized = crop.resize(size, Image.Resampling.LANCZOS)
        left = round(TARGET_AXIS_X - (SOURCE_AXIS_X - box[0]) * scale)
        top = TARGET_FLOOR - size[1]
        frame = Image.new("RGBA", CELL, (0, 0, 0, 0))
        frame.alpha_composite(resized, (left, top))
        path = frame_dir / f"keeper_prime_walk-right_f{index + 1}.png"
        frame.save(path, optimize=False, compress_level=9)
        bounds = alpha_bounds(frame)
        record = {
            "frame": index + 1,
            "pose": POSES[index],
            "file": rel(path),
            "sha256": digest(path),
            "opaqueBoundsExclusive": list(bounds),
            "opaqueWidth": bounds[2] - bounds[0],
            "opaqueHeight": bounds[3] - bounds[1],
            "opaqueArea": opaque_area(frame),
            "alphaCentroid": centroid(frame),
            "edgeAlphaPixels": edge_alpha_count(frame),
            "registration": {
                "sharedScale": round(scale, 12),
                "sourceAxisX": SOURCE_AXIS_X,
                "targetAxisX": TARGET_AXIS_X,
                "targetFloorExclusive": TARGET_FLOOR,
                "registeredSize": list(size),
                "registeredOffset": [left, top],
                "filter": "Lanczos",
                "perFrameScaleChange": False,
                "creativePixelWarp": False,
            },
        }
        if record["edgeAlphaPixels"]:
            raise RuntimeError(f"normalized frame {index + 1} touches a cell edge")
        frames.append(frame)
        records.append(record)
    return frames, records


def save_strip(path: Path, frames: list[Image.Image]) -> None:
    strip = Image.new("RGBA", (CELL[0] * len(frames), CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=False, compress_level=9)


def palette_sample(image: Image.Image, y0: int, y1: int, family: str) -> list[int]:
    values = []
    for y in range(max(0, y0), min(image.height, y1)):
        for x in range(image.width):
            r, g, b, a = image.getpixel((x, y))
            if a < 128:
                continue
            if family == "blue" and b > r + 18 and b >= g:
                values.append((r, g, b))
            if family == "navy" and b > r + 8 and b >= g and max(r, g, b) < 150:
                values.append((r, g, b))
    if not values:
        return [0, 0, 0]
    return [round(statistics.median(value[channel] for value in values)) for channel in range(3)]


def palette_record(frame: Image.Image) -> dict:
    return {
        "capBlue": palette_sample(frame, 15, 90, "blue"),
        "jumperBlue": palette_sample(frame, 120, 225, "blue"),
        "trouserNavy": palette_sample(frame, 205, 285, "navy"),
        "bootNavy": palette_sample(frame, 255, 318, "navy"),
    }


def checkerboard() -> Image.Image:
    output = Image.new("RGBA", CELL, (29, 40, 49, 255))
    draw = ImageDraw.Draw(output)
    for y in range(0, CELL[1], 16):
        for x in range(0, CELL[0], 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, x + 15, y + 15), fill=(41, 55, 65, 255))
    return output


def contact_sheet(frames: list[Image.Image], side: Image.Image) -> tuple[Path, Path]:
    font = ImageFont.load_default()
    contact = Image.new("RGBA", (8 * CELL[0], 356), (12, 20, 27, 255))
    draw = ImageDraw.Draw(contact)
    for index, frame in enumerate(frames):
        stage = checkerboard(); stage.alpha_composite(frame)
        contact.alpha_composite(stage, (index * CELL[0], 36))
        draw.text((index * CELL[0] + 8, 10), f"F{index + 1} · {POSES[index]}", fill="#ffffff", font=font)
        draw.line((index * CELL[0], 316 + 36, (index + 1) * CELL[0] - 1, 316 + 36), fill="#ff5d71", width=1)
    contact_path = PACK / "evidence/walk-contact-sheet.png"
    contact_path.parent.mkdir(parents=True, exist_ok=True)
    contact.save(contact_path, optimize=False, compress_level=9)

    comparison = Image.new("RGBA", (9 * CELL[0], 356), (12, 20, 27, 255))
    comparison_draw = ImageDraw.Draw(comparison)
    for index, (label, frame) in enumerate([("approved side neutral", side), *[(f"walk F{i + 1}", f) for i, f in enumerate(frames)]]):
        stage = checkerboard(); stage.alpha_composite(frame)
        comparison.alpha_composite(stage, (index * CELL[0], 36))
        comparison_draw.text((index * CELL[0] + 8, 10), label, fill="#ffffff", font=font)
    comparison_path = PACK / "evidence/approved-side-vs-walk.png"
    comparison.save(comparison_path, optimize=False, compress_level=9)
    return contact_path, comparison_path


def sidecar(strip: Path) -> Path:
    path = strip.with_suffix(".json")
    dump(path, {
        "name": "keeper_prime_walk-right",
        "w": 32,
        "h": 40,
        "density": 8,
        "frames": 8,
        "fps": FPS,
        "loop": True,
        "direction": "right",
        "outfit": "standard-single-band",
        "startPose": "walk-side-right-contact",
        "endPose": "walk-side-right-opposite-up",
        "rootMotion": {"authoredInPixels": False, "speedHighResolutionPixelsPerSecond": 168, "speedLogicalPixelsPerSecond": 21},
        "cell": [256, 320],
        "anchor": [16, 40],
        "sha256": digest(strip),
        "status": "review-draft-not-production",
    })
    return path


def copy_public(items: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    urls = {}
    for key, source in items.items():
        target = assets / f"{key}-{digest(source)[:16]}{source.suffix}"
        shutil.copyfile(source, target)
        urls[key] = f"assets/{target.name}"
    return urls


def write_page(frame_paths: list[Path], strip: Path, contact: Path, comparison: Path, side: Path) -> None:
    items = {f"frame{i + 1}": path for i, path in enumerate(frame_paths)}
    items.update({"strip": strip, "contact": contact, "comparison": comparison, "side": side, "original": ORIGINAL_RAW})
    urls = copy_public(items)
    frames_json = json.dumps([urls[f"frame{i + 1}"] for i in range(8)])
    labels_json = json.dumps(list(POSES))
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime Walk V1</title><style>
:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58;--green:#77e3a4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.views{{display:grid;grid-template-columns:minmax(320px,640px) 1fr;gap:24px;align-items:center}}.large{{width:min(512px,100%);aspect-ratio:4/5;margin:auto}}.game{{width:128px;height:160px}}.stage{{position:relative;overflow:hidden;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.stage img{{width:100%;height:100%;object-fit:contain;image-rendering:auto}}.game.stage{{background-size:12px 12px}}button,input{{font:inherit}}button{{margin:4px;padding:8px 11px}}button.active{{background:#185f3a;color:white}}.frame-grid{{display:grid;grid-template-columns:repeat(8,1fr);gap:8px}}.frame-grid button{{background:#111a21;border:1px solid var(--line);color:var(--ink)}}.frame-grid img{{width:100%;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/12px 12px}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}.route-pair{{display:flex;gap:24px;align-items:end;flex-wrap:wrap}}.route-large{{width:584px;height:320px}}.route-game{{width:292px;height:160px}}.walker{{position:absolute;bottom:0;left:0;object-fit:contain}}.route-large .walker{{width:256px;height:320px}}.route-game .walker{{width:128px;height:160px}}.door{{position:absolute;inset-block:0;width:34px;background:#263640;border-inline:2px solid #7690a0;z-index:2}}.door.left{{left:0}}.door.right{{right:0}}@media(max-width:850px){{.views{{grid-template-columns:1fr}}.frame-grid{{grid-template-columns:repeat(4,1fr)}}}}
</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-prime-side-right-rigged-v2/">Approved Side-right authority</a><h1>Keeper Prime Walk V1 · right-facing</h1><span class="status">Finished-art walk draft · awaiting visual approval</span><p>One coherent eight-pose loop derived from the approved Side-right model and Rig Motion V3. Nothing has entered Final or production.</p></header><main><p class="rule"><strong>Review priority:</strong> identity and palette must remain constant while the legs and arms move. Check the F8→F1 loop seam, boot planting, beard stability, body width and any apparent scale pulse.</p>
<article class="views"><div class="stage large"><img id="large" src="{urls['frame1']}" alt="Large walk frame"></div><div><h2 id="label">Frame 1 · contact</h2><p id="state">Looping in place</p><div><button id="prev">← Previous frame</button><button id="next">Next frame →</button><button id="loop">Loop walk</button><button id="move">Moving route</button><button id="pause">Pause</button></div><label>Frame time <input id="speed" type="range" min="80" max="400" value="125"> <span id="speedValue">125 ms</span></label><h3>Exact proposed game display size</h3><div class="stage game"><img id="game" src="{urls['frame1']}" alt="Walk frame at 128 by 160 pixels"></div><p>Both views use the same frame source and index. The game box is exactly 128 × 160 CSS pixels.</p></div></article>
<section class="frame-grid">{''.join(f'<button data-frame="{i}"><img src="{urls[f"frame{i + 1}"]}" alt="Frame {i + 1}"><span>F{i + 1} · {POSES[i]}</span></button>' for i in range(8))}</section>
<h2>Translated walk — begins and ends fully hidden</h2><article><div class="route-pair"><div><strong>Large source scale</strong><div class="stage route-large"><div class="door left"></div><img id="routeLarge" class="walker" src="{urls['frame1']}" alt="Translated walk large"><div class="door right"></div></div></div><div><strong>Exact game scale</strong><div class="stage route-game"><div class="door left"></div><img id="routeGame" class="walker" src="{urls['frame1']}" alt="Translated walk game scale"><div class="door right"></div></div></div></div><p>The route uses the approved Rig V3 speed: 168 high-resolution pixels per second (21 logical pixels per second), eight implied steps over five seconds. It starts walking while fully behind the left door.</p></article>
<h2>All eight registered poses</h2><article><img class="wide" src="{urls['contact']}" alt="Walk contact sheet"></article><h2>Approved side authority versus walk</h2><article><img class="wide" src="{urls['comparison']}" alt="Approved side authority beside walk frames"></article>
<h2>Current production versus Walk V1</h2><article class="views"><div><h3>Current production · unchanged</h3><img class="wide" src="{urls['original']}" alt="Current production walk strip"></div><div><h3>Walk V1 review draft</h3><img class="wide" src="{urls['strip']}" alt="Walk V1 review strip"></div></article>
<h2>Approval boundary</h2><article><p>This page proposes only the right-facing walk loop. Approval would make these exact eight poses the finished-art walk authority for the next separate walk→stop draft. It would not approve stop/start stitching, place anything in Final, or promote runtime art.</p></article></main><script>
const frames={frames_json},labels={labels_json};const large=document.getElementById('large'),game=document.getElementById('game'),routeLarge=document.getElementById('routeLarge'),routeGame=document.getElementById('routeGame'),label=document.getElementById('label'),state=document.getElementById('state'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let index=0,timer=null,mode='pause',start=0;function show(i){{index=(i+8)%8;for(const img of [large,game,routeLarge,routeGame])img.src=frames[index];label.textContent=`Frame ${{index+1}} · ${{labels[index]}}`;document.querySelectorAll('[data-frame]').forEach(b=>b.classList.toggle('active',Number(b.dataset.frame)===index));}}function stop(){{if(timer)clearTimeout(timer);timer=null;mode='pause';state.textContent='Paused';}}function tickLoop(){{if(mode!=='loop')return;show(index+1);timer=setTimeout(tickLoop,Number(speed.value));}}function loop(){{stop();mode='loop';state.textContent='Looping in place';timer=setTimeout(tickLoop,Number(speed.value));}}function tickMove(now){{if(mode!=='move')return;const elapsed=Math.min(5000,now-start),progress=elapsed/5000;show(Math.floor(elapsed/(1000/8))%8);routeLarge.style.transform=`translateX(${{-256+840*progress}}px)`;routeGame.style.transform=`translateX(${{-128+420*progress}}px)`;if(elapsed<5000)requestAnimationFrame(tickMove);else{{state.textContent='Moving route complete';mode='pause'}}}}function move(){{stop();mode='move';state.textContent='Moving at approved Rig V3 speed';start=performance.now();requestAnimationFrame(tickMove)}}document.getElementById('prev').onclick=()=>{{stop();show(index-1)}};document.getElementById('next').onclick=()=>{{stop();show(index+1)}};document.getElementById('loop').onclick=loop;document.getElementById('move').onclick=move;document.getElementById('pause').onclick=stop;speed.oninput=()=>speedValue.textContent=`${{speed.value}} ms`;document.querySelectorAll('[data-frame]').forEach(b=>b.onclick=()=>{{stop();show(Number(b.dataset.frame))}});show(0);loop();
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    required = [RAW, REJECTED_INITIAL, REJECTED_BACKGROUND, SIDE, SIDE_MASTER, SIDE_APPROVAL, MOTION, MOTION_APPROVAL, ORIGINAL_RAW, ORIGINAL_SIDECAR, ORIGINAL_RUNTIME]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    side_approval = json.loads(SIDE_APPROVAL.read_text())
    motion_approval = json.loads(MOTION_APPROVAL.read_text())
    if side_approval.get("status") != "approved-side-right-artwork-authority":
        raise RuntimeError("approved side-right authority missing")
    if motion_approval.get("status") != "approved-motion-authority":
        raise RuntimeError("approved motion authority missing")

    for directory in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    clean, clean_path = clean_source()
    cells, source_records = source_cells(clean)
    frames, frame_records = normalize(cells, source_records)
    strip = PACK / "drafts/keeper_prime_walk-right_f8.png"
    save_strip(strip, frames)
    strip_sidecar = sidecar(strip)
    side = Image.open(SIDE).convert("RGBA")
    contact, comparison = contact_sheet(frames, side)
    frame_paths = [ROOT / record["file"] for record in frame_records]
    palettes = [palette_record(frame) for frame in frames]
    continuity = []
    for index in range(8):
        a, b = frame_records[index], frame_records[(index + 1) % 8]
        continuity.append({
            "fromFrame": index + 1,
            "toFrame": (index + 1) % 8 + 1,
            "opaqueHeightDelta": b["opaqueHeight"] - a["opaqueHeight"],
            "opaqueWidthDelta": b["opaqueWidth"] - a["opaqueWidth"],
            "alphaCentroidDelta": [round(b["alphaCentroid"][0] - a["alphaCentroid"][0], 3), round(b["alphaCentroid"][1] - a["alphaCentroid"][1], 3)],
            "opaqueAreaRatio": round(b["opaqueArea"] / a["opaqueArea"], 6),
        })
    register = {
        "batchId": "keeper-prime-walk-2026-10-13-v1",
        "status": "draft-finished-art-walk-v1-awaiting-visual-approval",
        "purpose": "Create the first finished-art right-facing Keeper Prime walk loop from the approved side identity and Rig Motion V3 gait.",
        "authorities": {
            "sideRight": {"file": rel(SIDE), "sha256": digest(SIDE), "smoothMaster": rel(SIDE_MASTER), "smoothMasterSha256": digest(SIDE_MASTER), "approval": rel(SIDE_APPROVAL), "approvalSha256": digest(SIDE_APPROVAL), "approvalWording": side_approval["approval"]["wording"]},
            "motion": {"file": rel(MOTION), "sha256": digest(MOTION), "approval": rel(MOTION_APPROVAL), "approvalSha256": digest(MOTION_APPROVAL), "approvalWording": motion_approval["approval"]["wording"]},
        },
        "canonicalComparison": {
            "rawStrip": {"file": rel(ORIGINAL_RAW), "sha256": digest(ORIGINAL_RAW)},
            "rawSidecar": {"file": rel(ORIGINAL_SIDECAR), "sha256": digest(ORIGINAL_SIDECAR)},
            "runtimeStrip": {"file": rel(ORIGINAL_RUNTIME), "sha256": digest(ORIGINAL_RUNTIME)},
            "allRemainUnchanged": True,
        },
        "generation": {
            "mode": "built-in-image-generation-identity-preserve",
            "selectedSource": {"file": rel(RAW), "sha256": digest(RAW)},
            "cleanSource": {"file": rel(clean_path), "sha256": digest(clean_path), "lowAlphaCleanupThreshold": ALPHA_THRESHOLD},
            "rejectedSources": [{"file": rel(REJECTED_INITIAL), "sha256": digest(REJECTED_INITIAL), "reason": "bottom-row scale drift"}, {"file": rel(REJECTED_BACKGROUND), "sha256": digest(REJECTED_BACKGROUND), "reason": "unneeded background-only iteration"}],
            "sourceGrid": {"columns": 4, "rows": 2, "cell": list(SOURCE_CELL), "frameOrder": "top row left-to-right, then bottom row left-to-right"},
            "sourceCells": source_records,
            "promptLog": rel(PACK / "PROMPT_LOG.md"),
        },
        "animation": {
            "name": "keeper_prime_walk-right",
            "frames": 8,
            "fps": FPS,
            "durationSeconds": 1,
            "loop": True,
            "strip": {"file": rel(strip), "sha256": digest(strip), "sidecar": rel(strip_sidecar), "sidecarSha256": digest(strip_sidecar)},
            "rootMotion": {"bakedIntoStrip": False, "speedHighResolutionPixelsPerSecond": 168, "speedLogicalPixelsPerSecond": 21, "representativeDurationSeconds": 5, "beginsAndEndsFullyHidden": True},
        },
        "frames": frame_records,
        "palette": {"method": "median alpha>=128 samples in registered vertical regions", "approvedSideReference": palette_record(side), "frames": palettes},
        "continuity": continuity,
        "evidence": {"contactSheet": {"file": rel(contact), "sha256": digest(contact)}, "approvedSideComparison": {"file": rel(comparison), "sha256": digest(comparison)}},
        "validation": {"sharedScaleOnly": True, "perFrameScaleChange": False, "everySourceCellHasTransparentEdge": True, "everyOutputCellHasTransparentEdge": True, "stripMatchesFrames": True, "sidecarMatchesStrip": True, "leftWalkDeferredToDeterministicMirror": True, "productionSpritesChanged": False, "runtimeManifestChanged": False, "workbenchFinalChanged": False},
        "approvalBoundary": {"walkV1Approved": False, "walkStopApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank visually reviews the right-facing finished-art walk loop before any walk-to-stop frames are authored.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; all approved authorities, production sprites, manifests and prior drafts remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(frame_paths, strip, contact, comparison, SIDE)
    print(json.dumps({"batch": register["batchId"], "frames": 8, "fps": FPS, "publicPage": rel(PUBLIC / "index.html"), "sourceSha256": digest(RAW)}, indent=2))


if __name__ == "__main__":
    main()
