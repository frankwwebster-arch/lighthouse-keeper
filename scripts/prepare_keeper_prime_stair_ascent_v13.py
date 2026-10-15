#!/usr/bin/env python3
"""Prepare two V13 mid-swing frames between exact approved V12 contacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v13"
V6 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v6"
V12 = ROOT / "art/drafts/keeper-prime-stair-ascent-2026-10-15-v12"
FRAMES = PACK / "drafts/frames"
EVIDENCE = PACK / "evidence/registered-arm-sources"
CELL = (256, 320)
ALPHA_THRESHOLD = 8

LEG_SOURCES = {
    # Pose 3 is the raised passing pose. Pose 2 reaches forward before the
    # boot has cleared a 4.286-lp riser and would visibly enter the stair.
    "right": V6 / "drafts/frames/keeper_prime_stair_right-leg_side-left_f03.png",
    "left": V6 / "drafts/frames/keeper_prime_stair_left-leg_side-left_f03.png",
}
ARM_SOURCES = {
    "right": PACK / "sources/generated/right-foot-mid-swing-arm-study.png",
    "left": PACK / "sources/generated/left-foot-mid-swing-arm-study-rejected.png",
}
REJECTED = list(ARM_SOURCES.values())


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


def arm_mask(leg: str) -> Image.Image:
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    if leg == "right":
        draw.polygon([(43, 142), (100, 128), (133, 151), (132, 216), (101, 238), (48, 235), (25, 205)], fill=255)
        draw.polygon([(130, 137), (174, 139), (203, 171), (205, 231), (177, 270), (136, 270), (128, 228), (133, 188)], fill=255)
    else:
        draw.polygon([(43, 142), (101, 128), (134, 150), (133, 216), (99, 238), (47, 235), (25, 203)], fill=255)
        draw.polygon([(130, 137), (176, 139), (207, 171), (210, 232), (180, 270), (136, 270), (128, 228), (133, 188)], fill=255)
    # Remove the original neutral hand completely. The registered arm source
    # owns this immediate hip/occlusion patch; lower legs remain protected.
    draw.polygon([(111, 207), (165, 207), (174, 270), (111, 270)], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.55))


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    count = 0
    for x in range(CELL[0]):
        count += int(alpha.getpixel((x, 0)) > 0) + int(alpha.getpixel((x, CELL[1] - 1)) > 0)
    for y in range(1, CELL[1] - 1):
        count += int(alpha.getpixel((0, y)) > 0) + int(alpha.getpixel((CELL[0] - 1, y)) > 0)
    return count


def support_sole(image: Image.Image) -> dict:
    alpha = image.getchannel("A")
    for y in range(CELL[1] - 1, 260, -1):
        xs = [x for x in range(96, 190) if alpha.getpixel((x, y)) > ALPHA_THRESHOLD]
        if xs:
            return {"y": y, "minX": min(xs), "maxX": max(xs), "centreX": (min(xs) + max(xs)) / 2}
    raise RuntimeError("support sole missing")


def main() -> None:
    for path in [*LEG_SOURCES.values(), *ARM_SOURCES.values(), *REJECTED, V12 / "batch-register.json"]:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    FRAMES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    records = []
    for leg in ("right", "left"):
        base = Image.open(LEG_SOURCES[leg]).convert("RGBA")
        generated = Image.open(ARM_SOURCES[leg]).convert("RGBA")
        registered, registration = register_generated(generated, base)
        registered_path = EVIDENCE / f"{leg}-foot-mid-swing-arm-source-registered.png"
        registered.save(registered_path, optimize=False, compress_level=9)
        # The generated studies already reached an endpoint-like arm extreme.
        # The coherent midpoint is the exact V6 passing drawing: both arms are
        # between extremes while the moving foot passes the planted support.
        output = base.copy()
        if edge_alpha(output):
            raise RuntimeError(f"{leg} mid-swing touches a cell edge")
        output_path = FRAMES / f"keeper_prime_stair_{leg}-foot-mid-swing_side-left_f01.png"
        # Preserve the selected passing pose byte-for-byte, including its PNG
        # encoding, so the source hash is itself the out-of-scope-pixel proof.
        output_path.write_bytes(LEG_SOURCES[leg].read_bytes())
        support = support_sole(output)
        records.append({
            "movingLeg": leg,
            "supportLeg": "left" if leg == "right" else "right",
            "phase": f"{leg} foot mid-swing with opposite arm forward",
            "legSource": {"file": rel(LEG_SOURCES[leg]), "sha256": digest(LEG_SOURCES[leg])},
            "rejectedArmStudy": {"file": rel(ARM_SOURCES[leg]), "sha256": digest(ARM_SOURCES[leg])},
            "registeredRejectedArmStudy": {"file": rel(registered_path), "sha256": digest(registered_path), **registration},
            "draft": {"file": rel(output_path), "sha256": digest(output_path)},
            "supportSole": support,
            "cell": list(CELL), "density": 8, "edgeAlpha": 0,
            "byteIdenticalToLegSource": True,
            "protected": {"entireFrameExactV6PassingPose": True},
        })
    manifest = {
        "schema": "lighthouse-keeper/stair-ascent-source-preparation@13",
        "status": "one-mid-swing-per-leg-awaiting-review",
        "approvedContactAuthority": {"file": rel(V12 / "batch-register.json"), "sha256": digest(V12 / "batch-register.json")},
        "method": "Exact V6 mid-swing/passing drawings between exact V12 contact endpoints; generated arm studies retained but rejected because they reached endpoint-like extremes too early",
        "rejectedArmSources": [{"file": rel(path), "sha256": digest(path), "reason": "endpoint-like arm extreme is wrong for the neutral passing midpoint"} for path in REJECTED],
        "frames": records,
    }
    (PACK / "source-preparation-v13.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"frames": len(records), "preparation": rel(PACK / "source-preparation-v13.json")}, indent=2))


if __name__ == "__main__":
    main()
