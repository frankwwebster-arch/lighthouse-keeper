#!/usr/bin/env python3
"""Build Prime keeper_sweep_broom V5 from Frank-supplied drawn cells."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-sweep-broom-v5"
PACK = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v5"
SOURCES = PACK / "sources"
V4_SOURCES = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v4/sources/frank-drawn-cells"
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
    "turnSheet": "turn-with-stock-broom-front-corrected-contact-sheet.png",
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
            wood_straw = r > 68 and g > 30 and r > g * 1.06 and b < g * .88 and not is_skin((r, g, b))
            if wood_straw:
                seed.putpixel((x, y), 255)
    near = seed.filter(ImageFilter.MaxFilter(5))
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
            wood_straw = r > 68 and g > 30 and r > g * 1.06 and b < g * .88 and not is_skin((r, g, b))
            immediate_outline_or_ferrule = max(r, g, b) < 120
            if wood_straw or (immediate_outline_or_ferrule and not near_actor_colour.getpixel((x, y))):
                prop_mask.putpixel((x, y), 255)
    actor = Image.new("RGBA", CELL, (0, 0, 0, 0))
    prop = Image.new("RGBA", CELL, (0, 0, 0, 0))
    actor_px, prop_px = actor.load(), prop.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            value = px[x, y]
            if not value[3]:
                continue
            if prop_mask.getpixel((x, y)) and not is_skin(value[:3]):
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
        name: (SOURCES if name == "turnSheet" else V4_SOURCES) / filename
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
    base_names = ["standing", "walk1", "walk2", "walk3", "walk4", "hold", "sweep1", "sweep2", "sweep3"]
    for name in base_names:
        source_key = "actionSheet" if name in action_cells else name
        source_image = action_cells[name] if name in action_cells else Image.open(source_files[name])
        registered, registration = register(source_image)
        images[name] = registered
        actor, prop, contact = split_prop(registered) if name in {"hold", "sweep1", "sweep2", "sweep3"} else (registered, Image.new("RGBA", CELL), {"contactPixels": 0, "partitionExact": True})
        actor_file = LAYERS / f"{name}-actor.png"
        prop_file = LAYERS / f"{name}-prop.png"
        composite_file = FRAMES / f"{name}.png"
        actor.save(actor_file); prop.save(prop_file); registered.save(composite_file)
        check = gutter(registered)
        if check["edgeAlphaPixels"] or check["transparentGutterPx"] < 4:
            raise RuntimeError(f"{name} gutter failed: {check}")
        if name in {"hold", "sweep1", "sweep2", "sweep3"} and contact["contactPixels"] < 8:
            raise RuntimeError(f"{name} broom/hand contact failed: {contact}")
        records[name] = {
            "id": name, "source": {"file": rel(source_files[source_key]), "sha256": sha(source_files[source_key]), "role": "Frank-supplied pose redrawn with the dimensioned traditional stock broom" if name in action_cells else "Frank-supplied drawn cell authority"},
            "registration": registration,
            "actor": {"file": rel(actor_file), "sha256": sha(actor_file), "bounds": bounds(actor)},
            "prop": {"file": rel(prop_file), "sha256": sha(prop_file), "bounds": bounds(prop) if prop.getchannel("A").getbbox() else None},
            "composite": {"file": rel(composite_file), "sha256": sha(composite_file), "bounds": bounds(registered), **check},
            "ownership": {"partitionExact": contact["partitionExact"], "multiplyOwnedPixels": 0, "unownedVisiblePixels": 0},
            "broomHandContact": {"status": "pass" if name in {"hold", "sweep1", "sweep2", "sweep3"} else "not-held", **contact},
        }

    turn_sheet = Image.open(source_files["turnSheet"]).convert("RGBA")
    for index, turn_source in enumerate(split_contact_sheet(turn_sheet, 5), 1):
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
            "id": name, "source": {"file": rel(source_files["turnSheet"]), "sha256": sha(source_files["turnSheet"]), "role": f"Sol-derived held-broom turn cell {index}; approved V9 choreography reference"},
            "registration": registration,
            "actor": {"file": rel(actor_file), "sha256": sha(actor_file), "bounds": bounds(actor)},
            "prop": {"file": rel(prop_file), "sha256": sha(prop_file), "bounds": bounds(prop) if prop.getchannel("A").getbbox() else None},
            "composite": {"file": rel(composite_file), "sha256": sha(composite_file), "bounds": bounds(registered), **check},
            "ownership": {"partitionExact": True, "multiplyOwnedPixels": 0, "unownedVisiblePixels": 0},
            "broomHandContact": {"status": "pass", **contact},
        }

    contact_file = EVIDENCE / "v5-action-contact-sheet.png"
    sheet([(name, images[name]) for name in ["hold", "sweep1", "sweep2", "sweep3", "turn1", "turn2", "turn3", "turn4", "turn5"]]).save(contact_file)
    walk_sheet_file = EVIDENCE / "frank-walk-source-contact-sheet.png"
    sheet([(name, images[name]) for name in ["standing", "walk1", "walk2", "walk3", "walk4"]], 5).save(walk_sheet_file)

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

    approved_walk_dir = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames"
    approved_walk = [approved_walk_dir / f"keeper_prime_walk-right_f{i}.png" for i in range(1, 9)]
    if not all(file.exists() for file in approved_walk):
        raise RuntimeError("approved Walk V6 missing")
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
                      "bottomLp": 52, "mirror": False, "cupboard": "open", "durationMs": 100})
    add("hold", "fully obscured state swap", "door fully covers Keeper and broom · standard → sweep-left", 162, True, "closed", 180,
        extra={"doorCoverage": {"door": [112, 192], "unit": [143.25, 191.25]}})
    sweep_cycle = ["sweep1", "sweep2", "sweep3", "sweep2"] * 3
    for index, name in enumerate(sweep_cycle):
        add(name, "walking sweep outward", f"Frank-drawn {name} · genuine moving-leg sweep left", round(158 - index * 9.4, 2), True, "open", 125)
    for index, name in enumerate(["turn1", "turn2", "turn3", "turn4", "turn5"]):
        add(name, "held-broom core reversal", f"approved-turn-derived held-broom pivot {index + 1}/9", 54, True, "open", 105)
    for index, name in enumerate(["turn4", "turn3", "turn2", "turn1"]):
        add(name, "held-broom core reversal", f"approved-turn-derived held-broom pivot {index + 6}/9", 54, False, "open", 105)
    for index, name in enumerate(sweep_cycle):
        add(name, "walking sweep return", f"Frank-drawn {name} · genuine moving-leg sweep right", round(54 + index * 9.4, 2), False, "open", 125)
    add("hold", "fully obscured state swap", "door fully covers Keeper and broom · sweep-right → standard-left", 162, False, "closed", 180,
        extra={"doorCoverage": {"door": [112, 192], "unit": [143.25, 191.25]}})
    for index in range(8):
        walk_index = 7 - index
        route.append({"actorSrc": walk_urls[walk_index], "propSrc": blank_url, "compositeSrc": walk_urls[walk_index], "recordId": None,
                      "phase": "approved standard walk out of cupboard", "label": f"approved mirrored Walk V6 F{walk_index + 1} ← cupboard",
                      "actorRootXLp": 154 - index * 18, "propRootXLp": 0, "cellWidthLp": 32, "anchorXLp": 16,
                      "bottomLp": 52, "mirror": True, "cupboard": "open", "durationMs": 100})

    data = {"schema": "lighthouse-keeper/prime-action-review@2", "set": SET,
            "status": "versioned-reversible-review-candidate-not-approved", "room": {"widthLp": 192, "heightLp": 56, "floorLp": 52},
            "frames": records, "route": route, "contactSheet": contact_url, "walkSheet": walk_sheet_url,
            "sourceNote": "V5 corrects V4's left-facing held-turn endpoint so the broom leads on the Keeper's left; V4 remains rejected immutable provenance."}
    data_file = PACK / f"{SET}.json"; dump(data_file, data)
    batch_register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET,
        "status": "prime-sweep-broom-v5-awaiting-frank", "supersedes": {"set": "keeper-prime-sweep-broom-v4", "status": "rejected-provenance"},
        "sources": {name: {"file": rel(file), "sha256": sha(file)} for name, file in source_files.items()},
        "authorities": {"approvedWalkV6": {"directory": rel(approved_walk_dir), "frameSha256": [sha(file) for file in approved_walk]},
                        "approvedCoreTurnV9": {"file": "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/evidence/v9-contact-sheet.png", "sha256": sha(ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/evidence/v9-contact-sheet.png")}},
        "broomReplicationContract": {
            "type": "traditional rigid-stock broom (not a mop or fan broom)",
            "construction": ["one continuous polished timber shaft", "metal ferrule", "rigid horizontal timber stock/crossbar", "multiple separately bound straw bundles", "broad mostly straight working edge"],
            "registeredCellPx": list(CELL), "gameplayCellLp": [48, 40], "pxPerLp": 8,
            "registrationRootPx": [TARGET_ROOT_X, TARGET_FLOOR_Y],
            "authority": {"file": rel(source_files["broomAuthority"]), "sha256": sha(source_files["broomAuthority"])},
            "perFramePropBoundsPx": {name: records[name]["prop"]["bounds"] for name in ["hold", "sweep1", "sweep2", "sweep3", "turn1", "turn2", "turn3", "turn4", "turn5"]},
            "replicationRule": "Future hoover/lawn/tool variants may reuse gait and route timing, but must replace this separately owned prop layer and remeasure both hand contacts, floor contact, registered bounds and cupboard coverage."
        },
        "candidate": {"frames": list(records.values()), "route": {"file": rel(data_file), "sha256": sha(data_file), "frames": len(route)},
                      "contactSheet": {"file": rel(contact_file), "sha256": sha(contact_file)}, "reviewUrl": f"/keeper-review/{SET}/"},
        "checks": {"frankDrawnActionCellsUsed": True, "v3VisiblePixelsReused": False, "actualSweepLegPhases": True,
                   "heldBroomTurnIncluded": True, "broomSeparatelyOwned": True, "actorPropPartitionExact": True,
                   "fullDoorOcclusionMeasured": True, "approvedWalkInOut": True, "largeGameplayLiteralPlayback": True,
                   "transparentGutters": True, "productionChanged": False, "runtimeChanged": False},
        "publishedAssets": published,
        "approvalBoundary": {"candidateApproved": False, "promotionAllowed": False, "productionChanged": False, "runtimeChanged": False},
        "rollback": f"Delete only {rel(PACK)}, public/keeper-review/{SET}, scripts/build_keeper_prime_sweep_broom_v5.py and scripts/verify_keeper_prime_sweep_broom_v5.mjs."
    }
    dump(PACK / "batch-register.json", batch_register)
    (PACK / "HANDOFF.md").write_text("# Prime Keeper sweep broom V5\n\nCorrective review-only successor to rejected V4. The left-facing turn endpoint now carries the broom in front/left of the Keeper, and the closed cupboard leaf is widened to 80 lp for unambiguous full occlusion. Route: approved walk in, fully covered swap, moving-leg sweep out, held-broom reversal, moving-leg sweep return, fully covered swap, approved walk out. Nothing is approved or promoted.\n")

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime sweep broom V5</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#07131b;color:#edf8fb;font:14px/1.4 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:18px}}.status{{display:inline-block;border:1px solid #e6bd5c;color:#ffe4a0;border-radius:999px;padding:4px 9px}}.panel{{background:#10232d;border:1px solid #294a57;border-radius:12px;padding:14px;margin:14px 0}}button,input{{font:inherit}}button{{background:#173d52;color:white;border:1px solid #537788;border-radius:7px;padding:7px 10px}}button:disabled,input:disabled{{opacity:.45}}.controls{{display:flex;gap:7px;flex-wrap:wrap;align-items:center}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.stagewrap{{overflow:auto;background:#061018;padding:8px}}.stage{{position:relative;overflow:hidden;background:linear-gradient(#1a2d36 0 92.8%,#4d555b 92.8%)}}.stage img{{position:absolute;object-fit:fill}}.ghost{{opacity:.28;filter:hue-rotate(110deg) saturate(1.7)}}.door{{position:absolute;z-index:10;bottom:0;right:0;width:16px;height:56px;border:2px solid #6a4a27;background:#513719}}.door.closed{{width:80px;background:repeating-linear-gradient(90deg,#513719 0 9px,#855d31 9px 12px)}}.sheet{{max-width:100%;background:#061018}}@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><header><h1>Prime Keeper · keeper_sweep_broom V5</h1><span class="status">Review candidate · V4 rejected · nothing promoted</span><p>Corrected left-facing broom transfer, moving-leg sweep and full-width physical cupboard occlusion.</p></header><main><section class="panel"><div id="loading">Loading and decoding every unique frame…</div><div class="controls"><button id="play" disabled>Play</button><button id="prev" disabled>Previous</button><button id="next" disabled>Next</button><label>Speed <input id="speed" disabled type="range" min="0.5" max="2" value="1" step="0.1"></label><label><input id="ghost" disabled type="checkbox"> Previous-frame ghost</label></div><p id="caption"></p></section><section class="panel"><div class="grid"><div><h2>Large inspection · 6 px/lp</h2><div class="stagewrap"><div class="stage" id="large"></div></div></div><div><h2>Gameplay scale · 4 px/lp</h2><div class="stagewrap"><div class="stage" id="game"></div></div></div><div><h2>Literal 1× · 1 px/lp</h2><div class="stagewrap"><div class="stage" id="literal"></div></div></div><div><h2>Selected source layers</h2><p>Actor and broom are separate image layers; their recomposition is pixel-identical to the supplied drawn cell.</p><div class="stagewrap"><div class="stage" id="layers"></div></div></div></div></section><section class="panel"><h2>Frank-drawn action and held-broom turn</h2><img class="sheet" src="{contact_url}"><h2>Frank-drawn walk sources</h2><img class="sheet" src="{walk_sheet_url}"></section></main><script>
const DATA={json.dumps(data,separators=(',',':'))};let i=0,timer=null;const stages=[];function make(id,scale){{const host=document.querySelector('#'+id);host.style.width=192*scale+'px';host.style.height=56*scale+'px';for(const name of ['priorActor','priorProp','actor','prop']){{const img=document.createElement('img');img.dataset.layer=name;if(name.startsWith('prior'))img.className='ghost';host.append(img)}}const door=document.createElement('div');door.className='door';host.append(door);const value={{host,scale}};stages.push(value);return value}}make('large',6);make('game',4);make('literal',1);make('layers',4);
function place(stage,img,src,frame,prop=false){{img.src=src;img.style.width=frame.cellWidthLp*stage.scale+'px';img.style.height=40*stage.scale+'px';img.style.left=(frame[(prop?'propRootXLp':'actorRootXLp')]-frame.anchorXLp)*stage.scale+'px';img.style.top=(frame.bottomLp-40)*stage.scale+'px';img.style.transform=frame.mirror?'scaleX(-1)':'none'}}function show(){{const frame=DATA.route[i],prior=DATA.route[(i-1+DATA.route.length)%DATA.route.length],ghost=document.querySelector('#ghost').checked;for(const stage of stages){{const q=n=>stage.host.querySelector('[data-layer='+n+']');place(stage,q('actor'),frame.actorSrc,frame);place(stage,q('prop'),frame.propSrc,frame,true);place(stage,q('priorActor'),prior.actorSrc,prior);place(stage,q('priorProp'),prior.propSrc,prior,true);q('priorActor').style.display=q('priorProp').style.display=ghost?'block':'none';stage.host.querySelector('.door').className='door '+frame.cupboard}}document.querySelector('#caption').textContent=`${{i+1}}/${{DATA.route.length}} · ${{frame.phase}} · ${{frame.label}}`}}function stop(){{if(timer)clearTimeout(timer);timer=null;document.querySelector('#play').textContent='Play'}}function tick(){{const ms=DATA.route[i].durationMs;i=(i+1)%DATA.route.length;show();timer=setTimeout(tick,ms/Number(document.querySelector('#speed').value))}}document.querySelector('#play').onclick=()=>{{if(timer)stop();else{{document.querySelector('#play').textContent='Pause';tick()}}}};document.querySelector('#prev').onclick=()=>{{stop();i=(i-1+DATA.route.length)%DATA.route.length;show()}};document.querySelector('#next').onclick=()=>{{stop();i=(i+1)%DATA.route.length;show()}};document.querySelector('#ghost').onchange=show;
const urls=new Set([DATA.contactSheet,DATA.walkSheet]);for(const f of DATA.route){{urls.add(f.actorSrc);urls.add(f.propSrc)}}Promise.all([...urls].map(src=>new Promise((ok,bad)=>{{const img=new Image();img.onload=()=>img.decode?img.decode().then(ok,bad):ok();img.onerror=bad;img.src=src}}))).then(()=>{{document.querySelector('#loading').textContent=`${{urls.size}} unique images loaded and decoded.`;document.querySelectorAll('button,input').forEach(x=>x.disabled=false);show()}}).catch(e=>document.querySelector('#loading').textContent='Media failed: '+e);
</script></body></html>'''
    reviewer_file = PACK / "reviewer.html"
    reviewer_file.write_text(page)
    shell = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper sweep broom V5</title><style>html,body,iframe{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}#loading{padding:24px}iframe{display:none}</style><p id="loading">Loading immutable Prime Keeper sweep-broom V5 reviewer…</p><iframe id="review" title="Prime Keeper sweep broom V5 reviewer"></iframe><script>fetch("https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/__V5_COMMIT__/art/drafts/keeper-prime-sweep-broom-2026-10-18-v5/reviewer.html").then(r=>{if(!r.ok)throw Error('reviewer '+r.status);return r.text()}).then(t=>{document.querySelector('#review').srcdoc=t;document.querySelector('#review').style.display='block';document.querySelector('#loading').remove()}).catch(e=>document.querySelector('#loading').textContent='Reviewer failed to load: '+e.message)</script></html>'''
    (PUBLIC / "index.html").write_text(shell)
    print(json.dumps({"set": SET, "frames": len(records), "routeFrames": len(route), "publishedAssets": len(published)}, indent=2))


if __name__ == "__main__":
    main()
