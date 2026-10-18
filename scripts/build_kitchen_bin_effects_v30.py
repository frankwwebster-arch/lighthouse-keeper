#!/usr/bin/env python3
"""Build Kitchen V30: exact V29 palette with a taller, fuller stench cloud."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
V29_RAW = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v29"
RAW_DIR = ROOT / "art/raw/kitchen-bin-effects-2026-10-18-v30"
DRAFT_DIR = ROOT / "art/drafts/kitchen-bin-effects-2026-10-18-v30"
PUBLIC_DIR = ROOT / "public/keeper-review/kitchen-bin-effects-v30"
ASSET_DIR = PUBLIC_DIR / "assets"
V29_PAGE = ROOT / "public/keeper-review/kitchen-bin-effects-v29/index.html"

PRESERVED_HASHES = {
    "bin-standard.png": "86b05224a7da5fc5c05918f2875018920ed54cf46fc00cb08952ffd29789f9c0",
    "bin-broken-overflowing.png": "77ad87fabfd3e5c10a4a14f294af343a5d93a2a2015e6d77f18a4140b1f5fb4f",
    "kitchen-bin-standard-in-situ.png": "027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674",
    "kitchen-bin-broken-in-situ.png": "bf1c741f9ff7e985ddc44584c9c13c76c60e0df8104d34a2a11848f1be58a1c3",
    "fx-slow-flies-f40.png": "28f3b35fdfe91d655ebe47914d17c948203f2def6bfa6b8fd5e2bf0a2b86cc5c",
}
V29_MIASMA_SHA = "4eed9dfb501d965d761669bf7ccbe563b18c175e87ab39bffd7ee5c41a795d6c"

FX_CELL_SIZE = (80, 80)
FX_FRAMES = 40
FX_FPS = 4
FX_ROOM_TOP_LEFT = (4, 104)

# Every opaque colour below is taken verbatim from V29. V30 changes the cloud
# silhouette and reach, not Frank's approved colour treatment.
THROAT = (58, 100, 45, 122)
SOURCE_GLOW = (104, 148, 75, 90)
DARK = (50, 96, 43, 102)
DARK_SOFT = (46, 87, 39, 76)
MID = (58, 106, 48, 88)
MID_SOFT = (65, 110, 51, 48)
LIGHT = (108, 148, 77, 58)
LIGHT_SOFT = (118, 158, 86, 50)
EDGE = (101, 141, 72, 44)
TRACE = (105, 146, 72, 34)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def periodic(frame: int, phase: float = 0.0) -> float:
    return math.sin(math.tau * frame / FX_FRAMES + phase)


def cloud_mass(
    frame: Image.Image,
    centre_x: int,
    centre_y: int,
    width: int,
    height: int,
    phase_step: int,
    fill: tuple[int, int, int, int],
    inner: tuple[int, int, int, int],
) -> None:
    """Draw one asymmetrical, translucent pixel-cloud sheet."""
    draw = ImageDraw.Draw(frame)
    left = centre_x - width // 2
    right = centre_x + width // 2
    top = centre_y - height // 2
    bottom = centre_y + height // 2
    notch = phase_step % 3
    outline = [
        (left + 3 + notch, top),
        (centre_x - 3, top - 2),
        (centre_x + 5, top),
        (right - 2, top + 2),
        (right + 1, centre_y - 1),
        (right - 3, bottom - 1),
        (centre_x + 4, bottom + 1),
        (centre_x - 4, bottom),
        (left + 1, bottom - 2),
        (left - 1, centre_y + 1),
    ]
    draw.polygon(outline, fill=fill)

    inset = [
        (left + 5, centre_y - 2),
        (centre_x - 2, top + 1),
        (right - 5, centre_y - 2),
        (centre_x + 3, bottom - 2),
        (left + 4, bottom - 3),
    ]
    draw.polygon(inset, fill=inner)

    # Broken edge and negative holes keep the cloud atmospheric rather than a
    # solid cartoon bubble. The cadence advances only every five frames.
    holes = (
        (centre_x - 5 + notch, centre_y - 1),
        (centre_x + 3, centre_y + 2),
        (left + 3, centre_y + (1 if phase_step % 2 else -1)),
    )
    for x, y in holes:
        draw.point((x, y), fill=(0, 0, 0, 0))
    draw.point((right + 2, top + 3 + notch), fill=EDGE)
    draw.point((left - 2, bottom - 3), fill=TRACE)


def draw_stench_frame(frame_index: int) -> Image.Image:
    frame = Image.new("RGBA", FX_CELL_SIZE)
    draw = ImageDraw.Draw(frame)
    origin_x, origin_y = 40, 69
    slow_step = frame_index // 5
    sway = round(2 * periodic(frame_index, 0.25))

    # A narrow continuous throat keeps the whole environmental effect visibly
    # tied to the bin opening in every frame.
    throat = [
        (origin_x - 1, origin_y),
        (origin_x, 65),
        (origin_x + sway // 2, 61),
        (origin_x + sway, 57),
        (origin_x - 1 + sway, 53),
    ]
    draw.line(throat, fill=THROAT, width=2)
    draw.point((origin_x + 1, origin_y), fill=SOURCE_GLOW)

    # A softly branching stem joins three overlapping cloud sheets. The top
    # reaches y=6–8 instead of V29's y≈27, but retains a clear safety gutter.
    left_sway = round(3 * periodic(frame_index, 1.2))
    right_sway = round(4 * periodic(frame_index, 3.4))
    draw.line([(40 + sway, 55), (36 + left_sway, 47), (35 + left_sway, 40)], fill=DARK_SOFT, width=3)
    draw.line([(40 + sway, 55), (44 + right_sway, 46), (45 + right_sway, 36)], fill=MID, width=2)

    cloud_mass(frame, 38 + left_sway, 40, 24, 20, slow_step, DARK, LIGHT)
    cloud_mass(frame, 44 + right_sway, 28, 31, 24, slow_step + 2, MID, LIGHT_SOFT)
    cloud_mass(frame, 38 + round(5 * periodic(frame_index, 5.1)), 16, 36, 22, slow_step + 5, DARK_SOFT, MID_SOFT)

    # Sparse traces dissipate above and beside the high cloud.
    for index in range(5):
        angle = math.tau * (slow_step + index * 2) / 8
        x = 40 + round(math.cos(angle) * (12 + index * 2))
        y = 7 + index * 4 + round(math.sin(angle) * 2)
        draw.point((x, y), fill=MID_SOFT if index % 2 == 0 else TRACE)
    return frame


def make_strip() -> Image.Image:
    strip = Image.new("RGBA", (FX_CELL_SIZE[0] * FX_FRAMES, FX_CELL_SIZE[1]))
    for frame_index in range(FX_FRAMES):
        strip.alpha_composite(draw_stench_frame(frame_index), (frame_index * FX_CELL_SIZE[0], 0))
    return strip


def write_page() -> None:
    page = V29_PAGE.read_text()
    replacements = {
        "Kitchen V29 · quieter bin effects": "Kitchen V30 · taller bin stench cloud",
        "/keeper-review/kitchen-bin-effects-v29/assets": "/keeper-review/kitchen-bin-effects-v30/assets",
        "V29 draft": "V30 draft",
        "Pedal bin · quieter environmental loop": "Pedal bin · taller environmental cloud",
        "The excellent V28 standard and overflowing bin pixels are preserved exactly. Only the two reusable environmental overlays are revised: the greenish miasma is thinner, more diffuse and irregular, the flies are subdued, and both now take ten seconds to repeat at 4 fps. The bin itself remains static.": "The excellent V28 bin pixels, V29 green palette, subdued flies and ten-second timing are preserved exactly. Only the stench silhouette changes: it now rises substantially higher and broadens into a fuller, recognisable cloud above the bin while retaining irregular translucent edges. The bin itself remains static.",
        "Broken plus quieter environmental fault": "Broken plus taller environmental cloud",
        "Subtle reusable greenish miasma effect": "Taller reusable greenish miasma cloud",
        "Reusable subtle greenish miasma loop": "Reusable taller greenish miasma cloud loop",
        "Diffuse greenish miasma": "Taller greenish miasma cloud",
        "V28 remains immutable. V29 changes only the reusable effect strips and their timing.": "V28 and V29 remain immutable. V30 changes only the miasma silhouette and reach; its V29 colour palette and ten-second timing are unchanged.",
    }
    for before, after in replacements.items():
        if before not in page:
            raise RuntimeError(f"V29 review template text missing: {before}")
        page = page.replace(before, after)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    (PUBLIC_DIR / "index.html").write_text(page)


def main() -> None:
    for name, expected in PRESERVED_HASHES.items():
        source = V29_RAW / name
        if sha(source) != expected:
            raise RuntimeError(f"Pinned V29 input changed: {source.relative_to(ROOT)}")
    if sha(V29_RAW / "fx-stench-miasma-f40.png") != V29_MIASMA_SHA:
        raise RuntimeError("Pinned V29 miasma changed")

    for folder in (RAW_DIR, DRAFT_DIR, ASSET_DIR):
        folder.mkdir(parents=True, exist_ok=True)
    for name in PRESERVED_HASHES:
        copy(V29_RAW / name, RAW_DIR / name)

    miasma = make_strip()
    miasma.save(RAW_DIR / "fx-stench-miasma-f40.png", optimize=True)
    output_names = [*PRESERVED_HASHES, "fx-stench-miasma-f40.png"]
    for name in output_names:
        copy(RAW_DIR / name, ASSET_DIR / name)

    catalogue = {
        "version": 30,
        "status": "taller-cloud-miasma-awaiting-visual-confirmation",
        "states": ["standard", "broken_overflowing"],
        "objectSourceVersion": 28,
        "effectSourceVersion": 29,
        "objectPixelsChanged": False,
        "flyPixelsChanged": False,
        "miasmaColourPaletteChanged": False,
        "outputs": {
            name: {
                "sha256": sha(RAW_DIR / name),
                "size": list(Image.open(RAW_DIR / name).size),
            }
            for name in output_names
        },
        "effects": {
            "stench_miasma": {
                "file": "fx-stench-miasma-f40.png",
                "reusable": True,
                "style": "taller-fuller-irregular-translucent-greenish-cloud",
                "frames": FX_FRAMES,
                "fps": FX_FPS,
                "durationSeconds": FX_FRAMES / FX_FPS,
                "cellPixels": list(FX_CELL_SIZE),
                "roomTopLeft": list(FX_ROOM_TOP_LEFT),
                "objectPixelsChanged": False,
                "previousSha256": V29_MIASMA_SHA,
            },
            "slow_flies": {
                "file": "fx-slow-flies-f40.png",
                "reusable": True,
                "frames": FX_FRAMES,
                "fps": FX_FPS,
                "durationSeconds": FX_FRAMES / FX_FPS,
                "cellPixels": list(FX_CELL_SIZE),
                "roomTopLeft": list(FX_ROOM_TOP_LEFT),
                "objectPixelsChanged": False,
                "sfxCue": "kitchen_bin_flies_slow_loop",
            },
        },
        "boundaries": {
            "approved": False,
            "promoted": False,
            "v28ObjectPixelsPreserved": True,
            "v29FlyPixelsPreserved": True,
            "v29MiasmaPalettePreserved": True,
            "objectAnimated": False,
            "environmentalFxAnimated": True,
            "runtimeChanged": False,
            "canonicalChanged": False,
            "v20ThroughV29Changed": False,
        },
    }
    (DRAFT_DIR / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT_DIR / "batch-register.json").write_text(json.dumps({
        "version": 30,
        "preserves": list(range(20, 30)),
        "v29Disposition": "retained as immutable subtle-effect provenance; palette, flies and timing preserved",
        "rollback": "Delete only V30 raw/draft/review/archive/builder/verifier/docs files; V20-V29 remain immutable.",
    }, indent=2) + "\n")
    write_page()
    print(json.dumps({"review": str(PUBLIC_DIR.relative_to(ROOT)), "outputs": len(output_names)}, indent=2))


if __name__ == "__main__":
    main()
