#!/usr/bin/env python3
"""Build the Kitchen V6 countertop calibration gate from exact V5 rasters.

This is deliberately not the full Kitchen V6 family.  It makes three static,
review-only countertop constructions for the V5 kettle unit, cooker/hob and
sink, plus comparison overlays.  It reads no former V6 material and writes no
runtime sprite, manifest, register or game file.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
V5_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
SOURCE = ROOT / "art/source/kitchen-basic-assets-2026-10-16-v6-calibration"
RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v6-calibration"
DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v6-calibration"
PUBLIC = ROOT / "public/keeper-review/kitchen-countertop-calibration-v6"
ASSETS = PUBLIC / "assets"

DENSITY = 4
CELL_W = 21 * DENSITY
INK = (7, 27, 50, 255)
WOOD_DARK = (93, 48, 29, 255)
WOOD = (154, 86, 48, 255)
WOOD_LIGHT = (211, 138, 70, 255)
WOOD_HIGHLIGHT = (238, 174, 88, 255)
HOB = (55, 57, 70, 255)
HOB_LIGHT = (102, 105, 116, 255)
TRANSPARENT = (0, 0, 0, 0)

UNITS = {
    "obj_kettle": {
        "label": "Kettle counter",
        "file": "obj_kettle_standard_f1.png",
        "front_y": 48,
        "body_y": 56,
        "mask": [0, 40, 84, 56],
        "preserve": [14, 0, 68, 49],
        "logical": [21, 31],
        "material": "wood",
    },
    "obj_cooker": {
        "label": "Cooker / hob",
        "file": "obj_cooker_standard_f1.png",
        "front_y": 32,
        "body_y": 36,
        "mask": [0, 20, 84, 36],
        "preserve": None,
        "logical": [21, 28],
        "material": "hob",
    },
    "obj_sink": {
        "label": "Sink counter",
        "file": "obj_sink_standard_f1.png",
        "front_y": 48,
        "body_y": 56,
        "mask": [0, 40, 84, 56],
        "preserve": [14, 0, 70, 61],
        "logical": [21, 29],
        "material": "wood",
    },
}

OPTIONS = {
    "a": {"label": "A · 1 lp reveal", "depth_px": 4, "top_reveal_lp": 1.0},
    "b": {"label": "B · 1.5 lp reveal", "depth_px": 6, "top_reveal_lp": 1.5},
    "c": {"label": "C · 2 lp reveal", "depth_px": 8, "top_reveal_lp": 2.0},
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


def load_v5(stem: str) -> Image.Image:
    return Image.open(V5_RAW / UNITS[stem]["file"]).convert("RGBA")


def clear_box(image: Image.Image, box: list[int]) -> None:
    image.paste(TRANSPARENT, tuple(box))


def extend_rows_to_rectangle(region: Image.Image, x0: int = 2, x1: int = 81) -> Image.Image:
    """Keep interior V5 pixels and extend only row ends to a true rectangle."""
    out = region.copy()
    px = out.load()
    for y in range(out.height):
        opaque = [x for x in range(x0, x1 + 1) if px[x, y][3] >= 96]
        if not opaque:
            continue
        left, right = min(opaque), max(opaque)
        left_colour, right_colour = px[left, y], px[right, y]
        for x in range(x0, left):
            px[x, y] = left_colour
        for x in range(right + 1, x1 + 1):
            px[x, y] = right_colour
    return out


def wood_counter_from_v5(front_y: int, depth: int) -> Image.Image:
    """Reuse V5's polished kettle worktop and rectify only outer geometry."""
    authority = load_v5("obj_kettle")
    rear_y = front_y - depth
    out = Image.new("RGBA", authority.size, TRANSPARENT)
    out.alpha_composite(authority.crop((0, rear_y, 84, front_y)), (0, rear_y))
    out.alpha_composite(authority.crop((0, front_y, 84, front_y + 8)), (0, front_y))
    out = extend_rows_to_rectangle(out)
    d = ImageDraw.Draw(out)
    x0, x1 = 2, 81
    d.line((x0, rear_y, x1, rear_y), fill=INK, width=2)
    d.line((x0, rear_y, x0, front_y + 7), fill=INK, width=2)
    d.line((x1, rear_y, x1, front_y + 7), fill=INK, width=2)
    d.line((x0, front_y - 1, x1, front_y - 1), fill=INK, width=2)
    d.line((x0, front_y + 7, x1, front_y + 7), fill=INK, width=1)
    return out


def draw_hob(image: Image.Image, base: Image.Image, front_y: int, depth: int) -> None:
    """Rectify the V5 hob envelope while retaining its burner information."""
    d = ImageDraw.Draw(image)
    x0, x1 = 2, 81
    rear_y = front_y - depth
    d.rectangle((x0, rear_y, x1, front_y - 1), fill=HOB)
    d.line((x0 + 2, rear_y + 1, x1 - 2, rear_y + 1), fill=HOB_LIGHT, width=1)
    cy = rear_y + max(1, depth // 2)
    burner_h = max(2, depth - 2)
    for cx in (22, 61):
        d.ellipse((cx - 8, cy - burner_h // 2, cx + 8, cy + burner_h // 2), fill=(29, 31, 42, 255), outline=INK, width=1)
        d.ellipse((cx - 3, cy - 1, cx + 3, cy + 1), fill=(221, 171, 92, 255))
        d.line((cx - 9, cy - 2, cx + 9, cy + 2), fill=INK, width=1)
        d.line((cx - 9, cy + 2, cx + 9, cy - 2), fill=INK, width=1)
    if rear_y > 20:
        d.rectangle((10, 20, 73, rear_y - 1), fill=(247, 221, 165, 255))
        d.line((10, 20, 10, rear_y - 1), fill=INK, width=2)
        d.line((73, 20, 73, rear_y - 1), fill=INK, width=2)
    image.alpha_composite(base.crop((0, 32, 84, 36)), (0, 32))
    # Reassert the common straight envelope after the burner drawing.
    d = ImageDraw.Draw(image)
    d.line((x0, rear_y, x1, rear_y), fill=INK, width=2)
    d.line((x0, front_y - 1, x1, front_y - 1), fill=INK, width=2)
    d.line((x0, rear_y, x0, front_y - 1), fill=INK, width=2)
    d.line((x1, rear_y, x1, front_y - 1), fill=INK, width=2)


def make_candidate(stem: str, option: str) -> Image.Image:
    spec = UNITS[stem]
    base = load_v5(stem)
    out = base.copy()
    clear_box(out, spec["mask"])
    depth = OPTIONS[option]["depth_px"]
    if spec["material"] == "hob":
        draw_hob(out, base, spec["front_y"], depth)
    else:
        out.alpha_composite(wood_counter_from_v5(spec["front_y"], depth))
    if spec["preserve"]:
        box = tuple(spec["preserve"])
        out.alpha_composite(base.crop(box), (box[0], box[1]))
    return out


def edge_overlay(base: Image.Image, candidate: Image.Image) -> Image.Image:
    def edge(alpha: Image.Image) -> Image.Image:
        expanded = alpha.filter(ImageFilter.MaxFilter(3))
        contracted = alpha.filter(ImageFilter.MinFilter(3))
        return ImageChops.difference(expanded, contracted)

    out = Image.new("RGBA", base.size, (8, 18, 28, 255))
    red = Image.new("RGBA", base.size, (255, 91, 91, 0))
    red.putalpha(edge(base.getchannel("A")))
    cyan = Image.new("RGBA", base.size, (83, 221, 232, 0))
    cyan.putalpha(edge(candidate.getchannel("A")))
    out.alpha_composite(red)
    out.alpha_composite(cyan)
    return out


def ghost_overlay(base: Image.Image, candidate: Image.Image) -> Image.Image:
    out = Image.new("RGBA", base.size, (8, 18, 28, 255))
    old = base.copy()
    old.putalpha(old.getchannel("A").point(lambda a: round(a * 0.42)))
    tint = Image.new("RGBA", base.size, (255, 75, 108, 0))
    tint.putalpha(old.getchannel("A"))
    out.alpha_composite(tint)
    new = candidate.copy()
    new.putalpha(new.getchannel("A").point(lambda a: round(a * 0.72)))
    out.alpha_composite(new)
    return out


def seam_proof(candidate: Image.Image) -> Image.Image:
    out = Image.new("RGBA", (42 * DENSITY, candidate.height), TRANSPARENT)
    out.alpha_composite(candidate, (0, 0))
    out.alpha_composite(candidate, (21 * DENSITY, 0))
    return out


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def write_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V6 countertop calibration</title><style>
:root{color-scheme:dark;--bg:#07131c;--panel:#102630;--card:#0a1c25;--line:#365663;--ink:#f7f1dd;--muted:#adc0c7;--gold:#efb64d;--cyan:#55dde8;--red:#ff6f7d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:22px}h1,h2,h3{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.notice{border-left:4px solid var(--gold);background:#292417;padding:12px 14px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.option{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:14px 0}.grid{display:grid;grid-template-columns:repeat(3,minmax(290px,1fr));gap:12px}.unit{border:1px solid #294854;border-radius:10px;padding:10px}.compare{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;align-items:end}.well{min-height:150px;display:flex;align-items:end;justify-content:center;background:repeating-conic-gradient(#172c36 0 25%,#10232d 0 50%) 0/16px 16px;border-radius:7px;padding:8px;overflow:auto}.well img{flex:none;image-rendering:auto}.native{width:auto;height:auto}.logical{image-rendering:auto}.label{font-size:.75rem;color:var(--muted);text-align:center;margin-top:4px}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button{background:#17333f;color:var(--ink);border:1px solid #66818b;border-radius:7px;padding:7px 10px}button[aria-pressed="true"]{border-color:var(--cyan);color:var(--cyan)}button:disabled{opacity:.45}.seam{display:flex;align-items:end;justify-content:center;min-height:150px;background:#f4dbab;border-radius:8px;position:relative;overflow:auto;padding:8px}.seam img{flex:none}.seam:after{content:"bay seam";position:absolute;left:50%;top:6px;border-left:1px dashed #d7494d;height:calc(100% - 12px);color:#7c1d26;font-size:10px;padding-left:4px}.guide{position:relative}.guide:before,.guide:after{content:"";position:absolute;left:8px;right:8px;border-top:1px dashed}.guide:before{top:38%;border-color:var(--cyan)}.guide:after{top:51%;border-color:var(--gold)}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:7px;border-bottom:1px solid var(--line)}code{color:#9ce6eb}.small{font-size:.85rem;color:var(--muted)}@media(max-width:1000px){.grid{grid-template-columns:1fr}.compare{grid-template-columns:repeat(3,minmax(100px,1fr))}}@media(max-width:640px){header,main{padding:12px}.compare{grid-template-columns:1fr}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">V5 sole baseline</span><span class="tag">First gate only</span><h1>Kitchen V6 · countertop calibration</h1><p>This page stops before the full-family rebuild. Select one shared countertop construction for the ordinary counter, cooker/hob and sink.</p><p id="loading" class="notice">Preloading and decoding every comparison image… controls remain locked.</p></header><main>
<section class="panel"><h2>What is locked</h2><p>Every candidate begins from the exact Kitchen V5 standard raster. Cabinet, oven and sink fronts outside the declared countertop mask are byte-identical to V5. Bodies remain rectangular with vertical parallel sides and constant width. No former V6 pixel, source or construction is used.</p><p class="notice"><strong>Approval boundary:</strong> selecting A, B or C authorises only the countertop construction for the later full-family draft. It does not approve V5 or V6 art, and nothing here is promoted or wired into the game.</p></section>
<section class="panel"><h2>Shared construction alternatives · native 4× authoring scale</h2><p>All three use zero convergence and zero rear-edge narrowing. Front and rear edges are equal 20-lp horizontal runs; depth edges are vertical and parallel; the fascia is a common 2 lp. Each 20-lp asset remains wholly inside its exact 21-lp bay. The required 0.5-lp transparent gutter on each side therefore produces a measured straight 1-lp ownership seam—not a V-shaped gap.</p><div id="options"></div></section>
<section class="panel"><h2>Exact logical game scale</h2><p>The same candidate files are reduced by CSS to 1 screen pixel per logical pixel. No alternate raster or resampling pass is substituted.</p><div id="logical" class="grid"></div></section>
<section class="panel"><h2>Mechanical contract</h2><table><thead><tr><th>Option</th><th>Visible top</th><th>Rear/front edge</th><th>Shear</th><th>Fascia</th><th>Body</th></tr></thead><tbody id="contract"></tbody></table><p class="small">Cyan/red edge overlays expose silhouette changes; ghost overlays show the candidate over V5. The cooker burner drawing is registered only inside its declared hob mask. Animated states are deliberately not rebuilt at this gate.</p></section>
<section class="panel"><h2>SHA-256 and protected surfaces</h2><p>Every comparison records the full original V5 and candidate hash. V5, runtime sprites, the animation workbench/Final state and approved Keeper source family were measured before hand-back and are not written by this builder.</p><div id="hashes"></div><ul><li>Kitchen V5: unchanged</li><li>Runtime sprites and manifest: unchanged</li><li>Workbench/Final animation state: unchanged</li><li>Approved Keeper animation source family: unchanged</li></ul></section>
</main><script>
const DATA=__DATA__;const all=[];const collect=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))all.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const urls=[...new Set(all)];
const mk=(tag,attrs={})=>Object.assign(document.createElement(tag),attrs);const img=(src,alt,cls='native')=>mk('img',{src,alt,className:cls});
function viewSet(box,rec,mode){box.replaceChildren(img(rec[mode],`${rec.label} ${mode}`))}
function build(){const host=document.getElementById('options');for(const [key,opt] of Object.entries(DATA.options)){const sec=mk('article',{className:'option'});sec.innerHTML=`<h3>${opt.label}</h3><div class="controls"><button data-mode="candidate" aria-pressed="true">Candidate</button><button data-mode="ghost" aria-pressed="false">Ghost</button><button data-mode="edges" aria-pressed="false">Edges</button></div><div class="grid"></div><h3>Neighbour seam proof</h3><div class="seam"></div>`;const grid=sec.querySelector('.grid');for(const stem of DATA.unitOrder){const rec=opt.units[stem],card=mk('div',{className:'unit'});card.innerHTML=`<h3>${rec.label}</h3><div class="compare"><div><div class="well"></div><div class="label">Exact V5</div></div><div><div class="well"></div><div class="label">${opt.label}</div></div><div><div class="well guide"></div><div class="label">comparison</div></div></div>`;const wells=card.querySelectorAll('.well');wells[0].append(img(rec.v5,`${rec.label} V5`));wells[1].append(img(rec.candidate,`${rec.label} ${opt.label}`));viewSet(wells[2],rec,'candidate');grid.append(card)}const seam=sec.querySelector('.seam');seam.append(img(opt.seam,'Two adjacent ordinary units'));sec.querySelectorAll('button').forEach(b=>b.onclick=()=>{sec.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));grid.querySelectorAll('.unit').forEach((card,i)=>viewSet(card.querySelectorAll('.well')[2],opt.units[DATA.unitOrder[i]],b.dataset.mode))});host.append(sec)}
 const logical=document.getElementById('logical');for(const [key,opt] of Object.entries(DATA.options)){const card=mk('div',{className:'unit'});card.innerHTML=`<h3>${opt.label}</h3><div class="well"></div>`;const well=card.querySelector('.well');for(const stem of DATA.unitOrder){const rec=opt.units[stem],i=img(rec.candidate,rec.label,'logical');i.style.width=`${rec.logical[0]}px`;i.style.height=`${rec.logical[1]}px`;well.append(i)}logical.append(card)}
 const tb=document.getElementById('contract');for(const opt of Object.values(DATA.options)){const tr=mk('tr');tr.innerHTML=`<td>${opt.label}</td><td>${opt.topRevealLp} lp</td><td>20 / 20 lp</td><td>0 lp</td><td>2 lp</td><td>vertical, constant width</td>`;tb.append(tr)}const hashes=document.getElementById('hashes');for(const opt of Object.values(DATA.options)){const details=mk('details');details.innerHTML=`<summary>${opt.label}</summary><table><thead><tr><th>Unit</th><th>V5 original</th><th>V6 calibration candidate</th></tr></thead><tbody>${DATA.unitOrder.map(s=>`<tr><td>${opt.units[s].label}</td><td><code>${opt.units[s].v5Sha256}</code></td><td><code>${opt.units[s].candidateSha256}</code></td></tr>`).join('')}</tbody></table>`;hashes.append(details)}document.getElementById('loading').textContent=`All ${urls.length} unique comparison images loaded and decoded. Controls enabled.`;document.querySelectorAll('button').forEach(b=>b.disabled=false)}
document.querySelectorAll('button').forEach(b=>b.disabled=true);Promise.all(urls.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(build).catch(()=>document.getElementById('loading').textContent='One or more comparison images failed to load.');
</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html.replace("__DATA__", json.dumps(data, separators=(",", ":"))))


def main() -> None:
    for folder in (SOURCE, RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    for folder in (RAW, ASSETS):
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()

    data = {"version": 6, "status": "review-only-calibration-gate", "unitOrder": list(UNITS), "options": {}}
    records = []
    v5_urls = {}
    for stem in UNITS:
        base = load_v5(stem)
        name = f"{stem}_v5.png"
        save_png(base, ASSETS / name)
        v5_urls[stem] = f"/keeper-review/kitchen-countertop-calibration-v6/assets/{name}"

    for key, option in OPTIONS.items():
        option_data = {
            "label": option["label"],
            "depthPx": option["depth_px"],
            "topRevealLp": option["top_reveal_lp"],
            "construction": {"edgeLengthLp": 20, "shearLp": 0, "fasciaLp": 2, "rearEdgeScale": 1},
            "units": {},
        }
        candidates = {}
        for stem, spec in UNITS.items():
            base = load_v5(stem)
            candidate = make_candidate(stem, key)
            candidates[stem] = candidate
            paths = {}
            for kind, image in (
                ("candidate", candidate),
                ("ghost", ghost_overlay(base, candidate)),
                ("edges", edge_overlay(base, candidate)),
            ):
                name = f"{stem}_option_{key}_{kind}.png"
                save_png(image, RAW / name if kind == "candidate" else DRAFT / name)
                save_png(image, ASSETS / name)
                paths[kind] = f"/keeper-review/kitchen-countertop-calibration-v6/assets/{name}"
            diff = ImageChops.difference(base, candidate).getbbox()
            option_data["units"][stem] = {
                "label": spec["label"], "logical": spec["logical"], "v5": v5_urls[stem], **paths,
                "v5Sha256": sha(V5_RAW / spec["file"]),
                "candidateSha256": sha(RAW / f"{stem}_option_{key}_candidate.png"),
                "declaredChangeMaskPx": spec["mask"], "actualDifferenceBoundsPx": list(diff) if diff else None,
            }
            records.append({"stem": stem, "option": key, **option_data["units"][stem]})
        seam = seam_proof(candidates["obj_kettle"])
        seam_name = f"ordinary_counter_seam_option_{key}.png"
        save_png(seam, RAW / seam_name)
        save_png(seam, ASSETS / seam_name)
        option_data["seam"] = f"/keeper-review/kitchen-countertop-calibration-v6/assets/{seam_name}"
        data["options"][key] = option_data

    (DRAFT / "calibration-data.json").write_text(json.dumps(data, indent=2) + "\n")
    provenance = {
        "version": 6,
        "status": "review-only-calibration-gate",
        "soleVisualBaseline": "Kitchen Basic Assets V5",
        "readsFormerV6": False,
        "scope": ["obj_kettle standard", "obj_cooker standard", "obj_sink standard", "ordinary-unit seam proof"],
        "fullFamilyRebuilt": False,
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
        "protectedSnapshots": {
            "kitchenV5": tree_sha(ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
        "records": records,
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(provenance, indent=2) + "\n")
    write_page(data)
    print(json.dumps({"review": PUBLIC.relative_to(ROOT).as_posix(), "options": list(OPTIONS), "units": list(UNITS)}, indent=2))


if __name__ == "__main__":
    main()
