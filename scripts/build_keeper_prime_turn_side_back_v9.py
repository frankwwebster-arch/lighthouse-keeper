#!/usr/bin/env python3
"""Build V9: V7 plus one controlled 172.5-degree intermediate pose."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_keeper_prime_turn_side_back_v1 as v1
import build_keeper_prime_turn_side_back_v2 as v2
import build_keeper_prime_turn_side_back_v6 as v6


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9"
V7_REGISTER = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v7/batch-register.json"
V8_REGISTER = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v8/batch-register.json"
PALETTE = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v3/palette/keeper-standard-outfit-palette-v1-draft.json"
SOURCE = PACK / "sources/keeper-prime-turn-angle-172-5-generated.png"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v9"
PUBLIC_ROUTE = "/keeper-review/keeper-prime-turn-side-back-v9"
ANGLES = (90, 98, 105, 120, 135, 150, 165, 172.5, 180)
CELL = (256, 320)
FPS = 9
ALPHA_THRESHOLD = 8
SPECS = {
    "capCrownBlue": {"y": (15, 63), "kind": "bright-blue"},
    "capBandNavy": {"y": (60, 80), "kind": "navy"},
    "jumperBlue": {"y": (82, 215), "kind": "bright-blue"},
    "jumperCream": {"y": (115, 174), "kind": "cream"},
    "trouserNavy": {"y": (202, 254), "kind": "navy"},
    "bootNavy": {"y": (254, 317), "kind": "navy"},
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalize(source_path: Path) -> tuple[Image.Image, dict]:
    source = Image.open(source_path).convert("RGBA")
    box = source.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0).getbbox()
    if box is None:
        raise RuntimeError("empty midpoint source")
    crop = source.crop(box)
    height = 297
    width = round(crop.width * height / crop.height)
    if width > CELL[0] - 16:
        raise RuntimeError("midpoint cannot retain transparent gutter")
    resized = crop.resize((width, height), Image.Resampling.LANCZOS)
    left, top = (CELL[0] - width) // 2, 316 - height
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    output.alpha_composite(resized, (left, top))
    pixels = output.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if pixels[x, y][3] < ALPHA_THRESHOLD:
                pixels[x, y] = (0, 0, 0, 0)
    return output, {"sourcePixels": list(source.size), "sourceSignificantAlphaBoundsExclusive": list(box), "registeredSize": [width, height], "registeredOffset": [left, top], "targetHeight": height, "axisX": 128, "floorY": 316, "filter": "Lanczos", "creativePixelWarp": False}


def centroid(image: Image.Image) -> list[float]:
    points = [(x, y) for y in range(320) for x in range(256) if image.getpixel((x, y))[3] >= ALPHA_THRESHOLD]
    return [round(sum(x for x, _ in points) / len(points), 3), round(sum(y for _, y in points) / len(points), 3)]


def far_ear_pixels(image: Image.Image) -> int:
    return sum(1 for y in range(58, 116) for x in range(35, 116) if (lambda p: p[3] >= 220 and p[0] >= 180 and 65 <= p[1] <= 205 and p[2] <= 155 and p[0] - p[2] >= 45)(image.getpixel((x, y))))


def contact_sheet(frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (len(frames) * 256, 356), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    for index, (angle, frame) in enumerate(zip(ANGLES, frames)):
        stage = v1.checkerboard(); stage.alpha_composite(frame)
        output.alpha_composite(stage, (index * 256, 36))
        draw.text((index * 256 + 7, 10), f"F{index + 1} · {angle:g}°", fill="#ffffff", font=ImageFont.load_default())
    return output


def rear_evidence(frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (900, 356), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    for index, frame_index in enumerate((6, 7, 8)):
        stage = v1.checkerboard(); stage.alpha_composite(frames[frame_index])
        output.alpha_composite(stage, (index * 300 + 22, 36))
        draw.text((index * 300 + 8, 10), f"F{frame_index + 1} · {ANGLES[frame_index]:g}° · far-ear {far_ear_pixels(frames[frame_index])}", fill="#ffffff", font=ImageFont.load_default())
    return output


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists(): shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    urls = {}
    for key, source in records.items():
        target = assets / f"{key}-{v2.digest(source)[:16]}{source.suffix}"
        shutil.copyfile(source, target); urls[key] = target.name
    return urls


def write_page(paths: list[Path], old_paths: list[Path], contact: Path, rear: Path) -> None:
    records = {f"frame{i + 1}": path for i, path in enumerate(paths)}
    records.update({f"old{i + 1}": path for i, path in enumerate(old_paths)})
    records.update({"contact": contact, "rear": rear})
    urls = copy_public(records)
    asset = lambda key: f"{PUBLIC_ROUTE}/assets/{urls[key]}"
    frames_json = json.dumps([asset(f"frame{i + 1}") for i in range(9)])
    old_json = json.dumps([asset(f"old{i + 1}") for i in range(8)])
    angles_json = json.dumps(list(ANGLES))
    thumbs = "".join(f'<button class="thumb" data-frame="{i}"><img src="{asset(f"frame{i + 1}")}" alt=""><span>F{i + 1} · {ANGLES[i]:g}°</span></button>' for i in range(9))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side ↔ back Turn V9</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1450px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.grid,.compare{{display:grid;grid-template-columns:repeat(2,minmax(300px,1fr));gap:18px}}.stage{{width:min(100%,512px);aspect-ratio:4/5;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.stage img{{width:100%;height:100%;object-fit:contain}}.game-wrap{{min-height:390px;display:grid;place-items:center}}.game,.game img{{width:128px;height:160px}}.game{{background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/8px 8px;outline:1px solid #6f8492}}.game img{{object-fit:contain;image-rendering:pixelated}}.compare .stage{{width:min(100%,384px)}}button,input{{font:inherit}}button{{color:var(--ink);background:#111a21;border:1px solid var(--line);border-radius:6px;margin:4px;padding:8px 11px}}.step{{border-color:var(--amber)}}.active{{background:#185f3a!important}}.frames{{display:grid;grid-template-columns:repeat(9,minmax(88px,1fr));gap:8px;overflow:auto}}.thumb{{margin:0;padding:5px}}.thumb img{{width:100%;aspect-ratio:4/5;object-fit:contain;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/12px 12px}}.thumb span{{display:block;white-space:nowrap}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}@media(max-width:850px){{.grid,.compare{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/keeper-review/keeper-prime-turn-side-back-v7">← V7 eight-frame base</a><h1>Keeper Prime Turn V9 · one intermediate only</h1><span class="status">New reversible candidate · awaiting visual approval</span><p>V9 rejects V8's global 16-frame strategy. It keeps every V7 frame byte-identical and inserts only one new 172.5° pose between V7 F7 and F8. Final and production remain unchanged.</p></header><main><p class="rule"><strong>Review priority:</strong> does the single 165° → 172.5° → 180° sequence remove the ear flash without creating a new body, cap or boot wobble?</p><section class="grid"><article><h2>Large V9 inspection</h2><div class="stage"><img id="largePlayer" src="{asset('frame1')}" alt="Large V9 turn"></div></article><article><h2>Proposed in-game size</h2><div class="game-wrap"><div class="game"><img id="gamePlayer" src="{asset('frame1')}" alt="V9 game scale"></div></div><p>Exact 128 × 160 CSS-pixel display box.</p></article></section><article><h2 id="frameLabel">Frame 1 of 9 · 90°</h2><p id="mode">Looping side ↔ back at 9 fps</p><button id="previous" class="step">← Previous frame</button><button id="next" class="step">Next frame →</button><br><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="pause">Pause</button></article><section class="frames">{thumbs}</section><h2>Equal-duration comparison</h2><section class="compare"><article><h3>V7 · 8 poses / 8 fps</h3><div class="stage"><img id="oldPlayer" src="{asset('old1')}" alt="V7 baseline"></div></article><article><h3>V9 · 9 poses / 9 fps</h3><div class="stage"><img id="comparePlayer" src="{asset('frame1')}" alt="V9 candidate"></div></article></section><h2>Only changed interval</h2><article><img class="wide" src="{asset('rear')}" alt="165, 172.5 and 180 degree rear sequence"></article><h2>Complete V9 sequence</h2><article><img class="wide" src="{asset('contact')}" alt="Complete V9 sequence"></article><h2>Approval boundary</h2><article><p>V8 is rejected provenance. V9 is a separate draft based directly on V7. Approval would not promote Final or production.</p></article></main><script>const frames={frames_json},oldFrames={old_json},angles={angles_json};const large=document.getElementById('largePlayer'),game=document.getElementById('gamePlayer'),compare=document.getElementById('comparePlayer'),old=document.getElementById('oldPlayer'),label=document.getElementById('frameLabel'),mode=document.getElementById('mode');let timer=null,index=0;function show(i){{index=(i+9)%9;large.src=frames[index];game.src=frames[index];compare.src=frames[index];old.src=oldFrames[Math.min(7,Math.floor(index*8/9))];label.textContent=`Frame ${{index+1}} of 9 · ${{angles[index]}}°`;document.querySelectorAll('[data-frame]').forEach(b=>b.classList.toggle('active',Number(b.dataset.frame)===index));}}function stop(message='Paused'){{if(timer)clearTimeout(timer);timer=null;mode.textContent=message;}}function play(seq,loop,name){{stop();let cursor=0;mode.textContent=name;const tick=()=>{{show(seq[cursor++]);if(cursor>=seq.length){{if(loop)cursor=0;else{{stop('Finished');return}}}}timer=setTimeout(tick,1000/9);}};tick();}}document.getElementById('previous').onclick=()=>{{stop('Paused · frame stepping');show(index-1)}};document.getElementById('next').onclick=()=>{{stop('Paused · frame stepping');show(index+1)}};document.getElementById('forward').onclick=()=>play([0,1,2,3,4,5,6,7,8],false,'Playing side → back');document.getElementById('reverse').onclick=()=>play([8,7,6,5,4,3,2,1,0],false,'Playing back → side');document.getElementById('pingpong').onclick=()=>play([0,1,2,3,4,5,6,7,8,7,6,5,4,3,2,1],true,'Looping side ↔ back at 9 fps');document.getElementById('pause').onclick=()=>stop();document.querySelectorAll('[data-frame]').forEach(b=>b.onclick=()=>{{stop('Paused · selected frame');show(Number(b.dataset.frame))}});show(0);document.getElementById('pingpong').click();</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    v7 = json.loads(V7_REGISTER.read_text()); palette = json.loads(PALETTE.read_text())
    old_paths = [ROOT / record["file"] for record in v7["frames"]]
    old_frames = [Image.open(path).convert("RGBA") for path in old_paths]
    for generated in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if generated.exists(): shutil.rmtree(generated)
    frames = [frame.copy() for frame in old_frames[:7]]
    midpoint, registration = normalize(SOURCE)
    masks = PACK / "drafts/masks"; masks.mkdir(parents=True, exist_ok=True)
    checks, coverage_sets = {}, {}
    for name, spec in SPECS.items():
        midpoint, coverage, changed, check = v6.recolour_to_target(midpoint, spec, palette["components"][name]["target"]["medianHSV"])
        coverage_path = masks / f"f08-{name}-coverage.png"; changed_path = masks / f"f08-{name}-changed.png"
        coverage.save(coverage_path, optimize=False, compress_level=9); changed.save(changed_path, optimize=False, compress_level=9)
        checks[name] = {**check, "coverageMask": rel(coverage_path), "coverageMaskSha256": v2.digest(coverage_path), "changedMask": rel(changed_path), "changedMaskSha256": v2.digest(changed_path)}
        coverage_sets[name] = {pixel for pixel, value in enumerate(coverage.tobytes()) if value}
    overlap = len(coverage_sets["trouserNavy"] & coverage_sets["bootNavy"])
    if overlap: raise RuntimeError("midpoint trouser/boot masks overlap")
    frames.extend((midpoint, old_frames[7]))
    frame_dir = PACK / "drafts/frames"; frame_dir.mkdir(parents=True, exist_ok=True)
    paths, records = [], []
    for index, (angle, frame) in enumerate(zip(ANGLES, frames), start=1):
        path = frame_dir / f"keeper_prime_turn_side-right_to_back_f{index:02d}.png"
        if index <= 7: shutil.copyfile(old_paths[index - 1], path)
        elif index == 9: shutil.copyfile(old_paths[7], path)
        else: frame.save(path, optimize=False, compress_level=9)
        bounds = v1.alpha_bounds(frame); paths.append(path)
        records.append({"frame": index, "angleDegrees": angle, "file": rel(path), "sha256": v2.digest(path), "source": "new-172.5-intermediate" if index == 8 else f"byte-identical-v7-f{index if index <= 7 else 8}", "opaqueBoundsExclusive": list(bounds), "opaqueHeight": bounds[3] - bounds[1], "floorY": bounds[3], "alphaCentroid": centroid(frame), "edgeAlphaPixels": v1.edge_alpha_count(frame), "partialAlphaPixels": v6.partial_alpha(frame), "farLeftEarSkinPixels": far_ear_pixels(frame)})
    forward = PACK / "drafts/keeper_prime_turn_side-right_to_back_f9.png"; reverse = PACK / "drafts/keeper_prime_turn_back_to_side-right_f9.png"
    v1.save_strip(forward, frames); v1.save_strip(reverse, list(reversed(frames)))
    common = {"w": 32, "h": 40, "density": 8, "frames": 9, "fps": FPS, "anchor": [16, 40], "loop": False, "durationSeconds": 1, "outfit": "standard-single-band", "status": "draft-v9-awaiting-visual-approval"}
    forward_json = forward.with_suffix(".json"); reverse_json = reverse.with_suffix(".json")
    v2.dump(forward_json, {"name": "keeper_prime_turn_side-right_to_back_v9", **common, "startPose": "standing-side-right-v7", "endPose": "standing-back-v7", "sha256": v2.digest(forward), "frameFiles": [rel(path) for path in paths]})
    v2.dump(reverse_json, {"name": "keeper_prime_turn_back_to_side-right_v9", **common, "startPose": "standing-back-v7", "endPose": "standing-side-right-v7", "sha256": v2.digest(reverse), "frameFiles": [rel(path) for path in reversed(paths)], "exactReverseOf": rel(forward)})
    evidence = PACK / "evidence"; evidence.mkdir(parents=True, exist_ok=True)
    contact = evidence / "v9-contact-sheet.png"; rear = evidence / "v9-only-changed-interval.png"
    contact_sheet(frames).save(contact, optimize=False, compress_level=9); rear_evidence(frames).save(rear, optimize=False, compress_level=9)
    write_page(paths, old_paths, contact, rear)
    retained = all(paths[i].read_bytes() == old_paths[i].read_bytes() for i in range(7)) and paths[8].read_bytes() == old_paths[7].read_bytes()
    ear_counts = [records[i]["farLeftEarSkinPixels"] for i in (6, 7, 8)]
    register = {"batchId": "keeper-prime-turn-side-back-2026-10-13-v9", "status": "draft-v9-single-intermediate-awaiting-visual-approval", "purpose": "Test one temporally controlled 172.5° intermediate between V7 F7 and F8 after V8's global 16-pose strategy was rejected as significantly jerkier.", "v7Base": {"register": rel(V7_REGISTER), "registerSha256": v2.digest(V7_REGISTER), "disposition": "all eight V7 frames retained byte-for-byte"}, "rejectedV8": {"register": rel(V8_REGISTER), "registerSha256": v2.digest(V8_REGISTER), "feedback": "It's now significantly more jerky, so that's not an improvement", "disposition": "rejected provenance; no V8 frame reused"}, "midpoint": {"source": rel(SOURCE), "sourceSha256": v2.digest(SOURCE), "angleDegrees": 172.5, "registration": registration, "componentChecks": checks, "trouserBootMaskOverlapPixels": overlap}, "frames": records, "earOcclusion": {"frames": [7, 8, 9], "anglesDegrees": [165, 172.5, 180], "farLeftEarSkinPixels": ear_counts}, "animation": {"fps": FPS, "durationSeconds": 1, "cell": list(CELL), "logicalCell": [32, 40], "density": 8, "forward": {"file": rel(forward), "sha256": v2.digest(forward), "sidecar": rel(forward_json), "sidecarSha256": v2.digest(forward_json)}, "reverse": {"file": rel(reverse), "sha256": v2.digest(reverse), "sidecar": rel(reverse_json), "sidecarSha256": v2.digest(reverse_json), "exactFrameOrderReverse": True}}, "reviewSurface": {"publicReview": f"{PUBLIC_ROUTE}/", "publicPage": rel(PUBLIC / "index.html"), "publicPageSha256": v2.digest(PUBLIC / "index.html"), "v7V9EqualDurationComparison": True, "largeAndGameViewsSynchronized": True, "previousNextControls": True}, "evidence": {"contactSheet": {"file": rel(contact), "sha256": v2.digest(contact)}, "changedInterval": {"file": rel(rear), "sha256": v2.digest(rear)}}, "validation": {"allEightV7FramesByteIdentical": retained, "exactlyOneNewFrame": True, "everyFrameFloorY316": all(record["floorY"] == 316 for record in records), "everyFrameTransparentCellEdge": all(record["edgeAlphaPixels"] == 0 for record in records), "midpointTrouserBootMasksDisjoint": overlap == 0, "productionSpritesChanged": False, "runtimeManifestChanged": False, "finalLaneChanged": False, "priorDraftsChanged": False}, "approvalBoundary": {"v9Approved": False, "v7Superseded": False, "v8Reactivated": False, "productionPromotionAllowed": False, "finalLaneEntryAllowed": False}, "nextGate": "Frank compares V7 and V9, especially 165°→172.5°→180°, at large and exact game scale.", "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1–V8, Final and production remain unchanged."}
    v2.dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "frames": len(frames), "retainedV7": retained, "earCounts": ear_counts, "public": register["reviewSurface"]["publicReview"]}, indent=2))


if __name__ == "__main__": main()
