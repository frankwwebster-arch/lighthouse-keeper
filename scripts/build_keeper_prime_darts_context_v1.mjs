#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-context-v1";
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v1");
const source = path.join(pack, "sources/generated/keeper-prime-darts-14-pose-generated.png");
const sourceMotion = path.join(root, "art/drafts/keeper-darts-user-selected-2026-10-10-v1/source/keeper-darts-user-selected-source.png");
const canonical = path.join(root, "art/raw/keeper-first-batch/keeper_darts_f14.png");
const sideAuthority = path.join(root, "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png");
const walkDir = path.join(root, "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames");
const bridgeDir = path.join(root, "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames");
const turnRegister = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json"), "utf8"));
const turnFiles = turnRegister.approvedCandidate.frames.map((entry) => path.join(root, entry.file));
const timing = JSON.parse(fs.readFileSync(path.join(root, "data/keeper_timing_policy.json"), "utf8")).transitionProfile;
const frameDir = path.join(pack, "drafts/frames");
const evidenceDir = path.join(pack, "evidence");
const publicDir = path.join(root, "public/keeper-review", set);
const publicAssets = path.join(publicDir, "assets");
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "keeper-darts-v1-"));
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

for (const file of [source, sourceMotion, canonical, sideAuthority, ...turnFiles]) {
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

const frameEvidence = [];
const actionFrames = sourceFrames.map((sourceFrame, index) => {
  if (index === 0 || index === 13) {
    const exact = exactAuthorityCell();
    const file = path.join(frameDir, `keeper_prime_darts-right_f${String(index + 1).padStart(2, "0")}.png`);
    fs.writeFileSync(file, PNG.sync.write(exact));
    frameEvidence.push({ frame: index + 1, file: rel(file), sha256: sha(file), source: "exact Prime side-right authority", alphaBounds: alphaBounds(exact), edgeAlphaPixels: transparentEdges(exact), exactEndpoint: true });
    return file;
  }
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
  const file = path.join(frameDir, `keeper_prime_darts-right_f${String(index + 1).padStart(2, "0")}.png`);
  fs.writeFileSync(file, PNG.sync.write(cell));
  const bounds = alphaBounds(cell);
  const actorHeight = Math.round(measurement.actor.height * globalScale);
  const heightDelta = actorHeight - sideBounds.height;
  frameEvidence.push({
    frame: index + 1, file: rel(file), sha256: sha(file), source: rel(source), sourceGridCell: [index % 7 + 1, Math.floor(index / 7) + 1],
    alphaBounds: bounds, registeredActorHeight: actorHeight, primeAuthorityHeight: sideBounds.height, heightDelta, heightDeltaPercent: Number((100 * heightDelta / sideBounds.height).toFixed(3)),
    globalScale: Number(globalScale.toFixed(9)), offset: [dx, dy], edgeAlphaPixels: transparentEdges(cell), exactEndpoint: false,
  });
  if (transparentEdges(cell)) throw new Error(`frame ${index + 1} touches action cell edge`);
  return file;
});

if (sha(actionFrames[0]) !== sha(actionFrames[13])) throw new Error("darts endpoints are not byte-identical");
if (sha(actionFrames[0]) === sha(sideAuthority)) throw new Error("embedded endpoint should differ as a file-sized cell");
if (frameEvidence.some((entry) => Math.abs(entry.heightDeltaPercent ?? 0) > 3.5)) throw new Error("generated actor height drifts more than 3.5% from Prime authority");

const strip = new PNG({ width: ACTION_CELL.width * 14, height: ACTION_CELL.height });
actionFrames.forEach((file, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(file)), strip, 0, 0, ACTION_CELL.width, ACTION_CELL.height, index * ACTION_CELL.width, 0));
const stripFile = path.join(pack, "drafts/keeper_prime_darts-right_f14.png");
fs.writeFileSync(stripFile, PNG.sync.write(strip));
const sidecarFile = path.join(pack, "drafts/keeper_prime_darts-right_f14.json");
writeJson(sidecarFile, {
  schema: "lighthouse-keeper/sprite-sidecar@draft-1", w: 56, h: 40, frames: 14, density: 8, anchor: [28, 40], fps: 6,
  loop: false, facing: "right", interaction: "play-darts", startPose: "standing-side-right", endPose: "standing-side-right",
  exactEndpointSha256: sha(actionFrames[0]), productionPromotionAllowed: false,
});

const contact = new PNG({ width: ACTION_CELL.width * 7, height: ACTION_CELL.height * 2 });
actionFrames.forEach((file, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(file)), contact, 0, 0, ACTION_CELL.width, ACTION_CELL.height, (index % 7) * ACTION_CELL.width, Math.floor(index / 7) * ACTION_CELL.height));
const contactFile = path.join(evidenceDir, "keeper-prime-darts-context-v1-contact-sheet.png");
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
const historical = { canonical: publish(canonical, "historical-canonical"), selected: publish(sourceMotion, "historical-selected"), generated: publish(source, "generated-source"), contact: publish(contactFile, "contact") };

const frame = (asset, phase, label, rootXLp, durationMs, extra = {}) => ({ src: asset.url, phase, label, rootXLp, bottomLp: 52, durationMs, anchorLp: extra.anchorLp ?? [16, 40], flipX: extra.flipX ?? false, ...extra });
const route = [];
let rootX = 79.25;
for (let i = 0; i < 16; i += 1) {
  rootX += 21 / 8;
  route.push(frame(walk[i % 8], "walk approach", `approved Walk V6 · F${i % 8 + 1}`, rootX, 1000 / timing.walkFps));
}
for (const [imageIndex, delta] of [[3, 18], [2, 12], [1, 6], [0, 2]]) {
  rootX += delta / 8;
  route.push(frame(bridge[imageIndex], "smooth stop", `approved deceleration · ${delta} ku`, rootX, 1000 / timing.decelerationFps));
}
if (rootX !== 126) throw new Error(`approach root must finish at 126 lp, got ${rootX}`);
route.push(frame(action[0], "action entry", "exact Prime side neutral", rootX, 120, { anchorLp: ACTION_CELL.anchor }));
const actionDurations = [180, 220, 240, 220, 180, 150, 120, 100, 100, 100, 120, 170, 190, 140];
for (let i = 1; i < action.length; i += 1) route.push(frame(action[i], i < 5 ? "darts anticipation" : i < 11 ? "darts throw" : "darts recovery", `Prime darts candidate · F${i + 1}`, rootX, actionDurations[i], { anchorLp: ACTION_CELL.anchor }));
route.push(frame(action[0], "action exit", "byte-exact Prime side neutral", rootX, 100, { anchorLp: ACTION_CELL.anchor }));
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
if (rootX !== 79.25) throw new Error(`departure must return to 79.25 lp, got ${rootX}`);

const actionStart = route.findIndex((entry) => entry.phase === "action entry");
const actionEnd = route.findLastIndex((entry) => entry.phase === "action exit");
const dataFile = path.join(pack, "keeper-prime-darts-context-v1.json");
writeJson(dataFile, { set, status: "rejected-internal-provenance", rejectionReason: "Middle poses drift toward three-quarter view and snap against the strict Prime side endpoint.", stage: { logicalWidth: 172, logicalHeight: 56, floorBottomLp: 52, intendedGameScaleCssPxPerLp: 4 }, actionRange: [actionStart, actionEnd], route, frameEvidence });

const promptLog = `# Prompt log\n\nBuilt-in image-generation edit/generation used on 17 October 2026.\n\n## References\n\n- Prime side-right identity/rendering authority: \`${rel(sideAuthority)}\`\n- Historical user-selected darts pose sheet, motion geometry only: \`${rel(sourceMotion)}\`\n\n## Prompt\n\nRedraw the fourteen historical darts stages using exactly the Prime Keeper identity, proportions, one-stripe outfit palette and smooth rendering. Keep one fixed adult rotund Keeper, stable head/cap/beard/body/boots and floor anchor, use solid rectangular eyes without glints, separate moustache and restrained mouth, isolate all poses and darts on transparency, prevent duplicated limbs, return to exact neutral, and avoid scenery/text.\n\nThe generated sheet is not accepted as an identity authority. It is globally registered to the Prime height, and its first/last cells are replaced with the byte-identical embedded Prime side-right authority. Middle poses remain review candidates.\n`;
fs.writeFileSync(path.join(pack, "PROMPT_LOG.md"), promptLog);

const registerFile = path.join(pack, "batch-register.json");
const register = {
  schema: "lighthouse-keeper/review-batch@1", batchId: "keeper-prime-darts-context-2026-10-17-v1", status: "rejected-internal-provenance",
  purpose: "First whole-bank reference action shown only inside its complete approved locomotion context.",
  authorities: {
    primeSideRight: { file: rel(sideAuthority), sha256: sha(sideAuthority), role: "identity, scale, palette and exact endpoints" },
    approvedWalk: { directory: rel(walkDir), role: "approach/departure" },
    approvedStopBridge: { directory: rel(bridgeDir), role: "deceleration/acceleration" },
    approvedTurn: { register: rel(path.join(root, "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json")), role: "turn away" },
    fastTiming: { file: "data/keeper_timing_policy.json", sha256: sha(path.join(root, "data/keeper_timing_policy.json")) },
  },
  provenance: {
    canonicalHistorical: { file: rel(canonical), sha256: sha(canonical), role: "rejected visual provenance" },
    userSelectedHistorical: { file: rel(sourceMotion), sha256: sha(sourceMotion), role: "motion geometry only" },
    generatedSource: { file: rel(source), sha256: sha(source), role: "new pose source, not an authority" },
  },
  candidate: { strip: rel(stripFile), stripSha256: sha(stripFile), sidecar: rel(sidecarFile), sidecarSha256: sha(sidecarFile), frames: frameEvidence, routeData: rel(dataFile), routeDataSha256: sha(dataFile) },
  checks: { exactEmbeddedStartEnd: true, globalUniformRegistrationScale: Number(globalScale.toFixed(9)), primeAuthorityVisibleHeightPx: sideBounds.height, maximumAbsoluteMiddleFrameHeightDeltaPercent: Math.max(...frameEvidence.map((entry) => Math.abs(entry.heightDeltaPercent ?? 0))), allCellEdgesTransparent: frameEvidence.every((entry) => entry.edgeAlphaPixels === 0), fullContextRouteRequired: true },
  publishedAssets: published,
  approvalBoundary: { candidateApproved: false, timingApproved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rejectionReason: "Middle action poses drift toward three-quarter view and snap against the strict Prime side endpoint. Preserve for provenance only; use V2 for review.",
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; all authorities and earlier drafts remain unchanged.`,
};

const routeJson = JSON.stringify(route);
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime darts in context V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:20px}header{border-bottom:1px solid #284653}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.panel{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}.rule{border-left:4px solid #72e2a5;background:#14281f;padding:12px}.warn{border-left:4px solid #e8b852;background:#2a2518;padding:12px}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}button,select{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px}button:disabled{opacity:.45}.viewport{overflow-x:auto;padding:8px;background:#061016;border-radius:8px}.stage{position:relative;flex:none;background:linear-gradient(#16303a 0 91%,#3f5660 91% 94%,#18252c 94%);overflow:hidden}.stage:after{content:'';position:absolute;left:0;right:0;top:92.8%;border-top:1px solid #78909a}.actor{position:absolute;object-fit:contain;transform-origin:center}.board{position:absolute;border-radius:50%;background:radial-gradient(circle,#e8d5ae 0 12%,#233640 13% 25%,#d75545 26% 38%,#f1e4c8 39% 51%,#233640 52% 64%,#d75545 65% 77%,#f1e4c8 78%);border:2px solid #0a1014}.phase{font-weight:700;color:#73e3a8}.readout{font-variant-numeric:tabular-nums;min-height:3em}.scales{display:grid;gap:16px}.historical{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.historical article{background:#0b1c25;border-radius:9px;padding:10px}.historical img{width:100%;height:260px;object-fit:contain;background:#061016}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.metric b{display:block;font-size:21px;color:#72e2a5}@media(max-width:900px){.historical,.metrics{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-darts-context-v2/">← Current Darts V2 candidate</a><h1>Keeper Prime darts · complete-context V1</h1><span class="status">Rejected provenance · never promote</span><p>This first attempt is retained only to explain the replacement: its middle poses drift toward three-quarter view and snap against the strict Prime side endpoint.</p></header><main><p class="rule"><strong>Historical evidence:</strong> exact Prime entry and exit were embedded, but the intervening character was not sufficiently consistent. Review V2 instead.</p><section class="panel"><div class="controls"><button id="prev" disabled>← One frame</button><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="next" disabled>One frame →</button><select id="mode" disabled><option value="full">Loop full context</option><option value="action">Loop action only</option><option value="once">Full route once</option></select></div><p id="loading" class="readout">Loading and decoding every unique frame…</p><p id="readout" class="readout"></p></section><section class="panel scales"><div><h2>Large inspection · 8×</h2><div class="viewport"><div class="stage" data-scale="8"></div></div></div><div><h2>Proposed in-game presentation · 4×</h2><div class="viewport"><div class="stage" data-scale="4"></div></div></div><div><h2>Literal logical raster · 1×</h2><div class="viewport"><div class="stage" data-scale="1"></div></div></div></section><section class="metrics"><div class="panel metric"><b>14 action poses</b>inside a 62-frame complete route</div><div class="panel metric"><b>${Math.max(...frameEvidence.map((entry) => Math.abs(entry.heightDeltaPercent ?? 0)))}%</b>maximum registered actor-height deviation</div><div class="panel metric"><b>exact endpoints</b>same embedded Prime pixels before and after</div><div class="panel metric"><b>0 edge alpha</b>all action cells retain transparent gutters</div></section><section class="panel"><h2>Provenance comparison</h2><div class="historical"><article><h3>Original production</h3><img src="${historical.canonical.url}"><p>Historical only; not Prime authority.</p></article><article><h3>Frank-selected earlier motion</h3><img src="${historical.selected.url}"><p>Pose sequence only; no pixels reused as final character authority.</p></article><article><h3>Rejected registered contact sheet</h3><img src="${historical.contact.url}"><p>Retained for comparison; never promote.</p></article></div></section><p class="warn"><strong>Rejection boundary:</strong> V1 is retained as rejected provenance only. V2 is the current unapproved candidate. Final, runtime and production sprites remain unchanged.</p></main><script>
const route=${routeJson};const range=[${actionStart},${actionEnd}];const stages=[...document.querySelectorAll('.stage')];let index=0,timer=null;const controls=[...document.querySelectorAll('button,select')];function setup(){for(const s of stages){const z=+s.dataset.scale;s.style.width=(172*z)+'px';s.style.height=(56*z)+'px';const b=document.createElement('div');b.className='board';b.style.left=(148*z)+'px';b.style.top=(10*z)+'px';b.style.width=(12*z)+'px';b.style.height=(12*z)+'px';s.appendChild(b);const im=document.createElement('img');im.className='actor';s.appendChild(im)}}function render(){const f=route[index];for(const s of stages){const z=+s.dataset.scale,im=s.querySelector('.actor');im.src=f.src;const w=f.anchorLp[0]===28?56:32,h=40;im.style.width=(w*z)+'px';im.style.height=(h*z)+'px';im.style.left=((f.rootXLp-f.anchorLp[0])*z)+'px';im.style.top=((f.bottomLp-f.anchorLp[1])*z)+'px';im.style.transform=f.flipX?'scaleX(-1)':'none'}document.getElementById('readout').innerHTML='<span class="phase">'+f.phase+'</span> · frame '+(index+1)+' / '+route.length+' · '+f.label+' · root '+f.rootXLp.toFixed(3)+' lp'}function bounds(){return document.getElementById('mode').value==='action'?range:[0,route.length-1]}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){const [a,b]=bounds();if(index<a||index>b)index=a;render();const f=route[index];timer=setTimeout(()=>{if(index>=b){if(document.getElementById('mode').value==='once'){stop();return}index=a}else index++;tick()},f.durationMs)}document.getElementById('prev').onclick=()=>{stop();const[a,b]=bounds();index=index<=a?b:index-1;render()};document.getElementById('next').onclick=()=>{stop();const[a,b]=bounds();index=index>=b?a:index+1;render()};document.getElementById('play').onclick=()=>{stop();tick()};document.getElementById('pause').onclick=stop;document.getElementById('mode').onchange=()=>{stop();index=bounds()[0];render()};function preload(src){return new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(resolve).catch(resolve):resolve()};i.onerror=()=>reject(new Error(src));i.src=src})}setup();const unique=[...new Set(route.map(f=>f.src).concat(${JSON.stringify(Object.values(historical).map((entry) => entry.url))}))];Promise.all(unique.map(preload)).then(()=>{controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All '+unique.length+' unique images decoded before playback was enabled.';render();tick()}).catch(e=>document.getElementById('loading').textContent='Review locked: '+e.message)
</script></body></html>`;
const pageFile = path.join(publicDir, "index.html");
fs.writeFileSync(pageFile, html);
register.review = { page: rel(pageFile), pageSha256: sha(pageFile), routeFrames: route.length, actionRange: [actionStart, actionEnd], preloadUniqueImages: true };
writeJson(registerFile, register);
fs.rmSync(tempDir, { recursive: true, force: true });
console.log(JSON.stringify({ set, routeFrames: route.length, actionRange: [actionStart, actionEnd], globalScale, maximumAbsoluteHeightDeltaPercent: register.checks.maximumAbsoluteMiddleFrameHeightDeltaPercent, page: rel(pageFile) }, null, 2));
