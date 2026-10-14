#!/usr/bin/env python3
"""Build Walk V6 by repairing only V5 frame 8's lower-body contamination."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import build_keeper_prime_walk_v1 as base
import build_keeper_prime_walk_v4 as v4
import build_keeper_prime_walk_v5 as v5


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-v6"
V5_PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v5"
V4_PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v4"
SIDE = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
SOURCE = PACK / "sources/keeper-prime-walk-v6-f8-contralateral-arms.png"
PREFIX = "/keeper-review/keeper-prime-walk-v6/assets/"

# Two deliberately separate polygons: the backward near arm at screen left,
# and the forward far arm plus the V4 foreground-arm removal at screen right.
# Neither polygon owns the central trouser/leg silhouette that V5 corrupted.
MASK_POLYGONS = [
    [(35, 139), (83, 122), (113, 143), (113, 181), (101, 211), (94, 240), (53, 244), (32, 211)],
    [(102, 134), (147, 139), (211, 154), (231, 194), (218, 223), (176, 229), (149, 215), (125, 193)],
]


def arm_mask() -> Image.Image:
    mask = Image.new("L", base.CELL, 0)
    draw = ImageDraw.Draw(mask)
    for polygon in MASK_POLYGONS:
        draw.polygon(polygon, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.45))


def save_strip(path: Path, frames: list[Image.Image]) -> None:
    strip = Image.new("RGBA", (base.CELL[0] * len(frames), base.CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.paste(frame, (index * base.CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=False, compress_level=9)


def main() -> None:
    required = [SOURCE, SIDE, V5_PACK / "batch-register.json", V4_PACK / "batch-register.json", PACK / "HANDOFF.md"]
    required += [V5_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png" for frame in range(1, 9)]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {v5.rel(path)}")

    for directory in (PACK / "drafts", PACK / "evidence/registered-sources", PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    (PACK / "drafts/frames").mkdir(parents=True, exist_ok=True)
    (PACK / "evidence/registered-sources").mkdir(parents=True, exist_ok=True)

    frames: list[Image.Image] = []
    records: list[dict] = []
    for frame in range(1, 9):
        v5_path = V5_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        output = PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        if frame < 8:
            shutil.copyfile(v5_path, output)
            image = Image.open(output).convert("RGBA")
            provenance = {"source": v5.rel(v5_path), "sourceSha256": v5.digest(v5_path), "byteIdenticalToV5": True}
        else:
            accepted = Image.open(V4_PACK / "drafts/frames/keeper_prime_walk-right_f8.png").convert("RGBA")
            generated = Image.open(SOURCE).convert("RGBA")
            registered, registration = v4.register_to_frame(generated, accepted)
            registered_path = PACK / "evidence/registered-sources/frame-8.png"
            registered.save(registered_path, optimize=False, compress_level=9)
            mask = arm_mask()
            image = Image.composite(registered, accepted, mask)
            image.save(output, optimize=False, compress_level=9)
            audit = v4.pixel_differences(accepted, image, mask)
            if audit["changedOutsideDeclaredRegion"]:
                raise RuntimeError("frame 8 changed outside its two tightened arm polygons")
            provenance = {
                "acceptedLowerBodyBase": v5.rel(V4_PACK / "drafts/frames/keeper_prime_walk-right_f8.png"),
                "acceptedLowerBodyBaseSha256": v5.digest(V4_PACK / "drafts/frames/keeper_prime_walk-right_f8.png"),
                "generatedArmSource": v5.rel(SOURCE), "generatedArmSourceSha256": v5.digest(SOURCE),
                "registeredSource": v5.rel(registered_path), "registeredSourceSha256": v5.digest(registered_path),
                "registration": registration,
                "declaredEditPolygons": [[list(point) for point in polygon] for polygon in MASK_POLYGONS],
                "maskFeatherRadiusPixels": 0.45, "pixelAudit": audit, "byteIdenticalToV5": False,
            }
        if base.edge_alpha_count(image):
            raise RuntimeError(f"frame {frame} touches cell edge")
        frames.append(image)
        bounds = base.alpha_bounds(image)
        records.append({
            "frame": frame, "pose": base.POSES[frame - 1], "armState": v5.ARM_STATES[frame],
            "file": v5.rel(output), "sha256": v5.digest(output), "opaqueBoundsExclusive": list(bounds),
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
    sidecar_data["status"] = "walk-v6-frame8-leg-repair-review-draft-not-production"
    v5.dump(sidecar, sidecar_data)
    side = Image.open(SIDE).convert("RGBA")
    contact, comparison = base.contact_sheet(frames, side)
    base.write_page([PACK / "drafts/frames" / f"keeper_prime_walk-right_f{frame}.png" for frame in range(1, 9)], strip, contact, comparison, SIDE)

    assets = PUBLIC / "assets"
    previous_urls = []
    previous_records = []
    for frame in range(1, 9):
        source = V5_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        target = assets / f"previous-v5-frame{frame}-{v5.digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        previous_urls.append(PREFIX + target.name)
        previous_records.append({"frame": frame, "source": v5.rel(source), "sourceSha256": v5.digest(source), "public": v5.rel(target), "publicSha256": v5.digest(target), "byteIdentical": True})

    current_urls = [PREFIX + next(path.name for path in assets.iterdir() if path.name.startswith(f"frame{frame}-")) for frame in range(1, 9)]
    html_path = PUBLIC / "index.html"
    html = html_path.read_text()
    html = html.replace("Keeper Prime Walk V1", "Keeper Prime Walk V6")
    html = html.replace("Finished-art walk draft", "Frame-8 lower-body repair")
    html = html.replace("Walk V1 review draft", "Walk V6 frame-8 repair")
    html = html.replace("Current production versus Walk V1", "Current production versus Walk V6")
    html = html.replace('alt="Walk V1 review strip"', 'alt="Walk V6 review strip"')
    html = html.replace("assets/", PREFIX)
    compare = f'''<h2>Walk V5 versus Walk V6 · synchronized exact game size</h2><article><div class="route-pair"><div><strong>Previous V5</strong><div class="stage game"><img id="previousFrame" src="{previous_urls[0]}" alt="Previous Walk V5 frame"></div></div><div><strong>Walk V6 repaired</strong><div class="stage game"><img id="currentCompare" src="{current_urls[0]}" alt="Walk V6 frame"></div></div></div><p>Use Previous/Next to inspect F8. F1–F7 are byte-identical; only F8 changes.</p></article>'''
    html = html.replace("<h2>Translated walk — begins and ends fully hidden</h2>", compare + "<h2>Translated walk — begins and ends fully hidden</h2>")
    html = html.replace("One coherent eight-pose loop derived from the approved Side-right model and Rig Motion V3. Nothing has entered Final or production.", "A narrow correction of Walk V5 frame 8. V5 accidentally admitted frame-2 trouser pixels through an over-broad arm mask. V6 restores the accepted V4 frame-8 lower body and changes only two tightened arm polygons. F1–F7 are exact V5 bytes. Nothing has entered Final or production.")
    html = html.replace("identity and palette must remain constant while the legs and arms move.", "frame 8 must retain V5's correct opposing-arm direction while its trousers, legs and boots match the accepted frame-8 base without warping.")
    html = html.replace("const frames=", f"const previousFrames={json.dumps(previous_urls)};const frames=")
    html = html.replace("label.textContent=`Frame ${index+1}", "document.getElementById('previousFrame').src=previousFrames[index];document.getElementById('currentCompare').src=frames[index];label.textContent=`Frame ${index+1}")
    html_path.write_text(html)

    register = {
        "batchId": "keeper-prime-walk-2026-10-14-v6", "status": "draft-frame8-lower-body-repair-awaiting-visual-approval",
        "purpose": "Repair only V5 frame 8's warped legs by separating arm ownership from the accepted lower-body pixels.",
        "userFeedback": "something has gone wrong with frame 8, legs warped.",
        "previousCandidate": {"register": v5.rel(V5_PACK / "batch-register.json"), "sha256": v5.digest(V5_PACK / "batch-register.json"), "filesChanged": False},
        "acceptedFrame8Base": {"file": v5.rel(V4_PACK / "drafts/frames/keeper_prime_walk-right_f8.png"), "sha256": v5.digest(V4_PACK / "drafts/frames/keeper_prime_walk-right_f8.png")},
        "generation": {"mode": "no new generation; deterministic reuse of V5's selected smooth arm source with tightened two-polygon compositing",
                       "selectedSource": {"file": v5.rel(SOURCE), "sha256": v5.digest(SOURCE)},
                       "editMethod": "F1-F7 exact V5; F8 rebuilt from accepted V4 F8 with only the two arms and immediate occlusion pixels admitted."},
        "animation": {"name": "keeper_prime_walk-right", "frames": 8, "fps": 8, "durationSeconds": 1, "loop": True,
                      "strip": {"file": v5.rel(strip), "sha256": v5.digest(strip), "sidecar": v5.rel(sidecar), "sidecarSha256": v5.digest(sidecar)}},
        "frames": records, "previousWalkV5FrameComparison": previous_records,
        "evidence": {"contactSheet": {"file": v5.rel(contact), "sha256": v5.digest(contact)}, "approvedSideComparison": {"file": v5.rel(comparison), "sha256": v5.digest(comparison)}},
        "reviewPage": {"file": v5.rel(html_path), "sha256": v5.digest(html_path), "assetPrefix": PREFIX, "relativeAssetUrls": False},
        "validation": {"framesOneThroughSevenByteIdenticalToV5": True, "frame8ChangesConfinedToTwoArmPolygons": True,
                       "frame8LowerBodyRestoredFromAcceptedV4Base": True, "everyOutputCellHasTransparentEdge": True,
                       "stripMatchesFrames": True, "sidecarMatchesStrip": True, "productionSpritesChanged": False,
                       "runtimeManifestChanged": False, "workbenchFinalChanged": False},
        "approvalBoundary": {"walkV6Approved": False, "walkStopApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank checks repaired F8 legs and the F7-F8-F1 loop at large and exact game scale.",
        "rollback": f"Delete only {v5.rel(PACK)} and {v5.rel(PUBLIC)}; Walk V1-V5, approved authorities, production sprites, manifests and Final remain unchanged.",
    }
    v5.dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "modifiedFrames": [8], "publicPage": v5.rel(html_path)}, indent=2))


if __name__ == "__main__":
    main()
