#!/usr/bin/env python3
"""Build immutable Activity Cloud Composer V5 vocabulary expansion."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

import build_activity_cloud_composer_v1 as base


ROOT = Path(__file__).resolve().parents[1]
SET = "activity-cloud-composer-v5"
PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v5"
SOURCE_DIR = PACK / "source"
COMPONENTS = PACK / "drafts/components"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
PAGE = PUBLIC / "index.html"
CATALOGUE = PUBLIC / "catalogue.json"
V4_PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v4"
V4_REGISTER = V4_PACK / "batch-register.json"
V4_CATALOGUE = ROOT / "public/keeper-review/activity-cloud-composer-v4/catalogue.json"
V4_PAGE = ROOT / "public/keeper-review/activity-cloud-composer-v4/index.html"

CELLS = ((0, 0, 512, 512), (512, 0, 1024, 512), (1024, 0, 1536, 512),
         (0, 512, 512, 1024), (512, 512, 1024, 1024), (1024, 512, 1536, 1024))

SHEETS = (
    ("eggs-toast-source-sheet.png", (
        ("eggs-hen-coop", "eggs"), ("eggs-nest", "eggs"), ("eggs-basket", "eggs"),
        ("toast-toaster", "toast"), ("toast-slices", "toast"), ("toast-butter-jam", "toast"))),
    ("bathroom-source-sheet.png", (
        ("bathroom-toilet", "bathroom"), ("bathroom-toilet-roll", "bathroom"),
        ("bathroom-privacy-latch", "bathroom"), ("bathroom-bathtub", "bathroom"),
        ("bathroom-bubbles", "bathroom"), ("bathroom-rubber-duck", "bathroom"))),
    ("rest-reading-source-sheet.png", (
        ("rest-armchair", "rest"), ("rest-sleep-marks", "rest"),
        ("rest-blanket-pillow", "rest"), ("reading-open-book", "reading"),
        ("reading-pirate-ship", "reading"), ("reading-dragon", "reading"))),
    ("reading-pottery-source-sheet.png", (
        ("reading-treasure-chest", "reading"), ("reading-castle", "reading"),
        ("pottery-wheel", "pottery"), ("pottery-hands-moulding", "pottery"),
        ("pottery-wet-clay", "pottery"), ("pottery-vase", "pottery"))),
    ("writing-pet-source-sheet.png", (
        ("writing-fountain-pen", "writing"), ("writing-pencil", "writing"),
        ("writing-notebook", "writing"), ("writing-ink-bottle", "writing"),
        ("writing-eraser", "writing"), ("pet-food-bag", "pet-care"))),
    ("pet-fishing-source-sheet.png", (
        ("pet-bone", "pet-care"), ("pet-fish", "pet-care"), ("pet-heart", "pet-care"),
        ("pet-purr-marks", "pet-care"), ("pet-food-bowl", "pet-care"),
        ("fishing-rod", "fishing"))),
    ("fishing-exercise-source-sheet.png", (
        ("fishing-caught-fish", "fishing"), ("fishing-bait", "fishing"),
        ("fishing-float", "fishing"), ("fishing-tackle-box", "fishing"),
        ("exercise-sweat-drop", "exercise"), ("exercise-flexed-arm", "exercise"))),
    ("exercise-games-source-sheet.png", (
        ("exercise-dumbbell", "exercise"), ("exercise-trainers", "exercise"),
        ("exercise-skipping-rope", "exercise"), ("exercise-heart-pulse", "exercise"),
        ("games-playing-cards", "games"), ("games-dice", "games"))),
    ("games-repair-source-sheet.png", (
        ("games-board-and-pawns", "games"), ("games-chess-knight", "games"),
        ("repair-boat-hull-patch", "repair"), ("repair-petrol-fill", "repair"),
        ("repair-outboard-motor", "repair"), ("repair-wrench-cog", "repair"))),
    ("repair-source-sheet.png", (
        ("repair-rope-knot", "repair"), ("repair-tyre-pump", "repair"),
        ("repair-toolbox", "repair"), ("repair-hammer-nails", "repair"),
        ("repair-boat-varnish", "repair"), ("repair-battery-leads", "repair"))),
)

SUGGESTED_RECIPES = {
    "collecting-eggs": {"label": "Collecting eggs", "targetAssetLabel": "Chicken coop", "targetAssetId": "outdoor.chicken-coop", "bodyCompatibility": "rear-work-with-context", "elements": ["eggs-hen-coop", "eggs-nest", "eggs-basket", "mixing-egg"], "sfx": "coop-cluck"},
    "making-toast": {"label": "Making toast", "targetAssetLabel": "Toaster", "targetAssetId": "kitchen.toaster", "bodyCompatibility": "rear-work-with-context", "elements": ["toast-toaster", "toast-slices", "toast-butter-jam", "sandwich-bread"], "sfx": "toaster-pop"},
    "using-loo": {"label": "Using the loo", "targetAssetLabel": "Toilet", "targetAssetId": "bathroom.toilet", "bodyCompatibility": "dedicated-pose-required", "elements": ["bathroom-toilet", "bathroom-toilet-roll", "bathroom-privacy-latch", "bathroom-bubbles"], "sfx": "bathroom-door-close"},
    "soaking-in-bath": {"label": "Soaking in the bath", "targetAssetLabel": "Bath", "targetAssetId": "bathroom.bath", "bodyCompatibility": "dedicated-pose-required", "elements": ["bathroom-bathtub", "bathroom-bubbles", "bathroom-rubber-duck", "hygiene-shampoo"], "sfx": "bath-water"},
    "napping-armchair": {"label": "Napping in armchair", "targetAssetLabel": "Armchair", "targetAssetId": "lounge.armchair", "bodyCompatibility": "dedicated-pose-required", "elements": ["rest-armchair", "rest-sleep-marks", "rest-blanket-pillow", "tea-mug"], "sfx": "sleep-breath"},
    "reading-adventure": {"label": "Reading an adventure", "targetAssetLabel": "Reading chair", "targetAssetId": "lounge.reading-chair", "bodyCompatibility": "dedicated-pose-required", "elements": ["reading-open-book", "reading-pirate-ship", "reading-dragon", "reading-treasure-chest", "reading-castle"], "sfx": "page-turn"},
    "throwing-pottery": {"label": "Throwing pottery", "targetAssetLabel": "Pottery wheel", "targetAssetId": "workshop.pottery-wheel", "bodyCompatibility": "rear-work-with-context", "elements": ["pottery-wheel", "pottery-hands-moulding", "pottery-wet-clay", "pottery-vase"], "sfx": "pottery-wheel"},
    "writing": {"label": "Writing", "targetAssetLabel": "Writing desk", "targetAssetId": "study.writing-desk", "bodyCompatibility": "rear-work-with-context", "elements": ["writing-fountain-pen", "writing-pencil", "writing-notebook", "writing-ink-bottle", "writing-eraser"], "sfx": "pen-scratch"},
    "feeding-pet": {"label": "Feeding pet", "targetAssetLabel": "Pet feeding spot", "targetAssetId": "home.pet-feeding", "bodyCompatibility": "rear-work-with-context", "elements": ["pet-food-bag", "pet-bone", "pet-fish", "pet-heart", "pet-food-bowl"], "sfx": "pet-bowl"},
    "fishing": {"label": "Fishing", "targetAssetLabel": "Fishing spot", "targetAssetId": "outdoor.fishing-spot", "bodyCompatibility": "dedicated-pose-required", "elements": ["fishing-rod", "fishing-caught-fish", "fishing-bait", "fishing-float", "fishing-tackle-box"], "sfx": "fishing-cast"},
    "exercising": {"label": "Exercising", "targetAssetLabel": "Exercise mat", "targetAssetId": "home.exercise-mat", "bodyCompatibility": "dedicated-pose-required", "elements": ["exercise-sweat-drop", "exercise-flexed-arm", "exercise-dumbbell", "exercise-trainers", "exercise-skipping-rope"], "sfx": "exercise-effort"},
    "playing-games": {"label": "Playing cards or board game", "targetAssetLabel": "Games table", "targetAssetId": "lounge.games-table", "bodyCompatibility": "dedicated-pose-required", "elements": ["games-playing-cards", "games-dice", "games-board-and-pawns", "games-chess-knight"], "sfx": "game-piece"},
    "fixing-boat": {"label": "Fixing the boat", "targetAssetLabel": "Boat", "targetAssetId": "harbour.boat", "bodyCompatibility": "rear-work-with-context", "elements": ["repair-boat-hull-patch", "repair-outboard-motor", "repair-wrench-cog", "repair-rope-knot", "repair-toolbox"], "sfx": "boat-repair"},
    "filling-petrol": {"label": "Filling petrol", "targetAssetLabel": "Fuel point", "targetAssetId": "yard.fuel-point", "bodyCompatibility": "rear-work-with-context", "elements": ["repair-petrol-fill", "repair-outboard-motor", "repair-wrench-cog", "repair-battery-leads"], "sfx": "fuel-fill"},
    "general-mending": {"label": "General mending", "targetAssetLabel": "Repair bench", "targetAssetId": "workshop.repair-bench", "bodyCompatibility": "rear-work-with-context", "elements": ["repair-toolbox", "repair-hammer-nails", "repair-boat-varnish", "repair-battery-leads", "repair-tyre-pump"], "sfx": "repair-tools"},
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=None if compact else 2, separators=(",", ":") if compact else None) + "\n")


def page_v5() -> str:
    page = V4_PAGE.read_text()
    page = page.replace("Activity Cloud Composer V4", "Activity Cloud Composer V5")
    page = page.replace('href="/keeper-review/activity-cloud-composer-v3/index.html">← Immutable Composer V3', 'href="/keeper-review/activity-cloud-composer-v4/index.html">← Immutable Composer V4')
    page = page.replace('<span class="tag">V3 exact + deterministic music notation</span>', '<span class="tag">V4 exact + 60 household activity elements</span>')
    page = page.replace("const SET='activity-cloud-composer-v4',STORAGE='lighthouse-keeper.activity-cloud-composer-v4'", "const SET='activity-cloud-composer-v5',STORAGE='lighthouse-keeper.activity-cloud-composer-v5'")
    page = page.replace(
        '<h2 style="margin-top:18px">2 · Package elements</h2>',
        '<h2 style="margin-top:18px">2 · Package elements</h2><div class="actions"><select id="suggested"><option value="">Start from a suggested package…</option></select><button id="loadSuggested">Load package</button></div>',
    )
    old = "fetch(`/keeper-review/${SET}/catalogue.json`).then(r=>r.json()).then(async d=>{data=d;selection=[...d.defaultRecipe.elements];for(const family"
    new = "fetch(`/keeper-review/${SET}/catalogue.json`).then(r=>r.json()).then(async d=>{data=d;selection=[...d.defaultRecipe.elements];for(const [key,recipe] of Object.entries(d.suggestedRecipes)){const o=document.createElement('option');o.value=key;o.textContent=recipe.label;$('suggested').append(o)}for(const family"
    if old not in page:
        raise RuntimeError("V4 fetch contract changed")
    page = page.replace(old, new)
    anchor = "$('search').oninput=renderLibrary;"
    suggested = "$('loadSuggested').onclick=()=>{const r=data.suggestedRecipes[$('suggested').value];if(!r)return;$('activityLabel').value=r.label;$('recipeKey').value=$('suggested').value;$('targetLabel').value=r.targetAssetLabel;$('targetId').value=r.targetAssetId;$('compatibility').value=r.bodyCompatibility;$('sfx').value=r.sfx;selection=[...r.elements];updateAll()};"
    if anchor not in page:
        raise RuntimeError("V4 event contract changed")
    page = page.replace(anchor, suggested + anchor)
    page = page.replace("if(family!=='all'&&item.family!==family)continue;if(q&&!`${key} ${item.family}`.toLowerCase().includes(q))continue;", "const itemFamily=item.family||item.activity||'legacy';if(family!=='all'&&itemFamily!==family)continue;if(q&&!`${key} ${itemFamily}`.toLowerCase().includes(q))continue;")
    page = page.replace("fam.textContent=item.family", "fam.textContent=item.family||item.activity||'legacy'")
    page = page.replace("Object.values(d.components).map(v=>v.family)", "Object.values(d.components).map(v=>v.family||v.activity||'legacy')")
    return page


def main() -> None:
    for required in (V4_REGISTER, V4_CATALOGUE, V4_PAGE):
        if not required.exists():
            raise RuntimeError(f"missing dependency: {rel(required)}")

    v4 = json.loads(V4_CATALOGUE.read_text())
    v4_register = json.loads(V4_REGISTER.read_text())
    records, published, source_records = {}, [], []
    COMPONENTS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    for filename, specs in SHEETS:
        source_path = SOURCE_DIR / filename
        source = Image.open(source_path).convert("RGBA")
        if source.size != (1536, 1024):
            raise RuntimeError(f"unexpected source geometry: {filename} {source.size}")
        boundaries = {
            "verticalBoundaryX512AlphaPixels": base.boundary_count(source, "x", 512),
            "verticalBoundaryX1024AlphaPixels": base.boundary_count(source, "x", 1024),
            "horizontalBoundaryY512AlphaPixels": base.boundary_count(source, "y", 512),
        }
        if base.edge_alpha(source) or any(boundaries.values()):
            raise RuntimeError(f"source ownership failed: {filename} edge={base.edge_alpha(source)} {boundaries}")
        source_records.append({"file": rel(source_path), "sha256": sha(source_path), "pixels": list(source.size), "edgeAlphaPixels": base.edge_alpha(source), "cellBoundaryAlphaPixels": boundaries})
        for (name, family), crop in zip(specs, CELLS, strict=True):
            component, evidence = base.isolate(source, crop)
            if base.edge_alpha(component) or base.gutter(component) < 16:
                raise RuntimeError(f"unsafe component gutter: {name}")
            component_path = COMPONENTS / f"{name}.png"
            component.save(component_path)
            digest = sha(component_path)
            public_asset = ASSETS / f"{name}-{digest[:16]}.png"
            shutil.copyfile(component_path, public_asset)
            record = {**evidence, "file": rel(component_path), "sha256": digest, "family": family, "cellPixels": [base.CELL, base.CELL], "sourceSet": SET, "src": f"/keeper-review/{SET}/assets/{public_asset.name}"}
            records[name] = record
            published.append({"source": rel(component_path), "sourceSha256": digest, "public": rel(public_asset), "publicAssemblyPath": rel(public_asset), "publicSha256": sha(public_asset), "url": record["src"]})

    source_vocabulary = {"set": v4["set"], "catalogue": rel(V4_CATALOGUE), "catalogueSha256": sha(V4_CATALOGUE), "register": rel(V4_REGISTER), "registerSha256": sha(V4_REGISTER), "inheritedComponents": len(v4["components"])}
    components = {**v4["components"], **{name: {key: record[key] for key in ("src", "cellPixels", "family", "sourceSet", "sha256")} for name, record in records.items()}}
    composer = {**v4["composer"], "localStorageKey": "lighthouse-keeper.activity-cloud-composer-v5"}
    catalogue = {**v4, "set": SET, "sourceVocabulary": source_vocabulary, "components": components, "composer": composer, "suggestedRecipes": SUGGESTED_RECIPES}
    write_json(CATALOGUE, catalogue, compact=True)
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page_v5())

    register = {
        "schema": "lighthouse-keeper/activity-cloud-composer-register@5", "set": SET, "status": catalogue["status"],
        "sourceVocabulary": source_vocabulary, "generatedSources": source_records, "newComponents": records,
        "suggestedRecipes": SUGGESTED_RECIPES,
        "catalogue": {"file": rel(CATALOGUE), "sha256": sha(CATALOGUE), "components": len(components), "newComponents": len(records)},
        "page": {"file": rel(PAGE), "sha256": sha(PAGE)}, "candidate": {"publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)}},
        "publishedAssets": published,
        "checks": {"sourceEdgesClear": True, "sourceCellBoundariesClear": True, "componentGuttersClear": True, "componentOwnershipUnambiguous": True, "v4ComposerUnchanged": sha(V4_PAGE) == v4_register["page"]["sha256"], "primeBodyUnchanged": True, "runtimeChanged": False, "kitchenChanged": False, "deployed": False},
        "approvalBoundary": {"vocabularyApproved": False, "composerApproved": False, "recipesApproved": False, "runtimePromoted": False},
    }
    write_json(PACK / "batch-register.json", register)
    print(json.dumps({"set": SET, "components": len(components), "newComponents": len(records), "suggestedRecipes": len(SUGGESTED_RECIPES), "page": rel(PAGE)}, indent=2))


if __name__ == "__main__":
    main()
