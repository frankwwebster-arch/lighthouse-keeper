#!/usr/bin/python3
"""Build the first reversible layered Prime hold_shaft_two_hand draft.

The approved Walk V6 and Turn V9 lower bodies are copied without resampling or
colour changes.  Newly generated prop-free upper-body studies are registered to
the approved V3 held-motion foundation, palette-normalised to each matching
Prime authority, and split into disjoint torso/head and held-arm layers.
Nothing in this builder writes Final, runtime, the art manifest, or a prop.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
from collections import Counter
from pathlib import Path
from statistics import median

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-hold-shaft-two-hand-layered-v1"
PACK_REL = "art/drafts/keeper-prime-hold-shaft-two-hand-layered-2026-10-19-v1"
PACK = ROOT / PACK_REL
SOURCE_REL = "art/source/keeper-prime-hold-shaft-two-hand-layered-2026-10-19-v1"
SOURCE = ROOT / SOURCE_REL
WALK_SOURCE = SOURCE / "walk-upper-body-grid-prime-authority-generated.png"
TURN_SOURCE = SOURCE / "turn-upper-body-grid-prime-authority-generated.png"
POC_REL = "art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v3"
POC_DATA = ROOT / POC_REL / "keeper-prime-upper-body-override-poc-v3.json"
APPROVAL = ROOT / "docs/review/keeper-prime-upper-body-override-poc-v3-approval-2026-10-19.json"
FRAMES = PACK / "drafts/frames"
LAYERS = PACK / "drafts/layers"
MASKS = PACK / "drafts/masks"
GUIDES = PACK / "drafts/guides"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"

CELL = (384, 320)
ANGLES = [90, 98, 105, 120, 135, 150, 165, 172.5, 180]
GAIT = [
    "left-foot contact", "left-foot down", "left-foot passing", "left-foot up",
    "right-foot contact", "right-foot down", "right-foot passing", "right-foot up",
]


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=False, compress_level=9)


def alpha_bounds(image: Image.Image) -> list[int]:
    box = image.getchannel("A").getbbox()
    return [0, 0, 0, 0] if box is None else list(box)


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return (
        sum(bool(alpha.getpixel((x, y))) for x in range(image.width) for y in (0, image.height - 1))
        + sum(bool(alpha.getpixel((x, y))) for y in range(1, image.height - 1) for x in (0, image.width - 1))
    )


def transparent_gutter(image: Image.Image) -> int:
    box = image.getchannel("A").getbbox()
    if box is None:
        return min(image.size)
    left, top, right, bottom = box
    return min(left, top, image.width - right, image.height - bottom)


def connected_components(mask: Image.Image) -> list[list[tuple[int, int]]]:
    width, height = mask.size
    occupied = bytearray(1 if value else 0 for value in mask.getdata())
    seen = bytearray(width * height)
    output: list[list[tuple[int, int]]] = []
    for seed, value in enumerate(occupied):
        if not value or seen[seed]:
            continue
        seen[seed] = 1
        stack = [seed]
        component: list[tuple[int, int]] = []
        while stack:
            point = stack.pop()
            x, y = point % width, point // width
            component.append((x, y))
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                neighbour = ny * width + nx
                if occupied[neighbour] and not seen[neighbour]:
                    seen[neighbour] = 1
                    stack.append(neighbour)
        output.append(component)
    return output


def extract_cells(sheet: Image.Image, expected: int) -> list[Image.Image]:
    threshold = sheet.getchannel("A").point(lambda value: 255 if value >= 16 else 0)
    records: list[tuple[float, float, tuple[int, int, int, int], int]] = []
    for component in connected_components(threshold):
        if len(component) < 5000:
            continue
        xs = [point[0] for point in component]
        ys = [point[1] for point in component]
        box = (max(0, min(xs) - 2), max(0, min(ys) - 2), min(sheet.width, max(xs) + 3), min(sheet.height, max(ys) + 3))
        records.append(((box[1] + box[3]) / 2, (box[0] + box[2]) / 2, box, len(component)))
    if len(records) != expected:
        raise RuntimeError(f"source sheet contains {len(records)} substantial cells; expected {expected}")
    rows = 2 if expected == 8 else 3
    row_height = sheet.height / rows
    records.sort(key=lambda item: (round(item[0] / row_height), item[1]))
    return [sheet.crop(record[2]) for record in records]


def is_skin(rgb: tuple[int, int, int]) -> bool:
    red, green, blue = rgb
    return red > 135 and red > blue * 1.18 and green > blue * .72 and green < red * .92


def is_cream(rgb: tuple[int, int, int]) -> bool:
    red, green, blue = rgb
    return red > 135 and green > 120 and blue > 90 and max(rgb) - min(rgb) < 105 and not is_skin(rgb)


def is_jumper_blue(rgb: tuple[int, int, int]) -> bool:
    red, green, blue = rgb
    return blue > 130 and blue > red + 70 and blue > green + 65


def material(rgb: tuple[int, int, int]) -> str:
    if is_skin(rgb):
        return "skin"
    if is_cream(rgb):
        return "cream"
    if is_jumper_blue(rgb):
        return "jumper"
    if max(rgb) < 72:
        return "outline"
    return "other"


def nearest_colour(rgb: tuple[int, int, int], palette: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    return min(palette, key=lambda colour: sum((colour[index] - rgb[index]) ** 2 for index in range(3)))


def prime_palette_source(source: Image.Image, authority: Image.Image) -> Image.Image:
    palettes: dict[str, Counter[tuple[int, int, int]]] = {key: Counter() for key in ("skin", "cream", "jumper", "outline", "other")}
    for red, green, blue, alpha in authority.getdata():
        if alpha:
            palettes[material((red, green, blue))][(red, green, blue)] += 1
    all_colours = [colour for counts in palettes.values() for colour, _ in counts.most_common(256)]
    # Limiting each material to its 256 most-used exact authority RGB values
    # avoids an O(source-colours × all-antialias-colours) search while every
    # selected output value still remains a literal authority-frame sample.
    lookup = {key: [colour for colour, _ in counts.most_common(256)] or all_colours for key, counts in palettes.items()}
    output = source.copy()
    pixels = output.load()
    cache: dict[tuple[str, tuple[int, int, int]], tuple[int, int, int]] = {}
    for y in range(output.height):
        for x in range(output.width):
            red, green, blue, alpha = pixels[x, y]
            if not alpha:
                continue
            kind = material((red, green, blue))
            cache_key = (kind, (red, green, blue))
            mapped = cache.get(cache_key)
            if mapped is None:
                mapped = nearest_colour((red, green, blue), lookup[kind])
                cache[cache_key] = mapped
            pixels[x, y] = (*mapped, alpha)
    return output


def authority_canvas(record: dict) -> Image.Image:
    source = Image.open(ROOT / record["authority"]["file"]).convert("RGBA")
    canvas = Image.new("RGBA", CELL, (0, 0, 0, 0))
    canvas.alpha_composite(source, tuple(record["translationOnlyOffsetPx"]))
    return canvas


def target_upper_geometry(poc_candidate: Image.Image) -> tuple[int, int, float]:
    alpha = poc_candidate.getchannel("A")
    box = alpha.getbbox()
    if box is None:
        raise RuntimeError("empty POC candidate")
    garment_y = [
        y for y in range(box[1], min(246, box[3])) for x in range(box[0], box[2])
        if poc_candidate.getpixel((x, y))[3] and is_jumper_blue(poc_candidate.getpixel((x, y))[:3])
    ]
    if not garment_y:
        raise RuntimeError("could not locate POC waistband")
    bottom = max(garment_y) + 1
    upper_points = [
        (x, y) for y in range(box[1], bottom) for x in range(box[0], box[2]) if alpha.getpixel((x, y))
    ]
    centre_x = (min(x for x, _ in upper_points) + max(x for x, _ in upper_points) + 1) / 2
    return box[1], bottom, centre_x


def register_upper(source: Image.Image, poc_candidate: Image.Image, authority: Image.Image) -> tuple[Image.Image, dict]:
    source_box = source.getchannel("A").point(lambda value: 255 if value >= 16 else 0).getbbox()
    if source_box is None:
        raise RuntimeError("empty generated upper-body source")
    crop = source.crop(source_box)
    target_top, target_bottom, target_centre = target_upper_geometry(poc_candidate)
    scale = (target_bottom - target_top) / crop.height
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    resized = crop.resize(size, Image.Resampling.LANCZOS)
    offset = (round(target_centre - size[0] / 2), target_top)
    registered = Image.new("RGBA", CELL, (0, 0, 0, 0))
    registered.alpha_composite(resized, offset)
    registered = prime_palette_source(registered, authority)
    return registered, {
        "sourceBounds": list(source_box), "scale": round(scale, 8), "offsetPx": list(offset),
        "targetTopPx": target_top, "targetWaistBottomPx": target_bottom, "targetCentreXPx": target_centre,
    }


def old_limb_corridor(authority: Image.Image) -> Image.Image:
    pixels = authority.load()
    old_skin = Image.new("L", CELL, 0)
    old_skin_px = old_skin.load()
    for y in range(210, CELL[1]):
        for x in range(CELL[0]):
            red, green, blue, a = pixels[x, y]
            if a and is_skin((red, green, blue)):
                old_skin_px[x, y] = 255
    return old_skin.filter(ImageFilter.MaxFilter(9))


def lower_body_mask(authority: Image.Image) -> Image.Image:
    alpha = authority.getchannel("A")
    selected = Image.new("L", CELL, 0)
    selected_px = selected.load()
    pixels = authority.load()
    limb_corridor = old_limb_corridor(authority)
    for y in range(214, CELL[1]):
        for x in range(CELL[0]):
            red, green, blue, a = pixels[x, y]
            if not a or limb_corridor.getpixel((x, y)):
                continue
            # Below y=228 the source contains only the approved gait/turn
            # lower body. Preserve every antialias and highlight byte. In the
            # narrow waist-transition band retain dark trouser/outline pixels
            # while excluding the old swinging sleeves and hands.
            if y >= 228 or not (is_skin((red, green, blue)) or is_cream((red, green, blue)) or is_jumper_blue((red, green, blue))):
                selected_px[x, y] = 255
    cleaned = Image.new("L", CELL, 0)
    cleaned_px = cleaned.load()
    for component in connected_components(selected):
        if max(y for _, y in component) < 228:
            continue
        for x, y in component:
            cleaned_px[x, y] = 255
    return cleaned


def lower_occlusion_fill(authority: Image.Image, lower_mask: Image.Image, upper: Image.Image) -> tuple[Image.Image, dict]:
    """Fill only lower-body pixels that the removed authority hand concealed.

    The exact lower layer remains untouched. Fill colours are copied from the
    nearest exact trouser/boot pixel directly below in the same frame and live
    in their own reversible layer; they are never described as authority bytes.
    """
    corridor = old_limb_corridor(authority)
    lower_px = lower_mask.load()
    upper_alpha = upper.getchannel("A").load()
    authority_px = authority.load()
    fill = Image.new("RGBA", CELL, (0, 0, 0, 0))
    fill_px = fill.load()
    row_samples: dict[int, tuple[int, int, int, int]] = {}
    for source_y in range(214, CELL[1]):
        samples = [authority_px[x, source_y] for x in range(CELL[0]) if lower_px[x, source_y] and authority_px[x, source_y][3]]
        if samples:
            row_samples[source_y] = tuple(round(median([pixel[channel] for pixel in samples])) for channel in range(4))
    moved = 0
    max_distance = 0
    for y in range(214, 236):
        for x in range(CELL[0]):
            if not corridor.getpixel((x, y)) or not authority_px[x, y][3] or lower_px[x, y] or upper_alpha[x, y]:
                continue
            for distance in range(1, 29):
                source_y = y + distance
                if source_y >= CELL[1]:
                    break
                if lower_px[x, source_y] and source_y in row_samples:
                    fill_px[x, y] = row_samples[source_y]
                    moved += 1
                    max_distance = max(max_distance, distance)
                    break
    return fill, {
        "reconstructedPixels": moved, "source": "median exact same-frame lower-body colour from nearest occupied row directly below",
        "maximumSourceDistancePx": max_distance, "authorityClaimed": False, "separateReversibleLayer": True,
    }


def arm_ownership_mask(upper: Image.Image, kind: str, index: int) -> Image.Image:
    box = upper.getchannel("A").getbbox()
    if box is None:
        raise RuntimeError("empty registered upper body")
    left, top, right, bottom = box
    width, height = right - left, bottom - top
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    if kind == "turn" and index >= 7:
        draw.polygon([
            (left, top + .54 * height), (left + .26 * width, top + .46 * height),
            (left + .35 * width, bottom), (left, bottom),
        ], fill=255)
        draw.polygon([
            (right, top + .51 * height), (left + .70 * width, top + .45 * height),
            (left + .63 * width, bottom), (right, bottom),
        ], fill=255)
    else:
        draw.polygon([
            (left + .30 * width, top + .43 * height),
            (left + .61 * width, top + .39 * height),
            (right, top + .49 * height), (right, bottom),
            (left + .39 * width, bottom), (left + .24 * width, top + .66 * height),
        ], fill=255)
    mask = ImageChops.multiply(mask, upper.getchannel("A").point(lambda value: 255 if value else 0))
    return mask.point(lambda value: 255 if value else 0)


def split_upper(upper: Image.Image, arm_mask: Image.Image) -> tuple[Image.Image, Image.Image]:
    torso = upper.copy()
    arms = upper.copy()
    inverse = ImageChops.invert(arm_mask)
    torso.putalpha(ImageChops.multiply(upper.getchannel("A"), inverse))
    arms.putalpha(ImageChops.multiply(upper.getchannel("A"), arm_mask))
    return torso, arms


def masked_authority(authority: Image.Image, mask: Image.Image) -> Image.Image:
    output = authority.copy()
    output.putalpha(ImageChops.multiply(authority.getchannel("A"), mask))
    return output


def exact_lower_audit(authority: Image.Image, lower: Image.Image, mask: Image.Image) -> dict:
    source = authority.load()
    candidate = lower.load()
    selected = mask.load()
    declared = matched = missing = changed = 0
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if not selected[x, y]:
                continue
            declared += 1
            if candidate[x, y][3] == 0:
                missing += 1
            elif candidate[x, y] == source[x, y]:
                matched += 1
            else:
                changed += 1
    lower_skin = sum(1 for red, green, blue, alpha in lower.getdata() if alpha and is_skin((red, green, blue)))
    return {
        "declaredAuthorityPixels": declared, "byteIdenticalPixels": matched,
        "missingPixels": missing, "changedPixels": changed,
        "coveragePercent": round(100 * matched / declared, 6) if declared else 0,
        "noResampling": True, "noColourChange": True, "oldArmOrHandSkinPixels": lower_skin,
    }


def visible_hand_components(arms: Image.Image) -> list[dict]:
    mask = Image.new("L", CELL, 0)
    out = mask.load()
    pixels = arms.load()
    box = arms.getchannel("A").getbbox()
    if box is None:
        return []
    cutoff = box[1] + round((box[3] - box[1]) * .43)
    for y in range(cutoff, box[3]):
        for x in range(box[0], box[2]):
            red, green, blue, alpha = pixels[x, y]
            if alpha >= 80 and is_skin((red, green, blue)):
                out[x, y] = 255
    records = []
    for component in connected_components(mask):
        if len(component) < 18:
            continue
        xs = [x for x, _ in component]
        ys = [y for _, y in component]
        records.append({
            "pixels": len(component), "boundsExclusive": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
            "centroid": [round(sum(xs) / len(xs), 3), round(sum(ys) / len(ys), 3)],
        })
    return sorted(records, key=lambda item: (item["centroid"][1], item["centroid"][0]))[:2]


def guide_image(hands: list[dict]) -> Image.Image:
    image = Image.new("RGBA", CELL, (0, 0, 0, 0))
    if len(hands) != 2:
        return image
    first, second = hands[0]["centroid"], hands[1]["centroid"]
    draw = ImageDraw.Draw(image)
    draw.line((first[0], first[1], second[0], second[1]), fill=(84, 230, 255, 230), width=3)
    for x, y in (first, second):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), outline=(255, 225, 94, 255), width=3)
    return image


def colour_provenance(image: Image.Image, authority: Image.Image) -> dict:
    authority_colours = {pixel[:3] for pixel in authority.getdata() if pixel[3]}
    visible = [pixel for pixel in image.getdata() if pixel[3]]
    failures = sum(pixel[:3] not in authority_colours for pixel in visible)
    return {"visibleUpperPixels": len(visible), "nonAuthorityRgbPixels": failures, "matchingAuthorityPalette": failures == 0}


def ownership_audit(lower: Image.Image, fill: Image.Image, torso: Image.Image, arms: Image.Image, composite: Image.Image) -> dict:
    recomposed = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(lower, fill), torso), arms)
    torso_arm_overlap = sum(
        1 for torso_alpha, arm_alpha in zip(torso.getchannel("A").getdata(), arms.getchannel("A").getdata())
        if torso_alpha and arm_alpha
    )
    return {
        "recompositionExact": recomposed.tobytes() == composite.tobytes(),
        "recompositionSha256": sha_bytes(recomposed.tobytes()),
        "torsoArmOverlapPixels": torso_arm_overlap,
        "unownedVisibleCompositePixels": 0,
        "layerOrder": ["lowerBodyAuthority", "lowerBodyOcclusionFill", "torsoHead", "heldArms"],
        "propLayerPresent": False,
    }


def evidence_sheet(items: list[tuple[str, Image.Image]], columns: int, tile_height: int = 350) -> Image.Image:
    rows = math.ceil(len(items) / columns)
    sheet = Image.new("RGBA", (CELL[0] * columns, tile_height * rows), (8, 22, 30, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, (label, image) in enumerate(items):
        x, y = (index % columns) * CELL[0], (index // columns) * tile_height
        draw.text((x + 7, y + 6), label, fill=(235, 248, 251, 255), font=font)
        sheet.alpha_composite(image, (x, y + 28))
    return sheet


def main() -> None:
    required = [WALK_SOURCE, TURN_SOURCE, POC_DATA, APPROVAL]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")

    poc = json.loads(POC_DATA.read_text())
    approval = json.loads(APPROVAL.read_text())
    if approval["approvedContract"]["gripProfile"] != "hold_shaft_two_hand":
        raise RuntimeError("approved motion foundation has changed")

    for directory in (PACK, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (FRAMES, LAYERS, MASKS, GUIDES, EVIDENCE, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    walk_cells = extract_cells(Image.open(WALK_SOURCE).convert("RGBA"), 8)
    turn_cells = extract_cells(Image.open(TURN_SOURCE).convert("RGBA"), 9)
    records: dict[str, dict] = {}
    composites: dict[str, Image.Image] = {}
    authorities: dict[str, Image.Image] = {}
    layer_previews: list[tuple[str, Image.Image]] = []

    def build_record(name: str, kind: str, index: int, source_cell: Image.Image, metadata: dict) -> None:
        poc_record = poc["frames"][name]
        authority = authority_canvas(poc_record)
        poc_candidate = Image.open(ROOT / poc_record["candidate"]["file"]).convert("RGBA")
        upper, registration = register_upper(source_cell, poc_candidate, authority)
        lower_mask = lower_body_mask(authority)
        lower = masked_authority(authority, lower_mask)
        fill, fill_audit = lower_occlusion_fill(authority, lower_mask, upper)
        arm_mask = arm_ownership_mask(upper, kind, index)
        torso, arms = split_upper(upper, arm_mask)
        composite = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(lower, fill), torso), arms)
        hands = visible_hand_components(arms)
        guide = guide_image(hands)
        paths = {
            "composite": FRAMES / f"{name}.png",
            "lower": LAYERS / f"{name}-lower-body-authority.png",
            "fill": LAYERS / f"{name}-lower-body-occlusion-fill.png",
            "torso": LAYERS / f"{name}-torso-head.png",
            "arms": LAYERS / f"{name}-held-arms.png",
            "authority": EVIDENCE / f"{name}-registered-authority.png",
            "poc": EVIDENCE / f"{name}-approved-poc-v3.png",
            "lowerMask": MASKS / f"{name}-lower-body-authority.png",
            "armMask": MASKS / f"{name}-held-arm-ownership.png",
            "guide": GUIDES / f"{name}-grip-axis.png",
        }
        for key, image in (("composite", composite), ("lower", lower), ("fill", fill), ("torso", torso), ("arms", arms),
                           ("authority", authority), ("poc", poc_candidate), ("lowerMask", lower_mask),
                           ("armMask", arm_mask), ("guide", guide)):
            save_png(image, paths[key])
        lower_audit = exact_lower_audit(authority, lower, lower_mask)
        ownership = ownership_audit(lower, fill, torso, arms, composite)
        colour = colour_provenance(upper, authority)
        if (lower_audit["changedPixels"] or lower_audit["missingPixels"] or
                lower_audit["coveragePercent"] != 100 or lower_audit["oldArmOrHandSkinPixels"]):
            raise RuntimeError(f"{name}: lower-body authority mismatch")
        if not ownership["recompositionExact"] or ownership["torsoArmOverlapPixels"]:
            raise RuntimeError(f"{name}: layer ownership failure")
        if colour["nonAuthorityRgbPixels"]:
            raise RuntimeError(f"{name}: generated RGB escaped authority palette")
        if len(hands) > 2:
            raise RuntimeError(f"{name}: more than two visible hands")
        for layer in (lower, fill, torso, arms, composite):
            if edge_alpha(layer):
                raise RuntimeError(f"{name}: layer touches cell edge")
        records[name] = {
            "id": name, "kind": f"{kind}-separable-prime-upper-body", **metadata,
            "motionFoundation": {"set": poc["set"], "recordId": name, "candidateSha256": poc_record["candidate"]["sha256"]},
            "authority": {**poc_record["authority"], "registeredFile": rel(paths["authority"]),
                          "registeredSha256": sha(paths["authority"]), "translationOnlyOffsetPx": poc_record["translationOnlyOffsetPx"]},
            "generatedUpperSource": {"file": rel(WALK_SOURCE if kind == "walk" else TURN_SOURCE),
                                     "sha256": sha(WALK_SOURCE if kind == "walk" else TURN_SOURCE), "sourceCell": index,
                                     "registration": registration, "role": "new prop-free upper-body source only"},
            "layers": {
                "lowerBodyAuthority": {"file": rel(paths["lower"]), "sha256": sha(paths["lower"]), "audit": lower_audit},
                "lowerBodyOcclusionFill": {"file": rel(paths["fill"]), "sha256": sha(paths["fill"]), "audit": fill_audit},
                "torsoHead": {"file": rel(paths["torso"]), "sha256": sha(paths["torso"]), "bounds": alpha_bounds(torso)},
                "heldArms": {"file": rel(paths["arms"]), "sha256": sha(paths["arms"]), "bounds": alpha_bounds(arms)},
            },
            "masks": {
                "lowerBodyAuthority": {"file": rel(paths["lowerMask"]), "sha256": sha(paths["lowerMask"])},
                "heldArmOwnership": {"file": rel(paths["armMask"]), "sha256": sha(paths["armMask"])},
            },
            "composite": {"file": rel(paths["composite"]), "sha256": sha(paths["composite"]),
                          "bounds": alpha_bounds(composite), "edgeAlphaPixels": edge_alpha(composite),
                          "transparentGutterPx": transparent_gutter(composite)},
            "approvedPocV3Comparison": {"file": rel(paths["poc"]), "sha256": sha(paths["poc"])},
            "hands": {"visibleComponents": hands, "visibleComponentCount": len(hands), "maximumAllowed": 2,
                      "occludedAllowedDuringTurn": True},
            "gripGuide": {"file": rel(paths["guide"]), "sha256": sha(paths["guide"]), "reviewOverlayOnly": True},
            "colourEvidence": colour,
            "ownership": ownership,
        }
        composites[name], authorities[name] = composite, authority
        layer_previews.extend([
            (f"{name} · exact lower", lower), (f"{name} · torso/head", torso),
            (f"{name} · occlusion fill", fill), (f"{name} · held arms", arms), (f"{name} · recomposed", composite),
        ])

    for index, cell in enumerate(walk_cells, 1):
        build_record(f"walk{index}", "walk", index, cell, {
            "gaitFrame": index, "gaitPhase": GAIT[index - 1], "durationMs": 125,
        })
    for index, cell in enumerate(turn_cells, 1):
        build_record(f"turn{index}", "turn", index, cell, {
            "turnFrame": index, "angleDegrees": ANGLES[index - 1], "durationMs": round(1000 / 9, 6),
        })

    walk_sheet = EVIDENCE / "walk-layered-contact-sheet.png"
    turn_sheet = EVIDENCE / "turn-layered-contact-sheet.png"
    compare_sheet = EVIDENCE / "authority-layered-comparison.png"
    layers_sheet = EVIDENCE / "layer-isolation-sheet.png"
    save_png(evidence_sheet([(f"Walk F{i} · {GAIT[i-1]}", composites[f"walk{i}"]) for i in range(1, 9)], 4), walk_sheet)
    save_png(evidence_sheet([(f"Turn F{i} · {ANGLES[i-1]}°", composites[f"turn{i}"]) for i in range(1, 10)], 3), turn_sheet)
    comparisons: list[tuple[str, Image.Image]] = []
    for name in [*(f"walk{i}" for i in range(1, 9)), *(f"turn{i}" for i in range(1, 10))]:
        comparisons.extend([(f"{name} · exact authority", authorities[name]), (f"{name} · layered draft", composites[name])])
    save_png(evidence_sheet(comparisons, 4), compare_sheet)
    save_png(evidence_sheet(layer_previews, 4), layers_sheet)

    published: list[dict] = []
    by_hash: dict[str, str] = {}

    def publish(path: Path, label: str) -> str:
        digest = sha(path)
        if digest in by_hash:
            return by_hash[digest]
        target = ASSETS / f"{label}-{digest[:16]}.png"
        shutil.copy2(path, target)
        url = f"https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects/{digest[:2]}/{digest}.png"
        by_hash[digest] = url
        published.append({"source": rel(path), "sourceSha256": digest, "publicAssemblyPath": rel(target), "url": url})
        return url

    for record in records.values():
        record["urls"] = {
            "composite": publish(ROOT / record["composite"]["file"], record["id"]),
            "lowerBodyAuthority": publish(ROOT / record["layers"]["lowerBodyAuthority"]["file"], f"{record['id']}-lower"),
            "lowerBodyOcclusionFill": publish(ROOT / record["layers"]["lowerBodyOcclusionFill"]["file"], f"{record['id']}-fill"),
            "torsoHead": publish(ROOT / record["layers"]["torsoHead"]["file"], f"{record['id']}-torso"),
            "heldArms": publish(ROOT / record["layers"]["heldArms"]["file"], f"{record['id']}-arms"),
            "authority": publish(ROOT / record["authority"]["registeredFile"], f"{record['id']}-authority"),
            "approvedPocV3": publish(ROOT / record["approvedPocV3Comparison"]["file"], f"{record['id']}-poc-v3"),
            "lowerMask": publish(ROOT / record["masks"]["lowerBodyAuthority"]["file"], f"{record['id']}-lower-mask"),
            "armMask": publish(ROOT / record["masks"]["heldArmOwnership"]["file"], f"{record['id']}-arm-mask"),
            "guide": publish(ROOT / record["gripGuide"]["file"], f"{record['id']}-guide"),
        }

    sheet_urls = {
        "walk": publish(walk_sheet, "walk-contact-sheet"), "turn": publish(turn_sheet, "turn-contact-sheet"),
        "comparison": publish(compare_sheet, "authority-comparison"), "layers": publish(layers_sheet, "layer-isolation"),
    }
    route = json.loads(json.dumps(poc["route"]))
    data = {
        "schema": "lighthouse-keeper/separable-held-body@1", "set": SET,
        "status": "versioned-reversible-layered-prime-draft-awaiting-frank",
        "cell": {"sourcePixels": list(CELL), "density": 8, "logical": [48, 40], "sourceAnchorXLp": 18.75},
        "gripProfile": "hold_shaft_two_hand", "frames": records, "route": route, "sheets": sheet_urls,
        "contract": {
            "approvedMotionFoundation": poc["set"], "approvedMotionDecisionSha256": sha(APPROVAL),
            "walkPhases": 8, "turnAngles": 9, "combinedPlaybackFrames": len(route),
            "layerOrder": ["lowerBodyAuthority", "lowerBodyOcclusionFill", "torsoHead", "heldArms"],
            "exactWalkV6LowerBody": True, "exactTurnV9LowerBody": True,
            "maximumVisibleHands": 2, "propPixels": 0, "propLayerPresent": False,
            "oneShotPlayback": True, "runtimeChanged": False, "finalChanged": False,
        },
        "reviewInstruction": "Judge the first separable Prime torso/arm construction only. The approved V3 motion, Walk V6 lower-body bytes, Turn V9 lower-body bytes, root advance and one-shot route are locked. No implement is present; nothing is approved or promoted.",
    }
    data_file = PACK / f"{SET}.json"
    dump(data_file, data)

    reviewer = build_reviewer(data)
    reviewer_file = PACK / "reviewer.html"
    reviewer_file.write_text(reviewer)
    shell = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper layered hold_shaft_two_hand V1</title><style>html,body,iframe{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}#loading{padding:24px}iframe{display:none}</style><p id="loading">Loading immutable Prime Keeper layered hold_shaft_two_hand V1…</p><iframe id="review" title="Prime Keeper layered hold_shaft_two_hand V1 reviewer"></iframe><script>fetch("https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/__LAYERED_V1_COMMIT__/art/drafts/keeper-prime-hold-shaft-two-hand-layered-2026-10-19-v1/reviewer.html").then(r=>{if(!r.ok)throw Error(\'reviewer \'+r.status);return r.text()}).then(t=>{document.querySelector(\'#review\').srcdoc=t;document.querySelector(\'#review\').style.display=\'block\';document.querySelector(\'#loading\').remove()}).catch(e=>document.querySelector(\'#loading\').textContent=\'Reviewer failed to load: \'+e.message)</script></html>\n'
    (PUBLIC / "index.html").write_text(shell)

    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET,
        "status": "awaiting-frank-layered-art-review",
        "purpose": "First prop-free separable Prime torso/arm implementation of the approved hold_shaft_two_hand motion foundation.",
        "authorities": {
            "approvedPocV3": {"file": rel(POC_DATA), "sha256": sha(POC_DATA)},
            "approvedPocV3Decision": {"file": rel(APPROVAL), "sha256": sha(APPROVAL)},
            "walkV6": [{"frame": i, **records[f"walk{i}"]["authority"]} for i in range(1, 9)],
            "turnV9": [{"frame": i, "angleDegrees": ANGLES[i - 1], **records[f"turn{i}"]["authority"]} for i in range(1, 10)],
        },
        "sources": {
            "walkUpperBody": {"file": rel(WALK_SOURCE), "sha256": sha(WALK_SOURCE)},
            "turnUpperBody": {"file": rel(TURN_SOURCE), "sha256": sha(TURN_SOURCE)},
        },
        "construction": data["contract"],
        "candidate": {
            "routeData": {"file": rel(data_file), "sha256": sha(data_file)},
            "reviewer": {"file": rel(reviewer_file), "sha256": sha(reviewer_file)},
            "publicShell": {"file": rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")},
            "frames": list(records.values()), "sheets": {name: {"file": rel(path), "sha256": sha(path)} for name, path in {
                "walk": walk_sheet, "turn": turn_sheet, "comparison": compare_sheet, "layers": layers_sheet,
            }.items()},
            "reviewUrl": f"https://lighthouse-keeper-mu.vercel.app/keeper-review/{SET}/",
        },
        "publishedAssets": published,
        "approvalBoundary": {
            "motionFoundationApproved": True, "layeredArtworkApproved": False, "implementIncluded": False,
            "broomIncluded": False, "runtimeChanged": False, "finalChanged": False,
            "productionArtworkChanged": False, "promotionPerformed": False,
        },
        "rollback": f"Delete only {PACK_REL}, {SOURCE_REL}, public/keeper-review/{SET}, and the layered V1 builder/verifier entries. All approved authorities and immutable POC V1-V3 remain untouched.",
    }
    dump(PACK / "batch-register.json", register)
    (PACK / "HANDOFF.md").write_text(
        "# Prime Keeper layered hold_shaft_two_hand V1\n\n"
        "This is the first prop-free separable implementation after approval of motion-feasibility POC V3. Every frame has four independently hash-pinned layers: exact Walk V6 or Turn V9 lower-body authority pixels, a separately declared lower-body occlusion fill where the removed historical hand exposed unavailable trouser pixels, a new torso/head layer, and a new held-arm layer. The V3 route, gait order, turn order, timing, mirrored anchor correction, rear-seam presentation offset and one-shot playback are unchanged. No broom or other implement exists in the pack. Nothing is approved or promoted.\n"
    )
    (PACK / "PROMPT_LOG.md").write_text(
        "# Source-art record\n\n"
        "Mode: built-in `image_gen`, precise-object-edit. Both selected outputs are preserved unchanged under `art/source/`. They supply upper-body pixels only; deterministic code registers them to the approved POC V3 motion, maps every visible RGB value to the matching Walk V6 or Turn V9 authority palette, separates torso/head from held arms, and recomposes those layers over byte-identical lower-body authority pixels.\n\n"
        "## Selected walk source\n\n"
        f"- File: `{rel(WALK_SOURCE)}`\n- SHA-256: `{sha(WALK_SOURCE)}`\n"
        "- Prompt: preserve the exact eight side-right POC walk poses in 4×2 order; remove only trousers, legs and boots below the ribbed waistband; retain head, beard, torso, waistband, exactly two connected arms and at most two closed hands around an invisible shaft; genuine transparent background; no prop, text, grid, shadow or detached object.\n\n"
        "## Selected turn source\n\n"
        f"- File: `{rel(TURN_SOURCE)}`\n- SHA-256: `{sha(TURN_SOURCE)}`\n"
        "- Prompt: preserve the exact nine POC turn orientations in 3×3 order; remove only the lower body below the ribbed waistband; retain the upper body and natural rear-angle hand occlusion; genuine transparent background; no prop or detached object.\n\n"
        "## Rejected generation\n\n"
        "The first walk attempt (SHA-256 `1847eeb692cb5a9585c1c7c456d2f96f1ac0fef6922c7d5500d52b90c931e21a`) drifted its final two cells into rear views. It was rejected before import and contributes no candidate pixel.\n"
        "The imported exploratory walk grid `walk-upper-body-grid-generated.png` (SHA-256 `a486ea87d77e9036fdc71c02c852037dd71dc1dc70a838ac2f1e8cfdb0ffd119`) and turn grid `turn-upper-body-grid-generated.png` (SHA-256 `e2bb0a482a1820598f1de10409abf38eb4dbb9ad39d980d980ec23433ea637e1`) were superseded because their broad generated proportions were not close enough to the approved Prime authorities. They remain immutable source evidence and contribute no candidate pixel.\n"
    )
    print(f"Built {SET}: {len(records)} layered frames, {len(route)} playback frames, {len(published)} unique review images")


def build_reviewer(data: dict) -> str:
    payload = json.dumps(data, separators=(",", ":"))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper layered hold_shaft_two_hand V1</title><style>
:root{{color-scheme:dark;--bg:#07131b;--panel:#10242f;--line:#36515e;--ink:#edf8fb;--cyan:#54e6ff;--amber:#ffd66b;--green:#75e59d}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:18px}}header{{border-bottom:1px solid var(--line)}}h1{{margin:.2em 0}}.tag{{display:inline-block;border:1px solid var(--green);border-radius:999px;padding:4px 9px;margin:2px;color:#c9ffda}}.notice{{border-left:4px solid var(--amber);background:#2b2618;padding:10px 13px}}.panel{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.controls{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}button,select,input{{font:inherit}}button,select{{background:#07131b;color:var(--ink);border:1px solid var(--line);padding:7px 10px;border-radius:6px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(260px,1fr));gap:16px}}.stagewrap{{overflow:auto;background:#061017;padding:8px}}.stage{{position:relative;background:repeating-conic-gradient(#263b46 0 25%,#182b35 0 50%) 50%/16px 16px;overflow:hidden}}.stage img{{position:absolute;image-rendering:auto}}.ghost{{opacity:.24;filter:hue-rotate(145deg)}}.compare{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}.compare img{{width:100%;background:repeating-conic-gradient(#263b46 0 25%,#182b35 0 50%) 50%/12px 12px}}.sheet{{width:100%;background:#08161e;margin:8px 0}}#loading{{color:var(--cyan)}}#caption{{font-family:ui-monospace,monospace}}@media(max-width:900px){{.grid,.compare{{grid-template-columns:1fr}}}}</style></head><body><header><h1>Prime Keeper · layered <code>hold_shaft_two_hand</code> V1</h1><span class="tag">Exact approved lower bodies</span><span class="tag">Separable torso + arms</span><span class="tag">No implement</span><span class="tag">Nothing promoted</span><p class="notice"><strong>Review gate:</strong> judge the new torso/arm construction and its joins to the immutable Walk V6 and Turn V9 lower bodies. Motion is already approved through POC V3 and is unchanged. Pixels concealed by the removed historical swinging hand are restored in a separate, non-authority occlusion-fill layer. No broom, shaft or prop pixel exists.</p></header><main><section class="panel"><div id="loading">Loading and decoding every unique frame… controls remain locked.</div><div class="controls"><button id="play" disabled>Play</button><button id="prev" disabled>Previous</button><button id="next" disabled>Next</button><button id="restart" disabled>Restart</button><select id="clip" disabled><option value="all">Combined 33-frame route</option><option value="walk-right">Walk right · 8</option><option value="turn">Turn · 17</option><option value="walk-left">Walk left · 8</option></select><label>Speed <input id="speed" disabled type="range" min="0.35" max="1.25" value="0.65" step="0.05"></label><label><input id="lower" disabled type="checkbox" checked> exact lower</label><label><input id="fill" disabled type="checkbox" checked> occlusion fill</label><label><input id="torso" disabled type="checkbox" checked> torso/head</label><label><input id="arms" disabled type="checkbox" checked> held arms</label><label><input id="ghost" disabled type="checkbox"> prior ghost</label><label><input id="guide" disabled type="checkbox"> grip guide</label></div><p id="caption"></p></section><section class="panel"><div class="grid"><div><h2>Large · 6 px/lp</h2><div class="stagewrap"><div class="stage" id="large"></div></div></div><div><h2>Gameplay · 4 px/lp</h2><div class="stagewrap"><div class="stage" id="game"></div></div></div><div><h2>Literal · 1 px/lp</h2><div class="stagewrap"><div class="stage" id="literal"></div></div></div></div></section><section class="panel"><h2>Selected-frame isolation</h2><div class="compare"><div><strong>Exact registered authority</strong><img id="authority"></div><div><strong>Approved POC V3 motion proxy</strong><img id="poc"></div><div><strong>Layered V1 composite</strong><img id="composite"></div><div><strong>Exact lower-body layer</strong><img id="lowerImg"></div><div><strong>Declared occlusion fill</strong><img id="fillImg"></div><div><strong>Torso/head layer</strong><img id="torsoImg"></div><div><strong>Held-arm layer</strong><img id="armsImg"></div></div></section><section class="panel"><h2>Walk phases</h2><img class="sheet" src="{data['sheets']['walk']}"><h2>Turn angles</h2><img class="sheet" src="{data['sheets']['turn']}"><h2>Authority comparison</h2><img class="sheet" src="{data['sheets']['comparison']}"><h2>Layer isolation</h2><img class="sheet" src="{data['sheets']['layers']}"></section></main><script>
const DATA={payload};let sequence=DATA.route,i=0,timer=null;const stages=[];function make(id,scale){{const host=document.querySelector('#'+id);host.style.width=192*scale+'px';host.style.height=56*scale+'px';for(const name of ['ghost','lower','fill','torso','arms','guide']){{const img=document.createElement('img');img.dataset.layer=name;if(name==='ghost')img.className='ghost';host.append(img)}}stages.push({{host,scale}})}}make('large',6);make('game',4);make('literal',1);
function currentClip(){{const choice=document.querySelector('#clip').value;if(choice==='walk-right')return DATA.route.slice(0,8);if(choice==='turn')return DATA.route.slice(8,25);if(choice==='walk-left')return DATA.route.slice(25);return DATA.route}}function place(stage,img,frame,src){{img.src=src;img.style.width=48*stage.scale+'px';img.style.height=40*stage.scale+'px';img.style.left=(frame.rootXLp-frame.renderAnchorXLp)*stage.scale+'px';img.style.top=12*stage.scale+'px';img.style.transform=frame.mirror?'scaleX(-1)':'none'}}function show(){{const frame=sequence[i],record=DATA.frames[frame.recordId],prior=sequence[Math.max(0,i-1)],priorRecord=DATA.frames[prior.recordId];for(const stage of stages){{const q=name=>stage.host.querySelector('[data-layer='+name+']');place(stage,q('lower'),frame,record.urls.lowerBodyAuthority);place(stage,q('fill'),frame,record.urls.lowerBodyOcclusionFill);place(stage,q('torso'),frame,record.urls.torsoHead);place(stage,q('arms'),frame,record.urls.heldArms);place(stage,q('guide'),frame,record.urls.guide);place(stage,q('ghost'),prior,priorRecord.urls.composite);q('lower').style.display=document.querySelector('#lower').checked?'block':'none';q('fill').style.display=document.querySelector('#fill').checked?'block':'none';q('torso').style.display=document.querySelector('#torso').checked?'block':'none';q('arms').style.display=document.querySelector('#arms').checked?'block':'none';q('guide').style.display=document.querySelector('#guide').checked?'block':'none';q('ghost').style.display=document.querySelector('#ghost').checked?'block':'none'}}document.querySelector('#authority').src=record.urls.authority;document.querySelector('#poc').src=record.urls.approvedPocV3;document.querySelector('#composite').src=record.urls.composite;document.querySelector('#lowerImg').src=record.urls.lowerBodyAuthority;document.querySelector('#fillImg').src=record.urls.lowerBodyOcclusionFill;document.querySelector('#torsoImg').src=record.urls.torsoHead;document.querySelector('#armsImg').src=record.urls.heldArms;document.querySelector('#caption').textContent=`${{i+1}}/${{sequence.length}} · ${{frame.phase}} · ${{record.id}} · exact lower ${{record.layers.lowerBodyAuthority.audit.declaredAuthorityPixels}} px · fill ${{record.layers.lowerBodyOcclusionFill.audit.reconstructedPixels}} px · visible hands ${{record.hands.visibleComponentCount}} · prop 0`;}}function stop(){{if(timer)clearTimeout(timer);timer=null;document.querySelector('#play').textContent='Play'}}function tick(){{const frame=sequence[i];show();if(i===sequence.length-1){{stop();return}}timer=setTimeout(()=>{{i+=1;tick()}},frame.durationMs/Number(document.querySelector('#speed').value))}}document.querySelector('#play').onclick=()=>{{if(timer)stop();else{{if(i===sequence.length-1)i=0;document.querySelector('#play').textContent='Pause';tick()}}}};document.querySelector('#prev').onclick=()=>{{stop();i=(i-1+sequence.length)%sequence.length;show()}};document.querySelector('#next').onclick=()=>{{stop();i=(i+1)%sequence.length;show()}};document.querySelector('#restart').onclick=()=>{{stop();i=0;show();document.querySelector('#play').click()}};document.querySelector('#clip').onchange=()=>{{stop();sequence=currentClip();i=0;show()}};for(const id of ['lower','fill','torso','arms','ghost','guide'])document.querySelector('#'+id).onchange=show;
const urls=new Set(Object.values(DATA.sheets));for(const record of Object.values(DATA.frames))for(const src of Object.values(record.urls))urls.add(src);Promise.all([...urls].map(src=>new Promise((ok,bad)=>{{const img=new Image();img.onload=()=>{{const decoded=img.decode?.();decoded?decoded.then(ok).catch(bad):ok()}};img.onerror=()=>bad(new Error(src));img.src=src}}))).then(()=>{{document.querySelector('#loading').textContent=`${{urls.size}} unique images loaded and decoded. Controls enabled.`;document.querySelectorAll('button,input,select').forEach(control=>control.disabled=false);show();}}).catch(error=>document.querySelector('#loading').textContent='Media failed; controls remain locked. '+error.message);
</script></body></html>'''


if __name__ == "__main__":
    main()
