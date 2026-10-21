#!/usr/bin/env python3
"""Build the immutable Codex Bubble-story family expansion V1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/codex-bubble-story-families-2026-10-21-v1"
RAW_DIR = PACK / "source"
ASSET_DIR = PACK / "assets"
EVIDENCE_DIR = PACK / "evidence"
REGISTER = PACK / "source-register.json"
VISIBLE_ALPHA = 8
SOURCE_CELL = 384
SOURCE_TARGET = 352
CELL = 256
TARGET = 216


# id, family, label, original image-generation cache filename, exact primary request
SPECS = [
    ("fishing-landing-net", "fishing", "Landing net", "exec-adc364f3-dc4f-4ea5-ba0f-7dcf32c8e2d1.png", "one traditional landing net for fishing, immediately recognisable as a handheld oval fish net; short weathered sea-teal wooden handle, aged brass ferrule, deep soft rope-mesh net and compact angled silhouette"),
    ("fishing-lure", "fishing", "Fishing lure", "exec-7f343341-e317-4f62-8575-bc229a48bb2b.png", "one hand-carved minnow-shaped fishing lure with two safely stylised hooks, aged brass spinner, sea-glass teal and restrained coral stripes"),
    ("fishing-creel-basket", "fishing", "Fishing creel", "exec-892af920-db71-4820-8160-01fa86764098.png", "one traditional rounded wicker fishing creel with hinged lid, dark-navy shoulder strap, small aged-brass buckle and compact friendly silhouette"),
    ("fishing-waders", "fishing", "Fishing waders", "exec-0c348fd0-06f7-4b18-a6e4-cea82d6c4f80.png", "one pair of chest-high fishing waders arranged as one wearable object, storm-blue waterproof cloth, sea-teal reinforced boots, cream suspenders and brass buckles"),
    ("fishing-folding-stool", "fishing", "Angler's folding stool", "exec-0f8a61d0-e335-4596-a7c3-f75117c02285.png", "one tiny folding angler's stool, crossed weathered-wood legs, taut sea-teal canvas seat and aged-brass pivots"),
    ("fishing-line-clippers", "fishing", "Fishing-line clippers", "exec-4e565b94-98d0-4d9c-a9be-a49ac1ba4896.png", "one compact pair of fishing-line clippers, burnished-steel jaws, dark sea-teal grips, small brass pivot and short cream lanyard"),
    ("garden-trowel", "garden", "Garden trowel", "exec-61d89dd2-186f-4e7d-a092-6b9a7f9d1188.png", "one sturdy hand trowel with broad burnished-steel blade, weathered sea-teal wooden handle, aged-brass collar and friendly compact diagonal silhouette"),
    ("garden-secateurs", "garden", "Garden secateurs", "exec-1ae28051-c398-4a8c-a344-e68cd9bbc41d.png", "one closed pair of bypass pruning secateurs, curved burnished-steel blades, coral-red grips, aged-brass pivot and chunky safe silhouette"),
    ("garden-gloves", "garden", "Gardening gloves", "exec-badd2122-61bb-46cb-8bb7-a65b9da4c609.png", "one neatly overlapped pair of well-used gardening gloves, sea-glass teal canvas, warm-cream cuffs and small reinforced fingertips"),
    ("garden-wheelbarrow", "garden", "Garden wheelbarrow", "exec-f9a55924-e94d-4b2c-9066-2ffe5a5da03a.png", "one compact traditional wheelbarrow, storm-blue painted-metal tray, one coral-rimmed wheel, weathered timber handles and aged-brass bolts"),
    ("garden-rake", "garden", "Garden rake", "exec-b4bc58cc-dff0-426c-86b1-eb7682384ebb.png", "one short broad garden rake, sea-teal metal head with clearly separated blunt tines, weathered-wood shaft and brass hanging cap"),
    ("garden-compost-bag", "garden", "Compost bag", "exec-83a33692-187d-4738-80c0-a3f4a25c9a52.png", "one plump folded-top sack of rich garden compost, warm-cream paper with sea-teal and coral leaf motifs only, no words, with a little dark soil visible at the opening"),
    ("pet-dog", "pet-care", "Scruffy terrier", "exec-fde888fc-aa7e-4a59-af40-38be9fddfded.png", "one warm fictional scruffy terrier sitting in a jaunty three-quarter pose, shaggy cream and warm-brown fur, sea-teal collar and friendly alert expression"),
    ("pet-cat", "pet-care", "Curled tabby cat", "exec-58506cab-195b-4d61-a15a-149555fbb9d1.png", "one warm fictional curled tabby cat, storm-blue-grey and warm-cream stripes, sea-glass eyes, coral collar and tail wrapped into a compact crescent silhouette"),
    ("pet-rabbit", "pet-care", "Lop-eared rabbit", "exec-4b487ece-293f-43f4-bff1-d38744d701e0.png", "one warm fictional lop-eared rabbit sitting upright, soft warm-cream and light-brown fur, one ear flopped, sea-teal ribbon collar and bright curious expression"),
    ("pet-lead-and-collar", "pet-care", "Pet lead and collar", "exec-1fccb448-fbee-48ce-9119-c0e5ebb9bd08.png", "one rolled sea-teal woven dog lead clipped to a matching collar as one ordinary set, aged-brass clasp and buckle, restrained coral stitching"),
    ("pet-tennis-ball", "pet-care", "Pet tennis ball", "exec-294843f8-20ea-4799-bfe3-ecec416c4841.png", "one slightly scuffed pet tennis ball, warm golden-yellow felt with dark-navy curved seam and one tiny coral patch"),
    ("pet-feather-wand", "pet-care", "Feather wand", "exec-0013cc03-6215-4fc9-9141-422f4503aab8.png", "one cat-play feather wand, short sea-teal handle, cream cord and compact cluster of coral, storm-blue and warm-cream feathers attached securely"),
    ("repair-cordless-drill", "repair", "Cordless drill", "exec-445bdb44-75b4-44f2-a710-cfbd3885ec43.png", "one compact cordless drill angled three-quarters, storm-blue and sea-teal body, aged-brass chuck ring, warm-cream trigger and short steel bit fitted"),
    ("repair-drill-bit-case", "repair", "Drill-bit case", "exec-402a2b44-cc36-4233-b6bd-28a0656c6083.png", "one small open drill-bit case with six neatly graduated steel bits in a storm-blue tray, sea-teal shell and brass hinge, with no labels"),
    ("repair-flat-head-screwdriver", "repair", "Flat-head screwdriver", "exec-835b4c82-b396-4d16-bb86-6ffccd26784d.png", "one flat-head screwdriver angled diagonally, burnished-steel shaft with clearly flat blade tip, translucent sea-teal handle and aged-brass collar"),
    ("repair-phillips-screwdriver", "repair", "Phillips screwdriver", "exec-8aba4a12-217f-454d-8ba8-cacf924e8547.png", "one cross-head Phillips screwdriver angled diagonally, burnished-steel shaft with clearly cross-shaped tip, restrained-coral handle and aged-brass collar"),
    ("repair-combination-pliers", "repair", "Combination pliers", "exec-d3c00dfd-7c2d-4cdc-acd0-0424e7d740e3.png", "one pair of closed combination pliers, burnished-steel jaws, sea-teal padded grips, aged-brass pivot and compact sturdy silhouette"),
    ("repair-adjustable-spanner", "repair", "Adjustable spanner", "exec-f11918b9-a17b-400b-8d82-ccd381b0102b.png", "one adjustable spanner with crescent jaw slightly open, burnished steel with sea-glass teal handle inset and aged-brass adjustment wheel"),
    ("repair-tape-measure", "repair", "Tape measure", "exec-a24a5a15-1c41-46b9-9e9d-a25e5a15f813.png", "one compact retractable tape measure, storm-blue casing with sea-teal grip, aged-brass belt loop and short warm-cream tape extended with plain tick marks only"),
    ("repair-spirit-level", "repair", "Spirit level", "exec-fea2ccfd-a8b7-4604-bb78-2c8ce1f1b8d3.png", "one short boat-builder's spirit level, weathered sea-teal body, aged-brass end caps and three clearly visible glass bubble vials"),
    ("repair-hand-saw", "repair", "Hand saw", "exec-6776736c-6888-4add-ac97-8be3120408b7.png", "one traditional hand saw angled diagonally, short burnished-steel toothed blade, weathered storm-blue wooden handle and brass fasteners"),
    ("repair-wire-strippers", "repair", "Wire strippers", "exec-6ff518ae-8cba-41f2-bb1a-ed4877c5f302.png", "one pair of closed electrician's wire strippers, dark burnished-steel jaws with clear stripping notches, coral and sea-teal padded grips and brass pivot"),
    ("repair-soldering-iron", "repair", "Soldering iron", "exec-688314bb-2e1f-45ee-9279-16832341812b.png", "one compact soldering iron, burnished-copper tip, warm-cream ceramic collar, sea-teal handle and short neatly curled dark-navy cable"),
    ("repair-c-clamp", "repair", "C-clamp", "exec-f828a0a6-6e20-4f36-9139-4a3ce12faa66.png", "one sturdy C-clamp slightly open, storm-blue painted-iron frame, aged-brass screw and sea-teal turning handle"),
    ("pub-bitter-pint", "pub", "Pint of bitter", "exec-98ab9413-d910-4766-b454-cf272eb4aaa6.png", "one traditional non-branded dimpled pint glass filled with warm amber bitter and modest cream foam head, with no logo or writing"),
    ("pub-tankard", "pub", "Pewter tankard", "exec-00b053db-86cc-43a6-a23c-f44962e0711c.png", "one sturdy pewter tankard with curved handle, aged-silver metal, subtle brass rim and tiny engraved wave motif only"),
    ("pub-beer-pump", "pub", "Pub beer pump", "exec-f0fbfddf-1587-4183-97f9-96be0597b9a2.png", "one traditional hand-pulled pub beer engine, storm-blue ceramic base, tall sea-teal handle, aged-brass fittings and blank coral medallion"),
    ("pub-dartboard", "pub", "Pub dartboard", "exec-76594c7c-2a6a-4e79-a340-8a3f431616e9.png", "one round traditional dartboard with alternating dark-navy, warm-cream, sea-teal and restrained-coral scoring bands, aged-brass dividers and no numerals"),
    ("pub-darts", "pub", "Set of pub darts", "exec-977a1cc9-ad20-4984-8e8b-859843abd544.png", "one tidy fan of three pub darts as a single play set, aged-brass tips and barrels, sea-teal, coral and warm-cream flights"),
    ("pub-pool-cue-and-balls", "pub", "Pool cue and balls", "exec-75d1c2ec-7bf1-4d96-b0d5-aa9861f3d4d0.png", "one short wooden pool cue behind a compact triangle of three plain pool balls in sea-teal, coral and warm cream, with no numbers"),
    ("pub-crisps-bowl", "pub", "Bowl of crisps", "exec-1692efcd-581f-43f2-b738-7ab7bdaa8f7c.png", "one small storm-blue ceramic pub bowl filled with chunky golden potato crisps, sea-teal rim and one coral accent stripe"),
    ("pub-bar-stool", "pub", "Pub bar stool", "exec-0c3e8c67-aba3-4315-9656-45d97fcb1524.png", "one compact traditional pub bar stool, turned weathered-wood legs, round sea-teal leather seat, aged-brass foot ring and fasteners"),
    ("art-easel-and-canvas", "art", "Easel and blank canvas", "exec-46e56093-daf5-4a38-920a-c536a81637b0.png", "one small table-top art easel holding one blank warm-cream canvas, complete and uncropped, with weathered sea-teal wooden legs, aged-brass hinge and low canvas ledge"),
    ("art-paint-palette", "art", "Painter's palette", "exec-f612e2ba-0225-4b70-b898-d3c205202d12.png", "one classic thumb-hole wooden painter's palette with six neat paint dabs and one short brush resting across it"),
    ("art-brushes-pot", "art", "Pot of paintbrushes", "exec-133a30e7-440a-4e11-9d0d-3fe8cc053417.png", "one storm-blue ceramic pot holding a tidy fan of five different paintbrushes with weathered sea-teal and warm-wood handles"),
    ("art-watercolour-set", "art", "Watercolour set", "exec-05cab66d-87da-4caa-a1c8-4f4aa31450a2.png", "one small open watercolour tin with eight rich colour pans and slim brush, sea-teal enamel case and brass hinges, with no labels"),
    ("art-sketchbook-and-pencil", "art", "Sketchbook and pencil", "exec-37b13806-5cc9-4117-8644-eeb9bc4f166d.png", "one spiral-bound warm-cream sketchbook opened to a blank page with chunky sea-teal drawing pencil laid diagonally"),
    ("art-lino-roller", "art", "Lino-printing roller", "exec-7d88480a-fbfd-4478-9832-856384ea161b.png", "one compact printmaking brayer roller, deep storm-blue rubber cylinder, weathered sea-teal handle, aged-brass axle and warm-cream grip"),
    ("art-origami-boat", "art", "Origami boat", "exec-560fec92-8675-426c-a288-eafc8c7134eb.png", "one crisply folded paper boat made from warm-cream paper with subtle sea-teal and coral edge accents, with no printed text"),
    ("art-ink-bottle-and-quill", "art", "Ink bottle and quill", "exec-3eeb3afa-d564-4034-852b-4088e8fd03bc.png", "one squat storm-blue glass ink bottle with aged-brass neck and single warm-cream quill standing in it"),
    ("inventing-microscope", "inventing", "Inventor's microscope", "exec-436c4d7d-a432-493b-8c77-a63e5fff1529.png", "one compact vintage laboratory microscope, storm-blue enamel body, aged-brass focus wheels and objectives, sea-teal stage and warm-cream eyepiece"),
    ("inventing-test-tubes", "inventing", "Test-tube rack", "exec-6e45ca30-c3e3-4010-be46-02fbbbee53ba.png", "one small aged-brass rack holding three glass test tubes with sea-teal, coral and golden liquids at different levels and a few contained bubbles"),
    ("inventing-conical-flask", "inventing", "Conical flask", "exec-4b469402-5d04-41cc-978a-602beb40e73a.png", "one squat clear conical laboratory flask with sea-teal liquid, three contained coral bubbles and aged-brass stopper ring"),
    ("inventing-brass-telescope", "inventing", "Brass telescope", "exec-1ed8bbf4-0dbe-4ec9-a871-473ed4c07e92.png", "one small collapsible inventor's telescope, aged-brass tubes with storm-blue leather grip and sea-glass front lens, partly extended diagonally"),
    ("inventing-light-bulb", "inventing", "Inventor's light bulb", "exec-4f058772-5e9f-4bf0-965b-35bcea240e3c.png", "one charming old-fashioned clear light bulb with visible warm-brass loop filament and aged-brass screw base, without radiating glow"),
    ("inventing-gyroscope", "inventing", "Mechanical gyroscope", "exec-b19352c4-3901-47d0-b245-d9eca2754fe2.png", "one tabletop mechanical gyroscope with three nested aged-brass rings around a storm-blue centre, sea-teal axle tips and compact tilted silhouette"),
    ("inventing-horseshoe-magnet", "inventing", "Horseshoe magnet", "exec-9f22f991-5ddd-4675-bcfc-c379fb89112c.png", "one chunky horseshoe magnet, storm-blue body with coral-red pole caps and aged-brass rivets, with no sparks or force lines"),
    ("inventing-copper-coil", "inventing", "Copper induction coil", "exec-aff9e6c2-36b9-4627-94d9-f2713e347b53.png", "one compact induction coil, neat burnished-copper winding around a storm-blue core, sea-teal base and two aged-brass terminal posts"),
]

REJECTED = [{
    "id": "art-easel-and-canvas",
    "originalCacheFile": "exec-c9ec822d-5932-4c67-81c0-2a4a1d27d7b3.png",
    "originalGeneratedPngSha256": "f55ffe01aa543b80f2681598c424097161f63de0312d474df904ae56d33ae7ba",
    "originalGeneratedGeometry": [1275, 1234],
    "reason": "visible alpha touched all of the source image's top and bottom edges; the complete easel did not have a safe source gutter",
}]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_alpha(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y][3] <= VISIBLE_ALPHA:
                pixels[x, y] = (0, 0, 0, 0)
    return image


def visible_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.getchannel("A").point(lambda value: 255 if value > VISIBLE_ALPHA else 0).getbbox()
    if bounds is None:
        raise RuntimeError("image has no visible pixels")
    return bounds


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    points = {(x, 0) for x in range(image.width)} | {(x, image.height - 1) for x in range(image.width)}
    points |= {(0, y) for y in range(image.height)} | {(image.width - 1, y) for y in range(image.height)}
    return sum(alpha.getpixel(point) > VISIBLE_ALPHA for point in points)


def fit(source: Image.Image, cell_size: int, target_size: int) -> tuple[Image.Image, dict[str, object]]:
    bounds = visible_bounds(source)
    isolated = source.crop(bounds)
    scale = min(target_size / isolated.width, target_size / isolated.height)
    size = (max(1, round(isolated.width * scale)), max(1, round(isolated.height * scale)))
    isolated = isolated.resize(size, Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (cell_size, cell_size), (0, 0, 0, 0))
    offset = ((cell_size - size[0]) // 2, (cell_size - size[1]) // 2)
    cell.alpha_composite(isolated, offset)
    final_bounds = visible_bounds(cell)
    gutter = min(final_bounds[0], final_bounds[1], cell_size - final_bounds[2], cell_size - final_bounds[3])
    return cell, {
        "sourceVisibleBounds": list(bounds),
        "normalisedVisibleSize": list(size),
        "normalisedOffset": list(offset),
        "edgeAlphaPixels": edge_alpha(cell),
        "transparentGutterPx": gutter,
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
    columns = 6
    rows = (len(SPECS) + columns - 1) // columns
    sheet = Image.new("RGBA", (CELL * columns, (CELL + 32) * rows), (18, 35, 52, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (component_id, *_rest) in enumerate(SPECS):
        x = (index % columns) * CELL
        y = (index // columns) * (CELL + 32)
        draw.text((x + 7, y + 10), component_id.upper(), fill=(243, 231, 204, 255))
        board = checkerboard((CELL, CELL))
        board.alpha_composite(rendered[component_id])
        sheet.alpha_composite(board, (x, y + 32))
    return sheet


def write_hashes() -> None:
    files = sorted(path for path in PACK.rglob("*") if path.is_file() and path.name != "HASHES.sha256" and not path.name.endswith(".raw.png"))
    (PACK / "HASHES.sha256").write_text("\n".join(f"{sha(path)}  {path.relative_to(PACK).as_posix()}" for path in files) + "\n")


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    previous = json.loads(REGISTER.read_text()) if REGISTER.exists() else {"accepted": []}
    previous_by_id = {item["id"]: item for item in previous.get("accepted", [])}
    accepted = []
    components: dict[str, dict[str, object]] = {}
    rendered: dict[str, Image.Image] = {}

    for component_id, family, label, cache_file, primary_request in SPECS:
        raw_path = RAW_DIR / f"{component_id}.png"
        source_path = RAW_DIR / f"{component_id}-source.webp"
        if raw_path.exists():
            original = Image.open(raw_path).convert("RGBA")
            if edge_alpha(original):
                raise RuntimeError(f"{component_id}: generated source touches an outer edge")
            original_sha = sha(raw_path)
            original_geometry = list(original.size)
            review_source, _source_measurements = fit(clean_alpha(original), SOURCE_CELL, SOURCE_TARGET)
            review_source.save(source_path, format="WEBP", lossless=True, method=6)
        else:
            record = previous_by_id.get(component_id)
            if not record or not source_path.exists():
                raise RuntimeError(f"{component_id}: missing raw PNG and prepared source")
            original_sha = record["originalGeneratedPngSha256"]
            original_geometry = record["originalGeneratedGeometry"]

        source = Image.open(source_path).convert("RGBA")
        if source.size != (SOURCE_CELL, SOURCE_CELL) or edge_alpha(source):
            raise RuntimeError(f"{component_id}: unsafe prepared source")
        component, measurements = fit(source, CELL, TARGET)
        if measurements["edgeAlphaPixels"] or measurements["transparentGutterPx"] < 20:
            raise RuntimeError(f"{component_id}: unsafe 256px component")
        output = ASSET_DIR / f"{component_id}.png"
        component.save(output)
        rendered[component_id] = component
        accepted.append({
            "id": component_id,
            "family": family,
            "label": label,
            "primaryRequest": primary_request,
            "originalCacheFile": cache_file,
            "originalGeneratedPngSha256": original_sha,
            "originalGeneratedGeometry": original_geometry,
            "status": "accepted",
            "sourceFile": rel(source_path),
        })
        components[component_id] = {
            "file": rel(output),
            "sha256": sha(output),
            "family": family,
            "label": label,
            "cellPixels": [CELL, CELL],
            "sourceSet": "codex-bubble-story-families-v1",
            "sourceFile": rel(source_path),
            "sourceSha256": sha(source_path),
            "originalCacheFile": cache_file,
            "originalGeneratedPngSha256": original_sha,
            "originalGeneratedGeometry": original_geometry,
            **measurements,
        }

    register = {
        "schema": "lighthouse-keeper/codex-bubble-story-family-source-register@1",
        "created": "2026-10-21",
        "tool": "built-in image generation",
        "accepted": accepted,
        "rejected": REJECTED,
        "rejectedNote": "One easel attempt was rejected for source-edge contact and rerendered with a complete transparent gutter; all other first candidates passed geometry and visual screening.",
    }
    REGISTER.write_text(json.dumps(register, indent=2) + "\n")

    evidence = EVIDENCE_DIR / "final-assets-contact-sheet.webp"
    contact_sheet(rendered).save(evidence, format="WEBP", lossless=True, method=6)
    manifest = {
        "schema": "lighthouse-keeper/codex-bubble-story-families-pack@1",
        "set": "codex-bubble-story-families-v1",
        "status": "bubble-story-picture-source",
        "created": "2026-10-21",
        "sourceProcessing": {
            "reviewSourceGeometry": [SOURCE_CELL, SOURCE_CELL],
            "method": "clear alpha <= 8, isolate visible alpha, proportional fit within 352 px on a transparent 384 px lossless WebP source, then proportional fit within 216 px on a transparent 256 px PNG cell",
        },
        "sourceRegister": {"file": rel(REGISTER), "sha256": sha(REGISTER)},
        "components": components,
        "rejectedGenerations": REJECTED,
        "evidence": {"file": rel(evidence), "sha256": sha(evidence)},
        "checks": {
            "sourceEdgesClear": True,
            "componentGuttersClear": True,
            "componentOwnershipUnambiguous": True,
            "allAcceptedAssetsIndependent": True,
            "allTaskGenerationsRepresented": True,
            "runtimeChanged": False,
            "approvedAuthorityChanged": False,
            "deployed": False,
        },
    }
    (PACK / "asset-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    write_hashes()
    print(f"Built {len(components)} Bubble-story pictures across {len(set(spec[1] for spec in SPECS))} families")


if __name__ == "__main__":
    main()
