#!/usr/bin/env python3
"""Build/verify immutable V45: V44 plus small objects and preparation/tea."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-complete-review-v45"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45"
PUBLIC = ROOT / "public/keeper-review" / SET
V44_SET = "kitchen-ligne-claire-complete-review-v44"
V44_PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v44"
V44_PAGE = ROOT / "public/keeper-review" / V44_SET / "index.html"
V44_ARCHIVE = ROOT / "review-archive/sets" / f"{V44_SET}.json"
SMALL_PACK = ROOT / "art/drafts/kitchen-small-objects-ligne-claire-2026-10-22-v1"
PREP_PACK = ROOT / "art/drafts/kitchen-prep-tea-ligne-claire-2026-10-22-v2"
CONDIMENT_PACK = ROOT / "art/drafts/activity-story-ligne-claire-condiments-flat-glass-correction-2026-10-21-v1"
OBJECT_ROOT = ROOT / "review-archive/objects"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def archive_object(source: Path) -> Path:
    digest = sha(source)
    target = OBJECT_ROOT / digest[:2] / f"{digest}{source.suffix.lower()}"
    if target.exists() and sha(target) != digest:
        raise RuntimeError(f"archive collision: {target}")
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return target


def publish(source: Path, name: str) -> dict:
    stored = archive_object(source)
    return {
        "source": rel(stored),
        "sourceSha256": sha(stored),
        "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}",
    }


def alpha_sha(path: Path) -> str:
    return hashlib.sha256(Image.open(path).convert("RGBA").getchannel("A").tobytes()).hexdigest()


def copy_tree(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, target / item.name)


def exact_candidate_rows(manifest: dict, family: str, prefix: str) -> list[dict]:
    rows = []
    for item in manifest["objects"]:
        source = ROOT / item["sourceFile"]
        candidate = ROOT / item["candidateFile"]
        target = PACK / "candidates" / f"{prefix}--{item['id']}.png"
        shutil.copy2(candidate, target)
        rows.append({
            "family": family,
            "id": item["id"],
            "filename": f"{item['id']}.png",
            "sourceFile": item["sourceFile"],
            "sourceSha256": item["sourceSha256"],
            "candidateFile": item["candidateFile"],
            "candidateSha256": item["candidateSha256"],
            "reviewFile": rel(target),
            "reviewSha256": sha(target),
            "sourcePixels": item["canvas"],
            "candidatePixels": item["canvas"],
            "sourceAlphaBounds": item["sourceBounds"],
            "candidateAlphaBounds": item["candidateBounds"],
            "sourceAlphaSha256": alpha_sha(source),
            "candidateAlphaSha256": alpha_sha(candidate),
            "canvasExact": Image.open(source).size == Image.open(candidate).size,
            "alphaBoundsExact": item["sourceBounds"] == item["candidateBounds"],
            "alphaExact": alpha_sha(source) == alpha_sha(candidate),
            "authority": manifest["set"],
            "approval": None,
        })
    return rows


def condiment_rows() -> list[dict]:
    batch = load(CONDIMENT_PACK / "batch-register.json")
    rows = []
    for asset_id, item in batch["components"].items():
        current = ROOT / item["currentReferenceFile"]
        approved = ROOT / item["file"]
        if sha(current) != item["currentReferenceSha256"] or sha(approved) != item["sha256"]:
            raise RuntimeError(f"approved condiment drift: {asset_id}")
        target = PACK / "approved-current" / f"{asset_id}.png"
        shutil.copy2(approved, target)
        image = Image.open(approved).convert("RGBA")
        rows.append({
            "family": "condiments-approved-current-v2",
            "id": asset_id,
            "previousCurrentFile": item["currentReferenceFile"],
            "previousCurrentSha256": item["currentReferenceSha256"],
            "approvedCurrentFile": item["file"],
            "approvedCurrentSha256": item["sha256"],
            "reviewFile": rel(target),
            "reviewSha256": sha(target),
            "pixels": list(image.size),
            "alphaBounds": list(image.getchannel("A").getbbox() or (0, 0, 0, 0)),
            "status": "approved-and-registered-existing-authority",
        })
    return rows


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable complete V45 review")
    for directory in ("candidates", "effects", "evidence", "workbench-assets", "approved-current"):
        (PACK / directory).mkdir(parents=True)
    PUBLIC.mkdir(parents=True)

    v44 = load(V44_PACK / "manifest.json")
    v44_archive = load(V44_ARCHIVE)
    small = load(SMALL_PACK / "manifest.json")
    prep = load(PREP_PACK / "manifest.json")

    copy_tree(V44_PACK / "candidates", PACK / "candidates")
    copy_tree(V44_PACK / "effects", PACK / "effects")
    copy_tree(V44_PACK / "evidence", PACK / "evidence")
    copy_tree(V44_PACK / "workbench-assets", PACK / "workbench-assets")

    objects = json.loads(json.dumps(v44["objects"]))
    effects = json.loads(json.dumps(v44["effects"]))
    for item in objects:
        old = ROOT / item["reviewFile"]
        item["reviewFile"] = rel(PACK / "candidates" / old.name)
        item["reviewSha256"] = sha(ROOT / item["reviewFile"])
    for item in effects:
        old = ROOT / item["reviewFile"]
        item["reviewFile"] = rel(PACK / "effects" / old.name)
        item["reviewSha256"] = sha(ROOT / item["reviewFile"])

    new_objects = exact_candidate_rows(small, "small-objects", "small-objects")
    new_objects += exact_candidate_rows(prep, "preparation-tea", "preparation-tea")
    objects.extend(new_objects)
    approved = condiment_rows()

    extra_sheets = [
        ("small-objects", SMALL_PACK / "evidence/current-candidate-ghost-64px.png", "contact-small-objects.png", 5),
        ("preparation-tea", PREP_PACK / "evidence/current-candidate-ghost-64px.png", "contact-preparation-tea.png", 5),
        ("condiments-approved-current-v2", CONDIMENT_PACK / "evidence/superseded-vs-flat-glass-contact-sheet.png", "contact-condiments-approved-current-v2.png", 9),
    ]
    sheets = []
    for item in v44["contactSheets"]:
        source = ROOT / item["file"]
        target = PACK / "evidence" / source.name
        sheets.append({**item, "file": rel(target), "sha256": sha(target), "inheritedByteExactFrom": V44_SET})
    for family, source, name, rows in extra_sheets:
        target = PACK / "evidence" / name
        shutil.copy2(source, target)
        sheets.append({"family": family, "file": rel(target), "sha256": sha(target), "rows": rows})

    contracts = json.loads(json.dumps(v44["contracts"])) + [
        {"role": "mask-locked knives and mills", "file": rel(SMALL_PACK / "manifest.json"), "sha256": sha(SMALL_PACK / "manifest.json"), "approval": None},
        {"role": "mask-locked preparation and tea V2", "file": rel(PREP_PACK / "manifest.json"), "sha256": sha(PREP_PACK / "manifest.json"), "approval": None},
        {"role": "approved current condiment V2 authority", "file": rel(CONDIMENT_PACK / "batch-register.json"), "sha256": sha(CONDIMENT_PACK / "batch-register.json"), "approval": "existing-approved-and-registered"},
    ]
    manifest = {
        **v44,
        "set": SET,
        "version": 45,
        "status": "immutable-review-candidate-not-approved-not-registered",
        "scope": "V44 complete kitchen plus knives, mills, preparation and tea; approved condiment V2 authority included without redraw",
        "contracts": contracts,
        "objects": objects,
        "effects": effects,
        "approvedCurrentReferences": approved,
        "contactSheets": sheets,
        "workbench": {**v44["workbench"], "sourceSet": V44_SET, "sourceManifestSha256": sha(V44_PACK / "manifest.json"), "rootAbsoluteAssetPrefix": f"/keeper-review/{SET}/assets/"},
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "productionWrites": [], "approvalRequired": True},
        "rollback": "Discard only this V45 pack, archive set and review shell; V44, all approved/current assets and production files remain byte-identical.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "contact-sheet-index.json").write_text(json.dumps({"set": SET, "sheets": sheets}, indent=2) + "\n")

    additions = "".join(
        f'<article class="panel"><h2>{family} · {rows} rows</h2><img class="contact" src="/keeper-review/{SET}/assets/{name}" alt="Current candidate and alpha-ghost review for {family}"></article>'
        for family, _source, name, rows in extra_sheets
    )
    page = (V44_PAGE.read_text()
        .replace(V44_SET, SET)
        .replace("<title>Kitchen Ligne-Claire Healing Workbench V42</title>", "<title>Kitchen Ligne-Claire Complete Review V45</title>")
        .replace("V42 immutable Ligne-Claire healing workbench", "V45 immutable complete kitchen review")
        .replace("V44 preserves", "V45 preserves")
        .replace("All V44 controls are ready.", "All V45 controls are ready."))
    page = page.replace("</main>", f'<section class="panel"><h2>V45 small-object continuation</h2><p class="rule">Ten new candidates are mask-locked to their current alpha bytes and remain unregistered. The nine condiment V2 assets below are existing approved/current authorities, included byte-for-byte for palette and glass-language calibration.</p><p class="warn">Approval is required before any of the ten new candidates can become current. V44 interaction, movement, animation and healing code is unchanged.</p></section>{additions}</main>')
    (PUBLIC / "index.html").write_text(page)

    published = []
    for old_path, entry in v44_archive["entries"].items():
        name = Path(old_path).name
        published.append({"source": entry["object"], "sourceSha256": entry["sha256"], "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}"})
    for sheet in sheets[-3:]:
        published.append(publish(ROOT / sheet["file"], Path(sheet["file"]).name))
    for item in new_objects:
        published.append(publish(ROOT / item["reviewFile"], f"{item['family']}--{item['id']}.png"))
    for item in approved:
        published.append(publish(ROOT / item["reviewFile"], f"condiments-approved--{item['id']}.png"))
    paths = [item["publicAssemblyPath"] for item in published]
    if len(paths) != len(set(paths)):
        raise RuntimeError("duplicate V45 public assembly path")
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
        "productionWrites": [],
        "candidate": {"manifest": {"file": rel(PACK / "manifest.json"), "sha256": sha(PACK / "manifest.json")}, "publicShell": {"file": rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")}},
        "publishedAssets": published,
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    verify(pre_archive=True)
    print(f"Built V45: {len(objects)} object rows, {len(effects)} effects, {len(sheets)} sheets; registration closed")


def verify(pre_archive: bool = False) -> None:
    manifest = load(PACK / "manifest.json")
    register = load(PACK / "batch-register.json")
    if manifest["set"] != SET or register["set"] != SET or register["register"] or register["promote"]:
        raise RuntimeError("V45 gate changed")
    if manifest["registration"]["register"] or manifest["registration"]["promote"] or manifest["registration"]["productionWrites"]:
        raise RuntimeError("V45 registration opened")
    if len(manifest["objects"]) != 60 or len(manifest["approvedCurrentReferences"]) != 9 or len(manifest["contactSheets"]) != 14:
        raise RuntimeError("V45 coverage changed")
    for item in manifest["objects"]:
        source, candidate, review = ROOT / item["sourceFile"], ROOT / item["candidateFile"], ROOT / item["reviewFile"]
        if sha(source) != item["sourceSha256"] or sha(candidate) != item["candidateSha256"] or sha(review) != item["reviewSha256"]:
            raise RuntimeError(f"object hash drift: {item['filename']}")
        if item["family"] in ("small-objects", "preparation-tea"):
            si, ci = Image.open(source).convert("RGBA"), Image.open(candidate).convert("RGBA")
            if si.size != ci.size or si.getchannel("A").tobytes() != ci.getchannel("A").tobytes():
                raise RuntimeError(f"new object geometry drift: {item['id']}")
    for item in manifest["effects"]:
        if sha(ROOT / item["reviewFile"]) != item["reviewSha256"]:
            raise RuntimeError(f"effect drift: {item['filename']}")
    for item in manifest["approvedCurrentReferences"]:
        if sha(ROOT / item["approvedCurrentFile"]) != item["approvedCurrentSha256"] or sha(ROOT / item["reviewFile"]) != item["reviewSha256"]:
            raise RuntimeError(f"approved condiment drift: {item['id']}")
    v44_js = re.search(r"<script>(.*)</script>", V44_PAGE.read_text(), re.S).group(1)
    v45_js = re.search(r"<script>(.*)</script>", (PUBLIC / "index.html").read_text(), re.S).group(1).replace(SET, V44_SET).replace("All V45 controls are ready.", "All V44 controls are ready.")
    if v44_js != v45_js:
        raise RuntimeError("V44 movement/healing implementation changed")
    page = (PUBLIC / "index.html").read_text()
    if 'src="assets/' in page or f'/keeper-review/{SET}/assets/' not in page:
        raise RuntimeError("root-absolute V45 delivery regression")
    for item in register["publishedAssets"]:
        source = ROOT / item["source"]
        if not source.is_file() or sha(source) != item["sourceSha256"]:
            raise RuntimeError(f"published source drift: {item['source']}")
    if not pre_archive:
        archived = load(ROOT / "review-archive/sets" / f"{SET}.json")
        if len(archived["entries"]) != len(register["publishedAssets"]):
            raise RuntimeError("V45 archive entry coverage changed")
    print("Verified V45: exact-alpha new candidates; approved condiment bytes; V44 JS; root-absolute archive delivery; gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
