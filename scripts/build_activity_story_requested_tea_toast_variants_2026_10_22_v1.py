#!/usr/bin/env python3
"""Build and verify Frank's empty-mug V1 and mark-free toast-slices V3."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACK = ROOT / "art/drafts/activity-story-ligne-claire-tea-toast-2026-10-22-v1"
MUG_PACK = ROOT / "art/drafts/activity-story-ligne-claire-tea-mug-empty-2026-10-22-v1"
TOAST_PACK = ROOT / "art/drafts/activity-story-ligne-claire-toast-slices-no-slashes-2026-10-22-v1"
MUG_SOURCE = SOURCE_PACK / "drafts/components/tea-mug.png"
TOAST_SOURCE = SOURCE_PACK / "drafts/components/toast-slices.png"
MUG_OUTPUT = MUG_PACK / "drafts/components/tea-mug-empty.png"
TOAST_OUTPUT = TOAST_PACK / "drafts/components/toast-slices.png"
CELL = 256
VISIBLE_ALPHA = 8
INK = (5, 24, 36)
CREAM = (246, 229, 183)
BROWN = (166, 95, 42)
CREAM_BACK = (247, 236, 204, 255)
DARK_BACK = (18, 34, 45, 255)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def bounds(image: Image.Image) -> list[int]:
    alpha = image.getchannel("A")
    box = alpha.point(lambda value: 255 if value > VISIBLE_ALPHA else 0).getbbox()
    if box is None:
        raise RuntimeError("image has no visible pixels")
    return list(box)


def gutter(image: Image.Image) -> int:
    left, top, right, bottom = bounds(image)
    return min(left, top, CELL - right, CELL - bottom)


def edge_alpha_pixels(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    pixels = alpha.load()
    return sum(
        pixels[x, y] > 0
        for x, y in (
            *((x, 0) for x in range(image.width)),
            *((x, image.height - 1) for x in range(image.width)),
            *((0, y) for y in range(1, image.height - 1)),
            *((image.width - 1, y) for y in range(1, image.height - 1)),
        )
    )


def backed(image: Image.Image, colour: tuple[int, int, int, int]) -> Image.Image:
    result = Image.new("RGBA", image.size, colour)
    result.alpha_composite(image)
    return result


def make_sheet(source: Image.Image, candidate: Image.Image, titles: tuple[str, str, str, str]) -> Image.Image:
    header = 42
    sheet = Image.new("RGBA", (CELL * 4, header + CELL), DARK_BACK)
    draw = ImageDraw.Draw(sheet)
    for index, title in enumerate(titles):
        draw.text((index * CELL + 8, 14), title, fill=CREAM_BACK)
    sheet.alpha_composite(backed(source, CREAM_BACK), (0, header))
    sheet.alpha_composite(backed(candidate, CREAM_BACK), (CELL, header))
    sheet.alpha_composite(backed(candidate, DARK_BACK), (CELL * 2, header))
    small = candidate.resize((64, 64), Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
    cell.alpha_composite(small, (96, 96))
    sheet.alpha_composite(cell, (CELL * 3, header))
    return sheet


def components(image: Image.Image) -> list[set[tuple[int, int]]]:
    pixels = image.load()
    seen: set[tuple[int, int]] = set()
    found: list[set[tuple[int, int]]] = []
    for y in range(image.height):
        for x in range(image.width):
            if (x, y) in seen or pixels[x, y][3] == 0:
                continue
            group = {(x, y)}
            stack = [(x, y)]
            seen.add((x, y))
            while stack:
                px, py = stack.pop()
                for nx, ny in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                    point = (nx, ny)
                    if (
                        0 <= nx < image.width
                        and 0 <= ny < image.height
                        and point not in seen
                        and pixels[nx, ny][3] > 0
                    ):
                        seen.add(point)
                        group.add(point)
                        stack.append(point)
            found.append(group)
    return sorted(found, key=len, reverse=True)


def library() -> dict[str, object]:
    return json.loads((ROOT / "data/activity-stories/pictures.json").read_text())["pictures"]


def write_hashes(pack: Path) -> None:
    rows = [
        f"{sha256(path)}  {path.relative_to(pack).as_posix()}"
        for path in sorted(pack.rglob("*"))
        if path.is_file() and path.name != "HASHES.sha256"
    ]
    (pack / "HASHES.sha256").write_text("\n".join(rows) + "\n")


def registered() -> bool:
    pictures = library()
    mug = pictures.get("tea-mug-empty")
    toast = pictures["toast-slices"]
    return bool(
        mug
        and mug["current"] == 1
        and len(mug["versions"]) == 1
        and mug["versions"][0]["sha256"] == sha256(MUG_OUTPUT)
        and toast["current"] == 3
        and len(toast["versions"]) == 3
        and toast["versions"][2]["sha256"] == sha256(TOAST_OUTPUT)
    )


def build() -> None:
    for pack in (MUG_PACK, TOAST_PACK):
        (pack / "drafts/components").mkdir(parents=True, exist_ok=True)
        (pack / "evidence").mkdir(parents=True, exist_ok=True)

    mug_source = Image.open(MUG_SOURCE).convert("RGBA")
    mug = mug_source.copy()
    mug_pixels = mug.load()
    mug_changes = 0
    for y in range(CELL):
        for x in range(CELL):
            red, green, blue, alpha = mug_pixels[x, y]
            if alpha > 0 and (red, green, blue) == BROWN:
                mug_pixels[x, y] = (*CREAM, alpha)
                mug_changes += 1
    mug.save(MUG_OUTPUT, optimize=True)
    mug_sheet = MUG_PACK / "evidence/filled-v2-vs-empty-v1-contact-sheet.png"
    make_sheet(mug_source, mug, ("FILLED MUG V2", "EMPTY V1 / CREAM", "EMPTY V1 / DARK", "EMPTY / 64PX")).save(mug_sheet, optimize=True)

    toast_source = Image.open(TOAST_SOURCE).convert("RGBA")
    groups = components(toast_source)
    if len(groups) != 6:
        raise RuntimeError(f"expected slices plus five detached marks, found {len(groups)} components")
    toast = toast_source.copy()
    toast_pixels = toast.load()
    removed_pixels = 0
    for group in groups[1:]:
        for x, y in group:
            toast_pixels[x, y] = (0, 0, 0, 0)
            removed_pixels += 1
    toast.save(TOAST_OUTPUT, optimize=True)
    toast_sheet = TOAST_PACK / "evidence/marked-v2-vs-clean-v3-contact-sheet.png"
    make_sheet(toast_source, toast, ("MARKED V2", "CLEAN V3 / CREAM", "CLEAN V3 / DARK", "CLEAN / 64PX")).save(toast_sheet, optimize=True)

    status = "approved-and-registered" if registered() else "frank-requested-ready-to-register"
    mug_manifest = {
        "schema": "lighthouse-keeper/activity-story-requested-variant@1",
        "set": "activity-story-ligne-claire-tea-mug-empty-2026-10-22-v1",
        "status": status,
        "created": "2026-10-22",
        "request": "Do a version of the mug without any contents in it.",
        "id": "tea-mug-empty",
        "version": 1,
        "source": {"file": rel(MUG_SOURCE), "sha256": sha256(MUG_SOURCE)},
        "candidate": {
            "file": rel(MUG_OUTPUT),
            "sha256": sha256(MUG_OUTPUT),
            "cell": [CELL, CELL],
            "bounds": bounds(mug),
            "gutter": gutter(mug),
            "changedPixels": mug_changes,
            "edit": "replace every visible flat tea-brown pixel #a65f2a with the existing enamel cream #f6e5b7; preserve every other RGBA byte",
        },
        "rejectedAttempt": {
            "file": rel(MUG_PACK / "rejected/tea-mug-empty-generated-gradient-v1.png"),
            "sha256": sha256(MUG_PACK / "rejected/tea-mug-empty-generated-gradient-v1.png"),
            "reason": "The generative edit redrew the mug and introduced tonal modelling, so it was retained only as rejected provenance.",
        },
        "evidence": {"file": rel(mug_sheet), "sha256": sha256(mug_sheet)},
        "behaviour": "new optional picture id; the filled tea-mug V2 and every existing story reference remain unchanged",
        "rollback": "Select or remove only tea-mug-empty V1; never overwrite the filled mug or this file.",
    }
    toast_manifest = {
        "schema": "lighthouse-keeper/activity-story-requested-variant@1",
        "set": "activity-story-ligne-claire-toast-slices-no-slashes-2026-10-22-v1",
        "status": status,
        "created": "2026-10-22",
        "request": "Remove the action slashes below the slices; those will all be separately added.",
        "id": "toast-slices",
        "version": 3,
        "source": {"file": rel(TOAST_SOURCE), "sha256": sha256(TOAST_SOURCE), "libraryVersion": 2},
        "candidate": {
            "file": rel(TOAST_OUTPUT),
            "sha256": sha256(TOAST_OUTPUT),
            "cell": [CELL, CELL],
            "bounds": bounds(toast),
            "gutter": gutter(toast),
            "removedComponents": 5,
            "removedPixels": removed_pixels,
            "edit": "retain the single connected two-slice object byte-for-byte and clear only the five detached mark components",
        },
        "evidence": {"file": rel(toast_sheet), "sha256": sha256(toast_sheet)},
        "behaviour": "same toast-slices id; immutable V3 becomes current while V1 and marked V2 remain available; marks are now separate animation-owned art",
        "rollback": "Select retained toast-slices V2 or V1; never overwrite any version.",
    }
    (MUG_PACK / "manifest.json").write_text(json.dumps(mug_manifest, indent=2) + "\n")
    (TOAST_PACK / "manifest.json").write_text(json.dumps(toast_manifest, indent=2) + "\n")
    write_hashes(MUG_PACK)
    write_hashes(TOAST_PACK)
    print(f"Built empty mug ({mug_changes} tea pixels removed) and clean toast ({removed_pixels} mark pixels removed).")


def verify_pack_hashes(pack: Path) -> None:
    expected = [
        f"{sha256(path)}  {path.relative_to(pack).as_posix()}"
        for path in sorted(pack.rglob("*"))
        if path.is_file() and path.name != "HASHES.sha256"
    ]
    if (pack / "HASHES.sha256").read_text().splitlines() != expected:
        raise RuntimeError(f"stale hashes: {pack.name}")


def verify() -> None:
    mug_source = Image.open(MUG_SOURCE).convert("RGBA")
    mug = Image.open(MUG_OUTPUT).convert("RGBA")
    toast_source = Image.open(TOAST_SOURCE).convert("RGBA")
    toast = Image.open(TOAST_OUTPUT).convert("RGBA")
    for image, name in ((mug, "empty mug"), (toast, "clean toast")):
        if image.size != (CELL, CELL) or image.mode != "RGBA" or edge_alpha_pixels(image) or gutter(image) < 20:
            raise RuntimeError(f"unsafe output: {name}")
    changed = []
    for before, after in zip(mug_source.get_flattened_data(), mug.get_flattened_data()):
        if before != after:
            changed.append((before, after))
    if not changed or any(a[:3] != BROWN or b[:3] != CREAM or a[3] != b[3] for a, b in changed):
        raise RuntimeError("empty mug changed pixels outside the flat tea fill")
    toast_groups = components(toast_source)
    retained = toast_groups[0]
    for y in range(CELL):
        for x in range(CELL):
            before = toast_source.getpixel((x, y))
            after = toast.getpixel((x, y))
            if (x, y) in retained:
                if after != before:
                    raise RuntimeError("clean toast changed the retained slice object")
            elif after != (0, 0, 0, 0):
                raise RuntimeError("clean toast retained a detached action mark pixel")
    if not registered():
        raise RuntimeError("requested variants are not the expected current immutable library versions")
    pictures = library()
    if pictures["tea-mug"]["current"] != 2 or pictures["tea-mug"]["versions"][1]["sha256"] != sha256(MUG_SOURCE):
        raise RuntimeError("filled tea mug V2 changed")
    if pictures["toast-slices"]["versions"][1]["sha256"] != sha256(TOAST_SOURCE):
        raise RuntimeError("marked toast V2 changed")
    for pack in (MUG_PACK, TOAST_PACK):
        manifest = json.loads((pack / "manifest.json").read_text())
        if manifest["status"] != "approved-and-registered":
            raise RuntimeError(f"incorrect final status: {pack.name}")
        verify_pack_hashes(pack)
    print("Verified requested variants: empty mug V1 and mark-free toast-slices V3; prior art and story behaviour preserved.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
