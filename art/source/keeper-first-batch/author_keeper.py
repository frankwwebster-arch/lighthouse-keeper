#!/usr/bin/env python3
"""Author the first aligned keeper sprite batch at density 4."""
from __future__ import annotations

import json
import math
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw, ImageOps

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


def generated_frames(filename, expected, fallback=None, logical_width=32, logical_height=40, scale_reference_index=None, force_equal_cells=False, preserve_equal_cells=False, group_equal_components=False, min_component_pixels=1000, scale_multiplier=1.0, horizontal_scale=1.0):
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
    if group_equal_components:
        # Some prop-heavy sheets have correct pose centres but overlapping
        # horizontal extents. Group whole connected components around the ten
        # largest actor bodies so a neighbour can never leak across a cell,
        # while detached mugs and kettles remain with their nearest actor.
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
            if len(members) >= 20:
                found.append((len(members), (min_x, min_y, max_x + 1, max_y + 1), members))
        actors = sorted(sorted(found, reverse=True)[:expected], key=lambda item: item[1][0])
        if len(actors) != expected:
            raise ValueError(f"Expected {expected} keeper bodies in {filename}, found {len(actors)}")
        actor_centres = [(box[0] + box[2]) / 2 for _, box, _ in actors]
        grouped = [[] for _ in range(expected)]
        for _, box, members in found:
            centre = (box[0] + box[2]) / 2
            grouped[min(range(expected), key=lambda index: abs(actor_centres[index] - centre))].extend(members)
        bounds = []
        components = []
        for members in grouped:
            xs = [index % width for index in members]
            ys = [index // width for index in members]
            bounds.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
            components.append(members)
    elif preserve_equal_cells:
        # Recent generation prompts explicitly request equal cells.  Cropping
        # each cell as a whole preserves detached held props (records, darts,
        # fishing line and water drops) that component segmentation would lose.
        bounds = []
        for index in range(expected):
            x0 = round(index * sheet.width / expected)
            x1 = round((index + 1) * sheet.width / expected)
            box = alpha.crop((x0, 0, x1, sheet.height)).getbbox()
            if box is None:
                raise ValueError(f"Generated keeper cell {index} is empty in {filename}")
            bounds.append((x0 + box[0], box[1], x0 + box[2], box[3]))
    elif force_equal_cells:
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
    scale = min(height_scale, (target_width - 8) / widest) * scale_multiplier
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
        size = (max(1, round(pose.width * scale * horizontal_scale)), max(1, round(pose.height * scale)))
        if size[0] > target_width or size[1] > target_height:
            raise ValueError(
                f"Canonical anatomy for {filename} needs {size[0]}x{size[1]} px "
                f"but its {logical_width}x{logical_height} logical canvas is too small"
            )
        pose = pose.resize(size, Image.Resampling.LANCZOS)
        # The game contract requires hard alpha even when a generated edge has a fringe.
        a = pose.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
        pose.putalpha(a)
        frame = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        frame.alpha_composite(pose, ((target_width - pose.width) // 2, target_height - 2 - pose.height))
        frames.append(frame)
    return frames


def depth_scale_sequence(frames, scales, rise_logical):
    """Bake a deliberate walk-away depth change without changing the canvas."""
    if len(frames) != len(scales) or len(frames) != len(rise_logical):
        raise ValueError("Depth sequence controls must match the frame count")
    result = []
    for frame, scale, rise in zip(frames, scales, rise_logical):
        box = frame.getchannel("A").getbbox()
        if box is None:
            raise ValueError("Depth sequence frame is empty")
        pose = frame.crop(box)
        pose = pose.resize(
            (max(1, round(pose.width * scale)), max(1, round(pose.height * scale))),
            Image.Resampling.LANCZOS,
        )
        pose.putalpha(pose.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        canvas = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        bottom = frame.height - 2 - round(rise * D)
        canvas.alpha_composite(pose, ((frame.width - pose.width) // 2, bottom - pose.height))
        result.append(canvas)
    return result


def height_normalise_sequence(frames, heights_logical):
    """Restore a generated pose sequence to explicit canonical body heights."""
    if len(frames) != len(heights_logical):
        raise ValueError("Height targets must match the frame count")
    result = []
    for frame, logical_height in zip(frames, heights_logical):
        box = frame.getchannel("A").getbbox()
        if box is None:
            raise ValueError("Height-normalised frame is empty")
        pose = frame.crop(box)
        pose = pose.resize((pose.width, round(logical_height * D)), Image.Resampling.LANCZOS)
        pose.putalpha(pose.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        canvas = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        canvas.alpha_composite(pose, ((frame.width - pose.width) // 2, frame.height - 2 - pose.height))
        result.append(canvas)
    return result


def match_reference_heights(frames, references):
    """Match each generated actor frame to its canonical pose height."""
    if len(frames) != len(references):
        raise ValueError("Reference height sequence must match the frame count")
    result = []
    for frame, reference in zip(frames, references):
        box = frame.getchannel("A").getbbox()
        reference_box = reference.getchannel("A").getbbox()
        if box is None or reference_box is None:
            raise ValueError("Height-matched frame or reference is empty")
        pose = frame.crop(box)
        target_height = reference_box[3] - reference_box[1]
        scale = target_height / pose.height
        pose = pose.resize((max(1, round(pose.width * scale)), target_height), Image.Resampling.LANCZOS)
        pose.putalpha(pose.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        canvas = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        canvas.alpha_composite(pose, ((frame.width - pose.width) // 2, frame.height - 2 - pose.height))
        result.append(canvas)
    return result


def embed_frame(frame, logical_width, logical_height):
    """Centre a smaller canonical frame on a larger bottom-anchored canvas."""
    canvas = Image.new("RGBA", (logical_width * D, logical_height * D), (0, 0, 0, 0))
    canvas.alpha_composite(frame, ((canvas.width - frame.width) // 2, canvas.height - frame.height))
    return canvas


def rotate_embedded_frame(frame, logical_width, logical_height, angle, offset_x=0):
    """Rotate an already-authored frame gently without changing actor scale."""
    canvas = embed_frame(frame, logical_width, logical_height)
    rotated = canvas.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
    rotated.putalpha(rotated.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
    if not offset_x:
        return rotated
    shifted = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
    shifted.alpha_composite(rotated, (round(offset_x * D), 0))
    return shifted


def bare_head_frame(base):
    """Replace the captain cap with a small bare white-haired crown."""
    original = base.copy()
    frame = base.copy()
    # Generated canonical heads consistently reserve the first eight logical
    # pixels for the cap. Rebuild only that headwear band; the approved face and
    # beard below it remain byte-for-byte source pixels.
    ImageDraw.Draw(frame).rectangle((0, 0, frame.width, 8 * D), fill=(0, 0, 0, 0))
    crown = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(crown)
    ellipse(draw, (10, 2, 23, 14), CREAM, INK, 2)
    ellipse(draw, (11, 5, 22, 16), SKIN, INK, 2)
    rect(draw, (11, 5, 21, 8), SKIN_HI)
    # Put the preserved lower face, ears and beard back over the reconstructed
    # crown so no party variant can acquire a different beard silhouette.
    rebuilt = crown.copy()
    crown.alpha_composite(frame)
    pixels = crown.load()
    original_pixels = original.load()
    rebuilt_pixels = rebuilt.load()
    for y in range(min(15 * D, crown.height)):
        for x in range(crown.width):
            original_red, original_green, original_blue, original_alpha = original_pixels[x, y]
            if original_alpha and original_blue > original_red * 1.2 and original_blue > original_green * 1.05:
                pixels[x, y] = rebuilt_pixels[x, y]
                continue
            red, green, blue, alpha = pixels[x, y]
            if alpha and blue > red * 1.2 and blue > green * 1.05:
                pixels[x, y] = (*ImageColor.getrgb(CREAM), alpha)
    return crown


def draw_party_hat(draw, center_x=16, base_y=13):
    """Draw the approved small paper party hat from the supplied reference."""
    # A deliberately modest paper cone worn instead of the captain's cap.
    poly(draw, [(center_x - 4, base_y - 1), (center_x, base_y - 9), (center_x + 4, base_y - 1)], "#f1c7ca", INK, 1)
    poly(draw, [(center_x - 3, base_y - 2), (center_x, base_y - 8), (center_x, base_y - 2)], "#f7dadd", None)
    ellipse(draw, (center_x - 1.5, base_y - 12, center_x + 1.5, base_y - 9), "#c62828", INK, 1)
    rect(draw, (center_x - 4, base_y - 2, center_x + 4, base_y), "#c62828", INK, 1)
    # Uneven paper fringe, as in the user's physical reference.
    poly(draw, [(center_x - 4, base_y), (center_x - 3, base_y + 1.5), (center_x - 1, base_y), (center_x, base_y + 1.5), (center_x + 2, base_y), (center_x + 3, base_y + 1.5), (center_x + 4, base_y)], "#d32f2f", None)


def party_hat_frames(base_frames):
    """Add small party headwear without redrawing/rescaling keeper identity."""
    result = []
    for base in base_frames:
        frame = Image.new("RGBA", (32 * D, 48 * D), (0, 0, 0, 0))
        frame.alpha_composite(bare_head_frame(base), (0, 8 * D))
        draw_party_hat(ImageDraw.Draw(frame), base_y=12)
        result.append(frame)
    return result


def party_hat_put_on_back_frames(idle_frames, raised_frames):
    """Back-view reveal: lift the loose hat behind the body onto the cap."""
    # Recombine approved rear-view frames: stable idle legs with the canonical
    # ladder-climb upper-body reach. No keeper anatomy is regenerated.
    raised_indices = (None, 7, 2, 3, 3, 2, 7, None)
    hat_base_y = (40, 33, 25, 18, 13, 13, 13, 13)
    frames = []
    for step, raised_index in enumerate(raised_indices):
        actor = bare_head_frame(idle_frames[0])
        if raised_index is not None:
            raised = bare_head_frame(raised_frames[raised_index])
            ImageDraw.Draw(actor).rectangle((0, 8 * D, actor.width, 25 * D), fill=(0, 0, 0, 0))
            actor.alpha_composite(raised.crop((0, 8 * D, actor.width, 25 * D)), (0, 8 * D))
        frame = Image.new("RGBA", (32 * D, 48 * D), (0, 0, 0, 0))
        base_y = hat_base_y[step]
        if 2 <= step < 5:
            # Drawing first makes the loose hat rise behind his torso/head;
            # only the emerging top is visible until it reaches the cap.
            draw_party_hat(ImageDraw.Draw(frame), center_x=16, base_y=base_y)
        frame.alpha_composite(actor, (0, 8 * D))
        if step >= 4:
            draw_party_hat(ImageDraw.Draw(frame), center_x=16, base_y=12)
        frames.append(frame)
    return frames


def party_cake_eat_frames(base_frames):
    """Party-hat variant of the approved seated eating loop with cake slice."""
    result = []
    for base in base_frames:
        frame = Image.new("RGBA", (40 * D, 48 * D), (0, 0, 0, 0))
        frame.alpha_composite(bare_head_frame(base), (0, 8 * D))
        draw = ImageDraw.Draw(frame)
        draw_party_hat(draw, base_y=12)
        # Small plate and a readable slice of the established jam-layer cake.
        ellipse(draw, (29, 32, 39, 34), CREAM_HI, INK, 1)
        poly(draw, [(31, 28), (38, 29), (38, 32), (31, 32)], "#e7b86b", INK, 1)
        rect(draw, (31, 30, 38, 31), "#b72e3b")
        rect(draw, (31, 27, 38, 29), CREAM_HI)
        ellipse(draw, (34.5, 25.5, 36.5, 28), "#c62828", INK, 1)
        result.append(frame)
    return result


def remove_small_alpha_components(frame, min_pixels=200):
    """Remove neighbouring-cell flecks while retaining actor and released props."""
    width, height = frame.size
    pixels = bytearray(frame.getchannel("A").tobytes())
    source = pixels[:]
    keep = bytearray(width * height)
    for start, value in enumerate(source):
        if not value:
            continue
        source[start] = 0
        pending = [start]
        members = []
        while pending:
            index = pending.pop()
            members.append(index)
            y, x = divmod(index, width)
            for neighbour in (index - 1, index + 1, index - width, index + width):
                if 0 <= neighbour < width * height and source[neighbour] and (neighbour // width == y or neighbour % width == x):
                    source[neighbour] = 0
                    pending.append(neighbour)
        if len(members) >= min_pixels:
            for index in members:
                keep[index] = 255
    cleaned = frame.copy()
    cleaned.putalpha(Image.frombytes("L", frame.size, bytes(keep)))
    return cleaned


def place_on_vertical_action_canvas(frames, logical_height, rise_by_frame):
    """Preserve authored poses while giving a jump a real world-space arc."""
    if len(frames) != len(rise_by_frame):
        raise ValueError("Vertical action offsets must match the frame count")
    width = frames[0].width
    source_height = frames[0].height
    target_height = logical_height * D
    result = []
    for frame, rise in zip(frames, rise_by_frame):
        placed = Image.new("RGBA", (width, target_height), (0, 0, 0, 0))
        placed.alpha_composite(frame, (0, target_height - source_height - round(rise * D)))
        result.append(placed)
    return result


def recolor_privacy_mosaic(frame):
    """Change only lower-body blue privacy pixels to opaque flesh tones."""
    result = frame.copy()
    pixels = result.load()
    for y in range(18 * D, result.height):
        for x in range(result.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha and blue > red * 1.12 and blue > green * 1.03:
                shade = SKIN_D if (x // D + y // D) % 2 else SKIN
                pixels[x, y] = (*ImageColor.getrgb(shade), alpha)
    return result


def draw_video_game_controller(frame):
    """Overlay a readable oversized white dual-grip controller at the hands."""
    result = frame.copy()
    draw = ImageDraw.Draw(result)
    poly(draw, [(19, 20), (22, 18), (26, 18), (29, 20), (28, 25), (25, 23), (23, 23), (20, 25)], CREAM_HI, INK, 1)
    ellipse(draw, (21, 20, 22.5, 21.5), BLUE_D, None)
    ellipse(draw, (26, 20, 27.5, 21.5), BLUE_D, None)
    return result


def draw_held_record(frame, center=(46, 25)):
    """Keep the black vinyl readable after it separates from the hand."""
    result = frame.copy()
    draw = ImageDraw.Draw(result)
    ellipse(draw, (center[0] - 4, center[1] - 4, center[0] + 4, center[1] + 4), "#171719", INK, 1)
    ellipse(draw, (center[0] - 1.25, center[1] - 1.25, center[0] + 1.25, center[1] + 1.25), "#c62828", None)
    return result


def repair_fishing_actor(frame, actor_template, prop_start_x=50):
    """Retain a complete keeper while taking the changing rod/fish from a pose."""
    result = actor_template.copy()
    box = (prop_start_x * D, 0, frame.width, frame.height)
    ImageDraw.Draw(result).rectangle(box, fill=(0, 0, 0, 0))
    result.alpha_composite(frame.crop(box), (box[0], 0))
    return result


def snooker_frames():
    """Extract the eight overlapping source poses without neighbouring actors."""
    source = Image.open(Path(__file__).with_name("keeper-snooker-generated-source.png")).convert("RGBA")
    # Discard isolated generation flecks below the shared feet line before
    # measuring scale; otherwise invisible debris makes the keeper tiny.
    source = source.crop((0, 130, source.width, 580))
    # These ranges follow the actual pose centres rather than equal sheet cells.
    ranges = ((0, 245), (235, 522), (470, 800), (730, 995), (975, 1265), (1270, 1578), (1530, 1848), (1790, 2172))
    poses = []
    for x0, x1 in ranges:
        pose = source.crop((x0, 0, x1, source.height))
        box = pose.getchannel("A").getbbox()
        if box is None:
            raise ValueError("Empty snooker pose")
        poses.append(pose.crop(box))

    tallest = max(pose.height for pose in poses)
    widest = max(pose.width for pose in poses)
    scale = min(152 / tallest, 184 / widest)
    frames = []
    for pose in poses:
        pose = pose.resize((round(pose.width * scale), round(pose.height * scale)), Image.Resampling.LANCZOS)
        pose.putalpha(pose.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        frame = Image.new("RGBA", (48 * D, 40 * D), (0, 0, 0, 0))
        frame.alpha_composite(pose, ((frame.width - pose.width) // 2, frame.height - 2 - pose.height))
        frames.append(frame)

    # Remove only the adjacent-pose incursions. The two cue tips that share
    # those contaminated regions are restored below as prop-only pixels.
    clear_rectangles = {
        0: ((130, 105, 192, 160),),
        1: ((0, 0, 52, 160), (125, 0, 192, 160)),
        2: ((0, 0, 38, 160), (125, 0, 192, 160)),
        3: ((0, 0, 45, 160),),
        4: ((0, 0, 62, 160),),
        5: ((0, 0, 60, 160),),
        6: ((0, 0, 58, 160),),
        7: ((0, 0, 60, 160),),
    }
    for frame_index, rectangles in clear_rectangles.items():
        draw = ImageDraw.Draw(frames[frame_index])
        for box in rectangles:
            draw.rectangle(box, fill=(0, 0, 0, 0))
    # Restore the two forward cue extensions after the neighbouring boots have
    # been removed. These are prop pixels only; keeper anatomy is untouched.
    for frame_index, start_x in ((1, 122), (2, 128)):
        draw = ImageDraw.Draw(frames[frame_index])
        draw.rectangle((start_x, 87, 170, 95), fill=INK)
        draw.rectangle((start_x, 89, 166, 93), fill="#a9683c")
        draw.rectangle((166, 89, 171, 93), fill=CREAM_HI)
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


DEFAULT_KEEPER_ANIMATION_FPS = 4
# Add accepted per-clip review choices here. Any animated clip not listed uses
# the global 4fps baseline; one-frame technical parts remain at 0fps.
KEEPER_FPS_OVERRIDES = {
    "keeper_artist_smock_sit_front": 4.5,
    "keeper_bathrobe_walk": 8,
    "keeper_bbq_back": 2.5,
    "keeper_cake_from_oven_back": 4.5,
    "keeper_cake_turn_right": 7.5,
    "keeper_carry_cake": 8,
    "keeper_carry_meal": 8,
    "keeper_carry_shopping": 8,
    "keeper_check_instrument_back": 6,
    "keeper_clear_snow": 3.5,
    "keeper_count_money": 6,
    "keeper_cross": 5.5,
    "keeper_darts": 3,
    "keeper_door_open_back": 5.5,
    "keeper_door_open_side": 5,
    "keeper_feed_animals": 5.5,
    "keeper_fish_feed_up": 5,
    "keeper_fish_seated": 3,
    "keeper_get_into_bed": 3,
    "keeper_hammer_back": 5,
    "keeper_hammer_side": 5,
    "keeper_pyjamas_snore": 1,
    "keeper_row_boat": 3,
    "keeper_shower_wash": 2,
    "keeper_trampoline_front": 7.5,
    "keeper_turn_back": 10.5,
    "keeper_type_computer": 8.5,
    "keeper_work_back": 3,
}

REVIEW_EXPORT = ROOT / "docs/review/frank-keeper-animation-review-2026-10-09.json"
REVIEW_SETTINGS = {
    review["name"]: review
    for review in json.loads(REVIEW_EXPORT.read_text())["reviews"]
} if REVIEW_EXPORT.exists() else {}
REVIEW_POINT_FIELDS = (
    "seat_point", "hand_use_point", "pedal_point", "bowl_point",
    "look_target_point", "bed_surface_point", "pillow_point", "pivot",
)


def apply_review_geometry(name, frames, metadata):
    """Bake Frank's visual scale choices and modest alignment choices."""
    review = REVIEW_SETTINGS.get(name)
    if not review:
        return frames, metadata
    scale_x = review.get("widthPercent", 100) / 100
    scale_y = review.get("heightPercent", 100) / 100
    offset_x = review.get("actionOffsetX", 0)
    offset_y = review.get("actionOffsetY", 0)
    # Frank's saved width and height are production art direction, including
    # costume walks and clips also marked for redraft.  Canonical anatomy still
    # governs the drawing, but it must never silently override his visual size.
    # The comparison viewer also permits large staging translations. Those are
    # evidence for scene placement, not safe actor-sheet corrections. Small
    # alignment nudges are production choices and are baked here.
    if abs(offset_x) > 8:
        offset_x = 0
    if abs(offset_y) > 8:
        offset_y = 0
    reviewed_metadata = dict(metadata)
    reviewed_metadata["review_scale"] = [
        review.get("widthPercent", 100),
        review.get("heightPercent", 100),
    ]
    reviewed_metadata["review_offset"] = [offset_x, offset_y]
    if scale_x == 1 and scale_y == 1 and offset_x == 0 and offset_y == 0:
        return frames, reviewed_metadata

    old_width, old_height = frames[0].size
    anchor = metadata.get("anchor_point", [old_width / D / 2, old_height / D])
    anchor_px = (anchor[0] * D, anchor[1] * D)
    scaled_size = (max(1, round(old_width * scale_x)), max(1, round(old_height * scale_y)))
    origin = (
        round(anchor_px[0] - anchor_px[0] * scale_x + offset_x * D),
        round(anchor_px[1] - anchor_px[1] * scale_y + offset_y * D),
    )
    scaled_frames = []
    for frame in frames:
        scaled = frame.resize(scaled_size, Image.Resampling.LANCZOS)
        scaled.putalpha(scaled.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        if scaled.getchannel("A").getbbox() is None:
            raise ValueError(f"Review transform produced an empty frame for {name}")
        scaled_frames.append(scaled)

    # Transparent canvas is contractual staging space, not disposable padding:
    # it carries long tools, object contacts and future effects. Preserve the
    # full authored canvas as a minimum, and expand only where the transformed
    # full frame crosses an edge. Never crop back to the visible alpha bounds.
    min_x = math.floor(min(0, origin[0]) / D) * D
    min_y = math.floor(min(0, origin[1]) / D) * D
    max_x = math.ceil(max(old_width, origin[0] + scaled_size[0]) / D) * D
    max_y = math.ceil(max(old_height, origin[1] + scaled_size[1]) / D) * D
    canvas_size = (max_x - min_x, max_y - min_y)
    transformed = []
    for scaled in scaled_frames:
        canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        canvas.alpha_composite(scaled, (origin[0] - min_x, origin[1] - min_y))
        transformed.append(canvas)

    adjusted = reviewed_metadata
    adjusted["anchor_point"] = [
        round((anchor_px[0] - min_x) / D, 3),
        round((anchor_px[1] - min_y) / D, 3),
    ]
    for field in REVIEW_POINT_FIELDS:
        if field not in adjusted:
            continue
        point = adjusted[field]
        adjusted[field] = [
            round((anchor_px[0] + (point[0] * D - anchor_px[0]) * scale_x + offset_x * D - min_x) / D, 3),
            round((anchor_px[1] + (point[1] * D - anchor_px[1]) * scale_y + offset_y * D - min_y) / D, 3),
        ]
    return transformed, adjusted


def contract(frames, fps, pivot=None, *, w=32, h=40, anchor_point=None, loop=True, seat_point=None, hand_use_point=None, pedal_point=None, bowl_point=None, look_target_point=None, bed_surface_point=None, pillow_point=None, movement_vector=None, depth_scale_range=None, depth_offset_y=None, prop_handoff_frame=None, prop_variant=None, upgrade_tier=None, start_pose=None, end_pose=None, outfit=None, reverse_for=None, mirror_safe=False, facing=None, interaction=None, mirrors_for=None, review_scale=None, review_offset=None):
    value = {"w": w, "h": h, "frames": frames, "fps": fps, "density": D, "anchor": anchor_point or [w // 2, h], "z": 50}
    if pivot is not None: value["pivot"] = pivot
    value["loop"] = loop
    if seat_point is not None: value["seatPoint"] = seat_point
    if hand_use_point is not None: value["handUsePoint"] = hand_use_point
    if pedal_point is not None: value["pedalPoint"] = pedal_point
    if bowl_point is not None: value["bowlPoint"] = bowl_point
    if look_target_point is not None: value["lookTargetPoint"] = look_target_point
    if bed_surface_point is not None: value["bedSurfacePoint"] = bed_surface_point
    if pillow_point is not None: value["pillowPoint"] = pillow_point
    if movement_vector is not None: value["movementVector"] = movement_vector
    if depth_scale_range is not None: value["depthScaleRange"] = depth_scale_range
    if depth_offset_y is not None: value["depthOffsetY"] = depth_offset_y
    if prop_handoff_frame is not None: value["propHandoffFrame"] = prop_handoff_frame
    if prop_variant is not None: value["propVariant"] = prop_variant
    if upgrade_tier is not None: value["upgradeTier"] = upgrade_tier
    if start_pose is not None: value["startPose"] = start_pose
    if end_pose is not None: value["endPose"] = end_pose
    if outfit is not None: value["outfit"] = outfit
    if reverse_for is not None: value["reverseFor"] = reverse_for
    if mirror_safe: value["mirrorSafe"] = True
    if facing is not None: value["facing"] = facing
    if interaction is not None: value["interaction"] = interaction
    if mirrors_for is not None: value["mirrorsFor"] = mirrors_for
    if review_scale is not None: value["reviewScale"] = review_scale
    if review_offset is not None: value["reviewOffset"] = review_offset
    return value


def save(name, frames, legacy_fps=0, pivot=None, **metadata):
    # legacy_fps preserves the original cadence hints at existing call sites;
    # production timing is now governed solely by the baseline/override policy.
    if pivot is not None:
        metadata["pivot"] = pivot
        pivot = None
    frames, metadata = apply_review_geometry(name, frames, metadata)
    pivot = metadata.pop("pivot", pivot)
    frame_width = frames[0].width
    frame_height = frames[0].height
    if any(frame.size != (frame_width, frame_height) for frame in frames):
        raise ValueError(f"Mismatched frame sizes for {name}")
    strip = Image.new("RGBA", (frame_width * len(frames), frame_height), (0, 0, 0, 0))
    for i, frame in enumerate(frames): strip.alpha_composite(frame, (i * frame_width, 0))
    png = OUT / f"{name}_f{len(frames)}.png"
    # Frame-count revisions change the filename. Remove only obsolete generated
    # variants of this exact animation so audits never count stale strips.
    for stale in (*OUT.glob(f"{name}_f*.png"), *OUT.glob(f"{name}_f*.json")):
        if stale not in {png, png.with_suffix(".json")}:
            stale.unlink()
    strip.save(png, optimize=True)
    authored_fps = 0 if len(frames) == 1 else KEEPER_FPS_OVERRIDES.get(name, DEFAULT_KEEPER_ANIMATION_FPS)
    png.with_suffix(".json").write_text(json.dumps(contract(len(frames), authored_fps, pivot, w=frame_width // D, h=frame_height // D, **metadata), indent=2) + "\n")


def save_preview(name, frames, duration, ping_pong=False):
    runtime_name = name.replace("-", "_")
    duration = round(1000 / KEEPER_FPS_OVERRIDES.get(runtime_name, DEFAULT_KEEPER_ANIMATION_FPS))
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
turn_front_frames = height_normalise_sequence(
    generated_frames("keeper-turn-front-generated-source.png", 6),
    (38, 38, 38, 38, 38, 38),
)
work_frames = generated_frames("keeper-work-back-generated-source.png", 8)
sit_side_frames = generated_frames("keeper-sit-side-generated-source.png", 6)
nap_seated_frames = match_reference_heights(
    generated_frames("keeper-nap-seated-generated-source.png", 8),
    [sit_side_frames[-1]] * 8,
)
sit_front_frames = generated_frames("keeper-sit-front-generated-source.png", 6, horizontal_scale=0.88)
sit_back_frames = height_normalise_sequence(
    generated_frames("keeper-sit-back-generated-source.png", 6),
    (38, 37, 36, 35, 34, 34),
)
sitting_turn_back_to_rear_frames = height_normalise_sequence(
    generated_frames("keeper-sitting-turn-back-to-rear-generated-source.png", 4),
    (34, 34, 34, 34),
)
piano_frames = generated_frames("keeper-piano-generated-source.png", 8, scale_multiplier=0.90)
urinate_frames = generated_frames("keeper-loo-stand-generated-source.png", 6)
eat_seated_frames = generated_frames("keeper-eat-seated-generated-source.png", 8, scale_multiplier=0.90)
# Keep the knife and fork in their established hands through the middle of the
# loop; the previous two generated poses silently swapped and duplicated them.
eat_seated_frames[4:6] = [eat_seated_frames[2].copy(), eat_seated_frames[3].copy()]
door_side_frames = generated_frames("keeper-door-side-generated-source.png", 6)
door_back_frames = generated_frames("keeper-door-back-generated-source.png", 6)
ladder_frames = generated_frames("keeper-ladder-generated-source.png", 8)
stairs_up_frames = generated_frames("keeper-stairs-up-generated-source.png", 8)
stairs_down_frames = generated_frames("keeper-stairs-down-generated-source.png", 8)
switch_side_frames = generated_frames("keeper-switch-side-generated-source.png", 6)
switch_back_frames = generated_frames("keeper-switch-back-generated-source.png", 6)
walk_into_lift_frames = depth_scale_sequence(
    generated_frames("keeper-walk-into-lift-generated-source.png", 8),
    (1.0, 0.94, 0.88, 0.81, 0.75, 0.75, 0.75, 0.75),
    (0, 1.5, 3, 4.5, 6, 6, 6, 6),
)
parachute_jump_frames = generated_frames("keeper-parachute-jump-generated-source.png", 9, logical_width=48, logical_height=84, scale_reference_index=0)
reviewed_parachute_jump_frames, _ = apply_review_geometry(
    "keeper_parachute_jump",
    parachute_jump_frames,
    {"anchor_point": [24, 84]},
)
parachute_drift_frames = [
    rotate_embedded_frame(reviewed_parachute_jump_frames[-1], 96, 84, angle, offset)
    for angle, offset in ((0, 0), (-1, -0.5), (-2, -1), (-1, -0.5), (0, 0), (1, 0.5), (2, 1), (1, 0.5))
]
parachute_landing_source_frames = generated_frames(
    "keeper-parachute-landing-generated-source.png", 10,
    logical_width=64, logical_height=84, force_equal_cells=True,
)
reviewed_parachute_landing_frames, _ = apply_review_geometry(
    "keeper_parachute_jump",
    parachute_landing_source_frames,
    {"anchor_point": [32, 84]},
)
parachute_landing_frames = [embed_frame(frame, 96, 84) for frame in reviewed_parachute_landing_frames]
# The controller exits the loop at its neutral/open-canopy phase, so all three
# route pieces share the same byte-exact hand-off frame.
parachute_landing_frames[0] = parachute_drift_frames[0].copy()
platform_dive_frames = generated_frames("keeper-platform-dive-generated-source.png", 10, logical_width=48, logical_height=56, scale_reference_index=0)
dig_frames = generated_frames("keeper-dig-generated-source.png", 8)
feed_animals_frames = generated_frames("keeper-feed-animals-generated-source.png", 8)
sow_seeds_frames = generated_frames("keeper-sow-seeds-generated-source.png", 8)
pick_vegetable_frames = generated_frames("keeper-pick-vegetable-generated-source.png", 8)
pick_fruit_frames = generated_frames("keeper-pick-fruit-generated-source.png", 8)
carry_shopping_frames = generated_frames("keeper-carry-shopping-generated-source.png", 8)
row_boat_frames = generated_frames("keeper-row-boat-generated-source.png", 8, logical_width=40, scale_multiplier=0.90)
drive_speedboat_frames = generated_frames("keeper-drive-speedboat-generated-source.png", 8, scale_multiplier=0.90)
operate_outboard_frames = generated_frames("keeper-operate-outboard-generated-source.png", 8)
watch_tv_frames = generated_frames("keeper-watch-tv-generated-source.png", 8, scale_multiplier=0.90)
weld_frames = generated_frames("keeper-weld-generated-source.png", 8)
saw_wood_frames = [
    remove_small_alpha_components(frame, min_pixels=300)
    for frame in generated_frames("keeper-saw-wood-generated-source.png", 8, logical_width=64, preserve_equal_cells=True)
]
for saw_frame in saw_wood_frames:
    ImageDraw.Draw(saw_frame).rectangle(
        (saw_frame.width - 6 * D, 0, saw_frame.width, saw_frame.height),
        fill=(0, 0, 0, 0),
    )
wave_camera_frames = generated_frames("keeper-wave-generated-source.png", 8)
yawn_frames = generated_frames("keeper-yawn-generated-source.png", 8)
pyjamas_walk_frames = generated_frames("keeper-pyjamas-walk-light-blue-generated-source.png", 8)
pyjamas_turn_back_frames = generated_frames("keeper-pyjamas-turn-back-light-blue-generated-source.png", 6)
pyjamas_door_side_frames = generated_frames("keeper-door-side-pyjamas-generated-source.png", 6)
get_into_bed_frames = generated_frames("keeper-get-into-bed-light-blue-generated-source.png", 8, logical_width=48, min_component_pixels=10000)
pyjamas_snore_frames = generated_frames("keeper-snore-light-blue-generated-source.png", 6, logical_width=48)
swim_costume_horizontal_frames = generated_frames("keeper-swim-costume-horizontal-generated-source.png", 8, logical_width=80, logical_height=48)
swim_costume_up_frames = generated_frames("keeper-swim-costume-up-generated-source.png", 8, logical_width=48, logical_height=48)
swim_costume_down_frames = generated_frames("keeper-swim-costume-down-generated-source.png", 8, logical_width=48, logical_height=48)
scuba_horizontal_frames = generated_frames(
    "keeper-scuba-horizontal-generated-source.png", 8,
    logical_width=80, logical_height=48,
)
scuba_up_frames = generated_frames(
    "keeper-scuba-up-generated-source.png", 8,
    logical_width=48, logical_height=48,
)
scuba_down_frames = generated_frames(
    "keeper-scuba-down-generated-source.png", 8,
    logical_width=48, logical_height=48,
)
scuba_walk_side_frames = generated_frames(
    "keeper-scuba-walk-side-generated-source.png", 8,
    logical_width=48, logical_height=56, preserve_equal_cells=True, scale_multiplier=0.84,
)
scuba_jetty_dive_frames = generated_frames(
    "keeper-scuba-jetty-dive-generated-source.png", 12,
    logical_width=80, logical_height=72, group_equal_components=True,
)
# The final dive pose is the exact first production swim frame, so there is no
# costume, beard, scale or silhouette pop at the water-entry hand-off.
reviewed_scuba_horizontal_frames, _ = apply_review_geometry(
    "keeper_scuba_swim_horizontal",
    scuba_horizontal_frames,
    {"anchor_point": [40, 24]},
)
scuba_jetty_dive_frames[-1] = embed_frame(reviewed_scuba_horizontal_frames[0], 80, 72)
# Party costume is headwear-only.  Derive every pose from the approved keeper
# families so the face, skull, beard and body can never drift between costumes.
party_idle_reference = generated_frames("keeper-wave-generated-source.png", 8)
party_idle_frames = party_hat_frames([party_idle_reference[index] for index in (0, 1, 7, 0)])
party_walk_frames = party_hat_frames(walk_frames)
party_turn_back_frames = party_hat_frames(turn_frames)
party_hat_put_on_back = party_hat_put_on_back_frames(work_frames, ladder_frames)
party_cake_eat = party_cake_eat_frames(eat_seated_frames)
souwester_side_frames = generated_frames("keeper-souwester-walk-side-generated-source.png", 8, logical_height=48, scale_multiplier=0.86)
souwester_back_frames = generated_frames("keeper-souwester-walk-back-generated-source.png", 8, logical_height=48, scale_multiplier=0.86)
souwester_front_frames = generated_frames("keeper-souwester-walk-front-generated-source.png", 8, logical_height=48, scale_multiplier=0.86)
dance_frames = generated_frames("keeper-dance-generated-source.png", 8)
party_dance_frames = party_hat_frames(dance_frames)
play_guitar_frames = generated_frames("keeper-play-guitar-generated-source.png", 8, logical_width=48)
artist_smock_walk_frames = match_reference_heights(
    generated_frames("keeper-artist-smock-walk-generated-source.png", 8, horizontal_scale=1.08),
    walk_frames,
)
artist_smock_turn_back_frames = match_reference_heights(
    generated_frames("keeper-artist-smock-turn-back-generated-source.png", 6),
    turn_frames,
)
artist_smock_turn_front_frames = height_normalise_sequence(
    generated_frames("keeper-artist-smock-turn-front-generated-source.png", 6),
    (38, 38, 38, 38, 38, 38),
)
artist_smock_sit_front_frames = match_reference_heights(
    generated_frames("keeper-artist-smock-sit-front-generated-source.png", 6),
    sit_front_frames,
)
play_guitar_gretsch_frames = match_reference_heights(
    generated_frames("keeper-play-guitar-gretsch-generated-source.png", 8, logical_width=48),
    play_guitar_frames,
)
play_guitar_flying_v_frames = match_reference_heights(
    generated_frames("keeper-play-guitar-flying-v-1967-generated-source.png", 8, logical_width=64),
    [embed_frame(frame, 64, 40) for frame in play_guitar_frames],
)
guitar_pickup_acoustic_frames = generated_frames(
    "keeper-guitar-pickup-acoustic-generated-source.png", 12,
    logical_width=64, logical_height=56, force_equal_cells=True, scale_reference_index=0,
)
guitar_pickup_gretsch_frames = generated_frames(
    "keeper-guitar-pickup-gretsch-generated-source.png", 12,
    logical_width=64, logical_height=56, force_equal_cells=True, scale_reference_index=0,
)
guitar_pickup_flying_v_frames = generated_frames(
    "keeper-guitar-pickup-flying-v-1967-generated-source.png", 12,
    logical_width=64, logical_height=56, force_equal_cells=True, scale_reference_index=0,
)
pickup_start = embed_frame(turn_frames[0], 64, 56)
guitar_pickup_acoustic_frames[0] = pickup_start
guitar_pickup_acoustic_frames[-1] = embed_frame(play_guitar_frames[0], 64, 56)
guitar_pickup_gretsch_frames[0] = pickup_start
guitar_pickup_gretsch_frames[-1] = embed_frame(play_guitar_gretsch_frames[0], 64, 56)
guitar_pickup_flying_v_frames[0] = pickup_start
guitar_pickup_flying_v_frames[-1] = embed_frame(play_guitar_flying_v_frames[0], 64, 56)
play_drums_front_frames = generated_frames("keeper-play-drums-front-generated-source.png", 8, logical_height=48, scale_multiplier=0.90)
# Front is the timing and anatomy master. The rear source has more transparent
# height around its sticks, so independent fit-to-bounds makes its seated body
# about 10% smaller. Normalise the actor height while preserving body width.
play_drums_back_frames = generated_frames(
    "keeper-play-drums-back-generated-source.png",
    8,
    logical_height=48,
    scale_multiplier=0.99,
    horizontal_scale=0.95,
)
# Frame 6 repeats the front sheet's single raised screen-left stroke. A 180°
# viewpoint change places that physical arm on screen-right in the rear view.
play_drums_back_frames[5] = ImageOps.mirror(play_drums_back_frames[5])
watch_movie_frames = generated_frames("keeper-watch-movie-generated-source.png", 8, logical_width=48, scale_multiplier=0.90)
clear_snow_frames = generated_frames("keeper-clear-snow-generated-source.png", 8, logical_width=48)
lawn_mower_push_frames = match_reference_heights(
    generated_frames(
        "keeper-lawn-mower-push-generated-source.png",
        8,
        logical_width=48,
        preserve_equal_cells=True,
    ),
    walk_frames,
)
sweep_broom_frames = match_reference_heights(
    generated_frames(
        "keeper-sweep-broom-generated-source.png",
        8,
        logical_width=48,
        preserve_equal_cells=True,
    ),
    walk_frames,
)
hoover_basic_frames = match_reference_heights(
    generated_frames(
        "keeper-hoover-basic-generated-source.png",
        8,
        logical_width=48,
        preserve_equal_cells=True,
    ),
    walk_frames,
)
hoover_super_frames = match_reference_heights(
    generated_frames(
        "keeper-hoover-super-generated-source.png",
        8,
        logical_width=48,
        preserve_equal_cells=True,
    ),
    walk_frames,
)
crouch_work_back_frames = generated_frames("keeper-crouch-work-back-generated-source.png", 8)
# Frame 5 placed both hands behind the hips. Reuse the preceding correctly
# layered low-work pose; the neighbouring frames preserve the bend/rise motion.
crouch_work_back_frames[4] = crouch_work_back_frames[3].copy()
cake_from_oven_back_frames = generated_frames("keeper-cake-from-oven-back-generated-source.png", 8, logical_width=48)
cake_turn_right_frames = generated_frames("keeper-cake-turn-right-generated-source.png", 6, logical_width=48)
carry_cake_frames = generated_frames("keeper-carry-cake-generated-source.png", 8, logical_width=48)
carry_meal_frames = generated_frames("keeper-carry-meal-generated-source.png", 8, logical_width=48)
place_cake_frames = generated_frames("keeper-place-cake-generated-source.png", 8, logical_width=48, preserve_equal_cells=True)
place_cake_frames = [remove_small_alpha_components(frame) for frame in place_cake_frames]
save("keeper_walk", walk_frames, 10, mirror_safe=True)
save("keeper_turn_back", turn_frames, 8, loop=False, reverse_for="turn_front")
save("keeper_turn_front", turn_front_frames, 8, loop=False, reverse_for="turn_side_from_front", facing="right-to-front", interaction="turn-front")
save("keeper_work_back", work_frames, 8, hand_use_point=[16, 21])
save("keeper_cook_back", work_frames, 8, hand_use_point=[16, 21])
save("keeper_wash_back", work_frames, 8, hand_use_point=[16, 21])
save("keeper_brush_teeth_back", work_frames, 8, hand_use_point=[16, 21])
save("keeper_sit_side", sit_side_frames, 8, loop=False, seat_point=[16, 29], reverse_for="stand_side", mirror_safe=True)
save("keeper_nap_seated", nap_seated_frames, 8, seat_point=[16, 29], mirror_safe=True, start_pose="sitting-side-right", end_pose="sitting-side-right", facing="right", interaction="nap-seated", mirrors_for="left")
save("keeper_sit_front", sit_front_frames, 8, loop=False, seat_point=[16, 29], reverse_for="stand_front")
save("keeper_sit_back", sit_back_frames, 8, loop=False, seat_point=[16, 29], reverse_for="stand_back", facing="back")
save("keeper_sitting_turn_back_to_rear", sitting_turn_back_to_rear_frames, 8, loop=False, seat_point=[16, 29], reverse_for="sitting_turn_rear_to_back", facing="back-to-rear-right", interaction="turn-seated")
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
save("keeper_walk_into_lift", walk_into_lift_frames, 8, loop=False, movement_vector=[0, -1], depth_scale_range=[1.0, 0.75], depth_offset_y=[0, -6], facing="back-to-front", interaction="enter-lift")
save("keeper_parachute_jump", parachute_jump_frames, 10, loop=False, mirror_safe=True, facing="right", interaction="parachute-jump", mirrors_for="left")
save("keeper_parachute_drift", parachute_drift_frames, 4, anchor_point=[48, 84], loop=True, mirror_safe=True, facing="right", interaction="parachute-drift", mirrors_for="left", start_pose="parachute-open", end_pose="parachute-open")
save("keeper_parachute_landing", parachute_landing_frames, 6, anchor_point=[48, 84], loop=False, mirror_safe=True, facing="right", interaction="parachute-landing", mirrors_for="left", start_pose="parachute-open", end_pose="standing-side-right")
save("keeper_platform_dive", platform_dive_frames, 10, loop=False, mirror_safe=True, facing="right", interaction="platform-dive", mirrors_for="left")
save("keeper_dig", dig_frames, 8, hand_use_point=[27, 38], mirror_safe=True, facing="right", interaction="dig-ground", mirrors_for="left")
save("keeper_feed_animals", feed_animals_frames, 8, loop=False, hand_use_point=[27, 34], mirror_safe=True, facing="right", interaction="feed-bowl", mirrors_for="left")
save("keeper_sow_seeds", sow_seeds_frames, 8, hand_use_point=[27, 34], mirror_safe=True, facing="right", interaction="sow-ground", mirrors_for="left")
save("keeper_pick_vegetable", pick_vegetable_frames, 8, loop=False, hand_use_point=[26, 36], mirror_safe=True, facing="right", interaction="harvest-low", mirrors_for="left")
save("keeper_pick_fruit", pick_fruit_frames, 8, loop=False, hand_use_point=[25, 14], mirror_safe=True, facing="right", interaction="harvest-high", mirrors_for="left")
save("keeper_carry_shopping", carry_shopping_frames, 10, mirror_safe=True, facing="right", interaction="carry-shopping", mirrors_for="left")
save("keeper_row_boat", row_boat_frames, 8, seat_point=[20, 29], hand_use_point=[30, 20], mirror_safe=True, facing="right", interaction="row-boat", mirrors_for="left")
save("keeper_drive_speedboat", drive_speedboat_frames, 4, seat_point=[16, 29], hand_use_point=[25, 20], mirror_safe=True, facing="right", interaction="drive-speedboat", mirrors_for="left")
save("keeper_operate_outboard", operate_outboard_frames, 8, hand_use_point=[4, 21], mirror_safe=True, facing="rear-right", interaction="operate-outboard", mirrors_for="rear-left")
save("keeper_watch_tv", watch_tv_frames, 6, seat_point=[16, 29], look_target_point=[40, 14], mirror_safe=True, facing="rear-right", interaction="watch-tv", mirrors_for="rear-left")
save("keeper_weld", weld_frames, 8, hand_use_point=[27, 22], mirror_safe=True, facing="right", interaction="weld-workpiece", mirrors_for="left")
save("keeper_saw_wood", saw_wood_frames, 8, anchor_point=[32, 40], hand_use_point=[51, 23], mirror_safe=True, facing="right", interaction="saw-workpiece", mirrors_for="left")
save("keeper_wave_camera", wave_camera_frames, 8, loop=False, facing="front", interaction="emote-wave")
save("keeper_yawn", yawn_frames, 8, loop=False, facing="front-right", interaction="emote-yawn")
save("keeper_pyjamas_walk", pyjamas_walk_frames, 10, outfit="light-blue-pyjamas", mirror_safe=True, facing="right", interaction="walk-pyjamas", mirrors_for="left")
save("keeper_pyjamas_turn_back", pyjamas_turn_back_frames, 8, outfit="light-blue-pyjamas", loop=False, reverse_for="pyjamas_turn_front", facing="front-to-back", interaction="turn-pyjamas")
save("keeper_door_open_side_pyjamas", pyjamas_door_side_frames, 8, outfit="light-blue-pyjamas", loop=False, hand_use_point=[25, 20], reverse_for="door_close_side_pyjamas", mirror_safe=True, facing="right", interaction="open-door", mirrors_for="left")
save("keeper_get_into_bed", get_into_bed_frames, 8, outfit="light-blue-pyjamas", loop=False, bed_surface_point=[24, 31], pillow_point=[38, 22], reverse_for="get_out_of_bed", mirror_safe=True, facing="right", interaction="enter-bed", mirrors_for="left")
save("keeper_pyjamas_snore", pyjamas_snore_frames, 4, outfit="light-blue-pyjamas", bed_surface_point=[24, 31], pillow_point=[38, 22], mirror_safe=True, facing="right", interaction="sleep-snore", mirrors_for="left")
save("keeper_swim_costume_horizontal", swim_costume_horizontal_frames, 8, anchor_point=[40, 24], movement_vector=[1, 0], outfit="striped-swimming-costume", mirror_safe=True, facing="right", interaction="swim", mirrors_for="left")
save("keeper_swim_costume_up", swim_costume_up_frames, 8, anchor_point=[24, 24], movement_vector=[0, -1], outfit="striped-swimming-costume", facing="up", interaction="swim")
save("keeper_swim_costume_down", swim_costume_down_frames, 8, anchor_point=[24, 24], movement_vector=[0, 1], outfit="striped-swimming-costume", facing="down", interaction="swim")
save("keeper_scuba_swim_horizontal", scuba_horizontal_frames, 8, anchor_point=[40, 24], movement_vector=[1, 0], outfit="scuba", mirror_safe=True, facing="right", interaction="scuba-swim", mirrors_for="left")
save("keeper_scuba_swim_up", scuba_up_frames, 8, anchor_point=[24, 24], movement_vector=[0, -1], outfit="scuba", facing="up", interaction="scuba-swim")
save("keeper_scuba_swim_down", scuba_down_frames, 8, anchor_point=[24, 24], movement_vector=[0, 1], outfit="scuba", facing="down", interaction="scuba-swim")
save("keeper_scuba_walk_side", scuba_walk_side_frames, 8, anchor_point=[24, 56], movement_vector=[1, 0], outfit="scuba", mirror_safe=True, facing="right", interaction="scuba-jetty-walk", mirrors_for="left", start_pose="scuba-standing-side-right", end_pose="scuba-standing-side-right")
save("keeper_scuba_jetty_dive", scuba_jetty_dive_frames, 8, anchor_point=[40, 72], movement_vector=[1, 0], outfit="scuba", loop=False, mirror_safe=True, facing="right-to-prone", interaction="scuba-water-entry", mirrors_for="left", start_pose="scuba-standing-side-right", end_pose="scuba-swim-right")
save("keeper_party_idle", party_idle_frames, 6, anchor_point=[16, 48], outfit="party-hat", facing="front", interaction="party-idle")
save("keeper_party_walk", party_walk_frames, 10, anchor_point=[16, 48], outfit="party-hat", mirror_safe=True, facing="right", interaction="party-walk", mirrors_for="left")
save("keeper_party_turn_back", party_turn_back_frames, 8, anchor_point=[16, 48], outfit="party-hat", loop=False, reverse_for="party_turn_front", facing="front-to-back", interaction="party-turn")
save("keeper_party_hat_put_on_back", party_hat_put_on_back, 8, anchor_point=[16, 48], hand_use_point=[16, 13], outfit="party-hat-transition", loop=False, reverse_for="party-hat-remove-back", facing="back", interaction="put-on-party-hat")
save("keeper_party_eat_cake", party_cake_eat, 8, anchor_point=[16, 48], seat_point=[16, 37], hand_use_point=[27, 25], outfit="party-hat", facing="right", interaction="eat-cake", mirror_safe=True, mirrors_for="left")
save("keeper_party_dance", party_dance_frames, 10, anchor_point=[16, 48], outfit="party-hat", facing="front", interaction="party-dance")
save("keeper_souwester_walk_side", souwester_side_frames, 10, anchor_point=[16, 48], movement_vector=[1, 0], outfit="souwester", mirror_safe=True, facing="right", interaction="souwester-walk", mirrors_for="left")
save("keeper_souwester_walk_back", souwester_back_frames, 10, anchor_point=[16, 48], movement_vector=[0, -1], outfit="souwester", facing="back", interaction="souwester-walk-away")
save("keeper_souwester_walk_front", souwester_front_frames, 10, anchor_point=[16, 48], movement_vector=[0, 1], outfit="souwester", facing="front", interaction="souwester-walk-toward")
save("keeper_dance", dance_frames, 10, mirror_safe=True, facing="front", interaction="dance")
save("keeper_play_guitar", play_guitar_frames, 10, hand_use_point=[34, 20], prop_variant="acoustic", upgrade_tier=1, mirror_safe=True, facing="front-right", interaction="play-guitar", mirrors_for="front-left")
save("keeper_artist_smock_walk", artist_smock_walk_frames, 8, outfit="artist-smock", movement_vector=[1, 0], mirror_safe=True, facing="right", interaction="artist-smock-walk", mirrors_for="left")
save("keeper_artist_smock_turn_back", artist_smock_turn_back_frames, 6, outfit="artist-smock", loop=False, reverse_for="artist_smock_turn_side", facing="right-to-back", interaction="turn-back")
save("keeper_artist_smock_turn_front", artist_smock_turn_front_frames, 6, outfit="artist-smock", loop=False, reverse_for="artist_smock_turn_side_from_front", facing="right-to-front", interaction="turn-front")
save("keeper_artist_smock_sit_front", artist_smock_sit_front_frames, 6, outfit="artist-smock", loop=False, seat_point=[16, 29], reverse_for="artist_smock_stand_front", facing="front", interaction="sit-front")
save("keeper_play_guitar_gretsch", play_guitar_gretsch_frames, 8, hand_use_point=[34, 20], prop_variant="black-gretsch", upgrade_tier=2, mirror_safe=True, facing="front-right", interaction="play-guitar", mirrors_for="front-left")
save("keeper_play_guitar_flying_v_1967", play_guitar_flying_v_frames, 8, hand_use_point=[42, 20], prop_variant="red-flying-v-1967", upgrade_tier=3, mirror_safe=True, facing="front-right", interaction="play-guitar", mirrors_for="front-left")
save("keeper_guitar_pickup_acoustic", guitar_pickup_acoustic_frames, 12, anchor_point=[32, 56], loop=False, hand_use_point=[45, 25], prop_handoff_frame=6, prop_variant="acoustic", upgrade_tier=1, start_pose="standing-side-right", end_pose="play-guitar-acoustic", facing="side-to-back-to-front-right", interaction="pick-up-guitar")
save("keeper_guitar_pickup_gretsch", guitar_pickup_gretsch_frames, 12, anchor_point=[32, 56], loop=False, hand_use_point=[45, 25], prop_handoff_frame=6, prop_variant="black-gretsch", upgrade_tier=2, start_pose="standing-side-right", end_pose="play-guitar-gretsch", facing="side-to-back-to-front-right", interaction="pick-up-guitar")
save("keeper_guitar_pickup_flying_v_1967", guitar_pickup_flying_v_frames, 12, anchor_point=[32, 56], loop=False, hand_use_point=[45, 25], prop_handoff_frame=6, prop_variant="red-flying-v-1967", upgrade_tier=3, start_pose="standing-side-right", end_pose="play-guitar-flying-v-1967", facing="side-to-back-to-front-right", interaction="pick-up-guitar")
save("keeper_play_drums_front", play_drums_front_frames, 10, anchor_point=[16, 48], seat_point=[16, 37], hand_use_point=[16, 27], facing="front", interaction="play-drums")
save("keeper_play_drums_back", play_drums_back_frames, 10, anchor_point=[16, 48], seat_point=[16, 37], hand_use_point=[16, 27], facing="back", interaction="play-drums")
save("keeper_watch_movie", watch_movie_frames, 6, seat_point=[24, 29], hand_use_point=[34, 19], look_target_point=[56, 14], mirror_safe=True, facing="rear-right", interaction="watch-movie-popcorn", mirrors_for="rear-left")
save("keeper_clear_snow", clear_snow_frames, 8, hand_use_point=[43, 37], outfit="winter-coat", mirror_safe=True, facing="right", interaction="clear-snow", mirrors_for="left")
save("keeper_lawn_mower_push", lawn_mower_push_frames, 8, hand_use_point=[23, 22], movement_vector=[1, 0], prop_variant="manual-reel-mower", mirror_safe=True, facing="right", interaction="push-lawn-mower", mirrors_for="left")
save("keeper_sweep_broom", sweep_broom_frames, 8, hand_use_point=[27, 24], movement_vector=[1, 0], prop_variant="traditional-broom", upgrade_tier=1, mirror_safe=True, facing="right", interaction="clean-floor", mirrors_for="left")
save("keeper_hoover_basic", hoover_basic_frames, 8, hand_use_point=[27, 23], movement_vector=[1, 0], prop_variant="basic-upright-hoover", upgrade_tier=2, mirror_safe=True, facing="right", interaction="clean-floor", mirrors_for="left")
save("keeper_hoover_super", hoover_super_frames, 8, hand_use_point=[27, 23], movement_vector=[1, 0], prop_variant="eccentric-super-hoover", upgrade_tier=3, mirror_safe=True, facing="right", interaction="clean-floor", mirrors_for="left")
save("keeper_crouch_work_back", crouch_work_back_frames, 8, hand_use_point=[16, 38], facing="back", interaction="ground-work")
save("keeper_cake_from_oven_back", cake_from_oven_back_frames, 8, loop=False, hand_use_point=[24, 30], facing="back", interaction="retrieve-cake-from-oven")
save("keeper_cake_turn_right", cake_turn_right_frames, 8, loop=False, hand_use_point=[34, 20], mirror_safe=True, facing="back-to-right", interaction="turn-carry-cake", mirrors_for="back-to-left")
save("keeper_carry_cake", carry_cake_frames, 10, hand_use_point=[34, 20], mirror_safe=True, facing="right", interaction="walk-carry-cake", mirrors_for="left")
save("keeper_carry_meal", carry_meal_frames, 10, hand_use_point=[34, 20], mirror_safe=True, facing="right", interaction="walk-carry-meal", mirrors_for="left")
save("keeper_place_cake", place_cake_frames, 8, loop=False, hand_use_point=[39, 21], mirror_safe=True, facing="right", interaction="place-cake-on-table", mirrors_for="left")

# A transparent source contact sheet makes alignment mistakes easy to spot.
contact = Image.new("RGBA", (W * 4, H * 2), (244, 236, 214, 255))
for i, frame in enumerate((compose("front", "happy"), walk_frames[2], turn_frames[-1], work_frames[1], sit_side_frames[-1], sit_front_frames[-1], piano_frames[0], eat_seated_frames[2])):
    contact.alpha_composite(frame, ((i % 4) * W, (i // 4) * H))
contact.save(Path(__file__).with_name("keeper-contact-sheet.png"), optimize=True)

save_preview("keeper-walk", walk_frames, 100)
save_preview("keeper-turn-back", turn_frames, 120, ping_pong=True)
save_preview("keeper-turn-front", turn_front_frames, 120, ping_pong=True)
save_preview("keeper-work-back", work_frames, 120)
save_preview("keeper-sit-side", sit_side_frames, 120, ping_pong=True)
save_preview("keeper-nap-seated", nap_seated_frames, 250)
save_preview("keeper-sit-front", sit_front_frames, 120, ping_pong=True)
save_preview("keeper-sit-back", sit_back_frames, 120, ping_pong=True)
save_preview("keeper-sitting-turn-back-to-rear", sitting_turn_back_to_rear_frames, 120, ping_pong=True)
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
save_preview("keeper-walk-into-lift", walk_into_lift_frames, 120)
save_preview("keeper-parachute-jump", parachute_jump_frames, 100)
save_preview("keeper-parachute-drift", parachute_drift_frames, 250)
save_preview("keeper-parachute-landing", parachute_landing_frames, 167)
save_preview("keeper-platform-dive", platform_dive_frames, 100)
save_preview("keeper-dig", dig_frames, 120)
save_preview("keeper-feed-animals", feed_animals_frames, 120)
save_preview("keeper-sow-seeds", sow_seeds_frames, 120)
save_preview("keeper-pick-vegetable", pick_vegetable_frames, 120)
save_preview("keeper-pick-fruit", pick_fruit_frames, 120)
save_preview("keeper-carry-shopping", carry_shopping_frames, 100)
save_preview("keeper-row-boat", row_boat_frames, 120)
save_preview("keeper-drive-speedboat", drive_speedboat_frames, 250)
save_preview("keeper-operate-outboard", operate_outboard_frames, 120)
save_preview("keeper-watch-tv-right", watch_tv_frames, 160)
save_preview("keeper-watch-tv-left", [ImageOps.mirror(frame) for frame in watch_tv_frames], 160)
save_preview("keeper-weld", weld_frames, 120)
save_preview("keeper-saw-wood", saw_wood_frames, 120)
save_preview("keeper-wave-camera", wave_camera_frames, 120)
save_preview("keeper-yawn", yawn_frames, 120)
save_preview("keeper-pyjamas-walk", pyjamas_walk_frames, 100)
save_preview("keeper-pyjamas-turn-back", pyjamas_turn_back_frames, 120, ping_pong=True)
save_preview("keeper-door-open-side-pyjamas", pyjamas_door_side_frames, 120, ping_pong=True)
save_preview("keeper-get-into-bed", get_into_bed_frames, 120)
save_preview("keeper-pyjamas-snore", pyjamas_snore_frames, 250)
save_preview("keeper-swim-costume-horizontal", swim_costume_horizontal_frames, 120)
save_preview("keeper-swim-costume-up", swim_costume_up_frames, 120)
save_preview("keeper-swim-costume-down", swim_costume_down_frames, 120)
save_preview("keeper-scuba-swim-horizontal", scuba_horizontal_frames, 120)
save_preview("keeper-scuba-swim-up", scuba_up_frames, 120)
save_preview("keeper-scuba-swim-down", scuba_down_frames, 120)
save_preview("keeper-scuba-walk-side", scuba_walk_side_frames, 120)
save_preview("keeper-scuba-jetty-dive", scuba_jetty_dive_frames, 120)
save_preview("keeper-party-idle", party_idle_frames, 160)
save_preview("keeper-party-walk", party_walk_frames, 100)
save_preview("keeper-party-turn-back", party_turn_back_frames, 120, ping_pong=True)
save_preview("keeper-party-hat-put-on-back", party_hat_put_on_back, 120)
save_preview("keeper-party-eat-cake", party_cake_eat, 120)
save_preview("keeper-party-dance", party_dance_frames, 100)
save_preview("keeper-souwester-walk-side", souwester_side_frames, 100)
save_preview("keeper-souwester-walk-back", souwester_back_frames, 100)
save_preview("keeper-souwester-walk-front", souwester_front_frames, 100)
save_preview("keeper-dance", dance_frames, 100)
save_preview("keeper-play-guitar", play_guitar_frames, 100)
save_preview("keeper-artist-smock-walk", artist_smock_walk_frames, 100)
save_preview("keeper-artist-smock-turn-back", artist_smock_turn_back_frames, 120, ping_pong=True)
save_preview("keeper-artist-smock-turn-front", artist_smock_turn_front_frames, 120, ping_pong=True)
save_preview("keeper-artist-smock-sit-front", artist_smock_sit_front_frames, 120, ping_pong=True)
save_preview("keeper-play-guitar-gretsch", play_guitar_gretsch_frames, 120)
save_preview("keeper-play-guitar-flying-v-1967", play_guitar_flying_v_frames, 120)
save_preview("keeper-guitar-pickup-acoustic", guitar_pickup_acoustic_frames, 120)
save_preview("keeper-guitar-pickup-gretsch", guitar_pickup_gretsch_frames, 120)
save_preview("keeper-guitar-pickup-flying-v-1967", guitar_pickup_flying_v_frames, 120)
save_preview("keeper-play-drums-front", play_drums_front_frames, 100)
save_preview("keeper-play-drums-back", play_drums_back_frames, 100)
save_preview("keeper-watch-movie-right", watch_movie_frames, 160)
save_preview("keeper-watch-movie-left", [ImageOps.mirror(frame) for frame in watch_movie_frames], 160)
save_preview("keeper-clear-snow-right", clear_snow_frames, 120)
save_preview("keeper-clear-snow-left", [ImageOps.mirror(frame) for frame in clear_snow_frames], 120)
save_preview("keeper-lawn-mower-push-right", lawn_mower_push_frames, 120)
save_preview("keeper-lawn-mower-push-left", [ImageOps.mirror(frame) for frame in lawn_mower_push_frames], 120)
save_preview("keeper-sweep-broom-right", sweep_broom_frames, 120)
save_preview("keeper-sweep-broom-left", [ImageOps.mirror(frame) for frame in sweep_broom_frames], 120)
save_preview("keeper-hoover-basic-right", hoover_basic_frames, 120)
save_preview("keeper-hoover-basic-left", [ImageOps.mirror(frame) for frame in hoover_basic_frames], 120)
save_preview("keeper-hoover-super-right", hoover_super_frames, 120)
save_preview("keeper-hoover-super-left", [ImageOps.mirror(frame) for frame in hoover_super_frames], 120)
save_preview("keeper-crouch-work-back", crouch_work_back_frames, 120)
save_preview("keeper-cake-from-oven-back", cake_from_oven_back_frames, 120)
save_preview("keeper-cake-turn-right", cake_turn_right_frames, 120)
save_preview("keeper-cake-turn-left", [ImageOps.mirror(frame) for frame in cake_turn_right_frames], 120)
save_preview("keeper-carry-cake", carry_cake_frames, 100)
save_preview("keeper-carry-meal", carry_meal_frames, 100)
save_preview("keeper-place-cake", place_cake_frames, 120)

# October interaction expansion.  The tuple is export name, generated source,
# logical width, logical height, and runtime placement metadata.  Large room
# objects stay separate; hand/seat/look points are the attachment contract.
ADDITIONAL_CLIPS = [
    ("keeper_sad", "keeper-sad-generated-source.png", 32, 40, dict(facing="front", interaction="emote-sad")),
    ("keeper_hungry", "keeper-hungry-generated-source.png", 32, 40, dict(facing="front", interaction="emote-hungry")),
    ("keeper_bored", "keeper-bored-generated-source.png", 32, 40, dict(facing="front", interaction="emote-bored")),
    ("keeper_cross", "keeper-cross-generated-source.png", 32, 40, dict(facing="front", interaction="emote-cross")),
    ("keeper_vomit_loo_back", "keeper-vomit-loo-back-generated-source.png", 40, 40, dict(hand_use_point=[31, 27], bowl_point=[32, 35], facing="back", interaction="vomit-into-toilet", loop=False)),
    ("keeper_bathrobe_walk", "keeper-bathrobe-walk-generated-source.png", 32, 40, dict(outfit="cream-bathrobe", movement_vector=[1, 0], facing="right", interaction="bathrobe-walk", mirror_safe=True, mirrors_for="left")),
    ("keeper_shower_door_open_bathrobe", "keeper-shower-door-open-bathrobe-generated-source.png", 40, 40, dict(hand_use_point=[35, 18], outfit="cream-bathrobe", facing="rear-right", interaction="open-shower-door", loop=False, mirror_safe=True, mirrors_for="rear-left")),
    ("keeper_shower_enter_bathrobe", "keeper-shower-enter-bathrobe-generated-source.png", 40, 40, dict(outfit="cream-bathrobe", movement_vector=[0, -1], facing="back", interaction="enter-shower-cubicle", loop=False, mirror_safe=True, mirrors_for="rear-left")),
    ("keeper_fish_feed_up", "keeper-fish-feed-up-generated-source.png", 32, 48, dict(hand_use_point=[26, 7], facing="right", interaction="feed-fish-high", mirror_safe=True, mirrors_for="left")),
    ("keeper_aquarium_brush", "keeper-aquarium-brush-generated-source.png", 40, 40, dict(hand_use_point=[34, 17], facing="right", interaction="clean-aquarium", mirror_safe=True, mirrors_for="left")),
    ("keeper_aquarium_net", "keeper-aquarium-net-generated-source.png", 40, 40, dict(hand_use_point=[34, 21], facing="right", interaction="net-aquarium-fish", mirror_safe=True, mirrors_for="left")),
    ("keeper_hammer_back", "keeper-hammer-back-generated-source.png", 32, 40, dict(hand_use_point=[16, 22], facing="back", interaction="hammer-workbench")),
    ("keeper_hammer_side", "keeper-hammer-side-generated-source.png", 40, 40, dict(hand_use_point=[32, 23], facing="right", interaction="hammer-workbench", mirror_safe=True, mirrors_for="left")),
    ("keeper_read_side", "keeper-read-side-generated-source.png", 32, 40, dict(seat_point=[16, 29], facing="right", interaction="read-book", mirror_safe=True, mirrors_for="left")),
    ("keeper_read_front", "keeper-read-front-generated-source.png", 32, 40, dict(seat_point=[16, 29], facing="front", interaction="read-book")),
    ("keeper_write_side", "keeper-write-side-generated-source.png", 40, 40, dict(seat_point=[20, 29], hand_use_point=[34, 21], facing="right", interaction="write", mirror_safe=True, mirrors_for="left")),
    ("keeper_write_back", "keeper-write-back-generated-source.png", 32, 40, dict(seat_point=[16, 29], hand_use_point=[16, 21], facing="back", interaction="write")),
    ("keeper_lean_table_back", "keeper-lean-table-generated-source.png", 32, 40, dict(hand_use_point=[16, 27], facing="back", interaction="inspect-table")),
    ("keeper_telescope", "keeper-telescope-generated-source.png", 48, 40, dict(hand_use_point=[38, 17], look_target_point=[48, 12], facing="right", interaction="use-telescope", mirror_safe=True, mirrors_for="left")),
    ("keeper_put_record", "keeper-put-record-generated-source.png", 64, 40, dict(anchor_point=[32, 40], hand_use_point=[46, 25], facing="right", interaction="put-record", mirror_safe=True, mirrors_for="left")),
    ("keeper_paint_side", "keeper-paint-side-generated-source.png", 40, 40, dict(hand_use_point=[34, 17], outfit="artist-smock", facing="right", interaction="paint", mirror_safe=True, mirrors_for="left")),
    ("keeper_paint_back", "keeper-paint-back-generated-source.png", 32, 40, dict(hand_use_point=[16, 17], outfit="artist-smock", facing="back", interaction="paint")),
    ("keeper_pottery_front", "keeper-pottery-front-generated-source.png", 40, 40, dict(seat_point=[20, 29], hand_use_point=[20, 23], outfit="artist-smock", facing="front", interaction="pottery-wheel")),
    ("keeper_search_boxes", "keeper-search-boxes-generated-source.png", 32, 40, dict(hand_use_point=[16, 38], facing="back", interaction="search-boxes")),
    ("keeper_meal_from_oven_back", "keeper-meal-oven-back-generated-source.png", 48, 40, dict(hand_use_point=[24, 30], facing="back", interaction="retrieve-meal-from-oven", loop=False)),
    ("keeper_meal_place_side", "keeper-meal-place-side-generated-source.png", 48, 40, dict(hand_use_point=[39, 21], facing="right", interaction="place-meal-on-table", loop=False, mirror_safe=True, mirrors_for="left")),
    ("keeper_count_money", "keeper-count-money-generated-source.png", 40, 40, dict(seat_point=[20, 29], hand_use_point=[20, 21], facing="front", interaction="count-money")),
    ("keeper_snooker", "keeper-snooker-generated-source.png", 64, 40, dict(anchor_point=[32, 40], hand_use_point=[55, 25], facing="right", interaction="play-snooker", mirror_safe=True, mirrors_for="left")),
    ("keeper_table_tennis", "keeper-table-tennis-generated-source.png", 40, 40, dict(hand_use_point=[34, 20], facing="right", interaction="play-table-tennis", mirror_safe=True, mirrors_for="left")),
    ("keeper_darts", "keeper-darts-generated-source.png", 56, 40, dict(anchor_point=[28, 40], hand_use_point=[46, 15], look_target_point=[56, 12], facing="right", interaction="play-darts", mirror_safe=True, mirrors_for="left")),
    ("keeper_trampoline_front", "keeper-trampoline-front-generated-source.png", 32, 48, dict(outfit="old-school-workout-kit", facing="front", interaction="bounce-trampoline")),
    ("keeper_lift_weights_back", "keeper-weights-back-generated-source.png", 48, 56, dict(hand_use_point=[24, 5], outfit="old-school-workout-kit", facing="back", interaction="lift-weights")),
    ("keeper_pressups_side", "keeper-pressups-side-generated-source.png", 64, 40, dict(outfit="old-school-workout-kit", facing="right", interaction="press-ups", mirror_safe=True, mirrors_for="left")),
    ("keeper_anti_gravity", "keeper-anti-gravity-generated-source.png", 48, 48, dict(anchor_point=[24, 24], facing="right-prone", interaction="anti-gravity-float")),
    ("keeper_machete_side", "keeper-machete-side-generated-source.png", 80, 40, dict(anchor_point=[40, 40], hand_use_point=[66, 28], facing="right", interaction="chop-plants", mirror_safe=True, mirrors_for="left")),
    ("keeper_drink_pint", "keeper-drink-pint-generated-source.png", 40, 40, dict(seat_point=[20, 29], hand_use_point=[25, 16], facing="front-right", interaction="drink-pint", mirror_safe=True, mirrors_for="front-left")),
    ("keeper_ride_bike_front", "keeper-bike-front-generated-source.png", 48, 48, dict(seat_point=[24, 35], hand_use_point=[24, 27], pedal_point=[24, 42], outfit="old-school-workout-kit", facing="front", interaction="use-stationary-exercise-bike")),
    ("keeper_lift_button_front", "keeper-lift-button-front-generated-source.png", 32, 40, dict(hand_use_point=[27, 17], facing="front", interaction="press-lift-button", mirror_safe=True, mirrors_for="front-left-hand")),
    ("keeper_spiral_stairs", "keeper-spiral-stairs-generated-source.png", 40, 48, dict(facing="three-quarter", interaction="climb-spiral-stairs")),
    ("keeper_spiral_stairs_up", "keeper-spiral-stairs-generated-source.png", 40, 48, dict(movement_vector=[0, -1], facing="rotating-right-to-rear", interaction="spiral-stairs-up")),
    ("keeper_spiral_stairs_down", "keeper-spiral-stairs-down-generated-source.png", 40, 48, dict(movement_vector=[0, 1], facing="rotating-rear-to-front-right", interaction="spiral-stairs-down")),
    ("keeper_hot_drink_pour", "keeper-hot-drink-pour-generated-source.png", 48, 40, dict(hand_use_point=[40, 28], facing="right", interaction="pour-hot-drink", loop=False, mirror_safe=True, mirrors_for="left")),
    ("keeper_hot_drink_stir", "keeper-hot-drink-stir-generated-source.png", 48, 40, dict(hand_use_point=[40, 28], facing="right", interaction="stir-hot-drink", loop=False, mirror_safe=True, mirrors_for="left")),
    ("keeper_hot_drink_pickup", "keeper-hot-drink-pickup-generated-source.png", 48, 40, dict(hand_use_point=[40, 28], facing="right", interaction="pick-up-hot-drink", loop=False, mirror_safe=True, mirrors_for="left")),
    ("keeper_hot_drink_drink", "keeper-hot-drink-drink-generated-source.png", 48, 40, dict(hand_use_point=[34, 17], facing="right", interaction="drink-hot-drink", mirror_safe=True, mirrors_for="left")),
    ("keeper_hot_drink_put_down", "keeper-hot-drink-put-down-generated-source.png", 48, 40, dict(hand_use_point=[40, 28], facing="right", interaction="put-down-hot-drink", loop=False, mirror_safe=True, mirrors_for="left")),
    ("keeper_boat_enter", "keeper-boat-enter-generated-source.png", 48, 48, dict(seat_point=[36, 35], hand_use_point=[39, 23], facing="right", interaction="climb-into-boat", loop=False, mirror_safe=True, mirrors_for="left")),
    ("keeper_boat_exit", "keeper-boat-exit-generated-source.png", 48, 48, dict(seat_point=[36, 35], hand_use_point=[39, 23], facing="front-right", interaction="climb-out-of-boat", loop=False, mirror_safe=True, mirrors_for="left")),
    ("keeper_slide_side", "keeper-slide-side-generated-source.png", 48, 40, dict(facing="right", interaction="ride-slide", mirror_safe=True, mirrors_for="left")),
    ("keeper_bbq_back", "keeper-bbq-back-generated-source.png", 32, 40, dict(hand_use_point=[16, 22], facing="back", interaction="use-bbq")),
    ("keeper_hot_tub", "keeper-hot-tub-generated-source.png", 40, 40, dict(seat_point=[20, 29], facing="front", interaction="soak-hot-tub", outfit="privacy-foam")),
    ("keeper_bowling", "keeper-bowling-generated-source.png", 48, 40, dict(hand_use_point=[39, 35], facing="right", interaction="ten-pin-bowling", mirror_safe=True, mirrors_for="left")),
    ("keeper_video_game", "keeper-video-game-generated-source.png", 48, 40, dict(seat_point=[24, 29], hand_use_point=[24, 21], look_target_point=[56, 14], facing="rear-right", interaction="play-video-game", mirror_safe=True, mirrors_for="rear-left")),
    ("keeper_water_plants_side", "keeper-water-side-generated-source.png", 48, 40, dict(hand_use_point=[39, 31], facing="right", interaction="water-plants", mirror_safe=True, mirrors_for="left")),
    ("keeper_water_plants_back", "keeper-water-back-generated-source.png", 40, 40, dict(hand_use_point=[20, 31], facing="back", interaction="water-plants")),
    ("keeper_water_plants_front", "keeper-water-front-generated-source.png", 40, 40, dict(hand_use_point=[20, 31], facing="front", interaction="water-plants")),
    ("keeper_fish_standing", "keeper-fish-stand-generated-source.png", 96, 88, dict(anchor_point=[48, 56], hand_use_point=[80, 32], facing="right", interaction="fish-and-reel", mirror_safe=True, mirrors_for="left")),
    ("keeper_fish_seated", "keeper-fish-sit-generated-source.png", 96, 88, dict(anchor_point=[48, 56], seat_point=[48, 45], hand_use_point=[78, 29], facing="right", interaction="fish-and-reel", mirror_safe=True, mirrors_for="left")),
    ("keeper_collect_eggs_back", "keeper-collect-eggs-generated-source.png", 32, 40, dict(hand_use_point=[16, 38], facing="back", interaction="collect-eggs")),
    ("keeper_bath_enter", "keeper-bath-enter-generated-source.png", 40, 40, dict(facing="right", interaction="enter-bath", outfit="towel-privacy", loop=False, reverse_for="bath-exit", mirror_safe=True, mirrors_for="left")),
    ("keeper_bath_wash", "keeper-bath-wash-generated-source.png", 40, 40, dict(seat_point=[20, 29], facing="front", interaction="wash-in-bath", outfit="mosaic-privacy")),
    ("keeper_bath_exit", "keeper-bath-exit-generated-source.png", 40, 40, dict(facing="right", interaction="exit-bath", outfit="towel-privacy", loop=False, mirror_safe=True, mirrors_for="left")),
    ("keeper_shower_enter", "keeper-shower-enter-generated-source.png", 40, 40, dict(facing="rear-right", interaction="enter-shower", outfit="towel-privacy", loop=False, mirror_safe=True, mirrors_for="rear-left")),
    ("keeper_shower_wash", "keeper-shower-wash-generated-source.png", 40, 40, dict(facing="back", interaction="wash-in-shower", outfit="mosaic-privacy")),
    ("keeper_shower_exit", "keeper-shower-exit-generated-source.png", 40, 40, dict(facing="rear-right", interaction="exit-shower", outfit="towel-privacy", loop=False, mirror_safe=True, mirrors_for="rear-left")),
]

for outfit in ("knight", "spaceman", "pirate", "tarzan", "halloween", "mechanic"):
    for view, facing, vector in (("side", "right", [1, 0]), ("back", "back", [0, -1]), ("front", "front", [0, 1])):
        metadata = dict(outfit=outfit, facing=facing, movement_vector=vector, interaction=f"{outfit}-walk")
        if view == "side": metadata.update(mirror_safe=True, mirrors_for="left")
        ADDITIONAL_CLIPS.append((f"keeper_{outfit}_walk_{view}", f"keeper-{outfit}-{view}-generated-source.png", 32, 48, metadata))

ADDITIONAL_CLIPS.append(("keeper_mechanic_fix", "keeper-mechanic-fix-generated-source.png", 40, 40, dict(outfit="mechanic", hand_use_point=[34, 22], facing="right", interaction="fix-vehicle", mirror_safe=True, mirrors_for="left")))

for clip_name, source_name, logical_width, logical_height, metadata in ADDITIONAL_CLIPS:
    frame_count = {
        "keeper_hot_drink_pour": 10,
        "keeper_fish_standing": 16,
        "keeper_fish_seated": 16,
    }.get(clip_name, 8)
    # These values are anatomy scale, never "fit to available canvas".  Most
    # seated generated sheets started ten percent larger than the canonical
    # sit transition.  The bath was redrawn against canonical references; the
    # water-hidden hot-tub figure still needs an explicit visible-head scale so
    # its missing lower body cannot enlarge the keeper.
    costume_family_scale = next((scale for prefix, scale in {
        "keeper_knight_walk_": 0.92,
        "keeper_spaceman_walk_": 0.84,
        "keeper_pirate_walk_": 0.86,
        # These two bare-headed families can be compared directly with the
        # approved original walk.  The earlier multipliers produced only a
        # 33-35 px skull-to-sole silhouette versus the original's 38 px.
        "keeper_tarzan_walk_": 0.84,
        "keeper_halloween_walk_": 0.84,
        "keeper_mechanic_walk_": 0.83,
    }.items() if clip_name.startswith(prefix)), None)
    anatomy_scale = {
        "keeper_bath_wash": 0.90,
        "keeper_hot_tub": 0.65,
        "keeper_ride_bike_front": 0.965,
    }.get(clip_name, costume_family_scale if costume_family_scale is not None else (0.90 if "seat_point" in metadata else 1.0))
    if clip_name in {"keeper_search_boxes", "keeper_collect_eggs_back"}:
        # Both actions are object-specific uses of the canonical low rear work
        # loop. Boxes, basket and eggs belong to world objects, not the actor;
        # reusing these frames prevents the older crouch sheets from making the
        # keeper wider merely because the pose is shorter.
        frames = [frame.copy() for frame in crouch_work_back_frames]
    elif clip_name == "keeper_boat_enter":
        # The 48 px canvas provides room for the climb; it must not enlarge the
        # keeper beyond the canonical 38 px standing height.
        frames = generated_frames(source_name, 8, logical_width=logical_width, logical_height=logical_height, scale_reference_index=0)
    elif clip_name == "keeper_boat_exit":
        frames = generated_frames(source_name, 8, logical_width=logical_width, logical_height=logical_height, scale_reference_index=7)
    elif clip_name == "keeper_shower_door_open_bathrobe":
        frames = generated_frames(source_name, 8, logical_width=logical_width, logical_height=logical_height, preserve_equal_cells=True)
        turn_in = generated_frames("keeper-shower-enter-bathrobe-generated-source.png", 8, logical_width=logical_width, logical_height=logical_height, preserve_equal_cells=True)
        frames = [
            remove_small_alpha_components(frame, min_pixels=200)
            for frame in [turn_in[0].copy(), turn_in[1].copy()] + frames
        ]
    elif clip_name in {"keeper_fish_standing", "keeper_fish_seated"}:
        # The corrective renders intentionally provide 18 isolated source
        # poses. Drop two near-duplicate waiting holds while retaining four
        # patient frames, six progressive pull/reel frames and the complete
        # below-feet fish rise in a 16-frame production strip.
        source_frames = generated_frames(
            source_name,
            18,
            logical_width=logical_width,
            logical_height=logical_height,
            group_equal_components=True,
        )
        frames = [frame for index, frame in enumerate(source_frames) if index not in {1, 3}]
        if clip_name == "keeper_fish_standing":
            # Detached fish from neighbouring source poses sit to the left of
            # the keeper; his own line and catch are always to his right.
            for frame in frames:
                ImageDraw.Draw(frame).rectangle((0, 0, 28 * D, frame.height), fill=(0, 0, 0, 0))
            # Replace the one source slot that contains only a detached catch,
            # then hold the clean late pull and final catch for readability.
            frames[13] = frames[12].copy()
            frames[14] = frames[15].copy()
    elif clip_name.startswith("keeper_hot_drink_"):
        # Keep the kettle, mug, spoon, liquid and steam in fixed equal cells,
        # including frames where the mug has detached from the keeper's hand.
        # Actor-centred component grouping excludes neighbouring poses whose
        # source silhouettes overlap the nominal equal-cell boundaries.
        if clip_name in {"keeper_hot_drink_pour", "keeper_hot_drink_pickup", "keeper_hot_drink_drink", "keeper_hot_drink_put_down"}:
            frames = generated_frames(source_name, frame_count, logical_width=logical_width, logical_height=logical_height, group_equal_components=True, scale_multiplier=anatomy_scale)
            # Steam and released mugs remain substantial/attached components;
            # the accidental neighbouring-frame slivers are all smaller.
            frames = [remove_small_alpha_components(frame, min_pixels=200) for frame in frames]
        else:
            frames = generated_frames(
                source_name,
                frame_count,
                logical_width=logical_width,
                logical_height=logical_height,
                preserve_equal_cells=True,
                scale_multiplier=anatomy_scale,
            )
    elif clip_name == "keeper_snooker":
        frames = generated_frames(source_name, 8, logical_width=logical_width, logical_height=logical_height)
    elif clip_name == "keeper_meal_place_side":
        # After release, the plated meal is detached from the keeper but remains
        # in the actor strip until the world object takes over.
        frames = generated_frames(source_name, 8, logical_width=logical_width, logical_height=logical_height, preserve_equal_cells=True, scale_multiplier=anatomy_scale)
        frames = [remove_small_alpha_components(frame, min_pixels=300) for frame in frames]
    else:
        try:
            frames = generated_frames(source_name, frame_count, logical_width=logical_width, logical_height=logical_height, scale_multiplier=anatomy_scale)
        except ValueError:
            # A few prop-heavy strips bridge adjacent x-runs.  Their prompts use
            # explicit equal cells; isolate the principal figure inside each cell
            # so a neighbour's overlapping prop cannot leak into the frame.
            frames = generated_frames(source_name, frame_count, logical_width=logical_width, logical_height=logical_height, force_equal_cells=True, scale_multiplier=anatomy_scale)
    if clip_name == "keeper_anti_gravity":
        # Body-axis clips use a centred pivot rather than feet-on-floor. Re-centre
        # each extracted pose, then add a deliberate two-pixel vertical float.
        # Frames 3-6 progress through one back flip; generated-source ordering is
        # authoritative and must not be rearranged during extraction.
        y_offsets = (2, 0, -1, 0, 0, 0, -1, 2)
        centred = []
        for frame, y_offset in zip(frames, y_offsets):
            bounds = frame.getchannel("A").getbbox()
            if bounds is None:
                raise ValueError("Anti-gravity frame is empty")
            centre_x = (bounds[0] + bounds[2]) // 2
            centre_y = (bounds[1] + bounds[3]) // 2
            dx = logical_width * D // 2 - centre_x
            dy = (logical_height // 2 + y_offset) * D - centre_y
            shifted = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            shifted.alpha_composite(frame, (dx, dy))
            centred.append(shifted)
        # Hold the calm face-down float before committing to the flip.
        frames = [centred[0].copy(), centred[1].copy(), centred[0].copy(), centred[1].copy()] + centred
    if clip_name == "keeper_fish_feed_up":
        frames.extend(frames[-1].copy() for _ in range(6))
    if clip_name == "keeper_trampoline_front":
        # Keep Frank's compact-beard redraw and give the bounce a conspicuously
        # higher world-space arc instead of bottom-aligning every source pose.
        frames = place_on_vertical_action_canvas(
            frames,
            80,
            (0, 4, 12, 24, 30, 22, 10, 0),
        )
        metadata["anchor_point"] = [logical_width // 2, 80]
    if clip_name == "keeper_darts":
        # Four additional aim oscillations make the draw-back readable before
        # the throw, while retaining the authored release/recovery frames.
        frames = frames[:2] + [frames[2].copy(), frames[3].copy()] * 4 + frames[4:]
    if clip_name == "keeper_drink_pint":
        frames[4] = frames[3].copy()
    if clip_name == "keeper_meal_place_side":
        # Remove the left-edge remnant of the preceding generated cell in the
        # one affected pose without touching the keeper or released plate.
        ImageDraw.Draw(frames[5]).rectangle((0, 0, 16 * D, frames[5].height), fill=(0, 0, 0, 0))
    if clip_name == "keeper_video_game":
        stable = [frames[index].copy() for index in (0, 0, 2, 2, 4, 4, 6, 6)]
        frames = [draw_video_game_controller(frame) for frame in stable]
    if clip_name in {"keeper_shower_enter", "keeper_shower_wash"}:
        frames = [recolor_privacy_mosaic(frame) for frame in frames]
    if clip_name in {"keeper_bath_wash", "keeper_hot_tub"}:
        frames = [remove_small_alpha_components(frame, min_pixels=80) for frame in frames]
    if clip_name.startswith("keeper_tarzan_walk_"):
        # Tarzan is bare-headed. Preserve the now original-matched
        # skull-to-sole scale but remove the 8 px of logical headwear clearance
        # inherited by the other costume families.
        frames = [frame.crop((0, 8 * D, 32 * D, 48 * D)) for frame in frames]
    if clip_name == "keeper_put_record":
        # The source's two middle poses touch by a few pixels.  The usable
        # figure begins well inside the cell; clear only that neighbour fringe.
        for frame in frames:
            ImageDraw.Draw(frame).rectangle((0, 0, 3 * D, frame.height), fill=(0, 0, 0, 0))
        for frame_index in range(4, len(frames)):
            frames[frame_index] = draw_held_record(frames[frame_index])
    if clip_name == "keeper_hot_drink_pickup":
        frames = [remove_small_alpha_components(frame, min_pixels=200) for frame in frames]
    clip_fps = 10 if clip_name == "keeper_bathrobe_walk" else 8
    save(clip_name, frames, clip_fps, **metadata)
    save_preview(clip_name.replace("_", "-"), frames, 100 if clip_fps == 10 else 120)

# Semantic aliases reuse approved motion while preserving object-specific lookup.
for clip_name, frames, metadata in (
    ("keeper_check_instrument_side", switch_side_frames, dict(hand_use_point=[27, 17], facing="right", interaction="check-instrument", mirror_safe=True, mirrors_for="left")),
    ("keeper_check_instrument_back", switch_back_frames, dict(hand_use_point=[26, 17], facing="back", interaction="check-instrument")),
    ("keeper_type_computer", piano_frames, dict(seat_point=[16, 29], hand_use_point=[24, 20], facing="front-right", interaction="type-computer", mirror_safe=True, mirrors_for="front-left")),
):
    save(clip_name, frames, 8, **metadata)
    save_preview(clip_name.replace("_", "-"), frames, 120)

print(f"Keeper batch authored in {OUT}")
