#!/usr/bin/env python3
"""Build immutable Ligne-Claire pedal-bin states with V31 effects unchanged."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-bin-ligne-claire-v1"
DATED = "kitchen-bin-ligne-claire-2026-10-22-v1"
VERSION = 1
PACK = ROOT / "art" / "drafts" / DATED
SOURCE = ROOT / "art" / "raw" / "kitchen-bin-effects-2026-10-18-v31"
CONTRACT = ROOT / "art" / "drafts" / "kitchen-bin-effects-2026-10-18-v31" / "candidate-catalogue.json"
APPROVAL = ROOT / "docs" / "review" / "kitchen-bin-effects-v31-approval-2026-10-18.json"
PUBLIC = ROOT / "public" / "keeper-review" / SET
DENSITY = 8
LINE = 6
INK = "#051824"
SEA = "#53b1b5"
SEA_DARK = "#2d779d"
CREAM = "#faf4e0"
PAPER = "#f6e5b7"
COPPER = "#d36f2d"
BROWN = "#905231"
GREEN = "#73804d"
PALETTE = ((5, 24, 36), (83, 177, 181), (45, 119, 157), (250, 244, 224), (246, 229, 183), (211, 111, 45), (144, 82, 49), (115, 128, 77))


def p(value: float) -> int:
    return round(value * DENSITY)


def box(values: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    return tuple(p(v) for v in values)  # type: ignore[return-value]


def pts(values: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(p(x), p(y)) for x, y in values]


def edge(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], colour: str = INK, closed: bool = False) -> None:
    draw.line(pts(values + ([values[0]] if closed else [])), fill=colour, width=LINE, joint="curve")


def polygon(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], fill: str) -> None:
    draw.polygon(pts(values), fill=fill)
    edge(draw, values, closed=True)


def rounded(draw: ImageDraw.ImageDraw, values: tuple[float, float, float, float], radius: float, fill: str) -> None:
    draw.rounded_rectangle(box(values), radius=p(radius), fill=fill, outline=INK, width=LINE)


def ellipse(draw: ImageDraw.ImageDraw, values: tuple[float, float, float, float], fill: str) -> None:
    draw.ellipse(box(values), fill=fill, outline=INK, width=LINE)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def carcass(image: Image.Image) -> ImageDraw.ImageDraw:
    draw = ImageDraw.Draw(image)
    rounded(draw, (20.0, 23.0, 52.0, 66.0), 3.0, SEA)
    polygon(draw, [(46.0, 25.0), (52.0, 25.0), (52.0, 63.0), (47.0, 66.0)], SEA_DARK)
    rounded(draw, (24.0, 61.0, 48.0, 69.0), 2.0, INK)
    rounded(draw, (29.0, 62.0, 43.0, 67.0), 1.2, COPPER)
    return draw


def standard_master() -> Image.Image:
    image = Image.new("RGBA", (72 * DENSITY, 72 * DENSITY), (0, 0, 0, 0))
    draw = carcass(image)
    ellipse(draw, (18.0, 14.5, 54.0, 29.0), SEA)
    edge(draw, [(20.0, 24.5), (52.0, 24.5)], INK)
    return image


def broken_master() -> Image.Image:
    image = Image.new("RGBA", (72 * DENSITY, 72 * DENSITY), (0, 0, 0, 0))
    draw = carcass(image)
    # Same contents as the authority: large paper/tan scraps, one green item,
    # brown refuse and the two floor spills. No new symbols or objects.
    polygon(draw, [(11.0, 19.0), (15.0, 13.0), (21.0, 18.0), (25.0, 15.0), (28.0, 24.0), (22.0, 34.0), (13.0, 32.0)], PAPER)
    if VERSION >= 2:
        polygon(draw, [(23.0, 17.0), (27.0, 11.0), (33.0, 13.0), (36.0, 22.0), (31.0, 29.0), (25.0, 26.0)], BROWN)
        polygon(draw, [(29.0, 27.0), (33.0, 22.0), (38.0, 27.0), (37.0, 39.0), (30.0, 40.0)], GREEN)
        polygon(draw, [(34.0, 23.0), (39.0, 17.0), (45.0, 21.0), (48.0, 31.0), (43.0, 39.0), (36.0, 35.0)], PAPER)
        polygon(draw, [(43.0, 15.0), (48.0, 12.0), (53.0, 18.0), (52.0, 29.0), (46.0, 29.0)], PAPER)
        polygon(draw, [(49.0, 27.0), (55.0, 23.0), (61.0, 31.0), (60.0, 45.0), (54.0, 49.0), (50.0, 40.0)], BROWN)
        polygon(draw, [(17.0, 32.0), (22.0, 28.0), (28.0, 34.0), (26.0, 45.0), (20.0, 53.0), (17.0, 46.0)], COPPER)
    else:
        polygon(draw, [(23.0, 16.0), (29.0, 10.0), (36.0, 15.0), (42.0, 12.0), (47.0, 24.0), (38.0, 31.0), (27.0, 28.0)], BROWN)
        polygon(draw, [(42.0, 15.0), (48.0, 12.0), (53.0, 19.0), (52.0, 30.0), (45.0, 29.0)], PAPER)
        polygon(draw, [(28.0, 27.0), (33.0, 23.0), (38.0, 28.0), (37.0, 39.0), (30.0, 40.0)], GREEN)
        polygon(draw, [(16.0, 31.0), (22.0, 28.0), (28.0, 34.0), (25.0, 48.0), (18.0, 53.0)], COPPER)
        polygon(draw, [(46.0, 28.0), (55.0, 25.0), (62.0, 34.0), (59.0, 49.0), (52.0, 44.0)], BROWN)
    edge(draw, [(19.0, 27.0), (53.0, 29.0)], INK)
    polygon(draw, [(17.0, 8.0), (25.0, 5.0), (46.0, 7.0), (57.0, 15.0), (52.0, 20.0), (29.0, 15.0)], SEA)
    polygon(draw, [(8.0, 61.0), (13.0, 56.0), (18.0, 62.0), (15.0, 68.0), (7.0, 67.0)], PAPER)
    polygon(draw, [(52.0, 63.0), (59.0, 57.0), (63.0, 64.0), (68.0, 62.0), (65.0, 68.0), (55.0, 68.0)], COPPER)
    return image


def register(master: Image.Image, source: Image.Image) -> Image.Image:
    made = master.resize(source.size, Image.Resampling.LANCZOS).convert("RGBA")
    pixels = []
    for candidate, original in zip(made.getdata(), source.getdata()):
        if original[3] and candidate[3] < 8:
            colour = min(PALETTE, key=lambda value: sum((value[i] - original[i]) ** 2 for i in range(3)))
            pixels.append((*colour, candidate[3]))
        else:
            pixels.append(candidate)
    made.putdata(pixels)
    made.putalpha(source.getchannel("A"))
    return made


def checker(size: tuple[int, int], cell: int = 14) -> Image.Image:
    out = Image.new("RGBA", size, (246, 240, 220, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable bin V1")
    for path in (PACK / "masters", PACK / "candidates", PACK / "effects", PACK / "evidence", PUBLIC / "assets"):
        path.mkdir(parents=True)
    records = []
    for filename, renderer in (("bin-standard.png", standard_master), ("bin-broken-overflowing.png", broken_master)):
        source_path = SOURCE / filename
        source = Image.open(source_path).convert("RGBA")
        master = renderer()
        candidate = register(master, source)
        master_path = PACK / "masters" / filename.replace(".png", "-master-8x.png")
        candidate_path = PACK / "candidates" / filename
        master.save(master_path, optimize=True)
        candidate.save(candidate_path, optimize=True)
        records.append({"filename": filename, "sourceFile": source_path.relative_to(ROOT).as_posix(), "sourceSha256": sha256(source_path), "sourcePixels": list(source.size), "sourceAlphaBounds": list(source.getchannel("A").getbbox()), "sourceAlphaSha256": alpha_sha(source), "masterFile": master_path.relative_to(ROOT).as_posix(), "masterSha256": sha256(master_path), "candidateFile": candidate_path.relative_to(ROOT).as_posix(), "candidateSha256": sha256(candidate_path), "candidatePixels": list(candidate.size), "candidateAlphaBounds": list(candidate.getchannel("A").getbbox()), "candidateAlphaSha256": alpha_sha(candidate)})
    effects = []
    for filename in ("fx-stench-miasma-f40.png", "fx-slow-flies-f40.png"):
        target = PACK / "effects" / filename
        shutil.copy2(SOURCE / filename, target)
        effects.append({"filename": filename, "sourceFile": (SOURCE / filename).relative_to(ROOT).as_posix(), "sourceSha256": sha256(SOURCE / filename), "preservedFile": target.relative_to(ROOT).as_posix(), "preservedSha256": sha256(target), "frames": 40, "fps": 4, "cellPixels": [80, 80], "byteExact": True})

    font = ImageFont.load_default()
    sheet = Image.new("RGBA", (1320, 720), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), "Pedal bin family - current / candidate / geometry ghost / 64 px", fill=INK, font=font)
    for row, record in enumerate(records):
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        y = 48 + row * 330
        for col, item in enumerate((source, candidate)):
            panel = checker((390, 290))
            shown = item.resize((288, 288), Image.Resampling.LANCZOS)
            panel.alpha_composite(shown, (51, 1))
            sheet.alpha_composite(panel, (10 + col * 400, y))
        ghost = checker((390, 290))
        ghost.alpha_composite(candidate.resize((288, 288), Image.Resampling.LANCZOS), (51, 1))
        tint = Image.new("RGBA", source.size, (232, 72, 86, 0)); tint.putalpha(source.getchannel("A").point(lambda v: round(v * .36)))
        ghost.alpha_composite(tint.resize((288, 288), Image.Resampling.LANCZOS), (51, 1))
        sheet.alpha_composite(ghost, (810, y))
        sheet.alpha_composite(candidate.resize((64, 64), Image.Resampling.LANCZOS), (1225, y + 25))
        draw.text((20, y + 296), f"CURRENT {record['filename']}", fill=INK, font=font)
        draw.text((420, y + 296), f"V{VERSION} CANDIDATE", fill=INK, font=font)
        draw.text((820, y + 296), "GHOST - exact authority alpha", fill=INK, font=font)
    evidence_path = PACK / "evidence" / "bin-current-candidate-ghost-64px.png"
    sheet.save(evidence_path, optimize=True)

    manifest = {"schema": f"lighthouse-keeper/kitchen-bin-ligne-claire@{VERSION}", "set": SET, "created": "2026-10-22", "status": "immutable-review-candidate-not-approved-not-registered", "sourceApproval": APPROVAL.relative_to(ROOT).as_posix(), "sourceApprovalSha256": sha256(APPROVAL), "contractFile": CONTRACT.relative_to(ROOT).as_posix(), "contractSha256": sha256(CONTRACT), "objects": records, "effects": effects, "effectContract": {"objectAnimated": False, "environmentalEffectsSeparate": True, "frames": 40, "fps": 4, "durationSeconds": 10, "placement": [4, 104], "changed": False}, "unchanged": ["canvas", "alpha", "padding", "standard footprint", "overflow footprint", "lid orientation", "pedal", "room origin", "effect ownership", "effect frames", "effect timing", "interaction behaviour"], "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True}, "evidence": {"file": evidence_path.relative_to(ROOT).as_posix(), "sha256": sha256(evidence_path)}, "rollback": f"Discard only this V{VERSION} pack and review route."}
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n", encoding="utf-8")
    for record in records:
        shutil.copy2(ROOT / record["sourceFile"], PUBLIC / "assets" / ("current--" + record["filename"]))
        shutil.copy2(ROOT / record["candidateFile"], PUBLIC / "assets" / ("candidate--" + record["filename"]))
    for effect in effects:
        shutil.copy2(ROOT / effect["preservedFile"], PUBLIC / "assets" / effect["filename"])
    shutil.copy2(evidence_path, PUBLIC / "assets" / evidence_path.name)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bin Ligne-Claire V{VERSION}</title><style>body{{margin:0;background:#f6e5b7;color:#051824;font:16px/1.45 system-ui}}header,main{{max-width:1320px;margin:auto;padding:22px}}header{{border-bottom:4px solid #051824}}.status{{display:inline-block;border:2px solid #051824;background:#e7a638;padding:6px 10px;font-weight:800}}article{{background:#fff9e8;border:2px solid #051824;margin:18px 0;padding:14px}}img{{display:block;width:100%;height:auto;image-rendering:auto}}canvas{{width:320px;height:320px;background:#eee6cf}}</style></head><body><header><span class="status">IMMUTABLE CANDIDATE - NOT CURRENT</span><h1>Pedal bin Ligne-Claire V{VERSION}</h1><p>Static object redraw only. Approved V31 miasma and fly loops remain byte-identical, separate, 40 frames at 4 fps.</p></header><main><article><img src="/keeper-review/{SET}/assets/{evidence_path.name}"></article><article><h2>Broken candidate with unchanged animated overlays</h2><canvas id="preview" width="80" height="80"></canvas></article></main><script>const base='/keeper-review/{SET}/assets/',files=['candidate--bin-broken-overflowing.png','fx-stench-miasma-f40.png','fx-slow-flies-f40.png'],images={{}},canvas=document.getElementById('preview'),ctx=canvas.getContext('2d');Promise.all(files.map(name=>new Promise((ok,no)=>{{const i=new Image;i.onload=async()=>{{try{{await i.decode()}}catch{{}}images[name]=i;ok()}};i.onerror=no;i.src=base+name}}))).then(()=>{{const start=performance.now();function frame(t){{const n=Math.floor((t-start)/250)%40;ctx.clearRect(0,0,80,80);ctx.drawImage(images[files[0]],0,8);ctx.drawImage(images[files[1]],n*80,0,80,80,0,0,80,80);ctx.drawImage(images[files[2]],n*80,0,80,80,0,0,80,80);requestAnimationFrame(frame)}}requestAnimationFrame(frame)}})</script></body></html>'''
    (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    for record in manifest["objects"]:
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        if source.size != (72, 72) or source.size != candidate.size or alpha_sha(source) != alpha_sha(candidate) or source.getchannel("A").getbbox() != candidate.getchannel("A").getbbox():
            raise RuntimeError(f"bin geometry drift: {record['filename']}")
    for effect in manifest["effects"]:
        if sha256(ROOT / effect["sourceFile"]) != sha256(ROOT / effect["preservedFile"]):
            raise RuntimeError(f"effect changed: {effect['filename']}")
    if manifest["registration"]["register"] or manifest["registration"]["promote"]:
        raise RuntimeError("registration gate opened")
    html = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in html or "image-rendering:auto" not in html:
        raise RuntimeError("review delivery regression")
    print(f"Verified bin V{VERSION}: both 72x72 alphas exact; approved 40-frame effects byte-identical")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--verify", action="store_true"); args = parser.parse_args()
    verify() if args.verify else build()
