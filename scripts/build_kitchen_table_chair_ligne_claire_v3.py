#!/usr/bin/env python3
"""Build V3 with the real tabletop plane edge in contour ink."""

import argparse

import build_kitchen_table_chair_ligne_claire_v1 as base


base.VERSION = 3
base.SET = "kitchen-table-chair-ligne-claire-v3"
base.DATED = "kitchen-table-chair-ligne-claire-2026-10-22-v3"
base.PACK = base.ROOT / "art" / "drafts" / base.DATED
base.PUBLIC = base.ROOT / "public" / "keeper-review" / base.SET


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    base.verify() if args.verify else base.build()
