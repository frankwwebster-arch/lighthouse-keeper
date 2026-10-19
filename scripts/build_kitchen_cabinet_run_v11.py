#!/usr/bin/env python3
"""Build the cabinet-only Kitchen V11 visual gate.

The cabinet source is a new generated raster. Historical kitchen cabinet pixels
are never sampled or composited into the asset; the established empty room is
used only for the native-size placement proof.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-cabinet-run-2026-10-19-v11"
SOURCE_DIR = ROOT / "art" / "source" / SET
RAW_DIR = ROOT / "art" / "raw" / SET
DRAFT_DIR = ROOT / "art" / "drafts" / SET
REVIEW_DIR = ROOT / "public" / "keeper-review" / "kitchen-cabinet-run-v11"

SOURCE = SOURCE_DIR / "cabinet-run-generated-source.png"
ROOM_BACKGROUND = (
    ROOT
    / "art"
    / "raw"
    / "kitchen-rebuild-foundation-2026-10-18-v1"
    / "kitchen-standard-background.png"
)

NATIVE_BODY = (168, 74)
NATIVE_CELL = (176, 82)
CELL_GUTTER = (4, 4)
ROOM_SIZE = (772, 224)
PLACEMENTS = ((168, 134), (420, 134))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_generated_source(source: Image.Image) -> tuple[Image.Image, tuple[int, int, int, int]]:
    """Remove near-invisible generation dust and crop the one cabinet silhouette."""
    image = source.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a < 8:
                pixels[x, y] = (0, 0, 0, 0)
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("Generated cabinet source has no visible pixels")
    return image.crop(bbox), bbox


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Lanczos-resize premultiplied RGBA so transparent edges do not darken."""
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def write_review_page() -> None:
    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<base href="/keeper-review/kitchen-cabinet-run-v11/"><title>Kitchen Cabinet Run V11 · cabinet-only review</title>
<style>
:root{color-scheme:dark;--ink:#eaf6f4;--muted:#a9c5c3;--panel:#0d2630;--line:#276679;--copper:#e6802d;--sea:#74d7d0}*{box-sizing:border-box}body{margin:0;background:#07171e;color:var(--ink);font:15px/1.5 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:28px 22px 54px}h1{margin:.2rem 0 .55rem;font-size:clamp(28px,4vw,46px);line-height:1.05}h2{margin:0 0 12px;font-size:22px}.lede{max-width:850px;color:var(--muted);font-size:17px}.tags{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 24px}.tag{border:1px solid var(--line);border-radius:999px;padding:6px 10px;background:#0b212a;color:#cce7e4}.notice{border-left:4px solid var(--copper);background:#17262a;padding:12px 14px;margin:0 0 24px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:18px 0;overflow:auto}.checker{background-color:#0a1a22;background-image:linear-gradient(45deg,#112c37 25%,transparent 25%),linear-gradient(-45deg,#112c37 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#112c37 75%),linear-gradient(-45deg,transparent 75%,#112c37 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0}.frame{display:flex;justify-content:center;align-items:center;padding:24px;border-radius:10px;min-width:max-content}.master{width:min(100%,920px);height:auto;display:block}.native4{width:704px;height:328px;object-fit:contain;image-rendering:auto;display:block}.room{width:772px;height:224px;display:block;image-rendering:auto}.row{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,320px);gap:18px;align-items:start}.facts{margin:0;padding-left:20px;color:var(--muted)}.facts strong{color:var(--ink)}.onepx{display:flex;gap:14px;align-items:center;margin-top:14px;color:var(--muted)}.onepx img{width:176px;height:82px;display:block;background:#091920}.status{font-weight:700;color:var(--sea)}@media(max-width:780px){.row{grid-template-columns:1fr}.panel{padding:12px}}
</style></head><body><main>
<div class="tags"><span class="tag">Cabinet-only V11 reversible draft</span><span class="tag">New raster construction</span><span class="tag">No sink or appliances</span><span class="tag">Straight-on flat cutaway</span></div>
<h1>One two-cabinet run</h1>
<p class="lede">This gate deliberately reviews only the cabinetry. The same run can be duplicated without redrawing it. Sink, fridge, oven, dishwasher and every countertop appliance remain separate future assets.</p>
<p id="status" class="status">Loading review media…</p>
<p class="notice"><strong>Review boundary:</strong> this is a new unapproved cabinet draft. V10 remains immutable rejected provenance. Nothing has entered Final or runtime.</p>

<section class="panel"><h2>High-resolution construction</h2><div class="frame checker"><img class="master" src="assets/cabinet-run-master.png" alt="New two-bay storm-blue cabinet run on transparency"></div></section>

<section class="panel"><div class="row"><div><h2>Exact native asset · 4× inspection</h2><div class="frame checker"><img class="native4" src="assets/cabinet-run-native-cell.png" alt="Exact native two-bay cabinet cell shown four times larger"></div></div><div><h2>Geometry</h2><ul class="facts"><li><strong>Installed body:</strong> 168 × 74 px</li><li><strong>Two equal bays:</strong> 84 px each</li><li><strong>Body datum:</strong> y=134–207</li><li><strong>Cell:</strong> 176 × 82 px</li><li><strong>Transparent gutter:</strong> 4 px minimum</li><li><strong>Projection:</strong> straight-on, parallel, no vanishing point</li><li><strong>Structure:</strong> one worktop, one front plane, one plinth</li></ul><div class="onepx"><img src="assets/cabinet-run-native-cell.png" alt="Exact one-times native cabinet cell"><span>Actual 1× asset</span></div></div></div></section>

<section class="panel"><h2>Two byte-identical runs · exact 772 × 224 game view</h2><p class="lede">The same native cell is drawn twice at x=168 and x=420. The 84-pixel centre opening is retained for the standalone oven. This proves duplication only; it does not yet place the later standalone sink or dishwasher.</p><div class="frame"><img class="room" src="assets/cabinet-run-duplicated-native-room.png" alt="Two identical cabinet runs in the empty kitchen at exact game size"></div></section>
</main><script>
const images=[...document.images]; Promise.all(images.map(img=>img.complete&&img.naturalWidth?Promise.resolve():img.decode())).then(()=>{document.getElementById('status').textContent='All cabinet review media loaded and decoded.'}).catch(error=>{document.getElementById('status').textContent='A review image failed to decode: '+error.message});
</script></body></html>"""
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    (REVIEW_DIR / "index.html").write_text(html, encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if not ROOM_BACKGROUND.exists():
        raise FileNotFoundError(ROOM_BACKGROUND)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    assets_dir = REVIEW_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    source = Image.open(SOURCE)
    cabinet, source_bbox = clean_generated_source(source)

    master = Image.new("RGBA", (cabinet.width + 64, cabinet.height + 64), (0, 0, 0, 0))
    master.alpha_composite(cabinet, (32, 32))
    master_path = RAW_DIR / "cabinet-run-master.png"
    master.save(master_path)

    native_body = resize_premultiplied(cabinet, NATIVE_BODY)
    native_cell = Image.new("RGBA", NATIVE_CELL, (0, 0, 0, 0))
    native_cell.alpha_composite(native_body, CELL_GUTTER)
    native_path = RAW_DIR / "cabinet-run-native-cell.png"
    native_cell.save(native_path)

    room = Image.open(ROOM_BACKGROUND).convert("RGBA")
    if room.size != ROOM_SIZE:
        raise RuntimeError(f"Room background is {room.size}, expected {ROOM_SIZE}")
    for x, y in PLACEMENTS:
        room.alpha_composite(native_cell, (x - CELL_GUTTER[0], y - CELL_GUTTER[1]))
    room_path = RAW_DIR / "cabinet-run-duplicated-native-room.png"
    room.save(room_path)

    for source_path in (master_path, native_path, room_path):
        (assets_dir / source_path.name).write_bytes(source_path.read_bytes())

    catalogue = {
        "set": SET,
        "status": "cabinet-only-awaiting-visual-review",
        "source": {
            "file": str(SOURCE.relative_to(ROOT)),
            "sha256": sha256(SOURCE),
            "generatedFromScratch": True,
            "historicalCabinetPixelsUsed": False,
            "visibleSourceBBox": list(source_bbox),
        },
        "asset": {
            "name": "cabinet-run-two-bay",
            "masterFile": master_path.name,
            "nativeFile": native_path.name,
            "logicalBodyPixels": list(NATIVE_BODY),
            "cellPixels": list(NATIVE_CELL),
            "cellGutterPixels": list(CELL_GUTTER),
            "bayPixels": [84, 74],
            "projection": "straight-on-flat-cutaway-parallel",
            "containsSink": False,
            "containsAppliances": False,
        },
        "nativeRoom": {
            "file": room_path.name,
            "pixels": list(ROOM_SIZE),
            "bodyPlacements": [list(item) for item in PLACEMENTS],
            "standaloneOvenGapPixels": [336, 134, 84, 74],
        },
    }
    catalogue_path = DRAFT_DIR / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n", encoding="utf-8")

    register = {
        "set": SET,
        "status": "reversible-unapproved-unpromoted",
        "files": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (SOURCE, master_path, native_path, room_path, catalogue_path)
        },
    }
    (DRAFT_DIR / "batch-register.json").write_text(
        json.dumps(register, indent=2) + "\n", encoding="utf-8"
    )
    write_review_page()
    print(f"Built {SET}: one new two-bay cabinet run and one duplicated native-room proof")


if __name__ == "__main__":
    main()
