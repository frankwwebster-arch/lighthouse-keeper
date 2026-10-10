#!/usr/bin/env python3
"""Create the user-selected darts review draft without touching production art."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DRAFT_ID = "keeper-darts-user-selected-2026-10-10-v1"
DRAFT_DIR = ROOT / "art/drafts" / DRAFT_ID
SOURCE_COPY = DRAFT_DIR / "source/keeper-darts-user-selected-source.png"
DRAFT_STRIP = DRAFT_DIR / "keeper_darts_user_selected_f14.png"
DRAFT_SIDECAR = DRAFT_DIR / "source/keeper_darts_f14.json"
REGISTER = DRAFT_DIR / "draft-register.json"
REVIEW_DRAFTS = ROOT / "data/keeper_review_drafts.json"
CANONICAL_STRIP = ROOT / "art/raw/keeper-first-batch/keeper_darts_f14.png"
CANONICAL_RUNTIME = ROOT / "public/sprites/keeper_darts.png"
CANONICAL_SIDECAR = ROOT / "art/raw/keeper-first-batch/keeper_darts_f14.json"
EXPECTED_SOURCE_SHA = "ed8fd9e733c4468541f20b4976e75111838f76194c592951ecf6b27211aefa48"
EXPECTED_CANONICAL_STRIP_SHA = "a52db90e64bb9d5389085f8fd3801208bd884f2c486f997d01b6f0d5b50bd974"
EXPECTED_CANONICAL_RUNTIME_SHA = "7469f0ad727751d30214629c007123b47dae1d9bde087915b72b790834dd26f3"
FRAMES = 14
DENSITY = 4
LOGICAL_WIDTH = 56
LOGICAL_HEIGHT = 40
TARGET_WIDTH = LOGICAL_WIDTH * DENSITY
TARGET_HEIGHT = LOGICAL_HEIGHT * DENSITY


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def components(alpha: Image.Image) -> list[tuple[int, tuple[int, int, int, int], list[int]]]:
    """Return 4-connected alpha components with at least 20 source pixels."""
    width, height = alpha.size
    pixels = bytearray(alpha.tobytes())
    found: list[tuple[int, tuple[int, int, int, int], list[int]]] = []
    for start, value in enumerate(pixels):
        if not value:
            continue
        pixels[start] = 0
        pending = deque([start])
        members: list[int] = []
        min_x, min_y, max_x, max_y = width, height, 0, 0
        while pending:
            index = pending.pop()
            members.append(index)
            y, x = divmod(index, width)
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)
            for neighbour in (index - 1, index + 1, index - width, index + width):
                if not 0 <= neighbour < width * height or not pixels[neighbour]:
                    continue
                if neighbour // width != y and neighbour % width != x:
                    continue
                pixels[neighbour] = 0
                pending.append(neighbour)
        if len(members) >= 20:
            found.append((len(members), (min_x, min_y, max_x + 1, max_y + 1), members))
    return found


def extract_frames(source_path: Path) -> tuple[list[Image.Image], list[dict[str, object]], float]:
    """Extract 14 actors and assign detached darts to the nearest actor."""
    source = Image.open(source_path).convert("RGBA")
    alpha = source.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
    found = components(alpha)
    actors = sorted(found, reverse=True)[:FRAMES]
    if len(actors) != FRAMES:
        raise RuntimeError(f"expected {FRAMES} actor components, found {len(actors)}")
    actors.sort(key=lambda item: (
        int((((item[1][1] + item[1][3]) / 2) * 3) / source.height),
        (item[1][0] + item[1][2]) / 2,
    ))
    actor_centres = [((box[0] + box[2]) / 2, (box[1] + box[3]) / 2) for _, box, _ in actors]
    grouped: list[list[int]] = [[] for _ in range(FRAMES)]
    for _, box, members in found:
        centre = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
        nearest = min(
            range(FRAMES),
            key=lambda index: ((centre[0] - actor_centres[index][0]) ** 2 +
                               (centre[1] - actor_centres[index][1]) ** 2),
        )
        grouped[nearest].extend(members)

    bounds: list[tuple[int, int, int, int]] = []
    for members in grouped:
        xs = [index % source.width for index in members]
        ys = [index // source.width for index in members]
        bounds.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    tallest = max(y1 - y0 for _, y0, _, y1 in bounds)
    widest = max(x1 - x0 for x0, _, x1, _ in bounds)
    scale = min((TARGET_HEIGHT - 8) / tallest, (TARGET_WIDTH - 8) / widest)

    frames: list[Image.Image] = []
    evidence: list[dict[str, object]] = []
    for frame_number, (actor, box, members) in enumerate(zip(actors, bounds, grouped), 1):
        _, actor_box, _ = actor
        x0, y0, x1, y1 = box
        crop = source.crop(box)
        mask = bytearray((x1 - x0) * (y1 - y0))
        for index in members:
            y, x = divmod(index, source.width)
            mask[(y - y0) * (x1 - x0) + x - x0] = 255
        crop.putalpha(Image.frombytes("L", crop.size, bytes(mask)))
        resized = crop.resize(
            (max(1, round(crop.width * scale)), max(1, round(crop.height * scale))),
            Image.Resampling.LANCZOS,
        )
        resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))

        actor_centre_x = (actor_box[0] + actor_box[2]) / 2
        actor_bottom = actor_box[3]
        offset_x = round((TARGET_WIDTH / 2) - ((actor_centre_x - x0) * scale))
        offset_y = round((TARGET_HEIGHT - 2) - ((actor_bottom - y0) * scale))
        frame = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
        frame.alpha_composite(resized, (offset_x, offset_y))
        alpha_box = frame.getchannel("A").getbbox()
        if alpha_box is None:
            raise RuntimeError(f"draft frame {frame_number} is empty")
        if alpha_box[0] == 0 or alpha_box[2] == TARGET_WIDTH or alpha_box[1] == 0 or alpha_box[3] == TARGET_HEIGHT:
            raise RuntimeError(f"draft frame {frame_number} has no transparent safety gutter: {alpha_box}")
        frames.append(frame)
        evidence.append({
            "frame": frame_number,
            "sourceActorBox": list(actor_box),
            "sourceOwnedBox": list(box),
            "draftAlphaBox": list(alpha_box),
            "detachedComponentCount": max(0, sum(1 for _, component_box, _ in found if (
                min(range(FRAMES), key=lambda index: (
                    (((component_box[0] + component_box[2]) / 2) - actor_centres[index][0]) ** 2 +
                    (((component_box[1] + component_box[3]) / 2) - actor_centres[index][1]) ** 2
                )) == frame_number - 1
            )) - 1),
        })
    return frames, evidence, scale


def write_strip(frames: list[Image.Image], destination: Path) -> None:
    strip = Image.new("RGBA", (TARGET_WIDTH * FRAMES, TARGET_HEIGHT), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * TARGET_WIDTH, 0))
    strip.save(destination, optimize=False)


def write_evidence(frames: list[Image.Image]) -> list[str]:
    evidence_dir = DRAFT_DIR / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    canonical = Image.open(CANONICAL_STRIP).convert("RGBA")
    draft = Image.open(DRAFT_STRIP).convert("RGBA")
    columns = 7
    comparison = Image.new("RGBA", (TARGET_WIDTH * columns, TARGET_HEIGHT * 4 + 24), (0, 0, 0, 0))
    preview = Image.new("RGBA", (TARGET_WIDTH * columns, TARGET_HEIGHT * 2 + 8), (0, 0, 0, 0))
    for frame in range(FRAMES):
        column = frame % columns
        row = frame // columns
        canonical_frame = canonical.crop((frame * TARGET_WIDTH, 0, (frame + 1) * TARGET_WIDTH, TARGET_HEIGHT))
        draft_frame = draft.crop((frame * TARGET_WIDTH, 0, (frame + 1) * TARGET_WIDTH, TARGET_HEIGHT))
        comparison.alpha_composite(canonical_frame, (column * TARGET_WIDTH, row * (TARGET_HEIGHT + 8)))
        comparison.alpha_composite(draft_frame, (column * TARGET_WIDTH, (row + 2) * (TARGET_HEIGHT + 8)))
        preview.alpha_composite(draft_frame, (column * TARGET_WIDTH, row * (TARGET_HEIGHT + 8)))
    comparison_path = evidence_dir / "keeper_darts_canonical_vs_user_selected_draft.png"
    comparison.save(comparison_path, optimize=False)
    preview_path = evidence_dir / "keeper_darts_user_selected_draft.png"
    preview.save(preview_path, optimize=False)
    return [rel(comparison_path), rel(preview_path)]


def create(source_path: Path) -> None:
    if sha256(source_path) != EXPECTED_SOURCE_SHA:
        raise RuntimeError("the supplied darts reference no longer matches Frank's selected image")
    if sha256(CANONICAL_STRIP) != EXPECTED_CANONICAL_STRIP_SHA:
        raise RuntimeError("canonical raw darts strip changed; refusing to create a draft from another baseline")
    if sha256(CANONICAL_RUNTIME) != EXPECTED_CANONICAL_RUNTIME_SHA:
        raise RuntimeError("canonical runtime darts strip changed; refusing to create a draft from another baseline")

    (DRAFT_DIR / "source").mkdir(parents=True, exist_ok=True)
    SOURCE_COPY.write_bytes(source_path.read_bytes())
    frames, frame_evidence, scale = extract_frames(SOURCE_COPY)
    write_strip(frames, DRAFT_STRIP)

    sidecar = json.loads(CANONICAL_SIDECAR.read_text())
    sidecar["reviewDraft"] = {
        "draftId": DRAFT_ID,
        "label": "Frank-selected draft",
        "sourceSha256": EXPECTED_SOURCE_SHA,
        "canonicalPromotion": False,
        "extraction": "14 largest actor components in reading order; detached darts assigned to the nearest actor; actor centre and floor contact aligned without fitting by full prop bounds",
    }
    DRAFT_SIDECAR.write_text(json.dumps(sidecar, indent=2) + "\n")
    evidence_paths = write_evidence(frames)

    register = {
        "draftId": DRAFT_ID,
        "animation": "keeper_darts",
        "status": "active-review-draft",
        "label": "Frank-selected draft",
        "selection": "Frank identified the attached 14-pose image as a good darts animation and requested that it be put into the review.",
        "canonical": {
            "strip": rel(CANONICAL_STRIP),
            "stripSha256": sha256(CANONICAL_STRIP),
            "runtime": rel(CANONICAL_RUNTIME),
            "runtimeSha256": sha256(CANONICAL_RUNTIME),
            "sidecar": rel(CANONICAL_SIDECAR),
            "sidecarSha256": sha256(CANONICAL_SIDECAR),
        },
        "draft": {
            "source": rel(SOURCE_COPY),
            "sourceSha256": sha256(SOURCE_COPY),
            "strip": rel(DRAFT_STRIP),
            "stripSha256": sha256(DRAFT_STRIP),
            "sidecar": rel(DRAFT_SIDECAR),
            "sidecarSha256": sha256(DRAFT_SIDECAR),
            "frames": FRAMES,
            "canvas": [LOGICAL_WIDTH, LOGICAL_HEIGHT],
            "density": DENSITY,
            "anchor": sidecar["anchor"],
            "scale": scale,
            "frameEvidence": frame_evidence,
            "evidence": evidence_paths,
        },
        "rollback": "Remove this draft directory and its exact-name registry entry; canonical raw/runtime sprites, manifest and immutable review exports are untouched.",
    }
    REGISTER.write_text(json.dumps(register, indent=2) + "\n")
    REVIEW_DRAFTS.write_text(json.dumps({
        "version": 1,
        "drafts": [{
            "name": "keeper_darts",
            "status": "active-review-draft",
            "label": "Frank-selected draft",
            "register": rel(REGISTER),
        }],
    }, indent=2) + "\n")
    print(f"Created {DRAFT_ID}: {FRAMES} isolated frames; canonical sprites untouched")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", type=Path, help="Frank's selected source PNG")
    args = parser.parse_args()
    source = args.source or SOURCE_COPY
    if not source.exists():
        raise SystemExit("supply Frank's selected darts PNG on the first run")
    create(source.resolve())


if __name__ == "__main__":
    main()
