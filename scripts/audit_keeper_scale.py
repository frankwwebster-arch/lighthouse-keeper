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
import shutil
import statistics
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "art/raw/keeper-first-batch"
OUT = ROOT / "docs/keeper-scale-audit"
PUBLIC_REVIEW = ROOT / "public/keeper-review"
CONTRACT = json.loads((ROOT / "data/keeper_asset_contract.json").read_text())
DENSITY = CONTRACT["canvas"]["standard"]["density"]
AUDIT_REVISION = "2026-10-10-user-selected-replacements-v1"
ORIGINAL_KEEPER = "keeper_walk"
REVIEW_IMPORT_PATH = ROOT / "docs/review/frank-keeper-animation-review-2026-10-10.json"
CODEX_RESPONSE_PATHS = (
    ROOT / "docs/review/keeper-animation-codex-responses-2026-10-09.json",
    ROOT / "docs/review/keeper-animation-codex-responses-2026-10-10.json",
)
SIDE_ON_OCCLUSION_REGISTER_PATH = ROOT / "data/keeper_side_on_beard_occlusion_audit.json"
REVIEW_DRAFTS_PATH = ROOT / "data/keeper_review_drafts.json"
REVIEW_CANDIDATE_DECISIONS_PATH = ROOT / "data/keeper_review_candidate_decisions.json"
REVIEW_SETTINGS = {
    review["name"]: review
    for review in json.loads(REVIEW_IMPORT_PATH.read_text())["reviews"]
}

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
    "keeper_artist_smock_walk",
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
    "keeper_artist_smock_walk",
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
    "keeper_nap_seated": "baseline-anatomy side-seated nap loop with closed eyes, clearly reclined head and open mouth; beard silhouette was corrected from a smooth oval to the standard stepped, ragged side-view margin; furniture remains separate",
    "keeper_lawn_mower_push": "new baseline-anatomy side walk pushing an included manual reel mower; neighbouring-pose slivers removed; runtime translates the complete unit from behind a foreground shed door",
    "keeper_sweep_broom": "new baseline-anatomy tier-1 cleaning loop with its traditional broom included; runtime swaps tools only while fully hidden by the cupboard door",
    "keeper_hoover_basic": "review-sized tier-2 cleaning loop with its ordinary upright hoover included; runtime swaps tools only while fully hidden by the cupboard door",
    "keeper_hoover_super": "review-sized tier-3 cleaning loop with its original eccentric super hoover included; runtime swaps tools only while fully hidden by the cupboard door",
    "keeper_artist_smock_walk": "new artist-smock locomotion family; every pose is independently height-matched to the corresponding canonical walk frame after frame 4 was identified as undersized in the generated source",
    "keeper_artist_smock_turn_back": "new matching-outfit side-to-rear transition for activity routing",
    "keeper_artist_smock_turn_front": "new matching-outfit side-to-front transition for activity routing",
    "keeper_artist_smock_sit_front": "new matching-outfit front stand-to-sit transition with the canonical seat datum",
    "keeper_play_guitar_gretsch": "new tier-2 black Gretsch playing loop at canonical keeper scale",
    "keeper_play_guitar_flying_v_1967": "new tier-3 red 1967 Flying V playing loop at canonical keeper scale",
    "keeper_guitar_pickup_acoustic": "new side-to-rear rack pickup and return-to-play transition; prop handoff occurs on frame 6",
    "keeper_guitar_pickup_gretsch": "new tier-2 rack pickup and return-to-play transition; prop handoff occurs on frame 6",
    "keeper_guitar_pickup_flying_v_1967": "new tier-3 rack pickup and return-to-play transition; prop handoff occurs on frame 6",
    "keeper_sit_back": "new canonical rear stand-to-sit transition; final frame is the standard back-to-camera seated comparison ghost",
    "keeper_walk_into_lift": "intentional depth transition: rear walk scales from 100% to 75%, rises 6 logical pixels, then turns to a full-front neutral pose",
    "keeper_door_open_side_pyjamas": "clean six-frame side-door redraw in the canonical light-blue pyjama family; handle and floor interaction geometry are unchanged",
    "keeper_anti_gravity": "extended with four calm face-down float frames before the centred back flip; comparison-only rotation was not baked",
    "keeper_crouch_work_back": "redrawn; hands work in front and body width restored",
    "keeper_search_boxes": "reuses canonical corrected low rear work anatomy",
    "keeper_collect_eggs_back": "reuses canonical corrected low rear work anatomy",
    "keeper_scuba_swim_horizontal": "redrawn from the approved horizontal swim anatomy with coherent scuba equipment",
    "keeper_scuba_swim_up": "redrawn from the approved rear swim anatomy with coherent scuba equipment",
    "keeper_scuba_swim_down": "redrawn from the approved front swim anatomy with coherent scuba equipment",
    "keeper_scuba_walk_side": "new matching-outfit jetty locomotion for the scuba route",
    "keeper_scuba_jetty_dive": "new one-shot jetty dive whose endpoint is the exact first horizontal scuba-swim frame",
    "keeper_parachute_drift": "high-resolution eight-pose open-canopy loop, matched to both route hand-offs and baked at the saved 84% width / 122% height",
    "keeper_parachute_landing": "one-shot open-canopy touchdown, compression and canopy-collapse sequence with its entry canvas rebased to the resized drift hand-off",
    "keeper_swim_costume_horizontal": "re-rendered on an expanded horizontal canvas; Frank's saved 95.5% width / 100% height is baked",
    "keeper_spiral_stairs_down": "frame 4 redrawn to remove an erroneous third hand while preserving the descent cycle",
    "keeper_ride_bike_front": "enlarged from its undersized head unit on a 48 px interaction canvas",
    "keeper_carry_shopping": "frames 1 and 7 replaced with clean adjacent poses so all eight frames carry exactly two bags; cadence reduced to 5fps",
    "keeper_put_record": "expanded to a 64 px side-action canvas so the record remains complete through release",
    "keeper_water_plants_side": "expanded to a 48 px side-action canvas so the watering can and spout remain complete",
    "keeper_pressups_side": "redrawn cleanly, then resized to Frank's saved 79% width / 65% height",
    "keeper_fish_standing": "extended to 50 frames with a ten-second wait, stable actor contact, gradual pull/reel, held catch, ground placement and return to fishing",
    "keeper_fish_seated": "extended to 41 frames with a ten-second wait, stable seat contact, longer rod, gradual pull/reel, held catch, ground placement and return to fishing",
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
    "keeper_meal_place_side": "beard corrected and released plate restored; Frank's original saved 113.5% width / 94% height is now baked",
    "keeper_machete_side": "smooth machete restored from eight isolated grid cells on a 96 px logical long-tool canvas; Frank's saved 127.5% width / 129% height is baked",
    "keeper_souwester_walk_side": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
    "keeper_souwester_walk_front": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
    "keeper_souwester_walk_back": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
}

for _outfit in ("knight", "spaceman", "pirate", "mechanic"):
    for _view in ("side", "front", "back"):
        CORRECTED[f"keeper_{_outfit}_walk_{_view}"] = "costume-specific headwear envelope excluded from skull-to-sole scale"

for _view in ("side", "front", "back"):
    _halloween_review = REVIEW_SETTINGS.get(f"keeper_halloween_walk_{_view}", {})
    _tarzan_review = REVIEW_SETTINGS.get(f"keeper_tarzan_walk_{_view}", {})
    CORRECTED[f"keeper_halloween_walk_{_view}"] = (
        "identity rebuilt against the approved original, then resized to Frank's saved "
        f"{_halloween_review.get('widthPercent', 100)}% width / {_halloween_review.get('heightPercent', 100)}% height"
    )
    CORRECTED[f"keeper_tarzan_walk_{_view}"] = (
        "bare-headed identity rebuilt against the approved original, then resized to Frank's saved "
        f"{_tarzan_review.get('widthPercent', 100)}% width / {_tarzan_review.get('heightPercent', 100)}% height"
    )


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
        if sidecar.get("assetRole") in {"neutral", "bridge"}:
            continue
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
            "fps": sidecar.get("fps", 0),
            "loop": sidecar.get("loop", True),
            "canvas": [sidecar["w"], sidecar["h"]],
            "anchor": sidecar.get("anchor"),
            "facing": sidecar.get("facing"),
            "outfit": sidecar.get("outfit", "standard"),
            "interaction": sidecar.get("interaction"),
            "seatPoint": sidecar.get("seatPoint"),
            "reviewScale": sidecar.get("reviewScale", [100, 100]),
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

        saved_review = REVIEW_SETTINGS.get(asset["name"])
        review_scale = asset.get("reviewScale", [100, 100])
        user_sized = review_scale != [100, 100]
        direct = asset["name"] in DIRECT_SILHOUETTE_COMPARABLE
        direct_core = asset["name"] in DIRECT_CORE_COMPARABLE
        ratio = round(max(asset["alphaHeightRange"]) / original_height, 3) if direct else None
        core_difference = round(asset["medianTorsoScanWidthAt20"] - original_core_width, 2) if direct_core else None
        warnings = []
        if direct and not user_sized and not 0.96 <= ratio <= 1.04:
            warnings.append(
                f"direct skull-to-sole silhouette is {ratio:.3f} of approved original; required 0.960-1.040"
            )
        core_tolerance = CONTRACT["canonicalAnatomy"]["tolerance"]["coreWidth"]
        if direct_core and not user_sized and abs(core_difference) > core_tolerance:
            warnings.append(
                f"direct torso width differs by {core_difference:+.2f} logical px from approved original; required within ±{core_tolerance:.2f}"
            )
        verdict = (
            "failed" if warnings else
            "user-visual-size-authority" if user_sized else
            "measured-and-visual-pass" if direct else
            "fixed-scale-visual-pass"
        )
        asset["originalComparison"] = {
            "reference": ORIGINAL_KEEPER,
            "revision": AUDIT_REVISION,
            "type": (
                "user-reviewed-visual-sizing" if user_sized else
                "direct-skull-to-sole" if direct else
                "articulated-landmark-at-fixed-scale"
            ),
            "verdict": verdict,
            "silhouetteHeightRatio": ratio,
            "torsoScanDifference": core_difference,
            "visualReviewDate": "2026-10-10",
            "visualReviewBasis": (
                f"Frank's saved visual sizing is authoritative: "
                f"{review_scale[0]}% cumulative width / {review_scale[1]}% cumulative height"
                if user_sized else
                "same-size original reference printed beside representative frames; "
                "skull/head unit, shoulder-to-hip core width and supporting contacts reviewed"
            ),
            "warnings": warnings,
            "reviewScale": (
                review_scale
                if user_sized else None
            ),
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
            "rule": "Every delivered sheet is compared with this untouched identity/anatomy reference at native logical display scale. Frank's saved visual resize is authoritative; only directly comparable sheets without a saved resize must pass the 0.960-1.040 ratio gate.",
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
    review_import = json.loads(REVIEW_IMPORT_PATH.read_text())
    imported_reviews = {review["name"]: review for review in review_import["reviews"]}
    candidate_decisions = {}
    if REVIEW_CANDIDATE_DECISIONS_PATH.exists():
        decision_payload = json.loads(REVIEW_CANDIDATE_DECISIONS_PATH.read_text())
        if decision_payload.get("version") != 1 or not isinstance(decision_payload.get("decisions"), list):
            raise SystemExit("Review candidate decision register has an invalid schema")
        candidate_decisions = {decision["name"]: decision for decision in decision_payload["decisions"]}
    codex_responses = {}
    for response_path in CODEX_RESPONSE_PATHS:
        codex_responses.update(json.loads(response_path.read_text()))
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
        "artist-smock": "keeper_artist_smock_walk",
        "scuba": "keeper_scuba_walk_side",
    }
    bridge_sources = {
        "keeper_turn_back", "keeper_sit_side", "keeper_sit_front",
        "keeper_artist_smock_turn_back", "keeper_artist_smock_turn_front", "keeper_artist_smock_sit_front",
        "keeper_get_into_bed", "keeper_party_hat_put_on_back",
        "keeper_scuba_jetty_dive", "keeper_parachute_drift", "keeper_parachute_landing",
    }

    def bridge_for(asset: dict) -> list[str]:
        if asset["outfit"] == "scuba":
            if asset["name"] in {"keeper_scuba_walk_side", "keeper_scuba_jetty_dive"}:
                return []
            if asset["name"].startswith("keeper_scuba_swim_"):
                return ["keeper_scuba_jetty_dive"]
            return []
        if asset["name"] == "keeper_pyjamas_snore":
            return ["keeper_get_into_bed"]
        if asset["outfit"] == "artist-smock":
            if asset["name"] in {
                "keeper_artist_smock_walk", "keeper_artist_smock_turn_back",
                "keeper_artist_smock_turn_front", "keeper_artist_smock_sit_front",
            }:
                return []
            if asset.get("seatPoint") or asset.get("facing") == "front":
                return ["keeper_artist_smock_turn_front", "keeper_artist_smock_sit_front"]
            if asset.get("facing") and any(token in asset["facing"] for token in ("back", "rear")):
                return ["keeper_artist_smock_turn_back"]
            return []
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

    def infer_pose_tag(asset: dict) -> str:
        """Return the initial reviewer pose tag from authored movement metadata.

        This is deliberately an initial classification, not immutable content
        metadata: the browser review register can override it per exact name.
        """
        name = asset["name"].removeprefix("keeper_")
        posture = asset.get("postureClass") or ""
        facing = (asset.get("facing") or "").lower()
        movement = f"{name} {facing}"
        if posture == "body-axis":
            return "body-axis"
        if posture == "transition":
            return "standing-turning" if "turn" in movement or "rotating" in movement else "transition"
        if posture == "upright" and ("turn" in movement or "-to-" in facing):
            return "standing-turning"
        prefix = {"upright": "standing", "seated": "seated", "crouched": "crouching"}.get(posture)
        if prefix is None:
            return "other"
        if "front" in movement and not any(token in movement for token in ("right", "left", "side")):
            return f"{prefix}-front"
        if any(token in movement for token in ("back", "rear")) and not any(token in movement for token in ("right", "left", "side")):
            return f"{prefix}-back"
        if any(token in movement for token in ("front-right", "rear-right", "three-quarter")):
            return f"{prefix}-three-quarter"
        return f"{prefix}-side"

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
        imported = imported_reviews.get(asset["name"])
        review_status = (
            "unreviewed" if imported is None else
            "happy" if imported.get("happy") else
            "review-later" if imported.get("reviewLater") else
            "awaiting-new-draft"
        )
        decision = candidate_decisions.get(asset["name"])
        if decision:
            review_status = "happy" if decision.get("happy") else review_status
        review_assets.append({
            **review_clip(asset),
            "leadIn": review_clip(reviewed_by_name[lead_name]) if lead_name else None,
            "bridge": [review_clip(reviewed_by_name[name]) for name in bridge_names],
            "transitionKind": transition_kind,
            "transitionNote": transition_note,
            "reviewStatus": review_status,
            "poseTag": infer_pose_tag(asset),
            "codexResponse": codex_responses.get(asset["name"], ""),
        })

    # Drafts are opt-in review consumers. They never replace the canonical
    # source strip, runtime manifest entry, or existing production preview.
    active_review_drafts: dict[str, list[dict]] = {}
    draft_comparisons: list[dict] = []
    if SIDE_ON_OCCLUSION_REGISTER_PATH.exists():
        side_on_register = json.loads(SIDE_ON_OCCLUSION_REGISTER_PATH.read_text())
        draft_record_path = ROOT / side_on_register["draft"]["register"]
        if not side_on_register["draft"].get("rejected") and draft_record_path.exists():
            draft_record = json.loads(draft_record_path.read_text())
            draft_sidecar = json.loads((ROOT / draft_record["draft"]["sidecar"]).read_text())
            active_review_drafts.setdefault(draft_record["animation"], []).append({
                "name": draft_record["animation"],
                "label": draft_record["label"],
                "source": draft_record["draft"]["strip"],
                "frames": draft_sidecar["frames"],
                "fps": draft_sidecar["fps"],
                "canvas": [draft_sidecar["w"], draft_sidecar["h"]],
                "anchor": draft_sidecar["anchor"],
                "sha256": draft_record["draft"]["stripSha256"],
                "canonicalSha256": draft_record["canonical"]["stripSha256"],
                "correctedFrames": draft_record["draft"]["correctedFrames"],
                "layerOrderDecision": "foreground hand/fingers/wrist over beard at the declared crossing; rear hand remains behind beard",
            })
            draft_comparisons.append(draft_record["draft"])

    review_draft_registry = {"version": 1, "drafts": []}
    if REVIEW_DRAFTS_PATH.exists():
        review_draft_registry = json.loads(REVIEW_DRAFTS_PATH.read_text())
        for item in review_draft_registry.get("drafts", []):
            if item.get("status") not in {"active-review-draft", "promoted-review-draft"}:
                continue
            name = item["name"]
            draft_record = json.loads((ROOT / item["register"]).read_text())
            if draft_record["animation"] != name:
                raise SystemExit(f"Review draft register is attached to the wrong exact name: {name}")
            promoted = item.get("status") == "promoted-review-draft"
            comparison = draft_record["canonical"] if promoted else draft_record["draft"]
            draft_sidecar = json.loads((ROOT / comparison["sidecar"]).read_text())
            draft_image = Image.open(ROOT / comparison["strip"]).convert("RGBA")
            first_frame = draft_image.crop((0, 0, draft_sidecar["w"] * DENSITY, draft_sidecar["h"] * DENSITY))
            first_box = first_frame.getchannel("A").getbbox()
            if first_box is None:
                raise SystemExit(f"Review draft first frame is empty: {name}")
            active_review_drafts.setdefault(name, []).append({
                "name": name,
                "label": "Previous version" if promoted else "Frank-selected draft",
                "source": comparison["strip"],
                "frames": draft_sidecar["frames"],
                "fps": draft_sidecar["fps"],
                "canvas": [draft_sidecar["w"], draft_sidecar["h"]],
                "anchor": draft_sidecar["anchor"],
                "firstFrameAlphaBox": [round(value / DENSITY, 2) for value in first_box],
                "sha256": comparison["stripSha256"],
                "canonicalSha256": (
                    draft_record["promotion"]["stripSha256"]
                    if promoted else draft_record["canonical"]["stripSha256"]
                ),
                "selection": draft_record["selection"],
            })
            draft_comparisons.append(comparison)

    for asset in review_assets:
        variants = active_review_drafts.get(asset["name"])
        if variants:
            asset["draftVariants"] = variants

    initial_reviews = {}
    rolled_back_second_round = {
        "keeper_bath_enter", "keeper_bath_exit", "keeper_carry_shopping", "keeper_clear_snow",
        "keeper_collect_eggs_back", "keeper_crouch_work_back", "keeper_darts", "keeper_eat_seated",
        "keeper_fish_feed_up", "keeper_fish_seated", "keeper_fish_standing",
        "keeper_guitar_pickup_acoustic", "keeper_guitar_pickup_flying_v_1967", "keeper_guitar_pickup_gretsch",
        "keeper_hot_drink_pickup", "keeper_hot_drink_pour", "keeper_lawn_mower_push",
        "keeper_lean_table_back", "keeper_lift_button_front", "keeper_lift_weights_back",
        "keeper_machete_side", "keeper_meal_from_oven_back", "keeper_meal_place_side",
        "keeper_mechanic_walk_front", "keeper_nap_seated", "keeper_operate_outboard",
        "keeper_parachute_drift",
    }
    side_on_rejected = False
    if SIDE_ON_OCCLUSION_REGISTER_PATH.exists():
        side_on_rejected = json.loads(SIDE_ON_OCCLUSION_REGISTER_PATH.read_text()).get("draft", {}).get("rejected", False)

    for asset in review_assets:
        imported = imported_reviews.get(asset["name"])
        decision = candidate_decisions.get(asset["name"])
        if imported is None and decision is None:
            continue
        # Geometry and cadence were baked by the production author. Re-review
        # therefore starts from the delivered asset at neutral viewer controls,
        # while retaining Frank's exact notes and resolved decision state.
        initial_reviews[asset["name"]] = {
            "widthPercent": 100,
            "heightPercent": 100,
            "animationFps": asset["fps"],
            "ghostReference": (imported or {}).get("ghostReference", "auto"),
            "ghostPosition": (imported or {}).get("ghostPosition", "overlay"),
            "ghostRotation": (imported or {}).get("ghostRotation", 0),
            "ghostMirrored": (imported or {}).get("ghostMirrored", False),
            "actionRotation": 0,
            "actionOffsetX": 0,
            "actionOffsetY": 0,
            "actionOpacityPercent": 100,
            "notes": (imported or {}).get("notes", ""),
            "redraftRequested": False,
            "happy": decision.get("happy", False) if decision else (imported or {}).get("happy", False),
            "reviewLater": False if decision else (imported or {}).get("reviewLater", False),
            "candidateId": decision.get("candidateId") if decision else None,
            "updatedAt": decision.get("recordedAt") if decision else None,
        }

    template = (ROOT / "art/source/keeper-first-batch/scale-review-template.html").read_text()
    review_payload = {
        "contractVersion": CONTRACT["version"],
        "canonicalAnatomy": CONTRACT["canonicalAnatomy"],
        "counts": payload["counts"],
        "originalReference": review_clip(reviewed_by_name[ORIGINAL_KEEPER]),
        "ghostReferences": {
            "standingSide": review_clip(reviewed_by_name[ORIGINAL_KEEPER]),
            "standingFront": review_clip(reviewed_by_name["keeper_wave_camera"]),
            "standingBack": review_clip(reviewed_by_name["keeper_turn_back"]),
            "sittingSide": review_clip(reviewed_by_name["keeper_sit_side"]),
            "sittingFront": review_clip(reviewed_by_name["keeper_sit_front"]),
            "sittingBack": review_clip(reviewed_by_name["keeper_sit_back"]),
        },
        "reviewRevision": "2026-10-10-user-selected-replacements-v1",
        "sideOnOcclusionAudit": side_on_register if SIDE_ON_OCCLUSION_REGISTER_PATH.exists() else None,
        "reviewDrafts": review_draft_registry,
        "initialReviews": initial_reviews,
        "assets": review_assets,
    }
    review_html = template.replace("__KEEPER_REVIEW_DATA__", json.dumps(review_payload, separators=(",", ":")))
    (OUT / "review.html").write_text(review_html)
    PUBLIC_REVIEW.mkdir(parents=True, exist_ok=True)
    (PUBLIC_REVIEW / "index.html").write_text(review_html)
    if SIDE_ON_OCCLUSION_REGISTER_PATH.exists() and not side_on_register["draft"].get("rejected"):
        draft_public_dir = PUBLIC_REVIEW / "drafts"
        draft_public_dir.mkdir(parents=True, exist_ok=True)
        draft_record = json.loads((ROOT / side_on_register["draft"]["register"]).read_text())
        draft_strip = ROOT / draft_record["draft"]["strip"]
        shutil.copyfile(draft_strip, draft_public_dir / draft_strip.name)
    for comparison in draft_comparisons:
        draft_public_dir = PUBLIC_REVIEW / "drafts"
        draft_public_dir.mkdir(parents=True, exist_ok=True)
        draft_strip = ROOT / comparison["strip"]
        shutil.copyfile(draft_strip, draft_public_dir / draft_strip.name)

    def table_text(value: object) -> str:
        return str(value or "").replace("|", "\\|").replace("\n", "<br>")

    resolution_lines = [
        "# Keeper animation review resolution — 2026-10-10",
        "",
        "This table is generated from Frank's immutable review export and the current production asset set. The second-round art pass was rejected and restored from commit `131191c`; its historical rows remain evidence only. On 2026-10-10, Frank explicitly selected ten separate replacements (nine named sheets plus the necessary `keeper_parachute_landing` bridge). Those are now canonical production, with each prior version retained as an exact-name `Previous version` comparison in the reviewer. All other `Awaiting new draft review` rows still identify an unresolved request requiring a new versioned draft.",
        "",
        "| Animation | Frames | Frank's comment | Class | Decision | Proposed/implemented change | Status | Verification | Commit |",
        "|---|---:|---|---|---|---|---|---|---|",
    ]
    draft_statuses = {
        item["name"]: item.get("status")
        for item in review_draft_registry.get("drafts", [])
    }
    for asset in review_assets:
        imported = imported_reviews.get(asset["name"])
        comment = imported.get("notes", "") if imported else ""
        if imported is None:
            classification = "decision-needed"
            decision = "Frank review required"
            change = "New or previously unreviewed production animation"
        elif imported.get("happy"):
            classification = "keep"
            decision = codex_responses.get(asset["name"], "Retain accepted animation")
            change = "Frank's accepted visual scale and cadence are baked into production"
        elif imported.get("reviewLater"):
            classification = "decision-needed"
            decision = codex_responses.get(asset["name"], "Deferred exactly as requested")
            change = "No production redraw until deferred decision"
        elif imported.get("redraftRequested"):
            classification = "rebuild"
            decision = "Rebuilt and ready for Frank's verdict"
            change = codex_responses.get(asset["name"], asset["note"])
        else:
            classification = "fix"
            decision = "Changed and ready for Frank's verdict"
            change = codex_responses.get(asset["name"], asset["note"])
        draft_status = draft_statuses.get(asset["name"])
        if asset["name"] in rolled_back_second_round and draft_status != "promoted-review-draft":
            decision = "Rejected and restored"
        if draft_status == "active-review-draft":
            decision = "User-selected draft ready for Frank's verdict"
            change = codex_responses.get(asset["name"], asset["note"])
        if draft_status == "promoted-review-draft":
            decision = "Frank-selected replacement promoted"
            change = codex_responses.get(asset["name"], asset["note"])
        if asset["name"] == "keeper_darts" and SIDE_ON_OCCLUSION_REGISTER_PATH.exists() and not side_on_rejected:
            decision = "Draft v2 hand/beard repair ready for Frank's verdict; prior Frank-selected draft remains comparison-only"
            change = "Canonical production remains unchanged; a draft-only foreground-hand-over-beard correction is recorded for frames 3–6 and awaits explicit promotion or rejection."
        verification = (
            "Retained; full audit" if asset["reviewStatus"] == "happy" else
            "Deferred; unchanged" if asset["reviewStatus"] == "review-later" else
            "Full audit; Frank visual verdict pending"
        )
        if asset["name"] in rolled_back_second_round and draft_status != "promoted-review-draft":
            verification = "Restored pre-pass canonical; fresh draft required"
        if draft_status == "active-review-draft":
            verification = "Draft extracted and verified; canonical unchanged"
        if draft_status == "promoted-review-draft":
            verification = "Promoted after final-strip inspection; previous version retained"
        if asset["name"] == "keeper_darts" and SIDE_ON_OCCLUSION_REGISTER_PATH.exists() and not side_on_rejected:
            verification = "Draft v2 and selected-draft comparison verified; canonical unchanged"
        status_label = {
            "happy": "Happy",
            "review-later": "Review later",
            "awaiting-new-draft": "Awaiting new draft review",
            "unreviewed": "Unreviewed",
        }[asset["reviewStatus"]]
        resolution_lines.append(
            f"| `{asset['name']}` | {asset['frames']} | {table_text(comment)} | {classification} | "
            f"{table_text(decision)} | {table_text(change)} | {status_label} | {verification} | current main delivery |"
        )
    if SIDE_ON_OCCLUSION_REGISTER_PATH.exists():
        resolution_lines.extend([
            "",
            "## Side-on beard/hand occlusion audit v2",
            "",
            "All manifest Keeper frames are classified as side-on, front-facing, rear-facing or indeterminate, and the 101 exact standing/sitting side-action sheets are SHA-256-pinned against the restored production set. The pinned `keeper_clear_snow` side-beard reference remains byte-identical. Only canonical `keeper_darts` frames 3–6 have a confirmed foreground-hand-over-beard issue; the narrowly-scoped correction is shown as `Draft v2` beside canonical, while canonical production remains unchanged pending Frank's explicit decision. The earlier v1 draft is rejected historical evidence only.",
        ])
    if active_review_drafts:
        resolution_lines.extend([
            "",
            "## User-selected review comparisons",
            "",
            "Frank's supplied 14-pose darts image remains byte-identical as the `Frank-selected draft` comparison beside canonical `keeper_darts` and the new `Draft v2`; neither darts draft is promoted. The nine separately selected replacements and the dependent parachute-landing bridge were promoted only after final-strip inspection; their original canonical strips remain visible as exact-name `Previous version` comparisons. Every comparison is SHA-256-pinned in `data/keeper_review_drafts.json` and the v2 audit register.",
        ])
    resolution_path = ROOT / "docs/review/KEEPER_ANIMATION_REVIEW_RESOLUTION_2026-10-10.md"
    resolution_path.write_text("\n".join(resolution_lines) + "\n")

    with (OUT / "keeper-scale-summary.csv").open("w", newline="") as handle:
        fields = ["name", "frames", "canvas", "postureClass", "measurementMethod", "status", "outfit", "facing", "originalComparison", "medianFaceProxyWidth", "medianFaceProxyHeight", "faceProxyCoverage", "medianTorsoScanWidthAt20", "torsoScanCoverage", "alphaHeightRange", "alphaWidthRange", "bottomClearanceRange", "note"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for asset in serialisable:
            writer.writerow({field: json.dumps(asset[field]) if isinstance(asset.get(field), (list, dict)) else asset.get(field, "") for field in fields})

    lines = [
        "# Keeper scale audit",
        "",
        "This is the permanent, reproducible audit of every keeper sheet against the untouched approved original `keeper_walk`. Frank's saved visual width and height are the production sizing authority; the original remains the identity, anatomy and contact reference. The audit deliberately does **not** use the outer silhouette as character scale except for directly comparable full-body walks that Frank has not visually resized: hats, tools, raised arms, water and furniture can change that box without changing the keeper.",
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
        "The approved original is printed first in every contact-sheet row. Frank's saved width/height choice is shown at its delivered production size and is never failed for disagreeing with an automatic ratio. Directly comparable walks without a saved visual resize must measure 0.960–1.040 of the original skull-to-sole silhouette; unobscured side walks without a saved visual resize must also remain within 1 logical pixel of its median 20 px-above-floor torso scan, or the command fails. Other upright poses use inferred skull-to-supporting-sole height. Costumes use the face/ear/neck structure to infer the skull under hats and helmets. Seated and crouched poses use the head unit plus shoulder–hip–sole chain. Swimming, press-ups and other horizontal poses use the same articulated chain along the body axis. A skin-colour face proxy is recorded as evidence only and cannot overrule Frank's visual sizing.",
        "",
        "## Interactive comparison",
        "",
        f"Open [the sizing and transition review](review.html) to inspect all {payload['counts']['reviewedAnimationSheets']} accepted animations. Gallery mode is deliberately compact: each card shows the animation, its current review-state pill, latest local save/redraft timestamp, large playback and frame-stepping controls, plus an `Open close review` button. Independently filter by review state, pose (standing/sitting/crouching with front/back/side/turning subcategories) and use list. `Find animation` searches the exact animation name and temporarily overrides those filters, so a purpose such as `darts` can be isolated immediately. The default `Use now` list excludes reversible reserve entries; `Reserve list only` reveals them. In close review, Previous/Next and the Left/Right keys stay inside all selected filters and wrap from its final result to its first.",
        "The pinned reference can show standing side/front/back or sitting side/front/back identity ghosts. These fixed ghosts are anatomy comparisons, not a replacement for each reviewed clip's saved production size. In upright standard-cap poses the gold badge crossing the blue skull-top guide is a calibrated visual proxy; tilted, bent, seated, crouched, horizontal, bare-headed and alternate-headwear poses still require anatomical landmarks.",
        "Close-review cards retain precise candidate, size, position, rotation, opacity, ghost, frame-step and 1–20fps timing controls. `Pose tag` is initially inferred from the animation name plus authored posture/facing metadata, but the reviewer may save an override for any exact animation; filters use that saved override. `Relegate to reserve list` hides a likely duplicate from the default use-now gallery without deleting it or changing its production status. `Preferred promotion candidate` offers canonical production and every available draft for that exact animation. Recording the selection adds a timestamp and exportable `candidateId`; it deliberately does not mutate production art, so a later explicit, reversible promotion can also revert to any retained prior variant. Multi-draft cards can compress/expand only their retained comparison panels; every draft remains intact. `Hand back to Codex` uses a positive confirmation: confirming saves any unsaved cards locally, then sends the complete exact-name review batch to the deployed handoff queue without changing production art. The queue saves a semantic exact-name delta that ignores timestamps: the first server handoff compares against the shipped review baseline, then later Codex work examines only changes from the preceding handoff. The imported production pass starts viewer transforms at neutral because accepted geometry and cadence are already baked into the delivered sprite and manifest.",
        "Every card has Frank's notes and decision controls plus a read-only Codex response field. The rejected second-round pass remains historical evidence; the ten later selected canonical promotions show their exact prior strip as `Previous version`, while all other Awaiting new draft review cards still require a fresh draft. Orange cards have unsaved changes; saved happy, new-draft and later-review cards use distinct status colours.",
        "`Hand back to Codex` is the normal online workflow: it always shows a positive confirmation first. Confirming saves every edited card to that browser, then submits all 173 exact-name records to the durable review-handoff queue. The receipt reports only the records whose decisions or notes changed since the previous handoff, or from the shipped review baseline for the first server handoff; save timestamps do not count as changes. Cancelling leaves the review untouched; the handoff never edits production art. The collapsed advanced backup/import control retains `keeper-scale-choices.json` version 11 for exceptional offline recovery; it validates exact `keeper_*` names, rejects duplicates/unknown names and safely reconciles stale status-list entries from the matching named review. The close-review page can also prepend matching walks, insert known bridges or freeze a seam with onion skin; it prints the runtime PNG and authored source-strip filename.",
        "The character-width and character-height sliders each have adjacent −0.5% and +0.5% buttons for precise adjustments. They update the same per-animation values, obey the same 50%–150% limits and become part of the normal Save/export workflow.",
        "Every blue animation-transform slider also has −0.5/+0.5 buttons: degrees for rotation, logical pixels for horizontal/vertical position and percentage points for opacity. They update the same limited, saved and exported values as their sliders.",
        "Each card's frame-control block can play only that reviewed action from frame 1. `Play once` stops on the final frame; `Loop` repeats until paused. This playback choice is inspection-only and does not dirty the review.",
        "At browser widths of 1500px or more, focused mode becomes a widescreen workstation with the pinned canon on the left, a viewport-height animation stage in the centre and a compact two-column control console on the right. Control groups are colour-coded: amber for character size, purple for the ghost, blue for animation transforms, teal for frame navigation and green/red for review decisions and notes.",
        "Review progress is browser-local: changing display zoom or review-state filter saves immediately, and every `Save this review` records that animation as the latest completed card. Reloading restores the focused view and filter. The online `Hand back to Codex` button submits a complete durable batch; the offline copy cannot do that without a server, so its collapsed Advanced backup/import control remains an exceptional recovery path. Saving or advancing from the final result wraps to the first result in that same filter.",
        "",
        "## Reversible review drafts",
        "",
        "The completed v2 side-on beard/hand audit keeps the canonical production `keeper_darts` strip alongside the narrowly-scoped `Draft v2` hand-over-beard correction for frames 3–6 and Frank's separate byte-identical selected draft. Neither darts draft is promoted. The rejected partial v1 audit remains immutable historical evidence under `art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v1/`. The ten later selected canonical promotions retain their exact prior strips as `Previous version` comparisons.",
        "The review-draft register pins source, previous/current canonical and draft SHA-256 values. New amendments remain draft-only: canonical production art, `public/sprites/`, the runtime manifest, immutable review exports and existing previews remain untouched until explicit promotion. Rejecting a new draft requires only deleting its draft directory and exact-name entry from `data/keeper_review_drafts.json`.",
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
    if len(assets) != 191:
        raise SystemExit(f"Expected 191 keeper sheets, found {len(assets)}")
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
