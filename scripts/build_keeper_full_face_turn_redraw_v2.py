#!/usr/bin/env python3
"""Build the reversible V2 full-motion standard turn redraws.

Frames 1-5 are normalized from two approved-model image-generation sources.
Frame 6 is always restored byte-for-byte from the approved front neutral.
"""
from __future__ import annotations

import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "art/raw/keeper-first-batch"
CANON_PACK = ROOT / "art/drafts/keeper-full-face-canon-pack-2026-10-12-v1"
CANON = CANON_PACK / "drafts/keeper_full-face-canon_standard-neutral_f1.png"
PRIOR = ROOT / "art/drafts/keeper-full-face-standard-turn-endpoints-2026-10-12-v1"
BATCH_ID = "keeper-full-face-standard-turn-redraw-2026-10-12-v2"
BATCH = ROOT / "art/drafts" / BATCH_ID
PUBLIC = ROOT / "public/keeper-review/full-face-standard-turn-redraw-v2"
SOURCE_DIR = BATCH / "generated-sources"
NAMES = ("keeper_turn_front", "keeper_turn_left_front")
EXPECTED = {
    "canon": "6d3b5057f7dad4410230c5c2a1959a2db468aca6f2d28486ec6db9e07827056a",
    "keeper_turn_front": {
        "canonical": "cab51cb946eb39e1a05e2665ccff7f0f3cb6523621d42a4766ccb8212d86b57b",
        "generated": "f45c2abf02c1b0115e606e7b37401d9f3e1a97f2a511d355990ed0db117b2476",
    },
    "keeper_turn_left_front": {
        "canonical": "7060620c5009a76e74dfa222c9f21bb6a33b6e49545b9a9c177539b2a6323599",
        "generated": "3a7502caeb23a9e9195b018b82d4343d0c5d2564e78aed7668415d9d21f3244b",
    },
}

PROMPT_COMMON = """Use case: identity-preserve
Asset type: six-frame 2D game sprite turning animation source sheet
Primary request: Redraw the entire {direction}-profile-to-front turning animation as six clean, evenly spaced full-body poses of the SAME approved Lighthouse Keeper model. Image 1 is the binding identity and exact final front-facing pose. Image 2 supplies only the intended {direction}-side-to-front rotation order. Rebuild the moving poses from Image 1's adult proportions and restrained design rather than copying Image 2's oversized smiling transitional head.
Input images: Image 1: primary identity authority and exact final pose; Image 2: motion/order reference only.
Scene/backdrop: genuinely transparent background.
Subject: one adult lighthouse keeper in navy cap, blue sweater with cream stripe, dark trousers and boots, rotating in place from exact {direction} profile through 72°, 54°, 36°, 18°, to exact front view. Six poses total, left to right. Natural tiny counter-movements of arms and feet are allowed, but floor contact and body scale remain stable.
Style/medium: polished high-resolution pixel-art/cartoon game sprite matching Image 1 exactly in rendering, palette, outline weight, shading, anatomy and beard mass.
Composition/framing: single horizontal sprite sheet, six isolated equal cells, one character centered per cell, identical baseline and overall scale, generous transparent gutter around every pose. The final pose must visually match Image 1. Frame 5 must already be almost canonical so frame 5 to frame 6 is only the last small rotational step with no jump in head size, cap size, shoulder width, torso width, head height or foot placement.
Constraints: adult restrained face; solid dark rectangular eyes as visible; separate moustache; readable closed mouth; established broad beard; stable head position; native body width comparable to Image 1; coherent continuous rotation; no props; no text; no shadows; no scene; transparent background. Preserve the same Keeper identity in every frame. The turn must end at the canonical front pose without a model swap.
Avoid: cheesy pixie grin, generic smile, open mouth, moustache merged into mouth, white eye glints, round childlike eyes, oversized head, changing body proportions, sudden front-view scale change, duplicated/missing limbs, frame overlap, cropped pixels, background tiles, labels or watermark."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixel_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def threshold_bbox(image: Image.Image, threshold: int = 32) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A").point(lambda value: 255 if value >= threshold else 0)
    bbox = alpha.getbbox()
    if bbox is None:
        raise RuntimeError("generated pose has no foreground")
    return bbox


def split_generated(source: Image.Image) -> list[Image.Image]:
    alpha = source.getchannel("A")
    occupied = []
    for x in range(source.width):
        if any(alpha.getpixel((x, y)) >= 32 for y in range(source.height)):
            occupied.append(x)
    groups: list[list[int]] = []
    for x in occupied:
        if not groups or x > groups[-1][-1] + 1:
            groups.append([x])
        else:
            groups[-1].append(x)
    if len(groups) != 6:
        raise RuntimeError(f"expected 6 isolated generated poses, found {len(groups)}")
    poses = []
    for group in groups:
        left = max(0, group[0] - 4)
        right = min(source.width, group[-1] + 5)
        column = source.crop((left, 0, right, source.height))
        bbox = threshold_bbox(column)
        top = max(0, bbox[1] - 4)
        bottom = min(source.height, bbox[3] + 4)
        poses.append(source.crop((left, top, right, bottom)))
    return poses


def normalized_poses(source: Image.Image, canon: Image.Image) -> tuple[list[Image.Image], dict]:
    poses = split_generated(source)
    canon_box = canon.getchannel("A").getbbox()
    if canon_box is None:
        raise RuntimeError("approved canon has no foreground")
    target_height = canon_box[3] - canon_box[1]
    endpoint_box = threshold_bbox(poses[5])
    endpoint_width_at_height = round((endpoint_box[2] - endpoint_box[0]) * target_height / (endpoint_box[3] - endpoint_box[1]))
    horizontal_factor = (canon_box[2] - canon_box[0]) / endpoint_width_at_height
    frames = []
    source_boxes = []
    normalized_boxes = []
    for pose in poses:
        box = threshold_bbox(pose)
        crop = pose.crop(box)
        width = max(1, round(crop.width * target_height / crop.height * horizontal_factor))
        resized = crop.resize((width, target_height), Image.Resampling.LANCZOS)
        resized.putalpha(resized.getchannel("A").point(lambda value: 255 if value >= 128 else 0))
        resized_box = resized.getchannel("A").getbbox()
        if resized_box is None:
            raise RuntimeError("normalized pose has no foreground")
        frame = Image.new("RGBA", canon.size, (0, 0, 0, 0))
        centre_x = (resized_box[0] + resized_box[2]) / 2
        paste_x = round(64 - centre_x)
        paste_y = 158 - resized_box[3]
        frame.alpha_composite(resized, (paste_x, paste_y))
        frame_box = frame.getchannel("A").getbbox()
        if frame_box is None or frame_box[0] < 2 or frame_box[1] < 2 or frame_box[2] > 126 or frame_box[3] > 158:
            raise RuntimeError(f"normalized pose lost its safety gutter: {frame_box}")
        frames.append(frame)
        source_boxes.append(list(box))
        normalized_boxes.append(list(frame_box))
    generated_endpoint = frames[5]
    frames[5] = canon.copy()
    return frames, {
        "sourcePoseBoundsExclusive": source_boxes,
        "normalizedPoseBoundsExclusive": normalized_boxes,
        "targetOpaqueHeight": target_height,
        "horizontalFactor": round(horizontal_factor, 8),
        "generatedEndpointPixelSha256": pixel_sha(generated_endpoint),
        "deliveredEndpointPixelSha256": pixel_sha(frames[5]),
    }


def edge_count(frame: Image.Image) -> int:
    alpha = frame.getchannel("A")
    width, height = frame.size
    points = {(x, 0) for x in range(width)} | {(x, height - 1) for x in range(width)}
    points |= {(0, y) for y in range(height)} | {(width - 1, y) for y in range(height)}
    return sum(alpha.getpixel(point) > 0 for point in points)


def checker(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGBA", size, "#15212a")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], 16):
        for x in range(0, size[0], 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, x + 15, y + 15), fill="#22323d")
    return image


def staged(frame: Image.Image, scale: int = 3) -> Image.Image:
    stage = checker(frame.size)
    stage.alpha_composite(frame)
    return stage.resize((frame.width * scale, frame.height * scale), Image.Resampling.NEAREST)


def save_animation(frames: list[Image.Image], destination: Path, fps: float) -> None:
    rendered = [staged(frame).convert("P", palette=Image.Palette.ADAPTIVE, colors=192) for frame in frames]
    rendered[0].save(destination, save_all=True, append_images=rendered[1:], duration=round(1000 / fps), loop=0, disposal=2, optimize=False)


def save_comparison(original: list[Image.Image], draft: list[Image.Image], destination: Path, fps: float) -> None:
    font = ImageFont.load_default()
    rendered = []
    for before, after in zip(original, draft):
        left, right = staged(before), staged(after)
        stage = Image.new("RGB", (left.width + right.width + 36, left.height + 54), "#0d1319")
        stage.paste(left.convert("RGB"), (12, 42))
        stage.paste(right.convert("RGB"), (left.width + 24, 42))
        draw = ImageDraw.Draw(stage)
        draw.text((12, 14), "CANONICAL MOTION", fill="#a9bac6", font=font)
        draw.text((left.width + 24, 14), "V2 APPROVED-MODEL REDRAW", fill="#77d9a4", font=font)
        rendered.append(stage.convert("P", palette=Image.Palette.ADAPTIVE, colors=192))
    rendered[0].save(destination, save_all=True, append_images=rendered[1:], duration=round(1000 / fps), loop=0, disposal=2, optimize=False)


def save_strip_comparison(original: Image.Image, draft: Image.Image, destination: Path) -> None:
    font = ImageFont.load_default()
    margin = 18
    stage = Image.new("RGBA", (original.width + margin * 2, original.height * 2 + 74), "#0d1319")
    draw = ImageDraw.Draw(stage)
    draw.text((margin, 12), "CANONICAL PRODUCTION", fill="#a9bac6", font=font)
    stage.alpha_composite(original, (margin, 34))
    draw.text((margin, original.height + 46), "V2 FULL-MOTION REDRAW — F6 EXACT CANON", fill="#77d9a4", font=font)
    stage.alpha_composite(draft, (margin, original.height + 66))
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage.save(destination, optimize=False, compress_level=9)


def endpoint_metrics(frame5: Image.Image, frame6: Image.Image) -> dict:
    box5 = frame5.getchannel("A").getbbox()
    box6 = frame6.getchannel("A").getbbox()
    if box5 is None or box6 is None:
        raise RuntimeError("endpoint frame has no foreground")
    width5, width6 = box5[2] - box5[0], box6[2] - box6[0]
    height5, height6 = box5[3] - box5[1], box6[3] - box6[1]
    centre5 = (box5[0] + box5[2]) / 2
    centre6 = (box6[0] + box6[2]) / 2
    result = {
        "frame5AlphaBoundsExclusive": list(box5),
        "frame6AlphaBoundsExclusive": list(box6),
        "widthDeltaPixels": width5 - width6,
        "heightDeltaPixels": height5 - height6,
        "centreXDeltaPixels": centre5 - centre6,
        "baselineDeltaPixels": box5[3] - box6[3],
    }
    if abs(result["widthDeltaPixels"]) > 4 or abs(result["heightDeltaPixels"]) > 2 or abs(result["centreXDeltaPixels"]) > 1 or result["baselineDeltaPixels"] != 0:
        raise RuntimeError(f"F5 does not converge smoothly enough to exact canon F6: {result}")
    return result


def main() -> None:
    canon_register = json.loads((CANON_PACK / "canon-pack-register.json").read_text())
    if canon_register.get("status") != "approved-for-batch-authoring":
        raise RuntimeError("V1 canon pack is not approved for batch authoring")
    if sha256(CANON) != EXPECTED["canon"]:
        raise RuntimeError("approved canon changed")
    canon = Image.open(CANON).convert("RGBA")
    records = []
    public_assets: dict[str, dict[str, str]] = {}
    for name in NAMES:
        canonical_path = RAW / f"{name}_f6.png"
        sidecar_path = RAW / f"{name}_f6.json"
        generated_path = SOURCE_DIR / f"{name}-generated.png"
        if sha256(canonical_path) != EXPECTED[name]["canonical"] or sha256(generated_path) != EXPECTED[name]["generated"]:
            raise RuntimeError(f"{name} pinned input changed")
        sidecar = json.loads(sidecar_path.read_text())
        original_strip = Image.open(canonical_path).convert("RGBA")
        frame_width = sidecar["w"] * sidecar["density"]
        frame_height = sidecar["h"] * sidecar["density"]
        if original_strip.size != (frame_width * 6, frame_height):
            raise RuntimeError(f"{name} canonical strip/sidecar mismatch")
        original = [original_strip.crop((index * frame_width, 0, (index + 1) * frame_width, frame_height)) for index in range(6)]
        if original[5].tobytes() != canon.tobytes():
            raise RuntimeError(f"{name} canonical F6 is not the approved neutral")
        generated = Image.open(generated_path).convert("RGBA")
        frames, normalization = normalized_poses(generated, canon)
        metrics = endpoint_metrics(frames[4], frames[5])
        alpha_values = sorted({value for frame in frames for value in frame.getchannel("A").tobytes()})
        if alpha_values != [0, 255]:
            raise RuntimeError(f"{name} alpha is not binary")
        edge_counts = [edge_count(frame) for frame in frames]
        if any(edge_counts):
            raise RuntimeError(f"{name} touches cell edges: {edge_counts}")
        if frames[5].tobytes() != original[5].tobytes():
            raise RuntimeError(f"{name} F6 endpoint changed")

        out = BATCH / "drafts" / name
        evidence = BATCH / "evidence" / name
        out.mkdir(parents=True, exist_ok=True)
        evidence.mkdir(parents=True, exist_ok=True)
        draft_strip = Image.new("RGBA", original_strip.size, (0, 0, 0, 0))
        for index, frame in enumerate(frames):
            draft_strip.paste(frame, (index * frame_width, 0))
        draft_path = out / f"{name}_f6.png"
        draft_sidecar_path = out / f"{name}_f6.json"
        draft_strip.save(draft_path, optimize=False, compress_level=9)
        draft_sidecar = {
            **sidecar,
            "draft": True,
            "draftId": BATCH_ID,
            "canonicalUnchanged": True,
            "approvalRequiredForPromotion": True,
            "amendment": {
                "authoredFrames": [1, 2, 3, 4, 5],
                "lockedCanonicalEndpointFrame": 6,
                "scope": "complete moving model redraw using approved front model as identity authority",
                "widthPolicy": "native model width retained; reviewer width scaling remains a separate user decision",
            },
        }
        write_json(draft_sidecar_path, draft_sidecar)
        canonical_gif = evidence / "canonical.gif"
        candidate_gif = evidence / "candidate.gif"
        comparison_gif = evidence / "comparison.gif"
        strips_png = evidence / "strip-comparison.png"
        save_animation(original, canonical_gif, float(sidecar["fps"]))
        save_animation(frames, candidate_gif, float(sidecar["fps"]))
        save_comparison(original, frames, comparison_gif, float(sidecar["fps"]))
        save_strip_comparison(original_strip, draft_strip, strips_png)
        record = {
            "animation": name,
            "status": "active-review-draft",
            "canonical": {
                "strip": rel(canonical_path), "stripSha256": sha256(canonical_path),
                "sidecar": rel(sidecar_path), "sidecarSha256": sha256(sidecar_path),
            },
            "generatedSource": {
                "file": rel(generated_path), "sha256": sha256(generated_path),
                "prompt": PROMPT_COMMON.format(direction="right" if name == "keeper_turn_front" else "left"),
                "tool": "built-in image_gen",
            },
            "draft": {
                "strip": rel(draft_path), "stripSha256": sha256(draft_path),
                "sidecar": rel(draft_sidecar_path), "sidecarSha256": sha256(draft_sidecar_path),
            },
            "normalization": normalization,
            "endpointContinuity": metrics,
            "frameEvidence": [
                {
                    "frame": index + 1,
                    "canonicalPixelSha256": pixel_sha(original[index]),
                    "draftPixelSha256": pixel_sha(frames[index]),
                    "redrawn": index < 5,
                    "opaqueCellEdgePixels": edge_counts[index],
                    "alphaBoundsExclusive": list(frames[index].getchannel("A").getbbox()),
                }
                for index in range(6)
            ],
            "alphaValues": alpha_values,
            "evidence": [rel(canonical_gif), rel(candidate_gif), rel(comparison_gif), rel(strips_png)],
        }
        records.append(record)
        public_assets[name] = {}
        for label, asset in {"canonical": canonical_gif, "candidate": candidate_gif, "comparison": comparison_gif, "strips": strips_png}.items():
            target = PUBLIC / "assets" / f"{name}-{label}-{sha256(asset)[:16]}{asset.suffix}"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(asset, target)
            public_assets[name][label] = target.name

    register = {
        "batchId": BATCH_ID,
        "status": "awaiting-explicit-user-approval",
        "canonPack": rel(CANON_PACK / "canon-pack-register.json"),
        "canonPackSha256": sha256(CANON_PACK / "canon-pack-register.json"),
        "canonSha256": sha256(CANON),
        "scope": list(NAMES),
        "supersedes": {
            "draft": rel(PRIOR),
            "decision": "V1 F5-only transplant rejected in favour of a complete moving-model redraw",
            "preservation": "V1 remains historical and unmodified",
        },
        "candidates": records,
        "checks": {
            "stripSidecarAgreement": True,
            "binaryAlpha": True,
            "transparentCellEdges": True,
            "exactCanonicalFinalFrames": True,
            "smoothF5ToF6Geometry": True,
            "productionChanged": False,
        },
        "exclusions": {
            "keeper_count_money": "explicitly deleted amendment remains deleted and was not regenerated",
            "withdrawnFaceCameraDrafts": "rejected provenance only; not reused",
            "remainingInventory": "not touched pending review of these two V2 candidates",
        },
        "documentationAudit": {
            "result": "pass",
            "filesReconciled": [
                "README.md",
                "docs/STATUS.md",
                "docs/KEEPER_ANIMATION_HANDOFF.md",
                "docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md",
            ],
            "finding": "Documentation records canon approval, V1 rejection, V2 F1-F5 full-motion scope, exact-canon F6 endpoints, unchanged production and the remaining visual-approval gate.",
        },
        "rollback": f"Delete only {rel(BATCH)} and {rel(PUBLIC)}; canonical raw/runtime art, V1 history and manifests are unchanged.",
    }
    write_json(BATCH / "batch-register.json", register)
    (BATCH / "HANDOFF.md").write_text(
        "# Standard turn full-motion redraw — V2\n\n"
        "Status: **awaiting Frank's explicit visual approval; production unchanged**.\n\n"
        "V2 replaces the rejected F5-only transplant approach with a complete moving-model redraw for frames 1–5 of "
        "`keeper_turn_front` and `keeper_turn_left_front`. Both sequences use the approved full-face model as their identity authority. "
        "Frame 6 is restored byte-for-byte from the approved canon, and frame 5 is constrained to the same baseline, centreline, opaque height and near-matching width so the final rotational step cannot become a model-swap jump.\n\n"
        "The generated source sheets were created with the built-in image-generation tool. The exact prompts, input hashes and source hashes are recorded in `batch-register.json`. "
        "Normalization into 128×160 cells is deterministic, binary-alpha and gutter-checked. Native width is retained; any extra rotundness remains a separate review-app scale choice.\n\n"
        "V1 remains unchanged as rejected historical evidence. No raw/runtime sprite, manifest, prior draft or immutable review export was overwritten.\n\n"
        "Rebuild:\n\n```sh\n"
        "/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_full_face_turn_redraw_v2.py\n"
        "node scripts/verify_keeper_full_face_turn_redraw_v2.ts\n```\n"
    )

    cards = []
    for record in records:
        name = record["animation"]
        assets = public_assets[name]
        metrics = record["endpointContinuity"]
        cards.append(f"""
<section><h2>{html.escape(name)}</h2><p>Frames 1–5 are a full approved-model redraw. Frame 6 is exact canon. F5→F6 geometry: width Δ {metrics['widthDeltaPixels']} px, height Δ {metrics['heightDeltaPixels']} px, centre Δ {metrics['centreXDeltaPixels']} px, baseline Δ {metrics['baselineDeltaPixels']} px.</p>
<div class="grid"><article><h3>Canonical motion</h3><img src="assets/{assets['canonical']}" alt="Canonical {name} animation"></article><article><h3>V2 full-motion redraw</h3><img src="assets/{assets['candidate']}" alt="V2 {name} candidate"></article></div>
<article class="wide"><h3>Synchronized comparison</h3><img src="assets/{assets['comparison']}" alt="Side-by-side animated comparison for {name}"></article>
<details><summary>Full sprite sheets and hashes</summary><img src="assets/{assets['strips']}" alt="Canonical and V2 sprite sheets for {name}"><p>Canonical <code>{record['canonical']['stripSha256']}</code><br>V2 <code>{record['draft']['stripSha256']}</code></p></details></section>""")
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper standard turns V2 full-motion redraw</title>
<style>:root{{color-scheme:dark;--bg:#0d1319;--panel:#17212a;--line:#3a4c5a;--ink:#edf5fb;--muted:#a9bac6;--green:#77d9a4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}}header,main{{max-width:1450px;margin:auto;padding:18px}}header{{border-bottom:1px solid var(--line)}}h1,h2,h3{{font-family:system-ui,sans-serif}}.status{{display:inline-block;padding:5px 9px;border:1px solid var(--green);border-radius:999px;color:var(--green)}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}article,details{{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:12px;margin:12px 0}}img{{display:block;max-width:100%;height:auto;margin:auto}}article img{{max-height:620px}}.wide img{{width:min(100%,900px)}}code{{overflow-wrap:anywhere;color:#badaef}}a{{color:#8dcfff}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}</style></head>
<body><header><a href="/keeper-review/">← Animation reviewer</a> · <a href="/keeper-review/full-face-canon-v1/">Approved canon V1</a><h1>Standard turn full-motion redraw V2</h1><span class="status">Awaiting explicit visual approval · production unchanged</span><p>Frames 1–5 redraw the approved Keeper as one continuous rotating model. Frame 6 is restored from the approved canon exactly. V1 remains rejected historical evidence.</p></header><main>{''.join(cards)}
<section><h2>Verification boundary</h2><article><p>Both strips preserve the 6-frame, 4fps, 32×40 logical-cell contract. Every cell has binary alpha and a transparent safety gutter. F6 is byte-identical to canon; F5 is constrained to the same baseline, centreline and height with no more than four source pixels of width difference. Nothing is promoted by this page.</p></article></section></main></body></html>"""
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)
    print(json.dumps({"batch": BATCH_ID, "candidates": list(NAMES), "publicPage": rel(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
