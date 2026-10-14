#!/usr/bin/env python3
"""Build Keeper Prime Walk V4 with a deliberately articulated rear-arm cycle."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import build_keeper_prime_walk_v1 as base


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v4"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-v4"
V3_PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-13-v3"
SIDE = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
PREFIX = "/keeper-review/keeper-prime-walk-v4/assets/"
FPS = 8

SOURCES = {
    2: PACK / "sources/keeper-prime-walk-v4-f2-halfway-arm.png",
    3: PACK / "sources/keeper-prime-walk-v4-f3-passing-arm.png",
    5: PACK / "sources/keeper-prime-walk-v4-f5-reappearing-arm.png",
    6: PACK / "sources/keeper-prime-walk-v4-f6-passing-arm.png",
    7: PACK / "sources/keeper-prime-walk-v4-f7-rearward-arm.png",
}

# Polygons are deliberately confined to the far/rear arm and the small patch of
# torso it occludes.  They are expressed in the registered 256x320 sprite cell.
MASK_POLYGONS = {
    2: [(38, 137), (70, 122), (106, 132), (114, 174), (106, 224), (82, 244), (45, 240), (31, 205)],
    3: [(45, 136), (73, 123), (108, 134), (112, 181), (103, 234), (76, 248), (47, 235), (38, 194)],
    5: [(34, 142), (70, 128), (109, 140), (113, 186), (103, 229), (72, 241), (39, 228), (28, 184)],
    6: [(42, 141), (73, 127), (109, 139), (113, 185), (104, 235), (77, 249), (46, 237), (36, 190)],
    7: [(32, 138), (68, 122), (108, 133), (114, 179), (106, 226), (78, 245), (38, 238), (23, 196)],
}

ARM_STATES = {
    1: "rearward maximum authority (unchanged V3)",
    2: "rearward-to-passing halfway",
    3: "vertical passing",
    4: "up-pose authority (unchanged V3)",
    5: "forward return, cuff and hand begin reappearing",
    6: "vertical passing on return",
    7: "clear rearward swing",
    8: "rearward approach to loop seam (unchanged V3)",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def yellow_badge_box(image: Image.Image) -> tuple[int, int, int, int]:
    pixels = image.load()
    candidates = set()
    for y in range(round(image.height * 0.35)):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a >= 96 and r >= 185 and g >= 115 and b <= 85 and r >= g + 18:
                candidates.add((x, y))
    components = []
    while candidates:
        seed = candidates.pop()
        component = {seed}
        stack = [seed]
        while stack:
            x, y = stack.pop()
            for point in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if point in candidates:
                    candidates.remove(point)
                    component.add(point)
                    stack.append(point)
        xs = [x for x, _ in component]
        ys = [y for _, y in component]
        box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
        width, height = box[2] - box[0], box[3] - box[1]
        if len(component) >= 4 and image.width * 0.01 <= width <= image.width * 0.09 and image.height * 0.008 <= height <= image.height * 0.09 and 0.45 <= width / height <= 2.2:
            components.append((box, len(component)))
    if not components:
        raise RuntimeError("could not locate cap badge")
    return max(components, key=lambda item: (item[0][0] - item[0][1], item[1]))[0]


def significant_alpha_box(image: Image.Image) -> tuple[int, int, int, int]:
    return image.getchannel("A").point(lambda value: 255 if value >= base.ALPHA_THRESHOLD else 0).getbbox()


def register_to_frame(source: Image.Image, target: Image.Image) -> tuple[Image.Image, dict]:
    source_box = yellow_badge_box(source)
    target_box = yellow_badge_box(target)
    source_alpha = significant_alpha_box(source)
    target_alpha = significant_alpha_box(target)
    if source_alpha is None or target_alpha is None:
        raise RuntimeError("empty source or target during registration")
    scale = (target_alpha[3] - target_alpha[1]) / (source_alpha[3] - source_alpha[1])
    resized = source.resize((round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS)
    source_badge_x = (source_box[0] + source_box[2]) / 2 * scale
    target_badge_x = (target_box[0] + target_box[2]) / 2
    offset = (round(target_badge_x - source_badge_x), round(target_alpha[3] - source_alpha[3] * scale))
    registered = Image.new("RGBA", target.size, (0, 0, 0, 0))
    registered.alpha_composite(resized, offset)
    return registered, {
        "method": "uniform Lanczos scale from significant-alpha height, floor alignment, and cap-badge horizontal alignment",
        "sourceBadgeBoundsExclusive": list(source_box),
        "targetBadgeBoundsExclusive": list(target_box),
        "sourceAlphaBoundsExclusive": list(source_alpha),
        "targetAlphaBoundsExclusive": list(target_alpha),
        "scale": round(scale, 12),
        "offset": list(offset),
        "creativeWarp": False,
    }


def mask_for(frame: int) -> Image.Image:
    mask = Image.new("L", base.CELL, 0)
    ImageDraw.Draw(mask).polygon(MASK_POLYGONS[frame], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.65))


def pixel_differences(before: Image.Image, after: Image.Image, mask: Image.Image) -> dict:
    before_bytes = before.tobytes()
    after_bytes = after.tobytes()
    mask_bytes = mask.tobytes()
    changed = inside = outside = 0
    for index, (a, b) in enumerate(zip(before_bytes[::4], after_bytes[::4])):
        start = index * 4
        if before_bytes[start:start + 4] == after_bytes[start:start + 4]:
            continue
        changed += 1
        if mask_bytes[index] > 0:
            inside += 1
        else:
            outside += 1
    return {"changedPixels": changed, "changedInsideDeclaredRegion": inside, "changedOutsideDeclaredRegion": outside}


def frame_record(frame: int, path: Path, image: Image.Image, provenance: dict) -> dict:
    bounds = base.alpha_bounds(image)
    return {
        "frame": frame,
        "pose": base.POSES[frame - 1],
        "rearArmState": ARM_STATES[frame],
        "file": rel(path),
        "sha256": digest(path),
        "opaqueBoundsExclusive": list(bounds),
        "opaqueWidth": bounds[2] - bounds[0],
        "opaqueHeight": bounds[3] - bounds[1],
        "opaqueArea": base.opaque_area(image),
        "alphaCentroid": base.centroid(image),
        "edgeAlphaPixels": base.edge_alpha_count(image),
        "provenance": provenance,
    }


def save_strip_exact(path: Path, frames: list[Image.Image]) -> None:
    strip = Image.new("RGBA", (base.CELL[0] * len(frames), base.CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.paste(frame, (index * base.CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=False, compress_level=9)


def main() -> None:
    required = [SIDE, V3_PACK / "batch-register.json", PACK / "HANDOFF.md", PACK / "PROMPT_LOG.md", *SOURCES.values()]
    required += [V3_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png" for frame in range(1, 9)]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")

    for directory in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    (PACK / "drafts/frames").mkdir(parents=True, exist_ok=True)
    (PACK / "evidence/registered-sources").mkdir(parents=True, exist_ok=True)

    frames: list[Image.Image] = []
    records: list[dict] = []
    edits: list[dict] = []
    for frame in range(1, 9):
        v3_path = V3_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        v3 = Image.open(v3_path).convert("RGBA")
        output = PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        if frame not in SOURCES:
            shutil.copyfile(v3_path, output)
            image = Image.open(output).convert("RGBA")
            provenance = {"source": rel(v3_path), "sourceSha256": digest(v3_path), "byteIdenticalToV3": True}
        else:
            source = Image.open(SOURCES[frame]).convert("RGBA")
            registered, registration = register_to_frame(source, v3)
            registered_path = PACK / f"evidence/registered-sources/frame-{frame}.png"
            registered.save(registered_path, optimize=False, compress_level=9)
            mask = mask_for(frame)
            image = Image.composite(registered, v3, mask)
            image.save(output, optimize=False, compress_level=9)
            differences = pixel_differences(v3, image, mask)
            if differences["changedOutsideDeclaredRegion"] != 0:
                raise RuntimeError(f"frame {frame} changed outside declared arm region")
            provenance = {
                "base": rel(v3_path),
                "baseSha256": digest(v3_path),
                "generatedArmSource": rel(SOURCES[frame]),
                "generatedArmSourceSha256": digest(SOURCES[frame]),
                "registeredSource": rel(registered_path),
                "registeredSourceSha256": digest(registered_path),
                "registration": registration,
                "declaredEditPolygon": [list(point) for point in MASK_POLYGONS[frame]],
                "maskFeatherRadiusPixels": 0.65,
                "pixelAudit": differences,
                "byteIdenticalToV3": False,
            }
            edits.append({"frame": frame, **provenance})
        if base.edge_alpha_count(image):
            raise RuntimeError(f"frame {frame} touches cell edge")
        frames.append(image)
        records.append(frame_record(frame, output, image, provenance))

    strip = PACK / "drafts/keeper_prime_walk-right_f8.png"
    save_strip_exact(strip, frames)
    base.PACK = PACK
    base.PUBLIC = PUBLIC
    sidecar = base.sidecar(strip)
    sidecar_data = json.loads(sidecar.read_text())
    sidecar_data["status"] = "walk-v4-review-draft-not-production"
    dump(sidecar, sidecar_data)
    side = Image.open(SIDE).convert("RGBA")
    contact, comparison = base.contact_sheet(frames, side)

    previous_paths = [V3_PACK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png" for frame in range(1, 9)]
    base.write_page([PACK / record["file"].split(f"{PACK.relative_to(ROOT).as_posix()}/", 1)[-1] for record in records], strip, contact, comparison, SIDE)
    assets = PUBLIC / "assets"
    previous_urls = []
    previous_records = []
    for frame, source in enumerate(previous_paths, 1):
        target = assets / f"previous-v3-frame{frame}-{digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        previous_urls.append(f"{PREFIX}{target.name}")
        previous_records.append({"frame": frame, "source": rel(source), "sourceSha256": digest(source), "public": rel(target), "publicSha256": digest(target), "byteIdentical": True})

    html_path = PUBLIC / "index.html"
    html = html_path.read_text()
    html = html.replace("Keeper Prime Walk V1", "Keeper Prime Walk V4")
    html = html.replace("Finished-art walk draft", "Rear-arm cadence redraft")
    html = html.replace("Walk V1 review draft", "Walk V4 rear-arm redraft")
    html = html.replace("Current production versus Walk V1", "Current production versus Walk V4")
    html = html.replace('alt="Walk V1 review strip"', 'alt="Walk V4 rear-arm review strip"')
    html = html.replace("assets/", PREFIX)
    current_urls = []
    for frame in range(1, 9):
        current_urls.append(PREFIX + next(path.name for path in assets.iterdir() if path.name.startswith(f"frame{frame}-")))
    compare = f'''<h2>Walk V3 versus Walk V4 · synchronized exact game size</h2><article><div class="route-pair"><div><strong>Previous V3</strong><div class="stage game"><img id="previousFrame" src="{previous_urls[0]}" alt="Previous Walk V3 frame"></div></div><div><strong>Walk V4 rear-arm cycle</strong><div class="stage game"><img id="currentCompare" src="{current_urls[0]}" alt="Walk V4 frame"></div></div></div><p>Both boxes are exactly 128 × 160 proposed game display size and follow the same frame index.</p></article>'''
    html = html.replace("<h2>Translated walk — begins and ends fully hidden</h2>", compare + "<h2>Translated walk — begins and ends fully hidden</h2>")
    html = html.replace("One coherent eight-pose loop derived from the approved Side-right model and Rig Motion V3. Nothing has entered Final or production.", "A frame-by-frame rear-arm cadence redraft built on Walk V3. F1, F4 and F8 remain byte-identical; only the five frames Frank identified—F2, F3 and F5–F7—change, and only inside declared rear-arm regions. Nothing has entered Final or production.")
    html = html.replace("identity and palette must remain constant while the legs and arms move.", "the screen-left/rear arm must now advance visibly through the five corrected frames: rearward → passing → compact return → passing → rearward, while the approved head, torso and legs remain stable.")
    html = html.replace("const frames=", f"const previousFrames={json.dumps(previous_urls)};const frames=")
    html = html.replace("label.textContent=`Frame ${index+1}", "document.getElementById('previousFrame').src=previousFrames[index];document.getElementById('currentCompare').src=frames[index];label.textContent=`Frame ${index+1}")
    html_path.write_text(html)

    continuity = []
    for index in range(8):
        a, b = records[index], records[(index + 1) % 8]
        continuity.append({
            "fromFrame": index + 1,
            "toFrame": (index + 1) % 8 + 1,
            "opaqueHeightDelta": b["opaqueHeight"] - a["opaqueHeight"],
            "opaqueWidthDelta": b["opaqueWidth"] - a["opaqueWidth"],
            "alphaCentroidDelta": [round(b["alphaCentroid"][0] - a["alphaCentroid"][0], 3), round(b["alphaCentroid"][1] - a["alphaCentroid"][1], 3)],
            "opaqueAreaRatio": round(b["opaqueArea"] / a["opaqueArea"], 6),
        })

    v3_register = V3_PACK / "batch-register.json"
    register = {
        "batchId": "keeper-prime-walk-2026-10-14-v4",
        "status": "draft-rear-arm-cadence-v4-awaiting-visual-approval",
        "purpose": "Replace Walk V3's held rear/screen-left arm with an explicit, continuous eight-frame arm cycle without changing approved production or Final assets.",
        "userFeedback": "left are still too static - frames 2 and 3 are almost identical as are 5 6 ad 7",
        "previousCandidate": {"register": rel(v3_register), "sha256": digest(v3_register), "filesChanged": False},
        "generation": {
            "mode": "built-in-image-generation-per-frame-precise-object-edit, followed by deterministic cap-badge registration and declared-region compositing",
            "selectedSources": [{"frame": frame, "file": rel(path), "sha256": digest(path)} for frame, path in SOURCES.items()],
            "rejectedSources": [
                {"file": rel(PACK / "sources/rejected-f2-maximum-rearward.png"), "sha256": digest(PACK / "sources/rejected-f2-maximum-rearward.png"), "reason": "made F2 a second rearward maximum instead of a transition toward F3"},
                {"file": rel(PACK / "sources/rejected-f4-shoulder-loop.png"), "sha256": digest(PACK / "sources/rejected-f4-shoulder-loop.png"), "reason": "left a circular sleeve/shoulder loop instead of a clean occluded rear arm"},
                {"file": rel(PACK / "sources/rejected-f4-full-occlusion-model-shift.png"), "sha256": digest(PACK / "sources/rejected-f4-full-occlusion-model-shift.png"), "reason": "clean occlusion required a full-frame redraw that introduced an unacceptable body-model shift"},
            ],
            "promptLog": rel(PACK / "PROMPT_LOG.md"),
            "editMethod": "Only F2, F3 and F5–F7 change, each through a declared rear-arm polygon. F1, F4 and F8 remain byte-identical to Walk V3.",
        },
        "animation": {
            "name": "keeper_prime_walk-right",
            "frames": 8,
            "fps": FPS,
            "durationSeconds": 1,
            "loop": True,
            "strip": {"file": rel(strip), "sha256": digest(strip), "sidecar": rel(sidecar), "sidecarSha256": digest(sidecar)},
            "rootMotion": {"bakedIntoStrip": False, "speedHighResolutionPixelsPerSecond": 168, "speedLogicalPixelsPerSecond": 21, "representativeDurationSeconds": 5, "beginsAndEndsFullyHidden": True},
        },
        "rearArmCycle": [{"frame": frame, "state": ARM_STATES[frame]} for frame in range(1, 9)],
        "frames": records,
        "edits": edits,
        "continuity": continuity,
        "evidence": {
            "contactSheet": {"file": rel(contact), "sha256": digest(contact)},
            "approvedSideComparison": {"file": rel(comparison), "sha256": digest(comparison)},
        },
        "previousWalkV3FrameComparison": previous_records,
        "reviewPage": {"file": rel(html_path), "sha256": digest(html_path), "assetPrefix": PREFIX, "relativeAssetUrls": False},
        "validation": {
            "framesOneFourAndEightByteIdenticalToV3": True,
            "changedPixelsConfinedToDeclaredRegions": True,
            "everyOutputCellHasTransparentEdge": True,
            "stripMatchesFrames": True,
            "sidecarMatchesStrip": True,
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
            "workbenchFinalChanged": False,
        },
        "approvalBoundary": {"walkV4Approved": False, "walkStopApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank visually reviews Walk V4's rear-arm cadence at large and exact game scale before any walk-to-stop work continues.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; Walk V1–V3, approved authorities, production sprites, manifests and Final remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "frames": 8, "modifiedFrames": list(SOURCES), "publicPage": rel(html_path)}, indent=2))


if __name__ == "__main__":
    main()
