#!/usr/bin/env python3
"""Build the Kitchen v8 Step-1 v2 cooker-correction review sheets.

This script makes a proportional 2x generation guide and, after generation,
normalises the three-piece plate to 1:1 game scale.  It never builds a room or
creates production item sprites.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCES = HERE / "sources"
OUTPUTS = HERE / "outputs"

GUIDE_SIZE = (1536, 768)
PLATE_SIZE = (900, 384)
SOURCE_BASELINE_Y = 710
PLATE_BASELINE_Y = SOURCE_BASELINE_Y // 2
THREE_SCALE_SIZE = (1900, 1660)
SAGE_SWATCH = "#96B0A5"
DUCK_EGG_SWATCH = "#A8CEC6"

# Historical generation envelopes for the inherited sink/dresser and the
# superseded narrow-cooker guide. The selected corrected cooker source is
# normalised into the authoritative 126 × 252 px envelope below; the old guide
# is retained only to keep the v2 review build reproducible.
GUIDE_RECTS = {
    "belfast_sink_cabinet": (100, 250, 436, 710),
    "painted_dresser": (620, 38, 920, 710),
    "small_cream_cooker": (1120, 350, 1322, 710),
}

# Visible game-space envelopes derived from section 10b/10a-3.  Each final
# review canvas is exact, but contains only review art until Frank approves.
GAME_ENVELOPES = {
    "belfast_sink_cabinet": (168, 211),   # x622–790; taps no higher than y274; base y485
    "painted_dresser": (150, 355),        # x1555–1705; about y130–485
    "small_cream_cooker": (126, 252),     # one standard unit; eye-level hood/grill included
}

SINGLE_GUIDE_RECTS = {
    "belfast_sink_cabinet": (176, 520, 848, 1364),
    "painted_dresser": (262, 172, 762, 1356),
    "small_cream_cooker": (302, 348, 722, 1356),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Verdana Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Verdana.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def build_guide() -> Path:
    SOURCES.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", GUIDE_SIZE, (247, 242, 228, 255))
    draw = ImageDraw.Draw(image)
    draw.line((48, SOURCE_BASELINE_Y, GUIDE_SIZE[0] - 48, SOURCE_BASELINE_Y), fill=(82, 85, 82, 255), width=3)
    for rect in GUIDE_RECTS.values():
        x0, y0, x1, y1 = rect
        # Dashed technical envelope: generation must replace, not decorate, it.
        dash = 14
        for x in range(x0, x1, dash * 2):
            draw.line((x, y0, min(x + dash, x1), y0), fill=(164, 164, 154, 255), width=2)
            draw.line((x, y1, min(x + dash, x1), y1), fill=(164, 164, 154, 255), width=2)
        for y in range(y0, y1, dash * 2):
            draw.line((x0, y, x0, min(y + dash, y1)), fill=(164, 164, 154, 255), width=2)
            draw.line((x1, y, x1, min(y + dash, y1)), fill=(164, 164, 154, 255), width=2)
    path = SOURCES / "three-piece-proportion-guide-2x.png"
    image.save(path, optimize=True)

    # Dedicated portrait guides enforce the three different real-world aspect
    # ratios more reliably than a single wide generation plate.
    for name, rect in SINGLE_GUIDE_RECTS.items():
        guide = Image.new("RGBA", (1024, 1536), (247, 242, 228, 255))
        gd = ImageDraw.Draw(guide)
        x0, y0, x1, y1 = rect
        gd.line((96, y1, 928, y1), fill=(82, 85, 82, 255), width=3)
        dash = 14
        for x in range(x0, x1, dash * 2):
            gd.line((x, y0, min(x + dash, x1), y0), fill=(164, 164, 154, 255), width=2)
            gd.line((x, y1, min(x + dash, x1), y1), fill=(164, 164, 154, 255), width=2)
        for y in range(y0, y1, dash * 2):
            gd.line((x0, y, x0, min(y + dash, y1)), fill=(164, 164, 154, 255), width=2)
            gd.line((x1, y, x1, min(y + dash, y1)), fill=(164, 164, 154, 255), width=2)
        guide.save(SOURCES / f"{name}-proportion-guide-4x.png", optimize=True)
    return path


def normalise_plate(raw: Image.Image) -> Image.Image:
    raw = raw.convert("RGBA")
    target_ratio = GUIDE_SIZE[0] / GUIDE_SIZE[1]
    ratio = raw.width / raw.height
    if ratio > target_ratio:
        crop_w = round(raw.height * target_ratio)
        left = (raw.width - crop_w) // 2
        raw = raw.crop((left, 0, left + crop_w, raw.height))
    elif ratio < target_ratio:
        crop_h = round(raw.width / target_ratio)
        top = (raw.height - crop_h) // 2
        raw = raw.crop((0, top, raw.width, top + crop_h))
    return raw.resize(PLATE_SIZE, Image.Resampling.LANCZOS)


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, (239, 235, 222, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(220, 219, 210, 255))
    return image


def alpha_crop(image: Image.Image) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("reference has no visible pixels")
    return image.crop(bbox)


def fit_height(image: Image.Image, height: int) -> Image.Image:
    width = max(1, round(image.width * height / image.height))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def prepare_asset(raw_path: Path, canvas_size: tuple[int, int], gutter: int = 2) -> Image.Image:
    source = Image.open(raw_path).convert("RGBA")
    # Built-in generation sometimes leaves a very low-alpha atmospheric halo
    # despite the prompt.  It is not part of the object and is forbidden by the
    # style test, so discard alpha below 32 before computing the silhouette.
    alpha = source.getchannel("A")
    clean_alpha = alpha.point(lambda value: value if value >= 32 else 0)
    source.putalpha(clean_alpha)
    source = alpha_crop(source)
    # A transparent edge keeps the review candidates isolated without changing
    # the declared game-space canvas.  At 2x the gutter scales to four pixels.
    inner_size = (canvas_size[0] - gutter * 2, canvas_size[1] - gutter * 2)
    ratio = min(inner_size[0] / source.width, inner_size[1] / source.height)
    fitted = source.resize((max(1, round(source.width * ratio)), max(1, round(source.height * ratio))), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(fitted, ((canvas.width - fitted.width) // 2, canvas.height - fitted.height - gutter))
    return canvas


def scaled(image: Image.Image, factor: float, resample: Image.Resampling) -> Image.Image:
    return image.resize(
        (max(1, round(image.width * factor)), max(1, round(image.height * factor))),
        resample,
    )


def draw_scale_row(
    sheet: Image.Image,
    draw: ImageDraw.ImageDraw,
    *,
    title: str,
    note: str,
    pieces: list[tuple[str, Image.Image]],
    keeper: Image.Image,
    keeper_sole_y: int,
    baseline: int,
    centres: list[int],
    label_y: int,
) -> None:
    draw.text((42, label_y), title, font=font(25, True), fill=(250, 215, 116, 255))
    draw.text((42, label_y + 35), note, font=font(15), fill=(190, 213, 219, 255))
    draw.line((42, baseline, THREE_SCALE_SIZE[0] - 42, baseline), fill=(99, 121, 127, 255), width=2)

    labels = [label for label, _ in pieces] + ["PRIME KEEPER"]
    images = [image for _, image in pieces] + [keeper]
    for index, (label, image, centre) in enumerate(zip(labels, images, centres)):
        if index == len(images) - 1:
            y = baseline - keeper_sole_y
        else:
            y = baseline - image.height
        x = centre - image.width // 2
        sheet.alpha_composite(image, (x, y))
        label_box = draw.textbbox((0, 0), label, font=font(13, True))
        label_width = label_box[2] - label_box[0]
        draw.text((centre - label_width // 2, baseline + 13), label, font=font(13, True), fill=(225, 231, 222, 255))


def build_three_scale_review(
    assets: dict[str, Image.Image],
    source_paths: dict[str, Path],
    keeper: Image.Image,
) -> Path:
    sheet = Image.new("RGBA", THREE_SCALE_SIZE, (18, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((42, 26), "KITCHEN v8 UK COTTAGE · THREE-SCALE REVIEW GATE v2", font=font(31, True), fill=(250, 238, 207, 255))
    draw.text(
        (42, 70),
        "The same three Step-1 candidates beside the unchanged Prime Keeper · no room build · review only",
        font=font(17),
        fill=(190, 213, 219, 255),
    )

    # The existing painted colour is sampled from the candidate fronts.  The
    # second swatch is a deliberately clearer, bluer duck-egg alternative.
    draw.text((1420, 24), "COLOUR DECISION", font=font(14, True), fill=(250, 215, 116, 255))
    for x, colour, label in [
        (1420, SAGE_SWATCH, f"CURRENT SAGE  {SAGE_SWATCH}"),
        (1640, DUCK_EGG_SWATCH, f"DUCK-EGG  {DUCK_EGG_SWATCH}"),
    ]:
        draw.rounded_rectangle((x, 51, x + 185, 98), radius=7, fill=colour, outline=(232, 235, 222, 255), width=2)
        draw.text((x, 105), label, font=font(12, True), fill=(220, 228, 220, 255))

    order = ["belfast_sink_cabinet", "painted_dresser", "small_cream_cooker"]
    display_names = {
        "belfast_sink_cabinet": "BELFAST SINK",
        "painted_dresser": "PAINTED DRESSER",
        "small_cream_cooker": "OLD-SCHOOL COOKER",
    }

    # Close-up assets are reduced directly from the high-resolution selected
    # sources into doubled game envelopes.  They are not enlarged 1x pixels.
    close_up = [
        (
            display_names[name],
            prepare_asset(
                source_paths[name],
                (GAME_ENVELOPES[name][0] * 2, GAME_ENVELOPES[name][1] * 2),
                gutter=4,
            ),
        )
        for name in order
    ]
    keeper_2x = scaled(keeper, 2.0, Image.Resampling.NEAREST)
    draw_scale_row(
        sheet,
        draw,
        title="A · CLOSE-UP 2×",
        note="High-resolution review: line confidence, material character and restraint",
        pieces=close_up,
        keeper=keeper_2x,
        keeper_sole_y=632,
        baseline=900,
        centres=[225, 635, 1010, 1505],
        label_y=148,
    )

    room = [(display_names[name], assets[name]) for name in order]
    draw_scale_row(
        sheet,
        draw,
        title="B · ROOM 1:1",
        note="Normal play view: exact candidate envelopes; Prime source cell unchanged",
        pieces=room,
        keeper=keeper,
        keeper_sole_y=316,
        baseline=1358,
        centres=[475, 750, 985, 1360],
        label_y=964,
    )

    # Tower review is a true 1/8 reduction from the reviewed 1x candidates.
    # Wide spacing and a light backing panel make this a silhouette/colour-block
    # test without falsely magnifying the objects.
    tower = [(display_names[name], scaled(assets[name], 0.125, Image.Resampling.LANCZOS)) for name in order]
    keeper_eighth = scaled(keeper, 0.125, Image.Resampling.LANCZOS)
    draw.rounded_rectangle((350, 1477, 1550, 1629), radius=12, fill=(237, 232, 214, 255), outline=(111, 128, 130, 255), width=2)
    draw_scale_row(
        sheet,
        draw,
        title="C · TOWER ≈1/8",
        note="Exact 12.5% reduction: judge only silhouette and colour blocks; fine detail should disappear",
        pieces=tower,
        keeper=keeper_eighth,
        keeper_sole_y=40,
        baseline=1569,
        centres=[580, 820, 1050, 1320],
        label_y=1414,
    )
    # Labels in the pale tower panel need dark ink.
    draw.rectangle((350, 1584, 1550, 1629), fill=(237, 232, 214, 255))
    for centre, label in zip([580, 820, 1050, 1320], ["BELFAST SINK", "PAINTED DRESSER", "OLD-SCHOOL COOKER", "PRIME KEEPER"]):
        label_box = draw.textbbox((0, 0), label, font=font(13, True))
        label_width = label_box[2] - label_box[0]
        draw.text((centre - label_width // 2, 1590), label, font=font(13, True), fill=(31, 47, 54, 255))

    draw.text(
        (42, 1630),
        "COOKER CONTRACT: its single indicator is the status lamp — engine-lit steady green (working), flashing red (broken); no second lamp.",
        font=font(14, True),
        fill=(190, 213, 219, 255),
    )
    path = OUTPUTS / "kitchen-v8-three-scale-review.png"
    sheet.convert("RGB").save(path, optimize=True)
    return path


def build_cooker_revision_comparison(cooker: Image.Image, keeper: Image.Image) -> Path:
    """Show the immutable rejected cooker beside this reversible v2 draft."""
    previous_path = ROOT / "review/kitchen-proof-v8-style-test/outputs/small_cream_cooker-1x.png"
    previous = Image.open(previous_path).convert("RGBA")
    width, height = 1400, 620
    sheet = Image.new("RGBA", (width, height), (18, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((38, 28), "KITCHEN v8 · COOKER CORRECTION · 1:1", font=font(30, True), fill=(250, 238, 207, 255))
    draw.text(
        (38, 72),
        "Rejected narrow draft retained unchanged · new single-unit old-school gas cooker · range not drawn",
        font=font(17),
        fill=(190, 213, 219, 255),
    )
    baseline = 526
    draw.line((38, baseline, width - 38, baseline), fill=(99, 121, 127, 255), width=2)

    entries = [
        (260, previous, previous.height, "REJECTED · 101 × 180", "too narrow; no grill"),
        (660, cooker, cooker.height, "v2 DRAFT · 126 × 252", "one standard unit; eye-level grill"),
        (1080, keeper, 316, "PRIME KEEPER · EXACT 1:1", "source cell unchanged"),
    ]
    for centre, image, sole_or_height, title, note in entries:
        y = baseline - sole_or_height
        sheet.alpha_composite(image, (centre - image.width // 2, y))
        title_box = draw.textbbox((0, 0), title, font=font(15, True))
        title_width = title_box[2] - title_box[0]
        draw.text((centre - title_width // 2, 548), title, font=font(15, True), fill=(238, 204, 111, 255))
        note_box = draw.textbbox((0, 0), note, font=font(13))
        note_width = note_box[2] - note_box[0]
        draw.text((centre - note_width // 2, 576), note, font=font(13), fill=(169, 194, 201, 255))

    path = OUTPUTS / "kitchen-v8-cooker-correction-v2.png"
    sheet.convert("RGB").save(path, optimize=True)
    return path


def finalise(sink_path: Path, dresser_path: Path, cooker_path: Path) -> tuple[Path, Path, Path, Path]:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    assets = {
        "belfast_sink_cabinet": prepare_asset(sink_path, GAME_ENVELOPES["belfast_sink_cabinet"]),
        "painted_dresser": prepare_asset(dresser_path, GAME_ENVELOPES["painted_dresser"]),
        "small_cream_cooker": prepare_asset(cooker_path, GAME_ENVELOPES["small_cream_cooker"]),
    }
    for name, asset in assets.items():
        asset.save(OUTPUTS / f"{name}-1x.png", optimize=True)
    plate = Image.new("RGBA", PLATE_SIZE, (0, 0, 0, 0))
    plate_positions = {
        "belfast_sink_cabinet": 45,
        "painted_dresser": 320,
        "small_cream_cooker": 620,
    }
    for name, asset in assets.items():
        plate.alpha_composite(asset, (plate_positions[name], PLATE_BASELINE_Y - asset.height))
    plate_path = OUTPUTS / "three-new-cottage-pieces-1x.png"
    plate.save(plate_path, optimize=True)

    width, height = 1700, 650
    sheet = Image.new("RGBA", (width, height), (18, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((34, 24), "KITCHEN v8 UK COTTAGE · STEP 1 STYLE TEST v2", font=font(30, True), fill=(250, 238, 207, 255))
    draw.text((34, 67), "Three new pieces at 1:1 game scale · matt / one shadow tone / no gloss · review only", font=font(18), fill=(190, 213, 219, 255))

    baseline = 552
    plate_bg = checker(PLATE_SIZE)
    plate_bg.alpha_composite(plate)
    sheet.alpha_composite(plate_bg, (32, baseline - PLATE_BASELINE_Y))

    # Historical V7 is style-only. Show it at a consistent comparison height,
    # plus the exact Prime cell; it is not a geometry authority.
    v7_path = ROOT / "review/kitchen-proof-v3-rebuild/sources/v7-oven-authority.png"
    v7 = fit_height(alpha_crop(Image.open(v7_path).convert("RGBA")), 180)
    v7_x = 1050
    sheet.alpha_composite(v7, (v7_x, baseline - v7.height))

    keeper_path = ROOT / "review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png"
    keeper = Image.open(keeper_path).convert("RGBA")
    keeper_x = 1410
    keeper_y = baseline - 316
    sheet.alpha_composite(keeper, (keeper_x, keeper_y))

    label_y = 574
    labels = [
        (68, "BELFAST SINK CABINET"),
        (343, "PAINTED DRESSER"),
        (633, "OLD-SCHOOL CREAM COOKER"),
        (1020, "V7 OVEN · STYLE AUTHORITY"),
        (1395, "PRIME KEEPER · EXACT 1:1"),
    ]
    for x, label in labels:
        draw.text((x, label_y), label, font=font(15, True), fill=(238, 204, 111, 255))
    draw.text((1020, 602), "normalised for line/style comparison only", font=font(13), fill=(169, 194, 201, 255))
    draw.text((1395, 602), "source cell unchanged; sole datum aligned", font=font(13), fill=(169, 194, 201, 255))

    # Shared baseline makes relative scale obvious and catches floating feet.
    draw.line((32, baseline, width - 32, baseline), fill=(102, 122, 127, 255), width=2)
    sheet_path = OUTPUTS / "kitchen-v8-three-piece-style-test.png"
    sheet.convert("RGB").save(sheet_path, optimize=True)
    scale_path = build_three_scale_review(
        assets,
        {
            "belfast_sink_cabinet": sink_path,
            "painted_dresser": dresser_path,
            "small_cream_cooker": cooker_path,
        },
        keeper,
    )
    correction_path = build_cooker_revision_comparison(assets["small_cream_cooker"], keeper)
    return plate_path, sheet_path, scale_path, correction_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sink", type=Path)
    parser.add_argument("--dresser", type=Path)
    parser.add_argument("--cooker", type=Path)
    args = parser.parse_args()
    print(build_guide())
    supplied = [args.sink, args.dresser, args.cooker]
    if any(supplied):
        if not all(supplied):
            parser.error("--sink, --dresser and --cooker are required together")
        for path in finalise(args.sink, args.dresser, args.cooker):
            print(path)


if __name__ == "__main__":
    main()
