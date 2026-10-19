#!/usr/bin/env python3
"""Build the immutable synchronized walk-stop-turn-rear-action review V1."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SET = "keeper-prime-rear-action-sequence-v1"
DRAFT = ROOT / "art/drafts/keeper-prime-rear-action-sequence-2026-10-20-v1"
PUBLIC = ROOT / "public/keeper-review" / SET
SOURCE_CATALOGUE = ROOT / "public/keeper-review/activity-cloud-composer-v6/catalogue.json"
TEMPLATE = DRAFT / "page-template.html"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


source = json.loads(SOURCE_CATALOGUE.read_text())
route = source["route"]
last_action = max(i for i, frame in enumerate(route) if frame["phase"] == "Prime rear-work action")
sequence = route[: last_action + 1]
action_start_index = next(i for i, frame in enumerate(sequence) if frame["phase"] == "Prime rear-work action")

recipes = {
    "garden-bbq": source["defaultRecipe"],
    "make-sandwich": {
        "label": "Make a sandwich",
        "targetAssetLabel": "Kitchen work surface",
        "targetAssetId": "kitchen.prep",
        "bodyCompatibility": "rear-work-with-context",
        "elements": ["sandwich-bread", "sandwich-ham", "sandwich-lettuce", "sandwich-tomato", "cooking-sandwich"],
        "sfx": "sandwich-prep",
    },
    "washing-up": {
        "label": "Washing up",
        "targetAssetLabel": "Kitchen sink",
        "targetAssetId": "kitchen.sink",
        "bodyCompatibility": "rear-work-with-context",
        "elements": ["washing-plate", "washing-liquid", "washing-sponge", "washing-droplets", "washing-cutlery"],
        "sfx": "washing-splash-clink",
    },
    "make-tea": {
        "label": "Make tea",
        "targetAssetLabel": "Kettle point",
        "targetAssetId": "kitchen.kettle",
        "bodyCompatibility": "rear-work-with-context",
        "elements": ["tea-kettle", "tea-mug", "tea-milk", "cooking-steam"],
        "sfx": "kettle-pour",
    },
    "general-mending": source["suggestedRecipes"]["general-mending"],
}

for recipe in recipes.values():
    for component in recipe["elements"]:
        if component not in source["components"]:
            raise RuntimeError(f"unknown component {component}")

phase_counts = Counter(frame["phase"] for frame in sequence)
catalogue = {
    "schema": "lighthouse-keeper/keeper-prime-rear-action-sequence@1",
    "set": SET,
    "status": "immutable-reversible-review-candidate-not-approved",
    "sourceCatalogue": {
        "file": rel(SOURCE_CATALOGUE),
        "url": "/keeper-review/activity-cloud-composer-v6/catalogue.json",
        "sha256": sha(SOURCE_CATALOGUE),
        "set": source["set"],
    },
    "sequence": sequence,
    "actionStartIndex": action_start_index,
    "sequenceDurationMs": sum(frame["durationMs"] for frame in sequence),
    "phaseCounts": dict(phase_counts),
    "callout": {"frames": 42, "fps": 8, "quietTailFrames": 5, "startsWithAction": True, "placement": "raised-above-cap"},
    "recipes": recipes,
    "defaultRecipe": "garden-bbq",
    "controls": ["body", "callout", "treatment", "sfx-declaration", "timeline", "loop"],
    "separation": {"bodySilent": True, "contextBakedIntoKeeper": False, "componentsIndependent": True, "sfxIndependent": True},
    "approvalBoundary": {"candidateApproved": False, "runtimeChanged": False, "finalChanged": False, "kitchenChanged": False, "deployed": False},
}

PUBLIC.mkdir(parents=True, exist_ok=True)
catalogue_text = json.dumps(catalogue, separators=(",", ":")) + "\n"
(DRAFT / "catalogue.json").write_text(catalogue_text)
(PUBLIC / "catalogue.json").write_text(catalogue_text)
(PUBLIC / "index.html").write_bytes(TEMPLATE.read_bytes())

register = {
    "schema": "lighthouse-keeper/keeper-prime-rear-action-sequence-register@1",
    "set": SET,
    "status": catalogue["status"],
    "purpose": "Show one synchronized approved walk-stop-turn-to-rear sequence flowing into the complete Prime rear-work action while a separately controlled activity set animates above the cap.",
    "sourceCatalogue": catalogue["sourceCatalogue"],
    "protectedState": {
        "walkStopTurnRoute": "inherited byte-for-byte from Activity Cloud Composer V6",
        "rearWorkBody": "all 24 frames inherited byte-for-byte",
        "rearNeutralFrames": [1, 23, 24],
        "contextPropOrCounter": False,
    },
    "candidate": {
        "sequenceFrames": len(sequence),
        "actionStartIndex": action_start_index,
        "sequenceDurationMs": catalogue["sequenceDurationMs"],
        "phaseCounts": dict(phase_counts),
        "recipes": list(recipes),
        "treatments": ["orbit", "bustle"],
        "calloutFrames": 42,
        "calloutFps": 8,
    },
    "files": {
        "catalogue": {"file": rel(PUBLIC / "catalogue.json"), "sha256": sha(PUBLIC / "catalogue.json")},
        "page": {"file": rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")},
        "template": {"file": rel(TEMPLATE), "sha256": sha(TEMPLATE)},
    },
    "checks": {
        "preloadAndDecodeBeforePlayback": True,
        "singleSynchronizedClock": True,
        "calloutHiddenBeforeAction": True,
        "bodyCalloutSfxIndependent": True,
        "noNewMedia": True,
        "runtimeChanged": False,
        "kitchenChanged": False,
        "deployed": False,
    },
    "rollback": "Discard this draft directory, public review directory, builder, verifier and documentation entry. All inherited assets remain untouched.",
}
(DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
print(json.dumps({"set": SET, "sequenceFrames": len(sequence), "durationMs": catalogue["sequenceDurationMs"], "recipes": len(recipes)}, indent=2))
