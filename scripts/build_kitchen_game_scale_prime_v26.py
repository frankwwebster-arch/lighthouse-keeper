#!/usr/bin/env python3
"""Build Kitchen V26 game-scale proofs with Prime Keeper in situ."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "art/raw/kitchen-game-scale-prime-2026-10-17-v26"
DRAFT = ROOT / "art/drafts/kitchen-game-scale-prime-2026-10-17-v26"
PUBLIC = ROOT / "public/keeper-review/kitchen-game-scale-prime-v26"
ASSETS = PUBLIC / "assets"
ROOM = ROOT / "art/raw/kitchen-narrower-bin-2026-10-17-v25/full-kitchen-narrower-bin.png"
PRIME_FRONT = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png"
PRIME_SEATED_BACK = ROOT / "art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-back_f01.png"

ROOM_SHA = "175d77c063297c435eab468f297c369f79e5491b89bbdd2b03400d31cd334f4a"
PRIME_FRONT_SHA = "a9a5c37fe72221992ec499fa3096fdd0581977b4ac03ff7788da2af411107a2e"
PRIME_SEATED_BACK_SHA = "28a879bcee43c6d06330d05fb3cd74b4098b2ccce38ce41d15117f5fb0be5167"

ROOM_CROP = (0, 45, 2064, 643)
ROOM_LOGICAL = (193, 56)
DENSITY = 4
GAME_SIZE = (ROOM_LOGICAL[0] * DENSITY, ROOM_LOGICAL[1] * DENSITY)
PRIME_LOGICAL = (32, 40)
PRIME_SIZE = (PRIME_LOGICAL[0] * DENSITY, PRIME_LOGICAL[1] * DENSITY)
STANDING_TOP_LEFT = (362, 64)
SEATED_TOP_LEFT = (655, 64)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def write_page() -> None:
    prefix = "/keeper-review/kitchen-game-scale-prime-v26/assets"
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V26 · game-scale Prime proofs</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1100px;margin:auto;padding:22px}}h1,h2{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.stage{{overflow:auto;background:#02080b;border-radius:9px;padding:16px}}img{{display:block}}.native{{width:772px;height:224px;max-width:none}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}table{{border-collapse:collapse;width:100%}}th,td{{text-align:left;border-bottom:1px solid #315768;padding:8px}}code{{color:#9af1e9}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}
</style></head><body><main><span class="tag">V26</span><span class="tag">V25 preserved</span><span class="tag">Native game presentation</span><h1>Kitchen scale · Prime Keeper in situ</h1><p class="note">Each image below is displayed at its actual proposed game presentation size: <strong>772 × 224 px</strong>, representing a <strong>193 × 56-lp</strong> room at <strong>4 px/lp</strong>. Prime uses a <strong>32 × 40-lp</strong> cell, rendered here at <strong>128 × 160 px</strong>.</p><p id="loading">Loading and decoding review media…</p>
<section><h2>Prime standing at the fitted run</h2><div class="stage"><img data-media class="native" src="{prefix}/kitchen-game-scale-prime-standing.png" width="772" height="224" alt="Kitchen at game scale with Prime Keeper standing in front of the fitted run"></div><p>The approved permanent Prime Master is reduced from density 8 to the same density-4 presentation as the room and anchored on the 56-lp floor line.</p></section>
<section><h2>Prime seated at the one-person table</h2><div class="stage"><img data-media class="native" src="{prefix}/kitchen-game-scale-prime-seated-back.png" width="772" height="224" alt="Kitchen at game scale with the rear-facing seated Prime Keeper registered to the table chair"></div><p>The current exact rear-facing seated Prime pose shares the same 32 × 40-lp cell and is centred on the chair/table axis with its seat contact at 11 lp above the floor. This is a scale and placement proof; final chair/character occlusion remains a later runtime-layer decision.</p></section>
<section><h2>Room alone at the same scale</h2><div class="stage"><img data-media class="native" src="{prefix}/kitchen-game-scale-room.png" width="772" height="224" alt="Kitchen V25 normalized to the proposed game presentation"></div></section>
<section><h2>Measured contract</h2><table><tr><th>Element</th><th>Logical size</th><th>Displayed size</th></tr><tr><td>Complete kitchen room</td><td>193 × 56 lp</td><td>772 × 224 px</td></tr><tr><td>Prime cell</td><td>32 × 40 lp</td><td>128 × 160 px</td></tr><tr><td>Standard cabinet bay</td><td>21 lp</td><td>84 px</td></tr><tr><td>Prime floor anchor</td><td>y = 56 lp</td><td>y = 224 px</td></tr><tr><td>Seated contact</td><td>11 lp above floor</td><td>44 px above floor</td></tr></table></section>
<p class="warn"><strong>Version boundary:</strong> V25 art is unchanged. V26 adds derived scale-review images only; nothing is promoted or wired.</p>
</main><script>const files=['{prefix}/kitchen-game-scale-room.png','{prefix}/kitchen-game-scale-prime-standing.png','{prefix}/kitchen-game-scale-prime-seated-back.png'];Promise.all(files.map(src=>new Promise((ok,bad)=>{{const image=new Image;image.onload=()=>{{const decoded=image.decode?.();decoded?decoded.then(ok).catch(ok):ok()}};image.onerror=()=>bad(new Error('Could not load '+src));image.src=src}}))).then(()=>{{document.body.classList.add('ready');document.querySelector('#loading').textContent='All review images loaded and decoded.'}}).catch(error=>document.querySelector('#loading').textContent='Review locked: '+error.message)</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    pins = [(ROOM, ROOM_SHA), (PRIME_FRONT, PRIME_FRONT_SHA), (PRIME_SEATED_BACK, PRIME_SEATED_BACK_SHA)]
    for path, expected in pins:
        if sha(path) != expected:
            raise RuntimeError(f"Pinned input changed: {path.relative_to(ROOT)}")

    with Image.open(ROOM) as source_room, Image.open(PRIME_FRONT) as source_front, Image.open(PRIME_SEATED_BACK) as source_back:
        if source_room.size != (2169, 725):
            raise RuntimeError(f"V25 room is {source_room.size}, expected 2169 x 725")
        if source_front.size != (256, 320) or source_back.size != (256, 320):
            raise RuntimeError("Prime source cell must remain 256 x 320 at density 8")
        room = source_room.convert("RGBA").crop(ROOM_CROP).resize(GAME_SIZE, Image.Resampling.LANCZOS)
        front = source_front.convert("RGBA").resize(PRIME_SIZE, Image.Resampling.LANCZOS)
        back = source_back.convert("RGBA").resize(PRIME_SIZE, Image.Resampling.LANCZOS)

    standing = room.copy()
    standing.alpha_composite(front, STANDING_TOP_LEFT)
    seated = room.copy()
    seated.alpha_composite(back, SEATED_TOP_LEFT)

    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    outputs = {
        "kitchen-game-scale-room.png": room,
        "kitchen-game-scale-prime-standing.png": standing,
        "kitchen-game-scale-prime-seated-back.png": seated,
    }
    for name, image in outputs.items():
        image.save(RAW / name, optimize=True)
        copy(RAW / name, ASSETS / name)

    catalogue = {
        "version": 26,
        "status": "game-scale-prime-context-review",
        "base": {"version": 25, "sha256": ROOM_SHA, "changed": False},
        "presentation": {
            "densityPxPerLp": DENSITY,
            "roomLogical": list(ROOM_LOGICAL),
            "roomPixels": list(GAME_SIZE),
            "sourceCropExclusive": list(ROOM_CROP),
            "primeLogicalCell": list(PRIME_LOGICAL),
            "primePixels": list(PRIME_SIZE),
            "primeFloorAnchorLp": 56,
            "seatedContactAboveFloorLp": 11,
        },
        "placements": {
            "standing": {"topLeftPx": list(STANDING_TOP_LEFT), "rootLp": [106.5, 56], "sourceSha256": PRIME_FRONT_SHA},
            "seatedBack": {"topLeftPx": list(SEATED_TOP_LEFT), "rootLp": [179.75, 56], "sourceSha256": PRIME_SEATED_BACK_SHA},
        },
        "outputs": {name: {"sha256": sha(RAW / name), "size": list(image.size)} for name, image in outputs.items()},
        "boundaries": {"v25Changed": False, "approved": False, "promoted": False, "runtimeChanged": False, "finalChanged": False},
    }
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "version": 26,
        "v25Preserved": True,
        "rollback": "Delete only V26 raw/draft/review files, archive set, builder, verifier and V26 docs; V20–V25 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "outputs": len(outputs), "gameSize": GAME_SIZE}, indent=2))


if __name__ == "__main__":
    main()
