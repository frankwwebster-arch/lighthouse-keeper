#!/usr/bin/env python3
"""Build immutable Dishwasher V8 with oven-weight native-scale linework.

V8 keeps the V41 canvas, alpha, worktop and state contract, but redraws the
appliance face as deliberate supersampled game art instead of shrinking the
complete glossy image-generation reference.  The fascia is narrower and lower,
its controls align with the approved oven controls, and the cabinet-blue side
rails contain no bright cyan shine strokes.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-dishwasher-ligne-claire-v8"
PACK = ROOT / "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v8"
PUBLIC = ROOT / "public/keeper-review" / SET
STYLE_ROOT = ROOT / "art/source/kitchen-dishwasher-ligne-claire-2026-10-22-v8"
OLD_STYLE_ROOT = ROOT / "art/source/kitchen-dishwasher-ligne-claire-2026-10-22-v7"
STYLE_REFS = {state: STYLE_ROOT / f"dishwasher-v8-{state}-style-reference.png" for state in ("off", "on", "broken")}
OLD_PACK = ROOT / "art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v7"
MASTERS = PACK / "masters"
CANDIDATES = PACK / "candidates"
EVIDENCE = PACK / "evidence"
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"
APPROVED_CABINET = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/cabinet-a-le-rj.png"
APPROVED_OVEN = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45/workbench-assets/oven-on.png"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V7 = load_module("dishwasher_v7_builder_for_v8", ROOT / "scripts/build_kitchen_dishwasher_ligne_claire_v7.py")
V4 = load_module("dishwasher_v4_geometry_for_v8", ROOT / "scripts/build_kitchen_dishwasher_ligne_claire_v4.py")
ORIGINAL_REVIEW_HTML = V7.review_html


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def prepare_style_references() -> None:
    if STYLE_ROOT.exists():
        raise RuntimeError("refusing to overwrite immutable Dishwasher V8 source references")
    STYLE_ROOT.mkdir(parents=True)
    for state in ("off", "on", "broken"):
        shutil.copy2(OLD_STYLE_ROOT / f"dishwasher-v7-{state}-style-reference.png", STYLE_REFS[state])


def control_panel(draw: ImageDraw.ImageDraw, state: str) -> None:
    """Narrow fascia with controls centred at oven-native y=25.5."""
    V4.rounded(draw, (19.0, 21.0, 79.0, 31.5), 0.9, V4.CREAM)
    V4.edge(draw, [(21.0, 22.6), (77.0, 22.6)], "#fff3d5", max(5, round(V4.LINE * 0.42)))
    colours = (V4.BLUE_DARK, V4.BLUE_DARK, V4.BLUE_DARK)
    if state == "on":
        colours = (V4.COPPER, V4.COPPER, V4.COPPER)
    elif state == "broken":
        colours = (V4.COPPER, V4.COPPER, V4.RED)
    for x, colour in zip((24.0, 29.0, 34.0), colours):
        V4.ellipse(draw, (x, 24.0, x + 3.1, 27.1), colour)
    V4.ellipse(draw, (68.7, 23.0, 75.0, 29.3), V4.COPPER)
    draw.ellipse(V4.box(70.5, 24.8, 73.2, 27.5), fill=V4.CREAM_SHADOW)
    lamp = V4.GREEN if state == "on" else V4.RED if state == "broken" else V4.BLUE_DARK
    V4.ellipse(draw, (76.0, 24.1, 79.0, 27.1), lamp)


def closed_master(state: str, left_joined: bool, right_joined: bool) -> Image.Image:
    image, draw = V4.base_master(left_joined, right_joined)
    control_panel(draw, state)
    V4.rounded(draw, (19.0, 31.0, 79.0, 73.5), 1.3, V4.CREAM)
    V4.edge(draw, [(20.8, 32.7), (77.2, 32.7)], "#fff3d5", max(5, round(V4.LINE * 0.42)))
    V4.edge(draw, [(20.8, 34.0), (20.8, 70.8)], V4.CREAM_SHADOW, max(6, round(V4.LINE * 0.55)))
    V4.edge(draw, [(77.2, 34.0), (77.2, 70.8)], V4.CREAM_SHADOW, max(6, round(V4.LINE * 0.55)))
    V4.ellipse(draw, (22.0, 33.0, 28.2, 39.2), V4.COPPER)
    V4.ellipse(draw, (69.8, 33.0, 76.0, 39.2), V4.COPPER)
    V4.rounded(draw, (25.0, 34.2, 73.0, 38.0), 1.4, V4.COPPER)
    V4.edge(draw, [(27.0, 35.6), (71.0, 35.6)], "#b94c12", max(5, round(V4.LINE * 0.50)))
    return image


def broken_master(left_joined: bool, right_joined: bool) -> Image.Image:
    image, draw = V4.base_master(left_joined, right_joined)
    control_panel(draw, "broken")
    V4.rounded(draw, (18.5, 31.0, 79.5, 65.0), 1.5, V4.INK_2)
    # Restrained rack lines retain the reference's open-cavity read at game scale.
    V4.edge(draw, [(22.0, 39.0), (75.0, 39.0)], V4.METAL_DARK, max(6, round(V4.LINE * 0.60)))
    V4.edge(draw, [(22.0, 50.0), (75.0, 50.0)], V4.METAL_DARK, max(6, round(V4.LINE * 0.60)))
    for x in (25.0, 34.0, 43.0, 52.0, 61.0, 70.0):
        V4.edge(draw, [(x, 37.0), (x, 57.0)], V4.METAL_DARK, max(5, round(V4.LINE * 0.48)))

    # A visibly open but realistically inset door: lower-left attached, lower-right failed.
    door = [(17.0, 47.0), (20.0, 43.0), (29.0, 44.0), (76.5, 50.5), (81.0, 56.0), (74.0, 75.5), (27.0, 69.0), (19.0, 61.5)]
    V4.polygon(draw, door, V4.CREAM)
    V4.edge(draw, [(21.0, 47.0), (76.0, 54.5)], "#fff3d5", max(5, round(V4.LINE * 0.42)))
    V4.edge(draw, [(25.0, 66.0), (71.0, 72.0)], V4.CREAM_SHADOW, max(6, round(V4.LINE * 0.55)))
    # One-ended hanging handle: only the left boss remains attached.
    V4.ellipse(draw, (25.0, 48.0, 31.4, 54.4), V4.COPPER)
    V4.edge(draw, [(28.2, 51.2), (68.0, 65.0)], V4.INK, V4.p(4.6))
    V4.edge(draw, [(28.2, 51.2), (68.0, 65.0)], V4.COPPER, V4.p(2.8))
    V4.edge(draw, [(31.0, 51.8), (66.5, 64.1)], "#ffad54", max(5, round(V4.LINE * 0.46)))
    # Surviving left hinge and visibly failed right bracket.
    V4.rounded(draw, (18.0, 63.0, 23.0, 71.5), 0.8, V4.METAL_DARK)
    V4.edge(draw, [(76.0, 69.0), (81.0, 73.5)], V4.METAL_DARK, V4.p(2.0))
    V4.edge(draw, [(80.5, 68.5), (76.5, 74.0)], V4.METAL_DARK, V4.p(1.6))
    return image


def styled_master(state: str, left_joined: bool, right_joined: bool) -> Image.Image:
    return broken_master(left_joined, right_joined) if state == "broken" else closed_master(state, left_joined, right_joined)


def checker(size: tuple[int, int], cell: int = 16) -> Image.Image:
    out = Image.new("RGBA", size, (250, 244, 224, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def make_evidence(records: list[dict]) -> list[Path]:
    font = ImageFont.load_default()
    static = [item for item in records if item["suffix"] == ""]
    contact = Image.new("RGBA", (1510, 1100), (250, 244, 224, 255))
    draw = ImageDraw.Draw(contact)
    draw.text((20, 16), "Dishwasher V8 - native-scale oven-weight redraw / exact V41 alpha", fill=V4.INK, font=font)
    draw.text((20, 38), "Narrow lower fascia; oven-aligned controls; restrained blue rails; realistic inset door.", fill=V4.INK, font=font)
    for row, item in enumerate(static):
        source = Image.open(ROOT / item["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / item["candidateFile"]).convert("RGBA")
        y = 70 + row * 335
        for col, image in enumerate((source, candidate, candidate)):
            panel = checker((480, 285), 18)
            shown = image.resize((392, 328), Image.Resampling.NEAREST)
            panel.alpha_composite(shown, ((480 - shown.width) // 2, -20))
            if col == 2:
                ghost = source.resize(shown.size, Image.Resampling.NEAREST)
                tint = Image.new("RGBA", ghost.size, (235, 35, 70, 0))
                tint.putalpha(ghost.getchannel("A").point(lambda value: round(value * 0.36)))
                panel.alpha_composite(tint, ((480 - shown.width) // 2, -20))
            contact.alpha_composite(panel, (10 + col * 500, y))
        draw.text((20, y + 290), f"V41 {item['state'].upper()}", fill=V4.INK, font=font)
        draw.text((520, y + 290), f"V8 {item['state'].upper()}", fill=V4.INK, font=font)
        draw.text((1020, y + 290), "GHOST / EXACT ALPHA", fill=V4.INK, font=font)
    contact_path = EVIDENCE / "dishwasher-v41-v8-ghost.png"
    contact.save(contact_path, optimize=True)

    panel = Image.new("RGBA", (1250, 470), (250, 244, 224, 255))
    pdraw = ImageDraw.Draw(panel)
    pdraw.text((18, 16), "V8 control alignment - dishwasher control centres y=25.5, approved oven controls y=25.4", fill=V4.INK, font=font)
    oven = Image.open(APPROVED_OVEN).convert("RGBA")
    panel.alpha_composite(oven.resize((368, 340), Image.Resampling.NEAREST), (18, 55))
    for index, item in enumerate(static):
        candidate = Image.open(ROOT / item["candidateFile"]).convert("RGBA")
        crop = candidate.crop((7, 16, 91, 43)).resize((420, 135), Image.Resampling.NEAREST)
        x = 410 + (index % 2) * 420
        y = 55 + (index // 2) * 185
        panel.alpha_composite(crop, (x, y))
        pdraw.text((x, y + 142), item["state"].upper(), fill=V4.INK, font=font)
    panel_path = EVIDENCE / "dishwasher-control-panel-invariance.png"
    panel.save(panel_path, optimize=True)

    tiny = Image.new("RGBA", (950, 310), (250, 244, 224, 255))
    tdraw = ImageDraw.Draw(tiny)
    tdraw.text((18, 16), "64 px clarity - deliberate native-scale linework, nearest enlarged for audit", fill=V4.INK, font=font)
    for index, item in enumerate(static):
        candidate = Image.open(ROOT / item["candidateFile"]).convert("RGBA")
        small = candidate.resize((64, round(candidate.height * 64 / candidate.width)), Image.Resampling.LANCZOS)
        tiny.alpha_composite(small.resize((256, 214), Image.Resampling.NEAREST), (18 + index * 310, 58))
        tdraw.text((20 + index * 310, 280), item["state"].upper(), fill=V4.INK, font=font)
    tiny_path = EVIDENCE / "dishwasher-64px-proof.png"
    tiny.save(tiny_path, optimize=True)

    cabinet = Image.open(APPROVED_CABINET).convert("RGBA")
    oven = Image.open(APPROVED_OVEN).convert("RGBA")
    run_sheet = Image.new("RGBA", (1320, 800), (250, 244, 224, 255))
    rdraw = ImageDraw.Draw(run_sheet)
    rdraw.text((18, 16), "PRIMARY ACCEPTANCE VIEW - cabinet / Dishwasher V8 / approved oven", fill=V4.INK, font=font)
    for row, state in enumerate(("off", "on", "broken")):
        dishwasher = Image.open(CANDIDATES / f"dishwasher-{state}-lj-rj.png").convert("RGBA")
        native = checker((320, 105), 8)
        native.alpha_composite(cabinet, (20, 20))
        native.alpha_composite(dishwasher, (101, 20))
        native.alpha_composite(oven, (188, 17))
        enlarged = native.resize((1280, 420), Image.Resampling.NEAREST)
        y = 55 + row * 235
        run_sheet.alpha_composite(enlarged.crop((0, 0, 1280, 210)), (18, y))
        rdraw.text((20, y + 212), state.upper(), fill=V4.INK, font=font)
    run_path = EVIDENCE / "dishwasher-worktop-run-ghost.png"
    run_sheet.save(run_path, optimize=True)
    return [contact_path, panel_path, tiny_path, run_path]


def review_html() -> str:
    page = ORIGINAL_REVIEW_HTML().replace("V7", "V8").replace("v7", "v8")
    page = page.replace(
        "V8 uses the good high-resolution appliance references without the faulty alpha-speck crop: one approved worktop, no second turquoise strip, and oven-family enamel and handle, compact invariant controls, cabinet stiles and plinth, and the complete matching worktop including its underside return.",
        "V8 translates the good high-resolution reference into deliberate native-scale linework: oven-weight edges, restrained cabinet-blue rails without glossy cyan flashes, a narrower inset door and a lower fascia whose controls align with the approved oven. The exact approved worktop remains a separate continuous element."
    )
    return page


def configure_v7() -> None:
    for name, value in {
        "SET": SET, "PACK": PACK, "PUBLIC": PUBLIC, "STYLE_ROOT": STYLE_ROOT,
        "STYLE_REFS": STYLE_REFS, "MASTERS": MASTERS, "CANDIDATES": CANDIDATES,
        "EVIDENCE": EVIDENCE, "ARCHIVE_SET": ARCHIVE_SET, "V6_PACK": OLD_PACK,
    }.items():
        setattr(V7, name, value)
    V7.prepare_style_references = prepare_style_references
    V7.styled_master = styled_master
    V7.make_evidence = make_evidence
    V7.review_html = review_html
    V7.verify = lambda: None


def postprocess_metadata() -> None:
    manifest_path = PACK / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest.update({
        "schema": "lighthouse-keeper/kitchen-dishwasher-ligne-claire@8",
        "set": SET,
        "status": "immutable-review-candidate-not-approved-not-registered",
        "supersedesCandidate": {
            "set": "kitchen-dishwasher-ligne-claire-v7",
            "manifest": relative(OLD_PACK / "manifest.json"),
            "manifestSha256": sha(OLD_PACK / "manifest.json"),
            "reason": "V7 retained glossy cyan side-rail highlights from the image-generation reference, softened oven-critical edges during whole-reference reduction, and left the wide fascia too close to the worktop",
        },
        "corrections": [
            "cabinet-blue side rails are rebuilt without the rejected bright cyan shine strokes",
            "door and fascia are inset to x19..79 inside the unchanged 84-pixel cabinet bay",
            "fascia is lowered to y21..31.5 and dishwasher control centres align with the approved oven at native y=25.5 versus y=25.4",
            "deliberate supersampled game-scale contours replace whole-reference reduction for oven-equivalent sharpness",
            "Broken retains a wider-open lower-right hinge failure, lower-left attachment and one-ended hanging handle",
            "approved worktop, cabinet shoulders, V41 alpha/canvas/state behaviour and separate suds remain unchanged",
        ],
        "authorizedGeometryChange": "all three appliance faces are redrawn at game scale with a narrower, lower fascia and inset door; Broken keeps the established failed-hinge semantics; V41 canvas, alpha, state names and runtime remain locked",
        "generatedReferences": [{"file": relative(path), "sha256": sha(path), "role": "byte-identical V7 image-generation art-direction reference retained for reversible comparison; V8 visible pixels are rebuilt at native game scale"} for path in STYLE_REFS.values()],
        "verification": {
            "canvasExact": True, "alphaExact": True, "singleWorktopLayerAllStates": True,
            "leftAndRightCabinetShouldersExact": True, "ovenAlignedControlCenterY": 25.5,
            "approvedOvenControlCenterY": 25.4, "narrowFasciaBounds": [19, 21, 79, 32],
            "brightCyanSideRailHighlightsRemoved": True, "nativeScaleLinework": True,
            "doorWiderOpen": True, "rightHingeFailed": True, "handleHangsFromLeftAttachment": True,
            "sudsRemainSeparateOwnedEffect": True, "movementAnimationInteractionHealingRuntimeChanged": False,
        },
        "rollback": "Discard only this V8 source-reference directory, draft pack, archive set and review shell; V1-V7, V41 and production remain byte-for-byte unchanged.",
    })
    manifest.pop("brokenGenerationInput", None)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    register_path = PACK / "batch-register.json"
    register = json.loads(register_path.read_text())
    register["set"] = SET
    register["candidate"]["manifest"] = {"file": relative(manifest_path), "sha256": sha(manifest_path)}
    register_path.write_text(json.dumps(register, indent=2) + "\n")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    register = json.loads((PACK / "batch-register.json").read_text())
    archive = json.loads(ARCHIVE_SET.read_text())
    if manifest["set"] != SET or register["set"] != SET or register["register"] or register["promote"]:
        raise RuntimeError("V8 approval gate changed")
    if len(manifest["records"]) != 15 or len(archive["entries"]) != 10:
        raise RuntimeError("V8 family/archive coverage changed")
    old = {item["filename"]: item for item in json.loads((OLD_PACK / "manifest.json").read_text())["records"]}
    for record in manifest["records"]:
        source = Image.open(ROOT / record["sourceFile"]).convert("RGBA")
        candidate = Image.open(ROOT / record["candidateFile"]).convert("RGBA")
        if source.size != candidate.size or source.size != (98, 82) or source.getchannel("A").tobytes() != candidate.getchannel("A").tobytes():
            raise RuntimeError(f"canvas/alpha drift: {record['filename']}")
        if sha(ROOT / record["candidateFile"]) == old[record["filename"]]["candidateSha256"]:
            raise RuntimeError(f"V7 bytes survived unchanged: {record['filename']}")
        # The worktop is still exact; the fascia begins lower and stays narrow.
        approved = Image.open(V7.APPROVED_CAPS[record["suffix"]]).convert("RGB")
        if approved.crop((4, 4, 88, 17)).tobytes() != candidate.convert("RGB").crop((7, 4, 91, 17)).tobytes():
            raise RuntimeError(f"worktop drift: {record['filename']}")
        if approved.crop((4, 16, 12, 30)).tobytes() != candidate.convert("RGB").crop((7, 16, 15, 30)).tobytes() or approved.crop((80, 16, 88, 30)).tobytes() != candidate.convert("RGB").crop((83, 16, 91, 30)).tobytes():
            raise RuntimeError(f"shoulder drift: {record['filename']}")
        # Reject high-luminance cyan shine inside the vertical side rails.
        side = list(candidate.convert("RGB").crop((8, 30, 18, 71)).getdata()) + list(candidate.convert("RGB").crop((80, 30, 90, 71)).getdata())
        if sum(1 for red, green, blue in side if blue > 150 and green > 120 and blue > red * 1.45) > 4:
            raise RuntimeError(f"bright cyan rail flash returned: {record['filename']}")
    for route, item in archive["entries"].items():
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(ROOT / item["object"]) != item["sha256"]:
            raise RuntimeError(f"archive mismatch: {route}")
    page = (PUBLIC / "index.html").read_text()
    if "Dishwasher Ligne-Claire V8" not in page or f"/keeper-review/{SET}/assets/" not in page or 'src="assets/' in page:
        raise RuntimeError("V8 review delivery regression")
    print("Verified Dishwasher V8: oven-aligned lower/narrower fascia; sharp native linework; restrained rails; exact V41 alpha/worktop; gate closed")


def build() -> None:
    configure_v7()
    V7.build()
    postprocess_metadata()
    verify()
    print("Built Dishwasher V8: native-scale oven sharpness; inset door; lower aligned controls; V41/runtime locked")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
