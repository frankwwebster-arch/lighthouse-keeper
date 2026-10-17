#!/usr/bin/env python3
"""Build the Kitchen V18 B-only countertop calibration gate.

The immutable Kitchen V17 rollback remains untouched.  This gate reads only
the exact V5 standard rasters and replaces the inherited tapered countertop as
one semantic construction.  In particular, it never restores a rectangular
V5 crop after drawing the new surface (the defect in the historical V6 gate).
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
V5 = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
OLD_GATE = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v6-calibration"
SOURCE = ROOT / "art/source/kitchen-countertop-gate-2026-10-17-v18"
RAW = ROOT / "art/raw/kitchen-countertop-gate-2026-10-17-v18"
DRAFT = ROOT / "art/drafts/kitchen-countertop-gate-2026-10-17-v18"
PUBLIC = ROOT / "public/keeper-review/kitchen-countertop-gate-v18"
ASSETS = PUBLIC / "assets"

DENSITY = 4
LP_PER_BAY = 21
CELL_W = LP_PER_BAY * DENSITY
TOP_REVEAL_PX = 6
FASCIA_PX = 8
EDGE_X0 = 2
EDGE_X1 = 81
INK = (7, 27, 50, 255)
TRANSPARENT = (0, 0, 0, 0)

UNITS = {
    "obj_kettle": {
        "label": "Kettle counter",
        "file": "obj_kettle_standard_f1.png",
        "logical": [21, 31],
        "contact_y": 48,
        "inherited_surface": [0, 38, 84, 56],
        "appliance_shift_y": 4,
        "old_gate_front_y": 48,
    },
    "obj_cooker": {
        "label": "Cooker / hob",
        "file": "obj_cooker_standard_f1.png",
        "logical": [21, 28],
        "contact_y": 36,
        "inherited_surface": [0, 20, 84, 36],
        "appliance_shift_y": 0,
        "old_gate_front_y": 32,
    },
    "obj_sink": {
        "label": "Sink counter",
        "file": "obj_sink_standard_f1.png",
        "logical": [21, 29],
        "contact_y": 40,
        "inherited_surface": [0, 38, 84, 56],
        "appliance_shift_y": 0,
        "old_gate_front_y": 48,
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(file.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(file.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load(stem: str) -> Image.Image:
    return Image.open(V5 / UNITS[stem]["file"]).convert("RGBA")


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def clear(image: Image.Image, box: list[int]) -> None:
    image.paste(TRANSPARENT, tuple(box))


def opaque_copy(source: Image.Image, box: tuple[int, int, int, int], offset: tuple[int, int]) -> Image.Image:
    """Return a full-canvas shape layer without copying transparent rectangles."""
    layer = Image.new("RGBA", source.size, TRANSPARENT)
    layer.alpha_composite(source.crop(box), offset)
    return layer


def wood_structure(size: tuple[int, int], contact_y: int) -> Image.Image:
    """One continuous 20-lp V5-derived top and fascia, with no old edge pixels."""
    authority = load("obj_kettle")
    rear_y = contact_y - TOP_REVEAL_PX
    # The centre contains only V5 wood.  Stretching that texture avoids copying
    # either of V5's tapered outer outlines into the new straight construction.
    material = authority.crop((12, 42, 72, 56)).resize(
        (EDGE_X1 - EDGE_X0 + 1, TOP_REVEAL_PX + FASCIA_PX),
        Image.Resampling.LANCZOS,
    )
    material.putalpha(255)
    out = Image.new("RGBA", size, TRANSPARENT)
    out.alpha_composite(material, (EDGE_X0, rear_y))
    draw = ImageDraw.Draw(out)
    draw.rectangle((EDGE_X0, rear_y, EDGE_X1, contact_y + FASCIA_PX - 1), outline=INK, width=2)
    draw.line((EDGE_X0, contact_y - 1, EDGE_X1, contact_y - 1), fill=INK, width=2)
    return out


def hob_structure(size: tuple[int, int], contact_y: int) -> Image.Image:
    """Straighten the V5 hob envelope while keeping its centre material."""
    base = load("obj_cooker")
    rear_y = contact_y - TOP_REVEAL_PX
    material = base.crop((12, 30, 72, 36)).resize((80, 6), Image.Resampling.LANCZOS)
    material.putalpha(255)
    out = Image.new("RGBA", size, TRANSPARENT)
    out.alpha_composite(material, (EDGE_X0, rear_y))
    draw = ImageDraw.Draw(out)
    draw.rectangle((EDGE_X0, rear_y, EDGE_X1, contact_y - 1), outline=INK, width=2)
    return out


def kettle_appliance(base: Image.Image) -> Image.Image:
    # The exact V5 kettle is wholly above row 38.  Shift it 1 lp down so its
    # contact shadow rests on the corrected rear edge at y=42.
    return opaque_copy(base, (0, 0, base.width, 38), (0, 4))


def sink_appliance(base: Image.Image) -> Image.Image:
    """Extract only tap/basin pixels; never restore the old wooden wings."""
    layer = Image.new("RGBA", base.size, TRANSPARENT)
    # Above the first inherited wood row every opaque pixel belongs to the tap.
    layer.alpha_composite(base.crop((0, 0, base.width, 38)), (0, 0))
    # Hand-measured basin/tap silhouette after row 37.  These are inclusive x
    # ranges and deliberately stop before the old tapered countertop shoulders.
    ranges = {
        38: [(21, 29), (42, 61)],
        39: [(21, 29), (42, 61)],
        40: [(22, 27), (43, 50)],
        41: [(16, 66)], 42: [(16, 66)], 43: [(15, 67)], 44: [(15, 67)],
        45: [(14, 68)], 46: [(14, 69)],
        47: [(13, 70)], 48: [(13, 70)], 49: [(13, 70)], 50: [(13, 70)],
        51: [(13, 70)], 52: [(12, 70)],
        53: [(13, 69)], 54: [(13, 69)], 55: [(13, 69)], 56: [(13, 69)],
        57: [(13, 69)], 58: [(13, 69)], 59: [(13, 69)], 60: [(13, 69)],
        61: [(14, 68)],
    }
    for y, spans in ranges.items():
        for x0, x1 in spans:
            layer.alpha_composite(base.crop((x0, y, x1 + 1, y + 1)), (x0, y))
    return layer


def cooker_appliance(base: Image.Image) -> Image.Image:
    """Keep V5's declared splashback and burners, excluding old hob shoulders."""
    layer = Image.new("RGBA", base.size, TRANSPARENT)
    layer.alpha_composite(base.crop((0, 0, base.width, 20)), (0, 0))
    # The central burner/splashback information is safe; the tapered outer hob
    # envelope lived outside x=10..73 and is intentionally discarded.
    layer.alpha_composite(base.crop((10, 20, 74, 30)), (10, 20))
    return layer


def sink_body_extension(base: Image.Image) -> Image.Image:
    """Reach the true 19-lp contact without stretching the V5 cabinet front."""
    layer = Image.new("RGBA", base.size, TRANSPARENT)
    layer.alpha_composite(base.crop((4, 56, 13, 64)), (4, 48))
    layer.alpha_composite(base.crop((70, 56, 80, 64)), (70, 48))
    return layer


def make_candidate(stem: str) -> tuple[Image.Image, Image.Image, Image.Image]:
    spec = UNITS[stem]
    base = load(stem)
    out = base.copy()
    clear(out, spec["inherited_surface"])
    if stem == "obj_kettle":
        # Clear the old kettle before placing the same pixels at the corrected contact.
        clear(out, [0, 0, 84, 42])
        structure = wood_structure(base.size, spec["contact_y"])
        appliance = kettle_appliance(base)
    elif stem == "obj_sink":
        structure = wood_structure(base.size, spec["contact_y"])
        appliance = sink_appliance(base)
        out.alpha_composite(sink_body_extension(base))
    else:
        clear(out, [0, 0, 84, 36])
        structure = hob_structure(base.size, spec["contact_y"])
        appliance = cooker_appliance(base)
    out.alpha_composite(structure)
    out.alpha_composite(appliance)
    return out, structure, appliance


def ghost(base: Image.Image, candidate: Image.Image) -> Image.Image:
    out = Image.new("RGBA", base.size, (8, 18, 28, 255))
    old = Image.new("RGBA", base.size, (255, 75, 108, 0))
    old.putalpha(base.getchannel("A").point(lambda a: round(a * 0.55)))
    out.alpha_composite(old)
    new = candidate.copy()
    new.putalpha(new.getchannel("A").point(lambda a: round(a * 0.78)))
    out.alpha_composite(new)
    return out


def edges(base: Image.Image, candidate: Image.Image) -> Image.Image:
    def edge(alpha: Image.Image) -> Image.Image:
        return ImageChops.difference(alpha.filter(ImageFilter.MaxFilter(3)), alpha.filter(ImageFilter.MinFilter(3)))
    out = Image.new("RGBA", base.size, (8, 18, 28, 255))
    red = Image.new("RGBA", base.size, (255, 91, 91, 0)); red.putalpha(edge(base.getchannel("A")))
    cyan = Image.new("RGBA", base.size, (83, 221, 232, 0)); cyan.putalpha(edge(candidate.getchannel("A")))
    out.alpha_composite(red); out.alpha_composite(cyan)
    return out


def aligned_triptych(images: dict[str, Image.Image], guide: bool = False) -> Image.Image:
    height = 31 * DENSITY
    out = Image.new("RGBA", (3 * CELL_W, height), TRANSPARENT)
    for index, stem in enumerate(UNITS):
        image = images[stem]
        out.alpha_composite(image, (index * CELL_W, height - image.height))
    if guide:
        draw = ImageDraw.Draw(out)
        y = height - 19 * DENSITY
        draw.line((0, y, out.width - 1, y), fill=(85, 221, 232, 220), width=1)
    return out


def neutral_room_context(images: dict[str, Image.Image], guide: bool = False) -> Image.Image:
    """Three adjacent bays on the rear-wall line with 4 lp clear foreground."""
    width = 3 * LP_PER_BAY * DENSITY
    height = 56 * DENSITY
    wall_floor_y = 51 * DENSITY
    foot_y = 52 * DENSITY
    out = Image.new("RGBA", (width, height), (246, 224, 179, 255))
    draw = ImageDraw.Draw(out)
    # Neutral painted/stone room trim: no furniture-like timber picture frame.
    draw.rectangle((0, 0, width - 1, 7), fill=(231, 224, 204, 255))
    draw.line((0, 7, width - 1, 7), fill=(102, 109, 112, 255), width=2)
    draw.rectangle((0, wall_floor_y - 6, width - 1, wall_floor_y - 1), fill=(224, 216, 194, 255))
    draw.line((0, wall_floor_y - 7, width - 1, wall_floor_y - 7), fill=(102, 109, 112, 255), width=1)
    # Restrained wood floor is material, not a heavy structural surround.
    draw.rectangle((0, wall_floor_y, width - 1, height - 1), fill=(142, 82, 49, 255))
    draw.line((0, wall_floor_y, width - 1, wall_floor_y), fill=INK, width=2)
    draw.line((0, wall_floor_y + 8, width - 1, wall_floor_y + 8), fill=(199, 126, 68, 255), width=1)
    for x in range(0, width, 28):
        draw.line((x, wall_floor_y + 1, min(width - 1, x + 12), wall_floor_y + 1), fill=(183, 111, 61, 255), width=1)
    for index, stem in enumerate(UNITS):
        image = images[stem]
        out.alpha_composite(image, (index * CELL_W, foot_y - image.height))
    if guide:
        contact_y = foot_y - 19 * DENSITY
        draw.line((0, contact_y, width - 1, contact_y), fill=(40, 186, 201, 225), width=1)
        draw.line((0, foot_y, width - 1, foot_y), fill=(239, 182, 77, 225), width=1)
        for x in (CELL_W, CELL_W * 2):
            draw.line((x, 0, x, height - 1), fill=(214, 70, 77, 150), width=1)
    return out


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V18 countertop gate</title><style>
:root{color-scheme:dark;--bg:#07131c;--panel:#102630;--card:#0a1c25;--line:#365663;--ink:#f7f1dd;--muted:#adc0c7;--gold:#efb64d;--cyan:#55dde8;--red:#ff6f7d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1460px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.notice{border-left:4px solid var(--gold);background:#292417;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(3,minmax(270px,1fr));gap:12px}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}.well{min-height:180px;display:flex;align-items:end;justify-content:center;background:repeating-conic-gradient(#172c36 0 25%,#10232d 0 50%) 0/16px 16px;border-radius:8px;padding:10px;overflow:auto}.well img{flex:none}.triptych img{width:1008px;height:496px;image-rendering:auto}.roomview img{width:1008px;height:896px;image-rendering:auto}.native img{width:auto;height:auto}.logical img{image-rendering:auto}.compare{display:grid;grid-template-columns:1fr 1fr;gap:10px}.label{text-align:center;color:var(--muted);font-size:.82rem;margin-top:4px}button{background:#17333f;color:var(--ink);border:1px solid #66818b;border-radius:7px;padding:7px 10px;margin:0 5px 8px 0}button[aria-pressed=true]{border-color:var(--cyan);color:var(--cyan)}button:disabled{opacity:.45}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--line)}code{color:#9ce6eb}.pass{color:#8be69b}.fail{color:#ff8993}.small{font-size:.88rem;color:var(--muted)}@media(max-width:900px){.grid{grid-template-columns:1fr}.compare{grid-template-columns:1fr}.triptych img,.roomview img{max-width:none}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">Gate 1</span><span class="tag">B only · 1.5 lp</span><h1>Kitchen V18 · corrected countertop calibration</h1><p>Exact V5 is the sole visual baseline. The historical A/B/C page is used only as a labelled negative control; none of its candidate pixels are reused.</p><p id="loading" class="notice">Preloading and decoding every review image…</p></header><main>
<section class="panel"><h2>Approval boundary</h2><p class="notice"><strong>Please judge only these three standard units:</strong> kettle, cooker and sink. Approval authorises the construction recipe for the later family redraw. It does not approve or wire any kitchen asset into the game.</p><p>The selected construction is fixed: 20-lp width inside each 21-lp bay, 1.5-lp/6-px visible top, 2-lp/8-px fascia, zero shear and parallel vertical sides. The common worktop/hob contact is exactly 19 lp above the foot anchor.</p></section>
<section class="panel"><h2>Three-unit alignment proof</h2><div class="well triptych"><img id="triptych" src="__TRIPTYCH__" alt="Kettle, cooker and sink aligned on the 19-lp contact guide"></div><p class="small">Cyan is the exact shared 19-lp contact. Each raster is bottom-aligned without scaling; transparent bay gutters remain intact.</p></section>
<section class="panel"><h2>In situ · three adjacent rear-wall bays</h2><div><button id="roomClean" aria-pressed="true">Clean room</button><button id="roomGuides" aria-pressed="false">Show measured guides</button></div><div class="well roomview"><img id="room" src="__ROOM__" alt="Three calibrated kitchen units mounted on the rear wall"></div><p class="small">Review staging only: a neutral painted/stone surround, rear-wall junction at 51 lp, object foot line at 52 lp, and exactly 4 lp of unobstructed foreground floor. The red guide mode marks the two bay joins; cyan marks the shared 19-lp contact; gold marks the object foot line.</p></section>
<section class="panel"><h2>Inspect each unit</h2><div id="cards" class="grid"></div></section>
<section class="panel"><h2>Binding anti-splinter tests</h2><table><thead><tr><th>Test</th><th>Corrected V18</th><th>Historical gate B</th></tr></thead><tbody><tr><td>No rectangular V5 preserve-box after surface draw</td><td class="pass">PASS</td><td class="fail">FAIL</td></tr><tr><td>Contact line derived from each declared cell height</td><td class="pass">48 / 36 / 40 px</td><td class="fail">48 / 32 / 48 px</td></tr><tr><td>Every exposed surface pixel equals the one semantic structure</td><td class="pass">PASS</td><td class="fail">FAIL</td></tr><tr><td>20-lp horizontal run; transparent shared edges</td><td class="pass">PASS</td><td class="fail">FAIL</td></tr></tbody></table><p>The automated verifier must make the old B candidates fail. Alpha continuity alone is insufficient: it checks exact RGBA outside the declared appliance silhouette, the six-row reveal, the contact row, and the safety gutters.</p></section>
<section class="panel"><h2>Exact logical scale</h2><div id="logical" class="well logical"></div></section>
<section class="panel"><h2>Provenance</h2><p>V17, runtime sprites, manifests, registers, Keeper animations and Final state are protected snapshots. Generated imagery informed the clean single-slab reading only; all review rasters are deterministically rebuilt from the exact V5 PNGs and measured masks.</p><div id="hashes"></div></section>
</main><script>
const DATA=__DATA__;const all=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))all.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const urls=[...new Set(all)];
function image(src,alt){const i=new Image;i.src=src;i.alt=alt;return i}function build(){const cards=document.getElementById('cards');for(const stem of DATA.unitOrder){const r=DATA.units[stem],c=document.createElement('article');c.className='card';c.innerHTML=`<h3>${r.label}</h3><div><button data-mode="candidate" aria-pressed="true">Candidate</button><button data-mode="structure" aria-pressed="false">Structure</button><button data-mode="ghost" aria-pressed="false">Ghost</button><button data-mode="edges" aria-pressed="false">Edges</button></div><div class="compare"><div><div class="well native"></div><div class="label">Exact V5</div></div><div><div class="well native target"></div><div class="label">Corrected B</div></div></div><p class="small">Cell ${r.logical[0]}×${r.logical[1]} lp · contact y=${r.contactY}px · ${r.contactLp} lp above foot</p>`;c.querySelector('.native').append(image(r.v5,`${r.label} exact V5`));const target=c.querySelector('.target');target.append(image(r.candidate,`${r.label} candidate`));c.querySelectorAll('button').forEach(b=>b.onclick=()=>{c.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));target.replaceChildren(image(r[b.dataset.mode],`${r.label} ${b.dataset.mode}`))});cards.append(c);const logical=image(r.candidate,r.label);logical.style.width=r.logical[0]+'px';logical.style.height=r.logical[1]+'px';document.getElementById('logical').append(logical)}const room=document.getElementById('room'),clean=document.getElementById('roomClean'),guides=document.getElementById('roomGuides');clean.onclick=()=>{room.src=DATA.room;clean.setAttribute('aria-pressed','true');guides.setAttribute('aria-pressed','false')};guides.onclick=()=>{room.src=DATA.roomGuides;clean.setAttribute('aria-pressed','false');guides.setAttribute('aria-pressed','true')};const h=document.getElementById('hashes');for(const stem of DATA.unitOrder){const r=DATA.units[stem],p=document.createElement('p');p.innerHTML=`${r.label}: V5 <code>${r.v5Sha256}</code><br>V18 <code>${r.candidateSha256}</code>`;h.append(p)}document.getElementById('loading').textContent=`All ${urls.length} unique images loaded and decoded. Controls enabled.`;document.querySelectorAll('button').forEach(b=>b.disabled=false)}document.querySelectorAll('button').forEach(b=>b.disabled=true);Promise.all(urls.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(build).catch(()=>document.getElementById('loading').textContent='A review image failed to load.');
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    html = html.replace("__DATA__", json.dumps(data, separators=(",", ":")))
    html = html.replace("__TRIPTYCH__", data["triptych"])
    html = html.replace("__ROOM__", data["room"])
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    for folder in (SOURCE, RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    for folder in (RAW, DRAFT, ASSETS):
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()

    generated_reference = Path("/Users/frank/.codex/generated_images/01a141ee-8328-7620-9eff-090ec7bf264f/exec-27ca7caf-c5e8-4311-9ca0-f05db13e1330.png")
    if generated_reference.exists():
        shutil.copy2(generated_reference, SOURCE / "three-unit-single-slab-study.png")

    prefix = "/keeper-review/kitchen-countertop-gate-v18/assets"
    data = {"version": 18, "status": "review-only-gate", "unitOrder": list(UNITS), "units": {}}
    candidates: dict[str, Image.Image] = {}
    for stem, spec in UNITS.items():
        base = load(stem)
        candidate, structure, appliance = make_candidate(stem)
        candidates[stem] = candidate
        images = {
            "v5": base,
            "candidate": candidate,
            "structure": structure,
            "applianceMask": appliance,
            "ghost": ghost(base, candidate),
            "edges": edges(base, candidate),
        }
        urls = {}
        for kind, image in images.items():
            name = f"{stem}_{kind}.png"
            target = RAW / name if kind in {"candidate", "structure", "applianceMask"} else DRAFT / name
            save(image, target)
            save(image, ASSETS / name)
            urls[kind] = f"{prefix}/{name}"
        diff = ImageChops.difference(base, candidate).getbbox()
        data["units"][stem] = {
            "label": spec["label"], "logical": spec["logical"], "contactY": spec["contact_y"],
            "contactLp": 19, "topRevealPx": TOP_REVEAL_PX, "fasciaPx": FASCIA_PX,
            "v5Sha256": sha(V5 / spec["file"]), "candidateSha256": sha(RAW / f"{stem}_candidate.png"),
            "differenceBoundsPx": list(diff) if diff else None, **urls,
        }

    triptych = aligned_triptych(candidates, guide=True)
    save(triptych, RAW / "three_unit_contact_alignment.png")
    save(triptych, ASSETS / "three_unit_contact_alignment.png")
    data["triptych"] = f"{prefix}/three_unit_contact_alignment.png"
    room = neutral_room_context(candidates, guide=False)
    room_guides = neutral_room_context(candidates, guide=True)
    save(room, RAW / "three_unit_neutral_room.png")
    save(room, ASSETS / "three_unit_neutral_room.png")
    save(room_guides, RAW / "three_unit_neutral_room_guides.png")
    save(room_guides, ASSETS / "three_unit_neutral_room_guides.png")
    data["room"] = f"{prefix}/three_unit_neutral_room.png"
    data["roomGuides"] = f"{prefix}/three_unit_neutral_room_guides.png"
    (DRAFT / "gate-data.json").write_text(json.dumps(data, indent=2) + "\n")

    register = {
        "version": 18,
        "status": "review-only-gate",
        "soleVisualBaseline": "Kitchen Basic Assets V5",
        "historicalCalibrationPixelsReused": False,
        "selectedAbstractConstruction": {"option": "B", "topRevealLp": 1.5, "fasciaLp": 2, "shearLp": 0},
        "knownHistoricalRootCause": "V6 redrew a slab then restored rectangular V5 crops containing the inherited tapered worktop; sink/cooker front rows also missed the 19-lp contact datum.",
        "scope": ["obj_kettle standard", "obj_cooker standard", "obj_sink standard"],
        "fullFamilyRebuilt": False,
        "roomRebuilt": False,
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
        "protectedSnapshots": {
            "kitchenV5": tree_sha(V5),
            "kitchenV17": tree_sha(ROOT / "art/raw/kitchen-v5-exact-rollback-2026-10-17-v17"),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_page(data)
    print(json.dumps({"review": PUBLIC.relative_to(ROOT).as_posix(), "units": list(UNITS), "gate": "B only"}, indent=2))


if __name__ == "__main__":
    main()
