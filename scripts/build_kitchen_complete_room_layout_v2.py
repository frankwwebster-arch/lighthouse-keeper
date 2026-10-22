#!/usr/bin/env python3
"""Build the reversible complete-room V2 review from pinned V1 cabinetry.

The approved cabinetry/state sources and immutable V1 review crops are copied
byte-for-byte.  Five loose-object crops are derived from one coordinated
high-resolution source sheet and registered to the existing room datums.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-complete-room-layout-2026-10-22-v2"
V1 = ROOT / "art/drafts/kitchen-cabinetry-room-layout-2026-10-22-v1"
SOURCE = ROOT / "art/source/kitchen-loose-object-foundation-2026-10-22-v1/loose-object-construction-sheet.png"
OUT = ROOT / f"art/drafts/{SET}"
PUBLIC = ROOT / "public/keeper-review/kitchen-complete-room-layout-v2"
SOURCE_SHA256 = "3f7be0874d6a3320d89f5c15e5c467d1f71af58d5ed594530e5aef82a4b2df33"
V1_MANIFEST_SHA256 = "18cfad03b5d466e447e8bf7f66f4c5c0d9628c29e37398eecfa8bd74f13d6ffb"

# Source rectangles deliberately do not overlap.  logicalSize is the exact
# room-space draw envelope; the generated master is four times that size.
LOOSE = {
    "toaster": {"rect": [100, 80, 560, 430], "logicalSize": [42, 28], "support": "worktop", "label": "Toaster"},
    "kettle": {"rect": [600, 55, 1000, 430], "logicalSize": [38, 34], "support": "worktop", "label": "Kettle"},
    "bin": {"rect": [1040, 15, 1400, 430], "logicalSize": [32, 52], "support": "floor", "label": "Bin"},
    "table": {"rect": [100, 430, 930, 1000], "logicalSize": [80, 58], "support": "floor", "label": "Table"},
    "chair": {"rect": [950, 430, 1400, 1000], "logicalSize": [35, 79], "support": "floor", "label": "Chair"},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_crop(source: Image.Image, rect: list[int]) -> Image.Image:
    image = source.crop(rect).convert("RGBA")
    alpha = image.getchannel("A")
    alpha = alpha.point(lambda value: 0 if value < 16 else round((value - 16) * 255 / 239))
    image.putalpha(alpha)
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError(f"empty crop {rect}")
    return image.crop(bounds)


def scale_with_gutter(image: Image.Image, name: str, logical_size: list[int]) -> tuple[Image.Image, dict]:
    width, height = [value * 4 for value in logical_size]
    if name == "chair":
        # The source seat begins about 41.5% down the isolated chair.  Split at
        # that physical edge so the final seat top is exactly 7.75 lp (31 room
        # pixels) above the registered floor while total height remains 79 px.
        split = round(image.height * 0.415)
        upper_height = (logical_size[1] - 31) * 4
        lower_height = 31 * 4
        upper = image.crop((0, 0, image.width, split)).resize((width, upper_height), Image.Resampling.LANCZOS)
        lower = image.crop((0, split, image.width, image.height)).resize((width, lower_height), Image.Resampling.LANCZOS)
        visible = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        visible.alpha_composite(upper, (0, 0))
        visible.alpha_composite(lower, (0, upper_height))
    else:
        visible = image.resize((width, height), Image.Resampling.LANCZOS)
    gutter = 16
    output = Image.new("RGBA", (width + gutter * 2, height + gutter * 2), (0, 0, 0, 0))
    output.alpha_composite(visible, (gutter, gutter))
    return output, {
        "masterScale": 4,
        "logicalSize": logical_size,
        "opaqueDrawRect": [4, 4, logical_size[0], logical_size[1]],
        "logicalCanvas": [logical_size[0] + 8, logical_size[1] + 8],
    }


def main() -> None:
    assert sha256(SOURCE) == SOURCE_SHA256, "loose-object source bytes changed"
    v1_manifest_path = V1 / "manifest.json"
    assert sha256(v1_manifest_path) == V1_MANIFEST_SHA256, "V1 room manifest changed"
    v1 = json.loads(v1_manifest_path.read_text())
    source = Image.open(SOURCE).convert("RGBA")
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "assets").mkdir(parents=True, exist_ok=True)

    inherited = {}
    for name, record in v1["assets"].items():
        filename = record["file"]
        original = V1 / "assets" / filename
        assert sha256(original) == record["sha256"]
        for destination in (OUT / "assets" / filename, PUBLIC / "assets" / filename):
            destination.write_bytes(original.read_bytes())
        inherited[name] = dict(record)

    loose_assets = {}
    for name, spec in LOOSE.items():
        isolated = clean_crop(source, spec["rect"])
        output, geometry = scale_with_gutter(isolated, name, spec["logicalSize"])
        filename = f"{name}-loose-object-foundation-v1.png"
        draft_path = OUT / "assets" / filename
        public_path = PUBLIC / "assets" / filename
        output.save(draft_path, optimize=True)
        public_path.write_bytes(draft_path.read_bytes())
        loose_assets[name] = {
            "file": filename,
            "sha256": sha256(draft_path),
            "pixels": list(output.size),
            "sourceRect": spec["rect"],
            "support": spec["support"],
            "label": spec["label"],
            **geometry,
        }

    manifest = {
        **v1,
        "schema": "lighthouse-keeper/kitchen-complete-room-layout@2",
        "set": SET,
        "status": "unapproved-complete-room-layout-review",
        "cabinetryPredecessor": {
            "set": v1["set"],
            "manifestSha256": V1_MANIFEST_SHA256,
            "assetsByteExact": True,
        },
        "looseObjectSource": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": SOURCE_SHA256,
            "generatedTogether": True,
            "changed": False,
        },
        "assets": inherited,
        "looseAssets": loose_assets,
        "looseGeometry": {
            "worktopSupportY": 141,
            "floorSupportY": 208,
            "chairSeatTopHeightLp": 7.75,
            "chairSeatTopHeightRoomPixels": 31,
            "tableTopHeightLp": 14.5,
            "defaultPositions": {
                "toaster": [374, 109],
                "kettle": [334, 103],
                "bin": [728, 152],
                "table": [630, 146],
                "chair": [650, 125],
            },
        },
        "boundaries": {
            **v1["boundaries"],
            "looseObjectArtApproved": False,
            "looseObjectStatesAuthored": False,
            "runtimeChanged": False,
            "productionChanged": False,
        },
    }
    payload = (json.dumps(manifest, indent=2) + "\n").encode()
    (OUT / "manifest.json").write_bytes(payload)
    (PUBLIC / "manifest.json").write_bytes(payload)
    print(json.dumps({"set": SET, "looseAssets": loose_assets}, indent=2))


if __name__ == "__main__":
    main()
