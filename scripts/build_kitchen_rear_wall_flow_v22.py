#!/usr/bin/env python3
"""Build Kitchen V22: one continuous, rear-wall registered fitted run.

V22 does not redraw or promote the V21 asset family. It corrects the room
assembly by using the kettle bay as the depth authority, placing each asset's
centre treatment into one shared six-bay carcass. V21 remains immutable.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
V21_RAW = ROOT / "art/raw/kitchen-final-assets-2026-10-17-v21"
V21_SOURCE = ROOT / "art/source/kitchen-final-assets-2026-10-17-v21"
SOURCE = ROOT / "art/source/kitchen-rear-wall-flow-2026-10-17-v22"
RAW = ROOT / "art/raw/kitchen-rear-wall-flow-2026-10-17-v22"
DRAFT = ROOT / "art/drafts/kitchen-rear-wall-flow-2026-10-17-v22"
PUBLIC = ROOT / "public/keeper-review/kitchen-rear-wall-flow-v22"
ASSETS = PUBLIC / "assets"

DENSITY = 4
BAY_PX = 84
RUN_X = 84
RUN_Y = 100
RUN_BAYS = 6
RUN_W = BAY_PX * RUN_BAYS
ROOM_SIZE = (772, 224)
FOOT_LINE = 208
KETTLE_BODY_BOTTOM = 199  # first clear row in the V21 kettle module

INK = "#061b38"
STORM_DARK = "#083d74"
STORM = "#07569b"
STORM_LIGHT = "#0b6eb2"
SEA_DARK = "#1aa3aa"
SEA = "#4bd7d1"
SEA_LIGHT = "#a8fff0"
WALL_TOP = (244, 221, 181, 255)
WALL_BOTTOM = (226, 194, 143, 255)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(file.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(file.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def room_background() -> Image.Image:
    room = Image.new("RGBA", ROOM_SIZE, WALL_TOP)
    draw = ImageDraw.Draw(room)
    for y in range(180):
        t = y / 179
        colour = tuple(round(a + (b - a) * t) for a, b in zip(WALL_TOP, WALL_BOTTOM))
        draw.line((0, y, ROOM_SIZE[0], y), fill=colour)
    draw.rectangle((0, 180, ROOM_SIZE[0], 183), fill="#f3e6c8")
    draw.rectangle((0, 184, ROOM_SIZE[0], 188), fill="#6f594a")
    draw.rectangle((0, 189, ROOM_SIZE[0], 223), fill="#a95029")
    for y, colour in ((195, "#d47a3c"), (207, "#7e351f"), (218, "#d47a3c")):
        draw.line((0, y, ROOM_SIZE[0], y), fill=colour, width=2)
    return room


def module(name: str) -> Image.Image:
    image = Image.open(V21_RAW / f"{name}.png").convert("RGBA")
    if name == "basic-oven":
        image = image.crop((12, 0, 96, 120))
    if image.size != (84, 120):
        raise RuntimeError(f"{name} is {image.size}, expected one 84 x 120-px bay")
    return image


def draw_shared_carcass(room: Image.Image) -> None:
    """Draw one carcass; internal lines are divisions, never side panels."""
    draw = ImageDraw.Draw(room)
    left = RUN_X
    right = RUN_X + RUN_W - 1

    # One uninterrupted rear-wall worktop and fascia.
    draw.rectangle((left, 134, right, 136), fill=INK)
    draw.rectangle((left, 137, right, 143), fill=SEA)
    draw.line((left, 138, right, 138), fill=SEA_LIGHT)
    draw.rectangle((left, 144, right, 149), fill=SEA_DARK)
    draw.line((left, 150, right, 150), fill=INK)

    # One common front plane terminating at the kettle-authority bottom row.
    draw.rectangle((left, 151, right, 198), fill=STORM)
    draw.line((left, 152, right, 152), fill=STORM_LIGHT)
    draw.line((left, 198, right, 198), fill=INK)

    # A single recessed toe-kick keeps the run on the 52-lp foot line while
    # preserving the kettle bay's shallower/rearward body reading.
    draw.rectangle((left + 4, 199, right - 4, 206), fill=STORM_DARK)
    draw.line((left + 4, 199, right - 4, 199), fill=INK)
    draw.line((left + 4, 207, right - 4, 207), fill=INK)

    # Outer caps exist only at the full run ends.
    draw.rectangle((left, 151, left + 3, 198), fill=INK)
    draw.line((left + 4, 151, left + 4, 198), fill=STORM_LIGHT)
    draw.rectangle((right - 3, 151, right, 198), fill=INK)
    draw.line((right - 4, 151, right - 4, 198), fill=STORM_LIGHT)


def overlay_treatment(room: Image.Image, treatment: Image.Image, bay: int) -> None:
    """Keep a bay's prop/front detail, excluding its freestanding side shell."""
    # Rows 0:99 retain the appliance and the complete cabinet face only as far
    # forward as the kettle body. The 6-px side strips belong to the shared run.
    centre = treatment.crop((6, 0, 78, 99))
    room.alpha_composite(centre, (RUN_X + bay * BAY_PX + 6, RUN_Y))


def finish_shared_structure(room: Image.Image) -> None:
    draw = ImageDraw.Draw(room)
    left = RUN_X
    right = RUN_X + RUN_W - 1

    # Restore truly continuous structural bands after the per-bay treatments.
    draw.line((left, 134, right, 134), fill=INK)
    draw.line((left, 138, right, 138), fill=SEA_LIGHT)
    draw.line((left, 149, right, 149), fill=SEA_DARK)
    draw.line((left, 150, right, 150), fill=INK)
    draw.line((left + 4, 199, right - 4, 199), fill=INK)
    draw.line((left + 4, 207, right - 4, 207), fill=INK)

    # Five 2-px front-elevation divisions. They do not cross the worktop or
    # plinth and therefore cannot read as six freestanding end panels.
    for bay in range(1, RUN_BAYS):
        x = left + bay * BAY_PX
        draw.line((x - 1, 151, x - 1, 198), fill=INK)
        draw.line((x, 151, x, 198), fill=STORM_LIGHT)


def build_room(oven_name: str) -> Image.Image:
    room = room_background()
    draw_shared_carcass(room)
    names = ["fridge", "kettle", "toaster", oven_name, "mixer", "sink"]
    for bay, name in enumerate(names):
        overlay_treatment(room, module(name), bay)
    finish_shared_structure(room)

    bin_cell = Image.open(V21_RAW / "pedal-bin.png").convert("RGBA")
    bin_art = bin_cell.crop((12, 12, 52, 64))
    chair = Image.open(V21_RAW / "chair.png").convert("RGBA")
    table = Image.open(V21_RAW / "table.png").convert("RGBA")
    room.alpha_composite(bin_art, ((BAY_PX - bin_art.width) // 2, FOOT_LINE - bin_art.height))
    chair_x = RUN_X + RUN_W + 16
    room.alpha_composite(chair, (chair_x, FOOT_LINE - chair.height))
    room.alpha_composite(table, (chair_x + 43, FOOT_LINE - table.height))
    return room


def build_alignment_guide(room: Image.Image) -> Image.Image:
    guide = room.copy()
    draw = ImageDraw.Draw(guide, "RGBA")
    draw.line((RUN_X, 134, RUN_X + RUN_W - 1, 134), fill=(255, 216, 77, 255), width=1)
    draw.line((RUN_X, KETTLE_BODY_BOTTOM, RUN_X + RUN_W - 1, KETTLE_BODY_BOTTOM), fill=(114, 226, 165, 255), width=1)
    draw.line((RUN_X, FOOT_LINE, RUN_X + RUN_W - 1, FOOT_LINE), fill=(99, 216, 255, 255), width=1)
    for bay in range(RUN_BAYS + 1):
        x = RUN_X + bay * BAY_PX
        draw.line((x, 126, x, FOOT_LINE), fill=(255, 255, 255, 150), width=1)
    return guide


def write_page() -> None:
    prefix = "/keeper-review/kitchen-rear-wall-flow-v22/assets"
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V22 · rear-wall continuous run</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1500px;margin:auto;padding:22px}}h1,h2{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.scroll{{overflow:auto;background:#061016;border-radius:9px;padding:12px}}img{{display:block;image-rendering:auto}}.room{{width:2316px;height:672px}}.comparison{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}article{{background:#091e29;border:1px solid #315768;border-radius:11px;padding:12px;overflow:auto}}article img{{width:1512px;height:336px;max-width:none}}button{{font:inherit;padding:7px 12px;border-radius:7px;border:1px solid #78d8cf;background:#123c4a;color:#edf8f5}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}@media(max-width:800px){{main{{padding:12px}}.comparison{{grid-template-columns:1fr}}}}
</style></head><body><main><span class="tag">V22</span><span class="tag">V21 assets preserved</span><span class="tag">Rear-wall depth corrected</span><h1>One continuous fitted galley</h1><p class="note"><strong>Corrected:</strong> every fitted unit now uses the kettle bay's rear-wall depth. The six 21-lp bays sit exactly edge-to-edge inside one 126-lp carcass, with one uninterrupted worktop, one recessed plinth and end panels only at the two outside edges.</p><p id="loading">Loading and decoding review media…</p>
<section><h2>Full kitchen · corrected basic set</h2><p><button id="basic" disabled>Basic oven</button> <button id="upgrade" disabled>Upgrade 1 oven</button> <strong id="mode">Basic kitchen</strong></p><div class="scroll"><img data-media id="room" class="room" src="{prefix}/full-kitchen.png" width="2316" height="672" alt="Full lighthouse kitchen with one continuous rear-wall fitted run, pedal bin, chair and table"></div><p>Nothing has moved independently: bin, table and chair retain V21 placement; each appliance remains in its existing 21-lp bay. Only the fitted-run construction and depth registration changed.</p></section>
<section><h2>Before / corrected construction</h2><div class="comparison"><article><h3>V21 · separate complete cabinet drawings</h3><img data-media src="{prefix}/v21-before.png" width="1512" height="336" alt="V21 kitchen before rear-wall flow correction"></article><article><h3>V22 · one carcass, six treatments</h3><img data-media src="{prefix}/v22-after.png" width="1512" height="336" alt="V22 continuous rear-wall galley"></article></div></section>
<section><h2>Registration proof</h2><div class="scroll"><img data-media class="room" src="{prefix}/alignment-guide.png" width="2316" height="672" alt="Guide overlay showing six equal bays, common worktop, kettle-authority body line and foot line"></div><p>White = exact 21-lp bay boundaries. Yellow = one rear-wall worktop line. Green = the kettle-authority body depth shared by all bays. Cyan = 52-lp foot line; the common recessed toe-kick reaches it while 4 lp of foreground stays clear.</p></section>
<p class="warn"><strong>Reversible review boundary:</strong> V22 changes only the new room proof and its review metadata. V20 and V21 source, raw art and review pages remain byte-identical; runtime sprites, Final art and Keeper art remain untouched.</p>
</main><script>const prefix='{prefix}/',room=document.querySelector('#room'),mode=document.querySelector('#mode'),buttons=[document.querySelector('#basic'),document.querySelector('#upgrade')],files=['full-kitchen.png','full-kitchen-upgrade1.png','v21-before.png','v22-after.png','alignment-guide.png'];Promise.all(files.map(name=>new Promise((ok,bad)=>{{const image=new Image;image.onload=()=>{{const decoded=image.decode?.();decoded?decoded.then(ok).catch(ok):ok()}};image.onerror=()=>bad(new Error('Could not load '+name));image.src=prefix+name}}))).then(()=>{{document.body.classList.add('ready');buttons.forEach(button=>button.disabled=false);document.querySelector('#loading').textContent='All '+files.length+' unique review images loaded and decoded.'}}).catch(error=>document.querySelector('#loading').textContent='Review locked: '+error.message);buttons[0].onclick=()=>{{room.src=prefix+'full-kitchen.png';mode.textContent='Basic kitchen'}};buttons[1].onclick=()=>{{room.src=prefix+'full-kitchen-upgrade1.png';mode.textContent='Upgrade 1 kitchen'}}</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)

    basic = build_room("basic-oven")
    upgrade = build_room("upgrade-oven")
    guide = build_alignment_guide(basic)
    before = Image.open(V21_RAW / "full-kitchen.png").convert("RGBA")
    compare_box = (RUN_X, 96, RUN_X + RUN_W, FOOT_LINE)
    outputs = {
        "full-kitchen.png": basic,
        "full-kitchen-upgrade1.png": upgrade,
        "alignment-guide.png": guide,
        "v21-before.png": before.crop(compare_box),
        "v22-after.png": basic.crop(compare_box),
    }
    for name, image in outputs.items():
        save(image, RAW / name)
        save(image, ASSETS / name)

    data = {
        "version": 22,
        "status": "rear-wall-flow-correction-awaiting-visual-acceptance",
        "predecessor": "kitchen-final-assets-v21",
        "room": {"lp": [193, 56], "pixels": list(ROOM_SIZE), "footLineLp": 52, "foregroundLp": 4},
        "fittedRun": {
            "bays": RUN_BAYS,
            "bayWidthLp": 21,
            "runWidthLp": 126,
            "startLp": RUN_X / DENSITY,
            "worktopYpx": 134,
            "bodyBottomYpx": KETTLE_BODY_BOTTOM,
            "depthAuthority": "V21 kettle bay",
            "construction": "one shared carcass; per-bay centre treatments; outer end caps only",
        },
        "unchanged": ["asset order", "asset scale", "pedal bin", "table", "chair", "oven tiers", "room", "Keeper art", "runtime"],
        "outputs": {name: {"sha256": sha(RAW / name), "size": list(image.size)} for name, image in outputs.items()},
        "sources": {
            "v21RawTreeSha256": tree_sha(V21_RAW),
            "v21SourceTreeSha256": tree_sha(V21_SOURCE),
            "continuousRunReferenceSha256": sha(SOURCE / "continuous-run-reference.png"),
            "continuousRunReferenceUse": "visual intent only; production room is deterministic pixel assembly",
        },
    }
    (DRAFT / "layout-catalogue.json").write_text(json.dumps(data, indent=2) + "\n")
    register = {
        "version": 22,
        "status": data["status"],
        "approved": False,
        "promoted": False,
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
        "v21Preserved": True,
        "rollback": "Delete only V22 source/raw/draft/review files, its builder/verifier/docs and archive set; V20 and V21 remain byte-identical.",
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
