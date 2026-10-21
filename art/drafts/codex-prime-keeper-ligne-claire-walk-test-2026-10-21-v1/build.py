#!/usr/bin/env python3
"""Build the reversible Prime Keeper ligne-claire feasibility evidence.

The build intentionally preserves every source alpha byte.  It changes RGB
rendering only, using a small, named semantic palette shared by the approved
side endpoint and all eight approved Walk V6 frames.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

STATIC_SOURCE = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
WALK_DIR = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames"
WALK_SOURCES = [WALK_DIR / f"keeper_prime_walk-right_f{i}.png" for i in range(1, 9)]

CELL = (256, 320)
LOGICAL_CELL = (32, 40)
DENSITY = 8
ANCHOR_SOURCE = (128, 320)
ANCHOR_LOGICAL = (16, 40)
ALPHA_THRESHOLD = 8
FPS = 10  # approved Fast Timing V1 locomotion timing


# Named source-colour anchors and their deliberately restricted ligne-claire
# replacements.  This is a character-specific repaint, not a generic image
# filter: each family represents one Keeper material or intentional ink role.
PALETTE = [
    ("contour", (3, 4, 10), (13, 25, 52)),
    ("contour-soft", (18, 22, 38), (22, 39, 70)),
    ("marine-blue", (0, 92, 211), (15, 105, 205)),
    ("marine-blue-dark", (3, 59, 142), (13, 73, 148)),
    ("trouser-navy", (53, 61, 101), (56, 66, 108)),
    ("boot-blue", (98, 95, 144), (76, 84, 133)),
    ("cream", (252, 240, 221), (251, 242, 219)),
    ("cream-shadow", (225, 205, 184), (238, 224, 199)),
    ("skin", (252, 181, 121), (246, 176, 111)),
    ("skin-line", (206, 109, 70), (177, 76, 52)),
    ("badge-gold", (241, 190, 32), (244, 190, 24)),
    ("badge-shadow", (174, 124, 25), (184, 127, 22)),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_hash(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").getchannel("A").tobytes()).hexdigest()


def alpha_bounds(image: Image.Image) -> list[int]:
    alpha = np.asarray(image.convert("RGBA"), dtype=np.uint8)[:, :, 3]
    ys, xs = np.where(alpha > ALPHA_THRESHOLD)
    if not len(xs):
        return [0, 0, 0, 0]
    return [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)]


def floor_contact(image: Image.Image) -> dict[str, object]:
    alpha = np.asarray(image.convert("RGBA"), dtype=np.uint8)[:, :, 3]
    ys, xs = np.where(alpha > ALPHA_THRESHOLD)
    y = int(ys.max())
    row_x = np.where(alpha[y] > ALPHA_THRESHOLD)[0]
    return {
        "opaqueBottomY": y,
        "opaqueBottomXRangeInclusive": [int(row_x.min()), int(row_x.max())],
        "opaqueBottomXMidpoint": round(float((row_x.min() + row_x.max()) / 2), 3),
        "registeredFootAnchorSource": list(ANCHOR_SOURCE),
        "registeredFootAnchorLogical": list(ANCHOR_LOGICAL),
    }


def stylize(source: Image.Image) -> Image.Image:
    rgba = np.asarray(source.convert("RGBA"), dtype=np.uint8)
    rgb = rgba[:, :, :3].astype(np.int16)
    alpha = rgba[:, :, 3].copy()

    source_anchors = np.asarray([entry[1] for entry in PALETTE], dtype=np.int32)
    targets = np.asarray([entry[2] for entry in PALETTE], dtype=np.uint8)
    delta = rgb.astype(np.int32)[:, :, None, :] - source_anchors[None, None, :, :]
    distance = np.sum(delta * delta, axis=3, dtype=np.int32)
    labels = np.argmin(distance, axis=2)
    painted = targets[labels]

    # Preserve genuinely dark drawing as one stable deep-navy ink family.
    rgb32 = rgb.astype(np.int32)
    luminance = (rgb32[:, :, 0] * 299 + rgb32[:, :, 1] * 587 + rgb32[:, :, 2] * 114) // 1000
    painted[luminance < 30] = np.asarray(PALETTE[0][2], dtype=np.uint8)

    # Transparent RGB is canonicalised to zero; alpha itself is byte-identical.
    painted[alpha == 0] = 0
    result = np.dstack([painted, alpha]).astype(np.uint8)
    return Image.fromarray(result, "RGBA")


def checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    w, h = size
    canvas = Image.new("RGB", size, (235, 239, 238))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, min(x + tile - 1, w - 1), min(y + tile - 1, h - 1)), fill=(214, 222, 221))
    return canvas


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/System/Library/Fonts/Supplemental/Helvetica.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def labelled_pair(original: Image.Image, test: Image.Image, path: Path) -> None:
    header = 58
    gutter = 24
    panel = checker((CELL[0] * 2 + gutter, CELL[1] + header))
    panel.paste(original, (0, header), original)
    panel.paste(test, (CELL[0] + gutter, header), test)
    draw = ImageDraw.Draw(panel)
    draw.text((10, 17), "CURRENT PRIME KEEPER", fill=(13, 25, 52), font=font(16, True))
    draw.text((CELL[0] + gutter + 10, 17), "LIGNE-CLAIRE TEST", fill=(13, 25, 52), font=font(16, True))
    draw.line((CELL[0] + gutter // 2, 0, CELL[0] + gutter // 2, panel.height), fill=(172, 130, 29), width=2)
    panel.save(path, optimize=True)


def contact_sheet(frames: list[Image.Image], path: Path) -> None:
    labels = ["CONTACT", "DOWN", "PASSING", "UP", "OPPOSITE CONTACT", "OPPOSITE DOWN", "OPPOSITE PASSING", "OPPOSITE UP"]
    scale = 1
    header = 54
    gap = 8
    w = len(frames) * CELL[0] + (len(frames) - 1) * gap
    sheet = checker((w, CELL[1] + header), tile=16)
    draw = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(zip(frames, labels)):
        x = i * (CELL[0] + gap)
        sheet.paste(frame, (x, header), frame)
        draw.text((x + 8, 12), f"F{i + 1}  {label}", fill=(13, 25, 52), font=font(14, True))
        draw.line((x + 4, header + CELL[1] - 1, x + CELL[0] - 4, header + CELL[1] - 1), fill=(206, 55, 48), width=1)
    sheet.save(path, optimize=True)


def onion_sheet(frames: list[Image.Image], path: Path) -> None:
    header = 44
    gap = 8
    w = len(frames) * CELL[0] + (len(frames) - 1) * gap
    sheet = checker((w, CELL[1] + header), tile=16)
    draw = ImageDraw.Draw(sheet)
    for i, current in enumerate(frames):
        nxt = frames[(i + 1) % len(frames)]
        a0 = np.asarray(current.getchannel("A"), dtype=np.uint8)
        a1 = np.asarray(nxt.getchannel("A"), dtype=np.uint8)
        overlay = np.zeros((CELL[1], CELL[0], 4), dtype=np.uint8)
        overlay[:, :, 0] = 211
        overlay[:, :, 1] = 64
        overlay[:, :, 2] = 64
        overlay[:, :, 3] = (a1.astype(np.uint16) * 90 // 255).astype(np.uint8)
        cyan = np.zeros_like(overlay)
        cyan[:, :, 0] = 16
        cyan[:, :, 1] = 137
        cyan[:, :, 2] = 161
        cyan[:, :, 3] = (a0.astype(np.uint16) * 130 // 255).astype(np.uint8)
        x = i * (CELL[0] + gap)
        sheet.paste(Image.fromarray(cyan, "RGBA"), (x, header), Image.fromarray(cyan, "RGBA"))
        sheet.paste(Image.fromarray(overlay, "RGBA"), (x, header), Image.fromarray(overlay, "RGBA"))
        draw.text((x + 8, 11), f"F{i + 1} -> F{(i + 1) % len(frames) + 1}", fill=(13, 25, 52), font=font(14, True))
    sheet.save(path, optimize=True)


def dimensional_sheet(original: Image.Image, test: Image.Image, path: Path, metrics: dict[str, object]) -> None:
    panel_w = 256
    header = 66
    footer = 148
    gap = 18
    canvas = checker((panel_w * 3 + gap * 2, CELL[1] + header + footer), tile=16)
    canvas.paste(original, (0, header), original)
    canvas.paste(test, (panel_w + gap, header), test)

    diff_alpha = np.asarray(original.getchannel("A"), dtype=np.int16) - np.asarray(test.getchannel("A"), dtype=np.int16)
    diff = np.zeros((CELL[1], CELL[0], 4), dtype=np.uint8)
    diff[:, :, 0] = 230
    diff[:, :, 1] = 46
    diff[:, :, 2] = 46
    diff[:, :, 3] = np.clip(np.abs(diff_alpha), 0, 255).astype(np.uint8)
    diff_img = Image.fromarray(diff, "RGBA")
    x3 = (panel_w + gap) * 2
    canvas.paste(diff_img, (x3, header), diff_img)

    draw = ImageDraw.Draw(canvas)
    titles = ["ORIGINAL", "TEST", "ALPHA DIFFERENCE"]
    for i, title in enumerate(titles):
        x = i * (panel_w + gap)
        draw.text((x + 8, 15), title, fill=(13, 25, 52), font=font(15, True))
        draw.line((x, header + ANCHOR_SOURCE[1] - 1, x + panel_w, header + ANCHOR_SOURCE[1] - 1), fill=(206, 55, 48), width=1)
        draw.line((x + ANCHOR_SOURCE[0], header, x + ANCHOR_SOURCE[0], header + CELL[1]), fill=(173, 130, 29), width=1)

    y = header + CELL[1] + 13
    lines = [
        "Canvas: 256 x 320 px  |  logical cell: 32 x 40  |  density: 8",
        "Anchor/origin: source [128,320]  |  logical [16,40]  |  baseline y=320",
        f"Original bbox: {metrics['original']['boundsExclusive']}  |  Test bbox: {metrics['test']['boundsExclusive']}",
        f"Alpha bytes equal: {metrics['alphaByteIdentical']}  |  differing alpha pixels: {metrics['alphaDifferingPixels']}",
        f"Foot-contact evidence: original {metrics['original']['floorContact']['opaqueBottomXRangeInclusive']} at y={metrics['original']['floorContact']['opaqueBottomY']}; test identical",
        "Red line = baseline/safety-gutter edge; gold line = registered x origin.",
    ]
    for line in lines:
        draw.text((10, y), line, fill=(13, 25, 52), font=font(13, False))
        y += 20
    canvas.save(path, optimize=True)


def metrics_for(source_path: Path, original: Image.Image, test_path: Path, test: Image.Image) -> dict[str, object]:
    a = np.asarray(original.getchannel("A"), dtype=np.int16)
    b = np.asarray(test.getchannel("A"), dtype=np.int16)
    return {
        "source": str(source_path.relative_to(ROOT)),
        "sourceSha256": sha256(source_path),
        "test": str(test_path.relative_to(ROOT)),
        "testSha256": sha256(test_path),
        "canvasPixels": list(original.size),
        "logicalCell": list(LOGICAL_CELL),
        "density": DENSITY,
        "sourceAnchor": list(ANCHOR_SOURCE),
        "logicalAnchor": list(ANCHOR_LOGICAL),
        "baselineSourceY": ANCHOR_SOURCE[1],
        "original": {
            "boundsExclusive": alpha_bounds(original),
            "alphaSha256": alpha_hash(original),
            "floorContact": floor_contact(original),
        },
        "testGeometry": {
            "boundsExclusive": alpha_bounds(test),
            "alphaSha256": alpha_hash(test),
            "floorContact": floor_contact(test),
        },
        "alphaByteIdentical": bool(np.array_equal(a, b)),
        "alphaDifferingPixels": int(np.count_nonzero(a != b)),
        "edgeAlphaPixelsOriginal": int(np.count_nonzero(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]))),
        "edgeAlphaPixelsTest": int(np.count_nonzero(np.concatenate([b[0], b[-1], b[:, 0], b[:, -1]]))),
    }


def main() -> None:
    for folder in (OUT / "static", OUT / "walk/frames", OUT / "evidence"):
        folder.mkdir(parents=True, exist_ok=True)

    original_static = Image.open(STATIC_SOURCE).convert("RGBA")
    assert original_static.size == CELL
    static_test = stylize(original_static)
    static_path = OUT / "static/keeper-prime-side-right-ligne-claire-test-v1.png"
    static_test.save(static_path, optimize=True)

    frames: list[Image.Image] = []
    frame_paths: list[Path] = []
    for i, source_path in enumerate(WALK_SOURCES, start=1):
        original = Image.open(source_path).convert("RGBA")
        assert original.size == CELL
        test = stylize(original)
        frame_path = OUT / f"walk/frames/keeper-prime-ligne-claire-walk-right-f{i}.png"
        test.save(frame_path, optimize=True)
        frames.append(test)
        frame_paths.append(frame_path)

    strip = Image.new("RGBA", (CELL[0] * len(frames), CELL[1]), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        strip.alpha_composite(frame, (i * CELL[0], 0))
    strip_path = OUT / "walk/keeper-prime-ligne-claire-walk-right-f8.png"
    strip.save(strip_path, optimize=True)

    sidecar = {
        "name": "keeper-prime-ligne-claire-walk-right-review-only",
        "status": "FEASIBILITY TEST — NOT APPROVED PRODUCTION ART",
        "w": LOGICAL_CELL[0],
        "h": LOGICAL_CELL[1],
        "density": DENSITY,
        "cell": list(CELL),
        "frames": len(frames),
        "fps": FPS,
        "loop": True,
        "direction": "right",
        "anchor": list(ANCHOR_LOGICAL),
        "sourceAnchor": list(ANCHOR_SOURCE),
        "baselineSourceY": ANCHOR_SOURCE[1],
        "sourceMotion": "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/keeper_prime_walk-right_f8.png",
        "sourceMotionSha256": sha256(ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/keeper_prime_walk-right_f8.png"),
        "timingAuthority": "Fast Timing V1 for locomotion",
        "renderTreatment": "Prime-specific restricted flat palette with shared deep-navy ink; source alpha is byte-identical per frame",
    }
    sidecar_path = OUT / "walk/keeper-prime-ligne-claire-walk-right-f8.json"
    sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")

    durations = [round(1000 / FPS)] * len(frames)
    gif_frames = [frame.copy() for frame in frames]
    gif_frames[0].save(OUT / "walk/keeper-prime-ligne-claire-walk-preview.gif", save_all=True, append_images=gif_frames[1:], duration=durations, loop=0, disposal=2, transparency=0)
    frames[0].save(OUT / "walk/keeper-prime-ligne-claire-walk-preview.webp", save_all=True, append_images=frames[1:], duration=durations, loop=0, lossless=True, quality=100, method=6)

    labelled_pair(original_static, static_test, OUT / "evidence/current-vs-ligne-claire.png")
    contact_sheet(frames, OUT / "evidence/walk-contact-sheet.png")
    onion_sheet(frames, OUT / "evidence/onion-skin-adjacent.png")

    static_metrics = metrics_for(STATIC_SOURCE, original_static, static_path, static_test)
    evidence_metrics = {
        "status": "FEASIBILITY TEST — NOT APPROVED PRODUCTION ART",
        "geometryPolicy": "RGB treatment may change; source alpha bytes, cell, density, anchor, baseline and frame registration must not.",
        "static": static_metrics,
        "walk": [
            metrics_for(src, Image.open(src).convert("RGBA"), dst, frame)
            for src, dst, frame in zip(WALK_SOURCES, frame_paths, frames)
        ],
        "animation": {
            "frames": 8,
            "fps": FPS,
            "timingAuthority": "Fast Timing V1 for locomotion",
            "frameOrder": ["contact", "down", "passing", "up", "opposite-contact", "opposite-down", "opposite-passing", "opposite-up"],
            "cellPixels": list(CELL),
            "stripPixels": [CELL[0] * len(frames), CELL[1]],
            "rootMotionLogicalPixelsPerSecond": 21,
        },
        "palette": [{"role": role, "rgb": list(target)} for role, _source, target in PALETTE],
    }
    metrics_path = OUT / "evidence/dimensional-verification.json"
    metrics_path.write_text(json.dumps(evidence_metrics, indent=2) + "\n")

    dim_summary = {
        "original": {
            "boundsExclusive": static_metrics["original"]["boundsExclusive"],
            "floorContact": static_metrics["original"]["floorContact"],
        },
        "test": {
            "boundsExclusive": static_metrics["testGeometry"]["boundsExclusive"],
            "floorContact": static_metrics["testGeometry"]["floorContact"],
        },
        "alphaByteIdentical": static_metrics["alphaByteIdentical"],
        "alphaDifferingPixels": static_metrics["alphaDifferingPixels"],
    }
    dimensional_sheet(original_static, static_test, OUT / "evidence/dimensional-comparison.png", dim_summary)

    failures = []
    for label, record in [("static", static_metrics)] + [(f"walk-f{i + 1}", record) for i, record in enumerate(evidence_metrics["walk"])]:
        if not record["alphaByteIdentical"]:
            failures.append(f"{label}: alpha differs")
        if record["original"]["boundsExclusive"] != record["testGeometry"]["boundsExclusive"]:
            failures.append(f"{label}: bounds differ")
        if record["edgeAlphaPixelsTest"] != 0:
            failures.append(f"{label}: shared-edge alpha")
        if record["canvasPixels"] != list(CELL):
            failures.append(f"{label}: cell mismatch")
    if failures:
        raise SystemExit("\n".join(failures))

    sidecar["sha256"] = sha256(strip_path)
    sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")

    generated_studies = []
    for study in sorted((OUT / "sources/generated-studies").glob("*.png")):
        generated_studies.append({"file": str(study.relative_to(ROOT)), "sha256": sha256(study), "role": "rendering-language study only; rejected as geometry authority"})
    output_paths = [static_path, strip_path, sidecar_path, metrics_path]
    output_paths += frame_paths
    output_paths += sorted((OUT / "walk").glob("*.gif")) + sorted((OUT / "walk").glob("*.webp"))
    output_paths += sorted((OUT / "evidence").glob("*.png"))
    register = {
        "batchId": "codex-prime-keeper-ligne-claire-walk-test-2026-10-21-v1",
        "status": "FEASIBILITY TEST — NOT APPROVED PRODUCTION ART",
        "scope": "Rendering-treatment proof only. No production, canonical, runtime, manifest, gameplay, or interaction asset is changed.",
        "authorities": [
            {"role": "permanent Prime identity/face/front authority", "file": "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png", "sha256": sha256(ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png")},
            {"role": "approved static side-right endpoint and dimensional authority", "file": str(STATIC_SOURCE.relative_to(ROOT)), "sha256": sha256(STATIC_SOURCE)},
            {"role": "approved eight-frame side-right locomotion artwork authority", "file": "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/keeper_prime_walk-right_f8.png", "sha256": sha256(ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/keeper_prime_walk-right_f8.png")},
        ],
        "generatedStudies": generated_studies,
        "method": {
            "imageGeneration": "Two built-in image-generation studies established the target rendering language; neither generated silhouette was accepted as geometry.",
            "finalArtwork": "Deterministic character-specific semantic repaint of approved Prime pixels; exact source alpha retained byte-for-byte.",
            "paletteRoles": [role for role, _source, _target in PALETTE],
            "genericFilterOrEdgeDetection": False,
        },
        "geometry": {
            "logicalCell": list(LOGICAL_CELL),
            "density": DENSITY,
            "cellPixels": list(CELL),
            "logicalAnchor": list(ANCHOR_LOGICAL),
            "sourceAnchor": list(ANCHOR_SOURCE),
            "baselineSourceY": ANCHOR_SOURCE[1],
            "alphaByteIdenticalAllFrames": True,
            "transparentSafetyGutterAllFrames": True,
        },
        "animation": sidecar,
        "outputs": [{"file": str(path.relative_to(ROOT)), "sha256": sha256(path)} for path in sorted(set(output_paths))],
        "rollback": "Delete only this versioned draft directory. No canonical or production file depends on it.",
    }
    (OUT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")

    print(json.dumps({"status": "pass", "static": str(static_path.relative_to(ROOT)), "strip": str(strip_path.relative_to(ROOT)), "frames": len(frames), "fps": FPS}, indent=2))


if __name__ == "__main__":
    main()
