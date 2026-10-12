#!/usr/bin/env python3
"""Normalize the six exact-name party amendments into reversible review drafts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
DRAFT_ROOT = Path(__file__).resolve().parent
RAW = ROOT / "art/raw/keeper-first-batch"
PUBLIC = ROOT / "public/sprites"
GENERATED = DRAFT_ROOT / "generated/party"
OUT = DRAFT_ROOT / "drafts"
EVIDENCE = DRAFT_ROOT / "evidence/party"
HANDOFF = ROOT / "docs/review/keeper-review-handoff-2026-10-11T221440Z.json"
SOURCE_ALPHA_THRESHOLD = 32
FINAL_ALPHA_THRESHOLD = 128
EDGE_GUTTER_PX = 2


SPECS = {
    "keeper_party_walk": {
        "source": "keeper_party_walk-v3.png",
        "source_frames": 8,
        "source_indices": list(range(8)),
        "seam": "loop",
    },
    "keeper_party_turn_back": {
        "source": "keeper_party_turn_back-v2.png",
        "source_frames": 6,
        "source_indices": list(range(6)),
        "seam": "walk-to-back",
    },
    "keeper_party_hat_put_on_back": {
        "source": "keeper_party_hat_put_on_back-v2.png",
        "source_frames": 8,
        "source_indices": list(range(8)),
        "seam": "rear-no-hat-to-rear-party",
    },
    "keeper_party_eat_cake": {
        "source": "keeper_party_eat_cake-v4.png",
        "source_frames": 8,
        "source_indices": list(range(8)),
        "seam": "loop",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def current(name: str, suffix: str) -> Path:
    matches = sorted(RAW.glob(f"{name}_f*.{suffix}"))
    if len(matches) != 1:
        raise ValueError(f"Expected one {suffix} for {name}, found {matches}")
    return matches[0]


def equal_cells(path: Path, count: int) -> list[Image.Image]:
    source = Image.open(path).convert("RGBA")
    cells = []
    for index in range(count):
        left = round(source.width * index / count)
        right = round(source.width * (index + 1) / count)
        cells.append(source.crop((left, 0, right, source.height)))
    return cells


def foreground_crop(cell: Image.Image) -> tuple[Image.Image, tuple[int, int, int, int]]:
    mask = cell.getchannel("A").point(lambda value: 255 if value >= SOURCE_ALPHA_THRESHOLD else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("Generated source cell contains no foreground")
    return cell.crop(bbox), bbox


def normalize(crop: Image.Image, size: tuple[int, int], anchor: tuple[int, int], scale: float) -> Image.Image:
    resized = crop.resize(
        (max(1, round(crop.width * scale)), max(1, round(crop.height * scale))),
        Image.Resampling.LANCZOS,
    )
    resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= FINAL_ALPHA_THRESHOLD else 0))
    alpha_box = resized.getchannel("A").getbbox()
    if alpha_box is None:
        raise ValueError("Normalized pose contains no foreground")
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    centre_x = (alpha_box[0] + alpha_box[2]) / 2
    bottom_y = alpha_box[3]
    paste_x = round(anchor[0] - centre_x)
    paste_y = round((size[1] - EDGE_GUTTER_PX) - bottom_y)
    canvas.alpha_composite(resized, (paste_x, paste_y))
    final_box = canvas.getchannel("A").getbbox()
    if final_box is None:
        raise ValueError("Normalized canvas contains no foreground")
    if final_box[0] < EDGE_GUTTER_PX or final_box[1] < EDGE_GUTTER_PX or final_box[2] > size[0] - EDGE_GUTTER_PX or final_box[3] > size[1] - EDGE_GUTTER_PX:
        raise ValueError(f"Pose lost its transparent safety gutter: {final_box} in {size}")
    return canvas


def contact_sheet(frames: list[Image.Image], destination: Path) -> None:
    columns = min(4, len(frames))
    rows = (len(frames) + columns - 1) // columns
    scale = 2
    tile_w, tile_h = frames[0].width * scale + 16, frames[0].height * scale + 32
    sheet = Image.new("RGB", (columns * tile_w, rows * tile_h), "#ece9e3")
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        x0 = (index % columns) * tile_w
        y0 = (index // columns) * tile_h
        checker = Image.new("RGB", (frames[0].width * scale, frames[0].height * scale), "#f4f1eb")
        cdraw = ImageDraw.Draw(checker)
        for y in range(0, checker.height, 16):
            for x in range(0, checker.width, 16):
                if (x // 16 + y // 16) % 2:
                    cdraw.rectangle((x, y, x + 15, y + 15), fill="#dedbd5")
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
    reviews = {
        item["name"]: item
        for item in json.loads(HANDOFF.read_text())["review"]["reviews"]
    }
    walk_cells = equal_cells(GENERATED / SPECS["keeper_party_walk"]["source"], 8)
    walk_crops = [foreground_crop(cell)[0] for cell in walk_cells]
    # The image model changed pixel density between calls. Calibrate each
    # immutable source once against the same 184px upright party silhouette,
    # then keep that scale fixed for every pose extracted from that source.
    # The shared 224px-high canvas leaves room for raised hands and a lifted hat.
    source_scales = {}
    for source_name, source_frames in {
        spec["source"]: spec["source_frames"] for spec in SPECS.values()
    }.items():
        heights = sorted(
            foreground_crop(cell)[0].height
            for cell in equal_cells(GENERATED / source_name, source_frames)
        )
        source_scales[source_name] = 184 / heights[len(heights) // 2]
    manifest = {
        "family": "party",
        "fixedSourceScales": source_scales,
        "sourceAlphaThreshold": SOURCE_ALPHA_THRESHOLD,
        "finalAlphaThreshold": FINAL_ALPHA_THRESHOLD,
        "animations": {},
    }
    for name, spec in SPECS.items():
        canonical_strip = current(name, "png")
        canonical_sidecar = current(name, "json")
        canonical_runtime = PUBLIC / f"{name}.png"
        sidecar = json.loads(canonical_sidecar.read_text())
        review = reviews[name]
        source_path = GENERATED / spec["source"]
        source_cells = equal_cells(source_path, spec["source_frames"])
        source_crops = [foreground_crop(cell) for cell in source_cells]
        sidecar["h"] = 56
        sidecar["anchor"][1] = 56
        target_size = (sidecar["w"] * sidecar["density"], sidecar["h"] * sidecar["density"])
        anchor_px = (sidecar["anchor"][0] * sidecar["density"], sidecar["anchor"][1] * sidecar["density"])
        source_scale = source_scales[spec["source"]]
        frames = [normalize(source_crops[index][0], target_size, anchor_px, source_scale) for index in spec["source_indices"]]

        if name == "keeper_party_turn_back":
            walk_neutral = normalize(walk_crops[2], target_size, anchor_px, source_scales[SPECS["keeper_party_walk"]["source"]])
            frames[0] = walk_neutral
        if name == "keeper_party_hat_put_on_back":
            turn_sidecar = json.loads(current("keeper_party_turn_back", "json").read_text())
            turn_sidecar["h"] = 56
            turn_sidecar["anchor"][1] = 56
            turn_size = (turn_sidecar["w"] * turn_sidecar["density"], turn_sidecar["h"] * turn_sidecar["density"])
            turn_anchor = (turn_sidecar["anchor"][0] * turn_sidecar["density"], turn_sidecar["anchor"][1] * turn_sidecar["density"])
            turn_last = normalize(foreground_crop(equal_cells(GENERATED / SPECS["keeper_party_turn_back"]["source"], 6)[5])[0], turn_size, turn_anchor, source_scales[SPECS["keeper_party_turn_back"]["source"]])
            if turn_last.size != target_size:
                raise ValueError("Party rear seam canvases differ")
            frames[-2] = turn_last.copy()
            frames[-1] = turn_last.copy()
        if name in {"keeper_party_dance", "keeper_party_eat_cake"}:
            frames[-1] = frames[0].copy()

        draft_dir = OUT / name
        evidence_dir = EVIDENCE / name
        draft_dir.mkdir(parents=True, exist_ok=True)
        evidence_dir.mkdir(parents=True, exist_ok=True)
        strip = Image.new("RGBA", (target_size[0] * len(frames), target_size[1]), (0, 0, 0, 0))
        frame_evidence = []
        for index, frame in enumerate(frames):
            strip.alpha_composite(frame, (index * target_size[0], 0))
            frame_evidence.append({
                "frame": index + 1,
                "alphaBox": list(frame.getchannel("A").getbbox()),
                "opaqueBorderPixelCount": 0,
            })
        strip_path = draft_dir / f"{name}_f{len(frames)}.png"
        sidecar_path = draft_dir / f"{name}_f{len(frames)}.json"
        strip.save(strip_path)
        sidecar["frames"] = len(frames)
        sidecar["fps"] = review["animationFps"]
        sidecar["reviewScale"] = [review["widthPercent"], review["heightPercent"]]
        sidecar["reviewOffset"] = [review["actionOffsetX"], review["actionOffsetY"]]
        sidecar["reviewScaleRounds"] = {**sidecar.get("reviewScaleRounds", {}), "2026-10-11": sidecar["reviewScale"]}
        sidecar["reviewOffsetRounds"] = {**sidecar.get("reviewOffsetRounds", {}), "2026-10-11": sidecar["reviewOffset"]}
        sidecar["draftId"] = "keeper-review-amendments-2026-10-11-v1"
        sidecar["canonicalUnchanged"] = True
        sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")
        contact_path = evidence_dir / "frames.png"
        gif_path = evidence_dir / "preview.gif"
        contact_sheet(frames, contact_path)
        gif_preview(frames, float(sidecar["fps"]), gif_path)
        register = {
            "draftId": f"keeper-review-amendments-2026-10-11-v1-{name}",
            "handoffId": "d9081e53-2808-4b1f-8422-2df09cf38c3c",
            "animation": name,
            "status": "active-review-draft",
            "label": "11 Oct amendment draft v1",
            "selection": "Generated only for Frank's exact-name 11 October amendment handoff; requires separate explicit promotion.",
            "canonical": {
                "strip": rel(canonical_strip), "stripSha256": sha256(canonical_strip),
                "runtime": rel(canonical_runtime), "runtimeSha256": sha256(canonical_runtime),
                "sidecar": rel(canonical_sidecar), "sidecarSha256": sha256(canonical_sidecar),
            },
            "draft": {
                "source": rel(source_path), "sourceSha256": sha256(source_path),
                "strip": rel(strip_path), "stripSha256": sha256(strip_path),
                "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path),
                "frameEvidence": frame_evidence,
                "evidence": [rel(contact_path), rel(gif_path)],
                "fixedSourceScale": source_scale,
                "normalization": "equal source cells, alpha crop >=32, one fixed scale per immutable generated source calibrated to a 184px upright party silhouette, final binary alpha >=128, anchor-aligned on a shared 56-logical-pixel canvas",
                "seam": spec["seam"],
            },
            "qualification": "Every pose is a coherent full-character render. No head, beard, hat, or body part was transplanted from another frame.",
            "rollback": "Discard this exact-name draft directory and registry entry; canonical and earlier draft assets are unchanged.",
        }
        register_path = draft_dir / "draft-register.json"
        register_path.write_text(json.dumps(register, indent=2) + "\n")
        manifest["animations"][name] = {
            "register": rel(register_path),
            "sourceCellBboxes": [list(bbox) for _, bbox in source_crops],
            "draftStripSha256": sha256(strip_path),
            "canonicalStripSha256": sha256(canonical_strip),
        }

    # The final hat-put-on frames must be byte-identical to the rear turn endpoint.
    turn = Image.open(OUT / "keeper_party_turn_back/keeper_party_turn_back_f6.png").convert("RGBA")
    hat = Image.open(OUT / "keeper_party_hat_put_on_back/keeper_party_hat_put_on_back_f8.png").convert("RGBA")
    fw = turn.width // 6
    turn_last = turn.crop((5 * fw, 0, 6 * fw, turn.height))
    hat_fw = hat.width // 8
    for index in (6, 7):
        if hat.crop((index * hat_fw, 0, (index + 1) * hat_fw, hat.height)).tobytes() != turn_last.tobytes():
            raise ValueError("Party rear endpoint seam is not byte-identical")
    manifest["seamAssertions"] = ["party_hat_put_on_back frames 7-8 == party_turn_back frame 6"]
    (EVIDENCE / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(SPECS)} reversible party-family drafts with calibrated immutable-source scales")


if __name__ == "__main__":
    main()
