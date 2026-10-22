#!/usr/bin/env python3
"""Build an immutable exact-geometry Ligne-Claire table/chair review."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-table-chair-ligne-claire-v1"
DATED = "kitchen-table-chair-ligne-claire-2026-10-22-v1"
VERSION = 1
PACK = ROOT / "art" / "drafts" / DATED
SOURCE = ROOT / "art" / "raw" / "kitchen-rebuild-modular-2026-10-19-v10" / "table-chair.png"
CONTRACT = ROOT / "art" / "drafts" / "kitchen-rebuild-modular-2026-10-19-v10" / "candidate-catalogue.json"
PUBLIC = ROOT / "public" / "keeper-review" / SET
DENSITY = 8
LINE = 6
INK = "#051824"
BLUE = "#235b85"
BLUE_DARK = "#1d4562"
COPPER = "#d36f2d"
COPPER_LIGHT = "#e7a638"
PALETTE = ((5, 24, 36), (35, 91, 133), (29, 69, 98), (211, 111, 45), (231, 166, 56))


def p(value: float) -> int:
    return round(value * DENSITY)


def box(values: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    return tuple(p(v) for v in values)  # type: ignore[return-value]


def pts(values: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(p(x), p(y)) for x, y in values]


def edge(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], colour: str = INK, closed: bool = False) -> None:
    draw.line(pts(values + ([values[0]] if closed else [])), fill=colour, width=LINE, joint="curve")


def polygon(draw: ImageDraw.ImageDraw, values: list[tuple[float, float]], fill: str) -> None:
    draw.polygon(pts(values), fill=fill)
    edge(draw, values, closed=True)


def rounded(draw: ImageDraw.ImageDraw, values: tuple[float, float, float, float], radius: float, fill: str) -> None:
    draw.rounded_rectangle(box(values), radius=p(radius), fill=fill, outline=INK, width=LINE)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def alpha_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.getchannel("A").tobytes()).hexdigest()


def master() -> Image.Image:
    image = Image.new("RGBA", (84 * DENSITY, 79 * DENSITY), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Table construction: one shallow top, one front apron, two true legs.
    polygon(draw, [(2.0, 22.0), (7.0, 18.0), (77.0, 18.0), (82.0, 22.0), (80.0, 29.5), (4.0, 29.5)], COPPER)
    edge(draw, [(5.0, 25.0), (79.0, 25.0)], INK if VERSION >= 3 else COPPER_LIGHT)
    polygon(draw, [(7.0, 29.0), (15.0, 29.0), (13.0, 78.8), (7.0, 78.8)], BLUE)
    polygon(draw, [(69.0, 29.0), (77.0, 29.0), (77.0, 78.8), (71.0, 78.8)], BLUE)

    # The single rear-facing chair remains centred and preserves the source
    # footprint, orientation, seat height and table overlap.
    rounded(draw, (20.5, 21.5, 63.5, 38.0), 6.5, COPPER)
    edge(draw, [(24.0, 29.5), (24.0, 59.0)], BLUE)
    edge(draw, [(60.0, 29.5), (60.0, 59.0)], BLUE)
    for x in (29.5, 36.0, 42.0, 48.0, 54.5):
        edge(draw, [(x, 34.0), (x, 55.0)], BLUE)
    rounded(draw, (21.5, 52.0, 62.5, 61.5), 3.0, COPPER)
    polygon(draw, [(25.0, 59.0), (33.0, 59.0), (27.0, 78.8), (21.0, 78.8)], BLUE)
    polygon(draw, [(51.0, 59.0), (59.0, 59.0), (64.0, 78.8), (58.0, 78.8)], BLUE)
    edge(draw, [(28.0, 67.0), (57.0, 67.0)], BLUE_DARK)
    return image


def register(authored: Image.Image, source: Image.Image) -> Image.Image:
    candidate = authored.resize(source.size, Image.Resampling.LANCZOS).convert("RGBA")
    if VERSION >= 2:
        # Exact source alpha can legitimately extend a pixel beyond the clean
        # authored fill. Supply a source-derived spot colour at only those
        # otherwise colourless authority pixels; never expose transparent RGB.
        output = []
        for made, original in zip(candidate.getdata(), source.getdata()):
            if original[3] and made[3] < 8:
                colour = min(PALETTE, key=lambda item: sum((item[i] - original[i]) ** 2 for i in range(3)))
                output.append((*colour, made[3]))
            else:
                output.append(made)
        candidate.putdata(output)
    candidate.putalpha(source.getchannel("A"))
    return candidate


def checker(size: tuple[int, int], cell: int = 18) -> Image.Image:
    out = Image.new("RGBA", size, (246, 240, 220, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(226, 216, 192, 255))
    return out


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable table/chair V1")
    for path in (PACK / "masters", PACK / "candidates", PACK / "evidence", PUBLIC / "assets"):
        path.mkdir(parents=True)
    source = Image.open(SOURCE).convert("RGBA")
    authored = master()
    candidate = register(authored, source)
    master_path = PACK / "masters" / "table-chair-master-8x.png"
    candidate_path = PACK / "candidates" / "table-chair.png"
    authored.save(master_path, optimize=True)
    candidate.save(candidate_path, optimize=True)

    font = ImageFont.load_default()
    sheet = Image.new("RGBA", (1320, 520), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), f"Table and single rear-facing chair - current / V{VERSION} candidate / geometry ghost / 64 px", fill=INK, font=font)
    for column, item in enumerate((source, candidate)):
        panel = checker((400, 430))
        shown = item.resize((item.width * 5, item.height * 5), Image.Resampling.LANCZOS)
        panel.alpha_composite(shown, ((400 - shown.width) // 2, (430 - shown.height) // 2))
        sheet.alpha_composite(panel, (10 + column * 410, 52))
    ghost = checker((400, 430))
    shown = candidate.resize((candidate.width * 5, candidate.height * 5), Image.Resampling.LANCZOS)
    ghost.alpha_composite(shown, ((400 - shown.width) // 2, (430 - shown.height) // 2))
    tint = Image.new("RGBA", source.size, (232, 72, 86, 0))
    tint.putalpha(source.getchannel("A").point(lambda v: round(v * .36)))
    tint = tint.resize(shown.size, Image.Resampling.LANCZOS)
    ghost.alpha_composite(tint, ((400 - shown.width) // 2, (430 - shown.height) // 2))
    sheet.alpha_composite(ghost, (830, 52))
    tiny = candidate.resize((64, round(79 * 64 / 84)), Image.Resampling.LANCZOS)
    sheet.alpha_composite(tiny, (1242, 92))
    draw.text((18, 488), "CURRENT", fill=INK, font=font)
    draw.text((428, 488), f"V{VERSION} CANDIDATE", fill=INK, font=font)
    draw.text((848, 488), "GHOST - red alpha is the exact authority envelope", fill=INK, font=font)
    evidence_path = PACK / "evidence" / "table-chair-current-candidate-ghost-64px.png"
    sheet.save(evidence_path, optimize=True)

    manifest = {
        "schema": f"lighthouse-keeper/kitchen-table-chair-ligne-claire@{VERSION}",
        "set": SET,
        "created": "2026-10-22",
        "status": "immutable-review-candidate-not-approved-not-registered",
        "sourceFile": SOURCE.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(SOURCE),
        "sourcePixels": list(source.size),
        "sourceAlphaBounds": list(source.getchannel("A").getbbox()),
        "sourceAlphaSha256": alpha_sha(source),
        "candidateFile": candidate_path.relative_to(ROOT).as_posix(),
        "candidateSha256": sha256(candidate_path),
        "candidatePixels": list(candidate.size),
        "candidateAlphaBounds": list(candidate.getchannel("A").getbbox()),
        "candidateAlphaSha256": alpha_sha(candidate),
        "masterFile": master_path.relative_to(ROOT).as_posix(),
        "masterSha256": sha256(master_path),
        "contractFile": CONTRACT.relative_to(ROOT).as_posix(),
        "contractSha256": sha256(CONTRACT),
        "unchanged": ["canvas", "alpha", "padding", "rear-facing chair orientation", "one-place table span", "seat height", "footprint", "room placement", "draw stack", "interaction behaviour"],
        "registration": {"register": False, "promote": False, "currentSelectorChanges": [], "approvalRequired": True},
        "evidence": {"file": evidence_path.relative_to(ROOT).as_posix(), "sha256": sha256(evidence_path)},
        "rollback": "Discard only this V1 pack and review route.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACK / "batch-register.json").write_text(json.dumps({"status": "blocked-pending-explicit-frank-approval", "register": False, "promote": False, "currentSelectorChanges": []}, indent=2) + "\n", encoding="utf-8")
    for src, name in ((SOURCE, "current--table-chair.png"), (candidate_path, "candidate--table-chair.png"), (evidence_path, evidence_path.name)):
        shutil.copy2(src, PUBLIC / "assets" / name)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Table Chair Ligne-Claire V{VERSION}</title><style>body{{margin:0;background:#f6e5b7;color:#051824;font:16px/1.45 system-ui}}header,main{{max-width:1320px;margin:auto;padding:22px}}header{{border-bottom:4px solid #051824}}.status{{display:inline-block;border:2px solid #051824;padding:6px 10px;background:#e7a638;font-weight:800}}article{{background:#fff9e8;border:2px solid #051824;margin:18px 0;padding:14px}}img{{display:block;width:100%;height:auto;image-rendering:auto}}.row{{display:flex;gap:30px;align-items:end;flex-wrap:wrap}}.checker{{background:repeating-conic-gradient(#eee6cf 0 25%,#d9cfb2 0 50%) 50%/18px 18px;padding:20px}}.native{{width:84px}}.small{{width:64px}}</style></head><body><header><span class="status">IMMUTABLE CANDIDATE - NOT CURRENT</span><h1>Table and rear-facing chair Ligne-Claire V{VERSION}</h1><p>One even contour weight, flat closed colours, no gradients or texture. Exact 84 x 79 canvas and byte-exact authority alpha; room placement and seating geometry are unchanged.</p></header><main><article><img src="/keeper-review/{SET}/assets/{evidence_path.name}"></article><article class="row"><div class="checker"><img class="native" src="/keeper-review/{SET}/assets/candidate--table-chair.png"></div><div class="checker"><img class="small" src="/keeper-review/{SET}/assets/candidate--table-chair.png"></div><p>Native 84 px / 64 px width</p></article></main></body></html>'''
    (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    source = Image.open(ROOT / manifest["sourceFile"]).convert("RGBA")
    candidate = Image.open(ROOT / manifest["candidateFile"]).convert("RGBA")
    if source.size != (84, 79) or candidate.size != source.size:
        raise RuntimeError("table/chair canvas drift")
    if alpha_sha(source) != alpha_sha(candidate) or source.getchannel("A").getbbox() != candidate.getchannel("A").getbbox():
        raise RuntimeError("table/chair alpha or bounds drift")
    if manifest["registration"]["register"] or manifest["registration"]["promote"]:
        raise RuntimeError("registration gate opened")
    html = (PUBLIC / "index.html").read_text(encoding="utf-8")
    if 'src="assets/' in html or "image-rendering:auto" not in html:
        raise RuntimeError("review delivery regression")
    print(f"Verified table/chair V{VERSION}: exact 84x79 canvas and alpha; rear-facing one-place geometry preserved")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
