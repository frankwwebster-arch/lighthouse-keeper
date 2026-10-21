#!/usr/bin/env python3
"""Read-only verification for the ligne-claire feasibility pack."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageSequence


ROOT = Path(__file__).resolve().parents[3]
PACK = Path(__file__).resolve().parent
CELL = (256, 320)
FRAME_COUNT = 8


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_alpha_count(image: Image.Image) -> int:
    a = np.asarray(image.convert("RGBA").getchannel("A"), dtype=np.uint8)
    return int(np.count_nonzero(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])))


def main() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    metrics = json.loads((PACK / "evidence/dimensional-verification.json").read_text())
    failures: list[str] = []

    if register["status"] != "FEASIBILITY TEST — NOT APPROVED PRODUCTION ART":
        failures.append("register status is not fail-safe review-only wording")

    for authority in register["authorities"]:
        path = ROOT / authority["file"]
        if not path.exists() or sha(path) != authority["sha256"]:
            failures.append(f"authority hash mismatch: {authority['file']}")

    original_paths = [ROOT / record["source"] for record in metrics["walk"]]
    test_paths = [ROOT / record["test"] for record in metrics["walk"]]
    strip_path = PACK / "walk/keeper-prime-ligne-claire-walk-right-f8.png"
    strip = Image.open(strip_path).convert("RGBA")
    if strip.size != (CELL[0] * FRAME_COUNT, CELL[1]):
        failures.append(f"strip geometry is {strip.size}")

    for i, (original_path, test_path) in enumerate(zip(original_paths, test_paths), start=1):
        original = Image.open(original_path).convert("RGBA")
        test = Image.open(test_path).convert("RGBA")
        if original.size != CELL or test.size != CELL:
            failures.append(f"frame {i}: cell geometry mismatch")
        if original.getchannel("A").tobytes() != test.getchannel("A").tobytes():
            failures.append(f"frame {i}: alpha differs from authority")
        if edge_alpha_count(test):
            failures.append(f"frame {i}: opaque/shared cell edge")
        if strip.crop(((i - 1) * CELL[0], 0, i * CELL[0], CELL[1])).tobytes() != test.tobytes():
            failures.append(f"frame {i}: strip slice differs from individual frame")

    static_record = metrics["static"]
    static_original = Image.open(ROOT / static_record["source"]).convert("RGBA")
    static_test = Image.open(ROOT / static_record["test"]).convert("RGBA")
    if static_original.getchannel("A").tobytes() != static_test.getchannel("A").tobytes():
        failures.append("static: alpha differs from authority")
    if edge_alpha_count(static_test):
        failures.append("static: opaque cell edge")

    for preview_name in ("keeper-prime-ligne-claire-walk-preview.gif", "keeper-prime-ligne-claire-walk-preview.webp"):
        preview = Image.open(PACK / "walk" / preview_name)
        preview_frames = [frame.copy() for frame in ImageSequence.Iterator(preview)]
        if len(preview_frames) != FRAME_COUNT:
            failures.append(f"{preview_name}: expected 8 frames, got {len(preview_frames)}")
        if any(frame.size != CELL for frame in preview_frames):
            failures.append(f"{preview_name}: frame geometry mismatch")

    for output in register["outputs"]:
        path = ROOT / output["file"]
        if not path.exists() or sha(path) != output["sha256"]:
            failures.append(f"output hash mismatch: {output['file']}")

    if failures:
        raise SystemExit("FAIL\n- " + "\n- ".join(failures))
    print("PASS: 1 static cell and 8 walk cells preserve exact authority alpha, geometry, registration, gutters, strip assembly, preview counts, and recorded hashes.")


if __name__ == "__main__":
    main()
