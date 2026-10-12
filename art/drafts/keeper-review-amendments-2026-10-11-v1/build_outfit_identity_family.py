#!/usr/bin/env python3
"""Build reversible exact-name outfit identity amendments from isolated renders."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from collections import deque

from PIL import Image

from build_party_family import contact_sheet, gif_preview


ROOT = Path(__file__).resolve().parents[3]
DRAFT_ROOT = Path(__file__).resolve().parent
RAW = ROOT / "art/raw/keeper-first-batch"
PUBLIC = ROOT / "public/sprites"
GENERATED = DRAFT_ROOT / "generated/outfit-walks"
OUT = DRAFT_ROOT / "drafts"
EVIDENCE = DRAFT_ROOT / "evidence/outfit-identity"
HANDOFF = ROOT / "docs/review/keeper-review-handoff-2026-10-11T221440Z.json"
SOURCE_ALPHA_THRESHOLD = 32
FINAL_ALPHA_THRESHOLD = 128
GUTTER = 2

SPECS = {
    "keeper_bath_enter": ("keeper_bath_enter-v1-neutral.png", 8, "canonical pale skin and neutral side face"),
    "keeper_bath_exit": ("keeper_bath_exit-v1-neutral.png", 8, "canonical pale skin and neutral side face"),
    "keeper_collect_eggs_back": ("keeper_collect_eggs_back-v1.png", 8, "clean canonical rear jumper stripe"),
    "keeper_crouch_work_back": ("keeper_crouch_work_back-v1.png", 8, "clean canonical rear jumper stripe"),
    "keeper_lean_table_back": ("keeper_lean_table_back-v1.png", 8, "canonical upward-ended rear stripe"),
    "keeper_lift_weights_back": ("keeper_lift_weights_back-v1.png", 8, "coherent gym outfit and single barbell"),
    "keeper_parachute_drift": ("keeper_parachute_drift-v1-neutral.png", 8, "fixed character/canopy scale and neutral face"),
    "keeper_pressups_side": ("keeper_pressups_side-v1-neutral.png", 8, "canonical proportions and neutral side face"),
    "keeper_place_cake": ("keeper_place_cake-v1-neutral.png", 8, "coherent cake placement at tabletop height"),
    "keeper_platform_dive": ("keeper_platform_dive-v3-grid-neutral.png", 10, "canonical neutral swimming identity through rotation"),
    "keeper_video_game": ("keeper_video_game-v1-neutral.png", 8, "single 45-degree orientation and visible white controller"),
    "keeper_stairs_down": ("keeper_stairs_down-v1-neutral.png", 8, "canonical beard and restrained side face"),
    "keeper_search_boxes": ("keeper_crouch_work_back-v1.png", 8, "clean canonical rear jumper stripe"),
    "keeper_clear_snow": ("keeper_clear_snow-v1-neutral.png", 8, "canonical beard length and neutral side face"),
    "keeper_meal_from_oven_back": ("keeper_meal_from_oven_back-v1.png", 8, "canonical upward-ended rear stripe"),
    "keeper_meal_place_side": ("keeper_meal_place_side-v2-transparent-neutral.png", 8, "plate settles and remains fixed at standard tabletop height while the side face stays neutral"),
    "keeper_water_plants_back": ("keeper_water_plants_back-v1.png", 8, "canonical rear stripe with stable watering prop"),
    "keeper_water_plants_side": ("keeper_water_plants_side-v1-neutral.png", 8, "rooted feet and canonical neutral beard"),
    "keeper_hot_drink_pickup": ("keeper_hot_drink_pickup-v1-neutral-f7.png", 7, "frame 8 removed and mug starts at tabletop level"),
    "keeper_hot_drink_pour": ("keeper_hot_drink_pour-v1-neutral-f9.png", 9, "mug remains visible and frame 10 is removed"),
    "keeper_put_record": ("keeper_put_record-v1-neutral.png", 8, "one coherent record follows the placement path"),
    "keeper_play_drums_back": ("keeper_play_drums_back-v1.png", 8, "both sticks remain on the correct anatomical side"),
    "keeper_play_guitar_gretsch": ("keeper_play_guitar_gretsch-v1-green-neutral.png", 8, "solid rectangular eye without a white glint and neutral mouth"),
    "keeper_bbq_back": ("keeper_bbq_back-v1.png", 8, "smoke rises behind the body with one rapid flame flash"),
    "keeper_carry_shopping": ("keeper_carry_shopping-v1-neutral.png", 8, "front bag removed from source frames 1 and 7"),
    "keeper_pick_vegetable": ("keeper_pick_vegetable-v1-neutral.png", 8, "canonical beard, size and neutral side face"),
    "keeper_souwester_walk_back": ("keeper_souwester_walk_back-v1.png", 8, "alternating rear gait"),
}

GRID_SOURCES = {"keeper_meal_place_side", "keeper_play_guitar_gretsch"}
CHROMA_KEY_SOURCES = {"keeper_play_guitar_gretsch"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def current(name: str, suffix: str) -> Path:
    matches = sorted(RAW.glob(f"{name}_f*.{suffix}"))
    if len(matches) != 1:
        raise ValueError(f"Expected one canonical {suffix} for {name}, found {matches}")
    return matches[0]


def equal_cells(path: Path, count: int) -> list[Image.Image]:
    source = Image.open(path).convert("RGBA")
    return [source.crop((round(source.width * i / count), 0, round(source.width * (i + 1) / count), source.height)) for i in range(count)]


def chroma_key_connected_background(source: Image.Image) -> Image.Image:
    """Remove only green pixels connected to the image edge.

    Restricting the key to the edge-connected component preserves legitimate
    green food details inside the outlined subject.
    """
    keyed = source.copy()
    pixels = keyed.load()
    width, height = keyed.size
    queue: deque[tuple[int, int]] = deque()
    seen: set[tuple[int, int]] = set()

    def is_key(x: int, y: int) -> bool:
        red, green, blue, alpha = pixels[x, y]
        return alpha > 0 and green > 100 and green > max(red, blue) + 22

    for x in range(width):
        queue.extend(((x, 0), (x, height - 1)))
    for y in range(height):
        queue.extend(((0, y), (width - 1, y)))
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen or not is_key(x, y):
            continue
        seen.add((x, y))
        pixels[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                queue.append((nx, ny))
    return keyed


def source_cells(name: str, path: Path, count: int) -> list[Image.Image]:
    if name not in GRID_SOURCES and name != "keeper_platform_dive":
        return equal_cells(path, count)
    source = Image.open(path).convert("RGBA")
    if name in CHROMA_KEY_SOURCES:
        source = chroma_key_connected_background(source)
    columns, rows = (4, 2) if name in GRID_SOURCES else (5, 2)
    cells = []
    for row in range(rows):
        for column in range(columns):
            cells.append(source.crop((
                round(source.width * column / columns),
                round(source.height * row / rows),
                round(source.width * (column + 1) / columns),
                round(source.height * (row + 1) / rows),
            )))
    return cells


def crop_foreground(cell: Image.Image) -> Image.Image:
    mask = cell.getchannel("A").point(lambda value: 255 if value >= SOURCE_ALPHA_THRESHOLD else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("Source cell contains no foreground")
    crop = cell.crop(bbox)
    # Image-model sheets occasionally contain a few detached edge pixels from
    # an adjacent source cell. Retain every substantial component but reject
    # tiny, ambiguous fragments before normalization.
    alpha = crop.getchannel("A")
    pixels = alpha.load()
    seen: set[tuple[int, int]] = set()
    components: list[list[tuple[int, int]]] = []
    for y in range(crop.height):
        for x in range(crop.width):
            if pixels[x, y] < SOURCE_ALPHA_THRESHOLD or (x, y) in seen:
                continue
            stack = [(x, y)]
            seen.add((x, y))
            component: list[tuple[int, int]] = []
            while stack:
                px, py = stack.pop()
                component.append((px, py))
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if 0 <= nx < crop.width and 0 <= ny < crop.height and (nx, ny) not in seen and pixels[nx, ny] >= SOURCE_ALPHA_THRESHOLD:
                        seen.add((nx, ny))
                        stack.append((nx, ny))
            components.append(component)
    if not components:
        raise ValueError("Source crop contains no connected foreground")
    cutoff = max(12, round(max(map(len, components)) * 0.02))
    cleaned = crop.copy()
    clean_alpha = cleaned.getchannel("A")
    clean_pixels = clean_alpha.load()
    for component in components:
        if len(component) < cutoff:
            for x, y in component:
                clean_pixels[x, y] = 0
    cleaned.putalpha(clean_alpha)
    cleaned_bbox = cleaned.getchannel("A").getbbox()
    if cleaned_bbox is None:
        raise ValueError("Detached-fragment cleanup removed all foreground")
    return cleaned.crop(cleaned_bbox)


def main() -> None:
    reviews = {item["name"]: item for item in json.loads(HANDOFF.read_text())["review"]["reviews"]}
    manifest = {"family": "outfit-identity", "faceRule": "closed or hidden mouth; no generic grin", "animations": {}}
    for name, (source_name, frame_count, qualification) in SPECS.items():
        canonical_strip = current(name, "png")
        canonical_sidecar = current(name, "json")
        canonical_runtime = PUBLIC / f"{name}.png"
        sidecar = json.loads(canonical_sidecar.read_text())
        source = GENERATED / source_name
        cells = source_cells(name, source, frame_count)
        source_bboxes = []
        for cell in cells:
            bbox = cell.getchannel("A").point(lambda value: 255 if value >= SOURCE_ALPHA_THRESHOLD else 0).getbbox()
            if bbox is None:
                raise ValueError(f"{name} contains an empty source cell")
            source_bboxes.append(bbox)
        crops = [crop_foreground(cell) for cell in cells]
        size = (sidecar["w"] * sidecar["density"], sidecar["h"] * sidecar["density"])
        if name == "keeper_trampoline_front":
            source_top = min(bbox[1] for bbox in source_bboxes)
            source_bottom = max(bbox[3] for bbox in source_bboxes)
            scale = min(
                (size[0] - 2 * GUTTER) / max(crop.width for crop in crops),
                (size[1] - 2 * GUTTER) / (source_bottom - source_top),
            )
        else:
            scale = min(
                (size[0] - 2 * GUTTER) / max(crop.width for crop in crops),
                (size[1] - 2 * GUTTER) / max(crop.height for crop in crops),
            )
        frames = []
        frame_evidence = []
        for index, crop in enumerate(crops):
            pose = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.Resampling.LANCZOS)
            pose.putalpha(pose.getchannel("A").point(lambda value: 255 if value >= FINAL_ALPHA_THRESHOLD else 0))
            canvas = Image.new("RGBA", size, (0, 0, 0, 0))
            x = round((size[0] - pose.width) / 2)
            if name == "keeper_trampoline_front":
                y = GUTTER + round((source_bboxes[index][1] - source_top) * scale)
            else:
                y = size[1] - GUTTER - pose.height
            canvas.alpha_composite(pose, (x, y))
            bbox = canvas.getchannel("A").getbbox()
            if bbox is None or bbox[0] < GUTTER or bbox[1] < GUTTER or bbox[2] > size[0] - GUTTER or bbox[3] > size[1] - GUTTER:
                raise ValueError(f"{name} frame {index + 1} violates safety gutter: {bbox} in {size}")
            frames.append(canvas)
            frame_evidence.append({"frame": index + 1, "alphaBox": list(bbox), "opaqueBorderPixelCount": 0})

        # Walking sources deliberately include matching neutral endpoints; the
        # turn keeps its distinct rear endpoint and is not forced into a loop.
        if "walk" in name or name in {
            "keeper_collect_eggs_back", "keeper_crouch_work_back",
            "keeper_lean_table_back", "keeper_lift_weights_back",
            "keeper_parachute_drift", "keeper_pressups_side",
            "keeper_video_game", "keeper_search_boxes",
            "keeper_clear_snow", "keeper_water_plants_back", "keeper_water_plants_side",
            "keeper_lift_button_front", "keeper_water_plants_front",
            "keeper_play_drums_back",
            "keeper_bbq_back", "keeper_carry_shopping", "keeper_trampoline_front",
        }:
            frames[-1] = frames[0].copy()
            frame_evidence[-1]["alphaBox"] = frame_evidence[0]["alphaBox"]

        review = reviews[name]
        draft_dir = OUT / name
        evidence_dir = EVIDENCE / name
        draft_dir.mkdir(parents=True, exist_ok=True)
        evidence_dir.mkdir(parents=True, exist_ok=True)
        strip = Image.new("RGBA", (size[0] * len(frames), size[1]), (0, 0, 0, 0))
        for index, frame in enumerate(frames):
            strip.alpha_composite(frame, (index * size[0], 0))
        strip_path = draft_dir / f"{name}_f{len(frames)}.png"
        sidecar_path = draft_dir / f"{name}_f{len(frames)}.json"
        strip.save(strip_path)
        sidecar["frames"] = len(frames)
        sidecar["fps"] = review["animationFps"]
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
            "selection": "Exact-name review amendment only; requires separate explicit promotion.",
            "canonical": {"strip": rel(canonical_strip), "stripSha256": sha256(canonical_strip), "runtime": rel(canonical_runtime), "runtimeSha256": sha256(canonical_runtime), "sidecar": rel(canonical_sidecar), "sidecarSha256": sha256(canonical_sidecar)},
            "draft": {"source": rel(source), "sourceSha256": sha256(source), "strip": rel(strip_path), "stripSha256": sha256(strip_path), "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path), "frameEvidence": frame_evidence, "evidence": [rel(contact), rel(gif)], "fixedSourceScale": scale, "normalization": "equal source cells; one fixed source scale; binary final alpha; bottom-centred in the canonical canvas; two-pixel gutter"},
            "qualification": f"Coherent full-character render; {qualification}. No body-part transplant.",
            "rollback": "Discard this exact-name draft directory and registry entry; canonical and earlier draft assets are unchanged.",
        }
        register_path = draft_dir / "draft-register.json"
        register_path.write_text(json.dumps(register, indent=2) + "\n")
        manifest["animations"][name] = {"register": rel(register_path), "canonicalStripSha256": sha256(canonical_strip), "draftStripSha256": sha256(strip_path), "fixedSourceScale": scale}
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(SPECS)} reversible outfit-identity drafts")


if __name__ == "__main__":
    main()
