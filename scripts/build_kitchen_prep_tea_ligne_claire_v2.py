#!/usr/bin/env python3
"""Build or verify V2: separate milk vessels and the bread-slicing knife read."""

from __future__ import annotations

import argparse
import hashlib
import json

from PIL import Image, ImageChops, ImageDraw

from build_kitchen_prep_tea_ligne_claire_v1 import (
    BLUE,
    DARK_BLUE,
    DRAWERS as V1_DRAWERS,
    PACK as V1_PACK,
    RED,
    SPECS,
    finish,
    line_layer,
)
from build_kitchen_small_objects_ligne_claire_v1 import (
    CELL,
    CREAM,
    DARK_BROWN,
    GOLD,
    INK,
    ORANGE,
    PALE_BLUE,
    ROOT,
    alpha_bounds,
    build_sheet,
    clipped_layer,
    rel,
    sha,
)


SET = "kitchen-prep-tea-ligne-claire-v2"
PACK = ROOT / "art/drafts/kitchen-prep-tea-ligne-claire-2026-10-22-v2"


def draw_milk_v2(source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    candidate = Image.new("RGBA", CELL, CREAM); candidate.putalpha(alpha)
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.rectangle((15, 20, 132, 235), fill=PALE_BLUE)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(36, 83), (108, 83), (119, 213), (28, 213)], fill=CREAM)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.rectangle((112, 104, 239, 235), fill=CREAM)))
    candidate.alpha_composite(line_layer(alpha, lambda d: (
        d.ellipse((43, 24, 101, 47), outline=INK, width=3),
        d.line((31, 82, 109, 82), fill=INK, width=3),
        d.line([(108, 82), (113, 104), (118, 134), (118, 180), (109, 213)], fill=INK, width=3),
        d.arc((105, 103, 196, 137), 180, 360, fill=DARK_BLUE, width=4),
        d.arc((181, 121, 236, 190), 255, 105, fill=INK, width=3),
        d.line((52, 59, 45, 71), fill=PALE_BLUE, width=3),
        d.line((143, 148, 137, 162), fill=PALE_BLUE, width=3),
    )))
    return finish(candidate, source)


def draw_prep_v2(source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    candidate = Image.new("RGBA", CELL, GOLD); candidate.putalpha(alpha)
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.ellipse((48, 65, 184, 169), fill=ORANGE)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(20, 118), (58, 91), (133, 105), (161, 144), (109, 177), (45, 166)], fill=CREAM)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(53, 97), (159, 116), (170, 132), (64, 119)], fill=PALE_BLUE)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(158, 112), (226, 82), (242, 95), (231, 121), (169, 133)], fill=DARK_BROWN)))
    candidate.alpha_composite(line_layer(alpha, lambda d: (
        d.line([(55, 98), (158, 117), (168, 131), (64, 119), (55, 98)], fill=INK, width=3),
        d.line([(158, 112), (170, 132)], fill=INK, width=3),
        d.arc((66, 72, 121, 118), 205, 340, fill=CREAM, width=5),
        d.arc((91, 67, 146, 114), 205, 340, fill=CREAM, width=5),
        d.arc((118, 68, 171, 115), 205, 340, fill=CREAM, width=5),
        d.ellipse((191, 96, 198, 103), fill=GOLD, outline=INK, width=2),
        d.ellipse((213, 87, 220, 94), fill=GOLD, outline=INK, width=2),
    )))
    return finish(candidate, source)


DRAWERS = {**V1_DRAWERS, "milk": draw_milk_v2, "prep": draw_prep_v2}


def build() -> None:
    if PACK.exists():
        raise RuntimeError("refusing to overwrite immutable kitchen prep/tea V2")
    (PACK / "candidates").mkdir(parents=True)
    (PACK / "evidence").mkdir(parents=True)
    v1 = json.loads((V1_PACK / "manifest.json").read_text())
    records = []
    for spec in SPECS:
        source_path = ROOT / spec["source"]
        if sha(source_path) != spec["sha256"]:
            raise RuntimeError(f"source drift: {spec['id']}")
        source = Image.open(source_path).convert("RGBA")
        candidate = DRAWERS[spec["kind"]](source)
        candidate_path = PACK / "candidates" / f"{spec['id']}.png"
        candidate.save(candidate_path, optimize=True)
        v1_record = next(item for item in v1["objects"] if item["id"] == spec["id"])
        if spec["id"] not in ("tea-milk", "prep-bread-slicing") and candidate_path.read_bytes() != (ROOT / v1_record["candidateFile"]).read_bytes():
            raise RuntimeError(f"unchanged V1 candidate drift: {spec['id']}")
        if source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"alpha mismatch: {spec['id']}")
        records.append({
            "id": spec["id"], "label": spec["label"], "sourceFile": spec["source"], "sourceSha256": spec["sha256"],
            "candidateFile": rel(candidate_path), "candidateSha256": sha(candidate_path), "canvas": list(CELL),
            "sourceBounds": alpha_bounds(source), "candidateBounds": alpha_bounds(candidate),
            "alphaSha256": hashlib.sha256(source.getchannel("A").tobytes()).hexdigest(),
            "v1CandidateSha256": v1_record["candidateSha256"],
            "v2Change": "interior separation only" if spec["id"] in ("tea-milk", "prep-bread-slicing") else "byte-identical V1 carry-forward",
            "registration": {"anchor": "unchanged-current-library-anchor", "pivot": "unchanged", "footprint": "byte-exact-alpha"},
        })
    evidence = PACK / "evidence/current-candidate-ghost-64px.png"
    build_sheet(records, "Kitchen prep + tea V2 — vessel/knife separation corrected; geometry exact").save(evidence, optimize=True)
    manifest = {
        "schema": "lighthouse-keeper/kitchen-prep-tea-ligne-claire@2", "set": SET, "created": "2026-10-22",
        "status": "immutable-review-candidate-not-approved-not-registered", "supersedesReviewOnly": "kitchen-prep-tea-ligne-claire-v1",
        "v1Failure": "milk bottle and jug merged visually; bread-slicing knife handle did not separate from loaf at 64 px",
        "visualAuthority": "sandwich-tomato V2; approved flat-glass condiment V2 family",
        "method": "mask-locked deterministic redraw; V2 changes only two interior real-edge/material assignments",
        "objects": records,
        "unchanged": ["canvas", "alpha bytes", "transparent padding", "bounds", "orientation", "footprint", "anchors", "pivots", "identifiers", "library selection", "stories", "runtime"],
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True},
        "evidence": {"file": rel(evidence), "sha256": sha(evidence)},
        "rollback": "Discard only this V2 pack and review route; V1 and every current/production file remain untouched.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({"set": SET, "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "manifest": rel(PACK / "manifest.json"), "manifestSha256": sha(PACK / "manifest.json")}, indent=2) + "\n")
    verify()
    print(f"Built and verified {len(records)} corrected kitchen prep/tea candidates")


def verify() -> None:
    manifest_path = PACK / "manifest.json"; register_path = PACK / "batch-register.json"
    if not manifest_path.is_file() or not register_path.is_file():
        raise RuntimeError("missing V2 pack files")
    manifest = json.loads(manifest_path.read_text()); register = json.loads(register_path.read_text())
    if manifest["set"] != SET or manifest["registration"]["register"] or manifest["registration"]["promote"]:
        raise RuntimeError("registration gate changed")
    if register["status"] != "blocked-pending-explicit-frank-approval" or register["register"] or register["promote"]:
        raise RuntimeError("batch gate changed")
    v1 = json.loads((V1_PACK / "manifest.json").read_text())
    for record, spec in zip(manifest["objects"], SPECS):
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA"); candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        if sha(ROOT / record["sourceFile"]) != record["sourceSha256"] or sha(ROOT / record["candidateFile"]) != record["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record['id']}")
        if source.size != candidate.size or source.size != CELL or source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"geometry/alpha drift: {record['id']}")
        if alpha_bounds(candidate) != spec["bounds"]:
            raise RuntimeError(f"bounds drift: {record['id']}")
        v1_record = next(item for item in v1["objects"] if item["id"] == record["id"])
        if record["id"] not in ("tea-milk", "prep-bread-slicing") and record["candidateSha256"] != v1_record["candidateSha256"]:
            raise RuntimeError(f"V1 carry-forward drift: {record['id']}")
    print(f"Verified {SET}: {len(SPECS)} exact-alpha candidates; two bounded interior corrections; gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--verify", action="store_true"); args = parser.parse_args()
    verify() if args.verify else build()
