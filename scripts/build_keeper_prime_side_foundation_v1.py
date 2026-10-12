#!/usr/bin/env python3
"""Build the reversible Keeper Prime side-neutral foundation V1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "art/raw/keeper-first-batch"
BATCH_ID = "keeper-prime-side-foundation-2026-10-12-v1"
BATCH = ROOT / "art/drafts" / BATCH_ID
SOURCE = BATCH / "generated-sources/keeper_prime_neutral_standing-side-right-generated.png"
FRONT = RAW / "keeper_neutral_standing-front_f1.png"
OLD_SIDE = RAW / "keeper_neutral_standing-side-right_f1.png"
RIGHT = BATCH / "drafts/keeper_prime_neutral_standing-side-right_f1.png"
LEFT = BATCH / "drafts/keeper_prime_neutral_standing-side-left_f1.png"
PRIME = BATCH / "drafts/keeper_prime_neutral_standing-front_f1.png"
EVIDENCE = BATCH / "evidence/keeper-prime-turnaround-v1.png"

EXPECTED = {
    "front": "6d3b5057f7dad4410230c5c2a1959a2db468aca6f2d28486ec6db9e07827056a",
    "oldSide": "02106cfc54b224c8d4e9985e58420f1350f114d24e2e6c6258cad68e513657ce",
    "source": "f1d3f453a01dda021152732c8f574bc5ef821e7db2b9a4e2f0bd735cb756120b",
}

PROMPT = """Use case: identity-preserve
Asset type: foundational 2D game-sprite model reference, single full-body pose
Primary request: Create the exact right-profile neutral standing view of the SAME Lighthouse Keeper shown in Image 1. Image 1 is the sole binding identity authority. Everything—adult proportions, head-to-body ratio, rotund torso, cap size and construction, blue-and-cream uniform, dark trousers and boots, beard mass, moustache, restrained expression, palette, outline weight and rendering finish—must stem from Image 1. Image 2 supplies only the right-profile orientation, arms-down stance, foot placement and floor-facing choreography; do not copy Image 2's slimmer body, different face, hard/jagged outline or earlier model family.
Input images: Image 1: sole identity and rendering authority; Image 2: pose/orientation reference only.
Scene/backdrop: genuinely transparent background.
Subject: one adult lighthouse keeper standing completely still in exact right profile, arms relaxed naturally at his sides, feet together on one stable baseline. Preserve Image 1's slightly rotund body, broad established beard and mature restrained character. The visible eye is a solid dark rectangular eye with no white glint. The moustache is clearly separate from a readable closed mouth. The nose, ear, cap brim, beard and chest must form a convincing clean profile of Image 1, not a new character.
Style/medium: polished high-resolution pixel-art/cartoon sprite matching Image 1 exactly; same color palette, soft but deliberate outline treatment, shading density and material finish.
Composition/framing: one isolated full-body character centered on a transparent canvas, generous transparent gutter, same apparent standing height and floor anchor as Image 1.
Constraints: exact same Keeper identity as Image 1; adult and restrained; native rotundness retained; stable anatomy; exactly two arms, two hands, two legs and two boots; no prop; no text; no shadow; no floor; no scene; actual transparent background.
Avoid: copying Image 2's old identity; thin or shortened torso; childlike proportions; oversized or round eye; eye glint; smile or pixie grin; open mouth; moustache merged into mouth; shortened or smooth bulb beard; thick black cartoon outline; altered cap; pose motion; detached limbs; cropped pixels; background; labels; watermark."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixel_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("image has no opaque pixels")
    return bounds


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = {(x, 0) for x in range(image.width)} | {(x, image.height - 1) for x in range(image.width)}
    points |= {(0, y) for y in range(image.height)} | {(image.width - 1, y) for y in range(image.height)}
    return sum(alpha.getpixel(point) > 0 for point in points)


def normalize_side(source: Image.Image, front: Image.Image) -> tuple[Image.Image, dict]:
    source_bounds = source.getchannel("A").point(lambda value: 255 if value >= 32 else 0).getbbox()
    if source_bounds is None:
        raise RuntimeError("generated source has no foreground")
    crop = source.crop(source_bounds)
    front_bounds = alpha_bounds(front)
    target_height = front_bounds[3] - front_bounds[1]
    target_width = 80
    resized = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
    resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
    resized_bounds = alpha_bounds(resized)
    frame = Image.new("RGBA", front.size, (0, 0, 0, 0))
    paste_x = round(64 - (resized_bounds[0] + resized_bounds[2]) / 2)
    paste_y = 158 - resized_bounds[3]
    frame.alpha_composite(resized, (paste_x, paste_y))
    bounds = alpha_bounds(frame)
    if bounds[0] < 2 or bounds[1] < 2 or bounds[2] > 126 or bounds[3] > 158:
        raise RuntimeError(f"normalized side lost safety gutter: {bounds}")
    return frame, {
        "sourceBoundsExclusive": list(source_bounds),
        "frontBoundsExclusive": list(front_bounds),
        "normalizedBoundsExclusive": list(bounds),
        "targetOpaqueWidth": target_width,
        "targetOpaqueHeight": target_height,
        "baselineExclusive": 158,
        "centreX": 64,
        "normalization": "source alpha crop → 80×149 LANCZOS → binary alpha → centred at x64/baseline158",
    }


def checker(size: tuple[int, int]) -> Image.Image:
    result = Image.new("RGBA", size, "#dce3df")
    draw = ImageDraw.Draw(result)
    for y in range(0, size[1], 12):
        for x in range(0, size[0], 12):
            if (x // 12 + y // 12) % 2:
                draw.rectangle((x, y, x + 11, y + 11), fill="#c9d2cd")
    return result


def staged(image: Image.Image, scale: int = 3) -> Image.Image:
    result = checker(image.size)
    result.alpha_composite(image)
    return result.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)


def comparison(front: Image.Image, right: Image.Image, left: Image.Image, destination: Path) -> None:
    views = [("KEEPER PRIME — EXACT", front), ("DERIVED RIGHT — DRAFT", right), ("MIRRORED LEFT — DRAFT", left)]
    cards = [(label, staged(image)) for label, image in views]
    width = sum(image.width for _, image in cards) + 24 * (len(cards) + 1)
    height = cards[0][1].height + 86
    result = Image.new("RGBA", (width, height), "#102f3a")
    draw = ImageDraw.Draw(result)
    font = ImageFont.load_default()
    x = 24
    for label, image in cards:
        draw.text((x, 18), label, fill="#f2ca70", font=font)
        result.alpha_composite(image, (x, 50))
        x += image.width + 24
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.save(destination, optimize=False, compress_level=9)


def main() -> None:
    for key, path in (("front", FRONT), ("oldSide", OLD_SIDE), ("source", SOURCE)):
        if sha256(path) != EXPECTED[key]:
            raise RuntimeError(f"pinned {key} input changed")
    front = Image.open(FRONT).convert("RGBA")
    source = Image.open(SOURCE).convert("RGBA")
    right, normalization = normalize_side(source, front)
    left = right.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if right.size != (128, 160) or left.size != right.size:
        raise RuntimeError("foundation geometry changed")
    if sorted(set(right.getchannel("A").tobytes())) != [0, 255] or sorted(set(left.getchannel("A").tobytes())) != [0, 255]:
        raise RuntimeError("foundation alpha is not binary")
    if edge_alpha(right) or edge_alpha(left) or edge_alpha(front):
        raise RuntimeError("foundation touches a cell edge")
    RIGHT.parent.mkdir(parents=True, exist_ok=True)
    right.save(RIGHT, optimize=False, compress_level=9)
    left.save(LEFT, optimize=False, compress_level=9)
    PRIME.write_bytes(FRONT.read_bytes())
    comparison(front, right, left, EVIDENCE)
    register = {
        "batchId": BATCH_ID,
        "status": "incorporated-into-core-transition-draft-awaiting-route-approval",
        "identityName": "Keeper Prime",
        "identityShorthand": "KP",
        "identityRule": "The exact front image is the sole binding identity authority. Every other Keeper image must derive from Keeper Prime.",
        "keeperPrime": {
            "source": rel(FRONT),
            "sourceSha256": sha256(FRONT),
            "draftAlias": rel(PRIME),
            "draftAliasSha256": sha256(PRIME),
            "byteIdentical": PRIME.read_bytes() == FRONT.read_bytes(),
        },
        "poseReferenceOnly": {"source": rel(OLD_SIDE), "sha256": sha256(OLD_SIDE), "identityAuthority": False},
        "generatedSource": {"file": rel(SOURCE), "sha256": sha256(SOURCE), "tool": "built-in image_gen", "prompt": PROMPT},
        "candidates": [
            {"name": "keeper_prime_neutral_standing-side-right", "file": rel(RIGHT), "sha256": sha256(RIGHT), "pixelSha256": pixel_sha(right), "boundsExclusive": list(alpha_bounds(right)), "edgeAlphaPixels": edge_alpha(right), "derivedBy": "image generation plus deterministic normalization"},
            {"name": "keeper_prime_neutral_standing-side-left", "file": rel(LEFT), "sha256": sha256(LEFT), "pixelSha256": pixel_sha(left), "boundsExclusive": list(alpha_bounds(left)), "edgeAlphaPixels": edge_alpha(left), "derivedBy": "exact horizontal mirror of the right candidate"},
        ],
        "normalization": normalization,
        "evidence": {"turnaround": rel(EVIDENCE), "turnaroundSha256": sha256(EVIDENCE)},
        "transitionContract": {
            "states": ["walk", "stop", "action"],
            "roundTrip": ["walk-to-stop", "stop-to-action", "action-to-stop", "stop-to-walk"],
            "doorExample": "walk begins behind door → translated decelerating stop → exact side neutral → reach/open/return → exact side neutral held one 8fps tick → reversed stop/start → walk until fully door-occluded",
        },
        "checks": {"productionChanged": False, "frontByteIdentical": True, "binaryAlpha": True, "transparentCellEdges": True, "leftExactMirror": left.tobytes() == right.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()},
        "rollback": f"Delete only {rel(BATCH)}. No raw/runtime art, manifest, existing draft or review export was changed.",
    }
    write_json(BATCH / "foundation-register.json", register)
    (BATCH / "HANDOFF.md").write_text(
        "# Keeper Prime side foundation — V1\n\n"
        "Status: **incorporated into Keeper Prime core-transition Draft V1; awaiting complete-route approval; production unchanged**.\n\n"
        "`keeper_neutral_standing-front_f1.png` is named **Keeper Prime (KP)** and copied byte-for-byte as the sole identity authority. "
        "The right side neutral is newly derived from KP; the former side neutral supplied pose direction only. The left view is an exact mirror. "
        "Frank then requested all six core transitions together, so this side state now supplies their shared unapproved Draft stop endpoint.\n\n"
        "The proposed core state loop is `walk → stop → action → stop → walk`. A door action returns to exact neutral, holds one 8fps tick, then uses stop in reverse as walk-start and continues until fully hidden.\n\n"
        "Rebuild: `/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_side_foundation_v1.py`.\n"
    )
    print(json.dumps({"batch": BATCH_ID, "keeperPrime": sha256(PRIME), "right": sha256(RIGHT), "left": sha256(LEFT), "evidence": rel(EVIDENCE)}, indent=2))


if __name__ == "__main__":
    main()
