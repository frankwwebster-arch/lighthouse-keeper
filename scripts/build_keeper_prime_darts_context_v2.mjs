#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-context-v2";
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2");
const source = path.join(pack, "sources/generated/keeper-prime-darts-14-pose-generated-v2.png");
const rejectedSource = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v1/sources/generated/keeper-prime-darts-14-pose-generated.png");
const sourceMotion = path.join(root, "art/drafts/keeper-darts-user-selected-2026-10-10-v1/source/keeper-darts-user-selected-source.png");
const canonical = path.join(root, "art/raw/keeper-first-batch/keeper_darts_f14.png");
const sideAuthority = path.join(root, "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png");
const walkDir = path.join(root, "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames");
const bridgeDir = path.join(root, "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames");
const turnRegister = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json"), "utf8"));
const turnFiles = turnRegister.approvedCandidate.frames.map((entry) => path.join(root, entry.file));
const postureRegister = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-turn-front-side-2026-10-13-v1/batch-register.json"), "utf8"));
const postureFiles = postureRegister.frames.map((entry) => path.join(root, entry.file));
const collectFrames = {
  partial: path.join(root, "art/drafts/keeper-prime-stair-transitions-2026-10-15-v1/drafts/frames/keeper_prime_door-reach-right_partial.png"),
  full: path.join(root, "art/drafts/keeper-prime-stair-transitions-2026-10-15-v1/drafts/frames/keeper_prime_door-reach-right_full.png"),
};
const timing = JSON.parse(fs.readFileSync(path.join(root, "data/keeper_timing_policy.json"), "utf8")).transitionProfile;
const frameDir = path.join(pack, "drafts/frames");
const evidenceDir = path.join(pack, "evidence");
const publicDir = path.join(root, "public/keeper-review", set);
const publicAssets = path.join(publicDir, "assets");
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "keeper-darts-v1-"));
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

for (const file of [source, rejectedSource, sourceMotion, canonical, sideAuthority, ...turnFiles, ...postureFiles, ...Object.values(collectFrames)]) {
  if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`);
}
fs.mkdirSync(frameDir, { recursive: true });
fs.mkdirSync(evidenceDir, { recursive: true });
fs.rmSync(publicDir, { recursive: true, force: true });
fs.mkdirSync(publicAssets, { recursive: true });

const ACTION_CELL = { width: 448, height: 320, logical: [56, 40], density: 8, anchor: [28, 40] };
const ACTION_ANCHOR_PX = [224, 320];
const FLOOR_Y = 315;
const ALPHA_THRESHOLD = 6;

function alphaBounds(png, threshold = ALPHA_THRESHOLD) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1;
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    if (png.data[(y * png.width + x) * 4 + 3] <= threshold) continue;
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y);
  }
  if (maxX < 0) throw new Error("empty alpha image");
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1 };
}

function components(png) {
  const seen = new Uint8Array(png.width * png.height);
  const found = [];
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    const start = y * png.width + x;
    if (seen[start] || png.data[start * 4 + 3] <= ALPHA_THRESHOLD) continue;
    seen[start] = 1;
    const stack = [start];
    let count = 0, minX = x, maxX = x, minY = y, maxY = y;
    while (stack.length) {
      const current = stack.pop();
      const cy = Math.floor(current / png.width), cx = current % png.width;
      count += 1; minX = Math.min(minX, cx); maxX = Math.max(maxX, cx); minY = Math.min(minY, cy); maxY = Math.max(maxY, cy);
      for (const [nx, ny] of [[cx - 1, cy], [cx + 1, cy], [cx, cy - 1], [cx, cy + 1]]) {
        if (nx < 0 || ny < 0 || nx >= png.width || ny >= png.height) continue;
        const next = ny * png.width + nx;
        if (!seen[next] && png.data[next * 4 + 3] > ALPHA_THRESHOLD) { seen[next] = 1; stack.push(next); }
      }
    }
    found.push({ count, minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1 });
  }
  return found.sort((a, b) => b.count - a.count);
}

function cropGridFrame(sheet, index) {
  const column = index % 7, row = Math.floor(index / 7);
  const x0 = Math.round(column * sheet.width / 7), x1 = Math.round((column + 1) * sheet.width / 7);
  const y0 = Math.round(row * sheet.height / 2), y1 = Math.round((row + 1) * sheet.height / 2);
  const cell = new PNG({ width: x1 - x0, height: y1 - y0 });
  PNG.bitblt(sheet, cell, x0, y0, cell.width, cell.height, 0, 0);
  return cell;
}

function transparentEdges(png) {
  let count = 0;
  for (let x = 0; x < png.width; x += 1) {
    if (png.data[x * 4 + 3] > ALPHA_THRESHOLD) count += 1;
    if (png.data[((png.height - 1) * png.width + x) * 4 + 3] > ALPHA_THRESHOLD) count += 1;
  }
  for (let y = 1; y < png.height - 1; y += 1) {
    if (png.data[(y * png.width) * 4 + 3] > ALPHA_THRESHOLD) count += 1;
    if (png.data[(y * png.width + png.width - 1) * 4 + 3] > ALPHA_THRESHOLD) count += 1;
  }
  return count;
}

const sourceSheet = PNG.sync.read(fs.readFileSync(source));
const sourceFrames = Array.from({ length: 14 }, (_, index) => cropGridFrame(sourceSheet, index));
const sourceMeasurements = sourceFrames.map((frame, index) => {
  const all = alphaBounds(frame);
  const actor = components(frame)[0];
  if (!actor || actor.count < 20000) throw new Error(`frame ${index + 1} missing actor component`);
  const footBandTop = actor.maxY - Math.max(24, Math.round(actor.height * 0.13));
  let footMin = frame.width, footMax = -1;
  for (let y = footBandTop; y <= actor.maxY; y += 1) for (let x = actor.minX; x <= actor.maxX; x += 1) {
    if (frame.data[(y * frame.width + x) * 4 + 3] > ALPHA_THRESHOLD) { footMin = Math.min(footMin, x); footMax = Math.max(footMax, x); }
  }
  return { index, all, actor, footCentreX: (footMin + footMax) / 2 };
});
const orderedHeights = sourceMeasurements.map((entry) => entry.actor.height).sort((a, b) => a - b);
const medianActorHeight = (orderedHeights[6] + orderedHeights[7]) / 2;
const sidePng = PNG.sync.read(fs.readFileSync(sideAuthority));
const sideBounds = alphaBounds(sidePng);
const globalScale = sideBounds.height / medianActorHeight;

function exactAuthorityCell() {
  const cell = new PNG({ width: ACTION_CELL.width, height: ACTION_CELL.height });
  PNG.bitblt(sidePng, cell, 0, 0, sidePng.width, sidePng.height, ACTION_ANCHOR_PX[0] - 128, 0);
  return cell;
}

const generatedEvidence = [];
const generatedCoreFrames = sourceFrames.map((sourceFrame, index) => {
  const measurement = sourceMeasurements[index];
  const cropped = new PNG({ width: measurement.all.width, height: measurement.all.height });
  PNG.bitblt(sourceFrame, cropped, measurement.all.minX, measurement.all.minY, cropped.width, cropped.height, 0, 0);
  const cropFile = path.join(tempDir, `crop-${index + 1}.png`);
  const scaledFile = path.join(tempDir, `scaled-${index + 1}.png`);
  fs.writeFileSync(cropFile, PNG.sync.write(cropped));
  const scaledWidth = Math.max(1, Math.round(cropped.width * globalScale));
  const scaledHeight = Math.max(1, Math.round(cropped.height * globalScale));
  execFileSync("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", cropFile, "-vf", `scale=${scaledWidth}:${scaledHeight}:flags=lanczos,format=rgba`, "-frames:v", "1", scaledFile]);
  const scaled = PNG.sync.read(fs.readFileSync(scaledFile));
  for (let offset = 0; offset < scaled.data.length; offset += 4) if (scaled.data[offset + 3] <= 3) scaled.data.fill(0, offset, offset + 4);
  const footXInCrop = measurement.footCentreX - measurement.all.minX;
  const bodyBottomInCrop = measurement.actor.maxY - measurement.all.minY;
  const dx = Math.round(ACTION_ANCHOR_PX[0] - footXInCrop * globalScale);
  const dy = Math.round(FLOOR_Y - bodyBottomInCrop * globalScale);
  const cell = new PNG({ width: ACTION_CELL.width, height: ACTION_CELL.height });
  PNG.bitblt(scaled, cell, 0, 0, scaled.width, scaled.height, dx, dy);
  const file = path.join(frameDir, `keeper_prime_darts-core-right_f${String(index + 1).padStart(2, "0")}.png`);
  fs.writeFileSync(file, PNG.sync.write(cell));
  const bounds = alphaBounds(cell);
  const actorHeight = Math.round(measurement.actor.height * globalScale);
  const heightDelta = actorHeight - sideBounds.height;
  generatedEvidence.push({
    frame: index + 1, file: rel(file), sha256: sha(file), source: rel(source), sourceGridCell: [index % 7 + 1, Math.floor(index / 7) + 1],
    alphaBounds: bounds, registeredActorHeight: actorHeight, primeAuthorityHeight: sideBounds.height, heightDelta, heightDeltaPercent: Number((100 * heightDelta / sideBounds.height).toFixed(3)),
    globalScale: Number(globalScale.toFixed(9)), offset: [dx, dy], edgeAlphaPixels: transparentEdges(cell), exactEndpoint: false,
  });
  if (transparentEdges(cell)) throw new Error(`frame ${index + 1} touches action cell edge`);
  return file;
});

if (generatedEvidence.some((entry) => Math.abs(entry.heightDeltaPercent ?? 0) > 3.5)) throw new Error("generated actor height drifts more than 3.5% from Prime authority");

function embedAuthority(sourceFile, outputName) {
  const input = PNG.sync.read(fs.readFileSync(sourceFile));
  if (input.width !== 256 || input.height !== 320) throw new Error(`authority cell changed: ${rel(sourceFile)}`);
  const cell = new PNG({ width: ACTION_CELL.width, height: ACTION_CELL.height });
  PNG.bitblt(input, cell, 0, 0, input.width, input.height, ACTION_ANCHOR_PX[0] - 128, 0);
  const output = path.join(frameDir, outputName);
  fs.writeFileSync(output, PNG.sync.write(cell));
  if (transparentEdges(cell)) throw new Error(`${outputName} touches the action cell edge`);
  return output;
}
const exactEndpoint = embedAuthority(sideAuthority, "keeper_prime_darts-right_endpoint.png");
const postureEntry = [6, 5, 4, 3, 2, 1, 0].map((index) => embedAuthority(postureFiles[index], `keeper_prime_darts-right_posture-entry-${index + 1}.png`));
const postureExit = [...postureEntry].reverse();
const actionFrames = [exactEndpoint, ...postureEntry, ...generatedCoreFrames, ...postureExit, exactEndpoint];
const frameEvidence = actionFrames.map((file, index) => ({
  frame: index + 1, file: rel(file), sha256: sha(file), alphaBounds: alphaBounds(PNG.sync.read(fs.readFileSync(file))),
  edgeAlphaPixels: transparentEdges(PNG.sync.read(fs.readFileSync(file))), exactEndpoint: index === 0 || index === actionFrames.length - 1,
  role: index === 0 || index === actionFrames.length - 1 ? "exact Prime side-right endpoint" : index <= 3 || index >= actionFrames.length - 4 ? "approved Prime posture bridge" : "new registered darts core",
}));
if (sha(actionFrames[0]) !== sha(actionFrames.at(-1))) throw new Error("darts endpoints are not byte-identical");

const strip = new PNG({ width: ACTION_CELL.width * actionFrames.length, height: ACTION_CELL.height });
actionFrames.forEach((file, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(file)), strip, 0, 0, ACTION_CELL.width, ACTION_CELL.height, index * ACTION_CELL.width, 0));
const stripFile = path.join(pack, `drafts/keeper_prime_darts-right_f${actionFrames.length}.png`);
fs.writeFileSync(stripFile, PNG.sync.write(strip));
const sidecarFile = path.join(pack, `drafts/keeper_prime_darts-right_f${actionFrames.length}.json`);
writeJson(sidecarFile, {
  schema: "lighthouse-keeper/sprite-sidecar@draft-1", w: 56, h: 40, frames: actionFrames.length, density: 8, anchor: [28, 40], fps: 6,
  loop: false, facing: "right", interaction: "play-darts", startPose: "standing-side-right", endPose: "standing-side-right",
  repeatableCoreFrameRange: [2 + postureEntry.length, 1 + postureEntry.length + generatedCoreFrames.length], exactEndpointSha256: sha(actionFrames[0]), productionPromotionAllowed: false,
});

const contactRows = Math.ceil(actionFrames.length / 7);
const contact = new PNG({ width: ACTION_CELL.width * 7, height: ACTION_CELL.height * contactRows });
actionFrames.forEach((file, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(file)), contact, 0, 0, ACTION_CELL.width, ACTION_CELL.height, (index % 7) * ACTION_CELL.width, Math.floor(index / 7) * ACTION_CELL.height));
const contactFile = path.join(evidenceDir, "keeper-prime-darts-context-v2-contact-sheet.png");
fs.writeFileSync(contactFile, PNG.sync.write(contact));

const published = [];
const byHash = new Map();
function publish(file, label = "frame") {
  const digest = sha(file);
  if (byHash.has(digest)) return byHash.get(digest);
  const ext = path.extname(file);
  const name = `${label}-${digest.slice(0, 16)}${ext}`;
  fs.copyFileSync(file, path.join(publicAssets, name));
  const entry = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); published.push(entry); return entry;
}

const action = actionFrames.map((file) => publish(file, "dart"));
const walk = Array.from({ length: 8 }, (_, i) => publish(path.join(walkDir, `keeper_prime_walk-right_f${i + 1}.png`), "walk"));
const bridge = Array.from({ length: 5 }, (_, i) => publish(path.join(bridgeDir, `keeper_prime_stop-to-walk-right_f${i + 1}.png`), "bridge"));
const turn = turnFiles.map((file) => publish(file, "turn"));
const collect = { partial: publish(collectFrames.partial, "collect"), full: publish(collectFrames.full, "collect") };
const historical = { canonical: publish(canonical, "historical-canonical"), selected: publish(sourceMotion, "historical-selected"), rejectedV1: publish(rejectedSource, "rejected-v1"), generated: publish(source, "generated-source"), contact: publish(contactFile, "contact") };

const frame = (asset, phase, label, rootXLp, durationMs, extra = {}) => ({ src: asset.url, phase, label, rootXLp, bottomLp: 52, durationMs, anchorLp: extra.anchorLp ?? [16, 40], flipX: extra.flipX ?? false, boardDarts: extra.boardDarts ?? 0, ...extra });
const route = [];
let rootX = 83.25;
for (let i = 0; i < 16; i += 1) {
  rootX += 21 / 8;
  route.push(frame(walk[i % 8], "walk approach", `approved Walk V6 · F${i % 8 + 1}`, rootX, 1000 / timing.walkFps));
}
for (const [imageIndex, delta] of [[3, 18], [2, 12], [1, 6], [0, 2]]) {
  rootX += delta / 8;
  route.push(frame(bridge[imageIndex], "smooth stop", `approved deceleration · ${delta} ku`, rootX, 1000 / timing.decelerationFps));
}
if (rootX !== 130) throw new Error(`approach root must finish at 130 lp, got ${rootX}`);
route.push(frame(action[0], "action entry", "byte-exact Prime side neutral", rootX, 110, { anchorLp: ACTION_CELL.anchor }));
for (let i = 1; i <= postureEntry.length; i += 1) route.push(frame(action[i], "darts stance entry", `approved Prime posture bridge · F${i + 1}`, rootX, 1000 / timing.turnFps, { anchorLp: ACTION_CELL.anchor }));
const coreDurations = [170, 220, 230, 210, 175, 145, 115, 95, 95, 95, 115, 150, 175, 150];
let boardDarts = 0;
const coreStartIndex = 1 + postureEntry.length;
for (let throwNumber = 1; throwNumber <= 3; throwNumber += 1) {
  for (let coreIndex = 0; coreIndex < 14; coreIndex += 1) {
    if (coreIndex === 10) boardDarts = throwNumber;
    route.push(frame(action[coreStartIndex + coreIndex], coreIndex < 5 ? `dart ${throwNumber} anticipation` : coreIndex < 11 ? `dart ${throwNumber} flight` : `dart ${throwNumber} recovery`, `Prime darts repeatable core · throw ${throwNumber} · F${coreIndex + 1}`, rootX, coreDurations[coreIndex], { anchorLp: ACTION_CELL.anchor, boardDarts, throwNumber, coreFrame: coreIndex + 1 }));
  }
}
for (let i = coreStartIndex + generatedCoreFrames.length; i < action.length; i += 1) route.push(frame(action[i], i === action.length - 1 ? "action exit" : "darts stance exit", i === action.length - 1 ? "byte-exact Prime side neutral" : "approved Prime posture bridge return", rootX, i === action.length - 1 ? 100 : 1000 / timing.turnFps, { anchorLp: ACTION_CELL.anchor, boardDarts: 3 }));

for (const [imageIndex, delta] of [[1, 2], [2, 6], [3, 12], [4, 18]]) {
  rootX += delta / 8;
  route.push(frame(bridge[imageIndex], "walk to board", `approved acceleration · ${delta} ku`, rootX, 1000 / timing.decelerationFps, { boardDarts: 3 }));
}
for (let i = 0; i < 8; i += 1) {
  rootX += 21 / 8;
  const imageIndex = (i + 1) % 8;
  route.push(frame(walk[imageIndex], "walk to board", `approved Walk V6 · F${imageIndex + 1}`, rootX, 1000 / timing.walkFps, { boardDarts: 3 }));
}
for (const [imageIndex, delta] of [[3, 18], [2, 12], [1, 6], [0, 2]]) {
  rootX += delta / 8;
  route.push(frame(bridge[imageIndex], "stop at board", `approved deceleration · ${delta} ku`, rootX, 1000 / timing.decelerationFps, { boardDarts: 3 }));
}
if (rootX !== 160.5) throw new Error(`collection stop must finish at 160.5 lp, got ${rootX}`);
for (let remaining = 3; remaining >= 1; remaining -= 1) {
  route.push(frame(collect.partial, "collect darts", `approved Prime reach · approach dart ${4 - remaining}`, rootX, 110, { boardDarts: remaining }));
  route.push(frame(collect.full, "collect darts", `approved Prime reach · grasp dart ${4 - remaining}`, rootX, 150, { boardDarts: remaining }));
  route.push(frame(collect.full, "collect darts", `dart ${4 - remaining} removed from board`, rootX, 100, { boardDarts: remaining - 1 }));
  route.push(frame(collect.partial, "collect darts", `approved Prime reach · retract with dart ${4 - remaining}`, rootX, 110, { boardDarts: remaining - 1 }));
}
route.push(frame(bridge[0], "collection exit", "byte-exact Prime side neutral", rootX, 100, { boardDarts: 0 }));
for (let i = 1; i < turn.length; i += 1) route.push(frame(turn[i], "turn away", `approved Turn V9 · F${i + 1}`, rootX, 1000 / timing.turnFps));
for (let i = turn.length - 2; i >= 0; i -= 1) route.push(frame(turn[i], "turn away", `approved Turn V9 mirrored reverse · F${i + 1}`, rootX, 1000 / timing.turnFps, { flipX: true }));
for (const [imageIndex, delta] of [[1, 2], [2, 6], [3, 12], [4, 18]]) {
  rootX -= delta / 8;
  route.push(frame(bridge[imageIndex], "walk departure", `approved acceleration mirrored · ${delta} ku`, rootX, 1000 / timing.decelerationFps, { flipX: true }));
}
for (let i = 0; i < 16; i += 1) {
  rootX -= 21 / 8;
  const imageIndex = (i + 1) % 8;
  route.push(frame(walk[imageIndex], "walk departure", `approved Walk V6 mirrored · F${imageIndex + 1}`, rootX, 1000 / timing.walkFps, { flipX: true }));
}
if (rootX !== 113.75) throw new Error(`departure must return to 113.75 lp, got ${rootX}`);

const actionStart = route.findIndex((entry) => entry.phase === "action entry");
const actionEnd = route.findLastIndex((entry) => entry.phase === "collection exit");
const dataFile = path.join(pack, "keeper-prime-darts-context-v2.json");
writeJson(dataFile, { set, status: "draft-awaiting-frank", stage: { logicalWidth: 172, logicalHeight: 56, floorBottomLp: 52, intendedGameScaleCssPxPerLp: 4, rightWallCupboardDoor: { openPanelXLp: [162, 172], dartboardCentreLp: [166, 17] } }, actionRange: [actionStart, actionEnd], route, frameEvidence, generatedEvidence });

const promptLog = `# Prompt log\n\nBuilt-in image-generation edit/generation used on 17 October 2026.\n\n## References\n\n- Prime side-right identity/rendering authority: \`${rel(sideAuthority)}\`\n- Historical user-selected darts pose sheet, motion geometry only: \`${rel(sourceMotion)}\`\n- Rejected V1 generated source: \`${rel(rejectedSource)}\`\n\n## Prompt\n\nV1 was rejected internally because its action poses drifted from strict profile into three-quarter view. Correct the fourteen-stage sheet so every pose uses the same strict right-facing Prime Keeper head, cap, beard, rotund body, one-stripe outfit, palette, floor anchor and smooth outline quality. Retain only the motion order. Never show a second eye, change width/height, duplicate limbs or lose transparent gutters.\n\nThe V2 generated sheet remains a pose source, not an identity authority. The complete strip adds exact Prime endpoints and approved Prime posture bridges. The repeatable 14-frame core is played three times; stuck darts and collection are route state, not baked into character cells.\n`;
fs.writeFileSync(path.join(pack, "PROMPT_LOG.md"), promptLog);

const registerFile = path.join(pack, "batch-register.json");
const register = {
  schema: "lighthouse-keeper/review-batch@1", batchId: "keeper-prime-darts-context-2026-10-17-v2", status: "draft-awaiting-frank",
  purpose: "Three-dart activity with cupboard-door board, full-stride collection and complete approved locomotion context.",
  authorities: {
    primeSideRight: { file: rel(sideAuthority), sha256: sha(sideAuthority), role: "identity, scale, palette and exact endpoints" },
    approvedWalk: { directory: rel(walkDir), role: "approach/departure" },
    approvedStopBridge: { directory: rel(bridgeDir), role: "deceleration/acceleration" },
    approvedTurn: { register: rel(path.join(root, "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json")), role: "turn away" },
    approvedPostureBridge: { register: rel(path.join(root, "art/drafts/keeper-prime-turn-front-side-2026-10-13-v1/batch-register.json")), role: "controlled side-to-angled darts stance" },
    approvedCollectionReach: Object.fromEntries(Object.entries(collectFrames).map(([key, file]) => [key, { file: rel(file), sha256: sha(file) }])),
    fastTiming: { file: "data/keeper_timing_policy.json", sha256: sha(path.join(root, "data/keeper_timing_policy.json")) },
  },
  provenance: {
    canonicalHistorical: { file: rel(canonical), sha256: sha(canonical), role: "rejected visual provenance" },
    userSelectedHistorical: { file: rel(sourceMotion), sha256: sha(sourceMotion), role: "motion geometry only" },
    rejectedV1GeneratedSource: { file: rel(rejectedSource), sha256: sha(rejectedSource), rejection: "three-quarter identity drift caused a visible snap from the exact side endpoint" },
    generatedSource: { file: rel(source), sha256: sha(source), role: "new pose source, not an authority" },
  },
  candidate: { strip: rel(stripFile), stripSha256: sha(stripFile), sidecar: rel(sidecarFile), sidecarSha256: sha(sidecarFile), frames: frameEvidence, routeData: rel(dataFile), routeDataSha256: sha(dataFile) },
  checks: { exactEmbeddedStartEnd: true, threeIdenticalCoreRepeats: true, boardDartsAccumulateToThree: true, fullStrideWalkToCollection: true, collectionRemovesThreeDarts: true, globalUniformRegistrationScale: Number(globalScale.toFixed(9)), primeAuthorityVisibleHeightPx: sideBounds.height, maximumAbsoluteGeneratedActorHeightDeltaPercent: Math.max(...generatedEvidence.map((entry) => Math.abs(entry.heightDeltaPercent ?? 0))), allCellEdgesTransparent: frameEvidence.every((entry) => entry.edgeAlphaPixels === 0), fullContextRouteRequired: true, ghostOverlaysRequired: true },
  publishedAssets: published,
  approvalBoundary: { candidateApproved: false, timingApproved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  knownReviewRisk: "Middle throwing poses remain new Prime-directed renders. Approved posture bridges remove the direct strict-profile snap, but Frank must still judge face, silhouette and palette continuity in motion.",
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; all authorities and earlier drafts remain unchanged.`,
};

const routeJson = JSON.stringify(route);
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime darts in context V2</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:20px}header{border-bottom:1px solid #284653}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.panel{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}.rule{border-left:4px solid #72e2a5;background:#14281f;padding:12px}.warn{border-left:4px solid #e8b852;background:#2a2518;padding:12px}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}button,select{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px}button:disabled{opacity:.45}.viewport{overflow-x:auto;padding:8px;background:#061016;border-radius:8px}.stage{position:relative;flex:none;background:linear-gradient(#16303a 0 91%,#3f5660 91% 94%,#18252c 94%);overflow:hidden}.stage:after{content:'';position:absolute;left:0;right:0;top:92.8%;border-top:1px solid #78909a}.actor,.ghost{position:absolute;object-fit:contain;transform-origin:center;z-index:4}.ghost{opacity:.23;filter:hue-rotate(115deg) saturate(1.8);z-index:3;pointer-events:none}.adjacent{filter:hue-rotate(280deg) saturate(1.8)}.door{position:absolute;background:#6e5135;border:1px solid #c19a68;z-index:1}.hinge{position:absolute;right:0;width:1px;background:#e8c38d}.board{position:absolute;border-radius:50%;background:radial-gradient(circle,#e8d5ae 0 12%,#233640 13% 25%,#d75545 26% 38%,#f1e4c8 39% 51%,#233640 52% 64%,#d75545 65% 77%,#f1e4c8 78%);border:1px solid #0a1014;z-index:2}.stuck{display:none;position:absolute;background:#d92e2e;border-radius:50% 0 0 50%;z-index:3}.phase{font-weight:700;color:#73e3a8}.readout{font-variant-numeric:tabular-nums;min-height:3em}.scales{display:grid;gap:16px}.historical{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.historical article{background:#0b1c25;border-radius:9px;padding:10px}.historical img{width:100%;height:240px;object-fit:contain;background:#061016}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.metric b{display:block;font-size:21px;color:#72e2a5}@media(max-width:900px){.historical,.metrics{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-context-workbench-v1/">← Context workbench</a><h1>Keeper Prime darts · complete-context V2</h1><span class="status">Review draft · nothing promoted</span><p>Approved walk and stop, controlled stance change, three repeated throws, three darts lodging in the board, a full-stride walk to collect them, exact neutral return, turn and walk away.</p></header><main><p class="rule"><strong>Primary review:</strong> use the ghosts to check that body size, floor contact and head position mesh through every join. The board is mounted on the visible face of the open right-wall cupboard door; its present drawing is measured context, not final furniture art.</p><section class="panel"><div class="controls"><button id="prev" disabled>← One frame</button><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="next" disabled>One frame →</button><select id="mode" disabled><option value="full">Loop full context</option><option value="action">Loop action + collection</option><option value="once">Full route once</option></select><label><input id="primeGhost" type="checkbox"> Exact Prime ghost</label><label><input id="adjacentGhost" type="checkbox"> Previous-frame ghost</label></div><p id="loading" class="readout">Loading and decoding every unique frame…</p><p id="readout" class="readout"></p></section><section class="panel scales"><div><h2>Large inspection · 8×</h2><div class="viewport"><div class="stage" data-scale="8"></div></div></div><div><h2>Proposed in-game presentation · 4×</h2><div class="viewport"><div class="stage" data-scale="4"></div></div></div><div><h2>Literal logical raster · 1×</h2><div class="viewport"><div class="stage" data-scale="1"></div></div></div></section><section class="metrics"><div class="panel metric"><b>3 darts</b>same red-flight set and identical throw core</div><div class="panel metric"><b>${route.length} frames</b>approach through collection and departure</div><div class="panel metric"><b>${register.checks.maximumAbsoluteGeneratedActorHeightDeltaPercent}%</b>maximum generated-height deviation</div><div class="panel metric"><b>exact endpoints</b>same embedded Prime pixels at joins</div></section><section class="panel"><h2>Provenance comparison</h2><div class="historical"><article><h3>Original production</h3><img src="${historical.canonical.url}"><p>Historical only.</p></article><article><h3>Earlier selected motion</h3><img src="${historical.selected.url}"><p>Motion geometry only.</p></article><article><h3>Rejected internal V1</h3><img src="${historical.rejectedV1.url}"><p>Rejected for three-quarter identity drift.</p></article><article><h3>V2 registered strip</h3><img src="${historical.contact.url}"><p>Exact Prime endpoints, approved stance bridges and new throw core.</p></article></div></section><p class="warn"><strong>Approval boundary:</strong> this page proposes Darts V2 only. It does not promote the strip, approve final cupboard/board art, alter Final, or change runtime/production sprites.</p></main><script>
const route=${routeJson},range=[${actionStart},${actionEnd}],primeSrc=${JSON.stringify(action[0].url)},stages=[...document.querySelectorAll('.stage')];let index=0,timer=null;const controls=[...document.querySelectorAll('button,select')];function place(im,f,z){const w=f.anchorLp[0]===28?56:32;im.src=f.src;im.style.width=(w*z)+'px';im.style.height=(40*z)+'px';im.style.left=((f.rootXLp-f.anchorLp[0])*z)+'px';im.style.top=((f.bottomLp-f.anchorLp[1])*z)+'px';im.style.transform=f.flipX?'scaleX(-1)':'none'}function setup(){for(const s of stages){const z=+s.dataset.scale;s.style.width=(172*z)+'px';s.style.height=(56*z)+'px';const d=document.createElement('div');d.className='door';d.style.left=(162*z)+'px';d.style.top=(4*z)+'px';d.style.width=(10*z)+'px';d.style.height=(48*z)+'px';d.innerHTML='<i class="hinge"></i>';s.appendChild(d);const b=document.createElement('div');b.className='board';b.style.left=(162*z)+'px';b.style.top=(13*z)+'px';b.style.width=(8*z)+'px';b.style.height=(8*z)+'px';s.appendChild(b);for(let n=0;n<3;n++){const q=document.createElement('i');q.className='stuck';q.dataset.dart=n;q.style.left=((165.5+n*.45)*z)+'px';q.style.top=((16.1+n*.65)*z)+'px';q.style.width=(2.5*z)+'px';q.style.height=Math.max(1,.5*z)+'px';s.appendChild(q)}for(const cls of ['ghost prime','ghost adjacent','actor']){const im=document.createElement('img');im.className=cls;s.appendChild(im)}}}function render(){const f=route[index],prev=route[Math.max(0,index-1)];for(const s of stages){const z=+s.dataset.scale,actor=s.querySelector('.actor'),prime=s.querySelector('.prime'),adj=s.querySelector('.adjacent');place(actor,f,z);place(adj,prev,z);place(prime,{...f,src:primeSrc,anchorLp:[28,40],flipX:false},z);prime.style.display=document.getElementById('primeGhost').checked?'block':'none';adj.style.display=document.getElementById('adjacentGhost').checked?'block':'none';s.querySelectorAll('.stuck').forEach((d,n)=>d.style.display=n<f.boardDarts?'block':'none')}document.getElementById('readout').innerHTML='<span class="phase">'+f.phase+'</span> · frame '+(index+1)+' / '+route.length+' · '+f.label+' · root '+f.rootXLp.toFixed(3)+' lp · board '+f.boardDarts+'/3'}function bounds(){return document.getElementById('mode').value==='action'?range:[0,route.length-1]}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){const[a,b]=bounds();if(index<a||index>b)index=a;render();const f=route[index];timer=setTimeout(()=>{if(index>=b){if(document.getElementById('mode').value==='once'){stop();return}index=a}else index++;tick()},f.durationMs)}document.getElementById('prev').onclick=()=>{stop();const[a,b]=bounds();index=index<=a?b:index-1;render()};document.getElementById('next').onclick=()=>{stop();const[a,b]=bounds();index=index>=b?a:index+1;render()};document.getElementById('play').onclick=()=>{stop();tick()};document.getElementById('pause').onclick=stop;document.getElementById('mode').onchange=()=>{stop();index=bounds()[0];render()};document.getElementById('primeGhost').onchange=render;document.getElementById('adjacentGhost').onchange=render;function preload(src){return new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(resolve).catch(resolve):resolve()};i.onerror=()=>reject(new Error(src));i.src=src})}setup();const unique=[...new Set(route.map(f=>f.src).concat(primeSrc))];Promise.all(unique.map(preload)).then(()=>{controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All '+unique.length+' unique moving-frame images decoded before playback was enabled.';render();tick()}).catch(e=>document.getElementById('loading').textContent='Review locked: '+e.message)
</script></body></html>`;
const pageFile = path.join(publicDir, "index.html");
fs.writeFileSync(pageFile, html);
register.review = { page: rel(pageFile), pageSha256: sha(pageFile), routeFrames: route.length, actionRange: [actionStart, actionEnd], preloadUniqueImages: true };
writeJson(registerFile, register);
fs.rmSync(tempDir, { recursive: true, force: true });
console.log(JSON.stringify({ set, routeFrames: route.length, actionRange: [actionStart, actionEnd], globalScale, maximumAbsoluteHeightDeltaPercent: register.checks.maximumAbsoluteGeneratedActorHeightDeltaPercent, page: rel(pageFile) }, null, 2));
