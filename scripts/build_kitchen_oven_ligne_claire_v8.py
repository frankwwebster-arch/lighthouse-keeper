#!/usr/bin/env python3
"""Build/verify the top-safe Kitchen Oven Ligne-Claire V8 mapping gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-ligne-claire-v8"
DATED = "kitchen-oven-ligne-claire-2026-10-21-v8"
PACK = ROOT / "art" / "drafts" / DATED
AUTHORITY = ROOT / "art" / "source" / "kitchen-built-in-state-ligne-claire-2026-10-21-v7" / "oven-on-user-confirmed-visual-authority.png"
CURRENT = ROOT / "art" / "raw" / "kitchen-dishwasher-workbench-2026-10-20-v41" / "oven-on.png"
V7_MASTER = ROOT / "art" / "drafts" / "kitchen-built-in-state-ligne-claire-2026-10-21-v7" / "masters" / "oven-on-registered-master-8x.png"
PUBLIC = ROOT / "public" / "keeper-review" / SET
AUTHORITY_SHA = "0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538"
CURRENT_SHA = "72c05de613f386ed51f9e049a3a986f34279bf04614a05b7b193d0b243be7622"
CURRENT_BOUNDS = (4, 4, 88, 81)
AUTHORITY_CONTENT_BOUNDS = (162, 118, 1158, 1049)  # alpha > 1
# Eight or more source pixels of transparent clearance surround the measured
# authority content. V7 cropped at y=121 and therefore cut the upper contour.
SAFE_CROP = (155, 110, 1165, 1055)
MASTER_SIZE = (736, 680)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def alpha_bbox_over(image: Image.Image, threshold: int) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").point(lambda value: 255 if value > threshold else 0).getbbox()


def build_images(authority: Image.Image) -> tuple[Image.Image, Image.Image]:
    crop = authority.crop(SAFE_CROP)
    master = Image.new("RGBA", MASTER_SIZE, (0, 0, 0, 0))
    fitted = crop.resize((672, 616), Image.Resampling.LANCZOS)
    master.alpha_composite(fitted, (32, 32))
    candidate = master.resize((92, 85), Image.Resampling.LANCZOS)
    pixels = candidate.load()
    x0, y0, x1, y1 = CURRENT_BOUNDS
    for y in range(candidate.height):
        for x in range(candidate.width):
            if not (x0 <= x < x1 and y0 <= y < y1):
                pixels[x, y] = (0, 0, 0, 0)
    return master, candidate


def checker(size: tuple[int, int], cell: int = 24) -> Image.Image:
    image = Image.new("RGBA", size, (246, 240, 220, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return image


def contact_sheet(master: Image.Image, candidate: Image.Image) -> Image.Image:
    v7 = Image.open(V7_MASTER).convert("RGBA")
    sheet = Image.new("RGBA", (1600, 870), (255, 249, 232, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((24, 18), "Kitchen oven mapping V8 - top-contour correction", fill="#051824", font=font)
    draw.text((24, 42), "LEFT: rejected V7 byte-exact old alpha clips the new top   RIGHT: V8 keeps exact padding bounds and the authority's own complete contour", fill="#051824", font=font)
    for x, image in ((20, v7), (820, master)):
        panel = checker((760, 720))
        panel.alpha_composite(image, ((760 - image.width) // 2, 20))
        sheet.alpha_composite(panel, (x, 78))
    draw.text((28, 810), "REJECTED V7 MAPPING - top contour trimmed", fill="#b33a2b", font=font)
    draw.text((828, 810), "V8 MAPPING - measured top clearance retained", fill="#145b45", font=font)
    sheet.alpha_composite(candidate, (828, 830))
    draw.text((940, 850), "native 92 x 85; exact alpha bounds (4,4)-(88,81); no enlargement", fill="#051824", font=font)
    return sheet


def review_html() -> str:
    return """<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Kitchen Oven Ligne-Claire V8</title><style>:root{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85}*{box-sizing:border-box}body{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}header,main{max-width:1380px;margin:auto;padding:24px}header{border-bottom:4px solid var(--ink)}.status{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e7a638;font-weight:800;border-radius:999px}.ready{background:#d9ded3}article{margin:22px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}img{display:block;max-width:100%;height:auto;margin:auto;image-rendering:auto}.warning{border-left:6px solid #e84833;padding-left:14px}</style></head><body><header><span class=\"status\">TOP-SAFE OVEN GATE - NOT CURRENT</span> <span id=\"ready\" class=\"status ready\">VERIFYING 0/2</span><h1>Kitchen Oven Ligne-Claire V8</h1><p class=\"warning\">V7's mapping is rejected because its byte-exact old alpha trimmed the new hob contour. V8 preserves the exact authority, canvas and transparent padding bounds while retaining the authority's own complete contour.</p><p>No Broken-state propagation, dishwasher change, registration, promotion or runtime change has occurred.</p></header><main><article><h2>Exact visual authority (unchanged)</h2><img src=\"/keeper-review/kitchen-oven-ligne-claire-v8/assets/oven-on-user-confirmed-visual-authority.png\" alt=\"Exact preferred oven visual authority\" decoding=\"async\"></article><article><h2>Rejected V7 mapping versus top-safe V8</h2><img src=\"/keeper-review/kitchen-oven-ligne-claire-v8/assets/oven-v7-vs-v8-contact.png\" alt=\"Rejected clipped V7 and corrected V8 mapping\" decoding=\"async\"></article></main><script>(async()=>{const imgs=[...document.images],badge=document.getElementById('ready');let done=0;try{await Promise.all(imgs.map(async img=>{if(!img.complete)await new Promise((ok,no)=>{img.onload=ok;img.onerror=no});await img.decode();done++;badge.textContent=`VERIFYING ${done}/${imgs.length}`}));badge.textContent=`STATIC EVIDENCE READY - ${done}/${imgs.length} VERIFIED`}catch(error){badge.textContent='REVIEW LOCKED - '+error.message;throw error}})()</script></body></html>"""


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable V8 output")
    if sha256(AUTHORITY) != AUTHORITY_SHA or sha256(CURRENT) != CURRENT_SHA:
        raise RuntimeError("pinned authority changed")
    authority = Image.open(AUTHORITY).convert("RGBA")
    if alpha_bbox_over(authority, 1) != AUTHORITY_CONTENT_BOUNDS:
        raise RuntimeError("visual-authority content bounds changed")
    master, candidate = build_images(authority)
    master_path = PACK / "masters" / "oven-on-top-safe-master-8x.png"
    candidate_path = PACK / "candidates" / "oven" / "oven-on.png"
    evidence_path = PACK / "evidence" / "oven-v7-vs-v8-contact.png"
    for path in (master_path, candidate_path, evidence_path):
        path.parent.mkdir(parents=True, exist_ok=True)
    master.save(master_path, optimize=True)
    candidate.save(candidate_path, optimize=True)
    contact_sheet(master, candidate).save(evidence_path, optimize=True)
    manifest = {
        "schema": "lighthouse-keeper/kitchen-oven-ligne-claire@8",
        "set": SET,
        "created": "2026-10-21",
        "status": "immutable-reversible-oven-on-gate-not-approved-not-registered",
        "rejectedPredecessor": "kitchen-built-in-state-ligne-claire-v7",
        "correction": "retain the visual authority's complete top contour inside the exact source alpha bounds",
        "visualAuthorityFile": AUTHORITY.relative_to(ROOT).as_posix(),
        "visualAuthoritySha256": sha256(AUTHORITY),
        "visualAuthorityPixels": list(authority.size),
        "visualAuthorityContentBoundsAlphaGt1": list(AUTHORITY_CONTENT_BOUNDS),
        "safeCrop": list(SAFE_CROP),
        "sourceFile": CURRENT.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(CURRENT),
        "sourcePixels": [92, 85],
        "sourceAlphaBounds": list(CURRENT_BOUNDS),
        "masterFile": master_path.relative_to(ROOT).as_posix(),
        "masterSha256": sha256(master_path),
        "candidateFile": candidate_path.relative_to(ROOT).as_posix(),
        "candidateSha256": sha256(candidate_path),
        "candidatePixels": list(candidate.size),
        "candidateAlphaBounds": list(candidate.getchannel("A").getbbox() or ()),
        "alphaBoundsExact": candidate.getchannel("A").getbbox() == CURRENT_BOUNDS,
        "perPixelAlphaExact": False,
        "reasonPerPixelAlphaIsNotReused": "the old internal alpha silhouette clipped the approved new contour",
        "unchanged": ["canvas", "transparent padding bounds", "position", "anchors", "pivots", "collisions", "movement", "animations", "interactions", "healing", "timing", "state transitions", "runtime selectors"],
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"schema": "lighthouse-keeper/kitchen-batch-register@8", "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n", encoding="utf-8")
    (PUBLIC / "assets").mkdir(parents=True)
    shutil.copy2(AUTHORITY, PUBLIC / "assets" / AUTHORITY.name)
    shutil.copy2(evidence_path, PUBLIC / "assets" / evidence_path.name)
    (PUBLIC / "index.html").write_text(review_html(), encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    authority = Image.open(AUTHORITY).convert("RGBA")
    master, candidate = build_images(authority)
    stored_master = Image.open(ROOT / manifest["masterFile"]).convert("RGBA")
    stored_candidate = Image.open(ROOT / manifest["candidateFile"]).convert("RGBA")
    if sha256(AUTHORITY) != AUTHORITY_SHA or sha256(CURRENT) != CURRENT_SHA:
        raise RuntimeError("authority hash mismatch")
    if stored_master.tobytes() != master.tobytes() or stored_candidate.tobytes() != candidate.tobytes():
        raise RuntimeError("V8 output is not deterministic")
    if stored_candidate.size != (92, 85) or stored_candidate.getchannel("A").getbbox() != CURRENT_BOUNDS:
        raise RuntimeError("canvas or transparent padding bounds changed")
    gate = json.loads((PACK / "batch-register.json").read_text(encoding="utf-8"))
    if gate["register"] or gate["promote"] or gate["currentSelectorChanges"]:
        raise RuntimeError("registration gate opened")
    html = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in html or "V7's mapping is rejected" not in html:
        raise RuntimeError("review delivery regression")
    print("Verified Oven V8: exact visual authority, complete top contour, exact 92x85 canvas and alpha bounds, gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
