#!/usr/bin/env python3
"""Verify the approved room-door cloud handoff without third-party packages."""

from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_geometry(path: Path) -> tuple[int, int, str]:
    with path.open("rb") as handle:
        signature = handle.read(8)
        length, kind = struct.unpack(">I4s", handle.read(8))
        payload = handle.read(length)
    if signature != b"\x89PNG\r\n\x1a\n" or kind != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    width, height, bit_depth, colour_type = struct.unpack(">IIBB", payload[:10])
    mode = {6: "RGBA"}.get(colour_type, f"PNG-colour-type-{colour_type}")
    if bit_depth != 8:
        mode += f"-{bit_depth}bit"
    return width, height, mode


manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
for relative, expected in manifest["files"].items():
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"missing: {relative}")
    if sha256(path) != expected["sha256"]:
        raise SystemExit(f"hash mismatch: {relative}")
    if path.suffix.lower() == ".png":
        actual = png_geometry(path)
        wanted = (expected["width"], expected["height"], expected["mode"])
        if actual != wanted:
            raise SystemExit(f"PNG geometry mismatch: {relative}: {actual} != {wanted}")

print(f"OK: {len(manifest['files'])} immutable files verified")
