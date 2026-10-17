#!/usr/bin/env python3
"""Publish Kitchen V24 with the chair behind Prime and facing the table."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-rear-facing-chair-2026-10-17-v24"
RAW = ROOT / "art/raw/kitchen-rear-facing-chair-2026-10-17-v24"
DRAFT = ROOT / "art/drafts/kitchen-rear-facing-chair-2026-10-17-v24"
PUBLIC = ROOT / "public/keeper-review/kitchen-rear-facing-chair-v24"
ASSETS = PUBLIC / "assets"
V23 = ROOT / "art/raw/kitchen-continuous-run-approved-2026-10-17-v23/full-kitchen-approved.png"
EDIT_SOURCE = SOURCE / "image-edit-source.png"
EDIT_SHA = "85e50fc43d43538e226e41e9d781cd8eee805b6025fe15302639a8f178ce71b2"
V23_SHA = "5d5451acbaa81a48918268d25482a1d3f657a77c441c9d5b4f87ed547d4f9707"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def write_page() -> None:
    prefix = "/keeper-review/kitchen-rear-facing-chair-v24/assets"
    before = "/keeper-review/kitchen-continuous-run-approved-v23/assets/full-kitchen-approved.png"
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V24 · rear-facing chair</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1500px;margin:auto;padding:22px}}h1,h2,h3{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.scroll{{overflow:auto;background:#02080b;border-radius:9px;padding:12px}}img{{display:block;image-rendering:auto}}.room{{width:2169px;height:725px}}.comparison{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}article{{background:#091e29;border:1px solid #315768;border-radius:11px;padding:12px;overflow:auto}}article img{{width:1100px;height:640px;max-width:none}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}@media(max-width:800px){{main{{padding:12px}}.comparison{{grid-template-columns:1fr}}}}
</style></head><body><main><span class="tag">V24</span><span class="tag">V23 kitchen preserved</span><span class="tag">Chair corrected</span><h1>One-person table · Prime faces the rear wall</h1><p class="note"><strong>Requested change:</strong> the single chair is now centred on the player-facing side of the table and drawn from behind. Its backrest faces the player, so a seated Prime Keeper faces the table and rear wall with his back to the player.</p><p id="loading">Loading and decoding review media…</p>
<section><h2>Complete kitchen with corrected chair</h2><div class="scroll"><img data-media class="room" src="{prefix}/full-kitchen-rear-facing-chair.png" width="2169" height="725" alt="Complete approved kitchen with one rear-view chair centred in front of the table"></div><p>The fitted kitchen, standalone bin and table remain in the approved V23 composition. There is exactly one chair.</p></section>
<section><h2>Chair placement · before / after</h2><div class="comparison"><article><h3>V23 · side-on chair</h3><img data-media src="{prefix}/table-before.png" width="1100" height="640" alt="V23 table with side-on chair"></article><article><h3>V24 · back to player</h3><img data-media src="{prefix}/table-after.png" width="1100" height="640" alt="V24 table with rear-view chair centred on the near side"></article></div></section>
<p class="warn"><strong>Version boundary:</strong> V23 remains immutable approved kitchen provenance. V24 is the requested one-change successor and remains unpromoted and unwired pending visual confirmation.</p>
</main><script>const files=['{prefix}/full-kitchen-rear-facing-chair.png','{prefix}/table-before.png','{prefix}/table-after.png','{before}'];Promise.all(files.map(src=>new Promise((ok,bad)=>{{const image=new Image;image.onload=()=>{{const decoded=image.decode?.();decoded?decoded.then(ok).catch(ok):ok()}};image.onerror=()=>bad(new Error('Could not load '+src));image.src=src}}))).then(()=>{{document.body.classList.add('ready');document.querySelector('#loading').textContent='All review images loaded and decoded.'}}).catch(error=>document.querySelector('#loading').textContent='Review locked: '+error.message)</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    if sha(EDIT_SOURCE) != EDIT_SHA:
        raise RuntimeError("V24 image-edit source changed")
    if sha(V23) != V23_SHA:
        raise RuntimeError("V23 approved master changed")
    with Image.open(EDIT_SOURCE) as after, Image.open(V23) as before:
        if after.size != (2169, 725):
            raise RuntimeError(f"V24 edit is {after.size}, expected 2169 x 725")
        if before.size != (2170, 725):
            raise RuntimeError(f"V23 master is {before.size}, expected 2170 x 725")
        # The focused crop is review evidence only; the full generated edit is
        # retained byte-for-byte as the V24 room candidate.
        before_crop = before.convert("RGBA").crop((1500, 330, 2050, 650))
        after_crop = after.convert("RGBA").crop((1500, 330, 2050, 650))

    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    copy(EDIT_SOURCE, RAW / "full-kitchen-rear-facing-chair.png")
    copy(EDIT_SOURCE, ASSETS / "full-kitchen-rear-facing-chair.png")
    before_crop.save(RAW / "table-before.png", optimize=True)
    before_crop.save(ASSETS / "table-before.png", optimize=True)
    after_crop.save(RAW / "table-after.png", optimize=True)
    after_crop.save(ASSETS / "table-after.png", optimize=True)

    outputs = ["full-kitchen-rear-facing-chair.png", "table-before.png", "table-after.png"]
    catalogue = {
        "version": 24,
        "status": "requested-chair-correction-awaiting-visual-confirmation",
        "base": {"version": 23, "sha256": V23_SHA},
        "change": {
            "object": "single chair at table for one",
            "old": "side-on, between sink and table",
            "new": "rear view, centred on player-facing side, seat faces table/rear wall",
            "keeperOrientation": "back to player when seated",
            "chairCount": 1,
        },
        "source": {
            "generator": "OpenAI built-in image editing",
            "sha256": EDIT_SHA,
            "size": [2169, 725],
        },
        "outputs": {name: {"sha256": sha(RAW / name)} for name in outputs},
        "boundaries": {"approved": False, "promoted": False, "runtimeChanged": False, "finalChanged": False, "keeperChanged": False},
    }
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "version": 24,
        "v23Preserved": True,
        "rollback": "Delete only V24 source/raw/draft/review files, archive set, builder, verifier and V24 docs; V20–V23 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
