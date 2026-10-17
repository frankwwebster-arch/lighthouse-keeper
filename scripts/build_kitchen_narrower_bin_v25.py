#!/usr/bin/env python3
"""Publish Kitchen V25 with the standalone pedal bin 20% less wide."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-narrower-bin-2026-10-17-v25"
RAW = ROOT / "art/raw/kitchen-narrower-bin-2026-10-17-v25"
DRAFT = ROOT / "art/drafts/kitchen-narrower-bin-2026-10-17-v25"
PUBLIC = ROOT / "public/keeper-review/kitchen-narrower-bin-v25"
ASSETS = PUBLIC / "assets"
V24 = ROOT / "art/raw/kitchen-rear-facing-chair-2026-10-17-v24/full-kitchen-rear-facing-chair.png"
EDIT_SOURCE = SOURCE / "image-edit-source.png"
EDIT_SHA = "175d77c063297c435eab468f297c369f79e5491b89bbdd2b03400d31cd334f4a"
V24_SHA = "85e50fc43d43538e226e41e9d781cd8eee805b6025fe15302639a8f178ce71b2"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def write_page() -> None:
    prefix = "/keeper-review/kitchen-narrower-bin-v25/assets"
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V25 · narrower pedal bin</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1500px;margin:auto;padding:22px}}h1,h2,h3{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.scroll{{overflow:auto;background:#02080b;border-radius:9px;padding:12px}}img{{display:block;image-rendering:auto}}.room{{width:2169px;height:725px}}.comparison{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}article{{background:#091e29;border:1px solid #315768;border-radius:11px;padding:12px;overflow:auto}}article img{{width:780px;height:690px;max-width:none;image-rendering:pixelated}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}@media(max-width:800px){{main{{padding:12px}}.comparison{{grid-template-columns:1fr}}}}
</style></head><body><main><span class="tag">V25</span><span class="tag">V24 preserved</span><span class="tag">Bin 20% narrower</span><h1>Standalone pedal bin · reduced width</h1><p class="note"><strong>Requested change:</strong> the turquoise pedal bin is 20% less wide while retaining its centreline, height, floor contact, colour, lid and pedal treatment. The rear-facing chair and approved kitchen composition remain as in V24.</p><p id="loading">Loading and decoding review media…</p>
<section><h2>Complete kitchen</h2><div class="scroll"><img data-media class="room" src="{prefix}/full-kitchen-narrower-bin.png" width="2169" height="725" alt="Complete kitchen with narrower standalone turquoise pedal bin"></div></section>
<section><h2>Pedal bin · before / after</h2><div class="comparison"><article><h3>V24 · previous width</h3><img data-media src="{prefix}/bin-before.png" width="780" height="690" alt="V24 standalone pedal bin"></article><article><h3>V25 · 20% less wide</h3><img data-media src="{prefix}/bin-after.png" width="780" height="690" alt="V25 narrower standalone pedal bin"></article></div></section>
<p class="warn"><strong>Version boundary:</strong> V24 remains immutable. V25 is the requested one-change successor and remains unpromoted and unwired pending visual confirmation.</p>
</main><script>const files=['{prefix}/full-kitchen-narrower-bin.png','{prefix}/bin-before.png','{prefix}/bin-after.png'];Promise.all(files.map(src=>new Promise((ok,bad)=>{{const image=new Image;image.onload=()=>{{const decoded=image.decode?.();decoded?decoded.then(ok).catch(ok):ok()}};image.onerror=()=>bad(new Error('Could not load '+src));image.src=src}}))).then(()=>{{document.body.classList.add('ready');document.querySelector('#loading').textContent='All review images loaded and decoded.'}}).catch(error=>document.querySelector('#loading').textContent='Review locked: '+error.message)</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    if sha(EDIT_SOURCE) != EDIT_SHA:
        raise RuntimeError("V25 image-edit source changed")
    if sha(V24) != V24_SHA:
        raise RuntimeError("V24 room candidate changed")
    with Image.open(EDIT_SOURCE) as after, Image.open(V24) as before:
        if after.size != (2169, 725):
            raise RuntimeError(f"V25 edit is {after.size}, expected 2169 x 725")
        if before.size != (2169, 725):
            raise RuntimeError(f"V24 master is {before.size}, expected 2169 x 725")
        before_crop = before.convert("RGBA").crop((0, 420, 260, 650))
        after_crop = after.convert("RGBA").crop((0, 420, 260, 650))

    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    copy(EDIT_SOURCE, RAW / "full-kitchen-narrower-bin.png")
    copy(EDIT_SOURCE, ASSETS / "full-kitchen-narrower-bin.png")
    before_crop.save(RAW / "bin-before.png", optimize=True)
    before_crop.save(ASSETS / "bin-before.png", optimize=True)
    after_crop.save(RAW / "bin-after.png", optimize=True)
    after_crop.save(ASSETS / "bin-after.png", optimize=True)

    outputs = ["full-kitchen-narrower-bin.png", "bin-before.png", "bin-after.png"]
    catalogue = {
        "version": 25,
        "status": "requested-bin-width-correction-awaiting-visual-confirmation",
        "base": {"version": 24, "sha256": V24_SHA},
        "change": {
            "object": "standalone turquoise pedal bin",
            "widthFactor": 0.8,
            "centrelinePreserved": True,
            "heightPreserved": True,
            "floorContactPreserved": True,
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
        "version": 25,
        "v24Preserved": True,
        "rollback": "Delete only V25 source/raw/draft/review files, archive set, builder, verifier and V25 docs; V20–V24 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "outputs": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
