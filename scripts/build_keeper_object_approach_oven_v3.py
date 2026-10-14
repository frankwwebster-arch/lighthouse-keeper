#!/usr/bin/env python3
"""Build Oven Approach V3 with a corrected base datum and perspective study."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V1_PAGE = ROOT / "public/keeper-review/keeper-object-approach-oven-v1/index.html"
V1_REGISTER = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v1/batch-register.json"
PACK = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v3"
PUBLIC = ROOT / "public/keeper-review/keeper-object-approach-oven-v3"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


SPEC = {
    "schema": "lighthouse-keeper/room-perspective@1",
    "status": "draft-perspective-and-placement-awaiting-review",
    "oven": {
        "baseRaiseLp": 0.5,
        "reason": "The approved Keeper boot alpha ends 0.5 lp above the 40-lp cell bottom.",
        "footprintLp": [30, 30],
        "interactionCentreLp": 120,
    },
    "perspective": {
        "roomDepthLp": 42,
        "roomDepthIntervals": 4,
        "standardAssetDepthLp": 10.5,
        "assetBackPlaneZLp": 42,
        "assetFrontInteractionPlaneZLp": 31.5,
        "projectionDistanceLp": 1008,
        "horizonYLp": 20,
        "backWallAbsoluteScale": 0.96,
        "interactionPlaneAbsoluteScale": 32 / 33,
        "assetBackToFrontScale": 0.99,
        "assetBackEdgeRiseLp": 0.36,
        "authoringRule": "Normalize artwork at the front interaction plane; converge only the standard-depth rear face.",
    },
    "grid": {
        "worldPitchLp": 10.5,
        "worldPitchKu": 84,
        "storedInWorldSpace": True,
        "keeperScaleAtInteractionPlane": 1,
        "runtimeRasterScalingRequired": False,
        "collisionFootprintsChange": False,
        "authoringRounding": "Round projected density-8 coordinates to nearest ku; preserve bilateral symmetry; maximum 1-ku per-side error.",
    },
    "boundaries": {
        "approvedKeeperPixelsChanged": False,
        "approvedTimingChanged": False,
        "runtimeGridChanged": False,
        "productionChanged": False,
        "approvalChanged": False,
    },
}


PERSPECTIVE_HTML = r'''<article><h2>Perspective calibration · proposed 42-lp room depth</h2><p class="note">This is an authoring guide, not runtime scaling. Furniture fronts and the Keeper meet on the interaction plane at 100% canonical scale. A standard 10.5-lp-deep asset converges by only 1% from its front face to its rear face.</p><div class="perspectiveCards"><section><strong>Orthographic control · 0%</strong><svg viewBox="0 0 172 66" aria-label="Orthographic room-depth control"><rect x="1" y="1" width="170" height="54" fill="#15313d" stroke="#8da9b5"/><path d="M1 55H171" stroke="#d3ae75"/><rect x="71" y="25" width="30" height="30" fill="#6d737b" stroke="#dbe1e7"/><path d="M71 25h30M71 55h30" stroke="#fff" stroke-dasharray="2 2"/><text x="86" y="63" text-anchor="middle">no convergence</text></svg></section><section class="selected"><strong>Proposed · rear wall 4%; asset 1%</strong><svg viewBox="0 0 172 66" aria-label="Proposed slight room perspective"><rect x="1" y="1" width="170" height="54" fill="none" stroke="#526e7b" stroke-dasharray="2 2"/><path d="M4.4 1.8L167.6 1.8L167.6 54.6L4.4 54.6Z" fill="#15313d" stroke="#75e6a7"/><path d="M1 1L4.4 1.8M171 1L167.6 1.8M1 55L4.4 54.6M171 55L167.6 54.6" stroke="#75e6a7"/><path d="M71 55L71.15 24.8L100.85 24.8L101 55Z" fill="#6d737b" stroke="#dbe1e7"/><path d="M71.15 24.8H100.85" stroke="#fff" stroke-dasharray="2 2"/><text x="86" y="63" text-anchor="middle">selected calibration</text></svg></section><section><strong>Exaggerated control · 8%</strong><svg viewBox="0 0 172 66" aria-label="Exaggerated perspective control"><rect x="1" y="1" width="170" height="54" fill="none" stroke="#526e7b" stroke-dasharray="2 2"/><path d="M7.8 2.6L164.2 2.6L164.2 54.1L7.8 54.1Z" fill="#15313d" stroke="#e8b852"/><path d="M1 1L7.8 2.6M171 1L164.2 2.6M1 55L7.8 54.1M171 55L164.2 54.1" stroke="#e8b852"/><path d="M71 55L71.3 24.6L100.7 24.6L101 55Z" fill="#6d737b" stroke="#dbe1e7"/><text x="86" y="63" text-anchor="middle">comparison only</text></svg></section></div></article><section class="metrics"><article><div class="metric">42 lp</div><strong>notional room depth</strong><p>Four existing 10.5-lp modules.</p></article><article><div class="metric">10.5 lp</div><strong>standard asset depth</strong><p>One shared depth module for every furnishing unless later declared exceptional.</p></article><article><div class="metric">1%</div><strong>asset face convergence</strong><p>The rear face is 99% of the front face when normalised at the interaction lane.</p></article></section><article><h2>Grid consequence</h2><p>The 84-ku/10.5-lp snap lattice remains unchanged and is stored in unprojected world space. Every interaction root stays on its existing x anchor, and the Keeper stays at 100% canonical scale. Perspective is baked into room and asset construction guides; it does <strong>not</strong> rescale animation sprites at runtime. For density-8 exports, projected landmarks round to the nearest keeper unit while preserving bilateral symmetry.</p></article>'''


PERSPECTIVE_CSS = r'''.footDatum{position:absolute;left:0;right:0;border-top:1px dashed rgba(255,212,92,.9);z-index:4;pointer-events:none}.footDatum span{position:absolute;right:4px;bottom:2px;color:#ffe09d;background:#10232d;padding:1px 4px;font-size:10px}.perspectiveCards{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.perspectiveCards section{background:#0c1d26;border:1px solid #355363;border-radius:8px;padding:10px}.perspectiveCards section.selected{border-color:#75e6a7;box-shadow:0 0 0 2px rgba(117,230,167,.18)}.perspectiveCards svg{display:block;width:100%;margin-top:8px;background:#091820;border-radius:5px}.perspectiveCards text{fill:#c9e4ee;font:4px system-ui,sans-serif}@media(max-width:900px){.perspectiveCards{grid-template-columns:1fr}}'''


def main() -> None:
    if not V1_PAGE.exists() or not V1_REGISTER.exists():
        raise RuntimeError("Oven Approach V1 authority is missing")
    PACK.mkdir(parents=True, exist_ok=False)
    PUBLIC.mkdir(parents=True, exist_ok=False)
    spec_path = PACK / "room-perspective-v1.json"
    spec_path.write_text(json.dumps(SPEC, indent=2) + "\n")

    page = V1_PAGE.read_text()
    replacements = {
        "<title>Keeper oven approach V1</title>": "<title>Keeper oven approach V3</title>",
        "<h1>Oven approach V1 · walk → stop → turn fully away</h1>": "<h1>Oven approach V3 · corrected floor datum + perspective calibration</h1>",
        "The oven is deliberately an opaque block. Every Keeper image is exact approved artwork; only the candidate root translation remains under review.": "The oven remains an opaque proxy and every Keeper image remains exact approved artwork. V3 raises the proxy by the measured 0.5-lp boot gutter and proposes a shared perspective guide.",
        ".asset{position:absolute;bottom:0;": ".asset{position:absolute;bottom:0;",
        "The 30 × 30 lp oven block sits on the rear wall. The Keeper finishes on its centre interaction anchor. This is an authoring ruler, not a fixed device size.": "The oven base is raised exactly 0.5 lp to the approved Keeper's lowest opaque boot datum. The 30 × 30 lp proxy and interaction centre are otherwise unchanged.",
        "<div class=\"stage full\" id=\"fullStage\"><div class=\"floor\"></div><div class=\"asset\">": "<div class=\"stage full\" id=\"fullStage\"><div class=\"floor\"></div><div class=\"footDatum\"><span>shared boot / oven base</span></div><div class=\"asset\">",
        "<div class=\"stage detail\" id=\"detailStage\"><div class=\"floor\"></div><div class=\"asset\">": "<div class=\"stage detail\" id=\"detailStage\"><div class=\"floor\"></div><div class=\"footDatum\"><span>shared boot / oven base</span></div><div class=\"asset\">",
        "<article><h2>Boundary</h2>": PERSPECTIVE_HTML + "<article><h2>Boundary</h2>",
        "@media(max-width:760px)": PERSPECTIVE_CSS + "@media(max-width:760px)",
        "const DATA=": "const PERSPECTIVE=" + json.dumps(SPEC["perspective"], separators=(",", ":")) + ";const DATA=",
        "oven.style.height=`${DATA.oven.heightLp*scale}px`;target.style.left": "oven.style.height=`${DATA.oven.heightLp*scale}px`;oven.style.bottom=`${.5*scale}px`;const datum=el.querySelector('.footDatum');datum.style.bottom=`${.5*scale}px`;target.style.left",
        "This page changes no approved PNG, timing authority, Final lane, sprite manifest or runtime logic.": "This page changes no approved PNG, timing authority, Final lane, sprite manifest, runtime grid or runtime logic.",
    }
    for old, new in replacements.items():
        if old not in page:
            raise RuntimeError(f"V1 page pattern missing: {old[:80]}")
        page = page.replace(old, new, 1)
    output = PUBLIC / "index.html"
    output.write_text(page)
    register = {
        "schema": "lighthouse-keeper/review-batch@1",
        "batchId": "keeper-object-approach-oven-2026-10-14-v3",
        "status": SPEC["status"],
        "authorities": {
            "ovenApproachV1Register": {"file": str(V1_REGISTER.relative_to(ROOT)), "sha256": digest(V1_REGISTER)},
            "ovenApproachV1Page": {"file": str(V1_PAGE.relative_to(ROOT)), "sha256": digest(V1_PAGE)},
        },
        "spec": {"file": str(spec_path.relative_to(ROOT)), "sha256": digest(spec_path)},
        "reviewPage": {"file": str(output.relative_to(ROOT)), "sha256": digest(output)},
        "validation": {
            "ovenRaisedByExactBootGutter": True,
            "v1KeeperFrameUrlsReused": True,
            "worldGridUnchanged": True,
            "keeperInteractionScaleUnchanged": True,
            "approvedKeeperPixelsChanged": False,
            "runtimeChanged": False,
            "approvalChanged": False,
        },
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PACK / "HANDOFF.md").write_text("""# Keeper oven approach V3\n\nStatus: draft placement and perspective calibration awaiting Frank's review.\n\nV3 preserves every V1 Keeper frame URL, motion value and interaction x anchor. It raises only the opaque oven proxy by 0.5 lp so its base matches the approved Keeper's lowest opaque boot datum.\n\nThe perspective proposal uses a 42-lp room depth and one standard 10.5-lp asset-depth module. The back wall is 4% smaller than the open front. Normalised at the interaction plane, an asset's rear face is exactly 1% smaller than its front face. The 84-ku grid and Keeper scale remain unchanged.\n\nReview: `/keeper-review/keeper-object-approach-oven-v3/`. Nothing is approved or wired.\n""")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
