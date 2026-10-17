#!/usr/bin/env python3
"""Publish the exact Image 1 kitchen accepted by Frank as V23.

The approved raster is copied byte-for-byte. No crop, resize, colour operation,
or reconstruction is permitted here. V20–V22 remain immutable provenance.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-continuous-run-approved-2026-10-17-v23"
RAW = ROOT / "art/raw/kitchen-continuous-run-approved-2026-10-17-v23"
DRAFT = ROOT / "art/drafts/kitchen-continuous-run-approved-2026-10-17-v23"
PUBLIC = ROOT / "public/keeper-review/kitchen-continuous-run-approved-v23"
ASSETS = PUBLIC / "assets"
SOURCE_IMAGE = SOURCE / "approved-image-1.png"
OUTPUT_IMAGE = RAW / "full-kitchen-approved.png"
PUBLIC_IMAGE = ASSETS / "full-kitchen-approved.png"

APPROVED_SHA256 = "5d5451acbaa81a48918268d25482a1d3f657a77c441c9d5b4f87ed547d4f9707"
APPROVAL_POINT = {"xPercent": 37.3, "yPercent": 56.9, "comment": "this is correct"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_page() -> None:
    prefix = "/keeper-review/kitchen-continuous-run-approved-v23/assets"
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V23 · approved continuous run</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#071722;color:#edf8f5;font:16px/1.45 system-ui,sans-serif}}main{{max-width:1500px;margin:auto;padding:22px}}h1,h2{{line-height:1.12}}.tag{{display:inline-block;border:1px solid #78d8cf;border-radius:999px;padding:4px 9px;margin-right:6px;color:#9af1e9}}section{{background:#102b37;border:1px solid #315768;border-radius:14px;padding:16px;margin:16px 0}}.scroll{{overflow:auto;background:#02080b;border-radius:9px;padding:12px}}.frame{{position:relative;width:2170px;height:725px}}img{{display:block;width:2170px;height:725px;image-rendering:auto}}.marker{{display:none;position:absolute;left:37.3%;top:56.9%;width:24px;height:24px;border:3px solid #fff;border-radius:50%;box-shadow:0 0 0 3px #e14635,0 2px 9px #000;transform:translate(-50%,-50%);pointer-events:none}}body.show-marker .marker{{display:block}}button{{font:inherit;padding:7px 12px;border-radius:7px;border:1px solid #78d8cf;background:#123c4a;color:#edf8f5}}.note{{border-left:4px solid #72e2a5;background:#14281f;padding:11px 13px}}.warn{{border-left:4px solid #e8b852;background:#292315;padding:11px 13px}}code{{overflow-wrap:anywhere}}#loading{{font-variant-numeric:tabular-nums}}[data-media]{{visibility:hidden}}body.ready [data-media]{{visibility:visible}}@media(max-width:800px){{main{{padding:12px}}}}
</style></head><body><main><span class="tag">V23</span><span class="tag">Exact Image 1</span><span class="tag">Approved visual authority</span><h1>Approved continuous fitted kitchen</h1><p class="note"><strong>Frank: “this is correct.”</strong> This page publishes Image 1 byte-for-byte. It is the binding visual authority for the continuous rear-wall run: full-height shared carcass, uninterrupted sea-glass worktop and a common dark base, with the fitted bays reading as one installation.</p><p id="loading">Loading and decoding the approved image…</p>
<section><h2>Clean approved master</h2><p><button id="markerButton" disabled>Show approval point</button> <span id="markerStatus">Marker hidden</span></p><div class="scroll"><div class="frame"><img data-media id="approvedImage" src="{prefix}/full-kitchen-approved.png" width="2170" height="725" alt="Approved full Lighthouse Keeper kitchen with a continuous rear-wall fitted run, pedal bin, one chair and table"><span class="marker" aria-hidden="true"></span></div></div><p>Approval point: <code>x=37.3%, y=56.9%</code>, on the toaster/counter treatment. The marker is an HTML overlay only and is not baked into the approved raster.</p></section>
<section><h2>Authority boundary</h2><p>V23 supersedes V22's deterministic room reconstruction. V21 remains the isolated-asset inventory and V20 remains fitted-galley provenance, but any final room assembly or later production extraction must reproduce this exact V23 appearance. Runtime sprites, Final art and Keeper art remain unchanged until separately promoted.</p></section>
<p class="warn"><strong>Integrity:</strong> source, raw master and archived review object all have SHA-256 <code>{APPROVED_SHA256}</code>. No image-generation retry or post-processing was used after Frank's approval.</p>
</main><script>const image=document.querySelector('#approvedImage'),button=document.querySelector('#markerButton'),status=document.querySelector('#markerStatus');const ready=()=>{{document.body.classList.add('ready');button.disabled=false;document.querySelector('#loading').textContent='Approved image loaded and decoded.'}};image.onload=()=>{{const decoded=image.decode?.();decoded?decoded.then(ready).catch(ready):ready()}};image.onerror=()=>document.querySelector('#loading').textContent='Review locked: approved image failed to load.';button.onclick=()=>{{document.body.classList.toggle('show-marker');const shown=document.body.classList.contains('show-marker');button.textContent=shown?'Hide approval point':'Show approval point';status.textContent=shown?'Marker shown at 37.3%, 56.9%':'Marker hidden'}}</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    if sha(SOURCE_IMAGE) != APPROVED_SHA256:
        raise RuntimeError("approved Image 1 source hash changed")
    with Image.open(SOURCE_IMAGE) as image:
        if image.size != (2170, 725):
            raise RuntimeError(f"approved Image 1 is {image.size}, expected 2170 x 725")

    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_IMAGE, OUTPUT_IMAGE)
    shutil.copyfile(SOURCE_IMAGE, PUBLIC_IMAGE)
    if sha(OUTPUT_IMAGE) != APPROVED_SHA256 or sha(PUBLIC_IMAGE) != APPROVED_SHA256:
        raise RuntimeError("V23 publication is not byte-identical to approved Image 1")

    catalogue = {
        "version": 23,
        "status": "approved-visual-authority-unpromoted",
        "approval": {
            "date": "2026-10-17",
            "comment": "this is correct",
            "image": "Image 1",
            "point": APPROVAL_POINT,
        },
        "master": {
            "source": str(SOURCE_IMAGE.relative_to(ROOT)),
            "raw": str(OUTPUT_IMAGE.relative_to(ROOT)),
            "width": 2170,
            "height": 725,
            "sha256": APPROVED_SHA256,
            "transformationsAfterApproval": [],
        },
        "authority": {
            "roomAppearance": "V23 exact Image 1",
            "isolatedAssetInventory": "V21",
            "fittedGalleyProvenance": "V20",
            "rejectedRoomAssembly": "V22 deterministic reconstruction",
        },
        "boundaries": {
            "approved": True,
            "promoted": False,
            "runtimeChanged": False,
            "finalChanged": False,
            "keeperChanged": False,
        },
    }
    (DRAFT / "approval-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "version": 23,
        "approvedImageSha256": APPROVED_SHA256,
        "v22Preserved": True,
        "rollback": "Delete only V23 source/raw/draft/review files, its archive set, builder, verifier and V23 docs; V20–V22 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC.relative_to(ROOT)), "sha256": APPROVED_SHA256}, indent=2))


if __name__ == "__main__":
    main()
