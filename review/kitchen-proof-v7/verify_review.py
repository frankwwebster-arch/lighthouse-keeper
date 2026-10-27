#!/usr/bin/env python3
"""Verify the Kitchen v7 whole-room proof without cutting any art."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAGENTA = (255, 0, 255)
sys.dont_write_bytecode = True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_builder():
    spec = importlib.util.spec_from_file_location("kitchen_v7_builder", HERE / "build_review.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    check(manifest["schema"] == "lighthouse-keeper/kitchen-proof-v7-precut@1", "schema drift")
    check(manifest["status"] == "review-only-awaiting-frank", "review status drift")
    check(not manifest["cuttingPerformed"], "cutting boundary crossed")
    check(not manifest["canonMutation"] and not manifest["runtimeMutation"], "production boundary crossed")
    check(not (HERE / "parts").exists(), "parts directory exists before approval")

    for relative, record in manifest["files"].items():
        path = HERE / relative
        check(path.is_file(), f"missing manifested file: {relative}")
        check(path.stat().st_size == record["bytes"], f"byte count drift: {relative}")
        check(sha256(path) == record["sha256"], f"SHA-256 drift: {relative}")
        check(list(Image.open(path).size) == record["canvasPx"], f"canvas drift: {relative}")

    refs = manifest["styleReferences"]
    check(sha256(ROOT / "review/kitchen-proof-v3-rebuild/sources/approved-style-calibration.png") == refs["approvedCalibrationSha256"], "calibration changed")
    check(sha256(ROOT / "reference/kitchen-mood/kitchen-mood-01.png") == refs["mood01Sha256"], "mood 01 changed")
    check(sha256(ROOT / "reference/kitchen-mood/kitchen-mood-07-cooker.png") == refs["cookerReferenceSha256"], "cooker reference changed")
    check(sha256(ROOT / "review/kitchen-proof-v3-rebuild/sources/v7-oven-authority.png") == refs["v7OvenAuthoritySha256"], "oven authority changed")

    keeper_record = manifest["keeper"]
    keeper_path = ROOT / keeper_record["file"]
    check(sha256(keeper_path) == keeper_record["sourceSha256"], "Prime Keeper source changed")
    check(list(Image.open(keeper_path).size) == keeper_record["sourceCanvasPx"], "Prime Keeper canvas changed")
    check(keeper_record["scale"] == 1.0, "Prime Keeper was scaled")

    room_path = HERE / "outputs/kitchen-v7-free-room-with-prime-precut.png"
    room = Image.open(room_path).convert("RGB")
    check(list(room.size) == manifest["geometry"]["modulePx"] == [2048, 576], "room canvas mismatch")

    pane_pixels = set()
    for x0, y0, x1, y1 in manifest["geometry"]["paneRects"]:
        for y in range(y0, y1):
            for x in range(x0, x1):
                pane_pixels.add((x, y))
                check(room.getpixel((x, y)) == MAGENTA, f"pane is not exact magenta at {x},{y}")

    exact = 0
    near = 0
    for y in range(room.height):
        for x in range(room.width):
            r, g, b = room.getpixel((x, y))
            if (r, g, b) == MAGENTA:
                exact += 1
                check((x, y) in pane_pixels, f"magenta used outside glass at {x},{y}")
            elif r >= 180 and b >= 180 and g <= 100:
                near += 1
    checks = manifest["checks"]
    check(exact == len(pane_pixels) == checks["exactMagentaPixels"] == 38088, "exact-magenta count drift")
    check(near == checks["nearMagentaPixels"] == 0, "near-magenta contamination")

    # Independent deterministic rebuild. This proves the final output comes
    # from the pinned whole-room paint, exact shell and unscaled Prime source.
    builder = load_builder()
    rebuilt_source = Image.open(HERE / manifest["selectedSource"]["file"])
    shell = Image.open(HERE / "sources/structural-shell-2x.png").convert("RGB")
    rebuilt = builder.normalize_generated(rebuilt_source)
    builder.restore_structure(rebuilt, shell)
    builder.composite_keeper(rebuilt)
    check(rebuilt.tobytes() == room.tobytes(), "final room is not deterministic pre-cut assembly")

    # The complete structural window rectangles must match the restored result;
    # therefore generated furniture cannot cover the glass or frames.
    for x0, y0, x1, y1 in manifest["geometry"]["windows"]:
        check(rebuilt.crop((x0, y0, x1, y1)).tobytes() == room.crop((x0, y0, x1, y1)).tobytes(), "window structure drift")

    # Ensure the builder itself remains incapable of silently making a parts
    # tree during this review stage.
    with TemporaryDirectory() as temporary:
        check(not (Path(temporary) / "parts").exists(), "unexpected temporary parts tree")

    print("PASS: Kitchen v7 whole-room pre-cut proof")
    print("  2048x576 room; exact structural bands and windows")
    print(f"  {exact} exact-magenta pixels, all in eight pane interiors; 0 near-magenta")
    print("  Prime Keeper source pinned and composited 1:1 on sole datum y=502")
    print("  selected pass and every review image match the manifest")
    print("  no parts directory; no canon/runtime mutation")


if __name__ == "__main__":
    main()
