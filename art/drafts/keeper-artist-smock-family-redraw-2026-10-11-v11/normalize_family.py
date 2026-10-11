#!/usr/bin/env python3
"""Normalize the V11 artist-smock family without altering body proportions."""

from __future__ import annotations

import hashlib
import io
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RAW = ROOT / "art/raw/keeper-first-batch"
GENERATED = HERE / "generated"
DRAFTS = HERE / "drafts"
EVIDENCE = HERE / "evidence"
THRESHOLD = 32


@dataclass(frozen=True)
class Clip:
    name: str
    frames: int
    generated: str
    reference: str
    layout: str
    canvas: tuple[int, int]
    fps: float
    generation_inputs: tuple[str, str, str]


CLIPS = [
    Clip("keeper_artist_smock_walk", 8, "keeper_artist_smock_walk-source.png", "keeper_walk_f8.png", "row", (128, 160), 4, ("v10", "canon-pack", "source:keeper-walk-generated-source.png")),
    Clip("keeper_artist_smock_turn_back", 6, "keeper_artist_smock_turn_back-source.png", "keeper_turn_back_f6.png", "row", (128, 160), 4, ("v10", "generated:keeper_artist_smock_walk-source.png", "source:keeper-turn-back-generated-source.png")),
    Clip("keeper_artist_smock_turn_front", 6, "keeper_artist_smock_turn_front-source.png", "keeper_turn_front_f6.png", "row", (128, 160), 4, ("v10", "generated:keeper_artist_smock_walk-source.png", "source:keeper-turn-front-generated-source.png")),
    Clip("keeper_artist_smock_sit_front", 6, "keeper_artist_smock_sit_front-source.png", "keeper_sit_front_f6.png", "row", (128, 160), 4.5, ("v10", "generated:keeper_artist_smock_walk-source.png", "source:keeper-sit-front-generated-source.png")),
    Clip("keeper_paint_side", 8, "keeper_paint_side-source.png", "keeper_paint_side_f8.png", "grid4x2", (160, 192), 4, ("v10", "generated:keeper_artist_smock_walk-source.png", "source:keeper-paint-side-generated-source.png")),
    Clip("keeper_paint_back", 8, "keeper_paint_back-source.png", "keeper_paint_back_f8.png", "grid4x2", (160, 192), 4, ("v10", "generated:keeper_artist_smock_turn_back-source.png", "source:keeper-paint-back-generated-source.png")),
    Clip("keeper_pottery_front", 8, "keeper_pottery_front-source.png", "keeper_pottery_front_f8.png", "row", (160, 160), 4, ("v10", "generated:keeper_artist_smock_sit_front-source.png", "source:keeper-pottery-front-generated-source.png")),
]

V10 = ROOT / "art/drafts/keeper-canon-model-pack-artist-smock-2026-10-11-v10/generated/artist-smock-fresh-source.png"
CANON_PACK = ROOT / "art/drafts/keeper-canon-model-pack-artist-smock-2026-10-11-v10/evidence/canon-model-pack.png"
SOURCE_DIR = ROOT / "art/source/keeper-first-batch"


def resolve_generation_input(value: str) -> Path:
    if value == "v10":
        return V10
    if value == "canon-pack":
        return CANON_PACK
    kind, filename = value.split(":", 1)
    if kind == "generated":
        return GENERATED / filename
    if kind == "source":
        return SOURCE_DIR / filename
    raise RuntimeError(f"unknown generation input {value}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_bytes(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, "PNG", optimize=False, compress_level=9)
    return out.getvalue()


def alpha_bbox(image: Image.Image, threshold: int = 1) -> tuple[int, int, int, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.where(alpha >= threshold)
    if not len(xs):
        raise RuntimeError("empty frame")
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def crop_to_foreground(image: Image.Image) -> Image.Image:
    return image.crop(alpha_bbox(image, THRESHOLD))


def split_row(image: Image.Image, count: int) -> list[Image.Image]:
    alpha = np.asarray(image.getchannel("A")) >= THRESHOLD
    occupied = alpha.any(axis=0)
    runs: list[tuple[int, int]] = []
    start = None
    for x, value in enumerate(occupied):
        if value and start is None:
            start = x
        if start is not None and (not value or x == len(occupied) - 1):
            runs.append((start, x if not value else x + 1))
            start = None
    if len(runs) != count:
        raise RuntimeError(f"expected {count} isolated row poses, found {len(runs)}")
    return [crop_to_foreground(image.crop((x0, 0, x1, image.height))) for x0, x1 in runs]


def split_grid(image: Image.Image, count: int) -> list[Image.Image]:
    if count != 8:
        raise RuntimeError("the isolated grid contract is 4x2 / 8 poses")
    alpha = np.asarray(image.getchannel("A")) >= THRESHOLD
    h, w = alpha.shape
    for x in (round(w / 4), round(w / 2), round(3 * w / 4)):
        if np.count_nonzero(alpha[:, max(0, x - 3):min(w, x + 4)]):
            raise RuntimeError(f"opaque source pixels cross grid boundary x={x}")
    y = round(h / 2)
    if np.count_nonzero(alpha[max(0, y - 3):min(h, y + 4), :]):
        raise RuntimeError(f"opaque source pixels cross grid boundary y={y}")
    frames = []
    for row in range(2):
        for col in range(4):
            x0, x1 = round(col * w / 4), round((col + 1) * w / 4)
            y0, y1 = round(row * h / 2), round((row + 1) * h / 2)
            frames.append(crop_to_foreground(image.crop((x0, y0, x1, y1))))
    return frames


def split_generated(clip: Clip) -> list[Image.Image]:
    image = Image.open(GENERATED / clip.generated).convert("RGBA")
    return split_row(image, clip.frames) if clip.layout == "row" else split_grid(image, clip.frames)


def split_reference(clip: Clip) -> list[Image.Image]:
    strip = Image.open(RAW / clip.reference).convert("RGBA")
    if strip.width % clip.frames:
        raise RuntimeError(f"reference geometry is not divisible: {clip.reference}")
    width = strip.width // clip.frames
    return [strip.crop((i * width, 0, (i + 1) * width, strip.height)) for i in range(clip.frames)]


def resize_hard(image: Image.Image, scale: float) -> Image.Image:
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    resized = image.resize(size, Image.Resampling.LANCZOS)
    rgba = np.asarray(resized).copy()
    opaque = rgba[:, :, 3] >= 128
    rgba[:, :, 3] = np.where(opaque, 255, 0).astype(np.uint8)
    rgba[~opaque, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def place_like_reference(image: Image.Image, reference: Image.Image, canvas: tuple[int, int]) -> Image.Image:
    ref_box = alpha_bbox(reference)
    image_box = alpha_bbox(image)
    width_shift = (canvas[0] - reference.width) / 2
    height_shift = canvas[1] - reference.height
    target_cx = (ref_box[0] + ref_box[2]) / 2 + width_shift
    target_bottom = ref_box[3] + height_shift
    x = round(target_cx - (image_box[0] + image_box[2]) / 2)
    y = round(target_bottom - image_box[3])
    if x + image_box[0] < 1 or x + image_box[2] > canvas[0] - 1 or y + image_box[1] < 1 or y + image_box[3] > canvas[1] - 1:
        raise RuntimeError(f"normalized frame does not fit {canvas}: placement {(x, y)}, bounds {image_box}")
    out = Image.new("RGBA", canvas, (0, 0, 0, 0))
    out.alpha_composite(image, (x, y))
    return out


def strip(frames: list[Image.Image]) -> Image.Image:
    out = Image.new("RGBA", (frames[0].width * len(frames), frames[0].height), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        out.alpha_composite(frame, (index * frame.width, 0))
    return out


def normalize_clip(clip: Clip) -> tuple[list[Image.Image], dict]:
    generated = split_generated(clip)
    references = split_reference(clip)
    generated_first = alpha_bbox(generated[0], THRESHOLD)
    reference_first = alpha_bbox(references[0])
    scale = (reference_first[3] - reference_first[1]) / (generated_first[3] - generated_first[1])
    frames = [place_like_reference(resize_hard(frame, scale), ref, clip.canvas) for frame, ref in zip(generated, references)]
    return frames, {
        "source": str((GENERATED / clip.generated).relative_to(ROOT)),
        "sourceSha256": sha256(GENERATED / clip.generated),
        "reference": str((RAW / clip.reference).relative_to(ROOT)),
        "referenceSha256": sha256(RAW / clip.reference),
        "layout": clip.layout,
        "uniformScale": scale,
        "canvas": list(clip.canvas),
        "frames": clip.frames,
        "fps": clip.fps,
    }


def frame_hash(frame: Image.Image) -> str:
    return hashlib.sha256(frame.tobytes()).hexdigest()


def save_sidecar(clip: Clip, output_path: Path) -> Path:
    density = 4
    sidecar = {
        "w": clip.canvas[0] // density,
        "h": clip.canvas[1] // density,
        "frames": clip.frames,
        "fps": clip.fps,
        "density": density,
        "anchor": [clip.canvas[0] // (2 * density), clip.canvas[1] // density],
        "z": 50,
        "outfit": "artist-smock",
        "draft": True,
    }
    path = output_path.with_suffix(".json")
    path.write_text(json.dumps(sidecar, indent=2) + "\n")
    return path


def save_derived_sidecar(name: str, output_path: Path, frames: int) -> Path:
    candidates = sorted(RAW.glob(f"{name}_f*.json"))
    if len(candidates) != 1:
        raise RuntimeError(f"expected one canonical sidecar for {name}, found {candidates}")
    sidecar = json.loads(candidates[0].read_text())
    image = Image.open(output_path).convert("RGBA")
    sidecar.update({
        "w": image.width // frames // 4,
        "h": image.height // 4,
        "frames": frames,
        "density": 4,
        "anchor": [image.width // frames // 8, image.height // 4],
        "draft": True,
        "draftFamily": "keeper-artist-smock-family-redraw-2026-10-11-v11",
    })
    path = output_path.with_suffix(".json")
    path.write_text(json.dumps(sidecar, indent=2) + "\n")
    return path


def save_gif(path: Path, frames: list[Image.Image], fps: float) -> None:
    scale = 3
    rendered = []
    for frame in frames:
        checker = Image.new("RGBA", (frame.width * scale, frame.height * scale), (42, 46, 54, 255))
        draw = ImageDraw.Draw(checker)
        tile = 16
        for y in range(0, checker.height, tile):
            for x in range(0, checker.width, tile):
                if (x // tile + y // tile) % 2:
                    draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(50, 55, 64, 255))
        checker.alpha_composite(frame.resize((frame.width * scale, frame.height * scale), Image.Resampling.NEAREST))
        rendered.append(checker.convert("P", palette=Image.Palette.ADAPTIVE))
    rendered[0].save(path, save_all=True, append_images=rendered[1:], duration=round(1000 / fps), loop=0, disposal=2)


def save_comparison_gif(path: Path, old_frames: list[Image.Image], new_frames: list[Image.Image], fps: float) -> None:
    scale = 2
    rendered = []
    for old, new in zip(old_frames, new_frames):
        logical_h = max(old.height, new.height)
        width = (old.width + new.width + 20) * scale
        height = logical_h * scale
        stage = Image.new("RGBA", (width, height), (42, 46, 54, 255))
        draw = ImageDraw.Draw(stage)
        tile = 16
        for y in range(0, stage.height, tile):
            for x in range(0, stage.width, tile):
                if (x // tile + y // tile) % 2:
                    draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(50, 55, 64, 255))
        stage.alpha_composite(old.resize((old.width * scale, old.height * scale), Image.Resampling.NEAREST), (0, height - old.height * scale))
        new_x = (old.width + 20) * scale
        stage.alpha_composite(new.resize((new.width * scale, new.height * scale), Image.Resampling.NEAREST), (new_x, height - new.height * scale))
        draw.line((old.width * scale + 10 * scale, 0, old.width * scale + 10 * scale, height), fill=(209, 138, 70, 255), width=2)
        rendered.append(stage.convert("P", palette=Image.Palette.ADAPTIVE))
    rendered[0].save(path, save_all=True, append_images=rendered[1:], duration=round(1000 / fps), loop=0, disposal=2)


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def overview(all_frames: dict[str, list[Image.Image]]) -> Image.Image:
    row_h = 290
    out = Image.new("RGBA", (1500, 120 + row_h * len(CLIPS)), (18, 22, 31, 255))
    draw = ImageDraw.Draw(out)
    draw.text((36, 28), "V11 artist-smock family — complete reversible draft set", font=font(38, True), fill="#f8f9fb")
    draw.text((36, 78), "Seven authored clips; V10 coat system; production assets unchanged", font=font(22), fill="#bac6d8")
    for row, clip in enumerate(CLIPS):
        y = 115 + row * row_h
        draw.text((36, y + 8), clip.name, font=font(23, True), fill="#ffffff")
        frames = all_frames[clip.name]
        available = 1420
        scale = min(1.75, available / (sum(f.width for f in frames)))
        x = 36
        for frame in frames:
            shown = frame.resize((round(frame.width * scale), round(frame.height * scale)), Image.Resampling.NEAREST)
            out.alpha_composite(shown, (x, y + 48))
            x += shown.width
    return out


def seam_proof(turn_frame: Image.Image, sit_frame: Image.Image) -> Image.Image:
    out = Image.new("RGBA", (1160, 610), (18, 22, 31, 255))
    draw = ImageDraw.Draw(out)
    draw.text((36, 28), "Front transition seam — exact whole-frame identity", font=font(34, True), fill="#f8f9fb")
    draw.text((36, 76), "Sit-front frame 1 is authoritative; turn-front frame 6 reuses the complete raster", font=font(21), fill="#bac6d8")
    labels = ["turn-front · frame 6", "sit-front · frame 1"]
    for index, (label, frame) in enumerate(zip(labels, [turn_frame, sit_frame])):
        x = 70 + index * 460
        draw.text((x, 125), label, font=font(23, True), fill="#ffffff")
        shown = frame.resize((frame.width * 3, frame.height * 3), Image.Resampling.NEAREST)
        out.alpha_composite(shown, (x, 170))
    equal = frame_hash(turn_frame) == frame_hash(sit_frame)
    draw.text((70, 560), f"Differing RGBA pixels: {0 if equal else 'non-zero'}", font=font(24, True), fill="#78d69a" if equal else "#ff7d7d")
    return out


def main() -> None:
    DRAFTS.mkdir(exist_ok=True)
    EVIDENCE.mkdir(exist_ok=True)
    all_frames: dict[str, list[Image.Image]] = {}
    records = {}
    for clip in CLIPS:
        frames, record = normalize_clip(clip)
        repeat_frames, repeat_record = normalize_clip(clip)
        record["deterministicNormalizationRerun"] = (
            [frame_hash(frame) for frame in frames] == [frame_hash(frame) for frame in repeat_frames]
            and record == repeat_record
        )
        all_frames[clip.name] = frames
        records[clip.name] = record

    # Whole-frame seam authorities. These are complete-frame reuse, never head
    # or costume transplants.
    side_neutral = all_frames["keeper_artist_smock_walk"][2].copy()
    all_frames["keeper_artist_smock_turn_back"][0] = side_neutral.copy()
    all_frames["keeper_artist_smock_turn_front"][0] = side_neutral.copy()
    front_authority = all_frames["keeper_artist_smock_sit_front"][0].copy()
    all_frames["keeper_artist_smock_turn_front"][-1] = front_authority.copy()

    outputs = {}
    for clip in CLIPS:
        frames = all_frames[clip.name]
        output = DRAFTS / f"{clip.name}_f{clip.frames}.png"
        output.write_bytes(png_bytes(strip(frames)))
        sidecar = save_sidecar(clip, output)
        gif = EVIDENCE / f"{clip.name}-preview.gif"
        save_gif(gif, frames, clip.fps)
        comparison_gif = EVIDENCE / f"{clip.name}-comparison.gif"
        save_comparison_gif(comparison_gif, split_reference(clip), frames, clip.fps)
        alpha = np.asarray(strip(frames).getchannel("A"))
        outputs[clip.name] = {
            **records[clip.name],
            "draft": str(output.relative_to(ROOT)),
            "draftSha256": sha256(output),
            "sidecar": str(sidecar.relative_to(ROOT)),
            "sidecarSha256": sha256(sidecar),
            "preview": str(gif.relative_to(ROOT)),
            "previewSha256": sha256(gif),
            "comparisonPreview": str(comparison_gif.relative_to(ROOT)),
            "comparisonPreviewSha256": sha256(comparison_gif),
            "binaryAlpha": bool(np.isin(alpha, [0, 255]).all()),
            "opaqueBorderPixelCount": sum(
                int(np.count_nonzero(np.asarray(frame.getchannel("A"))[[0, -1], :])) +
                int(np.count_nonzero(np.asarray(frame.getchannel("A"))[:, [0, -1]]))
                for frame in frames
            ),
            "frameHashes": [frame_hash(frame) for frame in frames],
            "generation": {
                "method": "built-in image generator; referenced-image identity-preserve mode",
                "prompt": {
                    "path": str((HERE / "prompts" / f"{clip.name}.txt").relative_to(ROOT)),
                    "sha256": sha256(HERE / "prompts" / f"{clip.name}.txt"),
                },
                "inputs": [
                    {"path": str(resolve_generation_input(value).relative_to(ROOT)), "sha256": sha256(resolve_generation_input(value))}
                    for value in clip.generation_inputs
                ],
            },
        }

    # Derived manifest family: five neutrals and three walk bridges.
    neutrals = {
        "keeper_artist-smock_neutral_standing-side-right": side_neutral,
        "keeper_artist-smock_neutral_standing-side-left": side_neutral.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
        "keeper_artist-smock_neutral_standing-front": front_authority,
        "keeper_artist-smock_neutral_standing-back": all_frames["keeper_artist_smock_turn_back"][-1],
        "keeper_artist-smock_neutral_sitting-front": all_frames["keeper_artist_smock_sit_front"][-1],
    }
    derived = {}
    for name, frame in neutrals.items():
        path = DRAFTS / f"{name}_f1.png"
        path.write_bytes(png_bytes(frame))
        sidecar = save_derived_sidecar(name, path, 1)
        derived[name] = {
            "path": str(path.relative_to(ROOT)), "sha256": sha256(path),
            "sidecar": str(sidecar.relative_to(ROOT)), "sidecarSha256": sha256(sidecar),
            "frameHash": frame_hash(frame),
        }
    walk = all_frames["keeper_artist_smock_walk"]
    for name, indices in {
        "keeper_artist_smock_walk_start": [None, 3, 4, 5, None],
        "keeper_artist_smock_walk_stop": [None, 7, 0, 1, None],
        "keeper_artist_smock_walk_cycle": [None, 3, 4, 5, 6, 7, 0, 1, None],
    }.items():
        frames = [side_neutral.copy() if index is None else walk[index].copy() for index in indices]
        path = DRAFTS / f"{name}_f{len(frames)}.png"
        path.write_bytes(png_bytes(strip(frames)))
        sidecar = save_derived_sidecar(name, path, len(frames))
        derived[name] = {
            "path": str(path.relative_to(ROOT)), "sha256": sha256(path),
            "sidecar": str(sidecar.relative_to(ROOT)), "sidecarSha256": sha256(sidecar),
            "frameHashes": [frame_hash(frame) for frame in frames],
        }

    overview_path = EVIDENCE / "artist-smock-family-overview.png"
    overview_path.write_bytes(png_bytes(overview(all_frames)))
    seam_path = EVIDENCE / "front-transition-seam-proof.png"
    seam_path.write_bytes(png_bytes(seam_proof(
        all_frames["keeper_artist_smock_turn_front"][-1],
        all_frames["keeper_artist_smock_sit_front"][0],
    )))
    validation = {
        "status": "complete-artist-smock-family-draft-awaiting-frank-review",
        "acceptedCostumeAuthority": {
            "path": "art/drafts/keeper-canon-model-pack-artist-smock-2026-10-11-v10/generated/artist-smock-fresh-source.png",
            "sha256": sha256(ROOT / "art/drafts/keeper-canon-model-pack-artist-smock-2026-10-11-v10/generated/artist-smock-fresh-source.png"),
        },
        "authoredClips": outputs,
        "derivedAssets": derived,
        "seams": {
            "turnFrontLastEqualsSitFrontFirst": frame_hash(all_frames["keeper_artist_smock_turn_front"][-1]) == frame_hash(all_frames["keeper_artist_smock_sit_front"][0]),
            "preferredAuthority": "keeper_artist_smock_sit_front frame 1",
            "turnBackFirstEqualsWalkNeutral": frame_hash(all_frames["keeper_artist_smock_turn_back"][0]) == frame_hash(side_neutral),
            "turnFrontFirstEqualsWalkNeutral": frame_hash(all_frames["keeper_artist_smock_turn_front"][0]) == frame_hash(side_neutral),
        },
        "overview": {"path": str(overview_path.relative_to(ROOT)), "sha256": sha256(overview_path)},
        "frontSeamProof": {"path": str(seam_path.relative_to(ROOT)), "sha256": sha256(seam_path)},
        "scopeGate": {
            "authoredAnimations": 7,
            "manifestFamilyEntriesCovered": 15,
            "productionFilesChanged": False,
            "registered": False,
            "promoted": False,
            "committed": False,
            "pushed": False,
        },
    }
    (EVIDENCE / "validation.json").write_text(json.dumps(validation, indent=2) + "\n")


if __name__ == "__main__":
    main()
