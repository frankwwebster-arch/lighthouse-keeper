#!/usr/bin/env python3
"""Build V4 with rear-facing boot detail and an unchanged V2 upper body."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v4"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-orthographic-v4"
MASTER_PACK = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1"
V2_PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v2"
V3_PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v3"
FRONT = MASTER_PACK / "drafts/keeper_prime_master-neutral-front_f1.png"
FRONT_REGISTER = MASTER_PACK / "master-pack-register.json"
SIDE = V2_PACK / "drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
OLD_BACK = V2_PACK / "drafts/keeper_prime_master-neutral-standing-back_f1.png"
V2_REGISTER = V2_PACK / "batch-register.json"
V3_REGISTER = V3_PACK / "batch-register.json"
GENERATED = PACK / "sources/keeper-prime-back-rear-boots-generated.png"
REJECTED_ROUNDED = PACK / "rejected-sources/rounded-heel-counter-attempt.png"
LEGACY_BACK = ROOT / "art/raw/keeper-first-batch/keeper_neutral_standing-back_f1.png"

CELL = (256, 320)
TARGET_TOP = 18
TARGET_BOTTOM = 316
BOOT_EDIT_TOP = 273
ALPHA_THRESHOLD = 8


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bounds(image: Image.Image, threshold: int = 1) -> tuple[int, int, int, int]:
    box = image.getchannel("A").point(lambda value: 255 if value >= threshold else 0).getbbox()
    if box is None:
        raise RuntimeError("empty image")
    return box


def normalize(source_path: Path) -> tuple[Image.Image, dict]:
    source = Image.open(source_path).convert("RGBA")
    source_box = alpha_bounds(source, ALPHA_THRESHOLD)
    crop = source.crop(source_box)
    target_height = TARGET_BOTTOM - TARGET_TOP
    target_width = round(crop.width * target_height / crop.height)
    if target_width > CELL[0] - 16:
        raise RuntimeError("generated source cannot retain the safety gutter")
    resized = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    output.alpha_composite(resized, ((CELL[0] - target_width) // 2, TARGET_TOP))
    pixels = output.load()
    for y in range(output.height):
        for x in range(output.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha < ALPHA_THRESHOLD:
                pixels[x, y] = (0, 0, 0, 0)
    return output, {
        "sourcePixels": list(source.size),
        "sourceSignificantAlphaBoundsExclusive": list(source_box),
        "normalizedBoundsExclusive": list(alpha_bounds(output)),
    }


def runs(xs: list[int]) -> list[tuple[int, int]]:
    if not xs:
        return []
    result = []
    start = previous = xs[0]
    for value in xs[1:]:
        if value != previous + 1:
            result.append((start, previous + 1))
            start = value
        previous = value
    result.append((start, previous + 1))
    return [run for run in result if run[1] - run[0] >= 2]


def fit_rear_boot_detail(source: Image.Image, authority: Image.Image, original: Image.Image) -> Image.Image:
    """Fit generated rear boot RGB into the exact authority alpha components."""
    output = original.copy()
    source_alpha = source.getchannel("A")
    target_alpha = authority.getchannel("A")
    for y in range(BOOT_EDIT_TOP, TARGET_BOTTOM):
        source_runs = runs([x for x in range(CELL[0]) if source_alpha.getpixel((x, y)) >= ALPHA_THRESHOLD])
        target_runs = runs([x for x in range(CELL[0]) if target_alpha.getpixel((x, y)) >= ALPHA_THRESHOLD])
        if not source_runs or not target_runs:
            continue
        if len(source_runs) != len(target_runs):
            source_runs = [(source_runs[0][0], source_runs[-1][1])]
            target_runs = [(target_runs[0][0], target_runs[-1][1])]
        for (source_left, source_right), (target_left, target_right) in zip(source_runs, target_runs):
            row = Image.new("RGB", (source_right - source_left, 1))
            for offset, x in enumerate(range(source_left, source_right)):
                red, green, blue, _ = source.getpixel((x, y))
                row.putpixel((offset, 0), (red, green, blue))
            row = row.resize((target_right - target_left, 1), Image.Resampling.LANCZOS)
            for offset, x in enumerate(range(target_left, target_right)):
                alpha = target_alpha.getpixel((x, y))
                if alpha:
                    red, green, blue = row.getpixel((offset, 0))
                    output.putpixel((x, y), (red, green, blue, alpha))
    output.putalpha(target_alpha)
    return output


def edge_pixels(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(alpha.getpixel((x, y)) > 0 for x in range(image.width) for y in range(image.height) if x in (0, image.width - 1) or y in (0, image.height - 1))


def checkerboard(size: tuple[int, int] = CELL) -> Image.Image:
    image = Image.new("RGBA", size, (29, 40, 49, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], 16):
        for x in range(0, size[0], 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, min(size[0] - 1, x + 15), min(size[1] - 1, y + 15)), fill=(41, 55, 65, 255))
    return image


def ghost_overlay(front: Image.Image, candidate: Image.Image) -> Image.Image:
    stage = checkerboard()
    stage.alpha_composite(candidate)
    ghost = Image.new("RGBA", CELL, (43, 213, 255, 0))
    ghost.putalpha(front.getchannel("A").point(lambda value: 72 if value else 0))
    stage.alpha_composite(ghost)
    draw = ImageDraw.Draw(stage)
    draw.line((128, 0, 128, 319), fill="#ffffff", width=1)
    draw.line((0, 18, 255, 18), fill="#f7d35c", width=1)
    draw.line((0, 316, 255, 316), fill="#ffffff", width=1)
    draw.text((6, 6), "cyan: approved front alpha", fill="#ffffff", font=ImageFont.load_default())
    return stage


def boot_comparison(old: Image.Image, corrected: Image.Image) -> Image.Image:
    crop_box = (48, 248, 208, 320)
    scale = 3
    old_crop = old.crop(crop_box).resize((480, 216), Image.Resampling.NEAREST)
    new_crop = corrected.crop(crop_box).resize((480, 216), Image.Resampling.NEAREST)
    output = Image.new("RGBA", (992, 254), (12, 20, 27, 255))
    output.alpha_composite(old_crop, (8, 30))
    output.alpha_composite(new_crop, (504, 30))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    draw.text((8, 8), "V2 INVALID: front toe caps", fill="#ff8798", font=font)
    draw.text((504, 8), "V4 PROPOSAL: rear heel counters + back seams", fill="#77e3a4", font=font)
    return output


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    urls = {}
    for key, source in records.items():
        target = assets / f"{key}-{digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(register: dict) -> None:
    records = {
        "front": FRONT,
        "side": SIDE,
        "oldBack": OLD_BACK,
        "newBack": ROOT / register["candidate"]["file"],
        "bootCompare": ROOT / register["evidence"]["bootComparison"]["file"],
        "ghost": ROOT / register["evidence"]["frontGhostOverCorrectedBack"]["file"],
        "legacy": LEGACY_BACK,
    }
    urls = copy_public(records)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime orthographic views V4</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58;--red:#ff8798;--green:#77e3a4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}h1{{margin:.2rem 0}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe09e}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.sprite{{height:510px;max-height:62vh;object-fit:contain}}.wide{{width:100%}}.bad{{border-color:var(--red)}}.good{{border-color:var(--green)}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}code{{overflow-wrap:anywhere;color:#badff3}}</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-prime-orthographic-v3/">V3 side landmark audit</a><h1>Keeper Prime orthographic views V4</h1><span class="status">Draft · corrected rear-facing boots awaiting visual approval</span><p>The V2 back is invalid because its feet face the player. V4 changes only the registered lower-leg/boot region and promotes nothing.</p></header><main>
<p class="rule"><strong>Orientation correction:</strong> rounded front toe caps are removed. The proposed boots show flat squared heel backs, rectangular heel-counter panels, vertical back seams and rear sole edges. The complete alpha silhouette remains byte-identical to the approved front.</p>
<section class="grid"><article><h2>Approved front authority</h2><img class="sprite" src="assets/{urls['front']}" alt="Approved Prime front"></article><article><h2>Selected side · still V3-blocked</h2><img class="sprite" src="assets/{urls['side']}" alt="Selected side"></article><article class="good"><h2>V4 corrected 180° back</h2><img class="sprite" src="assets/{urls['newBack']}" alt="Corrected back with rear-facing boots"><p><code>{register['candidate']['sha256']}</code></p></article></section>
<h2>Boot orientation close-up</h2><article><img class="wide" src="assets/{urls['bootCompare']}" alt="Invalid front-facing boots beside corrected rear-facing boots"></article>
<h2>Rejected V2 back</h2><section class="grid"><article class="bad"><h3>V2 · front-facing feet</h3><img class="sprite" src="assets/{urls['oldBack']}" alt="Rejected V2 back with front-facing boots"><p>Rejected provenance only.</p></article><article><h3>Legacy rear-pose evidence</h3><img class="sprite" src="assets/{urls['legacy']}" alt="Legacy rear pose with rear-facing boot construction"><p>Pose/orientation evidence only; not a rendering target.</p></article><article><h3>V4 front ghost overlay</h3><img class="sprite" src="assets/{urls['ghost']}" alt="Approved front alpha ghost over corrected back"><p>0 of 81,920 alpha values differ.</p></article></section>
<h2>Deterministic boundary</h2><article><p>Rows 0–272 are byte-identical to V2. The edit begins at source y={register['editRegion']['topYInclusive']} and ends at y={register['editRegion']['bottomYExclusive'] - 1}. {register['validation']['changedPixelsInsideEditRegion']:,} pixels change inside that region; {register['validation']['changedPixelsOutsideEditRegion']} change outside it. Cap y=18, floor y=316, 298-pixel height, centreline and transparent gutter are unchanged.</p></article>
<h2>Approval boundary</h2><article><p>Approval would accept only the corrected back endpoint for later rig construction. The selected side remains blocked by the V3 15-point landmark register. No animation, raw/runtime sprite or manifest has changed.</p></article>
</main></body></html>"""
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    master = json.loads(FRONT_REGISTER.read_text())
    v2 = json.loads(V2_REGISTER.read_text())
    v3 = json.loads(V3_REGISTER.read_text())
    if master.get("status") != "approved-permanent-identity-authority":
        raise RuntimeError("Prime Master approval missing")
    if v3.get("validation", {}).get("sideLandmarkRegistrationReady") is not False:
        raise RuntimeError("V3 side must remain blocked")
    for required in (FRONT, SIDE, OLD_BACK, V2_REGISTER, V3_REGISTER, GENERATED, REJECTED_ROUNDED, LEGACY_BACK):
        if not required.exists():
            raise RuntimeError(f"missing {relative(required)}")
    for directory in (PACK / "drafts", PACK / "evidence", PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    front = Image.open(FRONT).convert("RGBA")
    side = Image.open(SIDE).convert("RGBA")
    old_back = Image.open(OLD_BACK).convert("RGBA")
    normalized, generated_geometry = normalize(GENERATED)
    corrected = fit_rear_boot_detail(normalized, front, old_back)
    candidate = PACK / "drafts/keeper_prime_master-neutral-standing-back_f1.png"
    corrected.save(candidate, optimize=False, compress_level=9)
    sidecar = candidate.with_suffix(".json")
    dump(sidecar, {"name": "keeper_prime_master-neutral-standing-back", "w": 32, "h": 40, "frames": 1, "fps": 1, "density": 8, "anchor": [16, 40], "loop": False, "startPose": "standing-back", "endPose": "standing-back", "outfit": "standard-single-broad-band", "status": "draft-awaiting-visual-approval", "identityAuthority": relative(FRONT), "carriedForwardUpperBody": relative(OLD_BACK), "generatedRearBootSource": relative(GENERATED), "editTopYInclusive": BOOT_EDIT_TOP})
    boot_evidence = PACK / "evidence/v2-v4-boot-orientation-comparison.png"
    ghost_evidence = PACK / "evidence/front-ghost-over-corrected-back.png"
    boot_comparison(old_back, corrected).save(boot_evidence, optimize=False, compress_level=9)
    ghost_overlay(front, corrected).save(ghost_evidence, optimize=False, compress_level=9)
    changed_inside = changed_outside = 0
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if old_back.getpixel((x, y)) != corrected.getpixel((x, y)):
                if BOOT_EDIT_TOP <= y < TARGET_BOTTOM:
                    changed_inside += 1
                else:
                    changed_outside += 1
    bounds = alpha_bounds(corrected)
    alpha_mismatches = sum(corrected.getchannel("A").getpixel((x, y)) != front.getchannel("A").getpixel((x, y)) for y in range(CELL[1]) for x in range(CELL[0]))
    register = {
        "batchId": "keeper-prime-orthographic-views-2026-10-13-v4",
        "status": "draft-back-boot-correction-awaiting-visual-approval",
        "purpose": "Correct the invalid front-facing boots in the 180-degree rear endpoint before KP Rig construction.",
        "approvedFront": {"file": relative(FRONT), "sha256": digest(FRONT), "register": relative(FRONT_REGISTER), "registerSha256": digest(FRONT_REGISTER)},
        "selectedSide": {"file": relative(SIDE), "sha256": digest(SIDE), "status": "blocked-by-v3-landmark-register"},
        "rejectedV2Back": {"file": relative(OLD_BACK), "sha256": digest(OLD_BACK), "reason": "feet retain front-facing toe-cap construction"},
        "immutablePredecessors": {"v2Register": relative(V2_REGISTER), "v2RegisterSha256": digest(V2_REGISTER), "v3Register": relative(V3_REGISTER), "v3RegisterSha256": digest(V3_REGISTER)},
        "generatedSource": {"file": relative(GENERATED), "sha256": digest(GENERATED), "normalizedGeometry": generated_geometry},
        "rejectedGeneratedAttempt": {"file": relative(REJECTED_ROUNDED), "sha256": digest(REJECTED_ROUNDED), "reason": "rear seams improved orientation, but rounded heel counters remained too easy to read as toe caps"},
        "legacyPoseEvidence": {"file": relative(LEGACY_BACK), "sha256": digest(LEGACY_BACK), "role": "rear boot orientation only"},
        "candidate": {"file": relative(candidate), "sha256": digest(candidate), "sidecar": relative(sidecar), "sidecarSha256": digest(sidecar), "promotionAllowed": False},
        "editRegion": {"topYInclusive": BOOT_EDIT_TOP, "bottomYExclusive": TARGET_BOTTOM, "scope": "lower legs and boots only"},
        "geometry": {"boundsExclusive": list(bounds), "opaqueWidth": bounds[2] - bounds[0], "opaqueHeight": bounds[3] - bounds[1], "capTopY": bounds[1], "floorY": bounds[3], "centreX": round((bounds[0] + bounds[2]) / 2, 3)},
        "evidence": {"bootComparison": {"file": relative(boot_evidence), "sha256": digest(boot_evidence)}, "frontGhostOverCorrectedBack": {"file": relative(ghost_evidence), "sha256": digest(ghost_evidence)}},
        "orientationContract": {"view": "exact 180-degree rear", "requiredBootCues": ["flat squared heel backs", "rectangular heel-counter panels", "vertical back seams", "rear sole edges"], "forbiddenBootCues": ["front toe caps", "rounded toe-like panels", "front vamp highlights", "shoelaces"]},
        "validation": {"cellGeometryMatches": corrected.size == CELL, "transparentSafetyGutter": edge_pixels(corrected) == 0, "edgePixels": edge_pixels(corrected), "alphaMatchesApprovedFrontExactly": alpha_mismatches == 0, "alphaMismatchPixels": alpha_mismatches, "upperBodyMatchesV2Exactly": changed_outside == 0, "changedPixelsInsideEditRegion": changed_inside, "changedPixelsOutsideEditRegion": changed_outside, "same298PixelHeight": bounds[1] == 18 and bounds[3] == 316, "sideLandmarkRegistrationReady": False, "productionSpritesChanged": False, "runtimeManifestChanged": False, "animationDraftsChanged": False},
        "promptLog": relative(PACK / "PROMPT_LOG.md"),
        "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; V2, V3, Prime Master and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(register)
    print(json.dumps({"batch": register["batchId"], "candidate": register["candidate"]["sha256"], "changedInside": changed_inside, "changedOutside": changed_outside, "alphaMismatches": alpha_mismatches, "publicPage": relative(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
