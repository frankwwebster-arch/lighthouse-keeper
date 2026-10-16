#!/usr/bin/env python3
"""Build the reversible Keeper Prime ladder-transition V1 review pack."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-ladder-transitions-v1"
PACK = ROOT / "art/drafts/keeper-prime-ladder-transitions-2026-10-16-v1"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
FRAMES = PACK / "drafts/frames"
SOURCES = PACK / "sources/generated"

APPROVED_BACK = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png"
APPROVED_BACK_MASTER = ROOT / "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/sources/keeper-prime-back-user-approved-rear-boots.png"
LEGACY_LADDER = ROOT / "art/raw/keeper-first-batch/keeper_ladder_climb_f8.png"
WALK_DIR = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames"
BRIDGE_DIR = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames"
TURN_DIR = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames"

SOURCE_FILES = {
    "contactA": SOURCES / "ladder-contact-a.png",
    "passingA": SOURCES / "ladder-passing-a.png",
    "mount": SOURCES / "ladder-mount.png",
    "dismountRight": SOURCES / "ladder-dismount-right.png",
    "dismountLanded": SOURCES / "ladder-dismount-landed.png",
}

CELL = (256, 320)
FLOOR_Y = 316
AXIS_X = 128
MASTER_AUTHORITY_HEIGHT = 1284
REGISTERED_AUTHORITY_HEIGHT = 298
REGISTRATION_SCALE = REGISTERED_AUTHORITY_HEIGHT / MASTER_AUTHORITY_HEIGHT
ART_SCALE = (24299 / 27322) ** 0.5


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def significant_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A").point(lambda value: 255 if value > 8 else 0)
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError("empty source")
    return bbox


def register_source(source: Path, target: Path) -> dict[str, object]:
    image = Image.open(source).convert("RGBA")
    bbox = significant_bbox(image)
    crop = image.crop(bbox)
    size = tuple(max(1, round(value * REGISTRATION_SCALE)) for value in crop.size)
    resized = crop.resize(size, Image.Resampling.LANCZOS)
    left = round(AXIS_X - size[0] / 2)
    top = FLOOR_Y - size[1]
    if left <= 0 or top <= 0 or left + size[0] >= CELL[0] or top + size[1] >= CELL[1]:
        raise ValueError(f"registered pose has no safety gutter: {source}")
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    output.alpha_composite(resized, (left, top))
    target.parent.mkdir(parents=True, exist_ok=True)
    output.save(target)
    return {
        "source": relative(source),
        "sourceSha256": sha256(source),
        "sourcePixels": list(image.size),
        "sourceSignificantAlphaBoundsExclusive": list(bbox),
        "registrationScale": REGISTRATION_SCALE,
        "registeredSize": list(size),
        "registeredOffset": [left, top],
        "rootInCellPixels": [AXIS_X, FLOOR_Y],
        "filter": "Lanczos",
        "creativePixelWarp": False,
    }


def mirror(source: Path, target: Path) -> None:
    image = Image.open(source).convert("RGBA")
    image.transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(target)


def publish(source: Path, label: str, records: list[dict[str, object]]) -> str:
    digest = sha256(source)
    filename = f"{label}-{digest[:16]}{source.suffix.lower()}"
    target = ASSETS / filename
    shutil.copyfile(source, target)
    url = f"/keeper-review/{SET}/assets/{filename}"
    records.append({
        "source": relative(source),
        "sourceSha256": digest,
        "published": relative(target),
        "url": url,
        "bytes": source.stat().st_size,
    })
    return url


for directory in (PUBLIC, ASSETS, FRAMES):
    directory.mkdir(parents=True, exist_ok=True)

required = [APPROVED_BACK, APPROVED_BACK_MASTER, LEGACY_LADDER, *SOURCE_FILES.values()]
required += [WALK_DIR / f"keeper_prime_walk-right_f{index}.png" for index in range(1, 9)]
required += [BRIDGE_DIR / f"keeper_prime_stop-to-walk-right_f{index}.png" for index in range(1, 5)]
required += [TURN_DIR / f"keeper_prime_turn_side-right_to_back_f{index:02}.png" for index in range(1, 10)]
for file in required:
    if not file.exists():
        raise FileNotFoundError(file)

registrations: dict[str, dict[str, object]] = {}
registered = {
    "contactA": FRAMES / "keeper_prime_ladder_contact-a_back_f01.png",
    "passingA": FRAMES / "keeper_prime_ladder_passing-a_back_f01.png",
    "mount": FRAMES / "keeper_prime_ladder_mount_back_f01.png",
    "dismountRight": FRAMES / "keeper_prime_ladder_dismount-right_back_f01.png",
    "dismountLanded": FRAMES / "keeper_prime_ladder_dismount-landed_back_f01.png",
}
for key, source in SOURCE_FILES.items():
    registrations[key] = register_source(source, registered[key])

registered["contactB"] = FRAMES / "keeper_prime_ladder_contact-b_back_f01.png"
registered["passingB"] = FRAMES / "keeper_prime_ladder_passing-b_back_f01.png"
mirror(registered["contactA"], registered["contactB"])
mirror(registered["passingA"], registered["passingB"])

published: list[dict[str, object]] = []
urls: dict[str, str] = {}
for key, file in registered.items():
    urls[key] = publish(file, key.lower(), published)
urls["back"] = publish(APPROVED_BACK, "approved-back", published)
for index in range(1, 9):
    urls[f"walk{index}"] = publish(WALK_DIR / f"keeper_prime_walk-right_f{index}.png", f"walk-{index}", published)
for index in range(1, 5):
    urls[f"bridge{index}"] = publish(BRIDGE_DIR / f"keeper_prime_stop-to-walk-right_f{index}.png", f"bridge-{index}", published)
for index in range(1, 10):
    urls[f"turn{index}"] = publish(TURN_DIR / f"keeper_prime_turn_side-right_to_back_f{index:02}.png", f"turn-{index}", published)


def frame(asset: str, x: float, y: float, duration: float, phase: str, **extra: object) -> dict[str, object]:
    return {
        "src": urls[asset],
        "sourceFrame": asset,
        "xLp": round(x, 3),
        "rootYLp": round(y, 3),
        "durationMs": duration,
        "phase": phase,
        "artScale": ART_SCALE,
        **extra,
    }


climb_assets = ["contactA", "passingA", "contactB", "passingB"]


def climb_frames(start_y: float, increments: int, x: float = 104, prefix: str = "climb") -> list[dict[str, object]]:
    result = []
    for index in range(increments + 1):
        asset = climb_assets[index % 4]
        result.append(frame(asset, x, start_y - index * 3.75, 95, f"{prefix} · {asset} · rise {index * 3.75:g} lp", rungPhase=index % 2))
    return result


walk_approach: list[dict[str, object]] = []
for index in range(32):
    asset_index = index % 8 + 1
    walk_approach.append(frame(f"walk{asset_index}", 20 + (index + 1) * 2.625, 116, 62.5, f"walk to ladder · cycle {index // 8 + 1}/4"))
walk_approach.append(frame("walk1", 104, 116, 70, "decelerate at ladder"))
for bridge_index in (4, 3, 2, 1):
    walk_approach.append(frame(f"bridge{bridge_index}", 104, 116, 70 + (4 - bridge_index) * 10, "walk → stop"))
for turn_index in range(1, 10):
    walk_approach.append(frame(f"turn{turn_index}", 104, 116, 62.5, "turn to face ladder"))
walk_approach.extend([
    frame("back", 104, 116, 80, "rear neutral at ladder"),
    frame("mount", 104, 116, 110, "first rung mount"),
])
walk_approach.extend(climb_frames(116, 8, prefix="begin climb"))

climb_continue = climb_frames(116, 20, prefix="continuous climb")

gait_loop = []
for index in range(8):
    asset = climb_assets[index % 4]
    gait_loop.append(frame(asset, 104, 96, 95, f"camera-follow gait · {asset}", ladderOffsetLp=-(index * 3.75) % 7.5))

dismount_walk = climb_frames(86, 8, prefix="last two climb cycles")
dismount_walk.extend([
    frame("dismountRight", 109, 56, 110, "right boot clears the ladder opening"),
    frame("dismountLanded", 116, 56, 120, "both feet established on landing"),
    frame("back", 122, 56, 100, "rear neutral clear of opening"),
])
for turn_index in range(9, 0, -1):
    dismount_walk.append(frame(f"turn{turn_index}", 122, 56, 62.5, "turn right toward room door"))
for bridge_index in (2, 3, 4):
    dismount_walk.append(frame(f"bridge{bridge_index}", 122, 56, 70, "stop → walk"))
for index in range(16):
    asset_index = index % 8 + 1
    dismount_walk.append(frame(f"walk{asset_index}", 122 + (index + 1) * 2.625, 56, 62.5, "walk to upper door"))

full_flow = walk_approach[:-9] + climb_frames(116, 16, prefix="climb one exact floor") + dismount_walk[9:]

spec = {
    "schema": "lighthouse-keeper/ladder-transitions@1",
    "set": SET,
    "status": "draft-awaiting-visual-review",
    "units": {"kuPerLogicalPixel": 8},
    "geometry": {
        "floorPitchLp": 60,
        "floorPitchKu": 480,
        "ladderWidthLp": 18,
        "rungPitchLp": 7.5,
        "rungPitchKu": 60,
        "rungIntervalsPerFloor": 8,
        "fullGaitCyclesPerFloor": 4,
        "doorToLadderLp": 84,
        "doorToLadderWalkingIntervals": 8,
        "climbFrameRiseLp": 3.75,
    },
    "registration": {
        "method": "one authority-derived scale for all generated masters, root-anchored in 256x320 cells; opposite phases are exact mirrors",
        "authorityScale": REGISTRATION_SCALE,
        "visibleCirculationArtScale": ART_SCALE,
        "cellPixels": list(CELL),
        "rootInCellPixels": [AXIS_X, FLOOR_Y],
        "filter": "Lanczos",
        "registrations": registrations,
    },
    "routes": {
        "gait": {"title": "1. Alternating ladder gait · camera follows", "frames": gait_loop},
        "approach": {"title": "2. Door → walk → stop → turn → climb", "frames": walk_approach},
        "continue": {"title": "3. Climb one floor and continue higher", "frames": climb_continue},
        "exit": {"title": "4. Climb → dismount → turn → walk to door", "frames": dismount_walk},
        "full": {"title": "5. Complete door-to-door ladder flow", "frames": full_flow},
    },
}

SPEC_FILE = PACK / "keeper-prime-ladder-transitions-v1.json"
write_json(SPEC_FILE, spec)

html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Keeper Prime ladder transitions V1</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1420px;margin:auto;padding:20px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}.panel{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button,select,input{font:inherit}button,select{color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled,select:disabled{opacity:.45}.readout{height:3.1em;color:#c9e4ee;font-variant-numeric:tabular-nums}.stages{display:grid;grid-template-columns:minmax(0,1fr);gap:20px}.stageScroll{overflow:auto}.stage{position:relative;overflow:hidden;background:linear-gradient(#173440,#102833);border:1px solid #496878}.stage.large{width:1032px;height:792px}.stage.game{width:688px;height:528px}.world{position:absolute;inset:0}.rail,.rung{position:absolute;background:#bd925b;border:1px solid #65482b;z-index:2}.floor{position:absolute;background:#586c78;border-top:2px solid #d0dee6;z-index:6}.door{position:absolute;background:#315363;border:2px solid #91aab6;z-index:8}.keeper{position:absolute;width:32px;height:40px;object-fit:contain;transform-origin:50% 98.75%;z-index:4}.root{position:absolute;width:1.2px;height:1.2px;border-radius:50%;background:#75e6a7;z-index:10}.cell{position:absolute;width:32px;height:40px;border:1px dashed #8ed7ff;z-index:9;pointer-events:none}.hide-guides .root,.hide-guides .cell{display:none}.progress{height:6px;background:#183746;border-radius:999px;overflow:hidden}.progress span{display:block;height:100%;background:#75e6a7}.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}.metrics article{background:#132b35;border:1px solid #31515f;border-radius:10px;padding:12px}.metrics b{display:block;font-size:1.15rem;color:#fff}.warning{color:#ffe09d}.legend{color:#bcd7e1}
</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a><h1>Keeper Prime ladder transitions V1</h1><span class="status">New reversible draft · nothing promoted</span><p>Prime-derived finished-art proposal for approach, exact eight-rung ascent, continuous climbing and a controlled upper-landing dismount.</p></header><main>
<p class="rule"><strong>Measured before drawing:</strong> 8 rung intervals × 7.5 lp = exactly 60 lp per floor. Four exact mirrored left/right gait cycles close the storey without phase remainder. The lower door is 84 lp—eight walking intervals—from the ladder.</p>
<section class="panel"><div class="controls"><label>Route <select id="route" disabled></select></label><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Frame</button><button id="next" disabled>Frame →</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox" checked> Loop</label><label><input id="guides" type="checkbox" checked> Contact guides</label><label>Speed <input id="speed" type="range" min="50" max="180" value="100"> <span id="speedLabel">100%</span></label></div><p id="loading" class="warning">Loading and decoding every unique frame before playback…</p><p id="readout" class="readout"></p><div class="progress"><span id="progress"></span></div></section>
<section class="stages"><article class="panel"><h2>Large inspection</h2><div class="stageScroll"><div class="stage large" data-scale="6"><div class="world"></div></div></div></article><article class="panel"><h2>4× logical game-design scale</h2><p class="legend">This is the 300×190 logical stage convention—not a prediction of physical centimetres on every device.</p><div class="stageScroll"><div class="stage game" data-scale="4"><div class="world"></div></div></div></article></section>
<section class="metrics"><article><b>60 lp / 480 ku</b>finished-floor pitch</article><article><b>8 × 7.5 lp</b>rung intervals per floor</article><article><b>4 complete cycles</b>equal left/right alternation</article><article><b>84 lp</b>door-to-ladder walk</article><article><b>One visible scale</b>door-hidden room/circulation handoff</article></section>
<section class="panel"><h2>What to judge</h2><p>First inspect the camera-follow gait for equal left/right work. Then inspect the approach join, the uninterrupted floor crossing, and whether the rightward top dismount reads as weight transfer rather than sliding. Ladder, Final, runtime and production remain unchanged until explicit approval.</p></section>
</main><script>
const SPEC=__SPEC__;
const routeSelect=document.getElementById('route'),stages=[...document.querySelectorAll('.stage')],controls=[...document.querySelectorAll('button,select')];let routeId='gait',index=0,timer=null,speed=1;
for(const [id,route] of Object.entries(SPEC.routes)){const option=document.createElement('option');option.value=id;option.textContent=route.title;routeSelect.append(option)}
function active(){return SPEC.routes[routeId].frames}function px(value,scale){return value*scale+'px'}
function architecture(world,scale,frame){world.innerHTML='';const add=(className,left,top,width,height)=>{const e=document.createElement('div');e.className=className;e.style.left=px(left,scale);e.style.top=px(top,scale);e.style.width=px(width,scale);e.style.height=px(height,scale);world.append(e);return e};const offset=frame.ladderOffsetLp||0;add('rail',95,4,1.5,112);add('rail',111.5,4,1.5,112);for(let y=3.5+offset;y<=116;y+=7.5)add('rung',95,y,18,1);add('floor',0,116,172,16);add('floor',0,56,95,4);add('floor',113,56,59,4);if(routeId==='approach'||routeId==='full')add('door',8,68,24,48);if(routeId==='exit'||routeId==='full')add('door',158,8,14,48)}
function renderStage(stage){const scale=Number(stage.dataset.scale),world=stage.querySelector('.world'),frame=active()[index];architecture(world,scale,frame);const img=document.createElement('img');img.className='keeper';img.src=frame.src;img.alt='Keeper ladder frame';img.style.left=px(frame.xLp-16,scale);img.style.top=px(frame.rootYLp-40,scale);img.style.width=px(32,scale);img.style.height=px(40,scale);img.style.transform=`scale(${frame.artScale})`;world.append(img);const cell=document.createElement('div');cell.className='cell';cell.style.left=px(frame.xLp-16,scale);cell.style.top=px(frame.rootYLp-40,scale);cell.style.width=px(32,scale);cell.style.height=px(40,scale);world.append(cell);const root=document.createElement('div');root.className='root';root.style.left=px(frame.xLp-.6,scale);root.style.top=px(frame.rootYLp-.6,scale);root.style.width=px(1.2,scale);root.style.height=px(1.2,scale);world.append(root)}
function render(){stages.forEach(renderStage);const frames=active(),f=frames[index];document.getElementById('readout').textContent=`${SPEC.routes[routeId].title} · F${index+1}/${frames.length} · ${f.phase} · root (${f.xLp}, ${f.rootYLp}) lp`;document.getElementById('progress').style.width=((index+1)/frames.length*100)+'%'}
function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){const frames=active();if(index>=frames.length-1){if(!document.getElementById('loop').checked)return stop();index=0}else index++;render();timer=setTimeout(tick,frames[index].durationMs/speed)}function play(){stop();if(index>=active().length-1)index=0;render();timer=setTimeout(tick,active()[index].durationMs/speed)}
routeSelect.onchange=e=>{stop();routeId=e.target.value;index=0;render();play()};document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=Math.max(0,index-1);render()};document.getElementById('next').onclick=()=>{stop();index=Math.min(active().length-1,index+1);render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};document.getElementById('guides').onchange=e=>stages.forEach(stage=>stage.classList.toggle('hide-guides',!e.target.checked));document.getElementById('speed').oninput=e=>{speed=Number(e.target.value)/100;document.getElementById('speedLabel').textContent=e.target.value+'%';if(timer)play()};
const unique=[...new Set(Object.values(SPEC.routes).flatMap(route=>route.frames.map(frame=>frame.src)))];function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}Promise.all(unique.map(preload)).then(()=>{controls.forEach(control=>control.disabled=false);document.getElementById('loading').textContent=`All ${unique.length} unique frame images decoded before playback`;render();play()}).catch(error=>{document.getElementById('loading').textContent='Playback locked: '+error.message});
</script></body></html>""".replace("__SPEC__", json.dumps(spec, separators=(",", ":")))

PAGE = PUBLIC / "index.html"
PAGE.write_text(html)

prompt_log = """# Keeper Prime ladder transitions V1 prompt log

Built-in image editing used the approved full-resolution rear Keeper as the identity, palette and rear-boot authority. Five high-resolution transparent studies were made: asymmetric contact A, compact passing A, first-rung mount, rightward upper-landing transfer and its flat-footed landing completion. Contact B and passing B are exact deterministic horizontal mirrors, not fresh generations. All sources are preserved under `sources/generated/`; registered 256 × 320 review cells use one fixed authority-derived scale and Lanczos resampling.

The legacy `keeper_ladder_climb_f8` strip is comparison provenance only. No pixels from it enter the candidate.
"""
(PACK / "PROMPT_LOG.md").write_text(prompt_log)

handoff = f"""# Keeper Prime ladder transitions V1

This reversible candidate implements the measured 60-lp straight-ladder module: eight 7.5-lp rung intervals, four full mirrored gait cycles, an exact 84-lp lower-door approach, uninterrupted continuation through the floor opening, and a rightward top dismount before the approved reverse turn and walk. It inherits Stair Transition V6's hidden-door circulation scale `{ART_SCALE:.9f}`. Nothing is promoted.

Review: `/keeper-review/{SET}/`.
"""
(PACK / "HANDOFF.md").write_text(handoff)

register = {
    "schema": "lighthouse-keeper/review-batch@1",
    "batchId": "keeper-prime-ladder-transitions-2026-10-16-v1",
    "status": "draft-awaiting-visual-review",
    "purpose": "Review finished Keeper Prime ladder approach, alternating climb, continuous-floor crossing and dismount transitions.",
    "authorities": {
        "approvedBack": {"file": relative(APPROVED_BACK), "sha256": sha256(APPROVED_BACK)},
        "approvedBackMaster": {"file": relative(APPROVED_BACK_MASTER), "sha256": sha256(APPROVED_BACK_MASTER)},
        "legacyLadderComparisonOnly": {"file": relative(LEGACY_LADDER), "sha256": sha256(LEGACY_LADDER), "usedInCandidate": False},
        "approvedWalk": {"register": "art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json", "sha256": sha256(ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json")},
        "approvedTurn": {"register": "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json", "sha256": sha256(ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json")},
        "approvedStairTransition": {"reviewSet": "keeper-prime-stair-transitions-v6", "deployCommit": "3f1f9f6", "approvedByFrankOn": "2026-10-16"},
    },
    "generatedSources": [{"role": key, "file": relative(file), "sha256": sha256(file), "pixels": list(Image.open(file).size)} for key, file in SOURCE_FILES.items()],
    "registeredFrames": [{"role": key, "file": relative(file), "sha256": sha256(file)} for key, file in registered.items()],
    "spec": {"file": relative(SPEC_FILE), "sha256": sha256(SPEC_FILE)},
    "reviewPage": {"file": relative(PAGE), "sha256": sha256(PAGE), "publicReview": f"/keeper-review/{SET}/", "preloadsAllUniqueFrames": True},
    "publishedAssets": published,
    "geometry": spec["geometry"],
    "validation": {"oppositeContactExactMirror": True, "oppositePassingExactMirror": True, "sourcePixelsPreserved": True, "productionChanged": False, "runtimeChanged": False, "finalChanged": False},
    "approvalBoundary": {"candidateApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
    "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; approved source art, prior drafts, Final and production remain unchanged.",
}
write_json(PACK / "batch-register.json", register)

print(json.dumps({
    "page": relative(PAGE),
    "registeredFrames": len(registered),
    "publishedAssets": len(published),
    "routes": {key: len(value["frames"]) for key, value in spec["routes"].items()},
    "artScale": ART_SCALE,
}, indent=2))
