#!/usr/bin/env python3
"""Verify isolated Kitchen v15 exports and their immutable v7 sources."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "review/kitchen-v15-isolated-assets-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads((PACKAGE / "manifest.json").read_text())
    assets = manifest["assets"]
    assert manifest["assetCount"] == 19 == len(assets)
    assert manifest["sourceMutation"] is False
    assert manifest["runtimeMutation"] is False
    assert manifest["deployment"] is False

    for name, record in assets.items():
        source = ROOT / record["sourcePath"]
        presentation_source = ROOT / record["presentationSourcePath"]
        output = ROOT / record["exportPath"]
        assert sha256(source) == record["sourceSha256"], name
        assert sha256(presentation_source) == record["presentationSourceSha256"], name
        assert sha256(output) == record["exportSha256"], name

        source_image = Image.open(source).convert("RGBA")
        presentation_image = Image.open(presentation_source).convert("RGBA")
        output_image = Image.open(output).convert("RGBA")
        assert list(source_image.size) == record["sourceCanvasPx"], name
        assert list(source_image.getchannel("A").getbbox()) == record["sourceActualEdgeBoundsPx"], name
        assert list(presentation_image.size) == record["presentationSourceCanvasPx"], name
        assert list(presentation_image.getchannel("A").getbbox()) == record["presentationSourceActualEdgeBoundsPx"], name
        assert list(output_image.size) == record["exportCanvasPx"], name
        assert output_image.getchannel("A").getextrema() == (0, 255), name

        crop_w, crop_h = record["actualEdgeCropPx"]
        gutter = record["transparentGutterPx"]
        scale = record["exportScale"]
        assert output_image.size == (crop_w * scale + gutter * 2, crop_h * scale + gutter * 2), name
        assert output_image.getpixel((0, 0))[3] == 0, name

    identical_base_cabinets = [
        "cupboard_A1.png",
        "dw_slot_cupboard.png",
        "cupboard_B1.png",
        "cupboard_B2.png",
        "cupboard_B3.png",
    ]
    assert len({assets[name]["sourceSha256"] for name in identical_base_cabinets}) == 1
    assert len({assets[name]["exportSha256"] for name in identical_base_cabinets}) == 1
    assert assets["wall_cupboard_1.png"]["sourceSha256"] == assets["wall_cupboard_2.png"]["sourceSha256"]
    assert assets["wall_cupboard_1.png"]["exportSha256"] == assets["wall_cupboard_2.png"]["exportSha256"]

    assert assets["dresser.png"]["presentationSourceCanvasPx"] == [999, 1575]
    assert assets["mixer.png"]["presentationSourceCanvasPx"] == [1142, 1377]
    assert assets["toaster.png"]["presentationSourceCanvasPx"] == [1387, 1134]

    print("PASS: 19 isolated transparent assets; pinned sources; exact-edge crops; native high-res donors; repeated cabinets identical")


if __name__ == "__main__":
    main()
