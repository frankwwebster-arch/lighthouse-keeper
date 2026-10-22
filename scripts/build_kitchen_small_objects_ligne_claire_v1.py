#!/usr/bin/env python3
"""Build or verify the immutable mask-locked kitchen knives and mills review pack."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-small-objects-ligne-claire-v1"
PACK = ROOT / "art/drafts/kitchen-small-objects-ligne-claire-2026-10-22-v1"
CELL = (256, 256)

INK = (5, 24, 36, 255)
CREAM = (239, 233, 216, 255)
PALE_BLUE = (151, 202, 218, 255)
ORANGE = (232, 112, 36, 255)
GOLD = (231, 166, 56, 255)
BROWN = (166, 95, 42, 255)
DARK_BROWN = (111, 61, 37, 255)

SPECS = (
    {
        "id": "knife-chef",
        "label": "Chef's knife",
        "source": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/knife-chef.png",
        "sha256": "292543ab725d9cadd473539847e25c08ba9c867720af7b71888690293a6ccb20",
        "bounds": [20, 69, 236, 187],
        "kind": "knife",
        "blade": [(16, 188), (151, 91), (160, 126), (76, 174)],
        "bolster": [(147, 89), (158, 81), (169, 119), (158, 128)],
        "handle": [(155, 80), (225, 55), (244, 68), (241, 100), (169, 124)],
        "rivets": [(180, 94), (204, 84), (225, 74)],
    },
    {
        "id": "knife-bread",
        "label": "Bread knife",
        "source": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/knife-bread.png",
        "sha256": "ea7fe35cd1487d4c1ee22539dc1ceb2e7f65143298b89e84eb9c9625228bc4d6",
        "bounds": [20, 77, 236, 179],
        "kind": "knife",
        "blade": [(15, 180), (151, 94), (164, 126), (66, 166)],
        "bolster": [(148, 91), (158, 83), (169, 119), (159, 128)],
        "handle": [(156, 82), (226, 59), (244, 72), (239, 104), (168, 123)],
        "rivets": [(181, 95), (205, 86), (226, 77)],
    },
    {
        "id": "knife-paring",
        "label": "Paring knife",
        "source": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/knife-paring.png",
        "sha256": "7d69426fd494b75186b23b33e21b69e89fd83b0747af006af227d241bdb01fb1",
        "bounds": [20, 69, 236, 186],
        "kind": "knife",
        "blade": [(15, 188), (146, 98), (158, 127), (77, 174)],
        "bolster": [(143, 95), (154, 85), (166, 119), (157, 129)],
        "handle": [(152, 84), (224, 57), (244, 70), (241, 102), (164, 124)],
        "rivets": [(179, 97), (203, 87), (225, 76)],
    },
    {
        "id": "condiment-salt-mill",
        "label": "Salt mill",
        "source": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-salt-mill.png",
        "sha256": "a0eadd6a9f3b760191d69cafca84e83dca5e6b9e1d76aed6f09886ace93b3259",
        "bounds": [79, 20, 177, 236],
        "kind": "mill",
        "base": CREAM,
        "secondary": GOLD,
    },
    {
        "id": "condiment-pepper-mill",
        "label": "Pepper mill",
        "source": "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/assets/condiment-pepper-mill.png",
        "sha256": "762f50f6954bb69afbbdef0b41d43eef13c7d4dee0dfcb3910acf42fff1fad38",
        "bounds": [80, 20, 175, 236],
        "kind": "mill",
        "base": BROWN,
        "secondary": DARK_BROWN,
    },
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def alpha_bounds(image: Image.Image) -> list[int]:
    bounds = image.getchannel("A").getbbox()
    if not bounds:
        raise RuntimeError("empty alpha")
    return list(bounds)


def clipped_layer(size: tuple[int, int], mask: Image.Image, draw_fn) -> Image.Image:
    layer = Image.new("RGBA", size)
    draw_fn(ImageDraw.Draw(layer))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), mask))
    return layer


def outer_outline(alpha: Image.Image, width: int = 3) -> Image.Image:
    solid = alpha.point(lambda v: 255 if v else 0)
    eroded = solid.filter(ImageFilter.MinFilter(width * 2 + 1))
    return ImageChops.subtract(solid, eroded)


def draw_knife(source: Image.Image, spec: dict) -> Image.Image:
    alpha = source.getchannel("A")
    candidate = Image.new("RGBA", CELL, CREAM)
    candidate.putalpha(alpha)

    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon(spec["handle"], fill=ORANGE)))
    candidate.alpha_composite(clipped_layer(CELL, alpha, lambda d: d.polygon(spec["bolster"], fill=GOLD)))

    seam = Image.new("RGBA", CELL)
    draw = ImageDraw.Draw(seam)
    b = spec["bolster"]
    draw.line([b[0], b[3]], fill=INK, width=3)
    draw.line([b[1], b[2]], fill=INK, width=3)
    for x, y in spec["rivets"]:
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=GOLD, outline=INK, width=3)
    # Two restrained metal construction ticks; no reflection band.
    blade = spec["blade"]
    draw.line([(blade[0][0] + 39, blade[0][1] - 20), (blade[0][0] + 59, blade[0][1] - 34)], fill=PALE_BLUE, width=3)
    draw.line([(blade[0][0] + 75, blade[0][1] - 52), (blade[0][0] + 90, blade[0][1] - 63)], fill=PALE_BLUE, width=3)
    seam.putalpha(ImageChops.multiply(seam.getchannel("A"), alpha))
    candidate.alpha_composite(seam)

    outline = outer_outline(alpha)
    ink = Image.new("RGBA", CELL, INK)
    ink.putalpha(outline)
    candidate.alpha_composite(ink)
    candidate.putalpha(alpha)
    return candidate


def draw_mill(source: Image.Image, spec: dict) -> Image.Image:
    alpha = source.getchannel("A")
    base = spec["base"]
    secondary = spec["secondary"]
    candidate = Image.new("RGBA", CELL, base)
    candidate.putalpha(alpha)
    regions = Image.new("RGBA", CELL)
    d = ImageDraw.Draw(regions)
    # Real construction regions: top screw/knob, collar, waist and foot.
    d.rectangle((70, 20, 186, 48), fill=secondary)
    d.rectangle((70, 101, 186, 119), fill=GOLD)
    d.rectangle((70, 201, 186, 238), fill=secondary)
    if spec["id"].endswith("salt-mill"):
        d.rectangle((70, 122, 186, 199), fill=CREAM)
    regions.putalpha(ImageChops.multiply(regions.getchannel("A"), alpha))
    candidate.alpha_composite(regions)

    seams = Image.new("RGBA", CELL)
    d = ImageDraw.Draw(seams)
    for y, inset in ((48, 7), (103, 3), (117, 3), (201, 2), (218, 0)):
        d.arc((78 + inset, y - 7, 178 - inset, y + 7), 0, 180, fill=INK, width=3)
    d.line((101, 31, 155, 31), fill=INK, width=3)
    d.line((110, 69, 146, 69), fill=PALE_BLUE if spec["id"].endswith("salt-mill") else GOLD, width=3)
    seams.putalpha(ImageChops.multiply(seams.getchannel("A"), alpha))
    candidate.alpha_composite(seams)

    outline = outer_outline(alpha)
    ink = Image.new("RGBA", CELL, INK)
    ink.putalpha(outline)
    candidate.alpha_composite(ink)
    candidate.putalpha(alpha)
    return candidate


def checker(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", size, (238, 233, 211))
    d = ImageDraw.Draw(image)
    step = 16
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                d.rectangle((x, y, x + step - 1, y + step - 1), fill=(218, 211, 187))
    return image.convert("RGBA")


def build_sheet(records: list[dict], title: str = "Kitchen small objects V1 — current / candidate / 50% ghost / native 64 px") -> Image.Image:
    row_h = 292
    sheet = Image.new("RGB", (1100, 58 + row_h * len(records)), (7, 23, 30))
    d = ImageDraw.Draw(sheet)
    d.text((22, 18), title, fill=(240, 249, 246))
    for index, record in enumerate(records):
        y = 58 + index * row_h
        d.rectangle((0, y, 1100, y + row_h - 1), fill=(242, 237, 218))
        d.text((18, y + 12), record["label"], fill=(5, 24, 36))
        current = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        ghost = Image.blend(current, candidate, 0.5)
        for x, title, image in ((18, "CURRENT", current), (286, "CANDIDATE", candidate), (554, "50% GHOST", ghost)):
            d.text((x, y + 34), title, fill=(5, 24, 36))
            tile = checker(CELL)
            tile.alpha_composite(image)
            sheet.paste(tile.convert("RGB"), (x, y + 52))
        d.text((828, y + 34), "NATIVE 64 PX", fill=(5, 24, 36))
        native = candidate.resize((64, 64), Image.Resampling.LANCZOS)
        proof = checker((224, 224))
        proof.alpha_composite(native.resize((192, 192), Image.Resampling.NEAREST), (16, 16))
        sheet.paste(proof.convert("RGB"), (828, y + 52))
        d.text((828, y + 255), f"bounds {record['candidateBounds']} · alpha exact", fill=(45, 72, 75))
    return sheet


def build() -> None:
    if PACK.exists():
        raise RuntimeError("refusing to overwrite immutable kitchen small-objects V1")
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
        candidate = draw_knife(source, spec) if spec["kind"] == "knife" else draw_mill(source, spec)
        candidate_path = PACK / "candidates" / f"{spec['id']}.png"
        candidate.save(candidate_path, optimize=True)
        if candidate.getchannel("A").tobytes() != source.getchannel("A").tobytes():
            raise RuntimeError(f"alpha mismatch: {spec['id']}")
        records.append({
            "id": spec["id"], "label": spec["label"], "sourceFile": spec["source"],
            "sourceSha256": spec["sha256"], "candidateFile": rel(candidate_path),
            "candidateSha256": sha(candidate_path), "canvas": list(CELL),
            "sourceBounds": alpha_bounds(source), "candidateBounds": alpha_bounds(candidate),
            "alphaSha256": hashlib.sha256(source.getchannel("A").tobytes()).hexdigest(),
            "registration": {"anchor": "unchanged-current-library-anchor", "pivot": "unchanged", "footprint": "byte-exact-alpha"},
        })
    evidence = PACK / "evidence/current-candidate-ghost-64px.png"
    build_sheet(records).save(evidence, optimize=True)
    manifest = {
        "schema": "lighthouse-keeper/kitchen-small-objects-ligne-claire@1",
        "set": SET, "created": "2026-10-22",
        "status": "immutable-review-candidate-not-approved-not-registered",
        "visualAuthority": "sandwich-tomato V2; approved flat-glass condiment V2 family",
        "method": "mask-locked deterministic redraw after rejecting generated geometry/tonal drift",
        "objects": records,
        "rules": ["one even near-black line", "real edges only", "closed flat colours", "no shine or gradients", "accurate adult tool construction", "clear at 64 px", "black only for black material"],
        "unchanged": ["canvas", "alpha bytes", "transparent padding", "bounds", "orientation", "footprint", "anchors", "pivots", "identifiers", "library selection", "stories", "runtime"],
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True},
        "evidence": {"file": rel(evidence), "sha256": sha(evidence)},
        "rollback": "Discard only this V1 pack and review route; no current or production file was changed.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({"set": SET, "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "manifest": rel(PACK / "manifest.json"), "manifestSha256": sha(PACK / "manifest.json")}, indent=2) + "\n")

    verify()
    print(f"Built and verified {len(records)} mask-locked kitchen small-object candidates")


def verify() -> None:
    manifest_path = PACK / "manifest.json"
    register_path = PACK / "batch-register.json"
    if not manifest_path.is_file() or not register_path.is_file():
        raise RuntimeError("missing pack files")
    manifest = json.loads(manifest_path.read_text())
    register = json.loads(register_path.read_text())
    if manifest["set"] != SET or manifest["registration"] != {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True}:
        raise RuntimeError("registration gate changed")
    if register["status"] != "blocked-pending-explicit-frank-approval" or register["register"] or register["promote"]:
        raise RuntimeError("batch gate changed")
    if len(manifest["objects"]) != len(SPECS):
        raise RuntimeError("object coverage changed")
    for record, spec in zip(manifest["objects"], SPECS):
        source_path = ROOT / record["sourceFile"]
        candidate_path = ROOT / record["candidateFile"]
        if sha(source_path) != record["sourceSha256"] or sha(candidate_path) != record["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record['id']}")
        source = Image.open(source_path).convert("RGBA")
        candidate = Image.open(candidate_path).convert("RGBA")
        if source.size != candidate.size or source.size != CELL:
            raise RuntimeError(f"canvas drift: {record['id']}")
        if source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"alpha drift: {record['id']}")
        if alpha_bounds(candidate) != spec["bounds"]:
            raise RuntimeError(f"bounds drift: {record['id']}")
    print(f"Verified {SET}: {len(SPECS)} exact-alpha candidates; gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
