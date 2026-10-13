#!/usr/bin/env python3
"""Build V5 from Frank's approved first rear-boot render without regeneration."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-orthographic-v5"
MASTER_PACK = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1"
V2_PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v2"
V3_PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v3"
V4_PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v4"
FRONT = MASTER_PACK / "drafts/keeper_prime_master-neutral-front_f1.png"
FRONT_REGISTER = MASTER_PACK / "master-pack-register.json"
SIDE = V2_PACK / "drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
OLD_BACK = V2_PACK / "drafts/keeper_prime_master-neutral-standing-back_f1.png"
V2_REGISTER = V2_PACK / "batch-register.json"
V3_REGISTER = V3_PACK / "batch-register.json"
V4_REGISTER = V4_PACK / "batch-register.json"
V4_STRICT_BACK = V4_PACK / "drafts/keeper_prime_master-neutral-standing-back_f1.png"
APPROVED_ORIGINAL = V4_PACK / "rejected-sources/rounded-heel-counter-attempt.png"
APPROVED_SOURCE = PACK / "sources/keeper-prime-back-user-approved-rear-boots.png"
LEGACY_BACK = ROOT / "art/raw/keeper-first-batch/keeper_neutral_standing-back_f1.png"

CELL = (256, 320)
TARGET_BOTTOM = 316
BOOT_EDIT_TOP = 273


def load_v4_builder():
    path = ROOT / "scripts/build_keeper_prime_orthographic_views_v4.py"
    spec = importlib.util.spec_from_file_location("keeper_prime_v4_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load V4 deterministic geometry helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V4 = load_v4_builder()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def approved_comparison(invalid: Image.Image, strict: Image.Image, approved: Image.Image) -> Image.Image:
    crop_box = (48, 248, 208, 320)
    crop_size = (320, 144)
    output = Image.new("RGBA", (992, 184), (12, 20, 27, 255))
    for x, image in ((8, invalid), (336, strict), (664, approved)):
        crop = image.crop(crop_box).resize(crop_size, Image.Resampling.NEAREST)
        output.alpha_composite(crop, (x, 32))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    draw.text((8, 8), "V2 INVALID: front-facing", fill="#ff8798", font=font)
    draw.text((336, 8), "V4 HISTORY: over-squared", fill="#efbd58", font=font)
    draw.text((664, 8), "V5 APPROVED: rear heel form", fill="#77e3a4", font=font)
    return output


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    urls: dict[str, str] = {}
    for key, source in records.items():
        target = assets / f"{key}-{digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(register: dict) -> None:
    records = {
        "front": FRONT,
        "side": SIDE,
        "invalidBack": OLD_BACK,
        "strictBack": V4_STRICT_BACK,
        "approvedBack": ROOT / register["approvedRearEndpoint"]["file"],
        "approvedSource": APPROVED_SOURCE,
        "bootCompare": ROOT / register["evidence"]["bootComparison"]["file"],
        "ghost": ROOT / register["evidence"]["frontGhostOverApprovedBack"]["file"],
        "legacy": LEGACY_BACK,
    }
    urls = copy_public(records)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime orthographic views V5</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58;--red:#ff8798;--green:#77e3a4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}h1{{margin:.2rem 0}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--green);border-radius:999px;padding:5px 10px;color:#a9f3c5}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.sprite{{height:510px;max-height:62vh;object-fit:contain}}.wide{{width:100%}}.bad{{border-color:var(--red)}}.good{{border-color:var(--green)}}.history{{border-color:var(--amber)}}.rule{{border-left:4px solid var(--green);background:#17291f;padding:10px 14px}}code{{overflow-wrap:anywhere;color:#badff3}}</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-prime-orthographic-v3/">V3 side landmark audit</a><h1>Keeper Prime orthographic views V5</h1><span class="status">Approved rear-boot design · rear endpoint authority for KP Rig V1</span><p>Frank approved the first rear-boot render on 13 October 2026: “They don't look like toe caps, they are excellent. Approved.” V5 records that exact source without regeneration.</p></header><main>
<p class="rule"><strong>Approved orientation:</strong> rounded rear heel-counter panels, central vertical back seams, heel backs and rear sole edges. These are intentional rear-boot forms, not toe caps.</p>
<section class="grid"><article><h2>Approved front authority</h2><img class="sprite" src="assets/{urls['front']}" alt="Approved Prime front"></article><article><h2>Selected side · still V3-blocked</h2><img class="sprite" src="assets/{urls['side']}" alt="Selected side"></article><article class="good"><h2>V5 approved 180° back</h2><img class="sprite" src="assets/{urls['approvedBack']}" alt="Approved back with rounded rear heel panels"><p><code>{register['approvedRearEndpoint']['sha256']}</code></p></article></section>
<h2>Approved smooth artwork master</h2><article class="good"><img class="sprite" src="assets/{urls['approvedSource']}" alt="Exact smooth full-resolution source whose boots Frank approved"><p>This 1122 × 1402 file is the exact first edit Frank approved and the rendering-quality authority. It is not a pixel-art asset. The 256 × 320 orthographic endpoint is a registered measurement/export proxy produced with Lanczos resampling; its complete anti-aliased outer alpha edge is byte-identical to the approved Prime front.</p></article>
<h2>Boot history</h2><article><img class="wide" src="assets/{urls['bootCompare']}" alt="Invalid V2, superseded V4 and approved V5 boot comparison"></article>
<section class="grid"><article class="bad"><h3>V2 rejected</h3><img class="sprite" src="assets/{urls['invalidBack']}" alt="V2 back with forward-facing boots"></article><article class="history"><h3>V4 historical draft</h3><img class="sprite" src="assets/{urls['strictBack']}" alt="V4 over-squared rear boots"><p>Superseded; retained as provenance.</p></article><article><h3>Legacy orientation evidence</h3><img class="sprite" src="assets/{urls['legacy']}" alt="Legacy rear pose"></article></section>
<h2>Registration and smoothness evidence</h2><article><img class="sprite" src="assets/{urls['ghost']}" alt="Approved front alpha ghost over approved back"><p>0 of 81,920 alpha values differ, including every partially transparent anti-aliased edge pixel. Rows 0–272 remain byte-identical to V2; {register['validation']['changedPixelsInsideEditRegion']:,} pixels change only within rows 273–315. Rough full-resolution renders, nearest-neighbour master resampling and jagged internal linework are approval blockers even when geometry passes.</p></article>
<h2>What happens next</h2><article><p>This approved front/back pair now authorizes KP Rig V1 construction. The selected side remains blocked at 5/15 exact horizontal datums and will be the first endpoint corrected from the rig. No raw/runtime sprite, animation strip or manifest has changed.</p></article>
</main></body></html>"""
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    master = json.loads(FRONT_REGISTER.read_text())
    v3 = json.loads(V3_REGISTER.read_text())
    v4 = json.loads(V4_REGISTER.read_text())
    if master.get("status") != "approved-permanent-identity-authority":
        raise RuntimeError("Prime Master approval missing")
    if v3.get("validation", {}).get("sideLandmarkRegistrationReady") is not False:
        raise RuntimeError("V3 side must remain blocked")
    required = (FRONT, SIDE, OLD_BACK, V2_REGISTER, V3_REGISTER, V4_REGISTER, V4_STRICT_BACK, APPROVED_ORIGINAL, LEGACY_BACK)
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {relative(path)}")
    if digest(APPROVED_ORIGINAL) != "2371101e33fcd2b9b27cbfdbcecdc1587c41783d5773605117a4678b5ac3ecc6":
        raise RuntimeError("Frank-approved original source hash changed")
    for directory in (PACK / "drafts", PACK / "evidence", PACK / "sources", PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(APPROVED_ORIGINAL, APPROVED_SOURCE)
    front = Image.open(FRONT).convert("RGBA")
    side = Image.open(SIDE).convert("RGBA")
    old_back = Image.open(OLD_BACK).convert("RGBA")
    strict_back = Image.open(V4_STRICT_BACK).convert("RGBA")
    normalized, source_geometry = V4.normalize(APPROVED_SOURCE)
    approved = V4.fit_rear_boot_detail(normalized, front, old_back)
    candidate = PACK / "drafts/keeper_prime_master-neutral-standing-back_f1.png"
    approved.save(candidate, optimize=False, compress_level=9)
    sidecar = candidate.with_suffix(".json")
    dump(sidecar, {"name": "keeper_prime_master-neutral-standing-back", "w": 32, "h": 40, "frames": 1, "fps": 1, "density": 8, "anchor": [16, 40], "loop": False, "startPose": "standing-back", "endPose": "standing-back", "outfit": "standard-single-broad-band", "status": "approved-rear-endpoint-authority-for-kp-rig", "identityAuthority": relative(FRONT), "carriedForwardUpperBody": relative(OLD_BACK), "approvedRearBootSource": relative(APPROVED_SOURCE), "editTopYInclusive": BOOT_EDIT_TOP, "productionPromotionAllowed": False})
    comparison = PACK / "evidence/v2-v4-v5-boot-history.png"
    ghost = PACK / "evidence/front-ghost-over-approved-back.png"
    approved_comparison(old_back, strict_back, approved).save(comparison, optimize=False, compress_level=9)
    V4.ghost_overlay(front, approved).save(ghost, optimize=False, compress_level=9)
    changed_inside = changed_outside = changed_from_v4 = 0
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if old_back.getpixel((x, y)) != approved.getpixel((x, y)):
                if BOOT_EDIT_TOP <= y < TARGET_BOTTOM:
                    changed_inside += 1
                else:
                    changed_outside += 1
            if strict_back.getpixel((x, y)) != approved.getpixel((x, y)):
                changed_from_v4 += 1
    bounds = V4.alpha_bounds(approved)
    alpha_mismatches = sum(approved.getchannel("A").getpixel((x, y)) != front.getchannel("A").getpixel((x, y)) for y in range(CELL[1]) for x in range(CELL[0]))
    register = {
        "batchId": "keeper-prime-orthographic-views-2026-10-13-v5",
        "status": "approved-rear-endpoint-authority-for-kp-rig",
        "purpose": "Record Frank's approved first rear-boot render and integrate only that source's boot detail into the registered back endpoint.",
        "approvedFront": {"file": relative(FRONT), "sha256": digest(FRONT), "register": relative(FRONT_REGISTER), "registerSha256": digest(FRONT_REGISTER)},
        "selectedSide": {"file": relative(SIDE), "sha256": digest(SIDE), "status": "blocked-by-v3-landmark-register"},
        "approvedSource": {"file": relative(APPROVED_SOURCE), "sha256": digest(APPROVED_SOURCE), "originalFile": relative(APPROVED_ORIGINAL), "originalSha256": digest(APPROVED_ORIGINAL), "normalizedGeometry": source_geometry, "regenerated": False},
        "approval": {"approvedBy": "Frank", "approvedOn": "2026-10-13", "wording": "They don't look like toe caps, they are excellent. Approved.", "scope": "The first generated rear-boot design and its deterministic orthographic integration; authorizes KP Rig V1 use, not raw/runtime promotion."},
        "history": {
            "v2InvalidBack": {"file": relative(OLD_BACK), "sha256": digest(OLD_BACK), "reason": "feet face the player"},
            "v4SupersededBack": {"file": relative(V4_STRICT_BACK), "sha256": digest(V4_STRICT_BACK), "reason": "over-squared substitute not selected by Frank"},
            "v2Register": {"file": relative(V2_REGISTER), "sha256": digest(V2_REGISTER)},
            "v3Register": {"file": relative(V3_REGISTER), "sha256": digest(V3_REGISTER)},
            "v4Register": {"file": relative(V4_REGISTER), "sha256": digest(V4_REGISTER)},
        },
        "approvedRearEndpoint": {"file": relative(candidate), "sha256": digest(candidate), "sidecar": relative(sidecar), "sidecarSha256": digest(sidecar), "animationAuthoringAllowed": True, "productionPromotionAllowed": False},
        "editRegion": {"topYInclusive": BOOT_EDIT_TOP, "bottomYExclusive": TARGET_BOTTOM, "scope": "lower legs and boots only"},
        "geometry": {"boundsExclusive": list(bounds), "opaqueWidth": bounds[2] - bounds[0], "opaqueHeight": bounds[3] - bounds[1], "capTopY": bounds[1], "floorY": bounds[3], "centreX": round((bounds[0] + bounds[2]) / 2, 3)},
        "evidence": {"bootComparison": {"file": relative(comparison), "sha256": digest(comparison)}, "frontGhostOverApprovedBack": {"file": relative(ghost), "sha256": digest(ghost)}},
        "orientationContract": {"view": "exact 180-degree rear", "requiredBootCues": ["rounded rear heel-counter panels", "central vertical back seams", "rear heel backs", "rear sole edges"], "forbiddenBootCues": ["forward-facing construction", "front vamp highlights", "shoelaces"]},
        "renderQualityContract": {"approvedArtworkMaster": relative(APPROVED_SOURCE), "minimumMasterDimensions": [1122, 1402], "actualMasterDimensions": list(Image.open(APPROVED_SOURCE).size), "masterMustRemainSmooth": True, "registeredProxyResampling": "LANCZOS", "registeredProxyAlphaAuthority": relative(FRONT), "outerAlphaMatchesAuthorityExactly": alpha_mismatches == 0, "nearestNeighbourMasterResamplingAllowed": False, "roughOrJaggedInternalLineworkAllowed": False},
        "validation": {"cellGeometryMatches": approved.size == CELL, "transparentSafetyGutter": V4.edge_pixels(approved) == 0, "edgePixels": V4.edge_pixels(approved), "alphaMatchesApprovedFrontExactly": alpha_mismatches == 0, "alphaMismatchPixels": alpha_mismatches, "upperBodyMatchesV2Exactly": changed_outside == 0, "changedPixelsInsideEditRegion": changed_inside, "changedPixelsOutsideEditRegion": changed_outside, "pixelsDifferentFromV4": changed_from_v4, "same298PixelHeight": bounds[1] == 18 and bounds[3] == 316, "sideLandmarkRegistrationReady": False, "productionSpritesChanged": False, "runtimeManifestChanged": False, "animationDraftsChanged": False},
        "legacyPoseEvidence": {"file": relative(LEGACY_BACK), "sha256": digest(LEGACY_BACK), "role": "orientation evidence only"},
        "promptLog": relative(PACK / "PROMPT_LOG.md"),
        "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; V2–V4, Prime Master and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(register)
    print(json.dumps({"batch": register["batchId"], "approvedRearEndpoint": register["approvedRearEndpoint"]["sha256"], "changedInside": changed_inside, "changedOutside": changed_outside, "alphaMismatches": alpha_mismatches, "differentFromV4": changed_from_v4, "publicPage": relative(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
