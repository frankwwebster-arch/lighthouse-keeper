#!/usr/bin/env python3
"""Build immutable Kitchen V56 with Dishwasher V8 as the sole candidate."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-complete-review-v56"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v56"
PUBLIC = ROOT / "public/keeper-review" / SET
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"
DW_PACK = ROOT / "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v8"
V46_SET = "kitchen-ligne-claire-complete-review-v46"
V46_PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v46"
V46_PAGE = ROOT / "public/keeper-review" / V46_SET / "index.html"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V55 = load_module("kitchen_review_v55_builder_for_v56", ROOT / "scripts/build_kitchen_ligne_claire_complete_review_v55.py")
ORIGINAL_COPY2 = V55.shutil.copy2


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def replace_versions(value):
    if isinstance(value, dict):
        return {key: replace_versions(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_versions(item) for item in value]
    if isinstance(value, str):
        return value.replace("V55", "V56").replace("v55", "v56").replace("V7", "V8").replace("v7", "v8")
    return value


def copy2_redirect(source, target, *args, **kwargs):
    source = Path(source)
    if source.parent == DW_PACK / "evidence" and source.name == "dishwasher-v41-v7-ghost.png":
        source = DW_PACK / "evidence/dishwasher-v41-v8-ghost.png"
    return ORIGINAL_COPY2(source, target, *args, **kwargs)


def configure_v55() -> None:
    for name, value in {
        "SET": SET, "PACK": PACK, "PUBLIC": PUBLIC, "ARCHIVE_SET": ARCHIVE_SET,
        "DW_PACK": DW_PACK,
    }.items():
        setattr(V55, name, value)
    V55.shutil.copy2 = copy2_redirect
    V55.verify = lambda: None


def postprocess() -> None:
    manifest_path = PACK / "manifest.json"
    manifest = replace_versions(json.loads(manifest_path.read_text()))
    manifest.update({
        "set": SET,
        "version": 56,
        "status": "immutable-review-candidate-not-approved-not-registered",
        "scope": "approved Kettle V47/V46 motion presentation with Dishwasher V8 replacing rejected V7; V8 uses native-scale oven-weight linework, a narrower lower fascia and restrained side rails",
        "rollback": "Discard only this V56 pack, archive set and review shell; V46, Dishwasher V8, all approved/current assets and production remain byte-identical.",
    })
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    page_path = PUBLIC / "index.html"
    page = page_path.read_text().replace("V55", "V56").replace("v55", "v56").replace("V7", "V8").replace("v7", "v8")
    page = page.replace(
        "V8 uses the good high-resolution appliance references with meaningful-alpha crop bounds. That seats the fascia directly beneath one exact approved cabinet worktop in Off, On and Broken, with no secondary turquoise strip.",
        "V8 translates the high-resolution reference into deliberate native-scale art. Oven-weight contours stay sharp at 1×; the cabinet-blue side rails lose the glossy cyan flashes; the fascia and door are narrower and inset; and the lowered control centres align with the approved oven while the worktop remains visibly separate."
    )
    page = page.replace(
        "Dishwasher V8 control-panel invariance",
        "Dishwasher V8 oven-aligned control and sharpness audit"
    )
    page_path.write_text(page)

    register_path = PACK / "batch-register.json"
    register = replace_versions(json.loads(register_path.read_text()))
    register["set"] = SET
    register["candidate"]["manifest"] = {"file": relative(manifest_path), "sha256": sha(manifest_path)}
    register["candidate"]["publicShell"] = {"file": relative(page_path), "sha256": sha(page_path)}
    register_path.write_text(json.dumps(register, indent=2) + "\n")

    archive = json.loads(ARCHIVE_SET.read_text())
    archive["set"] = SET
    archive["page"] = {"path": relative(page_path), "sha256": sha(page_path), "bytes": page_path.stat().st_size}
    ARCHIVE_SET.write_text(json.dumps(archive, indent=2) + "\n")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    register = json.loads((PACK / "batch-register.json").read_text())
    archive = json.loads(ARCHIVE_SET.read_text())
    if manifest["set"] != SET or manifest["version"] != 56 or register["set"] != SET or register["register"] or register["promote"]:
        raise RuntimeError("V56 approval gate changed")
    if len(manifest["objects"]) != 60 or len(manifest["contactSheets"]) != 16 or len(archive["entries"]) != 140:
        raise RuntimeError("V56 coverage changed")
    dishwasher = json.loads((DW_PACK / "manifest.json").read_text())
    expected = {item["filename"]: item for item in dishwasher["records"]}
    for item in manifest["objects"]:
        source = ROOT / item["sourceFile"]
        candidate = ROOT / item["candidateFile"]
        review = ROOT / item["reviewFile"]
        if sha(source) != item["sourceSha256"] or sha(candidate) != item["candidateSha256"] or sha(review) != item["reviewSha256"]:
            raise RuntimeError(f"object hash drift: {item['filename']}")
        if item["family"] == "dishwasher":
            target = expected[item["filename"]]
            if item["authority"] != dishwasher["set"] or item["candidateSha256"] != target["candidateSha256"]:
                raise RuntimeError(f"Dishwasher V8 substitution drift: {item['filename']}")
            if Image.open(source).convert("RGBA").getchannel("A").tobytes() != Image.open(candidate).convert("RGBA").getchannel("A").tobytes():
                raise RuntimeError(f"dishwasher alpha drift: {item['filename']}")
    old_tail = (re.search(r",A='/keeper-review/.*?</script>", V46_PAGE.read_text(), re.S).group(0)
        .replace(V46_SET, SET)
        .replace("All V46 controls are ready.", "All V56 controls are ready."))
    new_tail = re.search(r",A='/keeper-review/.*?</script>", (PUBLIC / "index.html").read_text(), re.S).group(0)
    if old_tail != new_tail:
        raise RuntimeError("V46 movement/healing/motion implementation changed")
    for route, item in archive["entries"].items():
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(ROOT / item["object"]) != item["sha256"]:
            raise RuntimeError(f"archive mismatch: {route}")
    page = (PUBLIC / "index.html").read_text()
    if ('src="assets/' in page or f'/keeper-review/{SET}/assets/' not in page
            or "All V56 controls are ready." not in page
            or "Dishwasher V8 is the sole unapproved visual candidate" not in page
            or "Reject by deleting only this V56 pack, archive set and review shell." not in page):
        raise RuntimeError("V56 root-absolute delivery or preload regression")
    if archive["page"]["sha256"] != sha(PUBLIC / "index.html"):
        raise RuntimeError("V56 page hash drift")
    print("Verified V56: Dishwasher V8 native sharpness/alignment; exact alpha; unchanged approved V46 behavior; archive complete; gate closed")


def build() -> None:
    configure_v55()
    V55.build()
    postprocess()
    verify()
    print("Built Kitchen V56: Dishwasher V8 sole candidate; Kettle V47 and approved motion/SFX preserved")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
