#!/usr/bin/env python3
"""Prepare V14 restrained arms and compact raised passing boots.

V14 keeps V12's exact contact geometry and V13's five-frame cadence. Generated
studies may contribute pixels only inside declared arm or moving-lower-leg
masks; head, torso core, support leg and all contact geometry stay locked.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v14"
V6 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v6"
V12 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v12"
V13 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v13"
FRAMES = PACK / "drafts/frames"
EVIDENCE = PACK / "evidence/registered-sources"
MASKS = PACK / "evidence/masks"
CELL = (256, 320)
ALPHA_THRESHOLD = 8

LEG_SOURCES = {
    "right": V6 / "drafts/frames/keeper_prime_stair_right-leg_side-left_f04.png",
    "left": V6 / "drafts/frames/keeper_prime_stair_left-leg_side-left_f04.png",
}
CONTACT_ARM_SOURCES = {
    "right": PACK / "sources/generated/right-contact-restrained-arms-v2.png",
    "left": PACK / "sources/generated/left-contact-restrained-arms-v2.png",
}
REJECTED_ARM_SOURCES = [
    PACK / "sources/generated/right-contact-restrained-arms.png",
    PACK / "sources/generated/left-contact-restrained-arms.png",
]
PASSING_BASES = {
    "right": V13 / "drafts/frames/keeper_prime_stair_right-foot-mid-swing_side-left_f01.png",
    "left": V13 / "drafts/frames/keeper_prime_stair_left-foot-mid-swing_side-left_f01.png",
}
PASSING_BOOT_SOURCES = {
    "right": PACK / "sources/generated/right-passing-compact-boot.png",
    "left": PACK / "sources/generated/left-passing-compact-boot.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    threshold = image.getchannel("A").point(lambda value: 255 if value > ALPHA_THRESHOLD else 0)
    bounds = threshold.getbbox()
    if bounds is None:
        raise RuntimeError("empty image")
    return bounds


def register_generated(source: Image.Image, target: Image.Image) -> tuple[Image.Image, dict]:
    sx0, sy0, sx1, sy1 = alpha_bounds(source)
    tx0, ty0, tx1, ty1 = alpha_bounds(target)
    scale = (ty1 - ty0) / (sy1 - sy0)
    crop = source.crop((sx0, sy0, sx1, sy1))
    resized = crop.resize((round(crop.width * scale), ty1 - ty0), Image.Resampling.LANCZOS)
    target_upper = target.crop((0, ty0, CELL[0], round(ty0 + (ty1 - ty0) * 0.67)))
    source_upper = resized.crop((0, 0, resized.width, round(resized.height * 0.67)))
    tux0, _, tux1, _ = alpha_bounds(target_upper)
    sux0, _, sux1, _ = alpha_bounds(source_upper)
    left = round((tux0 + tux1) / 2 - (sux0 + sux1) / 2)
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
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    if leg == "right":
        draw.polygon([(43, 142), (100, 128), (133, 151), (132, 216), (101, 238), (48, 235), (25, 205)], fill=255)
        draw.polygon([(130, 137), (174, 139), (203, 171), (205, 231), (177, 270), (136, 270), (128, 228), (133, 188)], fill=255)
    else:
        draw.polygon([(43, 142), (101, 128), (134, 150), (133, 216), (99, 238), (47, 235), (25, 203)], fill=255)
        draw.polygon([(130, 137), (176, 139), (207, 171), (210, 232), (180, 270), (136, 270), (128, 228), (133, 188)], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.55))


def passing_mask(leg: str) -> Image.Image:
    """Own only the screen-left moving leg below its hip; protect support boot."""
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    if leg == "right":
        draw.polygon([(54, 205), (112, 205), (127, 232), (124, 268), (109, 296), (31, 300), (18, 276), (25, 237)], fill=255)
    else:
        draw.polygon([(49, 205), (113, 205), (127, 233), (124, 270), (105, 297), (23, 300), (14, 270), (25, 230)], fill=255)
    # Keep this mask binary. A feathered exterior retained faint pixels from
    # the rejected extended boot and those pixels entered the next riser.
    # The knee join is inside the opaque trouser mass, so a hard ownership
    # boundary is both cleaner and deterministic.
    return mask


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
    xs = [x for x in range(start_x, end_x) if alpha.getpixel((x, y)) > ALPHA_THRESHOLD]
    if not xs:
        raise RuntimeError(f"no contact alpha at row {y}")
    return {"y": y, "minX": min(xs), "maxX": max(xs), "centreX": (min(xs) + max(xs)) / 2}


def unchanged_outside(base: Image.Image, candidate: Image.Image, mask: Image.Image) -> int:
    changed = 0
    bp, cp = base.load(), candidate.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if mask.getpixel((x, y)) == 0 and bp[x, y] != cp[x, y]:
                changed += 1
    return changed


def near_hand_centroid(image: Image.Image, leg: str) -> dict:
    x0, x1 = (100, 150) if leg == "right" else (125, 180)
    points = []
    for y in range(185, 235):
        for x in range(x0, x1):
            red, green, blue, alpha = image.getpixel((x, y))
            if alpha > 64 and red > 180 and 65 < green < 205 and blue < 150 and red > green + 30:
                points.append((x, y))
    if not points:
        raise RuntimeError(f"{leg} near hand not found")
    centre_x = sum(x for x, _ in points) / len(points)
    centre_y = sum(y for _, y in points) / len(points)
    return {"x": centre_x, "y": centre_y, "offsetFromPlumbX137Px": centre_x - 137, "samples": len(points)}


def far_hand_samples(image: Image.Image, leg: str) -> int:
    x0, x1 = (155, 210) if leg == "right" else (45, 105)
    samples = 0
    for y in range(165, 240):
        for x in range(x0, x1):
            red, green, blue, alpha = image.getpixel((x, y))
            if alpha > 64 and red > 180 and 65 < green < 205 and blue < 150 and red > green + 30:
                samples += 1
    return samples


def stair_surface_y(x_lp: float) -> float:
    floor_top, base_right, run, rise = 20, 116, 7, 60 / 14
    if x_lp >= base_right:
        return floor_top
    if x_lp < base_right - 98:
        return floor_top + 60
    step = int((base_right - x_lp - 1e-9) // run) + 1
    return floor_top + step * rise


def moving_leg_clearance(image: Image.Image, mask: Image.Image, support: dict, support_tread: int) -> dict:
    support_x = 119.5 - support_tread * 7
    support_y = 20 + support_tread * (60 / 14)
    x_lp = support_x - support["centreX"] / 8 + 16
    bottom_lp = support_y - (320 - support["y"]) / 8
    clearances = []
    for y in range(205, 310):
        for x in range(CELL[0]):
            if mask.getpixel((x, y)) == 255 and image.getpixel((x, y))[3] > ALPHA_THRESHOLD:
                world_x = x_lp - 16 + x / 8
                world_y = bottom_lp + (320 - y) / 8
                clearances.append(world_y - stair_surface_y(world_x))
    if not clearances:
        raise RuntimeError("moving-leg clearance mask contains no opaque pixels")
    return {"supportTread": support_tread, "minimumLp": min(clearances), "penetratingPixels": sum(value < -0.05 for value in clearances)}


def lift_masked_content(source: Image.Image, mask: Image.Image, lift_px: int) -> Image.Image:
    """Lift only the moving leg, tapering from a fixed knee to the full boot lift."""
    if lift_px == 0:
        return source
    output = source.copy()
    pixels = output.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if mask.getpixel((x, y)) > 0:
                pixels[x, y] = (0, 0, 0, 0)
    source_pixels = source.load()
    for y in range(205, 310):
        factor = max(0.0, min(1.0, (y - 205) / 35))
        target_y = round(y - lift_px * factor)
        for x in range(CELL[0]):
            if mask.getpixel((x, y)) > 0 and mask.getpixel((x, target_y)) > 0 and source_pixels[x, y][3] > 0:
                pixels[x, target_y] = source_pixels[x, y]
    return output


def main() -> None:
    paths = [*LEG_SOURCES.values(), *CONTACT_ARM_SOURCES.values(), *REJECTED_ARM_SOURCES, *PASSING_BASES.values(), *PASSING_BOOT_SOURCES.values(), V12 / "batch-register.json", V13 / "batch-register.json"]
    for path in paths:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    FRAMES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    MASKS.mkdir(parents=True, exist_ok=True)
    contacts = []
    passing = []

    for leg in ("right", "left"):
        leg_source = Image.open(LEG_SOURCES[leg]).convert("RGBA")
        generated = Image.open(CONTACT_ARM_SOURCES[leg]).convert("RGBA")
        horizontal, vertical = (14, 5) if leg == "right" else (12, 0)
        base = contact_lock(leg_source, horizontal, vertical)
        registered, registration = register_generated(generated, base)
        mask = arm_mask(leg)
        candidate = Image.composite(registered, base, mask)
        if edge_alpha(candidate):
            raise RuntimeError(f"{leg} contact touches a cell edge")
        registered_path = EVIDENCE / f"{leg}-contact-restrained-arms-registered.png"
        mask_path = MASKS / f"{leg}-contact-arm-mask.png"
        output_path = FRAMES / f"keeper_prime_stair_{leg}-contact-restrained_side-left_f01.png"
        registered.save(registered_path, optimize=False, compress_level=9)
        mask.save(mask_path, optimize=False, compress_level=9)
        candidate.save(output_path, optimize=False, compress_level=9)
        moving = row_range(candidate, 282, 0, 132)
        support = row_range(candidate, 316, 116, CELL[0])
        contacts.append({
            "leg": leg,
            "baseLegSource": {"file": rel(LEG_SOURCES[leg]), "sha256": digest(LEG_SOURCES[leg])},
            "generatedArmStudy": {"file": rel(CONTACT_ARM_SOURCES[leg]), "sha256": digest(CONTACT_ARM_SOURCES[leg])},
            "registeredArmStudy": {"file": rel(registered_path), "sha256": digest(registered_path), **registration},
            "mask": {"file": rel(mask_path), "sha256": digest(mask_path)},
            "draft": {"file": rel(output_path), "sha256": digest(output_path)},
            "contactGeometry": {"movingLegCorrectionSourcePx": [horizontal, vertical], "treadRunLp": 7, "riserRiseLp": 60 / 14},
            "supportSole": support, "movingSole": moving,
            "nearHand": near_hand_centroid(candidate, leg),
            "farHandVisibleSkinSamples": far_hand_samples(candidate, leg),
            "outsideMaskChangedPixels": unchanged_outside(base, candidate, mask),
            "cell": list(CELL), "density": 8, "edgeAlpha": 0,
        })

        pass_base = Image.open(PASSING_BASES[leg]).convert("RGBA")
        boot_study = Image.open(PASSING_BOOT_SOURCES[leg]).convert("RGBA")
        registered_boot, boot_registration = register_generated(boot_study, pass_base)
        leg_mask = passing_mask(leg)
        # The generated right-foot study registered 1.79 lp too low at its
        # heel. Lift that moving leg by two logical pixels while pinning the
        # knee; the left-foot/F4 study already clears its tread by >1.5 lp.
        moving_leg_lift_px = 16 if leg == "right" else 0
        registered_boot = lift_masked_content(registered_boot, leg_mask, moving_leg_lift_px)
        pass_candidate = Image.composite(registered_boot, pass_base, leg_mask)
        if edge_alpha(pass_candidate):
            raise RuntimeError(f"{leg} passing frame touches a cell edge")
        registered_boot_path = EVIDENCE / f"{leg}-passing-compact-boot-registered.png"
        leg_mask_path = MASKS / f"{leg}-passing-leg-mask.png"
        pass_output = FRAMES / f"keeper_prime_stair_{leg}-foot-passing-compact_side-left_f01.png"
        registered_boot.save(registered_boot_path, optimize=False, compress_level=9)
        leg_mask.save(leg_mask_path, optimize=False, compress_level=9)
        pass_candidate.save(pass_output, optimize=False, compress_level=9)
        pass_support = row_range(pass_candidate, 316, 110, CELL[0])
        support_tread = 1 if leg == "right" else 2
        passing.append({
            "movingLeg": leg, "supportLeg": "left" if leg == "right" else "right",
            "base": {"file": rel(PASSING_BASES[leg]), "sha256": digest(PASSING_BASES[leg])},
            "generatedBootStudy": {"file": rel(PASSING_BOOT_SOURCES[leg]), "sha256": digest(PASSING_BOOT_SOURCES[leg])},
            "registeredBootStudy": {"file": rel(registered_boot_path), "sha256": digest(registered_boot_path), **boot_registration},
            "mask": {"file": rel(leg_mask_path), "sha256": digest(leg_mask_path)},
            "draft": {"file": rel(pass_output), "sha256": digest(pass_output)},
            "supportSole": pass_support,
            "movingLegLiftPx": moving_leg_lift_px,
            "stairClearance": moving_leg_clearance(pass_candidate, leg_mask, pass_support, support_tread),
            "outsideMaskChangedPixels": unchanged_outside(pass_base, pass_candidate, leg_mask),
            "cell": list(CELL), "density": 8, "edgeAlpha": 0,
        })

    manifest = {
        "schema": "lighthouse-keeper/stair-ascent-source-preparation@14",
        "status": "restrained-synchronised-arms-and-compact-passing-boots-awaiting-review",
        "authorities": {
            "v12": {"file": rel(V12 / "batch-register.json"), "sha256": digest(V12 / "batch-register.json")},
            "v13": {"file": rel(V13 / "batch-register.json"), "sha256": digest(V13 / "batch-register.json")},
        },
        "method": "V12 contact construction plus tightly masked restrained-arm studies; V13 cadence plus tightly masked compact raised passing boots",
        "rejectedArmStudies": [{"file": rel(path), "sha256": digest(path), "reason": "measured arm angle remained about 25–30 degrees from vertical"} for path in REJECTED_ARM_SOURCES],
        "geometry": {"flightRunLp": 98, "flightRiseLp": 60, "risers": 14, "treadRunLp": 7, "riserRiseLp": 60 / 14, "reservedCoreRunLp": 105},
        "contacts": contacts,
        "passing": passing,
    }
    (PACK / "source-preparation-v14.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"contacts": len(contacts), "passing": len(passing), "preparation": rel(PACK / "source-preparation-v14.json")}, indent=2))


if __name__ == "__main__":
    main()
