#!/usr/bin/env python3
"""Build the reversible Kitchen Room V7 flat-cutaway review draft.

The room is redrawn deterministically from the approved flat-cutaway contract.
Kitchen V6 furniture is read-only and the sink porthole is a separate wall child.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = ROOT / "data/kitchen_room_flat_cutaway_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
V6_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v6-option-b"
V6_DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v6-option-b"
RAW = ROOT / "art/raw/kitchen-room-flat-cutaway-2026-10-16-v7"
DRAFT = ROOT / "art/drafts/kitchen-room-flat-cutaway-2026-10-16-v7"
PUBLIC = ROOT / "public/keeper-review/kitchen-room-flat-cutaway-v7"
ASSETS = PUBLIC / "assets"

DENSITY = RECIPE["density"]
BAY = RECIPE["canvas"]["bayWidthLp"]
DOOR_DATUM = RECIPE["canvas"]["doorDatumLp"]
ROOM_H = RECIPE["canvas"]["heightLp"]
ROOM_9_W = RECIPE["canvas"]["nineBayWidthLp"]
ROOM_12_W = RECIPE["canvas"]["twelveBayWidthLp"]
TRANSPARENT = (0, 0, 0, 0)


def colour(name: str) -> tuple[int, int, int, int]:
    return tuple(RECIPE["paletteRgba"][name])


def px(lp: float) -> int:
    return round(lp * DENSITY)


def rgba(size: tuple[int, int], fill=TRANSPARENT) -> Image.Image:
    return Image.new("RGBA", size, fill)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        digest.update(path.relative_to(directory).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def box_lp(values: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = values
    return px(x0), px(y0), px(x1) - 1, px(y1) - 1


def rect_lp(draw: ImageDraw.ImageDraw, values: tuple[float, float, float, float], fill) -> None:
    draw.rectangle(box_lp(values), fill=fill)


def wall_base(width_lp: int, variant: int) -> Image.Image:
    """Opaque room field with only parallel horizontal architectural bands."""
    out = rgba((px(width_lp), px(ROOM_H)), colour("cream"))
    draw = ImageDraw.Draw(out)
    width = out.width

    # Five-lp ceiling beam. Every line is horizontal; no perspective wedge.
    draw.rectangle((0, 0, width - 1, px(5) - 1), fill=colour("ink"))
    draw.rectangle((0, px(.5), width - 1, px(4.5) - 1), fill=colour("woodDark"))
    draw.rectangle((0, px(1), width - 1, px(4) - 1), fill=colour("wood"))
    draw.rectangle((0, px(1), width - 1, px(1.5) - 1), fill=colour("woodLight"))
    draw.rectangle((0, px(4), width - 1, px(4.5) - 1), fill=colour("woodDark"))

    # Wall field and an exact 1.5-lp skirting band.
    draw.rectangle((0, px(5), width - 1, px(49.5) - 1), fill=colour("cream"))
    draw.rectangle((0, px(5), width - 1, px(6) - 1), fill=colour("creamLight"))
    draw.rectangle((0, px(49.5), width - 1, px(51) - 1), fill=colour("ink"))
    draw.rectangle((0, px(50), width - 1, px(50.5) - 1), fill=colour("woodLight"))

    # Exact five-lp floor band. All grain and board marks are horizontal.
    draw.rectangle((0, px(51), width - 1, px(56) - 1), fill=colour("wood"))
    draw.rectangle((0, px(51), width - 1, px(52) - 1), fill=colour("ink"))
    draw.rectangle((0, px(52), width - 1, px(52.5) - 1), fill=colour("woodLight"))
    draw.rectangle((0, px(54.5), width - 1, px(55) - 1), fill=colour("woodDark"))
    draw.rectangle((0, px(55.5), width - 1, px(56) - 1), fill=colour("ink"))

    # Restrained plaster and timber texture stays at least 2 lp from a repeat edge.
    texture = (
        [(4, 12, 7, 13), (11, 32, 14, 34), (5, 43, 9, 46)],
        [(6, 17, 9, 18), (13, 27, 16, 29), (10, 44, 15, 47)],
        [(3, 24, 5, 26), (9, 13, 13, 14), (14, 39, 18, 42)],
    )[variant % 3]
    for x0, y0, x1, y1 in texture:
        if x1 <= width_lp - 2:
            rect_lp(draw, (x0, y0, x1, y1), colour("creamShadow"))
            if y1 - y0 >= 2:
                rect_lp(draw, (x0 + .5, y0, x1 - .5, y0 + .5), colour("creamLight"))
    for x0, length, y in ((3, 4, 2.6), (11, 5, 3.1), (5, 6, 53.2)):
        if x0 + length <= width_lp - 2:
            rect_lp(draw, (x0, y, x0 + length, y + .35), colour("woodDark"))
    return out


def repeat_frame(variant: int) -> Image.Image:
    return wall_base(BAY, variant)


def timber_post(draw: ImageDraw.ImageDraw, x0: float, x1: float) -> None:
    rect_lp(draw, (x0, 0, x1, 56), colour("ink"))
    rect_lp(draw, (x0 + .5, .5, x1 - .5, 55.5), colour("woodDark"))
    rect_lp(draw, (x0 + 1, 1, x1 - 1, 55), colour("wood"))
    rect_lp(draw, (x0 + 1, 1, x0 + 1.5, 55), colour("woodLight"))


def stair_cap() -> Image.Image:
    out = wall_base(46, 0)
    draw = ImageDraw.Draw(out)
    timber_post(draw, 0, 4)
    timber_post(draw, 42, 46)
    # Flat ladder: true vertical rails and horizontal rungs only.
    for x0 in (8, 22):
        rect_lp(draw, (x0, 5, x0 + 2, 49), colour("ink"))
        rect_lp(draw, (x0 + .5, 5.5, x0 + 1.5, 48.5), colour("wood"))
    for centre in RECIPE["modularPieces"]["stairCap"]["ladderRungCentresFromTopLp"]:
        rect_lp(draw, (9.5, centre - .75, 22.5, centre + .75), colour("ink"))
        rect_lp(draw, (10, centre - .25, 22, centre + .25), colour("woodLight"))
    return out


def far_cap(opening: bool = False) -> Image.Image:
    out = wall_base(38, 2)
    draw = ImageDraw.Draw(out)
    timber_post(draw, 34, 38)
    if opening:
        rect_lp(draw, (34, 5, 38, 51), colour("ink"))
        rect_lp(draw, (34, 5, 34.5, 51), colour("woodLight"))
    return out


def porthole() -> Image.Image:
    spec = RECIPE["sinkPorthole"]
    out = rgba((px(spec["cellLp"][0]), px(spec["cellLp"][1])))
    draw = ImageDraw.Draw(out)
    cx, cy = px(spec["centreLpFromCellTop"][0]), px(spec["centreLpFromCellTop"][1])
    outer = px(spec["outerDiameterLp"])
    ox0, oy0 = cx - outer // 2, cy - outer // 2
    ox1, oy1 = ox0 + outer - 1, oy0 + outer - 1

    draw.ellipse((ox0, oy0, ox1, oy1), fill=colour("ink"))
    draw.ellipse((ox0 + 2, oy0 + 2, ox1 - 2, oy1 - 2), fill=colour("brassDark"))
    draw.ellipse((ox0 + 4, oy0 + 4, ox1 - 4, oy1 - 4), fill=colour("brass"))
    draw.arc((ox0 + 5, oy0 + 5, ox1 - 5, oy1 - 5), 205, 335, fill=colour("brassLight"), width=2)

    glass = px(spec["glazingDiameterLp"])
    gx0, gy0 = cx - glass // 2, cy - glass // 2
    gx1, gy1 = gx0 + glass - 1, gy0 + glass - 1
    view = rgba(out.size)
    vd = ImageDraw.Draw(view)
    vd.rectangle((gx0, gy0, gx1, gy1), fill=colour("glassLight"))
    vd.rectangle((gx0, cy, gx1, gy1), fill=colour("glass"))
    vd.rectangle((gx0, cy + px(3), gx1, gy1), fill=colour("glassDeep"))
    # Simple lighthouse-island horizon detail, clipped to the glazing circle.
    vd.polygon([(cx - px(3), cy + px(3)), (cx, cy + px(.5)), (cx + px(3), cy + px(3))], fill=colour("woodDark"))
    vd.rectangle((cx - px(.4), cy - px(1.7), cx + px(.4), cy + px(1)), fill=colour("creamLight"))
    vd.rectangle((cx - px(1.2), cy - px(2.1), cx + px(1.2), cy - px(1.6)), fill=colour("brassDark"))
    vd.ellipse((gx0 + px(1), gy0 + px(1.5), gx0 + px(5), gy0 + px(3.5)), fill=colour("creamLight"))
    mask = Image.new("L", out.size, 0)
    ImageDraw.Draw(mask).ellipse((gx0, gy0, gx1, gy1), fill=255)
    view.putalpha(mask)
    out.alpha_composite(view)
    draw = ImageDraw.Draw(out)
    draw.ellipse((gx0 - 2, gy0 - 2, gx1 + 2, gy1 + 2), outline=colour("ink"), width=2)
    draw.arc((gx0 + 2, gy0 + 2, gx1 - 2, gy1 - 2), 200, 310, fill=colour("creamLight"), width=2)

    offsets = [(0, -24), (17, -17), (24, 0), (17, 17), (0, 24), (-17, 17), (-24, 0), (-17, -17)]
    for dx, dy in offsets:
        bx, by = cx + dx, cy + dy
        draw.ellipse((bx - 2, by - 2, bx + 1, by + 1), fill=colour("ink"))
        draw.ellipse((bx - 1, by - 1, bx, by), fill=colour("brassLight"))
    return out


REPEATS = [repeat_frame(index) for index in range(3)]
STAIR = stair_cap()
FAR_CLOSED = far_cap(False)
FAR_OPEN = far_cap(True)
PORTHOLE = porthole()


def room_shell(bays: int, open_far: bool = False) -> Image.Image:
    width_lp = DOOR_DATUM + BAY * bays
    out = rgba((px(width_lp), px(ROOM_H)))
    crop = RECIPE["modularPieces"]["stairCap"]["assemblyCropLp"]
    out.alpha_composite(STAIR.crop(tuple(px(value) for value in crop)), (0, 0))
    for index in range(bays):
        out.alpha_composite(REPEATS[index % len(REPEATS)], (px(DOOR_DATUM + index * BAY), 0))
    cap = FAR_OPEN if open_far else FAR_CLOSED
    out.alpha_composite(cap, (out.width - cap.width, 0))
    return out


def load_v6(name: str) -> Image.Image:
    return Image.open(V6_RAW / name).convert("RGBA")


def v6_standard(stem: str) -> Image.Image:
    return load_v6(f"{stem}_standard_f1.png")


def place_one_bay(out: Image.Image, image: Image.Image, bay: int) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY) + (px(BAY) - image.width) // 2
    out.alpha_composite(image, (x, out.height - image.height))


def place_child(out: Image.Image, child: Image.Image, bay: int) -> None:
    x = px(DOOR_DATUM + (bay - 1) * BAY) + (px(BAY) - child.width) // 2
    out.alpha_composite(child, (x, 0))


def room_composite(bays: int = 9) -> Image.Image:
    out = room_shell(bays)
    positions = {"obj_bin": 1, "obj_fridge": 2, "obj_kettle": 3, "obj_toaster": 4, "obj_cooker": 5, "obj_mixer": 6}
    for stem, bay in positions.items():
        place_one_bay(out, v6_standard(stem), bay)
    place_child(out, PORTHOLE, 7)
    place_one_bay(out, v6_standard("obj_sink"), 7)
    table = v6_standard("obj_table")
    x = px(DOOR_DATUM + 7 * BAY) + (px(2 * BAY) - table.width) // 2
    out.alpha_composite(table, (x, out.height - table.height))
    bowl = v6_standard("obj_petbowl")
    out.alpha_composite(bowl, (px(172), out.height - bowl.height))
    return out


def sink_move_proof(bay: int) -> Image.Image:
    out = room_shell(9)
    place_child(out, PORTHOLE, bay)
    place_one_bay(out, v6_standard("obj_sink"), bay)
    return out


def outline_12() -> Image.Image:
    out = room_shell(12)
    place_child(out, PORTHOLE, 9)
    draw = ImageDraw.Draw(out)
    for index in range(13):
        x = px(DOOR_DATUM + index * BAY)
        for y in range(px(6), px(51), 8):
            draw.line((x, y, x, min(y + 3, px(51) - 1)), fill=(88, 212, 223, 190), width=1)
    reservations = [(1, 1, 15), (2, 2, 46), (4, 1, 31), (5, 1, 31), (6, 2, 31), (8, 1, 31), (9, 2, 31), (11, 1, 28), (12, 1, 50)]
    for bay, span, height in reservations:
        x0 = px(DOOR_DATUM + (bay - 1) * BAY + .5)
        x1 = px(DOOR_DATUM + (bay - 1 + span) * BAY - .5) - 1
        y0 = px(ROOM_H - height)
        y1 = px(ROOM_H) - 1
        for x in range(x0, x1 + 1, 8):
            draw.line((x, y0, min(x + 3, x1), y0), fill=(239, 182, 77, 220), width=1)
        draw.line((x0, y0, x0, y1), fill=(239, 182, 77, 220), width=1)
        draw.line((x1, y0, x1, y1), fill=(239, 182, 77, 220), width=1)
    return out


def alpha_bound(image: Image.Image) -> dict | None:
    box = image.getchannel("A").getbbox()
    if not box:
        return None
    x0, y0, x1, y1 = box
    return {"xLp": x0 / DENSITY, "yLp": y0 / DENSITY, "widthLp": (x1 - x0) / DENSITY, "heightLp": (y1 - y0) / DENSITY}


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=False, compress_level=9)


def save_asset(name: str, image: Image.Image, cell_lp: tuple[int, int], extra: dict) -> dict:
    png_path = RAW / f"{name}.png"
    json_path = RAW / f"{name}.json"
    save_png(image, png_path)
    metadata = {
        "w": cell_lp[0], "h": cell_lp[1], "frames": 1, "fps": 0, "density": DENSITY,
        "anchor": [cell_lp[0] / 2, cell_lp[1]],
        "projection": {"id": "flat-cutaway-v1", "runtimeDepthScaling": False},
        "alphaBoundLp": alpha_bound(image), **extra,
    }
    json_path.write_text(json.dumps(metadata, indent=2) + "\n")
    review_name = f"{name}_frame1.png"
    save_png(image, ASSETS / review_name)
    return {
        "png": png_path.relative_to(ROOT).as_posix(),
        "json": json_path.relative_to(ROOT).as_posix(),
        "sha256": sha(png_path),
        "meta": metadata,
        "url": f"/keeper-review/kitchen-room-flat-cutaway-v7/assets/{review_name}",
    }


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen Room V7 · flat-cutaway review</title><style>
:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--muted:#a8bdc4;--gold:#efb64d;--cyan:#58d4df;--red:#ff786d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1520px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:12px;min-width:0}.scroll{overflow:auto;background:#071923;border-radius:10px;padding:10px}.scroll img{display:block;height:224px;width:auto}.small{font-size:.84rem;color:var(--muted)}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0}button,select,input{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled,input:disabled{opacity:.45}.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}.well{min-height:230px;display:flex;align-items:center;justify-content:center;overflow:auto;background:repeating-conic-gradient(#172c36 0 25%,#10232d 0 50%) 0/18px 18px;border-radius:8px}.well img{height:224px;width:auto}.guide{position:relative;display:inline-block}.guide:after{content:"parallel structural guides";position:absolute;left:0;right:0;top:20px;bottom:20px;border-top:2px solid var(--cyan);border-bottom:2px solid var(--gold);border-left:2px solid var(--cyan);border-right:2px solid var(--cyan);pointer-events:none;color:#06131c;background:linear-gradient(var(--cyan),var(--cyan)) no-repeat 8px 8px/150px 22px;padding:8px 12px;font-size:.75rem}.recipe{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}.metric{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:10px}.metric strong{display:block;color:var(--gold);font-size:1.15rem}code{color:#9ce5ea;word-break:break-all}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:7px;border-bottom:1px solid var(--line);vertical-align:top}@media(max-width:720px){header,main{padding:12px}.pair{grid-template-columns:1fr}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">Room redraw</span><span class="tag">V6 furniture unchanged</span><h1>Kitchen Room V7 · flat-cutaway shell</h1><p>The kitchen architecture now uses the same straight-on, zero-convergence construction as the selected Option B furniture. The porthole is owned by the sink and moves with it.</p><p id="loading" class="notice">Preloading and decoding every unique review image… controls remain locked.</p></header><main>
<section class="panel"><h2>Locked room recipe</h2><div class="recipe"><div class="metric"><strong>56 lp</strong>exact room height</div><div class="metric"><strong>4 + 21n lp</strong>whole-bay width formula</div><div class="metric"><strong>5 lp</strong>horizontal floor band</div><div class="metric"><strong>0 lp</strong>horizontal/vertical convergence</div><div class="metric"><strong>15 lp</strong>sink-owned porthole diameter</div><div class="metric"><strong>37.5 lp</strong>porthole centre above floor</div></div><p class="notice"><strong>Approval boundary:</strong> room and porthole review only. Kitchen V6 furniture, Keeper art, runtime sprites, Final and manifests remain unchanged.</p></section>
<section class="panel"><h2>Previous shell beside room redraw</h2><div class="pair"><div class="card"><h3>Kitchen V6 room shell</h3><div class="scroll"><img id="oldShell"></div></div><div class="card"><h3>V7 flat-cutaway room shell</h3><div class="scroll"><span class="guide"><img id="newShell"></span></div></div></div><p>V7 removes the residual diagonal floor joints and rebuilds the ceiling beam, wall, skirting and floor as parallel constant-width bands. No object or Keeper scale changes.</p></section>
<section class="panel"><h2>Modular pieces</h2><div class="grid"><div class="card"><h3>46 × 56-lp stair cap</h3><div class="scroll"><img id="stair"></div><p class="small">Only the rightmost 4 lp contributes to assembled kitchen width.</p></div><div class="card"><h3>21 × 56-lp repeat</h3><div class="scroll"><img id="repeat"></div><p class="small">Three texture variants; identical structural edge columns.</p></div><div class="card"><h3>38 × 56-lp far cap</h3><div class="scroll"><img id="far"></div><p class="small">Right-aligned overlay; contributes 0 lp. The closed cupboard leaf is not visible.</p></div></div></section>
<section class="panel"><h2>Exact shell assembly · 6–12 bays</h2><div class="controls"><label>Bays <select id="shellSelect" disabled></select></label></div><div class="scroll"><img id="shell"></div><p>Every selection is assembled from whole modules; no module is stretched and the far wall remains last.</p></section>
<section class="panel"><h2>Sink-owned porthole</h2><div class="grid"><div class="card"><h3>Separate wall child</h3><div class="well"><img id="porthole"></div><p class="small">21 × 56-lp transparent cell · 15-lp ring · 3-lp side gutters · z 25.</p></div><div class="card"><h3>Unchanged V6 sink</h3><div class="well"><img id="sink"></div><p class="small">The sink remains z 40 with the same 19-lp worktop datum and exact V6 pixels.</p></div><div class="card"><h3>Attached pair</h3><div class="well"><img id="attached"></div><p class="small">One bay anchor; the child translates exactly with its parent.</p></div></div></section>
<section class="panel"><h2>Move the sink · window follows</h2><div class="controls"><label>Sink bay <select id="moveSelect" disabled><option value="2">2</option><option value="5">5</option><option value="8">8</option></select></label></div><div class="scroll"><img id="moveProof"></div><p>The same sink bytes and the same porthole bytes are reused at all three positions. Child delta equals parent delta; neither changes scale or shape.</p></section>
<section class="panel"><h2>9-bay starting kitchen · 193 × 56 lp</h2><div class="scroll"><img id="room9"></div><p>The porthole is centred over the bay-7 sink and is not baked into the room repeat.</p></section>
<section class="panel"><h2>12-bay reservation · 256 × 56 lp</h2><div class="scroll"><img id="room12"></div><p>Dashed envelopes remain whole-bay reservations. The porthole is shown with the reserved sink bay and moves if that sink moves.</p></section>
<section class="panel"><h2>Far-wall cupboard relationship</h2><div class="pair"><div class="card"><h3>Closed</h3><div class="well"><img id="farClosed"></div><p class="small">No false frontal door is visible.</p></div><div class="card"><h3>Open foreground leaf</h3><div class="well"><img id="farDoor"></div><p class="small">Exact V6 rectangular leaf remains the real Keeper occluder; hinge x stays fixed.</p></div></div></section>
<section class="panel"><h2>Measured files and hashes</h2><table><thead><tr><th>Asset</th><th>Cell</th><th>Contribution / ownership</th><th>SHA-256</th></tr></thead><tbody id="rows"></tbody></table></section>
</main><script>
const DATA=__DATA__,all=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))all.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const urls=[...new Set(all)];
function setup(){document.querySelectorAll('select').forEach(x=>x.disabled=false);oldShell.src=DATA.oldShell;newShell.src=DATA.shells['9'];stair.src=DATA.pieces.stair.url;repeat.src=DATA.pieces.repeatA.url;far.src=DATA.pieces.farClosed.url;porthole.src=DATA.pieces.porthole.url;sink.src=DATA.sink;attached.src=DATA.attached;room9.src=DATA.room9;room12.src=DATA.room12;farClosed.src=DATA.pieces.farClosed.url;farDoor.src=DATA.farDoor;for(let n=6;n<=12;n++)shellSelect.add(new Option(`${n} bays · ${4+21*n} lp`,n));shellSelect.value='9';const showShell=()=>shell.src=DATA.shells[shellSelect.value];shellSelect.onchange=showShell;showShell();const showMove=()=>moveProof.src=DATA.moves[moveSelect.value];moveSelect.onchange=showMove;moveSelect.value='5';showMove();for(const r of DATA.rows){const tr=document.createElement('tr');tr.innerHTML=`<td>${r.name}</td><td>${r.cell}</td><td>${r.role}</td><td><code>${r.sha256}</code></td>`;rows.append(tr)}loading.textContent=`All ${urls.length} unique review images loaded and decoded. Controls enabled.`}
document.querySelectorAll('select').forEach(x=>x.disabled=true);Promise.all(urls.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed to load: ${e.message}`);
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


def main() -> None:
    for folder in (RAW, DRAFT, PUBLIC, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    for folder in (RAW, DRAFT, ASSETS):
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()

    records: dict[str, dict] = {}
    records["stair"] = save_asset("room_kitchen_stair_cap", STAIR, (46, 56), {"z": 15, "moduleContributionLp": 4, "assemblyCropLp": [42, 0, 46, 56]})
    for index, repeat in enumerate(REPEATS):
        records[f"repeat{'ABC'[index]}"] = save_asset(f"room_kitchen_repeat_{'abc'[index]}", repeat, (21, 56), {"z": 10, "moduleContributionLp": 21, "variant": index + 1})
    records["farClosed"] = save_asset("room_kitchen_far_cap_closed", FAR_CLOSED, (38, 56), {"z": 20, "moduleContributionLp": 0, "doorView": "right-side-wall-closed-invisible"})
    records["farOpen"] = save_asset("room_kitchen_far_cap_open", FAR_OPEN, (38, 56), {"z": 20, "moduleContributionLp": 0, "doorView": "right-side-wall-opening"})
    records["porthole"] = save_asset("obj_sink_porthole_standard_f1", PORTHOLE, (21, 56), {**RECIPE["sinkPorthole"]})

    shells = {}
    for bays in RECIPE["canvas"]["supportedBayCounts"]:
        rec = save_asset(f"room_kitchen_shell_{bays}bay", room_shell(bays), (DOOR_DATUM + BAY * bays, 56), {"z": 10, "bayCount": bays, "floorBandLp": 5})
        shells[str(bays)] = rec["url"]

    moves = {}
    placements = {}
    for bay in (2, 5, 8):
        rec = save_asset(f"sink_porthole_move_bay_{bay}", sink_move_proof(bay), (193, 56), {"reviewComposite": True, "sinkBay": bay, "childBay": bay})
        moves[str(bay)] = rec["url"]
        placements[str(bay)] = {"sinkXLp": DOOR_DATUM + (bay - 1) * BAY, "portholeXLp": DOOR_DATUM + (bay - 1) * BAY}

    room9 = save_asset("room_kitchen_9bay_composite", room_composite(), (193, 56), {"reviewComposite": True, "sinkBay": 7, "portholeBay": 7})
    room12 = save_asset("room_kitchen_12bay_outline", outline_12(), (256, 56), {"reviewComposite": True, "sinkReservationBay": 9, "portholeBay": 9})

    attached = rgba((px(21), px(56)))
    attached.alpha_composite(PORTHOLE)
    attached.alpha_composite(v6_standard("obj_sink"), (0, attached.height - v6_standard("obj_sink").height))
    attached_rec = save_asset("obj_sink_with_porthole_review", attached, (21, 56), {"reviewComposite": True, "parent": "obj_sink", "child": "obj_sink_porthole"})

    far_door = FAR_OPEN.copy()
    far_door.alpha_composite(load_v6("obj_cupboard_open_f1.png"))
    far_door_rec = save_asset("room_kitchen_far_cap_open_with_v6_door", far_door, (38, 56), {"reviewComposite": True, "doorPixels": "exact-kitchen-v6"})

    old_data = read_json(V6_DRAFT / "review-data.json")
    data = {
        "recipe": RECIPE,
        "oldShell": old_data["shells"]["9"],
        "shells": shells,
        "pieces": records,
        "sink": old_data["assets"]["obj_sink"]["states"]["standard"]["v6Urls"][0],
        "attached": attached_rec["url"],
        "moves": moves,
        "room9": room9["url"],
        "room12": room12["url"],
        "farDoor": far_door_rec["url"],
        "rows": [
            {"name": "stair-side cap", "cell": "46 × 56 lp", "role": "4-lp assembly crop", "sha256": records["stair"]["sha256"]},
            {"name": "repeat A", "cell": "21 × 56 lp", "role": "one whole bay", "sha256": records["repeatA"]["sha256"]},
            {"name": "far cap closed", "cell": "38 × 56 lp", "role": "0-lp right overlay", "sha256": records["farClosed"]["sha256"]},
            {"name": "sink porthole", "cell": "21 × 56 lp", "role": "sink-owned wall child", "sha256": records["porthole"]["sha256"]},
        ],
    }
    (DRAFT / "room-catalogue.json").write_text(json.dumps({
        "version": 7,
        "status": "reversible-draft",
        "recipe": RECIPE["id"],
        "projection": RECIPE["projection"],
        "room": RECIPE["canvas"],
        "pieces": records,
        "shells": shells,
        "sinkPorthole": records["porthole"],
        "movementPlacementsLp": placements,
        "composites": {"room9": room9, "room12": room12, "attached": attached_rec, "farDoor": far_door_rec},
    }, indent=2) + "\n")
    (DRAFT / "review-data.json").write_text(json.dumps(data, indent=2) + "\n")
    write_page(data)

    outputs = sorted(path for path in RAW.iterdir() if path.is_file()) + sorted(DRAFT.glob("*.json")) + [PUBLIC / "index.html"]
    register = {
        "version": 7,
        "status": "reversible-draft",
        "scope": "kitchen-room-and-sink-porthole-only",
        "visualBaseline": "Kitchen V6 Option B furniture plus approved flat room direction",
        "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)},
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
        "v6FurnitureChanged": False,
        "protectedSnapshots": {
            "kitchenV6": tree_sha(V6_RAW),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
        "outputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in outputs],
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"set": "kitchen-room-flat-cutaway-v7", "shells": len(shells), "portholeDiameterLp": 15, "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
