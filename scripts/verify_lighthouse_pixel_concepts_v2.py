#!/usr/bin/env python3
"""Verify Lighthouse Keeper pixel-style comparison V2 deterministically."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "public" / "art" / "concepts" / "pixel" / "manifest-v2.json"
ARCHIVE_INDEX = ROOT / "review-archive" / "index.json"
MAGENTA = np.asarray((255, 0, 255), dtype=np.uint8)


def sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def colour_count(image: Image.Image) -> int:
    colours = image.convert("RGB").getcolors(maxcolors=image.width * image.height)
    if colours is None:
        raise AssertionError("Image exceeded its maximum possible colour count")
    return len(colours)


def resolve_review_asset(relative_path: str, expected_sha256: str) -> Path:
    """Resolve a freshly built public asset or its archived immutable object."""

    public_path = ROOT / relative_path
    if public_path.exists():
        return public_path

    prefix = "public/"
    if not relative_path.startswith(prefix):
        raise AssertionError(f"Missing non-public asset: {relative_path}")
    legacy_path = "/" + relative_path[len(prefix) :]
    index = json.loads(ARCHIVE_INDEX.read_text(encoding="utf-8"))
    entry = index["legacyPaths"].get(legacy_path)
    if entry is None:
        raise AssertionError(f"Missing public and archived review asset: {relative_path}")
    assert entry["sha256"] == expected_sha256
    object_path = ROOT / entry["object"]
    assert object_path.exists()
    return object_path


def verify_geometry(image: Image.Image, geometry: dict) -> None:
    array = np.asarray(image.convert("RGB"))
    assert geometry["module"] in ([384, 128], [192, 64])
    expected_wall = 8 if geometry["module"][0] == 384 else 4
    expected_window = 48 if geometry["module"][0] == 384 else 24
    expected_bay = 24 if geometry["module"][0] == 384 else 12
    assert geometry["wallBand"] == expected_wall
    assert geometry["floorCeilingBand"] == expected_wall
    assert geometry["windowOuterSize"] == [expected_window, expected_window]
    assert geometry["bayWidth"] == expected_bay
    assert len(geometry["floorTops"]) == 3
    assert all(
        geometry["floorTops"][index + 1] - geometry["floorTops"][index]
        == geometry["module"][1]
        for index in range(2)
    )
    shell = geometry["outerShell"]
    pocket = geometry["hiddenCirculationPocket"]
    assert shell["topBounds"][0] > shell["baseBounds"][0]
    assert shell["topBounds"][1] < shell["baseBounds"][1]
    assert shell["taperPerSide"] > 0
    assert pocket["visible"] is False
    assert pocket["leftShellToRoomGapAtTop"] > 0
    assert pocket["leftShellToRoomGapAtBase"] > pocket["leftShellToRoomGapAtTop"]
    assert pocket["entrancePresentation"] == "slim edge-on jamb only"
    outdoors = geometry["outdoors"]
    assert outdoors["visibleTopFaces"] is False
    assert outdoors["presentation"] == "single orthographic side-profile panel"
    assert outdoors["groundLineY"] == geometry["groundLineY"]
    assert outdoors["plotWidth"] == geometry["module"][0]
    for plot in ("bedBounds", "lawnBounds", "terraceBounds"):
        left, _top, right, _bottom = outdoors[plot]
        assert right - left == geometry["module"][0]
    assert outdoors["stairPresentation"] == "side profile on far-right cliff only"
    for floor in geometry["windowGlassRects"]:
        assert len(floor) == 2
        for left, top, right, bottom in floor:
            glass = array[top : bottom + 1, left : right + 1]
            assert glass.size > 0
            assert np.all(glass == MAGENTA), (left, top, right, bottom)


def main() -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert payload["status"] == "review-only; no runtime or canon promotion"
    assert payload["magenta"] == "#FF00FF"

    expected = {
        "A-generated-16-bit": ((1920, 1080), 32, 3, 62),
        "B-generated-8-bit": ((960, 540), 16, 6, 31),
        "C-code-only-legacy-control": ((1920, 1080), 32, 3, 62),
    }

    for record in payload["concepts"]:
        concept_id = record["id"]
        native_size, colour_limit, factor, keeper_height = expected[concept_id]
        source_path = ROOT / record["source"]
        native_path = resolve_review_asset(
            record["native"]["path"], record["native"]["sha256"]
        )
        view_path = resolve_review_asset(
            record["view"]["path"], record["view"]["sha256"]
        )

        assert sha256(source_path) == record["sourceSha256"]
        assert sha256(native_path) == record["native"]["sha256"]
        assert sha256(view_path) == record["view"]["sha256"]

        native = Image.open(native_path).convert("RGB")
        view = Image.open(view_path).convert("RGB")
        assert native.size == native_size
        assert view.size == (native_size[0] * factor, native_size[1] * factor)
        assert record["view"]["integerUpscale"] == factor
        assert ImageChops.difference(
            native.resize(view.size, Image.Resampling.NEAREST), view
        ).getbbox() is None

        colours = colour_count(native)
        assert colours == record["native"]["paletteCount"]
        assert colours <= colour_limit
        array = np.asarray(native)
        key_count = int(np.all(array == MAGENTA, axis=2).sum())
        assert key_count == record["native"]["magentaPixels"]
        assert key_count > 0
        assert record["native"]["alphaValues"] == [255]
        assert record["keeper"]["visibleHeight"] == keeper_height

        if record["geometry"] is not None:
            verify_geometry(native, record["geometry"])
            assert record["ruleBreaks"] == []
        else:
            assert len(record["ruleBreaks"]) == 3

    comparison = payload["comparison"]
    comparison_path = resolve_review_asset(comparison["path"], comparison["sha256"])
    assert sha256(comparison_path) == comparison["sha256"]
    assert Image.open(comparison_path).size == tuple(comparison["size"])
    assert comparison["panelSize"] == [1920, 1080]
    print(
        "Lighthouse pixel concepts V2 verified: exact native grids, tapered "
        "red/white shell, concealed circulation pocket, 32/16-colour "
        "limits, reserved magenta, hard alpha, approved Keeper scale, exact "
        "nearest-neighbour views and labelled A/B/C comparison."
    )


if __name__ == "__main__":
    main()
