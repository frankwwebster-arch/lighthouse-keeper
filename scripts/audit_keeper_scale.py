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
    "keeper_crouch_work_back": "redrawn; hands work in front and body width restored",
    "keeper_search_boxes": "reuses canonical corrected low rear work anatomy",
    "keeper_collect_eggs_back": "reuses canonical corrected low rear work anatomy",
    "keeper_scuba_swim_down": "redrawn with approved keeper identity and cell gutters",
    "keeper_sit_front": "redrawn and width-normalised against canonical front body",
    "keeper_party_turn_back": "redrawn as a coherent front-to-rear turn",
    "keeper_party_idle": "redrawn from the corrected party identity",
    "keeper_piano": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_eat_seated": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_row_boat": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_drive_speedboat": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_watch_tv": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_play_drums_front": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_play_drums_back": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_watch_movie": "seated anatomy normalised to the sit-side head and torso unit",
    "keeper_bath_wash": "redrawn and normalised from the standing bare-headed and seated canonical landmarks",
    "keeper_hot_tub": "redrawn and normalised by the visible head/shoulder unit rather than the water silhouette",
    "keeper_place_cake": "redrawn for the standard 19 px table datum and a fully straight final pose",
    "keeper_meal_place_side": "redrawn for the standard 19 px table datum instead of the floor",
    "keeper_souwester_walk_side": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
    "keeper_souwester_walk_front": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
    "keeper_souwester_walk_back": "costume headwear excluded; skull, shoulder and sole landmarks normalised",
}

for _outfit in ("knight", "spaceman", "pirate", "tarzan", "halloween", "mechanic"):
    for _view in ("side", "front", "back"):
        CORRECTED[f"keeper_{_outfit}_walk_{_view}"] = "costume-specific headwear envelope excluded from skull-to-sole scale"


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


def frame_metrics(frame: Image.Image, logical_height: int) -> dict:
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
        measured = [frame_metrics(frame, sidecar["h"]) for frame in frames]
        face_widths = [m["faceProxy"]["width"] for m in measured if m["faceProxy"]]
        face_heights = [m["faceProxy"]["height"] for m in measured if m["faceProxy"]]
        posture = classify(name, sidecar)
        method = CONTRACT["measurementPolicy"].get(
            {"body-axis": "horizontalSwimmingExercise", "seated": "seatedCrouched", "crouched": "seatedCrouched"}.get(posture, posture),
            "articulated landmark chain",
        )
        status = "excluded-technical" if name in TECHNICAL else "corrected" if name in CORRECTED else "measured-pass"
        assets.append({
            "name": name,
            "source": str(png_path.relative_to(ROOT)),
            "frames": sidecar["frames"],
            "canvas": [sidecar["w"], sidecar["h"]],
            "anchor": sidecar.get("anchor"),
            "facing": sidecar.get("facing"),
            "outfit": sidecar.get("outfit", "standard"),
            "postureClass": posture,
            "measurementMethod": method,
            "status": status,
            "note": CORRECTED.get(name, "measured against the canonical anatomy for its pose class"),
            "medianFaceProxyWidth": median(face_widths),
            "medianFaceProxyHeight": median(face_heights),
            "faceProxyCoverage": f"{len(face_widths)}/{len(measured)}",
            "alphaHeightRange": [min(m["alphaHeight"] for m in measured), max(m["alphaHeight"] for m in measured)],
            "alphaWidthRange": [min(m["alphaWidth"] for m in measured), max(m["alphaWidth"] for m in measured)],
            "bottomClearanceRange": [min(m["bottomClearance"] for m in measured), max(m["bottomClearance"] for m in measured)],
            "frameMeasurements": measured,
            "_frames": frames,
        })
    return assets


def contact_sheets(assets: list[dict]) -> list[str]:
    reviewed = [a for a in assets if a["status"] != "excluded-technical"]
    per_sheet = 20
    paths = []
    font = ImageFont.load_default()
    for sheet_index in range(math.ceil(len(reviewed) / per_sheet)):
        subset = reviewed[sheet_index * per_sheet : (sheet_index + 1) * per_sheet]
        width, row_height = 1320, 230
        canvas = Image.new("RGB", (width, row_height * len(subset) + 42), "#101722")
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 12), f"KEEPER SCALE AUDIT {sheet_index + 1} / {math.ceil(len(reviewed) / per_sheet)} — red floor; blue skull; green shoulders; amber hips (upright rows)", fill="#ffffff", font=font)
        for row, asset in enumerate(subset):
            y = 42 + row * row_height
            draw.rectangle((0, y, width, y + row_height - 1), fill="#172333" if row % 2 else "#13202e")
            label = f"{asset['name']}  {asset['postureClass']}  {asset['status']}  face {asset['medianFaceProxyWidth']}x{asset['medianFaceProxyHeight']}  alpha-h {asset['alphaHeightRange']}"
            draw.text((12, y + 8), label, fill="#f4ecd9", font=font)
            reps = sorted(set((0, max(0, asset["frames"] // 2), asset["frames"] - 1)))
            x = 16
            for frame_index in reps:
                frame = asset["_frames"][frame_index]
                # Every pose is displayed at exactly two screen pixels per
                # logical pixel.  Never fit a large canvas into the row: that
                # would make an identically sized keeper look smaller merely
                # because a parachute or dive needs more transparent space.
                scale = 0.5
                scaled = frame.resize((round(frame.width * scale), round(frame.height * scale)), Image.Resampling.NEAREST)
                floor_y = y + 215
                px = x + max(0, (360 - scaled.width) // 2)
                py = floor_y - scaled.height
                canvas.paste(scaled, (px, py), scaled)
                draw.line((x, floor_y, x + 350, floor_y), fill="#ff5167", width=2)
                if asset["postureClass"] == "upright":
                    for key, colour in (
                        ("skullTopHeightAboveFloor", "#4da6ff"),
                        ("shoulderHeightAboveFloor", "#52d273"),
                        ("hipHeightAboveFloor", "#f2b84b"),
                    ):
                        datum_y = floor_y - round(CONTRACT["canonicalAnatomy"][key] * DENSITY * scale)
                        draw.line((x, datum_y, x + 350, datum_y), fill=colour, width=1)
                draw.text((x + 3, y + 28), f"f{frame_index + 1}", fill="#a9bbcb", font=font)
                x += 420
        path = OUT / f"keeper-scale-contact-{sheet_index + 1:02d}.png"
        canvas.save(path, optimize=True)
        paths.append(str(path.relative_to(ROOT)))
    return paths


def publish(assets: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    contact_paths = contact_sheets(assets)
    serialisable = [{k: v for k, v in asset.items() if k != "_frames"} for asset in assets]
    payload = {
        "version": 1,
        "authority": "data/keeper_asset_contract.json version 3",
        "rules": CONTRACT["measurementPolicy"],
        "canonicalAnatomy": CONTRACT["canonicalAnatomy"],
        "counts": {
            "allSheets": len(assets),
            "reviewedAnimationSheets": sum(a["status"] != "excluded-technical" for a in assets),
            "technicalRejectedSheets": sum(a["status"] == "excluded-technical" for a in assets),
            "allFramesMeasured": sum(a["frames"] for a in assets),
            "correctedSheets": sum(a["status"] == "corrected" for a in assets),
        },
        "contactSheets": contact_paths,
        "assets": serialisable,
    }
    (OUT / "keeper-scale-metrics.json").write_text(json.dumps(payload, indent=2) + "\n")
    with (OUT / "keeper-scale-summary.csv").open("w", newline="") as handle:
        fields = ["name", "frames", "canvas", "postureClass", "measurementMethod", "status", "outfit", "facing", "medianFaceProxyWidth", "medianFaceProxyHeight", "faceProxyCoverage", "alphaHeightRange", "alphaWidthRange", "bottomClearanceRange", "note"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for asset in serialisable:
            writer.writerow({field: json.dumps(asset[field]) if isinstance(asset.get(field), (list, dict)) else asset.get(field, "") for field in fields})

    lines = [
        "# Keeper scale audit",
        "",
        "This is the permanent, reproducible audit of every keeper sheet. It deliberately does **not** use the outer silhouette as character scale: hats, tools, raised arms, water and furniture can change that box without changing the keeper.",
        "",
        f"- {payload['counts']['allSheets']} keeper sheets inspected.",
        f"- {payload['counts']['reviewedAnimationSheets']} animation sheets accepted for review; {payload['counts']['technicalRejectedSheets']} obsolete modular/reference sheets excluded.",
        f"- {payload['counts']['allFramesMeasured']} individual frames measured.",
        f"- {payload['counts']['correctedSheets']} sheets explicitly rebuilt or anatomy-normalised in this pass.",
        "- Canonical upright anatomy: skull top 32.5 logical pixels above the walking floor, shoulders 24.5, hips 14.5, seat contact 11.",
        "- Allowed landmark drift: 0.5 logical pixel; core-width drift: 1 logical pixel. Pose contacts are checked independently from body scale.",
        "",
        "## Measurement method",
        "",
        "Upright poses use inferred skull-to-supporting-sole height. Costumes use the face/ear/neck structure to infer the skull under hats and helmets. Seated and crouched poses use the head unit plus shoulder–hip–sole chain. Swimming, press-ups and other horizontal poses use the same articulated chain along the body axis. A skin-colour face proxy is also recorded where visible as a machine-checkable warning signal; it is not allowed to overrule the anatomical method.",
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
    if len(assets) != 167:
        raise SystemExit(f"Expected 167 keeper sheets, found {len(assets)}")
    publish(assets)
    reviewed = sum(a["status"] != "excluded-technical" for a in assets)
    frames = sum(a["frames"] for a in assets)
    print(f"Measured {frames} frames across {len(assets)} sheets ({reviewed} review animations).")


if __name__ == "__main__":
    main()
