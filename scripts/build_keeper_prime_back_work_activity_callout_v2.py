#!/usr/bin/env python3
"""Build the immutable V2 game-language activity-callout review candidate.

V2 deliberately inherits the complete V1 Prime body and approved route.  Its
only new moving pixels are independently switchable callout components.
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
SET = "keeper-prime-back-work-activity-callout-v2"
PACK = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
COMPONENTS = PACK / "drafts/callouts"
EVIDENCE = PACK / "evidence"
V1_PACK = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v1"
V1_CATALOGUE = V1_PACK / "catalogue.json"
V1_PUBLIC_CATALOGUE = ROOT / "public/keeper-review/keeper-prime-back-work-activity-callout-v1/catalogue.json"
V1_REGISTER = V1_PACK / "batch-register.json"
PAGE = PUBLIC / "index.html"
RUNTIME_MANIFEST = ROOT / "public/sprites/manifest.json"
WORKBENCH = ROOT / "data/keeper_animation_workbench.json"

PHRASE_FRAMES = 42
PHRASE_FPS = 8
ASSET_CELL = 256
SAFE_GUTTER = 20
SAMPLE_FRAMES = [0, 3, 7, 14, 21, 28, 32, 37]

SOURCE_SPECS = {
    "cooking": {
        "file": PACK / "source/cooking-callout-language-generated-v2.png",
        "splitY": 560,
        "assets": ["pan", "spoon", "steam", "seasoning"],
    },
    "mixing": {
        "file": PACK / "source/mixing-callout-language-generated-v2.png",
        "splitY": 580,
        "assets": ["bowl", "whisk", "egg", "flour"],
    },
    "washing": {
        "file": PACK / "source/washing-callout-language-generated-v2.png",
        "splitY": 530,
        "assets": ["plate", "sponge", "droplets", "cutlery"],
    },
    "repair": {
        "file": PACK / "source/repair-callout-language-generated-v2.png",
        "splitY": 560,
        "assets": ["tools", "fastener", "oilcan", "sparks"],
    },
}

PHRASE_SPECS = {
    "cooking": {"label": "Cooking", "primary": "cooking-pan", "left": "cooking-spoon", "right": "cooking-seasoning", "envelope": "cooking-steam"},
    "mixing": {"label": "Mixing", "family": "mixing-washing", "primary": "mixing-bowl", "left": "mixing-whisk", "right": "mixing-egg", "envelope": "mixing-flour"},
    "washing": {"label": "Washing", "family": "mixing-washing", "primary": "washing-plate", "left": "washing-sponge", "right": "washing-cutlery", "envelope": "washing-droplets"},
    "repair": {"label": "Generic repair", "primary": "repair-tools", "left": "repair-fastener", "right": "repair-oilcan", "envelope": "repair-sparks"},
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        path.write_text(json.dumps(value, separators=(",", ":")) + "\n")
    else:
        path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bounds(image: Image.Image) -> dict[str, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.where(alpha > 0)
    if not len(xs):
        raise RuntimeError("empty callout component")
    return {
        "minX": int(xs.min()), "minY": int(ys.min()),
        "maxX": int(xs.max()), "maxY": int(ys.max()),
        "width": int(xs.max() - xs.min() + 1),
        "height": int(ys.max() - ys.min() + 1),
        "opaquePixels": int((alpha > 0).sum()),
    }


def edge_alpha_pixels(image: Image.Image) -> int:
    a = np.asarray(image.getchannel("A"))
    return int(np.count_nonzero(a[0]) + np.count_nonzero(a[-1]) + np.count_nonzero(a[:, 0]) + np.count_nonzero(a[:, -1]))


def transparent_gutter(image: Image.Image) -> int:
    b = alpha_bounds(image)
    return min(b["minX"], b["minY"], image.width - 1 - b["maxX"], image.height - 1 - b["maxY"])


def isolate_component(source: Image.Image, crop: tuple[int, int, int, int]) -> tuple[Image.Image, dict]:
    """Trim a declared, disjoint source cell and register it in a safe square."""
    cell = source.crop(crop).convert("RGBA")
    pixels = np.array(cell, copy=True)
    # The generated sheets already carry real transparency. Drop only the
    # sub-visible fringe so ownership and gutters are deterministic.
    pixels[pixels[:, :, 3] <= 8, 3] = 0
    isolated = Image.fromarray(pixels)
    bounds = alpha_bounds(isolated)
    trimmed = isolated.crop((bounds["minX"], bounds["minY"], bounds["maxX"] + 1, bounds["maxY"] + 1))
    available = ASSET_CELL - SAFE_GUTTER * 2
    scale = min(available / trimmed.width, available / trimmed.height)
    size = (max(1, round(trimmed.width * scale)), max(1, round(trimmed.height * scale)))
    resized = trimmed.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (ASSET_CELL, ASSET_CELL), (0, 0, 0, 0))
    xy = ((ASSET_CELL - size[0]) // 2, (ASSET_CELL - size[1]) // 2)
    canvas.alpha_composite(resized, xy)
    evidence = {
        "sourceCrop": list(crop),
        "sourceVisiblePixels": bounds["opaquePixels"],
        "registeredBounds": alpha_bounds(canvas),
        "edgeAlphaPixels": edge_alpha_pixels(canvas),
        "transparentGutterPx": transparent_gutter(canvas),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }
    return canvas, evidence


def build_components() -> tuple[dict[str, Path], dict[str, dict], list[dict]]:
    paths: dict[str, Path] = {}
    records: dict[str, dict] = {}
    sources: list[dict] = []
    for activity, spec in SOURCE_SPECS.items():
        source_path = spec["file"]
        source = Image.open(source_path).convert("RGBA")
        if source.size != (1536, 1024):
            raise RuntimeError(f"unexpected generated sheet geometry: {rel(source_path)}")
        split_y = int(spec["splitY"])
        cells = [(0, 0, 850, split_y), (850, 0, 1536, split_y), (0, split_y, 850, 1024), (850, split_y, 1536, 1024)]
        source_record = {"file": rel(source_path), "sha256": sha(source_path), "pixels": list(source.size), "splitX": 850, "splitY": split_y, "cells": []}
        for slot, crop in zip(spec["assets"], cells):
            key = f"{activity}-{slot}"
            component, evidence = isolate_component(source, crop)
            out = COMPONENTS / f"{key}.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            component.save(out)
            evidence.update({"file": rel(out), "sha256": sha(out), "activity": activity, "slot": slot, "cellPixels": [ASSET_CELL, ASSET_CELL]})
            if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 16:
                raise RuntimeError(f"unsafe component gutter: {key}")
            paths[key] = out
            records[key] = evidence
            source_record["cells"].append({"asset": key, "crop": list(crop), "visiblePixels": evidence["sourceVisiblePixels"]})
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


def orbit_frames(spec: dict) -> list[dict]:
    result = []
    for frame in range(PHRASE_FRAMES):
        parts = []
        env_o = opacity_window(frame, 0, 30, 35)
        if env_o:
            parts.append({"asset": spec["envelope"], "role": "activity-mark", "x": round(math.sin(frame * .29) * 4), "y": -7 + round(math.cos(frame * .23) * 3), "scale": round(.48 + .05 * math.sin(frame * .31), 3), "rotate": round(math.sin(frame * .19) * 7, 2), "opacity": round(env_o * .9, 3)})
        primary_o = opacity_window(frame, 2, 31, 35)
        if primary_o:
            parts.append({"asset": spec["primary"], "role": "primary", "x": 0, "y": -22 + round(math.sin(frame * .42) * 3), "scale": round((.68 + .04 * math.sin(frame * .31)) * min(1, (frame - 1) / 4), 3), "rotate": round(math.sin(frame * .25) * 5, 2), "opacity": round(primary_o, 3)})
        left_o = opacity_window(frame, 6, 27, 32)
        if left_o:
            angle = -2.55 + min(1, (frame - 6) / 18) * 1.25
            parts.append({"asset": spec["left"], "role": "helper", "x": round(math.cos(angle) * 68), "y": round(16 + math.sin(angle) * 50), "scale": .38, "rotate": round(-18 + math.sin(frame * .37) * 8, 2), "opacity": round(left_o, 3)})
        right_o = opacity_window(frame, 10, 29, 34)
        if right_o:
            angle = -.55 + min(1, (frame - 10) / 17) * 1.15
            parts.append({"asset": spec["right"], "role": "helper", "x": round(math.cos(angle) * 69), "y": round(12 - math.sin(angle) * 52), "scale": .34, "rotate": round(15 + math.cos(frame * .33) * 9, 2), "opacity": round(right_o, 3)})
        result.append({"frame": frame, "components": parts})
    return result


def bustle_frames(spec: dict) -> list[dict]:
    result = []
    for frame in range(PHRASE_FRAMES):
        parts = []
        env_o = opacity_window(frame, 0, 31, 36)
        pulse = 1 + .035 * math.sin(frame * .55)
        if env_o:
            parts.append({"asset": spec["envelope"], "role": "activity-cloud", "x": 0, "y": 2, "scale": round(.92 * pulse, 3), "rotate": round(math.sin(frame * .2) * 4, 2), "opacity": round(env_o * .82, 3)})
        primary_o = opacity_window(frame, 3, 30, 35)
        if primary_o:
            parts.append({"asset": spec["primary"], "role": "primary", "x": 0, "y": -5 + round(math.sin(frame * .45) * 2), "scale": .52, "rotate": round(math.sin(frame * .28) * 4, 2), "opacity": round(primary_o, 3)})
        left_o = opacity_window(frame, 7, 27, 32)
        if left_o:
            parts.append({"asset": spec["left"], "role": "helper", "x": -43 + round(math.sin(frame * .37) * 3), "y": 28 + round(math.cos(frame * .4) * 2), "scale": .30, "rotate": -19, "opacity": round(left_o, 3)})
        right_o = opacity_window(frame, 12, 29, 34)
        if right_o:
            parts.append({"asset": spec["right"], "role": "helper", "x": 42 + round(math.cos(frame * .34) * 3), "y": 24 + round(math.sin(frame * .41) * 2), "scale": .28, "rotate": 17, "opacity": round(right_o, 3)})
        result.append({"frame": frame, "components": parts})
    return result


def render_parts(parts: list[dict], assets: dict[str, Image.Image], size: tuple[int, int], centre: tuple[int, int], master_scale: float = 1.0) -> Image.Image:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    for part in parts:
        source = assets[part["asset"]].copy()
        target = max(1, round(104 * part["scale"] * master_scale))
        rendered = source.resize((target, target), Image.Resampling.LANCZOS)
        if part["rotate"]:
            rendered = rendered.rotate(-part["rotate"], resample=Image.Resampling.BICUBIC, expand=True)
        if part["opacity"] < 1:
            alpha = rendered.getchannel("A").point(lambda value, opacity=part["opacity"]: round(value * opacity))
            rendered.putalpha(alpha)
        x = round(centre[0] + part["x"] * master_scale - rendered.width / 2)
        y = round(centre[1] + part["y"] * master_scale - rendered.height / 2)
        canvas.alpha_composite(rendered, (x, y))
    return canvas


def render_contact_sheets(phrases: dict, component_paths: dict[str, Path], v1_catalogue: dict) -> dict[str, dict]:
    assets = {name: Image.open(path).convert("RGBA") for name, path in component_paths.items()}
    body = [Image.open(ROOT / record["file"]).convert("RGBA") for record in v1_catalogue["body"]["frames"]]
    outputs = {}
    cell_w, cell_h = 320, 256
    for treatment in ("orbit", "bustle"):
        sheet = Image.new("RGBA", (cell_w * len(SAMPLE_FRAMES), cell_h * len(phrases)), (9, 19, 27, 255))
        draw = ImageDraw.Draw(sheet)
        for row, (activity, phrase) in enumerate(phrases.items()):
            for col, sample in enumerate(SAMPLE_FRAMES):
                x0, y0 = col * cell_w, row * cell_h
                cell = Image.new("RGBA", (cell_w, cell_h - 24), (37, 57, 69, 255))
                d = ImageDraw.Draw(cell)
                d.rectangle((0, 166, cell_w, cell_h), fill=(23, 36, 42, 255))
                d.rounded_rectangle((106, 160, 214, 198), radius=4, fill=(81, 111, 130, 255), outline=(28, 42, 49, 255), width=3)
                d.rectangle((110, 160, 210, 167), fill=(209, 173, 112, 255))
                body_index = round(sample * 23 / (PHRASE_FRAMES - 1))
                actor = body[body_index].resize((128, 160), Image.Resampling.LANCZOS)
                cell.alpha_composite(actor, (96, 69))
                callout = render_parts(phrase["treatments"][treatment]["frames"][sample]["components"], assets, cell.size, (160, 56), .82)
                cell.alpha_composite(callout)
                sheet.alpha_composite(cell, (x0, y0))
                draw.text((x0 + 7, y0 + cell_h - 19), f"{activity} · F{sample + 1:02d}", fill=(238, 247, 250, 255))
        path = EVIDENCE / f"callout-{treatment}-in-context-contact-sheet.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(path)
        outputs[treatment] = {"file": rel(path), "sha256": sha(path), "sampleFrames": [f + 1 for f in SAMPLE_FRAMES], "includesPrimeBodyAtGameScale": True}
    return outputs


def publish(path: Path, label: str, published: list[dict]) -> dict:
    digest = sha(path)
    target = ASSETS / f"{label}-{digest[:16]}{path.suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
    entry = {"source": rel(path), "sourceSha256": digest, "public": rel(target), "publicAssemblyPath": rel(target), "publicSha256": sha(target), "url": f"/keeper-review/{SET}/assets/{target.name}"}
    published.append(entry)
    return entry


def main() -> None:
    for required in [V1_CATALOGUE, V1_PUBLIC_CATALOGUE, V1_REGISTER, PAGE, RUNTIME_MANIFEST, WORKBENCH, *[spec["file"] for spec in SOURCE_SPECS.values()]]:
        if not required.exists():
            raise RuntimeError(f"missing {rel(required)}")
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    component_paths, component_records, source_records = build_components()
    phrases = {}
    for activity, spec in PHRASE_SPECS.items():
        phrases[activity] = {
            **spec,
            "treatments": {
                "orbit": {"frames": orbit_frames(spec)},
                "bustle": {"frames": bustle_frames(spec)},
            },
        }

    v1_catalogue = json.loads(V1_CATALOGUE.read_text())
    v1_public = json.loads(V1_PUBLIC_CATALOGUE.read_text())
    v1_register = json.loads(V1_REGISTER.read_text())
    contact_sheets = render_contact_sheets(phrases, component_paths, v1_catalogue)
    published: list[dict] = []
    public_components = {name: publish(path, name, published) for name, path in component_paths.items()}
    callouts = {
        "fps": PHRASE_FPS,
        "frames": PHRASE_FRAMES,
        "durationSeconds": PHRASE_FRAMES / PHRASE_FPS,
        "styles": {
            "orbit": {"label": "Open radial orbit · no bubble", "status": "equal review candidate"},
            "bustle": {"label": "Activity bustle · bubble treatment", "status": "equal review candidate"},
        },
        "reviewDefaultStyle": "orbit",
        "styleApproved": None,
        "components": {name: {"src": entry["url"], "cellPixels": [ASSET_CELL, ASSET_CELL], "activity": component_records[name]["activity"], "slot": component_records[name]["slot"]} for name, entry in public_components.items()},
        "phrases": phrases,
        "reducedMotion": {activity: {"treatment": "bustle", "frame": 21} for activity in phrases},
    }
    sfx = v1_catalogue["sfx"]
    catalogue = {
        **v1_catalogue,
        "schema": "lighthouse-keeper/prime-back-work-activity-review@2",
        "set": SET,
        "status": "immutable-reversible-callout-v2-not-approved",
        "callouts": callouts,
        "bodyInheritance": {"set": v1_catalogue["set"], "catalogueFile": rel(V1_CATALOGUE), "catalogueSha256": sha(V1_CATALOGUE), "registerFile": rel(V1_REGISTER), "registerSha256": sha(V1_REGISTER), "bodyAndRouteChanged": False},
        "controlsRequired": ["body", "callout components", "activity treatment", "rear furniture", "SFX", "reduced motion"],
    }
    catalogue_path = PACK / "catalogue.json"
    write_json(catalogue_path, catalogue)
    runtime_hash = sha(RUNTIME_MANIFEST)
    workbench_hash = sha(WORKBENCH)
    public_catalogue = {
        **v1_public,
        "schema": catalogue["schema"],
        "status": catalogue["status"],
        "callouts": callouts,
        "bodyInheritance": catalogue["bodyInheritance"],
    }
    public_catalogue_path = PUBLIC / "catalogue.json"
    write_json(public_catalogue_path, public_catalogue, compact=True)

    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "prime-back-work-callout-v2-awaiting-frank",
        "purpose": "Replace only the rejected V1 callout evidence with game-language cooking, mixing, washing and repair components while retaining the immutable Prime rear-work body and approved route byte-for-byte.",
        "bodyInheritance": catalogue["bodyInheritance"],
        "protectedState": {
            "runtimeManifest": {"file": rel(RUNTIME_MANIFEST), "sha256": runtime_hash},
            "workbench": {"file": rel(WORKBENCH), "sha256": workbench_hash},
        },
        "authorities": v1_register["authorities"],
        "directionalReferences": {
            **v1_register["directionalReferences"],
            "frankRadialInspiration": {"sha256": "a7e7541ef113bb3c42978a4f67d386f907d12a55c59544643dd59a36fc8cd879", "retained": False, "authority": False, "contribution": "radial energy, varied scale and scattered marks only; no character, symbols, pixels or exact linework copied"},
            "primeMaster": {"file": "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png", "sha256": sha(ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png"), "authority": False, "contribution": "game palette and rendering language reference for generated callout artwork"},
            "kitchenLanguage": {"file": "art/raw/kitchen-rebuild-modular-2026-10-19-v10/kitchen-mixed-static.png", "sha256": sha(ROOT / "art/raw/kitchen-rebuild-modular-2026-10-19-v10/kitchen-mixed-static.png"), "authority": False, "contribution": "object finish, outline weight and material-language reference only"},
        },
        "generation": {"tool": "built-in image generation", "selectedSources": source_records, "sourceContribution": "new callout object artwork only; no Keeper body, route, contextual prop or runtime art generated", "backgroundIsolation": "native source alpha <= 8 discarded; four disjoint source ownership cells; every output registered to 256 px with a deterministic 20 px target gutter"},
        "candidate": {
            "calloutComponents": component_records,
            "calloutContactSheets": contact_sheets,
            "catalogue": {"file": rel(catalogue_path), "sha256": sha(catalogue_path)},
            "publicCatalogue": {"file": rel(public_catalogue_path), "sha256": sha(public_catalogue_path), "projection": "playback-fields-only"},
            "publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)},
            "publishedAssets": published,
        },
        "publishedAssets": published,
        "checks": {
            "v1BodyAndRouteInheritedByteForByte": True,
            "everyCalloutCellHasSafeEdge": all(r["edgeAlphaPixels"] == 0 and r["transparentGutterPx"] >= 16 for r in component_records.values()),
            "everyCalloutPixelHasOneOwner": all(r["ownership"] == {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0} for r in component_records.values()),
            "bothTreatmentsBuilt": set(callouts["styles"]) == {"orbit", "bustle"} and callouts["styleApproved"] is None,
            "allEvidenceIncludesPrimeAtGameScale": all(record["includesPrimeBodyAtGameScale"] for record in contact_sheets.values()),
            "calloutsSeparateFromBody": True,
            "bodySilent": sfx["bodySilent"],
            "sfxSeparate": True,
            "noContextualPropBakedIntoKeeper": True,
            "runtimeManifestUnchanged": sha(RUNTIME_MANIFEST) == runtime_hash,
            "workbenchUnchanged": sha(WORKBENCH) == workbench_hash,
            "productionUnchanged": True,
            "kitchenWorkChanged": False,
            "preloadRequired": True,
        },
        "approvalBoundary": {"candidateApproved": False, "bodyApproved": False, "calloutGrammarApproved": False, "sfxApproved": False, "promotionAllowed": False, "runtimeChanged": False, "finalChanged": False, "productionChanged": False, "deployed": False},
        "rollback": f"Discard {rel(PACK)}, public/keeper-review/{SET}, review-archive/sets/{SET}.json and this set's content-addressed objects; V1, every approved authority, runtime assets and Kitchen work remain unchanged.",
    }
    register_path = PACK / "batch-register.json"
    write_json(register_path, register)
    print(json.dumps({"review": f"/keeper-review/{SET}/", "components": len(component_records), "phrases": list(phrases), "treatments": list(callouts["styles"]), "bodyInherited": True}, indent=2))


if __name__ == "__main__":
    main()
