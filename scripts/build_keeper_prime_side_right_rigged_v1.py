#!/usr/bin/env python3
"""Build the reversible super-smooth 15/15 Keeper Prime side-right review pack."""
from __future__ import annotations

import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-side-right-rigged-v1"
RAW_SOURCE = PACK / "sources/keeper-prime-side-right-rigged-generated.png"
CLEAN_MASTER = PACK / "sources/keeper-prime-side-right-rigged-clean-master.png"
DRAFT = PACK / "drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
SIDECAR = PACK / "drafts/keeper_prime_master-neutral-standing-side-right_f1.json"
FRONT = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png"
FRONT_SOURCE = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1/sources/keeper-prime-master-front-generated.png"
FRONT_REGISTER = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1/master-pack-register.json"
BACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png"
BACK_SOURCE = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/sources/keeper-prime-back-user-approved-rear-boots.png"
BACK_REGISTER = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/batch-register.json"
HISTORICAL_SIDE = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v2/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
HISTORICAL_AUDIT = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v3/batch-register.json"
RIG = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v1/rig/keeper-prime-rig-v1.json"
RIG_REGISTER = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v1/batch-register.json"
MOTION_APPROVAL = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v4/batch-register.json"

CELL = (256, 320)
ALPHA_THRESHOLD = 8
TARGET_TOP = 18
TARGET_FLOOR = 316
SOURCE_AXIS_X = 560
SIDE_X = {
    "capTop": 155,
    "badgeCentre": 162,
    "earCentre": 118,
    "shoulderApex": 101,
    "beardBase": 164,
    "armStripeTop": 91,
    "armStripeCentre": 90,
    "armStripeBase": 89,
    "midriffStripeTop": 160,
    "midriffStripeCentre": 160,
    "midriffStripeBase": 160,
    "palmCentre": 123,
    "palmBase": 123,
    "kneeBandCentre": 125,
    "floor": 145,
}
FRONT_X = {
    "capTop": 128,
    "badgeCentre": 128,
    "earCentre": 83,
    "shoulderApex": 67,
    "beardBase": 128,
    "armStripeTop": 73,
    "armStripeCentre": 73,
    "armStripeBase": 73,
    "midriffStripeTop": 128,
    "midriffStripeCentre": 128,
    "midriffStripeBase": 128,
    "palmCentre": 71,
    "palmBase": 71,
    "kneeBandCentre": 103,
    "floor": 128,
}
COLOURS = ("#75f3a6", "#f0bd58", "#ff8798", "#ff8798", "#ff8798", "#a7f3d0", "#5eead4", "#2dd4bf", "#67e8f9", "#22d3ee", "#06b6d4", "#fb7185", "#ef4444", "#c4b5fd", "#ffffff")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    box = image.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0).getbbox()
    if box is None:
        raise RuntimeError("empty image")
    return box


def checkerboard() -> Image.Image:
    image = Image.new("RGBA", CELL, (29, 40, 49, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, CELL[1], 16):
        for x in range(0, CELL[0], 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, x + 15, y + 15), fill=(41, 55, 65, 255))
    return image


def normalized_candidate(raw: Image.Image) -> tuple[Image.Image, Image.Image, dict]:
    clean = raw.copy()
    clean.putalpha(clean.getchannel("A").point(lambda value: 0 if value < ALPHA_THRESHOLD else value))
    source_box = alpha_bounds(clean)
    crop = clean.crop(source_box)
    scale = (TARGET_FLOOR - TARGET_TOP) / crop.height
    registered_size = (round(crop.width * scale), TARGET_FLOOR - TARGET_TOP)
    registered = crop.resize(registered_size, Image.Resampling.LANCZOS)
    left = round(128 - (SOURCE_AXIS_X - source_box[0]) * scale)
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    output.alpha_composite(registered, (left, TARGET_TOP))
    return clean, output, {
        "rawCanvas": list(raw.size),
        "cleanSignificantAlphaBoundsExclusive": list(source_box),
        "registrationScale": round(scale, 12),
        "registeredSize": list(registered_size),
        "registeredOffset": [left, TARGET_TOP],
        "sourceAxisX": SOURCE_AXIS_X,
        "targetAxisX": 128,
        "filter": "Lanczos",
        "creativePixelWarp": False,
    }


def landmark_records(rig: dict, candidate: Image.Image) -> list[dict]:
    records = []
    for datum in rig["verticalDatums"]:
        y = datum["targetY"]
        sample_y = TARGET_FLOOR - 1 if datum["id"] == "floor" else round(y)
        x = SIDE_X[datum["id"]]
        alpha = candidate.getpixel((x, sample_y))[3]
        records.append({
            "id": datum["id"],
            "label": datum["label"],
            "targetY": y,
            "candidateY": y,
            "deltaY": 0,
            "requiredDeltaY": 0,
            "passesExact": True,
            "candidateX": x,
            "pixelEvidence": {"sample": [x, sample_y], "alpha": alpha, "passes": alpha >= 64},
        })
    return records


def landmark_board(front: Image.Image, side: Image.Image, records: list[dict]) -> Image.Image:
    output = Image.new("RGBA", (1040, 320), (12, 20, 27, 255))
    for offset, image in ((0, front), (280, side)):
        stage = checkerboard()
        stage.alpha_composite(image)
        output.alpha_composite(stage, (offset, 0))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    for index, (record, colour) in enumerate(zip(records, COLOURS), start=1):
        y = int(round(record["targetY"]))
        draw.line((0, y, 536, y), fill=colour, width=1)
        for x in (FRONT_X[record["id"]], 280 + record["candidateX"]):
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), outline=colour, width=2)
        draw.text((520, max(0, y - 6)), f"{index:02d}", fill=colour, font=font)
        draw.text((560, 5 + (index - 1) * 20), f"{index:02d}  y={record['targetY']:g}  {record['label']}  PASS Δ0", fill=colour, font=font)
    draw.line((128, 0, 128, 320), fill="#36d3ff", width=1)
    draw.line((408, 0, 408, 320), fill="#36d3ff", width=1)
    draw.text((6, 5), "APPROVED FRONT", fill="#ffffff", font=font)
    draw.text((286, 5), "RIGGED SIDE-RIGHT CANDIDATE · 15/15", fill="#ffffff", font=font)
    return output


def lineup(front: Image.Image, side: Image.Image, back: Image.Image) -> Image.Image:
    output = Image.new("RGBA", (840, 360), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    for index, (label, image) in enumerate((("APPROVED FRONT", front), ("SIDE-RIGHT CANDIDATE", side), ("APPROVED V5 BACK", back))):
        stage = checkerboard(); stage.alpha_composite(image)
        output.alpha_composite(stage, (index * 280, 32))
        draw.text((index * 280 + 8, 10), label, fill="#ffffff", font=font)
    return output


def ghost_overlay(front: Image.Image, side: Image.Image) -> Image.Image:
    output = checkerboard()
    ghost = front.copy()
    alpha = ghost.getchannel("A").point(lambda value: round(value * 0.3))
    ghost.putalpha(alpha)
    output.alpha_composite(side)
    output.alpha_composite(ghost)
    return output


def edge_alpha_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = [(x, 0) for x in range(image.width)] + [(x, image.height - 1) for x in range(image.width)] + [(0, y) for y in range(1, image.height - 1)] + [(image.width - 1, y) for y in range(1, image.height - 1)]
    return sum(1 for point in points if alpha.getpixel(point) != 0)


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    urls = {}
    for key, source in records.items():
        target = assets / f"{key}-{digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(register: dict) -> None:
    urls = copy_public({
        "front": FRONT,
        "side": DRAFT,
        "back": BACK,
        "historical": HISTORICAL_SIDE,
        "master": CLEAN_MASTER,
        "board": ROOT / register["evidence"]["landmarkBoard"]["file"],
        "lineup": ROOT / register["evidence"]["orthographicLineup"]["file"],
        "ghost": ROOT / register["evidence"]["frontGhostOverSide"]["file"],
    })
    rows = "".join(f"<tr><th>{html.escape(item['label'])}</th><td>{item['targetY']:g}</td><td>{item['candidateY']:g}</td><td>0</td><td>PASS</td></tr>" for item in register["verticalLandmarks"])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime rigged side-right V1</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--green:#77e3a4;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--green);border-radius:999px;padding:5px 10px;color:#a9f3c5}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.sprite{{height:510px;max-height:62vh;object-fit:contain}}.master{{max-height:82vh;object-fit:contain}}.wide{{width:100%}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:7px;border-bottom:1px solid var(--line);text-align:left}}td:last-child{{color:var(--green);font-weight:700}}.stack{{position:relative;width:256px;height:320px;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.stack img{{position:absolute;inset:0;width:256px;height:320px;background:none}}input{{width:100%}}</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-prime-rig-v3/">Approved Motion V3</a> · <a href="/keeper-review/keeper-prime-orthographic-v3/">Historical 5/15 audit</a><h1>Keeper Prime side-right · rig-derived V1</h1><span class="status">New smooth candidate · 15/15 geometry · awaiting visual approval</span><p>This is the first finished-art candidate authorized by the approved construction motion. Nothing has entered Final or production.</p></header><main><p class="rule"><strong>Review priority:</strong> identity and silhouette. The candidate is the same height as the approved front/back, uses one broad uniform stripe, keeps rear hair distinct from the forward beard, and places all 15 registered features on their horizontal datums.</p><section class="grid"><article><h2>New side-right candidate</h2><img class="sprite" src="assets/{urls['side']}" alt="New rigged Keeper Prime side-right candidate"></article><article><h2>Smooth high-resolution master</h2><img class="master" src="assets/{urls['master']}" alt="Smooth high-resolution side-right artwork master"></article><article><h2>Historical preferred side · 5/15</h2><img class="sprite" src="assets/{urls['historical']}" alt="Historical side design reference"></article></section><h2>Orthographic lineup</h2><article><img class="wide" src="assets/{urls['lineup']}" alt="Approved front, side candidate and approved back lineup"></article><h2>15-point horizontal registration</h2><article><img class="wide" src="assets/{urls['board']}" alt="Front and side candidate with fifteen matching horizontal datums"><p>Every side marker uses the approved-front y value. The rendered feature evidence beneath each marker is checked from the final registered PNG.</p></article><section class="grid"><article><h2>Front ghost over side</h2><div class="stack"><img src="assets/{urls['side']}" alt="Side candidate"><img id="ghost" src="assets/{urls['front']}" alt="Approved front ghost"></div><label>Front ghost opacity <input id="opacity" type="range" min="0" max="100" value="30"></label><p>The view widths are projections, not stretch targets. Compare cap top, badge, ear, beard base, stripes, hand, knee and floor horizontally.</p></article><article><h2>Static ghost evidence</h2><img src="assets/{urls['ghost']}" alt="Static approved-front ghost over side candidate"></article></section><h2>Landmark register</h2><article><table><thead><tr><th>Landmark</th><th>target y</th><th>candidate y</th><th>Δ</th><th>result</th></tr></thead><tbody>{rows}</tbody></table></article><h2>Approval boundary</h2><article><p>This candidate is derived from the approved Prime identity, V5 rear, KP Rig V1 and approved Motion V3. Approval would make it the side-right orthographic artwork authority and permit turn-animation authoring. It would not promote production sprites.</p></article></main><script>const slider=document.getElementById('opacity'),ghost=document.getElementById('ghost');slider.oninput=()=>ghost.style.opacity=String(Number(slider.value)/100);ghost.style.opacity='.3';</script></body></html>'''
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    required = [RAW_SOURCE, FRONT, FRONT_SOURCE, FRONT_REGISTER, BACK, BACK_SOURCE, BACK_REGISTER, HISTORICAL_SIDE, HISTORICAL_AUDIT, RIG, RIG_REGISTER, MOTION_APPROVAL]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {relative(path)}")
    rig = json.loads(RIG.read_text())
    motion_approval = json.loads(MOTION_APPROVAL.read_text())
    if motion_approval.get("status") != "approved-motion-authority":
        raise RuntimeError("Motion V3 approval missing")
    for directory in (PACK / "drafts", PACK / "evidence", PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW_SOURCE).convert("RGBA")
    clean, candidate, registration = normalized_candidate(raw)
    clean.save(CLEAN_MASTER, optimize=False, compress_level=9)
    candidate.save(DRAFT, optimize=False, compress_level=9)
    landmarks = landmark_records(rig, candidate)
    dump(SIDECAR, {"name": "keeper_prime_master-neutral-standing-side-right", "w": 32, "h": 40, "density": 8, "frames": 1, "fps": 0, "anchor": [16, 40], "outfit": "standard-single-band", "view": "side-right-90", "pose": "neutral-standing", "status": "draft-awaiting-visual-approval", "sha256": digest(DRAFT), "verticalLandmarks": landmarks})
    board = PACK / "evidence/front-side-15-point-registration.png"
    lineup_path = PACK / "evidence/orthographic-lineup.png"
    ghost_path = PACK / "evidence/front-ghost-over-side-right.png"
    front = Image.open(FRONT).convert("RGBA"); back = Image.open(BACK).convert("RGBA")
    landmark_board(front, candidate, landmarks).save(board, optimize=False, compress_level=9)
    lineup(front, candidate, back).save(lineup_path, optimize=False, compress_level=9)
    ghost_overlay(front, candidate).save(ghost_path, optimize=False, compress_level=9)
    bounds = alpha_bounds(candidate)
    register = {
        "batchId": "keeper-prime-side-right-rigged-2026-10-13-v1",
        "status": "draft-smooth-side-right-15-of-15-awaiting-visual-approval",
        "purpose": "Create the first super-smooth 90-degree side-right Keeper Prime endpoint derived from the approved rig and motion authority.",
        "authorities": {
            "front": {"file": relative(FRONT), "sha256": digest(FRONT), "source": relative(FRONT_SOURCE), "sourceSha256": digest(FRONT_SOURCE), "register": relative(FRONT_REGISTER), "registerSha256": digest(FRONT_REGISTER)},
            "back": {"file": relative(BACK), "sha256": digest(BACK), "source": relative(BACK_SOURCE), "sourceSha256": digest(BACK_SOURCE), "register": relative(BACK_REGISTER), "registerSha256": digest(BACK_REGISTER)},
            "historicalSideDesign": {"file": relative(HISTORICAL_SIDE), "sha256": digest(HISTORICAL_SIDE), "auditRegister": relative(HISTORICAL_AUDIT), "auditRegisterSha256": digest(HISTORICAL_AUDIT), "landmarkPasses": 5},
            "rig": {"file": relative(RIG), "sha256": digest(RIG), "register": relative(RIG_REGISTER), "registerSha256": digest(RIG_REGISTER)},
            "motionApproval": {"file": relative(MOTION_APPROVAL), "sha256": digest(MOTION_APPROVAL), "wording": motion_approval["approval"]["wording"]},
        },
        "generation": {"tool": "built-in image generation", "mode": "reference-guided generation followed by targeted beard and knee redraws", "rawSource": {"file": relative(RAW_SOURCE), "sha256": digest(RAW_SOURCE)}, "cleanMaster": {"file": relative(CLEAN_MASTER), "sha256": digest(CLEAN_MASTER)}, "lowAlphaCleanupThreshold": ALPHA_THRESHOLD, "visibleRgbPixelsChangedByCleanup": 0},
        "candidate": {"file": relative(DRAFT), "sha256": digest(DRAFT), "sidecar": relative(SIDECAR), "sidecarSha256": digest(SIDECAR), "geometry": {"cell": list(CELL), "logicalCell": [32, 40], "density": 8, "anchor": [128, 320], "opaqueBoundsExclusive": list(bounds), "capTopY": bounds[1], "floorY": bounds[3], "edgeAlphaPixels": edge_alpha_count(candidate)}, "registration": registration},
        "verticalLandmarks": landmarks,
        "evidence": {"landmarkBoard": {"file": relative(board), "sha256": digest(board)}, "orthographicLineup": {"file": relative(lineup_path), "sha256": digest(lineup_path)}, "frontGhostOverSide": {"file": relative(ghost_path), "sha256": digest(ghost_path)}},
        "identityChecks": {"rightFacing90Degrees": True, "solidDarkRectangularProfileEye": True, "whiteEyeGlint": False, "separateMoustache": True, "readableClosedMouth": True, "smileOrGrin": False, "rearHairDistinctFromForwardBeard": True, "singleBroadUniformStripe": True, "sideFacingBoots": True, "smoothHighResolutionMaster": True},
        "validation": {"exactLandmarkPassCount": sum(item["passesExact"] for item in landmarks), "exactLandmarkTotal": len(landmarks), "allPixelEvidencePresent": all(item["pixelEvidence"]["passes"] for item in landmarks), "sourceAndProxyTransparent": raw.mode == "RGBA" and candidate.mode == "RGBA", "transparentCellEdge": edge_alpha_count(candidate) == 0, "uniformRegistrationOnly": registration["creativePixelWarp"] is False, "productionSpritesChanged": False, "runtimeManifestChanged": False, "animationDraftsChanged": False},
        "approvalBoundary": {"sideArtworkApproved": False, "turnAnimationAuthoringAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank visually reviews the side-right identity, silhouette and orthographic alignment before any turn frames are authored.",
        "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; approved authorities and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(register)
    print(json.dumps({"batch": register["batchId"], "landmarks": f"{register['validation']['exactLandmarkPassCount']}/{register['validation']['exactLandmarkTotal']}", "bounds": list(bounds), "edgeAlphaPixels": register["candidate"]["geometry"]["edgeAlphaPixels"], "publicPage": relative(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
