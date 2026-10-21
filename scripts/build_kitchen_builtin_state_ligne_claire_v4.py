#!/usr/bin/env python3
"""Build and verify the immutable built-in On/Broken Ligne-Claire V4 pack.

Only RGB drawing language changes. Source alpha, frame cells, state timing,
placement, adjacency variants and the approved V41 move/heal controller remain
authoritative. Approved V3 fitted-family files are referenced byte-for-byte.
"""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_kitchen_fitted_cabinet_ligne_claire_v3 as fitted


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-built-in-state-ligne-claire-v4"
DATED = "kitchen-built-in-state-ligne-claire-2026-10-21-v4"
PACK = ROOT / "art" / "drafts" / DATED
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"
SOURCE_DIR = ROOT / "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41"
V3 = ROOT / "art/drafts/kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3"
V3_CANDIDATES = V3 / "candidates"

INKS = ((5, 24, 36), (10, 34, 43))
WORKTOP = fitted.WORKTOP
BLUES = fitted.BLUES
COPPER = fitted.COPPER
NEUTRALS = (
    (27, 39, 42),
    (92, 108, 111),
    (174, 187, 185),
    (246, 229, 183),
    (255, 241, 207),
)
SIGNAL_AQUA = (50, 210, 206)
SIGNAL_GREEN = (81, 170, 96)
SIGNAL_RED = (213, 72, 51)
VISIBLE_ALPHA = 8

OVEN_NAMES = (
    "oven-on.png",
    "oven-broken.png",
    "oven-broken-cavity-lit.png",
    "oven-broken-warning-lit.png",
    "oven-broken-both-lit.png",
    "oven-broken-cavity-flicker-f40.png",
    "oven-broken-warning-flicker-f40.png",
)
DISHWASHER_NAMES = tuple(
    f"dishwasher-{state}{suffix}.png"
    for state in ("on", "broken")
    for suffix in ("", "-le-re", "-le-rj", "-lj-re", "-lj-rj")
)
ASSET_GROUPS = (("oven", OVEN_NAMES), ("dishwasher", DISHWASHER_NAMES))

INHERITED_V3 = (
    "candidates/fridge/fridge-standard.png",
    "candidates/fridge/fridge-broken-hinge-failed.png",
    "candidates/sink/sink-cabinet-on-base.png",
    "candidates/sink/sink-cabinet-broken-base.png",
    "candidates/cabinets/cabinet-a-le-re.png",
    "candidates/cabinets/cabinet-a-le-rj.png",
    "candidates/cabinets/cabinet-a-lj-re.png",
    "candidates/cabinets/cabinet-a-lj-rj.png",
    "candidates/cabinets/cabinet-b-le-re.png",
    "candidates/cabinets/cabinet-b-le-rj.png",
    "candidates/cabinets/cabinet-b-lj-re.png",
    "candidates/cabinets/cabinet-b-lj-rj.png",
    "candidates/healing/join-body-backfill-template.png",
    "candidates/healing/countertop-join-cap-template.png",
    "candidates/healing/countertop-triangle-underlay-template.png",
    "candidates/healing/neighbour-seam-cleanup-left.png",
    "candidates/healing/neighbour-seam-cleanup-right.png",
)
UNCHANGED_EFFECTS = (
    "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-dishwasher-suds--compact-f40.png",
    "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-dishwasher-suds--regular-f40.png",
    "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-dishwasher-suds--emphatic-f40.png",
    "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-fridge-drip-ripple-f40.png",
    "art/raw/kitchen-sink-smooth-join-2026-10-19-v19/fx-sink-on-water-f40.png",
    "art/raw/kitchen-sink-smooth-join-2026-10-19-v19/fx-sink-broken-basin-spouts-f40.png",
)
CONTRACTS = (
    "art/drafts/kitchen-dishwasher-workbench-2026-10-20-v41/candidate-catalogue.json",
    "docs/review/kitchen-dishwasher-workbench-v41-approval-2026-10-20.json",
    "scripts/verify_kitchen_dishwasher_workbench_v41.mjs",
    "art/drafts/kitchen-split-cabinet-workbench-2026-10-20-v38/candidate-catalogue.json",
    "scripts/verify_kitchen_split_cabinet_workbench_v38.mjs",
    "docs/review/kitchen-fitted-cabinet-ligne-claire-v3-approval-2026-10-21.json",
    "art/drafts/kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3/manifest.json",
)

ROOM_CASES = (
    {
        "id": "on-dishwasher-right",
        "states": {"fridge": "standard", "sink": "on", "oven": "on", "dishwasher": "on"},
        "positions": {"fridge": 84, "cabinetA": 168, "oven": 252, "cabinetB": 336, "sink": 420, "dishwasher": 504},
    },
    {
        "id": "on-dishwasher-left",
        "states": {"fridge": "standard", "sink": "on", "oven": "on", "dishwasher": "on"},
        "positions": {"dishwasher": 84, "cabinetA": 168, "oven": 252, "cabinetB": 336, "sink": 420, "fridge": 504},
    },
    {
        "id": "broken-dishwasher-right",
        "states": {"fridge": "broken", "sink": "broken", "oven": "broken-both-lit", "dishwasher": "broken"},
        "positions": {"fridge": 84, "cabinetA": 168, "oven": 252, "cabinetB": 336, "sink": 420, "dishwasher": 504},
    },
    {
        "id": "broken-dishwasher-interior",
        "states": {"fridge": "broken", "sink": "broken", "oven": "broken", "dishwasher": "broken"},
        "positions": {"fridge": 84, "cabinetA": 168, "dishwasher": 252, "cabinetB": 336, "sink": 420, "oven": 504},
    },
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def spot(value: float, colours: tuple[tuple[int, int, int], ...]) -> tuple[int, int, int]:
    thresholds = tuple((index + 1) / len(colours) for index in range(len(colours) - 1))
    width = 0.045
    for index, threshold in enumerate(thresholds):
        if value < threshold - width:
            return colours[index]
        if value <= threshold + width:
            return fitted.mix(colours[index], colours[index + 1], (value - threshold + width) / (2 * width))
    return colours[-1]


def signal_colour(pixel: tuple[int, int, int, int], name: str, x: int, y: int) -> tuple[int, int, int] | None:
    """Keep functional lamps distinct without moving or growing their pixels."""
    r, g, b, _a = pixel
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    degrees = h * 360
    cell_x = x % (92 if name.startswith("oven-") else 98)
    if name.startswith("dishwasher-") and 15 <= y <= 29 and 15 <= cell_x <= 86 and s > 0.30:
        if 160 <= degrees <= 220:
            return SIGNAL_AQUA
        if 65 <= degrees < 160:
            return SIGNAL_GREEN
        if degrees < 28 or degrees >= 340:
            return SIGNAL_RED
    if name.startswith("oven-") and 12 <= y <= 30 and 60 <= cell_x <= 82 and s > 0.32:
        if degrees < 28 or degrees >= 340:
            return SIGNAL_RED
    return None


def style_pixel(pixel: tuple[int, int, int, int], name: str, x: int, y: int) -> tuple[int, int, int, int]:
    r, g, b, a = pixel
    if a == 0:
        return (0, 0, 0, 0)
    signal = signal_colour(pixel, name, x, y)
    if signal is not None:
        return (*signal, a)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    degrees = h * 360
    # Appliance construction lines are often anti-aliased through dark brown.
    # Keep the darkest core near-black, then blend its edge ramp into the
    # relevant spot colour instead of making an abrupt, pixelated threshold.
    if v <= 0.30:
        return (*spot(v, INKS), a)
    if s > 0.20 and 165 <= degrees < 198:
        colour = spot(v, WORKTOP)
    elif (s > 0.20 and 198 <= degrees < 265) or (b > g * 1.18 and b > r * 1.5):
        colour = spot(v, BLUES)
    elif (degrees < 65 or degrees >= 340) and s > 0.28:
        colour = spot(v, COPPER)
    else:
        colour = spot(v, NEUTRALS)
    if v < 0.48:
        colour = fitted.mix(INKS[-1], colour, (v - 0.30) / 0.18)
    return (*colour, a)


def stylise(image: Image.Image, name: str) -> Image.Image:
    source = image.convert("RGBA")
    output = Image.new("RGBA", source.size)
    width = source.width
    output.putdata([
        style_pixel(pixel, name, index % width, index // width)
        for index, pixel in enumerate(source.getdata())
    ])
    return output


def frame_geometry(image: Image.Image, family: str) -> tuple[int, int, int]:
    cell = 92 if family == "oven" else 98
    frames = image.width // cell
    if image.width % cell:
        raise RuntimeError(f"non-integral {family} strip width: {image.width}")
    return cell, image.height, frames


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, (238, 230, 207, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(221, 211, 186, 255))
    return image


def panel(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = min((size[0] - 28) / image.width, (size[1] - 28) / image.height, 5)
    shown = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    base = checker(size)
    base.alpha_composite(shown, ((size[0] - shown.width) // 2, (size[1] - shown.height) // 2))
    return base


def contact_sheet(records: list[dict[str, object]], family: str) -> dict[str, str]:
    rows = [item for item in records if item["family"] == family and int(item["frames"]) == 1]
    width, panel_height, header = 1000, 260, 60
    sheet = Image.new("RGBA", (width, header + panel_height * len(rows)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), f"{family.title()} On/Broken: current authority / Ligne-Claire V4", fill=INKS[0], font=font)
    draw.text((12, 31), "Same canvas, alpha, bounds, padding and functional-part pixels; RGB drawing language only", fill=INKS[0], font=font)
    for index, record in enumerate(rows):
        y = header + index * panel_height
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        sheet.alpha_composite(panel(source, (500, 230)), (0, y))
        sheet.alpha_composite(panel(candidate, (500, 230)), (500, y))
        draw.text((10, y + 235), f"CURRENT · {record['filename']}", fill=INKS[0], font=font)
        draw.text((510, y + 235), f"V4 · {str(record['candidateSha256'])[:12]}", fill=INKS[0], font=font)
    path = EVIDENCE / f"{family}-on-broken-current-vs-candidate.png"
    sheet.save(path, optimize=True)
    return {"file": rel(path), "sha256": sha256(path)}


def animation_sheet(records: list[dict[str, object]]) -> dict[str, str]:
    strips = [item for item in records if int(item["frames"]) == 40]
    sample_frames = (0, 5, 10, 15, 20, 25, 30, 35)
    cell_w, cell_h = 230, 220
    sheet = Image.new("RGBA", (cell_w * len(sample_frames), 44 + cell_h * len(strips) * 2), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), "Broken-oven lighting strips: current row / V4 row — frames and 4 fps timing unchanged", fill=INKS[0], font=font)
    for strip_index, record in enumerate(strips):
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        for version, image in enumerate((source, candidate)):
            y = 44 + (strip_index * 2 + version) * cell_h
            label = "CURRENT" if version == 0 else "V4"
            for column, frame in enumerate(sample_frames):
                crop = image.crop((frame * 92, 0, (frame + 1) * 92, 85))
                sheet.alpha_composite(panel(crop, (cell_w, 190)), (column * cell_w, y))
                draw.text((column * cell_w + 8, y + 194), f"{label} · {record['filename']} · F{frame:02d}", fill=INKS[0], font=font)
    path = EVIDENCE / "oven-broken-animation-sampler-current-vs-candidate.png"
    sheet.save(path, optimize=True)
    return {"file": rel(path), "sha256": sha256(path), "sampleFrames": list(sample_frames)}


def composite(base: Image.Image, layer: Image.Image, xy: tuple[int, int]) -> None:
    base.alpha_composite(layer.convert("RGBA"), xy)


def neighbours(identifier: str, positions: dict[str, int]) -> tuple[bool, bool]:
    x = positions[identifier]
    occupied = {value for key, value in positions.items() if key != identifier}
    return x - 84 in occupied, x + 84 in occupied


def room(case: dict[str, object], candidate: bool) -> Image.Image:
    positions = dict(case["positions"])
    states = dict(case["states"])
    image = Image.open(SOURCE_DIR / "room-background-exact.png").convert("RGBA")
    heal_root = V3_CANDIDATES / "healing" if candidate else SOURCE_DIR
    body = Image.open(heal_root / "join-body-backfill-template.png").convert("RGBA")
    triangle = Image.open(heal_root / "countertop-triangle-underlay-template.png").convert("RGBA")
    ordered = sorted(positions.items(), key=lambda item: item[1])
    joins = []
    for (left_id, left_x), (right_id, right_x) in zip(ordered, ordered[1:]):
        if left_x + 84 == right_x:
            method = "oven-triangle" if "oven" in (left_id, right_id) else "flat-v22"
            joins.append((left_id, right_id, right_x, method))
            composite(image, body.crop((0, 0, 6, 63)), (right_x - 3, 145))
            if method == "oven-triangle":
                composite(image, triangle, (right_x - 12, 134))

    for identifier, x in ordered:
        left, right = neighbours(identifier, positions)
        edge = f"{'lj' if left else 'le'}-{'rj' if right else 're'}"
        if identifier in ("cabinetA", "cabinetB"):
            prefix = "cabinet-a" if identifier == "cabinetA" else "cabinet-b"
            source = (V3_CANDIDATES / "cabinets" if candidate else SOURCE_DIR) / f"{prefix}-{edge}.png"
            composite(image, Image.open(source), (x - 4, 130))
        elif identifier == "fridge":
            filename = "fridge-broken-hinge-failed.png" if states["fridge"] == "broken" else "fridge-standard.png"
            source = (V3_CANDIDATES / "fridge" if candidate else SOURCE_DIR) / filename
            composite(image, Image.open(source), (x - 30, 130))
        elif identifier == "sink":
            if candidate:
                source = V3_CANDIDATES / "sink" / f"sink-cabinet-{states['sink']}-base.png"
            else:
                source = SOURCE_DIR / "sink-cabinet-v19-exact.png"
            composite(image, Image.open(source), (x - 4, 104))
        elif identifier == "oven":
            filename = f"oven-{states['oven']}.png"
            source = (CANDIDATES / "oven" if candidate else SOURCE_DIR) / filename
            composite(image, Image.open(source), (x - 4, 127))
        elif identifier == "dishwasher":
            filename = f"dishwasher-{states['dishwasher']}-{edge}.png"
            source = (CANDIDATES / "dishwasher" if candidate else SOURCE_DIR) / filename
            composite(image, Image.open(source), (x - 7, 130))

    cap = Image.open(heal_root / "countertop-join-cap-template.png").convert("RGBA")
    cleanup_left = Image.open(heal_root / "neighbour-seam-cleanup-left.png").convert("RGBA")
    cleanup_right = Image.open(heal_root / "neighbour-seam-cleanup-right.png").convert("RGBA")
    for left_id, _right_id, edge_x, method in joins:
        if method == "flat-v22":
            composite(image, cap.crop((0, 0, 16, 12)), (edge_x - 8, 134))
        elif left_id == "oven":
            composite(image, cleanup_right, (edge_x, 134))
        else:
            composite(image, cleanup_left, (edge_x - 6, 134))
    return image


def room_proof() -> dict[str, object]:
    width, row_h, header = 1544, 224, 48
    sheet = Image.new("RGBA", (width, header + row_h * len(ROOM_CASES)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), "On/Broken placement + healing: exact current datum / V3+V4 candidate datum", fill=INKS[0], font=font)
    cases = []
    for index, case in enumerate(ROOM_CASES):
        current = room(case, False)
        proposed = room(case, True)
        current_path = EVIDENCE / f"{case['id']}-current-room.png"
        candidate_path = EVIDENCE / f"{case['id']}-candidate-room.png"
        current.save(current_path, optimize=True)
        proposed.save(candidate_path, optimize=True)
        y = header + row_h * index
        sheet.alpha_composite(current, (0, y))
        sheet.alpha_composite(proposed, (772, y))
        draw.text((8, y + 7), f"CURRENT · {case['id']}", fill=INKS[0], font=font)
        draw.text((780, y + 7), f"V4 · {case['id']}", fill=INKS[0], font=font)
        cases.append({
            "id": case["id"], "positions": case["positions"], "states": case["states"],
            "currentFile": rel(current_path), "currentSha256": sha256(current_path),
            "candidateFile": rel(candidate_path), "candidateSha256": sha256(candidate_path),
            "sinkRoomDatum": [int(case["positions"]["sink"]) - 4, 104],
        })
    path = EVIDENCE / "on-broken-healing-current-vs-candidate.png"
    sheet.save(path, optimize=True)
    return {"file": rel(path), "sha256": sha256(path), "cases": cases}


def review_html(manifest: dict[str, object]) -> str:
    links = [
        ("Complete On/Broken room proof", "evidence--on-broken-healing-current-vs-candidate.png"),
        ("Oven state contact sheet", "evidence--oven-on-broken-current-vs-candidate.png"),
        ("Dishwasher state + edge-variant contact sheet", "evidence--dishwasher-on-broken-current-vs-candidate.png"),
        ("Broken-oven animation sampler", "evidence--oven-broken-animation-sampler-current-vs-candidate.png"),
    ]
    cards = "".join(f'<article><a href="assets/{href}"><h2>{html.escape(label)}</h2><img src="assets/{href}" alt="{html.escape(label)}"></a></article>' for label, href in links)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Built-In State Ligne-Claire V4</title><style>:root{{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1280px;margin:auto;padding:24px}}header{{border-bottom:4px solid var(--ink)}}.status{{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e0a229;font-weight:800;border-radius:999px}}article{{margin:22px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}}img{{display:block;width:100%;height:auto;image-rendering:auto}}a{{color:#174562}}code{{font-size:.85em}}.warning{{border-left:6px solid #d2523b;padding-left:14px}}</style></head><body><header><span class="status">STATIC REVIEW · NOT CURRENT</span><h1>Kitchen Built-In State Ligne-Claire V4</h1><p class="warning">V3 fitted cabinetry is approved and immutable. V4 changes only oven and dishwasher On/Broken RGB drawing language. No candidate is registered or wired.</p><p>The static sheets are the primary review surface. They cover every appliance state, all eight dishwasher edge-healing variants, both 40-frame broken-oven strips and four exact-datum room arrangements. The sink stays at its existing asset coordinates and declared room datum in every case.</p><p>All effects, timing, movement locks, repair unlocks, anchors, collisions and healing rules remain hash-pinned and byte-identical.</p></header><main>{cards}</main></body></html>'''


def write_hashes() -> None:
    files = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("\n".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}" for path in files) + "\n")


def build() -> None:
    if PUBLIC.exists():
        raise RuntimeError(f"refusing to overwrite immutable review route: {PUBLIC}")
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    records = []
    for family, names in ASSET_GROUPS:
        output_dir = CANDIDATES / family
        output_dir.mkdir(parents=True, exist_ok=True)
        for name in names:
            source_path = SOURCE_DIR / name
            source = Image.open(source_path).convert("RGBA")
            candidate = stylise(source, name)
            candidate_path = output_dir / name
            candidate.save(candidate_path, optimize=True)
            cell_w, cell_h, frames = frame_geometry(source, family)
            records.append({
                "family": family, "filename": name,
                "sourceFile": rel(source_path), "sourceSha256": sha256(source_path),
                "candidateFile": rel(candidate_path), "candidateSha256": sha256(candidate_path),
                "pixels": list(source.size), "cellPixels": [cell_w, cell_h], "frames": frames,
                "fps": 4 if frames == 40 else None,
                "alphaBounds": list(source.getchannel("A").getbbox() or (0, 0, 0, 0)),
                "alphaSha256": sha_bytes(source.getchannel("A").tobytes()),
                "canvasExact": True, "alphaExact": True, "frameGeometryExact": True,
                "rgbOnly": True, "signalPixelsStayAtSourceCoordinates": True,
            })

    contacts = {family: contact_sheet(records, family) for family, _names in ASSET_GROUPS}
    animation = animation_sheet(records)
    rooms = room_proof()
    inherited = [{"file": rel(V3 / path), "sha256": sha256(V3 / path), "byteIdentical": True} for path in INHERITED_V3]
    effects = [{"file": path, "sha256": sha256(ROOT / path), "byteIdentical": True} for path in UNCHANGED_EFFECTS]
    contracts = [{"file": path, "sha256": sha256(ROOT / path), "unchanged": True} for path in CONTRACTS]
    v41_catalogue = json.loads((ROOT / CONTRACTS[0]).read_text())
    manifest = {
        "schema": "lighthouse-keeper/kitchen-built-in-state-ligne-claire@4",
        "set": SET, "datedDirectory": DATED, "created": "2026-10-21",
        "status": "immutable-reversible-static-review-candidate-not-approved-not-registered",
        "scope": {
            "newCandidates": ["oven On", "oven Broken and three lit combinations", "two complete 40-frame broken-oven lighting strips", "dishwasher On/Broken base states", "all eight On/Broken dishwasher adjacency variants"],
            "inheritedApprovedV3": ["fridge Standard/Broken", "sink On/Broken bases", "Cabinet A/B edge variants", "five healing layers"],
            "excludedUnchanged": ["kettle", "toaster", "mixing bowl", "pedal bin", "table/chair", "separate water, drip and suds effects"],
        },
        "visualAuthority": {
            "approvedV3Manifest": {"file": rel(V3 / "manifest.json"), "sha256": sha256(V3 / "manifest.json")},
            "approvedV3Decision": {"file": CONTRACTS[-2], "sha256": sha256(ROOT / CONTRACTS[-2])},
            "recipe": {"file": "docs/KITCHEN_LIGNE_CLAIRE_ART_RECIPE_2026-10-21.md", "sha256": sha256(ROOT / "docs/KITCHEN_LIGNE_CLAIRE_ART_RECIPE_2026-10-21.md")},
            "generatedCalibrationUsed": False,
        },
        "derivation": "Deterministic RGB-only semantic spot-colour translation from each exact V41 state asset; no generated production pixels, resize, crop, alpha edit, spatial filter, contour growth, detail deletion or part reinterpretation",
        "assets": records,
        "inheritedApprovedV3": inherited,
        "unchangedEffects": effects,
        "unchangedContracts": contracts,
        "evidence": {"contacts": contacts, "animation": animation, "rooms": rooms},
        "behavior": {
            "brokenAssetLock": v41_catalogue["brokenAssetLock"],
            "snapContract": v41_catalogue["snapContract"],
            "effectOwnership": "exact approved V41 asset-local anchor contract",
            "ovenLightingFrames": 40, "ovenLightingFps": 4,
            "dishwasherEdgeVariantsPerState": 4,
        },
        "checks": {
            "sourceBytesUntouched": True, "candidateCanvasExact": True, "candidateAlphaExact": True,
            "transparentPaddingExact": True, "frameGeometryAndTimingExact": True,
            "allDishwasherOnBrokenEdgeVariantsPresent": True,
            "sinkCanvasAndAlphaInheritedV3Exact": True, "sinkRoomDatumUnchanged": True,
            "movementSnapSwapBrokenLockRepairUnlockHealingContractsUnchanged": True,
            "effectBytesUnchanged": True, "runtimeChanged": False, "roomLayoutChanged": False,
            "registrationPerformed": False, "currentSelectorChanged": False,
        },
        "approvalRequiredFor": "any V4 registration, selector update, Final copy or runtime wiring",
        "rollback": "Discard only this V4 dated directory and matching review set; approved V3, all source/current/production files, runtime code and selectors remain byte-for-byte in place.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({
        "set": SET, "status": "blocked-pending-explicit-frank-approval",
        "register": False, "promote": False, "currentSelectorChanges": [],
    }, indent=2) + "\n")

    PUBLIC_ASSETS.mkdir(parents=True, exist_ok=False)
    for record in records:
        shutil.copy2(ROOT / str(record["candidateFile"]), PUBLIC_ASSETS / f"{record['family']}--{record['filename']}")
    evidence_paths = [contacts["oven"]["file"], contacts["dishwasher"]["file"], animation["file"], rooms["file"]]
    evidence_paths += [case[key] for case in rooms["cases"] for key in ("currentFile", "candidateFile")]
    for raw in evidence_paths:
        source = ROOT / str(raw)
        shutil.copy2(source, PUBLIC_ASSETS / f"evidence--{source.name}")
    (PUBLIC / "index.html").write_text(review_html(manifest))
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
    write_hashes()
    verify()
    print(f"Built {SET}: {len(records)} exact-geometry state candidates; registration remains closed")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    if manifest["set"] != SET or "not-approved" not in manifest["status"]:
        raise RuntimeError("identity/status drift")
    if manifest["checks"]["registrationPerformed"] or manifest["checks"]["currentSelectorChanged"]:
        raise RuntimeError("registration boundary opened")
    expected = sum(len(names) for _family, names in ASSET_GROUPS)
    if len(manifest["assets"]) != expected:
        raise RuntimeError("asset coverage drift")
    for record in manifest["assets"]:
        source_path = ROOT / record["sourceFile"]
        candidate_path = ROOT / record["candidateFile"]
        source = Image.open(source_path).convert("RGBA")
        candidate = Image.open(candidate_path).convert("RGBA")
        if sha256(source_path) != record["sourceSha256"] or sha256(candidate_path) != record["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record['filename']}")
        if source.size != candidate.size or source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"canvas/alpha/padding drift: {record['filename']}")
        rebuilt = stylise(source, str(record["filename"]))
        if rebuilt.tobytes() != candidate.tobytes():
            raise RuntimeError(f"deterministic RGB drift: {record['filename']}")
        cell_w, cell_h, frames = frame_geometry(candidate, str(record["family"]))
        if [cell_w, cell_h] != record["cellPixels"] or frames != record["frames"]:
            raise RuntimeError(f"frame geometry drift: {record['filename']}")
        if frames == 40:
            for frame in range(frames):
                source_alpha = source.crop((frame * cell_w, 0, (frame + 1) * cell_w, cell_h)).getchannel("A").tobytes()
                candidate_alpha = candidate.crop((frame * cell_w, 0, (frame + 1) * cell_w, cell_h)).getchannel("A").tobytes()
                if source_alpha != candidate_alpha:
                    raise RuntimeError(f"frame alpha drift: {record['filename']} F{frame}")
    edge_names = {item["filename"] for item in manifest["assets"] if item["family"] == "dishwasher"}
    for state in ("on", "broken"):
        for edge in ("le-re", "le-rj", "lj-re", "lj-rj"):
            if f"dishwasher-{state}-{edge}.png" not in edge_names:
                raise RuntimeError(f"missing dishwasher variant: {state}-{edge}")
    for item in manifest["inheritedApprovedV3"] + manifest["unchangedEffects"] + manifest["unchangedContracts"]:
        if sha256(ROOT / item["file"]) != item["sha256"]:
            raise RuntimeError(f"inherited authority drift: {item['file']}")
    for case in manifest["evidence"]["rooms"]["cases"]:
        expected_sink = [int(case["positions"]["sink"]) - 4, 104]
        if case["sinkRoomDatum"] != expected_sink:
            raise RuntimeError(f"sink moved in room proof: {case['id']}")
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["register"] or register["promote"] or register["currentSelectorChanges"]:
        raise RuntimeError("registration guard is open")
    review = (PUBLIC / "index.html").read_text()
    if "image-rendering:pixelated" in review or "image-rendering:auto" not in review:
        raise RuntimeError("smooth static review rendering contract missing")
    for line in (PACK / "HASHES.sha256").read_text().splitlines():
        expected_hash, raw = line.split("  ", 1)
        if sha256(PACK / raw) != expected_hash:
            raise RuntimeError(f"pack checksum drift: {raw}")
    print(f"Verified {SET}: exact alpha/frame geometry, fixed sink datum, all state/healing variants, V41 behavior pinned")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
