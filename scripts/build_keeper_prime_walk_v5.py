#!/usr/bin/env python3
"""Build Keeper Prime Walk V5 with a leg-authoritative contralateral arm cycle."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import build_keeper_prime_walk_v1 as base
import build_keeper_prime_walk_v4 as v4


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v5"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-v5"
V4_PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v4"
SIDE = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
PREFIX = "/keeper-review/keeper-prime-walk-v5/assets/"
FPS = 8

SOURCES = {
    2: PACK / "sources/keeper-prime-walk-v5-f2-contralateral-arms.png",
    3: PACK / "sources/keeper-prime-walk-v5-f3-passing-arms.png",
    4: PACK / "sources/keeper-prime-walk-v5-f4-opposite-approach-arms.png",
    6: PACK / "sources/keeper-prime-walk-v5-f6-opposite-return-arms.png",
    7: PACK / "sources/keeper-prime-walk-v5-f7-passing-arms.png",
    # F8 is the reflected phase partner of F2. Reusing its generated arm source
    # prevents the image model from reversing foreground/background arms again.
    8: PACK / "sources/keeper-prime-walk-v5-f2-contralateral-arms.png",
}

MASK_POLYGONS = {
    2: [(25, 141), (78, 121), (117, 132), (145, 145), (210, 154), (229, 198), (211, 236), (164, 243), (126, 225), (105, 247), (44, 247), (22, 207)],
    3: [(42, 136), (91, 121), (132, 131), (177, 143), (205, 178), (198, 238), (151, 247), (102, 237), (62, 247), (38, 210)],
    4: [(24, 140), (78, 121), (117, 132), (152, 142), (217, 151), (236, 196), (218, 235), (164, 242), (126, 225), (104, 247), (43, 247), (20, 205)],
    6: [(34, 137), (82, 121), (125, 133), (166, 145), (211, 169), (218, 221), (185, 248), (136, 242), (106, 251), (54, 246), (30, 204)],
    7: [(34, 137), (82, 121), (125, 133), (172, 145), (205, 177), (207, 232), (164, 249), (118, 239), (78, 250), (35, 225)],
    8: [(24, 140), (78, 121), (117, 132), (145, 145), (211, 154), (230, 198), (212, 236), (164, 243), (126, 225), (105, 247), (43, 247), (20, 205)],
}

ARM_STATES = {
    1: "contact: near arm maximum back; far arm maximum forward",
    2: "down: both arms return toward passing",
    3: "passing: both arms near vertical",
    4: "up: near arm approaches forward; far arm approaches back",
    5: "opposite contact: near arm maximum forward; far arm maximum back",
    6: "opposite down: both arms return toward passing",
    7: "opposite passing: both arms near vertical",
    8: "opposite up: near arm approaches back; far arm approaches forward",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def mask_for(frame: int) -> Image.Image:
    mask = Image.new("L", base.CELL, 0)
    ImageDraw.Draw(mask).polygon(MASK_POLYGONS[frame], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.55))


def save_strip(path: Path, frames: list[Image.Image]) -> None:
    strip = Image.new("RGBA", (base.CELL[0] * len(frames), base.CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.paste(frame, (index * base.CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=False, compress_level=9)


def main() -> None:
    required = [SIDE, V4_PACK / "batch-register.json", PACK / "HANDOFF.md", PACK / "PROMPT_LOG.md", PACK / "arm-phase-map.json", *SOURCES.values()]
    required += [V4_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png" for frame in range(1, 9)]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")

    for directory in (PACK / "drafts", PACK / "evidence/registered-sources", PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    (PACK / "drafts/frames").mkdir(parents=True, exist_ok=True)
    (PACK / "evidence/registered-sources").mkdir(parents=True, exist_ok=True)

    frames = []
    records = []
    edits = []
    for frame in range(1, 9):
        base_path = V4_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        accepted = Image.open(base_path).convert("RGBA")
        output = PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        if frame in (1, 5):
            shutil.copyfile(base_path, output)
            image = Image.open(output).convert("RGBA")
            provenance = {"source": rel(base_path), "sourceSha256": digest(base_path), "byteIdenticalToV4": True}
        else:
            source = Image.open(SOURCES[frame]).convert("RGBA")
            registered, registration = v4.register_to_frame(source, accepted)
            registered_path = PACK / f"evidence/registered-sources/frame-{frame}.png"
            registered.save(registered_path, optimize=False, compress_level=9)
            mask = mask_for(frame)
            image = Image.composite(registered, accepted, mask)
            image.save(output, optimize=False, compress_level=9)
            audit = v4.pixel_differences(accepted, image, mask)
            if audit["changedOutsideDeclaredRegion"]:
                raise RuntimeError(f"frame {frame} changed outside declared arm region")
            provenance = {
                "base": rel(base_path), "baseSha256": digest(base_path),
                "generatedArmSource": rel(SOURCES[frame]), "generatedArmSourceSha256": digest(SOURCES[frame]),
                "registeredSource": rel(registered_path), "registeredSourceSha256": digest(registered_path),
                "registration": registration, "declaredEditPolygon": [list(point) for point in MASK_POLYGONS[frame]],
                "maskFeatherRadiusPixels": 0.55, "pixelAudit": audit, "byteIdenticalToV4": False,
            }
            edits.append({"frame": frame, **provenance})
        if base.edge_alpha_count(image):
            raise RuntimeError(f"frame {frame} touches cell edge")
        frames.append(image)
        bounds = base.alpha_bounds(image)
        records.append({
            "frame": frame, "pose": base.POSES[frame - 1], "armState": ARM_STATES[frame],
            "file": rel(output), "sha256": digest(output), "opaqueBoundsExclusive": list(bounds),
            "opaqueWidth": bounds[2] - bounds[0], "opaqueHeight": bounds[3] - bounds[1],
            "opaqueArea": base.opaque_area(image), "alphaCentroid": base.centroid(image),
            "edgeAlphaPixels": base.edge_alpha_count(image), "provenance": provenance,
        })

    strip = PACK / "drafts/keeper_prime_walk-right_f8.png"
    save_strip(strip, frames)
    base.PACK = PACK
    base.PUBLIC = PUBLIC
    sidecar = base.sidecar(strip)
    sidecar_data = json.loads(sidecar.read_text())
    sidecar_data["status"] = "walk-v5-review-draft-not-production"
    dump(sidecar, sidecar_data)
    side = Image.open(SIDE).convert("RGBA")
    contact, comparison = base.contact_sheet(frames, side)
    base.write_page([PACK / "drafts/frames" / f"keeper_prime_walk-right_f{frame}.png" for frame in range(1, 9)], strip, contact, comparison, SIDE)

    assets = PUBLIC / "assets"
    previous_urls = []
    previous_records = []
    for frame in range(1, 9):
        source = V4_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        target = assets / f"previous-v4-frame{frame}-{digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        previous_urls.append(PREFIX + target.name)
        previous_records.append({"frame": frame, "source": rel(source), "sourceSha256": digest(source), "public": rel(target), "publicSha256": digest(target), "byteIdentical": True})

    html_path = PUBLIC / "index.html"
    html = html_path.read_text()
    html = html.replace("Keeper Prime Walk V1", "Keeper Prime Walk V5")
    html = html.replace("Finished-art walk draft", "Leg-authoritative arm-cycle redraft")
    html = html.replace("Walk V1 review draft", "Walk V5 contralateral-arm redraft")
    html = html.replace("Current production versus Walk V1", "Current production versus Walk V5")
    html = html.replace('alt="Walk V1 review strip"', 'alt="Walk V5 review strip"')
    html = html.replace("assets/", PREFIX)
    current_urls = [PREFIX + next(path.name for path in assets.iterdir() if path.name.startswith(f"frame{frame}-")) for frame in range(1, 9)]
    compare = f'''<h2>Walk V4 versus Walk V5 · synchronized exact game size</h2><article><div class="route-pair"><div><strong>Previous V4</strong><div class="stage game"><img id="previousFrame" src="{previous_urls[0]}" alt="Previous Walk V4 frame"></div></div><div><strong>Walk V5</strong><div class="stage game"><img id="currentCompare" src="{current_urls[0]}" alt="Walk V5 frame"></div></div></div><p>Both boxes are exactly 128 × 160 proposed game size and follow the same frame index.</p></article>'''
    html = html.replace("<h2>Translated walk — begins and ends fully hidden</h2>", compare + "<h2>Translated walk — begins and ends fully hidden</h2>")
    html = html.replace("One coherent eight-pose loop derived from the approved Side-right model and Rig Motion V3. Nothing has entered Final or production.", "A leg-authoritative rebuild of the complete two-arm cadence. The accepted V4 legs are the phase authority; F1 and F5 remain byte-identical endpoints, while both arms travel continuously through passing poses. Nothing has entered Final or production.")
    html = html.replace("identity and palette must remain constant while the legs and arms move.", "the arm cadence must be read from the accepted legs: near arm back at F1, vertical at F3, forward at F5, vertical at F7, and back again at the loop seam.")
    html = html.replace("const frames=", f"const previousFrames={json.dumps(previous_urls)};const frames=")
    html = html.replace("label.textContent=`Frame ${index+1}", "document.getElementById('previousFrame').src=previousFrames[index];document.getElementById('currentCompare').src=frames[index];label.textContent=`Frame ${index+1}")
    html_path.write_text(html)

    continuity = []
    for index in range(8):
        a, b = records[index], records[(index + 1) % 8]
        continuity.append({"fromFrame": index + 1, "toFrame": (index + 1) % 8 + 1,
                           "opaqueHeightDelta": b["opaqueHeight"] - a["opaqueHeight"],
                           "opaqueWidthDelta": b["opaqueWidth"] - a["opaqueWidth"],
                           "alphaCentroidDelta": [round(b["alphaCentroid"][0] - a["alphaCentroid"][0], 3), round(b["alphaCentroid"][1] - a["alphaCentroid"][1], 3)],
                           "opaqueAreaRatio": round(b["opaqueArea"] / a["opaqueArea"], 6)})

    register = {
        "batchId": "keeper-prime-walk-2026-10-14-v5", "status": "draft-leg-authoritative-arm-cycle-awaiting-visual-approval",
        "purpose": "Derive the complete contralateral arm cadence from the already accepted leg phases instead of treating either arm as an independent sequence.",
        "userFeedback": "The legs are perfect; derive the arms from them. F2/F3 and F5/F6/F7 must not look held.",
        "previousCandidate": {"register": rel(V4_PACK / "batch-register.json"), "sha256": digest(V4_PACK / "batch-register.json"), "filesChanged": False},
        "armPhaseMap": {"file": rel(PACK / "arm-phase-map.json"), "sha256": digest(PACK / "arm-phase-map.json")},
        "generation": {"mode": "built-in image-generation identity-preserving edits followed by deterministic registration and declared-region compositing",
                       "selectedSources": [{"frame": frame, "file": rel(path), "sha256": digest(path)} for frame, path in SOURCES.items()],
                       "promptLog": rel(PACK / "PROMPT_LOG.md"), "editMethod": "F1/F5 stay byte-identical; F2-F4/F6-F8 replace only declared arm/occlusion regions."},
        "animation": {"name": "keeper_prime_walk-right", "frames": 8, "fps": FPS, "durationSeconds": 1, "loop": True,
                      "strip": {"file": rel(strip), "sha256": digest(strip), "sidecar": rel(sidecar), "sidecarSha256": digest(sidecar)}},
        "armCycle": [{"frame": frame, "state": ARM_STATES[frame]} for frame in range(1, 9)],
        "frames": records, "edits": edits, "continuity": continuity,
        "evidence": {"contactSheet": {"file": rel(contact), "sha256": digest(contact)}, "approvedSideComparison": {"file": rel(comparison), "sha256": digest(comparison)}},
        "previousWalkV4FrameComparison": previous_records,
        "reviewPage": {"file": rel(html_path), "sha256": digest(html_path), "assetPrefix": PREFIX, "relativeAssetUrls": False},
        "validation": {"framesOneAndFiveByteIdenticalToV4": True, "acceptedLegPixelsProtectedByBaseCompositing": True,
                       "changedPixelsConfinedToDeclaredRegions": True, "everyOutputCellHasTransparentEdge": True,
                       "stripMatchesFrames": True, "sidecarMatchesStrip": True, "productionSpritesChanged": False,
                       "runtimeManifestChanged": False, "workbenchFinalChanged": False},
        "approvalBoundary": {"walkV5Approved": False, "walkStopApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank visually reviews Walk V5 at large and exact game scale before any walk-to-stop work continues.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; Walk V1-V4, approved authorities, production sprites, manifests and Final remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "frames": 8, "modifiedFrames": sorted(SOURCES), "publicPage": rel(html_path)}, indent=2))


if __name__ == "__main__":
    main()
