#!/usr/bin/env python3
"""Build the immutable V13 Off oven from the approved V8 On authority.

This is a deterministic lighting-state edit, not a redraw.  The approved V8
On pixels are retained everywhere except the oven cavity and warning-lamp
masks.  Canvas, alpha, transparent padding and registration remain exact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

import build_kitchen_oven_broken_ligne_claire_v10 as state_tools


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-off-ligne-claire-v13"
DATED = "kitchen-oven-off-ligne-claire-2026-10-22-v13"
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
V12_BROKEN = V12 / "candidates" / "oven" / "oven-broken.png"
V12_APPROVAL = ROOT / "docs" / "review" / "kitchen-oven-broken-ligne-claire-v12-approval-2026-10-22.json"
SOURCE_OFF = ROOT / "art" / "raw" / "kitchen-dishwasher-workbench-2026-10-20-v41" / "oven-off.png"

PINNED = {
    V8_ON: "0ee7572ec03021a7efb747254bc97974de380cdee45a49d47e74b7aba9fd3d80",
    V8_MASTER: "42ba118f4072e2fbd83069039a51ac09255d865aff871acf3f9ca68efb9f52bb",
    V12_BROKEN: "cd9d2db29f58a000665fbebe79d88157a855271217d3ddbdd1b04481d0ad9988",
    V12_APPROVAL: "319ccae7aa426ef4534af87491ed43859b6821202608e68d54f7558c4822dbee",
    SOURCE_OFF: "c2f5687b598b42f15b42a2323e2d441d1b0b892ea2f75cbea590f4190e6c0b8e",
}
CELL = (92, 85)
MASTER_SIZE = (736, 680)
BOUNDS = (4, 4, 88, 81)
INK = (5, 24, 36, 255)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def lighting_mask() -> Image.Image:
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((16, 34, 78, 65), radius=3, fill=255)
    draw.ellipse((70, 20, 80, 31), fill=255)
    return mask


def checker(size: tuple[int, int], step: int = 24) -> Image.Image:
    image = Image.new("RGBA", size, (247, 241, 221, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill=(225, 215, 190, 255))
    return image


def panel(image: Image.Image, scale: int = 7) -> Image.Image:
    size = (CELL[0] * scale, CELL[1] * scale)
    result = checker(size)
    result.alpha_composite(image.resize(size, Image.Resampling.LANCZOS))
    return result


def build_off() -> tuple[Image.Image, Image.Image]:
    authority = Image.open(V8_ON).convert("RGBA")
    on_master = Image.open(V8_MASTER).convert("RGBA")
    off_master = state_tools.state_master(on_master, 0, 0)
    rendered = off_master.resize(CELL, Image.Resampling.LANCZOS)
    candidate = authority.copy()
    candidate.paste(rendered, (0, 0), lighting_mask())
    candidate.putalpha(authority.getchannel("A"))
    return off_master, candidate


def current_candidate_sheet(current: Image.Image, candidate: Image.Image) -> Path:
    sheet = Image.new("RGBA", (1360, 735), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((20, 18), "OFF oven · complete current-versus-candidate contact sheet", fill=INK, font=font)
    draw.text((20, 42), "V13 changes drawing language while preserving the exact 92 x 85 canvas and datum.", fill=INK, font=font)
    sheet.alpha_composite(panel(current), (20, 78))
    sheet.alpha_composite(panel(candidate), (696, 78))
    draw.text((20, 690), "CURRENT V41 OFF · preserved", fill=INK, font=font)
    draw.text((696, 690), "V13 OFF · review candidate", fill=INK, font=font)
    path = EVIDENCE / "complete-current-vs-candidate-off-v13.png"
    sheet.save(path, optimize=True)
    return path


def family_sheet(on: Image.Image, off: Image.Image, broken: Image.Image) -> Path:
    scale = 5
    width = 3 * CELL[0] * scale + 80
    sheet = Image.new("RGBA", (width, 535), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((18, 16), "One approved oven family · V8 On / V13 Off / V12 Broken", fill=INK, font=font)
    draw.text((18, 39), "Off is the exact intact V8 oven with only cavity and warning illumination removed.", fill=INK, font=font)
    for index, (label, image) in enumerate((("APPROVED V8 ON", on), ("V13 OFF CANDIDATE", off), ("APPROVED V12 BROKEN OFF", broken))):
        x = 20 + index * (CELL[0] * scale + 20)
        sheet.alpha_composite(panel(image, scale), (x, 70))
        draw.text((x, 505), label, fill=INK, font=font)
    path = EVIDENCE / "approved-family-on-off-broken-v13.png"
    sheet.save(path, optimize=True)
    return path


def ghost_sheet(on: Image.Image, off: Image.Image) -> Path:
    scale = 7
    sheet = Image.new("RGBA", (1360, 735), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((20, 18), "V8 On / V13 Off exact ghost proof", fill=INK, font=font)
    draw.text((20, 42), "Only the pale cavity and warning-lamp mask may change; all other native pixels are byte-identical.", fill=INK, font=font)
    mask = lighting_mask().resize((CELL[0] * scale, CELL[1] * scale), Image.Resampling.NEAREST)
    marked = panel(on, scale)
    tint = Image.new("RGBA", marked.size, (229, 166, 55, 98))
    marked.alpha_composite(Image.composite(tint, Image.new("RGBA", marked.size), mask))
    ghost = panel(Image.blend(on, off, 0.5), scale)
    sheet.alpha_composite(marked, (20, 78))
    sheet.alpha_composite(ghost, (696, 78))
    draw.text((20, 690), "DECLARED LIGHTING MASK", fill=INK, font=font)
    draw.text((696, 690), "50% ON / OFF GHOST", fill=INK, font=font)
    path = EVIDENCE / "on-off-ghost-v13.png"
    sheet.save(path, optimize=True)
    return path


def review_html(evidence: list[Path]) -> str:
    base = f"/keeper-review/{SET}/assets/"
    cards = "".join(
        f'<article><h2>{path.stem.replace("-", " ").title()}</h2><img src="{base}{path.name}" alt="{path.stem}"></article>'
        for path in evidence
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Oven Off V13</title><style>:root{{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1380px;margin:auto;padding:24px}}header{{border-bottom:4px solid var(--ink)}}.status{{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e7a638;font-weight:800;border-radius:999px}}article,.tool{{margin:22px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}}article img{{display:block;width:100%;height:auto}}.warning{{border-left:6px solid #e84833;padding-left:14px}}.ghost{{position:relative;width:min(736px,100%);aspect-ratio:92/85;background:repeating-conic-gradient(#e1d7be 0 25%,#f7f1dd 0 50%) 0/32px 32px}}.ghost img{{position:absolute;inset:0;width:100%;height:100%;image-rendering:auto}}.ghost img:last-child{{opacity:.5}}input{{width:min(736px,100%)}}</style></head><body><header><span class="status" id="ready">VERIFYING REVIEW MEDIA</span><h1>Kitchen Oven Off Ligne-Claire V13</h1><p class="warning"><b>Review only — not current.</b> V13 is the approved intact V8 oven with only its cavity and warning illumination removed. V8 On and V12 Broken remain immutable. No gameplay, movement, timing, collision, anchor, pivot, interaction, repair or healing code has changed.</p></header><main><section class="tool"><h2>Live V8 On / V13 Off ghost</h2><p>Move the slider. Only the cavity and warning lamp should change; the oven body must not swim.</p><div class="ghost"><img src="{base}oven-on.png" alt="Approved V8 On"><img id="overlay" src="{base}oven-off.png" alt="V13 Off"></div><label>Off overlay opacity <output id="value">50%</output></label><br><input id="opacity" type="range" min="0" max="100" value="50" disabled></section>{cards}</main><script>(()=>{{const imgs=[...document.images],ready=document.getElementById('ready'),slider=document.getElementById('opacity'),overlay=document.getElementById('overlay'),value=document.getElementById('value');async function load(){{await Promise.all(imgs.map(async i=>{{if(!i.complete)await new Promise((ok,no)=>{{i.onload=ok;i.onerror=no}});await i.decode()}}));ready.textContent=`REVIEW READY · ${{imgs.length}} IMAGES VERIFIED`;slider.disabled=false}}slider.oninput=()=>{{overlay.style.opacity=slider.value/100;value.textContent=slider.value+'%'}};load().catch(error=>{{ready.textContent='REVIEW LOCKED · '+error.message;throw error}})}})()</script></body></html>'''


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable V13 draft or review route")
    for path, expected in PINNED.items():
        if sha256(path) != expected:
            raise RuntimeError(f"pinned authority changed: {rel(path)}")
    for directory in (MASTERS, CANDIDATES, EVIDENCE, PUBLIC_ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    off_master, off = build_off()
    master_path = MASTERS / "oven-off-master-8x.png"
    candidate_path = CANDIDATES / "oven-off.png"
    off_master.save(master_path, optimize=True)
    off.save(candidate_path, optimize=True)
    shutil.copy2(V8_ON, CANDIDATES / "oven-on.png")
    shutil.copy2(V12_BROKEN, CANDIDATES / "oven-broken.png")

    on = Image.open(V8_ON).convert("RGBA")
    broken = Image.open(V12_BROKEN).convert("RGBA")
    current = Image.open(SOURCE_OFF).convert("RGBA")
    evidence = [
        family_sheet(on, off, broken),
        ghost_sheet(on, off),
        current_candidate_sheet(current, off),
    ]
    for path in evidence:
        shutil.copy2(path, PUBLIC_ASSETS / path.name)
    for path in (CANDIDATES / "oven-on.png", candidate_path, CANDIDATES / "oven-broken.png"):
        shutil.copy2(path, PUBLIC_ASSETS / path.name)

    mask = lighting_mask()
    changed_outside = sum(
        1 for y in range(CELL[1]) for x in range(CELL[0])
        if not mask.getpixel((x, y)) and on.getpixel((x, y)) != off.getpixel((x, y))
    )
    changed_inside = sum(
        1 for y in range(CELL[1]) for x in range(CELL[0])
        if mask.getpixel((x, y)) and on.getpixel((x, y)) != off.getpixel((x, y))
    )
    manifest = {
        "schema": "lighthouse-keeper/kitchen-oven-off-ligne-claire@13",
        "set": SET,
        "created": "2026-10-22",
        "status": "immutable-reversible-review-candidate-not-approved-not-registered",
        "scope": "Intact Off oven derived from approved V8 On; remove cavity and warning illumination only",
        "approvedAuthorities": {
            "on": {"set": "kitchen-oven-ligne-claire-v8", "file": rel(V8_ON), "sha256": sha256(V8_ON)},
            "broken": {"set": "kitchen-oven-broken-ligne-claire-v12", "file": rel(V12_BROKEN), "sha256": sha256(V12_BROKEN), "approval": rel(V12_APPROVAL), "approvalSha256": sha256(V12_APPROVAL)},
        },
        "source": {"file": rel(SOURCE_OFF), "sha256": sha256(SOURCE_OFF), "preserved": True},
        "candidate": {"file": rel(candidate_path), "sha256": sha256(candidate_path), "master": rel(master_path), "masterSha256": sha256(master_path), "pixels": list(CELL), "alphaBounds": list(BOUNDS), "alphaSha256": alpha_sha(off)},
        "registration": {"lightingMasks": {"cavity": [16, 34, 78, 65], "warningLamp": [70, 20, 80, 31]}, "changedPixelsOutsideMasks": changed_outside, "changedPixelsInsideMasks": changed_inside, "exactV8PixelsOutsideMasks": changed_outside == 0},
        "evidence": [{"file": rel(path), "sha256": sha256(path)} for path in evidence],
        "checks": {"exactCanvasPaddingAndAlpha": off.size == CELL and off.getchannel("A").getbbox() == BOUNDS and off.getchannel("A").tobytes() == on.getchannel("A").tobytes(), "exactV8PixelsOutsideLightingMasks": changed_outside == 0, "intactGeometry": True, "ovenDatumUnchanged": True, "movementAnimationInteractionRepairHealingContractsUnchanged": True, "runtimeChanged": False, "registrationPerformed": False, "currentSelectorChanged": False},
        "approvalRequiredFor": "any V13 registration, promotion, selector change, production copy or runtime wiring",
        "rollback": "Discard only this V13 draft, review route, builder and delivery record. Approved V8 On, approved V12 Broken and every source/production/runtime asset remain byte-for-byte intact.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"schema": "lighthouse-keeper/kitchen-batch-register@13", "set": SET, "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n", encoding="utf-8")
    (PUBLIC / "index.html").write_text(review_html(evidence), encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
    hashes = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}\n" for path in hashes), encoding="utf-8")
    verify()


def verify() -> None:
    for path, expected in PINNED.items():
        if sha256(path) != expected:
            raise RuntimeError(f"pinned authority drift: {rel(path)}")
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    on = Image.open(V8_ON).convert("RGBA")
    off_path = ROOT / manifest["candidate"]["file"]
    off = Image.open(off_path).convert("RGBA")
    if sha256(off_path) != manifest["candidate"]["sha256"]:
        raise RuntimeError("V13 Off candidate hash drift")
    if off.size != CELL or off.getchannel("A").getbbox() != BOUNDS or off.getchannel("A").tobytes() != on.getchannel("A").tobytes():
        raise RuntimeError("V13 canvas, transparent padding or alpha drift")
    mask = lighting_mask()
    if any(on.getpixel((x, y)) != off.getpixel((x, y)) for y in range(CELL[1]) for x in range(CELL[0]) if not mask.getpixel((x, y))):
        raise RuntimeError("V13 drift outside the declared lighting masks")
    if ImageChops.difference(on.convert("RGB"), off.convert("RGB")).getbbox() is None:
        raise RuntimeError("V13 Off is unexpectedly identical to On")
    gate = json.loads((PACK / "batch-register.json").read_text(encoding="utf-8"))
    if gate["register"] or gate["promote"] or gate["currentSelectorChanges"]:
        raise RuntimeError("V13 approval gate opened")
    page = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in page or f'/keeper-review/{SET}/assets/' not in page or ".decode()" not in page:
        raise RuntimeError("root-absolute/preload review contract missing")
    for record in manifest["evidence"]:
        if sha256(ROOT / record["file"]) != record["sha256"]:
            raise RuntimeError(f"evidence drift: {record['file']}")
    for row in (PACK / "HASHES.sha256").read_text(encoding="utf-8").splitlines():
        expected, relative = row.split("  ", 1)
        if sha256(PACK / relative) != expected:
            raise RuntimeError(f"checksum drift: {relative}")
    print("Verified Oven Off V13: exact approved V8 geometry and alpha, lighting-only change, V12 Broken preserved, gate closed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
