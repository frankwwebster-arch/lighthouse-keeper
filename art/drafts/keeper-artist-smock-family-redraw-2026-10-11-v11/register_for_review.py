#!/usr/bin/env python3
"""Register every V11 artist-smock family entry as a reversible review draft."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DRAFTS = HERE / "drafts"
REGISTERS = HERE / "registers"
RAW = ROOT / "art/raw/keeper-first-batch"
RUNTIME = ROOT / "public/sprites"
REGISTRY = ROOT / "data/keeper_review_drafts.json"
DENSITY = 4
LABEL = "V11 consistent artist set"


ASSETS = {
    "keeper_artist_smock_walk": ("keeper_artist_smock_walk_f8.png", "generated/keeper_artist_smock_walk-source.png"),
    "keeper_artist_smock_turn_back": ("keeper_artist_smock_turn_back_f6.png", "generated/keeper_artist_smock_turn_back-source.png"),
    "keeper_artist_smock_turn_front": ("keeper_artist_smock_turn_front_f6.png", "generated/keeper_artist_smock_turn_front-source.png"),
    "keeper_artist_smock_sit_front": ("keeper_artist_smock_sit_front_f6.png", "generated/keeper_artist_smock_sit_front-source.png"),
    "keeper_paint_side": ("keeper_paint_side_f8.png", "generated/keeper_paint_side-source.png"),
    "keeper_paint_back": ("keeper_paint_back_f8.png", "generated/keeper_paint_back-source.png"),
    "keeper_pottery_front": ("keeper_pottery_front_f8.png", "generated/keeper_pottery_front-source.png"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def frame_evidence(strip: Image.Image, frames: int) -> list[dict]:
    frame_width = strip.width // frames
    evidence = []
    for index in range(frames):
        frame = strip.crop((index * frame_width, 0, (index + 1) * frame_width, strip.height))
        alpha = np.asarray(frame.getchannel("A"))
        ys, xs = np.where(alpha > 0)
        if not len(xs):
            raise RuntimeError(f"empty frame {index + 1}")
        border = (
            np.count_nonzero(alpha[0, :]) + np.count_nonzero(alpha[-1, :])
            + np.count_nonzero(alpha[:, 0]) + np.count_nonzero(alpha[:, -1])
        )
        if border:
            raise RuntimeError(f"frame {index + 1} has {border} opaque border pixels")
        evidence.append({
            "frame": index + 1,
            "draftAlphaBox": [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)],
            "opaqueBorderPixelCount": int(border),
        })
    return evidence


def ensure_sidecar(name: str, draft_strip: Path, canonical_sidecar: Path) -> tuple[Path, dict]:
    image = Image.open(draft_strip).convert("RGBA")
    path = draft_strip.with_suffix(".json")
    base = json.loads(path.read_text()) if path.exists() else json.loads(canonical_sidecar.read_text())
    frames = int(base["frames"])
    if image.width % frames or image.height % DENSITY or (image.width // frames) % DENSITY:
        raise RuntimeError(f"{name} draft geometry is not density-{DENSITY} aligned")
    expected = {
        "w": image.width // frames // DENSITY,
        "h": image.height // DENSITY,
        "anchor": [image.width // frames // DENSITY // 2, image.height // DENSITY],
    }
    for key, value in expected.items():
        if base.get(key) != value:
            raise RuntimeError(f"{name} draft sidecar {key} is {base.get(key)}, expected {value}")
    if base.get("density") != DENSITY or not base.get("draft"):
        raise RuntimeError(f"{name} draft sidecar lost its density/draft contract")
    return path, base


def main() -> None:
    REGISTERS.mkdir(exist_ok=True)
    validation = json.loads((HERE / "evidence/validation.json").read_text())
    registered = []
    for name, (filename, source_relative) in ASSETS.items():
        draft_strip = DRAFTS / filename
        source = HERE / source_relative
        canonical_candidates = sorted(RAW.glob(f"{name}_f*.png"))
        if len(canonical_candidates) != 1:
            raise RuntimeError(f"expected one canonical strip for {name}, found {canonical_candidates}")
        canonical_strip = canonical_candidates[0]
        canonical_sidecar = canonical_strip.with_suffix(".json")
        runtime = RUNTIME / f"{name}.png"
        for required in (draft_strip, source, canonical_strip, canonical_sidecar, runtime):
            if not required.exists():
                raise RuntimeError(f"missing required input: {required}")

        draft_sidecar, sidecar = ensure_sidecar(name, draft_strip, canonical_sidecar)
        image = Image.open(draft_strip).convert("RGBA")
        alpha = np.asarray(image.getchannel("A"))
        if not np.isin(alpha, [0, 255]).all():
            raise RuntimeError(f"{name} draft alpha is not binary")
        evidence = frame_evidence(image, sidecar["frames"])
        evidence_paths = [
            "art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/evidence/artist-smock-family-overview.png",
            "art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/evidence/front-transition-seam-proof.png",
        ]
        comparison = HERE / "evidence" / f"{name}-comparison.gif"
        if comparison.exists():
            evidence_paths.append(relative(comparison))

        authored = validation["authoredClips"].get(name)
        derived = validation["derivedAssets"].get(name)
        record = {
            "draftId": f"{name}-artist-smock-v11",
            "animation": name,
            "status": "active-review-draft",
            "label": LABEL,
            "selection": (
                "Frank accepted the internally consistent V11 artist-smock family, subject only to the exact "
                "turn-front-to-sit-front seam; the registered V11 strips enforce whole-frame identity at that seam."
            ),
            "canonical": {
                "strip": relative(canonical_strip),
                "stripSha256": sha256(canonical_strip),
                "runtime": relative(runtime),
                "runtimeSha256": sha256(runtime),
                "sidecar": relative(canonical_sidecar),
                "sidecarSha256": sha256(canonical_sidecar),
            },
            "draft": {
                "source": relative(source),
                "sourceSha256": sha256(source),
                "strip": relative(draft_strip),
                "stripSha256": sha256(draft_strip),
                "sidecar": relative(draft_sidecar),
                "sidecarSha256": sha256(draft_sidecar),
                "frames": sidecar["frames"],
                "canvas": [sidecar["w"], sidecar["h"]],
                "density": sidecar["density"],
                "anchor": sidecar["anchor"],
                "uniformScale": authored.get("uniformScale") if authored else None,
                "derivedFrom": None if authored else (derived or {}),
                "frameEvidence": evidence,
                "evidence": evidence_paths,
            },
        }
        register = REGISTERS / f"{name}.json"
        register.write_text(json.dumps(record, indent=2) + "\n")
        registered.append({
            "name": name,
            "status": "active-review-draft",
            "label": LABEL,
            "register": relative(register),
        })

    registry = json.loads(REGISTRY.read_text())
    names = set(ASSETS)
    registry["drafts"] = [
        item for item in registry["drafts"]
        if item["name"] not in names and item.get("label") != LABEL
    ] + registered
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")

    validation["scopeGate"]["registered"] = True
    validation["scopeGate"]["reviewerAuthoredAnimations"] = len(registered)
    validation["scopeGate"]["reviewerTechnicalDerivativesExcluded"] = 8
    (HERE / "evidence/validation.json").write_text(json.dumps(validation, indent=2) + "\n")

    # The user's preferred front seam is an exact complete-frame identity gate.
    turn = Image.open(DRAFTS / "keeper_artist_smock_turn_front_f6.png").convert("RGBA")
    sit = Image.open(DRAFTS / "keeper_artist_smock_sit_front_f6.png").convert("RGBA")
    if turn.crop((5 * 128, 0, 6 * 128, 160)).tobytes() != sit.crop((0, 0, 128, 160)).tobytes():
        raise RuntimeError("turn-front frame 6 no longer equals sit-front frame 1")
    print(f"Registered {len(registered)} reversible V11 artist-smock drafts; front seam is byte-identical")


if __name__ == "__main__":
    main()
