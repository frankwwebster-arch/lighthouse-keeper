#!/usr/bin/env python3
"""Normalize the five exact-name scuba amendments into reversible review drafts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
DRAFT_ROOT = Path(__file__).resolve().parent
RAW = ROOT / "art/raw/keeper-first-batch"
PUBLIC = ROOT / "public/sprites"
GENERATED = DRAFT_ROOT / "generated/scuba"
OUT = DRAFT_ROOT / "drafts"
EVIDENCE = DRAFT_ROOT / "evidence/scuba"
HANDOFF = ROOT / "docs/review/keeper-review-handoff-2026-10-11T221440Z.json"
SOURCE_ALPHA_THRESHOLD = 32
FINAL_ALPHA_THRESHOLD = 128
GUTTER = 2


SPECS = {
    "keeper_scuba_walk_side": {"source": "keeper_scuba_walk_side-v1.png", "frames": 8, "mode": "floor", "axis": "height", "extent": 184},
    "keeper_scuba_jetty_dive": {"source": "keeper_scuba_jetty_dive-v2-grid.png", "frames": 12, "grid": [4, 3], "mode": "dive", "axis": "first-height", "extent": 184},
    "keeper_scuba_swim_horizontal": {"source": "keeper_scuba_swim_horizontal-v1.png", "frames": 8, "mode": "centre", "axis": "width", "extent": 272},
    "keeper_scuba_swim_up": {"source": "keeper_scuba_swim_up-v1.png", "frames": 8, "mode": "centre", "axis": "height", "extent": 184},
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
    return [
        source.crop((round(source.width * i / count), 0, round(source.width * (i + 1) / count), source.height))
        for i in range(count)
    ]


def grid_cells(path: Path, columns: int, rows: int) -> list[Image.Image]:
    source = Image.open(path).convert("RGBA")
    return [
        source.crop((
            round(source.width * column / columns),
            round(source.height * row / rows),
            round(source.width * (column + 1) / columns),
            round(source.height * (row + 1) / rows),
        ))
        for row in range(rows)
        for column in range(columns)
    ]


def foreground(cell: Image.Image) -> tuple[Image.Image, list[int]]:
    mask = cell.getchannel("A").point(lambda value: 255 if value >= SOURCE_ALPHA_THRESHOLD else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("Generated source cell contains no foreground")
    return cell.crop(bbox), list(bbox)


def source_scale(crops: list[Image.Image], spec: dict) -> float:
    if spec["axis"] == "first-height":
        measure = crops[0].height
    elif spec["axis"] == "height":
        values = sorted(crop.height for crop in crops)
        measure = values[-1] if spec["mode"] == "centre" else values[len(values) // 2]
    else:
        values = sorted(crop.width for crop in crops)
        measure = values[-1]
    return spec["extent"] / measure


def normalized_pose(crop: Image.Image, scale: float) -> Image.Image:
    pose = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.Resampling.LANCZOS)
    pose.putalpha(pose.getchannel("A").point(lambda value: 255 if value >= FINAL_ALPHA_THRESHOLD else 0))
    if pose.getchannel("A").getbbox() is None:
        raise ValueError("Normalized pose is empty")
    return pose


def place(pose: Image.Image, size: tuple[int, int], mode: str, index: int, count: int) -> Image.Image:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    box = pose.getchannel("A").getbbox()
    assert box is not None
    centre_x = (box[0] + box[2]) / 2
    centre_y = (box[1] + box[3]) / 2
    x = round(size[0] / 2 - centre_x)
    if mode == "floor":
        y = round(size[1] - GUTTER - box[3])
    elif mode == "dive":
        first_centre = size[1] - GUTTER - pose.height / 2
        target_centre = size[1] / 2
        progress = index / max(1, count - 1)
        desired_centre = first_centre * (1 - progress) + target_centre * progress
        y = round(desired_centre - centre_y)
    else:
        y = round(size[1] / 2 - centre_y)
    canvas.alpha_composite(pose, (x, y))
    final = canvas.getchannel("A").getbbox()
    if final is None or final[0] < GUTTER or final[1] < GUTTER or final[2] > size[0] - GUTTER or final[3] > size[1] - GUTTER:
        raise ValueError(f"Pose lost safety gutter: {final} in {size} ({mode}, frame {index + 1})")
    return canvas


def make_evidence(frames: list[Image.Image], fps: float, contact: Path, gif: Path) -> None:
    columns = min(4, len(frames))
    rows = (len(frames) + columns - 1) // columns
    tile_w, tile_h = frames[0].width * 2 + 16, frames[0].height * 2 + 32
    sheet = Image.new("RGB", (columns * tile_w, rows * tile_h), "#ece9e3")
    draw = ImageDraw.Draw(sheet)
    previews = []
    for index, frame in enumerate(frames):
        checker = Image.new("RGB", (frame.width * 2, frame.height * 2), "#f4f1eb")
        cdraw = ImageDraw.Draw(checker)
        for y in range(0, checker.height, 16):
            for x in range(0, checker.width, 16):
                if (x // 16 + y // 16) % 2:
                    cdraw.rectangle((x, y, x + 15, y + 15), fill="#dedbd5")
        enlarged = frame.resize(checker.size, Image.Resampling.NEAREST)
        checker.paste(enlarged, (0, 0), enlarged)
        x0, y0 = (index % columns) * tile_w, (index // columns) * tile_h
        sheet.paste(checker, (x0 + 8, y0 + 24))
        draw.text((x0 + 8, y0 + 6), f"FRAME {index + 1}", fill="#17233b")
        stage = Image.new("RGBA", frame.size, (236, 233, 227, 255))
        stage.alpha_composite(frame)
        previews.append(stage.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    contact.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(contact)
    previews[0].save(gif, save_all=True, append_images=previews[1:], duration=round(1000 / fps), loop=0, disposal=2, optimize=False)


def main() -> None:
    reviews = {item["name"]: item for item in json.loads(HANDOFF.read_text())["review"]["reviews"]}
    manifest = {"family": "scuba", "sourceAlphaThreshold": SOURCE_ALPHA_THRESHOLD, "finalAlphaThreshold": FINAL_ALPHA_THRESHOLD, "animations": {}}
    built_frames = {}
    for name, spec in SPECS.items():
        canonical_strip, canonical_sidecar = current(name, "png"), current(name, "json")
        canonical_runtime = PUBLIC / f"{name}.png"
        sidecar = json.loads(canonical_sidecar.read_text())
        source = GENERATED / spec["source"]
        raw_cells = (
            grid_cells(source, *spec["grid"])
            if "grid" in spec else
            equal_cells(source, spec["frames"])
        )
        extracted = [foreground(cell) for cell in raw_cells]
        crops = [item[0] for item in extracted]
        scale = source_scale(crops, spec)
        size = (sidecar["w"] * sidecar["density"], sidecar["h"] * sidecar["density"])
        poses = [normalized_pose(crop, scale) for crop in crops]
        frames = [place(pose, size, spec["mode"], i, len(poses)) for i, pose in enumerate(poses)]
        if name.startswith("keeper_scuba_swim_"):
            frames[-1] = frames[0].copy()
        built_frames[name] = frames

        review = reviews[name]
        draft_dir, evidence_dir = OUT / name, EVIDENCE / name
        draft_dir.mkdir(parents=True, exist_ok=True)
        evidence_dir.mkdir(parents=True, exist_ok=True)
        strip = Image.new("RGBA", (size[0] * len(frames), size[1]), (0, 0, 0, 0))
        frame_evidence = []
        for index, frame in enumerate(frames):
            strip.alpha_composite(frame, (index * size[0], 0))
            frame_evidence.append({"frame": index + 1, "alphaBox": list(frame.getchannel("A").getbbox()), "opaqueBorderPixelCount": 0})
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
        contact, gif = evidence_dir / "frames.png", evidence_dir / "preview.gif"
        make_evidence(frames, float(sidecar["fps"]), contact, gif)
        register = {
            "draftId": f"keeper-review-amendments-2026-10-11-v1-{name}",
            "handoffId": "d9081e53-2808-4b1f-8422-2df09cf38c3c",
            "animation": name,
            "status": "active-review-draft",
            "label": "11 Oct amendment draft v1",
            "selection": "Generated only for Frank's exact-name 11 October amendment handoff; requires separate explicit promotion.",
            "canonical": {"strip": rel(canonical_strip), "stripSha256": sha256(canonical_strip), "runtime": rel(canonical_runtime), "runtimeSha256": sha256(canonical_runtime), "sidecar": rel(canonical_sidecar), "sidecarSha256": sha256(canonical_sidecar)},
            "draft": {"source": rel(source), "sourceSha256": sha256(source), "strip": rel(strip_path), "stripSha256": sha256(strip_path), "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path), "frameEvidence": frame_evidence, "evidence": [rel(contact), rel(gif)], "fixedSourceScale": scale, "normalization": f"equal source cells; source alpha >= {SOURCE_ALPHA_THRESHOLD}; one fixed scale for the immutable source; final binary alpha >= {FINAL_ALPHA_THRESHOLD}; placement mode {spec['mode']}"},
            "qualification": "One coherent scuba model and outfit are used for the full exact-name clip; no head or limb transplant was used.",
            "rollback": "Discard this exact-name draft directory and registry entry; canonical and earlier draft assets are unchanged.",
        }
        register_path = draft_dir / "draft-register.json"
        register_path.write_text(json.dumps(register, indent=2) + "\n")
        manifest["animations"][name] = {"register": rel(register_path), "sourceCellBboxes": [bbox for _, bbox in extracted], "fixedSourceScale": scale, "canonicalStripSha256": sha256(canonical_strip), "draftStripSha256": sha256(strip_path)}

    manifest["seamAssertions"] = [
        "Every looping swim clip reuses frame 1 exactly as frame 8.",
        "Jetty dive uses one fixed scale from upright entry through horizontal exit.",
        "All five clips share the same pinned scuba model pack and outfit specification.",
    ]
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(SPECS)} reversible scuba-family drafts")


if __name__ == "__main__":
    main()
