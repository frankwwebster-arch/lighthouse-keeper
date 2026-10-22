#!/usr/bin/env python3
"""Build the immutable dishwasher Ligne-Claire V1 review family.

The approved V41 dishwasher remains the structural and behaviour authority.
This draft changes only drawing language, except for the explicitly requested
semantic correction: the LCD and status lamp belong to the door's top control
rail, not to the front fascia.  That rail moves with the door in Broken.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-dishwasher-ligne-claire-v1"
DATED = "kitchen-dishwasher-ligne-claire-2026-10-22-v1"
PACK = ROOT / "art" / "drafts" / DATED
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public" / "keeper-review" / SET
PUBLIC_ASSETS = PUBLIC / "assets"
SOURCE = ROOT / "art" / "raw" / "kitchen-dishwasher-workbench-2026-10-20-v41"
APPROVED_FITTED = ROOT / "art" / "drafts" / "kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3"
APPROVED_FITTED_DECISION = ROOT / "docs" / "review" / "kitchen-fitted-cabinet-ligne-claire-v3-approval-2026-10-21.json"
V41_DECISION = ROOT / "docs" / "review" / "kitchen-dishwasher-workbench-v41-approval-2026-10-20.json"

DENSITY = 8
LINE = 6
INK = "#051824"
INK_2 = "#0a222b"
CREAM = "#faf4e0"
CREAM_2 = "#f6e5b7"
METAL = "#d9ded3"
METAL_DARK = "#aebbb9"
BLUE = "#235b85"
BLUE_DARK = "#1d4562"
SEA = "#53b1b5"
SEA_LIGHT = "#6dc9c2"
COPPER = "#d36f2d"
AQUA = "#32d2ce"
GREEN = "#51aa60"
RED = "#e84833"

SUFFIXES = {
    "": (False, False),
    "-le-re": (False, False),
    "-le-rj": (False, True),
    "-lj-re": (True, False),
    "-lj-rj": (True, True),
}


def p(value: float) -> int:
    return round(value * DENSITY)


def box(x0: float, y0: float, x1: float, y1: float) -> tuple[int, int, int, int]:
    return p(x0), p(y0), p(x1), p(y1)


def points(values: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(p(x), p(y)) for x, y in values]


def edge(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], fill: str = INK, closed: bool = False) -> None:
    path = points(values + ([values[0]] if closed else []))
    draw.line(path, fill=fill, width=LINE, joint="curve")


def polygon(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], fill: str, outline: str = INK) -> None:
    draw.polygon(points(values), fill=fill)
    edge(draw, values, outline, closed=True)


def ellipse(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float], fill: str, outline: str = INK) -> None:
    draw.ellipse(box(*bounds), fill=fill, outline=outline, width=LINE)


def rounded(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float], radius: float, fill: str, outline: str = INK) -> None:
    draw.rounded_rectangle(box(*bounds), radius=p(radius), fill=fill, outline=outline, width=LINE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def alpha_bounds(image: Image.Image) -> list[int] | None:
    value = image.getchannel("A").getbbox()
    return list(value) if value else None


def base_master(left_joined: bool, right_joined: bool) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (98 * DENSITY, 82 * DENSITY), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Carcass and plinth. Every described edge uses exactly LINE pixels.
    rounded(draw, (8.0, 18.0, 18.0, 79.5), 1.5, BLUE)
    rounded(draw, (80.0, 18.0, 90.0, 79.5), 1.5, BLUE)
    draw.rectangle(box(11.0, 22.0, 15.0, 71.5), fill=BLUE_DARK)
    draw.rectangle(box(83.0, 22.0, 87.0, 71.5), fill=BLUE_DARK)
    rounded(draw, (10.0, 71.2, 88.0, 79.5), 1.2, BLUE)
    draw.rectangle(box(17.0, 74.0, 81.0, 78.0), fill=BLUE_DARK)
    rounded(draw, (8.5, 72.0, 17.0, 81.0), 1.3, BLUE)
    rounded(draw, (81.0, 72.0, 89.5, 81.0), 1.3, BLUE)

    # Approved fitted-family worktop colours, with one top edge and one front edge.
    rounded(draw, (6.5, 7.3, 91.5, 22.0), 4.0, SEA)
    edge(draw, [(10.0, 11.0), (88.0, 11.0)], SEA_LIGHT)
    edge(draw, [(8.2, 19.7), (89.8, 19.7)], INK)
    if left_joined:
        draw.rectangle(box(0.0, 7.0, 9.0, 21.8), fill=SEA)
        edge(draw, [(0.0, 19.7), (9.5, 19.7)], INK)
    if right_joined:
        draw.rectangle(box(89.0, 7.0, 98.0, 21.8), fill=SEA)
        edge(draw, [(88.5, 19.7), (98.0, 19.7)], INK)
    return image, draw


def closed_master(state: str, left_joined: bool, right_joined: bool) -> Image.Image:
    image, draw = base_master(left_joined, right_joined)

    # The control rail is the door's narrow upward-facing top edge. This is the
    # requested correction to the old floating front-fascia controls.
    rail = [(16.0, 20.7), (82.0, 20.7), (78.8, 30.2), (19.2, 30.2)]
    polygon(draw, rail, CREAM_2)
    screen = [(23.0, 22.5), (47.0, 22.5), (44.8, 27.8), (24.8, 27.8)]
    polygon(draw, screen, INK, INK)
    if state == "on":
        for x in (27.0, 33.1, 39.2):
            polygon(draw, [(x, 23.8), (x + 4.0, 23.8), (x + 3.4, 26.5), (x + 0.5, 26.5)], AQUA, AQUA)
    else:
        edge(draw, [(27.0, 25.2), (41.5, 25.2)], METAL_DARK)
    ellipse(draw, (67.2, 22.4, 73.5, 28.5), METAL_DARK)
    lamp = GREEN if state == "on" else CREAM
    ellipse(draw, (75.0, 22.3, 80.1, 27.4), lamp)

    # Closed front plane, then the physical handle. No shine strokes.
    rounded(draw, (15.0, 29.2, 83.0, 74.0), 1.1, METAL)
    ellipse(draw, (28.0, 37.6, 35.4, 45.2), COPPER)
    ellipse(draw, (63.1, 37.6, 70.5, 45.2), COPPER)
    rounded(draw, (31.3, 39.1, 67.2, 43.9), 1.7, COPPER)
    return image


def broken_master(left_joined: bool, right_joined: bool) -> Image.Image:
    image, draw = base_master(left_joined, right_joined)

    # Open cavity and the same sparse, mechanically legible contents.
    rounded(draw, (14.5, 21.0, 83.5, 61.0), 1.6, INK)
    ellipse(draw, (19.0, 35.0, 38.0, 55.0), BLUE_DARK)
    ellipse(draw, (31.0, 34.0, 48.0, 55.0), METAL_DARK)
    ellipse(draw, (49.0, 44.0, 57.0, 52.0), BLUE_DARK)
    rounded(draw, (61.0, 37.0, 72.0, 52.0), 1.2, METAL)
    edge(draw, [(72.0, 40.0), (76.0, 41.0), (76.0, 48.5), (72.0, 49.5)], METAL_DARK)
    edge(draw, [(17.0, 54.0), (80.0, 54.0)], METAL_DARK)

    # The door retains the inherited skew-whiff footprint. The control rail is
    # attached to its upper edge and therefore moves with it.
    door = [(8.5, 50.5), (13.0, 46.0), (28.0, 48.0), (82.0, 56.0), (88.0, 65.0), (81.0, 79.0), (24.0, 77.0), (14.0, 70.0)]
    polygon(draw, door, METAL)
    rail = [(13.0, 46.0), (28.0, 48.0), (82.0, 56.0), (79.8, 60.0), (26.5, 52.3), (11.0, 50.0)]
    polygon(draw, rail, CREAM_2)
    screen = [(21.0, 48.2), (39.0, 50.8), (37.7, 53.3), (20.0, 50.8)]
    polygon(draw, screen, INK, INK)
    edge(draw, [(24.0, 50.0), (27.0, 51.8), (30.0, 50.9), (33.0, 52.7)], RED)
    ellipse(draw, (69.0, 54.3, 74.0, 59.3), RED)

    # Handle remains on the front face and follows the same door perspective.
    ellipse(draw, (25.0, 54.0, 32.4, 61.4), COPPER)
    ellipse(draw, (62.0, 64.3, 69.4, 71.7), COPPER)
    edge(draw, [(29.0, 57.8), (65.8, 68.0)], COPPER)
    return image


def register(master: Image.Image, source: Image.Image) -> Image.Image:
    candidate = master.resize(source.size, Image.Resampling.LANCZOS)
    candidate.putalpha(source.getchannel("A"))
    return candidate


def checker(size: tuple[int, int], cell: int = 16) -> Image.Image:
    out = Image.new("RGBA", size, (246, 240, 220, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def fitted_panel() -> Image.Image:
    cabinet = Image.open(APPROVED_FITTED / "candidates" / "cabinets" / "cabinet-a-le-re.png").convert("RGBA")
    return cabinet


def make_evidence(records: list[dict[str, object]]) -> list[Path]:
    font = ImageFont.load_default()
    static = [r for r in records if r["suffix"] == ""]
    sheet = Image.new("RGBA", (1500, 1080), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((20, 16), "Dishwasher Ligne-Claire V1 - current / candidate / geometry ghost", fill=INK, font=font)
    draw.text((20, 38), "Exact 98 x 82 canvas and byte-exact alpha. Controls corrected to the door's top rail.", fill=INK, font=font)
    for row, record in enumerate(static):
        source = Image.open(ROOT / str(record["sourceFile"])).convert("RGBA")
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        master = Image.open(ROOT / str(record["masterFile"])).convert("RGBA")
        y = 72 + row * 330
        for col, item in enumerate((source, candidate, candidate)):
            panel = checker((470, 280), 20)
            shown = item.resize((item.width * 5, item.height * 5), Image.Resampling.LANCZOS)
            panel.alpha_composite(shown, ((470 - shown.width) // 2, (280 - shown.height) // 2))
            if col == 2:
                ghost = source.resize(shown.size, Image.Resampling.LANCZOS)
                tint = Image.new("RGBA", ghost.size, (232, 72, 86, 0))
                tint.putalpha(ghost.getchannel("A").point(lambda v: round(v * 0.36)))
                panel.alpha_composite(tint, ((470 - shown.width) // 2, (280 - shown.height) // 2))
            sheet.alpha_composite(panel, (10 + col * 495, y))
        draw.text((20, y + 286), f"CURRENT {record['state']}", fill=INK, font=font)
        draw.text((515, y + 286), f"V1 {record['state']} - 8x authored, registered once", fill=INK, font=font)
        draw.text((1010, y + 286), "GHOST - red is inherited authority envelope", fill=INK, font=font)
        sheet.alpha_composite(master.resize((196, 164), Image.Resampling.LANCZOS), (1270, y + 106))
    contact = EVIDENCE / "dishwasher-current-candidate-ghost.png"
    sheet.save(contact, optimize=True)

    # 64 px readability and family-palette proof.
    small = Image.new("RGBA", (920, 300), (250, 244, 224, 255))
    sdraw = ImageDraw.Draw(small)
    sdraw.text((18, 16), "64 px width proof - Off / On / Broken; approved V3 cabinet palette at right", fill=INK, font=font)
    for index, record in enumerate(static):
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        width = 64
        height = round(candidate.height * width / candidate.width)
        tiny = candidate.resize((width, height), Image.Resampling.LANCZOS)
        panel = checker((210, 220), 10)
        panel.alpha_composite(tiny, ((210 - width) // 2, (220 - height) // 2))
        panel.alpha_composite(candidate.resize((196, 164), Image.Resampling.LANCZOS), (7, 48))
        small.alpha_composite(panel, (10 + index * 220, 58))
        sdraw.text((20 + index * 220, 280), str(record["state"]).upper(), fill=INK, font=font)
    cabinet = fitted_panel()
    panel = checker((230, 220), 10)
    panel.alpha_composite(cabinet.resize((196, 164), Image.Resampling.LANCZOS), (17, 28))
    small.alpha_composite(panel, (680, 58))
    sdraw.text((692, 280), "APPROVED V3 FITTED FAMILY", fill=INK, font=font)
    proof64 = EVIDENCE / "dishwasher-64px-and-palette-proof.png"
    small.save(proof64, optimize=True)

    variants = Image.new("RGBA", (1240, 900), (250, 244, 224, 255))
    vdraw = ImageDraw.Draw(variants)
    vdraw.text((18, 16), "All 15 exact-canvas candidates - base plus four healing edge states", fill=INK, font=font)
    for index, record in enumerate(records):
        candidate = Image.open(ROOT / str(record["candidateFile"])).convert("RGBA")
        x = 10 + (index % 5) * 246
        y = 52 + (index // 5) * 275
        panel = checker((236, 230), 12)
        shown = candidate.resize((196, 164), Image.Resampling.LANCZOS)
        panel.alpha_composite(shown, (20, 18))
        variants.alpha_composite(panel, (x, y))
        vdraw.text((x + 8, y + 236), str(record["filename"]), fill=INK, font=font)
    all_variants = EVIDENCE / "dishwasher-all-edge-variants.png"
    variants.save(all_variants, optimize=True)
    return [contact, proof64, all_variants]


def review_html() -> str:
    states = "".join(
        f'<button data-state="{state}">{state.title()}</button>' for state in ("off", "on", "broken")
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dishwasher Ligne-Claire V1</title><style>:root{{--ink:#051824;--paper:#fff9e8;--cream:#f6e5b7;--blue:#235b85;--amber:#e7a638}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:22px}}header{{border-bottom:4px solid var(--ink)}}.status,button{{border:2px solid var(--ink);background:var(--amber);padding:7px 12px;font:inherit;font-weight:750}}button.active{{background:#6dc9c2}}.panel{{background:var(--paper);border:2px solid var(--ink);margin:18px 0;padding:15px}}.views{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}}.stage{{position:relative;min-height:360px;background:repeating-conic-gradient(#eee6cf 0 25%,#d9cfb2 0 50%) 50%/28px 28px;overflow:hidden}}.stage img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;image-rendering:auto}}.ghost{{filter:hue-rotate(115deg) saturate(2);opacity:.35}}.native{{width:98px;height:82px}}.small{{width:64px;height:auto}}.warning{{border-left:6px solid #e84833;padding-left:14px}}article img{{display:block;width:100%;height:auto}}@media(max-width:850px){{.views{{grid-template-columns:1fr}}}}</style></head><body><header><span class="status">IMMUTABLE CANDIDATE - NOT CURRENT</span> <span class="status" id="ready">PRELOADING</span><h1>Dishwasher Ligne-Claire V1</h1><p class="warning">Approval gate is closed. V41, V3, production selectors and gameplay remain untouched.</p><p>One even contour weight, only real edges, closed flat colours, no gradients or shine. The LCD and lamp now occupy the door's top control rail; in Broken that rail moves with the door.</p></header><main><div>{states} <label><input id="ghostToggle" type="checkbox" checked> authority ghost</label></div><section class="panel views"><div><h2>Current V41 authority</h2><div class="stage"><img id="current"></div></div><div><h2>V1 candidate</h2><div class="stage"><img id="candidate"></div></div><div><h2>Ghost check</h2><div class="stage"><img id="ghostCandidate"><img id="ghostCurrent" class="ghost"></div></div></section><section class="panel"><h2>Actual display sizes</h2><div><img id="native" class="native"> exact 98 x 82 &nbsp; <img id="small" class="small"> 64 px wide</div></section><article class="panel"><h2>Current / candidate / ghost evidence</h2><img src="/keeper-review/{SET}/assets/dishwasher-current-candidate-ghost.png"></article><article class="panel"><h2>64 px and approved palette proof</h2><img src="/keeper-review/{SET}/assets/dishwasher-64px-and-palette-proof.png"></article><article class="panel"><h2>Every healing edge candidate</h2><img src="/keeper-review/{SET}/assets/dishwasher-all-edge-variants.png"></article></main><script>const base='/keeper-review/{SET}/assets/';let state='off';const names=s=>`dishwasher-${{s}}.png`;const current=document.getElementById('current'),candidate=document.getElementById('candidate'),gc=document.getElementById('ghostCurrent'),gn=document.getElementById('ghostCandidate'),native=document.getElementById('native'),small=document.getElementById('small');function show(s){{state=s;const c=base+'current--'+names(s),n=base+'candidate--'+names(s);current.src=c;candidate.src=n;gc.src=c;gn.src=n;native.src=n;small.src=n;document.querySelectorAll('[data-state]').forEach(b=>b.classList.toggle('active',b.dataset.state===s))}}document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>show(b.dataset.state));document.getElementById('ghostToggle').onchange=e=>gc.style.display=e.target.checked?'block':'none';(async()=>{{const urls=[];for(const s of ['off','on','broken'])urls.push(base+'current--'+names(s),base+'candidate--'+names(s));urls.push(base+'dishwasher-current-candidate-ghost.png',base+'dishwasher-64px-and-palette-proof.png',base+'dishwasher-all-edge-variants.png');await Promise.all(urls.map(src=>new Promise((ok,no)=>{{const i=new Image;i.onload=async()=>{{try{{await i.decode()}}catch{{}}ok()}};i.onerror=no;i.src=src}})));document.getElementById('ready').textContent='ALL UNIQUE IMAGES DECODED';show('off')}})()</script></body></html>'''


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable V1 draft or review route")
    if not APPROVED_FITTED_DECISION.exists() or not V41_DECISION.exists():
        raise RuntimeError("required approvals are missing")
    for directory in (MASTERS, CANDIDATES, EVIDENCE, PUBLIC_ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    for state in ("off", "on", "broken"):
        for suffix, flags in SUFFIXES.items():
            filename = f"dishwasher-{state}{suffix}.png"
            source_path = SOURCE / filename
            source = Image.open(source_path).convert("RGBA")
            master = broken_master(*flags) if state == "broken" else closed_master(state, *flags)
            master_path = MASTERS / filename.replace(".png", "-master-8x.png")
            candidate_path = CANDIDATES / filename
            master.save(master_path, optimize=True)
            candidate = register(master, source)
            candidate.save(candidate_path, optimize=True)
            records.append({
                "state": state,
                "suffix": suffix,
                "filename": filename,
                "sourceFile": source_path.relative_to(ROOT).as_posix(),
                "sourceSha256": sha256(source_path),
                "sourcePixels": list(source.size),
                "sourceAlphaBounds": alpha_bounds(source),
                "sourceAlphaSha256": alpha_sha(source),
                "masterFile": master_path.relative_to(ROOT).as_posix(),
                "masterSha256": sha256(master_path),
                "masterPixels": list(master.size),
                "candidateFile": candidate_path.relative_to(ROOT).as_posix(),
                "candidateSha256": sha256(candidate_path),
                "candidatePixels": list(candidate.size),
                "candidateAlphaBounds": alpha_bounds(candidate),
                "candidateAlphaSha256": alpha_sha(candidate),
                "alphaExact": alpha_sha(source) == alpha_sha(candidate),
            })

    evidence = make_evidence(records)
    manifest = {
        "schema": "lighthouse-keeper/kitchen-dishwasher-ligne-claire@1",
        "set": SET,
        "created": "2026-10-22",
        "status": "immutable-reversible-review-candidate-not-approved-not-registered",
        "scope": "Dishwasher Off/On/Broken plus every healing-edge variant",
        "styleRules": ["one even line weight", "real edges only", "closed flat colour", "no gradient shine glow or texture", "accurate machine construction", "64 px clarity", "near-black contour; black only for black materials", "marks use contour weight"],
        "authorizedSemanticCorrection": "LCD and state lamp moved from the front fascia to the door's top control rail; rail moves with the door in Broken",
        "sourceAuthority": {"set": "kitchen-dishwasher-workbench-v41", "approval": V41_DECISION.relative_to(ROOT).as_posix(), "approvalSha256": sha256(V41_DECISION), "preserved": True},
        "paletteAuthority": {"set": "kitchen-fitted-cabinet-ligne-claire-v3", "approval": APPROVED_FITTED_DECISION.relative_to(ROOT).as_posix(), "approvalSha256": sha256(APPROVED_FITTED_DECISION), "preserved": True},
        "records": records,
        "verification": {"canvasExact": True, "alphaExact": True, "ghostEvidence": True, "nativeAnd64pxProof": True, "movementAnimationInteractionHealingRuntimeChanged": False},
        "evidence": [{"file": item.relative_to(ROOT).as_posix(), "sha256": sha256(item)} for item in evidence],
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True},
        "rollback": "Discard only this V1 draft and review route; all source, approved and production files remain byte-for-byte unchanged.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"schema": "lighthouse-keeper/kitchen-batch-register@1", "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n", encoding="utf-8")
    hash_lines = []
    for path in sorted(PACK.rglob("*")):
        if path.is_file() and path.name != "HASHES.sha256":
            hash_lines.append(f"{sha256(path)}  {path.relative_to(PACK).as_posix()}")
    (PACK / "HASHES.sha256").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    for state in ("off", "on", "broken"):
        shutil.copy2(SOURCE / f"dishwasher-{state}.png", PUBLIC_ASSETS / f"current--dishwasher-{state}.png")
        shutil.copy2(CANDIDATES / f"dishwasher-{state}.png", PUBLIC_ASSETS / f"candidate--dishwasher-{state}.png")
    for item in evidence:
        shutil.copy2(item, PUBLIC_ASSETS / item.name)
    (PUBLIC / "index.html").write_text(review_html(), encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    if manifest["registration"] != {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True}:
        raise RuntimeError("registration gate opened")
    if len(manifest["records"]) != 15:
        raise RuntimeError("incomplete dishwasher family")
    for record in manifest["records"]:
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        if source.size != candidate.size or source.size != (98, 82):
            raise RuntimeError(f"canvas drift: {record['filename']}")
        if alpha_sha(source) != alpha_sha(candidate) or alpha_bounds(source) != alpha_bounds(candidate):
            raise RuntimeError(f"alpha drift: {record['filename']}")
        if sha256(ROOT / record["sourceFile"]) != record["sourceSha256"] or sha256(ROOT / record["candidateFile"]) != record["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record['filename']}")
    html = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in html or "LCD and lamp now occupy" not in html:
        raise RuntimeError("review delivery regression")
    if any(record["sourceSha256"] == record["candidateSha256"] for record in manifest["records"]):
        raise RuntimeError("candidate unexpectedly equals source")
    print("Verified dishwasher V1: 15 exact canvases/alphas, closed gate, corrected attached control rail")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
