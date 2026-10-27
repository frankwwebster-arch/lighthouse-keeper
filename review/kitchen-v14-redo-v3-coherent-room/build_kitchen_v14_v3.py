#!/usr/bin/env python3
"""Build the Kitchen v14 V3 review from one coherent room-wide painting.

The room artwork is never redrawn in code. This builder only uniformly scales,
crops, masks, places approved painted references, assembles, annotates review
sheets and writes hashes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sources/imagegen"
REF = ROOT / "sources/reference"
OUT = ROOT / "outputs"
RESAMPLE = Image.Resampling.LANCZOS
PAPER = (245, 240, 221, 255)
MUTED = (171, 191, 194, 255)


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def save(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def fit_contain(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("empty alpha")
    im = im.crop(bbox)
    scale = min(size[0] / im.width, size[1] / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), RESAMPLE)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return canvas


def register_prime() -> Image.Image:
    # Exact crop/registration used by the verified V1/V2 candidates.
    source = rgba(REF / "keeper-prime-2x.png").crop((77, 18, 179, 316))
    return fit_contain(source, (120, 298))


def build_room() -> tuple[Image.Image, Image.Image, Image.Image]:
    raw = rgba(SRC / "kitchen-v14-coherent-room-no-keeper.png")
    if raw.size != (2172, 724):
        raise AssertionError(f"unexpected room-wide source size: {raw.size}")

    # Uniform reduction preserves the painting; the vertical crop maps the
    # furniture feet to the approved y=485 datum without distortion.
    scaled = raw.resize((2048, 683), RESAMPLE)
    empty = scaled.crop((0, 68, 2048, 644))
    shell = rgba(REF / "kitchen-v8-room-shell-empty-1x.png")
    if shell.size != (2048, 576):
        raise AssertionError(shell.size)

    # Recolour only the generated technical-magenta glass pixels. This is a
    # permitted mask recolour, not code-drawn artwork.
    pixels = []
    for r, g, b, a in empty.get_flattened_data():
        pixels.append((255, 0, 255, a) if a and r > 190 and b > 140 and g < 80 else (r, g, b, a))
    empty.putdata(pixels)

    # Keep the room-wide painting intact edge-to-edge. Only the frozen ceiling
    # and floor-slab boundary bands come from the approved shell.
    empty.alpha_composite(shell.crop((0, 0, 2048, 32)), (0, 0))
    empty.alpha_composite(shell.crop((0, 544, 2048, 576)), (0, 544))

    prime = register_prime()
    room = empty.copy()
    room.alpha_composite(prime, (1150, 204))
    return empty, room, prime


def card(sheet: Image.Image, im: Image.Image, xy: tuple[int, int], title: str, subtitle: str = "") -> None:
    x, y = xy
    d = ImageDraw.Draw(sheet)
    d.rounded_rectangle((x - 10, y - 48, x + im.width + 10, y + im.height + 42), radius=10, fill=(33, 46, 55, 255), outline=(87, 108, 113, 255), width=2)
    sheet.alpha_composite(im, (x, y))
    d.text((x, y - 38), title, font=font(22, True), fill=PAPER)
    if subtitle:
        d.text((x, y + im.height + 10), subtitle, font=font(16), fill=MUTED)


def two_scales(room: Image.Image) -> Image.Image:
    sheet = Image.new("RGBA", (2300, 980), (17, 27, 34, 255))
    d = ImageDraw.Draw(sheet)
    d.text((44, 28), "KITCHEN v14 V3 · ONE COHERENT ROOM · TWO VIEWING SCALES", font=font(34, True), fill=PAPER)
    d.text((44, 74), "One room-wide generated painting · exact registered module · review only", font=font(20), fill=MUTED)
    card(sheet, room, (120, 160), "ROOM VIEW · exact 1:1 · 2048 × 576")
    small = room.resize((256, 72), RESAMPLE)
    card(sheet, small, (1022, 830), "LIGHTHOUSE VIEW · exact 12.5% · 256 × 72", "The continuous sage-and-pine kitchen family remains one readable band.")
    return sheet


def continuity_comparison(room: Image.Image) -> Image.Image:
    old = rgba(REF / "kitchen-v14-redo-v2-rejected-room-1x.png")
    sheet = Image.new("RGBA", (4300, 900), (17, 27, 34, 255))
    d = ImageDraw.Draw(sheet)
    d.text((46, 26), "KITCHEN v14 · CONTINUITY CORRECTION", font=font(38, True), fill=PAPER)
    d.text((46, 78), "V2 is rejected: separately generated assets. V3 is authored as one complete room-wide painting.", font=font(21), fill=MUTED)
    card(sheet, old, (70, 160), "V2 · REJECTED · separate-asset appearance")
    card(sheet, room, (2180, 160), "V3 · COHERENT ROOM-WIDE PAINTING")
    return sheet


def v8_comparison(room: Image.Image) -> Image.Image:
    v8 = rgba(REF / "kitchen-v8-room-furnished-1x.png")
    sheet = Image.new("RGBA", (4300, 900), (17, 27, 34, 255))
    d = ImageDraw.Draw(sheet)
    d.text((46, 26), "KITCHEN v14 V3 · APPROVED V8 ROOM COMPARISON", font=font(38, True), fill=PAPER)
    d.text((46, 78), "Both rooms shown at exact 1:1. V3 carries one cabinet family, worktop datum and light across the room.", font=font(21), fill=MUTED)
    card(sheet, v8, (70, 160), "APPROVED V8 ROOM PROOF · exact 1:1")
    card(sheet, room, (2180, 160), "V3 COHERENT ROOM · exact 1:1")
    return sheet


def geometry_comparison(room: Image.Image) -> Image.Image:
    schematic = rgba(REF / "kitchen_v14_schematic_1x.png")
    sheet = Image.new("RGBA", (4300, 900), (17, 27, 34, 255))
    d = ImageDraw.Draw(sheet)
    d.text((46, 26), "KITCHEN v14 V3 · GEOMETRY CONTROL", font=font(38, True), fill=PAPER)
    d.text((46, 78), "The schematic is geometry only; the room-wide painting is registered on the same 2048 × 576 module.", font=font(21), fill=MUTED)
    card(sheet, schematic, (70, 160), "APPROVED v14 SCHEMATIC · exact 1:1")
    card(sheet, room, (2180, 160), "V3 REGISTERED ROOM · exact 1:1")
    return sheet


def build_manifest(empty: Image.Image, room: Image.Image, prime: Image.Image) -> None:
    source_path = SRC / "kitchen-v14-coherent-room-no-keeper.png"
    manifest = {
        "schema": "lighthouse-keeper/kitchen-v14-coherent-room-review@1",
        "status": "review-candidate-awaiting-frank",
        "previousDraft": "review/kitchen-v14-redo-v2",
        "previousDraftStatus": "rejected-no-room-continuity",
        "runtimeMutation": False,
        "productionCutsMade": False,
        "artMethod": "one complete room-wide OpenAI image-generation painting; code only uniformly scales, crops, masks, places approved painted references, assembles and verifies",
        "modulePx": [2048, 576],
        "twoViewingScales": {"room": [2048, 576], "lighthouse": [256, 72]},
        "source": {
            "path": "sources/imagegen/kitchen-v14-coherent-room-no-keeper.png",
            "canvasPx": [2172, 724],
            "sha256": sha(source_path),
            "registration": {"uniformScaleToPx": [2048, 683], "cropPx": [0, 68, 2048, 644]},
        },
        "approvedShellReuse": "exact ceiling and floor-slab boundary bands from sources/reference/kitchen-v8-room-shell-empty-1x.png",
        "prime": {"canvasPx": list(prime.size), "anchorPx": [1150, 204], "sha256": sha(OUT / "kitchen-v14-v3-prime-registered.png")},
        "outputs": {},
    }
    for path in sorted(OUT.glob("*.png")):
        manifest["outputs"][path.name] = {"canvasPx": list(rgba(path).size), "sha256": sha(path)}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    empty, room, prime = build_room()
    save(empty, OUT / "kitchen-v14-v3-coherent-room-empty-1x.png")
    save(prime, OUT / "kitchen-v14-v3-prime-registered.png")
    save(room, OUT / "kitchen-v14-v3-coherent-room-1x.png")
    save(two_scales(room), OUT / "kitchen-v14-v3-two-viewing-scales.png")
    save(continuity_comparison(room), OUT / "kitchen-v14-v2-v3-continuity-comparison.png")
    save(v8_comparison(room), OUT / "kitchen-v14-v3-v8-comparison.png")
    save(geometry_comparison(room), OUT / "kitchen-v14-v3-geometry-comparison.png")
    build_manifest(empty, room, prime)


if __name__ == "__main__":
    main()
