#!/usr/bin/env python3
"""Build/verify V47 by reusing the deterministic V46 family builder."""

from __future__ import annotations

import argparse

import build_kitchen_kettle_bubble_authority_v46 as family


family.SET = "kitchen-kettle-bubble-authority-v47"
family.VERSION = 47
family.PACK = family.ROOT / "art/drafts/kitchen-kettle-bubble-authority-2026-10-22-v47"
family.BROKEN_SOURCE = family.PACK / "source/kettle-broken-imagegen-source.png"
family.BROKEN_EFFECT_DX = 27
family.BROKEN_EFFECT_DY = -78
family.DIRECTION = (
    "Use the approved Bubble kettle as the intact kitchen authority; preserve V46's broken-handle idea, "
    "make the damage less restrained, detach the lid completely and pour separate steam from the open top."
)
family.STATUS = "immutable-review-candidate-not-approved-not-promoted"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    family.verify() if args.verify else family.build()


if __name__ == "__main__":
    main()
