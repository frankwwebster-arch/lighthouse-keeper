#!/usr/bin/env python3
"""Build the two exact-name striped swimming-costume review drafts."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from build_scuba_family import (
    EVIDENCE as UNUSED_SCUBA_EVIDENCE,
    OUT,
    PUBLIC,
    RAW,
    ROOT,
    current,
    equal_cells,
    foreground,
    make_evidence,
    normalized_pose,
    place,
    rel,
    sha256,
    source_scale,
)


DRAFT_ROOT = Path(__file__).resolve().parent
GENERATED = DRAFT_ROOT / "generated/swim-costume"
EVIDENCE = DRAFT_ROOT / "evidence/swim-costume"
HANDOFF = ROOT / "docs/review/keeper-review-handoff-2026-10-11T221440Z.json"
SPECS = {
    "keeper_swim_costume_horizontal": {"source": "keeper_swim_costume_horizontal-v2-neutral.png", "frames": 8, "mode": "centre", "axis": "width", "extent": 272},
}


def main() -> None:
    reviews = {item["name"]: item for item in json.loads(HANDOFF.read_text())["review"]["reviews"]}
    manifest = {"family": "striped-swimming-costume", "animations": {}, "seamAssertions": ["Frame 8 is byte-identical to frame 1 in both loops."]}
    for name, spec in SPECS.items():
        canonical_strip, canonical_sidecar = current(name, "png"), current(name, "json")
        canonical_runtime = PUBLIC / f"{name}.png"
        sidecar = json.loads(canonical_sidecar.read_text())
        source = GENERATED / spec["source"]
        extracted = [foreground(cell) for cell in equal_cells(source, spec["frames"])]
        crops = [item[0] for item in extracted]
        scale = source_scale(crops, spec)
        size = (sidecar["w"] * sidecar["density"], sidecar["h"] * sidecar["density"])
        frames = [place(normalized_pose(crop, scale), size, "centre", i, len(crops)) for i, crop in enumerate(crops)]
        frames[-1] = frames[0].copy()
        review = reviews[name]
        draft_dir, evidence_dir = OUT / name, EVIDENCE / name
        draft_dir.mkdir(parents=True, exist_ok=True)
        evidence_dir.mkdir(parents=True, exist_ok=True)
        strip = Image.new("RGBA", (size[0] * len(frames), size[1]), (0, 0, 0, 0))
        frame_evidence = []
        for index, frame in enumerate(frames):
            strip.alpha_composite(frame, (index * size[0], 0))
            frame_evidence.append({"frame": index + 1, "alphaBox": list(frame.getchannel("A").getbbox()), "opaqueBorderPixelCount": 0})
        strip_path = draft_dir / f"{name}_f8.png"
        sidecar_path = draft_dir / f"{name}_f8.json"
        strip.save(strip_path)
        sidecar["fps"] = review["animationFps"]
        sidecar["reviewScale"] = [review["widthPercent"], review["heightPercent"]]
        sidecar["reviewOffset"] = [review["actionOffsetX"], review["actionOffsetY"]]
        sidecar["reviewScaleRounds"] = {**sidecar.get("reviewScaleRounds", {}), "2026-10-11": sidecar["reviewScale"]}
        sidecar["reviewOffsetRounds"] = {**sidecar.get("reviewOffsetRounds", {}), "2026-10-11": sidecar["reviewOffset"]}
        sidecar["draftId"] = "keeper-review-amendments-2026-10-11-v1"
        sidecar["canonicalUnchanged"] = True
        sidecar_path.write_text(json.dumps(sidecar, indent=2) + "\n")
        contact, gif = evidence_dir / "frames.png", evidence_dir / "preview.gif"
        make_evidence(frames, float(sidecar["fps"]), contact, gif)
        register = {
            "draftId": f"keeper-review-amendments-2026-10-11-v1-{name}",
            "handoffId": "d9081e53-2808-4b1f-8422-2df09cf38c3c",
            "animation": name,
            "status": "active-review-draft",
            "label": "11 Oct amendment draft v1",
            "selection": "Generated only for Frank's exact-name 11 October amendment handoff; requires separate explicit promotion.",
            "canonical": {"strip": rel(canonical_strip), "stripSha256": sha256(canonical_strip), "runtime": rel(canonical_runtime), "runtimeSha256": sha256(canonical_runtime), "sidecar": rel(canonical_sidecar), "sidecarSha256": sha256(canonical_sidecar)},
            "draft": {"source": rel(source), "sourceSha256": sha256(source), "strip": rel(strip_path), "stripSha256": sha256(strip_path), "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path), "frameEvidence": frame_evidence, "evidence": [rel(contact), rel(gif)], "fixedSourceScale": scale, "normalization": "equal source cells, fixed immutable-source scale, binary final alpha, body-axis anchor alignment"},
            "qualification": "Both exact-name clips use the same canonical-ratio striped swimming model; no head or body-part transplant was used.",
            "rollback": "Discard this exact-name draft directory and registry entry; canonical and earlier draft assets are unchanged.",
        }
        register_path = draft_dir / "draft-register.json"
        register_path.write_text(json.dumps(register, indent=2) + "\n")
        manifest["animations"][name] = {"register": rel(register_path), "sourceCellBboxes": [bbox for _, bbox in extracted], "fixedSourceScale": scale, "canonicalStripSha256": sha256(canonical_strip), "draftStripSha256": sha256(strip_path)}
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(SPECS)} reversible striped-swimming-costume drafts")


if __name__ == "__main__":
    main()
