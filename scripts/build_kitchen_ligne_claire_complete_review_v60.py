#!/usr/bin/env python3
"""Build immutable Kitchen V60 with the approved kettle presented ~20% smaller.

The V47 source pixels remain byte-identical.  This builder changes only the
workbench draw rectangles, effect registration and detached-lid pivot while
retaining the cabinet anchor and the approved support plane.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OLD_SET = "kitchen-ligne-claire-complete-review-v59"
SET = "kitchen-ligne-claire-complete-review-v60"
OLD_PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v59"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v60"
OLD_PUBLIC = ROOT / "public/keeper-review" / OLD_SET
PUBLIC = ROOT / "public/keeper-review" / SET
OLD_ARCHIVE = ROOT / "review-archive/sets" / f"{OLD_SET}.json"
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"
OBJECT_ROOT = ROOT / "review-archive/objects"

OLD_RECT = "function kettleRect(state){return state==='broken'?{sx:20,sy:30,sw:216,sh:196,x:pos.cabinetA+11,y:82,w:62,h:59}:{sx:20,sy:53,sw:200,sh:172,x:pos.cabinetA+14,y:90,w:56,h:51}}"
NEW_RECT = "function kettleRect(state){return state==='broken'?{sx:20,sy:30,sw:216,sh:196,x:pos.cabinetA+17,y:94,w:50,h:47}:{sx:20,sy:53,sw:200,sh:172,x:pos.cabinetA+19,y:100,w:46,h:41}}"
OLD_STEAM = "if(state==='broken')ctx.drawImage(im,frame*cell[0],0,...cell,pos.cabinetA+27,63,27,42);else ctx.drawImage(im,frame*cell[0],0,...cell,pos.cabinetA+54,69,20,36)"
NEW_STEAM = "if(state==='broken')ctx.drawImage(im,frame*cell[0],0,...cell,pos.cabinetA+30,71,22,34);else ctx.drawImage(im,frame*cell[0],0,...cell,pos.cabinetA+52,76,16,29)"
OLD_LID = "drawKettleFrame(imgs['kettle--kettle-broken-lid.png'],rect,lid,{x:rect.x+22,y:rect.y+18})"
NEW_LID = "drawKettleFrame(imgs['kettle--kettle-broken-lid.png'],rect,lid,{x:rect.x+18,y:rect.y+14})"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def replace_versions(value):
    if isinstance(value, dict):
        return {key: replace_versions(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_versions(item) for item in value]
    if isinstance(value, str):
        return value.replace("V59", "V60").replace("v59", "v60")
    return value


def archive_object(source: Path) -> Path:
    digest = sha(source)
    target = OBJECT_ROOT / digest[:2] / f"{digest}{source.suffix.lower()}"
    if target.exists() and sha(target) != digest:
        raise RuntimeError(f"content-addressed archive collision: {target}")
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return target


def draw_kettle(room: Image.Image, state: str, rect: tuple[int, int, int, int]) -> None:
    source = Image.open(PACK / "candidates" / f"kettle--kettle-{state}.png").convert("RGBA")
    crop = (20, 30, 236, 226) if state == "broken" else ((20, 53, 220, 225))
    x, y, width, height = rect
    rendered = source.crop(crop).resize((width, height), Image.Resampling.BILINEAR)
    room.alpha_composite(rendered, (x, y))


def make_scale_evidence() -> Path:
    font = ImageFont.load_default()
    sheet = Image.new("RGBA", (1040, 930), (247, 241, 222, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 15), "KETTLE V47 PRESENTATION SCALE - identical source bytes / fixed centre / fixed support plane y141", fill=(5, 24, 36), font=font)
    draw.text((90, 40), "V59 live size", fill=(5, 24, 36), font=font)
    draw.text((590, 40), "V60 approximately 80%", fill=(5, 24, 36), font=font)
    background = Image.open(PACK / "workbench-assets/room-background-exact.png").convert("RGBA")
    cabinet = Image.open(PACK / "workbench-assets/cabinet-a-le-re.png").convert("RGBA")
    old = {"off": (182, 90, 56, 51), "on": (182, 90, 56, 51), "broken": (179, 82, 62, 59)}
    new = {"off": (187, 100, 46, 41), "on": (187, 100, 46, 41), "broken": (185, 94, 50, 47)}
    for row, state in enumerate(("off", "on", "broken")):
        y = 62 + row * 290
        for col, rects in enumerate((old, new)):
            room = background.copy()
            room.alpha_composite(cabinet, (164, 130))
            draw_kettle(room, state, rects[state])
            native = room.crop((150, 68, 270, 154))
            enlarged = native.resize((360, 258), Image.Resampling.NEAREST)
            sheet.alpha_composite(enlarged, (60 + col * 520, y))
        draw.text((18, y + 263), f"{state.upper()} - centre x210; support plane y141", fill=(5, 24, 36), font=font)
    path = PACK / "evidence/contact-kettle-scale-v60.png"
    sheet.save(path, optimize=True)
    return path


def patch_page() -> None:
    page = (OLD_PUBLIC / "index.html").read_text().replace("V59", "V60").replace("v59", "v60")
    # The inherited V59 fitted-carcase proof keeps its immutable basename.
    page = page.replace("contact-fitted-carcass-v60.png", "contact-fitted-carcass-v59.png")
    for before, after, label in (
        (OLD_RECT, NEW_RECT, "kettle draw rectangles"),
        (OLD_STEAM, NEW_STEAM, "steam registration"),
        (OLD_LID, NEW_LID, "lid pivot"),
        ('"version":42', '"version":60', "embedded workbench version"),
    ):
        if page.count(before) != 1:
            raise RuntimeError(f"expected one {label} match, found {page.count(before)}")
        page = page.replace(before, after)
    page = page.replace(
        '"supportAssetId":"cabinetA","supportPlaneY":141,',
        '"supportAssetId":"cabinetA","supportPlaneY":141,"presentation":{"placementMode":"cabinet-anchored","independentlyMovable":false,"requestedScale":0.8,"centreXWithinBay":42,"sourceArtChanged":false},',
    )
    page = page.replace(
        "Approved/static art and V41 movement, snapping, healing, Broken locking and repair behaviour remain unchanged.",
        "Approved/static art and V41 movement, snapping, healing, Broken locking and repair behaviour remain unchanged. V60 presents the cabinet-anchored kettle at approximately 80% of its former live-room size while keeping its centre and support plane fixed.",
    )
    page = page.replace(
        "only this V46 motion/SFX presentation remains unapproved.",
        "its V46 motion/SFX behaviour is approved; only V60's smaller room registration is under review.",
    )
    page = page.replace(
        "the Kettle V47 art and V46 motion/SFX presentation are approved and carried forward unchanged.",
        "the Kettle V47 art and V46 motion/SFX trajectories remain approved and byte-identical; only V60's smaller live-room registration is under review.",
    )
    page = page.replace(
        "The approved kettle art and V46 motion/SFX presentation, movement, Broken locking, state transitions and effect ownership are unchanged.",
        "The approved kettle art, V46 motion/SFX trajectories, movement, Broken locking, state transitions and effect ownership are unchanged; only its live-room scale and matching layer registration differ.",
    )
    page = page.replace(
        "V60 changes only appliance-shell composition and the join repair pixels.",
        "V60 inherits the appliance-shell and join correction and changes only the kettle's live-room scale/layer registration.",
    )
    addition = (
        '<section class="panel"><h2>V60 · cabinet-anchored kettle scale</h2>'
        '<p class="rule">Kettle V47 remains attached to Cabinet A rather than becoming an independently movable object. '
        'Its Off/On footprint is 46 × 41 native room pixels and its Broken footprint is 50 × 47: approximately 80% of the V59 presentation. '
        'Every state keeps centre x42 within the supporting bay and the same countertop contact plane at y141.</p>'
        '<p class="warn">The approved V47 PNGs are byte-identical. The detached lid still uses its own transform layer, steam remains non-transforming and re-registered over the open top, and repair still stops motion and sound immediately.</p></section>'
        '<article class="panel"><h2>V60 native-scale kettle comparison</h2><img class="contact" src="/keeper-review/kitchen-ligne-claire-complete-review-v60/assets/contact-kettle-scale-v60.png" alt="V59 and V60 kettle live-room presentation compared at enlarged native pixels"></article>'
    )
    page = page.replace("</main></body></html>", addition + "</main></body></html>")
    PUBLIC.mkdir(parents=True)
    (PUBLIC / "index.html").write_text(page)


def build() -> None:
    if PACK.exists() or PUBLIC.exists() or ARCHIVE_SET.exists():
        raise RuntimeError("V60 immutable outputs already exist; run with --verify")
    shutil.copytree(OLD_PACK, PACK)
    patch_page()
    evidence = make_scale_evidence()

    manifest_path = PACK / "manifest.json"
    manifest = replace_versions(json.loads(manifest_path.read_text()))
    for sheet in manifest["contactSheets"]:
        sheet["file"] = sheet["file"].replace("contact-fitted-carcass-v60.png", "contact-fitted-carcass-v59.png")
    manifest.update({
        "set": SET,
        "version": 60,
        "scope": "V59 fitted-carcase candidate plus an approximately 20% smaller cabinet-anchored Kettle V47 live-room presentation",
        "rollback": "Discard only this V60 pack, archive set and review shell; V59 and all approved source art, behaviour and production remain byte-identical.",
    })
    manifest["workbench"].update({
        "rootAbsoluteAssetPrefix": f"/keeper-review/{SET}/assets/",
        "kettlePresentationScale": {"requested": 0.8, "offOnPixels": [46, 41], "brokenPixels": [50, 47], "centreXWithinBay": 42, "supportPlaneY": 141},
        "kettleIndependentMovement": False,
        "kettleSourceArtChanged": False,
        "kettleStateBehaviourChanged": False,
    })
    manifest["contactSheets"].append({"family": "kettle-scale-v60", "file": rel(evidence), "sha256": sha(evidence), "rows": 3})
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    (PACK / "contact-sheet-index.json").write_text(json.dumps({"set": SET, "sheets": manifest["contactSheets"]}, indent=2) + "\n")

    old_archive = json.loads(OLD_ARCHIVE.read_text())
    entries = {}
    for old_route, item in old_archive["entries"].items():
        entries[old_route.replace(OLD_SET, SET)] = item
    stored = archive_object(evidence)
    route = f"/keeper-review/{SET}/assets/{evidence.name}"
    digest = sha(stored)
    entries[route] = {
        "sha256": digest,
        "extension": stored.suffix,
        "bytes": stored.stat().st_size,
        "object": rel(stored),
        "url": f"{old_archive['objectsBaseUrl']}/{digest[:2]}/{digest}{stored.suffix}",
    }
    archive = {
        "version": 1,
        "set": SET,
        "page": {"path": rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html"), "bytes": (PUBLIC / "index.html").stat().st_size},
        "objectsBaseUrl": old_archive["objectsBaseUrl"],
        "entries": dict(sorted(entries.items())),
    }
    ARCHIVE_SET.write_text(json.dumps(archive, indent=2) + "\n")

    register_path = PACK / "batch-register.json"
    register = replace_versions(json.loads(register_path.read_text()))
    register["set"] = SET
    register["candidate"] = {
        "manifest": {"file": rel(manifest_path), "sha256": sha(manifest_path)},
        "publicShell": {"file": rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")},
    }
    register["publishedAssets"] = [
        {
            "source": item["object"],
            "sourceSha256": item["sha256"],
            "publicAssemblyPath": route.removeprefix("/"),
        }
        for route, item in archive["entries"].items()
    ]
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    verify()
    print("Built Kitchen V60: Kettle V47 at approximately 80% live-room scale; cabinet anchor retained; gate closed")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    register = json.loads((PACK / "batch-register.json").read_text())
    archive = json.loads(ARCHIVE_SET.read_text())
    page = (PUBLIC / "index.html").read_text()
    if manifest["set"] != SET or manifest["version"] != 60 or register["register"] or register["promote"]:
        raise RuntimeError("V60 approval gate changed")
    if len(manifest["objects"]) != 60 or len(manifest["contactSheets"]) != 18 or len(archive["entries"]) != 142:
        raise RuntimeError("V60 coverage changed")
    for marker in (NEW_RECT, NEW_STEAM, NEW_LID, '"independentlyMovable":false', "V60 native-scale kettle comparison"):
        if marker not in page:
            raise RuntimeError(f"V60 page contract drift: {marker}")
    if OLD_RECT in page or OLD_STEAM in page or OLD_LID in page:
        raise RuntimeError("V59 kettle registration survived in V60")
    if 19 + 46 / 2 != 42 or 100 + 41 != 141 or 17 + 50 / 2 != 42 or 94 + 47 != 141:
        raise RuntimeError("V60 kettle centre/support-plane arithmetic drift")
    for name in ("kettle--kettle-off.png", "kettle--kettle-on.png", "kettle--kettle-broken.png"):
        if sha(PACK / "candidates" / name) != sha(OLD_PACK / "candidates" / name):
            raise RuntimeError(f"approved kettle source changed: {name}")
    for route, item in archive["entries"].items():
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(ROOT / item["object"]) != item["sha256"]:
            raise RuntimeError(f"V60 archive mismatch: {route}")
    if archive["page"]["sha256"] != sha(PUBLIC / "index.html"):
        raise RuntimeError("V60 page hash drift")
    print("Verified V60: source art byte-identical; 80% presentation; fixed centre/support plane; cabinet anchor and state behaviour retained")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
