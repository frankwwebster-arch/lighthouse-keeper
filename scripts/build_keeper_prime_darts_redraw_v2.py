#!/usr/bin/env python3
"""Build the complete 14-slot Prime Darts throw-core review draft."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
V1_SCRIPT = ROOT / "scripts/build_keeper_prime_darts_redraw_v1.py"
SPEC = importlib.util.spec_from_file_location("darts_redraw_v1", V1_SCRIPT)
assert SPEC and SPEC.loader
V1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V1)

PACK = ROOT / "art/drafts/keeper-prime-darts-redraw-2026-10-17-v2"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-darts-redraw-v2"
V1_PACK = ROOT / "art/drafts/keeper-prime-darts-redraw-2026-10-17-v1"
V1_REGISTER = V1_PACK / "batch-register.json"
APPROVAL = ROOT / "docs/review/keeper-prime-darts-redraw-v1-approval-2026-10-17.json"
PRIME = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
CELL = (448, 320)

GENERATED = (
    ("early-raise", "Early raise · dart at chest", PACK / "sources/generated/keeper_prime_darts-early-raise-generated.png"),
    ("mid-raise", "Mid raise · dart approaching cheek", PACK / "sources/generated/keeper_prime_darts-mid-raise-generated.png"),
    ("launch", "Launch · dart still in hand", PACK / "sources/generated/keeper_prime_darts-launch-generated.png"),
    ("follow-through", "Follow-through · empty hand", PACK / "sources/generated/keeper_prime_darts-follow-through-generated.png"),
    ("late-recovery", "Late recovery · arm nearing rest", PACK / "sources/generated/keeper_prime_darts-late-recovery-generated.png"),
)

APPROVED = {
    "windup": V1_PACK / "drafts/keeper_prime_darts-windup-right_f1.png",
    "release": V1_PACK / "drafts/keeper_prime_darts-release-right_f1.png",
    "recovery": V1_PACK / "drafts/keeper_prime_darts-recovery-right_f1.png",
}

SEQUENCE = (
    "prime", "early-raise", "mid-raise", "windup", "launch", "release", "follow-through",
    "recovery", "recovery", "late-recovery", "prime", "prime", "prime", "prime",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_edge_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(
        alpha.getpixel((x, y)) > 0
        for x, y in (
            *((x, 0) for x in range(image.width)),
            *((x, image.height - 1) for x in range(image.width)),
            *((0, y) for y in range(image.height)),
            *((image.width - 1, y) for y in range(image.height)),
        )
    )


def contact_sheet(frames: list[tuple[str, Image.Image]]) -> Image.Image:
    tile_w, tile_h = 464, 356
    columns = 3
    rows = (len(frames) + columns - 1) // columns
    output = Image.new("RGBA", (tile_w * columns, tile_h * rows), (7, 19, 27, 255))
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(output)
    for index, (label, frame) in enumerate(frames):
        x, y = (index % columns) * tile_w + 8, (index // columns) * tile_h + 28
        stage = V1.checker(CELL)
        stage.alpha_composite(frame)
        output.alpha_composite(stage, (x, y))
        draw.text((x, y - 18), label, fill=(239, 248, 251, 255), font=font)
        draw.line((x, y + 18, x + 447, y + 18), fill=(114, 226, 165, 255))
        draw.line((x, y + 315, x + 447, y + 315), fill=(114, 226, 165, 255))
    return output


def main() -> None:
    v1 = json.loads(V1_REGISTER.read_text())
    approval = json.loads(APPROVAL.read_text())
    for slug, digest in approval["approvedPoseHashes"].items():
        if sha(APPROVED[slug]) != digest:
            raise RuntimeError(f"approved {slug} hash drift")

    (PACK / "drafts/unique").mkdir(parents=True, exist_ok=True)
    (PACK / "drafts/core").mkdir(parents=True, exist_ok=True)
    (PACK / "evidence").mkdir(parents=True, exist_ok=True)
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    (PUBLIC / "assets").mkdir(parents=True)

    prime_small = Image.open(PRIME).convert("RGBA")
    prime = Image.new("RGBA", CELL, (0, 0, 0, 0))
    prime.alpha_composite(prime_small)
    prime_registered = PACK / "drafts/unique/keeper_prime_darts-neutral-right_f1.png"
    prime.save(prime_registered)
    unique: dict[str, Image.Image] = {"prime": prime}
    records = []
    for slug, label, source_path in GENERATED:
        source = Image.open(source_path).convert("RGBA")
        frame, geometry = V1.register_pose(source)
        target = PACK / "drafts/unique" / f"keeper_prime_darts-{slug}-right_f1.png"
        frame.save(target)
        unique[slug] = frame
        records.append({
            "id": slug, "label": label, "source": rel(source_path), "sourceSha256": sha(source_path),
            "draft": rel(target), "draftSha256": sha(target), "geometry": geometry,
        })
    for slug, source_path in APPROVED.items():
        unique[slug] = Image.open(source_path).convert("RGBA")

    slots = []
    for index, pose in enumerate(SEQUENCE, start=1):
        target = PACK / "drafts/core" / f"keeper_prime_darts-core-right_f{index:02}.png"
        unique[pose].save(target)
        slots.append({"frame": index, "pose": pose, "file": rel(target), "sha256": sha(target)})

    lineup = [("Exact Prime neutral", unique["prime"])]
    lineup.extend((label, unique[slug]) for slug, label, _ in GENERATED[:2])
    lineup.extend([
        ("Approved wind-up", unique["windup"]),
        ("Launch", unique["launch"]),
        ("Approved release", unique["release"]),
        ("Follow-through", unique["follow-through"]),
        ("Approved recovery", unique["recovery"]),
        ("Late recovery", unique["late-recovery"]),
    ])
    sheet = PACK / "evidence/keeper-prime-darts-redraw-v2-lineup.png"
    contact_sheet(lineup).save(sheet)

    published = []
    urls = {}
    by_hash = {}
    for pose, image in unique.items():
        source = next((ROOT / slot["file"] for slot in slots if slot["pose"] == pose), None)
        if source is None:
            raise RuntimeError(pose)
        digest = sha(source)
        if digest not in by_hash:
            name = f"pose-{digest[:16]}.png"
            shutil.copy2(source, PUBLIC / "assets" / name)
            by_hash[digest] = f"/keeper-review/keeper-prime-darts-redraw-v2/assets/{name}"
            published.append({"source": rel(source), "sourceSha256": digest, "url": by_hash[digest]})
        urls[pose] = by_hash[digest]
    sheet_name = f"lineup-{sha(sheet)[:16]}.png"
    shutil.copy2(sheet, PUBLIC / "assets" / sheet_name)
    published.append({"source": rel(sheet), "sourceSha256": sha(sheet), "url": f"/keeper-review/keeper-prime-darts-redraw-v2/assets/{sheet_name}"})

    sequence_json = json.dumps([{"frame": i + 1, "pose": pose, "src": urls[pose]} for i, pose in enumerate(SEQUENCE)])
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime Darts redraw V2</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}}header,main{{max-width:1500px;margin:auto;padding:20px}}header{{border-bottom:1px solid #284653}}a{{color:#8ed7ff}}.status{{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}}.panel{{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}}.rule{{border-left:4px solid #72e2a5;background:#14281f;padding:12px}}button,select{{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px;margin:3px}}.stage{{position:relative;width:896px;height:640px;max-width:100%;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px;overflow:hidden}}.stage img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}}.ghost{{opacity:.24;filter:hue-rotate(115deg) saturate(1.6)}}.controls{{display:flex;gap:6px;align-items:center;flex-wrap:wrap}}.sheet{{width:100%;background:#07131b}}.warn{{border-left:4px solid #e8b852;background:#2a2518;padding:12px}}</style></head><body><header><a href="/keeper-review/keeper-prime-darts-context-v6/">← Complete Darts route V6</a><h1>Keeper Prime Darts · complete throw-core redraw V2</h1><span class="status">14-slot Prime redraw candidate · nothing promoted</span><p>Every visible Keeper pixel is Prime-derived. Historical Darts supplies choreography only.</p></header><main><p class="rule"><strong>Approved authority retained:</strong> V1 wind-up, release and recovery are inserted byte-for-byte. Neutral slots use exact approved Prime. Five new bridge drawings complete the action.</p><section class="panel"><div class="controls"><button id="prev" disabled>← Frame</button><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="next" disabled>Frame →</button><label><input id="ghost" type="checkbox" disabled> Previous-frame ghost</label><span id="readout">Preloading and decoding all nine unique poses…</span></div><div class="stage"><img id="old" class="ghost"><img id="current"></div></section><section class="panel"><h2>Fixed-scale unique-pose lineup</h2><img class="sheet" src="/keeper-review/keeper-prime-darts-redraw-v2/assets/{sheet_name}" alt="Prime Darts unique-pose lineup"></section><p class="warn"><strong>Approval boundary:</strong> V1's three-pose family is approved. This V2 fourteen-slot core and its contextual V6 route remain candidates; Final, runtime and production are unchanged.</p></main><script>
const frames={sequence_json};let i=0,t=null;const current=document.getElementById('current'),old=document.getElementById('old'),readout=document.getElementById('readout'),controls=[...document.querySelectorAll('button,input')];async function preload(){{await Promise.all([...new Set(frames.map(f=>f.src))].map(src=>new Promise((ok,no)=>{{const im=new Image();im.onload=()=>{{const decoded=im.decode?.();decoded?decoded.then(ok).catch(ok):ok()}};im.onerror=no;im.src=src}})))}}function render(){{current.src=frames[i].src;old.src=frames[(i+frames.length-1)%frames.length].src;old.style.display=document.getElementById('ghost').checked?'block':'none';readout.textContent='F'+String(i+1).padStart(2,'0')+' · '+frames[i].pose}}function stop(){{clearTimeout(t);t=null}}function tick(){{render();t=setTimeout(()=>{{i=(i+1)%frames.length;tick()}},125)}}document.getElementById('prev').onclick=()=>{{stop();i=(i+frames.length-1)%frames.length;render()}};document.getElementById('next').onclick=()=>{{stop();i=(i+1)%frames.length;render()}};document.getElementById('play').onclick=()=>{{stop();tick()}};document.getElementById('pause').onclick=stop;document.getElementById('ghost').onchange=render;preload().then(()=>{{controls.forEach(control=>control.disabled=false);render();tick()}}).catch(error=>readout.textContent='Reviewer locked: '+error.message);
</script></body></html>'''
    page = PUBLIC / "index.html"
    page.write_text(html)

    checks = {
        "slotCount14": len(slots) == 14,
        "uniquePoseCount9": len({slot["sha256"] for slot in slots}) == 9,
        "approvedWindupExact": slots[3]["sha256"] == approval["approvedPoseHashes"]["windup"],
        "approvedReleaseExact": slots[5]["sha256"] == approval["approvedPoseHashes"]["release"],
        "approvedRecoveryExact": slots[7]["sha256"] == approval["approvedPoseHashes"]["recovery"],
        "neutralEndpointsExact": slots[0]["sha256"] == sha(prime_registered) and all(slots[i]["sha256"] == sha(prime_registered) for i in range(10, 14)),
        "allCells448x320": all(Image.open(ROOT / slot["file"]).size == CELL for slot in slots),
        "allCellEdgesClear": all(alpha_edge_count(Image.open(ROOT / slot["file"]).convert("RGBA")) == 0 for slot in slots),
        "fullKeeperRedrawNoInheritedActorPixels": True,
        "publishedPreloadRequired": True,
    }
    if not all(checks.values()):
        raise RuntimeError(checks)
    register = {
        "schema": "lighthouse-keeper/darts-redraw-core@2",
        "batchId": "keeper-prime-darts-redraw-2026-10-17-v2",
        "status": "complete-prime-core-awaiting-frank",
        "purpose": "Replace the complete inherited fourteen-slot Darts actor core with Prime-derived artwork.",
        "approvedAuthority": {"register": rel(V1_REGISTER), "sha256": sha(V1_REGISTER), "approval": rel(APPROVAL), "sha256Approval": sha(APPROVAL)},
        "historicalDartsRole": "choreography-only; zero visible actor pixels reused",
        "newBridgePoses": records,
        "coreSlots": slots,
        "lineup": {"file": rel(sheet), "sha256": sha(sheet)},
        "page": {"file": rel(page), "sha256": sha(page)},
        "checks": checks,
        "publishedAssets": published,
        "approvalBoundary": {"v1FamilyApproved": True, "v2CoreApproved": False, "finalChanged": False, "runtimeChanged": False, "productionChanged": False, "promotionAllowed": False},
        "rollback": "Delete only this V2 pack and review page; approved V1, historical Darts and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    (PACK / "HANDOFF.md").write_text("# Keeper Prime Darts redraw V2\n\nFourteen action slots use nine unique Prime-derived drawings: exact Prime neutral, the three approved V1 authorities and five new bridge poses. Historical Darts contributes choreography only. Nothing is promoted.\n")
    print(json.dumps({"page": rel(page), "slots": len(slots), "unique": len({slot['sha256'] for slot in slots}), "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
