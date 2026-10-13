#!/usr/bin/env python3
"""Build the reversible KP Rig Motion V3 walk-cadence revision."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v3"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-rig-v3"
V1_RIG = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v1/rig/keeper-prime-rig-v1.json"
V2_PACK = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v2"
V2_REGISTER = V2_PACK / "batch-register.json"
V2_MOTION = V2_PACK / "motion/keeper-prime-rig-motion-v2.json"
V2_PAGE = ROOT / "public/keeper-review/keeper-prime-rig-v2/index.html"
V2_BUILDER = ROOT / "scripts/build_keeper_prime_rig_motion_v2.py"

WALK_FRAMES = 150
WALK_FPS = 30
WALK_CYCLES = 4
WALK_STEPS = 8
WALK_TRAVEL = 840.0
SOURCE_CENTRE = 128.0
FEEDBACK = "He needs to do more leg movement during the walk, moves too fast with too few steps. Otherwise very good indeed."


def load_v2_builder():
    spec = importlib.util.spec_from_file_location("keeper_prime_rig_motion_v2", V2_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load V2 builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V2 = load_v2_builder()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def revised_clips(rig: dict) -> dict:
    clips = V2.make_clips(rig)
    side_base = json.loads(json.dumps(clips["walk"]["frames"][0]["joints"]))
    invariant = rig["invariantSegmentLengths"]
    upper, fore, hand = invariant["upperArm"], invariant["forearm"], invariant["wristToPalmCentre"]
    thigh, shin = invariant["thigh"], invariant["shin"]
    angles = {
        "nearUpper": V2.angle_from_vertical(side_base["shoulderNear"], side_base["elbowNear"]),
        "nearFore": V2.angle_from_vertical(side_base["elbowNear"], side_base["wristNear"]),
        "farUpper": V2.angle_from_vertical(side_base["shoulderFar"], side_base["elbowFar"]),
        "farFore": V2.angle_from_vertical(side_base["elbowFar"], side_base["wristFar"]),
    }
    frames = []
    for index in range(WALK_FRAMES):
        progress = index / (WALK_FRAMES - 1)
        phase = 2 * math.pi * WALK_CYCLES * progress
        swing = math.sin(phase)
        joints = json.loads(json.dumps(side_base))
        V2.set_arm(joints, "Near", upper, fore, hand, angles["nearUpper"] - swing * 26, angles["nearFore"] - swing * 20)
        V2.set_arm(joints, "Far", upper, fore, hand, angles["farUpper"] + swing * 26, angles["farFore"] + swing * 20)
        near_bend = max(0.0, -swing) * 44
        far_bend = max(0.0, swing) * 44
        V2.set_leg(joints, "Near", thigh, shin, swing * 32, swing * 32 - near_bend)
        V2.set_leg(joints, "Far", thigh, shin, -swing * 32, -swing * 32 - far_bend)
        world_root_x = -100 + progress * WALK_TRAVEL
        frames.append({
            "joints": joints,
            "offsetX": round(world_root_x - SOURCE_CENTRE, 6),
            "breath": 0.5,
            "gaitPhase": round((phase % (2 * math.pi)) / (2 * math.pi), 6),
        })
    clips["walk"] = {
        "label": "Walk with slower 8-step cadence",
        "view": "side",
        "fps": WALK_FPS,
        "loop": True,
        "frames": frames,
        "rootMotion": True,
        "rootTravelPixels": WALK_TRAVEL,
        "durationSeconds": WALK_FRAMES / WALK_FPS,
        "gaitCycles": WALK_CYCLES,
        "impliedSteps": WALK_STEPS,
        "rootSpeedPixelsPerSecond": round(WALK_TRAVEL / (WALK_FRAMES / WALK_FPS), 6),
        "thighSwingDegrees": 32,
        "maximumKneeLiftDegrees": 44,
        "startsFullyHidden": True,
        "endsFullyHidden": True,
        "endpointRule": "four complete gait cycles; loop reset occurs entirely outside the visible stage",
    }
    return clips


def write_page(motion: dict, register: dict) -> None:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    sheet = ROOT / register["evidence"]["motionContactSheet"]["file"]
    sheet_public = assets / f"motion-{digest(sheet)[:16]}.png"
    shutil.copyfile(sheet, sheet_public)
    public_motion = PUBLIC / "keeper-prime-rig-motion-v3.json"
    shutil.copyfile(PACK / "motion/keeper-prime-rig-motion-v3.json", public_motion)

    page = V2_PAGE.read_text()
    replacements = {
        "Keeper Prime Rig V2 Motion Demo": "Keeper Prime Rig V3 Motion Demo",
        "Keeper Prime Rig V2 · motion proof": "Keeper Prime Rig V3 · slower walk cadence",
        "KP Rig V1 approved · construction motion awaiting review": "KP Rig V1 approved · slower walk revision awaiting review",
        "Frank approved KP Rig V1 on 13 October 2026 and asked to see it animated. This page animates a construction mannequin, not finished Keeper raster art.": "Frank found the V2 motion very good overall, but asked for more leg movement, more steps and a slower walk. V3 changes only that cadence; it remains a construction mannequin, not finished Keeper raster art.",
        "The walk translates through the stage and resets only while fully hidden; it never walks on the spot.": "The revised walk now uses eight steps over five seconds, with greater thigh swing and knee lift. It still translates through the stage and resets only while fully hidden; it never walks on the spot.",
        "assets/motion-0e64dc88b2b2c30a.png": f"assets/{sheet_public.name}",
        "Maximum sampled segment error: 0.0 px · walk root travel: 840.0 px": "Maximum sampled segment error: 0.0 px · 8 steps / 5 seconds · 168 px/s root speed",
        "Motion approval authorizes the separate smooth 90° side artwork draft.": "V3 motion approval authorizes the separate smooth 90° side artwork draft.",
    }
    for old, new in replacements.items():
        if old not in page:
            raise RuntimeError(f"V2 page template no longer contains: {old}")
        page = page.replace(old, new)
    prefix, embedded_and_suffix = page.split("const DATA=", 1)
    _, suffix = embedded_and_suffix.split(";const svg=", 1)
    embedded = json.dumps(motion, separators=(",", ":"))
    page = f"{prefix}const DATA={embedded};const svg={suffix}"
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    for path in (V1_RIG, V2_REGISTER, V2_MOTION, V2_PAGE, V2_BUILDER):
        if not path.exists():
            raise RuntimeError(f"missing {relative(path)}")
    rig = json.loads(V1_RIG.read_text())
    v2_motion = json.loads(V2_MOTION.read_text())
    clips = revised_clips(rig)
    validation = V2.validate_motion(clips, rig["invariantSegmentLengths"])
    validation.update({
        "walkFrameCount": WALK_FRAMES,
        "walkDurationSeconds": WALK_FRAMES / WALK_FPS,
        "walkGaitCycles": WALK_CYCLES,
        "walkImpliedSteps": WALK_STEPS,
        "walkRootSpeedPixelsPerSecond": round(WALK_TRAVEL / (WALK_FRAMES / WALK_FPS), 6),
        "v2WalkFrameCount": len(v2_motion["clips"]["walk"]["frames"]),
        "v2WalkRootSpeedPixelsPerSecond": 420.0,
        "unchangedClipIds": ["idle", "reach", "sitStand"],
    })
    motion = {
        "motionId": "keeper-prime-construction-rig-2026-10-13-v3-motion",
        "status": "approved-rig-walk-cadence-revision-awaiting-review",
        "stage": v2_motion["stage"],
        "rig": v2_motion["rig"],
        "clips": clips,
        "rendering": v2_motion["rendering"],
        "validation": validation,
    }
    for directory in (PACK / "motion", PACK / "evidence", PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    motion_path = PACK / "motion/keeper-prime-rig-motion-v3.json"
    dump(motion_path, motion)
    contact = PACK / "evidence/rig-motion-keyframes.png"
    V2.contact_sheet(clips).save(contact, optimize=False, compress_level=9)
    register = {
        "batchId": "keeper-prime-construction-rig-2026-10-13-v3",
        "status": "walk-cadence-revision-awaiting-review",
        "purpose": "Respond only to Frank's V2 walk-cadence feedback while preserving the three accepted motion demonstrations unchanged.",
        "feedback": {"by": "Frank", "on": "2026-10-13", "wording": FEEDBACK},
        "predecessor": {"register": relative(V2_REGISTER), "registerSha256": digest(V2_REGISTER), "motion": relative(V2_MOTION), "motionSha256": digest(V2_MOTION), "publicPageSha256": digest(V2_PAGE)},
        "motion": {"file": relative(motion_path), "sha256": digest(motion_path), "clips": list(clips.keys())},
        "evidence": {"motionContactSheet": {"file": relative(contact), "sha256": digest(contact)}},
        "walkRevision": {"previousFrames": 60, "candidateFrames": WALK_FRAMES, "previousDurationSeconds": 2, "candidateDurationSeconds": 5, "previousGaitCycles": 1, "candidateGaitCycles": WALK_CYCLES, "previousImpliedSteps": 2, "candidateImpliedSteps": WALK_STEPS, "previousRootSpeedPixelsPerSecond": 420, "candidateRootSpeedPixelsPerSecond": 168, "previousThighSwingDegrees": 25, "candidateThighSwingDegrees": 32, "previousMaximumKneeLiftDegrees": 34, "candidateMaximumKneeLiftDegrees": 44},
        "unchangedClips": ["idle", "reach", "sitStand"],
        "validation": validation,
        "approvalBoundary": {"motionRevisionApproved": False, "finishedAnimationApproved": False, "productionPromotionAllowed": False},
        "nextGate": "Review the slower eight-step walk; after motion approval, author the separate smooth side-right endpoint with 15/15 exact y-datums.",
        "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; V1, V2, orthographic authorities and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(motion, register)
    print(json.dumps({"batch": register["batchId"], "walkFrames": WALK_FRAMES, "walkSeconds": 5, "steps": WALK_STEPS, "rootSpeed": 168, "publicPage": relative(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
