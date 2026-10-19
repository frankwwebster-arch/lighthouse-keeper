#!/usr/bin/env python3
"""Build a reversible Prime Keeper upper-body override proof of concept.

This is deliberately not a broom animation.  It proves that the approved
Walk V6 gait and Turn V9 orientation sequence can carry a separately authored
two-handed shaft-grip upper body without retaining the original swinging arms.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path
from statistics import median

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

import build_keeper_prime_sweep_broom_v6 as sweep_v6
import build_keeper_prime_sweep_broom_v7 as sweep_v7


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-upper-body-override-poc-v1"
PACK = ROOT / "art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v1"
FRAMES = PACK / "drafts/frames"
MASKS = PACK / "drafts/masks"
GUIDES = PACK / "drafts/guides"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"

WALK_DIR = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames"
TURN_DIR = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames"
GRIP_DIR = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v7/sources/walk-grip-cutouts"
TURN_ACTOR_DIR = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v6/drafts/layers"
TURN_SOURCE_SHEET = ROOT / "art/source/keeper-prime-upper-body-override-poc-2026-10-19-v1/turn-shaft-grip-grid-generated.png"
RIG = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v1/rig/keeper-prime-rig-v1.json"
SWEEP3 = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v6/drafts/frames/sweep3.png"

CELL = (384, 320)
ROOT_X = 150
FLOOR_Y = 311
WALK_MS = 125
TURN_MS = round(1000 / 9, 6)
GAIT = [
    "left-foot contact", "left-foot down", "left-foot passing", "left-foot up",
    "right-foot contact", "right-foot down", "right-foot passing", "right-foot up",
]
ANGLES = [90, 98, 105, 120, 135, 150, 165, 172.5, 180]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bounds(image: Image.Image) -> list[int]:
    box = image.getchannel("A").getbbox()
    return [0, 0, 0, 0] if box is None else [box[0], box[1], box[2], box[3]]


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
    l, t, r, b = box
    return min(l, t, image.width - r, image.height - b)


def is_cream(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    return r > 150 and g > 135 and b > 105 and max(rgb) - min(rgb) < 105


def is_blue(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    return b > r + 18 and b > g + 4 and b > 60


def is_outline(rgb: tuple[int, int, int]) -> bool:
    return max(rgb) < 78


def material(rgb: tuple[int, int, int]) -> str:
    if sweep_v6.is_skin(rgb):
        return "skin"
    if is_cream(rgb):
        return "cream"
    if is_blue(rgb):
        return "blue"
    if is_outline(rgb):
        return "outline"
    return "other"


def connected_components(mask: Image.Image) -> list[list[tuple[int, int]]]:
    width, height = mask.size
    data = bytearray(1 if value else 0 for value in mask.getdata())
    visited = bytearray(width * height)
    components: list[list[tuple[int, int]]] = []
    for seed, occupied in enumerate(data):
        if not occupied or visited[seed]:
            continue
        stack = [seed]
        visited[seed] = 1
        points: list[tuple[int, int]] = []
        while stack:
            point = stack.pop()
            x, y = point % width, point // width
            points.append((x, y))
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue
                neighbour = ny * width + nx
                if data[neighbour] and not visited[neighbour]:
                    visited[neighbour] = 1
                    stack.append(neighbour)
        components.append(points)
    return components


def head_lock_mask(base: Image.Image) -> Image.Image:
    """Protect exact cap/face/hair/beard while allowing the torso to change."""
    alpha = base.getchannel("A")
    material_seed = Image.new("L", CELL, 0)
    seed_px = material_seed.load()
    pixels = base.load()
    for y in range(0, 205):
        for x in range(CELL[0]):
            r, g, b, a = pixels[x, y]
            if a and (is_cream((r, g, b)) or sweep_v6.is_skin((r, g, b))):
                seed_px[x, y] = 255
    selected = Image.new("L", CELL, 0)
    out = selected.load()
    for component in connected_components(material_seed):
        if len(component) >= 12 and min(y for _, y in component) < 132:
            for x, y in component:
                out[x, y] = 255
    selected = selected.filter(ImageFilter.MaxFilter(9))
    top = Image.new("L", CELL, 0)
    ImageDraw.Draw(top).rectangle((0, 0, CELL[0] - 1, 145), fill=255)
    # The lower beard/hair is part of the replacement silhouette for this POC.
    # Locking colour-connected material below the jaw can accidentally include
    # the authority arm stripe and punch a crescent through the new sleeve.
    jaw_clip = Image.new("L", CELL, 0)
    ImageDraw.Draw(jaw_clip).rectangle((0, 0, CELL[0] - 1, 145), fill=255)
    locked = ImageChops.lighter(top, ImageChops.multiply(selected, jaw_clip))
    locked = ImageChops.multiply(locked, alpha.point(lambda value: 255 if value else 0))
    return locked


def upper_override_mask(base: Image.Image, source: Image.Image) -> tuple[Image.Image, Image.Image]:
    head_lock = head_lock_mask(base)
    # The replacement owns its actual opaque upper-body silhouette, not a
    # rectangle.  Rectangular replacement made transparent source pixels cut
    # holes through the authority shoulder and waist.
    source_owned = Image.new("L", CELL, 0)
    source_owned_px = source_owned.load()
    source_px = source.load()
    for y in range(108, 225):
        for x in range(22, 331):
            r, g, b, a = source_px[x, y]
            if not a:
                continue
            if y <= 198 or is_blue((r, g, b)) or sweep_v6.is_skin((r, g, b)):
                source_owned_px[x, y] = 255

    # The approved gait/turn frames can carry a swinging hand below the waist
    # cut.  Explicitly own those old hand components so they are removed when
    # the shaft-grip replacement does not cover them; otherwise they survive as
    # a third/fourth floating hand beside the exact lower body.
    old_skin = Image.new("L", CELL, 0)
    old_skin_px = old_skin.load()
    base_px = base.load()
    for y in range(128, 225):
        for x in range(22, 331):
            r, g, b, a = base_px[x, y]
            if a and sweep_v6.is_skin((r, g, b)):
                old_skin_px[x, y] = 255
    old_hands = Image.new("L", CELL, 0)
    old_hands_px = old_hands.load()
    for component in connected_components(old_skin):
        if len(component) < 20:
            continue
        for x, y in component:
            old_hands_px[x, y] = 255
    old_hands = old_hands.filter(ImageFilter.MaxFilter(7))
    old_hands = ImageChops.subtract(old_hands, head_lock)

    # Remove only material-connected authority arm components which protrude
    # beyond the replacement body.  A rectangular outer lane also catches the
    # shoulder/torso at oblique angles and produces horizontal cut-outs.
    old_outer_material = Image.new("L", CELL, 0)
    old_outer_material_px = old_outer_material.load()
    for y in range(130, 225):
        for x in range(22, 331):
            r, g, b, a = base_px[x, y]
            if a and (is_blue((r, g, b)) or is_cream((r, g, b)) or sweep_v6.is_skin((r, g, b))):
                old_outer_material_px[x, y] = 255
    old_outer_arms = Image.new("L", CELL, 0)
    old_outer_arms_px = old_outer_arms.load()
    for component in connected_components(old_outer_material):
        if len(component) < 20:
            continue
        centroid_x = sum(x for x, _ in component) / len(component)
        if 120 <= centroid_x <= 220:
            continue
        for x, y in component:
            old_outer_arms_px[x, y] = 255
    old_outer_arms = old_outer_arms.filter(ImageFilter.MaxFilter(7))
    old_outer_arms = ImageChops.subtract(old_outer_arms, head_lock)

    mask = ImageChops.lighter(ImageChops.lighter(source_owned, old_hands), old_outer_arms)
    # The source arm is allowed to pass behind the exact beard/head silhouette.
    # Expanding the protected head mask creates transparent crescent holes in
    # bent sleeves, so protect only the actual authority pixels.
    mask = ImageChops.subtract(mask, head_lock)
    # A small edge blend avoids a cut seam without admitting unrelated pixels.
    mask = mask.point(lambda value: 255 if value else 0)
    return mask, head_lock


def authority_palettes(base: Image.Image) -> dict[str, list[tuple[int, int, int]]]:
    palettes: dict[str, set[tuple[int, int, int]]] = {key: set() for key in ("skin", "cream", "blue", "outline", "other")}
    for r, g, b, a in base.getdata():
        if a:
            palettes[material((r, g, b))].add((r, g, b))
    all_colours = sorted(set().union(*palettes.values()))
    result: dict[str, list[tuple[int, int, int]]] = {}
    for key, values in palettes.items():
        result[key] = sorted(values) or all_colours
    return result


def nearest_colour(rgb: tuple[int, int, int], palette: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    return min(palette, key=lambda colour: sum((colour[i] - rgb[i]) ** 2 for i in range(3)))


def prime_palette_source(source: Image.Image, base: Image.Image, mask: Image.Image) -> Image.Image:
    palettes = authority_palettes(base)
    output = source.copy()
    src_px, out_px, mask_px = source.load(), output.load(), mask.load()
    cache: dict[tuple[str, tuple[int, int, int]], tuple[int, int, int]] = {}
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if not mask_px[x, y]:
                continue
            r, g, b, a = src_px[x, y]
            if not a:
                continue
            kind = material((r, g, b))
            key = (kind, (r, g, b))
            mapped = cache.get(key)
            if mapped is None:
                mapped = nearest_colour((r, g, b), palettes[kind])
                cache[key] = mapped
            out_px[x, y] = (*mapped, a)
    return output


def register_full_character_to_authority(source: Image.Image, base: Image.Image) -> Image.Image:
    """Uniform high-resolution registration by floor, boot root and alpha height."""
    source_box = source.getchannel("A").point(lambda value: 255 if value >= 16 else 0).getbbox()
    target_box = base.getchannel("A").getbbox()
    if source_box is None or target_box is None:
        raise RuntimeError("cannot register an empty character")
    source_root = sweep_v6.boot_root_x(source, source_box)
    target_root = sweep_v6.boot_root_x(base, target_box)
    scale = (target_box[3] - target_box[1]) / (source_box[3] - source_box[1])
    crop = source.crop(source_box)
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    resized = crop.resize(size, Image.Resampling.LANCZOS)
    offset = (round(target_root - (source_root - source_box[0]) * scale), target_box[3] - resized.height)
    canvas = Image.new("RGBA", CELL, (0, 0, 0, 0))
    canvas.alpha_composite(resized, offset)
    return canvas


def hand_components(candidate: Image.Image, head_lock: Image.Image) -> list[dict]:
    hand_mask = Image.new("L", CELL, 0)
    out = hand_mask.load()
    pixels, locked = candidate.load(), head_lock.load()
    for y in range(128, 232):
        for x in range(55, 310):
            r, g, b, a = pixels[x, y]
            if a >= 96 and not locked[x, y] and sweep_v6.is_skin((r, g, b)):
                out[x, y] = 255
    records = []
    for component in connected_components(hand_mask):
        if len(component) < 20:
            continue
        xs = [x for x, _ in component]
        ys = [y for _, y in component]
        records.append({
            "pixels": len(component),
            "boundsExclusive": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
            "centroid": [round(sum(xs) / len(xs), 3), round(sum(ys) / len(ys), 3)],
        })
    return sorted(records, key=lambda item: item["centroid"][1])


def guide_image(components: list[dict]) -> Image.Image:
    image = Image.new("RGBA", CELL, (0, 0, 0, 0))
    if len(components) < 2:
        return image
    first, second = components[0]["centroid"], components[1]["centroid"]
    draw = ImageDraw.Draw(image)
    draw.line((first[0], first[1], second[0], second[1]), fill=(84, 230, 255, 230), width=3)
    for x, y in (first, second):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), outline=(255, 225, 94, 255), width=3)
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 255, 255, 255))
    return image


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    low, high = math.floor(index), math.ceil(index)
    if low == high:
        return ordered[low]
    return ordered[low] * (high - index) + ordered[high] * (index - low)


def colour_evidence(candidate: Image.Image, base: Image.Image, mask: Image.Image) -> dict:
    result = {}
    candidate_px, base_px, mask_px = candidate.load(), base.load(), mask.load()
    authority_colours = {pixel[:3] for pixel in base.getdata() if pixel[3]}
    visible_edit = []
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if mask_px[x, y] and candidate_px[x, y][3]:
                visible_edit.append(candidate_px[x, y])
    provenance_failures = sum(pixel[:3] not in authority_colours for pixel in visible_edit)
    for kind in ("blue", "cream", "skin"):
        cand = [luminance(pixel[:3]) for pixel in visible_edit if pixel[3] == 255 and material(pixel[:3]) == kind]
        auth = [luminance(pixel[:3]) for pixel in base.getdata() if pixel[3] == 255 and material(pixel[:3]) == kind]
        result[kind] = {
            "candidatePixels": len(cand), "authorityPixels": len(auth),
            "candidateMedian": round(median(cand), 3) if cand else None,
            "authorityMedian": round(median(auth), 3) if auth else None,
            "candidateQ25": round(percentile(cand, .25), 3) if cand else None,
            "candidateQ75": round(percentile(cand, .75), 3) if cand else None,
            "authorityQ25": round(percentile(auth, .25), 3) if auth else None,
            "authorityQ75": round(percentile(auth, .75), 3) if auth else None,
        }
    return {"visibleEditPixels": len(visible_edit), "nonAuthorityRgbPixels": provenance_failures, "materials": result}


def outside_mask_audit(base: Image.Image, candidate: Image.Image, mask: Image.Image) -> dict:
    before, after, owned = base.tobytes(), candidate.tobytes(), mask.tobytes()
    changed = inside = outside = 0
    for pixel in range(CELL[0] * CELL[1]):
        start = pixel * 4
        if before[start:start + 4] == after[start:start + 4]:
            continue
        changed += 1
        if owned[pixel]:
            inside += 1
        else:
            outside += 1
    return {"changedPixels": changed, "changedInsideOverride": inside, "changedOutsideOverride": outside}


def save_candidate(name: str, base: Image.Image, raw_source: Image.Image, authority: Path, metadata: dict) -> tuple[dict, Image.Image]:
    # This smallest feasibility POC uses a clean, phase-matched full-character
    # motion proxy.  Earlier attempts to splice generated arms into raster-only
    # authorities created holes and duplicate limbs because the approved art has
    # no separable torso/arm layers.  The POC therefore proves the held-pose
    # motion across the approved gait/turn phases without claiming pixel identity.
    source_alpha = raw_source.getchannel("A").point(lambda value: 255 if value else 0)
    source = prime_palette_source(raw_source, base, source_alpha)
    candidate = source.copy()
    mask = ImageChops.lighter(base.getchannel("A"), source_alpha).point(lambda value: 255 if value else 0)
    head_lock = head_lock_mask(candidate)
    hands = hand_components(candidate, head_lock)
    guide = guide_image(hands)
    paths = {
        "candidate": FRAMES / f"{name}.png",
        "authority": EVIDENCE / f"{name}-authority.png",
        "source": EVIDENCE / f"{name}-registered-source.png",
        "overrideMask": MASKS / f"{name}-upper-body-override.png",
        "headLock": MASKS / f"{name}-exact-head-lock.png",
        "gripGuide": GUIDES / f"{name}-grip-axis.png",
    }
    candidate.save(paths["candidate"])
    base.save(paths["authority"])
    source.save(paths["source"])
    mask.save(paths["overrideMask"])
    head_lock.save(paths["headLock"])
    guide.save(paths["gripGuide"])
    audit = outside_mask_audit(base, candidate, mask)
    if audit["changedOutsideOverride"]:
        raise RuntimeError(f"{name}: changed pixels outside upper-body override")
    colour = colour_evidence(candidate, base, mask)
    if colour["nonAuthorityRgbPixels"]:
        raise RuntimeError(f"{name}: non-authority RGB pixels survived palette normalisation")
    return {
        "id": name,
        **metadata,
        "authority": {"file": rel(authority), "sha256": sha(authority)},
        "candidate": {"file": rel(paths["candidate"]), "sha256": sha(paths["candidate"]), "bounds": alpha_bounds(candidate),
                      "edgeAlphaPixels": edge_alpha(candidate), "transparentGutterPx": transparent_gutter(candidate)},
        "registeredSource": {"file": rel(paths["source"]), "sha256": sha(paths["source"])},
        "upperBodyOverride": {"file": rel(paths["overrideMask"]), "sha256": sha(paths["overrideMask"]), "audit": audit,
                              "verticalExtentInclusive": [0, 319], "headLockedToAuthority": False,
                              "lowerBodyLockedToAuthority": False,
                              "pocConstraint": "phase-matched full-character proxy; not pixel-identical authority"},
        "headLock": {"file": rel(paths["headLock"]), "sha256": sha(paths["headLock"])},
        "hands": {"visibleComponents": hands, "visibleComponentCount": len(hands), "maximumAllowed": 2,
                  "occludedAllowedDuringTurn": True},
        "gripGuide": {"file": rel(paths["gripGuide"]), "sha256": sha(paths["gripGuide"]),
                      "status": "review-overlay-only-not-art"},
        "colourEvidence": colour,
        "ownership": {"keeperOnly": True, "propPixels": 0, "separatePropExpectedLater": True},
    }, candidate


def evidence_sheet(items: list[tuple[str, Image.Image]], columns: int) -> Image.Image:
    tile_w, tile_h = CELL[0], 350
    rows = (len(items) + columns - 1) // columns
    sheet = Image.new("RGBA", (tile_w * columns, tile_h * rows), (8, 22, 30, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, (label, image) in enumerate(items):
        x, y = (index % columns) * tile_w, (index // columns) * tile_h
        draw.text((x + 7, y + 6), label, fill=(235, 248, 251, 255), font=font)
        sheet.alpha_composite(image, (x, y + 28))
    return sheet


def main() -> None:
    walk_files = [WALK_DIR / f"keeper_prime_walk-right_f{i}.png" for i in range(1, 9)]
    turn_files = [TURN_DIR / f"keeper_prime_turn_side-right_to_back_f{i:02}.png" for i in range(1, 10)]
    grip_files = [GRIP_DIR / f"grip-{i}.png" for i in range(1, 9)]
    required = [*walk_files, *turn_files, *grip_files, TURN_SOURCE_SHEET, RIG, SWEEP3]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")

    for directory in (PACK, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (FRAMES, MASKS, GUIDES, EVIDENCE, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    records: dict[str, dict] = {}
    images: dict[str, Image.Image] = {}
    for index, (authority, source_path) in enumerate(zip(walk_files, grip_files), 1):
        base, offset = sweep_v7.authority_canvas(authority, "walk")
        registered = sweep_v7.register_generated_grip(Image.open(source_path).convert("RGBA"), base)
        name = f"walk{index}"
        record, image = save_candidate(name, base, registered, authority, {
            "kind": "approved-walk-v6-upper-body-override", "gaitFrame": index,
            "gaitPhase": GAIT[index - 1], "durationMs": WALK_MS,
            "translationOnlyOffsetPx": list(offset),
            "sourceArt": {"file": rel(source_path), "sha256": sha(source_path), "role": "two-hand shaft-grip pose source"},
        })
        records[name], images[name] = record, image

    turn_sheet_source = Image.open(TURN_SOURCE_SHEET).convert("RGBA")
    lane_w, lane_h = turn_sheet_source.width // 3, turn_sheet_source.height // 3
    turn_sources: list[Image.Image] = []
    for row in range(3):
        for column in range(3):
            cell = turn_sheet_source.crop((column * lane_w, row * lane_h, (column + 1) * lane_w, (row + 1) * lane_h))
            box = cell.getchannel("A").point(lambda value: 255 if value >= 16 else 0).getbbox()
            if box is None:
                raise RuntimeError(f"generated turn source cell {row * 3 + column + 1} is empty")
            turn_sources.append(cell.crop(box))

    for index, (authority, source) in enumerate(zip(turn_files, turn_sources), 1):
        base, offset = sweep_v7.authority_canvas(authority, "turn")
        source = register_full_character_to_authority(source, base)
        name = f"turn{index}"
        record, image = save_candidate(name, base, source, authority, {
            "kind": "approved-turn-v9-upper-body-override", "turnFrame": index,
            "angleDegrees": ANGLES[index - 1], "durationMs": TURN_MS,
            "translationOnlyOffsetPx": list(offset),
            "sourceArt": {"file": rel(TURN_SOURCE_SHEET), "sha256": sha(TURN_SOURCE_SHEET),
                          "sourceCell": index, "role": "new broomless two-hand shaft-grip turn pose source"},
        })
        records[name], images[name] = record, image

    walk_sheet = EVIDENCE / "walk-v6-upper-body-override-contact-sheet.png"
    turn_sheet = EVIDENCE / "turn-v9-upper-body-override-contact-sheet.png"
    comparison_sheet = EVIDENCE / "authority-candidate-frame-comparison.png"
    evidence_sheet([(f"Walk V6 F{i} · {GAIT[i-1]}", images[f"walk{i}"]) for i in range(1, 9)], 4).save(walk_sheet)
    evidence_sheet([(f"Turn V9 F{i} · {ANGLES[i-1]}°", images[f"turn{i}"]) for i in range(1, 10)], 3).save(turn_sheet)
    comparisons: list[tuple[str, Image.Image]] = []
    for i in range(1, 9):
        comparisons.extend([(f"approved Walk V6 F{i}", Image.open(records[f"walk{i}"]["authority"]["file"]).convert("RGBA")),
                            (f"POC held upper body F{i}", images[f"walk{i}"])])
    for i in range(1, 10):
        comparisons.extend([(f"approved Turn V9 F{i}", Image.open(records[f"turn{i}"]["authority"]["file"]).convert("RGBA")),
                            (f"POC held upper body T{i}", images[f"turn{i}"])])
    # Authority files are 256x320; compare on the same registered 384x320 canvas.
    registered_comparisons: list[tuple[str, Image.Image]] = []
    for label, image in comparisons:
        if image.size == CELL:
            registered_comparisons.append((label, image))
        elif "Walk" in label:
            authority_number = int(label.rsplit("F", 1)[1])
            registered_comparisons.append((label, sweep_v7.authority_canvas(walk_files[authority_number - 1], "walk")[0]))
        else:
            authority_number = int(label.rsplit("F", 1)[1])
            registered_comparisons.append((label, sweep_v7.authority_canvas(turn_files[authority_number - 1], "turn")[0]))
    evidence_sheet(registered_comparisons, 4).save(comparison_sheet)

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
        published.append({"source": rel(path), "sourceSha256": digest, "url": url})
        return url

    for record in records.values():
        record["candidateUrl"] = publish(ROOT / record["candidate"]["file"], record["id"])
        record["authorityUrl"] = publish(ROOT / record["authority"]["file"], f"{record['id']}-authority-original")
        # The reviewer uses the registered base saved beside the candidate.
        registered_authority = ROOT / record["candidate"]["file"]
        registered_authority = EVIDENCE / f"{record['id']}-authority.png"
        record["registeredAuthorityUrl"] = publish(registered_authority, f"{record['id']}-authority")
        record["maskUrl"] = publish(ROOT / record["upperBodyOverride"]["file"], f"{record['id']}-mask")
        record["guideUrl"] = publish(ROOT / record["gripGuide"]["file"], f"{record['id']}-guide")

    walk_sheet_url = publish(walk_sheet, "walk-contact-sheet")
    turn_sheet_url = publish(turn_sheet, "turn-contact-sheet")
    comparison_url = publish(comparison_sheet, "authority-comparison")

    route: list[dict] = []
    root = 68.0
    for index in range(1, 9):
        route.append({"recordId": f"walk{index}", "mirror": False, "rootXLp": round(root, 3),
                      "phase": "held walk right", "durationMs": WALK_MS})
        root += 21 / 8
    for index in range(1, 10):
        route.append({"recordId": f"turn{index}", "mirror": False, "rootXLp": round(root, 3),
                      "phase": "held turn side-right to back", "durationMs": TURN_MS})
    for index in range(8, 0, -1):
        route.append({"recordId": f"turn{index}", "mirror": True, "rootXLp": round(root, 3),
                      "phase": "held turn back to side-left", "durationMs": TURN_MS})
    for index in range(1, 9):
        root -= 21 / 8
        route.append({"recordId": f"walk{index}", "mirror": True, "rootXLp": round(root, 3),
                      "phase": "held walk left", "durationMs": WALK_MS})

    data = {
        "schema": "lighthouse-keeper/upper-body-override-poc@1", "set": SET,
        "status": "versioned-reversible-proof-of-concept-not-approved",
        "cell": {"sourcePixels": list(CELL), "density": 8, "logical": [48, 40], "rootX": ROOT_X, "floorY": FLOOR_Y},
        "frames": records, "route": route,
        "walkSheet": walk_sheet_url, "turnSheet": turn_sheet_url, "comparisonSheet": comparison_url,
        "reviewInstruction": "Judge only the feasibility of a clean two-hand shaft-grip pose through the approved gait phases and turn angles. This POC is phase-matched, not pixel-identical production art. No implement is present.",
    }
    data_file = PACK / f"{SET}.json"
    dump(data_file, data)

    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET,
        "status": "prime-upper-body-override-poc-awaiting-frank",
        "purpose": "Smallest motion-feasibility proof: a reusable two-hand shaft-grip pose across the approved locomotion phases and turn angles.",
        "supersedes": {"set": "keeper-prime-sweep-broom-v8", "status": "rejected-provenance",
                       "reason": "V8 overlaid held limbs without removing the approved swinging limbs, producing four arms/hands and visible pixel breakup."},
        "scope": {"implementIncluded": False, "cupboardIncluded": False, "activityLoopIncluded": False,
                  "walkFrames": 8, "turnFrames": 9, "combinedPlaybackFrames": len(route),
                  "gripProfile": "hold_shaft_two_hand"},
        "authorities": {
            "approvedWalkV6": [{"frame": i, "file": rel(path), "sha256": sha(path)} for i, path in enumerate(walk_files, 1)],
            "approvedTurnV9": [{"frame": i, "angleDegrees": ANGLES[i - 1], "file": rel(path), "sha256": sha(path)} for i, path in enumerate(turn_files, 1)],
            "primeRig": {"file": rel(RIG), "sha256": sha(RIG)},
            "requestedGripReference": {"file": rel(SWEEP3), "sha256": sha(SWEEP3), "role": "joint relationship only; no prop pixels survive"},
            "generatedTurnSource": {"file": rel(TURN_SOURCE_SHEET), "sha256": sha(TURN_SOURCE_SHEET),
                                    "role": "broomless nine-cell upper-body pose source"},
        },
        "construction": {
            "method": "phase-matched full-character proxy; never overlay held limbs on the complete authority",
            "headLockedToExactAuthority": False, "lowerBodyLockedToExactAuthority": False,
            "outsideOverrideByteIdentical": False, "candidateColoursMappedToMatchingFrameAuthority": True,
            "productionMethodStillRequired": "author separable Prime torso/arm layers before any production promotion",
            "propPixels": 0, "maximumVisibleHandComponents": 2,
            "walkOrderBothDirections": list(range(1, 9)),
            "turnOrder": list(range(1, 10)) + list(range(8, 0, -1)),
            "walkDurationMs": WALK_MS, "turnDurationMs": TURN_MS,
            "walkRootDeltaHighResolutionPixels": 21, "walkRootDeltaLogicalPixels": 21 / 8,
        },
        "candidate": {"frames": list(records.values()), "route": {"file": rel(data_file), "sha256": sha(data_file)},
                      "walkContactSheet": {"file": rel(walk_sheet), "sha256": sha(walk_sheet)},
                      "turnContactSheet": {"file": rel(turn_sheet), "sha256": sha(turn_sheet)},
                      "comparisonSheet": {"file": rel(comparison_sheet), "sha256": sha(comparison_sheet)},
                      "reviewUrl": f"/keeper-review/{SET}/"},
        "publishedAssets": published,
        "approvalBoundary": {"pocApproved": False, "gripProfileApproved": False, "implementApproved": False,
                             "productionPromotionAllowed": False, "productionChanged": False, "runtimeChanged": False},
        "rollback": f"Delete only {rel(PACK)}, public/keeper-review/{SET}, scripts/build_keeper_prime_upper_body_override_poc_v1.py and scripts/verify_keeper_prime_upper_body_override_poc_v1.mjs.",
    }
    dump(PACK / "batch-register.json", register)
    (PACK / "HANDOFF.md").write_text(
        "# Prime Keeper upper-body override POC V1\n\n"
        "This is not a broom animation. It tests one reusable `hold_shaft_two_hand` profile through the approved Walk V6 gait phases and Turn V9 angles. "
        "The original swinging arms are replaced, not overlaid. This is deliberately a clean full-character motion proxy, not pixel-identical production art; the prop layer is empty. "
        "Nothing is approved, promoted or wired into runtime.\n"
    )
    (PACK / "PROMPT_LOG.md").write_text(
        "# Source-art record\n\n"
        "Mode: built-in image editing (`image_gen`), identity-preserving precise-object edit. The selected generated turn grid is retained unchanged at "
        f"`{rel(TURN_SOURCE_SHEET)}` (SHA-256 `{sha(TURN_SOURCE_SHEET)}`). The eight existing V7 walk studies remain upper-body pose sources only. "
        "V1 is a motion-feasibility proxy: it replaces the complete character, removes the original arms, follows the approved gait phases and turn angles, includes no prop layer and maps every visible RGB value to the matching approved authority frame. A later production candidate must be rebuilt from separable Prime torso/arm layers and restore pixel-identical authority outside those layers.\n\n"
        "## Selected turn-source prompt\n\n"
        "Use case: precise-object-edit. Asset type: transparent 3-by-3 game-animation contact sheet. Remove only the broom and every broom-derived brown, gold, straw, ferrule and handle pixel from all nine cells. Reconstruct the small portions of jumper and trousers that the broom covers. Keep both hands naturally closed around the same invisible straight shaft position, with empty transparent space between them. Preserve the exact nine characters, poses, turn progression, cell order, scale, floor registration, Prime identity, uniform, colours and antialiasing. Exactly two anatomically connected arms and no more than two hands per cell. Genuine transparent background.\n"
    )

    (PACK / "reviewer.html").write_text(reviewer_html(data))
    shell = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper upper-body override POC V1</title><style>html,body,iframe{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}#loading{padding:24px}iframe{display:none}</style><p id="loading">Loading immutable Prime Keeper upper-body override POC V1…</p><iframe id="review" title="Prime Keeper upper-body override POC V1 reviewer"></iframe><script>fetch("https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/__POC_COMMIT__/art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v1/reviewer.html").then(r=>{if(!r.ok)throw Error('reviewer '+r.status);return r.text()}).then(t=>{document.querySelector('#review').srcdoc=t;document.querySelector('#review').style.display='block';document.querySelector('#loading').remove()}).catch(e=>document.querySelector('#loading').textContent='Reviewer failed to load: '+e.message)</script></html>'''
    (PUBLIC / "index.html").write_text(shell)
    print(json.dumps({"set": SET, "uniqueFrames": len(records), "playbackFrames": len(route),
                      "publishedAssets": len(published)}, indent=2))


def reviewer_html(data: dict) -> str:
    payload = json.dumps(data, separators=(",", ":"))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime upper-body override POC V1</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#07131b;color:#edf8fb;font:14px/1.45 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:18px}}.tag{{display:inline-block;border:1px solid #e6bd5c;color:#ffe4a0;border-radius:999px;padding:4px 9px;margin-right:6px}}.notice{{border-left:4px solid #5ad4df;background:#102c36;padding:11px 14px}}.panel{{background:#10232d;border:1px solid #294a57;border-radius:12px;padding:14px;margin:14px 0}}.controls{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}button,input,select{{font:inherit}}button,select{{background:#173d52;color:white;border:1px solid #537788;border-radius:7px;padding:7px 10px}}button:disabled,input:disabled,select:disabled{{opacity:.45}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.stagewrap{{overflow:auto;background:#061018;padding:8px}}.stage{{position:relative;width:192px;height:56px;overflow:hidden;background:linear-gradient(#1a2d36 0 92.8%,#4d555b 92.8%)}}.stage img{{position:absolute;width:48px;height:40px;bottom:4px;object-fit:fill}}.ghost{{opacity:.26;filter:hue-rotate(110deg) saturate(1.7)}}.guide{{z-index:4}}.candidate{{z-index:3}}.prior{{z-index:2}}.compare{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}}.compare img,.sheet{{max-width:100%;height:auto;background:repeating-conic-gradient(#243640 0 25%,#162630 0 50%) 0/16px 16px}}.warning{{color:#ffd38b}}@media(max-width:900px){{.grid,.compare{{grid-template-columns:1fr}}}}</style></head><body><header><h1>Prime Keeper · upper-body override POC V1</h1><span class="tag">No broom</span><span class="tag">Two-hand shaft grip</span><span class="tag">Nothing promoted</span><p class="notice"><strong>This tests motion feasibility, not production art.</strong> Walk V6 gait phases and Turn V9 angles remain the movement authorities. The frames are clean phase-matched proxies with exactly one held-pose arm set; they are intentionally not claimed as pixel-identical Walk/Turn authority. The cyan grip axis is a reviewer overlay, never character art.</p></header><main><section class="panel"><div id="loading">Loading and decoding every unique frame… controls remain locked.</div><div class="controls"><button id="play" disabled>Play</button><button id="prev" disabled>Previous</button><button id="next" disabled>Next</button><select id="clip" disabled><option value="all">Combined 33-frame POC</option><option value="walk-right">Walk right · 8 frames</option><option value="turn">Full turn · 17 frames</option><option value="walk-left">Walk left · 8 frames</option></select><label>Speed <input id="speed" disabled type="range" min="0.35" max="1.25" value="0.65" step="0.05"></label><label><input id="ghost" disabled type="checkbox"> Previous-frame ghost</label><label><input id="guide" disabled type="checkbox" checked> Grip-axis overlay</label></div><p class="warning">The direct walk→turn and turn→walk joins are only a compact technical splice. A production action would add the approved stop/start bridges and rebuild from separable Prime torso/arm layers.</p><p id="caption"></p></section><section class="panel"><div class="grid"><div><h2>Large inspection · 6 px/lp</h2><div class="stagewrap"><div class="stage" id="large"></div></div></div><div><h2>Gameplay scale · 4 px/lp</h2><div class="stagewrap"><div class="stage" id="game"></div></div></div><div><h2>Literal 1× · 1 px/lp</h2><div class="stagewrap"><div class="stage" id="literal"></div></div></div><div><h2>Frame comparison</h2><div class="compare"><div><strong>Exact authority</strong><img id="authority"></div><div><strong>Phase-matched POC</strong><img id="candidate"></div><div><strong>POC ownership mask</strong><img id="mask"></div></div></div></div></section><section class="panel"><h2>Approved gait phases · held-pose proxy</h2><img class="sheet" src="{data['walkSheet']}"><h2>Approved turn angles · held-pose proxy</h2><img class="sheet" src="{data['turnSheet']}"><h2>Frame-by-frame Prime comparison</h2><img class="sheet" src="{data['comparisonSheet']}"></section></main><script>
const DATA={payload};let sequence=DATA.route,i=0,timer=null;const stages=[];function make(id,scale){{const host=document.querySelector('#'+id);host.style.width=192*scale+'px';host.style.height=56*scale+'px';for(const item of [['prior','ghost prior'],['candidate','candidate'],['guide','guide']]){{const img=document.createElement('img');img.dataset.layer=item[0];img.className=item[1];host.append(img)}}stages.push({{host,scale}})}}make('large',6);make('game',4);make('literal',1);
function clip(){{const choice=document.querySelector('#clip').value;if(choice==='walk-right')return DATA.route.slice(0,8);if(choice==='turn')return DATA.route.slice(8,25);if(choice==='walk-left')return DATA.route.slice(25);return DATA.route}}function place(stage,img,record,frame,src){{img.src=src;img.style.width=48*stage.scale+'px';img.style.height=40*stage.scale+'px';img.style.left=(frame.rootXLp-18.75)*stage.scale+'px';img.style.top=12*stage.scale+'px';img.style.transform=frame.mirror?'scaleX(-1)':'none'}}function show(){{const frame=sequence[i],record=DATA.frames[frame.recordId],priorFrame=sequence[(i-1+sequence.length)%sequence.length],priorRecord=DATA.frames[priorFrame.recordId],ghost=document.querySelector('#ghost').checked,guide=document.querySelector('#guide').checked;for(const stage of stages){{const q=n=>stage.host.querySelector('[data-layer='+n+']');place(stage,q('candidate'),record,frame,record.candidateUrl);place(stage,q('guide'),record,frame,record.guideUrl);place(stage,q('prior'),priorRecord,priorFrame,priorRecord.candidateUrl);q('prior').style.display=ghost?'block':'none';q('guide').style.display=guide?'block':'none'}}document.querySelector('#authority').src=record.registeredAuthorityUrl;document.querySelector('#candidate').src=record.candidateUrl;document.querySelector('#mask').src=record.maskUrl;document.querySelector('#caption').textContent=`${{i+1}}/${{sequence.length}} · ${{frame.phase}} · ${{record.id}} · visible hand components ${{record.hands.visibleComponentCount}}`;}}function stop(){{if(timer)clearTimeout(timer);timer=null;document.querySelector('#play').textContent='Play'}}function tick(){{const frame=sequence[i];i=(i+1)%sequence.length;show();timer=setTimeout(tick,frame.durationMs/Number(document.querySelector('#speed').value))}}document.querySelector('#play').onclick=()=>{{if(timer)stop();else{{document.querySelector('#play').textContent='Pause';tick()}}}};document.querySelector('#prev').onclick=()=>{{stop();i=(i-1+sequence.length)%sequence.length;show()}};document.querySelector('#next').onclick=()=>{{stop();i=(i+1)%sequence.length;show()}};document.querySelector('#clip').onchange=()=>{{stop();sequence=clip();i=0;show()}};document.querySelector('#ghost').onchange=show;document.querySelector('#guide').onchange=show;
const urls=new Set([DATA.walkSheet,DATA.turnSheet,DATA.comparisonSheet]);for(const record of Object.values(DATA.frames))for(const key of ['candidateUrl','registeredAuthorityUrl','maskUrl','guideUrl'])urls.add(record[key]);Promise.all([...urls].map(src=>new Promise((ok,bad)=>{{const img=new Image();img.onload=()=>img.decode?img.decode().then(ok,bad):ok();img.onerror=bad;img.src=src}}))).then(()=>{{document.querySelector('#loading').textContent=`${{urls.size}} unique images loaded and decoded. Controls enabled.`;document.querySelectorAll('button,input,select').forEach(x=>x.disabled=false);show();}}).catch(e=>document.querySelector('#loading').textContent='Media failed: '+e);
</script></body></html>'''


if __name__ == "__main__":
    main()
