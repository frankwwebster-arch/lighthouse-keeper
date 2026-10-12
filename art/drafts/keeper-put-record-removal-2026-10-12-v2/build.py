#!/usr/bin/env python3
"""Build the reversible masked record removal for frames 5-8."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
NAME = "keeper_put_record"
PRIOR = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/drafts" / NAME
ORIGINAL_SOURCE = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/generated/outfit-walks/keeper_put_record-v1-neutral.png"
MASK_INTERPRETATION = BATCH / "mask-removal-generated.png"
CANONICAL = ROOT / "art/raw/keeper-first-batch"
RUNTIME = ROOT / "public/sprites"
OUT = BATCH / "drafts" / NAME
EVIDENCE = BATCH / "evidence" / NAME
SOURCE_ALPHA_THRESHOLD = 32
FINAL_ALPHA_THRESHOLD = 128
EDGE_GUTTER = 2
FIXED_SOURCE_SCALE = 0.6190476190476191
EXPECTED_REMOVAL_BOXES = {
    4: (195, 383, 260, 441),
    5: (189, 383, 257, 441),
    6: (209, 383, 271, 441),
    7: (173, 383, 241, 441),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def equal_cells(image: Image.Image, count: int) -> list[Image.Image]:
    return [
        image.crop((round(image.width * index / count), 0, round(image.width * (index + 1) / count), image.height))
        for index in range(count)
    ]


def connected_components(mask: Image.Image) -> list[list[tuple[int, int]]]:
    pixels = mask.load()
    seen: set[tuple[int, int]] = set()
    result = []
    for y in range(mask.height):
        for x in range(mask.width):
            if pixels[x, y] == 0 or (x, y) in seen:
                continue
            stack = [(x, y)]
            seen.add((x, y))
            component = []
            while stack:
                px, py = stack.pop()
                component.append((px, py))
                for point in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    nx, ny = point
                    if 0 <= nx < mask.width and 0 <= ny < mask.height and point not in seen and pixels[nx, ny] != 0:
                        seen.add(point)
                        stack.append(point)
            result.append(component)
    return result


def component_box(component: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    xs = [point[0] for point in component]
    ys = [point[1] for point in component]
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def selected_removal(cell: Image.Image, interpreted: Image.Image, frame_index: int) -> list[tuple[int, int]]:
    mask = Image.new("L", cell.size, 0)
    pixels = mask.load()
    original_alpha = cell.getchannel("A")
    interpreted_alpha = interpreted.getchannel("A")
    for y in range(cell.height):
        for x in range(cell.width):
            if original_alpha.getpixel((x, y)) >= SOURCE_ALPHA_THRESHOLD and interpreted_alpha.getpixel((x, y)) < SOURCE_ALPHA_THRESHOLD:
                pixels[x, y] = 255
    candidates = [
        component for component in connected_components(mask)
        if component_box(component)[0] >= round(cell.width * 0.6) and component_box(component)[1] >= 360
    ]
    if not candidates:
        raise ValueError(f"Frame {frame_index + 1} has no masked record component")
    selected = max(candidates, key=len)
    box = component_box(selected)
    if box != EXPECTED_REMOVAL_BOXES[frame_index]:
        raise ValueError(f"Frame {frame_index + 1} removal box changed: {box}")
    return selected


def cleaned_crop_and_box(cell: Image.Image) -> tuple[Image.Image, tuple[int, int, int, int]]:
    threshold = cell.getchannel("A").point(lambda value: 255 if value >= SOURCE_ALPHA_THRESHOLD else 0)
    initial_box = threshold.getbbox()
    if initial_box is None:
        raise ValueError("Source cell contains no foreground")
    crop = cell.crop(initial_box)
    alpha = crop.getchannel("A")
    components = connected_components(alpha.point(lambda value: 255 if value >= SOURCE_ALPHA_THRESHOLD else 0))
    cutoff = max(12, round(max(map(len, components)) * 0.02))
    cleaned = crop.copy()
    clean_alpha = cleaned.getchannel("A")
    clean_pixels = clean_alpha.load()
    for component in components:
        if len(component) < cutoff:
            for x, y in component:
                clean_pixels[x, y] = 0
    cleaned.putalpha(clean_alpha)
    local_box = cleaned.getchannel("A").getbbox()
    if local_box is None:
        raise ValueError("Detached-fragment cleanup removed all foreground")
    final_box = (
        initial_box[0] + local_box[0],
        initial_box[1] + local_box[1],
        initial_box[0] + local_box[2],
        initial_box[1] + local_box[3],
    )
    return cleaned.crop(local_box), final_box


def normalize_crop(crop: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    pose = crop.resize(
        (max(1, round(crop.width * FIXED_SOURCE_SCALE)), max(1, round(crop.height * FIXED_SOURCE_SCALE))),
        Image.Resampling.LANCZOS,
    )
    pose.putalpha(pose.getchannel("A").point(lambda value: 255 if value >= FINAL_ALPHA_THRESHOLD else 0))
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    x = round((target_size[0] - pose.width) / 2)
    y = target_size[1] - EDGE_GUTTER - pose.height
    canvas.alpha_composite(pose, (x, y))
    return canvas


def contact_sheet(frames: list[Image.Image], destination: Path) -> None:
    scale = 4
    tile_w = frames[0].width * scale + 16
    tile_h = frames[0].height * scale + 32
    sheet = Image.new("RGB", (4 * tile_w, 2 * tile_h), "#ece9e3")
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        x0 = (index % 4) * tile_w
        y0 = (index // 4) * tile_h
        checker = Image.new("RGB", (frames[0].width * scale, frames[0].height * scale), "#f4f1eb")
        checker_draw = ImageDraw.Draw(checker)
        for y in range(0, checker.height, 16):
            for x in range(0, checker.width, 16):
                if (x // 16 + y // 16) % 2:
                    checker_draw.rectangle((x, y, x + 15, y + 15), fill="#dedbd5")
        enlarged = frame.resize(checker.size, Image.Resampling.NEAREST)
        checker.paste(enlarged, (0, 0), enlarged)
        sheet.paste(checker, (x0 + 8, y0 + 24))
        draw.text((x0 + 8, y0 + 6), f"FRAME {index + 1}", fill="#17233b")
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination)


def gif_preview(frames: list[Image.Image], fps: float, destination: Path) -> None:
    preview = []
    for frame in frames:
        stage = Image.new("RGBA", frame.size, (236, 233, 227, 255))
        stage.alpha_composite(frame)
        preview.append(stage.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    preview[0].save(destination, save_all=True, append_images=preview[1:], duration=round(1000 / fps), loop=0, disposal=2, optimize=False)


def main() -> None:
    prior_strip_path = PRIOR / f"{NAME}_f8.png"
    prior_sidecar_path = PRIOR / f"{NAME}_f8.json"
    prior_register_path = PRIOR / "draft-register.json"
    prior_strip = Image.open(prior_strip_path).convert("RGBA")
    sidecar = json.loads(prior_sidecar_path.read_text())
    frame_width = sidecar["w"] * sidecar["density"]
    frame_height = sidecar["h"] * sidecar["density"]
    target_size = (frame_width, frame_height)
    prior_frames = [prior_strip.crop((index * frame_width, 0, (index + 1) * frame_width, frame_height)) for index in range(8)]
    original = Image.open(ORIGINAL_SOURCE).convert("RGBA")
    interpreted = Image.open(MASK_INTERPRETATION).convert("RGBA")
    if original.size != interpreted.size:
        raise ValueError("Mask interpretation geometry does not match the original source")
    original_cells = equal_cells(original, 8)
    interpreted_cells = equal_cells(interpreted, 8)
    cleaned_source = original.copy()
    frames = [frame.copy() for frame in prior_frames]
    removal_evidence = []

    for index in range(4, 8):
        selected = selected_removal(original_cells[index], interpreted_cells[index], index)
        left = round(original.width * index / 8)
        cleaned_cell = original_cells[index].copy()
        for x, y in selected:
            cleaned_cell.putpixel((x, y), (0, 0, 0, 0))
            cleaned_source.putpixel((left + x, y), (0, 0, 0, 0))
        original_crop, crop_box = cleaned_crop_and_box(original_cells[index])
        cleaned_crop = cleaned_cell.crop(crop_box)
        normalized_original = normalize_crop(original_crop, target_size)
        if normalized_original.tobytes() != prior_frames[index].tobytes():
            raise ValueError(f"Frame {index + 1} normalization no longer reconstructs v1 exactly")
        normalized_cleaned = normalize_crop(cleaned_crop, target_size)
        result = prior_frames[index].copy()
        result_pixels = result.load()
        clean_alpha = normalized_cleaned.getchannel("A")
        prior_alpha = prior_frames[index].getchannel("A")
        removed = Image.new("L", target_size, 0)
        removed_pixels = removed.load()
        for y in range(frame_height):
            for x in range(frame_width):
                if prior_alpha.getpixel((x, y)) > 0 and clean_alpha.getpixel((x, y)) == 0:
                    result_pixels[x, y] = (0, 0, 0, 0)
                    removed_pixels[x, y] = 255
        removed_box = removed.getbbox()
        if removed_box is None:
            raise ValueError(f"Frame {index + 1} lost no marked pixels")
        frames[index] = result
        removal_evidence.append({
            "frame": index + 1,
            "sourceMaskBox": list(component_box(selected)),
            "sourceMaskPixelCount": len(selected),
            "normalizedRemovedBox": list(removed_box),
            "normalizedRemovedPixelCount": removed.histogram()[255],
        })

    for index in range(4):
        if frames[index].tobytes() != prior_frames[index].tobytes():
            raise ValueError(f"Unmarked frame {index + 1} changed")

    OUT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    strip = Image.new("RGBA", prior_strip.size, (0, 0, 0, 0))
    frame_evidence = []
    for index, frame in enumerate(frames):
        strip.paste(frame, (index * frame_width, 0))
        alpha = frame.getchannel("A")
        border_count = sum(alpha.getpixel((x, 0)) > 0 or alpha.getpixel((x, frame_height - 1)) > 0 for x in range(frame_width))
        border_count += sum(alpha.getpixel((0, y)) > 0 or alpha.getpixel((frame_width - 1, y)) > 0 for y in range(frame_height))
        if border_count:
            raise ValueError(f"Frame {index + 1} touches a cell boundary")
        frame_evidence.append({
            "frame": index + 1,
            "alphaBox": list(alpha.getbbox()),
            "opaqueBorderPixelCount": border_count,
            "pixelSha256": hashlib.sha256(frame.tobytes()).hexdigest(),
            "changedFromV1": index >= 4,
        })

    strip_path = OUT / f"{NAME}_f8.png"
    sidecar_path = OUT / f"{NAME}_f8.json"
    contact_path = EVIDENCE / "frames.png"
    gif_path = EVIDENCE / "preview.gif"
    cleaned_source_path = BATCH / "source-mask-cleaned.png"
    strip.save(strip_path)
    cleaned_source.save(cleaned_source_path)
    sidecar["draftId"] = "keeper-put-record-removal-2026-10-12-v2"
    sidecar["canonicalUnchanged"] = True
    sidecar["amendment"] = {
        "date": "2026-10-12",
        "frames": [5, 6, 7, 8],
        "reason": "Remove only the floating record regions marked by Frank's supplied mask.",
        "invariant": "Frames 1-4 and every unmasked pixel in frames 5-8 are byte-identical to the 11 October draft.",
    }
    sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")
    contact_sheet(frames, contact_path)
    gif_preview(frames, float(sidecar["fps"]), gif_path)

    canonical_strip = CANONICAL / f"{NAME}_f8.png"
    canonical_sidecar = CANONICAL / f"{NAME}_f8.json"
    canonical_runtime = RUNTIME / f"{NAME}.png"
    register = {
        "draftId": "keeper-put-record-removal-2026-10-12-v2",
        "handoffId": "direct-review-2026-10-12-put-record-mask-removal",
        "animation": NAME,
        "status": "active-review-draft",
        "label": "12 Oct masked record removal v2",
        "selection": "Direct annotated review correction; requires separate explicit promotion.",
        "canonical": {
            "strip": rel(canonical_strip), "stripSha256": sha256(canonical_strip),
            "runtime": rel(canonical_runtime), "runtimeSha256": sha256(canonical_runtime),
            "sidecar": rel(canonical_sidecar), "sidecarSha256": sha256(canonical_sidecar),
        },
        "previousDraft": {
            "register": rel(prior_register_path), "registerSha256": sha256(prior_register_path),
            "strip": rel(prior_strip_path), "stripSha256": sha256(prior_strip_path),
            "sidecar": rel(prior_sidecar_path), "sidecarSha256": sha256(prior_sidecar_path),
        },
        "draft": {
            "source": rel(cleaned_source_path), "sourceSha256": sha256(cleaned_source_path),
            "maskInterpretation": rel(MASK_INTERPRETATION), "maskInterpretationSha256": sha256(MASK_INTERPRETATION),
            "strip": rel(strip_path), "stripSha256": sha256(strip_path),
            "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path),
            "frameEvidence": frame_evidence,
            "removalEvidence": removal_evidence,
            "evidence": [rel(contact_path), rel(gif_path)],
            "normalization": "Generated RGB is discarded. Only the four largest source-alpha disappearances inside Frank's marked regions are mapped into the exact v1 normalization; all surviving v1 pixels are copied byte-for-byte.",
            "seam": "the single record remains in hand through frame 4 and is absent from frames 5-8 after placement",
        },
        "qualification": "Only the four marked record regions are made transparent. No Keeper pixel is regenerated or repainted in the review strip.",
        "rollback": "Remove this exact draft directory and registry entry; canonical and the complete 11 October draft remain unchanged.",
    }
    register_path = OUT / "draft-register.json"
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    (BATCH / "build-manifest.json").write_text(json.dumps({
        "animation": NAME,
        "priorStripSha256": sha256(prior_strip_path),
        "draftStripSha256": sha256(strip_path),
        "changedFrameNumbers": [5, 6, 7, 8],
        "unchangedFrameNumbers": [1, 2, 3, 4],
        "removalEvidence": removal_evidence,
        "frameEvidence": frame_evidence,
    }, indent=2) + "\n")
    print(f"Built {NAME} v2 by removing only the four marked record regions")


if __name__ == "__main__":
    main()
