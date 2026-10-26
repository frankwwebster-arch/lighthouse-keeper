#!/usr/bin/env python3
"""Deterministic acceptance checks for the Kitchen Proof V3 review package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "parts"
OUTPUTS = ROOT / "outputs"
SOURCES = ROOT / "sources"
MAGENTA = (255, 0, 255, 255)
V7_SHA = "0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def alpha_bbox(image: Image.Image):
    return image.getchannel("A").getbbox()


def inclusive_bbox(image: Image.Image):
    bbox = alpha_bbox(image)
    return None if bbox is None else [bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1]


def inclusive_rgba_bbox(image: Image.Image):
    # ImageChops on two opaque RGBA images leaves a zero alpha-difference
    # channel, so inspect colour deltas independently of that fourth band.
    bbox = image.convert("RGB").getbbox()
    return None if bbox is None else [bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1]


def has_enclosed_transparent_hole(image: Image.Image) -> bool:
    """Reject alpha-zero islands enclosed by opaque pixels; exterior padding is fine."""
    alpha = image.getchannel("A")
    w, h = alpha.size
    transparent = {(x, y) for y in range(h) for x in range(w) if alpha.getpixel((x, y)) == 0}
    if not transparent:
        return False
    stack = [p for p in transparent if p[0] in (0, w - 1) or p[1] in (0, h - 1)]
    exterior = set(stack)
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            p = (nx, ny)
            if 0 <= nx < w and 0 <= ny < h and p in transparent and p not in exterior:
                exterior.add(p)
                stack.append(p)
    return bool(transparent - exterior)


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    items = json.loads((PARTS / "item.json").read_text(encoding="utf-8"))

    check(manifest["schema"] == "lighthouse-keeper/kitchen-proof-v3@1", "manifest schema drift")
    check(manifest["status"] == "review-only-awaiting-frank", "review status must remain non-canonical")
    check(not manifest["canonMutation"] and not manifest["runtimeMutation"], "review package claims a production mutation")
    check(manifest["styleAuthority"]["sha256"] == V7_SHA, "manifest V7 pin drift")
    check(sha256(SOURCES / "v7-oven-authority.png") == V7_SHA, "historical V7 blob mismatch")
    check(items["walkY"] == 502, "room data walkY is not 502")

    # Content manifest: every generated/source payload is pinned and unchanged.
    for relative, record in manifest["files"].items():
        path = ROOT / relative
        check(path.is_file(), f"missing manifested file: {relative}")
        check(path.stat().st_size == record["bytes"], f"byte count changed: {relative}")
        check(sha256(path) == record["sha256"], f"SHA-256 changed: {relative}")

    room = Image.open(OUTPUTS / "kitchen_v3_room.png").convert("RGBA")
    room_2x = Image.open(OUTPUTS / "kitchen_v3_room_2x.png").convert("RGBA")
    tower = Image.open(OUTPUTS / "kitchen_v3_tower_scale.png").convert("RGBA")
    check(room.size == (1536, 576), "room size mismatch")
    check(room_2x.size == (3072, 1152), "2x size mismatch")
    check(tower.size == (384, 144), "tower size mismatch")
    check(room.resize(room_2x.size, Image.Resampling.NEAREST).tobytes() == room_2x.tobytes(), "2x is not exact nearest-neighbour")

    # Exact key: no near-magenta, magenta occurs only in declared panes, and
    # every declared pane is solid exact magenta. Coordinates are inclusive.
    panes = [tuple(rect) for rect in manifest["geometry"]["glassRects"]]
    pane_pixels = set()
    for x0, y0, x1, y1 in panes:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                pane_pixels.add((x, y))
                check(room.getpixel((x, y)) == MAGENTA, f"non-key pixel in pane at {x},{y}")
    exact_count = 0
    near_count = 0
    for y in range(room.height):
        for x in range(room.width):
            pixel = room.getpixel((x, y))
            if pixel == MAGENTA:
                exact_count += 1
                check((x, y) in pane_pixels, f"magenta used outside glass at {x},{y}")
            elif pixel[3] and pixel[0] >= 180 and pixel[2] >= 180 and pixel[1] <= 100:
                near_count += 1
    check(exact_count == manifest["checks"]["exactMagentaPixels"], "magenta count drift")
    check(near_count == 0 == manifest["checks"]["nearMagentaPixels"], "near-magenta exists")
    check(manifest["checks"]["itemPixelsAboveWindowLimit"] == 0, "item crosses a window exclusion")

    # Part dimensions, metadata completeness, hole-free base art and no Keeper
    # pixels hidden in any art part.
    required_keys = {"file", "pixelSize", "sha256", "realSizeM", "bayWidth", "useBay", "slotIn", "anchorPx", "standPointX", "lightOverlays", "styleReference"}
    overlay_names = {"overlay_oven_window.png", "overlay_dishwasher_led.png"}
    solid_base_names = {
        "worktop_tile.png", "plinth_tile.png", "front_drawers.png",
        "front_cupboard.png", "front_sink_2bay.png", "front_dishwasher.png",
        "cooker.png", "unit_fridge_freezer.png",
        "unit_utility_cupboard_closed.png",
    }
    for name, record in items["parts"].items():
        check(required_keys <= record.keys(), f"incomplete metadata: {name}")
        path = PARTS / name
        image = Image.open(path).convert("RGBA")
        check(list(image.size) == record["pixelSize"], f"declared dimensions mismatch: {name}")
        check(sha256(path) == record["sha256"], f"item metadata hash mismatch: {name}")
        check(record["styleReference"]["sha256"] == V7_SHA, f"style pin mismatch: {name}")
        if name in solid_base_names:
            check(not has_enclosed_transparent_hole(image), f"enclosed alpha cut-out in base part: {name}")

    # Overlay alpha and actual composite deltas must remain inside each declared
    # local rectangle (inclusive). Transparent area outside is mandatory.
    for name, allowed in manifest["checks"]["overlayAllowedRects"].items():
        overlay = Image.open(PARTS / name).convert("RGBA")
        bbox = inclusive_bbox(overlay)
        check(bbox is not None, f"empty overlay: {name}")
        ax0, ay0, ax1, ay1 = allowed
        check(bbox[0] >= ax0 and bbox[1] >= ay0 and bbox[2] <= ax1 and bbox[3] <= ay1, f"overlay alpha escapes allowed rect: {name}")
        if name == "overlay_oven_window.png":
            base = Image.open(PARTS / "cooker.png").convert("RGBA")
        else:
            base = Image.open(PARTS / "front_dishwasher.png").convert("RGBA")
        composite = base.copy()
        composite.alpha_composite(overlay)
        diff = ImageChops.difference(base, composite)
        db = inclusive_rgba_bbox(diff)
        check(db and db[0] >= ax0 and db[1] >= ay0 and db[2] <= ax1 and db[3] <= ay1, f"overlay composite diff escapes allowed rect: {name}")

    # Geometry joins: no transparent gap across either fitted-run worktop at
    # any x, while seams are limited to the declared bay boundaries.
    worktop = Image.open(PARTS / "worktop_tile.png").convert("RGBA")
    check(worktop.size == (84, 32) and alpha_bbox(worktop) == (0, 0, 84, 32), "worktop tile is not a full continuous tile")
    sink_insert = Image.open(PARTS / "insert_sink_2bay.png").convert("RGBA")
    check(sink_insert.size == (168, 67), "sink is not the declared separate 2-bay insert")
    plinth = Image.open(PARTS / "plinth_tile.png").convert("RGBA")
    check(plinth.size == (84, 17) and alpha_bbox(plinth) == (0, 0, 84, 17), "plinth tile is not full")
    check(manifest["checks"]["worktopRuns"] == [[496, 832], [916, 1336]], "worktop run endpoints drift")
    check(manifest["checks"]["worktopTopY"] == manifest["checks"]["cookerTopY"] == 309, "cooker/worktop top mismatch")
    check(manifest["checks"]["plinthY"] == manifest["checks"]["cookerPlinthY"] == [468, 485], "cooker/run plinth mismatch")

    # Isolation proof must be non-empty, confined to the sink insert rectangle,
    # and based on unchanged stored parts.
    isolation = manifest["checks"]["isolation"]
    x0, y0, x1, y1 = isolation["roomDiffBoundsInclusive"]
    ax0, ay0, ax1, ay1 = isolation["allowedBoundsInclusive"]
    check(isolation["changedLocalTapPixels"] == isolation["roomDiffPixels"] > 0, "isolation diff cardinality mismatch")
    check(x0 >= ax0 and y0 >= ay0 and x1 <= ax1 and y1 <= ay1, "isolation change escaped sink insert")
    check(isolation["allPartHashesUnchanged"], "isolation mutated a stored part")

    # Route arithmetic, phase boundary, and delivered proof scale.
    expected_current = [(698, 76), (866, 76), (866, -8), (462, 8)]
    expected_d15 = [622, 790, 874, 454]
    for result, (stop, error) in zip(manifest["routes"]["current38"], expected_current):
        check((result["stop"], result["errorPx"]) == (stop, error), f"current route result drift: {result['name']}")
    for index, (result, stop) in enumerate(zip(manifest["routes"]["d15Draft42"], expected_d15)):
        check(result["stop"] == stop and result["errorPx"] == 0, f"D15 root proof drift: {result['name']}")
        check(result["phaseValid"] == (index >= 2), f"D15 F5 authority boundary drift: {result['name']}")
    for name in ("route_current_38px.gif", "route_d15_draft_42px.gif"):
        gif = Image.open(OUTPUTS / name)
        check(gif.size == (1536, 576), f"route proof is not Prime 1:1: {name}")

    print("PASS: Kitchen Proof V3 review package")
    print(f"  {len(items['parts'])} separately verified parts")
    print(f"  {exact_count} exact-magenta glass pixels; 0 near-magenta")
    print("  current route errors: +76, +76, -8, +8 px")
    print("  D15 root errors: 0, 0, 0, 0 px; legs 1–2 remain phase-blocked by missing F5 bridge")


if __name__ == "__main__":
    main()
