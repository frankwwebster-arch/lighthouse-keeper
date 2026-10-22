#!/usr/bin/env python3
"""Build immutable V50: V46 motion workbench with Dishwasher V3."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-complete-review-v50"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v50"
PUBLIC = ROOT / "public/keeper-review" / SET
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"
OBJECT_ROOT = ROOT / "review-archive/objects"
V45_SET = "kitchen-ligne-claire-complete-review-v46"
V45_PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v46"
V45_PAGE = ROOT / "public/keeper-review" / V45_SET / "index.html"
V45_ARCHIVE = ROOT / "review-archive/sets" / f"{V45_SET}.json"
DW_PACK = ROOT / "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v3"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def copy_tree(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, target / item.name)


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


def write_archive(entries: list[dict]) -> None:
    page = PUBLIC / "index.html"
    base_url = "https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects"
    mapped = {}
    for item in entries:
        source = ROOT / item["source"]
        digest = item["sourceSha256"]
        route = "/" + item["publicAssemblyPath"].removeprefix("public/")
        mapped[route] = {
            "sha256": digest,
            "extension": source.suffix,
            "bytes": source.stat().st_size,
            "object": item["source"],
            "url": f"{base_url}/{digest[:2]}/{digest}{source.suffix}",
        }
    archive = {
        "version": 1,
        "set": SET,
        "page": {"path": rel(page), "sha256": sha(page), "bytes": page.stat().st_size},
        "objectsBaseUrl": base_url,
        "entries": dict(sorted(mapped.items())),
    }
    ARCHIVE_SET.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE_SET.write_text(json.dumps(archive, indent=2) + "\n")


def build() -> None:
    if PACK.exists() or PUBLIC.exists() or ARCHIVE_SET.exists():
        raise RuntimeError("refusing to overwrite immutable V50 review")
    for directory in ("candidates", "effects", "evidence", "workbench-assets", "approved-current", "components", "audio"):
        copy_tree(V45_PACK / directory, PACK / directory)
    PUBLIC.mkdir(parents=True)

    v45 = load(V45_PACK / "manifest.json")
    old_archive = load(V45_ARCHIVE)
    dishwasher = load(DW_PACK / "manifest.json")
    by_name = {item["filename"]: item for item in dishwasher["records"]}

    objects = json.loads(json.dumps(v45["objects"]))
    for item in objects:
        old_review = ROOT / item["reviewFile"]
        item["reviewFile"] = rel(PACK / "candidates" / old_review.name)
        item["reviewSha256"] = sha(ROOT / item["reviewFile"])
        if item["family"] != "dishwasher":
            continue
        source = by_name[item["filename"]]
        candidate = ROOT / source["candidateFile"]
        review_target = PACK / "candidates" / f"dishwasher--{item['filename']}"
        workbench_target = PACK / "workbench-assets" / item["filename"]
        shutil.copy2(candidate, review_target)
        shutil.copy2(candidate, workbench_target)
        item.update({
            "authority": dishwasher["set"],
            "candidateFile": source["candidateFile"],
            "candidateSha256": source["candidateSha256"],
            "candidatePixels": source["candidatePixels"],
            "candidateAlphaBounds": source["candidateAlphaBounds"],
            "candidateAlphaSha256": source["candidateAlphaSha256"],
            "canvasExact": True,
            "alphaBoundsExact": source["sourceAlphaBounds"] == source["candidateAlphaBounds"],
            "alphaExact": source["alphaExact"],
            "reviewFile": rel(review_target),
            "reviewSha256": sha(review_target),
        })

    effects = json.loads(json.dumps(v45["effects"]))
    for item in effects:
        item["reviewFile"] = rel(PACK / "effects" / Path(item["reviewFile"]).name)
        item["reviewSha256"] = sha(ROOT / item["reviewFile"])
    approved = json.loads(json.dumps(v45["approvedCurrentReferences"]))
    for item in approved:
        item["reviewFile"] = rel(PACK / "approved-current" / Path(item["reviewFile"]).name)
        item["reviewSha256"] = sha(ROOT / item["reviewFile"])

    # Replace the old dishwasher sheet and add explicit panel/run gates.
    contact = PACK / "evidence/contact-dishwasher.png"
    shutil.copy2(DW_PACK / "evidence/dishwasher-v41-v3-ghost.png", contact)
    panel = PACK / "evidence/contact-dishwasher-control-panel.png"
    run = PACK / "evidence/contact-dishwasher-worktop-run.png"
    shutil.copy2(DW_PACK / "evidence/dishwasher-control-panel-invariance.png", panel)
    shutil.copy2(DW_PACK / "evidence/dishwasher-worktop-run-ghost.png", run)
    sheets = []
    for item in v45["contactSheets"]:
        target = PACK / "evidence" / Path(item["file"]).name
        sheets.append({**item, "file": rel(target), "sha256": sha(target), "inheritedByteExactFrom": V45_SET if item["family"] != "dishwasher" else None})
    sheets.extend([
        {"family": "dishwasher-control-panel-v3", "file": rel(panel), "sha256": sha(panel), "rows": 3},
        {"family": "dishwasher-worktop-run-v3", "file": rel(run), "sha256": sha(run), "rows": 2},
    ])

    contracts = json.loads(json.dumps(v45["contracts"])) + [{
        "role": "geometry-locked dishwasher V3; invariant panel; approved cabinet worktop caps",
        "file": rel(DW_PACK / "manifest.json"),
        "sha256": sha(DW_PACK / "manifest.json"),
        "approval": None,
    }]
    manifest = {
        **v45,
        "set": SET,
        "version": 50,
        "status": "immutable-review-candidate-not-approved-not-registered",
        "scope": "V46 broken-appliance motion workbench with rejected dishwasher V1 replaced by geometry-locked V3",
        "contracts": contracts,
        "objects": objects,
        "effects": effects,
        "approvedCurrentReferences": approved,
        "contactSheets": sheets,
        "workbench": {
            **v45["workbench"],
            "sourceSet": V45_SET,
            "sourceManifestSha256": sha(V45_PACK / "manifest.json"),
            "rootAbsoluteAssetPrefix": f"/keeper-review/{SET}/assets/",
            "dishwasherCandidate": dishwasher["set"],
            "movementHealingImplementationChanged": False,
        },
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "productionWrites": [], "approvalRequired": True},
        "rollback": "Discard only this V50 pack, archive set and review shell; V46, Dishwasher V3, all approved/current assets and production remain byte-identical.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "contact-sheet-index.json").write_text(json.dumps({"set": SET, "sheets": sheets}, indent=2) + "\n")

    page = V45_PAGE.read_text().replace(V45_SET, SET)
    page = page.replace("<title>Kitchen V47 broken-appliance motion workbench</title>", "<title>Kitchen V50 · Dishwasher V3 and broken-appliance motion</title>")
    page = page.replace("V46 immutable kitchen review", "V50 immutable kitchen review")
    page = page.replace("Kitchen V47 · broken-appliance vibration workbench", "Kitchen V50 · Dishwasher V3 and broken-appliance motion")
    page = page.replace("V46 makes Kitchen Kettle Bubble Authority V47", "V50 keeps Kitchen Kettle Bubble Authority V47 as")
    page = page.replace("All V46 controls are ready.", "All V50 controls are ready.")
    page = page.replace("href=\"/keeper-review/kitchen-dishwasher-ligne-claire-v1/\">dishwasher drawing review", "href=\"/keeper-review/kitchen-dishwasher-ligne-claire-v3/index.html\">Dishwasher V3 drawing and ghost review")
    page = page.replace("<strong>Review boundary:</strong> V46 is an immutable, unapproved motion/SFX integration proof.", "<strong>Review boundary:</strong> V50 is an immutable, unapproved Dishwasher V3 plus V46 motion/SFX integration proof. V46 remains preserved unchanged.")
    page = page.replace('"dishwasherVisualCandidate":"kitchen-dishwasher-ligne-claire-v1"', '"dishwasherVisualCandidate":"kitchen-dishwasher-ligne-claire-v3"')
    old_dw = {item["filename"]: item for item in v45["objects"] if item["family"] == "dishwasher"}
    for filename, source in by_name.items():
        page = page.replace(f'"{filename}":"{old_dw[filename]["candidateSha256"]}"', f'"{filename}":"{source["candidateSha256"]}"')
    addition = f'''<section class="panel"><h2>V50 dishwasher correction</h2><p class="rule">The rejected V1 redraw is removed. V3 restores the exact V41 panel placements, uses one physical panel in every state, copies the matching approved cabinet worktop cap, and applies only the authorised steeper Broken-handle angle.</p><p class="warn">Registration remains closed. V46 motion/SFX, V41 movement, Broken locking, state transitions, effect ownership and countertop-healing code are unchanged.</p></section><article class="panel"><h2>Dishwasher V3 control-panel invariance</h2><img class="contact" src="/keeper-review/{SET}/assets/contact-dishwasher-control-panel.png"></article><article class="panel"><h2>Dishwasher V3 full-run worktop ghost</h2><img class="contact" src="/keeper-review/{SET}/assets/contact-dishwasher-worktop-run.png"></article>'''
    page = page.replace("</main>", addition + "</main>")
    (PUBLIC / "index.html").write_text(page)

    published = []
    for old_route, entry in old_archive["entries"].items():
        if "/assets/" not in old_route:
            continue
        name = Path(old_route).name
        replacement = None
        if name.startswith("dishwasher--dishwasher-"):
            replacement = ROOT / by_name[name.removeprefix("dishwasher--")]["candidateFile"]
        elif name in by_name:
            replacement = ROOT / by_name[name]["candidateFile"]
        elif name == "contact-dishwasher.png":
            replacement = contact
        if replacement:
            published.append(publish(replacement, name))
        else:
            published.append({"source": entry["object"], "sourceSha256": entry["sha256"], "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}"})
    published.extend([publish(panel, panel.name), publish(run, run.name)])
    if len({item["publicAssemblyPath"] for item in published}) != len(published):
        raise RuntimeError("duplicate V50 public assembly path")
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
        "productionWrites": [],
        "candidate": {
            "manifest": {"file": rel(PACK / "manifest.json"), "sha256": sha(PACK / "manifest.json")},
            "publicShell": {"file": rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")},
        },
        "publishedAssets": published,
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_archive(published)
    verify()
    print(f"Built V50: {len(objects)} object rows, {len(effects)} effects, {len(sheets)} sheets; registration closed")


def verify() -> None:
    manifest = load(PACK / "manifest.json")
    register = load(PACK / "batch-register.json")
    archive = load(ARCHIVE_SET)
    if manifest["set"] != SET or register["set"] != SET or register["register"] or register["promote"]:
        raise RuntimeError("V50 gate changed")
    if len(manifest["objects"]) != 60 or len(manifest["contactSheets"]) != 16 or len(archive["entries"]) != 140:
        raise RuntimeError("V50 coverage changed")
    dw_manifest = load(DW_PACK / "manifest.json")
    expected = {item["filename"]: item for item in dw_manifest["records"]}
    for item in manifest["objects"]:
        source = ROOT / item["sourceFile"]
        candidate = ROOT / item["candidateFile"]
        review = ROOT / item["reviewFile"]
        if sha(source) != item["sourceSha256"] or sha(candidate) != item["candidateSha256"] or sha(review) != item["reviewSha256"]:
            raise RuntimeError(f"object hash drift: {item['filename']}")
        if item["family"] == "dishwasher":
            target = expected[item["filename"]]
            if item["authority"] != dw_manifest["set"] or item["candidateSha256"] != target["candidateSha256"]:
                raise RuntimeError(f"dishwasher V3 substitution drift: {item['filename']}")
            if Image.open(source).convert("RGBA").getchannel("A").tobytes() != Image.open(candidate).convert("RGBA").getchannel("A").tobytes():
                raise RuntimeError(f"dishwasher alpha drift: {item['filename']}")
    old_tail = (re.search(r",A='/keeper-review/.*?</script>", V45_PAGE.read_text(), re.S).group(0)
        .replace(V45_SET, SET)
        .replace("All V46 controls are ready.", "All V50 controls are ready."))
    new_tail = re.search(r",A='/keeper-review/.*?</script>", (PUBLIC / "index.html").read_text(), re.S).group(0)
    if old_tail != new_tail:
        raise RuntimeError("V46 movement/healing/motion implementation changed")
    for route, item in archive["entries"].items():
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(ROOT / item["object"]) != item["sha256"]:
            raise RuntimeError(f"archive mismatch: {route}")
    page = (PUBLIC / "index.html").read_text()
    if 'src="assets/' in page or f'/keeper-review/{SET}/assets/' not in page or "All V50 controls are ready." not in page:
        raise RuntimeError("V50 root-absolute delivery or preload regression")
    print("Verified V50: V3 dishwasher bytes; exact alpha; unchanged V46 movement/healing/motion JS; root-absolute archive; gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
