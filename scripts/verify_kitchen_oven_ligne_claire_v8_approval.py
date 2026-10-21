#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs/review/kitchen-oven-ligne-claire-v8-approval-2026-10-21.json"
PACK = ROOT / "art/drafts/kitchen-oven-ligne-claire-2026-10-21-v8"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(message)


approval = json.loads(APPROVAL.read_text())
expected = {
    "manifest": PACK / "manifest.json",
    "reviewShell": ROOT / "public/keeper-review/kitchen-oven-ligne-claire-v8/index.html",
    "archiveManifest": ROOT / "review-archive/sets/kitchen-oven-ligne-claire-v8.json",
    "visualAuthority": ROOT / "art/source/kitchen-built-in-state-ligne-claire-2026-10-21-v7/oven-on-user-confirmed-visual-authority.png",
    "candidate": PACK / "candidates/oven/oven-on.png",
    "master": PACK / "masters/oven-on-top-safe-master-8x.png",
    "comparisonEvidence": PACK / "evidence/oven-v7-vs-v8-contact.png",
    "preservedV41Source": ROOT / "art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/oven-on.png",
}

if approval.get("approvalWords") != "approved":
    fail("V8 approval words changed")
if approval.get("visualAuthority") != "current-approved-oven-on":
    fail("V8 is no longer the approved Oven On authority")
if any(approval.get(key) for key in ("runtimeChanged", "finalChanged", "sourceOverwritten")):
    fail("Approval boundary claims an unauthorized mutation")

for key, path in expected.items():
    actual = sha256(path)
    recorded = approval["hashes"].get(key)
    if actual != recorded:
        fail(f"{key} hash changed: expected {recorded}, got {actual}")

gate = json.loads((PACK / "batch-register.json").read_text())
if gate != {
    "schema": "lighthouse-keeper/kitchen-batch-register@8",
    "status": "blocked-pending-explicit-frank-approval",
    "register": False,
    "promote": False,
    "currentSelectorChanges": [],
}:
    fail("Immutable V8 pre-approval gate was rewritten")

with Image.open(expected["candidate"]) as image:
    rgba = image.convert("RGBA")
    if rgba.size != (92, 85):
        fail(f"Candidate canvas changed: {rgba.size}")
    if rgba.getchannel("A").getbbox() != (4, 4, 88, 81):
        fail(f"Candidate alpha bounds changed: {rgba.getchannel('A').getbbox()}")

print("Verified V8 approval: exact Oven On authority registered; immutable pack and V41 source preserved; runtime gate unchanged")
