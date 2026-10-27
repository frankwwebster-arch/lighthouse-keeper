#!/usr/bin/env python3
"""Acceptance checks for the reversible Kitchen v8 cooker correction v2."""

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
    spec = importlib.util.spec_from_file_location("kitchen_v8_style_builder_v2", HERE / "build_style_test.py")
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
    check(manifest["schema"] == "lighthouse-keeper/kitchen-v8-style-test@2", "schema drift")
    check(manifest["status"] == "review-only-frank-endorsed-source", "review status drift")
    check(not manifest["fullRoomBuilt"], "full room crossed the v2 boundary")
    check(not manifest["runtimeMutation"] and not manifest["canonMutation"], "production boundary crossed")

    for key in ("predecessor", "styleAuthority", "subjectReference", "primeKeeper"):
        record = manifest[key]
        path = ROOT / record["file"]
        check(path.is_file(), f"missing pinned reference: {record['file']}")
        check(sha256(path) == record["sha256"], f"pinned reference drift: {record['file']}")

    prime = ROOT / manifest["primeKeeper"]["file"]
    check(Image.open(prime).size == (256, 320) and manifest["primeKeeper"]["scale"] == 1.0, "Prime Keeper contract drift")

    for record in manifest["selectedSources"].values():
        path = HERE / record["file"]
        check(path.stat().st_size == record["bytes"], f"source byte drift: {path.name}")
        check(sha256(path) == record["sha256"], f"source hash drift: {path.name}")

    for relative, record in manifest["reviewCanvases"].items():
        path = HERE / relative
        check(path.is_file(), f"missing output: {relative}")
        check(path.stat().st_size == record["bytes"], f"output byte drift: {relative}")
        check(sha256(path) == record["sha256"], f"output hash drift: {relative}")
        check(list(Image.open(path).size) == record["canvasPx"], f"output canvas drift: {relative}")

    builder = load_builder()
    expected = {
        "belfast_sink_cabinet": (168, 211),
        "painted_dresser": (150, 355),
        "old_school_cooker": (126, 252),
    }
    output_names = {
        "belfast_sink_cabinet": "belfast_sink_cabinet-1x.png",
        "painted_dresser": "painted_dresser-1x.png",
        "old_school_cooker": "small_cream_cooker-1x.png",
    }
    exact_magenta = 0
    near_magenta = 0
    for key, size in expected.items():
        source = HERE / manifest["selectedSources"][key]["file"]
        regenerated = builder.prepare_asset(source, size)
        actual = Image.open(HERE / "outputs" / output_names[key]).convert("RGBA")
        check(actual.tobytes() == regenerated.tobytes(), f"non-deterministic reduction: {key}")
        check(edge_alpha_is_zero(actual), f"missing two-pixel transparent gutter: {key}")
        rgba = iter(actual.tobytes())
        for r, g, b, a in zip(rgba, rgba, rgba, rgba):
            if a and (r, g, b) == (255, 0, 255):
                exact_magenta += 1
            elif a and r >= 180 and b >= 180 and g <= 100:
                near_magenta += 1

    checks = manifest["checks"]
    check(exact_magenta == checks["exactMagentaPixelsInNewPieces"] == 0, "exact magenta introduced")
    check(near_magenta == checks["nearMagentaPixelsInNewPieces"] == 0, "near magenta introduced")
    check(checks["standardUnitWidthPx"] == 126 and checks["cookerCanvasPx"] == [126, 252], "single-unit cooker boundary drift")
    check(checks["cookerKnobs"] == 4 and checks["eyeLevelHoodAndGrill"], "old-school cooker contract drift")
    check(checks["futureRangeWidthPx"] == 252 and not checks["futureRangeDrawn"], "deferred two-unit range contract drift")
    check(checks["reviewScales"] == [2.0, 1.0, 0.125], "three-scale review drift")
    check(not checks["itemsPromoted"], "candidate promoted without approval")

    print("PASS: Kitchen v8 cooker correction v2")
    print("  cooker is one 126 px standard unit with eye-level hood/grill and four controls")
    print("  future range is fixed at 252 px and is not drawn")
    print("  predecessor, subject reference, style authority and Prime Keeper are hash-pinned")
    print("  deterministic 1:1 reductions, transparent gutters and zero magenta")


if __name__ == "__main__":
    main()
