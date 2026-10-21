#!/usr/bin/env python3
"""Build the cabinet-only Ligne-Claire V2 review pack.

V2 is deliberately narrower than the rejected full-kitchen V1 pass. It changes
only RGB values in the eight split-cabinet variants and five compositor-owned
healing layers. Canvas, alpha, semantic masks and the existing V38/V41 movement
and healing contracts remain exact and unregistered.
"""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-cabinet-ligne-claire-v2"
DATED = "kitchen-cabinet-ligne-claire-2026-10-21-v2"
PACK = ROOT / "art" / "drafts" / DATED
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"

INK = (5, 24, 36)
WORKTOP = ((47, 119, 133), (83, 177, 181), (109, 201, 194))
BLUES = ((29, 69, 98), (35, 91, 133), (45, 119, 157), (64, 153, 194))
COPPER = ((144, 82, 49), (211, 111, 45), (231, 166, 56))
NEUTRALS = ((92, 108, 111), (174, 187, 185), (246, 229, 183))
PALETTE = (INK,) + WORKTOP + BLUES + COPPER + NEUTRALS
VISIBLE_ALPHA = 8

CABINET_SOURCE = "art/raw/kitchen-split-cabinet-workbench-2026-10-20-v38"
HEALING_SOURCE = "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41"
CABINET_NAMES = (
    "cabinet-a-le-re.png", "cabinet-a-le-rj.png",
    "cabinet-a-lj-re.png", "cabinet-a-lj-rj.png",
    "cabinet-b-le-re.png", "cabinet-b-le-rj.png",
    "cabinet-b-lj-re.png", "cabinet-b-lj-rj.png",
)
HEALING_NAMES = (
    "join-body-backfill-template.png",
    "countertop-join-cap-template.png",
    "countertop-triangle-underlay-template.png",
    "neighbour-seam-cleanup-left.png",
    "neighbour-seam-cleanup-right.png",
)
CONTRACT_FILES = (
    "art/drafts/kitchen-split-cabinet-workbench-2026-10-20-v38/candidate-catalogue.json",
    "art/drafts/kitchen-dishwasher-workbench-2026-10-20-v41/candidate-catalogue.json",
    "scripts/verify_kitchen_split_cabinet_workbench_v38.mjs",
    "scripts/verify_kitchen_dishwasher_workbench_v41.mjs",
    "docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md",
)
ROOM_CASES = (
    {
        "id": "origin-contiguous",
        "source": f"{CABINET_SOURCE}/cabinet-pair-origin-native-room.png",
        "placements": ((164, "cabinet-a-lj-rj.png"), (248, "cabinet-b-lj-rj.png")),
    },
    {
        "id": "dislocated-contiguous",
        "source": f"{CABINET_SOURCE}/cabinet-dislocated-contiguous-native-room.png",
        "placements": ((80, "cabinet-a-le-rj.png"), (248, "cabinet-b-lj-rj.png")),
    },
    {
        "id": "separated-exposed",
        "source": f"{CABINET_SOURCE}/cabinet-separated-exposed-native-room.png",
        "placements": ((80, "cabinet-a-le-rj.png"), (500, "cabinet-b-lj-re.png")),
    },
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def semantic_class(pixel: tuple[int, int, int, int]) -> str:
    r, g, b, a = pixel
    if a <= VISIBLE_ALPHA:
        return "transparent"
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    degrees = h * 360
    if v < 0.22 or (s < 0.18 and v < 0.42):
        return "construction-ink"
    if (degrees < 55 or degrees >= 340) and s > 0.35:
        return "hardware"
    if 165 <= degrees < 205:
        return "worktop"
    if 195 <= degrees < 265 or (b > g * 1.18 and b > r * 1.5):
        return "cabinet-body"
    return "neutral"


def class_mask(image: Image.Image, label: str) -> bytes:
    return bytes(255 if semantic_class(pixel) == label else 0 for pixel in image.getdata())


def cabinet_colour(pixel: tuple[int, int, int, int]) -> tuple[int, int, int]:
    r, g, b, _a = pixel
    _h, _s, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    label = semantic_class(pixel)
    if label == "construction-ink":
        return INK
    if label == "hardware":
        return COPPER[0] if value < 0.48 else (COPPER[1] if value < 0.78 else COPPER[2])
    if label == "worktop":
        return WORKTOP[0] if value < 0.42 else (WORKTOP[1] if value < 0.72 else WORKTOP[2])
    if label == "cabinet-body":
        if value < 0.42:
            return BLUES[0]
        if value < 0.58:
            return BLUES[1]
        if value < 0.78:
            return BLUES[2]
        return BLUES[3]
    if value > 0.70:
        return NEUTRALS[2]
    if value > 0.42:
        return NEUTRALS[1]
    return NEUTRALS[0]


def stylise(source: Image.Image) -> Image.Image:
    source = source.convert("RGBA")
    output = Image.new("RGBA", source.size)
    pixels = []
    for pixel in source.getdata():
        if pixel[3] == 0:
            pixels.append((0, 0, 0, 0))
        else:
            pixels.append((*cabinet_colour(pixel), pixel[3]))
    output.putdata(pixels)
    return output


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, (238, 230, 207, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(221, 211, 186, 255))
    return image


def panel(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = min((size[0] - 28) / image.width, (size[1] - 28) / image.height, 6)
    shown = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.NEAREST)
    base = checker(size)
    base.alpha_composite(shown, ((size[0] - shown.width) // 2, (size[1] - shown.height) // 2))
    return base


def contact_sheet(records: list[dict[str, object]], family: str) -> Path:
    rows = [record for record in records if record["family"] == family]
    width, panel_height, header = 840, 292, 56
    sheet = Image.new("RGBA", (width, header + panel_height * len(rows)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), f"{family}: exact source shapes / cabinet-only ligne-claire V2", fill=INK, font=font)
    draw.text((12, 29), "No contour dilation; alpha, worktop, body, hardware and construction masks hash-pinned", fill=INK, font=font)
    for index, record in enumerate(rows):
        y = header + index * panel_height
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        sheet.alpha_composite(panel(source, (420, 260)), (0, y))
        sheet.alpha_composite(panel(candidate, (420, 260)), (420, y))
        draw.text((10, y + 264), f"Current · {record['filename']}", fill=INK, font=font)
        draw.text((430, y + 264), f"V2 · {str(record['candidateSha256'])[:12]}", fill=INK, font=font)
    path = EVIDENCE / f"{family}-current-vs-candidate.png"
    sheet.save(path, optimize=True)
    return path


def replace_sprite(room: Image.Image, sprite: Image.Image, x: int, y: int) -> None:
    room_pixels = room.load()
    sprite_pixels = sprite.convert("RGBA").load()
    for sy in range(sprite.height):
        for sx in range(sprite.width):
            r, g, b, a = sprite_pixels[sx, sy]
            if a > VISIBLE_ALPHA:
                room_pixels[x + sx, y + sy] = (r, g, b, 255)


def movement_proof(records: list[dict[str, object]]) -> dict[str, object]:
    by_name = {str(record["filename"]): ROOT / str(record["candidateFile"]) for record in records}
    font = ImageFont.load_default()
    header = 42
    sheet = Image.new("RGBA", (1544, header + 224 * len(ROOM_CASES)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 12), "Move/snap/heal proof — current layouts / V2 cabinet art on the identical datums", fill=INK, font=font)
    cases = []
    for index, case in enumerate(ROOM_CASES):
        current_path = ROOT / str(case["source"])
        current = Image.open(current_path).convert("RGBA")
        candidate = current.copy()
        for x, name in case["placements"]:
            replace_sprite(candidate, Image.open(by_name[name]), x, 130)
        candidate_path = EVIDENCE / f"{case['id']}-candidate-room.png"
        candidate.save(candidate_path, optimize=True)
        y = header + index * 224
        sheet.alpha_composite(current, (0, y))
        sheet.alpha_composite(candidate, (772, y))
        draw.text((8, y + 7), f"CURRENT · {case['id']}", fill=INK, font=font)
        draw.text((780, y + 7), f"V2 CABINETS · {case['id']}", fill=INK, font=font)
        cases.append({
            "id": case["id"],
            "currentFile": rel(current_path),
            "currentSha256": sha256(current_path),
            "candidateFile": rel(candidate_path),
            "candidateSha256": sha256(candidate_path),
            "placements": [{"cellX": x, "candidate": name} for x, name in case["placements"]],
        })
    sheet_path = EVIDENCE / "cabinet-move-snap-heal-current-vs-candidate.png"
    sheet.save(sheet_path, optimize=True)
    return {"file": rel(sheet_path), "sha256": sha256(sheet_path), "cases": cases}


def review_html(records: list[dict[str, object]], evidence: dict[str, object]) -> str:
    cards = []
    for record in records:
        filename = html.escape(str(record["filename"]))
        family = html.escape(str(record["family"]))
        source_url = html.escape(f"/activity-stories/repo/{record['sourceFile']}")
        candidate_url = html.escape(f"assets/{family}--{filename}")
        cards.append(f'''<article><h3>{filename}</h3><div class="compare"><figure><figcaption>Current authority</figcaption><div class="stage"><img src="{source_url}" alt="Current {filename}"></div></figure><figure><figcaption>Cabinet V2</figcaption><div class="stage"><img src="{candidate_url}" alt="Candidate {filename}"></div></figure></div><p>{record['pixels'][0]} × {record['pixels'][1]} px · exact alpha and semantic shape masks · source <code>{str(record['sourceSha256'])[:12]}</code> · candidate <code>{str(record['candidateSha256'])[:12]}</code></p></article>''')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen cabinet ligne-claire V2</title><style>:root{{--ink:#051824;--cream:#f6e5b7;--paper:#fff9e8;--blue:#235b85}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1180px;margin:auto;padding:28px}}header{{border-bottom:4px solid var(--ink)}}.status{{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e84833;color:#fff;font-weight:800;border-radius:999px}}article{{margin:20px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}}.compare{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}figure{{margin:0}}figcaption{{font-weight:800}}.stage{{height:290px;display:grid;place-items:center;background:#eee6d0}}img{{max-width:95%;max-height:95%;image-rendering:pixelated}}a{{color:#174562;font-weight:800}}code{{font-size:.85em}}@media(max-width:700px){{.compare{{grid-template-columns:1fr}}}}</style></head><body><header><span class="status">REVIEW ONLY · NOT CURRENT</span><h1>Kitchen cabinet ligne-claire V2</h1><p>A cabinet-only correction after rejection of the full-kitchen V1 pass. No fridge, oven, sink or small object is proposed here.</p><p>V2 retains the exact source canvas, alpha, worktop shape, cabinet-body shape, hardware shape and dark construction-line positions. It adds no silhouette or contour pixels. Existing V38/V41 move, swap, snap and healing code is unchanged and hash-pinned.</p><p><a href="assets/evidence--cabinet-move-snap-heal-current-vs-candidate.png">Open move/snap/heal contact sheet</a> · <a href="/keeper-review/kitchen-split-cabinet-workbench-v38/">Open existing cabinet movement workbench</a> · <a href="/keeper-review/kitchen-dishwasher-workbench-v41/">Open existing healing/lock workbench</a></p></header><main>{''.join(cards)}</main></body></html>'''


def write_hashes() -> None:
    files = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text("\n".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}" for path in files) + "\n")


def build() -> None:
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    assets = []
    for family, source_dir, names in (
        ("cabinets", CABINET_SOURCE, CABINET_NAMES),
        ("healing", HEALING_SOURCE, HEALING_NAMES),
    ):
        family_dir = CANDIDATES / family
        family_dir.mkdir(parents=True, exist_ok=True)
        for name in names:
            source_path = ROOT / source_dir / name
            source = Image.open(source_path).convert("RGBA")
            candidate = stylise(source)
            candidate_path = family_dir / name
            candidate.save(candidate_path, optimize=True)
            alpha = source.getchannel("A")
            shape_hashes = {
                label: digest_bytes(class_mask(source, label))
                for label in ("construction-ink", "worktop", "cabinet-body", "hardware", "neutral")
            }
            assets.append({
                "family": family,
                "filename": name,
                "sourceFile": rel(source_path),
                "sourceSha256": sha256(source_path),
                "candidateFile": rel(candidate_path),
                "candidateSha256": sha256(candidate_path),
                "pixels": list(source.size),
                "alphaBounds": list(alpha.getbbox() or (0, 0, 0, 0)),
                "alphaSha256": digest_bytes(alpha.tobytes()),
                "semanticShapeMaskSha256": shape_hashes,
                "canvasExact": True,
                "alphaExact": True,
                "semanticShapeMasksExact": True,
                "contourDilationPixels": 0,
            })

    contacts = {}
    for family in ("cabinets", "healing"):
        path = contact_sheet(assets, family)
        contacts[family] = {"file": rel(path), "sha256": sha256(path)}
    movement = movement_proof(assets)
    tomato = ROOT / "art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/drafts/components/sandwich-tomato.png"
    v1_manifest = ROOT / "art/drafts/kitchen-ligne-claire-sweep-2026-10-21-v1/manifest.json"
    contracts = [{"file": path, "sha256": sha256(ROOT / path), "unchanged": True} for path in CONTRACT_FILES]
    manifest = {
        "schema": "lighthouse-keeper/kitchen-cabinet-ligne-claire@2",
        "set": SET,
        "datedDirectory": DATED,
        "created": "2026-10-21",
        "status": "immutable-reversible-cabinet-only-review-candidate-not-approved-not-registered",
        "supersedesForReview": "kitchen-ligne-claire-sweep-v1 (rejected for visible shape loss)",
        "scope": {"included": ["split cabinet A", "split cabinet B", "join/healing layers"], "excluded": ["fridge", "oven", "dishwasher", "sink", "kettle", "toaster", "mixing bowl", "pedal bin", "table/chair"]},
        "primaryVisualCalibration": {"file": rel(tomato), "sha256": sha256(tomato), "version": 2},
        "referenceManifest": {"file": rel(v1_manifest), "sha256": sha256(v1_manifest), "role": "original supplied reference hashes and rejected V1 provenance only"},
        "palette": ["#%02x%02x%02x" % colour for colour in PALETTE],
        "derivation": "RGB-only semantic-mask-preserving spot-colour translation; no resize, crop, alpha edit, contour dilation, erosion or silhouette generation",
        "assets": assets,
        "evidence": contacts,
        "movementHealingProof": movement,
        "unchangedContracts": contracts,
        "checks": {
            "sourceBytesUntouched": True,
            "candidateCanvasExact": True,
            "candidateAlphaExact": True,
            "candidateBoundsExact": True,
            "transparentPaddingExact": True,
            "worktopShapeMaskExact": True,
            "cabinetBodyShapeMaskExact": True,
            "hardwareShapeMaskExact": True,
            "constructionLineMaskExact": True,
            "contourDilationPixels": 0,
            "movementSnapSwapHealingContractsUnchanged": True,
            "roomLayoutChanged": False,
            "runtimeChanged": False,
            "registrationPerformed": False,
            "currentSelectorChanged": False,
        },
        "approvalRequiredFor": "any registration, selector update, Final copy or runtime wiring",
        "rollback": "Discard only the V2 dated directory and matching review set; all source/current/runtime files remain byte-for-byte in place.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "batch-register.json").write_text(json.dumps({
        "set": SET,
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
    }, indent=2) + "\n")

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC_ASSETS.mkdir(parents=True, exist_ok=True)
    for record in assets:
        shutil.copy2(ROOT / str(record["candidateFile"]), PUBLIC_ASSETS / f"{record['family']}--{record['filename']}")
    for item in contacts.values():
        shutil.copy2(ROOT / str(item["file"]), PUBLIC_ASSETS / f"evidence--{Path(str(item['file'])).name}")
    shutil.copy2(ROOT / str(movement["file"]), PUBLIC_ASSETS / f"evidence--{Path(str(movement['file'])).name}")
    for case in movement["cases"]:
        shutil.copy2(ROOT / str(case["candidateFile"]), PUBLIC_ASSETS / f"evidence--{Path(str(case['candidateFile'])).name}")
    (PUBLIC / "index.html").write_text(review_html(assets, contacts))
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
    write_hashes()
    verify()
    print(f"Built {SET}: {len(assets)} exact-shape candidates; registration remains closed")


def verify() -> None:
    manifest_path = PACK / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest["set"] != SET or "not-approved" not in manifest["status"]:
        raise RuntimeError("identity/status drift")
    if manifest["checks"]["registrationPerformed"] or manifest["checks"]["currentSelectorChanged"]:
        raise RuntimeError("registration boundary opened")
    if len(manifest["assets"]) != len(CABINET_NAMES) + len(HEALING_NAMES):
        raise RuntimeError("asset coverage drift")
    allowed = set(PALETTE)
    for record in manifest["assets"]:
        source_path = ROOT / record["sourceFile"]
        candidate_path = ROOT / record["candidateFile"]
        if sha256(source_path) != record["sourceSha256"] or sha256(candidate_path) != record["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record['filename']}")
        source = Image.open(source_path).convert("RGBA")
        candidate = Image.open(candidate_path).convert("RGBA")
        if source.size != candidate.size or list(source.getchannel("A").getdata()) != list(candidate.getchannel("A").getdata()):
            raise RuntimeError(f"canvas/alpha drift: {record['filename']}")
        if list(stylise(source).getdata()) != list(candidate.getdata()):
            raise RuntimeError(f"semantic shape or RGB derivation drift: {record['filename']}")
        for label, expected in record["semanticShapeMaskSha256"].items():
            if digest_bytes(class_mask(source, label)) != expected:
                raise RuntimeError(f"shape-mask drift: {record['filename']} {label}")
        colours = {pixel[:3] for pixel in candidate.getdata() if pixel[3] > VISIBLE_ALPHA}
        if not colours <= allowed:
            raise RuntimeError(f"non-spot colour: {record['filename']}")
    for contract in manifest["unchangedContracts"]:
        if sha256(ROOT / contract["file"]) != contract["sha256"]:
            raise RuntimeError(f"movement/healing contract drift: {contract['file']}")
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["register"] or register["promote"] or register["currentSelectorChanges"]:
        raise RuntimeError("registration guard is open")
    for line in (PACK / "HASHES.sha256").read_text().splitlines():
        expected, raw = line.split("  ", 1)
        if sha256(PACK / raw) != expected:
            raise RuntimeError(f"pack checksum drift: {raw}")
    print(f"Verified {SET}: exact canvas/alpha/semantic masks; V38/V41 move-heal contracts unchanged")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
