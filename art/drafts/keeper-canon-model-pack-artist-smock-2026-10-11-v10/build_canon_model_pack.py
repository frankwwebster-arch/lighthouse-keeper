#!/usr/bin/env python3
"""Extract the accepted Keeper model poses and render deterministic outlines.

The output is reference preparation only. It does not redraw, amend, or promote
any production sprite.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RAW = ROOT / "art/raw/keeper-first-batch"

MODELS = [
    ("standing-side-right", "keeper_walk", 2, "contract neutral"),
    ("standing-front", "keeper_wave_camera", 0, "reviewer ghost"),
    ("standing-back", "keeper_turn_back", 5, "reviewer ghost / contract neutral"),
    ("sitting-side-right", "keeper_sit_side", 5, "reviewer ghost / contract neutral"),
    ("sitting-front", "keeper_sit_front", 5, "reviewer ghost / contract neutral"),
    ("sitting-back", "keeper_sit_back", 5, "reviewer ghost / contract neutral"),
    ("sitting-rear-right", "keeper_watch_tv", 0, "contract neutral"),
    ("crouching-back", "keeper_crouch_work_back", 3, "contract neutral"),
    ("holding-small-object-side-right", "keeper_pick_vegetable", 7, "contract endpoint"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def source_paths(clip: str) -> tuple[Path, Path]:
    matches = sorted(RAW.glob(f"{clip}_f*.json"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one sidecar for {clip}, found {len(matches)}")
    sidecar = matches[0]
    return sidecar.with_suffix(".png"), sidecar


def extract(clip: str, frame: int) -> tuple[Image.Image, dict, Path, Path]:
    strip_path, sidecar_path = source_paths(clip)
    meta = json.loads(sidecar_path.read_text())
    strip = Image.open(strip_path).convert("RGBA")
    cell_w = int(meta["w"]) * int(meta["density"])
    cell_h = int(meta["h"]) * int(meta["density"])
    if strip.size != (cell_w * int(meta["frames"]), cell_h):
        raise RuntimeError(f"Geometry mismatch for {clip}: {strip.size}")
    if not 0 <= frame < int(meta["frames"]):
        raise RuntimeError(f"Frame {frame} is outside {clip}")
    return strip.crop((frame * cell_w, 0, (frame + 1) * cell_w, cell_h)), meta, strip_path, sidecar_path


def outline(frame: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A")
    expanded = alpha.filter(ImageFilter.MaxFilter(9))
    boundary = np.asarray(expanded, dtype=np.int16) - np.asarray(alpha, dtype=np.int16)
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    rgba = np.zeros((frame.height, frame.width, 4), dtype=np.uint8)
    rgba[boundary > 0] = (246, 239, 208, 255)
    return Image.fromarray(rgba, "RGBA")


def checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    w, h = size
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            shade = 42 if ((x // tile) + (y // tile)) % 2 == 0 else 50
            arr[y, x] = (shade, shade + 3, shade + 8, 255)
    return Image.fromarray(arr, "RGBA")


def render_sheet(records: list[dict]) -> Image.Image:
    card_w, card_h = 430, 530
    sheet = Image.new("RGBA", (3 * card_w + 80, 3 * card_h + 145), (19, 23, 32, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((40, 28), "Keeper canonical model pack — exact accepted rasters and extracted outlines", font=font(34, True), fill="#f7f8fb")
    draw.text((40, 76), "Nine accepted pose authorities; reference preparation only", font=font(22), fill="#b9c5d8")
    for index, record in enumerate(records):
        col, row = index % 3, index // 3
        x, y = 40 + col * card_w, 125 + row * card_h
        draw.rounded_rectangle((x, y, x + card_w - 20, y + card_h - 20), radius=18, fill="#252b38", outline="#465166", width=2)
        draw.text((x + 20, y + 18), record["pose"], font=font(22, True), fill="#ffffff")
        draw.text((x + 20, y + 52), f'{record["clip"]} · frame {record["frame"] + 1}', font=font(17), fill="#aebbd0")
        frame = record["image"]
        edged = Image.alpha_composite(outline(frame), frame)
        scaled = edged.resize((256, 320), Image.Resampling.NEAREST)
        stage = checker((320, 350), 20)
        stage.alpha_composite(scaled, ((320 - 256) // 2, 12))
        sheet.alpha_composite(stage, (x + 45, y + 92))
        draw.text((x + 20, y + 455), record["role"], font=font(16), fill="#d9c77e")
    return sheet


def main() -> None:
    (HERE / "outlines").mkdir(parents=True, exist_ok=True)
    (HERE / "models").mkdir(parents=True, exist_ok=True)
    (HERE / "evidence").mkdir(parents=True, exist_ok=True)
    records = []
    for pose, clip, frame_index, role in MODELS:
        frame, meta, strip_path, sidecar_path = extract(clip, frame_index)
        frame_path = HERE / "models" / f"{pose}.png"
        outline_path = HERE / "outlines" / f"{pose}-outline.png"
        frame.save(frame_path)
        outline(frame).save(outline_path)
        alpha = np.asarray(frame.getchannel("A"))
        records.append({
            "pose": pose,
            "clip": clip,
            "frame": frame_index,
            "role": role,
            "image": frame,
            "source": str(strip_path.relative_to(ROOT)),
            "sourceSha256": sha256(strip_path),
            "sidecar": str(sidecar_path.relative_to(ROOT)),
            "sidecarSha256": sha256(sidecar_path),
            "canvas": list(frame.size),
            "opaqueBounds": list(frame.getchannel("A").getbbox() or (0, 0, 0, 0)),
            "binaryAlpha": bool(np.isin(alpha, [0, 255]).all()),
            "modelFile": str(frame_path.relative_to(HERE)),
            "modelSha256": sha256(frame_path),
            "outlineFile": str(outline_path.relative_to(HERE)),
            "outlineSha256": sha256(outline_path),
        })

    sheet_path = HERE / "evidence/canon-model-pack.png"
    render_sheet(records).save(sheet_path)
    validation = {
        "status": "reference-preparation-only",
        "scope": "all nine accepted canonical/contract Keeper pose models",
        "productionFilesChanged": False,
        "models": [{k: v for k, v in item.items() if k != "image"} for item in records],
        "sheet": {"path": str(sheet_path.relative_to(HERE)), "sha256": sha256(sheet_path)},
    }
    (HERE / "evidence/validation.json").write_text(json.dumps(validation, indent=2) + "\n")


if __name__ == "__main__":
    main()
