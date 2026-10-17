#!/usr/bin/env python3
"""Build V17 as a byte-exact, review-only rollback to Kitchen V5."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = ROOT / "data/kitchen_v5_exact_rollback_v17_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
V5_RAW = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
V5_DRAFT = ROOT / "art/drafts/kitchen-basic-assets-2026-10-16-v5"
V5_SET = ROOT / "review-archive/sets/kitchen-basic-assets-v5.json"
RAW = ROOT / "art/raw/kitchen-v5-exact-rollback-2026-10-17-v17"
DRAFT = ROOT / "art/drafts/kitchen-v5-exact-rollback-2026-10-17-v17"
PUBLIC = ROOT / "public/keeper-review/kitchen-v5-exact-rollback-v17"
ASSETS = PUBLIC / "assets"
ROUTE = "/keeper-review/kitchen-v5-exact-rollback-v17"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(directory: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path for path in directory.rglob("*") if path.is_file()):
        digest.update(item.relative_to(directory).as_posix().encode())
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def reset(directory: Path) -> None:
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True)


def rewrite_urls(value, replacements: dict[str, str]):
    if isinstance(value, str):
        return replacements.get(value, value)
    if isinstance(value, list):
        return [rewrite_urls(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: rewrite_urls(item, replacements) for key, item in value.items()}
    return value


def write_page(data: dict, media_count: int) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V17 · exact V5 rollback</title><style>:root{color-scheme:dark;--bg:#06131c;--panel:#102630;--card:#091b24;--line:#365663;--ink:#f7f1dd;--gold:#efb64d;--good:#7ee0a6}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}header,main{max-width:1560px;margin:auto;padding:22px}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin-right:7px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}.alpha{background:repeating-conic-gradient(#33434b 0 25%,#203039 0 50%) 0/20px 20px;padding:8px;overflow:auto}.sprite{display:block;width:252px;max-width:100%;height:auto;margin:auto;image-rendering:pixelated}.room{display:block;min-width:772px;width:100%;height:auto;image-rendering:pixelated}.shell{display:block;width:100%;min-width:220px;height:auto;image-rendering:pixelated}.notice{border-left:4px solid var(--gold);background:#2a2518;padding:12px}.good{color:var(--good)}button,select{background:#17323e;color:var(--ink);border:1px solid #627d87;border-radius:7px;padding:7px 10px}button:disabled,select:disabled{opacity:.45}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}</style></head><body><header><span class="tag">Draft only</span><span class="tag">Exact V5 bytes</span><span class="tag">No Option B</span><h1>Kitchen V17 · complete rollback to V5</h1><p>This page contains no redrawn or reconstructed kitchen art. All ten asset families, every state/frame, all room pieces and both room compositions are byte-identical copies of Kitchen V5. V6–V16 are rejected provenance only.</p><p id="loading" class="notice">Preloading and decoding all __MEDIA_COUNT__ exact V5 review images… controls remain locked.</p></header><main><section class="panel"><h2>Complete V5 family</h2><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><span id="readout"></span></div><div id="family" class="grid"></div></section><section class="panel"><h2>V5 room compositions</h2><h3>Nine-bay starting kitchen</h3><div class="alpha"><img class="room" src="__ROOM9__"></div><h3>Twelve-bay outline</h3><div class="alpha"><img class="room" src="__ROOM12__"></div></section><section class="panel"><h2>V5 room pieces</h2><div class="grid"><article class="card"><h3>Stair-side cap</h3><div class="alpha"><img class="shell" src="__STAIR__"></div></article><article class="card"><h3>21 × 56 repeat</h3><div class="alpha"><img class="shell" src="__REPEAT__"></div></article><article class="card"><h3>Far wall closed</h3><div class="alpha"><img class="shell" src="__FAR_CLOSED__"></div></article><article class="card"><h3>Far wall open</h3><div class="alpha"><img class="shell" src="__FAR_OPEN__"></div></article></div></section><section class="panel"><p class="notice"><strong>Binding gate:</strong> V17 raw files, review images, metadata, bounds, anchors, interaction spots, state timing and room compositions must match V5 exactly. URL prefixes are the only permitted difference. Nothing is approved, promoted or wired.</p></section></main><script>const DATA=__DATA__;let n=0,timer=null;const cards={};const urls=[];const prefix='/keeper-review/kitchen-v5-exact-rollback-v17/assets/';const collect=v=>{if(typeof v==='string'&&v.startsWith(prefix))urls.push(v);else if(Array.isArray(v))v.forEach(collect);else if(v&&typeof v==='object')Object.values(v).forEach(collect)};collect(DATA);const unique=[...new Set(urls)];function render(){let max=1;for(const [name,card] of Object.entries(cards)){const frames=DATA.assets[name].states[card.select.value].urls;max=Math.max(max,frames.length);card.img.src=frames[n%frames.length]}readout.textContent=`Frame ${n+1} / ${max}`}function stop(){if(timer)clearInterval(timer);timer=null}function start(){stop();timer=setInterval(()=>{n=(n+1)%4;render()},220)}function setup(){for(const [name,spec] of Object.entries(DATA.assets)){const card=document.createElement('article');card.className='card';const title=document.createElement('h3');title.textContent=spec.label;const select=document.createElement('select');for(const state of Object.keys(spec.states)){const option=document.createElement('option');option.value=option.textContent=state;select.append(option)}const alpha=document.createElement('div');alpha.className='alpha';const img=document.createElement('img');img.className='sprite';alpha.append(img);const status=document.createElement('p');status.className='good';status.textContent='Exact V5 bytes';card.append(title,select,alpha,status);family.append(card);cards[name]={select,img};select.onchange=()=>{n=0;render()}}play.disabled=pause.disabled=false;play.onclick=start;pause.onclick=stop;render();start();loading.textContent=`All ${unique.length} exact V5 images loaded and decoded. Controls enabled; playback started.`}Promise.all(unique.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=`Media failed: ${e.message}`);</script></body></html>'''
    replacements = {
        "__MEDIA_COUNT__": str(media_count),
        "__ROOM9__": data["room9"],
        "__ROOM12__": data["room12"],
        "__STAIR__": data["stairCap"],
        "__REPEAT__": data["repeat"],
        "__FAR_CLOSED__": data["farClosed"],
        "__FAR_OPEN__": data["farOpen"],
        "__DATA__": json.dumps(data, separators=(",", ":")),
    }
    for needle, replacement in replacements.items():
        html = html.replace(needle, replacement)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    for directory in (RAW, DRAFT, PUBLIC):
        reset(directory)
    shutil.copytree(V5_RAW, RAW, dirs_exist_ok=True, copy_function=shutil.copy2)

    source_manifest = json.loads(V5_SET.read_text())
    replacements: dict[str, str] = {}
    source_map: dict[str, dict] = {}
    for source_url, entry in sorted(source_manifest["entries"].items()):
        name = Path(source_url).name
        target_url = f"{ROUTE}/assets/{name}"
        source_object = ROOT / entry["object"]
        target = ASSETS / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_object, target)
        if sha(target) != entry["sha256"]:
            raise ValueError(f"copy hash mismatch: {target_url}")
        replacements[source_url] = target_url
        source_map[target_url] = {
            "sourceUrl": source_url,
            "sourceObject": entry["object"],
            "sha256": entry["sha256"],
            "bytes": entry["bytes"],
        }

    v5_data = json.loads((V5_DRAFT / "review-data.json").read_text())
    review_data = rewrite_urls(v5_data, replacements)
    (DRAFT / "review-data.json").write_text(json.dumps(review_data, indent=2) + "\n")
    (DRAFT / "source-map.json").write_text(json.dumps(source_map, indent=2) + "\n")
    write_page(review_data, len(source_map))

    register = {
        "version": 17,
        "status": "reversible-review-draft",
        "scope": "complete-byte-exact-v5-rollback",
        "recipe": {"path": RECIPE_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RECIPE_PATH)},
        "v5RawTreeSha256": tree_sha(V5_RAW),
        "rollbackRawTreeSha256": tree_sha(RAW),
        "v5ReviewDataSha256": sha(V5_DRAFT / "review-data.json"),
        "v5ReviewSetSha256": sha(V5_SET),
        "copiedReviewImages": len(source_map),
        "runtimeSpriteManifestSha256": sha(ROOT / "public/sprites/manifest.json"),
        "animationWorkbenchFinalStateSha256": sha(ROOT / "data/keeper_animation_workbench.json"),
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"set": RECIPE["id"], "rawTreeExact": register["v5RawTreeSha256"] == register["rollbackRawTreeSha256"], "copiedReviewImages": len(source_map), "review": PUBLIC.relative_to(ROOT).as_posix()}, indent=2))


if __name__ == "__main__":
    main()
