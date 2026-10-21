#!/usr/bin/env python3
"""Build V15 Broken Ajar from approved V12 body plus established V10 door geometry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_kitchen_oven_broken_ajar_ligne_claire_v14 as base


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-broken-ajar-ligne-claire-v15"
DATED = "kitchen-oven-broken-ajar-ligne-claire-2026-10-22-v15"
PACK = ROOT / "art" / "drafts" / DATED
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates" / "oven"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"
INK = base.INK


def native_change_mask(include_lighting: bool = False) -> Image.Image:
    mask = Image.new("L", base.CELL, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((52, 18, 69, 36), fill=255)
    draw.ellipse((24, 42, 68, 56), fill=255)
    draw.rectangle((5, 27, 87, 81), fill=255)
    if include_lighting:
        draw.rounded_rectangle((16, 34, 78, 65), radius=3, fill=255)
        draw.ellipse((70, 20, 80, 31), fill=255)
    return mask


def ajar_master() -> Image.Image:
    v10 = Image.open(base.V10_MASTER).convert("RGBA")
    result = Image.open(base.V12_MASTER).convert("RGBA")
    original = result.copy()
    cavity = v10.crop((98, 270, 642, 515))
    result.paste(cavity, (98, 270), cavity)
    result.paste(result.crop((285, 270, 420, 330)), (420, 270))
    dial = original.crop((470, 210, 545, 290))
    dial_mask = Image.new("L", dial.size, 0)
    ImageDraw.Draw(dial_mask).ellipse((0, 0, 74, 74), fill=255)
    result.paste(dial, (470, 210), dial_mask)
    door = v10.crop((45, 474, 691, 645))
    result.paste(door, (45, 474), door)
    result.putalpha(Image.open(base.V8_MASTER).convert("RGBA").getchannel("A"))
    return result


def family_sheet(v12: Image.Image, v15: Image.Image) -> Path:
    sheet = Image.new("RGBA", (1180, 620), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((18, 16), "Approved V12 Broken / V15 Broken Ajar", fill=INK, font=font)
    draw.text((18, 40), "Approved V12 oven family with the established attached part-open door geometry only.", fill=INK, font=font)
    sheet.alpha_composite(base.panel(v12), (18, 74))
    sheet.alpha_composite(base.panel(v15), (610, 74))
    draw.text((18, 590), "APPROVED V12 · shallow cue", fill=INK, font=font)
    draw.text((610, 590), "V15 CANDIDATE · physical door ajar", fill=INK, font=font)
    path = EVIDENCE / "approved-v12-vs-v15-ajar-family.png"
    sheet.save(path, optimize=True)
    return path


def ghost_sheet(v12: Image.Image, v15: Image.Image) -> Path:
    sheet = Image.new("RGBA", (1180, 620), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((18, 16), "V12 / V15 attached-door ghost proof", fill=INK, font=font)
    draw.text((18, 40), "Only the declared door/cavity locality may move; countertop, body and datum stay fixed.", fill=INK, font=font)
    marked = base.panel(v12)
    tint = Image.new("RGBA", marked.size, (229, 166, 55, 94))
    marked.alpha_composite(Image.composite(tint, Image.new("RGBA", marked.size), native_change_mask().resize(marked.size, Image.Resampling.NEAREST)))
    sheet.alpha_composite(marked, (18, 74))
    sheet.alpha_composite(base.panel(Image.blend(v12, v15, 0.5)), (610, 74))
    draw.text((18, 590), "DECLARED LOCAL CHANGE MASK", fill=INK, font=font)
    draw.text((610, 590), "50% APPROVED V12 / V15 GHOST", fill=INK, font=font)
    path = EVIDENCE / "v12-v15-door-opacity-ghost.png"
    sheet.save(path, optimize=True)
    return path


def contact_sheet(records: list[dict[str, object]]) -> Path:
    samples = (0, 5, 10, 15, 20, 25, 30, 35)
    sheet = Image.new("RGBA", (1480, 1960), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((16, 15), "Broken Ajar V15 · complete approved-versus-candidate contact sheet", fill=INK, font=font)
    y = 48
    for record in records[:4]:
        current = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        sheet.alpha_composite(base.panel(current, 3), (20, y))
        sheet.alpha_composite(base.panel(candidate, 3), (430, y))
        draw.text((20, y + 260), f"APPROVED V12 · {record['filename']}", fill=INK, font=font)
        draw.text((430, y + 260), f"V15 AJAR · {record['filename']}", fill=INK, font=font)
        y += 290
    for record in records[4:]:
        for row, key in enumerate(("sourceFile", "candidateFile")):
            strip = Image.open(ROOT / record[key]).convert("RGBA")
            for col, frame in enumerate(samples):
                sample = strip.crop((frame * 92, 0, (frame + 1) * 92, 85))
                sheet.alpha_composite(base.panel(sample, 2), (col * 184, y + row * 190))
        y += 390
    path = EVIDENCE / "complete-v12-vs-v15-contact-sheet.png"
    sheet.crop((0, 0, 1480, y + 10)).save(path, optimize=True)
    return path


original_review_html = base.review_html


def review_html(evidence: list[Path]) -> str:
    return original_review_html(evidence).replace("Broken Ajar V14", "Broken Ajar V15").replace("Ligne-Claire V14", "Ligne-Claire V15").replace("V14 preserves", "V15 preserves").replace("V14 opacity", "V15 opacity").replace("V14 Broken Ajar", "V15 Broken Ajar").replace("V12 / V14 ghost", "V12 / V15 ghost").replace("oven-broken-v14.png", "oven-broken-v15.png")


def configure() -> None:
    base.SET, base.DATED = SET, DATED
    base.PACK, base.MASTERS, base.CANDIDATES, base.EVIDENCE = PACK, MASTERS, CANDIDATES, EVIDENCE
    base.PUBLIC, base.PUBLIC_ASSETS = PUBLIC, PUBLIC_ASSETS
    base.native_change_mask = native_change_mask
    base.ajar_master = ajar_master
    base.family_sheet = family_sheet
    base.ghost_sheet = ghost_sheet
    base.contact_sheet = contact_sheet
    base.review_html = review_html


def build() -> None:
    configure()
    base.build()
    (PUBLIC_ASSETS / "oven-broken-v14.png").replace(PUBLIC_ASSETS / "oven-broken-v15.png")
    manifest_path = PACK / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["schema"] = "lighthouse-keeper/kitchen-oven-broken-ajar-ligne-claire@15"
    manifest["status"] = "immutable-reversible-review-candidate-not-approved-not-registered"
    manifest["scope"] = "Approved V12 oven body with the established V10 attached moderate part-open door geometry; door/cavity locality only"
    manifest["registration"]["localChangeMasks"]["attachedAjarDoorAndCavity"] = [5, 27, 87, 81]
    manifest["priorRejectedProof"] = {"set": "kitchen-oven-broken-ajar-ligne-claire-v14", "reason": "foreshortened glass read as a displaced handle rather than a physical attached door", "preserved": True}
    manifest["approvalRequiredFor"] = "any V15 registration, promotion, selector change, production copy or runtime wiring"
    manifest["rollback"] = "Discard only this V15 draft, review route, builder and delivery record. Approved V8/V12, V13 Off, rejected V14 proof and every source/production/runtime file remain byte-for-byte intact."
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"schema":"lighthouse-keeper/kitchen-batch-register@15","set":SET,"status":"blocked-pending-explicit-frank-approval","register":False,"promote":False,"currentSelectorChanges":[]}, indent=2) + "\n", encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
    hashes = sorted(p for p in PACK.rglob("*") if p.is_file() and p.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("".join(f"{base.sha256(p)}  {p.relative_to(PACK).as_posix()}\n" for p in hashes), encoding="utf-8")
    verify()


def verify() -> None:
    configure()
    base.verify()
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    if manifest["schema"].split("@")[-1] != "15" or manifest["registration"]["localChangeMasks"]["attachedAjarDoorAndCavity"] != [5, 27, 87, 81]:
        raise RuntimeError("V15 manifest/version mask drift")
    print("Verified Oven Broken Ajar V15: physical attached door part-open, exact family alpha/datum, healing unchanged, gate closed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
