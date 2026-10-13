#!/usr/bin/env python3
"""Build the reversible 16-pose Keeper Prime side-right ↔ back Turn V8."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_keeper_prime_turn_side_back_v1 as v1
import build_keeper_prime_turn_side_back_v2 as v2
import build_keeper_prime_turn_side_back_v6 as v6


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v8"
V7_PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v7"
V7_REGISTER = V7_PACK / "batch-register.json"
PALETTE = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v3/palette/keeper-standard-outfit-palette-v1-draft.json"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v8"
PUBLIC_ROUTE = "/keeper-review/keeper-prime-turn-side-back-v8"
CELL = (256, 320)
ANGLES = (90, 94, 98, 101.5, 105, 112.5, 120, 127.5, 135, 142.5, 150, 157.5, 165, 170, 175, 180)
TARGET_HEIGHTS = (298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 297, 296, 297, 298, 298)
FPS = 16
ALPHA_THRESHOLD = 8
GENERATED = {
    94: "keeper-prime-turn-angle-94-generated.png",
    101.5: "keeper-prime-turn-angle-101-5-generated.png",
    112.5: "keeper-prime-turn-angle-112-5-generated.png",
    127.5: "keeper-prime-turn-angle-127-5-generated.png",
    142.5: "keeper-prime-turn-angle-142-5-generated.png",
    157.5: "keeper-prime-turn-angle-157-5-generated.png",
    170: "keeper-prime-turn-angle-170-generated.png",
    175: "keeper-prime-turn-angle-175-generated.png",
}
RETAINED_ANGLE_INDEX = {90: 0, 98: 1, 105: 2, 120: 3, 135: 4, 150: 5, 165: 6, 180: 7}
PALETTE_SPECS = {
    "capCrownBlue": {"y": (15, 63), "kind": "bright-blue"},
    "capBandNavy": {"y": (60, 80), "kind": "navy"},
    "jumperBlue": {"y": (82, 215), "kind": "bright-blue"},
    "jumperCream": {"y": (115, 174), "kind": "cream"},
    "trouserNavy": {"y": (202, 254), "kind": "navy"},
    "bootNavy": {"y": (254, 317), "kind": "navy"},
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalize(source_path: Path, target_height: int) -> tuple[Image.Image, dict]:
    source = Image.open(source_path).convert("RGBA")
    source_box = source.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0).getbbox()
    if source_box is None:
        raise RuntimeError(f"empty source: {source_path}")
    crop = source.crop(source_box)
    target_width = round(crop.width * target_height / crop.height)
    if target_width > CELL[0] - 16:
        raise RuntimeError(f"{source_path.name} cannot retain the safety gutter")
    resized = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
    left = (CELL[0] - target_width) // 2
    top = 316 - target_height
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    output.alpha_composite(resized, (left, top))
    pixels = output.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if pixels[x, y][3] < ALPHA_THRESHOLD:
                pixels[x, y] = (0, 0, 0, 0)
    return output, {
        "sourcePixels": list(source.size),
        "sourceSignificantAlphaBoundsExclusive": list(source_box),
        "targetHeight": target_height,
        "registeredSize": [target_width, target_height],
        "registeredOffset": [left, top],
        "axisX": 128,
        "floorY": 316,
        "filter": "Lanczos",
        "creativePixelWarp": False,
    }


def ear_skin_pixels(image: Image.Image) -> int:
    count = 0
    for y in range(58, 116):
        for x in range(35, 116):
            red, green, blue, alpha = image.getpixel((x, y))
            if alpha >= 220 and red >= 180 and 65 <= green <= 205 and blue <= 155 and red - blue >= 45:
                count += 1
    return count


def alpha_centroid(image: Image.Image) -> list[float]:
    points = []
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if image.getpixel((x, y))[3] >= ALPHA_THRESHOLD:
                points.append((x, y))
    return [round(sum(x for x, _ in points) / len(points), 3), round(sum(y for _, y in points) / len(points), 3)]


def contact_sheet(frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (len(frames) * 256, 356), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    for index, (angle, frame) in enumerate(zip(ANGLES, frames)):
        stage = v1.checkerboard(); stage.alpha_composite(frame)
        output.alpha_composite(stage, (index * 256, 36))
        draw.text((index * 256 + 7, 10), f"F{index + 1} · {angle:g}°", fill="#ffffff", font=font)
    return output


def ear_evidence(frames: list[Image.Image]) -> Image.Image:
    selected = frames[12:16]
    scale = 3
    crop = (28, 40, 128, 134)
    output = Image.new("RGBA", (4 * 300, 326), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    for index, (frame, angle) in enumerate(zip(selected, ANGLES[12:16])):
        stage = v1.checkerboard(); stage.alpha_composite(frame)
        detail = stage.crop(crop).resize((300, 282), Image.Resampling.NEAREST)
        output.alpha_composite(detail, (index * 300, 36))
        draw.text((index * 300 + 8, 10), f"F{index + 13} · {angle:g}° · far-ear pixels {ear_skin_pixels(frame)}", fill="#ffffff", font=font)
    return output


def old_new_sheet(old_frames: list[Image.Image], frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (8 * 256, 712), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    draw.text((8, 10), "V7 · 8 authored poses · 8 fps", fill="#ffffff", font=font)
    draw.text((8, 366), "V8 · 16 authored poses · 16 fps · same one-second duration", fill="#ffffff", font=font)
    for index, frame in enumerate(old_frames):
        stage = v1.checkerboard(); stage.alpha_composite(frame)
        output.alpha_composite(stage, (index * 256, 36))
    for index in range(8):
        stage = Image.new("RGBA", (256, 320), (12, 20, 27, 255))
        first = frames[index * 2]
        second = frames[index * 2 + 1]
        half_a = v1.checkerboard(); half_a.alpha_composite(first)
        half_b = v1.checkerboard(); half_b.alpha_composite(second)
        stage.alpha_composite(half_a.resize((128, 160), Image.Resampling.LANCZOS), (0, 80))
        stage.alpha_composite(half_b.resize((128, 160), Image.Resampling.LANCZOS), (128, 80))
        output.alpha_composite(stage, (index * 256, 392))
        draw.text((index * 256 + 5, 686), f"F{index * 2 + 1}/F{index * 2 + 2}", fill="#ffffff", font=font)
    return output


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    urls = {}
    for key, source in records.items():
        target = assets / f"{key}-{v2.digest(source)[:16]}{source.suffix}"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(frame_paths: list[Path], old_paths: list[Path], evidence: dict[str, Path]) -> None:
    records = {f"frame{index + 1}": path for index, path in enumerate(frame_paths)}
    records.update({f"old{index + 1}": path for index, path in enumerate(old_paths)})
    records.update(evidence)
    urls = copy_public(records)
    asset = lambda key: f"{PUBLIC_ROUTE}/assets/{urls[key]}"
    frames_json = json.dumps([asset(f"frame{index + 1}") for index in range(16)])
    old_json = json.dumps([asset(f"old{index + 1}") for index in range(8)])
    angles_json = json.dumps(list(ANGLES))
    thumbs = "".join(f'<button class="thumb" data-frame="{index}"><img src="{asset(f"frame{index + 1}")}" alt=""><span>F{index + 1} · {ANGLES[index]:g}°</span></button>' for index in range(16))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side ↔ back Turn V8</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58;--green:#75f3a6}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.review-grid,.compare{{display:grid;grid-template-columns:repeat(2,minmax(300px,1fr));gap:18px}}.large-stage{{width:min(100%,512px);aspect-ratio:4/5;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.large-stage img{{width:100%;height:100%;object-fit:contain}}.game-wrap{{min-height:390px;display:grid;place-items:center}}.game-stage,.game-stage img{{width:128px;height:160px}}.game-stage{{background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/8px 8px;outline:1px solid #6f8492}}.game-stage img{{display:block;object-fit:contain;image-rendering:pixelated}}.compare-stage{{width:min(100%,384px);aspect-ratio:4/5;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/20px 20px}}.compare-stage img{{width:100%;height:100%;object-fit:contain}}button,input{{font:inherit}}button{{color:var(--ink);background:#111a21;border:1px solid var(--line);border-radius:6px;margin:4px;padding:8px 11px}}.step{{border-color:var(--amber)}}.active{{background:#185f3a!important}}.frames{{display:grid;grid-template-columns:repeat(16,minmax(84px,1fr));gap:8px;overflow:auto}}.thumb{{margin:0;padding:5px}}.thumb img{{width:100%;aspect-ratio:4/5;object-fit:contain;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/12px 12px}}.thumb span{{display:block;white-space:nowrap}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}.good{{color:var(--green)}}@media(max-width:850px){{.review-grid,.compare{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/keeper-review/keeper-prime-turn-side-back-v7">← V7 eight-pose candidate</a><h1>Keeper Prime Turn V8 · 16 authored poses</h1><span class="status">New reversible candidate · awaiting visual approval</span><p>V8 keeps all eight V7 poses byte-identical and inserts eight smooth high-resolution drawings. It doubles pose cadence from 8 to 16 fps while retaining the same one-second side-to-back duration. Nothing has entered Final or production.</p></header><main><p class="rule"><strong>Review priority:</strong> watch F13→F16. The far/left ear should emerge as hidden → narrow sliver → partial ear → complete rear view, with no flash at 180°.</p><section class="review-grid"><article><h2>Large V8 inspection</h2><div class="large-stage"><img id="largePlayer" src="{asset('frame1')}" alt="Large V8 turn"></div></article><article><h2>Proposed in-game size</h2><div class="game-wrap"><div class="game-stage"><img id="gamePlayer" src="{asset('frame1')}" alt="V8 turn at proposed game size"></div></div><p>Exact 128 × 160 CSS-pixel display box at 100% browser zoom.</p></article></section><article><h2 id="frameLabel">Frame 1 of 16 · 90°</h2><p id="mode">Looping side ↔ back at 16 fps</p><button id="previous" class="step">← Previous frame</button><button id="next" class="step">Next frame →</button><br><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="pause">Pause</button><br><label>Playback rate <input id="speed" type="range" min="6" max="24" value="16"> <span id="speedValue">16 fps · 62.5 ms/frame</span></label></article><section class="frames">{thumbs}</section><h2>Does doubling the authored cadence help?</h2><section class="compare"><article><h3>V7 baseline · 8 poses / 8 fps</h3><div class="compare-stage"><img id="oldPlayer" src="{asset('old1')}" alt="V7 baseline turn"></div></article><article><h3>V8 proposal · 16 poses / 16 fps</h3><div class="compare-stage"><img id="comparePlayer" src="{asset('frame1')}" alt="V8 proposed turn"></div></article></section><p class="good">Both comparison loops cover the same angle in the same one-second duration.</p><h2>Ear reveal evidence · F13–F16</h2><article><img class="wide" src="{asset('earEvidence')}" alt="Gradual far-ear reveal from 165 to 180 degrees"></article><h2>Complete V8 sequence</h2><article><img class="wide" src="{asset('contact')}" alt="Complete V8 turn sequence"></article><h2>V7 / V8 cadence record</h2><article><img class="wide" src="{asset('comparison')}" alt="V7 and V8 cadence comparison"></article><h2>Approval boundary</h2><article><p>V8 is a separate draft. All V7 poses, earlier approvals, Final, runtime art and manifests remain unchanged. Approval would make V8 the next core-turn artwork candidate only.</p></article></main><script>const frames={frames_json},oldFrames={old_json},angles={angles_json};const large=document.getElementById('largePlayer'),game=document.getElementById('gamePlayer'),compare=document.getElementById('comparePlayer'),old=document.getElementById('oldPlayer'),label=document.getElementById('frameLabel'),mode=document.getElementById('mode'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let timer=null,index=0,sequence=[],cursor=0,loop=false,comparisonStart=performance.now();function show(i){{index=(i+frames.length)%frames.length;large.src=frames[index];game.src=frames[index];compare.src=frames[index];label.textContent=`Frame ${{index+1}} of ${{frames.length}} · ${{angles[index]}}°`;document.querySelectorAll('[data-frame]').forEach(button=>button.classList.toggle('active',Number(button.dataset.frame)===index));}}function stop(message='Paused'){{if(timer)clearTimeout(timer);timer=null;mode.textContent=message;}}function interval(){{return 1000/Number(speed.value)}}function step(delta){{stop('Paused · frame stepping');show(index+delta);}}function play(seq,repeat,name){{stop();sequence=seq;cursor=0;loop=repeat;mode.textContent=name;const tick=()=>{{show(sequence[cursor]);const oldIndex=Math.min(7,Math.floor((sequence[cursor]/16)*8));old.src=oldFrames[oldIndex];cursor+=1;if(cursor>=sequence.length){{if(loop)cursor=0;else{{stop('Finished');return}}}}timer=setTimeout(tick,interval());}};tick();}}document.getElementById('previous').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('forward').onclick=()=>play([...Array(16).keys()],false,'Playing side → back');document.getElementById('reverse').onclick=()=>play([...Array(16).keys()].reverse(),false,'Playing back → side');document.getElementById('pingpong').onclick=()=>play([...Array(16).keys(),...Array.from({{length:14}},(_,i)=>14-i)],true,`Looping side ↔ back at ${{speed.value}} fps`);document.getElementById('pause').onclick=()=>stop();speed.oninput=()=>{{speedValue.textContent=`${{speed.value}} fps · ${{(1000/Number(speed.value)).toFixed(1)}} ms/frame`;if(timer)document.getElementById('pingpong').click();}};document.querySelectorAll('[data-frame]').forEach(button=>button.onclick=()=>{{stop('Paused · selected frame');show(Number(button.dataset.frame));old.src=oldFrames[Math.min(7,Math.floor(Number(button.dataset.frame)/2))];}});show(0);play([...Array(16).keys(),...Array.from({{length:14}},(_,i)=>14-i)],true,'Looping side ↔ back at 16 fps');</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    v7 = json.loads(V7_REGISTER.read_text())
    palette = json.loads(PALETTE.read_text())
    old_paths = [ROOT / item["file"] for item in v7["frames"]]
    old_frames = [Image.open(path).convert("RGBA") for path in old_paths]
    for generated_dir in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if generated_dir.exists():
            shutil.rmtree(generated_dir)
    frame_dir = PACK / "drafts/frames"; frame_dir.mkdir(parents=True, exist_ok=True)
    mask_dir = PACK / "drafts/masks"; mask_dir.mkdir(parents=True, exist_ok=True)

    frames: list[Image.Image] = []
    frame_paths: list[Path] = []
    frame_records = []
    generated_records = []
    for index, (angle, target_height) in enumerate(zip(ANGLES, TARGET_HEIGHTS), start=1):
        target = frame_dir / f"keeper_prime_turn_side-right_to_back_f{index:02d}.png"
        if angle in RETAINED_ANGLE_INDEX:
            prior_index = RETAINED_ANGLE_INDEX[angle]
            shutil.copyfile(old_paths[prior_index], target)
            frame = Image.open(target).convert("RGBA")
            source = {"kind": "retained-v7", "v7Frame": prior_index + 1, "v7File": rel(old_paths[prior_index]), "v7Sha256": v7["frames"][prior_index]["sha256"]}
        else:
            source_path = PACK / "sources" / GENERATED[angle]
            frame, registration = normalize(source_path, target_height)
            component_checks = {}
            coverage_sets = {}
            for name, spec in PALETTE_SPECS.items():
                frame, coverage, changed, check = v6.recolour_to_target(frame, spec, palette["components"][name]["target"]["medianHSV"])
                coverage_path = mask_dir / f"f{index:02d}-{name}-coverage.png"
                changed_path = mask_dir / f"f{index:02d}-{name}-changed.png"
                coverage.save(coverage_path, optimize=False, compress_level=9)
                changed.save(changed_path, optimize=False, compress_level=9)
                component_checks[name] = {**check, "coverageMask": rel(coverage_path), "coverageMaskSha256": v2.digest(coverage_path), "changedMask": rel(changed_path), "changedMaskSha256": v2.digest(changed_path), "yRange": list(spec["y"])}
                coverage_sets[name] = {pixel for pixel, value in enumerate(coverage.tobytes()) if value}
            trouser_boot_overlap = len(coverage_sets["trouserNavy"] & coverage_sets["bootNavy"])
            if trouser_boot_overlap:
                raise RuntimeError(f"frame {index} trouser and boot masks overlap")
            frame.save(target, optimize=False, compress_level=9)
            source = {"kind": "new-authored-intermediate", "source": rel(source_path), "sourceSha256": v2.digest(source_path), "registration": registration, "componentChecks": component_checks, "trouserBootMaskOverlapPixels": trouser_boot_overlap}
            generated_records.append({"frame": index, "angleDegrees": angle, **source})
        frame_paths.append(target)
        frames.append(frame)
        bounds = v1.alpha_bounds(frame)
        frame_records.append({"frame": index, "angleDegrees": angle, "file": rel(target), "sha256": v2.digest(target), "source": source, "opaqueBoundsExclusive": list(bounds), "opaqueHeight": bounds[3] - bounds[1], "floorY": bounds[3], "alphaCentroid": alpha_centroid(frame), "edgeAlphaPixels": v1.edge_alpha_count(frame), "partialAlphaPixels": v6.partial_alpha(frame), "farLeftEarSkinPixels": ear_skin_pixels(frame)})

    forward = PACK / "drafts/keeper_prime_turn_side-right_to_back_f16.png"
    reverse = PACK / "drafts/keeper_prime_turn_back_to_side-right_f16.png"
    v1.save_strip(forward, frames); v1.save_strip(reverse, list(reversed(frames)))
    common = {"w": 32, "h": 40, "density": 8, "frames": 16, "fps": FPS, "anchor": [16, 40], "loop": False, "durationSeconds": 1, "outfit": "standard-single-band", "palette": palette["id"], "status": "draft-v8-awaiting-visual-approval"}
    forward_sidecar = forward.with_suffix(".json"); reverse_sidecar = reverse.with_suffix(".json")
    v2.dump(forward_sidecar, {"name": "keeper_prime_turn_side-right_to_back_v8", **common, "startPose": "standing-side-right-v7", "endPose": "standing-back-v7", "sha256": v2.digest(forward), "frameFiles": [rel(path) for path in frame_paths]})
    v2.dump(reverse_sidecar, {"name": "keeper_prime_turn_back_to_side-right_v8", **common, "startPose": "standing-back-v7", "endPose": "standing-side-right-v7", "sha256": v2.digest(reverse), "frameFiles": [rel(path) for path in reversed(frame_paths)], "exactReverseOf": rel(forward)})

    evidence_dir = PACK / "evidence"; evidence_dir.mkdir(parents=True, exist_ok=True)
    contact = evidence_dir / "v8-contact-sheet.png"
    ears = evidence_dir / "v8-ear-reveal-f13-f16.png"
    comparison = evidence_dir / "v7-v8-cadence-comparison.png"
    contact_sheet(frames).save(contact, optimize=False, compress_level=9)
    ear_evidence(frames).save(ears, optimize=False, compress_level=9)
    old_new_sheet(old_frames, frames).save(comparison, optimize=False, compress_level=9)
    write_page(frame_paths, old_paths, {"contact": contact, "earEvidence": ears, "comparison": comparison})

    retained_positions = [1, 3, 5, 7, 9, 11, 13, 16]
    exact_retention = all((ROOT / frame_records[pos - 1]["file"]).read_bytes() == old_paths[index].read_bytes() for index, pos in enumerate(retained_positions))
    rear_ear_counts = [frame_records[index - 1]["farLeftEarSkinPixels"] for index in (13, 14, 15, 16)]
    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v8",
        "status": "draft-v8-sixteen-pose-cadence-awaiting-visual-approval",
        "purpose": "Test whether eight additional authored intermediates remove the visible 165°→180° ear flash and make the complete side-right↔back turn smoother without changing its one-second duration.",
        "sourceCandidate": {"register": rel(V7_REGISTER), "registerSha256": v2.digest(V7_REGISTER), "disposition": "immutable V7 candidate; all eight V7 pose files are retained byte-for-byte"},
        "cadence": {"v7": {"authoredPoses": 8, "fps": 8, "durationSeconds": 1}, "v8": {"authoredPoses": 16, "fps": 16, "durationSeconds": 1}, "principleUnderReview": "If V8 is visually approved, use similarly dense authored cadence for other Keeper core animations where angle or limb motion otherwise jumps."},
        "anglesDegrees": list(ANGLES),
        "retainedV7Positions": retained_positions,
        "generatedSources": generated_records,
        "frames": frame_records,
        "earOcclusion": {"regionExclusive": [35, 58, 116, 116], "sequenceFrames": [13, 14, 15, 16], "sequenceAnglesDegrees": [165, 170, 175, 180], "farLeftEarSkinPixels": rear_ear_counts, "requiredProgression": "hidden/minimal → narrow sliver → partial → full rear ear"},
        "palette": {"file": rel(PALETTE), "sha256": v2.digest(PALETTE), "method": "each new intermediate receives component-specific additive HSV registration; approved V7 poses remain byte-identical"},
        "animation": {"fps": FPS, "durationSeconds": 1, "cell": list(CELL), "logicalCell": [32, 40], "density": 8, "forward": {"file": rel(forward), "sha256": v2.digest(forward), "sidecar": rel(forward_sidecar), "sidecarSha256": v2.digest(forward_sidecar)}, "reverse": {"file": rel(reverse), "sha256": v2.digest(reverse), "sidecar": rel(reverse_sidecar), "sidecarSha256": v2.digest(reverse_sidecar), "exactFrameOrderReverse": True}},
        "reviewSurface": {"publicReview": f"{PUBLIC_ROUTE}/", "publicPage": rel(PUBLIC / "index.html"), "publicPageSha256": v2.digest(PUBLIC / "index.html"), "largeAndGameViewsSynchronized": True, "gameCssDisplay": [128, 160], "previousNextControls": True, "v7V8EqualDurationComparison": True},
        "evidence": {"contactSheet": {"file": rel(contact), "sha256": v2.digest(contact)}, "earReveal": {"file": rel(ears), "sha256": v2.digest(ears)}, "cadenceComparison": {"file": rel(comparison), "sha256": v2.digest(comparison)}},
        "validation": {"allEightV7PosesByteIdentical": exact_retention, "newIntermediateCount": len(generated_records), "everyFrameFloorY316": all(record["floorY"] == 316 for record in frame_records), "everyFrameTransparentCellEdge": all(record["edgeAlphaPixels"] == 0 for record in frame_records), "allNewTrouserBootMasksDisjoint": all(record["trouserBootMaskOverlapPixels"] == 0 for record in generated_records), "forwardReverseExact": True, "stripSidecarAgreement": True, "productionSpritesChanged": False, "runtimeManifestChanged": False, "finalLaneChanged": False, "priorDraftsChanged": False},
        "approvalBoundary": {"v8Approved": False, "v7Superseded": False, "productionPromotionAllowed": False, "finalLaneEntryAllowed": False},
        "nextGate": "Frank compares V7 and V8 motion at large and exact game scale, concentrating on F13→F16 and the far-ear reveal.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1–V7, approvals, Final and production remain unchanged."
    }
    v2.dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "frames": len(frames), "retainedV7": exact_retention, "earCounts": rear_ear_counts, "public": register["reviewSurface"]["publicReview"]}, indent=2))


if __name__ == "__main__":
    main()
