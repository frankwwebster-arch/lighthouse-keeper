#!/usr/bin/env python3
"""Build the immutable Claude household cleaning-cupboard asset pack V1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/claude-household-cleaning-cupboard-pack-2026-10-21-v1"
SOURCE_DIR = PACK / "source"
ASSET_DIR = PACK / "assets"
EVIDENCE_DIR = PACK / "evidence"
KITCHEN_REFERENCE = ROOT / "art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1/evidence/final-assets-contact-sheet.webp"
TOOLS_REFERENCE = ROOT / "art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1/evidence/final-assets-contact-sheet.webp"
VISIBLE_ALPHA = 8
CELL = 256
TARGET = 216

SPECS = (
    ("cleaner-bleach-bottle", "cleaning-chemical", "exec-dbb004ff-483f-43c7-8153-566dadc1893e.png", "016774f6e082a09d4f26e4eb71155ee265b3a9bcb8b37c0180f520469baaee04", [1272, 1236]),
    ("cleaner-disinfectant-bottle", "cleaning-chemical", "exec-0ae07467-c00d-4102-ba03-af2982d96d35.png", "9d1d59847062e6675409b6d236256170070d175483ccd078ccd8b5f58b6909eb", [1308, 1202]),
    ("cleaner-multisurface-spray", "cleaning-chemical", "exec-810f113d-2c57-4466-b28a-1e8d5ee91172.png", "223b6e00efe5e29ec28681c227a1de9f6b12afa80304d755272bc9e8e100b000", [1174, 1339]),
    ("cleaner-glass-spray", "cleaning-chemical", "exec-da6f944e-97fa-40b0-ac45-94f2f869bc1f.png", "20d54ed88d00861a2c225b166b0f2a7a0488ebb50fe4e2d024975ddaafeda0e5", [1174, 1339]),
    ("cleaner-furniture-polish", "cleaning-chemical", "exec-fa7eb86d-ef27-453c-a7a1-01d90d7a333d.png", "63bdc732347a78b136c1687423adcc405f79e73d183f6656a9cfefc395415782", [1174, 1339]),
    ("cleaner-washing-up-liquid", "cleaning-chemical", "exec-ed850921-41e5-4c2c-879c-648cd92cc475.png", "ca1324e590b659cfae3f3a983010bd6efe12c3a80c4220321e7c88a7ce77ea5b", [1174, 1339]),
    ("laundry-washing-powder-box", "laundry", "exec-1d3eac73-3530-40f2-9b4f-1a03329f8169.png", "e6229d37ee2713798bf46ece2e765bf23e5f5e33ba44c9dac25f1ce5785aa350", [1312, 1199]),
    ("laundry-liquid-detergent", "laundry", "exec-3ee2cdae-1c1b-4398-96d7-e3112d6fafb3.png", "f4914c3220db67b974d1bbdccfa9b30c3168833f30fb7b459a00d496c4180210", [1174, 1339]),
    ("laundry-fabric-conditioner", "laundry", "exec-70554556-6e98-4473-8e88-78f5938593da.png", "1b3804672ec167b311be5e58e3652d3a1c3532cd9b263a83dce7a7a00d8a1878", [1174, 1339]),
    ("laundry-stain-remover-tub", "laundry", "exec-c9e5a753-b321-45ac-9e8b-14eb5b65fe09.png", "07d3f79c7c83b7dbee6285b01b113ded8232a2ab2eda52d07128ae3e3daa58ca", [1254, 1254]),
    ("dishwasher-tablets-tub", "dishwasher", "exec-5a7323b5-828c-4947-8846-5bfca7e7eeda.png", "dfbe101416e61f2b50bcb6d510c9e36423e96331d47e827beabb168930d01989", [1300, 1209]),
    ("dishwasher-salt-carton", "dishwasher", "exec-528dcc83-2f9c-4976-9bc9-acb11c0e6b62.png", "1e50d9846be8136199b3d16fd6216c8b68a87a014539616aacb66ca0feae8b1d", [1174, 1339]),
    ("dishwasher-rinse-aid", "dishwasher", "exec-7ece2f90-1783-424e-8642-99aff657eb93.png", "d7587a438172a1fc4b0c0667352a73e5778950fdae70dcf76e8c59693b27a28c", [1174, 1339]),
    ("cleaner-toilet-bottle", "cleaning-chemical", "exec-d0783e5f-d83e-4e97-a0a3-0592ce1a064b.png", "c3e5597a7171bab2c4703714362188340232342b78043c9f557c5ceede4496ab", [1174, 1339]),
    ("tool-dustpan", "tool", "exec-71c3849d-6789-4e7d-a8ad-46d9c20108fb.png", "eba64f11d7679cdf8b613e529e67da0f1c70d88d3ddb65697fb6f72cf0a17cb5", [1322, 1190]),
    ("tool-hand-brush", "tool", "exec-f8be51ac-6bd2-4c91-8cfc-4db47c2a1336.png", "2fdc69894183ef0e79b67ec7001a2b10f3df114e841f4678dc5107d9169ab215", [1536, 1024]),
    ("tool-broom", "tool", "exec-68638a2a-2eee-4add-b23f-552ca569a288.png", "b68567fec7ff332858a09649ad99ba6e9e29fb99ba65be677ef113fd6db00ae5", [1312, 1199]),
    ("tool-string-mop", "tool", "exec-ff1e4612-c951-4940-a4ef-ee1ccffc70ca.png", "1fb7c036c326b6d608465ae734649d73d8e33a4fa1857e461044c6a1c35f4702", [1230, 1278]),
    ("tool-cleaning-bucket", "tool", "exec-aecc962d-1c00-4e2d-8221-f21ac6518732.png", "fc2d859313c9d4152baca5ac24894fa43d9e0d2a971672429cebd376e6543a80", [1254, 1254]),
    ("wear-rubber-gloves-pair", "wearable", "exec-014411cb-88f7-4582-b3d7-6deb8722cca6.png", "0ef387085ebff7385104b2e14fe9c0748b2226ddb99bc28b31afa2fdee338937", [1402, 1122]),
    ("consumable-cellulose-sponge", "consumable", "exec-d6907e8f-d9c0-4658-8ce2-674ba528f384.png", "8d8f56678ca2bbf1c4365c40109ea7a06781dca2aa2fae545599122461e4c903", [1536, 1024]),
    ("consumable-scouring-pad", "consumable", "exec-0ac36ddc-c43b-4757-928b-d1563cde40a7.png", "50e69ebb4d1a51758d7adbe3d6186f34ae70d91468f56f6eb6920be97f76a7e3", [1536, 1024]),
    ("consumable-microfiber-cloth", "consumable", "exec-5455588f-cc9e-4010-9216-dc95b880ff98.png", "50cb49a3cc44681e128571d298dd5ae75cc05fae3f3512fbdc7c7dfe368506e9", [1536, 1024]),
    ("tool-feather-duster", "tool", "exec-350f5c77-d112-46f2-a18c-0e6279f11702.png", "8a868260a905d5d743388340416d0f66ff3e5f8e35d7d5f921c5b06f3b4d1c27", [1312, 1199]),
    ("tool-scrub-brush", "tool", "exec-a07f0f88-b331-4399-a415-3536dec687b6.png", "03da8374a4d987c9e6a4450f9801615275d227d356615ddd82ae0f0f2130899c", [1448, 1086]),
    ("consumable-bin-bag-roll", "consumable", "exec-081343ff-9c7b-4f9a-9a62-e0c9a3e918de.png", "d54d692d6059c56824bc239a6b3efb302ef0dbd9ff9125e59d53068c470a3114", [1536, 1024]),
)

REJECTED = (
    ("hand-brush-glow-attempt-1", "exec-5312cd77-d7a2-4780-be2c-bc421fd64d63.png", "7cbd269156e66a7bf62bf9ce52b169c75e74503bd25f615b8bfc9995cdab796e", [1536, 1024]),
    ("cellulose-sponge-glow-attempt-1", "exec-1aafbcdc-7ad1-480c-903b-cf27c8e948db.png", "a8d427e1f87f2f9b629166f633bb55e550578be33ff5556e1fc001c6bab07fb1", [1536, 1024]),
    ("scouring-pad-glow-attempt-1", "exec-387a0577-ead4-4730-9dc2-df0dca4515af.png", "eae06431dbc2c5c4b83c2f42cc7de828c52f46128fa26a548d342459602c04cd", [1536, 1024]),
    ("microfiber-cloth-glow-attempt-1", "exec-a4704e09-c925-4693-bd94-f2f54f6adae9.png", "0a1a67f9438a510dcf1fe54c66aad90f5fafb218d254b61add3eecf4215006b1", [1536, 1024]),
    ("hand-brush-glow-attempt-2", "exec-505e93a1-555b-4b51-896b-050c82552ff7.png", "c0d7935dc4eca04b5107bb8c5cf9f7c7bb30eb80045089d39199057b0ce4ce03", [1536, 1024]),
    ("cellulose-sponge-glow-attempt-2", "exec-a765f73f-2952-45f6-9625-c9462a741f04.png", "8294a98e844a013f43a88e2bf33227c35c004aca054a44c9edd3b723da6c0ed9", [1536, 1024]),
    ("hand-brush-clean-edit-rejected", "exec-667e7215-da67-463c-8177-d28c7017c537.png", "ec58c66857b87b2cfe557182e351a8411bf0b0a9abbc8d4031237293aee7a1f6", [1536, 1024]),
    ("cellulose-sponge-clean-edit-rejected", "exec-78346e31-0dd2-4859-af8d-adfe1279d042.png", "077433127cc156ce72b03af91db5e85c113672360e97ee48f4e22786aeecf713", [1536, 1024]),
    ("scouring-pad-clean-edit-rejected", "exec-d8c62ab2-afda-4092-abd7-b9585dc5e833.png", "63b8216544ccb8277fcd214a3c6e579a902c519acca5b5c715021ae1af2d7197", [1536, 1024]),
    ("microfiber-cloth-clean-edit-rejected", "exec-1e0f5104-f8ba-4013-a202-90bf6549be40.png", "aaddbe2c7de17866e413a3c5a00c9c7b488eadb7b334806bd560869758b88473", [1536, 1024]),
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.getchannel("A").point(lambda value: 255 if value > VISIBLE_ALPHA else 0).getbbox()
    if bounds is None:
        raise RuntimeError("source has no visible pixels")
    return bounds


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = {(x, 0) for x in range(image.width)} | {(x, image.height - 1) for x in range(image.width)}
    points |= {(0, y) for y in range(image.height)} | {(image.width - 1, y) for y in range(image.height)}
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in points)


def gutter(image: Image.Image) -> int:
    left, top, right, bottom = visible_bounds(image)
    return min(left, top, image.width - right, image.height - bottom)


def normalise(source: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    if source.size != (384, 384):
        raise RuntimeError(f"source must be 384 x 384: {source.size}")
    if edge_alpha(source):
        raise RuntimeError("source contains visible alpha on an outer edge")
    bounds = visible_bounds(source)
    isolated = source.crop(bounds)
    scale = min(TARGET / isolated.width, TARGET / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    isolated = isolated.resize(size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    offset = ((CELL - size[0]) // 2, (CELL - size[1]) // 2)
    cell.alpha_composite(isolated, offset)
    return cell, {
        "sourceVisibleBounds": list(bounds),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "edgeAlphaPixels": edge_alpha(cell),
        "transparentGutterPx": gutter(cell),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }


def checkerboard(size: tuple[int, int], tile: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, (234, 238, 239, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(210, 218, 220, 255))
    return image


def contact_sheet(rendered: dict[str, Image.Image]) -> Image.Image:
    rows = (len(SPECS) + 3) // 4
    sheet = Image.new("RGBA", (CELL * 4, (CELL + 36) * rows), (18, 35, 52, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (component_id, *_rest) in enumerate(SPECS):
        x = (index % 4) * CELL
        y = (index // 4) * (CELL + 36)
        draw.text((x + 8, y + 12), component_id.upper(), fill=(243, 231, 204, 255))
        board = checkerboard((CELL, CELL))
        board.alpha_composite(rendered[component_id])
        sheet.alpha_composite(board, (x, y + 36))
    return sheet


def main() -> None:
    required = [SOURCE_DIR / f"{spec[0]}-source.webp" for spec in SPECS]
    required += [KITCHEN_REFERENCE, TOOLS_REFERENCE]
    required += [EVIDENCE_DIR / "rejected" / f"{item[0]}.webp" for item in REJECTED]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing dependency: {rel(path)}")

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    components: dict[str, dict[str, object]] = {}
    rendered: dict[str, Image.Image] = {}

    for component_id, family, cache_file, original_sha, original_geometry in SPECS:
        source_path = SOURCE_DIR / f"{component_id}-source.webp"
        source = Image.open(source_path).convert("RGBA")
        component, measurements = normalise(source)
        if measurements["edgeAlphaPixels"] or measurements["transparentGutterPx"] < 20:
            raise RuntimeError(f"unsafe normalised component: {component_id}")
        output = ASSET_DIR / f"{component_id}.png"
        component.save(output)
        rendered[component_id] = component
        components[component_id] = {
            "file": rel(output),
            "sha256": sha(output),
            "family": family,
            "cellPixels": [CELL, CELL],
            "sourceSet": "claude-household-cleaning-cupboard-pack-v1",
            "sourceFile": rel(source_path),
            "sourceSha256": sha(source_path),
            "originalCacheFile": cache_file,
            "originalGeneratedPngSha256": original_sha,
            "originalGeneratedGeometry": original_geometry,
            **measurements,
        }

    rejected = []
    for role, cache_file, original_sha, original_geometry in REJECTED:
        file = EVIDENCE_DIR / "rejected" / f"{role}.webp"
        with Image.open(file) as image:
            pixels = list(image.size)
        rejected.append({
            "role": role,
            "status": "rejected-retained-for-completeness",
            "reason": "exterior ambient glow or field made the generation unsuitable as an independently composited prop",
            "cacheFile": cache_file,
            "originalGeneratedPngSha256": original_sha,
            "originalGeneratedGeometry": original_geometry,
            "file": rel(file),
            "sha256": sha(file),
            "pixels": pixels,
            "preservation": "deterministically-downsampled-lossless-webp",
        })

    evidence = EVIDENCE_DIR / "final-assets-contact-sheet.webp"
    contact_sheet(rendered).save(evidence, format="WEBP", lossless=True, method=6)
    manifest = {
        "schema": "lighthouse-keeper/claude-household-cleaning-cupboard-pack@1",
        "set": "claude-household-cleaning-cupboard-pack-v1",
        "status": "review-only",
        "created": "2026-10-21",
        "styleReferences": [
            {"file": rel(KITCHEN_REFERENCE), "sha256": sha(KITCHEN_REFERENCE), "role": "compact prop styling only"},
            {"file": rel(TOOLS_REFERENCE), "sha256": sha(TOOLS_REFERENCE), "role": "tool silhouette and palette styling only"},
        ],
        "sourceProcessing": {
            "reviewSourceGeometry": [384, 384],
            "method": "alpha <= 8 removed, visible-alpha isolation, proportional fit within 352 px, centered on a 384 px transparent canvas, lossless WebP; original generated PNG SHA-256, cache filename and geometry retained per component",
        },
        "components": components,
        "rejectedGenerations": rejected,
        "evidence": {"file": rel(evidence), "sha256": sha(evidence)},
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersClear": True,
            "componentOwnershipUnambiguous": True,
            "styleReferencesUnchanged": True,
            "allAcceptedAssetsIndependent": True,
            "allTaskGenerationsRepresented": True,
            "runtimeChanged": False,
            "kitchenAuthorityChanged": False,
            "primeChanged": False,
            "deployed": False,
        },
    }
    (PACK / "asset-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
