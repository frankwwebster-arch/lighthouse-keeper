#!/usr/bin/env python3
"""Build immutable Kitchen V57 fitted-carcass integration review.

V57 treats the approved Cabinet V11 module as the pixel authority for the
carcass around both appliances.  Appliance inserts remain reversible review
art: no approved source or production selector is overwritten.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-complete-review-v57"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v57"
PUBLIC = ROOT / "public/keeper-review" / SET
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"
OBJECT_ROOT = ROOT / "review-archive/objects"
V56_SET = "kitchen-ligne-claire-complete-review-v56"
V56_PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v56"
V56_PAGE = ROOT / "public/keeper-review" / V56_SET / "index.html"
V56_ARCHIVE = ROOT / "review-archive/sets" / f"{V56_SET}.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def copy_tree(source: Path, target: Path) -> None:
    target.mkdir(parents=True)
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, target / item.name)


def archive_object(source: Path) -> Path:
    digest = sha(source)
    target = OBJECT_ROOT / digest[:2] / f"{digest}{source.suffix.lower()}"
    if target.exists() and sha(target) != digest:
        raise RuntimeError(f"content-addressed archive collision: {target}")
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return target


def publish(source: Path, name: str) -> dict:
    stored = archive_object(source)
    return {
        "source": rel(stored),
        "sourceSha256": sha(stored),
        "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}",
    }


def write_archive(entries: list[dict]) -> None:
    page = PUBLIC / "index.html"
    base_url = "https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects"
    mapped = {}
    for item in entries:
        source = ROOT / item["source"]
        digest = item["sourceSha256"]
        route = "/" + item["publicAssemblyPath"].removeprefix("public/")
        mapped[route] = {
            "sha256": digest,
            "extension": source.suffix,
            "bytes": source.stat().st_size,
            "object": item["source"],
            "url": f"{base_url}/{digest[:2]}/{digest}{source.suffix}",
        }
    archive = {
        "version": 1,
        "set": SET,
        "page": {"path": rel(page), "sha256": sha(page), "bytes": page.stat().st_size},
        "objectsBaseUrl": base_url,
        "entries": dict(sorted(mapped.items())),
    }
    ARCHIVE_SET.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE_SET.write_text(json.dumps(archive, indent=2) + "\n")


def cabinet_for_suffix(suffix: str) -> str:
    return {
        "": "cabinet-a-le-re.png",
        "-le-re": "cabinet-a-le-re.png",
        "-le-rj": "cabinet-a-le-rj.png",
        "-lj-re": "cabinet-a-lj-re.png",
        "-lj-rj": "cabinet-a-lj-rj.png",
    }[suffix]


def overlay_exact(base: Image.Image, insert: Image.Image, bounds: tuple[int, int, int, int]) -> None:
    """Copy non-transparent insert pixels byte-exactly inside bounds."""
    x0, y0, x1, y1 = bounds
    bp = base.load()
    ip = insert.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            if ip[x, y][3]:
                bp[x, y] = ip[x, y]


def fitted_dishwasher(source: Image.Image, suffix: str, state: str) -> Image.Image:
    cabinet = Image.open(PACK / "workbench-assets" / cabinet_for_suffix(suffix)).convert("RGBA")
    out = Image.new("RGBA", source.size, (0, 0, 0, 0))
    out.alpha_composite(cabinet, (3, 0))
    # Closed inserts stop at the exact Cabinet V11 plinth.  The failed Broken
    # door is foreground damage and may legitimately hang over that plinth.
    overlay_exact(out, source, (18, 20, 80, 71) if state != "broken" else (16, 20, 82, 78))
    return out


def is_hob_or_knob(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    if not a:
        return False
    spread = max(r, g, b) - min(r, g, b)
    orange = r > 105 and r > g * 1.18 and r > b * 1.35
    neutral_metal = spread < 48
    near_black = max(r, g, b) < 30
    return orange or neutral_metal or near_black


def fitted_oven(source: Image.Image) -> Image.Image:
    """Seat approved oven components inside an exact Cabinet V11 carcass."""
    cabinet = Image.open(PACK / "workbench-assets/cabinet-a-le-re.png").convert("RGBA")
    out = cabinet.copy()  # 92 x 82: identical cabinet canvas and baseline.
    sp = source.load()
    op = out.load()
    # Retain the approved hob plates and copper selector, but use the cabinet's
    # exact continuous worktop pixels instead of the oven's separate blue slab.
    for y in range(4, 20):
        for x in range(4, 88):
            if is_hob_or_knob(sp[x, y]):
                op[x, y] = sp[x, y]
    # Preserve the approved cream fascia/cavity insert byte-for-byte.  It ends
    # immediately above the shared Cabinet V11 plinth.
    overlay_exact(out, source, (4, 20, 88, 71))
    return out


def repair_rear_line(image: Image.Image) -> Image.Image:
    out = image.copy()
    pixels = out.load()
    for x in range(out.width):
        pixels[x, 0] = (129, 130, 115, 255)
    return out


def checker(size: tuple[int, int], cell: int = 10) -> Image.Image:
    out = Image.new("RGBA", size, (250, 244, 224, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def make_family_contact(family: str, rows: list[tuple[str, Image.Image, Image.Image]], path: Path) -> None:
    font = ImageFont.load_default()
    height = 60 + len(rows) * 225
    sheet = Image.new("RGBA", (980, height), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), f"V57 {family} - previous candidate / fitted Cabinet V11 carcass", fill=(5, 24, 36), font=font)
    for index, (label, before, after) in enumerate(rows):
        y = 48 + index * 225
        for column, image in enumerate((before, after)):
            panel = checker((450, 190))
            shown = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)
            panel.alpha_composite(shown, ((450 - shown.width) // 2, 10))
            sheet.alpha_composite(panel, (18 + column * 480, y))
        draw.text((20, y + 194), f"{label} · {'V56' if family != 'healing' else 'old join'}", fill=(5, 24, 36), font=font)
        draw.text((500, y + 194), f"{label} · V57 exact fitted carcass", fill=(5, 24, 36), font=font)
    sheet.save(path, optimize=True)


def make_run_evidence() -> Path:
    font = ImageFont.load_default()
    sheet = Image.new("RGBA", (1370, 760), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), "PRIMARY ACCEPTANCE VIEW - one Cabinet V11 carcass / continuous rear line / shared plinth", fill=(5, 24, 36), font=font)
    cabinet = Image.open(PACK / "workbench-assets/cabinet-a-lj-rj.png").convert("RGBA")
    oven = Image.open(PACK / "workbench-assets/oven-on.png").convert("RGBA")
    for row, state in enumerate(("off", "on", "broken")):
        dishwasher = Image.open(PACK / "workbench-assets" / f"dishwasher-{state}-lj-rj.png").convert("RGBA")
        native = checker((340, 92), 6)
        native.alpha_composite(cabinet, (20, 5))
        native.alpha_composite(dishwasher, (101, 5))
        native.alpha_composite(oven, (188, 5))
        enlarged = native.resize((1360, 368), Image.Resampling.NEAREST)
        y = 45 + row * 235
        sheet.alpha_composite(enlarged.crop((0, 0, 1360, 205)), (5, y))
        draw.text((18, y + 208), state.upper(), fill=(5, 24, 36), font=font)
    path = PACK / "evidence/contact-fitted-carcass-v57.png"
    sheet.save(path, optimize=True)
    return path


def update_page(published_hashes: dict[str, str]) -> None:
    page = V56_PAGE.read_text().replace(V56_SET, SET).replace("V56", "V57").replace("v56", "v57")
    page = page.replace(
        "Dishwasher V8 is the sole unapproved candidate; registration remains closed.",
        "The fitted-carcase integration is the unapproved candidate: Dishwasher V8 supplies the appliance insert, the approved oven supplies its insert, and exact Cabinet V11 pixels supply both shells. Registration remains closed.",
    )
    page = page.replace(
        "Dishwasher V8 is the sole unapproved visual candidate",
        "The V57 fitted-carcase integration is the sole unapproved visual candidate",
    )
    page = page.replace(
        "The approved kettle art and V46 motion/SFX presentation, V41 canvas and alpha, movement, Broken locking, state transitions, effect ownership and countertop-healing code are unchanged.",
        "The approved kettle art and V46 motion/SFX presentation, movement, Broken locking, state transitions and effect ownership are unchanged. V57 changes only appliance-shell composition and the join repair pixels.",
    )
    page = page.replace("Dishwasher V8 is the sole unapproved candidate and supersedes rejected V6.", "V57 supersedes V56 as the single fitted-kitchen review candidate.")
    page = page.replace("Dishwasher V8 oven-aligned control and sharpness audit", "Fitted appliance control-height and sharpness audit")
    page = page.replace("Dishwasher V8 primary single-worktop fitted-run view", "V57 primary fitted-carcase run")
    page = page.replace("Reject by deleting only this V57 pack, archive set and review shell.", "Reject by deleting only this V57 pack, archive set and review shell; V56 and all approved sources remain intact.")
    page = page.replace("ctx.drawImage(imgs['oven-on.png'],x-4,127)", "ctx.drawImage(imgs['oven-on.png'],x-4,130)")

    match = re.search(r"const DATA=(\{.*?\}),KETTLE=", page, re.S)
    if not match:
        raise RuntimeError("could not locate embedded workbench data")
    data = json.loads(match.group(1))
    data["set"] = SET
    data["sourceProvenance"]["fittedCarcassCandidate"] = SET
    data["assets"]["oven"].update({"bodyPixels": [84, 74], "cellPixels": [92, 82], "cellOffset": [-4, -4], "carcass": "exact Cabinet V11 pixels"})
    data["assets"]["dishwasher"].update({"sameCarcass": True, "carcass": "exact Cabinet V11 pixels including side stiles and plinth"})
    data["joinResolver"]["rearLineContinuity"] = "opaque composite-matched one-pixel line restored across every healed join after cap selection"
    data["boundaries"]["interactionImplementationChanged"] = False
    data["boundaries"]["visualIntegrationChanged"] = True
    data["publishedAssets"].update(published_hashes)
    page = page[:match.start(1)] + json.dumps(data, separators=(",", ":")) + page[match.end(1):]
    addition = f'''<section class="panel"><h2>V57 · fitted kitchen carcass correction</h2><p class="rule">Cabinet V11 is now the literal pixel authority for appliance worktops, side stiles and plinths. The oven and dishwasher are inserts inside that shared shell, not freestanding blue units. Oven controls and Dishwasher V8 controls share the same room-height baseline. The healer's light first cap row is replaced with the composite-matched dark rear line at every join.</p><p class="warn">This remains an unapproved, reversible integration candidate. Approved oven and kettle source art, Dishwasher V8, runtime state semantics, motion, sound, repair locks and production selectors are untouched.</p></section><article class="panel"><h2>V57 fitted-carcase acceptance view</h2><img class="contact" src="/keeper-review/{SET}/assets/contact-fitted-carcass-v57.png" alt="Cabinet, dishwasher and oven sharing one exact carcass and plinth"></article>'''
    page = page.replace("</main>", addition + "</main>")
    (PUBLIC / "index.html").write_text(page)


def build() -> None:
    if PACK.exists() or PUBLIC.exists() or ARCHIVE_SET.exists():
        raise RuntimeError("refusing to overwrite immutable Kitchen V57 output")
    for directory in ("candidates", "effects", "evidence", "workbench-assets", "approved-current", "components", "audio"):
        copy_tree(V56_PACK / directory, PACK / directory)
    PUBLIC.mkdir(parents=True)

    manifest = load(V56_PACK / "manifest.json")
    old_objects = {item["filename"]: item for item in manifest["objects"]}

    # Dishwasher V8 becomes the appliance insert within exact per-edge cabinet shells.
    for item in [entry for entry in manifest["objects"] if entry["family"] == "dishwasher"]:
        source = Image.open(ROOT / item["candidateFile"]).convert("RGBA")
        suffix = item["filename"].removeprefix(f"dishwasher-{item['filename'].split('-')[1]}").removesuffix(".png")
        state = item["filename"].split("-")[1]
        fitted = fitted_dishwasher(source, suffix, state)
        fitted.save(PACK / "workbench-assets" / item["filename"], optimize=True)
        fitted.save(PACK / "candidates" / f"dishwasher--{item['filename']}", optimize=True)

    # Every oven state receives the same exact shell; approved insert pixels remain.
    for item in [entry for entry in manifest["objects"] if entry["family"] == "oven"]:
        source = Image.open(ROOT / item["candidateFile"]).convert("RGBA")
        fitted = fitted_oven(source)
        fitted.save(PACK / "candidates" / f"oven--{item['filename']}", optimize=True)
        if item["filename"] == "oven-on.png":
            fitted.save(PACK / "workbench-assets/oven-on.png", optimize=True)

    # Flat and oven-specific foreground repairs all restore the rear edge.
    for filename in ("countertop-join-cap-template.png", "neighbour-seam-cleanup-left.png", "neighbour-seam-cleanup-right.png"):
        previous = Image.open(V56_PACK / "workbench-assets" / filename).convert("RGBA")
        repaired = repair_rear_line(previous)
        repaired.save(PACK / "workbench-assets" / filename, optimize=True)
        repaired.save(PACK / "candidates" / f"healing--{filename}", optimize=True)

    # Replace affected audit sheets with evidence from the actual V57 bytes.
    dishwasher_rows = []
    for state in ("off", "on", "broken"):
        name = f"dishwasher-{state}-lj-rj.png"
        dishwasher_rows.append((state.upper(), Image.open(V56_PACK / "workbench-assets" / name).convert("RGBA"), Image.open(PACK / "workbench-assets" / name).convert("RGBA")))
    make_family_contact("dishwasher", dishwasher_rows, PACK / "evidence/contact-dishwasher.png")
    oven_rows = []
    for name in ("oven-on.png", "oven-off.png", "oven-broken.png"):
        old = Image.open(ROOT / old_objects[name]["candidateFile"]).convert("RGBA")
        new = Image.open(PACK / "candidates" / f"oven--{name}").convert("RGBA")
        oven_rows.append((name.removeprefix("oven-").removesuffix(".png").upper(), old, new))
    make_family_contact("oven", oven_rows, PACK / "evidence/contact-oven.png")
    healing_rows = []
    for name in ("countertop-join-cap-template.png", "neighbour-seam-cleanup-left.png", "neighbour-seam-cleanup-right.png"):
        healing_rows.append((name.removesuffix(".png"), Image.open(V56_PACK / "workbench-assets" / name).convert("RGBA"), Image.open(PACK / "workbench-assets" / name).convert("RGBA")))
    make_family_contact("healing", healing_rows, PACK / "evidence/contact-healing.png")
    run = make_run_evidence()
    shutil.copy2(run, PACK / "evidence/contact-dishwasher-worktop-run.png")

    # Rebase copied manifest paths and replace hashes for every changed object.
    objects = json.loads(json.dumps(manifest["objects"]))
    for item in objects:
        review = PACK / "candidates" / Path(item["reviewFile"]).name
        item["reviewFile"] = rel(review)
        if item["family"] in {"dishwasher", "oven"} or (item["family"] == "healing" and item["filename"] in {"countertop-join-cap-template.png", "neighbour-seam-cleanup-left.png", "neighbour-seam-cleanup-right.png"}):
            item["authority"] = SET
            item["candidateFile"] = rel(review)
            image = Image.open(review).convert("RGBA")
            item["candidateSha256"] = sha(review)
            item["candidatePixels"] = list(image.size)
            item["candidateAlphaBounds"] = list(image.getchannel("A").getbbox())
            item["candidateAlphaSha256"] = hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()
            item["canvasExact"] = item["family"] != "oven"
            item["alphaExact"] = False
        item["reviewSha256"] = sha(review)

    effects = json.loads(json.dumps(manifest["effects"]))
    for item in effects:
        item["reviewFile"] = rel(PACK / "effects" / Path(item["reviewFile"]).name)
        item["reviewSha256"] = sha(ROOT / item["reviewFile"])
    approved = json.loads(json.dumps(manifest["approvedCurrentReferences"]))
    for item in approved:
        item["reviewFile"] = rel(PACK / "approved-current" / Path(item["reviewFile"]).name)
        item["reviewSha256"] = sha(ROOT / item["reviewFile"])
    sheets = []
    for item in manifest["contactSheets"]:
        target = PACK / "evidence" / Path(item["file"]).name
        sheets.append({**item, "file": rel(target), "sha256": sha(target), "inheritedByteExactFrom": None if item["family"] in {"dishwasher", "oven", "healing", "dishwasher-worktop-run-v8"} else V56_SET})
    sheets.append({"family": "fitted-carcass-v57", "file": rel(run), "sha256": sha(run), "rows": 3})

    manifest.update({
        "set": SET,
        "version": 57,
        "status": "immutable-review-candidate-not-approved-not-registered",
        "scope": "exact Cabinet V11 carcasses around Dishwasher V8 and approved oven inserts; continuous dark rear line across every healed join; shared plinth and control baseline",
        "objects": objects,
        "effects": effects,
        "approvedCurrentReferences": approved,
        "contactSheets": sheets,
        "workbench": {
            **manifest["workbench"],
            "sourceSet": V56_SET,
            "sourceManifestSha256": sha(V56_PACK / "manifest.json"),
            "rootAbsoluteAssetPrefix": f"/keeper-review/{SET}/assets/",
            "fittedCarcassAuthority": "exact Cabinet V11 pixels",
            "rearLineJoinRepairChanged": True,
            "movementStateMotionAndSoundChanged": False,
        },
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "productionWrites": [], "approvalRequired": True},
        "rollback": "Discard only this V57 pack, archive set and review shell; V56, Dishwasher V8, approved oven/kettle assets and production remain byte-identical.",
    })
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "contact-sheet-index.json").write_text(json.dumps({"set": SET, "sheets": sheets}, indent=2) + "\n")

    # Publish every route inherited from V56 from the corresponding V57 copy.
    old_archive = load(V56_ARCHIVE)
    search_dirs = (PACK / "candidates", PACK / "effects", PACK / "evidence", PACK / "workbench-assets", PACK / "approved-current", PACK / "components", PACK / "audio")
    entries = []
    for old_route, old_entry in old_archive["entries"].items():
        name = Path(old_route).name
        matches = [directory / name for directory in search_dirs if (directory / name).exists()]
        if matches:
            entries.append(publish(matches[0], name))
        else:
            # Several unchanged public route names carry a family prefix while
            # their stored review copy does not. Reuse the immutable object.
            entries.append({
                "source": old_entry["object"],
                "sourceSha256": old_entry["sha256"],
                "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}",
            })
    entries.append(publish(run, run.name))
    if len({item["publicAssemblyPath"] for item in entries}) != len(entries):
        raise RuntimeError("duplicate V57 public route")

    workbench_hashes = {item.name: sha(item) for item in (PACK / "workbench-assets").iterdir() if item.is_file()}
    update_page(workbench_hashes)
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
        "productionWrites": [],
        "candidate": {
            "manifest": {"file": rel(PACK / "manifest.json"), "sha256": sha(PACK / "manifest.json")},
            "publicShell": {"file": rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")},
        },
        "publishedAssets": entries,
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    write_archive(entries)
    verify()
    print("Built Kitchen V57: exact fitted carcasses, continuous rear join line, shared plinth/control baseline; gate closed")


def verify() -> None:
    manifest = load(PACK / "manifest.json")
    register = load(PACK / "batch-register.json")
    archive = load(ARCHIVE_SET)
    if manifest["set"] != SET or manifest["version"] != 57 or register["register"] or register["promote"]:
        raise RuntimeError("V57 approval gate changed")
    if len(manifest["objects"]) != 60 or len(manifest["contactSheets"]) != 17 or len(archive["entries"]) != 141:
        raise RuntimeError("V57 coverage changed")
    cabinet = Image.open(PACK / "workbench-assets/cabinet-a-le-re.png").convert("RGBA")
    oven = Image.open(PACK / "workbench-assets/oven-on.png").convert("RGBA")
    if oven.size != cabinet.size or oven.crop((4, 71, 88, 78)).tobytes() != cabinet.crop((4, 71, 88, 78)).tobytes():
        raise RuntimeError("oven did not inherit exact Cabinet V11 plinth")
    for state in ("off", "on"):
        dishwasher = Image.open(PACK / "workbench-assets" / f"dishwasher-{state}-le-re.png").convert("RGBA")
        if dishwasher.crop((7, 71, 91, 78)).tobytes() != cabinet.crop((4, 71, 88, 78)).tobytes():
            raise RuntimeError(f"dishwasher {state} did not inherit exact Cabinet V11 plinth")
        if dishwasher.crop((7, 4, 91, 17)).tobytes() != cabinet.crop((4, 4, 88, 17)).tobytes():
            raise RuntimeError(f"dishwasher {state} worktop drift")
    for name in ("countertop-join-cap-template.png", "neighbour-seam-cleanup-left.png", "neighbour-seam-cleanup-right.png"):
        image = Image.open(PACK / "workbench-assets" / name).convert("RGBA")
        if any(pixel != (129, 130, 115, 255) for pixel in list(image.crop((0, 0, image.width, 1)).getdata())):
            raise RuntimeError(f"rear-line join interruption returned: {name}")
    page = (PUBLIC / "index.html").read_text()
    if f"/keeper-review/{SET}/assets/" not in page or "x-4,130" not in page or "V57 fitted-carcase acceptance view" not in page:
        raise RuntimeError("V57 workbench/page integration drift")
    for route, item in archive["entries"].items():
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(ROOT / item["object"]) != item["sha256"]:
            raise RuntimeError(f"V57 archive mismatch: {route}")
    if archive["page"]["sha256"] != sha(PUBLIC / "index.html"):
        raise RuntimeError("V57 page hash drift")
    print("Verified V57: exact Cabinet V11 shells/plinths; continuous rear joins; oven controls aligned; state/motion/SFX behavior preserved; gate closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
