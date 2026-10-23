#!/usr/bin/env python3
"""Build exact-size fitted kitchen proofs and light-only animation layers."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-warm-ligne-claire-family-2026-10-24-v4-on-food-corrected.png"
OUT = ROOT / "art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4"
CANDIDATES = OUT / "candidates"
EVIDENCE = OUT / "evidence"

NAMES = ("cupboard", "drawers", "sink", "dishwasher", "oven", "fridge")
STATES = ("off", "on", "broken")
X_BOUNDS = (65, 293, 521, 749, 977, 1205, 1433)
Y_BOUNDS = {
    "off": (71, 283),
    "on": (352, 566),
    "broken": (631, 842),
}
BODY_SIZE = (84, 74)
ANIMATION_CELL = (92, 82)
FRAME_COUNT = 40
FPS = 4


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def crop_body(source: Image.Image, state: str, index: int) -> Image.Image:
    y0, y1 = Y_BOUNDS[state]
    crop = source.crop((X_BOUNDS[index], y0, X_BOUNDS[index + 1], y1))
    return crop.resize(BODY_SIZE, Image.Resampling.LANCZOS).convert("RGBA")


def dark_lamp_patch(off_dishwasher: Image.Image) -> Image.Image:
    # First Off lamp is the authority for all three identical unlit lenses.
    return off_dishwasher.crop((10, 13, 20, 23))


def fix_dark_dishwasher_lamps(image: Image.Image, patch: Image.Image) -> Image.Image:
    fixed = image.copy()
    for left in (10, 19, 28):
        fixed.alpha_composite(patch, (left, 13))
    return fixed


def darken_oven_cavity(image: Image.Image) -> Image.Image:
    result = image.copy()
    pixels = result.load()
    # The open door begins below this registered cavity patch.  Darkening only
    # this rectangle leaves the failed dial, door and all cabinet pixels exact.
    for y in range(25, 51):
        for x in range(8, 76):
            r, g, b, a = pixels[x, y]
            if a:
                pixels[x, y] = (int(r * 0.42), int(g * 0.40), int(b * 0.44), a)
    return result


def irregular_schedule(seed: int, channels: int) -> list[list[bool]]:
    rng = random.Random(seed)
    schedules: list[list[bool]] = []
    for channel in range(channels):
        values: list[bool] = []
        on = True
        while len(values) < FRAME_COUNT:
            run = rng.randint(1, 5 if on else 3)
            values.extend([on] * run)
            on = not on
        schedules.append(values[:FRAME_COUNT])
    return schedules


def layer_strip(frames: list[Image.Image], path: Path) -> None:
    strip = Image.new("RGBA", (ANIMATION_CELL[0] * len(frames), ANIMATION_CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * ANIMATION_CELL[0], 0))
    strip.save(path, optimize=True)


def preview_gif(base: Image.Image, overlays: list[Image.Image], path: Path) -> None:
    frames = []
    for overlay in overlays:
        composed = Image.new("RGBA", ANIMATION_CELL, (0, 0, 0, 0))
        composed.alpha_composite(base, (4, 4))
        composed.alpha_composite(overlay)
        frames.append(composed.resize((ANIMATION_CELL[0] * 4, ANIMATION_CELL[1] * 4), Image.Resampling.NEAREST))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=250, loop=0, disposal=2)


def build_contact_sheet(cells: dict[str, dict[str, Image.Image]]) -> Image.Image:
    scale = 4
    margin = 28
    label_h = 18
    tile_w = BODY_SIZE[0] * scale
    tile_h = BODY_SIZE[1] * scale
    sheet = Image.new("RGB", (margin * 2 + tile_w * 6, margin * 2 + (tile_h + label_h) * 3), (249, 246, 232))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row, state in enumerate(STATES):
        y = margin + row * (tile_h + label_h)
        for col, name in enumerate(NAMES):
            x = margin + col * tile_w
            image = cells[state][name].convert("RGB").resize((tile_w, tile_h), Image.Resampling.NEAREST)
            sheet.paste(image, (x, y))
            draw.text((x + 4, y + tile_h + 3), f"{state.upper()} {name} 84x74", font=font, fill=(11, 29, 42))
    return sheet


def main() -> None:
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGB")
    assert source.size == (1536, 1024)
    assert tuple(b - a for a, b in zip(X_BOUNDS, X_BOUNDS[1:])) == (228,) * 6

    cells: dict[str, dict[str, Image.Image]] = {state: {} for state in STATES}
    for state in STATES:
        state_dir = CANDIDATES / state
        state_dir.mkdir(parents=True, exist_ok=True)
        for index, name in enumerate(NAMES):
            cells[state][name] = crop_body(source, state, index)

    dark_patch = dark_lamp_patch(cells["off"]["dishwasher"])
    cells["off"]["dishwasher"] = fix_dark_dishwasher_lamps(cells["off"]["dishwasher"], dark_patch)
    broken_dishwasher_lit = cells["broken"]["dishwasher"].copy()
    cells["broken"]["dishwasher"] = fix_dark_dishwasher_lamps(broken_dishwasher_lit, dark_patch)

    broken_oven_lit = cells["broken"]["oven"].copy()
    cells["broken"]["oven"] = darken_oven_cavity(broken_oven_lit)

    hashes: dict[str, dict[str, str]] = {state: {} for state in STATES}
    for state in STATES:
        for name in NAMES:
            path = CANDIDATES / state / f"{name}-{state}-84x74.png"
            cells[state][name].save(path, optimize=True)
            hashes[state][name] = sha256(path)

    # Dishwasher: static Broken base has three dark lenses.  Each transparent
    # frame replaces only the independently active lenses with exact red art.
    dishwasher_schedule = irregular_schedule(47031, 3)
    red_patches = [broken_dishwasher_lit.crop((left, 13, left + 10, 23)) for left in (10, 19, 28)]
    dishwasher_frames: list[Image.Image] = []
    for frame_index in range(FRAME_COUNT):
        layer = Image.new("RGBA", ANIMATION_CELL, (0, 0, 0, 0))
        for channel, left in enumerate((10, 19, 28)):
            if dishwasher_schedule[channel][frame_index]:
                layer.alpha_composite(red_patches[channel], (4 + left, 4 + 13))
        dishwasher_frames.append(layer)
    dishwasher_strip = CANDIDATES / "dishwasher-broken-red-lights-f40.png"
    layer_strip(dishwasher_frames, dishwasher_strip)
    preview_gif(cells["broken"]["dishwasher"], dishwasher_frames, EVIDENCE / "dishwasher-broken-red-lights-preview.gif")

    # Oven: static Broken base is dark.  Lit frames replace only the registered
    # cavity patch with the exact warm-lit source pixels.
    oven_schedule = irregular_schedule(47047, 1)[0]
    lit_cavity = broken_oven_lit.crop((8, 25, 76, 51))
    oven_frames: list[Image.Image] = []
    for lit in oven_schedule:
        layer = Image.new("RGBA", ANIMATION_CELL, (0, 0, 0, 0))
        if lit:
            layer.alpha_composite(lit_cavity, (4 + 8, 4 + 25))
        oven_frames.append(layer)
    oven_strip = CANDIDATES / "oven-broken-cavity-light-f40.png"
    layer_strip(oven_frames, oven_strip)
    preview_gif(cells["broken"]["oven"], oven_frames, EVIDENCE / "oven-broken-cavity-light-preview.gif")

    contact = build_contact_sheet(cells)
    contact_path = EVIDENCE / "exact-84x74-all-state-contact-sheet.png"
    contact.save(contact_path, optimize=True)

    room_rows = Image.new("RGB", (84 * 6, 74 * 3), (249, 246, 232))
    for row, state in enumerate(STATES):
        for col, name in enumerate(NAMES):
            room_rows.paste(cells[state][name].convert("RGB"), (col * 84, row * 74))
    room_rows.save(EVIDENCE / "exact-six-bay-native-runs.png", optimize=True)

    manifest = {
        "id": "kitchen-warm-ligne-claire-family-2026-10-24-v4",
        "status": "approved_visual_and_geometry_authority",
        "source": {"path": str(SOURCE.relative_to(ROOT)), "sha256": sha256(SOURCE), "dimensions": [1536, 1024]},
        "gameContract": {
            "bodySize": list(BODY_SIZE),
            "bayCount": 6,
            "runWidth": 504,
            "masterBayWidth": 228,
            "masterBayBoundariesX": list(X_BOUNDS),
            "masterBodyRowsY": {state: list(bounds) for state, bounds in Y_BOUNDS.items()},
            "roomSlotOriginsX": [84, 168, 252, 336, 420, 504],
            "roomSlotCentresX": [126, 210, 294, 378, 462, 546],
        },
        "states": hashes,
        "animation": {
            "frameCount": FRAME_COUNT,
            "fps": FPS,
            "cellSize": list(ANIMATION_CELL),
            "dishwasher": {
                "strip": str(dishwasher_strip.relative_to(ROOT)),
                "sha256": sha256(dishwasher_strip),
                "channels": 3,
                "schedules": dishwasher_schedule,
                "scope": "three independently blinking red lenses only",
            },
            "oven": {
                "strip": str(oven_strip.relative_to(ROOT)),
                "sha256": sha256(oven_strip),
                "schedule": oven_schedule,
                "scope": "internal cavity light only; red indicator remains static",
            },
        },
        "evidence": {
            "contactSheet": str(contact_path.relative_to(ROOT)),
            "nativeRuns": str((EVIDENCE / "exact-six-bay-native-runs.png").relative_to(ROOT)),
            "dishwasherPreview": str((EVIDENCE / "dishwasher-broken-red-lights-preview.gif").relative_to(ROOT)),
            "ovenPreview": str((EVIDENCE / "oven-broken-cavity-light-preview.gif").relative_to(ROOT)),
        },
        "production": {"register": False, "promote": False, "runtimeWired": False},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (OUT / "batch-register.json").write_text(
        json.dumps(
            {
                "register": False,
                "promote": False,
                "reason": "Art and exact cabinet geometry are approved; runtime promotion waits for extraction and room wiring.",
            },
            indent=2,
        )
        + "\n"
    )

    print(contact_path)
    print(EVIDENCE / "exact-six-bay-native-runs.png")
    print(dishwasher_strip)
    print(oven_strip)


if __name__ == "__main__":
    main()
