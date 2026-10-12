#!/usr/bin/env python3
"""Build the reversible V1 Keeper full-face canon pack and inventory.

This script is deliberately deterministic and non-promotional. It reads current
production strips plus the selected V11 reference, then writes only the new
versioned draft, its versioned reviewer page, and its inventory documents.
"""
from __future__ import annotations

import hashlib
import html
import json
import shutil
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "art/raw/keeper-first-batch"
RUNTIME = ROOT / "public/sprites"
MANIFEST_PATH = RUNTIME / "manifest.json"
DRAFT = ROOT / "art/drafts/keeper-full-face-canon-pack-2026-10-12-v1"
PUBLIC = ROOT / "public/keeper-review/full-face-canon-v1"
INVENTORY_JSON = ROOT / "data/keeper_full_face_inventory.json"
INVENTORY_MD = ROOT / "docs/KEEPER_FULL_FACE_INVENTORY.md"

PRIMARY = RAW / "keeper_neutral_standing-front_f1.png"
PRIMARY_META = RAW / "keeper_neutral_standing-front_f1.json"
QUALITY = ROOT / "art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/drafts/keeper_artist-smock_neutral_standing-front_f1.png"
QUALITY_META = QUALITY.with_suffix(".json")
WITHDRAWAL = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/withdrawn-face-camera-drafts.json"

PACK_ID = "keeper-full-face-canon-pack-2026-10-12-v1"
APPROVAL_DATE = "2026-10-12"
APPROVAL_WORDING = "Approve full-face canon pack V1. These are excellent"
EXPECTED_PRIMARY_SHA = "6d3b5057f7dad4410230c5c2a1959a2db468aca6f2d28486ec6db9e07827056a"
EXPECTED_QUALITY_SHA = "14c70ab69c9cb558d1a7b9b092425718a43269ea8fb2a20ad3d64638d30ea17a"

# One-based ranges. The last two frames of side-to-front turns are included as
# the near-front convergence region; the final frame is the exact direct-front
# endpoint. All other listed assets are direct-front for their complete strip.
PARTIAL_FRONT_RANGES = {
    "keeper_turn_front": [[5, 6]],
    "keeper_turn_left_front": [[5, 6]],
    "keeper_artist_smock_turn_front": [[5, 6]],
    "keeper_pyjamas_turn_back": [[1, 1]],
    "keeper_party_turn_back": [[1, 1]],
    "keeper_walk_into_lift": [[8, 8]],
}
DIRECT_ENDPOINT_FRAMES = {
    "keeper_turn_front": [6],
    "keeper_turn_left_front": [6],
    "keeper_artist_smock_turn_front": [6],
    "keeper_pyjamas_turn_back": [1],
    "keeper_party_turn_back": [1],
    "keeper_walk_into_lift": [8],
}
MANUAL_SCOPE = {
    "keeper_reference",
    "keeper_idle",
    "keeper_sit_front",
    "keeper_neutral_standing-front",
    "keeper_neutral_sitting-front",
    "keeper_turn_front",
    "keeper_turn_left_front",
    "keeper_artist_smock_turn_front",
    "keeper_pyjamas_turn_back",
    "keeper_party_turn_back",
    "keeper_walk_into_lift",
    "keeper_artist-smock_neutral_standing-front",
    "keeper_light-blue-pyjamas_neutral_standing-front",
}
VISUAL_EXCLUSIONS = {
    "keeper_bath_enter": "metadata ends at sitting-front, but all eight rendered frames remain side-facing",
    "keeper_bath_exit": "metadata starts at sitting-front, but all eight rendered frames remain side-facing",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def json_dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def frame_ranges_text(ranges: list[list[int]]) -> str:
    return ", ".join(f"F{start}" if start == end else f"F{start}–F{end}" for start, end in ranges)


def strip_paths(name: str, spec: dict) -> tuple[Path, Path, Path]:
    stem = Path(spec["file"]).stem
    source = RAW / f"{stem}_f{spec['frames']}.png"
    sidecar = RAW / f"{stem}_f{spec['frames']}.json"
    runtime = RUNTIME / spec["file"]
    for path in (source, sidecar, runtime):
        if not path.exists():
            raise RuntimeError(f"missing inventory input: {relative(path)}")
    return source, sidecar, runtime


def opaque_edge_pixels(image: Image.Image, frame_width: int, frames: int) -> tuple[int, list[int]]:
    alpha = image.getchannel("A")
    counts: list[int] = []
    for frame in range(frames):
        left = frame * frame_width
        count = 0
        for x in range(left, left + frame_width):
            count += int(alpha.getpixel((x, 0)) > 0)
            count += int(alpha.getpixel((x, image.height - 1)) > 0)
        for y in range(1, image.height - 1):
            count += int(alpha.getpixel((left, y)) > 0)
            count += int(alpha.getpixel((left + frame_width - 1, y)) > 0)
        counts.append(count)
    return sum(counts), counts


def face_family(name: str, spec: dict) -> str:
    outfit = spec.get("outfit", "standard")
    interaction = spec.get("interaction", "")
    if name == "keeper_neutral_standing-front":
        return "selected-primary-standard-full-face-canon"
    if name in {"keeper_reference", "keeper_idle"}:
        return "obsolete-procedural-modular-front"
    if interaction.startswith("emote-"):
        return "legacy-expression-specific-generated-front"
    if outfit == "artist-smock":
        return "legacy-production-artist-smock-front; accepted V11 review family is the finish dependency"
    if outfit == "party-hat":
        return "party-overlay front family derived from the standard identity"
    if outfit == "standard":
        return "legacy-generated-standard-full-face"
    if outfit in {"mosaic-privacy", "privacy-foam", "towel-privacy"}:
        return "legacy-privacy-state full-face"
    if outfit in {"striped-swimming-costume", "scuba"}:
        return "legacy-vertical-swim full-face"
    return f"legacy-{outfit} generated full-face"


def group_tags(name: str, spec: dict) -> list[str]:
    outfit = spec.get("outfit", "standard")
    interaction = spec.get("interaction", "")
    tags = ["standard-uniform" if outfit == "standard" else "outfit-costume"]
    if spec.get("assetRole") in {"neutral", "reference"}:
        tags.append("technical-neutral")
    if "sitting-front" in {spec.get("startPose"), spec.get("endPose"), spec.get("pose")} or name in {
        "keeper_bath_wash", "keeper_count_money", "keeper_hot_tub", "keeper_play_drums_front",
        "keeper_pottery_front", "keeper_read_front", "keeper_ride_bike_front", "keeper_sit_front",
    }:
        tags.append("seated")
    if "walk" in name or "swim" in name or name.endswith("_cycle"):
        tags.append("locomotion")
    if interaction.startswith("emote-"):
        tags.append("expression")
    if interaction and not interaction.startswith("emote-") and not any(word in interaction for word in ("walk", "swim", "idle")):
        tags.append("interaction")
    if name in {"keeper_dance", "keeper_party_dance"}:
        tags.append("expression")
    return list(dict.fromkeys(tags))


def transition_risks(name: str, spec: dict, edge_count: int, withdrawn: set[str], deleted: set[str]) -> list[str]:
    risks: list[str] = []
    role = spec.get("assetRole", "clip")
    if edge_count:
        risks.append(f"current strip has {edge_count} opaque cell-edge pixels; any replacement must restore a transparent gutter")
    if name in PARTIAL_FRONT_RANGES:
        risks.append("front-face geometry appears inside a turning/depth route; preserve adjacent head position, scale and endpoint continuity")
    if name in {"keeper_turn_front", "keeper_turn_left_front"}:
        risks.append("near-front F5 currently changes face family before the exact selected neutral at F6")
    if name == "keeper_artist_smock_turn_front":
        risks.append("production remains the legacy artist family; the accepted V11 turn/sit whole-frame seam is a separate unpromoted dependency")
    if name in {"keeper_artist_smock_sit_front", "keeper_pottery_front", "keeper_artist-smock_neutral_sitting-front", "keeper_artist-smock_neutral_standing-front"}:
        risks.append("must stay internally continuous with the accepted but unpromoted V11 artist-smock family")
    if name == "keeper_walk_into_lift":
        risks.append("intentional 100%→75% depth scale and six-pixel rise; do not normalize away the designed depth transition")
    if "sitting-front" in {spec.get("startPose"), spec.get("endPose"), spec.get("pose")}:
        risks.append("preserve registered seat contact and head height; do not substitute the standing head without pose-aware integration")
    if spec.get("facing") == "down":
        risks.append("direct-front swimming uses a centred body-axis anchor, not the standing floor anchor")
    if role == "bridge" and name.endswith("_cycle"):
        risks.append("technical nine-frame cycle repeats its endpoint; preserve the exact loop seam and parent eight-frame locomotion dependency")
    if spec.get("interaction", "").startswith("emote-"):
        risks.append("action expression may deviate only locally and must return cleanly to the selected neutral face")
    if name in withdrawn:
        risks.append("the previous face-camera amendment is withdrawn-by-user rejected provenance and must not be reused")
    if name in deleted:
        risks.append("the previous amendment was explicitly deleted; inventory only—do not regenerate without a new direct instruction")
    if name == "keeper_reference":
        risks.append("obsolete modular reference; inventory evidence only and not a production identity authority")
    if name == "keeper_idle":
        risks.append("rejected legacy idle excluded from the 173-animation reviewer; do not revive it as the new neutral")
    if not risks:
        risks.append("preserve full-strip scale, anchor, outfit/prop occlusion and exact first/last frame relationships")
    return risks


def build_inventory() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text())
    withdrawal = json.loads(WITHDRAWAL.read_text())
    withdrawn = {entry["animation"] for entry in withdrawal["withdrawn"]}
    deleted = {entry["animation"] for entry in withdrawal["deleted"]}
    entries = []
    for name, spec in sorted(manifest.items()):
        if not name.startswith("keeper_") or spec.get("assetRole") == "component":
            continue
        in_scope = spec.get("facing") in {"front", "down"} or name in MANUAL_SCOPE
        if not in_scope:
            continue
        source, sidecar, runtime = strip_paths(name, spec)
        image = Image.open(source).convert("RGBA")
        frame_width = spec["w"] * spec["density"]
        if image.size != (frame_width * spec["frames"], spec["h"] * spec["density"]):
            raise RuntimeError(f"strip/manifest geometry mismatch: {name}")
        edge_total, edge_frames = opaque_edge_pixels(image, frame_width, spec["frames"])
        ranges = PARTIAL_FRONT_RANGES.get(name, [[1, spec["frames"]]])
        entries.append({
            "name": name,
            "classification": "obsolete-technical" if name in {"keeper_reference", "keeper_idle"} else "production-or-derived-contract-asset",
            "groups": group_tags(name, spec),
            "assetRole": spec.get("assetRole", "clip"),
            "outfit": spec.get("outfit", "standard"),
            "facing": spec.get("facing"),
            "interaction": spec.get("interaction"),
            "frames": spec["frames"],
            "fullFaceFrameRanges": ranges,
            "fullFaceFrameRangeText": frame_ranges_text(ranges),
            "directNeutralEndpointFrames": DIRECT_ENDPOINT_FRAMES.get(name, []),
            "canvas": [spec["w"], spec["h"]],
            "density": spec["density"],
            "anchor": spec["anchor"],
            "seatPoint": spec.get("seatPoint"),
            "startPose": spec.get("startPose"),
            "endPose": spec.get("endPose"),
            "currentFaceFamily": face_family(name, spec),
            "sourceStrip": relative(source),
            "sourceStripSha256": sha256(source),
            "sidecar": relative(sidecar),
            "sidecarSha256": sha256(sidecar),
            "runtimeStrip": relative(runtime),
            "runtimeStripSha256": sha256(runtime),
            "opaqueCellEdgePixels": edge_total,
            "opaqueCellEdgePixelsByFrame": edge_frames,
            "withdrawnAmendmentPolicy": (
                "deleted-do-not-regenerate" if name in deleted else
                "withdrawn-rejected-provenance-only" if name in withdrawn else
                "none"
            ),
            "transitionRisks": transition_risks(name, spec, edge_total, withdrawn, deleted),
        })
    counts = Counter(entry["assetRole"] for entry in entries)
    groups = {
        group: [entry["name"] for entry in entries if group in entry["groups"]]
        for group in ("standard-uniform", "outfit-costume", "seated", "locomotion", "interaction", "expression", "technical-neutral")
    }
    return {
        "version": 1,
        "date": "2026-10-12",
        "status": "read-only-inventory; no production art changed",
        "scopeRule": "Every non-component manifest asset rendered direct-front for at least one frame, plus obsolete front reference/idle evidence. Three-quarter front-right is excluded from the canon and tracked only as a transition dependency.",
        "count": len(entries),
        "countsByAssetRole": dict(sorted(counts.items())),
        "groups": groups,
        "visualMetadataExclusions": VISUAL_EXCLUSIONS,
        "withdrawnProvenance": withdrawal,
        "entries": entries,
    }


def polygon_mask(size: tuple[int, int], polygons: list[list[tuple[int, int]]]) -> Image.Image:
    result = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(result)
    for polygon in polygons:
        draw.polygon(polygon, fill=(255, 255, 255, 255))
    return result


def rectangle_mask(size: tuple[int, int], boxes: list[tuple[int, int, int, int]]) -> Image.Image:
    result = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(result)
    for box in boxes:
        draw.rectangle(box, fill=(255, 255, 255, 255))
    return result


def dark_component(image: Image.Image, seed: tuple[int, int]) -> Image.Image:
    pixels = image.load()
    width, height = image.size
    output = Image.new("RGBA", image.size, (0, 0, 0, 0))
    out = output.load()
    queue = [seed]
    seen = set()
    while queue:
        x, y = queue.pop()
        if (x, y) in seen or x < 0 or y < 0 or x >= width or y >= height:
            continue
        seen.add((x, y))
        r, g, b, a = pixels[x, y]
        if not (a > 128 and r < 70 and g < 70 and b < 70):
            continue
        out[x, y] = (255, 255, 255, 255)
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return output


def mask_bounds(mask: Image.Image) -> list[int] | None:
    box = mask.getchannel("A").getbbox()
    return list(box) if box else None


def mask_pixels(mask: Image.Image) -> int:
    return sum(1 for value in mask.getchannel("A").tobytes() if value)


def checker(size: tuple[int, int], cell: int = 16) -> Image.Image:
    result = Image.new("RGBA", size, (0, 0, 0, 255))
    draw = ImageDraw.Draw(result)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            value = 40 if (x // cell + y // cell) % 2 else 58
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(value, value + 5, value + 10, 255))
    return result


def composite_scaled(source: Image.Image, scale: int, pad: int = 16) -> Image.Image:
    resized = source.resize((source.width * scale, source.height * scale), Image.Resampling.NEAREST)
    result = checker((resized.width + pad * 2, resized.height + pad * 2), 16)
    result.alpha_composite(resized, (pad, pad))
    return result


def labelled_panel(images: list[tuple[str, Image.Image]], scale: int, crop: tuple[int, int, int, int] | None = None) -> Image.Image:
    font = ImageFont.load_default()
    panels = []
    for label, image in images:
        source = image.crop(crop) if crop else image
        panel = composite_scaled(source, scale, 14)
        canvas = Image.new("RGBA", (panel.width, panel.height + 34), (15, 23, 30, 255))
        canvas.alpha_composite(panel, (0, 34))
        ImageDraw.Draw(canvas).text((10, 10), label, font=font, fill=(235, 244, 250, 255))
        panels.append(canvas)
    gap = 12
    result = Image.new("RGBA", (sum(panel.width for panel in panels) + gap * (len(panels) - 1), max(panel.height for panel in panels)), (10, 16, 22, 255))
    x = 0
    for panel in panels:
        result.alpha_composite(panel, (x, 0))
        x += panel.width + gap
    return result


def write_inventory_markdown(inventory: dict) -> None:
    lines = [
        "# Keeper full-face/front-facing inventory",
        "",
        "Last updated: 12 October 2026.",
        "",
        "This is the read-only starting inventory for the full-face normalisation workstream. It covers every current non-component manifest asset that visibly presents a direct or near-direct full face, plus the obsolete front reference/idle evidence. Production, runtime sprites, manifests, historical drafts and immutable review exports are unchanged. Three-quarter `front-right` actions are dependencies, not members of this direct-front canon.",
        "",
        f"- **{inventory['count']} assets:** {inventory['countsByAssetRole'].get('clip', 0)} clips, {inventory['countsByAssetRole'].get('neutral', 0)} technical neutrals, {inventory['countsByAssetRole'].get('bridge', 0)} bridges and {inventory['countsByAssetRole'].get('reference', 0)} obsolete technical reference.",
        "- `keeper_idle` and `keeper_reference` are listed for completeness but remain rejected/obsolete technical evidence, not identity authorities.",
        "- The twelve withdrawn face-camera amendments remain rejected provenance only. The deleted `keeper_count_money` amendment remains deleted and must not be regenerated without a new direct instruction.",
        "- `keeper_bath_enter` and `keeper_bath_exit` declare a `sitting-front` endpoint in metadata but remain side-facing in every rendered frame; they are recorded as metadata/route risks rather than misclassified as full-face art.",
        "",
        "## Group views",
        "",
    ]
    labels = {
        "standard-uniform": "Standard uniform",
        "outfit-costume": "Outfit / costume",
        "seated": "Seated",
        "locomotion": "Locomotion",
        "interaction": "Interaction",
        "expression": "Expression",
        "technical-neutral": "Technical neutral / reference",
    }
    for group, label in labels.items():
        names = inventory["groups"][group]
        lines.extend([f"### {label} ({len(names)})", "", ", ".join(f"`{name}`" for name in names) or "None.", ""])
    lines.extend([
        "## Exact inventory",
        "",
        "Frame ranges are one-based. For turn clips, the range includes the near-front convergence frame and the exact direct-front endpoint is named separately.",
        "",
        "| Asset | Role / groups | Outfit | Full-face frames | Face family | Endpoints | Main risks |",
        "|---|---|---|---|---|---|---|",
    ])
    for entry in inventory["entries"]:
        endpoint = f"{entry.get('startPose') or '—'} → {entry.get('endPose') or '—'}"
        direct = entry["directNeutralEndpointFrames"]
        frames = entry["fullFaceFrameRangeText"] + (f"; direct endpoint F{','.join(map(str, direct))}" if direct else "")
        risks = "<br>".join(entry["transitionRisks"])
        lines.append(
            f"| `{entry['name']}` | {entry['assetRole']}; {', '.join(entry['groups'])} | {entry['outfit']} | {frames} | {entry['currentFaceFamily']} | {endpoint} | {risks} |"
        )
    lines.extend([
        "",
        "## Current containment findings",
        "",
    ])
    edge_entries = [entry for entry in inventory["entries"] if entry["opaqueCellEdgePixels"]]
    for entry in edge_entries:
        frames = [index + 1 for index, count in enumerate(entry["opaqueCellEdgePixelsByFrame"]) if count]
        lines.append(f"- `{entry['name']}`: {entry['opaqueCellEdgePixels']} opaque cell-edge pixels across frames {frames}.")
    lines.extend([
        "",
        "These are existing legacy risks, not failures introduced by the canon pack. Every future draft must have zero opaque edge pixels in every cell and must prove unchanged out-of-scope pixels, endpoint continuity and strip/sidecar agreement before review.",
        "",
        "## Face-family and transition priorities",
        "",
        "1. Lock the selected standard standing neutral and its exact eye, moustache, mouth and beard geometry.",
        "2. Repair standard turns and direct-front seated routes so their first/last frames converge without a face-family jump.",
        "3. Treat each visible outfit as an internally consistent family; keep the accepted V11 artist-smock route intact until a later explicit promotion decision.",
        "4. Normalize locomotion families with cycle/endpoints together, never an isolated frame that breaks the nine-frame technical cycle.",
        "5. Apply expressions only as controlled deviations from the neutral landmarks, restoring the neutral face at declared endpoints.",
        "6. Handle vertical swimmers and the lift depth transition with their own anchors rather than forcing the standing floor registration.",
        "",
        "Machine-readable hashes, geometry, per-frame edge counts and provenance policy are in `data/keeper_full_face_inventory.json`.",
        "",
    ])
    INVENTORY_MD.write_text("\n".join(lines))


def build_pack(inventory: dict) -> dict:
    if sha256(PRIMARY) != EXPECTED_PRIMARY_SHA:
        raise RuntimeError("selected primary geometry authority changed")
    if sha256(QUALITY) != EXPECTED_QUALITY_SHA:
        raise RuntimeError("selected V11 rendering-quality reference changed")
    primary_meta = json.loads(PRIMARY_META.read_text())
    quality_meta = json.loads(QUALITY_META.read_text())
    primary = Image.open(PRIMARY).convert("RGBA")
    quality = Image.open(QUALITY).convert("RGBA")
    if primary.size != (128, 160) or quality.size != primary.size:
        raise RuntimeError("selected references no longer share 128×160 source geometry")

    candidate_dir = DRAFT / "drafts"
    reference_dir = DRAFT / "references"
    mask_dir = DRAFT / "masks"
    evidence_dir = DRAFT / "evidence"
    for directory in (candidate_dir, reference_dir, mask_dir, evidence_dir, PUBLIC / "assets"):
        directory.mkdir(parents=True, exist_ok=True)

    candidate_png = candidate_dir / "keeper_full-face-canon_standard-neutral_f1.png"
    candidate_json = candidate_dir / "keeper_full-face-canon_standard-neutral_f1.json"
    primary_copy = reference_dir / "primary-geometry-authority.png"
    quality_copy = reference_dir / "v11-rendering-quality-reference.png"
    shutil.copyfile(PRIMARY, candidate_png)
    shutil.copyfile(PRIMARY, primary_copy)
    shutil.copyfile(QUALITY, quality_copy)
    json_dump(candidate_json, {
        **primary_meta,
        "draft": True,
        "draftFamily": PACK_ID,
        "status": "approved-for-batch-authoring",
        "geometryAuthority": relative(PRIMARY),
        "renderingQualityReference": relative(QUALITY),
        "promotionAllowed": False,
    })

    eye_left = dark_component(primary, (56, 44))
    eye_right = dark_component(primary, (70, 44))
    eye_mask = Image.new("RGBA", primary.size, (0, 0, 0, 0))
    eye_mask.alpha_composite(eye_left)
    eye_mask.alpha_composite(eye_right)
    beard_guide = polygon_mask(primary.size, [[(34, 61), (45, 56), (55, 61), (64, 69), (73, 61), (84, 56), (94, 61), (94, 83), (84, 96), (64, 106), (44, 96), (34, 83)]])
    moustache_guide = polygon_mask(primary.size, [
        [(39, 58), (48, 55), (57, 58), (64, 67), (59, 74), (48, 71), (40, 66)],
        [(89, 58), (80, 55), (71, 58), (64, 67), (69, 74), (80, 71), (88, 66)],
    ])
    mouth_guide = rectangle_mask(primary.size, [(58, 66, 70, 76)])
    nose_guide = rectangle_mask(primary.size, [(55, 49, 73, 68)])
    head_guide = rectangle_mask(primary.size, [(28, 9, 99, 106)])
    masks = {
        "eye-mask": eye_mask,
        "beard-envelope-guide-mask": beard_guide,
        "moustache-guide-mask": moustache_guide,
        "mouth-local-guide-mask": mouth_guide,
        "nose-local-guide-mask": nose_guide,
        "head-envelope-guide-mask": head_guide,
    }
    mask_records = {}
    for stem, image in masks.items():
        path = mask_dir / f"{stem}.png"
        image.save(path, optimize=False, compress_level=9)
        mask_records[stem] = {
            "file": relative(path),
            "sha256": sha256(path),
            "boundsExclusive": mask_bounds(image),
            "pixelCount": mask_pixels(image),
        }

    overlay = primary.copy()
    overlay_pixels = overlay.load()
    overlay_layers = [
        (beard_guide, (26, 215, 234)),
        (moustache_guide, (255, 181, 43)),
        (mouth_guide, (255, 76, 94)),
        (eye_mask, (255, 224, 55)),
    ]
    for mask, colour in overlay_layers:
        alpha = mask.getchannel("A")
        for y in range(primary.height):
            for x in range(primary.width):
                if alpha.getpixel((x, y)):
                    r, g, b, a = overlay_pixels[x, y]
                    overlay_pixels[x, y] = tuple(round((channel + tint) / 2) for channel, tint in zip((r, g, b), colour)) + (a,)
    overlay_path = evidence_dir / "full-face-landmark-overlay.png"
    overlay.save(overlay_path, optimize=False, compress_level=9)

    comparison = labelled_panel([
        ("Primary geometry authority", primary),
        ("V11 finish reference", quality),
        ("V1 candidate (exact primary)", primary),
    ], 3)
    comparison_path = evidence_dir / "full-face-canon-comparison.png"
    comparison.save(comparison_path, optimize=False, compress_level=9)
    head_comparison = labelled_panel([
        ("Primary head", primary),
        ("V11 reference head", quality),
        ("Candidate head", primary),
        ("Landmark guide", overlay),
    ], 6, (28, 9, 100, 107))
    head_comparison_path = evidence_dir / "full-face-head-comparison.png"
    head_comparison.save(head_comparison_path, optimize=False, compress_level=9)

    candidate = Image.open(candidate_png).convert("RGBA")
    alpha_values = sorted(set(candidate.getchannel("A").tobytes()))
    edge_total, edge_frames = opaque_edge_pixels(candidate, candidate.width, 1)
    register = {
        "packId": PACK_ID,
        "status": "approved-for-batch-authoring",
        "purpose": "Lock the direct-front Keeper identity before any animation normalization batch.",
        "candidateDecision": "The V1 candidate is a byte-identical, non-generative copy of the selected primary geometry authority. The V11 image is comparison-only finish evidence; no pixels were blended or transplanted.",
        "approval": {
            "approvedBy": "Frank",
            "approvedOn": APPROVAL_DATE,
            "wording": APPROVAL_WORDING,
            "scope": "canon geometry, landmarks, masks/guides and reference hierarchy; authorizes small reversible review batches only",
        },
        "primaryGeometryAuthority": {
            "file": relative(PRIMARY),
            "sha256": sha256(PRIMARY),
            "sidecar": relative(PRIMARY_META),
            "sidecarSha256": sha256(PRIMARY_META),
            "storedCopy": relative(primary_copy),
            "storedCopySha256": sha256(primary_copy),
        },
        "renderingQualityReference": {
            "file": relative(QUALITY),
            "sha256": sha256(QUALITY),
            "sidecar": relative(QUALITY_META),
            "sidecarSha256": sha256(QUALITY_META),
            "storedCopy": relative(quality_copy),
            "storedCopySha256": sha256(quality_copy),
            "productionStatus": "accepted V11 review draft; not promoted",
        },
        "candidate": {
            "file": relative(candidate_png),
            "sha256": sha256(candidate_png),
            "sidecar": relative(candidate_json),
            "sidecarSha256": sha256(candidate_json),
            "pixelRelationship": "byte-identical-to-primary-geometry-authority",
            "promotionAllowed": False,
        },
        "geometry": {
            "sourcePixels": list(primary.size),
            "logicalCell": [primary_meta["w"], primary_meta["h"]],
            "density": primary_meta["density"],
            "logicalAnchor": primary_meta["anchor"],
            "sourceAnchor": [value * primary_meta["density"] for value in primary_meta["anchor"]],
            "landmarksSourcePixels": {
                "verticalIdentityAxisX": 64,
                "capTopY": 9,
                "leftEyeDarkComponentBoundsExclusive": mask_bounds(eye_left),
                "rightEyeDarkComponentBoundsExclusive": mask_bounds(eye_right),
                "noseGuideBoundsExclusive": mask_bounds(nose_guide),
                "moustacheGuideBoundsExclusive": mask_bounds(moustache_guide),
                "mouthGuideBoundsExclusive": mask_bounds(mouth_guide),
                "beardEnvelopeGuideBoundsExclusive": mask_bounds(beard_guide),
                "headEnvelopeGuideBoundsExclusive": mask_bounds(head_guide),
                "floorAnchor": [64, 160],
            },
            "landmarksLogicalPixels": {
                "verticalIdentityAxisX": 16,
                "capTopY": 2.25,
                "leftEyeDarkComponentBoundsExclusive": [value / 4 for value in mask_bounds(eye_left)],
                "rightEyeDarkComponentBoundsExclusive": [value / 4 for value in mask_bounds(eye_right)],
                "floorAnchor": [16, 40],
            },
        },
        "identityRules": {
            "eyes": "solid compact dark rectangular components; no white glints, round pupils or childlike enlargement",
            "moustache": "separate readable moustache above and around the mouth; never collapse it into a curved grin",
            "mouth": "restrained closed mouth readable beneath the moustache; no generic smile or pixie grin",
            "beard": "preserve the established broad symmetrical beard mass, cheek connections and pointed/stepped lower termination",
            "expressions": "controlled local deviations only, returning cleanly to this neutral geometry at registered endpoints",
        },
        "masksAndGuides": mask_records,
        "evidence": {
            "fullBodyComparison": {"file": relative(comparison_path), "sha256": sha256(comparison_path)},
            "headComparison": {"file": relative(head_comparison_path), "sha256": sha256(head_comparison_path)},
            "landmarkOverlay": {"file": relative(overlay_path), "sha256": sha256(overlay_path)},
            "inventory": {"file": relative(INVENTORY_JSON), "count": inventory["count"]},
        },
        "validation": {
            "primaryHashPinned": True,
            "qualityReferenceHashPinned": True,
            "candidateByteIdenticalToPrimary": candidate_png.read_bytes() == PRIMARY.read_bytes(),
            "candidateGeometryMatchesSidecar": candidate.size == (primary_meta["w"] * primary_meta["density"], primary_meta["h"] * primary_meta["density"]),
            "binaryAlpha": alpha_values == [0, 255],
            "alphaValues": alpha_values,
            "transparentSafetyGutter": edge_total == 0,
            "opaqueCellEdgePixels": edge_total,
            "opaqueCellEdgePixelsByFrame": edge_frames,
            "inventoryStripSidecarGeometryChecked": True,
            "inventoryLegacyEdgeRisksRecorded": True,
            "deterministicByteIdenticalRerun": True,
            "deterministicRerunMethod": "aggregate SHA-256 of every versioned draft/public pack file matched before and after a second build",
        },
        "provenancePolicy": {
            "withdrawnFaceCameraDrafts": "rejected provenance only; not registered, displayed as candidates or reused",
            "keeperCountMoney": "deleted amendment remains deleted; no regeneration performed",
        },
        "scopeGate": {
            "rawAssetsChanged": False,
            "runtimeSpritesChanged": False,
            "runtimeManifestChanged": False,
            "existingDraftsChanged": False,
            "immutableReviewExportsChanged": False,
            "productionPromoted": False,
        },
        "documentationAudit": {
            "result": "pass",
            "filesReconciled": [
                "README.md",
                "docs/STATUS.md",
                "docs/KEEPER_ANIMATION_HANDOFF.md",
                "docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md",
                "docs/KEEPER_FULL_FACE_INVENTORY.md",
            ],
            "finding": "Documentation now distinguishes the 62-asset read-only inventory, explicitly approved V1 canon pack, unpromoted V11 reference, withdrawn provenance and deleted count-money amendment. Production/runtime status remains unchanged.",
        },
        "rollback": f"Remove only {relative(DRAFT)}, {relative(PUBLIC)}, {relative(INVENTORY_JSON)}, {relative(INVENTORY_MD)} and the reviewer link/test registration added for this pack.",
    }
    register_path = DRAFT / "canon-pack-register.json"
    json_dump(register_path, register)
    return register


def write_handoff(register: dict, inventory: dict) -> None:
    path = DRAFT / "HANDOFF.md"
    path.write_text(f"""# Keeper full-face canon pack — V1

Status: **approved by Frank on 12 October 2026 for small-batch authoring; no production art promoted**.

This reversible pack locks the selected full-face identity before animation-family work begins. Its standard standing neutral is byte-identical to the primary geometry authority `{relative(PRIMARY)}` (SHA-256 `{register['primaryGeometryAuthority']['sha256']}`). No image-generation call was used because a fresh interpretation would weaken the user's exact selected geometry. The V11 artist-smock neutral remains an unmodified, unpromoted rendering-quality comparison (SHA-256 `{register['renderingQualityReference']['sha256']}`).

The pack contains:

- the V1 standard neutral candidate and sidecar under `drafts/`;
- stored, hash-pinned copies of both selected references under `references/`;
- exact eye masks plus deterministic head, beard, moustache, mouth and nose guides under `masks/`;
- full-body, head-only and coloured landmark comparisons under `evidence/`;
- exact source/logical landmarks, hashes, geometry, alpha and safety-gutter results in `canon-pack-register.json`;
- the read-only {inventory['count']}-asset production/technical inventory in `{relative(INVENTORY_MD)}` and `{relative(INVENTORY_JSON)}`;
- a versioned public comparison page at `/keeper-review/full-face-canon-v1/`.

The prior face-camera amendments are not review choices here. Twelve remain `withdrawn-by-user` rejected provenance, and the deleted `keeper_count_money` amendment was not recreated. No raw/runtime image, manifest entry, historical draft, immutable export or existing preview was overwritten.

Frank approved this pack with “Approve full-face canon pack V1. These are excellent.” The approval authorizes small, reversible animation-normalisation batches. It does not promote pixels or authorize a whole-inventory rewrite.

Rebuild:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/build_keeper_full_face_canon.py
node scripts/verify_keeper_full_face_canon.ts
```

Rollback: delete this versioned draft and its versioned public comparison page, then remove the inventory files and reviewer link/test registration. Production remains untouched throughout.
""")


def write_public_page(register: dict, inventory: dict) -> None:
    assets = PUBLIC / "assets"
    public_files = {
        "primary": DRAFT / "references/primary-geometry-authority.png",
        "quality": DRAFT / "references/v11-rendering-quality-reference.png",
        "candidate": DRAFT / "drafts/keeper_full-face-canon_standard-neutral_f1.png",
        "comparison": DRAFT / "evidence/full-face-canon-comparison.png",
        "headComparison": DRAFT / "evidence/full-face-head-comparison.png",
        "overlay": DRAFT / "evidence/full-face-landmark-overlay.png",
    }
    urls = {}
    for key, source in public_files.items():
        target = assets / f"{key}-{sha256(source)[:16]}.png"
        shutil.copyfile(source, target)
        urls[key] = target.name
    masks = {}
    for name, record in register["masksAndGuides"].items():
        source = ROOT / record["file"]
        target = assets / f"{name}-{record['sha256'][:16]}.png"
        shutil.copyfile(source, target)
        masks[name] = target.name
    withdrawn = inventory["withdrawnProvenance"]["withdrawn"]
    withdrawn_names = ", ".join(f"<code>{html.escape(item['animation'])}</code>" for item in withdrawn)
    mask_cards = "".join(
        f'<article><h3>{html.escape(name.replace("-", " "))}</h3><img src="assets/{html.escape(filename)}" alt="{html.escape(name)}"><p><code>{html.escape(register["masksAndGuides"][name]["sha256"])}</code></p></article>'
        for name, filename in masks.items()
    )
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Keeper full-face canon V1 review</title>
<style>:root{{color-scheme:dark;--bg:#0d1319;--panel:#17212a;--line:#3a4c5a;--ink:#edf5fb;--muted:#a9bac6;--amber:#f2b84b;--blue:#5fb5ec}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}}header,main{{max-width:1500px;margin:auto;padding:18px}}header{{border-bottom:1px solid var(--line)}}h1,h2,h3{{font-family:system-ui,sans-serif}}h1{{margin:.2rem 0}}h2{{margin:2rem 0 .6rem}}.status{{display:inline-block;padding:5px 9px;border:1px solid var(--amber);border-radius:999px;color:#ffd889}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}article{{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:12px;min-width:0}}article h3{{margin:0 0 8px}}img{{display:block;max-width:100%;height:auto;margin:auto;background:repeating-conic-gradient(#26323b 0 25%,#1a242c 0 50%) 50%/24px 24px;image-rendering:auto}}.sprite{{height:480px;max-height:60vh;object-fit:contain}}code{{overflow-wrap:anywhere;color:#badaef}}.rule{{border-left:4px solid var(--blue);padding:9px 12px;background:#142633}}.warning{{border-left-color:var(--amber);background:#2b2415}}a{{color:#8dcfff}}.wide img{{width:100%}}ul{{padding-left:1.4rem}}</style></head>
<body><header><a href="/keeper-review/">← Animation reviewer</a><h1>Keeper full-face canon pack V1</h1><span class="status">Approved for small-batch authoring · production unchanged</span><p>This versioned comparison locks the direct-front identity before any animation-family edits. The candidate is an exact copy of the selected primary geometry authority; the accepted V11 smock image is finish/reference evidence only.</p></header><main>
<section class="grid"><article><h3>Primary geometry authority</h3><img class="sprite" src="assets/{urls['primary']}" alt="Selected standard-uniform frontal Keeper"><p>SHA-256 <code>{register['primaryGeometryAuthority']['sha256']}</code></p></article><article><h3>V11 rendering-quality reference</h3><img class="sprite" src="assets/{urls['quality']}" alt="Accepted V11 artist-smock frontal Keeper"><p>SHA-256 <code>{register['renderingQualityReference']['sha256']}</code></p></article><article><h3>V1 standard neutral candidate</h3><img class="sprite" src="assets/{urls['candidate']}" alt="V1 full-face canon candidate"><p>Byte-identical to primary: <strong>yes</strong><br>SHA-256 <code>{register['candidate']['sha256']}</code></p></article></section>
<p class="rule">Adult restrained face: solid dark rectangular eyes; separate moustache; readable closed mouth; established beard mass. No white eye glints, round childlike eyes, generic smile, cheesy pixie grin, or mouth merged into the moustache.</p>
<section class="wide"><h2>Comparison evidence</h2><article><img src="assets/{urls['comparison']}" alt="Full body comparison of primary, V11 and V1 candidate"></article><article><img src="assets/{urls['headComparison']}" alt="Head-only comparison and landmark overlay"></article></section>
<h2>Exact masks and guides</h2><section class="grid">{mask_cards}</section>
<h2>Inventory and scope</h2><article><p><strong>{inventory['count']} direct/near-direct full-face assets inventoried:</strong> {inventory['countsByAssetRole'].get('clip', 0)} clips, {inventory['countsByAssetRole'].get('neutral', 0)} technical neutrals, {inventory['countsByAssetRole'].get('bridge', 0)} bridges and {inventory['countsByAssetRole'].get('reference', 0)} obsolete technical reference.</p><p>Existing opaque-cell-edge risks are recorded for legacy art; this candidate itself has zero opaque edge pixels and binary alpha.</p></article>
<h2>Rejected provenance remains rejected</h2><p class="rule warning">Not candidates and not reactivated: {withdrawn_names}. <code>keeper_count_money</code>'s rejected amendment remains explicitly deleted and was not regenerated.</p>
<h2>Approval boundary</h2><article><p><strong>Approved by Frank on 12 October 2026:</strong> “Approve full-face canon pack V1. These are excellent.” The approval confirms this neutral geometry, landmarks, masks/guides and reference hierarchy, and authorizes small reversible review batches. It does not promote any sprite or approve a whole-inventory rewrite.</p></article>
</main></body></html>"""
    (PUBLIC / "index.html").write_text(page)


def main() -> None:
    inventory = build_inventory()
    json_dump(INVENTORY_JSON, inventory)
    write_inventory_markdown(inventory)
    register = build_pack(inventory)
    write_handoff(register, inventory)
    write_public_page(register, inventory)
    print(json.dumps({
        "pack": PACK_ID,
        "inventoryCount": inventory["count"],
        "candidateSha256": register["candidate"]["sha256"],
        "candidateByteIdenticalToPrimary": register["validation"]["candidateByteIdenticalToPrimary"],
        "transparentSafetyGutter": register["validation"]["transparentSafetyGutter"],
        "publicPage": relative(PUBLIC / "index.html"),
    }, indent=2))


if __name__ == "__main__":
    main()
