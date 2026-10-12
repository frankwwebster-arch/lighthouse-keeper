#!/usr/bin/env python3
"""Extract exact adjacent frames for the party-hat frame-2 arm-plane edit."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
NAME = "keeper_party_hat_put_on_back"
V2 = ROOT / "art/drafts/keeper-party-hat-put-on-back-hands-2026-10-12-v2/drafts" / NAME / f"{NAME}_f8.png"
FRAME_SIZE = (128, 224)


def frame(strip: Image.Image, index: int) -> Image.Image:
    width, height = FRAME_SIZE
    return strip.crop((index * width, 0, (index + 1) * width, height))


def main() -> None:
    strip = Image.open(V2).convert("RGBA")
    destination = BATCH / "inputs"
    destination.mkdir(parents=True, exist_ok=True)
    frame(strip, 0).save(destination / "frame-1-reference-v2.png")
    frame(strip, 1).save(destination / "frame-2-edit-target-v2.png")
    frame(strip, 2).save(destination / "frame-3-reference-v2.png")


if __name__ == "__main__":
    main()
