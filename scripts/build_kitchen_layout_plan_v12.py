#!/usr/bin/env python3
"""Build Kitchen Layout Plan V12 from the exact approved V11 cabinet cell."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-layout-plan-2026-10-19-v12"
RAW = ROOT / "art" / "raw" / SET
DRAFT = ROOT / "art" / "drafts" / SET
PUBLIC = ROOT / "public" / "keeper-review" / "kitchen-layout-plan-v12"
ASSETS = PUBLIC / "assets"
BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"
CABINET = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"

ROOM = (772, 224)
CABINET_CELL = (176, 82)
CABINET_GUTTER = (4, 4)
RUNS = ((168, 134), (420, 134))
FRIDGE = (84, 140, 168, 218)
OVEN = (336, 131, 420, 208)
SINK_MOUNT = (504, 118, 588, 151)
TABLE = (680, 148, 764, 222)
ANCHORS = ((126, 218), (210, 218), (294, 218), (378, 218), (462, 218), (546, 218))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def base_room() -> Image.Image:
    background = Image.open(BACKGROUND).convert("RGBA")
    cabinet = Image.open(CABINET).convert("RGBA")
    if background.size != ROOM or cabinet.size != CABINET_CELL:
        raise RuntimeError("V12 authority geometry changed")
    room = background.copy()
    for x, y in RUNS:
        room.alpha_composite(cabinet, (x - CABINET_GUTTER[0], y - CABINET_GUTTER[1]))
    return room


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, colour=(19, 35, 47, 255)) -> None:
    font = ImageFont.load_default()
    x, y = xy
    box = draw.textbbox((x, y), text, font=font)
    draw.rectangle((box[0] - 2, box[1] - 1, box[2] + 2, box[3] + 1), fill=(246, 232, 198, 235))
    draw.text((x, y), text, fill=colour, font=font)


def envelope_proof(room: Image.Image) -> Image.Image:
    out = room.copy()
    layer = Image.new("RGBA", ROOM, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rectangle(FRIDGE, fill=(236, 243, 239, 86), outline=(28, 114, 129, 255), width=2)
    draw.rectangle(OVEN, fill=(226, 130, 51, 75), outline=(154, 61, 31, 255), width=2)
    draw.rectangle(SINK_MOUNT, fill=(83, 214, 207, 64), outline=(16, 113, 123, 255), width=1)
    draw.rectangle(TABLE, fill=(235, 178, 79, 48), outline=(142, 83, 34, 255), width=1)
    draw.line((0, 134, 671, 134), fill=(0, 202, 219, 230), width=1)
    draw.line((0, 218, 671, 218), fill=(246, 213, 79, 230), width=1)
    label(draw, (87, 144), "FRIDGE 84x78")
    label(draw, (201, 117), "RUN A 168x74")
    label(draw, (341, 113), "OVEN/HOB 84x77")
    label(draw, (453, 101), "RUN B 168x74")
    label(draw, (507, 120), "SINK OVERLAY")
    label(draw, (682, 135), "TABLE 84x74")
    label(draw, (5, 123), "cabinet top y=134")
    label(draw, (5, 208), "floor datum y=218")
    out.alpha_composite(layer)
    return out


def anchor_proof(room: Image.Image) -> Image.Image:
    out = room.copy()
    layer = Image.new("RGBA", ROOM, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for index, (x, y) in enumerate(ANCHORS, start=1):
        draw.line((x, 104, x, y), fill=(247, 197, 50, 205), width=1)
        draw.line((x - 4, y, x + 4, y), fill=(16, 93, 113, 255), width=1)
        draw.line((x, y - 4, x, y + 4), fill=(16, 93, 113, 255), width=1)
        label(draw, (x - 12, 105), f"A{index}")
    draw.rectangle(FRIDGE, outline=(28, 114, 129, 255), width=1)
    draw.rectangle(OVEN, outline=(154, 61, 31, 255), width=1)
    draw.rectangle(SINK_MOUNT, outline=(16, 113, 123, 255), width=1)
    out.alpha_composite(layer)
    return out


def page() -> str:
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-layout-plan-v12/"><title>Kitchen Layout Plan V12 · geometry-only room proof</title><style>
:root{color-scheme:dark;--bg:#07171e;--panel:#0d2630;--line:#276679;--ink:#eef8f5;--muted:#abc7c4;--gold:#e8ad47;--sea:#72d9d3}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:26px 20px 54px}h1{font-size:clamp(28px,4vw,46px);line-height:1.05;margin:.2rem 0 .5rem}h2{margin:0 0 8px}.lede{max-width:920px;color:var(--muted);font-size:17px}.tags{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 22px}.tag{border:1px solid var(--line);border-radius:999px;padding:6px 10px;background:#0b212a}.notice{border-left:4px solid var(--gold);background:#19262a;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:18px 0;overflow:auto}.stage{width:max-content;min-width:100%;display:flex;justify-content:center;padding:16px;background:#091a21;border-radius:9px}.stage img{width:772px;height:224px;display:block;image-rendering:auto}.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-top:14px}.fact{border:1px solid #214e5d;background:#0a2028;border-radius:9px;padding:10px}.fact strong{display:block;color:var(--sea)}code{color:#9de4df}.status{font-weight:700;color:var(--sea)}</style></head><body><main>
<div class="tags"><span class="tag">V12 reversible layout gate</span><span class="tag">Exact approved V11 cabinets</span><span class="tag">No new appliance art</span><span class="tag">Native 772 × 224</span></div><h1>Cabinets placed in the room</h1>
<p class="lede">This proof settles registration before any standalone appliance is drawn. It uses the exact approved cabinet cell twice and preserves the established fridge, oven/hob, sink and table confines.</p><p id="status" class="status">Loading review media…</p>
<p class="notice"><strong>Important:</strong> the appliance shapes below are measurement overlays, not proposed artwork. Independent sprites may finish a few pixels above or below the worktop. They do not contain, replace or redraw cabinet pixels.</p>
<section class="panel"><h2>Clean cabinet placement · exact game size</h2><div class="stage"><img src="assets/kitchen-layout-clean.png" alt="Two approved two-bay cabinet runs placed in the kitchen room"></div><div class="facts"><div class="fact"><strong>Run A</strong><code>x=168–336, y=134–208</code></div><div class="fact"><strong>Oven opening</strong><code>x=336–420</code></div><div class="fact"><strong>Run B</strong><code>x=420–588, y=134–208</code></div></div></section>
<section class="panel"><h2>Standalone-asset envelope proof</h2><div class="stage"><img src="assets/kitchen-layout-envelope-proof.png" alt="Measured fridge oven sink and table envelopes around the approved cabinets"></div><div class="facts"><div class="fact"><strong>Fridge</strong><code>84 × 78 at x=84, y=140</code><br>Top is 6 px below cabinet top.</div><div class="fact"><strong>Oven with hob</strong><code>84 × 77 at x=336, y=131</code><br>Top is 3 px above cabinet top.</div><div class="fact"><strong>Sink</strong>Independent overlay registered to final cabinet bay; not an extra room bay.</div><div class="fact"><strong>Table/chair</strong><code>84 × 74 at x=680, y=148</code></div></div></section>
<section class="panel"><h2>Keeper stop/turn anchor proof</h2><div class="stage"><img src="assets/kitchen-layout-anchor-proof.png" alt="Six unchanged kitchen interaction centres"></div><p class="lede">The six established room centres stay at x=126, 210, 294, 378, 462 and 546 on the y=218 walking datum. Appliance upgrades change sprites, not these route anchors.</p></section>
</main><script>const images=[...document.images];Promise.all(images.map(img=>img.complete&&img.naturalWidth?Promise.resolve():img.decode())).then(()=>document.getElementById('status').textContent='All layout media loaded and decoded.').catch(error=>document.getElementById('status').textContent='A review image failed to decode: '+error.message)</script></body></html>"""


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    clean = base_room()
    outputs = {
        "kitchen-layout-clean.png": clean,
        "kitchen-layout-envelope-proof.png": envelope_proof(clean),
        "kitchen-layout-anchor-proof.png": anchor_proof(clean),
    }
    for name, image in outputs.items():
        save(image, RAW / name)
        (ASSETS / name).write_bytes((RAW / name).read_bytes())
    catalogue = {
        "set": SET,
        "status": "geometry-only-awaiting-visual-review",
        "roomPixels": list(ROOM),
        "authority": {
            "approvedCabinetCell": str(CABINET.relative_to(ROOT)),
            "approvedCabinetCellSha256": sha(CABINET),
            "background": str(BACKGROUND.relative_to(ROOT)),
            "backgroundSha256": sha(BACKGROUND),
        },
        "geometry": {
            "cabinetBodyPlacements": [list(item) for item in RUNS],
            "fridgeBoundsExclusive": list(FRIDGE),
            "ovenHobBoundsExclusive": list(OVEN),
            "sinkOverlayRegistration": list(SINK_MOUNT),
            "tableChairBoundsExclusive": list(TABLE),
            "interactionAnchors": [list(item) for item in ANCHORS],
            "worktopTopY": 134,
            "walkingDatumY": 218,
        },
        "boundaries": {
            "newApplianceArt": False,
            "sinkConsumesExtraBay": False,
            "standaloneMeansIndependentSprite": True,
            "finalChanged": False,
            "runtimeChanged": False,
        },
        "outputs": {name: {"sha256": sha(RAW / name), "pixels": list(image.size)} for name, image in outputs.items()},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    register = {
        "set": SET,
        "status": "reversible-unapproved-unpromoted",
        "files": {str(path.relative_to(ROOT)): sha(path) for path in [CABINET, BACKGROUND, catalogue_path, *[RAW / name for name in outputs]]},
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(page())
    print("Built V12 geometry-only room proof from the exact approved V11 cabinet cell")


if __name__ == "__main__":
    main()
