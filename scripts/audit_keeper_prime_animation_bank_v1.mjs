#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const manifestPath = path.join(root, "public/sprites/manifest.json");
const sidecarDir = path.join(root, "art/raw/keeper-first-batch");
const outputJson = path.join(root, "data/keeper-prime-animation-bank-audit-v1.json");
const outputMd = path.join(root, "docs/KEEPER_PRIME_ANIMATION_BANK_AUDIT_2026-10-17.md");

const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const endpointAudit = JSON.parse(
  fs.readFileSync(path.join(root, "data/keeper_endpoint_audit.json"), "utf8"),
);

const endpointByClip = new Map();
for (const row of endpointAudit.rows) {
  const rows = endpointByClip.get(row.clip) ?? [];
  rows.push(row);
  endpointByClip.set(row.clip, rows);
}

const componentNames = new Set([
  "keeper_back_arm_l", "keeper_back_arm_r", "keeper_back_head",
  "keeper_back_leg_l", "keeper_back_leg_r", "keeper_back_torso",
  "keeper_front_arm_l", "keeper_front_arm_r", "keeper_front_head_asleep",
  "keeper_front_head_grumpy", "keeper_front_head_happy",
  "keeper_front_head_neutral", "keeper_front_head_open",
  "keeper_front_leg_l", "keeper_front_leg_r", "keeper_front_torso",
  "keeper_reference",
]);

const approvedPrimeAuthorities = [
  "Keeper Prime Master V1",
  "Keeper Prime Orthographic V5",
  "Keeper Prime Walk V7",
  "Keeper Prime Stop→Walk→Stop V2",
  "Keeper Prime Turn Side↔Back V10",
  "Keeper Prime Stair Ascent V17 approval",
  "Keeper Prime Stair Transitions V6",
  "Keeper Prime Stair Descent V2 approval",
  "Keeper Prime Ladder Transitions V4/V5 motion approval",
  "Keeper Prime Seated Six View V1 (review candidate, not yet approved)",
];

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

function outfitFor(name, meta) {
  if (meta.outfit) return meta.outfit;
  const normalized = name.replace(/^keeper_/, "");
  const prefixes = [
    "artist-smock", "light-blue-pyjamas", "cream-bathrobe", "party-hat",
    "mechanic", "old-school-workout-kit", "striped-swimming-costume", "scuba",
    "souwester", "knight", "pirate", "spaceman", "halloween", "tarzan",
    "towel-privacy", "mosaic-privacy", "privacy-foam",
  ];
  for (const prefix of prefixes) {
    if (normalized.startsWith(prefix) || normalized.startsWith(prefix.replaceAll("-", "_"))) {
      return prefix;
    }
  }
  if (/^bathrobe_/.test(normalized)) return "cream-bathrobe";
  if (/^pyjamas_/.test(normalized)) return "light-blue-pyjamas";
  if (/^party_/.test(normalized)) return "party-hat";
  return "standard";
}

function categoryFor(name, meta) {
  const n = name.toLowerCase();
  if (n.includes("_neutral_") || meta.assetRole === "neutral") return "technical-neutral";
  if (/walk|stairs|ladder|parachute|slide|anti_gravity|swim|drive|ride_bike|row_boat/.test(n)) return "locomotion";
  if (/turn|sit_|sitting_turn|enter|exit|pickup|get_into|landing|door_open|walk_into_lift|lift_button/.test(n)) return "transition";
  if (/bored|cross_f|hungry|sad|yawn|idle|wave_camera|dance|party_idle/.test(n)) return "expression";
  if (/seated|nap_|read_|eat_|watch_|piano|snooker|video_game|type_computer/.test(n)) return "seated-action";
  return "interaction";
}

function familyFor(name, meta) {
  const n = `${name} ${meta.outfit ?? ""} ${meta.interaction ?? ""}`.toLowerCase();
  if (/scuba/.test(n)) return "scuba";
  if (/swim|platform_dive|hot_tub/.test(n)) return "swimming";
  if (/old-school-workout-kit|lift_weights|pressups|trampoline/.test(n)) return "gym";
  return null;
}

function treatmentFor(name, meta) {
  if (name === "keeper_count_money") return "excluded-deleted-amendment";
  if (familyFor(name, meta)) return "full-redraw-user-rejected-family";
  if (/neutral/.test(name)) return "prime-redraw-required";
  if (/^[a-z_]+_(walk|turn|sit|reach|carry|pick|enter|exit|open|press|climb)/.test(name.replace(/^keeper_/, ""))) {
    return "motion-skeleton-candidate-only";
  }
  return "partial-motion-salvage-assessment";
}

function routeFor(name, meta, category) {
  const pose = meta.startPose ?? null;
  const endPose = meta.endPose ?? null;
  const needsTurn = pose && !pose.includes("side-right") && !pose.includes("side-left");
  if (category === "technical-neutral") return "authority endpoint only; no isolated action route";
  if (category === "locomotion") return "registered neutral → locomotion join → locomotion → registered neutral";
  return [
    "approved walk",
    "phase-correct stop",
    needsTurn ? `approved turn to ${pose}` : `exact ${pose ?? "declared action pose"} entry`,
    "action entry",
    "action/loop",
    `action exit to exact ${endPose ?? pose ?? "declared neutral"}`,
    needsTurn ? "approved turn to departure side" : "phase-correct walk start",
    "approved walk away",
  ].join(" → ");
}

function endpointSummary(name) {
  const rows = endpointByClip.get(name) ?? [];
  const statuses = [...new Set(rows.map((row) => row.status))].sort();
  return {
    measuredEnds: rows.length,
    statuses,
    maxMismatchPercent: rows.reduce((max, row) => Math.max(max, row.mismatchPercent ?? 0), 0),
    maxLandmarkDelta: rows.reduce((max, row) => Math.max(max, row.landmarkMaxDelta ?? 0), 0),
    remedies: [...new Set(rows.map((row) => row.remedy).filter(Boolean))].sort(),
  };
}

const rows = [];
for (const [name, manifestMeta] of Object.entries(manifest)) {
  if (!name.startsWith("keeper_") || componentNames.has(name)) continue;
  const sidecarPattern = new RegExp(`^${name}_f\\d+\\.json$`);
  const sidecarMatches = fs.readdirSync(sidecarDir).filter((file) => sidecarPattern.test(file));
  if (sidecarMatches.length !== 1) {
    throw new Error(`${name}: expected exactly one raw sidecar, found ${sidecarMatches.length}`);
  }
  const sidecarPath = path.join(sidecarDir, sidecarMatches[0]);
  const meta = JSON.parse(fs.readFileSync(sidecarPath, "utf8"));
  const pngPath = path.join(root, "public/sprites", manifestMeta.file);
  const bytes = fs.readFileSync(pngPath);
  const png = PNG.sync.read(bytes);
  const expected = {
    width: meta.w * meta.frames * meta.density,
    height: meta.h * meta.density,
  };
  const category = categoryFor(name, meta);
  const family = familyFor(name, meta);
  const endpoints = endpointSummary(name);
  const risks = [];
  if (!meta.startPose || !meta.endPose) risks.push("missing-declared-endpoint");
  if (endpoints.statuses.some((status) => status !== "pass")) risks.push("legacy-endpoint-does-not-match-neutral");
  if (png.width !== expected.width || png.height !== expected.height) risks.push("strip-sidecar-geometry-mismatch");
  if (meta.loop && meta.startPose !== meta.endPose) risks.push("loop-pose-mismatch");
  if (meta.outfit && meta.outfit !== "standard") risks.push("costume-route-and-door-occlusion-required");
  if (meta.handUsePoint) risks.push("prop-hand-contact-must-be-remeasured");
  if (meta.seatPoint) risks.push("seat-height-and-furniture-dependency");
  if (family) risks.push(`${family}-family-explicitly-rejected`);
  if (name === "keeper_count_money") risks.push("must-not-regenerate-without-direct-instruction");

  rows.push({
    id: name,
    frameRange: [1, meta.frames],
    frames: meta.frames,
    fps: meta.fps,
    loop: Boolean(meta.loop),
    logicalCell: [meta.w, meta.h],
    density: meta.density,
    anchor: meta.anchor,
    pixelStrip: [png.width, png.height],
    geometryMatchesSidecar: png.width === expected.width && png.height === expected.height,
    sha256: sha256(bytes),
    category,
    family,
    outfit: outfitFor(name, meta),
    facing: meta.facing ?? null,
    interaction: meta.interaction ?? null,
    startPose: meta.startPose ?? null,
    endPose: meta.endPose ?? null,
    mirrorSafe: meta.mirrorSafe ?? null,
    propDependencies: {
      handUsePoint: meta.handUsePoint ?? null,
      lookTargetPoint: meta.lookTargetPoint ?? null,
      seatPoint: meta.seatPoint ?? null,
      movementVector: meta.movementVector ?? null,
    },
    currentFaceAndBodyFamily: "legacy-first-batch-non-prime-production",
    historicalMotionTreatment: treatmentFor(name, meta),
    endpointAudit: endpoints,
    transitionRisks: risks,
    requiredContextRoute: routeFor(name, meta, category),
    sourceSidecar: path.relative(root, sidecarPath),
    runtimeFile: path.relative(root, pngPath),
  });
}

rows.sort((a, b) => a.category.localeCompare(b.category) || a.id.localeCompare(b.id));
const byCategory = Object.fromEntries(
  [...new Set(rows.map((row) => row.category))].sort().map((category) => [category, rows.filter((row) => row.category === category).length]),
);
const byOutfit = Object.fromEntries(
  [...new Set(rows.map((row) => row.outfit))].sort().map((outfit) => [outfit, rows.filter((row) => row.outfit === outfit).length]),
);
const byTreatment = Object.fromEntries(
  [...new Set(rows.map((row) => row.historicalMotionTreatment))].sort().map((treatment) => [treatment, rows.filter((row) => row.historicalMotionTreatment === treatment).length]),
);
const rejected = rows.filter((row) => row.family || row.id === "keeper_count_money").map((row) => row.id);
const audit = {
  schemaVersion: 1,
  generatedOn: "2026-10-17",
  scope: "Every Keeper runtime animation and technical neutral in public/sprites/manifest.json; rig fragments and the reference sheet are excluded.",
  authorityContract: "docs/KEEPER_PRIME_ANIMATION_BANK_NORMALISATION_CONTRACT_2026-10-17.md",
  primeAuthorities: approvedPrimeAuthorities,
  summary: {
    totalRows: rows.length,
    byCategory,
    byOutfit,
    byTreatment,
    legacyEndpointRiskCount: rows.filter((row) => row.transitionRisks.includes("legacy-endpoint-does-not-match-neutral")).length,
    geometryMismatchCount: rows.filter((row) => !row.geometryMatchesSidecar).length,
    explicitlyRejectedOrExcludedCount: rejected.length,
  },
  explicitlyRejectedOrExcluded: rejected,
  rows,
};

fs.writeFileSync(outputJson, `${JSON.stringify(audit, null, 2)}\n`);

const md = [];
md.push("# Keeper Prime animation-bank audit", "", "**Measured:** 17 October 2026  ", "**Status:** read-only inventory and redraft queue; nothing in this audit is promoted.", "");
md.push(`This inventory covers **${rows.length}** production Keeper animations and technical neutrals. Rig fragments and the static reference sheet are intentionally excluded. Every row retains its exact frame range, geometry, outfit, endpoints, dependencies, current rendering family and transition risks in \`data/keeper-prime-animation-bank-audit-v1.json\`.`);
md.push("", "The current production bank is legacy first-batch rendering, not Prime Keeper authority. Historical frames may contribute motion mechanics only. The binding rules are in `docs/KEEPER_PRIME_ANIMATION_BANK_NORMALISATION_CONTRACT_2026-10-17.md`.", "");
md.push("## Counts", "", "| Group | Count |", "|---|---:|");
for (const [key, value] of Object.entries(byCategory)) md.push(`| ${key} | ${value} |`);
md.push(`| **Total** | **${rows.length}** |`, "");
md.push("### Redraft treatment", "", "| Treatment | Count |", "|---|---:|");
for (const [key, value] of Object.entries(byTreatment)) md.push(`| ${key} | ${value} |`);
md.push("", `Legacy endpoint risks: **${audit.summary.legacyEndpointRiskCount}**. Strip/sidecar geometry mismatches: **${audit.summary.geometryMismatchCount}**. Explicitly rejected/excluded entries: **${audit.summary.explicitlyRejectedOrExcludedCount}**.`, "");
md.push("## Explicitly rejected or excluded", "", "Swimming, gym and scuba are full-redraw families. `keeper_count_money` must not be regenerated without a new direct instruction.", "");
for (const id of rejected) md.push(`- \`${id}\``);
md.push("", "## Inventory by review group", "");
for (const category of Object.keys(byCategory)) {
  md.push(`### ${category}`, "", "| Animation | Frames | Outfit | Start → end | Treatment | Main risks |", "|---|---:|---|---|---|---|");
  for (const row of rows.filter((item) => item.category === category)) {
    md.push(`| \`${row.id}\` | ${row.frameRange[0]}–${row.frameRange[1]} @ ${row.fps} fps | ${row.outfit} | ${row.startPose ?? "missing"} → ${row.endPose ?? "missing"} | ${row.historicalMotionTreatment} | ${row.transitionRisks.join(", ") || "none recorded"} |`);
  }
  md.push("");
}
md.push("## Review order", "", "1. Approve the six Prime seated endpoints, then build stand↔sit transitions for all six directions.", "2. Establish one complete standard-outfit action route as the reference implementation: walk → stop → action → exact neutral → walk.", "3. Work through standard standing interactions in small object-specific batches.", "4. Normalise seated actions against the approved seated authorities.", "5. Build costume routes behind door occlusion before costume actions.", "6. Redraw swimming, gym and scuba from first principles after their environments and props are fixed.", "", "No action may be approved from an isolated loop.", "");
fs.writeFileSync(outputMd, `${md.join("\n")}\n`);

console.log(JSON.stringify(audit.summary, null, 2));
