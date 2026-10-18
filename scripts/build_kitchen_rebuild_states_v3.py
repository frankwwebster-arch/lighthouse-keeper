#!/usr/bin/env python3
"""Build Kitchen Rebuild V3: corrected artwork and effect placement data."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-states-2026-10-18-v3"
V2_RAW = ROOT / "art/raw/kitchen-rebuild-states-2026-10-18-v2"
V2_SOURCE = ROOT / "art/source/kitchen-rebuild-states-2026-10-18-v2/generated"
BIN_V28 = ROOT / "art/raw/kitchen-bin-states-2026-10-18-v28"
BIN_V31 = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v31"
SOURCE = ROOT / "art/source" / SET / "generated"
EFFECT_SOURCE = SOURCE / "user-approved-broken-effects.png"
TABLE_SOURCE = SOURCE / "canon-height-table-chair-source.png"
BROKEN_OBJECT_SOURCE = V2_SOURCE / "broken-object-amendments-v1.png"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-states-v3"
ASSETS = PUBLIC / "assets"
ROOM, FX_CELL, FRAMES, FPS = (772, 224), (120, 144), 40, 4
BAYS = ("fridge", "kettle", "toaster", "oven", "bowl", "basin")
SOURCE_HASHES = {
    EFFECT_SOURCE: "75899da25b94494545263afbd49b17663c93442725d6043e9bb9782f1f1c41ee",
    TABLE_SOURCE: "6e60ddfe6ba9c205618dbdb4404f6f4b31d2a612ae5b884482ae07ff7b6086a1",
    BROKEN_OBJECT_SOURCE: "8a3f278218711a4684e9fdc7bdf318d19af29d8d768342ed5c7def4a53a141d8",
}

# Starting suggestions only. The workbench can move, resize and crop each one.
FX = {
    "kettle-on-steam": {"asset": "kettle", "state": "on", "origin": [130, -4], "size": [120, 144], "sfx": "kitchen_kettle_boiling_steam_loop"},
    "toaster-on-heat": {"asset": "toaster", "state": "on", "origin": [234, -8], "size": [120, 144], "sfx": "kitchen_toaster_heat_hum_loop"},
    "basin-on-flow": {"asset": "basin", "state": "on", "origin": [499, 48], "size": [84, 100], "sfx": "kitchen_basin_gentle_flow_loop"},
    "fridge-broken-drip": {"asset": "fridge", "state": "broken", "origin": [44, 80], "size": [120, 144], "sfx": "kitchen_fridge_slow_drip_loop"},
    "kettle-broken-steam": {"asset": "kettle", "state": "broken", "origin": [145, -38], "size": [120, 144], "sfx": "kitchen_kettle_broken_pressure_hiss_loop"},
    "toaster-broken-smoke": {"asset": "toaster", "state": "broken", "origin": [234, -24], "size": [120, 144], "sfx": "kitchen_toaster_burnt_smoke_crackle_loop"},
    "oven-broken-smoke": {"asset": "oven", "state": "broken", "origin": [311, 28], "size": [132, 158], "sfx": "kitchen_oven_broken_smoke_hiss_loop"},
    "oven-broken-flicker": {"asset": "oven", "state": "broken", "origin": [318, 74], "size": [120, 144], "sfx": "kitchen_oven_broken_warning_flicker_loop"},
    "basin-broken-spray": {"asset": "basin", "state": "broken", "origin": [482, -12], "size": [120, 144], "sfx": "kitchen_basin_broken_upward_spray_loop"},
    "bin-broken-smell": {"asset": "bin", "state": "broken", "origin": [-16, 44], "size": [120, 144], "sfx": "kitchen_bin_stench_miasma_loop"},
}
OBJECT_ORIGINS = {
    **{f"{asset}-standard": [84 + i * 84, 98] for i, asset in enumerate(BAYS)},
    "fridge-on": [84, 98], "kettle-on": [168, 98], "toaster-on": [252, 98], "oven-on": [336, 98], "bowl-on": [420, 98], "basin-on": [504, 98],
    "fridge-broken": [44, 105], "kettle-broken": [168, 98], "toaster-broken": [252, 85], "oven-broken": [336, 98], "bowl-broken": [420, 98], "basin-broken": [504, 85],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def clean_alpha(image: Image.Image, threshold: int = 12) -> Image.Image:
    image = image.convert("RGBA")
    image.putalpha(image.getchannel("A").point(lambda value: value if value >= threshold else 0))
    return image


def make_table() -> Image.Image:
    source = clean_alpha(Image.open(TABLE_SOURCE), 16)
    box = source.getchannel("A").getbbox()
    if not box:
        raise RuntimeError("table source is empty")
    # 80px = 20lp. Room y150 top, y177 seat, y208 feet.
    normalized = clean_alpha(source.crop(box).resize((80, 58), Image.Resampling.LANCZOS), 18)
    cell = Image.new("RGBA", (84, 79))
    cell.alpha_composite(normalized, (2, 21))  # cell origin is room (680,129)
    return cell


def extended_broken_cell(index: int) -> Image.Image:
    source = Image.open(BROKEN_OBJECT_SOURCE).convert("RGBA")
    run = Image.new("RGBA", (504, 126))
    segments = (((169, 160, 1714, 289), 42), ((169, 289, 1714, 345), 17), ((169, 345, 1714, 615), 67))
    y = 0
    for crop_box, height in segments:
        part = clean_alpha(source.crop(crop_box)).resize((504, height), Image.Resampling.LANCZOS)
        run.alpha_composite(clean_alpha(part), (0, y)); y += height
    cell = Image.new("RGBA", (84, 133))
    cell.alpha_composite(run.crop((index * 84, 0, (index + 1) * 84, 126)), (0, 7))
    return cell


def crop_effect(box: tuple[int, int, int, int], target: tuple[int, int]) -> Image.Image:
    source = clean_alpha(Image.open(EFFECT_SOURCE), 16).crop(box)
    alpha_box = source.getchannel("A").getbbox()
    if not alpha_box:
        raise RuntimeError(f"empty effect crop {box}")
    return clean_alpha(source.crop(alpha_box).resize(target, Image.Resampling.LANCZOS), 10)


def alpha_scaled(image: Image.Image, factor: float) -> Image.Image:
    result = image.copy()
    result.putalpha(result.getchannel("A").point(lambda a: max(0, min(255, round(a * factor)))))
    return result


def animated_cell(base: Image.Image, frame: int, bottom: int, amplitude: int = 2) -> Image.Image:
    cell = Image.new("RGBA", FX_CELL)
    phase, left, top = frame * math.tau / FRAMES, (FX_CELL[0] - base.width) // 2, bottom - base.height
    for y in range(base.height):
        offset = round(math.sin(phase + y * .071) * amplitude * (1 - y / max(1, base.height)))
        cell.alpha_composite(base.crop((0, y, base.width, y + 1)), (left + offset, top + y))
    return cell


def make_strip(builder) -> Image.Image:
    strip = Image.new("RGBA", (FX_CELL[0] * FRAMES, FX_CELL[1]))
    for frame in range(FRAMES):
        strip.alpha_composite(builder(frame), (frame * FX_CELL[0], 0))
    return strip


def bin_smell_strip() -> Image.Image:
    """Wrap the exact approved 80px V31 frames in the common editable cell."""
    source = Image.open(BIN_V31 / "fx-stench-miasma-f40.png").convert("RGBA")
    strip = Image.new("RGBA", (FX_CELL[0] * FRAMES, FX_CELL[1]))
    for frame in range(FRAMES):
        cell = Image.new("RGBA", FX_CELL)
        cell.alpha_composite(source.crop((frame * 80, 0, frame * 80 + 80, 80)), (20, 60))
        strip.alpha_composite(cell, (frame * 120, 0))
    return strip


def visual_variant(strip: Image.Image, scale_x: float, scale_y: float) -> Image.Image:
    """Create another model while retaining every source frame's painted detail."""
    output = Image.new("RGBA", strip.size)
    for frame in range(FRAMES):
        cell = strip.crop((frame * 120, 0, frame * 120 + 120, 144))
        box = cell.getchannel("A").getbbox()
        if not box:
            continue
        art = cell.crop(box)
        width = max(1, min(112, round(art.width * scale_x)))
        height = max(1, min(136, round(art.height * scale_y)))
        art = art.resize((width, height), Image.Resampling.LANCZOS)
        centre_x, bottom = (box[0] + box[2]) // 2, box[3]
        x, y = max(4, min(116 - width, centre_x - width // 2)), max(4, min(140 - height, bottom - height))
        target = Image.new("RGBA", FX_CELL); target.alpha_composite(clean_alpha(art, 8), (x, y))
        output.alpha_composite(target, (frame * 120, 0))
    return output


def timing_variant(strip: Image.Image, mode: int) -> Image.Image:
    """Re-time flickers without moving either exact lamp anchor."""
    output = Image.new("RGBA", strip.size)
    for frame in range(FRAMES):
        source_frame = (frame * (2 if mode == 1 else 3) + (frame // 7 if mode == 2 else 0)) % FRAMES
        output.alpha_composite(strip.crop((source_frame * 120, 0, source_frame * 120 + 120, 144)), (frame * 120, 0))
    return output


def warning_cell(frame: int, star: Image.Image, glow: Image.Image) -> Image.Image:
    cell = Image.new("RGBA", FX_CELL)
    if frame in {0, 1, 3, 4, 7, 8, 9, 13, 14, 18, 19, 20, 25, 27, 28, 32, 33, 37, 39}:
        cell.alpha_composite(alpha_scaled(star, .72 if frame % 3 else 1), (75, 55))
    if frame in {5, 6, 15, 16, 22, 23, 34, 35}:
        cell.alpha_composite(alpha_scaled(glow, .58 if frame % 2 else .82), (29, 101))
    return cell


def make_effects() -> dict[str, Image.Image]:
    effects = {name: Image.open(V2_RAW / f"fx-{name}-f40.png").convert("RGBA") for name in ("kettle-on-steam", "toaster-on-heat", "basin-on-flow")}
    drip = crop_effect((80, 60, 420, 470), (82, 98))
    white_steam = crop_effect((610, 25, 955, 500), (70, 122))
    thin_smoke = crop_effect((1160, 25, 1465, 500), (62, 116))
    thick_smoke = crop_effect((55, 500, 470, 1000), (88, 132))
    spray = crop_effect((555, 500, 980, 1000), (78, 126))
    star = crop_effect((1070, 540, 1315, 735), (18, 18))
    glow = crop_effect((1240, 650, 1510, 940), (50, 19))
    effects.update({
        "fridge-broken-drip": make_strip(lambda f: animated_cell(alpha_scaled(drip, .80 + .12 * math.sin(f * math.tau / 20)), f, 140, 1)),
        "kettle-broken-steam": make_strip(lambda f: animated_cell(alpha_scaled(white_steam, .78 + .12 * math.sin(f * math.tau / 18)), f, 140, 4)),
        "toaster-broken-smoke": make_strip(lambda f: animated_cell(alpha_scaled(thin_smoke, .76 + .12 * math.sin(f * math.tau / 17)), f, 138, 3)),
        "oven-broken-smoke": make_strip(lambda f: animated_cell(alpha_scaled(thick_smoke, .82 + .10 * math.sin(f * math.tau / 19)), f, 140, 4)),
        "basin-broken-spray": make_strip(lambda f: animated_cell(alpha_scaled(spray, .78 + .10 * math.sin(f * math.tau / 9)), f, 140, 2)),
        "oven-broken-flicker": make_strip(lambda f: warning_cell(f, star, glow)),
        "bin-broken-smell": bin_smell_strip(),
    })
    return effects


def make_models(base_effects: dict[str, Image.Image]) -> dict[str, dict[str, Image.Image]]:
    models = {}
    for family, strip in base_effects.items():
        if family == "oven-broken-flicker":
            models[family] = {"classic": strip, "rapid": timing_variant(strip, 1), "angry": timing_variant(strip, 2)}
        else:
            models[family] = {"classic": strip, "compact": visual_variant(strip, .82, .88), "emphatic": visual_variant(strip, 1.12, 1.06)}
    return models


def compose_room(background: Image.Image, table: Image.Image, cells: dict, states: dict, bin_state: str) -> Image.Image:
    room = background.copy()
    room.alpha_composite(Image.open(BIN_V28 / ("bin-broken-overflowing.png" if bin_state == "broken" else "bin-standard.png")).convert("RGBA"), (8, 149))
    for asset in BAYS:
        state = states[asset]
        room.alpha_composite(cells[asset][state], tuple(OBJECT_ORIGINS[f"{asset}-{state}"]))
    room.alpha_composite(table, (680, 129))
    return room


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_rebuild_states_v3.html").read_text()
    cards = "".join(f'<article><h3>{a.title()} · {s.title()}</h3><div class="cell"><img src="assets/{a}-{s}.png" alt="{a} {s}"></div></article>' for a, variants in catalogue["states"].items() for s in variants)
    options = "".join(f'<option value="{n}">{n.replace("-", " ").title()}</option>' for n in catalogue["effects"])
    return template.replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))).replace("__EFFECT_OPTIONS__", options).replace("__CARDS__", cards)


def main() -> None:
    for path, expected in SOURCE_HASHES.items():
        assert sha(path) == expected, f"source hash changed: {path}"
    # V3 is a disposable draft namespace. Rebuild it from sources so stale
    # output names can never leak into the review/archive manifests.
    for directory in (RAW, DRAFT, PUBLIC):
        if directory.exists(): shutil.rmtree(directory)
    for directory in (RAW, DRAFT, ASSETS): directory.mkdir(parents=True, exist_ok=True)
    states = {"fridge": ["standard", "broken"], "kettle": ["standard", "on", "broken"], "toaster": ["standard", "on", "broken"], "oven": ["standard", "on", "broken"], "bowl": ["standard", "broken"], "basin": ["standard", "on", "broken"]}
    cells = {asset: {state: Image.open(V2_RAW / f"{asset}-{state}.png").convert("RGBA") for state in variants} for asset, variants in states.items()}
    cells["toaster"]["broken"] = extended_broken_cell(2)
    cells["basin"]["broken"] = extended_broken_cell(5)
    table, background = make_table(), Image.open(V2_RAW / "kitchen-background.png").convert("RGBA")
    outputs = {}
    def publish(name: str, image: Image.Image) -> None:
        save(image, RAW / name); copy(RAW / name, ASSETS / name)
        outputs[name] = {"sha256": sha(RAW / name), "pixels": list(image.size)}
    for asset, variants in cells.items():
        for state, image in variants.items(): publish(f"{asset}-{state}.png", image)
    publish("kitchen-background.png", background); publish("table-chair.png", table)
    for source, name in ((BIN_V28 / "bin-standard.png", "bin-standard.png"), (BIN_V28 / "bin-broken-overflowing.png", "bin-broken.png"), (BIN_V31 / "fx-stench-miasma-f40.png", "fx-bin-stench-f40.png"), (BIN_V31 / "fx-slow-flies-f40.png", "fx-bin-flies-f40.png")):
        copy(source, RAW / name); copy(source, ASSETS / name)
        outputs[name] = {"sha256": sha(source), "pixels": list(Image.open(source).size)}
    models, effect_meta, effect_families = make_models(make_effects()), {}, {}
    for family, variants in models.items():
        entries = []
        for model, strip in variants.items():
            name = f"{family}--{model}"; filename = f"fx-{name}-f40.png"; publish(filename, strip)
            effect_meta[name] = {**FX[family], "family": family, "model": model, "file": filename, "frames": FRAMES, "fps": FPS, "durationSeconds": 10, "cellPixels": list(FX_CELL), "reusable": True, "effectOnly": True, "editableTransform": True, "crop": [0, 0, 0, 0]}
            entries.append(name)
        effect_families[family] = {"models": entries, "default": entries[0]}
    standard = {asset: "standard" for asset in BAYS}
    all_on = {"fridge": "standard", "kettle": "on", "toaster": "on", "oven": "on", "bowl": "standard", "basin": "on"}
    broken = {asset: "broken" for asset in BAYS}
    mixed = {"fridge": "broken", "kettle": "on", "toaster": "broken", "oven": "on", "bowl": "broken", "basin": "on"}
    for name, mapping, bin_state in (("kitchen-standard-v3.png", standard, "standard"), ("kitchen-all-on-static.png", all_on, "standard"), ("kitchen-all-broken-static.png", broken, "broken"), ("kitchen-mixed-static.png", mixed, "broken")):
        publish(name, compose_room(background, table, cells, mapping, bin_state))
    catalogue = {
        "set": SET, "version": 3, "status": "effect-placement-workbench-awaiting-review",
        "foundation": {"set": "kitchen-rebuild-foundation-2026-10-18-v1", "immutable": True, "roomPixels": list(ROOM), "bayWidthPixels": 84, "bayCount": 6},
        "method": {"objectArtSeparateFromEffects": True, "userTransformableEffects": True, "transformControls": ["drag", "resize", "crop", "nudge", "local-save", "json-export"], "environmentalEffectsSeparate": True},
        "states": states, "objectOrigins": OBJECT_ORIGINS, "table": {"origin": [680, 129], "widthPixels": 80, "footLineY": 208, "tableTopY": 150, "chairSeatY": 177},
        "effects": effect_meta, "effectFamilies": effect_families, "allOn": {**all_on, "bin": "standard"}, "allBroken": {**broken, "bin": "broken"}, "mixedPreset": {**mixed, "bin": "broken"},
        "sourceProvenance": {"userApprovedBrokenEffects": {"file": str(EFFECT_SOURCE.relative_to(ROOT)), "sha256": sha(EFFECT_SOURCE)}, "generatedTableChair": {"file": str(TABLE_SOURCE.relative_to(ROOT)), "sha256": sha(TABLE_SOURCE), "mode": "built-in image generation", "geometry": "deterministically normalized to canon datums"}},
        "outputs": outputs, "media": list(outputs), "promotion": "none", "runtimeWiring": "unchanged",
    }
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({"set": SET, "status": "awaiting-visual-review-and-exported-effect-placement", "promotion": "none", "runtimeWiring": "unchanged", "rollback": "Delete V3 only; V1 and V2 remain exact."}, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: {len(outputs)} outputs, {len(effect_meta)} transformable effects")


if __name__ == "__main__": main()
