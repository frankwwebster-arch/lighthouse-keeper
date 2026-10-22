#!/usr/bin/env python3
"""Complete the immutable V48 archive record after its duplicate-route stop."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-complete-review-v48"
SOURCE_SET = "kitchen-ligne-claire-complete-review-v49"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v48"
PAGE = ROOT / "public/keeper-review" / SET / "index.html"
ARCHIVE = ROOT / "review-archive/sets" / f"{SET}.json"
SOURCE_ARCHIVE = ROOT / "review-archive/sets" / f"{SOURCE_SET}.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> None:
    if ARCHIVE.exists() or (PACK / "batch-register.json").exists():
        raise RuntimeError("refusing to overwrite completed V48 records")
    source = json.loads(SOURCE_ARCHIVE.read_text())
    entries = {}
    for route, record in source["entries"].items():
        entries[route.replace(SOURCE_SET, SET)] = record
    archive = {
        **source,
        "set": SET,
        "page": {"path": PAGE.relative_to(ROOT).as_posix(), "sha256": sha(PAGE), "bytes": PAGE.stat().st_size},
        "entries": entries,
    }
    ARCHIVE.write_text(json.dumps(archive, indent=2) + "\n")
    manifest = PACK / "manifest.json"
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "retained-intermediate-superseded-by-v49-and-v50",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
        "productionWrites": [],
        "candidate": {
            "manifest": {"file": manifest.relative_to(ROOT).as_posix(), "sha256": sha(manifest)},
            "publicShell": {"file": PAGE.relative_to(ROOT).as_posix(), "sha256": sha(PAGE)},
        },
        "publishedAssets": [
            {
                "source": record["object"],
                "sourceSha256": record["sha256"],
                "publicAssemblyPath": "public" + route,
            }
            for route, record in entries.items()
        ],
        "recoveryNote": "V48 stopped before archive registration on a duplicate manifest basename; exact media were retained and this record supplies only the missing content-addressed route map. V49 fixed the builder and V50 is the active review.",
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    print(f"Finalized retained V48 archive record with {len(entries)} asset routes; gate closed")


if __name__ == "__main__":
    build()
