#!/usr/bin/env python3
"""Build a reversible three-pose Prime Keeper Darts redraw calibration pack."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-darts-redraw-2026-10-17-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-darts-redraw-v1"
PRIME_SOURCE = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/sources/keeper-prime-side-right-rigged-clean-master.png"
PRIME_PROXY = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
POSES = (
    ("windup", "Wind-up · dart beside cheek", PACK / "sources/generated/keeper_prime_darts-windup-generated.png"),
    ("release", "Release · arm extended", PACK / "sources/generated/keeper_prime_darts-release-generated.png"),
    ("recovery", "Recovery · arm lowering", PACK / "sources/generated/keeper_prime_darts-recovery-generated.png"),
)
RAW_CELL = (1122, 1402)
REGISTERED_CELL = (448, 320)
TARGET_TOP = 18
TARGET_FLOOR = 316
ALPHA_THRESHOLD = 8


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def significant_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    bounds = image.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0).getbbox()
    if bounds is None:
        raise RuntimeError("empty source")
    return bounds


def foot_axis(image: Image.Image, bounds: tuple[int, int, int, int]) -> float:
    alpha = image.getchannel("A")
    left, top, right, bottom = bounds
    scan_top = max(top, bottom - round((bottom - top) * 0.16))
    xs = []
    for y in range(scan_top, bottom):
        for x in range(left, right):
            if alpha.getpixel((x, y)) >= ALPHA_THRESHOLD:
                xs.append(x)
    if not xs:
        raise RuntimeError("no boot pixels found")
    return (min(xs) + max(xs) + 1) / 2


def register_pose(source: Image.Image) -> tuple[Image.Image, dict]:
    cleaned = source.copy()
    cleaned.putalpha(cleaned.getchannel("A").point(lambda value: 0 if value < ALPHA_THRESHOLD else value))
    bounds = significant_bounds(cleaned)
    crop = cleaned.crop(bounds)
    scale = (TARGET_FLOOR - TARGET_TOP) / crop.height
    size = (round(crop.width * scale), TARGET_FLOOR - TARGET_TOP)
    resized = crop.resize(size, Image.Resampling.LANCZOS)
    axis = foot_axis(cleaned, bounds)
    left = round(128 - (axis - bounds[0]) * scale)
    output = Image.new("RGBA", REGISTERED_CELL, (0, 0, 0, 0))
    output.alpha_composite(resized, (left, TARGET_TOP))
    out_bounds = significant_bounds(output)
    edge_alpha = sum(
        1
        for x, y in (
            *((x, 0) for x in range(output.width)),
            *((x, output.height - 1) for x in range(output.width)),
            *((0, y) for y in range(output.height)),
            *((output.width - 1, y) for y in range(output.height)),
        )
        if output.getpixel((x, y))[3]
    )
    return output, {
        "sourceCanvas": list(source.size),
        "sourceBoundsExclusive": list(bounds),
        "sourceFootAxisX": axis,
        "uniformScale": scale,
        "registeredSize": list(size),
        "registeredOffset": [left, TARGET_TOP],
        "registeredBoundsExclusive": list(out_bounds),
        "registeredFootAxisX": 128,
        "capTopY": out_bounds[1],
        "floorY": out_bounds[3] - 1,
        "edgeAlphaPixels": edge_alpha,
        "filter": "LANCZOS",
        "creativePixelWarp": False,
    }


def checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, (25, 38, 47, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(40, 55, 65, 255))
    return image


def contact_sheet(prime: Image.Image, frames: list[tuple[str, str, Image.Image]]) -> Image.Image:
    font = ImageFont.load_default()
    output = Image.new("RGBA", (4 * 480, 372), (7, 19, 27, 255))
    draw = ImageDraw.Draw(output)
    entries = [("prime", "Exact approved Prime", prime), *frames]
    for index, (_, label, frame) in enumerate(entries):
        x = index * 480 + 16
        stage = checker(REGISTERED_CELL)
        stage.alpha_composite(frame)
        output.alpha_composite(stage, (x, 36))
        draw.text((x, 12), label, fill=(239, 248, 251, 255), font=font)
        draw.line((x, 36 + TARGET_TOP, x + 447, 36 + TARGET_TOP), fill=(114, 226, 165, 255), width=1)
        draw.line((x, 36 + TARGET_FLOOR - 1, x + 447, 36 + TARGET_FLOOR - 1), fill=(114, 226, 165, 255), width=1)
    return output


def main() -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    (PACK / "drafts").mkdir(exist_ok=True)
    (PACK / "evidence").mkdir(exist_ok=True)
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    (PUBLIC / "assets").mkdir(parents=True)

    prime = Image.new("RGBA", REGISTERED_CELL, (0, 0, 0, 0))
    prime.alpha_composite(Image.open(PRIME_PROXY).convert("RGBA"), (0, 0))
    prime_padded = PACK / "evidence/keeper-prime-side-right-padded-56x40.png"
    prime.save(prime_padded)
    registered = []
    records = []
    for slug, label, source_path in POSES:
        source = Image.open(source_path).convert("RGBA")
        if source.size != RAW_CELL:
            raise RuntimeError(f"{slug} source is {source.size}, expected {RAW_CELL}")
        frame, geometry = register_pose(source)
        target = PACK / "drafts" / f"keeper_prime_darts-{slug}-right_f1.png"
        frame.save(target)
        registered.append((slug, label, frame))
        records.append({
            "id": slug,
            "label": label,
            "source": rel(source_path),
            "sourceSha256": sha(source_path),
            "draft": rel(target),
            "draftSha256": sha(target),
            "geometry": geometry,
        })

    sheet_path = PACK / "evidence/keeper-prime-darts-redraw-v1-contact-sheet.png"
    contact_sheet(prime, registered).save(sheet_path)

    publish = [("prime", prime_padded), *[(slug, PACK / "drafts" / f"keeper_prime_darts-{slug}-right_f1.png") for slug, _, _ in registered], ("contact", sheet_path)]
    urls = {}
    assets = []
    for label, source in publish:
        digest = sha(source)
        name = f"{label}-{digest[:16]}.png"
        shutil.copy2(source, PUBLIC / "assets" / name)
        urls[label] = f"/keeper-review/keeper-prime-darts-redraw-v1/assets/{name}"
        assets.append({"label": label, "source": rel(source), "sha256": digest, "url": urls[label]})

    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime Darts redraw V1</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:20px}}header{{border-bottom:1px solid #284653}}a{{color:#8ed7ff}}.status{{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}}.panel{{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}}.rule{{border-left:4px solid #72e2a5;background:#14281f;padding:12px}}button{{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px;margin:3px}}button.active{{background:#17683e;border-color:#72e2a5}}.views{{display:grid;grid-template-columns:minmax(420px,1fr) minmax(300px,520px);gap:18px}}.stage{{position:relative;aspect-ratio:7/5;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px;overflow:hidden}}.stage img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}}.ghost{{opacity:.28;filter:hue-rotate(115deg) saturate(1.6)}}.small{{width:448px;height:320px;max-width:100%}}.small img{{image-rendering:auto}}.sheet{{width:100%;background:#07131b}}.warn{{border-left:4px solid #e8b852;background:#2a2518;padding:12px}}@media(max-width:800px){{.views{{grid-template-columns:1fr}}}}
</style></head><body><header><a href="/keeper-review/keeper-prime-darts-context-v5/">← Darts tuning V5</a><h1>Keeper Prime Darts · redraw calibration V1</h1><span class="status">Three-pose drawing-family gate · not a complete animation</span><p>The historical Darts art supplies choreography only. Prime supplies every visible design decision.</p></header><main><p class="rule"><strong>What this gate answers:</strong> is this now unmistakably the same Keeper—same rotundity, broad stripe, palette, outline and shading—while throwing? If yes, the remaining in-betweens will be authored between these key poses.</p><section class="panel"><div><button data-pose="prime">Exact Prime</button><button data-pose="windup">Wind-up</button><button data-pose="release">Release</button><button data-pose="recovery">Recovery</button><label><input id="ghost" type="checkbox" checked> Exact Prime ghost</label></div><div class="views"><div><h2>Large inspection</h2><div class="stage"><img id="primeGhost" class="ghost" src="{urls['prime']}" alt="Exact Prime ghost"><img id="large" src="{urls['windup']}" alt="Selected Darts redraw pose"></div></div><div><h2>Exact registered action cell · 448 × 320</h2><div class="stage small"><img id="small" src="{urls['windup']}" alt="Selected registered pose"></div><p id="label">Wind-up · dart beside cheek</p></div></div></section><section class="panel"><h2>Fixed-scale lineup</h2><img class="sheet" src="{urls['contact']}" alt="Exact Prime and three Darts redraw calibration poses"></section><p class="warn"><strong>Approval boundary:</strong> these three new poses are a visual calibration only. They do not replace the fourteen-frame throw core, alter the contextual route, enter Final, or change runtime/production.</p></main><script>
const poses={json.dumps({slug: {"src": urls[slug], "label": label} for slug, label, _ in registered} | {"prime": {"src": urls["prime"], "label": "Exact approved Prime"}})};const large=document.getElementById('large'),small=document.getElementById('small'),label=document.getElementById('label'),ghost=document.getElementById('primeGhost');document.querySelectorAll('[data-pose]').forEach(button=>button.onclick=()=>{{const pose=poses[button.dataset.pose];large.src=pose.src;small.src=pose.src;label.textContent=pose.label;document.querySelectorAll('[data-pose]').forEach(item=>item.classList.toggle('active',item===button));}});document.getElementById('ghost').onchange=e=>ghost.style.display=e.target.checked?'block':'none';document.querySelector('[data-pose="windup"]').click();
</script></body></html>'''
    page = PUBLIC / "index.html"
    page.write_text(html)

    manifest = {
        "schema": "lighthouse-keeper/darts-redraw-calibration@1",
        "batchId": "keeper-prime-darts-redraw-2026-10-17-v1",
        "status": "three-pose-calibration-awaiting-frank",
        "purpose": "Prove a Prime-derived rendering family before authoring the complete Darts throw core.",
        "authorities": {
            "primeSource": {"file": rel(PRIME_SOURCE), "sha256": sha(PRIME_SOURCE)},
            "primeRegistered": {"file": rel(PRIME_PROXY), "sha256": sha(PRIME_PROXY)},
            "historicalDartsRole": "choreography-only",
        },
        "candidate": {"poses": records, "contactSheet": {"file": rel(sheet_path), "sha256": sha(sheet_path)}},
        "checks": {
            "poseCount": len(records),
            "allSourceCanvases1122x1402": all(record["geometry"]["sourceCanvas"] == list(RAW_CELL) for record in records),
            "allRegisteredCanvases448x320": all(Image.open(ROOT / record["draft"]).size == REGISTERED_CELL for record in records),
            "allCapTopsExact": all(record["geometry"]["capTopY"] == TARGET_TOP for record in records),
            "allFloorRowsExact": all(record["geometry"]["floorY"] == TARGET_FLOOR - 1 for record in records),
            "allEdgeAlphaZero": all(record["geometry"]["edgeAlphaPixels"] == 0 for record in records),
            "uniformWholeCharacterScalingOnly": True,
            "publishedPreloadRequired": True,
        },
        "publishedAssets": assets,
        "approvalBoundary": {"candidateApproved": False, "completeThrowCoreBuilt": False, "finalChanged": False, "runtimeChanged": False, "productionChanged": False, "promotionAllowed": False},
        "rollback": "Delete only this versioned draft directory and its review page; Prime, Darts V1-V4 and production remain unchanged.",
    }
    if not all(value is True for key, value in manifest["checks"].items() if key.startswith("all")):
        raise RuntimeError(manifest["checks"])
    dump(PACK / "batch-register.json", manifest)
    (PACK / "HANDOFF.md").write_text("# Keeper Prime Darts redraw calibration V1\n\nThree newly generated key poses use approved Prime as the sole identity and rendering authority and historical Darts only for choreography. They are uniformly registered to the exact Prime cap/floor datums. This is a visual family gate, not a complete animation or promotion.\n")
    print(json.dumps({"page": rel(page), "poses": len(records), "checks": manifest["checks"]}, indent=2))


if __name__ == "__main__":
    main()
