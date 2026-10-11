#!/usr/bin/env python3
"""Normalize the V5 reach pose and preview it in the walk-to-snooker route."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RAW = ROOT / "art/raw/keeper-first-batch"
SOURCE = HERE / "generated/single-reach-pose-v5-fresh-two-arm-redraft.png"
NORMALIZED = HERE / "generated/single-reach-pose-v5-normalized.png"
GIF = HERE / "single-reach-v5-in-walk-stop-snooker-preview.gif"
CONTACT = HERE / "single-reach-v5-in-walk-stop-snooker-contact-sheet.png"
REPORT = HERE / "validation-v5-preview.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_bytes(image: Image.Image) -> bytes:
    stream = io.BytesIO()
    image.save(stream, "PNG", optimize=False, compress_level=9)
    return stream.getvalue()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    filename = "Arial Bold.ttf" if bold else "Arial.ttf"
    try:
        return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{filename}", size)
    except OSError:
        return ImageFont.load_default()


def foreground_bbox(image: Image.Image, threshold: int = 32) -> tuple[int, int, int, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.where(alpha >= threshold)
    if not len(xs):
        raise RuntimeError("V5 source has no foreground")
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def normalize_reach() -> tuple[Image.Image, dict]:
    source = Image.open(SOURCE).convert("RGBA")
    bbox = foreground_bbox(source)
    crop = source.crop(bbox)
    target_h = 150
    scale = target_h / crop.height
    target_w = round(crop.width * scale)
    resized = crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    rgba = np.asarray(resized).copy()
    hard = rgba[:, :, 3] >= 128
    rgba[:, :, 3] = np.where(hard, 255, 0).astype(np.uint8)
    rgba[~hard, :3] = 0
    resized = Image.fromarray(rgba, "RGBA")

    alpha = np.asarray(resized.getchannel("A"))
    bottom_start = max(0, target_h - 22)
    ys, xs = np.where(alpha[bottom_start:] > 0)
    if not len(xs):
        raise RuntimeError("Cannot locate V5 boot contact")
    foot_center = (int(xs.min()) + int(xs.max())) / 2

    canvas = Image.new("RGBA", (256, 160), (0, 0, 0, 0))
    x = round(128 - foot_center)
    y = 158 - target_h
    canvas.alpha_composite(resized, (x, y))
    canvas_alpha = np.asarray(canvas.getchannel("A"))
    border = int(
        np.count_nonzero(canvas_alpha[0])
        + np.count_nonzero(canvas_alpha[-1])
        + np.count_nonzero(canvas_alpha[:, 0])
        + np.count_nonzero(canvas_alpha[:, -1])
    )
    return canvas, {
        "sourceForegroundThreshold": 32,
        "sourceForegroundBounds": list(bbox),
        "sourceForegroundSize": [crop.width, crop.height],
        "uniformScale": scale,
        "normalizedForegroundSize": [target_w, target_h],
        "footCenterInNormalizedCrop": foot_center,
        "placement": [x, y],
        "canvas": [256, 160],
        "anchor": [128, 160],
        "opaqueBounds": list(canvas.getchannel("A").getbbox() or (0, 0, 0, 0)),
        "binaryAlpha": bool(np.isin(canvas_alpha, [0, 255]).all()),
        "opaqueBorderPixelCount": border,
    }


def sheet_frames(path: Path, cell_w: int, count: int) -> list[Image.Image]:
    sheet = Image.open(path).convert("RGBA")
    return [sheet.crop((i * cell_w, 0, (i + 1) * cell_w, sheet.height)) for i in range(count)]


def on_route_canvas(frame: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", (256, 160), (0, 0, 0, 0))
    canvas.alpha_composite(frame, ((256 - frame.width) // 2, 0))
    return canvas


def stage(frame: Image.Image, label: str) -> Image.Image:
    background = Image.new("RGBA", (512, 360), (242, 242, 242, 255))
    enlarged = frame.resize((512, 320), Image.Resampling.NEAREST)
    background.alpha_composite(enlarged, (0, 40))
    draw = ImageDraw.Draw(background)
    text_bbox = draw.textbbox((0, 0), label, font=font(20, True))
    draw.text(((512 - (text_bbox[2] - text_bbox[0])) // 2, 8), label, font=font(20, True), fill=(25, 31, 43, 255))
    return background.convert("RGB")


def build_preview(reach: Image.Image) -> tuple[list[Image.Image], list[int], list[str]]:
    walk = [on_route_canvas(frame) for frame in sheet_frames(RAW / "keeper_walk_cycle_f9.png", 128, 9)]
    stop = [on_route_canvas(frame) for frame in sheet_frames(RAW / "keeper_walk_stop_f5.png", 128, 5)]
    neutral = on_route_canvas(Image.open(RAW / "keeper_neutral_standing-side-right_f1.png").convert("RGBA"))
    legacy = sheet_frames(RAW / "keeper_snooker_f8.png", 256, 8)

    frames = walk + stop + [neutral] + [reach] + legacy
    labels = (
        ["CANON WALK"] * len(walk)
        + ["CANON STOP"] * len(stop)
        + ["EXACT NEUTRAL"]
        + ["NEW REACH TRANSITION"]
        + ["LEGACY SNOOKER - BEARD STILL WRONG"] * len(legacy)
    )
    durations = [125] * len(walk) + [125] * len(stop) + [250, 375] + [250] * len(legacy)
    return [stage(frame, label) for frame, label in zip(frames, labels)], durations, labels


def contact_sheet(frames: list[Image.Image], labels: list[str]) -> Image.Image:
    thumbs = [frame.resize((256, 180), Image.Resampling.NEAREST) for frame in frames]
    columns = 8
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * 264 + 8, rows * 188 + 8), (255, 255, 255))
    for i, thumb in enumerate(thumbs):
        x = 8 + (i % columns) * 264
        y = 8 + (i // columns) * 188
        sheet.paste(thumb, (x, y))
    return sheet


def main() -> None:
    reach, metrics = normalize_reach()
    rerun, rerun_metrics = normalize_reach()
    NORMALIZED.write_bytes(png_bytes(reach))
    preview_frames, durations, labels = build_preview(reach)
    preview_frames[0].save(
        GIF,
        save_all=True,
        append_images=preview_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )
    contact_sheet(preview_frames, labels).save(CONTACT, "PNG", optimize=False, compress_level=9)
    report = {
        "status": "draft-animation-preview-only-awaiting-frank-review",
        "normalization": {
            **metrics,
            "deterministicRerun": png_bytes(reach) == png_bytes(rerun) and metrics == rerun_metrics,
            "output": {"path": str(NORMALIZED.relative_to(HERE)), "sha256": sha256(NORMALIZED)},
        },
        "sequence": [
            {"clip": "keeper_walk_cycle", "frames": 9, "durationMsPerFrame": 125},
            {"clip": "keeper_walk_stop", "frames": 5, "durationMsPerFrame": 125},
            {"clip": "keeper_neutral_standing-side-right", "frames": 1, "durationMs": 250},
            {"clip": "single-reach-pose-v5", "frames": 1, "durationMs": 375},
            {"clip": "keeper_snooker", "frames": 8, "durationMsPerFrame": 250, "status": "legacy-rejected-identity"},
        ],
        "preview": {"path": str(GIF.relative_to(HERE)), "sha256": sha256(GIF)},
        "contactSheet": {"path": str(CONTACT.relative_to(HERE)), "sha256": sha256(CONTACT)},
        "scopeGate": {"productionChanged": False, "reviewerChanged": False, "registered": False, "promoted": False},
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
