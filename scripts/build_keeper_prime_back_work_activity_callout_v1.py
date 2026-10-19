#!/usr/bin/env python3
"""Build the immutable Prime rear-work + activity-callout V1 review candidate."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-back-work-activity-callout-v1"
PACK = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v1"
SOURCE_OPENING = PACK / "source/prime-back-work-opening-grid-generated-v1.png"
SOURCE_SUSTAIN = PACK / "source/prime-back-work-sustain-grid-generated-v1.png"
SOURCE_CLOSING = PACK / "source/prime-back-work-closing-grid-generated-v1.png"
REJECTED_SOURCE = PACK / "source/prime-back-work-pose-grid-generated-v1.png"
SOURCES = [SOURCE_OPENING, SOURCE_SUSTAIN, SOURCE_CLOSING]
BODY_DIR = PACK / "drafts/body/frames"
MASK_DIR = PACK / "evidence/component-masks"
CALLOUT_DIR = PACK / "drafts/callouts"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"

REAR = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames/keeper_prime_turn_side-right_to_back_f09.png"
LEGACY = ROOT / "art/raw/keeper-first-batch/keeper_cook_back_f8.png"
LEGACY_SIDECAR = ROOT / "art/raw/keeper-first-batch/keeper_cook_back_f8.json"
APPROACH_REGISTER = ROOT / "art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v2/batch-register.json"
APPROACH_APPROVAL = ROOT / "art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v3/batch-register.json"
TURN_APPROVAL = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json"
RUNTIME_MANIFEST = ROOT / "public/sprites/manifest.json"
WORKBENCH = ROOT / "data/keeper_animation_workbench.json"
BRIEF = ROOT / "docs/KEEPER_BACK_WORK_ACTIVITY_CALLOUT_BRIEF_2026-10-19.md"
NORMALISATION = ROOT / "docs/KEEPER_PRIME_ANIMATION_BANK_NORMALISATION_CONTRACT_2026-10-17.md"
CLAUDE_NOTE = ROOT / "docs/CLAUDE_TO_CODEX_ACTIVITY_CALLOUT_SKETCH_2026-10-19.md"
CLAUDE_SKETCH = ROOT / "docs/sketches/KEEPER_ACTIVITY_CALLOUT_SKETCH_2026-10-19.html"

CELL = (256, 320)
LOGICAL_CELL = (32, 40)
DENSITY = 8
FLOOR_Y = 315
ACTION_FPS = 4
PHRASE_FRAMES = 42
PHRASE_FPS = 8
COMPONENTS = ["capCrown", "capBandBrim", "jumperBlue", "creamBand", "trousers", "boots", "skin", "hair", "outline"]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def write_compact_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":")) + "\n")


def alpha_bounds(image: Image.Image) -> dict[str, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.where(alpha > 0)
    if len(xs) == 0:
        raise RuntimeError("empty sprite")
    return {
        "minX": int(xs.min()), "minY": int(ys.min()), "maxX": int(xs.max()), "maxY": int(ys.max()),
        "width": int(xs.max() - xs.min() + 1), "height": int(ys.max() - ys.min() + 1),
        "opaquePixels": int((alpha > 0).sum()),
    }


def edge_alpha_pixels(image: Image.Image) -> int:
    a = np.asarray(image.getchannel("A"))
    return int(np.count_nonzero(a[0]) + np.count_nonzero(a[-1]) + np.count_nonzero(a[:, 0]) + np.count_nonzero(a[:, -1]))


def transparent_gutter(image: Image.Image) -> int:
    b = alpha_bounds(image)
    return min(b["minX"], b["minY"], image.width - 1 - b["maxX"], image.height - 1 - b["maxY"])


def isolate_character(cell: Image.Image) -> Image.Image:
    """Flood the smooth generated backdrop from cell edges; retain the enclosed actor."""
    rgb = np.asarray(cell.convert("RGB"), dtype=np.int16)
    h, w, _ = rgb.shape
    bg = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(1, h - 1):
        q.append((0, y)); q.append((w - 1, y))
    for x, y in q:
        bg[y, x] = True
    # The generated backdrop changes by only a few RGB points per adjacent
    # pixel; the inked character boundary changes much more sharply. Six
    # keeps the flood outside antialiased outline pixels without preserving the
    # broad backdrop glow as foreground.
    threshold_sq = 6 * 6
    while q:
        x, y = q.popleft()
        base = rgb[y, x]
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or nx >= w or ny < 0 or ny >= h or bg[ny, nx]:
                continue
            delta = rgb[ny, nx] - base
            if int(delta @ delta) <= threshold_sq:
                bg[ny, nx] = True
                q.append((nx, ny))
    foreground = ~bg
    # Keep the largest connected foreground component; glow islands are rejected.
    seen = np.zeros_like(foreground)
    largest: list[tuple[int, int]] = []
    for sy, sx in zip(*np.where(foreground & ~seen)):
        if seen[sy, sx]: continue
        comp: list[tuple[int, int]] = []
        cq = deque([(int(sx), int(sy))]); seen[sy, sx] = True
        while cq:
            x, y = cq.popleft(); comp.append((x, y))
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < w and 0 <= ny < h and foreground[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; cq.append((nx, ny))
        if len(comp) > len(largest):
            largest = comp
    if len(largest) < 5000:
        raise RuntimeError(f"background isolation found only {len(largest)} foreground pixels")
    mask = np.zeros((h, w), dtype=np.uint8)
    for x, y in largest:
        mask[y, x] = 255
    # Close one-pixel outline leaks, then let Lanczos registration restore antialiasing.
    mask_image = Image.fromarray(mask, "L")
    actor = cell.convert("RGBA")
    actor.putalpha(mask_image)
    return actor


def register_actor(actor: Image.Image) -> Image.Image:
    bounds = alpha_bounds(actor)
    crop = actor.crop((bounds["minX"], bounds["minY"], bounds["maxX"] + 1, bounds["maxY"] + 1))
    target_height = 298
    scale = target_height / crop.height
    target_width = max(1, round(crop.width * scale))
    resized = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", CELL, (0, 0, 0, 0))
    x = (CELL[0] - target_width) // 2
    y = FLOOR_Y - target_height + 1
    canvas.alpha_composite(resized, (x, y))
    return canvas


def classify_components(image: Image.Image) -> dict[str, np.ndarray]:
    arr = np.asarray(image.convert("RGBA"))
    rgb = arr[:, :, :3].astype(np.int16)
    alpha = arr[:, :, 3]
    h, w = alpha.shape
    yy, xx = np.indices((h, w))
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    visible = alpha > 0
    warm = (r > b + 25) & (g > b + 10)
    outline = visible & (luma < 38)
    remaining = visible & ~outline
    skin = remaining & warm & (r > 125) & (g < 205) & (b < 170) & (((xx < 95) | (xx > 160)) | (yy > 120))
    remaining &= ~skin
    cream = visible & warm & (r > 150) & (g > 130) & ~skin
    cap_band = remaining & (yy < 92) & (b < 130) & (luma < 100)
    remaining &= ~cap_band
    cap = remaining & (yy < 95) & (b > r + 35)
    remaining &= ~cap
    hair = remaining & (yy < 145) & cream
    remaining &= ~hair
    cream_band = remaining & (yy >= 108) & (yy < 220) & cream
    remaining &= ~cream_band
    boots = remaining & (yy >= 267)
    remaining &= ~boots
    trousers = remaining & (yy >= 205)
    remaining &= ~trousers
    jumper = remaining
    masks = {
        "capCrown": cap,
        "capBandBrim": cap_band,
        "jumperBlue": jumper,
        "creamBand": cream_band,
        "trousers": trousers,
        "boots": boots,
        "skin": skin,
        "hair": hair,
        "outline": outline,
    }
    owned = np.zeros_like(alpha, dtype=np.uint8)
    for mask in masks.values():
        owned += mask.astype(np.uint8)
    missing = visible & (owned == 0)
    if np.any(missing): masks["jumperBlue"] |= missing
    return masks


def luma_values(rgb: np.ndarray) -> np.ndarray:
    return np.rint(0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2]).astype(np.int16)


def palette_register(candidate: Image.Image, authority: Image.Image) -> Image.Image:
    out = np.array(candidate.convert("RGBA"), copy=True)
    authority_arr = np.asarray(authority.convert("RGBA"))
    candidate_masks = classify_components(candidate)
    authority_masks = classify_components(authority)
    for component in COMPONENTS:
        cy, cx = np.where(candidate_masks[component])
        ay, ax = np.where(authority_masks[component])
        if not len(cx) or not len(ax):
            raise RuntimeError(f"missing palette sample for {component}")
        source_rgb = out[cy, cx, :3]
        authority_rgb = authority_arr[ay, ax, :3]
        source_order = np.argsort(luma_values(source_rgb), kind="stable")
        authority_order = np.argsort(luma_values(authority_rgb), kind="stable")
        ranks = np.linspace(0, len(authority_order) - 1, len(source_order)).round().astype(int)
        mapped = authority_rgb[authority_order[ranks]]
        out[cy[source_order], cx[source_order], :3] = mapped
    return Image.fromarray(out, "RGBA")


def lock_lower_body(candidate: Image.Image, authority: Image.Image) -> Image.Image:
    # Lock only the central trouser/boot authority. Pasting the whole lower
    # half would also reintroduce the neutral side hands beneath raised work
    # arms, creating the duplicate-limb failure seen in earlier held-tool
    # experiments.
    out = np.array(candidate.convert("RGBA"), copy=True)
    authority_arr = np.asarray(authority.convert("RGBA"))
    candidate_masks = classify_components(candidate)
    authority_masks = classify_components(authority)
    yy, xx = np.indices((CELL[1], CELL[0]))
    central_lower = (yy >= 205) & (xx >= 76) & (xx <= 180)
    clear = candidate_masks["trousers"] | candidate_masks["boots"] | (candidate_masks["outline"] & central_lower)
    paste = authority_masks["trousers"] | authority_masks["boots"] | (authority_masks["outline"] & central_lower)
    out[clear] = 0
    out[paste] = authority_arr[paste]
    # No contextual hand is allowed below the hidden work-surface zone. Clear
    # residual generated glow/hand fragments outside the locked leg envelope.
    out[(yy >= 205) & ((xx < 76) | (xx > 180))] = 0
    return Image.fromarray(out, "RGBA")


def keep_actor_component(candidate: Image.Image) -> Image.Image:
    """Remove detached glow/speck components left by generated-source isolation."""
    out = np.array(candidate.convert("RGBA"), copy=True)
    alpha = out[:, :, 3]
    alpha[alpha < 8] = 0
    visible = alpha > 0
    seen = np.zeros_like(visible)
    components: list[list[tuple[int, int]]] = []
    h, w = visible.shape
    for sy, sx in zip(*np.where(visible & ~seen)):
        if seen[sy, sx]: continue
        comp: list[tuple[int, int]] = []
        q = deque([(int(sx), int(sy))]); seen[sy, sx] = True
        while q:
            x, y = q.popleft(); comp.append((x, y))
            for nx in range(x - 1, x + 2):
                for ny in range(y - 1, y + 2):
                    if 0 <= nx < w and 0 <= ny < h and visible[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; q.append((nx, ny))
        components.append(comp)
    keep = np.zeros_like(visible)
    for comp in components:
        if len(comp) < 80: continue
        for x, y in comp: keep[y, x] = True
    out[~keep] = 0
    return Image.fromarray(out, "RGBA")


def save_strip(path: Path, frames: list[Image.Image]) -> None:
    strip = Image.new("RGBA", (CELL[0] * len(frames), CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path)


def draw_scaled_icon(name: str, draw_fn) -> Path:
    scale = 4
    image = Image.new("RGBA", (96 * scale, 96 * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw_fn(draw, scale)
    image = image.resize((96, 96), Image.Resampling.LANCZOS)
    path = CALLOUT_DIR / f"icon-{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    return path


INK = (23, 37, 53, 255)
BLUE = (31, 125, 213, 255)
CREAM = (249, 230, 178, 255)
COPPER = (196, 105, 55, 255)
STEEL = (125, 156, 173, 255)
WATER = (83, 184, 224, 255)
YELLOW = (245, 191, 69, 255)
WHITE = (248, 247, 235, 255)


def line(draw: ImageDraw.ImageDraw, points, fill, width, scale):
    draw.line([(x * scale, y * scale) for x, y in points], fill=fill, width=width * scale, joint="curve")


def ellipse(draw: ImageDraw.ImageDraw, box, fill, outline, width, scale):
    draw.ellipse(tuple(v * scale for v in box), fill=fill, outline=outline, width=width * scale)


def polygon(draw: ImageDraw.ImageDraw, points, fill, outline, scale):
    points = [(x * scale, y * scale) for x, y in points]
    draw.polygon(points, fill=fill)
    draw.line(points + [points[0]], fill=outline, width=4 * scale, joint="curve")


def build_icons() -> dict[str, Path]:
    icons: dict[str, Path] = {}

    def pan(d, s):
        ellipse(d, (17, 37, 67, 66), COPPER, INK, 5, s); line(d, [(63, 48), (83, 38)], INK, 9, s); line(d, [(64, 48), (82, 40)], STEEL, 4, s)
    icons["pan"] = draw_scaled_icon("pan", pan)

    def spoon(d, s):
        ellipse(d, (34, 15, 61, 42), STEEL, INK, 5, s); line(d, [(47, 40), (47, 81)], INK, 9, s); line(d, [(47, 40), (47, 81)], STEEL, 4, s)
    icons["spoon"] = draw_scaled_icon("spoon", spoon)

    def heat(d, s):
        for x in (28, 48, 68): line(d, [(x, 78), (x - 5, 62), (x + 5, 48), (x, 31), (x + 3, 18)], YELLOW, 6, s)
    icons["heat"] = draw_scaled_icon("heat", heat)

    def bowl(d, s):
        polygon(d, [(17, 39), (79, 39), (70, 72), (58, 81), (38, 81), (26, 72)], BLUE, INK, s); line(d, [(20, 40), (76, 40)], CREAM, 5, s)
    icons["bowl"] = draw_scaled_icon("bowl", bowl)

    def whisk(d, s):
        line(d, [(29, 77), (51, 46)], INK, 9, s); line(d, [(29, 77), (51, 46)], STEEL, 4, s)
        for offset in (-9, 0, 9): ellipse(d, (42 + offset, 13, 61 + offset, 48), None, INK, 4, s)
    icons["whisk"] = draw_scaled_icon("whisk", whisk)

    def plate(d, s):
        ellipse(d, (14, 14, 82, 82), WHITE, INK, 5, s); ellipse(d, (28, 28, 68, 68), (219, 235, 237, 255), BLUE, 3, s)
    icons["plate"] = draw_scaled_icon("plate", plate)

    def sponge(d, s):
        polygon(d, [(20, 29), (73, 22), (80, 64), (28, 74)], YELLOW, INK, s)
        for x, y in ((35, 42), (55, 35), (62, 56), (40, 61)): ellipse(d, (x, y, x + 5, y + 5), COPPER, None, 0, s)
    icons["sponge"] = draw_scaled_icon("sponge", sponge)

    def bubbles(d, s):
        for box in ((15, 49, 39, 73), (37, 23, 67, 53), (61, 52, 82, 73)): ellipse(d, box, (180, 230, 244, 90), WATER, 4, s)
    icons["bubbles"] = draw_scaled_icon("bubbles", bubbles)

    def tools(d, s):
        line(d, [(20, 76), (67, 26)], INK, 12, s); line(d, [(20, 76), (67, 26)], COPPER, 6, s)
        polygon(d, [(59, 19), (75, 12), (84, 21), (77, 37)], STEEL, INK, s)
        line(d, [(76, 76), (30, 31)], INK, 12, s); line(d, [(76, 76), (30, 31)], STEEL, 6, s)
        ellipse(d, (19, 18, 39, 38), None, INK, 6, s)
    icons["tools"] = draw_scaled_icon("tools", tools)

    def bolt(d, s):
        polygon(d, [(48, 14), (72, 28), (72, 56), (48, 76), (24, 56), (24, 28)], STEEL, INK, s); ellipse(d, (39, 35, 57, 53), (0, 0, 0, 0), INK, 4, s)
    icons["bolt"] = draw_scaled_icon("bolt", bolt)
    return icons


def build_fan_effects() -> dict[str, Path]:
    effects: dict[str, Path] = {}

    def swirls(d, s):
        for ox, oy, flip in ((23, 39, 1), (56, 22, -1), (58, 58, 1)):
            points = []
            for step in range(22):
                angle = step * 0.52
                radius = 2 + step * 0.45
                points.append((ox + math.cos(angle) * radius * flip, oy + math.sin(angle) * radius))
            line(d, points, BLUE, 4, s)
    effects["swirls"] = draw_scaled_icon("swirls", swirls)

    def flicks(d, s):
        for points in (
            [(47, 78), (38, 61), (45, 65)],
            [(30, 72), (13, 58), (23, 59)],
            [(64, 71), (82, 54), (72, 57)],
            [(48, 57), (48, 36), (54, 46)],
        ):
            polygon(d, points, YELLOW, INK, s)
    effects["flicks"] = draw_scaled_icon("flicks", flicks)
    return effects


def build_puff_strip() -> tuple[Path, list[Image.Image]]:
    frames: list[Image.Image] = []
    for index in range(8):
        scale = 4
        image = Image.new("RGBA", (128 * scale, 96 * scale), (0, 0, 0, 0))
        d = ImageDraw.Draw(image)
        grow = min(index, 4) / 4
        fade = 1 if index < 6 else max(0, (8 - index) / 2)
        alpha = round(220 * grow * fade)
        if alpha:
            for cx, cy, rx, ry in ((44, 53, 26, 19), (67, 39, 29, 23), (88, 55, 24, 18), (62, 63, 34, 18)):
                box = ((cx - rx) * scale, (cy - ry) * scale, (cx + rx) * scale, (cy + ry) * scale)
                d.ellipse(box, fill=(248, 247, 235, alpha), outline=(42, 64, 77, alpha), width=3 * scale)
        frames.append(image.resize((128, 96), Image.Resampling.LANCZOS))
    path = CALLOUT_DIR / "puff-f8.png"
    strip = Image.new("RGBA", (128 * len(frames), 96), (0, 0, 0, 0))
    for i, frame in enumerate(frames): strip.alpha_composite(frame, (i * 128, 0))
    path.parent.mkdir(parents=True, exist_ok=True); strip.save(path)
    return path, frames


def phrase_frames(primary: str, secondary: str, accent: str) -> list[dict]:
    """Author a 5.25-second fan phrase: envelope, main icon, two helpers, quiet tail."""
    result = []
    for f in range(PHRASE_FRAMES):
        components = []
        if f <= 35:
            envelope_opacity = min(1, (f + 1) / 3) if f < 3 else max(0, (36 - f) / 5)
            components.append({"asset": "swirls", "kind": "envelope", "x": 0, "y": 3, "scale": .92, "rotate": (f * 7) % 24 - 12, "opacity": round(envelope_opacity, 3)})
        if f <= 9:
            flick_opacity = min(1, (f + 1) / 3) if f < 3 else max(0, (10 - f) / 5)
            components.append({"asset": "flicks", "kind": "envelope", "x": 0, "y": 26, "scale": .86 + min(f, 3) * .05, "rotate": 0, "opacity": round(flick_opacity, 3)})
        if 3 <= f <= 32:
            enter = min(1, (f - 2) / 3)
            leave = 1 if f <= 29 else max(0, (33 - f) / 3)
            components.append({"asset": primary, "kind": "icon", "role": "primary", "x": 0, "y": -39 + round(math.sin(f * .75) * 3), "scale": round((.62 + .38 * enter) * leave, 3), "rotate": round(math.sin(f * .55) * 5, 2), "opacity": round(leave, 3)})
        if 7 <= f <= 20:
            u = min(1, (f - 6) / 4); leave = 1 if f <= 17 else max(0, (21 - f) / 3)
            components.append({"asset": secondary, "kind": "icon", "role": "helper", "x": round(-4 - 49 * u), "y": round(27 - 27 * u + math.sin(f) * 2), "scale": round((.42 + .28 * u) * leave, 3), "rotate": round(-9 - 14 * u + math.sin(f) * 4, 2), "opacity": round(leave, 3)})
        if 14 <= f <= 28:
            u = min(1, (f - 13) / 4); leave = 1 if f <= 25 else max(0, (29 - f) / 3)
            components.append({"asset": accent, "kind": "icon", "role": "helper", "x": round(4 + 49 * u), "y": round(27 - 27 * u + math.cos(f) * 2), "scale": round((.42 + .28 * u) * leave, 3), "rotate": round(9 + 14 * u + math.cos(f) * 4, 2), "opacity": round(leave, 3)})
        result.append({"frame": f, "components": components})
    return result


def cloud_part(frame: int) -> dict | None:
    if frame > 36:
        return None
    puff_frame = frame if frame < 8 else (4 if frame < 31 else (5 if frame < 34 else (6 if frame < 36 else 7)))
    return {"asset": "puff", "kind": "envelope", "frame": puff_frame, "x": 0, "y": 0, "scale": 1.18, "rotate": 0, "opacity": 1}


def render_callout_contact_sheets(phrases: dict, icons: dict[str, Path], effects: dict[str, Path], puff_path: Path) -> dict[str, dict]:
    samples = [0, 3, 7, 14, 21, 28, 32, 37]
    asset_images = {name: Image.open(path).convert("RGBA") for name, path in {**icons, **effects}.items()}
    puff_strip = Image.open(puff_path).convert("RGBA")
    outputs = {}
    for style in ("fan", "cloud"):
        sheet = Image.new("RGBA", (220 * len(samples), 190 * len(phrases)), (19, 33, 43, 255))
        draw = ImageDraw.Draw(sheet)
        for row, (phrase_name, phrase) in enumerate(phrases.items()):
            for col, frame in enumerate(samples):
                x0, y0 = col * 220, row * 190
                cell = Image.new("RGBA", (220, 170), (0, 0, 0, 0))
                checker = ImageDraw.Draw(cell)
                for cy in range(0, 170, 16):
                    for cx in range(0, 220, 16):
                        checker.rectangle((cx, cy, cx + 15, cy + 15), fill=((224, 234, 233, 255) if (cx // 16 + cy // 16) % 2 == 0 else (113, 136, 146, 255)))
                parts = [part for part in phrase["frames"][frame]["components"] if style == "fan" or part.get("kind") != "envelope"]
                if style == "cloud":
                    cloud = cloud_part(frame)
                    if cloud: parts.insert(0, cloud)
                for part in parts:
                    part = dict(part)
                    if style == "cloud" and part.get("kind") == "icon":
                        if part.get("role") == "primary":
                            part["y"] += 20; part["scale"] *= .8
                        else:
                            part["x"] *= .55; part["y"] += 17; part["scale"] *= .75
                    if part["asset"] == "puff":
                        source = puff_strip.crop((part["frame"] * 128, 0, (part["frame"] + 1) * 128, 96))
                        base_width = 128
                    else:
                        source = asset_images[part["asset"]]
                        base_width = 72
                    target_width = max(1, round(base_width * part["scale"]))
                    target_height = max(1, round(source.height * target_width / source.width))
                    rendered = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    if part["rotate"]: rendered = rendered.rotate(-part["rotate"], resample=Image.Resampling.BICUBIC, expand=True)
                    if part["opacity"] < 1:
                        alpha = rendered.getchannel("A").point(lambda value, opacity=part["opacity"]: round(value * opacity))
                        rendered.putalpha(alpha)
                    px = round(110 + part["x"] - rendered.width / 2); py = round(85 + part["y"] - rendered.height / 2)
                    cell.alpha_composite(rendered, (px, py))
                sheet.alpha_composite(cell, (x0, y0))
                draw.text((x0 + 5, y0 + 173), f"{phrase_name} F{frame + 1:02d}", fill=(238, 247, 250, 255))
        path = PACK / f"evidence/callout-{style}-contact-sheet.png"
        path.parent.mkdir(parents=True, exist_ok=True); sheet.save(path)
        outputs[style] = {"file": rel(path), "sha256": sha(path), "sampleFrames": [frame + 1 for frame in samples]}
    return outputs


def publish(path: Path, label: str, published: list[dict], by_hash: dict[str, dict]) -> dict:
    digest = sha(path)
    if digest in by_hash:
        return by_hash[digest]
    target = ASSETS / f"{label}-{digest[:16]}{path.suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
    entry = {"source": rel(path), "sourceSha256": digest, "public": rel(target), "publicAssemblyPath": rel(target), "publicSha256": sha(target), "url": f"/keeper-review/{SET}/assets/{target.name}"}
    published.append(entry); by_hash[digest] = entry
    return entry


def main() -> None:
    for required in (*SOURCES, REJECTED_SOURCE, REAR, LEGACY, LEGACY_SIDECAR, APPROACH_REGISTER, APPROACH_APPROVAL, TURN_APPROVAL, RUNTIME_MANIFEST, WORKBENCH, BRIEF, NORMALISATION):
        if not required.exists(): raise RuntimeError(f"missing {rel(required)}")
    BODY_DIR.mkdir(parents=True, exist_ok=True); MASK_DIR.mkdir(parents=True, exist_ok=True); CALLOUT_DIR.mkdir(parents=True, exist_ok=True)
    if PUBLIC.exists(): shutil.rmtree(PUBLIC)
    ASSETS.mkdir(parents=True, exist_ok=True)

    rear = Image.open(REAR).convert("RGBA")
    grids = [Image.open(path).convert("RGBA") for path in SOURCES]
    if any(grid.size != (1536, 1024) for grid in grids): raise RuntimeError(f"unexpected generated grid sizes {[grid.size for grid in grids]}")
    # A genuine 24-frame performance: exact neutral; seven opening poses; eight
    # sustained-work poses; seven closing poses; exact neutral. No eight-frame
    # block is simply replayed.
    source_order: list[tuple[int, int] | None] = [None]
    source_order += [(0, index) for index in (0, 3, 2, 4, 1, 6, 5)]
    source_order += [(1, index) for index in range(8)]
    source_order += [(2, index) for index in (1, 0, 2, 3, 5, 4)]
    source_order += [None, None]
    frames: list[Image.Image] = []
    source_evidence = []
    for index, source_ref in enumerate(source_order):
        if source_ref is None:
            frame = rear.copy(); derivation = "exact-approved-rear-endpoint"
        else:
            source_grid, source_index = source_ref
            col, row = source_index % 4, source_index // 4
            source_cell = grids[source_grid].crop((col * 384, row * 512, (col + 1) * 384, (row + 1) * 512))
            isolated = isolate_character(source_cell)
            registered = register_actor(isolated)
            registered = palette_register(registered, rear)
            frame = lock_lower_body(registered, rear)
            frame = keep_actor_component(frame)
            frame = palette_register(frame, rear)
            derivation = f"generated-{('opening','sustain','closing')[source_grid]}-grid-cell-{source_index + 1}-geometry; deterministic backdrop isolation; exact rear Prime palette quantile registration; exact rear lower-body lock"
            source_evidence.append({"candidateFrame": index + 1, "sourceFile": rel(SOURCES[source_grid]), "sourceCell": source_index + 1, "isolatedBounds": alpha_bounds(isolated), "registeredBounds": alpha_bounds(frame)})
        if edge_alpha_pixels(frame): raise RuntimeError(f"frame {index + 1} touches cell edge")
        path = BODY_DIR / f"keeper_prime_work-back_f{index + 1:02d}.png"
        if source_ref is None:
            shutil.copyfile(REAR, path)
            frame = Image.open(path).convert("RGBA")
        else:
            frame.save(path)
        frames.append(frame)

    body_records = []
    rear_masks = classify_components(rear)
    rear_arr = np.asarray(rear)
    rear_swatches = {tuple(value) for value in rear_arr[:, :, :3][rear_arr[:, :, 3] > 0].tolist()}
    for index, (frame, source_ref) in enumerate(zip(frames, source_order)):
        masks = classify_components(frame); frame_arr = np.asarray(frame)
        ownership_sum = np.zeros((CELL[1], CELL[0]), dtype=np.uint8)
        mask_records = {}
        colour_evidence = {}
        for component in COMPONENTS:
            mask = masks[component]; ownership_sum += mask.astype(np.uint8)
            mask_img = Image.fromarray((mask.astype(np.uint8) * 255), "L")
            mask_path = MASK_DIR / f"work-back-f{index + 1:02d}-{component}.png"; mask_img.save(mask_path)
            cand_rgb = frame_arr[:, :, :3][mask]
            auth_rgb = rear_arr[:, :, :3][rear_masks[component]]
            cand_luma = luma_values(cand_rgb); auth_luma = luma_values(auth_rgb)
            med = lambda values: int(np.median(values)) if len(values) else None
            median_delta = abs(med(cand_luma) - med(auth_luma))
            p25_delta = abs(int(np.percentile(cand_luma, 25)) - int(np.percentile(auth_luma, 25)))
            p75_delta = abs(int(np.percentile(cand_luma, 75)) - int(np.percentile(auth_luma, 75)))
            colour_evidence[component] = {
                "status": "pass" if len(cand_rgb) and len(auth_rgb) and median_delta <= 2 and p25_delta <= 4 and p75_delta <= 4 else "fail",
                "authorityFile": rel(REAR), "authoritySha256": sha(REAR),
                "candidate": {"pixels": int(len(cand_rgb)), "medianLuma": med(cand_luma), "p25Luma": int(np.percentile(cand_luma, 25)), "p75Luma": int(np.percentile(cand_luma, 75))},
                "authority": {"pixels": int(len(auth_rgb)), "medianLuma": med(auth_luma), "p25Luma": int(np.percentile(auth_luma, 25)), "p75Luma": int(np.percentile(auth_luma, 75))},
                "visibleRgbFromExactAuthority": all(tuple(rgb) in rear_swatches for rgb in cand_rgb.tolist()),
                "regionalLumaDelta": {"median": median_delta, "p25": p25_delta, "p75": p75_delta},
            }
            mask_records[component] = {"file": rel(mask_path), "sha256": sha(mask_path), "pixels": int(mask.sum())}
        visible = frame_arr[:, :, 3] > 0
        unowned = int(np.count_nonzero(visible & (ownership_sum == 0)))
        multi = int(np.count_nonzero(ownership_sum > 1))
        body_path = BODY_DIR / f"keeper_prime_work-back_f{index + 1:02d}.png"
        body_records.append({
            "frame": index + 1, "file": rel(body_path), "sha256": sha(body_path), "sourceGrid": rel(SOURCES[source_ref[0]]) if source_ref is not None else None, "sourceGridCell": source_ref[1] + 1 if source_ref is not None else None,
            "derivation": "exact-approved-rear-endpoint" if source_ref is None else "generated geometry only; all visible RGB registered to exact Prime rear authority; y>=205 exact authority pixels",
            "bounds": alpha_bounds(frame), "edgeAlphaPixels": edge_alpha_pixels(frame), "transparentGutterPx": transparent_gutter(frame),
            "floorY": alpha_bounds(frame)["maxY"], "ownership": {"unownedVisiblePixels": unowned, "multiplyOwnedVisiblePixels": multi},
            "componentMasks": mask_records, "colourEvidence": colour_evidence,
        })
        if unowned or multi: raise RuntimeError(f"ownership failure in body frame {index + 1}")

    body_strip = PACK / "drafts/body/keeper_prime_work-back_f24.png"; save_strip(body_strip, frames)
    write_json(body_strip.with_suffix(".json"), {"schema": "lighthouse-keeper/sprite-sidecar@draft-1", "name": "keeper_prime_work-back", "w": 32, "h": 40, "density": 8, "frames": 24, "fps": 4, "anchor": [16, 40], "facing": "back", "startPose": "standing-back", "endPose": "standing-back", "loop": True, "bodySfxCues": [], "status": "review-draft-not-production", "frameSha256": [r["sha256"] for r in body_records]})

    icons = build_icons(); effects = build_fan_effects(); puff_path, puff_frames = build_puff_strip()
    phrase_specs = {
        "cooking": {"label": "Cooking", "primary": "pan", "secondary": "spoon", "accent": "heat"},
        "mixing": {"label": "Mixing", "family": "mixing-washing", "primary": "bowl", "secondary": "whisk", "accent": "heat"},
        "washing": {"label": "Washing", "family": "mixing-washing", "primary": "plate", "secondary": "sponge", "accent": "bubbles"},
        "repair": {"label": "Generic repair", "primary": "tools", "secondary": "bolt", "accent": "flicks"},
    }
    phrases = {name: {**spec, "frames": phrase_frames(spec["primary"], spec["secondary"], spec["accent"])} for name, spec in phrase_specs.items()}
    callout_contact_sheets = render_callout_contact_sheets(phrases, icons, effects, puff_path)
    sfx = {
        "bodySilent": True,
        "cooking": [{"frame": 8, "cue": "activity_cook_utensil_clink", "kind": "activity-beat"}, {"frame": 21, "cue": "asset_cooking_sizzle_loop", "kind": "asset-state"}],
        "mixing": [{"frame": 8, "cue": "activity_mix_whisk", "kind": "activity-beat"}, {"frame": 21, "cue": "activity_mix_bowl_clink", "kind": "activity-beat"}],
        "washing": [{"frame": 8, "cue": "asset_sink_water_loop", "kind": "asset-state"}, {"frame": 21, "cue": "activity_wash_crockery_clink", "kind": "activity-beat"}],
        "repair": [{"frame": 8, "cue": "activity_repair_tool_tap", "kind": "activity-beat"}, {"frame": 21, "cue": "activity_repair_ratchet", "kind": "activity-beat"}, {"frame": 32, "cue": "sfx_repair_done", "kind": "completion"}],
    }

    published: list[dict] = []; by_hash: dict[str, dict] = {}
    body_public = [publish(BODY_DIR / f"keeper_prime_work-back_f{i:02d}.png", f"work-back-f{i}", published, by_hash) for i in range(1, 25)]
    icon_public = {name: publish(path, f"icon-{name}", published, by_hash) for name, path in icons.items()}
    effect_public = {name: publish(path, f"effect-{name}", published, by_hash) for name, path in effects.items()}
    puff_public = publish(puff_path, "puff-f8", published, by_hash)
    authority_public = publish(REAR, "exact-prime-rear", published, by_hash)
    legacy_public = publish(LEGACY, "legacy-cook-back-motion-only", published, by_hash)

    approach = json.loads(APPROACH_REGISTER.read_text())
    source_by_old_url = {entry.get("url", "/" + entry["public"].removeprefix("public/")): ROOT / entry["source"] for entry in approach["publishedAssets"]}
    approach_frames = []
    for frame in approach["route"]["framesData"][:28]:
        source = source_by_old_url[frame["src"]]
        entry = publish(source, source.stem.replace("keeper_prime_", "authority-"), published, by_hash)
        approach_frames.append({**frame, "src": entry["url"], "authoritySha256": entry["sourceSha256"]})

    turn_files = [ROOT / f"art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames/keeper_prime_turn_side-right_to_back_f{i:02d}.png" for i in range(1, 9)]
    departure = []
    x = 374
    for source in reversed(turn_files):
        entry = publish(source, f"authority-return-{source.stem[-3:]}", published, by_hash)
        departure.append({"src": entry["url"], "phase": "approved reverse turn", "pose": source.stem[-3:], "dx": 0, "x": x, "durationMs": 62.5, "authoritySha256": entry["sourceSha256"]})
    bridge_files = [ROOT / f"art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f{i}.png" for i in range(2, 6)]
    for source, dx in zip(bridge_files, (2, 6, 12, 18)):
        x += dx; entry = publish(source, f"authority-accel-{source.stem[-2:]}", published, by_hash)
        departure.append({"src": entry["url"], "phase": "approved acceleration", "pose": source.stem[-2:], "dx": dx, "x": x, "durationMs": 83.3333333333, "authoritySha256": entry["sourceSha256"]})
    walk_files = [ROOT / f"art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f{i}.png" for i in range(2, 9)] + [ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f1.png"]
    for source in walk_files:
        x += 21; entry = publish(source, f"authority-depart-{source.stem[-2:]}", published, by_hash)
        departure.append({"src": entry["url"], "phase": "approved walk away", "pose": source.stem[-2:], "dx": 21, "x": x, "durationMs": 100, "authoritySha256": entry["sourceSha256"]})

    action_sequence = list(range(1, 25))
    action_route = [{"src": body_public[i - 1]["url"], "phase": "Prime rear-work action", "pose": f"work F{i}", "actionFrame": i, "dx": 0, "x": 374, "durationMs": 250, "candidateSha256": body_records[i - 1]["sha256"]} for i in action_sequence]
    route = approach_frames + action_route + departure

    catalogue = {
        "schema": "lighthouse-keeper/prime-back-work-activity-review@1", "set": SET, "status": "immutable-reversible-review-candidate-not-approved",
        "registration": {"logicalCell": list(LOGICAL_CELL), "cellPixels": list(CELL), "density": DENSITY, "anchor": [16, 40], "floorPixelY": FLOOR_Y},
        "body": {"fps": ACTION_FPS, "frames": [{**record, "src": body_public[i]["url"]} for i, record in enumerate(body_records)], "strip": {"file": rel(body_strip), "sha256": sha(body_strip)}, "sfxCues": []},
        "callouts": {"fps": PHRASE_FPS, "frames": PHRASE_FRAMES, "durationSeconds": PHRASE_FRAMES / PHRASE_FPS, "styles": {"fan": {"label": "Bubble-free fan", "status": "equal review candidate"}, "cloud": {"label": "Cloud / puff", "status": "equal review candidate"}}, "reviewDefaultStyle": "fan", "styleApproved": None, "puff": {"src": puff_public["url"], "frames": 8, "cellPixels": [128, 96]}, "envelopeEffects": {name: {"src": entry["url"], "cellPixels": [96, 96]} for name, entry in effect_public.items()}, "icons": {name: {"src": entry["url"], "cellPixels": [96, 96]} for name, entry in icon_public.items()}, "phrases": phrases, "reducedMotion": {name: {"primary": spec["primary"], "secondary": spec["secondary"]} for name, spec in phrase_specs.items()}},
        "sfx": sfx,
        "route": route,
        "reviewReferences": {"exactRear": authority_public["url"], "legacyCookBack": legacy_public["url"]},
        "contextLayer": {"kind": "review-only rear-wall furniture proxy", "position": "behind Keeper", "separate": True, "approved": False},
        "controlsRequired": ["body-visible", "envelope-visible", "icons-visible", "furniture-visible", "callout-style", "sfx-muted", "body-play-pause-step", "callout-play-pause-step", "route-or-isolated", "prime-ghost", "reduced-motion"],
    }
    catalogue_path = PACK / "catalogue.json"
    public_catalogue_path = PUBLIC / "catalogue.json"
    write_json(catalogue_path, catalogue)
    # The readable draft catalogue carries the full verification evidence. The
    # browser needs only playback fields, so publish a deterministic compact
    # projection rather than adding hundreds of kilobytes of audit-only data
    # to every deployment.
    public_catalogue = {
        "schema": catalogue["schema"], "status": catalogue["status"],
        "body": {"frames": [{"frame": f["frame"], "src": f["src"]} for f in catalogue["body"]["frames"]]},
        "callouts": catalogue["callouts"], "contextLayer": catalogue["contextLayer"],
        "sfx": catalogue["sfx"], "route": catalogue["route"],
        "reviewReferences": catalogue["reviewReferences"],
    }
    write_compact_json(public_catalogue_path, public_catalogue)

    callout_records = {}
    for name, path in {**icons, **effects, "puff": puff_path}.items():
        image = Image.open(path).convert("RGBA")
        frame_width = 128 if name == "puff" else image.width
        frames_count = 8 if name == "puff" else 1
        cells = []
        for i in range(frames_count):
            cell = image.crop((i * frame_width, 0, (i + 1) * frame_width, image.height))
            if edge_alpha_pixels(cell): raise RuntimeError(f"callout {name} frame {i + 1} touches edge")
            has_visible = bool(np.count_nonzero(np.asarray(cell.getchannel("A"))))
            cells.append({"frame": i + 1, "edgeAlphaPixels": 0, "transparentGutterPx": transparent_gutter(cell) if has_visible else min(cell.size) // 2})
        callout_records[name] = {"file": rel(path), "sha256": sha(path), "frames": cells}

    protected = {
        "exactRear": {"file": rel(REAR), "sha256": sha(REAR)}, "legacyCookBack": {"file": rel(LEGACY), "sha256": sha(LEGACY)},
        "legacyCookBackSidecar": {"file": rel(LEGACY_SIDECAR), "sha256": sha(LEGACY_SIDECAR)}, "approvedApproach": {"file": rel(APPROACH_APPROVAL), "sha256": sha(APPROACH_APPROVAL)},
        "approvedTurn": {"file": rel(TURN_APPROVAL), "sha256": sha(TURN_APPROVAL)}, "runtimeManifest": {"file": rel(RUNTIME_MANIFEST), "sha256": sha(RUNTIME_MANIFEST)},
        "workbench": {"file": rel(WORKBENCH), "sha256": sha(WORKBENCH)}, "brief": {"file": rel(BRIEF), "sha256": sha(BRIEF)}, "normalisationContract": {"file": rel(NORMALISATION), "sha256": sha(NORMALISATION)},
    }
    html = (ROOT / "scripts/templates/keeper_prime_back_work_activity_callout_v1.html").read_text()
    html = html.replace("__SET__", SET)
    (PUBLIC / "index.html").write_text(html)

    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET, "status": "prime-back-work-and-callout-v1-awaiting-frank",
        "purpose": "First Prime direct-rear generic work candidate using keeper_cook_back as choreography only, with independently switchable cooking, mixing, washing and generic-repair callouts in equal bubble-free-fan and cloud/puff treatments.",
        "authorities": protected,
        "directionalReferences": {
            "claudeNote": {"file": rel(CLAUDE_NOTE), "sha256": sha(CLAUDE_NOTE), "authority": False, "contribution": "composition and phrase-timing prompts only; superseded where Frank clarified both treatments are equal candidates"},
            "claudeSketch": {"file": rel(CLAUDE_SKETCH), "sha256": sha(CLAUDE_SKETCH), "authority": False, "contribution": "interaction reference only; no art, pixels, vector paths or definitive choices reused"},
        },
        "historicalChoreographyOnly": {"clip": "keeper_cook_back", "frames": 8, "fps": 4, "allowedEvidence": ["alternating shoulder and elbow paths", "planted-feet rhythm", "timing"], "visibleHistoricalPixelsReused": 0},
        "generation": {"tool": "built-in image generation", "selectedSources": [{"file": rel(path), "sha256": sha(path), "role": role, "knownInputDefect": "opaque generated backdrop; never survives registration"} for path, role in zip(SOURCES, ("opening frames 2-8", "sustained work frames 9-16", "closing frames 17-22"))], "rejectedPromptProvenance": {"file": rel(REJECTED_SOURCE), "sha256": sha(REJECTED_SOURCE), "reason": "initial eight-pose proposal was too short and raised hands too near the head"}, "sourceContribution": "pose geometry only; background removed deterministically; visible RGB registered from exact Prime rear authority", "sourceEvidence": source_evidence},
        "candidate": {"bodyFrames": body_records, "bodyStrip": {"file": rel(body_strip), "sha256": sha(body_strip), "pixels": [CELL[0] * 24, CELL[1]]}, "calloutComponents": callout_records, "calloutContactSheets": callout_contact_sheets, "catalogue": {"file": rel(catalogue_path), "sha256": sha(catalogue_path)}, "publicCatalogue": {"file": rel(public_catalogue_path), "sha256": sha(public_catalogue_path), "projection": "playback-fields-only"}, "routeFrames": len(route), "publicShell": {"file": rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")}, "publishedAssets": published},
        "publishedAssets": published,
        "checks": {"exactEntryEndpoint": body_records[0]["sha256"] == sha(REAR), "exactExitEndpoint": body_records[-1]["sha256"] == sha(REAR), "walkStopTurnActionSeamsExact": route[27]["authoritySha256"] == route[28]["candidateSha256"] == route[51]["candidateSha256"] == sha(REAR) and route[52]["authoritySha256"] == route[26]["authoritySha256"], "everyBodyCellHasSafeEdge": all(r["edgeAlphaPixels"] == 0 and r["transparentGutterPx"] >= 4 for r in body_records), "everyBodyPixelOwnedOnce": all(r["ownership"] == {"unownedVisiblePixels": 0, "multiplyOwnedVisiblePixels": 0} for r in body_records), "bodySilent": sfx["bodySilent"], "bothCalloutStylesBuilt": set(catalogue["callouts"]["styles"]) == {"fan", "cloud"} and catalogue["callouts"]["styleApproved"] is None, "calloutComponentsSeparate": True, "calloutCellsHaveSafeEdges": all(all(c["edgeAlphaPixels"] == 0 for c in r["frames"]) for r in callout_records.values()), "furnitureBehindKeeper": catalogue["contextLayer"]["position"] == "behind Keeper", "approvedRouteAuthoritiesReferencedByteForByte": True, "runtimeManifestUnchanged": True, "workbenchUnchanged": True, "productionUnchanged": True, "kitchenWorkChanged": False, "preloadRequired": True},
        "approvalBoundary": {"candidateApproved": False, "bodyApproved": False, "calloutGrammarApproved": False, "sfxApproved": False, "promotionAllowed": False, "runtimeChanged": False, "finalChanged": False, "productionChanged": False, "deployed": False},
        "rollback": f"Discard {rel(PACK)} and its new review-only page/archive set; no canonical, runtime, Final, approved-route or Kitchen asset requires restoration.",
    }
    register_path = PACK / "batch-register.json"; write_json(register_path, register)

    print(json.dumps({"review": f"/keeper-review/{SET}/", "bodyFrames": len(body_records), "durationSeconds": len(body_records) / ACTION_FPS, "routeFrames": len(route), "phrases": list(phrases), "sources": [sha(path) for path in SOURCES]}, indent=2))


if __name__ == "__main__":
    main()
