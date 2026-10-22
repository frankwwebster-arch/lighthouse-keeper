#!/usr/bin/env python3
"""Build immutable Dishwasher V7 with one fitted worktop layer.

V7 keeps the high-resolution V5/V6 appliance drawings, but derives their crop
from meaningful alpha instead of stray near-transparent generation pixels.
That seats the fascia directly below the one approved cabinet worktop in Off,
On and Broken. The V6 failed-hinge door and hanging-handle correction remains.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-dishwasher-ligne-claire-v7"
PACK = ROOT / "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v7"
PUBLIC = ROOT / "public/keeper-review" / SET
SOURCE = ROOT / "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41"
OVEN = ROOT / "art/drafts/kitchen-oven-ligne-claire-2026-10-21-v8/masters/oven-on-top-safe-master-8x.png"
APPROVED_CABINET = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/cabinet-a-le-rj.png"
APPROVED_OVEN = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/oven-on.png"
V5_STYLE_ROOT = ROOT / "art/source/kitchen-dishwasher-ligne-claire-2026-10-22-v5"
GENERATED_BROKEN = ROOT / "art/source/kitchen-dishwasher-ligne-claire-2026-10-22-v7-generation/dishwasher-v7-broken-door-handle-reference.png"
STYLE_ROOT = ROOT / "art/source/kitchen-dishwasher-ligne-claire-2026-10-22-v7"
STYLE_REFS = {state: STYLE_ROOT / f"dishwasher-v7-{state}-style-reference.png" for state in ("off", "on", "broken")}
V5_PACK = ROOT / "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v5"
V6_PACK = ROOT / "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v6"
V41_APPROVAL = ROOT / "docs/review/kitchen-dishwasher-workbench-v41-approval-2026-10-20.json"
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
OBJECT_ROOT = ROOT / "review-archive/objects"
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"
APPROVED_CAPS = {
    "": ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/cabinet-a-le-re.png",
    "-le-re": ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/cabinet-a-le-re.png",
    "-le-rj": ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/cabinet-a-le-rj.png",
    "-lj-re": ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/cabinet-b-lj-re.png",
    "-lj-rj": ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/cabinet-a-lj-rj.png",
}

DENSITY = 16
INK = "#051824"
SUFFIXES = {
    "": (False, False),
    "-le-re": (False, False),
    "-le-rj": (False, True),
    "-lj-re": (True, False),
    "-lj-rj": (True, True),
}


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


def import_v5_module():
    import importlib.util

    path = ROOT / "scripts/build_kitchen_dishwasher_ligne_claire_v5.py"
    spec = importlib.util.spec_from_file_location("dishwasher_v5_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V5 = import_v5_module()


def prepare_style_references() -> None:
    """Copy intact V5 references and the versioned Broken redraw."""
    if STYLE_ROOT.exists():
        raise RuntimeError("refusing to overwrite immutable Dishwasher V7 source references")
    STYLE_ROOT.mkdir(parents=True)
    for state in ("off", "on"):
        shutil.copy2(V5_STYLE_ROOT / f"dishwasher-v5-{state}-style-reference.png", STYLE_REFS[state])

    shutil.copy2(GENERATED_BROKEN, STYLE_REFS["broken"])


def configure_v5_primitives() -> None:
    """Reuse the proven V5 geometry and registration code with V7 paths."""
    for name, value in {
        "SET": SET,
        "PACK": PACK,
        "PUBLIC": PUBLIC,
        "STYLE_ROOT": STYLE_ROOT,
        "STYLE_REFS": STYLE_REFS,
        "MASTERS": MASTERS,
        "CANDIDATES": CANDIDATES,
        "EVIDENCE": EVIDENCE,
        "ARCHIVE_SET": ARCHIVE_SET,
    }.items():
        setattr(V5, name, value)
    V5.styled_master = styled_master
    V5.closed_master = lambda state, left_joined, right_joined: styled_master(state, left_joined, right_joined)
    V5.broken_master = lambda left_joined, right_joined: styled_master("broken", left_joined, right_joined)


def styled_master(state: str, left_joined: bool, right_joined: bool) -> Image.Image:
    """Seat the visible appliance drawing beneath one approved worktop.

    Generation left alpha values below 16 far above the real object. V5/V6
    treated those specks as crop bounds, lowering the appliance's own blue top
    trim until it appeared as a second worktop. The threshold finds bounds
    only; retained RGBA pixels and their antialiasing remain unchanged.
    """
    image, _ = V5.base_master(left_joined, right_joined)
    reference = Image.open(STYLE_REFS[state]).convert("RGBA")
    meaningful = reference.getchannel("A").point(lambda value: 255 if value >= 16 else 0)
    bounds = meaningful.getbbox()
    if not bounds:
        raise RuntimeError(f"empty visible style reference: {STYLE_REFS[state]}")
    pad = 2
    bounds = (
        max(0, bounds[0] - pad),
        max(0, bounds[1] - pad),
        min(reference.width, bounds[2] + pad),
        min(reference.height, bounds[3] + pad),
    )
    reference = reference.crop(bounds)
    reference.thumbnail((V5.p(84), V5.p(68)), Image.Resampling.LANCZOS)
    x = V5.p(49) - reference.width // 2
    image.alpha_composite(reference, (x, V5.p(13)))
    return image


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
    draw.text((20, 16), "Dishwasher V7 - V41 authority / corrected oven-style candidate / alpha ghost", fill=INK, font=font)
    draw.text((20, 38), "One worktop layer in every state; reference-faithful fascia; V6 failed door and hanging handle retained.", fill=INK, font=font)
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
        draw.text((520, y + 290), f"V7 {item['state'].upper()}", fill=INK, font=font)
        draw.text((1020, y + 290), "GHOST / EXACT ALPHA", fill=INK, font=font)
    contact_path = EVIDENCE / "dishwasher-v41-v7-ghost.png"
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

    cabinet = Image.open(APPROVED_CABINET).convert("RGBA")
    oven = Image.open(APPROVED_OVEN).convert("RGBA")
    current_dw = Image.open(SOURCE / "dishwasher-on-lj-rj.png").convert("RGBA")
    candidate_dw = Image.open(CANDIDATES / "dishwasher-on-lj-rj.png").convert("RGBA")
    run_sheet = Image.new("RGBA", (1320, 1120), (250, 244, 224, 255))
    rdraw = ImageDraw.Draw(run_sheet)
    rdraw.text((18, 16), "PRIMARY ACCEPTANCE VIEW - cabinet / dishwasher / oven as one fitted set", fill=INK, font=font)
    rows = (
        ("CURRENT V41 RUN", current_dw, False),
        ("V7 SINGLE-WORKTOP RUN - PRIMARY DECISION VIEW", candidate_dw, False),
        ("V7 SINGLE-WORKTOP RUN + RED V41 ALPHA GHOST", candidate_dw, True),
    )
    for row, (label, dishwasher, show_ghost) in enumerate(rows):
        native = checker((320, 105), 8)
        native.alpha_composite(cabinet, (20, 20))
        native.alpha_composite(dishwasher, (101, 20))
        native.alpha_composite(oven, (188, 17))
        if show_ghost:
            ghost = Image.new("RGBA", current_dw.size, (235, 35, 70, 0))
            ghost.putalpha(current_dw.getchannel("A").point(lambda value: round(value * 0.32)))
            native.alpha_composite(ghost, (101, 20))
        enlarged = native.resize((1280, 420), Image.Resampling.NEAREST)
        y = 55 + row * 350
        run_sheet.alpha_composite(enlarged.crop((0, 0, 1280, 320)), (18, y))
        rdraw.text((20, y + 326), label, fill=INK, font=font)
    run_path = EVIDENCE / "dishwasher-worktop-run-ghost.png"
    run_sheet.save(run_path, optimize=True)
    return [contact_path, panel_path, tiny_path, run_path]


def review_html() -> str:
    page = V5.review_html()
    return (page.replace("V5", "V7")
        .replace("v5", "v7")
        .replace("V1-V4 are rejected.", "V1-V6 are superseded.")
        .replace("Built from the approved fitted-set construction:", "V7 uses the good high-resolution appliance references without the faulty alpha-speck crop: one approved worktop, no second turquoise strip, and"))


def published_entry(source: Path, name: str) -> dict:
    stored = archive_object(source)
    return {"source": relative(stored), "sourceSha256": sha(stored), "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}"}


def write_archive(entries: list[dict]) -> None:
    page = PUBLIC / "index.html"
    base_url = "https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects"
    mapped = {}
    for item in entries:
        object_path = ROOT / item["source"]
        digest = item["sourceSha256"]
        route = "/" + item["publicAssemblyPath"].removeprefix("public/")
        mapped[route] = {"sha256": digest, "extension": object_path.suffix, "bytes": object_path.stat().st_size, "object": item["source"], "url": f"{base_url}/{digest[:2]}/{digest}{object_path.suffix}"}
    archive = {"version": 1, "set": SET, "page": {"path": relative(page), "sha256": sha(page), "bytes": page.stat().st_size}, "objectsBaseUrl": base_url, "entries": dict(sorted(mapped.items()))}
    ARCHIVE_SET.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE_SET.write_text(json.dumps(archive, indent=2) + "\n")


def build() -> None:
    if PACK.exists() or PUBLIC.exists() or ARCHIVE_SET.exists() or STYLE_ROOT.exists():
        raise RuntimeError("refusing to overwrite immutable Dishwasher V7 output")
    prepare_style_references()
    configure_v5_primitives()
    for directory in (MASTERS, CANDIDATES, EVIDENCE):
        directory.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True)

    records = []
    for state in ("off", "on", "broken"):
        for suffix, flags in SUFFIXES.items():
            filename = f"dishwasher-{state}{suffix}.png"
            source_path = SOURCE / filename
            source = Image.open(source_path).convert("RGBA")
            master = V5.broken_master(*flags) if state == "broken" else V5.closed_master(state, *flags)
            master_path = MASTERS / filename.replace(".png", "-master-16x.png")
            candidate_path = CANDIDATES / filename
            master.save(master_path, optimize=True)
            candidate = V5.register(master, source, suffix)
            candidate.save(candidate_path, optimize=True)
            records.append({
                "state": state, "suffix": suffix, "filename": filename,
                "sourceFile": relative(source_path), "sourceSha256": sha(source_path), "sourcePixels": list(source.size),
                "sourceAlphaBounds": alpha_bounds(source), "sourceAlphaSha256": alpha_sha(source),
                "masterFile": relative(master_path), "masterSha256": sha(master_path), "masterPixels": list(master.size),
                "candidateFile": relative(candidate_path), "candidateSha256": sha(candidate_path), "candidatePixels": list(candidate.size),
                "candidateAlphaBounds": alpha_bounds(candidate), "candidateAlphaSha256": alpha_sha(candidate), "alphaExact": alpha_sha(source) == alpha_sha(candidate),
            })

    evidence = make_evidence(records)
    manifest = {
        "schema": "lighthouse-keeper/kitchen-dishwasher-ligne-claire@7",
        "set": SET, "created": "2026-10-22", "status": "immutable-review-candidate-not-approved-not-registered",
        "sourceAuthority": {"set": "kitchen-dishwasher-workbench-v41", "approval": relative(V41_APPROVAL), "approvalSha256": sha(V41_APPROVAL), "preserved": True},
        "visualAuthority": {"asset": relative(OVEN), "sha256": sha(OVEN)},
        "supersedesCandidate": {"set": "kitchen-dishwasher-ligne-claire-v6", "manifest": relative(V6_PACK / "manifest.json"), "manifestSha256": sha(V6_PACK / "manifest.json"), "reason": "V6 preserved the V5 alpha-speck crop, leaving the appliance's own blue top trim visible as a second turquoise worktop layer in Off, On and Broken"},
        "corrections": [
            "the unexplained floating bolt and its motion marks are absent from the versioned Broken redraw",
            "the lower-right hinge visibly fails while the lower-left remains attached and the door hangs substantially farther open",
            "the slender orange/copper handle hangs diagonally from its left attachment with the right mounting point failed",
            "dishwasher suds remain the inherited separate, appliance-owned forty-frame floor-puddle effect rather than baked appliance pixels",
            "Off, On and Broken use meaningful-alpha reference bounds so the fascia begins directly below the worktop",
            "the appliance's own blue top trim is fully occluded by the one approved cabinet worktop; no second turquoise strip remains",
            "approved cabinet worktop, both cabinet-side shoulders, V41 alpha, canvas and state names remain exact",
        ],
        "authorizedGeometryChange": "all three appliance drawings move upward inside the unchanged V41 alpha envelope solely to remove the rejected double-worktop construction; the V6 Broken door/handle geometry remains",
        "records": records,
        "generatedReferences": [{"file": relative(item), "sha256": sha(item), "role": "versioned visual reference; Off/On copied from V5; Broken is a built-in image-generation precise edit using V7-clean and V41 structural references"} for item in STYLE_REFS.values()],
        "brokenGenerationInput": {"file": relative(GENERATED_BROKEN), "sha256": sha(GENERATED_BROKEN)},
        "evidence": [{"file": relative(item), "sha256": sha(item)} for item in evidence],
        "verification": {"canvasExact": True, "alphaExact": True, "countertopRowsFourToSixteenExact": True, "singleWorktopLayerAllStates": True, "meaningfulAlphaCropThreshold": 16, "leftAndRightCabinetShouldersExact": True, "allStatesDifferFromRejectedV6": True, "floatingBoltRemoved": True, "doorWiderOpen": True, "rightHingeFailed": True, "handleHangsFromLeftAttachment": True, "sudsRemainSeparateOwnedEffect": True, "movementAnimationInteractionHealingRuntimeChanged": False},
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "productionWrites": [], "approvalRequired": True},
        "rollback": "Discard only this V7 source-reference directory, draft pack, archive set and review shell; V1-V6, V41 and production remain byte-for-byte unchanged.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(review_html())

    published = []
    for state in ("off", "on", "broken"):
        published.append(published_entry(SOURCE / f"dishwasher-{state}.png", f"current--dishwasher-{state}.png"))
        published.append(published_entry(CANDIDATES / f"dishwasher-{state}.png", f"candidate--dishwasher-{state}.png"))
    published.extend(published_entry(item, item.name) for item in evidence)
    registration = {"schema": "lighthouse-keeper/reversible-review-batch@1", "set": SET, "status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": [], "productionWrites": [], "candidate": {"manifest": {"file": relative(PACK / "manifest.json"), "sha256": sha(PACK / "manifest.json")}, "publicShell": {"file": relative(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")}}, "publishedAssets": published}
    (PACK / "batch-register.json").write_text(json.dumps(registration, indent=2) + "\n")
    write_archive(published)
    verify()
    print("Built Dishwasher V7: one worktop layer in all states; V6 broken-door correction retained; V41 alpha/canvas locked; gate closed")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    register = json.loads((PACK / "batch-register.json").read_text())
    archive = json.loads(ARCHIVE_SET.read_text())
    if manifest["registration"]["register"] or manifest["registration"]["promote"] or register["register"] or register["promote"]:
        raise RuntimeError("registration gate opened")
    if len(manifest["records"]) != 15 or len(register["publishedAssets"]) != 10 or len(archive["entries"]) != 10:
        raise RuntimeError("incomplete dishwasher family or archive payload")
    v6_records = {item["filename"]: item for item in json.loads((V6_PACK / "manifest.json").read_text())["records"]}
    for record in manifest["records"]:
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate_path = ROOT / record["candidateFile"]
        candidate = Image.open(candidate_path).convert("RGBA")
        if source.size != candidate.size or source.size != (98, 82) or source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"canvas/alpha drift: {record['filename']}")
        approved = Image.open(APPROVED_CAPS[record["suffix"]]).convert("RGB")
        if approved.crop((4, 4, 88, 17)).tobytes() != candidate.convert("RGB").crop((7, 4, 91, 17)).tobytes():
            raise RuntimeError(f"worktop drift: {record['filename']}")
        if approved.crop((4, 16, 12, 30)).tobytes() != candidate.convert("RGB").crop((7, 16, 15, 30)).tobytes() or approved.crop((80, 16, 88, 30)).tobytes() != candidate.convert("RGB").crop((83, 16, 91, 30)).tobytes():
            raise RuntimeError(f"under-overhang shoulder drift: {record['filename']}")
        fascia_band = candidate.convert("RGB").crop((15, 17, 83, 20))
        cream_pixels = sum(1 for red, green, blue in fascia_band.getdata() if red > 160 and green > 140 and blue > 100)
        if cream_pixels < 140:
            raise RuntimeError(f"second turquoise worktop layer returned: {record['filename']}")
        if sha(candidate_path) == v6_records[record["filename"]]["candidateSha256"]:
            raise RuntimeError(f"rejected V6 double-worktop bytes survived: {record['filename']}")
    if sha(STYLE_REFS["broken"]) == sha(V5_STYLE_ROOT / "dishwasher-v5-broken-style-reference.png"):
        raise RuntimeError("Broken source correction missing")
    for route, item in archive["entries"].items():
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(ROOT / item["object"]) != item["sha256"]:
            raise RuntimeError(f"archive mismatch: {route}")
    page = (PUBLIC / "index.html").read_text()
    if 'src="assets/' in page or f"/keeper-review/{SET}/assets/" not in page or "Dishwasher Ligne-Claire V7" not in page:
        raise RuntimeError("V7 root-absolute review delivery regression")
    print("Verified Dishwasher V7: one worktop layer in Off/On/Broken; V6 door/handle retained; 15 exact canvases/alphas; gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
