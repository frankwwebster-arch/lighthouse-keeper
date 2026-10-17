#!/usr/bin/env python3
"""Build the reversible Kitchen V21 complete fitted-galley review set.

V21 keeps V20 as immutable visual/construction authority, adds the three
items requested in Frank's V20 review, and proves every finished asset in one
193 x 56-lp kitchen. Nothing here is promoted to the runtime sprite manifest.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
V20_RAW = ROOT / "art/raw/kitchen-fitted-galley-2026-10-17-v20"
V20_SOURCE = ROOT / "art/source/kitchen-fitted-galley-2026-10-17-v20"
SOURCE = ROOT / "art/source/kitchen-final-assets-2026-10-17-v21"
RAW = ROOT / "art/raw/kitchen-final-assets-2026-10-17-v21"
DRAFT = ROOT / "art/drafts/kitchen-final-assets-2026-10-17-v21"
PUBLIC = ROOT / "public/keeper-review/kitchen-final-assets-v21"
ASSETS = PUBLIC / "assets"
SEATED_KEEPER = ROOT / "review-archive/objects/82/8226a15137fc6973103131a355b215e6df7cfb94e0349f1962013ffb1593fc2b.png"

DENSITY = 4
BAY_LP = 21
BAY_PX = BAY_LP * DENSITY
FOOT_LINE_LP = 52
FOOT_LINE_PX = FOOT_LINE_LP * DENSITY
ROOM_LP = (193, 56)
ROOM_PX = tuple(value * DENSITY for value in ROOM_LP)

INK = "#061b38"
STORM_DARK = "#083d74"
STORM = "#07569b"
SEA_DARK = "#1aa3aa"
SEA = "#4bd7d1"
SEA_LIGHT = "#a8fff0"
COPPER = "#dd6816"
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


def clean(image: Image.Image, threshold: int = 8) -> Image.Image:
    image = image.convert("RGBA")
    alpha = image.getchannel("A")
    bounds = alpha.point(lambda value: 255 if value >= threshold else 0).getbbox()
    if bounds is None:
        raise RuntimeError("image has no visible pixels")
    image = image.crop(bounds)
    image.putalpha(image.getchannel("A").point(lambda value: 0 if value < threshold else value))
    return image


def resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def cell(image: Image.Image, size: tuple[int, int], bottom_gutter: int = 12) -> Image.Image:
    output = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (size[0] - image.width) // 2
    y = size[1] - bottom_gutter - image.height
    if x < 1 or y < 1:
        raise RuntimeError(f"asset {image.size} does not fit safely inside cell {size}")
    output.alpha_composite(image, (x, y))
    return output


def v20_module(name: str) -> Image.Image:
    # V20's 108 x 120 review cell has a 12-px transparent horizontal gutter.
    # Cropping only that gutter preserves the exact 84-px / 21-lp module.
    source = Image.open(V20_RAW / "appearance-cells" / f"{name}.png").convert("RGBA")
    return source.crop((12, 0, 96, 120))


def normalize_basic_oven() -> tuple[Image.Image, Image.Image]:
    source = clean(Image.open(SOURCE / "basic-oven-source.png"))
    art = resize(source, (BAY_PX, 77))
    return art, cell(art, (108, 120))


def normalize_bin() -> tuple[Image.Image, Image.Image]:
    source = clean(Image.open(SOURCE / "pedal-bin-source.png"))
    art = resize(source, (40, 52))
    return art, cell(art, (64, 76))


def normalize_table_chair() -> tuple[Image.Image, Image.Image, Image.Image]:
    source = Image.open(SOURCE / "table-chair-source.png").convert("RGBA")
    # The generated pair deliberately keeps the two objects disconnected.
    # These source windows are pinned by the verifier and normalized into the
    # exact V6 support geometry rather than trusted as generated measurements.
    chair_source = clean(source.crop((151, 163, 580, 848)))
    table_source = clean(source.crop((590, 330, 1420, 848)))

    # V6: seat support 7.75 lp above floor; chair top 12 lp above support;
    # total side depth 8.625 lp. Piecewise vertical scaling locks the support.
    split = round(chair_source.height * 355 / 685)
    upper = resize(chair_source.crop((0, 0, chair_source.width, split)), (35, 48))
    lower = resize(chair_source.crop((0, split, chair_source.width, chair_source.height)), (35, 31))
    chair = Image.new("RGBA", (35, 79), (0, 0, 0, 0))
    chair.alpha_composite(upper, (0, 0))
    chair.alpha_composite(lower, (0, 48))

    # The seated Prime's hands land at 14.5 lp. The 1.5-lp top is retained in
    # the art, with a 20-lp one-person span and a common floor baseline.
    table = resize(table_source, (80, 58))
    pair = Image.new("RGBA", (168, 96), (0, 0, 0, 0))
    pair.alpha_composite(chair, (16, 96 - 12 - chair.height))
    pair.alpha_composite(table, (59, 96 - 12 - table.height))
    return chair, table, pair


def room_background() -> Image.Image:
    room = Image.new("RGBA", ROOM_PX, WALL_TOP)
    draw = ImageDraw.Draw(room)
    wall_end = 180
    for y in range(wall_end):
        t = y / max(1, wall_end - 1)
        colour = tuple(round(a + (b - a) * t) for a, b in zip(WALL_TOP, WALL_BOTTOM))
        draw.line((0, y, ROOM_PX[0], y), fill=colour)
    draw.rectangle((0, 180, ROOM_PX[0], 183), fill="#f3e6c8")
    draw.rectangle((0, 184, ROOM_PX[0], 188), fill="#6f594a")
    draw.rectangle((0, 189, ROOM_PX[0], 223), fill="#a95029")
    for y, colour in ((195, "#d47a3c"), (207, "#7e351f"), (218, "#d47a3c")):
        draw.line((0, y, ROOM_PX[0], y), fill=colour, width=2)
    return room


def build_full_room(
    modules: dict[str, Image.Image],
    bin_art: Image.Image,
    chair: Image.Image,
    table: Image.Image,
    oven: Image.Image | None = None,
) -> Image.Image:
    room = room_background()
    run_x = BAY_PX
    order = ["fridge", "kettle", "toaster", "basic-oven", "mixer", "sink"]
    for index, name in enumerate(order):
        module = oven if name == "basic-oven" and oven is not None else modules[name]
        room.alpha_composite(module, (run_x + index * BAY_PX, FOOT_LINE_PX - 108))

    # Join only the worktop and plinth boundaries at internal seams. This keeps
    # V20's complete drawings intact while removing the freestanding-card gaps.
    draw = ImageDraw.Draw(room)
    for index in range(1, len(order)):
        x = run_x + index * BAY_PX
        draw.rectangle((x - 2, 134, x + 1, 136), fill=INK)
        draw.rectangle((x - 2, 137, x + 1, 143), fill=SEA)
        draw.line((x - 2, 139, x + 1, 139), fill=SEA_LIGHT)
        draw.rectangle((x - 2, 144, x + 1, 150), fill=SEA_DARK)
        draw.rectangle((x - 2, 201, x + 1, 207), fill=STORM_DARK)

    room.alpha_composite(bin_art, ((BAY_PX - bin_art.width) // 2, FOOT_LINE_PX - bin_art.height))
    chair_x = run_x + len(order) * BAY_PX + 16
    room.alpha_composite(chair, (chair_x, FOOT_LINE_PX - chair.height))
    room.alpha_composite(table, (chair_x + 43, FOOT_LINE_PX - table.height))
    return room


def build_fit_proof(chair: Image.Image, table: Image.Image) -> Image.Image:
    stage = Image.new("RGBA", (172 * DENSITY, 56 * DENSITY), "#16303a")
    draw = ImageDraw.Draw(stage)
    draw.rectangle((0, FOOT_LINE_PX, stage.width, stage.height), fill="#1a272d")
    draw.line((0, FOOT_LINE_PX, stage.width, FOOT_LINE_PX), fill="#90a4ae")
    chair_x = round(75.125 * DENSITY)
    table_x = round((75.125 + 8.625 + 2) * DENSITY)
    stage.alpha_composite(chair, (chair_x, FOOT_LINE_PX - chair.height))
    keeper = resize(Image.open(SEATED_KEEPER).convert("RGBA"), (32 * DENSITY, 40 * DENSITY))
    stage.alpha_composite(keeper, ((86 - 16) * DENSITY, (FOOT_LINE_LP - 40) * DENSITY))
    stage.alpha_composite(table, (table_x, FOOT_LINE_PX - table.height))
    draw = ImageDraw.Draw(stage)
    draw.line((0, FOOT_LINE_PX - 31, stage.width, FOOT_LINE_PX - 31), fill="#ffd84d", width=1)
    draw.line((0, FOOT_LINE_PX - 58, stage.width, FOOT_LINE_PX - 58), fill="#63d8ff", width=1)
    return stage


def write_page(data: dict) -> None:
    prefix = "/keeper-review/kitchen-final-assets-v21/assets"
    cards = "".join(
        f'<article><h3>{record["label"]}</h3><div class="checker"><img src="{prefix}/{record["file"]}" alt="{record["label"]}"></div><p>{record["note"]}</p></article>'
        for record in data["assets"]
    )
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V21 · final asset set</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1500px;margin:auto;padding:22px}}h1,h2,h3{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.scroll{{overflow:auto;background:#061016;border-radius:9px;padding:12px}}img{{display:block;image-rendering:auto}}.room{{width:2316px;height:672px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}}article{{background:#091e29;border:1px solid #315768;border-radius:11px;padding:12px}}.checker{{min-height:260px;display:flex;align-items:end;justify-content:center;background-color:#dce8e4;background-image:linear-gradient(45deg,#b9cac6 25%,transparent 25%),linear-gradient(-45deg,#b9cac6 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#b9cac6 75%),linear-gradient(-45deg,transparent 75%,#b9cac6 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0;border-radius:8px;padding:16px;overflow:auto}}.checker img{{max-width:none;transform:scale(3);transform-origin:center bottom;margin-bottom:24px}}.comparison{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.comparison img{{margin:auto;max-width:100%;height:360px;object-fit:contain}}.fit{{width:1376px;height:448px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:7px;text-align:left;border-bottom:1px solid #315768}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}@media(max-width:800px){{main{{padding:12px}}.comparison{{grid-template-columns:1fr}}}}
</style></head><body><main><span class="tag">V21</span><span class="tag">Complete final candidate</span><span class="tag">V20 preserved</span><h1>Complete fitted lighthouse kitchen</h1><p class="note"><strong>All requested V20 changes are present:</strong> a compact single-door basic oven, the V20 double oven retained as Upgrade 1, a simple standalone pedal bin, and a one-person table with exactly one V6-sized chair.</p><p id="loading">Loading and decoding review media…</p>
<section><h2>Full kitchen · every asset in situ</h2><p><button id="basicRoom" disabled>Basic oven</button> <button id="upgradeRoom" disabled>Upgrade 1 oven</button> <strong id="roomMode">Basic kitchen</strong></p><div class="scroll"><img data-media id="roomImage" class="room" src="{prefix}/full-kitchen.png" width="2316" height="672" alt="Full fitted lighthouse kitchen with pedal bin, fridge, kettle, toaster, basic oven, mixing bowl, sink and one-person table with one chair"></div><p>Left to right: standalone pedal bin; fridge; kettle; toaster; selected oven tier; mixing bowl; sink; table for one and its single chair. The six cabinet bays share one fitted run and the last 4 lp remain clear foreground floor.</p></section>
<section><h2>Basic oven and Upgrade 1</h2><div class="comparison"><article><h3>Basic · now</h3><img data-media src="{prefix}/basic-oven.png" alt="Narrow single-door basic oven"><p>Narrow 15-lp appliance inset inside the unchanged 21-lp cabinet frame; one door, compact hob.</p></article><article><h3>Upgrade 1 · retained from V20</h3><img data-media src="{prefix}/upgrade-oven.png" alt="V20 double oven retained as first upgrade"><p>The larger V20 oven remains byte-derived from V20 and is no longer the basic tier.</p></article></div></section>
<section><h2>Chair and tabletop fit · V6 geometry</h2><div class="scroll"><img data-media class="fit" src="{prefix}/table-chair-fit.png" width="1376" height="448" alt="Seated Keeper fitted to the single chair and table"></div><table><tr><th>Chair support</th><td>7.75 lp above floor</td></tr><tr><th>Chair depth</th><td>8.625 lp</td></tr><tr><th>Seat-to-shin clearance</th><td>0.5 lp</td></tr><tr><th>Tabletop</th><td>14.5 lp above floor; 1.5-lp top</td></tr><tr><th>Table span</th><td>20 lp; one place only</td></tr></table><p>Yellow = V6 seat support. Cyan = tabletop at the seated hand line. The chair is behind the Keeper and the table is in front, preserving the action draw stack.</p></section>
<section><h2>Final asset catalogue</h2><div class="grid">{cards}</div></section>
<p class="warn"><strong>Delivery boundary:</strong> this completes the review asset family and full-room proof without overwriting V20, changing Keeper art, or wiring sprites into the live game. Promotion remains a separate explicit step after visual acceptance.</p>
</main><script>const prefix='{prefix}/',room=document.querySelector('#roomImage'),mode=document.querySelector('#roomMode'),controls=[document.querySelector('#basicRoom'),document.querySelector('#upgradeRoom')],preload=['full-kitchen.png','full-kitchen-upgrade1.png',...new Set([...document.querySelectorAll('[data-media],.checker img')].map(i=>i.src.split('/').pop()))];Promise.all(preload.map(name=>new Promise((ok,bad)=>{{const i=new Image;i.onload=()=>{{const d=i.decode?.();d?d.then(ok).catch(ok):ok()}};i.onerror=()=>bad(new Error('Could not load '+name));i.src=prefix+name}}))).then(()=>{{document.body.classList.add('ready');controls.forEach(b=>b.disabled=false);document.querySelector('#loading').textContent='All '+new Set(preload).size+' unique review images loaded and decoded.'}}).catch(e=>document.querySelector('#loading').textContent='Review locked: '+e.message);controls[0].onclick=()=>{{room.src=prefix+'full-kitchen.png';mode.textContent='Basic kitchen';room.alt='Full kitchen with compact basic oven'}};controls[1].onclick=()=>{{room.src=prefix+'full-kitchen-upgrade1.png';mode.textContent='Upgrade 1 kitchen';room.alt='Full kitchen with V20 double oven as Upgrade 1'}}</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)

    basic_oven_art, basic_oven_cell = normalize_basic_oven()
    bin_art, bin_cell = normalize_bin()
    chair, table, table_chair = normalize_table_chair()
    modules = {
        "fridge": v20_module("fridge"),
        "basic-oven": basic_oven_cell.crop((12, 0, 96, 120)),
        "kettle": v20_module("kettle"),
        "toaster": v20_module("toaster"),
        "mixer": v20_module("mixer"),
        "sink": v20_module("sink"),
    }
    upgrade_oven = v20_module("oven")
    full_room = build_full_room(modules, bin_art, chair, table)
    upgrade_room = build_full_room(modules, bin_art, chair, table, upgrade_oven)
    fit_proof = build_fit_proof(chair, table)

    outputs = {
        "fridge.png": modules["fridge"],
        "basic-oven.png": basic_oven_cell,
        "upgrade-oven.png": upgrade_oven,
        "kettle.png": modules["kettle"],
        "toaster.png": modules["toaster"],
        "mixer.png": modules["mixer"],
        "sink.png": modules["sink"],
        "pedal-bin.png": bin_cell,
        "table-chair.png": table_chair,
        "chair.png": chair,
        "table.png": table,
        "full-kitchen.png": full_room,
        "full-kitchen-upgrade1.png": upgrade_room,
        "table-chair-fit.png": fit_proof,
    }
    for name, image in outputs.items():
        save(image, RAW / name)
        save(image, ASSETS / name)

    records = [
        ("Pedal bin", "pedal-bin.png", "Standalone 10 × 13-lp bin; closed lid and copper foot pedal."),
        ("Undercounter fridge", "fridge.png", "Exact V20 appearance, one 21-lp fitted bay."),
        ("Kettle counter", "kettle.png", "Exact V20 appearance; kettle remains about 7 lp."),
        ("Toaster counter", "toaster.png", "Exact V20 appearance; toaster remains about 10 lp."),
        ("Basic oven", "basic-oven.png", "New compact single-door 15-lp appliance inset in one 21-lp bay."),
        ("Mixing counter", "mixer.png", "Exact V20 appearance."),
        ("Sink", "sink.png", "Exact V20 short-faucet appearance."),
        ("Table for one + one chair", "table-chair.png", "V6 chair support/depth with a 14.5-lp one-person tabletop."),
        ("Oven Upgrade 1", "upgrade-oven.png", "Former V20 oven retained as the first upgrade tier."),
    ]
    data = {
        "version": 21,
        "status": "complete-final-candidate-awaiting-visual-acceptance",
        "base": "kitchen-fitted-galley-v20",
        "room": {"lp": list(ROOM_LP), "pixels": list(ROOM_PX), "footLineLp": FOOT_LINE_LP, "foregroundLp": 4},
        "ovenTiers": {
            "basic": {"cabinetBayLp": 21, "applianceInsetLp": 15, "doors": 1},
            "upgrade1": {"source": "V20 oven/grill appearance", "doors": 2},
        },
        "pedalBin": {"standalone": True, "widthLp": 10, "heightLp": 13},
        "tableForOne": {
            "chairs": 1,
            "chairSeatSupportLp": 7.75,
            "chairDepthLp": 8.625,
            "shinClearanceLp": 0.5,
            "tabletopLp": 14.5,
            "tabletopThicknessLp": 1.5,
            "tableWidthLp": 20,
            "authority": "/keeper-review/keeper-prime-sit-stand-side-v6",
        },
        "assets": [{"label": label, "file": file, "note": note, "sha256": sha(RAW / file)} for label, file, note in records],
        "review": {"fullRoom": "full-kitchen.png", "upgradeRoom": "full-kitchen-upgrade1.png", "fitProof": "table-chair-fit.png"},
        "sources": {
            path.name: {"sha256": sha(path), "generator": "OpenAI built-in image generation"}
            for path in sorted(SOURCE.glob("*.png"))
        },
    }
    (DRAFT / "asset-catalogue.json").write_text(json.dumps(data, indent=2) + "\n")
    register = {
        "version": 21,
        "status": data["status"],
        "completeAssetSet": True,
        "approved": False,
        "promoted": False,
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
        "predecessor": {
            "commit": "2d67163",
            "v20SourceTreeSha256": tree_sha(V20_SOURCE),
            "v20RawTreeSha256": tree_sha(V20_RAW),
        },
        "protectedSnapshots": {
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "sitStandV6KeeperFrame": sha(SEATED_KEEPER),
        },
        "rollback": "Delete only V21 source/raw/draft/review files, V21 scripts/docs and its archive manifest/objects; V20 remains byte-identical.",
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_page(data)
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "roomLp": ROOM_LP, "assets": len(records)}, indent=2))


if __name__ == "__main__":
    main()
