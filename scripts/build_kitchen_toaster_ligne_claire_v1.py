#!/usr/bin/env python3
"""Build an immutable, exact-alpha ligne-claire toaster family from V34."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VERSION = int(os.environ.get("TOASTER_LIGNE_CLAIRE_VERSION", "1"))
SET = f"kitchen-toaster-ligne-claire-v{VERSION}"
PACK = ROOT / f"art/drafts/kitchen-toaster-ligne-claire-2026-10-22-v{VERSION}"
SOURCE = ROOT / "art/raw/kitchen-toaster-states-2026-10-18-v34"
CONTRACT = ROOT / "art/drafts/kitchen-toaster-states-2026-10-18-v34/candidate-catalogue.json"
PUBLIC = ROOT / "public/keeper-review" / SET

INK = (5, 24, 36)
CORAL = (217, 62, 47)
CORAL_DARK = (166, 45, 40)
RED = (236, 69, 45)
BLUE = (45, 119, 157)
METAL = (174, 187, 185)
CREAM = (250, 244, 224)
BREAD = (231, 164, 73)
BREAD_DARK = (171, 100, 45)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_sha(im: Image.Image) -> str:
    return hashlib.sha256(im.getchannel("A").tobytes()).hexdigest()


def recolour(source: Image.Image, state: str) -> Image.Image:
    """Reduce V34 modelling to closed flat spot colours without moving a pixel."""
    out = Image.new("RGBA", source.size)
    pixels = []
    for y in range(source.height):
        for x in range(source.width):
            r, g, b, a = source.getpixel((x, y))
            if not a:
                pixels.append((0, 0, 0, 0)); continue
            hi, lo = max(r, g, b), min(r, g, b)
            lum = (r * 3 + g * 5 + b * 2) // 10
            # V2 corrects V1's black side plane: chromatic red remains enamel.
            if VERSION >= 4 and state != "standard" and 27 <= x <= 58 and y < 45 and r > 75 and g > r * .30 and r > b * 1.08:
                colour = BREAD if lum > 115 else BREAD_DARK
            elif VERSION == 3 and state != "standard" and 27 <= x <= 58 and y < 45 and r > g * 1.2 and hi - lo > 28:
                colour = BREAD if lum > 115 else BREAD_DARK
            elif VERSION >= 2 and r > g * 1.35 and r > b * 1.25 and hi - lo > 28:
                colour = CORAL if lum > 90 else CORAL_DARK
            # Real dark edges, slot, feet, switch and broken fissures.
            elif lum < 63 or (hi - lo < 18 and lum < 100):
                colour = INK
            # Toast remains bread-coloured in On/Broken; it is not a light source.
            elif state != "standard" and y < 43 and r > 125 and g > 55 and g > b * 1.15:
                colour = BREAD if lum > 125 else BREAD_DARK
            # Painted red enamel uses two planes only.
            elif r > g * 1.35 and r > b * 1.25:
                colour = CORAL if lum > 90 else CORAL_DARK
            # Neutral front metal and control hardware.
            elif hi - lo < 30:
                colour = METAL if lum > 115 else INK
            elif b > r * 1.10:
                colour = BLUE
            elif r > 150 and g > 125:
                colour = CREAM
            else:
                colour = CORAL_DARK
            pixels.append((*colour, a))
    out.putdata(pixels)
    return out


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    out = Image.new("RGBA", size, (246, 240, 220, 255)); d = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError(f"refusing to overwrite immutable toaster V{VERSION}")
    for p in (PACK / "candidates", PACK / "effects", PACK / "evidence", PUBLIC / "assets"):
        p.mkdir(parents=True)
    records = []
    for state in ("standard", "on", "broken"):
        filename = f"toaster-{state}.png"
        source_path = SOURCE / filename
        source = Image.open(source_path).convert("RGBA")
        candidate = recolour(source, state)
        target = PACK / "candidates" / filename
        candidate.save(target, optimize=True)
        records.append({
            "state": state, "filename": filename,
            "sourceFile": source_path.relative_to(ROOT).as_posix(), "sourceSha256": sha(source_path),
            "candidateFile": target.relative_to(ROOT).as_posix(), "candidateSha256": sha(target),
            "pixels": list(source.size), "alphaBounds": list(source.getchannel("A").getbbox()),
            "sourceAlphaSha256": alpha_sha(source), "candidateAlphaSha256": alpha_sha(candidate),
        })
    effect_source = SOURCE / "fx-toaster-restrained_heat-f40.png"
    effect_target = PACK / "effects" / effect_source.name
    shutil.copy2(effect_source, effect_target)

    font = ImageFont.load_default(); sheet = Image.new("RGBA", (1120, 760), (250, 244, 224, 255)); d = ImageDraw.Draw(sheet)
    d.text((18, 14), f"Toaster V34 authority / Ligne-Claire V{VERSION} / exact alpha ghost / 64 px proof", fill=INK, font=font)
    for row, record in enumerate(records):
        src = Image.open(ROOT / record["sourceFile"]).convert("RGBA"); cand = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        y = 44 + row * 232
        for col, im in enumerate((src, cand)):
            panel = checker((330, 200)); shown = im.resize((252, 204), Image.Resampling.NEAREST); panel.alpha_composite(shown, (39, -2)); sheet.alpha_composite(panel, (10 + col * 345, y))
        ghost = checker((330, 200)); shown = cand.resize((252, 204), Image.Resampling.NEAREST); ghost.alpha_composite(shown, (39, -2))
        tint = Image.new("RGBA", src.size, (232, 72, 86, 0)); tint.putalpha(src.getchannel("A").point(lambda v: round(v * .34))); ghost.alpha_composite(tint.resize((252, 204), Image.Resampling.NEAREST), (39, -2)); sheet.alpha_composite(ghost, (700, y))
        sheet.alpha_composite(cand.resize((79, 64), Image.Resampling.LANCZOS), (1035, y + 12))
        d.text((18, y + 205), f"CURRENT {record['filename']} 84x68", fill=INK, font=font); d.text((363, y + 205), f"V{VERSION} CANDIDATE", fill=INK, font=font); d.text((708, y + 205), "ALPHA GHOST", fill=INK, font=font)
    evidence = PACK / "evidence/toaster-current-candidate-ghost-64px.png"; sheet.save(evidence, optimize=True)

    contract = json.loads(CONTRACT.read_text())
    manifest = {
        "schema": "lighthouse-keeper/kitchen-toaster-ligne-claire@1", "set": SET, "version": VERSION, "created": "2026-10-22",
        "status": "immutable-review-candidate-not-approved-not-registered", "sourceSet": "kitchen-toaster-states-v34",
        "contractFile": CONTRACT.relative_to(ROOT).as_posix(), "contractSha256": sha(CONTRACT), "objects": records,
        "effects": [{"filename": effect_source.name, "sourceFile": effect_source.relative_to(ROOT).as_posix(), "sourceSha256": sha(effect_source), "preservedFile": effect_target.relative_to(ROOT).as_posix(), "preservedSha256": sha(effect_target), "frames": 40, "fps": 4, "byteExact": True}],
        "preservedBehaviour": {"cellPixels": contract["cellPixels"], "roomCellTopLeft": contract["roomCellTopLeft"], "construction": contract["construction"], "requirements": contract["requirements"], "sfxCues": contract["sfxCues"]},
        "unchanged": ["canvas", "alpha", "transparent padding", "state geometry", "room position", "separate heat strip", "40 frames", "4 fps", "sound cues", "runtime"],
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True},
        "evidence": {"file": evidence.relative_to(ROOT).as_posix(), "sha256": sha(evidence)}, "rollback": f"Discard only this V{VERSION} pack and review route."
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({"status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n")
    for r in records:
        shutil.copy2(ROOT / r["sourceFile"], PUBLIC / "assets" / ("current--" + r["filename"])); shutil.copy2(ROOT / r["candidateFile"], PUBLIC / "assets" / ("candidate--" + r["filename"]))
    shutil.copy2(effect_target, PUBLIC / "assets" / effect_target.name); shutil.copy2(evidence, PUBLIC / "assets" / evidence.name)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Toaster Ligne-Claire V{VERSION}</title><style>body{{margin:0;background:#f6e5b7;color:#051824;font:16px/1.45 system-ui}}header,main{{max-width:1160px;margin:auto;padding:22px}}header{{border-bottom:4px solid #051824}}.status{{border:2px solid #051824;background:#e7a638;padding:6px 10px;font-weight:800}}article{{background:#fff9e8;border:2px solid #051824;margin:18px 0;padding:14px}}img{{display:block;width:100%;image-rendering:auto}}</style></head><body><header><span class="status">IMMUTABLE CANDIDATE - NOT CURRENT</span><h1>Toaster Ligne-Claire V{VERSION}</h1><p>Exact 84x68 state masks and room placement; the separate 40-frame restrained heat strip, timing, sound cues and runtime remain byte-for-byte untouched.</p></header><main><article><img src="/keeper-review/{SET}/assets/{evidence.name}"></article></main></body></html>'''
    (PUBLIC / "index.html").write_text(html); (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")


def verify() -> None:
    m = json.loads((PACK / "manifest.json").read_text()); c = json.loads(CONTRACT.read_text())
    for r in m["objects"]:
        src = Image.open(ROOT / r["sourceFile"]).convert("RGBA"); cand = Image.open(ROOT / r["candidateFile"]).convert("RGBA")
        if src.size != cand.size or alpha_sha(src) != alpha_sha(cand) or src.getchannel("A").getbbox() != cand.getchannel("A").getbbox():
            raise RuntimeError(f"toaster geometry drift: {r['filename']}")
    effect = m["effects"][0]
    if sha(ROOT / effect["sourceFile"]) != sha(ROOT / effect["preservedFile"]): raise RuntimeError("heat strip changed")
    if m["preservedBehaviour"]["requirements"] != c["requirements"] or m["registration"]["register"] or m["registration"]["promote"]: raise RuntimeError("contract/gate drift")
    if 'src="assets/' in (PUBLIC / "index.html").read_text(): raise RuntimeError("relative review URL")
    print(f"Verified toaster V{VERSION}: 3 exact 84x68 alphas; V34 position, heat strip, timing, cues and runtime preserved")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--verify", action="store_true"); args = parser.parse_args(); verify() if args.verify else build()
