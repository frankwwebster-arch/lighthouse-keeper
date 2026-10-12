#!/usr/bin/env python3
"""Build the reversible Keeper Prime core-transition Draft V1.

Generated sheets are treated as pose sources. Shared endpoints are restored from
the registered Keeper Prime front/side states after deterministic normalisation.
Nothing in raw or runtime art is changed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "art/raw/keeper-first-batch"
BATCH_ID = "keeper-prime-core-transitions-2026-10-12-v1"
BATCH = ROOT / "art/drafts" / BATCH_ID
SOURCES = BATCH / "generated-sources"
DRAFTS = BATCH / "drafts"
EVIDENCE = BATCH / "evidence"
SIDE = ROOT / "art/drafts/keeper-prime-side-foundation-2026-10-12-v1/drafts/keeper_prime_neutral_standing-side-right_f1.png"
FRONT = ROOT / "art/raw/keeper-first-batch/keeper_neutral_standing-front_f1.png"
SUPERSEDED_NEAR_FRONT = SOURCES / "keeper_prime_turn_front_near-front-generated.png"

SOURCE_FILES = {
    "walk": SOURCES / "keeper_prime_walk_cycle-generated.png",
    "back": SOURCES / "keeper_prime_neutral_standing-back-generated.png",
    "front_turn": SOURCES / "keeper_prime_turn_front-generated.png",
    "front_near_side": SOURCES / "keeper_prime_turn_front_near-side-generated.png",
    "front_near_sequence": SOURCES / "keeper_prime_turn_front_near-sequence-generated.png",
    "back_turn": SOURCES / "keeper_prime_turn_back-generated.png",
    "sit": SOURCES / "keeper_prime_sit_side-generated.png",
}
CANONICAL_FILES = {
    "walk": RAW / "keeper_walk_cycle_f9.png",
    "stop": RAW / "keeper_walk_stop_f5.png",
    "front_turn": RAW / "keeper_turn_front_f6.png",
    "back_turn": RAW / "keeper_turn_back_f6.png",
    "sit": RAW / "keeper_sit_side_f6.png",
    "back": RAW / "keeper_neutral_standing-back_f1.png",
}

EXPECTED = {
    "side": "6f782bb4d59003166b34573b3109d40bae5c408fc108106e256153d80f8c8e3f",
    "front": "6d3b5057f7dad4410230c5c2a1959a2db468aca6f2d28486ec6db9e07827056a",
    "walk": "209846c41e2b0c7cf84b641094a44b22a637cfb637bdd1f838b08b79e0167a77",
    "back": "c8214ace6ba79de9ee05a4f276ef91976ab25b7a818baa61a9efeefae1b49bcf",
    "front_turn": "2a82458c2e3c0d2468970023dd7f0af6330f9f29a9c9aaa52ee72c2300fa5c08",
    "front_near_side": "1818c9a3104892d24e1ef3424e18a35ca5a2721a92ad890bf6a70b42874519af",
    "front_near_sequence": "4a24acca1e7ba58e14b2eb4bae713369c0b7e2ff8a21c69d1582477dd1d049cf",
    "back_turn": "96c603966eb91cd0136dbc5d06ba3ebbdaf4dab04155a02ca454aafb261a9adf",
    "sit": "36a48456ba509a3987220b2039b8e00962c342e87df570d53d1ef98fa3891d09",
    "superseded_near_front": "ed707416cfd63d5960fe91e39e1b3aaff9b8e50daf72ffdb7245e1a9d125d684",
    "canonical_walk": "dbd4e1827753ed384371044f3e976bef5c7529ce0f40cabfc4249902407b7e3c",
    "canonical_stop": "ed7c58911ea9c5dfa56e7bed2e67e106740d88835e860ffaa16ac18dd9d8a6e5",
    "canonical_front_turn": "cab51cb946eb39e1a05e2665ccff7f0f3cb6523621d42a4766ccb8212d86b57b",
    "canonical_back_turn": "b950027233b2005897fcc2056f993ff0d9d38c1f4501b60ad31d1c6cba29b635",
    "canonical_sit": "b5030c9ef9758bb684370a85178f6456ef0244f3221ac0adc5f8418eb131b7f5",
    "canonical_back": "9bf53472c3ebf1c93cdba8f0a6bec7acb45d2a8f02e5ff117105efe90b39e422",
}

PROMPT_SUMMARIES = {
    "walk": "Keeper Prime identity-preserving nine-frame right walk; old walk supplied choreography only; exact side-neutral endpoints; transparent isolated poses.",
    "back": "Keeper Prime exact directly-away neutral; front and derived side bound identity; old back supplied orientation only.",
    "front_turn": "Six-step exact side-to-exact-front Keeper Prime turn; old turn supplied rotation choreography only.",
    "front_near_side": "Keeper Prime 72-degree near-side correction derived directly from the exact side to prevent an early model/scale jump.",
    "front_near_sequence": "Keeper Prime 54/36/18-degree near-front corrections derived directly from the exact front to prevent an endpoint model/scale jump.",
    "back_turn": "Six-step exact side-to-exact-back Keeper Prime turn; old turn supplied rotation choreography only.",
    "sit": "Six-step exact side-neutral-to-seated Keeper Prime motion; old sit supplied body mechanics only; no chair drawn.",
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


def threshold_bbox(image: Image.Image, threshold: int = 32) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").point(lambda value: 255 if value >= threshold else 0).getbbox()
    if bbox is None:
        raise RuntimeError("image has no foreground")
    return bbox


def split_generated(source: Image.Image, expected: int) -> list[Image.Image]:
    alpha = source.getchannel("A")
    occupied = [x for x in range(source.width) if any(alpha.getpixel((x, y)) >= 32 for y in range(source.height))]
    groups: list[list[int]] = []
    for x in occupied:
        if not groups or x > groups[-1][-1] + 1:
            groups.append([x])
        else:
            groups[-1].append(x)
    if len(groups) != expected:
        raise RuntimeError(f"expected {expected} isolated poses, found {len(groups)}")
    poses = []
    for group in groups:
        left, right = max(0, group[0] - 4), min(source.width, group[-1] + 5)
        column = source.crop((left, 0, right, source.height))
        box = threshold_bbox(column)
        poses.append(column.crop((box[0], box[1], box[2], box[3])))
    return poses


def normalize_poses(source: Image.Image, expected: int, endpoint: Image.Image) -> tuple[list[Image.Image], dict]:
    poses = split_generated(source, expected)
    endpoint_box = threshold_bbox(endpoint)
    target_height = endpoint_box[3] - endpoint_box[1]
    first_box = threshold_bbox(poses[0])
    scale = target_height / (first_box[3] - first_box[1])
    predicted_first_width = max(1, round((first_box[2] - first_box[0]) * scale))
    horizontal_factor = (endpoint_box[2] - endpoint_box[0]) / predicted_first_width
    frames: list[Image.Image] = []
    source_boxes: list[list[int]] = []
    normal_boxes: list[list[int]] = []
    for pose in poses:
        box = threshold_bbox(pose)
        crop = pose.crop(box)
        width = max(1, round(crop.width * scale * horizontal_factor))
        height = max(1, round(crop.height * scale))
        resized = crop.resize((width, height), Image.Resampling.LANCZOS)
        resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        rb = threshold_bbox(resized, 1)
        frame = Image.new("RGBA", endpoint.size, (0, 0, 0, 0))
        paste_x = round(64 - (rb[0] + rb[2]) / 2)
        paste_y = 158 - rb[3]
        frame.alpha_composite(resized, (paste_x, paste_y))
        fb = threshold_bbox(frame, 1)
        if fb[0] < 2 or fb[1] < 2 or fb[2] > 126 or fb[3] > 158:
            raise RuntimeError(f"normalised pose lost transparent safety gutter: {fb}")
        frames.append(frame)
        source_boxes.append(list(box))
        normal_boxes.append(list(fb))
    return frames, {
        "sourcePoseBoundsExclusive": source_boxes,
        "normalisedPoseBoundsExclusive": normal_boxes,
        "scale": round(scale, 8),
        "horizontalFactor": round(horizontal_factor, 8),
        "baselineExclusive": 158,
        "centreX": 64,
    }


def normalize_single(source: Image.Image, target_height: int = 149) -> tuple[Image.Image, dict]:
    box = threshold_bbox(source)
    crop = source.crop(box)
    width = round(crop.width * target_height / crop.height)
    resized = crop.resize((width, target_height), Image.Resampling.LANCZOS)
    resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
    rb = threshold_bbox(resized, 1)
    frame = Image.new("RGBA", (128, 160), (0, 0, 0, 0))
    frame.alpha_composite(resized, (round(64 - (rb[0] + rb[2]) / 2), 158 - rb[3]))
    fb = threshold_bbox(frame, 1)
    if fb[0] < 2 or fb[1] < 2 or fb[2] > 126 or fb[3] > 158:
        raise RuntimeError(f"back neutral lost transparent safety gutter: {fb}")
    return frame, {"sourceBoundsExclusive": list(box), "normalisedBoundsExclusive": list(fb), "targetOpaqueHeight": target_height}


def converge_turn_envelope(frames: list[Image.Image], start: Image.Image, end: Image.Image) -> tuple[list[Image.Image], list[int]]:
    """Fit turn silhouettes to a linear endpoint envelope without touching endpoints."""
    start_box, end_box = threshold_bbox(start, 1), threshold_bbox(end, 1)
    start_width, end_width = start_box[2] - start_box[0], end_box[2] - end_box[0]
    targets = [round(start_width + (end_width - start_width) * index / (len(frames) - 1)) for index in range(len(frames))]
    result: list[Image.Image] = []
    for index, (frame, target_width) in enumerate(zip(frames, targets)):
        if index == 0:
            result.append(start.copy())
            continue
        if index == len(frames) - 1:
            result.append(end.copy())
            continue
        box = threshold_bbox(frame, 1)
        crop = frame.crop(box)
        resized = crop.resize((target_width, crop.height), Image.Resampling.LANCZOS)
        resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        rb = threshold_bbox(resized, 1)
        fitted = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        fitted.alpha_composite(resized, (round(64 - (rb[0] + rb[2]) / 2), 158 - rb[3]))
        result.append(fitted)
    return result, targets


def fit_frame_width(frame: Image.Image, target_width: int) -> Image.Image:
    box = threshold_bbox(frame, 1)
    crop = frame.crop(box)
    resized = crop.resize((target_width, crop.height), Image.Resampling.LANCZOS)
    resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
    rb = threshold_bbox(resized, 1)
    fitted = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    fitted.alpha_composite(resized, (round(64 - (rb[0] + rb[2]) / 2), 158 - rb[3]))
    return fitted


def edge_alpha(frame: Image.Image) -> int:
    alpha = frame.getchannel("A")
    points = {(x, 0) for x in range(frame.width)} | {(x, frame.height - 1) for x in range(frame.width)}
    points |= {(0, y) for y in range(frame.height)} | {(frame.width - 1, y) for y in range(frame.height)}
    return sum(alpha.getpixel(point) > 0 for point in points)


def validate_frames(name: str, frames: list[Image.Image]) -> None:
    for index, frame in enumerate(frames, 1):
        if frame.size != (128, 160):
            raise RuntimeError(f"{name} F{index} has wrong cell size")
        if sorted(set(frame.getchannel("A").tobytes())) != [0, 255]:
            raise RuntimeError(f"{name} F{index} alpha is not binary")
        if edge_alpha(frame):
            raise RuntimeError(f"{name} F{index} touches a cell edge")


def save_asset(name: str, frames: list[Image.Image], fps: float, start_pose: str, end_pose: str, *, loop: bool = False, reverse_for: str | None = None) -> dict:
    validate_frames(name, frames)
    strip = Image.new("RGBA", (128 * len(frames), 160), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * 128, 0))
    png = DRAFTS / f"{name}_f{len(frames)}.png"
    sidecar = DRAFTS / f"{name}_f{len(frames)}.json"
    png.parent.mkdir(parents=True, exist_ok=True)
    strip.save(png, optimize=False, compress_level=9)
    metadata = {
        "w": 32, "h": 40, "frames": len(frames), "fps": fps, "density": 4,
        "anchor": [16, 40], "z": 50, "loop": loop, "mirrorSafe": True,
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
        "frameBoundsExclusive": [list(threshold_bbox(frame, 1)) for frame in frames],
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


def save_evidence(assets: list[tuple[str, list[Image.Image]]]) -> None:
    font = ImageFont.load_default()
    rows = []
    for label, frames in assets:
        row = Image.new("RGBA", (len(frames) * 128 * 2, 160 * 2 + 34), "#102f3a")
        ImageDraw.Draw(row).text((10, 10), label, fill="#f2ca70", font=font)
        for index, frame in enumerate(frames):
            card = checker(frame.size)
            card.alpha_composite(frame)
            row.alpha_composite(card.resize((256, 320), Image.Resampling.NEAREST), (index * 256, 34))
        rows.append(row)
    width = max(row.width for row in rows)
    result = Image.new("RGBA", (width, sum(row.height for row in rows)), "#102f3a")
    y = 0
    for row in rows:
        result.alpha_composite(row, (0, y))
        y += row.height
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    result.save(EVIDENCE / "keeper-prime-core-transitions-v1.png", optimize=False, compress_level=9)


def main() -> None:
    for key, path in {"side": SIDE, "front": FRONT, **SOURCE_FILES}.items():
        if sha256(path) != EXPECTED[key]:
            raise RuntimeError(f"pinned {key} input changed")
    if sha256(SUPERSEDED_NEAR_FRONT) != EXPECTED["superseded_near_front"]:
        raise RuntimeError("pinned superseded near-front source changed")
    for key, path in CANONICAL_FILES.items():
        if sha256(path) != EXPECTED[f"canonical_{key}"]:
            raise RuntimeError(f"pinned canonical comparison {key} changed")

    side = Image.open(SIDE).convert("RGBA")
    front = Image.open(FRONT).convert("RGBA")
    back, back_normalisation = normalize_single(Image.open(SOURCE_FILES["back"]).convert("RGBA"))

    walk, walk_normalisation = normalize_poses(Image.open(SOURCE_FILES["walk"]).convert("RGBA"), 9, side)
    for index in (0, 4, 8):
        walk[index] = side.copy()

    front_turn, front_normalisation = normalize_poses(Image.open(SOURCE_FILES["front_turn"]).convert("RGBA"), 6, side)
    front_turn, front_targets = converge_turn_envelope(front_turn, side, front)
    near_side, near_side_normalisation = normalize_single(Image.open(SOURCE_FILES["front_near_side"]).convert("RGBA"))
    front_turn[1] = fit_frame_width(near_side, front_targets[1])
    near_sequence, near_sequence_normalisation = normalize_poses(Image.open(SOURCE_FILES["front_near_sequence"]).convert("RGBA"), 3, front)
    for index, target_width in enumerate(front_targets[2:5]):
        front_turn[index + 2] = fit_frame_width(near_sequence[index], target_width)

    back_turn, back_turn_normalisation = normalize_poses(Image.open(SOURCE_FILES["back_turn"]).convert("RGBA"), 6, side)
    back_turn, back_targets = converge_turn_envelope(back_turn, side, back)

    sit, sit_normalisation = normalize_poses(Image.open(SOURCE_FILES["sit"]).convert("RGBA"), 6, side)
    sit[0] = side.copy()

    stop = [walk[5].copy(), walk[6].copy(), walk[7].copy(), side.copy()]
    stand = list(reversed([frame.copy() for frame in sit]))

    asset_records = [
        save_asset("keeper_prime_walk_cycle", walk, 8, "standing-side-right", "standing-side-right", loop=True),
        save_asset("keeper_prime_walk_stop", stop, 8, "walking-side-right", "standing-side-right", reverse_for="keeper_prime_walk_start"),
        save_asset("keeper_prime_turn_front", front_turn, 6, "standing-side-right", "standing-front", reverse_for="keeper_prime_turn_side_from_front"),
        save_asset("keeper_prime_turn_back", back_turn, 6, "standing-side-right", "standing-back", reverse_for="keeper_prime_turn_side_from_back"),
        save_asset("keeper_prime_sit_side", sit, 6, "standing-side-right", "sitting-side-right", reverse_for="keeper_prime_stand_side"),
        save_asset("keeper_prime_stand_side", stand, 6, "sitting-side-right", "standing-side-right"),
        save_asset("keeper_prime_neutral_standing-back", [back], 0, "standing-back", "standing-back"),
    ]
    save_evidence([
        ("WALK CYCLE — F1/F5/F9 EXACT SIDE STOP", walk),
        ("WALK TO STOP — REVERSE IS START", stop),
        ("SIDE TO EXACT KEEPER PRIME FRONT", front_turn),
        ("SIDE TO EXACT REAR", back_turn),
        ("STOP TO SIT — REVERSE IS STAND", sit),
    ])

    exact = {
        "walkNeutralFramesExact": all(walk[index].tobytes() == side.tobytes() for index in (0, 4, 8)),
        "stopEndpointExact": stop[-1].tobytes() == side.tobytes(),
        "frontTurnStartExact": front_turn[0].tobytes() == side.tobytes(),
        "frontTurnEndByteIdentity": front_turn[-1].tobytes() == front.tobytes(),
        "backTurnStartExact": back_turn[0].tobytes() == side.tobytes(),
        "backTurnEndExact": back_turn[-1].tobytes() == back.tobytes(),
        "sitStartExact": sit[0].tobytes() == side.tobytes(),
        "standExactReverse": all(a.tobytes() == b.tobytes() for a, b in zip(stand, reversed(sit))),
    }
    if not all(exact.values()):
        raise RuntimeError(f"shared endpoint contract failed: {exact}")

    evidence = EVIDENCE / "keeper-prime-core-transitions-v1.png"
    register = {
        "batchId": BATCH_ID,
        "status": "draft-awaiting-visual-approval",
        "identity": {"name": "Keeper Prime", "shorthand": "KP", "front": rel(FRONT), "frontSha256": sha256(FRONT), "side": rel(SIDE), "sideSha256": sha256(SIDE)},
        "generatedSources": {key: {"file": rel(path), "sha256": sha256(path), "tool": "built-in image_gen", "promptSummary": PROMPT_SUMMARIES[key]} for key, path in SOURCE_FILES.items()},
        "canonicalComparisons": {key: {"file": rel(path), "sha256": sha256(path), "authority": "production comparison/choreography only; not Keeper Prime identity"} for key, path in CANONICAL_FILES.items()},
        "supersededGeneratedSources": [{"file": rel(SUPERSEDED_NEAR_FRONT), "sha256": sha256(SUPERSEDED_NEAR_FRONT), "reason": "single near-front correction still produced an abrupt F4→F5 scale change; retained as rejected provenance only"}],
        "normalisation": {
            "walk": walk_normalisation,
            "back": back_normalisation,
            "frontTurn": {**front_normalisation, "convergedWidths": front_targets, "nearSideCorrection": near_side_normalisation, "nearFrontSequence": near_sequence_normalisation},
            "backTurn": {**back_turn_normalisation, "convergedWidths": back_targets},
            "sit": sit_normalisation,
        },
        "assets": asset_records,
        "exactEndpointChecks": exact,
        "deterministicChecks": {"binaryAlpha": True, "transparentCellEdges": True, "fixedCellGeometry": [128, 160], "logicalCell": [32, 40], "density": 4, "stripSidecarAgreement": True},
        "evidence": {"contactSheet": rel(evidence), "sha256": sha256(evidence)},
        "productionChanged": False,
        "rollback": f"Delete only {rel(BATCH)} and its public review copies. Raw/runtime art and manifests are unchanged.",
    }
    write_json(BATCH / "batch-register.json", register)
    (BATCH / "HANDOFF.md").write_text(
        "# Keeper Prime core transitions — Draft V1\n\n"
        "Status: **awaiting visual approval; production unchanged**.\n\n"
        "This reversible batch establishes the six requested review routes around one exact Keeper Prime side stop: walk→stop; stop→walk; walk→stop→exact front; walk→stop→exact back; walk→stop→sit; and exact reversed sit→stand→walk. "
        "The old production strips supplied choreography only. Shared state pixels are exact, every cell is 128×160 RGBA with binary alpha and a transparent gutter, and no runtime file or manifest is modified.\n\n"
        "The workbench supplies residual root motion during the stop so the Keeper never walks on the spot.\n"
    )
    print(json.dumps({"batch": BATCH_ID, "assets": len(asset_records), "evidence": rel(evidence), "exactEndpointChecks": exact}, indent=2))


if __name__ == "__main__":
    main()
