#!/usr/bin/env python3
"""Build the review-only Kitchen V20 fitted-galley appearance gate.

V20 deliberately separates two questions:

* the six isolated drawings establish the new storm-blue visual language; and
* the three-bay room proof establishes the fitted construction rule.

Nothing produced here is a runtime asset.  Exact production modules must be
assembled from the shared run-wide layers recorded in the V20 recipe after
Frank accepts this gate.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-fitted-galley-2026-10-17-v20"
RAW = ROOT / "art/raw/kitchen-fitted-galley-2026-10-17-v20"
DRAFT = ROOT / "art/drafts/kitchen-fitted-galley-2026-10-17-v20"
PUBLIC = ROOT / "public/keeper-review/kitchen-fitted-galley-v20"
ASSETS = PUBLIC / "assets"

SHEET_SOURCE = SOURCE / "isolated-six-appearance-source.png"
ROOM_SOURCE = SOURCE / "three-bay-fitted-run-source.png"

LP_PX = 4
BAY_LP = 21
BAY_PX = BAY_LP * LP_PX
ROOM_LP = (63, 56)
ROOM_PX = tuple(value * LP_PX for value in ROOM_LP)
FOOT_LINE_LP = 52
FOOT_LINE_PX = FOOT_LINE_LP * LP_PX
FOREGROUND_LP = 4

# The generated source is a regular 2 x 3 appearance sheet.  Thresholded alpha
# bounds remove only the extremely faint diffusion halo, not visible art.
APPEARANCES = [
    ("fridge", "Undercounter fridge", (0, 0, 512, 512)),
    ("oven", "Oven and grill", (512, 0, 1024, 512)),
    ("kettle", "Kettle counter", (1024, 0, 1536, 512)),
    ("toaster", "Toaster counter", (0, 512, 512, 1024)),
    ("mixer", "Mixing bowl and spoon", (512, 512, 1024, 1024)),
    ("sink", "Sink and faucet", (1024, 512, 1536, 1024)),
]

CELL_PX = (108, 120)
CELL_GUTTER_X = 12
CELL_GUTTER_BOTTOM = 12

# The joined source was generated at 1536 x 1024.  This crop contains the
# complete fitted run, including its two outer end caps, and scales uniformly
# to three exact 84-pixel bays.  The placement maps the cabinet baseline to the
# measured 52-lp rear-wall foot line.
RUN_CROP = (69, 0, 1467, 1024)
RUN_SOURCE_BASELINE_Y = 871


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


def trim_visible(image: Image.Image, threshold: int = 32) -> Image.Image:
    alpha = image.getchannel("A").point(lambda value: 255 if value >= threshold else 0)
    bounds = alpha.getbbox()
    if bounds is None:
        raise RuntimeError("appearance slot has no visible pixels")
    cropped = image.crop(bounds)
    # Remove invisible diffusion debris while preserving antialiased edge pixels.
    clean_alpha = cropped.getchannel("A").point(lambda value: 0 if value < 8 else value)
    cropped.putalpha(clean_alpha)
    return cropped


def build_appearance_sheet() -> tuple[Image.Image, dict]:
    source = Image.open(SHEET_SOURCE).convert("RGBA")
    sheet = Image.new("RGBA", (CELL_PX[0] * 3, CELL_PX[1] * 2), (0, 0, 0, 0))
    records: dict[str, dict] = {}
    for index, (stem, label, slot) in enumerate(APPEARANCES):
        art = trim_visible(source.crop(slot))
        target_height = round(art.height * BAY_PX / art.width)
        art = art.resize((BAY_PX, target_height), Image.Resampling.LANCZOS)
        x = (index % 3) * CELL_PX[0] + CELL_GUTTER_X
        y = (index // 3) * CELL_PX[1] + CELL_PX[1] - CELL_GUTTER_BOTTOM - art.height
        sheet.alpha_composite(art, (x, y))
        cell = sheet.crop(
            (
                (index % 3) * CELL_PX[0],
                (index // 3) * CELL_PX[1],
                (index % 3 + 1) * CELL_PX[0],
                (index // 3 + 1) * CELL_PX[1],
            )
        )
        save(cell, RAW / "appearance-cells" / f"{stem}.png")
        records[stem] = {
            "label": label,
            "cellPixels": list(CELL_PX),
            "appearanceWidthPx": BAY_PX,
            "appearanceWidthLp": BAY_LP,
            "appearanceHeightPx": target_height,
            "status": "appearance-reference-not-runtime-module",
        }
    return sheet, records


def build_room_proof() -> Image.Image:
    source = Image.open(ROOM_SOURCE).convert("RGB")
    run = source.crop(RUN_CROP)
    scale = ROOM_PX[0] / run.width
    resized_height = round(run.height * scale)
    run = run.resize((ROOM_PX[0], resized_height), Image.Resampling.LANCZOS)
    # Extend the room with the source's quiet upper-wall colour, then register
    # the fitted run's baseline exactly to the 52-lp foot line.
    background = source.getpixel((768, 180))
    room = Image.new("RGB", ROOM_PX, background)
    paste_y = round(FOOT_LINE_PX - RUN_SOURCE_BASELINE_Y * scale)
    room.paste(run, (0, paste_y))
    return room.convert("RGBA")


def write_page(data: dict) -> None:
    sheet = data["images"]["appearanceSheet"]
    room = data["images"]["roomProof"]
    html = f'''<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Kitchen V20 · fitted galley</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1160px;margin:auto;padding:22px}}h1,h2{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.checker{{background-color:#dce8e4;background-image:linear-gradient(45deg,#b9cac6 25%,transparent 25%),linear-gradient(-45deg,#b9cac6 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#b9cac6 75%),linear-gradient(-45deg,transparent 75%,#b9cac6 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0;border-radius:9px;padding:18px;overflow:auto}}img{{display:block;margin:auto;image-rendering:pixelated}}.sheet{{width:972px;max-width:none}}.room{{width:1008px;max-width:none}}.note{{border-left:4px solid #ff776d;padding:10px 12px;background:#30252a}}table{{width:100%;border-collapse:collapse}}th,td{{padding:7px;text-align:left;border-bottom:1px solid #315768}}code{{color:#98eee7}}@media(max-width:760px){{main{{padding:12px}}.checker{{justify-content:flex-start}}}}
</style><main><span class=tag>V20</span><span class=tag>Review only</span><span class=tag>Nothing wired</span><h1>Fitted lighthouse galley</h1><p>New storm-blue direction. Judge the visual family and the connected construction separately.</p><section><h2>1 · Six required appearances</h2><div class=checker><img class=sheet src="{sheet}" width=972 height=720 alt="Six isolated fitted galley appearances"></div><p>Top: fridge, oven/grill, kettle. Bottom: toaster, mixing bowl/spoon, sink. Each appearance is normalized to one 21-lp bay; transparent gutters are presentation safety space, not cabinet gaps.</p></section><section><h2>2 · Three-bay fitted construction</h2><div class=checker><img class=room src="{room}" width=1008 height=896 alt="Kettle, oven and sink joined into one fitted kitchen run"></div><p><strong>This is the construction authority:</strong> one continuous worktop, highlight, fascia and recessed plinth; only internal bay seams; end caps only at the complete run's two outer ends.</p></section><section><h2>Scale lock</h2><table><tr><th>Standard cabinet</th><td>60 cm = 21 lp = 84 source px</td></tr><tr><th>Kettle</th><td>18 cm = 6.3 lp; target envelope about 7 lp</td></tr><tr><th>Toaster</th><td>28 cm = 9.8 lp; target envelope about 10 lp</td></tr><tr><th>Room proof</th><td>63 × 56 lp; foot line 52 lp; 4-lp foreground channel</td></tr></table></section><p class=note><strong>Approval boundary:</strong> this is a new reversible appearance/construction gate. It does not approve, promote or wire kitchen art, change the live game, or alter Keeper animations and registers.</p></main>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)

    sheet, appearances = build_appearance_sheet()
    room = build_room_proof()
    save(sheet, RAW / "isolated-six-appearance-grid.png")
    save(room, RAW / "three-bay-fitted-room.png")
    save(sheet, ASSETS / "isolated-six-appearance-grid.png")
    save(room, ASSETS / "three-bay-fitted-room.png")

    prefix = "/keeper-review/kitchen-fitted-galley-v20/assets"
    data = {
        "version": 20,
        "status": "review-only-fitted-galley-gate",
        "images": {
            "appearanceSheet": f"{prefix}/isolated-six-appearance-grid.png",
            "roomProof": f"{prefix}/three-bay-fitted-room.png",
        },
        "grid": {
            "pixelsPerLp": LP_PX,
            "bayLp": BAY_LP,
            "bayPx": BAY_PX,
            "roomLp": list(ROOM_LP),
            "roomPx": list(ROOM_PX),
            "footLineLp": FOOT_LINE_LP,
            "foregroundLp": FOREGROUND_LP,
        },
        "physicalScale": {
            "cabinetCm": 60,
            "cabinetLp": 21,
            "cmPerLp": 60 / 21,
            "kettle": {"cm": 18, "calculatedLp": 18 / (60 / 21), "targetLp": 7},
            "toaster": {"cm": 28, "calculatedLp": 28 / (60 / 21), "targetLp": 10},
        },
        "appearances": appearances,
        "construction": {
            "carcassProjection": "orthographic-front-elevation",
            "illustrativeDepthPercent": 10,
            "worktopTopPlaneSourcePx": [3, 5],
            "worktopFasciaSourcePx": [2, 3],
            "underWorktopShadowSourcePx": [1, 2],
            "recessedPlinthSourcePx": [2, 3],
            "internalSeamSourcePx": [1, 2],
            "sharedAcrossWholeRun": ["worktop", "highlight", "fascia", "plinth"],
            "outerCapsOnly": True,
        },
        "source": {
            "isolatedSha256": sha(SHEET_SOURCE),
            "roomSha256": sha(ROOM_SOURCE),
            "generator": "OpenAI image generation, then deterministic Pillow normalization",
        },
    }
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    register = {
        "version": 20,
        "status": data["status"],
        "approved": False,
        "promoted": False,
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
        "fullStateFamilyBuilt": False,
        "rollback": "Delete only the V20 source/raw/draft/review directories and V20 scripts/docs.",
        "protectedSnapshots": {
            "kitchenV5": tree_sha(ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_page(data)
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "grid": data["grid"]}, indent=2))


if __name__ == "__main__":
    main()
