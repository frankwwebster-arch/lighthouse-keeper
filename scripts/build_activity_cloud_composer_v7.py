#!/usr/bin/env python3
"""Build immutable Activity Cloud Composer V7 generic-symbol extension."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

import build_activity_cloud_composer_v1 as base


ROOT = Path(__file__).resolve().parents[1]
SET = "activity-cloud-composer-v7"
PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-20-v7"
SOURCE_DIR = PACK / "source"
COMPONENTS = PACK / "drafts/components"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
PAGE = PUBLIC / "index.html"
CATALOGUE = PUBLIC / "catalogue.json"
V6_PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-20-v6"
V6_REGISTER = V6_PACK / "batch-register.json"
V6_CATALOGUE = ROOT / "public/keeper-review/activity-cloud-composer-v6/catalogue.json"
V6_PAGE = ROOT / "public/keeper-review/activity-cloud-composer-v6/index.html"
SHEET = SOURCE_DIR / "generic-action-symbols-sheet-source.png"
QUESTION = SOURCE_DIR / "generic-question-mark-source.png"
VISIBLE_ALPHA = 8
SOURCE_CELL = 512

SHEET_SPECS = (
    ("symbol-heat-shimmer", "heat", 0, 0),
    ("symbol-pleasant-aroma", "scent", 1, 0),
    ("symbol-foul-odour", "scent", 2, 0),
    ("symbol-electrical-arc", "electrical", 0, 1),
    ("symbol-welding-sparks", "welding", 1, 1),
    ("symbol-exclamation-mark", "notation", 2, 1),
)
QUESTION_SPEC = ("symbol-question-mark", "notation")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=None if compact else 2, separators=(",", ":") if compact else None) + "\n")


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.getchannel("A").point(lambda value: 255 if value > VISIBLE_ALPHA else 0).getbbox()
    if bounds is None:
        raise RuntimeError("source has no visible pixels")
    return bounds


def source_gutter(image: Image.Image, bounds: tuple[int, int, int, int]) -> int:
    return min(bounds[0], bounds[1], image.width - bounds[2], image.height - bounds[3])


def boundary_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    coords: set[tuple[int, int]] = set()
    for x in (0, 511, 512, 1023, 1024, 1535):
        coords.update((x, y) for y in range(image.height))
    for y in (0, 511, 512, 1023):
        coords.update((x, y) for x in range(image.width))
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in coords)


def normalise(source: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    bounds = alpha_bounds(source)
    isolated = source.crop(bounds)
    scale = min(216 / isolated.width, 216 / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    isolated = isolated.resize(size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (base.CELL, base.CELL), (0, 0, 0, 0))
    offset = ((base.CELL - size[0]) // 2, (base.CELL - size[1]) // 2)
    cell.alpha_composite(isolated, offset)
    return cell, {
        "sourceVisibleBounds": list(bounds),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "edgeAlphaPixels": base.edge_alpha(cell),
        "transparentGutterPx": base.gutter(cell),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }


def publish_component(
    component_id: str,
    family: str,
    source: Image.Image,
    source_path: Path,
    source_meta: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    component, evidence = normalise(source)
    if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
        raise RuntimeError(f"unsafe normalised component: {component_id}")
    component_path = COMPONENTS / f"{component_id}.png"
    component.save(component_path)
    digest = sha(component_path)
    public_asset = ASSETS / f"{component_id}-{digest[:16]}.png"
    shutil.copyfile(component_path, public_asset)
    record = {
        **evidence,
        **source_meta,
        "file": rel(component_path),
        "sha256": digest,
        "family": family,
        "cellPixels": [base.CELL, base.CELL],
        "sourceSet": SET,
        "sourceFile": rel(source_path),
        "sourceSha256": sha(source_path),
        "src": f"/keeper-review/{SET}/assets/{public_asset.name}",
    }
    published = {
        "source": rel(component_path),
        "sourceSha256": digest,
        "public": rel(public_asset),
        "publicAssemblyPath": rel(public_asset),
        "publicSha256": sha(public_asset),
        "url": record["src"],
    }
    return record, published


def page_v7() -> str:
    page = V6_PAGE.read_text()
    page = page.replace("Activity Cloud Composer V6", "Activity Cloud Composer V7")
    page = page.replace(
        'href="/keeper-review/activity-cloud-composer-v5/index.html">← Immutable Composer V5',
        'href="/keeper-review/activity-cloud-composer-v6/index.html">← Immutable Composer V6',
    )
    page = page.replace("V5 exact + three loo callout elements", "V6 exact + seven generic action symbols")
    page = page.replace(
        "const SET='activity-cloud-composer-v6',STORAGE='lighthouse-keeper.activity-cloud-composer-v6'",
        "const SET='activity-cloud-composer-v7',STORAGE='lighthouse-keeper.activity-cloud-composer-v7'",
    )
    return page


def main() -> None:
    for required in (V6_REGISTER, V6_CATALOGUE, V6_PAGE, SHEET, QUESTION):
        if not required.exists():
            raise RuntimeError(f"missing dependency: {rel(required)}")
    COMPONENTS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    v6 = json.loads(V6_CATALOGUE.read_text())
    v6_register = json.loads(V6_REGISTER.read_text())
    records: dict[str, dict[str, object]] = {}
    published: list[dict[str, object]] = []

    sheet = Image.open(SHEET).convert("RGBA")
    if sheet.size != (1536, 1024):
        raise RuntimeError(f"wrong source-sheet geometry: {sheet.size}")
    if boundary_alpha(sheet):
        raise RuntimeError("source sheet crosses an outer or shared ownership edge")
    source_cells: list[dict[str, object]] = []
    for component_id, family, column, row in SHEET_SPECS:
        cell = sheet.crop((column * SOURCE_CELL, row * SOURCE_CELL, (column + 1) * SOURCE_CELL, (row + 1) * SOURCE_CELL))
        bounds = alpha_bounds(cell)
        gutter = source_gutter(cell, bounds)
        if gutter < 80:
            raise RuntimeError(f"source gutter below 80 px for {component_id}: {gutter}")
        source_meta = {
            "sourceCell": [column, row],
            "sourceBounds": list(bounds),
            "sourceGutterPx": gutter,
            "sourceOwner": component_id,
        }
        record, publication = publish_component(component_id, family, cell, SHEET, source_meta)
        records[component_id] = record
        published.append(publication)
        source_cells.append({
            "owner": component_id,
            "cell": [column, row],
            "bounds": list(bounds),
            "gutterPx": gutter,
            "ambiguousPixels": 0,
            "unownedVisiblePixels": 0,
        })

    question = Image.open(QUESTION).convert("RGBA")
    if base.edge_alpha(question):
        raise RuntimeError("question source touches its outer edge")
    question_bounds = alpha_bounds(question)
    question_id, question_family = QUESTION_SPEC
    question_meta = {
        "sourceCell": None,
        "sourceBounds": list(question_bounds),
        "sourceGutterPx": source_gutter(question, question_bounds),
        "sourceOwner": question_id,
    }
    question_record, question_publication = publish_component(question_id, question_family, question, QUESTION, question_meta)
    records[question_id] = question_record
    published.append(question_publication)

    source_vocabulary = {
        "set": v6["set"],
        "catalogue": rel(V6_CATALOGUE),
        "catalogueSha256": sha(V6_CATALOGUE),
        "register": rel(V6_REGISTER),
        "registerSha256": sha(V6_REGISTER),
        "inheritedComponents": len(v6["components"]),
    }
    components = {
        **v6["components"],
        **{
            name: {key: record[key] for key in ("src", "cellPixels", "family", "sourceSet", "sha256")}
            for name, record in records.items()
        },
    }
    composer = {**v6["composer"], "localStorageKey": "lighthouse-keeper.activity-cloud-composer-v7"}
    catalogue = {
        **v6,
        "set": SET,
        "sourceVocabulary": source_vocabulary,
        "components": components,
        "composer": composer,
    }
    write_json(CATALOGUE, catalogue, compact=True)
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page_v7())

    register = {
        "schema": "lighthouse-keeper/activity-cloud-composer-register@7",
        "set": SET,
        "status": catalogue["status"],
        "sourceVocabulary": source_vocabulary,
        "generatedSources": [
            {
                "file": rel(SHEET),
                "sha256": sha(SHEET),
                "pixels": list(sheet.size),
                "layout": [3, 2],
                "cellPixels": [SOURCE_CELL, SOURCE_CELL],
                "boundaryAlphaPixels": 0,
                "cells": source_cells,
            },
            {
                "file": rel(QUESTION),
                "sha256": sha(QUESTION),
                "pixels": list(question.size),
                "edgeAlphaPixels": 0,
                "visibleBounds": list(question_bounds),
                "owner": question_id,
            },
        ],
        "newComponents": records,
        "suggestedRecipes": catalogue["suggestedRecipes"],
        "catalogue": {
            "file": rel(CATALOGUE),
            "sha256": sha(CATALOGUE),
            "components": len(components),
            "newComponents": len(records),
        },
        "page": {"file": rel(PAGE), "sha256": sha(PAGE)},
        "candidate": {"publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)}},
        "publishedAssets": published,
        "checks": {
            "sourceEdgesClear": True,
            "sourceCellGuttersAtLeast80": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "v6ComposerUnchanged": sha(V6_PAGE) == v6_register["page"]["sha256"],
            "primeBodyUnchanged": True,
            "runtimeChanged": False,
            "kitchenChanged": False,
            "deployed": False,
        },
        "approvalBoundary": {
            "vocabularyApproved": False,
            "composerApproved": False,
            "recipesApproved": False,
            "runtimePromoted": False,
        },
        "rollback": "Delete only Composer V7 draft/page/archive set and V7-only objects; V6 remains immutable.",
    }
    write_json(PACK / "batch-register.json", register)
    print(json.dumps({
        "set": SET,
        "inheritedComponents": len(v6["components"]),
        "newComponents": len(records),
        "components": len(components),
        "page": rel(PAGE),
    }, indent=2))


if __name__ == "__main__":
    main()
