#!/usr/bin/env python3
"""Build immutable Activity Cloud Composer V2 with a shampoo token."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

import build_activity_cloud_composer_v1 as base


ROOT = Path(__file__).resolve().parents[1]
SET = "activity-cloud-composer-v2"
PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v2"
SOURCE = PACK / "source/hygiene-shampoo-generated-v1.png"
COMPONENT = PACK / "drafts/components/hygiene-shampoo.png"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
PAGE = PUBLIC / "index.html"
CATALOGUE = PUBLIC / "catalogue.json"
V1_PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v1"
V1_REGISTER = V1_PACK / "batch-register.json"
V1_CATALOGUE = ROOT / "public/keeper-review/activity-cloud-composer-v1/catalogue.json"
V1_PAGE = ROOT / "public/keeper-review/activity-cloud-composer-v1/index.html"
NAME = "hygiene-shampoo"
FAMILY = "hygiene"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    separators = (",", ":") if compact else None
    path.write_text(json.dumps(value, indent=None if compact else 2, separators=separators) + "\n")


def page_v2() -> str:
    page = base.build_page()
    replacements = (
        ("Activity Cloud Composer V1", "Activity Cloud Composer V2"),
        ('href="/keeper-review/keeper-prime-back-work-activity-callout-v3/index.html">← Immutable V3 vocabulary', 'href="/keeper-review/activity-cloud-composer-v1/index.html">← Immutable Composer V1'),
        ('<span class="tag">Review-only tool</span>', '<span class="tag">Review-only tool</span><span class="tag">V1 exact + shampoo</span>'),
        ("const SET='activity-cloud-composer-v1',STORAGE='lighthouse-keeper.activity-cloud-composer-v1'", "const SET='activity-cloud-composer-v2',STORAGE='lighthouse-keeper.activity-cloud-composer-v2'"),
    )
    for old, new in replacements:
        if old not in page:
            raise RuntimeError(f"V1 page contract changed; missing replacement: {old}")
        page = page.replace(old, new)
    return page


def main() -> None:
    for required in (SOURCE, V1_REGISTER, V1_CATALOGUE, V1_PAGE):
        if not required.exists():
            raise RuntimeError(f"missing dependency: {rel(required)}")

    source = Image.open(SOURCE).convert("RGBA")
    if base.edge_alpha(source):
        raise RuntimeError("generated shampoo source touches its outer edge")
    component, evidence = base.isolate(source, (0, 0, source.width, source.height))
    if base.edge_alpha(component) or base.gutter(component) < 16:
        raise RuntimeError("unsafe shampoo component gutter")

    COMPONENT.parent.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    component.save(COMPONENT)
    digest = sha(COMPONENT)
    public_asset = ASSETS / f"{NAME}-{digest[:16]}.png"
    shutil.copyfile(COMPONENT, public_asset)
    public_url = f"/keeper-review/{SET}/assets/{public_asset.name}"

    v1 = json.loads(V1_CATALOGUE.read_text())
    v1_register = json.loads(V1_REGISTER.read_text())
    components = dict(v1["components"])
    components[NAME] = {
        "sha256": digest,
        "family": FAMILY,
        "cellPixels": [base.CELL, base.CELL],
        "sourceSet": SET,
        "src": public_url,
    }
    composer = dict(v1["composer"])
    composer["localStorageKey"] = "lighthouse-keeper.activity-cloud-composer-v2"
    catalogue = {
        **v1,
        "set": SET,
        "sourceVocabulary": {
            "set": v1["set"],
            "catalogue": rel(V1_CATALOGUE),
            "catalogueSha256": sha(V1_CATALOGUE),
            "register": rel(V1_REGISTER),
            "registerSha256": sha(V1_REGISTER),
            "inheritedComponents": len(v1["components"]),
        },
        "components": components,
        "composer": composer,
    }
    write_json(CATALOGUE, catalogue, compact=True)
    PAGE.write_text(page_v2())

    published = [{
        "source": rel(COMPONENT),
        "sourceSha256": digest,
        "public": rel(public_asset),
        "publicAssemblyPath": rel(public_asset),
        "publicSha256": sha(public_asset),
        "url": public_url,
    }]
    register = {
        "schema": "lighthouse-keeper/activity-cloud-composer-register@2",
        "set": SET,
        "status": catalogue["status"],
        "sourceVocabulary": catalogue["sourceVocabulary"],
        "generatedSource": {
            "file": rel(SOURCE),
            "sha256": sha(SOURCE),
            "pixels": list(source.size),
            "edgeAlphaPixels": base.edge_alpha(source),
            "visibleBounds": base.alpha_bounds(source),
        },
        "newComponents": {
            NAME: {
                **evidence,
                "file": rel(COMPONENT),
                "sha256": digest,
                "family": FAMILY,
                "cellPixels": [base.CELL, base.CELL],
                "sourceSet": SET,
                "src": public_url,
            }
        },
        "catalogue": {"file": rel(CATALOGUE), "sha256": sha(CATALOGUE), "components": len(components), "newComponents": 1},
        "page": {"file": rel(PAGE), "sha256": sha(PAGE)},
        "candidate": {"publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)}},
        "publishedAssets": published,
        "checks": {
            "sourceEdgesClear": True,
            "componentGutterClear": True,
            "componentOwnershipUnambiguous": True,
            "v1ComposerUnchanged": sha(V1_PAGE) == v1_register["page"]["sha256"],
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
    print(json.dumps({"set": SET, "components": len(components), "newComponent": NAME, "page": rel(PAGE)}, indent=2))


if __name__ == "__main__":
    main()
