#!/usr/bin/env python3
"""Build the reversible Walk V2 review wrapper without changing Walk V1 art."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V1_PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-13-v1"
V1_PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-v1"
PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-13-v2"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-v2"
PUBLIC_PREFIX = "/keeper-review/keeper-prime-walk-v2/assets/"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    v1_register_path = V1_PACK / "batch-register.json"
    v1_page_path = V1_PUBLIC / "index.html"
    v1_assets = V1_PUBLIC / "assets"
    for required in (v1_register_path, v1_page_path, v1_assets):
        if not required.exists():
            raise RuntimeError(f"missing {rel(required)}")

    v1_register = json.loads(v1_register_path.read_text())
    if v1_register.get("batchId") != "keeper-prime-walk-2026-10-13-v1":
        raise RuntimeError("Walk V1 provenance changed")

    PACK.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    public_assets = PUBLIC / "assets"
    public_assets.mkdir(parents=True, exist_ok=True)

    source_assets = sorted(path for path in v1_assets.iterdir() if path.is_file())
    copied_assets = []
    for source in source_assets:
        target = public_assets / source.name
        shutil.copyfile(source, target)
        copied_assets.append({
            "name": source.name,
            "v1File": rel(source),
            "v1Sha256": digest(source),
            "v2File": rel(target),
            "v2Sha256": digest(target),
            "byteIdentical": digest(source) == digest(target),
        })

    v1_html = v1_page_path.read_text()
    if 'src="assets/' not in v1_html or 'const frames=["assets/' not in v1_html:
        raise RuntimeError("Walk V1 no longer has the pinned relative-asset failure signature")
    v2_html = v1_html.replace("Keeper Prime Walk V1", "Keeper Prime Walk V2")
    v2_html = v2_html.replace("Walk V1 review draft", "Walk V1 artwork · V2 routing wrapper")
    v2_html = v2_html.replace("Current production versus Walk V1", "Current production versus Walk V1 artwork")
    v2_html = v2_html.replace("assets/", PUBLIC_PREFIX)
    v2_html = v2_html.replace(
        "Finished-art walk draft · awaiting visual approval",
        "Walk V1 artwork · fixed review routing · awaiting visual approval",
    )
    v2_html = v2_html.replace(
        "One coherent eight-pose loop derived from the approved Side-right model and Rig Motion V3. Nothing has entered Final or production.",
        "Byte-identical Walk V1 artwork with absolute review asset addresses so Vercel cannot redirect frames to the wrong folder. Nothing has entered Final or production.",
    )
    (PUBLIC / "index.html").write_text(v2_html)

    handoff = """# Keeper Prime Walk V2 routing wrapper

Walk V2 changes no artwork. It copies every published Walk V1 review asset
byte-for-byte and changes only the review page's asset addresses from relative
`assets/...` paths to absolute
`/keeper-review/keeper-prime-walk-v2/assets/...` paths.

Vercel canonicalizes the public directory URL by removing its trailing slash.
Under that URL, a relative path resolves incorrectly beneath
`/keeper-review/assets/` and returns 404. Absolute paths make the review page
independent of trailing-slash behavior.

Status: technical review wrapper, awaiting the same visual decision as Walk
V1. No raw sprite, runtime sprite, manifest, workbench Final entry, source art
or V1 file changed. Roll back by deleting only this V2 draft and public folder.
"""
    (PACK / "HANDOFF.md").write_text(handoff)
    (PACK / "PROMPT_LOG.md").write_text(
        "# Prompt log\n\nNo image generation or image editing was used. This is a deterministic review-routing correction only.\n"
    )

    register = {
        "batchId": "keeper-prime-walk-2026-10-13-v2",
        "status": "technical-review-wrapper-awaiting-walk-v1-visual-approval",
        "purpose": "Publish the exact Walk V1 artwork under absolute asset URLs that remain valid after Vercel removes the trailing slash.",
        "source": {
            "walkV1Register": {"file": rel(v1_register_path), "sha256": digest(v1_register_path)},
            "walkV1ReviewPage": {"file": rel(v1_page_path), "sha256": digest(v1_page_path)},
            "walkV1Status": v1_register.get("status"),
        },
        "publishedAssets": copied_assets,
        "reviewPage": {
            "file": rel(PUBLIC / "index.html"),
            "sha256": digest(PUBLIC / "index.html"),
            "assetPrefix": PUBLIC_PREFIX,
            "relativeAssetUrls": False,
            "artworkChanged": False,
        },
        "validation": {
            "allWalkV1AssetsCopiedByteIdentically": all(item["byteIdentical"] for item in copied_assets),
            "walkV1FilesChanged": False,
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
            "workbenchFinalChanged": False,
        },
        "approvalBoundary": {
            "walkV1ArtworkApproved": False,
            "walkStopApproved": False,
            "finalLaneEntryAllowed": False,
            "productionPromotionAllowed": False,
        },
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; Walk V1, approved authorities, production art and prior drafts remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "assets": len(copied_assets), "publicPage": rel(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
