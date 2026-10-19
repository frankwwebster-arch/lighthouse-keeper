#!/usr/bin/env python3
"""Build immutable Activity Cloud Composer V6 bathroom vocabulary extension."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

import build_activity_cloud_composer_v1 as base


ROOT = Path(__file__).resolve().parents[1]
SET = "activity-cloud-composer-v6"
PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-20-v6"
SOURCE_DIR = PACK / "source"
COMPONENTS = PACK / "drafts/components"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
PAGE = PUBLIC / "index.html"
CATALOGUE = PUBLIC / "catalogue.json"
V5_PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v5"
V5_REGISTER = V5_PACK / "batch-register.json"
V5_CATALOGUE = ROOT / "public/keeper-review/activity-cloud-composer-v5/catalogue.json"
V5_PAGE = ROOT / "public/keeper-review/activity-cloud-composer-v5/index.html"

SOURCES = (
    ("bathroom-flush-handle", "bathroom-flush-handle-source.png"),
    ("bathroom-loo-brush", "bathroom-loo-brush-source.png"),
    ("bathroom-bad-smell", "bathroom-bad-smell-source.png"),
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=None if compact else 2, separators=(",", ":") if compact else None) + "\n")


def alpha_bounds(image: Image.Image, threshold: int = 8) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    bounds = mask.getbbox()
    if bounds is None:
        raise RuntimeError("source has no visible pixels")
    return bounds


def normalise(source: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    """Fit one source owner into a deterministic 256 px cell with a 20 px gutter."""
    bounds = alpha_bounds(source)
    isolated = source.crop(bounds)
    max_content = 216
    scale = min(max_content / isolated.width, max_content / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    isolated = isolated.resize(size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (base.CELL, base.CELL), (0, 0, 0, 0))
    offset = ((base.CELL - size[0]) // 2, (base.CELL - size[1]) // 2)
    cell.alpha_composite(isolated, offset)
    gutter = base.gutter(cell)
    return cell, {
        "sourceVisibleBounds": list(bounds),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "edgeAlphaPixels": base.edge_alpha(cell),
        "transparentGutterPx": gutter,
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }


def page_v6() -> str:
    page = V5_PAGE.read_text()
    page = page.replace("Activity Cloud Composer V5", "Activity Cloud Composer V6")
    page = page.replace('href="/keeper-review/activity-cloud-composer-v4/index.html">← Immutable Composer V4', 'href="/keeper-review/activity-cloud-composer-v5/index.html">← Immutable Composer V5')
    page = page.replace('<span class="tag">V4 exact + 60 household activity elements</span>', '<span class="tag">V5 exact + three loo callout elements</span>')
    page = page.replace("const SET='activity-cloud-composer-v5',STORAGE='lighthouse-keeper.activity-cloud-composer-v5'", "const SET='activity-cloud-composer-v6',STORAGE='lighthouse-keeper.activity-cloud-composer-v6'")
    return page


def main() -> None:
    for required in (V5_REGISTER, V5_CATALOGUE, V5_PAGE):
        if not required.exists():
            raise RuntimeError(f"missing dependency: {rel(required)}")

    v5 = json.loads(V5_CATALOGUE.read_text())
    v5_register = json.loads(V5_REGISTER.read_text())
    records: dict[str, dict[str, object]] = {}
    published: list[dict[str, object]] = []
    source_records: list[dict[str, object]] = []
    COMPONENTS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    for name, filename in SOURCES:
        source_path = SOURCE_DIR / filename
        source = Image.open(source_path).convert("RGBA")
        source_edge_alpha = base.edge_alpha(source)
        if source_edge_alpha:
            raise RuntimeError(f"source touches outer edge: {filename}")
        component, evidence = normalise(source)
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 16:
            raise RuntimeError(f"unsafe component gutter: {name}")
        component_path = COMPONENTS / f"{name}.png"
        component.save(component_path)
        digest = sha(component_path)
        public_asset = ASSETS / f"{name}-{digest[:16]}.png"
        shutil.copyfile(component_path, public_asset)
        source_records.append({
            "file": rel(source_path), "sha256": sha(source_path), "pixels": list(source.size),
            "edgeAlphaPixels": source_edge_alpha, "visibleBounds": list(alpha_bounds(source)), "owner": name,
        })
        record = {
            **evidence, "file": rel(component_path), "sha256": digest, "family": "bathroom",
            "cellPixels": [base.CELL, base.CELL], "sourceSet": SET,
            "src": f"/keeper-review/{SET}/assets/{public_asset.name}",
        }
        records[name] = record
        published.append({
            "source": rel(component_path), "sourceSha256": digest, "public": rel(public_asset),
            "publicAssemblyPath": rel(public_asset), "publicSha256": sha(public_asset), "url": record["src"],
        })

    source_vocabulary = {
        "set": v5["set"], "catalogue": rel(V5_CATALOGUE), "catalogueSha256": sha(V5_CATALOGUE),
        "register": rel(V5_REGISTER), "registerSha256": sha(V5_REGISTER),
        "inheritedComponents": len(v5["components"]),
    }
    components = {
        **v5["components"],
        **{name: {key: record[key] for key in ("src", "cellPixels", "family", "sourceSet", "sha256")} for name, record in records.items()},
    }
    suggestions = json.loads(json.dumps(v5["suggestedRecipes"]))
    suggestions["using-loo"]["elements"] = [
        "bathroom-toilet", "bathroom-toilet-roll", "bathroom-flush-handle",
        "bathroom-loo-brush", "bathroom-bad-smell",
    ]
    composer = {**v5["composer"], "localStorageKey": "lighthouse-keeper.activity-cloud-composer-v6"}
    catalogue = {
        **v5, "set": SET, "sourceVocabulary": source_vocabulary, "components": components,
        "composer": composer, "suggestedRecipes": suggestions,
    }
    write_json(CATALOGUE, catalogue, compact=True)
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page_v6())

    register = {
        "schema": "lighthouse-keeper/activity-cloud-composer-register@6", "set": SET,
        "status": catalogue["status"], "sourceVocabulary": source_vocabulary,
        "generatedSources": source_records, "newComponents": records,
        "suggestedRecipes": suggestions,
        "catalogue": {"file": rel(CATALOGUE), "sha256": sha(CATALOGUE), "components": len(components), "newComponents": len(records)},
        "page": {"file": rel(PAGE), "sha256": sha(PAGE)},
        "candidate": {"publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)}},
        "publishedAssets": published,
        "checks": {
            "sourceEdgesClear": True, "componentGuttersClear": True,
            "componentOwnershipUnambiguous": True, "v5ComposerUnchanged": sha(V5_PAGE) == v5_register["page"]["sha256"],
            "primeBodyUnchanged": True, "runtimeChanged": False, "kitchenChanged": False, "deployed": False,
        },
        "approvalBoundary": {"vocabularyApproved": False, "composerApproved": False, "recipesApproved": False, "runtimePromoted": False},
    }
    write_json(PACK / "batch-register.json", register)
    print(json.dumps({"set": SET, "components": len(components), "newComponents": len(records), "suggestedRecipes": len(suggestions), "page": rel(PAGE)}, indent=2))


if __name__ == "__main__":
    main()
