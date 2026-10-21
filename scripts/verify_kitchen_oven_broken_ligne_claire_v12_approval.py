#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs/review/kitchen-oven-broken-ligne-claire-v12-approval-2026-10-22.json"
PACK = ROOT / "art/drafts/kitchen-oven-broken-ligne-claire-2026-10-21-v12"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(message)


approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
expected = {
    "manifest": PACK / "manifest.json",
    "reviewShell": ROOT / "public/keeper-review/kitchen-oven-broken-ligne-claire-v12/index.html",
    "archiveManifest": ROOT / "review-archive/sets/kitchen-oven-broken-ligne-claire-v12.json",
    "familyEvidence": PACK / "evidence/approved-v8-on-vs-v12-broken-family.png",
}
for asset in manifest["assets"]:
    expected[asset["filename"]] = ROOT / asset["candidateFile"]
expected["fx-oven-broken-symbols.png"] = ROOT / manifest["optionalBrokenSymbolEffect"]["file"]

if approval.get("approvalWords") != "approved":
    fail("V12 approval words changed")
if approval.get("visualAuthority") != "current-approved-oven-broken-family":
    fail("V12 is no longer the approved Broken oven authority")
if any(approval.get(key) for key in ("runtimeChanged", "finalChanged", "sourceOverwritten")):
    fail("V12 approval boundary claims an unauthorized mutation")
for key, path in expected.items():
    actual = sha256(path)
    recorded = approval["hashes"].get(key)
    if actual != recorded:
        fail(f"{key} hash changed: expected {recorded}, got {actual}")

gate = json.loads((PACK / "batch-register.json").read_text(encoding="utf-8"))
if gate != {
    "schema": "lighthouse-keeper/kitchen-batch-register@12",
    "set": "kitchen-oven-broken-ligne-claire-v12",
    "status": "blocked-pending-explicit-frank-approval",
    "register": False,
    "promote": False,
    "currentSelectorChanges": [],
}:
    fail("Immutable V12 pre-approval gate was rewritten")

for name in ("oven-broken.png", "oven-broken-cavity-lit.png", "oven-broken-warning-lit.png", "oven-broken-both-lit.png"):
    with Image.open(expected[name]) as image:
        rgba = image.convert("RGBA")
        if rgba.size != (92, 85) or rgba.getchannel("A").getbbox() != (4, 4, 88, 81):
            fail(f"V12 geometry changed: {name}")

print("Verified V12 approval: exact Broken oven family registered; immutable gate, sources and runtime preserved")
