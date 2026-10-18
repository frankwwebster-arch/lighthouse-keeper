#!/usr/bin/env python3
"""Build the movement-first Prime keeper_sweep_broom V7 review candidate.

V7 deliberately does not redraw locomotion.  Every walking body starts with an
exact approved Walk V6 frame, and every turning body starts with an exact
approved Turn V9 frame.  Only a declared upper-body arm/hand corridor is
replaced.  The walk grip is the already-reviewed Sweep 3 grip requested by
Frank; broom art remains a separate provisional layer.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

import build_keeper_prime_sweep_broom_v6 as v6
import build_keeper_prime_walk_v5 as walk_v5


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-sweep-broom-v7"
PACK = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v7"
SOURCES = PACK / "sources"
FRAMES = PACK / "drafts/frames"
LAYERS = PACK / "drafts/layers"
MASKS = PACK / "drafts/masks"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"

WALK_DIR = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames"
TURN_DIR = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames"
STOP = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
V6_PACK = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v6"
SWEEP3 = V6_PACK / "drafts/frames/sweep3.png"
WALK_GRIP_SHEET = SOURCES / "sweep3-grip-walk-contact-sheet.png"
WALK_GRIP_CUTOUTS = [SOURCES / "walk-grip-cutouts" / f"grip-{i}.png" for i in range(1, 9)]
BROOM_AUTHORITY = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v4/sources/frank-drawn-cells/broom-detail-authority.png"

CELL = (384, 320)
ROOT_X = 150
FLOOR_Y = 311
WALK_MS = 125  # exact approved Walk V6 8 fps
TURN_MS = 1000 / 9  # exact approved Turn V9 one-second side-to-back duration

GAIT = [
    "left-foot contact", "left-foot down", "left-foot passing", "left-foot up",
    "right-foot contact", "right-foot down", "right-foot passing", "right-foot up",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def authority_canvas(path: Path, kind: str) -> tuple[Image.Image, tuple[int, int]]:
    """Translate authority bytes onto the 48 lp review cell; never resample."""
    source = Image.open(path).convert("RGBA")
    if kind == "walk":
        box = v6.alpha_bbox(source)
        root = v6.boot_root_x(source, box)
        offset = (round(ROOT_X - root), FLOOR_Y - (box[3] - 1))
    else:
        # Turn V9 is authored around axis x=128 and exact floor y=316.
        offset = (ROOT_X - 128, FLOOR_Y - 316)
    canvas = Image.new("RGBA", CELL, (0, 0, 0, 0))
    canvas.alpha_composite(source, offset)
    return canvas, offset


def walk_old_arm_mask(frame: int, authority_offset: tuple[int, int]) -> Image.Image:
    mask = Image.new("L", CELL, 0)
    source_frame = frame if frame in walk_v5.MASK_POLYGONS else (2 if frame == 1 else 6)
    ox, oy = authority_offset
    ImageDraw.Draw(mask).polygon([(x + ox, y + oy) for x, y in walk_v5.MASK_POLYGONS[source_frame]], fill=255)
    return mask


def arm_mask(kind: str, frame: int, authority_offset: tuple[int, int] = (0, 0)) -> Image.Image:
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    if kind == "walk":
        # Reuse the already-proven Walk V5 arm-ownership polygons, translated
        # with the exact authority frame.  Add only the compact Sweep-3 grip
        # corridor; the rear torso and all gait pixels remain authority-owned.
        old = walk_old_arm_mask(frame, authority_offset)
        mask = ImageChops.lighter(mask, old)
        draw = ImageDraw.Draw(mask)
        draw.polygon([(118, 128), (185, 121), (247, 139), (272, 181),
                      (260, 226), (212, 243), (148, 229), (116, 187)], fill=255)
        # The rear half must never own trouser or leg pixels; the lower front
        # allowance exists only for the Sweep-3 lower hand at the shaft.
        draw.rectangle((160, 246, CELL[0], CELL[1]), fill=0)
        return mask.filter(ImageFilter.GaussianBlur(0.55))
    else:
        # The source turn supplies only the changed carrying-arm corridor.
        # The approved V9 cap/head and planted lower body remain outside it.
        polygon = [
            (42, 145), (92, 124), (144, 126), (178, 158), (204, 151),
            (220, 123), (286, 126), (308, 157), (307, 225), (276, 250),
            (80, 250), (42, 222),
        ]
    draw.polygon(polygon, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.55))


def disjoint_actor_prop(actor: Image.Image, prop: Image.Image) -> tuple[Image.Image, Image.Image, Image.Image]:
    """Keep actor/prop independently reversible; render hands over the prop."""
    actor = actor.copy()
    prop = prop.copy()
    composite = Image.alpha_composite(prop, actor)
    return actor, prop, composite


def compose(base: Image.Image, source: Image.Image, kind: str, frame: int,
            prop_override: Image.Image | None = None,
            authority_offset: tuple[int, int] = (0, 0)) -> tuple[Image.Image, Image.Image, Image.Image, Image.Image]:
    if prop_override is None:
        source_actor, source_prop, _ = v6.split_prop(source)
    else:
        source_actor, source_prop = source, prop_override
    mask = arm_mask(kind, frame, authority_offset)
    actor = Image.composite(source_actor, base, mask)
    actor, prop, composite = disjoint_actor_prop(actor, source_prop)
    return actor, prop, composite, mask


def register_generated_grip(source: Image.Image, target: Image.Image) -> Image.Image:
    """Uniformly register by approved cap badge and floor; no creative warp."""
    import build_keeper_prime_walk_v4 as walk_register
    registered, _ = walk_register.register_to_frame(source, target)
    return registered


def bounds(image: Image.Image) -> dict[str, int]:
    box = image.getchannel("A").getbbox()
    if box is None:
        return {"minX": 0, "minY": 0, "maxX": -1, "maxY": -1, "width": 0, "height": 0, "opaquePixels": 0}
    l, t, r, b = box
    count = sum(1 for value in image.getchannel("A").getdata() if value)
    return {"minX": l, "minY": t, "maxX": r - 1, "maxY": b - 1,
            "width": r - l, "height": b - t, "opaquePixels": count}


def edge_alpha(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return (sum(bool(alpha.getpixel((x, y))) for x in range(CELL[0]) for y in (0, CELL[1] - 1))
            + sum(bool(alpha.getpixel((x, y))) for y in range(1, CELL[1] - 1) for x in (0, CELL[0] - 1)))


def gutter(image: Image.Image) -> int:
    box = image.getchannel("A").getbbox()
    if box is None:
        return min(CELL)
    l, t, r, b = box
    return min(l, t, CELL[0] - r, CELL[1] - b)


def audit_outside(base: Image.Image, actor: Image.Image, mask: Image.Image) -> dict[str, int]:
    before, after, owned = base.tobytes(), actor.tobytes(), mask.tobytes()
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
    return {"changedPixels": changed, "changedInsideArmCorridor": inside, "changedOutsideArmCorridor": outside}


def contact_pixels(actor: Image.Image, prop: Image.Image) -> int:
    dilated = prop.getchannel("A").filter(ImageFilter.MaxFilter(5))
    count = 0
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            r, g, b, a = actor.getpixel((x, y))
            if a and v6.is_skin((r, g, b)) and dilated.getpixel((x, y)):
                count += 1
    return count


def evidence_sheet(items: list[tuple[str, Image.Image]], columns: int) -> Image.Image:
    tile_w, tile_h = CELL[0], 348
    rows = (len(items) + columns - 1) // columns
    out = Image.new("RGBA", (tile_w * columns, tile_h * rows), (8, 22, 30, 255))
    draw = ImageDraw.Draw(out)
    font = ImageFont.load_default()
    for index, (label, image) in enumerate(items):
        x, y = (index % columns) * tile_w, (index // columns) * tile_h
        draw.text((x + 7, y + 6), label, fill=(235, 248, 251, 255), font=font)
        out.alpha_composite(image, (x, y + 26))
    return out


def main() -> None:
    walk_files = [WALK_DIR / f"keeper_prime_walk-right_f{i}.png" for i in range(1, 9)]
    turn_files = [TURN_DIR / f"keeper_prime_turn_side-right_to_back_f{i:02}.png" for i in range(1, 10)]
    turn_sources = [V6_PACK / f"drafts/frames/turn{i}.png" for i in range(1, 10)]
    required = [*walk_files, *turn_files, *turn_sources, *WALK_GRIP_CUTOUTS,
                STOP, SWEEP3, WALK_GRIP_SHEET, BROOM_AUTHORITY]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")

    # Preserve the immutable source/prompt evidence when rebuilding outputs.
    for directory in (FRAMES, LAYERS, MASKS, EVIDENCE, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (FRAMES, LAYERS, MASKS, EVIDENCE, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    records: dict[str, dict] = {}
    images: dict[str, Image.Image] = {}
    bases: dict[str, Image.Image] = {}

    sweep3_composite = Image.open(SWEEP3).convert("RGBA")
    generated_grips = [Image.open(path).convert("RGBA") for path in WALK_GRIP_CUTOUTS]
    _, sweep3_prop, _ = v6.split_prop(sweep3_composite)
    for index, authority in enumerate(walk_files, 1):
        name = f"sweep{index}"
        base, offset = authority_canvas(authority, "walk")
        grip_source = register_generated_grip(generated_grips[index - 1], base)
        mask = arm_mask("walk", index, offset)
        # The gait body is the approved Walk V6 frame byte-for-byte outside
        # the declared arm/hand corridor. The edited source contributes only
        # the requested Sweep-3 carrying pose.
        actor = Image.composite(grip_source, base, mask)
        actor, prop, composite = disjoint_actor_prop(actor, sweep3_prop)
        paths = {
            "actor": LAYERS / f"{name}-actor.png",
            "prop": LAYERS / f"{name}-prop.png",
            "composite": FRAMES / f"{name}.png",
            "mask": MASKS / f"{name}-arm-corridor.png",
            "base": EVIDENCE / f"{name}-approved-base.png",
        }
        actor.save(paths["actor"]); prop.save(paths["prop"]); composite.save(paths["composite"])
        mask.save(paths["mask"]); base.save(paths["base"])
        audit = audit_outside(base, actor, mask)
        records[name] = {
            "id": name, "kind": "approved-walk-with-sweep3-grip", "gaitFrame": index,
            "gaitPhase": GAIT[index - 1], "durationMs": WALK_MS,
            "authority": {"file": rel(authority), "sha256": sha(authority), "translationOnlyOffsetPx": list(offset)},
            "armSource": {"file": rel(WALK_GRIP_CUTOUTS[index - 1]), "sha256": sha(WALK_GRIP_CUTOUTS[index - 1]),
                          "requestedPose": "Sweep 3", "scope": "authority-edited gait cell"},
            "actor": {"file": rel(paths["actor"]), "sha256": sha(paths["actor"]), "bounds": bounds(actor)},
            "prop": {"file": rel(paths["prop"]), "sha256": sha(paths["prop"]), "bounds": bounds(prop), "status": "provisional-art-movement-review"},
            "composite": {"file": rel(paths["composite"]), "sha256": sha(paths["composite"]), "bounds": bounds(composite),
                          "edgeAlphaPixels": edge_alpha(composite), "transparentGutterPx": gutter(composite)},
            "armCorridor": {"file": rel(paths["mask"]), "sha256": sha(paths["mask"]), "audit": audit},
            "approvedBase": {"file": rel(paths["base"]), "sha256": sha(paths["base"])},
            "broomHandContactPixels": contact_pixels(actor, prop),
            "ownership": {"separateLayers": True, "renderOrder": ["prop", "actor"], "recompositionExact": True},
        }
        images[name], bases[name] = composite, base

    for index, (authority, source_path) in enumerate(zip(turn_files, turn_sources), 1):
        name = f"turn{index}"
        base, offset = authority_canvas(authority, "turn")
        source = Image.open(source_path).convert("RGBA")
        actor, prop, composite, mask = compose(base, source, "turn", index)
        paths = {
            "actor": LAYERS / f"{name}-actor.png", "prop": LAYERS / f"{name}-prop.png",
            "composite": FRAMES / f"{name}.png", "mask": MASKS / f"{name}-arm-corridor.png",
            "base": EVIDENCE / f"{name}-approved-base.png",
        }
        actor.save(paths["actor"]); prop.save(paths["prop"]); composite.save(paths["composite"])
        mask.save(paths["mask"]); base.save(paths["base"])
        audit = audit_outside(base, actor, mask)
        records[name] = {
            "id": name, "kind": "approved-turn-v9-with-carrying-arms", "turnFrame": index,
            "angleDegrees": [90, 98, 105, 120, 135, 150, 165, 172.5, 180][index - 1],
            "durationMs": round(TURN_MS, 6),
            "authority": {"file": rel(authority), "sha256": sha(authority), "translationOnlyOffsetPx": list(offset)},
            "armSource": {"file": rel(source_path), "sha256": sha(source_path), "role": "arm/hand corridor only"},
            "actor": {"file": rel(paths["actor"]), "sha256": sha(paths["actor"]), "bounds": bounds(actor)},
            "prop": {"file": rel(paths["prop"]), "sha256": sha(paths["prop"]), "bounds": bounds(prop), "status": "provisional-art-movement-review"},
            "composite": {"file": rel(paths["composite"]), "sha256": sha(paths["composite"]), "bounds": bounds(composite),
                          "edgeAlphaPixels": edge_alpha(composite), "transparentGutterPx": gutter(composite)},
            "armCorridor": {"file": rel(paths["mask"]), "sha256": sha(paths["mask"]), "audit": audit},
            "approvedBase": {"file": rel(paths["base"]), "sha256": sha(paths["base"])},
            "broomHandContactPixels": contact_pixels(actor, prop),
            "ownership": {"separateLayers": True, "renderOrder": ["prop", "actor"], "recompositionExact": True},
        }
        images[name], bases[name] = composite, base

    walk_sheet = EVIDENCE / "v7-walk-movement-contact-sheet.png"
    turn_sheet = EVIDENCE / "v7-turn-movement-contact-sheet.png"
    comparison_sheet = EVIDENCE / "v7-frame-by-frame-authority-comparison.png"
    evidence_sheet([(f"F{i} · {GAIT[i-1]}", images[f"sweep{i}"]) for i in range(1, 9)], 4).save(walk_sheet)
    evidence_sheet([(f"T{i} · {records[f'turn{i}']['angleDegrees']}°", images[f"turn{i}"]) for i in range(1, 10)], 3).save(turn_sheet)
    comparison = []
    for i in range(1, 9):
        comparison.extend([(f"approved Walk V6 F{i}", bases[f"sweep{i}"]), (f"V7 F{i} · arm corridor only", images[f"sweep{i}"])])
    evidence_sheet(comparison, 4).save(comparison_sheet)

    published: list[dict] = []
    by_hash: dict[str, str] = {}
    def publish(path: Path, label: str) -> str:
        ASSETS.mkdir(parents=True, exist_ok=True)
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
        record["urls"] = {part: publish(ROOT / record[part]["file"], f"{record['id']}-{part}") for part in ("actor", "prop", "composite")}
        record["authorityUrl"] = publish(ROOT / record["approvedBase"]["file"], f"{record['id']}-approved-base")
    walk_sheet_url = publish(walk_sheet, "walk-movement-contact-sheet")
    turn_sheet_url = publish(turn_sheet, "turn-movement-contact-sheet")
    comparison_url = publish(comparison_sheet, "frame-by-frame-authority-comparison")
    walk_authority_urls = [publish(path, f"approved-walk-v6-f{i}") for i, path in enumerate(walk_files, 1)]
    neutral_url = publish(STOP, "exact-side-right-neutral")
    blank = LAYERS / "blank-prop.png"; Image.new("RGBA", CELL, (0, 0, 0, 0)).save(blank)
    blank_url = publish(blank, "blank-prop")

    route: list[dict] = []
    def standard_walk(direction: str, start: float, delta: float, cycles: int, phase: str) -> None:
        for step in range(cycles * 8):
            gait = step % 8
            route.append({
                "actorSrc": walk_authority_urls[gait], "propSrc": blank_url, "authoritySrc": walk_authority_urls[gait],
                "recordId": None, "gaitFrame": gait + 1, "phase": phase,
                "label": f"approved Walk V6 F{gait+1} · {GAIT[gait]}",
                "actorRootXLp": round(start + step * delta, 3), "propRootXLp": 0,
                "cellWidthLp": 32, "anchorXLp": 16, "bottomLp": 52,
                "mirror": direction == "left", "cupboard": "open", "durationMs": WALK_MS,
            })

    def exact_neutral(phase: str) -> None:
        route.append({
            "actorSrc": neutral_url, "propSrc": blank_url, "authoritySrc": neutral_url,
            "recordId": None, "gaitFrame": None, "turnFrame": None,
            "phase": phase, "label": "exact approved side-right neutral",
            "actorRootXLp": 154, "propRootXLp": 0,
            "cellWidthLp": 32, "anchorXLp": 16, "bottomLp": 52,
            "mirror": False, "cupboard": "closed", "durationMs": 250,
        })

    def action(name: str, phase: str, root: float, mirror: bool, duration: float | None = None, cupboard: str = "open") -> None:
        record = records[name]
        route.append({
            "actorSrc": record["urls"]["actor"], "propSrc": record["urls"]["prop"],
            "authoritySrc": record["authorityUrl"], "recordId": name,
            "gaitFrame": record.get("gaitFrame"), "turnFrame": record.get("turnFrame"),
            "phase": phase, "label": (f"{name} · {record.get('gaitPhase', str(record.get('angleDegrees')) + '°')}"),
            "actorRootXLp": root, "propRootXLp": root, "cellWidthLp": 48, "anchorXLp": ROOT_X / 8,
            "bottomLp": 52, "mirror": mirror, "cupboard": cupboard,
            "durationMs": duration if duration is not None else record["durationMs"],
        })

    # Both travel directions advance F1→F8 in time.  Direction changes only
    # root motion and horizontal mirroring; it never reverses the gait.
    standard_walk("right", 22, 7.4, 2, "approved standard walk into cupboard")
    exact_neutral("phase-correct stop at exact side-right neutral")
    action("sweep1", "fully obscured standard-to-sweep swap", 154, True, 375, "closed")
    for step in range(16):
        action(f"sweep{step % 8 + 1}", "approved walking gait while sweeping left", round(151 - step * 6.4, 3), True)
    turn_order = list(range(1, 10)) + list(range(8, 0, -1))
    for position, index in enumerate(turn_order):
        action(f"turn{index}", "exact approved V9 reversal while carrying broom", 54, position < 9)
    for step in range(16):
        action(f"sweep{step % 8 + 1}", "approved walking gait while sweeping right", round(55 + step * 6.4, 3), False)
    action("sweep1", "fully obscured sweep-to-standard swap", 154, True, 375, "closed")
    exact_neutral("exact side-right neutral after action exit")
    standard_walk("left", 151, -7.4, 2, "approved standard walk away from cupboard")

    data = {
        "schema": "lighthouse-keeper/prime-action-review@3", "set": SET,
        "status": "versioned-reversible-movement-candidate-not-approved",
        "room": {"widthLp": 192, "heightLp": 56, "floorLp": 52},
        "frames": records, "route": route,
        "walkSheet": walk_sheet_url, "turnSheet": turn_sheet_url, "comparisonSheet": comparison_url,
        "reviewInstruction": "Assess locomotion and turn only. Broom rendering is explicitly provisional and separately owned.",
    }
    data_file = PACK / f"{SET}.json"; dump(data_file, data)

    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET,
        "status": "prime-sweep-broom-v7-movement-awaiting-frank",
        "supersedes": {"set": "keeper-prime-sweep-broom-v6", "status": "rejected-provenance",
                       "reason": "V6 redrew locomotion, time-reversed the mirrored walk-away phase and therefore produced a jerky, physically impossible gait."},
        "userDirection": "Use exact standard walk and standard turn. The sole body change is arm position; use hands as in Sweep 3. Correct movement before correcting broom rendering.",
        "authorities": {
            "approvedWalkV6": [{"frame": i, "file": rel(path), "sha256": sha(path), "durationMs": WALK_MS} for i, path in enumerate(walk_files, 1)],
            "approvedTurnV9": [{"frame": i, "file": rel(path), "sha256": sha(path), "durationMs": round(TURN_MS, 6)} for i, path in enumerate(turn_files, 1)],
            "exactSideRightNeutral": {"file": rel(STOP), "sha256": sha(STOP)},
        },
        "armSource": {"file": rel(WALK_GRIP_SHEET), "sha256": sha(WALK_GRIP_SHEET),
                      "cutouts": [{"file": rel(path), "sha256": sha(path)} for path in WALK_GRIP_CUTOUTS],
                      "scope": "eight authority-edited walk cells using the requested Sweep 3 grip"},
        "broom": {
            "status": "provisional-separate-layer-not-for-art-approval",
            "authority": {"file": rel(BROOM_AUTHORITY), "sha256": sha(BROOM_AUTHORITY)},
            "knownIssue": "Current prop rendering varies through the turn; movement is the only V7 approval gate.",
            "replicationRule": "Future broom/hoover/lawnmower art must remain a separate layer and preserve the approved gait, turn, grip coordinates and root registration.",
        },
        "candidate": {"frames": list(records.values()), "route": {"file": rel(data_file), "sha256": sha(data_file), "frames": len(route)},
                      "walkContactSheet": {"file": rel(walk_sheet), "sha256": sha(walk_sheet)},
                      "turnContactSheet": {"file": rel(turn_sheet), "sha256": sha(turn_sheet)},
                      "frameComparison": {"file": rel(comparison_sheet), "sha256": sha(comparison_sheet)},
                      "reviewUrl": f"/keeper-review/{SET}/"},
        "movementContract": {
            "walkFrameOrderBothDirections": [1, 2, 3, 4, 5, 6, 7, 8],
            "walkDirectionImplementedByMirrorAndRootOnly": True,
            "turnFrameOrder": turn_order,
            "walkDurationMs": WALK_MS, "sideToBackDurationMs": 1000,
            "walkCellsDerivedFrameForFrameFromExactAuthority": True,
            "walkCellsByteIdenticalOutsideArmCorridor": True,
            "turnCellsExactAuthorityOutsideArmCorridor": True,
            "walkFootLeadAndPhaseOrderLocked": True,
        },
        "publishedAssets": published,
        "approvalBoundary": {"movementApproved": False, "broomArtApproved": False, "candidateApproved": False,
                             "productionPromotionAllowed": False, "productionChanged": False, "runtimeChanged": False},
        "rollback": f"Delete only {rel(PACK)}, public/keeper-review/{SET}, scripts/build_keeper_prime_sweep_broom_v7.py and scripts/verify_keeper_prime_sweep_broom_v7.mjs.",
    }
    dump(PACK / "batch-register.json", register)
    (PACK / "HANDOFF.md").write_text(
        "# Prime Keeper sweep broom V7 · movement proof\n\n"
        "V6 is rejected because it redrew locomotion and reversed the mirrored walk-away gait in time. "
        "V7 maps every walking frame one-to-one to exact approved Walk V6 and starts every turning frame from exact approved Turn V9. "
        "Both travel directions advance F1→F8; only spatial mirroring and root direction change. The walk arm/hand grip is derived from Sweep 3. "
        "The broom is separately owned and explicitly provisional: judge movement first. Nothing is approved or promoted.\n"
    )
    (PACK / "PROMPT_LOG.md").write_text(
        "# Prime Keeper sweep broom V7 prompt log\n\n"
        "Mode: built-in image editing (`image_gen`). Two exploratory contact-sheet edits were generated from exact Walk V6 / Turn V9 plus the broom authority. "
        "Their generated broom pixels were rejected because the broom changed shape and tone. Apple Vision foreground extraction isolated the eight selected grip studies. "
        "Each study is registered to its corresponding Walk V6 frame and contributes pixels only inside the declared arm/hand corridor; all other visible Keeper pixels come from the exact approved Walk V6 authority. "
        "The generated broom is discarded. Turn V9 remains the exact base outside its carrying-arm corridor.\n\n"
        "## Selected walk-edit prompt\n\n"
        "Use case: precise-object-edit. Asset type: an eight-frame transparent animation contact sheet. "
        "In each of the eight supplied approved Walk V6 cells, replace only the two arms and hands with the same natural bent-forward two-hand grip shown in the supplied Sweep 3 reference. "
        "Preserve the exact approved Keeper body, face, beard, cap, jumper, trousers, boots, silhouette, scale, floor contact, left-foot/right-foot gait phase, frame order and spacing. "
        "Do not add a broom to the selected output. Do not change the legs or feet. Keep one isolated character in each cell on a clean transparent background with generous gutters.\n\n"
        "## Runtime assembly rule\n\n"
        "Both travel directions play F1→F8 at 125 ms per frame. Direction changes by mirroring and root motion only; the frame sequence is never time-reversed. "
        "The provisional broom is a separately owned layer rendered behind the hands.\n"
    )

    reviewer = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime sweep broom V7 · movement proof</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#07131b;color:#edf8fb;font:14px/1.45 system-ui,sans-serif}}header,main{{max-width:1540px;margin:auto;padding:18px}}.status{{display:inline-block;border:1px solid #e6bd5c;color:#ffe4a0;border-radius:999px;padding:4px 9px;margin-right:6px}}.warning{{border-left:4px solid #e6bd5c;background:#292516;padding:10px 13px}}.panel{{background:#10232d;border:1px solid #294a57;border-radius:12px;padding:14px;margin:14px 0}}button,input{{font:inherit}}button{{background:#173d52;color:white;border:1px solid #537788;border-radius:7px;padding:7px 10px}}button:disabled,input:disabled{{opacity:.45}}.controls{{display:flex;gap:7px;flex-wrap:wrap;align-items:center}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.stagewrap{{overflow:auto;background:#061018;padding:8px}}.stage{{position:relative;overflow:hidden;background:linear-gradient(#1a2d36 0 92.8%,#4d555b 92.8%)}}.stage img{{position:absolute;object-fit:fill}}.stage img[data-layer=prop]{{z-index:3}}.stage img[data-layer=actor]{{z-index:4}}.stage img[data-layer=priorProp]{{z-index:1}}.stage img[data-layer=priorActor]{{z-index:2}}.ghost{{opacity:.27;filter:hue-rotate(110deg) saturate(1.7)}}.doorframe{{position:absolute;z-index:12;bottom:0;right:0;width:15px;height:56px;background:#1b0f08;border-left:2px solid #b58752}}.doorleaf{{position:absolute;z-index:11;bottom:0;right:0;width:18px;height:56px;border:2px solid #2b190c;background:repeating-linear-gradient(90deg,#513719 0 8px,#855d31 8px 11px);transition:none}}.doorleaf.closed{{width:96px}}.sheet{{max-width:100%;background:#061018}}.compare{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.compare img{{max-width:100%;height:auto;background:repeating-conic-gradient(#243640 0 25%,#162630 0 50%) 0/16px 16px}}@media(max-width:900px){{.grid,.compare{{grid-template-columns:1fr}}}}</style></head><body><header><h1>Prime Keeper · keeper_sweep_broom V7</h1><span class="status">Movement proof</span><span class="status">V6 rejected</span><span class="status">Nothing promoted</span><p class="warning"><strong>Judge movement first.</strong> The Keeper now uses the exact approved Walk V6 gait and exact approved Turn V9. The broom remains a separate provisional layer; its varying rendering is acknowledged and is not this gate.</p></header><main><section class="panel"><div id="loading">Loading and decoding every unique frame… controls remain locked.</div><div class="controls"><button id="play" disabled>Play</button><button id="prev" disabled>Previous</button><button id="next" disabled>Next</button><label>Speed <input id="speed" disabled type="range" min="0.5" max="1.5" value="1" step="0.1"></label><label><input id="ghost" disabled type="checkbox"> Previous-frame ghost</label></div><p><strong>Binding cadence:</strong> both left and right travel run F1→F8 at exact approved 8 fps. The 17-frame reversal is exact V9 forward then reverse at its one-second side→back timing.</p><p id="caption"></p></section><section class="panel"><div class="grid"><div><h2>Large inspection · 6 px/lp</h2><div class="stagewrap"><div class="stage" id="large"></div></div></div><div><h2>Gameplay scale · 4 px/lp</h2><div class="stagewrap"><div class="stage" id="game"></div></div></div><div><h2>Literal 1× · 1 px/lp</h2><div class="stagewrap"><div class="stage" id="literal"></div></div></div><div><h2>Frame authority comparison</h2><div class="compare"><div><strong>Exact authority</strong><img id="authority"></div><div><strong>V7 arm corridor + separate prop</strong><img id="candidate"></div></div></div></div></section><section class="panel"><h2>Exact eight-frame left/right gait · Sweep 3 grip</h2><img class="sheet" src="{walk_sheet_url}"><h2>Exact nine-frame V9 turn body</h2><img class="sheet" src="{turn_sheet_url}"><h2>Frame-by-frame Prime comparison</h2><img class="sheet" src="{comparison_url}"></section></main><script>
const DATA={json.dumps(data,separators=(',',':'))};let i=0,timer=null;const stages=[];function make(id,scale){{const host=document.querySelector('#'+id);host.style.width=192*scale+'px';host.style.height=56*scale+'px';for(const name of ['priorActor','priorProp','actor','prop']){{const img=document.createElement('img');img.dataset.layer=name;if(name.startsWith('prior'))img.className='ghost';host.append(img)}}const leaf=document.createElement('div');leaf.className='doorleaf';host.append(leaf);const frame=document.createElement('div');frame.className='doorframe';host.append(frame);const value={{host,scale}};stages.push(value);return value}}make('large',6);make('game',4);make('literal',1);
function place(stage,img,src,frame,prop=false){{img.src=src;img.style.width=frame.cellWidthLp*stage.scale+'px';img.style.height=40*stage.scale+'px';img.style.left=(frame[(prop?'propRootXLp':'actorRootXLp')]-frame.anchorXLp)*stage.scale+'px';img.style.top=(frame.bottomLp-40)*stage.scale+'px';img.style.transform=frame.mirror?'scaleX(-1)':'none'}}function show(){{const frame=DATA.route[i],prior=DATA.route[(i-1+DATA.route.length)%DATA.route.length],ghost=document.querySelector('#ghost').checked;for(const stage of stages){{const q=n=>stage.host.querySelector('[data-layer='+n+']');place(stage,q('actor'),frame.actorSrc,frame);place(stage,q('prop'),frame.propSrc,frame,true);place(stage,q('priorActor'),prior.actorSrc,prior);place(stage,q('priorProp'),prior.propSrc,prior,true);q('priorActor').style.display=q('priorProp').style.display=ghost?'block':'none';stage.host.querySelector('.doorleaf').className='doorleaf '+frame.cupboard}}document.querySelector('#authority').src=frame.authoritySrc;document.querySelector('#candidate').src=frame.recordId?DATA.frames[frame.recordId].urls.composite:frame.actorSrc;document.querySelector('#caption').textContent=`${{i+1}}/${{DATA.route.length}} · ${{frame.phase}} · ${{frame.label}}`;}}
function stop(){{if(timer)clearTimeout(timer);timer=null;document.querySelector('#play').textContent='Play'}}function tick(){{const ms=DATA.route[i].durationMs;i=(i+1)%DATA.route.length;show();timer=setTimeout(tick,ms/Number(document.querySelector('#speed').value))}}document.querySelector('#play').onclick=()=>{{if(timer)stop();else{{document.querySelector('#play').textContent='Pause';tick()}}}};document.querySelector('#prev').onclick=()=>{{stop();i=(i-1+DATA.route.length)%DATA.route.length;show()}};document.querySelector('#next').onclick=()=>{{stop();i=(i+1)%DATA.route.length;show()}};document.querySelector('#ghost').onchange=show;
const urls=new Set([DATA.walkSheet,DATA.turnSheet,DATA.comparisonSheet]);for(const f of DATA.route){{urls.add(f.actorSrc);urls.add(f.propSrc);urls.add(f.authoritySrc)}}for(const r of Object.values(DATA.frames))urls.add(r.urls.composite);Promise.all([...urls].map(src=>new Promise((ok,bad)=>{{const img=new Image();img.onload=()=>img.decode?img.decode().then(ok,bad):ok();img.onerror=bad;img.src=src}}))).then(()=>{{document.querySelector('#loading').textContent=`${{urls.size}} unique images loaded and decoded. Controls enabled.`;document.querySelectorAll('button,input').forEach(x=>x.disabled=false);show();}}).catch(e=>document.querySelector('#loading').textContent='Media failed: '+e);
</script></body></html>'''
    reviewer_file = PACK / "reviewer.html"; reviewer_file.write_text(reviewer)
    shell = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper sweep broom V7</title><style>html,body,iframe{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}#loading{padding:24px}iframe{display:none}</style><p id="loading">Loading immutable Prime Keeper sweep-broom V7 movement reviewer…</p><iframe id="review" title="Prime Keeper sweep broom V7 movement reviewer"></iframe><script>fetch("https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/__V7_COMMIT__/art/drafts/keeper-prime-sweep-broom-2026-10-18-v7/reviewer.html").then(r=>{if(!r.ok)throw Error('reviewer '+r.status);return r.text()}).then(t=>{document.querySelector('#review').srcdoc=t;document.querySelector('#review').style.display='block';document.querySelector('#loading').remove()}).catch(e=>document.querySelector('#loading').textContent='Reviewer failed to load: '+e.message)</script></html>'''
    (PUBLIC / "index.html").write_text(shell)
    print(json.dumps({"set": SET, "candidateFrames": len(records), "routeFrames": len(route), "publishedAssets": len(published)}, indent=2))


if __name__ == "__main__":
    main()
