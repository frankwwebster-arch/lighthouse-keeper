#!/usr/bin/env python3
"""Build or verify the approved ligne-claire sandwich-family pack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from build_activity_story_ligne_claire_bbq_family_2026_10_21_v1 import (
    CELL,
    HEADER,
    INK,
    ROW_HEIGHT,
    VISIBLE_ALPHA,
    contact_sheet,
    edge_alpha_pixels,
    normalise,
    sha256,
    visible_bounds,
    write_hashes,
)


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1"
SET = "activity-story-ligne-claire-sandwich-2026-10-21-v1"

SPECS: tuple[dict[str, object], ...] = (
    {
        "id": "sandwich-bread",
        "label": "Bread",
        "family": "sandwich",
        "source": "sandwich-bread-source.png",
        "cache": "exec-aeb4e10f-47d4-469f-bb15-8d1133e3cdc6.png",
        "current": "review-archive/objects/11/11313cc6d0839d313ecb96ef4136e372904fe848de862034a2234637ecabb8c8.png",
        "currentSha256": "11313cc6d0839d313ecb96ef4136e372904fe848de862034a2234637ecabb8c8",
        "palette": [INK, (246, 229, 183), (231, 166, 56), (207, 92, 24)],
        "preserves": "exactly two overlapping square white-bread slices, with the front-left slice above the rear-right slice in the current low front three-quarter arrangement",
    },
    {
        "id": "sandwich-ham",
        "label": "Ham",
        "family": "sandwich",
        "source": "sandwich-ham-source.png",
        "cache": "exec-7918ad10-4002-4ac1-95aa-f31f16a8491e.png",
        "current": "review-archive/objects/d3/d3cdba07f6b695e7e9918fde92822aeb3f1d543aafde0b59bd204069641c4fb7.png",
        "currentSha256": "d3cdba07f6b695e7e9918fde92822aeb3f1d543aafde0b59bd204069641c4fb7",
        "palette": [INK, (245, 126, 106), (215, 73, 62), (246, 229, 183)],
        "preserves": "exactly two folded pink ham slices, stacked and curling into open ends on both sides in the current broad horizontal silhouette",
    },
    {
        "id": "sandwich-lettuce",
        "label": "Lettuce",
        "family": "sandwich",
        "source": "sandwich-lettuce-source.png",
        "cache": "exec-53624b20-2d29-4544-b1d9-0b8b7b13505b.png",
        "current": "review-archive/objects/3a/3addb510966c088b52b2d50a5a5e6088231a4e083798a95f8d98573e35b37ef5.png",
        "currentSha256": "3addb510966c088b52b2d50a5a5e6088231a4e083798a95f8d98573e35b37ef5",
        "palette": [INK, (16, 110, 62), (57, 148, 55), (139, 204, 35), (231, 236, 111)],
        "preserves": "exactly three overlapping loose lettuce leaves in the current compact fan, with ruffled edges and pale central ribs",
    },
    {
        "id": "sandwich-tomato",
        "label": "Tomato",
        "family": "sandwich",
        "source": "sandwich-tomato-source.png",
        "cache": "exec-46ef36db-2b48-4d0f-8800-091e7c5ea731.png",
        "current": "review-archive/objects/10/10f760734f45b9cf6e2ee7ca815f7c89137cd64854bd71de98b07beaa871e2be.png",
        "currentSha256": "10f760734f45b9cf6e2ee7ca815f7c89137cd64854bd71de98b07beaa871e2be",
        "palette": [INK, (195, 43, 55), (232, 72, 51), (245, 126, 106), (246, 229, 183), (57, 148, 55)],
        "preserves": "exactly one whole tomato behind-left and two overlapping slices in front-right, including the leafy calyx and visible seed chambers",
    },
    {
        "id": "cooking-sandwich",
        "label": "Finished sandwich",
        "family": "cooking",
        "source": "cooking-sandwich-source.png",
        "cache": "exec-8e4cc29f-07f4-41a5-80a2-134440e2f0ad.png",
        "current": "review-archive/objects/b8/b88b28b259ebbf7b4729f54116605009cf120bc9abe9c37dce0a19e4dfe847e4.png",
        "currentSha256": "b88b28b259ebbf7b4729f54116605009cf120bc9abe9c37dce0a19e4dfe847e4",
        "palette": [INK, (246, 229, 183), (231, 166, 56), (245, 126, 106), (232, 72, 51), (57, 148, 55), (139, 204, 35)],
        "preserves": "exactly two overlapping triangular finished sandwiches in the current lower-left and taller rear-right arrangement, each with bread, lettuce, tomato and ham",
    },
)

REJECTED: tuple[dict[str, str], ...] = (
    {
        "file": "rejected/cooking-sandwich-square-v1.png",
        "cache": "exec-524da84f-94ed-42da-ba10-6335e1a796d3.png",
        "reason": "The finished sandwich pair drifted into square full-slice sandwiches instead of preserving the current triangular quarters.",
    },
    {
        "file": "rejected/cooking-sandwich-square-v2.png",
        "cache": "exec-e41e2d61-d15e-4112-85aa-6240c4752ee4.png",
        "reason": "The targeted edit retained four-corner bread faces, so the two objects still did not read as the current triangular sandwich quarters.",
    },
    {
        "file": "rejected/cooking-sandwich-cheese-v3.png",
        "cache": "exec-a47a6663-bc36-431d-9ce0-83fd08eaa9a4.png",
        "reason": "The geometry was corrected, but yellow cheese was added even though the current asset contains bread, lettuce, tomato and ham only.",
    },
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def library_entries() -> dict[str, dict[str, object]]:
    return json.loads((ROOT / "data/activity-stories/pictures.json").read_text())["pictures"]


def build() -> None:
    source_dir = PACK / "source"
    component_dir = PACK / "drafts/components"
    evidence_dir = PACK / "evidence"
    component_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    entries: dict[str, object] = {}
    rows: list[tuple[dict[str, object], Image.Image]] = []
    for spec in SPECS:
        current_path = ROOT / str(spec["current"])
        source_path = source_dir / str(spec["source"])
        if sha256(current_path) != spec["currentSha256"]:
            raise RuntimeError(f"current source drift: {spec['id']}")
        source = Image.open(source_path)
        if source.mode != "RGBA":
            raise RuntimeError(f"source is not RGBA: {spec['id']}")
        if edge_alpha_pixels(source):
            raise RuntimeError(f"source touches an outer edge: {spec['id']}")
        palette = list(spec["palette"])
        component, evidence = normalise(source, palette)
        if evidence["edgeAlphaPixels"] or evidence["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe output: {spec['id']}")
        output_path = component_dir / f"{spec['id']}.png"
        component.save(output_path, optimize=True)
        entries[str(spec["id"])] = {
            "family": spec["family"],
            "label": spec["label"],
            "intent": "approved-new-version-v2",
            "priorLibraryVersion": 1,
            "currentLibraryVersion": 2,
            "proposedLibraryVersion": 2,
            "preserves": spec["preserves"],
            "currentReferenceFile": spec["current"],
            "currentReferenceSha256": spec["currentSha256"],
            "sourceFile": rel(source_path),
            "sourceSha256": sha256(source_path),
            "sourcePixels": list(source.size),
            "originalCacheFile": spec["cache"],
            "flatPalette": ["#%02x%02x%02x" % colour for colour in palette],
            "derivation": "alpha>8 crop; Lanczos scale to fit 216px; nearest fixed RGB palette; integer-centred in transparent 256x256 RGBA; lossless PNG",
            "file": rel(output_path),
            "sha256": sha256(output_path),
            "cellPixels": [CELL, CELL],
            **evidence,
        }
        rows.append((spec, component))

    contact_path = evidence_dir / "current-vs-ligne-claire-contact-sheet.png"
    contact_sheet(rows).save(contact_path, optimize=True)
    rejected = [{**item, "sha256": sha256(PACK / item["file"])} for item in REJECTED]
    register = {
        "schema": "lighthouse-keeper/activity-story-ligne-claire-family-pack@1",
        "set": SET,
        "status": "approved-and-registered",
        "created": "2026-10-21",
        "tool": "built-in image generation plus deterministic fixed-palette normalisation",
        "families": ["sandwich", "cooking"],
        "semanticSet": "sandwich ingredients and their finished result",
        "visualAuthority": "art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/drafts/components",
        "preservationRule": "Translate each current asset's drawing language while preserving subject identity, viewpoint, object count, container, construction, state, recognisable contents, relative arrangement and broad silhouette.",
        "visibleAlphaThreshold": VISIBLE_ALPHA,
        "components": entries,
        "rejected": rejected,
        "evidence": {
            "file": rel(contact_path),
            "sha256": sha256(contact_path),
            "columns": 5,
            "rows": len(rows),
            "coveredIds": [spec["id"] for spec in SPECS],
        },
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersAtLeast20": True,
            "componentOwnershipUnambiguous": True,
            "currentReferenceHashesPinned": True,
            "exactPalettesRecorded": True,
            "contactSheetCoversEveryCandidate": True,
            "libraryVersionsAdded": True,
            "storiesChanged": False,
            "activityStoriesRuntimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
        "approval": {
            "by": "Frank",
            "date": "2026-10-21",
            "words": "approved",
            "scope": "the exact five-picture sandwich family contact sheet",
        },
        "rollback": "Set each picture's current selector back to V1; the approved V2 assets and all earlier bytes remain immutable and selectable.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built and verified {len(rows)} approved components in {SET}")


def verify() -> None:
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["set"] != SET or register["status"] != "approved-and-registered":
        raise RuntimeError("register identity/status mismatch")
    expected_ids = [str(spec["id"]) for spec in SPECS]
    if list(register["components"]) != expected_ids:
        raise RuntimeError("register component order/coverage mismatch")
    library = library_entries()
    for spec in SPECS:
        picture_id = str(spec["id"])
        entry = register["components"][picture_id]
        source_path = ROOT / entry["sourceFile"]
        output_path = ROOT / entry["file"]
        current_path = ROOT / entry["currentReferenceFile"]
        for path in (source_path, output_path, current_path):
            if not path.is_file():
                raise RuntimeError(f"missing manifest path: {path}")
        if sha256(source_path) != entry["sourceSha256"] or sha256(output_path) != entry["sha256"]:
            raise RuntimeError(f"candidate hash mismatch: {picture_id}")
        if sha256(current_path) != entry["currentReferenceSha256"]:
            raise RuntimeError(f"prior-current hash mismatch: {picture_id}")
        picture = library[picture_id]
        if picture["current"] != 2 or len(picture["versions"]) != 2:
            raise RuntimeError(f"approved candidate is not current V2: {picture_id}")
        prior = next((version for version in picture["versions"] if version["v"] == 1), None)
        current = next((version for version in picture["versions"] if version["v"] == 2), None)
        if prior is None or prior["sha256"] != entry["currentReferenceSha256"]:
            raise RuntimeError(f"library V1 hash drift: {picture_id}")
        if current is None or current["sha256"] != entry["sha256"]:
            raise RuntimeError(f"library V2 hash drift: {picture_id}")
        source = Image.open(source_path)
        output = Image.open(output_path)
        if source.mode != "RGBA" or output.mode != "RGBA" or output.size != (CELL, CELL):
            raise RuntimeError(f"mode/dimensions mismatch: {picture_id}")
        if edge_alpha_pixels(source) or edge_alpha_pixels(output):
            raise RuntimeError(f"edge alpha found: {picture_id}")
        output_box = visible_bounds(output)
        if list(output_box) != entry["bounds"]:
            raise RuntimeError(f"bounds mismatch: {picture_id}")
        gutter = min(output_box[0], output_box[1], CELL - output_box[2], CELL - output_box[3])
        if gutter != entry["transparentGutterPx"] or gutter < 20:
            raise RuntimeError(f"gutter mismatch: {picture_id}")
        allowed = {tuple(int(value[index:index + 2], 16) for index in (1, 3, 5)) for value in entry["flatPalette"]}
        actual = {pixel[:3] for pixel in output.get_flattened_data() if pixel[3] > VISIBLE_ALPHA}
        if not actual.issubset(allowed):
            raise RuntimeError(f"palette mismatch: {picture_id}")
        if entry["ownership"] != {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0}:
            raise RuntimeError(f"ownership mismatch: {picture_id}")
    evidence = register["evidence"]
    contact_path = ROOT / evidence["file"]
    if sha256(contact_path) != evidence["sha256"]:
        raise RuntimeError("contact sheet hash mismatch")
    contact = Image.open(contact_path)
    if contact.mode != "RGBA" or contact.size != (CELL * 5, HEADER + ROW_HEIGHT * len(expected_ids)):
        raise RuntimeError("contact sheet geometry mismatch")
    if evidence["coveredIds"] != expected_ids or evidence["rows"] != len(expected_ids) or evidence["columns"] != 5:
        raise RuntimeError("contact sheet coverage metadata mismatch")
    if not register["checks"]["libraryVersionsAdded"]:
        raise RuntimeError("approved pack does not record its registered versions")
    expected_hash_lines = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hash_lines:
        raise RuntimeError("HASHES.sha256 is stale or incomplete")
    print(f"Verified {SET}: {len(expected_ids)} approved V2 components, contact sheet and retained V1 priors")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="verify existing outputs without rebuilding")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
