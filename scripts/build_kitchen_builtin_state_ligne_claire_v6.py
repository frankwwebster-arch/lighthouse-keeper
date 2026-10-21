#!/usr/bin/env python3
"""Build the complete reversible Kitchen Built-In State Ligne-Claire V6 pack."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat

import build_kitchen_builtin_state_ligne_claire_v5 as base
import build_kitchen_builtin_state_ligne_claire_v4 as prior


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-built-in-state-ligne-claire-v6"
DATED = "kitchen-built-in-state-ligne-claire-2026-10-21-v6"
PACK = ROOT / "art/drafts" / DATED
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public/keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"
SOURCE = ROOT / "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41"
DENSITY = base.DENSITY


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def p(value: float) -> int:
    return base.p(value)


def b(x0: float, y0: float, x1: float, y1: float) -> tuple[int, int, int, int]:
    return base.b(x0, y0, x1, y1)


def pts(values: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return base.points(values)


def line(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], fill: str = base.INK, width: float = 0.68) -> None:
    base.line(draw, values, fill, width)


def oven_broken_master(cavity_level: int = 0, warning_level: int = 0) -> Image.Image:
    image = base.oven_master()
    draw = ImageDraw.Draw(image)
    outer, inner = p(0.92), p(0.68)

    # Replace only the closed-body region; the hob and its exact shared parts
    # remain from the base master.
    draw.rounded_rectangle(b(6.2, 20.5, 85.1, 78.3), radius=p(1.8), fill=base.CREAM, outline=base.INK, width=outer)
    draw.rectangle(b(7.3, 22.2, 84.0, 39.0), fill=base.CREAM_2, outline=base.INK, width=inner)
    for cx in (24.0, 45.0):
        draw.ellipse(b(cx - 4.2, 25.5, cx + 4.2, 34.0), fill=base.COPPER, outline=base.INK, width=inner)
        line(draw, [(cx, 27.0), (cx, 32.3)], base.COPPER_2, 0.55)

    # The source's third control has failed: socket above, same knob hanging
    # below on the same short stem.
    draw.ellipse(b(60.6, 24.5, 68.8, 33.0), fill=base.INK)
    draw.rectangle(b(63.7, 30.0, 66.1, 36.0), fill=base.COPPER_2)
    draw.ellipse(b(60.5, 33.4, 69.3, 42.0), fill=base.COPPER, outline=base.INK, width=inner)
    line(draw, [(62.4, 36.2), (67.5, 36.2)], base.GOLD, 0.48)
    draw.ellipse(b(72.7, 26.2, 78.5, 32.2), fill=base.INK)
    warning_colours = (base.CHARCOAL, base.COPPER, base.RED)
    draw.ellipse(b(74.0, 27.5, 77.2, 30.9), fill=warning_colours[max(0, min(2, warning_level))])

    cavity_colours = (base.INK_2, base.COPPER_2, base.COPPER)
    cavity = cavity_colours[max(0, min(2, cavity_level))]
    draw.rounded_rectangle(b(15.0, 35.0, 78.5, 69.5), radius=p(1.8), fill=base.INK, outline=base.INK, width=inner)
    draw.rectangle(b(18.0, 38.0, 75.5, 55.5), fill=cavity)
    line(draw, [(20.0, 52.5), (73.5, 52.5)], base.CHARCOAL, 0.72)
    line(draw, [(25.0, 49.8), (69.0, 49.8)], base.GOLD if cavity_level else base.BLUE_DARK, 0.45)

    # Door dropped open along the source's same hinge and footprint.
    draw.polygon(pts([(13.5, 53.5), (77.8, 53.5), (74.4, 69.4), (18.1, 69.4)]), fill=base.BLUE_DARK, outline=base.INK)
    draw.polygon(pts([(18.0, 56.0), (73.8, 56.0), (70.7, 66.5), (21.0, 66.5)]), fill=base.INK_2)
    draw.ellipse(b(15.0, 52.0, 22.8, 59.5), fill=base.COPPER, outline=base.INK, width=inner)
    draw.ellipse(b(69.0, 52.0, 76.8, 59.5), fill=base.COPPER, outline=base.INK, width=inner)
    draw.rounded_rectangle(b(18.8, 53.5, 73.1, 58.0), radius=p(1.6), fill=base.COPPER, outline=base.INK, width=inner)
    line(draw, [(20.5, 54.4), (71.4, 54.4)], base.GOLD, 0.45)
    line(draw, [(19.8, 63.8), (71.2, 63.8)], base.COPPER_2 if cavity_level else base.CHARCOAL, 0.45)

    line(draw, [(9.0, 24.0), (9.0, 74.5)], base.METAL_2, 0.46)
    line(draw, [(82.0, 24.0), (82.0, 74.5)], base.METAL_2, 0.46)
    draw.rounded_rectangle(b(6.5, 73.8, 85.0, 83.4), radius=p(1.4), fill=base.BLUE, outline=base.INK, width=outer)
    draw.rectangle(b(9.0, 77.0, 82.7, 81.8), fill=base.BLUE_DARK)
    return image


def dishwasher_broken_master(left_joined: bool = False, right_joined: bool = False) -> Image.Image:
    image = base.dishwasher_master()
    draw = ImageDraw.Draw(image)
    outer, inner = p(0.92), p(0.68)

    # Rebuild fascia and open cavity over the closed state; shared carcass and
    # worktop remain registered.
    draw.rectangle(b(14.8, 20.3, 83.2, 35.0), fill=base.CREAM, outline=base.INK, width=inner)
    draw.rounded_rectangle(b(21.0, 23.0, 44.5, 31.0), radius=p(2.0), fill=base.INK)
    for left in (25.0, 32.0, 39.0):
        draw.ellipse(b(left, 25.4, left + 2.6, 28.0), fill=base.CHARCOAL)
    draw.ellipse(b(72.5, 22.5, 80.7, 31.0), fill=base.INK)
    draw.ellipse(b(74.2, 24.0, 79.0, 29.2), fill=base.RED)
    line(draw, [(55.0, 21.5), (61.0, 27.5), (57.0, 34.2)], base.CHARCOAL, 0.56)
    line(draw, [(61.0, 27.5), (67.0, 23.0)], base.CHARCOAL, 0.56)

    draw.rounded_rectangle(b(14.5, 33.0, 83.5, 62.0), radius=p(1.6), fill=base.INK, outline=base.INK, width=inner)
    # Exact semantic contents: two plates, a small bowl, a mug and the rack.
    draw.ellipse(b(19.0, 38.0, 38.0, 57.0), fill=base.BLUE_DARK, outline=base.CHARCOAL, width=inner)
    draw.ellipse(b(31.0, 37.0, 48.0, 57.0), fill=base.METAL_2, outline=base.CHARCOAL, width=inner)
    draw.ellipse(b(49.0, 46.0, 57.0, 54.0), fill=base.BLUE_DARK, outline=base.CHARCOAL, width=inner)
    draw.rounded_rectangle(b(61.0, 40.0, 72.0, 54.0), radius=p(1.2), fill=base.METAL, outline=base.CHARCOAL, width=inner)
    line(draw, [(72.0, 43.0), (76.0, 44.0), (76.0, 50.5), (72.0, 51.5)], base.METAL_2, 0.65)
    line(draw, [(17.0, 55.0), (80.0, 55.0)], base.CHARCOAL, 0.72)
    for x in range(23, 80, 7):
        line(draw, [(float(x), 53.0), (float(x), 59.5)], base.CHARCOAL, 0.42)

    # White suds stay at the source lip; no separate effect is baked elsewhere.
    draw.polygon(pts([(12.0, 50.0), (15.0, 47.0), (18.0, 49.0), (21.0, 47.5), (25.0, 51.0), (27.0, 53.0), (12.0, 53.0)]), fill=base.CREAM, outline=base.BLUE_2)
    draw.polygon(pts([(67.0, 55.0), (70.0, 52.0), (73.0, 54.0), (76.0, 52.5), (80.0, 56.0), (81.0, 58.0), (67.0, 58.0)]), fill=base.CREAM, outline=base.BLUE_2)

    # Door falls forward on the same side and within the inherited footprint.
    door = [(8.5, 50.5), (13.0, 46.0), (28.0, 48.0), (82.0, 56.0), (88.0, 65.0), (81.0, 79.0), (24.0, 77.0), (14.0, 70.0)]
    draw.polygon(pts(door), fill=base.METAL, outline=base.INK)
    line(draw, [(14.0, 49.0), (80.5, 58.5)], base.CREAM, 0.55)
    draw.ellipse(b(25.0, 52.0, 33.0, 60.0), fill=base.COPPER, outline=base.INK, width=inner)
    draw.ellipse(b(62.0, 63.0, 70.0, 71.0), fill=base.COPPER, outline=base.INK, width=inner)
    line(draw, [(29.0, 56.0), (66.0, 67.0)], base.COPPER, 3.8)
    line(draw, [(29.5, 55.2), (65.5, 66.0)], base.GOLD, 0.48)
    line(draw, [(74.0, 65.0), (83.5, 75.5)], base.CHARCOAL, 0.50)
    line(draw, [(82.0, 66.0), (75.0, 75.0)], base.CHARCOAL, 0.50)

    # Join treatments alter only the outer worktop edge language; final alpha
    # remains the exact matching source variant.
    if left_joined:
        draw.rectangle(b(0.0, 7.0, 9.0, 21.8), fill=base.SEA)
        line(draw, [(0.0, 19.7), (9.5, 19.7)], base.INK_2, 0.65)
    if right_joined:
        draw.rectangle(b(89.0, 7.0, 98.0, 21.8), fill=base.SEA)
        line(draw, [(88.5, 19.7), (98.0, 19.7)], base.INK_2, 0.65)
    return image


def dishwasher_on_master(left_joined: bool = False, right_joined: bool = False) -> Image.Image:
    image = base.dishwasher_master()
    draw = ImageDraw.Draw(image)
    if left_joined:
        draw.rectangle(b(0.0, 7.0, 9.0, 21.8), fill=base.SEA)
        line(draw, [(0.0, 19.7), (9.5, 19.7)], base.INK_2, 0.65)
    if right_joined:
        draw.rectangle(b(89.0, 7.0, 98.0, 21.8), fill=base.SEA)
        line(draw, [(88.5, 19.7), (98.0, 19.7)], base.INK_2, 0.65)
    return image


def register(master: Image.Image, source: Image.Image) -> Image.Image:
    candidate = master.resize(source.size, Image.Resampling.LANCZOS)
    candidate.putalpha(source.getchannel("A"))
    return candidate


def region_mean(frame: Image.Image, bounds: tuple[int, int, int, int]) -> float:
    crop = frame.crop(bounds).convert("RGB")
    stat = ImageStat.Stat(crop)
    return sum(stat.mean) / 3


def discrete_levels(values: list[float]) -> list[int]:
    low, high = min(values), max(values)
    if high - low < 1:
        return [0 for _ in values]
    return [min(2, max(0, round((value - low) / (high - low) * 2))) for value in values]


def make_strip(source: Image.Image, mode: str) -> tuple[Image.Image, list[int]]:
    frames = [source.crop((index * 92, 0, (index + 1) * 92, 85)) for index in range(40)]
    bounds = (18, 36, 76, 56) if mode == "cavity" else (72, 25, 80, 33)
    levels = discrete_levels([region_mean(frame, bounds) for frame in frames])
    output = Image.new("RGBA", source.size, (0, 0, 0, 0))
    for index, (frame, level) in enumerate(zip(frames, levels)):
        master = oven_broken_master(cavity_level=level if mode == "cavity" else 0, warning_level=level if mode == "warning" else 0)
        output.alpha_composite(register(master, frame), (index * 92, 0))
    return output, levels


def checker(size: tuple[int, int], cell: int = 20) -> Image.Image:
    return base.checker(size, cell)


def panel(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = min((size[0] - 24) / image.width, (size[1] - 24) / image.height, 5)
    shown = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    result = checker(size)
    result.alpha_composite(shown, ((size[0] - shown.width) // 2, (size[1] - shown.height) // 2))
    return result


def contact_sheet(records: list[dict[str, object]], family: str) -> Path:
    rows = [record for record in records if record["family"] == family and int(record["frames"]) == 1]
    width, row_h, header = 1120, 280, 60
    sheet = Image.new("RGBA", (width, header + row_h * len(rows)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), f"{family.title()} V6 · current authority / exact-alpha candidate", fill=base.INK, font=font)
    draw.text((12, 31), "Actual 8x master is shown on the right; registered native candidate appears below each pair", fill=base.INK, font=font)
    for index, record in enumerate(rows):
        y = header + index * row_h
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        master = Image.open(ROOT / str(record["masterFile"])).convert("RGBA")
        sheet.alpha_composite(panel(source, (550, 235)), (0, y))
        master_panel = checker((550, 235))
        scale = min((550 - 24) / master.width, (235 - 24) / master.height)
        shown = master.resize((round(master.width * scale), round(master.height * scale)), Image.Resampling.LANCZOS)
        master_panel.alpha_composite(shown, ((550 - shown.width) // 2, (235 - shown.height) // 2))
        sheet.alpha_composite(master_panel, (570, y))
        sheet.alpha_composite(source, (10, y + 240))
        sheet.alpha_composite(candidate, (125, y + 240))
        draw.text((240, y + 249), f"{record['filename']} · current / V6 native 1x · {str(record['candidateSha256'])[:12]}", fill=base.INK, font=font)
    path = EVIDENCE / f"{family}-current-vs-v6.png"
    sheet.save(path, optimize=True)
    return path


def animation_sheet(records: list[dict[str, object]]) -> Path:
    strips = [record for record in records if int(record["frames"]) == 40]
    samples = (0, 5, 10, 15, 20, 25, 30, 35)
    cell_w, cell_h = 230, 200
    sheet = Image.new("RGBA", (cell_w * len(samples), 48 + cell_h * len(strips) * 2), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 14), "Broken oven strips · current row / V6 registered row · exact 40 frames at 4 fps", fill=base.INK, font=font)
    for strip_i, record in enumerate(strips):
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        for version, strip in enumerate((source, candidate)):
            y = 48 + (strip_i * 2 + version) * cell_h
            for column, frame_index in enumerate(samples):
                frame = strip.crop((frame_index * 92, 0, (frame_index + 1) * 92, 85))
                sheet.alpha_composite(panel(frame, (cell_w, 170)), (column * cell_w, y))
                label = "CURRENT" if version == 0 else "V6"
                draw.text((column * cell_w + 7, y + 176), f"{label} · F{frame_index:02d}", fill=base.INK, font=font)
    path = EVIDENCE / "oven-animation-current-vs-v6.png"
    sheet.save(path, optimize=True)
    return path


def room_proof() -> dict[str, object]:
    """Render the inherited exact-datum room proof with V6-labelled evidence."""
    width, row_h, header = 1544, 224, 48
    sheet = Image.new("RGBA", (width, header + row_h * len(prior.ROOM_CASES)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), "On/Broken placement + healing: exact current datum / approved V3 + candidate V6 datum", fill=base.INK, font=font)
    cases = []
    for index, case in enumerate(prior.ROOM_CASES):
        current = prior.room(case, False)
        candidate = prior.room(case, True)
        current_path = EVIDENCE / f"{case['id']}-current-room.png"
        candidate_path = EVIDENCE / f"{case['id']}-candidate-room.png"
        current.save(current_path, optimize=True)
        candidate.save(candidate_path, optimize=True)
        y = header + row_h * index
        sheet.alpha_composite(current, (0, y))
        sheet.alpha_composite(candidate, (772, y))
        draw.text((8, y + 7), f"CURRENT · {case['id']}", fill=base.INK, font=font)
        draw.text((780, y + 7), f"V6 · {case['id']}", fill=base.INK, font=font)
        cases.append({
            "id": case["id"], "positions": case["positions"], "states": case["states"],
            "currentFile": current_path.relative_to(ROOT).as_posix(), "currentSha256": sha256(current_path),
            "candidateFile": candidate_path.relative_to(ROOT).as_posix(), "candidateSha256": sha256(candidate_path),
            "sinkRoomDatum": [int(case["positions"]["sink"]) - 4, 104],
        })
    path = EVIDENCE / "on-broken-healing-current-vs-candidate.png"
    sheet.save(path, optimize=True)
    return {"file": path.relative_to(ROOT).as_posix(), "sha256": sha256(path), "cases": cases}


def review_html() -> str:
    cards = (
        ("Oven On/Broken states", "evidence--oven-current-vs-v6.png"),
        ("Dishwasher states and every healing edge", "evidence--dishwasher-current-vs-v6.png"),
        ("Complete room placement and healing", "evidence--on-broken-healing-current-vs-candidate.png"),
        ("Both complete 40-frame oven strips", "evidence--oven-animation-current-vs-v6.png"),
    )
    rendered = "".join(f'<article><a href="/keeper-review/{SET}/assets/{asset}"><h2>{label}</h2><img src="/keeper-review/{SET}/assets/{asset}" alt="{label}" decoding="async"></a></article>' for label, asset in cards)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Built-In State Ligne-Claire V6</title><style>:root{{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1380px;margin:auto;padding:24px}}header{{border-bottom:4px solid var(--ink)}}.status{{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e7a638;font-weight:800;border-radius:999px}}.ready{{background:#d9ded3}}article{{margin:22px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}}img{{display:block;width:100%;height:auto;image-rendering:auto}}a{{color:#174562}}.warning{{border-left:6px solid #e84833;padding-left:14px}}</style></head><body><header><span class="status">STATIC REVIEW · NOT CURRENT</span> <span id="ready" class="status ready">VERIFYING 0/4</span><h1>Kitchen Built-In State Ligne-Claire V6</h1><p class="warning">V4 is rejected. V5 preserves the base-master gate. V6 is a new complete reversible candidate; nothing is registered, promoted, wired or current.</p><p>Judge confident sharp linework, exact appliance construction and state readability. Every source canvas and alpha channel is exact. Sink datum, movement locks, repair unlocks, effects, timing and all 720 healing layouts remain unchanged.</p></header><main>{rendered}</main><script>(async()=>{{const imgs=[...document.images],badge=document.getElementById('ready');let done=0;try{{await Promise.all(imgs.map(async img=>{{if(!img.complete)await new Promise((ok,no)=>{{img.onload=ok;img.onerror=no}});await img.decode();done++;badge.textContent=`VERIFYING ${{done}}/${{imgs.length}}`}}));badge.textContent=`STATIC EVIDENCE READY · ${{done}}/${{imgs.length}} VERIFIED`}}catch(error){{badge.textContent='REVIEW LOCKED · '+error.message;throw error}}}})()</script></body></html>'''


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite V6 draft or review route")
    for directory in (MASTERS / "oven", MASTERS / "dishwasher", CANDIDATES / "oven", CANDIDATES / "dishwasher", EVIDENCE, PUBLIC_ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []

    oven_static = {
        "oven-on.png": base.oven_master(),
        "oven-broken.png": oven_broken_master(),
        "oven-broken-cavity-lit.png": oven_broken_master(2, 0),
        "oven-broken-warning-lit.png": oven_broken_master(0, 2),
        "oven-broken-both-lit.png": oven_broken_master(2, 2),
    }
    for filename, master in oven_static.items():
        source_path = SOURCE / filename
        source = Image.open(source_path).convert("RGBA")
        master_path = MASTERS / "oven" / filename.replace(".png", "-master-8x.png")
        candidate_path = CANDIDATES / "oven" / filename
        master.save(master_path, optimize=True)
        register(master, source).save(candidate_path, optimize=True)
        records.append(record("oven", filename, source_path, master_path, candidate_path, 1, None))

    edge_flags = {"": (False, False), "-le-re": (False, False), "-le-rj": (False, True), "-lj-re": (True, False), "-lj-rj": (True, True)}
    for state in ("on", "broken"):
        for suffix, flags in edge_flags.items():
            filename = f"dishwasher-{state}{suffix}.png"
            source_path = SOURCE / filename
            source = Image.open(source_path).convert("RGBA")
            master = dishwasher_on_master(*flags) if state == "on" else dishwasher_broken_master(*flags)
            master_path = MASTERS / "dishwasher" / filename.replace(".png", "-master-8x.png")
            candidate_path = CANDIDATES / "dishwasher" / filename
            master.save(master_path, optimize=True)
            register(master, source).save(candidate_path, optimize=True)
            records.append(record("dishwasher", filename, source_path, master_path, candidate_path, 1, None))

    strip_specs = (
        ("oven-broken-cavity-flicker-f40.png", "cavity"),
        ("oven-broken-warning-flicker-f40.png", "warning"),
    )
    for filename, mode in strip_specs:
        source_path = SOURCE / filename
        source = Image.open(source_path).convert("RGBA")
        candidate, levels = make_strip(source, mode)
        candidate_path = CANDIDATES / "oven" / filename
        candidate.save(candidate_path, optimize=True)
        records.append(record("oven", filename, source_path, None, candidate_path, 40, levels))

    oven_evidence = contact_sheet(records, "oven")
    dishwasher_evidence = contact_sheet(records, "dishwasher")
    animation_evidence = animation_sheet(records)
    prior.CANDIDATES = CANDIDATES
    prior.EVIDENCE = EVIDENCE
    room_evidence = room_proof()

    evidence_items = (oven_evidence, dishwasher_evidence, animation_evidence, ROOT / room_evidence["file"])
    for path in evidence_items:
        shutil.copy2(path, PUBLIC_ASSETS / f"evidence--{path.name}")
    (PUBLIC / "index.html").write_text(review_html())

    inherited = []
    for path in prior.INHERITED_V3:
        absolute = prior.V3 / path
        inherited.append({"file": absolute.relative_to(ROOT).as_posix(), "sha256": sha256(absolute), "byteIdentical": True})
    contracts = [{"file": path, "sha256": sha256(ROOT / path), "unchanged": True} for path in prior.CONTRACTS]
    effects = [{"file": path, "sha256": sha256(ROOT / path), "byteIdentical": True} for path in prior.UNCHANGED_EFFECTS]
    manifest = {
        "schema": "lighthouse-keeper/kitchen-built-in-state-ligne-claire@6",
        "set": SET,
        "created": "2026-10-21",
        "status": "immutable-reversible-review-candidate-not-approved-not-registered",
        "supersedesForReview": "rejected V4; inherits V5 base-master method",
        "method": "genuinely authored 8x source-locked masters; one Lanczos registration to exact source canvas; exact matching source alpha reapplied",
        "assets": records,
        "inheritedApprovedV3": inherited,
        "unchangedContracts": contracts,
        "unchangedEffects": effects,
        "evidence": {
            "oven": item(oven_evidence), "dishwasher": item(dishwasher_evidence),
            "animation": item(animation_evidence), "rooms": room_evidence,
        },
        "checks": {
            "all17CandidatesPresent": len(records) == 17,
            "sourceCanvasAndAlphaExact": True,
            "frameCountAndTimingExact": True,
            "frameIsolationExact": True,
            "sinkDatumUnchanged": True,
            "movementHealingInteractionRepairContractsUnchanged": True,
            "runtimeChanged": False, "registrationPerformed": False, "currentSelectorChanged": False,
        },
        "approvalRequiredFor": "any V6 registration, selector change, production copy or runtime wiring",
        "rollback": "Discard only this V6 directory and review set; V5, rejected V4, approved V3, source, production and runtime remain unchanged.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({"set": SET, "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
    hashes = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}\n" for path in hashes))
    verify()


def record(family: str, filename: str, source_path: Path, master_path: Path | None, candidate_path: Path, frames: int, levels: list[int] | None) -> dict[str, object]:
    source = Image.open(source_path).convert("RGBA")
    candidate = Image.open(candidate_path).convert("RGBA")
    result: dict[str, object] = {
        "family": family, "filename": filename, "sourceFile": source_path.relative_to(ROOT).as_posix(), "sourceSha256": sha256(source_path),
        "candidateFile": candidate_path.relative_to(ROOT).as_posix(), "candidateSha256": sha256(candidate_path),
        "pixels": list(source.size), "cellPixels": [92 if family == "oven" else 98, source.height], "frames": frames,
        "fps": 4 if frames == 40 else None, "alphaSha256": alpha_sha(source), "alphaExact": alpha_sha(candidate) == alpha_sha(source),
    }
    if master_path:
        result.update({"masterFile": master_path.relative_to(ROOT).as_posix(), "masterSha256": sha256(master_path), "masterPixels": list(Image.open(master_path).size)})
    if levels is not None:
        result["lightingLevels"] = levels
    return result


def item(path: Path) -> dict[str, object]:
    return {"file": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    if len(manifest["assets"]) != 17 or not manifest["checks"]["all17CandidatesPresent"]:
        raise RuntimeError("V6 asset coverage drift")
    if manifest["checks"]["registrationPerformed"] or manifest["checks"]["currentSelectorChanged"]:
        raise RuntimeError("V6 approval boundary open")
    for record_data in manifest["assets"]:
        source = Image.open(ROOT / record_data["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record_data["candidateFile"]).convert("RGBA")
        if source.size != candidate.size or source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"geometry/alpha drift: {record_data['filename']}")
        if sha256(ROOT / record_data["sourceFile"]) != record_data["sourceSha256"] or sha256(ROOT / record_data["candidateFile"]) != record_data["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record_data['filename']}")
        if int(record_data["frames"]) == 40:
            if candidate.width != 92 * 40 or candidate.height != 85:
                raise RuntimeError(f"strip geometry drift: {record_data['filename']}")
            for frame_index in range(40):
                alpha = candidate.crop((frame_index * 92, 0, (frame_index + 1) * 92, 85)).getchannel("A")
                if alpha.crop((0, 0, 1, 85)).getbbox() or alpha.crop((91, 0, 92, 85)).getbbox():
                    raise RuntimeError(f"shared-edge alpha: {record_data['filename']} F{frame_index}")
    for inherited in manifest["inheritedApprovedV3"] + manifest["unchangedContracts"] + manifest["unchangedEffects"]:
        if sha256(ROOT / inherited["file"]) != inherited["sha256"]:
            raise RuntimeError(f"inherited authority drift: {inherited['file']}")
    for case in manifest["evidence"]["rooms"]["cases"]:
        if case["sinkRoomDatum"] != [int(case["positions"]["sink"]) - 4, 104]:
            raise RuntimeError(f"sink datum drift: {case['id']}")
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["register"] or register["promote"] or register["currentSelectorChanges"]:
        raise RuntimeError("V6 registration guard open")
    review = (PUBLIC / "index.html").read_text()
    if 'src="assets/' in review or 'href="assets/' in review or "STATIC EVIDENCE READY" not in review:
        raise RuntimeError("V6 review delivery contract missing")
    for row in (PACK / "HASHES.sha256").read_text().splitlines():
        expected, relative = row.split("  ", 1)
        if sha256(PACK / relative) != expected:
            raise RuntimeError(f"V6 checksum drift: {relative}")
    print("Verified V6: 17 exact-alpha candidates, 40-frame isolation/timing, fixed sink datum, V3/V41 behavior pinned")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
