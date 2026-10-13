#!/usr/bin/env python3
"""Build the reversible Keeper Prime Construction Rig V1 review pack."""
from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-rig-v1"
MASTER = ROOT / "art/drafts/keeper-prime-master-2026-10-12-v1"
ORTHO_V2 = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v2"
ORTHO_V3 = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v3"
ORTHO_V5 = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5"
FRONT = MASTER / "drafts/keeper_prime_master-neutral-front_f1.png"
SIDE = ORTHO_V2 / "drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
BACK = ORTHO_V5 / "drafts/keeper_prime_master-neutral-standing-back_f1.png"
SMOOTH_BACK_MASTER = ORTHO_V5 / "sources/keeper-prime-back-user-approved-rear-boots.png"
MASTER_REGISTER = MASTER / "master-pack-register.json"
V3_REGISTER = ORTHO_V3 / "batch-register.json"
V5_REGISTER = ORTHO_V5 / "batch-register.json"

CELL = (256, 320)
DENSITY = 8
AXIS_X = 128.0
CAP_TOP = 18.0
FLOOR_Y = 316.0
ANCHOR_Y = 320.0


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def logical(value: float) -> float:
    return round(value / DENSITY, 4)


def length(a: list[float], b: list[float]) -> float:
    return round(math.hypot(b[0] - a[0], b[1] - a[1]), 4)


FRONT_JOINTS = {
    "root": [128.0, 224.0],
    "spineLower": [128.0, 202.0],
    "spineMid": [128.0, 174.0],
    "chest": [128.0, 145.0],
    "neck": [128.0, 121.0],
    "headCentre": [128.0, 83.5],
    "crown": [128.0, 18.0],
    "shoulderLeft": [82.0, 124.0],
    "elbowLeft": [63.0, 170.0],
    "wristLeft": [68.0, 203.0],
    "handLeft": [70.0, 215.0],
    "shoulderRight": [174.0, 124.0],
    "elbowRight": [193.0, 170.0],
    "wristRight": [188.0, 203.0],
    "handRight": [186.0, 215.0],
    "hipLeft": [104.0, 224.0],
    "kneeLeft": [103.0, 266.5],
    "ankleLeft": [102.0, 292.0],
    "heelLeft": [84.0, 316.0],
    "toeLeft": [112.0, 316.0],
    "hipRight": [152.0, 224.0],
    "kneeRight": [153.0, 266.5],
    "ankleRight": [154.0, 292.0],
    "heelRight": [172.0, 316.0],
    "toeRight": [144.0, 316.0],
}

SIDE_JOINTS = {
    "root": [128.0, 224.0],
    "spineLower": [128.0, 202.0],
    "spineMid": [128.0, 174.0],
    "chest": [128.0, 145.0],
    "neck": [128.0, 121.0],
    "headCentre": [132.0, 83.5],
    "crown": [128.0, 18.0],
    "shoulderNear": [119.0, 124.0],
    "elbowNear": [100.0, 170.0],
    "wristNear": [105.0, 203.0],
    "handNear": [107.0, 215.0],
    "shoulderFar": [133.0, 124.0],
    "elbowFar": [152.0, 170.0],
    "wristFar": [147.0, 203.0],
    "handFar": [145.0, 215.0],
    "hipNear": [120.0, 224.0],
    "kneeNear": [119.0, 266.5],
    "ankleNear": [118.0, 292.0],
    "heelNear": [104.0, 316.0],
    "toeNear": [150.0, 316.0],
    "hipFar": [134.0, 224.0],
    "kneeFar": [135.0, 266.5],
    "ankleFar": [136.0, 292.0],
    "heelFar": [122.0, 316.0],
    "toeFar": [162.0, 316.0],
}

BONES = [
    ("crown", "headCentre", "head-axis"),
    ("headCentre", "neck", "head-neck"),
    ("neck", "chest", "upper-spine"),
    ("chest", "spineMid", "chest-spine"),
    ("spineMid", "spineLower", "mid-spine"),
    ("spineLower", "root", "lower-spine"),
    ("neck", "shoulderLeft", "left-clavicle"),
    ("shoulderLeft", "elbowLeft", "left-upper-arm"),
    ("elbowLeft", "wristLeft", "left-forearm"),
    ("wristLeft", "handLeft", "left-hand"),
    ("neck", "shoulderRight", "right-clavicle"),
    ("shoulderRight", "elbowRight", "right-upper-arm"),
    ("elbowRight", "wristRight", "right-forearm"),
    ("wristRight", "handRight", "right-hand"),
    ("root", "hipLeft", "left-pelvis"),
    ("hipLeft", "kneeLeft", "left-thigh"),
    ("kneeLeft", "ankleLeft", "left-shin"),
    ("ankleLeft", "heelLeft", "left-rear-foot"),
    ("ankleLeft", "toeLeft", "left-front-foot"),
    ("root", "hipRight", "right-pelvis"),
    ("hipRight", "kneeRight", "right-thigh"),
    ("kneeRight", "ankleRight", "right-shin"),
    ("ankleRight", "heelRight", "right-rear-foot"),
    ("ankleRight", "toeRight", "right-front-foot"),
]

SIDE_BONES = [
    ("crown", "headCentre", "head-axis"), ("headCentre", "neck", "head-neck"),
    ("neck", "chest", "upper-spine"), ("chest", "spineMid", "chest-spine"),
    ("spineMid", "spineLower", "mid-spine"), ("spineLower", "root", "lower-spine"),
    ("neck", "shoulderNear", "near-clavicle"), ("shoulderNear", "elbowNear", "near-upper-arm"),
    ("elbowNear", "wristNear", "near-forearm"), ("wristNear", "handNear", "near-hand"),
    ("neck", "shoulderFar", "far-clavicle"), ("shoulderFar", "elbowFar", "far-upper-arm"),
    ("elbowFar", "wristFar", "far-forearm"), ("wristFar", "handFar", "far-hand"),
    ("root", "hipNear", "near-pelvis"), ("hipNear", "kneeNear", "near-thigh"),
    ("kneeNear", "ankleNear", "near-shin"), ("ankleNear", "heelNear", "near-rear-foot"),
    ("ankleNear", "toeNear", "near-front-foot"), ("root", "hipFar", "far-pelvis"),
    ("hipFar", "kneeFar", "far-thigh"), ("kneeFar", "ankleFar", "far-shin"),
    ("ankleFar", "heelFar", "far-rear-foot"), ("ankleFar", "toeFar", "far-front-foot"),
]


def bone_records(joints: dict[str, list[float]], bones: list[tuple[str, str, str]]) -> list[dict]:
    return [
        {
            "id": bone_id,
            "from": start,
            "to": end,
            "lengthSourcePixels": length(joints[start], joints[end]),
            "lengthLogical": logical(length(joints[start], joints[end])),
            "fixedLength": True,
        }
        for start, end, bone_id in bones
    ]


def joint_records(joints: dict[str, list[float]]) -> dict[str, dict]:
    return {name: {"source": point, "logical": [logical(point[0]), logical(point[1])]} for name, point in joints.items()}


def checkerboard() -> Image.Image:
    image = Image.new("RGBA", CELL, (29, 40, 49, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, CELL[1], 16):
        for x in range(0, CELL[0], 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, x + 15, y + 15), fill=(41, 55, 65, 255))
    return image


def rig_layer(joints: dict[str, list[float]], bones: list[tuple[str, str, str]], landmarks: list[dict], show_landmarks: bool = True) -> Image.Image:
    image = Image.new("RGBA", CELL, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if show_landmarks:
        for item in landmarks:
            y = int(round(item["targetY"]))
            draw.line((0, y, 255, y), fill=(247, 211, 92, 90), width=1)
    draw.line((int(AXIS_X), 0, int(AXIS_X), 319), fill=(255, 255, 255, 130), width=1)
    far = {"far-clavicle", "far-upper-arm", "far-forearm", "far-hand", "far-pelvis", "far-thigh", "far-shin", "far-rear-foot", "far-front-foot"}
    for start, end, bone_id in bones:
        colour = (120, 170, 210, 150) if bone_id in far else (54, 211, 255, 235)
        draw.line((*joints[start], *joints[end]), fill=colour, width=3)
    for name, point in joints.items():
        radius = 3 if name not in {"root", "neck", "headCentre"} else 4
        x, y = point
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(12, 20, 27, 255), outline=(255, 255, 255, 255), width=1)
    return image


def composite_evidence(art: Image.Image, overlay: Image.Image, title: str) -> Image.Image:
    stage = checkerboard()
    stage.alpha_composite(art)
    stage.alpha_composite(overlay)
    draw = ImageDraw.Draw(stage)
    draw.rectangle((0, 0, 255, 18), fill=(12, 20, 27, 220))
    draw.text((6, 5), title, fill="#ffffff", font=ImageFont.load_default())
    return stage


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], label: str, colour: str) -> None:
    draw.line((*start, *end), fill=colour, width=2)
    x1, y1 = start
    x2, y2 = end
    draw.polygon(((x1, y1), (x1 + 7, y1 - 4), (x1 + 7, y1 + 4)), fill=colour)
    draw.polygon(((x2, y2), (x2 - 7, y2 - 4), (x2 - 7, y2 + 4)), fill=colour)
    draw.text(((x1 + x2) // 2 - len(label) * 3, y1 - 13), label, fill=colour, font=ImageFont.load_default())


def measurement_sheet(front: Image.Image, overlay: Image.Image) -> Image.Image:
    output = Image.new("RGBA", (840, 420), (12, 20, 27, 255))
    stage = checkerboard()
    stage.alpha_composite(front)
    stage.alpha_composite(overlay)
    stage = stage.resize((336, 420), Image.Resampling.LANCZOS)
    output.alpha_composite(stage, (0, 0))
    draw = ImageDraw.Draw(output)
    scale = 420 / 320
    def p(x: float, y: float) -> tuple[int, int]: return (round(x * scale), round(y * scale))
    arrow(draw, p(74, 88), p(182, 88), "108px", "#ff9b54")
    arrow(draw, p(70, 135), p(186, 135), "116px", "#6ee7b7")
    arrow(draw, p(82, 205), p(174, 205), "92px", "#67e8f9")
    arrow(draw, p(104, 224), p(152, 224), "48px", "#d7a2ff")
    x = 365
    lines = [
        ("WORKING CELL", "256 × 320 (32 × 40 logical), density 8"),
        ("VERTICAL AXIS", "x=128; cap y=18; floor y=316; anchor y=320"),
        ("HEAD ENVELOPE", "111px / 13.875u wide; ear row 108px / 13.5u"),
        ("SHOULDERS", "joint span 92px / 11.5u; visible envelope 116px / 14.5u"),
        ("ARMS", "upper 49.77px; forearm 33.38px; wrist→hand 12.17px"),
        ("TORSO", "neck y=121; band base/spine-mid y=174; waist y=205"),
        ("LEGS", "thigh 42.51px; shin 25.52px; knee-band centre y=266.5"),
        ("VIEW RULE", "lengths and y-datums invariant; widths are projections"),
        ("ART RULE", "smooth high-resolution master; no raster stretching"),
    ]
    draw.text((x, 18), "KEEPER PRIME CONSTRUCTION RIG V1", fill="#ffffff", font=ImageFont.load_default())
    y = 48
    for heading, value in lines:
        draw.text((x, y), heading, fill="#77e3a4", font=ImageFont.load_default())
        draw.text((x, y + 14), value, fill="#edf5fa", font=ImageFont.load_default())
        y += 40
    return output


def orthographic_board(front: Image.Image, side: Image.Image, back: Image.Image, front_layer: Image.Image, side_layer: Image.Image, back_layer: Image.Image, landmarks: list[dict]) -> Image.Image:
    output = Image.new("RGBA", (1060, 360), (12, 20, 27, 255))
    for offset, art, layer, title in ((0, front, front_layer, "APPROVED FRONT"), (280, side, side_layer, "HISTORICAL SIDE · 5/15"), (560, back, back_layer, "APPROVED V5 BACK")):
        stage = composite_evidence(art, layer, title)
        output.alpha_composite(stage, (offset, 20))
    draw = ImageDraw.Draw(output)
    draw.text((845, 20), "INVARIANT Y-DATUMS", fill="#ffffff", font=ImageFont.load_default())
    y = 43
    for item in landmarks:
        draw.text((845, y), f"{item['targetY']:>5g}  {item['label']}", fill="#77e3a4" if item["passesCurrentSide"] else "#ff8798", font=ImageFont.load_default())
        y += 19
    return output


def copy_public(records: dict[str, Path]) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    urls: dict[str, str] = {}
    for key, source in records.items():
        target = assets / f"{key}-{digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(register: dict) -> None:
    files = {
        "front": FRONT, "side": SIDE, "back": BACK,
        "frontRig": ROOT / register["evidence"]["frontRigOverlay"]["file"],
        "sideRig": ROOT / register["evidence"]["sideTargetOverlay"]["file"],
        "backRig": ROOT / register["evidence"]["backRigOverlay"]["file"],
        "board": ROOT / register["evidence"]["orthographicBoard"]["file"],
        "measure": ROOT / register["evidence"]["measurementSheet"]["file"],
    }
    urls = copy_public(files)
    shutil.copyfile(PACK / "rig/keeper-prime-rig-v1.json", PUBLIC / "keeper-prime-rig-v1.json")
    rows = "".join(f"<tr class=\"{'pass' if item['passesCurrentSide'] else 'fail'}\"><th>{item['label']}</th><td>{item['targetY']:g}</td><td>{item['currentSideY']:g}</td><td>{item['currentSideDeltaY']:+g}</td></tr>" for item in register["verticalDatums"])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime Construction Rig V1</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--amber:#efbd58;--red:#ff8798;--green:#77e3a4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}h1,h2{{margin:.3rem 0 1rem}}.status{{display:inline-block;border:1px solid var(--amber);border-radius:999px;padding:5px 10px;color:#ffe09e}}article,.card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.wide{{width:100%}}.stack{{position:relative;width:256px;height:320px;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.stack img{{position:absolute;inset:0;width:256px;height:320px;background:none}}label{{display:flex;gap:8px;align-items:center;margin:7px 0}}input[type=range]{{width:100%}}table{{width:100%;border-collapse:collapse}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:6px}}tr.fail td:last-child{{color:var(--red)}}tr.pass td:last-child{{color:var(--green)}}#poseLab{{width:100%;max-width:520px;height:520px;background:#0c141b;border:1px solid var(--line);border-radius:8px}}.controls{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}button{{background:#243743;color:var(--ink);border:1px solid #577181;border-radius:7px;padding:8px;cursor:pointer}}.rule{{border-left:4px solid var(--green);background:#17291f;padding:10px 14px}}</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-prime-orthographic-v5/">Approved V5 rear</a><h1>Keeper Prime Construction Rig V1</h1><span class="status">Draft construction contract · awaiting rig approval</span><p>Built from the permanently approved smooth front and V5 rear. The historical side remains a design reference and visibly fails 10 of 15 invariant y-datums.</p></header><main>
<p class="rule"><strong>Rig rule:</strong> bone lengths, vertical anatomy, floor anchor and identity volumes remain fixed. Side widths are projections, not smaller anatomy. Final beard, hair and clothing are redrawn around the rig at smooth master resolution; finished raster art is never mechanically stretched.</p>
<h2>Orthographic measurement board</h2><article><img class="wide" src="assets/{urls['board']}" alt="Front, historical side and approved back with construction skeleton and horizontal datums"></article>
<h2>Overlay inspection</h2><section class="grid" id="overlayGrid">''' + ''.join(f'''<article><h3>{title}</h3><div class="stack"><img class="art" src="assets/{urls[art_key]}" alt="{title} art"><img class="rig" src="assets/{urls[rig_key]}" alt="{title} rig overlay"></div><label>Art opacity <input class="artOpacity" type="range" min="0" max="100" value="100"></label><label><input class="rigToggle" type="checkbox" checked> Skeleton and datums</label></article>''' for title, art_key, rig_key in (("Approved front", "front", "frontRig"), ("Historical side / target rig", "side", "sideRig"), ("Approved V5 back", "back", "backRig"))) + f'''</section>
<h2>Exact measurements</h2><article><img class="wide" src="assets/{urls['measure']}" alt="Keeper Prime construction measurements"></article>
<h2>Posable fixed-length lab</h2><section class="grid"><article><svg id="poseLab" viewBox="0 0 256 320" aria-label="Interactive fixed-length Keeper skeleton"></svg></article><article><p>Move the sliders: joints rotate, but the registered upper-arm, forearm, thigh and shin lengths do not change. This is a construction underlay—not finished character deformation.</p><div class="controls"><label>Arm angle <input id="armAngle" type="range" min="-65" max="65" value="0"></label><label>Elbow bend <input id="elbowBend" type="range" min="0" max="100" value="20"></label><label>Hip angle <input id="hipAngle" type="range" min="-35" max="35" value="0"></label><label>Knee bend <input id="kneeBend" type="range" min="0" max="90" value="0"></label></div><button id="resetPose">Reset neutral pose</button><p id="lengthReadout"></p></article></section>
<h2>Side validation target</h2><article><table><thead><tr><th>Datum</th><th>target y</th><th>historical side y</th><th>Δ</th></tr></thead><tbody>{rows}</tbody></table><p>The rig target is 15/15 exact. Current art is 5/15 and remains blocked. No generated side art is included in Rig V1.</p></article>
<h2>Approval boundary</h2><article><p>Approving this page accepts the construction measurements and posable underlay only. It does not promote any raw/runtime asset. The next separate review pack will use this rig to author one super-smooth 90° side endpoint and must prove 15/15 y-datum agreement before any turn frames begin.</p></article>
</main><script>
document.querySelectorAll('#overlayGrid article').forEach(card=>{{const art=card.querySelector('.art'),rig=card.querySelector('.rig'),slider=card.querySelector('.artOpacity'),toggle=card.querySelector('.rigToggle');slider.addEventListener('input',()=>art.style.opacity=String(Number(slider.value)/100));toggle.addEventListener('change',()=>rig.style.display=toggle.checked?'block':'none')}})
const svg=document.getElementById('poseLab'),ns='http://www.w3.org/2000/svg';const base={json.dumps(FRONT_JOINTS)};const L={{upper:{length(FRONT_JOINTS['shoulderRight'],FRONT_JOINTS['elbowRight'])},fore:{length(FRONT_JOINTS['elbowRight'],FRONT_JOINTS['wristRight'])},thigh:{length(FRONT_JOINTS['hipRight'],FRONT_JOINTS['kneeRight'])},shin:{length(FRONT_JOINTS['kneeRight'],FRONT_JOINTS['ankleRight'])}}};
function node(tag,attrs){{const e=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,String(v)));return e}}function end(p,len,deg){{const r=deg*Math.PI/180;return[p[0]+Math.sin(r)*len,p[1]+Math.cos(r)*len]}}
function render(){{svg.innerHTML='';svg.append(node('rect',{{x:0,y:0,width:256,height:320,fill:'#0c141b'}}));for(const y of {json.dumps([item['targetY'] for item in register['verticalDatums']])})svg.append(node('line',{{x1:0,y1:y,x2:256,y2:y,stroke:'#efbd58',opacity:.18,'stroke-width':.7}}));const a=Number(document.getElementById('armAngle').value),e=Number(document.getElementById('elbowBend').value),h=Number(document.getElementById('hipAngle').value),k=Number(document.getElementById('kneeBend').value);const j=JSON.parse(JSON.stringify(base));j.elbowRight=end(j.shoulderRight,L.upper,a);j.wristRight=end(j.elbowRight,L.fore,a-(e*.9));j.handRight=end(j.wristRight,12.1655,a-(e*.9));j.elbowLeft=end(j.shoulderLeft,L.upper,-a);j.wristLeft=end(j.elbowLeft,L.fore,-a+(e*.9));j.handLeft=end(j.wristLeft,12.1655,-a+(e*.9));j.kneeRight=end(j.hipRight,L.thigh,h);j.ankleRight=end(j.kneeRight,L.shin,h-(k*.8));j.kneeLeft=end(j.hipLeft,L.thigh,-h);j.ankleLeft=end(j.kneeLeft,L.shin,-h+(k*.8));const bones={json.dumps(BONES)};for(const [s,t] of bones)svg.append(node('line',{{x1:j[s][0],y1:j[s][1],x2:j[t][0],y2:j[t][1],stroke:'#36d3ff','stroke-width':3,'stroke-linecap':'round'}}));for(const p of Object.values(j))svg.append(node('circle',{{cx:p[0],cy:p[1],r:3,fill:'#0c141b',stroke:'#fff','stroke-width':1}}));document.getElementById('lengthReadout').textContent=`Fixed: upper arm ${{L.upper.toFixed(2)}}px · forearm ${{L.fore.toFixed(2)}}px · thigh ${{L.thigh.toFixed(2)}}px · shin ${{L.shin.toFixed(2)}}px`;}}
for(const id of ['armAngle','elbowBend','hipAngle','kneeBend'])document.getElementById(id).addEventListener('input',render);document.getElementById('resetPose').addEventListener('click',()=>{{armAngle.value=0;elbowBend.value=20;hipAngle.value=0;kneeBend.value=0;render()}});render();
</script></body></html>'''
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    required = (FRONT, SIDE, BACK, SMOOTH_BACK_MASTER, MASTER_REGISTER, V3_REGISTER, V5_REGISTER)
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {relative(path)}")
    master = json.loads(MASTER_REGISTER.read_text())
    v3 = json.loads(V3_REGISTER.read_text())
    v5 = json.loads(V5_REGISTER.read_text())
    if master.get("status") != "approved-permanent-identity-authority":
        raise RuntimeError("Prime Master authority missing")
    if v5.get("status") != "approved-rear-endpoint-authority-for-kp-rig":
        raise RuntimeError("approved V5 rear authority missing")
    if v3.get("validation", {}).get("exactLandmarkPassCount") != 5:
        raise RuntimeError("V3 side audit changed")
    for directory in (PACK / "rig", PACK / "overlays", PACK / "evidence", PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    landmarks = [
        {"id": item["id"], "label": item["label"], "targetY": item["frontY"], "targetLogicalY": logical(item["frontY"]), "currentSideY": item["sideY"], "currentSideDeltaY": item["deltaY"], "passesCurrentSide": item["passesExact"], "requiredDeltaY": 0}
        for item in v3["verticalLandmarks"]
    ]
    front = Image.open(FRONT).convert("RGBA")
    side = Image.open(SIDE).convert("RGBA")
    back = Image.open(BACK).convert("RGBA")
    front_layer = rig_layer(FRONT_JOINTS, BONES, landmarks)
    back_layer = rig_layer(FRONT_JOINTS, BONES, landmarks)
    side_layer = rig_layer(SIDE_JOINTS, SIDE_BONES, landmarks)
    front_overlay = PACK / "overlays/front-rig-only.png"
    side_overlay = PACK / "overlays/side-target-rig-only.png"
    back_overlay = PACK / "overlays/back-rig-only.png"
    front_layer.save(front_overlay, optimize=False, compress_level=9)
    side_layer.save(side_overlay, optimize=False, compress_level=9)
    back_layer.save(back_overlay, optimize=False, compress_level=9)
    front_evidence = PACK / "evidence/front-rig-overlay.png"
    side_evidence = PACK / "evidence/historical-side-target-rig-overlay.png"
    back_evidence = PACK / "evidence/back-rig-overlay.png"
    composite_evidence(front, front_layer, "APPROVED FRONT + KP RIG V1").save(front_evidence, optimize=False, compress_level=9)
    composite_evidence(side, side_layer, "HISTORICAL SIDE + TARGET RIG").save(side_evidence, optimize=False, compress_level=9)
    composite_evidence(back, back_layer, "APPROVED V5 BACK + KP RIG V1").save(back_evidence, optimize=False, compress_level=9)
    board = PACK / "evidence/orthographic-rig-board.png"
    sheet = PACK / "evidence/keeper-prime-measurement-sheet.png"
    orthographic_board(front, side, back, front_layer, side_layer, back_layer, landmarks).save(board, optimize=False, compress_level=9)
    measurement_sheet(front, front_layer).save(sheet, optimize=False, compress_level=9)
    front_bones = bone_records(FRONT_JOINTS, BONES)
    side_bones = bone_records(SIDE_JOINTS, SIDE_BONES)
    rig = {
        "rigId": "keeper-prime-construction-rig-2026-10-13-v1",
        "status": "draft-construction-contract-awaiting-visual-approval",
        "coordinateSystem": {"sourceCell": list(CELL), "logicalCell": [32, 40], "density": DENSITY, "axisX": AXIS_X, "capTopY": CAP_TOP, "opaqueFloorY": FLOOR_Y, "anchor": [128, ANCHOR_Y]},
        "frontBackInvariant": {"joints": joint_records(FRONT_JOINTS), "bones": front_bones},
        "sideRightProjection": {"joints": joint_records(SIDE_JOINTS), "bones": side_bones, "rule": "vertical anatomy and segment lengths remain invariant; x positions and visible depth are projected"},
        "invariantSegmentLengths": {"upperArm": length(FRONT_JOINTS["shoulderRight"], FRONT_JOINTS["elbowRight"]), "forearm": length(FRONT_JOINTS["elbowRight"], FRONT_JOINTS["wristRight"]), "wristToPalmCentre": length(FRONT_JOINTS["wristRight"], FRONT_JOINTS["handRight"]), "thigh": length(FRONT_JOINTS["hipRight"], FRONT_JOINTS["kneeRight"]), "shin": length(FRONT_JOINTS["kneeRight"], FRONT_JOINTS["ankleRight"])},
        "bodyVolumeEnvelopes": {
            "head": {"frontBoundsExclusive": [73, 18, 184, 149], "frontWidth": 111, "earToEarAtY88": [74, 182], "earToEarWidth": 108},
            "shoulders": {"datumY": 121, "jointSpan": [82, 174], "jointWidth": 92, "visibleEnvelopeAtY135": [70, 186], "visibleWidth": 116},
            "torso": {"chestBandBoundsExclusive": [48, 145, 208, 178], "coreWidthAtY205": [82, 174], "coreWidth": 92, "waistY": 205},
            "pelvis": {"hipJointSpan": [104, 152], "jointWidth": 48, "rootY": 224},
            "beard": {"frontBoundsExclusive": [86, 82, 171, 149], "baseY": 149, "redrawAroundRig": True},
        },
        "verticalDatums": landmarks,
        "poseLimitsDegrees": {"shoulder": [-65, 65], "elbowBend": [0, 100], "hip": [-35, 35], "kneeBend": [0, 90], "neckTurn": [-90, 90]},
        "occlusionOrder": {"front": ["far-limbs", "torso", "near-limbs", "beard-hair", "face", "props"], "sideRight": ["far-limbs", "torso", "far-hair", "near-limbs", "near-beard", "face", "props"], "back": ["far-limbs", "torso", "near-limbs", "rear-hair", "props"]},
        "contacts": {"floor": {"y": FLOOR_Y, "anchorY": ANCHOR_Y}, "leftPalm": FRONT_JOINTS["handLeft"], "rightPalm": FRONT_JOINTS["handRight"], "seatReference": [128, 233], "propGripRadius": 7},
        "renderQuality": {"smoothHighResolutionMasterRequired": True, "nearestNeighbourMasterResizeAllowed": False, "registeredProxyResampling": "LANCZOS", "roughOuterEdgesAllowed": False, "jaggedInternalLineworkAllowed": False, "finishedRasterMechanicalStretchAllowed": False},
        "approvalBoundary": {"rigApprovalAllowsSideAuthoring": True, "productionPromotionAllowed": False, "animationAuthoringAllowed": False},
    }
    rig_path = PACK / "rig/keeper-prime-rig-v1.json"
    dump(rig_path, rig)
    register = {
        "batchId": rig["rigId"], "status": rig["status"], "purpose": "Create the fixed, posable Keeper Prime measurement foundation before any side correction or animation redraw.",
        "authorities": {
            "front": {"file": relative(FRONT), "sha256": digest(FRONT), "register": relative(MASTER_REGISTER), "registerSha256": digest(MASTER_REGISTER)},
            "back": {"file": relative(BACK), "sha256": digest(BACK), "smoothMaster": relative(SMOOTH_BACK_MASTER), "smoothMasterSha256": digest(SMOOTH_BACK_MASTER), "register": relative(V5_REGISTER), "registerSha256": digest(V5_REGISTER)},
            "historicalSideDesign": {"file": relative(SIDE), "sha256": digest(SIDE), "register": relative(V3_REGISTER), "registerSha256": digest(V3_REGISTER), "landmarkPasses": 5, "landmarkTotal": 15},
        },
        "rig": {"file": relative(rig_path), "sha256": digest(rig_path)},
        "verticalDatums": landmarks,
        "measurements": {"sourcePixels": {"overallOpaqueHeight": 298, "headEnvelopeWidth": 111, "earToEarOuter": 108, "shoulderJointSpan": 92, "shoulderVisibleEnvelope": 116, "waistCoreWidth": 92, "hipJointSpan": 48}, "logicalUnits": {"overallOpaqueHeight": logical(298), "headEnvelopeWidth": logical(111), "earToEarOuter": logical(108), "shoulderJointSpan": logical(92), "shoulderVisibleEnvelope": logical(116), "waistCoreWidth": logical(92), "hipJointSpan": logical(48)}},
        "evidence": {
            "frontRigOverlay": {"file": relative(front_overlay), "sha256": digest(front_overlay)},
            "sideTargetOverlay": {"file": relative(side_overlay), "sha256": digest(side_overlay)},
            "backRigOverlay": {"file": relative(back_overlay), "sha256": digest(back_overlay)},
            "frontComposite": {"file": relative(front_evidence), "sha256": digest(front_evidence)},
            "sideComposite": {"file": relative(side_evidence), "sha256": digest(side_evidence)},
            "backComposite": {"file": relative(back_evidence), "sha256": digest(back_evidence)},
            "orthographicBoard": {"file": relative(board), "sha256": digest(board)},
            "measurementSheet": {"file": relative(sheet), "sha256": digest(sheet)},
        },
        "validation": {"frontBackJointIdentity": True, "mirroredArmLengthsExact": True, "mirroredLegLengthsExact": True, "sideNearFarLongSegmentLengthsExact": True, "allTargetDatumsUseApprovedFrontY": True, "targetLandmarkPassCount": 15, "targetLandmarkTotal": 15, "historicalSidePassCount": 5, "historicalSideBlocked": True, "smoothMasterRequired": True, "productionSpritesChanged": False, "runtimeManifestChanged": False, "animationDraftsChanged": False},
        "nextGate": "Approve KP Rig V1, then author one separate super-smooth side-right endpoint with 15/15 exact y-datums.",
        "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; all authorities, production sprites and manifests remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write_page(register)
    print(json.dumps({"batch": register["batchId"], "frontBones": len(front_bones), "sideBones": len(side_bones), "targetDatums": "15/15", "historicalSide": "5/15", "publicPage": relative(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
