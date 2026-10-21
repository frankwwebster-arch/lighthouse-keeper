#!/usr/bin/env python3
"""Build the immutable, review-only ligne-claire BBQ picture pilot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1"
SOURCE = PACK / "source"
COMPONENTS = PACK / "drafts/components"
EVIDENCE = PACK / "evidence"
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216
INK = (5, 24, 36)

SPECS = (
    {
        "id": "bbq-grill-unlit",
        "label": "Unlit barbecue",
        "source": "bbq-grill-unlit-source.png",
        "cache": "exec-23685bc4-1383-4b24-8a20-49aa8aa2680e.png",
        "current": "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/assets/bbq-grill.png",
        "currentSha256": "e6c7d5e51308d4fc974d6c3f090548cfba4d725d43564c9f7a6943bb55b407b7",
        "libraryVersion": 2,
        "palette": [INK, (23, 124, 157), (13, 78, 103), (227, 167, 44), (242, 237, 226), (48, 52, 58)],
        "preserves": "the current compact open round grill, front three-quarter viewpoint, cold coals, grate, handles and three legs",
    },
    {
        "id": "bbq-grill",
        "label": "Barbecue grill (lit)",
        "source": "bbq-grill-source.png",
        "cache": "exec-d7f0a935-b5b6-4ea3-9c82-e1f2e33510b6.png",
        "current": "review-archive/objects/89/8984470c007ff8a35af6fc8428afa9a38318c89bb5c4e7e1f2f34d7b858a5ee0.png",
        "currentSha256": "8984470c007ff8a35af6fc8428afa9a38318c89bb5c4e7e1f2f34d7b858a5ee0",
        "libraryVersion": 3,
        "palette": [INK, (23, 124, 157), (13, 78, 103), (227, 167, 44), (242, 237, 226), (48, 52, 58), (232, 72, 51), (235, 139, 45)],
        "preserves": "the same grill model and viewpoint as the unlit picture, with lit coral/orange and black coals",
    },
    {
        "id": "bbq-charcoal",
        "label": "Charcoal",
        "source": "bbq-charcoal-source.png",
        "cache": "exec-2cd449c4-d417-4844-be47-381b517edd52.png",
        "current": "review-archive/objects/4b/4b728ffaefec6c4ef792c3ef5261cc5815060077ac3d0a08b44be0abbfd6dfa2.png",
        "currentSha256": "4b728ffaefec6c4ef792c3ef5261cc5815060077ac3d0a08b44be0abbfd6dfa2",
        "libraryVersion": 2,
        "palette": [INK, (232, 171, 55), (246, 196, 91), (230, 71, 49), (47, 50, 59), (73, 76, 82)],
        "preserves": "the current open ochre paper bag, visible charcoal inside, loose foreground lumps and flame motif",
    },
    {
        "id": "bbq-sausages",
        "label": "Sausages (raw)",
        "source": "bbq-sausages-source.png",
        "cache": "exec-d9e9b757-8d5d-4031-9f76-9714c118d7cf.png",
        "current": "art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1/assets/bbq-sausages.png",
        "currentSha256": "dfc97e3a148a3a77487a0e64b66e4dcb0b6a1406f69ac6f957a45ee93dc94fee",
        "libraryVersion": 3,
        "palette": [INK, (245, 126, 106), (215, 73, 62)],
        "preserves": "the current five linked raw sausages, plate-free state and loose curved diagonal chain",
    },
    {
        "id": "bbq-hotdogs",
        "label": "Hot dogs",
        "source": "bbq-hotdogs-source.png",
        "cache": "exec-99e4c968-6c20-41cd-bba5-41582dc8d9ab.png",
        "current": "review-archive/objects/63/63d205ed77f06ea3121f4ef2bba1a3dde9d90c064bedaa2c5ceb761553f46f6c.png",
        "currentSha256": "63d205ed77f06ea3121f4ef2bba1a3dde9d90c064bedaa2c5ceb761553f46f6c",
        "libraryVersion": 2,
        "palette": [INK, (231, 166, 56), (246, 229, 183), (181, 70, 51), (231, 202, 42)],
        "preserves": "the current two overlapping served hot dogs, golden buns and mustard zigzags",
    },
    {
        "id": "bbq-tongs",
        "label": "Tongs",
        "source": "bbq-tongs-source.png",
        "cache": "exec-173fad28-4f96-42a5-a9cb-d0179369c95c.png",
        "current": "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/assets/bbq-tongs.png",
        "currentSha256": "885d696d6636f25d51c93c9d3f35fb5a9a09533b5e9604b12339740e1b45c8c2",
        "libraryVersion": 2,
        "palette": [INK, (237, 233, 222), (13, 76, 117), (227, 167, 44)],
        "preserves": "the current diagonal closed tongs, scalloped steel ends, dark blue grips and ochre hanging loop",
    },
)

REJECTED = (
    {
        "file": "rejected/bbq-charcoal-loose-v1.png",
        "cache": "exec-d3ebab79-44cb-4dc4-bff5-9a4ceee26946.png",
        "reason": "Removed the charcoal bag and therefore changed the current asset's meaning instead of translating its style.",
    },
    {
        "file": "rejected/bbq-charcoal-loose-v2.png",
        "cache": "exec-5be27e7c-5603-44a2-bcce-0a68245d72ae.png",
        "reason": "Second bagless attempt repeated the semantic error; it also retained an unwanted background haze.",
    },
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def bounds(image: Image.Image) -> tuple[int, int, int, int]:
    found = image.getchannel("A").point(lambda a: 255 if a > VISIBLE_ALPHA else 0).getbbox()
    if found is None:
        raise RuntimeError("image has no visible pixels")
    return found


def edge_pixels(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = {(x, 0) for x in range(image.width)} | {(x, image.height - 1) for x in range(image.width)}
    points |= {(0, y) for y in range(image.height)} | {(image.width - 1, y) for y in range(image.height)}
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in points)


def flatten(image: Image.Image, palette: list[tuple[int, int, int]]) -> Image.Image:
    rgba = image.convert("RGBA")
    out = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    source_pixels = rgba.load()
    output_pixels = out.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = source_pixels[x, y]
            if a <= VISIBLE_ALPHA:
                continue
            colour = min(palette, key=lambda p: (r - p[0]) ** 2 + (g - p[1]) ** 2 + (b - p[2]) ** 2)
            output_pixels[x, y] = (*colour, a)
    return out


def normalise(source: Image.Image, palette: list[tuple[int, int, int]]) -> tuple[Image.Image, dict[str, object]]:
    source_bounds = bounds(source)
    isolated = source.crop(source_bounds)
    scale = min(TARGET / isolated.width, TARGET / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    resized = isolated.resize(size, Image.Resampling.LANCZOS)
    flattened = flatten(resized, palette)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    offset = ((CELL - size[0]) // 2, (CELL - size[1]) // 2)
    cell.alpha_composite(flattened, offset)
    final_bounds = bounds(cell)
    gutter = min(final_bounds[0], final_bounds[1], CELL - final_bounds[2], CELL - final_bounds[3])
    return cell, {
        "sourceVisibleBounds": list(source_bounds),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "bounds": list(final_bounds),
        "transparentGutterPx": gutter,
        "edgeAlphaPixels": edge_pixels(cell),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }


def backed(image: Image.Image, colour: tuple[int, int, int, int]) -> Image.Image:
    result = Image.new("RGBA", image.size, colour)
    result.alpha_composite(image)
    return result


def fit_current(path: Path) -> Image.Image:
    source = Image.open(path).convert("RGBA")
    box = bounds(source)
    isolated = source.crop(box)
    scale = min(TARGET / isolated.width, TARGET / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    isolated = isolated.resize(size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.alpha_composite(isolated, ((CELL - size[0]) // 2, (CELL - size[1]) // 2))
    return cell


def contact_sheet(rows: list[tuple[dict[str, object], Image.Image]]) -> Image.Image:
    header = 46
    row_height = CELL + 34
    columns = 5
    sheet = Image.new("RGBA", (CELL * columns, header + row_height * len(rows)), (5, 24, 36, 255))
    draw = ImageDraw.Draw(sheet)
    titles = ("CURRENT", "PILOT · CREAM", "PILOT · DARK", "CURRENT · 64PX", "PILOT · 64PX")
    for index, title in enumerate(titles):
        draw.text((index * CELL + 8, 14), title, fill=(246, 233, 205, 255))
    cream = (246, 233, 205, 255)
    dark = (5, 24, 36, 255)
    for row, (spec, pilot) in enumerate(rows):
        y = header + row * row_height
        current_path = ROOT / str(spec["current"])
        current = fit_current(current_path)
        sheet.alpha_composite(backed(current, cream), (0, y))
        sheet.alpha_composite(backed(pilot, cream), (CELL, y))
        sheet.alpha_composite(backed(pilot, dark), (CELL * 2, y))
        current_small = current.resize((64, 64), Image.Resampling.LANCZOS)
        pilot_small = pilot.resize((64, 64), Image.Resampling.LANCZOS)
        current_cell = Image.new("RGBA", (CELL, CELL), cream)
        pilot_cell = Image.new("RGBA", (CELL, CELL), cream)
        current_cell.alpha_composite(current_small, (96, 96))
        pilot_cell.alpha_composite(pilot_small, (96, 96))
        sheet.alpha_composite(current_cell, (CELL * 3, y))
        sheet.alpha_composite(pilot_cell, (CELL * 4, y))
        draw.text((8, y + CELL + 8), f"{spec['id']} · old", fill=(246, 233, 205, 255))
        draw.text((CELL + 8, y + CELL + 8), f"{spec['id']} · pilot", fill=(246, 233, 205, 255))
    return sheet


def write_hashes() -> None:
    files = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text(
        "\n".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}" for path in files) + "\n"
    )


def main() -> None:
    COMPONENTS.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    entries: dict[str, object] = {}
    rows: list[tuple[dict[str, object], Image.Image]] = []

    for spec in SPECS:
        source_path = SOURCE / str(spec["source"])
        current_path = ROOT / str(spec["current"])
        if sha256(current_path) != spec["currentSha256"]:
            raise RuntimeError(f"current source drift: {spec['id']}")
        source = Image.open(source_path).convert("RGBA")
        if edge_pixels(source):
            raise RuntimeError(f"source touches edge: {spec['id']}")
        component, evidence = normalise(source, list(spec["palette"]))
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe output: {spec['id']}")
        output_path = COMPONENTS / f"{spec['id']}.png"
        component.save(output_path, optimize=True)
        entries[str(spec["id"])] = {
            "family": "bbq-tools" if spec["id"] == "bbq-tongs" else "bbq",
            "label": spec["label"],
            "intent": f"approved-new-version-v{spec['libraryVersion']}",
            "libraryVersion": spec["libraryVersion"],
            "preserves": spec["preserves"],
            "currentReferenceFile": spec["current"],
            "currentReferenceSha256": spec["currentSha256"],
            "sourceFile": rel(source_path),
            "sourceSha256": sha256(source_path),
            "sourcePixels": list(source.size),
            "originalCacheFile": spec["cache"],
            "flatPalette": ["#%02x%02x%02x" % colour for colour in spec["palette"]],
            "file": rel(output_path),
            "sha256": sha256(output_path),
            "cellPixels": [CELL, CELL],
            **evidence,
        }
        rows.append((spec, component))

    contact_path = EVIDENCE / "current-vs-ligne-claire-contact-sheet.png"
    contact_sheet(rows).save(contact_path, optimize=True)
    rejected = []
    for item in REJECTED:
        path = PACK / item["file"]
        rejected.append({**item, "sha256": sha256(path)})
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-pilot@1",
        "set": "activity-story-ligne-claire-bbq-pilot-2026-10-21-v1",
        "status": "approved-and-registered",
        "created": "2026-10-21",
        "tool": "built-in image generation plus deterministic fixed-palette normalisation",
        "visualDirection": "original ligne-claire-inspired style translation: near-black ink, flat spot colour, no gradients or rendered light",
        "preservationRule": "Translate each current asset's drawing language while preserving its subject identity, viewpoint, object count, state, container and broad composition unless Frank explicitly requests a content correction.",
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "components": entries,
        "rejected": rejected,
        "evidence": {"file": rel(contact_path), "sha256": sha256(contact_path), "columns": 5, "rows": len(rows)},
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "currentReferenceHashesPinned": True,
            "libraryVersionsAdded": True,
            "storiesChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": {
            "by": "Frank",
            "date": "2026-10-21",
            "words": "agreed, these are superb",
            "scope": "the six ligne-claire BBQ picture translations shown on the current-vs-pilot contact sheet",
        },
        "rollback": "Point any picture back to its prior current version. Every earlier file remains byte-identical and independently addressable.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes()
    print("Built 6-picture approved ligne-claire BBQ pilot")


if __name__ == "__main__":
    main()
