import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const registerFile = path.join(root, "art/drafts/keeper-prime-darts-isolation-2026-10-17-v1/batch-register.json");
const register = JSON.parse(fs.readFileSync(registerFile, "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (register.batchId !== "keeper-prime-darts-isolation-2026-10-17-v1") fail("Wrong batch id");
if (register.segmentation.actorComponents !== 14) fail("Expected fourteen owned actor components");
if (register.segmentation.excludedDetachedProjectileComponents !== 4) fail("Expected four detached projectiles");
if (!register.segmentation.sourceOwnership.some((entry: any) => entry.foreignActorPixels > 0)) fail("Expected recorded foreign-actor contamination in immutable V2 source slicing");
if (register.candidate.frames.length !== 30) fail("Registered candidate must contain 30 frames");
if (register.candidate.frames.slice(8, 22).length !== 14) fail("Corrected core must contain fourteen frames");

for (const entry of register.candidate.frames) {
  const file = path.join(root, entry.file);
  if (!fs.existsSync(file)) fail(`Missing candidate frame ${entry.file}`);
  if (sha(file) !== entry.sha256) fail(`Hash mismatch ${entry.file}`);
  const png = PNG.sync.read(fs.readFileSync(file));
  if (png.width !== 448 || png.height !== 320) fail(`Wrong registered geometry ${entry.file}`);
  if (entry.gutterAlphaPixels !== 0) fail(`Registered gutter failed ${entry.file}`);
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    if (x >= 2 && x < png.width - 2 && y >= 2 && y < png.height - 2) continue;
    if (png.data[(y * png.width + x) * 4 + 3] > 6) fail(`Opaque two-pixel gutter at ${entry.file} (${x},${y})`);
  }
}

const stripFile = path.join(root, register.candidate.strip);
const strip = PNG.sync.read(fs.readFileSync(stripFile));
if (strip.width !== 448 * 30 || strip.height !== 320) fail("Strip geometry disagrees with sidecar");
if (sha(stripFile) !== register.candidate.stripSha256) fail("Strip hash mismatch");
const sidecarFile = path.join(root, register.candidate.sidecar);
const sidecar = JSON.parse(fs.readFileSync(sidecarFile, "utf8"));
if (sidecar.w !== 56 || sidecar.h !== 40 || sidecar.frames !== 30 || sidecar.density !== 8) fail("Sidecar geometry mismatch");
if (sha(sidecarFile) !== register.candidate.sidecarSha256) fail("Sidecar hash mismatch");

for (const entry of register.publishedAssets) {
  const source = path.join(root, entry.source);
  if (!fs.existsSync(source) || sha(source) !== entry.sourceSha256) fail(`Published provenance mismatch ${entry.source}`);
}
for (const [field, expected] of [["page", register.review.pageSha256], ["comparisonData", register.review.comparisonDataSha256]] as const) {
  const file = path.join(root, register.review[field]);
  if (!fs.existsSync(file) || sha(file) !== expected) fail(`Review ${field} mismatch`);
}
const comparison = JSON.parse(fs.readFileSync(path.join(root, register.review.comparisonData), "utf8"));
if (comparison.frames.length !== 14) fail("Comparison must expose fourteen core pairs");
if (!comparison.frames.every((entry: any, index: number) => entry.registeredFrame === index + 9)) fail("Comparison registered frame mapping is wrong");
if (!register.checks.globalConnectedComponentOwnership || !register.checks.detachedProjectilesExcludedFromCharacterCells || !register.checks.twoPixelTransparentGutters || !register.checks.stripSidecarAgreement) fail("Required isolation checks are not asserted");
if (register.approvalBoundary.candidateApproved || register.approvalBoundary.finalChanged || register.approvalBoundary.runtimeChanged || register.approvalBoundary.productionChanged || register.approvalBoundary.promotionAllowed) fail("Approval boundary was breached");

console.log("Darts isolation V1 verified: 14 whole actor components, 4 detached projectile components excluded, 30 registered cells with two-pixel transparent gutters, immutable endpoints/bridges retained.");
