#!/usr/bin/env python3
"""Build the reversible, high-resolution Keeper Prime master V1 review pack."""
from __future__ import annotations

import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-master-v1"
SOURCE = PACK / "sources/keeper-prime-master-front-generated.png"
PRIMARY = ROOT / "art/raw/keeper-first-batch/keeper_neutral_standing-front_f1.png"
QUALITY = ROOT / "art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/drafts/keeper_artist-smock_neutral_standing-front_f1.png"
REJECTED_DOUBLE = PACK / "rejected-sources/double-stripe-smooth-render.png"
REJECTED_NARROW = PACK / "rejected-sources/double-stripe-narrow-render.png"
REJECTED_MOUTH = PACK / "rejected-sources/double-stripe-neutral-mouth-render.png"

CELL = (256, 320)
LOGICAL_CELL = (32, 40)
DENSITY = 8
ANCHOR = (16, 40)
TARGET_TOP = 18
TARGET_BOTTOM = 316
ALPHA_CROP_THRESHOLD = 8


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def json_dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def significant_bbox(image: Image.Image, threshold: int = ALPHA_CROP_THRESHOLD) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    binary = alpha.point(lambda value: 255 if value >= threshold else 0)
    box = binary.getbbox()
    if box is None:
        raise RuntimeError("source has no significant alpha")
    return box


def normalize_source() -> tuple[Image.Image, dict]:
    source = Image.open(SOURCE).convert("RGBA")
    box = significant_bbox(source)
    crop = source.crop(box)
    target_height = TARGET_BOTTOM - TARGET_TOP
    target_width = round(crop.width * target_height / crop.height)
    if target_width > CELL[0] - 16:
        raise RuntimeError(f"preferred source is too wide for a safe gutter: {target_width}px")
    resized = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", CELL, (0, 0, 0, 0))
    x = (CELL[0] - target_width) // 2
    canvas.alpha_composite(resized, (x, TARGET_TOP))
    # Remove invisible generation haze while retaining normal antialiasing.
    pixels = canvas.load()
    for y in range(canvas.height):
        for px in range(canvas.width):
            red, green, blue, alpha = pixels[px, y]
            if alpha < ALPHA_CROP_THRESHOLD:
                pixels[px, y] = (0, 0, 0, 0)
    bbox = canvas.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("normalized master became empty")
    return canvas, {
        "sourcePixels": list(source.size),
        "sourceSignificantAlphaBoundsExclusive": list(box),
        "normalizedOpaqueBoundsExclusive": list(bbox),
        "normalizedOpaqueWidthHeightRatio": round((bbox[2] - bbox[0]) / (bbox[3] - bbox[1]), 6),
        "logicalCell": list(LOGICAL_CELL),
        "density": DENSITY,
        "sourceCell": list(CELL),
        "logicalAnchor": list(ANCHOR),
        "sourceAnchor": [ANCHOR[0] * DENSITY, ANCHOR[1] * DENSITY],
    }


def landmarks() -> dict:
    # Exact coordinates for the normalized 256x320 proposal. Bounds are exclusive.
    return {
        "verticalIdentityAxisX": 128,
        "floorAnchor": [128, 320],
        "capTopY": 18,
        "headEnvelopeBoundsExclusive": [73, 18, 184, 148],
        "leftEyeBoundsExclusive": [111, 75, 120, 87],
        "rightEyeBoundsExclusive": [137, 75, 146, 87],
        "noseBoundsExclusive": [118, 86, 139, 105],
        "moustacheBoundsExclusive": [96, 91, 162, 119],
        "mouthBoundsExclusive": [119, 108, 137, 114],
        "beardEnvelopeBoundsExclusive": [86, 82, 171, 149],
        "chestBandBoundsExclusive": [48, 145, 208, 178],
    }


def mask_for(bounds: list[int]) -> Image.Image:
    mask = Image.new("L", CELL, 0)
    ImageDraw.Draw(mask).rectangle((bounds[0], bounds[1], bounds[2] - 1, bounds[3] - 1), fill=255)
    return mask


def labelled_comparison(master: Image.Image) -> Image.Image:
    scale = Image.Resampling.NEAREST
    primary = Image.open(PRIMARY).convert("RGBA").resize(CELL, scale)
    quality = Image.open(QUALITY).convert("RGBA").resize(CELL, scale)
    width, height = 3 * 288, 384
    panel = Image.new("RGBA", (width, height), (14, 22, 29, 255))
    draw = ImageDraw.Draw(panel)
    labels = ["Frame 6 authority", "V11 finish reference", "Prime Master V1 proposal"]
    for index, (label, image) in enumerate(zip(labels, (primary, quality, master))):
        x = index * 288 + 16
        checker = Image.new("RGBA", CELL, (31, 43, 52, 255))
        checker_draw = ImageDraw.Draw(checker)
        for y in range(0, CELL[1], 16):
            for px in range(0, CELL[0], 16):
                if (px // 16 + y // 16) % 2:
                    checker_draw.rectangle((px, y, px + 15, y + 15), fill=(42, 56, 66, 255))
        checker.alpha_composite(image)
        panel.alpha_composite(checker, (x, 42))
        draw.text((x, 14), label, fill=(236, 244, 249, 255), font=ImageFont.load_default())
    return panel


def write_page(register: dict) -> None:
    assets = PUBLIC / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    sources = {
        "primary": PRIMARY,
        "quality": QUALITY,
        "master": ROOT / register["candidate"]["file"],
        "comparison": ROOT / register["evidence"]["comparison"]["file"],
        "overlay": ROOT / register["evidence"]["landmarkOverlay"]["file"],
    }
    urls: dict[str, str] = {}
    for key, source in sources.items():
        target = assets / f"{key}-{digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        urls[key] = target.name
    mask_cards = []
    for name, record in register["masksAndGuides"].items():
        source = ROOT / record["file"]
        target = assets / f"mask-{name}-{record['sha256'][:16]}.png"
        shutil.copyfile(source, target)
        mask_cards.append(
            f'<article><h3>{html.escape(name.replace("-", " ").title())}</h3>'
            f'<img src="assets/{target.name}" alt="{html.escape(name)} guide mask">'
            f'<p><code>{record["boundsExclusive"]}</code></p></article>'
        )
    masks_html = "".join(mask_cards)
    page = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Keeper Prime Master V1</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--muted:#aabac5;--amber:#f0b84d}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1420px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}h1{{margin:.2rem 0}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffd889}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.sprite{{height:520px;max-height:62vh;object-fit:contain}}.wide{{width:100%}}code{{overflow-wrap:anywhere;color:#b8dbef}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}a{{color:#8ed2fa}}</style></head><body><header><a href=\"/animation-workbench\">← Animation Workbench</a><h1>Keeper Prime Master V1</h1><span class=\"status\">Draft · awaiting visual approval · Final contains 0 animations</span><p>A new smooth high-resolution foundation derived from Frame 6 identity. No animation, raw sprite, runtime sprite or manifest has been promoted.</p></header><main><section class=\"grid\"><article><h2>Frame 6 identity authority</h2><img class=\"sprite\" src=\"assets/{urls['primary']}\" alt=\"Frame 6 identity authority\"><p><code>{register['references']['frame6']['sha256']}</code></p></article><article><h2>V11 finish reference</h2><img class=\"sprite\" src=\"assets/{urls['quality']}\" alt=\"V11 rendering reference\"><p><code>{register['references']['v11']['sha256']}</code></p></article><article><h2>Prime Master V1 proposal</h2><img class=\"sprite\" src=\"assets/{urls['master']}\" alt=\"Prime Master V1 proposal\"><p><code>{register['candidate']['sha256']}</code></p></article></section><p class=\"rule\"><strong>User-selected design decision:</strong> one broad pale chest band replaces the legacy double stripe so the uniform remains stable through turns and action poses. The double-stripe generations are rejected provenance.</p><h2>Side-by-side evidence</h2><article><img class=\"wide\" src=\"assets/{urls['comparison']}\" alt=\"Frame 6, V11 and Prime Master comparison\"></article><h2>Landmark evidence</h2><article><img class=\"sprite\" src=\"assets/{urls['overlay']}\" alt=\"Prime Master landmark overlay\"><pre>{html.escape(json.dumps(register['geometry']['landmarksSourcePixels'], indent=2))}</pre></article><h2>Approval boundary</h2><article><p>This is the only active foundation candidate. Every existing animation is unapproved. Full animation redrafting begins only after explicit approval of this master.</p></article></main></body></html>"""
    page = page.replace(
        "<h2>Approval boundary</h2>",
        f'<h2>Masks and guides</h2><section class="grid">{masks_html}</section><h2>Approval boundary</h2>',
    )
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    if not SOURCE.exists():
        raise RuntimeError(f"missing pinned preferred generated source: {relative(SOURCE)}")
    for directory in (PACK / "drafts", PACK / "references", PACK / "masks", PACK / "evidence", PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PRIMARY, PACK / "references/frame6-identity-authority.png")
    shutil.copyfile(QUALITY, PACK / "references/v11-rendering-quality-reference.png")

    master, geometry = normalize_source()
    master_path = PACK / "drafts/keeper_prime_master-neutral-front_f1.png"
    master.save(master_path, optimize=False, compress_level=9)
    feature_landmarks = landmarks()
    sidecar = {
        "name": "keeper_prime_master-neutral-front",
        "w": LOGICAL_CELL[0], "h": LOGICAL_CELL[1], "frames": 1, "fps": 1,
        "density": DENSITY, "anchor": list(ANCHOR), "loop": False,
        "startPose": "standing-front", "endPose": "standing-front",
        "status": "draft-awaiting-visual-approval",
        "source": relative(SOURCE),
        "uniform": "standard-single-broad-band",
        "landmarksSourcePixels": feature_landmarks,
    }
    sidecar_path = master_path.with_suffix(".json")
    json_dump(sidecar_path, sidecar)

    mask_records = {}
    for name, key in (("eye-left", "leftEyeBoundsExclusive"), ("eye-right", "rightEyeBoundsExclusive"), ("nose", "noseBoundsExclusive"), ("moustache", "moustacheBoundsExclusive"), ("mouth", "mouthBoundsExclusive"), ("beard-envelope", "beardEnvelopeBoundsExclusive"), ("head-envelope", "headEnvelopeBoundsExclusive"), ("chest-band", "chestBandBoundsExclusive")):
        path = PACK / "masks" / f"{name}-guide-mask.png"
        mask_for(feature_landmarks[key]).save(path, optimize=False, compress_level=9)
        mask_records[name] = {"file": relative(path), "sha256": digest(path), "boundsExclusive": feature_landmarks[key]}

    overlay = master.copy()
    draw = ImageDraw.Draw(overlay)
    colours = {"eyes": "#56c9ff", "moustache": "#ffb34d", "mouth": "#ff5c76", "beard": "#66e08b", "head": "#c78cff", "band": "#f4e06b"}
    for key, colour in (("leftEyeBoundsExclusive", colours["eyes"]), ("rightEyeBoundsExclusive", colours["eyes"]), ("moustacheBoundsExclusive", colours["moustache"]), ("mouthBoundsExclusive", colours["mouth"]), ("beardEnvelopeBoundsExclusive", colours["beard"]), ("headEnvelopeBoundsExclusive", colours["head"]), ("chestBandBoundsExclusive", colours["band"])):
        x0, y0, x1, y1 = feature_landmarks[key]
        draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=colour, width=2)
    draw.line((128, 0, 128, 319), fill="#ffffff", width=1)
    overlay_path = PACK / "evidence/keeper-prime-master-landmark-overlay.png"
    overlay.save(overlay_path, optimize=False, compress_level=9)
    comparison_path = PACK / "evidence/keeper-prime-master-comparison.png"
    labelled_comparison(master).save(comparison_path, optimize=False, compress_level=9)

    bbox = master.getchannel("A").getbbox()
    assert bbox is not None
    edge_alpha = []
    for x in range(master.width):
        edge_alpha.extend((master.getpixel((x, 0))[3], master.getpixel((x, master.height - 1))[3]))
    for y in range(master.height):
        edge_alpha.extend((master.getpixel((0, y))[3], master.getpixel((master.width - 1, y))[3]))
    rejected = []
    for path, reason in ((REJECTED_DOUBLE, "preferred rendering lost the single-band uniform"), (REJECTED_NARROW, "double stripe rejected as difficult to retain consistently"), (REJECTED_MOUTH, "double stripe rejected; superseded surgical mouth variant")):
        if path.exists():
            rejected.append({"file": relative(path), "sha256": digest(path), "reason": reason})
    register = {
        "packId": "keeper-prime-master-2026-10-12-v1",
        "status": "draft-awaiting-visual-approval",
        "purpose": "Replace visibly pixelated Frame 6 endpoints with one smooth master family before any animation is redrafted.",
        "userDecision": "Prefer the first smooth render and replace the double-stripe jumper with one broad pale band for animation consistency.",
        "references": {
            "frame6": {"file": relative(PRIMARY), "sha256": digest(PRIMARY), "role": "identity, stance, head-position and endpoint geometry authority; coarse raster is not a rendering target"},
            "v11": {"file": relative(QUALITY), "sha256": digest(QUALITY), "role": "smooth rendering-quality reference only"},
        },
        "generatedSource": {"file": relative(SOURCE), "sha256": digest(SOURCE), "role": "user-preferred first smooth single-band render"},
        "candidate": {"file": relative(master_path), "sha256": digest(master_path), "sidecar": relative(sidecar_path), "sidecarSha256": digest(sidecar_path), "promotionAllowed": False},
        "geometry": {**geometry, "landmarksSourcePixels": feature_landmarks},
        "masksAndGuides": mask_records,
        "evidence": {
            "comparison": {"file": relative(comparison_path), "sha256": digest(comparison_path)},
            "landmarkOverlay": {"file": relative(overlay_path), "sha256": digest(overlay_path)},
        },
        "identityRules": {
            "eyes": "solid dark rectangular eyes; no glints, whites, round or childlike eyes",
            "moustache": "clearly separate from the mouth",
            "mouth": "short straight readable closed mouth; no grin or generic smile",
            "beard": "established broad cream beard mass",
            "uniform": "one broad pale chest-and-sleeve band; do not restore the legacy double stripe",
        },
        "rejectedGeneratedProvenance": rejected,
        "validation": {
            "candidateGeometryMatchesSidecar": master.size == CELL,
            "transparentSafetyGutter": max(edge_alpha) == 0,
            "opaqueCellEdgePixels": sum(1 for value in edge_alpha if value > 0),
            "alphaCropThreshold": ALPHA_CROP_THRESHOLD,
            "deterministicNormalization": True,
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
            "finalAnimations": 0,
        },
        "promptLog": relative(PACK / "PROMPT_LOG.md"),
        "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; production and historical drafts remain untouched.",
    }
    json_dump(PACK / "master-pack-register.json", register)
    write_page(register)
    print(json.dumps({"candidate": relative(master_path), "sha256": digest(master_path), "bbox": bbox, "publicPage": relative(PUBLIC / 'index.html')}, indent=2))


if __name__ == "__main__":
    main()
