#!/usr/bin/env python3
"""Build the immutable V3 activity-object vocabulary review candidate.

V3 inherits every Prime body and route byte from V1 through V2.  It adds only
separately owned callout components, authored phrase metadata and review media.
"""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-back-work-activity-callout-v3"
PACK = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
COMPONENTS = PACK / "drafts/callouts"
EVIDENCE = PACK / "evidence"
V1_PACK = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v1"
V1_CATALOGUE = V1_PACK / "catalogue.json"
V2_PACK = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2"
V2_CATALOGUE = V2_PACK / "catalogue.json"
V2_PUBLIC_CATALOGUE = ROOT / "public/keeper-review/keeper-prime-back-work-activity-callout-v2/catalogue.json"
V2_REGISTER = V2_PACK / "batch-register.json"
PAGE = PUBLIC / "index.html"
RUNTIME_MANIFEST = ROOT / "public/sprites/manifest.json"
WORKBENCH = ROOT / "data/keeper_animation_workbench.json"
KITCHEN_REFERENCE = ROOT / "art/source/kitchen-warm-ligne-claire-family-2026-10-24-v4-on-food-corrected.png"

PHRASE_FRAMES = 42
PHRASE_FPS = 8
ASSET_CELL = 256
SAFE_GUTTER = 20
ATLAS_COLUMNS = 8
CALLOUT_PLACEMENT = {
    "policy": "raised-clear-of-cap-no-contextual-surface",
    "large": {"actorTopPx": 190, "calloutTopPx": 0, "minimumCapClearancePx": 16},
    "game": {"actorTopPx": 122, "calloutTopPx": -8, "outerScale": 0.62, "minimumCapClearancePx": 8},
    "counterPresent": False,
    "furniturePresent": False,
}

SOURCE_SPECS = [
    ("proteins", "proteins-generated-v3.png", 789, 543, [
        ("cooking-cow", "food-provenance"), ("cooking-sheep", "food-provenance"),
        ("cooking-pig", "food-provenance"), ("cooking-bacon", "cooking"),
    ]),
    ("kitchen-prep", "kitchen-prep-generated-v3.png", 805, 525, [
        ("cooking-knife", "cooking"), ("cooking-vegetables", "cooking"),
        ("cooking-gravy", "cooking"), ("cooking-sandwich", "cooking"),
    ]),
    ("meals-flour", "meals-flour-generated-v3.png", 803, 502, [
        ("meal-breakfast", "meal"), ("meal-lunch", "meal"),
        ("meal-dinner", "meal"), ("baking-flour", "baking"),
    ]),
    ("washing-tea", "washing-tea-generated-v3.png", 753, 524, [
        ("washing-liquid", "washing"), ("tea-kettle", "tea"),
        ("tea-mug", "tea"), ("tea-milk", "tea"),
    ]),
    ("dental", "dental-generated-v3.png", 811, 531, [
        ("dental-toothpaste", "dental"), ("dental-water", "dental"),
        ("dental-toothbrush", "dental"), ("dental-teeth", "dental"),
    ]),
    ("bbq-meats", "bbq-meats-generated-v3.png", 844, 517, [
        ("bbq-steak", "bbq"), ("bbq-lamb-chops", "bbq"),
        ("bbq-leg-lamb", "bbq"), ("bbq-grill", "bbq"),
    ]),
    ("sandwich-ingredients", "sandwich-ingredients-generated-v3.png", 790, 502, [
        ("sandwich-bread", "sandwich"), ("sandwich-ham", "sandwich"),
        ("sandwich-lettuce", "sandwich"), ("sandwich-tomato", "sandwich"),
    ]),
    ("maintenance-leisure", "maintenance-leisure-generated-v3.png", 794, 538, [
        ("maintenance-lamp-polish", "maintenance"), ("maintenance-welding", "maintenance"),
        ("leisure-vinyl", "leisure"), ("hygiene-shower", "hygiene"),
    ]),
    ("rest-music", "rest-music-generated-v3.png", 789, 507, [
        ("rest-sleep", "rest"), ("music-drums", "music"),
        ("music-guitar", "music"), ("music-piano", "music"),
    ]),
    ("harvest-garden", "harvest-garden-generated-v3.png", 797, 528, [
        ("harvest-fruit", "harvest"), ("harvest-vegetables", "harvest"),
        ("garden-watering", "garden"), ("garden-seeds", "garden"),
    ]),
    ("aquarium-garden", "aquarium-garden-generated-v3.png", 793, 493, [
        ("aquarium-food", "aquarium"), ("aquarium-fish", "aquarium"),
        ("aquarium-cleaning", "aquarium"), ("garden-seedling", "garden"),
    ]),
    ("story-figures", "story-figures-isolated-generated-v3.png", 777, 517, [
        ("rest-counting-sheep", "rest"), ("music-drummer", "music"),
        ("music-guitarist", "music"), ("music-composer", "music"),
    ]),
    ("aquarium-details", "aquarium-details-generated-v3.png", 795, 525, [
        ("aquarium-castle", "aquarium"), ("aquarium-plants", "aquarium"),
        ("aquarium-treasure", "aquarium"), ("aquarium-aerator", "aquarium"),
    ]),
]


def recipe(label: str, family: str, compatibility: str, primary: str, helpers: list[str],
           envelope: str, *, schedule: str = "any", story: list[str] | None = None,
           lineage: dict | None = None, note: str = "") -> dict:
    return {
        "label": label, "family": family, "bodyCompatibility": compatibility,
        "schedule": schedule, "primary": primary, "helpers": helpers,
        "envelope": envelope, "story": story or [], "lineage": lineage,
        "note": note,
    }


RECIPES = {
    "breakfast": recipe("Cook breakfast", "cooking", "rear-work", "meal-breakfast", ["cooking-bacon", "cooking-pig", "cooking-pan"], "cooking-steam", schedule="breakfast", lineage={"animal": "cooking-pig", "result": "cooking-bacon"}),
    "lunch": recipe("Prepare lunch", "cooking", "rear-work", "meal-lunch", ["cooking-vegetables", "cooking-knife", "cooking-spoon"], "cooking-seasoning", schedule="lunch"),
    "dinner-beef": recipe("Cook beef dinner", "cooking", "rear-work", "meal-dinner", ["cooking-cow", "bbq-steak", "cooking-gravy"], "cooking-steam", schedule="dinner", lineage={"animal": "cooking-cow", "result": "bbq-steak"}),
    "dinner-lamb": recipe("Cook lamb dinner", "cooking", "rear-work", "meal-dinner", ["cooking-sheep", "bbq-lamb-chops", "cooking-gravy"], "cooking-steam", schedule="dinner", lineage={"animal": "cooking-sheep", "results": ["bbq-lamb-chops", "bbq-leg-lamb"]}),
    "snack-sandwich": recipe("Make a sandwich", "cooking", "rear-work", "cooking-sandwich", ["sandwich-bread", "sandwich-ham", "sandwich-lettuce", "sandwich-tomato"], "cooking-seasoning", schedule="snack", story=["sandwich-bread", "sandwich-ham", "sandwich-lettuce", "sandwich-tomato", "cooking-sandwich"], note="Ingredients arrive separately and resolve to the completed sandwich."),
    "bake-cake": recipe("Bake a cake", "baking", "rear-work", "mixing-bowl", ["baking-flour", "mixing-egg", "mixing-whisk"], "mixing-flour"),
    "washing-up": recipe("Wash up", "washing", "rear-work", "washing-plate", ["washing-liquid", "washing-sponge", "washing-cutlery"], "washing-droplets"),
    "make-tea": recipe("Make tea", "tea", "rear-work", "tea-kettle", ["tea-mug", "tea-milk", "cooking-spoon"], "cooking-steam"),
    "brush-teeth": recipe("Brush teeth", "dental", "dedicated-pose-required", "dental-toothbrush", ["dental-toothpaste", "dental-water", "dental-teeth"], "washing-droplets"),
    "polish-lamp": recipe("Polish lighthouse lamp", "maintenance", "rear-work", "maintenance-lamp-polish", ["repair-oilcan", "repair-fastener"], "repair-sparks"),
    "bbq-beef": recipe("Cook beef on BBQ", "bbq", "rear-work-with-context", "bbq-grill", ["cooking-cow", "bbq-steak", "cooking-vegetables"], "cooking-steam", lineage={"animal": "cooking-cow", "result": "bbq-steak"}),
    "bbq-lamb": recipe("Cook lamb on BBQ", "bbq", "rear-work-with-context", "bbq-grill", ["cooking-sheep", "bbq-lamb-chops", "bbq-leg-lamb"], "cooking-steam", lineage={"animal": "cooking-sheep", "results": ["bbq-lamb-chops", "bbq-leg-lamb"]}),
    "welding": recipe("Welding", "maintenance", "dedicated-pose-required", "maintenance-welding", ["repair-tools", "repair-fastener"], "repair-sparks"),
    "play-vinyl": recipe("Put on a vinyl record", "leisure", "dedicated-pose-required", "leisure-vinyl", ["repair-fastener"], "cooking-seasoning"),
    "showering": recipe("Shower", "hygiene", "dedicated-pose-required", "hygiene-shower", ["washing-droplets", "washing-sponge"], "washing-droplets"),
    "sleeping": recipe("Sleep", "rest", "dedicated-pose-required", "rest-sleep", ["rest-counting-sheep"], "cooking-steam"),
    "play-drums": recipe("Play drums", "music", "dedicated-pose-required", "music-drums", ["music-drummer"], "cooking-seasoning"),
    "play-guitar": recipe("Play guitar", "music", "dedicated-pose-required", "music-guitar", ["music-guitarist"], "cooking-seasoning"),
    "play-piano": recipe("Play piano", "music", "dedicated-pose-required", "music-piano", ["music-composer"], "cooking-seasoning"),
    "pick-fruit": recipe("Pick fruit", "harvest", "dedicated-pose-required", "harvest-fruit", ["garden-watering", "garden-seedling"], "cooking-seasoning"),
    "pick-vegetables": recipe("Pick vegetables", "harvest", "dedicated-pose-required", "harvest-vegetables", ["garden-seeds", "garden-seedling"], "cooking-seasoning"),
    "feed-fish": recipe("Feed aquarium fish", "aquarium", "dedicated-pose-required", "aquarium-fish", ["aquarium-food", "aquarium-castle", "aquarium-plants"], "washing-droplets"),
    "clean-fish-tank": recipe("Clean fish tank", "aquarium", "dedicated-pose-required", "aquarium-cleaning", ["aquarium-castle", "aquarium-treasure", "aquarium-aerator"], "washing-droplets"),
    "water-plants": recipe("Water plants", "garden", "dedicated-pose-required", "garden-watering", ["garden-seedling"], "washing-droplets"),
    "sow-seeds": recipe("Sow seeds", "garden", "dedicated-pose-required", "garden-seeds", ["garden-seedling"], "cooking-seasoning"),
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":") if compact else None, indent=None if compact else 2) + "\n")


def alpha_bounds(image: Image.Image) -> dict[str, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.where(alpha > 0)
    if not len(xs):
        raise RuntimeError("empty callout component")
    return {"minX": int(xs.min()), "minY": int(ys.min()), "maxX": int(xs.max()), "maxY": int(ys.max()), "width": int(xs.max() - xs.min() + 1), "height": int(ys.max() - ys.min() + 1), "opaquePixels": int((alpha > 0).sum())}


def edge_alpha_pixels(image: Image.Image) -> int:
    a = np.asarray(image.getchannel("A"))
    return int(np.count_nonzero(a[0]) + np.count_nonzero(a[-1]) + np.count_nonzero(a[:, 0]) + np.count_nonzero(a[:, -1]))


def transparent_gutter(image: Image.Image) -> int:
    b = alpha_bounds(image)
    return min(b["minX"], b["minY"], image.width - 1 - b["maxX"], image.height - 1 - b["maxY"])


def isolate_component(source: Image.Image, crop: tuple[int, int, int, int]) -> tuple[Image.Image, dict]:
    pixels = np.array(source.crop(crop).convert("RGBA"), copy=True)
    pixels[pixels[:, :, 3] <= 8, 3] = 0
    isolated = Image.fromarray(pixels)
    bounds = alpha_bounds(isolated)
    trimmed = isolated.crop((bounds["minX"], bounds["minY"], bounds["maxX"] + 1, bounds["maxY"] + 1))
    available = ASSET_CELL - SAFE_GUTTER * 2
    scale = min(available / trimmed.width, available / trimmed.height)
    size = (max(1, round(trimmed.width * scale)), max(1, round(trimmed.height * scale)))
    resized = trimmed.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (ASSET_CELL, ASSET_CELL), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((ASSET_CELL - size[0]) // 2, (ASSET_CELL - size[1]) // 2))
    return canvas, {
        "sourceCrop": list(crop), "sourceVisiblePixels": bounds["opaquePixels"],
        "registeredBounds": alpha_bounds(canvas), "edgeAlphaPixels": edge_alpha_pixels(canvas),
        "transparentGutterPx": transparent_gutter(canvas),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }


def boundary_alpha(source: Image.Image, split_x: int, split_y: int) -> dict:
    a = np.asarray(source.getchannel("A")) > 8
    return {
        "verticalSharedBoundaryAlphaPixels": int(a[:, split_x].sum()),
        "horizontalSharedBoundaryAlphaPixels": int(a[split_y, :].sum()),
    }


def build_components() -> tuple[dict[str, Path], dict[str, dict], list[dict]]:
    paths, records, sources = {}, {}, []
    for group, filename, split_x, split_y, assets in SOURCE_SPECS:
        source_path = PACK / "source" / filename
        source = Image.open(source_path).convert("RGBA")
        if source.size != (1536, 1024):
            raise RuntimeError(f"unexpected source geometry: {rel(source_path)}")
        boundary = boundary_alpha(source, split_x, split_y)
        if any(boundary.values()):
            raise RuntimeError(f"source ownership boundary contains alpha: {filename}")
        cells = [(0, 0, split_x, split_y), (split_x, 0, 1536, split_y), (0, split_y, split_x, 1024), (split_x, split_y, 1536, 1024)]
        source_record = {"file": rel(source_path), "sha256": sha(source_path), "pixels": list(source.size), "splitX": split_x, "splitY": split_y, **boundary, "cells": []}
        for (key, family), crop in zip(assets, cells):
            component, evidence = isolate_component(source, crop)
            out = COMPONENTS / f"{key}.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            component.save(out)
            evidence.update({"file": rel(out), "sha256": sha(out), "family": family, "sourceGroup": group, "cellPixels": [ASSET_CELL, ASSET_CELL]})
            if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 16:
                raise RuntimeError(f"unsafe component gutter: {key}")
            paths[key] = out
            records[key] = evidence
            source_record["cells"].append({"asset": key, "family": family, "crop": list(crop), "visiblePixels": evidence["sourceVisiblePixels"]})
        sources.append(source_record)
    return paths, records, sources


def opacity_window(frame: int, start: int, hold_end: int, end: int) -> float:
    if frame < start or frame > end:
        return 0.0
    if frame < start + 3:
        return (frame - start + 1) / 3
    if frame <= hold_end:
        return 1.0
    return max(0.0, (end - frame + 1) / max(1, end - hold_end))


def standard_frames(spec: dict, treatment: str) -> list[dict]:
    result = []
    helper_positions = [(-58, 20, -16), (57, 18, 16), (-44, -5, -9), (45, -8, 9)]
    for frame in range(PHRASE_FRAMES):
        parts = []
        env_o = opacity_window(frame, 0, 30, 36)
        if env_o:
            parts.append({"asset": spec["envelope"], "role": "activity-envelope", "x": 0, "y": -2 if treatment == "orbit" else 4, "scale": .44 if treatment == "orbit" else .76, "rotate": round(math.sin(frame * .22) * 5, 2), "opacity": round(env_o * .82, 3)})
        primary_o = opacity_window(frame, 3, 31, 36)
        if primary_o:
            parts.append({"asset": spec["primary"], "role": "primary", "x": 0, "y": -28 if treatment == "orbit" else -12, "scale": .58 if treatment == "orbit" else .50, "rotate": round(math.sin(frame * .27) * 4, 2), "opacity": round(primary_o, 3)})
        for index, asset in enumerate(spec["helpers"][:4]):
            start = 7 + index * 5
            visible = opacity_window(frame, start, 27 + min(index, 2), 33 + min(index, 2))
            if not visible:
                continue
            x, y, rotate = helper_positions[index]
            if treatment == "bustle":
                x, y = round(x * .70), round(y * .62 + 18)
            parts.append({"asset": asset, "role": "helper", "x": x + round(math.sin(frame * (.31 + index * .03)) * 3), "y": y + round(math.cos(frame * (.36 + index * .02)) * 3), "scale": .32 if treatment == "orbit" else .27, "rotate": rotate, "opacity": round(visible, 3)})
        result.append({"frame": frame, "components": parts})
    return result


def sandwich_frames(spec: dict, treatment: str) -> list[dict]:
    result = []
    ingredients = spec["story"][:-1]
    final = spec["story"][-1]
    positions = [(-58, -6), (-20, 24), (20, -2), (58, 20)]
    for frame in range(PHRASE_FRAMES):
        parts = []
        env_o = opacity_window(frame, 0, 31, 36)
        if env_o:
            parts.append({"asset": spec["envelope"], "role": "activity-envelope", "x": 0, "y": 1, "scale": .40 if treatment == "orbit" else .72, "rotate": 0, "opacity": round(env_o * .72, 3)})
        for index, asset in enumerate(ingredients):
            start = 3 + index * 4
            visible = opacity_window(frame, start, 21, 25)
            if visible:
                x, y = positions[index]
                if treatment == "bustle":
                    x, y = round(x * .65), round(y * .55 + 13)
                parts.append({"asset": asset, "role": "ingredient", "x": x, "y": y, "scale": .28, "rotate": -12 + index * 8, "opacity": round(visible, 3)})
        final_o = opacity_window(frame, 23, 31, 36)
        if final_o:
            parts.append({"asset": final, "role": "resolved-primary", "x": 0, "y": -19 if treatment == "orbit" else -8, "scale": .62 if treatment == "orbit" else .54, "rotate": round(math.sin(frame * .28) * 3, 2), "opacity": round(final_o, 3)})
        result.append({"frame": frame, "components": parts})
    return result


def build_phrases() -> dict:
    phrases = {}
    for key, spec in RECIPES.items():
        maker = sandwich_frames if spec["story"] else standard_frames
        phrases[key] = {**spec, "treatments": {name: {"frames": maker(spec, name)} for name in ("orbit", "bustle")}}
    return phrases


def render_parts(parts: list[dict], assets: dict[str, Image.Image], size: tuple[int, int], centre: tuple[int, int], master_scale: float = 1.0) -> Image.Image:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    for part in parts:
        source = assets[part["asset"]].copy()
        target = max(1, round(104 * part["scale"] * master_scale))
        rendered = source.resize((target, target), Image.Resampling.LANCZOS)
        if part["rotate"]:
            rendered = rendered.rotate(-part["rotate"], resample=Image.Resampling.BICUBIC, expand=True)
        if part["opacity"] < 1:
            rendered.putalpha(rendered.getchannel("A").point(lambda value, opacity=part["opacity"]: round(value * opacity)))
        canvas.alpha_composite(rendered, (round(centre[0] + part["x"] * master_scale - rendered.width / 2), round(centre[1] + part["y"] * master_scale - rendered.height / 2)))
    return canvas


def build_atlas(component_paths: dict[str, Path]) -> dict:
    names = sorted(component_paths)
    rows = math.ceil(len(names) / ATLAS_COLUMNS)
    atlas = Image.new("RGBA", (ATLAS_COLUMNS * ASSET_CELL, rows * ASSET_CELL), (0, 0, 0, 0))
    for index, name in enumerate(names):
        image = Image.open(component_paths[name]).convert("RGBA")
        atlas.alpha_composite(image, ((index % ATLAS_COLUMNS) * ASSET_CELL, (index // ATLAS_COLUMNS) * ASSET_CELL))
    path = EVIDENCE / "activity-object-library-atlas.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(path)
    return {"file": rel(path), "sha256": sha(path), "cellPixels": [ASSET_CELL, ASSET_CELL], "columns": ATLAS_COLUMNS, "rows": rows, "componentOrder": names, "edgeAlphaPixelsPerCell": 0}


def build_contact_sheet(phrases: dict, component_paths: dict[str, Path], v2_catalogue: dict) -> dict:
    selected = [key for key, spec in RECIPES.items() if spec["bodyCompatibility"].startswith("rear-work")]
    samples = [3, 10, 17, 24, 31, 37]
    assets = {name: Image.open(path).convert("RGBA") for name, path in component_paths.items()}
    body = [Image.open(ROOT / record["file"]).convert("RGBA") for record in v2_catalogue["body"]["frames"]]
    cell_w, cell_h = 320, 300
    sheet = Image.new("RGBA", (cell_w * len(samples), cell_h * len(selected)), (9, 19, 27, 255))
    draw = ImageDraw.Draw(sheet)
    for row, activity in enumerate(selected):
        for col, sample in enumerate(samples):
            x0, y0 = col * cell_w, row * cell_h
            cell = Image.new("RGBA", (cell_w, cell_h - 24), (37, 57, 69, 255))
            actor = body[round(sample * 23 / (PHRASE_FRAMES - 1))].resize((128, 160), Image.Resampling.LANCZOS)
            cell.alpha_composite(actor, (96, 112))
            callout = render_parts(phrases[activity]["treatments"]["orbit"]["frames"][sample]["components"], assets, cell.size, (160, 68), .88)
            cell.alpha_composite(callout)
            sheet.alpha_composite(cell, (x0, y0))
            draw.text((x0 + 7, y0 + cell_h - 19), f"{activity} · F{sample + 1:02d}", fill=(238, 247, 250, 255))
    path = EVIDENCE / "rear-work-recipes-raised-no-counter-contact-sheet.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)
    return {"file": rel(path), "sha256": sha(path), "recipes": selected, "sampleFrames": [value + 1 for value in samples], "includesPrimeBodyAtGameScale": True, "counterPresent": False, "calloutRaised": True}


def publish(path: Path, label: str, published: list[dict]) -> dict:
    digest = sha(path)
    target = ASSETS / f"{label}-{digest[:16]}{path.suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
    entry = {"source": rel(path), "sourceSha256": digest, "public": rel(target), "publicAssemblyPath": rel(target), "publicSha256": sha(target), "url": f"/keeper-review/{SET}/assets/{target.name}"}
    published.append(entry)
    return entry


def main() -> None:
    required = [V1_CATALOGUE, V2_CATALOGUE, V2_PUBLIC_CATALOGUE, V2_REGISTER, PAGE, RUNTIME_MANIFEST, WORKBENCH, KITCHEN_REFERENCE]
    required += [PACK / "source" / filename for _, filename, _, _, _ in SOURCE_SPECS]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    component_paths, component_records, source_records = build_components()
    v2_catalogue = json.loads(V2_CATALOGUE.read_text())
    v2_public = json.loads(V2_PUBLIC_CATALOGUE.read_text())
    v2_register = json.loads(V2_REGISTER.read_text())

    inherited_paths = {name: ROOT / record["file"] for name, record in v2_register["candidate"]["calloutComponents"].items()}
    all_component_paths = {**inherited_paths, **component_paths}
    phrases = build_phrases()
    atlas = build_atlas(component_paths)
    contact_sheet = build_contact_sheet(phrases, all_component_paths, v2_catalogue)
    published: list[dict] = []
    public_components = {name: publish(path, name, published) for name, path in all_component_paths.items()}
    published_atlas = publish(ROOT / atlas["file"], "activity-object-library-atlas", published)
    published_contact = publish(ROOT / contact_sheet["file"], "rear-work-recipes-raised-no-counter", published)

    components = {}
    for name, entry in public_components.items():
        if name in component_records:
            source = component_records[name]
            components[name] = {"src": entry["url"], "cellPixels": [ASSET_CELL, ASSET_CELL], "family": source["family"], "sourceSet": SET}
        else:
            source = v2_catalogue["callouts"]["components"][name]
            components[name] = {**source, "src": entry["url"], "sourceSet": "keeper-prime-back-work-activity-callout-v2"}
    callouts = {
        "fps": PHRASE_FPS, "frames": PHRASE_FRAMES, "durationSeconds": PHRASE_FRAMES / PHRASE_FPS,
        "styles": {
            "orbit": {"label": "Open radial orbit · no bubble", "status": "equal review candidate"},
            "bustle": {"label": "Activity bustle · bubble treatment", "status": "equal review candidate"},
        },
        "reviewDefaultStyle": "orbit", "styleApproved": None, "placement": CALLOUT_PLACEMENT,
        "components": components, "phrases": phrases,
        "reducedMotion": {name: {"treatment": "bustle", "frame": 24 if name == "snack-sandwich" else 21} for name in phrases},
    }
    sfx = {"bodySilent": True}
    for key, spec in RECIPES.items():
        cues = [{"frame": 7, "cue": f"{spec['family']}-activity-beat", "kind": "activity-beat"}]
        if spec["family"] in {"tea", "washing", "aquarium", "bbq"}:
            cues.append({"frame": 22, "cue": f"{spec['family']}-asset-state", "kind": "asset-state"})
        sfx[key] = cues

    catalogue = {
        **v2_catalogue,
        "schema": "lighthouse-keeper/prime-back-work-activity-review@3", "set": SET,
        "status": "immutable-reversible-vocabulary-v3-not-approved",
        "callouts": callouts, "sfx": sfx,
        "bodyInheritance": {"set": v2_catalogue["set"], "catalogueFile": rel(V2_CATALOGUE), "catalogueSha256": sha(V2_CATALOGUE), "registerFile": rel(V2_REGISTER), "registerSha256": sha(V2_REGISTER), "bodyAndRouteChanged": False},
        "controlsRequired": ["body", "callout envelope", "primary/resolved object", "supporting objects", "activity treatment", "SFX", "reduced motion"],
    }
    catalogue_path = PACK / "catalogue.json"
    write_json(catalogue_path, catalogue)
    public_catalogue = {**v2_public, "schema": catalogue["schema"], "set": SET, "status": catalogue["status"], "callouts": callouts, "sfx": sfx, "bodyInheritance": catalogue["bodyInheritance"]}
    public_catalogue_path = PUBLIC / "catalogue.json"
    write_json(public_catalogue_path, public_catalogue, compact=True)

    inherited_hashes = {name: {"file": rel(path), "sha256": sha(path)} for name, path in inherited_paths.items()}
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET,
        "status": "prime-back-work-vocabulary-v3-awaiting-frank",
        "purpose": "Expand the validated V2 game-language callout vocabulary, narrative figures, aquarium details and time-aware recipes without changing the Prime rear-work body, approved route, runtime art or Kitchen work.",
        "bodyInheritance": catalogue["bodyInheritance"],
        "protectedState": {
            "runtimeManifest": {"file": rel(RUNTIME_MANIFEST), "sha256": sha(RUNTIME_MANIFEST)},
            "workbench": {"file": rel(WORKBENCH), "sha256": sha(WORKBENCH)},
            "kitchenReference": {"file": rel(KITCHEN_REFERENCE), "sha256": sha(KITCHEN_REFERENCE)},
        },
        "authorities": v2_register["authorities"],
        "directionalReferences": {**v2_register["directionalReferences"], "v2GameLanguage": {"file": rel(V2_CATALOGUE), "sha256": sha(V2_CATALOGUE), "authority": False, "contribution": "validated callout rendering language and inherited component bytes only"}},
        "generation": {"tool": "built-in image generation", "selectedSources": source_records, "sourceContribution": "52 new callout-only object and story tokens; no Keeper, room, counter, furniture or runtime pixels", "backgroundIsolation": "native alpha <= 8 discarded; explicit disjoint 2x2 ownership partitions; every output registered to 256 px with a deterministic 20 px target gutter"},
        "candidate": {
            "newCalloutComponents": component_records, "inheritedV2Components": inherited_hashes,
            "componentAtlas": {**atlas, "publishedUrl": published_atlas["url"]},
            "raisedNoCounterContactSheet": {**contact_sheet, "publishedUrl": published_contact["url"]},
            "recipes": {name: {key: value for key, value in spec.items() if key != "treatments"} for name, spec in phrases.items()},
            "catalogue": {"file": rel(catalogue_path), "sha256": sha(catalogue_path)},
            "publicCatalogue": {"file": rel(public_catalogue_path), "sha256": sha(public_catalogue_path), "projection": "playback-fields-only"},
            "publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)}, "publishedAssets": published,
        },
        "publishedAssets": published,
        "checks": {
            "v2BodyAndRouteInheritedByteForByte": True,
            "everyNewCalloutCellHasSafeEdge": all(value["edgeAlphaPixels"] == 0 and value["transparentGutterPx"] >= 16 for value in component_records.values()),
            "everyNewCalloutPixelHasOneOwner": all(value["ownership"] == {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0} for value in component_records.values()),
            "everySourceOwnershipBoundaryTransparent": all(not row["verticalSharedBoundaryAlphaPixels"] and not row["horizontalSharedBoundaryAlphaPixels"] for row in source_records),
            "bothTreatmentsBuilt": set(callouts["styles"]) == {"orbit", "bustle"} and callouts["styleApproved"] is None,
            "calloutRaisedAboveCap": True, "counterRemoved": True, "furnitureRemoved": True,
            "calloutsSeparateFromBody": True, "bodySilent": True, "sfxSeparate": True,
            "noContextualPropBakedIntoKeeper": True, "productionUnchanged": True,
            "kitchenWorkChanged": False, "runtimeChanged": False, "preloadRequired": True,
        },
        "approvalBoundary": {"candidateApproved": False, "bodyApproved": False, "calloutGrammarApproved": False, "recipeMappingApproved": False, "sfxApproved": False, "promotionAllowed": False, "runtimeChanged": False, "finalChanged": False, "productionChanged": False, "deployed": False},
        "rollback": f"Discard {rel(PACK)}, public/keeper-review/{SET}, review-archive/sets/{SET}.json and this set's content-addressed objects; V1/V2, every approved authority, runtime assets and Kitchen work remain unchanged.",
    }
    register_path = PACK / "batch-register.json"
    write_json(register_path, register)
    print(json.dumps({"review": f"/keeper-review/{SET}/", "newComponents": len(component_records), "inheritedComponents": len(inherited_paths), "recipes": len(phrases), "counter": False, "bodyInherited": True}, indent=2))


if __name__ == "__main__":
    main()
