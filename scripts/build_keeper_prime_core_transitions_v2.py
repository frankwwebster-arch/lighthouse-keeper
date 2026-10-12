#!/usr/bin/env python3
"""Build the reversible Keeper Prime core-transition Draft V2.

V2 preserves the approved V1 walk and deceleration byte-for-byte, removes the
duplicated stationary walk-start endpoint in the workbench recipe, and rebuilds
each rejected moving action from one coherent generated source sheet.  Raw,
runtime, V1 and approved historical Final art are never modified.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "art/drafts/keeper-prime-core-transitions-2026-10-12-v1"
BATCH_ID = "keeper-prime-core-transitions-2026-10-12-v2"
BATCH = ROOT / "art/drafts" / BATCH_ID
SOURCES = BATCH / "generated-sources"
DRAFTS = BATCH / "drafts"
EVIDENCE = BATCH / "evidence"
PROMPT_LOG = BATCH / "PROMPTS.md"
SIDE = ROOT / "art/drafts/keeper-prime-side-foundation-2026-10-12-v1/drafts/keeper_prime_neutral_standing-side-right_f1.png"
FRONT = ROOT / "art/raw/keeper-first-batch/keeper_neutral_standing-front_f1.png"
BACK = V1 / "drafts/keeper_prime_neutral_standing-back_f1.png"

GENERATED = {
    "front_turn": SOURCES / "keeper_prime_turn_front_coherent-generated.png",
    "back_turn": SOURCES / "keeper_prime_turn_back_coherent-generated.png",
    "sit": SOURCES / "keeper_prime_sit_side_coherent-generated.png",
}
V1_ASSETS = {
    "walk": V1 / "drafts/keeper_prime_walk_cycle_f9.png",
    "stop": V1 / "drafts/keeper_prime_walk_stop_f4.png",
    "back": V1 / "drafts/keeper_prime_neutral_standing-back_f1.png",
    "front_turn": V1 / "drafts/keeper_prime_turn_front_f6.png",
    "back_turn": V1 / "drafts/keeper_prime_turn_back_f6.png",
    "sit": V1 / "drafts/keeper_prime_sit_side_f6.png",
}
EXPECTED = {
    "side": "6f782bb4d59003166b34573b3109d40bae5c408fc108106e256153d80f8c8e3f",
    "front": "6d3b5057f7dad4410230c5c2a1959a2db468aca6f2d28486ec6db9e07827056a",
    "back": "1cddf5ac365c407bab5cdd16737a0be294db068d51aae73aff1234b48af478d6",
    "walk": "f2a8ccfab05ccfbc53935ea5687ed526ab124026fd03e1d30b31c1e76db5433c",
    "stop": "b2e90b69b9e3d1ad8b534516a6585417604638379b2cf377be559037abba66f2",
    "v1_front_turn": "535167c7b9c5694ccfefef7537d0e40e6df4c4633d859594a8d537aace9a75f6",
    "v1_back_turn": "d8511941c8eb0ccca945e351385b8b243394dccb61f3e4dd77a62888d31bdf3b",
    "v1_sit": "85c445f5df0d6d3cdb963d518949ad0d5c7bc592fc34705f4810b4e62ff458ec",
    "front_turn": "e56b08ceb16859d620fdbe085c46ab980d843590e38a1c8c14cf273d8ad408e2",
    "back_turn": "553dea73ce5497fe1585132934675c3781d5979273898d74332a3a6ee46c1422",
    "sit": "1233fdfba20c4d1d439c518fc49c559ea34d9870b1df9401cc530ce3be95b8f3",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixel_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def bbox(image: Image.Image, threshold: int = 1) -> tuple[int, int, int, int]:
    result = image.getchannel("A").point(lambda value: 255 if value >= threshold else 0).getbbox()
    if result is None:
        raise RuntimeError("empty foreground")
    return result


def split_source(source: Image.Image, expected: int = 6) -> list[Image.Image]:
    alpha = source.getchannel("A")
    occupied = [
        x for x in range(source.width)
        if alpha.crop((x, 0, x + 1, source.height)).getextrema()[1] >= 32
    ]
    groups: list[list[int]] = []
    for x in occupied:
        if not groups or x > groups[-1][-1] + 1:
            groups.append([x])
        else:
            groups[-1].append(x)
    if len(groups) != expected:
        raise RuntimeError(f"expected {expected} isolated poses, found {len(groups)}")
    poses: list[Image.Image] = []
    for group in groups:
        crop = source.crop((max(0, group[0] - 4), 0, min(source.width, group[-1] + 5), source.height))
        poses.append(crop.crop(bbox(crop, 32)))
    return poses


def normalise(source_path: Path, start: Image.Image, end: Image.Image | None = None) -> tuple[list[Image.Image], dict]:
    poses = split_source(Image.open(source_path).convert("RGBA"))
    start_box = bbox(start)
    first_box = bbox(poses[0], 32)
    scale = (start_box[3] - start_box[1]) / (first_box[3] - first_box[1])
    first_width = max(1, round((first_box[2] - first_box[0]) * scale))
    horizontal_factor = (start_box[2] - start_box[0]) / first_width
    frames: list[Image.Image] = []
    for pose in poses:
        source_box = bbox(pose, 32)
        crop = pose.crop(source_box)
        resized = crop.resize(
            (max(1, round(crop.width * scale * horizontal_factor)), max(1, round(crop.height * scale))),
            Image.Resampling.LANCZOS,
        )
        resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        rb = bbox(resized)
        frame = Image.new("RGBA", (128, 160), (0, 0, 0, 0))
        frame.alpha_composite(resized, (round(64 - (rb[0] + rb[2]) / 2), 158 - rb[3]))
        frames.append(frame)

    if end is not None:
        start_width = start_box[2] - start_box[0]
        end_box = bbox(end)
        end_width = end_box[2] - end_box[0]
        targets = [round(start_width + (end_width - start_width) * index / 5) for index in range(6)]
        for index in range(1, 5):
            frame_box = bbox(frames[index])
            crop = frames[index].crop(frame_box)
            resized = crop.resize((targets[index], crop.height), Image.Resampling.LANCZOS)
            resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
            rb = bbox(resized)
            frame = Image.new("RGBA", (128, 160), (0, 0, 0, 0))
            frame.alpha_composite(resized, (round(64 - (rb[0] + rb[2]) / 2), 158 - rb[3]))
            frames[index] = frame
    else:
        targets = [bbox(frame)[2] - bbox(frame)[0] for frame in frames]

    frames[0] = start.copy()
    if end is not None:
        frames[-1] = end.copy()
    return frames, {
        "generatedSource": rel(source_path),
        "generatedSourceSha256": sha256(source_path),
        "singleCoherentSource": True,
        "uniformScale": round(scale, 8),
        "uniformHorizontalFactor": round(horizontal_factor, 8),
        "targetWidths": targets,
        "centreX": 64,
        "standingBaselineExclusive": 158,
    }


def split_strip(path: Path, count: int) -> list[Image.Image]:
    strip = Image.open(path).convert("RGBA")
    if strip.size != (128 * count, 160):
        raise RuntimeError(f"unexpected strip geometry: {path}")
    return [strip.crop((index * 128, 0, (index + 1) * 128, 160)) for index in range(count)]


def edge_alpha(frame: Image.Image) -> int:
    alpha = frame.getchannel("A")
    points = {(x, 0) for x in range(128)} | {(x, 159) for x in range(128)}
    points |= {(0, y) for y in range(160)} | {(127, y) for y in range(160)}
    return sum(alpha.getpixel(point) > 0 for point in points)


def validate(name: str, frames: list[Image.Image]) -> None:
    for index, frame in enumerate(frames, 1):
        if frame.size != (128, 160):
            raise RuntimeError(f"{name} F{index} has wrong geometry")
        if sorted(set(frame.getchannel("A").tobytes())) != [0, 255]:
            raise RuntimeError(f"{name} F{index} alpha is not binary")
        if edge_alpha(frame):
            raise RuntimeError(f"{name} F{index} touches a cell edge")


def seam_metrics(frames: list[Image.Image]) -> list[dict]:
    values = []
    for index, (left, right) in enumerate(zip(frames, frames[1:]), 1):
        lb, rb = bbox(left), bbox(right)
        la = sum(left.getchannel("A").tobytes()) // 255
        ra = sum(right.getchannel("A").tobytes()) // 255
        lc = ((lb[0] + lb[2]) / 2, (lb[1] + lb[3]) / 2)
        rc = ((rb[0] + rb[2]) / 2, (rb[1] + rb[3]) / 2)
        values.append({
            "seam": f"F{index}->F{index + 1}",
            "widthDelta": (rb[2] - rb[0]) - (lb[2] - lb[0]),
            "heightDelta": (rb[3] - rb[1]) - (lb[3] - lb[1]),
            "centreDelta": [round(rc[0] - lc[0], 2), round(rc[1] - lc[1], 2)],
            "opaqueAreaRatio": round(ra / la, 4),
            "baselineDelta": rb[3] - lb[3],
        })
    return values


def save_asset(name: str, frames: list[Image.Image], fps: float, start_pose: str, end_pose: str, reverse_for: str | None = None) -> dict:
    validate(name, frames)
    strip = Image.new("RGBA", (128 * len(frames), 160), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * 128, 0))
    png = DRAFTS / f"{name}_f{len(frames)}.png"
    sidecar = png.with_suffix(".json")
    png.parent.mkdir(parents=True, exist_ok=True)
    strip.save(png, optimize=False, compress_level=9)
    metadata = {
        "w": 32, "h": 40, "frames": len(frames), "fps": fps, "density": 4,
        "anchor": [16, 40], "z": 50, "loop": False, "mirrorSafe": True,
        "facing": "right", "startPose": start_pose, "endPose": end_pose,
        "assetRole": "draft-bridge", "identity": "keeper_prime",
    }
    if reverse_for:
        metadata["reverseFor"] = reverse_for
    write_json(sidecar, metadata)
    return {
        "name": name, "strip": rel(png), "stripSha256": sha256(png),
        "sidecar": rel(sidecar), "sidecarSha256": sha256(sidecar),
        "framePixelSha256": [pixel_sha(frame) for frame in frames],
        "frameBoundsExclusive": [list(bbox(frame)) for frame in frames],
        "cellEdgeAlphaPixels": [edge_alpha(frame) for frame in frames],
        "seams": seam_metrics(frames),
    }


def copy_unchanged(name: str, frame_count: int) -> dict:
    source_png = V1 / "drafts" / f"{name}_f{frame_count}.png"
    source_json = source_png.with_suffix(".json")
    target_png = DRAFTS / source_png.name
    target_json = DRAFTS / source_json.name
    target_png.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_png, target_png)
    shutil.copyfile(source_json, target_json)
    frames = split_strip(target_png, frame_count)
    validate(name, frames)
    return {
        "name": name, "strip": rel(target_png), "stripSha256": sha256(target_png),
        "sidecar": rel(target_json), "sidecarSha256": sha256(target_json),
        "copiedByteForByteFrom": rel(source_png),
        "originalSha256": sha256(source_png),
        "unchanged": True,
        "framePixelSha256": [pixel_sha(frame) for frame in frames],
        "frameBoundsExclusive": [list(bbox(frame)) for frame in frames],
        "cellEdgeAlphaPixels": [edge_alpha(frame) for frame in frames],
    }


def checker(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGBA", size, "#dce3df")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], 12):
        for x in range(0, size[0], 12):
            if (x // 12 + y // 12) % 2:
                draw.rectangle((x, y, x + 11, y + 11), fill="#c9d2cd")
    return image


def evidence_row(label: str, frames: list[Image.Image]) -> Image.Image:
    row = Image.new("RGBA", (len(frames) * 192, 274), "#102f3a")
    ImageDraw.Draw(row).text((10, 9), label, fill="#f2ca70", font=ImageFont.load_default())
    for index, frame in enumerate(frames):
        card = checker(frame.size)
        card.alpha_composite(frame)
        row.alpha_composite(card.resize((192, 240), Image.Resampling.NEAREST), (index * 192, 34))
    return row


def save_evidence(comparisons: list[tuple[str, list[Image.Image]]]) -> Path:
    rows = [evidence_row(label, frames) for label, frames in comparisons]
    sheet = Image.new("RGBA", (max(row.width for row in rows), sum(row.height for row in rows)), "#102f3a")
    y = 0
    for row in rows:
        sheet.alpha_composite(row, (0, y))
        y += row.height
    path = EVIDENCE / "keeper-prime-core-transitions-v2-comparison.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=False, compress_level=9)
    return path


def main() -> None:
    if not PROMPT_LOG.exists():
        raise RuntimeError("missing V2 image-generation prompt log")
    pinned = {"side": SIDE, "front": FRONT, "back": BACK, **GENERATED}
    for key, path in pinned.items():
        if sha256(path) != EXPECTED[key]:
            raise RuntimeError(f"pinned {key} input changed")
    for key, path in V1_ASSETS.items():
        expected_key = key if key in {"walk", "stop"} else f"v1_{key}" if key != "back" else "back"
        if sha256(path) != EXPECTED[expected_key]:
            raise RuntimeError(f"pinned V1 {key} changed")

    side = Image.open(SIDE).convert("RGBA")
    front = Image.open(FRONT).convert("RGBA")
    back = Image.open(BACK).convert("RGBA")
    front_turn, front_norm = normalise(GENERATED["front_turn"], side, front)
    back_turn, back_norm = normalise(GENERATED["back_turn"], side, back)
    sit, sit_norm = normalise(GENERATED["sit"], side)
    stand = [frame.copy() for frame in reversed(sit)]

    assets = [
        copy_unchanged("keeper_prime_walk_cycle", 9),
        copy_unchanged("keeper_prime_walk_stop", 4),
        save_asset("keeper_prime_turn_front", front_turn, 6, "standing-side-right", "standing-front", "keeper_prime_turn_side_from_front"),
        save_asset("keeper_prime_turn_back", back_turn, 6, "standing-side-right", "standing-back", "keeper_prime_turn_side_from_back"),
        save_asset("keeper_prime_sit_side", sit, 6, "standing-side-right", "sitting-side-right", "keeper_prime_stand_side"),
        save_asset("keeper_prime_stand_side", stand, 6, "sitting-side-right", "standing-side-right"),
        copy_unchanged("keeper_prime_neutral_standing-back", 1),
    ]

    exact = {
        "walkAndStopByteIdenticalToV1": all(record.get("unchanged") for record in (assets[0], assets[1])),
        "frontTurnStartExact": front_turn[0].tobytes() == side.tobytes(),
        "frontTurnEndByteIdentity": front_turn[-1].tobytes() == front.tobytes(),
        "backTurnStartExact": back_turn[0].tobytes() == side.tobytes(),
        "backTurnEndExact": back_turn[-1].tobytes() == back.tobytes(),
        "sitStartExact": sit[0].tobytes() == side.tobytes(),
        "standExactReverse": all(a.tobytes() == b.tobytes() for a, b in zip(stand, reversed(sit))),
    }
    if not all(exact.values()):
        raise RuntimeError(f"endpoint contract failed: {exact}")

    critical = {
        "frontF2ToF3": seam_metrics(front_turn)[1],
        "backF2ToF3": seam_metrics(back_turn)[1],
        "sitF2ToF3": seam_metrics(sit)[1],
    }
    for name, seam in critical.items():
        if abs(seam["widthDelta"]) > 8 or abs(seam["heightDelta"]) > 8 or not 0.82 <= seam["opaqueAreaRatio"] <= 1.18:
            raise RuntimeError(f"{name} exceeds deterministic continuity bounds: {seam}")

    evidence = save_evidence([
        ("V1 FRONT TURN — REJECTED SEAM", split_strip(V1_ASSETS["front_turn"], 6)),
        ("V2 FRONT TURN — ONE COHERENT SOURCE", front_turn),
        ("V1 BACK TURN — REJECTED SEAM", split_strip(V1_ASSETS["back_turn"], 6)),
        ("V2 BACK TURN — ONE COHERENT SOURCE", back_turn),
        ("V1 SIT — REJECTED RENDER-DENSITY JOIN", split_strip(V1_ASSETS["sit"], 6)),
        ("V2 SIT — ONE COHERENT SOURCE", sit),
        ("V2 STAND — EXACT REVERSE", stand),
    ])

    register = {
        "batchId": BATCH_ID,
        "status": "draft-awaiting-visual-approval",
        "userReviewBasis": {
            "route1": "accepted; deceleration preserved byte-for-byte",
            "route2": "shorten the stationary acceleration beat",
            "routes3And4": "replace the step 19->20 perspective/scale discontinuity",
            "routes5And6": "remove the apparent pixel-density mismatch around Keeper Prime",
        },
        "identity": {"name": "Keeper Prime", "shorthand": "KP", "front": rel(FRONT), "frontSha256": sha256(FRONT), "side": rel(SIDE), "sideSha256": sha256(SIDE)},
        "generatedSources": {key: {"file": rel(path), "sha256": sha256(path), "tool": "built-in image_gen", "singleAnimationSource": True} for key, path in GENERATED.items()},
        "promptLog": {"file": rel(PROMPT_LOG), "sha256": sha256(PROMPT_LOG), "tool": "built-in image_gen"},
        "normalisation": {"frontTurn": front_norm, "backTurn": back_norm, "sit": sit_norm},
        "criticalSeamChecks": critical,
        "assets": assets,
        "originalDraftComparisons": {key: {"file": rel(path), "sha256": sha256(path)} for key, path in V1_ASSETS.items()},
        "exactEndpointChecks": exact,
        "deterministicChecks": {
            "binaryAlpha": True,
            "transparentCellEdges": True,
            "fixedCellGeometry": [128, 160],
            "logicalCell": [32, 40],
            "density": 4,
            "stripSidecarAgreement": True,
            "walkStopOutOfScopePixelsUnchanged": True,
            "singleGeneratedSourcePerMovingAction": True,
            "criticalSeamLimits": {"absoluteWidthDeltaMax": 8, "absoluteHeightDeltaMax": 8, "opaqueAreaRatio": [0.82, 1.18]},
        },
        "evidence": {"contactSheet": rel(evidence), "sha256": sha256(evidence)},
        "productionChanged": False,
        "rollback": f"Delete only {rel(BATCH)} and its content-hashed public Draft copies; V1, raw, runtime, manifests and Final are unchanged.",
    }
    write_json(BATCH / "batch-register.json", register)
    (BATCH / "HANDOFF.md").write_text(
        "# Keeper Prime core transitions — Draft V2\n\n"
        "Status: **awaiting visual approval; production unchanged**.\n\n"
        "V2 preserves the accepted V1 walk and moving deceleration byte-for-byte. The front turn, back turn and sit are each rebuilt from one coherent six-pose source so the rejected route-step 19→20 seams no longer swap perspective, scale or rendering family. Stand remains the exact reverse of sit. The workbench removes the duplicated exact-stop frame from acceleration while keeping a short neutral beat.\n"
    )
    print(json.dumps({"batch": BATCH_ID, "assets": len(assets), "criticalSeams": critical, "evidence": rel(evidence)}, indent=2))


if __name__ == "__main__":
    main()
