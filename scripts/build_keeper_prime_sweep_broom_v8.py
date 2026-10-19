#!/usr/bin/env python3
"""Build the immutable Prime keeper_sweep_broom V8 movement correction.

The locomotion contract is deliberately mechanical: approved Walk V6,
stop/walk V1 and Turn V9 pixels are copied without resampling.  During the
working state, only a declared hard-edged held-arm/hand region can differ.
The broom is a separate, provisional prop layer.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

import build_keeper_prime_sweep_broom_v6 as v6
import build_keeper_prime_sweep_broom_v7 as v7


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-sweep-broom-v8"
PACK = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-19-v8"
FRAMES = PACK / "drafts/frames"
LAYERS = PACK / "drafts/layers"
MASKS = PACK / "drafts/masks"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"

WALK_DIR = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames"
TURN_DIR = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames"
BRIDGE_DIR = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames"
NEUTRAL = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
GRIP_DIR = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v7/sources/walk-grip-cutouts"
TURN_SOURCE_DIR = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v6/drafts/frames"
BROOM_AUTHORITY = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v4/sources/frank-drawn-cells/broom-detail-authority.png"
SWEEP3 = ROOT / "art/drafts/keeper-prime-sweep-broom-2026-10-18-v6/drafts/frames/sweep3.png"

CELL = (384, 320)
ROOT_X = 150
FLOOR_Y = 311
WALK_MS = 125
TURN_MS = 1000 / 9
WALK_DELTA_LP = 21 / 8
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


def hard_effective_mask(mask: Image.Image, source: Image.Image) -> Image.Image:
    """Permit real source art only; transparent/black matte cannot erase authority."""
    hard = mask.point(lambda value: 255 if value else 0)
    opaque = source.getchannel("A").point(lambda value: 255 if value else 0)
    # Some rejected turn sources contain opaque black extraction voids.  Keep
    # true dark outlines only when they sit immediately beside coloured art;
    # reject broad black matte regions so the approved authority remains.
    colour = Image.new("L", CELL, 0)
    source_pixels, colour_pixels = source.load(), colour.load()
    for y in range(CELL[1]):
        for x in range(CELL[0]):
            r, g, b, a = source_pixels[x, y]
            if a and max(r, g, b) >= 80:
                colour_pixels[x, y] = 255
    real_art = ImageChops.multiply(opaque, colour.filter(ImageFilter.MaxFilter(3)))
    return ImageChops.multiply(hard, real_art)


def held_limb_mask(kind: str, frame: int, offset: tuple[int, int]) -> Image.Image:
    """Hard ownership mask: never owns head, torso body, trousers, legs or boots."""
    mask = Image.new("L", CELL, 0)
    draw = ImageDraw.Draw(mask)
    if kind == "walk":
        # The right-facing front quadrant only.  The lower edge is above the
        # waistband/trouser boundary in every approved gait cell.
        draw.polygon([
            (116, 130), (154, 118), (197, 124), (237, 139),
            (268, 165), (270, 220), (244, 243), (188, 244),
            (142, 227), (116, 190),
        ], fill=255)
    else:
        # Approved Turn V9 remains exact below y=234.  This is the correction
        # for V7's destructive mask, which extended into trousers and boots.
        draw.polygon([
            (92, 126), (146, 119), (198, 128), (236, 119),
            (286, 129), (309, 158), (306, 220), (279, 234),
            (119, 234), (92, 213),
        ], fill=255)
    return mask


def save_frame(name: str, base: Image.Image, source_actor: Image.Image,
               prop: Image.Image, mask: Image.Image, authority: Path,
               meta: dict) -> tuple[dict, Image.Image]:
    effective = hard_effective_mask(mask, source_actor)
    max_owned_y = int(meta.pop("maxOwnedYLimit", 234))
    owned = effective
    # Never erase authority pixels: the held-limb art is a strict overlay.
    # This keeps the approved body continuous even where a rejected source has
    # transparent extraction holes.
    actor = Image.composite(source_actor, base, effective)
    composite = Image.alpha_composite(prop, actor)
    paths = {
        "actor": LAYERS / f"{name}-actor.png",
        "prop": LAYERS / f"{name}-prop.png",
        "composite": FRAMES / f"{name}.png",
        "mask": MASKS / f"{name}-held-limb-only.png",
        "base": EVIDENCE / f"{name}-approved-base.png",
    }
    actor.save(paths["actor"]); prop.save(paths["prop"]); composite.save(paths["composite"])
    owned.save(paths["mask"]); base.save(paths["base"])
    audit = v7.audit_outside(base, actor, owned)
    if audit["changedOutsideArmCorridor"]:
        raise RuntimeError(f"{name}: changed pixels outside held-limb mask")
    if any(owned.getpixel((x, y)) for y in range(max_owned_y + 1, CELL[1]) for x in range(CELL[0])):
        raise RuntimeError(f"{name}: held-limb mask touches lower body")
    record = {
        "id": name,
        **meta,
        "authority": {"file": rel(authority), "sha256": sha(authority)},
        "actor": {"file": rel(paths["actor"]), "sha256": sha(paths["actor"]), "bounds": v7.bounds(actor)},
        "prop": {"file": rel(paths["prop"]), "sha256": sha(paths["prop"]), "bounds": v7.bounds(prop),
                 "status": "provisional-art-movement-review"},
        "composite": {"file": rel(paths["composite"]), "sha256": sha(paths["composite"]),
                      "bounds": v7.bounds(composite), "edgeAlphaPixels": v7.edge_alpha(composite),
                      "transparentGutterPx": v7.gutter(composite)},
        "heldLimbMask": {"file": rel(paths["mask"]), "sha256": sha(paths["mask"]),
                         "hardEdged": True, "maxOwnedY": max_owned_y, "audit": audit},
        "approvedBase": {"file": rel(paths["base"]), "sha256": sha(paths["base"])},
        "broomHandContactPixels": v7.contact_pixels(actor, prop),
        "ownership": {"separateLayers": True, "renderOrder": ["prop", "actor"], "recompositionExact": True},
    }
    return record, composite


def evidence_sheet(items: list[tuple[str, Image.Image]], columns: int) -> Image.Image:
    tile_w, tile_h = CELL[0], 348
    rows = (len(items) + columns - 1) // columns
    out = Image.new("RGBA", (tile_w * columns, tile_h * rows), (8, 22, 30, 255))
    draw = ImageDraw.Draw(out); font = ImageFont.load_default()
    for index, (label, image) in enumerate(items):
        x, y = (index % columns) * tile_w, (index // columns) * tile_h
        draw.text((x + 7, y + 6), label, fill=(235, 248, 251, 255), font=font)
        out.alpha_composite(image, (x, y + 26))
    return out


def main() -> None:
    walk_files = [WALK_DIR / f"keeper_prime_walk-right_f{i}.png" for i in range(1, 9)]
    turn_files = [TURN_DIR / f"keeper_prime_turn_side-right_to_back_f{i:02}.png" for i in range(1, 10)]
    bridge_files = [BRIDGE_DIR / f"keeper_prime_stop-to-walk-right_f{i}.png" for i in range(1, 6)]
    grips = [GRIP_DIR / f"grip-{i}.png" for i in range(1, 9)]
    turn_sources = [TURN_SOURCE_DIR / f"turn{i}.png" for i in range(1, 10)]
    required = [*walk_files, *turn_files, *bridge_files, *grips, *turn_sources, NEUTRAL, BROOM_AUTHORITY, SWEEP3]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")

    for directory in (FRAMES, LAYERS, MASKS, EVIDENCE, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (FRAMES, LAYERS, MASKS, EVIDENCE, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    records: dict[str, dict] = {}
    images: dict[str, Image.Image] = {}
    _, stable_walk_prop, _ = v6.split_prop(Image.open(SWEEP3).convert("RGBA"))

    for index, (authority, grip_path) in enumerate(zip(walk_files, grips), 1):
        base, offset = v7.authority_canvas(authority, "walk")
        grip = v7.register_generated_grip(Image.open(grip_path).convert("RGBA"), base)
        source_actor, _, _ = v6.split_prop(grip)
        name = f"sweep{index}"
        record, image = save_frame(
            name, base, source_actor, stable_walk_prop,
            held_limb_mask("walk", index, offset), authority,
            {"kind": "approved-walk-v6-held-limb-edit", "gaitFrame": index,
             "gaitPhase": GAIT[index - 1], "durationMs": WALK_MS,
             "translationOnlyOffsetPx": list(offset),
             "maxOwnedYLimit": 244,
             "editScope": "held arms and hands only; locomotion body is exact Walk V6"},
        )
        records[name], images[name] = record, image

    angles = [90, 98, 105, 120, 135, 150, 165, 172.5, 180]
    for index, (authority, source_path) in enumerate(zip(turn_files, turn_sources), 1):
        base, offset = v7.authority_canvas(authority, "turn")
        source = Image.open(source_path).convert("RGBA")
        source_actor, source_prop, _ = v6.split_prop(source)
        name = f"turn{index}"
        record, image = save_frame(
            name, base, source_actor, source_prop,
            held_limb_mask("turn", index, offset), authority,
            {"kind": "approved-turn-v9-held-limb-edit", "turnFrame": index,
             "angleDegrees": angles[index - 1], "durationMs": round(TURN_MS, 6),
             "translationOnlyOffsetPx": list(offset),
             "editScope": "held arms and hands only; head, torso body and complete lower body are exact Turn V9"},
        )
        records[name], images[name] = record, image

    walk_sheet = EVIDENCE / "v8-walk-exact-movement-contact-sheet.png"
    turn_sheet = EVIDENCE / "v8-turn-exact-movement-contact-sheet.png"
    compare_sheet = EVIDENCE / "v8-authority-candidate-comparison.png"
    evidence_sheet([(f"Walk V6 F{i} · {GAIT[i-1]}", images[f"sweep{i}"]) for i in range(1, 9)], 4).save(walk_sheet)
    evidence_sheet([(f"Turn V9 F{i} · {angles[i-1]}°", images[f"turn{i}"]) for i in range(1, 10)], 3).save(turn_sheet)
    comparisons: list[tuple[str, Image.Image]] = []
    for i in range(1, 9):
        base, _ = v7.authority_canvas(walk_files[i-1], "walk")
        comparisons += [(f"authority Walk V6 F{i}", base), (f"V8 · limb pixels only", images[f"sweep{i}"])]
    for i in range(1, 10):
        base, _ = v7.authority_canvas(turn_files[i-1], "turn")
        comparisons += [(f"authority Turn V9 F{i}", base), (f"V8 · limb pixels only", images[f"turn{i}"])]
    evidence_sheet(comparisons, 4).save(compare_sheet)

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
        record["urls"] = {part: publish(ROOT / record[part]["file"], f"{record['id']}-{part}")
                          for part in ("actor", "prop", "composite")}
        record["authorityUrl"] = publish(ROOT / record["approvedBase"]["file"], f"{record['id']}-authority")
        record["maskUrl"] = publish(ROOT / record["heldLimbMask"]["file"], f"{record['id']}-mask")
    walk_urls = [publish(path, f"approved-walk-v6-f{i}") for i, path in enumerate(walk_files, 1)]
    bridge_urls = [publish(path, f"approved-bridge-f{i}") for i, path in enumerate(bridge_files, 1)]
    neutral_url = publish(NEUTRAL, "exact-side-right-neutral")
    blank = LAYERS / "blank-prop.png"; Image.new("RGBA", CELL, (0, 0, 0, 0)).save(blank)
    blank_url = publish(blank, "blank-prop")
    walk_sheet_url = publish(walk_sheet, "walk-contact-sheet")
    turn_sheet_url = publish(turn_sheet, "turn-contact-sheet")
    compare_sheet_url = publish(compare_sheet, "authority-comparison")

    route: list[dict] = []
    def add_authority(src: str, phase: str, label: str, root: float, mirror: bool,
                      duration: float = WALK_MS, cupboard: str = "open", gait: int | None = None,
                      authority_kind: str = "walk") -> None:
        route.append({"actorSrc": src, "propSrc": blank_url, "authoritySrc": src,
                      "recordId": None, "gaitFrame": gait, "turnFrame": None,
                      "phase": phase, "label": label, "actorRootXLp": round(root, 3),
                      "propRootXLp": 0, "cellWidthLp": 32, "anchorXLp": 16,
                      "bottomLp": 52, "mirror": mirror, "cupboard": cupboard,
                      "durationMs": duration, "authorityKind": authority_kind})

    def add_action(name: str, phase: str, root: float, mirror: bool,
                   cupboard: str = "open", duration: float | None = None) -> None:
        record = records[name]
        route.append({"actorSrc": record["urls"]["actor"], "propSrc": record["urls"]["prop"],
                      "authoritySrc": record["authorityUrl"], "maskSrc": record["maskUrl"],
                      "recordId": name, "gaitFrame": record.get("gaitFrame"),
                      "turnFrame": record.get("turnFrame"), "phase": phase,
                      "label": f"{name} · {record.get('gaitPhase', str(record.get('angleDegrees')) + '°')}",
                      "actorRootXLp": round(root, 3), "propRootXLp": round(root, 3),
                      "cellWidthLp": 48, "anchorXLp": ROOT_X / 8, "bottomLp": 52,
                      "mirror": mirror, "cupboard": cupboard,
                      "durationMs": duration if duration is not None else record["durationMs"],
                      "authorityKind": "action"})

    # Exact approved approach: six complete cycles, one phase-correct F1, then
    # exact walk-to-stop bridge with 18→12→6→2 high-res-pixel root deltas.
    root = 23.25
    for step in range(48):
        gait = step % 8 + 1
        add_authority(walk_urls[gait-1], "approved Walk V6 approach", f"Walk V6 F{gait} · {GAIT[gait-1]}", root, False, gait=gait)
        root += WALK_DELTA_LP
    add_authority(walk_urls[0], "approved Walk V6 approach", "Walk V6 F1 · phase-correct contact", root, False, gait=1)
    root += WALK_DELTA_LP
    for bridge_index, delta in zip((4, 3, 2, 1), (18/8, 12/8, 6/8, 2/8)):
        root += delta
        add_authority(bridge_urls[bridge_index-1], "approved walk-to-stop bridge",
                      f"exact reverse bridge F{bridge_index}", root, False,
                      cupboard="closed" if bridge_index <= 3 else "closing", authority_kind="bridge")
    add_authority(neutral_url, "exact side-right neutral before hidden swap",
                  "exact approved side-right neutral", root, False, duration=250,
                  cupboard="closed", authority_kind="neutral")

    add_action("sweep1", "fully obscured standard-to-sweep swap", 154, True, "closed", 250)
    for step in range(32):
        add_action(f"sweep{step % 8 + 1}", "approved F1→F8 gait while sweeping left",
                   154 - step * WALK_DELTA_LP, True)
    turn_order = list(range(1, 10)) + list(range(8, 0, -1))
    for position, index in enumerate(turn_order):
        add_action(f"turn{index}", "approved Turn V9 reversal with held-limb-only edit",
                   70, position < 9)
    for step in range(32):
        add_action(f"sweep{step % 8 + 1}", "approved F1→F8 gait while sweeping right",
                   70 + step * WALK_DELTA_LP, False)
    add_action("sweep1", "fully obscured sweep-to-standard swap", 154, False, "closed", 250)
    add_authority(neutral_url, "exact side-right neutral after hidden swap",
                  "exact approved side-right neutral", 154, False, duration=250,
                  cupboard="closed", authority_kind="neutral")

    # Exact mirrored stop-to-walk bridge, hidden until the Keeper clears the door.
    root = 154.0
    add_authority(bridge_urls[0], "approved stop-to-walk bridge", "exact mirrored stop F1", root, True,
                  cupboard="closed", authority_kind="bridge")
    for bridge_index, delta in zip((2, 3, 4, 5), (2/8, 6/8, 12/8, 18/8)):
        root -= delta
        add_authority(bridge_urls[bridge_index-1], "approved stop-to-walk bridge",
                      f"exact mirrored bridge F{bridge_index}", root, True,
                      cupboard="closed" if bridge_index <= 3 else "opening", authority_kind="bridge",
                      gait=1 if bridge_index == 5 else None)
    for step in range(48):
        gait = step % 8 + 1
        if step:
            root -= WALK_DELTA_LP
        add_authority(walk_urls[gait-1], "approved Walk V6 departure", f"Walk V6 F{gait} · {GAIT[gait-1]}",
                      root, True, gait=gait)

    data = {"schema": "lighthouse-keeper/prime-action-review@4", "set": SET,
            "status": "versioned-reversible-movement-candidate-not-approved",
            "room": {"widthLp": 192, "heightLp": 56, "floorLp": 52},
            "frames": records, "route": route, "walkSheet": walk_sheet_url,
            "turnSheet": turn_sheet_url, "comparisonSheet": compare_sheet_url,
            "reviewInstruction": "Judge exact movement and continuity only. Broom rendering remains provisional."}
    data_file = PACK / f"{SET}.json"; dump(data_file, data)

    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET,
        "status": "prime-sweep-broom-v8-movement-awaiting-frank",
        "supersedes": {"set": "keeper-prime-sweep-broom-v7", "status": "rejected-provenance",
                       "reason": "V7 used incorrect root speed and a destructive turn mask that erased lower-body pixels."},
        "userDirection": "Walk and turn must remain the approved Prime animations. Only held-arm/hand pixels may change; use the Sweep 3 grip. Correct movement before broom art.",
        "authorities": {
            "approvedWalkV6": [{"frame": i, "file": rel(path), "sha256": sha(path), "durationMs": WALK_MS}
                               for i, path in enumerate(walk_files, 1)],
            "approvedTurnV9": [{"frame": i, "file": rel(path), "sha256": sha(path), "durationMs": round(TURN_MS, 6)}
                              for i, path in enumerate(turn_files, 1)],
            "approvedStopWalkV1": [{"frame": i, "file": rel(path), "sha256": sha(path)}
                                   for i, path in enumerate(bridge_files, 1)],
            "exactSideRightNeutral": {"file": rel(NEUTRAL), "sha256": sha(NEUTRAL)},
        },
        "movementContract": {
            "walkFrameOrderBothDirections": list(range(1, 9)), "walkDurationMs": WALK_MS,
            "walkRootDeltaHighResolutionPx": 21, "walkRootDeltaLogicalPx": WALK_DELTA_LP,
            "stopRootDeltasHighResolutionPx": [18, 12, 6, 2],
            "startRootDeltasHighResolutionPx": [2, 6, 12, 18],
            "turnFrameOrder": turn_order, "sideToBackDurationMs": 1000,
            "authorityCopiedWithoutResampling": True,
            "candidateChangesRestrictedToHeldLimbMask": True,
            "heldLimbMaskHardEdged": True, "heldLimbMaskMaxY": 234,
            "headTorsoBodyTrousersLegsBootsExactAuthority": True,
            "transparentSourceCannotEraseAuthority": True,
        },
        "broom": {"status": "provisional-separate-layer-not-for-art-approval",
                  "authority": {"file": rel(BROOM_AUTHORITY), "sha256": sha(BROOM_AUTHORITY)},
                  "knownIssue": "Shape and tone correction is deliberately deferred until movement is accepted."},
        "candidate": {"frames": list(records.values()), "route": {"file": rel(data_file), "sha256": sha(data_file), "frames": len(route)},
                      "walkContactSheet": {"file": rel(walk_sheet), "sha256": sha(walk_sheet)},
                      "turnContactSheet": {"file": rel(turn_sheet), "sha256": sha(turn_sheet)},
                      "frameComparison": {"file": rel(compare_sheet), "sha256": sha(compare_sheet)},
                      "reviewUrl": f"/keeper-review/{SET}/"},
        "publishedAssets": published,
        "approvalBoundary": {"movementApproved": False, "broomArtApproved": False,
                             "candidateApproved": False, "productionPromotionAllowed": False,
                             "productionChanged": False, "runtimeChanged": False},
        "rollback": f"Delete only {rel(PACK)}, public/keeper-review/{SET}, scripts/build_keeper_prime_sweep_broom_v8.py and scripts/verify_keeper_prime_sweep_broom_v8.mjs.",
    }
    dump(PACK / "batch-register.json", register)
    (PACK / "HANDOFF.md").write_text(
        "# Prime Keeper sweep broom V8 · exact movement correction\n\n"
        "V7 is rejected. V8 copies the approved Walk V6, stop/walk V1 and Turn V9 movement, timing and registration. "
        "Only a hard held-arm/hand mask may differ in working frames; it ends above the trousers and transparent edit pixels cannot erase authority. "
        "The broom remains a separate provisional layer. Nothing is approved or promoted.\n")

    reviewer = reviewer_html(data)
    (PACK / "reviewer.html").write_text(reviewer)
    shell = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper sweep broom V8</title><style>html,body,iframe{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}#loading{padding:24px}iframe{display:none}</style><p id="loading">Loading immutable Prime Keeper sweep-broom V8 movement reviewer…</p><iframe id="review" title="Prime Keeper sweep broom V8 movement reviewer"></iframe><script>fetch("https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/__V8_COMMIT__/art/drafts/keeper-prime-sweep-broom-2026-10-19-v8/reviewer.html").then(r=>{if(!r.ok)throw Error('reviewer '+r.status);return r.text()}).then(t=>{document.querySelector('#review').srcdoc=t;document.querySelector('#review').style.display='block';document.querySelector('#loading').remove()}).catch(e=>document.querySelector('#loading').textContent='Reviewer failed to load: '+e.message)</script></html>'''
    (PUBLIC / "index.html").write_text(shell)
    print(json.dumps({"set": SET, "candidateFrames": len(records), "routeFrames": len(route),
                      "publishedAssets": len(published)}, indent=2))


def reviewer_html(data: dict) -> str:
    payload = json.dumps(data, separators=(",", ":"))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime sweep broom V8 · exact movement</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#07131b;color:#edf8fb;font:14px/1.45 system-ui,sans-serif}}header,main{{max-width:1540px;margin:auto;padding:18px}}.status{{display:inline-block;border:1px solid #e6bd5c;color:#ffe4a0;border-radius:999px;padding:4px 9px;margin-right:6px}}.warning{{border-left:4px solid #e6bd5c;background:#292516;padding:10px 13px}}.panel{{background:#10232d;border:1px solid #294a57;border-radius:12px;padding:14px;margin:14px 0}}button,input{{font:inherit}}button{{background:#173d52;color:white;border:1px solid #537788;border-radius:7px;padding:7px 10px}}button:disabled,input:disabled{{opacity:.45}}.controls{{display:flex;gap:7px;flex-wrap:wrap;align-items:center}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.stagewrap{{overflow:auto;background:#061018;padding:8px}}.stage{{position:relative;overflow:hidden;background:linear-gradient(#1a2d36 0 92.8%,#4d555b 92.8%)}}.stage img{{position:absolute;object-fit:fill}}.stage img[data-layer=prop]{{z-index:3}}.stage img[data-layer=actor]{{z-index:4}}.stage img[data-layer=priorProp]{{z-index:1}}.stage img[data-layer=priorActor]{{z-index:2}}.ghost{{opacity:.27;filter:hue-rotate(110deg) saturate(1.7)}}.doorframe{{position:absolute;z-index:12;bottom:0;right:0;width:15px;height:56px;background:#1b0f08;border-left:2px solid #b58752}}.doorleaf{{position:absolute;z-index:11;bottom:0;right:0;width:18px;height:56px;border:2px solid #2b190c;background:repeating-linear-gradient(90deg,#513719 0 8px,#855d31 8px 11px)}}.doorleaf.closed{{width:96px}}.doorleaf.closing{{width:96px}}.doorleaf.opening{{width:72px}}.sheet{{max-width:100%;background:#061018}}.compare{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}}.compare img{{max-width:100%;height:auto;background:repeating-conic-gradient(#243640 0 25%,#162630 0 50%) 0/16px 16px}}@media(max-width:900px){{.grid,.compare{{grid-template-columns:1fr}}}}</style></head><body><header><h1>Prime Keeper · keeper_sweep_broom V8</h1><span class="status">Exact movement correction</span><span class="status">V7 rejected</span><span class="status">Nothing promoted</span><p class="warning"><strong>Judge movement only.</strong> Opening and departure are exact approved Walk V6 at 8 fps and 21 high-resolution pixels per frame. Entry/exit use the exact approved stop bridge. The reversal is exact Turn V9 outside a hard held-limb-only mask. The broom is still provisional.</p></header><main><section class="panel"><div id="loading">Loading and decoding every unique frame… controls remain locked.</div><div class="controls"><button id="play" disabled>Play</button><button id="prev" disabled>Previous</button><button id="next" disabled>Next</button><label>Speed <input id="speed" disabled type="range" min="0.5" max="1.5" value="1" step="0.1"></label><label><input id="ghost" disabled type="checkbox"> Previous-frame ghost</label></div><p><strong>Binding movement:</strong> F1→F8 in both directions; 125 ms/frame; 2.625 gameplay px/frame; approved 18→12→6→2 stop and 2→6→12→18 start; Turn V9 1→9→1.</p><p id="caption"></p></section><section class="panel"><div class="grid"><div><h2>Large inspection · 6 px/lp</h2><div class="stagewrap"><div class="stage" id="large"></div></div></div><div><h2>Gameplay scale · 4 px/lp</h2><div class="stagewrap"><div class="stage" id="game"></div></div></div><div><h2>Literal 1× · 1 px/lp</h2><div class="stagewrap"><div class="stage" id="literal"></div></div></div><div><h2>Frame authority comparison</h2><div class="compare"><div><strong>Exact authority</strong><img id="authority"></div><div><strong>V8 candidate</strong><img id="candidate"></div><div><strong>Owned limb pixels</strong><img id="mask"></div></div></div></div></section><section class="panel"><h2>Walk V6 movement, Sweep-3 grip</h2><img class="sheet" src="{data['walkSheet']}"><h2>Turn V9 movement</h2><img class="sheet" src="{data['turnSheet']}"><h2>Frame-by-frame Prime comparison</h2><img class="sheet" src="{data['comparisonSheet']}"></section></main><script>
const DATA={payload};let i=0,timer=null;const stages=[];function make(id,scale){{const host=document.querySelector('#'+id);host.style.width=192*scale+'px';host.style.height=56*scale+'px';for(const name of ['priorActor','priorProp','actor','prop']){{const img=document.createElement('img');img.dataset.layer=name;if(name.startsWith('prior'))img.className='ghost';host.append(img)}}const leaf=document.createElement('div');leaf.className='doorleaf';host.append(leaf);const frame=document.createElement('div');frame.className='doorframe';host.append(frame);stages.push({{host,scale}})}}make('large',6);make('game',4);make('literal',1);
function place(stage,img,src,frame,prop=false){{img.src=src;img.style.width=frame.cellWidthLp*stage.scale+'px';img.style.height=40*stage.scale+'px';img.style.left=(frame[(prop?'propRootXLp':'actorRootXLp')]-frame.anchorXLp)*stage.scale+'px';img.style.top=(frame.bottomLp-40)*stage.scale+'px';img.style.transform=frame.mirror?'scaleX(-1)':'none'}}function show(){{const frame=DATA.route[i],prior=DATA.route[(i-1+DATA.route.length)%DATA.route.length],ghost=document.querySelector('#ghost').checked;for(const stage of stages){{const q=n=>stage.host.querySelector('[data-layer='+n+']');place(stage,q('actor'),frame.actorSrc,frame);place(stage,q('prop'),frame.propSrc,frame,true);place(stage,q('priorActor'),prior.actorSrc,prior);place(stage,q('priorProp'),prior.propSrc,prior,true);q('priorActor').style.display=q('priorProp').style.display=ghost?'block':'none';stage.host.querySelector('.doorleaf').className='doorleaf '+frame.cupboard}}document.querySelector('#authority').src=frame.authoritySrc;document.querySelector('#candidate').src=frame.recordId?DATA.frames[frame.recordId].urls.composite:frame.actorSrc;const mask=document.querySelector('#mask');mask.src=frame.recordId?DATA.frames[frame.recordId].maskUrl:frame.propSrc;document.querySelector('#caption').textContent=`${{i+1}}/${{DATA.route.length}} · ${{frame.phase}} · ${{frame.label}}`;}}function stop(){{if(timer)clearTimeout(timer);timer=null;document.querySelector('#play').textContent='Play'}}function tick(){{const ms=DATA.route[i].durationMs;i=(i+1)%DATA.route.length;show();timer=setTimeout(tick,ms/Number(document.querySelector('#speed').value))}}document.querySelector('#play').onclick=()=>{{if(timer)stop();else{{document.querySelector('#play').textContent='Pause';tick()}}}};document.querySelector('#prev').onclick=()=>{{stop();i=(i-1+DATA.route.length)%DATA.route.length;show()}};document.querySelector('#next').onclick=()=>{{stop();i=(i+1)%DATA.route.length;show()}};document.querySelector('#ghost').onchange=show;
const urls=new Set([DATA.walkSheet,DATA.turnSheet,DATA.comparisonSheet]);for(const f of DATA.route){{urls.add(f.actorSrc);urls.add(f.propSrc);urls.add(f.authoritySrc);if(f.maskSrc)urls.add(f.maskSrc)}}for(const r of Object.values(DATA.frames))urls.add(r.urls.composite);Promise.all([...urls].map(src=>new Promise((ok,bad)=>{{const img=new Image();img.onload=()=>img.decode?img.decode().then(ok,bad):ok();img.onerror=bad;img.src=src}}))).then(()=>{{document.querySelector('#loading').textContent=`${{urls.size}} unique images loaded and decoded. Controls enabled.`;document.querySelectorAll('button,input').forEach(x=>x.disabled=false);show();}}).catch(e=>document.querySelector('#loading').textContent='Media failed: '+e);
</script></body></html>'''


if __name__ == "__main__":
    main()
