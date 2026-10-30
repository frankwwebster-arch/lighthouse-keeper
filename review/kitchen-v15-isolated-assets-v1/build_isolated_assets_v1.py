#!/usr/bin/env python3
"""Build tight, high-resolution transparent exports of the Kitchen v15 v7 parts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "review/kitchen-v15-isolated-assets-v1"
SOURCE = ROOT / "review/kitchen-v15-painted-room-v7/parts"
OUTPUT = PACKAGE / "assets-5x"
SCALE = 5
GUTTER = 24

PRESENTATION_OVERRIDES = {
    "dresser.png": ROOT / "review/kitchen-v15-painted-room-v5/sources/imagegen/dresser-clear-counter-transparent.png",
    "mixer.png": ROOT / "review/kitchen-proof-v8-assets-v1/sources/selected/stand_mixer.png",
    "toaster.png": ROOT / "review/kitchen-proof-v8-assets-v1/sources/selected/cream_toaster.png",
}

PRESENTATION_OVERRIDE_SHA256 = {
    "dresser.png": "194de29c91685f3ae29b39c24d09a22a00bb840f9b27f76f8790588861a36d57",
    "mixer.png": "b52a0c670687bbee558591981fdd4ba03c523cdf5e9cecde297dea406bdd342c",
    "toaster.png": "2cefcab9040fec30f024c531ee37d72465d099515e299a9074ae98e71db17025",
}

EXPECTED_SHA256 = {
    "calendar.png": "caecb96f7e1c7fc137621f9b1f9d0e584d1950f4e6d965dd01001c2da1230967",
    "clock.png": "b9caf0ae6cfa432f52e8e838e70b53d668e1e6a14023cb72acdb165e91ce58f4",
    "cooker_t1.png": "3513318eb0ad12e1fde92d154293e039b0c4a176de2b12c8c4e37a4fad378fc9",
    "cupboard_A1.png": "f3ea9f7bd8c38a57e2a36c3761f752558908ce814f8e9d244ef103b7482afe53",
    "cupboard_B1.png": "f3ea9f7bd8c38a57e2a36c3761f752558908ce814f8e9d244ef103b7482afe53",
    "cupboard_B2.png": "f3ea9f7bd8c38a57e2a36c3761f752558908ce814f8e9d244ef103b7482afe53",
    "cupboard_B3.png": "f3ea9f7bd8c38a57e2a36c3761f752558908ce814f8e9d244ef103b7482afe53",
    "dresser.png": "aea552c7a17ed64a2f8677c1bdd819193a84eae17dbaeacc0c7881f384215bff",
    "dw_slot_cupboard.png": "f3ea9f7bd8c38a57e2a36c3761f752558908ce814f8e9d244ef103b7482afe53",
    "fridge_t1.png": "f86f78ef5da92e6b58e59eeea1661e60f31ad65bc1590642f7c4c8b46f4c687f",
    "mixer.png": "e1fb51bef211d57b2039911a6c6559cd9ed5ed654664d18dbb2e1fe1707eb3b4",
    "prime_keeper.png": "756f0a723c55997a3d5c38c625765b4077e7d959b7cd5827bcf69c17e27f4444",
    "runA_worktop.png": "467681593ccd9475259a9547e12a499909987dd774000d4893cd13756ea21716",
    "runB_worktop.png": "4645c9222a1dd601e2a4267e9aaf3253b2237e1b729610d0154f236dabce5bdc",
    "sink_cabinet.png": "a4620fc1b889bc906f86290979f093b134699b8b3e0182e772bb469f79cd161c",
    "teapot.png": "fcb0a2ec2116bc609e10c5cc4cf6589c6d7f2321f83cc58b96da5a1728e624c1",
    "toaster.png": "f6d9a2635f3c4b7664c06e01d67a622602dfc8e60bb3804d3a40d12e96179a4e",
    "wall_cupboard_1.png": "f60eccededdb001ebd09c9d6e1472f9fa6c63b27961906330548194f47432e00",
    "wall_cupboard_2.png": "f60eccededdb001ebd09c9d6e1472f9fa6c63b27961906330548194f47432e00",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checkerboard(size: tuple[int, int], cell: int = 16) -> Image.Image:
    image = Image.new("RGB", size, "#e5e2dc")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#f5f2ec")
    return image


def build_contact_sheet(paths: list[Path]) -> None:
    columns = 4
    card_w, card_h = 560, 500
    margin, title_h = 36, 92
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (margin * 2 + columns * card_w, title_h + margin + rows * card_h),
        "#173f3d",
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((margin, 28), "KITCHEN v15 — 19 ISOLATED ASSETS — 5x TRANSPARENT PNG", fill="#fff6df", font=font)
    draw.text((margin, 50), "Preview checkerboard only; every delivered asset has real alpha.", fill="#cfe4dc", font=font)

    for index, path in enumerate(paths):
        row, column = divmod(index, columns)
        left = margin + column * card_w
        top = title_h + row * card_h
        preview = checkerboard((card_w - 20, card_h - 58))
        asset = Image.open(path).convert("RGBA")
        asset.thumbnail((card_w - 56, card_h - 94), Image.Resampling.LANCZOS)
        px = (preview.width - asset.width) // 2
        py = (preview.height - asset.height) // 2
        preview.paste(asset, (px, py), asset)
        sheet.paste(preview, (left + 10, top + 10))
        draw.text((left + 14, top + card_h - 34), f"{path.name}  {Image.open(path).size[0]}x{Image.open(path).size[1]}", fill="#fff6df", font=font)

    sheet.save(PACKAGE / "isolated-assets-contact-sheet.png", optimize=True)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    records: dict[str, object] = {}
    output_paths: list[Path] = []

    source_names = sorted(path.name for path in SOURCE.glob("*.png"))
    if source_names != sorted(EXPECTED_SHA256):
        raise SystemExit(f"Source set changed: {source_names}")

    for name in source_names:
        source_path = SOURCE / name
        if sha256(source_path) != EXPECTED_SHA256[name]:
            raise SystemExit(f"Pinned source hash changed: {name}")

        room_cut_image = Image.open(source_path).convert("RGBA")
        presentation_source = PRESENTATION_OVERRIDES.get(name, source_path)
        expected_presentation_sha = PRESENTATION_OVERRIDE_SHA256.get(name, EXPECTED_SHA256[name])
        if sha256(presentation_source) != expected_presentation_sha:
            raise SystemExit(f"Pinned presentation source hash changed: {name}")

        source_image = Image.open(presentation_source).convert("RGBA")
        alpha_bbox = source_image.getchannel("A").getbbox()
        if alpha_bbox is None:
            raise SystemExit(f"No visible pixels: {name}")

        actual_edge_crop = source_image.crop(alpha_bbox)
        export_scale = 1 if name in PRESENTATION_OVERRIDES else SCALE
        if export_scale == 1:
            scaled = actual_edge_crop
        else:
            scaled = actual_edge_crop.convert("RGBa").resize(
                (actual_edge_crop.width * export_scale, actual_edge_crop.height * export_scale),
                Image.Resampling.LANCZOS,
            ).convert("RGBA")
        export = Image.new(
            "RGBA",
            (scaled.width + GUTTER * 2, scaled.height + GUTTER * 2),
            (0, 0, 0, 0),
        )
        export.alpha_composite(scaled, (GUTTER, GUTTER))

        output_path = OUTPUT / name
        export.save(output_path, optimize=True)
        output_paths.append(output_path)

        records[name] = {
            "sourcePath": str(source_path.relative_to(ROOT)),
            "sourceSha256": EXPECTED_SHA256[name],
            "sourceCanvasPx": list(room_cut_image.size),
            "sourceActualEdgeBoundsPx": list(room_cut_image.getchannel("A").getbbox()),
            "presentationSourcePath": str(presentation_source.relative_to(ROOT)),
            "presentationSourceSha256": expected_presentation_sha,
            "presentationSourceCanvasPx": list(source_image.size),
            "presentationSourceActualEdgeBoundsPx": list(alpha_bbox),
            "actualEdgeCropPx": list(actual_edge_crop.size),
            "exportPath": str(output_path.relative_to(ROOT)),
            "exportCanvasPx": list(export.size),
            "exportScale": export_scale,
            "transparentGutterPx": GUTTER,
            "exportSha256": sha256(output_path),
        }

    manifest = {
        "schema": "lighthouse-keeper/kitchen-v15-isolated-assets-v1@1",
        "status": "review-export-awaiting-frank",
        "sourcePackage": "review/kitchen-v15-painted-room-v7",
        "sourceMutation": False,
        "runtimeMutation": False,
        "deployment": False,
        "assetCount": len(records),
        "format": "RGBA PNG; source actual-edge crop; native full-resolution donor where available, otherwise 5x Lanczos; 24px transparent export gutter",
        "assets": records,
    }
    (PACKAGE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    build_contact_sheet(output_paths)


if __name__ == "__main__":
    main()
