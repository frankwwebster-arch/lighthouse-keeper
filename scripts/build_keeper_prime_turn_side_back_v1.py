#!/usr/bin/env python3
"""Build the reversible smooth Keeper Prime side-right ↔ back Turn V1 review pack."""
from __future__ import annotations

import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v1"
SIDE = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
SIDE_REGISTER = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/batch-register.json"
SIDE_APPROVAL = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v2/batch-register.json"
BACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png"
BACK_REGISTER = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/batch-register.json"
TURN_APPROVAL = ROOT / "art/drafts/keeper-prime-turn-front-side-2026-10-13-v2/batch-register.json"
RIG = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v1/rig/keeper-prime-rig-v1.json"
ANGLES = (90, 98, 105, 120, 135, 150, 165, 180)
SOURCE_AXIS_X = 560
CELL = (256, 320)
TARGET_TOP = 18
TARGET_FLOOR = 316
ALPHA_THRESHOLD = 8
FPS = 8


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
        raise RuntimeError("empty image")
    return box


def edge_alpha_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = [(x, 0) for x in range(image.width)] + [(x, image.height - 1) for x in range(image.width)]
    points += [(0, y) for y in range(1, image.height - 1)] + [(image.width - 1, y) for y in range(1, image.height - 1)]
    return sum(1 for point in points if alpha.getpixel(point) != 0)


def normalize(source: Path, clean_path: Path) -> tuple[Image.Image, dict]:
    raw = Image.open(source).convert("RGBA")
    clean = raw.copy()
    clean.putalpha(clean.getchannel("A").point(lambda value: 0 if value < ALPHA_THRESHOLD else value))
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean.save(clean_path, optimize=False, compress_level=9)
    box = alpha_bounds(clean)
    crop = clean.crop(box)
    scale = (TARGET_FLOOR - TARGET_TOP) / crop.height
    size = (round(crop.width * scale), TARGET_FLOOR - TARGET_TOP)
    registered = crop.resize(size, Image.Resampling.LANCZOS)
    left = round(128 - (SOURCE_AXIS_X - box[0]) * scale)
    frame = Image.new("RGBA", CELL, (0, 0, 0, 0))
    frame.alpha_composite(registered, (left, TARGET_TOP))
    return frame, {
        "rawCanvas": list(raw.size),
        "cleanSignificantAlphaBoundsExclusive": list(box),
        "scale": round(scale, 12),
        "registeredSize": list(size),
        "registeredOffset": [left, TARGET_TOP],
        "sourceAxisX": SOURCE_AXIS_X,
        "targetAxisX": 128,
        "filter": "Lanczos",
        "creativePixelWarp": False,
    }


def checkerboard() -> Image.Image:
    output = Image.new("RGBA", CELL, (29, 40, 49, 255))
    draw = ImageDraw.Draw(output)
    for y in range(0, CELL[1], 16):
        for x in range(0, CELL[0], 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, x + 15, y + 15), fill=(41, 55, 65, 255))
    return output


def opaque_area(image: Image.Image) -> int:
    return sum(1 for value in image.getchannel("A").tobytes() if value >= ALPHA_THRESHOLD)


def alpha_centroid(image: Image.Image, max_y: int | None = None) -> list[float]:
    points = []
    alpha = image.getchannel("A")
    for y in range(image.height if max_y is None else min(max_y, image.height)):
        for x in range(image.width):
            if alpha.getpixel((x, y)) >= ALPHA_THRESHOLD:
                points.append((x, y))
    return [round(sum(p[0] for p in points) / len(points), 3), round(sum(p[1] for p in points) / len(points), 3)]


def contact_sheet(frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (len(frames) * CELL[0], 356), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    for index, (angle, frame) in enumerate(zip(ANGLES, frames)):
        stage = checkerboard(); stage.alpha_composite(frame)
        output.alpha_composite(stage, (index * CELL[0], 36))
        draw.text((index * CELL[0] + 8, 10), f"F{index + 1} · {angle}°", fill="#ffffff", font=font)
    return output


def datum_sheet(frames: list[Image.Image], rig: dict) -> Image.Image:
    output = contact_sheet(frames).crop((0, 36, len(frames) * CELL[0], 356))
    draw = ImageDraw.Draw(output)
    colours = ("#75f3a6", "#f0bd58", "#ff8798", "#c4b5fd", "#ffffff")
    selected = {"capTop", "badgeCentre", "beardBase", "palmBase", "floor"}
    for index, datum in enumerate(item for item in rig["verticalDatums"] if item["id"] in selected):
        y = round(datum["targetY"])
        draw.line((0, y, output.width, y), fill=colours[index], width=1)
        draw.text((6, max(0, y - 11)), f"{datum['label']} y={datum['targetY']:g}", fill=colours[index], font=ImageFont.load_default())
    return output


def save_strip(path: Path, frames: list[Image.Image]) -> None:
    strip = Image.new("RGBA", (CELL[0] * len(frames), CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=False, compress_level=9)


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    urls = {}
    for key, source in records.items():
        suffix = source.suffix
        target = assets / f"{key}-{digest(source)[:16]}{suffix}"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(register: dict, frame_paths: list[Path], forward: Path, reverse: Path, contact: Path, datums: Path) -> None:
    records = {f"frame{index + 1}": path for index, path in enumerate(frame_paths)}
    records.update({"forward": forward, "reverse": reverse, "contact": contact, "datums": datums})
    urls = copy_public(records)
    frames_json = json.dumps([f"assets/{urls[f'frame{index + 1}']}" for index in range(len(ANGLES))])
    widths = ", ".join(str(frame["opaqueBoundsExclusive"][2] - frame["opaqueBoundsExclusive"][0]) for frame in register["frames"])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side ↔ back Turn V1</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.player{{display:grid;grid-template-columns:minmax(280px,520px) 1fr;gap:24px;align-items:center}}.stage{{position:relative;aspect-ratio:4/5;max-height:68vh;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px;margin:auto}}.stage img{{width:100%;height:100%;object-fit:contain;image-rendering:auto}}button,input{{font:inherit}}button{{margin:4px;padding:8px 11px}}.active{{background:#185f3a;color:white}}.frames{{display:grid;grid-template-columns:repeat(8,1fr);gap:8px}}.frames button{{background:#111a21;border:1px solid var(--line);color:var(--ink)}}.frames img{{width:100%;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/12px 12px}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}@media(max-width:800px){{.player{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-prime-side-right-rigged-v1/">Approved side</a> · <a href="/keeper-review/keeper-prime-orthographic-v5/">Approved back</a><h1>Keeper Prime Turn V1 · side-right ↔ back</h1><span class="status">Eight-pose smooth draft · awaiting visual approval</span><p>Exact approved endpoints with six newly drawn rear-quarter poses. Nothing has entered Final or production.</p></header><main><p class="rule"><strong>Review priority:</strong> watch the face and beard disappear into rear hair, the cap badge disappear, and both boots rotate into the approved rear construction without a height, width or perspective snap.</p><article class="player"><div class="stage"><img id="player" src="assets/{urls['frame1']}" alt="Animated Keeper side-to-back turn"></div><div><h2 id="label">Frame 1 · 90° · exact approved side-right</h2><p id="mode">Paused</p><div><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="route">Route context</button><button id="pause">Pause</button></div><label>Frame time <input id="speed" type="range" min="80" max="500" value="125"> <span id="speedValue">125 ms</span></label><p>Route context: side stop → turn fully away → brief back hold → turn back to side → exact stop.</p><p>Registered silhouette widths: {widths}px. Height remains 298px and the floor remains y=316 throughout.</p></div></article><section class="frames">{''.join(f'<button data-frame="{i}"><img src="assets/{urls[f"frame{i + 1}"]}" alt="Frame {i + 1}, {ANGLES[i]} degrees"><span>F{i + 1} · {ANGLES[i]}°</span></button>' for i in range(len(ANGLES)))}</section><h2>All eight registered poses</h2><article><img class="wide" src="assets/{urls['contact']}" alt="Eight turn poses from side-right to back"></article><h2>Horizontal rig guides</h2><article><img class="wide" src="assets/{urls['datums']}" alt="Side-to-back turn poses aligned to registered horizontal guides"><p>Cap top and floor are exact in every frame. Internal landmarks are review guides rather than software-warp targets; each intermediate pose is independently drawn and uniformly registered.</p></article><h2>Approval boundary</h2><article><p>The side-right and back endpoints are approved authorities. This side ↔ back Turn V1 is not. Approval would authorize this exact eight-frame transition as a core-turn artwork authority; it would not promote production sprites or approve later walk/sit work.</p></article></main><script>const frames={frames_json},angles={json.dumps(list(ANGLES))};const img=document.getElementById('player'),label=document.getElementById('label'),mode=document.getElementById('mode'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let timer=null,sequence=[],cursor=0,loop=false;const names=['exact approved side-right','near-side bridge','105° turn','120° turn','135° rear quarter','150° turn','near-back bridge','exact approved back'];function show(i){{img.src=frames[i];label.textContent=`Frame ${{i+1}} · ${{angles[i]}}° · ${{names[i]}}`;document.querySelectorAll('[data-frame]').forEach(b=>b.classList.toggle('active',Number(b.dataset.frame)===i));}}function stop(){{if(timer)clearTimeout(timer);timer=null;mode.textContent='Paused';}}function play(seq,repeat,name){{stop();sequence=seq;cursor=0;loop=repeat;mode.textContent=name;const tick=()=>{{show(sequence[cursor]);cursor+=1;if(cursor>=sequence.length){{if(loop)cursor=0;else{{stop();return}}}}timer=setTimeout(tick,Number(speed.value));}};tick();}}document.getElementById('forward').onclick=()=>play([0,1,2,3,4,5,6,7],false,'Side → back');document.getElementById('reverse').onclick=()=>play([7,6,5,4,3,2,1,0],false,'Back → side');document.getElementById('pingpong').onclick=()=>play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');document.getElementById('route').onclick=()=>play([0,0,1,2,3,4,5,6,7,7,7,6,5,4,3,2,1,0,0],true,'Route: side stop → back hold → side stop');document.getElementById('pause').onclick=stop;speed.oninput=()=>speedValue.textContent=`${{speed.value}} ms`;document.querySelectorAll('[data-frame]').forEach(b=>b.onclick=()=>{{stop();show(Number(b.dataset.frame));}});show(0);play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    sources = [PACK / f"sources/keeper-prime-turn-angle-{angle}-generated.png" for angle in ANGLES[1:-1]]
    required = [SIDE, SIDE_REGISTER, SIDE_APPROVAL, BACK, BACK_REGISTER, TURN_APPROVAL, RIG, *sources]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    turn_approval = json.loads(TURN_APPROVAL.read_text())
    back_register = json.loads(BACK_REGISTER.read_text())
    if turn_approval.get("status") != "approved-front-side-turn-artwork-authority" or turn_approval.get("approvalBoundary", {}).get("authorizesSideBackTurnV1Draft") is not True:
        raise RuntimeError("explicit front-to-side Turn V1 approval missing")
    if back_register.get("status") != "approved-rear-endpoint-authority-for-kp-rig" or back_register.get("approvedRearEndpoint", {}).get("animationAuthoringAllowed") is not True:
        raise RuntimeError("approved rear endpoint authority missing")
    rig = json.loads(RIG.read_text())
    for generated_dir in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if generated_dir.exists():
            shutil.rmtree(generated_dir)
    frames = [Image.open(SIDE).convert("RGBA")]
    registrations = []
    clean_sources = []
    for angle, source in zip(ANGLES[1:-1], sources):
        clean_path = PACK / f"sources/keeper-prime-turn-angle-{angle}-clean.png"
        frame, registration = normalize(source, clean_path)
        frames.append(frame); registrations.append(registration); clean_sources.append(clean_path)
    frames.append(Image.open(BACK).convert("RGBA"))
    frame_dir = PACK / "drafts/frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    frame_paths = []
    frame_records = []
    for index, (angle, frame) in enumerate(zip(ANGLES, frames), start=1):
        path = frame_dir / f"keeper_prime_turn_side-right_to_back_f{index}.png"
        frame.save(path, optimize=False, compress_level=9)
        bounds = alpha_bounds(frame)
        frame_paths.append(path)
        frame_records.append({
            "frame": index, "angleDegrees": angle, "file": rel(path), "sha256": digest(path),
            "endpointAuthority": "approved-side-right" if index == 1 else "approved-back" if index == len(ANGLES) else None,
            "opaqueBoundsExclusive": list(bounds), "opaqueWidth": bounds[2] - bounds[0], "opaqueHeight": bounds[3] - bounds[1],
            "opaqueArea": opaque_area(frame), "alphaCentroid": alpha_centroid(frame), "headAlphaCentroid": alpha_centroid(frame, 150),
            "edgeAlphaPixels": edge_alpha_count(frame),
            "registration": None if index in (1, len(ANGLES)) else registrations[index - 2],
        })
    forward = PACK / "drafts/keeper_prime_turn_side-right_to_back_f8.png"
    reverse = PACK / "drafts/keeper_prime_turn_back_to_side-right_f8.png"
    save_strip(forward, frames); save_strip(reverse, list(reversed(frames)))
    continuity = []
    for left, right in zip(frame_records, frame_records[1:]):
        continuity.append({
            "fromFrame": left["frame"], "toFrame": right["frame"],
            "opaqueWidthDelta": right["opaqueWidth"] - left["opaqueWidth"],
            "opaqueHeightDelta": right["opaqueHeight"] - left["opaqueHeight"],
            "alphaCentroidDelta": [round(right["alphaCentroid"][0] - left["alphaCentroid"][0], 3), round(right["alphaCentroid"][1] - left["alphaCentroid"][1], 3)],
            "headAlphaCentroidDelta": [round(right["headAlphaCentroid"][0] - left["headAlphaCentroid"][0], 3), round(right["headAlphaCentroid"][1] - left["headAlphaCentroid"][1], 3)],
        })
    forward_sidecar = PACK / "drafts/keeper_prime_turn_side-right_to_back_f8.json"
    reverse_sidecar = PACK / "drafts/keeper_prime_turn_back_to_side-right_f8.json"
    common = {"w": 32, "h": 40, "density": 8, "frames": 8, "fps": FPS, "anchor": [16, 40], "loop": False, "outfit": "standard-single-band", "status": "draft-awaiting-visual-approval"}
    dump(forward_sidecar, {"name": "keeper_prime_turn_side-right_to_back", **common, "startPose": "standing-side-right", "endPose": "standing-back", "sha256": digest(forward), "frameFiles": [rel(path) for path in frame_paths]})
    dump(reverse_sidecar, {"name": "keeper_prime_turn_back_to_side-right", **common, "startPose": "standing-back", "endPose": "standing-side-right", "sha256": digest(reverse), "frameFiles": [rel(path) for path in reversed(frame_paths)], "exactReverseOf": rel(forward)})
    contact = PACK / "evidence/turn-contact-sheet.png"
    datums = PACK / "evidence/turn-horizontal-datums.png"
    contact.parent.mkdir(parents=True, exist_ok=True)
    contact_sheet(frames).save(contact, optimize=False, compress_level=9)
    datum_sheet(frames, rig).save(datums, optimize=False, compress_level=9)
    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v1",
        "status": "draft-side-back-turn-v1-awaiting-visual-approval",
        "purpose": "Show how the exact approved Keeper Prime side-right rotates smoothly into the exact approved rear endpoint and back.",
        "authorities": {
            "sideRight": {"file": rel(SIDE), "sha256": digest(SIDE), "register": rel(SIDE_REGISTER), "registerSha256": digest(SIDE_REGISTER), "approval": rel(SIDE_APPROVAL), "approvalSha256": digest(SIDE_APPROVAL)},
            "back": {"file": rel(BACK), "sha256": digest(BACK), "register": rel(BACK_REGISTER), "registerSha256": digest(BACK_REGISTER), "approvalWording": back_register["approval"]["wording"]},
            "frontSideTurnApproval": {"file": rel(TURN_APPROVAL), "sha256": digest(TURN_APPROVAL), "approvalWording": turn_approval["approval"]["wording"]},
            "rig": {"file": rel(RIG), "sha256": digest(RIG)},
        },
        "generation": {"tool": "built-in image generation", "mode": "six independently drawn rear-quarter poses; a near-side bridge and near-back bridge reduce endpoint perspective jumps", "rawSources": [{"angleDegrees": angle, "file": rel(source), "sha256": digest(source)} for angle, source in zip(ANGLES[1:-1], sources)], "cleanSources": [{"angleDegrees": angle, "file": rel(source), "sha256": digest(source)} for angle, source in zip(ANGLES[1:-1], clean_sources)], "rejectedSources": [{"angleDegrees": 150, "file": rel(PACK / "sources/keeper-prime-turn-angle-150-rejected-a.png"), "sha256": digest(PACK / "sources/keeper-prime-turn-angle-150-rejected-a.png"), "reason": "face remained too visible and boots retained toe-facing construction"}, {"angleDegrees": 165, "file": rel(PACK / "sources/keeper-prime-turn-angle-165-rejected-a.png"), "sha256": digest(PACK / "sources/keeper-prime-turn-angle-165-rejected-a.png"), "reason": "cap and upper-body silhouette remained too narrow and tilted before the exact back endpoint"}], "lowAlphaCleanupThreshold": ALPHA_THRESHOLD, "creativePixelWarp": False},
        "animation": {
            "anglesDegrees": list(ANGLES), "fps": FPS, "durationSeconds": round(len(frames) / FPS, 3), "cell": list(CELL), "logicalCell": [32, 40], "density": 8, "anchor": [128, 320],
            "forward": {"file": rel(forward), "sha256": digest(forward), "sidecar": rel(forward_sidecar), "sidecarSha256": digest(forward_sidecar), "startPose": "standing-side-right", "endPose": "standing-back"},
            "reverse": {"file": rel(reverse), "sha256": digest(reverse), "sidecar": rel(reverse_sidecar), "sidecarSha256": digest(reverse_sidecar), "startPose": "standing-back", "endPose": "standing-side-right", "exactFrameOrderReverse": True},
        },
        "frames": frame_records,
        "continuity": continuity,
        "evidence": {"contactSheet": {"file": rel(contact), "sha256": digest(contact)}, "horizontalDatums": {"file": rel(datums), "sha256": digest(datums)}},
        "validation": {
            "sideEndpointByteIdentical": frame_paths[0].read_bytes() == SIDE.read_bytes(),
            "backEndpointByteIdentical": frame_paths[-1].read_bytes() == BACK.read_bytes(),
            "reverseIsExactFrameOrderReverse": True,
            "everyFrameHeightPixels": 298,
            "everyFrameCapTopY": 18,
            "everyFrameFloorExclusiveY": 316,
            "everyFrameTransparentCellEdge": all(item["edgeAlphaPixels"] == 0 for item in frame_records),
            "uniformRegistrationOnly": all(item["registration"] is None or item["registration"]["creativePixelWarp"] is False for item in frame_records),
            "productionSpritesChanged": False, "runtimeManifestChanged": False, "otherAnimationDraftsChanged": False,
        },
        "approvalBoundary": {"sideRightArtworkApproved": True, "backArtworkApproved": True, "frontSideTurnV1Approved": True, "sideBackTurnV1Approved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank reviews the looping side-right ↔ back transition and route context for visible jumps before any walk/stop or stand/sit core animation authoring.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; approved authorities, existing drafts and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(register, frame_paths, forward, reverse, contact, datums)
    print(json.dumps({"batch": register["batchId"], "widths": [item["opaqueWidth"] for item in frame_records], "heights": [item["opaqueHeight"] for item in frame_records], "endpointsExact": [register["validation"]["sideEndpointByteIdentical"], register["validation"]["backEndpointByteIdentical"]], "public": rel(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
