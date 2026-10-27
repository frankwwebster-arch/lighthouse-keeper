#!/usr/bin/env python3
"""Acceptance checks for the Kitchen v8 Step-1 style test only."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_builder():
    spec = importlib.util.spec_from_file_location("kitchen_v8_style_builder", HERE / "build_style_test.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def edge_alpha_is_zero(image: Image.Image) -> bool:
    alpha = image.getchannel("A")
    edges = [
        alpha.crop((0, 0, image.width, 2)),
        alpha.crop((0, image.height - 2, image.width, image.height)),
        alpha.crop((0, 0, 2, image.height)),
        alpha.crop((image.width - 2, 0, image.width, image.height)),
    ]
    return all(edge.getextrema() == (0, 0) for edge in edges)


def main() -> None:
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    check(manifest["schema"] == "lighthouse-keeper/kitchen-v8-style-test@1", "schema drift")
    check(manifest["status"] == "review-only-awaiting-frank", "approval status drift")
    check(manifest["stepCompleted"] == 1 and not manifest["step2Started"], "Step 2 boundary crossed")
    check(not manifest["runtimeMutation"] and not manifest["canonMutation"], "production boundary crossed")
    check(not (HERE / "parts").exists(), "production parts directory exists")

    authority = ROOT / manifest["styleAuthority"]["file"]
    prime = ROOT / manifest["primeKeeper"]["file"]
    check(sha256(authority) == manifest["styleAuthority"]["sha256"], "V7 authority changed")
    check(sha256(prime) == manifest["primeKeeper"]["sha256"], "Prime Keeper changed")
    check(Image.open(prime).size == (256, 320) and manifest["primeKeeper"]["scale"] == 1.0, "Prime 1:1 contract drift")

    for record in manifest["selectedSources"].values():
        path = HERE / record["file"]
        check(path.stat().st_size == record["bytes"], f"selected-source byte drift: {path.name}")
        check(sha256(path) == record["sha256"], f"selected-source hash drift: {path.name}")

    builder = load_builder()
    selected = manifest["selectedSources"]
    regenerated = {
        "outputs/belfast_sink_cabinet-1x.png": builder.prepare_asset(HERE / selected["belfast_sink_cabinet"]["file"], (168, 211)),
        "outputs/painted_dresser-1x.png": builder.prepare_asset(HERE / selected["painted_dresser"]["file"], (150, 355)),
        "outputs/small_cream_cooker-1x.png": builder.prepare_asset(HERE / selected["small_cream_cooker"]["file"], (101, 180)),
    }

    exact_magenta = 0
    near_magenta = 0
    for relative, record in manifest["reviewCanvases"].items():
        path = HERE / relative
        check(path.is_file(), f"missing review output: {relative}")
        check(path.stat().st_size == record["bytes"], f"output byte drift: {relative}")
        check(sha256(path) == record["sha256"], f"output hash drift: {relative}")
        check(list(Image.open(path).size) == record["canvasPx"], f"output canvas drift: {relative}")

    for relative, expected in regenerated.items():
        actual = Image.open(HERE / relative).convert("RGBA")
        check(actual.tobytes() == expected.tobytes(), f"non-deterministic 1:1 reduction: {relative}")
        check(edge_alpha_is_zero(actual), f"two-pixel transparent gutter missing: {relative}")
        for y in range(actual.height):
            for x in range(actual.width):
                r, g, b, a = actual.getpixel((x, y))
                if a and (r, g, b) == (255, 0, 255):
                    exact_magenta += 1
                elif a and r >= 180 and b >= 180 and g <= 100:
                    near_magenta += 1

    checks = manifest["checks"]
    check(exact_magenta == checks["exactMagentaPixelsInNewPieces"] == 0, "magenta used in candidate pieces")
    check(near_magenta == checks["nearMagentaPixelsInNewPieces"] == 0, "near-magenta used in candidate pieces")
    check(checks["threeScaleReview"] and checks["reviewScales"] == [2.0, 1.0, 0.125], "three-scale gate missing")
    check(checks["currentSage"] == "#96B0A5" and checks["proposedDuckEgg"] == "#A8CEC6", "colour-choice swatches drifted")
    check(checks["cookerKnobs"] == 4, "manual cooker knob review not recorded")
    check(checks["cookerStatusBezel"] == "single-indicator-dark-unlit-engine-status-lamp", "single cooker status indicator contract drifted")
    check(checks["cookerWorkingLight"] == "steady-green" and checks["cookerBrokenLight"] == "flashing-red", "cooker engine-light states drifted")
    check(not checks["secondCookerStatusLamp"], "second cooker status lamp introduced")
    check(not checks["fullRoomBuilt"] and not checks["itemsPromoted"], "Step 1 scope exceeded")

    print("PASS: Kitchen v8 UK Cottage Step-1 style test")
    print("  three candidate canvases at declared 1:1 game envelopes")
    print("  V7 authority and exact Prime source hash-pinned")
    print("  three-scale review present at 2x, 1:1 and 1/8 with colour swatches")
    print("  cooker has one indicator/status bezel; no second status lamp")
    print("  two-pixel transparent edge gutters; zero magenta/near-magenta")
    print("  Step 2 not started; no room, production parts, runtime or canon mutation")


if __name__ == "__main__":
    main()
