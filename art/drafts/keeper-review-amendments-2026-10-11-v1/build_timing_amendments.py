#!/usr/bin/env python3
"""Build exact-frame timing, hold, and canvas amendments without repainting art."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

from build_party_family import contact_sheet, gif_preview


ROOT = Path(__file__).resolve().parents[3]
DRAFT_ROOT = Path(__file__).resolve().parent
RAW = ROOT / "art/raw/keeper-first-batch"
PUBLIC = ROOT / "public/sprites"
OUT = DRAFT_ROOT / "drafts"
EVIDENCE = DRAFT_ROOT / "evidence/timing"
HANDOFF = ROOT / "docs/review/keeper-review-handoff-2026-10-11T221440Z.json"
GUTTER = 2

SPECS = {
    "keeper_eat_seated": {"indices": [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1], "note": "mirrored lowering phase added after the raise sequence"},
    "keeper_nap_seated": {"indices": [1, 2, 3, 4, 5, 6], "note": "neutral frames 1 and 8 removed; only head-back open-mouth nap remains"},
    "keeper_fish_feed_up": {"indices": list(range(14)), "note": "verified frame 8 plus six byte-identical hold frames; reviewer cadence applied"},
    "keeper_shower_enter_bathrobe": {"indices": list(range(8)), "note": "reviewer size and position saved without repainting accepted art"},
    "keeper_shower_door_open_bathrobe": {"indices": list(range(10)), "note": "two logical pixels of right-side canvas margin added for the reported crop", "right_margin_logical": 2},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def current(name: str, suffix: str) -> Path:
    matches = sorted(RAW.glob(f"{name}_f*.{suffix}"))
    if len(matches) != 1:
        raise ValueError(f"Expected one canonical {suffix} for {name}, found {matches}")
    return matches[0]


def main() -> None:
    reviews = {item["name"]: item for item in json.loads(HANDOFF.read_text())["review"]["reviews"]}
    manifest = {"family": "timing-and-canvas", "animations": {}}
    for name, spec in SPECS.items():
        canonical_strip = current(name, "png")
        canonical_sidecar = current(name, "json")
        canonical_runtime = PUBLIC / f"{name}.png"
        sidecar = json.loads(canonical_sidecar.read_text())
        source = Image.open(canonical_strip).convert("RGBA")
        old_width = sidecar["w"] * sidecar["density"]
        old_height = sidecar["h"] * sidecar["density"]
        source_frames = [source.crop((i * old_width, 0, (i + 1) * old_width, old_height)) for i in range(sidecar["frames"])]
        right_margin = spec.get("right_margin_logical", 0) * sidecar["density"]
        frames = []
        for index in spec["indices"]:
            frame = source_frames[index].copy()
            if right_margin:
                expanded = Image.new("RGBA", (old_width + right_margin, old_height), (0, 0, 0, 0))
                expanded.alpha_composite(frame)
                frame = expanded
            frames.append(frame)
        frame_width = frames[0].width
        for index, frame in enumerate(frames):
            bbox = frame.getchannel("A").getbbox()
            if bbox is None or bbox[0] < GUTTER or bbox[1] < GUTTER or bbox[2] > frame.width - GUTTER or bbox[3] > frame.height - GUTTER:
                raise ValueError(f"{name} frame {index + 1} violates safety gutter: {bbox}")
        draft_dir = OUT / name
        evidence_dir = EVIDENCE / name
        draft_dir.mkdir(parents=True, exist_ok=True)
        evidence_dir.mkdir(parents=True, exist_ok=True)
        strip = Image.new("RGBA", (frame_width * len(frames), old_height), (0, 0, 0, 0))
        frame_evidence = []
        for index, frame in enumerate(frames):
            strip.alpha_composite(frame, (index * frame_width, 0))
            frame_evidence.append({"frame": index + 1, "alphaBox": list(frame.getchannel("A").getbbox()), "opaqueBorderPixelCount": 0})
        strip_path = draft_dir / f"{name}_f{len(frames)}.png"
        sidecar_path = draft_dir / f"{name}_f{len(frames)}.json"
        strip.save(strip_path)
        review = reviews[name]
        sidecar["frames"] = len(frames)
        sidecar["fps"] = review["animationFps"]
        if right_margin:
            sidecar["w"] += spec["right_margin_logical"]
        sidecar["reviewScale"] = [review["widthPercent"], review["heightPercent"]]
        sidecar["reviewOffset"] = [review["actionOffsetX"], review["actionOffsetY"]]
        sidecar["reviewScaleRounds"] = {**sidecar.get("reviewScaleRounds", {}), "2026-10-11": sidecar["reviewScale"]}
        sidecar["reviewOffsetRounds"] = {**sidecar.get("reviewOffsetRounds", {}), "2026-10-11": sidecar["reviewOffset"]}
        sidecar["draftId"] = "keeper-review-amendments-2026-10-11-v1"
        sidecar["canonicalUnchanged"] = True
        sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")
        contact, gif = evidence_dir / "frames.png", evidence_dir / "preview.gif"
        contact_sheet(frames, contact)
        gif_preview(frames, float(sidecar["fps"]), gif)
        register = {
            "draftId": f"keeper-review-amendments-2026-10-11-v1-{name}",
            "handoffId": "d9081e53-2808-4b1f-8422-2df09cf38c3c",
            "animation": name,
            "status": "active-review-draft",
            "label": "11 Oct amendment draft v1",
            "selection": "Exact-name timing/canvas amendment only; requires separate explicit promotion.",
            "canonical": {"strip": rel(canonical_strip), "stripSha256": sha256(canonical_strip), "runtime": rel(canonical_runtime), "runtimeSha256": sha256(canonical_runtime), "sidecar": rel(canonical_sidecar), "sidecarSha256": sha256(canonical_sidecar)},
            "draft": {"source": rel(canonical_strip), "sourceSha256": sha256(canonical_strip), "strip": rel(strip_path), "stripSha256": sha256(strip_path), "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path), "frameEvidence": frame_evidence, "evidence": [rel(contact), rel(gif)], "normalization": "exact canonical frame copies only; reviewed frame order/holds and optional transparent canvas extension; no repainting"},
            "qualification": spec["note"],
            "rollback": "Discard this exact-name draft directory and registry entry; canonical and earlier draft assets are unchanged.",
        }
        register_path = draft_dir / "draft-register.json"
        register_path.write_text(json.dumps(register, indent=2) + "\n")
        manifest["animations"][name] = {"register": rel(register_path), "canonicalStripSha256": sha256(canonical_strip), "draftStripSha256": sha256(strip_path), "frameOrder": [i + 1 for i in spec["indices"]]}
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(SPECS)} reversible timing/canvas drafts")


if __name__ == "__main__":
    main()
