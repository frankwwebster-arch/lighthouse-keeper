#!/usr/bin/env python3
"""Build the reversible frame-6 rear-drumming hand-plane correction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
NAME = "keeper_play_drums_back"
PRIOR = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/drafts" / NAME
CANONICAL = ROOT / "art/raw/keeper-first-batch"
RUNTIME = ROOT / "public/sprites"
SOURCE = BATCH / "frame-6-corrected-generated.png"
OUT = BATCH / "drafts" / NAME
EVIDENCE = BATCH / "evidence" / NAME
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
    pose = crop.resize(
        (max(1, round(crop.width * scale)), target_height),
        Image.Resampling.LANCZOS,
    )
    pose.putalpha(pose.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0))
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    x = round((target_size[0] - pose.width) / 2)
    y = target_size[1] - EDGE_GUTTER - pose.height
    canvas.alpha_composite(pose, (x, y))
    final_box = canvas.getchannel("A").getbbox()
    if final_box is None or final_box[0] < EDGE_GUTTER or final_box[1] < EDGE_GUTTER or final_box[2] > target_size[0] - EDGE_GUTTER or final_box[3] > target_size[1] - EDGE_GUTTER:
        raise ValueError(f"Corrected pose lost its safety gutter: {final_box}")
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
    prior_box = prior_frames[5].getchannel("A").getbbox()
    target_height = prior_box[3] - prior_box[1]
    corrected = normalize_source(Image.open(SOURCE).convert("RGBA"), target_size, target_height)
    frames[5] = corrected

    for index in [0, 1, 2, 3, 4, 6, 7]:
        if frames[index].tobytes() != prior_frames[index].tobytes():
            raise ValueError(f"Unrelated frame {index + 1} changed")
    if frames[5].tobytes() == prior_frames[5].tobytes():
        raise ValueError("Corrected frame 6 is byte-identical to v1")

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
            "changedFromV1": index == 5,
        })

    strip_path = OUT / f"{NAME}_f8.png"
    sidecar_path = OUT / f"{NAME}_f8.json"
    contact_path = EVIDENCE / "frames.png"
    gif_path = EVIDENCE / "preview.gif"
    strip.save(strip_path)
    sidecar["draftId"] = "keeper-play-drums-back-hands-2026-10-12-v2"
    sidecar["canonicalUnchanged"] = True
    sidecar["amendment"] = {
        "date": "2026-10-12",
        "frames": [6],
        "reason": "Hands and crossed drumsticks were incorrectly posed behind the Keeper's back.",
        "invariant": "Frames 1-5 and 7-8 are byte-identical to the 11 October draft; frame 6 keeps the hands in the playable front/side plane.",
    }
    sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")
    contact_sheet(frames, contact_path)
    gif_preview(frames, float(sidecar["fps"]), gif_path)
    corrected.save(BATCH / "frame-6-normalized.png")

    canonical_strip = CANONICAL / f"{NAME}_f8.png"
    canonical_sidecar = CANONICAL / f"{NAME}_f8.json"
    canonical_runtime = RUNTIME / f"{NAME}.png"
    register = {
        "draftId": "keeper-play-drums-back-hands-2026-10-12-v2",
        "handoffId": "direct-review-2026-10-12-play-drums-back-hands",
        "animation": NAME,
        "status": "active-review-draft",
        "label": "12 Oct forward-hand-plane correction v2",
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
            "source": rel(SOURCE), "sourceSha256": sha256(SOURCE),
            "strip": rel(strip_path), "stripSha256": sha256(strip_path),
            "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path),
            "frameEvidence": frame_evidence,
            "evidence": [rel(contact_path), rel(gif_path)],
            "normalization": "Corrected full pose is alpha-cropped, height-matched to v1 frame 6, bottom-centred, binary-alpha normalized and confined to the original canvas with a two-pixel gutter.",
            "seam": "frame 6 is a low side-plane recovery between frame 5's low stick and frame 7's raised stroke; the hands never cross the back",
        },
        "qualification": "Only frame 6 changes. Both hands are connected to side-plane sleeves and direct the sticks forward toward the unseen drum kit; no hand or stick crosses the back.",
        "rollback": "Remove this exact draft directory and registry entry; canonical and the complete 11 October draft remain unchanged.",
    }
    register_path = OUT / "draft-register.json"
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    (BATCH / "build-manifest.json").write_text(json.dumps({
        "animation": NAME,
        "priorStripSha256": sha256(prior_strip_path),
        "draftStripSha256": sha256(strip_path),
        "changedFrameNumbers": [6],
        "unchangedFrameNumbers": [1, 2, 3, 4, 5, 7, 8],
        "frameEvidence": frame_evidence,
    }, indent=2) + "\n")
    print(f"Built {NAME} v2 with frame 6 hands moved out of the back plane")


if __name__ == "__main__":
    main()
