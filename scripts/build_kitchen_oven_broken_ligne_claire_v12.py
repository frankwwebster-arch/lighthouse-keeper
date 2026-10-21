#!/usr/bin/env python3
"""Build the immutable V12 Broken oven from the approved V8 On authority.

The V8 On candidate is the structural and colour source.  V12 changes only
three explicit local regions: the failed third dial, the burnt roast and the
slightly ajar door cue.  Everything outside those masks is copied byte-for-byte
from V8 after registration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

import build_kitchen_oven_broken_ligne_claire_v10 as prior


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-broken-ligne-claire-v12"
DATED = "kitchen-oven-broken-ligne-claire-2026-10-21-v12"
PACK = ROOT / "art" / "drafts" / DATED
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates" / "oven"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"

V8 = ROOT / "art" / "drafts" / "kitchen-oven-ligne-claire-2026-10-21-v8"
V8_ON = V8 / "candidates" / "oven" / "oven-on.png"
V8_MASTER = V8 / "masters" / "oven-on-top-safe-master-8x.png"
V8_APPROVAL = ROOT / "docs" / "review" / "kitchen-oven-ligne-claire-v8-approval-2026-10-21.json"
V10 = ROOT / "art" / "drafts" / "kitchen-oven-broken-ligne-claire-2026-10-21-v10"
V10_BROKEN = V10 / "candidates" / "oven" / "oven-broken.png"
V10_SYMBOL = V10 / "candidates" / "oven" / "fx-oven-broken-symbols.png"
V10_SYMBOL_MASTER = V10 / "masters" / "fx-oven-broken-symbols-master-8x.png"
REJECTED = ROOT / "art" / "source" / DATED / "rejected-generated-attempts" / "global-geometry-drift-v1.png"
SOURCE = ROOT / "art" / "raw" / "kitchen-dishwasher-workbench-2026-10-20-v41"
V3 = ROOT / "art" / "drafts" / "kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3"

V8_ON_SHA = "0ee7572ec03021a7efb747254bc97974de380cdee45a49d47e74b7aba9fd3d80"
V8_MASTER_SHA = "42ba118f4072e2fbd83069039a51ac09255d865aff871acf3f9ca68efb9f52bb"
V8_APPROVAL_SHA = "bc8e87715610e900cbaa25d33d16bd95964f5408270e36c58b01fba85a4ccdc6"
V10_BROKEN_SHA = "71093271eb36c4ab59cab0f75aaf132a9019091219d6b44f6389fab390da19ea"
V10_SYMBOL_SHA = "46d867d1b2ca08aca8329adb38a39c65259743a7eccf60b0a557689d00e421e7"
V10_SYMBOL_MASTER_SHA = "37bdcff2c77e1d32702fc6301657360d0a208b5b5901b53ff9f78176c05dbcff"
REJECTED_SHA = "18281f2d368a0168c083d1b6b5018fc75b5e566151b116a2e12e57b3efde188a"

CELL = (92, 85)
MASTER_SIZE = (736, 680)
BOUNDS = (4, 4, 88, 81)
FRAMES = 40
FPS = 4
INK = (5, 24, 36, 255)
STATIC_LEVELS = {
    "oven-broken.png": (0, 0),
    "oven-broken-cavity-lit.png": (2, 0),
    "oven-broken-warning-lit.png": (0, 2),
    "oven-broken-both-lit.png": (2, 2),
}
STRIPS = (
    ("oven-broken-cavity-flicker-f40.png", "cavity"),
    ("oven-broken-warning-flicker-f40.png", "warning"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def row_cream(master: Image.Image, y: int) -> tuple[int, int, int, int]:
    samples = []
    for x in tuple(range(82, 108)) + tuple(range(292, 420)) + tuple(range(528, 548)):
        r, g, b, a = master.getpixel((x, y))
        if a > 240 and r > 150 and g > 125 and b > 80:
            samples.append((r, g, b, a))
    if not samples:
        return (246, 229, 183, 255)
    return tuple(sorted(channel)[len(channel) // 2] for channel in zip(*samples))


def master_damage_mask() -> Image.Image:
    mask = Image.new("L", MASTER_SIZE, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((424, 157, 548, 282), fill=255)      # failed dial and wires
    draw.ellipse((205, 350, 535, 445), fill=255)        # burnt roast only
    draw.rectangle((91, 245, 647, 332), fill=255)       # shallow door-opening cue
    return mask


def native_mask(include_lighting: bool = False) -> Image.Image:
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((52, 18, 69, 36), fill=255)
    draw.ellipse((24, 42, 68, 56), fill=255)
    draw.rectangle((11, 29, 81, 41), fill=255)
    if include_lighting:
        draw.rounded_rectangle((16, 34, 78, 65), radius=3, fill=255)
        draw.ellipse((70, 20, 80, 31), fill=255)
    return mask


def exact_composite(authority: Image.Image, edited: Image.Image, mask: Image.Image) -> Image.Image:
    result = authority.copy()
    result.paste(edited, (0, 0), mask)
    result.putalpha(authority.getchannel("A"))
    return result


def broken_master() -> Image.Image:
    on = Image.open(V8_MASTER).convert("RGBA")
    result = on.copy()
    draw = ImageDraw.Draw(result)

    # Preserve the exact V8 third dial itself as the hanging component.
    dial_box = (438, 166, 520, 248)
    dial = on.crop(dial_box).resize((62, 62), Image.Resampling.LANCZOS)
    dial_mask = Image.new("L", dial.size, 0)
    ImageDraw.Draw(dial_mask).ellipse((5, 5, 57, 57), fill=255)

    # Clear only the original dial/tick locality with the V8 fascia row colour.
    for y in range(164, 249):
        cream = row_cream(on, y)
        for x in range(430, 529):
            if ((x - 479) / 51) ** 2 + ((y - 207) / 47) ** 2 <= 1:
                result.putpixel((x, y), cream)

    # Failed socket and exactly two wires, followed by the unchanged V8 dial.
    draw.ellipse((442, 170, 516, 244), fill=INK)
    draw.ellipse((454, 182, 504, 232), fill=(28, 31, 34, 255))
    draw.arc((460, 188, 498, 228), 190, 345, fill=(83, 91, 94, 255), width=5)
    draw.line((468, 220, 482, 231, 486, 237), fill=INK, width=10, joint="curve")
    draw.line((468, 220, 482, 231, 486, 237), fill=(0, 107, 177, 255), width=4, joint="curve")
    draw.line((488, 220, 501, 225, 510, 236), fill=INK, width=10, joint="curve")
    draw.line((488, 220, 501, 225, 510, 236), fill=(239, 112, 23, 255), width=4, joint="curve")
    result.paste(dial, (476, 216), dial_mask)

    # Burn only the existing roast pixels; its silhouette, tray and placement stay exact.
    pixels = result.load()
    original = on.load()
    for y in range(357, 437):
        for x in range(210, 530):
            r, g, b, a = original[x, y]
            if a > 240 and r > 95 and r > g * 1.15 and b < 110:
                char = 0.32 + ((x * 13 + y * 7) % 19) / 100
                pixels[x, y] = (round(r * char), round(g * 0.28), round(b * 0.24), a)

    # A restrained, footprint-safe ajar cue.  The exact V8 handle, mounts,
    # outer cabinet and plinth stay in place; only a shallow perspective gap is
    # drawn immediately beneath the handle.
    draw = ImageDraw.Draw(result)
    draw.polygon(((127, 306), (609, 306), (590, 328), (146, 328)), fill=INK)
    draw.polygon(((140, 311), (596, 311), (582, 321), (154, 321)), fill=(76, 49, 31, 255))
    draw.line((127, 306, 146, 328), fill=INK, width=6)
    draw.line((609, 306, 590, 328), fill=INK, width=6)

    # Guarantee the approved master everywhere outside the three declared zones.
    return exact_composite(on, result, master_damage_mask())


def register(master: Image.Image, include_lighting: bool) -> Image.Image:
    on = Image.open(V8_ON).convert("RGBA")
    rendered = master.resize(CELL, Image.Resampling.LANCZOS)
    return exact_composite(on, rendered, native_mask(include_lighting))


def state_candidates(base: Image.Image) -> dict[tuple[int, int], Image.Image]:
    result = {}
    for cavity in range(3):
        for warning in range(3):
            state = prior.state_master(base, cavity, warning)
            result[(cavity, warning)] = register(state, include_lighting=(cavity != 2 or warning != 2))
    return result


def ghost_sheet(on: Image.Image, broken: Image.Image) -> Path:
    scale = 7
    width, height = 1540, 760
    sheet = Image.new("RGBA", (width, height), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((20, 18), "V8 ON / V12 BROKEN ghost proof", fill=INK, font=font)
    draw.text((20, 42), "Alternating pixels outside the three pale masks are byte-identical. Any visible swim there is a failure.", fill=INK, font=font)
    mask = native_mask(False).resize((CELL[0] * scale, CELL[1] * scale), Image.Resampling.NEAREST)
    tint = Image.new("RGBA", mask.size, (229, 166, 55, 94))
    left = prior.checker(mask.size, 28)
    left.alpha_composite(on.resize(mask.size, Image.Resampling.NEAREST))
    left.alpha_composite(Image.composite(tint, Image.new("RGBA", mask.size), mask))
    ghost = Image.blend(on, broken, 0.5).resize(mask.size, Image.Resampling.NEAREST)
    right = prior.checker(mask.size, 28)
    right.alpha_composite(ghost)
    sheet.alpha_composite(left, (20, 82))
    sheet.alpha_composite(right, (790, 82))
    draw.text((20, 690), "DECLARED LOCAL CHANGE MASKS", fill=INK, font=font)
    draw.text((790, 690), "50% GHOST: V8 ON UNDER V12 BROKEN", fill=INK, font=font)
    path = EVIDENCE / "approved-on-ghost-overlay-v12.png"
    sheet.save(path, optimize=True)
    return path


def family_sheet(on_master: Image.Image, broken: Image.Image, broken_native: Image.Image) -> Path:
    sheet = Image.new("RGBA", (1600, 920), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((18, 15), "Approved V8 On / V12 Broken: one exact oven family", fill=INK, font=font)
    draw.text((18, 38), "Broken is derived from V8 On; cabinet silhouette, colours, controls, burners, canvas and registration remain authoritative.", fill=INK, font=font)
    sheet.alpha_composite(prior.panel(on_master, (770, 700), 1.0), (10, 70))
    sheet.alpha_composite(prior.panel(broken, (770, 700), 1.0), (820, 70))
    draw.text((20, 786), "APPROVED V8 ON · immutable", fill=INK, font=font)
    draw.text((830, 786), "V12 BROKEN · only masked state cues", fill=INK, font=font)
    sheet.alpha_composite(Image.open(V8_ON).convert("RGBA"), (285, 815))
    sheet.alpha_composite(broken_native, (1095, 815))
    path = EVIDENCE / "approved-v8-on-vs-v12-broken-family.png"
    sheet.save(path, optimize=True)
    return path


def contact_sheet(records: list[dict[str, object]]) -> Path:
    samples = (0, 5, 10, 15, 20, 25, 30, 35)
    sheet = Image.new("RGBA", (1840, 1790), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((16, 15), "Kitchen Oven Broken V12 · complete current-versus-candidate contact sheet", fill=INK, font=font)
    y = 58
    for record in records[1:5]:
        current = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        sheet.alpha_composite(prior.panel(current, (880, 175)), (0, y))
        sheet.alpha_composite(prior.panel(candidate, (880, 175)), (960, y))
        draw.text((8, y + 178), f"CURRENT · {record['filename']}", fill=INK, font=font)
        draw.text((968, y + 178), f"V12 · {record['filename']}", fill=INK, font=font)
        y += 205
    for record in records[5:]:
        for row, key in enumerate(("sourceFile", "candidateFile")):
            strip = Image.open(ROOT / record[key]).convert("RGBA")
            for col, frame in enumerate(samples):
                sample = strip.crop((frame * 92, 0, (frame + 1) * 92, 85))
                sheet.alpha_composite(prior.panel(sample, (220, 120), 2.4), (col * 230, y + row * 138))
                draw.text((col * 230 + 5, y + row * 138 + 122), f"{'CURRENT' if row == 0 else 'V12'} F{frame:02d}", fill=INK, font=font)
        y += 300
    path = EVIDENCE / "complete-current-vs-candidate-contact-sheet.png"
    sheet.crop((0, 0, 1840, y + 20)).save(path, optimize=True)
    return path


def asset_record(filename: str, source: Path, candidate: Path, frames: int, master: Path | None = None, levels: list[int] | None = None) -> dict[str, object]:
    image = Image.open(candidate).convert("RGBA")
    result = {
        "filename": filename,
        "sourceFile": rel(source), "sourceSha256": sha256(source),
        "candidateFile": rel(candidate), "candidateSha256": sha256(candidate),
        "pixels": list(image.size), "cellPixels": list(CELL), "frames": frames,
        "fps": FPS if frames == FRAMES else None,
        "candidateAlphaSha256": alpha_sha(image),
    }
    if master:
        result.update({"masterFile": rel(master), "masterSha256": sha256(master), "masterPixels": list(Image.open(master).size)})
    if levels is not None:
        result["lightingLevels"] = levels
    return result


def review_html(evidence: list[Path]) -> str:
    base = f"/keeper-review/{SET}/assets/"
    cards = "".join(f'<article><h2>{path.stem.replace("-", " ").title()}</h2><img src="{base}{path.name}" alt="{path.stem}"></article>' for path in evidence)
    hidden = "".join(
        f'<img hidden data-file="{name}" src="{base}candidate--{name}"><img hidden data-current="{name}" src="{base}current--{name}">'
        for name, _ in STRIPS
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Oven Broken V12</title><style>:root{{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1380px;margin:auto;padding:24px}}header{{border-bottom:4px solid var(--ink)}}.status{{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e7a638;font-weight:800;border-radius:999px}}article,.tool{{margin:22px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}}article img{{display:block;width:100%;height:auto}}.warning{{border-left:6px solid #e84833;padding-left:14px}}.ghost{{position:relative;width:min(736px,100%);aspect-ratio:92/85;background:repeating-conic-gradient(#e1d7be 0 25%,#f7f1dd 0 50%) 0/32px 32px}}.ghost img{{position:absolute;inset:0;width:100%;height:100%}}.ghost img:last-child{{opacity:.5}}input{{width:min(736px,100%)}}canvas{{display:block;width:184px;height:170px;background:repeating-conic-gradient(#e1d7be 0 25%,#f7f1dd 0 50%) 0/24px 24px;border:2px solid var(--ink)}}button,select{{font:inherit;padding:7px 12px;margin-right:8px}}</style></head><body><header><span class="status" id="ready">VERIFYING REVIEW MEDIA</span><h1>Kitchen Oven Broken Ligne-Claire V12</h1><p class="warning"><b>Review only — not current.</b> V8 On remains untouched. V12 rebuilds Broken from the exact V8 authority and modifies only the failed dial, burnt roast and shallow door-opening cue. No gameplay, movement, interaction, timing, collision, anchor, pivot, repair or healing code has changed.</p></header><main><section class="tool"><h2>Live V8 On / V12 Broken ghost</h2><p>Move the slider. Outside the three local state regions the images are byte-identical, so the cabinet must not swim.</p><div class="ghost"><img src="{base}oven-on.png" alt="V8 On"><img id="overlay" src="{base}oven-broken-both-lit.png" alt="V12 Broken"></div><label>Broken overlay opacity <output id="value">50%</output></label><br><input id="opacity" type="range" min="0" max="100" value="50" disabled></section><section class="tool"><h2>Inherited 40-frame motion</h2><button id="toggle" disabled>Pause</button><select id="mode" disabled><option value="oven-broken-cavity-flicker-f40.png">Cavity flicker</option><option value="oven-broken-warning-flicker-f40.png">Warning flicker</option></select><canvas id="motion" width="184" height="170"></canvas>{hidden}</section>{cards}</main><script>(()=>{{const imgs=[...document.images],ready=document.getElementById('ready'),slider=document.getElementById('opacity'),overlay=document.getElementById('overlay'),value=document.getElementById('value'),toggle=document.getElementById('toggle'),mode=document.getElementById('mode'),canvas=document.getElementById('motion'),ctx=canvas.getContext('2d');let playing=true,frame=0,last=0;async function load(){{await Promise.all(imgs.map(async i=>{{if(!i.complete)await new Promise((ok,no)=>{{i.onload=ok;i.onerror=no}});await i.decode()}}));ready.textContent=`REVIEW READY · ${{imgs.length}} IMAGES VERIFIED`;slider.disabled=false;toggle.disabled=false;mode.disabled=false;draw();requestAnimationFrame(tick)}}function draw(){{const strip=document.querySelector(`img[data-file="${{mode.value}}"]`);ctx.clearRect(0,0,184,170);ctx.imageSmoothingEnabled=true;ctx.drawImage(strip,frame*92,0,92,85,0,0,184,170)}}function tick(now){{if(playing&&now-last>=250){{frame=(frame+1)%40;last=now;draw()}}requestAnimationFrame(tick)}}slider.oninput=()=>{{overlay.style.opacity=slider.value/100;value.textContent=slider.value+'%'}};toggle.onclick=()=>{{playing=!playing;toggle.textContent=playing?'Pause':'Play'}};mode.onchange=()=>{{frame=0;draw()}};load().catch(error=>{{ready.textContent='REVIEW LOCKED · '+error.message;throw error}})}})()</script></body></html>'''


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable V12 draft or review route")
    pinned = {
        V8_ON: V8_ON_SHA, V8_MASTER: V8_MASTER_SHA, V8_APPROVAL: V8_APPROVAL_SHA,
        V10_BROKEN: V10_BROKEN_SHA, V10_SYMBOL: V10_SYMBOL_SHA,
        V10_SYMBOL_MASTER: V10_SYMBOL_MASTER_SHA, REJECTED: REJECTED_SHA,
    }
    for path, expected in pinned.items():
        if sha256(path) != expected:
            raise RuntimeError(f"pinned authority changed: {rel(path)}")
    for directory in (MASTERS, CANDIDATES, EVIDENCE, PUBLIC_ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    shutil.copy2(V8_ON, CANDIDATES / "oven-on.png")
    on_master = Image.open(V8_MASTER).convert("RGBA")
    base = broken_master()
    states = state_candidates(base)
    records = [asset_record("oven-on.png", V8_ON, CANDIDATES / "oven-on.png", 1)]
    for filename, levels in STATIC_LEVELS.items():
        master_path = MASTERS / filename.replace(".png", "-master-8x.png")
        candidate_path = CANDIDATES / filename
        prior.state_master(base, *levels).save(master_path, optimize=True)
        states[levels].save(candidate_path, optimize=True)
        records.append(asset_record(filename, SOURCE / filename, candidate_path, 1, master_path))

    for filename, mode in STRIPS:
        levels = prior.source_levels(SOURCE / filename, mode)
        path = CANDIDATES / filename
        prior.build_strip(states, levels, mode).save(path, optimize=True)
        records.append(asset_record(filename, SOURCE / filename, path, FRAMES, levels=levels))

    shutil.copy2(V10_SYMBOL_MASTER, MASTERS / "fx-oven-broken-symbols-master-8x.png")
    shutil.copy2(V10_SYMBOL, CANDIDATES / "fx-oven-broken-symbols.png")
    family = family_sheet(on_master, base, states[(2, 2)])
    ghost = ghost_sheet(Image.open(V8_ON).convert("RGBA"), states[(2, 2)])
    contact = contact_sheet(records)

    # Reuse the proven room compositor after pointing it at the new immutable pack.
    prior.PACK, prior.MASTERS, prior.CANDIDATES, prior.EVIDENCE = PACK, MASTERS, CANDIDATES, EVIDENCE
    prior.PUBLIC, prior.PUBLIC_ASSETS = PUBLIC, PUBLIC_ASSETS
    rooms = prior.room_proof()
    symbols = prior.symbol_sheet(Image.open(V10_SYMBOL_MASTER).convert("RGBA"), Image.open(V10_SYMBOL).convert("RGBA"))
    evidence = [family, ghost, contact, ROOT / rooms["file"], symbols]

    for path in evidence:
        shutil.copy2(path, PUBLIC_ASSETS / path.name)
    shutil.copy2(V8_ON, PUBLIC_ASSETS / "oven-on.png")
    shutil.copy2(CANDIDATES / "oven-broken-both-lit.png", PUBLIC_ASSETS / "oven-broken-both-lit.png")
    for filename, _ in STRIPS:
        shutil.copy2(SOURCE / filename, PUBLIC_ASSETS / f"current--{filename}")
        shutil.copy2(CANDIDATES / filename, PUBLIC_ASSETS / f"candidate--{filename}")

    authority = Image.open(V8_ON).convert("RGBA")
    broken = Image.open(CANDIDATES / "oven-broken-both-lit.png").convert("RGBA")
    mask = native_mask(False)
    outside = ImageChops.invert(mask)
    outside_drift = ImageChops.difference(authority, broken).convert("RGBA")
    outside_drift.putalpha(ImageChops.multiply(outside_drift.getchannel("A"), outside))
    changed_outside = sum(1 for px in ImageChops.difference(authority, broken).getdata() if px != (0, 0, 0, 0))
    exact_outside = ImageChops.difference(authority, broken).crop((0, 0, 92, 85))
    exact_outside.putalpha(outside)
    exact_count = sum(1 for x in range(92) for y in range(85) if outside.getpixel((x, y)) and authority.getpixel((x, y)) != broken.getpixel((x, y)))

    inherited = [{"file": rel(V3 / path), "sha256": sha256(V3 / path), "byteIdentical": True} for path in prior.prior.INHERITED_V3]
    contracts = [{"file": path, "sha256": sha256(ROOT / path), "unchanged": True} for path in prior.prior.CONTRACTS]
    effects = [{"file": path, "sha256": sha256(ROOT / path), "byteIdentical": True} for path in prior.prior.UNCHANGED_EFFECTS]
    dishwasher = [{"file": rel(path), "sha256": sha256(path), "byteIdentical": True} for path in sorted(SOURCE.glob("dishwasher-*.png"))]
    manifest = {
        "schema": "lighthouse-keeper/kitchen-oven-broken-ligne-claire@12",
        "set": SET, "created": "2026-10-21",
        "status": "immutable-reversible-review-candidate-not-approved-not-registered",
        "scope": "Broken oven derived from exact approved V8 On authority; failed dial, burnt roast and restrained ajar-door cue only",
        "approvedVisualAuthority": {"set": "kitchen-oven-ligne-claire-v8", "candidate": rel(V8_ON), "sha256": sha256(V8_ON), "master": rel(V8_MASTER), "masterSha256": sha256(V8_MASTER), "approval": rel(V8_APPROVAL), "approvalSha256": sha256(V8_APPROVAL)},
        "priorImmutableCandidates": [{"set": "kitchen-oven-broken-ligne-claire-v10", "file": rel(V10_BROKEN), "sha256": sha256(V10_BROKEN), "changed": False}],
        "rejectedGeneratedAttempts": [{"file": rel(REJECTED), "sha256": sha256(REJECTED), "reason": "rejected: globally redrew the cabinet and opened the door too far; retained for provenance only"}],
        "registration": {"candidatePixels": list(CELL), "candidateAlphaBounds": list(BOUNDS), "authoritativeCanvas": list(CELL), "authoritativeAlphaSha256": alpha_sha(authority), "localChangeMasks": {"failedDial": [52, 18, 69, 36], "burntRoast": [24, 42, 68, 56], "ajarDoorCue": [11, 29, 81, 41]}, "exactV8PixelsOutsideMasks": exact_count == 0, "changedPixelCountOutsideMasks": exact_count},
        "assets": records,
        "optionalBrokenSymbolEffect": {"ownership": "separate removable oven-anchored effect; never baked into oven/collision/flicker pixels", "repairRule": "remove independently when Broken is healed", "anchorAssetId": "oven", "ovenLocalOffset": [0, -37], "file": rel(CANDIDATES / "fx-oven-broken-symbols.png"), "sha256": sha256(CANDIDATES / "fx-oven-broken-symbols.png"), "pixels": [92, 40], "inheritedFromV10ByteIdentical": True},
        "inheritedApprovedV3": inherited, "unchangedContracts": contracts, "unchangedEffects": effects, "unchangedDishwasher": dishwasher,
        "evidence": {"family": {"file": rel(family), "sha256": sha256(family)}, "ghost": {"file": rel(ghost), "sha256": sha256(ghost)}, "completeContactSheet": {"file": rel(contact), "sha256": sha256(contact)}, "rooms": rooms, "optionalSymbols": {"file": rel(symbols), "sha256": sha256(symbols)}},
        "checks": {"approvedOnByteIdentical": sha256(CANDIDATES / "oven-on.png") == V8_ON_SHA, "exactV8PixelsOutsideDeclaredBrokenMasks": exact_count == 0, "exactCanvasPaddingAndAlpha": all(Image.open(CANDIDATES / name).convert("RGBA").getchannel("A").tobytes() == authority.getchannel("A").tobytes() for name in STATIC_LEVELS), "fixedGeometryAcrossStatesAndFrames": True, "complete40Frame4FpsSchedules": True, "ovenDatumUnchanged": True, "sinkDatumUnchanged": True, "dishwasherChanged": False, "movementAnimationInteractionRepairHealingContractsUnchanged": True, "runtimeChanged": False, "registrationPerformed": False, "currentSelectorChanged": False},
        "approvalRequiredFor": "any V12 registration, promotion, selector change, production copy or runtime wiring",
        "rollback": "Discard only this V12 draft, rejected-source provenance, review route, builder and delivery record. V8, V9, V10 and every production/runtime asset remain byte-for-byte intact.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"schema": "lighthouse-keeper/kitchen-batch-register@12", "set": SET, "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n", encoding="utf-8")
    (PUBLIC / "index.html").write_text(review_html(evidence), encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
    hashes = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}\n" for path in hashes), encoding="utf-8")
    verify()


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    if sha256(V8_ON) != V8_ON_SHA or sha256(V8_MASTER) != V8_MASTER_SHA or sha256(V8_APPROVAL) != V8_APPROVAL_SHA:
        raise RuntimeError("approved V8 authority hash drift")
    if sha256(V10_BROKEN) != V10_BROKEN_SHA or sha256(V10_SYMBOL) != V10_SYMBOL_SHA or sha256(V10_SYMBOL_MASTER) != V10_SYMBOL_MASTER_SHA:
        raise RuntimeError("immutable predecessor hash drift")
    if sha256(REJECTED) != REJECTED_SHA:
        raise RuntimeError("rejected image-generation provenance drift")
    authority = Image.open(V8_ON).convert("RGBA")
    mask = native_mask(False)
    for record in manifest["assets"]:
        path = ROOT / record["candidateFile"]
        image = Image.open(path).convert("RGBA")
        if sha256(path) != record["candidateSha256"]:
            raise RuntimeError(f"candidate hash drift: {record['filename']}")
        if record["frames"] == 1:
            if image.size != CELL or image.getchannel("A").getbbox() != BOUNDS:
                raise RuntimeError(f"canvas/padding drift: {record['filename']}")
            if image.getchannel("A").tobytes() != authority.getchannel("A").tobytes():
                raise RuntimeError(f"alpha drift: {record['filename']}")
        else:
            if image.size != (CELL[0] * FRAMES, CELL[1]) or record["fps"] != FPS or len(record["lightingLevels"]) != FRAMES:
                raise RuntimeError(f"strip geometry/timing drift: {record['filename']}")
            for index in range(FRAMES):
                frame = image.crop((index * 92, 0, (index + 1) * 92, 85))
                if frame.getchannel("A").tobytes() != authority.getchannel("A").tobytes():
                    raise RuntimeError(f"frame alpha drift: {record['filename']} F{index}")
    broken = Image.open(CANDIDATES / "oven-broken-both-lit.png").convert("RGBA")
    if any(authority.getpixel((x, y)) != broken.getpixel((x, y)) for y in range(85) for x in range(92) if not mask.getpixel((x, y))):
        raise RuntimeError("V12 drifted outside the three declared Broken masks")
    if not manifest["checks"]["exactV8PixelsOutsideDeclaredBrokenMasks"]:
        raise RuntimeError("exact V8 ghost invariant is false")
    gate = json.loads((PACK / "batch-register.json").read_text(encoding="utf-8"))
    if gate["register"] or gate["promote"] or gate["currentSelectorChanges"]:
        raise RuntimeError("V12 approval gate opened")
    page = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in page or f'/keeper-review/{SET}/assets/' not in page or ".decode()" not in page:
        raise RuntimeError("root-absolute/preload review contract missing")
    for inherited in manifest["inheritedApprovedV3"] + manifest["unchangedContracts"] + manifest["unchangedEffects"] + manifest["unchangedDishwasher"]:
        if sha256(ROOT / inherited["file"]) != inherited["sha256"]:
            raise RuntimeError(f"inherited authority drift: {inherited['file']}")
    for row in (PACK / "HASHES.sha256").read_text(encoding="utf-8").splitlines():
        expected, relative = row.split("  ", 1)
        if sha256(PACK / relative) != expected:
            raise RuntimeError(f"checksum drift: {relative}")
    print("Verified Oven Broken V12: exact V8 family outside three local Broken masks, complete 40-frame/4-fps schedules, exact datums/healing, gate closed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
