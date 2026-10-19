#!/usr/bin/env python3
"""Build Kitchen Rebuild V10 with structural cabinetry and isolated assets.

V10 preserves the accepted Rebuild V1 room, blue cabinet faces, table and bin,
but changes the compositing contract.  The six immutable 84-pixel slots are:

    fridge | two blue cabinets | oven | two blue cabinets (sink last)

Every interactive object is an alpha-isolated Off/On/Broken family.  State
art never contains wall, floor, counter or cabinet pixels.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-modular-2026-10-19-v10"
V1 = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1"
V9_SET = "kitchen-rebuild-states-2026-10-19-v9"
V9 = ROOT / "art/raw" / V9_SET
V9_CATALOGUE = ROOT / "art/drafts" / V9_SET / "candidate-catalogue.json"
RAW = ROOT / "art/raw" / SET
SOURCE = ROOT / "art/source" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-modular-v10"
ASSETS = PUBLIC / "assets"

ROOM = (772, 224)
BAY_X = {"fridge": 84, "kettle": 168, "toaster": 252, "oven": 336, "bowl": 420, "basin": 504}
BAY_CENTRES = {name: x + 42 for name, x in BAY_X.items()}
FLOOR_Y = 218
BODY_CELL = (84, 120)
PADDED_CELL = (88, 124)
BODY_OFFSET = (2, 2)
FRIDGE_CELL = (128, 130)
FRIDGE_ORIGIN = (42, 96)
OBJECT_ORIGIN = {name: (x - 2, 96) for name, x in BAY_X.items() if name != "fridge"}
OBJECT_ORIGIN["fridge"] = FRIDGE_ORIGIN
STATES = ("off", "on", "broken")
FRAMES = 40
FPS = 4

# Palette sampled from the accepted V1/V9 kitchen family.
INK = (8, 22, 34, 255)
INK_SOFT = (18, 42, 58, 255)
BLUE_DARK = (11, 49, 83, 255)
BLUE = (25, 74, 113, 255)
BLUE_LIGHT = (47, 101, 139, 255)
TEAL = (71, 137, 132, 255)
TEAL_LIGHT = (161, 201, 181, 255)
CREAM = (238, 218, 181, 255)
CREAM_LIGHT = (255, 241, 207, 255)
CREAM_SHADE = (207, 172, 126, 255)
WHITE = (250, 239, 215, 255)
ORANGE = (214, 91, 31, 255)
ORANGE_LIGHT = (255, 155, 59, 255)
RED = (227, 42, 28, 255)
BLACK = (13, 17, 21, 255)
WATER = (56, 168, 218, 210)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def pad(image: Image.Image) -> Image.Image:
    result = Image.new("RGBA", PADDED_CELL)
    result.alpha_composite(image, BODY_OFFSET)
    return result


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", BODY_CELL)
    return image, ImageDraw.Draw(image)


def draw_old_kettle(state: str) -> Image.Image:
    """Traditional single-spout whistling kettle, centred on the old anchor."""
    image, d = canvas()
    # Large arched top handle makes this read as an old-fashioned steam kettle.
    d.arc((25, 3, 59, 31), 188, 352, fill=INK, width=5)
    d.arc((28, 7, 56, 29), 188, 352, fill=BLUE_LIGHT, width=2)
    # Round enamel body and foot.
    d.ellipse((27, 16, 57, 43), fill=CREAM, outline=INK, width=2)
    d.polygon(((29, 30), (55, 30), (58, 40), (54, 44), (30, 44), (26, 40)), fill=CREAM, outline=INK)
    d.line((31, 39, 53, 39), fill=CREAM_SHADE, width=2)
    d.line((33, 42, 52, 42), fill=INK, width=2)
    d.ellipse((33, 14, 51, 20), fill=INK)
    if state != "broken":
        d.ellipse((35, 13, 49, 18), fill=CREAM_LIGHT, outline=INK)
        d.rectangle((40, 10, 44, 14), fill=ORANGE, outline=INK)
    else:
        # Open neck; the displaced lid is a separate static part of the state.
        d.ellipse((35, 13, 49, 18), fill=BLACK, outline=INK)
        d.ellipse((62, 35, 76, 40), fill=CREAM_LIGHT, outline=INK)
        d.rectangle((67, 32, 71, 36), fill=ORANGE, outline=INK)
        d.line((31, 33, 36, 29), fill=CREAM_SHADE, width=2)
    # Long tapered spout and whistle cap on the right.
    d.polygon(((54, 24), (67, 17), (72, 19), (59, 31)), fill=CREAM, outline=INK)
    d.ellipse((68, 15, 76, 22), fill=INK)
    d.ellipse((69, 16, 74, 20), fill=ORANGE if state == "on" else CREAM_SHADE)
    d.line((32, 23, 34, 34), fill=CREAM_LIGHT, width=2)
    return pad(image)


def draw_one_slice_toaster(state: str) -> Image.Image:
    image, d = canvas()
    if state in {"on", "broken"}:
        toast_fill = (48, 36, 28, 255) if state == "broken" else (213, 143, 72, 255)
        toast_edge = BLACK if state == "broken" else (105, 57, 25, 255)
        d.rounded_rectangle((34, 10, 50, 29), radius=4, fill=toast_fill, outline=toast_edge, width=2)
        if state == "on":
            d.line((37, 14, 47, 14), fill=(244, 186, 103, 255), width=2)
        else:
            d.point((38, 17), fill=(90, 69, 54, 255)); d.point((46, 21), fill=(94, 71, 53, 255))
    # Deliberately narrow one-slot body, centred on the unchanged bay centre.
    d.rounded_rectangle((25, 25, 59, 44), radius=5, fill=CREAM, outline=INK, width=2)
    d.line((29, 28, 55, 28), fill=CREAM_LIGHT, width=2)
    d.rounded_rectangle((31, 22, 53, 28), radius=3, fill=INK, outline=CREAM_SHADE)
    d.line((29, 41, 55, 41), fill=CREAM_SHADE, width=2)
    d.rectangle((59, 31, 64, 34), fill=ORANGE, outline=INK)
    d.rectangle((29, 44, 34, 46), fill=INK); d.rectangle((51, 44, 56, 46), fill=INK)
    if state == "broken":
        d.line((28, 34, 34, 31), fill=(75, 59, 52, 255), width=2)
        d.line((51, 36, 56, 39), fill=(75, 59, 52, 255), width=2)
    return pad(image)


def draw_bowl(state: str) -> Image.Image:
    image, d = canvas()
    if state != "broken":
        d.ellipse((22, 27, 62, 37), fill=CREAM_LIGHT, outline=INK, width=2)
        d.pieslice((24, 26, 60, 47), 0, 180, fill=CREAM, outline=INK, width=2)
        d.arc((25, 30, 59, 44), 0, 180, fill=BLUE_LIGHT, width=2)
        d.line((30, 41, 55, 41), fill=CREAM_SHADE, width=2)
    else:
        d.polygon(((11, 31), (34, 29), (39, 34), (34, 42), (21, 41)), fill=CREAM, outline=INK)
        d.line((14, 32, 34, 33), fill=BLUE_LIGHT, width=2)
        d.polygon(((46, 34), (51, 28), (74, 31), (68, 41), (53, 42)), fill=CREAM, outline=INK)
        d.line((51, 32, 72, 33), fill=BLUE_LIGHT, width=2)
        d.polygon(((39, 34), (44, 31), (47, 36), (44, 39)), fill=CREAM_SHADE, outline=INK)
    return pad(image)


def draw_basin(state: str) -> Image.Image:
    image, d = canvas()
    # Basin rim is an object overlay; the blue worktop remains wholly structural.
    d.rounded_rectangle((6, 34, 78, 46), radius=3, fill=CREAM_LIGHT, outline=INK, width=2)
    d.ellipse((14, 34, 69, 43), fill=(173, 197, 183, 255), outline=CREAM_SHADE, width=1)
    d.ellipse((22, 36, 61, 42), fill=(31, 75, 93, 255), outline=INK)
    # Brass/copper taps and a high, readable spout.
    d.ellipse((27, 29, 34, 36), fill=ORANGE, outline=INK)
    d.ellipse((66, 29, 73, 36), fill=ORANGE, outline=INK)
    d.line((30, 29, 30, 25), fill=INK, width=2); d.line((69, 29, 69, 25), fill=INK, width=2)
    if state != "broken":
        d.line((52, 32, 52, 14), fill=INK, width=4)
        d.arc((51, 8, 69, 27), 180, 302, fill=INK, width=4)
        d.line((65, 19, 65, 28), fill=INK, width=4)
        d.line((53, 31, 53, 15), fill=CREAM_SHADE, width=1)
    else:
        d.line((52, 32, 52, 17), fill=INK, width=4)
        d.line((52, 17, 60, 10), fill=INK, width=4)
        d.line((60, 10, 64, 15), fill=INK, width=3)
        d.line((63, 13, 68, 8), fill=CREAM_SHADE, width=2)
    return pad(image)


def draw_fridge(state: str) -> Image.Image:
    """Same installed 84 x 78 body in every state; broken parts may overflow."""
    base = Image.new("RGBA", (124, 126))
    d = ImageDraw.Draw(base)
    # Installed body: room x=84..167, y=140..217 when placed at (44,98).
    d.rounded_rectangle((40, 42, 123, 119), radius=3, fill=WHITE, outline=INK, width=2)
    d.rectangle((44, 47, 119, 111), fill=CREAM_LIGHT, outline=CREAM_SHADE, width=1)
    d.line((44, 48, 119, 48), fill=(255, 249, 228, 255), width=2)
    d.line((44, 112, 119, 112), fill=INK_SOFT, width=2)
    for x in range(50, 114, 8):
        d.line((x, 115, x + 4, 115), fill=BLUE_DARK)
    d.rectangle((109, 58, 114, 91), fill=ORANGE, outline=INK)
    d.line((110, 60, 110, 88), fill=ORANGE_LIGHT)
    if state == "on":
        d.ellipse((47, 52, 51, 56), fill=(89, 199, 212, 255), outline=INK)
    if state == "broken":
        # Replace the closed door with a dark, stocked cavity.
        d.rectangle((43, 45, 120, 112), fill=INK, outline=BLACK, width=2)
        d.rectangle((47, 49, 116, 108), fill=(35, 61, 66, 255), outline=CREAM_SHADE)
        d.line((48, 69, 115, 69), fill=(191, 214, 200, 255), width=2)
        d.line((48, 88, 115, 88), fill=(191, 214, 200, 255), width=2)
        # Generic small contents, deliberately unlabelled.
        d.rectangle((51, 55, 63, 67), fill=(178, 72, 48, 255), outline=INK)
        d.ellipse((72, 55, 85, 67), fill=(211, 184, 82, 255), outline=INK)
        d.rectangle((93, 53, 109, 68), fill=(210, 226, 208, 255), outline=INK)
        d.ellipse((54, 73, 68, 85), fill=(104, 157, 91, 255), outline=INK)
        d.rectangle((78, 74, 92, 86), fill=(220, 137, 66, 255), outline=INK)
        d.ellipse((98, 74, 111, 86), fill=(214, 224, 230, 255), outline=INK)
        # Top hinge failed; lower-right hinge remains visibly attached.
        d.ellipse((115, 103, 123, 113), fill=ORANGE, outline=INK)
        # Door falls toward the left; its lower-left corner meets floor y=120.
        door = ((19, 52), (105, 66), (101, 116), (5, 120))
        d.polygon(door, fill=WHITE, outline=INK)
        d.line((23, 57, 99, 69), fill=CREAM_SHADE, width=2)
        d.line((11, 115, 96, 111), fill=CREAM_SHADE, width=2)
        d.polygon(((87, 73), (94, 74), (91, 103), (84, 102)), fill=ORANGE, outline=INK)
        d.line((89, 76, 87, 99), fill=ORANGE_LIGHT)
        # Static floor pool; y=120 is the actual room floor surface.
        d.ellipse((0, 118, 82, 125), fill=WATER)
        d.ellipse((18, 119, 66, 123), outline=(148, 224, 240, 220), width=1)
    result = Image.new("RGBA", FRIDGE_CELL)
    result.alpha_composite(base, (2, 2))
    return result


def draw_oven(state: str, broken_lit: bool = False) -> Image.Image:
    image, d = canvas()
    # One standalone 84-pixel cooker: its own hob and body, no blue worktop.
    d.rounded_rectangle((2, 34, 81, 119), radius=2, fill=CREAM, outline=INK, width=2)
    d.rectangle((4, 34, 79, 50), fill=CREAM_LIGHT, outline=INK, width=2)
    d.rectangle((8, 36, 75, 45), fill=(39, 58, 60, 255), outline=INK)
    for box in ((13, 37, 27, 43), (32, 37, 46, 43), (52, 37, 69, 43)):
        d.ellipse(box, fill=(27, 36, 40, 255), outline=(116, 77, 51, 255))
    d.rectangle((4, 50, 79, 69), fill=CREAM_LIGHT, outline=INK)
    dial_x = (14, 29, 44, 59)
    for x in dial_x:
        d.ellipse((x, 55, x + 7, 62), fill=ORANGE, outline=INK)
        d.line((x + 3, 56, x + 3, 59), fill=ORANGE_LIGHT)
    d.ellipse((70, 56, 76, 62), fill=RED if state == "on" else (106, 52, 33, 255), outline=INK)
    lit = state == "on" or broken_lit
    cavity_fill = (112, 55, 26, 255) if lit else BLACK
    d.rounded_rectangle((9, 71, 73, 103), radius=2, fill=cavity_fill, outline=INK, width=2)
    if lit:
        d.rectangle((13, 75, 69, 98), fill=(185, 91, 35, 255), outline=(78, 42, 24, 255))
        d.line((15, 78, 67, 78), fill=(255, 199, 92, 255), width=2)
    else:
        d.line((13, 78, 69, 78), fill=(57, 63, 62, 255), width=1)
    # Roasting tray and contents in On/Broken states.
    if state in {"on", "broken"}:
        d.rectangle((19, 89, 63, 97), fill=(80, 56, 37, 255), outline=INK)
        roast = (31, 85, 53, 95)
        d.ellipse(roast, fill=BLACK if state == "broken" else (196, 105, 38, 255), outline=INK)
        if state == "on":
            d.line((34, 87, 49, 87), fill=ORANGE_LIGHT, width=2)
    if state != "broken":
        # Closed door with transparent/dark window treatment.
        d.rounded_rectangle((7, 68, 75, 106), radius=2, outline=INK, width=2)
        d.rectangle((14, 75, 68, 99), outline=CREAM_SHADE, width=2)
    else:
        # One dial hangs by two wires; remove the original dial from the fascia.
        d.rectangle((57, 53, 69, 65), fill=CREAM_LIGHT)
        d.line((62, 60, 66, 73), fill=(91, 45, 32, 255), width=1)
        d.line((66, 60, 70, 73), fill=(41, 48, 55, 255), width=1)
        d.ellipse((65, 70, 75, 80), fill=ORANGE, outline=INK)
        # Door opens straight toward camera: horizontal, centred and foreshortened.
        d.rectangle((10, 101, 72, 105), fill=(45, 30, 24, 255), outline=INK)
        d.rounded_rectangle((7, 105, 75, 118), radius=2, fill=CREAM, outline=INK, width=2)
        d.rectangle((16, 108, 66, 115), fill=(25, 31, 33, 210), outline=CREAM_SHADE)
        d.line((11, 117, 71, 117), fill=CREAM_SHADE)
    d.rectangle((8, 118, 18, 119), fill=INK); d.rectangle((65, 118, 75, 119), fill=INK)
    return pad(image)


def cabinet_module(source_name: str) -> Image.Image:
    """Exact V1 lower cabinet with the exact clean fridge worktop above it."""
    source = Image.open(V1 / source_name).convert("RGBA")
    clean = Image.open(V1 / "bay-fridge.png").convert("RGBA")
    out = Image.new("RGBA", BODY_CELL)
    out.alpha_composite(clean.crop((0, 35, 84, 53)), (0, 35))
    out.alpha_composite(source.crop((0, 53, 84, 120)), (0, 53))
    return out


def cabinet_runs() -> tuple[Image.Image, Image.Image]:
    left = Image.new("RGBA", (168, 120))
    right = Image.new("RGBA", (168, 120))
    left.alpha_composite(cabinet_module("bay-kettle.png"), (0, 0))
    left.alpha_composite(cabinet_module("bay-toaster.png"), (84, 0))
    right.alpha_composite(cabinet_module("bay-mixing-bowl.png"), (0, 0))
    right.alpha_composite(cabinet_module("bay-basin.png"), (84, 0))
    # The fridge counter crop has finished outer ends.  At the internal join of
    # each two-bay run, replace those two end tapers with a neutral centre
    # sample from the same accepted V1 worktop.  The result is one uninterrupted
    # slab per run, with finished ends only beside the standalone appliances.
    clean = Image.open(V1 / "bay-fridge.png").convert("RGBA")
    bridge = clean.crop((38, 35, 46, 53))
    left.alpha_composite(bridge, (80, 35))
    right.alpha_composite(bridge, (80, 35))
    return left, right


def timed_full_state_strip(frame: Image.Image, active: set[int]) -> Image.Image:
    strip = Image.new("RGBA", (PADDED_CELL[0] * FRAMES, PADDED_CELL[1]))
    for index in active:
        strip.alpha_composite(frame, (index * PADDED_CELL[0], 0))
    return strip


def warning_strip(active: set[int]) -> Image.Image:
    strip = Image.new("RGBA", (PADDED_CELL[0] * FRAMES, PADDED_CELL[1]))
    for index in active:
        cell = Image.new("RGBA", PADDED_CELL)
        d = ImageDraw.Draw(cell)
        # Matches the physical warning lamp on the cooker fascia.
        d.ellipse((70, 56, 80, 66), fill=(255, 46, 24, 86))
        d.ellipse((73, 59, 78, 64), fill=(255, 76, 32, 255), outline=(122, 21, 17, 255))
        d.point((75, 60), fill=(255, 232, 160, 255))
        strip.alpha_composite(cell, (index * PADDED_CELL[0], 0))
    return strip


def compose(background: Image.Image, left: Image.Image, right: Image.Image, table: Image.Image,
            objects: dict[str, dict[str, Image.Image]], states: dict[str, str], bin_state: str) -> Image.Image:
    room = background.copy()
    room.alpha_composite(left, (168, 98))
    room.alpha_composite(right, (420, 98))
    room.alpha_composite(Image.open(V9 / f"bin-{bin_state}.png").convert("RGBA"), (8, 149))
    for name in ("fridge", "kettle", "toaster", "oven", "bowl", "basin"):
        room.alpha_composite(objects[name][states[name]], OBJECT_ORIGIN[name])
    room.alpha_composite(table, (680, 129))
    return room


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_rebuild_states_v9.html").read_text()
    cards = "".join(
        f'<article><h3>{asset.title()} · {state.title()}</h3>'
        f'<div class="cell"><img src="assets/{asset}-{state}.png" alt="isolated {asset} {state}"></div>'
        f'<p class="readout">anchor {catalogue["interactionAnchors"][asset]}</p></article>'
        for asset in ("fridge", "kettle", "toaster", "oven", "bowl", "basin")
        for state in STATES
    )
    template = template.replace('/keeper-review/kitchen-rebuild-states-v9/', '/keeper-review/kitchen-rebuild-modular-v10/')
    template = template.replace('Kitchen Rebuild V9 · irregular failing-bulb flicker', 'Kitchen Rebuild V10 · modular structural separation')
    template = template.replace('Rebuild V9 reversible draft', 'Rebuild V10 reversible modular draft')
    template = template.replace('Kitchen broken-state animation builder', 'Modular kitchen states and animation builder')
    template = template.replace('while everything else stays Standard', 'while everything else stays Off')
    template = template.replace('The approved On-state combination remains a fixed comparison view.', 'On states use the same isolated bodies over two unchanged cabinet runs.')
    template = template.replace('<section><h2>All On · native game size</h2>', '<section><h2>Structure only · two cabinet runs</h2><p>No appliance or countertop object is baked into this layer. Empty slots remain for the standalone fridge and oven.</p><div class="stage"><canvas id="structure" width="772" height="224"></canvas></div></section><section><h2>All Off · native game size</h2><div class="stage"><canvas id="all-off" width="772" height="224"></canvas></div></section><section><h2>Keeper stop/turn anchor proof</h2><p>Each crosshair is fixed to the centre of its original 84-pixel bay at the y=218 walking plane. Off, On and Broken states retain these exact coordinates.</p><div class="stage"><canvas id="anchors" width="772" height="224"></canvas></div></section><section><h2>All On · native game size</h2>')
    template = template.replace('V9 draft only. Nothing is promoted to Final or runtime. Rejecting it requires deleting only the V9 directories; accepted V8 geometry remains immutable.', 'V10 draft only. Nothing is promoted to Final or runtime. Rejecting it requires deleting only the V10 directories; V1–V9 remain immutable.')
    template = template.replace("KEY='kitchen-rebuild-v9-asset-layer-config'", "KEY='kitchen-rebuild-v10-asset-layer-config'")
    template = template.replace("a.download='kitchen-rebuild-v9-asset-layers.json'", "a.download='kitchen-rebuild-v10-asset-layers.json'")
    template = template.replace('.cell img{max-height:245px;max-width:95%;image-rendering:pixelated}', '.cell img{height:240px;width:auto;max-width:95%;object-fit:contain;image-rendering:pixelated}')
    template = template.replace("const CENTRE={fridge:[104,139],kettle:[198,104],toaster:[282,100],oven:[378,103],bowl:[450,112],basin:[534,98],bin:[44,158]};", "const CENTRE={fridge:[126,139],kettle:[210,116],toaster:[294,116],oven:[378,116],bowl:[462,116],basin:[546,116],bin:[44,158]};")
    template = template.replace("const presets={on:{fridge:'standard',kettle:'on',toaster:'on',oven:'on',bowl:'standard',basin:'on',bin:'standard'},broken:{fridge:'broken',kettle:'broken',toaster:'broken',oven:'broken',bowl:'broken',basin:'broken',bin:'broken'},mixed:{fridge:'broken',kettle:'on',toaster:'broken',oven:'on',bowl:'broken',basin:'on',bin:'broken'}};", "const presets={off:{fridge:'off',kettle:'off',toaster:'off',oven:'off',bowl:'off',basin:'off',bin:'standard'},on:{fridge:'on',kettle:'on',toaster:'on',oven:'on',bowl:'on',basin:'on',bin:'standard'},broken:{fridge:'broken',kettle:'broken',toaster:'broken',oven:'broken',bowl:'broken',basin:'broken',bin:'broken'},mixed:{fridge:'broken',kettle:'on',toaster:'broken',oven:'broken',bowl:'on',basin:'broken',bin:'broken'}};")
    old_draw = "function drawBase(ctx,states){ctx.clearRect(0,0,772,224);ctx.drawImage(images['kitchen-background.png'],0,0);ctx.drawImage(images[states.bin==='broken'?'bin-broken.png':'bin-standard.png'],8,149);for(const asset of ['fridge','kettle','toaster','oven','bowl','basin']){const value=states[asset],o=DATA.objectOrigins[`${asset}-${value}`];ctx.drawImage(images[`${asset}-${value}.png`],o[0],o[1])}ctx.drawImage(images['table-chair.png'],680,129)}"
    new_draw = "function drawStructure(ctx,table=true){ctx.clearRect(0,0,772,224);ctx.drawImage(images['kitchen-background.png'],0,0);ctx.drawImage(images['cabinet-run-left.png'],168,98);ctx.drawImage(images['cabinet-run-right.png'],420,98);if(table)ctx.drawImage(images['table-chair.png'],680,129)}function drawBase(ctx,states){drawStructure(ctx);ctx.drawImage(images[states.bin==='broken'?'bin-broken.png':'bin-standard.png'],8,149);for(const asset of ['fridge','kettle','toaster','oven','bowl','basin']){const value=states[asset],o=DATA.objectOrigins[`${asset}-${value}`];ctx.drawImage(images[`${asset}-${value}.png`],o[0],o[1])}}"
    template = template.replace(old_draw, new_draw)
    template = template.replace("function drawCanonicalOn(ctx){for(const family of ['kettle-on-steam','toaster-on-heat','basin-on-flow']){const m=DATA.effects[DATA.effectFamilies[family].default];drawLayer(ctx,{model:DATA.effectFamilies[family].default,x:m.origin[0],y:m.origin[1],w:m.size[0],h:m.size[1],speed:1,crop:[0,0,0,0]})}}", "function drawCanonicalOn(ctx,states){for(const family of ['kettle-on-steam','toaster-on-heat','basin-on-flow']){const model=DATA.effectFamilies[family].default,m=DATA.effects[model];if(states[m.asset]==='on')drawLayer(ctx,{model,x:m.origin[0],y:m.origin[1],w:m.size[0],h:m.size[1],speed:1,crop:[0,0,0,0]})}}")
    template = template.replace("function drawScene(id,states,layerAssets=[],box=false){const ctx=$(id).getContext('2d');ctx.imageSmoothingEnabled=false;drawBase(ctx,states);if(id==='#all-on')drawCanonicalOn(ctx);const sceneLayers=layerAssets.flatMap(asset=>layers[asset]).sort((a,b)=>layerOrder(a)-layerOrder(b));", "function drawScene(id,states,layerAssets=[],box=false){const ctx=$(id).getContext('2d');ctx.imageSmoothingEnabled=false;drawBase(ctx,states);drawCanonicalOn(ctx,states);const sceneLayers=layerAssets.filter(asset=>states[asset]==='broken').flatMap(asset=>layers[asset]).sort((a,b)=>layerOrder(a)-layerOrder(b));")
    template = template.replace("function focusPreset(){const p={fridge:'standard',kettle:'standard',toaster:'standard',oven:'standard',bowl:'standard',basin:'standard',bin:'standard'};p[selectedAsset]='broken';return p}", "function focusPreset(){const p={fridge:'off',kettle:'off',toaster:'off',oven:'off',bowl:'off',basin:'off',bin:'standard'};p[selectedAsset]='broken';return p}")
    template = template.replace("function render(){if(!state.loaded)return;drawScene('#all-on',presets.on);drawScene('#all-broken',presets.broken,ASSETS);drawScene('#mixed',presets.mixed,['fridge','toaster','bowl','bin']);drawScene('#workbench',focusPreset(),[selectedAsset],true)}", "function render(){if(!state.loaded)return;const structure=$('#structure').getContext('2d');structure.imageSmoothingEnabled=false;drawStructure(structure);drawScene('#all-off',presets.off);const anchor=$('#anchors').getContext('2d');anchor.imageSmoothingEnabled=false;drawBase(anchor,presets.off);anchor.font='8px ui-monospace,monospace';anchor.textAlign='center';for(const [asset,[x,y]] of Object.entries(DATA.interactionAnchors)){anchor.strokeStyle='#ffcf55';anchor.beginPath();anchor.moveTo(x,118);anchor.lineTo(x,y);anchor.stroke();anchor.fillStyle='#65fbff';anchor.fillRect(x-2,y-2,5,5);anchor.fillStyle='#17344b';anchor.fillText(asset,x,116)}drawScene('#all-on',presets.on);drawScene('#all-broken',presets.broken,ASSETS);drawScene('#mixed',presets.mixed,ASSETS);drawScene('#workbench',focusPreset(),[selectedAsset],true)}")
    return template.replace('__DATA__', json.dumps(catalogue, separators=(",", ":"))).replace('__CARDS__', cards)


def main() -> None:
    v9 = json.loads(V9_CATALOGUE.read_text())
    for directory in (RAW, SOURCE, DRAFT, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (RAW, SOURCE, DRAFT, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    background = Image.open(V1 / "kitchen-standard-background.png").convert("RGBA")
    table = Image.open(V9 / "table-chair.png").convert("RGBA")
    left, right = cabinet_runs()
    objects = {
        "fridge": {state: draw_fridge(state) for state in STATES},
        "kettle": {state: draw_old_kettle(state) for state in STATES},
        "toaster": {state: draw_one_slice_toaster(state) for state in STATES},
        "oven": {state: draw_oven(state) for state in STATES},
        "bowl": {state: draw_bowl(state) for state in STATES},
        "basin": {state: draw_basin(state) for state in STATES},
    }

    outputs: dict[str, dict[str, object]] = {}
    fixed = {
        "kitchen-background.png": background,
        "cabinet-run-left.png": left,
        "cabinet-run-right.png": right,
        "table-chair.png": table,
        "bin-standard.png": Image.open(V9 / "bin-standard.png").convert("RGBA"),
        "bin-broken.png": Image.open(V9 / "bin-broken.png").convert("RGBA"),
    }
    for name, image in fixed.items():
        save(image, RAW / name); save(image, ASSETS / name)
        outputs[name] = {"sha256": sha(RAW / name), "pixels": list(image.size)}
    for asset, variants in objects.items():
        for state, image in variants.items():
            name = f"{asset}-{state}.png"
            save(image, RAW / name); save(image, ASSETS / name)
            outputs[name] = {"sha256": sha(RAW / name), "pixels": list(image.size)}

    # Preserve every reusable V9 effect except the two oven-locked families,
    # which must match the new isolated cooker exactly.
    effects = json.loads(json.dumps(v9["effects"]))
    families = json.loads(json.dumps(v9["effectFamilies"]))
    for name, meta in effects.items():
        if name.startswith("oven-broken-cavity-flicker") or name.startswith("oven-broken-warning-flicker"):
            continue
        src = V9 / meta["file"]
        shutil.copyfile(src, RAW / meta["file"]); shutil.copyfile(src, ASSETS / meta["file"])
        image = Image.open(src)
        outputs[meta["file"]] = {"sha256": sha(src), "pixels": list(image.size)}

    cavity_timing = {
        "classic": {2, 6, 7, 13, 19, 22, 23, 24, 31, 35, 38},
        "slow": {1, 4, 10, 11, 16, 21, 22, 29, 33, 34, 35},
        "erratic": {3, 9, 15, 16, 24, 29, 31, 33, 34, 36, 38},
    }
    warning_timing = {
        "classic": {1, 2, 8, 14, 15, 23, 29, 30, 37},
        "rapid": {2, 3, 5, 9, 10, 11, 17, 19, 20, 26, 27, 32, 34, 35, 38},
        "angry": {0, 1, 2, 5, 6, 11, 12, 13, 19, 20, 22, 23, 24, 31, 32, 36, 38, 39},
    }
    lit_broken = draw_oven("broken", broken_lit=True)
    for model, active in cavity_timing.items():
        key = f"oven-broken-cavity-flicker--{model}"
        filename = f"fx-{key}-f40.png"
        strip = timed_full_state_strip(lit_broken, active)
        save(strip, RAW / filename); save(strip, ASSETS / filename)
        effects[key].update({"file": filename, "origin": [334, 96], "size": [88, 124], "cellPixels": [88, 124], "timingFrames": sorted(active), "isolatedObjectOnly": True})
        outputs[filename] = {"sha256": sha(RAW / filename), "pixels": list(strip.size)}
    for model, active in warning_timing.items():
        key = f"oven-broken-warning-flicker--{model}"
        filename = f"fx-{key}-f40.png"
        strip = warning_strip(active)
        save(strip, RAW / filename); save(strip, ASSETS / filename)
        effects[key].update({"file": filename, "origin": [334, 96], "size": [88, 124], "cellPixels": [88, 124], "timingFrames": sorted(active), "isolatedObjectOnly": True})
        outputs[filename] = {"sha256": sha(RAW / filename), "pixels": list(strip.size)}

    # Correct canonical starts for the redesigned props while retaining drag,
    # crop, resize and speed controls.
    for key, meta in effects.items():
        if key.startswith("kettle-on-steam"):
            meta.update({"origin": [170, 4], "size": [120, 144]})
        elif key.startswith("kettle-broken-steam"):
            meta.update({"origin": [150, -27], "size": [120, 144]})
        elif key.startswith("toaster-on-heat"):
            meta.update({"origin": [234, 4], "size": [120, 144]})
        elif key.startswith("toaster-broken-smoke"):
            meta.update({"origin": [234, -25], "size": [120, 144]})
        elif key.startswith("basin-on-flow"):
            meta.update({"origin": [524, 54], "size": [60, 80]})

    off = {name: "off" for name in BAY_X}
    on = {name: "on" for name in BAY_X}
    broken = {name: "broken" for name in BAY_X}
    mixed = {"fridge": "broken", "kettle": "on", "toaster": "broken", "oven": "broken", "bowl": "on", "basin": "broken"}
    rooms = {
        "kitchen-structure-only.png": compose(background, left, right, table, objects, off, "standard"),
        "kitchen-all-off-static.png": compose(background, left, right, table, objects, off, "standard"),
        "kitchen-all-on-static.png": compose(background, left, right, table, objects, on, "standard"),
        "kitchen-all-broken-static.png": compose(background, left, right, table, objects, broken, "broken"),
        "kitchen-mixed-static.png": compose(background, left, right, table, objects, mixed, "broken"),
    }
    # True structure proof intentionally omits all six objects and the bin.
    structure = background.copy(); structure.alpha_composite(left, (168, 98)); structure.alpha_composite(right, (420, 98)); structure.alpha_composite(table, (680, 129))
    rooms["kitchen-structure-only.png"] = structure
    for name, image in rooms.items():
        save(image, RAW / name); save(image, ASSETS / name)
        outputs[name] = {"sha256": sha(RAW / name), "pixels": list(image.size)}

    object_origins = {f"{asset}-{state}": list(OBJECT_ORIGIN[asset]) for asset in BAY_X for state in STATES}
    interaction = {asset: [BAY_CENTRES[asset], FLOOR_Y] for asset in BAY_X}
    installed = {asset: [x, 98, 84, 120] for asset, x in BAY_X.items()}
    media = list(outputs)
    catalogue = {
        "set": SET,
        "version": 10,
        "status": "modular-structural-separation-awaiting-visual-review",
        "layout": {
            "sequence": ["fridge", "cabinet-run-left", "oven", "cabinet-run-right", "table"],
            "slotOrder": list(BAY_X),
            "bayWidthPixels": 84,
            "roomPixels": list(ROOM),
            "cabinetRuns": {"left": {"origin": [168, 98], "pixels": [168, 120]}, "right": {"origin": [420, 98], "pixels": [168, 120], "includesSinkCabinet": True}},
        },
        "method": {
            "structuralCabinetLayer": True,
            "objectOnlyTransparentStates": True,
            "standaloneFridge": True,
            "standaloneOvenAndHob": True,
            "fixedInteractionAnchors": True,
            "assetFirstLayerWorkbench": True,
            "environmentalEffectsSeparate": True,
            "canonicalLoopSeconds": 10,
        },
        "states": {asset: list(STATES) for asset in BAY_X},
        "objectOrigins": object_origins,
        "installedSlots": installed,
        "interactionAnchors": interaction,
        "interactionAnchorRule": "Every state retains the bay-centre x and room-floor y stop/turn anchor; overflow never moves the installed body.",
        "effectFamilies": families,
        "effects": effects,
        "allOff": {**off, "bin": "standard"},
        "allOn": {**on, "bin": "standard"},
        "allBroken": {**broken, "bin": "broken"},
        "mixedPreset": {**mixed, "bin": "broken"},
        "sourceProvenance": {
            "immutableV1BackgroundSha256": sha(V1 / "kitchen-standard-background.png"),
            "immutableV1CabinetSources": {name: sha(V1 / name) for name in ("bay-fridge.png", "bay-kettle.png", "bay-toaster.png", "bay-mixing-bowl.png", "bay-basin.png")},
            "immutableV9CatalogueSha256": sha(V9_CATALOGUE),
            "imageGenerationMode": "deterministic-project-native-Pillow; no stochastic bitmap generation used after exact-geometry audit",
        },
        "sfxPlaceholders": [
            "kitchen_fridge_low_electrical_buzz_loop",
            "kitchen_kettle_boiling_steam_loop",
            "kitchen_kettle_broken_pressure_hiss_loop",
            "kitchen_toaster_heat_hum_loop",
            "kitchen_toaster_burnt_smoke_crackle_loop",
            "kitchen_oven_on_fan_loop",
            "kitchen_oven_broken_smoke_hiss_loop",
            "kitchen_oven_broken_warning_flicker_loop",
            "kitchen_bowl_ceramic_break_one_shot",
            "kitchen_basin_gentle_flow_loop",
            "kitchen_basin_broken_upward_spray_loop",
            "kitchen_bin_flies_slow_loop",
        ],
        "outputs": outputs,
        "media": media,
        "promotion": "none",
        "runtimeWiring": "unchanged",
    }
    (SOURCE / "construction.json").write_text(json.dumps({"palette": {"ink": INK, "blue": BLUE, "cream": CREAM}, "layout": catalogue["layout"], "anchors": interaction}, indent=2) + "\n")
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "set": SET,
        "status": "awaiting-modular-family-visual-review",
        "parent": V9_SET,
        "preserves": ["Rebuild V1 room/cabinet palette and lower faces", "approved V28/V31 bin", "V9 reusable effect families and controls"],
        "promotion": "none",
        "runtimeWiring": "unchanged",
        "rollback": "Delete V10 source/raw/draft/review/archive/builder/verifier/docs files only; V1–V9 remain immutable.",
    }, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: two cabinet runs, 18 isolated object states, {len(effects)} effect models")


if __name__ == "__main__":
    main()
