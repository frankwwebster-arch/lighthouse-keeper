#!/usr/bin/env python3
"""Extract exact equal-width source cells used for the two image edits."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
SOURCE = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/generated/outfit-walks/keeper_carry_shopping-v1-neutral.png"


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    for frame, label in ((1, "source"), (2, "reference"), (7, "source"), (8, "reference")):
        index = frame - 1
        left = round(image.width * index / 8)
        right = round(image.width * (index + 1) / 8)
        image.crop((left, 0, right, image.height)).save(BATCH / f"frame-{frame}-{label}.png")


if __name__ == "__main__":
    main()
