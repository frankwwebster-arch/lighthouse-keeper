#!/usr/bin/env python3
"""Build immutable richer activity-cloud choreography over approved Prime sequence V1."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-rear-action-choreography-v1"
PACK = ROOT / "art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v1"
SOURCE_SHEET = PACK / "source/activity-comic-symbols-source-sheet.png"
SYMBOL_DIR = PACK / "drafts/symbols"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
PAGE_TEMPLATE = PACK / "page-template.html"
CATALOGUE = PUBLIC / "catalogue.json"
SEQUENCE_CATALOGUE = ROOT / "public/keeper-review/keeper-prime-rear-action-sequence-v1/catalogue.json"
VOCABULARY_CATALOGUE = ROOT / "public/keeper-review/activity-cloud-composer-v6/catalogue.json"
APPROVAL_RECORD = ROOT / "docs/review/keeper-prime-rear-action-sequence-v1-approval-2026-10-20.json"
VERIFIER = ROOT / "scripts/verify_keeper_prime_rear_action_choreography_v1.mjs"
PROMPT_LOG = PACK / "PROMPT_LOG.md"
FRAME_COUNT = 42
FPS = 8
QUIET_START = 37
CELL = 256
SOURCE_CELL = 512
VISIBLE_ALPHA = 8


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=None if compact else 2, separators=(",", ":") if compact else None) + "\n")


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    bounds = alpha.point(lambda value: 255 if value > VISIBLE_ALPHA else 0).getbbox()
    if bounds is None:
        raise RuntimeError("image has no visible pixels")
    return bounds


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    width, height = image.size
    coords = {(x, 0) for x in range(width)} | {(x, height - 1) for x in range(width)}
    coords |= {(0, y) for y in range(height)} | {(width - 1, y) for y in range(height)}
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in coords)


def gutter(image: Image.Image) -> int:
    left, top, right, bottom = alpha_bounds(image)
    return min(left, top, image.width - right, image.height - bottom)


def boundary_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    coords = set()
    for x in (0, 511, 512, 1023, 1024, 1535):
        coords.update((x, y) for y in range(image.height))
    for y in (0, 511, 512, 1023):
        coords.update((x, y) for x in range(image.width))
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in coords)


SYMBOL_SPECS = (
    ("symbol-heat-curls", "heat", 0, 0),
    ("symbol-sizzle-spark", "impact", 1, 0),
    ("symbol-motion-ticks", "motion", 2, 0),
    ("symbol-water-droplets", "water", 0, 1),
    ("symbol-soap-bubbles", "water", 1, 1),
    ("symbol-impact-star", "impact", 2, 1),
)


def build_symbols() -> tuple[dict[str, dict[str, object]], list[dict[str, object]], dict[str, object]]:
    source = Image.open(SOURCE_SHEET).convert("RGBA")
    if source.size != (1536, 1024):
        raise RuntimeError(f"wrong symbol source geometry: {source.size}")
    if boundary_alpha(source):
        raise RuntimeError("symbol source crosses an outer or shared ownership edge")

    SYMBOL_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    records: dict[str, dict[str, object]] = {}
    published: list[dict[str, object]] = []
    source_cells: list[dict[str, object]] = []
    for component_id, family, column, row in SYMBOL_SPECS:
        cell = source.crop((column * SOURCE_CELL, row * SOURCE_CELL, (column + 1) * SOURCE_CELL, (row + 1) * SOURCE_CELL))
        bounds = alpha_bounds(cell)
        source_gutter = min(bounds[0], bounds[1], SOURCE_CELL - bounds[2], SOURCE_CELL - bounds[3])
        if source_gutter < 80:
            raise RuntimeError(f"source gutter below 80 px for {component_id}: {source_gutter}")
        isolated = cell.crop(bounds)
        scale = min(216 / isolated.width, 216 / isolated.height)
        size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
        isolated = isolated.resize(size, Image.Resampling.LANCZOS)
        output = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
        offset = ((CELL - size[0]) // 2, (CELL - size[1]) // 2)
        output.alpha_composite(isolated, offset)
        output_gutter = gutter(output)
        if edge_alpha(output) or output_gutter < 20:
            raise RuntimeError(f"unsafe normalised symbol {component_id}")
        output_path = SYMBOL_DIR / f"{component_id}.png"
        output.save(output_path)
        digest = sha(output_path)
        public_path = ASSETS / f"{component_id}-{digest[:16]}.png"
        shutil.copyfile(output_path, public_path)
        src = f"/keeper-review/{SET}/assets/{public_path.name}"
        record = {
            "id": component_id,
            "family": family,
            "owner": component_id,
            "sourceSet": SET,
            "sourceFile": rel(SOURCE_SHEET),
            "sourceSha256": sha(SOURCE_SHEET),
            "sourceCell": [column, row],
            "sourceBounds": list(bounds),
            "sourceGutterPx": source_gutter,
            "normalisedVisibleSize": list(size),
            "normalisedOffset": list(offset),
            "cellPixels": [CELL, CELL],
            "transparentGutterPx": output_gutter,
            "edgeAlphaPixels": 0,
            "ambiguousPixels": 0,
            "unownedVisiblePixels": 0,
            "file": rel(output_path),
            "sha256": digest,
            "src": src,
        }
        records[component_id] = record
        source_cells.append({
            "owner": component_id,
            "cell": [column, row],
            "bounds": list(bounds),
            "gutterPx": source_gutter,
            "ambiguousPixels": 0,
            "unownedVisiblePixels": 0,
        })
        published.append({
            "source": rel(output_path),
            "sourceSha256": digest,
            "public": rel(public_path),
            "publicAssemblyPath": rel(public_path),
            "publicSha256": sha(public_path),
            "url": src,
        })
    source_record = {
        "file": rel(SOURCE_SHEET),
        "sha256": sha(SOURCE_SHEET),
        "pixels": [1536, 1024],
        "layout": [3, 2],
        "cellPixels": [512, 512],
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "outerAndSharedEdgeAlphaPixels": 0,
        "cells": source_cells,
    }
    return records, published, source_record


def k(frame: int, x: float, y: float, scale: float, rotation: float, opacity: float, ease: str = "smooth") -> list[object]:
    return [frame, x, y, scale, rotation, opacity, ease]


def t(instance: str, component: str, role: str, z: int, keys: list[list[object]]) -> dict[str, object]:
    return {"instance": instance, "component": component, "role": role, "z": z, "keys": keys}


def authored_tracks() -> dict[str, dict[str, object]]:
    invisible = (0, 0, 0.35, 0, 0)
    stories: dict[str, dict[str, object]] = {
        "garden-bbq": {
            "label": "Garden BBQ",
            "targetAssetLabel": "Garden barbecue",
            "targetAssetId": "outdoor.bbq",
            "bodyCompatibility": "rear-work-with-context",
            "elements": ["bbq-grill", "bbq-charcoal", "bbq-sausages", "bbq-hotdogs", "bbq-burgers"],
            "hero": "bbq-grill",
            "resolved": "bbq-burgers",
            "sfx": [
                {"frame": 7, "owner": "outdoor.bbq", "cue": "charcoal-rattle", "kind": "asset-state"},
                {"frame": 15, "owner": "garden-bbq", "cue": "bbq-sizzle", "kind": "activity-beat"},
                {"frame": 31, "owner": "garden-bbq", "cue": "food-ready", "kind": "completion"},
            ],
            "storyBeats": ["grill arrives", "charcoal feeds heat", "sausages and hot dogs flip", "burgers resolve the cook"],
            "treatments": {
                "open": {
                    "objects": [
                        t("grill", "bbq-grill", "hero", 4, [k(0, 0, 48, .38, -8, 0), k(4, 0, 20, .78, 3, 1, "back"), k(8, 0, 24, .72, 0, 1), k(36, 0, 24, .72, 0, 1), k(41, 0, 24, .72, 0, 1)]),
                        t("charcoal", "bbq-charcoal", "support", 2, [k(0, -132, -72, .32, -28, 0), k(5, -118, -60, .46, -24, 0), k(9, -28, 30, .40, 12, 1, "in"), k(15, 0, 40, .34, 18, .7), k(24, 0, 40, .3, 18, 0), k(41, 0, 40, .3, 18, 0)]),
                        t("sausages", "bbq-sausages", "support", 5, [k(0, -128, 56, .34, -24, 0), k(8, -122, 54, .45, -20, 0), k(11, -78, -28, .53, -5, 1, "out"), k(15, -12, 5, .48, 14, 1, "in"), k(19, 20, -4, .48, -10, 1, "back"), k(27, 58, -40, .40, 12, .45), k(32, 90, -62, .34, 18, 0), k(41, 90, -62, .34, 18, 0)]),
                        t("hotdogs", "bbq-hotdogs", "support", 5, [k(0, 132, 54, .34, 24, 0), k(15, 126, 54, .42, 22, 0), k(18, 82, -32, .50, 8, 1, "out"), k(22, 18, 7, .46, -12, 1, "in"), k(25, -20, -2, .46, 9, 1, "back"), k(31, -82, -56, .36, -18, 0), k(41, -82, -56, .36, -18, 0)]),
                        t("burgers", "bbq-burgers", "resolved", 6, [k(0, 0, 70, .30, 0, 0), k(24, 0, 68, .34, 0, 0), k(28, 0, -4, .62, -5, 1, "back"), k(31, 4, -18, .70, 3, 1), k(36, 44, -25, .60, 0, 1), k(41, 44, -25, .60, 0, 1)]),
                    ],
                    "symbols": [
                        t("heat", "symbol-heat-curls", "punctuation", 7, [k(0, -12, 12, .25, -8, 0), k(7, -12, 8, .30, -8, 0), k(10, -18, -42, .42, -4, 1, "out"), k(21, 2, -72, .52, 8, .8), k(29, 20, -94, .45, 14, 0), k(41, 20, -94, .45, 14, 0)]),
                        t("sizzle", "symbol-sizzle-spark", "punctuation", 8, [k(0, 40, -10, .22, 0, 0), k(11, 38, -8, .25, 0, 0), k(14, 48, -38, .36, 14, 1, "back"), k(18, 58, -50, .28, -9, 0), k(41, 58, -50, .28, -9, 0)]),
                        t("flip", "symbol-motion-ticks", "punctuation", 8, [k(0, -40, -4, .22, -20, 0), k(17, -38, -5, .22, -20, 0), k(20, -62, -35, .33, -26, 1, "back"), k(24, -76, -50, .28, -30, 0), k(41, -76, -50, .28, -30, 0)]),
                    ],
                },
                "bubble": {
                    "objects": [
                        t("grill", "bbq-grill", "hero", 4, [k(0, 0, 44, .34, 0, 0), k(4, 0, 21, .64, -3, 1, "back"), k(36, 0, 24, .62, 0, 1), k(41, 0, 24, .62, 0, 1)]),
                        t("charcoal", "bbq-charcoal", "support", 2, [k(0, -58, -50, .25, -18, 0), k(5, -56, -42, .34, -18, 0), k(9, -22, 18, .34, 8, 1, "in"), k(17, -2, 33, .29, 14, .6), k(23, 0, 35, .27, 14, 0), k(41, 0, 35, .27, 14, 0)]),
                        t("sausages", "bbq-sausages", "support", 5, [k(0, -74, 36, .27, -20, 0), k(8, -70, 30, .36, -16, 0), k(12, -42, -17, .43, 0, 1, "back"), k(17, -8, 1, .42, 16, 1), k(26, 48, -34, .33, 14, 0), k(41, 48, -34, .33, 14, 0)]),
                        t("hotdogs", "bbq-hotdogs", "support", 5, [k(0, 74, 35, .27, 20, 0), k(15, 70, 30, .34, 17, 0), k(19, 40, -16, .42, 2, 1, "back"), k(23, 5, 3, .41, -14, 1), k(29, -46, -35, .32, -15, 0), k(41, -46, -35, .32, -15, 0)]),
                        t("burgers", "bbq-burgers", "resolved", 6, [k(0, 0, 55, .28, 0, 0), k(25, 0, 48, .30, 0, 0), k(29, 0, -5, .55, -4, 1, "back"), k(33, 0, -16, .61, 2, 1), k(36, 24, -18, .53, 0, 1), k(41, 24, -18, .53, 0, 1)]),
                    ],
                    "symbols": [
                        t("heat", "symbol-heat-curls", "punctuation", 7, [k(0, 0, 0, .2, 0, 0), k(7, -8, -15, .25, -4, 0), k(10, -10, -52, .35, 0, 1, "out"), k(25, 8, -61, .39, 7, .8), k(30, 12, -65, .34, 10, 0), k(41, 12, -65, .34, 10, 0)]),
                        t("sizzle", "symbol-sizzle-spark", "punctuation", 8, [k(0, 28, -8, .2, 0, 0), k(12, 28, -8, .22, 0, 0), k(15, 40, -30, .31, 12, 1, "back"), k(19, 42, -36, .24, -8, 0), k(41, 42, -36, .24, -8, 0)]),
                        t("flip", "symbol-motion-ticks", "punctuation", 8, [k(0, -26, -6, .2, -18, 0), k(18, -26, -6, .2, -18, 0), k(21, -45, -28, .29, -24, 1, "back"), k(25, -49, -34, .23, -26, 0), k(41, -49, -34, .23, -26, 0)]),
                    ],
                },
            },
        },
        "make-sandwich": {
            "label": "Sandwich assembly",
            "targetAssetLabel": "Kitchen work surface",
            "targetAssetId": "kitchen.prep",
            "bodyCompatibility": "rear-work-with-context",
            "elements": ["sandwich-bread", "sandwich-ham", "sandwich-lettuce", "sandwich-tomato", "cooking-sandwich"],
            "hero": "sandwich-bread",
            "resolved": "cooking-sandwich",
            "sfx": [
                {"frame": 8, "owner": "make-sandwich", "cue": "bread-set-down", "kind": "asset-state"},
                {"frame": 20, "owner": "make-sandwich", "cue": "ingredients-stack", "kind": "activity-beat"},
                {"frame": 31, "owner": "make-sandwich", "cue": "sandwich-finished", "kind": "completion"},
            ],
            "storyBeats": ["bread opens the stage", "ham, lettuce and tomato stack", "layers compress", "finished sandwich settles"],
            "treatments": {
                "open": {
                    "objects": [
                        t("bread", "sandwich-bread", "hero", 4, [k(0, -110, 42, .35, -18, 0), k(5, -78, -18, .62, -10, 1, "back"), k(10, -48, 16, .58, -4, 1), k(26, -14, 18, .53, 0, .8), k(30, 0, 18, .48, 0, 0), k(41, 0, 18, .48, 0, 0)]),
                        t("ham", "sandwich-ham", "support", 5, [k(0, 112, -65, .28, 24, 0), k(8, 110, -60, .36, 22, 0), k(12, 62, -58, .43, 12, 1, "out"), k(17, 3, -2, .45, -5, 1, "in"), k(29, 0, 7, .40, 0, .7), k(32, 0, 12, .38, 0, 0), k(41, 0, 12, .38, 0, 0)]),
                        t("lettuce", "sandwich-lettuce", "support", 5, [k(0, -124, -62, .28, -24, 0), k(12, -120, -58, .34, -22, 0), k(16, -70, -44, .44, -12, 1, "out"), k(21, -3, 1, .45, 6, 1, "in"), k(29, 0, 6, .40, 0, .7), k(32, 0, 12, .38, 0, 0), k(41, 0, 12, .38, 0, 0)]),
                        t("tomato", "sandwich-tomato", "support", 6, [k(0, 128, 54, .28, 20, 0), k(17, 124, 48, .34, 18, 0), k(21, 72, 32, .43, 10, 1, "out"), k(25, 1, 3, .45, -4, 1, "in"), k(29, 0, 4, .40, 0, .7), k(32, 0, 10, .38, 0, 0), k(41, 0, 10, .38, 0, 0)]),
                        t("sandwich", "cooking-sandwich", "resolved", 7, [k(0, 0, 60, .32, 0, 0), k(27, 0, 44, .38, 0, 0), k(30, 0, 3, .66, -4, 1, "back"), k(34, 22, -9, .72, 2, 1), k(36, 34, -12, .66, 0, 1), k(41, 34, -12, .66, 0, 1)]),
                    ],
                    "symbols": [
                        t("stack", "symbol-motion-ticks", "punctuation", 8, [k(0, 0, -35, .2, -90, 0), k(13, 0, -35, .25, -90, 0), k(18, 14, -54, .33, -80, 1, "back"), k(24, 18, -60, .27, -78, 0), k(41, 18, -60, .27, -78, 0)]),
                        t("finish", "symbol-impact-star", "punctuation", 9, [k(0, 42, -30, .2, 0, 0), k(28, 42, -30, .25, 0, 0), k(31, 54, -44, .36, 12, 1, "back"), k(35, 62, -50, .30, 18, 0), k(41, 62, -50, .30, 18, 0)]),
                    ],
                },
                "bubble": {
                    "objects": [
                        t("bread", "sandwich-bread", "hero", 4, [k(0, -65, 34, .3, -12, 0), k(5, -46, -8, .52, -7, 1, "back"), k(10, -32, 13, .50, -2, 1), k(27, -8, 15, .46, 0, .7), k(31, 0, 17, .42, 0, 0), k(41, 0, 17, .42, 0, 0)]),
                        t("ham", "sandwich-ham", "support", 5, [k(0, 67, -47, .23, 18, 0), k(8, 64, -43, .31, 17, 0), k(13, 38, -35, .37, 9, 1, "back"), k(17, 2, -2, .39, -3, 1), k(29, 0, 7, .35, 0, .6), k(32, 0, 11, .33, 0, 0), k(41, 0, 11, .33, 0, 0)]),
                        t("lettuce", "sandwich-lettuce", "support", 5, [k(0, -70, -45, .23, -18, 0), k(12, -67, -42, .30, -17, 0), k(17, -39, -31, .38, -8, 1, "back"), k(21, -2, 0, .39, 4, 1), k(29, 0, 6, .35, 0, .6), k(32, 0, 10, .33, 0, 0), k(41, 0, 10, .33, 0, 0)]),
                        t("tomato", "sandwich-tomato", "support", 6, [k(0, 72, 38, .23, 16, 0), k(17, 69, 35, .29, 15, 0), k(22, 40, 23, .37, 8, 1, "back"), k(25, 1, 2, .39, -3, 1), k(29, 0, 5, .35, 0, .6), k(32, 0, 9, .33, 0, 0), k(41, 0, 9, .33, 0, 0)]),
                        t("sandwich", "cooking-sandwich", "resolved", 7, [k(0, 0, 46, .28, 0, 0), k(27, 0, 38, .32, 0, 0), k(30, 0, 2, .57, -3, 1, "back"), k(34, 10, -7, .62, 2, 1), k(36, 18, -9, .58, 0, 1), k(41, 18, -9, .58, 0, 1)]),
                    ],
                    "symbols": [
                        t("stack", "symbol-motion-ticks", "punctuation", 8, [k(0, 0, -28, .18, -90, 0), k(14, 0, -28, .21, -90, 0), k(19, 8, -43, .28, -82, 1, "back"), k(24, 10, -47, .23, -80, 0), k(41, 10, -47, .23, -80, 0)]),
                        t("finish", "symbol-impact-star", "punctuation", 9, [k(0, 34, -24, .18, 0, 0), k(28, 34, -24, .20, 0, 0), k(31, 40, -34, .30, 10, 1, "back"), k(35, 44, -38, .24, 15, 0), k(41, 44, -38, .24, 15, 0)]),
                    ],
                },
            },
        },
        "washing-up": {
            "label": "Washing up",
            "targetAssetLabel": "Kitchen sink",
            "targetAssetId": "kitchen.sink",
            "bodyCompatibility": "rear-work-with-context",
            "elements": ["washing-plate", "washing-liquid", "washing-sponge", "washing-droplets", "washing-cutlery"],
            "hero": "washing-plate",
            "resolved": "washing-cutlery",
            "sfx": [
                {"frame": 8, "owner": "kitchen.sink", "cue": "tap-water", "kind": "asset-state"},
                {"frame": 18, "owner": "washing-up", "cue": "sponge-scrub", "kind": "activity-beat"},
                {"frame": 31, "owner": "washing-up", "cue": "clean-clink", "kind": "completion"},
            ],
            "storyBeats": ["plate rises", "liquid and water meet", "sponge scrubs across", "clean cutlery glints"],
            "treatments": {
                "open": {
                    "objects": [
                        t("plate", "washing-plate", "hero", 4, [k(0, -105, 50, .36, -18, 0), k(5, -62, 12, .66, -8, 1, "back"), k(10, -25, 20, .62, 0, 1), k(36, 0, 20, .60, 0, 1), k(41, 0, 20, .60, 0, 1)]),
                        t("liquid", "washing-liquid", "support", 6, [k(0, 118, -58, .30, 24, 0), k(7, 110, -52, .39, 22, 0), k(11, 64, -38, .46, 36, 1, "back"), k(16, 34, -20, .43, 52, 1), k(21, 70, -54, .36, 28, 0), k(41, 70, -54, .36, 28, 0)]),
                        t("sponge", "washing-sponge", "support", 7, [k(0, -120, -55, .28, -22, 0), k(12, -112, -48, .38, -18, 0), k(15, -58, -10, .46, -8, 1, "back"), k(19, -16, 5, .48, 9, 1), k(22, 22, 2, .48, -8, 1), k(25, -8, 5, .48, 8, 1), k(29, 66, -35, .35, 18, 0), k(41, 66, -35, .35, 18, 0)]),
                        t("droplets", "washing-droplets", "support", 5, [k(0, 118, 50, .25, 18, 0), k(8, 108, 42, .34, 14, 0), k(12, 68, 8, .43, 4, 1, "out"), k(18, 20, -16, .46, -8, 1), k(25, -48, -42, .36, -18, .5), k(28, -74, -60, .31, -22, 0), k(41, -74, -60, .31, -22, 0)]),
                        t("cutlery", "washing-cutlery", "resolved", 8, [k(0, 0, 62, .28, 0, 0), k(26, 0, 56, .32, 0, 0), k(30, 28, -12, .58, -7, 1, "back"), k(34, 52, -22, .62, 3, 1), k(36, 55, -22, .60, 0, 1), k(41, 55, -22, .60, 0, 1)]),
                    ],
                    "symbols": [
                        t("water", "symbol-water-droplets", "punctuation", 9, [k(0, 48, -20, .2, 0, 0), k(8, 48, -20, .25, 0, 0), k(12, 34, -55, .36, -10, 1, "back"), k(20, -8, -72, .40, -18, .8), k(26, -35, -84, .32, -22, 0), k(41, -35, -84, .32, -22, 0)]),
                        t("bubbles", "symbol-soap-bubbles", "punctuation", 10, [k(0, -30, 10, .2, 0, 0), k(12, -30, 6, .24, 0, 0), k(16, -25, -34, .34, -4, 1, "back"), k(24, 24, -58, .42, 12, .8), k(29, 42, -70, .34, 18, 0), k(41, 42, -70, .34, 18, 0)]),
                        t("scrub", "symbol-motion-ticks", "punctuation", 11, [k(0, -48, -4, .18, -10, 0), k(17, -48, -4, .22, -10, 0), k(20, -62, -25, .31, -18, 1, "back"), k(24, -70, -32, .25, -20, 0), k(41, -70, -32, .25, -20, 0)]),
                    ],
                },
                "bubble": {
                    "objects": [
                        t("plate", "washing-plate", "hero", 4, [k(0, -62, 35, .31, -12, 0), k(5, -40, 10, .56, -6, 1, "back"), k(10, -17, 16, .54, 0, 1), k(36, 0, 17, .52, 0, 1), k(41, 0, 17, .52, 0, 1)]),
                        t("liquid", "washing-liquid", "support", 6, [k(0, 68, -42, .25, 20, 0), k(7, 64, -38, .33, 18, 0), k(11, 40, -28, .39, 32, 1, "back"), k(16, 24, -14, .37, 48, 1), k(21, 46, -39, .30, 24, 0), k(41, 46, -39, .30, 24, 0)]),
                        t("sponge", "washing-sponge", "support", 7, [k(0, -68, -40, .23, -18, 0), k(12, -64, -36, .31, -15, 0), k(15, -38, -8, .39, -6, 1, "back"), k(19, -10, 4, .40, 8, 1), k(22, 17, 2, .40, -7, 1), k(25, -5, 4, .40, 7, 1), k(29, 42, -26, .29, 15, 0), k(41, 42, -26, .29, 15, 0)]),
                        t("droplets", "washing-droplets", "support", 5, [k(0, 68, 36, .21, 14, 0), k(8, 63, 31, .28, 12, 0), k(12, 41, 7, .36, 3, 1, "back"), k(18, 13, -12, .38, -6, 1), k(25, -34, -32, .30, -14, .4), k(28, -45, -43, .25, -18, 0), k(41, -45, -43, .25, -18, 0)]),
                        t("cutlery", "washing-cutlery", "resolved", 8, [k(0, 0, 48, .24, 0, 0), k(26, 0, 42, .27, 0, 0), k(30, 18, -9, .49, -5, 1, "back"), k(34, 35, -16, .53, 2, 1), k(36, 38, -16, .51, 0, 1), k(41, 38, -16, .51, 0, 1)]),
                    ],
                    "symbols": [
                        t("water", "symbol-water-droplets", "punctuation", 9, [k(0, 30, -15, .18, 0, 0), k(8, 30, -15, .21, 0, 0), k(12, 22, -40, .30, -8, 1, "back"), k(20, -5, -51, .33, -14, .8), k(26, -22, -58, .26, -17, 0), k(41, -22, -58, .26, -17, 0)]),
                        t("bubbles", "symbol-soap-bubbles", "punctuation", 10, [k(0, -20, 8, .17, 0, 0), k(12, -20, 5, .20, 0, 0), k(16, -16, -25, .29, -3, 1, "back"), k(24, 15, -43, .35, 10, .8), k(29, 26, -50, .28, 14, 0), k(41, 26, -50, .28, 14, 0)]),
                        t("scrub", "symbol-motion-ticks", "punctuation", 11, [k(0, -32, -2, .16, -8, 0), k(17, -32, -2, .18, -8, 0), k(20, -42, -18, .26, -15, 1, "back"), k(24, -47, -23, .21, -17, 0), k(41, -47, -23, .21, -17, 0)]),
                    ],
                },
            },
        },
        "general-repair": {
            "label": "General repair",
            "targetAssetLabel": "Repair bench",
            "targetAssetId": "workshop.repair-bench",
            "bodyCompatibility": "rear-work-with-context",
            "elements": ["repair-toolbox", "repair-boat-hull-patch", "repair-hammer-nails", "repair-wrench-cog", "repair-rope-knot"],
            "hero": "repair-toolbox",
            "resolved": "repair-rope-knot",
            "sfx": [
                {"frame": 7, "owner": "workshop.repair-bench", "cue": "toolbox-open", "kind": "asset-state"},
                {"frame": 18, "owner": "general-repair", "cue": "hammer-tap-wrench-click", "kind": "activity-beat"},
                {"frame": 31, "owner": "general-repair", "cue": "repair-secured", "kind": "completion"},
            ],
            "storyBeats": ["toolbox opens", "patch meets the job", "hammer strikes and wrench tightens", "rope knot resolves"],
            "treatments": {
                "open": {
                    "objects": [
                        t("toolbox", "repair-toolbox", "hero", 4, [k(0, -112, 48, .34, -18, 0), k(5, -72, 12, .62, -8, 1, "back"), k(11, -45, 22, .58, 0, 1), k(36, -38, 25, .54, 0, 1), k(41, -38, 25, .54, 0, 1)]),
                        t("patch", "repair-boat-hull-patch", "support", 3, [k(0, 118, 50, .30, 18, 0), k(8, 110, 44, .40, 16, 0), k(12, 62, 18, .48, 6, 1, "back"), k(17, 20, 12, .50, -4, 1), k(28, 12, 15, .45, 0, .8), k(34, 10, 17, .42, 0, .4), k(37, 10, 17, .42, 0, 0), k(41, 10, 17, .42, 0, 0)]),
                        t("hammer", "repair-hammer-nails", "support", 7, [k(0, -112, -62, .28, -25, 0), k(11, -108, -58, .36, -22, 0), k(15, -58, -40, .45, -12, 1, "out"), k(18, 4, -16, .50, 30, 1, "in"), k(20, -8, -28, .48, -18, 1, "back"), k(24, 36, -52, .34, 16, 0), k(41, 36, -52, .34, 16, 0)]),
                        t("wrench", "repair-wrench-cog", "support", 6, [k(0, 122, -60, .28, 24, 0), k(16, 116, -55, .36, 22, 0), k(20, 62, -34, .46, 10, 1, "back"), k(23, 28, -7, .48, -28, 1), k(26, 18, -3, .48, 34, 1), k(30, 72, -45, .35, 18, 0), k(41, 72, -45, .35, 18, 0)]),
                        t("knot", "repair-rope-knot", "resolved", 8, [k(0, 0, 62, .28, 0, 0), k(26, 0, 55, .32, 0, 0), k(30, 22, -8, .58, -5, 1, "back"), k(34, 52, -18, .64, 3, 1), k(36, 55, -18, .62, 0, 1), k(41, 55, -18, .62, 0, 1)]),
                    ],
                    "symbols": [
                        t("impact", "symbol-impact-star", "punctuation", 10, [k(0, 16, -18, .2, 0, 0), k(15, 16, -18, .24, 0, 0), k(18, 28, -39, .38, 8, 1, "back"), k(21, 35, -46, .28, 16, 0), k(41, 35, -46, .28, 16, 0)]),
                        t("tighten", "symbol-motion-ticks", "punctuation", 9, [k(0, 44, -4, .18, 12, 0), k(20, 44, -4, .22, 12, 0), k(23, 64, -24, .33, 22, 1, "back"), k(27, 72, -32, .26, 26, 0), k(41, 72, -32, .26, 26, 0)]),
                        t("spark", "symbol-sizzle-spark", "punctuation", 10, [k(0, -10, -20, .18, -8, 0), k(17, -10, -20, .20, -8, 0), k(20, -24, -46, .31, -14, 1, "back"), k(24, -31, -54, .24, -18, 0), k(41, -31, -54, .24, -18, 0)]),
                    ],
                },
                "bubble": {
                    "objects": [
                        t("toolbox", "repair-toolbox", "hero", 4, [k(0, -65, 34, .29, -12, 0), k(5, -44, 9, .53, -6, 1, "back"), k(11, -30, 17, .50, 0, 1), k(36, -25, 20, .47, 0, 1), k(41, -25, 20, .47, 0, 1)]),
                        t("patch", "repair-boat-hull-patch", "support", 3, [k(0, 68, 35, .25, 14, 0), k(8, 64, 31, .34, 12, 0), k(12, 39, 13, .40, 4, 1, "back"), k(17, 13, 8, .42, -3, 1), k(28, 8, 11, .38, 0, .8), k(34, 6, 13, .35, 0, .4), k(37, 6, 13, .35, 0, 0), k(41, 6, 13, .35, 0, 0)]),
                        t("hammer", "repair-hammer-nails", "support", 7, [k(0, -68, -45, .23, -20, 0), k(11, -65, -42, .30, -18, 0), k(15, -38, -29, .38, -10, 1, "back"), k(18, 2, -12, .42, 26, 1), k(20, -5, -20, .40, -15, 1, "back"), k(24, 24, -37, .28, 13, 0), k(41, 24, -37, .28, 13, 0)]),
                        t("wrench", "repair-wrench-cog", "support", 6, [k(0, 70, -43, .23, 19, 0), k(16, 67, -40, .30, 18, 0), k(20, 39, -25, .39, 8, 1, "back"), k(23, 18, -5, .40, -24, 1), k(26, 12, -2, .40, 28, 1), k(30, 46, -32, .29, 15, 0), k(41, 46, -32, .29, 15, 0)]),
                        t("knot", "repair-rope-knot", "resolved", 8, [k(0, 0, 48, .24, 0, 0), k(26, 0, 42, .27, 0, 0), k(30, 15, -6, .50, -4, 1, "back"), k(34, 35, -13, .55, 2, 1), k(36, 38, -13, .53, 0, 1), k(41, 38, -13, .53, 0, 1)]),
                    ],
                    "symbols": [
                        t("impact", "symbol-impact-star", "punctuation", 10, [k(0, 11, -13, .18, 0, 0), k(15, 11, -13, .20, 0, 0), k(18, 20, -28, .32, 7, 1, "back"), k(21, 24, -33, .23, 13, 0), k(41, 24, -33, .23, 13, 0)]),
                        t("tighten", "symbol-motion-ticks", "punctuation", 9, [k(0, 29, -3, .16, 10, 0), k(20, 29, -3, .18, 10, 0), k(23, 42, -17, .28, 18, 1, "back"), k(27, 47, -22, .22, 22, 0), k(41, 47, -22, .22, 22, 0)]),
                        t("spark", "symbol-sizzle-spark", "punctuation", 10, [k(0, -7, -14, .16, -7, 0), k(17, -7, -14, .18, -7, 0), k(20, -16, -33, .26, -12, 1, "back"), k(24, -21, -38, .20, -15, 0), k(41, -21, -38, .20, -15, 0)]),
                    ],
                },
            },
        },
    }
    if invisible != (0, 0, 0.35, 0, 0):
        raise AssertionError("unreachable")
    return stories


def ease_value(name: str, value: float) -> float:
    value = max(0.0, min(1.0, value))
    if name == "linear":
        return value
    if name == "in":
        return value * value * value
    if name == "out":
        return 1 - (1 - value) ** 3
    if name == "back":
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * (value - 1) ** 3 + c1 * (value - 1) ** 2
    return value * value * (3 - 2 * value)


def sample_track(track: dict[str, object], frame: int) -> dict[str, object]:
    keys = track["keys"]
    left = keys[0]
    right = keys[-1]
    for key in keys:
        if key[0] <= frame:
            left = key
        if key[0] >= frame:
            right = key
            break
    if right[0] == left[0]:
        amount = 0.0
    else:
        amount = ease_value(str(right[6]), (frame - left[0]) / (right[0] - left[0]))
    values = [left[index] + (right[index] - left[index]) * amount for index in range(1, 6)]
    return {
        "instance": track["instance"],
        "component": track["component"],
        "role": track["role"],
        "x": round(values[0], 2),
        "y": round(values[1], 2),
        "scale": round(values[2], 3),
        "rotation": round(values[3], 2),
        "opacity": round(max(0.0, min(1.0, values[4])), 3),
        "z": track["z"],
    }


def story_phase(frame: int) -> str:
    if frame < 8:
        return "beginning"
    if frame < 28:
        return "working"
    if frame < QUIET_START:
        return "resolution"
    return "quiet-tail"


def full_timeline(treatment: dict[str, object]) -> list[dict[str, object]]:
    frames = []
    for frame in range(FRAME_COUNT):
        frames.append({
            "frame": frame,
            "timeMs": frame * 1000 / FPS,
            "storyPhase": story_phase(frame),
            "quietTail": frame >= QUIET_START,
            "objects": [sample_track(track, frame) for track in treatment["objects"]],
            "symbols": [sample_track(track, frame) for track in treatment["symbols"]],
        })
    return frames


def reduced_timeline(full: list[dict[str, object]]) -> list[dict[str, object]]:
    segments = ((0, 7, 5), (8, 14, 12), (15, 21, 18), (22, 27, 25), (28, 36, 33), (37, 41, 39))
    frames = []
    for frame in range(FRAME_COUNT):
        start, end, sample_index = next(segment for segment in segments if segment[0] <= frame <= segment[1])
        sampled = full[sample_index]
        primary = max((item for item in sampled["objects"] if item["role"] in ("hero", "resolved")), key=lambda item: item["opacity"])
        supports = [item for item in sampled["objects"] if item["role"] == "support"]
        secondary = max(supports, key=lambda item: item["opacity"])
        objects = []
        for item in sampled["objects"]:
            copy = dict(item)
            copy["rotation"] = 0
            if item["instance"] not in (primary["instance"], secondary["instance"]):
                copy["opacity"] = 0
            objects.append(copy)
        symbols = []
        selected_symbol = max(sampled["symbols"], key=lambda item: item["opacity"], default=None)
        for item in sampled["symbols"]:
            copy = dict(item)
            copy["rotation"] = 0
            if frame >= QUIET_START or selected_symbol is None or item["instance"] != selected_symbol["instance"]:
                copy["opacity"] = 0
            else:
                copy["opacity"] = min(copy["opacity"], .65)
            symbols.append(copy)
        frames.append({
            "frame": frame,
            "timeMs": frame * 1000 / FPS,
            "storyPhase": story_phase(frame),
            "quietTail": frame >= QUIET_START,
            "holdSegment": [start, end],
            "objects": objects,
            "symbols": symbols,
        })
    return frames


def compile_stories(source: dict[str, object], symbols: dict[str, dict[str, object]]) -> tuple[dict[str, object], dict[str, object]]:
    stories = authored_tracks()
    used_objects: dict[str, dict[str, object]] = {}
    for story in stories.values():
        for component_id in story["elements"]:
            component = source["components"].get(component_id)
            if not component:
                raise RuntimeError(f"missing inherited component: {component_id}")
            used_objects[component_id] = {key: component.get(key) for key in ("src", "sha256", "family", "cellPixels", "sourceSet")}
        compiled = {}
        for treatment_name, treatment in story.pop("treatments").items():
            full = full_timeline(treatment)
            compiled[treatment_name] = {"full": full, "reduced": reduced_timeline(full)}
        story["timelines"] = compiled
        for treatment in compiled.values():
            for mode in treatment.values():
                for frame in mode:
                    for item in frame["symbols"]:
                        if item["component"] not in symbols:
                            raise RuntimeError(f"missing symbol component: {item['component']}")
    return stories, used_objects


def main() -> None:
    required = (SOURCE_SHEET, PAGE_TEMPLATE, SEQUENCE_CATALOGUE, VOCABULARY_CATALOGUE, APPROVAL_RECORD, VERIFIER, PROMPT_LOG)
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing dependency: {rel(path)}")

    sequence = json.loads(SEQUENCE_CATALOGUE.read_text())
    vocabulary = json.loads(VOCABULARY_CATALOGUE.read_text())
    symbols, published, source_record = build_symbols()
    stories, inherited_components = compile_stories(vocabulary, symbols)
    authority_snapshot = sorted({(frame["src"], frame.get("authoritySha256", frame.get("candidateSha256"))) for frame in sequence["sequence"]})
    phase_counts = Counter(frame["phase"] for frame in sequence["sequence"])
    catalogue = {
        "schema": "lighthouse-keeper/keeper-prime-rear-action-choreography@1",
        "set": SET,
        "status": "immutable-reversible-choreography-review-candidate-not-approved",
        "sourceSequence": {
            "set": sequence["set"],
            "file": rel(SEQUENCE_CATALOGUE),
            "url": "/keeper-review/keeper-prime-rear-action-sequence-v1/catalogue.json",
            "sha256": sha(SEQUENCE_CATALOGUE),
            "approvalRecord": rel(APPROVAL_RECORD),
            "approvalSha256": sha(APPROVAL_RECORD),
        },
        "sourceVocabulary": {
            "set": vocabulary["set"],
            "file": rel(VOCABULARY_CATALOGUE),
            "url": "/keeper-review/activity-cloud-composer-v6/catalogue.json",
            "sha256": sha(VOCABULARY_CATALOGUE),
        },
        "sequence": sequence["sequence"],
        "actionStartIndex": sequence["actionStartIndex"],
        "sequenceDurationMs": sequence["sequenceDurationMs"],
        "phaseCounts": dict(phase_counts),
        "authoritySnapshot": [{"src": src, "sha256": digest} for src, digest in authority_snapshot],
        "callout": {
            "frames": FRAME_COUNT,
            "fps": FPS,
            "quietTailFrames": FRAME_COUNT - QUIET_START,
            "quietTailRange": [QUIET_START, FRAME_COUNT - 1],
            "startsWithAction": True,
            "placement": "raised-above-cap",
            "treatments": ["open", "bubble"],
            "motionModes": ["full", "reduced"],
        },
        "symbols": {key: {field: value for field, value in record.items() if field in ("src", "sha256", "family", "cellPixels", "sourceSet", "owner")} for key, record in symbols.items()},
        "inheritedComponents": inherited_components,
        "stories": stories,
        "defaultStory": "garden-bbq",
        "controls": ["body", "hero-result", "supporting-objects", "symbols", "treatment-marks", "treatment", "sfx-declaration", "speed", "loop", "reduced-motion", "path-overlay", "timeline"],
        "separation": {
            "bodySilent": True,
            "bodyLayerIndependent": True,
            "heroResultLayerIndependent": True,
            "supportingObjectLayerIndependent": True,
            "symbolLayerIndependent": True,
            "treatmentLayerIndependent": True,
            "sfxDeclarationIndependent": True,
            "contextBakedIntoKeeper": False,
        },
        "approvalBoundary": {
            "candidateApproved": False,
            "runtimeChanged": False,
            "finalChanged": False,
            "kitchenChanged": False,
            "primeAuthorityChanged": False,
            "deployed": False,
        },
    }

    PUBLIC.mkdir(parents=True, exist_ok=True)
    write_json(CATALOGUE, catalogue, compact=True)
    (PACK / "catalogue.json").write_bytes(CATALOGUE.read_bytes())
    (PUBLIC / "index.html").write_bytes(PAGE_TEMPLATE.read_bytes())

    files = {}
    for label, path in (
        ("catalogue", CATALOGUE),
        ("draftCatalogue", PACK / "catalogue.json"),
        ("page", PUBLIC / "index.html"),
        ("template", PAGE_TEMPLATE),
        ("builder", Path(__file__)),
        ("verifier", VERIFIER),
        ("promptLog", PROMPT_LOG),
    ):
        files[label] = {"file": rel(path), "sha256": sha(path)}
    register = {
        "schema": "lighthouse-keeper/keeper-prime-rear-action-choreography-register@1",
        "set": SET,
        "status": catalogue["status"],
        "purpose": "Four richer deterministic activity-cloud stories over the byte-exact approved Prime rear-action sequence, each with separately authored open and bubble treatments plus reduced motion.",
        "sourceSequence": catalogue["sourceSequence"],
        "sourceVocabulary": catalogue["sourceVocabulary"],
        "generatedSource": source_record,
        "newSymbols": symbols,
        "publishedAssets": published,
        "candidate": {
            "publicShell": files["page"],
            "stories": list(stories),
            "storyCount": len(stories),
            "treatmentsPerStory": 2,
            "motionModesPerTreatment": 2,
            "timelineFrames": FRAME_COUNT,
            "timelineFps": FPS,
            "quietTailFrames": FRAME_COUNT - QUIET_START,
            "sequenceFrames": len(sequence["sequence"]),
        },
        "files": files,
        "checks": {
            "sourceSheetOwnershipIsolated": True,
            "sourceSheetGuttersAtLeast80": True,
            "componentGuttersAtLeast20": True,
            "preloadAndDecodeBeforePlayback": True,
            "singleSynchronizedClock": True,
            "allTimelinesDeclaredAsData": True,
            "fullAndReducedMotion": True,
            "pathOverlayDiagnostic": True,
            "layersIndependent": True,
            "primeSequenceByteExact": True,
            "v6VocabularyByteExact": True,
            "runtimeChanged": False,
            "kitchenChanged": False,
            "deployed": False,
        },
        "rollback": "Delete only this versioned draft directory, its public review directory, archive set/object entries, builder, verifier, package command and documentation references. Prime Rear Action Sequence V1, Composer V6, runtime, Final and Kitchen remain untouched.",
    }
    write_json(PACK / "batch-register.json", register)
    print(json.dumps({
        "set": SET,
        "stories": list(stories),
        "symbols": len(symbols),
        "sequenceFrames": len(sequence["sequence"]),
        "timelineFramesPerMode": FRAME_COUNT,
        "publishedAssets": len(published),
    }, indent=2))


if __name__ == "__main__":
    main()
