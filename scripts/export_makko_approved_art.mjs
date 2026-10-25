import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  renameSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, extname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const REPO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const EXPORT_NAME = "makko-approved-art-2026-10-25";
const EXPORT_ROOT = join(REPO, EXPORT_NAME);
const BUILD_ROOT = join(REPO, `.${EXPORT_NAME}.building`);
const MARKER = ".generated-by-export_makko_approved_art";
const CHECK_ONLY = process.argv.includes("--check");

const records = [];

function repoPath(path) {
  return join(REPO, path);
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function pngDimensions(path) {
  if (extname(path).toLowerCase() !== ".png") return undefined;
  const header = readFileSync(path).subarray(0, 24);
  const signature = "89504e470d0a1a0a";
  if (header.subarray(0, 8).toString("hex") !== signature) {
    throw new Error(`Invalid PNG signature: ${path}`);
  }
  return [header.readUInt32BE(16), header.readUInt32BE(20)];
}

function ensureParent(path) {
  mkdirSync(dirname(path), { recursive: true });
}

function recordFile({ source, destination, category, status, note }) {
  const sourceHash = sha256(source);
  const destinationHash = sha256(destination);
  if (sourceHash !== destinationHash) {
    throw new Error(`Copy hash mismatch: ${destination}`);
  }
  const item = {
    path: relative(BUILD_ROOT, destination),
    category,
    status,
    bytes: statSync(destination).size,
    sha256: destinationHash,
    sourceRepoPath: relative(REPO, source),
    sourceSha256: sourceHash,
  };
  const dimensions = pngDimensions(destination);
  if (dimensions) item.dimensions = dimensions;
  if (note) item.note = note;
  records.push(item);
  return item;
}

function copyOne(sourceRepoPath, destinationPath, metadata) {
  const source = repoPath(sourceRepoPath);
  if (!existsSync(source) || !statSync(source).isFile()) {
    throw new Error(`Missing export source: ${sourceRepoPath}`);
  }
  const destination = join(BUILD_ROOT, destinationPath);
  ensureParent(destination);
  copyFileSync(source, destination);
  return recordFile({ source, destination, ...metadata });
}

function copyTree(sourceRepoPath, destinationPath, metadata, filter = () => true) {
  const sourceRoot = repoPath(sourceRepoPath);
  const walk = (directory) => {
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      const fullPath = join(directory, entry.name);
      const sourceRelative = relative(sourceRoot, fullPath);
      if (!filter(sourceRelative, entry)) continue;
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile()) {
        copyOne(
          join(sourceRepoPath, sourceRelative),
          join(destinationPath, sourceRelative),
          metadata,
        );
      }
    }
  };
  walk(sourceRoot);
}

function writeGenerated(destinationPath, value, metadata) {
  const destination = join(BUILD_ROOT, destinationPath);
  ensureParent(destination);
  const text = typeof value === "string" ? value : `${JSON.stringify(value, null, 2)}\n`;
  writeFileSync(destination, text);
  const item = {
    path: destinationPath,
    category: metadata.category,
    status: metadata.status,
    bytes: statSync(destination).size,
    sha256: sha256(destination),
    generated: true,
  };
  if (metadata.note) item.note = metadata.note;
  records.push(item);
  return item;
}

function findArchiveObject(hashPrefix) {
  const bucket = repoPath(join("review-archive/objects", hashPrefix.slice(0, 2)));
  const matches = readdirSync(bucket)
    .filter((name) => name.startsWith(hashPrefix))
    .map((name) => join(bucket, name));
  if (matches.length !== 1) {
    throw new Error(`Expected one archive object for ${hashPrefix}, found ${matches.length}`);
  }
  const fullHash = matches[0].split("/").at(-1).split(".")[0];
  if (sha256(matches[0]) !== fullHash) {
    throw new Error(`Archive object filename/hash mismatch: ${matches[0]}`);
  }
  return { path: matches[0], sha256: fullHash };
}

function copyArchiveObject(archiveObject, destinationPath, metadata) {
  const destination = join(BUILD_ROOT, destinationPath);
  ensureParent(destination);
  copyFileSync(archiveObject.path, destination);
  return recordFile({ source: archiveObject.path, destination, ...metadata });
}

function safeSlug(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function exportConceptArt() {
  const metadata = {
    category: "original-concept-art",
    status: "historical-reference-requested-by-frank",
    note: "Original concept/reference art; not represented as current production authority.",
  };
  const clean = (path) => !path.split("/").includes(".DS_Store") && !path.endsWith(".DS_Store");
  copyTree("style_b_pixel", "01_original_concept_art/style_b_pixel", metadata, clean);
  copyTree("art/background", "01_original_concept_art/lighthouse_background_concepts", metadata, clean);
}

function exportPrimeIdentity() {
  const metadata = {
    category: "prime-keeper-identity",
    status: "approved-authority",
  };
  const copies = [
    [
      "art/drafts/keeper-prime-master-2026-10-12-v1/sources/keeper-prime-master-front-generated.png",
      "02_prime_keeper/01_approved_identity/front/keeper-prime-master-front-high-resolution.png",
    ],
    [
      "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png",
      "02_prime_keeper/01_approved_identity/front/keeper-prime-neutral-front-256x320.png",
    ],
    [
      "art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.json",
      "02_prime_keeper/01_approved_identity/front/keeper-prime-neutral-front-256x320.json",
    ],
    [
      "art/drafts/keeper-prime-master-2026-10-12-v1/references/frame6-identity-authority.png",
      "02_prime_keeper/01_approved_identity/front/frame6-identity-authority.png",
    ],
    [
      "art/drafts/keeper-prime-master-2026-10-12-v1/references/v11-rendering-quality-reference.png",
      "02_prime_keeper/01_approved_identity/front/rendering-quality-reference.png",
    ],
    [
      "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/sources/keeper-prime-back-user-approved-rear-boots.png",
      "02_prime_keeper/01_approved_identity/back/keeper-prime-back-high-resolution-approved-boots.png",
    ],
    [
      "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png",
      "02_prime_keeper/01_approved_identity/back/keeper-prime-neutral-back-256x320.png",
    ],
    [
      "art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.json",
      "02_prime_keeper/01_approved_identity/back/keeper-prime-neutral-back-256x320.json",
    ],
    [
      "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/sources/keeper-prime-side-right-rigged-clean-master.png",
      "02_prime_keeper/01_approved_identity/side-right/keeper-prime-side-right-clean-master.png",
    ],
    [
      "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png",
      "02_prime_keeper/01_approved_identity/side-right/keeper-prime-neutral-side-right-256x320.png",
    ],
    [
      "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.json",
      "02_prime_keeper/01_approved_identity/side-right/keeper-prime-neutral-side-right-256x320.json",
    ],
  ];
  for (const [source, destination] of copies) copyOne(source, destination, metadata);
}

function exportPrimeRuntimeSheets() {
  copyTree(
    "art/raw/keeper-prime-runtime-v1",
    "02_prime_keeper/02_ready_to_import_runtime_sheets",
    {
      category: "prime-keeper-runtime-sheets",
      status: "approved-and-runtime-promoted",
      note: "PNG sheets are density 4. JSON sidecars carry logical cell size, density, frames, fps, loop, anchors and source hashes.",
    },
  );
  copyOne(
    "data/keeper_prime_runtime_bank.json",
    "02_prime_keeper/02_ready_to_import_runtime_sheets/runtime-bank.json",
    { category: "prime-keeper-runtime-sheets", status: "approved-and-runtime-promoted" },
  );
}

function exportApprovedPrimeRoutes() {
  const catalogue = JSON.parse(readFileSync(repoPath("public/prime-keeper-animations/catalogue.json"), "utf8"));
  copyOne(
    "public/prime-keeper-animations/catalogue.json",
    "02_prime_keeper/03_approved_review_routes/catalogue.json",
    { category: "prime-keeper-approved-routes", status: "approved-authority" },
  );

  catalogue.clips.forEach((clip, clipIndex) => {
    const folder = `${String(clipIndex + 1).padStart(2, "0")}_${safeSlug(clip.id)}`;
    const exportedFrames = clip.frames.map((frame, frameIndex) => {
      const match = frame.src.match(/([0-9a-f]{16})\.[^.]+$/);
      if (!match) throw new Error(`Cannot resolve content hash from ${frame.src}`);
      const archiveObject = findArchiveObject(match[1]);
      const extension = extname(archiveObject.path);
      const filename = `frame-${String(frameIndex + 1).padStart(3, "0")}-${archiveObject.sha256.slice(0, 16)}${extension}`;
      const destination = `02_prime_keeper/03_approved_review_routes/${folder}/frames/${filename}`;
      const record = copyArchiveObject(archiveObject, destination, {
        category: "prime-keeper-approved-routes",
        status: "approved-authority",
        note: `${clip.version}: ${frame.label || `frame ${frameIndex + 1}`}`,
      });
      return {
        index: frameIndex + 1,
        file: `frames/${filename}`,
        sha256: record.sha256,
        durationMs: frame.durationMs,
        label: frame.label || null,
        dimensions: record.dimensions,
        originalReviewUrl: frame.src,
      };
    });
    writeGenerated(
      `02_prime_keeper/03_approved_review_routes/${folder}/animation.json`,
      {
        schema: "lighthouse-keeper/makko-frame-sequence@1",
        id: clip.id,
        title: clip.title,
        version: clip.version,
        category: clip.category,
        approvedBy: clip.approvedBy,
        approvedOn: clip.approvedOn,
        scope: clip.scope,
        loop: clip.loop,
        startPose: clip.startPose,
        endPose: clip.endPose,
        reviewUrl: clip.reviewUrl,
        frames: exportedFrames,
      },
      { category: "prime-keeper-approved-routes", status: "approved-authority" },
    );
  });
}

function exportApprovedV12Sequences() {
  const data = JSON.parse(readFileSync(repoPath("data/keeper_prime_animation_drafts_v12.json"), "utf8"));
  const approval = JSON.parse(
    readFileSync(repoPath("docs/review/keeper-prime-morning-drafts-v12-approval-2026-10-23.json"), "utf8"),
  );
  const approvedById = new Map(approval.approvedSequences.map((sequence) => [sequence.id, sequence]));

  for (const sequence of data.sequences) {
    const approved = approvedById.get(sequence.id);
    if (!approved) throw new Error(`V12 sequence lacks approval entry: ${sequence.id}`);
    const stripHash = sha256(repoPath(sequence.draftStrip.path));
    if (stripHash !== approved.stripSha256 || stripHash !== sequence.draftStrip.sha256) {
      throw new Error(`V12 strip approval hash mismatch: ${sequence.id}`);
    }
    const folder = `02_prime_keeper/04_approved_v12_sequences/${safeSlug(sequence.id)}`;
    const stripName = `${sequence.id}.png`;
    const record = copyOne(sequence.draftStrip.path, `${folder}/${stripName}`, {
      category: "prime-keeper-approved-v12-sequences",
      status: "approved-review-authority",
    });
    const cell = sequence.frames[0].cell;
    if (!sequence.frames.every((frame) => frame.cell[0] === cell[0] && frame.cell[1] === cell[1])) {
      throw new Error(`V12 sequence mixes cell geometries: ${sequence.id}`);
    }
    const expectedWidth = sequence.frames.length * cell[0];
    if (record.dimensions[0] !== expectedWidth || record.dimensions[1] !== cell[1]) {
      throw new Error(`V12 strip geometry mismatch: ${sequence.id}`);
    }
    writeGenerated(
      `${folder}/${sequence.id}.json`,
      {
        schema: "lighthouse-keeper/makko-horizontal-strip@1",
        id: sequence.id,
        title: sequence.title,
        approvedBy: "Frank",
        approvedOn: approval.reviewedOn,
        file: stripName,
        sha256: approved.stripSha256,
        cell,
        anchor: data.dimensions.anchor,
        frames: sequence.frames.length,
        fps: sequence.fps,
        loop: sequence.id.includes("cook") || sequence.id.includes("brush"),
        startPose: sequence.startPose,
        endPose: sequence.endPose,
        frameData: sequence.frames.map((frame, index) => ({
          index: index + 1,
          label: frame.label,
          durationMs: frame.durationMs,
          sourceSha256: frame.sha256,
        })),
      },
      { category: "prime-keeper-approved-v12-sequences", status: "approved-review-authority" },
    );
  }
}

function exportLegacyApprovedAnimations() {
  const reviewDrafts = JSON.parse(readFileSync(repoPath("data/keeper_review_drafts.json"), "utf8"));
  const promoted = reviewDrafts.drafts.filter((entry) => entry.status === "promoted-review-draft");
  if (promoted.length !== 10) {
    throw new Error(`Expected 10 legacy canonical promotions, found ${promoted.length}`);
  }
  const catalogue = [];
  for (const entry of promoted) {
    const register = JSON.parse(readFileSync(repoPath(entry.register), "utf8"));
    if (register.status !== "promoted-review-draft" || register.animation !== entry.name) {
      throw new Error(`Legacy promotion register mismatch: ${entry.name}`);
    }
    if (sha256(repoPath(register.promotion.strip)) !== register.promotion.stripSha256) {
      throw new Error(`Legacy promoted strip hash mismatch: ${entry.name}`);
    }
    if (sha256(repoPath(register.promotion.sidecar)) !== register.promotion.sidecarSha256) {
      throw new Error(`Legacy promoted sidecar hash mismatch: ${entry.name}`);
    }
    const folder = `02_prime_keeper/05_approved_legacy_canonical_sheets/${entry.name}`;
    const stripName = register.promotion.strip.split("/").at(-1);
    const sidecarName = register.promotion.sidecar.split("/").at(-1);
    copyOne(register.promotion.strip, `${folder}/${stripName}`, {
      category: "legacy-approved-keeper-sheets",
      status: "frank-selected-canonical-legacy",
      note: register.selection,
    });
    copyOne(register.promotion.sidecar, `${folder}/${sidecarName}`, {
      category: "legacy-approved-keeper-sheets",
      status: "frank-selected-canonical-legacy",
    });
    catalogue.push({
      id: entry.name,
      status: "Frank-selected canonical legacy animation",
      strip: `${entry.name}/${stripName}`,
      stripSha256: register.promotion.stripSha256,
      sidecar: `${entry.name}/${sidecarName}`,
      sidecarSha256: register.promotion.sidecarSha256,
      selection: register.selection,
      register: entry.register,
    });
  }
  writeGenerated(
    "02_prime_keeper/05_approved_legacy_canonical_sheets/catalogue.json",
    {
      schema: "lighthouse-keeper/makko-approved-legacy-keeper-sheets@1",
      count: catalogue.length,
      note: "These exact-name selections were approved and canonical before Prime Keeper superseded the legacy character direction. Keep them separate from the Prime bank.",
      animations: catalogue,
    },
    { category: "legacy-approved-keeper-sheets", status: "frank-selected-canonical-legacy" },
  );
}

function exportKitchen() {
  const approved = { category: "approved-kitchen", status: "approved-authority" };
  copyOne(
    "art/source/kitchen-warm-ligne-claire-family-2026-10-24-v4-on-food-corrected.png",
    "03_approved_kitchen/01_native_visual_master/kitchen-warm-ligne-claire-family-v4-master.png",
    approved,
  );
  copyOne(
    "art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4/evidence/exact-six-bay-native-runs.png",
    "03_approved_kitchen/01_native_visual_master/exact-six-bay-native-runs.png",
    approved,
  );
  copyOne(
    "art/drafts/kitchen-room-layout-review-2026-10-24-v4/native-assets/fitted-units-static-native.png",
    "03_approved_kitchen/02_locked_fitted_units/fitted-units-static-native-1368x284.png",
    {
      category: "approved-kitchen",
      status: "approved-and-locked",
      note: "Exact locked fitted-unit base. Do not redraw, move, scale, resample or recolour.",
    },
  );
  copyTree(
    "art/raw/kitchen-warm-ligne-claire-runtime-v1",
    "03_approved_kitchen/03_runtime_compatibility_assets",
    {
      category: "approved-kitchen",
      status: "approved-runtime-compatibility",
      note: "84x74 compatibility bodies and 40-frame light-only animation strips; the native master remains the visual authority.",
    },
  );
  for (const filename of [
    "dishwasher-broken-red-lights-preview.gif",
    "oven-broken-cavity-light-preview.gif",
    "exact-84x74-all-state-contact-sheet.png",
  ]) {
    copyOne(
      `art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4/evidence/${filename}`,
      `03_approved_kitchen/04_previews/${filename}`,
      { category: "approved-kitchen", status: "approved-evidence" },
    );
  }
  for (const source of [
    "art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4/manifest.json",
    "art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4/batch-register.json",
    "data/kitchen_asset_contract_v1.json",
    "data/kitchen_room_grid_contract_v2.json",
    "data/kitchen_runtime_promotion_v1.json",
  ]) {
    copyOne(source, `03_approved_kitchen/05_contracts/${source.split("/").at(-1)}`, approved);
  }
}

function exportApprovedActivityPictures() {
  const catalogue = JSON.parse(readFileSync(repoPath("data/activity-stories/pictures.json"), "utf8"));
  const selected = [];
  const explicitApproval = /^(Approved|Frank-approved|Frank-requested)/;

  for (const [id, picture] of Object.entries(catalogue.pictures)) {
    const version = picture.versions.find((candidate) => candidate.v === picture.current);
    if (!version || !explicitApproval.test(version.note || "")) continue;
    const source = version.url.replace(/^\/activity-stories\/repo\//, "");
    if (source === version.url) throw new Error(`Unexpected activity picture URL: ${version.url}`);
    const sourceHash = sha256(repoPath(source));
    if (sourceHash !== version.sha256) throw new Error(`Activity picture hash mismatch: ${id}`);
    const filename = `${id}-v${version.v}.png`;
    copyOne(source, `04_approved_activity_story_art/${picture.family}/${filename}`, {
      category: "approved-activity-story-art",
      status: "approved-current-version",
      note: version.note,
    });
    selected.push({
      id,
      label: picture.label,
      family: picture.family,
      kind: picture.kind,
      version: version.v,
      file: `${picture.family}/${filename}`,
      sha256: version.sha256,
      cell: version.cell,
      bounds: version.bounds,
      note: version.note,
      sourceRepoPath: source,
    });
  }

  if (selected.length !== 84) {
    throw new Error(`Expected 84 explicitly approved current activity pictures, found ${selected.length}`);
  }
  writeGenerated(
    "04_approved_activity_story_art/catalogue.json",
    {
      schema: "lighthouse-keeper/makko-approved-activity-pictures@1",
      count: selected.length,
      selectionRule: "Current catalogue version with a note beginning Approved, Frank-approved or Frank-requested.",
      pictures: selected,
    },
    { category: "approved-activity-story-art", status: "approved-current-version" },
  );
}

function exportApprovalRecords() {
  const reviewDir = repoPath("docs/review");
  for (const name of readdirSync(reviewDir).filter((name) => name.includes("approval") && name.endsWith(".json")).sort()) {
    copyOne(`docs/review/${name}`, `00_approval_records/${name}`, {
      category: "approval-record",
      status: "source-of-truth",
    });
  }
  for (const source of [
    "docs/KITCHEN_ASSET_AUTHORITY.md",
    "docs/PRIME_KEEPER_ANIMATION_LIBRARY_2026-10-21.md",
    "docs/KEEPER_ANIMATION_HANDOFF.md",
  ]) {
    copyOne(source, `00_approval_records/${source.split("/").at(-1)}`, {
      category: "authority-document",
      status: "source-of-truth",
    });
  }
}

function exportEarlyProductionEnvironment() {
  copyTree(
    "art/raw/first-production-batch",
    "05_early_production_environment",
    {
      category: "early-production-environment",
      status: "production-delivery-order-item-1",
      note: "Original production shell stripes and three room plates; retained as usable project history, not as the current kitchen visual authority.",
    },
    (path) => !path.endsWith(".DS_Store"),
  );
}

function rootReadme() {
  const categoryCounts = Object.fromEntries(
    [...new Set(records.map((record) => record.category))].sort().map((category) => [
      category,
      records.filter((record) => record.category === category).length,
    ]),
  );
  return `# Lighthouse Keeper — approved artwork export for Makko

Built 25 October 2026 from hash-pinned repository authorities. This is a copied,
self-contained handoff: deleting it will not alter the Lighthouse Keeper project.

## Start here

- \`02_prime_keeper/02_ready_to_import_runtime_sheets\` contains 27 promoted
  horizontal sprite sheets and matching JSON sidecars. The sidecars specify
  logical cell size, density, frame count, fps, loop, anchor and provenance.
- \`02_prime_keeper/03_approved_review_routes\` contains all 14 approved playable
  review authorities as numbered PNG frames with per-route \`animation.json\`.
- \`02_prime_keeper/04_approved_v12_sequences\` contains the ten complete
  sequences Frank approved on 23 October as horizontal strips plus compact
  import metadata.
- \`02_prime_keeper/05_approved_legacy_canonical_sheets\` contains the ten
  exact-name legacy animations Frank selected and made canonical before Prime
  Keeper superseded that character direction. They are isolated from Prime to
  prevent accidental visual mixing.
- \`03_approved_kitchen/01_native_visual_master\` is the kitchen Frank loved and
  approved. The 1536 × 1024 V4 master is the visual authority.
- \`03_approved_kitchen/02_locked_fitted_units\` is the exact immutable 1368 × 284
  fitted-unit base. It must not be redrawn, moved, scaled, resampled or recoloured.
- \`04_approved_activity_story_art\` contains the 84 current picture versions
  whose catalogue explicitly says Approved, Frank-approved or Frank-requested.
- \`01_original_concept_art\` is included because Frank specifically requested
  the original concepts. It is historical reference, not current production art.
- \`05_early_production_environment\` contains the original production shell
  stripes and room plates.

## Deliberate exclusions

Rejected and superseded drafts, untracked experiments, the held-tool feasibility
proxy (its motion concept was approved but its artwork was not), unapproved loose
kitchen/furniture candidates, and the broad legacy Keeper sprite bank are not in
this export. Their presence would make Makko learn conflicting character and room
designs—the problem this package is intended to avoid.

## Integrity

\`MANIFEST.json\` records every file, its SHA-256, source repository path and
approval classification. \`CHECKSUMS.sha256\` can be checked with:

\`shasum -a 256 -c CHECKSUMS.sha256\`

Repository command: \`npm run verify:makko-export\`.

## File counts by class

${Object.entries(categoryCounts).map(([category, count]) => `- ${category}: ${count}`).join("\n")}
`;
}

function finalise() {
  writeGenerated("README.md", rootReadme(), {
    category: "handoff-documentation",
    status: "generated",
  });

  const manifestRecords = [...records].sort((a, b) => a.path.localeCompare(b.path));
  const manifest = {
    schema: "lighthouse-keeper/makko-approved-art-export@1",
    exportName: EXPORT_NAME,
    builtOn: "2026-10-25",
    sourceBranch: "main",
    sourceCommit: execFileSync("git", ["rev-parse", "HEAD"], { cwd: REPO, encoding: "utf8" }).trim(),
    selectionPolicy: {
      approvedArt: "Explicit approval records, approved Prime library/runtime registers, locked kitchen authority, or current activity picture notes recording Frank approval/request.",
      concepts: "Original style_b_pixel and lighthouse background concepts included by explicit user request and labelled historical.",
      excluded: "Rejected, superseded, untracked or merely review-candidate artwork.",
    },
    summary: {
      files: manifestRecords.length,
      bytes: manifestRecords.reduce((total, record) => total + record.bytes, 0),
      primeRuntimeSheets: 27,
      approvedPrimeRoutes: 14,
      approvedV12Sequences: 10,
      legacyApprovedAnimations: 10,
      approvedActivityPictures: 84,
    },
    files: manifestRecords,
  };
  const manifestPath = join(BUILD_ROOT, "MANIFEST.json");
  writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
  const checksums = manifestRecords.map((record) => `${record.sha256}  ${record.path}`).join("\n");
  writeFileSync(join(BUILD_ROOT, "CHECKSUMS.sha256"), `${checksums}\n`);
  writeFileSync(join(BUILD_ROOT, MARKER), "Generated by scripts/export_makko_approved_art.mjs\n");
}

function verifyExisting() {
  if (!existsSync(EXPORT_ROOT)) throw new Error(`Export folder does not exist: ${EXPORT_ROOT}`);
  if (!existsSync(join(EXPORT_ROOT, MARKER))) throw new Error("Export marker is missing; refusing to verify an unknown folder.");
  const manifest = JSON.parse(readFileSync(join(EXPORT_ROOT, "MANIFEST.json"), "utf8"));
  for (const record of manifest.files) {
    const exported = join(EXPORT_ROOT, record.path);
    if (!existsSync(exported)) throw new Error(`Missing exported file: ${record.path}`);
    if (sha256(exported) !== record.sha256) throw new Error(`Export hash mismatch: ${record.path}`);
    if (record.sourceRepoPath) {
      const source = repoPath(record.sourceRepoPath);
      if (!existsSync(source)) throw new Error(`Missing source file: ${record.sourceRepoPath}`);
      if (sha256(source) !== record.sourceSha256) throw new Error(`Source changed: ${record.sourceRepoPath}`);
    }
  }
  console.log(`Makko export verified: ${manifest.summary.files} files, ${manifest.summary.bytes} bytes`);
}

function build() {
  rmSync(BUILD_ROOT, { recursive: true, force: true });
  mkdirSync(BUILD_ROOT, { recursive: true });

  exportApprovalRecords();
  exportConceptArt();
  exportPrimeIdentity();
  exportPrimeRuntimeSheets();
  exportApprovedPrimeRoutes();
  exportApprovedV12Sequences();
  exportLegacyApprovedAnimations();
  exportKitchen();
  exportApprovedActivityPictures();
  exportEarlyProductionEnvironment();
  finalise();

  if (existsSync(EXPORT_ROOT)) {
    if (!existsSync(join(EXPORT_ROOT, MARKER))) {
      throw new Error(`Refusing to replace unrecognised folder: ${EXPORT_ROOT}`);
    }
    rmSync(EXPORT_ROOT, { recursive: true });
  }
  renameSync(BUILD_ROOT, EXPORT_ROOT);
  verifyExisting();
}

if (CHECK_ONLY) verifyExisting();
else build();
