#!/usr/bin/env python3
"""Build leg-authoritative arm guides for Keeper Prime Walk V5.

The accepted V4 leg poses are copied without alteration.  Each guide overlays
the deterministic contralateral arm targets that correspond to that leg phase.
Red is the near/foreground arm; cyan is the far/background arm.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v4/drafts/frames"
PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v5"
GUIDES = PACK / "evidence/arm-phase-guides"

# Pixel-space joints in the accepted 256x320 cell.  The endpoints (F1/F5) are
# measured from the accepted art; the intervening poses are a smooth, symmetric
# interpolation tied to the eight accepted leg phases.
ARM_JOINTS = {
    1: {"near": [(113, 151), (76, 178), (58, 216)], "far": [(96, 153), (159, 171), (198, 205)]},
    2: {"near": [(113, 151), (91, 181), (82, 218)], "far": [(96, 153), (149, 179), (175, 213)]},
    3: {"near": [(113, 151), (108, 184), (110, 221)], "far": [(96, 153), (132, 188), (145, 221)]},
    4: {"near": [(113, 151), (139, 181), (160, 214)], "far": [(96, 153), (113, 190), (105, 224)]},
    5: {"near": [(113, 151), (158, 175), (190, 207)], "far": [(96, 153), (100, 181), (80, 215)]},
    6: {"near": [(113, 151), (140, 184), (160, 220)], "far": [(96, 153), (110, 190), (105, 225)]},
    7: {"near": [(113, 151), (120, 189), (115, 224)], "far": [(96, 153), (132, 189), (145, 222)]},
    8: {"near": [(113, 151), (95, 184), (85, 220)], "far": [(96, 153), (150, 180), (175, 214)]},
}

PHASES = {
    1: "contact: near arm back / far arm forward",
    2: "down: both arms return toward passing",
    3: "passing: both arms near vertical",
    4: "up: near arm forward / far arm back",
    5: "opposite contact: near arm forward / far arm back",
    6: "opposite down: both arms return toward passing",
    7: "opposite passing: both arms near vertical",
    8: "opposite up: near arm back / far arm forward",
}


def draw_arm(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], colour: tuple[int, int, int, int]) -> None:
    draw.line(points, fill=(8, 12, 18, 230), width=10, joint="curve")
    draw.line(points, fill=colour, width=5, joint="curve")
    for x, y in points:
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(8, 12, 18, 255))
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=colour)


def main() -> None:
    GUIDES.mkdir(parents=True, exist_ok=True)
    manifest = {
        "status": "deterministic-guide-not-art",
        "authority": "accepted V4 legs",
        "rule": "near and far arms counter-swing in exact opposition to the accepted leg cycle",
        "colours": {"near": "red", "far": "cyan"},
        "frames": [],
    }
    for frame in range(1, 9):
        source = V4 / f"keeper_prime_walk-right_f{frame}.png"
        image = Image.open(source).convert("RGBA")
        checker = Image.new("RGBA", image.size, (18, 30, 40, 255))
        draw_checker = ImageDraw.Draw(checker)
        for y in range(0, image.height, 16):
            for x in range(0, image.width, 16):
                if (x // 16 + y // 16) % 2:
                    draw_checker.rectangle((x, y, x + 15, y + 15), fill=(31, 48, 59, 255))
        faded = ImageEnhance.Brightness(image).enhance(0.55)
        faded.putalpha(image.getchannel("A").point(lambda value: round(value * 0.58)))
        checker.alpha_composite(faded)
        guide = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(guide)
        draw_arm(draw, ARM_JOINTS[frame]["far"], (24, 211, 238, 255))
        draw_arm(draw, ARM_JOINTS[frame]["near"], (255, 72, 72, 255))
        checker.alpha_composite(guide)
        draw = ImageDraw.Draw(checker)
        draw.rectangle((0, 0, 255, 31), fill=(6, 12, 18, 225))
        draw.text((8, 5), f"F{frame}  {PHASES[frame]}", fill=(255, 255, 255, 255))
        output = GUIDES / f"keeper_prime_walk_v5_arm-guide_f{frame}.png"
        checker.save(output, optimize=False, compress_level=9)
        manifest["frames"].append({
            "frame": frame,
            "acceptedBase": source.relative_to(ROOT).as_posix(),
            "phase": PHASES[frame],
            "joints": ARM_JOINTS[frame],
            "guide": output.relative_to(ROOT).as_posix(),
        })
    (PACK / "arm-phase-map.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
