#!/usr/bin/env python3
"""Stage and promote Frank's selected keeper sheets as reversible exact-name replacements.

The selected source files are copied byte-for-byte into a versioned draft.  The
production candidates are the previously verified outputs from commit 2b90227;
only the explicitly selected exact animation names are read from that commit.
The snow and machete candidates use their matching isolated-grid working
sources because the one-row references contain joined neighbouring poses.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "art/raw/keeper-first-batch"
PUBLIC = ROOT / "public/sprites"
DRAFT_ID = "keeper-user-selected-batch-2026-10-10-v1"
DRAFT_ROOT = ROOT / "art/drafts" / DRAFT_ID
REGISTRY = ROOT / "data/keeper_review_drafts.json"
SOURCE_ROOT = Path("/Users/frank/.codex/generated_images/01a12506-3c6d-7d52-a0b1-dc3b36fc032c")
HISTORICAL_COMMIT = "2b90227"


SELECTIONS = {
    "keeper_guitar_pickup_flying_v_1967": {
        "attachment": "exec-81f7097c-8efc-40db-b602-1687af35613e.png",
        "sha256": "183e9ad3b1f7288c327a7109a2f1e3f507f909e1f67482b6e33be763d842dc69",
        "raw": "keeper_guitar_pickup_flying_v_1967_f12",
    },
    "keeper_guitar_pickup_gretsch": {
        "attachment": "exec-c2da8dec-a980-40a8-9c2b-45d09face5fc.png",
        "sha256": "62319e80e21c9d093178f18521580b926ffcc2ed785c5946321959d42b09fae6",
        "raw": "keeper_guitar_pickup_gretsch_f12",
    },
    "keeper_guitar_pickup_acoustic": {
        "attachment": "exec-96d5e306-fc19-4d7d-b76f-2ca9d950c5d3.png",
        "sha256": "97220284e11ed3bd664c5d65be655b63fe3284f800a2f86c93912dbcad3b6893",
        "raw": "keeper_guitar_pickup_acoustic_f12",
    },
    "keeper_fish_standing": {
        "attachment": "exec-565653f3-f431-424e-a283-b90f264f8336.png",
        "sha256": "9ecf2af163e9290499be1379e61580c459685d966e6a82d2db0312aca7f87124",
        "raw": "keeper_fish_standing_f50",
    },
    "keeper_fish_seated": {
        "attachment": "exec-4e62f4b3-55cb-499e-b593-1bc168d2017e.png",
        "sha256": "8dedc0f4473fcdc49d8d67e2ff494f0e99e17391ca8e5a7462bbb592c2c06580",
        "raw": "keeper_fish_seated_f41",
    },
    "keeper_clear_snow": {
        "attachment": "exec-77d26231-3d0c-4ff9-a918-e8cc055ecf8c.png",
        "sha256": "c4eea3f639873f14d91736a10c7f411d6da4423ac158fb6346fe79a3cb3c87a6",
        "raw": "keeper_clear_snow_f8",
        "workingSource": "art/source/keeper-first-batch/keeper-clear-snow-round2-grid-generated-source.png",
        "workingSourceSha256": "b5470890cef0448794414393947e50eb55971884d59cb389a8947bdbbf5dc455",
        "qualification": "The earlier supplied one-row snow source joins neighbouring poses; the later supplied separated version identifies the selected artwork and the matching isolated-grid source is used for deterministic production extraction.",
    },
    "keeper_meal_place_side": {
        "attachment": "exec-c450ecd5-e433-48f9-a3e2-cdbe85d692a2.png",
        "sha256": "46b5157591944ac624118f759a4c6bf6949501e391b3e7e06a1fa442788302e4",
        "raw": "keeper_meal_place_side_f8",
    },
    "keeper_parachute_drift": {
        "attachment": "exec-b2870e70-1651-44a3-8d74-4d709d0c6711.png",
        "sha256": "5f461731f05c2eeb7c2e7e911e5a5760e70a127337f2be81b6b4399f8612a39f",
        "raw": "keeper_parachute_drift_f8",
    },
    "keeper_machete_side": {
        "attachment": "exec-4284d279-2218-4606-b4fc-76592b11df0b.png",
        "sha256": "df6209ee8d6a0b5abb7133881721164846b9065bcfd189ce03d5b60c1eac7fc0",
        "raw": "keeper_machete_side_f8",
        "workingSource": "art/source/keeper-first-batch/keeper-machete-side-round2-grid-generated-source.png",
        "workingSourceSha256": "6424439fb6be1809242bb587042763bfcd5d245472bae2d34c54e4acb1a1da64",
        "qualification": "Two poses touch in the supplied one-row sheet; the matching isolated-grid working copy supplies the same eight poses without ambiguous shared pixels.",
    },
}

SUPERSEDED_SNOW = {
    "attachment": "exec-61d2e06f-7657-41cc-82fe-4c85059462b7.png",
    "sha256": "b34b7c40710d9110ef93eb5d7aecf6b4b3d6a69df54534c45ffdcebb8ebe26d6",
    "reason": "Superseded by Frank's later separated snow sheet; its source poses join across frame ownership boundaries.",
}

LANDING_DEPENDENCY = {
    "name": "keeper_parachute_landing",
    "source": "art/source/keeper-first-batch/keeper-parachute-landing-generated-source.png",
    "sourceSha256": "6a0b199f02897906e20207bd4badbbe79687daaea36472322f1681129e861976",
    "raw": "keeper_parachute_landing_f10",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{HISTORICAL_COMMIT}:{path}"], cwd=ROOT)


def current_raw(name: str, suffix: str) -> Path:
    matches = sorted(RAW.glob(f"{name}_f*.{suffix}"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one current {suffix} for {name}, found {matches}")
    return matches[0]


def verify_gutters(strip_path: Path, sidecar_path: Path) -> list[list[int]]:
    sidecar = json.loads(sidecar_path.read_text())
    image = Image.open(strip_path).convert("RGBA")
    frame_width = sidecar["w"] * sidecar["density"]
    if image.size != (frame_width * sidecar["frames"], sidecar["h"] * sidecar["density"]):
        raise RuntimeError(f"geometry mismatch for {strip_path}")
    boxes = []
    for index in range(sidecar["frames"]):
        frame = image.crop((index * frame_width, 0, (index + 1) * frame_width, image.height))
        box = frame.getchannel("A").getbbox()
        if box is None or box[0] == 0 or box[1] == 0 or box[2] == frame_width or box[3] == image.height:
            raise RuntimeError(f"frame {index + 1} lacks a full transparent safety gutter in {strip_path}: {box}")
        boxes.append(list(box))
    return boxes


def write_contact_sheet(strip_path: Path, sidecar_path: Path, destination: Path) -> None:
    """Lay out every final candidate cell so production inspection is explicit."""
    sidecar = json.loads(sidecar_path.read_text())
    image = Image.open(strip_path).convert("RGBA")
    frame_width = sidecar["w"] * sidecar["density"]
    columns = min(10, sidecar["frames"])
    rows = (sidecar["frames"] + columns - 1) // columns
    scale = min(1.0, 220 / frame_width, 220 / image.height)
    cell_width = round(frame_width * scale) + 8
    cell_height = round(image.height * scale) + 8
    contact = Image.new("RGBA", (columns * cell_width, rows * cell_height), (28, 35, 46, 255))
    for index in range(sidecar["frames"]):
        frame = image.crop((index * frame_width, 0, (index + 1) * frame_width, image.height))
        frame = frame.resize((round(frame.width * scale), round(frame.height * scale)), Image.Resampling.NEAREST)
        x = (index % columns) * cell_width + 4
        y = (index // columns) * cell_height + 4
        contact.alpha_composite(frame, (x, y))
    destination.parent.mkdir(parents=True, exist_ok=True)
    contact.convert("RGB").save(destination, quality=95)


def stage() -> None:
    DRAFT_ROOT.mkdir(parents=True, exist_ok=True)
    entries = []
    for name, spec in SELECTIONS.items():
        target = DRAFT_ROOT / name
        source_dir = target / "source"
        previous_dir = target / "previous"
        candidate_dir = target / "candidate"
        for directory in (source_dir, previous_dir, candidate_dir):
            directory.mkdir(parents=True, exist_ok=True)

        supplied = SOURCE_ROOT / spec["attachment"]
        stored_source = source_dir / spec["attachment"]
        if supplied.exists():
            shutil.copyfile(supplied, stored_source)
        if not stored_source.exists() or sha256(stored_source) != spec["sha256"]:
            raise RuntimeError(f"selected source hash mismatch for {name}")

        old_raw = current_raw(name, "png")
        old_sidecar = current_raw(name, "json")
        old_runtime = PUBLIC / f"{name}.png"
        previous_strip = previous_dir / old_raw.name
        previous_sidecar = previous_dir / old_sidecar.name
        previous_runtime = previous_dir / old_runtime.name
        shutil.copyfile(old_raw, previous_strip)
        shutil.copyfile(old_sidecar, previous_sidecar)
        shutil.copyfile(old_runtime, previous_runtime)

        raw_base = spec["raw"]
        candidate_strip = candidate_dir / f"{raw_base}.png"
        candidate_sidecar = candidate_dir / f"{raw_base}.json"
        candidate_strip.write_bytes(git_blob(f"art/raw/keeper-first-batch/{raw_base}.png"))
        candidate_sidecar.write_bytes(git_blob(f"art/raw/keeper-first-batch/{raw_base}.json"))
        frame_boxes = verify_gutters(candidate_strip, candidate_sidecar)
        contact_sheet = target / "evidence/final-candidate-frames.jpg"
        write_contact_sheet(candidate_strip, candidate_sidecar, contact_sheet)

        working_source = spec.get("workingSource")
        if working_source:
            working_path = ROOT / working_source
            if sha256(working_path) != spec["workingSourceSha256"]:
                raise RuntimeError(f"isolated working source hash mismatch for {name}")

        record = {
            "draftId": f"{DRAFT_ID}-{name}",
            "animation": name,
            "status": "active-review-draft",
            "label": "Frank-selected replacement",
            "selection": "Frank supplied this sheet and requested that it replace the current exact-name animation.",
            "canonical": {
                "strip": rel(previous_strip), "stripSha256": sha256(previous_strip),
                "runtime": rel(previous_runtime), "runtimeSha256": sha256(previous_runtime),
                "sidecar": rel(previous_sidecar), "sidecarSha256": sha256(previous_sidecar),
            },
            "draft": {
                "source": rel(stored_source), "sourceSha256": sha256(stored_source),
                "strip": rel(candidate_strip), "stripSha256": sha256(candidate_strip),
                "sidecar": rel(candidate_sidecar), "sidecarSha256": sha256(candidate_sidecar),
                "frameEvidence": [{"frame": index + 1, "alphaBox": box} for index, box in enumerate(frame_boxes)],
                "evidence": [rel(contact_sheet)],
                **({"workingSource": working_source, "workingSourceSha256": spec["workingSourceSha256"]} if working_source else {}),
            },
            "qualification": spec.get("qualification"),
            "rollback": "Restore the three files in previous/ and discard this exact animation draft; no other keeper animation is involved.",
        }
        register = target / "draft-register.json"
        register.write_text(json.dumps(record, indent=2) + "\n")
        entries.append({"name": name, "status": "active-review-draft", "label": record["label"], "register": rel(register)})

    superseded_dir = DRAFT_ROOT / "keeper_clear_snow/source"
    superseded = SOURCE_ROOT / SUPERSEDED_SNOW["attachment"]
    stored_superseded = superseded_dir / SUPERSEDED_SNOW["attachment"]
    if superseded.exists():
        shutil.copyfile(superseded, stored_superseded)
    if not stored_superseded.exists() or sha256(stored_superseded) != SUPERSEDED_SNOW["sha256"]:
        raise RuntimeError("superseded snow source hash mismatch")
    (DRAFT_ROOT / "superseded-sources.json").write_text(json.dumps({
        "keeper_clear_snow": {**SUPERSEDED_SNOW, "stored": rel(stored_superseded)}
    }, indent=2) + "\n")

    registry = json.loads(REGISTRY.read_text())
    selected_names = set(SELECTIONS)
    registry["drafts"] = [item for item in registry["drafts"] if item["name"] not in selected_names] + entries
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    print(f"Staged {len(entries)} exact-name reversible replacements in {rel(DRAFT_ROOT)}")


def preview(name: str, strip_path: Path, sidecar_path: Path, *, mirror: bool = False, slug: str | None = None) -> None:
    sidecar = json.loads(sidecar_path.read_text())
    image = Image.open(strip_path).convert("RGBA")
    frame_width = sidecar["w"] * sidecar["density"]
    frames = []
    for index in range(sidecar["frames"]):
        frame = image.crop((index * frame_width, 0, (index + 1) * frame_width, image.height))
        if mirror:
            frame = ImageOps.mirror(frame)
        canvas = Image.new("RGBA", (frame.width * 2, frame.height * 2), (244, 236, 214, 255))
        canvas.alpha_composite(frame.resize(canvas.size, Image.Resampling.NEAREST))
        frames.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    destination = ROOT / "docs/floor-asset-catalogue" / f"{slug or name.replace('_', '-')}-preview.gif"
    duration = round(1000 / sidecar["fps"])
    frames[0].save(destination, save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=2, optimize=False)


def promote() -> None:
    registry = json.loads(REGISTRY.read_text())
    by_name = {item["name"]: item for item in registry["drafts"]}
    for name in SELECTIONS:
        item = by_name.get(name)
        if not item:
            raise RuntimeError(f"missing staged registry entry for {name}")
        register_path = ROOT / item["register"]
        record = json.loads(register_path.read_text())
        draft_strip = ROOT / record["draft"]["strip"]
        draft_sidecar = ROOT / record["draft"]["sidecar"]
        verify_gutters(draft_strip, draft_sidecar)
        for stale in (*RAW.glob(f"{name}_f*.png"), *RAW.glob(f"{name}_f*.json")):
            stale.unlink()
        promoted_strip = RAW / draft_strip.name
        promoted_sidecar = RAW / draft_sidecar.name
        shutil.copyfile(draft_strip, promoted_strip)
        shutil.copyfile(draft_sidecar, promoted_sidecar)
        record["status"] = "promoted-review-draft"
        record["promotion"] = {
            "strip": rel(promoted_strip), "stripSha256": sha256(promoted_strip),
            "sidecar": rel(promoted_sidecar), "sidecarSha256": sha256(promoted_sidecar),
        }
        promoted_runtime = PUBLIC / f"{name}.png"
        if promoted_runtime.exists():
            record["promotion"].update({
                "runtime": rel(promoted_runtime),
                "runtimeSha256": sha256(promoted_runtime),
            })
        register_path.write_text(json.dumps(record, indent=2) + "\n")
        item["status"] = "promoted-review-draft"
        item["label"] = "Previous version"
        if name == "keeper_clear_snow":
            preview(name, promoted_strip, promoted_sidecar, slug="keeper-clear-snow-right")
            preview(name, promoted_strip, promoted_sidecar, mirror=True, slug="keeper-clear-snow-left")
        else:
            preview(name, promoted_strip, promoted_sidecar)
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    print(f"Promoted {len(SELECTIONS)} selected replacements; previous versions remain in {rel(DRAFT_ROOT)}")


def stage_landing_dependency() -> None:
    """Stage the drift-to-landing hand-off required by the selected drift canvas."""
    spec = LANDING_DEPENDENCY
    name = spec["name"]
    target = DRAFT_ROOT / name
    source_dir, previous_dir, candidate_dir = target / "source", target / "previous", target / "candidate"
    for directory in (source_dir, previous_dir, candidate_dir):
        directory.mkdir(parents=True, exist_ok=True)
    source = ROOT / spec["source"]
    stored_source = source_dir / source.name
    shutil.copyfile(source, stored_source)
    if sha256(stored_source) != spec["sourceSha256"]:
        raise RuntimeError("parachute landing source hash mismatch")
    old_raw, old_sidecar = current_raw(name, "png"), current_raw(name, "json")
    old_runtime = PUBLIC / f"{name}.png"
    for source_file in (old_raw, old_sidecar, old_runtime):
        shutil.copyfile(source_file, previous_dir / source_file.name)
    candidate_strip = candidate_dir / f"{spec['raw']}.png"
    candidate_sidecar = candidate_dir / f"{spec['raw']}.json"
    candidate_strip.write_bytes(git_blob(f"art/raw/keeper-first-batch/{spec['raw']}.png"))
    candidate_sidecar.write_bytes(git_blob(f"art/raw/keeper-first-batch/{spec['raw']}.json"))
    boxes = verify_gutters(candidate_strip, candidate_sidecar)
    contact_sheet = target / "evidence/final-candidate-frames.jpg"
    write_contact_sheet(candidate_strip, candidate_sidecar, contact_sheet)
    record = {
        "draftId": f"{DRAFT_ID}-{name}", "animation": name,
        "status": "active-review-draft", "label": "Dependent route bridge",
        "selection": "The selected parachute drift changes the open-canopy canvas and anchor; this deterministic landing derivative preserves the byte-exact drift-to-landing hand-off.",
        "canonical": {
            "strip": rel(previous_dir / old_raw.name), "stripSha256": sha256(previous_dir / old_raw.name),
            "runtime": rel(previous_dir / old_runtime.name), "runtimeSha256": sha256(previous_dir / old_runtime.name),
            "sidecar": rel(previous_dir / old_sidecar.name), "sidecarSha256": sha256(previous_dir / old_sidecar.name),
        },
        "draft": {
            "source": rel(stored_source), "sourceSha256": sha256(stored_source),
            "strip": rel(candidate_strip), "stripSha256": sha256(candidate_strip),
            "sidecar": rel(candidate_sidecar), "sidecarSha256": sha256(candidate_sidecar),
            "frameEvidence": [{"frame": index + 1, "alphaBox": box} for index, box in enumerate(boxes)],
            "evidence": [rel(contact_sheet)],
        },
        "qualification": "This is a required route-contact derivative, not an independently selected redraw.",
        "rollback": "Restore the three files in previous/ together with keeper_parachute_drift's previous version.",
    }
    register = target / "draft-register.json"
    register.write_text(json.dumps(record, indent=2) + "\n")
    registry = json.loads(REGISTRY.read_text())
    registry["drafts"] = [item for item in registry["drafts"] if item["name"] != name]
    registry["drafts"].append({"name": name, "status": "active-review-draft", "label": record["label"], "register": rel(register)})
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    print("Staged keeper_parachute_landing dependent route bridge")


def promote_landing_dependency() -> None:
    name = LANDING_DEPENDENCY["name"]
    registry = json.loads(REGISTRY.read_text())
    item = next(item for item in registry["drafts"] if item["name"] == name)
    register_path = ROOT / item["register"]
    record = json.loads(register_path.read_text())
    draft_strip, draft_sidecar = ROOT / record["draft"]["strip"], ROOT / record["draft"]["sidecar"]
    verify_gutters(draft_strip, draft_sidecar)
    for stale in (*RAW.glob(f"{name}_f*.png"), *RAW.glob(f"{name}_f*.json")):
        stale.unlink()
    promoted_strip, promoted_sidecar = RAW / draft_strip.name, RAW / draft_sidecar.name
    shutil.copyfile(draft_strip, promoted_strip)
    shutil.copyfile(draft_sidecar, promoted_sidecar)
    runtime = PUBLIC / f"{name}.png"
    record["status"] = "promoted-review-draft"
    record["promotion"] = {
        "strip": rel(promoted_strip), "stripSha256": sha256(promoted_strip),
        "sidecar": rel(promoted_sidecar), "sidecarSha256": sha256(promoted_sidecar),
        **({"runtime": rel(runtime), "runtimeSha256": sha256(runtime)} if runtime.exists() else {}),
    }
    register_path.write_text(json.dumps(record, indent=2) + "\n")
    item["status"], item["label"] = "promoted-review-draft", "Previous version"
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    preview(name, promoted_strip, promoted_sidecar)
    print("Promoted keeper_parachute_landing dependent route bridge")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("stage", "promote", "stage-landing", "promote-landing"))
    args = parser.parse_args()
    if args.action == "stage":
        stage()
    elif args.action == "promote":
        promote()
    elif args.action == "stage-landing":
        stage_landing_dependency()
    else:
        promote_landing_dependency()


if __name__ == "__main__":
    main()
