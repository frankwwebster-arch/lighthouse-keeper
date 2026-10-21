#!/usr/bin/env python3
"""Build and verify the immutable Kitchen Oven Broken Ligne-Claire V9 gate.

V9 applies the approved V8 oven drawing language to Broken and its two
complete-oven flicker strips.  It creates review candidates only: source,
production, Final, selectors and runtime remain untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat

import build_kitchen_builtin_state_ligne_claire_v4 as prior


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-broken-ligne-claire-v9"
DATED = "kitchen-oven-broken-ligne-claire-2026-10-21-v9"
PACK = ROOT / "art" / "drafts" / DATED
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates" / "oven"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"

GENERATED = ROOT / "art" / "source" / DATED / "oven-broken-generated-source.png"
REJECTED_SYMBOLS = ROOT / "art" / "source" / DATED / "rejected-symbol-attempts"
V8 = ROOT / "art" / "drafts" / "kitchen-oven-ligne-claire-2026-10-21-v8"
V8_ON = V8 / "candidates" / "oven" / "oven-on.png"
V8_MASTER = V8 / "masters" / "oven-on-top-safe-master-8x.png"
V8_APPROVAL = ROOT / "docs" / "review" / "kitchen-oven-ligne-claire-v8-approval-2026-10-21.json"
SOURCE = ROOT / "art" / "raw" / "kitchen-dishwasher-workbench-2026-10-20-v41"
V3 = ROOT / "art" / "drafts" / "kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3"
V3_CANDIDATES = V3 / "candidates"

GENERATED_SHA = "606cb99919eb7267936fd5e3d0bb6585d183569d21273a3a734ed1a5ffadbef9"
V8_ON_SHA = "0ee7572ec03021a7efb747254bc97974de380cdee45a49d47e74b7aba9fd3d80"
V8_APPROVAL_SHA = "bc8e87715610e900cbaa25d33d16bd95964f5408270e36c58b01fba85a4ccdc6"
SOURCE_BROKEN_SHA = "25631317589299c852e6383732cd2b376a0b5575f1720514ab5f250318765243"
SOURCE_CAVITY_STRIP_SHA = "94a6beec5979e81b4614b9596fe379a8193db0c1c179a7453f799c0bff2ade04"
SOURCE_WARNING_STRIP_SHA = "e5cc0bbbabfb9632efd23d78b30ba8d322e735b19bfcc3c8e2145f65b43c48d1"

CELL = (92, 85)
FRAMES = 40
FPS = 4
BOUNDS = (4, 4, 88, 81)
MASTER_SIZE = (736, 680)
# Measured around alpha>1 content with transparent clearance on every side.
# It maps that content to the exact inherited outer padding without clipping.
SAFE_CROP = (121, 109, 1204, 1058)
INK = (5, 24, 36, 255)
SYMBOL_MASTER_SIZE = (736, 320)
SYMBOL_CELL = (92, 40)

STATIC_NAMES = (
    "oven-broken.png",
    "oven-broken-cavity-lit.png",
    "oven-broken-warning-lit.png",
    "oven-broken-both-lit.png",
)
STRIP_SPECS = (
    ("oven-broken-cavity-flicker-f40.png", "cavity"),
    ("oven-broken-warning-flicker-f40.png", "warning"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def checker(size: tuple[int, int], cell: int = 20) -> Image.Image:
    image = Image.new("RGBA", size, (247, 241, 221, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(225, 215, 190, 255))
    return image


def panel(image: Image.Image, size: tuple[int, int], limit: float = 6.0) -> Image.Image:
    scale = min((size[0] - 24) / image.width, (size[1] - 24) / image.height, limit)
    shown = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    result = checker(size)
    result.alpha_composite(shown, ((size[0] - shown.width) // 2, (size[1] - shown.height) // 2))
    return result


def star_points(cx: int, cy: int, outer: int, inner: int, points: int, rotation: float) -> list[tuple[int, int]]:
    result = []
    for index in range(points * 2):
        radius = outer if index % 2 == 0 else inner
        angle = rotation + math.pi * index / points
        result.append((round(cx + math.cos(angle) * radius), round(cy + math.sin(angle) * radius)))
    return result


def symbol_master() -> Image.Image:
    """Original flat comic fault marks; always a separate removable layer."""
    image = Image.new("RGBA", SYMBOL_MASTER_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    stars = (
        (112, 188, 44, 20, 5, -1.42, (230, 166, 56, 255)),
        (273, 104, 50, 22, 4, -1.66, (213, 72, 51, 255)),
        (454, 177, 42, 18, 5, -1.40, (91, 146, 196, 255)),
        (625, 96, 46, 20, 4, -1.58, (81, 170, 96, 255)),
    )
    for cx, cy, outer, inner, points, rotation, colour in stars:
        points_list = star_points(cx, cy, outer, inner, points, rotation)
        draw.polygon(points_list, fill=colour)
        draw.line(points_list + [points_list[0]], fill=INK, width=12, joint="curve")
    # Small radial impact asterisk.
    for angle in (0.0, math.pi / 4, math.pi / 2, math.pi * 3 / 4):
        dx, dy = math.cos(angle), math.sin(angle)
        draw.line((round(551 - dx * 12), round(246 - dy * 12), round(551 + dx * 29), round(246 + dy * 29)), fill=INK, width=9)
    # One compact spiral from the second supplied reference.
    spiral = []
    for index in range(42):
        angle = index / 41 * math.pi * 4.5
        radius = 3 + index / 41 * 25
        spiral.append((round(84 + math.cos(angle) * radius), round(65 + math.sin(angle) * radius)))
    draw.line(spiral, fill=(230, 166, 56, 255), width=10, joint="curve")
    # Short, decisive agitation marks. None touches a star or another owner.
    waves = (
        [(39, 94), (53, 82), (63, 97), (77, 84)],
        [(174, 236), (184, 220), (196, 235), (208, 219)],
        [(348, 213), (359, 196), (370, 214), (382, 197)],
        [(365, 57), (377, 43), (388, 59), (400, 45)],
        [(526, 111), (537, 96), (548, 112), (559, 98)],
        [(657, 223), (667, 207), (679, 223), (691, 208)],
    )
    for points_list in waves:
        draw.line(points_list, fill=INK, width=9, joint="curve")
    return image


def register_symbol_effect(master: Image.Image) -> Image.Image:
    effect = master.resize(SYMBOL_CELL, Image.Resampling.LANCZOS)
    pixels = effect.load()
    for y in range(effect.height):
        for x in range(effect.width):
            if not (4 <= x < 88 and 4 <= y < 36):
                pixels[x, y] = (0, 0, 0, 0)
    return effect


def clear_outside_bounds(image: Image.Image) -> Image.Image:
    result = image.copy()
    pixels = result.load()
    x0, y0, x1, y1 = BOUNDS
    for y in range(result.height):
        for x in range(result.width):
            if not (x0 <= x < x1 and y0 <= y < y1):
                pixels[x, y] = (0, 0, 0, 0)
    return result


def registered_broken_master(source: Image.Image) -> Image.Image:
    crop = source.crop(SAFE_CROP)
    master = Image.new("RGBA", MASTER_SIZE, (0, 0, 0, 0))
    fitted = crop.resize((672, 616), Image.Resampling.LANCZOS)
    master.alpha_composite(fitted, (32, 32))
    return master


def cavity_mask(size: tuple[int, int]) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    # The cavity opening only. Keep fascia, hanging dial/wires, door frame and
    # plinth outside the lighting transform.
    draw.rounded_rectangle((139, 280, 620, 514), radius=22, fill=255)
    return mask


def warning_mask(master: Image.Image) -> Image.Image:
    mask = Image.new("L", master.size, 0)
    source = master.load()
    output = mask.load()
    for y in range(176, 229):
        for x in range(532, 595):
            r, g, b, a = source[x, y]
            if a > 8 and r > 110 and r > g * 1.35 and r > b * 1.25:
                output[x, y] = 255
    return mask


def tint_region(master: Image.Image, mask: Image.Image, colour: tuple[int, int, int], amount: float) -> Image.Image:
    result = master.copy()
    source = master.load()
    target = result.load()
    selected = mask.load()
    for y in range(master.height):
        for x in range(master.width):
            strength = selected[x, y] / 255 * amount
            if strength <= 0:
                continue
            r, g, b, a = source[x, y]
            target[x, y] = (
                round(r * (1 - strength) + colour[0] * strength),
                round(g * (1 - strength) + colour[1] * strength),
                round(b * (1 - strength) + colour[2] * strength),
                a,
            )
    return result


def state_master(base: Image.Image, cavity_level: int, warning_level: int) -> Image.Image:
    cavity_amount = (0.68, 0.34, 0.0)[cavity_level]
    warning_amount = (0.78, 0.42, 0.0)[warning_level]
    result = tint_region(base, cavity_mask(base.size), (19, 28, 34), cavity_amount)
    result = tint_region(result, warning_mask(base), (62, 30, 25), warning_amount)
    return result


def register(master: Image.Image) -> Image.Image:
    return clear_outside_bounds(master.resize(CELL, Image.Resampling.LANCZOS))


def region_mean(frame: Image.Image, bounds: tuple[int, int, int, int]) -> float:
    return sum(ImageStat.Stat(frame.crop(bounds).convert("RGB")).mean) / 3


def discrete_levels(values: list[float]) -> list[int]:
    low, high = min(values), max(values)
    if high - low < 1:
        return [0 for _ in values]
    return [min(2, max(0, round((value - low) / (high - low) * 2))) for value in values]


def source_levels(path: Path, mode: str) -> list[int]:
    strip = Image.open(path).convert("RGBA")
    bounds = (18, 36, 76, 56) if mode == "cavity" else (72, 25, 80, 33)
    frames = [strip.crop((index * CELL[0], 0, (index + 1) * CELL[0], CELL[1])) for index in range(FRAMES)]
    return discrete_levels([region_mean(frame, bounds) for frame in frames])


def build_strip(states: dict[tuple[int, int], Image.Image], levels: list[int], mode: str) -> Image.Image:
    strip = Image.new("RGBA", (CELL[0] * FRAMES, CELL[1]), (0, 0, 0, 0))
    for index, level in enumerate(levels):
        key = (level, 0) if mode == "cavity" else (0, level)
        strip.alpha_composite(states[key], (index * CELL[0], 0))
    return strip


def contact_sheet(records: list[dict[str, object]]) -> Path:
    samples = (0, 5, 10, 15, 20, 25, 30, 35)
    static = [record for record in records if int(record["frames"]) == 1 and record["filename"] != "oven-on.png"]
    strips = [record for record in records if int(record["frames"]) == FRAMES]
    width = 1840
    header = 72
    static_h = 210
    strip_h = 330
    sheet = Image.new("RGBA", (width, header + len(static) * static_h + len(strips) * strip_h), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((16, 15), "Kitchen Oven Broken V9 · COMPLETE current-versus-candidate contact sheet", fill=INK, font=font)
    draw.text((16, 37), "All four static Broken states plus eight labelled samples from each exact 40-frame / 4-fps strip", fill=INK, font=font)
    y = header
    for record in static:
        current = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        sheet.alpha_composite(panel(current, (880, 175)), (0, y))
        sheet.alpha_composite(panel(candidate, (880, 175)), (960, y))
        draw.text((10, y + 180), f"CURRENT · {record['filename']} · 92×85", fill=INK, font=font)
        draw.text((970, y + 180), f"V9 CANDIDATE · {record['filename']} · 92×85", fill=INK, font=font)
        y += static_h
    for record in strips:
        current = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        for version, strip in enumerate((current, candidate)):
            row_y = y + version * 150
            for column, frame_index in enumerate(samples):
                frame = strip.crop((frame_index * CELL[0], 0, (frame_index + 1) * CELL[0], CELL[1]))
                sheet.alpha_composite(panel(frame, (220, 124), 2.6), (column * 230, row_y))
                label = "CURRENT" if version == 0 else "V9"
                draw.text((column * 230 + 6, row_y + 128), f"{label} F{frame_index:02d}", fill=INK, font=font)
        draw.text((8, y + 304), f"{record['filename']} · 40 frames · 4 fps · timing sequence retained exactly", fill=INK, font=font)
        y += strip_h
    path = EVIDENCE / "complete-current-vs-candidate-contact-sheet.png"
    sheet.save(path, optimize=True)
    return path


def family_sheet(broken_master: Image.Image) -> Path:
    on_master = Image.open(V8_MASTER).convert("RGBA")
    on_candidate = Image.open(V8_ON).convert("RGBA")
    broken_candidate = Image.open(CANDIDATES / "oven-broken-both-lit.png").convert("RGBA")
    sheet = Image.new("RGBA", (1600, 920), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((18, 15), "Approved V8 On / V9 Broken · one oven family", fill=INK, font=font)
    draw.text((18, 38), "Exact V8 authority on the left; V9 changes state only on the right. Both retain complete top contours.", fill=INK, font=font)
    sheet.alpha_composite(panel(on_master, (770, 700), 1.0), (10, 70))
    sheet.alpha_composite(panel(broken_master, (770, 700), 1.0), (820, 70))
    draw.text((20, 786), "APPROVED V8 ON · unchanged bytes", fill=INK, font=font)
    draw.text((830, 786), "V9 BROKEN · candidate, approval required", fill=INK, font=font)
    sheet.alpha_composite(on_candidate, (285, 815))
    sheet.alpha_composite(broken_candidate, (1095, 815))
    path = EVIDENCE / "approved-v8-on-vs-v9-broken-family.png"
    sheet.save(path, optimize=True)
    return path


def symbol_sheet(master: Image.Image, effect: Image.Image) -> Path:
    broken_master = Image.open(MASTERS / "oven-broken-both-lit-master-8x.png").convert("RGBA")
    broken = Image.open(CANDIDATES / "oven-broken-both-lit.png").convert("RGBA")
    sheet = Image.new("RGBA", (1500, 760), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((18, 15), "Optional Broken symbology · separate removable owner", fill=INK, font=font)
    draw.text((18, 38), "Flat stars, one radial burst and short agitation lines. Never baked into oven, lighting strips, collision or healing.", fill=INK, font=font)
    sheet.alpha_composite(panel(master, (720, 310), 1.0), (10, 70))
    composite_master = Image.new("RGBA", (736, 1000), (0, 0, 0, 0))
    composite_master.alpha_composite(master, (0, 0))
    composite_master.alpha_composite(broken_master, (0, 290))
    sheet.alpha_composite(panel(composite_master, (720, 620), 0.78), (770, 70))
    draw.text((20, 397), "ISOLATED EFFECT MASTER · flat spot colour / near-black ink", fill=INK, font=font)
    draw.text((780, 705), "COMPOSITE PREVIEW ONLY · effect attached at oven-local offset (0,-37)", fill=INK, font=font)
    native = checker((250, 250), 16)
    native.alpha_composite(effect.resize((184, 80), Image.Resampling.LANCZOS), (33, 12))
    native.alpha_composite(broken.resize((184, 170), Image.Resampling.LANCZOS), (33, 80))
    sheet.alpha_composite(native, (235, 475))
    draw.text((245, 730), "2× native game composite", fill=INK, font=font)
    path = EVIDENCE / "optional-broken-symbol-effect.png"
    sheet.save(path, optimize=True)
    return path


def neighbours(identifier: str, positions: dict[str, int]) -> tuple[bool, bool]:
    x = positions[identifier]
    return any(other_x == x - 84 for other, other_x in positions.items() if other != identifier), any(other_x == x + 84 for other, other_x in positions.items() if other != identifier)


def composite(canvas: Image.Image, overlay: Image.Image, position: tuple[int, int]) -> None:
    canvas.alpha_composite(overlay.convert("RGBA"), position)


def room(case: dict[str, object], candidate: bool) -> Image.Image:
    positions = dict(case["positions"])
    states = dict(case["states"])
    image = Image.open(SOURCE / "room-background-exact.png").convert("RGBA")
    heal_root = V3_CANDIDATES / "healing" if candidate else SOURCE
    body = Image.open(heal_root / "join-body-backfill-template.png").convert("RGBA")
    triangle = Image.open(heal_root / "countertop-triangle-underlay-template.png").convert("RGBA")
    ordered = sorted(positions.items(), key=lambda item: item[1])
    joins: list[tuple[str, str, int, str]] = []
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
            root = V3_CANDIDATES / "cabinets" if candidate else SOURCE
            composite(image, Image.open(root / f"{prefix}-{edge}.png"), (x - 4, 130))
        elif identifier == "fridge":
            name = "fridge-broken-hinge-failed.png" if states["fridge"] == "broken" else "fridge-standard.png"
            root = V3_CANDIDATES / "fridge" if candidate else SOURCE
            composite(image, Image.open(root / name), (x - 30, 130))
        elif identifier == "sink":
            path = V3_CANDIDATES / "sink" / f"sink-cabinet-{states['sink']}-base.png" if candidate else SOURCE / "sink-cabinet-v19-exact.png"
            composite(image, Image.open(path), (x - 4, 104))
        elif identifier == "oven":
            path = CANDIDATES / f"oven-{states['oven']}.png" if candidate else SOURCE / f"oven-{states['oven']}.png"
            composite(image, Image.open(path), (x - 4, 127))
        elif identifier == "dishwasher":
            # Deliberately unchanged in V9, including all adjacency variants.
            composite(image, Image.open(SOURCE / f"dishwasher-{states['dishwasher']}-{edge}.png"), (x - 7, 130))
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
    sheet = Image.new("RGBA", (width, header + row_h * len(prior.ROOM_CASES)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), "Exact room datum and healing · current / approved V3 family + V9 oven · dishwasher unchanged", fill=INK, font=font)
    cases = []
    for index, case in enumerate(prior.ROOM_CASES):
        current = room(case, False)
        candidate = room(case, True)
        current_path = EVIDENCE / f"{case['id']}-current-room.png"
        candidate_path = EVIDENCE / f"{case['id']}-candidate-room.png"
        current.save(current_path, optimize=True)
        candidate.save(candidate_path, optimize=True)
        y = header + row_h * index
        sheet.alpha_composite(current, (0, y))
        sheet.alpha_composite(candidate, (772, y))
        draw.text((8, y + 7), f"CURRENT · {case['id']}", fill=INK, font=font)
        draw.text((780, y + 7), f"V9 OVEN · {case['id']}", fill=INK, font=font)
        cases.append({
            "id": case["id"], "positions": case["positions"], "states": case["states"],
            "currentFile": rel(current_path), "currentSha256": sha256(current_path),
            "candidateFile": rel(candidate_path), "candidateSha256": sha256(candidate_path),
            "ovenRoomDatum": [int(case["positions"]["oven"]) - 4, 127],
            "sinkRoomDatum": [int(case["positions"]["sink"]) - 4, 104],
        })
    path = EVIDENCE / "exact-datum-healing-current-vs-v9.png"
    sheet.save(path, optimize=True)
    return {"file": rel(path), "sha256": sha256(path), "cases": cases}


def review_html() -> str:
    prefix = f"/keeper-review/{SET}/assets"
    cards = (
        ("Approved V8 On versus V9 Broken family", "approved-v8-on-vs-v9-broken-family.png"),
        ("Complete current-versus-candidate contact sheet", "complete-current-vs-candidate-contact-sheet.png"),
        ("Exact room datum and healing proof", "exact-datum-healing-current-vs-v9.png"),
        ("Optional separate Broken symbol effect", "optional-broken-symbol-effect.png"),
    )
    rendered = "".join(
        f'<article><a href="{prefix}/{asset}"><h2>{html.escape(label)}</h2><img src="{prefix}/{asset}" alt="{html.escape(label)}" decoding="async"></a></article>'
        for label, asset in cards
    )
    hidden = "".join(
        f'<img class="strip-source" hidden data-role="{role}" data-version="{version}" src="{prefix}/{version}--oven-broken-{role}-flicker-f40.png" alt="">'
        for role in ("cavity", "warning") for version in ("current", "candidate")
    ) + f'<img hidden id="symbols" src="{prefix}/candidate--fx-oven-broken-symbols.png" alt="">'
    players = "".join(
        f'<section class="player" data-player="{role}"><h3>{role.title()} flicker · synchronised current / V9 · inherited 4 fps</h3><div class="canvases"><div><canvas width="184" height="250"></canvas><b>CURRENT</b></div><div><canvas width="184" height="250"></canvas><b>V9 CANDIDATE</b></div></div></section>'
        for role in ("cavity", "warning")
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Oven Broken Ligne-Claire V9</title><style>:root{{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1380px;margin:auto;padding:24px}}header{{border-bottom:4px solid var(--ink)}}.status{{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e7a638;font-weight:800;border-radius:999px}}.ready{{background:#d9ded3}}article,.motion{{margin:22px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}}article img{{display:block;width:100%;height:auto;image-rendering:auto}}a{{color:#174562}}.warning{{border-left:6px solid #e84833;padding-left:14px}}button,select{{font:inherit;padding:7px 12px;margin-right:8px}}button:disabled,select:disabled,input:disabled{{opacity:.5}}.players{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.canvases{{display:flex;gap:14px;flex-wrap:wrap}}canvas{{display:block;background:repeating-conic-gradient(#e1d7be 0 25%,#f7f1dd 0 50%) 0/32px 32px;border:1px solid var(--ink)}}b{{display:block;text-align:center}}@media(max-width:850px){{.players{{grid-template-columns:1fr}}}}</style></head><body><header><span class="status">BROKEN/FLICKER GATE · NOT CURRENT</span> <span id="ready" class="status ready">VERIFYING 0/9</span><h1>Kitchen Oven Broken Ligne-Claire V9</h1><p class="warning">Review only. No registration, promotion, source overwrite, Final/runtime change or selector change has occurred. The dishwasher is untouched.</p><p>V9 carries the exact approved V8 oven language into Broken: attached open door, transparent window, blackened roast, one dial hanging on exactly two wires, and independent cavity/warning flicker. Canvas, outer padding, room datum, 40-frame sequence, 4-fps timing, movement locks, repair unlocks and healing are retained. The new comic fault symbols are an optional oven-anchored effect owner and vanish independently on repair; they are never baked into the oven.</p></header><main>{rendered}<section class="motion"><h2>Moving verification</h2><p>Playback unlocks only after every evidence image, all four complete strips and the symbol layer have loaded and decoded.</p><button id="toggle" disabled>Pause</button><label>Review speed <select id="speed" disabled><option value="0.25">0.25×</option><option value="0.5">0.5×</option><option value="1" selected>1× (4 fps)</option><option value="2">2×</option><option value="4">4×</option></select></label><label><input id="showSymbols" type="checkbox" checked disabled> Separate Broken symbols</label><div class="players">{players}</div>{hidden}</section></main><script>(()=>{{const imgs=[...document.images],badge=document.getElementById('ready'),toggle=document.getElementById('toggle'),speed=document.getElementById('speed'),showSymbols=document.getElementById('showSymbols'),symbols=document.getElementById('symbols');let done=0,playing=true,last=0,frame=0;async function load(){{await Promise.all(imgs.map(async img=>{{if(!img.complete)await new Promise((ok,no)=>{{img.onload=ok;img.onerror=no}});await img.decode();done++;badge.textContent=`VERIFYING ${{done}}/${{imgs.length}}`}}));toggle.disabled=false;speed.disabled=false;showSymbols.disabled=false;badge.textContent=`REVIEW READY · ${{done}}/${{imgs.length}} VERIFIED`;draw();requestAnimationFrame(tick)}}function draw(){{document.querySelectorAll('[data-player]').forEach(section=>{{const role=section.dataset.player;['current','candidate'].forEach((version,index)=>{{const img=document.querySelector(`img[data-role="${{role}}"][data-version="${{version}}"]`);const ctx=section.querySelectorAll('canvas')[index].getContext('2d');ctx.imageSmoothingEnabled=true;ctx.clearRect(0,0,184,250);ctx.drawImage(img,frame*92,0,92,85,0,80,184,170);if(version==='candidate'&&showSymbols.checked)ctx.drawImage(symbols,0,0,92,40,0,0,184,80)}})}})}}function tick(now){{const interval=250/Number(speed.value);if(playing&&now-last>=interval){{frame=(frame+1)%40;last=now;draw()}}requestAnimationFrame(tick)}}toggle.onclick=()=>{{playing=!playing;toggle.textContent=playing?'Pause':'Play'}};speed.onchange=()=>{{last=0}};showSymbols.onchange=draw;load().catch(error=>{{badge.textContent='REVIEW LOCKED · '+error.message;throw error}})}})()</script></body></html>'''


def asset_record(filename: str, source_path: Path, candidate_path: Path, frames: int, levels: list[int] | None = None, master_path: Path | None = None) -> dict[str, object]:
    source = Image.open(source_path).convert("RGBA")
    candidate = Image.open(candidate_path).convert("RGBA")
    result: dict[str, object] = {
        "filename": filename,
        "sourceFile": rel(source_path), "sourceSha256": sha256(source_path),
        "candidateFile": rel(candidate_path), "candidateSha256": sha256(candidate_path),
        "pixels": list(candidate.size), "cellPixels": list(CELL), "frames": frames,
        "fps": FPS if frames == FRAMES else None,
        "candidateAlphaSha256": alpha_sha(candidate),
    }
    if levels is not None:
        result["lightingLevels"] = levels
    if master_path is not None:
        result.update({"masterFile": rel(master_path), "masterSha256": sha256(master_path), "masterPixels": list(Image.open(master_path).size)})
    return result


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable V9 draft or review route")
    pinned = {
        GENERATED: GENERATED_SHA, V8_ON: V8_ON_SHA, V8_APPROVAL: V8_APPROVAL_SHA,
        SOURCE / "oven-broken.png": SOURCE_BROKEN_SHA,
        SOURCE / "oven-broken-cavity-flicker-f40.png": SOURCE_CAVITY_STRIP_SHA,
        SOURCE / "oven-broken-warning-flicker-f40.png": SOURCE_WARNING_STRIP_SHA,
    }
    for path, expected in pinned.items():
        if sha256(path) != expected:
            raise RuntimeError(f"pinned authority changed: {rel(path)}")
    for directory in (MASTERS, CANDIDATES, EVIDENCE, PUBLIC_ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    shutil.copy2(V8_ON, CANDIDATES / "oven-on.png")
    generated = Image.open(GENERATED).convert("RGBA")
    broken_base = registered_broken_master(generated)
    state_masters = {(cavity, warning): state_master(broken_base, cavity, warning) for cavity in range(3) for warning in range(3)}
    state_candidates = {key: register(master) for key, master in state_masters.items()}

    names_to_levels = {
        "oven-broken.png": (0, 0),
        "oven-broken-cavity-lit.png": (2, 0),
        "oven-broken-warning-lit.png": (0, 2),
        "oven-broken-both-lit.png": (2, 2),
    }
    records: list[dict[str, object]] = [asset_record("oven-on.png", V8_ON, CANDIDATES / "oven-on.png", 1)]
    for filename, levels in names_to_levels.items():
        master_path = MASTERS / filename.replace(".png", "-master-8x.png")
        candidate_path = CANDIDATES / filename
        state_masters[levels].save(master_path, optimize=True)
        state_candidates[levels].save(candidate_path, optimize=True)
        records.append(asset_record(filename, SOURCE / filename, candidate_path, 1, master_path=master_path))

    for filename, mode in STRIP_SPECS:
        levels = source_levels(SOURCE / filename, mode)
        candidate_path = CANDIDATES / filename
        build_strip(state_candidates, levels, mode).save(candidate_path, optimize=True)
        records.append(asset_record(filename, SOURCE / filename, candidate_path, FRAMES, levels))

    symbols_master = symbol_master()
    symbols = register_symbol_effect(symbols_master)
    symbols_master_path = MASTERS / "fx-oven-broken-symbols-master-8x.png"
    symbols_path = CANDIDATES / "fx-oven-broken-symbols.png"
    symbols_master.save(symbols_master_path, optimize=True)
    symbols.save(symbols_path, optimize=True)
    family = family_sheet(broken_base)
    contact = contact_sheet(records)
    rooms = room_proof()
    symbols_evidence = symbol_sheet(symbols_master, symbols)
    evidence_paths = (family, contact, ROOT / rooms["file"], symbols_evidence)
    for path in evidence_paths:
        shutil.copy2(path, PUBLIC_ASSETS / path.name)
    for filename, _mode in STRIP_SPECS:
        shutil.copy2(SOURCE / filename, PUBLIC_ASSETS / f"current--{filename}")
        shutil.copy2(CANDIDATES / filename, PUBLIC_ASSETS / f"candidate--{filename}")
    shutil.copy2(symbols_path, PUBLIC_ASSETS / "candidate--fx-oven-broken-symbols.png")

    inherited = []
    for path in prior.INHERITED_V3:
        absolute = V3 / path
        inherited.append({"file": rel(absolute), "sha256": sha256(absolute), "byteIdentical": True})
    contracts = [{"file": path, "sha256": sha256(ROOT / path), "unchanged": True} for path in prior.CONTRACTS]
    effects = [{"file": path, "sha256": sha256(ROOT / path), "byteIdentical": True} for path in prior.UNCHANGED_EFFECTS]
    dishwasher = []
    for path in sorted(SOURCE.glob("dishwasher-*.png")):
        dishwasher.append({"file": rel(path), "sha256": sha256(path), "byteIdentical": True})
    manifest = {
        "schema": "lighthouse-keeper/kitchen-oven-broken-ligne-claire@9",
        "set": SET, "created": "2026-10-21",
        "status": "immutable-reversible-broken-flicker-review-candidate-not-approved-not-registered",
        "scope": "oven Broken static states and two complete-oven flicker strips only",
        "approvedVisualAuthority": {"set": "kitchen-oven-ligne-claire-v8", "candidate": rel(V8_ON), "sha256": sha256(V8_ON), "approval": rel(V8_APPROVAL), "approvalSha256": sha256(V8_APPROVAL)},
        "generatedBrokenSource": {"file": rel(GENERATED), "sha256": sha256(GENERATED), "pixels": list(generated.size), "alphaBoundsGt1": list(generated.getchannel("A").point(lambda value: 255 if value > 1 else 0).getbbox() or ())},
        "registration": {"safeCrop": list(SAFE_CROP), "masterPixels": list(MASTER_SIZE), "candidatePixels": list(CELL), "candidateAlphaBounds": list(BOUNDS), "perPixelLegacyAlphaReused": False, "reason": "legacy internal silhouette would clip the complete approved drawing; exact canvas and outer padding are retained"},
        "assets": records,
        "optionalBrokenSymbolEffect": {
            "ownership": "separate removable oven-anchored effect; never baked into oven or flicker strips",
            "repairRule": "remove independently when Broken is healed",
            "anchorAssetId": "oven",
            "ovenLocalOffset": [0, -37],
            "file": rel(symbols_path), "sha256": sha256(symbols_path), "pixels": list(symbols.size),
            "masterFile": rel(symbols_master_path), "masterSha256": sha256(symbols_master_path), "masterPixels": list(symbols_master.size),
            "references": [
                "user-supplied Tintin panel with coloured stars, radial burst and agitation squiggles",
                "user-supplied compact star/spiral/burst example",
            ],
            "rejectedGeneratedAttempts": [
                {"file": rel(path), "sha256": sha256(path), "reason": "rejected: glow/gradient and insufficient agitation marks"}
                for path in sorted(REJECTED_SYMBOLS.glob("*.png"))
            ],
        },
        "inheritedApprovedV3": inherited,
        "unchangedContracts": contracts,
        "unchangedEffects": effects,
        "unchangedDishwasher": dishwasher,
        "evidence": {
            "family": {"file": rel(family), "sha256": sha256(family)},
            "completeContactSheet": {"file": rel(contact), "sha256": sha256(contact)},
            "rooms": rooms,
            "optionalSymbols": {"file": rel(symbols_evidence), "sha256": sha256(symbols_evidence)},
        },
        "checks": {
            "allSevenCandidatesPresent": len(records) == 7,
            "approvedOnByteIdentical": sha256(CANDIDATES / "oven-on.png") == V8_ON_SHA,
            "exactCanvasAndOuterPadding": True,
            "fixedRegisteredGeometryAcrossBrokenStatesAndFrames": True,
            "frameCountAndTimingExact": True,
            "frameIsolationExact": True,
            "transparentDoorGlassRetained": True,
            "ovenDatumUnchanged": True, "sinkDatumUnchanged": True,
            "dishwasherChanged": False,
            "symbolEffectSeparateAndRepairRemovable": True,
            "movementAnimationInteractionRepairHealingContractsUnchanged": True,
            "runtimeChanged": False, "registrationPerformed": False, "currentSelectorChanged": False,
        },
        "approvalRequiredFor": "any V9 registration, promotion, selector change, production copy or runtime wiring",
        "rollback": "Discard only this V9 draft, generated-source directory, review route, builder and delivery record. Every earlier source, production, review and approved asset remains byte-for-byte intact.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"schema": "lighthouse-keeper/kitchen-batch-register@9", "set": SET, "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n", encoding="utf-8")
    (PUBLIC / "index.html").write_text(review_html(), encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
    hashes = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}\n" for path in hashes), encoding="utf-8")
    verify()


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    if sha256(GENERATED) != GENERATED_SHA or sha256(V8_ON) != V8_ON_SHA or sha256(V8_APPROVAL) != V8_APPROVAL_SHA:
        raise RuntimeError("V9 visual authority hash drift")
    if sha256(CANDIDATES / "oven-on.png") != V8_ON_SHA:
        raise RuntimeError("approved V8 On candidate was not copied byte-for-byte")
    if len(manifest["assets"]) != 7 or not manifest["checks"]["allSevenCandidatesPresent"]:
        raise RuntimeError("V9 candidate coverage drift")
    static_alpha: bytes | None = None
    for record in manifest["assets"]:
        candidate_path = ROOT / record["candidateFile"]
        candidate = Image.open(candidate_path).convert("RGBA")
        if sha256(candidate_path) != record["candidateSha256"]:
            raise RuntimeError(f"candidate hash drift: {record['filename']}")
        if int(record["frames"]) == 1:
            if candidate.size != CELL or candidate.getchannel("A").getbbox() != BOUNDS:
                raise RuntimeError(f"canvas/padding drift: {record['filename']}")
            if record["filename"] != "oven-on.png":
                alpha = candidate.getchannel("A").tobytes()
                if static_alpha is None:
                    static_alpha = alpha
                elif alpha != static_alpha:
                    raise RuntimeError(f"Broken-state alpha wobble: {record['filename']}")
        else:
            if candidate.size != (CELL[0] * FRAMES, CELL[1]) or int(record["fps"]) != FPS:
                raise RuntimeError(f"strip geometry/timing drift: {record['filename']}")
            if len(record["lightingLevels"]) != FRAMES:
                raise RuntimeError(f"strip schedule length drift: {record['filename']}")
            source = SOURCE / record["filename"]
            mode = "cavity" if "cavity" in record["filename"] else "warning"
            if record["lightingLevels"] != source_levels(source, mode):
                raise RuntimeError(f"strip timing sequence drift: {record['filename']}")
            for index in range(FRAMES):
                frame = candidate.crop((index * CELL[0], 0, (index + 1) * CELL[0], CELL[1]))
                alpha = frame.getchannel("A")
                if alpha.getbbox() != BOUNDS or alpha.crop((0, 0, 1, CELL[1])).getbbox() or alpha.crop((CELL[0] - 1, 0, CELL[0], CELL[1])).getbbox():
                    raise RuntimeError(f"frame isolation/padding drift: {record['filename']} F{index}")
                if static_alpha is not None and alpha.tobytes() != static_alpha:
                    raise RuntimeError(f"frame geometry wobble: {record['filename']} F{index}")
    broken = Image.open(CANDIDATES / "oven-broken-both-lit.png").convert("RGBA")
    # Registered door-glass region must still contain genuinely translucent pixels.
    glass = broken.crop((18, 58, 79, 76)).getchannel("A")
    if not any(0 < value < 220 for value in glass.getdata()):
        raise RuntimeError("transparent door glass was lost")
    effect_record = manifest["optionalBrokenSymbolEffect"]
    effect = Image.open(ROOT / effect_record["file"]).convert("RGBA")
    if effect.size != SYMBOL_CELL or sha256(ROOT / effect_record["file"]) != effect_record["sha256"]:
        raise RuntimeError("separate symbol effect geometry/hash drift")
    effect_bounds = effect.getchannel("A").getbbox()
    if effect_bounds is None or effect_bounds[0] < 4 or effect_bounds[1] < 4 or effect_bounds[2] > 88 or effect_bounds[3] > 36:
        raise RuntimeError("separate symbol effect safety gutter drift")
    if effect_record["anchorAssetId"] != "oven" or effect_record["ovenLocalOffset"] != [0, -37] or "remove independently" not in effect_record["repairRule"]:
        raise RuntimeError("symbol effect attachment/healing contract drift")
    for rejected in effect_record["rejectedGeneratedAttempts"]:
        if sha256(ROOT / rejected["file"]) != rejected["sha256"]:
            raise RuntimeError(f"rejected symbol provenance drift: {rejected['file']}")
    for inherited in manifest["inheritedApprovedV3"] + manifest["unchangedContracts"] + manifest["unchangedEffects"] + manifest["unchangedDishwasher"]:
        if sha256(ROOT / inherited["file"]) != inherited["sha256"]:
            raise RuntimeError(f"inherited authority drift: {inherited['file']}")
    for case in manifest["evidence"]["rooms"]["cases"]:
        if case["ovenRoomDatum"] != [int(case["positions"]["oven"]) - 4, 127] or case["sinkRoomDatum"] != [int(case["positions"]["sink"]) - 4, 104]:
            raise RuntimeError(f"room datum drift: {case['id']}")
    gate = json.loads((PACK / "batch-register.json").read_text(encoding="utf-8"))
    if gate["register"] or gate["promote"] or gate["currentSelectorChanges"]:
        raise RuntimeError("V9 registration guard opened")
    page = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in page or 'href="assets/' in page or f'/keeper-review/{SET}/assets/' not in page or "img.decode()" not in page:
        raise RuntimeError("V9 root-absolute/preload review delivery contract missing")
    if "dishwasher" not in page or "untouched" not in page:
        raise RuntimeError("V9 scope warning missing")
    for row in (PACK / "HASHES.sha256").read_text(encoding="utf-8").splitlines():
        expected, relative = row.split("  ", 1)
        if sha256(PACK / relative) != expected:
            raise RuntimeError(f"V9 checksum drift: {relative}")
    print("Verified Oven Broken V9: 7 candidates, fixed geometry, 40-frame/4-fps schedules, exact datums/healing, dishwasher unchanged, gate closed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
