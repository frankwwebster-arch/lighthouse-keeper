#!/usr/bin/env python3
"""Publish the Prime orthographic vertical-landmark registration audit (V3)."""
from __future__ import annotations

import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v3"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-orthographic-v3"
V2_PACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v2"
MASTER_PACK = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1"
FRONT = MASTER_PACK / "drafts/keeper_prime_master-neutral-front_f1.png"
FRONT_REGISTER = MASTER_PACK / "master-pack-register.json"
SIDE = V2_PACK / "drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
BACK = V2_PACK / "drafts/keeper_prime_master-neutral-standing-back_f1.png"
V2_REGISTER = V2_PACK / "batch-register.json"
ATTEMPT_1 = PACK / "rejected-sources/side-landmark-edit-attempt-1.png"
ATTEMPT_2 = PACK / "rejected-sources/side-landmark-edit-attempt-2.png"

CELL = (256, 320)
ALPHA_THRESHOLD = 8


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


def geometry(image: Image.Image) -> dict:
    box = alpha_bounds(image)
    return {
        "opaqueBoundsExclusive": list(box),
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


def landmark_records() -> list[dict]:
    # Coordinates are semantic bounds/centres measured at the registered density-8
    # source scale. Half-pixel centres are retained rather than rounded away.
    rows = [
        ("capTop", "cap top", 18, 18, "outer silhouette"),
        ("badgeCentre", "golden badge centre", 48.5, 46.0, "gold component centre"),
        ("earCentre", "visible ear centre", 88.5, 89.5, "skin component centre"),
        ("shoulderApex", "shoulder apex", 121, 108, "upper blue body envelope"),
        ("beardBase", "beard base", 149, 142, "cream beard envelope, exclusive base"),
        ("armStripeTop", "arm stripe top", 150, 150, "near sleeve cream envelope"),
        ("armStripeCentre", "arm stripe centre", 159, 159, "near sleeve cream centre"),
        ("armStripeBase", "arm stripe base", 168, 168, "near sleeve cream envelope"),
        ("midriffStripeTop", "midriff stripe top", 157, 155, "torso cream envelope"),
        ("midriffStripeCentre", "midriff stripe centre", 165.5, 162.5, "torso cream centre"),
        ("midriffStripeBase", "midriff stripe base", 174, 170, "torso cream envelope"),
        ("palmCentre", "resting palm centre", 215, 218, "skin component centre"),
        ("palmBase", "resting palm base", 227, 231, "skin component, exclusive base"),
        ("kneeBandCentre", "knee band centre", 266.5, 264.5, "blue knee-band centre"),
        ("floor", "floor bound", 316, 316, "opaque bound, exclusive floor"),
    ]
    return [
        {
            "id": key,
            "label": label,
            "frontY": front_y,
            "sideY": side_y,
            "deltaY": side_y - front_y,
            "requiredDeltaY": 0,
            "passesExact": side_y == front_y,
            "measurement": measurement,
        }
        for key, label, front_y, side_y, measurement in rows
    ]


def landmark_board(front: Image.Image, side: Image.Image, records: list[dict]) -> Image.Image:
    output = Image.new("RGBA", (1040, 320), (12, 20, 27, 255))
    for offset, image in ((0, front), (280, side)):
        stage = checkerboard()
        stage.alpha_composite(image)
        output.alpha_composite(stage, (offset, 0))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    colours = ("#f7d35c", "#ff9b54", "#d7a2ff", "#6ee7b7", "#fff1c2", "#a7f3d0", "#5eead4", "#2dd4bf", "#67e8f9", "#22d3ee", "#06b6d4", "#fb7185", "#ef4444", "#c4b5fd", "#ffffff")
    front_x = {"capTop": 128, "badgeCentre": 128, "earCentre": 83, "shoulderApex": 67, "beardBase": 128, "armStripeTop": 73, "armStripeCentre": 73, "armStripeBase": 73, "midriffStripeTop": 128, "midriffStripeCentre": 128, "midriffStripeBase": 128, "palmCentre": 71, "palmBase": 71, "kneeBandCentre": 103, "floor": 128}
    side_x = {"capTop": 159, "badgeCentre": 164, "earCentre": 117, "shoulderApex": 126, "beardBase": 151, "armStripeTop": 112, "armStripeCentre": 112, "armStripeBase": 112, "midriffStripeTop": 152, "midriffStripeCentre": 152, "midriffStripeBase": 152, "palmCentre": 120, "palmBase": 120, "kneeBandCentre": 120, "floor": 128}
    for index, (record, colour) in enumerate(zip(records, colours), start=1):
        front_y = int(round(record["frontY"]))
        side_y = int(round(record["sideY"]))
        draw.line((0, front_y, 536, front_y), fill=colour, width=1)
        draw.ellipse((front_x[record["id"]] - 3, front_y - 3, front_x[record["id"]] + 3, front_y + 3), outline=colour, width=2)
        sx = 280 + side_x[record["id"]]
        draw.ellipse((sx - 3, side_y - 3, sx + 3, side_y + 3), outline=colour, width=2)
        if side_y != front_y:
            draw.line((sx + 6, front_y, sx + 6, side_y), fill="#ff5d73", width=2)
        draw.text((520, max(0, front_y - 6)), f"{index:02d}", fill=colour, font=font)
        status = "PASS" if record["passesExact"] else f"FAIL {record['deltaY']:+g}px"
        legend_y = 5 + (index - 1) * 20
        draw.text((560, legend_y), f"{index:02d}  y={record['frontY']:g}  {record['label']}  {status}", fill=colour if record["passesExact"] else "#ff8798", font=font)
    draw.text((6, 5), "APPROVED FRONT", fill="#ffffff", font=font)
    draw.text((286, 5), "SELECTED V2 SIDE", fill="#ffffff", font=font)
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
    sources = {
        "front": FRONT,
        "side": SIDE,
        "back": BACK,
        "board": ROOT / register["evidence"]["landmarkBoard"]["file"],
        "attempt1": ATTEMPT_1,
        "attempt2": ATTEMPT_2,
    }
    urls = copy_public(sources)
    rows = "".join(
        f"<tr class=\"{'pass' if item['passesExact'] else 'fail'}\"><th>{html.escape(item['label'])}</th><td>{item['frontY']:g}</td><td>{item['sideY']:g}</td><td>{item['deltaY']:+g}</td><td>{'PASS' if item['passesExact'] else 'REDRAFT'}</td></tr>"
        for item in register["verticalLandmarks"]
    )
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime orthographic registration V3</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58;--red:#ff8798;--green:#77e3a4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}h1{{margin:.2rem 0}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--red);border-radius:999px;padding:5px 10px;color:#ffbdc7}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.sprite{{height:510px;max-height:62vh;object-fit:contain}}.wide{{width:100%}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:7px;border-bottom:1px solid var(--line);text-align:left}}tr.fail td:last-child{{color:var(--red);font-weight:700}}tr.pass td:last-child{{color:var(--green);font-weight:700}}code{{overflow-wrap:anywhere;color:#badff3}}</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-prime-orthographic-v2/">V2 exact front/back overlay</a><h1>Keeper Prime orthographic registration V3</h1><span class="status">Draft audit · selected side requires landmark redraft</span><p>V2 is immutable. V3 adds the exact vertical skeleton requested for turn authoring; no production or animation art has changed.</p></header><main>
<p class="rule"><strong>What passes:</strong> front, selected side and back are each exactly 298 source pixels high from cap top y=18 to floor y=316. <strong>What does not:</strong> equal total height alone is insufficient. Badge, ear, shoulder, beard base, midriff stripe, palm and knee datums expose internal vertical drift in the selected side.</p>
<section class="grid"><article><h2>Approved front</h2><img class="sprite" src="assets/{urls['front']}" alt="Approved Prime front"></article><article><h2>Selected V2 side · audit source</h2><img class="sprite" src="assets/{urls['side']}" alt="Selected side under landmark audit"></article><article><h2>Exact-silhouette V2 back</h2><img class="sprite" src="assets/{urls['back']}" alt="V2 back"></article></section>
<h2>Front ↔ side vertical skeleton</h2><article><img class="wide" src="assets/{urls['board']}" alt="Front and side with horizontal landmark datums"><p>A horizontal line is drawn from each approved-front datum. The circle marks the side feature's measured position; red vertical ticks show the miss. Zero means exact.</p></article>
<h2>Measured landmark register</h2><article><table><thead><tr><th>Landmark</th><th>front y</th><th>side y</th><th>side Δ</th><th>result</th></tr></thead><tbody>{rows}</tbody></table><p>The beard base, shoulders, arm stripe and midriff stripe are separately registered; matching one cannot conceal drift in another.</p></article>
<h2>Rejected generated correction attempts</h2><p>Both attempts retained the selected design reasonably well but still missed multiple hard datums. They are evidence only and are not candidates.</p><section class="grid"><article><h3>Attempt 1</h3><img class="sprite" src="assets/{urls['attempt1']}" alt="Rejected side correction attempt 1"></article><article><h3>Attempt 2</h3><img class="sprite" src="assets/{urls['attempt2']}" alt="Rejected side correction attempt 2"></article></section>
<h2>Decision</h2><article><p>The selected side remains the preferred visual design, but it is not transition-ready. The next side draft must preserve that design while bringing every hard vertical datum to delta 0 before any turn frames are authored.</p></article>
</main></body></html>"""
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    master = json.loads(FRONT_REGISTER.read_text())
    v2 = json.loads(V2_REGISTER.read_text())
    if master.get("status") != "approved-permanent-identity-authority":
        raise RuntimeError("Prime Master approval missing")
    for required in (FRONT, SIDE, BACK, V2_REGISTER, ATTEMPT_1, ATTEMPT_2):
        if not required.exists():
            raise RuntimeError(f"missing {relative(required)}")
    for directory in (PACK / "references", PACK / "evidence", PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    front = Image.open(FRONT).convert("RGBA")
    side = Image.open(SIDE).convert("RGBA")
    back = Image.open(BACK).convert("RGBA")
    landmarks = landmark_records()
    board = PACK / "evidence/front-side-vertical-landmark-register.png"
    landmark_board(front, side, landmarks).save(board, optimize=False, compress_level=9)
    geometries = {"approvedFront": geometry(front), "selectedSideRight90": geometry(side), "v2Back180": geometry(back)}
    register = {
        "batchId": "keeper-prime-orthographic-views-2026-10-13-v3",
        "status": "draft-landmark-redraft-required",
        "purpose": "Register a hard front-to-side vertical skeleton before authoring any turn frames.",
        "approvedFront": {"file": relative(FRONT), "sha256": digest(FRONT), "register": relative(FRONT_REGISTER), "registerSha256": digest(FRONT_REGISTER)},
        "immutableV2": {"register": relative(V2_REGISTER), "registerSha256": digest(V2_REGISTER), "side": {"file": relative(SIDE), "sha256": digest(SIDE)}, "back": {"file": relative(BACK), "sha256": digest(BACK)}},
        "geometry": geometries,
        "verticalLandmarks": landmarks,
        "evidence": {"landmarkBoard": {"file": relative(board), "sha256": digest(board)}},
        "rejectedGeneratedAttempts": [
            {"file": relative(ATTEMPT_1), "sha256": digest(ATTEMPT_1), "reason": "missed hard internal datums after normalization"},
            {"file": relative(ATTEMPT_2), "sha256": digest(ATTEMPT_2), "reason": "improved guidance still missed beard, shoulder, stripe and hand datums"},
        ],
        "alignmentContract": {"cell": [256, 320], "logicalCell": [32, 40], "density": 8, "anchor": [16, 40], "capTopY": 18, "floorY": 316, "opaqueHeight": 298, "requiredLandmarkDeltaY": 0},
        "validation": {
            "allViewsSameHeight": all(item["opaqueHeight"] == 298 for item in geometries.values()),
            "allViewsShareCapTop": all(item["capTopY"] == 18 for item in geometries.values()),
            "allViewsShareFloor": all(item["floorY"] == 316 for item in geometries.values()),
            "exactLandmarkPassCount": sum(item["passesExact"] for item in landmarks),
            "exactLandmarkTotal": len(landmarks),
            "sideLandmarkRegistrationReady": all(item["passesExact"] for item in landmarks),
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
            "animationDraftsChanged": False,
        },
        "previousV2Validation": v2["validation"],
        "promptLog": relative(PACK / "PROMPT_LOG.md"),
        "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; V2, Prime Master and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(register)
    print(json.dumps({"batch": register["batchId"], "height": 298, "landmarkPasses": f"{register['validation']['exactLandmarkPassCount']}/{register['validation']['exactLandmarkTotal']}", "publicPage": relative(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
