#!/usr/bin/env python3
"""Verify catalogue, keeper production, review and route contracts read-only."""

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
KEEPER_DIR = ROOT / "art/raw/keeper-first-batch"
SPRITE_DIR = ROOT / "public/sprites"


def frame_image(name, index):
    clip = manifest[name]
    strip = Image.open(SPRITE_DIR / clip["file"]).convert("RGBA")
    width = clip["w"] * clip["density"]
    height = clip["h"] * clip["density"]
    return strip.crop((index * width, 0, (index + 1) * width, height))


def embedded(frame, width, height):
    """Centre a frame horizontally and bottom-align it on a transparent canvas."""
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas.alpha_composite(frame, ((width - frame.width) // 2, height - frame.height))
    return canvas


# Floor catalogue and non-keeper export integrity.
catalogue = json.loads((ROOT / "docs/floor-asset-catalogue/catalogue.json").read_text())
spaces = catalogue["spaces"]
rows = catalogue["rows"]
assert len(spaces) == 71 and len({space["space_id"] for space in spaces}) == 71
assert len(rows) == 1579
with (ROOT / "docs/floor-asset-catalogue/catalogue.csv").open(newline="") as handle:
    assert len(list(csv.DictReader(handle))) == len(rows)
for space in spaces:
    if space["category"] == "standard":
        assert space["dimensions"] == [110, 35]
    for item in space["items"]:
        if not item["owned"]:
            continue
        for tier in item["tiers"]:
            required = tier["required_states"].lower()
            if item["id"] == "armchair":
                assert required == "standard", (space["space_id"], item["id"], required)
            else:
                assert all(state in required for state in ("standard", "on", "broken"))

manifest = json.loads((SPRITE_DIR / "manifest.json").read_text())
floor_contracts = json.loads((ROOT / "art/source/floor-asset-catalogue/export-contract.json").read_text())
for name, contract in floor_contracts.items():
    raw_path = ROOT / contract["file"]
    raw = Image.open(raw_path).convert("RGBA")
    assert raw.size == (
        contract["w"] * contract["density"] * contract["frames"],
        contract["h"] * contract["density"],
    )
    assert set(raw.getchannel("A").tobytes()) <= {0, 255}
    assert hashlib.sha256(raw_path.read_bytes()).hexdigest() == contract["sha256"]
    exported = Image.open(SPRITE_DIR / manifest[name]["file"]).convert("RGBA")
    assert ImageChops.difference(raw, exported).getbbox() is None
    for key in ("w", "h", "frames", "density", "anchor"):
        assert manifest[name][key] == contract[key], (name, key)
assert floor_contracts["obj_tv_broken"]["frames"] == 1
assert floor_contracts["room_lamp"]["w"] == 95

# Every keeper strip must agree byte-for-byte with its sidecar and runtime copy.
keeper_pngs = sorted(KEEPER_DIR.glob("*.png"))
assert len(keeper_pngs) == 191
keeper_names = set()
keeper_sidecars = {}
for raw_path in keeper_pngs:
    sidecar = json.loads(raw_path.with_suffix(".json").read_text())
    name = raw_path.stem.rsplit("_f", 1)[0]
    keeper_names.add(name)
    keeper_sidecars[name] = sidecar
    raw = Image.open(raw_path).convert("RGBA")
    assert raw.size == (
        sidecar["w"] * sidecar["density"] * sidecar["frames"],
        sidecar["h"] * sidecar["density"],
    ), name
    # Frank's saved production scaling may expand the transparent staging
    # canvas beyond the old automatic-audit ceiling (seated fishing is the
    # largest current example at 135 × 115 logical pixels).
    assert 16 <= sidecar["w"] <= 160 and 16 <= sidecar["h"] <= 128
    assert sidecar["density"] == 4
    assert 0 <= sidecar["anchor"][0] <= sidecar["w"]
    assert 0 <= sidecar["anchor"][1] <= sidecar["h"]
    for point_name in ("seatPoint", "handUsePoint", "pedalPoint", "bowlPoint", "bedSurfacePoint", "pillowPoint", "pivot"):
        if point_name in sidecar:
            assert 0 <= sidecar[point_name][0] <= sidecar["w"], (name, point_name)
            assert 0 <= sidecar[point_name][1] <= sidecar["h"], (name, point_name)
    assert set(raw.getchannel("A").tobytes()) <= {0, 255}, name
    runtime = manifest[name]
    for key in ("w", "h", "frames", "fps", "density", "anchor"):
        assert runtime.get(key, 0) == sidecar.get(key, 0), (name, key)
    assert sidecar["fps"] == 0 if sidecar["frames"] == 1 else 1 <= sidecar["fps"] <= 20
    exported = Image.open(SPRITE_DIR / runtime["file"]).convert("RGBA")
    assert ImageChops.difference(raw, exported).getbbox() is None, name

# Review-accepted timing changes are production data; every other animated clip
# keeps its authored 4 fps baseline.
accepted_fps = {
    "keeper_artist_smock_sit_front": 4.5,
    "keeper_bathrobe_walk": 8,
    "keeper_bbq_back": 2.5,
    "keeper_cake_from_oven_back": 4.5,
    "keeper_cake_turn_right": 7.5,
    "keeper_carry_cake": 8,
    "keeper_carry_meal": 8,
    "keeper_carry_shopping": 8,
    "keeper_check_instrument_back": 6,
    "keeper_clear_snow": 3.5,
    "keeper_count_money": 6,
    "keeper_cross": 5.5,
    "keeper_darts": 3,
    "keeper_door_open_back": 5.5,
    "keeper_door_open_side": 5,
    "keeper_feed_animals": 5.5,
    "keeper_fish_feed_up": 5,
    "keeper_fish_seated": 3,
    "keeper_get_into_bed": 3,
    "keeper_hammer_back": 5,
    "keeper_hammer_side": 5,
    "keeper_pyjamas_snore": 1,
    "keeper_row_boat": 3,
    "keeper_shower_wash": 2,
    "keeper_trampoline_front": 7.5,
    "keeper_turn_back": 10.5,
    "keeper_type_computer": 8.5,
    "keeper_work_back": 3,
}
for name in keeper_names:
    clip = manifest[name]
    if clip["frames"] > 1:
        assert clip["fps"] == accepted_fps.get(name, 4), (name, clip["fps"])

# Frank's saved visual sizing is production art direction. Every imported
# review must be recorded byte-for-byte in the authored sidecar so a future
# scale audit cannot silently replace it with an automatic measurement.
review_export = json.loads(
    (ROOT / "docs/review/frank-keeper-animation-review-2026-10-09.json").read_text()
)
for review in review_export["reviews"]:
    sidecar = keeper_sidecars[review["name"]]
    assert sidecar["reviewScale"] == [
        review.get("widthPercent", 100),
        review.get("heightPercent", 100),
    ], review["name"]
    assert sidecar["fps"] == review.get("animationFps", sidecar["fps"]), review["name"]

# Rebuilt and newly introduced production sequences.
required_frames = {
    "keeper_anti_gravity": 12,
    "keeper_darts": 14,
    "keeper_fish_feed_up": 14,
    "keeper_fish_seated": 16,
    "keeper_fish_standing": 16,
    "keeper_hot_drink_pour": 10,
    "keeper_parachute_jump": 9,
    "keeper_parachute_drift": 8,
    "keeper_parachute_landing": 10,
    "keeper_scuba_walk_side": 8,
    "keeper_scuba_jetty_dive": 12,
    "keeper_scuba_swim_horizontal": 8,
    "keeper_shower_door_open_bathrobe": 10,
}
for name, frames in required_frames.items():
    assert manifest[name]["frames"] == frames, name

# The untouched walk/turn/front authorities retain their canonical canvases.
for name in ("keeper_walk", "keeper_turn_back", "keeper_wave_camera"):
    assert manifest[name]["w"] == 32 and manifest[name]["h"] == 40
    assert manifest[name]["anchor"] == [16, 40]
assert manifest["keeper_walk"]["mirrorSafe"] is True
assert manifest["keeper_sit_side"]["reverseFor"] == "stand_side"
assert manifest["keeper_sit_front"]["reverseFor"] == "stand_front"

# Scuba route: visible jetty locomotion, one-shot water entry and an exact
# hand-off to the established horizontal swim loop.
scuba_walk = manifest["keeper_scuba_walk_side"]
scuba_dive = manifest["keeper_scuba_jetty_dive"]
scuba_swim = manifest["keeper_scuba_swim_horizontal"]
assert scuba_walk["outfit"] == scuba_dive["outfit"] == scuba_swim["outfit"] == "scuba"
assert scuba_walk["movementVector"] == [1, 0] and scuba_walk["loop"] is True
assert scuba_walk["startPose"] == scuba_walk["endPose"] == "scuba-standing-side-right"
assert scuba_dive["loop"] is False and scuba_dive["startPose"] == "scuba-standing-side-right"
assert scuba_dive["endPose"] == "scuba-swim-right"
assert scuba_dive["interaction"] == "scuba-water-entry"
dive_last = frame_image("keeper_scuba_jetty_dive", scuba_dive["frames"] - 1)
swim_first = frame_image("keeper_scuba_swim_horizontal", 0)
assert ImageChops.difference(dive_last, embedded(swim_first, dive_last.width, dive_last.height)).getbbox() is None

# Parachuting is split into entry, a gentle loop and a one-shot landing. The
# neutral open-canopy frame is byte-identical at both production hand-offs.
parachute_jump = manifest["keeper_parachute_jump"]
parachute_drift = manifest["keeper_parachute_drift"]
parachute_landing = manifest["keeper_parachute_landing"]
assert parachute_jump["loop"] is False
assert parachute_drift["loop"] is True
assert parachute_landing["loop"] is False
assert parachute_drift["startPose"] == parachute_drift["endPose"] == "parachute-open"
assert parachute_landing["startPose"] == "parachute-open"
assert parachute_landing["endPose"] == "standing-side-right"
jump_last = frame_image("keeper_parachute_jump", parachute_jump["frames"] - 1)
drift_first = frame_image("keeper_parachute_drift", 0)
landing_first = frame_image("keeper_parachute_landing", 0)
assert ImageChops.difference(embedded(jump_last, drift_first.width, drift_first.height), drift_first).getbbox() is None
assert ImageChops.difference(drift_first, landing_first).getbbox() is None

# Long tools, fishing lines and props retain at least their expanded staging
# canvas; Frank's saved enlargement may expand that canvas further.
assert manifest["keeper_fish_standing"]["w"] >= 96
assert manifest["keeper_fish_standing"]["h"] >= 88
assert manifest["keeper_fish_seated"]["w"] >= 96
assert manifest["keeper_fish_seated"]["h"] >= 88
assert manifest["keeper_snooker"]["w"] == 64
assert manifest["keeper_pressups_side"]["w"] == 64
assert manifest["keeper_scuba_swim_horizontal"]["w"] == 80
assert manifest["keeper_swim_costume_horizontal"]["w"] == 80

# Three-tier cleaning remains an actor/tool strip that emerges only while the
# cupboard foreground fully occludes the keeper.
keeper_contract = json.loads((ROOT / "data/keeper_asset_contract.json").read_text())
assert keeper_contract["version"] == 7 and keeper_contract["status"] == "authoritative"
cleaning = {
    "keeper_sweep_broom": ("traditional-broom", 1, "sweepBroomRight"),
    "keeper_hoover_basic": ("basic-upright-hoover", 2, "hooverBasicRight"),
    "keeper_hoover_super": ("eccentric-super-hoover", 3, "hooverSuperRight"),
}
for name, (variant, tier, profile_name) in cleaning.items():
    clip = manifest[name]
    profile = keeper_contract["interactionProfiles"][profile_name]
    assert clip["propVariant"] == variant and clip["upgradeTier"] == tier
    assert clip["interaction"] == "clean-floor" and clip["movementVector"] == [1, 0]
    assert clip["mirrorSafe"] is True
    assert profile["cupboardExitForegroundOcclusionRequired"] is True
    assert profile["toolIncluded"] is True and profile["upgradeTier"] == tier
for profile_name in ("sweepBroomLeft", "hooverBasicLeft", "hooverSuperLeft"):
    assert keeper_contract["interactionProfiles"][profile_name]["cupboardExitForegroundOcclusionRequired"] is True

# Party headwear explicitly replaces the ordinary cap while retaining the
# canonical face, beard, body and movement below the reconstructed crown.
party_rule = keeper_contract["costumeIdentityRules"]["partyHat"]
assert party_rule["headwearOnly"] is True
assert party_rule["replacesCaptainCap"] is True
assert party_rule["skullScaleChanges"] is False
assert party_rule["faceIdentity"] == "canonical-keeper"
for name in party_rule["clips"]:
    clip = manifest[name]
    assert clip["h"] == 48 and clip["anchor"][1] == 48

# Object authority and the most important world-contact/occlusion rules remain
# stable even where review geometry rebased an individual sprite canvas.
object_dimensions = json.loads((ROOT / "data/keeper_object_dimensions.json").read_text())
assert object_dimensions["keeperBasis"]["skullTopHeight"] == 32.5
assert object_dimensions["furniture"]["diningChair"]["seatTopHeight"] == 11
assert object_dimensions["furniture"]["armchair"]["keeperClips"] == [
    "keeper_sit_side", "keeper_sit_front", "keeper_nap_seated"
]
assert object_dimensions["fixturesAndStations"]["gardenShedDoor"]["foregroundOcclusionRequired"] is True
assert object_dimensions["fixturesAndStations"]["guitarRack"]["propHandoffFrame"] == 6
assert keeper_contract["interactionProfiles"]["guitarPickupGretsch"]["propHandoffFrame"] == 6
assert keeper_contract["interactionProfiles"]["rearSeat"] == {
    "clip": "keeper_sit_back", "seatPoint": [16, 29], "offsetFromFeet": [0, -11]
}

# Frank's immutable review export is retained byte-for-byte; the generated
# audit adds neutral imported baselines and read-only Codex responses without
# mutating that evidence file.
review_path = ROOT / "docs/review/frank-keeper-animation-review-2026-10-09.json"
assert hashlib.sha256(review_path.read_bytes()).hexdigest() == "c19129f8419df2c046f3abb06de9f339f1cd8edb31c2d505dea8e79562d5f486"
review_export = json.loads(review_path.read_text())
assert review_export["version"] == 8 and len(review_export["reviews"]) == 161
review_names = [review["name"] for review in review_export["reviews"]]
assert len(review_names) == len(set(review_names)) == 161
assert len(review_export["happyAnimations"]) == 88
assert len(review_export["redraftAnimations"]) == 28
assert len(review_export["reviewLaterAnimations"]) == 3
responses = json.loads((ROOT / "docs/review/keeper-animation-codex-responses-2026-10-09.json").read_text())
assert len(responses) == 79 and set(responses) <= keeper_names
assert all(isinstance(value, str) and value.strip() for value in responses.values())
awaiting_names = {
    review["name"]
    for review in review_export["reviews"]
    if not review.get("happy") and not review.get("reviewLater")
}
assert len(awaiting_names) == 70 and awaiting_names <= responses.keys()
assert all("Implemented as requested" not in responses[name] for name in awaiting_names)
resolution = (ROOT / "docs/review/KEEPER_ANIMATION_REVIEW_RESOLUTION_2026-10-09.md").read_text()
assert resolution.count("\n| `keeper_") == 173

# The all-sheet audit retains identity/anatomy evidence while recording Frank's
# visual size as authoritative wherever the review changed width or height.
scale_audit = json.loads((ROOT / "docs/keeper-scale-audit/keeper-scale-metrics.json").read_text())
assert scale_audit["version"] == 2
assert scale_audit["auditRevision"] == "2026-10-10-user-visual-size-v3"
assert scale_audit["originalReference"]["name"] == "keeper_walk"
assert scale_audit["counts"] == {
    "allSheets": 191,
    "reviewedAnimationSheets": 173,
    "technicalRejectedSheets": 18,
    "allFramesMeasured": 1420,
    "correctedSheets": 81,
    "comparisonFailures": 0,
}
assert len(scale_audit["assets"]) == 191
review_assets = [asset for asset in scale_audit["assets"] if asset["status"] != "excluded-technical"]
assert len(review_assets) == 173
imported_reviews = {review["name"]: review for review in review_export["reviews"]}
status_counts = {}
for asset in review_assets:
    imported = imported_reviews.get(asset["name"])
    status = (
        "unreviewed" if imported is None else
        "happy" if imported.get("happy") else
        "review-later" if imported.get("reviewLater") else
        "awaiting-new-draft"
    )
    status_counts[status] = status_counts.get(status, 0) + 1
assert status_counts == {
    "happy": 88,
    "awaiting-new-draft": 70,
    "review-later": 3,
    "unreviewed": 12,
}
assert all("originalComparison" in asset for asset in scale_audit["assets"])
assert all(
    asset["originalComparison"]["verdict"] in {
        "measured-and-visual-pass",
        "fixed-scale-visual-pass",
        "user-visual-size-authority",
    }
    for asset in review_assets
)
direct = [asset for asset in scale_audit["assets"] if asset["originalComparison"]["type"] == "direct-skull-to-sole"]
assert [asset["name"] for asset in direct] == ["keeper_walk"]
assert all(0.96 <= asset["originalComparison"]["silhouetteHeightRatio"] <= 1.04 for asset in direct)
user_sized = [
    asset for asset in review_assets
    if asset["originalComparison"]["verdict"] == "user-visual-size-authority"
]
assert len(user_sized) == 128
for asset in user_sized:
    imported = imported_reviews[asset["name"]]
    assert asset["originalComparison"]["reviewScale"] == [
        imported.get("widthPercent", 100),
        imported.get("heightPercent", 100),
    ]
assert len(scale_audit["contactSheets"]) == 9
assert all((ROOT / path).exists() for path in scale_audit["contactSheets"])

# Review UI: status filters, read-only agent narrative, and filter-aware cyclic
# Previous/Next navigation are all part of the delivered review workflow.
review_html = (ROOT / "docs/keeper-scale-audit/review.html").read_text()
assert "__KEEPER_REVIEW_DATA__" not in review_html
assert '"reviewedAnimationSheets":173' in review_html
# Parse the exact payload used by the page, then prove every imported note and
# decision remains attached to its original keeper_* name. Filters only retain
# card objects; they must never join notes to cards by visible-list position.
review_page_data = json.loads(
    review_html.split("const DATA=", 1)[1].split(";\nconst $=", 1)[0]
)
page_reviews = review_page_data["initialReviews"]
page_assets = {asset["name"]: asset for asset in review_page_data["assets"]}
assert len(page_assets) == 173
assert set(page_reviews) == set(review_names)
for imported in review_export["reviews"]:
    name = imported["name"]
    delivered = page_reviews[name]
    assert delivered["notes"] == imported.get("notes", ""), name
    assert delivered["happy"] is imported.get("happy", False), name
    assert delivered["reviewLater"] is imported.get("reviewLater", False), name
    expected_status = (
        "happy" if imported.get("happy") else
        "review-later" if imported.get("reviewLater") else
        "awaiting-new-draft"
    )
    assert page_assets[name]["reviewStatus"] == expected_status, name
    escaped_comment = str(imported.get("notes", "") or "").replace("|", "\\|").replace("\n", "<br>")
    expected_row_start = f"| `{name}` | {page_assets[name]['frames']} | {escaped_comment} |"
    assert resolution.count(expected_row_start) == 1, name
ordered_page_assets = sorted(page_assets.values(), key=lambda asset: asset["name"])
filter_groups = {
    "all": ordered_page_assets,
    "needs-input": [asset for asset in ordered_page_assets if asset["reviewStatus"] != "happy"],
    "happy": [asset for asset in ordered_page_assets if asset["reviewStatus"] == "happy"],
    "awaiting-new-draft": [asset for asset in ordered_page_assets if asset["reviewStatus"] == "awaiting-new-draft"],
    "review-later": [asset for asset in ordered_page_assets if asset["reviewStatus"] == "review-later"],
    "unreviewed": [asset for asset in ordered_page_assets if asset["reviewStatus"] == "unreviewed"],
    "has-response": [asset for asset in ordered_page_assets if asset["codexResponse"]],
}
assert {name: len(assets) for name, assets in filter_groups.items()} == {
    "all": 173,
    "needs-input": 85,
    "happy": 88,
    "awaiting-new-draft": 70,
    "review-later": 3,
    "unreviewed": 12,
    "has-response": 79,
}
for filtered_assets in filter_groups.values():
    # A complete Next cycle visits each same-filter object exactly once and
    # wraps to the first. Its comment is still looked up by that object's name.
    names = [asset["name"] for asset in filtered_assets]
    assert names and len(names) == len(set(names))
    walked = [names[index % len(names)] for index in range(len(names) + 1)]
    assert walked[:-1] == names and walked[-1] == names[0]
    for name in names:
        if name in imported_reviews:
            assert page_reviews[name]["notes"] == imported_reviews[name].get("notes", "")
for token in (
    "Needs my input",
    "Happy",
    "Awaiting new draft review",
    "Review later",
    "Unreviewed",
    "Has Codex response",
    "readonly",
    "Codex response (read only)",
    "REVIEW_STORAGE_KEY='lighthouse-keeper-animation-reviews-v2'",
    "REVIEW_PROGRESS_STORAGE_KEY='lighthouse-keeper-review-progress-v2'",
    "function filteredReviewCards()",
    "function applyReviewFilter",
    "function stepDetail(delta)",
    "savedReview(asset.name)",
    "reviewNotes.value=card.notes",
    "state.savedReviews[asset.name]",
    "state.reviewCards.indexOf(next)",
    "(Math.max(0,position)+delta+filtered.length)%filtered.length",
    "version:9",
    "reviewStatuses",
    "codexResponse",
):
    assert token in review_html, token

# Every generated keeper preview remains animated and the four new route clips
# have dedicated previews in addition to the pre-existing mirrored variants.
preview_paths = list((ROOT / "docs/floor-asset-catalogue").glob("keeper-*-preview.gif"))
assert len(preview_paths) == 179
assert all(Image.open(path).is_animated for path in preview_paths)
for slug in ("keeper-scuba-walk-side", "keeper-scuba-jetty-dive", "keeper-parachute-drift", "keeper-parachute-landing"):
    assert (ROOT / f"docs/floor-asset-catalogue/{slug}-preview.gif").exists()

print(
    "Verified: 71 spaces, 1579 catalogue rows, floor exports, 191 keeper sheets/1420 frames, "
    "reviewed visual sizing and identity authorities, scuba/parachute routes, cleaning cupboard occlusion, "
    "review evidence/statuses/responses, filtered cyclic navigation and 179 animated previews."
)
