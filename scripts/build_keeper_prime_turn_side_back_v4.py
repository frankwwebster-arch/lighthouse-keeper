#!/usr/bin/env python3
"""Build V4 with a boot-only full-back endpoint redraw registered to F7."""
from __future__ import annotations

import colorsys
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_keeper_prime_turn_side_back_v1 as v1
import build_keeper_prime_turn_side_back_v2 as v2
import build_keeper_prime_turn_side_back_v3 as v3


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v4"
PRIOR_PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v3"
PRIOR_REGISTER = PRIOR_PACK / "batch-register.json"
PALETTE = PRIOR_PACK / "palette/keeper-standard-outfit-palette-v1-draft.json"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v4"
PUBLIC_ROUTE = "/keeper-review/keeper-prime-turn-side-back-v4"
GENERATED_SOURCE = PACK / "sources/keeper-prime-back-boots-generated.png"
ANGLES = (90, 98, 105, 120, 135, 150, 165, 180)
CELL = (256, 320)
FPS = 8
BOOT_CUT_Y = 250


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def boot_metrics(image: Image.Image) -> dict:
    alpha = image.getchannel("A")
    records = []
    for start, end in ((0, 128), (128, 256)):
        points = [(x, y) for y in range(BOOT_CUT_Y, 320) for x in range(start, end) if alpha.getpixel((x, y)) >= 8]
        xs = [point[0] for point in points]; ys = [point[1] for point in points]
        records.append({"boundsExclusive": [min(xs), min(ys), max(xs) + 1, max(ys) + 1], "width": max(xs) - min(xs) + 1, "height": max(ys) - min(ys) + 1})
    return {"left": records[0], "right": records[1], "innerGap": records[1]["boundsExclusive"][0] - records[0]["boundsExclusive"][2], "floorExclusiveY": max(item["boundsExclusive"][3] for item in records)}


def recolour_boots(image: Image.Image, target_hsv: list[float]) -> tuple[Image.Image, dict]:
    spec = {"y": (BOOT_CUT_Y, 317), "kind": "navy"}
    samples = v3.pixels_for(image, spec)
    before = v3.stats(samples)
    shifts = [target_hsv[index] - before["medianHSV"][index] for index in range(3)]
    output = image.copy()
    for x, y, *_rgb, h, saturation, value in samples:
        h = max(0, min(1, h + shifts[0])); saturation = max(0, min(1, saturation + shifts[1])); value = max(0, min(1, value + shifts[2]))
        r, g, b = colorsys.hsv_to_rgb(h, saturation, value)
        output.putpixel((x, y), (round(r * 255), round(g * 255), round(b * 255), image.getpixel((x, y))[3]))
    corrected = []
    for x, y, *_ in samples:
        r, g, b, _ = output.getpixel((x, y)); h, s, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        corrected.append((x, y, r, g, b, h, s, value))
    return output, {"before": before, "corrected": v3.stats(corrected), "targetMedianHSV": target_hsv, "method": "smooth additive HSV offset; existing boot gradients retained"}


def ghost_overlay(reference: Image.Image, candidate: Image.Image) -> Image.Image:
    output = v1.checkerboard()
    ref_alpha = reference.getchannel("A")
    candidate_alpha = candidate.getchannel("A")
    draw = ImageDraw.Draw(output)
    for y in range(BOOT_CUT_Y, 320):
        for x in range(256):
            ref = ref_alpha.getpixel((x, y)) >= 8
            current = candidate_alpha.getpixel((x, y)) >= 8
            if ref and current:
                output.putpixel((x, y), (240, 240, 240, 255))
            elif ref:
                output.putpixel((x, y), (65, 220, 255, 255))
            elif current:
                output.putpixel((x, y), (255, 90, 190, 255))
    draw.line((0, BOOT_CUT_Y, 255, BOOT_CUT_Y), fill="#f0bd58", width=1)
    draw.line((0, 315, 255, 315), fill="#75f3a6", width=1)
    draw.text((6, BOOT_CUT_Y + 3), "boot redraw boundary y=250", fill="#f0bd58", font=ImageFont.load_default())
    draw.text((6, 302), "floor y=316", fill="#75f3a6", font=ImageFont.load_default())
    return output


def comparison(reference: Image.Image, prior: Image.Image, candidate: Image.Image, overlay: Image.Image) -> Image.Image:
    output = Image.new("RGBA", (4 * 256, 356), (12, 20, 27, 255))
    labels = ("F7 preceding pose", "F8 V3 boots", "F8 V4 redrawn boots", "ghost: F7 cyan / V4 magenta")
    draw = ImageDraw.Draw(output)
    for index, (label, image) in enumerate(zip(labels, (reference, prior, candidate, overlay))):
        stage = v1.checkerboard() if index < 3 else Image.new("RGBA", CELL, (0, 0, 0, 0))
        stage.alpha_composite(image)
        output.alpha_composite(stage, (index * 256, 36))
        draw.text((index * 256 + 8, 10), label, fill="#ffffff", font=ImageFont.load_default())
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


def write_page(frame_paths: list[Path], comparison_path: Path, contact_path: Path) -> None:
    records = {f"frame{index + 1}": path for index, path in enumerate(frame_paths)}
    records.update({"comparison": comparison_path, "contact": contact_path})
    urls = copy_public(records)
    asset = lambda key: f"{PUBLIC_ROUTE}/assets/{urls[key]}"
    frames_json = json.dumps([asset(f"frame{index + 1}") for index in range(8)])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side ↔ back Turn V4</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe0a0}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.player{{display:grid;grid-template-columns:minmax(280px,520px) 1fr;gap:24px;align-items:center}}.stage{{aspect-ratio:4/5;max-height:68vh;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px;margin:auto}}.stage img{{width:100%;height:100%;object-fit:contain;image-rendering:auto}}button,input{{font:inherit}}button{{margin:4px;padding:8px 11px}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}@media(max-width:800px){{.player{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/keeper-review/keeper-prime-turn-side-back-v3">← V3</a><h1>Keeper Prime Turn V4 · F8 boot geometry correction</h1><span class="status">Boot-only endpoint redraft · awaiting visual approval</span><p>F1–F7 are exact V3 bytes. F8 is exact V3 above y=250; only the two boot assemblies and their silhouette below that registered boundary have changed. Nothing has entered Final or production.</p></header><main><p class="rule"><strong>Review priority:</strong> watch F7 → F8. The boots should keep their visual weight, cuff construction, spacing and floor contact while resolving cleanly into a fully rear-facing pair.</p><article class="player"><div class="stage"><img id="player" src="{asset('frame1')}" alt="Animated side-to-back turn with corrected F8 boots"></div><div><h2>Corrected V4 loop</h2><p id="mode">Looping side ↔ back</p><div><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="pause">Pause</button></div><label>Frame time <input id="speed" type="range" min="80" max="500" value="125"> <span id="speedValue">125 ms</span></label></div></article><h2>Boot comparison and ghost overlay</h2><article><img class="wide" src="{asset('comparison')}" alt="F7, V3 F8, V4 F8 and boot ghost overlay"><p>Ghost colours: shared silhouette is white; F7-only is cyan; V4-only is magenta. The amber line is the boot-only redraw boundary; green is the common floor.</p></article><h2>Corrected eight-frame sequence</h2><article><img class="wide" src="{asset('contact')}" alt="Eight side-to-back turn poses with corrected rear boots"></article><h2>Approval boundary</h2><article><p>V4 preserves the V3 palette contract and changes no prior draft, approved rear master, Final asset, production sprite or runtime manifest. It is a new review candidate only.</p></article></main><script>const frames={frames_json};const img=document.getElementById('player'),mode=document.getElementById('mode'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let timer=null,sequence=[],cursor=0,loop=false;function show(i){{img.src=frames[i];}}function stop(){{if(timer)clearTimeout(timer);timer=null;mode.textContent='Paused';}}function play(seq,repeat,name){{stop();sequence=seq;cursor=0;loop=repeat;mode.textContent=name;const tick=()=>{{show(sequence[cursor]);cursor+=1;if(cursor>=sequence.length){{if(loop)cursor=0;else{{stop();return}}}}timer=setTimeout(tick,Number(speed.value));}};tick();}}document.getElementById('forward').onclick=()=>play([0,1,2,3,4,5,6,7],false,'Side → back');document.getElementById('reverse').onclick=()=>play([7,6,5,4,3,2,1,0],false,'Back → side');document.getElementById('pingpong').onclick=()=>play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');document.getElementById('pause').onclick=stop;speed.oninput=()=>speedValue.textContent=`${{speed.value}} ms`;play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    if not PRIOR_REGISTER.exists() or not PALETTE.exists() or not GENERATED_SOURCE.exists():
        raise RuntimeError("required V3 register, palette or boot source missing")
    prior = json.loads(PRIOR_REGISTER.read_text()); palette = json.loads(PALETTE.read_text())
    prior_frames = [ROOT / item["file"] for item in prior["frames"]]
    for generated in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if generated.exists():
            shutil.rmtree(generated)
    clean_source = PACK / "sources/keeper-prime-back-boots-generated-clean.png"
    generated_frame, registration = v1.normalize(GENERATED_SOURCE, clean_source)
    original = Image.open(prior_frames[-1]).convert("RGBA")
    candidate = original.copy()
    candidate.paste((0, 0, 0, 0), (0, BOOT_CUT_Y, 256, 320))
    candidate.alpha_composite(generated_frame.crop((0, BOOT_CUT_Y, 256, 320)), (0, BOOT_CUT_Y))
    candidate, palette_check = recolour_boots(candidate, palette["components"]["bootNavy"]["target"]["medianHSV"])
    changed_mask = Image.new("L", CELL, 0)
    changed_pixels = 0
    for y in range(320):
        for x in range(256):
            if candidate.getpixel((x, y)) != original.getpixel((x, y)):
                changed_mask.putpixel((x, y), 255); changed_pixels += 1
    mask_path = PACK / "drafts/masks/keeper_prime_turn_f8_boot_geometry_changed.png"
    mask_path.parent.mkdir(parents=True, exist_ok=True); changed_mask.save(mask_path, optimize=False, compress_level=9)
    frames = [Image.open(path).convert("RGBA") for path in prior_frames[:-1]] + [candidate]
    frame_dir = PACK / "drafts/frames"; frame_dir.mkdir(parents=True, exist_ok=True)
    frame_paths = []
    for index, frame in enumerate(frames, start=1):
        path = frame_dir / f"keeper_prime_turn_side-right_to_back_f{index}.png"
        if index < 8: shutil.copyfile(prior_frames[index - 1], path)
        else: frame.save(path, optimize=False, compress_level=9)
        frame_paths.append(path)
    forward = PACK / "drafts/keeper_prime_turn_side-right_to_back_f8.png"; reverse = PACK / "drafts/keeper_prime_turn_back_to_side-right_f8.png"
    v1.save_strip(forward, frames); v1.save_strip(reverse, list(reversed(frames)))
    common = {"w": 32, "h": 40, "density": 8, "frames": 8, "fps": FPS, "anchor": [16, 40], "loop": False, "outfit": "standard-single-band", "palette": palette["id"], "status": "draft-awaiting-visual-approval"}
    forward_sidecar = forward.with_suffix(".json"); reverse_sidecar = reverse.with_suffix(".json")
    v2.dump(forward_sidecar, {"name": "keeper_prime_turn_side-right_to_back_v4", **common, "startPose": "standing-side-right", "endPose": "standing-back-boot-redraw-candidate", "sha256": v2.digest(forward), "frameFiles": [rel(path) for path in frame_paths]})
    v2.dump(reverse_sidecar, {"name": "keeper_prime_turn_back_to_side-right_v4", **common, "startPose": "standing-back-boot-redraw-candidate", "endPose": "standing-side-right", "sha256": v2.digest(reverse), "frameFiles": [rel(path) for path in reversed(frame_paths)], "exactReverseOf": rel(forward)})
    evidence_dir = PACK / "evidence"; evidence_dir.mkdir(parents=True, exist_ok=True)
    overlay_path = evidence_dir / "f7-v4-boot-ghost-overlay.png"; comparison_path = evidence_dir / "f7-f8-boot-geometry-comparison.png"; contact_path = evidence_dir / "turn-contact-sheet-corrected.png"
    overlay = ghost_overlay(frames[-2], candidate); overlay.save(overlay_path, optimize=False, compress_level=9)
    comparison(frames[-2], original, candidate, overlay).save(comparison_path, optimize=False, compress_level=9)
    v1.contact_sheet(frames).save(contact_path, optimize=False, compress_level=9)
    frame_records = []
    for index, (angle, path, frame) in enumerate(zip(ANGLES, frame_paths, frames), start=1):
        bounds = v1.alpha_bounds(frame)
        frame_records.append({"frame": index, "angleDegrees": angle, "file": rel(path), "sha256": v2.digest(path), "sourceV3Sha256": v2.digest(prior_frames[index - 1]), "change": "boot-geometry-and-palette-only-below-y250" if index == 8 else "none-byte-identical", "opaqueBoundsExclusive": list(bounds), "opaqueHeight": bounds[3] - bounds[1], "edgeAlphaPixels": v1.edge_alpha_count(frame)})
    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v4", "status": "draft-side-back-turn-v4-boot-geometry-awaiting-visual-approval", "purpose": "Remove the F7→F8 boot-construction snap while preserving the V3 full-outfit palette and exact F8 pixels above the boot line.",
        "priorDraft": {"register": rel(PRIOR_REGISTER), "registerSha256": v2.digest(PRIOR_REGISTER)}, "palette": {"file": rel(PALETTE), "sha256": v2.digest(PALETTE), "status": palette["status"]},
        "generation": {"tool": "built-in image editing", "source": rel(GENERATED_SOURCE), "sourceSha256": v2.digest(GENERATED_SOURCE), "cleanSource": rel(clean_source), "cleanSourceSha256": v2.digest(clean_source), "registration": registration, "acceptedRegion": {"minYInclusive": BOOT_CUT_Y, "maxYExclusive": 320}, "rejectedRegion": {"minYInclusive": 0, "maxYExclusive": BOOT_CUT_Y, "reason": "generated redraw outside the boots is not used"}, "creativePixelWarp": False},
        "bootRedraw": {"cutY": BOOT_CUT_Y, "changedPixels": changed_pixels, "changedMask": rel(mask_path), "changedMaskSha256": v2.digest(mask_path), "paletteCheck": palette_check, "metrics": {"f7": boot_metrics(frames[-2]), "f8V3": boot_metrics(original), "f8V4": boot_metrics(candidate)}},
        "frames": frame_records,
        "animation": {"fps": FPS, "cell": list(CELL), "forward": {"file": rel(forward), "sha256": v2.digest(forward), "sidecar": rel(forward_sidecar), "sidecarSha256": v2.digest(forward_sidecar)}, "reverse": {"file": rel(reverse), "sha256": v2.digest(reverse), "sidecar": rel(reverse_sidecar), "sidecarSha256": v2.digest(reverse_sidecar), "exactFrameOrderReverse": True}},
        "evidence": {"comparison": {"file": rel(comparison_path), "sha256": v2.digest(comparison_path)}, "ghostOverlay": {"file": rel(overlay_path), "sha256": v2.digest(overlay_path)}, "contactSheet": {"file": rel(contact_path), "sha256": v2.digest(contact_path)}},
        "validation": {"frames1To7ByteIdenticalToV3": True, "frame8RowsAbove250ByteIdenticalToV3": candidate.crop((0, 0, 256, BOOT_CUT_Y)).tobytes() == original.crop((0, 0, 256, BOOT_CUT_Y)).tobytes(), "frame8ChangesConfinedToY250AndBelow": True, "frame8CapTopAndFloorStable": v1.alpha_bounds(candidate)[1] == 18 and v1.alpha_bounds(candidate)[3] == 316, "everyFrameTransparentCellEdge": all(item["edgeAlphaPixels"] == 0 for item in frame_records), "productionSpritesChanged": False, "runtimeManifestChanged": False, "approvedBackMasterChanged": False, "priorDraftsChanged": False},
        "approvalBoundary": {"sideBackTurnV4Approved": False, "rearBootEndpointApproved": False, "standardOutfitPaletteApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank visually reviews F7→F8 boot continuity in both directions before V4 can replace V3 as the review candidate.", "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1–V3, approved authorities and production remain unchanged."
    }
    v2.dump(PACK / "batch-register.json", register); write_page(frame_paths, comparison_path, contact_path)
    print(json.dumps({"batch": register["batchId"], "changedPixels": changed_pixels, "metrics": register["bootRedraw"]["metrics"], "bootMedianV": palette_check, "public": rel(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__": main()
