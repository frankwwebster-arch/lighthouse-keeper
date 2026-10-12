#!/usr/bin/env python3
"""Build the reversible frame-2 rear-hand correction for the party-hat transition."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
NAME = "keeper_party_hat_put_on_back"
PRIOR = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/drafts" / NAME
CANONICAL = ROOT / "art/raw/keeper-first-batch"
RUNTIME = ROOT / "public/sprites"
SOURCE = BATCH / "frame-2-corrected-generated.png"
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
    final_box = canvas.getchannel("A").getbbox()
    if final_box is None:
        raise ValueError("Corrected pose contains no foreground on its target canvas")
    if (
        final_box[0] < EDGE_GUTTER
        or final_box[1] < EDGE_GUTTER
        or final_box[2] > target_size[0] - EDGE_GUTTER
        or final_box[3] > target_size[1] - EDGE_GUTTER
    ):
        raise ValueError(f"Corrected pose lost its safety gutter: {final_box}")
    return canvas


def contact_sheet(frames: list[Image.Image], destination: Path) -> None:
    scale = 3
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
    if prior_strip.size != (frame_width * 8, frame_height):
        raise ValueError("Prior draft geometry no longer matches its sidecar")
    frames = [
        prior_strip.crop((index * frame_width, 0, (index + 1) * frame_width, frame_height))
        for index in range(8)
    ]
    prior_height = frames[1].getchannel("A").getbbox()[3] - frames[1].getchannel("A").getbbox()[1]
    frames[1] = normalize_source(Image.open(SOURCE).convert("RGBA"), (frame_width, frame_height), prior_height)

    OUT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    output_strip = Image.new("RGBA", prior_strip.size, (0, 0, 0, 0))
    frame_evidence = []
    for index, frame in enumerate(frames):
        output_strip.paste(frame, (index * frame_width, 0))
        border_count = 0
        alpha = frame.getchannel("A")
        for x in range(frame_width):
            border_count += int(alpha.getpixel((x, 0)) > 0)
            border_count += int(alpha.getpixel((x, frame_height - 1)) > 0)
        for y in range(1, frame_height - 1):
            border_count += int(alpha.getpixel((0, y)) > 0)
            border_count += int(alpha.getpixel((frame_width - 1, y)) > 0)
        frame_evidence.append({
            "frame": index + 1,
            "alphaBox": list(alpha.getbbox()),
            "opaqueBorderPixelCount": border_count,
            "pixelSha256": hashlib.sha256(frame.tobytes()).hexdigest(),
        })
        if border_count:
            raise ValueError(f"Frame {index + 1} touches a shared strip boundary")

    # The amendment must be a one-frame replacement, never a silent family redraw.
    for index in [0, 2, 3, 4, 5, 6, 7]:
        if frames[index].tobytes() != prior_strip.crop((index * frame_width, 0, (index + 1) * frame_width, frame_height)).tobytes():
            raise ValueError(f"Unrelated frame {index + 1} changed")
    if frames[1].tobytes() == prior_strip.crop((frame_width, 0, 2 * frame_width, frame_height)).tobytes():
        raise ValueError("Frame 2 correction is byte-identical to the rejected pose")

    strip_path = OUT / f"{NAME}_f8.png"
    sidecar_path = OUT / f"{NAME}_f8.json"
    contact_path = EVIDENCE / "frames.png"
    gif_path = EVIDENCE / "preview.gif"
    output_strip.save(strip_path)
    sidecar["draftId"] = "keeper-party-hat-put-on-back-hands-2026-10-12-v2"
    sidecar["canonicalUnchanged"] = True
    sidecar["amendment"] = {
        "date": "2026-10-12",
        "frame": 2,
        "reason": "Hands and hat were composited on the wrong side of the rear-facing body.",
        "invariant": "Frames 1 and 3-8 are byte-identical to the 11 October draft.",
    }
    sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")
    contact_sheet(frames, contact_path)
    gif_preview(frames, float(sidecar["fps"]), gif_path)

    canonical_strip = CANONICAL / "keeper_party_hat_put_on_back_f8.png"
    canonical_sidecar = CANONICAL / "keeper_party_hat_put_on_back_f8.json"
    canonical_runtime = RUNTIME / "keeper_party_hat_put_on_back.png"
    register = {
        "draftId": "keeper-party-hat-put-on-back-hands-2026-10-12-v2",
        "handoffId": "direct-review-2026-10-12-party-hat-frame-2",
        "animation": NAME,
        "status": "active-review-draft",
        "label": "12 Oct rear-hand correction v2",
        "selection": "Direct annotated review correction; requires separate explicit promotion.",
        "canonical": {
            "strip": rel(canonical_strip),
            "stripSha256": sha256(canonical_strip),
            "runtime": rel(canonical_runtime),
            "runtimeSha256": sha256(canonical_runtime),
            "sidecar": rel(canonical_sidecar),
            "sidecarSha256": sha256(canonical_sidecar),
        },
        "previousDraft": {
            "register": rel(prior_register_path),
            "registerSha256": sha256(prior_register_path),
            "strip": rel(prior_strip_path),
            "stripSha256": sha256(prior_strip_path),
            "sidecar": rel(prior_sidecar_path),
            "sidecarSha256": sha256(prior_sidecar_path),
        },
        "draft": {
            "source": rel(SOURCE),
            "sourceSha256": sha256(SOURCE),
            "workingSource": rel(BATCH / "frame-2-source.png"),
            "workingSourceSha256": sha256(BATCH / "frame-2-source.png"),
            "strip": rel(strip_path),
            "stripSha256": sha256(strip_path),
            "sidecar": rel(sidecar_path),
            "sidecarSha256": sha256(sidecar_path),
            "frameEvidence": frame_evidence,
            "evidence": [rel(contact_path), rel(gif_path)],
            "normalization": "Frame 2 alpha crop >=32, uniform height match to rejected frame 2, final binary alpha >=128, bottom-centred on the unchanged 128x224 review cell.",
            "seam": "rear-no-hat to connected rear-plane arm lift to overhead hat raise; frames 1 and 3-8 unchanged",
        },
        "qualification": "Only frame 2 is re-rendered. It replaces the impossible front-plane hand placement with connected rear-view arms holding the hat at the nape; every other frame is byte-identical to the prior draft.",
        "rollback": "Remove this draft directory and registry entry; canonical and the complete 11 October draft remain unchanged.",
    }
    register_path = OUT / "draft-register.json"
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    manifest = {
        "animation": NAME,
        "sourceSha256": sha256(SOURCE),
        "priorStripSha256": sha256(prior_strip_path),
        "draftStripSha256": sha256(strip_path),
        "unchangedFrameNumbers": [1, 3, 4, 5, 6, 7, 8],
        "frameEvidence": frame_evidence,
    }
    (BATCH / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {NAME} v2 with only frame 2 replaced")


if __name__ == "__main__":
    main()
