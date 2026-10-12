#!/usr/bin/env python3
"""Build the first reversible full-face normalization review batch.

Only frame 5 of the two standard-uniform side-to-front turns is amended. Frame
6 is already byte-identical to the approved neutral canon and remains untouched.
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
BATCH_ID = "keeper-full-face-standard-turn-endpoints-2026-10-12-v1"
BATCH = ROOT / "art/drafts" / BATCH_ID
PUBLIC = ROOT / "public/keeper-review/full-face-standard-turn-endpoints-v1"
NAMES = ("keeper_turn_front", "keeper_turn_left_front")
EXPECTED_CANON_SHA = "6d3b5057f7dad4410230c5c2a1959a2db468aca6f2d28486ec6db9e07827056a"
EXPECTED_SOURCE_SHAS = {
    "keeper_turn_front": "cab51cb946eb39e1a05e2665ccff7f0f3cb6523621d42a4766ccb8212d86b57b",
    "keeper_turn_left_front": "7060620c5009a76e74dfa222c9f21bb6a33b6e49545b9a9c177539b2a6323599",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixel_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def edge_count(frame: Image.Image) -> int:
    alpha = frame.getchannel("A")
    width, height = frame.size
    points = {(x, 0) for x in range(width)} | {(x, height - 1) for x in range(width)}
    points |= {(0, y) for y in range(height)} | {(width - 1, y) for y in range(height)}
    return sum(alpha.getpixel(point) > 0 for point in points)


def replacement_mask(size: tuple[int, int]) -> Image.Image:
    """Return the declared F5 head/face replacement zone.

    The wide upper zone removes the non-canonical oversized cap, eyes and ears.
    The narrower lower zone follows the beard envelope and avoids both hands,
    legs and all outer-arm action pixels.
    """
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((18, 0, 111, 75), fill=255)
    draw.rectangle((30, 76, 99, 107), fill=255)
    return mask


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
    palette_frames = [staged(frame).convert("P", palette=Image.Palette.ADAPTIVE, colors=192) for frame in frames]
    palette_frames[0].save(
        destination,
        save_all=True,
        append_images=palette_frames[1:],
        duration=round(1000 / fps),
        loop=0,
        disposal=2,
        optimize=False,
    )


def save_comparison_animation(
    original: list[Image.Image], candidate: list[Image.Image], destination: Path, fps: float
) -> None:
    font = ImageFont.load_default()
    rendered: list[Image.Image] = []
    for before, after in zip(original, candidate):
        left, right = staged(before), staged(after)
        stage = Image.new("RGB", (left.width + right.width + 36, left.height + 54), "#0d1319")
        stage.paste(left.convert("RGB"), (12, 42))
        stage.paste(right.convert("RGB"), (left.width + 24, 42))
        draw = ImageDraw.Draw(stage)
        draw.text((12, 14), "CANONICAL", fill="#a9bac6", font=font)
        draw.text((left.width + 24, 14), "V1 DRAFT", fill="#77d9a4", font=font)
        rendered.append(stage.convert("P", palette=Image.Palette.ADAPTIVE, colors=192))
    rendered[0].save(
        destination,
        save_all=True,
        append_images=rendered[1:],
        duration=round(1000 / fps),
        loop=0,
        disposal=2,
        optimize=False,
    )


def save_strip_comparison(original: Image.Image, candidate: Image.Image, destination: Path) -> None:
    font = ImageFont.load_default()
    margin = 18
    stage = Image.new("RGBA", (original.width + margin * 2, original.height * 2 + 74), "#0d1319")
    draw = ImageDraw.Draw(stage)
    draw.text((margin, 12), "CANONICAL PRODUCTION", fill="#a9bac6", font=font)
    stage.alpha_composite(original, (margin, 34))
    draw.text((margin, original.height + 46), "V1 REVIEW DRAFT — ONLY F5 HEAD/FACE CHANGED", fill="#77d9a4", font=font)
    stage.alpha_composite(candidate, (margin, original.height + 66))
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage.save(destination, optimize=False, compress_level=9)


def main() -> None:
    canon_register = json.loads((CANON_PACK / "canon-pack-register.json").read_text())
    if canon_register.get("status") != "approved-for-batch-authoring":
        raise RuntimeError("V1 canon pack is not approved for batch authoring")
    if sha256(CANON) != EXPECTED_CANON_SHA:
        raise RuntimeError("approved full-face canon changed")
    canon = Image.open(CANON).convert("RGBA")
    if canon.size != (128, 160):
        raise RuntimeError("approved canon geometry changed")
    mask = replacement_mask(canon.size)
    (BATCH / "masks").mkdir(parents=True, exist_ok=True)
    mask_path = BATCH / "masks/frame-5-head-face-replacement-mask.png"
    mask_rgba = Image.new("RGBA", canon.size, (99, 210, 255, 0))
    mask_rgba.putalpha(mask)
    mask_rgba.save(mask_path, optimize=False, compress_level=9)

    candidate_records = []
    public_assets: dict[str, dict[str, str]] = {}
    for name in NAMES:
        source = RAW / f"{name}_f6.png"
        source_sidecar = RAW / f"{name}_f6.json"
        if sha256(source) != EXPECTED_SOURCE_SHAS[name]:
            raise RuntimeError(f"{name} source hash changed")
        sidecar = json.loads(source_sidecar.read_text())
        width = sidecar["w"] * sidecar["density"]
        height = sidecar["h"] * sidecar["density"]
        original_strip = Image.open(source).convert("RGBA")
        if original_strip.size != (width * sidecar["frames"], height):
            raise RuntimeError(f"{name} strip/sidecar geometry mismatch")
        original = [original_strip.crop((i * width, 0, (i + 1) * width, height)) for i in range(sidecar["frames"])]
        candidate = [frame.copy() for frame in original]
        candidate[4] = Image.composite(canon, original[4], mask)

        if candidate[5].tobytes() != canon.tobytes():
            raise RuntimeError(f"{name} F6 no longer matches the approved neutral")
        for index in (0, 1, 2, 3, 5):
            if candidate[index].tobytes() != original[index].tobytes():
                raise RuntimeError(f"{name} F{index + 1} changed unexpectedly")
        before = original[4].load()
        after = candidate[4].load()
        mask_pixels = mask.load()
        changed = []
        outside_changes = 0
        for y in range(height):
            for x in range(width):
                if before[x, y] != after[x, y]:
                    changed.append((x, y))
                    if not mask_pixels[x, y]:
                        outside_changes += 1
        if not changed or outside_changes:
            raise RuntimeError(f"{name} invalid F5 scope ({len(changed)} changes, {outside_changes} outside mask)")
        if any(edge_count(frame) for frame in candidate):
            raise RuntimeError(f"{name} candidate lost its transparent cell gutter")
        alpha_values = sorted({value for frame in candidate for value in frame.getchannel("A").tobytes()})
        if alpha_values != [0, 255]:
            raise RuntimeError(f"{name} candidate alpha is not binary")

        out = BATCH / "drafts" / name
        evidence = BATCH / "evidence" / name
        out.mkdir(parents=True, exist_ok=True)
        evidence.mkdir(parents=True, exist_ok=True)
        strip = Image.new("RGBA", original_strip.size, (0, 0, 0, 0))
        for index, frame in enumerate(candidate):
            strip.paste(frame, (index * width, 0))
        strip_path = out / f"{name}_f6.png"
        sidecar_path = out / f"{name}_f6.json"
        strip.save(strip_path, optimize=False, compress_level=9)
        draft_sidecar = {
            **sidecar,
            "draft": True,
            "draftId": BATCH_ID,
            "canonicalUnchanged": True,
            "approvalRequiredForPromotion": True,
            "amendment": {
                "authoredFrames": [5],
                "unchangedFrames": [1, 2, 3, 4, 6],
                "scope": "declared head/face replacement mask only",
                "endpoint": "F6 remains byte-identical to the approved standing-front neutral",
            },
        }
        write_json(sidecar_path, draft_sidecar)
        original_gif = evidence / "canonical.gif"
        candidate_gif = evidence / "candidate.gif"
        comparison_gif = evidence / "comparison.gif"
        comparison_png = evidence / "strip-comparison.png"
        save_animation(original, original_gif, float(sidecar["fps"]))
        save_animation(candidate, candidate_gif, float(sidecar["fps"]))
        save_comparison_animation(original, candidate, comparison_gif, float(sidecar["fps"]))
        save_strip_comparison(original_strip, strip, comparison_png)
        bbox = [min(x for x, _ in changed), min(y for _, y in changed), max(x for x, _ in changed) + 1, max(y for _, y in changed) + 1]
        record = {
            "animation": name,
            "status": "active-review-draft",
            "canonical": {
                "strip": rel(source),
                "stripSha256": sha256(source),
                "sidecar": rel(source_sidecar),
                "sidecarSha256": sha256(source_sidecar),
            },
            "draft": {
                "strip": rel(strip_path),
                "stripSha256": sha256(strip_path),
                "sidecar": rel(sidecar_path),
                "sidecarSha256": sha256(sidecar_path),
            },
            "frameEvidence": [
                {
                    "frame": index + 1,
                    "canonicalPixelSha256": pixel_sha(original[index]),
                    "draftPixelSha256": pixel_sha(candidate[index]),
                    "changed": index == 4,
                    "opaqueCellEdgePixels": edge_count(candidate[index]),
                }
                for index in range(6)
            ],
            "authoredFrame": 5,
            "changedPixelCount": len(changed),
            "changedPixelBoundsExclusive": bbox,
            "unchangedOutOfScopePixels": outside_changes == 0,
            "endpointFrame": 6,
            "endpointByteIdenticalToCanon": candidate[5].tobytes() == canon.tobytes(),
            "alphaValues": alpha_values,
            "evidence": [rel(original_gif), rel(candidate_gif), rel(comparison_gif), rel(comparison_png)],
        }
        candidate_records.append(record)
        public_assets[name] = {}
        for label, asset in {
            "canonical": original_gif,
            "candidate": candidate_gif,
            "comparison": comparison_gif,
            "strips": comparison_png,
        }.items():
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
        "method": "Replace only the declared F5 head/face zone with the exact approved neutral pixels; leave F1-F4 and F6 byte-identical to canonical production.",
        "mask": {"file": rel(mask_path), "sha256": sha256(mask_path), "boundsExclusive": [18, 0, 112, 108]},
        "candidates": candidate_records,
        "checks": {
            "stripSidecarAgreement": True,
            "binaryAlpha": True,
            "transparentCellEdges": True,
            "unchangedOutOfScopePixels": True,
            "endpointContinuity": "Both F6 endpoints are byte-identical to the approved neutral canon; F5 and F6 share the same canonical head placement and scale.",
            "productionChanged": False,
        },
        "exclusions": {
            "keeper_count_money": "explicitly deleted amendment remains deleted and was not regenerated",
            "withdrawnFaceCameraDrafts": "rejected provenance only; not reused",
            "remainingInventory": "not touched pending review of these first two candidates",
        },
        "rollback": f"Delete only {rel(BATCH)} and {rel(PUBLIC)}; canonical raw/runtime art and manifests are unchanged.",
    }
    write_json(BATCH / "batch-register.json", register)
    (BATCH / "HANDOFF.md").write_text(
        "# Standard turn full-face endpoints — V1\n\n"
        "Status: **awaiting Frank's explicit visual approval; production unchanged**.\n\n"
        "This first two-animation batch covers `keeper_turn_front` and `keeper_turn_left_front` only. "
        "In each strip, F5's oversized smiling head is replaced inside the declared head/face mask with the exact approved neutral pixels. "
        "F1–F4 and F6 are byte-identical to canonical production; F6 was already byte-identical to the approved neutral. "
        "The standard body, hands, legs, timing, turn direction, floor anchor and sidecar contract remain unchanged outside the mask.\n\n"
        "No image-generation call was used: the approved canon is transplanted deterministically. "
        "The rejected face-camera provenance and deleted `keeper_count_money` amendment were not used.\n\n"
        "Rebuild with the bundled Pillow runtime:\n\n"
        "```sh\n"
        "/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_full_face_turn_endpoints.py\n"
        "node scripts/verify_keeper_full_face_turn_endpoints.ts\n"
        "```\n\n"
        f"Rollback: delete `{rel(BATCH)}` and `{rel(PUBLIC)}` only.\n"
    )

    cards = []
    for record in candidate_records:
        name = record["animation"]
        assets = public_assets[name]
        cards.append(f"""
<section><h2>{html.escape(name)}</h2><p>Only F5 head/face pixels inside the declared mask change. F6 remains byte-identical to the approved neutral.</p>
<div class="grid"><article><h3>Canonical production</h3><img src="assets/{assets['canonical']}" alt="Canonical {name} animation"></article><article><h3>V1 candidate</h3><img src="assets/{assets['candidate']}" alt="V1 {name} candidate"></article></div>
<article class="wide"><h3>Synchronized comparison</h3><img src="assets/{assets['comparison']}" alt="Side-by-side animated comparison for {name}"></article>
<details><summary>Full strips and hashes</summary><img src="assets/{assets['strips']}" alt="Canonical and candidate strips for {name}"><p>Canonical <code>{record['canonical']['stripSha256']}</code><br>Draft <code>{record['draft']['stripSha256']}</code></p></details></section>""")
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper standard turn full-face endpoints V1</title>
<style>:root{{color-scheme:dark;--bg:#0d1319;--panel:#17212a;--line:#3a4c5a;--ink:#edf5fb;--muted:#a9bac6;--green:#77d9a4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}}header,main{{max-width:1450px;margin:auto;padding:18px}}header{{border-bottom:1px solid var(--line)}}h1,h2,h3{{font-family:system-ui,sans-serif}}.status{{display:inline-block;padding:5px 9px;border:1px solid var(--green);border-radius:999px;color:var(--green)}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}article,details{{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:12px;margin:12px 0}}img{{display:block;max-width:100%;height:auto;margin:auto;image-rendering:auto}}article img{{max-height:620px}}.wide img{{width:min(100%,900px)}}code{{overflow-wrap:anywhere;color:#badaef}}a{{color:#8dcfff}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}</style></head>
<body><header><a href="/keeper-review/">← Animation reviewer</a> · <a href="/keeper-review/full-face-canon-v1/">Approved canon V1</a><h1>First two full-face normalizations</h1><span class="status">Awaiting explicit visual approval · production unchanged</span><p><code>keeper_turn_front</code> and <code>keeper_turn_left_front</code> only. The candidate F5 uses the approved adult neutral head and face; F6 was already an exact canon match.</p></header><main>{''.join(cards)}
<section><h2>Verification boundary</h2><article><p>F1–F4 and F6 are byte-identical to production. Every F5 change is inside the published mask. Both strips have binary alpha, zero opaque cell-edge pixels, unchanged geometry/timing/anchors, and an exact neutral F6 endpoint. Nothing is promoted by this page.</p></article></section></main></body></html>"""
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(page)
    print(json.dumps({"batch": BATCH_ID, "candidates": list(NAMES), "publicPage": rel(PUBLIC / "index.html")}, indent=2))


if __name__ == "__main__":
    main()
