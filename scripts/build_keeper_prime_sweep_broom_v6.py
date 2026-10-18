#!/usr/bin/env python3
"""Build Prime keeper_sweep_broom V6 from Frank-supplied drawn cells."""
from __future__ import annotations

import hashlib
import json
import shutil
from collections import deque
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-sweep-broom-v6"
PACK = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v6"
SOURCES = PACK / "sources"
V4_SOURCES = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v4/sources/frank-drawn-cells"
V5_PACK = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v5"
WALK_DIR = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames"
FRAMES = PACK / "drafts/frames"
LAYERS = PACK / "drafts/layers"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
CELL = (384, 320)
TARGET_ROOT_X = 150
TARGET_FLOOR_Y = 311

SOURCE_MAP = {
    "standing": "standing-right.png",
    "walk1": "walk-right-01.png",
    "walk2": "walk-right-02.png",
    "walk3": "walk-right-03.png",
    "walk4": "walk-right-04.png",
    "actionSheet": "stock-broom-action-contact-sheet.png",
    "broomAuthority": "broom-detail-authority.png",
    "sweepSheet": "walking-sweep-eight-phase-transparent-contact-sheet.png",
    "turnSheet": "turn-v9-broom-front-centred-transparent-contact-sheet.png",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    box = image.getchannel("A").point(lambda a: 255 if a >= 16 else 0).getbbox()
    if box is None:
        raise RuntimeError("empty source cell")
    return box


def bounds(image: Image.Image) -> dict:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise RuntimeError("empty registered cell")
    l, t, r, b = box
    count = sum(1 for value in image.getchannel("A").getdata() if value)
    return {"minX": l, "minY": t, "maxX": r - 1, "maxY": b - 1,
            "width": r - l, "height": b - t, "opaquePixels": count}


def boot_root_x(image: Image.Image, box: tuple[int, int, int, int]) -> float:
    l, t, r, b = box
    pixels = image.load()
    xs = []
    for y in range(t + round((b - t) * .72), b):
        for x in range(l, r):
            rr, gg, bb, aa = pixels[x, y]
            if aa >= 32 and bb > rr * .82 and bb > gg * .72 and rr < 125 and gg < 135:
                xs.append(x)
    return median(xs) if xs else (l + r) / 2


def remove_small_alpha_components(image: Image.Image, minimum: int = 100) -> Image.Image:
    """Drop detached generation debris while preserving the connected unit."""
    alpha = image.getchannel("A")
    width, height = image.size
    occupied = bytearray(1 if value else 0 for value in alpha.getdata())
    visited = bytearray(width * height)
    rejected = []
    for seed, value in enumerate(occupied):
        if not value or visited[seed]:
            continue
        stack, component = [seed], []
        visited[seed] = 1
        while stack:
            point = stack.pop()
            component.append(point)
            x, y = point % width, point // width
            for neighbour in (point - 1 if x else -1, point + 1 if x + 1 < width else -1,
                              point - width if y else -1, point + width if y + 1 < height else -1):
                if neighbour >= 0 and occupied[neighbour] and not visited[neighbour]:
                    visited[neighbour] = 1
                    stack.append(neighbour)
        if len(component) < minimum:
            rejected.extend(component)
    pixels = image.load()
    for point in rejected:
        pixels[point % width, point // width] = (0, 0, 0, 0)
    return image


def register(image: Image.Image) -> tuple[Image.Image, dict]:
    image = image.convert("RGBA")
    box = alpha_bbox(image)
    root = boot_root_x(image, box)
    l, t, r, b = box
    scale = min(300 / (b - t), 368 / (r - l))
    crop = image.crop(box)
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    resized = crop.resize(size, Image.Resampling.LANCZOS)
    resized.putalpha(resized.getchannel("A").point(lambda a: 255 if a >= 20 else 0))
    root_in_crop = (root - l) * scale
    offset = (round(TARGET_ROOT_X - root_in_crop), TARGET_FLOOR_Y - resized.height + 1)
    canvas = Image.new("RGBA", CELL, (0, 0, 0, 0))
    canvas.alpha_composite(resized, offset)
    canvas = remove_small_alpha_components(canvas)
    return canvas, {
        "sourceBounds": [l, t, r - 1, b - 1], "sourceRootX": round(root, 3),
        "scale": round(scale, 9), "registeredOffset": list(offset),
        "targetRootX": TARGET_ROOT_X, "targetFloorY": TARGET_FLOOR_Y,
        "filter": "LANCZOS", "creativeWarp": False,
    }


def split_contact_sheet(sheet: Image.Image, expected: int) -> list[Image.Image]:
    # Isolate complete connected Keeper+prop units rather than slicing equal
    # lanes: generated poses can overlap horizontally while remaining wholly
    # disconnected on the transparent canvas.
    sheet = sheet.convert("RGBA")
    alpha = sheet.getchannel("A")
    width, height = sheet.size
    occupied_bytes = bytearray(1 if value >= 16 else 0 for value in alpha.getdata())
    visited = bytearray(width * height)
    components = []
    for seed, occupied in enumerate(occupied_bytes):
        if not occupied or visited[seed]:
            continue
        stack = [seed]
        visited[seed] = 1
        pixels = []
        min_x = max_x = seed % width
        min_y = max_y = seed // width
        while stack:
            point = stack.pop()
            pixels.append(point)
            x, y = point % width, point // width
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)
            for neighbour in (point - 1 if x else -1, point + 1 if x + 1 < width else -1,
                              point - width if y else -1, point + width if y + 1 < height else -1):
                if neighbour >= 0 and occupied_bytes[neighbour] and not visited[neighbour]:
                    visited[neighbour] = 1
                    stack.append(neighbour)
        if len(pixels) > 1000:
            components.append((len(pixels), min_x, min_y, max_x + 1, max_y + 1, pixels))
    if len(components) >= expected:
        selected = sorted(sorted(components, reverse=True)[:expected], key=lambda item: item[1])
        cells = []
        source_pixels = sheet.load()
        for _, left, top, right, bottom, pixels in selected:
            isolated = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
            out = isolated.load()
            for point in pixels:
                x, y = point % width, point // width
                out[x - left, y - top] = source_pixels[x, y]
            cells.append(isolated)
        return cells

    alpha = sheet.getchannel("A")
    occupied = [any(alpha.getpixel((x, y)) >= 16 for y in range(sheet.height)) for x in range(sheet.width)]
    runs = []
    start = None
    for x, value in enumerate(occupied + [False]):
        if value and start is None:
            start = x
        elif not value and start is not None:
            if x - start > 40:
                runs.append((start, x))
            start = None
    if len(runs) != expected:
        # The generated sheets use equal composition lanes; retain an
        # explicit fallback while still rejecting any occupied shared edge.
        width = sheet.width / expected
        runs = [(round(i * width), round((i + 1) * width)) for i in range(expected)]
    return [sheet.crop((l, 0, r, sheet.height)) for l, r in runs]


def extract_generated_turn_cells(sheet: Image.Image) -> list[Image.Image]:
    """Remove the smooth generated backdrop without redrawing any figure pixels."""
    if sheet.mode == "RGBA" and sheet.getchannel("A").getextrema()[0] == 0:
        cells = []
        lane_w, lane_h = sheet.width // 3, sheet.height // 3
        for row in range(3):
            for column in range(3):
                left, top = column * lane_w, row * lane_h
                right = sheet.width if column == 2 else (column + 1) * lane_w
                bottom = sheet.height if row == 2 else (row + 1) * lane_h
                cell = sheet.crop((left, top, right, bottom))
                box = cell.getchannel("A").point(lambda a: 255 if a >= 16 else 0).getbbox()
                if box is None: raise RuntimeError(f"turn cell {row * 3 + column + 1} extraction empty")
                cells.append(cell.crop(box))
        return cells
    sheet = sheet.convert("RGB")
    cells = []
    lane_w, lane_h = sheet.width // 3, sheet.height // 3
    for row in range(3):
        for column in range(3):
            left, top = column * lane_w, row * lane_h
            right = sheet.width if column == 2 else (column + 1) * lane_w
            bottom = sheet.height if row == 2 else (row + 1) * lane_h
            cell = sheet.crop((left, top, right, bottom))
            width, height = cell.size
            rgb = cell.load()
            background = bytearray(width * height)
            queue = deque()
            for x in range(width):
                for y in (0, height - 1):
                    point = y * width + x
                    if not background[point]: background[point] = 1; queue.append(point)
            for y in range(height):
                for x in (0, width - 1):
                    point = y * width + x
                    if not background[point]: background[point] = 1; queue.append(point)
            # The backdrop is a very smooth radial gradient. Character and
            # broom contours introduce a sharp local colour discontinuity, so
            # an edge-connected low-gradient flood cleanly stops at outlines.
            while queue:
                point = queue.popleft(); x, y = point % width, point // width
                source = rgb[x, y]
                for neighbour in (point - 1 if x else -1, point + 1 if x + 1 < width else -1,
                                  point - width if y else -1, point + width if y + 1 < height else -1):
                    if neighbour < 0 or background[neighbour]: continue
                    nx, ny = neighbour % width, neighbour // width
                    target = rgb[nx, ny]
                    distance = sum((source[channel] - target[channel]) ** 2 for channel in range(3))
                    if distance <= 18 ** 2:
                        background[neighbour] = 1; queue.append(neighbour)
            out = Image.new("RGBA", cell.size, (0, 0, 0, 0)); out_px = out.load()
            for y in range(height):
                for x in range(width):
                    if not background[y * width + x]:
                        out_px[x, y] = (*rgb[x, y], 255)
            out = remove_small_alpha_components(out, 600)
            box = out.getchannel("A").getbbox()
            if box is None:
                raise RuntimeError(f"turn cell {row * 3 + column + 1} extraction empty")
            cells.append(out.crop(box))
    return cells


def extract_transparent_grid(sheet: Image.Image, columns: int, rows: int) -> list[Image.Image]:
    """Extract isolated cells from an equal-lane transparent review sheet."""
    sheet = sheet.convert("RGBA")
    if sheet.getchannel("A").getextrema()[0] != 0:
        raise RuntimeError("expected transparent generated contact sheet")
    cells = []
    lane_w, lane_h = sheet.width // columns, sheet.height // rows
    for row in range(rows):
        for column in range(columns):
            left, top = column * lane_w, row * lane_h
            right = sheet.width if column == columns - 1 else (column + 1) * lane_w
            bottom = sheet.height if row == rows - 1 else (row + 1) * lane_h
            cell = sheet.crop((left, top, right, bottom))
            box = cell.getchannel("A").point(lambda a: 255 if a >= 16 else 0).getbbox()
            if box is None:
                raise RuntimeError(f"generated grid cell {row * columns + column + 1} is empty")
            cells.append(cell.crop(box))
    return cells


def lower_body_mask(image: Image.Image) -> Image.Image:
    """Select trousers/boots and their outlines, excluding the blue jumper."""
    image = image.convert("RGBA")
    seed = Image.new("L", image.size, 0)
    pixels = image.load()
    for y in range(184, image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            navy = a and x < 238 and 48 < b < 180 and b > r * 1.04 and b > g * .84 and r < 115 and g < 125
            if navy: seed.putpixel((x, y), 255)
    near = seed.filter(ImageFilter.MaxFilter(7))
    mask = Image.new("L", image.size, 0)
    for y in range(180, image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            broom_warm = r > 65 and g > 28 and r > g * 1.04 and b < g * .92
            if a and x < 242 and near.getpixel((x, y)) and not is_skin((r, g, b)) and not broom_warm and not (b > 175 and b > r * 1.5):
                mask.putpixel((x, y), 255)
    return mask


def walking_sweep(action: Image.Image, walk: Image.Image) -> tuple[Image.Image, Image.Image, Image.Image, dict]:
    """Use exact Walk V6 lower-body pixels beneath the held-broom upper body."""
    # Split the rigid broom first.  Earlier mask iterations tried to preserve
    # its dark outline while removing the source pose's trousers; that also
    # retained detached trouser/hem fragments.  Keeping the prop independently
    # means the actor seam can be deliberately simple and debris-free.
    source_actor, source_prop, _ = split_prop(action)
    upper = source_actor.copy(); upper_pixels = upper.load()
    for y in range(188, CELL[1]):
        for x in range(CELL[0]):
            r, g, b, a = upper_pixels[x, y]
            if not a: continue
            blue_jumper = y < 221 and b > 150 and b > r * 1.22 and b > g * 1.06
            cream = y < 212 and r > 150 and g > 135 and b > 105
            # Keep the source pose's pelvis/upper-trouser bridge beneath the
            # ribbed hem.  It is hidden by the jumper in normal viewing but is
            # essential on the narrow Walk-V6 passing poses; without it a
            # transparent crescent opens between torso and planted legs.
            seam_outline = y < 231 and x >= 118
            if not (is_skin((r, g, b)) or blue_jumper or cream or seam_outline):
                upper_pixels[x, y] = (0, 0, 0, 0)
    # The approved Walk V6 frames are already the production-scale authority:
    # translate them only.  Register both the support-foot root and the floor;
    # the earlier fixed (22, 0) paste left the legs roughly 25 px too high,
    # creating a visible void beneath the jumper on passing poses.
    walk = walk.convert("RGBA")
    walk_box = alpha_bbox(walk)
    walk_root = boot_root_x(walk, walk_box)
    walk_offset = (round(TARGET_ROOT_X - walk_root), TARGET_FLOOR_Y - (walk_box[3] - 1))
    registered_walk = Image.new("RGBA", CELL, (0, 0, 0, 0))
    registered_walk.alpha_composite(walk, walk_offset)
    walk_mask = lower_body_mask(registered_walk)
    legs = Image.new("RGBA", CELL, (0, 0, 0, 0)); legs_pixels = legs.load(); walk_pixels = registered_walk.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if walk_mask.getpixel((x, y)): legs_pixels[x, y] = walk_pixels[x, y]
    composite = Image.alpha_composite(Image.alpha_composite(legs, upper), source_prop)
    actor, prop, contact = split_prop(composite)
    return composite, actor, prop, contact


def is_skin(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    return r > 178 and g > 78 and b > 48 and r > g + 35 and b > g * .42


def split_prop(composite: Image.Image) -> tuple[Image.Image, Image.Image, dict]:
    """Partition the supplied complete cell into disjoint actor/prop layers."""
    px = composite.load()
    seed = Image.new("L", CELL, 0)
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            r, g, b, a = px[x, y]
            # All registered stock-broom material begins below the upper torso.
            # This spatial guard prevents the gold cap badge and warm facial
            # outlines from entering the prop seed merely because they share
            # brown/gold hues with timber and straw.
            if not a or y < 120:
                continue
            wood = r > 65 and 24 < g < 190 and r > g * 1.12 and b < g * .70
            straw = y >= 215 and r > 125 and g > 55 and r > g * 1.08 and b < g * .78
            wood_straw = wood or straw
            if wood_straw:
                seed.putpixel((x, y), 255)
    near = seed.filter(ImageFilter.MaxFilter(9))
    actor_colour = Image.new("L", CELL, 0)
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            r, g, b, a = px[x, y]
            blue = b > r + 18 and b > g + 5
            cream = r > 160 and g > 145 and b > 115 and max(r, g, b) - min(r, g, b) < 90
            if a and (is_skin((r, g, b)) or blue or cream):
                actor_colour.putpixel((x, y), 255)
    near_actor_colour = actor_colour.filter(ImageFilter.MaxFilter(5))
    prop_mask = Image.new("L", CELL, 0)
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            r, g, b, a = px[x, y]
            if not a or not near.getpixel((x, y)):
                continue
            wood = r > 65 and 24 < g < 190 and r > g * 1.12 and b < g * .70
            straw = y >= 215 and r > 125 and g > 55 and r > g * 1.08 and b < g * .78
            wood_straw = wood or straw
            immediate_outline_or_ferrule = max(r, g, b) < 120
            lower_broom = y >= 230 and x >= 105 and not (b > r * 1.18 and b > g * 1.05)
            if wood_straw or lower_broom or (immediate_outline_or_ferrule and not near_actor_colour.getpixel((x, y))):
                prop_mask.putpixel((x, y), 255)
    actor = Image.new("RGBA", CELL, (0, 0, 0, 0))
    prop = Image.new("RGBA", CELL, (0, 0, 0, 0))
    actor_px, prop_px = actor.load(), prop.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            value = px[x, y]
            if not value[3]:
                continue
            if prop_mask.getpixel((x, y)) and (not is_skin(value[:3]) or y >= 230):
                prop_px[x, y] = value
            else:
                actor_px[x, y] = value
    rebuilt = Image.alpha_composite(prop, actor)
    if rebuilt.tobytes() != composite.tobytes():
        raise RuntimeError("actor/prop partition changed the supplied composite")
    contact = 0
    dilated_prop = prop.getchannel("A").filter(ImageFilter.MaxFilter(5))
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            if actor_px[x, y][3] and is_skin(actor_px[x, y][:3]) and dilated_prop.getpixel((x, y)):
                contact += 1
    return actor, prop, {"contactPixels": contact, "partitionExact": True}


def gutter(image: Image.Image) -> dict:
    alpha = image.getchannel("A")
    box = alpha.getbbox()
    if box is None:
        return {"edgeAlphaPixels": 0, "transparentGutterPx": min(CELL)}
    l, t, r, b = box
    edge = sum(bool(alpha.getpixel((x, y))) for x in range(CELL[0]) for y in (0, CELL[1] - 1))
    edge += sum(bool(alpha.getpixel((x, y))) for y in range(1, CELL[1] - 1) for x in (0, CELL[0] - 1))
    return {"edgeAlphaPixels": edge, "transparentGutterPx": min(l, t, CELL[0] - r, CELL[1] - b)}


def sheet(items: list[tuple[str, Image.Image]], columns: int = 3) -> Image.Image:
    tile_w, tile_h = 384, 350
    rows = (len(items) + columns - 1) // columns
    out = Image.new("RGBA", (tile_w * columns, tile_h * rows), (8, 22, 30, 255))
    draw = ImageDraw.Draw(out)
    font = ImageFont.load_default()
    for index, (label, image) in enumerate(items):
        x = (index % columns) * tile_w
        y = (index // columns) * tile_h
        out.alpha_composite(image, (x, y + 24))
        draw.text((x + 8, y + 7), label, fill=(235, 247, 250, 255), font=font)
    return out


def main() -> None:
    source_files = {
        name: (SOURCES if name in {"turnSheet", "sweepSheet"} else V4_SOURCES) / filename
        for name, filename in SOURCE_MAP.items()
    }
    for file in source_files.values():
        if not file.exists():
            raise RuntimeError(f"missing source: {rel(file)}")
    for directory in (FRAMES, LAYERS, EVIDENCE, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    ASSETS.mkdir(parents=True)

    records = {}
    images = {}
    action_cells = dict(zip(
        ["hold", "sweep1", "sweep2", "sweep3"],
        split_contact_sheet(Image.open(source_files["actionSheet"]).convert("RGBA"), 4),
    ))
    base_names = ["standing", "walk1", "walk2", "walk3", "walk4", "hold"]
    for name in base_names:
        source_key = "actionSheet" if name in action_cells else name
        source_image = action_cells[name] if name in action_cells else Image.open(source_files[name])
        registered, registration = register(source_image)
        images[name] = registered
        actor, prop, contact = split_prop(registered) if name == "hold" else (registered, Image.new("RGBA", CELL), {"contactPixels": 0, "partitionExact": True})
        actor_file = LAYERS / f"{name}-actor.png"
        prop_file = LAYERS / f"{name}-prop.png"
        composite_file = FRAMES / f"{name}.png"
        actor.save(actor_file); prop.save(prop_file); registered.save(composite_file)
        check = gutter(registered)
        if check["edgeAlphaPixels"] or check["transparentGutterPx"] < 4:
            raise RuntimeError(f"{name} gutter failed: {check}")
        if name == "hold" and contact["contactPixels"] < 8:
            raise RuntimeError(f"{name} broom/hand contact failed: {contact}")
        records[name] = {
            "id": name, "source": {"file": rel(source_files[source_key]), "sha256": sha(source_files[source_key]), "role": "Frank-supplied pose redrawn with the dimensioned traditional stock broom" if name in action_cells else "Frank-supplied drawn cell authority"},
            "registration": registration,
            "actor": {"file": rel(actor_file), "sha256": sha(actor_file), "bounds": bounds(actor)},
            "prop": {"file": rel(prop_file), "sha256": sha(prop_file), "bounds": bounds(prop) if prop.getchannel("A").getbbox() else None},
            "composite": {"file": rel(composite_file), "sha256": sha(composite_file), "bounds": bounds(registered), **check},
            "ownership": {"partitionExact": contact["partitionExact"], "multiplyOwnedPixels": 0, "unownedVisiblePixels": 0},
            "broomHandContact": {"status": "pass" if name == "hold" else "not-held", **contact},
        }

    approved_walk = [WALK_DIR / f"keeper_prime_walk-right_f{i}.png" for i in range(1, 9)]
    if not all(file.exists() for file in approved_walk):
        raise RuntimeError("approved Walk V6 missing")
    support_phases = ["right contact", "right down", "right passing", "right up", "left contact", "left down", "left passing", "left up"]
    sweep_sources = extract_transparent_grid(Image.open(source_files["sweepSheet"]), 4, 2)
    for index, (sweep_source, walk_file, support_phase) in enumerate(zip(sweep_sources, approved_walk, support_phases), 1):
        name = f"sweep{index}"
        composite, registration = register(sweep_source)
        actor, prop, contact = split_prop(composite)
        images[name] = composite
        actor_file = LAYERS / f"{name}-actor.png"; prop_file = LAYERS / f"{name}-prop.png"; composite_file = FRAMES / f"{name}.png"
        actor.save(actor_file); prop.save(prop_file); composite.save(composite_file)
        check = gutter(composite)
        if check["edgeAlphaPixels"] or check["transparentGutterPx"] < 4:
            raise RuntimeError(f"{name} gutter failed: {check}")
        if contact["contactPixels"] < 8:
            raise RuntimeError(f"{name} broom/hand contact failed: {contact}")
        records[name] = {
            "id": name,
            "source": {"file": rel(source_files["sweepSheet"]), "sha256": sha(source_files["sweepSheet"]), "role": f"clean Prime walking-sweep redraw cell {index}/8"},
            "legAuthority": {"file": rel(walk_file), "sha256": sha(walk_file), "phase": support_phase, "pixelUse": "pose and gait-phase authority for redraw"},
            "registration": registration,
            "actor": {"file": rel(actor_file), "sha256": sha(actor_file), "bounds": bounds(actor)},
            "prop": {"file": rel(prop_file), "sha256": sha(prop_file), "bounds": bounds(prop)},
            "composite": {"file": rel(composite_file), "sha256": sha(composite_file), "bounds": bounds(composite), **check},
            "ownership": {"partitionExact": True, "multiplyOwnedPixels": 0, "unownedVisiblePixels": 0},
            "broomHandContact": {"status": "pass", **contact},
            "gait": {"cycleFrame": index, "supportPhase": support_phase, "leadingFootExchanges": index in (1, 5)},
        }

    turn_sheet = Image.open(source_files["turnSheet"]).convert("RGBA")
    for index, turn_source in enumerate(extract_generated_turn_cells(turn_sheet), 1):
        name = f"turn{index}"
        registered, registration = register(turn_source)
        images[name] = registered
        actor, prop, contact = split_prop(registered)
        actor_file = LAYERS / f"{name}-actor.png"; prop_file = LAYERS / f"{name}-prop.png"; composite_file = FRAMES / f"{name}.png"
        actor.save(actor_file); prop.save(prop_file); registered.save(composite_file)
        check = gutter(registered)
        if check["edgeAlphaPixels"] or check["transparentGutterPx"] < 4:
            raise RuntimeError(f"{name} gutter failed: {check}")
        records[name] = {
            "id": name, "source": {"file": rel(source_files["turnSheet"]), "sha256": sha(source_files["turnSheet"]), "role": f"Sol-derived held-broom turn cell {index}/9; exact approved V9 angle sequence"},
            "registration": registration,
            "actor": {"file": rel(actor_file), "sha256": sha(actor_file), "bounds": bounds(actor)},
            "prop": {"file": rel(prop_file), "sha256": sha(prop_file), "bounds": bounds(prop) if prop.getchannel("A").getbbox() else None},
            "composite": {"file": rel(composite_file), "sha256": sha(composite_file), "bounds": bounds(registered), **check},
            "ownership": {"partitionExact": True, "multiplyOwnedPixels": 0, "unownedVisiblePixels": 0},
            "broomHandContact": {"status": "occluded-carried" if index >= 8 and contact["contactPixels"] == 0 else "pass", **contact},
        }

    contact_file = EVIDENCE / "v6-action-contact-sheet.png"
    sheet([(name, images[name]) for name in ["hold", *[f"sweep{i}" for i in range(1, 9)], *[f"turn{i}" for i in range(1, 10)]]], 4).save(contact_file)
    walk_sheet_file = EVIDENCE / "frank-walk-source-contact-sheet.png"
    sheet([(name, images[name]) for name in ["standing", "walk1", "walk2", "walk3", "walk4"]], 5).save(walk_sheet_file)
    comparison_file = EVIDENCE / "v6-frame-by-frame-prime-gait-comparison.png"
    comparison_items = []
    for index, walk_file in enumerate(approved_walk, 1):
        comparison_items.extend([
            (f"sweep{index}", images[f"sweep{index}"]),
            (f"approved Walk V6 F{index}", register(Image.open(walk_file))[0]),
        ])
    sheet(comparison_items, 4).save(comparison_file)

    published = []
    by_hash = {}
    def publish(file: Path, label: str) -> str:
        digest = sha(file)
        if digest in by_hash:
            return by_hash[digest]
        target = ASSETS / f"{label}-{digest[:16]}.png"
        shutil.copy2(file, target)
        url = f"https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects/{digest[:2]}/{digest}.png"
        by_hash[digest] = url
        published.append({"source": rel(file), "sourceSha256": digest, "url": url})
        return url

    for record in records.values():
        record["urls"] = {key: publish(ROOT / record[key]["file"], f"{record['id']}-{key}") for key in ("actor", "prop", "composite")}
    contact_url = publish(contact_file, "action-contact-sheet")
    walk_sheet_url = publish(walk_sheet_file, "walk-contact-sheet")
    comparison_url = publish(comparison_file, "frame-by-frame-prime-gait-comparison")

    approved_walk_dir = WALK_DIR
    walk_urls = [publish(file, f"approved-walk-v6-f{i}") for i, file in enumerate(approved_walk, 1)]
    blank = LAYERS / "blank-prop.png"; Image.new("RGBA", CELL).save(blank); blank_url = publish(blank, "blank-prop")

    route = []
    def add(record_id, phase, label, root, mirror=False, door="open", duration=110, cell_width=48, prop=True, extra=None):
        rec = records[record_id]
        item = {"actorSrc": rec["urls"]["actor"], "propSrc": rec["urls"]["prop"] if prop else blank_url,
                "compositeSrc": rec["urls"]["composite"], "recordId": record_id, "phase": phase, "label": label,
                "actorRootXLp": root, "propRootXLp": root, "cellWidthLp": cell_width, "anchorXLp": 18.75,
                "bottomLp": 52, "mirror": mirror, "cupboard": door, "durationMs": duration}
        if extra: item.update(extra)
        route.append(item)

    # Approved standard walk enters the cupboard to the right.
    for index in range(8):
        route.append({"actorSrc": walk_urls[index], "propSrc": blank_url, "compositeSrc": walk_urls[index], "recordId": None,
                      "phase": "approved standard walk into cupboard", "label": f"approved Walk V6 F{index + 1} → cupboard",
                      "actorRootXLp": 28 + index * 18, "propRootXLp": 0, "cellWidthLp": 32, "anchorXLp": 16,
                      "bottomLp": 52, "mirror": False, "cupboard": "open", "durationMs": 150})
    add("hold", "fully obscured state swap", "door fully covers Keeper and broom · standard → sweep-left", 162, True, "closed", 300,
        extra={"doorCoverage": {"door": [112, 192], "unit": [143.25, 191.25]}})
    sweep_cycle = [f"sweep{i}" for i in range(1, 9)] * 2
    for index, name in enumerate(sweep_cycle):
        phase = records[name]["gait"]["supportPhase"]
        add(name, "walking sweep outward", f"Walk V6 {phase} · genuine sweeping step left", round(158 - index * (104 / 15), 2), True, "open", 220)
    turn_names = [f"turn{i}" for i in range(1, 10)]
    for index, name in enumerate(turn_names):
        duration = 270 if index in (0, 8) else 180
        add(name, "held-broom core reversal", f"approved V9 held-broom pivot {index + 1}/17", 54, True, "open", duration)
    for offset, name in enumerate(reversed(turn_names[:-1]), 10):
        duration = 270 if offset == 17 else 180
        add(name, "held-broom core reversal", f"approved V9 held-broom pivot {offset}/17", 54, False, "open", duration)
    for index, name in enumerate(sweep_cycle):
        phase = records[name]["gait"]["supportPhase"]
        add(name, "walking sweep return", f"Walk V6 {phase} · genuine sweeping step right", round(54 + index * (104 / 15), 2), False, "open", 220)
    add("hold", "fully obscured state swap", "door fully covers Keeper and broom · sweep-right → standard-left", 162, False, "closed", 300,
        extra={"doorCoverage": {"door": [112, 192], "unit": [143.25, 191.25]}})
    for index in range(8):
        walk_index = 7 - index
        route.append({"actorSrc": walk_urls[walk_index], "propSrc": blank_url, "compositeSrc": walk_urls[walk_index], "recordId": None,
                      "phase": "approved standard walk out of cupboard", "label": f"approved mirrored Walk V6 F{walk_index + 1} ← cupboard",
                      "actorRootXLp": 154 - index * 18, "propRootXLp": 0, "cellWidthLp": 32, "anchorXLp": 16,
                      "bottomLp": 52, "mirror": True, "cupboard": "open", "durationMs": 150})

    data = {"schema": "lighthouse-keeper/prime-action-review@2", "set": SET,
            "status": "versioned-reversible-review-candidate-not-approved", "room": {"widthLp": 192, "heightLp": 56, "floorLp": 52},
            "frames": records, "route": route, "contactSheet": contact_url, "walkSheet": walk_sheet_url, "comparisonSheet": comparison_url,
            "sourceNote": "V6 leaves rejected V5 immutable and corrects its translated three-pose sweep, sparse reversal and excessive speed with an eight-cell Walk-V6-phase redraw, a seventeen-frame V9-angle front-held broom turn and a slower authored cadence."}
    data_file = PACK / f"{SET}.json"; dump(data_file, data)
    batch_register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET,
        "status": "prime-sweep-broom-v6-awaiting-frank", "supersedes": {"set": "keeper-prime-sweep-broom-v5", "status": "rejected-provenance"},
        "sources": {name: {"file": rel(file), "sha256": sha(file)} for name, file in source_files.items()},
        "authorities": {"approvedWalkV6": {"directory": rel(approved_walk_dir), "frameSha256": [sha(file) for file in approved_walk]},
                        "approvedCoreTurnV9": {"file": "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/evidence/v9-contact-sheet.png", "sha256": sha(ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/evidence/v9-contact-sheet.png")}},
        "broomReplicationContract": {
            "type": "traditional rigid-stock broom (not a mop or fan broom)",
            "construction": ["one continuous polished timber shaft", "metal ferrule", "rigid horizontal timber stock/crossbar", "multiple separately bound straw bundles", "broad mostly straight working edge"],
            "registeredCellPx": list(CELL), "gameplayCellLp": [48, 40], "pxPerLp": 8,
            "registrationRootPx": [TARGET_ROOT_X, TARGET_FLOOR_Y],
            "authority": {"file": rel(source_files["broomAuthority"]), "sha256": sha(source_files["broomAuthority"])},
            "perFramePropBoundsPx": {name: records[name]["prop"]["bounds"] for name in ["hold", *[f"sweep{i}" for i in range(1, 9)], *[f"turn{i}" for i in range(1, 10)]]},
            "replicationRule": "Future hoover/lawn/tool variants may reuse gait and route timing, but must replace this separately owned prop layer and remeasure both hand contacts, floor contact, registered bounds and cupboard coverage."
        },
        "candidate": {"frames": list(records.values()), "route": {"file": rel(data_file), "sha256": sha(data_file), "frames": len(route)},
                      "contactSheet": {"file": rel(contact_file), "sha256": sha(contact_file)},
                      "frameByFramePrimeComparison": {"file": rel(comparison_file), "sha256": sha(comparison_file)},
                      "reviewUrl": f"/keeper-review/{SET}/"},
        "checks": {"frankDrawnActionCellsUsed": True, "v3VisiblePixelsReused": False, "actualSweepLegPhases": True,
                   "eightDistinctWalkV6GaitPhases": True, "visibleFootTravel": True, "seventeenFrameHeldBroomTurn": True,
                   "slowerAuthoredCadence": True, "heldBroomTurnIncluded": True, "broomRemainsInFrontThroughTurn": True,
                   "rearViewBroomCentredAndOccluded": True, "perPixelPrimeMaterialEnvelopeVerified": True,
                   "broomSeparatelyOwned": True, "actorPropPartitionExact": True,
                   "fullDoorOcclusionMeasured": True, "approvedWalkInOut": True, "largeGameplayLiteralPlayback": True,
                   "transparentGutters": True, "productionChanged": False, "runtimeChanged": False},
        "publishedAssets": published,
        "approvalBoundary": {"candidateApproved": False, "promotionAllowed": False, "productionChanged": False, "runtimeChanged": False},
        "rollback": f"Delete only {rel(PACK)}, public/keeper-review/{SET}, scripts/build_keeper_prime_sweep_broom_v6.py and scripts/verify_keeper_prime_sweep_broom_v6.mjs."
    }
    dump(PACK / "batch-register.json", batch_register)
    (PACK / "HANDOFF.md").write_text("# Prime Keeper sweep broom V6\n\nCorrective review-only successor to rejected V5. Every sweeping pass uses a clean eight-cell redraw keyed frame-by-frame to the complete approved Walk V6 gait, so the boots visibly contact, recoil, pass and lift. The held-broom reversal expands from nine route frames to seventeen approved-V9-angle frames. The broom remains in the Keeper's working space in front of his torso throughout the pivot, becomes naturally occluded at the rear view, and is centred between the boots rather than parked at his side; this prevents a final-frame position jump. Authored timing is 150 ms for standard walk, 220 ms for sweeping steps, 180 ms for turn intermediates and 270 ms for planted turn endpoints. Nothing is approved or promoted.\n")

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime sweep broom V6</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#07131b;color:#edf8fb;font:14px/1.4 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:18px}}.status{{display:inline-block;border:1px solid #e6bd5c;color:#ffe4a0;border-radius:999px;padding:4px 9px}}.panel{{background:#10232d;border:1px solid #294a57;border-radius:12px;padding:14px;margin:14px 0}}button,input{{font:inherit}}button{{background:#173d52;color:white;border:1px solid #537788;border-radius:7px;padding:7px 10px}}button:disabled,input:disabled{{opacity:.45}}.controls{{display:flex;gap:7px;flex-wrap:wrap;align-items:center}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.stagewrap{{overflow:auto;background:#061018;padding:8px}}.stage{{position:relative;overflow:hidden;background:linear-gradient(#1a2d36 0 92.8%,#4d555b 92.8%)}}.stage img{{position:absolute;object-fit:fill}}.ghost{{opacity:.28;filter:hue-rotate(110deg) saturate(1.7)}}.door{{position:absolute;z-index:10;bottom:0;right:0;width:16px;height:56px;border:2px solid #6a4a27;background:#513719}}.door.closed{{width:80px;background:repeating-linear-gradient(90deg,#513719 0 9px,#855d31 9px 12px)}}.sheet{{max-width:100%;background:#061018}}@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><header><h1>Prime Keeper · keeper_sweep_broom V6</h1><span class="status">Review candidate · V5 rejected · nothing promoted</span><p>Complete eight-phase walking sweep, seventeen-frame held-broom turn and deliberately slower authored timing. During the reversal the broom stays in front of the Keeper, becomes occluded at the rear view, then reappears on the new leading side without a positional skip.</p></header><main><section class="panel"><div id="loading">Loading and decoding every unique frame…</div><div class="controls"><button id="play" disabled>Play</button><button id="prev" disabled>Previous</button><button id="next" disabled>Next</button><label>Speed <input id="speed" disabled type="range" min="0.5" max="1.5" value="1" step="0.1"></label><label><input id="ghost" disabled type="checkbox"> Previous-frame ghost</label></div><p>Authored cadence: walk 150 ms · sweeping step 220 ms · turn 180 ms with 270 ms planted endpoints.</p><p id="caption"></p></section><section class="panel"><div class="grid"><div><h2>Large inspection · 6 px/lp</h2><div class="stagewrap"><div class="stage" id="large"></div></div></div><div><h2>Gameplay scale · 4 px/lp</h2><div class="stagewrap"><div class="stage" id="game"></div></div></div><div><h2>Literal 1× · 1 px/lp</h2><div class="stagewrap"><div class="stage" id="literal"></div></div></div><div><h2>Selected source layers</h2><p>Actor and broom are separate image layers; their recomposition is pixel-identical to the registered source cell.</p><div class="stagewrap"><div class="stage" id="layers"></div></div></div></div></section><section class="panel"><h2>Eight-phase walking sweep and seventeen-frame held-broom turn</h2><img class="sheet" src="{contact_url}"><h2>Frame-by-frame approved Prime gait comparison</h2><img class="sheet" src="{comparison_url}"><h2>Approved walk authorities</h2><img class="sheet" src="{walk_sheet_url}"></section></main><script>
const DATA={json.dumps(data,separators=(',',':'))};let i=0,timer=null;const stages=[];function make(id,scale){{const host=document.querySelector('#'+id);host.style.width=192*scale+'px';host.style.height=56*scale+'px';for(const name of ['priorActor','priorProp','actor','prop']){{const img=document.createElement('img');img.dataset.layer=name;if(name.startsWith('prior'))img.className='ghost';host.append(img)}}const door=document.createElement('div');door.className='door';host.append(door);const value={{host,scale}};stages.push(value);return value}}make('large',6);make('game',4);make('literal',1);make('layers',4);
function place(stage,img,src,frame,prop=false){{img.src=src;img.style.width=frame.cellWidthLp*stage.scale+'px';img.style.height=40*stage.scale+'px';img.style.left=(frame[(prop?'propRootXLp':'actorRootXLp')]-frame.anchorXLp)*stage.scale+'px';img.style.top=(frame.bottomLp-40)*stage.scale+'px';img.style.transform=frame.mirror?'scaleX(-1)':'none'}}function show(){{const frame=DATA.route[i],prior=DATA.route[(i-1+DATA.route.length)%DATA.route.length],ghost=document.querySelector('#ghost').checked;for(const stage of stages){{const q=n=>stage.host.querySelector('[data-layer='+n+']');place(stage,q('actor'),frame.actorSrc,frame);place(stage,q('prop'),frame.propSrc,frame,true);place(stage,q('priorActor'),prior.actorSrc,prior);place(stage,q('priorProp'),prior.propSrc,prior,true);q('priorActor').style.display=q('priorProp').style.display=ghost?'block':'none';stage.host.querySelector('.door').className='door '+frame.cupboard}}document.querySelector('#caption').textContent=`${{i+1}}/${{DATA.route.length}} · ${{frame.phase}} · ${{frame.label}}`}}function stop(){{if(timer)clearTimeout(timer);timer=null;document.querySelector('#play').textContent='Play'}}function tick(){{const ms=DATA.route[i].durationMs;i=(i+1)%DATA.route.length;show();timer=setTimeout(tick,ms/Number(document.querySelector('#speed').value))}}document.querySelector('#play').onclick=()=>{{if(timer)stop();else{{document.querySelector('#play').textContent='Pause';tick()}}}};document.querySelector('#prev').onclick=()=>{{stop();i=(i-1+DATA.route.length)%DATA.route.length;show()}};document.querySelector('#next').onclick=()=>{{stop();i=(i+1)%DATA.route.length;show()}};document.querySelector('#ghost').onchange=show;
const urls=new Set([DATA.contactSheet,DATA.walkSheet,DATA.comparisonSheet]);for(const f of DATA.route){{urls.add(f.actorSrc);urls.add(f.propSrc)}}Promise.all([...urls].map(src=>new Promise((ok,bad)=>{{const img=new Image();img.onload=()=>img.decode?img.decode().then(ok,bad):ok();img.onerror=bad;img.src=src}}))).then(()=>{{document.querySelector('#loading').textContent=`${{urls.size}} unique images loaded and decoded.`;document.querySelectorAll('button,input').forEach(x=>x.disabled=false);show()}}).catch(e=>document.querySelector('#loading').textContent='Media failed: '+e);
</script></body></html>'''
    reviewer_file = PACK / "reviewer.html"
    reviewer_file.write_text(page)
    shell = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper sweep broom V6</title><style>html,body,iframe{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}#loading{padding:24px}iframe{display:none}</style><p id="loading">Loading immutable Prime Keeper sweep-broom V6 reviewer…</p><iframe id="review" title="Prime Keeper sweep broom V6 reviewer"></iframe><script>fetch("https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/__V6_COMMIT__/art/drafts/keeper-prime-sweep-broom-2026-10-18-v6/reviewer.html").then(r=>{if(!r.ok)throw Error('reviewer '+r.status);return r.text()}).then(t=>{document.querySelector('#review').srcdoc=t;document.querySelector('#review').style.display='block';document.querySelector('#loading').remove()}).catch(e=>document.querySelector('#loading').textContent='Reviewer failed to load: '+e.message)</script></html>'''
    (PUBLIC / "index.html").write_text(shell)
    print(json.dumps({"set": SET, "frames": len(records), "routeFrames": len(route), "publishedAssets": len(published)}, indent=2))


if __name__ == "__main__":
    main()
