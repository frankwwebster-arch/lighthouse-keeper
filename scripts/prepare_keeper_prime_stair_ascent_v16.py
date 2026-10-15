#!/usr/bin/env python3
"""Prepare V16's three tightly masked stair-ascent corrections."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v16"
V6 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v6"
V14 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v14"
V15 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v15"
FRAMES = PACK / "drafts/frames"
REGISTERED = PACK / "evidence/registered-sources"
MASKS = PACK / "evidence/masks"
CELL = (256, 320)
ALPHA_THRESHOLD = 8

V14_FRAMES = {
    "right_passing": V14 / "drafts/frames/keeper_prime_stair_right-foot-passing-compact_side-left_f01.png",
    "left_passing": V14 / "drafts/frames/keeper_prime_stair_left-foot-passing-compact_side-left_f01.png",
    "right_contact": V14 / "drafts/frames/keeper_prime_stair_right-contact-restrained_side-left_f01.png",
    "left_contact": V14 / "drafts/frames/keeper_prime_stair_left-contact-restrained_side-left_f01.png",
}
GENERATED = {
    "right_passing": PACK / "sources/generated/right-passing-balanced-lift.png",
    "right_contact": PACK / "sources/generated/right-contact-complete-toecap.png",
}
LEFT_CONTACT_BASE = V6 / "drafts/frames/keeper_prime_stair_left-leg_side-left_f04.png"


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


def polygon_mask(points: list[tuple[int, int]]) -> Image.Image:
    mask = Image.new("L", CELL, 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask


def lower_masked_content(source: Image.Image, mask: Image.Image, lower_px: int) -> Image.Image:
    """Lower the moving boot while keeping its hip/knee join registered."""
    output = source.copy()
    pixels = output.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if mask.getpixel((x, y)):
                pixels[x, y] = (0, 0, 0, 0)
    source_pixels = source.load()

    def sample(x: int, y: float) -> tuple[int, int, int, int]:
        y0 = max(0, min(CELL[1] - 1, int(y)))
        y1 = min(CELL[1] - 1, y0 + 1)
        fraction = y - y0
        return tuple(round(source_pixels[x, y0][channel] * (1 - fraction) + source_pixels[x, y1][channel] * fraction) for channel in range(4))  # type: ignore[return-value]

    transition_end = 202 + 28 + lower_px
    for target_y in range(202, 296):
        if target_y <= transition_end:
            source_y = (target_y + lower_px * 202 / 28) / (1 + lower_px / 28)
        else:
            source_y = target_y - lower_px
        for x in range(CELL[0]):
            if not mask.getpixel((x, target_y)) or not mask.getpixel((x, max(0, min(CELL[1] - 1, round(source_y))))):
                continue
            value = sample(x, source_y)
            if value[3] > 0:
                pixels[x, target_y] = value
    return output


def changed_outside(base: Image.Image, candidate: Image.Image, mask: Image.Image) -> int:
    changed = 0
    bp, cp = base.load(), candidate.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if mask.getpixel((x, y)) == 0 and bp[x, y] != cp[x, y]:
                changed += 1
    return changed


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(int(alpha.getpixel((x, y)) > 0) for x in range(CELL[0]) for y in (0, CELL[1] - 1)) + sum(int(alpha.getpixel((x, y)) > 0) for y in range(1, CELL[1] - 1) for x in (0, CELL[0] - 1))


def row_range(image: Image.Image, y: int, start_x: int, end_x: int) -> dict:
    xs = [x for x in range(start_x, end_x) if image.getpixel((x, y))[3] > ALPHA_THRESHOLD]
    if not xs:
        raise RuntimeError(f"no contact alpha at row {y}")
    return {"y": y, "minX": min(xs), "maxX": max(xs), "centreX": (min(xs) + max(xs)) / 2}


def opaque_bounds_in_mask(image: Image.Image, mask: Image.Image) -> list[int]:
    points = [(x, y) for y in range(CELL[1]) for x in range(CELL[0]) if mask.getpixel((x, y)) and image.getpixel((x, y))[3] > ALPHA_THRESHOLD]
    if not points:
        raise RuntimeError("masked region contains no opaque pixels")
    return [min(x for x, _ in points), min(y for _, y in points), max(x for x, _ in points) + 1, max(y for _, y in points) + 1]


def stair_surface_y(x_lp: float) -> float:
    if x_lp >= 116:
        return 20
    if x_lp < 18:
        return 80
    step = int((116 - x_lp - 1e-9) // 7) + 1
    return 20 + step * (60 / 14)


def moving_leg_clearance(image: Image.Image, mask: Image.Image, support: dict, support_tread: int) -> dict:
    support_x = 119.5 - support_tread * 7
    support_y = 20 + support_tread * (60 / 14)
    x_lp = support_x - support["centreX"] / 8 + 16
    bottom_lp = support_y - (320 - support["y"]) / 8
    values = []
    for y in range(205, 310):
        for x in range(CELL[0]):
            if mask.getpixel((x, y)) == 255 and image.getpixel((x, y))[3] > ALPHA_THRESHOLD:
                world_x = x_lp - 16 + x / 8
                world_y = bottom_lp + (320 - y) / 8
                values.append(world_y - stair_surface_y(world_x))
    return {"supportTread": support_tread, "minimumLp": min(values), "penetratingPixels": sum(value < -0.05 for value in values)}


def save(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=False, compress_level=9)


def main() -> None:
    for path in [*V14_FRAMES.values(), *GENERATED.values(), LEFT_CONTACT_BASE, V14 / "batch-register.json", V15 / "batch-register.json"]:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    FRAMES.mkdir(parents=True, exist_ok=True)
    REGISTERED.mkdir(parents=True, exist_ok=True)
    MASKS.mkdir(parents=True, exist_ok=True)

    originals = {key: Image.open(path).convert("RGBA") for key, path in V14_FRAMES.items()}

    # RIGHT compact passing: use only the newly studied moving leg.
    registered_passing, passing_registration = register_generated(Image.open(GENERATED["right_passing"]).convert("RGBA"), originals["right_passing"])
    # Stop the ownership mask at the moving boot. The generated full-character
    # study's planted boot reaches farther left than V14's and must never be
    # allowed into this mask or the stair-clearance measurement.
    passing_mask = polygon_mask([(48, 202), (111, 202), (121, 226), (116, 250), (103, 284), (30, 284), (17, 269), (27, 229)])
    registered_passing = lower_masked_content(registered_passing, passing_mask, 6)
    right_passing = Image.composite(registered_passing, originals["right_passing"], passing_mask)

    # LEFT contact: restore only differences from the exact V6 base within the detached-remnant box.
    left_base = Image.open(LEFT_CONTACT_BASE).convert("RGBA")
    artefact_mask = Image.new("L", CELL, 0)
    ap = artefact_mask.load()
    for y in range(158, 202):
        for x in range(60, 91):
            if originals["left_contact"].getpixel((x, y)) != left_base.getpixel((x, y)):
                ap[x, y] = 255
    left_contact = Image.composite(left_base, originals["left_contact"], artefact_mask)

    # RIGHT contact: repair only the upper/front boot; preserve the exact sole/contact row.
    registered_toecap, toecap_registration = register_generated(Image.open(GENERATED["right_contact"]).convert("RGBA"), originals["right_contact"])
    toecap_mask = polygon_mask([(40, 238), (105, 232), (119, 245), (114, 278), (103, 280), (43, 280), (33, 270)])
    right_contact = Image.composite(registered_toecap, originals["right_contact"], toecap_mask)

    outputs = {
        "right_passing": FRAMES / "keeper_prime_stair_right-foot-passing-balanced_side-left_f01.png",
        "left_passing": FRAMES / "keeper_prime_stair_left-foot-passing-compact_side-left_f01.png",
        "right_contact": FRAMES / "keeper_prime_stair_right-contact-complete-toecap_side-left_f01.png",
        "left_contact": FRAMES / "keeper_prime_stair_left-contact-clean_side-left_f01.png",
    }
    candidates = {"right_passing": right_passing, "left_passing": originals["left_passing"], "right_contact": right_contact, "left_contact": left_contact}
    for key, image in candidates.items():
        if image.size != CELL or edge_alpha(image):
            raise RuntimeError(f"{key} violates the cell/gutter contract")
        save(outputs[key], image)
    evidence = {
        "right_passing": (registered_passing, passing_mask),
        "left_contact": (left_base, artefact_mask),
        "right_contact": (registered_toecap, toecap_mask),
    }
    for key, (registered, mask) in evidence.items():
        save(REGISTERED / f"{key}-registered.png", registered)
        save(MASKS / f"{key}-mask.png", mask)

    right_support = row_range(right_passing, 316, 110, CELL[0])
    left_prep = json.loads((V14 / "source-preparation-v14.json").read_text())
    left_passing_record = next(frame for frame in left_prep["passing"] if frame["movingLeg"] == "left")
    left_passing_mask = Image.open(ROOT / left_passing_record["mask"]["file"]).convert("L")
    records = {
        "right_passing": {
            "base": {"file": rel(V14_FRAMES["right_passing"]), "sha256": digest(V14_FRAMES["right_passing"])},
            "generatedStudy": {"file": rel(GENERATED["right_passing"]), "sha256": digest(GENERATED["right_passing"])},
            "registeredStudy": {"file": rel(REGISTERED / "right_passing-registered.png"), "sha256": digest(REGISTERED / "right_passing-registered.png"), **passing_registration},
            "mask": {"file": rel(MASKS / "right_passing-mask.png"), "sha256": digest(MASKS / "right_passing-mask.png")},
            "draft": {"file": rel(outputs["right_passing"]), "sha256": digest(outputs["right_passing"])},
            "supportSole": right_support,
            "movingBoundsExclusive": opaque_bounds_in_mask(right_passing, passing_mask),
            "stairClearance": moving_leg_clearance(right_passing, passing_mask, right_support, 1),
            "outsideMaskChangedPixels": changed_outside(originals["right_passing"], right_passing, passing_mask),
        },
        "left_passing": {
            "draft": {"file": rel(outputs["left_passing"]), "sha256": digest(outputs["left_passing"])},
            "v14Sha256": digest(V14_FRAMES["left_passing"]),
            "supportSole": left_passing_record["supportSole"],
            "movingBoundsExclusive": opaque_bounds_in_mask(originals["left_passing"], left_passing_mask),
            "stairClearance": left_passing_record["stairClearance"],
        },
        "left_contact": {
            "base": {"file": rel(V14_FRAMES["left_contact"]), "sha256": digest(V14_FRAMES["left_contact"])},
            "restorationAuthority": {"file": rel(LEFT_CONTACT_BASE), "sha256": digest(LEFT_CONTACT_BASE)},
            "mask": {"file": rel(MASKS / "left_contact-mask.png"), "sha256": digest(MASKS / "left_contact-mask.png")},
            "draft": {"file": rel(outputs["left_contact"]), "sha256": digest(outputs["left_contact"])},
            "outsideMaskChangedPixels": changed_outside(originals["left_contact"], left_contact, artefact_mask),
        },
        "right_contact": {
            "base": {"file": rel(V14_FRAMES["right_contact"]), "sha256": digest(V14_FRAMES["right_contact"])},
            "generatedStudy": {"file": rel(GENERATED["right_contact"]), "sha256": digest(GENERATED["right_contact"])},
            "registeredStudy": {"file": rel(REGISTERED / "right_contact-registered.png"), "sha256": digest(REGISTERED / "right_contact-registered.png"), **toecap_registration},
            "mask": {"file": rel(MASKS / "right_contact-mask.png"), "sha256": digest(MASKS / "right_contact-mask.png")},
            "draft": {"file": rel(outputs["right_contact"]), "sha256": digest(outputs["right_contact"])},
            "outsideMaskChangedPixels": changed_outside(originals["right_contact"], right_contact, toecap_mask),
        },
    }
    manifest = {
        "schema": "lighthouse-keeper/stair-ascent-source-preparation@16",
        "status": "three-defect-correction-awaiting-review",
        "authorities": {
            "v14Artwork": {"file": rel(V14 / "batch-register.json"), "sha256": digest(V14 / "batch-register.json")},
            "v15Timeline": {"file": rel(V15 / "batch-register.json"), "sha256": digest(V15 / "batch-register.json")},
        },
        "cell": list(CELL),
        "density": 8,
        "corrections": records,
    }
    (PACK / "source-preparation-v16.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "rightPassingClearance": records["right_passing"]["stairClearance"],
        "rightPassingBounds": records["right_passing"]["movingBoundsExclusive"],
        "passingMovingBottomExclusive": {"right": records["right_passing"]["movingBoundsExclusive"][3], "left": records["left_passing"]["movingBoundsExclusive"][3]},
        "leftContactMaskPixels": sum(value > 0 for value in artefact_mask.get_flattened_data()),
        "outsideMaskChanges": sum(records[key].get("outsideMaskChangedPixels", 0) for key in ("right_passing", "left_contact", "right_contact")),
    }, indent=2))


if __name__ == "__main__":
    main()
