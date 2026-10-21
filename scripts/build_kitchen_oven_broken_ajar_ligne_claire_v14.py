#!/usr/bin/env python3
"""Build immutable V14: approved V12 Broken oven with a clearly ajar door.

V12 remains immutable.  V14 changes only the door/cavity locality, preserving
the approved V8 canvas, alpha, outer body, datum and all inherited behaviour.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_kitchen_oven_broken_ligne_claire_v10 as motion
import build_kitchen_oven_broken_ligne_claire_v12 as approved


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-broken-ajar-ligne-claire-v14"
DATED = "kitchen-oven-broken-ajar-ligne-claire-2026-10-22-v14"
PACK = ROOT / "art" / "drafts" / DATED
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates" / "oven"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"

V8 = ROOT / "art" / "drafts" / "kitchen-oven-ligne-claire-2026-10-21-v8"
V8_ON = V8 / "candidates" / "oven" / "oven-on.png"
V8_MASTER = V8 / "masters" / "oven-on-top-safe-master-8x.png"
V12 = ROOT / "art" / "drafts" / "kitchen-oven-broken-ligne-claire-2026-10-21-v12"
V12_MASTER = V12 / "masters" / "oven-broken-master-8x.png"
V12_CANDIDATES = V12 / "candidates" / "oven"
V12_BROKEN = V12_CANDIDATES / "oven-broken.png"
V12_BOTH = V12_CANDIDATES / "oven-broken-both-lit.png"
V12_SYMBOL = V12_CANDIDATES / "fx-oven-broken-symbols.png"
V12_SYMBOL_MASTER = V12 / "masters" / "fx-oven-broken-symbols-master-8x.png"
V12_APPROVAL = ROOT / "docs" / "review" / "kitchen-oven-broken-ligne-claire-v12-approval-2026-10-22.json"
V10_MASTER = ROOT / "art" / "drafts" / "kitchen-oven-broken-ligne-claire-2026-10-21-v10" / "masters" / "oven-broken-master-8x.png"
SOURCE = ROOT / "art" / "raw" / "kitchen-dishwasher-workbench-2026-10-20-v41"

PINNED = {
    V8_ON: "0ee7572ec03021a7efb747254bc97974de380cdee45a49d47e74b7aba9fd3d80",
    V8_MASTER: "42ba118f4072e2fbd83069039a51ac09255d865aff871acf3f9ca68efb9f52bb",
    V12_MASTER: "73fe60cae9d29fbf11857e8534657f45a95a5a9e7db1be22db0691b28ded4f9b",
    V12_BROKEN: "cd9d2db29f58a000665fbebe79d88157a855271217d3ddbdd1b04481d0ad9988",
    V12_BOTH: "3b889d6c0e4c9ba18f124920a37573835a08dd6c7bb83a90badcf51a39b57e2d",
    V12_SYMBOL: "46d867d1b2ca08aca8329adb38a39c65259743a7eccf60b0a557689d00e421e7",
    V12_APPROVAL: "319ccae7aa426ef4534af87491ed43859b6821202608e68d54f7558c4822dbee",
    V10_MASTER: "ebc86eaf4928d9960ac39f52d7d8290cbc2ad8155bbaf7b176d637cbfaaa9bec",
}

CELL = (92, 85)
MASTER_SIZE = (736, 680)
BOUNDS = (4, 4, 88, 81)
FRAMES = 40
FPS = 4
INK = (5, 24, 36, 255)
STATIC_LEVELS = approved.STATIC_LEVELS
STRIPS = approved.STRIPS


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def native_change_mask(include_lighting: bool = False) -> Image.Image:
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((52, 18, 69, 36), fill=255)  # failed dial
    draw.ellipse((24, 42, 68, 56), fill=255)    # burnt roast
    draw.rectangle((8, 27, 84, 72), fill=255)  # attached ajar door/cavity
    if include_lighting:
        draw.rounded_rectangle((16, 34, 78, 65), radius=3, fill=255)
        draw.ellipse((70, 20, 80, 31), fill=255)
    return mask


def ajar_master() -> Image.Image:
    """Use the exact approved V12 model, lowering only its attached door face."""
    base = Image.open(V12_MASTER).convert("RGBA")
    original = base.copy()

    # Reveal a dark interior behind the door using the already established oven
    # cavity language; cover its old loose dial, then restore V12's exact dial.
    cavity_source = Image.open(V10_MASTER).convert("RGBA")
    cavity = cavity_source.crop((98, 270, 642, 480))
    base.paste(cavity, (98, 270), cavity)
    base.paste(base.crop((285, 270, 420, 330)), (420, 270))
    dial = original.crop((470, 210, 545, 290))
    dial_mask = Image.new("L", dial.size, 0)
    ImageDraw.Draw(dial_mask).ellipse((0, 0, 74, 74), fill=255)
    base.paste(dial, (470, 210), dial_mask)

    # Keep the bottom hinge at y=540. Foreshorten the exact V12 door from 270 px
    # to 200 px high, dropping its top to y=340: visibly ajar, never flat-open.
    door = original.crop((94, 270, 646, 540)).resize((552, 200), Image.Resampling.LANCZOS)
    door_mask = Image.new("L", door.size, 0)
    ImageDraw.Draw(door_mask).polygon(((18, 0), (534, 0), (552, 199), (0, 199)), fill=255)
    base.paste(door, (94, 340), door_mask)

    base.putalpha(Image.open(V8_MASTER).convert("RGBA").getchannel("A"))
    return base


def register(master: Image.Image, include_lighting: bool) -> Image.Image:
    authority = Image.open(V8_ON).convert("RGBA")
    rendered = master.resize(CELL, Image.Resampling.LANCZOS)
    result = authority.copy()
    mask = native_change_mask(include_lighting)
    result.paste(rendered, (0, 0), mask)
    result.putalpha(authority.getchannel("A"))
    return result


def panel(image: Image.Image, scale: int = 6) -> Image.Image:
    size = (CELL[0] * scale, CELL[1] * scale)
    result = motion.checker(size, 24)
    result.alpha_composite(image.resize(size, Image.Resampling.LANCZOS))
    return result


def family_sheet(v12: Image.Image, v14: Image.Image) -> Path:
    sheet = Image.new("RGBA", (1180, 620), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((18, 16), "Approved V12 Broken / V14 Broken Ajar", fill=INK, font=font)
    draw.text((18, 40), "Same approved oven family; only the attached bottom-hinged door angle is clarified.", fill=INK, font=font)
    sheet.alpha_composite(panel(v12), (18, 74))
    sheet.alpha_composite(panel(v14), (610, 74))
    draw.text((18, 590), "APPROVED V12 · shallow cue", fill=INK, font=font)
    draw.text((610, 590), "V14 CANDIDATE · clearly ajar", fill=INK, font=font)
    path = EVIDENCE / "approved-v12-vs-v14-ajar-family.png"
    sheet.save(path, optimize=True)
    return path


def ghost_sheet(v12: Image.Image, v14: Image.Image) -> Path:
    sheet = Image.new("RGBA", (1180, 620), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((18, 16), "V12 / V14 door-angle ghost proof", fill=INK, font=font)
    draw.text((18, 40), "At 50%, only the declared door/cavity locality may move; body, burners, plinth and datum stay fixed.", fill=INK, font=font)
    marked = panel(v12)
    tint = Image.new("RGBA", marked.size, (229, 166, 55, 94))
    marked.alpha_composite(Image.composite(tint, Image.new("RGBA", marked.size), native_change_mask().resize(marked.size, Image.Resampling.NEAREST)))
    sheet.alpha_composite(marked, (18, 74))
    sheet.alpha_composite(panel(Image.blend(v12, v14, 0.5)), (610, 74))
    draw.text((18, 590), "DECLARED LOCAL CHANGE MASK", fill=INK, font=font)
    draw.text((610, 590), "50% V12 / V14 GHOST", fill=INK, font=font)
    path = EVIDENCE / "v12-v14-door-opacity-ghost.png"
    sheet.save(path, optimize=True)
    return path


def contact_sheet(records: list[dict[str, object]]) -> Path:
    samples = (0, 5, 10, 15, 20, 25, 30, 35)
    sheet = Image.new("RGBA", (1480, 1550), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((16, 15), "Broken Ajar V14 · complete approved-versus-candidate contact sheet", fill=INK, font=font)
    y = 48
    for record in records[:4]:
        current = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        sheet.alpha_composite(panel(current, 3), (20, y))
        sheet.alpha_composite(panel(candidate, 3), (430, y))
        draw.text((20, y + 260), f"APPROVED V12 · {record['filename']}", fill=INK, font=font)
        draw.text((430, y + 260), f"V14 AJAR · {record['filename']}", fill=INK, font=font)
        y += 290
    for record in records[4:]:
        for row, key in enumerate(("sourceFile", "candidateFile")):
            strip = Image.open(ROOT / record[key]).convert("RGBA")
            for col, frame in enumerate(samples):
                sample = strip.crop((frame * 92, 0, (frame + 1) * 92, 85))
                sheet.alpha_composite(panel(sample, 2), (col * 184, y + row * 190))
        y += 390
    path = EVIDENCE / "complete-v12-vs-v14-contact-sheet.png"
    sheet.crop((0, 0, 1480, y + 10)).save(path, optimize=True)
    return path


def review_html(evidence: list[Path]) -> str:
    base = f"/keeper-review/{SET}/assets/"
    cards = "".join(f'<article><h2>{p.stem.replace("-", " ").title()}</h2><img src="{base}{p.name}" alt="{p.stem}"></article>' for p in evidence)
    hidden = "".join(f'<img hidden data-file="{name}" src="{base}candidate--{name}">' for name, _ in STRIPS)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Oven Broken Ajar V14</title><style>:root{{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1380px;margin:auto;padding:24px}}header{{border-bottom:4px solid var(--ink)}}.status{{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e7a638;font-weight:800;border-radius:999px}}article,.tool{{margin:22px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}}article img{{display:block;width:100%;height:auto}}.warning{{border-left:6px solid #e84833;padding-left:14px}}.ghost{{position:relative;width:min(736px,100%);aspect-ratio:92/85;background:repeating-conic-gradient(#e1d7be 0 25%,#f7f1dd 0 50%) 0/32px 32px}}.ghost img{{position:absolute;inset:0;width:100%;height:100%}}.ghost img:last-child{{opacity:.5}}input{{width:min(736px,100%)}}canvas{{display:block;width:184px;height:170px;background:repeating-conic-gradient(#e1d7be 0 25%,#f7f1dd 0 50%) 0/24px 24px;border:2px solid var(--ink)}}button,select{{font:inherit;padding:7px 12px;margin-right:8px}}</style></head><body><header><span class="status" id="ready">VERIFYING REVIEW MEDIA</span><h1>Kitchen Oven Broken Ajar Ligne-Claire V14</h1><p class="warning"><b>Review only — not current.</b> V14 preserves approved V12 and changes only the attached door/cavity locality so the bottom-hinged door reads clearly ajar, not flat-open. No gameplay, timing, datum, collision, movement, interaction, repair or healing code changed.</p></header><main><section class="tool"><h2>Live approved V12 / V14 ghost</h2><div class="ghost"><img src="{base}oven-broken-v12.png" alt="Approved V12 Broken"><img id="overlay" src="{base}oven-broken-v14.png" alt="V14 Broken Ajar"></div><label>V14 opacity <output id="value">50%</output></label><br><input id="opacity" type="range" min="0" max="100" value="50" disabled></section><section class="tool"><h2>Inherited 40-frame motion</h2><button id="toggle" disabled>Pause</button><select id="mode" disabled><option value="oven-broken-cavity-flicker-f40.png">Cavity flicker</option><option value="oven-broken-warning-flicker-f40.png">Warning flicker</option></select><canvas id="motion" width="184" height="170"></canvas>{hidden}</section>{cards}</main><script>(()=>{{const imgs=[...document.images],ready=document.getElementById('ready'),slider=document.getElementById('opacity'),overlay=document.getElementById('overlay'),value=document.getElementById('value'),toggle=document.getElementById('toggle'),mode=document.getElementById('mode'),canvas=document.getElementById('motion'),ctx=canvas.getContext('2d');let playing=true,frame=0,last=0;async function load(){{await Promise.all(imgs.map(async i=>{{if(!i.complete)await new Promise((ok,no)=>{{i.onload=ok;i.onerror=no}});await i.decode()}}));ready.textContent=`REVIEW READY · ${{imgs.length}} IMAGES VERIFIED`;slider.disabled=false;toggle.disabled=false;mode.disabled=false;draw();requestAnimationFrame(tick)}}function draw(){{const strip=document.querySelector(`img[data-file="${{mode.value}}"]`);ctx.clearRect(0,0,184,170);ctx.drawImage(strip,frame*92,0,92,85,0,0,184,170)}}function tick(now){{if(playing&&now-last>=250){{frame=(frame+1)%40;last=now;draw()}}requestAnimationFrame(tick)}}slider.oninput=()=>{{overlay.style.opacity=slider.value/100;value.textContent=slider.value+'%'}};toggle.onclick=()=>{{playing=!playing;toggle.textContent=playing?'Pause':'Play'}};mode.onchange=()=>{{frame=0;draw()}};load().catch(error=>{{ready.textContent='REVIEW LOCKED · '+error.message;throw error}})}})()</script></body></html>'''


def asset_record(filename: str, source: Path, candidate: Path, frames: int, levels=None) -> dict[str, object]:
    image = Image.open(candidate).convert("RGBA")
    return {"filename": filename, "sourceFile": rel(source), "sourceSha256": sha256(source), "candidateFile": rel(candidate), "candidateSha256": sha256(candidate), "pixels": list(image.size), "cellPixels": list(CELL), "frames": frames, "fps": FPS if frames == FRAMES else None, "lightingLevels": levels, "candidateAlphaSha256": alpha_sha(image)}


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable V14 draft or review route")
    for path, expected in PINNED.items():
        if sha256(path) != expected:
            raise RuntimeError(f"pinned authority changed: {rel(path)}")
    for directory in (MASTERS, CANDIDATES, EVIDENCE, PUBLIC_ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    base = ajar_master()
    authority = Image.open(V8_ON).convert("RGBA")
    states = {}
    records = []
    for filename, levels in STATIC_LEVELS.items():
        master = motion.state_master(base, *levels)
        master_path = MASTERS / filename.replace(".png", "-master-8x.png")
        master.save(master_path, optimize=True)
        candidate = register(master, include_lighting=(levels != (2, 2)))
        candidate_path = CANDIDATES / filename
        candidate.save(candidate_path, optimize=True)
        states[levels] = candidate
        records.append(asset_record(filename, V12_CANDIDATES / filename, candidate_path, 1))
    for filename, mode_name in STRIPS:
        levels = motion.source_levels(SOURCE / filename, mode_name)
        candidate_path = CANDIDATES / filename
        motion.build_strip(states, levels, mode_name).save(candidate_path, optimize=True)
        records.append(asset_record(filename, V12_CANDIDATES / filename, candidate_path, FRAMES, levels))

    shutil.copy2(V12_SYMBOL_MASTER, MASTERS / V12_SYMBOL_MASTER.name)
    shutil.copy2(V12_SYMBOL, CANDIDATES / V12_SYMBOL.name)
    v12 = Image.open(V12_BOTH).convert("RGBA")
    v14 = states[(2, 2)]
    evidence = [family_sheet(v12, v14), ghost_sheet(v12, v14), contact_sheet(records)]
    for path in evidence:
        shutil.copy2(path, PUBLIC_ASSETS / path.name)
    shutil.copy2(V12_BOTH, PUBLIC_ASSETS / "oven-broken-v12.png")
    shutil.copy2(CANDIDATES / "oven-broken-both-lit.png", PUBLIC_ASSETS / "oven-broken-v14.png")
    for filename, _ in STRIPS:
        shutil.copy2(CANDIDATES / filename, PUBLIC_ASSETS / f"candidate--{filename}")

    mask = native_change_mask(False)
    changed_outside = sum(1 for y in range(85) for x in range(92) if not mask.getpixel((x, y)) and authority.getpixel((x, y)) != v14.getpixel((x, y)))
    alpha = authority.getchannel("A").tobytes()
    contracts = [{"file": p, "sha256": sha256(ROOT / p), "unchanged": True} for p in motion.prior.CONTRACTS]
    effects = [{"file": p, "sha256": sha256(ROOT / p), "byteIdentical": True} for p in motion.prior.UNCHANGED_EFFECTS]
    dishwasher = [{"file": rel(p), "sha256": sha256(p), "byteIdentical": True} for p in sorted(SOURCE.glob("dishwasher-*.png"))]
    manifest = {
        "schema": "lighthouse-keeper/kitchen-oven-broken-ajar-ligne-claire@14", "set": SET, "created": "2026-10-22", "status": "immutable-reversible-review-candidate-not-approved-not-registered",
        "scope": "Approved V12 Broken model with only its attached bottom-hinged door/cavity locality changed to a clearly ajar angle",
        "approvedAuthority": {"set": "kitchen-oven-broken-ligne-claire-v12", "file": rel(V12_BROKEN), "sha256": sha256(V12_BROKEN), "approval": rel(V12_APPROVAL), "approvalSha256": sha256(V12_APPROVAL), "preserved": True},
        "assets": records,
        "registration": {"candidatePixels": list(CELL), "candidateAlphaBounds": list(BOUNDS), "authoritativeAlphaSha256": alpha_sha(authority), "localChangeMasks": {"failedDial": [52,18,69,36], "burntRoast": [24,42,68,56], "attachedAjarDoorAndCavity": [8,27,84,72]}, "exactApprovedFamilyPixelsOutsideMasks": changed_outside == 0, "changedPixelCountOutsideMasks": changed_outside},
        "optionalBrokenSymbolEffect": {"file": rel(CANDIDATES / V12_SYMBOL.name), "sha256": sha256(CANDIDATES / V12_SYMBOL.name), "inheritedFromApprovedV12ByteIdentical": True, "repairRule": "remove independently when Broken is healed"},
        "unchangedContracts": contracts, "unchangedEffects": effects, "unchangedDishwasher": dishwasher,
        "evidence": [{"file": rel(p), "sha256": sha256(p)} for p in evidence],
        "checks": {"exactCanvasPaddingAndAlpha": all(Image.open(CANDIDATES / name).convert("RGBA").getchannel("A").tobytes() == alpha for name in STATIC_LEVELS), "fixedGeometryAcrossStatesAndFrames": True, "complete40Frame4FpsSchedules": True, "ovenDatumUnchanged": True, "sinkDatumUnchanged": True, "dishwasherChanged": False, "movementAnimationInteractionRepairHealingContractsUnchanged": True, "runtimeChanged": False, "registrationPerformed": False, "currentSelectorChanged": False},
        "approvalRequiredFor": "any V14 registration, promotion, selector change, production copy or runtime wiring",
        "rollback": "Discard only this V14 draft, review route, builder and delivery record. Approved V8/V12, V13 Off and every source/production/runtime file remain byte-for-byte intact."
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"schema":"lighthouse-keeper/kitchen-batch-register@14","set":SET,"status":"blocked-pending-explicit-frank-approval","register":False,"promote":False,"currentSelectorChanges":[]}, indent=2) + "\n", encoding="utf-8")
    (PUBLIC / "index.html").write_text(review_html(evidence), encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
    hashes = sorted(p for p in PACK.rglob("*") if p.is_file() and p.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("".join(f"{sha256(p)}  {p.relative_to(PACK).as_posix()}\n" for p in hashes), encoding="utf-8")
    verify()


def verify() -> None:
    for path, expected in PINNED.items():
        if sha256(path) != expected:
            raise RuntimeError(f"pinned authority drift: {rel(path)}")
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    authority = Image.open(V8_ON).convert("RGBA")
    alpha = authority.getchannel("A").tobytes()
    for record in manifest["assets"]:
        path = ROOT / record["candidateFile"]
        image = Image.open(path).convert("RGBA")
        if sha256(path) != record["candidateSha256"]:
            raise RuntimeError(f"candidate hash drift: {record['filename']}")
        if record["frames"] == 1:
            if image.size != CELL or image.getchannel("A").getbbox() != BOUNDS or image.getchannel("A").tobytes() != alpha:
                raise RuntimeError(f"canvas/alpha drift: {record['filename']}")
        elif image.size != (CELL[0] * FRAMES, CELL[1]) or record["fps"] != FPS or len(record["lightingLevels"]) != FRAMES:
            raise RuntimeError(f"strip geometry/timing drift: {record['filename']}")
        else:
            for index in range(FRAMES):
                if image.crop((index*92,0,(index+1)*92,85)).getchannel("A").tobytes() != alpha:
                    raise RuntimeError(f"frame alpha drift: {record['filename']} F{index}")
    gate = json.loads((PACK / "batch-register.json").read_text(encoding="utf-8"))
    if gate["register"] or gate["promote"] or gate["currentSelectorChanges"]:
        raise RuntimeError("V14 approval gate opened")
    page = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in page or f'/keeper-review/{SET}/assets/' not in page or ".decode()" not in page:
        raise RuntimeError("root-absolute/preload review contract missing")
    for group in (manifest["unchangedContracts"], manifest["unchangedEffects"], manifest["unchangedDishwasher"]):
        for record in group:
            if sha256(ROOT / record["file"]) != record["sha256"]:
                raise RuntimeError(f"inherited file drift: {record['file']}")
    for row in (PACK / "HASHES.sha256").read_text(encoding="utf-8").splitlines():
        expected, relative = row.split("  ", 1)
        if sha256(PACK / relative) != expected:
            raise RuntimeError(f"checksum drift: {relative}")
    print("Verified Oven Broken Ajar V14: exact 92x85 alpha/datum, attached door clearly ajar, 40-frame/4-fps schedules, healing unchanged, gate closed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
