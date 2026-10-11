#!/usr/bin/env python3
"""Normalize the coherent generated V10 smock source and build review evidence."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "generated/artist-smock-fresh-source.png"
CANON = ROOT / "art/raw/keeper-first-batch/keeper_neutral_standing-side-right_f1.png"
OLD_STRIP = ROOT / "art/raw/keeper-first-batch/keeper_artist_smock_walk_f8.png"
PROMPT = HERE / "PROMPT.txt"
INPUTS = [
    HERE / "evidence/canon-model-pack.png",
    ROOT / "art/source/keeper-first-batch/keeper-turnaround-source.png",
    ROOT / "art/source/keeper-first-batch/keeper-walk-generated-source.png",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_bytes(image: Image.Image) -> bytes:
    stream = io.BytesIO()
    image.save(stream, "PNG", optimize=False, compress_level=9)
    return stream.getvalue()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def foreground_bbox(image: Image.Image, threshold: int = 32) -> tuple[int, int, int, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.where(alpha >= threshold)
    if not len(xs):
        raise RuntimeError("Generated source has no foreground")
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def normalize() -> tuple[Image.Image, dict]:
    source = Image.open(SOURCE).convert("RGBA")
    source_bbox = foreground_bbox(source)
    crop = source.crop(source_bbox)
    target_h = 150
    scale = target_h / crop.height
    target_w = round(crop.width * scale)
    resized = crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    rgba = np.asarray(resized).copy()
    hard = rgba[:, :, 3] >= 128
    rgba[:, :, 3] = np.where(hard, 255, 0).astype(np.uint8)
    rgba[~hard, :3] = 0
    resized = Image.fromarray(rgba, "RGBA")
    canvas = Image.new("RGBA", (128, 160), (0, 0, 0, 0))
    x = (128 - target_w) // 2
    y = 158 - target_h
    canvas.alpha_composite(resized, (x, y))
    alpha = np.asarray(canvas.getchannel("A"))
    border = int(np.count_nonzero(alpha[0]) + np.count_nonzero(alpha[-1]) + np.count_nonzero(alpha[:, 0]) + np.count_nonzero(alpha[:, -1]))
    return canvas, {
        "sourceForegroundThreshold": 32,
        "sourceForegroundBounds": list(source_bbox),
        "sourceForegroundSize": [crop.width, crop.height],
        "uniformScale": scale,
        "normalizedForegroundSize": [target_w, target_h],
        "placement": [x, y],
        "canvas": [128, 160],
        "opaqueBounds": list(canvas.getchannel("A").getbbox() or (0, 0, 0, 0)),
        "binaryAlpha": bool(np.isin(alpha, [0, 255]).all()),
        "opaqueBorderPixelCount": border,
        "aspectRatioSource": crop.width / crop.height,
        "aspectRatioNormalized": target_w / target_h,
    }


def checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    w, h = size
    out = Image.new("RGBA", size, (43, 47, 55, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(51, 56, 65, 255))
    return out


def contain(image: Image.Image, box: tuple[int, int], resample=Image.Resampling.LANCZOS) -> Image.Image:
    w, h = box
    scale = min(w / image.width, h / image.height)
    return image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))), resample)


def source_view() -> Image.Image:
    source = Image.open(SOURCE).convert("RGBA")
    crop = source.crop(foreground_bbox(source))
    sheet = Image.new("RGBA", (1200, 1550), (19, 23, 32, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((50, 34), "V10 — fresh artist-smock source", font=font(44, True), fill="#f8f9fb")
    draw.text((50, 92), "One coherent ImageGen render · new costume design · canon model pack as identity reference", font=font(24), fill="#b7c4d9")
    stage = checker((1100, 1360), 34)
    shown = contain(crop, (920, 1260))
    stage.alpha_composite(shown, ((stage.width - shown.width) // 2, (stage.height - shown.height) // 2))
    sheet.alpha_composite(stage, (50, 150))
    return sheet


def native_comparison(normalized: Image.Image) -> Image.Image:
    old = Image.open(OLD_STRIP).convert("RGBA").crop((0, 0, 136, 160))
    canon = Image.open(CANON).convert("RGBA")
    cells = [("Existing smock frame", old), ("V10 fresh smock", normalized), ("Canonical Keeper", canon)]
    sheet = Image.new("RGBA", (1450, 750), (19, 23, 32, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((45, 28), "Artist smock — first-frame comparison", font=font(40, True), fill="#f8f9fb")
    draw.text((45, 80), "Nearest-neighbour enlargement above; exact normalized raster below", font=font(22), fill="#b7c4d9")
    for i, (label, image) in enumerate(cells):
        x = 45 + i * 470
        draw.text((x, 125), label, font=font(25, True), fill="#ffffff")
        stage = checker((420, 480), 20)
        big = image.resize((image.width * 3, image.height * 3), Image.Resampling.NEAREST)
        stage.alpha_composite(big, ((420 - big.width) // 2, 0))
        sheet.alpha_composite(stage, (x, 165))
        native_stage = checker((160, 190), 8)
        native_stage.alpha_composite(image, ((160 - image.width) // 2, 10))
        sheet.alpha_composite(native_stage, (x + 130, 535))
    return sheet


def main() -> None:
    (HERE / "drafts").mkdir(exist_ok=True)
    normalized, metrics = normalize()
    repeat, repeat_metrics = normalize()
    normalized_path = HERE / "drafts/artist-smock-first-frame-normalized.png"
    source_view_path = HERE / "evidence/artist-smock-source-view.png"
    comparison_path = HERE / "evidence/artist-smock-native-comparison.png"
    normalized_path.write_bytes(png_bytes(normalized))
    source_view_path.write_bytes(png_bytes(source_view()))
    comparison_path.write_bytes(png_bytes(native_comparison(normalized)))
    validation = json.loads((HERE / "evidence/validation.json").read_text())
    validation["generation"] = {
        "method": "built-in image generator; referenced-image identity-preserve mode",
        "source": {"path": str(SOURCE.relative_to(HERE)), "sha256": sha256(SOURCE)},
        "prompt": {"path": str(PROMPT.relative_to(HERE)), "sha256": sha256(PROMPT)},
        "referencedInputs": [{"path": str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path), "sha256": sha256(path)} for path in INPUTS],
        "selectedCandidateCount": 1,
    }
    validation["normalization"] = {
        **metrics,
        "deterministicRerun": png_bytes(normalized) == png_bytes(repeat) and metrics == repeat_metrics,
        "output": {"path": str(normalized_path.relative_to(HERE)), "sha256": sha256(normalized_path)},
    }
    validation["reviewEvidence"] = {
        "sourceView": {"path": str(source_view_path.relative_to(HERE)), "sha256": sha256(source_view_path)},
        "nativeComparison": {"path": str(comparison_path.relative_to(HERE)), "sha256": sha256(comparison_path)},
    }
    validation["scopeGate"] = {
        "generatedCharacters": 1,
        "outfit": "artist-smock",
        "animationFramesStarted": 0,
        "otherCostumesStarted": 0,
        "registered": False,
        "promoted": False,
        "committed": False,
        "pushed": False,
    }
    (HERE / "evidence/validation.json").write_text(json.dumps(validation, indent=2) + "\n")


if __name__ == "__main__":
    main()
