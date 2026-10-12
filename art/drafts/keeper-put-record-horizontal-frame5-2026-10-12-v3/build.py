#!/usr/bin/env python3
"""Build the reversible frame-5 horizontal held-record correction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
NAME = "keeper_put_record"
V1 = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/drafts" / NAME
V2 = ROOT / "art/drafts/keeper-put-record-removal-2026-10-12-v2/drafts" / NAME
GENERATED = BATCH / "frame-5-horizontal-record-generated.png"
CANONICAL = ROOT / "art/raw/keeper-first-batch"
RUNTIME = ROOT / "public/sprites"
OUT = BATCH / "drafts" / NAME
EVIDENCE = BATCH / "evidence" / NAME
FINAL_ALPHA_THRESHOLD = 128
EDGE_GUTTER = 2
EDIT_BOX = (139, 78, 193, 118)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def frames_from_strip(strip: Image.Image, frame_width: int, frame_height: int) -> list[Image.Image]:
    return [strip.crop((index * frame_width, 0, (index + 1) * frame_width, frame_height)) for index in range(8)]


def normalize_generated(target: Image.Image) -> Image.Image:
    generated = Image.open(GENERATED).convert("RGBA")
    alpha = generated.getchannel("A")
    box = alpha.getbbox()
    if box is None:
        raise ValueError("Generated edit has no foreground")
    crop = generated.crop(box)
    target_box = target.getchannel("A").getbbox()
    if target_box is None:
        raise ValueError("Target frame has no foreground")
    target_height = target_box[3] - target_box[1]
    scale = target_height / crop.height
    resized = crop.resize(
        (max(1, round(crop.width * scale)), target_height),
        Image.Resampling.LANCZOS,
    )
    resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= FINAL_ALPHA_THRESHOLD else 0))
    canvas = Image.new("RGBA", target.size, (0, 0, 0, 0))
    # Align the generated cap/body with the edit target; only EDIT_BOX is used.
    canvas.alpha_composite(resized, (64, target_box[1]))
    return canvas


def apply_local_edit(target: Image.Image, generated: Image.Image) -> Image.Image:
    result = target.copy()
    left, top, right, bottom = EDIT_BOX
    clear = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
    result.paste(clear, (left, top))
    patch = generated.crop(EDIT_BOX)
    result.alpha_composite(patch, (left, top))
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


def transition_sheet(frames: list[Image.Image], destination: Path) -> None:
    selected = frames[3:6]
    scale = 6
    tile_w = selected[0].width * scale + 20
    tile_h = selected[0].height * scale + 36
    sheet = Image.new("RGB", (3 * tile_w, tile_h), "#ece9e3")
    draw = ImageDraw.Draw(sheet)
    for offset, frame in enumerate(selected):
        x0 = offset * tile_w
        checker = Image.new("RGB", (frame.width * scale, frame.height * scale), "#f4f1eb")
        checker_draw = ImageDraw.Draw(checker)
        for y in range(0, checker.height, 16):
            for x in range(0, checker.width, 16):
                if (x // 16 + y // 16) % 2:
                    checker_draw.rectangle((x, y, x + 15, y + 15), fill="#dedbd5")
        enlarged = frame.resize(checker.size, Image.Resampling.NEAREST)
        checker.paste(enlarged, (0, 0), enlarged)
        sheet.paste(checker, (x0 + 10, 26))
        draw.text((x0 + 10, 7), f"FRAME {offset + 4}", fill="#17233b")
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
    v2_strip_path = V2 / f"{NAME}_f8.png"
    v2_sidecar_path = V2 / f"{NAME}_f8.json"
    v2_register_path = V2 / "draft-register.json"
    v2_strip = Image.open(v2_strip_path).convert("RGBA")
    sidecar = json.loads(v2_sidecar_path.read_text())
    frame_width = sidecar["w"] * sidecar["density"]
    frame_height = sidecar["h"] * sidecar["density"]
    v2_frames = frames_from_strip(v2_strip, frame_width, frame_height)
    normalized_generated = normalize_generated(v2_frames[4])
    frames = [frame.copy() for frame in v2_frames]
    frames[4] = apply_local_edit(v2_frames[4], normalized_generated)

    for index in (0, 1, 2, 3, 5, 6, 7):
        if frames[index].tobytes() != v2_frames[index].tobytes():
            raise ValueError(f"Out-of-scope frame {index + 1} changed")
    if frames[4].tobytes() == v2_frames[4].tobytes():
        raise ValueError("Frame 5 did not change")

    OUT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    normalized_path = EVIDENCE / "frame-5-generated-normalized.png"
    normalized_generated.save(normalized_path)
    strip = Image.new("RGBA", v2_strip.size, (0, 0, 0, 0))
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
            "changedFromV2": index == 4,
        })

    strip_path = OUT / f"{NAME}_f8.png"
    sidecar_path = OUT / f"{NAME}_f8.json"
    contact_path = EVIDENCE / "frames.png"
    transition_path = EVIDENCE / "frames-4-6-transition.png"
    gif_path = EVIDENCE / "preview.gif"
    strip.save(strip_path)
    sidecar["draftId"] = "keeper-put-record-horizontal-frame5-2026-10-12-v3"
    sidecar["canonicalUnchanged"] = True
    sidecar["amendment"] = {
        "date": "2026-10-12",
        "frames": [5],
        "reason": "Keep the frame-5 record in both hands, edge-on and parallel to ground level.",
        "invariant": "Frames 1-4 and 6-8 are byte-identical to v2; only the tight frame-5 hands/record box changes.",
    }
    sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")
    contact_sheet(frames, contact_path)
    transition_sheet(frames, transition_path)
    gif_preview(frames, float(sidecar["fps"]), gif_path)

    canonical_strip = CANONICAL / f"{NAME}_f8.png"
    canonical_sidecar = CANONICAL / f"{NAME}_f8.json"
    canonical_runtime = RUNTIME / f"{NAME}.png"
    v1_strip_path = V1 / f"{NAME}_f8.png"
    register = {
        "draftId": "keeper-put-record-horizontal-frame5-2026-10-12-v3",
        "handoffId": "direct-review-2026-10-12-put-record-horizontal-frame5",
        "animation": NAME,
        "status": "active-review-draft",
        "label": "12 Oct horizontal held-record correction v3",
        "selection": "Direct annotated review correction; requires separate explicit promotion.",
        "canonical": {
            "strip": rel(canonical_strip), "stripSha256": sha256(canonical_strip),
            "runtime": rel(canonical_runtime), "runtimeSha256": sha256(canonical_runtime),
            "sidecar": rel(canonical_sidecar), "sidecarSha256": sha256(canonical_sidecar),
        },
        "previousDraft": {
            "register": rel(v2_register_path), "registerSha256": sha256(v2_register_path),
            "strip": rel(v2_strip_path), "stripSha256": sha256(v2_strip_path),
            "sidecar": rel(v2_sidecar_path), "sidecarSha256": sha256(v2_sidecar_path),
        },
        "draft": {
            "source": rel(GENERATED), "sourceSha256": sha256(GENERATED),
            "strip": rel(strip_path), "stripSha256": sha256(strip_path),
            "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path),
            "frameEvidence": frame_evidence,
            "editBox": list(EDIT_BOX),
            "evidence": [rel(contact_path), rel(transition_path), rel(gif_path), rel(normalized_path)],
            "normalization": "The built-in edit is normalized to the exact v2 frame-5 height and cap/body alignment; only the tight hands-and-record box is composited into v2.",
            "seam": "frame 4 holds the record horizontally; frame 5 keeps it horizontal in both hands while bending; frame 6 has released it after placement",
        },
        "qualification": "Only frame 5 and only its hands/record box changes from v2. Frames 1-4 and 6-8 are byte-identical to v2.",
        "rollback": "Remove this exact draft directory and registry entry; canonical, v1 and v2 remain unchanged.",
        "pinnedV1StripSha256": sha256(v1_strip_path),
    }
    register_path = OUT / "draft-register.json"
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    (BATCH / "build-manifest.json").write_text(json.dumps({
        "animation": NAME,
        "v1StripSha256": sha256(v1_strip_path),
        "v2StripSha256": sha256(v2_strip_path),
        "draftStripSha256": sha256(strip_path),
        "changedFrameNumbers": [5],
        "unchangedFrameNumbers": [1, 2, 3, 4, 6, 7, 8],
        "editBox": list(EDIT_BOX),
        "frameEvidence": frame_evidence,
    }, indent=2) + "\n")
    print(f"Built {NAME} v3 with a horizontal record held in frame 5")


if __name__ == "__main__":
    main()
