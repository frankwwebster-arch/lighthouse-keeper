#!/usr/bin/env python3
"""Verify the Gate 0 style proof geometry, key colour and provenance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
MAGENTA = (255, 0, 255, 255)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixels(image: Image.Image):
    return image.convert("RGBA").get_flattened_data()


def near_magenta(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r >= 200 and b >= 200 and g <= 80 and pixel != MAGENTA


def assert_key_mask(image: Image.Image) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    rgba = image.convert("RGBA")
    for y in range(rgba.height):
        for x in range(rgba.width):
            pixel = rgba.getpixel((x, y))
            if pixel == MAGENTA:
                result.add((x, y))
            if near_magenta(pixel):
                raise AssertionError(f"near-magenta non-key pixel at {(x, y)}: {pixel}")
    assert result, "missing exact magenta"
    return result


def main() -> None:
    manifest_path = ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "candidate-awaiting-frank"
    assert manifest["canonMutation"] is False
    assert manifest["geometry"]["deliveredModulePx"] == [1536, 512]
    assert manifest["geometry"]["bayCount"] == 13
    assert manifest["geometry"]["bayWidthPx"] == 96

    for source in manifest["sources"].values():
        path = ROOT / source["path"]
        assert path.is_file(), path
        assert sha256(path) == source["sha256"], path

    loaded: dict[str, Image.Image] = {}
    for name, record in manifest["outputs"].items():
        path = ROOT / record["path"]
        assert path.is_file(), path
        assert sha256(path) == record["sha256"], path
        image = Image.open(path).convert("RGBA")
        assert list(image.size) == record["size"]
        assert sum(1 for pixel in pixels(image) if pixel == MAGENTA) == record["magentaPixels"]
        assert all(pixel[3] in (0, 255) for pixel in pixels(image)) == record["hardAlpha"]
        loaded[name] = image

    a_authoring = loaded["candidateAAuthoring"]
    a_room = loaded["candidateARoom"]
    b_room = loaded["candidateBRoom"]
    a_tower = loaded["candidateATower"]
    b_tower = loaded["candidateBTower"]

    assert a_authoring.size == (768, 256)
    assert a_room.size == (1536, 512)
    assert b_room.size == (1536, 512)
    assert a_tower.size == (384, 128)
    assert b_tower.size == (384, 128)

    # Candidate A delivery must be an exact 2x nearest-neighbour expansion.
    expected_a = a_authoring.resize((1536, 512), Image.Resampling.NEAREST)
    assert expected_a.tobytes() == a_room.tobytes(), "candidate A is not exact 2x"

    # The two styles must compare the exact same key apertures at ROOM scale.
    assert assert_key_mask(a_room) == assert_key_mask(b_room)

    # Window boxes and the four exact key panes inside each are fixed.
    for window_x in (544, 1120):
        for x0, x1 in ((window_x + 16, window_x + 91), (window_x + 100, window_x + 175)):
            for y0, y1 in ((146, 219), (228, 303)):
                for y in range(y0, y1 + 1):
                    for x in range(x0, x1 + 1):
                        assert a_room.getpixel((x, y)) == MAGENTA
                        assert b_room.getpixel((x, y)) == MAGENTA

    # A is intentionally palette-bounded; B is genuinely smoother/richer.
    a_colours = len(set(pixels(a_room)))
    b_colours = len(set(pixels(b_room)))
    assert a_colours <= 64, a_colours
    assert b_colours > a_colours, (a_colours, b_colours)

    # Keepers stand inside the approved walk-in zone and on the floor line.
    assert manifest["candidates"]["A"]["keeperHeightPx"] in range(244, 251)
    assert manifest["candidates"]["B"]["keeperHeightPx"] in range(244, 251)

    print(
        "Gate 0 style proof verified: exact grid, identical exact-magenta masks, "
        f"A exact 2x ({a_colours} colours), B smooth ({b_colours} RGBA colours), "
        "sources and outputs hash-pinned."
    )


if __name__ == "__main__":
    main()
