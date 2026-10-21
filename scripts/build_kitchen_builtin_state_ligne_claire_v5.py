#!/usr/bin/env python3
"""Build the source-locked base-master gate for Kitchen Ligne-Claire V5.

The V5 gate authors oven On and dishwasher On at 8x source resolution, then
registers each master once to the exact authority canvas and alpha channel.
It is deliberately limited to the two base drawings: state propagation is
blocked until these masters receive explicit visual approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-built-in-state-ligne-claire-v5"
DATED = "kitchen-built-in-state-ligne-claire-2026-10-21-v5"
PACK = ROOT / "art" / "drafts" / DATED
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
SOURCE_ROOT = ROOT / "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41"
DENSITY = 8

INK = "#051824"
INK_2 = "#0a222b"
CREAM = "#faf4e0"
CREAM_2 = "#f6e5b7"
METAL = "#d9ded3"
METAL_2 = "#aebbb9"
CHARCOAL = "#5c6c6f"
BLUE = "#235b85"
BLUE_2 = "#2d779d"
BLUE_DARK = "#1d4562"
SEA = "#53b1b5"
SEA_2 = "#6dc9c2"
COPPER = "#d36f2d"
COPPER_2 = "#b56636"
GOLD = "#e7a638"
RED = "#e84833"
GREEN = "#51aa60"
AQUA = "#32d2ce"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def p(value: float) -> int:
    return round(value * DENSITY)


def b(x0: float, y0: float, x1: float, y1: float) -> tuple[int, int, int, int]:
    return (p(x0), p(y0), p(x1), p(y1))


def points(values: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(p(x), p(y)) for x, y in values]


def line(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], fill: str = INK, width: float = 0.72) -> None:
    draw.line(points(values), fill=fill, width=max(1, p(width)), joint="curve")


def oven_master() -> Image.Image:
    image = Image.new("RGBA", (92 * DENSITY, 85 * DENSITY), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    outer = p(0.92)
    inner = p(0.68)

    # Cream body and shallow blue hob: the source silhouette and straight-on
    # projection remain authoritative.
    draw.rounded_rectangle(b(6.2, 18.5, 85.1, 78.3), radius=p(2.0), fill=CREAM, outline=INK, width=outer)
    draw.rounded_rectangle(b(4.7, 4.7, 87.3, 23.0), radius=p(3.4), fill=BLUE, outline=INK, width=outer)
    draw.polygon(points([(5.3, 16.0), (86.7, 16.0), (85.4, 22.4), (6.5, 22.4)]), fill=BLUE_DARK)
    line(draw, [(7.0, 16.2), (85.4, 16.2)], BLUE_2, 0.55)
    line(draw, [(6.5, 22.5), (85.4, 22.5)], INK, 0.76)

    # Two exact cooking plates and the small stacked rear-right control.
    for left, right in ((16.0, 36.5), (47.0, 68.0)):
        draw.ellipse(b(left, 7.0, right, 15.5), fill=INK)
        draw.ellipse(b(left + 1.0, 7.5, right - 1.0, 13.7), fill=CHARCOAL)
    draw.rounded_rectangle(b(73.4, 9.0, 82.1, 18.0), radius=p(1.9), fill=COPPER, outline=INK, width=inner)
    draw.rounded_rectangle(b(74.3, 2.5, 81.4, 11.0), radius=p(1.7), fill=COPPER, outline=INK, width=inner)
    line(draw, [(75.0, 9.5), (80.8, 9.5)], GOLD, 0.50)

    # Fascia, knobs and warning lamp retain source centres and hierarchy.
    draw.rectangle(b(7.3, 22.2, 84.0, 39.5), fill=CREAM_2, outline=INK, width=inner)
    for cx in (24.0, 45.0, 65.0):
        draw.ellipse(b(cx - 4.2, 25.5, cx + 4.2, 34.0), fill=COPPER, outline=INK, width=inner)
        line(draw, [(cx, 27.0), (cx, 32.3)], COPPER_2, 0.58)
    draw.ellipse(b(72.5, 26.0, 78.5, 32.4), fill=INK)
    draw.ellipse(b(73.8, 27.2, 77.2, 31.0), fill=RED)

    # Handle and cavity are simple construction, not bevelled decoration.
    draw.ellipse(b(15.5, 38.7, 23.2, 46.4), fill=COPPER, outline=INK, width=inner)
    draw.ellipse(b(69.0, 38.7, 76.7, 46.4), fill=COPPER, outline=INK, width=inner)
    draw.rounded_rectangle(b(19.0, 40.0, 73.2, 45.0), radius=p(1.8), fill=COPPER, outline=INK, width=inner)
    line(draw, [(20.7, 40.9), (71.6, 40.9)], GOLD, 0.52)

    draw.rounded_rectangle(b(18.0, 46.2, 76.0, 72.0), radius=p(2.0), fill=INK, outline=INK, width=inner)
    draw.rounded_rectangle(b(21.0, 49.0, 73.0, 68.8), radius=p(0.9), fill=COPPER_2, outline=INK_2, width=inner)
    draw.rectangle(b(22.0, 63.7, 72.0, 68.0), fill=BLUE_DARK)
    line(draw, [(23.0, 64.0), (70.7, 64.0)], GOLD, 0.48)

    # Source tray and food remain recognisable, centred and at the same depth.
    draw.rounded_rectangle(b(27.5, 57.1, 67.0, 65.0), radius=p(2.0), fill=CREAM_2, outline=INK, width=inner)
    draw.polygon(points([(31.0, 58.0), (34.5, 54.6), (58.8, 54.1), (63.7, 58.1), (62.5, 60.5), (32.0, 60.5)]), fill=COPPER, outline=INK)
    line(draw, [(37.0, 56.0), (42.0, 55.3), (48.5, 55.7), (55.3, 55.0)], GOLD, 0.45)

    # Quiet side construction and the existing blue floor plinth.
    line(draw, [(9.0, 24.0), (9.0, 75.0)], METAL_2, 0.48)
    line(draw, [(82.0, 24.0), (82.0, 75.0)], METAL_2, 0.48)
    draw.rounded_rectangle(b(6.5, 74.5, 85.0, 83.4), radius=p(1.4), fill=BLUE, outline=INK, width=outer)
    draw.rectangle(b(9.0, 77.0, 82.7, 81.8), fill=BLUE_DARK)
    line(draw, [(8.0, 76.0), (84.0, 76.0)], BLUE_2, 0.48)
    return image


def dishwasher_master() -> Image.Image:
    image = Image.new("RGBA", (98 * DENSITY, 82 * DENSITY), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    outer = p(0.92)
    inner = p(0.68)

    # Source carcass, fascia, door and base remain distinct construction planes.
    draw.rounded_rectangle(b(8.0, 18.0, 18.0, 79.5), radius=p(1.5), fill=BLUE, outline=INK, width=outer)
    draw.rounded_rectangle(b(80.0, 18.0, 90.0, 79.5), radius=p(1.5), fill=BLUE, outline=INK, width=outer)
    draw.rectangle(b(11.0, 21.0, 15.0, 72.0), fill=BLUE_DARK)
    draw.rectangle(b(83.0, 21.0, 87.0, 72.0), fill=BLUE_DARK)
    draw.rounded_rectangle(b(15.0, 20.5, 83.0, 34.0), radius=p(1.1), fill=CREAM, outline=INK, width=inner)
    draw.rounded_rectangle(b(15.0, 33.0, 83.0, 74.0), radius=p(1.1), fill=METAL, outline=INK, width=inner)
    line(draw, [(18.0, 35.7), (18.0, 70.5)], CREAM, 0.46)
    line(draw, [(80.0, 35.7), (80.0, 70.5)], CHARCOAL, 0.46)

    # Recessed three-cell display, round selector and green On lamp retain the
    # authority's layout. The cream fascia remains continuous around them.
    display = [(27.0, 22.0), (49.5, 22.0), (49.5, 31.2), (23.2, 31.2), (23.2, 29.2), (20.8, 29.2), (20.8, 24.0), (27.0, 24.0)]
    draw.polygon(points(display), fill=INK)
    for left in (28.8, 35.8, 42.8):
        draw.rounded_rectangle(b(left, 24.1, left + 4.7, 29.2), radius=p(0.35), fill=AQUA)
    draw.ellipse(b(69.1, 22.7, 77.1, 30.8), fill=INK)
    draw.ellipse(b(71.0, 24.5, 75.3, 28.9), fill=CHARCOAL)
    draw.ellipse(b(78.8, 22.4, 84.0, 27.8), fill=GREEN, outline=CREAM, width=p(0.45))

    # Compact copper handle at the exact source height and span.
    draw.ellipse(b(28.0, 37.6, 35.4, 45.2), fill=COPPER, outline=INK, width=inner)
    draw.ellipse(b(63.1, 37.6, 70.5, 45.2), fill=COPPER, outline=INK, width=inner)
    draw.rounded_rectangle(b(31.3, 39.1, 67.2, 43.9), radius=p(1.7), fill=COPPER, outline=INK, width=inner)
    line(draw, [(33.0, 40.1), (65.5, 40.1)], GOLD, 0.48)

    # Shared shallow worktop. The secondary stroke describes its front plane;
    # it is not a glossy highlight.
    draw.rounded_rectangle(b(6.5, 7.3, 91.5, 22.0), radius=p(4.0), fill=SEA, outline=INK, width=outer)
    line(draw, [(10.0, 11.0), (88.0, 11.0)], SEA_2, 0.58)
    line(draw, [(8.2, 19.7), (89.8, 19.7)], INK_2, 0.65)

    draw.rounded_rectangle(b(10.0, 71.2, 88.0, 79.5), radius=p(1.2), fill=BLUE, outline=INK, width=outer)
    draw.rectangle(b(17.0, 74.0, 81.0, 78.0), fill=BLUE_DARK)
    draw.rounded_rectangle(b(8.5, 72.0, 17.0, 81.0), radius=p(1.3), fill=BLUE, outline=INK, width=outer)
    draw.rounded_rectangle(b(81.0, 72.0, 89.5, 81.0), radius=p(1.3), fill=BLUE, outline=INK, width=outer)
    return image


def register(master: Image.Image, source: Image.Image) -> Image.Image:
    candidate = master.resize(source.size, Image.Resampling.LANCZOS)
    candidate.putalpha(source.getchannel("A"))
    return candidate


def checker(size: tuple[int, int], cell: int = 24) -> Image.Image:
    image = Image.new("RGBA", size, (242, 235, 214, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(225, 215, 190, 255))
    return image


def evidence_sheet(records: list[dict[str, object]]) -> Path:
    width, row_h, header = 1660, 760, 76
    sheet = Image.new("RGBA", (width, header + row_h * len(records)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((20, 16), "Kitchen Built-In State Ligne-Claire V5 · base-master gate", fill=INK, font=font)
    draw.text((20, 38), "Actual 8x authored masters at inspection scale; exact-alpha registered candidates at native scale; no state propagation", fill=INK, font=font)
    for index, record in enumerate(records):
        y = header + index * row_h
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        master = Image.open(ROOT / str(record["masterFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        current_panel = checker((810, 680))
        enlarged = source.resize((source.width * 6, source.height * 6), Image.Resampling.LANCZOS)
        current_panel.alpha_composite(enlarged, ((810 - enlarged.width) // 2, (680 - enlarged.height) // 2))
        master_panel = checker((810, 680))
        master_panel.alpha_composite(master, ((810 - master.width) // 2, (680 - master.height) // 2))
        sheet.alpha_composite(current_panel, (10, y))
        sheet.alpha_composite(master_panel, (840, y))
        draw.text((22, y + 687), f"CURRENT AUTHORITY · {record['filename']} · enlarged only for structure", fill=INK, font=font)
        draw.text((852, y + 687), f"V5 ACTUAL 8x MASTER · {str(record['masterSha256'])[:12]}", fill=INK, font=font)
        native_y = y + 714
        sheet.alpha_composite(source, (24, native_y))
        sheet.alpha_composite(candidate, (150, native_y))
        draw.text((280, native_y + 20), f"native 1x current / candidate · exact {record['pixels'][0]} x {record['pixels'][1]} canvas and alpha", fill=INK, font=font)
    output = EVIDENCE / "base-masters-current-vs-v5.png"
    sheet.save(output, optimize=True)
    return output


def build() -> None:
    if PACK.exists():
        raise RuntimeError(f"refusing to overwrite existing V5 draft: {PACK}")
    MASTERS.mkdir(parents=True)
    (CANDIDATES / "oven").mkdir(parents=True)
    (CANDIDATES / "dishwasher").mkdir(parents=True)
    EVIDENCE.mkdir(parents=True)

    specs = (
        ("oven", "oven-on.png", oven_master),
        ("dishwasher", "dishwasher-on.png", dishwasher_master),
    )
    records: list[dict[str, object]] = []
    for family, filename, renderer in specs:
        source_path = SOURCE_ROOT / filename
        source = Image.open(source_path).convert("RGBA")
        master = renderer()
        candidate = register(master, source)
        master_path = MASTERS / f"{family}-on-master-8x.png"
        candidate_path = CANDIDATES / family / filename
        master.save(master_path, optimize=True)
        candidate.save(candidate_path, optimize=True)
        records.append({
            "family": family,
            "filename": filename,
            "sourceFile": source_path.relative_to(ROOT).as_posix(),
            "sourceSha256": sha256(source_path),
            "masterFile": master_path.relative_to(ROOT).as_posix(),
            "masterSha256": sha256(master_path),
            "candidateFile": candidate_path.relative_to(ROOT).as_posix(),
            "candidateSha256": sha256(candidate_path),
            "pixels": list(source.size),
            "masterPixels": list(master.size),
            "alphaSha256": alpha_sha(source),
            "alphaExact": alpha_sha(candidate) == alpha_sha(source),
        })

    evidence = evidence_sheet(records)
    manifest = {
        "schema": "lighthouse-keeper/kitchen-built-in-state-ligne-claire@5-base-gate",
        "set": SET,
        "created": "2026-10-21",
        "status": "reversible-base-master-gate-not-approved-not-registered",
        "supersedesForReview": "rejected kitchen-built-in-state-ligne-claire-v4",
        "scope": ["oven On base master", "dishwasher On base master"],
        "blockedUntilExplicitApproval": ["Broken states", "lit states", "40-frame oven strips", "dishwasher edge variants", "room proof", "registration"],
        "method": "genuinely authored 8x source-locked masters; one Lanczos registration to exact source canvas; exact source alpha reapplied",
        "assets": records,
        "evidence": {"file": evidence.relative_to(ROOT).as_posix(), "sha256": sha256(evidence)},
        "checks": {
            "sourceUntouched": True,
            "productionUntouched": True,
            "runtimeUntouched": True,
            "healingUntouched": True,
            "registrationPerformed": False,
        },
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({
        "set": SET,
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
    }, indent=2) + "\n")
    hashes = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}\n" for path in hashes))
    verify()


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    if manifest["status"] != "reversible-base-master-gate-not-approved-not-registered":
        raise RuntimeError("V5 approval boundary drift")
    if manifest["checks"]["registrationPerformed"]:
        raise RuntimeError("V5 registration unexpectedly open")
    for record in manifest["assets"]:
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        master = Image.open(ROOT / record["masterFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        if source.size != candidate.size or master.size != (source.width * DENSITY, source.height * DENSITY):
            raise RuntimeError(f"canvas drift: {record['filename']}")
        if source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"alpha drift: {record['filename']}")
        for key in ("sourceFile", "masterFile", "candidateFile"):
            hash_key = key.replace("File", "Sha256")
            if sha256(ROOT / record[key]) != record[hash_key]:
                raise RuntimeError(f"hash drift: {record['filename']} {key}")
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["register"] or register["promote"] or register["currentSelectorChanges"]:
        raise RuntimeError("V5 registration guard open")
    for row in (PACK / "HASHES.sha256").read_text().splitlines():
        expected, relative = row.split("  ", 1)
        if sha256(PACK / relative) != expected:
            raise RuntimeError(f"pack checksum drift: {relative}")
    print("Verified V5 base gate: two authored 8x masters, exact native canvases/alpha, registration closed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
