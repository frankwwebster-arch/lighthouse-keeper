#!/usr/bin/env python3
"""Notify this Mac when a changed Keeper review hand-back is ready.

This intentionally runs without Codex. It reads only the public hand-back queue,
keeps a small local record of already-notified batch IDs, and never changes game
assets, review data, or the queue itself.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ENDPOINT = "https://lighthouse-keeper-mu.vercel.app/api/keeper-review-handoffs"
STATE_PATH = (
    Path.home()
    / "Library"
    / "Application Support"
    / "Lighthouse Keeper"
    / "keeper-review-handoff-monitor.json"
)
NOTIFICATION_TITLE = "Lighthouse Keeper review"


def load_state(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError:
        return {"version": 1, "reportedHandoffIds": []}
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"could not read monitor state at {path}: {error}") from error
    if not isinstance(value, dict) or not isinstance(value.get("reportedHandoffIds"), list):
        raise RuntimeError(f"monitor state at {path} has an invalid format")
    return value


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temporary_path = Path(handle.name)
    temporary_path.replace(path)


def fetch_handoffs(endpoint: str) -> list[dict[str, Any]]:
    request = urllib.request.Request(endpoint, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, UnicodeError, urllib.error.URLError, json.JSONDecodeError) as error:
        raise RuntimeError(f"could not read the hand-back queue: {error}") from error
    handoffs = payload.get("handoffs") if isinstance(payload, dict) else None
    if not isinstance(handoffs, list):
        raise RuntimeError("the hand-back queue returned no handoff list")
    return [handoff for handoff in handoffs if isinstance(handoff, dict)]


def changed_count(handoff: dict[str, Any]) -> int | None:
    value = handoff.get("changedAnimationCount")
    if isinstance(value, bool):
        return None
    try:
        count = int(value)
    except (TypeError, ValueError):
        return None
    return count if count >= 0 else None


def pending_changed_handoffs(
    handoffs: list[dict[str, Any]], reported_ids: set[str]
) -> list[dict[str, Any]]:
    pending: list[dict[str, Any]] = []
    for handoff in handoffs:
        handoff_id = handoff.get("id")
        if not isinstance(handoff_id, str) or handoff_id in reported_ids:
            continue
        if (changed_count(handoff) or 0) > 0:
            pending.append(handoff)
    return sorted(pending, key=lambda handoff: str(handoff.get("submittedAt", "")))


def apple_script_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def notification_text(handoff: dict[str, Any]) -> tuple[str, str]:
    count = changed_count(handoff) or 0
    names = handoff.get("changedAnimationNames")
    changed_names = [name for name in names if isinstance(name, str)] if isinstance(names, list) else []
    shown_names = ", ".join(changed_names[:3])
    suffix = f" — {shown_names}" if shown_names else ""
    if len(changed_names) > 3:
        suffix += ", …"
    subtitle = f"{count} changed animation{'s' if count != 1 else ''}{suffix}"
    submitted = handoff.get("submittedAt")
    detail = "Open the live reviewer and start the amendment task."
    if isinstance(submitted, str) and submitted:
        detail = f"Handed back {submitted}. {detail}"
    return subtitle, detail


def notify(handoff: dict[str, Any]) -> None:
    subtitle, detail = notification_text(handoff)
    script = (
        f"display notification {apple_script_string(detail)} "
        f"with title {apple_script_string(NOTIFICATION_TITLE)} "
        f"subtitle {apple_script_string(subtitle)}"
    )
    result = subprocess.run(
        ["/usr/bin/osascript", "-e", script], check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "macOS notification failed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read and report without notifying or saving state")
    parser.add_argument("--endpoint", default=ENDPOINT, help=argparse.SUPPRESS)
    parser.add_argument("--state-file", type=Path, default=STATE_PATH, help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        state = load_state(args.state_file)
        reported_ids = {value for value in state["reportedHandoffIds"] if isinstance(value, str)}
        pending = pending_changed_handoffs(fetch_handoffs(args.endpoint), reported_ids)
        if args.check:
            if pending:
                for handoff in pending:
                    subtitle, detail = notification_text(handoff)
                    print(f"Would notify: {subtitle}\n{detail}\nID: {handoff['id']}")
            else:
                print("No unreported changed Keeper review hand-backs.")
            return 0
        for handoff in pending:
            notify(handoff)
            reported_ids.add(handoff["id"])
        state["version"] = 1
        state["reportedHandoffIds"] = sorted(reported_ids)[-500:]
        save_state(args.state_file, state)
        print(f"Checked {len(pending)} newly changed Keeper review hand-back(s).")
        return 0
    except RuntimeError as error:
        print(f"Keeper review hand-back monitor failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
