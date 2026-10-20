#!/usr/bin/env python3
"""Build one self-contained, immutable Claude Code activity-cloud review pack."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1"
V2 = ROOT / "art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2"
V2_INPUT = V2 / "claude-code-model-test-pack"
V7 = ROOT / "art/drafts/activity-cloud-composer-2026-10-20-v7"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


README = """# Claude Code activity-cloud review pack

This is the one folder to give Claude Code. It combines the complete Prime Rear Action Choreography V2 model-test input with the later Composer V7 generic-symbol extension.

## What is inside

- **74 final usable visual assets:** 41 byte-exact approved Prime body frames, 20 independently owned activity objects, 6 original kinetic/comic symbols and 7 new generic action symbols.
- **3 accepted source images:** the original six-symbol sheet, the V7 six-symbol sheet and the separately generated question-mark source.
- **1 rejected source image:** retained only to demonstrate the insufficient-gutter failure; it is not a candidate asset.
- **Complete choreography data:** V1 and V2 catalogues, all four authored stories, full/reduced 42-frame timelines and approved Prime-sequence metadata.
- **Complete vocabulary data:** Composer V6 vocabulary plus Composer V7 catalogue/register and all new symbol ownership records.
- **Governing guidance:** authoring standard, richer-choreography brief and the V2/V7 delivery records.
- **Review shells:** the immutable V2 choreography and V7 composer HTML for code inspection.

Start with `CLAUDE_REVIEW_PROMPT.md`, then `asset-manifest.json`. Every packaged file is SHA-256 pinned; `HASHES.sha256` is a conventional checksum list.

This pack is input-only. Claude should review and report, not edit the pack, approved Prime authorities, V1/V2/V7, runtime/Final assets, Kitchen work or deployment configuration.
"""


PROMPT = """Review the self-contained Lighthouse Keeper activity-cloud package at:

`art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1`

Read `README.md` and `asset-manifest.json` first, followed by:

- `metadata/choreography-v2-catalogue.json`
- `metadata/composer-v7-catalogue.json`
- `guidance/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md`
- `guidance/ACTIVITY_CALLOUT_DYNAMIC_CHOREOGRAPHY_NEXT.md`

This is a review task only. Do not edit any repository file and do not generate replacements unless I explicitly ask afterward.

Please review:

1. The four Prime Rear Action Choreography V2 examples—Garden BBQ, sandwich assembly, washing up and general repair—in both bubble and open treatments.
2. Whether the movement feels like a genuine hive of activity while remaining legible: object travel, separation, overlap, staging, rhythm and the five-frame quiet tail.
3. Whether directional ticks and contact stars actively sell momentum and interaction rather than behaving as decoration. Identify any beat where marks are missing, mistimed, too dense or detached from the moving object.
4. The seven new Composer V7 symbols: heat shimmer, pleasant aroma, foul odour, electrical arc, welding sparks, exclamation mark and question mark. Judge semantic clarity, family consistency, thumbnail readability and possible confusion with the six original symbols.
5. Which new symbols would strengthen each of the four examples, if any. Recommend specific timing/anchor/interaction roles, but do not modify the timelines.
6. Bubble treatment specifically: head origin, lighter background, connector placement, object spacing and whether the bubble contains energy without becoming cluttered.
7. Open treatment specifically: whether the same story remains readable without the enclosing bubble.
8. Reduced-motion behavior and independent layer ownership.

Treat every approved Prime body image as immutable and byte-exact. Treat all activity objects and symbols as independent layers. Do not recommend baking marks into objects or context into the Keeper.

Return a concise structured report with:

- overall verdict;
- strongest aspects;
- issues ranked Critical / Important / Optional;
- story-by-story notes;
- symbol-by-symbol notes for all 13 symbols;
- precise recommended changes, referencing story, treatment, frame range and component id where possible;
- a final list of what should remain untouched.
"""


def role_for(path: Path) -> str:
    value = path.relative_to(PACK).as_posix()
    if value.startswith("assets/body/"):
        return "approved-prime-body"
    if value.startswith("assets/activity/"):
        return "activity-object"
    if value.startswith("assets/symbol/original/"):
        return "original-comic-symbol"
    if value.startswith("assets/symbol/generic-v7/"):
        return "generic-action-symbol-v7"
    if value.startswith("assets/source/"):
        return "accepted-source-art"
    if value.startswith("evidence/rejected/"):
        return "rejected-source-evidence-not-a-candidate"
    if value.startswith("metadata/"):
        return "machine-readable-metadata"
    if value.startswith("guidance/"):
        return "governing-guidance"
    if value.startswith("review-shells/"):
        return "review-shell-code"
    return "handoff-instruction"


def main() -> None:
    required = [
        V2_INPUT / "asset-manifest.json",
        V2 / "batch-register.json",
        V7 / "batch-register.json",
        ROOT / "public/keeper-review/activity-cloud-composer-v7/catalogue.json",
    ]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing dependency: {rel(path)}")
    if PACK.exists():
        raise RuntimeError(f"immutable pack already exists: {rel(PACK)}")

    # Copy the complete V2 visual input set without changing any source bytes.
    for source in sorted((V2_INPUT / "assets/body").glob("*.png")):
        copy(source, PACK / "assets/body" / source.name)
    for source in sorted((V2_INPUT / "assets/activity").glob("*.png")):
        copy(source, PACK / "assets/activity" / source.name)
    for source in sorted((V2_INPUT / "assets/symbol").glob("*.png")):
        copy(source, PACK / "assets/symbol/original" / source.name)
    original_sheet = V2_INPUT / "assets/source/activity-comic-symbols-source-sheet.png"
    copy(original_sheet, PACK / "assets/source/original-six-symbol-source-sheet.png")

    # Add all seven normalised V7 symbols with hashes in their local filenames.
    for source in sorted((V7 / "drafts/components").glob("*.png")):
        copy(source, PACK / "assets/symbol/generic-v7" / f"{source.stem}-{sha(source)[:12]}.png")
    copy(V7 / "source/generic-action-symbols-sheet-source.png", PACK / "assets/source/generic-action-symbols-sheet-source.png")
    copy(V7 / "source/generic-question-mark-source.png", PACK / "assets/source/generic-question-mark-source.png")
    copy(
        V7 / "rejected/generic-action-symbols-sheet-attempt-1-insufficient-gutter.png",
        PACK / "evidence/rejected/generic-action-symbols-sheet-attempt-1-insufficient-gutter.png",
    )

    metadata = {
        V2_INPUT / "metadata/approved-prime-sequence.json": "approved-prime-sequence.json",
        V2_INPUT / "metadata/activity-vocabulary.json": "composer-v6-activity-vocabulary.json",
        V2_INPUT / "metadata/v1-catalogue.json": "choreography-v1-catalogue.json",
        V2_INPUT / "metadata/v2-catalogue.json": "choreography-v2-catalogue.json",
        V2_INPUT / "asset-manifest.json": "choreography-v2-original-asset-manifest.json",
        V2 / "batch-register.json": "choreography-v2-register.json",
        ROOT / "public/keeper-review/activity-cloud-composer-v7/catalogue.json": "composer-v7-catalogue.json",
        V7 / "batch-register.json": "composer-v7-register.json",
    }
    for source, name in metadata.items():
        copy(source, PACK / "metadata" / name)

    guidance = {
        ROOT / "docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md": "ACTIVITY_CALLOUT_AUTHORING_STANDARD.md",
        ROOT / "docs/ACTIVITY_CALLOUT_DYNAMIC_CHOREOGRAPHY_NEXT.md": "ACTIVITY_CALLOUT_DYNAMIC_CHOREOGRAPHY_NEXT.md",
        ROOT / "docs/KEEPER_PRIME_REAR_ACTION_CHOREOGRAPHY_V2_2026-10-20.md": "KEEPER_PRIME_REAR_ACTION_CHOREOGRAPHY_V2_2026-10-20.md",
        ROOT / "docs/ACTIVITY_CLOUD_COMPOSER_V7_2026-10-20.md": "ACTIVITY_CLOUD_COMPOSER_V7_2026-10-20.md",
        ROOT / "data/activity_callout_style_contract.json": "activity_callout_style_contract.json",
    }
    for source, name in guidance.items():
        copy(source, PACK / "guidance" / name)

    review_shells = {
        V2 / "page-template.html": "keeper-prime-rear-action-choreography-v2.html",
        ROOT / "public/keeper-review/activity-cloud-composer-v7/index.html": "activity-cloud-composer-v7.html",
    }
    for source, name in review_shells.items():
        copy(source, PACK / "review-shells" / name)

    write(PACK / "README.md", README)
    write(PACK / "CLAUDE_REVIEW_PROMPT.md", PROMPT)

    excluded = {"asset-manifest.json", "HASHES.sha256", "batch-register.json"}
    files = []
    for path in sorted(item for item in PACK.rglob("*") if item.is_file()):
        local = path.relative_to(PACK).as_posix()
        if local in excluded:
            continue
        files.append({
            "path": local,
            "role": role_for(path),
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        })

    pngs = [item for item in files if item["path"].endswith(".png")]
    final_visuals = [item for item in pngs if item["role"] in {
        "approved-prime-body", "activity-object", "original-comic-symbol", "generic-action-symbol-v7"
    }]
    accepted_sources = [item for item in pngs if item["role"] == "accepted-source-art"]
    rejected_sources = [item for item in pngs if item["role"] == "rejected-source-evidence-not-a-candidate"]
    if (len(final_visuals), len(accepted_sources), len(rejected_sources), len(pngs)) != (74, 3, 1, 78):
        raise RuntimeError("unexpected visual counts")

    manifest = {
        "schema": "lighthouse-keeper/claude-activity-cloud-review-pack@1",
        "pack": PACK.name,
        "status": "immutable-input-only-review-pack",
        "purpose": "One self-contained Claude Code review input for Prime Rear Action Choreography V2 plus Composer V7 generic symbols.",
        "counts": {
            "files": len(files),
            "pngImages": len(pngs),
            "finalUsableVisualAssets": len(final_visuals),
            "approvedPrimeBodyImages": sum(item["role"] == "approved-prime-body" for item in files),
            "activityObjectImages": sum(item["role"] == "activity-object" for item in files),
            "originalSymbolImages": sum(item["role"] == "original-comic-symbol" for item in files),
            "genericV7SymbolImages": sum(item["role"] == "generic-action-symbol-v7" for item in files),
            "acceptedSourceImages": len(accepted_sources),
            "rejectedEvidenceImages": len(rejected_sources),
        },
        "authorities": {
            "choreographyV2Register": {"file": rel(V2 / "batch-register.json"), "sha256": sha(V2 / "batch-register.json")},
            "composerV7Register": {"file": rel(V7 / "batch-register.json"), "sha256": sha(V7 / "batch-register.json")},
            "authoringStandard": {"file": "guidance/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md", "sha256": sha(PACK / "guidance/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md")},
        },
        "files": files,
    }
    write(PACK / "asset-manifest.json", json.dumps(manifest, indent=2) + "\n")

    hash_targets = sorted(item for item in PACK.rglob("*") if item.is_file() and item.name not in {"HASHES.sha256", "batch-register.json"})
    hashes = "".join(f"{sha(path)}  {path.relative_to(PACK).as_posix()}\n" for path in hash_targets)
    write(PACK / "HASHES.sha256", hashes)
    register = {
        "schema": "lighthouse-keeper/claude-activity-cloud-review-pack-register@1",
        "pack": PACK.name,
        "status": "immutable-input-only-review-pack",
        "manifest": {"file": rel(PACK / "asset-manifest.json"), "sha256": sha(PACK / "asset-manifest.json")},
        "hashList": {"file": rel(PACK / "HASHES.sha256"), "sha256": sha(PACK / "HASHES.sha256")},
        "counts": manifest["counts"],
        "sourcePacksUnchanged": True,
        "runtimeChanged": False,
        "kitchenChanged": False,
        "deployed": False,
        "rollback": f"Delete only {rel(PACK)} and its builder/verifier/documentation references.",
    }
    write(PACK / "batch-register.json", json.dumps(register, indent=2) + "\n")
    print(json.dumps({"pack": rel(PACK), **manifest["counts"]}, indent=2))


if __name__ == "__main__":
    main()
