#!/usr/bin/env python3
"""Acceptance tests for the Kitchen V3 modular rebuild."""

from __future__ import annotations

import hashlib
import importlib.util
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


def inclusive_bbox(image: Image.Image, alpha: bool = True):
    subject = image.getchannel("A") if alpha else image.convert("RGB")
    bbox = subject.getbbox()
    return None if bbox is None else [bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1]


def load_builder():
    spec = importlib.util.spec_from_file_location("kitchen_v3_rebuild_builder", ROOT / "build_review.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def partial_alpha_confined_to_edge(image: Image.Image) -> bool:
    """A generated halo would leave partial alpha away from the hard silhouette."""
    alpha = image.getchannel("A")
    w, h = image.size
    opaque = {(x, y) for y in range(h) for x in range(w) if alpha.getpixel((x, y)) == 255}
    for y in range(h):
        for x in range(w):
            value = alpha.getpixel((x, y))
            if 0 < value < 255:
                if not any((x + dx, y + dy) in opaque for dx in range(-2, 3) for dy in range(-2, 3)):
                    return False
    return True


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    items = json.loads((PARTS / "item.json").read_text(encoding="utf-8"))
    room_data = json.loads((PARTS / "room.json").read_text(encoding="utf-8"))

    check(manifest["schema"] == "lighthouse-keeper/kitchen-proof-v3-rebuild@1", "manifest schema drift")
    check(manifest["status"] == "review-only-awaiting-frank", "candidate must remain review-only")
    check(not manifest["canonMutation"] and not manifest["runtimeMutation"], "production boundary crossed")
    check(sha256(SOURCES / "v7-oven-authority.png") == V7_SHA, "V7 historical authority changed")
    check(sha256(SOURCES / "approved-style-calibration.png") == manifest["style"]["approvedCalibrationSha256"], "approved calibration changed")
    check(room_data["walkY"] == 502 and room_data["bayCount"] == 14 and room_data["bayWidthPx"] == 84, "room data geometry drift")
    shell = Image.open(PARTS / "room_shell_kitchen.png").convert("RGBA")
    check(shell.size == (1536, 576), "room shell size mismatch")
    check(sha256(PARTS / "room_shell_kitchen.png") == manifest["shell"]["sha256"], "room shell hash mismatch")

    for relative, record in manifest["files"].items():
        path = ROOT / relative
        check(path.is_file(), f"missing manifested file: {relative}")
        check(path.stat().st_size == record["bytes"], f"byte count changed: {relative}")
        check(sha256(path) == record["sha256"], f"SHA-256 changed: {relative}")

    room = Image.open(OUTPUTS / "kitchen_v3_rebuild_room.png").convert("RGBA")
    room2 = Image.open(OUTPUTS / "kitchen_v3_rebuild_room_2x.png").convert("RGBA")
    tower = Image.open(OUTPUTS / "kitchen_v3_rebuild_tower_scale.png").convert("RGBA")
    check(room.size == (1536, 576), "room size mismatch")
    check(room2.size == (3072, 1152), "2x size mismatch")
    check(tower.size == (384, 144), "tower-scale size mismatch")
    check(room.resize(room2.size, Image.Resampling.NEAREST).tobytes() == room2.tobytes(), "2x output is not nearest-neighbour")

    # Key-colour gates. Every pane is a deterministic hard rectangle; key is
    # forbidden everywhere else.
    pane_pixels = set()
    local_rects = manifest["geometry"]["glassLocalRects"]
    for wx, wy, _, _ in manifest["geometry"]["windows"]:
        for lx0, ly0, lx1, ly1 in local_rects:
            for y in range(wy + ly0, wy + ly1 + 1):
                for x in range(wx + lx0, wx + lx1 + 1):
                    pane_pixels.add((x, y))
                    check(room.getpixel((x, y)) == MAGENTA, f"non-key glass pixel at {x},{y}")
    exact = 0
    near = 0
    for y in range(room.height):
        for x in range(room.width):
            r, g, b, a = room.getpixel((x, y))
            if (r, g, b, a) == MAGENTA:
                exact += 1
                check((x, y) in pane_pixels, f"key used outside glass at {x},{y}")
            elif a and r >= 180 and b >= 180 and g <= 100:
                near += 1
    check(exact == len(pane_pixels) == manifest["checks"]["exactMagentaPixels"], "exact-magenta count drift")
    check(near == manifest["checks"]["nearMagentaPixels"] == 0, "near-magenta exists")

    # Part contract, dimensions, source pins and exterior-halo removal.
    required = {"id", "tier", "bayWidth", "reservedBayWidth", "useBay", "category", "realSizeM", "canvasPx", "anchorPx", "standPointX", "lightOverlays", "movingPartOverlays", "interactionAnchors", "bubbleOriginPx", "effectOriginPx", "statusLightPointPx", "faultRecipes", "palette", "styleReference", "sourceSha256", "files", "sha256"}
    for name, record in items["parts"].items():
        check(required <= record.keys(), f"metadata incomplete: {name}")
        path = PARTS / name
        image = Image.open(path).convert("RGBA")
        check(list(image.size) == record["canvasPx"], f"declared size mismatch: {name}")
        check(sha256(path) == record["sha256"], f"part hash mismatch: {name}")
        check(record["styleReference"]["sha256"] == V7_SHA, f"style pin mismatch: {name}")
        check(partial_alpha_confined_to_edge(image), f"detached partial-alpha halo/shadow: {name}")

    for name in ("worktop_tile.png", "plinth_tile.png", "front_drawers.png", "front_cupboard.png", "front_cupboard_2bay.png", "front_dishwasher.png"):
        image = Image.open(PARTS / name).convert("RGBA")
        check(image.getchannel("A").getextrema() == (255, 255), f"cut-out/gap in solid fitted component: {name}")
    check(Image.open(PARTS / "worktop_tile.png").size == (84, 31), "task-authority 84x31 worktop drift")
    check(manifest["checks"]["worktopRuns"] == [[496, 832], [916, 1336]], "run endpoints drift")
    check(manifest["checks"]["worktopTopY"] == manifest["checks"]["cookerTopY"] == 305, "cooker/worktop top mismatch")
    check(manifest["checks"]["plinthY"] == manifest["checks"]["cookerPlinthY"] == [468, 485], "cooker/run plinth mismatch")
    check(manifest["checks"]["itemPixelsAboveWindowLimit"] == 0, "item crosses y274 window exclusion")

    # Independent reconstruction proves the declared item layer leaves both
    # window exclusions empty above the sill.
    builder = load_builder()
    part_images = {name: Image.open(PARTS / name).convert("RGBA") for name in items["parts"]}
    rebuilt, item_layer = builder.assemble(part_images)
    check(rebuilt.tobytes() == room.tobytes(), "room is not deterministic code assembly")
    for x0, _, x1, _ in manifest["geometry"]["windows"]:
        for y in range(274):
            for x in range(x0, x1):
                check(item_layer.getpixel((x, y))[3] == 0, f"item/window collision at {x},{y}")

    # Overlay alpha and actual composite differences stay within declarations.
    overlay_bases = {"overlay_oven_window.png": "cooker.png", "overlay_dishwasher_led.png": "front_dishwasher.png"}
    for overlay_name, base_name in overlay_bases.items():
        overlay = Image.open(PARTS / overlay_name).convert("RGBA")
        base = Image.open(PARTS / base_name).convert("RGBA")
        allowed = manifest["checks"]["overlayRects"][overlay_name]
        bbox = inclusive_bbox(overlay)
        check(bbox and bbox[0] >= allowed[0] and bbox[1] >= allowed[1] and bbox[2] <= allowed[2] and bbox[3] <= allowed[3], f"overlay alpha escapes: {overlay_name}")
        lit = base.copy(); lit.alpha_composite(overlay)
        diff = ImageChops.difference(base, lit)
        db = inclusive_bbox(diff, alpha=False)
        check(db and db[0] >= allowed[0] and db[1] >= allowed[1] and db[2] <= allowed[2] and db[3] <= allowed[3], f"overlay composite escapes: {overlay_name}")

    # Prime cells remain exact and are composited 1:1 on the sole datum.
    keeper = Image.open(SOURCES / "keeper_prime_master-neutral-standing-back_f1.png").convert("RGBA")
    check(keeper.size == (256, 320), "Prime cell size changed")
    for label, root_x in (("fridge", 454), ("sink", 622), ("cooker", 874)):
        expected = room.copy(); expected.alpha_composite(keeper, (root_x - 128, 502 - 316))
        actual = Image.open(OUTPUTS / f"keeper_check_{label}.png").convert("RGBA")
        check(expected.tobytes() == actual.tobytes(), f"Prime composite changed/scaled: {label}")

    isolation = manifest["checks"]["isolation"]
    check(isolation["changedLocalTapPixels"] == isolation["roomDiffPixels"] > 0, "isolation cardinality mismatch")
    x0, y0, x1, y1 = isolation["roomDiffBoundsInclusive"]
    ax0, ay0, ax1, ay1 = isolation["allowedBoundsInclusive"]
    check(x0 >= ax0 and y0 >= ay0 and x1 <= ax1 and y1 <= ay1, "sink isolation escaped insert rectangle")
    check(isolation["allStoredPartHashesUnchanged"], "isolation mutated stored art")

    print("PASS: Kitchen V3 modular rebuild")
    print(f"  {len(items['parts'])} item/component parts plus one shell with exact dimensions and source pins")
    print(f"  {exact} exact-magenta pixels; 0 near-magenta; 0 item/window collisions")
    print("  no detached partial-alpha halos; solid run components contain no cut-outs")
    print("  Prime Keeper: exact 256x320 source, native 1:1 at x454/x622/x874")
    print(f"  sink isolation: {isolation['roomDiffPixels']} pixels, confined to {isolation['roomDiffBoundsInclusive']}")


if __name__ == "__main__":
    main()
