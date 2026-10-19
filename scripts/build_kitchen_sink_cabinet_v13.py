#!/usr/bin/env python3
"""Build the standalone Kitchen Sink Cabinet V13 fit gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-sink-cabinet-2026-10-19-v13"
SOURCE_DIR = ROOT / "art/source" / SET
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-sink-cabinet-v13"
ASSETS = PUBLIC / "assets"
GENERATED = SOURCE_DIR / "rejected-sources/snapped-tap-family.png"
SELECTED = SOURCE_DIR / "sink-cabinet-selected-source.png"
CABINET = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"
BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"

ROOM = (772, 224)
SINK_CELL = (92, 108)
BODY_ORIGIN_IN_CELL = (4, 30)
BODY_SIZE = (84, 74)
RUN_BODY_ORIGIN = (168, 134)
SINK_BODY_ORIGIN = (336, 134)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def selected_source() -> Image.Image:
    sheet = Image.open(GENERATED).convert("RGBA")
    if sheet.size != (2172, 724):
        raise RuntimeError(f"Unexpected generated sheet size {sheet.size}")
    standard = sheet.crop((0, 0, 724, 724))
    pixels = standard.load()
    for y in range(standard.height):
        for x in range(standard.width):
            if pixels[x, y][3] < 8:
                pixels[x, y] = (0, 0, 0, 0)
    bbox = standard.getchannel("A").getbbox()
    if bbox != (50, 13, 689, 693):
        raise RuntimeError(f"Generated standard sink bounds changed: {bbox}")
    object_image = standard.crop(bbox)
    selected = Image.new("RGBA", (object_image.width + 64, object_image.height + 64), (0, 0, 0, 0))
    selected.alpha_composite(object_image, (32, 32))
    return selected


def native_cell(source: Image.Image) -> Image.Image:
    # Remove the selected-source padding. The worktop begins 156 source pixels
    # below the original state cell's top. Scale tap and cabinet independently
    # so the complete cabinet body is exactly the approved 84 × 74 footprint.
    object_image = source.crop((32, 32, source.width - 32, source.height - 32))
    split = 144
    upper = resize_premultiplied(object_image.crop((0, 0, object_image.width, split)), (84, 26))
    body = resize_premultiplied(object_image.crop((0, split, object_image.width, object_image.height)), BODY_SIZE)
    cell = Image.new("RGBA", SINK_CELL, (0, 0, 0, 0))
    cell.alpha_composite(upper, (4, 4))
    cell.alpha_composite(body, BODY_ORIGIN_IN_CELL)
    return cell


def room_proof(sink: Image.Image) -> Image.Image:
    room = Image.open(BACKGROUND).convert("RGBA")
    cabinet = Image.open(CABINET).convert("RGBA")
    if room.size != ROOM or cabinet.size != (176, 82):
        raise RuntimeError("Authority geometry changed")
    room.alpha_composite(cabinet, (RUN_BODY_ORIGIN[0] - 4, RUN_BODY_ORIGIN[1] - 4))
    room.alpha_composite(sink, (SINK_BODY_ORIGIN[0] - 4, SINK_BODY_ORIGIN[1] - 30))
    return room


def page() -> str:
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-sink-cabinet-v13/"><title>Kitchen Sink Cabinet V13 · standalone fit gate</title><style>
:root{color-scheme:dark;--bg:#07171e;--panel:#0d2630;--line:#276679;--ink:#eff9f6;--muted:#abc8c5;--sea:#72d9d3;--gold:#e8ad47}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:26px 20px 54px}h1{font-size:clamp(28px,4vw,46px);line-height:1.05;margin:.2rem 0 .5rem}h2{margin:0 0 9px}.lede{max-width:900px;color:var(--muted);font-size:17px}.tags{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 22px}.tag{border:1px solid var(--line);border-radius:999px;padding:6px 10px;background:#0b212a}.notice{border-left:4px solid var(--gold);background:#19262a;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:18px 0;overflow:auto}.checker{background-color:#091a21;background-image:linear-gradient(45deg,#112d37 25%,transparent 25%),linear-gradient(-45deg,#112d37 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#112d37 75%),linear-gradient(-45deg,transparent 75%,#112d37 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}.stage{display:flex;justify-content:center;align-items:center;width:max-content;min-width:100%;padding:18px;border-radius:9px}.master{width:min(100%,730px);height:auto}.native4{width:368px;height:432px;image-rendering:auto}.room{width:772px;height:224px;display:block}.states{display:grid;grid-template-columns:repeat(3,minmax(180px,1fr));gap:12px}.card{background:#091d25;border:1px solid #214f5d;border-radius:10px;padding:12px;text-align:center}.card img{width:184px;height:216px;display:block;margin:auto}.status{font-weight:700;color:var(--sea)}@media(max-width:700px){.states{grid-template-columns:1fr}}</style></head><body><main>
<div class="tags"><span class="tag">V13 reversible draft</span><span class="tag">One complete 84 px bay</span><span class="tag">No cabinet beneath</span><span class="tag">No water effects yet</span></div><h1>Standalone sink cabinet</h1><p class="lede">The sink is its own complete one-bay unit: cabinet, worktop, basin and intact tap. It does not overlay or redraw any approved cabinet. This gate tests the join beside the exact approved two-cabinet run before water animation is added.</p><p id="status" class="status">Loading review media…</p>
<p class="notice"><strong>Corrected state rule:</strong> the tap and basin do not change in the broken state. Standard, On base and Broken base are byte-identical; On and Broken will be distinguished only by separate reusable water-effect strips.</p>
<section class="panel"><h2>High-resolution construction</h2><div class="stage checker"><img class="master" src="assets/sink-cabinet-selected-source.png" alt="High-resolution standalone one-bay sink cabinet"></div></section>
<section class="panel"><h2>Exact native sink asset · 4× inspection</h2><div class="stage checker"><img class="native4" src="assets/sink-cabinet-standard.png" alt="Native sink cabinet shown four times larger"></div><p class="lede">The cabinet body is exactly 84 × 74 px. Its 92 × 108 cell adds transparent safety gutters and headroom for the intact tap.</p></section>
<section class="panel"><h2>All three static state bases</h2><div class="states"><div class="card"><h3>Standard</h3><img src="assets/sink-cabinet-standard.png" alt="Standard sink cabinet"></div><div class="card"><h3>On base</h3><img src="assets/sink-cabinet-on-base.png" alt="On-state static sink cabinet base"></div><div class="card"><h3>Broken base</h3><img src="assets/sink-cabinet-broken-base.png" alt="Broken-state static sink cabinet base"></div></div></section>
<section class="panel"><h2>Approved two-cabinet run + standalone sink · native game size</h2><div class="stage"><img class="room" src="assets/cabinet-run-plus-sink-native-room.png" alt="Approved two-cabinet run and separate sink cabinet side by side in the room"></div><p class="lede">The approved run occupies x=168–336. The independent sink body begins exactly at x=336 and occupies x=336–420. Both bodies share y=134–208, but neither asset contains pixels from the other.</p></section>
</main><script>const images=[...document.images];Promise.all(images.map(img=>img.complete&&img.naturalWidth?Promise.resolve():img.decode())).then(()=>document.getElementById('status').textContent='All sink-fit media loaded and decoded.').catch(error=>document.getElementById('status').textContent='A review image failed to decode: '+error.message)</script></body></html>"""


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    source = selected_source()
    save(source, SELECTED)
    sink = native_cell(source)
    standard = RAW / "sink-cabinet-standard.png"
    on_base = RAW / "sink-cabinet-on-base.png"
    broken_base = RAW / "sink-cabinet-broken-base.png"
    for destination in (standard, on_base, broken_base):
        save(sink, destination)
    room = room_proof(sink)
    room_path = RAW / "cabinet-run-plus-sink-native-room.png"
    save(room, room_path)
    outputs = [SELECTED, standard, on_base, broken_base, room_path]
    for output in outputs:
        (ASSETS / output.name).write_bytes(output.read_bytes())
    catalogue = {
        "set": SET,
        "status": "standalone-sink-fit-awaiting-visual-review",
        "construction": {
            "completeStandaloneOneBayUnit": True,
            "overlaysApprovedCabinet": False,
            "containsOwnCabinetWorktopBasinTap": True,
            "bodyPixels": list(BODY_SIZE),
            "cellPixels": list(SINK_CELL),
            "bodyOriginInCell": list(BODY_ORIGIN_IN_CELL),
            "tapAndBasinChangeWhenBroken": False,
        },
        "states": {
            "standard": standard.name,
            "onBase": on_base.name,
            "brokenBase": broken_base.name,
            "allStaticBasesByteIdentical": len({sha(standard), sha(on_base), sha(broken_base)}) == 1,
            "waterEffectsIncluded": False,
        },
        "fitProof": {
            "approvedTwoBayRunBodyBoundsExclusive": [168, 134, 336, 208],
            "standaloneSinkBodyBoundsExclusive": [336, 134, 420, 208],
            "sharedPixels": False,
            "nativeRoomPixels": list(ROOM),
        },
        "outputs": {output.name: sha(output) for output in outputs},
        "boundaries": {"finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    register = {"set": SET, "status": "reversible-unapproved-unpromoted", "files": {str(path.relative_to(ROOT)): sha(path) for path in [GENERATED, *outputs, catalogue_path]}}
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(page())
    print("Built Kitchen Sink Cabinet V13: complete standalone one-bay unit beside exact approved V11 run")


if __name__ == "__main__":
    main()
