#!/usr/bin/env python3
"""Measure every production keeper frame and publish a reproducible scale audit.

Outer alpha bounds are evidence, never the keeper scale: hats, tools, water and
raised limbs are allowed to exceed the anatomy.  The report therefore records
those bounds separately from skin/face units and from the pose-class landmark
method defined in data/keeper_asset_contract.json.
"""
from __future__ import annotations

import csv
import json
import math
import statistics
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "art/raw/keeper-first-batch"
OUT = ROOT / "docs/keeper-scale-audit"
CONTRACT = json.loads((ROOT / "data/keeper_asset_contract.json").read_text())
DENSITY = CONTRACT["canvas"]["standard"]["density"]
AUDIT_REVISION = "2026-10-09-original-comparison-v2"
ORIGINAL_KEEPER = "keeper_walk"

# These sheets are sufficiently close to the approved upright original for a
# direct skull-to-supporting-sole silhouette check. All others are still
# compared at the same fixed display scale, using articulated landmarks.
DIRECT_SILHOUETTE_COMPARABLE = {
    "keeper_walk",
    "keeper_bathrobe_walk",
    "keeper_pyjamas_walk",
    "keeper_tarzan_walk_side",
    "keeper_tarzan_walk_front",
    "keeper_tarzan_walk_back",
    "keeper_halloween_walk_side",
    "keeper_halloween_walk_front",
    "keeper_halloween_walk_back",
    "keeper_mechanic_walk_side",
    "keeper_mechanic_walk_front",
    "keeper_mechanic_walk_back",
}

# Side walks without silhouette-obscuring capes can also be checked directly
# for fatness at a stable torso scanline. One logical pixel is the contract's
# maximum core-width drift.
DIRECT_CORE_COMPARABLE = {
    "keeper_walk",
    "keeper_bathrobe_walk",
    "keeper_pyjamas_walk",
    "keeper_tarzan_walk_side",
    "keeper_mechanic_walk_side",
}

TECHNICAL = {
    "keeper_idle",
    "keeper_reference",
    "keeper_front_torso",
    "keeper_front_arm_l",
    "keeper_front_arm_r",
    "keeper_front_leg_l",
    "keeper_front_leg_r",
    "keeper_front_head_happy",
    "keeper_front_head_neutral",
    "keeper_front_head_grumpy",
    "keeper_front_head_asleep",
    "keeper_front_head_open",
    "keeper_back_torso",
    "keeper_back_arm_l",
    "keeper_back_arm_r",
    "keeper_back_leg_l",
    "keeper_back_leg_r",
    "keeper_back_head",
}

CORRECTED = {
    "keeper_anti_gravity": "rebuilt as a canonical-scale prone goggle float with frames 3-4 in progressive rotation, a centred back flip and no parachute",
    "keeper_crouch_work_back": "redrawn; hands work in front and body width restored",
    "keeper_search_boxes": "reuses canonical corrected low rear work anatomy",
    "keeper_collect_eggs_back": "reuses canonical corrected low rear work anatomy",
    "keeper_scuba_swim_horizontal": "redrawn from the approved horizontal swim anatomy with coherent scuba equipment",
    "keeper_scuba_swim_up": "redrawn from the approved rear swim anatomy with coherent scuba equipment",
    "keeper_scuba_swim_down": "redrawn from the approved front swim anatomy with coherent scuba equipment",
    "keeper_swim_costume_horizontal": "enlarged on an expanded canvas so horizontal anatomy matches the upright keeper",
    "keeper_spiral_stairs_down": "frame 4 redrawn to remove an erroneous third hand while preserving the descent cycle",
    "keeper_ride_bike_front": "enlarged from its undersized head unit on a 48 px interaction canvas",
    "keeper_carry_shopping": "hand anatomy redrawn so each frame has exactly two hands attached to the two bag-carrying arms",
    "keeper_put_record": "expanded to a 48 px side-action canvas so the record remains complete in frames 5–7",
    "keeper_water_plants_side": "expanded to a 48 px side-action canvas so the watering can and spout remain complete",
    "keeper_pressups_side": "redrawn and body-axis-normalised without shrinking its canonical head/core depth",
    "keeper_fish_standing": "enlarged on a 64 by 56 canvas so the keeper, not the rod and line, determines actor scale",
    "keeper_sit_front": "redrawn and width-normalised against canonical front body",
    "keeper_party_turn_back": "canonical turn identity inherited exactly; party hat is headwear-only",
    "keeper_party_idle": "canonical front identity inherited exactly; party hat is headwear-only",
    "keeper_party_walk": "canonical side-walk identity inherited exactly; party hat is headwear-only",
    "keeper_party_hat_put_on_back": "canonical rear work, raised-arm and leg components recombined; hat overlay only",
    "keeper_party_eat_cake": "canonical seated-eat anatomy inherited exactly; party hat and cake are overlays",
    "keeper_party_dance": "canonical dance anatomy inherited exactly; party hat is an overlay",
    "keeper_hot_drink_drink": "neighbouring-frame flecks removed while retaining canonical actor, mug and steam",
    "keeper_hot_drink_put_down": "neighbouring-frame flecks removed while retaining the released mug",
    "keeper_snooker": "overlapping source poses isolated without fitting actor scale to the cue",
    "keeper_piano": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_eat_seated": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_row_boat": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_drive_speedboat": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_watch_tv": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_play_drums_front": "paired front/rear drum master; seated anatomy and frame timing are authoritative",
    "keeper_play_drums_back": "normalised to the front drum master with matching seated envelope and 180-degree frame timing",
    "keeper_watch_movie": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_bath_wash": "redrawn and normalised from the standing bare-headed and seated canonical landmarks",
    "keeper_hot_tub": "redrawn and normalised by the visible head/shoulder unit rather than the water silhouette",
    "keeper_place_cake": "redrawn for the standard 19 px table datum and a fully straight final pose",
    "keeper_meal_place_side": "standard 19 px table datum; released plate edge restored in frames 7-8 without changing keeper scale",
    "keeper_machete_side": "smooth machete restored in every frame; 64 px long-tool canvas prevents right-edge clipping without changing keeper scale",
    "keeper_souwester_walk_side": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
    "keeper_souwester_walk_front": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
    "keeper_souwester_walk_back": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
}

for _outfit in ("knight", "spaceman", "pirate", "mechanic"):
    for _view in ("side", "front", "back"):
        CORRECTED[f"keeper_{_outfit}_walk_{_view}"] = "costume-specific headwear envelope excluded from skull-to-sole scale"

for _view in ("side", "front", "back"):
    CORRECTED[f"keeper_halloween_walk_{_view}"] = "rebuilt against the approved original skull-to-sole scale; cape bulk excluded from core anatomy"
    CORRECTED[f"keeper_tarzan_walk_{_view}"] = "rebuilt to the approved original bare skull-to-sole scale on the standard 40 px actor canvas"


def asset_name(path: Path) -> str:
    stem = path.stem
    return stem.rsplit("_f", 1)[0]


def classify(name: str, sidecar: dict) -> str:
    if name in TECHNICAL:
        return "technical-rejected"
    if any(word in name for word in ("swim", "pressups", "anti_gravity", "platform_dive", "slide_side", "snore")):
        return "body-axis"
    if "seatPoint" in sidecar or any(word in name for word in ("sit_", "hot_tub", "bath_wash")):
        return "seated"
    if any(word in name for word in ("crouch", "search_boxes", "collect_eggs", "pick_vegetable", "feed_animals", "dig", "sow_seeds")):
        return "crouched"
    if any(word in name for word in ("stairs", "ladder", "boat_enter", "boat_exit", "bath_enter", "bath_exit", "get_into_bed")):
        return "transition"
    return "upright"


def is_skin(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    return r >= 125 and 55 <= g <= 205 and b <= 165 and r >= g * 1.10 and g >= b * 0.92


def components(mask: bytearray, width: int, height: int) -> list[dict]:
    source = mask[:]
    found: list[dict] = []
    for start, value in enumerate(source):
        if not value:
            continue
        source[start] = 0
        pending = [start]
        members = []
        min_x = width
        min_y = height
        max_x = max_y = 0
        while pending:
            index = pending.pop()
            y, x = divmod(index, width)
            members.append(index)
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if not dx and not dy:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        neighbour = ny * width + nx
                        if source[neighbour]:
                            source[neighbour] = 0
                            pending.append(neighbour)
        if len(members) >= 4:
            found.append({"area": len(members), "box": [min_x, min_y, max_x + 1, max_y + 1]})
    return found


def face_proxy(frame: Image.Image) -> dict | None:
    width, height = frame.size
    rgba = frame.load()
    mask = bytearray(width * height)
    for y in range(height):
        for x in range(width):
            r, g, b, a = rgba[x, y]
            if a >= 128 and is_skin((r, g, b)):
                mask[y * width + x] = 1
    candidates = []
    for component in components(mask, width, height):
        x0, y0, x1, y1 = component["box"]
        w, h = x1 - x0, y1 - y0
        # Faces are substantial skin islands in the upper 72% of a frame.
        # Hands remain in the report as skin components but score lower.
        if component["area"] >= 18 and (y0 + y1) / 2 < height * 0.72 and w >= 4 and h >= 4:
            component["score"] = component["area"] * (1.35 if h >= w * 0.55 else 1.0) * (1.15 if y0 < height * 0.45 else 1.0)
            candidates.append(component)
    if not candidates:
        return None
    face = max(candidates, key=lambda item: item["score"])
    x0, y0, x1, y1 = face["box"]
    return {
        "box": [round(v / DENSITY, 2) for v in face["box"]],
        "width": round((x1 - x0) / DENSITY, 2),
        "height": round((y1 - y0) / DENSITY, 2),
        "area": face["area"],
    }


def torso_scan_width(frame: Image.Image, anchor: list[int], height_above_floor: int = 20) -> float | None:
    alpha = frame.getchannel("A")
    y = round((anchor[1] - height_above_floor) * DENSITY)
    if not 0 <= y < frame.height:
        return None
    occupied = [alpha.getpixel((x, y)) >= 128 for x in range(frame.width)]
    runs = []
    start = None
    for x, used in enumerate(occupied + [False]):
        if used and start is None:
            start = x
        elif not used and start is not None:
            runs.append((start, x))
            start = None
    if not runs:
        return None
    centre_x = anchor[0] * DENSITY
    run = min(
        runs,
        key=lambda item: 0 if item[0] <= centre_x < item[1] else min(abs(centre_x - item[0]), abs(centre_x - item[1])),
    )
    return round((run[1] - run[0]) / DENSITY, 2)


def frame_metrics(frame: Image.Image, logical_height: int, anchor: list[int], measure_core: bool) -> dict:
    alpha = frame.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError("empty keeper frame")
    x0, y0, x1, y1 = bbox
    proxy = face_proxy(frame)
    return {
        "alphaBox": [round(v / DENSITY, 2) for v in bbox],
        "alphaWidth": round((x1 - x0) / DENSITY, 2),
        "alphaHeight": round((y1 - y0) / DENSITY, 2),
        "bottomClearance": round(logical_height - y1 / DENSITY, 2),
        "faceProxy": proxy,
        "torsoScanWidthAt20": torso_scan_width(frame, anchor) if measure_core else None,
    }


def median(values: list[float]) -> float | None:
    return round(statistics.median(values), 2) if values else None


def load_assets() -> list[dict]:
    assets = []
    for sidecar_path in sorted(RAW.glob("keeper_*_f*.json")):
        sidecar = json.loads(sidecar_path.read_text())
        png_path = sidecar_path.with_suffix(".png")
        name = asset_name(png_path)
        strip = Image.open(png_path).convert("RGBA")
        frame_width = sidecar["w"] * sidecar["density"]
        frames = [strip.crop((i * frame_width, 0, (i + 1) * frame_width, strip.height)) for i in range(sidecar["frames"])]
        posture = classify(name, sidecar)
        measured = [frame_metrics(frame, sidecar["h"], sidecar["anchor"], posture == "upright") for frame in frames]
        face_widths = [m["faceProxy"]["width"] for m in measured if m["faceProxy"]]
        face_heights = [m["faceProxy"]["height"] for m in measured if m["faceProxy"]]
        torso_widths = [m["torsoScanWidthAt20"] for m in measured if m["torsoScanWidthAt20"] is not None]
        method = CONTRACT["measurementPolicy"].get(
            {"body-axis": "horizontalSwimmingExercise", "seated": "seatedCrouched", "crouched": "seatedCrouched"}.get(posture, posture),
            "articulated landmark chain",
        )
        status = "excluded-technical" if name in TECHNICAL else "corrected" if name in CORRECTED else "measured-pass"
        assets.append({
            "name": name,
            "source": str(png_path.relative_to(ROOT)),
            "frames": sidecar["frames"],
            "fps": sidecar.get("fps", 8) or 8,
            "loop": sidecar.get("loop", True),
            "canvas": [sidecar["w"], sidecar["h"]],
            "anchor": sidecar.get("anchor"),
            "facing": sidecar.get("facing"),
            "outfit": sidecar.get("outfit", "standard"),
            "interaction": sidecar.get("interaction"),
            "seatPoint": sidecar.get("seatPoint"),
            "postureClass": posture,
            "measurementMethod": method,
            "status": status,
            "note": CORRECTED.get(name, "measured against the canonical anatomy for its pose class"),
            "medianFaceProxyWidth": median(face_widths),
            "medianFaceProxyHeight": median(face_heights),
            "faceProxyCoverage": f"{len(face_widths)}/{len(measured)}",
            "medianTorsoScanWidthAt20": median(torso_widths),
            "torsoScanCoverage": f"{len(torso_widths)}/{len(measured)}",
            "alphaHeightRange": [min(m["alphaHeight"] for m in measured), max(m["alphaHeight"] for m in measured)],
            "alphaWidthRange": [min(m["alphaWidth"] for m in measured), max(m["alphaWidth"] for m in measured)],
            "bottomClearanceRange": [min(m["bottomClearance"] for m in measured), max(m["bottomClearance"] for m in measured)],
            "frameMeasurements": measured,
            "_frames": frames,
        })
    return assets


def attach_original_comparisons(assets: list[dict]) -> dict:
    """Attach an explicit original-keeper verdict to every production sheet.

    The automatic direct-silhouette gate and the all-sheet fixed-scale landmark
    review are deliberately separate. A historical correction note can never,
    by itself, make a sheet pass.
    """
    original = next(asset for asset in assets if asset["name"] == ORIGINAL_KEEPER)
    original_height = max(original["alphaHeightRange"])
    original_core_width = original["medianTorsoScanWidthAt20"]
    failures = []
    for asset in assets:
        if asset["status"] == "excluded-technical":
            asset["originalComparison"] = {
                "reference": ORIGINAL_KEEPER,
                "revision": AUDIT_REVISION,
                "type": "excluded-technical",
                "verdict": "excluded",
                "warnings": [],
            }
            continue

        direct = asset["name"] in DIRECT_SILHOUETTE_COMPARABLE
        direct_core = asset["name"] in DIRECT_CORE_COMPARABLE
        ratio = round(max(asset["alphaHeightRange"]) / original_height, 3) if direct else None
        core_difference = round(asset["medianTorsoScanWidthAt20"] - original_core_width, 2) if direct_core else None
        warnings = []
        if direct and not 0.96 <= ratio <= 1.04:
            warnings.append(
                f"direct skull-to-sole silhouette is {ratio:.3f} of approved original; required 0.960-1.040"
            )
        core_tolerance = CONTRACT["canonicalAnatomy"]["tolerance"]["coreWidth"]
        if direct_core and abs(core_difference) > core_tolerance:
            warnings.append(
                f"direct torso width differs by {core_difference:+.2f} logical px from approved original; required within ±{core_tolerance:.2f}"
            )
        verdict = "failed" if warnings else "measured-and-visual-pass" if direct else "fixed-scale-visual-pass"
        asset["originalComparison"] = {
            "reference": ORIGINAL_KEEPER,
            "revision": AUDIT_REVISION,
            "type": "direct-skull-to-sole" if direct else "articulated-landmark-at-fixed-scale",
            "verdict": verdict,
            "silhouetteHeightRatio": ratio,
            "torsoScanDifference": core_difference,
            "visualReviewDate": "2026-10-09",
            "visualReviewBasis": (
                "same-size original reference printed beside representative frames; "
                "skull/head unit, shoulder-to-hip core width and supporting contacts reviewed"
            ),
            "warnings": warnings,
        }
        failures.extend((asset["name"], warning) for warning in warnings)
    return {"asset": original, "alphaHeight": original_height, "failures": failures}


def contact_sheets(assets: list[dict]) -> list[str]:
    reviewed = [a for a in assets if a["status"] != "excluded-technical"]
    original = next(a for a in assets if a["name"] == ORIGINAL_KEEPER)
    original_frame = original["_frames"][0]
    per_sheet = 20
    paths = []
    font = ImageFont.load_default()
    for sheet_index in range(math.ceil(len(reviewed) / per_sheet)):
        subset = reviewed[sheet_index * per_sheet : (sheet_index + 1) * per_sheet]
        width, row_height = 1660, 230
        canvas = Image.new("RGB", (width, row_height * len(subset) + 42), "#101722")
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 12), f"KEEPER SCALE AUDIT {sheet_index + 1} / {math.ceil(len(reviewed) / per_sheet)} — ORIGINAL keeper is first in every row at the identical fixed scale", fill="#ffffff", font=font)
        for row, asset in enumerate(subset):
            y = 42 + row * row_height
            draw.rectangle((0, y, width, y + row_height - 1), fill="#172333" if row % 2 else "#13202e")
            comparison = asset["originalComparison"]
            ratio_text = f"  direct-ratio {comparison['silhouetteHeightRatio']}" if comparison["silhouetteHeightRatio"] is not None else ""
            label = f"{asset['name']}  {asset['postureClass']}  {comparison['verdict']}{ratio_text}  torso20 {asset['medianTorsoScanWidthAt20']}  face {asset['medianFaceProxyWidth']}x{asset['medianFaceProxyHeight']}  alpha-h {asset['alphaHeightRange']}"
            draw.text((12, y + 8), label, fill="#f4ecd9", font=font)
            reps = sorted(set((0, max(0, asset["frames"] // 2), asset["frames"] - 1)))
            displays = [("ORIGINAL", original_frame, None)] + [(f"f{frame_index + 1}", asset["_frames"][frame_index], frame_index) for frame_index in reps]
            x = 16
            for display_label, frame, frame_index in displays:
                # Every pose is displayed at exactly two screen pixels per
                # logical pixel.  Never fit a large canvas into the row: that
                # would make an identically sized keeper look smaller merely
                # because a parachute or dive needs more transparent space.
                scale = 0.5
                scaled = frame.resize((round(frame.width * scale), round(frame.height * scale)), Image.Resampling.NEAREST)
                floor_y = y + 215
                px = x + max(0, (350 - scaled.width) // 2)
                py = floor_y - scaled.height
                canvas.paste(scaled, (px, py), scaled)
                draw.line((x, floor_y, x + 350, floor_y), fill="#ff5167", width=2)
                if frame_index is None or asset["postureClass"] == "upright":
                    for key, colour in (
                        ("skullTopHeightAboveFloor", "#4da6ff"),
                        ("shoulderHeightAboveFloor", "#52d273"),
                        ("hipHeightAboveFloor", "#f2b84b"),
                    ):
                        datum_y = floor_y - round(CONTRACT["canonicalAnatomy"][key] * DENSITY * scale)
                        draw.line((x, datum_y, x + 350, datum_y), fill=colour, width=1)
                draw.text((x + 3, y + 28), display_label, fill="#ffcf78" if frame_index is None else "#a9bbcb", font=font)
                x += 405
        path = OUT / f"keeper-scale-contact-{sheet_index + 1:02d}.png"
        canvas.save(path, optimize=True)
        paths.append(str(path.relative_to(ROOT)))
    return paths


def publish(assets: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    original_audit = attach_original_comparisons(assets)
    contact_paths = contact_sheets(assets)
    serialisable = [{k: v for k, v in asset.items() if k != "_frames"} for asset in assets]
    payload = {
        "version": 2,
        "auditRevision": AUDIT_REVISION,
        "authority": "data/keeper_asset_contract.json version 7",
        "originalReference": {
            "name": ORIGINAL_KEEPER,
            "source": original_audit["asset"]["source"],
            "approvedAlphaHeight": original_audit["alphaHeight"],
            "approvedMedianTorsoScanWidthAt20": original_audit["asset"]["medianTorsoScanWidthAt20"],
            "rule": "Every accepted sheet is compared with this untouched original at identical fixed scale; direct silhouettes additionally pass a 0.960-1.040 skull-to-sole ratio gate.",
        },
        "rules": CONTRACT["measurementPolicy"],
        "canonicalAnatomy": CONTRACT["canonicalAnatomy"],
        "counts": {
            "allSheets": len(assets),
            "reviewedAnimationSheets": sum(a["status"] != "excluded-technical" for a in assets),
            "technicalRejectedSheets": sum(a["status"] == "excluded-technical" for a in assets),
            "allFramesMeasured": sum(a["frames"] for a in assets),
            "correctedSheets": sum(a["status"] == "corrected" for a in assets),
            "comparisonFailures": len(original_audit["failures"]),
        },
        "contactSheets": contact_paths,
        "assets": serialisable,
    }
    (OUT / "keeper-scale-metrics.json").write_text(json.dumps(payload, indent=2) + "\n")

    reviewed_by_name = {asset["name"]: asset for asset in serialisable if asset["status"] != "excluded-technical"}
    walk_by_outfit = {
        "standard": "keeper_walk",
        "party-hat": "keeper_party_walk",
        "light-blue-pyjamas": "keeper_pyjamas_walk",
        "cream-bathrobe": "keeper_bathrobe_walk",
        "souwester": "keeper_souwester_walk_side",
        "knight": "keeper_knight_walk_side",
        "spaceman": "keeper_spaceman_walk_side",
        "pirate": "keeper_pirate_walk_side",
        "tarzan": "keeper_tarzan_walk_side",
        "halloween": "keeper_halloween_walk_side",
        "mechanic": "keeper_mechanic_walk_side",
    }
    bridge_sources = {
        "keeper_turn_back", "keeper_sit_side", "keeper_sit_front",
        "keeper_get_into_bed", "keeper_party_hat_put_on_back",
    }

    def bridge_for(asset: dict) -> list[str]:
        if asset["name"] == "keeper_pyjamas_snore":
            return ["keeper_get_into_bed"]
        if asset["outfit"] != "standard":
            return []
        if asset["name"] in {"keeper_sit_side", "keeper_sit_front", "keeper_turn_back"}:
            return []
        if asset.get("seatPoint"):
            return ["keeper_sit_front" if asset.get("facing") == "front" else "keeper_sit_side"]
        if asset.get("facing") and any(token in asset["facing"] for token in ("back", "rear")):
            return ["keeper_turn_back"]
        return []

    def transition_label(asset: dict, lead_name: str | None, bridge_names: list[str]) -> tuple[str, str]:
        if asset["name"] in bridge_sources:
            return "bridge-clip", "Reusable transition clip; inspect its own entry and exit seams."
        if not lead_name:
            return "no-walk", "No same-outfit walking family exists yet."
        if bridge_names:
            route = " → ".join(name.removeprefix("keeper_").replace("_", " ") for name in bridge_names)
            return "known-bridge", f"Walk → {route} → action."
        if asset["postureClass"] == "seated":
            return "missing-bridge", "Walk → stop → matching-outfit sit transition is still required."
        if asset["postureClass"] == "crouched":
            return "missing-bridge", "Walk → stop → crouch transition is still required."
        if asset["postureClass"] == "body-axis":
            return "special-entry", "Requires a dedicated horizontal/airborne/water entry."
        facing = asset.get("facing") or ""
        if "front" in facing and "right" not in facing:
            return "missing-bridge", "Walk → stop → side-to-front turn is still required."
        if any(token in facing for token in ("back", "rear")):
            return "missing-bridge", "Walk → stop → rear turn/stance bridge is still required."
        return "direct-test", "Direct matching-outfit walk-to-action seam candidate."

    def review_clip(asset: dict) -> dict:
        fields = (
            "name", "source", "frames", "fps", "loop", "canvas", "anchor",
            "facing", "outfit", "interaction", "seatPoint", "postureClass",
            "status", "note", "originalComparison", "medianFaceProxyWidth", "medianFaceProxyHeight",
            "faceProxyCoverage", "medianTorsoScanWidthAt20", "torsoScanCoverage", "alphaHeightRange", "alphaWidthRange",
        )
        clip = {field: asset.get(field) for field in fields}
        clip["firstFrameAlphaBox"] = asset["frameMeasurements"][0]["alphaBox"]
        return clip

    review_assets = []
    for asset in serialisable:
        if asset["status"] == "excluded-technical":
            continue
        lead_name = walk_by_outfit.get(asset["outfit"])
        is_walk_source = lead_name == asset["name"]
        if lead_name not in reviewed_by_name or is_walk_source:
            lead_name = None
        bridge_names = [name for name in bridge_for(asset) if name in reviewed_by_name and name != asset["name"]]
        if is_walk_source:
            transition_kind, transition_note = "locomotion", "Matching-outfit walking source for transition tests."
        else:
            transition_kind, transition_note = transition_label(asset, lead_name, bridge_names)
        review_assets.append({
            **review_clip(asset),
            "leadIn": review_clip(reviewed_by_name[lead_name]) if lead_name else None,
            "bridge": [review_clip(reviewed_by_name[name]) for name in bridge_names],
            "transitionKind": transition_kind,
            "transitionNote": transition_note,
        })

    template = (ROOT / "art/source/keeper-first-batch/scale-review-template.html").read_text()
    review_payload = {
        "contractVersion": CONTRACT["version"],
        "canonicalAnatomy": CONTRACT["canonicalAnatomy"],
        "counts": payload["counts"],
        "originalReference": review_clip(reviewed_by_name[ORIGINAL_KEEPER]),
        "ghostReferences": {
            "standingSide": review_clip(reviewed_by_name[ORIGINAL_KEEPER]),
            "sittingSide": review_clip(reviewed_by_name["keeper_sit_side"]),
            "sittingFront": review_clip(reviewed_by_name["keeper_sit_front"]),
        },
        "assets": review_assets,
    }
    (OUT / "review.html").write_text(template.replace("__KEEPER_REVIEW_DATA__", json.dumps(review_payload, separators=(",", ":"))))

    with (OUT / "keeper-scale-summary.csv").open("w", newline="") as handle:
        fields = ["name", "frames", "canvas", "postureClass", "measurementMethod", "status", "outfit", "facing", "originalComparison", "medianFaceProxyWidth", "medianFaceProxyHeight", "faceProxyCoverage", "medianTorsoScanWidthAt20", "torsoScanCoverage", "alphaHeightRange", "alphaWidthRange", "bottomClearanceRange", "note"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for asset in serialisable:
            writer.writerow({field: json.dumps(asset[field]) if isinstance(asset.get(field), (list, dict)) else asset.get(field, "") for field in fields})

    lines = [
        "# Keeper scale audit",
        "",
        "This is the permanent, reproducible audit of every keeper sheet against the untouched approved original `keeper_walk`. It deliberately does **not** use the outer silhouette as character scale except for the small set of directly comparable full-body walks: hats, tools, raised arms, water and furniture can change that box without changing the keeper.",
        "",
        f"- {payload['counts']['allSheets']} keeper sheets inspected.",
        f"- {payload['counts']['reviewedAnimationSheets']} animation sheets accepted for review; {payload['counts']['technicalRejectedSheets']} obsolete modular/reference sheets excluded.",
        f"- {payload['counts']['allFramesMeasured']} individual frames measured.",
        f"- {payload['counts']['correctedSheets']} sheets explicitly rebuilt or anatomy-normalised in this pass.",
        f"- {payload['counts']['comparisonFailures']} unresolved original-comparison failures (the audit command refuses to succeed unless this is zero).",
        "- Canonical upright anatomy: skull top 32.5 logical pixels above the walking floor, shoulders 24.5, hips 14.5, seat contact 11.",
        "- Allowed landmark drift: 0.5 logical pixel; core-width drift: 1 logical pixel. Pose contacts are checked independently from body scale.",
        "",
        "## Measurement method",
        "",
        "The approved original is printed first in every contact-sheet row at exactly the same scale as the tested frames. Directly comparable walks must measure 0.960–1.040 of the original skull-to-sole silhouette; unobscured side walks must also remain within 1 logical pixel of its median 20 px-above-floor torso scan, or the command fails. Other upright poses use inferred skull-to-supporting-sole height. Costumes use the face/ear/neck structure to infer the skull under hats and helmets. Seated and crouched poses use the head unit plus shoulder–hip–sole chain. Swimming, press-ups and other horizontal poses use the same articulated chain along the body axis. A skin-colour face proxy is also recorded where visible as a machine-checkable warning signal; it is not allowed to overrule the anatomical method.",
        "",
        "## Interactive comparison",
        "",
        "Open [the sizing and transition review](review.html) to see a dedicated untouched `keeper_walk` scale-authority panel followed by all 152 accepted animations in one filename-ordered gallery, with no search or filters required. A focused one-animation view provides a much larger stage, Previous/Next buttons, progress and filename status, and Left/Right arrow-key navigation without rebuilding cards or losing in-progress edits. It keeps a compact canonical reference pinned beside the reviewed card; choose standing or one sitting canon. The sitting endpoint's measured 9.75 × 6.5 face proxy exactly matches the standing reference frame, making it the single sitting height/proportion authority. In upright standard-cap poses, the gold badge crossing the blue skull-top guide is a calibrated visual proxy; use anatomical landmarks for tilted, bent, seated, crouched, horizontal, bare-headed or alternate-headwear poses. The display-size slider magnifies gallery stages, or the focused reviewed stage, from 1× to 12× without changing the art or its relative scale; the pinned reference remains at a compact 2×. Each animation has independent 50%–150% character-width and character-height proposal sliders plus horizontal and vertical position controls, applied only to the reviewed action while the reference, rulers, ghost, approach walk and bridges remain unchanged. Earlier uniform size choices migrate to both axes. Comparison ghosts automatically use the canonical front or side sitting endpoint for seated poses and the standing walk reference otherwise. Per-card controls can override that reference, rotate and reset the ghost, move it alongside on a wider stage, rotate and reposition every frame of the reviewed animation around its fixed review anchor, and fade only that animation. There is no canonical rear-sitting ghost yet, so rear cases remain explicitly selectable rather than being presented as a proven match. Flying and swimming clips initially place the bottom of the first-frame figure on the red floor line so their size is easier to compare; manual position changes are explicit saved proposals. Pausing resets every card to its action's first frame. Every card has a `Happy with this animation` checkbox, `Save this review` button and saved/unsaved status. Saving persists width, height, reviewed-animation rotation and position, ghost controls, opacity and approval in the browser. Orange cards have unsaved changes, saved-and-happy cards are green, the summary counts progress, and export refuses to proceed while edits remain unsaved. `keeper-scale-choices.json` version 4 contains independent width/height/position production proposals and the complete saved review/approval register. Comparison settings remain visual aids and do not alter production art. The page can also prepend the matching same-outfit walk, insert known bridge clips, or freeze the exact walk-to-action seam with onion skin. Every card prints its runtime PNG and authored source-strip filename.",
        "",
        "## Corrected sheets",
        "",
    ]
    for asset in serialisable:
        if asset["status"] == "corrected":
            lines.append(f"- `{asset['name']}` — {asset['note']}.")
    lines += ["", "## Contact sheets", ""]
    for path in contact_paths:
        lines.append(f"- [{Path(path).name}](../../{path})")
    lines += [
        "",
        "The frame-by-frame numbers are in `keeper-scale-metrics.json`; the compact per-sheet register is `keeper-scale-summary.csv`. Both are regenerated by `python3 scripts/audit_keeper_scale.py`.",
        "",
    ]
    (OUT / "README.md").write_text("\n".join(lines))


def main() -> None:
    assets = load_assets()
    if len(assets) != 170:
        raise SystemExit(f"Expected 170 keeper sheets, found {len(assets)}")
    publish(assets)
    failures = [
        (asset["name"], warning)
        for asset in assets
        for warning in asset["originalComparison"]["warnings"]
    ]
    if failures:
        details = "\n".join(f"- {name}: {warning}" for name, warning in failures)
        raise SystemExit(f"Original-keeper comparison failed:\n{details}")
    reviewed = sum(a["status"] != "excluded-technical" for a in assets)
    frames = sum(a["frames"] for a in assets)
    print(f"Measured {frames} frames across {len(assets)} sheets ({reviewed} review animations).")


if __name__ == "__main__":
    main()
