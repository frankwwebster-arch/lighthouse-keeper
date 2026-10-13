#!/usr/bin/env python3
"""Build V3: a full standard-outfit palette correction for the rear endpoint."""
from __future__ import annotations

import colorsys
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_keeper_prime_turn_side_back_v1 as v1
import build_keeper_prime_turn_side_back_v2 as v2


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v3"
PRIOR_PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v2"
PRIOR_REGISTER = PRIOR_PACK / "batch-register.json"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v3"
PUBLIC_ROUTE = "/keeper-review/keeper-prime-turn-side-back-v3"
GENERATED_REFERENCE = PACK / "sources/keeper-prime-back-full-outfit-palette-generated-reference.png"
ANGLES = (90, 98, 105, 120, 135, 150, 165, 180)
CELL = (256, 320)
FPS = 8


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

COMPONENTS = {
    "capCrownBlue": {"y": (15, 63), "kind": "bright-blue", "label": "Cap crown blue"},
    "capBandNavy": {"y": (60, 76), "kind": "navy", "label": "Cap band navy"},
    "jumperBlue": {"y": (82, 205), "kind": "bright-blue", "label": "Jumper blue"},
    "jumperCream": {"y": (115, 170), "kind": "cream", "label": "Jumper cream band"},
    "trouserNavy": {"y": (202, 254), "kind": "navy", "label": "Trouser navy"},
    "bootNavy": {"y": (254, 317), "kind": "navy", "label": "Boot navy"},
}


def component_match(spec: dict, y: int, pixel: tuple[int, int, int, int]) -> bool:
    start, end = spec["y"]
    r, g, b, a = pixel
    if not (start <= y < end and a >= 8):
        return False
    h, s, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if spec["kind"] == "bright-blue":
        return 0.52 <= h <= 0.70 and s >= 0.75 and value >= 0.24 and b - r >= 24
    if spec["kind"] == "navy":
        return 0.53 <= h <= 0.75 and 0.20 <= s <= 0.75 and value >= 0.16 and b - r >= 10
    return s < 0.32 and value > 0.55 and r > g >= b


def pixels_for(image: Image.Image, spec: dict) -> list[tuple[int, int, int, int, int, float, float, float]]:
    output = []
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            if component_match(spec, y, pixel):
                h, s, value = colorsys.rgb_to_hsv(*(channel / 255 for channel in pixel[:3]))
                output.append((x, y, *pixel[:3], h, s, value))
    return output


def quantile(values: list[float], position: float) -> float:
    ordered = sorted(values)
    return ordered[round(position * (len(ordered) - 1))]


def stats(samples: list[tuple[int, int, int, int, int, float, float, float]]) -> dict:
    if len(samples) < 100:
        raise RuntimeError("component mask unexpectedly small")
    channels = {"r": [item[2] for item in samples], "g": [item[3] for item in samples], "b": [item[4] for item in samples], "h": [item[5] for item in samples], "s": [item[6] for item in samples], "v": [item[7] for item in samples]}
    return {
        "pixels": len(samples),
        "medianRGB": [round(quantile(channels[key], 0.5)) for key in ("r", "g", "b")],
        "medianHSV": [round(quantile(channels[key], 0.5), 6) for key in ("h", "s", "v")],
        "hsvP10": [round(quantile(channels[key], 0.1), 6) for key in ("h", "s", "v")],
        "hsvP90": [round(quantile(channels[key], 0.9), 6) for key in ("h", "s", "v")],
    }


def transfer_component(image: Image.Image, reference: Image.Image, spec: dict) -> tuple[Image.Image, Image.Image, Image.Image, dict]:
    source = pixels_for(image, spec)
    target = pixels_for(reference, spec)
    source_stats = stats(source); target_stats = stats(target)
    hue_shift = target_stats["medianHSV"][0] - source_stats["medianHSV"][0]
    saturation_shift = target_stats["medianHSV"][1] - source_stats["medianHSV"][1]
    value_shift = target_stats["medianHSV"][2] - source_stats["medianHSV"][2]
    result = image.copy()
    coverage = Image.new("L", image.size, 0)
    changed = Image.new("L", image.size, 0)
    changed_pixels = 0
    for x, y, r, g, b, h, saturation, value in source:
        coverage.putpixel((x, y), 255)
        mapped_s = max(0, min(1, saturation + saturation_shift))
        mapped_v = max(0, min(1, value + value_shift))
        nr, ng, nb = colorsys.hsv_to_rgb(max(0, min(1, h + hue_shift)), mapped_s, mapped_v)
        updated = (round(nr * 255), round(ng * 255), round(nb * 255), image.getpixel((x, y))[3])
        if updated != image.getpixel((x, y)):
            result.putpixel((x, y), updated)
            changed.putpixel((x, y), 255)
            changed_pixels += 1
    corrected_samples = []
    for x, y, *_ in source:
        r, g, b, _ = result.getpixel((x, y))
        h, s, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        corrected_samples.append((x, y, r, g, b, h, s, value))
    return result, coverage, changed, {"source": source_stats, "target": target_stats, "corrected": stats(corrected_samples), "changedPixels": changed_pixels}


def comparison(reference: Image.Image, prior: Image.Image, corrected: Image.Image, changed: Image.Image) -> Image.Image:
    output = Image.new("RGBA", (4 * CELL[0], 356), (12, 20, 27, 255))
    panels = (reference, prior, corrected, Image.merge("RGBA", (changed, changed, changed, changed)))
    labels = ("F7 palette authority", "F8 V2", "F8 V3 full outfit", "all changed pixels")
    draw = ImageDraw.Draw(output)
    for index, (label, panel) in enumerate(zip(labels, panels)):
        stage = v1.checkerboard(); stage.alpha_composite(panel)
        output.alpha_composite(stage, (index * CELL[0], 36))
        draw.text((index * CELL[0] + 8, 10), label, fill="#ffffff", font=ImageFont.load_default())
    return output


def palette_sheet(palette: dict) -> Image.Image:
    width, height = 1080, 180
    output = Image.new("RGBA", (width, height), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    cell = width // len(COMPONENTS)
    for index, (name, spec) in enumerate(COMPONENTS.items()):
        rgb = tuple(palette["components"][name]["target"]["medianRGB"])
        left = index * cell
        draw.rectangle((left + 12, 34, left + cell - 12, 130), fill=rgb, outline="#ffffff", width=2)
        draw.text((left + 12, 10), spec["label"], fill="#ffffff", font=font)
        draw.text((left + 12, 140), f"RGB {rgb}", fill="#ffffff", font=font)
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


def write_page(frame_paths: list[Path], comparison_path: Path, palette_path: Path, contact_path: Path) -> None:
    records = {f"frame{index + 1}": path for index, path in enumerate(frame_paths)}
    records.update({"comparison": comparison_path, "palette": palette_path, "contact": contact_path})
    urls = copy_public(records)
    asset = lambda key: f"{PUBLIC_ROUTE}/assets/{urls[key]}"
    frames_json = json.dumps([asset(f"frame{index + 1}") for index in range(8)])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side ↔ back Turn V3</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.player{{display:grid;grid-template-columns:minmax(280px,520px) 1fr;gap:24px;align-items:center}}.stage{{aspect-ratio:4/5;max-height:68vh;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px;margin:auto}}.stage img{{width:100%;height:100%;object-fit:contain;image-rendering:auto}}button,input{{font:inherit}}button{{margin:4px;padding:8px 11px}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}@media(max-width:800px){{.player{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/keeper-review/keeper-prime-turn-side-back-v2">← V2</a><h1>Keeper Prime Turn V3 · full standard-outfit palette</h1><span class="status">Full-outfit colour correction · awaiting visual approval</span><p>F1–F7 are exact prior bytes. F8 retains exact geometry and alpha; only registered cap, jumper, cream band, trouser and boot colour pixels have changed. Nothing has entered Final or production.</p></header><main><p class="rule"><strong>Review priority:</strong> watch F7 → F8. The cap, jumper, cream band, trousers and boots should all retain the same established colours as the Keeper becomes fully rear-facing.</p><article class="player"><div class="stage"><img id="player" src="{asset('frame1')}" alt="Animated full-outfit corrected side-to-back turn"></div><div><h2>Corrected V3 loop</h2><p id="mode">Looping side ↔ back</p><div><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="pause">Pause</button></div><label>Frame time <input id="speed" type="range" min="80" max="500" value="125"> <span id="speedValue">125 ms</span></label></div></article><h2>F7/F8 comparison and declared change mask</h2><article><img class="wide" src="{asset('comparison')}" alt="F7 palette authority, F8 V2, corrected F8 V3 and all changed pixels"></article><h2>Draft standard-outfit palette anchors</h2><article><img class="wide" src="{asset('palette')}" alt="Standard outfit component colour anchors"><p>Approval of V3 would also approve these component medians as the palette target for every later standard-uniform animation. Each new batch must provide component masks and deterministic colour checks; pose shading may vary within the registered distribution, but the outfit may not flash darker between frames.</p></article><h2>Corrected eight-frame sequence</h2><article><img class="wide" src="{asset('contact')}" alt="Eight corrected side-to-back turn poses"></article><h2>Approval boundary</h2><article><p>V3 does not alter V1, V2, the approved rear master, Final or production. It is a new review candidate and a draft palette authority only.</p></article></main><script>const frames={frames_json};const img=document.getElementById('player'),mode=document.getElementById('mode'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let timer=null,sequence=[],cursor=0,loop=false;function show(i){{img.src=frames[i];}}function stop(){{if(timer)clearTimeout(timer);timer=null;mode.textContent='Paused';}}function play(seq,repeat,name){{stop();sequence=seq;cursor=0;loop=repeat;mode.textContent=name;const tick=()=>{{show(sequence[cursor]);cursor+=1;if(cursor>=sequence.length){{if(loop)cursor=0;else{{stop();return}}}}timer=setTimeout(tick,Number(speed.value));}};tick();}}document.getElementById('forward').onclick=()=>play([0,1,2,3,4,5,6,7],false,'Side → back');document.getElementById('reverse').onclick=()=>play([7,6,5,4,3,2,1,0],false,'Back → side');document.getElementById('pingpong').onclick=()=>play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');document.getElementById('pause').onclick=stop;speed.oninput=()=>speedValue.textContent=`${{speed.value}} ms`;play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    if not PRIOR_REGISTER.exists() or not GENERATED_REFERENCE.exists():
        raise RuntimeError("required V2 register or generated palette reference missing")
    prior = json.loads(PRIOR_REGISTER.read_text())
    prior_frames = [ROOT / item["file"] for item in prior["frames"]]
    for generated in (PACK / "drafts", PACK / "evidence", PACK / "palette", PUBLIC):
        if generated.exists():
            shutil.rmtree(generated)
    frames = [Image.open(path).convert("RGBA") for path in prior_frames]
    reference = frames[-2]
    original = frames[-1].copy()
    corrected = original.copy()
    palette = {"id": "keeper-standard-outfit-palette-2026-10-13-v1-draft", "status": "draft-awaiting-visual-approval", "authorityFrame": rel(prior_frames[-2]), "authorityFrameSha256": v2.digest(prior_frames[-2]), "components": {}, "futureBatchContract": {"componentMasksRequired": True, "medianHsvTolerance": [0.02, 0.08, 0.02], "noUnmaskedColourChanges": True, "transparentCellGutterRequired": True}}
    mask_dir = PACK / "palette/masks"
    mask_dir.mkdir(parents=True, exist_ok=True)
    changed_union = Image.new("L", CELL, 0)
    coverage_union = Image.new("L", CELL, 0)
    for name, spec in COMPONENTS.items():
        if name == "jumperBlue":
            source = pixels_for(corrected, spec); target = pixels_for(reference, spec)
            coverage = Image.new("L", CELL, 0); changed = Image.new("L", CELL, 0)
            for x, y, *_ in source:
                coverage.putpixel((x, y), 255)
            record = {"source": stats(source), "target": stats(target), "corrected": stats(source), "changedPixels": 0, "disposition": "retained exact V2 pixels because the V2 jumper correction already matches F7"}
        else:
            corrected, coverage, changed, record = transfer_component(corrected, reference, spec)
        coverage_path = mask_dir / f"{name}-coverage.png"
        changed_path = mask_dir / f"{name}-changed.png"
        coverage.save(coverage_path, optimize=False, compress_level=9)
        changed.save(changed_path, optimize=False, compress_level=9)
        coverage_union = Image.frombytes("L", CELL, bytes(max(a, b) for a, b in zip(coverage_union.tobytes(), coverage.tobytes())))
        changed_union = Image.frombytes("L", CELL, bytes(max(a, b) for a, b in zip(changed_union.tobytes(), changed.tobytes())))
        palette["components"][name] = {"label": spec["label"], "coverageMask": rel(coverage_path), "coverageMaskSha256": v2.digest(coverage_path), "changedMask": rel(changed_path), "changedMaskSha256": v2.digest(changed_path), **record}
    coverage_union_path = mask_dir / "standard-outfit-all-components-coverage.png"
    changed_union_path = mask_dir / "standard-outfit-all-components-changed.png"
    coverage_union.save(coverage_union_path, optimize=False, compress_level=9)
    changed_union.save(changed_union_path, optimize=False, compress_level=9)
    palette["coverageUnion"] = {"file": rel(coverage_union_path), "sha256": v2.digest(coverage_union_path)}
    palette["changedUnion"] = {"file": rel(changed_union_path), "sha256": v2.digest(changed_union_path)}
    palette_path = PACK / "palette/keeper-standard-outfit-palette-v1-draft.json"
    v2.dump(palette_path, palette)
    frame_dir = PACK / "drafts/frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    frames[-1] = corrected
    frame_paths = []
    for index, frame in enumerate(frames, start=1):
        path = frame_dir / f"keeper_prime_turn_side-right_to_back_f{index}.png"
        if index < 8:
            shutil.copyfile(prior_frames[index - 1], path)
        else:
            frame.save(path, optimize=False, compress_level=9)
        frame_paths.append(path)
    forward = PACK / "drafts/keeper_prime_turn_side-right_to_back_f8.png"
    reverse = PACK / "drafts/keeper_prime_turn_back_to_side-right_f8.png"
    v1.save_strip(forward, frames); v1.save_strip(reverse, list(reversed(frames)))
    common = {"w": 32, "h": 40, "density": 8, "frames": 8, "fps": FPS, "anchor": [16, 40], "loop": False, "outfit": "standard-single-band", "palette": palette["id"], "status": "draft-awaiting-visual-approval"}
    forward_sidecar = forward.with_suffix(".json"); reverse_sidecar = reverse.with_suffix(".json")
    v2.dump(forward_sidecar, {"name": "keeper_prime_turn_side-right_to_back_v3", **common, "startPose": "standing-side-right", "endPose": "standing-back-full-outfit-palette-candidate", "sha256": v2.digest(forward), "frameFiles": [rel(path) for path in frame_paths]})
    v2.dump(reverse_sidecar, {"name": "keeper_prime_turn_back_to_side-right_v3", **common, "startPose": "standing-back-full-outfit-palette-candidate", "endPose": "standing-side-right", "sha256": v2.digest(reverse), "frameFiles": [rel(path) for path in reversed(frame_paths)], "exactReverseOf": rel(forward)})
    evidence_dir = PACK / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    comparison_path = evidence_dir / "f7-f8-full-outfit-palette-comparison.png"
    contact_path = evidence_dir / "turn-contact-sheet-corrected.png"
    palette_sheet_path = evidence_dir / "standard-outfit-palette-swatches.png"
    comparison(reference, original, corrected, changed_union).save(comparison_path, optimize=False, compress_level=9)
    v1.contact_sheet(frames).save(contact_path, optimize=False, compress_level=9)
    palette_sheet(palette).save(palette_sheet_path, optimize=False, compress_level=9)
    frame_records = []
    for index, (angle, path, frame) in enumerate(zip(ANGLES, frame_paths, frames), start=1):
        bounds = v1.alpha_bounds(frame)
        frame_records.append({"frame": index, "angleDegrees": angle, "file": rel(path), "sha256": v2.digest(path), "sourceV2Sha256": v2.digest(prior_frames[index - 1]), "change": "standard-outfit-palette-only" if index == 8 else "none-byte-identical", "opaqueBoundsExclusive": list(bounds), "opaqueHeight": bounds[3] - bounds[1], "edgeAlphaPixels": v1.edge_alpha_count(frame)})
    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v3",
        "status": "draft-side-back-turn-v3-full-outfit-palette-awaiting-visual-approval",
        "purpose": "Remove all F7→F8 standard-outfit colour jumps and define a reusable palette contract for future standard-uniform animation batches.",
        "priorDraft": {"register": rel(PRIOR_REGISTER), "registerSha256": v2.digest(PRIOR_REGISTER)},
        "generatedPaletteReference": {"file": rel(GENERATED_REFERENCE), "sha256": v2.digest(GENERATED_REFERENCE), "disposition": "colour evidence only; rejected as geometry because it redrew the Keeper"},
        "palette": {"file": rel(palette_path), "sha256": v2.digest(palette_path), "status": palette["status"]},
        "frames": frame_records,
        "animation": {"fps": FPS, "cell": list(CELL), "forward": {"file": rel(forward), "sha256": v2.digest(forward), "sidecar": rel(forward_sidecar), "sidecarSha256": v2.digest(forward_sidecar)}, "reverse": {"file": rel(reverse), "sha256": v2.digest(reverse), "sidecar": rel(reverse_sidecar), "sidecarSha256": v2.digest(reverse_sidecar), "exactFrameOrderReverse": True}},
        "evidence": {"comparison": {"file": rel(comparison_path), "sha256": v2.digest(comparison_path)}, "paletteSwatches": {"file": rel(palette_sheet_path), "sha256": v2.digest(palette_sheet_path)}, "contactSheet": {"file": rel(contact_path), "sha256": v2.digest(contact_path)}},
        "validation": {"frames1To7ByteIdenticalToV2": True, "frame8AlphaByteIdenticalToV2": corrected.getchannel("A").tobytes() == original.getchannel("A").tobytes(), "frame8GeometryUnchanged": v1.alpha_bounds(corrected) == v1.alpha_bounds(original), "frame8OnlyRegisteredOutfitPixelsChanged": True, "everyFrameTransparentCellEdge": all(item["edgeAlphaPixels"] == 0 for item in frame_records), "productionSpritesChanged": False, "runtimeManifestChanged": False, "approvedBackMasterChanged": False, "priorDraftsChanged": False},
        "approvalBoundary": {"sideBackTurnV3Approved": False, "standardOutfitPaletteApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank reviews F7→F8 full-outfit colour continuity and the proposed reusable standard-outfit palette anchors.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1/V2, approved authorities and production remain unchanged.",
    }
    v2.dump(PACK / "batch-register.json", register)
    write_page(frame_paths, comparison_path, palette_sheet_path, contact_path)
    print(json.dumps({"batch": register["batchId"], "changedPixels": sum(1 for value in changed_union.tobytes() if value), "components": {name: {"fromV": item["source"]["medianHSV"][2], "toV": item["corrected"]["medianHSV"][2], "targetV": item["target"]["medianHSV"][2]} for name, item in palette["components"].items()}, "public": rel(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
