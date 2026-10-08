#!/usr/bin/env python3
"""Author the first aligned keeper sprite batch at density 4."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "art/raw/keeper-first-batch"
OUT.mkdir(parents=True, exist_ok=True)

ASSET_CONTRACT = json.loads((ROOT / "data/keeper_asset_contract.json").read_text())
STANDARD_CANVAS = ASSET_CONTRACT["canvas"]["standard"]
D = STANDARD_CANVAS["density"]
W, H = STANDARD_CANVAS["width"] * D, STANDARD_CANVAS["height"] * D
INK = "#14243a"
INK2 = "#202f4d"
NAVY = "#263d70"
NAVY_HI = "#355d9a"
BLUE_D = "#205b83"
BLUE = "#267da0"
BLUE_HI = "#4c9fc1"
CREAM_D = "#d8c9a8"
CREAM = "#f3e7cc"
CREAM_HI = "#fff5dc"
SKIN_D = "#c8784f"
SKIN = "#eaa06f"
SKIN_HI = "#f6bd86"
BOOT = "#17243b"


def image():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def poly(draw, points, fill, outline=INK, width=2):
    points = [(round(x * D), round(y * D)) for x, y in points]
    draw.polygon(points, fill=fill)
    if outline:
        draw.line(points + [points[0]], fill=outline, width=width, joint="curve")


def rect(draw, box, fill, outline=None, width=2):
    draw.rectangle(tuple(round(v * D) for v in box), fill=fill, outline=outline, width=width)


def ellipse(draw, box, fill, outline=INK, width=2):
    draw.ellipse(tuple(round(v * D) for v in box), fill=fill, outline=outline, width=width)


def legs(im, rear=False, phase=0):
    d = ImageDraw.Draw(im)
    offsets = [(0, 0), (0, 0)]
    if phase:
        offsets = [(-phase, -abs(phase) // 2), (phase, 0)]
    for i, x in enumerate((10, 17)):
        ox, oy = offsets[i]
        poly(d, [(x + ox, 25 + oy), (x + 6 + ox, 25 + oy), (x + 6 + ox, 36), (x + ox, 36)], NAVY)
        rect(d, (x + ox + 1, 27 + oy, x + 5 + ox, 29 + oy), NAVY_HI)
        foot = (x - 1 + ox, 35, x + 6 + ox, 39)
        rect(d, foot, BOOT, INK, 2)
        rect(d, (x + ox, 36, x + 5 + ox, 37), "#324568")
    if rear:
        rect(d, (11, 27, 15, 29), "#1b2b49")
        rect(d, (18, 27, 22, 29), "#1b2b49")


def torso(im, rear=False, bob=0):
    d = ImageDraw.Draw(im)
    poly(d, [(9, 15 + bob), (23, 15 + bob), (26, 27 + bob), (6, 27 + bob)], BLUE)
    rect(d, (7, 20 + bob, 25, 23 + bob), CREAM)
    rect(d, (9, 16 + bob, 22, 18 + bob), BLUE_HI)
    rect(d, (8, 25 + bob, 24, 27 + bob), BLUE_D)
    if rear:
        rect(d, (14, 16 + bob, 18, 26 + bob), "#2d88ab")


def arm(im, side, rear=False, raised=0, bob=0):
    d = ImageDraw.Draw(im)
    left = side == "l"
    x = 5 if left else 23
    direction = -1 if left else 1
    y = 16 + bob
    hand_y = 27 - raised + bob
    poly(d, [(x, y), (x + 4, y), (x + 4 + direction, hand_y), (x + direction, hand_y)], BLUE)
    rect(d, (min(x + direction, x + 4 + direction), hand_y - 2, max(x + direction, x + 4 + direction), hand_y), CREAM)
    hx = x + 2 + direction
    ellipse(d, (hx - 2, hand_y - 1, hx + 2, hand_y + 3), SKIN, INK, 2)
    rect(d, (x + 1, y + 1, x + 3, y + 3), BLUE_HI)


def head(im, mood="neutral", rear=False, bob=0):
    d = ImageDraw.Draw(im)
    y = bob
    ellipse(d, (9, 4 + y, 23, 17 + y), SKIN, INK, 2)
    rect(d, (10, 5 + y, 22, 8 + y), SKIN_HI)
    # Cap crown, band and tiny brass badge.
    poly(d, [(8, 4 + y), (10, 1 + y), (22, 1 + y), (24, 4 + y)], NAVY)
    rect(d, (7, 4 + y, 25, 7 + y), NAVY, INK, 2)
    rect(d, (10, 2 + y, 21, 3 + y), NAVY_HI)
    rect(d, (15, 3 + y, 17, 5 + y), "#e6b955")
    if rear:
        poly(d, [(9, 9 + y), (23, 9 + y), (22, 17 + y), (10, 17 + y)], CREAM)
        rect(d, (12, 10 + y, 20, 12 + y), CREAM_HI)
        return
    # Ears, brows, eyes, nose.
    ellipse(d, (7, 9 + y, 10, 13 + y), SKIN, INK, 1)
    ellipse(d, (22, 9 + y, 25, 13 + y), SKIN, INK, 1)
    rect(d, (11, 8 + y, 14, 9 + y), CREAM_D)
    rect(d, (18, 8 + y, 21, 9 + y), CREAM_D)
    rect(d, (12, 10 + y, 13, 12 + y), INK)
    rect(d, (19, 10 + y, 20, 12 + y), INK)
    rect(d, (15, 11 + y, 18, 14 + y), SKIN_D)
    # Beard and moustache keep the old keeper's large readable triangle.
    poly(d, [(9, 13 + y), (13, 13 + y), (16, 15 + y), (19, 13 + y), (23, 13 + y), (21, 22 + y), (16, 25 + y), (11, 22 + y)], CREAM)
    rect(d, (11, 14 + y, 15, 16 + y), CREAM_HI)
    rect(d, (17, 14 + y, 21, 16 + y), CREAM_HI)
    mouth_y = 16 + y
    if mood == "happy":
        poly(d, [(14, mouth_y), (16, mouth_y + 2), (18, mouth_y)], SKIN_D, None)
    elif mood == "grumpy":
        poly(d, [(14, mouth_y + 1), (16, mouth_y), (18, mouth_y + 1)], SKIN_D, None)
    elif mood == "open":
        ellipse(d, (15, mouth_y, 17, mouth_y + 2), "#7e3c35", None)
    elif mood == "asleep":
        rect(d, (12, 10 + y, 14, 10.5 + y), INK)
        rect(d, (18, 10 + y, 20, 10.5 + y), INK)


def compose(view="front", mood="neutral", phase=0, hands=0, bob=0):
    im = image()
    rear = view == "back"
    legs(im, rear=rear, phase=phase)
    torso(im, rear=rear, bob=bob)
    arm(im, "l", rear=rear, raised=hands, bob=bob)
    head(im, mood=mood, rear=rear, bob=bob)
    arm(im, "r", rear=rear, raised=hands, bob=bob)
    return im


def side_walk(step=0):
    """A right-facing walk pose. Runtime mirroring supplies left-facing travel."""
    im = image()
    d = ImageDraw.Draw(im)
    bob = -1 if abs(step) >= 2 else 0

    def side_leg(far, stride):
        hip_x = 15 if far else 18
        knee_x = hip_x + stride * 0.55
        foot_x = hip_x + stride
        colour = INK2 if far else NAVY
        poly(d, [(hip_x - 2, 25 + bob), (hip_x + 3, 25 + bob), (knee_x + 2, 34), (knee_x - 2, 34)], colour)
        poly(d, [(knee_x - 2, 33), (knee_x + 2, 33), (foot_x + 3, 38), (foot_x - 2, 38)], colour)
        poly(d, [(foot_x - 2, 37), (foot_x + 5, 37), (foot_x + 6, 39), (foot_x - 3, 39)], BOOT)
        rect(d, (min(knee_x, foot_x), 35, max(knee_x, foot_x) + 2, 36), "#324568")

    # Rear limbs first, then body, then near limbs for readable depth.
    side_leg(True, -step)
    far_hand_x = 13 + step * 0.45
    poly(d, [(13, 16 + bob), (16, 17 + bob), (far_hand_x + 2, 27), (far_hand_x - 1, 27)], BLUE_D)
    ellipse(d, (far_hand_x - 2, 25, far_hand_x + 2, 29), SKIN_D, INK, 2)

    poly(d, [(11, 15 + bob), (22, 15 + bob), (24, 27 + bob), (9, 27 + bob)], BLUE)
    rect(d, (10, 20 + bob, 23, 23 + bob), CREAM)
    rect(d, (11, 16 + bob, 21, 18 + bob), BLUE_HI)
    rect(d, (10, 25 + bob, 23, 27 + bob), BLUE_D)

    # Side-profile head: one eye, projecting nose and beard, but same cap/beard identity.
    ellipse(d, (10, 4 + bob, 23, 17 + bob), SKIN, INK, 2)
    rect(d, (11, 5 + bob, 21, 8 + bob), SKIN_HI)
    poly(d, [(9, 4 + bob), (11, 1 + bob), (22, 1 + bob), (25, 4 + bob)], NAVY)
    rect(d, (8, 4 + bob, 26, 7 + bob), NAVY, INK, 2)
    rect(d, (11, 2 + bob, 21, 3 + bob), NAVY_HI)
    rect(d, (16, 3 + bob, 18, 5 + bob), "#e6b955")
    ellipse(d, (8, 9 + bob, 11, 13 + bob), SKIN, INK, 1)
    rect(d, (18, 9 + bob, 20, 11 + bob), INK)
    poly(d, [(21, 11 + bob), (25, 13 + bob), (21, 15 + bob)], SKIN_D)
    poly(d, [(12, 13 + bob), (18, 13 + bob), (23, 15 + bob), (22, 21 + bob), (17, 24 + bob), (12, 21 + bob)], CREAM)
    rect(d, (15, 14 + bob, 21, 16 + bob), CREAM_HI)

    side_leg(False, step)
    near_hand_x = 22 - step * 0.45
    poly(d, [(20, 16 + bob), (23, 17 + bob), (near_hand_x + 2, 27), (near_hand_x - 1, 27)], BLUE)
    rect(d, (20, 17 + bob, 22, 19 + bob), BLUE_HI)
    ellipse(d, (near_hand_x - 2, 25, near_hand_x + 2, 29), SKIN, INK, 2)
    return im


def generated_frames(filename, expected, fallback=None, logical_width=32, logical_height=40, scale_reference_index=None, force_equal_cells=False, min_component_pixels=1000):
    """Normalise an identity-locked generated source onto aligned contract slots."""
    source = Path(__file__).with_name(filename)
    if not source.exists():
        if fallback is not None:
            return fallback
        raise FileNotFoundError(source)
    sheet = Image.open(source).convert("RGBA")
    alpha = sheet.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
    occupied = []
    for x in range(sheet.width):
        occupied.append(alpha.crop((x, 0, x + 1, sheet.height)).getbbox() is not None)
    runs = []
    start = None
    for x, used in enumerate(occupied + [False]):
        if used and start is None:
            start = x
        elif not used and start is not None:
            if x - start > 80:
                runs.append((start, x))
            start = None
    components = None
    if force_equal_cells:
        bounds = []
        components = []
        for index in range(expected):
            x0 = round(index * sheet.width / expected)
            x1 = round((index + 1) * sheet.width / expected)
            cell = alpha.crop((x0, 0, x1, sheet.height))
            width, height = cell.size
            pixels = bytearray(cell.tobytes())
            found = []
            for start, value in enumerate(pixels):
                if not value:
                    continue
                pixels[start] = 0
                pending = [start]
                members = []
                min_x, min_y, max_x, max_y = width, height, 0, 0
                while pending:
                    member = pending.pop()
                    y, x = divmod(member, width)
                    members.append(member)
                    min_x, min_y = min(min_x, x), min(min_y, y)
                    max_x, max_y = max(max_x, x), max(max_y, y)
                    for neighbour in (member - 1, member + 1, member - width, member + width):
                        if 0 <= neighbour < width * height and pixels[neighbour] and (neighbour // width == y or neighbour % width == x):
                            pixels[neighbour] = 0
                            pending.append(neighbour)
                found.append((len(members), (min_x, min_y, max_x + 1, max_y + 1), members))
            if not found:
                raise ValueError(f"Generated keeper cell {index} is empty in {filename}")
            _, box, members = max(found, key=lambda item: item[0])
            bounds.append((x0 + box[0], box[1], x0 + box[2], box[3]))
            components.append([((member // width) * sheet.width) + (member % width) + x0 for member in members])
    elif len(runs) != expected:
        # Rarely two well-spaced figures overlap by a few x columns without
        # touching. Fall back to actual connected figures rather than cutting
        # either pose at an arbitrary cell boundary.
        width, height = alpha.size
        pixels = bytearray(alpha.tobytes())
        found = []
        for start, value in enumerate(pixels):
            if not value:
                continue
            pixels[start] = 0
            pending = [start]
            members = []
            min_x, min_y, max_x, max_y = width, height, 0, 0
            while pending:
                index = pending.pop()
                y, x = divmod(index, width)
                members.append(index)
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x), max(max_y, y)
                for neighbour in (index - 1, index + 1, index - width, index + width):
                    if 0 <= neighbour < width * height and pixels[neighbour] and (neighbour // width == y or neighbour % width == x):
                        pixels[neighbour] = 0
                        pending.append(neighbour)
            if len(members) > min_component_pixels:
                found.append(((min_x, min_y, max_x + 1, max_y + 1), members))
        found.sort(key=lambda item: item[0][0])
        if len(found) != expected:
            raise ValueError(f"Expected {expected} generated keeper poses in {filename}, found {len(runs)} column runs and {len(found)} connected figures")
        bounds = [box for box, _ in found]
        components = [members for _, members in found]
    else:
        bounds = []
        for x0, x1 in runs:
            crop_alpha = alpha.crop((x0, 0, x1, sheet.height))
            box = crop_alpha.getbbox()
            if box is None:
                raise ValueError("Generated keeper pose is empty")
            bounds.append((x0 + box[0], box[1], x0 + box[2], box[3]))
    tallest = max(y1 - y0 for _, y0, _, y1 in bounds)
    widest = max(x1 - x0 for x0, _, x1, _ in bounds)
    target_width = logical_width * D
    target_height = logical_height * D
    height_scale = (target_height - 8) / tallest
    if scale_reference_index is not None:
        _, reference_y0, _, reference_y1 = bounds[scale_reference_index]
        height_scale = min(height_scale, 152 / (reference_y1 - reference_y0))
    elif logical_height == 40:
        height_scale = 152 / tallest
    scale = min(height_scale, (target_width - 8) / widest)
    frames = []
    for pose_index, box in enumerate(bounds):
        pose = sheet.crop(box)
        if components is not None:
            x0, y0, x1, y1 = box
            component_alpha = bytearray((x1 - x0) * (y1 - y0))
            for index in components[pose_index]:
                y, x = divmod(index, sheet.width)
                component_alpha[(y - y0) * (x1 - x0) + x - x0] = 255
            pose.putalpha(Image.frombytes("L", pose.size, bytes(component_alpha)))
        size = (max(1, round(pose.width * scale)), max(1, round(pose.height * scale)))
        pose = pose.resize(size, Image.Resampling.LANCZOS)
        # The game contract requires hard alpha even when a generated edge has a fringe.
        a = pose.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
        pose.putalpha(a)
        frame = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        frame.alpha_composite(pose, ((target_width - pose.width) // 2, target_height - 2 - pose.height))
        frames.append(frame)
    return frames


def part(which, rear=False, mood="neutral"):
    im = image()
    if which == "torso": torso(im, rear)
    elif which == "arm_l": arm(im, "l", rear)
    elif which == "arm_r": arm(im, "r", rear)
    elif which == "leg_l":
        whole = image(); legs(whole, rear); im.alpha_composite(whole.crop((0, 0, 16 * D, H)), (0, 0))
    elif which == "leg_r":
        whole = image(); legs(whole, rear); im.alpha_composite(whole.crop((16 * D, 0, W, H)), (16 * D, 0))
    elif which == "head": head(im, mood, rear)
    return im


def contract(frames, fps, pivot=None, *, w=32, h=40, loop=True, seat_point=None, hand_use_point=None, look_target_point=None, bed_surface_point=None, pillow_point=None, reverse_for=None, mirror_safe=False, facing=None, interaction=None, mirrors_for=None):
    value = {"w": w, "h": h, "frames": frames, "fps": fps, "density": D, "anchor": [w // 2, h], "z": 50}
    if pivot is not None: value["pivot"] = pivot
    value["loop"] = loop
    if seat_point is not None: value["seatPoint"] = seat_point
    if hand_use_point is not None: value["handUsePoint"] = hand_use_point
    if look_target_point is not None: value["lookTargetPoint"] = look_target_point
    if bed_surface_point is not None: value["bedSurfacePoint"] = bed_surface_point
    if pillow_point is not None: value["pillowPoint"] = pillow_point
    if reverse_for is not None: value["reverseFor"] = reverse_for
    if mirror_safe: value["mirrorSafe"] = True
    if facing is not None: value["facing"] = facing
    if interaction is not None: value["interaction"] = interaction
    if mirrors_for is not None: value["mirrorsFor"] = mirrors_for
    return value


def save(name, frames, fps=0, pivot=None, **metadata):
    frame_width = frames[0].width
    frame_height = frames[0].height
    if any(frame.size != (frame_width, frame_height) for frame in frames):
        raise ValueError(f"Mismatched frame sizes for {name}")
    strip = Image.new("RGBA", (frame_width * len(frames), frame_height), (0, 0, 0, 0))
    for i, frame in enumerate(frames): strip.alpha_composite(frame, (i * frame_width, 0))
    png = OUT / f"{name}_f{len(frames)}.png"
    strip.save(png, optimize=True)
    png.with_suffix(".json").write_text(json.dumps(contract(len(frames), fps, pivot, w=frame_width // D, h=frame_height // D, **metadata), indent=2) + "\n")


def save_preview(name, frames, duration, ping_pong=False):
    sequence = frames + (frames[-2:0:-1] if ping_pong else [])
    previews = []
    for frame in sequence:
        canvas = Image.new("RGBA", (frame.width * 2, frame.height * 2), (244, 236, 214, 255))
        canvas.alpha_composite(frame.resize((frame.width * 2, frame.height * 2), Image.Resampling.NEAREST))
        previews.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    preview = ROOT / f"docs/floor-asset-catalogue/{name}-preview.gif"
    previews[0].save(preview, save_all=True, append_images=previews[1:], duration=duration, loop=0, disposal=2, optimize=False)


PIVOTS = {"torso": [16, 25], "arm_l": [10, 15], "arm_r": [22, 15], "leg_l": [13, 25], "leg_r": [19, 25]}
for view in ("front", "back"):
    for p in ("torso", "arm_l", "arm_r", "leg_l", "leg_r"):
        save(f"keeper_{view}_{p}", [part(p, view == "back")], pivot=PIVOTS[p])
for mood in ("happy", "neutral", "grumpy", "asleep", "open"):
    save(f"keeper_front_head_{mood}", [part("head", False, mood)], pivot=[16, 11])
save("keeper_back_head", [part("head", True)], pivot=[16, 11])
save("keeper_reference", [compose("front", "neutral")])

save("keeper_idle", [compose("front", "neutral", bob=b) for b in (0, 0, -1, 0)], 6)
walk_frames = generated_frames("keeper-walk-generated-source.png", 8, [side_walk(p) for p in (-3, -2, 0, 2, 3, 2, 0, -2)])
turn_frames = generated_frames("keeper-turn-back-generated-source.png", 6)
work_frames = generated_frames("keeper-work-back-generated-source.png", 8)
sit_side_frames = generated_frames("keeper-sit-side-generated-source.png", 6)
sit_front_frames = generated_frames("keeper-sit-front-generated-source.png", 6)
piano_frames = generated_frames("keeper-piano-generated-source.png", 8)
urinate_frames = generated_frames("keeper-loo-stand-generated-source.png", 6)
eat_seated_frames = generated_frames("keeper-eat-seated-generated-source.png", 8)
door_side_frames = generated_frames("keeper-door-side-generated-source.png", 6)
door_back_frames = generated_frames("keeper-door-back-generated-source.png", 6)
ladder_frames = generated_frames("keeper-ladder-generated-source.png", 8)
stairs_up_frames = generated_frames("keeper-stairs-up-generated-source.png", 8)
stairs_down_frames = generated_frames("keeper-stairs-down-generated-source.png", 8)
switch_side_frames = generated_frames("keeper-switch-side-generated-source.png", 6)
switch_back_frames = generated_frames("keeper-switch-back-generated-source.png", 6)
parachute_jump_frames = generated_frames("keeper-parachute-jump-generated-source.png", 9, logical_width=48, logical_height=84, scale_reference_index=0)
platform_dive_frames = generated_frames("keeper-platform-dive-generated-source.png", 10, logical_width=48, logical_height=56, scale_reference_index=0)
dig_frames = generated_frames("keeper-dig-generated-source.png", 8)
feed_animals_frames = generated_frames("keeper-feed-animals-generated-source.png", 8)
sow_seeds_frames = generated_frames("keeper-sow-seeds-generated-source.png", 8)
pick_vegetable_frames = generated_frames("keeper-pick-vegetable-generated-source.png", 8)
pick_fruit_frames = generated_frames("keeper-pick-fruit-generated-source.png", 8)
carry_shopping_frames = generated_frames("keeper-carry-shopping-generated-source.png", 8)
row_boat_frames = generated_frames("keeper-row-boat-generated-source.png", 8, logical_width=40)
drive_speedboat_frames = generated_frames("keeper-drive-speedboat-generated-source.png", 8)
operate_outboard_frames = generated_frames("keeper-operate-outboard-generated-source.png", 8)
watch_tv_frames = generated_frames("keeper-watch-tv-generated-source.png", 8)
weld_frames = generated_frames("keeper-weld-generated-source.png", 8)
saw_wood_frames = generated_frames("keeper-saw-wood-generated-source.png", 8, logical_width=40, force_equal_cells=True)
wave_camera_frames = generated_frames("keeper-wave-generated-source.png", 8)
yawn_frames = generated_frames("keeper-yawn-generated-source.png", 8)
pyjamas_walk_frames = generated_frames("keeper-pyjamas-walk-generated-source.png", 8)
pyjamas_turn_back_frames = generated_frames("keeper-pyjamas-turn-back-generated-source.png", 6)
get_into_bed_frames = generated_frames("keeper-get-into-bed-generated-source.png", 8, logical_width=48, min_component_pixels=10000)
pyjamas_snore_frames = generated_frames("keeper-snore-generated-source.png", 6, logical_width=48)
save("keeper_walk", walk_frames, 10, mirror_safe=True)
save("keeper_turn_back", turn_frames, 8, loop=False, reverse_for="turn_front")
save("keeper_work_back", work_frames, 8, hand_use_point=[16, 21])
save("keeper_cook_back", work_frames, 8, hand_use_point=[16, 21])
save("keeper_wash_back", work_frames, 8, hand_use_point=[16, 21])
save("keeper_brush_teeth_back", work_frames, 8, hand_use_point=[16, 21])
save("keeper_sit_side", sit_side_frames, 8, loop=False, seat_point=[16, 29], reverse_for="stand_side", mirror_safe=True)
save("keeper_sit_front", sit_front_frames, 8, loop=False, seat_point=[16, 29], reverse_for="stand_front")
save("keeper_piano", piano_frames, 10, seat_point=[16, 29], hand_use_point=[24, 20])
save("keeper_urinate_back", urinate_frames, 8, hand_use_point=[16, 27])
save("keeper_eat_seated", eat_seated_frames, 8, seat_point=[16, 29], hand_use_point=[24, 17], mirror_safe=True)
save("keeper_door_open_side", door_side_frames, 8, loop=False, hand_use_point=[25, 20], reverse_for="door_close_side", mirror_safe=True)
save("keeper_door_open_back", door_back_frames, 8, loop=False, hand_use_point=[24, 20], reverse_for="door_close_back", mirror_safe=True)
save("keeper_ladder_climb", ladder_frames, 10, hand_use_point=[16, 6], reverse_for="ladder_descend")
save("keeper_stairs_up", stairs_up_frames, 10, mirror_safe=True)
save("keeper_stairs_down", stairs_down_frames, 10, mirror_safe=True)
save("keeper_switch_press_side", switch_side_frames, 8, loop=False, hand_use_point=[27, 17], reverse_for="switch_withdraw_side", mirror_safe=True, facing="right", interaction="press-switch", mirrors_for="left")
save("keeper_switch_press_back", switch_back_frames, 8, loop=False, hand_use_point=[26, 17], reverse_for="switch_withdraw_back", mirror_safe=True, facing="back", interaction="press-switch", mirrors_for="back-left-hand")
save("keeper_parachute_jump", parachute_jump_frames, 10, loop=False, mirror_safe=True, facing="right", interaction="parachute-jump", mirrors_for="left")
save("keeper_platform_dive", platform_dive_frames, 10, loop=False, mirror_safe=True, facing="right", interaction="platform-dive", mirrors_for="left")
save("keeper_dig", dig_frames, 8, hand_use_point=[27, 38], mirror_safe=True, facing="right", interaction="dig-ground", mirrors_for="left")
save("keeper_feed_animals", feed_animals_frames, 8, loop=False, hand_use_point=[27, 34], mirror_safe=True, facing="right", interaction="feed-bowl", mirrors_for="left")
save("keeper_sow_seeds", sow_seeds_frames, 8, hand_use_point=[27, 34], mirror_safe=True, facing="right", interaction="sow-ground", mirrors_for="left")
save("keeper_pick_vegetable", pick_vegetable_frames, 8, loop=False, hand_use_point=[26, 36], mirror_safe=True, facing="right", interaction="harvest-low", mirrors_for="left")
save("keeper_pick_fruit", pick_fruit_frames, 8, loop=False, hand_use_point=[25, 14], mirror_safe=True, facing="right", interaction="harvest-high", mirrors_for="left")
save("keeper_carry_shopping", carry_shopping_frames, 10, mirror_safe=True, facing="right", interaction="carry-shopping", mirrors_for="left")
save("keeper_row_boat", row_boat_frames, 8, seat_point=[20, 29], hand_use_point=[30, 20], mirror_safe=True, facing="right", interaction="row-boat", mirrors_for="left")
save("keeper_drive_speedboat", drive_speedboat_frames, 8, seat_point=[16, 29], hand_use_point=[25, 20], mirror_safe=True, facing="right", interaction="drive-speedboat", mirrors_for="left")
save("keeper_operate_outboard", operate_outboard_frames, 8, hand_use_point=[4, 21], mirror_safe=True, facing="rear-right", interaction="operate-outboard", mirrors_for="rear-left")
save("keeper_watch_tv", watch_tv_frames, 6, seat_point=[16, 29], look_target_point=[40, 14], mirror_safe=True, facing="rear-right", interaction="watch-tv", mirrors_for="rear-left")
save("keeper_weld", weld_frames, 8, hand_use_point=[27, 22], mirror_safe=True, facing="right", interaction="weld-workpiece", mirrors_for="left")
save("keeper_saw_wood", saw_wood_frames, 8, hand_use_point=[35, 23], mirror_safe=True, facing="right", interaction="saw-workpiece", mirrors_for="left")
save("keeper_wave_camera", wave_camera_frames, 8, loop=False, facing="front", interaction="emote-wave")
save("keeper_yawn", yawn_frames, 8, loop=False, facing="front-right", interaction="emote-yawn")
save("keeper_pyjamas_walk", pyjamas_walk_frames, 10, mirror_safe=True, facing="right", interaction="walk-pyjamas", mirrors_for="left")
save("keeper_pyjamas_turn_back", pyjamas_turn_back_frames, 8, loop=False, reverse_for="pyjamas_turn_front", facing="front-to-back", interaction="turn-pyjamas")
save("keeper_get_into_bed", get_into_bed_frames, 8, loop=False, bed_surface_point=[24, 31], pillow_point=[38, 22], reverse_for="get_out_of_bed", mirror_safe=True, facing="right", interaction="enter-bed", mirrors_for="left")
save("keeper_pyjamas_snore", pyjamas_snore_frames, 4, bed_surface_point=[24, 31], pillow_point=[38, 22], mirror_safe=True, facing="right", interaction="sleep-snore", mirrors_for="left")

# A transparent source contact sheet makes alignment mistakes easy to spot.
contact = Image.new("RGBA", (W * 4, H * 2), (244, 236, 214, 255))
for i, frame in enumerate((compose("front", "happy"), walk_frames[2], turn_frames[-1], work_frames[1], sit_side_frames[-1], sit_front_frames[-1], piano_frames[0], eat_seated_frames[2])):
    contact.alpha_composite(frame, ((i % 4) * W, (i // 4) * H))
contact.save(Path(__file__).with_name("keeper-contact-sheet.png"), optimize=True)

save_preview("keeper-walk", walk_frames, 100)
save_preview("keeper-turn-back", turn_frames, 120, ping_pong=True)
save_preview("keeper-work-back", work_frames, 120)
save_preview("keeper-sit-side", sit_side_frames, 120, ping_pong=True)
save_preview("keeper-sit-front", sit_front_frames, 120, ping_pong=True)
save_preview("keeper-piano", piano_frames, 100)
save_preview("keeper-urinate-back", urinate_frames, 120)
save_preview("keeper-eat-seated", eat_seated_frames, 120)
save_preview("keeper-door-open-side", door_side_frames, 120, ping_pong=True)
save_preview("keeper-door-open-back", door_back_frames, 120, ping_pong=True)
save_preview("keeper-ladder-climb", ladder_frames, 100, ping_pong=True)
save_preview("keeper-stairs-up", stairs_up_frames, 100)
save_preview("keeper-stairs-down", stairs_down_frames, 100)
save_preview("keeper-switch-press-right", switch_side_frames, 120, ping_pong=True)
save_preview("keeper-switch-press-left", [ImageOps.mirror(frame) for frame in switch_side_frames], 120, ping_pong=True)
save_preview("keeper-switch-press-back", switch_back_frames, 120, ping_pong=True)
save_preview("keeper-parachute-jump", parachute_jump_frames, 100)
save_preview("keeper-platform-dive", platform_dive_frames, 100)
save_preview("keeper-dig", dig_frames, 120)
save_preview("keeper-feed-animals", feed_animals_frames, 120)
save_preview("keeper-sow-seeds", sow_seeds_frames, 120)
save_preview("keeper-pick-vegetable", pick_vegetable_frames, 120)
save_preview("keeper-pick-fruit", pick_fruit_frames, 120)
save_preview("keeper-carry-shopping", carry_shopping_frames, 100)
save_preview("keeper-row-boat", row_boat_frames, 120)
save_preview("keeper-drive-speedboat", drive_speedboat_frames, 120)
save_preview("keeper-operate-outboard", operate_outboard_frames, 120)
save_preview("keeper-watch-tv-right", watch_tv_frames, 160)
save_preview("keeper-watch-tv-left", [ImageOps.mirror(frame) for frame in watch_tv_frames], 160)
save_preview("keeper-weld", weld_frames, 120)
save_preview("keeper-saw-wood", saw_wood_frames, 120)
save_preview("keeper-wave-camera", wave_camera_frames, 120)
save_preview("keeper-yawn", yawn_frames, 120)
save_preview("keeper-pyjamas-walk", pyjamas_walk_frames, 100)
save_preview("keeper-pyjamas-turn-back", pyjamas_turn_back_frames, 120, ping_pong=True)
save_preview("keeper-get-into-bed", get_into_bed_frames, 120)
save_preview("keeper-pyjamas-snore", pyjamas_snore_frames, 250)
print(f"Keeper batch authored in {OUT}")
