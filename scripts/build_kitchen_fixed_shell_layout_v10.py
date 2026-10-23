#!/usr/bin/env python3
"""Build Kitchen Fixed Shell Layout V10 from the immutable V9 review.

V10 changes only the two exposed end returns, the Broken dishwasher door and
the requested Kettle/Toaster/Mixing-bowl state families.  V9's accepted front
grid, fronts, sink, worktop, appliance controls and interaction datums remain
byte-derived and unmoved.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

import build_kitchen_fixed_shell_layout_v6 as v6
import build_kitchen_fixed_shell_layout_v8 as v8
import build_kitchen_fixed_shell_layout_v9 as v9


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-fixed-shell-2026-10-23-v10"
PUBLIC_SLUG = "kitchen-fixed-shell-layout-v10"
ATLAS_NAME = "kitchen-fixed-shell-atlas-v10.png"
OUT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review" / PUBLIC_SLUG
V9 = ROOT / "art/drafts/kitchen-fixed-shell-2026-10-23-v9"
FIRST_RENDER = ROOT / "art/source/kitchen-high-resolution-foundation-2026-10-22-v1/kitchen-fitted-run-first-render-authority.png"
WARM_STATES = ROOT / "art/source/kitchen-fixed-shell-2026-10-23-v10/warm-bowl-state-reference.png"
END_DEPTH_MASTER = 80
END_DEPTH_LOGICAL = 16
GUTTER = 8

EXPECTED = {
    FIRST_RENDER: "bb37dc2e3e47c7c26649e627bae32eed04801c2e20571cbee7996d13e6e06bf2",
    WARM_STATES: "9e124727bd4e9225b80d715798324a5d2407146d87b837f92b46cce8750f6b8e",
    V9 / "assets/kitchen-fixed-shell-atlas-v9.png": "2eeaef85609eed228a0ecfa7eed30ef722d2ed070957969d3b86792c517b480f",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fitted_insert(image: Image.Image, body: list[int], name: str) -> Image.Image:
    result = v9.fitted_insert(image, body, name)
    if name != "dishwasher-broken":
        return result

    # Keep the exact approved cabinet/control/interior and exact source water,
    # but replace the fully-horizontal door with a clearly foreshortened,
    # partly-open inner face attached across its bottom hinge.
    water = Image.new("RGBA", result.size, (0, 0, 0, 0))
    src, dst = result.load(), water.load()
    for y in range(250, result.height):
        for x in range(result.width):
            r, g, b, a = src[x, y]
            if a and b > 115 and b > r * 1.18 and b >= g * 0.92:
                dst[x, y] = src[x, y]

    draw = ImageDraw.Draw(result)
    draw.rectangle((35, 276, result.width - 35, result.height - 1), fill=(0, 0, 0, 0))
    result.alpha_composite(water)
    return result


def partial_dishwasher_door(size: tuple[int, int], body: list[int]) -> Image.Image:
    """Foreground door layer: the fixed plinth must not overpaint the door."""
    result = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(result)
    bx, by, bw, _ = body
    ink = (3, 18, 28, 255)
    cream = (250, 231, 189, 255)
    cream_light = (255, 245, 218, 255)
    dark = (31, 43, 51, 255)
    dark_light = (58, 72, 80, 255)
    orange = (247, 112, 15, 255)
    orange_light = (255, 175, 66, 255)

    free_y = by + 218
    hinge_y = by + 326
    outer = [(bx + 35, free_y), (bx + bw - 35, free_y), (bx + bw - 12, hinge_y), (bx + 12, hinge_y)]
    inner = [(bx + 46, free_y + 9), (bx + bw - 46, free_y + 9), (bx + bw - 23, hinge_y - 9), (bx + 23, hinge_y - 9)]
    panel = [(bx + 59, free_y + 20), (bx + bw - 59, free_y + 20), (bx + bw - 38, hinge_y - 22), (bx + 38, hinge_y - 22)]
    draw.polygon(outer, fill=ink)
    draw.polygon(inner, fill=cream)
    draw.line(inner[:2], fill=cream_light, width=5)
    draw.polygon(panel, fill=dark, outline=ink)
    draw.line((panel[0][0] + 9, panel[0][1] + 7, panel[1][0] - 9, panel[1][1] + 7), fill=dark_light, width=4)
    handle_y = free_y + 17
    draw.rounded_rectangle((bx + 118, handle_y - 8, bx + bw - 118, handle_y + 8), radius=8, fill=ink)
    draw.rounded_rectangle((bx + 126, handle_y - 4, bx + bw - 126, handle_y + 4), radius=4, fill=orange)
    draw.line((bx + 137, handle_y - 2, bx + bw - 137, handle_y - 2), fill=orange_light, width=2)
    draw.ellipse((bx + 23, hinge_y - 17, bx + 45, hinge_y + 5), fill=ink)
    draw.ellipse((bx + bw - 45, hinge_y - 17, bx + bw - 23, hinge_y + 5), fill=ink)
    return result


def build_fixed_layers(cupboard: Image.Image, body: list[int]) -> tuple[Image.Image, Image.Image, Image.Image]:
    # V9's complete-front correction remains exact. The shallow in-bay end
    # bevel is retained only as the front boundary; real depth is now supplied
    # by a separate fixed layer outside the 504 px front run.
    return v9.build_fixed_layers(cupboard, body)


def make_end_returns() -> Image.Image:
    """Full-depth side returns entirely outside the exact six-bay front run."""
    width = v6.MASTER_RUN[0] + END_DEPTH_MASTER * 2
    height = v6.MASTER_RUN[1]
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    ink = (3, 18, 30, 255)
    blue_dark = (4, 51, 99, 255)
    blue = (5, 75, 143, 255)
    blue_light = (8, 104, 181, 255)
    cyan = (18, 185, 194, 255)
    cyan_dark = (7, 143, 171, 255)
    cyan_light = (104, 226, 222, 255)

    # Left: a worktop return, full carcass side and recessed plinth return.
    draw.polygon([(END_DEPTH_MASTER, 0), (23, 0), (0, 17), (0, 49), (END_DEPTH_MASTER, 50)], fill=ink)
    draw.polygon([(END_DEPTH_MASTER - 5, 5), (27, 5), (6, 20), (6, 39), (END_DEPTH_MASTER - 5, 43)], fill=cyan)
    draw.line((29, 9, END_DEPTH_MASTER - 7, 9), fill=cyan_light, width=4)
    draw.line((6, 40, END_DEPTH_MASTER - 5, 44), fill=cyan_dark, width=5)
    draw.polygon([(END_DEPTH_MASTER, 50), (0, 49), (0, 342), (END_DEPTH_MASTER, 338)], fill=ink)
    draw.polygon([(END_DEPTH_MASTER - 6, 58), (7, 56), (7, 330), (END_DEPTH_MASTER - 6, 328)], fill=blue)
    draw.polygon([(END_DEPTH_MASTER - 10, 65), (13, 62), (13, 320), (END_DEPTH_MASTER - 10, 318)], fill=blue_dark)
    draw.line((17, 66, END_DEPTH_MASTER - 11, 69), fill=blue_light, width=4)
    draw.polygon([(0, 338), (END_DEPTH_MASTER, 334), (END_DEPTH_MASTER, 369), (0, 359)], fill=ink)
    draw.polygon([(7, 343), (END_DEPTH_MASTER - 5, 340), (END_DEPTH_MASTER - 5, 363), (7, 353)], fill=blue_dark)

    # Right: the exact mirror, so both exposed bookends share one geometry.
    # The 80-master-pixel side returns stop exactly at the front-grid boundary;
    # the front shell owns local x=80..2599 without a one-pixel overlap.
    right = image.crop((0, 0, END_DEPTH_MASTER, height)).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    image.alpha_composite(right, (width - END_DEPTH_MASTER, 0))
    return image


def flood_isolate(source: Image.Image, box: tuple[int, int, int, int], threshold: int = 38) -> Image.Image:
    """Remove only edge-connected warm review-sheet background."""
    crop = source.crop(box).convert("RGB")
    work = crop.copy()
    marker = (255, 0, 255)
    for seed in ((0, 0), (work.width - 1, 0), (0, work.height - 1), (work.width - 1, work.height - 1)):
        ImageDraw.floodfill(work, seed, marker, thresh=threshold)
    result = crop.convert("RGBA")
    alpha = Image.new("L", crop.size, 255)
    a = alpha.load()
    pix = work.load()
    for y in range(work.height):
        for x in range(work.width):
            if pix[x, y] == marker:
                a[x, y] = 0
    # Remove tiny disconnected antialias dust after the flood.
    alpha = alpha.point(lambda value: 255 if value > 32 else 0)
    result.putalpha(alpha)
    bounds = alpha.getbbox()
    if bounds is None:
        raise RuntimeError(f"empty state crop {box}")
    return result.crop(bounds)


def first_render_broken_kettle() -> Image.Image:
    source = Image.open(FIRST_RENDER).convert("RGBA")
    crop = source.crop((1048, 145, 1237, 307))
    rgba = crop.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b, a = rgba[x, y]
            cyan = g > 92 and b > 92 and g > r * 1.18 and b > r * 1.18
            outside = x > 183 or y > 149
            if not a or cyan or outside:
                rgba[x, y] = (r, g, b, 0)
    bounds = crop.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("broken kettle extraction is empty")
    return crop.crop(bounds)


def contain(source: Image.Image, canvas: tuple[int, int], visible: tuple[int, int], bottom: int = 16) -> Image.Image:
    source = source.convert("RGBA")
    source.thumbnail(visible, Image.Resampling.LANCZOS)
    output = Image.new("RGBA", canvas, (0, 0, 0, 0))
    x = (canvas[0] - source.width) // 2
    y = canvas[1] - bottom - source.height
    output.alpha_composite(source, (x, y))
    return output


def broken_toaster(standard: Image.Image) -> Image.Image:
    """Preserve every accepted toaster pixel and add only jammed burnt toast."""
    toast = Image.new("RGBA", standard.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(toast)
    ink = (3, 18, 28, 255)
    crust = (113, 55, 23, 255)
    burnt = (38, 28, 24, 255)
    ember = (174, 78, 22, 255)
    shape = [(67, 0), (116, 0), (132, 16), (128, 66), (61, 66), (58, 17)]
    draw.polygon(shape, fill=ink)
    draw.polygon([(73, 3), (110, 2), (123, 17), (120, 58), (69, 58), (67, 18)], fill=crust)
    draw.polygon([(78, 7), (107, 6), (116, 18), (113, 51), (75, 51), (73, 20)], fill=burnt)
    draw.ellipse((84, 14, 102, 31), fill=ember)
    result = toast.copy()
    result.alpha_composite(standard)
    # Re-expose only the projecting top of the slice above the accepted slot;
    # the exact casing continues to own every pixel below it.
    projecting = toast.crop((0, 0, toast.width, 31))
    standard_top_alpha = standard.crop((0, 0, standard.width, 31)).getchannel("A")
    projecting.putalpha(ImageChops.multiply(projecting.getchannel("A"), ImageChops.invert(standard_top_alpha)))
    result.alpha_composite(projecting, (0, 0))
    return result


def record_image(atlas: Image.Image, record: dict) -> Image.Image:
    x, y, w, h = record["atlasRect"]
    return atlas.crop((x, y, x + w, y + h))


def repack(manifest: dict) -> dict:
    atlas_path = OUT / "assets" / ATLAS_NAME
    atlas = Image.open(atlas_path).convert("RGBA")
    images: dict[tuple[str, str], Image.Image] = {}
    for section in ("fixedLayers", "overlays", "assets", "looseAssets"):
        for name, record in manifest[section].items():
            images[(section, name)] = record_image(atlas, record)

    dishwasher_record = manifest["assets"]["dishwasher-broken"]
    dishwasher_image = images[("assets", "dishwasher-broken")]
    images[("overlays", "dishwasher-broken-door")] = partial_dishwasher_door(
        dishwasher_image.size, dishwasher_record["bodyRect"]
    )
    manifest["overlays"]["dishwasher-broken-door"] = {
        "bodyRect": dishwasher_record["bodyRect"],
        "logicalBody": [84, 74],
        "role": "partly-open bottom-hinged foreground door; drawn after fixed shell",
    }
    end_returns = make_end_returns()
    images[("fixedLayers", "end-perspective-returns")] = end_returns
    manifest["fixedLayers"]["end-perspective-returns"] = {
        "logicalSize": [504 + END_DEPTH_LOGICAL * 2, 74],
        "bodyOrigin": [84 - END_DEPTH_LOGICAL, 134],
        "drawOrder": "before carcass backing and inserts",
        "outsideFrontGrid": True,
    }

    standard_toaster = images[("looseAssets", "toaster")]
    images[("looseAssets", "toaster-broken")] = broken_toaster(standard_toaster)
    manifest["looseAssets"]["toaster-broken"] = {
        **{k: v for k, v in manifest["looseAssets"]["toaster"].items() if k not in {"atlasRect", "file"}},
        "label": "Toaster · Broken",
        "authority": "exact accepted V9 toaster casing plus deterministic burnt-toast insert",
        "casingChanged": False,
    }

    kettle = contain(first_render_broken_kettle(), (200, 184), (184, 164), bottom=16)
    images[("looseAssets", "kettle-broken")] = kettle
    manifest["looseAssets"]["kettle-broken"] = {
        "pixels": list(kettle.size),
        "support": "worktop",
        "label": "Kettle · Broken",
        "masterScale": 4,
        "logicalSize": [42, 38],
        "opaqueDrawRect": [4, 4, 42, 38],
        "logicalCanvas": [50, 46],
        "sourceFile": str(FIRST_RENDER.relative_to(ROOT)),
        "sourceSha256": EXPECTED[FIRST_RENDER],
        "authority": "accepted first-render broken kettle; no steam baked in",
    }

    warm = Image.open(WARM_STATES).convert("RGB")
    bowl_standard = flood_isolate(warm, (390, 280, 496, 390))
    bowl_broken = flood_isolate(warm, (1395, 280, 1512, 392))
    bowl_canvas = (232, 152)
    images[("looseAssets", "bowl")] = contain(bowl_standard, bowl_canvas, (196, 120), bottom=16)
    images[("looseAssets", "bowl-broken")] = contain(bowl_broken, bowl_canvas, (216, 120), bottom=16)
    bowl_common = {
        "pixels": list(bowl_canvas),
        "support": "table-child",
        "masterScale": 4,
        "logicalSize": [50, 30],
        "opaqueDrawRect": [4, 4, 50, 30],
        "logicalCanvas": [58, 38],
        "sourceFile": str(WARM_STATES.relative_to(ROOT)),
        "sourceSha256": EXPECTED[WARM_STATES],
        "authority": "warm dimensional state-sheet reference",
    }
    manifest["looseAssets"]["bowl"] = {**bowl_common, "label": "Mixing bowl + whisk"}
    manifest["looseAssets"]["bowl-broken"] = {**bowl_common, "label": "Mixing bowl · Broken", "whiskBesideBowl": True, "spillRetained": True}

    # Repack every requested drawing into one lossless atlas.
    ordered: list[tuple[str, str, Image.Image, dict]] = []
    for section in ("fixedLayers", "overlays", "assets", "looseAssets"):
        for name, record in manifest[section].items():
            ordered.append((section, name, images[(section, name)], record))
    width = max(image.width for _, _, image, _ in ordered) + GUTTER * 2
    height = sum(image.height + GUTTER for _, _, image, _ in ordered) + GUTTER
    packed = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    y = GUTTER
    for _, _, image, record in ordered:
        packed.alpha_composite(image, (GUTTER, y))
        record["file"] = ATLAS_NAME
        record["atlasRect"] = [GUTTER, y, image.width, image.height]
        y += image.height + GUTTER
    packed.save(atlas_path, optimize=True)
    public_atlas = PUBLIC / "assets" / ATLAS_NAME
    public_atlas.write_bytes(atlas_path.read_bytes())
    manifest["atlas"] = {
        "file": ATLAS_NAME,
        "sha256": sha256(atlas_path),
        "pixels": list(packed.size),
        "drawingCount": len(ordered),
        "uniqueImageRequests": 1,
        "lossless": True,
    }
    return manifest


def patch_page(path: Path) -> None:
    page = path.read_text()
    replacements = {
        "Kitchen Fixed Shell Layout V6": "Kitchen Fixed Shell Layout V10",
        "UNAPPROVED FIXED-SHELL V6": "UNAPPROVED FIXED-SHELL V10",
        "/keeper-review/kitchen-fixed-shell-layout-v6": "/keeper-review/kitchen-fixed-shell-layout-v10",
        "lighthouse-kitchen-fixed-shell-v6": "lighthouse-kitchen-fixed-shell-v10",
        "The approved model renders supply the visible fronts and states. One continuous worktop, one continuous plinth and one fixed six-bay carcass now own every join.":
            "V9's complete cabinet fronts remain exact. Full worktop/carcass/plinth side returns now project outside the six-bay front grid; Broken dishwasher, kettle, toaster and bowl states are visible together.",
        "Six 84 px apertures and identical shared dividers.": "Six exact 84 px front apertures; external 16 px side returns never consume bay width.",
        "drawRecord(ctx,w,84,134,504,14)": "drawRecord(ctx,w,84,134,504,10)",
    }
    for old, new in replacements.items():
        if old not in page:
            raise AssertionError(f"V10 page patch target missing: {old}")
        page = page.replace(old, new)

    page = page.replace(
        "const LOOSE=['chair','table','bin','kettle','toaster'], COUNTER=['kettle','toaster'], FLOOR=['bin','chair','table'];",
        "const LOOSE=['chair','table','bowl','bin','kettle','toaster'], COUNTER=['kettle','toaster'], FLOOR=['bin','chair','table'], CHILD=['bowl'];",
    )
    page = page.replace("chair:'Chair'};", "chair:'Chair',bowl:'Bowl + whisk'};")
    page = page.replace(
        "const DEFAULT={sink:'on',dishwasher:'on',oven:'on',fridge:'standard'};",
        "const DEFAULT={sink:'on',dishwasher:'on',oven:'on',fridge:'standard',kettle:'off',toaster:'standard',bowl:'standard'};",
    )
    page = page.replace(
        "function drawBacking(ctx){drawRecord(ctx,manifest.fixedLayers['carcass-backing'],84,134,504,74)}",
        "function drawBacking(ctx){drawRecord(ctx,manifest.fixedLayers['end-perspective-returns'],68,134,536,74);drawRecord(ctx,manifest.fixedLayers['carcass-backing'],84,134,504,74)}",
    )
    page = page.replace(
        "function drawHob(ctx){const index=order.indexOf('oven');if(index<0)return;drawRecord(ctx,manifest.overlays.hob,ORIGINS[index],134,84,14)}",
        "function drawDishwasherDoor(ctx){if(states.dishwasher!=='broken')return;const index=order.indexOf('dishwasher'),rec=manifest.overlays['dishwasher-broken-door'],b=rec.bodyRect,[,,aw,ah]=rec.atlasRect,sx=84/b[2],sy=74/b[3];drawRecord(ctx,rec,ORIGINS[index]-b[0]*sx,134-b[1]*sy,aw*sx,ah*sy)}function drawHob(ctx){const index=order.indexOf('oven');if(index<0)return;drawRecord(ctx,manifest.overlays.hob,ORIGINS[index],134,84,14)}",
    )
    page = page.replace(
        "drawFixed(ctx);drawSinkOverlay(ctx);drawHob(ctx);",
        "drawFixed(ctx);drawDishwasherDoor(ctx);drawSinkOverlay(ctx);drawHob(ctx);",
    )
    old_position = "function objectPosition(name,placement=null){const a=manifest.looseAssets[name],counter=COUNTER.includes(name),resolved=placement||(counter?owners[name]:floorSlots[name]),centre=counter?ownerCentre(resolved):slot(resolved).centreX,supportY=counter?manifest.roomGrid.fittedGrid.worktopSupportY:manifest.roomGrid.floorSlots.supportY;return[centre-(a.opaqueDrawRect[0]+a.logicalSize[0]/2),supportY-(a.opaqueDrawRect[1]+a.logicalSize[1])]}"
    new_position = "function objectPosition(name,placement=null){const a=manifest.looseAssets[visual(name)],counter=COUNTER.includes(name),child=CHILD.includes(name),resolved=placement||(counter?owners[name]:child?floorSlots.table:floorSlots[name]),centre=counter?ownerCentre(resolved):slot(resolved).centreX,supportY=counter?manifest.roomGrid.fittedGrid.worktopSupportY:child?manifest.looseGeometry.tableChildSupportY:manifest.roomGrid.floorSlots.supportY;return[centre-(a.opaqueDrawRect[0]+a.logicalSize[0]/2),supportY-(a.opaqueDrawRect[1]+a.logicalSize[1])]}"
    if old_position not in page:
        raise AssertionError("V10 objectPosition patch target missing")
    page = page.replace(old_position, new_position)
    page = page.replace(
        "function drawLoose(ctx,name,placement=null,alpha=1){const a=manifest.looseAssets[name],[x,y]=objectPosition(name,placement);drawRecord(ctx,a,x,y,a.logicalCanvas[0],a.logicalCanvas[1],alpha)}",
        "function drawLoose(ctx,name,placement=null,alpha=1){const a=manifest.looseAssets[visual(name)],[x,y]=objectPosition(name,placement);drawRecord(ctx,a,x,y,a.logicalCanvas[0],a.logicalCanvas[1],alpha)}",
    )
    page = page.replace(
        "const rec=selected.kind==='cabinet'?manifest.states[selected.name]:null;",
        "const rec=manifest.states[selected.name]||null;",
    )
    page = page.replace(
        "const [x,y]=objectPosition(name),a=manifest.looseAssets[name];",
        "const [x,y]=objectPosition(name),a=manifest.looseAssets[visual(name)];",
    )
    page = page.replace(
        "if(loose){selected={kind:'loose',name:loose};drag=COUNTER.includes(loose)?{kind:'loose',name:loose,from:owners[loose],owner:owners[loose]}:{kind:'loose',name:loose,from:floorSlots[loose],slot:floorSlots[loose]};",
        "if(loose){selected={kind:'loose',name:loose};if(CHILD.includes(loose)){message='The bowl is centred on and moves with the table.';render();return}if(isBroken(loose)){message=`${LABEL[loose]} is broken and locked until repaired.`;render();return}drag=COUNTER.includes(loose)?{kind:'loose',name:loose,from:owners[loose],owner:owners[loose]}:{kind:'loose',name:loose,from:floorSlots[loose],slot:floorSlots[loose]};",
    )
    page = page.replace(
        "if(isBroken(selected.name)){message=`${LABEL[selected.name]} is broken and locked until repaired.`;render();return}",
        "if(isBroken(selected.name)||COUNTER.some(n=>owners[n]===selected.name&&isBroken(n))){message=`${LABEL[selected.name]} or its supported appliance is broken and locked until repaired.`;render();return}",
    )
    page = page.replace(
        "buttons(document.getElementById('loose-buttons'),['toaster','kettle','bin','table','chair'],'loose');",
        "buttons(document.getElementById('loose-buttons'),['toaster','kettle','bowl','bin','table','chair'],'loose');",
    )
    page = page.replace(
        "states={sink:'broken',dishwasher:'broken',oven:'broken',fridge:'broken'};",
        "states={sink:'broken',dishwasher:'broken',oven:'broken',fridge:'broken',kettle:'broken',toaster:'broken',bowl:'broken'};",
    )
    path.write_text(page)


def main() -> None:
    for path, digest in EXPECTED.items():
        assert sha256(path) == digest, f"authority changed: {path}"

    v6.SET = SET
    v6.OUT = OUT
    v6.PUBLIC = PUBLIC
    v6.ATLAS_NAME = ATLAS_NAME
    v6.fitted_insert = fitted_insert
    v6.build_fixed_layers = build_fixed_layers
    v6.sink_overlay = v8.sink_overlay
    v6.main()

    manifest = json.loads((OUT / "manifest.json").read_text())
    manifest = repack(manifest)
    manifest["schema"] = "lighthouse-keeper/kitchen-fixed-shell-layout@10"
    manifest["status"] = "unapproved-full-end-perspective-and-broken-loose-states-review"
    manifest["architecture"].update({
        "standardCabinetTopFasciaUsed": False,
        "fullOuterEndPerspectiveReturns": True,
        "outerReturnsOutsideFrontGrid": True,
        "healingOverlay": False,
    })
    manifest["fixedLayers"]["worktop-run"]["logicalSize"] = [504, 10]
    manifest["states"].update({
        "kettle": {"off": "kettle", "on": "kettle", "broken": "kettle-broken"},
        "toaster": {"standard": "toaster", "on": "toaster", "broken": "toaster-broken"},
        "bowl": {"standard": "bowl", "broken": "bowl-broken"},
    })
    manifest["corrections"] = {
        "v9FrontsAndGridRetained": True,
        "outerEndReturnLogicalDepth": END_DEPTH_LOGICAL,
        "outerEndReturnsOutsideFrontGrid": True,
        "worktopCarcassAndPlinthPerspectiveContinuous": True,
        "dishwasherBrokenDoor": "partly open, foreshortened and attached across bottom hinge",
        "dishwasherControlsChanged": False,
        "dishwasherBrokenLights": "three fixed red lamps retained",
        "brokenKettleAuthority": "accepted first-render broken kettle; no baked steam",
        "brokenToaster": "accepted V9 casing unchanged; burnt toast added behind slot",
        "brokenBowl": "warm cracked bowl, retained spill, whisk beside bowl",
        "verticalGridChanged": False,
        "interactionCoordinatesChanged": False,
    }
    manifest["looseGeometry"].update({
        "bowlOwnership": "table-child",
        "bowlMovesWithTable": True,
        "tableChildSupportY": 155,
    })
    manifest["boundaries"].update({
        "productionChanged": False,
        "runtimeChanged": False,
        "candidateReviewOnly": True,
    })
    payload = json.dumps(manifest, indent=2) + "\n"
    (OUT / "manifest.json").write_text(payload)
    (PUBLIC / "manifest.json").write_text(payload)
    patch_page(PUBLIC / "index.html")
    print(json.dumps({"set": SET, "atlas": manifest["atlas"], "corrections": manifest["corrections"]}, indent=2))


if __name__ == "__main__":
    main()
