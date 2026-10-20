#!/usr/bin/env python3
"""Build the immutable V2 bubble-choreography refinement and model-test pack."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import math
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-rear-action-choreography-v2"
V1_SET = "keeper-prime-rear-action-choreography-v1"
PACK = ROOT / "art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2"
PUBLIC = ROOT / "public/keeper-review" / SET
V1_PUBLIC = ROOT / "public/keeper-review" / V1_SET
V1_DRAFT = ROOT / "art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v1"
CATALOGUE = PACK / "catalogue.json"
PUBLIC_CATALOGUE_GZ = PUBLIC / "catalogue.json.gz"
PAGE = PUBLIC / "index.html"
MODEL_PACK = PACK / "claude-code-model-test-pack"
ARCHIVE_INDEX = ROOT / "review-archive/index.json"
VERIFIER = ROOT / "scripts/verify_keeper_prime_rear_action_choreography_v2.mjs"
PACKAGE = ROOT / "package.json"
FRAME_COUNT = 42
FPS = 8
QUIET_START = 37


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    separators = (",", ":") if compact else None
    path.write_text(json.dumps(value, indent=None if compact else 2, separators=separators) + "\n")


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def round_state(item: dict[str, object]) -> dict[str, object]:
    result = dict(item)
    for key, digits in (("x", 2), ("y", 2), ("scale", 3), ("rotation", 2), ("opacity", 3)):
        result[key] = round(float(result[key]), digits)
    return result


def activity_envelope(frame: int) -> float:
    if frame >= QUIET_START:
        return 0.0
    if frame < 5:
        return frame / 5
    if frame > 33:
        return (QUIET_START - frame) / (QUIET_START - 33)
    return 1.0


def transform_object(item: dict[str, object], frame: int, support_index: int) -> dict[str, object]:
    result = dict(item)
    if frame >= QUIET_START or float(item["opacity"]) <= 0:
        return round_state(result)
    envelope = activity_envelope(frame) * float(item["opacity"])
    phase = support_index * 1.71 + len(str(item["instance"])) * 0.19
    if item["role"] == "support":
        lanes = ((-48, -24), (52, -18), (-46, 30))
        lane_x, lane_y = lanes[support_index % len(lanes)]
        interaction_centre = (13, 20, 26)[support_index % 3]
        interaction = math.exp(-((frame - interaction_centre) / 2.4) ** 2)
        separation = 1 - 0.22 * interaction
        result["x"] = clamp(float(item["x"]) * 1.24 + lane_x * envelope * separation + math.sin(frame * .58 + phase) * 10 * envelope, -112, 112)
        result["y"] = clamp(float(item["y"]) * 1.12 + lane_y * envelope * separation + math.cos(frame * .46 + phase) * 7 * envelope, -72, 68)
        result["scale"] = float(item["scale"]) * (1 - .16 * envelope)
        result["rotation"] = float(item["rotation"]) + math.sin(frame * .51 + phase) * 6 * envelope
    else:
        result["x"] = clamp(float(item["x"]) * 1.08 + math.sin(frame * .37 + phase) * 4 * envelope, -108, 108)
        result["y"] = clamp(float(item["y"]) + math.cos(frame * .41 + phase) * 3 * envelope, -70, 68)
        result["scale"] = float(item["scale"]) * (1 - .06 * envelope)
        result["rotation"] = float(item["rotation"]) + math.sin(frame * .43 + phase) * 2.5 * envelope
    return round_state(result)


def transform_existing_symbol(item: dict[str, object], frame: int, index: int) -> dict[str, object]:
    result = dict(item)
    if frame >= QUIET_START or float(item["opacity"]) <= 0:
        return round_state(result)
    envelope = activity_envelope(frame) * float(item["opacity"])
    phase = index * 1.37
    result["x"] = clamp(float(item["x"]) * 1.22 + math.sin(frame * .67 + phase) * 6 * envelope, -118, 118)
    result["y"] = clamp(float(item["y"]) * 1.08 + math.cos(frame * .53 + phase) * 5 * envelope, -78, 72)
    result["rotation"] = float(item["rotation"]) + math.sin(frame * .72 + phase) * 7 * envelope
    return round_state(result)


def momentum_tick(current: dict[str, object], previous: dict[str, object], support_index: int, frame: int) -> dict[str, object]:
    dx = float(current["x"]) - float(previous["x"])
    dy = float(current["y"]) - float(previous["y"])
    speed = math.hypot(dx, dy)
    direction_x, direction_y = (dx / speed, dy / speed) if speed > .001 else (1.0, 0.0)
    normal_x, normal_y = -direction_y, direction_x
    trailing_distance = 18 + min(10, speed)
    side = -1 if support_index % 2 else 1
    opacity = 0.0 if frame >= QUIET_START or float(current["opacity"]) < .12 or speed < .8 else min(1.0, float(current["opacity"]) * (.35 + speed / 6))
    return round_state({
        "instance": f"momentum-{current['instance']}",
        "component": "symbol-motion-ticks",
        "role": "momentum",
        "motionFunction": "directional-trail",
        "anchorInstance": current["instance"],
        "x": clamp(float(current["x"]) - direction_x * trailing_distance + normal_x * 8 * side, -120, 120),
        "y": clamp(float(current["y"]) - direction_y * trailing_distance + normal_y * 8 * side, -80, 74),
        "scale": .26 + min(.19, speed / 45),
        "rotation": math.degrees(math.atan2(dy, dx)),
        "opacity": opacity,
        "z": 10 + support_index,
    })


def contact_star(support: dict[str, object], anchor: dict[str, object], support_index: int, frame: int, story_index: int) -> dict[str, object]:
    centres = (14, 20, 26)
    centre = centres[support_index] + story_index % 2
    distance = math.hypot(float(support["x"]) - float(anchor["x"]), float(support["y"]) - float(anchor["y"]))
    beat = math.exp(-((frame - centre) / 2.05) ** 2)
    proximity = clamp((92 - distance) / 46, 0, 1)
    opacity = 0.0 if frame >= QUIET_START else min(1.0, beat * (.45 + .55 * proximity) * max(float(support["opacity"]), float(anchor["opacity"])))
    return round_state({
        "instance": f"contact-{support['instance']}",
        "component": "symbol-impact-star",
        "role": "interaction",
        "motionFunction": "contact-impact",
        "anchorInstance": support["instance"],
        "interactionWith": anchor["instance"],
        "x": clamp((float(support["x"]) + float(anchor["x"])) / 2, -116, 116),
        "y": clamp((float(support["y"]) + float(anchor["y"])) / 2 - 5, -78, 72),
        "scale": .24 + .28 * beat,
        "rotation": -16 + support_index * 17 + frame * 5,
        "opacity": opacity,
        "z": 14 + support_index,
    })


def transform_bubble(story_id: str, story_index: int, full: list[dict[str, object]]) -> list[dict[str, object]]:
    transformed_objects = []
    for frame_row in full:
        frame = int(frame_row["frame"])
        support_index = 0
        objects = []
        for item in frame_row["objects"]:
            index = support_index
            if item["role"] == "support":
                support_index += 1
            objects.append(transform_object(item, frame, index))
        transformed_objects.append(objects)

    transformed = []
    for frame_row, objects in zip(full, transformed_objects):
        frame = int(frame_row["frame"])
        symbols = [transform_existing_symbol(item, frame, index) for index, item in enumerate(frame_row["symbols"])]
        supports = [item for item in objects if item["role"] == "support"]
        anchor = max((item for item in objects if item["role"] in ("hero", "resolved")), key=lambda item: item["opacity"])
        previous_objects = transformed_objects[max(0, frame - 1)]
        previous_by_instance = {item["instance"]: item for item in previous_objects}
        for support_index, support in enumerate(supports):
            symbols.append(momentum_tick(support, previous_by_instance[support["instance"]], support_index, frame))
            symbols.append(contact_star(support, anchor, support_index, frame, story_index))
        transformed.append({**frame_row, "objects": objects, "symbols": symbols})
    return transformed


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
            value = dict(item)
            value["rotation"] = 0
            if item["instance"] not in (primary["instance"], secondary["instance"]):
                value["opacity"] = 0
            objects.append(value)
        selected = max(sampled["symbols"], key=lambda item: item["opacity"], default=None)
        symbols = []
        for item in sampled["symbols"]:
            value = dict(item)
            value["rotation"] = 0
            if frame >= QUIET_START or selected is None or item["instance"] != selected["instance"]:
                value["opacity"] = 0
            else:
                value["opacity"] = min(float(value["opacity"]), .65)
            symbols.append(value)
        frames.append({
            "frame": frame,
            "timeMs": frame * 1000 / FPS,
            "storyPhase": sampled["storyPhase"],
            "quietTail": frame >= QUIET_START,
            "holdSegment": [start, end],
            "objects": objects,
            "symbols": symbols,
        })
    return frames


def build_page() -> str:
    page = (V1_PUBLIC / "index.html").read_text()
    replacements = {
        "keeper-prime-rear-action-choreography-v1": SET,
        "Richer activity-cloud choreography": "Bubble activity-cloud refinement",
        "Immutable V1 candidate": "Immutable V2 bubble refinement",
        "Four authored visual stories": "Four livelier bubble stories",
        "Open + bubble staging": "V1 open staging preserved",
        "Compact bustle · bubble": "Livelier bustle · refined bubble",
        "background:rgba(246,239,211,.14)": "background:rgba(246,239,211,.22)",
        "border:3px solid rgba(239,246,245,.78)": "border:3px solid rgba(239,246,245,.84)",
        "inset 0 0 28px rgba(115,210,197,.08)": "inset 0 0 34px rgba(244,231,204,.13)",
        "left:48px;bottom:3px;background:rgba(246,239,211,.08)": "left:168px;bottom:1px;background:rgba(246,239,211,.16)",
        "<option value=\"bubble\">Livelier bustle · refined bubble</option>": "<option value=\"bubble\" selected>Livelier bustle · refined bubble</option>",
        "Ready · ${preloadUrls().length} unique images decoded · four stories × two authored treatments × full/reduced motion": "Ready · ${preloadUrls().length} unique images decoded · refined bubble bustle + byte-exact V1 open treatment",
    }
    for old, new in replacements.items():
        if old not in page:
            raise RuntimeError(f"page replacement token missing: {old}")
        page = page.replace(old, new)
    page = page.replace(
        '<a href="/keeper-review/keeper-prime-rear-action-sequence-v1/index.html">← Approved Prime Rear Action Sequence V1</a>',
        f'<a href="/keeper-review/{V1_SET}/index.html">← Immutable choreography V1</a> · <a href="/keeper-review/keeper-prime-rear-action-sequence-v1/index.html">Approved Prime sequence</a>',
    )
    page = page.replace(
        "This gate changes only the independently controlled review callout above the cap.",
        "V2 keeps the approved Prime sequence and V1 open treatment exact while refining only the bubble: lighter fill, head-aligned connector, wider object lanes and denser independent ticks/stars.",
    )
    decode_function = "function decode(url){return new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>img.decode?img.decode().then(resolve,reject):resolve();img.onerror=()=>reject(new Error(`Could not load ${url}`));img.src=url})}"
    fetch_function = "async function fetchGzip(url){const response=await fetch(url);if(!response.ok)throw new Error(`Catalogue ${response.status}`);const stream=response.body.pipeThrough(new DecompressionStream('gzip'));return new Response(stream).json()}"
    if decode_function not in page:
        raise RuntimeError("decode function insertion point missing")
    page = page.replace(decode_function, f"{decode_function}\n{fetch_function}")
    old_fetch = "fetch(`/keeper-review/${SET}/catalogue.json`).then(response=>response.json())"
    if old_fetch not in page:
        raise RuntimeError("catalogue fetch replacement point missing")
    page = page.replace(old_fetch, "fetchGzip(`/keeper-review/${SET}/catalogue.json.gz`)")
    return page


def source_path(url: str, archive: dict[str, object]) -> Path:
    public = ROOT / "public" / url.lstrip("/")
    if public.exists():
        return public
    entry = archive["legacyPaths"].get(url)
    if not entry:
        raise RuntimeError(f"asset is not public or archived: {url}")
    return ROOT / entry["object"]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:48] or "asset"


def copy_asset(source: Path, destination: Path, expected_sha: str) -> None:
    if sha(source) != expected_sha:
        raise RuntimeError(f"source hash drift: {rel(source)}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    if sha(destination) != expected_sha:
        raise RuntimeError(f"copy hash drift: {rel(destination)}")


def build_model_pack(catalogue: dict[str, object], v1: dict[str, object]) -> dict[str, object]:
    if MODEL_PACK.exists():
        shutil.rmtree(MODEL_PACK)
    archive = json.loads(ARCHIVE_INDEX.read_text())
    assets: list[dict[str, object]] = []
    by_url: dict[str, list[int]] = {}
    for index, frame in enumerate(catalogue["sequence"]):
        by_url.setdefault(frame["src"], []).append(index)
    for ordinal, (url, indices) in enumerate(by_url.items(), 1):
        frame = catalogue["sequence"][indices[0]]
        digest = frame.get("authoritySha256", frame.get("candidateSha256"))
        source = source_path(url, archive)
        destination = MODEL_PACK / "assets/body" / f"{ordinal:02d}-{slug(frame['pose'])}-{digest[:12]}.png"
        copy_asset(source, destination, digest)
        assets.append({
            "id": f"body-{ordinal:02d}", "kind": "approved-prime-body", "sourceUrl": url,
            "sourceFile": rel(source), "sourceSha256": digest, "file": rel(destination),
            "sha256": digest, "usedBySequenceFrames": indices,
        })
    for component_id, component in catalogue["inheritedComponents"].items():
        digest = component["sha256"]
        source = source_path(component["src"], archive)
        destination = MODEL_PACK / "assets/activity" / f"{component_id}-{digest[:12]}.png"
        copy_asset(source, destination, digest)
        assets.append({
            "id": component_id, "kind": "activity-object", "family": component["family"],
            "sourceUrl": component["src"], "sourceFile": rel(source), "sourceSha256": digest,
            "file": rel(destination), "sha256": digest,
        })
    for component_id, component in catalogue["symbols"].items():
        digest = component["sha256"]
        source = source_path(component["src"], archive)
        destination = MODEL_PACK / "assets/symbol" / f"{component_id}-{digest[:12]}.png"
        copy_asset(source, destination, digest)
        assets.append({
            "id": component_id, "kind": "comic-symbol", "family": component["family"],
            "sourceUrl": component["src"], "sourceFile": rel(source), "sourceSha256": digest,
            "file": rel(destination), "sha256": digest,
        })
    source_sheet = V1_DRAFT / "source/activity-comic-symbols-source-sheet.png"
    sheet_destination = MODEL_PACK / "assets/source/activity-comic-symbols-source-sheet.png"
    copy_asset(source_sheet, sheet_destination, sha(source_sheet))
    assets.append({
        "id": "activity-comic-symbols-source-sheet", "kind": "isolated-symbol-source-sheet",
        "sourceFile": rel(source_sheet), "sourceSha256": sha(source_sheet),
        "file": rel(sheet_destination), "sha256": sha(sheet_destination),
    })

    metadata = MODEL_PACK / "metadata"
    metadata.mkdir(parents=True, exist_ok=True)
    write_json(metadata / "v2-catalogue.json", catalogue, compact=True)
    shutil.copyfile(V1_PUBLIC / "catalogue.json", metadata / "v1-catalogue.json")
    sequence_file = ROOT / catalogue["sourceSequence"]["file"]
    vocabulary_file = ROOT / catalogue["sourceVocabulary"]["file"]
    shutil.copyfile(sequence_file, metadata / "approved-prime-sequence.json")
    shutil.copyfile(vocabulary_file, metadata / "activity-vocabulary.json")
    manifest = {
        "schema": "lighthouse-keeper/activity-cloud-model-test-pack@1",
        "set": SET,
        "purpose": "Self-contained Claude Code model-test input; every visual file used by V2 plus the isolated symbol source sheet.",
        "assetCount": len(assets),
        "bodyAssetCount": sum(asset["kind"] == "approved-prime-body" for asset in assets),
        "activityAssetCount": sum(asset["kind"] == "activity-object" for asset in assets),
        "symbolAssetCount": sum(asset["kind"] == "comic-symbol" for asset in assets),
        "sourceAssetCount": sum(asset["kind"] == "isolated-symbol-source-sheet" for asset in assets),
        "assets": assets,
        "constraints": {
            "inputOnly": True,
            "doNotOverwriteCanonicalOrThisPack": True,
            "approvedPrimeBytesMustRemainExact": True,
            "newOutputMustUseANewVersionedDirectory": True,
            "runtimePromotionAllowed": False,
            "kitchenChangesAllowed": False,
        },
    }
    write_json(MODEL_PACK / "asset-manifest.json", manifest)
    (MODEL_PACK / "README.md").write_text(f"""# Claude Code model-test asset pack

This self-contained input pack contains every visual asset referenced by `{SET}`:

- {manifest['bodyAssetCount']} byte-exact approved Prime body images;
- {manifest['activityAssetCount']} independently owned activity-object images;
- {manifest['symbolAssetCount']} independently owned comic-symbol images;
- the isolated six-cell symbol source sheet;
- V1/V2 catalogues, approved sequence metadata and activity vocabulary.

Start with `asset-manifest.json`; every file has its original URL, repository source, SHA-256 and local pack path. The V2 timelines are in `metadata/v2-catalogue.json`.

This directory is input-only. Ask a model to write experiments to a new versioned directory and never overwrite this pack, V1, approved Prime assets, runtime art or Kitchen work.
""")
    (MODEL_PACK / "CLAUDE_CODE_MODEL_TEST_PROMPT.md").write_text(f"""Use the self-contained asset pack at `{rel(MODEL_PACK)}` to test alternative model-authored bubble choreography.

Read `asset-manifest.json`, `metadata/v2-catalogue.json` and `README.md` first. Use only the supplied visual assets. Preserve every approved Prime body image byte-for-byte. Keep body, hero/result, supporting objects, comic symbols and treatment marks independently controllable. Explore lively but legible bubble staging with clear head-to-bubble origin, low overlap, mobile objects and abundant separate ticks/stars. Preserve a five-frame quiet tail and reduced-motion mode.

Write all outputs into a new versioned draft directory. Do not modify this pack, V1/V2, runtime/Final assets, Kitchen work or deployment configuration, and do not deploy.
""")
    return manifest


def main() -> None:
    required = (V1_PUBLIC / "catalogue.json", V1_PUBLIC / "index.html", ARCHIVE_INDEX, VERIFIER, PACKAGE)
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing dependency: {rel(path)}")
    v1 = json.loads((V1_PUBLIC / "catalogue.json").read_text())
    catalogue = copy.deepcopy(v1)
    catalogue["schema"] = "lighthouse-keeper/keeper-prime-rear-action-choreography@2"
    catalogue["set"] = SET
    catalogue["status"] = "immutable-reversible-bubble-refinement-candidate-not-approved"
    catalogue["predecessor"] = {
        "set": V1_SET,
        "catalogueFile": rel(V1_PUBLIC / "catalogue.json"),
        "catalogueSha256": sha(V1_PUBLIC / "catalogue.json"),
        "pageFile": rel(V1_PUBLIC / "index.html"),
        "pageSha256": sha(V1_PUBLIC / "index.html"),
        "manifestFile": f"review-archive/sets/{V1_SET}.json",
        "manifestSha256": sha(ROOT / f"review-archive/sets/{V1_SET}.json"),
    }
    catalogue["defaultTreatment"] = "bubble"
    catalogue["callout"]["bubbleRefinement"] = {
        "mainFill": "rgba(246,239,211,.22)",
        "connectorLeftPx": 168,
        "connectorRelationship": "head-aligned",
        "supportingObjectLanes": 3,
        "additionalKineticSymbolsPerStory": 6,
        "kineticSymbolGrammar": {
            "directionalTrails": 3,
            "contactImpacts": 3,
            "marksFollowOwnedObjectMotion": True,
        },
        "openTreatmentChanged": False,
    }
    for story_index, (story_id, story) in enumerate(catalogue["stories"].items()):
        full = transform_bubble(story_id, story_index, story["timelines"]["bubble"]["full"])
        story["timelines"]["bubble"] = {"full": full, "reduced": reduced_timeline(full)}

    PUBLIC.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)
    write_json(CATALOGUE, catalogue, compact=True)
    stale_plain_catalogue = PUBLIC / "catalogue.json"
    if stale_plain_catalogue.exists():
        stale_plain_catalogue.unlink()
    PUBLIC_CATALOGUE_GZ.write_bytes(gzip.compress(CATALOGUE.read_bytes(), compresslevel=9, mtime=0))
    page = build_page()
    PAGE.write_text(page)
    (PACK / "page-template.html").write_text(page)
    model_manifest = build_model_pack(catalogue, v1)

    register = {
        "schema": "lighthouse-keeper/keeper-prime-rear-action-choreography-register@2",
        "set": SET,
        "status": catalogue["status"],
        "purpose": "Frank-directed V2 bubble refinement: lighter fill, head-aligned connector, more mobile separated objects, object-trailing momentum ticks and interaction-owned impact stars.",
        "predecessor": catalogue["predecessor"],
        "publishedAssets": [],
        "candidate": {
            "publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)},
            "catalogue": {"file": rel(CATALOGUE), "sha256": sha(CATALOGUE)},
            "publicCatalogueGzip": {"file": rel(PUBLIC_CATALOGUE_GZ), "sha256": sha(PUBLIC_CATALOGUE_GZ)},
            "stories": list(catalogue["stories"]),
            "storyCount": len(catalogue["stories"]),
            "treatmentsPerStory": 2,
            "motionModesPerTreatment": 2,
            "timelineFrames": FRAME_COUNT,
            "timelineFps": FPS,
            "quietTailFrames": FRAME_COUNT - QUIET_START,
            "sequenceFrames": len(catalogue["sequence"]),
        },
        "modelTestPack": {
            "directory": rel(MODEL_PACK),
            "manifest": rel(MODEL_PACK / "asset-manifest.json"),
            "manifestSha256": sha(MODEL_PACK / "asset-manifest.json"),
            "assetCount": model_manifest["assetCount"],
            "prompt": rel(MODEL_PACK / "CLAUDE_CODE_MODEL_TEST_PROMPT.md"),
        },
        "files": {
            "draftCatalogue": {"file": rel(CATALOGUE), "sha256": sha(CATALOGUE)},
            "template": {"file": rel(PACK / "page-template.html"), "sha256": sha(PACK / "page-template.html")},
            "builder": {"file": rel(Path(__file__)), "sha256": sha(Path(__file__))},
            "verifier": {"file": rel(VERIFIER), "sha256": sha(VERIFIER)},
        },
        "checks": {
            "v1BytesUnchanged": True,
            "approvedPrimeSequenceByteExact": True,
            "openTreatmentByteExactToV1": True,
            "bubbleOnlyRefinement": True,
            "layersIndependent": True,
            "modelTestPackSelfContained": True,
            "runtimeChanged": False,
            "kitchenChanged": False,
            "deployed": False,
        },
        "rollback": "Delete only this V2 draft directory, V2 public review directory, V2 archive set manifest, builder, verifier, package command and V2 documentation references. V1, approved Prime authorities, runtime, Final and Kitchen remain untouched.",
    }
    write_json(PACK / "batch-register.json", register)
    print(json.dumps({
        "set": SET,
        "stories": list(catalogue["stories"]),
        "bubbleKineticSymbolsPerStory": 6,
        "modelTestAssets": model_manifest["assetCount"],
        "publishedAssets": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
