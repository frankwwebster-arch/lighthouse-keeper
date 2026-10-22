#!/usr/bin/env python3
"""Build immutable high-resolution Ligne-Claire kettle states from V45."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-kettle-ligne-claire-v1"
DATED = "kitchen-kettle-ligne-claire-2026-10-22-v1"
PACK = ROOT / "art" / "drafts" / DATED
SOURCE = ROOT / "art" / "raw" / "kitchen-kettle-standalone-2026-10-21-v45"
CONTRACT = ROOT / "art" / "drafts" / "kitchen-kettle-standalone-2026-10-21-v45" / "candidate-catalogue.json"
PUBLIC = ROOT / "public" / "keeper-review" / SET

INK = (5, 24, 36)
INK_2 = (10, 34, 43)
CREAM = (250, 244, 224)
CREAM_DARK = (246, 229, 183)
SEA = (83, 177, 181)
SEA_DARK = (45, 119, 157)
BLUE = (35, 91, 133)
BLUE_DARK = (29, 69, 98)
COPPER = (211, 111, 45)
COPPER_DARK = (144, 82, 49)
METAL = (174, 187, 185)
CHARCOAL = (92, 108, 111)
PALETTE = (INK, INK_2, CREAM, CREAM_DARK, SEA, SEA_DARK, BLUE, BLUE_DARK, COPPER, COPPER_DARK, METAL, CHARCOAL)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def line(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], colour: tuple[int, int, int], width: int) -> None:
    draw.line(points, fill=colour, width=width, joint="curve")


def polygon(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], fill: tuple[int, int, int], width: int) -> None:
    draw.polygon(points, fill=fill)
    draw.line(points + [points[0]], fill=INK, width=width, joint="curve")


def rounded(draw: ImageDraw.ImageDraw, bounds: tuple[int, int, int, int], radius: int, fill: tuple[int, int, int], width: int) -> None:
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=INK, width=width)


def ellipse(draw: ImageDraw.ImageDraw, bounds: tuple[int, int, int, int], fill: tuple[int, int, int], width: int) -> None:
    draw.ellipse(bounds, fill=fill, outline=INK, width=width)


def intact_master() -> Image.Image:
    image = Image.new("RGBA", (652, 604), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    w = 9

    # Main enamel vessel and its single flat lower shadow plane.
    ellipse(draw, (43, 214, 548, 610), CREAM, w)
    polygon(draw, [(455, 280), (542, 220), (608, 269), (547, 383), (495, 414), (470, 359)], CREAM, w)
    ellipse(draw, (532, 209, 615, 323), COPPER, w)
    ellipse(draw, (557, 237, 601, 292), METAL, w)
    ellipse(draw, (570, 247, 593, 281), INK, w)

    rounded(draw, (33, 477, 556, 570), 33, SEA, w)
    polygon(draw, [(460, 495), (543, 487), (543, 548), (461, 557)], SEA_DARK, w)

    # Lid and knob are closed, centred and keep the exact V45 hierarchy.
    ellipse(draw, (148, 190, 438, 282), SEA, w)
    ellipse(draw, (249, 151, 339, 222), COPPER, w)
    rounded(draw, (277, 197, 316, 229), 8, COPPER_DARK, w)

    # Handle: blue grip and two copper mounts, drawn as actual thick parts.
    line(draw, [(116, 275), (91, 218), (100, 137), (151, 89)], INK, 51)
    line(draw, [(116, 275), (91, 218), (100, 137), (151, 89)], COPPER, 31)
    line(draw, [(457, 273), (482, 210), (480, 139), (440, 91)], INK, 51)
    line(draw, [(457, 273), (482, 210), (480, 139), (440, 91)], COPPER, 31)
    rounded(draw, (145, 39, 451, 139), 38, BLUE, w)
    ellipse(draw, (86, 230, 145, 307), COPPER, w)
    ellipse(draw, (430, 229, 488, 307), COPPER, w)
    return image


def rotated_lid() -> Image.Image:
    layer = Image.new("RGBA", (460, 270), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    ellipse(draw, (30, 90, 420, 225), SEA, 14)
    ellipse(draw, (190, 25, 300, 110), COPPER, 14)
    rounded(draw, (225, 85, 270, 125), 9, COPPER_DARK, 14)
    return layer.rotate(16, resample=Image.Resampling.BICUBIC, expand=False)


def broken_master() -> Image.Image:
    image = Image.new("RGBA", (1040, 992), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    w = 14

    ellipse(draw, (48, 350, 875, 1020), CREAM, w)
    ellipse(draw, (194, 381, 689, 503), INK, w)
    polygon(draw, [(730, 445), (873, 347), (1000, 438), (895, 635), (802, 688), (749, 604)], CREAM, w)
    ellipse(draw, (873, 350, 1006, 514), COPPER, w)
    ellipse(draw, (918, 386, 984, 472), METAL, w)
    ellipse(draw, (938, 407, 976, 458), INK, w)
    rounded(draw, (33, 801, 879, 957), 55, SEA, w)
    polygon(draw, [(707, 829), (858, 814), (858, 910), (707, 941)], SEA_DARK, w)

    # Open lid retains its hinge, angle and displaced knob.
    image.alpha_composite(rotated_lid(), (183, 161))
    draw = ImageDraw.Draw(image)

    # Torn left mount, twisted right arm and sloping blue grip.
    line(draw, [(187, 408), (152, 340), (181, 229), (270, 143)], INK, 78)
    line(draw, [(187, 408), (152, 340), (181, 229), (270, 143)], COPPER, 48)
    polygon(draw, [(160, 373), (190, 350), (211, 389), (187, 433), (163, 422)], CREAM_DARK, w)
    line(draw, [(715, 460), (755, 375), (743, 303), (690, 258)], INK, 78)
    line(draw, [(715, 460), (755, 375), (743, 303), (690, 258)], COPPER, 48)
    line(draw, [(306, 99), (700, 282)], INK, 154)
    line(draw, [(306, 99), (700, 282)], BLUE, 120)
    ellipse(draw, (104, 355, 190, 477), COPPER, w)
    ellipse(draw, (678, 394, 774, 517), COPPER, w)

    # Crushed left panel uses one flat shadow tone, not modelling.
    polygon(draw, [(99, 626), (160, 591), (233, 625), (288, 688), (226, 737), (153, 708)], CREAM_DARK, w)
    line(draw, [(107, 628), (196, 666), (272, 707)], INK, w)

    # Large jagged rupture, surrounding fragments and decisive fracture lines.
    hole = [(646, 690), (689, 655), (739, 672), (774, 716), (822, 724), (844, 777), (807, 840), (748, 825), (708, 787), (660, 778)]
    polygon(draw, hole, CHARCOAL, w)
    polygon(draw, [(629, 683), (663, 647), (689, 655), (670, 704)], CREAM_DARK, w)
    polygon(draw, [(774, 716), (817, 704), (842, 741), (822, 778)], CREAM_DARK, w)
    polygon(draw, [(709, 787), (748, 825), (719, 857), (685, 815)], CREAM_DARK, w)
    for crack in (
        [(657, 685), (618, 657), (590, 661)],
        [(661, 704), (617, 720), (588, 750)],
        [(689, 655), (678, 616), (660, 592)],
        [(822, 778), (858, 786), (884, 809)],
        [(710, 815), (696, 852), (700, 885)],
    ):
        line(draw, crack, INK, w)
    return image


def register(master: Image.Image, source: Image.Image) -> Image.Image:
    if master.size != source.size:
        raise RuntimeError("master/source canvas mismatch")
    pixels = []
    for candidate, original in zip(master.getdata(), source.getdata()):
        if original[3] and candidate[3] < 8:
            colour = min(PALETTE, key=lambda value: sum((value[i] - original[i]) ** 2 for i in range(3)))
            pixels.append((*colour, candidate[3]))
        else:
            pixels.append(candidate)
    master.putdata(pixels)
    master.putalpha(source.getchannel("A"))
    return master


def checker(size: tuple[int, int], cell: int = 18) -> Image.Image:
    out = Image.new("RGBA", size, (246, 240, 220, 255)); draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable kettle V1")
    for path in (PACK / "masters", PACK / "candidates", PACK / "effects", PACK / "evidence", PUBLIC / "assets"):
        path.mkdir(parents=True)
    records = []
    shared = intact_master()
    for filename in ("kettle-off.png", "kettle-on.png", "kettle-broken.png"):
        source_path = SOURCE / filename
        source = Image.open(source_path).convert("RGBA")
        master = shared.copy() if filename != "kettle-broken.png" else broken_master()
        candidate = register(master.copy(), source)
        master_path = PACK / "masters" / filename.replace(".png", "-master.png")
        candidate_path = PACK / "candidates" / filename
        master.save(master_path, optimize=True); candidate.save(candidate_path, optimize=True)
        records.append({"filename": filename, "sourceFile": source_path.relative_to(ROOT).as_posix(), "sourceSha256": sha256(source_path), "sourcePixels": list(source.size), "sourceAlphaBounds": list(source.getchannel("A").getbbox()), "sourceAlphaSha256": alpha_sha(source), "masterFile": master_path.relative_to(ROOT).as_posix(), "masterSha256": sha256(master_path), "candidateFile": candidate_path.relative_to(ROOT).as_posix(), "candidateSha256": sha256(candidate_path), "candidatePixels": list(candidate.size), "candidateAlphaBounds": list(candidate.getchannel("A").getbbox()), "candidateAlphaSha256": alpha_sha(candidate)})
    effect_records = []
    for state in ("on", "broken"):
        for model in ("compact", "regular", "emphatic"):
            filename = f"fx-kettle-{state}-steam--{model}-f40.png"
            target = PACK / "effects" / filename
            shutil.copy2(SOURCE / filename, target)
            effect_records.append({"filename": filename, "sourceFile": (SOURCE / filename).relative_to(ROOT).as_posix(), "sourceSha256": sha256(SOURCE / filename), "preservedFile": target.relative_to(ROOT).as_posix(), "preservedSha256": sha256(target), "frames": 40, "fps": 4, "byteExact": True})

    font = ImageFont.load_default(); sheet = Image.new("RGBA", (1500, 1110), (250, 244, 224, 255)); draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), "Kettle V45 authority / Ligne-Claire V1 / alpha ghost / exact logical size", fill=INK, font=font)
    for row, record in enumerate(records):
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA"); candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        y = 48 + row * 350
        scale = min(300 / source.width, 300 / source.height)
        shown_size = (round(source.width * scale), round(source.height * scale))
        for col, item in enumerate((source, candidate)):
            panel = checker((440, 310)); shown = item.resize(shown_size, Image.Resampling.LANCZOS); panel.alpha_composite(shown, ((440-shown.width)//2,(310-shown.height)//2)); sheet.alpha_composite(panel, (10+col*450,y))
        ghost = checker((440, 310)); shown = candidate.resize(shown_size, Image.Resampling.LANCZOS); ghost.alpha_composite(shown, ((440-shown.width)//2,(310-shown.height)//2)); tint=Image.new("RGBA",source.size,(232,72,86,0)); tint.putalpha(source.getchannel("A").point(lambda v:round(v*.34))); tint=tint.resize(shown_size,Image.Resampling.LANCZOS); ghost.alpha_composite(tint,((440-shown.width)//2,(310-shown.height)//2)); sheet.alpha_composite(ghost,(910,y))
        logical = (62,59) if record["filename"] == "kettle-broken.png" else (56,51); sheet.alpha_composite(candidate.resize(logical,Image.Resampling.LANCZOS),(1380,y+20))
        draw.text((18,y+316),f"CURRENT {record['filename']} · {source.size}",fill=INK,font=font); draw.text((468,y+316),"V1 CANDIDATE",fill=INK,font=font); draw.text((928,y+316),f"GHOST · logical {logical[0]}x{logical[1]}",fill=INK,font=font)
    evidence = PACK / "evidence" / "kettle-current-candidate-ghost-logical.png"; sheet.save(evidence,optimize=True)

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    manifest = {"schema":"lighthouse-keeper/kitchen-kettle-ligne-claire@1","set":SET,"created":"2026-10-22","status":"immutable-review-candidate-not-approved-not-registered","sourceSet":"kitchen-kettle-standalone-v45","contractFile":CONTRACT.relative_to(ROOT).as_posix(),"contractSha256":sha256(CONTRACT),"objects":records,"effects":effect_records,"preservedBehaviour":{"logicalFootprints":contract["geometry"]["logicalFootprintPixels"],"stateRender":contract["geometry"]["stateRender"],"supportSurfaceSlots":contract["geometry"]["supportSurfaceSlots"],"supportPlaneY":contract["geometry"]["supportPlaneY"],"brokenBodyAnimation":contract["states"]["broken"]["bodyAnimation"],"brokenAssetLock":contract["brokenAssetLock"],"countertopOccupancy":contract["countertopOccupancy"],"teaInteraction":contract["teaInteraction"]},"unchanged":["canvas","alpha","transparent gutter","logical render size","support contact","support slots","bottom-centre pivot","broken body keyframes","steam frames","steam timing","asset-local effects","tea interaction","movement locks","repair transitions"],"registration":{"register":False,"promote":False,"currentSelectorChanges":[],"approvalRequired":True},"evidence":{"file":evidence.relative_to(ROOT).as_posix(),"sha256":sha256(evidence)},"rollback":"Discard only this V1 pack and review route."}
    (PACK/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8"); (PACK/"batch-register.json").write_text(json.dumps({"status":"blocked-pending-explicit-frank-approval","register":False,"promote":False,"currentSelectorChanges":[]},indent=2)+"\n",encoding="utf-8")
    for record in records:
        shutil.copy2(ROOT/record["sourceFile"],PUBLIC/"assets"/("current--"+record["filename"])); shutil.copy2(ROOT/record["candidateFile"],PUBLIC/"assets"/("candidate--"+record["filename"]))
    for effect in effect_records: shutil.copy2(ROOT/effect["preservedFile"],PUBLIC/"assets"/effect["filename"])
    shutil.copy2(evidence,PUBLIC/"assets"/evidence.name)
    html=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kettle Ligne-Claire V1</title><style>body{{margin:0;background:#f6e5b7;color:#051824;font:16px/1.45 system-ui}}header,main{{max-width:1520px;margin:auto;padding:22px}}header{{border-bottom:4px solid #051824}}.status{{border:2px solid #051824;background:#e7a638;padding:6px 10px;font-weight:800}}article{{background:#fff9e8;border:2px solid #051824;margin:18px 0;padding:14px}}img{{display:block;width:100%;image-rendering:auto}}</style></head><body><header><span class="status">IMMUTABLE CANDIDATE - NOT CURRENT</span><h1>Kettle Ligne-Claire V1</h1><p>Exact high-resolution canvases and alpha; judged at 56–62 logical pixels. V45 pivot, rattle keyframes, support carrying, locks, tea interaction and all six steam strips are untouched.</p></header><main><article><img src="/keeper-review/{SET}/assets/{evidence.name}"></article></main></body></html>'''; (PUBLIC/"index.html").write_text(html,encoding="utf-8"); (PUBLIC/"manifest.json").write_text(json.dumps(manifest,separators=(",",":"))+"\n",encoding="utf-8")


def verify() -> None:
    manifest=json.loads((PACK/"manifest.json").read_text(encoding="utf-8")); contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    for record in manifest["objects"]:
        source=Image.open(ROOT/record["sourceFile"]).convert("RGBA"); candidate=Image.open(ROOT/record["candidateFile"]).convert("RGBA")
        if source.size!=candidate.size or alpha_sha(source)!=alpha_sha(candidate) or source.getchannel("A").getbbox()!=candidate.getchannel("A").getbbox(): raise RuntimeError(f"kettle geometry drift: {record['filename']}")
    if sha256(ROOT/manifest["objects"][0]["candidateFile"])!=sha256(ROOT/manifest["objects"][1]["candidateFile"]): raise RuntimeError("Off/On candidate bytes differ")
    for effect in manifest["effects"]:
        if sha256(ROOT/effect["sourceFile"])!=sha256(ROOT/effect["preservedFile"]): raise RuntimeError(f"effect changed: {effect['filename']}")
    preserved=manifest["preservedBehaviour"]
    if preserved["brokenBodyAnimation"]!=contract["states"]["broken"]["bodyAnimation"] or preserved["teaInteraction"]!=contract["teaInteraction"] or preserved["brokenAssetLock"]!=contract["brokenAssetLock"]: raise RuntimeError("behaviour snapshot drift")
    if manifest["registration"]["register"] or manifest["registration"]["promote"]: raise RuntimeError("registration gate opened")
    html=(PUBLIC/"index.html").read_text(encoding="utf-8")
    if 'src="assets/' in html or "image-rendering:auto" not in html: raise RuntimeError("review delivery regression")
    print("Verified kettle V1: exact high-res canvases/alphas, Off=On, V45 motion/interactions and six effect strips preserved")


if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--verify",action="store_true"); args=parser.parse_args(); verify() if args.verify else build()
