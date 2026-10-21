#!/usr/bin/env python3
"""Build the immutable fitted-cabinet Ligne-Claire V3 review pack.

V3 answers the rejected V2 review without altering any source or runtime file.
It applies one shared colour system to Cabinet A/B, the fridge carcass/worktop,
the sink cabinet and the compositor's join/healing layers.  Canvas, alpha,
semantic membership and all V19/V37/V38/V41 placement/behaviour contracts stay
exact.  Review enlargement uses smooth interpolation instead of the pixelated
V2 presentation.
"""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-fitted-cabinet-ligne-claire-v3"
DATED = "kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3"
PACK = ROOT / "art" / "drafts" / DATED
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"
CALIBRATION = EVIDENCE / "style-calibration-non-authoritative.png"
STYLE_REFERENCES = (
    PACK / "references" / "herge-soft-clarity.png",
    PACK / "references" / "herge-detail-density.png",
)

VISIBLE_ALPHA = 8
INKS = ((5, 24, 36), (10, 34, 43))
WORKTOP = ((47, 119, 133), (83, 177, 181), (109, 201, 194))
BLUES = ((29, 69, 98), (35, 91, 133), (45, 119, 157), (64, 153, 194))
COPPER = ((144, 82, 49), (211, 111, 45), (231, 166, 56))
NEUTRALS = ((92, 108, 111), (174, 187, 185), (246, 229, 183))
PALETTE_ANCHORS = INKS + WORKTOP + BLUES + COPPER + NEUTRALS

CABINET_SOURCE = "art/raw/kitchen-split-cabinet-workbench-2026-10-20-v38"
FRIDGE_SOURCE = "art/raw/kitchen-modular-fridge-workbench-2026-10-20-v37"
SINK_SOURCE = "art/raw/kitchen-sink-smooth-join-2026-10-19-v19"
HEALING_SOURCE = "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41"

CABINET_NAMES = (
    "cabinet-a-le-re.png", "cabinet-a-le-rj.png",
    "cabinet-a-lj-re.png", "cabinet-a-lj-rj.png",
    "cabinet-b-le-re.png", "cabinet-b-le-rj.png",
    "cabinet-b-lj-re.png", "cabinet-b-lj-rj.png",
)
FRIDGE_NAMES = ("fridge-standard.png", "fridge-broken-hinge-failed.png")
SINK_NAMES = (
    "sink-cabinet-standard.png",
    "sink-cabinet-on-base.png",
    "sink-cabinet-broken-base.png",
)
HEALING_NAMES = (
    "join-body-backfill-template.png",
    "countertop-join-cap-template.png",
    "countertop-triangle-underlay-template.png",
    "neighbour-seam-cleanup-left.png",
    "neighbour-seam-cleanup-right.png",
)

ASSET_GROUPS = (
    ("cabinets", CABINET_SOURCE, CABINET_NAMES),
    ("fridge", FRIDGE_SOURCE, FRIDGE_NAMES),
    ("sink", SINK_SOURCE, SINK_NAMES),
    ("healing", HEALING_SOURCE, HEALING_NAMES),
)

CONTRACT_FILES = (
    "art/drafts/kitchen-split-cabinet-workbench-2026-10-20-v38/candidate-catalogue.json",
    "art/drafts/kitchen-modular-fridge-workbench-2026-10-20-v37/candidate-catalogue.json",
    "art/drafts/kitchen-sink-smooth-join-2026-10-19-v19/candidate-catalogue.json",
    "art/drafts/kitchen-dishwasher-workbench-2026-10-20-v41/candidate-catalogue.json",
    "scripts/verify_kitchen_split_cabinet_workbench_v38.mjs",
    "scripts/verify_kitchen_modular_fridge_workbench_v37.mjs",
    "scripts/verify_kitchen_sink_smooth_join_v19.mjs",
    "scripts/verify_kitchen_dishwasher_workbench_v41.mjs",
    "docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md",
)

INHERITED_EFFECTS = (
    "art/raw/kitchen-modular-fridge-workbench-2026-10-20-v37/fx-fridge-drip-ripple-f40.png",
    "art/raw/kitchen-sink-smooth-join-2026-10-19-v19/fx-sink-on-water-f40.png",
    "art/raw/kitchen-sink-smooth-join-2026-10-19-v19/fx-sink-broken-basin-spouts-f40.png",
)

ROOM_SOURCE = ROOT / CABINET_SOURCE
ROOM_CASES = (
    {
        "id": "origin-contiguous",
        "source": "cabinet-pair-origin-native-room.png",
        "positions": {"fridge": 84, "cabinetA": 168, "cabinetB": 252, "oven": 336, "sink": 420},
    },
    {
        "id": "dislocated-contiguous",
        "source": "cabinet-dislocated-contiguous-native-room.png",
        "positions": {"cabinetA": 84, "fridge": 168, "cabinetB": 252, "oven": 336, "sink": 420},
    },
    {
        "id": "separated-exposed",
        "source": "cabinet-separated-exposed-native-room.png",
        "positions": {"cabinetA": 84, "oven": 168, "fridge": 252, "sink": 420, "cabinetB": 504},
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
    if s > 0.20 and 165 <= degrees < 198:
        return "worktop"
    if (s > 0.20 and 198 <= degrees < 265) or (b > g * 1.18 and b > r * 1.5):
        return "cabinet-body"
    return "neutral"


def class_mask(image: Image.Image, label: str) -> bytes:
    return bytes(255 if semantic_class(pixel) == label else 0 for pixel in image.getdata())


def mix(a: tuple[int, int, int], b: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    amount = max(0.0, min(1.0, amount))
    amount = amount * amount * (3.0 - 2.0 * amount)
    return tuple(round(left + (right - left) * amount) for left, right in zip(a, b))


def soft_spots(
    value: float,
    colours: tuple[tuple[int, int, int], ...],
    thresholds: tuple[float, ...],
    width: float,
) -> tuple[tuple[int, int, int], bool]:
    for index, threshold in enumerate(thresholds):
        low = threshold - width
        high = threshold + width
        if value < low:
            return colours[index], False
        if value <= high:
            return mix(colours[index], colours[index + 1], (value - low) / (2 * width)), True
    return colours[-1], False


def style_colour(pixel: tuple[int, int, int, int]) -> tuple[tuple[int, int, int], bool]:
    r, g, b, _a = pixel
    _h, _s, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    label = semantic_class(pixel)
    if label == "construction-ink":
        return soft_spots(value, INKS, (0.13,), 0.055)
    if label == "hardware":
        return soft_spots(value, COPPER, (0.48, 0.78), 0.055)
    if label == "worktop":
        return soft_spots(value, WORKTOP, (0.42, 0.72), 0.065)
    if label == "cabinet-body":
        return soft_spots(value, BLUES, (0.42, 0.58, 0.78), 0.055)
    return soft_spots(value, NEUTRALS, (0.42, 0.70), 0.055)


def stylise(source: Image.Image) -> tuple[Image.Image, int]:
    source = source.convert("RGBA")
    output = Image.new("RGBA", source.size)
    pixels = []
    transition_count = 0
    for pixel in source.getdata():
        if pixel[3] == 0:
            pixels.append((0, 0, 0, 0))
            continue
        colour, transition = style_colour(pixel)
        transition_count += int(transition)
        pixels.append((*colour, pixel[3]))
    output.putdata(pixels)
    return output, transition_count


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
    shown = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    base = checker(size)
    base.alpha_composite(shown, ((size[0] - shown.width) // 2, (size[1] - shown.height) // 2))
    return base


def contact_sheet(records: list[dict[str, object]], family: str) -> Path:
    rows = [record for record in records if record["family"] == family]
    width, panel_height, header = 920, 304, 64
    sheet = Image.new("RGBA", (width, header + panel_height * len(rows)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), f"{family}: current authority / fitted-family Ligne-Claire V3", fill=INKS[0], font=font)
    draw.text((12, 31), "Exact canvas, alpha, padding and semantic masks; smooth review enlargement", fill=INKS[0], font=font)
    for index, record in enumerate(rows):
        y = header + index * panel_height
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        sheet.alpha_composite(panel(source, (460, 270)), (0, y))
        sheet.alpha_composite(panel(candidate, (460, 270)), (460, y))
        draw.text((10, y + 276), f"CURRENT · {record['filename']}", fill=INKS[0], font=font)
        draw.text((470, y + 276), f"V3 · {str(record['candidateSha256'])[:12]}", fill=INKS[0], font=font)
    path = EVIDENCE / f"{family}-current-vs-candidate.png"
    sheet.save(path, optimize=True)
    return path


def composite(base: Image.Image, layer: Image.Image, xy: tuple[int, int]) -> None:
    base.alpha_composite(layer.convert("RGBA"), xy)


def neighbours(identifier: str, positions: dict[str, int]) -> tuple[bool, bool]:
    x = positions[identifier]
    occupied = {value for key, value in positions.items() if key != identifier}
    return x - 84 in occupied, x + 84 in occupied


def joins(positions: dict[str, int]) -> list[dict[str, object]]:
    ordered = sorted(positions.items(), key=lambda item: item[1])
    result = []
    for (left_id, left_x), (right_id, right_x) in zip(ordered, ordered[1:]):
        if left_x + 84 == right_x:
            result.append({
                "left": left_id,
                "right": right_id,
                "edge": right_x,
                "method": "oven-triangle" if "oven" in (left_id, right_id) else "flat-v22",
            })
    return result


def room_candidate(case: dict[str, object], records: list[dict[str, object]]) -> Path:
    positions = dict(case["positions"])
    lookup = {
        (str(record["family"]), str(record["filename"])): Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        for record in records
    }
    room = Image.open(ROOM_SOURCE / "room-background-exact.png").convert("RGBA")
    active_joins = joins(positions)

    body = lookup[("healing", "join-body-backfill-template.png")]
    triangle = lookup[("healing", "countertop-triangle-underlay-template.png")]
    for item in active_joins:
        edge = int(item["edge"])
        composite(room, body.crop((0, 0, 6, 63)), (edge - 3, 145))
        if item["method"] == "oven-triangle":
            composite(room, triangle, (edge - 12, 134))

    for identifier, x in sorted(positions.items(), key=lambda item: item[1]):
        if identifier in ("cabinetA", "cabinetB"):
            left, right = neighbours(identifier, positions)
            prefix = "cabinet-a" if identifier == "cabinetA" else "cabinet-b"
            name = f"{prefix}-{'lj' if left else 'le'}-{'rj' if right else 're'}.png"
            composite(room, lookup[("cabinets", name)], (x - 4, 130))
        elif identifier == "fridge":
            composite(room, lookup[("fridge", "fridge-standard.png")], (x - 30, 130))
        elif identifier == "sink":
            sink = lookup[("sink", "sink-cabinet-standard.png")].copy()
            left, _right = neighbours(identifier, positions)
            if not left:
                sink.paste((0, 0, 0, 0), (0, 26, 12, 108))
                source_patch = Image.open(ROOM_SOURCE / "cabinet-run-v11-exact.png").convert("RGBA").crop((0, 0, 12, 82))
                patch, _count = stylise(source_patch)
                composite(sink, patch, (0, 26))
            composite(room, sink, (x - 4, 104))
        elif identifier == "oven":
            composite(room, Image.open(ROOM_SOURCE / "oven-off.png").convert("RGBA"), (x - 4, 127))

    cap = lookup[("healing", "countertop-join-cap-template.png")]
    cleanup_left = lookup[("healing", "neighbour-seam-cleanup-left.png")]
    cleanup_right = lookup[("healing", "neighbour-seam-cleanup-right.png")]
    for item in active_joins:
        edge = int(item["edge"])
        if item["method"] == "flat-v22":
            composite(room, cap.crop((0, 0, 16, 12)), (edge - 8, 134))
        elif item["left"] == "oven":
            composite(room, cleanup_right, (edge, 134))
        else:
            composite(room, cleanup_left, (edge - 6, 134))

    path = EVIDENCE / f"{case['id']}-candidate-room.png"
    room.save(path, optimize=True)
    return path


def movement_proof(records: list[dict[str, object]]) -> dict[str, object]:
    font = ImageFont.load_default()
    header = 48
    sheet = Image.new("RGBA", (1544, header + 224 * len(ROOM_CASES)), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 12), "Move/snap/heal proof — current / V3 fitted-family art at identical V38 datums", fill=INKS[0], font=font)
    cases = []
    for index, case in enumerate(ROOM_CASES):
        current_path = ROOM_SOURCE / str(case["source"])
        candidate_path = room_candidate(case, records)
        current = Image.open(current_path).convert("RGBA")
        candidate = Image.open(candidate_path).convert("RGBA")
        y = header + index * 224
        sheet.alpha_composite(current, (0, y))
        sheet.alpha_composite(candidate, (772, y))
        draw.text((8, y + 7), f"CURRENT · {case['id']}", fill=INKS[0], font=font)
        draw.text((780, y + 7), f"V3 FITTED FAMILY · {case['id']}", fill=INKS[0], font=font)
        cases.append({
            "id": case["id"],
            "currentFile": rel(current_path),
            "currentSha256": sha256(current_path),
            "candidateFile": rel(candidate_path),
            "candidateSha256": sha256(candidate_path),
            "positions": case["positions"],
        })
    path = EVIDENCE / "fitted-family-move-snap-heal-current-vs-candidate.png"
    sheet.save(path, optimize=True)
    return {"file": rel(path), "sha256": sha256(path), "cases": cases}


def review_html(records: list[dict[str, object]]) -> str:
    sections = []
    for family in ("cabinets", "fridge", "sink", "healing"):
        cards = []
        for record in (item for item in records if item["family"] == family):
            filename = html.escape(str(record["filename"]))
            source_url = html.escape(f"/activity-stories/repo/{record['sourceFile']}")
            candidate_url = html.escape(f"assets/{family}--{filename}")
            cards.append(f'''<article><h3>{filename}</h3><div class="compare"><figure><figcaption>Current authority</figcaption><div class="stage"><img src="{source_url}" alt="Current {filename}"></div></figure><figure><figcaption>V3 candidate</figcaption><div class="stage"><img src="{candidate_url}" alt="Candidate {filename}"></div></figure></div><p>{record['pixels'][0]} × {record['pixels'][1]} px · exact alpha and semantic masks · soft transition pixels {record['softTransitionPixels']} · source <code>{str(record['sourceSha256'])[:12]}</code> · candidate <code>{str(record['candidateSha256'])[:12]}</code></p></article>''')
        sections.append(f"<section><h2>{family.title()}</h2>{''.join(cards)}</section>")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen fitted-cabinet Ligne-Claire V3</title><style>:root{{--ink:#051824;--cream:#f6e5b7;--paper:#fff9e8;--blue:#235b85}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,section{{max-width:1180px;margin:auto;padding:28px}}header{{border-bottom:4px solid var(--ink)}}.status{{display:inline-block;padding:7px 12px;border:2px solid var(--ink);background:#e0a229;color:#071824;font-weight:800;border-radius:999px}}article{{margin:20px 0;padding:15px;background:var(--paper);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue)}}.compare{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}figure{{margin:0}}figcaption{{font-weight:800}}.stage{{height:290px;display:grid;place-items:center;background:#eee6d0}}img{{max-width:95%;max-height:95%;image-rendering:auto}}a{{color:#174562;font-weight:800}}code{{font-size:.85em}}.warning{{border-left:6px solid #d2523b;padding-left:14px}}@media(max-width:700px){{.compare{{grid-template-columns:1fr}}}}</style></head><body><header><span class="status">REVIEW ONLY · NOT CURRENT</span><h1>Kitchen fitted-cabinet Ligne-Claire V3</h1><p class="warning">V2 is rejected and remains immutable. V3 is a new candidate only; nothing here is registered, wired or current.</p><p>V3 treats Cabinet A/B, the fridge worktop/carcass, the sink cabinet and their five healing layers as one fitted family. The oven and small objects are unchanged and outside this review.</p><p>The exact current asset remains the structural authority. Canvas, alpha, padding, worktop/body/fixture/line masks, pivots, anchors, collisions, movement, state, interaction and healing contracts are hash-pinned. Review enlargement now uses smooth interpolation rather than V2's pixelated scaling.</p><p><a href="assets/evidence--fitted-family-move-snap-heal-current-vs-candidate.png">Open complete move/snap/heal contact sheet</a> · <a href="assets/evidence--style-calibration-non-authoritative.png">Open non-authoritative colour study</a> · <a href="/keeper-review/kitchen-split-cabinet-workbench-v38/">Open V38 movement authority</a> · <a href="/keeper-review/kitchen-dishwasher-workbench-v41/">Open V41 healing/lock authority</a></p></header>{''.join(sections)}</body></html>'''


def write_hashes() -> None:
    files = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256")
    (PACK / "HASHES.sha256").write_text(
        "\n".join(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}" for path in files) + "\n"
    )


def build() -> None:
    if not CALIBRATION.exists():
        raise RuntimeError(f"missing calibration study: {CALIBRATION}")
    for reference in STYLE_REFERENCES:
        if not reference.exists():
            raise RuntimeError(f"missing supplied style reference: {reference}")
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    assets = []
    labels = ("construction-ink", "worktop", "cabinet-body", "hardware", "neutral")
    for family, source_dir, names in ASSET_GROUPS:
        family_dir = CANDIDATES / family
        family_dir.mkdir(parents=True, exist_ok=True)
        for name in names:
            source_path = ROOT / source_dir / name
            source = Image.open(source_path).convert("RGBA")
            candidate, transitions = stylise(source)
            candidate_path = family_dir / name
            candidate.save(candidate_path, optimize=True)
            alpha = source.getchannel("A")
            shape_hashes = {label: digest_bytes(class_mask(source, label)) for label in labels}
            candidate_hashes = {label: digest_bytes(class_mask(candidate, label)) for label in labels}
            if shape_hashes != candidate_hashes:
                raise RuntimeError(f"candidate semantic classification drift: {family}/{name}")
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
                "softTransitionPixels": transitions,
                "visibleRgbColourCount": len({pixel[:3] for pixel in candidate.getdata() if pixel[3] > VISIBLE_ALPHA}),
                "canvasExact": True,
                "alphaExact": True,
                "semanticShapeMasksExact": True,
                "contourDilationPixels": 0,
            })

    contacts = {}
    for family in ("cabinets", "fridge", "sink", "healing"):
        path = contact_sheet(assets, family)
        contacts[family] = {"file": rel(path), "sha256": sha256(path)}
    movement = movement_proof(assets)

    tomato = ROOT / "art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/drafts/components/sandwich-tomato.png"
    rejection = ROOT / "docs/review/kitchen-cabinet-ligne-claire-v2-rejection-2026-10-21.json"
    contracts = [{"file": path, "sha256": sha256(ROOT / path), "unchanged": True} for path in CONTRACT_FILES]
    effects = [{"file": path, "sha256": sha256(ROOT / path), "unchanged": True} for path in INHERITED_EFFECTS]
    manifest = {
        "schema": "lighthouse-keeper/kitchen-fitted-cabinet-ligne-claire@3",
        "set": SET,
        "datedDirectory": DATED,
        "created": "2026-10-21",
        "status": "immutable-reversible-review-candidate-not-approved-not-registered",
        "supersedesForReview": "kitchen-cabinet-ligne-claire-v2 (rejected for incomplete family palette and pixelated review presentation)",
        "v2Rejection": {"file": rel(rejection), "sha256": sha256(rejection)},
        "scope": {
            "included": ["split cabinet A", "split cabinet B", "fridge worktop and carcass", "sink cabinet and fixtures", "join/healing layers"],
            "excluded": ["oven", "dishwasher", "kettle", "toaster", "mixing bowl", "pedal bin", "table/chair", "all animation/effect strips"],
        },
        "primaryVisualCalibration": {"file": rel(tomato), "sha256": sha256(tomato), "version": 2},
        "suppliedStyleReferences": [
            {
                "file": rel(reference),
                "sha256": sha256(reference),
                "role": "soft-but-clear antialiasing and retained interior-detail density",
            }
            for reference in STYLE_REFERENCES
        ],
        "nonAuthoritativeCalibrationStudy": {"file": rel(CALIBRATION), "sha256": sha256(CALIBRATION), "candidatePixelsUsed": False},
        "paletteAnchors": ["#%02x%02x%02x" % colour for colour in PALETTE_ANCHORS],
        "derivation": "Shared semantic spot-colour translation with narrow deterministic tone-transition ramps and every source interior line retained; no resize, crop, alpha edit, spatial blur, contour dilation, erosion, detail deletion or silhouette generation",
        "reviewPresentation": {"nearestNeighbourEnlargement": False, "cssPixelatedRendering": False, "smoothInterpolation": "Lanczos/contact sheets; auto/browser"},
        "assets": assets,
        "evidence": contacts,
        "movementHealingProof": movement,
        "unchangedContracts": contracts,
        "unchangedEffects": effects,
        "checks": {
            "sourceBytesUntouched": True,
            "candidateCanvasExact": True,
            "candidateAlphaExact": True,
            "candidateBoundsExact": True,
            "transparentPaddingExact": True,
            "semanticShapeMasksExact": True,
            "sharedFittedFamilyPalette": True,
            "contourDilationPixels": 0,
            "movementSnapSwapHealingContractsUnchanged": True,
            "animationAndEffectBytesUnchanged": True,
            "roomLayoutChanged": False,
            "runtimeChanged": False,
            "registrationPerformed": False,
            "currentSelectorChanged": False,
        },
        "approvalRequiredFor": "any registration, selector update, Final copy or runtime wiring",
        "rollback": "Discard only the V3 dated directory and matching review set; V1, V2, every source/current/runtime file and all selectors remain byte-for-byte in place.",
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
        raise RuntimeError(f"refusing to overwrite immutable review route: {PUBLIC}")
    PUBLIC_ASSETS.mkdir(parents=True, exist_ok=False)
    for record in assets:
        shutil.copy2(ROOT / str(record["candidateFile"]), PUBLIC_ASSETS / f"{record['family']}--{record['filename']}")
    for item in contacts.values():
        shutil.copy2(ROOT / str(item["file"]), PUBLIC_ASSETS / f"evidence--{Path(str(item['file'])).name}")
    shutil.copy2(ROOT / str(movement["file"]), PUBLIC_ASSETS / f"evidence--{Path(str(movement['file'])).name}")
    for case in movement["cases"]:
        shutil.copy2(ROOT / str(case["candidateFile"]), PUBLIC_ASSETS / f"evidence--{Path(str(case['candidateFile'])).name}")
    shutil.copy2(CALIBRATION, PUBLIC_ASSETS / "evidence--style-calibration-non-authoritative.png")
    (PUBLIC / "index.html").write_text(review_html(assets))
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
    write_hashes()
    verify()
    print(f"Built {SET}: {len(assets)} exact-geometry candidates; registration remains closed")


def verify() -> None:
    manifest_path = PACK / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest["set"] != SET or "not-approved" not in manifest["status"]:
        raise RuntimeError("identity/status drift")
    if manifest["checks"]["registrationPerformed"] or manifest["checks"]["currentSelectorChanged"]:
        raise RuntimeError("registration boundary opened")
    expected_count = sum(len(names) for _family, _source, names in ASSET_GROUPS)
    if len(manifest["assets"]) != expected_count:
        raise RuntimeError("asset coverage drift")
    for record in manifest["assets"]:
        source_path = ROOT / record["sourceFile"]
        candidate_path = ROOT / record["candidateFile"]
        if sha256(source_path) != record["sourceSha256"] or sha256(candidate_path) != record["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record['filename']}")
        source = Image.open(source_path).convert("RGBA")
        candidate = Image.open(candidate_path).convert("RGBA")
        rebuilt, transitions = stylise(source)
        if source.size != candidate.size:
            raise RuntimeError(f"canvas drift: {record['filename']}")
        if source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"alpha/padding drift: {record['filename']}")
        if rebuilt.tobytes() != candidate.tobytes() or transitions != record["softTransitionPixels"]:
            raise RuntimeError(f"deterministic RGB derivation drift: {record['filename']}")
        for label, expected in record["semanticShapeMaskSha256"].items():
            if digest_bytes(class_mask(source, label)) != expected:
                raise RuntimeError(f"source shape-mask drift: {record['filename']} {label}")
            if digest_bytes(class_mask(candidate, label)) != expected:
                raise RuntimeError(f"candidate shape-mask drift: {record['filename']} {label}")
    for item in manifest["unchangedContracts"] + manifest["unchangedEffects"]:
        if sha256(ROOT / item["file"]) != item["sha256"]:
            raise RuntimeError(f"inherited authority drift: {item['file']}")
    rejection = manifest["v2Rejection"]
    if sha256(ROOT / rejection["file"]) != rejection["sha256"]:
        raise RuntimeError("V2 rejection record drift")
    register = json.loads((PACK / "batch-register.json").read_text())
    if register["register"] or register["promote"] or register["currentSelectorChanges"]:
        raise RuntimeError("registration guard is open")
    review = (PUBLIC / "index.html").read_text()
    forbidden_resampler = "Resampling." + "NEAREST"
    if "image-rendering:pixelated" in review or forbidden_resampler in Path(__file__).read_text():
        raise RuntimeError("pixelated review rendering returned")
    if "image-rendering:auto" not in review:
        raise RuntimeError("smooth review rendering contract missing")
    for line in (PACK / "HASHES.sha256").read_text().splitlines():
        expected, raw = line.split("  ", 1)
        if sha256(PACK / raw) != expected:
            raise RuntimeError(f"pack checksum drift: {raw}")
    print(f"Verified {SET}: exact geometry/alpha/masks; fitted palette and V19/V37/V38/V41 contracts pinned")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
