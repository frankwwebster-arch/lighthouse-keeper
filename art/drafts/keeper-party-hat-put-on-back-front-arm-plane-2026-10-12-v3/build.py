#!/usr/bin/env python3
"""Build the reversible frame-2 front/near arm-plane correction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
NAME = "keeper_party_hat_put_on_back"
V1 = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/drafts" / NAME
V2 = ROOT / "art/drafts/keeper-party-hat-put-on-back-hands-2026-10-12-v2/drafts" / NAME
CANONICAL = ROOT / "art/raw/keeper-first-batch"
RUNTIME = ROOT / "public/sprites"
SOURCE = BATCH / "frame-2-front-arm-plane-generated.png"
OUT = BATCH / "drafts" / NAME
EVIDENCE = BATCH / "evidence" / NAME
ALPHA_THRESHOLD = 128
SOURCE_ALPHA_THRESHOLD = 32
EDGE_GUTTER = 2
TARGET_HEIGHT = 184


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def cleaned_source_crop(source: Image.Image) -> Image.Image:
    threshold = source.getchannel("A").point(lambda value: 255 if value >= SOURCE_ALPHA_THRESHOLD else 0)
    components = connected_components(threshold)
    if not components:
        raise ValueError("Generated edit contains no foreground")
    largest = max(components, key=len)
    keep = set(largest)
    cleaned = source.copy()
    alpha = cleaned.getchannel("A")
    pixels = alpha.load()
    for y in range(alpha.height):
        for x in range(alpha.width):
            if (x, y) not in keep:
                pixels[x, y] = 0
    cleaned.putalpha(alpha)
    box = cleaned.getchannel("A").getbbox()
    if box is None:
        raise ValueError("Foreground cleanup removed the pose")
    return cleaned.crop(box)


def normalize_source(source: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    crop = cleaned_source_crop(source)
    scale = TARGET_HEIGHT / crop.height
    resized = crop.resize((max(1, round(crop.width * scale)), TARGET_HEIGHT), Image.Resampling.LANCZOS)
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
        raise ValueError("Corrected pose contains no foreground on target canvas")
    if final_box[0] < EDGE_GUTTER or final_box[1] < EDGE_GUTTER or final_box[2] > target_size[0] - EDGE_GUTTER or final_box[3] > target_size[1] - EDGE_GUTTER:
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


def transition_sheet(frames: list[Image.Image], destination: Path) -> None:
    scale = 5
    tile_w = frames[0].width * scale + 20
    tile_h = frames[0].height * scale + 36
    sheet = Image.new("RGB", (3 * tile_w, tile_h), "#ece9e3")
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames[:3]):
        x0 = index * tile_w
        checker = Image.new("RGB", (frame.width * scale, frame.height * scale), "#f4f1eb")
        checker_draw = ImageDraw.Draw(checker)
        for y in range(0, checker.height, 16):
            for x in range(0, checker.width, 16):
                if (x // 16 + y // 16) % 2:
                    checker_draw.rectangle((x, y, x + 15, y + 15), fill="#dedbd5")
        enlarged = frame.resize(checker.size, Image.Resampling.NEAREST)
        checker.paste(enlarged, (0, 0), enlarged)
        sheet.paste(checker, (x0 + 10, 26))
        draw.text((x0 + 10, 7), f"FRAME {index + 1}", fill="#17233b")
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
    frames = [v2_strip.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height)) for i in range(8)]
    frames[1] = normalize_source(Image.open(SOURCE).convert("RGBA"), (frame_width, frame_height))

    for index in (0, 2, 3, 4, 5, 6, 7):
        if frames[index].tobytes() != v2_strip.crop((index * frame_width, 0, (index + 1) * frame_width, frame_height)).tobytes():
            raise ValueError(f"Out-of-scope frame {index + 1} changed")

    OUT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    output_strip = Image.new("RGBA", v2_strip.size, (0, 0, 0, 0))
    frame_evidence = []
    for index, frame in enumerate(frames):
        output_strip.paste(frame, (index * frame_width, 0))
        alpha = frame.getchannel("A")
        border_count = sum(alpha.getpixel((x, 0)) > 0 or alpha.getpixel((x, frame_height - 1)) > 0 for x in range(frame_width))
        border_count += sum(alpha.getpixel((0, y)) > 0 or alpha.getpixel((frame_width - 1, y)) > 0 for y in range(frame_height))
        if border_count:
            raise ValueError(f"Frame {index + 1} touches a shared strip boundary")
        frame_evidence.append({
            "frame": index + 1,
            "alphaBox": list(alpha.getbbox()),
            "opaqueBorderPixelCount": border_count,
            "pixelSha256": hashlib.sha256(frame.tobytes()).hexdigest(),
            "changedFromV2": index == 1,
        })

    strip_path = OUT / f"{NAME}_f8.png"
    sidecar_path = OUT / f"{NAME}_f8.json"
    contact_path = EVIDENCE / "frames.png"
    transition_path = EVIDENCE / "frames-1-3-transition.png"
    gif_path = EVIDENCE / "preview.gif"
    output_strip.save(strip_path)
    sidecar["draftId"] = "keeper-party-hat-put-on-back-front-arm-plane-2026-10-12-v3"
    sidecar["canonicalUnchanged"] = True
    sidecar["amendment"] = {
        "date": "2026-10-12",
        "frame": 2,
        "reason": "Keep both forearms and hands in the front/near plane, clear of the head, while beginning the hat lift.",
        "invariant": "Frames 1 and 3-8 are byte-identical to v2.",
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
        "draftId": "keeper-party-hat-put-on-back-front-arm-plane-2026-10-12-v3",
        "handoffId": "direct-review-2026-10-12-party-hat-frame-2-front-plane",
        "animation": NAME,
        "status": "active-review-draft",
        "label": "12 Oct front-arm-plane correction v3",
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
            "source": rel(SOURCE), "sourceSha256": sha256(SOURCE),
            "strip": rel(strip_path), "stripSha256": sha256(strip_path),
            "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path),
            "frameEvidence": frame_evidence,
            "evidence": [rel(contact_path), rel(transition_path), rel(gif_path)],
            "normalization": "Largest connected source component only; uniform 184px alpha-height normalization matching frame 3's full action height; binary alpha >=128; bottom-centred with a 2px gutter on the unchanged 128x224 cell.",
            "seam": "neutral arms-down frame 1 to front/near-plane half-lift frame 2 to overhead frame 3; frames 1 and 3-8 unchanged",
        },
        "qualification": "Only frame 2 is re-rendered. Both connected arms remain outside and clear of the head silhouette while the hat begins its upward path.",
        "rollback": "Remove this exact draft directory and registry entry; canonical, v1 and v2 remain unchanged.",
        "pinnedV1StripSha256": sha256(v1_strip_path),
    }
    register_path = OUT / "draft-register.json"
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    (BATCH / "build-manifest.json").write_text(json.dumps({
        "animation": NAME,
        "sourceSha256": sha256(SOURCE),
        "v1StripSha256": sha256(v1_strip_path),
        "v2StripSha256": sha256(v2_strip_path),
        "draftStripSha256": sha256(strip_path),
        "changedFrameNumbers": [2],
        "unchangedFrameNumbers": [1, 3, 4, 5, 6, 7, 8],
        "frameEvidence": frame_evidence,
    }, indent=2) + "\n")
    print(f"Built {NAME} v3 with frame 2 arms clear of the head")


if __name__ == "__main__":
    main()
