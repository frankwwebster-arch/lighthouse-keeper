#!/usr/bin/env python3
"""Build immutable dishwasher Ligne-Claire V2 from exact V41 geometry.

V2 rejects V1's reinterpreted control rail. The original V41 fascia, display,
selector and lamp positions are authoritative in every state. Only the Broken
handle receives Frank's explicitly authorised steeper angle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-dishwasher-ligne-claire-v2"
PACK = ROOT / "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v2"
PUBLIC = ROOT / "public/keeper-review" / SET
SOURCE = ROOT / "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41"
OVEN = ROOT / "art/drafts/kitchen-oven-ligne-claire-2026-10-21-v8/masters/oven-on-top-safe-master-8x.png"
APPROVED_CABINET = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/cabinet-a-le-rj.png"
APPROVED_OVEN = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/oven-on.png"
REFERENCES = ROOT / "art/raw/kitchen-dishwasher-ligne-claire-references-2026-10-22-v2"
V41_APPROVAL = ROOT / "docs/review/kitchen-dishwasher-workbench-v41-approval-2026-10-20.json"
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
OBJECT_ROOT = ROOT / "review-archive/objects"
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"

DENSITY = 16
LINE = 14
INK = "#051824"
INK_2 = "#0b2432"
CREAM = "#fff3d8"
CREAM_SHADOW = "#efd9aa"
METAL = "#d8d9ce"
METAL_DARK = "#8da1aa"
BLUE = "#235b85"
BLUE_DARK = "#1d4562"
SEA = "#53b1b5"
SEA_DARK = "#2f7785"
COPPER = "#f47b19"
AQUA = "#23d6dd"
GREEN = "#50bd4d"
RED = "#ef3328"

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


def pts(values: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(p(x), p(y)) for x, y in values]


def edge(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], fill: str = INK, width: int = LINE) -> None:
    draw.line(pts(values), fill=fill, width=width, joint="curve")


def polygon(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], fill: str, outline: str = INK) -> None:
    draw.polygon(pts(values), fill=fill)
    edge(draw, values + [values[0]], outline)


def rounded(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float], radius: float, fill: str, outline: str | None = INK) -> None:
    draw.rounded_rectangle(box(*bounds), radius=p(radius), fill=fill, outline=outline, width=LINE if outline else 1)


def ellipse(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float], fill: str, outline: str = INK) -> None:
    draw.ellipse(box(*bounds), fill=fill, outline=outline, width=LINE)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def alpha_bounds(image: Image.Image) -> list[int] | None:
    value = image.getchannel("A").getbbox()
    return list(value) if value else None


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def archive_object(source: Path) -> Path:
    digest = sha(source)
    target = OBJECT_ROOT / digest[:2] / f"{digest}{source.suffix.lower()}"
    if target.exists() and sha(target) != digest:
        raise RuntimeError(f"content-addressed archive collision: {target}")
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return target


def base_master(left_joined: bool, right_joined: bool) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (98 * DENSITY, 82 * DENSITY), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Cover the complete V41 alpha envelope. V1 began at y=7.3 while V41
    # alpha begins at y=4, exposing black RGB after alpha registration.
    rounded(draw, (7.0, 4.0, 91.0, 22.0), 4.0, SEA)
    edge(draw, [(10.5, 8.0), (87.5, 8.0)], SEA_DARK)
    if left_joined:
        draw.rectangle(box(0.0, 4.0, 10.0, 22.0), fill=SEA)
        edge(draw, [(0.0, 5.0), (10.0, 5.0)])
    if right_joined:
        draw.rectangle(box(88.0, 4.0, 98.0, 22.0), fill=SEA)
        edge(draw, [(88.0, 5.0), (98.0, 5.0)])

    rounded(draw, (8.0, 18.0, 18.0, 79.5), 1.5, BLUE)
    rounded(draw, (80.0, 18.0, 90.0, 79.5), 1.5, BLUE)
    draw.rectangle(box(10.5, 24.0, 14.3, 71.0), fill=BLUE_DARK)
    draw.rectangle(box(83.7, 24.0, 87.5, 71.0), fill=BLUE_DARK)
    rounded(draw, (8.0, 71.5, 90.0, 80.0), 1.3, BLUE)
    draw.rectangle(box(17.0, 74.0, 81.0, 78.3), fill=BLUE_DARK)
    return image, draw


def control_panel(draw: ImageDraw.ImageDraw, state: str) -> None:
    """One invariant physical panel; only the state indication changes."""
    # The fascia overlays the counter's lower outline: no black worktop band.
    rounded(draw, (15.0, 15.8, 83.0, 29.5), 1.0, CREAM)
    rounded(draw, (21.7, 17.8, 43.2, 25.3), 1.2, INK_2)
    if state == "on":
        for x in (24.4, 30.7, 37.0):
            draw.rounded_rectangle(box(x, 19.3, x + 4.0, 23.8), radius=p(0.35), fill=AQUA)
    elif state == "broken":
        edge(draw, [(24.5, 22.6), (28.0, 19.6), (31.5, 23.0), (35.0, 20.0), (39.5, 22.6)], RED)
    else:
        for x in (24.7, 31.0, 37.3):
            draw.rounded_rectangle(box(x, 19.8, x + 3.6, 23.3), radius=p(0.25), fill=BLUE_DARK)

    # Exact V41 order: selector, then tiny status lamp immediately to its right.
    ellipse(draw, (69.7, 18.3, 76.6, 25.2), METAL_DARK)
    draw.ellipse(box(71.5, 20.0, 74.8, 23.3), fill=CREAM_SHADOW)
    lamp = GREEN if state == "on" else RED if state == "broken" else CREAM_SHADOW
    ellipse(draw, (78.8, 19.0, 82.3, 22.5), lamp)


def closed_master(state: str, left_joined: bool, right_joined: bool) -> Image.Image:
    image, draw = base_master(left_joined, right_joined)
    control_panel(draw, state)
    rounded(draw, (15.0, 29.1, 83.0, 74.0), 1.2, CREAM)
    edge(draw, [(17.0, 31.3), (17.0, 69.8)], CREAM_SHADOW)
    edge(draw, [(81.0, 31.3), (81.0, 69.8)], CREAM_SHADOW)
    ellipse(draw, (27.8, 37.5, 35.2, 44.9), COPPER)
    ellipse(draw, (62.8, 37.5, 70.2, 44.9), COPPER)
    rounded(draw, (31.3, 39.0, 66.8, 43.5), 1.7, COPPER)
    edge(draw, [(34.0, 40.6), (64.0, 40.6)], "#b94c12", round(LINE * 0.58))
    return image


def broken_master(left_joined: bool, right_joined: bool) -> Image.Image:
    image, draw = base_master(left_joined, right_joined)
    control_panel(draw, "broken")
    rounded(draw, (14.0, 29.0, 84.0, 60.8), 1.6, INK_2)
    ellipse(draw, (18.0, 37.0, 36.5, 56.0), BLUE_DARK)
    ellipse(draw, (29.0, 34.5, 47.0, 55.5), METAL_DARK)
    ellipse(draw, (48.0, 44.0, 56.0, 52.0), BLUE_DARK)
    rounded(draw, (60.0, 36.5, 72.0, 52.5), 1.0, METAL)
    edge(draw, [(72.0, 39.0), (76.0, 40.5), (76.0, 48.5), (72.0, 50.0)], METAL_DARK)
    edge(draw, [(16.5, 53.5), (81.5, 53.5)], METAL_DARK)
    for x in (22.0, 31.0, 40.0, 49.0, 58.0, 67.0, 76.0):
        edge(draw, [(x, 52.0), (x, 58.0)], METAL_DARK, round(LINE * 0.72))

    # Prior door footprint. Only the handle angle is intentionally amended.
    door = [(5.0, 41.5), (8.5, 37.5), (23.0, 39.0), (83.5, 50.0), (91.0, 58.5), (82.0, 76.0), (20.5, 69.5), (11.5, 61.0)]
    polygon(draw, door, CREAM)
    edge(draw, [(9.0, 42.2), (82.0, 55.0)], CREAM_SHADOW)
    edge(draw, [(15.0, 63.0), (76.0, 70.0)], CREAM_SHADOW)
    ellipse(draw, (28.0, 48.7, 35.5, 56.2), COPPER)
    ellipse(draw, (61.0, 62.2, 68.5, 69.7), COPPER)
    edge(draw, [(31.7, 52.5), (64.7, 66.0)], COPPER, p(4.6))
    edge(draw, [(34.0, 53.7), (62.5, 65.2)], "#b94c12", round(LINE * 0.58))
    edge(draw, [(75.5, 62.0), (82.0, 69.2)], METAL_DARK)
    edge(draw, [(82.0, 62.0), (75.5, 69.2)], METAL_DARK)
    return image


def register(master: Image.Image, source: Image.Image) -> Image.Image:
    candidate = master.resize(source.size, Image.Resampling.LANCZOS)
    candidate.putalpha(source.getchannel("A"))
    # The twelve-row worktop cap is already the exact approved cabinet-run
    # treatment in V41. Preserve its RGBA bytes so the full kitchen counter is
    # continuous, not merely similar, at every edge state.
    candidate.paste(source.crop((0, 4, source.width, 16)), (0, 4))
    return candidate


def checker(size: tuple[int, int], cell: int = 16) -> Image.Image:
    out = Image.new("RGBA", size, (250, 244, 224, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def make_evidence(records: list[dict]) -> list[Path]:
    font = ImageFont.load_default()
    static = [item for item in records if item["suffix"] == ""]
    contact = Image.new("RGBA", (1510, 1100), (250, 244, 224, 255))
    draw = ImageDraw.Draw(contact)
    draw.text((20, 16), "Dishwasher V2 - exact V41 authority / corrected candidate / alpha ghost", fill=INK, font=font)
    draw.text((20, 38), "Invariant panel; original indicator placement; no black worktop band; only Broken handle angle authorised.", fill=INK, font=font)
    for row, item in enumerate(static):
        source = Image.open(ROOT / item["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / item["candidateFile"]).convert("RGBA")
        y = 70 + row * 335
        for col, image in enumerate((source, candidate, candidate)):
            panel = checker((480, 285), 18)
            shown = image.resize((392, 328), Image.Resampling.NEAREST)
            panel.alpha_composite(shown, ((480 - shown.width) // 2, -20))
            if col == 2:
                ghost = source.resize(shown.size, Image.Resampling.NEAREST)
                tint = Image.new("RGBA", ghost.size, (235, 35, 70, 0))
                tint.putalpha(ghost.getchannel("A").point(lambda value: round(value * 0.36)))
                panel.alpha_composite(tint, ((480 - shown.width) // 2, -20))
            contact.alpha_composite(panel, (10 + col * 500, y))
        draw.text((20, y + 290), f"V41 {item['state'].upper()}", fill=INK, font=font)
        draw.text((520, y + 290), f"V2 {item['state'].upper()}", fill=INK, font=font)
        draw.text((1020, y + 290), "GHOST / EXACT ALPHA", fill=INK, font=font)
    contact_path = EVIDENCE / "dishwasher-v41-v2-ghost.png"
    contact.save(contact_path, optimize=True)

    panel = Image.new("RGBA", (1250, 470), (250, 244, 224, 255))
    pdraw = ImageDraw.Draw(panel)
    pdraw.text((18, 16), "Invariant physical control panel - identical coordinates in Off / On / Broken", fill=INK, font=font)
    for index, item in enumerate(static):
        candidate = Image.open(ROOT / item["candidateFile"]).convert("RGBA")
        crop = candidate.crop((13, 15, 86, 33)).resize((584, 144), Image.Resampling.NEAREST)
        x = 18 + (index % 2) * 615
        y = 52 + (index // 2) * 190
        panel.alpha_composite(crop, (x, y))
        pdraw.text((x, y + 150), item["state"].upper(), fill=INK, font=font)
    pdraw.text((640, 395), "Only LCD and lamp state colour changes", fill=INK, font=font)
    panel_path = EVIDENCE / "dishwasher-control-panel-invariance.png"
    panel.save(panel_path, optimize=True)

    tiny = Image.new("RGBA", (950, 310), (250, 244, 224, 255))
    tdraw = ImageDraw.Draw(tiny)
    tdraw.text((18, 16), "64 px clarity - nearest enlarged for pixel audit", fill=INK, font=font)
    for index, item in enumerate(static):
        candidate = Image.open(ROOT / item["candidateFile"]).convert("RGBA")
        small = candidate.resize((64, round(candidate.height * 64 / candidate.width)), Image.Resampling.LANCZOS)
        tiny.alpha_composite(small.resize((256, 214), Image.Resampling.NEAREST), (18 + index * 310, 58))
        tdraw.text((20 + index * 310, 280), item["state"].upper(), fill=INK, font=font)
    tiny_path = EVIDENCE / "dishwasher-64px-proof.png"
    tiny.save(tiny_path, optimize=True)

    # Exact in-situ run: cabinet, dishwasher and oven at the same room origins
    # used by the movable V41 workbench. The two rows must share one counter.
    cabinet = Image.open(APPROVED_CABINET).convert("RGBA")
    oven = Image.open(APPROVED_OVEN).convert("RGBA")
    current_dw = Image.open(SOURCE / "dishwasher-on-lj-rj.png").convert("RGBA")
    candidate_dw = Image.open(CANDIDATES / "dishwasher-on-lj-rj.png").convert("RGBA")
    run_sheet = Image.new("RGBA", (1320, 800), (250, 244, 224, 255))
    rdraw = ImageDraw.Draw(run_sheet)
    rdraw.text((18, 16), "Full-run counter audit - exact V41 origins and approved neighbours", fill=INK, font=font)
    for row, (label, dishwasher) in enumerate((("CURRENT V41 RUN", current_dw), ("V2 RUN + RED V41 GHOST", candidate_dw))):
        native = checker((320, 105), 8)
        native.alpha_composite(cabinet, (20, 20))
        native.alpha_composite(dishwasher, (101, 20))
        native.alpha_composite(oven, (188, 17))
        if row == 1:
            ghost = Image.new("RGBA", current_dw.size, (235, 35, 70, 0))
            ghost.putalpha(current_dw.getchannel("A").point(lambda value: round(value * 0.32)))
            native.alpha_composite(ghost, (101, 20))
        enlarged = native.resize((1280, 420), Image.Resampling.NEAREST)
        y = 55 + row * 360
        run_sheet.alpha_composite(enlarged.crop((0, 0, 1280, 320)), (18, y))
        rdraw.text((20, y + 326), label, fill=INK, font=font)
    run_path = EVIDENCE / "dishwasher-worktop-run-ghost.png"
    run_sheet.save(run_path, optimize=True)
    return [contact_path, panel_path, tiny_path, run_path]


def review_html() -> str:
    buttons = "".join(f'<button data-state="{state}">{state.title()}</button>' for state in ("off", "on", "broken"))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dishwasher Ligne-Claire V2</title><style>:root{{--ink:#061721;--paper:#fff9e8;--cream:#f1ddb2;--sea:#53b1b5;--orange:#f47b19}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:22px}}header{{border-bottom:4px solid var(--ink)}}.tag,button{{border:2px solid var(--ink);background:var(--orange);padding:7px 12px;font:inherit;font-weight:750}}button.active{{background:var(--sea)}}.panel{{background:var(--paper);border:2px solid var(--ink);margin:18px 0;padding:15px}}.views{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}}.stage{{position:relative;min-height:360px;background:repeating-conic-gradient(#eee6cf 0 25%,#d9cfb2 0 50%) 50%/28px 28px;overflow:hidden}}.stage img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;image-rendering:auto}}.ghost{{filter:hue-rotate(115deg) saturate(2);opacity:.35}}article img{{display:block;width:100%;height:auto}}.warn{{border-left:6px solid #ef3328;padding-left:14px}}@media(max-width:850px){{.views{{grid-template-columns:1fr}}}}</style></head><body><header><span class="tag">IMMUTABLE V2 CANDIDATE</span> <span class="tag" id="ready">PRELOADING</span><h1>Dishwasher Ligne-Claire V2</h1><p class="warn">V1 is rejected. V41 and production remain unchanged. Registration is closed pending explicit approval.</p><p>Exact V41 fascia placements; one panel shared by all states; exact approved worktop bytes across the complete run. Only the Broken handle receives the authorised steeper angle.</p></header><main><div>{buttons} <label><input id="ghostToggle" type="checkbox" checked> V41 authority ghost</label></div><section class="panel views"><div><h2>Exact V41 authority</h2><div class="stage"><img id="current"></div></div><div><h2>V2 candidate</h2><div class="stage"><img id="candidate"></div></div><div><h2>Ghost overlay</h2><div class="stage"><img id="ghostCandidate"><img id="ghostCurrent" class="ghost"></div></div></section><article class="panel"><h2>Full-run worktop ghost</h2><img src="/keeper-review/{SET}/assets/dishwasher-worktop-run-ghost.png"></article><article class="panel"><h2>Current / candidate / ghost</h2><img src="/keeper-review/{SET}/assets/dishwasher-v41-v2-ghost.png"></article><article class="panel"><h2>Control-panel invariance</h2><img src="/keeper-review/{SET}/assets/dishwasher-control-panel-invariance.png"></article><article class="panel"><h2>64 px proof</h2><img src="/keeper-review/{SET}/assets/dishwasher-64px-proof.png"></article></main><script>const base='/keeper-review/{SET}/assets/';const names=s=>`dishwasher-${{s}}.png`;function show(s){{const a=base+'current--'+names(s),b=base+'candidate--'+names(s);current.src=a;candidate.src=b;ghostCurrent.src=a;ghostCandidate.src=b;document.querySelectorAll('[data-state]').forEach(x=>x.classList.toggle('active',x.dataset.state===s))}}document.querySelectorAll('[data-state]').forEach(x=>x.onclick=()=>show(x.dataset.state));ghostToggle.onchange=e=>ghostCurrent.style.display=e.target.checked?'block':'none';(async()=>{{const urls=[];for(const s of ['off','on','broken'])urls.push(base+'current--'+names(s),base+'candidate--'+names(s));urls.push(base+'dishwasher-v41-v2-ghost.png',base+'dishwasher-control-panel-invariance.png',base+'dishwasher-64px-proof.png',base+'dishwasher-worktop-run-ghost.png');await Promise.all(urls.map(src=>new Promise((ok,no)=>{{const i=new Image;i.onload=async()=>{{try{{await i.decode()}}catch{{}}ok()}};i.onerror=no;i.src=src}})));ready.textContent='ALL UNIQUE IMAGES DECODED';show('on')}})()</script></body></html>'''


def published_entry(source: Path, name: str) -> dict:
    stored = archive_object(source)
    return {
        "source": relative(stored),
        "sourceSha256": sha(stored),
        "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}",
    }


def write_archive(entries: list[dict]) -> None:
    page = PUBLIC / "index.html"
    mapped = {}
    base_url = "https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects"
    for item in entries:
        object_path = ROOT / item["source"]
        digest = item["sourceSha256"]
        route = "/" + item["publicAssemblyPath"].removeprefix("public/")
        mapped[route] = {
            "sha256": digest,
            "extension": object_path.suffix,
            "bytes": object_path.stat().st_size,
            "object": item["source"],
            "url": f"{base_url}/{digest[:2]}/{digest}{object_path.suffix}",
        }
    archive = {
        "version": 1,
        "set": SET,
        "page": {"path": relative(page), "sha256": sha(page), "bytes": page.stat().st_size},
        "objectsBaseUrl": base_url,
        "entries": dict(sorted(mapped.items())),
    }
    ARCHIVE_SET.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE_SET.write_text(json.dumps(archive, indent=2) + "\n")


def build() -> None:
    if PACK.exists() or PUBLIC.exists() or ARCHIVE_SET.exists():
        raise RuntimeError("refusing to overwrite immutable dishwasher V2")
    for directory in (MASTERS, CANDIDATES, EVIDENCE):
        directory.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True)

    records = []
    for state in ("off", "on", "broken"):
        for suffix, flags in SUFFIXES.items():
            filename = f"dishwasher-{state}{suffix}.png"
            source_path = SOURCE / filename
            source = Image.open(source_path).convert("RGBA")
            master = broken_master(*flags) if state == "broken" else closed_master(state, *flags)
            master_path = MASTERS / filename.replace(".png", "-master-16x.png")
            candidate_path = CANDIDATES / filename
            master.save(master_path, optimize=True)
            candidate = register(master, source)
            candidate.save(candidate_path, optimize=True)
            records.append({
                "state": state,
                "suffix": suffix,
                "filename": filename,
                "sourceFile": relative(source_path),
                "sourceSha256": sha(source_path),
                "sourcePixels": list(source.size),
                "sourceAlphaBounds": alpha_bounds(source),
                "sourceAlphaSha256": alpha_sha(source),
                "masterFile": relative(master_path),
                "masterSha256": sha(master_path),
                "masterPixels": list(master.size),
                "candidateFile": relative(candidate_path),
                "candidateSha256": sha(candidate_path),
                "candidatePixels": list(candidate.size),
                "candidateAlphaBounds": alpha_bounds(candidate),
                "candidateAlphaSha256": alpha_sha(candidate),
                "alphaExact": alpha_sha(source) == alpha_sha(candidate),
            })

    evidence = make_evidence(records)
    generated = sorted(REFERENCES.glob("*.png"))
    manifest = {
        "schema": "lighthouse-keeper/kitchen-dishwasher-ligne-claire@2",
        "set": SET,
        "created": "2026-10-22",
        "status": "immutable-review-candidate-not-approved-not-registered",
        "sourceAuthority": {
            "set": "kitchen-dishwasher-workbench-v41",
            "approval": relative(V41_APPROVAL),
            "approvalSha256": sha(V41_APPROVAL),
            "preserved": True,
        },
        "visualAuthority": {"asset": relative(OVEN), "sha256": sha(OVEN)},
        "corrections": [
            "restored exact V41 panel placement",
            "same panel geometry in every state",
            "restored tiny lamp to the right of selector",
            "removed V1 black worktop band",
            "steeper Broken handle angle explicitly authorised by Frank",
            "exact V41 approved cabinet-run worktop rows preserved byte-for-byte",
        ],
        "authorizedGeometryChange": "Broken handle right attachment rotated downward; door, carcass and all other geometry remain V41-locked",
        "records": records,
        "generatedReferences": [
            {"file": relative(item), "sha256": sha(item), "role": "visual reference only; not registered directly"}
            for item in generated
        ],
        "evidence": [{"file": relative(item), "sha256": sha(item)} for item in evidence],
        "verification": {
            "canvasExact": True,
            "alphaExact": True,
            "panelCoordinatesInvariant": True,
            "countertopRowsFourToFifteenExact": True,
            "movementAnimationInteractionHealingRuntimeChanged": False,
        },
        "registration": {
            "register": False,
            "promote": False,
            "currentSelectorChanges": [],
            "productionWrites": [],
            "approvalRequired": True,
        },
        "rollback": "Discard only this V2 pack, archive set and review shell; V1, V41 and production remain byte-for-byte unchanged.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(review_html())

    published = []
    for state in ("off", "on", "broken"):
        published.append(published_entry(SOURCE / f"dishwasher-{state}.png", f"current--dishwasher-{state}.png"))
        published.append(published_entry(CANDIDATES / f"dishwasher-{state}.png", f"candidate--dishwasher-{state}.png"))
    published.extend(published_entry(item, item.name) for item in evidence)
    registration_record = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
        "productionWrites": [],
        "candidate": {
            "manifest": {"file": relative(PACK / "manifest.json"), "sha256": sha(PACK / "manifest.json")},
            "publicShell": {"file": relative(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")},
        },
        "publishedAssets": published,
    }
    (PACK / "batch-register.json").write_text(json.dumps(registration_record, indent=2) + "\n")
    write_archive(published)
    verify()
    print("Built dishwasher V2: exact V41 alpha/canvas, invariant panel, corrected Broken handle; gate closed")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    register = json.loads((PACK / "batch-register.json").read_text())
    archive = json.loads(ARCHIVE_SET.read_text())
    if manifest["registration"]["register"] or manifest["registration"]["promote"] or register["register"] or register["promote"]:
        raise RuntimeError("registration gate opened")
    if len(manifest["records"]) != 15 or len(register["publishedAssets"]) != 10 or len(archive["entries"]) != 10:
        raise RuntimeError("incomplete dishwasher family or archive payload")
    for record in manifest["records"]:
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        if source.size != candidate.size or source.size != (98, 82):
            raise RuntimeError(f"canvas drift: {record['filename']}")
        if source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"alpha drift: {record['filename']}")
        if source.crop((0, 4, source.width, 16)).tobytes() != candidate.crop((0, 4, candidate.width, 16)).tobytes():
            raise RuntimeError(f"worktop drift: {record['filename']}")
        if sha(ROOT / record["sourceFile"]) != record["sourceSha256"] or sha(ROOT / record["candidateFile"]) != record["candidateSha256"]:
            raise RuntimeError(f"hash drift: {record['filename']}")
    for route, item in archive["entries"].items():
        object_path = ROOT / item["object"]
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(object_path) != item["sha256"]:
            raise RuntimeError(f"archive mismatch: {route}")
    page = (PUBLIC / "index.html").read_text()
    if 'src="assets/' in page or f'/keeper-review/{SET}/assets/' not in page:
        raise RuntimeError("root-absolute review delivery regression")
    print("Verified dishwasher V2: 15 exact canvases/alphas; content-addressed review; gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
