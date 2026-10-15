#!/usr/bin/env python3
"""Prepare V12 stair-contact artwork on a 14-tread, 7 x 60/14 lp flight.

V12 deliberately starts again from the V7 binding RIGHT/LEFT contact drawings.
It expands their moving-foot offset from 6 to 7 logical pixels while keeping
the proven 14-rise vertical cadence, then admits generated pixels only inside
declared arm regions.  The accepted
contact legs, Prime head and central torso remain the deterministic authority.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v12"
V7 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v7"
V6 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v6"
FRAMES = PACK / "drafts/frames"
EVIDENCE = PACK / "evidence/registered-arm-sources"
CELL = (256, 320)
ALPHA_THRESHOLD = 8

CONTACTS = {
    "right": V7 / "drafts/frames/keeper_prime_stair_right-contact_side-left_f01.png",
    "left": V7 / "drafts/frames/keeper_prime_stair_left-contact_side-left_f01.png",
}
LEG_SOURCES = {
    "right": V6 / "drafts/frames/keeper_prime_stair_right-leg_side-left_f04.png",
    "left": V6 / "drafts/frames/keeper_prime_stair_left-leg_side-left_f04.png",
}
ARM_SOURCES = {
    "right": PACK / "sources/generated/right-leg-contact-arm-study.png",
    "left": PACK / "sources/generated/left-leg-contact-arm-study-opposite.png",
}
REJECTED_ARM_SOURCES = [PACK / "sources/generated/left-leg-contact-arm-study.png"]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    threshold = alpha.point(lambda value: 255 if value > ALPHA_THRESHOLD else 0)
    bounds = threshold.getbbox()
    if bounds is None:
        raise RuntimeError("empty image")
    return bounds


def register_generated(source: Image.Image, target: Image.Image) -> tuple[Image.Image, dict]:
    """Fit the generated study to the target's full alpha height and upper centre."""
    sx0, sy0, sx1, sy1 = alpha_bounds(source)
    tx0, ty0, tx1, ty1 = alpha_bounds(target)
    scale = (ty1 - ty0) / (sy1 - sy0)
    crop = source.crop((sx0, sy0, sx1, sy1))
    resized = crop.resize((round(crop.width * scale), ty1 - ty0), Image.Resampling.LANCZOS)
    # Align the upper two-thirds rather than the boots, because only arms are admitted.
    target_upper = target.crop((0, ty0, CELL[0], round(ty0 + (ty1 - ty0) * 0.67)))
    source_upper = resized.crop((0, 0, resized.width, round(resized.height * 0.67)))
    tux0, _, tux1, _ = alpha_bounds(target_upper)
    sux0, _, sux1, _ = alpha_bounds(source_upper)
    target_centre = (tux0 + tux1) / 2
    source_centre = (sux0 + sux1) / 2
    left = round(target_centre - source_centre)
    registered = Image.new("RGBA", CELL, (0, 0, 0, 0))
    registered.alpha_composite(resized, (left, ty0))
    return registered, {
        "sourceBoundsExclusive": [sx0, sy0, sx1, sy1],
        "targetBoundsExclusive": [tx0, ty0, tx1, ty1],
        "scale": scale,
        "registeredLeft": left,
        "registeredTop": ty0,
    }


def sample_bilinear(image: Image.Image, x: float, y: float) -> tuple[int, int, int, int]:
    x0 = max(0, min(image.width - 1, int(x)))
    y0 = max(0, min(image.height - 1, int(y)))
    x1 = min(image.width - 1, x0 + 1)
    y1 = min(image.height - 1, y0 + 1)
    fx, fy = x - x0, y - y0
    pixels = image.load()
    values = []
    for channel in range(4):
        top = pixels[x0, y0][channel] * (1 - fx) + pixels[x1, y0][channel] * fx
        bottom = pixels[x0, y1][channel] * (1 - fx) + pixels[x1, y1][channel] * fx
        values.append(round(top * (1 - fy) + bottom * fy))
    return tuple(values)  # type: ignore[return-value]


def contact_lock(source: Image.Image, horizontal: int, vertical: int) -> Image.Image:
    """Retarget V6's screen-left moving leg to one exact 7 x 60/14-lp step."""
    output = source.copy()
    pixels = output.load()
    start_y, full_y, boundary_x = 220, 260, 110
    for y in range(start_y, output.height):
        for x in range(boundary_x + horizontal):
            pixels[x, y] = (0, 0, 0, 0)
    for y in range(start_y, 317):
        for x in range(boundary_x + horizontal):
            factor = max(0.0, min(1.0, (y - start_y) / (full_y - start_y + vertical)))
            sx = x - horizontal * factor
            sy = y - vertical * factor
            if sx < 0 or sx >= boundary_x or sy < start_y or sy >= source.height:
                continue
            pixels[x, y] = sample_bilinear(source, sx, sy)
    for y in range(317, output.height):
        for x in range(output.width):
            pixels[x, y] = (0, 0, 0, 0)
    return output


def arm_mask(leg: str) -> Image.Image:
    """Declared generated-pixel admission regions; excludes head and legs."""
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    if leg == "right":
        draw.polygon([(43, 142), (100, 128), (133, 151), (132, 216), (101, 238), (48, 235), (25, 205)], fill=255)
        draw.polygon([(130, 137), (174, 139), (203, 171), (205, 231), (177, 270), (136, 270), (128, 228), (133, 188)], fill=255)
    else:
        draw.polygon([(43, 142), (101, 128), (134, 150), (133, 216), (99, 238), (47, 235), (25, 203)], fill=255)
        draw.polygon([(130, 137), (176, 139), (207, 171), (210, 232), (180, 270), (136, 270), (128, 228), (133, 188)], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.55))


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    count = 0
    for x in range(CELL[0]):
        count += int(alpha.getpixel((x, 0)) > 0) + int(alpha.getpixel((x, CELL[1] - 1)) > 0)
    for y in range(1, CELL[1] - 1):
        count += int(alpha.getpixel((0, y)) > 0) + int(alpha.getpixel((CELL[0] - 1, y)) > 0)
    return count


def row_range(image: Image.Image, y: int, start_x: int, end_x: int) -> dict:
    alpha = image.getchannel("A")
    xs = [x for x in range(start_x, end_x) if alpha.getpixel((x, y)) > 64]
    if not xs:
        raise RuntimeError(f"no contact alpha at row {y}")
    return {"y": y, "minX": min(xs), "maxX": max(xs), "centreX": (min(xs) + max(xs)) / 2}


def main() -> None:
    for path in [*CONTACTS.values(), *LEG_SOURCES.values(), *ARM_SOURCES.values(), *REJECTED_ARM_SOURCES]:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    FRAMES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    records = []
    for leg in ("right", "left"):
        contact = Image.open(CONTACTS[leg]).convert("RGBA")
        leg_source = Image.open(LEG_SOURCES[leg]).convert("RGBA")
        source = Image.open(ARM_SOURCES[leg]).convert("RGBA")
        registered, registration = register_generated(source, contact)
        registered_path = EVIDENCE / f"{leg}-leg-arm-study-registered.png"
        registered.save(registered_path, optimize=False, compress_level=9)

        # V7 used +22/+20 horizontal and +5/+0 vertical corrections for a
        # 48 x 34 source-pixel contact.  Reduce the inward correction by
        # eight source pixels to produce the deeper 56-pixel tread while
        # retaining the proven 60/14-lp vertical pitch (34.286 source px).
        horizontal = 14 if leg == "right" else 12
        vertical = 5 if leg == "right" else 0
        geometry_base = contact_lock(leg_source, horizontal, vertical)
        mask = arm_mask(leg)
        output = Image.composite(registered, geometry_base, mask)
        if edge_alpha(output):
            raise RuntimeError(f"{leg} output touches a cell edge")
        output_path = FRAMES / f"keeper_prime_stair_{leg}-contact_side-left_f01.png"
        output.save(output_path, optimize=False, compress_level=9)
        moving = row_range(output, 282, 0, 132)
        support = row_range(output, 316, 116, CELL[0])
        separation = support["centreX"] - moving["centreX"]
        records.append({
            "leg": leg,
            "phase": "adjacent-tread contact with visible contralateral arms",
            "original": {"file": rel(CONTACTS[leg]), "sha256": digest(CONTACTS[leg])},
            "legSource": {"file": rel(LEG_SOURCES[leg]), "sha256": digest(LEG_SOURCES[leg])},
            "armSource": {"file": rel(ARM_SOURCES[leg]), "sha256": digest(ARM_SOURCES[leg])},
            "registeredArmSource": {"file": rel(registered_path), "sha256": digest(registered_path), **registration},
            "draft": {"file": rel(output_path), "sha256": digest(output_path)},
            "declaredArmMask": "two feathered polygons, y128..250 only",
            "contactGeometry": {"treadRunLp": 7, "riserRiseLp": 60 / 14, "movingLegCorrectionSourcePx": [horizontal, vertical]},
            "supportSole": support,
            "movingSole": moving,
            "localSeparation": {"xPx": separation, "xLp": separation / 8, "yPx": 34, "yLp": 34 / 8},
            "cell": list(CELL),
            "density": 8,
            "edgeAlpha": 0,
        })

    manifest = {
        "schema": "lighthouse-keeper/stair-ascent-source-preparation@12",
        "status": "contact-and-arm-reset-awaiting-visual-inspection",
        "method": "V7 binding contacts retargeted to 7 x 60/14 lp; generated studies admitted only inside declared arm polygons",
        "geometry": {"flightRunLp": 98, "flightRiseLp": 60, "risers": 14, "treadRunLp": 7, "riserRiseLp": 60 / 14, "reservedCoreRunLp": 105},
        "rejectedArmSources": [{"file": rel(path), "sha256": digest(path), "reason": "duplicated the selected forward-arm phase instead of producing the required opposite silhouette"} for path in REJECTED_ARM_SOURCES],
        "frames": records,
    }
    (PACK / "source-preparation-v12.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"frames": len(records), "preparation": rel(PACK / "source-preparation-v12.json")}, indent=2))


if __name__ == "__main__":
    main()
