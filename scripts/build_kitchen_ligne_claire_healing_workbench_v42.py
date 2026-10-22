#!/usr/bin/env python3
"""Build a reversible V42 movable/healing review using approved/candidate art.

The interaction implementation is mechanically inherited from approved V41.
Only review delivery, the visible oven state and asset byte sources change.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-healing-workbench-v42"
DATED = "kitchen-ligne-claire-healing-workbench-2026-10-22-v42"
PACK = ROOT / "art" / "drafts" / DATED
ASSETS = PACK / "assets"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"
V41_HTML = ROOT / "public" / "keeper-review" / "kitchen-dishwasher-workbench-v41" / "index.html"
V41_RAW = ROOT / "art" / "raw" / "kitchen-dishwasher-workbench-2026-10-20-v41"
FITTED = ROOT / "art" / "drafts" / "kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3" / "candidates"
DISHWASHER = ROOT / "art" / "drafts" / "kitchen-dishwasher-ligne-claire-2026-10-22-v1" / "candidates"
OVEN_ON = ROOT / "art" / "drafts" / "kitchen-oven-ligne-claire-2026-10-21-v8" / "candidates" / "oven" / "oven-on.png"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def asset_sources() -> dict[str, Path]:
    mapping: dict[str, Path] = {
        "room-background-exact.png": V41_RAW / "room-background-exact.png",
        "sink-cabinet-v19-exact.png": FITTED / "sink" / "sink-cabinet-standard.png",
        "fridge-standard.png": FITTED / "fridge" / "fridge-standard.png",
        "oven-on.png": OVEN_ON,
        "fx-dishwasher-suds--compact-f40.png": V41_RAW / "fx-dishwasher-suds--compact-f40.png",
        "fx-dishwasher-suds--regular-f40.png": V41_RAW / "fx-dishwasher-suds--regular-f40.png",
        "fx-dishwasher-suds--emphatic-f40.png": V41_RAW / "fx-dishwasher-suds--emphatic-f40.png",
    }
    for name in (
        "join-body-backfill-template.png", "countertop-join-cap-template.png",
        "countertop-triangle-underlay-template.png", "neighbour-seam-cleanup-left.png",
        "neighbour-seam-cleanup-right.png",
    ):
        mapping[name] = FITTED / "healing" / name
    for unit in ("a", "b"):
        for suffix in ("le-re", "le-rj", "lj-re", "lj-rj"):
            name = f"cabinet-{unit}-{suffix}.png"
            mapping[name] = FITTED / "cabinets" / name
    for state in ("off", "on", "broken"):
        for suffix in ("", "-le-re", "-le-rj", "-lj-re", "-lj-rj"):
            name = f"dishwasher-{state}{suffix}.png"
            mapping[name] = DISHWASHER / name
    return mapping


def make_cabinet_run(path: Path) -> None:
    left = Image.open(FITTED / "cabinets" / "cabinet-a-le-rj.png").convert("RGBA")
    right = Image.open(FITTED / "cabinets" / "cabinet-b-lj-re.png").convert("RGBA")
    out = Image.new("RGBA", (176, 82), (0, 0, 0, 0))
    out.alpha_composite(left, (0, 0))
    out.alpha_composite(right, (84, 0))
    out.save(path, optimize=True)


def parse_data(html: str) -> tuple[dict[str, object], tuple[int, int]]:
    start = html.index("const DATA=") + len("const DATA=")
    end = html.index(",A='assets/'", start)
    return json.loads(html[start:end]), (start, end)


def transformed_html(source: str, published: dict[str, str]) -> str:
    data, (start, end) = parse_data(source)
    data["set"] = SET
    data["version"] = 42
    data["status"] = "immutable-review-candidate-not-approved-not-registered"
    data["sourceProvenance"] = {
        "interactionAuthority": "approved kitchen-dishwasher-workbench-v41",
        "fittedVisualAuthority": "approved kitchen-fitted-cabinet-ligne-claire-v3",
        "ovenVisualAuthority": "approved kitchen-oven-ligne-claire-v8",
        "dishwasherVisualCandidate": "kitchen-dishwasher-ligne-claire-v1",
    }
    data["publishedAssets"] = published
    data["boundaries"] = {
        "productionChanged": False,
        "runtimeChanged": False,
        "promotionPerformed": False,
        "interactionImplementationChanged": False,
        "approvalRequired": True,
    }
    replacement = json.dumps(data, separators=(",", ":"))
    html = source[:start] + replacement + source[end:]
    html = html.replace("<base href=\"/keeper-review/kitchen-dishwasher-workbench-v41/\">", f"<base href=\"/keeper-review/{SET}/\">")
    html = html.replace("Kitchen Dishwasher Workbench V41", "Kitchen Ligne-Claire Healing Workbench V42")
    html = html.replace("V41 reversible behaviour workbench", "V42 immutable Ligne-Claire healing workbench")
    html = html.replace("V40 pixels unchanged", "approved V3 fitted family")
    html = html.replace("<h1>Broken-state lock · effects stay with their appliance</h1>", "<h1>Ligne-Claire fitted family · exact V41 movement and healing</h1>")
    old_lede = "V41 changes no artwork. It demonstrates the binding kitchen rule that a broken movable asset keeps its exact snapped bay until repaired. The dishwasher's suds remain separate reusable animation layers, but every layer is owned by the dishwasher and stored in dishwasher-local coordinates, so the appliance and its effects cannot become detached."
    new_lede = "V42 preserves the approved V41 movement, locking, snap and healing implementation while substituting the approved fitted-family and oven artwork plus the reversible dishwasher candidate. Broken still locks position; repair still unlocks it; suds remain separate asset-local layers. Nothing on this page is registered or current."
    html = html.replace(old_lede, new_lede)
    html = html.replace("Loading and decoding all byte-identical V40 states, edge variants, join layers, proofs and forty-frame suds strips before interaction unlocks…", "Loading and decoding every unique root-absolute asset before interaction unlocks…")
    html = html.replace("Coordinated dishwasher family · 4× inspection", "Candidate dishwasher family · smooth inspection")
    html = html.replace("image-rendering:pixelated", "image-rendering:auto")
    html = html.replace("src=\"assets/", f"src=\"/keeper-review/{SET}/assets/")
    html = html.replace(",A='assets/'", f",A='/keeper-review/{SET}/assets/'")
    html = html.replace("ctx.drawImage(imgs['oven-off.png'],x-4,127)", "ctx.drawImage(imgs['oven-on.png'],x-4,127)")
    html = html.replace("All V41 controls are ready. Every image is byte-identical to V40; only the Broken-state movement rule and effect ownership changed.", "All V42 controls are ready. Every image decoded before interaction; V41 movement, state locking, effect ownership and healing logic remain unchanged.")
    proof_start = html.index('<section class="panel"><h2>Exact-game-size state proofs</h2>')
    proof_end = html.index('</section>', proof_start) + len('</section>')
    proof = f'''<section class="panel"><h2>Registration and visual audit</h2><p class="rule">Dishwasher canvas, alpha, padding and all four healing-edge variants are exact. Use the live room above to dislocate units and inspect both exposed and joined edges. The full current/candidate/ghost and 64 px evidence is preserved in the <a href="/keeper-review/kitchen-dishwasher-ligne-claire-v1/">dishwasher drawing review</a>.</p></section>'''
    html = html[:proof_start] + proof + html[proof_end:]
    boundary_start = html.index('<p class="warn"><strong>Review boundary:</strong>')
    boundary_end = html.index('</p>', boundary_start) + len('</p>')
    boundary = '<p class="warn"><strong>Review boundary:</strong> V42 is an immutable, unapproved integration proof. Approved V41 behaviour, approved V3/V8 art, all source files and all production selectors remain byte-for-byte untouched. Reject by deleting only this V42 pack and route.</p>'
    html = html[:boundary_start] + boundary + html[boundary_end:]
    return html


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable V42 workbench")
    ASSETS.mkdir(parents=True)
    PUBLIC_ASSETS.mkdir(parents=True)
    sources = asset_sources()
    for name, source in sources.items():
        if not source.exists():
            raise RuntimeError(f"missing asset authority: {source}")
        shutil.copy2(source, ASSETS / name)
    make_cabinet_run(ASSETS / "cabinet-run-v11-exact.png")
    sources["cabinet-run-v11-exact.png"] = ASSETS / "cabinet-run-v11-exact.png"
    published = {name: sha256(ASSETS / name) for name in sorted(sources)}
    source_html = V41_HTML.read_text(encoding="utf-8")
    html = transformed_html(source_html, published)
    (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    for name in published:
        shutil.copy2(ASSETS / name, PUBLIC_ASSETS / name)
    records = []
    for name, authority in sorted(sources.items()):
        candidate = ASSETS / name
        records.append({
            "filename": name,
            "authorityFile": authority.relative_to(ROOT).as_posix(),
            "authoritySha256": sha256(authority),
            "reviewFile": candidate.relative_to(ROOT).as_posix(),
            "reviewSha256": sha256(candidate),
            "byteExactToAuthority": sha256(authority) == sha256(candidate),
        })
    manifest = {
        "schema": "lighthouse-keeper/kitchen-ligne-claire-healing-workbench@42",
        "set": SET,
        "created": "2026-10-22",
        "status": "immutable-review-candidate-not-approved-not-registered",
        "v41HtmlAuthority": V41_HTML.relative_to(ROOT).as_posix(),
        "v41HtmlSha256": sha256(V41_HTML),
        "changes": ["root-absolute asset delivery", "smooth browser scaling", "approved/candidate Ligne-Claire asset substitution", "visible oven uses approved V8 On"],
        "unchanged": ["84 px bay origins", "snap and swap", "broken position lock", "repair unlock", "healing resolver", "draw order", "anchors", "effect ownership", "effect timing", "interaction state transitions"],
        "assets": records,
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True},
        "rollback": "Discard only this V42 pack and review route.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"schema": "lighthouse-keeper/kitchen-batch-register@42", "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n", encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    if manifest["registration"]["register"] or manifest["registration"]["promote"]:
        raise RuntimeError("registration gate opened")
    if sha256(V41_HTML) != manifest["v41HtmlSha256"]:
        raise RuntimeError("V41 behaviour authority changed")
    for record in manifest["assets"]:
        authority = ROOT / record["authorityFile"]
        review = ROOT / record["reviewFile"]
        if sha256(authority) != record["authoritySha256"] or sha256(review) != record["reviewSha256"]:
            raise RuntimeError(f"asset hash drift: {record['filename']}")
        if record["filename"] != "cabinet-run-v11-exact.png" and sha256(authority) != sha256(review):
            raise RuntimeError(f"asset not byte-exact to selected authority: {record['filename']}")
    html = (PUBLIC / "index.html").read_text(encoding="utf-8")
    required = [
        f"A='/keeper-review/{SET}/assets/'",
        "ctx.drawImage(imgs['oven-on.png'],x-4,127)",
        "image-rendering:auto",
        "function neighbours(", "function joins(", "function drawAsset(",
        "function setState(", "function tryMove(", "getElementById('rotate').onclick=", "canvas.onpointerdown=",
    ]
    for token in required:
        if token not in html:
            raise RuntimeError(f"missing V42 contract token: {token}")
    if "src=\"assets/" in html or "A='assets/'" in html or "image-rendering:pixelated" in html:
        raise RuntimeError("relative-path or pixelated-delivery regression")
    print(f"Verified V42: {len(manifest['assets'])} decoded assets, V41 interaction/healing implementation preserved, root-absolute smooth delivery")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
