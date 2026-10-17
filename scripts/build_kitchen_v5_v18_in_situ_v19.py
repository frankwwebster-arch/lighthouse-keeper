#!/usr/bin/env python3
"""Build the immutable Kitchen V19 exact V5/V18 in-situ comparison.

V18 is retained as rejected evidence.  This builder does not redraw either
variant: it bottom-aligns the exact V5 and exact V18 rasters, without scaling,
inside the same neutral three-bay room function used by the V18 review.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
V5 = ROOT / "art/raw/kitchen-basic-assets-2026-10-16-v5"
V18 = ROOT / "art/raw/kitchen-countertop-gate-2026-10-17-v18"
RAW = ROOT / "art/raw/kitchen-v5-v18-in-situ-2026-10-17-v19"
DRAFT = ROOT / "art/drafts/kitchen-v5-v18-in-situ-2026-10-17-v19"
PUBLIC = ROOT / "public/keeper-review/kitchen-v5-v18-in-situ-comparison-v19"
ASSETS = PUBLIC / "assets"
V18_BUILDER = ROOT / "scripts/build_kitchen_countertop_gate_v18.py"

ORDER = ["obj_kettle", "obj_cooker", "obj_sink"]
V5_FILES = {
    "obj_kettle": "obj_kettle_standard_f1.png",
    "obj_cooker": "obj_cooker_standard_f1.png",
    "obj_sink": "obj_sink_standard_f1.png",
}
V18_FILES = {stem: f"{stem}_candidate.png" for stem in ORDER}


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


def load_room_function():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("kitchen_v18_builder", V18_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the immutable V18 room builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.neutral_room_context


def load_set(folder: Path, files: dict[str, str]) -> dict[str, Image.Image]:
    return {stem: Image.open(folder / files[stem]).convert("RGBA") for stem in ORDER}


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def write_detailed_page(data: dict) -> None:
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V19 · exact V5 in situ</title><style>
:root{color-scheme:dark;--bg:#07131c;--panel:#102630;--line:#365663;--ink:#f7f1dd;--muted:#adc0c7;--gold:#efb64d;--cyan:#55dde8;--red:#ff7883}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.48 system-ui,sans-serif}header,main{max-width:1240px;margin:auto;padding:22px}h1,h2{line-height:1.15}.tag{display:inline-block;border:1px solid var(--gold);border-radius:999px;padding:5px 10px;color:#ffd98a;margin:0 7px 7px 0}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}.notice{border-left:4px solid var(--gold);background:#292417;padding:12px 14px}.rejected{border-left-color:var(--red)}.toolbar button{background:#17333f;color:var(--ink);border:1px solid #66818b;border-radius:7px;padding:7px 10px;margin:0 5px 8px 0}.toolbar button[aria-pressed=true]{border-color:var(--cyan);color:var(--cyan)}button:disabled{opacity:.45}.well{display:flex;justify-content:center;overflow:auto;background:#091922;border-radius:10px;padding:12px}.well img{width:1008px;height:896px;flex:none;image-rendering:auto}.caption{font-size:.9rem;color:var(--muted)}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--line)}code{color:#9ce6eb;font-size:.78rem;word-break:break-all}.pass{color:#8be69b}.fail{color:#ff8993}@media(max-width:760px){header,main{padding:14px}.well{justify-content:flex-start}}
</style></head><body><header><span class="tag">Draft only</span><span class="tag">Exact pixels</span><span class="tag">No scaling</span><h1>Kitchen V19 · exact V5 in the measured room</h1><p>V5 and rejected V18 are mounted in precisely the same neutral three-bay room. The room, scale, bay positions and rear-wall foot line are identical; only the unit artwork changes.</p><p id="loading" class="notice">Preloading and decoding every review image…</p></header><main>
<section class="panel"><h2>Exact V5 · preferred basis</h2><div class="toolbar"><button data-version="v5" data-mode="clean" aria-pressed="true">Clean room</button><button data-version="v5" data-mode="guides" aria-pressed="false">Measured guides</button></div><div class="well"><img id="v5" src="__V5_ROOM__" alt="Exact V5 kettle, cooker and sink mounted in the neutral three-bay room"></div><p class="caption">Exact V5 standard frame PNGs, unaltered and unscaled. Each occupies its original 21-lp bay and is bottom-aligned to the 52-lp rear-wall foot line, leaving 4 lp of foreground floor.</p></section>
<section class="panel"><h2>Rejected V18 · same staging</h2><p class="notice rejected">V18 is retained only as immutable rejection evidence. It is not a source for the V5 view above.</p><div class="toolbar"><button data-version="v18" data-mode="clean" aria-pressed="true">Clean room</button><button data-version="v18" data-mode="guides" aria-pressed="false">Measured guides</button></div><div class="well"><img id="v18" src="__V18_ROOM__" alt="Rejected V18 kettle, cooker and sink mounted in the same neutral three-bay room"></div><p class="caption">The same 252 × 224-px room pixels, three 84-px bays, foot line and native-size placement. This makes the unit art the only visual variable.</p></section>
<section class="panel"><h2>Measured equivalence</h2><table><tbody><tr><th>Room canvas</th><td class="pass">63 × 56 lp (252 × 224 px)</td></tr><tr><th>Object placement</th><td class="pass">x = 0 / 84 / 168 px; bottom y = 208 px</td></tr><tr><th>Rear-wall junction</th><td class="pass">51 lp</td></tr><tr><th>Foreground channel</th><td class="pass">4 lp clear</td></tr><tr><th>Scaling or repainting</th><td class="pass">None</td></tr></tbody></table></section>
<section class="panel"><h2>Source identity</h2><div id="hashes"></div><p class="caption">The automated verifier pins every source SHA-256, rebuilds both composites from the shared empty room and checks every RGBA pixel. No runtime sprite, manifest, register, Keeper animation or live-game file is changed.</p></section>
</main><script>
const DATA=__DATA__;const urls=[...new Set(Object.values(DATA.rooms))];const buttons=[...document.querySelectorAll('button')];function setView(version,mode){document.getElementById(version).src=DATA.rooms[version+mode[0].toUpperCase()+mode.slice(1)];buttons.filter(b=>b.dataset.version===version).forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)))}function build(){buttons.forEach(b=>{b.disabled=false;b.onclick=()=>setView(b.dataset.version,b.dataset.mode)});const h=document.getElementById('hashes');for(const stem of DATA.order){const r=DATA.sources[stem],p=document.createElement('p');p.innerHTML=`<strong>${r.label}</strong><br>V5 <code>${r.v5Sha256}</code><br>V18 <code>${r.v18Sha256}</code>`;h.append(p)}document.getElementById('loading').textContent=`All ${urls.length} unique images loaded and decoded. Controls enabled.`}buttons.forEach(b=>b.disabled=true);Promise.all(urls.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(build).catch(()=>document.getElementById('loading').textContent='A review image failed to load.');
</script></body></html>'''
    html = html.replace("__DATA__", json.dumps(data, separators=(",", ":")))
    html = html.replace("__V5_ROOM__", data["rooms"]["v5Clean"])
    html = html.replace("__V18_ROOM__", data["rooms"]["v18Clean"])
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def write_page(data: dict) -> None:
    """Write the small production review; measured detail remains in JSON/docs."""
    clean = data["rooms"]["v5Clean"]
    guides = data["rooms"]["v5Guides"]
    html = f'''<!doctype html><meta charset=utf-8><title>Kitchen V19 · V5 in situ</title><style>body{{background:#07131c;color:#fff;font:16px system-ui}}img{{display:block;width:1008px;margin:12px 0}}</style><h1>Exact V5 · in situ</h1><p>Draft only. Native V5 kettle, cooker and sink in the measured V18 room.</p><img width=1008 src="{clean}" alt="V5 room"><h2>Measured guides</h2><img width=1008 src="{guides}" alt="V5 room guides"><p>Three 21-lp bays · 52-lp foot line · 4-lp clear foreground. V18 rejected.</p>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html)


def main() -> None:
    for folder in (RAW, DRAFT, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()

    room = load_room_function()
    v5_images = load_set(V5, V5_FILES)
    v18_images = load_set(V18, V18_FILES)
    empty = {stem: Image.new("RGBA", v5_images[stem].size, (0, 0, 0, 0)) for stem in ORDER}
    outputs = {
        "empty_room.png": room(empty, guide=False),
        "v5_room.png": room(v5_images, guide=False),
        "v5_room_guides.png": room(v5_images, guide=True),
        "v18_room.png": room(v18_images, guide=False),
        "v18_room_guides.png": room(v18_images, guide=True),
    }
    for name, image in outputs.items():
        save(image, RAW / name)
        if name != "empty_room.png":
            save(image, ASSETS / name)

    prefix = "/keeper-review/kitchen-v5-v18-in-situ-comparison-v19/assets"
    data = {
        "version": 19,
        "status": "review-only-comparison",
        "order": ORDER,
        "roomGeometry": {"logical": [63, 56], "pixels": [252, 224], "bayPx": 84, "wallFloorLp": 51, "footLineLp": 52, "foregroundLp": 4},
        "rooms": {
            "v5Clean": f"{prefix}/v5_room.png",
            "v5Guides": f"{prefix}/v5_room_guides.png",
            "v18Clean": f"{prefix}/v18_room.png",
            "v18Guides": f"{prefix}/v18_room_guides.png",
        },
        "sources": {},
    }
    labels = {"obj_kettle": "Kettle counter", "obj_cooker": "Cooker / hob", "obj_sink": "Sink counter"}
    for stem in ORDER:
        data["sources"][stem] = {
            "label": labels[stem],
            "v5File": V5_FILES[stem],
            "v18File": V18_FILES[stem],
            "v5Sha256": sha(V5 / V5_FILES[stem]),
            "v18Sha256": sha(V18 / V18_FILES[stem]),
        }
    (DRAFT / "comparison-data.json").write_text(json.dumps(data, indent=2) + "\n")
    register = {
        "version": 19,
        "status": "review-only-comparison",
        "decision": "V18 rejected; exact V5 preferred for this comparison",
        "sameRoomFunction": "scripts/build_kitchen_countertop_gate_v18.py::neutral_room_context",
        "sourcePixelsAltered": False,
        "sourcePixelsScaled": False,
        "roomRebuilt": False,
        "fullFamilyRebuilt": False,
        "runtimeChanged": False,
        "finalChanged": False,
        "keeperChanged": False,
        "protectedSnapshots": {
            "kitchenV5": tree_sha(V5),
            "kitchenV18Raw": tree_sha(V18),
            "kitchenV17": tree_sha(ROOT / "art/raw/kitchen-v5-exact-rollback-2026-10-17-v17"),
            "runtimeSpriteManifest": sha(ROOT / "public/sprites/manifest.json"),
            "animationWorkbenchFinalState": sha(ROOT / "data/keeper_animation_workbench.json"),
            "approvedKeeperSourceFamily": tree_sha(ROOT / "art/raw/keeper-first-batch"),
        },
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_page(data)
    print(json.dumps({"review": PUBLIC.relative_to(ROOT).as_posix(), "comparison": "exact V5 versus rejected V18"}, indent=2))


if __name__ == "__main__":
    main()
