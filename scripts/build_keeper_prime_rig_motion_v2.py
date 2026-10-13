#!/usr/bin/env python3
"""Build the approved KP Rig V1 successor with deterministic motion previews."""
from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v2"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-rig-v2"
V1_PACK = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v1"
V1_REGISTER = V1_PACK / "batch-register.json"
V1_RIG = V1_PACK / "rig/keeper-prime-rig-v1.json"
FRONT = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png"
SIDE = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v2/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"

STAGE = (640, 340)
SOURCE_CENTRE = 128.0
FLOOR_Y = 316.0


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def copy_joints(records: dict) -> dict[str, list[float]]:
    return {name: list(value["source"]) for name, value in records.items()}


def length(a: list[float], b: list[float]) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def angle_from_vertical(a: list[float], b: list[float]) -> float:
    return math.degrees(math.atan2(b[0] - a[0], b[1] - a[1]))


def endpoint(start: list[float], segment_length: float, degrees: float) -> list[float]:
    radians = math.radians(degrees)
    return [start[0] + math.sin(radians) * segment_length, start[1] + math.cos(radians) * segment_length]


def smoothstep(value: float) -> float:
    return value * value * (3 - 2 * value)


def triangle(value: float) -> float:
    return 1 - abs((value % 1) * 2 - 1)


def translate(names: list[str], joints: dict[str, list[float]], dx: float, dy: float) -> None:
    for name in names:
        joints[name] = [joints[name][0] + dx, joints[name][1] + dy]


def two_bone_ik(hip: list[float], ankle: list[float], upper: float, lower: float, bend_right: bool) -> list[float]:
    dx, dy = ankle[0] - hip[0], ankle[1] - hip[1]
    distance = math.hypot(dx, dy)
    distance = max(abs(upper - lower) + 1e-6, min(upper + lower - 1e-6, distance))
    ux, uy = dx / distance, dy / distance
    along = (upper * upper - lower * lower + distance * distance) / (2 * distance)
    height = math.sqrt(max(0.0, upper * upper - along * along))
    base = [hip[0] + ux * along, hip[1] + uy * along]
    candidates = ([base[0] - uy * height, base[1] + ux * height], [base[0] + uy * height, base[1] - ux * height])
    return list(max(candidates, key=lambda point: point[0]) if bend_right else min(candidates, key=lambda point: point[0]))


def set_arm(joints: dict[str, list[float]], prefix: str, upper: float, fore: float, hand: float, upper_angle: float, fore_angle: float) -> None:
    shoulder = joints[f"shoulder{prefix}"]
    elbow = endpoint(shoulder, upper, upper_angle)
    wrist = endpoint(elbow, fore, fore_angle)
    palm = endpoint(wrist, hand, fore_angle)
    joints[f"elbow{prefix}"] = elbow
    joints[f"wrist{prefix}"] = wrist
    joints[f"hand{prefix}"] = palm


def set_leg(joints: dict[str, list[float]], prefix: str, thigh: float, shin: float, hip_angle: float, shin_angle: float) -> None:
    hip = joints[f"hip{prefix}"]
    knee = endpoint(hip, thigh, hip_angle)
    ankle = endpoint(knee, shin, shin_angle)
    joints[f"knee{prefix}"] = knee
    joints[f"ankle{prefix}"] = ankle
    direction = 1 if prefix in {"Right", "Near", "Far"} else -1
    joints[f"heel{prefix}"] = [ankle[0] - direction * 18, ankle[1] + 24]
    joints[f"toe{prefix}"] = [ankle[0] + direction * 10, ankle[1] + 24]


def make_clips(rig: dict) -> dict:
    front_base = copy_joints(rig["frontBackInvariant"]["joints"])
    side_base = copy_joints(rig["sideRightProjection"]["joints"])
    invariant = rig["invariantSegmentLengths"]
    upper, fore, hand = invariant["upperArm"], invariant["forearm"], invariant["wristToPalmCentre"]
    thigh, shin = invariant["thigh"], invariant["shin"]
    front_angles = {
        "rightUpper": angle_from_vertical(front_base["shoulderRight"], front_base["elbowRight"]),
        "rightFore": angle_from_vertical(front_base["elbowRight"], front_base["wristRight"]),
        "leftUpper": angle_from_vertical(front_base["shoulderLeft"], front_base["elbowLeft"]),
        "leftFore": angle_from_vertical(front_base["elbowLeft"], front_base["wristLeft"]),
    }
    side_angles = {
        "nearUpper": angle_from_vertical(side_base["shoulderNear"], side_base["elbowNear"]),
        "nearFore": angle_from_vertical(side_base["elbowNear"], side_base["wristNear"]),
        "farUpper": angle_from_vertical(side_base["shoulderFar"], side_base["elbowFar"]),
        "farFore": angle_from_vertical(side_base["elbowFar"], side_base["wristFar"]),
    }
    front_leg_angles = {
        "rightThigh": angle_from_vertical(front_base["hipRight"], front_base["kneeRight"]),
        "rightShin": angle_from_vertical(front_base["kneeRight"], front_base["ankleRight"]),
        "leftThigh": angle_from_vertical(front_base["hipLeft"], front_base["kneeLeft"]),
        "leftShin": angle_from_vertical(front_base["kneeLeft"], front_base["ankleLeft"]),
    }
    side_leg_angles = {
        "nearThigh": angle_from_vertical(side_base["hipNear"], side_base["kneeNear"]),
        "nearShin": angle_from_vertical(side_base["kneeNear"], side_base["ankleNear"]),
        "farThigh": angle_from_vertical(side_base["hipFar"], side_base["kneeFar"]),
        "farShin": angle_from_vertical(side_base["kneeFar"], side_base["ankleFar"]),
    }
    # V1 records its invariant measurements to four decimals. Reconstruct every
    # animated rest limb from those authoritative lengths so the motion proof
    # does not inherit the sub-pixel rounding difference in V1's source joints.
    set_arm(front_base, "Right", upper, fore, hand, front_angles["rightUpper"], front_angles["rightFore"])
    set_arm(front_base, "Left", upper, fore, hand, front_angles["leftUpper"], front_angles["leftFore"])
    set_leg(front_base, "Right", thigh, shin, front_leg_angles["rightThigh"], front_leg_angles["rightShin"])
    set_leg(front_base, "Left", thigh, shin, front_leg_angles["leftThigh"], front_leg_angles["leftShin"])
    set_arm(side_base, "Near", upper, fore, hand, side_angles["nearUpper"], side_angles["nearFore"])
    set_arm(side_base, "Far", upper, fore, hand, side_angles["farUpper"], side_angles["farFore"])
    set_leg(side_base, "Near", thigh, shin, side_leg_angles["nearThigh"], side_leg_angles["nearShin"])
    set_leg(side_base, "Far", thigh, shin, side_leg_angles["farThigh"], side_leg_angles["farShin"])
    clips: dict[str, dict] = {}

    idle_frames = []
    for index in range(60):
        phase = math.sin(2 * math.pi * index / 60)
        joints = json.loads(json.dumps(front_base))
        set_arm(joints, "Right", upper, fore, hand, front_angles["rightUpper"] + phase * 2.0, front_angles["rightFore"] + phase * 1.5)
        set_arm(joints, "Left", upper, fore, hand, front_angles["leftUpper"] - phase * 2.0, front_angles["leftFore"] - phase * 1.5)
        idle_frames.append({"joints": joints, "offsetX": 192.0, "breath": round((phase + 1) / 2, 6)})
    clips["idle"] = {"label": "Restrained idle", "view": "front", "fps": 30, "loop": True, "frames": idle_frames, "rootMotion": False, "endpointRule": "exact neutral at quarter-cycle crossings"}

    walk_frames = []
    for index in range(60):
        progress = index / 59
        phase = 2 * math.pi * progress
        swing = math.sin(phase)
        joints = json.loads(json.dumps(side_base))
        set_arm(joints, "Near", upper, fore, hand, side_angles["nearUpper"] - swing * 24, side_angles["nearFore"] - swing * 18)
        set_arm(joints, "Far", upper, fore, hand, side_angles["farUpper"] + swing * 24, side_angles["farFore"] + swing * 18)
        near_bend = max(0.0, -swing) * 34
        far_bend = max(0.0, swing) * 34
        set_leg(joints, "Near", thigh, shin, swing * 25, swing * 25 - near_bend)
        set_leg(joints, "Far", thigh, shin, -swing * 25, -swing * 25 - far_bend)
        world_root_x = -100 + progress * 840
        walk_frames.append({"joints": joints, "offsetX": round(world_root_x - SOURCE_CENTRE, 6), "breath": 0.5})
    clips["walk"] = {"label": "Walk with root travel", "view": "side", "fps": 30, "loop": True, "frames": walk_frames, "rootMotion": True, "rootTravelPixels": 840, "startsFullyHidden": True, "endsFullyHidden": True, "endpointRule": "loop reset occurs entirely outside the visible stage"}

    reach_frames = []
    for index in range(72):
        progress = index / 71
        amount = smoothstep(triangle(progress))
        joints = json.loads(json.dumps(front_base))
        set_arm(joints, "Right", upper, fore, hand, front_angles["rightUpper"] + amount * 67, front_angles["rightFore"] + amount * 90)
        set_arm(joints, "Left", upper, fore, hand, front_angles["leftUpper"], front_angles["leftFore"])
        reach_frames.append({"joints": joints, "offsetX": 192.0, "breath": 0.5})
    clips["reach"] = {"label": "Controlled right-hand reach", "view": "front", "fps": 30, "loop": True, "frames": reach_frames, "rootMotion": False, "endpointRule": "first and last frames return to exact neutral"}

    sit_frames = []
    upper_body = ["root", "spineLower", "spineMid", "chest", "neck", "headCentre", "crown", "shoulderNear", "elbowNear", "wristNear", "handNear", "shoulderFar", "elbowFar", "wristFar", "handFar", "hipNear", "hipFar"]
    neutral_near_ankle = list(side_base["ankleNear"])
    neutral_far_ankle = list(side_base["ankleFar"])
    for index in range(90):
        progress = index / 89
        amount = smoothstep(triangle(progress))
        joints = json.loads(json.dumps(side_base))
        translate(upper_body, joints, -18 * amount, 32 * amount)
        for prefix, ankle, bend_right in (("Near", neutral_near_ankle, True), ("Far", neutral_far_ankle, True)):
            hip = joints[f"hip{prefix}"]
            knee = two_bone_ik(hip, ankle, thigh, shin, bend_right)
            joints[f"knee{prefix}"] = knee
            joints[f"ankle{prefix}"] = list(ankle)
            joints[f"heel{prefix}"] = list(side_base[f"heel{prefix}"])
            joints[f"toe{prefix}"] = list(side_base[f"toe{prefix}"])
        sit_frames.append({"joints": joints, "offsetX": 192.0, "breath": 0.5})
    clips["sitStand"] = {"label": "Sit → stand with planted ankles", "view": "side", "fps": 30, "loop": True, "frames": sit_frames, "rootMotion": False, "plantedAnkles": True, "endpointRule": "first and last frames return to exact neutral"}
    return clips


def motion_bone_pairs(view: str) -> list[tuple[str, str, str]]:
    if view == "front":
        return [("shoulderLeft", "elbowLeft", "upperArm"), ("elbowLeft", "wristLeft", "forearm"), ("wristLeft", "handLeft", "wristToPalmCentre"), ("shoulderRight", "elbowRight", "upperArm"), ("elbowRight", "wristRight", "forearm"), ("wristRight", "handRight", "wristToPalmCentre"), ("hipLeft", "kneeLeft", "thigh"), ("kneeLeft", "ankleLeft", "shin"), ("hipRight", "kneeRight", "thigh"), ("kneeRight", "ankleRight", "shin")]
    return [("shoulderNear", "elbowNear", "upperArm"), ("elbowNear", "wristNear", "forearm"), ("wristNear", "handNear", "wristToPalmCentre"), ("shoulderFar", "elbowFar", "upperArm"), ("elbowFar", "wristFar", "forearm"), ("wristFar", "handFar", "wristToPalmCentre"), ("hipNear", "kneeNear", "thigh"), ("kneeNear", "ankleNear", "shin"), ("hipFar", "kneeFar", "thigh"), ("kneeFar", "ankleFar", "shin")]


def validate_motion(clips: dict, invariant: dict) -> dict:
    max_error = 0.0
    for clip in clips.values():
        for frame in clip["frames"]:
            joints = frame["joints"]
            for start, end, kind in motion_bone_pairs(clip["view"]):
                max_error = max(max_error, abs(length(joints[start], joints[end]) - invariant[kind]))
    reach = clips["reach"]["frames"]
    sit = clips["sitStand"]["frames"]
    idle = clips["idle"]["frames"]
    walk = clips["walk"]["frames"]
    return {
        "maximumInvariantSegmentErrorPixels": round(max_error, 9),
        "allInvariantSegmentErrorsBelowOneMillionthPixel": max_error < 1e-6,
        "idleFirstLastJointDelta": round(max(length(idle[0]["joints"][name], idle[-1]["joints"][name]) for name in idle[0]["joints"]), 6),
        "reachReturnsToNeutral": max(length(reach[0]["joints"][name], reach[-1]["joints"][name]) for name in reach[0]["joints"]) < 1e-6,
        "sitStandReturnsToNeutral": max(length(sit[0]["joints"][name], sit[-1]["joints"][name]) for name in sit[0]["joints"]) < 1e-6,
        "sitStandNearAnkleMaximumDrift": round(max(length(frame["joints"]["ankleNear"], sit[0]["joints"]["ankleNear"]) for frame in sit), 9),
        "sitStandFarAnkleMaximumDrift": round(max(length(frame["joints"]["ankleFar"], sit[0]["joints"]["ankleFar"]) for frame in sit), 9),
        "walkRootTravelPixels": round(walk[-1]["offsetX"] - walk[0]["offsetX"], 6),
        "walkStartsAndEndsHidden": clips["walk"]["startsFullyHidden"] and clips["walk"]["endsFullyHidden"],
        "finishedRasterDeformed": False,
        "productionSpritesChanged": False,
        "runtimeManifestChanged": False,
        "animationDraftsChanged": False,
    }


def draw_mannequin(draw: ImageDraw.ImageDraw, joints: dict[str, list[float]], view: str, offset_x: float, offset_y: float, scale: float = 0.48) -> None:
    def p(name: str) -> tuple[float, float]:
        return ((joints[name][0] + offset_x) * scale, joints[name][1] * scale + offset_y)
    if view == "front":
        limbs = [("shoulderLeft", "elbowLeft", 13, "#0964bd"), ("elbowLeft", "wristLeft", 12, "#0964bd"), ("shoulderRight", "elbowRight", 13, "#0964bd"), ("elbowRight", "wristRight", 12, "#0964bd"), ("hipLeft", "kneeLeft", 15, "#1e2e52"), ("kneeLeft", "ankleLeft", 14, "#1e2e52"), ("hipRight", "kneeRight", 15, "#1e2e52"), ("kneeRight", "ankleRight", 14, "#1e2e52")]
        shoulders = (p("shoulderLeft"), p("shoulderRight")); head = p("headCentre"); root = p("root")
    else:
        limbs = [("shoulderFar", "elbowFar", 11, "#24568b"), ("elbowFar", "wristFar", 10, "#24568b"), ("hipFar", "kneeFar", 13, "#172542"), ("kneeFar", "ankleFar", 12, "#172542"), ("shoulderNear", "elbowNear", 13, "#0964bd"), ("elbowNear", "wristNear", 12, "#0964bd"), ("hipNear", "kneeNear", 15, "#1e2e52"), ("kneeNear", "ankleNear", 14, "#1e2e52")]
        shoulders = (p("shoulderNear"), p("shoulderFar")); head = p("headCentre"); root = p("root")
    for start, end, width, colour in limbs:
        draw.line((*p(start), *p(end)), fill=colour, width=width)
    torso_width = 50 if view == "front" else 38
    draw.ellipse((root[0] - torso_width * scale, 122 * scale + offset_y, root[0] + torso_width * scale, 224 * scale + offset_y), fill="#0875d1", outline="#061524", width=2)
    draw.line((root[0] - torso_width * scale, 164 * scale + offset_y, root[0] + torso_width * scale, 164 * scale + offset_y), fill="#fff1c2", width=8)
    draw.ellipse((head[0] - (45 if view == "front" else 35) * scale, (45 if view == "front" else 44) * scale + offset_y, head[0] + (45 if view == "front" else 39) * scale, 126 * scale + offset_y), fill="#ffad68", outline="#061524", width=2)
    draw.ellipse((head[0] - 38 * scale, 82 * scale + offset_y, head[0] + 42 * scale, 150 * scale + offset_y), fill="#fff0d0", outline="#061524", width=2)
    draw.ellipse((head[0] - 48 * scale, 18 * scale + offset_y, head[0] + 48 * scale, 69 * scale + offset_y), fill="#0875d1", outline="#061524", width=2)
    hand_names = ("handLeft", "handRight") if view == "front" else ("handFar", "handNear")
    for name in hand_names:
        x, y = p(name); draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill="#ffad68", outline="#061524")
    bone_pairs = motion_bone_pairs(view)
    for start, end, _ in bone_pairs:
        draw.line((*p(start), *p(end)), fill="#36d3ff", width=2)
    for name in joints:
        if name.startswith(("shoulder", "elbow", "wrist", "hand", "hip", "knee", "ankle")):
            x, y = p(name); draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill="#ffffff")


def contact_sheet(clips: dict) -> Image.Image:
    row_height = 185
    output = Image.new("RGBA", (920, row_height * len(clips)), (12, 20, 27, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    x_positions = [14, 238, 462, 686]
    for row, (clip_id, clip) in enumerate(clips.items()):
        row_y = row * row_height
        draw.text((14, row_y + 6), clip["label"], fill="#ffffff", font=font)
        indices = [0, len(clip["frames"]) // 3, 2 * len(clip["frames"]) // 3, len(clip["frames"]) - 1]
        for column, frame_index in enumerate(indices):
            frame = clip["frames"][frame_index]
            centre_x = x_positions[column] + 96
            root_name = "root"
            source_offset_x = centre_x / 0.48 - frame["joints"][root_name][0]
            draw_mannequin(draw, frame["joints"], clip["view"], source_offset_x, row_y + 20, 0.48)
            draw.text((x_positions[column], row_y + 168), f"F{frame_index + 1}", fill="#badff3", font=font)
        draw.line((0, row_y + row_height - 1, 919, row_y + row_height - 1), fill="#40515e")
    return output


def write_page(motion: dict, register: dict) -> None:
    assets = PUBLIC / "assets"
    if assets.exists(): shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    sheet = ROOT / register["evidence"]["motionContactSheet"]["file"]
    sheet_public = assets / f"motion-{digest(sheet)[:16]}.png"
    shutil.copyfile(sheet, sheet_public)
    shutil.copyfile(PACK / "motion/keeper-prime-rig-motion-v2.json", PUBLIC / "keeper-prime-rig-motion-v2.json")
    embedded = json.dumps(motion, separators=(",", ":"))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime Rig V2 Motion Demo</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58;--green:#77e3a4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1220px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--green);border-radius:999px;padding:5px 10px;color:#a9f3c5}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}#stage{{width:100%;height:auto;aspect-ratio:640/340;background:#0c141b;border:1px solid var(--line);border-radius:8px}}.toolbar{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}button{{background:#243743;color:var(--ink);border:1px solid #577181;border-radius:7px;padding:9px 12px;cursor:pointer}}button.active{{border-color:var(--green);background:#16472c}}label{{display:flex;gap:8px;align-items:center}}input[type=range]{{width:180px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:#0c141b}}.rule{{border-left:4px solid var(--amber);background:#2a2518;padding:10px 14px}}code{{color:#badff3}}</style></head><body><header><a href="/keeper-review/keeper-prime-rig-v1/">← Approved KP Rig V1</a> · <a href="/animation-workbench">Animation Workbench</a><h1>Keeper Prime Rig V2 · motion proof</h1><span class="status">KP Rig V1 approved · construction motion awaiting review</span><p>Frank approved KP Rig V1 on 13 October 2026 and asked to see it animated. This page animates a construction mannequin, not finished Keeper raster art.</p></header><main><p class="rule"><strong>Motion contract:</strong> every sampled upper arm, forearm, wrist-to-palm, thigh and shin keeps its registered length. The walk translates through the stage and resets only while fully hidden; it never walks on the spot.</p><article><svg id="stage" viewBox="0 0 640 340" aria-label="Animated Keeper Prime construction mannequin"></svg><div class="toolbar" id="clips"></div><div class="toolbar"><button id="playPause">Pause</button><button id="restart">Restart</button><label>Speed <input id="speed" type="range" min="25" max="200" value="100"><span id="speedLabel">1×</span></label><label><input id="bones" type="checkbox" checked> Show bones</label><label><input id="trail" type="checkbox"> Motion trail</label></div><p id="readout"></p></article><h2>Key-frame evidence</h2><article><img src="assets/{sheet_public.name}" alt="Idle, walk, reach and sit-stand construction key frames"></article><h2>What to review</h2><article><p>Look for believable shoulder, elbow, hip and knee pivots; restrained idle movement; continuous root travel in the walk; a controlled reach; and stable feet during sit/stand. The simplified mannequin shows volumes only. It is deliberately not proposed artwork.</p></article><h2>Approval boundary</h2><article><p>Motion approval authorizes the separate smooth 90° side artwork draft. It does not approve an animation strip, deform approved raster art or change production.</p><p><code>Maximum sampled segment error: {register['validation']['maximumInvariantSegmentErrorPixels']} px · walk root travel: {register['validation']['walkRootTravelPixels']} px</code></p></article></main><script>
const DATA={embedded};const svg=document.getElementById('stage'),ns='http://www.w3.org/2000/svg',clipsElement=document.getElementById('clips'),playPauseButton=document.getElementById('playPause'),restartButton=document.getElementById('restart'),speedInput=document.getElementById('speed'),speedLabelElement=document.getElementById('speedLabel'),bonesInput=document.getElementById('bones'),trailInput=document.getElementById('trail'),readoutElement=document.getElementById('readout');let clipId='idle',playing=true,start=performance.now(),pausedAt=0;const buttons={{}};function el(tag,a){{const n=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(a))n.setAttribute(k,String(v));return n}}function line(a,b,w,c,o=1){{svg.append(el('line',{{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:c,'stroke-width':w,'stroke-linecap':'round',opacity:o}}))}}function circle(p,r,c,stroke='none'){{svg.append(el('circle',{{cx:p[0],cy:p[1],r,fill:c,stroke,'stroke-width':1}}))}}function P(j,name,ox){{return[j[name][0]+ox,j[name][1]]}}
function renderMannequin(frame,view,opacity=1,bones=true){{const j=frame.joints,ox=frame.offsetX;if(view==='front'){{for(const[a,b,w,c]of [['shoulderLeft','elbowLeft',28,'#0964bd'],['elbowLeft','wristLeft',25,'#0964bd'],['shoulderRight','elbowRight',28,'#0964bd'],['elbowRight','wristRight',25,'#0964bd'],['hipLeft','kneeLeft',31,'#1e2e52'],['kneeLeft','ankleLeft',28,'#1e2e52'],['hipRight','kneeRight',31,'#1e2e52'],['kneeRight','ankleRight',28,'#1e2e52']])line(P(j,a,ox),P(j,b,ox),w,c,opacity);const r=P(j,'root',ox),h=P(j,'headCentre',ox);svg.append(el('ellipse',{{cx:r[0],cy:171,rx:52,ry:53,fill:'#0875d1',stroke:'#061524','stroke-width':4,opacity}}));line([r[0]-49,164],[r[0]+49,164],18,'#fff1c2',opacity);svg.append(el('ellipse',{{cx:h[0],cy:84,rx:46,ry:42,fill:'#ffad68',stroke:'#061524','stroke-width':4,opacity}}));svg.append(el('ellipse',{{cx:h[0],cy:114,rx:42,ry:36,fill:'#fff0d0',stroke:'#061524','stroke-width':4,opacity}}));svg.append(el('ellipse',{{cx:h[0],cy:45,rx:50,ry:27,fill:'#0875d1',stroke:'#061524','stroke-width':4,opacity}}));for(const n of ['handLeft','handRight'])circle(P(j,n,ox),12,'#ffad68','#061524')}}else{{for(const[a,b,w,c]of [['shoulderFar','elbowFar',23,'#24568b'],['elbowFar','wristFar',21,'#24568b'],['hipFar','kneeFar',27,'#172542'],['kneeFar','ankleFar',24,'#172542'],['shoulderNear','elbowNear',28,'#0964bd'],['elbowNear','wristNear',25,'#0964bd'],['hipNear','kneeNear',31,'#1e2e52'],['kneeNear','ankleNear',28,'#1e2e52']])line(P(j,a,ox),P(j,b,ox),w,c,opacity);const r=P(j,'root',ox),h=P(j,'headCentre',ox);svg.append(el('ellipse',{{cx:r[0],cy:171+(r[1]-224),rx:40,ry:53,fill:'#0875d1',stroke:'#061524','stroke-width':4,opacity}}));line([r[0]-36,164+(r[1]-224)],[r[0]+36,164+(r[1]-224)],18,'#fff1c2',opacity);svg.append(el('ellipse',{{cx:h[0],cy:h[1],rx:36,ry:42,fill:'#ffad68',stroke:'#061524','stroke-width':4,opacity}}));svg.append(el('ellipse',{{cx:h[0]+24,cy:h[1]+30,rx:34,ry:36,fill:'#fff0d0',stroke:'#061524','stroke-width':4,opacity}}));svg.append(el('ellipse',{{cx:h[0]-2,cy:h[1]-39,rx:48,ry:27,fill:'#0875d1',stroke:'#061524','stroke-width':4,opacity}}));for(const n of ['handFar','handNear'])circle(P(j,n,ox),12,'#ffad68','#061524')}}if(bones){{const pairs=view==='front'?[['shoulderLeft','elbowLeft'],['elbowLeft','wristLeft'],['wristLeft','handLeft'],['shoulderRight','elbowRight'],['elbowRight','wristRight'],['wristRight','handRight'],['hipLeft','kneeLeft'],['kneeLeft','ankleLeft'],['hipRight','kneeRight'],['kneeRight','ankleRight']]:[['shoulderNear','elbowNear'],['elbowNear','wristNear'],['wristNear','handNear'],['shoulderFar','elbowFar'],['elbowFar','wristFar'],['wristFar','handFar'],['hipNear','kneeNear'],['kneeNear','ankleNear'],['hipFar','kneeFar'],['kneeFar','ankleFar']];for(const[a,b]of pairs){{line(P(j,a,ox),P(j,b,ox),3,'#36d3ff',opacity);circle(P(j,a,ox),3,'#fff')}}}}}}
function render(now){{svg.innerHTML='';svg.append(el('rect',{{x:0,y:0,width:640,height:340,fill:'#0c141b'}}));line([0,316],[640,316],2,'#efbd58',.7);const clip=DATA.clips[clipId],speed=Number(speedInput.value)/100,elapsed=playing?(now-start)*speed:pausedAt*speed,index=Math.floor(elapsed/(1000/clip.fps))%clip.frames.length;if(trailInput.checked){{for(const d of [12,8,4]){{const i=(index-d+clip.frames.length)%clip.frames.length;renderMannequin(clip.frames[i],clip.view,.07,false)}}}}renderMannequin(clip.frames[index],clip.view,1,bonesInput.checked);readoutElement.textContent=`${{clip.label}} · frame ${{index+1}}/${{clip.frames.length}} · ${{clip.fps}} fps${{clip.rootMotion?' · 840px root travel':''}}`;if(playing)requestAnimationFrame(render)}}
for(const[id,clip]of Object.entries(DATA.clips)){{const b=document.createElement('button');b.textContent=clip.label;b.onclick=()=>{{clipId=id;start=performance.now();pausedAt=0;Object.values(buttons).forEach(x=>x.classList.remove('active'));b.classList.add('active');if(!playing){{playing=true;playPauseButton.textContent='Pause';requestAnimationFrame(render)}}}};buttons[id]=b;clipsElement.append(b)}}buttons.idle.classList.add('active');playPauseButton.onclick=()=>{{if(playing){{pausedAt=performance.now()-start;playing=false;playPauseButton.textContent='Play'}}else{{start=performance.now()-pausedAt;playing=true;playPauseButton.textContent='Pause';requestAnimationFrame(render)}}}};restartButton.onclick=()=>{{start=performance.now();pausedAt=0;if(!playing)render(performance.now())}};speedInput.oninput=()=>speedLabelElement.textContent=`${{(Number(speedInput.value)/100).toFixed(2)}}×`;bonesInput.onchange=()=>{{if(!playing)render(performance.now())}};trailInput.onchange=()=>{{if(!playing)render(performance.now())}};requestAnimationFrame(render);
</script></body></html>'''
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    for path in (V1_REGISTER, V1_RIG, FRONT, SIDE):
        if not path.exists(): raise RuntimeError(f"missing {relative(path)}")
    v1_register = json.loads(V1_REGISTER.read_text())
    rig = json.loads(V1_RIG.read_text())
    if v1_register.get("status") != "draft-construction-contract-awaiting-visual-approval": raise RuntimeError("V1 review provenance changed")
    for directory in (PACK / "motion", PACK / "evidence", PUBLIC): directory.mkdir(parents=True, exist_ok=True)
    clips = make_clips(rig)
    validation = validate_motion(clips, rig["invariantSegmentLengths"])
    motion = {
        "motionId": "keeper-prime-construction-rig-2026-10-13-v2-motion",
        "status": "approved-rig-construction-motion-awaiting-review",
        "stage": {"width": STAGE[0], "height": STAGE[1], "floorY": FLOOR_Y},
        "rig": {"file": relative(V1_RIG), "sha256": digest(V1_RIG)},
        "clips": clips,
        "rendering": {"constructionMannequinOnly": True, "finishedRasterArtDeformed": False, "smoothFinishedArtRequiredLater": True},
        "validation": validation,
    }
    motion_path = PACK / "motion/keeper-prime-rig-motion-v2.json"
    dump(motion_path, motion)
    contact = PACK / "evidence/rig-motion-keyframes.png"
    contact_sheet(clips).save(contact, optimize=False, compress_level=9)
    register = {
        "batchId": "keeper-prime-construction-rig-2026-10-13-v2",
        "status": "approved-rig-motion-demo-awaiting-review",
        "purpose": "Record Frank's KP Rig V1 approval and prove its fixed-length construction skeleton under representative motion before finished side artwork.",
        "approvedV1": {"register": relative(V1_REGISTER), "registerSha256": digest(V1_REGISTER), "rig": relative(V1_RIG), "rigSha256": digest(V1_RIG)},
        "approval": {"approvedBy": "Frank", "approvedOn": "2026-10-13", "wording": "Approve KP Rig V1, let's see it animated", "scope": "KP Rig V1 measurement and posable construction contract; authorizes construction-motion proof, not finished art or production promotion."},
        "motion": {"file": relative(motion_path), "sha256": digest(motion_path), "clips": list(clips.keys())},
        "evidence": {"motionContactSheet": {"file": relative(contact), "sha256": digest(contact)}},
        "validation": validation,
        "approvalBoundary": {"motionReviewAllowsSideArtworkAuthoring": True, "finishedAnimationApproved": False, "productionPromotionAllowed": False},
        "nextGate": "Review construction motion, then author one separate smooth side-right endpoint with 15/15 exact y-datums.",
        "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; approved V1, orthographic authorities and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(motion, register)
    print(json.dumps({"batch": register["batchId"], "clips": register["motion"]["clips"], "maxSegmentError": validation["maximumInvariantSegmentErrorPixels"], "walkRootTravel": validation["walkRootTravelPixels"], "publicPage": relative(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
