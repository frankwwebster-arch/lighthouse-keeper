#!/usr/bin/env python3
"""Build/verify the recovered-oven visual-authority gate for Kitchen V7.

V7 fixes the V6 process error: it uses Frank's exact preferred 1305x1206
oven PNG as the visual authority instead of replacing it with a scripted
approximation.  Only a reversible oven-On gate is produced here.  Broken
states and other appliances remain blocked until the registered result has
been reviewed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-built-in-state-ligne-claire-v7"
DATED = "kitchen-built-in-state-ligne-claire-2026-10-21-v7"
PACK = ROOT / "art" / "drafts" / DATED
SOURCE_AUTHORITY = ROOT / "art" / "source" / DATED / "oven-on-user-confirmed-visual-authority.png"
CURRENT = ROOT / "art" / "raw" / "kitchen-dishwasher-workbench-2026-10-20-v41" / "oven-on.png"
V6_MASTER = ROOT / "art" / "drafts" / "kitchen-built-in-state-ligne-claire-2026-10-21-v6" / "masters" / "oven" / "oven-on-master-8x.png"
PUBLIC = ROOT / "public" / "keeper-review" / SET
MASTER_SIZE = (736, 680)
CONTENT_BBOX = (165, 121, 1155, 1047)
SOURCE_ALPHA_BBOX = (4, 4, 88, 81)
EXPECTED_AUTHORITY_SHA = "0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538"
EXPECTED_CURRENT_SHA = "72c05de613f386ed51f9e049a3a986f34279bf04614a05b7b193d0b243be7622"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def make_master(authority: Image.Image, current: Image.Image) -> Image.Image:
    crop = authority.crop(CONTENT_BBOX)
    x0, y0, x1, y1 = SOURCE_ALPHA_BBOX
    master = Image.new("RGBA", MASTER_SIZE, (0, 0, 0, 0))
    fitted = crop.resize(((x1 - x0) * 8, (y1 - y0) * 8), Image.Resampling.LANCZOS)
    master.alpha_composite(fitted, (x0 * 8, y0 * 8))
    scaled_alpha = current.getchannel("A").resize(MASTER_SIZE, Image.Resampling.LANCZOS)
    master.putalpha(scaled_alpha)
    return master


def make_candidate(master: Image.Image, current: Image.Image) -> Image.Image:
    candidate = master.resize(current.size, Image.Resampling.LANCZOS)
    candidate.putalpha(current.getchannel("A"))
    return candidate


def checker(size: tuple[int, int], cell: int = 24) -> Image.Image:
    image = Image.new("RGBA", size, (246, 240, 220, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return image


def make_contact_sheet(master: Image.Image, candidate: Image.Image) -> Image.Image:
    v6 = Image.open(V6_MASTER).convert("RGBA")
    sheet = Image.new("RGBA", (1600, 850), (255, 249, 232, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((24, 18), "Kitchen oven V7 - recovered visual authority gate", fill="#051824", font=font)
    draw.text((24, 42), "LEFT: rejected V6 scripted substitute   RIGHT: exact preferred oven mapped to the unchanged authority geometry", fill="#051824", font=font)
    left = checker((760, 700))
    right = checker((760, 700))
    left.alpha_composite(v6, ((760 - v6.width) // 2, 10))
    right.alpha_composite(master, ((760 - master.width) // 2, 10))
    sheet.alpha_composite(left, (20, 78))
    sheet.alpha_composite(right, (820, 78))
    draw.text((28, 790), "REJECTED V6 - newly reconstructed artwork", fill="#b33a2b", font=font)
    draw.text((828, 790), "V7 - recovered preferred drawing; no substitute", fill="#145b45", font=font)
    sheet.alpha_composite(candidate, (828, 810))
    draw.text((940, 830), "registered native candidate: exact 92 x 85 canvas and byte-exact source alpha", fill="#051824", font=font)
    return sheet


def write_review_html() -> None:
    html = """<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Kitchen Oven Ligne-Claire V7</title><style>:root{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85}*{box-sizing:border-box}body{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}header,main{max-width:1380px;margin:auto;padding:24px}header{border-bottom:4px solid var(--ink)}.status{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e7a638;font-weight:800;border-radius:999px}.ready{background:#d9ded3}article{margin:22px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}img{display:block;max-width:100%;height:auto;margin:auto;image-rendering:auto}a{color:#174562}.warning{border-left:6px solid #e84833;padding-left:14px}</style></head><body><header><span class=\"status\">RECOVERED OVEN GATE - NOT CURRENT</span> <span id=\"ready\" class=\"status ready\">VERIFYING 0/2</span><h1>Kitchen Oven Ligne-Claire V7</h1><p class=\"warning\">V6 is rejected. V7 restores Frank's exact preferred oven as the visual authority. No broken-state propagation, registration, promotion or runtime change has occurred.</p><p>The first image is the exact 1305 x 1206 RGBA file Frank identified as superb. The comparison below shows where V6 went wrong and the corrected exact-geometry mapping. Judge the drawing, not an enlarged native sprite.</p></header><main><article><h2>Exact recovered visual authority</h2><img src=\"/keeper-review/kitchen-built-in-state-ligne-claire-v7/assets/oven-on-user-confirmed-visual-authority.png\" alt=\"Exact preferred oven visual authority\" decoding=\"async\"></article><article><h2>Rejected substitution versus corrected mapping</h2><img src=\"/keeper-review/kitchen-built-in-state-ligne-claire-v7/assets/oven-v6-vs-v7-contact.png\" alt=\"Rejected V6 and corrected V7 oven mapping\" decoding=\"async\"></article></main><script>(async()=>{const imgs=[...document.images],badge=document.getElementById('ready');let done=0;try{await Promise.all(imgs.map(async img=>{if(!img.complete)await new Promise((ok,no)=>{img.onload=ok;img.onerror=no});await img.decode();done++;badge.textContent=`VERIFYING ${done}/${imgs.length}`}));badge.textContent=`STATIC EVIDENCE READY - ${done}/${imgs.length} VERIFIED`}catch(error){badge.textContent='REVIEW LOCKED - '+error.message;throw error}})()</script></body></html>"""
    (PUBLIC / "index.html").write_text(html, encoding="utf-8")


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite existing immutable V7 output")
    if sha256(SOURCE_AUTHORITY) != EXPECTED_AUTHORITY_SHA:
        raise RuntimeError("preferred oven authority bytes changed")
    if sha256(CURRENT) != EXPECTED_CURRENT_SHA:
        raise RuntimeError("current oven authority bytes changed")
    authority = Image.open(SOURCE_AUTHORITY).convert("RGBA")
    current = Image.open(CURRENT).convert("RGBA")
    master = make_master(authority, current)
    candidate = make_candidate(master, current)
    master_path = PACK / "masters" / "oven-on-registered-master-8x.png"
    candidate_path = PACK / "candidates" / "oven" / "oven-on.png"
    evidence_path = PACK / "evidence" / "oven-v6-vs-v7-contact.png"
    for path in (master_path, candidate_path, evidence_path):
        path.parent.mkdir(parents=True, exist_ok=True)
    master.save(master_path, optimize=True)
    candidate.save(candidate_path, optimize=True)
    make_contact_sheet(master, candidate).save(evidence_path, optimize=True)
    record = {
        "schema": "lighthouse-keeper/kitchen-built-in-state-ligne-claire@7",
        "set": SET,
        "created": "2026-10-21",
        "status": "immutable-reversible-oven-on-gate-not-approved-not-registered",
        "rejectedPredecessor": "kitchen-built-in-state-ligne-claire-v6",
        "failureCorrected": "V6 substituted a scripted redraw for the preferred visual authority",
        "visualAuthorityFile": SOURCE_AUTHORITY.relative_to(ROOT).as_posix(),
        "visualAuthoritySha256": sha256(SOURCE_AUTHORITY),
        "visualAuthorityPixels": list(authority.size),
        "visualAuthorityContentBbox": list(CONTENT_BBOX),
        "sourceFile": CURRENT.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(CURRENT),
        "sourcePixels": list(current.size),
        "sourceAlphaSha256": alpha_sha(current),
        "masterFile": master_path.relative_to(ROOT).as_posix(),
        "masterSha256": sha256(master_path),
        "masterPixels": list(master.size),
        "candidateFile": candidate_path.relative_to(ROOT).as_posix(),
        "candidateSha256": sha256(candidate_path),
        "candidatePixels": list(candidate.size),
        "candidateAlphaSha256": alpha_sha(candidate),
        "alphaExact": alpha_sha(candidate) == alpha_sha(current),
        "scope": ["oven-on base gate only"],
        "unchanged": ["canvas", "alpha", "position", "anchors", "pivots", "collisions", "movement", "animations", "interactions", "healing", "timing", "state transitions", "runtime selectors"],
    }
    (PACK / "manifest.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({
        "schema": "lighthouse-keeper/kitchen-batch-register@7",
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
    }, indent=2) + "\n", encoding="utf-8")
    (PUBLIC / "assets").mkdir(parents=True)
    shutil.copy2(SOURCE_AUTHORITY, PUBLIC / "assets" / SOURCE_AUTHORITY.name)
    shutil.copy2(evidence_path, PUBLIC / "assets" / evidence_path.name)
    write_review_html()
    (PUBLIC / "manifest.json").write_text(json.dumps(record, separators=(",", ":")) + "\n", encoding="utf-8")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    if manifest["visualAuthoritySha256"] != EXPECTED_AUTHORITY_SHA or sha256(SOURCE_AUTHORITY) != EXPECTED_AUTHORITY_SHA:
        raise RuntimeError("preferred visual-authority hash mismatch")
    if manifest["sourceSha256"] != EXPECTED_CURRENT_SHA or sha256(CURRENT) != EXPECTED_CURRENT_SHA:
        raise RuntimeError("current source hash mismatch")
    current = Image.open(CURRENT).convert("RGBA")
    authority = Image.open(SOURCE_AUTHORITY).convert("RGBA")
    master = Image.open(ROOT / manifest["masterFile"]).convert("RGBA")
    candidate = Image.open(ROOT / manifest["candidateFile"]).convert("RGBA")
    if authority.size != (1305, 1206) or master.size != MASTER_SIZE or candidate.size != current.size:
        raise RuntimeError("canvas contract mismatch")
    if alpha_sha(candidate) != alpha_sha(current):
        raise RuntimeError("candidate alpha is not byte-exact")
    expected_master = make_master(authority, current)
    expected_candidate = make_candidate(expected_master, current)
    if master.tobytes() != expected_master.tobytes() or candidate.tobytes() != expected_candidate.tobytes():
        raise RuntimeError("V7 output is not deterministic from the pinned authority")
    gate = json.loads((PACK / "batch-register.json").read_text(encoding="utf-8"))
    if gate != {"schema": "lighthouse-keeper/kitchen-batch-register@7", "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}:
        raise RuntimeError("registration gate opened")
    html = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in html or "V6 is rejected" not in html:
        raise RuntimeError("review route regression")
    print("Verified V7: exact preferred oven authority, exact 92x85 canvas/alpha, registration closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
