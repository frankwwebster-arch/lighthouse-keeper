#!/usr/bin/env python3
"""Build the reversible frame-1/frame-7 right-hand shopping-bag correction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
NAME = "keeper_carry_shopping"
PRIOR = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/drafts" / NAME
CANONICAL = ROOT / "art/raw/keeper-first-batch"
RUNTIME = ROOT / "public/sprites"
OUT = BATCH / "drafts" / NAME
EVIDENCE = BATCH / "evidence" / NAME
CORRECTED_SOURCES = {
    0: BATCH / "frame-1-corrected-generated.png",
    6: BATCH / "frame-7-corrected-generated.png",
}
ALPHA_THRESHOLD = 128
EDGE_GUTTER = 2


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalize_source(source: Image.Image, target_size: tuple[int, int], target_height: int) -> Image.Image:
    mask = source.getchannel("A").point(lambda value: 255 if value >= 32 else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("Corrected source contains no foreground")
    crop = source.crop(bbox)
    scale = target_height / crop.height
    resized = crop.resize(
        (max(1, round(crop.width * scale)), target_height),
        Image.Resampling.LANCZOS,
    )
    resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0))
    alpha_box = resized.getchannel("A").getbbox()
    if alpha_box is None:
        raise ValueError("Corrected pose contains no foreground after normalization")
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    centre_x = (alpha_box[0] + alpha_box[2]) / 2
    paste_x = round(target_size[0] / 2 - centre_x)
    paste_y = round(target_size[1] - EDGE_GUTTER - alpha_box[3])
    canvas.alpha_composite(resized, (paste_x, paste_y))
    bbox = canvas.getchannel("A").getbbox()
    if bbox is None or bbox[0] < EDGE_GUTTER or bbox[1] < EDGE_GUTTER or bbox[2] > target_size[0] - EDGE_GUTTER or bbox[3] > target_size[1] - EDGE_GUTTER:
        raise ValueError(f"Corrected pose lost its safety gutter: {bbox}")
    return canvas


def composite_right_hand_bag(prior: Image.Image, corrected: Image.Image, anchor_x: int) -> Image.Image:
    """Overlay only the forward hand/bag quadrant, preserving face/body pixels."""
    mask = corrected.getchannel("A").copy()
    pixels = mask.load()
    # The front/right grip and bag live on the viewer-right side below the
    # elbow. This guard preserves the head, face, beard, torso, rear bag and
    # both upper limbs from the reviewed v1 frame.
    for y in range(mask.height):
        for x in range(mask.width):
            if x < anchor_x - 2 or y < 72:
                pixels[x, y] = 0
    patch = corrected.copy()
    patch.putalpha(mask)
    result = prior.copy()
    result.alpha_composite(patch)
    return result


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
    preview[0].save(
        destination,
        save_all=True,
        append_images=preview[1:],
        duration=round(1000 / fps),
        loop=0,
        disposal=2,
        optimize=False,
    )


def main() -> None:
    prior_strip_path = PRIOR / f"{NAME}_f8.png"
    prior_sidecar_path = PRIOR / f"{NAME}_f8.json"
    prior_register_path = PRIOR / "draft-register.json"
    prior_strip = Image.open(prior_strip_path).convert("RGBA")
    sidecar = json.loads(prior_sidecar_path.read_text())
    frame_width = sidecar["w"] * sidecar["density"]
    frame_height = sidecar["h"] * sidecar["density"]
    target_size = (frame_width, frame_height)
    if prior_strip.size != (frame_width * 8, frame_height):
        raise ValueError("Prior draft geometry no longer matches its sidecar")
    prior_frames = [
        prior_strip.crop((index * frame_width, 0, (index + 1) * frame_width, frame_height))
        for index in range(8)
    ]
    frames = [frame.copy() for frame in prior_frames]
    normalized_sources = {}
    for index, source_path in CORRECTED_SOURCES.items():
        prior_box = prior_frames[index].getchannel("A").getbbox()
        prior_height = prior_box[3] - prior_box[1]
        normalized = normalize_source(Image.open(source_path).convert("RGBA"), target_size, prior_height)
        normalized_sources[index] = normalized
        frames[index] = composite_right_hand_bag(prior_frames[index], normalized, sidecar["anchor"][0] * sidecar["density"])

    # The v1 family builder deliberately made frame 8 a byte-identical copy of
    # frame 1 for a seamless loop. Carry the corrected frame-1 endpoint across
    # rather than allowing the restored bag to vanish on the final beat.
    frames[7] = frames[0].copy()

    for index in [1, 2, 3, 4, 5]:
        if frames[index].tobytes() != prior_frames[index].tobytes():
            raise ValueError(f"Unrelated frame {index + 1} changed")
    for index in [0, 6, 7]:
        if frames[index].tobytes() == prior_frames[index].tobytes():
            raise ValueError(f"Corrected frame {index + 1} is byte-identical to v1")
    if frames[7].tobytes() != frames[0].tobytes():
        raise ValueError("Frame 8 no longer matches frame 1 for the seamless loop")

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
        changed_bbox = None
        if index in [0, 6, 7]:
            difference = Image.new("L", target_size, 0)
            diff_pixels = difference.load()
            before = prior_frames[index].load()
            after = frame.load()
            for y in range(frame_height):
                for x in range(frame_width):
                    if before[x, y] != after[x, y]:
                        diff_pixels[x, y] = 255
            changed_bbox = list(difference.getbbox())
            if changed_bbox[0] < sidecar["anchor"][0] * sidecar["density"] - 2 or changed_bbox[1] < 72:
                raise ValueError(f"Frame {index + 1} changed outside the forward hand/bag quadrant: {changed_bbox}")
        frame_evidence.append({
            "frame": index + 1,
            "alphaBox": list(alpha.getbbox()),
            "opaqueBorderPixelCount": border_count,
            "pixelSha256": hashlib.sha256(frame.tobytes()).hexdigest(),
            "changedPixelBoxFromV1": changed_bbox,
        })

    strip_path = OUT / f"{NAME}_f8.png"
    sidecar_path = OUT / f"{NAME}_f8.json"
    contact_path = EVIDENCE / "frames.png"
    gif_path = EVIDENCE / "preview.gif"
    strip.save(strip_path)
    sidecar["draftId"] = "keeper-carry-shopping-right-bag-2026-10-12-v2"
    sidecar["canonicalUnchanged"] = True
    sidecar["amendment"] = {
        "date": "2026-10-12",
        "authoredFrames": [1, 7],
        "derivedLoopEndpointFrame": 8,
        "reason": "Right-hand shopping bag was missing in annotated frames 1 and 7 while surrounding gait frames retained it; frame 8 follows corrected frame 1 to preserve the existing exact loop endpoint.",
        "invariant": "Frames 2-6 are byte-identical to the 11 October draft; frame 8 is byte-identical to corrected frame 1; face, beard, torso and rear bag are preserved in the authored corrections.",
    }
    sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")
    contact_sheet(frames, contact_path)
    gif_preview(frames, float(sidecar["fps"]), gif_path)

    canonical_strip = CANONICAL / "keeper_carry_shopping_f8.png"
    canonical_sidecar = CANONICAL / "keeper_carry_shopping_f8.json"
    canonical_runtime = RUNTIME / "keeper_carry_shopping.png"
    register = {
        "draftId": "keeper-carry-shopping-right-bag-2026-10-12-v2",
        "handoffId": "direct-review-2026-10-12-carry-shopping-right-bag",
        "animation": NAME,
        "status": "active-review-draft",
        "label": "12 Oct right-hand bag correction v2",
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
            "source": rel(CORRECTED_SOURCES[0]),
            "sourceSha256": sha256(CORRECTED_SOURCES[0]),
            "workingSource": rel(CORRECTED_SOURCES[6]),
            "workingSourceSha256": sha256(CORRECTED_SOURCES[6]),
            "strip": rel(strip_path), "stripSha256": sha256(strip_path),
            "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path),
            "frameEvidence": frame_evidence,
            "evidence": [rel(contact_path), rel(gif_path)],
            "normalization": "Corrected full poses are alpha-cropped and height-matched; only their viewer-right lower quadrant is composited over frames 1 and 7, preserving all other v1 pixels. Corrected frame 1 is copied exactly to frame 8 as the established loop endpoint.",
            "seam": "right-hand bag remains present through the complete eight-frame gait; frames 1 and 8 are byte-identical loop endpoints; frames 2-6 are unchanged",
        },
        "qualification": "Only the forward/right hand and shopping-bag quadrant is authored in frames 1 and 7; corrected frame 1 is copied to frame 8 to retain the exact loop endpoint. The face, beard, cap, torso, rear bag, gait family and frames 2-6 remain from the reviewed v1 draft.",
        "rollback": "Remove this exact draft directory and registry entry; canonical and the complete 11 October draft remain unchanged.",
    }
    register_path = OUT / "draft-register.json"
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    (BATCH / "build-manifest.json").write_text(json.dumps({
        "animation": NAME,
        "priorStripSha256": sha256(prior_strip_path),
        "draftStripSha256": sha256(strip_path),
        "authoredFrameNumbers": [1, 7],
        "derivedLoopEndpointFrameNumber": 8,
        "changedFrameNumbers": [1, 7, 8],
        "unchangedFrameNumbers": [2, 3, 4, 5, 6],
        "frameEvidence": frame_evidence,
    }, indent=2) + "\n")
    for index, normalized in normalized_sources.items():
        normalized.save(BATCH / f"frame-{index + 1}-normalized.png")
    print(f"Built {NAME} v2 with right-hand bags restored in frames 1 and 7 and frame 8 synchronized to frame 1")


if __name__ == "__main__":
    main()
