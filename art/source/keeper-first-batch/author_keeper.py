#!/usr/bin/env python3
"""Author the first aligned keeper sprite batch at density 4."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "art/raw/keeper-first-batch"
OUT.mkdir(parents=True, exist_ok=True)

D = 4
W, H = 32 * D, 40 * D
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


def contract(frames, fps, pivot=None):
    value = {"w": 32, "h": 40, "frames": frames, "fps": fps, "density": 4, "anchor": [16, 40], "z": 50}
    if pivot is not None: value["pivot"] = pivot
    return value


def save(name, frames, fps=0, pivot=None):
    strip = Image.new("RGBA", (W * len(frames), H), (0, 0, 0, 0))
    for i, frame in enumerate(frames): strip.alpha_composite(frame, (i * W, 0))
    png = OUT / f"{name}_f{len(frames)}.png"
    strip.save(png, optimize=True)
    png.with_suffix(".json").write_text(json.dumps(contract(len(frames), fps, pivot), indent=2) + "\n")


PIVOTS = {"torso": [16, 25], "arm_l": [10, 15], "arm_r": [22, 15], "leg_l": [13, 25], "leg_r": [19, 25]}
for view in ("front", "back"):
    for p in ("torso", "arm_l", "arm_r", "leg_l", "leg_r"):
        save(f"keeper_{view}_{p}", [part(p, view == "back")], pivot=PIVOTS[p])
for mood in ("happy", "neutral", "grumpy", "asleep", "open"):
    save(f"keeper_front_head_{mood}", [part("head", False, mood)], pivot=[16, 11])
save("keeper_back_head", [part("head", True)], pivot=[16, 11])
save("keeper_reference", [compose("front", "neutral")])

save("keeper_idle", [compose("front", "neutral", bob=b) for b in (0, 0, -1, 0)], 6)
save("keeper_walk", [compose("front", "neutral", phase=p, bob=-abs(p) // 2) for p in (-2, -1, 0, 1, 2, 1, 0, -1)], 10)
save("keeper_cook_back", [compose("back", hands=h, bob=b) for h, b in ((4, 0), (5, -1), (6, -1), (5, 0), (4, 0), (3, 0))], 8)
save("keeper_wash_back", [compose("back", hands=h, bob=b) for h, b in ((3, 0), (4, 0), (5, -1), (4, -1), (3, 0), (2, 0))], 8)
save("keeper_brush_teeth_back", [compose("back", hands=h, bob=b) for h, b in ((4, 0), (6, 0), (4, 0), (6, -1), (4, -1), (5, 0))], 8)

# A transparent source contact sheet makes alignment mistakes easy to spot.
contact = Image.new("RGBA", (W * 3, H * 2), (244, 236, 214, 255))
for i, frame in enumerate((compose("front", "happy"), compose("front"), compose("back"), compose("front", phase=-2), compose("front", phase=2), compose("back", hands=5))):
    contact.alpha_composite(frame, ((i % 3) * W, (i // 3) * H))
contact.save(Path(__file__).with_name("keeper-contact-sheet.png"), optimize=True)
print(f"Keeper batch authored in {OUT}")
