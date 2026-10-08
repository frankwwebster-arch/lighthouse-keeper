#!/usr/bin/env python3
"""Normalize the first generated Pixel art batch to the runtime contract.

Run with the bundled Codex Python runtime (Pillow required). The source files are
kept under art/source/first-production-batch so the exports are reproducible.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art" / "source" / "first-production-batch"
OUTPUT = ROOT / "art" / "raw" / "first-production-batch"

ASSETS = {
    "room_kitchen_source.png": ("room_kitchen.png", (105, 35)),
    "room_living_source.png": ("room_living.png", (105, 35)),
    "room_bedroom_source.png": ("room_bedroom.png", (105, 35)),
    "tower_stripe_red_source.png": ("tower_stripe_red.png", (110, 8)),
    "tower_stripe_white_source.png": ("tower_stripe_white.png", (110, 8)),
}


def normalize(source_path: Path, output_path: Path, size: tuple[int, int]) -> None:
    source = Image.open(source_path).convert("RGBA")
    alpha = source.getchannel("A")
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError(f"{source_path} has no visible pixels")

    # The very wide generated stripe sources can contain a handful of isolated
    # translucent pixels far from the actual band. Ignore rows/columns whose
    # visible coverage is less than a quarter of the corresponding dimension.
    if size[1] <= 8:
        dense_rows = [
            y
            for y in range(source.height)
            if sum(alpha.crop((0, y, source.width, y + 1)).histogram()[128:])
            >= source.width // 4
        ]
        if dense_rows:
            bounds = (bounds[0], dense_rows[0], bounds[2], dense_rows[-1] + 1)

    cropped = source.crop(bounds)
    resized = cropped.resize(size, Image.Resampling.NEAREST)

    # Production sprites use hard pixel edges: a source pixel is either fully
    # visible or fully transparent. This removes generated edge antialiasing.
    hard_alpha = resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
    rgb = resized.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGB")
    result = Image.merge("RGBA", (*rgb.split(), hard_alpha))
    result.save(output_path, optimize=True)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for source_name, (output_name, size) in ASSETS.items():
        normalize(SOURCE / source_name, OUTPUT / output_name, size)
        print(f"{output_name}: {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
