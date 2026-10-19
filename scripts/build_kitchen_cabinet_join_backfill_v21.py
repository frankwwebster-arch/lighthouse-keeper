#!/usr/bin/env python3
"""Build a reversible dynamic cabinet-join backfill proof without editing assets."""

from __future__ import annotations

import hashlib
import json
import shutil
import statistics
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-cabinet-join-backfill-2026-10-19-v21"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-cabinet-join-backfill-v21"
ASSETS = PUBLIC / "assets"
BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"
RUN = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"
SINK = ROOT / "art/raw/kitchen-sink-smooth-join-2026-10-19-v19/sink-cabinet-standard.png"

ROOM = (772, 224)
RUN_CELL_ORIGIN = (164, 130)
RUN_BODY = (168, 134, 336, 208)
SINK_BODY_DEFAULT_X = 336
SINK_CELL_OFFSET = (-4, -30)
BODY_HEIGHT = 74
BACKFILL_TOP_INSET = 11
UNDERLAP = 3
MAX_GAP = 8
MIN_OVERLAP = -6
TEMPLATE_WIDTH = UNDERLAP * 2 + MAX_GAP


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def row_palette(run: Image.Image, shadow: bool) -> list[tuple[int, int, int, int]]:
    """Derive one structural colour per cabinet row from exact approved V11."""
    palette: list[tuple[int, int, int, int]] = []
    last = (3, 57, 79, 255)
    for body_y in range(BODY_HEIGHT):
        cell_y = body_y + 4
        samples = [
            run.getpixel((x, cell_y))
            for x in range(20, 156)
            if run.getpixel((x, cell_y))[3] >= 245
        ]
        if samples:
            rgb = tuple(round(statistics.median(pixel[channel] for pixel in samples)) for channel in range(3))
            last = (*rgb, 255)
        r, g, b, _ = last
        if shadow:
            # A recessed join should be visibly structural but never read as
            # pale wall. Preserve hue while lowering value by roughly 24%.
            r, g, b = (round(r * 0.76), round(g * 0.76), round(b * 0.76))
        palette.append((r, g, b, 255))
    return palette


def template(palette: list[tuple[int, int, int, int]]) -> Image.Image:
    visible_palette = palette[BACKFILL_TOP_INSET:]
    image = Image.new("RGBA", (TEMPLATE_WIDTH, len(visible_palette)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for y, colour in enumerate(visible_palette):
        draw.line((0, y, TEMPLATE_WIDTH - 1, y), fill=colour)
    return image


def backfill_bounds(sink_body_x: int) -> tuple[int, int, int, int] | None:
    gap = sink_body_x - RUN_BODY[2]
    if gap < MIN_OVERLAP or gap > MAX_GAP:
        return None
    return (RUN_BODY[2] - UNDERLAP, RUN_BODY[1] + BACKFILL_TOP_INSET, sink_body_x + UNDERLAP, RUN_BODY[3])


def compose(
    background: Image.Image,
    run: Image.Image,
    sink: Image.Image,
    fill: Image.Image | None,
    sink_body_x: int = SINK_BODY_DEFAULT_X,
) -> Image.Image:
    room = background.copy()
    bounds = backfill_bounds(sink_body_x) if fill is not None else None
    if bounds:
        left, top, right, bottom = bounds
        source_width = right - left
        room.alpha_composite(fill.crop((0, 0, source_width, bottom - top)), (left, top))
    room.alpha_composite(run, RUN_CELL_ORIGIN)
    room.alpha_composite(sink, (sink_body_x + SINK_CELL_OFFSET[0], RUN_BODY[1] + SINK_CELL_OFFSET[1]))
    return room


def focus(room: Image.Image) -> Image.Image:
    return room.crop((312, 124, 360, 216))


def build_page(catalogue: dict) -> str:
    template_path = ROOT / "scripts/templates/kitchen_cabinet_join_backfill_v21.html"
    return template_path.read_text().replace("__DATA__", json.dumps(catalogue, separators=(",", ":")))


def main() -> None:
    for directory in (RAW, DRAFT, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (RAW, DRAFT, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    background = Image.open(BACKGROUND).convert("RGBA")
    run = Image.open(RUN).convert("RGBA")
    sink = Image.open(SINK).convert("RGBA")
    if background.size != ROOM or run.size != (176, 82) or sink.size != (92, 108):
        raise RuntimeError("Join-backfill authority geometry changed")

    matched = template(row_palette(run, shadow=False))
    shadow = template(row_palette(run, shadow=True))
    without = compose(background, run, sink, None)
    with_matched = compose(background, run, sink, matched)
    with_shadow = compose(background, run, sink, shadow)
    gap_six = compose(background, run, sink, matched, SINK_BODY_DEFAULT_X + 6)
    gap_nine = compose(background, run, sink, matched, SINK_BODY_DEFAULT_X + 9)

    outputs = {
        "room-background-exact.png": background,
        "cabinet-run-v11-exact.png": run,
        "sink-cabinet-v19-exact.png": sink,
        "join-backfill-matched-template.png": matched,
        "join-backfill-shadow-template.png": shadow,
        "room-default-without-backfill.png": without,
        "room-default-matched-backfill.png": with_matched,
        "room-default-shadow-backfill.png": with_shadow,
        "focus-without-backfill.png": focus(without),
        "focus-matched-backfill.png": focus(with_matched),
        "focus-shadow-backfill.png": focus(with_shadow),
        "room-six-pixel-gap-backfilled.png": gap_six,
        "room-nine-pixel-gap-auto-disabled.png": gap_nine,
    }
    for name, image in outputs.items():
        save(image, RAW / name)
        shutil.copyfile(RAW / name, ASSETS / name)
    # Preserve the three authorities byte-for-byte, not merely pixel-for-pixel.
    for name, source in {
        "room-background-exact.png": BACKGROUND,
        "cabinet-run-v11-exact.png": RUN,
        "sink-cabinet-v19-exact.png": SINK,
    }.items():
        shutil.copyfile(source, RAW / name)
        shutil.copyfile(source, ASSETS / name)

    catalogue = {
        "set": SET,
        "version": 21,
        "status": "dynamic-join-backfill-awaiting-visual-review",
        "authorities": {
            "background": {"file": "room-background-exact.png", "source": str(BACKGROUND.relative_to(ROOT)), "byteIdentical": True},
            "leftAsset": {"file": "cabinet-run-v11-exact.png", "source": str(RUN.relative_to(ROOT)), "byteIdentical": True, "cellOrigin": list(RUN_CELL_ORIGIN), "bodyBounds": list(RUN_BODY)},
            "rightAsset": {"file": "sink-cabinet-v19-exact.png", "source": str(SINK.relative_to(ROOT)), "byteIdentical": True, "defaultBodyX": SINK_BODY_DEFAULT_X, "bodySize": [84, 74], "cellOffsetFromBody": list(SINK_CELL_OFFSET)},
        },
        "backfill": {
            "drawOrder": ["room-background", "join-backfill", "cabinet-assets"],
            "underlapPixelsPerSide": UNDERLAP,
            "maximumBridgedGapPixels": MAX_GAP,
            "minimumAllowedOverlapPixels": MIN_OVERLAP,
            "verticalRule": "intersection-of-neighbour-body-bounds",
            "startsBelowWorktopPixels": BACKFILL_TOP_INSET,
            "defaultBounds": list(backfill_bounds(SINK_BODY_DEFAULT_X)),
            "matchedTemplate": "join-backfill-matched-template.png",
            "shadowTemplate": "join-backfill-shadow-template.png",
            "derivedFromExactV11Rows": True,
            "assetPixelsChanged": False,
        },
        "interaction": {
            "sinkDraggableHorizontally": True,
            "sinkBodyXRange": [324, 360],
            "styleSelectable": ["matched", "shadow"],
            "backfillToggle": True,
            "autoDisableBeyondGapPixels": MAX_GAP,
        },
        "outputs": {name: sha(RAW / name) for name in outputs},
        "media": list(outputs),
        "boundaries": {"v11Changed": False, "v19Changed": False, "v20Changed": False, "backgroundChanged": False, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    registered = [BACKGROUND, RUN, SINK, catalogue_path, *[RAW / name for name in outputs]]
    register = {
        "set": SET,
        "status": "reversible-unapproved-unpromoted",
        "files": {str(path.relative_to(ROOT)): sha(path) for path in registered},
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print("Built Kitchen Cabinet Join Backfill V21: exact assets plus dynamic behind-only seam masking")


if __name__ == "__main__":
    main()
