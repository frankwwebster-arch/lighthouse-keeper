#!/usr/bin/env python3
"""Build immutable exact-alpha ligne-claire mixing-bowl states from V36."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-mixing-bowl-ligne-claire-v1"
PACK = ROOT / "art/drafts/kitchen-mixing-bowl-ligne-claire-2026-10-22-v1"
SOURCE = ROOT / "art/raw/kitchen-mixing-bowl-states-2026-10-18-v36"
CONTRACT = ROOT / "art/drafts/kitchen-mixing-bowl-states-2026-10-18-v36/candidate-catalogue.json"
PUBLIC = ROOT / "public/keeper-review" / SET

INK = (5, 24, 36)
CREAM = (250, 244, 224)
CREAM_DARK = (226, 216, 192)
CORAL = (217, 62, 47)
BLUE = (45, 119, 157)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_sha(im: Image.Image) -> str:
    return hashlib.sha256(im.getchannel("A").tobytes()).hexdigest()


def recolour(source: Image.Image) -> Image.Image:
    out = Image.new("RGBA", source.size); pixels = []
    for r, g, b, a in source.getdata():
        if not a:
            pixels.append((0, 0, 0, 0)); continue
        hi, lo = max(r, g, b), min(r, g, b); lum = (r * 3 + g * 5 + b * 2) // 10
        if lum < 72 or (hi - lo < 15 and lum < 104): colour = INK
        elif r > g * 1.35 and r > b * 1.25: colour = CORAL
        elif b > r * 1.13 and b > g * 1.04: colour = BLUE
        elif lum > 185: colour = CREAM
        else: colour = CREAM_DARK
        pixels.append((*colour, a))
    out.putdata(pixels); return out


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    out = Image.new("RGBA", size, (246, 240, 220, 255)); d = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2: d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def build() -> None:
    if PACK.exists() or PUBLIC.exists(): raise RuntimeError("refusing to overwrite immutable mixing-bowl V1")
    for p in (PACK / "candidates", PACK / "evidence", PUBLIC / "assets"): p.mkdir(parents=True)
    records = []
    for state in ("standard", "broken"):
        filename = f"mixing-bowl-{state}.png"; source_path = SOURCE / filename
        source = Image.open(source_path).convert("RGBA"); candidate = recolour(source); target = PACK / "candidates" / filename; candidate.save(target, optimize=True)
        records.append({"state": state, "filename": filename, "sourceFile": source_path.relative_to(ROOT).as_posix(), "sourceSha256": sha(source_path), "candidateFile": target.relative_to(ROOT).as_posix(), "candidateSha256": sha(target), "pixels": list(source.size), "alphaBounds": list(source.getchannel("A").getbbox()), "sourceAlphaSha256": alpha_sha(source), "candidateAlphaSha256": alpha_sha(candidate)})

    font = ImageFont.load_default(); sheet = Image.new("RGBA", (1120, 530), (250, 244, 224, 255)); d = ImageDraw.Draw(sheet)
    d.text((18, 14), "Mixing bowl V36 authority / Ligne-Claire V1 / exact alpha ghost / 64 px proof", fill=INK, font=font)
    for row, record in enumerate(records):
        src = Image.open(ROOT / record["sourceFile"]).convert("RGBA"); cand = Image.open(ROOT / record["candidateFile"]).convert("RGBA"); y = 44 + row * 232
        for col, im in enumerate((src, cand)):
            panel = checker((330, 200)); panel.alpha_composite(im.resize((252, 204), Image.Resampling.NEAREST), (39, -2)); sheet.alpha_composite(panel, (10 + col * 345, y))
        ghost = checker((330, 200)); ghost.alpha_composite(cand.resize((252, 204), Image.Resampling.NEAREST), (39, -2)); tint = Image.new("RGBA", src.size, (232, 72, 86, 0)); tint.putalpha(src.getchannel("A").point(lambda v: round(v * .34))); ghost.alpha_composite(tint.resize((252, 204), Image.Resampling.NEAREST), (39, -2)); sheet.alpha_composite(ghost, (700, y)); sheet.alpha_composite(cand.resize((79, 64), Image.Resampling.LANCZOS), (1035, y + 12))
        d.text((18, y + 205), f"CURRENT {record['filename']} 84x68", fill=INK, font=font); d.text((363, y + 205), "V1 CANDIDATE", fill=INK, font=font); d.text((708, y + 205), "ALPHA GHOST", fill=INK, font=font)
    evidence = PACK / "evidence/mixing-bowl-current-candidate-ghost-64px.png"; sheet.save(evidence, optimize=True)

    contract = json.loads(CONTRACT.read_text())
    manifest = {"schema": "lighthouse-keeper/kitchen-mixing-bowl-ligne-claire@1", "set": SET, "created": "2026-10-22", "status": "immutable-review-candidate-not-approved-not-registered", "sourceSet": "kitchen-mixing-bowl-states-v36", "contractFile": CONTRACT.relative_to(ROOT).as_posix(), "contractSha256": sha(CONTRACT), "objects": records, "effects": [], "preservedBehaviour": {"cellPixels": contract["cellPixels"], "roomCellTopLeft": contract["roomCellTopLeft"], "construction": contract["construction"], "requirements": contract["requirements"], "sfxCues": contract["sfxCues"]}, "unchanged": ["canvas", "alpha", "transparent padding", "state geometry", "room position", "large ceramic pieces", "sound cue", "runtime"], "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True}, "evidence": {"file": evidence.relative_to(ROOT).as_posix(), "sha256": sha(evidence)}, "rollback": "Discard only this V1 pack and review route."}
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n"); (PACK / "batch-register.json").write_text(json.dumps({"status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n")
    for r in records:
        shutil.copy2(ROOT / r["sourceFile"], PUBLIC / "assets" / ("current--" + r["filename"])); shutil.copy2(ROOT / r["candidateFile"], PUBLIC / "assets" / ("candidate--" + r["filename"]))
    shutil.copy2(evidence, PUBLIC / "assets" / evidence.name)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mixing Bowl Ligne-Claire V1</title><style>body{{margin:0;background:#f6e5b7;color:#051824;font:16px/1.45 system-ui}}header,main{{max-width:1160px;margin:auto;padding:22px}}header{{border-bottom:4px solid #051824}}.status{{border:2px solid #051824;background:#e7a638;padding:6px 10px;font-weight:800}}article{{background:#fff9e8;border:2px solid #051824;margin:18px 0;padding:14px}}img{{display:block;width:100%;image-rendering:auto}}</style></head><body><header><span class="status">IMMUTABLE CANDIDATE - NOT CURRENT</span><h1>Mixing Bowl Ligne-Claire V1</h1><p>Exact 84x68 masks and room placement. The intact vessel, large broken pieces, no-animation requirement, break cue and runtime are unchanged.</p></header><main><article><img src="/keeper-review/{SET}/assets/{evidence.name}"></article></main></body></html>'''; (PUBLIC / "index.html").write_text(html); (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")


def verify() -> None:
    m = json.loads((PACK / "manifest.json").read_text()); c = json.loads(CONTRACT.read_text())
    for r in m["objects"]:
        src = Image.open(ROOT / r["sourceFile"]).convert("RGBA"); cand = Image.open(ROOT / r["candidateFile"]).convert("RGBA")
        if src.size != cand.size or alpha_sha(src) != alpha_sha(cand) or src.getchannel("A").getbbox() != cand.getchannel("A").getbbox(): raise RuntimeError(f"bowl geometry drift: {r['filename']}")
    if m["preservedBehaviour"]["requirements"] != c["requirements"] or m["registration"]["register"] or m["registration"]["promote"]: raise RuntimeError("contract/gate drift")
    if 'src="assets/' in (PUBLIC / "index.html").read_text(): raise RuntimeError("relative review URL")
    print("Verified mixing bowl V1: 2 exact 84x68 alphas; V36 placement, break structure/cue and runtime preserved")


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--verify", action="store_true"); a = p.parse_args(); verify() if a.verify else build()
