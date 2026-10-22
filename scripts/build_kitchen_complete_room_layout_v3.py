#!/usr/bin/env python3
"""Build the load-safe V3 kitchen review from immutable V2 drawings.

V2's nineteen PNGs are packed losslessly into one transparent atlas.  The
review therefore has one image to download and decode before interaction,
while every source rectangle and room-space registration remains unchanged.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
V2_SET = "kitchen-complete-room-layout-2026-10-22-v2"
SET = "kitchen-complete-room-layout-2026-10-22-v3"
V2 = ROOT / "art/drafts" / V2_SET
V2_PAGE = ROOT / "public/keeper-review/kitchen-complete-room-layout-v2/index.html"
OUT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-complete-room-layout-v3"
V2_MANIFEST_SHA256 = "a3a4bbef753700b168a8341c2ff1dfd6b4eecab9436e550e51ec85849ab87b33"
ATLAS_NAME = "kitchen-complete-room-atlas-v3.png"
GUTTER = 8


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"expected one occurrence, found {text.count(old)}: {old[:80]!r}")
    return text.replace(old, new)


def build_atlas(v2: dict) -> tuple[Image.Image, dict[str, list[int]]]:
    ordered = [("assets", name, record) for name, record in v2["assets"].items()]
    ordered += [("looseAssets", name, record) for name, record in v2["looseAssets"].items()]
    images = []
    for group, name, record in ordered:
        source = V2 / "assets" / record["file"]
        assert sha256(source) == record["sha256"], f"V2 source changed: {name}"
        image = Image.open(source).convert("RGBA")
        assert list(image.size) == record["pixels"]
        images.append((group, name, image))

    width = max(image.width for _, _, image in images) + GUTTER * 2
    height = sum(image.height for _, _, image in images) + GUTTER * (len(images) + 1)
    atlas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    rects: dict[str, list[int]] = {}
    y = GUTTER
    for group, name, image in images:
        atlas.alpha_composite(image, (GUTTER, y))
        rects[f"{group}:{name}"] = [GUTTER, y, image.width, image.height]
        y += image.height + GUTTER
    return atlas, rects


def build_page() -> str:
    page = V2_PAGE.read_text()
    page = page.replace("Kitchen Complete Room Layout V2", "Kitchen Complete Room Layout V3")
    page = page.replace("UNAPPROVED COMPLETE-ROOM REVIEW V2", "UNAPPROVED COMPLETE-ROOM REVIEW V3")
    page = page.replace("LOADING 19 EXACT ASSETS", "LOADING ONE LOSSLESS ATLAS")
    page = page.replace("kitchen-complete-room-layout-v2", "kitchen-complete-room-layout-v3")
    page = replace_once(
        page,
        "let manifest,images={},order=[...CABINETS]",
        "let manifest,atlas,order=[...CABINETS]",
    )
    page = replace_once(
        page,
        "const loadImage=(name,record)=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>image.decode().then(()=>{images[name]=image;resolve()}).catch(reject);image.onerror=reject;image.src=`${ROUTE}/assets/${record.file}`});",
        "const loadAtlas=record=>new Promise((resolve,reject)=>{let settled=false;const image=new Image(),finish=value=>{if(settled)return;settled=true;clearTimeout(timer);value instanceof Error?reject(value):(atlas=image,resolve())},timer=setTimeout(()=>finish(new Error('atlas timed out after 30 seconds')),30000);image.onload=()=>image.decode().then(()=>finish(true)).catch(error=>finish(error));image.onerror=()=>finish(new Error('atlas failed to load'));image.src=`${ROUTE}/assets/${record.file}`});",
    )
    page = replace_once(
        page,
        "function drawCabinet(ctx,name,origin,alpha=1){const visual=visualName(name),asset=manifest.assets[visual],image=images[visual],body=asset.bodyRect,sx=BODY[0]/body[2],sy=BODY[1]/body[3],x=origin-body[0]*sx,y=BODY_Y-body[1]*sy;ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(image,x,y,image.width*sx,image.height*sy);ctx.restore()}",
        "function drawCabinet(ctx,name,origin,alpha=1){const visual=visualName(name),asset=manifest.assets[visual],body=asset.bodyRect,[ax,ay,aw,ah]=asset.atlasRect,sx=BODY[0]/body[2],sy=BODY[1]/body[3],x=origin-body[0]*sx,y=BODY_Y-body[1]*sy;ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(atlas,ax,ay,aw,ah,x,y,aw*sx,ah*sy);ctx.restore()}",
    )
    page = replace_once(
        page,
        "function drawLoose(ctx,name,position,alpha=1){const asset=manifest.looseAssets[name],size=asset.logicalCanvas;ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(images[`loose:${name}`],position[0],position[1],size[0],size[1]);ctx.restore()}",
        "function drawLoose(ctx,name,position,alpha=1){const asset=manifest.looseAssets[name],size=asset.logicalCanvas,[ax,ay,aw,ah]=asset.atlasRect;ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(atlas,ax,ay,aw,ah,position[0],position[1],size[0],size[1]);ctx.restore()}",
    )
    old_loader = "fetch(`${ROUTE}/manifest.json`).then(response=>{if(!response.ok)throw new Error(`manifest ${response.status}`);return response.json()}).then(value=>{manifest=value;loose=clonePositions(manifest.looseGeometry.defaultPositions);saved();const requests=Object.entries(manifest.assets).map(([name,record])=>loadImage(name,record));for(const [name,record] of Object.entries(manifest.looseAssets))requests.push(loadImage(`loose:${name}`,record));return Promise.all(requests)}).then(()=>{ready=true;document.getElementById('ready').textContent='19 ASSETS READY';document.getElementById('ready').style.background='var(--sea)';document.querySelectorAll('button').forEach(button=>button.disabled=false);render()}).catch(error=>{document.getElementById('ready').textContent=`REVIEW LOCKED — ${error.message}`;document.getElementById('readout').textContent='One or more review files failed to decode. Movement remains disabled.'});"
    new_loader = "fetch(`${ROUTE}/manifest.json`).then(response=>{if(!response.ok)throw new Error(`manifest ${response.status}`);return response.json()}).then(value=>{manifest=value;loose=clonePositions(manifest.looseGeometry.defaultPositions);saved();return loadAtlas(manifest.atlas)}).then(()=>{ready=true;document.getElementById('ready').textContent='1 ATLAS READY • 19 DRAWINGS';document.getElementById('ready').style.background='var(--sea)';document.querySelectorAll('button').forEach(button=>button.disabled=false);render()}).catch(error=>{document.getElementById('ready').textContent=`REVIEW LOCKED — ${error.message}`;document.getElementById('readout').textContent='The review atlas did not decode. Movement remains disabled; reload once or report this exact message.'});"
    page = replace_once(page, old_loader, new_loader)
    page = page.replace(
        "Loading and decoding every source crop before movement is enabled…",
        "Loading one lossless atlas containing all 19 exact drawings before movement is enabled…",
    )
    page = page.replace(
        "All five loose objects come from one source sheet using the approved cabinetry as the style authority.",
        "All five loose objects come from one source sheet using the approved cabinetry as the style authority. V3 changes delivery only: all 19 unchanged drawings share one lossless atlas.",
    )
    return page


def main() -> None:
    v2_manifest_path = V2 / "manifest.json"
    assert sha256(v2_manifest_path) == V2_MANIFEST_SHA256, "V2 manifest changed"
    v2 = json.loads(v2_manifest_path.read_text())
    atlas, rects = build_atlas(v2)
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "assets").mkdir(parents=True, exist_ok=True)
    draft_atlas = OUT / "assets" / ATLAS_NAME
    public_atlas = PUBLIC / "assets" / ATLAS_NAME
    atlas.save(draft_atlas, optimize=True)
    public_atlas.write_bytes(draft_atlas.read_bytes())
    atlas_sha = sha256(draft_atlas)

    assets = {}
    for name, record in v2["assets"].items():
        assets[name] = {
            **record,
            "sourceFile": record["file"],
            "sourceSha256": record["sha256"],
            "file": ATLAS_NAME,
            "atlasRect": rects[f"assets:{name}"],
        }
    loose_assets = {}
    for name, record in v2["looseAssets"].items():
        loose_assets[name] = {
            **record,
            "sourceFile": record["file"],
            "sourceSha256": record["sha256"],
            "file": ATLAS_NAME,
            "atlasRect": rects[f"looseAssets:{name}"],
        }

    manifest = {
        **v2,
        "schema": "lighthouse-keeper/kitchen-complete-room-layout@3",
        "set": SET,
        "status": "unapproved-complete-room-layout-review-load-safe",
        "deliveryPredecessor": {
            "set": V2_SET,
            "manifestSha256": V2_MANIFEST_SHA256,
            "drawingPixelsChanged": False,
            "roomGeometryChanged": False,
            "interactionChanged": False,
        },
        "atlas": {
            "file": ATLAS_NAME,
            "sha256": atlas_sha,
            "pixels": list(atlas.size),
            "drawingCount": len(assets) + len(loose_assets),
            "uniqueImageRequests": 1,
            "lossless": True,
        },
        "assets": assets,
        "looseAssets": loose_assets,
    }
    payload = (json.dumps(manifest, indent=2) + "\n").encode()
    (OUT / "manifest.json").write_bytes(payload)
    (PUBLIC / "manifest.json").write_bytes(payload)
    page = build_page()
    (PUBLIC / "index.html").write_text(page)
    print(json.dumps({"set": SET, "atlas": manifest["atlas"]}, indent=2))


if __name__ == "__main__":
    main()
