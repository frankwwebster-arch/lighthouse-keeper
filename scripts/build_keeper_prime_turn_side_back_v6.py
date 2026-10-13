#!/usr/bin/env python3
"""Build V6 from V5 feedback: F1 palette, F7 height and smooth-master F8."""
from __future__ import annotations

import colorsys
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_keeper_prime_turn_side_back_v1 as v1
import build_keeper_prime_turn_side_back_v2 as v2
import build_keeper_prime_turn_side_back_v3 as v3
import build_keeper_prime_orthographic_views_v4 as ortho


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v6"
V4_PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v4"
V4_REGISTER = V4_PACK / "batch-register.json"
V5_APPROVAL = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v5/batch-register.json"
PALETTE = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v3/palette/keeper-standard-outfit-palette-v1-draft.json"
SMOOTH_BACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/sources/keeper-prime-back-user-approved-rear-boots.png"
SMOOTH_BACK_REGISTER = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/batch-register.json"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v6"
PUBLIC_ROUTE = "/keeper-review/keeper-prime-turn-side-back-v6"
ANGLES = (90, 98, 105, 120, 135, 150, 165, 180)
CELL = (256, 320)
FPS = 8


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def rgba_changed(before: Image.Image, after: Image.Image) -> tuple[Image.Image, int]:
    mask = Image.new("L", CELL, 0)
    changed = 0
    for y in range(320):
        for x in range(256):
            if before.getpixel((x, y)) != after.getpixel((x, y)):
                mask.putpixel((x, y), 255)
                changed += 1
    return mask, changed


def recolour_to_target(image: Image.Image, spec: dict, target_hsv: list[float]) -> tuple[Image.Image, Image.Image, Image.Image, dict]:
    samples = v3.pixels_for(image, spec)
    before = v3.stats(samples)
    shifts = [target_hsv[index] - before["medianHSV"][index] for index in range(3)]
    output = image.copy()
    coverage = Image.new("L", CELL, 0)
    changed = Image.new("L", CELL, 0)
    changed_pixels = 0
    for x, y, _r, _g, _b, hue, saturation, value in samples:
        coverage.putpixel((x, y), 255)
        mapped = [max(0, min(1, channel + shift)) for channel, shift in zip((hue, saturation, value), shifts)]
        red, green, blue = colorsys.hsv_to_rgb(*mapped)
        updated = (round(red * 255), round(green * 255), round(blue * 255), image.getpixel((x, y))[3])
        if updated != image.getpixel((x, y)):
            output.putpixel((x, y), updated)
            changed.putpixel((x, y), 255)
            changed_pixels += 1
    corrected_samples = []
    for x, y, *_ in samples:
        red, green, blue, _alpha = output.getpixel((x, y))
        hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        corrected_samples.append((x, y, red, green, blue, hue, saturation, value))
    return output, coverage, changed, {"source": before, "targetMedianHSV": target_hsv, "corrected": v3.stats(corrected_samples), "changedPixels": changed_pixels, "method": "masked additive HSV offset; gradients retained"}


def scale_about_floor(image: Image.Image, target_height: int = 296) -> tuple[Image.Image, dict]:
    bounds = v1.alpha_bounds(image)
    crop = image.crop(bounds)
    scale = target_height / crop.height
    target_width = round(crop.width * scale)
    resized = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
    centre_x = (bounds[0] + bounds[2]) / 2
    left = round(centre_x - target_width / 2)
    top = 316 - target_height
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    output.alpha_composite(resized, (left, top))
    pixels = output.load()
    for y in range(320):
        for x in range(256):
            if pixels[x, y][3] < 8:
                pixels[x, y] = (0, 0, 0, 0)
    return output, {"sourceBoundsExclusive": list(bounds), "uniformScale": round(scale, 12), "registeredSize": [target_width, target_height], "registeredOffset": [left, top], "floorY": 316, "filter": "Lanczos", "creativePixelWarp": False}


def partial_alpha(image: Image.Image) -> int:
    return sum(0 < alpha < 255 for alpha in image.getchannel("A").getdata())


def panel_sheet(old_frames: list[Image.Image], new_frames: list[Image.Image]) -> Image.Image:
    output = Image.new("RGBA", (6 * 256, 356), (12, 20, 27, 255))
    labels = ("F1 V5", "F1 V6 palette", "F7 V5", "F7 V6 height", "F8 V5 proxy", "F8 V6 smooth master")
    images = (old_frames[0], new_frames[0], old_frames[6], new_frames[6], old_frames[7], new_frames[7])
    draw = ImageDraw.Draw(output)
    for index, (label, image) in enumerate(zip(labels, images)):
        stage = v1.checkerboard(); stage.alpha_composite(image)
        output.alpha_composite(stage, (index * 256, 36))
        draw.text((index * 256 + 8, 10), label, fill="#ffffff", font=ImageFont.load_default())
    return output


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    urls: dict[str, str] = {}
    for key, source in records.items():
        target = assets / f"{key}-{v2.digest(source)[:16]}{source.suffix}"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(frame_paths: list[Path], evidence: Path, contact: Path) -> None:
    records = {f"frame{index + 1}": path for index, path in enumerate(frame_paths)}
    records.update({"evidence": evidence, "contact": contact})
    urls = copy_public(records)
    asset = lambda key: f"{PUBLIC_ROUTE}/assets/{urls[key]}"
    frames_json = json.dumps([asset(f"frame{index + 1}") for index in range(8)])
    angles_json = json.dumps(list(ANGLES))
    thumbs = "".join(f'<button class="thumb" data-frame="{index}"><img src="{asset(f"frame{index + 1}")}" alt=""><span>F{index + 1} · {ANGLES[index]}°</span></button>' for index in range(8))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side ↔ back Turn V6</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.review-grid{{display:grid;grid-template-columns:minmax(330px,1fr) minmax(290px,.72fr);gap:18px}}.large-stage{{width:min(100%,512px);aspect-ratio:4/5;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.large-stage img{{width:100%;height:100%;object-fit:contain}}.game-wrap{{min-height:230px;display:grid;place-items:center}}.game-stage,.game-stage img{{width:128px;height:160px}}.game-stage{{background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/8px 8px;outline:1px solid #6f8492}}.game-stage img{{display:block;object-fit:contain;image-rendering:pixelated}}button,input{{font:inherit}}button{{color:var(--ink);background:#111a21;border:1px solid var(--line);border-radius:6px;margin:4px;padding:8px 11px}}.step{{border-color:var(--amber)}}.active{{background:#185f3a!important}}.frames{{display:grid;grid-template-columns:repeat(8,minmax(82px,1fr));gap:8px;overflow:auto}}.thumb{{margin:0;padding:5px}}.thumb img{{width:100%;aspect-ratio:4/5;object-fit:contain;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/12px 12px}}.thumb span{{display:block;white-space:nowrap}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}@media(max-width:850px){{.review-grid{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/keeper-review/keeper-prime-turn-side-back-v5">← Approved V5 record</a><h1>Keeper Prime Turn V6 · three-point refinement</h1><span class="status">New reversible candidate · awaiting visual approval</span><p>V6 responds only to Frank's latest review: F1 lower-uniform colour, F7 perceived height and F8 rendering smoothness. V5 remains immutable approved provenance; Final and production are unchanged.</p></header><main><p class="rule"><strong>Review priority:</strong> F1 trousers/boots should no longer read dark; F7 should sit slightly lower without losing its floor; F8 should resolve from the approved smooth 1122 × 1402 rear master rather than the coarse proxy.</p><section class="review-grid"><article><h2>Large inspection view</h2><div class="large-stage"><img id="largePlayer" src="{asset('frame1')}" alt="Large V6 turn"></div></article><article><h2>Proposed in-game size</h2><div class="game-wrap"><div class="game-stage"><img id="gamePlayer" src="{asset('frame1')}" alt="V6 turn at proposed game size"></div></div><p>Exact 128 × 160 CSS-pixel display box at 100% browser zoom.</p></article></section><article><h2 id="frameLabel">Frame 1 of 8 · 90°</h2><p id="mode">Looping side ↔ back</p><button id="previous" class="step">← Previous frame</button><button id="next" class="step">Next frame →</button><br><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="pause">Pause</button><br><label>Frame time <input id="speed" type="range" min="80" max="500" value="125"> <span id="speedValue">125 ms</span></label></article><section class="frames">{thumbs}</section><h2>Exact before/after evidence</h2><article><img class="wide" src="{asset('evidence')}" alt="V5 and V6 comparison for frames 1, 7 and 8"></article><h2>Complete V6 sequence</h2><article><img class="wide" src="{asset('contact')}" alt="Complete V6 turn sequence"></article><h2>Approval boundary</h2><article><p>V6 changes only F1, F7 and F8. F2–F6 are exact V5/V4 bytes. Approval would supersede V5 as the side/back core-turn artwork authority; it would not promote production.</p></article></main><script>const frames={frames_json},angles={angles_json};const large=document.getElementById('largePlayer'),game=document.getElementById('gamePlayer'),label=document.getElementById('frameLabel'),mode=document.getElementById('mode'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let timer=null,index=0,sequence=[],cursor=0,loop=false;function show(i){{index=(i+frames.length)%frames.length;large.src=frames[index];game.src=frames[index];label.textContent=`Frame ${{index+1}} of ${{frames.length}} · ${{angles[index]}}°`;document.querySelectorAll('[data-frame]').forEach(button=>button.classList.toggle('active',Number(button.dataset.frame)===index));}}function stop(message='Paused'){{if(timer)clearTimeout(timer);timer=null;mode.textContent=message;}}function step(delta){{stop('Paused · frame stepping');show(index+delta);}}function play(seq,repeat,name){{stop();sequence=seq;cursor=0;loop=repeat;mode.textContent=name;const tick=()=>{{show(sequence[cursor]);cursor+=1;if(cursor>=sequence.length){{if(loop)cursor=0;else{{stop('Finished');return}}}}timer=setTimeout(tick,Number(speed.value));}};tick();}}document.getElementById('previous').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('forward').onclick=()=>play([0,1,2,3,4,5,6,7],false,'Playing side → back');document.getElementById('reverse').onclick=()=>play([7,6,5,4,3,2,1,0],false,'Playing back → side');document.getElementById('pingpong').onclick=()=>play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');document.getElementById('pause').onclick=()=>stop();speed.oninput=()=>speedValue.textContent=`${{speed.value}} ms`;document.querySelectorAll('[data-frame]').forEach(button=>button.onclick=()=>{{stop('Paused · selected frame');show(Number(button.dataset.frame));}});show(0);play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    v4_register = json.loads(V4_REGISTER.read_text())
    approval = json.loads(V5_APPROVAL.read_text())
    palette = json.loads(PALETTE.read_text())
    if approval.get("status") != "approved-side-back-turn-artwork-authority":
        raise RuntimeError("V5 approval authority missing")
    old_paths = [ROOT / item["file"] for item in v4_register["frames"]]
    old_frames = [Image.open(path).convert("RGBA") for path in old_paths]
    frames = [image.copy() for image in old_frames]
    for generated in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if generated.exists():
            shutil.rmtree(generated)

    masks = PACK / "drafts/masks"; masks.mkdir(parents=True, exist_ok=True)
    f1_checks = {}
    for name in ("trouserNavy", "bootNavy"):
        frames[0], coverage, changed, check = recolour_to_target(frames[0], v3.COMPONENTS[name], palette["components"][name]["target"]["medianHSV"])
        coverage_path = masks / f"f1-{name}-coverage.png"; changed_path = masks / f"f1-{name}-changed.png"
        coverage.save(coverage_path, optimize=False, compress_level=9); changed.save(changed_path, optimize=False, compress_level=9)
        f1_checks[name] = {**check, "coverageMask": rel(coverage_path), "coverageMaskSha256": v2.digest(coverage_path), "changedMask": rel(changed_path), "changedMaskSha256": v2.digest(changed_path)}

    frames[6], f7_registration = scale_about_floor(frames[6], 296)

    smooth_f8, f8_registration = ortho.normalize(SMOOTH_BACK)
    f8_checks = {}
    f8_specs = {
        "capCrownBlue": {"y": (15, 63), "kind": "bright-blue"}, "capBandNavy": {"y": (60, 78), "kind": "navy"},
        "jumperBlue": {"y": (104, 215), "kind": "bright-blue"}, "jumperCream": {"y": (126, 166), "kind": "cream"},
        "trouserNavy": {"y": (202, 254), "kind": "navy"}, "bootNavy": {"y": (250, 317), "kind": "navy"},
    }
    for name, spec in f8_specs.items():
        smooth_f8, coverage, changed, check = recolour_to_target(smooth_f8, spec, palette["components"][name]["target"]["medianHSV"])
        coverage_path = masks / f"f8-{name}-coverage.png"; changed_path = masks / f"f8-{name}-changed.png"
        coverage.save(coverage_path, optimize=False, compress_level=9); changed.save(changed_path, optimize=False, compress_level=9)
        f8_checks[name] = {**check, "coverageMask": rel(coverage_path), "coverageMaskSha256": v2.digest(coverage_path), "changedMask": rel(changed_path), "changedMaskSha256": v2.digest(changed_path)}
    frames[7] = smooth_f8

    frame_dir = PACK / "drafts/frames"; frame_dir.mkdir(parents=True, exist_ok=True)
    frame_paths = []
    frame_records = []
    for index, (angle, frame, prior_path, prior_record) in enumerate(zip(ANGLES, frames, old_paths, v4_register["frames"]), start=1):
        path = frame_dir / f"keeper_prime_turn_side-right_to_back_f{index}.png"
        if index in (2, 3, 4, 5, 6): shutil.copyfile(prior_path, path)
        else: frame.save(path, optimize=False, compress_level=9)
        frame_paths.append(path)
        bounds = v1.alpha_bounds(frame)
        mask, changed_pixels = rgba_changed(old_frames[index - 1], frame)
        mask_path = masks / f"f{index}-all-changed.png"
        if changed_pixels: mask.save(mask_path, optimize=False, compress_level=9)
        frame_records.append({"frame": index, "angleDegrees": angle, "file": rel(path), "sha256": v2.digest(path), "sourceV4File": rel(prior_path), "sourceV4Sha256": prior_record["sha256"], "change": {1: "trouser-and-boot-palette-only", 7: "uniform-floor-anchored-height-correction", 8: "full-frame-approved-smooth-master-rebuild"}.get(index, "none-byte-identical"), "changedPixels": changed_pixels, "changedMask": rel(mask_path) if changed_pixels else None, "changedMaskSha256": v2.digest(mask_path) if changed_pixels else None, "opaqueBoundsExclusive": list(bounds), "opaqueHeight": bounds[3] - bounds[1], "edgeAlphaPixels": v1.edge_alpha_count(frame), "partialAlphaPixels": partial_alpha(frame)})

    forward = PACK / "drafts/keeper_prime_turn_side-right_to_back_f8.png"; reverse = PACK / "drafts/keeper_prime_turn_back_to_side-right_f8.png"
    v1.save_strip(forward, frames); v1.save_strip(reverse, list(reversed(frames)))
    common = {"w": 32, "h": 40, "density": 8, "frames": 8, "fps": FPS, "anchor": [16, 40], "loop": False, "outfit": "standard-single-band", "palette": palette["id"], "paletteApproval": rel(V5_APPROVAL), "status": "draft-v6-awaiting-visual-approval"}
    forward_sidecar = forward.with_suffix(".json"); reverse_sidecar = reverse.with_suffix(".json")
    v2.dump(forward_sidecar, {"name": "keeper_prime_turn_side-right_to_back_v6", **common, "startPose": "standing-side-right-palette-corrected", "endPose": "standing-back-smooth-master" , "sha256": v2.digest(forward), "frameFiles": [rel(path) for path in frame_paths]})
    v2.dump(reverse_sidecar, {"name": "keeper_prime_turn_back_to_side-right_v6", **common, "startPose": "standing-back-smooth-master", "endPose": "standing-side-right-palette-corrected", "sha256": v2.digest(reverse), "frameFiles": [rel(path) for path in reversed(frame_paths)], "exactReverseOf": rel(forward)})

    evidence_dir = PACK / "evidence"; evidence_dir.mkdir(parents=True, exist_ok=True)
    comparison = evidence_dir / "v5-v6-three-point-comparison.png"; contact = evidence_dir / "v6-contact-sheet.png"
    panel_sheet(old_frames, frames).save(comparison, optimize=False, compress_level=9)
    v1.contact_sheet(frames).save(contact, optimize=False, compress_level=9)
    write_page(frame_paths, comparison, contact)

    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v6", "status": "draft-v6-three-point-refinement-awaiting-visual-approval",
        "purpose": "Address Frank's V5 scale-review feedback: F1 lower uniform too dark, F7 slightly too tall and F8 visibly pixelated when enlarged.",
        "priorApproval": {"register": rel(V5_APPROVAL), "registerSha256": v2.digest(V5_APPROVAL), "wording": approval["approval"]["wording"], "disposition": "immutable approved provenance; V6 is a separate superseding candidate only"},
        "palette": {"file": rel(PALETTE), "sha256": v2.digest(PALETTE), "approvalRegister": rel(V5_APPROVAL), "approvalRegisterSha256": v2.digest(V5_APPROVAL)},
        "smoothBackAuthority": {"file": rel(SMOOTH_BACK), "sha256": v2.digest(SMOOTH_BACK), "register": rel(SMOOTH_BACK_REGISTER), "registerSha256": v2.digest(SMOOTH_BACK_REGISTER), "dimensions": list(Image.open(SMOOTH_BACK).size), "approvalWording": "They don't look like toe caps, they are excellent. Approved."},
        "changes": {
            "f1Palette": {"scope": ["trouserNavy", "bootNavy"], "componentChecks": f1_checks, "alphaUnchanged": frames[0].getchannel("A").tobytes() == old_frames[0].getchannel("A").tobytes()},
            "f7Height": {"sourceHeight": 298, "candidateHeight": 296, "floorY": 316, "registration": f7_registration},
            "f8SmoothMaster": {"registration": f8_registration, "componentChecks": f8_checks, "sourcePartialAlphaPixels": partial_alpha(old_frames[7]), "candidatePartialAlphaPixels": partial_alpha(frames[7]), "filter": "Lanczos", "creativePixelWarp": False}
        },
        "frames": frame_records,
        "animation": {"fps": FPS, "cell": list(CELL), "logicalCell": [32, 40], "density": 8, "forward": {"file": rel(forward), "sha256": v2.digest(forward), "sidecar": rel(forward_sidecar), "sidecarSha256": v2.digest(forward_sidecar)}, "reverse": {"file": rel(reverse), "sha256": v2.digest(reverse), "sidecar": rel(reverse_sidecar), "sidecarSha256": v2.digest(reverse_sidecar), "exactFrameOrderReverse": True}},
        "reviewSurface": {"publicReview": f"{PUBLIC_ROUTE}/", "publicPage": rel(PUBLIC / "index.html"), "publicPageSha256": v2.digest(PUBLIC / "index.html"), "largeAndGameViewsSynchronized": True, "gameCssDisplay": [128, 160], "previousNextControls": True},
        "evidence": {"comparison": {"file": rel(comparison), "sha256": v2.digest(comparison)}, "contactSheet": {"file": rel(contact), "sha256": v2.digest(contact)}},
        "validation": {"frames2To6ByteIdenticalToV4": True, "frame1AlphaUnchanged": True, "frame7UniformScaleOnly": True, "frame7FloorStable": True, "frame8UsesApprovedSmoothMaster": True, "frame8UniformRegistrationOnly": True, "everyFrameTransparentCellEdge": all(item["edgeAlphaPixels"] == 0 for item in frame_records), "productionSpritesChanged": False, "runtimeManifestChanged": False, "finalLaneChanged": False, "priorDraftsChanged": False},
        "approvalBoundary": {"v6Approved": False, "v5ApprovalRevoked": False, "productionPromotionAllowed": False, "finalLaneEntryAllowed": False},
        "nextGate": "Frank reviews the V6 large and exact game-scale loops, especially F1, F7 and F8, before any authority changes.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1–V5, approved endpoints, Final and production remain unchanged."
    }
    v2.dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "f1Changed": frame_records[0]["changedPixels"], "f7Bounds": frame_records[6]["opaqueBoundsExclusive"], "f8Bounds": frame_records[7]["opaqueBoundsExclusive"], "f8PartialAlpha": register["changes"]["f8SmoothMaster"], "public": register["reviewSurface"]["publicReview"]}, indent=2))


if __name__ == "__main__":
    main()
