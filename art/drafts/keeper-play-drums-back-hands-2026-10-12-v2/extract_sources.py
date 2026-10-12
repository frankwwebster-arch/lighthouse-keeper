#!/usr/bin/env python3
"""Extract exact source cells and normalized v1 reference frames."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
SOURCE = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/generated/outfit-walks/keeper_play_drums_back-v1.png"
STRIP = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/drafts/keeper_play_drums_back/keeper_play_drums_back_f8.png"


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    for frame in (5, 6, 7):
        left = round(source.width * (frame - 1) / 8)
        right = round(source.width * frame / 8)
        source.crop((left, 0, right, source.height)).save(BATCH / f"frame-{frame}-source.png")

    strip = Image.open(STRIP).convert("RGBA")
    frame_width = strip.width // 8
    for frame in (5, 6, 7):
        left = (frame - 1) * frame_width
        strip.crop((left, 0, left + frame_width, strip.height)).save(BATCH / f"frame-{frame}-v1.png")


if __name__ == "__main__":
    main()
