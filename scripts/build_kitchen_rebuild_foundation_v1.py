#!/usr/bin/env python3
"""Build the clean-slate Kitchen Rebuild V1 standard-state foundation."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-foundation-2026-10-18-v1"
SOURCE_DIR = ROOT / "art/source" / SET
SOURCE = SOURCE_DIR / "generated/full-standard-kitchen-transparent-v2.png"
MASTER = SOURCE_DIR / "generated/full-standard-kitchen-master-v1.png"
BIN_STANDARD = ROOT / "art/raw/kitchen-bin-states-2026-10-18-v28/bin-standard.png"
BIN_BROKEN = ROOT / "art/raw/kitchen-bin-states-2026-10-18-v28/bin-broken-overflowing.png"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-foundation-v1"
ASSETS = PUBLIC / "assets"

SOURCE_SHA = "3a4430a0d07be4a945e00ba717d2f23e55e8730ba63b420efa41aaa3c283a9f1"
MASTER_SHA = "a6f0b8d3d8181096e0455effc2753630ad893c34760c68a20fb40baedb60b48d"
BIN_STANDARD_SHA = "86b05224a7da5fc5c05918f2875018920ed54cf46fc00cb08952ffd29789f9c0"
BIN_BROKEN_SHA = "77ad87fabfd3e5c10a4a14f294af343a5d93a2a2015e6d77f18a4140b1f5fb4f"

ROOM_SIZE = (772, 224)
SCALE = 4
LOGICAL_ROOM = (193, 56)
RUN_X = 84
BAY_WIDTH = 84
BAY_COUNT = 6
RUN_WIDTH = BAY_WIDTH * BAY_COUNT
RUN_RIGHT = RUN_X + RUN_WIDTH
WORKTOP_TOP = 134
FASCIA_TOP = 151
RUN_BOTTOM = 218
FLOOR_LINE = 208
TABLE_BOUNDS = (680, 148, 764, 222)
BIN_CELL_ORIGIN = (8, 149)

# Extraction boundaries were measured once from the generated transparent
# master.  Every delivered standard asset is derived from this same drawing.
RUN_SOURCE_X = (169, 1714)
RUN_SEGMENTS = (
    ((169, 200, 1714, 289), (RUN_WIDTH, WORKTOP_TOP - 105)),
    ((169, 289, 1714, 345), (RUN_WIDTH, FASCIA_TOP - WORKTOP_TOP)),
    ((169, 345, 1714, 615), (RUN_WIDTH, RUN_BOTTOM - FASCIA_TOP)),
)
TABLE_SOURCE = (1755, 305, 2130, 636)
BAY_NAMES = ("fridge", "kettle", "toaster", "oven-hob", "mixing-bowl", "basin")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def alpha_cleanup(image: Image.Image, threshold: int = 16) -> Image.Image:
    """Discard extraction haze while keeping the artist-rendered edge alpha."""
    result = image.copy().convert("RGBA")
    pixels = result.load()
    for y in range(result.height):
        for x in range(result.width):
            r, g, b, a = pixels[x, y]
            if a < threshold:
                pixels[x, y] = (0, 0, 0, 0)
            elif a < 255:
                pixels[x, y] = (r, g, b, a)
    return result


def normalize_run(source: Image.Image) -> Image.Image:
    run = Image.new("RGBA", (RUN_WIDTH, RUN_BOTTOM - 105))
    destination_y = 0
    for source_box, size in RUN_SEGMENTS:
        section = alpha_cleanup(source.crop(source_box)).resize(size, Image.Resampling.LANCZOS)
        section = alpha_cleanup(section)
        run.alpha_composite(section, (0, destination_y))
        destination_y += size[1]
    return run


def normalize_table(source: Image.Image) -> Image.Image:
    table = alpha_cleanup(source.crop(TABLE_SOURCE)).resize(
        (TABLE_BOUNDS[2] - TABLE_BOUNDS[0], TABLE_BOUNDS[3] - TABLE_BOUNDS[1]),
        Image.Resampling.LANCZOS,
    )
    return alpha_cleanup(table)


def make_background() -> Image.Image:
    image = Image.new("RGBA", ROOM_SIZE, (244, 226, 188, 255))
    pixels = image.load()
    # Restrained deterministic plaster modulation; no old kitchen pixels are
    # copied.  The room remains quiet so the new unified furniture reads first.
    for y in range(0, 190):
        for x in range(ROOM_SIZE[0]):
            grain = ((x * 17 + y * 31 + (x // 23) * 7) % 11) - 5
            warm = max(0, 5 - abs(y - 92) // 24)
            pixels[x, y] = (244 + grain // 3, 225 + warm + grain // 4, 186 + warm + grain // 5, 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 190, 771, 193), fill=(236, 216, 178, 255))
    draw.rectangle((0, 194, 771, 196), fill=(174, 142, 105, 255))
    draw.line((0, 197, 771, 197), fill=(62, 53, 49, 255), width=1)
    draw.rectangle((0, 198, 771, 223), fill=(181, 73, 39, 255))
    for y, colour in ((202, (211, 94, 47, 255)), (208, (139, 52, 37, 255)), (216, (215, 93, 45, 255))):
        draw.line((0, y, 771, y), fill=colour, width=2)
    for x in range(34, 772, 83):
        draw.line((x, 198, x - 9, 223), fill=(148, 55, 38, 255), width=1)
    return image


def make_measurement_overlay(room: Image.Image) -> Image.Image:
    overlay = room.copy()
    shade = Image.new("RGBA", ROOM_SIZE)
    draw = ImageDraw.Draw(shade)
    for i in range(BAY_COUNT + 1):
        x = RUN_X + i * BAY_WIDTH
        draw.line((x, 88, x, 223), fill=(255, 244, 120, 220), width=1)
    draw.rectangle((RUN_X, 88, RUN_RIGHT - 1, 217), outline=(255, 244, 120, 230), width=1)
    draw.line((0, WORKTOP_TOP, 771, WORKTOP_TOP), fill=(63, 231, 255, 225), width=1)
    draw.line((0, FASCIA_TOP, 771, FASCIA_TOP), fill=(255, 174, 66, 225), width=1)
    draw.line((0, FLOOR_LINE, 771, FLOOR_LINE), fill=(255, 255, 255, 225), width=1)
    draw.rectangle(TABLE_BOUNDS, outline=(255, 244, 120, 230), width=1)
    draw.rectangle((BIN_CELL_ORIGIN[0], BIN_CELL_ORIGIN[1], BIN_CELL_ORIGIN[0] + 71, BIN_CELL_ORIGIN[1] + 71), outline=(255, 244, 120, 230), width=1)
    font = ImageFont.load_default()
    labels = (
        (RUN_X + 2, 91, "1 FRIDGE"),
        (RUN_X + BAY_WIDTH + 2, 91, "2 KETTLE"),
        (RUN_X + BAY_WIDTH * 2 + 2, 91, "3 TOASTER"),
        (RUN_X + BAY_WIDTH * 3 + 2, 91, "4 OVEN/HOB"),
        (RUN_X + BAY_WIDTH * 4 + 2, 91, "5 BOWL"),
        (RUN_X + BAY_WIDTH * 5 + 2, 91, "6 BASIN"),
    )
    for x, y, label in labels:
        draw.rectangle((x - 1, y - 1, x + len(label) * 6, y + 9), fill=(5, 20, 40, 205))
        draw.text((x, y), label, font=font, fill=(255, 244, 120, 255))
    overlay.alpha_composite(shade)
    return overlay


def build_page() -> str:
    cards = "".join(
        f'<article><h3>{name.replace("-", " / ").title()}</h3><div class="isolated"><img data-media src="assets/bay-{name}.png" width="84" height="120" alt="Isolated standard {name} bay"></div><p>84 × 120 px review cell</p></article>'
        for name in BAY_NAMES
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/keeper-review/kitchen-rebuild-foundation-v1/"><title>Kitchen Rebuild V1 · standard foundation</title><style>
:root{{--ink:#eef7ff;--muted:#a9bad0;--panel:#13253c;--line:#35516f;--accent:#78d8db;--warn:#ffce64}}*{{box-sizing:border-box}}body{{margin:0;background:#09131f;color:var(--ink);font:15px/1.5 system-ui,sans-serif}}main{{max-width:1240px;margin:auto;padding:28px}}h1,h2,h3{{line-height:1.15}}h1{{font-size:34px;margin:.3rem 0}}h2{{margin-top:34px}}h3{{margin:.2rem 0 .8rem}}p{{color:var(--muted);max-width:86ch}}.tags{{display:flex;gap:8px;flex-wrap:wrap}}.tag{{border:1px solid var(--line);border-radius:999px;padding:4px 9px;color:var(--accent)}}section,article{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}}section{{margin:18px 0}}.native{{overflow:auto;background:#050a10;padding:12px;border-radius:8px}}.native img{{display:block;width:772px;height:224px;image-rendering:pixelated}}.inspect{{overflow:auto;background:#050a10;padding:12px;border-radius:8px}}.inspect img{{display:block;width:1544px;height:448px;image-rendering:pixelated}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(220px,1fr));gap:12px}}.grid article{{margin:0}}.isolated{{height:240px;display:flex;align-items:end;justify-content:center;background:linear-gradient(#f6e8c9 0 78%,#b94e2c 78%);overflow:hidden;border-radius:8px}}.isolated img{{width:168px;height:240px;image-rendering:pixelated}}.authority{{display:flex;gap:24px;align-items:end;flex-wrap:wrap}}.authority figure{{margin:0;text-align:center}}.authority img{{width:288px;height:288px;image-rendering:pixelated;background:linear-gradient(#f6e8c9 0 65%,#b94e2c 65%)}}button{{background:#143c55;color:white;border:1px solid #5a7c97;border-radius:7px;padding:8px 12px}}button:disabled{{opacity:.45}}.warn{{border-left:4px solid var(--warn);padding-left:12px}}code{{color:#aee8ef}}@media(max-width:820px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body><main><div class="tags"><span class="tag">Clean-slate Rebuild V1</span><span class="tag">Standard state only</span><span class="tag">Exact 772 × 224 game canvas</span><span class="tag">Bin unchanged</span></div><h1>Kitchen standard-state foundation</h1><p>This is one new coherent master construction. Every fitted asset except the separately approved bin was redrawn together, then registered to the binding room geometry. No On, Broken or animated artwork is in this gate.</p><p id="loading">Loading and decoding all review media…</p>
<section><h2>Complete kitchen · exact native game size</h2><div class="native"><img data-media src="assets/kitchen-standard-foundation.png" width="772" height="224" alt="Complete rebuilt standard kitchen at exact game size"></div><p>Six equal 84-pixel bays occupy x=84–588. The accepted standard bin is placed from its unchanged 72×72 cell at x=8/y=149. The entire one-person table and rear-facing chair remain visible.</p></section>
<section><h2>2× inspection</h2><div class="inspect"><img data-media src="assets/kitchen-standard-foundation.png" width="772" height="224" alt="Two-times inspection of rebuilt standard kitchen"></div></section>
<section><h2>Deterministic measurement proof</h2><button id="toggle" disabled>Alternate room / measurement overlay</button><div class="native" style="margin-top:12px"><img id="proof" data-media src="assets/kitchen-standard-measurement-overlay.png" width="772" height="224" alt="Kitchen bay and alignment measurement overlay"></div><p>Yellow: six equal bay limits plus retained bin/table cells. Cyan: worktop top y=134. Orange: fascia y=151. White: historical rear-wall foot line y=208.</p></section>
<h2>Isolated standard modules · literal crops from the same master</h2><div class="grid">{cards}</div>
<section><h2>Accepted bin authority · unchanged bytes</h2><div class="authority"><figure><img data-media src="assets/bin-standard-approved.png" width="72" height="72" alt="Approved standard bin"><figcaption>Standard · accepted SHA prefix <code>86b05224</code></figcaption></figure><figure><img data-media src="assets/bin-broken-approved.png" width="72" height="72" alt="Approved broken bin"><figcaption>Broken · accepted SHA prefix <code>77ad87fa</code></figcaption></figure></div><p>These are byte-for-byte copies of the accepted V28/V31 bin family. Rebuild V1 does not reinterpret them.</p></section>
<p class="warn"><strong>Review boundary:</strong> V41 and the earlier asset-by-asset kitchen drafts are rejected provenance. This reversible draft changes no Final/runtime asset. Approval of this standard foundation is required before coordinated Off/On/Broken families are drawn from it.</p>
<script>const media=[...document.querySelectorAll('[data-media]')];const loading=document.querySelector('#loading');const button=document.querySelector('#toggle');const proof=document.querySelector('#proof');Promise.all(media.map(img=>img.complete?img.decode():new Promise((ok,bad)=>{{img.addEventListener('load',()=>img.decode().then(ok,bad),{{once:true}});img.addEventListener('error',bad,{{once:true}})}}))).then(()=>{{loading.textContent='All review media loaded and decoded.';button.disabled=false}}).catch(()=>{{loading.textContent='A review image failed to load.'}});let measured=true;button.addEventListener('click',()=>{{measured=!measured;proof.src=measured?'assets/kitchen-standard-measurement-overlay.png':'assets/kitchen-standard-foundation.png'}});</script></main></body></html>'''


def main() -> None:
    assert sha(SOURCE) == SOURCE_SHA
    assert sha(MASTER) == MASTER_SHA
    assert sha(BIN_STANDARD) == BIN_STANDARD_SHA
    assert sha(BIN_BROKEN) == BIN_BROKEN_SHA

    for directory in (RAW, DRAFT, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    source = Image.open(SOURCE).convert("RGBA")
    assert source.size == (2172, 724)
    run = normalize_run(source)
    table = normalize_table(source)
    furniture = Image.new("RGBA", ROOM_SIZE)
    furniture.alpha_composite(run, (RUN_X, 105))
    furniture.alpha_composite(table, TABLE_BOUNDS[:2])

    background = make_background()
    room_without_bin = background.copy()
    room_without_bin.alpha_composite(furniture)
    room = room_without_bin.copy()
    bin_standard = Image.open(BIN_STANDARD).convert("RGBA")
    room.alpha_composite(bin_standard, BIN_CELL_ORIGIN)
    overlay = make_measurement_overlay(room)

    outputs: dict[str, dict[str, object]] = {}
    deliverables = {
        "kitchen-standard-background.png": background,
        "kitchen-standard-furniture-layer.png": furniture,
        "kitchen-standard-without-bin.png": room_without_bin,
        "kitchen-standard-foundation.png": room,
        "kitchen-standard-measurement-overlay.png": overlay,
        "standard-fitted-run.png": run,
        "standard-table-chair.png": table,
    }
    for i, name in enumerate(BAY_NAMES):
        # Fixed 84 x 120 transparent cells.  The crop includes a safety gutter
        # above every appliance and exactly one equal fitted bay.
        deliverables[f"bay-{name}.png"] = furniture.crop((RUN_X + i * BAY_WIDTH, 98, RUN_X + (i + 1) * BAY_WIDTH, 218))

    for filename, image in deliverables.items():
        path = RAW / filename
        save(image, path)
        outputs[filename] = {"sha256": sha(path), "pixels": list(image.size)}
        copy(path, ASSETS / filename)

    for source_path, filename in ((BIN_STANDARD, "bin-standard-approved.png"), (BIN_BROKEN, "bin-broken-approved.png")):
        copy(source_path, RAW / filename)
        copy(source_path, ASSETS / filename)
        outputs[filename] = {"sha256": sha(source_path), "pixels": [72, 72]}

    catalogue = {
        "set": SET,
        "version": 1,
        "status": "clean-slate-standard-foundation-awaiting-review",
        "scope": "standard-state foundation only; no alternate states or animation",
        "roomPixels": list(ROOM_SIZE),
        "logicalRoomPixels": list(LOGICAL_ROOM),
        "renderScale": SCALE,
        "geometry": {
            "fittedRunXExclusive": [RUN_X, RUN_RIGHT],
            "bayCount": BAY_COUNT,
            "bayWidthPixels": BAY_WIDTH,
            "bayOrder": list(BAY_NAMES),
            "worktopTopY": WORKTOP_TOP,
            "fasciaTopY": FASCIA_TOP,
            "rearWallFootLineY": FLOOR_LINE,
            "runVisibleBottomYExclusive": RUN_BOTTOM,
            "tableChairBoundsExclusive": list(TABLE_BOUNDS),
            "approvedBinCellTopLeft": list(BIN_CELL_ORIGIN),
        },
        "construction": {
            "oneUnifiedGeneratedMaster": True,
            "allNewAssetsDerivedFromSameMaster": True,
            "backgroundRedrawnDeterministically": True,
            "priorAssetPixelsUsed": ["accepted-bin-standard", "accepted-bin-broken-authority-card"],
            "sourceSha256": SOURCE_SHA,
            "sourceMasterSha256": MASTER_SHA,
            "sourceRunCropExclusive": [RUN_SOURCE_X[0], 200, RUN_SOURCE_X[1], 615],
            "sourceTableCropExclusive": list(TABLE_SOURCE),
        },
        "acceptedBinAuthority": {
            "standardSha256": BIN_STANDARD_SHA,
            "brokenSha256": BIN_BROKEN_SHA,
            "modified": False,
        },
        "outputs": outputs,
    }
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    register = {
        "set": SET,
        "status": "awaiting-standard-foundation-visual-review",
        "replaces": "all non-bin kitchen standard assets and rejected V32-V41 drafts",
        "preserves": "approved V28/V31 standard and broken bin cells byte-for-byte",
        "promotion": "none",
        "runtimeWiring": "unchanged",
        "nextGate": "user review of standard room only",
        "rollback": "Delete only Rebuild V1 source/raw/draft/review/archive/builder/verifier/docs files.",
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page())
    print(f"Built {SET}: {len(outputs)} deterministic PNG outputs")


if __name__ == "__main__":
    main()
