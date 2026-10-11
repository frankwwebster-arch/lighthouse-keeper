#!/usr/bin/env python3
"""Build the reversible half-speed walk-to-snooker route review draft."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
DRAFT = Path(__file__).resolve().parent
RAW = ROOT / "art/raw/keeper-first-batch"
OUT = DRAFT / "drafts"
EVIDENCE = DRAFT / "evidence"

CELL = (128, 160)
CANVAS = (320, 160)
ANCHOR = (128, 158)
SOURCE_ALPHA_THRESHOLD = 32
FINAL_ALPHA_THRESHOLD = 128
FIXED_SOURCE_SCALE = 0.14204545454545456


GENERATED_SOURCES = {
    "reach": ROOT / "art/drafts/keeper-standard-snooker-single-reach-2026-10-11-v1/generated/single-reach-pose-v5-fresh-two-arm-redraft.png",
    "cue_contact": ROOT / "art/drafts/keeper-standard-snooker-authoring-robustness-test-2026-10-11-v1/generated/cue-contact-v1.png",
    "mid_lean": DRAFT / "generated/mid-lean-v1.png",
    "deep_lean": ROOT / "art/drafts/keeper-standard-snooker-authoring-robustness-test-2026-10-11-v1/generated/deep-lean-v1-failed.png",
    "stroke_forward": DRAFT / "generated/stroke-forward-v1.png",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def threshold_bbox(alpha: Image.Image, threshold: int) -> tuple[int, int, int, int]:
    mask = alpha.point(lambda value: 255 if value >= threshold else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("Source contains no foreground pixels")
    return bbox


def normalize_generated(name: str, path: Path) -> tuple[Image.Image, dict]:
    source = Image.open(path).convert("RGBA")
    bbox = threshold_bbox(source.getchannel("A"), SOURCE_ALPHA_THRESHOLD)
    crop = source.crop(bbox)
    resized_size = (
        max(1, round(crop.width * FIXED_SOURCE_SCALE)),
        max(1, round(crop.height * FIXED_SOURCE_SCALE)),
    )
    resized = crop.resize(resized_size, Image.Resampling.LANCZOS)
    alpha = resized.getchannel("A").point(
        lambda value: 255 if value >= FINAL_ALPHA_THRESHOLD else 0
    )
    resized.putalpha(alpha)

    # Only the lowest 28 pixels can define the stance. This deliberately ignores
    # the cue, hands, coat and beard when locating the canonical foot anchor.
    bottom_top = max(0, resized.height - 28)
    bottom_bbox = alpha.crop((0, bottom_top, resized.width, resized.height)).getbbox()
    if bottom_bbox is None:
        raise ValueError(f"Could not locate boots for {name}")
    feet_left, _, feet_right, feet_bottom = bottom_bbox
    feet_center_x = (feet_left + feet_right) / 2
    feet_baseline_y = bottom_top + feet_bottom
    paste_x = round(ANCHOR[0] - feet_center_x)
    paste_y = round(ANCHOR[1] - feet_baseline_y)

    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(resized, (paste_x, paste_y))
    output = OUT / f"{name}.png"
    canvas.save(output)

    border_alpha = canvas.getchannel("A")
    border_opaque = {
        "top": border_alpha.crop((0, 0, CANVAS[0], 1)).getbbox() is not None,
        "right": border_alpha.crop((CANVAS[0] - 1, 0, CANVAS[0], CANVAS[1])).getbbox() is not None,
        "bottom": border_alpha.crop((0, CANVAS[1] - 1, CANVAS[0], CANVAS[1])).getbbox() is not None,
        "left": border_alpha.crop((0, 0, 1, CANVAS[1])).getbbox() is not None,
    }
    if any(border_opaque.values()):
        raise ValueError(f"{name} touches a shared canvas edge: {border_opaque}")
    evidence = {
        "name": name,
        "source": str(path.relative_to(ROOT)),
        "source_sha256": sha256(path),
        "source_size": list(source.size),
        "source_alpha_threshold": SOURCE_ALPHA_THRESHOLD,
        "source_foreground_bbox": list(bbox),
        "fixed_source_scale": FIXED_SOURCE_SCALE,
        "resized_foreground_size": list(resized_size),
        "foot_anchor_target": list(ANCHOR),
        "placement": [paste_x, paste_y],
        "final_alpha_threshold": FINAL_ALPHA_THRESHOLD,
        "output": str(output.relative_to(ROOT)),
        "output_sha256": sha256(output),
        "output_alpha_bbox": list(canvas.getchannel("A").getbbox()),
        "opaque_pixels_on_canvas_edges": border_opaque,
    }
    return canvas, evidence


def extract_strip(filename: str) -> list[Image.Image]:
    strip = Image.open(RAW / filename).convert("RGBA")
    if strip.height != CELL[1] or strip.width % CELL[0]:
        raise ValueError(f"Unexpected strip geometry: {filename} {strip.size}")
    return [
        strip.crop((index * CELL[0], 0, (index + 1) * CELL[0], CELL[1]))
        for index in range(strip.width // CELL[0])
    ]


def place_native(frame: Image.Image, mirror: bool = False) -> Image.Image:
    if mirror:
        frame = frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(frame, (ANCHOR[0] - 64, 0))
    return canvas


def preview_frame(sprite: Image.Image, label: str) -> Image.Image:
    scale = 2
    stage = Image.new("RGB", (CANVAS[0] * scale, CANVAS[1] * scale + 40), "#ece9e3")
    draw = ImageDraw.Draw(stage)
    tile = 16
    for y in range(40, stage.height, tile):
        for x in range(0, stage.width, tile):
            colour = "#dedbd5" if ((x // tile) + ((y - 40) // tile)) % 2 else "#f4f1eb"
            draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=colour)
    enlarged = sprite.resize((CANVAS[0] * scale, CANVAS[1] * scale), Image.Resampling.NEAREST)
    stage.paste(enlarged, (0, 40), enlarged)
    font = ImageFont.load_default(size=18)
    draw.text((12, 10), f"HALF SPEED  |  {label}", fill="#17233b", font=font)
    return stage


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    generated: dict[str, Image.Image] = {}
    normalization: list[dict] = []
    for name, path in GENERATED_SOURCES.items():
        generated[name], record = normalize_generated(name, path)
        normalization.append(record)

    walk = [place_native(frame) for frame in extract_strip("keeper_walk_cycle_f9.png")]
    stop = [place_native(frame) for frame in extract_strip("keeper_walk_stop_f5.png")]
    neutral = place_native(extract_strip("keeper_neutral_standing-side-right_f1.png")[0])
    turn_right_to_back = [place_native(frame) for frame in extract_strip("keeper_turn_back_f6.png")]
    left_to_back = extract_strip("keeper_turn_left_back_f6.png")
    turn_back_to_left = [place_native(frame) for frame in reversed(left_to_back)][1:]
    walk_start_left = [place_native(frame, mirror=True) for frame in extract_strip("keeper_walk_start_f5.png")]
    walk_left = [place_native(frame, mirror=True) for frame in extract_strip("keeper_walk_cycle_f9.png")]

    # Durations are exactly twice their source timing: 8 fps -> 250 ms and
    # 10.5 fps -> 190 ms. Authored action poses use an intentionally readable
    # half-speed review cadence of 500 ms.
    route: list[tuple[Image.Image, str, int]] = []
    route += [(frame, "WALK RIGHT", 250) for frame in walk]
    route += [(frame, "STOP", 250) for frame in stop]
    route += [(neutral, "EXACT CANON NEUTRAL", 500)]
    route += [(generated["reach"], "REACH", 500)]
    route += [(generated["cue_contact"], "CUE CONTACT", 500)]
    route += [(generated["mid_lean"], "LOWER", 500)]
    route += [(generated["deep_lean"], "AIM", 500)]
    route += [(generated["stroke_forward"], "STROKE 1", 500)]
    route += [(generated["deep_lean"], "RECOVER 1", 500)]
    route += [(generated["stroke_forward"], "STROKE 2", 500)]
    route += [(generated["deep_lean"], "RECOVER 2", 500)]
    route += [(generated["mid_lean"], "RISE", 500)]
    route += [(generated["cue_contact"], "CUE HELD", 500)]
    route += [(generated["reach"], "RELEASE CUE", 500)]
    route += [(neutral, "EXACT CANON NEUTRAL", 500)]
    route += [(frame, "TURN RIGHT TO BACK", 190) for frame in turn_right_to_back]
    route += [(frame, "TURN BACK TO LEFT", 190) for frame in turn_back_to_left]
    route += [(frame, "START WALK LEFT", 250) for frame in walk_start_left]
    route += [(frame, "WALK LEFT", 250) for frame in walk_left]

    for index, (frame, label, _) in enumerate(route):
        if frame.size != CANVAS:
            raise ValueError(f"Route frame {index} ({label}) has geometry {frame.size}")
        alpha = frame.getchannel("A")
        edges = (
            alpha.crop((0, 0, CANVAS[0], 1)),
            alpha.crop((CANVAS[0] - 1, 0, CANVAS[0], CANVAS[1])),
            alpha.crop((0, CANVAS[1] - 1, CANVAS[0], CANVAS[1])),
            alpha.crop((0, 0, 1, CANVAS[1])),
        )
        if any(edge.getbbox() is not None for edge in edges):
            raise ValueError(f"Route frame {index} ({label}) touches a canvas edge")

    preview = [preview_frame(frame, label) for frame, label, _ in route]
    durations = [duration for _, _, duration in route]
    gif_path = OUT / "keeper-walk-stop-snooker-turn-walk-half-speed.gif"
    preview[0].save(
        gif_path,
        save_all=True,
        append_images=preview[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )

    # The reviewer supports one constant FPS per strip. At 4 fps, the canonical
    # walk/stop frames retain their accepted 250 ms cadence and each authored
    # 500 ms action hold is represented by two identical frames. The 190 ms
    # canonical turn frames round to one 250 ms review frame.
    review_route: list[tuple[Image.Image, str]] = []
    for frame, label, duration in route:
        review_route.extend((frame, label) for _ in range(max(1, round(duration / 250))))
    review_strip = Image.new("RGBA", (CANVAS[0] * len(review_route), CANVAS[1]), (0, 0, 0, 0))
    review_frame_evidence = []
    for index, (frame, label) in enumerate(review_route):
        review_strip.alpha_composite(frame, (index * CANVAS[0], 0))
        bbox = frame.getchannel("A").getbbox()
        review_frame_evidence.append({
            "frame": index + 1,
            "routeLabel": label,
            "draftAlphaBox": list(bbox) if bbox else None,
            "opaqueBorderPixelCount": 0,
        })
    review_strip_path = OUT / f"keeper_snooker_route_review_f{len(review_route)}.png"
    review_strip.save(review_strip_path)
    review_sidecar = {
        "w": 80,
        "h": 40,
        "frames": len(review_route),
        "fps": 4,
        "density": 4,
        "anchor": [32, 40],
        "z": 50,
        "loop": True,
        "mirrorSafe": False,
        "facing": "complete-right-to-left-route",
        "interaction": "play-snooker-route-review",
        "assetRole": "clip",
        "startPose": "walking-side-right",
        "endPose": "walking-side-left",
        "reviewScale": [100, 100],
        "reviewOffset": [0, 0],
        "reviewOnly": True,
        "acceptedPreviewSha256": sha256(gif_path),
    }
    review_sidecar_path = OUT / f"keeper_snooker_route_review_f{len(review_route)}.json"
    review_sidecar_path.write_text(json.dumps(review_sidecar, indent=2) + "\n")

    key_poses = [
        (neutral, "CANON NEUTRAL"),
        (generated["reach"], "REACH"),
        (generated["cue_contact"], "CUE CONTACT"),
        (generated["mid_lean"], "LOWER"),
        (generated["deep_lean"], "AIM"),
        (generated["stroke_forward"], "STROKE"),
        (neutral, "CANON NEUTRAL"),
    ]
    tiles = [preview_frame(sprite, label) for sprite, label in key_poses]
    sheet = Image.new("RGB", (tiles[0].width * 2, tiles[0].height * 4), "white")
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % 2) * tile.width, (index // 2) * tile.height))
    contact_path = OUT / "snooker-action-key-poses-contact-sheet.png"
    sheet.save(contact_path)

    manifest = {
        "status": "visually-accepted-draft-not-yet-promoted",
        "visual_acceptance": {
            "accepted_by": "Frank",
            "accepted_on": "2026-10-11",
            "accepted_preview_sha256": sha256(gif_path),
            "scope": "complete half-speed walk-stop-snooker-turn-walk sequence",
        },
        "production_assets_changed": False,
        "preview": str(gif_path.relative_to(ROOT)),
        "preview_sha256": sha256(gif_path),
        "key_pose_contact_sheet": str(contact_path.relative_to(ROOT)),
        "key_pose_contact_sheet_sha256": sha256(contact_path),
        "canvas": list(CANVAS),
        "anchor": list(ANCHOR),
        "frame_count": len(route),
        "duration_ms": sum(durations),
        "review_strip": {
            "path": str(review_strip_path.relative_to(ROOT)),
            "sha256": sha256(review_strip_path),
            "sidecar": str(review_sidecar_path.relative_to(ROOT)),
            "sidecar_sha256": sha256(review_sidecar_path),
            "frames": len(review_route),
            "fps": 4,
            "duration_ms": len(review_route) * 250,
            "timing_conversion": "250 ms route frames occur once; 500 ms route frames occur twice; 190 ms turn frames round to one 250 ms review frame",
            "frame_evidence": review_frame_evidence,
        },
        "loop": True,
        "verification": {
            "all_route_frames_match_canvas_geometry": True,
            "all_route_frames_have_clear_canvas_edges": True,
            "stop_last_equals_neutral": stop[-1].tobytes() == neutral.tobytes(),
            "neutral_equals_turn_first": neutral.tobytes() == turn_right_to_back[0].tobytes(),
            "right_turn_back_equals_left_turn_back": turn_right_to_back[-1].tobytes()
            == place_native(left_to_back[-1]).tobytes(),
            "left_turn_end_equals_mirrored_walk_start": turn_back_to_left[-1].tobytes()
            == walk_start_left[0].tobytes(),
        },
        "route": [
            {"frame": index, "label": label, "duration_ms": duration}
            for index, (_, label, duration) in enumerate(route)
        ],
        "normalization": normalization,
        "canonical_sources": [
            {
                "path": str((RAW / filename).relative_to(ROOT)),
                "sha256": sha256(RAW / filename),
            }
            for filename in (
                "keeper_walk_cycle_f9.png",
                "keeper_walk_stop_f5.png",
                "keeper_neutral_standing-side-right_f1.png",
                "keeper_turn_back_f6.png",
                "keeper_turn_left_back_f6.png",
                "keeper_walk_start_f5.png",
            )
        ],
    }
    manifest_path = EVIDENCE / "build-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    canonical_strip = RAW / "keeper_snooker_f8.png"
    canonical_runtime = ROOT / "public/sprites/keeper_snooker.png"
    canonical_sidecar = RAW / "keeper_snooker_f8.json"
    register = {
        "draftId": "keeper_snooker-standard-canon-route-2026-10-11-v1",
        "animation": "keeper_snooker",
        "status": "active-review-draft",
        "label": "Accepted canonical-keeper snooker route",
        "selection": "Frank accepted the complete half-speed walk-right, stop, cue acquisition, two-stroke snooker action, cue release, turn and walk-left sequence on 2026-10-11. This registration requests a separate manual decision in the review platform and does not promote production art.",
        "canonical": {
            "strip": str(canonical_strip.relative_to(ROOT)),
            "stripSha256": sha256(canonical_strip),
            "runtime": str(canonical_runtime.relative_to(ROOT)),
            "runtimeSha256": sha256(canonical_runtime),
            "sidecar": str(canonical_sidecar.relative_to(ROOT)),
            "sidecarSha256": sha256(canonical_sidecar),
        },
        "draft": {
            "source": str(gif_path.relative_to(ROOT)),
            "sourceSha256": sha256(gif_path),
            "strip": str(review_strip_path.relative_to(ROOT)),
            "stripSha256": sha256(review_strip_path),
            "sidecar": str(review_sidecar_path.relative_to(ROOT)),
            "sidecarSha256": sha256(review_sidecar_path),
            "frames": len(review_route),
            "canvas": [80, 40],
            "density": 4,
            "anchor": [32, 40],
            "fixedSourceScale": FIXED_SOURCE_SCALE,
            "acceptedPreviewSha256": sha256(gif_path),
            "frameEvidence": review_frame_evidence,
            "evidence": [
                str((OUT / "snooker-action-key-poses-contact-sheet.png").relative_to(ROOT)),
                str(gif_path.relative_to(ROOT)),
                str(manifest_path.relative_to(ROOT)),
            ],
        },
        "rollback": "Remove this exact-name registry entry and its published review-only strip; canonical raw/runtime sprites and the runtime manifest are untouched.",
    }
    register_path = DRAFT / "draft-register.json"
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({
        "preview": str(gif_path),
        "sha256": manifest["preview_sha256"],
        "contact_sheet": str(contact_path),
        "review_strip": str(review_strip_path),
        "review_frames": len(review_route),
        "register": str(register_path),
        "frames": len(route),
        "duration_ms": sum(durations),
        "manifest": str(manifest_path),
    }, indent=2))


if __name__ == "__main__":
    main()
