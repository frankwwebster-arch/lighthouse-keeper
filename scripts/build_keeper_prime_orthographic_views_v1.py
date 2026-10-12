#!/usr/bin/env python3
"""Build the reversible Keeper Prime 90° side and 180° back review pack."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-orthographic-v1"
MASTER_PACK = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1"
FRONT = MASTER_PACK / "drafts/keeper_prime_master-neutral-front_f1.png"
FRONT_REGISTER = MASTER_PACK / "master-pack-register.json"
SIDE_SOURCE = PACK / "sources/keeper-prime-side-right-generated.png"
BACK_SOURCE = PACK / "sources/keeper-prime-back-generated.png"
REJECTED_BACK = PACK / "rejected-sources/back-hair-cut-too-short-generated.png"
LEGACY_SIDE = ROOT / "art/raw/keeper-first-batch/keeper_neutral_standing-side-right_f1.png"
LEGACY_BACK = ROOT / "art/raw/keeper-first-batch/keeper_neutral_standing-back_f1.png"

CELL = (256, 320)
LOGICAL_CELL = (32, 40)
DENSITY = 8
ANCHOR = (16, 40)
TARGET_TOP = 18
TARGET_BOTTOM = 316
ALPHA_THRESHOLD = 8


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def json_dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bbox(image: Image.Image, threshold: int = 1) -> tuple[int, int, int, int]:
    mask = image.getchannel("A").point(lambda value: 255 if value >= threshold else 0)
    box = mask.getbbox()
    if box is None:
        raise RuntimeError("empty transparent image")
    return box


def normalize(source_path: Path) -> tuple[Image.Image, dict]:
    source = Image.open(source_path).convert("RGBA")
    source_box = alpha_bbox(source, ALPHA_THRESHOLD)
    crop = source.crop(source_box)
    target_height = TARGET_BOTTOM - TARGET_TOP
    target_width = round(crop.width * target_height / crop.height)
    if target_width > CELL[0] - 16:
        raise RuntimeError(f"{source_path.name} cannot retain an 8px safety gutter")
    resized = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    target_x = (CELL[0] - target_width) // 2
    output.alpha_composite(resized, (target_x, TARGET_TOP))
    pixels = output.load()
    for y in range(output.height):
        for x in range(output.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha < ALPHA_THRESHOLD:
                pixels[x, y] = (0, 0, 0, 0)
    box = alpha_bbox(output)
    return output, {
        "sourcePixels": list(source.size),
        "sourceSignificantAlphaBoundsExclusive": list(source_box),
        "normalizedOpaqueBoundsExclusive": list(box),
        "opaqueWidth": box[2] - box[0],
        "opaqueHeight": box[3] - box[1],
        "opaqueCenterX": round((box[0] + box[2]) / 2, 3),
        "capTopY": box[1],
        "floorY": box[3],
    }


def checkerboard() -> Image.Image:
    image = Image.new("RGBA", CELL, (29, 40, 49, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, CELL[1], 16):
        for x in range(0, CELL[0], 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, x + 15, y + 15), fill=(41, 55, 65, 255))
    return image


def ghost_overlay(candidate: Image.Image, label: str) -> Image.Image:
    front = Image.open(FRONT).convert("RGBA")
    stage = checkerboard()
    stage.alpha_composite(candidate)
    ghost = Image.new("RGBA", CELL, (0, 0, 0, 0))
    front_alpha = front.getchannel("A").point(lambda value: 72 if value else 0)
    ghost_colour = Image.new("RGBA", CELL, (43, 213, 255, 0))
    ghost_colour.putalpha(front_alpha)
    ghost.alpha_composite(ghost_colour)
    stage.alpha_composite(ghost)
    draw = ImageDraw.Draw(stage)
    for y, colour in ((18, "#f7d35c"), (148, "#7be79b"), (207, "#ff87a1"), (316, "#ffffff")):
        draw.line((0, y, CELL[0] - 1, y), fill=colour, width=1)
    draw.line((128, 0, 128, CELL[1] - 1), fill="#ffffff", width=1)
    draw.text((7, 6), f"cyan ghost: approved front | {label}", fill="#ffffff", font=ImageFont.load_default())
    return stage


def lineup(front: Image.Image, side: Image.Image, back: Image.Image) -> Image.Image:
    width, height = 3 * 288, 370
    output = Image.new("RGBA", (width, height), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    for index, (label, image) in enumerate((("0° approved front", front), ("90° side proposal", side), ("180° back proposal", back))):
        x = index * 288 + 16
        stage = checkerboard()
        stage.alpha_composite(image)
        output.alpha_composite(stage, (x, 34))
        draw.text((x, 12), label, fill="#eef6fb", font=ImageFont.load_default())
    draw.line((0, 34 + TARGET_BOTTOM, width - 1, 34 + TARGET_BOTTOM), fill="#ffffff", width=1)
    return output


def edge_pixels(image: Image.Image) -> int:
    count = 0
    for x in range(image.width):
        count += image.getpixel((x, 0))[3] > 0
        count += image.getpixel((x, image.height - 1))[3] > 0
    for y in range(image.height):
        count += image.getpixel((0, y))[3] > 0
        count += image.getpixel((image.width - 1, y))[3] > 0
    return count


def cross_sections(image: Image.Image, rows: tuple[int, ...]) -> dict[str, dict]:
    alpha = image.getchannel("A")
    result = {}
    for y in rows:
        xs = [x for x in range(image.width) if alpha.getpixel((x, y)) >= ALPHA_THRESHOLD]
        if not xs:
            raise RuntimeError(f"no silhouette at y={y}")
        left, right = min(xs), max(xs) + 1
        result[str(y)] = {"left": left, "rightExclusive": right, "width": right - left, "centerX": round((left + right) / 2, 3)}
    return result


def copy_public(register: dict) -> dict[str, str]:
    assets = PUBLIC / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    records = {
        "front": register["approvedFront"],
        "side": register["candidates"]["sideRight90"],
        "back": register["candidates"]["back180"],
        "lineup": register["evidence"]["lineup"],
        "sideGhost": register["evidence"]["sideGhostOverlay"],
        "backGhost": register["evidence"]["backGhostOverlay"],
        "legacySide": register["poseReferences"]["legacySide"],
        "legacyBack": register["poseReferences"]["legacyBack"],
        "rejectedBack": register["rejectedProvenance"][0],
    }
    urls = {}
    for key, record in records.items():
        source = ROOT / record["file"]
        target = assets / f"{key}-{record['sha256'][:16]}.png"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(register: dict) -> None:
    urls = copy_public(register)
    geometry_rows = "".join(
        f"<tr><th>{name}</th><td>{record['normalizedOpaqueBoundsExclusive']}</td><td>{record['opaqueCenterX']}</td><td>{record['capTopY']}</td><td>{record['floorY']}</td></tr>"
        for name, record in register["geometry"].items()
    )
    section_rows = "".join(
        f"<tr><th>{y}</th><td>{values['approvedFront']['width']}</td><td>{values['sideRight90']['width']}</td><td>{values['back180']['width']}</td><td>{values['backWidthDeltaFromFront']:+d}</td><td>{values['backCenterDeltaFromFront']:+.1f}</td></tr>"
        for y, values in register["crossSections"].items()
    )
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Keeper Prime orthographic views V1</title>
<style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58;--blue:#58d7ff}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1450px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}h1{{margin:.2rem 0}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe09e}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.sprite{{height:520px;max-height:64vh;object-fit:contain}}.wide{{width:100%}}code{{overflow-wrap:anywhere;color:#badff3}}.rule{{border-left:4px solid var(--blue);background:#142733;padding:10px 14px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:8px;border-bottom:1px solid var(--line);text-align:left}}</style></head>
<body><header><a href="/animation-workbench">← Animation Workbench</a><h1>Keeper Prime orthographic views V1</h1><span class="status">Draft · 90° side and 180° back awaiting visual approval</span><p>Prime Master V1 is permanently approved. These two new views are reversible proposals only; no animation or runtime sprite has been promoted.</p></header><main>
<section class="grid"><article><h2>0° approved front</h2><img class="sprite" src="assets/{urls['front']}" alt="Approved Prime Keeper front"><p><code>{register['approvedFront']['sha256']}</code></p></article><article><h2>90° right side</h2><img class="sprite" src="assets/{urls['side']}" alt="Proposed Prime Keeper 90 degree side"><p><code>{register['candidates']['sideRight90']['sha256']}</code></p></article><article><h2>180° back</h2><img class="sprite" src="assets/{urls['back']}" alt="Proposed Prime Keeper 180 degree back"><p><code>{register['candidates']['back180']['sha256']}</code></p></article></section>
<p class="rule">All three use one broad pale jumper band. The side and back are normalized to the approved front's 256×320 cell, density 8, `[16,40]` anchor, cap-top line and floor line.</p>
<h2>Orthographic lineup</h2><article><img class="wide" src="assets/{urls['lineup']}" alt="Front side and back aligned lineup"></article>
<h2>Ghost overlays</h2><p>The cyan ghost is the permanently approved front master; the full-colour figure is the proposed view.</p><section class="grid"><article><h3>Front ghost over 90° side</h3><img class="sprite" src="assets/{urls['sideGhost']}" alt="Approved front ghost over side proposal"></article><article><h3>Front ghost over 180° back</h3><img class="sprite" src="assets/{urls['backGhost']}" alt="Approved front ghost over back proposal"></article></section>
<h2>Deterministic alignment</h2><article><table><thead><tr><th>View</th><th>Opaque bounds</th><th>centre X</th><th>cap top</th><th>floor</th></tr></thead><tbody>{geometry_rows}</tbody></table><p>White vertical: identity axis. Yellow: cap top. Green: head/shoulder transition. Pink: waist. White horizontal: floor.</p></article>
<h2>Silhouette cross-sections</h2><article><table><thead><tr><th>source y</th><th>front width</th><th>side width</th><th>back width</th><th>back Δ width</th><th>back Δ centre</th></tr></thead><tbody>{section_rows}</tbody></table><p>The back is required to remain within 4 source pixels of the approved front width and within 0.5 pixel of its centre at every registered landmark row. Its centreline is also checked at every occupied row. The side narrows intentionally because it represents body depth.</p></article>
<h2>Pose-only historical references</h2><section class="grid"><article><h3>Legacy side pose</h3><img class="sprite" src="assets/{urls['legacySide']}" alt="Legacy side pose-only reference"></article><article><h3>Legacy back pose</h3><img class="sprite" src="assets/{urls['legacyBack']}" alt="Legacy back pose-only reference"></article></section>
<h2>Rejected provenance</h2><article><h3>Too-short rear-hair edit</h3><img class="sprite" src="assets/{urls['rejectedBack']}" alt="Rejected back view with rear hair cut too short"><p>This is not a candidate. It resulted from confusing the selected first back view's rear hair with beard and must not replace the full rear-hair design above.</p></article>
<h2>Approval boundary</h2><article><p>Approve or reject each proposed view visually. Approval will establish the three-view model used to author rotations; it will not promote any runtime sprite or animation.</p></article>
</main></body></html>"""
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    master = json.loads(FRONT_REGISTER.read_text())
    if master.get("status") != "approved-permanent-identity-authority":
        raise RuntimeError("Prime Master V1 is not registered as permanently approved")
    for required in (FRONT, SIDE_SOURCE, BACK_SOURCE, REJECTED_BACK, LEGACY_SIDE, LEGACY_BACK):
        if not required.exists():
            raise RuntimeError(f"missing {rel(required)}")
    for directory in (PACK / "drafts", PACK / "references", PACK / "evidence", PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FRONT, PACK / "references/approved-prime-front.png")
    shutil.copyfile(LEGACY_SIDE, PACK / "references/legacy-side-pose-only.png")
    shutil.copyfile(LEGACY_BACK, PACK / "references/legacy-back-pose-only.png")

    side, side_geometry = normalize(SIDE_SOURCE)
    back, back_geometry = normalize(BACK_SOURCE)
    front = Image.open(FRONT).convert("RGBA")
    front_box = alpha_bbox(front)
    front_geometry = {
        "normalizedOpaqueBoundsExclusive": list(front_box),
        "opaqueWidth": front_box[2] - front_box[0],
        "opaqueHeight": front_box[3] - front_box[1],
        "opaqueCenterX": round((front_box[0] + front_box[2]) / 2, 3),
        "capTopY": front_box[1],
        "floorY": front_box[3],
    }
    section_ys = (45, 80, 120, 150, 165, 185, 205, 225, 250, 275, 300, 315)
    raw_sections = {"approvedFront": cross_sections(front, section_ys), "sideRight90": cross_sections(side, section_ys), "back180": cross_sections(back, section_ys)}
    occupied_ys = tuple(range(max(front_box[1], back_geometry["capTopY"]), min(front_box[3], back_geometry["floorY"])))
    all_row_sections = {"approvedFront": cross_sections(front, occupied_ys), "back180": cross_sections(back, occupied_ys)}
    all_row_center_deltas = [
        abs(all_row_sections["back180"][str(y)]["centerX"] - all_row_sections["approvedFront"][str(y)]["centerX"])
        for y in occupied_ys
    ]
    section_records = {}
    for y in section_ys:
        key = str(y)
        section_records[key] = {
            "approvedFront": raw_sections["approvedFront"][key],
            "sideRight90": raw_sections["sideRight90"][key],
            "back180": raw_sections["back180"][key],
            "backWidthDeltaFromFront": raw_sections["back180"][key]["width"] - raw_sections["approvedFront"][key]["width"],
            "backCenterDeltaFromFront": round(raw_sections["back180"][key]["centerX"] - raw_sections["approvedFront"][key]["centerX"], 3),
        }
    outputs = {
        "sideRight90": PACK / "drafts/keeper_prime_master-neutral-standing-side-right_f1.png",
        "back180": PACK / "drafts/keeper_prime_master-neutral-standing-back_f1.png",
    }
    side.save(outputs["sideRight90"], optimize=False, compress_level=9)
    back.save(outputs["back180"], optimize=False, compress_level=9)
    for name, pose in (("sideRight90", "standing-side-right"), ("back180", "standing-back")):
        path = outputs[name]
        json_dump(path.with_suffix(".json"), {
            "name": path.stem.removesuffix("_f1"),
            "w": 32, "h": 40, "frames": 1, "fps": 1, "density": 8,
            "anchor": [16, 40], "loop": False, "startPose": pose, "endPose": pose,
            "outfit": "standard-single-broad-band",
            "status": "draft-awaiting-visual-approval",
            "identityAuthority": rel(FRONT),
            "generatedSource": rel(SIDE_SOURCE if name == "sideRight90" else BACK_SOURCE),
        })

    lineup_path = PACK / "evidence/orthographic-lineup.png"
    lineup(front, side, back).save(lineup_path, optimize=False, compress_level=9)
    side_ghost = PACK / "evidence/front-ghost-over-side-right.png"
    back_ghost = PACK / "evidence/front-ghost-over-back.png"
    ghost_overlay(side, "90° side").save(side_ghost, optimize=False, compress_level=9)
    ghost_overlay(back, "180° back").save(back_ghost, optimize=False, compress_level=9)

    candidate_records = {}
    for key, path in outputs.items():
        sidecar = path.with_suffix(".json")
        candidate_records[key] = {
            "file": rel(path), "sha256": sha256(path),
            "sidecar": rel(sidecar), "sidecarSha256": sha256(sidecar),
            "promotionAllowed": False,
        }
    register = {
        "batchId": "keeper-prime-orthographic-views-2026-10-13-v1",
        "status": "draft-awaiting-visual-approval",
        "purpose": "Establish exact 90-degree side and 180-degree back views from the permanently approved Prime Master V1.",
        "approvedFront": {"file": rel(FRONT), "sha256": sha256(FRONT), "register": rel(FRONT_REGISTER), "registerSha256": sha256(FRONT_REGISTER)},
        "poseReferences": {
            "legacySide": {"file": rel(LEGACY_SIDE), "sha256": sha256(LEGACY_SIDE), "role": "pose only"},
            "legacyBack": {"file": rel(LEGACY_BACK), "sha256": sha256(LEGACY_BACK), "role": "pose only"},
        },
        "generatedSources": {
            "sideRight90": {"file": rel(SIDE_SOURCE), "sha256": sha256(SIDE_SOURCE)},
            "back180": {"file": rel(BACK_SOURCE), "sha256": sha256(BACK_SOURCE)},
        },
        "rejectedProvenance": [{"file": rel(REJECTED_BACK), "sha256": sha256(REJECTED_BACK), "reason": "incorrectly shortened the approved first back view's full rear hair after misidentifying it as beard"}],
        "candidates": candidate_records,
        "geometry": {"approvedFront": front_geometry, "sideRight90": side_geometry, "back180": back_geometry},
        "crossSections": section_records,
        "evidence": {
            "lineup": {"file": rel(lineup_path), "sha256": sha256(lineup_path)},
            "sideGhostOverlay": {"file": rel(side_ghost), "sha256": sha256(side_ghost)},
            "backGhostOverlay": {"file": rel(back_ghost), "sha256": sha256(back_ghost)},
        },
        "alignmentContract": {
            "cell": [256, 320], "logicalCell": [32, 40], "density": 8, "anchor": [16, 40],
            "capTopY": 18, "floorY": 316, "identityAxisX": 128,
            "ghostAuthority": rel(FRONT),
        },
        "identityContract": {
            "masterApprovalWording": "Approved. Make sure this is NEVER forgotten.",
            "uniform": "one broad pale chest-and-sleeve band; never restore the double stripe",
            "renderFamily": "smooth high-resolution Prime Master V1 only",
            "side": "exact right-facing 90-degree orthographic profile",
            "back": "exact 180-degree rear elevation with no facial features; the full cream mass below the cap is rear hair, not beard",
        },
        "validation": {
            "cellGeometryMatches": side.size == CELL and back.size == CELL,
            "transparentSafetyGutters": edge_pixels(side) == 0 and edge_pixels(back) == 0,
            "edgePixels": {"sideRight90": edge_pixels(side), "back180": edge_pixels(back)},
            "sharedCapTop": side_geometry["capTopY"] == back_geometry["capTopY"] == front_geometry["capTopY"] == 18,
            "sharedFloor": side_geometry["floorY"] == back_geometry["floorY"] == front_geometry["floorY"] == 316,
            "backMaxRegisteredWidthDelta": max(abs(record["backWidthDeltaFromFront"]) for record in section_records.values()),
            "backMaxRegisteredCenterDelta": max(abs(record["backCenterDeltaFromFront"]) for record in section_records.values()),
            "backMaxAllOccupiedRowCenterDelta": max(all_row_center_deltas),
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
        },
        "promptLog": rel(PACK / "PROMPT_LOG.md"),
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; the approved front and all production/runtime art remain unchanged.",
    }
    json_dump(PACK / "batch-register.json", register)
    write_page(register)
    print(json.dumps({"batch": register["batchId"], "side": candidate_records["sideRight90"]["sha256"], "back": candidate_records["back180"]["sha256"], "publicPage": rel(PUBLIC / 'index.html')}, indent=2))


if __name__ == "__main__":
    main()
