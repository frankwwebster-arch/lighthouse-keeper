#!/usr/bin/env python3
"""Assemble the immutable all-kitchen V43 review without registering assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VERSION = int(os.environ.get("KITCHEN_COMPLETE_REVIEW_VERSION", "43"))
SET = f"kitchen-ligne-claire-complete-review-v{VERSION}"
PACK = ROOT / f"art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v{VERSION}"
PUBLIC = ROOT / "public/keeper-review" / SET
V42_PACK = ROOT / "art/drafts/kitchen-ligne-claire-healing-workbench-2026-10-22-v42"
V42_PAGE = ROOT / "public/keeper-review/kitchen-ligne-claire-healing-workbench-v42/index.html"
INK = (5, 24, 36)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_sha(im: Image.Image) -> str:
    return hashlib.sha256(im.getchannel("A").tobytes()).hexdigest()


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def checker(size: tuple[int, int], cell: int = 14) -> Image.Image:
    out = Image.new("RGBA", size, (246, 240, 220, 255)); d = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2: d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def record(family: str, filename: str, source: str, candidate: str, authority: str, approval: str | None = None) -> dict:
    sp, cp = ROOT / source, ROOT / candidate
    si, ci = Image.open(sp).convert("RGBA"), Image.open(cp).convert("RGBA")
    return {
        "family": family, "filename": filename, "authority": authority, "approval": approval,
        "sourceFile": source, "sourceSha256": sha(sp), "candidateFile": candidate, "candidateSha256": sha(cp),
        "sourcePixels": list(si.size), "candidatePixels": list(ci.size),
        "sourceAlphaBounds": list(si.getchannel("A").getbbox() or (0, 0, 0, 0)), "candidateAlphaBounds": list(ci.getchannel("A").getbbox() or (0, 0, 0, 0)),
        "sourceAlphaSha256": alpha_sha(si), "candidateAlphaSha256": alpha_sha(ci),
        "canvasExact": si.size == ci.size, "alphaBoundsExact": si.getchannel("A").getbbox() == ci.getchannel("A").getbbox(),
        "alphaExact": alpha_sha(si) == alpha_sha(ci),
    }


def collect() -> tuple[list[dict], list[dict], list[dict]]:
    objects: list[dict] = []; effects: list[dict] = []; contracts: list[dict] = []
    approval_fitted = "docs/review/kitchen-fitted-cabinet-ligne-claire-v3-approval-2026-10-21.json"
    approval_oven = "docs/review/kitchen-oven-ligne-claire-v8-approval-2026-10-21.json"
    approval_broken = "docs/review/kitchen-oven-broken-ligne-claire-v12-approval-2026-10-22.json"

    fitted_path = "art/drafts/kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3/manifest.json"; fitted = load(fitted_path)
    contracts.append({"role": "approved fitted geometry/palette/healing", "file": fitted_path, "sha256": sha(ROOT / fitted_path), "approval": approval_fitted, "approvalSha256": sha(ROOT / approval_fitted)})
    for a in fitted["assets"]: objects.append(record(a["family"], a["filename"], a["sourceFile"], a["candidateFile"], fitted["set"], approval_fitted))

    on_path = "art/drafts/kitchen-oven-ligne-claire-2026-10-21-v8/manifest.json"; on = load(on_path)
    contracts.append({"role": "approved oven On visual", "file": on_path, "sha256": sha(ROOT / on_path), "approval": approval_oven, "approvalSha256": sha(ROOT / approval_oven)})
    objects.append(record("oven", "oven-on.png", on["sourceFile"], on["candidateFile"], on["set"], approval_oven))
    off_path = "art/drafts/kitchen-oven-off-ligne-claire-2026-10-22-v13/manifest.json"; off = load(off_path)
    objects.append(record("oven", "oven-off.png", off["source"]["file"], off["candidate"]["file"], off["set"]))
    broken_path = "art/drafts/kitchen-oven-broken-ajar-ligne-claire-2026-10-22-v15/manifest.json"; broken = load(broken_path)
    contracts.append({"role": "approved V12 body plus requested ajar-door V15 candidate", "file": broken_path, "sha256": sha(ROOT / broken_path), "approval": approval_broken, "approvalSha256": sha(ROOT / approval_broken)})
    for a in broken["assets"]:
        target = effects if a["frames"] > 1 else objects
        if target is objects: target.append(record("oven", a["filename"], a["sourceFile"], a["candidateFile"], broken["set"], approval_broken))
        else: effects.append({"family": "oven", "filename": a["filename"], "sourceFile": a["sourceFile"], "sourceSha256": a["sourceSha256"], "candidateFile": a["candidateFile"], "candidateSha256": a["candidateSha256"], "pixels": a["pixels"], "cellPixels": a["cellPixels"], "frames": a["frames"], "fps": a["fps"], "byteExact": a["sourceSha256"] == a["candidateSha256"], "authority": broken["set"]})
    symbol = broken["optionalBrokenSymbolEffect"]["file"]
    effects.append({"family": "oven", "filename": Path(symbol).name, "sourceFile": symbol, "sourceSha256": sha(ROOT / symbol), "candidateFile": symbol, "candidateSha256": sha(ROOT / symbol), "pixels": list(Image.open(ROOT / symbol).size), "frames": 1, "fps": None, "byteExact": True, "authority": broken["set"], "separateRemovableLayer": True})

    dw_path = "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v1/manifest.json"; dw = load(dw_path)
    contracts.append({"role": "dishwasher states and healing variants", "file": dw_path, "sha256": sha(ROOT / dw_path), "approval": None})
    for a in dw["records"]: objects.append(record("dishwasher", a["filename"], a["sourceFile"], a["candidateFile"], dw["set"]))
    for model in ("compact", "regular", "emphatic"):
        source = f"art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-dishwasher-suds--{model}-f40.png"
        im = Image.open(ROOT / source)
        effects.append({"family": "dishwasher", "filename": Path(source).name, "sourceFile": source, "sourceSha256": sha(ROOT / source), "candidateFile": source, "candidateSha256": sha(ROOT / source), "pixels": list(im.size), "cellPixels": [112, 104], "frames": 40, "fps": 4, "byteExact": True, "authority": "approved V41 runtime"})

    singles = [
        ("table-chair", "art/drafts/kitchen-table-chair-ligne-claire-2026-10-22-v3/manifest.json"),
        ("bin", "art/drafts/kitchen-bin-ligne-claire-2026-10-22-v2/manifest.json"),
        ("kettle", "art/drafts/kitchen-kettle-ligne-claire-2026-10-22-v1/manifest.json"),
        ("toaster", "art/drafts/kitchen-toaster-ligne-claire-2026-10-22-v4/manifest.json"),
        ("mixing-bowl", "art/drafts/kitchen-mixing-bowl-ligne-claire-2026-10-22-v1/manifest.json"),
    ]
    for family, path in singles:
        m = load(path); contracts.append({"role": f"{family} candidate", "file": path, "sha256": sha(ROOT / path), "approval": None})
        rows = m.get("objects")
        if rows:
            for a in rows: objects.append(record(family, a["filename"], a["sourceFile"], a["candidateFile"], m["set"]))
        else: objects.append(record(family, "table-chair.png", m["sourceFile"], m["candidateFile"], m["set"]))
        for e in m.get("effects", []): effects.append({"family": family, **e, "authority": m["set"]})

    fridge_fx = "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/fx-fridge-drip-ripple-f40.png"
    im = Image.open(ROOT / fridge_fx)
    effects.append({"family": "fridge", "filename": Path(fridge_fx).name, "sourceFile": fridge_fx, "sourceSha256": sha(ROOT / fridge_fx), "candidateFile": fridge_fx, "candidateSha256": sha(ROOT / fridge_fx), "pixels": list(im.size), "cellPixels": [144, 90], "frames": 40, "fps": 4, "byteExact": True, "authority": "approved V41 runtime"})
    return objects, effects, contracts


def make_sheets(objects: list[dict]) -> list[dict]:
    font = ImageFont.load_default(); result = []
    families = []
    for r in objects:
        if r["family"] not in families: families.append(r["family"])
    for family in families:
        rows = [r for r in objects if r["family"] == family]
        sheet = Image.new("RGBA", (1520, 58 + len(rows) * 238), (250, 244, 224, 255)); d = ImageDraw.Draw(sheet)
        d.text((18, 14), f"{family.upper()} · complete current / candidate / alpha ghost / 64 px proof", fill=INK, font=font)
        d.text((18, 31), "Every row records exact canvas, alpha bounds and SHA-256 in manifest.json", fill=INK, font=font)
        for i, r in enumerate(rows):
            src = Image.open(ROOT / r["sourceFile"]).convert("RGBA"); cand = Image.open(ROOT / r["candidateFile"]).convert("RGBA"); y = 56 + i * 238
            scale = min(300 / src.width, 174 / src.height); size = (max(1, round(src.width * scale)), max(1, round(src.height * scale)))
            for col, im in enumerate((src, cand)):
                panel = checker((360, 180)); shown = im.resize(size, Image.Resampling.LANCZOS); panel.alpha_composite(shown, ((360 - shown.width)//2, (180 - shown.height)//2)); sheet.alpha_composite(panel, (10 + col * 375, y))
            ghost = checker((360, 180)); shown = cand.resize(size, Image.Resampling.LANCZOS); ghost.alpha_composite(shown, ((360-shown.width)//2,(180-shown.height)//2)); tint = Image.new("RGBA", src.size, (232,72,86,0)); tint.putalpha(src.getchannel("A").point(lambda v: round(v*.32))); tint=tint.resize(size,Image.Resampling.LANCZOS); ghost.alpha_composite(tint,((360-tint.width)//2,(180-tint.height)//2)); sheet.alpha_composite(ghost,(760,y))
            proof = cand.copy(); proof.thumbnail((96,64), Image.Resampling.LANCZOS); sheet.alpha_composite(proof,(1160+(96-proof.width)//2,y+8))
            d.text((18,y+185),f"CURRENT · {r['filename']} · {r['sourcePixels']} · {r['sourceSha256'][:16]}",fill=INK,font=font)
            d.text((393,y+185),f"CANDIDATE · {r['candidateSha256'][:16]}",fill=INK,font=font)
            d.text((768,y+185),f"GHOST · bounds {r['candidateAlphaBounds']}",fill=INK,font=font)
            d.text((1145,y+83),"64 px",fill=INK,font=font)
            d.text((18,y+203),f"authority {r['authority']} · canvas exact {r['canvasExact']} · alpha exact {r['alphaExact']}",fill=INK,font=font)
        path = PACK / "evidence" / f"contact-{family}.png"; sheet.save(path, optimize=True)
        result.append({"family": family, "file": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "rows": len(rows)})
    return result


def build() -> None:
    if PACK.exists() or PUBLIC.exists(): raise RuntimeError(f"refusing to overwrite immutable complete V{VERSION} review")
    for p in (PACK / "candidates", PACK / "effects", PACK / "evidence", PACK / "workbench-assets", PUBLIC / "assets"): p.mkdir(parents=True)
    objects, effects, contracts = collect()
    for r in objects:
        name = f"{r['family']}--{r['filename']}"; target = PACK / "candidates" / name; shutil.copy2(ROOT / r["candidateFile"], target); shutil.copy2(target, PUBLIC / "assets" / name); r["reviewFile"] = target.relative_to(ROOT).as_posix(); r["reviewSha256"] = sha(target)
    for e in effects:
        source = e.get("preservedFile") or e["candidateFile"]
        e.setdefault("candidateFile", source); e.setdefault("candidateSha256", e.get("preservedSha256") or sha(ROOT / source))
        name = f"{e['family']}--{e['filename']}"; target = PACK / "effects" / name; shutil.copy2(ROOT / source, target); shutil.copy2(target, PUBLIC / "assets" / name); e["reviewFile"] = target.relative_to(ROOT).as_posix(); e["reviewSha256"] = sha(target)
    for source in sorted((V42_PACK / "assets").iterdir()):
        target = PACK / "workbench-assets" / source.name; shutil.copy2(source, target); shutil.copy2(target, PUBLIC / "assets" / source.name)
    sheets = make_sheets(objects)
    for s in sheets: shutil.copy2(ROOT / s["file"], PUBLIC / "assets" / Path(s["file"]).name)
    v42_manifest = load("art/drafts/kitchen-ligne-claire-healing-workbench-2026-10-22-v42/manifest.json")
    manifest = {
        "schema": "lighthouse-keeper/kitchen-ligne-claire-complete-review@1", "set": SET, "version": VERSION, "created": "2026-10-22",
        "status": "immutable-review-candidate-not-approved-not-registered", "scope": "complete kitchen furniture/object sweep and unchanged movement/healing laboratory",
        "styleRules": ["one even line weight", "real edges only", "closed flat spot colours", "no gradients shine glow hatching or texture", "even daylight object colour", "accurate machines simplified only by omission", "clarity at 64 px", "black only for black materials", "marks use contour weight"],
        "contracts": contracts, "objects": objects, "effects": effects, "contactSheets": sheets,
        "workbench": {"sourceSet": v42_manifest["set"], "sourceManifestSha256": sha(V42_PACK / "manifest.json"), "interactionAuthority": "approved V41", "movementHealingImplementationChanged": False, "rootAbsoluteAssetPrefix": f"/keeper-review/{SET}/assets/", "preloadBeforeControls": True},
        "verificationRequired": ["canvas", "alpha", "transparent padding", "alpha bounds", "pivots", "anchors", "collisions", "movement", "animations", "interactions", "repair", "countertop healing"],
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "productionWrites": [], "approvalRequired": True},
        "rollback": f"Discard only this V{VERSION} pack/review route; all approved, source, production and prior immutable review bytes remain unchanged."
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n"); (PACK / "batch-register.json").write_text(json.dumps({"status":"blocked-pending-explicit-frank-approval","register":False,"promote":False,"currentSelectorChanges":[],"productionWrites":[]},indent=2)+"\n")
    (PACK / "contact-sheet-index.json").write_text(json.dumps({"set": SET, "sheets": sheets}, indent=2)+"\n")
    sheet_html = "".join(f'<article class="panel"><h2>{s["family"]} · {s["rows"]} rows</h2><img class="contact" src="/keeper-review/{SET}/assets/{Path(s["file"]).name}" alt="Current candidate and alpha ghost comparison for {s["family"]}"></article>' for s in sheets)
    page = V42_PAGE.read_text().replace("kitchen-ligne-claire-healing-workbench-v42", SET).replace("V42 preserves", f"V{VERSION} preserves").replace("All V42 controls are ready.", f"All V{VERSION} controls are ready.")
    page = page.replace("</script></main>", f'''</script><section class="panel"><h2>Complete coordinated sweep</h2><p class="rule">Every candidate remains unregistered. The sheets below include every fitted variant and every object state, with source, candidate, alpha ghost, native clarity proof, dimensions, bounds and hashes. Effects are separately hash-audited in the manifest.</p><p><a href="/keeper-review/kitchen-kettle-ligne-claire-v1/">Kettle proof</a> · <a href="/keeper-review/kitchen-toaster-ligne-claire-v4/">Toaster proof</a> · <a href="/keeper-review/kitchen-mixing-bowl-ligne-claire-v1/">Bowl proof</a> · <a href="/keeper-review/kitchen-table-chair-ligne-claire-v3/">Table/chair proof</a> · <a href="/keeper-review/kitchen-bin-ligne-claire-v2/">Bin proof</a></p></section>{sheet_html}</main>''')
    (PUBLIC / "index.html").write_text(page); (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":"))+"\n")


def verify() -> None:
    m = json.loads((PACK / "manifest.json").read_text())
    for r in m["objects"]:
        src, cand = Image.open(ROOT / r["sourceFile"]).convert("RGBA"), Image.open(ROOT / r["candidateFile"]).convert("RGBA")
        if src.size != cand.size or src.getchannel("A").getbbox() != cand.getchannel("A").getbbox(): raise RuntimeError(f"canvas/padding drift {r['family']} {r['filename']}")
        if sha(ROOT / r["sourceFile"]) != r["sourceSha256"] or sha(ROOT / r["candidateFile"]) != r["candidateSha256"] or sha(ROOT / r["reviewFile"]) != r["reviewSha256"]: raise RuntimeError(f"hash drift {r['filename']}")
    for e in m["effects"]:
        if sha(ROOT / e["reviewFile"]) != e["reviewSha256"]: raise RuntimeError(f"effect drift {e['filename']}")
        if e.get("byteExact") and e["sourceSha256"] != e["candidateSha256"]: raise RuntimeError(f"byte-exact effect changed {e['filename']}")
    v42_script = re.search(r"<script>(.*)</script>", V42_PAGE.read_text(), re.S).group(1)
    candidate_script = re.search(r"<script>(.*)</script>", (PUBLIC / "index.html").read_text(), re.S).group(1).replace(SET, "kitchen-ligne-claire-healing-workbench-v42").replace(f"All V{VERSION} controls are ready.", "All V42 controls are ready.")
    if v42_script != candidate_script: raise RuntimeError("V41/V42 interaction implementation changed")
    if m["registration"]["register"] or m["registration"]["promote"] or m["registration"]["productionWrites"]: raise RuntimeError("registration gate opened")
    html = (PUBLIC / "index.html").read_text()
    if 'src="assets/' in html or f"/keeper-review/{SET}/assets/" not in html: raise RuntimeError("root-absolute delivery regression")
    print(f"Verified complete V{VERSION}: {len(m['objects'])} object states, {len(m['effects'])} effects, {len(m['contactSheets'])} complete sheets; V41 movement/healing JS unchanged; gate closed")


if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--verify", action="store_true"); a=p.parse_args(); verify() if a.verify else build()
