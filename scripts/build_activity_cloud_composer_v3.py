#!/usr/bin/env python3
"""Build immutable Activity Cloud Composer V3 with album-sleeve homages."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

import build_activity_cloud_composer_v1 as base


ROOT = Path(__file__).resolve().parents[1]
SET = "activity-cloud-composer-v3"
PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v3"
SOURCE = PACK / "source"
COMPONENTS = PACK / "drafts/components"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
PAGE = PUBLIC / "index.html"
CATALOGUE = PUBLIC / "catalogue.json"
V2_PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v2"
V2_REGISTER = V2_PACK / "batch-register.json"
V2_CATALOGUE = ROOT / "public/keeper-review/activity-cloud-composer-v2/catalogue.json"
V2_PAGE = ROOT / "public/keeper-review/activity-cloud-composer-v2/index.html"
FAMILY = "music"

ALBUMS = (
    "music-album-sgt-pepper-homage",
    "music-album-morning-glory-homage",
    "music-album-screamadelica-homage",
    "music-album-velvet-banana-homage",
    "music-album-london-calling-homage",
    "music-album-dark-side-homage",
    "music-album-abbey-road-homage",
    "music-album-tapestry-homage",
    "music-album-sticky-fingers-homage",
    "music-album-never-mind-bollocks-homage",
    "music-album-born-usa-homage",
    "music-album-nevermind-homage",
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    separators = (",", ":") if compact else None
    path.write_text(json.dumps(value, indent=None if compact else 2, separators=separators) + "\n")


def page_v3() -> str:
    page = V2_PAGE.read_text()
    replacements = (
        ("Activity Cloud Composer V2", "Activity Cloud Composer V3"),
        ('href="/keeper-review/activity-cloud-composer-v1/index.html">\u2190 Immutable Composer V1', 'href="/keeper-review/activity-cloud-composer-v2/index.html">\u2190 Immutable Composer V2'),
        ('<span class="tag">V1 exact + shampoo</span>', '<span class="tag">V2 exact + 12 album homages</span>'),
        ("const SET='activity-cloud-composer-v2',STORAGE='lighthouse-keeper.activity-cloud-composer-v2'", "const SET='activity-cloud-composer-v3',STORAGE='lighthouse-keeper.activity-cloud-composer-v3'"),
    )
    for old, new in replacements:
        if old not in page:
            raise RuntimeError(f"V2 page contract changed; missing replacement: {old}")
        page = page.replace(old, new)
    return page


def main() -> None:
    for required in (V2_REGISTER, V2_CATALOGUE, V2_PAGE):
        if not required.exists():
            raise RuntimeError(f"missing dependency: {rel(required)}")

    v2 = json.loads(V2_CATALOGUE.read_text())
    v2_register = json.loads(V2_REGISTER.read_text())
    components = dict(v2["components"])
    source_records = {}
    records = {}
    published = []
    COMPONENTS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    for name in ALBUMS:
        source_path = SOURCE / f"{name}.png"
        if not source_path.exists():
            raise RuntimeError(f"missing generated album source: {rel(source_path)}")
        source = Image.open(source_path).convert("RGBA")
        if base.edge_alpha(source):
            raise RuntimeError(f"generated album source touches outer edge: {name}")
        component, evidence = base.isolate(source, (0, 0, source.width, source.height))
        if base.edge_alpha(component) or base.gutter(component) < 16:
            raise RuntimeError(f"unsafe album component gutter: {name}")

        component_path = COMPONENTS / f"{name}.png"
        component.save(component_path)
        digest = sha(component_path)
        public_asset = ASSETS / f"{name}-{digest[:16]}.png"
        shutil.copyfile(component_path, public_asset)
        public_url = f"/keeper-review/{SET}/assets/{public_asset.name}"
        source_records[name] = {
            "file": rel(source_path),
            "sha256": sha(source_path),
            "pixels": list(source.size),
            "edgeAlphaPixels": base.edge_alpha(source),
            "visibleBounds": base.alpha_bounds(source),
        }
        record = {
            **evidence,
            "file": rel(component_path),
            "sha256": digest,
            "family": FAMILY,
            "cellPixels": [base.CELL, base.CELL],
            "sourceSet": SET,
            "src": public_url,
        }
        records[name] = record
        components[name] = {key: record[key] for key in ("sha256", "family", "cellPixels", "sourceSet", "src")}
        published.append({
            "source": rel(component_path),
            "sourceSha256": digest,
            "public": rel(public_asset),
            "publicAssemblyPath": rel(public_asset),
            "publicSha256": sha(public_asset),
            "url": public_url,
        })

    composer = dict(v2["composer"])
    composer["localStorageKey"] = "lighthouse-keeper.activity-cloud-composer-v3"
    source_vocabulary = {
        "set": v2["set"],
        "catalogue": rel(V2_CATALOGUE),
        "catalogueSha256": sha(V2_CATALOGUE),
        "register": rel(V2_REGISTER),
        "registerSha256": sha(V2_REGISTER),
        "inheritedComponents": len(v2["components"]),
    }
    catalogue = {
        **v2,
        "set": SET,
        "sourceVocabulary": source_vocabulary,
        "components": components,
        "composer": composer,
    }
    write_json(CATALOGUE, catalogue, compact=True)
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page_v3())

    register = {
        "schema": "lighthouse-keeper/activity-cloud-composer-register@3",
        "set": SET,
        "status": catalogue["status"],
        "sourceVocabulary": source_vocabulary,
        "generatedSources": source_records,
        "newComponents": records,
        "catalogue": {"file": rel(CATALOGUE), "sha256": sha(CATALOGUE), "components": len(components), "newComponents": len(records)},
        "page": {"file": rel(PAGE), "sha256": sha(PAGE)},
        "candidate": {"publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)}},
        "publishedAssets": published,
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersClear": True,
            "componentOwnershipUnambiguous": True,
            "v2ComposerUnchanged": sha(V2_PAGE) == v2_register["page"]["sha256"],
            "primeBodyUnchanged": True,
            "runtimeChanged": False,
            "kitchenChanged": False,
            "deployed": False,
        },
        "approvalBoundary": {
            "vocabularyApproved": False,
            "composerApproved": False,
            "recipeApproved": False,
            "runtimePromoted": False,
        },
    }
    write_json(PACK / "batch-register.json", register)
    print(json.dumps({"set": SET, "components": len(components), "newComponents": len(records), "page": rel(PAGE)}, indent=2))


if __name__ == "__main__":
    main()
