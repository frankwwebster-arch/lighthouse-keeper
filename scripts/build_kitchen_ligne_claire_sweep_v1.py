#!/usr/bin/env python3
"""Build the reversible Kitchen Ligne-Claire Sweep V1 review pack.

The conversion is deliberately geometry-locked: every candidate keeps the
source RGBA canvas and alpha bytes exactly, while RGB is reduced to the shared
spot-colour language and existing structural ink is normalised to the approved
sandwich-tomato V2 near-black.  Runtime, state, timing and collision data are
not rewritten or registered.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import shutil
import colorsys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-sweep-v1"
DATED = "kitchen-ligne-claire-sweep-2026-10-21-v1"
PACK = ROOT / "art" / "drafts" / DATED
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"

INK = (5, 24, 36)  # exact sandwich-tomato V2 ink
VISIBLE_ALPHA = 8

# A restrained shared spot palette.  The first six entries are the exact
# sandwich-tomato V2 palette; the remainder cover the established kitchen's
# semantic blues, sea-glass, metal, wood and water without gradients.
PALETTE = (
    INK,
    (195, 43, 55),
    (232, 72, 51),
    (245, 126, 106),
    (246, 229, 183),
    (57, 148, 55),
    (250, 244, 224),
    (217, 222, 211),
    (174, 187, 185),
    (92, 108, 111),
    (29, 69, 98),
    (35, 91, 133),
    (45, 119, 157),
    (83, 177, 181),
    (109, 201, 194),
    (64, 153, 194),
    (211, 111, 45),
    (231, 166, 56),
    (144, 82, 49),
    (181, 102, 54),
    (115, 125, 76),
    (173, 194, 132),
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def asset(family: str, source_dir: str, name: str, role: str = "state") -> dict[str, str]:
    return {
        "family": family,
        "source": f"{source_dir}/{name}",
        "name": name,
        "role": role,
    }


ASSETS: tuple[dict[str, str], ...] = tuple(
    [
        asset("cabinet-a", "art/raw/kitchen-split-cabinet-workbench-2026-10-20-v38", name)
        for name in (
            "cabinet-a-le-re.png", "cabinet-a-le-rj.png",
            "cabinet-a-lj-re.png", "cabinet-a-lj-rj.png",
        )
    ]
    + [
        asset("cabinet-b", "art/raw/kitchen-split-cabinet-workbench-2026-10-20-v38", name)
        for name in (
            "cabinet-b-le-re.png", "cabinet-b-le-rj.png",
            "cabinet-b-lj-re.png", "cabinet-b-lj-rj.png",
        )
    ]
    + [
        asset("join-healing", "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41", name, "compositor-layer")
        for name in (
            "join-body-backfill-template.png", "countertop-join-cap-template.png",
            "countertop-triangle-underlay-template.png",
            "neighbour-seam-cleanup-left.png", "neighbour-seam-cleanup-right.png",
        )
    ]
    + [
        asset("fridge", "art/raw/kitchen-modular-fridge-workbench-2026-10-20-v37", name)
        for name in ("fridge-standard.png", "fridge-broken-hinge-failed.png")
    ]
    + [
        asset("dishwasher", "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41", name)
        for name in (
            "dishwasher-off.png", "dishwasher-on.png", "dishwasher-broken.png",
            "dishwasher-off-le-re.png", "dishwasher-off-le-rj.png",
            "dishwasher-off-lj-re.png", "dishwasher-off-lj-rj.png",
            "dishwasher-on-le-re.png", "dishwasher-on-le-rj.png",
            "dishwasher-on-lj-re.png", "dishwasher-on-lj-rj.png",
            "dishwasher-broken-le-re.png", "dishwasher-broken-le-rj.png",
            "dishwasher-broken-lj-re.png", "dishwasher-broken-lj-rj.png",
        )
    ]
    + [
        asset("oven", "art/raw/kitchen-oven-standalone-2026-10-20-v32", name,
              "full-state-animation" if "f40" in name else "state")
        for name in (
            "oven-off.png", "oven-on.png", "oven-broken.png",
            "oven-broken-cavity-lit.png", "oven-broken-warning-lit.png",
            "oven-broken-both-lit.png", "oven-broken-cavity-flicker-f40.png",
            "oven-broken-warning-flicker-f40.png",
        )
    ]
    + [
        asset("sink", "art/raw/kitchen-sink-smooth-join-2026-10-19-v19", name)
        for name in (
            "sink-cabinet-standard.png", "sink-cabinet-on-base.png",
            "sink-cabinet-broken-base.png",
        )
    ]
    + [
        asset("kettle", "art/raw/kitchen-kettle-standalone-2026-10-21-v45", name)
        for name in ("kettle-off.png", "kettle-on.png", "kettle-broken.png")
    ]
    + [
        asset("toaster", "art/raw/kitchen-rebuild-modular-2026-10-19-v10", name)
        for name in ("toaster-off.png", "toaster-on.png", "toaster-broken.png")
    ]
    + [
        asset("mixing-bowl", "art/raw/kitchen-rebuild-modular-2026-10-19-v10", name)
        for name in ("bowl-off.png", "bowl-on.png", "bowl-broken.png")
    ]
    + [asset("table-chair", "art/raw/kitchen-rebuild-modular-2026-10-19-v10", "table-chair.png")]
    + [
        asset("pedal-bin", "art/raw/kitchen-bin-effects-2026-10-18-v31", name)
        for name in ("bin-standard.png", "bin-broken-overflowing.png")
    ]
)


INHERITED_EFFECTS: tuple[str, ...] = (
    "art/raw/kitchen-modular-fridge-workbench-2026-10-20-v37/fx-fridge-drip-ripple-f40.png",
    "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-dishwasher-suds--compact-f40.png",
    "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-dishwasher-suds--regular-f40.png",
    "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-dishwasher-suds--emphatic-f40.png",
    "art/raw/kitchen-sink-smooth-join-2026-10-19-v19/fx-sink-on-water-f40.png",
    "art/raw/kitchen-sink-smooth-join-2026-10-19-v19/fx-sink-broken-basin-spouts-f40.png",
    "art/raw/kitchen-kettle-standalone-2026-10-21-v45/fx-kettle-on-steam--compact-f40.png",
    "art/raw/kitchen-kettle-standalone-2026-10-21-v45/fx-kettle-on-steam--regular-f40.png",
    "art/raw/kitchen-kettle-standalone-2026-10-21-v45/fx-kettle-on-steam--emphatic-f40.png",
    "art/raw/kitchen-kettle-standalone-2026-10-21-v45/fx-kettle-broken-steam--compact-f40.png",
    "art/raw/kitchen-kettle-standalone-2026-10-21-v45/fx-kettle-broken-steam--regular-f40.png",
    "art/raw/kitchen-kettle-standalone-2026-10-21-v45/fx-kettle-broken-steam--emphatic-f40.png",
    "art/raw/kitchen-bin-effects-2026-10-18-v31/fx-stench-miasma-f40.png",
    "art/raw/kitchen-bin-effects-2026-10-18-v31/fx-slow-flies-f40.png",
    "art/raw/kitchen-rebuild-modular-2026-10-19-v10/fx-toaster-on-heat--classic-f40.png",
    "art/raw/kitchen-rebuild-modular-2026-10-19-v10/fx-toaster-broken-smoke--classic-f40.png",
)


CONTRACT_FILES: tuple[str, ...] = (
    "art/drafts/kitchen-split-cabinet-workbench-2026-10-20-v38/candidate-catalogue.json",
    "art/drafts/kitchen-modular-fridge-workbench-2026-10-20-v37/candidate-catalogue.json",
    "art/drafts/kitchen-dishwasher-workbench-2026-10-20-v41/candidate-catalogue.json",
    "art/drafts/kitchen-oven-standalone-2026-10-20-v32/candidate-catalogue.json",
    "art/drafts/kitchen-sink-smooth-join-2026-10-19-v19/candidate-catalogue.json",
    "art/drafts/kitchen-kettle-standalone-2026-10-21-v45/candidate-catalogue.json",
    "art/drafts/kitchen-rebuild-modular-2026-10-19-v10/candidate-catalogue.json",
    "art/drafts/kitchen-bin-effects-2026-10-18-v31/candidate-catalogue.json",
    "docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md",
)


REFERENCE_IMAGES: tuple[str, ...] = (
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-fa7e6c19-4319-4c06-a9c4-c34dc95f1132.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-92f74b7a-3dc7-49d3-a00e-880022f47bcb.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-40b3e539-2030-45d2-94c3-e9dc186ae814.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-b0dacd79-6b13-4463-b160-50307abb11a1.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-30fd6420-0ff8-4989-b6cb-d8394bf3eaf5.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-8adc6086-7c2e-40ec-a03d-10f56a0d2c98.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-801fb3f8-e389-4e83-9f0f-14c294d1ee50.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-cfd7e9d7-968c-44de-b734-6a5e3b212e60.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-b2d26276-dac7-4cd2-b457-4b8221adc1f4.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-58ad51a8-45bc-4af9-83cc-fbc1f02b51cd.png",
    "/var/folders/81/wzg46xhj4xv6yqt7v22vq2kw0000gp/T/codex-clipboard-c37e3b49-cb19-4403-a355-2c8b59265f25.png",
)


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").getbbox()


def rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    values = []
    for value in rgb:
        channel = value / 255.0
        values.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
    r, g, b = values
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722)
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883
    def pivot(value: float) -> float:
        return value ** (1 / 3) if value > 0.008856 else 7.787 * value + 16 / 116
    fx, fy, fz = pivot(x), pivot(y), pivot(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


LAB_PALETTE = tuple(rgb_to_lab(colour) for colour in PALETTE)


def nearest_palette(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    lab = rgb_to_lab(rgb)
    best = 0
    best_distance = float("inf")
    for index, candidate in enumerate(LAB_PALETTE):
        distance = sum((lab[channel] - candidate[channel]) ** 2 for channel in range(3))
        if distance < best_distance:
            best = index
            best_distance = distance
    return PALETTE[best]


def spot_colour(rgb: tuple[int, int, int], family: str) -> tuple[int, int, int]:
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    degrees = h * 360
    if s < 0.32:
        light_neutral = (217, 222, 211) if family in {"dishwasher", "sink"} else (246, 229, 183)
        if v > 0.48:
            return light_neutral
        if v > 0.30:
            return (174, 187, 185)
        return (92, 108, 111)
    if degrees < 15 or degrees >= 345:
        return (195, 43, 55) if v < 0.62 else (232, 72, 51)
    if degrees < 48:
        return (144, 82, 49) if v < 0.52 else ((231, 166, 56) if degrees > 34 else (211, 111, 45))
    if degrees < 72:
        return (231, 166, 56) if s > 0.38 else (246, 229, 183)
    if degrees < 165:
        return (57, 148, 55) if v < 0.72 else (173, 194, 132)
    if degrees < 205:
        return (83, 177, 181) if v < 0.72 else (109, 201, 194)
    if degrees < 260:
        if v < 0.36:
            return (29, 69, 98)
        if v < 0.62:
            return (35, 91, 133)
        return (45, 119, 157)
    if degrees < 325:
        return (35, 91, 133) if v < 0.58 else (245, 126, 106)
    return (195, 43, 55) if v < 0.62 else (232, 72, 51)


def stylise(source: Image.Image, family: str) -> Image.Image:
    source = source.convert("RGBA")
    width, height = source.size
    # Pillow 8 on the system Python and current Pillow both expose getdata().
    rgba = list(source.getdata())
    alpha = source.getchannel("A")
    visible = alpha.point(lambda value: 255 if value > VISIBLE_ALPHA else 0)

    # Boundary ink remains inside the original alpha silhouette.  The radius
    # grows only for high-resolution concept masters and strip cells.
    radius = max(1, min(2, round(min(width, height) / 256)))
    eroded = visible.filter(ImageFilter.MinFilter(radius * 2 + 1))
    boundary = ImageChops.subtract(visible, eroded)

    # Existing dark construction lines are kept, but only at decisive values.
    line = Image.new("L", source.size, 0)
    line_pixels = line.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = rgba[y * width + x]
            if a > VISIBLE_ALPHA and max(r, g, b) < 48:
                line_pixels[x, y] = 255
    if radius > 1:
        line = line.filter(ImageFilter.MaxFilter(radius * 2 - 1))
    ink_mask = ImageChops.lighter(boundary, line)

    output = Image.new("RGBA", source.size, (0, 0, 0, 0))
    output_pixels = output.load()
    ink_pixels = ink_mask.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = rgba[y * width + x]
            if a == 0:
                output_pixels[x, y] = (0, 0, 0, 0)
            elif ink_pixels[x, y] and a > VISIBLE_ALPHA:
                output_pixels[x, y] = (*INK, a)
            else:
                output_pixels[x, y] = (*spot_colour((r, g, b), family), a)
    return output


def make_reference_board() -> list[dict[str, object]]:
    source_dir = PACK / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    thumbs: list[Image.Image] = []
    for index, raw in enumerate(REFERENCE_IMAGES, start=1):
        path = Path(raw)
        if not path.is_file():
            raise RuntimeError(f"missing supplied style reference: {path}")
        image = Image.open(path).convert("RGB")
        records.append({
            "index": index,
            "originalBasename": path.name,
            "sha256": sha256(path),
            "pixels": list(image.size),
            "role": "secondary seascape ligne-claire reference" if index > 6 else "secondary interior/furniture ligne-claire reference",
        })
        copy = image.copy()
        copy.thumbnail((480, 320), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (500, 350), (246, 229, 183))
        tile.paste(copy, ((500 - copy.width) // 2, (350 - copy.height) // 2))
        thumbs.append(tile)
    board = Image.new("RGB", (1000, math.ceil(len(thumbs) / 2) * 350), (246, 229, 183))
    for index, thumb in enumerate(thumbs):
        board.paste(thumb, ((index % 2) * 500, (index // 2) * 350))
    board_path = source_dir / "supplied-ligne-claire-reference-board.jpg"
    board.save(board_path, quality=88, optimize=True)
    return records


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGB", size, (238, 230, 207))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(221, 211, 186))
    return image


def panel(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = min((size[0] - 24) / image.width, (size[1] - 24) / image.height, 6)
    shown = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))), Image.Resampling.NEAREST)
    base = checker(size)
    base.paste(shown, ((size[0] - shown.width) // 2, (size[1] - shown.height) // 2), shown)
    return base.convert("RGBA")


def contact_sheet(family: str, records: list[dict[str, object]]) -> Path:
    panel_size = (420, 300)
    header = 64
    row = 338
    sheet = Image.new("RGBA", (panel_size[0] * 2, header + row * len(records)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((16, 14), f"{family} — current / ligne-claire candidate", fill=INK, font=font)
    draw.text((16, 36), "Exact canvas, alpha, bounds and registration retained", fill=(29, 69, 98), font=font)
    for index, record in enumerate(records):
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        y = header + index * row
        sheet.paste(panel(source, panel_size), (0, y))
        sheet.paste(panel(candidate, panel_size), (panel_size[0], y))
        draw.text((10, y + panel_size[1] + 8), str(record["filename"]), fill=INK, font=font)
        draw.text((430, y + panel_size[1] + 8), f"candidate {str(record['candidateSha256'])[:12]}", fill=INK, font=font)
    path = EVIDENCE / f"{family}-current-vs-candidate.png"
    sheet.save(path, optimize=True)
    return path


def room_proof(records: list[dict[str, object]]) -> dict[str, object]:
    by_key = {(str(record["family"]), str(record["filename"])): record for record in records}
    background = Image.open(ROOT / "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/room-background-exact.png").convert("RGBA")

    def image_for(family: str, filename: str, candidate: bool) -> Image.Image:
        record = by_key[(family, filename)]
        key = "candidateFile" if candidate else "sourceFile"
        return Image.open(ROOT / str(record[key])).convert("RGBA")

    def paste(canvas: Image.Image, image: Image.Image, position: tuple[int, int]) -> None:
        canvas.alpha_composite(image, position)

    def draw_state(candidate: bool, broken: bool) -> Image.Image:
        canvas = background.copy()
        paste(canvas, image_for("pedal-bin", "bin-broken-overflowing.png" if broken else "bin-standard.png", candidate), (8, 149))
        paste(canvas, image_for("fridge", "fridge-broken-hinge-failed.png" if broken else "fridge-standard.png", candidate), (54, 130))
        paste(canvas, image_for("cabinet-a", "cabinet-a-lj-rj.png", candidate), (164, 130))
        paste(canvas, image_for("cabinet-b", "cabinet-b-lj-rj.png", candidate), (248, 130))
        paste(canvas, image_for("oven", "oven-broken.png" if broken else "oven-off.png", candidate), (332, 127))
        paste(canvas, image_for("sink", "sink-cabinet-broken-base.png" if broken else "sink-cabinet-standard.png", candidate), (416, 104))
        dishwasher_name = "dishwasher-broken-lj-re.png" if broken else "dishwasher-off-lj-re.png"
        paste(canvas, image_for("dishwasher", dishwasher_name, candidate), (497, 130))

        kettle = image_for("kettle", "kettle-broken.png" if broken else "kettle-off.png", candidate)
        if broken:
            kettle = kettle.crop((32, 32, 1008, 960)).resize((62, 59), Image.Resampling.LANCZOS)
            paste(canvas, kettle, (179, 82))
        else:
            kettle = kettle.crop((32, 32, 620, 572)).resize((56, 51), Image.Resampling.LANCZOS)
            paste(canvas, kettle, (182, 90))
        paste(canvas, image_for("toaster", "toaster-broken.png" if broken else "toaster-off.png", candidate), (250, 96))
        paste(canvas, image_for("mixing-bowl", "bowl-broken.png" if broken else "bowl-off.png", candidate), (418, 96))
        paste(canvas, image_for("table-chair", "table-chair.png", candidate), (680, 129))
        return canvas

    paths: dict[str, str] = {}
    for candidate in (False, True):
        for broken in (False, True):
            label = ("candidate" if candidate else "current") + ("-broken" if broken else "-standard")
            path = EVIDENCE / f"room-{label}.png"
            draw_state(candidate, broken).save(path, optimize=True)
            paths[label] = rel(path)

    scale = 1
    header = 44
    sheet = Image.new("RGBA", (772 * 2, header + 224 * 2), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((14, 12), "Complete kitchen proof — current / candidate · Standard and Broken", fill=INK, font=font)
    sheet.paste(Image.open(ROOT / paths["current-standard"]), (0, header))
    sheet.paste(Image.open(ROOT / paths["candidate-standard"]), (772, header))
    sheet.paste(Image.open(ROOT / paths["current-broken"]), (0, header + 224))
    sheet.paste(Image.open(ROOT / paths["candidate-broken"]), (772, header + 224))
    sheet_path = EVIDENCE / "complete-kitchen-current-vs-candidate.png"
    sheet.save(sheet_path, optimize=True)
    return {
        "file": rel(sheet_path),
        "sha256": sha256(sheet_path),
        "roomPixels": [772, 224],
        "columns": ["current", "candidate"],
        "rows": ["standard", "broken"],
        "individualProofs": {label: {"file": path, "sha256": sha256(ROOT / path)} for label, path in paths.items()},
        "note": "Review-only in-situ assembly on the exact inherited room and canonical bay datums; no room or runtime asset was changed.",
    }


def review_html(families: dict[str, list[dict[str, object]]], evidence: dict[str, dict[str, object]]) -> str:
    sections = []
    for family, records in families.items():
        cards = []
        for record in records:
            filename = html.escape(str(record["filename"]))
            asset_path = html.escape(f"assets/{family}--{filename}")
            source_url = html.escape(f"/activity-stories/repo/{record['sourceFile']}")
            cards.append(f'''<article class="pair"><h3>{filename}</h3><div class="compare"><figure><figcaption>Current</figcaption><div class="stage"><img src="{source_url}" alt="Current {filename}"></div></figure><figure><figcaption>Candidate</figcaption><div class="stage"><img src="{asset_path}" alt="Candidate {filename}"></div></figure></div><p>Canvas {record['pixels'][0]} × {record['pixels'][1]} · alpha exact · bounds {record['alphaBounds']}</p></article>''')
        sheet = evidence[family]
        sections.append(f'''<section><h2>{html.escape(family)}</h2><p><a href="assets/evidence--{Path(str(sheet['file'])).name}">Complete family contact sheet</a></p>{''.join(cards)}</section>''')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen ligne-claire sweep V1</title><style>:root{{--ink:#051824;--cream:#f6e5b7;--paper:#fff9e8;--blue:#235b85;--sea:#6dc9c2}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,section{{max-width:1240px;margin:auto;padding:28px}}header{{border-bottom:4px solid var(--ink)}}h1,h2,h3{{margin:.2em 0}}.status{{display:inline-block;background:#e84833;color:white;padding:7px 12px;border:2px solid var(--ink);border-radius:999px;font-weight:800}}section{{border-bottom:2px solid var(--ink)}}.pair{{background:var(--paper);border:2px solid var(--ink);padding:14px;margin:18px 0;box-shadow:5px 5px 0 var(--blue)}}.compare{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}figure{{margin:0}}figcaption{{font-weight:800;margin-bottom:7px}}.stage{{height:300px;display:grid;place-items:center;background-color:#eee6d0;background-image:linear-gradient(45deg,#d9cfb7 25%,transparent 25%),linear-gradient(-45deg,#d9cfb7 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#d9cfb7 75%),linear-gradient(-45deg,transparent 75%,#d9cfb7 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0}}img{{max-width:95%;max-height:95%;image-rendering:pixelated}}a{{color:#174562;font-weight:800}}@media(max-width:700px){{.compare{{grid-template-columns:1fr}}}}</style></head><body><header><span class="status">REJECTED · NEVER CURRENT</span><h1>Kitchen ligne-claire sweep V1</h1><p>This immutable historical pass was rejected because exact canvas and alpha were not enough to preserve all visible internal shapes: the fridge worktop lost definition and the oven read too flat. <a href="/keeper-review/kitchen-cabinet-ligne-claire-v2/">Review the cabinet-only V2 correction.</a></p><p>Sandwich-tomato V2 was the primary calibration; Frank's first six supplied original ligne-claire references guided architecture, furniture, contour rhythm and selective detail. Five later seascape panels extend the separate exterior recipe without adding exterior pixels here.</p><p>No source, approved asset, runtime identifier, state machine, animation timing, interaction, healing rule, room layout, anchor, pivot or collision was changed. V1 was never registered.</p><p><a href="assets/evidence--complete-kitchen-current-vs-candidate.png">Open the rejected current-versus-candidate room contact sheet</a></p></header>{''.join(sections)}</body></html>'''


def write_hashes() -> None:
    paths = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("\n".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}" for path in paths) + "\n")


def build() -> None:
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    PUBLIC_ASSETS.mkdir(parents=True, exist_ok=True)
    references = make_reference_board()

    records: list[dict[str, object]] = []
    families: dict[str, list[dict[str, object]]] = defaultdict(list)
    for spec in ASSETS:
        source_path = ROOT / spec["source"]
        if not source_path.is_file():
            raise RuntimeError(f"missing authority asset: {source_path}")
        source = Image.open(source_path).convert("RGBA")
        candidate = stylise(source, spec["family"])
        family_dir = CANDIDATES / spec["family"]
        family_dir.mkdir(parents=True, exist_ok=True)
        candidate_path = family_dir / spec["name"]
        candidate.save(candidate_path, optimize=True)
        source_alpha = source.getchannel("A")
        candidate_alpha = candidate.getchannel("A")
        if ImageChops.difference(source_alpha, candidate_alpha).getbbox() is not None:
            raise RuntimeError(f"alpha drift: {spec['family']}/{spec['name']}")
        record: dict[str, object] = {
            "family": spec["family"],
            "filename": spec["name"],
            "role": spec["role"],
            "sourceFile": rel(source_path),
            "sourceSha256": sha256(source_path),
            "candidateFile": rel(candidate_path),
            "candidateSha256": sha256(candidate_path),
            "pixels": list(source.size),
            "mode": "RGBA",
            "alphaSha256": hashlib.sha256(source_alpha.tobytes()).hexdigest(),
            "alphaBounds": list(alpha_bounds(source) or (0, 0, 0, 0)),
            "alphaExact": True,
            "canvasExact": True,
            "registrationExact": True,
        }
        records.append(record)
        families[spec["family"]].append(record)

    evidence: dict[str, dict[str, object]] = {}
    for family, family_records in families.items():
        path = contact_sheet(family, family_records)
        evidence[family] = {"file": rel(path), "sha256": sha256(path), "rows": len(family_records), "columns": 2}
    complete_room_proof = room_proof(records)

    inherited_effects = []
    for raw in INHERITED_EFFECTS:
        path = ROOT / raw
        image = Image.open(path)
        inherited_effects.append({"file": raw, "sha256": sha256(path), "pixels": list(image.size), "byteIdentical": True})
    contracts = [{"file": raw, "sha256": sha256(ROOT / raw), "unchanged": True} for raw in CONTRACT_FILES]

    tomato = ROOT / "art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/drafts/components/sandwich-tomato.png"
    recipe = ROOT / "docs/KITCHEN_LIGNE_CLAIRE_ART_RECIPE_2026-10-21.md"
    calibration_study = PACK / "source/imagegen-calibration-study.png"
    calibration_prompt = PACK / "source/imagegen-calibration-prompt.txt"
    if not calibration_study.is_file() or not calibration_prompt.is_file():
        raise RuntimeError("image-generation calibration evidence is missing")
    manifest = {
        "schema": "lighthouse-keeper/kitchen-ligne-claire-sweep@1",
        "set": SET,
        "datedDirectory": DATED,
        "created": "2026-10-21",
        "status": "immutable-reversible-rejected-review-candidate-not-approved-not-registered",
        "rejection": {
            "date": "2026-10-21",
            "reason": "Exact canvas and alpha did not preserve every visible internal shape strongly enough: the fridge worktop lost definition and the oven read too flat.",
            "supersededForReviewBy": "kitchen-cabinet-ligne-claire-v2",
        },
        "primaryVisualCalibration": {"file": rel(tomato), "sha256": sha256(tomato), "version": 2},
        "secondaryReferences": references,
        "recipe": {"file": rel(recipe), "sha256": sha256(recipe)},
        "calibrationStudy": {
            "mode": "built-in image generation",
            "role": "non-authoritative line/palette study only; not an asset candidate",
            "promptFile": rel(calibration_prompt),
            "promptSha256": sha256(calibration_prompt),
            "outputFile": rel(calibration_study),
            "outputSha256": sha256(calibration_study),
            "structuralAuthority": False,
            "candidateSource": False,
        },
        "palette": ["#%02x%02x%02x" % colour for colour in PALETTE],
        "derivation": "exact source RGBA canvas and alpha bytes; RGB-only CIELAB nearest shared spot palette; exact tomato-V2 ink for original decisive dark lines and an inside-only silhouette contour; no dithering; lossless PNG",
        "assets": records,
        "evidence": evidence,
        "completeRoomProof": complete_room_proof,
        "inheritedEffects": inherited_effects,
        "unchangedContracts": contracts,
        "checks": {
            "allAssetsCoveredByContactSheets": True,
            "sourceAndCandidateHashesRecorded": True,
            "sourceBytesUntouched": True,
            "candidateCanvasExact": True,
            "candidateAlphaExact": True,
            "candidateBoundsExact": True,
            "transparentPaddingExact": True,
            "anchorsPivotsCollisionsInheritedUnchanged": True,
            "animationFrameCountsAndTimingInheritedUnchanged": True,
            "movementInteractionHealingInheritedUnchanged": True,
            "roomLayoutChanged": False,
            "runtimeChanged": False,
            "claudeImplementationChanged": False,
            "registrationPerformed": False,
            "currentSelectorChanged": False,
        },
        "rollback": "Discard art/drafts/kitchen-ligne-claire-sweep-2026-10-21-v1 and its keeper-review set. No source/current/runtime bytes or selectors were changed.",
        "approvalRequiredFor": "any registration, selector update, Final copy or runtime wiring",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({
        "set": SET,
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
        "source": "manifest.json",
    }, indent=2) + "\n")

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC_ASSETS.mkdir(parents=True, exist_ok=True)
    for family, family_records in families.items():
        for record in family_records:
            shutil.copy2(ROOT / str(record["candidateFile"]), PUBLIC_ASSETS / f"{family}--{record['filename']}")
    for item in evidence.values():
        shutil.copy2(ROOT / str(item["file"]), PUBLIC_ASSETS / f"evidence--{Path(str(item['file'])).name}")
    shutil.copy2(ROOT / str(complete_room_proof["file"]), PUBLIC_ASSETS / f"evidence--{Path(str(complete_room_proof['file'])).name}")
    for item in complete_room_proof["individualProofs"].values():
        shutil.copy2(ROOT / str(item["file"]), PUBLIC_ASSETS / f"evidence--{Path(str(item['file'])).name}")
    (PUBLIC / "index.html").write_text(review_html(families, evidence))
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
    write_hashes()
    verify()
    print(f"Built {SET}: {len(records)} geometry-locked candidates in {len(families)} families")


def verify() -> None:
    manifest_path = PACK / "manifest.json"
    if not manifest_path.is_file():
        raise RuntimeError("manifest missing")
    manifest = json.loads(manifest_path.read_text())
    if manifest["set"] != SET or "not-approved" not in manifest["status"]:
        raise RuntimeError("review status/identity drift")
    if manifest["checks"]["registrationPerformed"] or manifest["checks"]["currentSelectorChanged"]:
        raise RuntimeError("candidate was registered or selected")
    if len(manifest["assets"]) != len(ASSETS):
        raise RuntimeError("asset coverage mismatch")
    for record in manifest["assets"]:
        source_path = ROOT / record["sourceFile"]
        candidate_path = ROOT / record["candidateFile"]
        if sha256(source_path) != record["sourceSha256"] or sha256(candidate_path) != record["candidateSha256"]:
            raise RuntimeError(f"asset hash drift: {record['family']}/{record['filename']}")
        source = Image.open(source_path).convert("RGBA")
        candidate = Image.open(candidate_path).convert("RGBA")
        if source.size != candidate.size or source.mode != candidate.mode:
            raise RuntimeError(f"canvas drift: {record['family']}/{record['filename']}")
        if ImageChops.difference(source.getchannel("A"), candidate.getchannel("A")).getbbox() is not None:
            raise RuntimeError(f"alpha drift: {record['family']}/{record['filename']}")
        if list(alpha_bounds(source) or (0, 0, 0, 0)) != record["alphaBounds"]:
            raise RuntimeError(f"bounds drift: {record['family']}/{record['filename']}")
        colours = {pixel[:3] for pixel in candidate.getdata() if pixel[3] > VISIBLE_ALPHA}
        if not colours.issubset(set(PALETTE)):
            raise RuntimeError(f"non-spot colour: {record['family']}/{record['filename']}")
    for record in manifest["inheritedEffects"]:
        if sha256(ROOT / record["file"]) != record["sha256"]:
            raise RuntimeError(f"inherited effect changed: {record['file']}")
    for record in manifest["unchangedContracts"]:
        if sha256(ROOT / record["file"]) != record["sha256"]:
            raise RuntimeError(f"contract changed: {record['file']}")
    for family, item in manifest["evidence"].items():
        path = ROOT / item["file"]
        if sha256(path) != item["sha256"]:
            raise RuntimeError(f"contact sheet drift: {family}")
    room = manifest["completeRoomProof"]
    if sha256(ROOT / room["file"]) != room["sha256"]:
        raise RuntimeError("complete room contact sheet drift")
    for label, item in room["individualProofs"].items():
        if sha256(ROOT / item["file"]) != item["sha256"]:
            raise RuntimeError(f"room proof drift: {label}")
    recipe = manifest["recipe"]
    # V1 is rejected immutable provenance, while the project recipe is a
    # deliberately living document that records lessons from later gates.
    # Pin V1's original recipe declaration instead of requiring the living
    # file to remain frozen at its pre-rejection bytes.
    if recipe != {
        "file": "docs/KITCHEN_LIGNE_CLAIRE_ART_RECIPE_2026-10-21.md",
        "sha256": "694a06d1358da96eebfb1f38e4c71906e84ad64d2b2dfd844ca27d3939c7c796",
    }:
        raise RuntimeError("V1 recipe provenance drift")
    study = manifest["calibrationStudy"]
    if sha256(ROOT / study["promptFile"]) != study["promptSha256"]:
        raise RuntimeError("calibration prompt drift")
    if sha256(ROOT / study["outputFile"]) != study["outputSha256"]:
        raise RuntimeError("calibration study drift")
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["register"] or register["promote"] or register["currentSelectorChanges"]:
        raise RuntimeError("registration guard is not closed")
    expected_hashes = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    hashes_path = PACK / "HASHES.sha256"
    if hashes_path.is_file() and hashes_path.read_text().splitlines() != expected_hashes:
        raise RuntimeError("HASHES.sha256 is stale")
    print(f"Verified {SET}: {len(manifest['assets'])} candidates, exact alpha/canvas, no registration")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        verify()
    else:
        build()


if __name__ == "__main__":
    main()
