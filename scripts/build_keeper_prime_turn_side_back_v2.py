#!/usr/bin/env python3
"""Build the reversible V2 side/back turn with a jumper-only F8 colour correction."""
from __future__ import annotations

import bisect
import colorsys
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_keeper_prime_turn_side_back_v1 as v1


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v2"
PRIOR_PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v1"
PRIOR_REGISTER = PRIOR_PACK / "batch-register.json"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v2"
PUBLIC_ROUTE = "/keeper-review/keeper-prime-turn-side-back-v2"
GENERATED_REFERENCE = PACK / "sources/keeper-prime-back-bright-jumper-generated-reference.png"
ANGLES = (90, 98, 105, 120, 135, 150, 165, 180)
CELL = (256, 320)
FPS = 8


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def is_jumper_blue(x: int, y: int, pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    if not (84 <= y <= 204 and a >= 8 and b - r >= 24):
        return False
    h, s, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return 0.52 <= h <= 0.70 and s >= 0.55 and value >= 0.24


def jumper_samples(image: Image.Image) -> tuple[list[float], list[float], list[float]]:
    hues, saturations, values = [], [], []
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            if is_jumper_blue(x, y, pixel):
                h, s, value = colorsys.rgb_to_hsv(*(channel / 255 for channel in pixel[:3]))
                hues.append(h); saturations.append(s); values.append(value)
    return sorted(hues), sorted(saturations), sorted(values)


def median(items: list[float]) -> float:
    return items[len(items) // 2]


def recolour_jumper(target: Image.Image, reference: Image.Image) -> tuple[Image.Image, Image.Image, dict]:
    source_h, source_s, source_v = jumper_samples(target)
    target_h, target_s, target_v = jumper_samples(reference)
    if min(len(source_v), len(target_v)) < 1000:
        raise RuntimeError("jumper colour masks are unexpectedly small")
    hue_shift = median(target_h) - median(source_h)
    saturation_shift = median(target_s) - median(source_s)
    result = target.copy()
    mask = Image.new("L", target.size, 0)
    changed = 0
    for y in range(target.height):
        for x in range(target.width):
            r, g, b, a = target.getpixel((x, y))
            if not is_jumper_blue(x, y, (r, g, b, a)):
                continue
            h, s, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            quantile = bisect.bisect_left(source_v, value) / max(1, len(source_v) - 1)
            mapped_value = target_v[round(quantile * (len(target_v) - 1))]
            nr, ng, nb = colorsys.hsv_to_rgb(max(0, min(1, h + hue_shift)), max(0, min(1, s + saturation_shift)), mapped_value)
            updated = (round(nr * 255), round(ng * 255), round(nb * 255), a)
            if updated != (r, g, b, a):
                result.putpixel((x, y), updated)
                mask.putpixel((x, y), 255)
                changed += 1
    return result, mask, {
        "changedPixels": changed,
        "referenceJumperPixels": len(target_v),
        "originalJumperPixels": len(source_v),
        "referenceMedianHSV": [round(median(target_h), 6), round(median(target_s), 6), round(median(target_v), 6)],
        "originalMedianHSV": [round(median(source_h), 6), round(median(source_s), 6), round(median(source_v), 6)],
        "correctedMedianHSV": [round(median(jumper_samples(result)[i]), 6) for i in range(3)],
        "method": "jumper-mask HSV quantile transfer from F7; alpha and non-mask pixels retained exactly",
    }


def comparison(original: Image.Image, corrected: Image.Image, reference: Image.Image, mask: Image.Image) -> Image.Image:
    output = Image.new("RGBA", (4 * CELL[0], 356), (12, 20, 27, 255))
    labels = ("F7 colour reference", "F8 original", "F8 corrected", "changed-pixel mask")
    panels = (reference, original, corrected, Image.merge("RGBA", (mask, mask, mask, mask)))
    draw = ImageDraw.Draw(output)
    for index, (label, panel) in enumerate(zip(labels, panels)):
        stage = v1.checkerboard(); stage.alpha_composite(panel)
        output.alpha_composite(stage, (index * CELL[0], 36))
        draw.text((index * CELL[0] + 8, 10), label, fill="#ffffff", font=ImageFont.load_default())
    return output


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    urls = {}
    for key, source in records.items():
        target = assets / f"{key}-{digest(source)[:16]}{source.suffix}"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(frame_paths: list[Path], comparison_path: Path, contact_path: Path) -> None:
    records = {f"frame{index + 1}": path for index, path in enumerate(frame_paths)}
    records.update({"comparison": comparison_path, "contact": contact_path})
    urls = copy_public(records)
    asset = lambda key: f"{PUBLIC_ROUTE}/assets/{urls[key]}"
    frames_json = json.dumps([asset(f"frame{index + 1}") for index in range(8)])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side ↔ back Turn V2</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.player{{display:grid;grid-template-columns:minmax(280px,520px) 1fr;gap:24px;align-items:center}}.stage{{aspect-ratio:4/5;max-height:68vh;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px;margin:auto}}.stage img{{width:100%;height:100%;object-fit:contain;image-rendering:auto}}button,input{{font:inherit}}button{{margin:4px;padding:8px 11px}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}@media(max-width:800px){{.player{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/keeper-review/keeper-prime-turn-side-back-v1">← V1</a><h1>Keeper Prime Turn V2 · F8 jumper-colour correction</h1><span class="status">Jumper-only amendment · awaiting visual approval</span><p>F1–F7 are exact V1 copies. F8 retains the exact V1 geometry and alpha; only masked blue jumper pixels have changed. Nothing has entered Final or production.</p></header><main><p class="rule"><strong>Review priority:</strong> watch F7 → F8. The blue jumper should no longer darken as the Keeper reaches the exact rear pose.</p><article class="player"><div class="stage"><img id="player" src="{asset('frame1')}" alt="Animated corrected side-to-back turn"></div><div><h2 id="label">Corrected V2 loop</h2><p id="mode">Looping side ↔ back</p><div><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="pause">Pause</button></div><label>Frame time <input id="speed" type="range" min="80" max="500" value="125"> <span id="speedValue">125 ms</span></label></div></article><h2>Colour and mask evidence</h2><article><img class="wide" src="{asset('comparison')}" alt="F7 reference, original F8, corrected F8 and jumper-only changed-pixel mask"></article><h2>Corrected eight-frame sequence</h2><article><img class="wide" src="{asset('contact')}" alt="Eight corrected side-to-back turn poses"></article><h2>Approval boundary</h2><article><p>V2 does not alter the approved back master or V1. Approval would accept this corrected F8 as the colour-consistent endpoint candidate for the side/back turn; production promotion remains separate.</p></article></main><script>const frames={frames_json};const img=document.getElementById('player'),mode=document.getElementById('mode'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let timer=null,sequence=[],cursor=0,loop=false;function show(i){{img.src=frames[i];}}function stop(){{if(timer)clearTimeout(timer);timer=null;mode.textContent='Paused';}}function play(seq,repeat,name){{stop();sequence=seq;cursor=0;loop=repeat;mode.textContent=name;const tick=()=>{{show(sequence[cursor]);cursor+=1;if(cursor>=sequence.length){{if(loop)cursor=0;else{{stop();return}}}}timer=setTimeout(tick,Number(speed.value));}};tick();}}document.getElementById('forward').onclick=()=>play([0,1,2,3,4,5,6,7],false,'Side → back');document.getElementById('reverse').onclick=()=>play([7,6,5,4,3,2,1,0],false,'Back → side');document.getElementById('pingpong').onclick=()=>play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');document.getElementById('pause').onclick=stop;speed.oninput=()=>speedValue.textContent=`${{speed.value}} ms`;play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    if not PRIOR_REGISTER.exists() or not GENERATED_REFERENCE.exists():
        raise RuntimeError("required V1 register or generated colour reference is missing")
    prior = json.loads(PRIOR_REGISTER.read_text())
    prior_frames = [ROOT / item["file"] for item in prior["frames"]]
    for generated in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if generated.exists():
            shutil.rmtree(generated)
    frame_dir = PACK / "drafts/frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    frames = [Image.open(path).convert("RGBA") for path in prior_frames]
    original_f8 = frames[-1].copy()
    corrected_f8, jumper_mask, colour = recolour_jumper(original_f8, frames[-2])
    frames[-1] = corrected_f8
    frame_paths = []
    for index, frame in enumerate(frames, start=1):
        path = frame_dir / f"keeper_prime_turn_side-right_to_back_f{index}.png"
        if index < 8:
            shutil.copyfile(prior_frames[index - 1], path)
        else:
            frame.save(path, optimize=False, compress_level=9)
        frame_paths.append(path)
    mask_path = PACK / "drafts/masks/keeper_prime_turn_f8_jumper_changed_pixels.png"
    mask_path.parent.mkdir(parents=True, exist_ok=True)
    jumper_mask.save(mask_path, optimize=False, compress_level=9)
    forward = PACK / "drafts/keeper_prime_turn_side-right_to_back_f8.png"
    reverse = PACK / "drafts/keeper_prime_turn_back_to_side-right_f8.png"
    v1.save_strip(forward, frames); v1.save_strip(reverse, list(reversed(frames)))
    common = {"w": 32, "h": 40, "density": 8, "frames": 8, "fps": FPS, "anchor": [16, 40], "loop": False, "outfit": "standard-single-band", "status": "draft-awaiting-visual-approval"}
    forward_sidecar = forward.with_suffix(".json"); reverse_sidecar = reverse.with_suffix(".json")
    dump(forward_sidecar, {"name": "keeper_prime_turn_side-right_to_back_v2", **common, "startPose": "standing-side-right", "endPose": "standing-back-colour-corrected-candidate", "sha256": digest(forward), "frameFiles": [rel(path) for path in frame_paths]})
    dump(reverse_sidecar, {"name": "keeper_prime_turn_back_to_side-right_v2", **common, "startPose": "standing-back-colour-corrected-candidate", "endPose": "standing-side-right", "sha256": digest(reverse), "frameFiles": [rel(path) for path in reversed(frame_paths)], "exactReverseOf": rel(forward)})
    contact_path = PACK / "evidence/turn-contact-sheet-corrected.png"
    comparison_path = PACK / "evidence/f7-f8-jumper-colour-comparison.png"
    contact_path.parent.mkdir(parents=True, exist_ok=True)
    v1.contact_sheet(frames).save(contact_path, optimize=False, compress_level=9)
    comparison(original_f8, corrected_f8, frames[-2], jumper_mask).save(comparison_path, optimize=False, compress_level=9)
    records = []
    for index, (angle, path, frame) in enumerate(zip(ANGLES, frame_paths, frames), start=1):
        bounds = v1.alpha_bounds(frame)
        records.append({"frame": index, "angleDegrees": angle, "file": rel(path), "sha256": digest(path), "opaqueBoundsExclusive": list(bounds), "opaqueWidth": bounds[2] - bounds[0], "opaqueHeight": bounds[3] - bounds[1], "edgeAlphaPixels": v1.edge_alpha_count(frame), "sourceV1Sha256": digest(prior_frames[index - 1]), "change": "jumper-colour-only" if index == 8 else "none-byte-identical"})
    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v2",
        "status": "draft-side-back-turn-v2-jumper-colour-correction-awaiting-visual-approval",
        "purpose": "Remove the visible F7→F8 jumper-darkening jump without altering the approved rear master or any V1 artifact.",
        "priorDraft": {"register": rel(PRIOR_REGISTER), "registerSha256": digest(PRIOR_REGISTER)},
        "generatedColourReference": {"file": rel(GENERATED_REFERENCE), "sha256": digest(GENERATED_REFERENCE), "disposition": "colour evidence only; rejected as geometry because it redrew the Keeper"},
        "colourCorrection": {**colour, "mask": rel(mask_path), "maskSha256": digest(mask_path), "geometrySource": rel(prior_frames[-1]), "colourReference": rel(prior_frames[-2]), "capChanged": False, "creamStripeChanged": False},
        "frames": records,
        "animation": {"fps": FPS, "cell": list(CELL), "forward": {"file": rel(forward), "sha256": digest(forward), "sidecar": rel(forward_sidecar), "sidecarSha256": digest(forward_sidecar)}, "reverse": {"file": rel(reverse), "sha256": digest(reverse), "sidecar": rel(reverse_sidecar), "sidecarSha256": digest(reverse_sidecar), "exactFrameOrderReverse": True}},
        "evidence": {"comparison": {"file": rel(comparison_path), "sha256": digest(comparison_path)}, "contactSheet": {"file": rel(contact_path), "sha256": digest(contact_path)}},
        "validation": {"frames1To7ByteIdenticalToV1": True, "frame8AlphaByteIdenticalToV1": corrected_f8.getchannel("A").tobytes() == original_f8.getchannel("A").tobytes(), "frame8GeometryUnchanged": v1.alpha_bounds(corrected_f8) == v1.alpha_bounds(original_f8), "frame8OnlyMaskPixelsChanged": True, "everyFrameTransparentCellEdge": all(item["edgeAlphaPixels"] == 0 for item in records), "productionSpritesChanged": False, "runtimeManifestChanged": False, "approvedBackMasterChanged": False, "priorDraftChanged": False},
        "approvalBoundary": {"sideBackTurnV2Approved": False, "backMasterApprovalChanged": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank visually reviews the F7→F8 jumper colour continuity before V2 can become the side/back turn authority.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1, approved authorities and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(frame_paths, comparison_path, contact_path)
    print(json.dumps({"batch": register["batchId"], "changedPixels": colour["changedPixels"], "medianValue": {"f7": colour["referenceMedianHSV"][2], "f8Original": colour["originalMedianHSV"][2], "f8Corrected": colour["correctedMedianHSV"][2]}, "public": rel(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
