#!/usr/bin/env python3
"""Extract exact frame references for the frame-5 horizontal-record edit."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
NAME = "keeper_put_record"
V1 = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/drafts" / NAME / f"{NAME}_f8.png"
V2 = ROOT / "art/drafts/keeper-put-record-removal-2026-10-12-v2/drafts" / NAME / f"{NAME}_f8.png"
FRAME_SIZE = (272, 160)


def frame(strip: Image.Image, index: int) -> Image.Image:
    width, height = FRAME_SIZE
    return strip.crop((index * width, 0, (index + 1) * width, height))


def save_reference(image: Image.Image, filename: str) -> None:
    destination = BATCH / "inputs" / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)


def main() -> None:
    v1 = Image.open(V1).convert("RGBA")
    v2 = Image.open(V2).convert("RGBA")
    save_reference(frame(v2, 4), "frame-5-edit-target-v2.png")
    save_reference(frame(v1, 3), "frame-4-horizontal-record-reference-v1.png")
    save_reference(frame(v2, 5), "frame-6-next-pose-v2.png")


if __name__ == "__main__":
    main()
