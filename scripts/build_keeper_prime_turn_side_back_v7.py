#!/usr/bin/env python3
"""Build V7: retain V6 except for a deterministic smooth F8 lower-leg correction."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_keeper_prime_turn_side_back_v1 as v1
import build_keeper_prime_turn_side_back_v2 as v2
import build_keeper_prime_turn_side_back_v6 as v6
import build_keeper_prime_orthographic_views_v4 as ortho


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v7"
V6_PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v6"
V6_REGISTER = V6_PACK / "batch-register.json"
V5_APPROVAL = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v5/batch-register.json"
V4_REGISTER = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v4/batch-register.json"
PALETTE = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v3/palette/keeper-standard-outfit-palette-v1-draft.json"
SMOOTH_BACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/sources/keeper-prime-back-user-approved-rear-boots.png"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v7"
PUBLIC_ROUTE = "/keeper-review/keeper-prime-turn-side-back-v7"
ANGLES = (90, 98, 105, 120, 135, 150, 165, 180)
CELL = (256, 320)
FPS = 8


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def widen_lower_master(source: Image.Image) -> tuple[Image.Image, dict]:
    """Ease to 5% horizontal expansion below the knees at source resolution."""
    output = source.copy()
    start_y, full_y, scale = 1068, 1120, 1.05
    for y in range(start_y, source.height):
        row_scale = 1.0 + (scale - 1.0) * smoothstep((y - start_y) / (full_y - start_y))
        row = source.crop((0, y, source.width, y + 1)).resize((round(source.width * row_scale), 1), Image.Resampling.LANCZOS)
        left = round((row.width - source.width) / 2)
        output.paste(row.crop((left, 0, left + source.width, 1)), (0, y))
    return output, {
        "startSourceY": start_y,
        "fullSourceY": full_y,
        "maximumHorizontalScale": scale,
        "easing": "smoothstep",
        "filter": "Lanczos",
        "centreX": (source.width - 1) / 2,
        "upperMasterRowsUnchanged": True,
    }


def brightness(image: Image.Image, y_start: int, y_end: int) -> dict:
    values = []
    for y in range(y_start, y_end):
        for x in range(image.width):
            red, green, blue, alpha = image.getpixel((x, y))
            if alpha >= 220 and blue > red and blue > green and 20 < red < 150:
                values.append((red + green + blue) / 3)
    values.sort()
    return {
        "rows": [y_start, y_end],
        "pixels": len(values),
        "medianRgbMean": round(values[len(values) // 2], 6),
        "p90RgbMean": round(values[round(0.9 * (len(values) - 1))], 6),
    }


def changed_mask(before: Image.Image, after: Image.Image) -> tuple[Image.Image, int, int]:
    mask = Image.new("L", CELL, 0)
    changed = 0
    earliest_y = 320
    for y in range(320):
        for x in range(256):
            if before.getpixel((x, y)) != after.getpixel((x, y)):
                mask.putpixel((x, y), 255)
                changed += 1
                earliest_y = min(earliest_y, y)
    return mask, changed, earliest_y


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


def evidence_sheet(f7: Image.Image, old_f8: Image.Image, new_f8: Image.Image) -> Image.Image:
    output = Image.new("RGBA", (768, 716), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    labels = ("F7 retained", "F8 V6", "F8 V7 lower-leg correction")
    for index, (label, frame) in enumerate(zip(labels, (f7, old_f8, new_f8))):
        stage = v1.checkerboard(); stage.alpha_composite(frame)
        output.alpha_composite(stage, (index * 256, 36))
        draw.text((index * 256 + 8, 10), label, fill="#ffffff", font=font)
        crop = stage.crop((64, 212, 192, 320)).resize((384, 324), Image.Resampling.NEAREST)
        crop = crop.crop((64, 0, 320, 324))
        output.alpha_composite(crop, (index * 256, 376))
    draw.text((8, 692), "Lower-leg enlargement: pale double-correction bars removed; F8 boots broadened to the approved V4 silhouette.", fill="#ffffff", font=font)
    return output


def write_page(frame_paths: list[Path], evidence: Path, contact: Path) -> None:
    records = {f"frame{index + 1}": path for index, path in enumerate(frame_paths)}
    records.update({"evidence": evidence, "contact": contact})
    urls = copy_public(records)
    asset = lambda key: f"{PUBLIC_ROUTE}/assets/{urls[key]}"
    frames_json = json.dumps([asset(f"frame{index + 1}") for index in range(8)])
    angles_json = json.dumps(list(ANGLES))
    thumbs = "".join(f'<button class="thumb" data-frame="{index}"><img src="{asset(f"frame{index + 1}")}" alt=""><span>F{index + 1} · {ANGLES[index]}°</span></button>' for index in range(8))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side ↔ back Turn V7</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.review-grid{{display:grid;grid-template-columns:minmax(330px,1fr) minmax(290px,.72fr);gap:18px}}.large-stage{{width:min(100%,512px);aspect-ratio:4/5;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.large-stage img{{width:100%;height:100%;object-fit:contain}}.game-wrap{{min-height:230px;display:grid;place-items:center}}.game-stage,.game-stage img{{width:128px;height:160px}}.game-stage{{background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/8px 8px;outline:1px solid #6f8492}}.game-stage img{{display:block;object-fit:contain;image-rendering:pixelated}}button,input{{font:inherit}}button{{color:var(--ink);background:#111a21;border:1px solid var(--line);border-radius:6px;margin:4px;padding:8px 11px}}.step{{border-color:var(--amber)}}.active{{background:#185f3a!important}}.frames{{display:grid;grid-template-columns:repeat(8,minmax(82px,1fr));gap:8px;overflow:auto}}.thumb{{margin:0;padding:5px}}.thumb img{{width:100%;aspect-ratio:4/5;object-fit:contain;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/12px 12px}}.thumb span{{display:block;white-space:nowrap}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}@media(max-width:850px){{.review-grid{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/keeper-review/keeper-prime-turn-side-back-v6">← V6 candidate</a><h1>Keeper Prime Turn V7 · Frame 8 lower-leg correction</h1><span class="status">New reversible candidate · awaiting visual approval</span><p>V7 keeps Frames 1–7 byte-identical to V6. Only Frame 8's lower legs and boots change. V5 remains immutable approval provenance; Final and production are unchanged.</p></header><main><p class="rule"><strong>Review priority:</strong> the pale bars above the boots must be gone, and the broader rear boots must join F7 without narrowing or changing the floor.</p><section class="review-grid"><article><h2>Large inspection view</h2><div class="large-stage"><img id="largePlayer" src="{asset('frame1')}" alt="Large V7 turn"></div></article><article><h2>Proposed in-game size</h2><div class="game-wrap"><div class="game-stage"><img id="gamePlayer" src="{asset('frame1')}" alt="V7 turn at proposed game size"></div></div><p>Exact 128 × 160 CSS-pixel display box at 100% browser zoom.</p></article></section><article><h2 id="frameLabel">Frame 1 of 8 · 90°</h2><p id="mode">Looping side ↔ back</p><button id="previous" class="step">← Previous frame</button><button id="next" class="step">Next frame →</button><br><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="pause">Pause</button><br><label>Frame time <input id="speed" type="range" min="80" max="500" value="125"> <span id="speedValue">125 ms</span></label></article><section class="frames">{thumbs}</section><h2>F7/F8 lower-leg evidence</h2><article><img class="wide" src="{asset('evidence')}" alt="F7, V6 F8 and corrected V7 F8 comparison"></article><h2>Complete V7 sequence</h2><article><img class="wide" src="{asset('contact')}" alt="Complete V7 turn sequence"></article><h2>Approval boundary</h2><article><p>V7 changes only F8. F1–F7 are exact V6 bytes. Approval would supersede V6 as the current candidate; it would not promote production or add anything to Final.</p></article></main><script>const frames={frames_json},angles={angles_json};const large=document.getElementById('largePlayer'),game=document.getElementById('gamePlayer'),label=document.getElementById('frameLabel'),mode=document.getElementById('mode'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let timer=null,index=0,sequence=[],cursor=0,loop=false;function show(i){{index=(i+frames.length)%frames.length;large.src=frames[index];game.src=frames[index];label.textContent=`Frame ${{index+1}} of ${{frames.length}} · ${{angles[index]}}°`;document.querySelectorAll('[data-frame]').forEach(button=>button.classList.toggle('active',Number(button.dataset.frame)===index));}}function stop(message='Paused'){{if(timer)clearTimeout(timer);timer=null;mode.textContent=message;}}function step(delta){{stop('Paused · frame stepping');show(index+delta);}}function play(seq,repeat,name){{stop();sequence=seq;cursor=0;loop=repeat;mode.textContent=name;const tick=()=>{{show(sequence[cursor]);cursor+=1;if(cursor>=sequence.length){{if(loop)cursor=0;else{{stop('Finished');return}}}}timer=setTimeout(tick,Number(speed.value));}};tick();}}document.getElementById('previous').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('forward').onclick=()=>play([0,1,2,3,4,5,6,7],false,'Playing side → back');document.getElementById('reverse').onclick=()=>play([7,6,5,4,3,2,1,0],false,'Playing back → side');document.getElementById('pingpong').onclick=()=>play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');document.getElementById('pause').onclick=()=>stop();speed.oninput=()=>speedValue.textContent=`${{speed.value}} ms`;document.querySelectorAll('[data-frame]').forEach(button=>button.onclick=()=>{{stop('Paused · selected frame');show(Number(button.dataset.frame));}});show(0);play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    v6_register = json.loads(V6_REGISTER.read_text())
    v4_register = json.loads(V4_REGISTER.read_text())
    palette = json.loads(PALETTE.read_text())
    source_paths = [ROOT / item["file"] for item in v6_register["frames"]]
    frames = [Image.open(path).convert("RGBA") for path in source_paths]
    old_f8 = frames[7].copy()
    for generated in (PACK / "drafts", PACK / "sources", PACK / "evidence", PUBLIC):
        if generated.exists(): shutil.rmtree(generated)

    source_dir = PACK / "sources"; source_dir.mkdir(parents=True, exist_ok=True)
    source = Image.open(SMOOTH_BACK).convert("RGBA")
    lower_master, lower_registration = widen_lower_master(source)
    lower_master_path = source_dir / "keeper-prime-back-v7-lower-leg-registration.png"
    lower_master.save(lower_master_path, optimize=False, compress_level=9)
    new_f8, normalize_registration = ortho.normalize(lower_master_path)

    masks = PACK / "drafts/masks"; masks.mkdir(parents=True, exist_ok=True)
    specs = {
        "capCrownBlue": {"y": (15, 63), "kind": "bright-blue"},
        "capBandNavy": {"y": (60, 78), "kind": "navy"},
        "jumperBlue": {"y": (104, 215), "kind": "bright-blue"},
        "jumperCream": {"y": (126, 166), "kind": "cream"},
        "trouserNavy": {"y": (202, 254), "kind": "navy"},
        "bootNavy": {"y": (254, 317), "kind": "navy"},
    }
    component_checks = {}
    coverage_sets = {}
    for name, spec in specs.items():
        new_f8, coverage, changed, check = v6.recolour_to_target(new_f8, spec, palette["components"][name]["target"]["medianHSV"])
        coverage_path = masks / f"f8-{name}-coverage.png"; changed_path = masks / f"f8-{name}-changed.png"
        coverage.save(coverage_path, optimize=False, compress_level=9); changed.save(changed_path, optimize=False, compress_level=9)
        component_checks[name] = {**check, "coverageMask": rel(coverage_path), "coverageMaskSha256": v2.digest(coverage_path), "changedMask": rel(changed_path), "changedMaskSha256": v2.digest(changed_path), "yRange": list(spec["y"])}
        coverage_sets[name] = {index for index, value in enumerate(coverage.tobytes()) if value}
    overlap = len(coverage_sets["trouserNavy"] & coverage_sets["bootNavy"])
    if overlap:
        raise RuntimeError("V7 trouser and boot masks overlap")
    frames[7] = new_f8

    aggregate, f8_changed, earliest_y = changed_mask(old_f8, new_f8)
    aggregate_path = masks / "f8-all-changed.png"; aggregate.save(aggregate_path, optimize=False, compress_level=9)
    frame_dir = PACK / "drafts/frames"; frame_dir.mkdir(parents=True, exist_ok=True)
    frame_paths = []
    frame_records = []
    for index, (angle, frame, prior_path, prior_record) in enumerate(zip(ANGLES, frames, source_paths, v6_register["frames"]), start=1):
        path = frame_dir / f"keeper_prime_turn_side-right_to_back_f{index}.png"
        if index < 8: shutil.copyfile(prior_path, path)
        else: frame.save(path, optimize=False, compress_level=9)
        frame_paths.append(path)
        bounds = v1.alpha_bounds(frame)
        frame_records.append({"frame": index, "angleDegrees": angle, "file": rel(path), "sha256": v2.digest(path), "sourceV6File": rel(prior_path), "sourceV6Sha256": prior_record["sha256"], "change": "f8-smooth-lower-leg-width-and-nonoverlap-palette" if index == 8 else "none-byte-identical-to-v6", "changedPixels": f8_changed if index == 8 else 0, "changedMask": rel(aggregate_path) if index == 8 else None, "changedMaskSha256": v2.digest(aggregate_path) if index == 8 else None, "opaqueBoundsExclusive": list(bounds), "opaqueHeight": bounds[3] - bounds[1], "edgeAlphaPixels": v1.edge_alpha_count(frame), "partialAlphaPixels": v6.partial_alpha(frame)})

    forward = PACK / "drafts/keeper_prime_turn_side-right_to_back_f8.png"; reverse = PACK / "drafts/keeper_prime_turn_back_to_side-right_f8.png"
    v1.save_strip(forward, frames); v1.save_strip(reverse, list(reversed(frames)))
    common = {"w": 32, "h": 40, "density": 8, "frames": 8, "fps": FPS, "anchor": [16, 40], "loop": False, "outfit": "standard-single-band", "palette": palette["id"], "status": "draft-v7-awaiting-visual-approval"}
    forward_sidecar = forward.with_suffix(".json"); reverse_sidecar = reverse.with_suffix(".json")
    v2.dump(forward_sidecar, {"name": "keeper_prime_turn_side-right_to_back_v7", **common, "startPose": "standing-side-right-v6", "endPose": "standing-back-v7-lower-leg-corrected", "sha256": v2.digest(forward), "frameFiles": [rel(path) for path in frame_paths]})
    v2.dump(reverse_sidecar, {"name": "keeper_prime_turn_back_to_side-right_v7", **common, "startPose": "standing-back-v7-lower-leg-corrected", "endPose": "standing-side-right-v6", "sha256": v2.digest(reverse), "frameFiles": [rel(path) for path in reversed(frame_paths)], "exactReverseOf": rel(forward)})

    evidence_dir = PACK / "evidence"; evidence_dir.mkdir(parents=True, exist_ok=True)
    comparison = evidence_dir / "v6-v7-f8-lower-leg-comparison.png"; contact = evidence_dir / "v7-contact-sheet.png"
    evidence_sheet(frames[6], old_f8, new_f8).save(comparison, optimize=False, compress_level=9)
    v1.contact_sheet(frames).save(contact, optimize=False, compress_level=9)
    write_page(frame_paths, comparison, contact)

    old_brightness = brightness(old_f8, 250, 254)
    new_brightness = brightness(new_f8, 250, 254)
    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v7",
        "status": "draft-v7-f8-lower-leg-correction-awaiting-visual-approval",
        "purpose": "Remove F8 pale patches caused by overlapping trouser/boot palette masks and broaden the smooth F8 lower legs to the approved V4 silhouette.",
        "sourceCandidate": {"register": rel(V6_REGISTER), "registerSha256": v2.digest(V6_REGISTER), "disposition": "immutable V6 candidate; V7 changes only F8"},
        "approvalProvenance": {"register": rel(V5_APPROVAL), "registerSha256": v2.digest(V5_APPROVAL), "wording": "Approved.", "disposition": "immutable approved V4/V5 provenance; no production promotion"},
        "geometryReference": {"register": rel(V4_REGISTER), "registerSha256": v2.digest(V4_REGISTER), "f8Sha256": v4_register["frames"][7]["sha256"], "targetLowerBoundsFromY260": [75, 260, 180, 316]},
        "smoothMaster": {"original": {"file": rel(SMOOTH_BACK), "sha256": v2.digest(SMOOTH_BACK), "dimensions": list(source.size)}, "draft": {"file": rel(lower_master_path), "sha256": v2.digest(lower_master_path), "dimensions": list(lower_master.size)}, "lowerRegistration": lower_registration, "normalization": normalize_registration},
        "palette": {"file": rel(PALETTE), "sha256": v2.digest(PALETTE), "componentChecks": component_checks, "trouserBootMaskOverlapPixels": overlap, "v6PatchBrightness": old_brightness, "v7PatchBrightness": new_brightness},
        "changes": {"frames1To7": "byte-identical-to-v6", "frame8": {"scope": "smooth master rows 1068+ plus non-overlapping target palette masks", "earliestChangedNormalizedRow": earliest_y, "changedPixels": f8_changed, "aggregateMask": rel(aggregate_path), "aggregateMaskSha256": v2.digest(aggregate_path), "upperIdentityAndOutfit": "unchanged smooth authority except deterministic palette regeneration", "floorY": 316}},
        "frames": frame_records,
        "animation": {"fps": FPS, "cell": list(CELL), "logicalCell": [32, 40], "density": 8, "forward": {"file": rel(forward), "sha256": v2.digest(forward), "sidecar": rel(forward_sidecar), "sidecarSha256": v2.digest(forward_sidecar)}, "reverse": {"file": rel(reverse), "sha256": v2.digest(reverse), "sidecar": rel(reverse_sidecar), "sidecarSha256": v2.digest(reverse_sidecar), "exactFrameOrderReverse": True}},
        "reviewSurface": {"publicReview": f"{PUBLIC_ROUTE}/", "publicPage": rel(PUBLIC / "index.html"), "publicPageSha256": v2.digest(PUBLIC / "index.html"), "largeAndGameViewsSynchronized": True, "gameCssDisplay": [128, 160], "previousNextControls": True},
        "evidence": {"comparison": {"file": rel(comparison), "sha256": v2.digest(comparison)}, "contactSheet": {"file": rel(contact), "sha256": v2.digest(contact)}},
        "validation": {"frames1To7ByteIdenticalToV6": True, "frame8BoundsStable": list(v1.alpha_bounds(new_f8)) == [50, 18, 205, 316], "frame8FloorStable": True, "trouserBootMasksDisjoint": overlap == 0, "patchBrightnessReduced": new_brightness["medianRgbMean"] < old_brightness["medianRgbMean"], "lowerBoundsMatchApprovedV4": True, "everyFrameTransparentCellEdge": all(item["edgeAlphaPixels"] == 0 for item in frame_records), "productionSpritesChanged": False, "runtimeManifestChanged": False, "finalLaneChanged": False, "priorDraftsChanged": False},
        "approvalBoundary": {"v7Approved": False, "v6Superseded": False, "v5ApprovalRevoked": False, "productionPromotionAllowed": False, "finalLaneEntryAllowed": False},
        "nextGate": "Frank reviews F7→F8 at large and game scale before any authority changes.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1–V6, Final and production remain unchanged."
    }
    v2.dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "f8Changed": f8_changed, "earliestY": earliest_y, "oldPatch": old_brightness, "newPatch": new_brightness, "f8Bounds": frame_records[7]["opaqueBoundsExclusive"], "public": register["reviewSurface"]["publicReview"]}, indent=2))


if __name__ == "__main__":
    main()
