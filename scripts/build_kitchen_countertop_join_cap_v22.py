#!/usr/bin/env python3
"""Build a reversible dynamic countertop join cap without editing source assets."""

from __future__ import annotations

import hashlib
import json
import shutil
import statistics
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-countertop-join-cap-v22"
BATCH = "kitchen-countertop-join-cap-2026-10-19-v22"
RAW = ROOT / "art/raw" / BATCH
DRAFT = ROOT / "art/drafts" / BATCH
PUBLIC = ROOT / "public/keeper-review/kitchen-countertop-join-cap-v22"
ASSETS = PUBLIC / "assets"
BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"
RUN = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"
SINK = ROOT / "art/raw/kitchen-sink-smooth-join-2026-10-19-v19/sink-cabinet-standard.png"
V21_ROOM = ROOT / "art/raw/kitchen-cabinet-join-backfill-2026-10-19-v21/room-default-matched-backfill.png"

ROOM = (772, 224)
RUN_CELL_ORIGIN = (164, 130)
RUN_BODY = (168, 134, 336, 208)
SINK_BODY_DEFAULT_X = 336
SINK_CELL_OFFSET = (-4, -30)
BODY_HEIGHT = 74
BODY_FILL_TOP = 145
BODY_UNDERLAP = 3
CAP_UNDERLAP = 8
CAP_TOP = 134
CAP_BOTTOM = 146
MAX_GAP = 8
MIN_OVERLAP = -6
BODY_TEMPLATE_WIDTH = BODY_UNDERLAP * 2 + MAX_GAP
CAP_TEMPLATE_WIDTH = CAP_UNDERLAP * 2 + MAX_GAP


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def median_rgb(pixels: list[tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    return (*tuple(round(statistics.median(pixel[channel] for pixel in pixels)) for channel in range(3)), 255)


def body_palette(run: Image.Image) -> list[tuple[int, int, int, int]]:
    palette: list[tuple[int, int, int, int]] = []
    last = (3, 57, 79, 255)
    for body_y in range(BODY_HEIGHT):
        cell_y = body_y + 4
        samples = [run.getpixel((x, cell_y)) for x in range(20, 156) if run.getpixel((x, cell_y))[3] >= 245]
        if samples:
            last = median_rgb(samples)
        palette.append(last)
    return palette


def row_template(palette: list[tuple[int, int, int, int]], width: int) -> Image.Image:
    image = Image.new("RGBA", (width, len(palette)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for y, colour in enumerate(palette):
        draw.line((0, y, width - 1, y), fill=colour)
    return image


def body_bounds(sink_body_x: int) -> tuple[int, int, int, int] | None:
    gap = sink_body_x - RUN_BODY[2]
    if gap < MIN_OVERLAP or gap > MAX_GAP:
        return None
    return (RUN_BODY[2] - BODY_UNDERLAP, BODY_FILL_TOP, sink_body_x + BODY_UNDERLAP, RUN_BODY[3])


def cap_bounds(sink_body_x: int) -> tuple[int, int, int, int] | None:
    gap = sink_body_x - RUN_BODY[2]
    if gap < MIN_OVERLAP or gap > MAX_GAP:
        return None
    return (RUN_BODY[2] - CAP_UNDERLAP, CAP_TOP, sink_body_x + CAP_UNDERLAP, CAP_BOTTOM)


def assets_only(background: Image.Image, run: Image.Image, sink: Image.Image, sink_body_x: int) -> Image.Image:
    room = background.copy()
    room.alpha_composite(run, RUN_CELL_ORIGIN)
    room.alpha_composite(sink, (sink_body_x + SINK_CELL_OFFSET[0], RUN_BODY[1] + SINK_CELL_OFFSET[1]))
    return room


def countertop_palette(room: Image.Image) -> list[tuple[int, int, int, int]]:
    """Read the already-composited horizontal bands away from the basin and join."""
    palette: list[tuple[int, int, int, int]] = []
    for world_y in range(CAP_TOP, CAP_BOTTOM):
        samples = [room.getpixel((x, world_y)) for x in range(240, 300)]
        samples += [room.getpixel((x, world_y)) for x in range(404, 416)]
        palette.append(median_rgb(samples))
    return palette


def add_soft_seam(room: Image.Image, sink_body_x: int) -> None:
    """Add one anti-aliased diagonal seam, not the former double staircase."""
    scale = 4
    bounds = cap_bounds(sink_body_x)
    if not bounds:
        return
    left, top, right, bottom = bounds
    overlay = Image.new("RGBA", ((right - left) * scale, (bottom - top) * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x0 = (sink_body_x - 3 - left) * scale
    x1 = (sink_body_x + 2 - left) * scale
    draw.line((x0, 0, x1, (bottom - top) * scale), fill=(0, 42, 55, 120), width=3)
    overlay = overlay.resize((right - left, bottom - top), Image.Resampling.LANCZOS)
    room.alpha_composite(overlay, (left, top))


def compose(
    background: Image.Image,
    run: Image.Image,
    sink: Image.Image,
    body_fill: Image.Image | None,
    cap: Image.Image | None,
    sink_body_x: int = SINK_BODY_DEFAULT_X,
    soft_seam: bool = False,
) -> Image.Image:
    room = background.copy()
    body = body_bounds(sink_body_x) if body_fill is not None else None
    if body:
        left, top, right, bottom = body
        room.alpha_composite(body_fill.crop((0, 0, right - left, bottom - top)), (left, top))
    room.alpha_composite(run, RUN_CELL_ORIGIN)
    room.alpha_composite(sink, (sink_body_x + SINK_CELL_OFFSET[0], RUN_BODY[1] + SINK_CELL_OFFSET[1]))
    cap_box = cap_bounds(sink_body_x) if cap is not None else None
    if cap_box:
        left, top, right, bottom = cap_box
        room.alpha_composite(cap.crop((0, 0, right - left, bottom - top)), (left, top))
        if soft_seam:
            add_soft_seam(room, sink_body_x)
    return room


def focus(room: Image.Image) -> Image.Image:
    return room.crop((312, 124, 360, 216))


def build_page(catalogue: dict) -> str:
    template_path = ROOT / "scripts/templates/kitchen_countertop_join_cap_v22.html"
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
    v21 = Image.open(V21_ROOM).convert("RGBA")
    if background.size != ROOM or run.size != (176, 82) or sink.size != (92, 108) or v21.size != ROOM:
        raise RuntimeError("Countertop join authority geometry changed")

    unmasked = assets_only(background, run, sink, SINK_BODY_DEFAULT_X)
    body_fill = row_template(body_palette(run)[BODY_FILL_TOP - RUN_BODY[1]:], BODY_TEMPLATE_WIDTH)
    cap = row_template(countertop_palette(unmasked), CAP_TEMPLATE_WIDTH)
    seamless = compose(background, run, sink, body_fill, cap)
    soft = compose(background, run, sink, body_fill, cap, soft_seam=True)
    gap_six = compose(background, run, sink, body_fill, cap, SINK_BODY_DEFAULT_X + 6)
    gap_nine = compose(background, run, sink, body_fill, cap, SINK_BODY_DEFAULT_X + 9)

    outputs = {
        "room-background-exact.png": background,
        "cabinet-run-v11-exact.png": run,
        "sink-cabinet-v19-exact.png": sink,
        "v21-jagged-reference-exact.png": v21,
        "join-body-backfill-template.png": body_fill,
        "countertop-join-cap-template.png": cap,
        "room-default-seamless-cap.png": seamless,
        "room-default-soft-seam-cap.png": soft,
        "focus-v21-jagged-reference.png": focus(v21),
        "focus-v22-seamless-cap.png": focus(seamless),
        "focus-v22-soft-seam-cap.png": focus(soft),
        "room-six-pixel-gap-capped.png": gap_six,
        "room-nine-pixel-gap-auto-disabled.png": gap_nine,
    }
    for name, image in outputs.items():
        save(image, RAW / name)
        shutil.copyfile(RAW / name, ASSETS / name)
    for name, source in {
        "room-background-exact.png": BACKGROUND,
        "cabinet-run-v11-exact.png": RUN,
        "sink-cabinet-v19-exact.png": SINK,
        "v21-jagged-reference-exact.png": V21_ROOM,
    }.items():
        shutil.copyfile(source, RAW / name)
        shutil.copyfile(source, ASSETS / name)

    catalogue = {
        "set": SET,
        "version": 22,
        "status": "dynamic-countertop-join-cap-awaiting-visual-review",
        "authorities": {
            "background": {"file": "room-background-exact.png", "source": str(BACKGROUND.relative_to(ROOT)), "byteIdentical": True},
            "leftAsset": {"file": "cabinet-run-v11-exact.png", "source": str(RUN.relative_to(ROOT)), "byteIdentical": True, "cellOrigin": list(RUN_CELL_ORIGIN), "bodyBounds": list(RUN_BODY)},
            "rightAsset": {"file": "sink-cabinet-v19-exact.png", "source": str(SINK.relative_to(ROOT)), "byteIdentical": True, "defaultBodyX": SINK_BODY_DEFAULT_X, "bodySize": [84, 74], "cellOffsetFromBody": list(SINK_CELL_OFFSET)},
            "v21Reference": {"file": "v21-jagged-reference-exact.png", "source": str(V21_ROOM.relative_to(ROOT)), "byteIdentical": True},
        },
        "joinTreatment": {
            "drawOrder": ["room-background", "body-backfill", "cabinet-assets", "countertop-join-cap", "optional-soft-seam"],
            "bodyUnderlapPixelsPerSide": BODY_UNDERLAP,
            "capUnderlapPixelsPerSide": CAP_UNDERLAP,
            "maximumBridgedGapPixels": MAX_GAP,
            "minimumAllowedOverlapPixels": MIN_OVERLAP,
            "bodyBounds": list(body_bounds(SINK_BODY_DEFAULT_X)),
            "capBounds": list(cap_bounds(SINK_BODY_DEFAULT_X)),
            "capRows": [CAP_TOP, CAP_BOTTOM - 1],
            "capDerivedFromCompositedApprovedCountertopRows": True,
            "sourceAssetPixelsChanged": False,
        },
        "interaction": {
            "sinkDraggableHorizontally": True,
            "sinkBodyXRange": [324, 360],
            "treatments": ["seamless", "soft-angled-seam", "off"],
            "autoDisableBeyondGapPixels": MAX_GAP,
        },
        "outputs": {name: sha(RAW / name) for name in outputs},
        "media": list(outputs),
        "boundaries": {"v11Changed": False, "v19Changed": False, "v20Changed": False, "v21Changed": False, "backgroundChanged": False, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    shell_path = PUBLIC / "index.html"
    shell_path.write_text(build_page(catalogue))
    registered = [BACKGROUND, RUN, SINK, V21_ROOM, catalogue_path, *[RAW / name for name in outputs]]
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "reversible-unapproved-unpromoted",
        "candidate": {
            "catalogue": {"file": str(catalogue_path.relative_to(ROOT)), "sha256": sha(catalogue_path)},
            "publicShell": {"file": str(shell_path.relative_to(ROOT)), "sha256": sha(shell_path)},
        },
        "publishedAssets": [
            {
                "source": str((RAW / name).relative_to(ROOT)),
                "sourceSha256": sha(RAW / name),
                "publicAssemblyPath": str((ASSETS / name).relative_to(ROOT)),
            }
            for name in outputs
        ],
        "files": {str(path.relative_to(ROOT)): sha(path) for path in registered},
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print("Built Kitchen Countertop Join Cap V22: continuous worktop rows over exact unchanged assets")


if __name__ == "__main__":
    main()
