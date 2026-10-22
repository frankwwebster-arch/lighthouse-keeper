#!/usr/bin/env python3
"""Build or verify the immutable mask-locked kitchen tea and preparation review pack."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from build_kitchen_small_objects_ligne_claire_v1 import (
    BROWN,
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
    outer_outline,
    rel,
    sha,
)


SET = "kitchen-prep-tea-ligne-claire-v1"
PACK = ROOT / "art/drafts/kitchen-prep-tea-ligne-claire-2026-10-22-v1"
BLUE = (24, 112, 166, 255)
DARK_BLUE = (13, 78, 117, 255)
RED = (232, 72, 51, 255)
WHITE = (248, 246, 235, 255)

SPECS = (
    {
        "id": "tea-kettle", "label": "Tea kettle",
        "source": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/tea-kettle.png",
        "sha256": "7014b90c1465cbf0b1b9559f57be78a4a36c354ba13033c9639aa048253dd7cf",
        "bounds": [20, 24, 236, 232], "kind": "kettle",
    },
    {
        "id": "tea-milk", "label": "Milk bottle and jug",
        "source": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/tea-milk.png",
        "sha256": "01eb45bb370455c770702cc7cb25334fccc3d2a6d3cc0cf376733da2f9dfeadc",
        "bounds": [20, 25, 236, 230], "kind": "milk",
    },
    {
        "id": "tea-mug", "label": "Mug of tea",
        "source": "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3/drafts/callouts/tea-mug.png",
        "sha256": "af8fb40591e8165cfb4ec8f9f30be0df24abd733cc412d086c3920a37242bff3",
        "bounds": [20, 38, 236, 218], "kind": "mug",
    },
    {
        "id": "toast-slices", "label": "Toast slices",
        "source": "art/drafts/activity-cloud-composer-2026-10-19-v5/drafts/components/toast-slices.png",
        "sha256": "4a1344273465976f1c69b858e1ada925a69432242450c2838c68d9fe63e25a27",
        "bounds": [25, 20, 230, 236], "kind": "toast",
    },
    {
        "id": "prep-bread-slicing", "label": "Bread slicing preparation",
        "source": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/prep-bread-slicing.png",
        "sha256": "d665a9df3462d9543137b9134610181d84081cff0311d2b17293985a0a5234fb",
        "bounds": [20, 65, 236, 190], "kind": "prep",
    },
)


def finish(candidate: Image.Image, source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    outline = outer_outline(alpha)
    ink = Image.new("RGBA", CELL, INK)
    ink.putalpha(outline)
    candidate.alpha_composite(ink)
    candidate.putalpha(alpha)
    return candidate


def line_layer(alpha: Image.Image, painter) -> Image.Image:
    layer = Image.new("RGBA", CELL)
    painter(ImageDraw.Draw(layer))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), alpha))
    return layer


def draw_kettle(source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    candidate = Image.new("RGBA", CELL, CREAM); candidate.putalpha(alpha)
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.rectangle((15, 197, 240, 235), fill=DARK_BLUE)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(177, 111), (225, 91), (242, 112), (207, 157), (179, 146)], fill=ORANGE)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.ellipse((96, 92, 165, 124), fill=GOLD)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.arc((43, 35, 203, 164), 184, 356, fill=DARK_BLUE, width=27)))
    candidate.alpha_composite(line_layer(alpha, lambda d: (
        d.arc((91, 100, 169, 130), 178, 360, fill=INK, width=3),
        d.line((57, 203, 200, 203), fill=INK, width=3),
        d.line((189, 121, 219, 108), fill=INK, width=3),
        d.line((195, 67, 206, 78), fill=PALE_BLUE, width=3),
        d.line((211, 42, 222, 55), fill=PALE_BLUE, width=3),
    )))
    return finish(candidate, source)


def draw_milk(source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    candidate = Image.new("RGBA", CELL, CREAM); candidate.putalpha(alpha)
    # Bottle glass and neck remain visually quiet; milk is a single cream plane.
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.rectangle((15, 20, 132, 235), fill=PALE_BLUE)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(36, 83), (108, 83), (119, 213), (28, 213)], fill=CREAM)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.rectangle((112, 104, 239, 235), fill=CREAM)))
    candidate.alpha_composite(line_layer(alpha, lambda d: (
        d.ellipse((43, 24, 101, 47), outline=INK, width=3),
        d.line((31, 82, 109, 82), fill=INK, width=3),
        d.arc((105, 103, 196, 137), 180, 360, fill=DARK_BLUE, width=4),
        d.arc((181, 121, 236, 190), 255, 105, fill=INK, width=3),
        d.line((52, 59, 45, 71), fill=PALE_BLUE, width=3),
        d.line((143, 148, 137, 162), fill=PALE_BLUE, width=3),
    )))
    return finish(candidate, source)


def draw_mug(source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    candidate = Image.new("RGBA", CELL, CREAM); candidate.putalpha(alpha)
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.ellipse((65, 43, 226, 92), fill=ORANGE)))
    candidate.alpha_composite(line_layer(alpha, lambda d: (
        d.ellipse((62, 38, 228, 91), outline=DARK_BLUE, width=7),
        d.arc((20, 80, 99, 166), 75, 285, fill=INK, width=3),
        d.line((101, 112, 101, 188), fill=PALE_BLUE, width=3),
    )))
    return finish(candidate, source)


def draw_toast(source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    candidate = Image.new("RGBA", CELL, GOLD); candidate.putalpha(alpha)
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(45, 61), (83, 25), (142, 22), (169, 68), (149, 143), (79, 157)], fill=CREAM)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(89, 105), (140, 65), (207, 74), (232, 123), (202, 200), (131, 207)], fill=CREAM)))
    candidate.alpha_composite(line_layer(alpha, lambda d: (
        d.line([(47, 64), (82, 30), (141, 27), (165, 69)], fill=INK, width=3),
        d.line([(91, 108), (140, 70), (205, 78), (226, 123)], fill=INK, width=3),
        d.arc((74, 51, 151, 122), 205, 345, fill=ORANGE, width=4),
        d.arc((124, 101, 212, 181), 205, 345, fill=ORANGE, width=4),
    )))
    return finish(candidate, source)


def draw_prep(source: Image.Image) -> Image.Image:
    alpha = source.getchannel("A")
    candidate = Image.new("RGBA", CELL, GOLD); candidate.putalpha(alpha)
    # Loaf, cut slice and knife remain the exact current compound silhouette.
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.ellipse((48, 65, 184, 169), fill=ORANGE)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(20, 118), (58, 91), (133, 105), (161, 144), (109, 177), (45, 166)], fill=CREAM)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(53, 97), (159, 116), (170, 132), (64, 119)], fill=CREAM)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon([(158, 112), (226, 82), (242, 95), (231, 121), (169, 133)], fill=ORANGE)))
    candidate.alpha_composite(line_layer(alpha, lambda d: (
        d.line([(55, 98), (158, 117), (168, 131)], fill=INK, width=3),
        d.line([(158, 112), (170, 132)], fill=INK, width=3),
        d.arc((66, 72, 121, 118), 205, 340, fill=CREAM, width=5),
        d.arc((91, 67, 146, 114), 205, 340, fill=CREAM, width=5),
        d.arc((118, 68, 171, 115), 205, 340, fill=CREAM, width=5),
        d.ellipse((191, 96, 198, 103), fill=GOLD, outline=INK, width=2),
        d.ellipse((213, 87, 220, 94), fill=GOLD, outline=INK, width=2),
    )))
    return finish(candidate, source)


DRAWERS = {"kettle": draw_kettle, "milk": draw_milk, "mug": draw_mug, "toast": draw_toast, "prep": draw_prep}


def build() -> None:
    if PACK.exists():
        raise RuntimeError("refusing to overwrite immutable kitchen prep/tea V1")
    (PACK / "candidates").mkdir(parents=True)
    (PACK / "evidence").mkdir(parents=True)
    records = []
    for spec in SPECS:
        source_path = ROOT / spec["source"]
        if sha(source_path) != spec["sha256"]:
            raise RuntimeError(f"source drift: {spec['id']}")
        source = Image.open(source_path).convert("RGBA")
        if source.size != CELL or alpha_bounds(source) != spec["bounds"]:
            raise RuntimeError(f"source geometry drift: {spec['id']}")
        candidate = DRAWERS[spec["kind"]](source)
        candidate_path = PACK / "candidates" / f"{spec['id']}.png"
        candidate.save(candidate_path, optimize=True)
        if candidate.getchannel("A").tobytes() != source.getchannel("A").tobytes():
            raise RuntimeError(f"alpha mismatch: {spec['id']}")
        records.append({
            "id": spec["id"], "label": spec["label"], "sourceFile": spec["source"], "sourceSha256": spec["sha256"],
            "candidateFile": rel(candidate_path), "candidateSha256": sha(candidate_path), "canvas": list(CELL),
            "sourceBounds": alpha_bounds(source), "candidateBounds": alpha_bounds(candidate),
            "alphaSha256": hashlib.sha256(source.getchannel("A").tobytes()).hexdigest(),
            "registration": {"anchor": "unchanged-current-library-anchor", "pivot": "unchanged", "footprint": "byte-exact-alpha"},
        })
    evidence = PACK / "evidence/current-candidate-ghost-64px.png"
    build_sheet(records, "Kitchen prep + tea V1 — current / candidate / 50% ghost / native 64 px").save(evidence, optimize=True)
    manifest = {
        "schema": "lighthouse-keeper/kitchen-prep-tea-ligne-claire@1", "set": SET, "created": "2026-10-22",
        "status": "immutable-review-candidate-not-approved-not-registered",
        "visualAuthority": "sandwich-tomato V2; approved flat-glass condiment V2 family",
        "method": "mask-locked deterministic redraw after rejecting generated geometry/tonal drift",
        "objects": records,
        "rules": ["one even near-black line", "real edges only", "closed flat colours", "no shine or gradients", "accurate adult object construction", "clear at 64 px", "black only for black material"],
        "unchanged": ["canvas", "alpha bytes", "transparent padding", "bounds", "orientation", "footprint", "anchors", "pivots", "identifiers", "library selection", "stories", "runtime"],
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True},
        "evidence": {"file": rel(evidence), "sha256": sha(evidence)},
        "rollback": "Discard only this V1 pack and review route; no current or production file was changed.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({"set": SET, "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "manifest": rel(PACK / "manifest.json"), "manifestSha256": sha(PACK / "manifest.json")}, indent=2) + "\n")
    verify()
    print(f"Built and verified {len(records)} mask-locked kitchen prep/tea candidates")


def verify() -> None:
    manifest_path = PACK / "manifest.json"; register_path = PACK / "batch-register.json"
    if not manifest_path.is_file() or not register_path.is_file():
        raise RuntimeError("missing pack files")
    manifest = json.loads(manifest_path.read_text()); register = json.loads(register_path.read_text())
    if manifest["set"] != SET or manifest["registration"]["register"] or manifest["registration"]["promote"]:
        raise RuntimeError("registration gate changed")
    if register["status"] != "blocked-pending-explicit-frank-approval" or register["register"] or register["promote"]:
        raise RuntimeError("batch gate changed")
    if len(manifest["objects"]) != len(SPECS):
        raise RuntimeError("object coverage changed")
    for record, spec in zip(manifest["objects"], SPECS):
        source_path = ROOT / record["sourceFile"]; candidate_path = ROOT / record["candidateFile"]
        if sha(source_path) != record["sourceSha256"] or sha(candidate_path) != record["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record['id']}")
        source = Image.open(source_path).convert("RGBA"); candidate = Image.open(candidate_path).convert("RGBA")
        if source.size != candidate.size or source.size != CELL or source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"geometry/alpha drift: {record['id']}")
        if alpha_bounds(candidate) != spec["bounds"]:
            raise RuntimeError(f"bounds drift: {record['id']}")
    print(f"Verified {SET}: {len(SPECS)} exact-alpha candidates; gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--verify", action="store_true"); args = parser.parse_args()
    verify() if args.verify else build()
